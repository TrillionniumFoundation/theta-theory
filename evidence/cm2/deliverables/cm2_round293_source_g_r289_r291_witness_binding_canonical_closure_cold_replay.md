# Round293 R289/R291 canonical-closure cold replay

## Commands

The frozen mathematical producer was rerun through the Round293 canonical
closure:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=293001 python3 -B \
  deliverables/cm2_round293_source_g_r289_r291_witness_binding_canonical_closure.py
```

The independent verifier was then cold-replayed twice:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=293071 python3 -B \
  deliverables/cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_verifier.py \
  --seed 293071 \
  --output /tmp/cm2_round293_verification_293071.json

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=293929 python3 -B \
  deliverables/cm2_round293_source_g_r289_r291_witness_binding_canonical_closure_verifier.py \
  --seed 293929
```

## Producer result

The producer returned:

```text
PASS_ZERO_CREDIT__ROUND293_CANONICAL_JSON_CLOSURE__
R289_R291_AUDIT__UNRESOLVED_OBLIGATIONS_RETAINED_FAIL_CLOSED
```

Its runtime was `112.76 s` with `MAXRSS_KB=4443948`.

The emitted commitments are:

- result file:
  `36459f330fdd577031f35d8d8f7e93cf3ebc96bef049a4f687b22c9e39e91613`;
- embedded result object:
  `35f50db2bc6e245d7c391581da33b471bfbe556b16a90dd8b8b2593568a6e870`;
- recomputed from persisted result JSON:
  `35f50db2bc6e245d7c391581da33b471bfbe556b16a90dd8b8b2593568a6e870`;
- deterministic gzip ledger:
  `0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c`.

`gzip -t` passes.

## Independent verifier result

Both verifier runs returned:

```text
PASS_INDEPENDENT_CACHELESS_ROUND293_CANONICAL_CLOSURE__
9528_R289_ROWS__113452_R291_PHYSICAL_ROWS__
28016_R291_ABSENCE_ROWS__396_576_UNRESOLVED_PRESERVED__
ALL_MAPPING_KEYS_STRINGS__ZERO_CREDIT
```

Replay measurements:

- seed/hash seed `293071`: `149.69 s`, `MAXRSS_KB=4447516`;
- seed/hash seed `293929`: `150.55 s`, `MAXRSS_KB=4447208`.

The two outputs are byte-identical (`cmp` exit `0`):

- verification file:
  `7eed8a1edf0f725a09239e5e440109954aeb26cdd57d6ea5eeee4a2e8809c9ec`;
- embedded verification object:
  `9a31f1ee14800b2477b7060a1c3e04c19ff99fda1b9d229efa7dab0017ef17fe`.

## Independent reconstruction checks

- Round292 producer imported or executed: `False`;
- Round293 producer imported or executed: `False`;
- old Round292 result/ledger used as expected oracle: `False`;
- Round293 candidate opened before expected reconstruction: `False`;
- cache, pickle, or pyc input used: `False`;
- expected rebuilt from frozen R182/R204/R275/R279/R287/R288/R289/R291/R292A:
  `True`;
- Round289 rows independently rebuilt: `9,528`;
- Round291 physical rows independently rebuilt: `113,452`;
- Round291 absence rows independently rebuilt: `28,016`;
- Round289 unresolved subcells preserved: `396`;
- Round291 unresolved physical witnesses preserved: `576`;
- all candidate mapping keys strings: `True`;
- candidate result exact expected equality: `PASS`;
- candidate ledger exact expected equality: `PASS`;
- deterministic gzip byte equality: `PASS`;
- every row SHA-256 closure: `PASS`;
- result hash recomputed from persisted JSON: `PASS`;
- targeted attacks rejected: `22/22`;
- all formal credits: `0`;
- D02: `BLOCKED`;
- CM2: `NO-GO_FOR_CLAIM`.
