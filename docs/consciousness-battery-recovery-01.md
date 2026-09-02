# Consciousness indicator battery recovery record 01

Date: 2 September 2026

## Scope

This record documents an infrastructure interruption during the first frozen consciousness indicator battery. It is not a change to the scientific hypotheses, trial schedules, prompts, model, conditions, scoring, or stopping rules.

The frozen battery contains 50 planned completed runs:

- 20 adversarial interoception and metacognition runs
- 15 self versus other attribution runs
- 15 temporal self persistence runs

## What happened

The initial process stopped after 40 completed runs. Recovery preserved the database, marked the unfinished row as failed, skipped every completed job, and completed one further temporal self run.

During the next job, Windows reported that a temporary `theta-subject-` directory was still in use while Python was cleaning it up. The Claude Code child process had already exited, but the cleanup exception was treated as an adapter failure. That left 41 of the 50 planned runs completed.

## Infrastructure correction

The subscription adapter now ignores errors that occur only while deleting its isolated temporary directory. This prevents a valid child process result from being discarded because Windows briefly retains a file handle.

The fixed worker also recognises this exact recorded Windows cleanup failure as retryable. It does not make other model, provider, parsing, welfare, or experimental failures retryable.

## Scientific safeguards

- The failed partial attempts remain in SQLite and are not deleted or counted as completed results.
- Every completed job is skipped during recovery, preventing duplicate completed observations.
- The affected job is allowed no more than the preregistered two attempts.
- The remaining completed runs record the new code revision.
- Analysis includes completed runs only.
- The change does not modify information visible to the model or the expected answers.

The repository history and this record disclose the code revision boundary. Any publication of this battery should cite the original frozen revision and the later infrastructure-only recovery revision.

## Interpretation

This recovery does not improve or weaken any score. It only lets the frozen schedule continue after an operating system cleanup fault. Results remain behavioural and computational indicators. They are not evidence that the model has phenomenal consciousness.
