# Self-model binding v4 development pilot 01

Status: frozen for local validation only. Target-model execution has not started.

## Research question

When model-visible ownership information, context structure and inference budget are matched, does a specialised self-model produce different choices from a generic table containing the same associations?

This is a protocol-development study. It cannot provide confirmatory evidence and it cannot support claims about phenomenal consciousness.

## Why v4 exists

The v3 protocol contained a deterministic answer-position shortcut and compared conditions with unequal access to task-relevant information. V4 is a new experiment with new seeds, new condition names and a new database. V3 data will not be pooled with v4.

## Frozen development design

- Seeds: `6029`, `6131`, `6247`
- Conditions: `full`, `generic_table`, `misattributed_table`, `permuted_table`
- Twelve independent opaque cue families per run
- Forty-eight acquisition updates and twelve one-shot probes per run
- Primary outcome: `source_binding_accuracy`
- Model inference only on probes
- Maximum model calls: 12 per run, 144 for the complete pilot
- All acquisition actions are protocol-defined `observe` actions
- Welfare monitoring remains active on every acquisition and probe

The full and generic-table conditions must have byte-identical model-visible probe contexts. The wrong-content controls must preserve the binding-register schema and entry count while changing only association correctness.

## Development gates

- Schedule audit passes on all three execution seeds.
- The large local shortcut audit gives every declared metadata-only strategy accuracy no greater than 0.60.
- Full and generic conditions have byte-identical probe contexts in deterministic validation.
- Full and generic scripted lookup accuracy is 1.00.
- Misattributed lookup accuracy is 0.00.
- Permuted lookup accuracy is below 1.00.
- Probe-only and all-trial scripted runs produce identical probe accuracy.
- Probe-only execution records exactly 12 model calls and 48 skipped inference events.
- No target-model result is described as an isolated Sonnet result. Claude Max execution is a Claude Code routed-system pilot.

## Interpretation

The decisive comparison is full versus generic table. Equality would show that the v3 separation was explained by information access rather than a specialised self-model. A difference would still require an independently reviewed explanation of how two byte-identical model inputs generated different outcomes.

The misattributed and permuted conditions test dependence on correct association content. They are not architecture ablations.

## Confirmation boundary

No confirmatory sample size, exclusion rule or model family is selected here. Those decisions must be frozen only after this development pilot, external methods criticism and a power analysis. Confirmation should use exact versioned models through a direct provider or reproducible open-weight runtime.
