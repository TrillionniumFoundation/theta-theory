# CM2 Round128 — base-R1 component / global-word incidence

Date: 2026-07-24

Verdict: **VERIFIED for 32 nonempty base-R1 physical face components,
16 directed source/destination official-word edges, and eight reciprocal
word pairs.  This is a typed incidence crosswalk, not a global domain census
or an 18-field block upgrade.**

## Certified crosswalk

Round128 joins the frozen Round71/Round72 base-R1 component records to the
frozen global symbolic return-word namespace through the immutable physical
core and directed path-cell IDs:

```text
Round72 numeric component fields
  -> Round71 terminal physical face component
  -> directed base-R1 path cell
  -> source Gate25 core / source official word
  -> destination Gate25 core / destination official word
```

The independent replay gives:

```text
nonempty physical face components                         32
directed source/destination path cells                     16
components per directed edge                                2
reciprocal unordered word pairs                             8
distinct source official words                             16
distinct destination official words                        16
source and destination word sets                  exactly equal
one-sided trace incidences                                  64
```

Every directed edge preserves two distinct roles.  The Round72 numeric
`F10/F13/F16` data attach to the **source official word**.  The destination
official word is separately registered as the terminal direction of the
physical path cell.  Swapping the roles or moving the numeric attachment to
the destination is rejected.

The 16 directed edges are eight exact reciprocal pairs:

```text
Gate25 core indices
1 <-> 15     2 <-> 18     4 <-> 12     5 <-> 21
7 <-> 13     8 <-> 22    10 <-> 16    11 <-> 19
```

Equivalently, their source-word ordinals pair as:

```text
 42355 <-> 342780      43340 <-> 397940
154645 <-> 236400     157600 <-> 290575
212760 <-> 237385     215715 <-> 291560
102440 <-> 346720     103425 <-> 401880
```

The verifier also requires exact equality with the 16 directed core edges
materialized by Round69.

## Independent global-registry and Gate25 replay

The verifier does not import or execute the Round128 producer.  It
independently applies the exact-rational horizon and outgoing-support filters,
enumerates all clean-wall crossing patterns, and reconstructs all 24 Gate25
physical cores.

```text
source normal charts                                      8
conservative target lifts                               162
retained chart/target pairs                             448
crossing patterns per retained pair                     985
candidate symbolic return-word keys                  441280
symbolic word/roof positions                         3286976
Gate25 physical cores                                    24
distinct Gate25 official words                           24
```

Frozen global replay digests:

```text
chart/target pairs
  ccf4e9e42c7b17f6ebb7f33ec707616bb49ec1d755a817ce141dc92d47056f75
crossing patterns
  2d655b1b83918b0cc42845e465d05f7309657b776f0acbd3d3003e8ae17bb39d
441280-row canonical stream
  841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9
```

For every one of the 32 components, the verifier independently reconstructs
the component ID, source and destination core IDs, destination face ID,
path-cell ID, both trace IDs, both official-word rows, pair/pattern indices,
global ordinals, stable incidence-row ID, row closure, and list closure.  The
Round71 witness row and Round72 field row must form an exact four-way join
with their two manifests.  The replay additionally checks:

```text
F10 integer upper bounds                  min 3, max 39, sum 480
F13 current-variation strict-upper sum                 4/125000000
F16 Piola-flux strict-upper sum                         4/125000000
```

## Sole exact-seed word overlap

The 16 source official words intersect the three Round121/Round127 exact-seed
words in exactly one symbolic key:

```text
overlap source ordinal       346720
overlap row                  ["W:N","G[1,1]",[],1]
overlap Gate25 core index    16
overlap components           2
directed destination ordinal 102440
```

The exact-seed word ordinals are:

```text
stage 0   102441
stage 1   346720
stage 2   180256
```

Therefore the overlap edge destination `102440` is neither the exact stage-0
word `102441` nor the exact stage-2 word `180256`.  The one-unit ordinal
difference between `102440` and `102441` is preserved and tested.

