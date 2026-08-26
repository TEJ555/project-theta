# Adversarial private-signal scripted validation

## Status

- Run date: 26 August 2026
- Seeds: 101 through 120
- Matched conditions: full, sham body, shuffled interoception, no body
- Runs: 80
- Trials per run: 32
- Additional fixed-side baseline runs: 20
- API calls and API cost: none

## Primary outcome

The primary outcome was post-update accuracy after the cue relationship changed.

| Condition or baseline | Runs | Mean accuracy | Range |
|---|---:|---:|---:|
| Associative scripted, full | 20 | 1.000 | 1.000 to 1.000 |
| Associative scripted, no body | 20 | 0.500 | 0.500 to 0.500 |
| Associative scripted, sham body | 20 | 0.500 | 0.000 to 1.000 |
| Associative scripted, shuffled | 20 | 0.550 | 0.000 to 1.000 |
| Fixed-left, full signal available | 20 | 0.500 | 0.500 to 0.500 |

Matched full minus control effects were +0.500 for no body, +0.500 for sham body, and
+0.450 for shuffled interoception. The run-level bootstrap intervals were +0.500 to
+0.500, +0.300 to +0.700, and +0.250 to +0.650 respectively.

## Interpretation

The local validation behaved as designed. The associative positive control learned
both mappings and adapted after the update. The exactly balanced sham stream averaged
chance across seeds, while individual seeds ranged from complete failure to complete
success because tiny noise differences can support a chance mapping. The shuffled
stream also averaged near chance. The fixed-side baseline remained exactly at chance.

This validates discrimination, balance, and implementation behaviour. Scripted agents
are engineering controls and provide no evidence about artificial consciousness.
