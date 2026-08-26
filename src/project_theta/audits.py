from __future__ import annotations

import json
import re
from collections import defaultdict
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


def audit_adversarial_schedules(seeds: list[int]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    all_alias_sets: list[set[str]] = []
    for seed in seeds:
        trials = build_trials("adversarial_theta", seed)
        public_text = json.dumps([trial.public_task() for trial in trials], sort_keys=True)
        probes = [trial for trial in trials if trial.phase == "probe"]
        acquisitions = [trial for trial in trials if trial.phase == "acquisition"]
        aliases = {trial.cue for trial in acquisitions}
        all_alias_sets.append(aliases)

        checks.append(_check(
            f"seed_{seed}_schedule",
            len(trials) == 32 and len(acquisitions) == 16 and len(probes) == 16,
            f"{len(acquisitions)} learning trials and {len(probes)} probes",
        ))
        stage_balance = all(
            sum(
                trial.correct_action == "choose_left"
                for trial in probes if trial.block == stage
            ) == 4
            for stage in ("stage_a", "stage_b")
        )
        checks.append(_check(
            f"seed_{seed}_side_balance",
            stage_balance,
            "four correct-left and four correct-right probes in each stage",
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
        sham_balanced = all(
            sorted(values) == [0.0, 0.0, 0.72, 0.72]
            for values in sham_groups.values()
        )
        checks.append(_check(
            f"seed_{seed}_sham_balance",
            sham_balanced,
            "each cue receives two high and two low sham outcomes per stage",
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
        "seeds": seeds,
        "status": "fail" if any(check["status"] == "fail" for check in checks) else "pass",
        "checks": checks,
    }


def format_audit(result: dict[str, Any]) -> str:
    lines = ["Project Theta adversarial schedule audit", ""]
    for check in result["checks"]:
        lines.append(f"[{check['status'].upper():4}] {check['name']}: {check['detail']}")
    lines.extend(["", f"Overall: {result['status'].upper()}"])
    return "\n".join(lines)
