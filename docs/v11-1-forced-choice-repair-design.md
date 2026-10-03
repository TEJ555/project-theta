# V11.1 forced-choice and provenance repair

V11.1 addresses one identified measurement failure in V11. It does not reinterpret or
replace V11.

## Failure being repaired

One V11 response abstained from a two-option forced choice. The harness recorded a
deterministic fallback in the step decision and retained the invalid-action count only in
the final metric. This made the metric impossible to reconstruct exactly from raw trial
rows and caused the frozen execution and validity gates to fail.

## Protocol changes

1. The model instruction states that every controlled item is forced choice and that it
   must select the better permitted option even if neither seems ideal.
2. The raw model action and invalid-action flag are stored in the hidden trial record.
3. Invalid actions receive an incorrect score. A fallback remains only to keep the
   deterministic simulation state well-defined and can never earn a correct response.
4. The analyzer reconstructs invalid-action counts from the preserved raw flag.
5. The cohort uses six fresh seeds and is analyzed independently of V11.

## Falsifiable prediction

The repaired protocol will preserve the V11 mechanism pattern while meeting a strict
forced-choice compliance bound of no more than six invalid actions across 6,336 calls and
no more than one invalid action in any run. All original V11 scientific thresholds remain
unchanged.

The compliance bound was defined after observing the V11 failure and is therefore a
protocol-development choice, not a retroactive V11 criterion. It is tested only on fresh
V11.1 data.

