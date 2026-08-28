# CM2 one-hundred-twenty-fifth direct assault

Date: 2026-07-23  
Result: **248/248 re-signed semantic mutations and 15/15 strict-JSON attacks
rejected.**

## Test contract

Every semantic mutation is applied to a deep copy of the final Round125
certificate.  The attack harness re-signs every affected nested row,
aggregate digest, crosslink, and outer result envelope before presenting the
mutant to the verifier.  The assault therefore targets the closed
mathematical contract rather than relying on stale hashes.

The canonical verification artifact freezes two ordered,
duplicate-free arrays:

```text
semantic_mutation_rejection_labels
strict_json_attack_rejection_labels
```

Their lengths and rejection totals are:

```text
semantic mutations  248/248 rejected
strict-JSON attacks 15/15 rejected
```

Every listed mutant is rejected after independent reconstruction.

## Semantic assault coverage

The final re-signed suite covers:

- closed schema enforcement, missing or unknown result fields, status
  downgrades, upstream byte pins, nested row digests, aggregate digests, and
  the outer result digest;
- virtual F18 installation, local maturity inflation, a false complete
  18-field block, global Gate5 inflation, or a false CM2 promotion;
- deletion, duplication, reordering, rank/stage changes, child rewiring, and
  owner/chart corruption in any of the 72 graph-current rows;
- mutation of `eta`, the target radius, either Eulerian component, the exact
  divergence identity, the same-colour zero, guarded interval endpoints,
  actual absolute uppers, or cross-precision containment flags;
- replacing a positive target-cosine lower by zero or a value that violates
  `1/c<=2^B`, inferring `B` solely by reversing F11, or changing the
  stagewise `15/14/14` ranks;
- deleting the density normalization, changing `L<=delta<1`, reversing the
  normalization/sup inequality, or dropping the factor
  `M||rho||_infinity` from the bulk or trace payment;
- removing the mandatory input factor
  `J_*^in=|partial_x ell_*|`, changing a face speed, changing an orientation,
  or permitting unconditional cancellation at one of the 69 adjacent input
  incidences;
- deleting, duplicating, relabelling, or cross-wiring any of the four
  recipient components or any of the 72 physical routes;
- mutating a source/target component row hash, Round122 boundary row,
  Round124 family row, graph-current row, same-key F11 slot, authoritative
  dynamic F11 row, or Piola/current identity in a recipient map;
- changing one of the F11/Piola bounds `4915200/2457600/2457600`, replacing
  the two-component vector current by a scalar tangential test, or adding a
  transparent-roof operator factor;
- deleting or rewriting one of the three source-injection contracts,
  changing `25*2^B+27`, or breaking the acyclic
  `contract -> leg -> derivation -> F17` dependency direction;
- deleting a graph ID/hash pair from a stage derivation, pairing an ID with
  another leg's hash, changing the canonical 24-leg digest, or retaining a
  bare narrative boolean after its row evidence has been removed;
- deleting, duplicating, reordering, or relabelling any of the 144 input
  traces, 432 output traces, or 215 output incidence rows;
- changing a Round124 input-family tag domain, an input materialized recut,
  a Round123 cut canonical digest, a root-velocity witness, or an
  unnormalized-density witness;
- cancelling across distinct input-family tags, cancelling one of the 23 old
  inter-child incidences, retaining one of the 192 same-input new-cut
  incidences, or assigning output-fragment tags before certified internal
  cancellation;
- forcing two adjacent new-cut output cells to have one natural-cell ID, or
  forcing the two sides of an old input cut to have distinct output-cell IDs;
- deletion, duplication, reordering, immutable-key corruption, wrong roof,
  wrong stage, wrong field/value, graph/map/contract/derivation rewiring, or
  F11/F15 cross-key rewiring in any of the 120 F17 slots;
- treating the three-leg product as a one-step F17 value, treating 432 trace
  rows or 216 fragments as source slots, or multiplying F17 by the roof or
  fragment count;
- changing the 120 new-slot count, the 2040 combined count, any slot-ID
  digest, the certified field list `1..17`, or the remaining field `[18]`;
- removing any strict nonclaim concerning global scope, inter-child traces,
  F18, complete blocks, global Gate5, or CM2.

Every accepted final attack must be rejected by mathematical or schema
reconstruction.  Rejection only because an obsolete digest was not
re-signed does not count.

## Strict JSON mutations

The strict-parser suite should retain the established attacks:

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

The authoritative strict-parser count is `15/15`.

## Canonical contract to preserve

After every rejected mutant, the unchanged canonical certificate must still
reconstruct as:

```text
actual common children                         24
graph-current leg rows                         72
recipient components                            4
recipient pullback maps                        72
source contracts / derivations                3 / 3
input artificial traces                       144
stage-3 output artificial traces              432
stage-3 incidences cancelled / retained    192 / 23
retained typed output trace sides              48
new F17 full-key slots                         120
stage slot counts                         48/24/48
combined child-local slots                    2040
child-local fields                    F1-F17 = 17/18
F18                                  NOT_INSTALLED
global Gate5                                10/18
complete 18-field blocks                         0
Gate5 blocks                                     0
CM2                                   NO-GO_FOR_CLAIM
```

Final status:

```text
semantic mutations rejected  248/248
strict-JSON attacks rejected 15/15
```
