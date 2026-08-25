from __future__ import annotations

import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from math import comb, sqrt
from pathlib import Path
from random import Random
from statistics import fmean, median
from typing import Any, Iterable

from .experiments import PROTOCOLS
from .types import RunSummary


@dataclass(frozen=True)
class Aggregate:
    experiment: str
    condition: str
    metric: str
    n: int
    mean: float | None
    minimum: float | None
    maximum: float | None


def _bootstrap_ci(values: list[float], seed: int = 20260825, samples: int = 2000) -> tuple[float, float] | None:
    if not values:
        return None
    if len(values) == 1:
        return values[0], values[0]
    rng = Random(seed)
    estimates = sorted(fmean(rng.choice(values) for _ in values) for _ in range(samples))
    return estimates[int(samples * 0.025)], estimates[min(samples - 1, int(samples * 0.975))]


def _sign_test(values: list[float]) -> float | None:
    nonzero = [value for value in values if value != 0]
    n = len(nonzero)
    if not n:
        return None
    positive = sum(value > 0 for value in nonzero)
    tail = min(positive, n - positive)
    probability = 2 * sum(comb(n, k) for k in range(tail + 1)) / (2 ** n)
    return min(1.0, probability)


def summarize_runs(summaries: Iterable[RunSummary]) -> dict[str, Any]:
    items = list(summaries)
    grouped: dict[tuple[str, str], list[RunSummary]] = defaultdict(list)
    for item in items:
        grouped[(item.experiment, item.condition)].append(item)

    aggregates: list[dict[str, Any]] = []
    for (experiment, condition), runs in sorted(grouped.items()):
        metric = PROTOCOLS[experiment].primary_outcomes[0]
        values = [float(run.metrics[metric]) for run in runs if isinstance(run.metrics.get(metric), (int, float))]
        aggregates.append({
            "experiment": experiment,
            "condition": condition,
            "metric": metric,
            "n": len(values),
            "mean": round(fmean(values), 6) if values else None,
            "minimum": round(min(values), 6) if values else None,
            "maximum": round(max(values), 6) if values else None,
        })

    by_key = {(item.experiment, item.condition, item.seed): item for item in items}
    comparisons: list[dict[str, Any]] = []
    for experiment, condition in sorted(grouped):
        if condition == "full":
            continue
        metric = PROTOCOLS[experiment].primary_outcomes[0]
        differences: list[float] = []
        for run in grouped[(experiment, condition)]:
            reference = by_key.get((experiment, "full", run.seed))
            left = reference.metrics.get(metric) if reference else None
            right = run.metrics.get(metric)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                differences.append(float(left) - float(right))
        interval = _bootstrap_ci(differences)
        comparisons.append({
            "experiment": experiment,
            "comparison": f"full - {condition}",
            "metric": metric,
            "pairs": len(differences),
            "mean_difference": round(fmean(differences), 6) if differences else None,
            "median_difference": round(median(differences), 6) if differences else None,
            "ci95": [round(interval[0], 6), round(interval[1], 6)] if interval else None,
            "sign_test_p": round(value, 6) if (value := _sign_test(differences)) is not None else None,
        })

    warnings: list[str] = []
    if any(item.stop_reason for item in items):
        warnings.append("One or more runs stopped early; inspect welfare events before interpretation.")
    for aggregate in aggregates:
        if aggregate["n"] == 0:
            warnings.append(
                f"{aggregate['experiment']}/{aggregate['condition']} has no primary metric value."
            )
        if aggregate["condition"] == "full" and aggregate["mean"] is not None and aggregate["mean"] < 0.7:
            warnings.append(
                f"Positive-control failure: {aggregate['experiment']} full mean is below 0.70."
            )
    for comparison in comparisons:
        if comparison["pairs"] < 10:
            warnings.append(
                f"Pilot-sized comparison: {comparison['experiment']} {comparison['comparison']} "
                f"has only {comparison['pairs']} pairs."
            )
        effect = comparison["mean_difference"]
        if effect is not None and effect < 0.15:
            warnings.append(
                f"Weak control separation: {comparison['experiment']} "
                f"{comparison['comparison']} effect is below 0.15."
            )
    return {
        "runs": len(items),
        "completed": sum(not item.stop_reason for item in items),
        "aggregates": aggregates,
        "paired_comparisons": comparisons,
        "warnings": warnings,
        "epistemic_notice": "These are behavioural/computational indicators, not phenomenal evidence.",
    }


def summaries_from_database(path: str | Path) -> list[RunSummary]:
    connection = sqlite3.connect(path)
    rows = connection.execute(
        """
        SELECT r.run_id, r.experiment, r.condition_name, r.seed, r.stop_reason,
               m.name, m.value
        FROM runs r LEFT JOIN metrics m ON r.run_id=m.run_id
        WHERE r.status='completed'
        ORDER BY r.created_at, m.name
        """
    ).fetchall()
    connection.close()
    combined: dict[str, RunSummary] = {}
    for run_id, experiment, condition, seed, stop_reason, metric, value in rows:
        summary = combined.setdefault(
            run_id,
            RunSummary(run_id, experiment, condition, seed, 0, bool(stop_reason), stop_reason, {}),
        )
        if metric:
            summary.metrics[metric] = value
            if metric == "steps" and value is not None:
                summary.steps = int(value)
    return list(combined.values())


def format_summary(summary: dict[str, Any]) -> str:
    lines = [
        f"Project Theta study: {summary['runs']} runs",
        "",
        "Experiment                    Condition                 n   Primary metric                  Mean     Range",
        "-" * 112,
    ]
    for row in summary["aggregates"]:
        mean = "n/a" if row["mean"] is None else f"{row['mean']:.3f}"
        bounds = "n/a" if row["minimum"] is None else f"{row['minimum']:.3f}..{row['maximum']:.3f}"
        lines.append(
            f"{row['experiment']:<29} {row['condition']:<25} {row['n']:>2}   "
            f"{row['metric']:<29} {mean:>6}   {bounds}"
        )
    lines.extend(["", "Paired full-condition effects (positive means full scored higher):"])
    for row in summary["paired_comparisons"]:
        effect = "n/a" if row["mean_difference"] is None else f"{row['mean_difference']:+.3f}"
        ci = "n/a" if row["ci95"] is None else f"[{row['ci95'][0]:+.3f}, {row['ci95'][1]:+.3f}]"
        lines.append(
            f"  {row['experiment']}: {row['comparison']} on {row['metric']} = {effect}, "
            f"95% bootstrap CI {ci}, pairs={row['pairs']}"
        )
    if summary["warnings"]:
        lines.extend(["", "Validity warnings:"])
        lines.extend(f"  - {warning}" for warning in summary["warnings"])
    lines.extend(["", summary["epistemic_notice"]])
    return "\n".join(lines)
