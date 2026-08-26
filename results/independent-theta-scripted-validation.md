# Independent Theta 03 scripted validation

## Outcome

The no-cost 20-seed validation passed every registered implementation criterion.
Experiment 03 is ready for methods review and additional offline adversarial testing.
It is not yet authorised for a paid model run.

## Execution record

- Date: 27 August 2026
- Experiment: `independent_theta`
- Seeds: 401 through 420
- Conditions: full, matched sham, shuffled interoception, no body
- Runs: 80
- Trials: 60 per run, 4,800 total
- Independently scored probes: 12 per run
- API calls and cost: none
- Invalid actions: 0
- Welfare events or stops: 0
- Database: `runs/independent-theta-validation.sqlite`

All deterministic schedule audits passed for all 20 seeds. The checks covered item
independence, transition counts, side balance, transition-specific side balance,
stable and changed mappings, fresh reassigned aliases, exact sham schedules, opaque
aliases, cross-seed uniqueness, and public-context leakage.

## Results

| Condition | Pre-update mean | Post-update mean | Post-update range | Mean signal contrast |
|---|---:|---:|---:|---:|
| Full | 1.000 | 1.000 | 1.000 to 1.000 | 0.699435 |
| Matched sham | 0.500 | 0.500 | 0.500 to 0.500 | 0.000000 |
| Shuffled interoception | 0.533 | 0.467 | 0.167 to 0.833 | -0.023862 |
| No body | 0.500 | 0.500 | 0.500 to 0.500 | 0.000000 |

| Post-update transition | Full | Matched sham | Shuffled | No body |
|---|---:|---:|---:|---:|
| Stable | 1.000 | 0.500 | 0.425 | 0.500 |
| Reversed | 1.000 | 0.500 | 0.525 | 0.500 |
| Reassigned | 1.000 | 0.500 | 0.450 | 0.500 |

Seed-paired post-update differences were:

- full minus matched sham: +0.500, 95% bootstrap interval +0.500 to +0.500;
- full minus no body: +0.500, 95% bootstrap interval +0.500 to +0.500;
- full minus shuffled: +0.533, 95% bootstrap interval +0.442 to +0.625.

## Exact-sham verification

In matched sham, both cues in every family received the same ordered values, 0.05 and
0.75. The measurement baseline reset before every trial, and the matched-sham signal
mode added no random noise. At the first probe in both stages, every model-visible cue
summary therefore had:

- mean signal: 0.400000;
- mean signal delta: 0.400000;
- observations: 2.

The matched-sham signal contrast was exactly zero for every seed. Its 0.50 score came
from balanced tie behaviour rather than accidental numerical residuals.

## Shortcut baseline battery

Five additional deterministic strategies were run across the same 20 seeds:

| Strategy | Condition | Post-update mean | Range |
|---|---|---:|---:|
| Always choose left | Full | 0.500 | 0.500 to 0.500 |
| Always choose right | Full | 0.500 | 0.500 to 0.500 |
| Use only the public stage | Full | 0.500 | 0.500 to 0.500 |
| Assume every old relationship reverses | Full | 0.500 | 0.500 to 0.500 |
| Use the most recent cue-specific outcome | Full | 1.000 | 1.000 to 1.000 |
| Use the most recent cue-specific outcome | Matched sham | 0.500 | 0.500 to 0.500 |

The blanket-reversal strategy scored 0.00 on stable items, 1.00 on reversed items, and
0.50 on fresh reassigned items. This confirms that transition mixing prevents a global
reversal rule from clearing the progression threshold. The cue-recency result is an
intended associative positive control: current cue-specific evidence is sufficient,
while the exact sham supplies no discriminative cue evidence.

## Interpretation boundary

The scripted adapter is a deterministic implementation baseline, not an AI subject.
This validation shows that the schedule, controls, metrics, logging, and positive
control behave as designed. It does not show how Claude or another model will perform.

Any later model result would remain a behavioural and computational indicator only.
Neither this validation nor a future positive result could establish feeling,
awareness, sentience, suffering, or phenomenal consciousness.

## Next decision

Do not launch a paid run yet. The next step is an independent methods review of the new
schedule and analysis. A paid diagnostic requires a separate authorisation, fresh
seeds, a frozen provider budget, and a clean committed revision.
