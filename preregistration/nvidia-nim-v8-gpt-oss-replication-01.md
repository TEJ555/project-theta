# NVIDIA GPT OSS V8 internal replication 01

## Administrative record

- Frozen: 14 September 2026, before any provider call on the replication seeds
- Registration revision: the Git commit containing this document
- Inspected development data: seeds 5100 and 5101
- Protocol: `active_interoceptive_control_v8`
- Provider route: NVIDIA hosted NIM development endpoint
- Exact requested and required model: `openai/gpt-oss-20b`
- Reasoning effort: low
- Temperature: 0.0
- Fresh paired seeds: 5201, 5202, 5203, 5204, 5205, 5206, 5207, 5216,
  5226, 5231, 5237, and 5250
- Conditions: full, no memory, shuffled interoception, and no body
- Runs: 48
- Decisions per run: 24
- Maximum hosted requests: 1,152
- Request timeout: 300 seconds
- Provider SDK retries per decision: up to 4
- Maximum attempts per seed-condition job: 2, with retries restricted to recognised
  infrastructure interruptions

This is an internal replication, not an externally reviewed confirmatory study. The
development seeds are excluded from every replication estimate.

## Research question

Across fresh synthetic bodies, does the intact model and scaffold regulate a private
body signal more accurately than the same system receiving deterministically shuffled
interoception?

The primary outcome is `active_regulation_accuracy` across twelve scored probes per
seed and condition. Fresh seeds are the paired inferential units.

## Sample-size and seed rule

Twelve pairs are the smallest multiple of four that permits exact balance of four
condition positions and a two-sided exact sign test below 0.05 without requiring a
unanimous result. Ten positive pairs out of twelve, with no ties, produce a two-sided
sign-test probability below 0.05.

The seed set is the first lexicographic solution found in the inclusive candidate
range 5201 to 5400 that gives every condition each ordinal position exactly three
times and gives six bodies a left-lowering mapping and six a right-lowering mapping.
Selection used only committed schedule metadata. No provider response was generated
or inspected for any candidate replication seed.

## Frozen execution order

The committed worker deterministically produces this order:

| Seed | First | Second | Third | Fourth |
|---:|---|---|---|---|
| 5201 | No body | Shuffled interoception | No memory | Full |
| 5202 | No body | Shuffled interoception | No memory | Full |
| 5203 | No body | No memory | Full | Shuffled interoception |
| 5204 | No memory | Shuffled interoception | Full | No body |
| 5205 | Full | No body | Shuffled interoception | No memory |
| 5206 | No memory | No body | Full | Shuffled interoception |
| 5207 | Full | No body | Shuffled interoception | No memory |
| 5216 | Full | No memory | No body | Shuffled interoception |
| 5226 | Shuffled interoception | No memory | No body | Full |
| 5231 | No memory | Full | Shuffled interoception | No body |
| 5237 | Shuffled interoception | Full | No memory | No body |
| 5250 | Shuffled interoception | Full | No body | No memory |

Each condition appears exactly three times in every ordinal position. If the worker
and this table disagree, execution stops before interpretation.

## Hypotheses and analysis

The primary directional hypothesis is that full regulation accuracy exceeds shuffled
interoception accuracy. For each seed, calculate full minus shuffled interoception.
Report the mean and median paired difference, deterministic seed-bootstrap 95 percent
interval, exact two-sided sign test with ties omitted, positive-pair count, tie count,
and all seed-level scores.

Secondary mechanism comparisons are full minus no memory and full minus no body. The
secondary outcomes are fresh-alias transfer accuracy, regulation improvement, final
target error, prediction mean absolute error, and calibration compliance. All are
reported whether favourable, null, or reversed. Secondary outcomes cannot rescue a
failed primary result.

## Progression criteria

The replication progresses to outside methods review only if every operational rule
and every primary performance rule passes:

- all 48 planned runs complete without a welfare stop
- every run contains exactly 24 valid model decisions
- every provider response reports the required exact model identifier
- schedule, blinding, causality, execution, and metric audits pass
- mean full-condition regulation accuracy is at least 0.75
- mean full-minus-shuffled-interoception accuracy is at least 0.20
- full exceeds shuffled interoception in at least 10 of 12 paired seeds
- the exact two-sided sign test for the primary contrast is below 0.05
- mean full-condition fresh-alias transfer accuracy is at least 0.667

Failure of a performance criterion triggers diagnosis rather than redesigning or
extending this dataset. Passing permits outside methods review and design of a new
independent confirmation. Neither outcome permits a consciousness claim.

## Integrity and stopping rules

The worker requires a clean committed code revision. It preserves interrupted and
failed attempts rather than deleting them. A duplicate completion, unrecognised prior
failure, exhausted attempt limit, model-identity mismatch, malformed decision,
welfare stop, or failed audit blocks automatic interpretation.

There is no performance-based early stopping. Interim scores may be inspected only
for operational safety and failures. All 48 planned jobs remain in the analysis once
the replication begins.

## Interpretation boundary

The strongest permitted positive conclusion is that this model and scaffold learn
and use an action-to-private-body mapping under controlled information ablations on
this benchmark. This would be a behavioural and computational result. It would not
establish feeling, awareness, suffering, sentience, or phenomenal consciousness.
