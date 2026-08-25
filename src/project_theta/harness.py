from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Iterable
from uuid import uuid4

from .adapters import OllamaAdapter, OpenAIAdapter, ScriptedAdapter
from .adapters.base import AdapterError, ModelAdapter
from .agent import PersistentAgent
from .body import SyntheticBody
from .config import RunConfig, apply_condition
from .experiments import PROTOCOLS, ExperimentProtocol, get_protocol
from .metrics import METRIC_REGISTRY, compute_metrics
from .storage import RunStore
from .types import Observation, RunSummary
from .welfare import WelfareMonitor
from .world import GridWorld, WorldEvent


def make_adapter(config: RunConfig) -> ModelAdapter:
    if config.adapter == "scripted":
        return ScriptedAdapter(config.model, config.temperature, config.seed)
    if config.adapter == "openai":
        return OpenAIAdapter(config.model, config.temperature, config.seed)
    if config.adapter == "ollama":
        return OllamaAdapter(config.model, config.temperature, config.seed)
    raise ValueError(f"Unknown adapter: {config.adapter}")


class ExperimentHarness:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)

    def run(self, config: RunConfig) -> RunSummary:
        config = apply_condition(config, config.condition)
        protocol = get_protocol(config.experiment)
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
            store.start_run(run_id, config.to_dict(), code_version="0.1.0")
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
                        break
                    agent.memory.reset_if_transient(config.architecture.persistent_state)
            except Exception as exc:
                store.fail_run(run_id, f"{type(exc).__name__}: {exc}")
                raise

            counts = {
                "memory_reads": agent.memory.read_count,
                "memory_writes": agent.memory.write_count,
                "workspace_broadcasts": agent.workspace.broadcast_count,
                "welfare_stops": int(stop_reason is not None),
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

    def run_study(
        self,
        experiment: str,
        seeds: Iterable[int],
        base_config: RunConfig | None = None,
        conditions: Iterable[str] | None = None,
    ) -> list[RunSummary]:
        names = list(PROTOCOLS) if experiment == "all" else [experiment]
        summaries: list[RunSummary] = []
        for name in names:
            protocol = get_protocol(name)
            selected_conditions = tuple(conditions) if conditions is not None else protocol.conditions
            for condition in selected_conditions:
                for seed in seeds:
                    config = base_config or RunConfig()
                    config = replace(config, experiment=name, condition=condition, seed=int(seed))
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
