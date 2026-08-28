# Round302-C cold replay

Run from the workspace root. The commands disable bytecode cache writes and
use explicit, distinct Python hash seeds.

## Producer replay A

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=302311 \
  python3 -B \
  deliverables/cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure.py \
  --seed 302311
```

Expected semantic commitments:

```text
ledger_rows_sha256=99c6aa1b956c58ef96d8b3ac4cbefeddcd8f927fa235e0f571dbdfad779c3ec3
result_sha256=cdb22066742b427bae5011ed0271dbba4a84bb0dd9838cbd39f5163488ff72bb
seed_affects_output=false
```

Record the two candidate file pins:

```bash
sha256sum \
  deliverables/cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_disposition_ledger.json.gz \
  deliverables/cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_result.json
```

Expected:

```text
c326d50f62a427c71e6f41b188b00b08baf6db7bf535ba082f23678239eebba6  deliverables/cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_disposition_ledger.json.gz
d371d3d6ce01b0779717dc817216204cf0c142d0b95caf42ede3d1d243d5daa2  deliverables/cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_result.json
```

## Producer replay B

Repeat with a different seed and hash seed:

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=302929 \
  python3 -B \
  deliverables/cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure.py \
  --seed 302929
```

Require the same semantic and file pins as replay A. The observed replay
completed in 3:01.25 and was byte-identical.

## Independent verifier replay A

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=302373 \
  python3 -B \
  deliverables/cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_verifier.py \
  --seed 302373
```

Expected:

```text
PASS_INDEPENDENT_ROUND302C_EXACT_25336_RESIDUAL_EARLIEST_P01_DISPOSITIONS__51_OF_51_ATTACKS_REJECTED
attack_suite_sha256=a2fc5550dbf3e28095a0c7dfa04e1b994a86d64d253f6bb988c038cc13b1dabc
verification_sha256=3ae6e3f6fe7acf6e4d5778e6175f99d5553fa7e201cfab11a381d2573d5e3594
```

The verifier must rebuild all expected semantics and bytes before opening the
candidate ledger/result. The producer is checked only as the fixed byte pin:

```text
e583aff49329c047ae9797084bfba8509b1a3184f2bb04b63de2351f04adbaef
```

## Independent verifier replay B

The second verifier replay must not write artifacts:

```bash
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=302977 \
  python3 -B \
  deliverables/cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_verifier.py \
  --seed 302977 \
  --no-write
```

Require the same attack-suite and verification self-closures as replay A.
The observed replay completed in 5:20.22, rejected 51/51 attacks, and left the
attack/verification file pins unchanged.

## Final package check

```bash
cd deliverables
sha256sum -c \
  cm2_round302c_source_g_r248_residual_single_endpoint_sheet_disposition_closure_manifest.sha256
```

Exactly eight entries must report `OK`: producer, disposition ledger, result,
independent verifier, attack suite, verification, report, and cold replay.

This replay establishes only the complete R248 sheet **attachment disposition
frontier**. It issues zero formal maximality credit and does not by itself
prove maximal physical components.
