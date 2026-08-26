# Project Theta publication plan

## Recommended public structure

Project Theta should have one public source repository and one plain-language website.
The repository is the scientific record. The website is the readable front door. They
should link to the same versioned protocols, code, data summaries, limitations, and
citations.

## GitHub repository

Publish the current repository only after a secret scan, license check, database
privacy review, and removal of local or provider-specific artifacts. Keep these areas
public:

- source code and tests;
- protocol and preregistration files;
- literature review, evidence table, search log, and bibliography;
- fixed configuration files and deterministic seeds;
- analysis code and derived result tables;
- welfare rules, limitations, roadmap, and contribution guide.

Do not publish API keys, local environment folders, raw provider credentials, billing
records, or any database field that could contain a secret. Raw model transcripts
should receive a separate privacy and licensing review before release.

Suggested repository sections:

```text
README
docs
preregistration
research
references
results
src
tests
```

## Website

The first website does not need live experiments. A static site is safer and easier to
audit. It should contain:

1. What Project Theta is and is not.
2. The distinction between behavioural, computational, and phenomenal claims.
3. An interactive diagram of the world, body, agent loop, and experimental controls.
4. A results page with condition-level charts, confidence intervals, sample sizes, and
   validity warnings.
5. The full roadmap and current deployment gate.
6. A research page with the literature review, evidence map, protocol, and BibTeX.
7. An ethics page with stop rules and an incident log.
8. A reproducibility page with exact commits, seeds, model IDs, prompts, and database
   schema versions.

Every results chart should carry this sentence:

> These measurements concern behaviour and implemented computation. They do not
> establish phenomenal consciousness.

## Domain

`projecttheta.org` is a good descriptive choice if it is still available and does not
conflict with an existing organization or mark. Domain availability can change at any
time, so it should be checked again immediately before purchase. Buying a domain is
separate from deploying the lab and does not require running a continuous agent.

## Release sequence

1. Finish internal scientific and secret audits.
2. Tag a read-only release candidate.
3. Ask an independent consciousness researcher and research ethicist to review it.
4. Publish the repository with the pilot and replication clearly labelled.
5. Publish the static website from the tagged release.
6. Collect issues and external replication proposals.
7. Consider a bounded server deployment only after the deployment gate passes.

## Public language

Use specific claims such as "the full condition scored 1.0 accuracy across six matched
seeds." Avoid phrases such as "Claude felt theta," "the model became self-aware," or
"we detected consciousness." A human tone comes from clear ownership of uncertainty,
not from removing scientific caveats.
