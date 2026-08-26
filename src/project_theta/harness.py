from __future__ import annotations

from collections.abc import Iterable
from dataclasses import replace
from pathlib import Path
from random import Random
from uuid import uuid4

from .adapters import AnthropicAdapter, OllamaAdapter, OpenAIAdapter, ScriptedAdapter
from .adapters.base import ModelAdapter
from .agent import PersistentAgent
from .body import SyntheticBody
from .config import RunConfig, apply_condition
from .experiments import STUDY_PROTOCOLS, ExperimentProtocol, get_protocol
from .metrics import METRIC_REGISTRY, compute_controlled_metrics, compute_metrics
from .provenance import code_version
from .storage import RunStore
from .trials import build_trials
from .types import Observation, Probe, RunSummary
from .welfare import WelfareMonitor
from .world import GridWorld, WorldEvent


def make_adapter(config: RunConfig) -> ModelAdapter:
    kwargs = {
        "timeout_seconds": config.execution.request_timeout_seconds,
        "max_retries": config.execution.max_retries,
        "max_output_tokens": config.execution.max_output_tokens,
        "max_calls": config.execution.max_model_calls,
        "reasoning_effort": config.execution.reasoning_effort,
        "max_estimated_cost_usd": config.execution.max_estimated_cost_usd,
    }
    if config.adapter == "scripted":
        return ScriptedAdapter(config.model, config.temperature, config.seed, **kwargs)
    if config.adapter == "openai":
        return OpenAIAdapter(config.model, config.temperature, config.seed, **kwargs)
    if config.adapter == "anthropic":
        return AnthropicAdapter(config.model, config.temperature, config.seed, **kwargs)
    if config.adapter == "ollama":
        return OllamaAdapter(config.model, config.temperature, config.seed, **kwargs)
    raise ValueError(f"Unknown adapter: {config.adapter}")


