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

Version 0.2 controlled trials, paired analysis, recovery and worker infrastructure are
implemented. The next milestone is the API pilot gate in `ROADMAP.md`: add recorded
provider fixtures, matched-context padding, mapping/delay reversal and blinded exports.
Preserve schema 2 through an explicit migration.

Constraints for any coding agent:

- never describe a result as proof or detection of phenomenal consciousness;
- never weaken/bypass welfare stops to make a run complete;
- never expose hidden world/body state to the subject adapter;
- never silently fall back to the scripted adapter after provider failure;
- preserve deterministic seeds and add a matched negative control;
- update preregistration-facing docs and tests with each protocol change.

Before accepting changes, inspect the exact adapter context in the SQLite `steps`
table for leakage and compare full/ablation component counts.
