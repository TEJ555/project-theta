from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def state_register(context: dict[str, Any]) -> dict[str, Any] | None:
    for item in context.get("workspace_broadcast", []):
        if item.get("source") == "state_register":
            content = item.get("content")
            return content if isinstance(content, dict) else None
    return None


def raw_actor_values(context: dict[str, Any]) -> dict[str, float]:
    values: dict[str, list[float]] = defaultdict(list)
    for item in context.get("workspace_broadcast", []):
        if item.get("source") != "memory":
            continue
        for record in item.get("content", []):
            actor = ""
            pointer: float | None = None
            for tag in record.get("tags", []):
                if tag.startswith("u:"):
                    actor = tag.removeprefix("u:")
                if tag in {"v:0", "v:1"}:
                    pointer = float(tag.removeprefix("v:"))
            if actor and pointer is not None:
                values[actor].append(pointer)
    return {actor: sum(rows) / len(rows) for actor, rows in values.items()}


def option_maps(context: dict[str, Any]) -> tuple[dict[str, str], dict[str, str]]:
    token_to_action: dict[str, str] = {}
    actor_to_action: dict[str, str] = {}
    task = context.get("observation", {}).get("task", {})
    for option in task.get("options", []):
        action = str(option.get("action", ""))
        stimulus = option.get("stimulus", {})
        token_to_action[str(stimulus.get("token", ""))] = action
        for feature in stimulus.get("features", []):
            if feature.startswith("u:"):
                actor_to_action[feature.removeprefix("u:")] = action
    return token_to_action, actor_to_action


def audit(payload: dict[str, Any]) -> dict[str, int]:
    counts = defaultdict(int)
    for run in payload.get("runs", []):
        for probe in run.get("probes", []):
            counts["probes"] += 1
            context = probe["model_visible_context"]
            response_action = str(probe["response"].get("action", ""))
            expected_action = str(probe["expected"].get("action", ""))
            rationale = str(probe["response"].get("rationale", "")).lower()
            if "register" in rationale:
                counts["rationales_mentioning_register"] += 1

            token_to_action, actor_to_action = option_maps(context)
            register = state_register(context)
            if register:
                predictions = register.get("predictions", {})
                if len(predictions) == 2 and len(set(predictions.values())) == 2:
                    counts["decisive_register_probes"] += 1
                    best_token = max(predictions, key=predictions.get)
                    if response_action == token_to_action.get(best_token):
                        counts["register_argmax_followed"] += 1

            actor_values = raw_actor_values(context)
            scored = {
                actor: actor_values[actor]
                for actor in actor_to_action
                if actor in actor_values
            }
            if len(scored) == 2 and len(set(scored.values())) == 2:
                counts["raw_memory_rule_probes"] += 1
                best_actor = max(scored, key=scored.get)
                if actor_to_action[best_actor] == expected_action:
                    counts["raw_memory_rule_correct"] += 1
    return dict(sorted(counts.items()))


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the V5 answer-table shortcuts")
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.bundle.read_text(encoding="utf-8"))
    result = audit(payload)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
