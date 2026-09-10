import json
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from project_theta.audits import (
    audit_adversarial_schedules,
    audit_causal_role_binding_v5_schedules,
    audit_controlled_schedules,
    audit_endogenous_agency_v6_schedules,
    audit_independent_schedules,
    audit_metadata_shortcuts,
    audit_self_model_binding_v3_schedules,
    audit_self_model_binding_v4_schedules,
)
from project_theta.config import RunConfig
from project_theta.harness import ExperimentHarness
from project_theta.trials import build_trials


class ControlledTrialTests(unittest.TestCase):
    def test_consciousness_indicator_schedules_are_balanced_and_blinded(self):
        for experiment in (
            "self_vs_other",
            "temporal_self",
            "self_model_binding_v2",
            "temporal_binding_v2",
        ):
            with self.subTest(experiment=experiment):
                result = audit_controlled_schedules(experiment, [1811, 1931, 2053])
                self.assertEqual(result["status"], "pass")

    def test_independent_schedule_has_independent_balanced_items(self):
        result = audit_independent_schedules([401, 402, 403, 404])
        self.assertEqual(result["status"], "pass")
        trials = build_trials("independent_theta", 401)
        probes = [trial for trial in trials if trial.phase == "probe"]
        self.assertEqual(len(trials), 60)
        self.assertEqual(len(probes), 12)
        self.assertEqual(len({(trial.block, trial.family) for trial in probes}), 12)

    def test_self_model_binding_v3_schedule_is_independent_and_blinded(self):
        result = audit_self_model_binding_v3_schedules([3527, 3631, 3733])
        self.assertEqual(result["status"], "pass")

    def test_v4_schedule_is_blinded_and_shortcut_resistant(self):
        result = audit_self_model_binding_v4_schedules([5209, 5303, 5413])
        self.assertEqual(result["status"], "pass")
        shortcut = audit_metadata_shortcuts("self_model_binding_v4")
        self.assertEqual(shortcut["status"], "pass")
        self.assertLessEqual(max(shortcut["scores"].values()), 0.60)
        for trial in build_trials("self_model_binding_v4", 5209):
            self.assertNotIn("trial_id", trial.public_task())

    def test_independent_full_separates_from_exact_sham(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "independent.sqlite")
            full = harness.run(replace(
                RunConfig(), experiment="independent_theta", condition="full", seed=401
            ))
            sham = harness.run(replace(
                RunConfig(), experiment="independent_theta", condition="matched_sham", seed=401
            ))
            self.assertEqual(full.metrics["post_update_accuracy"], 1.0)
            self.assertEqual(full.metrics["stable_post_accuracy"], 1.0)
            self.assertEqual(full.metrics["reversed_post_accuracy"], 1.0)
            self.assertEqual(full.metrics["reassigned_post_accuracy"], 1.0)
            self.assertEqual(sham.metrics["post_update_accuracy"], 0.5)
            self.assertEqual(sham.metrics["stable_post_accuracy"], 0.5)
            self.assertEqual(sham.metrics["reversed_post_accuracy"], 0.5)
            self.assertEqual(sham.metrics["reassigned_post_accuracy"], 0.5)
            self.assertEqual(full.metrics["independent_probe_items"], 12)

    def test_exact_sham_is_equal_in_model_visible_stage_summaries(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "sham.sqlite"
            ExperimentHarness(database).run(replace(
                RunConfig(), experiment="independent_theta", condition="matched_sham", seed=401
            ))
            connection = sqlite3.connect(database)
            contexts = [json.loads(row[0]) for row in connection.execute(
                "SELECT context_json FROM steps ORDER BY tick"
            )]
            connection.close()
            for stage in ("stage_a", "stage_b"):
                context = next(
                    item for item in contexts
                    if item["observation"]["task"].get("stage") == stage
                    and item["observation"]["task"]["phase"] == "probe"
                )
                associations = next(
                    item["content"] for item in context["workspace_broadcast"]
                    if item["source"] == "learned_associations"
                )
                summaries = associations["by_stage_cue"][stage].values()
                self.assertTrue(summaries)
                self.assertEqual({row["mean_signal"] for row in summaries}, {0.4})
                self.assertEqual({row["mean_signal_delta"] for row in summaries}, {0.4})

    def test_independent_shortcut_baselines_do_not_clear_the_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "shortcuts.sqlite")

            def run(model: str, condition: str = "full"):
                return harness.run(replace(
                    RunConfig(),
                    experiment="independent_theta",
                    condition=condition,
                    seed=401,
                    model=model,
                ))

            for model in (
                "fixed-left-baseline-v1",
                "fixed-right-baseline-v1",
                "stage-only-baseline-v1",
            ):
                self.assertEqual(run(model).metrics["post_update_accuracy"], 0.5)

            reversal = run("global-reversal-baseline-v1")
            self.assertEqual(reversal.metrics["post_update_accuracy"], 0.5)
            self.assertEqual(reversal.metrics["stable_post_accuracy"], 0.0)
            self.assertEqual(reversal.metrics["reversed_post_accuracy"], 1.0)
            self.assertEqual(reversal.metrics["reassigned_post_accuracy"], 0.5)

            self.assertEqual(
                run("cue-recency-baseline-v1").metrics["post_update_accuracy"], 1.0
            )
            self.assertEqual(
                run("cue-recency-baseline-v1", "matched_sham").metrics[
                    "post_update_accuracy"
                ],
                0.5,
            )

    def test_adversarial_schedule_is_balanced_reversed_and_blinded(self):
        result = audit_adversarial_schedules([91, 92, 93, 94])
        self.assertEqual(result["status"], "pass")
        compact = audit_adversarial_schedules([301, 302, 303, 304], "compact")
        self.assertEqual(compact["status"], "pass")

    def test_adversarial_full_and_simple_baselines_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "adversarial.sqlite")
            full = harness.run(replace(
                RunConfig(), experiment="adversarial_theta", condition="full", seed=101
            ))
            no_body = harness.run(replace(
                RunConfig(), experiment="adversarial_theta", condition="no_body", seed=101
            ))
            fixed = harness.run(replace(
                RunConfig(),
                experiment="adversarial_theta",
                condition="full",
                seed=101,
                model="fixed-left-baseline-v1",
            ))
            self.assertEqual(full.metrics["pre_update_accuracy"], 1.0)
            self.assertEqual(full.metrics["post_update_accuracy"], 1.0)
            self.assertEqual(no_body.metrics["post_update_accuracy"], 0.5)
            self.assertEqual(fixed.metrics["post_update_accuracy"], 0.5)

    def test_adversarial_context_hides_condition_map_and_experiment_name(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "adversarial.sqlite"
            ExperimentHarness(database).run(replace(
                RunConfig(), experiment="adversarial_theta", condition="sham_body", seed=91
            ))
            connection = sqlite3.connect(database)
            contexts = [row[0] for row in connection.execute("SELECT context_json FROM steps")]
            connection.close()
            joined = "\n".join(contexts).lower()
            for forbidden in (
                "adversarial_theta", "correct_action", "sham_perturbation", '"condition"', '"seed"'
            ):
                self.assertNotIn(forbidden, joined)

    def test_probe_sides_are_balanced_and_scoring_is_not_public(self):
        trials = build_trials("private_theta", 11)
        probes = [trial for trial in trials if trial.phase == "probe"]
        self.assertEqual(sum(trial.correct_action == "choose_left" for trial in probes), 6)
        for trial in probes:
            public = trial.public_task()
            self.assertNotIn("correct_action", public)
            self.assertNotIn("perturbation", public)

    def test_full_learns_and_memory_ablation_is_at_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "study.sqlite")
            full = harness.run(replace(RunConfig(), experiment="memory_ablation", condition="full"))
            ablated = harness.run(
                replace(RunConfig(), experiment="memory_ablation", condition="no_memory")
            )
            self.assertEqual(full.metrics["forced_choice_accuracy"], 1.0)
            self.assertEqual(ablated.metrics["forced_choice_accuracy"], 0.5)

    def test_hidden_scoring_key_is_separate_from_adapter_context(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "study.sqlite"
            ExperimentHarness(database).run(RunConfig())
            connection = sqlite3.connect(database)
            context_json, hidden_json = connection.execute(
                "SELECT context_json, hidden_world_json FROM steps WHERE tick=12"
            ).fetchone()
            connection.close()
            context = json.loads(context_json)
            hidden = json.loads(hidden_json)
            self.assertNotIn("correct_action", context_json)
            self.assertIn("correct_action", hidden)
            self.assertNotIn("condition", context)
            self.assertNotIn("seed", context)

    def test_temporal_controls_are_discriminative(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "temporal.sqlite")
            full = harness.run(replace(RunConfig(), experiment="temporal_self", condition="full"))
            no_persistence = harness.run(
                replace(RunConfig(), experiment="temporal_self", condition="no_persistence")
            )
            self.assertEqual(full.metrics["temporal_choice_accuracy"], 1.0)
            self.assertEqual(no_persistence.metrics["temporal_choice_accuracy"], 0.5)

    def test_self_model_binding_v2_is_selectively_discriminative(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "self-model-v2.sqlite"
            harness = ExperimentHarness(database)
            full = harness.run(replace(
                RunConfig(), experiment="self_model_binding_v2", condition="full", seed=811
            ))
            no_self_model = harness.run(replace(
                RunConfig(),
                experiment="self_model_binding_v2",
                condition="no_self_model",
                seed=811,
            ))
            no_workspace = harness.run(replace(
                RunConfig(),
                experiment="self_model_binding_v2",
                condition="no_workspace",
                seed=811,
            ))
            self.assertEqual(full.metrics["source_binding_accuracy"], 1.0)
            self.assertEqual(no_self_model.metrics["source_binding_accuracy"], 0.5)
            self.assertEqual(no_workspace.metrics["source_binding_accuracy"], 0.5)

            connection = sqlite3.connect(database)
            contexts = [
                json.loads(row[0])
                for row in connection.execute(
                    "SELECT context_json FROM steps WHERE context_json LIKE '%source_binding_probe%'"
                )
            ]
            connection.close()
            self.assertTrue(contexts)
            for context in contexts:
                memories = next(
                    (
                        item["content"] for item in context["workspace_broadcast"]
                        if item["source"] == "memory"
                    ),
                    [],
                )
                self.assertTrue(all("owner" not in item for item in memories))

    def test_self_model_binding_v3_defeats_single_pair_shortcut(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "self-model-v3.sqlite")
            full = harness.run(replace(
                RunConfig(), experiment="self_model_binding_v3", condition="full", seed=3527
            ))
            no_self_model = harness.run(replace(
                RunConfig(),
                experiment="self_model_binding_v3",
                condition="no_self_model",
                seed=3527,
            ))
            no_workspace = harness.run(replace(
                RunConfig(),
                experiment="self_model_binding_v3",
                condition="no_workspace",
                seed=3527,
            ))
            self.assertEqual(full.metrics["source_binding_accuracy"], 1.0)
            self.assertEqual(no_self_model.metrics["source_binding_accuracy"], 0.5)
            self.assertEqual(no_workspace.metrics["source_binding_accuracy"], 0.5)

    def test_v4_information_matched_full_and_generic_inputs_are_equal(self):
        with tempfile.TemporaryDirectory() as directory:
            full_db = Path(directory) / "full.sqlite"
            generic_db = Path(directory) / "generic.sqlite"
            seed = 5209
            full = ExperimentHarness(full_db).run(replace(
                RunConfig(), experiment="self_model_binding_v4", condition="full", seed=seed
            ))
            generic = ExperimentHarness(generic_db).run(replace(
                RunConfig(),
                experiment="self_model_binding_v4",
                condition="generic_table",
                seed=seed,
            ))
            self.assertEqual(full.metrics["source_binding_accuracy"], 1.0)
            self.assertEqual(generic.metrics["source_binding_accuracy"], 1.0)

            def probe_contexts(path: Path):
                connection = sqlite3.connect(path)
                rows = [row[0] for row in connection.execute(
                    "SELECT context_json FROM steps WHERE context_json LIKE '%source_binding_probe%' ORDER BY tick"
                )]
                connection.close()
                return rows

            self.assertEqual(probe_contexts(full_db), probe_contexts(generic_db))

    def test_v4_wrong_content_controls_and_lookup_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "v4.sqlite")
            seed = 5209
            wrong = harness.run(replace(
                RunConfig(),
                experiment="self_model_binding_v4",
                condition="misattributed_table",
                seed=seed,
            ))
            permuted = harness.run(replace(
                RunConfig(),
                experiment="self_model_binding_v4",
                condition="permuted_table",
                seed=seed,
            ))
            self.assertEqual(wrong.metrics["source_binding_accuracy"], 0.0)
            self.assertLess(permuted.metrics["source_binding_accuracy"], 1.0)

    def test_v4_probe_only_profile_cuts_calls_without_changing_scripted_probes(self):
        with tempfile.TemporaryDirectory() as directory:
            full_db = Path(directory) / "all.sqlite"
            fast_db = Path(directory) / "fast.sqlite"
            base = replace(
                RunConfig(), experiment="self_model_binding_v4", condition="full", seed=5209
            )
            all_trials = ExperimentHarness(full_db).run(base)
            probe_only = ExperimentHarness(fast_db).run(replace(
                base, inference_profile="probes_only"
            ))
            self.assertEqual(all_trials.metrics["source_binding_accuracy"], 1.0)
            self.assertEqual(probe_only.metrics["source_binding_accuracy"], 1.0)
            self.assertEqual(probe_only.metrics["model_calls"], 12)
            self.assertEqual(probe_only.metrics["inference_skipped"], 48)
            connection = sqlite3.connect(fast_db)
            api_calls = connection.execute("SELECT COUNT(*) FROM api_calls").fetchone()[0]
            connection.close()
            self.assertEqual(api_calls, 12)

    def test_v5_schedule_is_balanced_blinded_and_uses_novel_transfer_routes(self):
        result = audit_causal_role_binding_v5_schedules([7027, 7121, 7229])
        self.assertEqual(result["status"], "pass")
        trials = build_trials("causal_role_binding_v5", 7027)
        self.assertEqual(len(trials), 60)
        public_text = json.dumps([trial.public_task() for trial in trials]).lower()
        for forbidden in (
            "trial_id",
            "correct_action",
            "causal_role_binding_v5",
            "continuity",
            '"owner"',
        ):
            self.assertNotIn(forbidden, public_text)

    def test_v5_role_bound_transfers_while_unbound_only_retrieves_exact_routes(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "v5.sqlite")
            base = replace(
                RunConfig(),
                experiment="causal_role_binding_v5",
                seed=7027,
                inference_profile="probes_only",
            )
            full = harness.run(replace(base, condition="full"))
            unbound = harness.run(replace(base, condition="unbound_binding"))
            reset = harness.run(replace(base, condition="continuity_reset"))

            self.assertEqual(full.metrics["exact_binding_accuracy"], 1.0)
            self.assertEqual(full.metrics["causal_transfer_accuracy"], 1.0)
            self.assertEqual(unbound.metrics["exact_binding_accuracy"], 1.0)
            self.assertEqual(unbound.metrics["causal_transfer_accuracy"], 0.5)
            self.assertEqual(reset.metrics["exact_binding_accuracy"], 0.5)
            self.assertEqual(reset.metrics["causal_transfer_accuracy"], 0.5)
            self.assertEqual(full.metrics["model_calls"], 12)
            self.assertEqual(full.metrics["inference_skipped"], 48)

    def test_v5_conditions_match_raw_context_except_causal_register_values(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v5.sqlite"
            harness = ExperimentHarness(database)
            base = replace(
                RunConfig(),
                experiment="causal_role_binding_v5",
                seed=7027,
                inference_profile="probes_only",
            )
            summaries = {
                condition: harness.run(replace(base, condition=condition))
                for condition in ("full", "unbound_binding", "continuity_reset")
            }

            def normalized_contexts(run_id: str):
                connection = sqlite3.connect(database)
                contexts = [
                    json.loads(row[0])
                    for row in connection.execute(
                        "SELECT context_json FROM steps WHERE run_id=? ORDER BY tick",
                        (run_id,),
                    )
                ]
                connection.close()
                for context in contexts:
                    for item in context["workspace_broadcast"]:
                        if item["source"] == "state_register":
                            item["content"]["predictions"] = "condition-specific-causal-output"
                return contexts

            reference = normalized_contexts(summaries["full"].run_id)
            self.assertEqual(reference, normalized_contexts(summaries["unbound_binding"].run_id))
            self.assertEqual(reference, normalized_contexts(summaries["continuity_reset"].run_id))

    def test_v5_diagnostic_controls_isolate_register_memory_and_pointer_content(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "v5-controls.sqlite"
            harness = ExperimentHarness(database)
            base = replace(
                RunConfig(),
                experiment="causal_role_binding_v5",
                seed=7321,
                inference_profile="probes_only",
            )
            results = {
                condition: harness.run(replace(base, condition=condition))
                for condition in (
                    "full",
                    "permuted_continuity",
                    "register_hidden",
                    "raw_role_memory_hidden",
                )
            }

            self.assertEqual(results["full"].metrics["causal_transfer_accuracy"], 1.0)
            self.assertEqual(
                results["permuted_continuity"].metrics["exact_binding_accuracy"], 1.0
            )
            self.assertEqual(
                results["permuted_continuity"].metrics["causal_transfer_accuracy"], 0.0
            )
            self.assertEqual(results["register_hidden"].metrics["exact_binding_accuracy"], 0.5)
            self.assertEqual(
                results["register_hidden"].metrics["causal_transfer_accuracy"], 0.5
            )
            self.assertEqual(
                results["raw_role_memory_hidden"].metrics["exact_binding_accuracy"], 1.0
            )
            self.assertEqual(
                results["raw_role_memory_hidden"].metrics["causal_transfer_accuracy"], 1.0
            )

            connection = sqlite3.connect(database)
            registers = {}
            for condition, summary in results.items():
                context = json.loads(connection.execute(
                    """
                    SELECT context_json FROM steps
                    WHERE run_id=? AND context_json LIKE '%causal_transfer_probe%'
                    ORDER BY tick LIMIT 1
                    """,
                    (summary.run_id,),
                ).fetchone()[0])
                registers[condition] = next(
                    item["content"]
                    for item in context["workspace_broadcast"]
                    if item["source"] == "state_register"
                )
            connection.close()

            for field in (
                "entry_count",
                "update_count",
                "capacity",
                "actor_entry_count",
                "route_entry_count",
            ):
                self.assertEqual(
                    {register[field] for register in registers.values()},
                    {registers["full"][field]},
                )

    def test_v6_schedule_removes_answer_table_and_requires_intervention_structure(self):
        result = audit_endogenous_agency_v6_schedules([1001, 1002, 1003])
        self.assertEqual(result["status"], "pass")
        trials = build_trials("endogenous_agency_v6", 1001)
        self.assertEqual(len(trials), 18)
        public_text = json.dumps([trial.public_task() for trial in trials]).lower()
        for forbidden in ("state_register", '"predictions"', '"v:0"', '"v:1"'):
            self.assertNotIn(forbidden, public_text)

    def test_v6_model_authored_state_and_diagnostic_controls(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "v6.sqlite")
            base = replace(
                RunConfig(),
                experiment="endogenous_agency_v6",
                seed=1001,
                inference_profile="all_trials",
            )
            summaries = {
                condition: harness.run(replace(base, condition=condition))
                for condition in (
                    "full",
                    "evidence_only",
                    "journal_only",
                    "permuted_journal",
                    "neutral_journal",
                )
            }
            for condition in ("full", "evidence_only", "journal_only", "neutral_journal"):
                self.assertEqual(summaries[condition].metrics["agency_exact_accuracy"], 1.0)
                self.assertEqual(summaries[condition].metrics["agency_transfer_accuracy"], 1.0)
                self.assertEqual(summaries[condition].metrics["authored_state_accuracy"], 1.0)
                self.assertEqual(summaries[condition].metrics["model_calls"], 18)
            self.assertEqual(
                summaries["permuted_journal"].metrics["agency_exact_accuracy"], 0.0
            )
            self.assertEqual(
                summaries["permuted_journal"].metrics["agency_transfer_accuracy"], 0.0
            )

    def test_v6_pooled_association_baseline_is_exactly_balanced(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "v6-pooled.sqlite")
            config = replace(
                RunConfig(),
                experiment="endogenous_agency_v6",
                condition="journal_only",
                model="pooled-correlation-baseline-v1",
                seed=1001,
            )
            summary = harness.run(config)
            self.assertEqual(summary.metrics["authored_state_accuracy"], 0.0)
            self.assertEqual(summary.metrics["agency_exact_accuracy"], 0.5)
            self.assertEqual(summary.metrics["agency_transfer_accuracy"], 0.5)

    def test_temporal_binding_v2_is_selectively_discriminative(self):
        with tempfile.TemporaryDirectory() as directory:
            harness = ExperimentHarness(Path(directory) / "temporal-v2.sqlite")
            full = harness.run(replace(
                RunConfig(), experiment="temporal_binding_v2", condition="full", seed=823
            ))
            no_persistence = harness.run(replace(
                RunConfig(),
                experiment="temporal_binding_v2",
                condition="no_persistence",
                seed=823,
            ))
            no_recurrence = harness.run(replace(
                RunConfig(),
                experiment="temporal_binding_v2",
                condition="no_recurrence",
                seed=823,
            ))
            self.assertEqual(full.metrics["temporal_choice_accuracy"], 1.0)
            self.assertEqual(no_persistence.metrics["temporal_choice_accuracy"], 0.5)
            self.assertEqual(no_recurrence.metrics["temporal_choice_accuracy"], 0.5)


if __name__ == "__main__":
    unittest.main()
