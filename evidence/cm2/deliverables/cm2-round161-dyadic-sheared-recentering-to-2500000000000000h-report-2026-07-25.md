# CM2 Round161 — dyadic sheared recentering to 2500000000000000h

Date: 2026-07-25

## Result

Round161 certifies a second correlation-preserving macro slab from
`abs(delta_x)/h=100000` to `2500000000000000`.  Its exact status is

```text
CERTIFIED_DYADIC_SHEARED_RECENTERING_TO_2500000000000000H__D02_STILL_BLOCKED
```

The combined connected corridor is now

```text
abs(delta_x)/h in [0,2500000000000000].
```

It contains 75 exact typed slabs, 225 typed boxes and zero interior untyped
event cells.  The new upper endpoint is explicitly nonterminal.

## Recentered macro coordinate

The exact rational shear is

```text
u = abs(delta_x)/h = -delta_x/h
s = 1403486916994043/500000000000000
w = delta_beta/h - s u.
```

The one new slab has

```text
u in [100000,2500000000000000]
width = 2499999999900000h
equivalent exact 4h slabs = 624999999975000.
```

Its gap-free typed chain is

```text
C24_EVENT             w in [-430,-405]
STRICT_RETURN_BRIDGE  w in [-405,-350]
D3_EVENT              w in [-350,134111000000].
```

The exact internal shared faces are `w=-405` and `w=-350`.  The slab adds
three typed boxes, zero internal untyped cells and zero new event families.

## Exact attachment to Round160

The slope change at the inherited `u=100000` face is

```text
w_new = w_old + 13083005957/5000000000.
```

The three strict physical-beta intersections are

```text
C24
  [280280,1401461916994043/5000000000]
bridge
  [280295,1401736916994043/5000000000]
D3
  [280690,280710].
```

Every intersection has positive width.  The new slab is therefore attached
to the certified Round160 connected sheet in all three typed families; it is
not merely a remote box with the same local labels.

## Complete C24 audit and correlated collision-three anchor

The C24 event graph has strict opposite edge signs, positive `w` derivative,
a parametric interval-Newton image strictly inside `[-430,-405]`, and one
transverse root on every fixed-`u` fibre.  Its complete 1,648-collision path,
official words, wall order, charts, homogeneity, incidence, core margins and
radius-four candidates all pass.

At collision three, the generic axis-box owner routine loses the `(u,w)`
correlation for anchor `W[0,0]`; its compact 256-bit documentary outer
straddles zero.  Round161 does not treat that as an event or increase
precision until a sign appears.  It instead proves at 8,192 bits that:

```text
partial D3/partial w > 0 on the complete C24 macro box
D3 < 0 on the upper C24 face w=-405
therefore D3 < 0 throughout the complete C24 macro box.
```

The correlated miss margin has dyadic depth 4,285.  After this one anchor is
decided by the correlated proof, the pinned complete-owner logic audits the
remaining candidates.  The retained collision-three universe contains 57
candidates; the full radius-four universe contains 161.  Both have exactly
one anchor entry, zero ambiguous nonanchor candidates and the same strict
winner `W[0,-1]`.  The anchor remains counted among all 161 candidate tests.

## Strict-return bridge

The 55h bridge is bounded by the two event families:

- D3 is strictly increasing in `w` and strictly negative at `w=-350`;
- the terminal C24 function is strictly increasing in `w` and strictly
  positive at `w=-405`;
- the terminal phase box has the intended sole unresolved destination-core
  collar;
- the correlated sign proofs force the whole bridge to
  `RETURN_AT_3_INNER`.

The complete 1,648-collision bridge path and all radius-four candidates pass.
The bridge was deliberately widened from an earlier rejected 3h design:
that narrow design classified the terminal return directly and did not have
the collar shape required by the pinned bridge verifier.

## D3 event box

The D3 graph has strict opposite edge signs, positive `w` derivative, a
parametric Newton image strictly inside
`[-350,134111000000]`, and one transverse root for every fixed `u`.

The collision-three retained and full radius-four universes leave only the
intended anchor discriminant unresolved.  The anchor double root strictly
preempts the frozen nonanchor winner, and all other candidate decisions and
winner gaps are strict.

## Full audit census

```text
new complete R1648 C24 audits                       1
new complete R1648 bridge audits                    1
new collision-stage/object pairs                3,296
new R1648-path radius-four candidate tests     530,656
new complete D3 event-box audits                    1
new D3 event-box radius-four candidate tests      483
new total radius-four candidate tests         531,139.
```

The correlated C24 anchor proof changes the decision method for one
candidate; it does not reduce this census.

