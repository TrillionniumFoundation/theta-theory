# Hostile proof audit — referee revision v4

**Date:** 2026-08-29  
**Controlling branch:** `theta-referee-revision-v4-full-positive-2026-08-29`  
**Purpose:** identify the strongest internal objections to the new positive
proofs before a second external review.

This audit is not an external correctness certificate.  It records the
questions asked internally and the exact manuscript mechanism intended to
answer each question.

## 1. Paper I — response and symbolic desingularization

### Finding I.1 — Is the four-branch system merely a one-dimensional toy?

**Risk.** A full-cover interval map alone would not justify the collision
terminology or the later area-preserving dynamics.

**Repair.** The controlling paper constructs the invertible two-dimensional
extension

```text
B_a(x,y)=(T_a(x),s_{i-1}(a)+w_i(a)y),
```

whose branch derivative is `diag(w_i^{-1},w_i)`.  It preserves area, is
uniformly hyperbolic, has moving stable and unstable seams, and admits a
finite-flight mapping-torus suspension.  The one-dimensional transfer operator
is its unstable quotient, not an unrelated stochastic model.

### Finding I.2 — Could the response still be an exact-coboundary tautology?

**Risk.** Earlier examples differentiated invariance or assumed
`F=(I-L)H`.

**Repair.** The arbitrary-source theorem takes independently prescribed
centered `F_a` and dual tests `G_a`.  The proof uses the actual reduced
resolvent and normal convergence; no primitive is assumed.  The open-billiard
corollary also chooses a cylinder observable with unequal periodic sums, which
excludes cohomology to a constant.

### Finding I.3 — Does repeated differentiation leave the declared spaces?

**Risk.** A moving-face current controlled only in the weakest space cannot be
reinserted into an arbitrary Kato word.

**Repair.** The exact formula proves

```text
partial_a^k L_a : W^{r+k,1} -> W^{r,1}
```

for every `k`.  Every reduced resolvent preserves each centered level.  An
order-`N` word is therefore typed on the finite ladder from `W^{r+N,1}` to
`W^{r,1}`.  No historical-label reset occurs.

### Finding I.4 — Is nonconjugacy really proved?

**Risk.** A moving partition can be a coordinate artifact.

**Repair.** Branches two and three contain regular interior fixed points.  The
ranges of their unstable multipliers are

```text
branch 2: [4,20/3],
branch 3: [40/13,40/11].
```

They are disjoint.  A `C^1` conjugacy cannot exchange the fixed points and must
preserve their multipliers, which vary strictly with the parameter.

### Finding I.5 — Is the open-billiard coding differentiable on one fixed space?

**Risk.** Merely citing symbolic coding would not prove parameter regularity.

**Repair.** The proof uses a parameter-dependent contraction on a weighted
sequence space.  Strict convexity, obstacle separation, and no eclipse give a
uniform graph-transform contraction.  The analytic contraction theorem yields
an analytic fixed collision sequence.  Exponential dependence on distant
symbols gives the Hölder norm.  Roof, Jacobian, and physical observables are
analytic compositions of the collision sequence and boundary jets.

### Finding I.6 — Does the specular positive class still rely on an invariant
source?

**Risk.** The response could again be source-specific.

**Repair.** On the fixed symbolic space, every analytic Hölder observable is an
allowed source/test.  Ruelle spectral perturbation gives arbitrary-source
correlation response.  The changing isolated periodic flight proves
nonconjugacy independently.

## 2. Paper II — pressure, covariance, and full frequency

### Finding II.1 — Is the Green--Kubo tensor genuinely symmetric and positive?

**Risk.** An unsymmetrized one-sided correlation matrix need not be symmetric.

**Repair.** The definition is the symmetrized series.  The theorem proves it is
the pressure Hessian, the normalized partial-sum variance, and the Gordin
martingale bracket.  Positivity is the positivity of a square/bracket, not a
notation convention.

### Finding II.2 — Does the renewal formula confuse entry and exit segments?

**Risk.** Reusing one roof integral in both positions reverses orientations.

**Repair.** The paper defines `B_{G,a,z}` with
`exp(-z(tau-u))` and `ell_{F,a,z}` with `exp(-zu)`.  Decomposition by the number
of complete returns fixes their order in the resolvent product.

### Finding II.3 — Is the full-frequency theorem valid only on the imaginary
axis?

**Risk.** The scalar phase lemma is stated at `ib`, while the theorem uses a
right strip.

**Repair.** On the constant block, positive real part strictly decreases the
modulus.  If the real part exceeds a fixed multiple of the Diophantine phase
gap, `1-|lambda|` supplies the bound; below that scale, continuity from `ib`
preserves half the phase gap.  The quotient contraction is uniform throughout
the strip.  This two-case argument is part of the block inverse estimate.

### Finding II.4 — Can parameter derivatives create uncontrolled powers of
frequency?

**Risk.** Differentiating `e^{-z tau_i(a)}` introduces powers of `z`, and each
resolvent word contains several high-frequency factors.

