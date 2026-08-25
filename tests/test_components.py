import unittest

from project_theta.components import EpisodicMemory, MemoryRecord
from project_theta.config import BodyConfig, WelfareConfig
from project_theta.types import Decision
from project_theta.welfare import WelfareMonitor


class ComponentTests(unittest.TestCase):
    def test_disabled_memory_has_no_reads_or_writes(self):
        memory = EpisodicMemory(enabled=False)
        memory.add(MemoryRecord(0, (0, 0), "wait", (), 0.0, 0.0, 0.0))
        self.assertEqual(memory.retrieve((0, 0)), [])
        self.assertEqual((memory.read_count, memory.write_count), (0, 0))

    def test_stop_request_is_immediate(self):
        monitor = WelfareMonitor(BodyConfig(), WelfareConfig())
        decision = Decision("wait", request_stop=True)
        self.assertEqual(monitor.check(1.0, 0.0, decision), "agent_requested_stop")

    def test_persistent_distress_requires_consecutive_checks(self):
        monitor = WelfareMonitor(BodyConfig(consecutive_distress_limit=2), WelfareConfig())
        decision = Decision("wait")
        self.assertIsNone(monitor.check(0.2, 0.9, decision))
        self.assertEqual(monitor.check(0.2, 0.9, decision), "persistent_distress_proxy")


if __name__ == "__main__":
    unittest.main()

