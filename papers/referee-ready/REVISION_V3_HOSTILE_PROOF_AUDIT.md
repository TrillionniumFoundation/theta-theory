# Hostile proof audit — referee revision v3

**Date:** 2026-08-28  
**Scope:** the five controlling referee manuscripts  
**Rule:** a blocker is marked repaired only when the revised statement has a
specified object, topology, and proof route.  Deleting a claim does not count
as a positive repair.

## H1. Regular fixed-point count in the moving-cut family

**Finding.**  The first draft counted the fixed point at the common circle cut
as a regular interior fixed point.

**Repair.**  The controlling Paper I uses only branches two and three.  Their
fixed points are interior, their width ranges are

\[
[3/20,1/4]
\quad\hbox{and}\quad
[11/40,13/40],
\]

and hence their multiplier ranges are disjoint.  Equality of the second branch
multiplier forces equality of the parameter.

**Status:** repaired in `paper-I-bilateral-response/main-submission.tex`.

## H2. Regularity level for order-N finite differences

**Finding.**  An order-`N` finite-DQ proof needs the `(N+1)`st parameter
letter, which on an output level `W^{1,1}` requires `W^{N+2,1}` input.

**Repair.**  The controlling Paper I uses the ladder

```text
W^{N+2,1} -> W^{N+1,1} -> ... -> W^{1,1}.
```

For `U3`, the fifth level controls the fourth-order Taylor remainder.

**Status:** repaired.

## H3. Future insertion after physical assembly

**Finding.**  An assembled current estimate is insufficient if the output does
not lie in an invariant space on which a later source letter acts.

**Repair.**  For the moving-cut platform,

\[
\partial_a^kL_a:W^{r+k,1}\to W^{r,1},
\]

and every centered reduced resolvent preserves each `W^{r,1}` level.  Every
Kato word is therefore a bounded graded composition.  No assembly reset or
unnamed trace extension is used.

**Status:** repaired.

## H4. The probabilistic model was formerly external to the response model

**Finding.**  Replacing a deterministic fast system by an unrelated Bernoulli
process does not prove deterministic homogenization.

**Repair.**  The exact predictable innovation theorem proves directly that the
branch symbols of the nonautonomous moving-cut map are conditionally
independent with probabilities equal to the current branch widths.  The
martingale array in Paper III is therefore endogenous to the Paper-I map.

**Status:** repaired.

## H5. High-frequency strip near the imaginary axis

**Finding.**  A fixed-table high-frequency theorem and compactness do not imply
family derivatives.  Moreover a phrase such as “small complex strip” must
specify which side of the Laplace axis is controlled.

**Repair.**  Paper II proves a direct block decomposition of the branchwise
roof-twisted operator.  On the imaginary axis a Diophantine roof vector gives

\[
1-|\lambda_a(b)|\ge c(1+|b|)^{-2\nu}.
\]

The quotient by constants contracts by `9/20`.  Repeated inverse
differentiation gives explicit polynomial derivative bounds.  The controlling
statement extends to the Laplace half-strip

\[
0\le\operatorname{Re}z\le\sigma_0,
\]

not to an unjustified symmetric strip.  For `Re z>0`, normalize the positive
weights `w_i e^{-Re(z) tau_i}`; their lower ratios remain uniform on the bounded
strip, so the same phase-variance argument applies, while total mass below one
only improves separation.

**Status:** repaired.

## H6. Triangular Lorentz geometry

**Finding.**  The earlier radius interval conflicted with nearest-neighbour
nonoverlap.

**Repair.**  The controlling theorem uses

\[
\sqrt3/4<r<1/2.
\]

The upper bound is nonoverlap.  The maximal row spacing of the triangular
lattice is `sqrt(3)/2`; the lower bound closes every rational corridor.
Irrational lines are dense modulo the lattice.  A contained-disk/containing-disk
margin gives an explicit open `C^2` deformation class.

**Status:** repaired.

## H7. Symmetry and positivity of the physical covariance

**Finding.**  A one-sided correlation series is not manifestly symmetric or
positive.

**Repair.**  Paper II defines the symmetrized Green--Kubo series and proves its
equality to a pressure Hessian, a partial-sum variance limit, and the Gordin
martingale bracket.  Symmetry and positive semidefiniteness follow from these
identities.  The antisymmetric iterated-correlation tensor is kept as a
separate area anomaly.

**Status:** repaired.

## H8. Geometric rough lift

**Finding.**  The off-diagonal iterated sum alone is not the canonical
polygonal geometric second level.

**Repair.**  Paper III defines

