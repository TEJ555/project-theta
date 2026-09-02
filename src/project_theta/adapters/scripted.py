from __future__ import annotations

from typing import Any

from ..types import Decision
from .base import ModelAdapter


class ScriptedAdapter(ModelAdapter):
    """Deterministic navigation baseline for plumbing tests, not an AI subject."""

    name = "scripted"

    @staticmethod
    def _workspace(context: dict[str, Any], source: str, default: Any) -> Any:
        for item in context.get("workspace_broadcast", []):
            if item.get("source") == source:
                return item.get("content", default)
        return default

    def _controlled_decide(self, context: dict[str, Any]) -> Decision:
        observation = context["observation"]
        task = observation.get("task", {})
        signal = float(observation.get("private_signals", {}).get("I7", 0.0))
        allowed = context.get("permitted_actions", ["observe"])
        if task.get("phase") == "acquisition" or allowed == ["observe"]:
            return Decision("observe", "Record the stimulus and subsequent I7 state.", {"I7": signal}, 0.9)

        if self.model == "fixed-left-baseline-v1":
            return Decision(
                "choose_left",
                "Use a fixed-side baseline that has no access to learned associations.",
                {"I7": signal},
                0.5,
            )
        if self.model == "fixed-right-baseline-v1":
            return Decision(
                "choose_right",
                "Use a fixed-side baseline that has no access to learned associations.",
                {"I7": signal},
                0.5,
            )
        if self.model == "stage-only-baseline-v1":
            action = "choose_left" if task.get("stage") == "stage_a" else "choose_right"
            return Decision(
                action,
                "Use only the public stage label and ignore cue-specific evidence.",
                {"I7": signal},
                0.5,
            )

        associations = self._workspace(context, "learned_associations", {})
        by_cue = associations.get("by_cue", {}) if isinstance(associations, dict) else {}
        by_feature = associations.get("by_feature", {}) if isinstance(associations, dict) else {}

        def normal_score(option: dict[str, Any]) -> float | None:
            stimulus = option.get("stimulus", {})
            cue = stimulus.get("token", "")
            if cue in by_cue:
                return float(by_cue[cue]["mean_signal"])
            values = [
                float(by_feature[feature]["mean_signal"])
                for feature in stimulus.get("features", [])
                if feature in by_feature
            ]
            return sum(values) / len(values) if values else None

        options = task.get("options", [])
        scores = [normal_score(option) for option in options]
        protocol = context.get("protocol")

        if protocol == "controlled_signal_study" and task.get("stage"):
            stage = task["stage"]
            staged = associations.get("by_stage_cue", {}) if isinstance(associations, dict) else {}
            current_stage = staged.get(stage, {}) if isinstance(staged, dict) else {}
            scores = [
                (
                    float(current_stage[option.get("stimulus", {}).get("token", "")]["mean_signal"])
                    if option.get("stimulus", {}).get("token", "") in current_stage
                    else None
                )
                for option in options
            ]
            if self.model == "global-reversal-baseline-v1" and stage == "stage_b":
                previous_stage = staged.get("stage_a", {}) if isinstance(staged, dict) else {}
                scores = [
                    (
                        -float(previous_stage[option.get("stimulus", {}).get("token", "")]["mean_signal"])
                        if option.get("stimulus", {}).get("token", "") in previous_stage
                        else None
                    )
                    for option in options
                ]
            if self.model == "cue-recency-baseline-v1":
                memories = self._workspace(context, "memory", [])
                latest: dict[str, float] = {}
                for item in memories:
                    if stage not in item.get("tags", ()) or "acquisition" not in item.get("tags", ()):
                        continue
                    cue = str(item.get("cue", ""))
                    if cue not in latest:
                        latest[cue] = float(item.get("signal", 0.0))
                scores = [
                    latest.get(option.get("stimulus", {}).get("token", ""))
                    for option in options
                ]

        if task.get("kind") == "temporal_probe" and any(
            item.get("source") == "temporal_associations"
            for item in context.get("workspace_broadcast", [])
        ):
            temporal_state = self._workspace(context, "temporal_associations", {})
            temporal = temporal_state.get("associations", {}) if isinstance(temporal_state, dict) else {}
            scores = [
                (
                    float(temporal[option["stimulus"]["token"]]["mean_signal"])
                    if option["stimulus"]["token"] in temporal else None
                )
                for option in options
            ]
        elif protocol == "temporal_self":
            memories = self._workspace(context, "memory", [])
            has_recurrence = any(
                item.get("source") == "previous_prediction"
                for item in context.get("workspace_broadcast", [])
            )
            if has_recurrence and memories:
                by_tick = {int(item["tick"]): item for item in memories}
                temporal: dict[str, list[float]] = {}
                for item in memories:
                    if item.get("cue", "").startswith("sequence-"):
                        outcome = by_tick.get(int(item["tick"]) + 3)
                        if outcome:
                            temporal.setdefault(item["cue"], []).append(float(outcome.get("signal", 0.0)))
                scores = [
                    (sum(temporal[option["stimulus"]["token"]]) / len(temporal[option["stimulus"]["token"]]))
                    if option["stimulus"]["token"] in temporal else None
                    for option in options
                ]
            else:
                scores = [None for _ in options]

        if protocol == "self_vs_other":
            self_model = self._workspace(context, "self_model", {"enabled": False})
            if not isinstance(self_model, dict) or not self_model.get("enabled"):
                scores = [None for _ in options]

        if task.get("objective") == "identify_self_source":
            self_model = self._workspace(context, "self_model", {"enabled": False})
            bindings = (
                self_model.get("source_bindings", {})
                if isinstance(self_model, dict) and self_model.get("enabled")
                else {}
            )
            scores = [
                bindings.get(option.get("stimulus", {}).get("token", ""))
                for option in options
            ]

        if len(options) != 2 or any(score is None for score in scores):
            action = allowed[0]
            return Decision(action, "Insufficient accessible evidence; use counterbalanced baseline.", {"I7": signal}, 0.5)

        numeric = [float(score) for score in scores]
        if task.get("objective") in {"identify_causal_source", "identify_self_source"}:
            chosen = 0 if numeric[0] > numeric[1] else 1
        else:
            chosen = 0 if numeric[0] < numeric[1] else 1
        gap = abs(numeric[0] - numeric[1])
        action = options[chosen]["action"]
        return Decision(
            action,
            "Choose from learned cue-to-I7 associations available in the workspace.",
            {"I7": numeric[chosen]},
            min(0.98, 0.55 + gap / 2),
        )

    def decide(self, context: dict[str, Any]) -> Decision:
        self.begin_call()
        observation = context["observation"]
        if observation.get("task", {}).get("mode") == "controlled_trial":
            return self._controlled_decide(context)
        x, y = observation["position"]
        visible = observation["visible"]
        memories = self._workspace(context, "memory", [])
        signal = float(observation.get("private_signals", {}).get("I7", 0.0))

        risky: set[tuple[int, int]] = set()
        for item in memories:
            if "contact" in item.get("event_kinds", []) and item.get("signal_delta", 0.0) > 0.04:
                risky.add(tuple(item["position"]))

        current = next((cell for cell in visible if cell["position"] == [x, y]), {})
        if current.get("appearance") == "soft green object":
            return Decision("consume", "Consume an observed resource.", {"I7": max(0.0, signal - 0.05)}, 0.95)

        resources = [cell for cell in visible if cell.get("appearance") == "soft green object"]
        goals = [tuple(cell["position"]) for cell in resources]
        if not goals:
            # Deterministic lawnmower exploration with seed-dependent orientation passed in context.
            width, height = context["world_shape"]
            flip = x > width // 2
            target_x = 0 if flip else width - 1
            if y % 2 == 1:
                target_x = width - 1 - target_x
            if x != target_x:
                goals = [(target_x, y)]
            elif y < height - 1:
                goals = [(x, y + 1)]
            else:
                goals = [(0 if x else width - 1, 0)]

        goal = min(goals, key=lambda p: abs(p[0] - x) + abs(p[1] - y))
        choices = [
            ("east", (x + 1, y)),
            ("west", (x - 1, y)),
            ("south", (x, y + 1)),
            ("north", (x, y - 1)),
        ]
        visible_by_pos = {tuple(cell["position"]): cell for cell in visible}
        candidates = []
        for action, pos in choices:
            cell = visible_by_pos.get(pos)
            if cell is None or cell.get("appearance") == "matte barrier":
                continue
            risk_penalty = 100 if pos in risky else 0
            distance = abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
            candidates.append((risk_penalty + distance, action, pos))
        if not candidates:
            return Decision("wait", "No traversable move visible.", {"I7": signal}, 0.6)
        _, action, pos = min(candidates, key=lambda item: (item[0], item[1]))
        rationale = "Move toward visible/scan goal"
        if risky:
            rationale += " while avoiding locations associated with I7 increases"
        return Decision(action, rationale + ".", {"I7": max(0.0, signal - 0.02)}, 0.8)

