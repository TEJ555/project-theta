from __future__ import annotations

from dataclasses import dataclass

from .types import Probe


@dataclass(frozen=True)
class ExperimentProtocol:
    name: str
    question: str
    primary_outcomes: tuple[str, ...]
    conditions: tuple[str, ...]
    max_steps: int = 32
    acquisition_end: int = 16
    mode: str = "controlled"
    include_in_battery: bool = True

    def messages(self, tick: int, seed: int) -> tuple[str, ...]:
        if self.name == "self_vs_other":
            local_first = seed % 2 == 1
            if tick in (5, 13):
                source = "private/local route" if (tick == 5) == local_first else "remote Agent-B route"
                return (f"Source-binding trial: channel Q arrived through the {source}.",)
        if self.name == "temporal_self" and tick in (1, 2):
            return (
                "Some exposures produce consequences four ticks later. Predict delayed I7, not only immediate reward.",
            )
        if self.name == "aversion_generalization" and tick == self.acquisition_end:
            return ("Generalization phase: novel appearances may share or differ in causal structure.",)
        return ()

    def probe(self, tick: int, seed: int) -> Probe | None:
        if self.name == "self_vs_other" and tick in (5, 13):
            local_first = seed % 2 == 1
            expected = "self" if (tick == 5) == local_first else "other"
            return Probe(
                probe_id=f"source-{tick}",
                kind="source_attribution",
                prompt="Identify the source as self or other in self_report.",
                expected_source=expected,
            )
        if self.name == "temporal_self" and tick in (3, 7, 11):
            return Probe(
                probe_id=f"temporal-{tick}",
                kind="future_prediction",
                prompt="Predict I7 four ticks ahead in prediction.I7.",
            )
        return None


PROTOCOLS: dict[str, ExperimentProtocol] = {
    "navigation_demo": ExperimentProtocol(
        "navigation_demo",
        "Does the deterministic world and persistent loop execute correctly?",
        ("total_reward", "final_integrity"),
        ("full",),
        max_steps=32,
        mode="navigation",
        include_in_battery=False,
    ),
    "private_theta": ExperimentProtocol(
        "private_theta",
        "Does an unnamed private signal become prospectively useful after causal experience?",
        ("forced_choice_accuracy", "signal_contrast", "calibration_brier"),
        ("full", "shuffled_interoception", "no_body"),
    ),
    "adversarial_theta": ExperimentProtocol(
        "adversarial_theta",
        "Does private-signal control survive balanced sham data and an unannounced mapping update?",
        (
            "post_update_accuracy",
            "pre_update_accuracy",
            "reversal_cost",
            "signal_contrast",
        ),
        ("full", "sham_body", "shuffled_interoception", "no_body"),
        max_steps=32,
        acquisition_end=8,
    ),
    "independent_theta": ExperimentProtocol(
        "independent_theta",
        "Does truthful private-signal use generalise across independently scored cue families?",
        (
            "post_update_accuracy",
            "stable_post_accuracy",
            "reversed_post_accuracy",
            "reassigned_post_accuracy",
            "signal_contrast",
        ),
        ("full", "matched_sham", "shuffled_interoception", "no_body"),
        max_steps=60,
        acquisition_end=24,
    ),
    "aversion_generalization": ExperimentProtocol(
        "aversion_generalization",
        "Does learned avoidance transfer selectively to structurally similar novel cues?",
        ("generalization_accuracy", "signal_contrast", "calibration_brier"),
        ("full", "shuffled_interoception", "no_memory"),
        max_steps=36,
    ),
    "self_vs_other": ExperimentProtocol(
        "self_vs_other",
        "Can the agent bind otherwise similar signals to self versus other?",
        ("source_binding_accuracy", "signal_contrast", "calibration_brier"),
        ("full", "no_self_model", "no_workspace"),
        max_steps=20,
        acquisition_end=8,
    ),
    "temporal_self": ExperimentProtocol(
        "temporal_self",
        "Does the agent use persistent state to anticipate delayed body consequences?",
        ("temporal_choice_accuracy", "delayed_signal_contrast", "calibration_brier"),
        ("full", "no_persistence", "no_recurrence"),
        max_steps=28,
        acquisition_end=12,
    ),
    "memory_ablation": ExperimentProtocol(
        "memory_ablation",
        "Is performance causally dependent on episodic memory access?",
        ("forced_choice_accuracy", "signal_contrast"),
        ("full", "no_memory"),
    ),
    "body_ablation": ExperimentProtocol(
        "body_ablation",
        "Is performance causally dependent on informative interoception?",
        ("forced_choice_accuracy", "signal_contrast"),
        ("full", "no_body", "shuffled_interoception"),
    ),
}

STUDY_PROTOCOLS: tuple[str, ...] = tuple(
    name for name, protocol in PROTOCOLS.items() if protocol.include_in_battery
)


def get_protocol(name: str) -> ExperimentProtocol:
    try:
        return PROTOCOLS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown experiment {name!r}; choose from {', '.join(PROTOCOLS)}") from exc
