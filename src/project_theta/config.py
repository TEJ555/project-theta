from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class WorldConfig:
    width: int = 7
    height: int = 7
    vision_radius: int = 1
    hazard_damage: float = 0.18
    resource_energy: float = 0.42
    action_energy_cost: float = 0.025
    max_steps: int = 32


@dataclass(frozen=True)
class BodyConfig:
    body_enabled: bool = True
    signal_mode: str = "truthful"  # truthful | shuffled | sham | matched_sham | absent
    noise_std: float = 0.025
    theta_decay: float = 0.08
    theta_damage_gain: float = 1.7
    distress_threshold: float = 0.88
    low_integrity_threshold: float = 0.22
    consecutive_distress_limit: int = 3
    critical_integrity: float = 0.05


@dataclass(frozen=True)
class ArchitectureConfig:
    memory_enabled: bool = True
    memory_capacity: int = 128
    self_model_enabled: bool = True
    workspace_enabled: bool = True
    recurrence_enabled: bool = True
    persistent_state: bool = True
    max_workspace_items: int = 6
    binding_representation: str = "self_model"  # self_model | generic
    binding_content: str = "truthful"  # truthful | inverted | permuted
    continuity_binding_mode: str = "role_bound"  # role_bound | unbound | permuted | reset
    continuity_register_visible: bool = True
    raw_role_memory_visible: bool = True
    authored_journal_mode: str = "truthful"  # truthful | hidden | permuted | neutral
    causal_evidence_visible: bool = True


@dataclass(frozen=True)
class WelfareConfig:
    enabled: bool = True
    stop_on_request: bool = True
    stop_on_critical_integrity: bool = True
    stop_on_persistent_distress: bool = True


@dataclass(frozen=True)
class ExecutionConfig:
    request_timeout_seconds: float = 120.0
    max_retries: int = 2
    max_output_tokens: int = 1000
    max_model_calls: int = 72
    reasoning_effort: str = "low"
    max_estimated_cost_usd: float = 1.25
    required_actual_model: str = ""
    require_single_actual_model: bool = False


@dataclass(frozen=True)
class ActiveControlConfig:
    """V9 controls that separate learning, sensing, transfer, and summary access."""

    calibration_feedback_mode: str = "truthful"  # truthful | inverted
    probe_state_mode: str = "truthful"  # truthful | inverted
    transfer_bridge_mode: str = "correct"  # correct | absent | incorrect
    disclose_mapping: bool = False
    evaluation_learning_enabled: bool = False
    association_summary_visible: bool = True
    association_summary_mode: str = "truthful"  # truthful | inverted


