# CM2 Round 69 — base-parameter return root, incidence correction, and all-gate assault

Date: 2026-07-21  
Scope: append-only continuation from the frozen Round-68 aggregate  
Strict verdict: **Round 69 constructs a positive actual `s=0` depth-one
return root with 176 half-open-owned atoms and identifies the exact physical
reason why the Round-68 direct-equality route cannot work: moving first-event
occurrence faces are disjoint from the C24 return-core interior.  The correct
bridge is a typed path-cell/face incidence graph.  No arbitrary-time incidence
component is materialized, no composite gate closes, and CM2 remains
`NO-GO_FOR_CLAIM`.**

## 1. Positive actual root at the base parameter

The frozen full-core ledger has 4,216 `RETURN_AT_1_INNER` atoms.  Exactly 352
closed parameter boxes touch `s=0`.  The already frozen ownership convention is
lower-closed/upper-open, so exactly the 176 boxes with lower endpoint zero own
the base fibre; the 176 boxes ending at zero do not.

Their disjoint owned `(collision-section,t,p)` rectangles form a positive
actual base-parameter root.  Exact replay gives:

```text
owned s=0 return atoms                         176
source cores / destination cores              16 / 16
directed source-to-destination core edges      16
unordered reciprocal core pairs                 8
depth histogram                       13:16, 14:116, 15:44
fixed-s collision mass lower             191/8000000
fixed-s collision mass upper       267591/8000000000
```

Every atom has one strict first-collision owner, lands strictly inside its
declared destination core at time one, has invariant collision-area inverse
Jacobian one, and has zero log area-Jacobian distortion.  This is an actual
finite depth-one return graph at the same base parameter used by `m_occ`; it is
not an all-depth invariant return graph or a stable product.

## 2. Why direct equality is the wrong join

The 64 raw moving-occurrence carriers are first-event grazing faces.  The
frozen exhaustive audit compares them with all 24 C24 cores:

```text
core/occurrence pairs                         1536
different collision-section component         768
different strict first target                  656
same target, |p|=1 versus core |p|<3/10        112
intersections                                    0
```

The stronger atom audit has `4216*64=269824` pairs and again zero
intersections.  Therefore the selected 176-atom root has `176*64=11264`
raw occurrence pairs and zero intersections.  Restricting `m_occ` to a
fixed-`j` owner law cannot create source points in a disjoint core interior.

Consequently the two roots cannot be joined by recordwise equality of their
source points, and the Round-68 twelve-field direct-equality target is rejected
for these two carrier types.  This is not a failure of measurability; it is a
typed support obstruction.

## 3. Correct incidence target

The right global object has at least two node sorts:

```text
path-cell:  (component_id, return depth, path key, owner atom)
face:       (component_id, time_j, carrier seed/family, connected rank)
trace:      face key plus side label
```

An edge says that the face is a boundary/pullback carrier incident to the path
cell.  It does not say the face point equals an interior path point.  At strict
R1-inner depth, the moving-occurrence incidence is certified empty and the
local F10/F13 sums are genuinely zero.  For arbitrary `R_n`, the grammar is
frozen but instantiated moving-occurrence pullback component IDs and connected
ranks remain zero.  That is now the first missing common-root object.

## 4. Gate 1/3

The 176-atom root provides actual restriction IDs, return components, owner
atoms, word cells, source coordinates and time-one landings.  It does not
export the Gate-1 `Q,E,u,v` representative data under those keys, and it has no
actual stable-plaque side.  The all-cell material radius, uniform Piola
remainder, two-sided physical trace/current and stopped `MT_DQ` bounds remain
absent.  Gate 1 and Gate 3 stay `NOT_CERTIFIED`.

## 5. Gate 2/4

The base root promotes the one-step physical graph from one illustrative tile
to 176 owned atoms on 16 reciprocal core edges.  This sharpens Gate-4 field 4
to an actual base-parameter depth-one graph, but not to the required all-depth
measurable commuting-square family.  No invariant stable plaque, stable
holonomy, product quotient, marker saturation, path budget, or strong recipient
is obtained.  Gate 2 remains `0/17`; Gate 4 remains `1/7`, with fields 1, 4 and
7 partial.

## 6. Gate 5

Because the Round-27 local statement holds on every one of the 4,216 strict
R1-inner atoms, all 176 base-owned atoms inherit the candidate-local fields
F1--F13.  In particular they carry 176 empty F10 slots and 176 empty F13
current/trace slots on the same actual base root.  This is a concrete
same-root local packet of maturity `13/18`, not a global operator block.

F14--F18, nonempty limiting-boundary faces, arbitrary-time occurrence
pullbacks, the conditional terminal kernel, and all seven missing positive
potentials remain open.  Global Gate-5 maturity stays `10/18` with zero
complete blocks.

## 7. Latest technology boundary

The arXiv API was checked directly on 2026-07-21 for moving-scatterer linear
response, dispersing-billiard stable holonomy, time-dependent-billiard transfer
operators, and sequential dispersing billiards.  The first query returned only
an unrelated quantum-pumping paper; the next two returned zero results.  The
sequential query returned `arXiv:2502.07765v2` and `arXiv:2104.06947v3`, which
do not build the required path-cell/face incidence registry or moving-boundary
operator estimates.  No external theorem is promoted.

## Shortest remaining route

Materialize one nonempty time-qualified pullback component of a frozen physical
carrier on an actual `R_n/Q_n` path component, assign its canonical connected
rank and two side traces, and prove the incidence map to the path cell.  Once
that typed edge exists, attach owner/current data to the face node and
stable/material/operator data to the path node.  Direct interior/face equality
must not be attempted again.
