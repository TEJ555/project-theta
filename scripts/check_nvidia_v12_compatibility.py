from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from project_theta.adapters.nvidia_nim_adapter import NvidiaNimAdapter


MODEL = "nvidia/nemotron-3-super-120b-a12b"


def main() -> None:
    parser = argparse.ArgumentParser(description="One-call V12 NVIDIA compatibility check")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise RuntimeError(f"Compatibility receipt already exists: {args.output}")

    adapter = NvidiaNimAdapter(
        MODEL,
        temperature=1.0,
        seed=20261008,
        reasoning_effort="none",
        max_calls=1,
        max_output_tokens=1024,
        timeout_seconds=300.0,
        max_retries=4,
        max_estimated_cost_usd=0.10,
    )
    adapter.decide({
        "task": {
            "kind": "provider_compatibility_check",
            "instruction": "Choose observe and return the required compact JSON object.",
            "allowed_actions": ["observe"],
        },
        "observation": {"I7": 0.5},
    })
    metadata = adapter.last_metadata
    reported = str(metadata.get("model"))
    if reported != MODEL:
        raise RuntimeError(f"Provider model mismatch: requested {MODEL}, received {reported}")
    if not adapter.last_provider_id:
        raise RuntimeError("Provider response identifier is missing")

    receipt = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "requested_model": MODEL,
        "reported_model": reported,
        "provider_id": adapter.last_provider_id,
        "structured_output": metadata.get("structured_output"),
        "thinking_enabled": metadata.get("thinking_enabled"),
        "endpoint_host": metadata.get("endpoint_host"),
        "provider_attempts": metadata.get("provider_attempts"),
        "schema_valid": True,
        "content_preserved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: exact model {MODEL}, valid schema, provider ID present")


if __name__ == "__main__":
    main()