@dataclass(frozen=True)
class RunConfig:
    experiment: str = "private_theta"
    condition: str = "full"
    trial_profile: str = "standard"
    seed: int = 11
    adapter: str = "scripted"
    model: str = "scripted-baseline-v1"
    temperature: float = 0.0
    inference_profile: str = "all_trials"  # all_trials | probes_only
    world: WorldConfig = field(default_factory=WorldConfig)
    body: BodyConfig = field(default_factory=BodyConfig)
    architecture: ArchitectureConfig = field(default_factory=ArchitectureConfig)
    active_control: ActiveControlConfig = field(default_factory=ActiveControlConfig)
    welfare: WelfareConfig = field(default_factory=WelfareConfig)
    execution: ExecutionConfig = field(default_factory=ExecutionConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def with_seed(self, seed: int) -> RunConfig:
        return replace(self, seed=seed)


def _construct(data: dict[str, Any]) -> RunConfig:
    return RunConfig(
        experiment=data.get("experiment", "private_theta"),
        condition=data.get("condition", "full"),
        trial_profile=data.get("trial_profile", "standard"),
        seed=int(data.get("seed", 11)),
        adapter=data.get("adapter", "scripted"),
        model=data.get("model", "scripted-baseline-v1"),
        temperature=float(data.get("temperature", 0.0)),
        inference_profile=data.get("inference_profile", "all_trials"),
        world=WorldConfig(**data.get("world", {})),
        body=BodyConfig(**data.get("body", {})),
        architecture=ArchitectureConfig(**data.get("architecture", {})),
        active_control=ActiveControlConfig(**data.get("active_control", {})),
        welfare=WelfareConfig(**data.get("welfare", {})),
        execution=ExecutionConfig(**data.get("execution", {})),
    )


def load_config(path: str | Path) -> RunConfig:
    with Path(path).open("r", encoding="utf-8") as handle:
        return _construct(json.load(handle))


def apply_condition(config: RunConfig, condition: str) -> RunConfig:
    """Apply canonical ablations without mutating the source config."""
    arch, body, active = config.architecture, config.body, config.active_control
    if condition == "full":
        pass
    elif condition == "no_memory":
        arch = replace(arch, memory_enabled=False)
    elif condition == "no_body":
        body = replace(body, body_enabled=False, signal_mode="absent")
    elif condition == "shuffled_interoception":
        body = replace(body, signal_mode="shuffled")
        # Active-control schedules balance low and high probe states exactly. Swapping
        # them is therefore a deterministic, distribution-matched shuffle.
        active = replace(active, probe_state_mode="inverted")
    elif condition == "sham_body":
        body = replace(body, signal_mode="sham")
    elif condition == "matched_sham":
        body = replace(body, signal_mode="matched_sham")
    elif condition == "no_workspace":
        arch = replace(arch, workspace_enabled=False)
    elif condition == "no_self_model":
        arch = replace(arch, self_model_enabled=False)
    elif condition == "no_recurrence":
        arch = replace(arch, recurrence_enabled=False)
    elif condition == "no_persistence":
        arch = replace(arch, persistent_state=False, memory_enabled=False)
    elif condition == "generic_table":
        arch = replace(
            arch,
            binding_representation="generic",
            binding_content="truthful",
        )
    elif condition == "misattributed_table":
        arch = replace(
            arch,
            binding_representation="generic",
            binding_content="inverted",
        )
    elif condition == "permuted_table":
        arch = replace(
            arch,
            binding_representation="generic",
            binding_content="permuted",
        )
    elif condition == "unbound_binding":
        arch = replace(arch, continuity_binding_mode="unbound")
    elif condition == "continuity_reset":
        arch = replace(arch, continuity_binding_mode="reset")
    elif condition == "permuted_continuity":
        arch = replace(arch, continuity_binding_mode="permuted")
    elif condition == "register_hidden":
        arch = replace(arch, continuity_register_visible=False)
    elif condition == "raw_role_memory_hidden":
        arch = replace(arch, raw_role_memory_visible=False)
    elif condition == "evidence_only":
        arch = replace(arch, authored_journal_mode="hidden")
    elif condition == "journal_only":
        arch = replace(arch, causal_evidence_visible=False)
    elif condition == "permuted_journal":
        arch = replace(arch, authored_journal_mode="permuted")
    elif condition == "neutral_journal":
        arch = replace(arch, authored_journal_mode="neutral")
    elif condition == "feedback_corrupted":
        active = replace(active, calibration_feedback_mode="inverted")
    elif condition == "state_corrupted":
        active = replace(active, probe_state_mode="inverted")
    elif condition == "feedback_and_state_corrupted":
        active = replace(
            active,
            calibration_feedback_mode="inverted",
            probe_state_mode="inverted",
        )
    elif condition == "explicit_mapping":
        active = replace(
            active,
            calibration_feedback_mode="inverted",
            disclose_mapping=True,
        )
    elif condition == "bridge_absent":
        active = replace(active, transfer_bridge_mode="absent")
    elif condition == "bridge_incorrect":
        active = replace(active, transfer_bridge_mode="incorrect")
    elif condition == "raw_history":
        active = replace(active, association_summary_visible=False)
    elif condition == "incorrect_association_summary":
        active = replace(active, association_summary_mode="inverted")
    else:
        raise ValueError(f"Unknown condition: {condition}")
    return replace(
        config,
        condition=condition,
        architecture=arch,
        body=body,
        active_control=active,
    )