\[
\mathbb W^\varepsilon
=\varepsilon^2\sum_{i<j}M_i\otimes M_j
 +\frac{\varepsilon^2}{2}\sum_iM_i\otimes M_i.
\]

Its symmetric part is exactly one half of the first-level tensor square.
Only the antisymmetric part needs a separate predictable compensator.

**Status:** repaired.

## H9. Pointwise viscosity closure

**Finding.**  A residual identity paired with anisotropic densities does not
produce a pointwise viscosity inequality.

**Repair.**  Paper III defines a pointwise finite-branch entropic recursion.
Monotonicity, stability, and a locally uniform Taylor expansion give the
half-relaxed viscosity inequalities directly.  The exact Cole--Hopf transform
gives global comparison and Feynman--Kac.

**Status:** repaired.

## H10. Pure controls on constrained sets

**Finding.**  On a closed convex control set, the pure saddle need not be an
unconstrained zero of the saddle gradient.

**Repair.**  Paper IV formulates the problem as the strongly monotone
variational inequality

\[
\langle G_z(w_*),w-w_*\rangle\ge0,
\qquad w\in U\times V.
\]

Strong concavity--convexity converts its unique solution into the global pure
saddle.  The state/jet selector is Lipschitz by comparing the two variational
inequalities.

**Status:** repaired.

## H11. Noncompact filtering was previously degenerate

**Finding.**  Exact one-step prior erasure does not test weighted filter
stability.

**Repair.**  The hidden process is now a Gaussian refresh--autoregression.  It
has strict total-variation prediction contraction, a quadratic Lyapunov drift,
a bounded nonconstant observation likelihood, an invariant posterior moment
ball, and a strict observation-gap contraction after finitely many prediction
steps.

**Status:** repaired.

## H12. Game nonconvexity and pure Isaacs were previously separate

**Finding.**  Writing a nonconvex polynomial in the cotangent variable does not
show that a physical game produces it.

**Repair.**  The curvature-compensation theorem adds actual quadratic actuator
energies to a general `C^2` mechanical payoff.  In the explicit energy game the
unique pure controls are

\[
u_*=p/\mu,
\qquad v_*=-p/\nu,
\]

and the resulting Hamiltonian is

\[
H(p)=\tfrac12(\mu^{-1}-\nu^{-1})p^2.
\]

It is concave when `mu>nu`.  Lower and upper recursions have this same
Hamiltonian and converge to the same Isaacs value.  Completion of squares
verifies the continuous-time feedback saddle.

**Status:** repaired.

## H13. Terminal differentiability

**Finding.**  The old representation draft assumed the expansion of the
terminal solution map.

**Repair.**  Paper V proves a parabolic-Hölder implicit-function theorem.  On
the actual entropic branch the terminal map is globally real analytic, with
first derivative equal to tilted expectation and second derivative equal to
tilted covariance.

**Status:** repaired.

## H14. Girsanov and the `Z` variable

**Finding.**  Algebraically rewriting a drift is not a Girsanov theorem, and
`Z=sigma^T Du` cannot be inverted without a separate theorem.

**Repair.**  Paper V constructs the density process

\[
\mathcal Z_s=
\exp\{\vartheta u(s,X_s)-\vartheta u(t,x)\},
\]

proves by Itô calculus that it is the stochastic exponential of
`vartheta sigma^T Du`, imposes a Novikov condition, defines the
Radon--Nikodym derivative, and obtains the shifted Brownian motion and changed
drift.  The BSDE integrand remains `Z=sigma^T Du`; no inversion is attempted.

**Status:** repaired.

## H15. Path and second-order actualization

**Finding.**  An envelope of solved equations is not a DPP or 2BSDE.

**Repair.**  The entropic path branch is defined by conditional exponential
expectation and has a quadratic BSDE.  The pure path game is verified by
functional Itô calculus and completed squares.  The volatility branch starts
from an explicit stable family of controlled laws, proves conditioning/pasting
stability, invokes the established path-viscosity comparison theorem, and then
uses the standard aggregation/minimality theorem for its nondominated 2BSDE.

**Status:** repaired.

## Audit verdict

```yaml
hostile_findings: 15
hostile_findings_repaired_in_controlling_files: 15
positive_actual_platforms:
  moving_cut_response_and_innovations: true
  Diophantine_high_frequency_suspension: true
  nonautonomous_rough_and_entropic_HJB: true
  noncompact_filter_and_pure_game: true
  tangent_Girsanov_BSDE_PPDE_2BSDE: true
known_internal_proof_blockers_after_this_audit: 0
second_external_referee_review: NOT_YET_PERFORMED
```

The last field remains essential: this is an internal hostile audit of the
revision, not an external acceptance or correctness certificate.
