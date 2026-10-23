# Independent author derivation of native339

This note concerns the existing physical A2-DYN source after native337.
It is a coauthor calculation and proof check, not an independent referee
report or a claim of journal acceptance.  Parent integration controls the
active manuscript, retained history, commit and remote publication.

## New conclusion and exact source

For the original triangular Lorentz gas, unit physical speed, radii
`[9/20,47/100]`, original five-rectangle section, and all genuine collision
words with both endpoints in the original cap, the regular roof
restriction to any original endpoint horizontal side is strictly convex
for every collision count `m >= 114`.  Original endpoint vertical sides
have strictly convex restrictions at every `m >= 1`.  Consequently the
regular endpoint section side stratum contributes no constant-roof atom
to the exact derivative of native336 for `m >= 114`.

Before that threshold, the sum of the absolute signed contributions after
exact `(label, physical roof)` grouping is bounded by

`4 N_h A_V F_cs C_mom atan(kappa_es sigma^(m-1))`, `N_h = 20`.

The factor 4 consists of the two-sided angular integral and two physical
collar orientations. The latter is a conservative general trace
allowance. The subsequently proved native341 transversality excludes an
open section/unvisited coincidence in the actual model; native339 does
not need that later absence theorem for its safe bound. The original
regular root kernel is not evaluated at a singular collision. The theorem instead
passes actual roots on `p0=b+h` or `p0=b-h` to the designated positive-
visited word traces.  All sums retain exact records and physical times.

## Main calculation

Write the true reduced action Hessian as `G=[[a,e],[e,d]]`, and use the
actual initial horizontal section side `p0=b`.  Since `F_0=-Rb`, the
implicit function `q0=x(q1)` satisfies `x'=-e/a`.  Thus

`S'=R(pm+b e/a)` and `S''=d-e^2/a+Rb (e/a)'`.

The extra last term has positive displayed sign because
`F_0=-Rb` and `x''=-(e/a)'`.  Uniform positive definiteness of `G` alone
does not control it.  For example, the nonphysical diagnostic
`F(x,y)=(x+y^2)^2/2` has a positive definite Hessian on `F_x=b>0`, yet its
restriction there is exactly constant.  This example is only an algebraic
check against an invalid proof shortcut; it is not substituted for the
billiard action.

The decisive existing physical inputs are:

- native260: `|e|=R omega`, the optical bound on `omega`, the original
  endpoint cap, and `omega I_m <= 500 sigma^(m-2)_+`;
- native288: every entry of `D G[eta]` is bounded by
  `C_F ||eta||_infinity`, uniformly in count and visited grazing approach;
- native289: `|D log omega[eta]| <= C_omega I_m ||eta||_infinity`.

Because the signed cofactor `e` is nonzero and has constant sign on a
regular word, these give the genuinely stronger estimate
`|D e[eta]| <= 500 R_plus C_omega sigma^(m-2)_+ ||eta||_infinity`.
The quotient derivative in the extra curvature term therefore decays
exponentially, whereas the Schur term `d-e^2/a` stays at least
`lambda_circle`.  The exact rational certificate gives threshold 114.

For a constant-roof arc, the first derivative identity directly forces
`|pm| <= kappa_es |b| sigma^(m-1)`.  This is a statement about the actual
physical source, not a newly imposed condition.  Native284's endpoint
root kernel then pays the charge inside this forced momentum band.  The
original conditional factor `1/c_*` occurs once, already in `F_cs`.

## Boundary, measure and label checks

The endpoint action extends smoothly on the designated word at a boundary
with strictly positive visited incidences, even if an unvisited disk is
tangent.  The estimates are limits from that word's physical side.  A
visited tangency has its separately retained zero coarea trace and is not
made regular by this extension.

The canonical endpoint map `(q0,q1)->(p0,pm)` has absolute Jacobian
`det(G)/R^2`.  On finite semialgebraic open physical sheets, a boundary arc
lying in `p0=b` admits a left or right collar except at finitely many arc
nodes.  A finite collection of traces with the same collar orientation
can be approximated at common `b +/- h` and common terminal momentum;
native284 applies there to actual regular roots.  One orientation costs
`C_mom`; both cost `2 C_mom`.  Passing finite positive sums precedes the
supremum over their collections.  This closes the trace gap in a direct
application of a regular-root formula to an arbitrary physical side.

The exact record vector changes from zero outside an endpoint section
test to at most one exact label inside.  Its label-sum jump is at most
one.  Coincident real constraints form one physical interface; assign it
once, then combine signed terms at the same label and physical roof.
The twenty horizontal side occurrences bound the sum without a word or
component count.  A level `b=0` has constant regular polar angle and zero
regular angular charge; a critical point at `(p0,pm)=(0,0)` is a separate
incoming sector and remains in the proof ledger.

## Novelty control against retained history

The one-sided Tauberian argument for positive density already exists in
historical v77 (`7b291428cf38455404fae326651a986b1697cf97.tex` in the retained
660-object archive).  Its persistence and forward angular-loss statements
must not be repackaged as new.  Native262 already pays interior positive
variation using the inherited normalized averaged `v0` input.
Native324 already establishes a uniform full regular endpoint angular
charge; native336 identifies constant-roof side atoms; native337 gives
their exact high-frequency jump spectrum.  None of those statements
contains the forced exponentially narrow opposite-endpoint momentum
band or the mixed-derivative curvature argument above.  Searches of the
retained source objects found no earlier physical endpoint-isoroof
payment.  This is a source-census observation, not a claim of exhaustive
priority across external mathematics.

## Remaining mathematical scope

The result does not pay the nonconstant endpoint boundary density,
interior section side atoms, unvisited sides away from endpoint section
sides, or positive-visited critical germs strictly inside the section.
It does not prove the original normalized raw pointwise LLT.  It is a
proved elimination of one actual atomic stratum and an explicit uniform
payment of that stratum at all counts, while retaining all previous
proof bodies and the original target.

The included `verify_endpoint_isoroof.py` performs exact arithmetic and
independent local cubic-action chain-rule checks.  It does not validate
continuous geometry, source abundance, external dynamical inputs, or the
full local limit theorem by finite samples.  The written proof supplies
the first two new assertions conditional only on the explicitly cited
retained native lemmas; the broader paper's inherited analytic inputs
remain identified as such in the parent ledger.
