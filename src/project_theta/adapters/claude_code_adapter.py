from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from time import monotonic
from typing import Any

from ..prompts import AGENT_INSTRUCTIONS, DECISION_SCHEMA
from ..types import Decision
from .base import AdapterError, ModelAdapter

_METERED_ENVIRONMENT_VARIABLES = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
)


def resolve_claude_code_path() -> str | None:
    configured = os.getenv("THETA_CLAUDE_CODE_PATH")
    if configured:
        return configured if Path(configured).is_file() else None
    discovered = shutil.which("claude")
    if discovered:
        return discovered
    if os.name == "nt" and os.getenv("APPDATA"):
        candidate = Path(os.environ["APPDATA"]) / "npm" / "claude.cmd"
        if candidate.is_file():
            return str(candidate)
    return None


def subscription_environment() -> tuple[dict[str, str], list[str]]:
    environment = os.environ.copy()
    removed = [name for name in _METERED_ENVIRONMENT_VARIABLES if environment.pop(name, None)]
    return environment, removed


def claude_code_auth_status(executable: str, timeout_seconds: float = 20.0) -> dict[str, Any]:
    environment, _ = subscription_environment()
    try:
        result = subprocess.run(
            [executable, "auth", "status"],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
            env=environment,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise AdapterError(f"Could not inspect Claude Code authentication: {exc}") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()[:1000]
        raise AdapterError(f"Claude Code authentication check failed: {detail}")
    try:
        status = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AdapterError("Claude Code returned an invalid authentication status.") from exc
    if not isinstance(status, dict):
        raise AdapterError("Claude Code authentication status was not a JSON object.")
    return status


class ClaudeCodeSubscriptionAdapter(ModelAdapter):
    """Use a locally authenticated Claude Code Max subscription without an API key."""

    name = "claude_code"

    def __init__(self, model: str, temperature: float = 0.0, seed: int = 0, **kwargs: Any):
        super().__init__(model, temperature, seed, **kwargs)
        executable = resolve_claude_code_path()
        if not executable:
            raise AdapterError(
                "Claude Code is not installed. Install @anthropic-ai/claude-code and sign in "
                "with a Claude.ai Max account."
            )
        self.executable = executable
        self.environment, self.removed_metered_variables = subscription_environment()
        self.auth_status = claude_code_auth_status(executable, self.timeout_seconds)
        if self.auth_status.get("authMethod") != "claude.ai":
            raise AdapterError(
                "Claude Code is not using Claude.ai subscription authentication. Run "
                "`claude /login` and choose the Claude app subscription."
            )
        if str(self.auth_status.get("subscriptionType", "")).lower() != "max":
            raise AdapterError("Project Theta requires an authenticated Claude Max subscription.")

    @staticmethod
    def _token_usage(payload: dict[str, Any]) -> tuple[int, int]:
        usage = payload.get("usage", {})
        if not isinstance(usage, dict):
            usage = {}
        input_tokens = int(usage.get("input_tokens", 0) or 0)
        output_tokens = int(usage.get("output_tokens", 0) or 0)
        model_usage = payload.get("modelUsage", {})
        if not input_tokens and isinstance(model_usage, dict):
            for item in model_usage.values():
                if isinstance(item, dict):
                    input_tokens += int(item.get("inputTokens", 0) or 0)
                    output_tokens += int(item.get("outputTokens", 0) or 0)
        return input_tokens, output_tokens

    def decide(self, context: dict[str, Any]) -> Decision:
        self.begin_call()
        command = [
            self.executable,
            "-p",
            "--output-format",
            "json",
            "--json-schema",
            json.dumps(DECISION_SCHEMA, separators=(",", ":")),
            "--system-prompt",
            AGENT_INSTRUCTIONS,
            "--model",
            self.model,
            "--effort",
            self.reasoning_effort,
            "--max-turns",
            "1",
            "--tools",
            "",
            "--permission-mode",
            "dontAsk",
            "--safe-mode",
            "--strict-mcp-config",
            "--disable-slash-commands",
            "--no-chrome",
            "--no-session-persistence",
        ]
        started = monotonic()
        try:
            with tempfile.TemporaryDirectory(prefix="theta-subject-") as directory:
                result = subprocess.run(
                    command,
                    input=json.dumps(context, sort_keys=True),
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                    check=False,
                    cwd=directory,
                    env=self.environment,
                )
        except subprocess.TimeoutExpired as exc:
            raise AdapterError(
                f"Claude Code exceeded the {self.timeout_seconds:g}-second timeout."
            ) from exc
        except (OSError, subprocess.SubprocessError) as exc:
            raise AdapterError(f"Claude Code failed to start: {exc}") from exc

        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()[:2000]
            raise AdapterError(f"Claude Code subscription call failed: {detail}")
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise AdapterError("Claude Code returned invalid JSON output.") from exc
        if not isinstance(payload, dict) or payload.get("is_error"):
            raise AdapterError(f"Claude Code returned an unsuccessful result: {payload!r}")

        reported_cost = float(payload.get("total_cost_usd", 0.0) or 0.0)
        if reported_cost > 0.0:
            raise AdapterError(
                "Claude Code reported metered API cost. The run was stopped before another call."
            )
        structured = payload.get("structured_output")
        if not isinstance(structured, dict):
            raw_result = payload.get("result", "")
            try:
                structured = json.loads(raw_result) if isinstance(raw_result, str) else raw_result
            except json.JSONDecodeError as exc:
                raise AdapterError("Claude Code did not return the required decision object.") from exc
        if not isinstance(structured, dict):
            raise AdapterError("Claude Code structured output was not a decision object.")

        input_tokens, output_tokens = self._token_usage(payload)
        model_usage = payload.get("modelUsage", {})
        actual_models = sorted(model_usage) if isinstance(model_usage, dict) else []
        self.last_provider_id = str(payload.get("session_id") or "") or None
        self.last_metadata = {
            "latency_ms": round((monotonic() - started) * 1000, 3),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "model": self.model,
            "actual_models": actual_models,
            "reasoning_effort": self.reasoning_effort,
            "temperature_requested": self.temperature,
            "temperature_applied": None,
            "subscription_type": "max",
            "auth_method": "claude.ai",
            "api_key_environment_removed": bool(self.removed_metered_variables),
            "tools_enabled": False,
            "session_persistence": False,
            "reported_cli_cost_usd": reported_cost,
            "estimated_cost_usd": 0.0,
            "estimated_run_cost_usd": 0.0,
            "num_turns": int(payload.get("num_turns", 0) or 0),
        }
        return self.decision_from_mapping(structured)
