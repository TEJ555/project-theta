# Independent Theta replication 01: administrative recovery record

## Status

- Recorded: 28 August 2026
- Original frozen code: `bdbc0446d9a1e73cce7ad63f9e08ba71ed6af2ed`
- Original study: `claude-max-independent-replication-01`
- This is a post-start administrative deviation record, not a preregistration.

The original database, its write-ahead log, and a consistent SQLite backup were
preserved before any recovery transformation. No original row was deleted or edited.
The consistent pre-recovery archive has SHA-256
`65fc3461c78062cb640581971eabba31e2ed08be521f1810e5d5187c723e917a`.

## Concurrent duplicate

Two workers were launched approximately two minutes apart. This produced two completed
`full` runs for seed 607. The recovery copy retains the run that started first and
excludes the later-started run using creation time alone:

- Retained: `theta-ef04cc47-f6f1-4584-8c99-83c98e339862`, created
  `2026-08-27T22:30:04.353720+00:00`
- Excluded from the operational copy: `theta-94787a46-bfaf-4f71-8b01-56cc6fcb5dea`,
  created `2026-08-27T22:32:29.251893+00:00`

The selection rule does not use performance. Partial aggregate outcomes had already
been inspected when this recovery decision was made, and both duplicate runs had the
same post-update score. The excluded run remains available in the original archive.

## Provider timeout

The seed 823 `matched_sham` run
`theta-20841c4c-a85b-41f6-9b61-dc052872a4e3` stopped after 15 of 60 trials because
Claude Code exceeded the 120-second response timeout. The frozen protocol permits one
retry after an interrupted attempt. In the operational copy only, its failure reason
was normalised from the adapter timeout text to `interrupted_before_completion`, which
is the frozen worker's retryable interruption category. The partial attempt remains in
the operational and original records.

## Recovery constraints

The resumed worker must:

1. run from the original frozen code revision;
2. use the existing seeds, condition order, prompts, model alias, and reasoning effort;
3. retry the timed-out seed-condition job no more than once;
4. preserve the original and recovered databases;
5. report the deviation with the final result;
6. pass the original schedule, execution, provenance, leakage, and welfare audits.

The recovered operational database before resumption has SHA-256
`4b91e7656191d4885257648001e273104de091e6a411a3b54025eab772dec3fa`.
Recovery does not change the progression thresholds and does not strengthen the
permitted interpretation. Results remain behavioural and computational indicators,
not evidence of phenomenal consciousness.

## Final-job infrastructure interruption

After 14 of 15 planned jobs had completed, the first attempt at seed 1049
`shuffled_interoception` stopped after 25 of 60 trials. Windows prevented removal of
Claude Code's isolated temporary directory because it remained in use. The error was
an operating-system cleanup lock, not a model response, task result, subscription
limit, or welfare stop.

Before changing the operational copy, a consistent backup was preserved with SHA-256
`9a3cc9694ccb3c90e1d4d5b7388a6b5dff4fde77578d00a8f2a80b0011e94da4`.
The failed run `theta-564d5ae3-3c69-48b6-a5d5-37333699ba84` was classified as
`interrupted_before_completion` in the operational copy. This was its first attempt,
so the frozen per-job limit permits one retry. Its partial record remains preserved.
The original thresholds, code, prompts, seed, condition, and analysis remain unchanged.