## Precision retention

All strict decisions use 8,192-bit Arb enclosures.  The JSON serializes
selected values on a fixed 256-bit rational lattice for deterministic finite
documents.  At dyadic depth 4,285 that display lattice is too coarse:
`D3_upper_w_edge_outer`, and even displayed derivative outers, can straddle
zero although the original Arb predicate is strict.

The decision order is:

1. construct the correlated Arb enclosure at 8,192 bits;
2. require the strict derivative and upper-edge signs;
3. derive the monotone whole-box miss;
4. audit all nonanchor candidates and winner gaps;
5. only then serialize conservative 256-bit documentary outers.

Neither producer nor verifier infers a sign from the coarse display fields.

## Independent verification and attacks

The independent verifier does not import or execute the producer.  It pins
the producer and engine sources, pins the Round160 certificate and verifier,
and reconstructs:

- the complete C24, bridge and D3 typed audits;
- the collision-three correlated anchor proof and both candidate universes;
- the exact rational shear and both internal `w` adjacencies;
- the three slope-change physical-beta intersections at `100000h`;
- the macro width and 624,999,999,975,000 equivalent 4h slabs;
- the complete 531,139-test census;
- the 75/225/0 combined atlas and open upper endpoint;
- every strict nonpromotion field.

It reports `PASS` and rejects

```text
semantic/document mutations        92/92
strict JSON/encoding attacks        12/12.
```

The attack set includes coherent rehashed changes to the huge endpoint, shear,
D3 band, correlated anchor proof, candidate counts, typed-audit digest,
adjacencies, slope-change seam, inherited physical overlaps, census, atlas,
inheritance, compact-domain claims, terminal claims and type-sensitive fields.

## Hashes

```text
Round161 engine source SHA256
  ae5c2ac7d22de85ae4a3d39b3ce42307c5c39e652ed1643a46c5630d746c050f
producer source SHA256
  7122fc6f38389657292160d7fb1a7248434163123853f5dcd5246b48b1efae73
certificate file SHA256
  317ee6a43cd6db687f9ac4b089940c436817b4bfec7449ab778b462cff35e0cd
certificate result SHA256
  842ef791a414e85b5f2eeb458f876d837d269a284f26ae8317059bd4e0fb2f12
verifier source SHA256
  0adfb5e2375a07a487f97ca4c6c9c48a495bac75f4e7719fe03297c304b2839f
verification file SHA256
  01da56a79ec34736946c047784de75aa773e61822ffd45fa8a3fe5cc339832db
verification result SHA256
  5c1a78555644f4fb424e8e164e3088fd24a1d393252a6214d4b8829815571e07
```

The certificate also binds the reconstructed typed audits by
`28fd4c1bd0fe702b2286432ba10a384ccdabf77300610a15bea8872bd50104f7`
and the macro-slab list by
`56dc2575a4d29cbb90308f36764fa723fd7f63082edad594504e904b4b76d765`.

## Compact first-face analysis

The first geometrically forced negative-direction source-chart seam is

```text
A=-pi/4,
u approximately 2^4295.086903144661.
```

It is a transverse nonterminal `E -> S` chart gluing, not a terminal escape.
The current result does not assert that no owner, discriminant, wall,
homogeneity, incidence or core margin vanishes earlier.  A future
continuation must export all named margins and type whichever one reaches
zero first.

The physical quotient is most safely represented by four rational half-angle
source charts over `S^1_A x [-1,1]_p`, with exact cyclic seam gluing and
`p=+/-1` source-grazing strata.  The accompanying compact-angular plan records
the rational map, lift lattice and exterior branch-and-bound leaf taxonomy.

## Strict nonpromotion and next gate

Round161 advances the connected typed sheet by
`2,499,999,999,900,000h`.  It does not certify a terminal upper endpoint,
the compact fundamental angular cell complex, a globally first event, or
disconnected-exterior-sheet exhaustion.

```text
D02                                  BLOCKED
D03 negative oracle            unauthorized
global Gate5                         10/18
global complete blocks                   0
CM2                        NO-GO_FOR_CLAIM.
```

The next core gate is to continue with validated compact/dyadic checkpoints
that export all named first-face margins, type and glue the first certified
chart/owner/event/terminal face, and then complete the four-chart exterior
branch-and-bound with zero unresolved leaves.

The local 8,192-bit Arb affine engine was sufficient for this round.  No new
external dependency was introduced; the previously reviewed
QR/Lohner/Taylor-model/Krawczyk routes remain fallbacks if compact-angle
continuation develops new wrapping.
