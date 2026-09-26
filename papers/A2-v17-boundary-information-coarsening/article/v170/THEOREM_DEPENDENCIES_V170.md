# A2 v170 — proof dependencies and precise objects

## Main theorem: ramified Hilbert boundary

`thm:ramified-boundary-v170` is the central new statement. It is for every
contact order a>=2 and every pair of positive coefficient powers rho,sigma,
not a finite list of tested triples.

The proof has two routes, which meet in the same normalized surface:

```text
v169 marked all-order chain theorem
    |  flat coefficient base change and exact Newton polygon
    v
prop:ramified-rees-v170 -- all normalized Rees degrees and affine charts
    |                                  |
    v                                  v
prop:ramified-singularities-v170    lem:coordinate-ideal-v170
    |                                  |
cyclic indices, divisor classes,        v
intersection and discrepancy       entire parameter fibre:
formulas                          pure CM, multiplicities, exact nilpotence

raw complete-intersection charts of the same pulled-back graph
    |                                  |
    v                                  v
lem:binomial-conductor-v170        lem:conductor-depth-v170
    |                                  |
    +---------- global conductor ------+
                       |
              root residue maps and all normalization lifts
```

The raw chart regular sequences are written in `eq:raw-cover-charts-v170`.
The conductor-depth lemma, rather than finite generic-point calculations,
rules out an extra ideal condition only at a crossing. The coordinate-ideal
lemma gives the full scheme fibre, rather than inferring it from its cycle.

`cor:equal-power-v170` provides a direct all-chart conductor calculation by
finite semigroup representatives. `prop:log-compatibility-v170` proves the
marked principalization property, root-cover composition and gluing.
`cor:hilbert-lifts-v170` relates normalized residue characters to actual
embedded Hilbert limits and realizes every root label by an arc.
`cor:toric-fibres-v170` applies the lattice lemma to any nontrivial normal
toric surface modification of the plane, without the failure-algebra input.

## Three schemes that must not be conflated

Y is the integral retained-coefficient Hilbert graph. Its normalization Z
can have quotient singularities. The fibre F of Z over the coefficient
origin is a one-dimensional parameter scheme and can be nonreduced.
A fibre of the universal embedded curve over a point of Y or Z is a
different scheme. Its punctual nilradical from v169 is not the nilradical
of F and not the conductor of Z -> Y. The new theorem normalizes parameters;
it does not replace any universal-curve fibre by its normalization or radical.

## Inherited route and the companion

The complete v169 ideal/content, chain, monic universal-curve, genus-correction,
fixed-degree equivariance, Quot and earlier contact material are retained.
Paper I is independent reconstruction mathematics. Only the effective-family
application invokes it. No new ramified-boundary proof assumes a full-B_a
fibre classification, an arbitrary-Kronecker boundary theorem, or an external
independent audit of Paper I.

All 465 predecessor mathematical blocks and 682 master labels are locked.
Complete mathematical bodies remain in both submitted sources and exactly
once in the preservation master. New front matters replace only expository
front matters, whose exact predecessors are archived. The master is not a
third submission. Auxiliary exact checks are not proof certificates.
