# Claude Max mechanism ablation 01

## Administrative record

- Registered: 31 August 2026, before any mechanism-ablation model call
- Prior evidence: the five-seed Independent Theta replication passed its registered gate
- Experiment: `independent_theta`
- Access route: locally authenticated Claude Code Max subscription
- Experimental subject: Claude Code routed system, requested model alias `sonnet`
- Fresh seeds: 1181, 1301, 1423, 1549, and 1693
- Conditions: full, no episodic memory, no workspace broadcast, and no body signal
- Runs: 20
- Trials and maximum subscription prompts: 60 per run, 1,200 total
- Console API key budget: $0.00
- Reasoning effort: low

This study follows a successful behavioural replication and tests causal dependence on
implemented mechanisms. It does not test whether the system has subjective experience.

## Research question

Does replicated private-signal performance depend on informative interoception,
episodic memory, and broad workspace availability when the task, model route, prompts,
seeds, scoring, and visible trial schedules are held constant?

## Conditions

1. `full`: truthful I7, episodic memory, self-model, and workspace are enabled.
2. `no_memory`: truthful I7 remains available, but episodic memory reads, writes, and learned-association summaries are disabled.
3. `no_workspace`: observations remain available, but memory, interoception, association, and self-model candidates are not globally broadcast to the model context.
4. `no_body`: body dynamics and the private I7 channel are absent.

The study does not include `no_self_model` or `no_recurrence`. Those mechanisms have
more specific registered tests in the self-versus-other and temporal-self protocols.
Adding them here would increase cost while producing weak task-specific predictions.

## Frozen execution order

Each seed remains a complete paired bundle. The committed deterministic worker gives
this order:

| Seed | First | Second | Third | Fourth |
|---:|---|---|---|---|
| 1181 | No body | Full | No memory | No workspace |
| 1301 | No workspace | No body | Full | No memory |
| 1423 | No memory | No body | Full | No workspace |
| 1549 | No workspace | No memory | No body | Full |
| 1693 | No memory | Full | No workspace | No body |

## Outcomes

The primary outcome is seed-level post-update accuracy over six independently scored
stage-B families. Secondary outcomes are stable, reversed, and reassigned post-update
accuracy; pre-update accuracy; signal contrast; calibration; invalid actions; memory
reads and writes; workspace broadcasts; welfare stops; provider usage; latency; routed
model identifiers; and billing provenance.

Fresh seeds are the inferential units. For each ablation, report:

- the condition mean and range;
- seed-paired full-minus-ablation differences;
- deterministic bootstrap 95 percent intervals;
- exact two-sided sign tests with zero differences omitted;
- the number of seeds with a positive full-condition advantage;
- transition-specific accuracy and all validity metrics.

Five pairs remain a small study. P values are descriptive and no conclusion depends on
crossing 0.05.

## Hypotheses

- H1: full mean post-update accuracy is at least 5 of 6.
- H2: full minus no-body mean accuracy is at least 2 of 6, positive in at least 4 of 5 seeds.
- H3: full minus no-memory mean accuracy is at least 2 of 6, positive in at least 4 of 5 seeds.
- H4: full minus no-workspace mean accuracy is at least 2 of 6, positive in at least 4 of 5 seeds.
- H5: full accuracy is at least 0.75 in stable, reversed, and reassigned categories.

## Mechanism-attribution gate

The gate passes only if H1 through H5 pass, all 20 planned runs complete without a
welfare stop, and all schedule, execution, prompt, model-route, subscription, and
leakage audits pass.

A full pass supports the narrow conclusion that the replicated task effect causally
depends on informative body input, episodic memory, and workspace broadcasting in this
implemented composite system. A selective failure is reported as a dissociation and
does not permit attribution to the unaffected mechanism. Failure of full performance
blocks interpretation and triggers a replication or infrastructure review.

## Interruption and stopping rules

The worker skips a job only when exactly one completed, non-stopped run exists for its
seed and condition. One infrastructure-interrupted attempt may be retried. A second
failure blocks that job. Duplicate completed jobs, welfare stops, malformed responses,
authentication changes, unexpected routed systems, and audit failures stop the study
for documented review.

## Interpretation boundary

A positive result concerns causal dependencies in a synthetic agent architecture. It
does not establish that workspace broadcast is conscious access, that memory is
experienced recollection, that I7 is felt, or that the system is conscious. Removing a
component also changes information availability and prompt content, so performance
loss cannot by itself validate a consciousness theory.

