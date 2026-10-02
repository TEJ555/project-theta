import importlib.util
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from project_theta.config import RunConfig
from project_theta.metrics import METRIC_REGISTRY
from project_theta.storage import RunStore


def _load_analyzer():
    path = Path(__file__).resolve().parents[1] / "scripts" / "analyze_v10_reliability.py"
    spec = importlib.util.spec_from_file_location("theta_v10_analysis", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ANALYZER = _load_analyzer()


class V10AnalysisTests(unittest.TestCase):
    def _completed_run(self, database: Path, seed: int, run_id: str | None = None) -> None:
        config = replace(
            RunConfig(),
            experiment="multi_body_reliability_v10",
            condition="full",
            seed=seed,
            adapter="nvidia_nim",
            model="openai/gpt-oss-20b",
        )
        run_id = run_id or f"complete-{seed}"
        with RunStore(database) as store:
            store.start_run(run_id, config.to_dict(), code_version="a" * 40)
            tick = 0
            for family_number in range(4):
                family = f"family-{seed}-{family_number}"
                kinds = [
                    ("active_body_learning", 12),
                    ("body_mapping_checkpoint", 8),
                    ("interface_comprehension_probe", 8),
                    ("active_regulation_probe", 8),
                    ("active_regulation_transfer_probe", 8),
                ]
                for kind, count in kinds:
                    for _ in range(count):
                        task = {"kind": kind, "family_token": family, "target_I7": 0.5}
                        correct_action = None if kind == "active_body_learning" else "choose_left"
                        perturbation = (
                            0.8
                            if kind in {
                                "active_regulation_probe",
                                "active_regulation_transfer_probe",
                            }
                            else 0.5
                        )
                        store.connection.execute(
                            "INSERT INTO steps VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                run_id,
                                tick,
                                json.dumps({"task": task}),
                                "{}",
                                json.dumps({"action": "choose_left"}),
                                "[]",
                                json.dumps({
                                    "correct_action": correct_action,
                                    "perturbation": perturbation,
                                }),
                                json.dumps({"theta": 0.5}),
                                0.0,
                                f"provider-{seed}-{tick}",
                            ),
                        )
                        store.connection.execute(
                            "INSERT INTO api_calls VALUES (?, ?, ?, ?)",
                            (
                                run_id,
                                tick,
                                f"provider-{seed}-{tick}",
                                json.dumps({"model": "openai/gpt-oss-20b"}),
                            ),
                        )
                        tick += 1
            store.finish_run(
                run_id,
                {
                    "active_regulation_accuracy": 1.0,
                    "active_exact_accuracy": 1.0,
                    "active_transfer_accuracy": 1.0,
                    "interface_comprehension_accuracy": 1.0,
                    "body_mapping_checkpoint_accuracy": 1.0,
                    "hidden_regulation_improvement": 0.3,
                    "hidden_regulation_final_error": 0.0,
                    "invalid_action_count": 0,
                    "welfare_stops": 0,
                    "model_calls": 176,
                },
                METRIC_REGISTRY,
                None,
            )

    def test_preserved_interruption_is_reported_but_does_not_contaminate_outcomes(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v10.sqlite"
            interrupted = replace(
                RunConfig(),
                experiment="multi_body_reliability_v10",
                condition="full",
                seed=6300,
                adapter="nvidia_nim",
                model="openai/gpt-oss-20b",
            )
            with RunStore(database) as store:
                store.start_run("interrupted-6300", interrupted.to_dict(), code_version="a" * 40)
                store.fail_run("interrupted-6300", "interrupted_before_completion")
            for seed in sorted(ANALYZER.PLANNED_SEEDS):
                self._completed_run(database, seed)

            result = ANALYZER.analyze(database, bootstrap_samples=100)

            self.assertTrue(result["complete"])
            self.assertTrue(result["progression_pass"])
            self.assertEqual(result["provider"]["calls"], 1056)
            self.assertEqual(result["execution"]["preserved_interruptions"], 1)
            self.assertEqual(len(result["seeds"]), 6)
            families = [
                family
                for seed in result["seeds"]
                for family in seed["families"]
            ]
            self.assertEqual(len(families), 24)
            self.assertTrue(all(family["hidden_final_error"] == 0.0 for family in families))
            for family in families:
                self.assertAlmostEqual(family["hidden_improvement"], 0.3)

            failed = replace(interrupted, seed=6301)
            with RunStore(database) as store:
                store.start_run("nonretryable-6301", failed.to_dict(), code_version="a" * 40)
                store.fail_run("nonretryable-6301", "AdapterError: malformed provider output")

            blocked = ANALYZER.analyze(database, bootstrap_samples=10)
            self.assertFalse(blocked["complete"])
            self.assertFalse(blocked["progression_pass"])

    def test_duplicate_completed_seed_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v10.sqlite"
            for seed in sorted(ANALYZER.PLANNED_SEEDS):
                self._completed_run(database, seed)
            self._completed_run(database, 6300, run_id="duplicate-complete-6300")

            result = ANALYZER.analyze(database, bootstrap_samples=10)

            self.assertFalse(result["complete"])
            self.assertFalse(result["progression_pass"])

    def test_null_required_metric_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v10.sqlite"
            for seed in sorted(ANALYZER.PLANNED_SEEDS):
                self._completed_run(database, seed)
            with RunStore(database) as store:
                store.connection.execute(
                    "UPDATE metrics SET value=NULL "
                    "WHERE run_id='complete-6300' AND name='model_calls'"
                )
                store.connection.commit()

            result = ANALYZER.analyze(database, bootstrap_samples=10)

            self.assertFalse(result["complete"])
            self.assertFalse(result["progression_pass"])

    def test_stored_metric_must_match_recomputed_trials(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v10.sqlite"
            for seed in sorted(ANALYZER.PLANNED_SEEDS):
                self._completed_run(database, seed)
            with RunStore(database) as store:
                store.connection.execute(
                    "UPDATE metrics SET value=0.75 "
                    "WHERE run_id='complete-6300' "
                    "AND name='active_regulation_accuracy'"
                )
                store.connection.commit()

            result = ANALYZER.analyze(database, bootstrap_samples=10)

            self.assertFalse(result["complete"])
            self.assertFalse(result["progression_pass"])
            seed = next(item for item in result["seeds"] if item["seed"] == 6300)
            self.assertFalse(seed["stored_metric_consistency"])

    def test_step_and_api_provider_ids_must_align(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v10.sqlite"
            for seed in sorted(ANALYZER.PLANNED_SEEDS):
                self._completed_run(database, seed)
            with RunStore(database) as store:
                store.connection.execute(
                    "UPDATE steps SET provider_id='mismatched-provider-id' "
                    "WHERE run_id='complete-6300' AND tick=0"
                )
                store.connection.commit()

            result = ANALYZER.analyze(database, bootstrap_samples=10)

            self.assertFalse(result["complete"])
            self.assertFalse(result["progression_pass"])
            run = next(
                item for item in result["execution"]["runs"]
                if item["run_id"] == "complete-6300"
            )
            self.assertFalse(run["provider_alignment"])


if __name__ == "__main__":
    unittest.main()
