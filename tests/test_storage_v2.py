import sqlite3
import tempfile
import unittest
from pathlib import Path

from project_theta.config import RunConfig
from project_theta.harness import ExperimentHarness
from project_theta.storage import SCHEMA_VERSION, RunStore


class StorageV2Tests(unittest.TestCase):
    def test_provenance_api_metadata_and_schema_are_recorded(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "run.sqlite"
            ExperimentHarness(database).run(RunConfig())
            connection = sqlite3.connect(database)
            self.assertEqual(connection.execute("SELECT version FROM schema_info").fetchone()[0], SCHEMA_VERSION)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM run_artifacts").fetchone()[0], 1)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM api_calls").fetchone()[0], 24)
            connection.close()

    def test_interrupted_run_recovery_preserves_status(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "run.sqlite"
            with RunStore(database) as store:
                store.start_run("unfinished", RunConfig().to_dict(), "test-version")
                self.assertEqual(store.mark_interrupted_runs(), 1)
                status = store.connection.execute(
                    "SELECT status, stop_reason FROM runs WHERE run_id='unfinished'"
                ).fetchone()
            self.assertEqual(status, ("failed", "interrupted_before_completion"))


if __name__ == "__main__":
    unittest.main()
