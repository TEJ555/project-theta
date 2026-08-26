from __future__ import annotations

from dataclasses import asdict, dataclass
from random import Random

from .config import BodyConfig, WorldConfig
from .world import WorldEvent


@dataclass
class BodyState:
    energy: float = 1.0
    integrity: float = 1.0
    temperature: float = 0.5
    theta: float = 0.0


class SyntheticBody:
    """Hidden physiology with an intentionally semantically opaque I7 channel."""

    def __init__(self, config: BodyConfig, world_config: WorldConfig, seed: int):
        self.config = config
        self.world_config = world_config
        self.state = BodyState()
        self.rng = Random(seed ^ 0xA17E)
        self._previous_signal = 0.0
        self._sham_theta = 0.0

    def update(self, events: tuple[WorldEvent, ...]) -> None:
        if not self.config.body_enabled:
            return
        self.state.energy = max(0.0, self.state.energy - self.world_config.action_energy_cost)
        damage = sum(event.magnitude for event in events if event.kind == "contact")
        resource = sum(event.magnitude for event in events if event.kind == "resource_consumed")
        self.state.integrity = max(0.0, self.state.integrity - damage)
        self.state.energy = min(1.0, self.state.energy + resource)
        target_theta = min(1.0, damage * self.config.theta_damage_gain + (1.0 - self.state.integrity) * 0.7)
        self.state.theta = max(0.0, self.state.theta * (1.0 - self.config.theta_decay))
        self.state.theta = min(1.0, max(self.state.theta, target_theta))

    def controlled_perturbation(self, magnitude: float) -> None:
        """Change the private channel without labeling it as damage or valence."""
        if not self.config.body_enabled:
            return
        self.state.theta = min(1.0, max(self.state.theta, magnitude))

    def controlled_sham_perturbation(self, magnitude: float) -> None:
        """Set a plausible private signal that is independent of the true perturbation."""
        if self.config.body_enabled:
            self._sham_theta = min(1.0, max(0.0, magnitude))

    def standardized_recovery(self, reset_measurement_baseline: bool = False) -> None:
        """Reset transient theta between laboratory trials, preserving other state."""
        if self.config.body_enabled:
            self.state.theta = 0.0
            self._sham_theta = 0.0
        if reset_measurement_baseline:
            self._previous_signal = 0.0

    def sense(self, tick: int) -> tuple[dict[str, float], dict[str, float]]:
        if self.config.signal_mode == "absent":
            current = 0.0
        elif self.config.signal_mode == "shuffled":
            # Deterministic but causally unrelated to current body damage.
            current = 0.5 + 0.42 * self.rng.uniform(-1.0, 1.0)
        elif self.config.signal_mode == "matched_sham":
            current = self._sham_theta
        elif self.config.signal_mode == "sham":
            current = self._sham_theta + self.rng.gauss(0.0, self.config.noise_std)
        else:
            current = self.state.theta + self.rng.gauss(0.0, self.config.noise_std)
        current = round(min(1.0, max(0.0, current)), 4)
        delta = round(current - self._previous_signal, 4)
        self._previous_signal = current
        return {"I7": current}, {"I7": delta}

    def hidden_state(self) -> dict[str, float]:
        return {key: round(float(value), 6) for key, value in asdict(self.state).items()}
