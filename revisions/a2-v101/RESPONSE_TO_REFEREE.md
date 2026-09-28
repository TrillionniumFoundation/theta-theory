# A2 revision 101: response to the v100 referee

Controlling review: `c05195ef73bd3c5c8185928920926baf2d38df2c`,
`reviews/a2-v100-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`.
Reviewed paper: `7407ad098cac70ac07bb7d9d01f562890041cada`.
This revision starts from the review commit and leaves the historical mathematics unchanged.

The revision makes finite whole-model spectral calibration its main structural theorem.
It does not claim that polarization, real curve selection, tropicalization, resolution,
or the existence of a Puiseux expansion is new. The substantive claim is that a
finite set of actual feasible calibration experiments, with every stochastic nuisance
parameter free, determines the complete leading spectral fibre on every full-rank
coprime binary multiplicity/boundary pattern, with a quantitative stability theorem.
The second geometric addition identifies a remote entrance with a residual/time
contact pair, including its real accessible divisors and its norm-dependent units.

## R100.1: theorem-level real/positive tropical comparison

`article/v101/real_residue.tex`, Theorem `thm:v101-residue`, proves an exact
Puiseux-residue formula. Its full-support part maps to the fixed-weight coordinate
signed-valuation fibre. It distinguishes this coordinate projection from the full
inverse-limit real analytification of Jell–Scheiderer–Yu; we do not assert that the
latter loses the same information. Positive degeneration parameter is separated
from positive coordinate orthant. The actual observation-unit section and spectral
decoder are identified as the additional data. Proposition `prop:v101-lift` gives
a sufficient nonsingular real lifting test and states where it does not apply.
The bibliography now includes the specified Jell–Scheiderer–Yu and Rose–Telek
papers, with publisher-verified metadata.

Theorem `thm:v101-filtered` derives the conjugate limits from finite weighted-jet
conditions on a Nash isomorphism and its inverse. It proves compatibility with
composition, residue and positive ramification. It does not assume the desired
convergence as a hypothesis. Metric invariance requires transported metric data.

## R100.2 and R100.3: finite scalar information, not a distance function

`article/v101/finite_metric.tex`, Theorem `thm:v101-finite`, replaces generic
quadratic distance-function reconstruction as the headline. The retained coordinates
are explicitly the repeated-interior centred variances and signed endpoint sums in
the square-root regime, or the cluster sums in the linear regime. All other root
variables, weights and both channels are optimized over, not frozen.

The proof shows that the constrained minima in the actual experiment converge to
the quotient Fisher form, uniformly on compact subsets of fixed patterns. The
finite costs `c(e_i)` and `c(e_i+e_j)` determine that form. The real-root decoder
then determines all simultaneous leading roots and their metric, including the
endpoint profiling constraints. At degree d, no more than d(2d+1) scalar costs are
needed. Corollary `cor:v101-stability` gives radial inclusions, a Hausdorff bound and
a measurement-error-to-matrix-error bound. The datum is marked and sufficient;
we do not assert a false converse after endpoint projection or a minimality claim.

The previous separation and distance-function results remain in the paper.
The finite arithmetic check uses the actual degree-two binary model with two
double roots, five exterior clocks, and a full nine-dimensional score. It verifies
three-probe reconstruction of the two-dimensional quotient exactly and evaluates
fully feasible recovery curves. Those finite checks are not advertised as proofs
of the general theorem or as finite-t global minimization certificates.

## R100.4: entrance orders as singularity geometry

`article/v101/divisorial_contact.tex`, Theorem `thm:v101-divisorial`, identifies the
nonzero entrance order of an isolated Nash remote germ as the maximum ratio of
residual-ideal order to time-ideal order on accessible real divisors. It also proves
an intrinsic real-arc characterization and identifies the leading coefficient as
the reciprocal maximum of a continuously extended metric-unit ratio on the resolved
zero-time set. The proof includes the compact fixed-time minimum argument.

Feasibility inequalities are rectilinearized along with the residual/time pair;
complex exceptional divisors with no accessible real sector are not used. The
integral-closure corollary explains which part is an ideal invariant and why the
leading coefficient requires the norm. The existing n/m realization is rederived
by its explicit contact chart and unit, and the regular cubic walls are related to
the (1,1) contact. The exact critical-shell test and second correction remain
separate: equal leading terms do not decide membership.

The structural statement is proved for Nash residual/path germs (and specified
positive ramifications). The existing broader continuous-semialgebraic entrance
and uniform-family theorem remains intact. We do not claim a classification of
all source singularities, or that every rational exponent occurs in the cubic family.

## R100.5 and R100.6: format and finite diagrams

Definition `def:v101-format` lists parameter, source and auxiliary dimensions,
observation and target dimensions, polynomial count and degree, and Boolean and
quantifier syntax length for the actual finite presentation, including the path
and any threshold. Algebraic coefficient representations are specified separately.
Proposition `prop:v101-format` obtains a computable numerator/denominator bound
from the eliminated minimum graph's polynomial degrees.

The common monomialization convention is explicitly finite-family-dependent.
The all-arcs/all-polynomials order comparison is pointwise for each polynomial;
it does not assert that one modification principalizes the infinite polynomial
ring. The infinitely many lines x-cy explain the distinction. No bit-complexity
claim or new practical resolution algorithm is introduced.

## R100.7: general/concrete dependency

The principal article now begins with the direct model inverse, multiplicity law,
finite calibration, exact cubic fibre and two walls. Its dependency appendix states
that these proofs do not require the relative resolution atlas. The general atlas
is used for its own uniform weighted conclusions beyond the explicit normal forms;
the divisorial theorem uses the finite residual/time principalization. We do not
retroactively describe the atlas as essential to a direct pencil calculation.

## R100.8: source-bound validation and current entry

`CURRENT_REVIEW_ENTRY.md` identifies the authoritative entrypoint on this new
branch without deleting the old README. The existing recursive v100 builder is
reused by `scripts/build_a2_v101.py`; the new wrapper records the exact source
hashes and preserves principal/archive/complete PDFs, logs, recorder files and
auxiliary files only after successful native execution. Inline bibliography is
used, so an absent BibTeX bbl is not a missing build product.

The branch-scoped workflow checks out the triggering SHA, runs the arithmetic
check, builds the complete source/PDF dependency graph, and preserves successful
artifacts on this revision branch with source-commit provenance. A receipt-only
commit is not mislabelled as the commit whose own hash was compiled. The
workflow refuses to overwrite a branch which advanced meanwhile.

At the initial source submission, the finite exact diagnostic has been executed
locally. Full principal/archive/complete native success is **not claimed** without
an actual `native/RUNTIME_RECEIPT.json` and matching outputs. A pending workflow
is not closure of this request. The local validation record states its exact scope.

## R100.9 and editorial preservation

No existing theorem or historical source is deleted or replaced. Every mathematical
module in the v100 principal remains included in v101, and the complete v100 volume
is also the new archive. New material consists of the finite calibration proof,
real-residue/finite-jet comparison, divisorial-contact proof, and the specifically
requested format/dependency clarification. Build logic reuses the existing recursive
builder rather than creating a new certificate framework. The title, abstract and
introduction foreground the concrete structural theorem in ordinary theorem/proof
style; claims of significance are left for independent mathematical assessment.

The response supplies mathematical arguments, not a promise of journal acceptance
or a declaration that the referee's originality judgment has been mechanically closed.
