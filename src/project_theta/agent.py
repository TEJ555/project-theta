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

    def decide(self, observation: Observation) -> tuple[Decision, dict[str, Any]]:
        retrieved = self.memory.retrieve(observation.position)
        signal = observation.private_signals.get("I7", 0.0)
        self.self_model.update(observation.position, signal, retrieved)
        candidates = [
            WorkspaceItem("external", observation.visible, 0.6),
            WorkspaceItem("interoception", observation.private_signals, min(1.0, 0.3 + signal)),
            WorkspaceItem("memory", [item.to_dict() for item in retrieved], 0.5 if retrieved else 0.1),
            WorkspaceItem("self_model", self.self_model.snapshot(), 0.55),
        ]
        if self.last_decision and self.config.architecture.recurrence_enabled:
            candidates.append(WorkspaceItem("previous_prediction", self.last_decision.prediction, 0.45))
        broadcast = self.workspace.broadcast(candidates)
        context = {
            "protocol": self.config.experiment,
            "world_shape": [self.config.world.width, self.config.world.height],
            "permitted_actions": ["north", "south", "east", "west", "wait", "consume", "inspect"],
            "observation": observation.to_dict(),
            "workspace_broadcast": broadcast,
            "self_model": self.self_model.snapshot(),
            "retrieved_memories": [item.to_dict() for item in retrieved],
            "memory_summary": self._memory_summary(),
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
        )
        self.memory.add(record)
        return record
