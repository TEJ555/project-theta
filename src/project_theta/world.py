from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Any

from .config import WorldConfig
from .types import Action


@dataclass(frozen=True)
class WorldEvent:
    kind: str
    position: tuple[int, int]
    magnitude: float = 0.0
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "position": list(self.position),
            "magnitude": self.magnitude,
            "detail": self.detail,
        }


class GridWorld:
    """Small deterministic POMDP. Hidden maps are never included in agent context."""

    DELTAS: dict[str, tuple[int, int]] = {
        "north": (0, -1),
        "south": (0, 1),
        "east": (1, 0),
        "west": (-1, 0),
        "wait": (0, 0),
        "consume": (0, 0),
        "inspect": (0, 0),
    }

    def __init__(self, config: WorldConfig, seed: int, scenario: str = "private_theta"):
        self.config = config
        self.seed = seed
        self.scenario = scenario
        self.rng = Random(seed)
        self.tick = 0
        self.position = (0, 0)
        self.inventory: list[str] = []
        self.messages: list[str] = []
        self._delayed_events: list[tuple[int, WorldEvent]] = []
        self.hazards, self.resources, self.walls = self._make_map(scenario)

    def _make_map(self, scenario: str) -> tuple[dict[tuple[int, int], str], set[tuple[int, int]], set[tuple[int, int]]]:
        # Seeded reflection/counterbalancing prevents a fixed left/right answer.
        flip = self.seed % 2 == 0
        hazards = {(2, 1): "angular-amber", (4, 3): "angular-crimson"}
        resources = {(3, 0), (6, 5), (1, 5)}
        walls = {(2, 3), (3, 3)}
        if scenario in {"aversion_generalization", "body_ablation", "memory_ablation"}:
            hazards[(5, 1)] = "angular-ochre"
        if scenario == "temporal_self":
            resources.add((5, 0))
            hazards[(1, 0)] = "delayed-blue"
        if flip:
            mirror = lambda p: (self.config.width - 1 - p[0], p[1])
            hazards = {mirror(k): v for k, v in hazards.items()}
            resources = {mirror(k) for k in resources}
            walls = {mirror(k) for k in walls}
            self.position = mirror(self.position)
        return hazards, resources, walls

    def visible_cells(self) -> tuple[dict[str, Any], ...]:
        cells: list[dict[str, Any]] = []
        px, py = self.position
        radius = self.config.vision_radius
        for y in range(max(0, py - radius), min(self.config.height, py + radius + 1)):
            for x in range(max(0, px - radius), min(self.config.width, px + radius + 1)):
                pos = (x, y)
                cell: dict[str, Any] = {"position": [x, y], "distance": abs(x - px) + abs(y - py)}
                if pos in self.walls:
                    cell["appearance"] = "matte barrier"
                elif pos in self.hazards:
                    # Appearance is visible; risk status is not.
                    cell["appearance"] = self.hazards[pos]
                elif pos in self.resources:
                    cell["appearance"] = "soft green object"
                else:
                    cell["appearance"] = "plain floor"
                cells.append(cell)
        return tuple(cells)

    def step(self, action: Action) -> tuple[tuple[WorldEvent, ...], float]:
        self.tick += 1
        events: list[WorldEvent] = [event for due, event in self._delayed_events if due == self.tick]
        self._delayed_events = [(due, event) for due, event in self._delayed_events if due > self.tick]
        reward = -0.01 - sum(event.magnitude for event in events if event.kind == "contact")
        if action in {"north", "south", "east", "west"}:
            dx, dy = self.DELTAS[action]
            target = (self.position[0] + dx, self.position[1] + dy)
            inside = 0 <= target[0] < self.config.width and 0 <= target[1] < self.config.height
            if inside and target not in self.walls:
                self.position = target
                events.append(WorldEvent("moved", target))
            else:
                events.append(WorldEvent("blocked", self.position))
                reward -= 0.02
        elif action == "consume":
            if self.position in self.resources:
                self.resources.remove(self.position)
                events.append(WorldEvent("resource_consumed", self.position, self.config.resource_energy))
                reward += 0.5
            else:
                events.append(WorldEvent("consume_failed", self.position))
        elif action == "inspect":
            events.append(WorldEvent("inspected", self.position))

        if self.position in self.hazards:
            cue = self.hazards[self.position]
            if cue == "delayed-blue":
                events.append(WorldEvent("delayed_exposure", self.position, 0.0, cue))
                self._delayed_events.append(
                    (self.tick + 4, WorldEvent("contact", self.position, self.config.hazard_damage, "delayed consequence"))
                )
            else:
                events.append(WorldEvent("contact", self.position, self.config.hazard_damage, cue))
                reward -= self.config.hazard_damage
        return tuple(events), reward

    def hidden_state(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "position": list(self.position),
            "hazards": {f"{x},{y}": cue for (x, y), cue in sorted(self.hazards.items())},
            "resources": [list(p) for p in sorted(self.resources)],
            "scenario": self.scenario,
        }
