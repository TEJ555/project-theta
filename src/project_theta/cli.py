from __future__ import annotations

import argparse
import json
import os
from dataclasses import replace
from pathlib import Path

from . import EPISTEMIC_NOTICE
from .analysis import format_summary, summaries_from_database, summarize_runs
from .audits import add_execution_audit, audit_adversarial_schedules, format_audit
from .config import RunConfig, load_config
from .doctor import format_doctor, run_doctor
from .experiments import PROTOCOLS
from .harness import ExperimentHarness
from .provenance import code_version, is_immutable_code_version
from .storage import RunStore
from .worker import run_worker


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
    run.add_argument("--experiment", choices=[*PROTOCOLS, "all"])
    run.add_argument("--seeds", type=_seeds, default=[11, 22, 33])
    run.add_argument("--conditions", help="comma-separated override")
    run.add_argument("--adapter", choices=["scripted", "openai", "anthropic", "ollama"])
    run.add_argument("--model", help="provider model ID (provider-specific default if omitted)")
    run.add_argument("--temperature", type=float, default=0.0)
    run.add_argument("--db", default="runs/study.sqlite")
    run.add_argument("--config", help="optional JSON base configuration")
    run.add_argument("--json", dest="json_path", help="write summary JSON")
    run.add_argument("--verbose-json", action="store_true", help="also print full per-run JSON")
    run.add_argument("--max-runs", type=int, help="hard cap on run count")

    report = sub.add_parser("report", help="print a compact statistical study summary")
    report.add_argument("--db", required=True)
    report.add_argument("--json", action="store_true", help="print machine-readable summary")

    validate = sub.add_parser("validate", help="run the complete pre-deployment scripted validation")
    validate.add_argument("--seeds", type=_seeds, default=list(range(101, 121)))
    validate.add_argument("--db", default="runs/validation.sqlite")

    recover = sub.add_parser("recover", help="mark incomplete runs after an interrupted process")
    recover.add_argument("--db", required=True)

    worker = sub.add_parser("worker", help="run a resumable bounded study worker")
    worker.add_argument("--spec", required=True)
    worker.add_argument("--once", action="store_true", help="run one cycle and exit")

    doctor = sub.add_parser("doctor", help="check local or model-backed deployment readiness")
    doctor.add_argument(
        "--adapter", choices=["scripted", "openai", "anthropic", "ollama"], default="scripted"
    )
    doctor.add_argument("--db", default="runs/doctor.sqlite")

    audit = sub.add_parser("audit", help="audit blinded schedules for shortcut leakage")
    audit.add_argument("--seeds", type=_seeds, default=[91, 92, 93, 94])
    audit.add_argument("--db", help="also verify completed runs use the adversarial protocol")
    audit.add_argument("--profile", choices=["standard", "compact"], default="standard")

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
        summary = summarize_runs(summaries_from_database(args.db))
        print(json.dumps(summary, indent=2) if args.json else format_summary(summary))
        return 0
    if args.command == "recover":
        with RunStore(args.db) as store:
            count = store.mark_interrupted_runs()
        print(f"Marked {count} interrupted run(s) as failed; completed step logs were preserved.")
        return 0
    if args.command == "worker":
        return run_worker(args.spec, once=args.once)
    if args.command == "doctor":
        result = run_doctor(args.adapter, args.db)
        print(format_doctor(result))
        return 0 if result["status"] == "pass" else 1
    if args.command == "audit":
        result = audit_adversarial_schedules(args.seeds, args.profile)
        if args.db:
            if len(args.seeds) != 1:
                raise SystemExit("Execution audit requires exactly one expected seed.")
            expected_steps = 16 if args.profile == "compact" else 32
            result = add_execution_audit(result, args.db, args.seeds[0], expected_steps)
        print(format_audit(result))
        return 0 if result["status"] == "pass" else 1
    if args.command == "validate":
        summaries = ExperimentHarness(args.db).run_study("all", args.seeds, RunConfig())
        summary = summarize_runs(summaries)
        print(format_summary(summary))
        return 1 if summary["warnings"] else 0
    if args.command == "demo":
        config = replace(
            RunConfig(),
            experiment="navigation_demo",
            seed=args.seed,
            world=replace(RunConfig().world, max_steps=args.steps),
        )
        summary = ExperimentHarness(args.db).run(config)
        print(json.dumps({"epistemic_notice": EPISTEMIC_NOTICE, "run": summary.to_dict()}, indent=2))
        return 0
    config = load_config(args.config) if args.config else RunConfig()
    adapter_name = args.adapter or config.adapter
    default_models = {
        "scripted": "scripted-baseline-v1",
        "openai": os.getenv("THETA_OPENAI_MODEL", "gpt-5.6"),
        "anthropic": os.getenv("THETA_ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        "ollama": os.getenv("THETA_OLLAMA_MODEL", "llama3.2"),
    }
    configured_model = config.model if args.config and config.adapter == adapter_name else None
    config = replace(
        config,
        adapter=adapter_name,
        model=args.model or configured_model or default_models[adapter_name],
        temperature=args.temperature,
    )
    if config.adapter != "scripted":
        if os.getenv("THETA_ENABLE_MODEL_RUNS") != "YES":
            raise SystemExit(
                "Model-backed runs are locked. Set THETA_ENABLE_MODEL_RUNS=YES after reviewing "
                "the run count and provider configuration."
            )
        if args.max_runs is None:
            raise SystemExit("Model-backed runs require an explicit --max-runs budget.")
        revision = code_version()
        if not is_immutable_code_version(revision):
            raise SystemExit(
                "Model-backed runs require a clean committed revision or an explicit "
                "THETA_CODE_VERSION in an immutable deployment."
            )
    conditions = args.conditions.split(",") if args.conditions else None
    experiment_name = args.experiment or config.experiment
    summaries = ExperimentHarness(args.db).run_study(
        experiment_name, args.seeds, config, conditions=conditions, max_runs=args.max_runs
    )
    payload = {"epistemic_notice": EPISTEMIC_NOTICE, "runs": [item.to_dict() for item in summaries]}
    rendered = json.dumps(payload, indent=2)
    print(format_summary(summarize_runs(summaries)))
    if args.verbose_json:
        print(rendered)
    if args.json_path:
        path = Path(args.json_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered + "\n", encoding="utf-8")
    return 0
