from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


PLANNED_SEEDS = (7500, 7501, 7502, 7503, 7504, 7505)
REQUIRED_MODEL = "nvidia/nemotron-3-super-120b-a12b"
BASE_ANALYZER = Path(__file__).with_name("analyze_v11_1_repair.py")


def _load_base_analyzer():
    spec = importlib.util.spec_from_file_location("theta_v11_1_analysis_base", BASE_ANALYZER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load base analyzer: {BASE_ANALYZER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = _load_base_analyzer()
CONDITIONS = BASE.CONDITIONS


def analyze(database: Path, bootstrap_samples: int = 10_000) -> dict[str, Any]:
    result = BASE.analyze(
        database,
        bootstrap_samples,
        planned_seeds=PLANNED_SEEDS,
        required_model=REQUIRED_MODEL,
    )
    result["study"] = "V12 Nemotron cross-model replication"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze the frozen V12 cross-model replication")
    parser.add_argument("database", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bootstrap-samples", type=int, default=10_000)
    args = parser.parse_args()
    result = analyze(args.database, args.bootstrap_samples)
    payload = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
        print("Project Theta V12 Nemotron cross-model analysis")
        for name, passed in result["gates"].items():
            print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        print("Progression: " + ("PASS" if result["mechanism_progression_pass"] else "BLOCKED"))
        print(f"Full analysis: {args.output}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
