import contextlib
import io
import json
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from project_theta.audits import (
    add_execution_audit,
    audit_adversarial_schedules,
    audit_independent_schedules,
)
from project_theta.cli import main
from project_theta.config import RunConfig
from project_theta.harness import ExperimentHarness
from project_theta.storage import RunStore


class CliTests(unittest.TestCase):
    def test_multi_seed_execution_audit_requires_exact_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "multi.sqlite"
            ExperimentHarness(database).run_study(
                "independent_theta",
                [401, 402],
                RunConfig(),
                conditions=["full", "matched_sham"],
                max_runs=4,
            )
            interrupted_config = replace(
                RunConfig(),
                experiment="independent_theta",
                condition="full",
                seed=401,
            )
            with RunStore(database) as store:
                store.start_run("allowed-interrupted-attempt", interrupted_config.to_dict())
                store.mark_interrupted_runs()
            audit = add_execution_audit(
                audit_independent_schedules([401, 402]),
                database,
                [401, 402],
                60,
                expected_experiment="independent_theta",
                expected_conditions=["full", "matched_sham"],
            )
            self.assertEqual(audit["status"], "pass")

    def test_execution_audit_accepts_preserved_windows_cleanup_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "cleanup-retry.sqlite"
            ExperimentHarness(database).run_study(
                "independent_theta",
                [403],
                RunConfig(),
                conditions=["full"],
                max_runs=1,
            )
            failed_config = replace(
                RunConfig(),
                experiment="independent_theta",
                condition="full",
                seed=403,
            )
            with RunStore(database) as store:
                store.start_run("allowed-cleanup-attempt", failed_config.to_dict())
                store.fail_run(
                    "allowed-cleanup-attempt",
                    "AdapterError: Claude Code failed to start: [WinError 32] "
                    "C:/Temp/theta-subject-example",
                )
            audit = add_execution_audit(
                audit_independent_schedules([403]),
                database,
                [403],
                60,
                expected_experiment="independent_theta",
                expected_conditions=["full"],
            )
            self.assertEqual(audit["status"], "pass")

    def test_config_experiment_is_used_when_cli_option_is_omitted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "config.json"
            database = root / "study.sqlite"
            config.write_text(json.dumps({
                "experiment": "adversarial_theta",
                "condition": "full",
                "trial_profile": "compact",
                "adapter": "scripted",
                "model": "scripted-baseline-v1",
                "execution": {"max_model_calls": 18},
            }), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                exit_code = main([
                    "run",
                    "--config", str(config),
                    "--seeds", "91",
                    "--max-runs", "1",
                    "--db", str(database),
                ])
            connection = sqlite3.connect(database)
            experiment, steps = connection.execute(
                "SELECT experiment, (SELECT COUNT(*) FROM steps) FROM runs"
            ).fetchone()
            connection.close()
            self.assertEqual(exit_code, 0)
            self.assertEqual(experiment, "adversarial_theta")
            self.assertEqual(steps, 16)
            audit = add_execution_audit(
                audit_adversarial_schedules([91], "compact"), database, 91, 16
            )
            self.assertEqual(audit["status"], "pass")


if __name__ == "__main__":
    unittest.main()

