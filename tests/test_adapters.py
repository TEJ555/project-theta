import json
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from project_theta.adapters.anthropic_adapter import AnthropicAdapter
from project_theta.adapters.base import AdapterError
from project_theta.adapters.claude_code_adapter import ClaudeCodeSubscriptionAdapter
from project_theta.adapters.openai_adapter import OpenAIAdapter
from project_theta.adapters.scripted import ScriptedAdapter


class AdapterTests(unittest.TestCase):
    def test_claude_code_adapter_requires_max_and_isolates_the_subject(self):
        captured = {}
        decision_payload = {
            "action": "observe",
            "rationale": "test",
            "prediction": {"I7": 0.0},
            "confidence": 0.5,
            "self_report": "",
            "request_stop": False,
        }

        def fake_run(command, **kwargs):
            captured["command"] = command
            captured.update(kwargs)
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps({
                    "type": "result",
                    "is_error": False,
                    "session_id": "subscription-session",
                    "total_cost_usd": 0.0,
                    "num_turns": 1,
                    "structured_output": decision_payload,
                    "usage": {"input_tokens": 25, "output_tokens": 10},
                }),
                stderr="",
            )

        auth = {"authMethod": "claude.ai", "subscriptionType": "max"}
        with (
            patch(
                "project_theta.adapters.claude_code_adapter.resolve_claude_code_path",
                return_value="claude",
            ),
            patch(
                "project_theta.adapters.claude_code_adapter.claude_code_auth_status",
                return_value=auth,
            ),
            patch(
                "project_theta.adapters.claude_code_adapter.claude_code_version",
                return_value="2.1.247 (Claude Code)",
            ),
            patch(
                "project_theta.adapters.claude_code_adapter.subprocess.run",
                side_effect=fake_run,
            ),
            patch.dict("os.environ", {"ANTHROPIC_API_KEY": "metered-key"}),
        ):
            adapter = ClaudeCodeSubscriptionAdapter("sonnet")
            decision = adapter.decide({"permitted_actions": ["observe"]})

        self.assertEqual(decision.action, "observe")
        self.assertIn("--json-schema", captured["command"])
        self.assertIn("--safe-mode", captured["command"])
        self.assertIn("--no-session-persistence", captured["command"])
        tools_index = captured["command"].index("--tools")
        self.assertEqual(captured["command"][tools_index + 1], "")
        self.assertNotIn("ANTHROPIC_API_KEY", captured["env"])
        self.assertNotIn("project-theta", str(captured["cwd"]).lower())
        self.assertEqual(adapter.last_metadata["reported_cost_equivalent_usd"], 0.0)
        self.assertEqual(adapter.last_metadata["billing_route"], "claude_max_subscription")
        self.assertEqual(adapter.last_metadata["estimated_cost_usd"], 0.0)
        self.assertTrue(adapter.last_metadata["metered_provider_environment_absent"])
        self.assertEqual(adapter.last_metadata["claude_code_version"], "2.1.247 (Claude Code)")
        self.assertEqual(adapter.last_metadata["total_tokens"], 35)

    def test_claude_code_cost_equivalent_is_not_counted_as_api_spend(self):
        auth = {"authMethod": "claude.ai", "subscriptionType": "max"}
        response = SimpleNamespace(
            returncode=0,
            stdout=json.dumps({
                "type": "result",
                "is_error": False,
                "total_cost_usd": 0.01,
                "structured_output": {},
            }),
            stderr="",
        )
        with (
            patch(
                "project_theta.adapters.claude_code_adapter.resolve_claude_code_path",
                return_value="claude",
            ),
            patch(
                "project_theta.adapters.claude_code_adapter.claude_code_auth_status",
                return_value=auth,
            ),
            patch(
                "project_theta.adapters.claude_code_adapter.claude_code_version",
                return_value="2.1.247 (Claude Code)",
            ),
            patch(
                "project_theta.adapters.claude_code_adapter.subprocess.run",
                return_value=response,
            ),
        ):
            adapter = ClaudeCodeSubscriptionAdapter("sonnet")
            adapter.decide({"permitted_actions": ["observe"]})
        self.assertEqual(adapter.last_metadata["reported_cost_equivalent_usd"], 0.01)
        self.assertEqual(adapter.last_metadata["estimated_cost_usd"], 0.0)

    def test_claude_code_adapter_rejects_console_authentication(self):
        auth = {"authMethod": "console", "subscriptionType": None}
        with (
            patch(
                "project_theta.adapters.claude_code_adapter.resolve_claude_code_path",
                return_value="claude",
            ),
            patch(
                "project_theta.adapters.claude_code_adapter.claude_code_auth_status",
                return_value=auth,
            ),
            patch(
                "project_theta.adapters.claude_code_adapter.claude_code_version",
                return_value="2.1.247 (Claude Code)",
            ),
            self.assertRaisesRegex(AdapterError, "subscription authentication"),
        ):
            ClaudeCodeSubscriptionAdapter("sonnet")

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

    def test_anthropic_adapter_uses_schema_and_enforces_cost_guard(self):
        captured = {}

        class Messages:
            def create(self, **kwargs):
                captured.update(kwargs)
                return SimpleNamespace(
                    id="msg-test",
                    model="claude-sonnet-4-6",
                    content=[SimpleNamespace(
                        type="text",
                        text=json.dumps({
                            "action": "observe", "rationale": "test",
                            "prediction": {"I7": 0.0}, "confidence": 0.5,
                            "self_report": "", "request_stop": False,
                        }),
                    )],
                    usage=SimpleNamespace(input_tokens=500_000, output_tokens=100),
                )

        class FakeAnthropic:
            def __init__(self, **kwargs):
                self.messages = Messages()

        transformed_schema = {
            "type": "object",
            "properties": {"confidence": {"type": "number", "description": "0 to 1"}},
            "required": ["confidence"],
            "additionalProperties": False,
        }
        fake_module = SimpleNamespace(
            Anthropic=FakeAnthropic,
            transform_schema=lambda schema: transformed_schema,
        )
        with patch.dict(sys.modules, {"anthropic": fake_module}):
            adapter = AnthropicAdapter("claude-sonnet-4-6", max_estimated_cost_usd=1.25)
            decision = adapter.decide({"permitted_actions": ["observe"]})
            with self.assertRaises(AdapterError):
                adapter.decide({"permitted_actions": ["observe"]})
        self.assertEqual(decision.action, "observe")
        self.assertNotIn("temperature", captured)
        self.assertEqual(captured["output_config"]["effort"], "low")
        self.assertEqual(captured["output_config"]["format"]["type"], "json_schema")
        self.assertIs(captured["output_config"]["format"]["schema"], transformed_schema)
        self.assertNotIn(
            "minimum", captured["output_config"]["format"]["schema"]["properties"]["confidence"]
        )
        self.assertEqual(adapter.last_metadata["temperature_requested"], 0.0)
        self.assertIsNone(adapter.last_metadata["temperature_applied"])
        self.assertGreater(adapter.estimated_cost_usd, 1.25)


if __name__ == "__main__":
    unittest.main()
