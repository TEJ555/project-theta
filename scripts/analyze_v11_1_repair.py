from __future__ import annotations

import argparse
import json
import random
import sqlite3
from math import isclose
from pathlib import Path
from statistics import fmean, median
from typing import Any


PLANNED_SEEDS = (7400, 7401, 7402, 7403, 7404, 7405)
CONDITIONS = (
    "full",
    "shuffled_interoception",
    "incorrect_association_summary",
    "raw_history",
    "bridge_incorrect",
    "explicit_mapping",
)
REQUIRED_MODEL = "openai/gpt-oss-20b"
ALLOWED_INFRASTRUCTURE_FAILURE = "AdapterError: NVIDIA NIM returned an empty completion."
REQUIRED_METRICS = {
    "active_regulation_accuracy",
    "active_exact_accuracy",
    "active_transfer_accuracy",
    "interface_comprehension_accuracy",
    "body_mapping_checkpoint_accuracy",
    "hidden_regulation_improvement",
    "hidden_regulation_final_error",
    "invalid_action_count",
    "welfare_stops",
    "model_calls",
}


def _mean(values: list[float]) -> float | None:
    return fmean(values) if values else None


def _raw_metrics(connection: sqlite3.Connection, run_id: str) -> dict[str, float | int | None]:
    rows = connection.execute(
        """
        SELECT observation_json, decision_json, hidden_world_json, hidden_body_json
        FROM steps WHERE run_id=? ORDER BY tick
        """,
        (run_id,),
    ).fetchall()
    scored: list[dict[str, Any]] = []
    invalid_actions = 0
    for observation_json, decision_json, hidden_json, body_json in rows:
        observation = json.loads(observation_json)
        decision = json.loads(decision_json)
        hidden = json.loads(hidden_json)
        body = json.loads(body_json)
        task = observation.get("task", {})
        action = decision.get("action")
        allowed = task.get("allowed_actions", [])
        invalid_actions += int(
            bool(hidden.get("invalid_action", bool(allowed) and action not in allowed))
        )
        correct_action = hidden.get("correct_action")
        if not correct_action:
            continue
        kind = str(task.get("kind", ""))
        target = task.get("target_I7")
        perturbation = hidden.get("perturbation")
        final_error = None
        improvement = None
        if kind in {"active_regulation_probe", "active_regulation_transfer_probe"}:
            final_error = abs(float(body.get("theta")) - float(target))
            improvement = abs(float(perturbation) - float(target)) - final_error
        scored.append({
            "kind": kind,
            "correct": action == correct_action,
            "final_error": final_error,
            "improvement": improvement,
        })

    def accuracy(kinds: set[str]) -> float | None:
        values = [float(row["correct"]) for row in scored if row["kind"] in kinds]
        return round(fmean(values), 6) if values else None

    active = [
        row for row in scored
        if row["kind"] in {"active_regulation_probe", "active_regulation_transfer_probe"}
    ]
    return {
        "active_regulation_accuracy": accuracy(
            {"active_regulation_probe", "active_regulation_transfer_probe"}
        ),
        "active_exact_accuracy": accuracy({"active_regulation_probe"}),
        "active_transfer_accuracy": accuracy({"active_regulation_transfer_probe"}),
        "interface_comprehension_accuracy": accuracy({"interface_comprehension_probe"}),
        "body_mapping_checkpoint_accuracy": accuracy({"body_mapping_checkpoint"}),
        "hidden_regulation_final_error": round(
            fmean(float(row["final_error"]) for row in active), 6
        ) if active else None,
        "hidden_regulation_improvement": round(
            fmean(float(row["improvement"]) for row in active), 6
        ) if active else None,
        "invalid_action_count": invalid_actions,
        "steps": len(rows),
    }


def _bootstrap_effect(values: list[float], seed: int, samples: int) -> dict[str, Any]:
    rng = random.Random(seed)
    draws = [fmean(rng.choice(values) for _ in values) for _ in range(samples)]
    draws.sort()

    def quantile(probability: float) -> float:
        index = (len(draws) - 1) * probability
        lower = int(index)
        upper = min(lower + 1, len(draws) - 1)
        weight = index - lower
        return draws[lower] * (1.0 - weight) + draws[upper] * weight

    return {
        "mean": fmean(values),
        "positive_seeds": sum(value > 0 for value in values),
        "lower_95": round(quantile(0.025), 6),
        "upper_95": round(quantile(0.975), 6),
        "samples": samples,
        "seed": seed,
    }


