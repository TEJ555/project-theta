from __future__ import annotations

import hashlib
import json
import platform
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .prompts import AGENT_INSTRUCTIONS

SCHEMA_VERSION = 2

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS schema_info(version INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS runs(
  run_id TEXT PRIMARY KEY, created_at TEXT NOT NULL, completed_at TEXT,
  experiment TEXT NOT NULL, condition_name TEXT NOT NULL, seed INTEGER NOT NULL,
  adapter TEXT NOT NULL, model TEXT NOT NULL, temperature REAL NOT NULL,
  config_json TEXT NOT NULL, code_version TEXT, status TEXT NOT NULL,
  stop_reason TEXT, epistemic_notice TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS steps(
  run_id TEXT NOT NULL REFERENCES runs(run_id), tick INTEGER NOT NULL,
  observation_json TEXT NOT NULL, context_json TEXT NOT NULL, decision_json TEXT NOT NULL,
  events_json TEXT NOT NULL, hidden_world_json TEXT NOT NULL, hidden_body_json TEXT NOT NULL,
  reward REAL NOT NULL, provider_id TEXT, PRIMARY KEY(run_id, tick)
);
CREATE TABLE IF NOT EXISTS memories(
  run_id TEXT NOT NULL REFERENCES runs(run_id), tick INTEGER NOT NULL,
  record_json TEXT NOT NULL, PRIMARY KEY(run_id, tick)
);
CREATE TABLE IF NOT EXISTS probes(
  run_id TEXT NOT NULL REFERENCES runs(run_id), tick INTEGER NOT NULL,
  probe_id TEXT NOT NULL, kind TEXT NOT NULL, expected_json TEXT,
  response_json TEXT NOT NULL, PRIMARY KEY(run_id, probe_id)
);
CREATE TABLE IF NOT EXISTS welfare_events(
  run_id TEXT NOT NULL REFERENCES runs(run_id), tick INTEGER NOT NULL,
  reason TEXT NOT NULL, state_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS metrics(
  run_id TEXT NOT NULL REFERENCES runs(run_id), name TEXT NOT NULL,
  value REAL, class TEXT NOT NULL, definition_version INTEGER NOT NULL,
  PRIMARY KEY(run_id, name)
);
CREATE TABLE IF NOT EXISTS run_artifacts(
  run_id TEXT PRIMARY KEY REFERENCES runs(run_id),
  config_sha256 TEXT NOT NULL, prompt_sha256 TEXT NOT NULL,
  code_version TEXT NOT NULL, python_version TEXT NOT NULL, platform TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS api_calls(
  run_id TEXT NOT NULL REFERENCES runs(run_id), tick INTEGER NOT NULL,
  provider_id TEXT, metadata_json TEXT NOT NULL,
  PRIMARY KEY(run_id, tick)
);
CREATE TABLE IF NOT EXISTS worker_state(
  worker_id TEXT PRIMARY KEY, completed_cycles INTEGER NOT NULL,
  last_seed INTEGER, updated_at TEXT NOT NULL
);
"""


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


class RunStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path, timeout=30)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.connection.execute("PRAGMA busy_timeout=30000")
        self.connection.executescript(SCHEMA_SQL)
        count = self.connection.execute("SELECT COUNT(*) FROM schema_info").fetchone()[0]
        if count == 0:
            self.connection.execute("INSERT INTO schema_info(version) VALUES (?)", (SCHEMA_VERSION,))
        else:
            self.connection.execute("UPDATE schema_info SET version=?", (SCHEMA_VERSION,))
        self.connection.commit()

    def start_run(self, run_id: str, config: dict[str, Any], code_version: str = "unknown") -> None:
        self.connection.execute(
            """INSERT INTO runs VALUES (?, ?, NULL, ?, ?, ?, ?, ?, ?, ?, ?, 'running', NULL, ?)""",
            (
                run_id,
                datetime.now(timezone.utc).isoformat(),
                config["experiment"],
                config["condition"],
                config["seed"],
                config["adapter"],
                config["model"],
                config["temperature"],
                _json(config),
                code_version,
                "Behavioural/computational indicators only; no phenomenal inference.",
            ),
        )
        config_json = _json(config)
        self.connection.execute(
            "INSERT INTO run_artifacts VALUES (?, ?, ?, ?, ?, ?)",
            (
                run_id,
                hashlib.sha256(config_json.encode("utf-8")).hexdigest(),
                hashlib.sha256(AGENT_INSTRUCTIONS.encode("utf-8")).hexdigest(),
                code_version,
                sys.version.split()[0],
                platform.platform(),
            ),
        )
        self.connection.commit()

    def log_step(
        self,
        run_id: str,
        tick: int,
        observation: dict[str, Any],
        context: dict[str, Any],
        decision: dict[str, Any],
        events: list[dict[str, Any]],
        hidden_world: dict[str, Any],
        hidden_body: dict[str, Any],
        reward: float,
        provider_id: str | None,
    ) -> None:
        self.connection.execute(
            "INSERT INTO steps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (run_id, tick, _json(observation), _json(context), _json(decision), _json(events),
             _json(hidden_world), _json(hidden_body), reward, provider_id),
        )

    def log_memory(self, run_id: str, tick: int, record: dict[str, Any]) -> None:
        self.connection.execute("INSERT INTO memories VALUES (?, ?, ?)", (run_id, tick, _json(record)))

    def log_api_call(
        self, run_id: str, tick: int, provider_id: str | None, metadata: dict[str, Any]
    ) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO api_calls VALUES (?, ?, ?, ?)",
            (run_id, tick, provider_id, _json(metadata)),
        )

    def checkpoint(self) -> None:
        self.connection.commit()

    def log_probe(self, run_id: str, tick: int, probe: Any, response: dict[str, Any]) -> None:
        self.connection.execute(
            "INSERT INTO probes VALUES (?, ?, ?, ?, ?, ?)",
            (run_id, tick, probe.probe_id, probe.kind,
             _json({"source": probe.expected_source, "action": probe.correct_action}), _json(response)),
        )

    def finish_run(
        self,
        run_id: str,
        metrics: dict[str, float | int | None],
        metric_registry: dict[str, dict[str, str]],
        stop_reason: str | None,
    ) -> None:
        for name, value in metrics.items():
            if name not in metric_registry:
                continue
            self.connection.execute(
                "INSERT OR REPLACE INTO metrics VALUES (?, ?, ?, ?, ?)",
                (run_id, name, value, metric_registry[name]["class"], 1),
            )
        self.connection.execute(
            "UPDATE runs SET completed_at=?, status='completed', stop_reason=? WHERE run_id=?",
            (datetime.now(timezone.utc).isoformat(), stop_reason, run_id),
        )
        self.connection.commit()

    def fail_run(self, run_id: str, reason: str) -> None:
        self.connection.execute(
            "UPDATE runs SET completed_at=?, status='failed', stop_reason=? WHERE run_id=?",
            (datetime.now(timezone.utc).isoformat(), reason[:2000], run_id),
        )
        self.connection.commit()

    def log_welfare(self, run_id: str, tick: int, reason: str, state: dict[str, Any]) -> None:
        self.connection.execute(
            "INSERT INTO welfare_events VALUES (?, ?, ?, ?)", (run_id, tick, reason, _json(state))
        )

    def mark_interrupted_runs(self) -> int:
        cursor = self.connection.execute(
            """UPDATE runs SET completed_at=?, status='failed',
               stop_reason='interrupted_before_completion' WHERE status='running'""",
            (datetime.now(timezone.utc).isoformat(),),
        )
        self.connection.commit()
        return cursor.rowcount

    def worker_state(self, worker_id: str) -> tuple[int, int | None]:
        row = self.connection.execute(
            "SELECT completed_cycles, last_seed FROM worker_state WHERE worker_id=?", (worker_id,)
        ).fetchone()
        return (int(row[0]), row[1]) if row else (0, None)

    def update_worker_state(self, worker_id: str, cycles: int, last_seed: int) -> None:
        self.connection.execute(
            """INSERT INTO worker_state VALUES (?, ?, ?, ?)
               ON CONFLICT(worker_id) DO UPDATE SET completed_cycles=excluded.completed_cycles,
               last_seed=excluded.last_seed, updated_at=excluded.updated_at""",
            (worker_id, cycles, last_seed, datetime.now(timezone.utc).isoformat()),
        )
        self.connection.commit()

    def report(self) -> list[dict[str, Any]]:
        query = """
        SELECT r.run_id, r.experiment, r.condition_name, r.seed, r.adapter, r.status,
               r.stop_reason, m.name, m.value, m.class
        FROM runs r LEFT JOIN metrics m ON r.run_id=m.run_id
        ORDER BY r.created_at, m.name
        """
        rows = self.connection.execute(query).fetchall()
        by_run: dict[str, dict[str, Any]] = {}
        for run_id, experiment, condition, seed, adapter, status, stop, name, value, metric_class in rows:
            entry = by_run.setdefault(run_id, {
                "run_id": run_id, "experiment": experiment, "condition": condition,
                "seed": seed, "adapter": adapter, "status": status, "stop_reason": stop, "metrics": {},
            })
            if name:
                entry["metrics"][name] = {"value": value, "class": metric_class}
        return list(by_run.values())

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> RunStore:  # noqa: PYI034 - Python 3.10 has no typing.Self
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
