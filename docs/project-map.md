# Project map

Project Theta has two maintained source surfaces.

## Research code

The GitHub repository contains protocols, simulations, adapters, preregistrations, tests, analyses and public data exports.

Primary status files:

- `docs/study-registry.md`
- `docs/decision-log.md`
- `docs/methods-correction-2026-09-06.md`
- `preregistration/self-model-binding-v4-development-01.md`

## Public website

The website is maintained as a separate Sites project and published at `https://projecttheta.org`.

The website should summarise the study registry rather than maintain conflicting status text. Any public result article must link positive findings, failures and later corrections together.

## Evidence handling

Working SQLite databases remain outside Git. Reviewed exports belong in `public-data/` and exclude provider session identifiers and raw provider metadata. Another researcher must be able to verify checksums and reproduce summary tables without making model calls.
