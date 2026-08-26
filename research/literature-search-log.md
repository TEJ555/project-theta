# Literature search log

## Search record

- Search date: 26 August 2026
- Coverage end date: 26 August 2026
- Protocol: `preregistration/literature-review-protocol-01.md`
- Raw result file: `research/literature-search-results.json`
- Search program: `scripts/literature_search.py`
- Deduplication and ranking program: `scripts/screen_literature.py`
- Maximum records retrieved per database and search family: 100

The search used five families: theory, artificial systems, embodiment, measurement,
and welfare. Exact query strings are stored in the raw result file and in the search
program. Publisher pages, PubMed records, DOI metadata, arXiv records, and citation
chaining were used to verify the final corpus.

## Database results

| Family | Database | Results reported | Records retrieved |
|---|---:|---:|---:|
| Artificial systems | arXiv | 410 | 100 |
| Artificial systems | Crossref | 1,013,496 | 100 |
| Artificial systems | OpenAlex | 345 | 100 |
| Artificial systems | PubMed | 351 | 100 |
| Embodiment | arXiv | 850 | 100 |
| Embodiment | Crossref | 1,775,988 | 100 |
| Embodiment | OpenAlex | 909 | 100 |
| Embodiment | PubMed | 2,517 | 100 |
| Measurement | arXiv | 3,308 | 100 |
| Measurement | Crossref | 2,847,607 | 100 |
| Measurement | OpenAlex | 6,675 | 100 |
| Measurement | PubMed | 4,262 | 100 |
| Theory | arXiv | 121 | 100 |
| Theory | Crossref | 1,426,471 | 100 |
| Theory | OpenAlex | 64 | 64 |
| Theory | PubMed | 726 | 100 |
| Welfare | arXiv | 513 | 100 |
| Welfare | Crossref | 10,498,606 | 100 |
| Welfare | OpenAlex | 52 | 52 |
| Welfare | PubMed | 558 | 100 |

The searches retrieved 1,916 records. DOI and normalized-title deduplication removed
116 duplicates, leaving 1,800 unique records.

Semantic Scholar returned HTTP 429 for all five queries, so it contributed no records.
This failure is preserved in the raw file. The very large Crossref counts show that
its bibliographic matching was broad and noisy. Retrieval was capped at 100 records
per search, so the review should not be described as an exhaustive census.

## Screening process

All 1,800 unique titles were processed by a deterministic relevance ranking. The
ranking gave weight to theory names, artificial-consciousness terms, measurement
terms, multiple-database retrieval, and citation counts. It was used only to order
records for inspection. It did not decide inclusion.

The primary reviewer assessed the first 100 ranked records and added seminal or recent
records found through backward citation searching, review bibliographies, PubMed, and
targeted title searches. Forty-seven records form the version 1.0 evidence corpus.
Forty-three DOI records were verified against Crossref on 26 August 2026. Four preprint
records were verified against arXiv. The checked metadata is stored in
`research/reference-verification.json`, and the bibliography is stored in
`references/project-theta.bib`.

The remaining search records have not received independent human screening. A second
reviewer should screen the ranked set, audit a random sample of lower-ranked records,
and resolve disagreements before journal submission or any claim of exhaustive
coverage.

## Reproduction

From the repository root:

```powershell
python scripts/literature_search.py
python scripts/screen_literature.py --limit 100
python scripts/verify_references.py
python scripts/build_bibliography.py
```

Network providers can change rankings and metadata. Preserve the dated raw file when
updating the search.

## Amendments

No search amendments have been made since the protocol was frozen.
