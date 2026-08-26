import contextlib
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from project_theta.audits import add_execution_audit, audit_adversarial_schedules
from project_theta.cli import main


class CliTests(unittest.TestCase):
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
