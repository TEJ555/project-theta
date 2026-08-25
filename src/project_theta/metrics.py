from __future__ import annotations

from math import sqrt
from statistics import fmean
from typing import Any

METRIC_REGISTRY: dict[str, dict[str, str]] = {
    "steps": {"class": "descriptive", "direction": "descriptive"},
    "total_reward": {"class": "behavioural", "direction": "higher"},
    "final_integrity": {"class": "behavioural", "direction": "higher"},
    "resource_efficiency": {"class": "behavioural", "direction": "higher"},
    "post_acquisition_hazard_revisit_rate": {"class": "behavioural", "direction": "lower"},
    "source_attribution_accuracy": {"class": "behavioural", "direction": "higher"},
    "prediction_mae": {"class": "behavioural", "direction": "lower"},
    "delayed_event_prediction_mae": {"class": "behavioural", "direction": "lower"},
    "theta_damage_correlation": {"class": "behavioural", "direction": "context-dependent"},
    "mean_theta": {"class": "safety", "direction": "report-always"},
    "memory_reads": {"class": "computational", "direction": "descriptive"},
    "memory_writes": {"class": "computational", "direction": "descriptive"},
    "workspace_broadcasts": {"class": "computational", "direction": "descriptive"},
    "welfare_stops": {"class": "safety", "direction": "report-always"},
}


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    mx, my = fmean(xs), fmean(ys)
    numerator = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denominator = sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return numerator / denominator if denominator else None


def compute_metrics(
    rows: list[dict[str, Any]], acquisition_end: int, component_counts: dict[str, int]
) -> dict[str, float | int | None]:
    if not rows:
        return {}
    theta = [float(row["signal"]) for row in rows]
    damage = [float(row["damage"]) for row in rows]
    predictions = [row.get("prediction") for row in rows]
    valid_predictions = [
        abs(float(pred) - float(rows[i + 1]["signal"]))
        for i, pred in enumerate(predictions[:-1])
        if isinstance(pred, (int, float))
    ]
    contacts = [row for row in rows if row["contact"]]
    contacted_positions = {tuple(row["position"]) for row in contacts if row["tick"] <= acquisition_end}
    later_visits = [
        row for row in rows if row["tick"] > acquisition_end and tuple(row["position"]) in contacted_positions
    ]
    later_contacts = sum(1 for row in later_visits if row["contact"])
    probe_rows = [row for row in rows if row.get("expected_source")]
    source_correct = sum(
        1
        for row in probe_rows
        if str(row["expected_source"]).lower() in str(row.get("self_report", "")).lower()
    )
    delayed_errors = [
        abs(float(row["prediction"]) - float(rows[i + 4]["signal"]))
        for i, row in enumerate(rows[:-4])
        if row.get("delayed_exposure") and isinstance(row.get("prediction"), (int, float))
    ]
    return {
        "steps": len(rows),
        "total_reward": round(sum(float(row["reward"]) for row in rows), 6),
        "final_integrity": round(float(rows[-1]["integrity"]), 6),
        "mean_theta": round(fmean(theta), 6),
        "resource_efficiency": round(
            sum(int(row["resource_consumed"]) for row in rows) / max(1, len(rows)), 6
        ),
        "theta_damage_correlation": (
            round(value, 6) if (value := _pearson(theta[1:], damage[:-1])) is not None else None
        ),
        "post_acquisition_hazard_revisit_rate": round(
            later_contacts / max(1, len(later_visits)), 6
        ),
        "prediction_mae": round(fmean(valid_predictions), 6) if valid_predictions else None,
        "delayed_event_prediction_mae": round(fmean(delayed_errors), 6) if delayed_errors else None,
        "source_attribution_accuracy": round(source_correct / len(probe_rows), 6) if probe_rows else None,
        "memory_reads": component_counts.get("memory_reads", 0),
        "memory_writes": component_counts.get("memory_writes", 0),
        "workspace_broadcasts": component_counts.get("workspace_broadcasts", 0),
        "welfare_stops": component_counts.get("welfare_stops", 0),
    }
