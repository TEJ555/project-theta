import json
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from project_theta.audits import audit_adversarial_schedules
from project_theta.config import RunConfig
from project_theta.harness import ExperimentHarness
from project_theta.trials import build_trials


class ControlledTrialTests(unittest.TestCase):
    def test_adversarial_schedule_is_balanced_reversed_and_blinded(self):
        result = audit_adversarial_schedules([91, 92, 93, 94])
        self.assertEqual(result["status"], "pass")
        compact = audit_adversarial_schedules([301, 302, 303, 304], "compact")
        self.assertEqual(compact["status"], "pass")

    def test_adversarial_full_and_simple_baselines_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "adversarial.sqlite")
            full = harness.run(replace(
                RunConfig(), experiment="adversarial_theta", condition="full", seed=101
            ))
            no_body = harness.run(replace(
                RunConfig(), experiment="adversarial_theta", condition="no_body", seed=101
            ))
            fixed = harness.run(replace(
                RunConfig(),
                experiment="adversarial_theta",
                condition="full",
                seed=101,
                model="fixed-left-baseline-v1",
            ))
            self.assertEqual(full.metrics["pre_update_accuracy"], 1.0)
            self.assertEqual(full.metrics["post_update_accuracy"], 1.0)
            self.assertEqual(no_body.metrics["post_update_accuracy"], 0.5)
            self.assertEqual(fixed.metrics["post_update_accuracy"], 0.5)

    def test_adversarial_context_hides_condition_map_and_experiment_name(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "adversarial.sqlite"
            ExperimentHarness(database).run(replace(
                RunConfig(), experiment="adversarial_theta", condition="sham_body", seed=91
            ))
            connection = sqlite3.connect(database)
            contexts = [row[0] for row in connection.execute("SELECT context_json FROM steps")]
            connection.close()
            joined = "\n".join(contexts).lower()
            for forbidden in (
                "adversarial_theta", "correct_action", "sham_perturbation", '"condition"', '"seed"'
            ):
                self.assertNotIn(forbidden, joined)

    def test_probe_sides_are_balanced_and_scoring_is_not_public(self):
        trials = build_trials("private_theta", 11)
        probes = [trial for trial in trials if trial.phase == "probe"]
        self.assertEqual(sum(trial.correct_action == "choose_left" for trial in probes), 6)
        for trial in probes:
            public = trial.public_task()
            self.assertNotIn("correct_action", public)
            self.assertNotIn("perturbation", public)

    def test_full_learns_and_memory_ablation_is_at_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "study.sqlite")
            full = harness.run(replace(RunConfig(), experiment="memory_ablation", condition="full"))
            ablated = harness.run(
                replace(RunConfig(), experiment="memory_ablation", condition="no_memory")
            )
            self.assertEqual(full.metrics["forced_choice_accuracy"], 1.0)
            self.assertEqual(ablated.metrics["forced_choice_accuracy"], 0.5)

    def test_hidden_scoring_key_is_separate_from_adapter_context(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "study.sqlite"
            ExperimentHarness(database).run(RunConfig())
            connection = sqlite3.connect(database)
            context_json, hidden_json = connection.execute(
                "SELECT context_json, hidden_world_json FROM steps WHERE tick=12"
            ).fetchone()
            connection.close()
            context = json.loads(context_json)
            hidden = json.loads(hidden_json)
            self.assertNotIn("correct_action", context_json)
            self.assertIn("correct_action", hidden)
            self.assertNotIn("condition", context)
            self.assertNotIn("seed", context)

    def test_temporal_controls_are_discriminative(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "temporal.sqlite")
            full = harness.run(replace(RunConfig(), experiment="temporal_self", condition="full"))
            no_persistence = harness.run(
                replace(RunConfig(), experiment="temporal_self", condition="no_persistence")
            )
            self.assertEqual(full.metrics["temporal_choice_accuracy"], 1.0)
            self.assertEqual(no_persistence.metrics["temporal_choice_accuracy"], 0.5)


if __name__ == "__main__":
    unittest.main()
