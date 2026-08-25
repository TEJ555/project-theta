from __future__ import annotations

import json
from typing import Any

from .base import AdapterError, ModelAdapter
from ..prompts import AGENT_INSTRUCTIONS, DECISION_SCHEMA


class OpenAIAdapter(ModelAdapter):
    name = "openai"

    def __init__(self, model: str, temperature: float = 0.0, seed: int = 0):
        super().__init__(model, temperature, seed)
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise AdapterError('Install the optional dependency: pip install -e ".[openai]"') from exc
        self.client = OpenAI()

    def decide(self, context: dict[str, Any]):
        self.call_count += 1
        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=AGENT_INSTRUCTIONS,
                input=json.dumps(context, sort_keys=True),
                temperature=self.temperature,
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
            return self.decision_from_mapping(json.loads(response.output_text))
        except Exception as exc:  # provider errors are recorded by the harness
            raise AdapterError(f"OpenAI adapter failed: {exc}") from exc
