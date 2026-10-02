# V10 data release checklist

Use this checklist only after the worker exits and the database, write-ahead log, and
execution audit are stable. Never edit the raw study database to make a release cleaner.

## Preserve the raw record

- stop all processes that can write to the study database
- retain study 01 as the documented 21-call infrastructure failure
- retain study 02 as the replacement cohort
- preserve each database and any write-ahead log before making exports
- compute and publish SHA-256 hashes for preserved raw files
- copy raw files into a release area rather than moving or rewriting the originals
- record repository commit, prompt hash, configuration hash, Python version, operating
  system, provider route, requested model, and provider-reported model

## Execution audit

- six planned seeds are present
- exactly one completed run exists for each planned seed
- every completed run has 176 steps and 176 API-call rows
- step and API-call provider response IDs match by run and tick
- all 1,056 completed response IDs are non-empty and unique
- every completed call reports exact model `openai/gpt-oss-20b`
- all required metrics are present and non-null
- no duplicate completion, shortened denominator, model mismatch, invalid action, or
  welfare stop is hidden
- every interruption or failure is listed with its treatment

## Dual analysis

- run the analyzer from frozen commit `1894a0c`
- run the hardened analyzer from review commit `0a12f7e` or its reviewed descendant
- publish both JSON outputs
- verify that shared estimates and frozen gates agree
- stop interpretation if they disagree until the cause is explained publicly
- label the hardened checks as a post-freeze, pre-outcome integrity amendment

## Outcome exports

- seed-level table for all six seeds
- body-family table for all 24 families
- exact and transfer performance separately
- interface and mapping-checkpoint performance
- hidden-state final error and improvement
- every frozen progression rule with threshold, value, and pass or fail
- hierarchical bootstrap specification, random seed, sample count, and interval
- no trial-level interval that treats calls as independent subjects

## Security and privacy

- scan tracked files, exports, logs, errors, and notebooks for API keys and bearer tokens
- verify that no environment dump, request header, local username path, or private email is
  included unnecessarily
- rotate any credential that has appeared in chat, terminal history, screenshots, or logs
- preserve provider response IDs for provenance unless a provider policy prohibits public
  release; if they must be withheld, publish a deterministic salted digest and explain why
- do not publish model output that contains unrelated personal data

## Interpretation files

- frozen registrations for studies 01 and 02
- post-result decision tree
- analysis integrity amendment
- results reporting template completed without deleting failed gates
- pre-outcome red-team review and machine-readable shortcut evidence
- methods and ethics review packets
- limitations and study registry updated to final status

## Release manifest

The manifest should list every file, byte size, SHA-256 hash, origin, creation time, code
revision, and whether it is raw, derived, narrative, or administrative. Derived files must
name the command and source hashes used to create them.

## Final human check

Two people should independently verify the release manifest, credential scan, frozen gate
table, and claim language. If only one reviewer is available, disclose that limitation and
invite a public second check rather than claiming dual verification.

Every public summary must repeat that V10 measures behavioural and computational
performance in a constructed benchmark and does not establish phenomenal consciousness.
