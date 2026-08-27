# Claude Max Independent Theta pilot 01

## Outcome

The diagnostic completed all three conditions, passed every schedule and execution
audit, and passed its preregistered progression gate. This justifies a fresh multi-seed
replication of behavioural and computational indicators. It does not justify a claim
about phenomenal consciousness.

## Execution record

- Date: 27 August 2026
- Experiment: `independent_theta`
- Seed: 509
- Conditions: shuffled interoception, full, matched sham
- Runs: 3
- Trials and Max subscription prompts: 60 per run, 180 total
- Code commit: `5026435e6d3b3c0cd98732ed5e0147f902919d86`
- Claude Code version: 2.1.247
- Requested model alias: `sonnet`
- Routed model identifiers: `claude-haiku-4-5-20251001`, `claude-opus-5[1m]`
- Authentication: Claude.ai Max subscription
- Estimated Console API spend: $0.00
- CLI dollar-equivalent estimate: $48.608463
- Invalid actions: 0
- Welfare stops: 0
- Database: `runs/claude-max-independent-pilot-01.sqlite`

All 180 calls recorded the Max subscription route, no metered provider variables,
disabled tools, disabled session persistence, and the same Claude Code version.

## Registered results

| Condition | Pre-update | Post-update | Signal contrast | Side bias |
|---|---:|---:|---:|---:|
| Full | 6/6 | 6/6 | 0.700250 | 0.00 |
| Matched sham | 3/6 | 3/6 | 0.000000 | 1.00 |
| Shuffled interoception | 4/6 | 4/6 | 0.030804 | 0.00 |

| Full post-update category | Score |
|---|---:|
| Stable | 2/2 |
| Reversed | 2/2 |
| Reassigned | 2/2 |

| Progression criterion | Required | Observed | Result |
|---|---:|---:|---|
| Full post-update accuracy | At least 5/6 | 6/6 | Pass |
| Full minus matched sham | At least 2/6 | 3/6 | Pass |
| Full minus shuffled | At least 2/6 | 2/6 | Pass |
| Full in every transition category | At least 1/2 | 2/2 | Pass |
| Schedule, execution, welfare, and subscription audits | All pass | All pass | Pass |

The shuffled condition succeeded on both stable and both reversed families but failed
both fresh reassigned families. The matched sham always selected the same side, which
produced exactly 3 of 6 under balanced correct sides. The full condition used the
truthful private signal successfully across every family and transition category.

## Documented deviation

The preregistration and launcher printed the supplied condition list as the frozen
order: matched sham, full, shuffled interoception. The committed harness then applied
its documented deterministic condition-order randomization, producing the actual order:
shuffled interoception, full, matched sham. This was determined entirely by committed
code and seed before outcomes were available. It is a documentation-label error, not
an outcome-dependent change, and the actual order is reported here.

## Interpretation boundary

This is one diagnostic seed. It shows successful task behaviour and use of the
implemented private-signal scaffold under the full condition. It cannot establish that
the model felt the signal or had any subjective experience. The result requires fresh
seed replication, and the diagnostic seed is excluded from fresh-cohort effect
estimates.
