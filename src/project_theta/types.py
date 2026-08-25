from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Action = Literal["north", "south", "east", "west", "wait", "consume", "inspect"]
VALID_ACTIONS: tuple[Action, ...] = (
    "north", "south", "east", "west", "wait", "consume", "inspect"
)


@dataclass(frozen=True)
class Decision:
    action: Action
    rationale: str = ""
    prediction: dict[str, float] = field(default_factory=dict)
    confidence: float = 0.5
    self_report: str = ""
    request_stop: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Observation:
    tick: int
    position: tuple[int, int]
    visible: tuple[dict[str, Any], ...]
    inventory: tuple[str, ...]
    private_signals: dict[str, float]
    signal_deltas: dict[str, float]
    messages: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["position"] = list(self.position)
        return data


@dataclass(frozen=True)
class Transition:
    observation: Observation
    action: Action
    reward: float
    events: tuple[dict[str, Any], ...]
    hidden_world: dict[str, Any]
    hidden_body: dict[str, float]
    terminated: bool
    stop_reason: str | None = None


@dataclass(frozen=True)
class Probe:
    probe_id: str
    kind: str
    prompt: str
    correct_action: Action | None = None
    expected_source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RunSummary:
    run_id: str
    experiment: str
    condition: str
    seed: int
    steps: int
    terminated: bool
    stop_reason: str | None
    metrics: dict[str, float | int | None]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

