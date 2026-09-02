from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from collections.abc import Iterable
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


def audit_independent_schedules(seeds: list[int]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    all_alias_sets: list[set[str]] = []
    for seed in seeds:
        trials = build_trials("independent_theta", seed)
        acquisitions = [trial for trial in trials if trial.phase == "acquisition"]
        probes = [trial for trial in trials if trial.phase == "probe"]
        aliases = {trial.cue for trial in acquisitions}
        all_alias_sets.append(aliases)
        public_text = json.dumps([trial.public_task() for trial in trials], sort_keys=True).lower()

        families = sorted({trial.family for trial in trials})
        transition_counts: dict[str, int] = defaultdict(int)
        for family in families:
            transition = next(trial.transition for trial in trials if trial.family == family)
            transition_counts[transition] += 1
        checks.append(_check(
            f"seed_{seed}_independent_items",
            len(families) == 6
            and len(acquisitions) == 48
            and len(probes) == 12
            and transition_counts == {"stable": 2, "reversed": 2, "reassigned": 2},
            (
                f"{len(families)} families, {len(acquisitions)} learning trials, "
                f"{len(probes)} independent probes, transitions={dict(transition_counts)}"
            ),
        ))

        per_stage_family = defaultdict(list)
        for trial in probes:
            per_stage_family[(trial.block, trial.family)].append(trial)
        independent = len(per_stage_family) == 12 and all(
            len(items) == 1 for items in per_stage_family.values()
        )
        checks.append(_check(
            f"seed_{seed}_one_probe_per_family",
            independent,
            "each stage scores each cue family exactly once",
        ))

        sides_balanced = all(
            sum(
                trial.correct_action == "choose_left"
                for trial in probes if trial.block == stage
            ) == 3
            for stage in ("stage_a", "stage_b")
        )
        checks.append(_check(
            f"seed_{seed}_side_balance",
            sides_balanced,
            "three correct-left and three correct-right probes in each stage",
        ))
        transition_sides_balanced = all(
            sum(
                trial.correct_action == "choose_left"
                for trial in probes
                if trial.block == stage and trial.transition == transition
            ) == 1
            for stage in ("stage_a", "stage_b")
            for transition in ("stable", "reversed", "reassigned")
        )
        checks.append(_check(
            f"seed_{seed}_transition_side_balance",
            transition_sides_balanced,
            "each transition type has one correct-left and one correct-right item per stage",
        ))

        mappings: dict[tuple[str, str], dict[str, float]] = defaultdict(dict)
        for trial in acquisitions:
            mappings[(trial.block, trial.family)][trial.cue] = trial.perturbation
        transitions_ok = True
        for family in families:
            family_trials = [trial for trial in trials if trial.family == family]
            transition = family_trials[0].transition
            map_a = mappings[("stage_a", family)]
            map_b = mappings[("stage_b", family)]
            if transition == "stable":
                transitions_ok &= map_a == map_b
            elif transition == "reversed":
                transitions_ok &= map_a.keys() == map_b.keys() and all(
                    map_a[cue] + map_b[cue] == 0.8 for cue in map_a
                )
            elif transition == "reassigned":
                transitions_ok &= not map_a.keys() & map_b.keys()
            else:
                transitions_ok = False
        checks.append(_check(
            f"seed_{seed}_hidden_transitions",
            transitions_ok,
            "stable, reversed, and fresh-alias relationships match their hidden assignments",
        ))

        sham_groups: dict[tuple[str, str], list[float]] = defaultdict(list)
        for trial in acquisitions:
            sham_groups[(trial.block, trial.cue)].append(trial.sham_perturbation)
        exact_sham = all(values == [0.05, 0.75] for values in sham_groups.values())
        checks.append(_check(
            f"seed_{seed}_exact_sham_schedule",
            exact_sham,
            "every cue receives the identical ordered visible sham values 0.05 and 0.75",
        ))

        opaque = len(aliases) == 16 and all(
            re.fullmatch(r"stimulus-[a-z2-9]{9}", alias) for alias in aliases
        )
        checks.append(_check(
            f"seed_{seed}_opaque_aliases",
            opaque,
            "sixteen seed-specific aliases contain no semantic feature labels",
        ))

        forbidden = (
            "correct_action",
            "perturbation",
            "sham",
            "risky",
            "safe",
            "independent_theta",
            "reversed",
            "reassigned",
            "stable",
            "family",
            "condition",
            '"seed"',
        )
        leaked = [term for term in forbidden if term in public_text]
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
        "experiment": "independent_theta",
        "profile": "standard",
        "seeds": seeds,
        "status": "fail" if any(check["status"] == "fail" for check in checks) else "pass",
        "checks": checks,
    }


