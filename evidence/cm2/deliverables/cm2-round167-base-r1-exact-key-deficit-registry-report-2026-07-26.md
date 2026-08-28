# CM2 Round167 — bounded base-R1 exact-key deficit registry

Date: 2026-07-26

## Decision

Round167 certifies a bounded bookkeeping sub-gate.  It does not promote
Gate5 and does not borrow the local `18/18` result from Round135.

The exact-key registry contains:

```text
base-R1 component/source-word attachment rows       32
official source-word deficit rows                    16
open global field rows                                8
source-word × open-field deficit cells              128
global complete 18-field blocks                       0
global Gate5 maturity                             10/18
```

The eight still-open global fields are

```text
F5, F6, F10, F11, F14, F15, F17, F18.
```

## Binding discipline

The 32 local numerical attachment rows retain their real component and
official source-word keys.  Local `F10/F13/F16` values are not merged across
the two components of a source word, attached to a destination word, or
given invented `homogeneous_subbranch`, owner, `t54`, or `q_j` keys.

Round131 ordinal `346720`, Round133 observed-occurrence rows, and Round135
local fibre rows remain explicitly non-promotable because they belong to
different physical roots or incomplete registries.  Round135 therefore
contributes zero global Gate5 credit here.

## Verification

The verifier does not import or execute the Round167 producer.  It
independently reconstructs the complete expected result:

```text
component attachment rows                32
source-word deficit rows                 16
open global field rows                    8
source-word/open-field deficit cells    128
```

Exact canonical equality is required.  All 14/14 semantic mutations are
re-signed before verification and rejected.  Strict canonical JSON,
duplicate-key, symlink, hard-link, output-alias, and atomic-write guards are
also enforced.

Producer and verifier cold replays under distinct `PYTHONHASHSEED` values
were byte-identical.  A parent-thread replay reproduced the published
verification file exactly:

```text
certificate result
  de11046ac15949b5e69493987d3963c5547be77ba741a55bb10f9e3ad170b552
verification result
  0aa1cb693105f92c77241fe1238d9cc0f494ecb82a5130a3ce23d1555fea3c5a
verification status
  PASS
```

## Strict state

At the Round167 snapshot:

```text
D02                                  BLOCKED
global Gate5                         10/18
global complete 18-field blocks          0
CM2                        NO-GO_FOR_CLAIM
```

The dependency order remains

```text
D02 -> D03 -> D04 -> D07 -> D09 -> D10 -> D11 -> D12 -> D13
    -> F5/F6/F10/F11 -> F14 -> F15 -> F17 -> F18.
```

Round148 already makes `D05`, `D06`, and `D08` available, but that does not
skip the open dependencies above.
