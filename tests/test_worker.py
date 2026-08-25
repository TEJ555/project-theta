import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from project_theta.storage import RunStore
from project_theta.worker import run_worker


class WorkerTests(unittest.TestCase):
    def test_scripted_worker_resumes_with_fresh_seeds(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "worker.sqlite"
            spec = root / "worker.json"
            spec.write_text(json.dumps({
                "worker_id": "test-worker",
                "database": str(database),
                "experiment": "memory_ablation",
                "conditions": ["full", "no_memory"],
                "adapter": "scripted",
                "model": "scripted-baseline-v1",
                "start_seed": 500,
                "seeds_per_cycle": 1,
                "max_runs_per_cycle": 2,
                "interval_seconds": 1,
            }), encoding="utf-8")
            self.assertEqual(run_worker(spec, once=True), 0)
            self.assertEqual(run_worker(spec, once=True), 0)
            with RunStore(database) as store:
                state = store.worker_state("test-worker")
                seeds = [row[0] for row in store.connection.execute("SELECT DISTINCT seed FROM runs ORDER BY seed")]
            self.assertEqual(state, (2, 501))
            self.assertEqual(seeds, [500, 501])

    def test_model_worker_requires_explicit_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = root / "worker.json"
            spec.write_text(json.dumps({
                "worker_id": "locked", "database": str(root / "x.sqlite"),
                "experiment": "private_theta", "adapter": "openai", "model": "test",
                "seeds_per_cycle": 1, "max_runs_per_cycle": 1,
            }), encoding="utf-8")
            with patch.dict(os.environ, {"THETA_ENABLE_MODEL_RUNS": "NO"}):
                with self.assertRaises(RuntimeError):
                    run_worker(spec, once=True)


if __name__ == "__main__":
    unittest.main()
