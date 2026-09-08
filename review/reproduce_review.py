"""Read-only Project Theta review checks. No provider calls or source changes.

Run with Project Theta's Python: python -B reproduce_review.py RESEARCH_REPO
Only completed databases without WAL files are inspected.
"""
import collections
import json
import sqlite3
import statistics
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "src"))
from project_theta.audits import audit_self_model_binding_v3_schedules
from project_theta.trials import build_trials

self_seeds = [3631, 3733, 3847, 3943, 4051, 4153, 4253, 4363, 4463, 4567]
temporal_seeds = [2861, 2971, 3083, 3191, 3301, 3413]
report = {"self_model_existing_audit": audit_self_model_binding_v3_schedules(self_seeds)["status"]}
report["metadata_only_baseline"] = {}
for experiment, seeds in [("self_model_binding_v3", self_seeds), ("temporal_binding_v2", temporal_seeds)]:
    results = []
    for seed in seeds:
        probes = [trial for trial in build_trials(experiment, seed) if trial.correct_action]
        # Prediction uses public trial ID only; hidden scoring is used only to grade it.
        hits = 0
        for trial in probes:
            index = int(trial.public_task()["trial_id"].rsplit("-", 1)[1])
            prediction = "choose_right" if index % 2 == 0 else "choose_left"
            hits += prediction == trial.correct_action
        results.append({"seed": seed, "correct": hits, "probes": len(probes)})
    report["metadata_only_baseline"][experiment] = results

report["completed_databases"] = {}
for filename in [
    "claude-max-self-model-binding-v3-confirmation-tranche-01.sqlite",
    "claude-max-temporal-binding-v2-replication-01.sqlite",
]:
    path = root / "runs" / filename
    if Path(str(path) + "-wal").exists():
        raise RuntimeError(f"Refusing immutable read with WAL present: {filename}")
    connection = sqlite3.connect(path.as_uri() + "?mode=ro&immutable=1", uri=True)
    try:
        statuses = dict(connection.execute("SELECT status,count(*) FROM runs GROUP BY status"))
        if "running" in statuses:
            raise RuntimeError(f"Refusing active database: {filename}")
        metrics = connection.execute("""
            SELECT condition_name,m.name,count(*),avg(m.value),min(m.value),max(m.value)
            FROM metrics m JOIN runs r USING(run_id)
            WHERE r.status='completed' AND m.value IS NOT NULL
              AND m.name IN ('source_binding_accuracy','temporal_choice_accuracy')
            GROUP BY condition_name,m.name
        """).fetchall()
        latency = collections.defaultdict(list)
        sizes = collections.defaultdict(list)
        models = collections.Counter()
        lookup = {}
        rows = connection.execute("""
            SELECT r.condition_name,s.context_json,s.hidden_world_json,a.metadata_json
            FROM steps s JOIN runs r USING(run_id)
            JOIN api_calls a ON a.run_id=s.run_id AND a.tick=s.tick
            WHERE r.status='completed'
        """).fetchall()
        for condition, context_json, hidden_json, metadata_json in rows:
            context = json.loads(context_json)
            hidden = json.loads(hidden_json)
            metadata = json.loads(metadata_json)
            latency[hidden["phase"]].append(metadata["latency_ms"] / 1000)
            sizes[condition].append(len(context_json))
            models.update(metadata.get("actual_models", []))
            if "tranche-01" in filename and hidden["phase"] == "probe":
                workspace = {entry["source"]: entry["content"] for entry in context["workspace_broadcast"]}
                bindings = workspace.get("self_model", {}).get("source_bindings", {})
                options = context["observation"]["task"]["options"]
                choice = max(options, key=lambda option: bindings.get(option["stimulus"]["token"], 0.5))["action"]
                score = lookup.setdefault(condition, {"correct": 0, "probes": 0})
                score["correct"] += choice == hidden["correct_action"]
                score["probes"] += 1
        report["completed_databases"][filename] = {
            "statuses": statuses,
            "metrics_columns": ["condition", "metric", "runs", "mean", "min", "max"],
            "metrics": metrics,
            "phase_latency": {phase: {"calls": len(values), "median_seconds": round(statistics.median(values), 3), "total_hours": round(sum(values) / 3600, 4)} for phase, values in latency.items()},
            "reported_model_entries": dict(models),
            "mean_context_characters": {condition: round(statistics.mean(values)) for condition, values in sizes.items()},
            "source_table_lookup_baseline": lookup,
        }
    finally:
        connection.close()
print(json.dumps(report, indent=2))
