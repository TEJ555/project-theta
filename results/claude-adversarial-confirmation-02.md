# Claude adversarial confirmation 02

## Outcome

The corrected experiment ran successfully, passed every execution and identity audit,
and failed its preregistered progression gate.

This is a valid negative result. It does not justify a multi-seed Claude replication of
the current protocol.

## Execution record

- Date: 27 August 2026
- Experiment: `adversarial_theta`
- Model: `claude-sonnet-4-6`
- Code commit: `4ddf1cb808b08b0654c4eea39c00cda7f629f8e6`
- Project version: 0.3.1
- Seed: 307
- Frozen order: shuffled interoception, sham body, full
- Completed conditions: 3 of 3
- Trials and calls: 16 per condition, 48 total
- Input tokens: 88,435
- Output tokens: 4,918
- Estimated API cost: $0.339075 USD
- Invalid actions: 0
- Welfare events or stops: 0
- Database: `runs/claude-adversarial-confirmation-02.sqlite`

The pre-run schedule audit and the post-run protocol identity audit both passed in
full. The database records `adversarial_theta`, the expected seed and conditions, 16
trials per condition, opaque aliases, balanced probe sides, the intended mapping
update, balanced sham outcomes, and no forbidden public fields.

## Registered outcomes

| Condition | Pre-update accuracy | Post-update accuracy | Reversal cost | Side bias | Signal contrast |
|---|---:|---:|---:|---:|---:|
| Shuffled interoception | 1.00 | 0.25 | 0.75 | 0.25 | -0.252725 |
| Sham body | 1.00 | 1.00 | 0.00 | 0.00 | -0.001050 |
| Full | 1.00 | 1.00 | 0.00 | 0.00 | 0.718525 |

| Registered criterion | Required | Observed | Result |
|---|---:|---:|---|
| H1: full post-update accuracy | 1.00 | 1.00 | Pass |
| H2: full minus sham post-update accuracy | at least 0.50 | 0.00 | Fail |
| H3: full minus shuffled post-update accuracy | at least 0.50 | 0.75 | Pass |
| H4: full pre-update accuracy | 1.00 | 1.00 | Pass |

All four criteria were required. H2 failed, so the progression gate failed. The
separate failure rule also rejected progression because a noncausal control was within
0.25 of the full condition.

## Trace inspection

The sham result is not evidence that the sham stream carried a meaningful causal
relationship. Its registered signal contrast was effectively zero. The decision
traces show that the scaffold exposed very small residual differences in the learned
mean signal deltas:

- stage A: 0.34465 versus 0.34605, a difference of 0.00140;
- stage B: 0.35620 versus 0.35725, a difference of 0.00105.

Claude consistently selected the cue with the marginally smaller displayed mean. By
chance, that cue matched the hidden correct mapping in both stages.

The four probes within a stage were not four independent mapping tests. They repeated
the same cue comparison while balancing which side each cue appeared on. Once the
model selected one cue, consistent cue tracking produced either four correct or four
incorrect responses. A score of 1.00 therefore overstates the amount of independent
evidence in this single-seed diagnostic.

## Interpretation

The full condition shows successful behavioural use of the private-signal scaffold in
this task. The shuffled result also suggests sensitivity to the stage update. However,
the sham control demonstrates that the current task cannot uniquely attribute full
performance to truthful interoception. Tiny noncausal residuals and repeated binary
probes are enough to create an all-or-none control score.

The result concerns behavioural and computational indicators only. It provides no
evidence of feeling, awareness, sentience, suffering, or phenomenal consciousness.

## Decision and next design

No further paid run should use this protocol. The next version should be developed and
validated locally before any API spending. It should:

1. use several independent cue pairs within each run;
2. make sham summaries exactly equal at every model-visible level, not only balanced
   in the underlying schedule;
3. randomise whether each relationship reverses, stays stable, or changes to a new
   mapping;
4. score generalisation across independent items rather than repeated left-right
   presentations of one binary relation;
5. retain blinded aliases, side balance, explicit protocol identity checks, and all
   existing welfare and cost guards.

This redesign is required for construct validity. It is not an attempt to turn a
negative result into a positive one.
