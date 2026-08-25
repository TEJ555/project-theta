import unittest

from project_theta.metrics import compute_metrics


class MetricTests(unittest.TestCase):
    def test_metrics_are_typed_and_no_consciousness_score_exists(self):
        rows = [
            {"tick": i, "position": [i, 0], "signal": i / 10, "damage": float(i == 1),
             "contact": i == 1, "delayed_exposure": False, "resource_consumed": False,
             "reward": 0.0, "integrity": 1.0, "prediction": i / 10, "self_report": "",
             "expected_source": None}
            for i in range(5)
        ]
        metrics = compute_metrics(rows, 2, {})
        self.assertIn("prediction_mae", metrics)
        self.assertNotIn("consciousness_score", metrics)


if __name__ == "__main__":
    unittest.main()

