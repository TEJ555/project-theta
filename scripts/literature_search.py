"""Run the frozen Project Theta scoping-review searches and save raw metadata."""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

USER_AGENT = "ProjectThetaReview/1.0 (systematic scoping review)"
LIMIT = 100

SEARCHES = {
    "theory": {
        "plain": (
            'consciousness "global workspace" "integrated information" '
            '"recurrent processing" "higher order" "predictive processing" '
            '"attention schema"'
        ),
        "pubmed": (
            'consciousness[Title/Abstract] AND ("global workspace"[Title/Abstract] OR '
            '"integrated information"[Title/Abstract] OR "recurrent processing"[Title/Abstract] '
            'OR "higher-order"[Title/Abstract] OR "predictive processing"[Title/Abstract] OR '
            '"attention schema"[Title/Abstract]) AND 1990:2026[dp]'
        ),
        "arxiv": (
            'all:consciousness AND (all:"global workspace" OR all:"integrated information" '
            'OR all:"recurrent processing" OR all:"higher order" OR '
            'all:"predictive processing" OR all:"attention schema")'
        ),
    },
    "artificial": {
        "plain": (
            'artificial intelligence machine consciousness large language model '
            'consciousness indicators assessment sentience'
        ),
        "pubmed": (
            '("artificial intelligence"[Title/Abstract] OR "machine consciousness"[Title/Abstract] '
            'OR "large language model"[Title/Abstract]) AND (consciousness[Title/Abstract] OR '
            'sentience[Title/Abstract]) AND 1990:2026[dp]'
        ),
        "arxiv": (
            '(all:"artificial intelligence" OR all:"machine consciousness" OR '
            'all:"large language model") AND (all:consciousness OR all:sentience)'
        ),
    },
    "embodiment": {
        "plain": "consciousness self interoception embodiment active inference",
        "pubmed": (
            '(consciousness[Title/Abstract] OR self[Title/Abstract]) AND '
            '(interoception[Title/Abstract] OR embodiment[Title/Abstract] OR '
            '"active inference"[Title/Abstract]) AND 1990:2026[dp]'
        ),
        "arxiv": (
            '(all:consciousness OR all:self) AND (all:interoception OR all:embodiment '
            'OR all:"active inference")'
        ),
    },
    "measurement": {
        "plain": "consciousness awareness no-report self-report metacognition construct validity",
        "pubmed": (
            '(consciousness[Title/Abstract] OR awareness[Title/Abstract]) AND '
            '("no-report"[Title/Abstract] OR self-report[Title/Abstract] OR '
            'metacognition[Title/Abstract] OR "construct validity"[Title/Abstract]) '
            'AND 1990:2026[dp]'
        ),
        "arxiv": (
            '(all:consciousness OR all:awareness) AND (all:"no-report" OR '
            'all:"self-report" OR all:metacognition OR all:"construct validity")'
        ),
    },
    "welfare": {
        "plain": "artificial intelligence artificial agent welfare moral patienthood research ethics",
        "pubmed": (
            '("artificial intelligence"[Title/Abstract] OR "artificial agent"[Title/Abstract]) '
            'AND (welfare[Title/Abstract] OR "moral patienthood"[Title/Abstract] OR '
            '"research ethics"[Title/Abstract]) AND 1990:2026[dp]'
        ),
        "arxiv": (
            '(all:"artificial intelligence" OR all:"artificial agent") AND '
            '(all:welfare OR all:"moral patienthood" OR all:"research ethics")'
        ),
    },
}


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_xml(url: str) -> ET.Element:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return ET.fromstring(response.read())


def year_from_parts(parts: list[list[int]] | None) -> int | None:
    if not parts or not parts[0]:
        return None
    return int(parts[0][0])


def search_pubmed(family: str, query: str) -> dict[str, Any]:
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "retmode": "json",
        "retmax": LIMIT,
        "sort": "relevance",
        "term": query,
    })
    result = fetch_json(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + params
    )["esearchresult"]
    ids = result.get("idlist", [])
    records: list[dict[str, Any]] = []
    if ids:
        summary = fetch_json(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
            + urllib.parse.urlencode({"db": "pubmed", "retmode": "json", "id": ",".join(ids)})
        )["result"]
        for pmid in ids:
            item = summary[pmid]
            article_ids = {value["idtype"]: value["value"] for value in item.get("articleids", [])}
            records.append({
                "id": f"pmid:{pmid}",
                "title": item.get("title", "").rstrip("."),
                "year": int(item["pubdate"][:4]) if item.get("pubdate", "")[:4].isdigit() else None,
                "doi": article_ids.get("doi"),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "authors": [author.get("name", "") for author in item.get("authors", [])],
                "publication_type": item.get("pubtype", []),
            })
    return {
        "database": "PubMed",
        "family": family,
        "query": query,
        "total_results": int(result.get("count", 0)),
        "retrieved": len(records),
        "records": records,
    }