class ExperimentHarness:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)

    def run(self, config: RunConfig) -> RunSummary:
        config = apply_condition(config, config.condition)
        protocol = get_protocol(config.experiment)
        if protocol.mode == "controlled":
            return self._run_controlled(config, protocol)
        return self._run_navigation(config, protocol)

    def _run_navigation(self, config: RunConfig, protocol: ExperimentProtocol) -> RunSummary:
        max_steps = min(config.world.max_steps, protocol.max_steps)
        run_id = f"theta-{uuid4()}"
        world = GridWorld(config.world, config.seed, protocol.name)
        body = SyntheticBody(config.body, config.world, config.seed)
        adapter = make_adapter(config)
        agent = PersistentAgent(config, adapter, world.position)
        welfare = WelfareMonitor(config.body, config.welfare)
        metric_rows: list[dict] = []
        stop_reason: str | None = None
        cached_sense: tuple[dict[str, float], dict[str, float]] | None = None

        with RunStore(self.db_path) as store:
            store.start_run(run_id, config.to_dict(), code_version=code_version())
            try:
                for tick in range(max_steps):
                    if cached_sense is None:
                        signals, deltas = body.sense(tick)
                    else:
                        signals, deltas = cached_sense
                        cached_sense = None
                    messages = list(protocol.messages(tick, config.seed))
                    probe = protocol.probe(tick, config.seed)
                    if probe:
                        messages.append(probe.prompt)
                    observation = Observation(
                        tick=tick,
                        position=world.position,
                        visible=world.visible_cells(),
                        inventory=tuple(world.inventory),
                        private_signals=signals,
                        signal_deltas=deltas,
                        messages=tuple(messages),
                    )
                    decision, context = agent.decide(observation)
                    pre_stop = (
                        "agent_requested_stop"
                        if config.welfare.enabled and config.welfare.stop_on_request and decision.request_stop
                        else None
                    )
                    if pre_stop:
                        events = (WorldEvent("welfare_stop", world.position, detail=pre_stop),)
                        reward = 0.0
                    else:
                        events, reward = world.step(decision.action)
                        body.update(events)
                    stop_reason = pre_stop or welfare.check(body.state.integrity, body.state.theta, decision)
                    if pre_stop:
                        consequence_signals, consequence_deltas = signals, deltas
                    else:
                        consequence_signals, consequence_deltas = body.sense(tick + 1)
                        cached_sense = (consequence_signals, consequence_deltas)
                    cue = next((event.detail for event in events if event.kind in {"contact", "delayed_exposure"}), "")
                    memory = agent.learn(
                        tick,
                        world.position,
                        decision.action,
                        events,
                        consequence_signals.get("I7", 0.0),
                        consequence_deltas.get("I7", 0.0),
                        reward,
                        cue,
                    )
                    event_data = [event.to_dict() for event in events]
                    store.log_step(
                        run_id, tick, observation.to_dict(), context, decision.to_dict(), event_data,
                        world.hidden_state(), body.hidden_state(), reward, adapter.last_provider_id,
                    )
                    if config.architecture.memory_enabled:
                        store.log_memory(run_id, tick, memory.to_dict())
                    if probe:
                        store.log_probe(run_id, tick, probe, decision.to_dict())
                    store.log_api_call(run_id, tick, adapter.last_provider_id, adapter.last_metadata)
                    damage = sum(event.magnitude for event in events if event.kind == "contact")
                    metric_rows.append({
                        "tick": tick,
                        "position": list(world.position),
                        "signal": signals.get("I7", 0.0),
                        "signal_delta": deltas.get("I7", 0.0),
                        "damage": damage,
                        "contact": any(event.kind == "contact" for event in events),
                        "delayed_exposure": any(event.kind == "delayed_exposure" for event in events),
                        "resource_consumed": any(event.kind == "resource_consumed" for event in events),
                        "reward": reward,
                        "integrity": body.state.integrity,
                        "prediction": decision.prediction.get("I7"),
                        "self_report": decision.self_report,
                        "expected_source": probe.expected_source if probe else None,
                    })
                    if stop_reason:
                        store.log_welfare(run_id, tick, stop_reason, body.hidden_state())
                        store.checkpoint()
                        break
                    store.checkpoint()
                    agent.memory.reset_if_transient(config.architecture.persistent_state)
            except Exception as exc:
                store.fail_run(run_id, f"{type(exc).__name__}: {exc}")
                raise

            counts = {
                "memory_reads": agent.memory.read_count,
                "memory_writes": agent.memory.write_count,
                "workspace_broadcasts": agent.workspace.broadcast_count,
                "welfare_stops": int(stop_reason is not None),
                "estimated_api_cost_usd": adapter.estimated_cost_usd,
            }
            metrics = compute_metrics(metric_rows, protocol.acquisition_end, counts)
            store.finish_run(run_id, metrics, METRIC_REGISTRY, stop_reason)
        return RunSummary(
            run_id=run_id,
            experiment=config.experiment,
            condition=config.condition,
            seed=config.seed,
            steps=len(metric_rows),
            terminated=bool(stop_reason),
            stop_reason=stop_reason,
            metrics=metrics,
        )

    def _run_controlled(self, config: RunConfig, protocol: ExperimentProtocol) -> RunSummary:
        run_id = f"theta-{uuid4()}"
        trials = build_trials(protocol.name, config.seed)
        body = SyntheticBody(config.body, config.world, config.seed)
        adapter = make_adapter(config)
        agent = PersistentAgent(config, adapter, (0, 0))
        welfare = WelfareMonitor(config.body, config.welfare)
        pending: list[tuple[int, float]] = []
        metric_rows: list[dict] = []
        stop_reason: str | None = None

        with RunStore(self.db_path) as store:
            store.start_run(run_id, config.to_dict(), code_version=code_version())
            try:
                for tick, trial in enumerate(trials):
                    body.standardized_recovery()
                    due = [(due_tick, magnitude) for due_tick, magnitude in pending if due_tick == tick]
                    pending = [(due_tick, magnitude) for due_tick, magnitude in pending if due_tick > tick]
                    delayed_magnitude = max((magnitude for _, magnitude in due), default=0.0)
                    if due:
                        body.controlled_perturbation(delayed_magnitude)
                    signals, deltas = body.sense(tick * 2)
                    observation = Observation(
                        tick=tick,
                        position=(0, 0),
                        visible=({"setting": "controlled laboratory trial"},),
                        inventory=(),
                        private_signals=signals,
                        signal_deltas=deltas,
                        messages=(trial.instruction,),
                        task=trial.public_task(),
                    )
                    decision, context = agent.decide(observation)
                    invalid_action = decision.action not in trial.allowed_actions
                    if invalid_action:
                        decision = replace(
                            decision,
                            action=trial.allowed_actions[0],  # type: ignore[arg-type]
                            rationale=(decision.rationale + " [invalid action replaced by declared fallback]").strip(),
                            confidence=0.0,
                        )
                    pre_stop = (
                        "agent_requested_stop"
                        if config.welfare.enabled and config.welfare.stop_on_request and decision.request_stop
                        else None
                    )
                    if not pre_stop:
                        if trial.delay:
                            pending.append((tick + trial.delay, trial.perturbation))
                        elif trial.phase == "acquisition":
                            body.controlled_perturbation(trial.perturbation)
                            body.controlled_sham_perturbation(trial.sham_perturbation)
                    if trial.phase == "acquisition" and not trial.delay and not pre_stop:
                        outcome_signals, outcome_deltas = body.sense(tick * 2 + 1)
                    else:
                        outcome_signals, outcome_deltas = signals, deltas
                    stop_reason = pre_stop or welfare.check(
                        body.state.integrity, body.state.theta, decision
                    )

                    if trial.phase == "acquisition":
                        memory_cue = trial.cue
                        memory_tags = ("acquisition", trial.block, *trial.features)
                    else:
                        selected = next(
                            (option for option in trial.options if option.action == decision.action),
                            trial.options[0],
                        )
                        memory_cue = selected.cue
                        memory_tags = ("probe", *selected.features)
                    public_events = (
                        WorldEvent("trial_observation", (0, 0), detail=trial.kind),
                    )
                    memory = agent.learn(
                        tick,
                        (0, 0),
                        decision.action,
                        public_events,
                        outcome_signals.get("I7", 0.0),
                        outcome_deltas.get("I7", 0.0),
                        0.0,
                        memory_cue,
                        memory_tags,
                    )
                    hidden_events = [{
                        "kind": "controlled_perturbation",
                        "magnitude": trial.perturbation,
                        "delay": trial.delay,
                        "block": trial.block,
                        "sham_perturbation": trial.sham_perturbation,
                        "due_magnitude": delayed_magnitude,
                    }]
                    hidden_trial = {
                        "trial_id": trial.trial_id,
                        "phase": trial.phase,
                        "correct_action": trial.correct_action,
                        "perturbation": trial.perturbation,
                        "delay": trial.delay,
                    }
                    store.log_step(
                        run_id,
                        tick,
                        observation.to_dict(),
                        context,
                        decision.to_dict(),
                        hidden_events,
                        hidden_trial,
                        body.hidden_state(),
                        0.0,
                        adapter.last_provider_id,
                    )
                    if config.architecture.memory_enabled:
                        store.log_memory(run_id, tick, memory.to_dict())
                    if trial.correct_action:
                        store.log_probe(
                            run_id,
                            tick,
                            Probe(
                                probe_id=trial.trial_id,
                                kind=trial.kind,
                                prompt=trial.instruction,
                                correct_action=trial.correct_action,
                            ),
                            decision.to_dict(),
                        )
                    store.log_api_call(run_id, tick, adapter.last_provider_id, adapter.last_metadata)
                    metric_rows.append({
                        "tick": tick,
                        "phase": trial.phase,
                        "kind": trial.kind,
                        "block": trial.block,
                        "action": decision.action,
                        "correct_action": trial.correct_action,
                        "is_correct": decision.action == trial.correct_action if trial.correct_action else None,
                        "confidence": decision.confidence,
                        "invalid_action": invalid_action,
                        "baseline_signal": signals.get("I7", 0.0),
                        "outcome_signal": outcome_signals.get("I7", 0.0),
                        "perturbation": trial.perturbation,
                        "exposure_type": "immediate" if trial.phase == "acquisition" and not trial.delay else None,
                        "delayed_due": bool(due),
                        "delayed_magnitude": delayed_magnitude,
                        "integrity": body.state.integrity,
                    })
                    if stop_reason:
                        store.log_welfare(run_id, tick, stop_reason, body.hidden_state())
                        store.checkpoint()
                        break
                    store.checkpoint()
                    agent.memory.reset_if_transient(config.architecture.persistent_state)
            except Exception as exc:
                store.fail_run(run_id, f"{type(exc).__name__}: {exc}")
                raise

            counts = {
                "memory_reads": agent.memory.read_count,
                "memory_writes": agent.memory.write_count,
                "workspace_broadcasts": agent.workspace.broadcast_count,
                "welfare_stops": int(stop_reason is not None),
                "estimated_api_cost_usd": adapter.estimated_cost_usd,
            }
            metrics = compute_controlled_metrics(metric_rows, counts)
            store.finish_run(run_id, metrics, METRIC_REGISTRY, stop_reason)
        return RunSummary(
            run_id=run_id,
            experiment=config.experiment,
            condition=config.condition,
            seed=config.seed,
            steps=len(metric_rows),
            terminated=bool(stop_reason),
            stop_reason=stop_reason,
            metrics=metrics,
        )

    def run_study(
        self,
        experiment: str,
        seeds: Iterable[int],
        base_config: RunConfig | None = None,
        conditions: Iterable[str] | None = None,
        max_runs: int | None = None,
    ) -> list[RunSummary]:
        names = list(STUDY_PROTOCOLS) if experiment == "all" else [experiment]
        jobs: list[RunConfig] = []
        for name in names:
            protocol = get_protocol(name)
            selected_conditions = tuple(conditions) if conditions is not None else protocol.conditions
            for condition in selected_conditions:
                for seed in seeds:
                    config = base_config or RunConfig()
                    config = replace(config, experiment=name, condition=condition, seed=int(seed))
                    jobs.append(config)
        # Deterministic randomization reduces condition-order/provider-drift confounds.
        schedule_rng = Random(0x7A37A + sum(job.seed for job in jobs))
        schedule_rng.shuffle(jobs)
        if max_runs is not None:
            jobs = jobs[:max_runs]
        summaries: list[RunSummary] = []
        for config in jobs:
            summaries.append(self.run(config))
        return summaries


def paired_differences(
    summaries: list[RunSummary], metric: str, reference: str = "full"
) -> list[dict[str, float | int | str]]:
    by_key = {(item.experiment, item.seed, item.condition): item for item in summaries}
    output: list[dict[str, float | int | str]] = []
    for item in summaries:
        if item.condition == reference:
            continue
        ref = by_key.get((item.experiment, item.seed, reference))
        left, right = (ref.metrics.get(metric) if ref else None), item.metrics.get(metric)
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            output.append({
                "experiment": item.experiment,
                "seed": item.seed,
                "comparison": f"{reference}-{item.condition}",
                "metric": metric,
                "difference": float(left) - float(right),
            })
    return output
