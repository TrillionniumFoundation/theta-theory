# Author Response to the Round-Twenty Referee Reports

**Referee branch:** `review/round20-gpt56-pro-harsh-11paper-2026-09-02@1e69f06bfa6df29cad985f6ccef6aa9559ac6a7b`  
**Revision branch:** `revision/round21-referee-positive-closure-11paper-2026-09-02`

We agree with the referee's threshold objection: the previously declared
Round-Nineteen branch contained no revised mathematical source.  This response
therefore begins from the exact Round-Twenty report commit and replaces the
active `ROUND17_POSITIVE_CLOSURE.tex` file in every paper folder.  The new
proofs are not branch renamings, report-only changes, or certificate claims.

The detailed Round-Eighteen reports incorporated by Round Twenty were treated
as the controlling blocker inventory.  The historical recursive/CM2 corpus
was audited first.  Its own control files are fail-closed and give zero formal
theorem credit; only local constructions whose full hypotheses could be
restated and reproved were retained.  The result is recorded in
`ROUND21_HISTORICAL_DERIVATION_AUDIT.md` and the noncircular order in
`ROUND21_PROOF_DEPENDENCY_LEDGER.md`.

## A1

The former generated face quotient has been removed.  The active proof first
constructs one labelled baker diffeomorphism and then its ordinary mapping
torus; closedness and properness of the complete equivalence relation and the
corner collars are proved.  A primitive is matched at the one-form level, so
the exact symplectic form descends.  Negative-Sobolev restriction is no longer
used: positive Sobolev test jets carry all face/corner restrictions and the
current space is their Hilbert dual.  The material derivative is a bounded
transpose on one fixed fibre.  The response formula is obtained as the limit
of exact finite-cylinder derivatives, and the FCLT now contains an explicit
geometric projective estimate and trace-norm covariance proof.

## A2

The impossible unweighted countable-branch sum is replaced by an
inverse-Jacobian-weighted complexity theorem.  The parent-fold bundle is
constructed on transported stable-curve strong/weak spaces.  The arithmetic
and UNI arguments are written geometrically from reflection equations,
regular continuation, four independent periodic differences, and a common
suffix cancellation; the JSON file is retained only as a regression summary.
The very-high-frequency tail uses two fixed returned coarea coordinates and a
fixed number of integrations, eliminating the circular constants `c_M`.
Together with the Dolgopyat range this gives an integrable global majorant, a
roof-density theorem, the raw four-dimensional LLT, and precisely delimited
conditioning windows.

## A3

The one-step countable edge surrogate is replaced by the exact regular
conditional history kernel of the induced billiard.  The state retains the
complete past, current continuous unstable coordinate, and full physical
excursion.  A model-derived exponential cost produces a Polish marked
stopped/recession space.  The stopped Gibbs representation includes the exact
relative entropy of a continuous terminal prefix rather than `-log` of a
point probability.  Controlled compactness, a legal finite-memory recovery
using actual physical excursions, explicit collision/physical-clock rates,
and inserted local conditional Laplace principles are proved.

## A4

Exponential variation is derived from stable holonomy and A2 distortion;
it is no longer inferred from summability.  Power drift and a synchronized
minorization are proved and then used to establish the precise weighted
Lipschitz operator gap.  The source class is a linear parameter space, not a
false algebra, and the Feynman--Kac operators act analytically on one fixed
weighted space.  The suspension rough-path estimates are written.  The
operator renewal identity is derived by integrating the graph resolvent along
flights and explicitly intertwined with A2.  All transmission zeros in a
strip are resolved simultaneously by their finite Jordan chains; the fixed
resolved space then yields an `O(|b|^{-2})` memory transform and exponential
inverse-Laplace bound.

## B2

The hard-sphere scaling and trace topology are fixed.  Uniform flux estimates
exclude concentration near grazing and multiple contacts, closing the Green
specular graph.  The precontact map is stratified on compact semianalytic
parameter sets.  Most importantly, the exponential-generating `1/k!` symmetry
factor is part of the connected coefficient before estimation.  The remaining
rooted recursion is Catalan/geometric; no factorial is discarded.  A positive
balanced recovery is constructed by solving the controlled Boltzmann equation
with positive relative multiplier, respecting the nonlinear map
`f -> A_f`.  The finite-volume likelihood is the exact exponential tilt of
the random initial configuration, not a Poisson compensator.  The limiting
Legendre calculation and full grand-canonical/microcanonical LDP proofs are
then separated cleanly.

## B1

The constraint is placed on its true quotient space.  The source-dependent
saddle is global on compact interior mean sets.  High-frequency smoothing is
performed by many disjoint fixed-size, full-rank blocks.  Each block requires
only a fixed derivative order, so the former `C^4` versus `O(N)` contradiction
disappears.  Position variables are included in the coarea minor whenever the
Fourier direction is position dominated.  The local theorem distinguishes
lattice and continuous coordinates, states absolute versus relative shell
errors, and never assigns positive mass to an exact point in a continuous
coordinate.  Exact-number pressure and the microcanonical Schur covariance
are extracted from the already proved B2 grand-canonical pressure.

