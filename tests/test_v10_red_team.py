import importlib.util
import unittest
from pathlib import Path


def _load_red_team():
    path = Path(__file__).resolve().parents[1] / "scripts" / "red_team_v10.py"
    spec = importlib.util.spec_from_file_location("theta_v10_red_team", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RED_TEAM = _load_red_team()


class V10RedTeamTests(unittest.TestCase):
    def test_held_out_public_metadata_rules_stay_below_threshold(self):
        result = RED_TEAM.run_red_team(start_seed=20000, count=40)

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["schedule_audit_status"], "pass")
        self.assertEqual(result["forbidden_public_terms_found"], [])
        self.assertLessEqual(result["best_rule_score"], result["threshold"])
        self.assertEqual(result["fixed_kappa_score"], 0.5)
        self.assertEqual(result["fixed_sigma_score"], 0.5)
        self.assertEqual(result["first_displayed_score"], 0.5)
        self.assertEqual(
            result["transparent_intended_information_solver"]["combined_regulation"],
            1.0,
        )


if __name__ == "__main__":
    unittest.main()
