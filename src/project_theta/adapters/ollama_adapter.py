from __future__ import annotations

import json
import os
from time import monotonic
from typing import Any
from urllib import request

from ..prompts import AGENT_INSTRUCTIONS
from .base import AdapterError, ModelAdapter


class OllamaAdapter(ModelAdapter):
    name = "ollama"

    def __init__(self, model: str, temperature: float = 0.0, seed: int = 0, base_url: str | None = None, **kwargs: Any):
        super().__init__(model, temperature, seed, **kwargs)
        self.base_url = (base_url or os.getenv("THETA_OLLAMA_URL", "http://localhost:11434")).rstrip("/")

    def decide(self, context: dict[str, Any]):
        self.begin_call()
        started = monotonic()
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
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                result = json.loads(response.read().decode("utf-8"))
            self.last_provider_id = result.get("created_at")
            self.last_metadata = {
                "latency_ms": round((monotonic() - started) * 1000, 3),
                "input_tokens": result.get("prompt_eval_count"),
                "output_tokens": result.get("eval_count"),
                "total_duration_ns": result.get("total_duration"),
                "model": result.get("model", self.model),
            }
            return self.decision_from_mapping(json.loads(result["response"]))
        except Exception as exc:
            raise AdapterError(f"Ollama adapter failed: {exc}") from exc
