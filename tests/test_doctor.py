import tempfile
import unittest
from pathlib import Path

from project_theta.doctor import run_doctor


class DoctorTests(unittest.TestCase):
    def test_scripted_preflight_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_doctor("scripted", Path(directory) / "doctor.sqlite")
        self.assertEqual(result["status"], "pass")
        self.assertTrue(all(check["status"] != "fail" for check in result["checks"]))


if __name__ == "__main__":
    unittest.main()
