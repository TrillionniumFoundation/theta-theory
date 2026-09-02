# Author Response to the Round-Twenty-Six Referee Report

**Repository:** `TrillionniumFoundation/theta-theory`  
**Revision branch:** `revision/round27-referee-positive-closure-11paper-2026-09-02`  
**Base review branch:** `review/round26-gpt56-pro-harsh-11paper-2026-09-02`  
**Base review commit:** `8b1b945ee2ea69226dcb9562bd61812c5c58db47`  
**Active revision:** Round Twenty Seven  
**Date:** 2 September 2026

## 1. Source-of-truth correction

The referee was correct that the nominal Round-Twenty-Five branch was a no-op: it pointed to the same mathematical tree as Round Twenty Three.  Round Twenty Seven is not an audit-only response.  Every active `main.tex` resolves to `ROUND27_REVISION.tex`, which imports only `ROUND27_POSITIVE_CLOSURE.tex`; each paper has a standalone `ROUND27_REVISION.tex`; the root dossier source is versioned; and the CI workflow rebuilds and publishes the consolidated dossier plus all eleven individual revision PDFs as one workflow artifact.  The repository also contains the response, dependency ledger, source manifest, verifier, and CI workflow.

The revision is based directly on the Round-Twenty-Six review head.  It does not claim that a status document repairs a theorem.  The mathematical source and the statements described below are the same files imported by `main.tex`.

Historical Round-Seventeen through Round-Twenty-Three derivations were inspected for reusable arguments.  The useful ingredients retained were the parent-fold current scale, conditional-reference entropy recovery, finite-radius history norms, graph-level coarea, hypocoercive decompositions, strict-topology pullback, and finite-scale phase posterior.  The false minorization, ill-typed renewal product, raw collision-defect graph, deterministic restart, noiseless dominated observation, formal moment propagation, and phase-sensitive leading max-plus claims were not retained.

## 2. Direct counterexamples in the report

### 2.1 A4 complete-past minorization

**Referee objection.**  Finite append/shift steps do not erase the remote exact tail, so transition laws from different tails cannot dominate one common nonzero probability measure.

