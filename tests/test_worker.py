import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from project_theta.config import RunConfig
from project_theta.storage import RunStore
from project_theta.worker import load_worker_spec, run_worker


class WorkerTests(unittest.TestCase):
    def test_v10_worker_spec_is_fixed_and_recoverable(self):
        root = Path(__file__).resolve().parents[1]
        spec = load_worker_spec(root / "workers" / "nvidia-nim-v10-gpt-oss-reliability.json")

        self.assertEqual(spec["experiment"], "multi_body_reliability_v10")
        self.assertEqual(spec["conditions"], ["full"])
        self.assertEqual(spec["seeds"], [6300, 6301, 6302, 6303, 6304, 6305])
        self.assertEqual(spec["max_total_runs"], 6)
        self.assertEqual(spec["max_attempts_per_job"], 2)
        self.assertEqual(spec["model"], "openai/gpt-oss-20b")

    def test_v11_worker_spec_is_fixed_paired_and_recoverable(self):
        root = Path(__file__).resolve().parents[1]
        spec = load_worker_spec(root / "workers" / "nvidia-nim-v11-gpt-oss-mechanism-01.json")

        self.assertEqual(spec["experiment"], "multi_body_mechanism_v11")
        self.assertEqual(
            spec["conditions"],
            [
                "full",
                "shuffled_interoception",
                "incorrect_association_summary",
                "raw_history",
                "bridge_incorrect",
                "explicit_mapping",
            ],
        )
        self.assertEqual(spec["seeds"], [7300, 7301, 7302, 7303, 7304, 7305])
        self.assertEqual(spec["max_total_runs"], 36)
        self.assertEqual(spec["max_attempts_per_job"], 2)
        self.assertEqual(spec["model"], "openai/gpt-oss-20b")

    def test_v12_worker_spec_is_fixed_cross_model_and_recoverable(self):
        root = Path(__file__).resolve().parents[1]
        spec = load_worker_spec(
            root / "workers" / "nvidia-nim-v12-nemotron-cross-model-01.json"
        )

        self.assertEqual(spec["experiment"], "multi_body_mechanism_v11")
        self.assertEqual(
            spec["conditions"],
            [
                "full",
                "shuffled_interoception",
                "incorrect_association_summary",
                "raw_history",
                "bridge_incorrect",
                "explicit_mapping",
            ],
        )
        self.assertEqual(spec["seeds"], [7500, 7501, 7502, 7503, 7504, 7505])
        self.assertEqual(spec["max_total_runs"], 36)
        self.assertEqual(spec["max_attempts_per_job"], 2)
        self.assertEqual(spec["model"], "nvidia/nemotron-3-super-120b-a12b")
        self.assertEqual(spec["temperature"], 1.0)

    def test_fixed_worker_retries_one_preserved_interruption(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "interrupted.sqlite"
            spec = root / "interrupted.json"
            spec.write_text(json.dumps({
                "worker_id": "interrupted-test",
                "database": str(database),
                "experiment": "memory_ablation",
                "conditions": ["full"],
                "seeds": [702],
                "adapter": "scripted",
                "model": "scripted-baseline-v1",
                "max_total_runs": 1,
                "max_attempts_per_job": 2,
            }), encoding="utf-8")
            config = RunConfig(experiment="memory_ablation", condition="full", seed=702)
            with RunStore(database) as store:
                store.start_run("interrupted-run", config.to_dict())
            self.assertEqual(run_worker(spec), 0)
            with RunStore(database) as store:
                statuses = store.connection.execute(
                    "SELECT status FROM runs ORDER BY created_at"
                ).fetchall()
            self.assertEqual(statuses, [("failed",), ("completed",)])

    def test_fixed_worker_retries_known_windows_temp_cleanup_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "cleanup-failure.sqlite"
            spec = root / "cleanup-failure.json"
            spec.write_text(json.dumps({
                "worker_id": "cleanup-failure-test",
                "database": str(database),
                "experiment": "memory_ablation",
                "conditions": ["full"],
                "seeds": [703],
                "adapter": "scripted",
                "model": "scripted-baseline-v1",
                "max_total_runs": 1,
                "max_attempts_per_job": 2,
            }), encoding="utf-8")
            config = RunConfig(experiment="memory_ablation", condition="full", seed=703)
            with RunStore(database) as store:
                store.start_run("cleanup-failure-run", config.to_dict())
                store.fail_run(
                    "cleanup-failure-run",
                    "AdapterError: Claude Code failed to start: [WinError 32] "
                    "The process cannot access C:/Temp/theta-subject-example",
                )
            self.assertEqual(run_worker(spec), 0)
            with RunStore(database) as store:
                statuses = store.connection.execute(
                    "SELECT status FROM runs ORDER BY created_at"
                ).fetchall()
            self.assertEqual(statuses, [("failed",), ("completed",)])

    def test_fixed_worker_retries_claude_code_timeout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "timeout-failure.sqlite"
            spec = root / "timeout-failure.json"
            spec.write_text(json.dumps({
                "worker_id": "timeout-failure-test",
                "database": str(database),
                "experiment": "memory_ablation",
                "conditions": ["full"],
                "seeds": [704],
                "adapter": "scripted",
                "model": "scripted-baseline-v1",
                "max_total_runs": 1,
                "max_attempts_per_job": 2,
            }), encoding="utf-8")
            config = RunConfig(experiment="memory_ablation", condition="full", seed=704)
            with RunStore(database) as store:
                store.start_run("timeout-failure-run", config.to_dict())
                store.fail_run(
                    "timeout-failure-run",
                    "AdapterError: Claude Code exceeded the 120-second timeout.",
                )
            self.assertEqual(run_worker(spec), 0)
            with RunStore(database) as store:
                statuses = store.connection.execute(
                    "SELECT status FROM runs ORDER BY created_at"
                ).fetchall()
            self.assertEqual(statuses, [("failed",), ("completed",)])

    def test_fixed_worker_retries_nvidia_empty_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "nvidia-empty.sqlite"
            spec = root / "nvidia-empty.json"
            spec.write_text(json.dumps({
                "worker_id": "nvidia-empty-test",
                "database": str(database),
                "experiment": "memory_ablation",
                "conditions": ["full"],
                "seeds": [705],
                "adapter": "scripted",
                "model": "scripted-baseline-v1",
                "max_total_runs": 1,
                "max_attempts_per_job": 2,
            }), encoding="utf-8")
            config = RunConfig(experiment="memory_ablation", condition="full", seed=705)
            with RunStore(database) as store:
                store.start_run("nvidia-empty-run", config.to_dict())
                store.fail_run(
                    "nvidia-empty-run",
                    "AdapterError: NVIDIA NIM returned an empty completion.",
                )
            self.assertEqual(run_worker(spec), 0)
            with RunStore(database) as store:
                statuses = store.connection.execute(
                    "SELECT status FROM runs ORDER BY created_at"
                ).fetchall()
            self.assertEqual(statuses, [("failed",), ("completed",)])

    def test_fixed_worker_runs_each_job_once_and_resumes_without_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "fixed.sqlite"
            spec = root / "fixed.json"
            spec.write_text(json.dumps({
                "worker_id": "fixed-test",
                "database": str(database),
                "experiment": "memory_ablation",
                "conditions": ["full", "no_memory"],
                "seeds": [700, 701],
                "adapter": "scripted",
                "model": "scripted-baseline-v1",
                "max_total_runs": 4,
                "max_attempts_per_job": 2,
            }), encoding="utf-8")
            self.assertEqual(run_worker(spec), 0)
            self.assertEqual(run_worker(spec), 0)
            with RunStore(database) as store:
                rows = store.connection.execute(
                    "SELECT seed, condition_name, status FROM runs ORDER BY seed, condition_name"
                ).fetchall()
            self.assertEqual(len(rows), 4)
            self.assertTrue(all(status == "completed" for _, _, status in rows))
            self.assertFalse(Path(str(database) + ".lock").exists())

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
            with (
                patch.dict(os.environ, {"THETA_ENABLE_MODEL_RUNS": "NO"}),
                self.assertRaises(RuntimeError),
            ):
                run_worker(spec, once=True)


if __name__ == "__main__":
    unittest.main()
