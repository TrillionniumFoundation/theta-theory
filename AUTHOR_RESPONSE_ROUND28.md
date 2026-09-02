# Author Response to the Round-Twenty-Eight Referee Report

**Repository:** `TrillionniumFoundation/theta-theory`  
**Revision branch:** `revision/round29-referee-positive-closure-11paper-2026-09-02`  
**Controlling review branch:** `review/round28-gpt56-pro-harsh-11paper-2026-09-02`  
**Controlling review commit:** `12bfa8d233078a3a0fb2e25b9e9ab7245c62c2e7`  
**Reviewed source commit:** `31d955aad5cff5c8edba00bfb9e500a87fd3ba72`  
**Active revision:** Round Twenty Nine  
**Date:** 2 September 2026

## 1. Revision policy

The Round-Twenty-Eight report correctly distinguished source-switching success from mathematical correctness. Round Twenty Nine therefore changes the active theorem sources themselves. It does not treat a response, ledger, manifest, verifier, or successful build as a proof.

The revision preserves the positive program: current response and functional limits, Sinai mixed local limits, chronological path large deviations, history pressure and memory, hard-sphere exact preparation and dynamic large deviations, kinetic fluctuations and nonlinear semigroups, filtering and statistical limits, cotangent rigidity, and phase/control synthesis. The changes restrict each statement only to the exact state, source, regularity, and attainable classes supported by its proof; no theorem is replaced by a no-go statement.

Historical Round-Seventeen through Round-Twenty-Seven derivations were reused where they remained valid: parent-fold transport, Jacobian-weighted branch summation, completed graphs, weak-Harris coupling, exact coarea conditioning, factorial Duhamel bounds, relative-entropy tilting, hypocoercive Fourier estimates, mixed strict duality, and finite-scale phase posteriors. The direct contradictions identified by the referee were not retained.

## 2. Direct contradictions and active-source repairs

### A1: derivative direction and path continuity

**Report.** The material derivative was mapped toward a more regular Sobolev-dual space, contradicting the distributional derivative of a Dirac mass. The displayed “polygonal” process was a step function and therefore did not take values in `C([0,1])`.

**Round 29.** The test connection loses two derivatives,
`nabla_test : Phi^{s+2} -> Phi^s`, so transposition gives the correct current map
`nabla : J^s -> J^{s+2}`. The `j`th jet lives in `J^{m+2j}`. Boundary data are split into decaying shell currents and normally convergent cumulative currents. The process now contains the fractional interpolation term
`(nt-floor(nt))Y_floor(nt)`, and a maximal-jump lemma transfers the martingale FCLT to the continuous interpolation. Trace-norm differentiability of the covariance is proved from normally convergent projection derivatives.

### A2: impossible branch certificate and continuous arithmetic

**Report.** An unweighted sum of inverse-branch `C^2` norms was impossible already at derivative order zero. Two roof vectors do not generically remove all continuous characters in dimension two. Bad-word and operator estimates were stated rather than derived.

**Round 29.** Every branch derivative is multiplied by the inverse Jacobian. The global hypothesis is a finite Jacobian-weighted grammar: finite chart types, a finite returned-UNI automaton, finite terminal nonstationarity charts, and finite periodic data. In dimension two the explicit generators `(1,0)`, `(0,1)`, and `(sqrt(2),sqrt(3))` have trivial annihilator. Stable-curve pairings are defined in completed anisotropic spaces. Returned blocks and finite-automaton bad words both acquire an integrable `|b|^{-M}` bound, which is assembled into four frequency regimes and a source-uniform mixed local theorem.

### A3: false balance, invalid clock, and pinned renewal coordinate

**Report.** The prior history balance failed for a chronological-only test, a collision-stopped path was evaluated on a physical-time interval not guaranteed to exist, and `S_{nu_N}R` was treated as a nondegenerate square-root Gaussian although it is pinned by the stopping rule.

**Round 29.** The state begins with an exact finite-word telescoping identity containing the increment `R(m_k)/N`, the holding occupation, transition flow, endpoint values, and a quantified discretization error. Collision and physical completed graphs are separate and normalized by their actual totals. Recurrent and recession pieces are disjoint projective coordinates with a proved mass budget and terminal compactification. The stopped theorem applies the Gaussian local limit only to `(nu_N,S_nu kappa,S_nu tau)` and retains `O_N=S_nu R-N` as an order-one overshoot kernel. A fractional conditional exponential moment gives the genuine power drift exported to A4.

### A4: unsupported drift, incompatible norm, and unproved sectoriality

**Report.** The claimed power drift did not follow from the imported A3 moment. A capped distance together with a global Lipschitz seminorm forced bounded oscillation, contradicting unbounded weights and sources. Renewal and compression domains were incomplete, and a sectorial high-frequency expansion was asserted without sectoriality.