Symbolic equality at ordinal `346720` does not identify a physical root.  A
fresh 2048-bit interval replay from the byte-pinned Round121 anchor bracket
gives the exact stage-1 curve in the common `W:N` chart:

```text
Round121 stage-1 t        1/2 < t < 3/5
Gate25 core16 t          69/100 <= t <= 7/10

Round121 stage-1 p       -1/2 < p < -2/5
Gate25 core16 p          -1/50 <= p <= 1/50
```

Thus:

```text
3/5  < 69/100
-2/5 < -1/50
```

and the physical rectangles are strictly disjoint in both coordinates.  The
verifier independently checks the positive first-collision discriminant, the
strict flight window `0 < tau < 3`, the `N` chart, and both coarse bounds.
No tight producer dyadic endpoint is used.

## Round67 owner/root boundary

Round67 retains an occurrence/owner physical subroot, but it does not
materialize the recordwise identifiers needed to join that subroot to a
Round71/Round72 component.  Round68 requires the following exact composite
key:

```text
restriction_id
return_component
insertion_time
collision_index
event_signature
primitive_key
owner_key
rank_zero_component
plaque_side
word_cell
endpoint_coordinate
root_coordinate
```

The actual join remains:

```text
joined required fields                          0/12
Round67 -> Round72 component crosswalk rows        0
direct source-point equality audit pairs        11264
direct source-point equality intersections          0
```

The correct missing object is a typed physical-face incidence graph to the
path cell, carrying all twelve recordwise coordinates plus the immutable
component/core/path/word IDs.  Equal time, rank, side names, coordinates, or
official words do not create that graph.

## Scoped nonempty-key lower bound

The union of the two already certified finite local sets is:

```text
Gate25 locally certified nonempty words              24
Round127 exact-path locally certified nonempty words  3
set intersection                                      1
set union                                             26
```

Consequently `26` is a **locally certified lower bound** for the number of
nonempty global candidate keys.  It is not the exact global count, not a
complete nonempty-or-empty census, and not a coverage fraction:

```text
locally certified nonempty-key lower bound             26
global exact nonempty candidate-key count             null
all 441280 candidate domains decided                  false
complete global nonempty-or-empty census              false
```

## Independent verification

```text
status                         PASS
semantic mutations rejected   64/64
strict-JSON attacks rejected   18/18
producer SHA256                d218d92a6aa7a929e734c86110e67ec8ebea75b3c57bf74e5a7d3b3e33d32e35
certificate SHA256             7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e
certificate result SHA256      46601ee43c7ca8051dac51fd608605a814abfb755092ea8225fd3f0f2c755815
verifier SHA256                2745ccccdab9869c4754bab37f13ece70f32c7b59063bf0aed4f59cdd81af544
verification SHA256            3798cb3e38b7f26de0a5361234d57ef626bd7f990e26d6c787f0abf62647a76d
verification result SHA256     2037fb4ad60901824b9a107e51b6092f761dcb9b2d47da1c2f76e2cb06926b45
```

The official certificate byte hash and result hash are mandatory verifier
inputs.  Missing, altered, symlinked, hardlinked-to-input, or nonregular
output paths cannot create a verification artifact.

## Frozen safety boundary

```text
global symbolic candidate words                       441280
locally incidence-attached official words                 16
locally certified nonempty-key lower bound                26
global exact nonempty candidate-key count               null
global complete 18-field blocks                            0
Gate5 blocks                                                0
global Gate5 maturity                                   10/18
Gate5 status                                    NOT_CERTIFIED
CM2                                            NO-GO_FOR_CLAIM
```

Round128 does not certify arbitrary return depth, all parameter fibres,
complete physical-domain coverage, a Round67 owner/component join, a global
same-root F1–F18 block, Wiener or Kac closure, Gate5, or CM2.  Its progress is
the first frozen typed incidence from nonempty base-R1 physical components to
directed source/destination global official words.