## B3

The cutoff collision form is now stated with its correct weighted microscopic
`L^2` coercivity.  A transport--collision graph norm and Kawashima moment
system control the hydrodynamic block and give a nonautonomous closed-range
theorem.  A concrete Hermite/Fourier scale has Hilbert--Schmidt embeddings and
therefore is nuclear.  Localized cumulants use B2's normalized expansion;
stopping-time conditional increments and compact containment give process
tightness.  The Gaussian process is constructed before the action Hessian is
identified.  The latter is treated as a nonconvex second epi-derivative on a
positive exponential balance manifold, with an implicit exactly balanced
second-order recovery.

## B4

The state topology and action sublevels are defined and proved compact.
State-dependent control transfer solves the same positive controlled
Boltzmann equation from the perturbed initial state, rather than adding a
signed current.  Strong continuity is asserted uniformly only on energy
shells.  The discounted DPP yields the correct implicit nonlinear resolvent
identity

`J_lambda h = J_mu((mu/lambda) h + (1-mu/lambda) J_lambda h)`.

This gives a parameter-independent maximal dissipative graph and comparison.
The law--hierarchy map is proved by absolutely convergent Janossy inversion.
The microscopic corrector solves an exact backward specular boundary problem;
a diagonal choice handles genealogy-dependent exponents without assuming a
uniform one.  Compact containment, both extended-generator inequalities, and
comparison then yield the nonlinear semigroup limit.

## C1

Hidden transition and observation kernels are separated.  Atomic, lattice,
and continuous observations live on one stratified reference measure, so no
unsupported smoothing is needed.  A fixed hidden reference measure is part of
the reachable regular chart, and domination, Sobolev regularity, and compact
forward invariance are derived from A2/B1/B2/B4.  Zero evidence is assigned an
explicit isolated cemetery belief; no projective direction is attached to the
zero measure.  The controlled belief kernel is Feller and the relaxed-control
DPP and selectors are verified.  Finite coordinates are chosen on one
forward-invariant reachable compact set with an explicit finite-horizon error
argument.  LAN is a direct uniform triangular-array log-likelihood expansion
with third-order remainder and contiguity.  Uniform tests and posterior
concentration are proved before the strategy-uniform Bernstein--von Mises
theorem.

## C2

The weighted strict topology is defined by explicit compact and normalized
tail seminorms and its measure dual is proved.  Coboundary separation is stated
only for A4/B4, where invariant weighted probabilities exist.  Common form
domains, coercivity, metric transport, and derivatives are verified for the
actual platforms.  A form-level Schur complement is proved under a bounded
form-domain projection.  Countable-history Livsic and the hard-sphere
annihilator are separate model-specific theorems.  Changing-filtration
convergence includes finite-dimensional conditional laws, compact
containment, and an Aldous stopping-time estimate.  Only after the observation
filtration is identified with the innovation filtration is the optional
projection represented as a stochastic exponential.  The contraction
definition contains only state/source/form data; rates, pressures,
covariances, and memory are conclusions, and A3/B2/C1 furnish explicit
examples.

## D1

Phase labels are now disjoint Borel events in the original finite-volume
sample space, defined from separated order-parameter minima; the exact marginal
mixture is therefore a theorem.  Sharp A2/B1 local asymptotics give complete
weight constants and component LDPs at one speed, including any boundary
phase.  The sufficient state contains every phase-conditioned belief
`(rho_j, pi_j)`, and C1 supplies common likelihood domination.  The
risk-sensitive value optimizes one shared observation-based policy outside
the finite sum; separately optimized component values are not combined.  The
zero-free complex chart is derived from the upstream spectral/coefficient
expansion.  The coexistence theorem now concerns
`(J, sqrt(a)(TX-m_J))`, with Gaussian mean zero, defines `gamma_*`, and includes
all subexponential constants.  Phase-aware contractions preserve this policy
and scaling order.

## Claim strength and verification

All eleven advertised positive regular-regime theorem packages remain active.
No principal theorem has been replaced by a no-go result, a theorem downgrade,
or a genericity statement.  Assumptions newly made explicit--regular source
charts, compact interior saddle sets, finite horizon, and positive prepared
states--are the same model class in which the prior manuscripts claimed their
results; they now appear before use and are propagated through the dependency
ledger.

Repository proof-structure, hostile-pattern, dependency, and TeX build checks
are supplied by the Round-Twenty-One workflow.  Their success certifies source
identity and reproducibility only.  It does not claim journal acceptance or
replace a new independent mathematical review.