**Revision.**  The exact-past state is retained, but the theorem is a weak-Harris contraction in the distance
\[
d_*(h,h')=\min\{1,\sqrt{d_\sigma(h,h')[2+W(h)+W(h')]}\}.
\]
The sublevel condition is a Wasserstein small-set estimate, not Doeblin domination.  The proof couples newly generated suffixes while the untouched tail is merely discounted by the shift.  The active source explicitly states that no common dominated measure is asserted.

### 2.2 A4 weighted Lipschitz norm

**Referee objection.**  Dividing by `(1+d)(V+V')` does not impose continuity.

**Revision.**  The active seminorm divides by `d_*`, which tends to zero as histories approach.  The source space for Feynman--Kac perturbations has logarithmic growth relative to `W`; the power drift proves that multiplication by `e^g` acts on one fixed weighted space.

### 2.3 A4 renewal typing and orthogonal dynamics

**Referee objection.**  The old product had incompatible domains, a free mark, and an undefined history `h_x`; stability of `e^{tQLQ}` was inferred incorrectly from full mixing.

**Revision.**  The maps are now
`B(z): flow -> history`, `T(z): history -> history`, and
`A(z): history -> flow`, with stable history represented by a disintegration kernel `eta_x(dh)`.  The identity is
\[
(z-L_{\rm flow})^{-1}=R_0(z)+A(z)(I-T(z))^{-1}B(z).
\]
Orthogonal stability is a separate finite-rank compression theorem relative to the true spectral projection.  The memory expansion is derived under explicit graph-domain conditions
`QLP: R -> D(L_Q^2)` and `PLQ: D(L_Q) -> R`, so the `z^{-1}` and `z^{-2}` coefficients are typed.

### 2.4 B3 collision-kernel counterexample

**Referee objection.**  Every nonzero `h in ker C` produced a zero image, contradicting the claimed null space and closed-range argument.

**Revision.**  Collision defects live in
\[
L^2(A_f^{-1})/\ker\mathcal C.
\]
Each class uses its minimal representative in
`\overline{Ran C^*}`.  Hence `B(0,[h])=0` implies `[h]=0`.  The closed-range theorem is proved from an adjoint localized hypocoercive estimate on this quotient.  The complete adjoint, including the initial output, is recorded in B3 and C2.

### 2.5 B3 stopping-time restart

**Referee objection.**  Conditioning on the complete microscopic phase point gives a deterministic Dirac future, not a regenerated prepared ensemble.

**Revision.**  The process proof uses cut stopping times for the empirical/open-history filtration.  B2's factorial cut algebra gives a uniform `L^p` conditional density of unresolved future roots relative to the prepared root reference.  Conditional connected cumulants follow from the first post-cut vertex.  No full-state stochastic regeneration is claimed.

### 2.6 C1 hidden/observation contradiction

**Referee objection.**  A state complete enough for deterministic hidden evolution also makes noiseless observation deterministic, so it cannot have a smooth conditional density.

**Revision.**  The hidden dynamics remains deterministic, but the observation includes an explicit independent measurement-noise channel with a finite probability envelope.  Pointwise observation density, support, QMD, and log derivatives are derived from the noise density and the deterministic signal map.  Aggregate A2/B1 local theorems are no longer relabelled as point-history observation kernels.

### 2.7 D1 shared policy

**Referee objection.**
\[
\sup_\alpha\max_jG_j(\alpha)=\max_j\sup_\alpha G_j(\alpha),
\]
so the scalar leading limit cannot retain the shared-policy constraint.

**Revision.**  The equality is now a theorem and is explicitly described as phase-blind.  Shared control is retained in the exact finite-scale phase log-sum-exp and in the subleading expansion
\[
V_N=NG_*-\kappa^\dagger\log N+
\log\sup_{\alpha\in\mathfrak A_*}C(\alpha,\mathbf b)+o(1),
\]
where the same policy occurs in every phase coefficient.  A compact relaxed-policy space and a uniform controlled Laplace principle justify the finite-`N` optimization/limit exchange.

### 2.8 B4 high-velocity entropy counterexample

**Referee objection.**  Formal finite entropy need not control the asserted superquadratic moment.

**Revision.**  The microscopic rate is the lower-semicontinuous attainable closure of the original entropy action in the topology in which the microscopic laws are exponentially tight.  On its effective domain the rate equals the same entropy integral; no moment penalty is added to the Hamiltonian.  B2 pressure for truncated collision sources plus a uniform Povzner estimate gives an exponential microscopic containment bound.  The report's formal high-velocity pair is correctly assigned infinite microscopic rate when it has no attainable superquadratic approximation.

### 2.9 B2 grazing constant

**Referee objection.**  Angular integration produces `1/|v-v_*|`, which is not controlled by a polynomial moment.

**Revision.**  The regular root class has a uniform velocity density bound and Gaussian tail.  The relative-velocity convolution is bounded, and `|g|^{-1}` is locally integrable in three dimensions.  This yields a uniform bound on
\[
\int f(v)f(v_*)/|v-v_*|\,dv\,dv_*
\]
and the required grazing estimate.  General attainable paths are reached by regular positive recovery.

### 2.10 B2 loop rank

**Referee objection.**  An analytic determinant ideal can vanish identically; cyclomatic number alone is not geometric rank.

**Revision.**  Round Twenty Seven introduces **causal subtree-shear coordinates**.  For each chronologically ordered surplus edge, the descendant subtree is translated before the closing time.  The full loop Jacobian is block lower triangular; its diagonal block is `+I` or `-I` away from explicit grazing/simultaneous-contact sets.  This proves nonvanishing and simultaneous independence of all surplus constraints, so the per-loop gains multiply without an unverified determinant ideal.

### 2.11 A2 scalar integration by parts

**Referee objection.**  A scalar two-dimensional integral did not prove an anisotropic transfer-operator bound, and bad words left an uncontrolled all-frequency remainder.

**Revision.**  Returned branches are first matched through a common suffix inside the stable-curve pairing that defines the strong/weak norm.  Repeated coarea integration differentiates the actual branch Jacobian, holonomy, test function, and matched-curve coordinate, all controlled by a fixed high-order branch certificate.  A separate terminal nonstationary chart gives every bad word the same `|b|^{-M}` factor.  Four disjoint frequency regimes yield an integrable source-uniform bound.

## 3. Paper-level closure

### A1

The full-product parameter derivative is replaced by a projective finite-cylinder connection.  The derivative of the parameter-dependent tail conditional expectation is present explicitly.  Material derivatives move down a declared Hilbert scale.  Infinite subdivision compatibility is the kernel of a bounded incidence operator.  A dyadic maximal coboundary lemma gives the functional, not merely terminal-time, martingale approximation.  The motivating geometric seam current is proved to satisfy the response-domain tail estimate.

### A2

The active class includes exact integer homology generators, an exact Diophantine roof proof object, coprime periods, high-order branch calculus, returned UNI charts, and terminal nonstationarity for bad words.  The operator proof treats stable pairings, matched curves, four Fourier regimes, source derivatives, and a concrete nonempty algebraic billiard family.

### A3

Excursions use completed-graph topology, which tolerates moving reflection times.  Diffuse weak limits are represented by a relaxed chronological kernel and a normalized graph current rather than by ordering atoms.  Long excursions form a rational-threshold projective inverse limit.  The rate map is defined by a closed history balance and graph compatibility identity.  A renewal local theorem treats random stopping and overshoot; exact continuous conditioning is coarea disintegration; connector cells have a proved uniform lower probability.

### A4

Weak-Harris geometry, fixed-space Feynman--Kac analyticity, typed first/last-return renewal, separately proved compressed semigroup stability, and sectorial memory calculus are now one compatible construction based on the same A3 Lyapunov function.

### B1

Regular blocks occur with a uniform conditional probability and an exponential lower-tail estimate.  Predictable boundary-flat charts handle exterior hard-core surfaces.  One reserve chart gives the exceptional family an integrable high-frequency density, eliminating the old uncontrolled `C_N`.  The grand-canonical pressure is imported before canonical extraction.  Numerator and denominator use separate source-dependent saddles, and exact continuous constraints use coarea.

### B2

The retained state is a precisely defined decorated ordered forest with open half-edges, a factorial/automorphism norm, and an associative fibre-product cut operation.  Causal shears prove loop rank.  A radius-loss Duhamel estimate proves finite-time propagation.  A finite collision-simplex compiler corrects balance while preserving positivity without importing B3.  Exact deterministic tilts and strict convexity give controlled concentration.  Atomic empirical measures use narrow-Orlicz topology; strong `L^1` is reserved for a mollified correlation density.

### B3

The defect quotient removes the infinite collision kernel.  Spatially varying coefficients are handled by a space-time partition and explicit commutator absorption.  Cut-density cumulants replace deterministic restart.  Nuclear compact containment yields the process CLT.  De la Vallee--Poussin uniform integrability and the quotient right inverse close the Mosco theorem.

### B4

The exact microscopic effective domain, source/Povzner containment, temporal `W_2` modulus, varying-reference entropy topology, viscosity comparison, canonical realization map, and BBGKY core convergence are all stated in the active source.

### C1

Independent measurement noise resolves model typing.  The finite envelope integrates to one.  Derivative filtering is performed before normalization.  Finite coordinates remain in a forward-invariant convex shell.  Diagnostic action frequencies and a finite observability Gramian derive the information lower bound.  The BvM proof includes growing local annuli.

### C2

The strict dual is proved for Polish states.  The annihilator contains the initial boundary source.  Periodic localization uses continuous Holder distances and tail cutoffs along complete exposing rays.  Whole-path functionals use a path-augmented prediction process.  Girsanov uses an exponential bracket condition derived from the diagnostic score envelope.

### D1

The Morse--Bott calculation integrates all `m` and `z` saddle coordinates.  The labelled rate is defined before conditioning.  Arbitrary prior phase weights are distinguished from microscopic phase probabilities.  Uniform relaxed-policy compactness proves the control Laplace principle.  Shared control survives exactly where it mathematically can: finite scale, polynomial order, constant order, and labelled outputs.

## 4. Verification artifacts

The branch includes:

- eleven active `ROUND27_POSITIVE_CLOSURE.tex` files;
- eleven `main.tex` wrappers importing only Round Twenty Seven;
- eleven standalone `ROUND27_REVISION.tex` wrappers, rebuilt as individual PDFs by CI;
- `ROUND27_REVISION_DOSSIER.tex`, rebuilt together with the eleven individual PDFs by CI;
- `ROUND27_PROOF_DEPENDENCY_LEDGER.md`;
- `ROUND27_REVIEW_INDEX.md`;
- `ROUND27_SOURCE_MANIFEST.json`;
- `tools/verify_round27.py`;
- `.github/workflows/verify-round27-referee-closure.yml`.

The verifier rejects old Round-Twenty-Three imports, the false exact-tail minorization pattern, the non-Lipschitz denominator, the old renewal ordering, unquotiented B3 collision defects, noiseless dominated C1 observations, and a claim that the leading D1 scalar value preserves shared control.  It also requires the new theorem tokens listed in the review index and checks that all TeX wrappers compile.

## 5. Status for the next review

Round Twenty Seven is a positive reconstruction: it keeps the program's local limits, chronological path LDP, memory, hard-sphere pressure/LDP, kinetic fluctuation and semigroup limits, filtering, rigidity, and coexistence/control conclusions on explicitly defined certified or attainable domains.  All objections enumerated in the Round-Twenty-Six report have an active-source replacement and a regression gate.  Repository verification establishes source identity, internal typing, buildability, and the presence of the claimed repairs; mathematical acceptance remains the responsibility of independent specialist referees.
