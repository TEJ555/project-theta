from __future__ import annotations

from collections import defaultdict
from typing import Any

from .adapters.base import ModelAdapter
from .components import EpisodicMemory, GlobalWorkspace, MemoryRecord, SelfModel, WorkspaceItem
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

    def decide(self, observation: Observation) -> tuple[Decision, dict[str, Any]]:
        memory_limit = min(64, max(1, int(observation.task.get("memory_limit", 5))))
        retrieved = self.memory.retrieve(observation.position, limit=memory_limit)
        signal = observation.private_signals.get("I7", 0.0)
        self.self_model.update(observation.position, signal, retrieved)
        candidates = [
            WorkspaceItem("external", observation.visible, 0.6),
            WorkspaceItem("interoception", observation.private_signals, min(1.0, 0.3 + signal)),
            WorkspaceItem("memory", [item.to_dict() for item in retrieved], 0.5 if retrieved else 0.1),
            WorkspaceItem("learned_associations", self._association_summary(), 0.72),
            WorkspaceItem("self_model", self.self_model.snapshot(), 0.55),
        ]
        if self.last_decision and self.config.architecture.recurrence_enabled:
            candidates.append(WorkspaceItem("previous_prediction", self.last_decision.prediction, 0.45))
        broadcast = self.workspace.broadcast(candidates)
        permitted = observation.task.get(
            "allowed_actions",
            ["north", "south", "east", "west", "wait", "consume", "inspect"],
        )
        public_protocol = (
            "controlled_signal_study"
            if self.config.experiment in {"adversarial_theta", "independent_theta"}
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
        decision = self.adapter.decide(context)
        self.last_decision = decision
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
        )
        self.memory.add(record)
        return record
