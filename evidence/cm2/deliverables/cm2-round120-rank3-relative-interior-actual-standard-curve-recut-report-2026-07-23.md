# CM2 Round120 — relative-interior grazing parent-W children and Gate5 F1–F4 slots

Date: 2026-07-23  
Verdict: **VERIFIED parameterized actual-child registry with child-local Gate5 F1–F4 (`4/18`).**

## Result

Round120 installs a new fixed-`s=0` standard-Borel parent-W registry directly
on the Round113/117 grazing-domain regular relative interiors.  It does not
reuse the physically disjoint compact-Q2 parent-W IDs from Round31.

The frozen certificate contains:

- `72/72` Round113 parent proof boxes: `8` HIT and `64` BYPASS;
- `112` symbolic Round117 generator-family templates, including every
  infinite homogeneity tail;
- `216` official three-leg recut-frontier rows and `360` roof levels;
- `288` transparent-wall roof levels with the required
  collision-to-wall / wall-to-collision split;
- `2,240` unique full-key F1–F4 slot-schema rows;
- `24` independently certified nonempty central-outer parents, which make
  the parameterized child registry nonvacuous.

The rank-3 child-local maturity is therefore `4/18`.  F5–F18 remain
uninstalled on these children.  Global Gate5 remains `10/18`, the complete
18-field block count remains `0`, and CM2 remains `NO-GO_FOR_CLAIM`.

## Physical-domain type correction

Round31 is used only as a Borel-registry design precedent.  Its 24 compact
physical cores satisfy

```text
|p| <= 1/50.
```

The Round120 source-grazing domain has `0<c0<=1/16384` and

```text
p^2 = 1-c0^2 >= 1-(1/16384)^2 > (1/50)^2.
```

The old `time2-atom-id`, Q2 parent-W IDs and branch-rule IDs therefore cannot
be inherited.  Round120 instead uses a new typed parent-W key built from a
repaired endpoint, a canonical angular lift, and the exact intercept `b`.

## Fixed-b intersection theorem

On the source `G` cylinder, `R_G=9/25`, put

```text
phi = sigma0 arccos(c0),
b   = phi - 4 R_G theta_C(t).
```

The four canonical angular lifts are fixed as

```text
E: theta=asin(t)             N: theta=pi/2-asin(t)
W: theta=pi-asin(t)          S: theta=-pi/2+asin(t).
```

For fixed `b`, the verifier independently recomputes

```text
dt/dc0 = -(sigma0 epsilon_C)/(4 R_G)
         sqrt((1-t^2)/(1-c0^2)).
```

Together with the Round112/113 designated-third discriminant this gives:

```text
HIT:    -d(c3^2)/dc0 > 424
BYPASS:  d(b3^2)/dc0 > 480.
```

The 1024-bit replay obtains the stronger global lower bounds

```text
HIT     890069101/2097152
BYPASS  1007197773/2097152.
```

Thus every fixed-b leaf intersects every active half-open R117 operator cell
in either the empty set or one connected interval, with connected rank zero.
The certificate states this as a standard-Borel set-theoretic fibre theorem;
it does not claim a total numerical equality decider for every arbitrary exact
real `b`.

Nonvacuity is paid separately.  Round117 has 24 certified nonempty
central-outer relative-interior operator regions.  Since `B_t` is nonzero,
the `b`-level foliation is regular, so each strict interior point lies on a
locally positive-length fixed-b fibre.  A stable interface seed is frozen at

```text
parent  round113-cell:08b7ca8449af5f6e8d4e3abce98803656664ed7ec957aba62406763b68b2fea6
cell    round117-operator-cell:dca0117235e58b6a0cbc8b9db55ed846b8f26939041fa7eaffd3b68184d54ae1
```

This is an existence interface, not a materialized exact-b witness ID.

## Gate5 F1–F4 binding

The immutable homogeneous-subbranch identity is exactly the inherited
Round117 operator-cell ID.  A carrier child has the canonical typed payload

```text
(round120-child-v1,
 typed-parent-W-id,
 round117-operator-cell-id(active-labels),
 source-interval-rank,
 source-adapted-index-k,
 connected-rank-0).
```

Slots use the formal Gate5 key

```text
(official-word-key-id, homogeneous-subbranch-id, roof-level-j, field-name).
```

F1 records the empty-or-connected-domain theorem and positive-length emission
condition.  F2 records source, middle H0 and actual-third homogeneity; on
BYPASS cells the third collision is the actual G-winner and `b3` is never
treated as a collision angle.  F3/F4 are rebuilt at every roof level:

- roof one: typed collision-source to typed official-relative-target chart;
- roof two: collision-source to the oriented transparent-wall chart, then
  that wall chart to the typed official-relative-target chart.

The actual owner tuple is replayed separately and is not confused with the
relative target stored in the official word key.

## Boundary ownership

The natural boundaries `c0=0`, `c3=0` and `b3=0` are individually owned by
the singular ledger.  A regular child owns none of them.  Among artificial
boundaries, the unique Round113 dyadic owner, Round117 homogeneity owner and
corrected source-adapted owner are combined by conjunction; one artificial
layer never overrides another.

The corrected source grid uses Round47 adapted arclength,

```text
u_*(r) = integral (kappa_G+4) dr = (61/9)(r-r_left),
```

with half-open cells of adapted length `1e-90`.  The superseded Round31
Euclidean-cell interpretation is not reused.

## Independent verification

The verifier uses 1024-bit Arb arithmetic and imports neither the Round120
producer nor a shared Round120 mathematics helper.  It independently checks:

- all `38/38` runtime and upstream byte pins;
- all 24 Round31 physical cores and their momentum bound;
- all 72 parent joins and 216 official legs;
- all 112 generator templates, 360 roof levels and 2,240 slot rows;
- the 24 nonempty Round117 central-outer parents;
- HIT/BYPASS derivative signs and bounds, H0 margins, chart margins,
  repaired endpoint IDs, owner/path/word crosswalks and every nested digest.

It rejects `49` uniquely labelled re-signed semantic mutations and `15`
strict-JSON mutations.  Two independent producer replays and two independent
verifier replays are byte-identical to their canonical artifacts.

## Strict nonclaims and next blocker

Round120 deliberately leaves all of the following at zero or uninstalled:

- materialized exact-b witness IDs;
- actual image-recut interval instances and natural image indices;
- pulled-back image-cut common-refinement ranks;
- child-local F5–F18;
- finite counts for the Borel child/recut registries;
- endpoint-inclusive physical collars, cross-trace union reach and a
  whole-face physical-owner atlas.

The next core round must materialize the three image-recut endpoints, their
natural adapted indices and the pullback common refinement on the same child
IDs.  Only then may the universal F5/F6 seeds be restricted and installed.

