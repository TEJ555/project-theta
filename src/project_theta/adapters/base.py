from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..types import VALID_ACTIONS, Decision


class AdapterError(RuntimeError):
    pass


class ModelAdapter(ABC):
    """Provider-neutral boundary. Adapters receive only the agent-visible context."""

    name = "abstract"

    def __init__(
        self,
        model: str,
        temperature: float = 0.0,
        seed: int = 0,
        timeout_seconds: float = 120.0,
        max_retries: int = 2,
        max_output_tokens: int = 1000,
        max_calls: int = 50,
        reasoning_effort: str = "low",
        max_estimated_cost_usd: float = 1.25,
    ):
        self.model = model
        self.temperature = temperature
        self.seed = seed
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.max_output_tokens = max_output_tokens
        self.max_calls = max_calls
        self.reasoning_effort = reasoning_effort
        self.max_estimated_cost_usd = max_estimated_cost_usd
        self.estimated_cost_usd = 0.0
        self.call_count = 0
        self.last_provider_id: str | None = None
        self.last_metadata: dict[str, Any] = {}

    def begin_call(self) -> None:
        if self.call_count >= self.max_calls:
            raise AdapterError(f"Per-run model call budget exhausted ({self.max_calls}).")
        if self.estimated_cost_usd >= self.max_estimated_cost_usd:
            raise AdapterError(
                "Per-run estimated provider cost budget exhausted "
                f"(${self.max_estimated_cost_usd:.2f})."
            )
        self.call_count += 1

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
