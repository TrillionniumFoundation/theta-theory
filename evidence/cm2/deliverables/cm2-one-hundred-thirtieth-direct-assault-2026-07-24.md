# CM2 one-hundred-thirtieth direct assault

Date: 2026-07-24

Result: **78/78 fully re-signed semantic mutations and 16/16 strict-JSON
attacks rejected.**

## Assault model

Every semantic case starts from a deep copy of the official Round130
certificate.  After the selected value is changed, the assault harness
recomputes:

```text
affected row_sha256 values
dependent row-hash crosslinks
all 24 registry aggregate hashes
outer result_sha256
```

The independent verifier therefore cannot reject a case merely because its
old hash became stale.  Rejection comes from independent mathematics,
canonical-key rules, exact registries, typed crosslinks, count closure, or
the fail-closed safety contract.

The verifier never imports or executes the Round130 producer.

## Provenance and canonical-lambda assault

The suite rejects changes to:

- certificate status or precision;
- the frozen Round129 verification verdict;
- canonical exact-lambda key version or mathematical fibre key;
- normalized-coordinate range;
- the non-eventually-one binary convention;
- the dedicated `u=1` upper-endpoint case;
- rejection of noncanonical lambda locators;
- lambda-key uniqueness;
- the ban on independently supplied `b` keys;
- the statement that the uncountable family is not finitely serialized.

The verifier independently exercises:

```text
u=0       NORMALIZED_BINARY, eventually all 0
u=1/2     terminating dyadic, eventually all 0
u=1       UPPER_ENDPOINT, no binary sequence
```

It re-isolates all three analytic roots at 4096-bit precision and proves that
the forward-derived `b` enclosures are strictly ordered.  Actual object IDs
are derived from the shared canonical lambda key; a separate `b` locator
cannot select or alter the fibre.

## Widened stage-three assault

Re-signed attacks are rejected when they:

- reuse the narrow Round123 exact-seed guard claim;
- change the merged-cut count;
- flip an endpoint sign;
- remove the canonical key from an actual endpoint constructor;
- relabel the terminal natural cell;
- alter a merged-cut origin;
- move a fragment to another common rank;
- treat a fragment template as an actual whole-family row;
- make a child partition nonexhaustive;
- remove arbitrary-density acceptance from a norm leg.

The verifier independently proves

```text
192 < U3/delta   < 193
192 < U3_x/delta < 193
```

and checks all 192 root guards, 193 natural cells, 215 ordered cuts, 216
positive output fragments, 24 exhaustive partitions, and 72 accepted norm
legs.

## F14 assault

The suite rejects:

- an artificially improved F14 value;
- paying F14 with the empty local F10 dependency;
- removing the canonical lambda key from an actual F14 slot.

The verifier reconstructs all 120 F14 rows from the accepted norm legs and
their same-key F10/F13/F16 dependencies.  It requires the genuine
arbitrary-positive-density one-step value `<34`, signed Jordan extension,
and absence of a fragment-count multiplier.

## F15 and cemetery assault

The suite rejects changes that:

- make the relative partition nonexhaustive;
- invent positive relative cemetery arrival;
- claim ambient pre-regularization cemetery;
- claim all-time owner cemetery;
- allow cross-member or cross-tag deduplication;
- improve the F15 value without proof;
- remove Tonelli completion;
- install a global raw-Z theorem;
- convert relative-zero cemetery into ambient cemetery.

The verifier closes 72 relative-cemetery rows, 72 standard-family operators,
and 120 F15 slots.  It keeps the strict boundary:

```text
restricted relative cemetery          ZERO
ambient cemetery                      NOT_INSTALLED
all-time owner cemetery               NOT_INSTALLED
global raw-Z/Orlicz theorem            NOT_CLAIMED
```

## F17 trace and graph-current assault

Typed trace mutations are rejected when they:

- relabel an artificial input trace as physical;
- allow cross-tag cancellation;
- cancel an inter-child input incidence;
- drop the stage-three Jacobian;
- permit cross-lambda output incidence;
- retain a same-input pair that must cancel;
- alter a source-injection rank;
- change a graph-current orientation coefficient;
- replace physical boundary traces by artificial ones;
- erase the artificial/physical crosswalk;
- collapse the recipient to a scalar-only space;
- corrupt a Piola determinant identity;
- collapse a pullback to one component;
- alter the three-leg source derivation;
- rename F17 as the diagnostic along-curve F11;
- improve a stagewise F17 value without proof;
- allow cross-lambda cancellation in the family contract.

The independent `lambda × s` replay checks:

