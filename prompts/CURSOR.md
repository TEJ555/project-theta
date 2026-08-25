# Cursor continuation brief

Open this repository as the workspace. Read `README.md`, `docs/research-framing.md`,
`docs/ethics.md`, `docs/hypotheses.md`, and `docs/experiment-protocol.md` before editing.

Start with:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -v
theta demo --steps 24 --db runs/demo.sqlite
```

Recommended next milestone: implement confirmatory v0.2 forced-choice trials. Add a
procedural map generator with held-out causal mappings, a probe API separate from free
navigation, matched token budgets for ablations, raw numerator/denominator metrics,
and a blinded paired-analysis command. Preserve current schema through a migration.

Constraints for any coding agent:

- never describe a result as proof or detection of phenomenal consciousness;
- never weaken/bypass welfare stops to make a run complete;
- never expose hidden world/body state to the subject adapter;
- never silently fall back to the scripted adapter after provider failure;
- preserve deterministic seeds and add a matched negative control;
- update preregistration-facing docs and tests with each protocol change.

Before accepting changes, inspect the exact adapter context in the SQLite `steps`
table for leakage and compare full/ablation component counts.

