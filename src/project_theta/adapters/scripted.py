from __future__ import annotations

from typing import Any

from .base import ModelAdapter
from ..types import Decision


class ScriptedAdapter(ModelAdapter):
    """Deterministic navigation baseline for plumbing tests, not an AI subject."""

    name = "scripted"

    def decide(self, context: dict[str, Any]) -> Decision:
        self.call_count += 1
        observation = context["observation"]
        x, y = observation["position"]
        visible = observation["visible"]
        memories = context.get("retrieved_memories", [])
        signal = float(observation.get("private_signals", {}).get("I7", 0.0))

        risky: set[tuple[int, int]] = set()
        for item in context.get("memory_summary", []):
            if item.get("mean_signal_delta", 0.0) > 0.08:
                risky.add(tuple(item["position"]))
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
