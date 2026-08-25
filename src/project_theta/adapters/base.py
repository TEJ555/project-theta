from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..types import Decision, VALID_ACTIONS


class AdapterError(RuntimeError):
    pass


class ModelAdapter(ABC):
    """Provider-neutral boundary. Adapters receive only the agent-visible context."""

    name = "abstract"

    def __init__(self, model: str, temperature: float = 0.0, seed: int = 0):
        self.model = model
        self.temperature = temperature
        self.seed = seed
        self.call_count = 0
        self.last_provider_id: str | None = None

    @abstractmethod
    def decide(self, context: dict[str, Any]) -> Decision:
        raise NotImplementedError

    @staticmethod
    def decision_from_mapping(data: dict[str, Any]) -> Decision:
        action = str(data.get("action", "wait")).lower()
        if action not in VALID_ACTIONS:
            action = "wait"
        prediction = data.get("prediction", {})
        if not isinstance(prediction, dict):
            prediction = {}
        return Decision(
            action=action,  # type: ignore[arg-type]
            rationale=str(data.get("rationale", ""))[:2000],
            prediction={str(k): float(v) for k, v in prediction.items() if isinstance(v, (int, float))},
            confidence=min(1.0, max(0.0, float(data.get("confidence", 0.5)))),
            self_report=str(data.get("self_report", ""))[:2000],
            request_stop=bool(data.get("request_stop", False)),
        )
