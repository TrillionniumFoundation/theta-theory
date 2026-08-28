# Paper 1 blueprint v1

Working title:

> **Moving Singularities in Billiard Transfer Operators: Current Calculus and
> a Two-Disk Fixed-Section Model**

Target after the global event inventory is closed:

> **First Variation of a Fixed-Section Dispersing Billiard with a Translating
> Scatterer**

## Scope

This paper treats finite-time, one-return first variation caused by moving
singularities.  It deliberately excludes CM2, PPE, recovery/source trees,
long-time susceptibility, and transfer from the fixed section to the standard
full-boundary collision map.

## Main theorem hierarchy

### Theorem A — finite regular-radical current calculus

For finitely many parameter-dependent branches whose switching functions are
submersions and whose singular dependence is smooth in radical variables,
the transfer-operator difference quotient converges in `(C^{1,alpha})*`.
The limit is the sum of regular transport currents and explicit switching-face
currents.  The coefficient measures converge in total variation on a common
occurrence atlas.

### Theorem B — trace gluing at circular switches

When the direct and hit branches have the same physical trace, their apparent
face atoms cancel with orientation retained.  The remaining current has an
integrable inverse-square-root envelope and `O(rho^{1/2})` collar mass.

### Theorem C — finite analytic contact

Distinct regular analytic event germs, including finite-order tangential
contacts, have an integrable double-radical envelope with local mass
`O(rho(1+log rho^{-1}))`.  Determinant lower bounds are unnecessary once the
actual first-variation coefficient is dominated by this envelope and all
remaining factors are uniformly bounded.

### Pilot theorem — two possible versions

**Version now available.**  For the rational fixed-section two-disk model:

- common section, common invariant law, reversibility, and the exact one-return
  block identity are explicit;
- a positive-mass compact clean cylinder has analytic uniformly non-grazing
  entry/exit first variation;
- regular circular tangency charts and all verified distinct regular
  two-event contacts satisfy Theorems A–C;
- the remaining global problem is a finite algebraic event inventory.

This version must not be advertised as global first variation for the entire
map.

**Target version after the inventory.**  On a nonempty open neighbourhood of
the rational model, for every fixed `h in C^{1+alpha}` there is an order-one
current `Kh` such that

```text
((P_s-P_0)/s)h -> Kh in (C^{1,alpha})*,
sup_s ||((P_s-P_0)/s)h|| <= C ||h||_{C^{1+alpha}}.
```

The theorem should claim strong convergence for each fixed source and a
uniform operator bound, not operator-norm convergence unless that stronger
statement is separately proved.  Common invariance gives `K1=0`.

## Required global inventory theorem

The final pilot theorem is conditional on a finite, frozen table proving:

1. full common-chart coverage of every one-return physical branch;
2. a square-free event list and uniform submersion margins;
3. exhaustive common-factor classification and trace cancellation;
4. no unresolved triple or higher uncancelled radical incidence;
5. treatment of corners, lift changes, return targets, and grazing strata;
6. uniform continuation for a nonempty parameter neighbourhood.

The proof should build the atlas directly for the complete one-return map.
This avoids making global test-side strong continuity of an intermediate block
an additional gate.

## Proposed 44–48 page structure

1. Introduction and exact scope — 4 pages
2. Fixed-section model and main results — 5 pages
3. Common-atlas current calculus — 5 pages
4. Radical faces and circular trace gluing — 7 pages
5. Multiple analytic events — 5 pages
6. Complete event inventory — 8 pages
7. Global assembly and `K1=0` — 4 pages
8. Positive core and block interpretation — 3 pages
9. Exact-arithmetic/reproducibility appendix — 3–5 pages

Long obstruction catalogues, CM2 interfaces, PPE, source clocks, and research
programmes belong in companion material, not this paper.

## Submission ladder

- Without the complete inventory: a general/local current-calculus paper can
  be written, but the pilot is only a regular-subatlas application; target a
  strong specialist journal.
- With a complete inventory for one rational example: a strong specialist/CMP
  level submission becomes plausible.
- With strict margins yielding a nonempty open class and a reusable finite-atlas
  theorem: the paper becomes a credible top-field candidate.

## Stop conditions

Pause the global theorem if the inventory finds any of the following without a
new local normal form:

- a genuine coincident event factor with unequal traces;
- an individual critical germ whose quotient is not uniformly integrable;
- an unresolved three-or-more radical product;
- loss of parameter continuation or target transversality.

These cannot be bypassed by saying the exceptional set has zero measure.
