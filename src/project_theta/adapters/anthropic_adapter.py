from __future__ import annotations

import json
from time import monotonic
from typing import Any

from ..prompts import AGENT_INSTRUCTIONS, DECISION_SCHEMA
from .base import AdapterError, ModelAdapter

# Standard first-party Claude API rates, USD per million tokens. Unknown models are
# rejected while the cost guard is enabled so an unpriced model cannot bypass it.
_PRICES: dict[str, tuple[float, float, float, float]] = {
    # regular input, output, five-minute cache write, cache read
    "claude-sonnet-4-6": (3.0, 15.0, 3.75, 0.30),
    "claude-haiku-4-5": (1.0, 5.0, 1.25, 0.10),
    "claude-haiku-4-5-20251001": (1.0, 5.0, 1.25, 0.10),
}


class AnthropicAdapter(ModelAdapter):
    name = "anthropic"

    def __init__(self, model: str, temperature: float = 0.0, seed: int = 0, **kwargs: Any):
        super().__init__(model, temperature, seed, **kwargs)
        if model not in _PRICES:
            raise AdapterError(
                f"No frozen Project Theta price entry for Anthropic model {model!r}; "
                "add and test a current official rate before running it."
            )
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise AdapterError('Install the optional dependency: pip install -e ".[anthropic]"') from exc
        self.client = Anthropic(timeout=self.timeout_seconds, max_retries=self.max_retries)

    def decide(self, context: dict[str, Any]):
        self.begin_call()
        started = monotonic()
        try:
            response = self.client.messages.create(
                model=self.model,
                system=AGENT_INSTRUCTIONS,
                messages=[{"role": "user", "content": json.dumps(context, sort_keys=True)}],
                max_tokens=self.max_output_tokens,
                output_config={
                    "effort": self.reasoning_effort,
                    "format": {"type": "json_schema", "schema": DECISION_SCHEMA},
                },
            )
            self.last_provider_id = response.id
            usage = response.usage
            input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
            cache_creation = int(getattr(usage, "cache_creation_input_tokens", 0) or 0)
            cache_read = int(getattr(usage, "cache_read_input_tokens", 0) or 0)
            output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
            priced_input = input_tokens + cache_creation + cache_read
            input_rate, output_rate, cache_write_rate, cache_read_rate = _PRICES[self.model]
            call_cost = (
                input_tokens * input_rate
                + cache_creation * cache_write_rate
                + cache_read * cache_read_rate
                + output_tokens * output_rate
            ) / 1_000_000
            self.estimated_cost_usd += call_cost
            self.last_metadata = {
                "latency_ms": round((monotonic() - started) * 1000, 3),
                "input_tokens": input_tokens,
                "cache_creation_input_tokens": cache_creation,
                "cache_read_input_tokens": cache_read,
                "output_tokens": output_tokens,
                "total_tokens": priced_input + output_tokens,
                "model": response.model,
                "reasoning_effort": self.reasoning_effort,
                # Anthropic SDK 1.x no longer exposes a temperature parameter on
                # Messages.create. Keep the requested value in provenance while
                # accurately recording that the provider default was used.
                "temperature_requested": self.temperature,
                "temperature_applied": None,
                "estimated_cost_usd": round(call_cost, 8),
                "estimated_run_cost_usd": round(self.estimated_cost_usd, 8),
            }
            text = "".join(
                str(getattr(block, "text", "")) for block in response.content
                if getattr(block, "type", None) == "text"
            )
            return self.decision_from_mapping(json.loads(text))
        except AdapterError:
            raise
        except Exception as exc:
            raise AdapterError(f"Anthropic adapter failed: {exc}") from exc
