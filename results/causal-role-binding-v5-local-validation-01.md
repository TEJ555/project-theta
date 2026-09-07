# Causal role binding v5 local validation 01

Completed: 7 September 2026

Status: all frozen engineering gates passed. No Claude, network or paid-provider calls
were made.

## Design

- 100 deterministic seeds, 8000 through 8099.
- Three conditions and 300 completed runs.
- Six independent role families per run.
- Forty-eight matched acquisition events.
- Six exact-route calibration probes.
- Six novel-route transfer probes.
- Twelve scripted decision calls and 48 skipped acquisition calls per run.

Every condition received the same raw event stream, memory allowance, public tasks and
inference budget. Contexts matched after replacing only the values produced by the causal
state register.

## Results

| Condition | Runs | Exact-route accuracy | Novel-transfer accuracy |
|---|---:|---:|---:|
| Role-bound | 100 | 1.000 | 1.000 |
| Unbound | 100 | 1.000 | 0.500 |
| State reset | 100 | 0.500 | 0.500 |

The role-bound minus unbound transfer difference was +0.500 for every seed. The role-bound
minus reset difference was also +0.500 for every seed. These deterministic effects validate
the implementation and do not estimate a model effect.

The schedule audit passed all 100 seeds. The strongest declared metadata-only strategy scored
0.508 across 2,400 diagnostic probes.

## What this establishes

The task distinguishes exact route retrieval from role-based transfer in the scripted
mechanisms. The unbound control can answer every calibration item while remaining at the
balanced baseline on novel routes. Resetting the state removes both abilities.

## What this does not establish

The role-bound mechanism is code supplied by the experimenter. Its scripted success is not
evidence that a language model learned a self, formed an experience or became conscious. A
future model-backed development study could test whether the supplied causal register changes
behaviour, but only after independent review of construct validity and remaining shortcuts.
