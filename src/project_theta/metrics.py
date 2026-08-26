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
    "acquisition_exposures": {"class": "descriptive", "direction": "descriptive"},
    "probe_opportunities": {"class": "descriptive", "direction": "descriptive"},
    "probe_correct": {"class": "descriptive", "direction": "higher"},
    "forced_choice_accuracy": {"class": "behavioural", "direction": "higher"},
    "pre_update_accuracy": {"class": "behavioural", "direction": "higher"},
    "post_update_accuracy": {"class": "behavioural", "direction": "higher"},
    "stable_post_accuracy": {"class": "behavioural", "direction": "higher"},
    "reversed_post_accuracy": {"class": "behavioural", "direction": "higher"},
    "reassigned_post_accuracy": {"class": "behavioural", "direction": "higher"},
    "independent_probe_items": {"class": "descriptive", "direction": "higher"},
    "reversal_cost": {"class": "behavioural", "direction": "lower"},
    "generalization_accuracy": {"class": "behavioural", "direction": "higher"},
    "source_binding_accuracy": {"class": "behavioural", "direction": "higher"},
    "temporal_choice_accuracy": {"class": "behavioural", "direction": "higher"},
    "signal_contrast": {"class": "behavioural", "direction": "higher"},
    "delayed_signal_contrast": {"class": "behavioural", "direction": "higher"},
    "calibration_brier": {"class": "behavioural", "direction": "lower"},
    "choice_side_bias": {"class": "behavioural", "direction": "lower"},
    "invalid_action_count": {"class": "quality", "direction": "lower"},
    "estimated_api_cost_usd": {"class": "cost", "direction": "report-always"},
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
        "estimated_api_cost_usd": round(
            float(component_counts.get("estimated_api_cost_usd", 0.0)), 8
        ),
    }


def compute_controlled_metrics(
    rows: list[dict[str, Any]], component_counts: dict[str, int]
) -> dict[str, float | int | None]:
    probes = [row for row in rows if row["phase"] == "probe"]
    correct = [1.0 if row["is_correct"] else 0.0 for row in probes]
    left_count = sum(1 for row in probes if row["action"] == "choose_left")

    def accuracy(kind: str | None = None) -> float | None:
        selected = probes if kind is None else [row for row in probes if row["kind"] == kind]
        if not selected:
            return None
        return round(sum(bool(row["is_correct"]) for row in selected) / len(selected), 6)

    immediate = [row for row in rows if row.get("exposure_type") == "immediate"]
    risky = [float(row["outcome_signal"]) for row in immediate if row["perturbation"] >= 0.5]
    safe = [float(row["outcome_signal"]) for row in immediate if row["perturbation"] <= 0.1]
    delayed = [row for row in rows if row.get("delayed_due")]
    delayed_risky = [float(row["baseline_signal"]) for row in delayed if row["delayed_magnitude"] > 0]
    delayed_safe = [float(row["baseline_signal"]) for row in delayed if row["delayed_magnitude"] == 0]
    brier = [
        (float(row["confidence"]) - (1.0 if row["is_correct"] else 0.0)) ** 2
        for row in probes
    ]
    pre_update = accuracy("pre_update_probe")
    post_update = accuracy("post_update_probe")

    def post_transition_accuracy(transition: str) -> float | None:
        selected = [
            row for row in probes
            if row["kind"] == "post_update_probe" and row.get("transition") == transition
        ]
        if not selected:
            return None
        return round(sum(bool(row["is_correct"]) for row in selected) / len(selected), 6)

    return {
        "steps": len(rows),
        "acquisition_exposures": sum(1 for row in rows if row["phase"] == "acquisition"),
        "probe_opportunities": len(probes),
        "probe_correct": int(sum(correct)),
        "forced_choice_accuracy": accuracy(),
        "pre_update_accuracy": pre_update,
        "post_update_accuracy": post_update,
        "stable_post_accuracy": post_transition_accuracy("stable"),
        "reversed_post_accuracy": post_transition_accuracy("reversed"),
        "reassigned_post_accuracy": post_transition_accuracy("reassigned"),
        "independent_probe_items": len({
            (row.get("block"), row.get("family"))
            for row in probes if row.get("family")
        }),
        "reversal_cost": (
            round(float(pre_update) - float(post_update), 6)
            if pre_update is not None and post_update is not None else None
        ),
        "generalization_accuracy": accuracy("generalization_probe"),
        "source_binding_accuracy": accuracy("source_binding_probe"),
        "temporal_choice_accuracy": accuracy("temporal_probe"),
        "signal_contrast": (
            round(fmean(risky) - fmean(safe), 6) if risky and safe else None
        ),
        "delayed_signal_contrast": (
            round(fmean(delayed_risky) - fmean(delayed_safe), 6)
            if delayed_risky and delayed_safe else None
        ),
        "calibration_brier": round(fmean(brier), 6) if brier else None,
        "choice_side_bias": round(abs(left_count / len(probes) - 0.5) * 2, 6) if probes else None,
        "invalid_action_count": sum(int(row.get("invalid_action", False)) for row in rows),
        "mean_theta": round(fmean(float(row["baseline_signal"]) for row in rows), 6),
        "final_integrity": round(float(rows[-1]["integrity"]), 6) if rows else None,
        "memory_reads": component_counts.get("memory_reads", 0),
        "memory_writes": component_counts.get("memory_writes", 0),
        "workspace_broadcasts": component_counts.get("workspace_broadcasts", 0),
        "welfare_stops": component_counts.get("welfare_stops", 0),
        "estimated_api_cost_usd": round(
            float(component_counts.get("estimated_api_cost_usd", 0.0)), 8
        ),
    }
