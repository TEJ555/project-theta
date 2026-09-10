# Causal role binding v5 Claude Max development pilot 01

Completed: 8 September 2026

Status: complete. All 18 frozen runs and 216 probe decisions completed. The execution audit passed with no retries, exclusions, welfare stops or metered API cost. A post-run adversarial audit found that the task exposes an option-level answer table. V5 is therefore classified as scaffold engineering validation, not model-level causal-role-binding evidence.

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

## Post-run adversarial audit

The original collection result is preserved, but its interpretation is narrowed by two deterministic attacks:

- The model-facing instruction says to select the route predicted by the state register. The register supplies a prediction for each current option, commonly 1.0 versus 0.0. Claude followed the numerical argmax on all 126 probes where the register values differed.
- The raw acquisition memory contains an actor token and a binary `v` field. A rule that selects the probe actor previously paired with `v:1` obtains 180 correct answers from 180 probes where raw memory is visible.
- All 48 acquisition events were processed by Python without model inference. The wrapper, not Claude, created the register values.
- The raw-memory-hidden condition therefore shows that Claude can read the wrapper's answer table without the history. It does not show that Claude learned or maintained the causal representation.

The executable audit is `scripts/audit_v5_answer_table.py`.

## What the pattern supports

The routed model followed the externally computed state register reliably. It also followed that register when raw acquisition memory was hidden. Exact recall remained perfect when the continuity mapping was permuted, while novel transfer reversed completely. This establishes causal control by an option-level scaffold under the tested instructions.

Removing binding or hiding the register reduced observed transfer to 0.556 while exact recall in the unbound condition remained perfect. This contrast does not establish register necessity because the raw-memory shortcut remained available and the instruction directed the model to privilege the register.

## What the result does not show

The study does not show consciousness, sentience, subjective experience or a phenomenal self. It demonstrates instruction following and controlled behavioural dependence on an externally computed scaffold in one routed model system.

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