**Round 29.** A3 now proves `E[e^{epsilon chi}|h] <= C W(h)^zeta` with `rho+zeta<1`, yielding `PW <= C W^{rho+zeta}`. Weak-Harris transport uses a capped cost, but the operator seminorm divides by a local history distance times the polynomial weight, so functions may grow like `W^gamma`. The suspension state is explicitly `(h,m,r)` and the four maps `R0,B,T,A` are fully typed. Compression is transported by an equal-rank graph isomorphism with complete graph-norm hypotheses. The memory expansion is proved on a vertical half-plane by three resolvent identities and `B_Q(R) subset D(L_Q^3)`; no analytic or sectorial semigroup is assumed.

### B1: exceptional Fourier tail and undefined coefficient power

**Report.** The reserved “good block” need not be good on the exponentially exceptional event, so that event still contributed a nonintegrable constant over the continuous Fourier space. The coefficient ratio used undefined indices.

**Round 29.** Good blocks are used only for central and annular contraction. A deterministic finite coarea-anchor cover supplies a `W^{s,1}` density conditionally on every exterior configuration, including the exceptional event. Conditioning is nested in one increasing filtration. Source derivatives are centered and controlled at the same scale. Numerator and denominator use separate saddles but the same fixed constraint dimension; the common power of `N` cancels and the ratio contains only the Hessian determinant and coarea amplitude ratio.

### B2: undefined fibre product, wrong labels, and constraint-breaking shear

**Report.** A fibre product is not canonical for arbitrary signed measures; a fully labelled graph does not have automorphism factor `k!`; and translating a descendant subtree generally breaks earlier tree contacts.

**Round 29.** Histories are kernels admitting declared disintegrations with respect to standard cut reference measures. Gluing is ordinary kernel composition, so Tonelli proves associativity. Fully labelled histories have trivial automorphism and carry the separate exponential-generating factor `1/k!`; unlabelled histories use `1/|Aut G|`. Loop pivots are tangent vector fields on the full tree-contact manifold, constructed by a causal right inverse of the tree constraint derivative. They preserve every tree contact exactly and give a lower-triangular surplus Jacobian with certified nonzero diagonal. The regular coarea calculation retains one `epsilon^2` factor per true surplus contact; singular charts are optimized separately. The creation operator, time-ordered Duhamel map, filtered logarithm, initial cumulant condition, local recovery frames, Chernoff tilt, and projective joint rate are all explicit.

### B3: erased contact cycles and wrong localization scaling

**Report.** Quotienting by `ker C` erased observable contact-current perturbations with positive entropy cost. Space localization created commutators of order `1/ell`, not `ell`.

**Round 29.** The full contact Hilbert space is retained and decomposed as `ker C` plus its orthogonal complement. Balance sees only the normal component, but action, covariance, and the Mosco Hessian charge both normal and cycle directions. The density-only quotient appears only after an explicit infimum over contact tangents. The graph estimate is proved as a global small perturbation of the Maxwellian Fourier/Kawashima estimate; no shrinking spatial partition is used. Stopping-time tightness is derived from a root-revealment martingale and factorial cluster influence bounds, without a conditional-density denominator or regeneration claim.

### B4: wrong contraction, broken semigroup, and unsupported moment

**Report.** A density path cannot have the cost of every contact control producing it; initial entropy inside each time interval destroys `V_0=Id` and double counts under concatenation; and a Gaussian reference cannot support the asserted exponential superquadratic moment.

**Round 29.** The joint rate retains `(f,Gamma)` and the density rate is its infimum over `Gamma`. The running action contains only the dynamic collision entropy. Initial preparation entropy is charged once by a separate outer variational functional. Consequently `V_0=I` and `V_{t+s}=V_tV_s`. Containment is proved at quadratic energy scale: microscopic elastic dynamics conserves the empirical second moment pathwise, and a dynamic relative-entropy estimate gives uniform second-moment integrability. The state space, collision entropy topology, comparison shell, canonical entropy-projection realization, and semigroup types are explicit.

### C1: envelope normalization and non-differentiable Dirac transport

**Report.** Translating a density against an arbitrary finite probability envelope was not normalized. Deterministic Dirac push-forwards are not differentiable in total variation or finite signed-measure norm.

**Round 29.** Each observation stratum has its canonical sigma-finite base measure and a fixed positive probability envelope `q_s m_s`; the density with respect to that envelope is exactly `rho_s(y-O(x))/q_s(y)` (with the corresponding group Jacobian on surface strata). Hidden push-forwards are differentiated in a negative Sobolev scale, losing one order per derivative. Global Feller continuity and diagnostic derivative contraction are separate statements. Diagnostic policies have pointwise conditional action-probability bounds, and a beliefwise Gramian gives the information lower bound directly. Signal separation plus an injective noise channel supplies global testing away from the LAN neighbourhood.

### C2: hidden local compactness and mismatched innovations

