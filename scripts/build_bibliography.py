"""Build the checked BibTeX bibliography from verified reference metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ARXIV_RECORDS = [
    {
        "key": "butlin2023consciousness",
        "authors": (
            "Patrick Butlin and Robert Long and Eric Elmoznino and Yoshua Bengio and "
            "Jonathan Birch and Axel Constant and George Deane and Stephen M. Fleming and others"
        ),
        "title": "Consciousness in Artificial Intelligence: Insights from the Science of Consciousness",
        "year": "2023",
        "id": "2308.08708",
    },
    {
        "key": "chalmers2023llm",
        "authors": "David J. Chalmers",
        "title": "Could a Large Language Model Be Conscious?",
        "year": "2023",
        "id": "2303.07103",
    },
    {
        "key": "long2024welfare",
        "authors": (
            "Robert Long and Jeff Sebo and Patrick Butlin and Kathleen Finlinson and Kyle Fish and "
            "Jacqueline Harding and Jacob Pfau and Toni Sims and Jonathan Birch and David Chalmers"
        ),
        "title": "Taking AI Welfare Seriously",
        "year": "2024",
        "id": "2411.00986",
    },
    {
        "key": "butlin2025principles",
        "authors": "Patrick Butlin and Theodoros Lappas",
        "title": "Principles for Responsible AI Consciousness Research",
        "year": "2025",
        "id": "2501.07290",
    },
]


def clean(value: Any) -> str:
    return str(value or "").replace("&amp;", "and").replace("{", "").replace("}", "")


def citation_key(record: dict[str, Any], used: set[str]) -> str:
    family = "source"
    named_authors = [author for author in record.get("authors", []) if author.strip()]
    if named_authors:
        family = re.sub(r"[^a-z]", "", named_authors[0].split()[-1].lower()) or "source"
    year = str(record["published"][0][0])
    word = next((w for w in re.findall(r"[A-Za-z]+", record["title"].lower()) if len(w) > 4), "work")
    base = f"{family}{year}{word}"
    key = base
    suffix = ord("a")
    while key in used:
        key = base + chr(suffix)
        suffix += 1
    used.add(key)
    return key


def main() -> int:
    payload = json.loads(Path("research/reference-verification.json").read_text(encoding="utf-8"))
    target = Path("references/project-theta.bib")
    target.parent.mkdir(parents=True, exist_ok=True)
    used: set[str] = set()
    entries = []
    for record in payload["records"]:
        key = citation_key(record, used)
        fields = {
            "author": " and ".join(clean(a) for a in record["authors"] if a.strip()),
            "title": "{" + clean(record["title"]) + "}",
            "journal": clean(record["container"]),
            "year": str(record["published"][0][0]),
            "volume": clean(record.get("volume")),
            "number": clean(record.get("issue")),
            "pages": clean(record.get("pages")),
            "doi": clean(record["doi"]).lower(),
            "url": "https://doi.org/" + clean(record["doi"]).lower(),
        }
        lines = [f"@article{{{key},"]
        lines.extend(f"  {name} = {{{value}}}," for name, value in fields.items() if value)
        lines.append("}")
        entries.append("\n".join(lines))
    for record in ARXIV_RECORDS:
        entries.append(
            "\n".join([
                f"@article{{{record['key']},",
                f"  author = {{{record['authors']}}},",
                f"  title = {{{{{record['title']}}}}},",
                f"  year = {{{record['year']}}},",
                f"  journal = {{arXiv preprint arXiv:{record['id']}}},",
                f"  doi = {{10.48550/arXiv.{record['id']}}},",
                f"  url = {{https://arxiv.org/abs/{record['id']}}},",
                "}",
            ])
        )
    target.write_text("\n\n".join(entries) + "\n", encoding="utf-8")
    print(json.dumps({"entries": len(entries), "output": str(target)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