def _is_allowed_recovery_failure(reason: str | None) -> bool:
    """Accept only the two pre-documented, non-outcome recovery states."""
    return reason in {
        "interrupted_before_completion",
        ALLOWED_INFRASTRUCTURE_FAILURE,
    }


def analyze(database: Path, bootstrap_samples: int = 10_000) -> dict[str, Any]:
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    runs = connection.execute(
        """
        SELECT run_id, seed, condition_name, status, stop_reason
        FROM runs
        WHERE experiment='multi_body_mechanism_v11'
        ORDER BY seed, condition_name, created_at
        """
    ).fetchall()
    expected_keys = {(seed, condition) for seed in PLANNED_SEEDS for condition in CONDITIONS}
    completed: dict[tuple[int, str], list[tuple[str, str, str | None]]] = {
        key: [] for key in expected_keys
    }
    recovery_failures: dict[tuple[int, str], int] = {key: 0 for key in expected_keys}
    execution_rows: list[dict[str, Any]] = []
    all_provider_ids: list[str] = []
    all_models: list[str] = []

    for run_id, seed, condition, status, stop_reason in runs:
        key = (int(seed), str(condition))
        if key in completed and status == "completed" and stop_reason is None:
            completed[key].append((run_id, status, stop_reason))
        if key in recovery_failures and status == "failed" and _is_allowed_recovery_failure(stop_reason):
            recovery_failures[key] += 1
        steps = int(connection.execute(
            "SELECT COUNT(*) FROM steps WHERE run_id=?", (run_id,)
        ).fetchone()[0])
        calls = connection.execute(
            "SELECT tick, provider_id, metadata_json FROM api_calls WHERE run_id=? ORDER BY tick",
            (run_id,),
        ).fetchall()
        step_ids = dict(connection.execute(
            "SELECT tick, provider_id FROM steps WHERE run_id=? ORDER BY tick", (run_id,)
        ).fetchall())
        call_ids = {int(tick): str(provider_id or "") for tick, provider_id, _ in calls}
        aligned = len(step_ids) == len(call_ids) and all(
            provider_id and call_ids.get(int(tick)) == str(provider_id)
            for tick, provider_id in step_ids.items()
        )
        metadata = [json.loads(item[2]) for item in calls]
        provider_ids = [str(item[1] or "") for item in calls]
        models = [str(item.get("model")) for item in metadata]
        if status == "completed" and stop_reason is None:
            all_provider_ids.extend(provider_ids)
            all_models.extend(models)
        execution_rows.append({
            "run_id": run_id,
            "seed": int(seed),
            "condition": str(condition),
            "status": status,
            "stop_reason": stop_reason,
            "steps": steps,
            "provider_calls": len(calls),
            "provider_alignment": aligned,
            "models": sorted(set(models)),
        })

    structure_valid = (
        all(
            (int(seed), str(condition)) in expected_keys
            for _, seed, condition, _, _ in runs
        )
        and all(len(completed[key]) == 1 for key in expected_keys)
        and all(recovery_failures[key] <= 1 for key in expected_keys)
        and all(
            (
                row["status"] == "completed"
                and row["stop_reason"] is None
                and row["steps"] == 176
                and row["provider_calls"] == 176
                and row["provider_alignment"]
                and row["models"] == [REQUIRED_MODEL]
            )
            or (
                row["status"] == "failed"
                and _is_allowed_recovery_failure(row["stop_reason"])
                and row["steps"] < 176
                and row["provider_calls"] == row["steps"]
                and row["provider_alignment"]
                and set(row["models"]) <= {REQUIRED_MODEL}
            )
            for row in execution_rows
        )
        and len(all_provider_ids) == 6_336
        and len(set(all_provider_ids)) == 6_336
        and set(all_models) == {REQUIRED_MODEL}
    )

    results: list[dict[str, Any]] = []
    for key in sorted(expected_keys):
        if len(completed[key]) != 1:
            continue
        run_id = completed[key][0][0]
        stored = dict(connection.execute(
            "SELECT name, value FROM metrics WHERE run_id=?", (run_id,)
        ).fetchall())
        raw = _raw_metrics(connection, run_id)
        required_present = REQUIRED_METRICS <= set(stored) and all(
            stored[name] is not None for name in REQUIRED_METRICS
        )
        raw_consistent = required_present and all(
            raw.get(name) is not None
            and isclose(float(stored[name]), float(raw[name]), rel_tol=0.0, abs_tol=1e-12)
            for name in (
                "active_regulation_accuracy",
                "active_exact_accuracy",
                "active_transfer_accuracy",
                "interface_comprehension_accuracy",
                "body_mapping_checkpoint_accuracy",
                "hidden_regulation_improvement",
                "hidden_regulation_final_error",
                "invalid_action_count",
            )
        )
        results.append({
            "run_id": run_id,
            "seed": key[0],
            "condition": key[1],
            "metrics": stored,
            "raw_metrics": raw,
            "required_metrics_present": required_present,
            "stored_metric_consistency": raw_consistent,
        })

    complete = (
        structure_valid
        and len(results) == len(expected_keys)
        and all(item["required_metrics_present"] for item in results)
        and all(item["stored_metric_consistency"] for item in results)
        and all(float(item["metrics"]["model_calls"]) == 176 for item in results)
    )
    invalid_action_counts = [
        int(float(item["metrics"]["invalid_action_count"])) for item in results
    ]
    forced_choice_compliant = (
        len(invalid_action_counts) == len(expected_keys)
        and sum(invalid_action_counts) <= 6
        and max(invalid_action_counts, default=0) <= 1
    )
    safety_valid = (
        len(results) == len(expected_keys)
        and all(float(item["metrics"]["welfare_stops"]) == 0 for item in results)
    )

    by_key = {(item["seed"], item["condition"]): item for item in results}

    def values(condition: str, metric: str) -> list[float]:
        return [
            float(by_key[(seed, condition)]["metrics"][metric])
            for seed in PLANNED_SEEDS
            if (seed, condition) in by_key
        ]

    condition_results: dict[str, Any] = {}
    for condition in CONDITIONS:
        regulation = values(condition, "active_regulation_accuracy")
        condition_results[condition] = {
            metric: _mean(values(condition, metric))
            for metric in (
                "active_regulation_accuracy",
                "active_exact_accuracy",
                "active_transfer_accuracy",
                "interface_comprehension_accuracy",
                "body_mapping_checkpoint_accuracy",
                "hidden_regulation_final_error",
                "hidden_regulation_improvement",
            )
        }
        condition_results[condition]["median_seed_regulation_accuracy"] = (
            median(regulation) if regulation else None
        )

    def paired(left: str, right: str, metric: str) -> list[float]:
        return [
            float(by_key[(seed, left)]["metrics"][metric])
            - float(by_key[(seed, right)]["metrics"][metric])
            for seed in PLANNED_SEEDS
            if (seed, left) in by_key and (seed, right) in by_key
        ]

    effects = {
        "full_minus_shuffled_regulation": paired(
            "full", "shuffled_interoception", "active_regulation_accuracy"
        ),
        "full_minus_incorrect_summary_regulation": paired(
            "full", "incorrect_association_summary", "active_regulation_accuracy"
        ),
        "raw_history_minus_incorrect_summary_regulation": paired(
            "raw_history", "incorrect_association_summary", "active_regulation_accuracy"
        ),
        "full_minus_raw_history_regulation": paired(
            "full", "raw_history", "active_regulation_accuracy"
        ),
        "bridge_incorrect_exact_minus_transfer": [
            float(by_key[(seed, "bridge_incorrect")]["metrics"]["active_exact_accuracy"])
            - float(by_key[(seed, "bridge_incorrect")]["metrics"]["active_transfer_accuracy"])
            for seed in PLANNED_SEEDS
            if (seed, "bridge_incorrect") in by_key
        ],
    }
    effect_summaries = {
        name: _bootstrap_effect(items, 20261002 + index, bootstrap_samples)
        for index, (name, items) in enumerate(effects.items())
        if len(items) == len(PLANNED_SEEDS)
    }

    full_values = values("full", "active_regulation_accuracy")
    shuffled_values = values("shuffled_interoception", "active_regulation_accuracy")
    explicit_values = values("explicit_mapping", "active_regulation_accuracy")
    bridge_exact = values("bridge_incorrect", "active_exact_accuracy")
    bridge_transfer = values("bridge_incorrect", "active_transfer_accuracy")
    interface_values = [
        float(item["metrics"]["interface_comprehension_accuracy"]) for item in results
    ]

    gates = {
        "complete_execution": complete,
        "full_replicates_v10": (
            len(full_values) == 6
            and fmean(full_values) >= 0.75
            and median(full_values) >= 0.75
            and min(full_values) > 0.5
        ),
        "current_state_dependence": (
            len(shuffled_values) == 6
            and fmean(shuffled_values) <= 0.65
            and effect_summaries.get("full_minus_shuffled_regulation", {}).get("mean", -1) >= 0.15
            and effect_summaries.get("full_minus_shuffled_regulation", {}).get("positive_seeds", 0) >= 5
        ),
        "bridge_specificity": (
            len(bridge_exact) == 6
            and fmean(bridge_exact) >= 0.75
            and fmean(bridge_transfer) <= 0.55
            and effect_summaries.get("bridge_incorrect_exact_minus_transfer", {}).get("mean", -1) >= 0.20
            and effect_summaries.get("bridge_incorrect_exact_minus_transfer", {}).get("positive_seeds", 0) >= 5
        ),
        "explicit_mapping_competence": (
            len(explicit_values) == 6
            and fmean(explicit_values) >= 0.75
            and median(explicit_values) >= 0.75
        ),
        "interface_invariance": (
            len(interface_values) == 36
            and fmean(interface_values) >= 0.90
            and sum(value >= 0.875 for value in interface_values) >= 30
        ),
        "forced_choice_compliance": forced_choice_compliant,
        "safety_and_validity": complete and safety_valid,
    }

    classifications = {
        "incorrect_summary_interference": (
            effect_summaries.get(
                "raw_history_minus_incorrect_summary_regulation", {}
            ).get("mean", -1) >= 0.15
            and effect_summaries.get(
                "raw_history_minus_incorrect_summary_regulation", {}
            ).get("positive_seeds", 0) >= 5
        ),
        "summary_necessity": (
            effect_summaries.get("full_minus_raw_history_regulation", {}).get("mean", -1)
            >= 0.15
            and effect_summaries.get(
                "full_minus_raw_history_regulation", {}
            ).get("positive_seeds", 0) >= 5
        ),
    }
    connection.close()
    return {
        "database": str(database),
        "complete": complete,
        "mechanism_progression_pass": all(gates.values()),
        "gates": gates,
        "classifications": classifications,
        "conditions": condition_results,
        "paired_effects": effect_summaries,
        "runs": results,
        "execution": {
            "rows": execution_rows,
            "preserved_recovery_failures": sum(recovery_failures.values()),
            "preserved_interruptions": sum(
                row["status"] == "failed"
                and row["stop_reason"] == "interrupted_before_completion"
                for row in execution_rows
            ),
            "preserved_nvidia_empty_completions": sum(
                row["status"] == "failed"
                and row["stop_reason"] == ALLOWED_INFRASTRUCTURE_FAILURE
                for row in execution_rows
            ),
            "provider_calls": len(all_provider_ids),
            "unique_provider_ids": len(set(all_provider_ids)),
            "models": sorted(set(all_models)),
            "invalid_actions": sum(invalid_action_counts),
            "maximum_invalid_actions_in_one_run": max(invalid_action_counts, default=0),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze the frozen V11.1 forced-choice repair")
    parser.add_argument("database", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bootstrap-samples", type=int, default=10_000)
    args = parser.parse_args()
    result = analyze(args.database, args.bootstrap_samples)
    payload = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
        print("Project Theta V11.1 forced-choice repair analysis")
        for name, passed in result["gates"].items():
            print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        print(
            "Progression: "
            + ("PASS" if result["mechanism_progression_pass"] else "BLOCKED")
        )
        print(f"Full analysis: {args.output}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
