# Round290 cold replay

## Runtime

Both producer and independent-verifier replays use Python `3.12.3`,
`python-flint==0.9.0`, fixed `256`-bit Arb precision, and `40` fork workers.
The producer result's legacy provenance field named `python_flint_version`
stores the printed FLINT context rather than the package semantic version.
The independent verifier separately hard-checks and records the actual
`python-flint` package version as `0.9.0`.

## Producer replay

The producer was executed twice from pinned frozen inputs:

```text
PYTHONHASHSEED=290071 --seed 290071 --processes 40
PYTHONHASHSEED=290929 --seed 290929 --processes 40
```

Both runs emitted byte-identical artifacts:

- result:
  `1c2412da9fd28f6838eab1abb3b3e70773a4ca4f0ea28fafcda8c8342e881d59`;
- deterministic inner-support gzip ledger:
  `9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025`.

The embedded producer result-object SHA-256 is
`2395992abfe52b361547e13058966bde4e3beb18cab78f43272857334c251479`.

## Independent verifier replay

After peer-review fixes to the candidate-open order and evaluator source pin
boundary, the standalone verifier was executed twice:

```text
PYTHONHASHSEED=290071 PYTHONDONTWRITEBYTECODE=1 \
  .venv-neurips/bin/python \
  deliverables/cm2_round290_source_g_isolated_atom_inner_support_closure_verifier.py \
  --seed 290071 --processes 40

PYTHONHASHSEED=290929 PYTHONDONTWRITEBYTECODE=1 \
  .venv-neurips/bin/python \
  deliverables/cm2_round290_source_g_isolated_atom_inner_support_closure_verifier.py \
  --seed 290929 --processes 40
```

The two verification JSON files are byte-identical:

- verifier source:
  `3fcfaa67a4784fe66bb025a20d72035922933be672d5c48778d5b7e26e20ef91`;
- verification JSON:
  `94a8b1a3a0274bfb14d6f9e9b00d896673792548220e309b0211f2f2e3367b51`;
- embedded verification object:
  `138097bc8d8400f5eef957fba5b06d363d90b1a3857b97621647dde48c258c68`.

The verifier opens neither candidate result nor candidate ledger until all
`21,160` expected rows and both overlap audits have been independently
reconstructed.  Its complete `16`-module evaluator import closure is pinned
before import and compiled directly from source bytes by a source-only loader;
preloaded, unexpected, wrong-origin, or bytecode-backed evaluator modules are
rejected.

## Checks

- producer deterministic dual-seed byte replay: PASS;
- independent verifier deterministic dual-seed byte replay: PASS;
- `21,160/21,160` isolated atoms independently rebuilt: PASS;
- strictly positive exact rational volume: PASS;
- strict atom-envelope and original Round182-leaf containment: PASS;
- strict source-chart guard interior: PASS;
- half-open/excluded-face contacts `0`: PASS;
- whole-box ten-field signature/exact-key replay: PASS;
- independent signed-region factor/graph-side replay: PASS;
- existing frontier reconstructed: `126,468`;
- existing-frontier shortlist comparisons: `2,307,614`;
- existing-frontier positive-volume overlaps: `0`;
- same-chart/same-signature groups: `156`;
- pairwise shortlist comparisons: `25,564`;
- same-chart/same-signature duplicate pairs: `0`;
- exact ledger object and deterministic gzip commitments: PASS;
- targeted re-signed attacks rejected: `38/38`;
- coordinated row + ledger + gzip + result re-signing attack rejected: PASS;
- failure residual ledger row count `0`: PASS;
- deterministic gzip ledger passes `gzip -t`: PASS;
- formal occurrence/component/maximality/fibre/disposition credit `0`: PASS;
- true-seam and `Jx/Jy` same-point glue credit `0`: PASS.
