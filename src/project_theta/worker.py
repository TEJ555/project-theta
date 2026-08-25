from __future__ import annotations

import json
import os
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

from .analysis import format_summary, summarize_runs
from .config import RunConfig, load_config
from .harness import ExperimentHarness
from .storage import RunStore


def load_worker_spec(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        spec = json.load(handle)
    required = {"worker_id", "database", "experiment", "adapter", "model"}
    missing = sorted(required - spec.keys())
    if missing:
        raise ValueError(f"Worker spec missing fields: {', '.join(missing)}")
    if int(spec.get("seeds_per_cycle", 0)) < 1:
        raise ValueError("seeds_per_cycle must be at least 1")
    if int(spec.get("max_runs_per_cycle", 0)) < 1:
        raise ValueError("max_runs_per_cycle must be at least 1")
    return spec


def run_worker(spec_path: str | Path, once: bool = False) -> int:
    spec = load_worker_spec(spec_path)
    database = Path(os.getenv("THETA_DATABASE", spec["database"]))
    base = load_config(spec["base_config"]) if spec.get("base_config") else RunConfig()
    adapter_name = os.getenv("THETA_ADAPTER", spec["adapter"])
    if adapter_name != "scripted" and os.getenv("THETA_ENABLE_MODEL_RUNS") != "YES":
        raise RuntimeError("Model worker is locked; set THETA_ENABLE_MODEL_RUNS=YES explicitly.")
    base = replace(
        base,
        adapter=adapter_name,
        model=os.getenv("THETA_MODEL", spec["model"]),
        temperature=float(spec.get("temperature", 0.0)),
    )
    with RunStore(database) as store:
        completed_cycles, _ = store.worker_state(spec["worker_id"])
        store.mark_interrupted_runs()

    while True:
        start = int(spec.get("start_seed", 1000)) + completed_cycles * int(spec["seeds_per_cycle"])
        seeds = list(range(start, start + int(spec["seeds_per_cycle"])))
        conditions = spec.get("conditions")
        summaries = ExperimentHarness(database).run_study(
            spec["experiment"],
            seeds,
            base,
            conditions=conditions,
            max_runs=int(spec["max_runs_per_cycle"]),
        )
        print(format_summary(summarize_runs(summaries)), flush=True)
        completed_cycles += 1
        with RunStore(database) as store:
            store.update_worker_state(spec["worker_id"], completed_cycles, seeds[-1])
        if once:
            return 0
        time.sleep(max(1.0, float(spec.get("interval_seconds", 300))))
