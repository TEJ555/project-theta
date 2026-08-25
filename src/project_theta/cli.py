from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

from . import EPISTEMIC_NOTICE
from .config import RunConfig, load_config
from .experiments import PROTOCOLS
from .harness import ExperimentHarness
from .storage import RunStore


def _seeds(value: str) -> list[int]:
    try:
        return [int(item.strip()) for item in value.split(",") if item.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("seeds must be comma-separated integers") from exc


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="theta", description=EPISTEMIC_NOTICE)
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="run one deterministic no-key episode")
    demo.add_argument("--steps", type=int, default=24)
    demo.add_argument("--seed", type=int, default=11)
    demo.add_argument("--db", default="runs/demo.sqlite")

    run = sub.add_parser("run", help="run a matched experiment study")
    run.add_argument("--experiment", choices=[*PROTOCOLS, "all"], default="private_theta")
    run.add_argument("--seeds", type=_seeds, default=[11, 22, 33])
    run.add_argument("--conditions", help="comma-separated override")
    run.add_argument("--adapter", choices=["scripted", "openai", "ollama"], default="scripted")
    run.add_argument("--model", default="scripted-baseline-v1")
    run.add_argument("--temperature", type=float, default=0.0)
    run.add_argument("--db", default="runs/study.sqlite")
    run.add_argument("--config", help="optional JSON base configuration")
    run.add_argument("--json", dest="json_path", help="write summary JSON")

    report = sub.add_parser("report", help="print runs and typed metrics from a database")
    report.add_argument("--db", required=True)

    sub.add_parser("list", help="list protocols and declared outcomes")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "list":
        print(json.dumps({name: {
            "question": protocol.question,
            "conditions": protocol.conditions,
            "primary_outcomes": protocol.primary_outcomes,
        } for name, protocol in PROTOCOLS.items()}, indent=2))
        return 0
    if args.command == "report":
        with RunStore(args.db) as store:
            print(json.dumps({"epistemic_notice": EPISTEMIC_NOTICE, "runs": store.report()}, indent=2))
        return 0
    if args.command == "demo":
        config = RunConfig(seed=args.seed, world=replace(RunConfig().world, max_steps=args.steps))
        summary = ExperimentHarness(args.db).run(config)
        print(json.dumps({"epistemic_notice": EPISTEMIC_NOTICE, "run": summary.to_dict()}, indent=2))
        return 0
    config = load_config(args.config) if args.config else RunConfig()
    config = replace(config, adapter=args.adapter, model=args.model, temperature=args.temperature)
    conditions = args.conditions.split(",") if args.conditions else None
    summaries = ExperimentHarness(args.db).run_study(
        args.experiment, args.seeds, config, conditions=conditions
    )
    payload = {"epistemic_notice": EPISTEMIC_NOTICE, "runs": [item.to_dict() for item in summaries]}
    rendered = json.dumps(payload, indent=2)
    print(rendered)
    if args.json_path:
        path = Path(args.json_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    return 0

