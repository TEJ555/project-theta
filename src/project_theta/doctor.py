from __future__ import annotations

import importlib.util
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any

from .adapters.base import AdapterError
from .adapters.claude_code_adapter import (
    claude_code_auth_status,
    claude_code_version,
    resolve_claude_code_path,
    subscription_environment,
)
from .config import RunConfig
from .experiments import STUDY_PROTOCOLS
from .provenance import code_version, is_immutable_code_version
from .storage import SCHEMA_VERSION, RunStore
from .trials import build_trials


def run_doctor(adapter: str = "scripted", database: str | Path = "runs/doctor.sqlite") -> dict[str, Any]:
    checks: list[dict[str, str]] = []

    def add(name: str, status: str, detail: str) -> None:
        checks.append({"name": name, "status": status, "detail": detail})

    add(
        "python",
        "pass" if sys.version_info >= (3, 10) else "fail",
        f"Python {sys.version.split()[0]} (requires >=3.10)",
    )
    revision = code_version()
    immutable_revision = is_immutable_code_version(revision)
    add(
        "code_version",
        "pass" if immutable_revision else "fail" if adapter != "scripted" else "warn",
        revision if immutable_revision else f"{revision} (set THETA_CODE_VERSION for deployment)",
    )
    schedules_ok = True
    max_trials = 0
    for experiment in STUDY_PROTOCOLS:
        trials = build_trials(experiment, 101)
        max_trials = max(max_trials, len(trials))
        probes = [trial for trial in trials if trial.correct_action]
        left = sum(trial.correct_action == "choose_left" for trial in probes)
        schedules_ok &= len(probes) >= 8 and left * 2 == len(probes)
        schedules_ok &= all("correct_action" not in trial.public_task() for trial in probes)
    add(
        "trial_schedules",
        "pass" if schedules_ok else "fail",
        f"{len(STUDY_PROTOCOLS)} protocols; balanced, blinded; max {max_trials} calls/run",
    )
    config = RunConfig()
    add(
        "call_budget",
        "pass" if config.execution.max_model_calls >= max_trials else "fail",
        f"limit {config.execution.max_model_calls}; required at least {max_trials}",
    )
    supported_efforts = {"none", "low", "medium", "high", "xhigh", "max"}
    add(
        "reasoning_effort",
        "pass" if config.execution.reasoning_effort in supported_efforts else "fail",
        config.execution.reasoning_effort,
    )
    add(
        "cost_guard",
        "pass" if config.execution.max_estimated_cost_usd > 0 else "fail",
        f"${config.execution.max_estimated_cost_usd:.2f} estimated maximum per run",
    )
    add("welfare", "pass" if config.welfare.enabled else "fail", "online stop monitor enabled")

    try:
        with RunStore(database) as store:
            version = store.connection.execute("SELECT version FROM schema_info").fetchone()[0]
        add("database", "pass" if version == SCHEMA_VERSION else "fail", f"SQLite schema {version}")
    except (OSError, sqlite3.Error) as exc:
        add("database", "fail", f"{type(exc).__name__}: {exc}")

    if adapter == "openai":
        add(
            "openai_sdk",
            "pass" if importlib.util.find_spec("openai") else "fail",
            "OpenAI Python SDK installed" if importlib.util.find_spec("openai") else "install .[openai]",
        )
        add(
            "api_key",
            "pass" if os.getenv("OPENAI_API_KEY") else "fail",
            "OPENAI_API_KEY is set" if os.getenv("OPENAI_API_KEY") else "OPENAI_API_KEY is missing",
        )
    if adapter == "anthropic":
        anthropic_installed = bool(importlib.util.find_spec("anthropic"))
        add(
            "anthropic_sdk",
            "pass" if anthropic_installed else "fail",
            "Anthropic Python SDK installed"
            if anthropic_installed else "install .[anthropic]",
        )
        if anthropic_installed:
            try:
                from anthropic import transform_schema

                from .prompts import DECISION_SCHEMA

                transformed = transform_schema(DECISION_SCHEMA)

                def unsupported_keys(value: Any) -> set[str]:
                    if isinstance(value, dict):
                        own = {key for key in value if key in {"minimum", "maximum"}}
                        return own | set().union(
                            *(unsupported_keys(item) for item in value.values()), set()
                        )
                    if isinstance(value, list):
                        return set().union(*(unsupported_keys(item) for item in value), set())
                    return set()

                unsupported = unsupported_keys(transformed)
                add(
                    "anthropic_schema",
                    "fail" if unsupported else "pass",
                    "provider-compatible structured-output schema"
                    if not unsupported else f"unsupported constraints: {sorted(unsupported)}",
                )
            except (ImportError, TypeError, ValueError) as exc:
                add("anthropic_schema", "fail", f"{type(exc).__name__}: {exc}")
        add(
            "api_key",
            "pass" if os.getenv("ANTHROPIC_API_KEY") else "fail",
            "ANTHROPIC_API_KEY is set"
            if os.getenv("ANTHROPIC_API_KEY") else "ANTHROPIC_API_KEY is missing",
        )
    if adapter == "claude_code":
        executable = resolve_claude_code_path()
        add(
            "claude_code_cli",
            "pass" if executable else "fail",
            executable or "install @anthropic-ai/claude-code",
        )
        if executable:
            try:
                version = claude_code_version(executable)
                add("claude_code_version", "pass", version)
                status = claude_code_auth_status(executable)
                subscription_ok = (
                    status.get("authMethod") == "claude.ai"
                    and str(status.get("subscriptionType", "")).lower() == "max"
                )
                add(
                    "claude_max_subscription",
                    "pass" if subscription_ok else "fail",
                    (
                        "Claude.ai Max subscription authenticated"
                        if subscription_ok
                        else (
                            f"authMethod={status.get('authMethod')}, "
                            f"subscriptionType={status.get('subscriptionType')}"
                        )
                    ),
                )
            except AdapterError as exc:
                add("claude_max_subscription", "fail", str(exc))
        _, removed = subscription_environment()
        add(
            "subscription_isolation",
            "pass",
            (
                "metered provider variables will be removed from child calls"
                + (f": {', '.join(sorted(removed))}" if removed else "")
            ),
        )
    if adapter != "scripted":
        add(
            "model_run_gate",
            "pass" if os.getenv("THETA_ENABLE_MODEL_RUNS") == "YES" else "fail",
            "explicit gate enabled" if os.getenv("THETA_ENABLE_MODEL_RUNS") == "YES" else "set THETA_ENABLE_MODEL_RUNS=YES",
        )

    return {
        "status": "fail" if any(check["status"] == "fail" for check in checks) else "pass",
        "checks": checks,
    }


def format_doctor(result: dict[str, Any]) -> str:
    lines = ["Project Theta preflight", ""]
    for check in result["checks"]:
        lines.append(f"[{check['status'].upper():4}] {check['name']}: {check['detail']}")
    lines.extend(["", f"Overall: {result['status'].upper()}"])
    return "\n".join(lines)
