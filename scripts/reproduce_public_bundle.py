from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from statistics import fmean


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify and summarize a public Theta bundle")
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    root = args.bundle.resolve()
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    grouped: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for item in manifest["exports"]:
        path = root / item["file"]
        if sha256(path) != item["sha256"]:
            raise RuntimeError(f"Checksum failed: {path.name}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        for record in payload["runs"]:
            run = record["run"]
            if run["status"] != "completed":
                continue
            for name, metric in record["metrics"].items():
                value = metric["value"]
                if metric["class"] == "behavioural" and isinstance(value, (int, float)):
                    grouped[(run["experiment"], run["condition"], name)].append(float(value))
    rows = [
        {
            "experiment": experiment,
            "condition": condition,
            "metric": metric,
            "n": len(values),
            "mean": round(fmean(values), 6),
            "minimum": min(values),
            "maximum": max(values),
        }
        for (experiment, condition, metric), values in sorted(grouped.items())
    ]
    print(json.dumps({"checksums": "pass", "summaries": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
