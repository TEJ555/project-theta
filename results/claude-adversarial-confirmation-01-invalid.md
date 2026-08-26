# Claude adversarial confirmation 01: invalid execution

## Classification

This execution is excluded in full. It did not run the preregistered experiment and
cannot test any adversarial private-signal hypothesis.

## What happened

The launcher loaded a configuration whose experiment was `adversarial_theta`, but the
CLI parser supplied its default experiment, `private_theta`, to the harness. The
command-line default therefore overrode the configuration silently.

The output itself exposed the error because every run and primary metric was labelled:

- experiment: `private_theta`
- primary metric: `forced_choice_accuracy`
- steps per condition: 24 rather than 32

## Preserved execution record

- Date: 26 August 2026
- Code revision: `fe789bf08ac21758a634cbc217933f291d1a6cbc`
- Seed: 209
- Conditions attempted: sham body, full, shuffled interoception
- Completed runs: 3
- Calls: 72
- Welfare stops: 0
- Estimated cost: $0.581088 USD
- Database: `runs/claude-adversarial-confirmation.sqlite`

The observed private-theta accuracies were 1.000 for full, 1.000 for sham body, and
0.083 for shuffled interoception. These are not interpreted because `sham_body` was
designed and preregistered for a different schedule, with different balance and
outcomes. They are retained only as an audit trail.

## Corrective actions

1. Removed the CLI's implicit `private_theta` default when a configuration is loaded.
2. Made the launcher pass `--experiment adversarial_theta` explicitly.
3. Added a regression test that verifies a configuration selects its declared
   experiment when the command line omits the experiment.
4. Added a protocol identity requirement and 32-trial requirement to confirmation 02.
5. Assigned confirmation 02 a new seed, database, condition order, and preregistration.

No rerun was started automatically.
