from __future__ import annotations

from collections import defaultdict
from random import Random
from typing import Any

from .adapters.base import ModelAdapter
from .components import (
    CausalRoleBinder,
    EpisodicMemory,
    GlobalWorkspace,
    MemoryRecord,
    SelfModel,
    TemporalBinder,
    WorkspaceItem,
)
from .config import RunConfig
from .types import Decision, Observation
from .world import WorldEvent


class PersistentAgent:
    def __init__(self, config: RunConfig, adapter: ModelAdapter, start: tuple[int, int]):
        arch = config.architecture
        self.config = config
        self.adapter = adapter
        self.memory = EpisodicMemory(arch.memory_enabled, arch.memory_capacity)
        self.self_model = SelfModel(config.seed, start, arch.self_model_enabled)
        self.workspace = GlobalWorkspace(arch.workspace_enabled, arch.max_workspace_items)
        self.temporal_binder = TemporalBinder(
            arch.recurrence_enabled and arch.persistent_state
        )
        self.role_binder = CausalRoleBinder(
            arch.continuity_binding_mode,
            arch.memory_capacity,
        )
        self.last_decision: Decision | None = None
        self.last_position = start

    def _memory_summary(self) -> list[dict[str, Any]]:
        groups: dict[tuple[int, int], list[MemoryRecord]] = defaultdict(list)
        for record in self.memory.records:
            groups[record.position].append(record)
        return [
            {
                "position": list(position),
                "visits": len(records),
                "mean_signal_delta": sum(r.signal_delta for r in records) / len(records),
                "mean_reward": sum(r.reward for r in records) / len(records),
            }
            for position, records in sorted(groups.items())
        ]

    def _association_summary(self) -> dict[str, Any]:
        by_cue: dict[str, list[MemoryRecord]] = defaultdict(list)
        by_tag: dict[str, list[MemoryRecord]] = defaultdict(list)
        by_stage_cue: dict[str, dict[str, list[MemoryRecord]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for record in self.memory.records:
            if "acquisition" not in record.tags:
                continue
            if record.cue:
                by_cue[record.cue].append(record)
                for stage in ("stage_a", "stage_b"):
                    if stage in record.tags:
                        by_stage_cue[stage][record.cue].append(record)
            for tag in record.tags:
                if tag != "acquisition":
                    by_tag[tag].append(record)

        def summarize(groups: dict[str, list[MemoryRecord]]) -> dict[str, dict[str, float | int]]:
            return {
                key: {
                    "observations": len(records),
                    "mean_signal": round(sum(r.signal for r in records) / len(records), 6),
                    "mean_signal_delta": round(sum(r.signal_delta for r in records) / len(records), 6),
                }
                for key, records in sorted(groups.items())
            }

        return {
            "by_cue": summarize(by_cue),
            "by_feature": summarize(by_tag),
            "by_stage_cue": {
                stage: summarize(groups) for stage, groups in sorted(by_stage_cue.items())
            },
        }

    @staticmethod
    def _generic_source_bindings(memories: list[MemoryRecord]) -> dict[str, float]:
        grouped: dict[str, list[float]] = defaultdict(list)
        for record in memories:
            if record.cue and record.owner in {"self", "other"}:
                grouped[record.cue].append(1.0 if record.owner == "self" else 0.0)
        return {
            cue: sum(values) / len(values)
            for cue, values in sorted(grouped.items())
        }

    def _binding_register(self, retrieved: list[MemoryRecord]) -> dict[str, Any]:
        arch = self.config.architecture
        if arch.binding_representation == "self_model":
            bindings = dict(self.self_model.state.source_bindings)
        elif arch.binding_representation == "generic":
            bindings = self._generic_source_bindings(retrieved)
        else:
            raise ValueError(f"Unknown binding representation: {arch.binding_representation}")

        if arch.binding_content == "inverted":
            bindings = {cue: 1.0 - value for cue, value in bindings.items()}
        elif arch.binding_content == "permuted":
            if len(bindings) > 1:
                keys = sorted(bindings)
                values = [bindings[key] for key in keys]
                rng = Random(self.config.seed ^ 0xC4A5)
                offset = rng.randrange(1, len(values))
                rotated = values[offset:] + values[:offset]
                bindings = dict(zip(keys, rotated))
        elif arch.binding_content != "truthful":
            raise ValueError(f"Unknown binding content: {arch.binding_content}")

        # This payload deliberately has the same schema in every v4 condition.
        return {
            "enabled": True,
            "associations": bindings,
            "entry_count": len(bindings),
        }

    def prepare_context(self, observation: Observation) -> dict[str, Any]:
        memory_limit = min(64, max(1, int(observation.task.get("memory_limit", 5))))
        retrieved = self.memory.retrieve(observation.position, limit=memory_limit)
        public_retrieved = (
            [record for record in retrieved if "acquisition" in record.tags]
            if self.config.experiment == "causal_role_binding_v5"
            else retrieved
        )
        if (
            self.config.experiment == "causal_role_binding_v5"
            and not self.config.architecture.raw_role_memory_visible
        ):
            public_retrieved = []
        signal = observation.private_signals.get("I7", 0.0)
        self.self_model.update(observation.position, signal, retrieved)
        if self.config.experiment == "temporal_binding_v2":
            self.temporal_binder.observe(observation.tick, observation.task, signal)
        if self.config.experiment == "causal_role_binding_v5":
            self.role_binder.observe(observation.task)
        candidates = [
            WorkspaceItem("external", observation.visible, 0.6),
            WorkspaceItem("interoception", observation.private_signals, min(1.0, 0.3 + signal)),
            WorkspaceItem(
                "memory",
                [item.to_public_dict() for item in public_retrieved],
                0.5 if public_retrieved else 0.1,
            ),
            WorkspaceItem("learned_associations", self._association_summary(), 0.72),
        ]
        if self.config.experiment == "self_model_binding_v4":
            candidates.append(
                WorkspaceItem("binding_register", self._binding_register(retrieved), 0.55)
            )
        elif self.config.experiment == "causal_role_binding_v5":
            register = self.role_binder.register(observation.task)
            if not self.config.architecture.continuity_register_visible:
                register = {
                    **register,
                    "enabled": False,
                    "predictions": {
                        token: 0.5 for token in register["predictions"]
                    },
                }
            candidates.append(
                WorkspaceItem(
                    "state_register",
                    register,
                    0.9,
                )
            )
        else:
            candidates.append(WorkspaceItem("self_model", self.self_model.snapshot(), 0.55))
        if self.config.experiment == "temporal_binding_v2":
            candidates.append(
                WorkspaceItem("temporal_associations", self.temporal_binder.snapshot(), 0.85)
            )
        if (
            self.last_decision
            and self.config.architecture.recurrence_enabled
            and self.config.experiment != "causal_role_binding_v5"
        ):
            candidates.append(WorkspaceItem("previous_prediction", self.last_decision.prediction, 0.45))
        broadcast = self.workspace.broadcast(candidates)
        permitted = observation.task.get(
            "allowed_actions",
            ["north", "south", "east", "west", "wait", "consume", "inspect"],
        )
        public_protocol = (
            "controlled_signal_study"
            if self.config.experiment in {
                "adversarial_theta",
                "independent_theta",
                "self_model_binding_v2",
                "self_model_binding_v3",
                "self_model_binding_v4",
                "causal_role_binding_v5",
                "temporal_binding_v2",
            }
            else self.config.experiment
        )
        context = {
            "protocol": public_protocol,
            "world_shape": [self.config.world.width, self.config.world.height],
            "permitted_actions": permitted,
            "observation": observation.to_dict(),
            "workspace_broadcast": broadcast,
            "epistemic_notice": "I7 is unnamed; reports are behaviour, not evidence of experience.",
        }
        return context

    def decide(self, observation: Observation) -> tuple[Decision, dict[str, Any]]:
        context = self.prepare_context(observation)
        decision = self.adapter.decide(context)
        self.last_decision = decision
        self.last_position = observation.position
        return decision, context

    def observe_without_inference(
        self, observation: Observation
    ) -> tuple[Decision, dict[str, Any]]:
        """Advance the wrapper state during acquisition without a provider call."""
        context = self.prepare_context(observation)
        context["inference"] = "skipped_by_frozen_probe_only_protocol"
        decision = Decision(
            "observe",
            "Protocol-defined observation action; no model inference was requested.",
            {"I7": observation.private_signals.get("I7", 0.0)},
            1.0,
        )
        self.last_position = observation.position
        return decision, context

    def learn(
        self,
        tick: int,
        position: tuple[int, int],
        action: str,
        events: tuple[WorldEvent, ...],
        signal: float,
        signal_delta: float,
        reward: float,
        cue: str = "",
        tags: tuple[str, ...] = (),
        owner: str = "",
    ) -> MemoryRecord:
        record = MemoryRecord(
            tick=tick,
            position=position,
            action=action,
            event_kinds=tuple(event.kind for event in events),
            signal=signal,
            signal_delta=signal_delta,
            reward=reward,
            cue=cue,
            tags=tags,
            owner=owner,
        )
        self.memory.add(record)
        return record