**Report.** A continuous weight with compact sublevels would force local compactness, contrary to the claimed arbitrary Polish setting. Brownian innovation formulas were applied to general discrete/surface/countable observation channels.

**Round 29.** The mixed strict topology is generated by all sequences of compact sets and vanishing coefficients; no compact exhaustion or proper continuous weight is assumed. Its weighted dual is proved by pullback from finite Radon measures. The full kinetic annihilator first forces the contact source to be orthogonal to `ker C`. Exposing rays use finite bounded potentials and overlapping A4 pressure charts. Stopped paths are embedded by constant continuation in one fixed `D([0,T],E)` space and carry an explicit continuation kernel. Discrete-time product likelihoods, marked-point Doléans exponentials, and Brownian Girsanov likelihoods are separate propositions. BSDE stability includes terminal and driver convergence.

### D1: zero prior phases, circular rates, and policy integration

**Report.** Zero-weight phases were included in the leading maximum, component rates were circularly defined, and a Morse--Bott integration over a policy manifold was used although the policy is optimized rather than integrated.

**Round 29.** The upstream local input is a finite mixed lattice/continuous vector. The labelled rate `mathcal I(j,z)` is primary; `gamma_j` and `I_j` are derived from it. Only `J_+(w)={j:w_j>0}` enters the log-sum-exp; exponentially small priors are folded into the phase rate. Relaxed policies are represented by closed strategic measures, so compactness and adaptedness are proved. A uniform finite-dimensional controlled expansion is stated only for the supported source coordinates. Mechanical state variables use mixed lattice--Morse--Bott integration. Policies use a uniform second-order epi-development and lexicographic argmax; no policy-volume factor appears.

## 3. New mathematical tools

1. **Loss-Indexed Projective Current Calculus (LIPCC):** a projective connection whose current index increases with distributional singularity, with separate shell and cumulative boundary jets.
2. **Jacobian-Weighted Finite Grammar (JWFG):** finite billiard chart/automaton data that imply weighted branch regularity, returned UNI, bad-word decay, and correct continuous arithmetic.
3. **Two-Clock Telescoping Current Complex (TCTCC):** an exact discrete balance object retaining chronological increments, transition flow, holding occupation, two graph clocks, and endpoint defects.
4. **Universal Coarea Anchor Family (UCAF):** a deterministic finite minor cover that gives high-frequency density decay on every conditional component.
5. **Disintegrated Kernel Category with Constraint-Preserving Pivots (DKC-CPP):** a typed collision-history category and tangent loop-rank mechanism.
6. **Orthogonal Contact Cycle--Normal Splitting (OCCNS):** full joint contact geometry with density contraction performed only after minimization.
7. **Preparation--Running-Action Factorization (PRAF):** a dynamic action that concatenates and an initial entropy charged once.
8. **Stratified Envelope and Distributional Belief-Jet Calculus (SEDBJ):** exactly normalized observation densities and differentiable deterministic filters on a Sobolev-loss scale.
9. **Weighted Mixed-Strict/Channel-Specific Calculus (WMSC):** Polish strict duality without local compactness and likelihood formulas matching the observation type.
10. **Positive-Support Epi-Argmax Expansion (PSEA):** phase asymptotics with zero-prior exclusion and deterministic lexicographic policy selection.

## 4. Active deliverables

The revision source tree and its reproducible build chain contain:

- eleven active `ROUND29_POSITIVE_CLOSURE.tex` sources;
- eleven standalone `ROUND29_REVISION.tex` wrappers;
- eleven `main.tex` aliases resolving only to Round Twenty Nine;
- source wrappers for eleven rebuilt individual PDFs and one 51-page consolidated dossier; local verification has produced all twelve PDFs, and CI republishes them as an artifact;
- `ROUND29_REVIEW_INDEX.md`;
- `ROUND29_PROOF_DEPENDENCY_LEDGER.md`;
- `ROUND29_MATHEMATICAL_REGRESSIONS.md`;
- `ROUND29_SOURCE_MANIFEST.json`;
- `ROUND29_FINAL_VERIFICATION.json`;
- `tools/verify_round29.py`;
- `.github/workflows/verify-round29-referee-closure.yml`.

The verifier checks source identity, forbidden old imports, control bytes, theorem/proof balance, label uniqueness, direct counterexample tokens, source hashes, all eleven standalone builds, the consolidated dossier build, PDF headers, and page inventory. These checks establish reproducibility and removal of the enumerated formal contradictions. They do not replace independent specialist review of every deep analytic estimate.

## 5. Status for the next review

All direct algebraic, topological, domain, scaling, and stochastic-calculus contradictions listed in the Round-Twenty-Eight report have an active-source replacement and an executable regression gate. The remaining question is not whether the old formulas survived--they did not--but whether the new certified geometric and analytic arguments meet the standards of the next independent specialist review.
