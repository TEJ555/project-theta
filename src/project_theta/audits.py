from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any

from .trials import ControlledTrial, build_trials


def _check(name: str, passed: bool, detail: str) -> dict[str, str]:
    return {"name": name, "status": "pass" if passed else "fail", "detail": detail}


def _stage_mapping(trials: list[ControlledTrial], stage: str) -> dict[str, float]:
    values: dict[str, list[float]] = defaultdict(list)
    for trial in trials:
        if trial.phase == "acquisition" and trial.block == stage:
            values[trial.cue].append(trial.perturbation)
    return {cue: sum(samples) / len(samples) for cue, samples in values.items()}


def audit_adversarial_schedules(
    seeds: list[int], profile: str = "standard"
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    all_alias_sets: list[set[str]] = []
    for seed in seeds:
        trials = build_trials("adversarial_theta", seed, profile)
        public_text = json.dumps([trial.public_task() for trial in trials], sort_keys=True)
        probes = [trial for trial in trials if trial.phase == "probe"]
        acquisitions = [trial for trial in trials if trial.phase == "acquisition"]
        aliases = {trial.cue for trial in acquisitions}
        all_alias_sets.append(aliases)

        expected_per_phase = 8 if profile == "standard" else 4
        checks.append(_check(
            f"seed_{seed}_schedule",
            len(acquisitions) == expected_per_phase * 2
            and len(probes) == expected_per_phase * 2,
            f"{len(acquisitions)} learning trials and {len(probes)} probes",
        ))
        stage_balance = all(
            sum(
                trial.correct_action == "choose_left"
                for trial in probes if trial.block == stage
            ) == expected_per_phase // 2
            for stage in ("stage_a", "stage_b")
        )
        checks.append(_check(
            f"seed_{seed}_side_balance",
            stage_balance,
            (
                f"{expected_per_phase // 2} correct-left and "
                f"{expected_per_phase // 2} correct-right probes in each stage"
            ),
        ))

        mapping_a = _stage_mapping(trials, "stage_a")
        mapping_b = _stage_mapping(trials, "stage_b")
        mapping_reversed = (
            mapping_a.keys() == mapping_b.keys()
            and all(mapping_a[cue] + mapping_b[cue] == 0.72 for cue in mapping_a)
        )
        checks.append(_check(
            f"seed_{seed}_mapping_update",
            mapping_reversed,
            "each cue reverses its true perturbation relationship",
        ))

        sham_groups: dict[tuple[str, str], list[float]] = defaultdict(list)
        for trial in acquisitions:
            sham_groups[(trial.block, trial.cue)].append(trial.sham_perturbation)
        expected_sham = [0.0, 0.72] * (expected_per_phase // 4)
        sham_balanced = all(sorted(values) == sorted(expected_sham) for values in sham_groups.values())
        checks.append(_check(
            f"seed_{seed}_sham_balance",
            sham_balanced,
            f"each cue receives the same {len(expected_sham)}-outcome sham distribution per stage",
        ))

        opaque = len(aliases) == 2 and all(
            re.fullmatch(r"stimulus-[a-z2-9]{9}", alias) for alias in aliases
        )
        checks.append(_check(
            f"seed_{seed}_opaque_aliases",
            opaque,
            "two seed-specific aliases contain no semantic feature labels",
        ))

        forbidden = (
            "correct_action",
            "perturbation",
            "sham",
            "risky",
            "safe",
            "adversarial_theta",
            "reversal",
            "condition",
            '"seed"',
        )
        leaked = [term for term in forbidden if term in public_text.lower()]
        checks.append(_check(
            f"seed_{seed}_public_leakage",
            not leaked,
            "no forbidden terms" if not leaked else "found " + ", ".join(leaked),
        ))

    aliases_unique = all(
        not all_alias_sets[left].intersection(all_alias_sets[right])
        for left in range(len(all_alias_sets))
        for right in range(left + 1, len(all_alias_sets))
    )
    checks.append(_check(
        "cross_seed_alias_uniqueness",
        aliases_unique,
        f"aliases do not repeat across {len(seeds)} schedules",
    ))
    return {
        "experiment": "adversarial_theta",
        "profile": profile,
        "seeds": seeds,
        "status": "fail" if any(check["status"] == "fail" for check in checks) else "pass",
        "checks": checks,
    }


def add_execution_audit(
    result: dict[str, Any], database: str | Path, expected_seed: int, expected_steps: int = 32
) -> dict[str, Any]:
    """Add protocol identity and trial-count checks for a partial or complete study."""
    connection = sqlite3.connect(database)
    rows = connection.execute(
        """
        SELECT r.run_id, r.experiment, r.condition_name, r.seed, r.status,
               (SELECT COUNT(*) FROM steps s WHERE s.run_id=r.run_id),
               (SELECT COUNT(*) FROM metrics m
                WHERE m.run_id=r.run_id AND m.name='post_update_accuracy')
        FROM runs r
        ORDER BY r.created_at
        """
    ).fetchall()
    connection.close()
    checks = result["checks"]
    checks.append(_check(
        "execution_has_runs",
        bool(rows),
        f"{len(rows)} recorded run(s)",
    ))
    for run_id, experiment, condition, seed, status, step_count, metric_count in rows:
        true_steps = int(step_count or 0)
        identity_ok = (
            experiment == "adversarial_theta"
            and int(seed) == expected_seed
            and status == "completed"
            and true_steps == expected_steps
            and int(metric_count or 0) > 0
        )
        checks.append(_check(
            f"execution_{condition}_{run_id[-8:]}",
            identity_ok,
            (
                f"experiment={experiment}, seed={seed}, status={status}, "
                f"steps={true_steps}, post-update metric rows={metric_count}"
            ),
        ))
    result["status"] = "fail" if any(check["status"] == "fail" for check in checks) else "pass"
    return result


def format_audit(result: dict[str, Any]) -> str:
    lines = ["Project Theta adversarial schedule audit", ""]
    for check in result["checks"]:
        lines.append(f"[{check['status'].upper():4}] {check['name']}: {check['detail']}")
    lines.extend(["", f"Overall: {result['status'].upper()}"])
    return "\n".join(lines)
