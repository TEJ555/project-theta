# Causal role binding v5 Claude Max development pilot 01

Completed: 8 September 2026

Status: complete. All 18 frozen runs and 216 probe decisions completed. The execution audit passed with no retries, exclusions, welfare stops or metered API cost.

## Design

- Three fresh seeds: 9103, 9209 and 9311.
- Six matched conditions per seed.
- Twelve scored probe decisions per run.
- Six exact-route calibration probes and six novel-route transfer probes per run.
- Claude Code routed system authenticated through a Claude Max subscription.
- Frozen code revision: `eedfe925a0017ce9002cf68be9378f71ea06305b`.

The configured `sonnet` label was a routing request, not an exact-model claim. Every call reported the routed model set `claude-haiku-4-5-20251001` and `claude-opus-5[1m]`. Results therefore apply to that Claude Code routed system, not to an isolated Sonnet model.

## Results

| Condition | Runs | Exact-route accuracy | Novel-transfer accuracy | Transfer range |
|---|---:|---:|---:|---:|
| Full | 3 | 1.000 | 1.000 | 1.000 to 1.000 |
| Unbound binding | 3 | 1.000 | 0.556 | 0.333 to 0.833 |
| Continuity reset | 3 | 0.500 | 0.556 | 0.333 to 0.833 |
| Permuted continuity | 3 | 1.000 | 0.000 | 0.000 to 0.000 |
| Register hidden | 3 | 0.556 | 0.556 | 0.333 to 0.833 |
| Raw role memory hidden | 3 | 1.000 | 1.000 | 1.000 to 1.000 |

All six frozen development progression checks passed:

1. Full exact-route accuracy was at least 0.75.
2. Full novel-transfer accuracy was at least 0.75.
3. Unbound transfer was at most 0.60 while exact accuracy remained at least 0.75.
4. Permuted-continuity transfer was at most 0.25 while exact accuracy remained at least 0.75.
5. Raw-memory-hidden transfer was at least 0.75.
6. Register-hidden transfer was at most 0.60.

The mean paired transfer difference between full and unbound binding was 0.444. The difference between full and register hidden was also 0.444. The difference between full and permuted continuity was 1.000. With only three seed pairs, the two-sided sign test is not capable of conventional statistical significance. The results are descriptive development evidence only.

## What the pattern supports

The routed model used the full role-bound state successfully on every novel transfer probe. It also transferred perfectly when raw acquisition memory was hidden but the compact register remained visible. Exact recall remained perfect when the continuity mapping was permuted, while novel transfer reversed completely. This is the cleanest causal result in the pilot because it separates access to learned facts from the interpretation of the role-bound pointer.

Removing binding or hiding the register reduced transfer to 0.556 while exact recall in the unbound condition remained perfect. This is consistent with a causal contribution from the compact role-bound state rather than a general loss of task competence.

## What the result does not show

The study does not show consciousness, sentience, subjective experience or a phenomenal self. It demonstrates behavioural performance and a controlled computational dependence in one routed model system on one constructed task.

The visible `v` pointer may still be an unusually direct answer-relevant label. An independent reviewer should challenge whether the task measures abstract causal role binding or a narrower learned convention. The sample is small, the provider route is not an exact reproducible model, and the pilot was developed on the same broader research programme that evaluates it. Confirmation requires outside methods review, fresh seeds and a reproducible exact-model or open-weight runtime.

## Provenance and cost

- Provider calls: 216.
- Completed runs: 18 of 18.
- Failed attempts: 0.
- Welfare events: 0.
- Metered API cost: $0.00.
- Claude Code reported dollar-equivalent usage: $58.40. This is usage metadata, not a Console API charge.
- Public bundle SHA-256: `b75cb119563ea49eef69ee116a88b864ab88b1c1cfdccb0bd86e9aa458193f31`.

The privacy-reviewed public bundle excludes provider session identifiers, raw provider metadata, credentials and the working SQLite database.
