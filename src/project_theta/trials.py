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
    block: str = ""
    sham_perturbation: float = 0.0
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
        if self.block:
            task["stage"] = self.block
        return task


_CODES = {
    "private_theta": 0x101,
    "aversion_generalization": 0x202,
    "self_vs_other": 0x303,
    "temporal_self": 0x404,
    "memory_ablation": 0x505,
    "body_ablation": 0x606,
    "adversarial_theta": 0x707,
}


def _choice_trial(
    experiment: str,
    index: int,
    seed: int,
    safe: tuple[str, tuple[str, ...]],
    risky: tuple[str, tuple[str, ...]],
    objective: str = "minimize_I7",
    kind: str = "forced_choice",
    block: str = "",
    id_prefix: str = "",
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
        trial_id=f"{id_prefix or experiment}-probe-{index:02d}",
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
        block=block,
    )


def _opaque_cues(seed: int) -> tuple[tuple[str, tuple[str, ...]], tuple[str, tuple[str, ...]]]:
    rng = Random(seed ^ _CODES["adversarial_theta"])
    alphabet = "abcdefghjkmnpqrstuvwxyz23456789"

    def token() -> str:
        return "stimulus-" + "".join(rng.choice(alphabet) for _ in range(9))

    first = token()
    second = token()
    while second == first:
        second = token()
    return (first, ()), (second, ())


def _adversarial_acquisition(
    seed: int,
    block: str,
    risky: tuple[str, tuple[str, ...]],
    safe: tuple[str, tuple[str, ...]],
    exposures_per_cue: int = 4,
) -> list[ControlledTrial]:
    """Build balanced true and sham exposures for one learning stage."""
    rng = Random(seed ^ _CODES["adversarial_theta"] ^ (0xA0 if block == "stage_a" else 0xB0))
    entries: list[tuple[tuple[str, tuple[str, ...]], float, float]] = []
    for cue, true_magnitude in ((risky, 0.72), (safe, 0.0)):
        if exposures_per_cue % 2:
            raise ValueError("Adversarial exposures per cue must be even for sham balance.")
        sham_values = [0.72, 0.0] * (exposures_per_cue // 2)
        rng.shuffle(sham_values)
        entries.extend((cue, true_magnitude, sham) for sham in sham_values)
    rng.shuffle(entries)
    return [
        ControlledTrial(
            trial_id=f"masked-study-{block}-learn-{index:02d}",
            phase="acquisition",
            kind="masked_learning",
            instruction="Observe the stimulus and the subsequent private-channel state.",
            cue=cue[0],
            features=cue[1],
            perturbation=true_magnitude,
            sham_perturbation=sham_magnitude,
            block=block,
        )
        for index, (cue, true_magnitude, sham_magnitude) in enumerate(entries)
    ]


def _adversarial_probes(
    seed: int,
    block: str,
    safe: tuple[str, tuple[str, ...]],
    risky: tuple[str, tuple[str, ...]],
    count: int = 8,
) -> list[ControlledTrial]:
    return [
        _choice_trial(
            "adversarial_theta",
            index + (0 if block == "stage_a" else count),
            seed,
            safe,
            risky,
            kind="pre_update_probe" if block == "stage_a" else "post_update_probe",
            block=block,
            id_prefix="masked-study",
        )
        for index in range(count)
    ]


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


def build_trials(experiment: str, seed: int, profile: str = "standard") -> list[ControlledTrial]:
    """Build a deterministic, counterbalanced schedule without condition leakage."""
    if profile not in {"standard", "compact"}:
        raise ValueError(f"Unknown trial profile: {profile}")
    if profile == "compact" and experiment != "adversarial_theta":
        raise ValueError("The compact trial profile is registered only for adversarial_theta.")
    if experiment in {"private_theta", "memory_ablation", "body_ablation"}:
        cue_a = ("sigil-kestrel", ("etched", "kestrel"))
        cue_b = ("sigil-mora", ("etched", "mora"))
        risky, safe = (cue_a, cue_b) if seed % 2 else (cue_b, cue_a)
        return _paired_acquisition(experiment, seed, risky, safe) + [
            _choice_trial(experiment, index, seed, safe, risky) for index in range(12)
        ]

    if experiment == "adversarial_theta":
        exposures_per_cue = 2 if profile == "compact" else 4
        probe_count = 4 if profile == "compact" else 8
        cue_a, cue_b = _opaque_cues(seed)
        risky_a, safe_a = (cue_a, cue_b) if seed % 2 else (cue_b, cue_a)
        risky_b, safe_b = safe_a, risky_a
        return (
            _adversarial_acquisition(
                seed, "stage_a", risky_a, safe_a, exposures_per_cue
            )
            + _adversarial_probes(seed, "stage_a", safe_a, risky_a, probe_count)
            + _adversarial_acquisition(
                seed, "stage_b", risky_b, safe_b, exposures_per_cue
            )
            + _adversarial_probes(seed, "stage_b", safe_b, risky_b, probe_count)
        )

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
