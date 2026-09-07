import unittest

from project_theta.config import RunConfig, apply_condition


class AblationTests(unittest.TestCase):
    def test_named_ablations_change_mechanism(self):
        base = RunConfig()
        self.assertFalse(apply_condition(base, "no_memory").architecture.memory_enabled)
        self.assertFalse(apply_condition(base, "no_workspace").architecture.workspace_enabled)
        self.assertEqual(
            apply_condition(base, "generic_table").architecture.binding_representation,
            "generic",
        )
        self.assertEqual(
            apply_condition(base, "misattributed_table").architecture.binding_content,
            "inverted",
        )
        self.assertEqual(
            apply_condition(base, "unbound_binding").architecture.continuity_binding_mode,
            "unbound",
        )
        self.assertEqual(
            apply_condition(base, "continuity_reset").architecture.continuity_binding_mode,
            "reset",
        )
        self.assertEqual(
            apply_condition(base, "permuted_continuity").architecture.continuity_binding_mode,
            "permuted",
        )
        self.assertFalse(
            apply_condition(base, "register_hidden").architecture.continuity_register_visible
        )
        self.assertFalse(
            apply_condition(base, "raw_role_memory_hidden").architecture.raw_role_memory_visible
        )
        self.assertFalse(apply_condition(base, "no_self_model").architecture.self_model_enabled)
        self.assertEqual(apply_condition(base, "no_body").body.signal_mode, "absent")
        self.assertFalse(apply_condition(base, "no_body").body.body_enabled)
        self.assertEqual(apply_condition(base, "shuffled_interoception").body.signal_mode, "shuffled")
        self.assertEqual(apply_condition(base, "sham_body").body.signal_mode, "sham")
        self.assertEqual(apply_condition(base, "matched_sham").body.signal_mode, "matched_sham")
        self.assertFalse(apply_condition(base, "no_recurrence").architecture.recurrence_enabled)
        self.assertFalse(apply_condition(base, "no_persistence").architecture.persistent_state)

    def test_unknown_condition_fails(self):
        with self.assertRaises(ValueError):
            apply_condition(RunConfig(), "placebo_magic")


if __name__ == "__main__":
    unittest.main()
