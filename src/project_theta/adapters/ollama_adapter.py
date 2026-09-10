from __future__ import annotations

import json
import os
from time import monotonic
from typing import Any
from urllib import request

from ..prompts import AGENT_INSTRUCTIONS, DECISION_SCHEMA
from .base import AdapterError, ModelAdapter


class OllamaAdapter(ModelAdapter):
    name = "ollama"

    def __init__(self, model: str, temperature: float = 0.0, seed: int = 0, base_url: str | None = None, **kwargs: Any):
        super().__init__(model, temperature, seed, **kwargs)
        self.base_url = (base_url or os.getenv("THETA_OLLAMA_URL", "http://localhost:11434")).rstrip("/")
        self.model_digest, self.model_details = self._resolve_model_identity()

    def _resolve_model_identity(self) -> tuple[str, dict[str, Any]]:
        req = request.Request(f"{self.base_url}/api/tags")
        try:
            with request.urlopen(req, timeout=min(self.timeout_seconds, 10.0)) as response:
                result = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise AdapterError(f"Ollama model inventory failed: {exc}") from exc
        for item in result.get("models", []):
            if item.get("name") == self.model or item.get("model") == self.model:
                digest = item.get("digest")
                if not isinstance(digest, str) or not digest:
                    raise AdapterError(f"Ollama did not report a digest for {self.model!r}.")
                details = item.get("details")
                return digest, details if isinstance(details, dict) else {}
        raise AdapterError(
            f"Ollama model {self.model!r} is not installed. Run: ollama pull {self.model}"
        )

    def decide(self, context: dict[str, Any]):
        self.begin_call()
        started = monotonic()
        payload = {
            "model": self.model,
            "system": AGENT_INSTRUCTIONS,
            "prompt": json.dumps(context, sort_keys=True),
            "stream": False,
            "format": DECISION_SCHEMA,
            "think": False,
            "options": {
                "temperature": self.temperature,
                "seed": self.seed,
                "num_predict": self.max_output_tokens,
            },
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
                "requested_model": self.model,
                "model_digest": self.model_digest,
                "model_details": self.model_details,
                "seed": self.seed,
                "temperature_requested": self.temperature,
                "temperature_applied": self.temperature,
                "structured_output": "json_schema",
                "endpoint_host": "localhost",
                "billing_route": "local_ollama",
                "provider_reported_cost_usd": 0.0,
            }
            return self.decision_from_mapping(json.loads(result["response"]))
        except Exception as exc:
            raise AdapterError(f"Ollama adapter failed: {exc}") from exc
