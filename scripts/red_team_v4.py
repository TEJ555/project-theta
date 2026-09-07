"""Independent, no-provider red-team checks for self-model binding v4.

This script intentionally uses only deterministic schedules and the scripted adapter.
It is safe to run before target-model collection. A passing result rules out the
declared shortcut family, not every possible shortcut.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import tempfile
from collections import defaultdict
from dataclasses import replace
from pathlib import Path
from typing import Any

from project_theta.audits import audit_self_model_binding_v4_schedules
from project_theta.config import RunConfig
from project_theta.harness import ExperimentHarness
from project_theta.trials import build_trials


def _probe_rows(seeds: list[int]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed in seeds:
        probes = [
            trial
            for trial in build_trials("self_model_binding_v4", seed)
            if trial.phase == "probe"
        ]
        for order, trial in enumerate(probes):
            public = trial.public_task()
            options = public["options"]
            rows.append(
                {
                    "seed": seed,
                    "order": order,
                    "left": options[0]["stimulus"]["token"],
                    "right": options[1]["stimulus"]["token"],
                    "correct": trial.correct_action,
                    "public": public,
                }
            )
    return rows


def _public_features(row: dict[str, Any]) -> dict[str, bool]:
    left = row["left"].removeprefix("stimulus-")
    right = row["right"].removeprefix("stimulus-")
    features = {
        "lexical_first": left < right,
        "left_checksum_even": sum(map(ord, left)) % 2 == 0,
        "pair_checksum_even": (sum(map(ord, left)) + sum(map(ord, right))) % 2 == 0,
        "left_first_half": left[0] < "n",
        "right_first_half": right[0] < "n",
    }
    for index, (left_char, right_char) in enumerate(zip(left, right)):
        features[f"character_{index}_lexical_first"] = left_char < right_char
        features[f"left_character_{index}_even"] = ord(left_char) % 2 == 0
    for modulus in range(2, 7):
        for residue in range(modulus):
            features[f"order_mod_{modulus}_is_{residue}"] = row["order"] % modulus == residue
    return features


def _learn_boolean_rules(
    training: list[dict[str, Any]], test: list[dict[str, Any]]
) -> dict[str, float]:
    names = sorted(_public_features(training[0]))
    orientations: dict[str, bool] = {}
    for name in names:
        left_if_true_score = sum(
            (
                "choose_left"
                if _public_features(row)[name]
                else "choose_right"
            )
            == row["correct"]
            for row in training
        )
        orientations[name] = left_if_true_score >= len(training) / 2

    scores: dict[str, float] = {}
    for name in names:
        left_if_true = orientations[name]
        correct = 0
        for row in test:
            feature = _public_features(row)[name]
            choose_left = feature if left_if_true else not feature
            action = "choose_left" if choose_left else "choose_right"
            correct += action == row["correct"]
        scores[name] = correct / len(test)

    for action in ("choose_left", "choose_right"):
        scores[f"fixed_{action}"] = sum(row["correct"] == action for row in test) / len(test)

    by_position: dict[int, list[str]] = defaultdict(list)
    for row in training:
        by_position[row["order"]].append(row["correct"])
    position_rule = {
        order: "choose_left"
        if outcomes.count("choose_left") >= outcomes.count("choose_right")
        else "choose_right"
        for order, outcomes in by_position.items()
    }
    scores["learned_probe_position"] = sum(
        position_rule[row["order"]] == row["correct"] for row in test
    ) / len(test)
    return dict(sorted(scores.items()))


def _hidden_diagnostics(rows: list[dict[str, Any]]) -> dict[str, float]:
    """Score old rules that use hidden seed data and are not available to the model."""
    predictions = {
        "old_index_plus_seed_parity": lambda row: (
            "choose_right" if (row["order"] + row["seed"]) % 2 == 0 else "choose_left"
        ),
        "seed_parity_fixed_side": lambda row: (
            "choose_left" if row["seed"] % 2 == 0 else "choose_right"
        ),
    }
    return {
        name: sum(rule(row) == row["correct"] for row in rows) / len(rows)
        for name, rule in predictions.items()
    }


def _probe_contexts(database: Path, run_id: str) -> list[str]:
    connection = sqlite3.connect(database)
    rows = [
        row[0]
        for row in connection.execute(
            """
            SELECT context_json FROM steps
            WHERE run_id=? AND context_json LIKE '%source_binding_probe%'
            ORDER BY tick
            """,
            (run_id,),
        )
    ]
    connection.close()
    return rows


def _context_checks(seeds: list[int]) -> dict[str, Any]:
    equality: dict[str, bool] = {}
    metrics: dict[str, dict[str, float | int | None]] = {}
    with tempfile.TemporaryDirectory(prefix="theta-v4-red-team-") as directory:
        database = Path(directory) / "validation.sqlite"
        harness = ExperimentHarness(database)
        for seed in seeds:
            summaries = {}
            for condition in (
                "full",
                "generic_table",
                "misattributed_table",
                "permuted_table",
            ):
                summaries[condition] = harness.run(
                    replace(
                        RunConfig(),
                        experiment="self_model_binding_v4",
                        condition=condition,
                        seed=seed,
                        inference_profile="probes_only",
                    )
                )
            equality[str(seed)] = _probe_contexts(
                database, summaries["full"].run_id
            ) == _probe_contexts(database, summaries["generic_table"].run_id)
            metrics[str(seed)] = {
                condition: summary.metrics.get("source_binding_accuracy")
                for condition, summary in summaries.items()
            }
            metrics[str(seed)]["full_model_calls"] = summaries["full"].metrics.get(
                "model_calls"
            )
            metrics[str(seed)]["full_inference_skipped"] = summaries["full"].metrics.get(
                "inference_skipped"
            )
    return {"byte_identical_full_generic": equality, "scripted_metrics": metrics}


def run_red_team(start_seed: int, count: int, context_seed_count: int) -> dict[str, Any]:
    if count < 20 or count % 2:
        raise ValueError("count must be an even integer of at least 20")
    seeds = list(range(start_seed, start_seed + count))
    split = count // 2
    training = _probe_rows(seeds[:split])
    test = _probe_rows(seeds[split:])
    scores = _learn_boolean_rules(training, test)
    threshold = 0.60
    public_tasks = [row["public"] for row in training + test]
    public_text = json.dumps(public_tasks, sort_keys=True).lower()
    forbidden = (
        "trial_id",
        "correct_action",
        "self_model_binding_v4",
        '"owner"',
        '"seed"',
        '"condition"',
    )
    context_checks = _context_checks(seeds[:context_seed_count])
    schedule = audit_self_model_binding_v4_schedules(seeds)
    status = "pass"
    if schedule["status"] != "pass" or max(scores.values()) > threshold:
        status = "fail"
    if any(term in public_text for term in forbidden):
        status = "fail"
    if not all(context_checks["byte_identical_full_generic"].values()):
        status = "fail"
    return {
        "experiment": "self_model_binding_v4",
        "status": status,
        "epistemic_notice": (
            "Passing excludes only the tested shortcut family. It is not evidence of consciousness."
        ),
        "seed_range": [seeds[0], seeds[-1]],
        "schedule_count": count,
        "held_out_probe_count": len(test),
        "public_strategy_threshold": threshold,
        "best_public_strategy": max(scores, key=scores.get),
        "best_public_strategy_score": max(scores.values()),
        "public_strategy_scores": scores,
        "hidden_data_diagnostics": _hidden_diagnostics(test),
        "forbidden_public_terms_found": [term for term in forbidden if term in public_text],
        "context_checks": context_checks,
        "schedule_audit_status": schedule["status"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-seed", type=int, default=10000)
    parser.add_argument("--count", type=int, default=400)
    parser.add_argument("--context-seeds", type=int, default=5)
    args = parser.parse_args()
    result = run_red_team(args.start_seed, args.count, args.context_seeds)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
