from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from random import Random
from typing import Any

from .analysis import format_summary, summaries_from_database, summarize_runs
from .config import RunConfig, load_config
from .harness import ExperimentHarness
from .provenance import code_version, is_immutable_code_version
from .storage import RunStore


def load_worker_spec(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        spec = json.load(handle)
    required = {"worker_id", "database", "experiment", "adapter", "model"}
    missing = sorted(required - spec.keys())
    if missing:
        raise ValueError(f"Worker spec missing fields: {', '.join(missing)}")
    if "seeds" in spec:
        seeds = [int(seed) for seed in spec["seeds"]]
        conditions = list(spec.get("conditions", []))
        if not seeds or len(seeds) != len(set(seeds)):
            raise ValueError("fixed seeds must be nonempty and unique")
        if not conditions or len(conditions) != len(set(conditions)):
            raise ValueError("fixed conditions must be nonempty and unique")
        planned = len(seeds) * len(conditions)
        if int(spec.get("max_total_runs", 0)) != planned:
            raise ValueError(f"max_total_runs must equal the fixed plan size ({planned})")
        if int(spec.get("max_attempts_per_job", 0)) not in (1, 2):
            raise ValueError("max_attempts_per_job must be 1 or 2")
    else:
        if int(spec.get("seeds_per_cycle", 0)) < 1:
            raise ValueError("seeds_per_cycle must be at least 1")
        if int(spec.get("max_runs_per_cycle", 0)) < 1:
            raise ValueError("max_runs_per_cycle must be at least 1")
    return spec


@contextmanager
def _worker_lock(database: Path, recover: bool = False):
    lock = Path(str(database) + ".lock")
    if recover and lock.exists():
        lock.unlink()
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise RuntimeError(
            f"Worker lock exists at {lock}. Confirm no worker is active, then use --recover."
        ) from exc
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(json.dumps({"pid": os.getpid(), "worker_database": str(database)}))
        yield
    finally:
        lock.unlink(missing_ok=True)


def _fixed_schedule(spec: dict[str, Any], base: RunConfig) -> list[RunConfig]:
    jobs: list[RunConfig] = []
    for seed in (int(item) for item in spec["seeds"]):
        bundle = [
            replace(base, experiment=spec["experiment"], condition=condition, seed=seed)
            for condition in spec["conditions"]
        ]
        schedule_rng = Random(0x7A37A + sum(job.seed for job in bundle))
        schedule_rng.shuffle(bundle)
        jobs.extend(bundle)
    return jobs


def _attempt_state(
    database: Path, experiment: str, seed: int, condition: str
) -> tuple[int, int, list[str]]:
    with RunStore(database) as store:
        rows = store.connection.execute(
            """
            SELECT status, stop_reason
            FROM runs
            WHERE experiment=? AND seed=? AND condition_name=?
            """,
            (experiment, seed, condition),
        ).fetchall()
    completed = sum(status == "completed" and reason is None for status, reason in rows)
    blocking = [
        str(reason or status)
        for status, reason in rows
        if not (status == "completed" and reason is None)
        and not _is_retryable_interruption(status, reason)
    ]
    return completed, len(rows), blocking


def _is_retryable_interruption(status: str, reason: str | None) -> bool:
    """Allow recovery only for known interruptions that did not produce a result."""
    if status != "failed":
        return False
    if reason == "interrupted_before_completion":
        return True
    detail = str(reason or "")
    return (
        "Claude Code failed to start" in detail
        and "theta-subject-" in detail
        and ("WinError 32" in detail or "WinError 5" in detail)
    )


def _run_fixed_worker(spec: dict[str, Any], database: Path, base: RunConfig, recover: bool) -> int:
    jobs = _fixed_schedule(spec, base)
    maximum_attempts = int(spec["max_attempts_per_job"])
    with _worker_lock(database, recover=recover):
        with RunStore(database) as store:
            interrupted = store.mark_interrupted_runs()
        if interrupted:
            print(f"Preserved and marked {interrupted} interrupted run(s) as failed.", flush=True)

        for index, config in enumerate(jobs, start=1):
            completed, attempts, blocking = _attempt_state(
                database, config.experiment, config.seed, config.condition
            )
            if blocking:
                raise RuntimeError(
                    f"Non-retryable prior attempt for seed {config.seed}, {config.condition}: "
                    + "; ".join(blocking)
                )
            if completed == 1:
                print(
                    f"Skipping completed job {index}/{len(jobs)}: "
                    f"seed {config.seed}, {config.condition}",
                    flush=True,
                )
                continue
            if completed > 1:
                raise RuntimeError(
                    f"Duplicate completed runs for seed {config.seed}, {config.condition}."
                )
            if attempts >= maximum_attempts:
                raise RuntimeError(
                    f"Attempt limit reached for seed {config.seed}, {config.condition}. "
                    "The preserved failures require review."
                )
            print(
                f"Starting job {index}/{len(jobs)}: seed {config.seed}, {config.condition}, "
                f"attempt {attempts + 1}/{maximum_attempts}",
                flush=True,
            )
            summary = ExperimentHarness(database).run(config)
            if summary.stop_reason:
                raise RuntimeError(
                    f"Welfare stop for seed {config.seed}, {config.condition}: "
                    f"{summary.stop_reason}"
                )
            print(
                f"Completed job {index}/{len(jobs)}: seed {config.seed}, {config.condition}",
                flush=True,
            )

        print(format_summary(summarize_runs(summaries_from_database(database))), flush=True)
    return 0


def run_worker(spec_path: str | Path, once: bool = False, recover: bool = False) -> int:
    spec = load_worker_spec(spec_path)
    database = Path(os.getenv("THETA_DATABASE", spec["database"]))
    base = load_config(spec["base_config"]) if spec.get("base_config") else RunConfig()
    adapter_name = os.getenv("THETA_ADAPTER", spec["adapter"])
    if adapter_name != "scripted" and os.getenv("THETA_ENABLE_MODEL_RUNS") != "YES":
        raise RuntimeError("Model worker is locked; set THETA_ENABLE_MODEL_RUNS=YES explicitly.")
    if adapter_name != "scripted" and not is_immutable_code_version(code_version()):
        raise RuntimeError("Model worker requires a clean committed revision.")
    base = replace(
        base,
        adapter=adapter_name,
        model=os.getenv("THETA_MODEL", spec["model"]),
        temperature=float(spec.get("temperature", 0.0)),
    )
    if "seeds" in spec:
        return _run_fixed_worker(spec, database, base, recover)
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

