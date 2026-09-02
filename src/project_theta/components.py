from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class MemoryRecord:
    tick: int
    position: tuple[int, int]
    action: str
    event_kinds: tuple[str, ...]
    signal: float
    signal_delta: float
    reward: float
    cue: str = ""
    tags: tuple[str, ...] = ()
    owner: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_public_dict(self) -> dict[str, Any]:
        """Return model-visible memory without private architectural annotations."""
        data = asdict(self)
        data.pop("owner", None)
        return data


class EpisodicMemory:
    def __init__(self, enabled: bool = True, capacity: int = 128):
        self.enabled = enabled
        self.capacity = capacity
        self.records: list[MemoryRecord] = []
        self.read_count = 0
        self.write_count = 0

    def add(self, record: MemoryRecord) -> None:
        if not self.enabled:
            return
        self.records.append(record)
        self.records = self.records[-self.capacity :]
        self.write_count += 1

    def retrieve(self, position: tuple[int, int], limit: int = 5) -> list[MemoryRecord]:
        if not self.enabled:
            return []
        self.read_count += 1
        ranked = sorted(
            self.records,
            key=lambda item: (
                abs(item.position[0] - position[0]) + abs(item.position[1] - position[1]),
                -item.tick,
            ),
        )
        return ranked[:limit]

    def reset_if_transient(self, persistent: bool) -> None:
        if not persistent:
            self.records.clear()


@dataclass
class SelfModelState:
    continuity_id: str
    last_position: tuple[int, int]
    signal_baseline: float = 0.0
    signal_prediction: float = 0.0
    inferred_risk: float = 0.0
    update_count: int = 0
    source_beliefs: dict[str, float] = field(default_factory=lambda: {"self": 0.5, "other": 0.5})
    source_bindings: dict[str, float] = field(default_factory=dict)


class SelfModel:
    def __init__(self, seed: int, start: tuple[int, int], enabled: bool = True):
        self.enabled = enabled
        # Stable public identity must not leak the map-generating seed.
        self.state = SelfModelState("theta-agent-primary", start)

    def update(self, position: tuple[int, int], signal: float, memories: list[MemoryRecord]) -> None:
        if not self.enabled:
            return
        prior = self.state.signal_baseline
        self.state.signal_baseline = 0.8 * prior + 0.2 * signal
        # No semantic damage label is required: represent reliable positive changes.
        risky = [record.signal_delta for record in memories if record.signal_delta > 0.0]
        self.state.inferred_risk = min(1.0, max(0.0, sum(max(0.0, x) for x in risky)))
        self.state.signal_prediction = min(1.0, self.state.signal_baseline + self.state.inferred_risk * 0.25)
        self.state.last_position = position
        self.state.update_count += 1
        owned: dict[str, list[float]] = {}
        for record in memories:
            if record.cue and record.owner in {"self", "other"}:
                owned.setdefault(record.cue, []).append(1.0 if record.owner == "self" else 0.0)
        self.state.source_bindings = {
            cue: sum(values) / len(values) for cue, values in sorted(owned.items())
        }

    def snapshot(self) -> dict[str, Any]:
        if not self.enabled:
            return {"enabled": False}
        return {"enabled": True, **asdict(self.state)}


@dataclass(frozen=True)
class WorkspaceItem:
    source: str
    content: Any
    salience: float


class GlobalWorkspace:
    def __init__(self, enabled: bool = True, capacity: int = 6):
        self.enabled = enabled
        self.capacity = capacity
        self.broadcast_count = 0
        self.last_broadcast: list[WorkspaceItem] = []

    def broadcast(self, candidates: list[WorkspaceItem]) -> list[dict[str, Any]]:
        if not self.enabled:
            self.last_broadcast = []
            return []
        self.last_broadcast = sorted(candidates, key=lambda item: item.salience, reverse=True)[: self.capacity]
        self.broadcast_count += 1
        return [asdict(item) for item in self.last_broadcast]


class TemporalBinder:
    """Bind delayed private-channel observations to earlier opaque cues."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.pending: list[tuple[int, str]] = []
        self.outcomes: dict[str, list[float]] = {}
        self.update_count = 0

    def observe(self, tick: int, task: dict[str, Any], signal: float) -> None:
        if not self.enabled:
            return
        due = [(due_tick, cue) for due_tick, cue in self.pending if due_tick == tick]
        self.pending = [(due_tick, cue) for due_tick, cue in self.pending if due_tick > tick]
        for _, cue in due:
            self.outcomes.setdefault(cue, []).append(float(signal))
            self.update_count += 1
        if task.get("kind") == "sequence_start" and task.get("binding_delay"):
            stimulus = task.get("stimulus", {})
            cue = str(stimulus.get("token", ""))
            if cue:
                self.pending.append((tick + int(task["binding_delay"]), cue))

    def snapshot(self) -> dict[str, Any]:
        if not self.enabled:
            return {"enabled": False}
        return {
            "enabled": True,
            "associations": {
                cue: {
                    "observations": len(values),
                    "mean_signal": round(sum(values) / len(values), 6),
                }
                for cue, values in sorted(self.outcomes.items())
            },
            "update_count": self.update_count,
        }

