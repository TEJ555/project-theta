"""Deduplicate and rank records from the frozen literature search.

The ranking is a screening aid. It does not make inclusion decisions.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

HIGH_VALUE_TERMS = {
    "artificial consciousness",
    "attention schema",
    "global neuronal workspace",
    "global workspace",
    "higher-order",
    "integrated information",
    "interoceptive inference",
    "machine consciousness",
    "no-report",
    "predictive processing",
    "recurrent processing",
}

RELEVANT_TERMS = {
    "active inference",
    "ai consciousness",
    "ai welfare",
    "conscious access",
    "consciousness indicator",
    "consciousness research",
    "consciousness theor",
    "construct validity",
    "embodied self",
    "interoception",
    "large language model",
    "metacognition",
    "moral patient",
    "self-model",
    "sentience",
    "synthetic phenomenology",
}


def normalized_title(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def normalized_doi(value: str | None) -> str:
    return (value or "").lower().removeprefix("https://doi.org/").strip()


def record_key(record: dict[str, Any]) -> tuple[str, str]:
    doi = normalized_doi(record.get("doi"))
    return ("doi", doi) if doi else ("title", normalized_title(record.get("title", "")))


def relevance_score(record: dict[str, Any], families: set[str], databases: set[str]) -> int:
    title = normalized_title(record.get("title", ""))
    score = sum(5 for term in HIGH_VALUE_TERMS if term in title)
    score += sum(2 for term in RELEVANT_TERMS if term in title)
    score += min(len(families), 3)
    score += min(len(databases), 3)
    citations = int(record.get("citation_count") or 0)
    if citations >= 500:
        score += 3
    elif citations >= 100:
        score += 2
    elif citations >= 20:
        score += 1
    return score


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="research/literature-search-results.json")
    parser.add_argument("--output", default="research/literature-screening-candidates.csv")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    unique: dict[tuple[str, str], dict[str, Any]] = {}
    raw_count = 0
    for search in payload["searches"]:
        for record in search["records"]:
            raw_count += 1
            key = record_key(record)
            if key not in unique:
                unique[key] = {
                    "record": record,
                    "families": set(),
                    "databases": set(),
                }
            unique[key]["families"].add(search["family"])
            unique[key]["databases"].add(search["database"])

    rows = []
    for entry in unique.values():
        record = entry["record"]
        score = relevance_score(record, entry["families"], entry["databases"])
        rows.append({
            "score": score,
            "title": record.get("title", ""),
            "year": record.get("year") or "",
            "doi": normalized_doi(record.get("doi")),
            "url": record.get("url") or "",
            "authors": "; ".join(record.get("authors") or []),
            "families": "; ".join(sorted(entry["families"])),
            "databases": "; ".join(sorted(entry["databases"])),
            "citation_count": record.get("citation_count") or "",
        })
    rows.sort(key=lambda row: (-int(row["score"]), -int(row["citation_count"] or 0), row["title"]))
    rows = rows[: args.limit]

    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({
        "raw_records": raw_count,
        "duplicates_removed": raw_count - len(unique),
        "unique_records": len(unique),
        "candidates_written": len(rows),
        "output": str(target),
        "notice": "Ranking only. Inclusion requires reviewer assessment.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
