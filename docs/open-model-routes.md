# Open model routes

Status: development infrastructure

## Purpose

Project Theta should not depend on one Claude Code routed system. Cross-model work is
scientifically useful because a result that appears only in one provider stack may be
a model-specific strategy, a routing artefact, or a provider implementation detail.

The preferred sequence is:

1. validate every schedule and baseline without a model;
2. run a bounded development block on NVIDIA's hosted NIM endpoint;
3. repeat the frozen protocol on at least one other exact model family;
4. run the strongest design locally from preserved open weights;
5. reserve larger confirmatory samples for designs that survive shortcut attacks.

## Route A: NVIDIA hosted NIM

Project Theta uses the OpenAI-compatible endpoint at
`https://integrate.api.nvidia.com/v1/chat/completions`. The default development model
is `nvidia/nemotron-3.5-lightning-30b-a3b`.

Advantages:

- it is not Claude Code routed;
- the requested model ID is explicit;
- NVIDIA currently provides hosted endpoints for development and prototyping;
- a 30B mixture-of-experts model is practical without owning a large GPU;
- the adapter requests schema-guided JSON and logs returned model identity, tokens,
  latency, seed, temperature and response ID.

Limits:

- the service is hosted, so backend software and weights may change;
- NVIDIA does not return a dollar charge with each response;
- free development access is a service policy, not a permanent research guarantee;
- the viral claim that every account receives one free year is not part of the
  official documentation reviewed on 10 September 2026;
- a returned model ID is useful provenance, but it is not a cryptographic weight
  digest.

Create a key from NVIDIA's model catalogue, install the `nvidia` optional dependency,
then run:

```powershell
python -m pip install -e ".[nvidia]"
.\scripts\run_nvidia_nim_v6_pilot.ps1
```

The launcher never writes the key to disk. The first pilot is one seed across five
conditions, with 18 model decisions per run and 90 maximum hosted requests in total.
It is development evidence, not a confirmatory study.

## Route B: local Ollama

The current laptop can use a compact quantized model through Ollama. `qwen3:8b` is a
reasonable first local subject. The published Ollama package is about 5.2 GB, so some
CPU offload may occur on a laptop GPU and the run can be slow.

Advantages:

- no provider API charge;
- no model routing;
- the weights can be retained;
- the exact model digest is collected automatically and the runtime can be archived;
- later work can add activation-level and component-level interventions.

Limits:

- a compact local model may fail the task for capability reasons;
- slow inference makes large development sweeps inefficient;
- a weak-model null result says little about the hypothesis;
- local runs still need fixed prompts, seeds, decoding settings and software versions.

After installing Ollama, pull the model and run a one-seed development block:

```powershell
ollama pull qwen3:8b
.\scripts\run_ollama_v6_pilot.ps1
```

## Interpretation

Passing V6 would show that a model can use intervention evidence to author and later
use a compact persistent causal state under controlled ablations. It would be a
behavioural and computational result. It would not establish feelings, sentience, or
phenomenal consciousness.

The result becomes more compelling if it survives fresh aliases, active
interventions, model-family replication, exact-weight local reproduction, simple
baseline attacks, and a preregistered seed-level analysis.

## Sources

- NVIDIA LLM API reference: https://docs.api.nvidia.com/nim/reference/llm-apis
- NVIDIA structured generation: https://docs.nvidia.com/nim/large-language-models/latest/structured-generation.html
- Ollama structured outputs: https://docs.ollama.com/capabilities/structured-outputs
- Ollama Qwen3 8B package: https://ollama.com/library/qwen3:8b
