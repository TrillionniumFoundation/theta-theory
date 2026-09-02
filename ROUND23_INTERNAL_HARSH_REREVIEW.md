# Round-Twenty-Three internal hostile rereview

**Target:** all active `ROUND23_POSITIVE_CLOSURE.tex` sources  
**Method:** attempt to reconstruct the Round-Twenty-Two counterexamples and adjacent failure modes before allowing the branch to enter the external-review queue.  A source-level PASS here means that the stated attack is blocked by an explicit definition or proof step.  It is not an external referee decision.

## Executive finding

The exact mechanisms refuted in Round Twenty-Two no longer occur in the active sources.  In every case the revision changes the mathematical object rather than changing only the theorem's wording:

- response rates are domain norms;
- lattice arithmetic is a closed-subgroup calculation;
- order is a state coordinate;
- entropy recovery stays absolutely continuous;
- memory is an exact block identity with a `z^-1` leading term;
- canonical pressures are normalized;
- hard-sphere recollisions gain a regular loop factor and retain history across cuts;
- the kinetic Hessian is normal to the zero-cost manifold;
- compactness includes superquadratic uniform integrability;
- hidden Dirac dynamics are not dominated;
- strict duality is pulled back from the standard theorem;
- optional projections use prediction-process convergence;
- phase polynomial weights come from a local theorem.

The attacks below are also encoded, where finite-dimensional, in `tools/verify_round23.py`.

## A1 attacks

### A1-H1 — slow cylinder approximation inside a Hilbert space

**Attack.**  Choose a square-summable observable whose conditional-expectation tail decreases polynomially.  The old proof would still assign it an exponential rate.

**Result.**  Blocked.  The active response theorem is stated on `mathfrak C_eta^r`, whose norm contains the exponential tail.  Bare membership in the current Hilbert fibre has no probabilistic consequence.

### A1-H2 — nonmeasurable or nonintegrable current “expectation”

**Attack.**  Treat a deterministic current fibre element as if it were a random variable and write an expectation without a source probability space.

**Result.**  Blocked.  The source declares a strongly measurable map from the symbolic probability space into the Hilbert current fibre and uses a Bochner integral.

### A1-H3 — coordinatewise variances do not prove trace class

**Attack.**  Give finite variance in every basis direction but an infinite sum.

**Result.**  Blocked.  The martingale increment lies in `L^2(H)` and the proof uses the exact identity `trace Q=E||D||^2` followed by finite-rank tail control.

## A2 attacks

### A2-H1 — invertible real periodic matrix with nontrivial torus character

**Attack.**  For an invertible real matrix `D`, take `omega=2 pi D^{-T}k`; real invertibility alone does not imply a trivial character.

**Result.**  Blocked.  The active certificate first forces the roof frequency to zero using two irrationally related differences, then forces each torus coordinate through exact `Z^3` generators, and finally forces the constant phase through coprime periods.

### A2-H2 — dependent return points used for two integrations by parts

**Attack.**  Regard `T^n x` and `T^m x` as two independent variables although both depend on the same initial point.

**Result.**  Blocked.  Both phase functions are differentiated with respect to the genuine original collision coordinates `(r,phi)`.  The returned points appear only inside those phase functions.

### A2-H3 — an unbounded Fourier tail receives a frequency-independent exceptional constant

**Attack.**  Add an `e^{-cn}` bad-word term independent of `b` and integrate it over `b in R`.

**Result.**  Blocked.  The proof delays coarea until the first two good blocks, so the same `(1+|b|)^-2` factor multiplies the delayed contribution.  Every term in the unbounded region is integrable.

## A3 attacks

### A3-H1 — two path orderings with identical Eulerian occupation

**Attack.**  Exchange two legal excursions `A,B`.  Unordered transition counts and clock totals agree, while the physical path changes.

**Result.**  Blocked.  The empirical object is on chronological start time times complete mark space, and the stopped physical path is also retained.

### A3-H2 — representative atoms against a non-atomic kernel

**Attack.**  Approximate a continuous controlled density by one atom per cell; relative entropy is infinite.

**Result.**  Blocked.  Each cell receives the reference kernel conditioned on that cell.  The recovered density is a conditional expectation of `dq/dK`, and its KL is the coarse KL.

### A3-H3 — one excursion of length `N`

