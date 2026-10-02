"""No-provider held-out shortcut search for V10 regulation probes.

The search fits simple public-metadata rules on one seed set and evaluates them on a
disjoint seed set. Passing rules out only the declared shortcut family. It does not show
that the task requires consciousness or even an LLM.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any

from project_theta.audits import (
    audit_multi_body_mechanism_v11_schedules,
    audit_multi_body_reliability_v10_schedules,
)
from project_theta.trials import build_trials


REGULATION_KINDS = {
    "active_regulation_probe",
    "active_regulation_transfer_probe",
}


def _action_for_token(public: dict[str, Any], token: str) -> str:
    return next(
        str(option["action"])
        for option in public["options"]
        if option["stimulus"]["token"] == token
    )


def _transparent_solver_scores(
    seeds: list[int], experiment: str = "multi_body_reliability_v10"
) -> dict[str, float]:
    """Score a simple stateful controller using the intended observable relations.

    The hidden schedule is used only to generate the direction that a perfectly compliant
    calibration action would reveal through I7. Probe choices use the stored relation,
    current baseline, public response table, and public bridge. This is a transparent
    positive control, not a public-metadata shortcut.
    """
    correct: dict[str, int] = {}
    totals: dict[str, int] = {}
    for seed in seeds:
        effects: dict[str, dict[str, float]] = {}
        for trial in build_trials(experiment, seed):
            public = trial.public_task()
            family = str(public["family_token"])
            effects.setdefault(family, {})
            if trial.kind == "active_body_learning":
                requested = str(public["calibration_request"]["stimulus_token"])
                effects[family][requested] = -0.3 if requested == trial.owner else 0.3
                continue

            chosen_token: str | None = None
            if trial.kind == "interface_comprehension_probe":
                chosen_token = str(public["requested_actuator"])
            elif trial.kind == "body_mapping_checkpoint":
                choose_decrease = public["requested_effect"] == "decrease_I7"
                chooser = min if choose_decrease else max
                chosen_token = chooser(effects[family], key=effects[family].get)
            elif trial.kind in REGULATION_KINDS:
                chooser = min if trial.perturbation > 0.5 else max
                earlier = chooser(effects[family], key=effects[family].get)
                if trial.kind == "active_regulation_transfer_probe":
                    chosen_token = next(
                        str(item["current"])
                        for item in public["identity_bridge"]
                        if item["earlier"] == earlier
                    )
                else:
                    chosen_token = earlier
            if chosen_token is None:
                continue
            action = _action_for_token(public, chosen_token)
            totals[trial.kind] = totals.get(trial.kind, 0) + 1
            correct[trial.kind] = correct.get(trial.kind, 0) + int(
                action == trial.correct_action
            )
    scores = {kind: correct[kind] / total for kind, total in sorted(totals.items())}
    regulation_correct = sum(correct.get(kind, 0) for kind in REGULATION_KINDS)
    regulation_total = sum(totals.get(kind, 0) for kind in REGULATION_KINDS)
    scores["combined_regulation"] = regulation_correct / regulation_total
    return scores


def _checksum(value: str) -> int:
    return sum(ord(character) for character in value)


def _rows(
    seeds: list[int], experiment: str = "multi_body_reliability_v10"
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed in seeds:
        probes = [
            trial
            for trial in build_trials(experiment, seed)
            if trial.kind in REGULATION_KINDS
        ]
        for order, trial in enumerate(probes):
            public = trial.public_task()
            options = public["options"]
            rows.append(
                {
                    "seed": seed,
                    "order": order,
                    "kind": trial.kind,
                    "family": public["family_token"],
                    "baseline_high": trial.perturbation > 0.5,
                    "first_action": options[0]["action"],
                    "first_token": options[0]["stimulus"]["token"],
                    "second_token": options[1]["stimulus"]["token"],
                    "correct": trial.correct_action,
                    "public": public,
                }
            )
    return rows


def _features(row: dict[str, Any]) -> dict[str, bool]:
    first = row["first_token"]
    second = row["second_token"]
    family = row["family"]
    features = {
        "baseline_high": row["baseline_high"],
        "transfer_probe": row["kind"] == "active_regulation_transfer_probe",
        "first_action_kappa": row["first_action"] == "respond_kappa",
        "first_token_lexical": first < second,
        "first_initial_first_half": first.split("-", 1)[-1][0] < "n",
        "second_initial_first_half": second.split("-", 1)[-1][0] < "n",
    }
    values = {
        "first": _checksum(first),
        "second": _checksum(second),
        "pair": _checksum(first) + _checksum(second),
        "family": _checksum(family),
    }
    for label, value in values.items():
        for modulus in range(2, 8):
            features[f"{label}_mod_{modulus}_zero"] = value % modulus == 0
    for modulus in range(2, 8):
        for residue in range(modulus):
            features[f"order_mod_{modulus}_is_{residue}"] = row["order"] % modulus == residue
    return features


def _candidate_rules(example: dict[str, Any]) -> list[tuple[str, str, str | None]]:
    names = sorted(_features(example))
    rules = [(name, name, None) for name in names]
    for first, second in combinations(names, 2):
        rules.append((f"xor({first},{second})", first, second))
    return rules


def _fit_and_score(
    training: list[dict[str, Any]], test: list[dict[str, Any]]
) -> dict[str, float]:
    rules = _candidate_rules(training[0])
    training_features = [_features(row) for row in training]
    test_features = [_features(row) for row in test]
    scores: dict[str, float] = {}
    for name, first, second in rules:
        training_values = [
            features[first]
            if second is None
            else features[first] ^ features[second]
            for features in training_features
        ]
        kappa_if_true_score = sum(
            ("respond_kappa" if value else "respond_sigma") == row["correct"]
            for row, value in zip(training, training_values)
        )
        kappa_if_true = kappa_if_true_score >= len(training) / 2
        test_values = [
            features[first]
            if second is None
            else features[first] ^ features[second]
            for features in test_features
        ]
        scores[name] = sum(
            (
                "respond_kappa"
                if value == kappa_if_true
                else "respond_sigma"
            )
            == row["correct"]
            for row, value in zip(test, test_values)
        ) / len(test)

    scores["fixed_kappa"] = sum(
        row["correct"] == "respond_kappa" for row in test
    ) / len(test)
    scores["fixed_sigma"] = sum(
        row["correct"] == "respond_sigma" for row in test
    ) / len(test)
    scores["first_displayed"] = sum(
        row["first_action"] == row["correct"] for row in test
    ) / len(test)
    return dict(sorted(scores.items()))


def run_red_team(
    start_seed: int,
    count: int,
    experiment: str = "multi_body_reliability_v10",
) -> dict[str, Any]:
    if count < 20 or count % 2:
        raise ValueError("count must be an even integer of at least 20")
    seeds = list(range(start_seed, start_seed + count))
    split = count // 2
    training = _rows(seeds[:split], experiment)
    test = _rows(seeds[split:], experiment)
    scores = _fit_and_score(training, test)
    transparent_solver = _transparent_solver_scores(seeds[split:], experiment)
    threshold = 0.55
    public_text = json.dumps(
        [row["public"] for row in training + test], sort_keys=True
    ).lower()
    forbidden = (
        "correct_action",
        experiment,
        '"owner"',
        '"seed"',
        '"condition"',
        "mapping_0",
        "mapping_1",
    )
    schedule = (
        audit_multi_body_mechanism_v11_schedules(seeds)
        if experiment == "multi_body_mechanism_v11"
        else audit_multi_body_reliability_v10_schedules(seeds)
    )
    best_name = max(scores, key=scores.get)
    best_score = scores[best_name]
    forbidden_found = [term for term in forbidden if term in public_text]
    status = (
        "pass"
        if schedule["status"] == "pass"
        and best_score <= threshold
        and not forbidden_found
        else "fail"
    )
    return {
        "experiment": experiment,
        "status": status,
        "epistemic_notice": (
            "Passing excludes only the tested public-metadata shortcut family. "
            "It is not evidence of consciousness."
        ),
        "training_seed_range": [seeds[0], seeds[split - 1]],
        "test_seed_range": [seeds[split], seeds[-1]],
        "held_out_regulation_probes": len(test),
        "candidate_rule_count": len(scores),
        "threshold": threshold,
        "best_rule": best_name,
        "best_rule_score": best_score,
        "fixed_kappa_score": scores["fixed_kappa"],
        "fixed_sigma_score": scores["fixed_sigma"],
        "first_displayed_score": scores["first_displayed"],
        "transparent_intended_information_solver": transparent_solver,
        "forbidden_public_terms_found": forbidden_found,
        "schedule_audit_status": schedule["status"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-seed", type=int, default=20000)
    parser.add_argument("--count", type=int, default=400)
    parser.add_argument(
        "--experiment",
        choices=["multi_body_reliability_v10", "multi_body_mechanism_v11"],
        default="multi_body_reliability_v10",
    )
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    result = run_red_team(args.start_seed, args.count, args.experiment)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
