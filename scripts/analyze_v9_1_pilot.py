from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any


REPORTED_METRICS = (
    "calibration_compliance",
    "interface_comprehension_accuracy",
    "active_regulation_accuracy",
    "active_exact_accuracy",
    "active_transfer_accuracy",
    "hidden_regulation_final_error",
    "hidden_regulation_improvement",
    "active_prediction_mae",
    "invalid_action_count",
    "welfare_stops",
    "model_calls",
)


def _loads(value: str) -> dict[str, Any]:
    loaded = json.loads(value)
    return loaded if isinstance(loaded, dict) else {}


def analyze(database: Path) -> dict[str, Any]:
    connection = sqlite3.connect(database)
    runs = connection.execute(
        "SELECT run_id, condition_name, seed, status, stop_reason FROM runs ORDER BY created_at"
    ).fetchall()
    result: dict[str, Any] = {"database": str(database), "runs": {}}
    for run_id, condition, seed, status, stop_reason in runs:
        metrics = dict(connection.execute(
            "SELECT name, value FROM metrics WHERE run_id=?",
            (run_id,),
        ).fetchall())
        rows = connection.execute(
            """
            SELECT tick, observation_json, decision_json, events_json,
                   hidden_world_json, hidden_body_json
            FROM steps WHERE run_id=? ORDER BY tick
            """,
            (run_id,),
        ).fetchall()
        errors: list[dict[str, Any]] = []
        kind_counts: dict[str, dict[str, int]] = {}
        for tick, observation_json, decision_json, events_json, hidden_json, body_json in rows:
            observation = _loads(observation_json)
            decision = _loads(decision_json)
            hidden = _loads(hidden_json)
            body = _loads(body_json)
            events = json.loads(events_json)
            task = observation.get("task", {})
            kind = str(task.get("kind", ""))
            correct = hidden.get("correct_action")
            if not correct:
                continue
            counters = kind_counts.setdefault(kind, {"correct": 0, "total": 0})
            counters["total"] += 1
            is_correct = decision.get("action") == correct
            counters["correct"] += int(is_correct)
            if not is_correct:
                event = events[0] if isinstance(events, list) and events else {}
                errors.append({
                    "tick": tick,
                    "kind": kind,
                    "stage": task.get("stage"),
                    "family": task.get("family_token"),
                    "displayed_I7": observation.get("private_signals", {}).get("I7"),
                    "hidden_baseline_I7": hidden.get("perturbation"),
                    "chosen": decision.get("action"),
                    "correct": correct,
                    "predicted_I7": decision.get("prediction", {}).get("I7"),
                    "hidden_outcome_I7": body.get("theta"),
                    "action_effect": event.get("action_effect"),
                })
        result["runs"][str(condition)] = {
            "seed": seed,
            "status": status,
            "stop_reason": stop_reason,
            "metrics": {name: metrics.get(name) for name in REPORTED_METRICS},
            "kind_counts": kind_counts,
            "errors": errors,
        }
    provider_rows = connection.execute(
        "SELECT provider_id, metadata_json FROM api_calls"
    ).fetchall()
    provider_metadata = [_loads(row[1]) for row in provider_rows]
    result["provider"] = {
        "calls": len(provider_rows),
        "unique_provider_ids": len({row[0] for row in provider_rows}),
        "models": sorted({str(row.get("model")) for row in provider_metadata}),
        "input_tokens": sum(int(row.get("input_tokens", 0) or 0) for row in provider_metadata),
        "output_tokens": sum(int(row.get("output_tokens", 0) or 0) for row in provider_metadata),
    }
    connection.close()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a V9.1 run-level and error audit")
    parser.add_argument("database", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(analyze(args.database), indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