**Attack.**  Pay order-`N` entropy to select one very long mark, so the number of returns divided by `N` tends to zero.

**Result.**  Blocked.  No lower return-count compactness is asserted.  The mark is represented in the recession coordinate and pays its actual entropy cost.

### A3-H4 — arbitrary path tilt treated as a fixed cylinder insertion

**Attack.**  Insert `exp(-NF(path))` into a local theorem proved only for bounded finite-memory observables.

**Result.**  Blocked.  The active conditioning proof first approximates `F` exponentially by finite-memory functionals on rate sublevels, applies source-inserted inversion, then removes the approximation.

## A4 attacks

### A4-H1 — order-one Lyapunov mass in a remote mark

**Attack.**  Put a mark of size `rho^-n` at depth `n`; its Lyapunov contribution is one.

**Result.**  Blocked.  The proof never claims that contribution is small.  Its influence on the current transition density is `(theta/rho)^n`, and the bounded metric tail is `sigma^n`.

### A4-H2 — residue of a holomorphic full resolvent

**Attack.**  Evaluate the full resolvent at a regular point; the residue is zero, so an alleged transmission generalized vector vanishes.

**Result.**  Blocked.  The construction is deleted.  Only genuine Riesz projections at genuine spectral poles are used.

### A4-H3 — generic memory transform behaves as `z^-1`

**Attack.**  Expand `(z-QLQ)^-1`; the coefficient `PLQLP/z` is generally nonzero.

**Result.**  Blocked.  The active theorem states exactly this expansion.  Time decay comes from the `Q` semigroup; a separate explicit leading-pole subtraction creates an integrable remainder when needed.

### A4-H4 — rough observable outside the spectral Banach space

**Attack.**  Give an observable with a finite `2+epsilon` moment but no weighted Lipschitz regularity; the Poisson series need not converge in the claimed norm.

**Result.**  Blocked.  The rough-path theorem requires both the weighted Banach-space membership and the moment.

## B1 attacks

### B1-H1 — Stirling divergence

**Attack.**  At zero source, retain the unnormalised `1/N!` exact-particle integral and divide its logarithm by `N`.

**Result.**  Blocked.  The canonical source is a probability MGF and equals one at the origin.  Absolute free energy displays the ideal-gas correction separately.

### B1-H2 — look-ahead selection of good blocks

**Attack.**  Choose a positive fraction of “good” blocks after observing the complete configuration, then multiply conditional characteristic contractions as if the choice were predictable.

**Result.**  Blocked.  Label blocks are deterministic and chart partitions are expanded in lexicographic filtration order.  The tower-property product is adapted.

### B1-H3 — boundary distribution after zero extension

**Attack.**  A coarea density is smooth inside a chart but nonzero at its boundary; zero extension creates a distributional derivative.

**Result.**  Blocked.  The partition functions vanish through the required derivative order at every chart boundary before integration by parts.

### B1-H4 — conditional Gaussian with omitted cross term

**Attack.**  Let lattice and continuous constraints have nonzero covariance and condition on a nonzero lattice deviation.

**Result.**  Blocked.  The local coefficient uses the shifted conditional mean and Schur complement.

## B2 attacks

### B2-H1 — grazing concentration with bounded moments

**Attack.**  Concentrate collision current near grazing while preserving velocity moments.

**Result.**  Blocked on the theorem's regular class.  Quantitative grazing decay uses an `L^p(A_f)` density.  General finite-entropy controls are approximated by bounded-density nongrazing controls; moments alone are not used.

### B2-H2 — rank-loss mechanism outside a named list

**Attack.**  Construct a graph chronology whose loop Jacobian loses rank for an algebraic reason not described as grazing, simultaneity, collinearity, or a named multiple contact.

**Result.**  Blocked.  All rank loss is encoded by the maximal-minor determinant ideal, whose sublevel is controlled by analytic stratification.  Named boundary events are separate.

### B2-H3 — regular surplus contact receives no extra smallness

**Attack.**  On a chart with a nonzero loop minor, the old proof only controlled the singular complement and left the regular surplus integral at order one after Boltzmann--Grad cancellation.

**Result.**  Blocked.  The loop-closure tube has an additional coarea width.  Optimizing regular and small-minor contributions gives a positive power per independent loop.

### B2-H4 — hidden correlations cross a slice

