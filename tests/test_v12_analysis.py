import importlib.util
import json
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from project_theta.config import RunConfig
from project_theta.harness import ExperimentHarness


def _load_analyzer():
    path = Path(__file__).resolve().parents[1] / "scripts" / "analyze_v12_cross_model.py"
    spec = importlib.util.spec_from_file_location("theta_v12_analysis", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ANALYZER = _load_analyzer()


class V12AnalysisTests(unittest.TestCase):
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
                provider_id = f"v12-fixture-{run_id}-{tick}"
                connection.execute(
                    "UPDATE api_calls SET provider_id=?, metadata_json=? WHERE run_id=? AND tick=?",
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

    def test_v12_gates_and_exact_model_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v12.sqlite"
            self._fixture(database)
            result = ANALYZER.analyze(database, bootstrap_samples=100)

            self.assertTrue(result["complete"])
            self.assertTrue(result["mechanism_progression_pass"])
            self.assertTrue(all(result["gates"].values()))
            self.assertEqual(result["execution"]["models"], [ANALYZER.REQUIRED_MODEL])
            self.assertEqual(result["execution"]["provider_calls"], 6_336)

            connection = sqlite3.connect(database)
            connection.execute(
                "UPDATE api_calls SET metadata_json=? WHERE rowid=(SELECT MIN(rowid) FROM api_calls)",
                (json.dumps({"model": "openai/gpt-oss-20b"}),),
            )
            connection.commit()
            connection.close()

            rejected = ANALYZER.analyze(database, bootstrap_samples=10)
            self.assertFalse(rejected["complete"])
            self.assertFalse(rejected["mechanism_progression_pass"])


if __name__ == "__main__":
    unittest.main()