**Repair.** An order-`N` inverse derivative is a finite sum of words with at
most `N+1` resolvents and total multiplier derivative order `N`.  The manuscript
uses the explicit safe exponent

```text
2 nu (N+1)+N.
```

It also records the exact Sobolev loss from inverse-branch derivatives.

### Finding II.5 — Is the open-billiard Dolgopyat hypothesis nonempty?

**Risk.** A temporal-shear assumption could merely rename the desired
high-frequency cancellation.

**Repair.** The paper identifies two explicit return words through two
different obstacles.  The derivative of their roof difference is the
difference of tangential projections of the corresponding flight directions.
For three noncollinear asymmetric disks it is nonzero away from a
codimension-one symmetry relation.  Compactness gives a positive cylinder
margin, and the condition persists under small analytic obstacle motion.
The remaining cone contraction is the standard Dolgopyat theorem under this
geometric shear.

### Finding II.6 — Is the triangular finite-horizon proof complete?

**Risk.** Checking only one corridor direction would be insufficient.

**Repair.** For every primitive lattice vector `v`, adjacent parallel lattice
lines are separated by `area/|v|`.  The maximum occurs for the shortest
vectors and equals `sqrt(3)/2`; hence `r>sqrt(3)/4` blocks every primitive
direction.  Compactness converts absence of an infinite corridor into a finite
maximum free flight.  `r<1/2` is the exact nearest-neighbour nonoverlap bound.

## 3. Paper III — exact innovations, rough path, and HJB

### Finding III.1 — Is the probabilistic process external to the collision map?

**Risk.** Replacing a deterministic fast map by an independent product shift
would leave the advertised microscopic chain open.

**Repair.** Exact conditional uniformity is proved inductively for the same
moving full-cover collision map.  Branch labels are innovations of that map
under its Lebesgue invariant law, even when the parameter is predictable from
the slow history.

### Finding III.2 — Is the second level geometric?

**Risk.** The iterated sum `sum_{i<j}` alone misses the within-step diagonal of
the polygonal lift.

**Repair.** The controlling definition includes

```text
(1/2) sum_i M_i tensor M_i.
```

Discrete integration by parts gives
`Sym WW = (1/2) W tensor W`, identifying the Stratonovich/geometric lift.

### Finding III.3 — Does the slow feedback break the innovation theorem?

**Risk.** `A_k=Theta(X_k^epsilon)` depends on the past branch symbols.

**Repair.** The innovation theorem is formulated for every predictable
parameter.  Since the slow state is adapted, `A_k` is known before the next
branch is chosen, and the conditional-uniform induction still applies.

### Finding III.4 — Is the covariance actual in arbitrary finite dimension?

**Risk.** Four centered branch vectors span at most three dimensions.

**Repair.** The base theorem assumes the displayed positive covariance.  The
common-platform document gives an actual construction in every finite
dimension by taking a finite Cartesian product of the four-branch symplectic
collision map.  Response, innovations, pressure, and covariance tensorize.

### Finding III.5 — Is the microscopic value problem genuinely defined?

**Risk.** An undefined “viscosity-duality solution” would simply move the hard
problem into terminology.

**Repair.** The prelimit is a finite sum/logarithm operator on bounded
continuous slow-state functions.  Its terminal recursion exists by direct
backward iteration.  The consistency remainder is a third-moment Taylor
remainder.  No fast distribution is evaluated at a viscosity contact.

### Finding III.6 — Does qualitative WIP yield the whole microscopic sequence?

**Risk.** Without a quantitative rate, block errors can accumulate.

**Repair.** The actual model uses direct predictable characteristics, so the
full sequence converges.  The separate block theorem requires the explicit
accumulation condition and states only a diagonal consequence without a rate.

### Finding III.7 — Is theta-expectation more than terminology?

**Risk.** Monotonicity and time consistency alone are standard semigroup
properties.

**Repair.** Paper III proves a microscopic collision construction, a compact-
control nonlinear branch, and forward theta-independence of the collision
innovations.  Paper V adds an intrinsic tangent-curvature characterization.

## 4. Paper IV — filtering and pure games

### Finding IV.1 — Does the noncompact filter truly retain memory?

**Risk.** Exact one-step refresh would be a degenerate forgetting example.

**Repair.** Only a fraction `delta` is refreshed.  The remaining mass follows
an autoregression with coefficient `r`.  Prediction contraction is strict but
nonzero, and a finite observation gap is required to dominate Bayes expansion.

### Finding IV.2 — Does a Lyapunov estimate imply contraction?

**Risk.** Moment stability and filter stability are logically different.

**Repair.** TV contraction comes from the common refresh component.  The
quadratic Lyapunov identity is used only to preserve the posterior moment ball.
They enter through two separate strict gates.

### Finding IV.3 — Is the pure saddle theorem valid on constrained controls?

**Risk.** A zero of the unconstrained gradient need not lie in closed convex
control sets.

