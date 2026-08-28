# Round293-B supplemental dual-producer replay attestation

## Outcome

The superseding Round293 canonical closure has now been replayed under a
second producer hash seed.  The result JSON and deterministic GZIP ledger are
byte-identical to the artifacts produced by the recorded first run.

- producer alpha seed: `293001`;
- producer beta seed: `293997`;
- result file SHA-256, both runs:
  `36459f330fdd577031f35d8d8f7e93cf3ebc96bef049a4f687b22c9e39e91613`;
- ledger file SHA-256, both runs:
  `0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c`;
- result `cmp`: exit `0`;
- ledger `cmp`: exit `0`;
- beta runtime: `113.56 s`;
- beta maximum resident set: `4,444,932 KiB`.

The exact beta command contract was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=293997 python3 -B \
  cm2_round293_source_g_r289_r291_witness_binding_canonical_closure.py
```

The existing independent verifier record remains unchanged: seeds `293071`
and `293929` produced byte-identical verification files, reconstructed the
complete `9,528 / 113,452 / 28,016` row frontier without importing or
executing the producer, and rejected all `22/22` targeted attacks.

## Admission boundary

The original Round292-B result remains a nonadmissible defect witness.  It was
not modified in place.  Round293 remains the only admissible superseding
canonical closure, and Round293-B adds only the missing second-producer-seed
replay evidence.

The supplemental attestation also pins the sealed Round292-A verifier and
manifest, plus the original Round293 manifest.  It grants no mathematical
credit: maximality, fibre, global disposition, D02, and CM2 states do not
move.
