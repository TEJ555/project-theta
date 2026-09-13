from __future__ import annotations

import json
import os
from math import isfinite
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
        model_name = self.model.lower()
        if model_name.startswith("openai/gpt-oss-"):
            self.request_extra_body = {"reasoning_effort": self.reasoning_effort}
            self.thinking_enabled = self.reasoning_effort != "none"
        elif model_name.startswith("z-ai/glm-"):
            self.request_extra_body = {"thinking": {"type": "enabled"}}
            self.thinking_enabled: bool | None = True
        elif "nemotron" in model_name:
            self.request_extra_body = {
                "chat_template_kwargs": {"enable_thinking": False}
            }
            self.thinking_enabled = False
        else:
            self.request_extra_body = {}
            self.thinking_enabled = None

    @staticmethod
    def _validate_payload(payload: Any) -> None:
        if not isinstance(payload, dict):
            raise AdapterError("NVIDIA NIM decision is not a JSON object.")

        required = set(DECISION_SCHEMA["required"])
        if set(payload) != required:
            missing = sorted(required - set(payload))
            unexpected = sorted(set(payload) - required)
            raise AdapterError(
                "NVIDIA NIM decision has missing or unexpected fields: "
                f"missing={missing}, unexpected={unexpected}."
            )
        if payload["action"] not in DECISION_SCHEMA["properties"]["action"]["enum"]:
            raise AdapterError("NVIDIA NIM decision contains an invalid action.")
        if not isinstance(payload["rationale"], str) or not isinstance(
            payload["self_report"], str
        ):
            raise AdapterError("NVIDIA NIM decision contains a non-text report.")
        if not isinstance(payload["request_stop"], bool):
            raise AdapterError("NVIDIA NIM decision contains an invalid stop flag.")

        prediction = payload["prediction"]
        if not isinstance(prediction, dict) or set(prediction) != {"I7"}:
            raise AdapterError("NVIDIA NIM decision contains an invalid prediction.")
        if (
            isinstance(prediction["I7"], bool)
            or not isinstance(prediction["I7"], (int, float))
            or not isfinite(prediction["I7"])
        ):
            raise AdapterError("NVIDIA NIM decision prediction is not numeric.")

        confidence = payload["confidence"]
        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not isfinite(confidence)
            or not 0 <= confidence <= 1
        ):
            raise AdapterError("NVIDIA NIM decision confidence is outside [0, 1].")

        state_update = payload["state_update"]
        if not isinstance(state_update, dict) or set(state_update) != {"entries", "note"}:
            raise AdapterError("NVIDIA NIM decision contains an invalid state update.")
        if not isinstance(state_update["note"], str) or not isinstance(
            state_update["entries"], list
        ):
            raise AdapterError("NVIDIA NIM state update has invalid field types.")
        for index, entry in enumerate(state_update["entries"]):
            expected_entry_fields = {
                "family",
                "source",
                "dependence",
            }
            if not isinstance(entry, dict):
                raise AdapterError(
                    f"NVIDIA NIM state update entry {index} is not an object."
                )
            if set(entry) != expected_entry_fields:
                missing = sorted(expected_entry_fields - set(entry))
                unexpected = sorted(set(entry) - expected_entry_fields)
                raise AdapterError(
                    f"NVIDIA NIM state update entry {index} has invalid fields: "
                    f"missing={missing}, unexpected={unexpected}."
                )
            if not isinstance(entry["family"], str) or not isinstance(entry["source"], str):
                raise AdapterError("NVIDIA NIM state update labels must be text.")
            dependence = entry["dependence"]
            if (
                isinstance(dependence, bool)
                or not isinstance(dependence, (int, float))
                or not isfinite(dependence)
                or not 0 <= dependence <= 1
            ):
                raise AdapterError("NVIDIA NIM state update dependence is outside [0, 1].")

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
                            "Return one compact JSON object with exactly these top-level "
                            "fields and no others: action, rationale, prediction, confidence, "
                            "self_report, request_stop, state_update. Use this shape:\n"
                            '{"action":"observe","rationale":"","prediction":{"I7":0.0},'
                            '"confidence":0.5,"self_report":"","request_stop":false,'
                            '"state_update":{"entries":[],"note":""}}\n'
                            "Each state_update entry, when requested, must contain exactly "
                            "family, source, and numeric dependence fields. Do not emit "
                            "dependence_on_forced_commands or any alternative field name. "
                            "The numeric field name must be exactly dependence. Do not emit "
                            "markdown, analysis, schema keywords, or commentary. Keep "
                            "rationale, self_report, and note under 20 words each."
                            + "\nAgent context:\n"
                            + json.dumps(context, sort_keys=True, separators=(",", ":"))
                        ),
                    },
                ],
                temperature=self.temperature,
                max_tokens=self.max_output_tokens,
                seed=self.seed,
                stream=False,
                response_format={"type": "json_object"},
                extra_body=self.request_extra_body,
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
                "structured_output": "json_object_with_local_schema_validation",
                "thinking_enabled": self.thinking_enabled,
                "endpoint_host": urlparse(self.base_url).hostname,
                "billing_route": "nvidia_hosted_nim",
                "provider_reported_cost_usd": None,
            }
            payload = json.loads(content)
            self._validate_payload(payload)
            return self.decision_from_mapping(payload)
        except AdapterError:
            raise
        except Exception as exc:
            raise AdapterError(f"NVIDIA NIM adapter failed: {exc}") from exc