**Attack.**  Two microscopic ensembles have the same one-particle density/contact trace at time `s` but different collision ancestry, hence different futures.

**Result.**  Blocked.  The interface state includes all connected histories and open ancestral half-edges.  Composition glues that hierarchy, not only its projections.

### B2-H5 — analytic pressure without an LDP lower bound

**Attack.**  A locally uniform log-MGF limit alone may fail to expose all finite-action points or prove concentration under tilted laws.

**Result.**  Blocked.  The source separately proves exponential tightness, exact deterministic initial-law tilts, concentration through the history expansion, and positive rate-dense recovery.

## B3 attacks

### B3-H1 — collision form degenerates in velocity tails

**Attack.**  Compact positivity permits the reference density to vanish too quickly at infinity, destroying one global form comparison.

**Result.**  Blocked on the declared regular class by global two-sided Maxwellian comparison and weighted derivative bounds.

### B3-H2 — deterministic-time cumulants at a random stopping time

**Attack.**  Restarting from a reduced density ignores the deterministic microscopic history at the stopping time.

**Result.**  Blocked.  The proof conditions on the full hard-sphere phase point, where exact deterministic restart holds, and imports B2's uniform complete-history bound.

### B3-H3 — zero-cost manifold receives positive Hessian

**Attack.**  Move `f` and set `Gamma=A_f` throughout.  The action is identically zero.

**Result.**  Blocked.  The normal defect is zero along this path and the collision quadratic form vanishes exactly.

## B4 attacks

### B4-H1 — vanishing remote mass carries fixed energy

**Attack.**  Put mass `n^-2` near speed `n`.  Narrow convergence holds, the second moment does not converge, and quadratic tests are not compact.

**Result.**  Blocked.  The `(2+delta)` moment diverges and excludes the sequence from every fixed shell.  The theorem uses `W_2` compactness.

### B4-H2 — weak metric silently upgraded to weighted total variation

**Attack.**  Start two measures close on a countable family of tests but far in a strong weighted norm.

**Result.**  Blocked.  The transfer estimate begins and ends in `W_2`; no topological upgrade is asserted.

### B4-H3 — product collision measure fails under weak convergence

**Attack.**  Send collision energy to infinity while preserving weak convergence.

**Result.**  Blocked by the uniform superquadratic moment.  The proof truncates velocities, passes the bounded product kernel, and removes the tail uniformly.

### B4-H4 — graph convergence without comparison

**Attack.**  Two viscosity solutions survive because maximal dissipativity of a formal graph is not a comparison theorem on the measure state.

**Result.**  Blocked.  The source gives a cylindrical core, containment function, product-continuity modulus, and a `W_2` doubling argument before using microscopic graph convergence.

## C1 attacks

### C1-H1 — common probability dominates uncountably many deterministic Dirac kernels

**Attack.**  A dominating probability would need a positive atom at every deterministic image point.

**Result.**  Blocked by type separation.  The hidden transition is never dominated; only observation laws have densities.

### C1-H2 — aggregate LLT used as a conditional observation theorem

**Attack.**  Integrating over hidden entrances smooths a law even though the conditional law at a fixed hidden state is singular or discontinuous.

**Result.**  Blocked.  The source repeats the A2/B1 inversion with the hidden entrance history retained as an insertion and states the resulting `L^1` conditional regularity.

### C1-H3 — infinite reference measure destroys a small-evidence bound

**Attack.**  Bound a bad evidence set by `delta nu(Y)` when `nu(Y)=infinity`.

**Result.**  Blocked.  The integrated numerator identity bounds posterior error by `L^1` numerator/evidence differences and never multiplies a uniform pointwise error by total reference mass.

### C1-H4 — nonconvex reachable set has no continuous retraction

**Attack.**  A finite coordinate reconstruction is asserted to land in an arbitrary compact reachable subset.

**Result.**  Blocked.  Reconstruction takes convex combinations in the ambient belief simplex; it only approximates the reachable set.

### C1-H5 — compact action set includes an uninformative policy

**Attack.**  Choose the same parameter-independent observation at every step; Fisher information is zero.

**Result.**  Blocked.  Uniform LAN/BvM is stated only on the persistently excited and identifiable policy class.

## C2 attacks

### C2-H1 — weighted tail functions contradict a proposed strict sequence criterion