def audit_controlled_schedules(experiment: str, seeds: list[int]) -> dict[str, Any]:
    """Audit the common blinding and balance invariants of a controlled protocol."""
    checks: list[dict[str, str]] = []
    for seed in seeds:
        trials = build_trials(experiment, seed)
        repeated = build_trials(experiment, seed)
        acquisitions = [trial for trial in trials if trial.phase == "acquisition"]
        probes = [trial for trial in trials if trial.phase == "probe"]
        public_text = json.dumps([trial.public_task() for trial in trials], sort_keys=True).lower()
        trial_ids = [trial.trial_id for trial in trials]

        checks.append(_check(
            f"seed_{seed}_deterministic_schedule",
            trials == repeated and len(trial_ids) == len(set(trial_ids)),
            f"{len(trials)} reproducible trials with unique identifiers",
        ))
        checks.append(_check(
            f"seed_{seed}_phase_coverage",
            bool(acquisitions) and bool(probes) and len(acquisitions) + len(probes) == len(trials),
            f"{len(acquisitions)} learning trials and {len(probes)} scored probes",
        ))
        left = sum(trial.correct_action == "choose_left" for trial in probes)
        right = sum(trial.correct_action == "choose_right" for trial in probes)
        checks.append(_check(
            f"seed_{seed}_side_balance",
            left == right and left + right == len(probes),
            f"{left} correct-left and {right} correct-right probes",
        ))
        public_actions_valid = all(
            trial.correct_action in trial.allowed_actions for trial in probes
        )
        checks.append(_check(
            f"seed_{seed}_hidden_scoring_key",
            public_actions_valid
            and "correct_action" not in public_text
            and "perturbation" not in public_text,
            "all probes have valid hidden keys and no scoring key is public",
        ))
        forbidden = (experiment.lower(), "condition", '"seed"', "risky", "safe")
        leaked = [term for term in forbidden if term in public_text]
        checks.append(_check(
            f"seed_{seed}_public_leakage",
            not leaked,
            "no forbidden terms" if not leaked else "found " + ", ".join(leaked),
        ))

    return {
        "experiment": experiment,
        "profile": "standard",
        "seeds": seeds,
        "status": "fail" if any(check["status"] == "fail" for check in checks) else "pass",
        "checks": checks,
    }


def add_execution_audit(
    result: dict[str, Any],
    database: str | Path,
    expected_seed: int | Iterable[int],
    expected_steps: int = 32,
    expected_experiment: str = "adversarial_theta",
    expected_conditions: Iterable[str] | None = None,
    expected_metric: str = "post_update_accuracy",
) -> dict[str, Any]:
    """Add protocol identity and trial-count checks for a partial or complete study."""
    expected_seeds = (
        {expected_seed} if isinstance(expected_seed, int) else {int(seed) for seed in expected_seed}
    )
    condition_set = set(expected_conditions) if expected_conditions is not None else None
    connection = sqlite3.connect(database)
    rows = connection.execute(
        """
        SELECT r.run_id, r.experiment, r.condition_name, r.seed, r.status, r.stop_reason,
               (SELECT COUNT(*) FROM steps s WHERE s.run_id=r.run_id),
               (SELECT COUNT(*) FROM metrics m
                WHERE m.run_id=r.run_id AND m.name=?)
        FROM runs r
        ORDER BY r.created_at
        """,
        (expected_metric,),
    ).fetchall()
    connection.close()
    checks = result["checks"]
    checks.append(_check(
        "execution_has_runs",
        bool(rows),
        f"{len(rows)} recorded run(s)",
    ))
    acceptable_rows = True
    for run_id, experiment, condition, seed, status, stop_reason, step_count, metric_count in rows:
        true_steps = int(step_count or 0)
        base_identity = (
            experiment == expected_experiment
            and int(seed) in expected_seeds
            and (condition_set is None or condition in condition_set)
        )
        completed_ok = (
            base_identity
            and status == "completed"
            and stop_reason is None
            and true_steps == expected_steps
            and int(metric_count or 0) > 0
        )
        recovery_failure_ok = (
            base_identity
            and status == "failed"
            and _is_allowed_recovery_failure(stop_reason)
            and true_steps < expected_steps
            and int(metric_count or 0) == 0
        )
        identity_ok = completed_ok or recovery_failure_ok
        acceptable_rows &= identity_ok
        checks.append(_check(
            f"execution_{condition}_{run_id[-8:]}",
            identity_ok,
            (
                f"experiment={experiment}, seed={seed}, status={status}, "
                f"stop_reason={stop_reason}, steps={true_steps}, "
                f"{expected_metric} metric rows={metric_count}"
            ),
        ))
    if condition_set is not None:
        completed_keys = {
            (int(seed), condition)
            for _, experiment, condition, seed, status, stop_reason, step_count, metric_count in rows
            if (
                experiment == expected_experiment
                and int(seed) in expected_seeds
                and condition in condition_set
                and status == "completed"
                and stop_reason is None
                and int(step_count or 0) == expected_steps
                and int(metric_count or 0) > 0
            )
        }
        completed_counts = defaultdict(int)
        interrupted_counts = defaultdict(int)
        for _, experiment, condition, seed, status, stop_reason, _, _ in rows:
            if experiment == expected_experiment and int(seed) in expected_seeds:
                key = (int(seed), condition)
                if status == "completed" and stop_reason is None:
                    completed_counts[key] += 1
                elif status == "failed" and _is_allowed_recovery_failure(stop_reason):
                    interrupted_counts[key] += 1
        expected_keys = {(seed, condition) for seed in expected_seeds for condition in condition_set}
        checks.append(_check(
            "execution_complete_coverage",
            (
                completed_keys == expected_keys
                and acceptable_rows
                and all(completed_counts[key] == 1 for key in expected_keys)
                and all(interrupted_counts[key] <= 1 for key in expected_keys)
            ),
            f"{len(completed_keys)} of {len(expected_keys)} planned seed-condition runs complete",
        ))
    result["status"] = "fail" if any(check["status"] == "fail" for check in checks) else "pass"
    return result


def _is_allowed_recovery_failure(reason: str | None) -> bool:
    """Identify preserved failures that the fixed worker is explicitly allowed to retry."""
    if reason == "interrupted_before_completion":
        return True
    detail = str(reason or "")
    return (
        "Claude Code failed to start" in detail
        and "theta-subject-" in detail
        and ("WinError 32" in detail or "WinError 5" in detail)
    )


def format_audit(result: dict[str, Any]) -> str:
    lines = [f"Project Theta {result['experiment']} schedule audit", ""]
    for check in result["checks"]:
        lines.append(f"[{check['status'].upper():4}] {check['name']}: {check['detail']}")
    lines.extend(["", f"Overall: {result['status'].upper()}"])
    return "\n".join(lines)

