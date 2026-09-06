from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pseudonym(database: Path, run_id: str) -> str:
    value = f"{database.name}|{run_id}".encode()
    return "run-" + hashlib.sha256(value).hexdigest()[:16]


def parse_json(value: str | None) -> Any:
    return json.loads(value) if value else None


def export_database(database: Path, destination: Path) -> dict[str, Any]:
    wal = Path(str(database) + "-wal")
    if wal.exists():
        raise RuntimeError(f"Refusing active or uncheckpointed database with WAL file: {database}")
    connection = sqlite3.connect(str(database.resolve()))
    running = connection.execute(
        "SELECT COUNT(*) FROM runs WHERE status='running'"
    ).fetchone()[0]
    if running:
        connection.close()
        raise RuntimeError(f"Refusing database with {running} running row(s): {database}")

    run_rows = connection.execute(
        """
        SELECT run_id, created_at, completed_at, experiment, condition_name, seed,
               adapter, model, temperature, config_json, code_version, status,
               stop_reason, epistemic_notice
        FROM runs ORDER BY created_at
        """
    ).fetchall()
    exported_runs = []
    for row in run_rows:
        run_id = row[0]
        public_id = pseudonym(database, run_id)
        metrics = {
            name: {"value": value, "class": metric_class, "definition_version": version}
            for name, value, metric_class, version in connection.execute(
                "SELECT name,value,class,definition_version FROM metrics WHERE run_id=? ORDER BY name",
                (run_id,),
            )
        }
        artifact = connection.execute(
            """
            SELECT config_sha256,prompt_sha256,code_version,python_version,platform
            FROM run_artifacts WHERE run_id=?
            """,
            (run_id,),
        ).fetchone()
        probes = [
            {
                "tick": tick,
                "probe_id": probe_id,
                "kind": kind,
                "expected": parse_json(expected),
                "response": parse_json(response),
                "observation": parse_json(observation),
                "model_visible_context": parse_json(context),
            }
            for tick, probe_id, kind, expected, response, observation, context
            in connection.execute(
                """
                SELECT p.tick,p.probe_id,p.kind,p.expected_json,p.response_json,
                       s.observation_json,s.context_json
                FROM probes p JOIN steps s ON s.run_id=p.run_id AND s.tick=p.tick
                WHERE p.run_id=? ORDER BY p.tick
                """,
                (run_id,),
            )
        ]
        exported_runs.append({
            "run": {
                "public_run_id": public_id,
                "created_at": row[1],
                "completed_at": row[2],
                "experiment": row[3],
                "condition": row[4],
                "seed": row[5],
                "adapter": row[6],
                "requested_model": row[7],
                "requested_temperature": row[8],
                "config": parse_json(row[9]),
                "code_version": row[10],
                "status": row[11],
                "stop_reason": row[12],
                "epistemic_notice": row[13],
            },
            "artifact_hashes": (
                {
                    "config_sha256": artifact[0],
                    "prompt_sha256": artifact[1],
                    "code_version": artifact[2],
                    "python_version": artifact[3],
                    "platform": artifact[4],
                }
                if artifact else None
            ),
            "metrics": metrics,
            "probes": probes,
        })
    connection.close()

    destination.mkdir(parents=True, exist_ok=True)
    output = destination / f"{database.stem}.public.json"
    payload = {
        "source_database": database.name,
        "source_database_sha256": sha256(database),
        "privacy_note": (
            "Provider session identifiers and raw provider metadata are excluded. "
            "Run identifiers are one-way pseudonyms."
        ),
        "epistemic_notice": (
            "These are behavioural and computational records. They are not evidence "
            "of phenomenal consciousness."
        ),
        "runs": exported_runs,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "file": output.name,
        "sha256": sha256(output),
        "runs": len(exported_runs),
        "completed": sum(item["run"]["status"] == "completed" for item in exported_runs),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a privacy-reviewed public Theta export")
    parser.add_argument("--db", action="append", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    exports = [export_database(path.resolve(), args.out.resolve()) for path in args.db]
    manifest = {
        "format": "project-theta-public-bundle-v1",
        "exports": exports,
        "excluded": [
            "provider session identifiers",
            "raw provider metadata",
            "API credentials",
            "working database files",
        ],
    }
    manifest_path = args.out.resolve() / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
