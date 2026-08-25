from __future__ import annotations

import json
from time import monotonic
from typing import Any

from ..prompts import AGENT_INSTRUCTIONS, DECISION_SCHEMA
from .base import AdapterError, ModelAdapter


class OpenAIAdapter(ModelAdapter):
    name = "openai"

    def __init__(self, model: str, temperature: float = 0.0, seed: int = 0, **kwargs: Any):
        super().__init__(model, temperature, seed, **kwargs)
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise AdapterError('Install the optional dependency: pip install -e ".[openai]"') from exc
        self.client = OpenAI(timeout=self.timeout_seconds, max_retries=self.max_retries)
        if not hasattr(self.client, "responses"):
            raise AdapterError("Installed OpenAI SDK does not expose the Responses API; upgrade openai.")

    def decide(self, context: dict[str, Any]):
        self.begin_call()
        started = monotonic()
        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=AGENT_INSTRUCTIONS,
                input=json.dumps(context, sort_keys=True),
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
                reasoning={"effort": self.reasoning_effort},
                store=False,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "theta_decision",
                        "strict": True,
                        "schema": DECISION_SCHEMA,
                    }
                },
            )
            self.last_provider_id = response.id
            usage = getattr(response, "usage", None)
            self.last_metadata = {
                "latency_ms": round((monotonic() - started) * 1000, 3),
                "input_tokens": getattr(usage, "input_tokens", None),
                "output_tokens": getattr(usage, "output_tokens", None),
                "total_tokens": getattr(usage, "total_tokens", None),
                "model": getattr(response, "model", self.model),
                "reasoning_effort": self.reasoning_effort,
            }
            return self.decision_from_mapping(json.loads(response.output_text))
        except Exception as exc:  # provider errors are recorded by the harness
            raise AdapterError(f"OpenAI adapter failed: {exc}") from exc
