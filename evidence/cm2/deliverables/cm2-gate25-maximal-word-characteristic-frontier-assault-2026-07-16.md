# CM2 Gates 2/5: seeded maximal-word and characteristic-Z assault

Date: 2026-07-16 (Asia/Shanghai)  
Frozen inputs: the fourteenth-round 24-core, roof-two chart, universal
operator, componentwise Growth, invariant-family, selected-loop/coding and
Gate-2 frontier stacks were read only  
Strict verdict: **a 24-row positive seeded implicit maximal-component
registry and a finite characteristic-`Z` theorem on the rational inner
cores are certified; full-key characteristic restriction, the stable
quotient, complete 18-field blocks, Gate 2 and Gate 5 remain
`NOT_CERTIFIED`**

## 1. A genuine, but implicit, maximal-component registry

For each of the 24 already certified positive physical return cores and every
fixed `|s|<=1/400`, define `M_i(s)` to be the connected component containing
that core of

```text
exact word domain D_w(s)
 intersect fixed source normal chart
 intersect fixed target open-semicircle chart
 intersect all declared intermediate oriented transparent-wall charts
 intersect {|p_source|<3/10, |p_target|<3/10}.
```

This is not an arbitrary compact subrectangle.  It is, by definition, the
maximal connected component of the displayed exact physical
word/chart/central-homogeneity predicate.  The frozen core prism lies inside
that predicate for every parameter fibre, so every `M_i(s)` is nonempty and
the 24 components belong to 24 distinct candidate keys.  Their union has the
same strict collision-SRB mass lower bound

```text
mu_collision(union_i M_i) > 147/550000.
```

Each row has an immutable ID obtained from the word key, rational seed,
source/target/intermediate chart labels, central homogeneity label and the
boundary-predicate digest.  The registry contains 20 roof-one and four
roof-two rows.

The word “implicit” is essential.  The component is selected by its exact
predicate and positive seed, not by a claimed numerical endpoint table.

## 2. Frozen boundary-predicate universe

Every possible boundary of a seeded component is placed in a finite
over-ledger.  For a source `G` chart the exact first-hit candidate list has
57 targets, and for a source `W` chart it has 55.  The owner ledger contains,
for each candidate, its discriminant, forward-root and horizon equalities,
plus every selected/competitor root tie.  This gives respectively

```text
4*57-1 = 227,       4*55-1 = 219
```

owner predicates.

The transparent-wall ledger uses the exhaustive integer range `[-5,5]`.
The target-lift universe is `[-4,4]^2`, all disk radii are below one and the
source lies in the central lift, so no relevant endpoint leaves this range.
It registers

```text
44 endpoint-on-wall predicates
+121 vertical/horizontal wall-time ties
+  2 coordinate-velocity zeros
=167 word predicates.
```

After adding two source-chart seams, two target-chart seams and four
source/target central-homogeneity faces, the over-ledger has

```text
402 predicates on each of the 12 G-source rows,
394 predicates on each of the 12 W-source rows.
```

This freezes the complete boundary *family*.  It does not root-isolate the
predicates on an arbitrary moving standard curve.  Consequently neither the
order of boundary crossings nor the full maximal-component multiplicity is
yet certified.

## 3. Exact characteristic restriction on the positive inner cores

The smaller rational cores admit a stronger theorem.  In every one of the
eight source charts their three `t` bands are exactly

```text
[-7/10,-69/100], [1/100,1/50], [69/100,7/10].
```

The least gap is `67/100`.  Since

```text
dr/dt = R/sqrt(1-t^2) >= R >= 4/25,
```

the source-`r` gap between distinct bands is at least

```text
67/625 > delta_1 = 1/37724355673552103994.
```

A canonical curve may cross a normal-chart seam, so the preceding
within-chart computation is not used as a global shortcut.  The certificate
also orders all 12 physical normal arcs on each of the two source collision
components, including every cross-chart adjacent pair.  All 24 cyclic gaps
have angular size strictly greater than `1/100`; since the smaller obstacle
radius is `4/25`, the global physical source-`r` gap is strictly greater than

```text
(4/25)*(1/100) = 1/625 > delta_1.
```

Thus the multiplicity conclusion remains valid even for a short curve that
crosses a chart seam; it is a statement on the physical collision component,
not merely on one coordinate copy.

On either oriented standard-curve chart, `t` is monotone in boundary
arclength and `p` is strictly monotone along the graph.  The inverse image of
a `t` interval and a `p` interval is therefore an interval.  A canonical
short curve can meet at most one of the 24 core rectangles.  Hence