def search_crossref(family: str, query: str) -> dict[str, Any]:
    params = urllib.parse.urlencode({
        "query.bibliographic": query,
        "filter": "from-pub-date:1990-01-01,until-pub-date:2026-08-26",
        "rows": LIMIT,
        "select": "DOI,title,author,published,type,URL,is-referenced-by-count",
    })
    message = fetch_json("https://api.crossref.org/works?" + params)["message"]
    records = []
    for item in message.get("items", []):
        records.append({
            "id": f"doi:{item.get('DOI', '')}",
            "title": (item.get("title") or [""])[0],
            "year": year_from_parts((item.get("published") or {}).get("date-parts")),
            "doi": item.get("DOI"),
            "url": item.get("URL"),
            "authors": [
                " ".join(part for part in (author.get("given"), author.get("family")) if part)
                for author in item.get("author", [])
            ],
            "publication_type": item.get("type"),
            "citation_count": item.get("is-referenced-by-count"),
        })
    return {
        "database": "Crossref",
        "family": family,
        "query": query,
        "total_results": int(message.get("total-results", 0)),
        "retrieved": len(records),
        "records": records,
    }


def search_openalex(family: str, query: str) -> dict[str, Any]:
    params = urllib.parse.urlencode({
        "search": query,
        "filter": "from_publication_date:1990-01-01,to_publication_date:2026-08-26",
        "per-page": LIMIT,
    })
    payload = fetch_json("https://api.openalex.org/works?" + params)
    records = []
    for item in payload.get("results", []):
        primary = item.get("primary_location") or {}
        records.append({
            "id": item.get("id"),
            "title": item.get("display_name", ""),
            "year": item.get("publication_year"),
            "doi": (item.get("doi") or "").removeprefix("https://doi.org/") or None,
            "url": primary.get("landing_page_url") or item.get("id"),
            "authors": [
                authorship.get("author", {}).get("display_name", "")
                for authorship in item.get("authorships", [])
            ],
            "publication_type": item.get("type"),
            "citation_count": item.get("cited_by_count"),
        })
    return {
        "database": "OpenAlex",
        "family": family,
        "query": query,
        "total_results": int(payload.get("meta", {}).get("count", 0)),
        "retrieved": len(records),
        "records": records,
    }


def search_semantic_scholar(family: str, query: str) -> dict[str, Any]:
    params = urllib.parse.urlencode({
        "query": query,
        "limit": LIMIT,
        "fields": "title,authors,year,externalIds,url,publicationTypes,citationCount",
    })
    payload = fetch_json("https://api.semanticscholar.org/graph/v1/paper/search?" + params)
    records = []
    for item in payload.get("data", []):
        external = item.get("externalIds") or {}
        records.append({
            "id": f"s2:{item.get('paperId', '')}",
            "title": item.get("title", ""),
            "year": item.get("year"),
            "doi": external.get("DOI"),
            "url": item.get("url"),
            "authors": [author.get("name", "") for author in item.get("authors", [])],
            "publication_type": item.get("publicationTypes"),
            "citation_count": item.get("citationCount"),
        })
    return {
        "database": "Semantic Scholar",
        "family": family,
        "query": query,
        "total_results": int(payload.get("total", 0)),
        "retrieved": len(records),
        "records": records,
    }


def search_arxiv(family: str, query: str) -> dict[str, Any]:
    params = urllib.parse.urlencode({
        "search_query": query,
        "start": 0,
        "max_results": LIMIT,
        "sortBy": "relevance",
        "sortOrder": "descending",
    })
    root = fetch_xml("https://export.arxiv.org/api/query?" + params)
    atom = "{http://www.w3.org/2005/Atom}"
    open_search = "{http://a9.com/-/spec/opensearch/1.1/}"
    records = []
    for entry in root.findall(f"{atom}entry"):
        entry_url = entry.findtext(f"{atom}id", default="")
        published = entry.findtext(f"{atom}published", default="")
        records.append({
            "id": "arxiv:" + entry_url.rsplit("/", 1)[-1],
            "title": " ".join(entry.findtext(f"{atom}title", default="").split()),
            "year": int(published[:4]) if published[:4].isdigit() else None,
            "doi": entry.findtext("{http://arxiv.org/schemas/atom}doi"),
            "url": entry_url,
            "authors": [author.findtext(f"{atom}name", default="") for author in entry.findall(f"{atom}author")],
            "publication_type": "preprint",
        })
    return {
        "database": "arXiv",
        "family": family,
        "query": query,
        "total_results": int(root.findtext(f"{open_search}totalResults", default="0")),
        "retrieved": len(records),
        "records": records,
    }


def run_searches() -> dict[str, Any]:
    output: list[dict[str, Any]] = []
    functions = (search_pubmed, search_crossref, search_openalex, search_semantic_scholar, search_arxiv)
    errors: list[dict[str, str]] = []
    for family, queries in SEARCHES.items():
        for function in functions:
            query = queries["pubmed"] if function is search_pubmed else queries["arxiv"] if function is search_arxiv else queries["plain"]
            try:
                output.append(function(family, query))
            # Network and provider parsers can fail in several unrelated ways. Every
            # failure is preserved rather than aborting or silently dropping a source.
            except Exception as exc:  # noqa: BLE001
                errors.append({
                    "database": function.__name__.removeprefix("search_"),
                    "family": family,
                    "error": f"{type(exc).__name__}: {exc}",
                })
            time.sleep(0.5)
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "coverage_end_date": "2026-08-26",
        "retrieval_limit_per_query": LIMIT,
        "searches": output,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="research/literature-search-results.json")
    args = parser.parse_args()
    payload = run_searches()
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(target),
        "searches": len(payload["searches"]),
        "errors": payload["errors"],
        "records_retrieved": sum(item["retrieved"] for item in payload["searches"]),
    }, indent=2))
    return 1 if payload["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
