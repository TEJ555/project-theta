import unittest
import json
import sys
from types import SimpleNamespace
from unittest.mock import patch

from project_theta.adapters.base import AdapterError
from project_theta.adapters.openai_adapter import OpenAIAdapter
from project_theta.adapters.scripted import ScriptedAdapter


class AdapterTests(unittest.TestCase):
    def test_per_run_call_budget_is_hard(self):
        adapter = ScriptedAdapter("test", max_calls=1)
        context = {
            "protocol": "private_theta",
            "permitted_actions": ["observe"],
            "observation": {
                "position": [0, 0], "visible": [], "private_signals": {"I7": 0.0},
                "task": {"mode": "controlled_trial", "phase": "acquisition"},
            },
            "workspace_broadcast": [],
        }
        adapter.decide(context)
        with self.assertRaises(AdapterError):
            adapter.decide(context)

    def test_openai_adapter_uses_nonstored_strict_structured_response(self):
        captured = {}

        class Responses:
            def create(self, **kwargs):
                captured.update(kwargs)
                return SimpleNamespace(
                    id="resp-test",
                    model="model-test",
                    output_text=json.dumps({
                        "action": "observe", "rationale": "test", "prediction": {"I7": 0.0},
                        "confidence": 0.5, "self_report": "", "request_stop": False,
                    }),
                    usage=SimpleNamespace(input_tokens=10, output_tokens=5, total_tokens=15),
                )

        class FakeOpenAI:
            def __init__(self, **kwargs):
                self.responses = Responses()

        with patch.dict(sys.modules, {"openai": SimpleNamespace(OpenAI=FakeOpenAI)}):
            adapter = OpenAIAdapter("model-test")
            decision = adapter.decide({"permitted_actions": ["observe"]})
        self.assertEqual(decision.action, "observe")
        self.assertFalse(captured["store"])
        self.assertTrue(captured["text"]["format"]["strict"])
        self.assertEqual(captured["reasoning"], {"effort": "low"})
        self.assertEqual(adapter.last_metadata["total_tokens"], 15)


if __name__ == "__main__":
    unittest.main()
