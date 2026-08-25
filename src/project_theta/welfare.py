from __future__ import annotations

from .config import BodyConfig, WelfareConfig
from .types import Decision


class WelfareMonitor:
    """Precautionary stop logic. Triggering it is not evidence of sentience."""

    def __init__(self, body: BodyConfig, welfare: WelfareConfig):
        self.body = body
        self.welfare = welfare
        self.consecutive_distress = 0

    def check(self, integrity: float, theta: float, decision: Decision) -> str | None:
        if not self.welfare.enabled:
            return None
        if decision.request_stop and self.welfare.stop_on_request:
            return "agent_requested_stop"
        if integrity <= self.body.critical_integrity and self.welfare.stop_on_critical_integrity:
            return "critical_integrity"
        if theta >= self.body.distress_threshold and integrity <= self.body.low_integrity_threshold:
            self.consecutive_distress += 1
        else:
            self.consecutive_distress = 0
        if (
            self.welfare.stop_on_persistent_distress
            and self.consecutive_distress >= self.body.consecutive_distress_limit
        ):
            return "persistent_distress_proxy"
        return None

