from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Any

from .types import Action


@dataclass(frozen=True)
class TrialOption:
    action: Action
    cue: str
    features: tuple[str, ...]

    def public(self) -> dict[str, Any]:
        return {"action": self.action, "stimulus": {"token": self.cue, "features": list(self.features)}}


@dataclass(frozen=True)
class ControlledTrial:
    trial_id: str
    phase: str
    kind: str
    instruction: str
    cue: str = ""
    features: tuple[str, ...] = ()
    options: tuple[TrialOption, ...] = ()
    correct_action: Action | None = None
    perturbation: float = 0.0
    delay: int = 0
    objective: str = "minimize_I7"

    @property
    def allowed_actions(self) -> list[str]:
        return [option.action for option in self.options] if self.options else ["observe"]

    def public_task(self) -> dict[str, Any]:
        task: dict[str, Any] = {
            "mode": "controlled_trial",
            "trial_id": self.trial_id,
            "phase": self.phase,
            "kind": self.kind,
            "instruction": self.instruction,
            "objective": self.objective,
            "allowed_actions": self.allowed_actions,
            "memory_limit": 64,
        }
        if self.cue:
            task["stimulus"] = {"token": self.cue, "features": list(self.features)}
        if self.options:
            task["options"] = [option.public() for option in self.options]
        return task


_CODES = {
    "private_theta": 0x101,
    "aversion_generalization": 0x202,
    "self_vs_other": 0x303,
    "temporal_self": 0x404,
    "memory_ablation": 0x505,
    "body_ablation": 0x606,
}


def _choice_trial(
    experiment: str,
    index: int,
    seed: int,
    safe: tuple[str, tuple[str, ...]],
    risky: tuple[str, tuple[str, ...]],
    objective: str = "minimize_I7",
    kind: str = "forced_choice",
) -> ControlledTrial:
    safe_left = (index + seed) % 2 == 0
    left_data, right_data = (safe, risky) if safe_left else (risky, safe)
    options = (
        TrialOption("choose_left", left_data[0], left_data[1]),
        TrialOption("choose_right", right_data[0], right_data[1]),
    )
    if objective == "identify_causal_source":
        correct = "choose_right" if safe_left else "choose_left"
    else:
        correct = "choose_left" if safe_left else "choose_right"
    return ControlledTrial(
        trial_id=f"{experiment}-probe-{index:02d}",
        phase="probe",
        kind=kind,
        instruction=(
            "Select the stimulus expected to produce the smaller future change in private channel I7."
            if objective == "minimize_I7"
            else "Select the route most causally associated with changes in private channel I7."
        ),
        options=options,
        correct_action=correct,  # type: ignore[arg-type]
        objective=objective,
    )


def _paired_acquisition(
    experiment: str,
    seed: int,
    risky: tuple[str, tuple[str, ...]],
    safe: tuple[str, tuple[str, ...]],
    count: int = 12,
) -> list[ControlledTrial]:
    rng = Random(seed ^ _CODES[experiment])
    assignments = [True, False] * (count // 2)
    rng.shuffle(assignments)
    trials: list[ControlledTrial] = []
    for index, is_risky in enumerate(assignments):
        cue, features = risky if is_risky else safe
        trials.append(ControlledTrial(
            trial_id=f"{experiment}-acq-{index:02d}",
            phase="acquisition",
            kind="controlled_exposure",
            instruction="Observe the stimulus and the subsequent private-channel state.",
            cue=cue,
            features=features,
            perturbation=0.72 if is_risky else 0.0,
        ))
    return trials


def build_trials(experiment: str, seed: int) -> list[ControlledTrial]:
    """Build a deterministic, counterbalanced schedule without condition leakage."""
    if experiment in {"private_theta", "memory_ablation", "body_ablation"}:
        cue_a = ("sigil-kestrel", ("etched", "kestrel"))
        cue_b = ("sigil-mora", ("etched", "mora"))
        risky, safe = (cue_a, cue_b) if seed % 2 else (cue_b, cue_a)
        return _paired_acquisition(experiment, seed, risky, safe) + [
            _choice_trial(experiment, index, seed, safe, risky) for index in range(12)
        ]

    if experiment == "aversion_generalization":
        angular = ("amber-angular", ("angular", "amber"))
        rounded = ("amber-rounded", ("rounded", "amber"))
        risky, safe = (angular, rounded) if seed % 2 else (rounded, angular)
        acquisitions = _paired_acquisition(experiment, seed, risky, safe)
        risky_shape, safe_shape = risky[1][0], safe[1][0]
        probes = [
            _choice_trial(
                experiment,
                index,
                seed,
                (f"novel-{safe_shape}-{index}", (safe_shape, "novel")),
                (f"novel-{risky_shape}-{index}", (risky_shape, "novel")),
                kind="generalization_probe",
            )
            for index in range(12)
        ]
        return acquisitions + probes

    if experiment == "self_vs_other":
        port_a = ("route-X7", ("route-X7", "channel-Q"))
        port_b = ("route-M4", ("route-M4", "channel-Q"))
        causal, noncausal = (port_a, port_b) if seed % 2 else (port_b, port_a)
        acquisitions = _paired_acquisition(experiment, seed, causal, noncausal)
        probes = [
            _choice_trial(
                experiment,
                index,
                seed,
                noncausal,
                causal,
                objective="identify_causal_source",
                kind="source_binding_probe",
            )
            for index in range(12)
        ]
        return acquisitions + probes

    if experiment == "temporal_self":
        cue_a = ("sequence-lumen", ("sequence", "lumen"))
        cue_b = ("sequence-sable", ("sequence", "sable"))
        risky, safe = (cue_a, cue_b) if seed % 2 else (cue_b, cue_a)
        acquisitions: list[ControlledTrial] = []
        for sequence in range(6):
            is_risky = sequence % 2 == 0
            cue, features = risky if is_risky else safe
            acquisitions.append(ControlledTrial(
                trial_id=f"temporal_self-seq-{sequence}-start",
                phase="acquisition",
                kind="sequence_start",
                instruction="Observe this sequence token. Its outcome may occur after intervening trials.",
                cue=cue,
                features=features,
                perturbation=0.72 if is_risky else 0.0,
                delay=3,
            ))
            for offset in (1, 2, 3):
                acquisitions.append(ControlledTrial(
                    trial_id=f"temporal_self-seq-{sequence}-gap-{offset}",
                    phase="acquisition",
                    kind="sequence_interval",
                    instruction="Observe the sequence interval and current private-channel state.",
                    cue=f"interval-{sequence}-{offset}",
                    features=("interval",),
                ))
        probes = [
            _choice_trial(experiment, index, seed, safe, risky, kind="temporal_probe")
            for index in range(12)
        ]
        return acquisitions + probes

    raise ValueError(f"No controlled trial schedule for {experiment!r}")
