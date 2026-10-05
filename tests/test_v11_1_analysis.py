import importlib.util
import json
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from project_theta.config import RunConfig
from project_theta.harness import ExperimentHarness
from project_theta.storage import RunStore


def _load_analyzer():
    path = Path(__file__).resolve().parents[1] / "scripts" / "analyze_v11_1_repair.py"
    spec = importlib.util.spec_from_file_location("theta_v11_1_analysis", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ANALYZER = _load_analyzer()


class V111AnalysisTests(unittest.TestCase):
    def _fixture(self, database: Path) -> None:
        harness = ExperimentHarness(database)
        base = replace(
            RunConfig(),
            experiment="multi_body_mechanism_v11",
            inference_profile="all_trials",
            execution=replace(RunConfig().execution, max_model_calls=176),
        )
        for seed in ANALYZER.PLANNED_SEEDS:
            for condition in ANALYZER.CONDITIONS:
                harness.run(replace(base, seed=seed, condition=condition))

        connection = sqlite3.connect(database)
        for (run_id,) in connection.execute("SELECT run_id FROM runs ORDER BY run_id"):
            for (tick,) in connection.execute(
                "SELECT tick FROM api_calls WHERE run_id=? ORDER BY tick", (run_id,)
            ):
                provider_id = f"fixture-{run_id}-{tick}"
                connection.execute(
                    "UPDATE api_calls SET provider_id=?, metadata_json=? "
                    "WHERE run_id=? AND tick=?",
                    (
                        provider_id,
                        json.dumps({"model": ANALYZER.REQUIRED_MODEL}),
                        run_id,
                        tick,
                    ),
                )
                connection.execute(
                    "UPDATE steps SET provider_id=? WHERE run_id=? AND tick=?",
                    (provider_id, run_id, tick),
                )
        connection.commit()
        connection.close()

    def test_repaired_raw_provenance_and_gates(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v11-1.sqlite"
            self._fixture(database)
            result = ANALYZER.analyze(database, bootstrap_samples=100)

            self.assertTrue(result["complete"])
            self.assertTrue(result["mechanism_progression_pass"])
            self.assertTrue(all(result["gates"].values()))
            self.assertEqual(result["execution"]["invalid_actions"], 0)

            connection = sqlite3.connect(database)
            run_id, decision_json, hidden_json = connection.execute(
                "SELECT run_id, decision_json, hidden_world_json FROM steps "
                "WHERE tick=0 ORDER BY run_id LIMIT 1"
            ).fetchone()
            decision = json.loads(decision_json)
            hidden = json.loads(hidden_json)
            hidden["invalid_action"] = True
            hidden["raw_action"] = "none"
            decision["action"] = "respond_kappa"
            connection.execute(
                "UPDATE steps SET decision_json=?, hidden_world_json=? "
                "WHERE run_id=? AND tick=0",
                (json.dumps(decision), json.dumps(hidden), run_id),
            )
            connection.commit()
            connection.close()

            rejected = ANALYZER.analyze(database, bootstrap_samples=10)
            self.assertFalse(rejected["complete"])
            self.assertFalse(rejected["mechanism_progression_pass"])

    def test_exact_documented_empty_completion_is_preserved_but_not_analyzed(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v11-1-recovery.sqlite"
            self._fixture(database)
            failed = replace(
                RunConfig(),
                experiment="multi_body_mechanism_v11",
                condition="raw_history",
                seed=7402,
            )
            with RunStore(database) as store:
                store.start_run("preserved-empty-completion", failed.to_dict())
                store.fail_run(
                    "preserved-empty-completion",
                    ANALYZER.ALLOWED_INFRASTRUCTURE_FAILURE,
                )

            accepted = ANALYZER.analyze(database, bootstrap_samples=10)
            self.assertTrue(accepted["complete"])
            self.assertTrue(accepted["mechanism_progression_pass"])
            self.assertEqual(
                accepted["execution"]["preserved_nvidia_empty_completions"], 1
            )
            self.assertEqual(accepted["execution"]["provider_calls"], 6_336)

            with RunStore(database) as store:
                store.start_run("unrecognised-provider-failure", failed.to_dict())
                store.fail_run(
                    "unrecognised-provider-failure",
                    "AdapterError: NVIDIA NIM returned malformed content.",
                )

            rejected = ANALYZER.analyze(database, bootstrap_samples=10)
            self.assertFalse(rejected["complete"])
            self.assertFalse(rejected["mechanism_progression_pass"])

    def test_second_recovery_attempt_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v11-1-duplicate-recovery.sqlite"
            self._fixture(database)
            failed = replace(
                RunConfig(),
                experiment="multi_body_mechanism_v11",
                condition="raw_history",
                seed=7402,
            )
            with RunStore(database) as store:
                for run_id in ("first-empty-completion", "second-empty-completion"):
                    store.start_run(run_id, failed.to_dict())
                    store.fail_run(run_id, ANALYZER.ALLOWED_INFRASTRUCTURE_FAILURE)

            rejected = ANALYZER.analyze(database, bootstrap_samples=10)
            self.assertFalse(rejected["complete"])
            self.assertFalse(rejected["mechanism_progression_pass"])


if __name__ == "__main__":
    unittest.main()
