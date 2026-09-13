# NVIDIA GPT OSS V6 internal replication 01

## Administrative record

- Frozen: 13 September 2026, before any call on the replication seeds
- Registration revision: the Git commit containing this document
- Prior exploratory data: seed 3101, inspected before this registration
- Protocol: `endogenous_agency_v6`
- Provider route: NVIDIA hosted NIM development endpoint
- Exact requested and required model: `openai/gpt-oss-20b`
- Reasoning effort: low
- Temperature: 0.0
- Fresh replication seeds: 3329, 3350, 3221, 3265, 3657, 3893, 3363,
  3242, 3324, 3749, 4003, 3417, 3268, 3397, and 3838
- Conditions: full, evidence only, journal only, permuted journal, and neutral journal
- Runs: 75
- Decisions per run: 18
- Maximum hosted requests: 1,350
- Request timeout: 300 seconds
- Provider SDK retries per decision: up to 4
- Maximum attempts per seed-condition job: 2

This is an internal development replication. It is not confirmatory because the
design has not yet received independent methods review. Seed 3101 is excluded from
the replication estimates because it was inspected before this plan was frozen.

## Research question

Does the full system use model-authored persistent causal state more successfully
than registered controls that hide, neutralise, or corrupt that state?

The primary outcome is `agency_transfer_accuracy`, the fraction correct across six
exact-identity and six fresh-alias probes for each seed and condition. Fresh seeds are
the paired inferential units.

## Frozen execution order

Jobs are grouped by seed. The committed worker randomiser produces an exactly
balanced order: each condition appears in every ordinal position three times.

| Seed | 1 | 2 | 3 | 4 | 5 |
|---:|---|---|---|---|---|
| 3329 | Full | Evidence only | Journal only | Permuted journal | Neutral journal |
| 3350 | Evidence only | Journal only | Permuted journal | Neutral journal | Full |
| 3221 | Journal only | Permuted journal | Neutral journal | Full | Evidence only |
| 3265 | Permuted journal | Neutral journal | Full | Evidence only | Journal only |
| 3657 | Neutral journal | Full | Evidence only | Journal only | Permuted journal |
| 3893 | Full | Evidence only | Journal only | Permuted journal | Neutral journal |
| 3363 | Evidence only | Journal only | Permuted journal | Neutral journal | Full |
| 3242 | Journal only | Permuted journal | Neutral journal | Full | Evidence only |
| 3324 | Permuted journal | Neutral journal | Full | Evidence only | Journal only |
| 3749 | Neutral journal | Full | Evidence only | Journal only | Permuted journal |
| 4003 | Full | Evidence only | Journal only | Permuted journal | Neutral journal |
| 3417 | Evidence only | Journal only | Permuted journal | Neutral journal | Full |
| 3268 | Journal only | Permuted journal | Neutral journal | Full | Evidence only |
| 3397 | Permuted journal | Neutral journal | Full | Evidence only | Journal only |
| 3838 | Neutral journal | Full | Evidence only | Journal only | Permuted journal |

The table above is generated from the committed worker algorithm and is part of the
frozen plan. If code and table disagree, execution must stop before interpretation.

## Hypotheses and comparisons

The primary comparison is the seed-paired difference between full and evidence only.
The directional hypothesis is that the full condition performs better.

Secondary mechanism comparisons are full minus neutral journal and full minus
permuted journal. Full minus journal only is reported as a sufficiency diagnostic.
No individual secondary result can rescue a failed primary comparison.

For each condition, report the mean, median, range, and a deterministic seed-bootstrap
95 percent interval. For every full-minus-control comparison, report the mean and
median paired difference, bootstrap interval, exact two-sided sign test with ties
omitted, number of positive pairs, number of ties, and all seed-level scores.

## Progression criteria

The study progresses to outside methods review only if every operational requirement
and every primary performance requirement passes:

- all 75 planned runs complete without a welfare stop;
- every run contains exactly 18 valid model decisions;
- every provider response reports the required model identifier;
- schedule, blinding, shortcut, execution, and metric-coverage audits pass;
- mean full-condition accuracy is at least 0.75;
- mean full-minus-evidence-only accuracy is at least 0.20;
- full exceeds evidence only in at least 10 of 15 paired seeds.

The neutral and permuted journal comparisons are mechanism diagnostics. Their effect
sizes and uncertainty are reported whether favourable, null, or reversed. They are
not additional primary gates because the one-seed pilot was used to develop them.

Passing permits independent review and a new active-intervention protocol. Failing
triggers protocol diagnosis. Neither outcome permits a consciousness claim.

## Integrity and stopping rules

The worker requires a clean committed code revision. It preserves interrupted and
failed attempts rather than deleting them. A duplicate completion, unrecognised prior
failure, exhausted two-attempt limit, model-identity mismatch, malformed decision,
welfare stop, or failed audit blocks automatic interpretation.

There is no performance-based early stopping. Interim scores may be monitored only
for operational failures. All 75 planned jobs remain in the analysis once started.

## Interpretation boundary

The strongest permitted positive conclusion is that this scaffolded model system
uses its own persistent causal estimates under controlled information interventions
on this benchmark. That would be a behavioural and computational result. It would not
establish subjective experience or phenomenal consciousness.
