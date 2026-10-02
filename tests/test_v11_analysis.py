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
    path = Path(__file__).resolve().parents[1] / "scripts" / "analyze_v11_mechanisms.py"
    spec = importlib.util.spec_from_file_location("theta_v11_analysis", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ANALYZER = _load_analyzer()


class V11AnalysisTests(unittest.TestCase):
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
        runs = connection.execute(
            "SELECT run_id FROM runs ORDER BY run_id"
        ).fetchall()
        for (run_id,) in runs:
            ticks = connection.execute(
                "SELECT tick FROM api_calls WHERE run_id=? ORDER BY tick", (run_id,)
            ).fetchall()
            for (tick,) in ticks:
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

    def test_frozen_mechanism_gates_and_classifications(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v11.sqlite"
            self._fixture(database)
            interrupted = replace(
                RunConfig(),
                experiment="multi_body_mechanism_v11",
                condition="full",
                seed=7300,
            )
            with RunStore(database) as store:
                store.start_run("preserved-interruption", interrupted.to_dict())
                store.fail_run("preserved-interruption", "interrupted_before_completion")

            result = ANALYZER.analyze(database, bootstrap_samples=100)

            self.assertTrue(result["complete"])
            self.assertTrue(result["mechanism_progression_pass"])
            self.assertTrue(all(result["gates"].values()))
            self.assertTrue(result["classifications"]["incorrect_summary_interference"])
            self.assertFalse(result["classifications"]["summary_necessity"])
            self.assertEqual(result["execution"]["provider_calls"], 6_336)
            self.assertEqual(result["execution"]["unique_provider_ids"], 6_336)
            self.assertEqual(result["execution"]["preserved_interruptions"], 1)

            connection = sqlite3.connect(database)
            connection.execute(
                "UPDATE api_calls SET metadata_json=? WHERE rowid=(SELECT MIN(rowid) FROM api_calls)",
                (json.dumps({"model": "wrong/model"}),),
            )
            connection.commit()
            connection.close()

            rejected = ANALYZER.analyze(database, bootstrap_samples=10)
            self.assertFalse(rejected["complete"])
            self.assertFalse(rejected["mechanism_progression_pass"])


if __name__ == "__main__":
    unittest.main()