```text
characteristic component multiplicity <= 1,
new artificial endpoints per nonempty intersection <= 2.
```

Let one parent curve have weight `q`, length `L` and conditional density
`rho`, and let `I` be its sole retained core interval.  The frozen invariant
density cone gives `sup rho/inf rho <= 2000/1999`, so the unnormalised retained
weight satisfies

```text
q_I/|I| <= (2000/1999) q/L.
```

Thus

```text
Z_*(1_core F) <= (2000/1999) Z_*(F).                 (3.1)
```

Restriction to an interval preserves the log-Hölder seminorm.  Paying (3.1)
before the already certified physical step gives the still contracting
coefficient

```text
(2000/1999)*(360134800/360493663)
 =720269600000/720626832337
 =1-357232337/720626832337 <1.                       (3.2)
```

Equations (3.1)--(3.2) are unnormalised source estimates.  Conditioning on a
retained mass that tends to zero near a core corner can still make normalized
shape cost arbitrarily large; no such uniform conditional claim is made.

## 4. Exact 18-field status

The new result must not be misread as a full-key operator registry.

| Layer | Exact status |
|---|---|
| full key `nonempty_or_empty_domain_proof` | completed as `NONEMPTY` on at least 24 keys |
| positive seeded maximal component ID | materialized implicitly on 24 keys |
| core-local fields 5--6 templates | certified |
| core-local field-7 characteristic/Growth seed | certified by (3.1)--(3.2) |
| core-local fields 14--15 unnormalised regular-density/standard-family seeds | certified |
| full-key field 7 | **not certified** |
| full-key fields 14--17 | **not certified** |
| complete 18-field block count | `0` |

The full maximal components may meet their word/owner/chart boundaries more
than once.  Until every frozen predicate is root-isolated and ordered on
every canonical short standard curve, the pre-restriction
`Xi<900337/901685` cannot be copied into a full-key field.  Flux-face and
dynamic-test fields additionally require the still missing complete
current/DQ/`MT_DQ` stack.

## 5. Selected loop and the Gate-2 endpoint packet

The selected physical QNL occurrence still supplies a common-fiber loop
matrix and four nonzero wedges, and the clean horseshoe now has a finite
faithful SFT coding.  Neither a horseshoe symbol nor a collision word is an
onto inverse branch of the required stable quotient.

No certificate presently binds the selected occurrence to one of the 24
maximal word components, and none constructs

```text
stable-saturated product base,
stable projection pi^s,
quotient density rho,
onto inverse-branch label a and reverse weight p_a,
same-carrier endpoint maps X_a,Y_a,
pointwise endpoint-slope identity or denominator lower bound.
```

Therefore Gate-2 fields 9--12 remain false.  The old two-dimensional
key-refined reverse conditional remains Dirac; the new component registry
does not create PPE.

## 6. Exact remaining boundary

```text
24 POSITIVE SEEDED MAXIMAL WORD COMPONENTS:          CERTIFIED_IMPLICIT
24 INNER-CORE CHARACTERISTIC MULTIPLICITY/Z:         CERTIFIED

MAXIMAL-COMPONENT BOUNDARY ROOT ORDER/MULTIPLICITY:  NOT CERTIFIED
FULL-KEY CHARACTERISTIC BOUNDARY Z:                  NOT CERTIFIED
FULL-KEY FIELDS 7 AND 14--17:                        NOT CERTIFIED
COMPLETE 18-FIELD OPERATOR BLOCK COUNT:              0
STABLE QUOTIENT / rho / p_a / ENDPOINT PACKET:       NOT CERTIFIED
GATE 2:                                               NOT CERTIFIED
GATE 5:                                               NOT CERTIFIED
```

The next executable Gate-5 step is to intersect the frozen 394/402-predicate
ledgers with canonical short curves, isolate and order every root, then sum
the actual word-boundary components.  In parallel Gate 2 still needs an
interval-indexed stable-saturated physical base and its same-carrier endpoint
maps.

## 7. Reproduction

```bash
PY=/tmp/cm2-flint-venv/bin/python

PYTHONPATH=deliverables $PY -m py_compile \
  deliverables/cm2_gate25_maximal_word_characteristic_frontier_cert.py \
  deliverables/cm2_gate25_maximal_word_characteristic_frontier_verifier.py

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_maximal_word_characteristic_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_maximal_word_characteristic_frontier_verifier.py \
  --self-test

# Expected exit 2: Gates 2 and 5 remain fail-closed.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_maximal_word_characteristic_frontier_verifier.py
```
