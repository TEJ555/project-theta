import unittest

from project_theta.analysis import format_summary, summarize_runs
from project_theta.types import RunSummary


class AnalysisTests(unittest.TestCase):
    def test_paired_effect_and_small_sample_warning(self):
        runs = []
        for seed in (1, 2, 3):
            runs.append(RunSummary(f"f{seed}", "memory_ablation", "full", seed, 24, False, None,
                                   {"forced_choice_accuracy": 1.0}))
            runs.append(RunSummary(f"a{seed}", "memory_ablation", "no_memory", seed, 24, False, None,
                                   {"forced_choice_accuracy": 0.5}))
        summary = summarize_runs(runs)
        self.assertEqual(summary["paired_comparisons"][0]["mean_difference"], 0.5)
        self.assertTrue(any("Pilot-sized" in warning for warning in summary["warnings"]))
        self.assertIn("memory_ablation", format_summary(summary))


if __name__ == "__main__":
    unittest.main()