```text
input artificial traces                 144
input inter-child incidences              69
stage-three output traces                432
stage-three output incidences            215
same-input cancellations                 192
retained inter-child incidences           23
graph-current legs                        72
recipient components                       4
Piola pullback maps                        72
source derivations                          3
F17 slots                                120
```

Every cancellation requires one exact lambda and one family tag.  The 23
inter-child incidences remain as two typed traces before total variation.

## Same-key and F18 assault

The suite rejects:

- changing the F1–F17 binding count;
- breaking the shared operator carrier;
- removing the canonical lambda key from an actual same-key map;
- changing the direct-standard-N route;
- changing a phase suffix;
- claiming Wiener invertibility;
- claiming Wiener aperiodicity;
- claiming Kac closure;
- claiming global phase registration;
- claiming CM2;
- changing a level block from 18 fields;
- promoting a level block or child packet to global scope;
- changing a child-packet level count;
- promoting the family-level phase contract.

The verifier reconstructs 120 exact-once F1–F17 maps, 120 F18 slots, 120
local level blocks, and 24 local child packets.  F18 remains the structural
identity

```text
z^j*z^(r-j)=z^r
z^2*z^1*z^2=z^5
```

and nothing stronger.

## Actual-slot crosswalk assault

For each of the three canonical lambda vectors, the verifier independently
derives:

```text
one exact b key
one actual parent
24 actual refined children
120 actual base keys
2160 unique actual F1-F18 slots
120 local complete 18-field blocks
```

The three slot sets are pairwise disjoint.  This directly tests the
one-way lambda-to-`b` derivation, shared immutable key, exact field census,
and prohibition on cross-fibre identification.

## Count and global-promotion assault

The suite rejects:

- changing the combined finite template-row count;
- assigning a finite whole-family actual row count;
- inventing a global block in the count ledger;
- relabelling local 18/18 as global 18/18;
- inventing global complete blocks;
- inventing complete blocks or Gate5 blocks;
- promoting Gate5 from 10/18;
- changing Gate5 to certified;
- changing CM2 to go-for-claim;
- deleting the global nonclaim.

The finite 2814 rows are templates.  Per-fibre counts do not become the
cardinality of the uncountable family and do not become global Gate5
coverage.

## Strict JSON assault

The byte parser rejects all 16 attacks:

```text
duplicate top-level schema key
duplicate nested key
NaN
Infinity
-Infinity
decimal float
exponent-form float
negative zero
oversized integer
UTF-8 BOM
invalid UTF-8
NUL byte
top-level array
trailing garbage
unpaired surrogate
truncated JSON
```

The parser enforces duplicate-free UTF-8 JSON, canonical signed-64-bit
integers, no floats or nonfinite constants, no invalid Unicode, and a closed
certificate envelope.

## CLI, link, and nonregular-file assault

```text
valid official certificate       rc=0, PASS
missing certificate              rc=1, output absent
tampered certificate             rc=1, output absent
certificate symlink              rc=1, output absent
certificate hardlink             rc=1, output absent
certificate FIFO                 rc=1, output absent
output symlink                   rc=1, sentinel unchanged
output hardlink                  rc=1, sentinel unchanged
output FIFO                      rc=1, FIFO unchanged
protected producer output        rc=1, producer unchanged
```

Input and output checks cover type, link count, resolved path, and inode
identity.  The protected set includes the official certificate, producer,
verifier, Round129 primary inputs, and every byte-pinned upstream or
mathematical helper file.  Successful output is atomic.

Two complete verifier runs under hash seeds `0` and `987654321` produced
byte-identical verification artifacts.

## Frozen hashes

```text
producer
  441b714c6795646a1eeafe94be7419c9b91e14838ea0c321878cde2e11efff31
certificate
  5bbef09b759c33b635edcf74544af8052ec88915e4f323272d27febfbfe220d5
verifier
  59d1becfad10272b56ba034396500424cc1f6b29ab8a4a3673050d77a82cf136
verification
  510ffb04b90277004f2968e27db4367d9253c2e678b51f384dcfd4dc6c241888
```

## State after assault

```text
every exact lambda fibre local maturity       18/18
per-fibre children                                24
per-fibre base keys                              120
per-fibre field slots                           2160
per-fibre local complete level blocks            120
whole-family actual row census                   null
global complete 18-field blocks                    0
Gate5 blocks                                       0
global Gate5 maturity                          10/18
Gate5 status                           NOT_CERTIFIED
CM2                                   NO-GO_FOR_CLAIM
```

The assault protects the precise boundary between one rigorously
parameterized positive-Borel local 18/18 family and the still-absent global
all-word, arbitrary-return-depth, same-physical-root Gate5 theorem.