**Attack.**  Put a test of amplitude comparable to `W` on disjoint remote annuli; normalized tails do not vanish as claimed.

**Result.**  Blocked.  The bespoke sequence criterion is removed.  The topology is the exact pullback of the standard strict topology and its dual follows by a linear homeomorphism.

### C2-H2 — collision term omitted from the balance adjoint

**Attack.**  Integrate the linearized collision operator against an adjoint test; a nonzero `L_f^*r` term remains.

**Result.**  Blocked.  It is explicit in both the smooth adjoint and the closed annihilator theorem.

### C2-H3 — pressure derivative only gives equilibrium means

**Attack.**  An equilibrium expectation identity is not a periodic-orbit sum identity.

**Result.**  Blocked.  A separate zero-temperature equilibrium-localisation lemma approximates each periodic measure, followed by a constructive Livsic argument.

### C2-H4 — weak convergence does not preserve conditional distributions or brackets

**Attack.**  Use two joint laws with the same weak limit but unstable conditional laws.

**Result.**  Blocked.  The theorem assumes convergence of the prediction process, filter martingale problems, UT characteristics, and predictable brackets.

### C2-H5 — a likelihood martingale hits zero

**Attack.**  A finite continuous Brownian stochastic exponential is strictly positive, so it cannot represent such a likelihood.

**Result.**  Blocked.  The active theorem assumes finite-horizon equivalence, strict positivity, and reciprocal moments before taking logarithms.

## D1 attacks

### D1-H1 — equal LDP costs but different polynomial powers

**Attack.**  Two models have the same exponential rate and different local dimensions or exact-number prefactors.

**Result.**  Blocked.  The phase weights are computed from the full local coefficient and Morse--Bott normal determinant.  The LDP is used only for exponential separation.

### D1-H2 — phase boundary or noncompact complement has the same cost

**Attack.**  Conditioning on a cell changes the rate because its boundary carries a minimizer, or mass escapes outside all compact phase charts.

**Result.**  Blocked.  Tubular boundaries are chosen above the minimum, and exponential tightness first confines all minima to a compact sublevel.

### D1-H3 — controller chooses a different action after learning the unobserved phase

**Attack.**  Put `sup` inside the phase sum.

**Result.**  Blocked.  The Bellman state carries the phase posterior and chooses one common action before the evidence-weighted update.

### D1-H4 — global complex dominance without a gap

**Attack.**  At coexistence, analytic component sums may have zeros arbitrarily near the real parameter.

**Result.**  Blocked.  Zero-free charts are asserted only in a region with a quantitative real-part gap and proved by Rouche.  The coexistence sum is retained otherwise.

### D1-H5 — Gaussian component means inserted after global centering

**Attack.**  Center once globally and then assign each component its uncentered phase mean.

**Result.**  Blocked.  The fluctuation is centered by `m_{J_N}` on the labelled space before mixture and contraction.

## Cross-paper hostile checks

### X-H1 — source-slot ambiguity

Every active wrapper imports `ROUND23_POSITIVE_CLOSURE.tex`; no Round-Twenty-Three wrapper imports the legacy `ROUND17` slot.

### X-H2 — circular exact-number dependence

The B2 grand-canonical theorems precede B1.  B1 returns only the exact-number local coefficient to the B2 microcanonical theorem.

### X-H3 — status words substitute for a theorem

The verifier requires the active labels and proof environments, not occurrences of words such as “closed”, “exact”, or “verified”.

### X-H4 — unresolved citations hide an import

Every active citation key is checked against all bibliography files loaded by that paper.  Missing citations fail before TeX publication.

### X-H5 — prior internal PASS is inherited

No.  Round-Twenty-One internal review files remain historical.  Round Twenty-Three has a new verifier, new regressions, new source manifest, new build hashes, and a new workflow.

## Internal disposition

**Direct Round-Twenty-Two counterexamples:** source-level closure found for all listed attacks.  
**Dependency order:** acyclic under the explicit B2-GC/B1/B2-MC split.  
**Publication condition:** this disposition becomes a repository verification PASS only after `tools/verify_round23.py` and all eleven clean TeX builds succeed on the exact branch head.  
**External status:** open for the next independent referee round; no internal check is represented as journal acceptance or as a proof that no further counterexample exists.
