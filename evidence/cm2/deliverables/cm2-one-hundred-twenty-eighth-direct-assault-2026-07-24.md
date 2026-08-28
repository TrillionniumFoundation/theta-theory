# CM2 one-hundred-twenty-eighth direct assault

Date: 2026-07-24

Result: **64/64 semantic mutations and 18/18 strict-JSON attacks rejected.**

## Assault model

Each semantic attack starts from a deep copy of the canonical Round128
certificate.  The outer result digest is recomputed for every candidate.
For row-level attacks, the affected row hash and list aggregate hash are also
recomputed where applicable.  Rejection therefore depends on independent
registry, component, edge, reciprocal-pair, geometry, and safety replay
rather than on a stale outer signature.

The verifier never imports or executes the Round128 producer.

## Envelope, provenance, and global registry

The attack suite rejects:

- a certificate schema change;
- a changed producer provenance pin;
- a changed Round71 upstream pin;
- promotion of the global candidate count;
- alteration of the frozen 441280-row stream digest;
- alteration of the Gate25 core count or core-ID digest.

The verifier independently reconstructs all 448 retained chart/target pairs,
985 crossing patterns, 441280 official candidate rows, 3286976 roof
positions, and 24 Gate25 physical cores.

## Component source/destination role assault

The following component attacks are rejected after re-signing:

- changing the source official-word row, ID, or ordinal;
- changing the destination official-word row, ID, or ordinal;
- swapping all available source and destination roles;
- moving the `F10/F13/F16` attachment role from source to destination;
- orphaning a component, path cell, source core, or trace ID;
- changing the physical face side or local `F10` value;
- directly changing a row hash or aggregate digest;
- reordering, deleting, or duplicating a component row with a recomputed
  aggregate;
- changing the declared 32-row component census.

These attacks protect the directional contract:

```text
numeric F10/F13/F16 fields attach to source official word
destination official word records the terminal path direction
```

Word membership does not erase those roles.

## Directed edge and reciprocal-pair assault

The verifier rejects:

- changing the 16-edge census;
- changing a source or destination word ID;
- swapping source and destination roles;
- moving edge-level numeric attachment to the destination;
- duplicating the two component IDs of an edge;
- orphaning an edge path-cell ID;
- breaking a directed core edge;
- reordering edge rows with a recomputed aggregate;
- changing the eight-pair census;
- orphaning a reciprocal edge ID;
- disabling exact reverse direction;
- duplicating the reciprocal source-word IDs.

The independently reconstructed 16 directed edges must equal Round69's
16-edge set.  Each edge has exactly two distinct components, and the eight
unordered pairs each contain exactly the two reverse directions.

## Round67 typed-crosswalk assault

The suite rejects:

- promoting the actual join from `0/12` to `1/12`;
- deleting one of the twelve missing recordwise fields;
- inventing a Round67-to-Round72 component crosswalk row;
- changing the required field count from twelve.

This preserves the distinction between a Round67 occurrence/owner subroot
and the Round71/Round72 component/path-cell root.  Matching names, times,
ranks, sides, coordinates, or official words are not a recordwise typed
incidence graph.

## Exact-overlap and physical-separation assault

The suite rejects:

- changing the sole overlap official word;
- promoting symbolic overlap to the same physical root;
- promoting it to the same operator block;
- replacing destination ordinal `102440` by exact stage-0 ordinal `102441`;
- replacing destination ordinal `102440` by exact stage-2 ordinal `180256`;
- expanding the exact stage-1 `t` interval into Gate25 core16;
- expanding the exact stage-1 `p` interval into Gate25 core16;
- changing the two-component overlap census.

The independent 2048-bit replay retains:

```text
1/2 < t < 3/5 < 69/100
-1/2 < p < -2/5 < -1/50
0 < first-collision flight time < 3
```

Thus ordinal `346720` is a symbolic overlap only.  Its two local component
rows do not share the Round121 physical root, subbranch, or operator block.

## Lower-bound and global nonpromotion assault

The suite rejects:

- changing the scoped lower bound `26`;
- replacing the global exact nonempty count `null` by `26`;
- claiming a complete global domain census;
- changing the scoped union count;
- repeating the `null -> 26` promotion in the global safety ledger;
- inventing a global complete 18-field block or Gate5 block;
- promoting Gate5 to certified or CM2 to go-for-claim;
- claiming arbitrary return-depth certification;
- deleting a strict nonclaim;
- adding an unknown result field.

The finite set identity

```text
24 Gate25 words union 3 exact-path words
with one shared word = 26 distinct words
```

proves only a locally certified nonempty-key lower bound.

## Strict JSON assault

The byte-level parser rejects all 18 attacks:

```text
duplicate top-level schema key
duplicate nested status key
floating-point integer
NaN constant
positive Infinity constant
negative Infinity constant
UTF-8 BOM
invalid UTF-8
top-level array
top-level null
trailing second document
oversized integer
negative zero
leading-zero integer
closed envelope extra key
closed result extra key
stale outer result digest
unpaired surrogate
```

Duplicate keys, nonintegral or nonfinite numbers, noncanonical integers,
encoding errors, wrong top-level types, widened schemas, trailing documents,
stale signatures, and invalid Unicode are all fail-closed.

## CLI and output-path assault

```text
valid official certificate             rc=0, PASS
missing certificate                    rc=1, fresh output absent
different/tampered certificate         rc=1, fresh output absent
dangling output symlink                rc=1, target absent
output hardlink to pinned upstream     rc=1, upstream unchanged
nonregular output target               rc=1, no artifact
```

The verifier enforces the official certificate byte and result hashes.  Its
protected output set includes the certificate, producer, verifier, and every
pinned upstream artifact.  Resolved paths and inode identity are both
checked.

Two full verifier runs under `PYTHONHASHSEED=0` and `987654321` produced
byte-identical verification artifacts.

## Frozen executable and artifact hashes

```text
producer       d218d92a6aa7a929e734c86110e67ec8ebea75b3c57bf74e5a7d3b3e33d32e35
certificate    7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e
verifier       2745ccccdab9869c4754bab37f13ece70f32c7b59063bf0aed4f59cdd81af544
verification   3798cb3e38b7f26de0a5361234d57ef626bd7f990e26d6c787f0abf62647a76d
```

## State after assault

```text
global symbolic word keys                         441280
Round71/Round72 physical components                   32
directed source/destination word edges                16
reciprocal word pairs                                  8
Round67 joined fields                               0/12
locally certified nonempty-key lower bound            26
global exact nonempty candidate-key count           null
global complete 18-field blocks                        0
Gate5 blocks                                            0
global Gate5 maturity                               10/18
Gate5 status                                NOT_CERTIFIED
CM2                                        NO-GO_FOR_CLAIM
```

The assault protects the boundary between typed local physical incidence,
symbolic official-word membership, absent recordwise owner-root joining, and
absent global operator-block coverage.
