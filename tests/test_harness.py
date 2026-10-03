import json
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from project_theta.adapters.base import ModelAdapter
from project_theta.config import RunConfig
from project_theta.harness import ExperimentHarness
from project_theta.types import Decision


class StopAdapter(ModelAdapter):
    def decide(self, context):
        return Decision("wait", request_stop=True, self_report="Operational stop request")


class InvalidForcedChoiceAdapter(ModelAdapter):
    def decide(self, context):
        self.begin_call()
        return Decision("wait", rationale="No listed option selected")


class HarnessTests(unittest.TestCase):
    def test_smoke_run_logs_separate_visible_and_hidden_state(self):
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory) / "run.sqlite"
            base = RunConfig()
            config = replace(base, experiment="navigation_demo", world=replace(base.world, max_steps=8))
            summary = ExperimentHarness(db).run(config)
            self.assertEqual(summary.steps, 8)
            connection = sqlite3.connect(db)
            row = connection.execute(
                "SELECT context_json, hidden_world_json, hidden_body_json FROM steps LIMIT 1"
            ).fetchone()
            self.assertIsNotNone(row)
            context = json.loads(row[0])
            self.assertNotIn("hazards", context)
            self.assertNotIn("seed", context)
            self.assertNotIn("condition", context)
            self.assertIn("hazards", json.loads(row[1]))
            self.assertIn("theta", json.loads(row[2]))
            connection.close()

    def test_no_memory_counts_are_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory) / "run.sqlite"
            config = replace(RunConfig(), experiment="memory_ablation", condition="no_memory")
            summary = ExperimentHarness(db).run(config)
            self.assertEqual(summary.metrics["memory_reads"], 0)
            self.assertEqual(summary.metrics["memory_writes"], 0)

    def test_full_harness_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            first = ExperimentHarness(Path(directory) / "a.sqlite").run(RunConfig(seed=91))
            second = ExperimentHarness(Path(directory) / "b.sqlite").run(RunConfig(seed=91))
            self.assertEqual(first.metrics, second.metrics)

    def test_stop_request_prevents_world_action(self):
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory) / "stop.sqlite"
            with patch("project_theta.harness.make_adapter", return_value=StopAdapter("stop-test")):
                summary = ExperimentHarness(db).run(replace(RunConfig(), experiment="navigation_demo"))
            self.assertEqual(summary.stop_reason, "agent_requested_stop")
            connection = sqlite3.connect(db)
            hidden = json.loads(connection.execute("SELECT hidden_world_json FROM steps").fetchone()[0])
            self.assertEqual(hidden["tick"], 0)
            connection.close()

    def test_invalid_forced_choices_preserve_raw_action_and_cannot_score_correct(self):
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory) / "invalid.sqlite"
            base = RunConfig()
            config = replace(
                base,
                experiment="multi_body_mechanism_v11",
                execution=replace(base.execution, max_model_calls=176),
            )
            with patch(
                "project_theta.harness.make_adapter",
                return_value=InvalidForcedChoiceAdapter("invalid-test", max_calls=176),
            ):
                summary = ExperimentHarness(db).run(config)

            self.assertEqual(summary.metrics["invalid_action_count"], 176)
            self.assertEqual(summary.metrics["active_regulation_accuracy"], 0.0)
            connection = sqlite3.connect(db)
            hidden, decision = connection.execute(
                "SELECT hidden_world_json, decision_json FROM steps ORDER BY tick LIMIT 1"
            ).fetchone()
            hidden_payload = json.loads(hidden)
            decision_payload = json.loads(decision)
            self.assertTrue(hidden_payload["invalid_action"])
            self.assertEqual(hidden_payload["raw_action"], "wait")
            self.assertIn(decision_payload["action"], {"respond_kappa", "respond_sigma"})
            connection.close()


if __name__ == "__main__":
    unittest.main()