**Repair.** The theorem is stated as the variational inclusion

```text
0 in G_z(w)+N_{U x V}(w).
```

The normal cone is maximal monotone; the compensated saddle operator is
strongly monotone; coercivity gives a unique solution.  Strong
concavity/convexity converts the variational inequalities to global saddle
inequalities.

### Finding IV.4 — Do mixed Hessians destroy strong monotonicity?

**Risk.** A large cross-control Hessian could appear in the symmetric part of
the saddle operator.

**Repair.** The two cross terms have opposite signs and cancel exactly because
`D_vu^2 F=(D_uv^2 F)^T`.  Only the compensated diagonal curvatures remain.

### Finding IV.5 — Does a local pure saddle prove a discrete game value?

**Risk.** Lower and upper discrete operators need not coincide at finite mesh.

**Repair.** The paper does not assert finite-mesh equality.  It proves separate
monotone lower and upper recursions.  Their consistency Hamiltonians coincide
by the pure local saddle theorem, and comparison identifies the same limiting
Isaacs value.

### Finding IV.6 — Is there a continuous-time feedback verification?

**Risk.** Formal optimization of the Hamiltonian is not a game theorem.

**Repair.** It\^o's formula under arbitrary `(u,v*)` and `(u*,v)` gives the two
value inequalities.  In the quadratic branch, completion of squares displays
them exactly.  Uniform parabolic approximation and strong-monotonicity
stability extend the result to the viscosity solution.

## 5. Paper V — characterization, Girsanov, and path branches

### Finding V.1 — Is terminal differentiability still assumed?

**Risk.** A formal expansion would not prove a derivative semigroup.

**Repair.** The parabolic terminal operator is shown to be a Banach-space
isomorphism by Schauder theory.  The implicit-function theorem gives a genuine
`C^{k-1}` solution map and its tangent equation.

### Finding V.2 — Is the characterization theorem circular?

**Risk.** If the exponential tilt were assumed, the conclusion would be
immediate.

**Repair.** The assumptions mention only probability first derivatives and a
covariance formula for second derivatives.  Along the ray `t phi`, these imply
a measure-valued replicator ODE.  Its unique solution is the exponential tilt;
integration of the first derivative then gives the log-moment functional.

### Finding V.3 — Do microscopic tangent laws converge, or are they added after
the diffusion limit?

**Risk.** A continuum representation alone would not explain the deterministic
origin.

**Repair.** The finite collision path law is exponentially tilted before the
limit.  Weak path convergence plus bounded exponential weights gives
convergence of the tilted laws, first derivatives, second derivatives, and all
finite-partition tangent kernels.  The exact discrete cocycle passes to the
continuum.

### Finding V.4 — Does the Girsanov density satisfy an integrability condition?

**Risk.** A local stochastic exponential need not be a true martingale.

**Repair.** The density is the normalized conditional exponential terminal
payoff.  For bounded payoff it is a positive bounded martingale and therefore
uniformly integrable.  In a bounded-gradient window Novikov holds directly;
otherwise the bounded-density/BMO route gives the change of measure.

### Finding V.5 — Is a nonlinear `Z -> p` inversion hidden?

**Risk.** If `sigma` depends on the unknown gradient, pointwise matrix
invertibility is not enough.

**Repair.** The actual entropic branch has state-dependent `sigma`, and the
tangent drift is written in terms of the already proved field `Du`.  No
inversion is performed.

### Finding V.6 — Are the path and 2BSDE branches dynamically defined?

**Risk.** Merely naming PPDE/2BSDE would not prove a representation.

**Repair.** The path entropic evaluation is a conditional exponential moment,
so the tower DPP is exact.  The volatility-control law family is stable under
conditioning and pasting, which gives the nonlinear DPP before the PPDE and
2BSDE representation are invoked.

## 6. Cross-paper checks

1. All terminal PDEs use the convention
   `-u_t - generator - Hamiltonian = 0`.
2. Paper II's covariance and Paper III's predictable bracket are the same
   finite branch matrix.
3. Paper III's collision recursion is the microscopic law tilted in Paper V.
4. Paper IV imports only the Paper III rough limit, not a representation
   theorem.
5. Paper V is strictly downstream of Papers III--IV.
6. The open-billiard strengthening is not a hidden input to the Markov
   collision chain.
7. No old A1--A5, S1--S3, CM2 interface forest, or paired-contact lemma appears
   as a load-bearing import.

## 7. Audit verdict

```yaml
hostile_findings: 31
hostile_findings_with_positive_repairs: 31
known_internal_referee_objection_gaps: 0
external_second_review: NOT_YET_PERFORMED
analytical_proof_certified_by_this_audit: false
```

The residual risks are the ordinary risks of new mathematics: the external
referee must check the analytic open-billiard coding, uniform Dolgopyat
constants, high-frequency derivative bookkeeping, curvature-compensated game
approximation, and tangent-law characterization line by line.  None of those
items is left as an unnamed downstream hypothesis in the five manuscripts.
