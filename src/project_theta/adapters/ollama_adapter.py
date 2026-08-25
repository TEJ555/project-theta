from __future__ import annotations

import json
import os
from typing import Any
from urllib import request

from .base import AdapterError, ModelAdapter
from ..prompts import AGENT_INSTRUCTIONS


class OllamaAdapter(ModelAdapter):
    name = "ollama"

    def __init__(self, model: str, temperature: float = 0.0, seed: int = 0, base_url: str | None = None):
        super().__init__(model, temperature, seed)
        self.base_url = (base_url or os.getenv("THETA_OLLAMA_URL", "http://localhost:11434")).rstrip("/")

    def decide(self, context: dict[str, Any]):
        self.call_count += 1
        payload = {
            "model": self.model,
            "system": AGENT_INSTRUCTIONS,
            "prompt": json.dumps(context, sort_keys=True),
            "stream": False,
            "format": "json",
            "options": {"temperature": self.temperature, "seed": self.seed},
        }
        req = request.Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        try:
            with request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
            self.last_provider_id = result.get("created_at")
            return self.decision_from_mapping(json.loads(result["response"]))
        except Exception as exc:
            raise AdapterError(f"Ollama adapter failed: {exc}") from exc
