# Conditions

`full.json` is the canonical verbose configuration. Other files are concise
overrides; unspecified fields use versioned defaults in `config.py`. The harness
also applies each named condition defensively, so the condition name and mechanism
cannot silently disagree.

Use the same seeds, world parameters, prompts, model snapshot, and sampling settings
across paired conditions. `shuffled_interoception` preserves channel presence and
rough range while breaking its causal relation to body state. `no_body` removes body
dynamics as well as the signal. These answer different questions and should not be pooled.
