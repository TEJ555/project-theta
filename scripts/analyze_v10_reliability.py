from __future__ import annotations

import argparse
import json
import random
import sqlite3
from pathlib import Path
from statistics import fmean, median
from typing import Any


PLANNED_SEEDS = {6300, 6301, 6302, 6303, 6304, 6305}


def _accuracy(rows: list[dict[str, Any]]) -> float | None:
    return fmean(float(row["correct"]) for row in rows) if rows else None


def _quantile(values: list[float], probability: float) -> float:
    ordered = sorted(values)
    index = (len(ordered) - 1) * probability
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def analyze(database: Path, bootstrap_samples: int = 10_000) -> dict[str, Any]:
    connection = sqlite3.connect(database)
    runs = connection.execute(
        """
        SELECT run_id, seed, status, stop_reason
        FROM runs
        WHERE experiment='multi_body_reliability_v10' AND condition_name='full'
        ORDER BY seed
        """
    ).fetchall()
    seed_results: list[dict[str, Any]] = []
    for run_id, seed, status, stop_reason in runs:
        metrics = dict(connection.execute(
            "SELECT name, value FROM metrics WHERE run_id=?",
            (run_id,),
        ).fetchall())
        step_rows = connection.execute(
            """
            SELECT observation_json, decision_json, hidden_world_json, hidden_body_json
            FROM steps WHERE run_id=? ORDER BY tick
            """,
            (run_id,),
        ).fetchall()
        scored: list[dict[str, Any]] = []
        for observation_json, decision_json, hidden_json, body_json in step_rows:
            observation = json.loads(observation_json)
            decision = json.loads(decision_json)
            hidden = json.loads(hidden_json)
            body = json.loads(body_json)
            task = observation.get("task", {})
            correct_action = hidden.get("correct_action")
            if not correct_action:
                continue
            kind = str(task.get("kind", ""))
            scored.append({
                "family": str(task.get("family_token", "")),
                "kind": kind,
                "correct": decision.get("action") == correct_action,
                "hidden_final_error": (
                    abs(float(body.get("theta")) - float(task.get("target_I7", 0.5)))
                    if kind in {
                        "active_regulation_probe",
                        "active_regulation_transfer_probe",
                    }
                    else None
                ),
            })
        families = sorted({row["family"] for row in scored if row["family"]})
        family_results: list[dict[str, Any]] = []
        for family in families:
            family_rows = [row for row in scored if row["family"] == family]
            exact = [row for row in family_rows if row["kind"] == "active_regulation_probe"]
            transfer = [
                row for row in family_rows
                if row["kind"] == "active_regulation_transfer_probe"
            ]
            interface = [
                row for row in family_rows if row["kind"] == "interface_comprehension_probe"
            ]
            mapping = [row for row in family_rows if row["kind"] == "body_mapping_checkpoint"]
            active = exact + transfer
            family_results.append({
                "family": family,
                "regulation_accuracy": _accuracy(active),
                "exact_accuracy": _accuracy(exact),
                "transfer_accuracy": _accuracy(transfer),
                "interface_accuracy": _accuracy(interface),
                "mapping_accuracy": _accuracy(mapping),
                "hidden_final_error": fmean(
                    float(row["hidden_final_error"]) for row in active
                ) if active else None,
                "denominators": {
                    "regulation": len(active),
                    "exact": len(exact),
                    "transfer": len(transfer),
                    "interface": len(interface),
                    "mapping": len(mapping),
                },
            })
        seed_results.append({
            "seed": int(seed),
            "status": status,
            "stop_reason": stop_reason,
            "metrics": metrics,
            "families": family_results,
        })

    families = [family for seed in seed_results for family in seed["families"]]
    complete = (
        len(seed_results) == len(PLANNED_SEEDS)
        and {seed["seed"] for seed in seed_results} == PLANNED_SEEDS
        and all(seed["status"] == "completed" and seed["stop_reason"] is None for seed in seed_results)
        and all(len(seed["families"]) == 4 for seed in seed_results)
        and all(
            family["denominators"] == {
                "regulation": 16,
                "exact": 8,
                "transfer": 8,
                "interface": 8,
                "mapping": 8,
            }
            for family in families
        )
    )
    seed_regulation = [
        float(seed["metrics"].get("active_regulation_accuracy"))
        for seed in seed_results
        if seed["metrics"].get("active_regulation_accuracy") is not None
    ]
    pooled_regulation = fmean(
        float(family["regulation_accuracy"]) for family in families
    ) if families else None
    pooled_exact = fmean(float(family["exact_accuracy"]) for family in families) if families else None
    pooled_transfer = (
        fmean(float(family["transfer_accuracy"]) for family in families) if families else None
    )
    pooled_interface = (
        fmean(float(family["interface_accuracy"]) for family in families) if families else None
    )
    pooled_mapping = (
        fmean(float(family["mapping_accuracy"]) for family in families) if families else None
    )
    hidden_error = (
        fmean(float(family["hidden_final_error"]) for family in families) if families else None
    )
    hidden_improvement = (
        fmean(float(seed["metrics"].get("hidden_regulation_improvement")) for seed in seed_results)
        if seed_results else None
    )

    bootstrap_interval = None
    if complete:
        rng = random.Random(20260925)
        bootstrap_values: list[float] = []
        by_seed = [seed["families"] for seed in seed_results]
        for _ in range(bootstrap_samples):
            sampled_seeds = [rng.choice(by_seed) for _ in by_seed]
            sampled_families = [
                rng.choice(seed_families) for seed_families in sampled_seeds for _ in range(4)
            ]
            bootstrap_values.append(fmean(
                float(family["regulation_accuracy"]) for family in sampled_families
            ))
        bootstrap_interval = {
            "samples": bootstrap_samples,
            "seed": 20260925,
            "lower_95": round(_quantile(bootstrap_values, 0.025), 6),
            "upper_95": round(_quantile(bootstrap_values, 0.975), 6),
        }

    invalid_actions = sum(float(seed["metrics"].get("invalid_action_count", 0)) for seed in seed_results)
    welfare_stops = sum(float(seed["metrics"].get("welfare_stops", 0)) for seed in seed_results)
    provider_rows = connection.execute(
        """
        SELECT a.provider_id, a.metadata_json
        FROM api_calls a JOIN runs r ON r.run_id=a.run_id
        WHERE r.experiment='multi_body_reliability_v10'
        """
    ).fetchall()
    provider_metadata = [json.loads(row[1]) for row in provider_rows]
    provider_ids = [str(row[0]) for row in provider_rows if row[0]]
    required_model_only = {
        str(row.get("model")) for row in provider_metadata
    } == {"openai/gpt-oss-20b"}
    gates = {
        "complete_execution": (
            complete
            and len(provider_rows) == 1056
            and len(provider_ids) == 1056
            and len(set(provider_ids)) == 1056
            and required_model_only
        ),
        "pooled_regulation": pooled_regulation is not None and pooled_regulation >= 0.75,
        "median_seed_regulation": bool(seed_regulation) and median(seed_regulation) >= 0.75,
        "no_seed_at_or_below_chance": bool(seed_regulation) and min(seed_regulation) > 0.5,
        "family_regulation_pass_rate": len(families) == 24 and sum(
            float(family["regulation_accuracy"]) >= 0.625 for family in families
        ) >= 18,
        "exact_and_transfer": pooled_exact is not None and pooled_transfer is not None
        and pooled_exact >= 0.75 and pooled_transfer >= 0.75,
        "hidden_final_error": hidden_error is not None and hidden_error <= 0.1,
        "hidden_improvement": hidden_improvement is not None and hidden_improvement > 0,
        "interface": pooled_interface is not None and pooled_interface >= 0.9 and sum(
            float(family["interface_accuracy"]) >= 0.875 for family in families
        ) >= 20,
        "mapping_checkpoint": pooled_mapping is not None and pooled_mapping >= 0.75 and sum(
            float(family["mapping_accuracy"]) >= 0.875 for family in families
        ) >= 18,
        "safety_and_validity": invalid_actions == 0 and welfare_stops == 0,
    }
    connection.close()
    return {
        "database": str(database),
        "complete": complete,
        "progression_pass": all(gates.values()),
        "gates": gates,
        "aggregates": {
            "pooled_regulation_accuracy": pooled_regulation,
            "median_seed_regulation_accuracy": median(seed_regulation) if seed_regulation else None,
            "minimum_seed_regulation_accuracy": min(seed_regulation) if seed_regulation else None,
            "pooled_exact_accuracy": pooled_exact,
            "pooled_transfer_accuracy": pooled_transfer,
            "pooled_interface_accuracy": pooled_interface,
            "pooled_mapping_accuracy": pooled_mapping,
            "mean_hidden_final_error": hidden_error,
            "mean_hidden_improvement": hidden_improvement,
            "families_at_regulation_floor": sum(
                float(family["regulation_accuracy"]) >= 0.625 for family in families
            ),
            "families_at_interface_floor": sum(
                float(family["interface_accuracy"]) >= 0.875 for family in families
            ),
            "families_at_mapping_floor": sum(
                float(family["mapping_accuracy"]) >= 0.875 for family in families
            ),
            "hierarchical_bootstrap": bootstrap_interval,
        },
        "seeds": seed_results,
        "provider": {
            "calls": len(provider_rows),
            "unique_provider_ids": len(set(provider_ids)),
            "models": sorted({str(row.get("model")) for row in provider_metadata}),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze the frozen V10 reliability cohort")
    parser.add_argument("database", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bootstrap-samples", type=int, default=10_000)
    args = parser.parse_args()
    payload = json.dumps(analyze(args.database, args.bootstrap_samples), indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
        result = json.loads(payload)
        print("Project Theta V10 reliability analysis")
        for name, passed in result["gates"].items():
            print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        aggregates = result["aggregates"]
        print(
            "Regulation: "
            f"pooled={aggregates['pooled_regulation_accuracy']}, "
            f"median_seed={aggregates['median_seed_regulation_accuracy']}, "
            f"families_at_floor={aggregates['families_at_regulation_floor']}/24"
        )
        print(f"Progression: {'PASS' if result['progression_pass'] else 'BLOCKED'}")
        print(f"Full analysis: {args.output}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
