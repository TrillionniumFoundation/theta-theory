# CM2 one-hundred-twenty-fourth direct assault

Date: 2026-07-23  
Result: **154/154 semantic mutations and 15/15 strict-JSON mutations rejected.**

## Test contract

Every semantic mutation is applied to a deep copy of the final Round124
certificate.  The verifier re-signs the affected nested rows and the outer
result envelope before evaluating the mutant.  These tests therefore attack
the closed mathematical contract rather than relying on a stale digest.

The authoritative ordered labels are frozen in
`semantic_mutation_rejection_labels` and
`strict_json_attack_rejection_labels` in the canonical verification
artifact.  Both arrays have unique labels and exact lengths `154` and `15`.

## Semantic assault coverage

The 154 re-signed attacks cover:

- schema closure, missing/unknown result fields, status downgrades, upstream
  byte pins, and frozen Round122/Round123 contracts;
- virtual installation of F17/F18, local/global maturity inflation, complete
  blocks, Gate5 blocks, and a false CM2 promotion;
- positive mass and density, normalization, the accepted regularity cone,
  the strong norm, countable finite-norm completion, and tag preservation;
- Jordan factor-two or cancellation errors, equal-mass assumptions, missing
  Jacobians, missing conditional normalization, retained zero-mass outputs,
  and fragment/member multipliers;
- changing `F15=34`, renaming F15 as F14, deleting its strict gap, confusing
  roof slots with repeated physical operators, or replacing the Tonelli
  family estimate by a fragmentwise estimate;
- the adapted contraction, `C_p^*`, additive raw-`Z_*` debt, recovery clock,
  all three stagewise source/output coefficients, and strict properness;
- conflating local `Z_*` with Round61 `Z_col`, or promoting the Round61,
  Round62, and Round65 global frontiers;
- deletion, duplication, reordering, relabelling, cross-child rewiring, false
  endpoint ownership, nonzero cemetery arrival, discarded relative domain,
  ambient cemetery installation, or geometry deduplication in any of the 72
  relative zero-cemetery rows;
- deletion, duplication, reordering, wrong stage/rank/owner/chart/recut,
  cross-wired F7/F14 dependencies, fake input/output lengths, altered output
  members or tags, lost mass identity, wrong F15 value, cemetery crosslink,
  roof duplication, or misuse of bypass `b3` in any of the 72 family rows;
- deletion, duplication, reordering, immutable-key corruption, wrong roof,
  stage, field, value, recut, member, dependency, operator row, cemetery row,
  projective/Jordan status, direct-path confusion, or payload-as-slot
  promotion in any of the 120 F15 slots;
- wrong inherited/new slot counts or ID digests, an inflated 2160-slot
  registry, false inclusion of F17, and removal of F17 from the uninstalled
  list.

Every attack is rejected after reconstruction; none relies only on the
certificate's stored row or result digests.

## Strict JSON mutations

The exact strict-parser attacks are:

```text
duplicate top-level key
duplicate deep key
NaN constant
Infinity constant
negative Infinity constant
JSON decimal float
JSON exponent float
top-level array
top-level null
UTF-8 BOM
invalid UTF-8
unpaired surrogate
bool masquerading as integer
noncanonical fraction
zero-denominator fraction
```

All `15/15` are rejected.  Duplicate keys, non-finite and floating JSON
numbers, wrong top-level types, byte-encoding faults, boolean-as-integer
confusion, and noncanonical rational syntax remain fail-closed.

## Canonical contract after assault

The unchanged canonical certificate independently verifies with:

```text
actual common children                         24
family-leg operator rows                       72
relative zero-cemetery rows                    72
tagged stage-3 payload members                216
new F15 full-key slots                        120
stage slot counts                        48/24/48
combined child-local slots                   1920
F15 one-step value                             34
child-local fields                    F1-F16 = 16/18
F17/F18                             NOT_INSTALLED
global Gate5                                10/18
complete 18-field blocks                         0
Gate5 blocks                                     0
CM2                                   NO-GO_FOR_CLAIM
```
