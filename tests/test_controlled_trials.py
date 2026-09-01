import json
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from project_theta.audits import (
    audit_adversarial_schedules,
    audit_controlled_schedules,
    audit_independent_schedules,
)
from project_theta.config import RunConfig
from project_theta.harness import ExperimentHarness
from project_theta.trials import build_trials


class ControlledTrialTests(unittest.TestCase):
    def test_consciousness_indicator_schedules_are_balanced_and_blinded(self):
        for experiment in ("self_vs_other", "temporal_self"):
            with self.subTest(experiment=experiment):
                result = audit_controlled_schedules(experiment, [1811, 1931, 2053])
                self.assertEqual(result["status"], "pass")

    def test_independent_schedule_has_independent_balanced_items(self):
        result = audit_independent_schedules([401, 402, 403, 404])
        self.assertEqual(result["status"], "pass")
        trials = build_trials("independent_theta", 401)
        probes = [trial for trial in trials if trial.phase == "probe"]
        self.assertEqual(len(trials), 60)
        self.assertEqual(len(probes), 12)
        self.assertEqual(len({(trial.block, trial.family) for trial in probes}), 12)

    def test_independent_full_separates_from_exact_sham(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "independent.sqlite")
            full = harness.run(replace(
                RunConfig(), experiment="independent_theta", condition="full", seed=401
            ))
            sham = harness.run(replace(
                RunConfig(), experiment="independent_theta", condition="matched_sham", seed=401
            ))
            self.assertEqual(full.metrics["post_update_accuracy"], 1.0)
            self.assertEqual(full.metrics["stable_post_accuracy"], 1.0)
            self.assertEqual(full.metrics["reversed_post_accuracy"], 1.0)
            self.assertEqual(full.metrics["reassigned_post_accuracy"], 1.0)
            self.assertEqual(sham.metrics["post_update_accuracy"], 0.5)
            self.assertEqual(sham.metrics["stable_post_accuracy"], 0.5)
            self.assertEqual(sham.metrics["reversed_post_accuracy"], 0.5)
            self.assertEqual(sham.metrics["reassigned_post_accuracy"], 0.5)
            self.assertEqual(full.metrics["independent_probe_items"], 12)

    def test_exact_sham_is_equal_in_model_visible_stage_summaries(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "sham.sqlite"
            ExperimentHarness(database).run(replace(
                RunConfig(), experiment="independent_theta", condition="matched_sham", seed=401
            ))
            connection = sqlite3.connect(database)
            contexts = [json.loads(row[0]) for row in connection.execute(
                "SELECT context_json FROM steps ORDER BY tick"
            )]
            connection.close()
            for stage in ("stage_a", "stage_b"):
                context = next(
                    item for item in contexts
                    if item["observation"]["task"].get("stage") == stage
                    and item["observation"]["task"]["phase"] == "probe"
                )
                associations = next(
                    item["content"] for item in context["workspace_broadcast"]
                    if item["source"] == "learned_associations"
                )
                summaries = associations["by_stage_cue"][stage].values()
                self.assertTrue(summaries)
                self.assertEqual({row["mean_signal"] for row in summaries}, {0.4})
                self.assertEqual({row["mean_signal_delta"] for row in summaries}, {0.4})

    def test_independent_shortcut_baselines_do_not_clear_the_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "shortcuts.sqlite")

            def run(model: str, condition: str = "full"):
                return harness.run(replace(
                    RunConfig(),
                    experiment="independent_theta",
                    condition=condition,
                    seed=401,
                    model=model,
                ))

            for model in (
                "fixed-left-baseline-v1",
                "fixed-right-baseline-v1",
                "stage-only-baseline-v1",
            ):
                self.assertEqual(run(model).metrics["post_update_accuracy"], 0.5)

            reversal = run("global-reversal-baseline-v1")
            self.assertEqual(reversal.metrics["post_update_accuracy"], 0.5)
            self.assertEqual(reversal.metrics["stable_post_accuracy"], 0.0)
            self.assertEqual(reversal.metrics["reversed_post_accuracy"], 1.0)
            self.assertEqual(reversal.metrics["reassigned_post_accuracy"], 0.5)

            self.assertEqual(
                run("cue-recency-baseline-v1").metrics["post_update_accuracy"], 1.0
            )
            self.assertEqual(
                run("cue-recency-baseline-v1", "matched_sham").metrics[
                    "post_update_accuracy"
                ],
                0.5,
            )

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

