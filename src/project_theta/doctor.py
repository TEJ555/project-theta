from __future__ import annotations

import importlib.util
import os
import re
import sys
from pathlib import Path
from typing import Any

from .config import RunConfig
from .experiments import STUDY_PROTOCOLS
from .provenance import code_version
from .storage import RunStore, SCHEMA_VERSION
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
    immutable_revision = bool(re.fullmatch(r"[0-9a-fA-F]{40}", revision)) or bool(
        os.getenv("THETA_CODE_VERSION")
    )
    add(
        "code_version",
        "pass" if immutable_revision else "warn",
        revision if immutable_revision else f"{revision} (set THETA_CODE_VERSION for deployment)",
    )
    schedules_ok = True
    max_trials = 0
    for experiment in STUDY_PROTOCOLS:
        trials = build_trials(experiment, 101)
        max_trials = max(max_trials, len(trials))
        probes = [trial for trial in trials if trial.correct_action]
        left = sum(trial.correct_action == "choose_left" for trial in probes)
        schedules_ok &= len(probes) == 12 and left == 6
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
    add("welfare", "pass" if config.welfare.enabled else "fail", "online stop monitor enabled")

    try:
        with RunStore(database) as store:
            version = store.connection.execute("SELECT version FROM schema_info").fetchone()[0]
        add("database", "pass" if version == SCHEMA_VERSION else "fail", f"SQLite schema {version}")
    except Exception as exc:
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
