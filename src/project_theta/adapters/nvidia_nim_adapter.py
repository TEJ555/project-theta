from __future__ import annotations

import json
import os
from time import monotonic
from typing import Any
from urllib.parse import urlparse

from ..prompts import AGENT_INSTRUCTIONS, DECISION_SCHEMA
from .base import AdapterError, ModelAdapter


class NvidiaNimAdapter(ModelAdapter):
    """Run a named model through NVIDIA's OpenAI-compatible hosted NIM API."""

    name = "nvidia_nim"

    def __init__(
        self,
        model: str,
        temperature: float = 0.0,
        seed: int = 0,
        base_url: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(model, temperature, seed, **kwargs)
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise AdapterError(
                'Install the optional dependency: pip install -e ".[nvidia]"'
            ) from exc

        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            raise AdapterError("NVIDIA_API_KEY is missing.")
        self.base_url = (
            base_url
            or os.getenv("THETA_NVIDIA_BASE_URL")
            or "https://integrate.api.nvidia.com/v1"
        ).rstrip("/")
        self.client = OpenAI(
            api_key=api_key,
            base_url=self.base_url,
            timeout=self.timeout_seconds,
            max_retries=self.max_retries,
        )

    def decide(self, context: dict[str, Any]):
        self.begin_call()
        started = monotonic()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": AGENT_INSTRUCTIONS},
                    {
                        "role": "user",
                        "content": (
                            "Return a decision that exactly matches the supplied JSON schema.\n"
                            + json.dumps(context, sort_keys=True)
                        ),
                    },
                ],
                temperature=self.temperature,
                max_tokens=self.max_output_tokens,
                seed=self.seed,
                stream=False,
                extra_body={"guided_json": DECISION_SCHEMA},
            )
            if not response.choices:
                raise AdapterError("NVIDIA NIM returned no completion choice.")
            content = response.choices[0].message.content
            if not isinstance(content, str) or not content.strip():
                raise AdapterError("NVIDIA NIM returned an empty completion.")

            usage = getattr(response, "usage", None)
            self.last_provider_id = getattr(response, "id", None)
            self.last_metadata = {
                "latency_ms": round((monotonic() - started) * 1000, 3),
                "input_tokens": getattr(usage, "prompt_tokens", None),
                "output_tokens": getattr(usage, "completion_tokens", None),
                "total_tokens": getattr(usage, "total_tokens", None),
                "model": getattr(response, "model", self.model),
                "requested_model": self.model,
                "seed": self.seed,
                "temperature_requested": self.temperature,
                "temperature_applied": self.temperature,
                "structured_output": "guided_json",
                "endpoint_host": urlparse(self.base_url).hostname,
                "billing_route": "nvidia_hosted_nim",
                "provider_reported_cost_usd": None,
            }
            return self.decision_from_mapping(json.loads(content))
        except AdapterError:
            raise
        except Exception as exc:
            raise AdapterError(f"NVIDIA NIM adapter failed: {exc}") from exc
