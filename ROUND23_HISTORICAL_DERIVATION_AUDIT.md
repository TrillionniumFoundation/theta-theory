# Round-Twenty-Three historical derivation audit

**Purpose.**  This audit records which earlier derivations were reused, which mechanisms were rejected after the Round-Twenty-Two counterexamples, and which new mathematical tools were introduced.  It is a provenance document, not an argument that age or volume of prior material establishes correctness.

## Materials reviewed before reconstruction

The active revision was prepared after examining:

- `REFEREE_REPORT_ROUND22_GPT56_PRO_HARSH.md` — controlling external report;
- `ROUND21_HISTORICAL_DERIVATION_AUDIT.md` — earlier source map;
- `ROUND21_PROOF_DEPENDENCY_LEDGER.md` — earlier cross-paper order;
- `ROUND21_INTERNAL_HARSH_REREVIEW.md` — internal counterexample checklist that failed to detect several later external counterexamples;
- every Round-Twenty-One `ROUND17_POSITIVE_CLOSURE.tex` active-slot source;
- the earlier author responses and bibliography sets;
- the Round-Twenty-One verifier/workflow, whose structural checks were retained only where they remained mathematically meaningful.

The internal rereview was particularly informative negatively: it showed that a long list of named “attacks” and successful compilation did not prevent errors in normalization, state sufficiency, operator algebra, and topology.  Round Twenty-Three therefore converts the referee's explicit examples into executable identities and changes the active source filenames so that a new proof cannot be mistaken for another patch in a legacy slot.

## Reuse/reject/rebuild table

| Paper | Earlier material retained | Mechanism rejected | Round-Twenty-Three rebuild |
|---|---|---|---|
| A1 | labelled suspension, positive-test/dual-current principle, fixed-fibre transport idea | automatic exponential cylinder rate for a Hilbert completion; untyped `integral J dmu`; covariance by coordinatewise claims | three-layer type system: geometric fibre, measurable current observable, explicit projective response domain; Bochner mean; Hilbert projective martingale proof |
| A2 | finite-horizon inducing, anisotropic operator platform, physical roof variable, four-dimensional inversion target | real determinant as arithmetic certificate; two returned points as independent variables; branch mass as a derivative norm | periodic closed-subgroup annihilator; exact integer generators and irrational roof pair; original-section two-coordinate coarea; weighted branch derivative sum |
| A3 | complete-past kernel, entropy-control strategy, terminal/recession motivation | unordered transition occupation as path state; representative atoms; uniform return-count lower bound; cylinder insertion for an arbitrary path functional | chronological marked point measure with full excursion paths; conditional-reference quantisation; one-big-excursion recession; finite-memory exponential approximation |
| A4 | history kernel, Lyapunov/Harris strategy, Feynman--Kac sources, renewal and projection programme | uniform truncation of a Lyapunov tail; arbitrary moment observable in spectral space; formal renewal types; regular-point residue; false `z^-2` memory cancellation | distinct mark-size and influence scales; weighted Lipschitz rough paths; typed entry/exit maps; closed block Schur--Feshbach memory with correct `z^-1` term |
| B1 | exact-number coefficient objective, mixed lattice/continuous inversion, block smoothing idea | unnormalised factorial pressure; post hoc “good block” selection; boundary extension without flatness; marginal covariance after lattice conditioning | probability reference/explicit ideal-gas subtraction; deterministic label blocks; adapted flat atlas; full joint covariance and Schur conditioning |
| B2 | Green contact trace, precontact coordinates, connected graph expansion, positive collision controls | moments as grazing trace regularity; named singular list as exhaustive; no regular surplus factor; finite-time concatenation on `(f,Gamma)`; LMGF-to-LDP shortcut | `L^p` regular trace and entropy density; determinant ideal; transverse loop opening; open-half-edge history hierarchy; exact tilted concentration and recovery |
| B3 | collision form, hypocoercive goal, nuclear fluctuation space, Mosco objective | local positivity promoted to global gap; Fredholm language beyond the estimate; reduced-state Markov restart; Hessian in separate `A` and `Gamma` logarithmic coordinates | global Maxwellian comparison; closed range modulo explicit invariants; full microscopic restart; normal collision defect and exact zero-manifold Hessian |
| B4 | controlled Boltzmann action, Nisio DPP, nonlinear implicit resolvent idea, BBGKY correctors | quadratic topology on a second-moment shell; weak-to-strong transfer; product collision convergence by assertion; maximal dissipativity as comparison | superquadratic `W_2` shell; synchronous transfer; truncation proof for product kernel; explicit viscosity core, containment and comparison |
| C1 | unnormalised filter philosophy, stratified observations, risk-sensitive DPP, finite statistical approximation, LAN goal | common hidden-state domination; aggregate LLT as conditional density; pointwise Bayes continuity at zero evidence; retraction into nonconvex reachable set; compact-policy information lower bound | deterministic push-forward prediction; observation-only domination; inserted conditional density proof; integrated numerator inequality; convex belief reconstruction; persistent excitation |
| C2 | strict-duality goal, form-level compression, rigidity, optional projection and innovation programme | bespoke strict sequence criterion; omitted collision adjoint; direct pressure-to-periodic inference; weak path convergence to conditional laws/brackets; nonnegative likelihood as Brownian exponential | exact pullback of standard strict topology; complete adjoint; equilibrium localisation plus Livsic; prediction-process/UT theorem; strict positive equivalence |
| D1 | genuine microscopic phase cells, component beliefs, common-policy principle, complex phase and Gaussian-mixture goals | LDP-derived polynomial weights; unproved phase conditioning; compact-only separation; componentwise optimiser inside log-sum; globally assumed zero-free dominance | source-inserted local normal form and Morse--Bott weights; `I`-continuity cells; exponential-tightness separation; posterior Bellman state; Rouche under a proved gap |

## Historical derivations that materially helped

### A-series

The labelled suspension and the “trace on tests, transpose to currents” discipline from A1 remain useful and are preserved.  The A2 inducing/anisotropic framework identified the right variables for the joint lattice--roof theorem.  A3's insistence on the complete physical excursion and A4's complete-past kernel were also correct strategic choices.  The revision does not discard these platforms; it repairs the source/target spaces and the missing quantitative estimates.

The decisive new observation is that the same history needs two unrelated weights.  A Lyapunov weight measures how large a remote mark is, while hyperbolicity measures how strongly that mark can still influence the present.  Conflating these was the source of the A4 truncation error.  The ratio `theta/rho` is now the small parameter, not the tail of the Lyapunov sum itself.

### B-series

Earlier collision-tree and precontact materials supplied the spanning-tree coordinates used by the new loop-opening lemma.  The referee's objection showed that a singular-small-set estimate alone cannot control regular surplus contacts.  The new tool solves tree contacts first, then treats every independent loop as a genuinely additional tube condition.  This produces a positive power of the diameter after the Boltzmann--Grad cross-section has already been cancelled.

The earlier finite-time ambition also highlighted exactly what the interface state must retain.  A density/contact pair cannot encode collision correlations crossing a cut.  The new state is the complete factorial history hierarchy with open ancestral half-edges, so time-slice composition is an exact gluing operation.  B1, B3, and B4 are rebuilt downstream of this hierarchy rather than assuming it away.

### C/D-series

The use of unnormalised filters was retained because it leads to the integrated ratio inequality that controls zero evidence.  What was removed was the attempt to dominate the deterministic hidden map.  The hidden state is now pushed forward exactly; only observations are integrated against a reference measure.

The earlier phase-posterior idea in D1 was also retained.  Its missing input was subexponential information.  The new Morse--Bott calculation begins with the source-inserted local coefficient already proved upstream, so the phase exponent, Gaussian normal determinant, minimizer-manifold volume, lattice powers, exact-number saddle, and conditioning factors all enter one coefficient.

## Newly created tools and why they were needed

### 1. Projective current response norm

A Hilbert space describes square summability, not a geometric approximation rate.  The new response norm adds the exponential conditional-expectation tail as a separate term.  It both states the correct domain and supplies the summable projective series used by the FCLT.

### 2. Periodic-data annihilator design

The arithmetic problem is a closed-subgroup problem, not real linear algebra.  The revision designs a finite periodic certificate that kills the continuous character first, the lattice character second, and the constant phase last.

### 3. Conditional-reference entropy quantisation

A finite approximation to a non-atomic controlled kernel must remain absolutely continuous.  Conditioning the reference kernel inside each partition cell gives exactly the desired cell probabilities and makes the recovered KL equal the coarse KL.

### 4. Loop-closure determinant ideal

A fixed named catalogue of singular collision geometries is not stable under graph complexity.  The sum of squared maximal minors gives one analytic object whose small sublevel controls every rank-loss mechanism on a chart.  It is combined with regular coarea rather than used in its place.

### 5. Defect-coordinate Hessian

The collision action is zero on the manifold `Gamma=A_f`.  Its correct normal coordinate is therefore the difference between the actual collision-current tangent and the tangent induced by changing `f`.  This turns the referee's counterexample into the defining invariance of the quadratic form.

### 6. Integrated Bayes continuity

Pointwise posterior ratios are unstable when evidence is small.  Multiplying the posterior error by its evidence yields an estimate solely in terms of unnormalised numerator/evidence errors, which converge in `L^1`.  This makes the zero-evidence convention immaterial.

### 7. Prediction-process transport

Conditional laws and brackets are not continuous functions of an ordinary weak path law.  The revision makes the prediction process and semimartingale characteristics part of the convergence interface, which is exactly the information needed by downstream stochastic integrals and BSDEs.

### 8. Local-to-phase coefficient transfer

An LDP loses all polynomial factors.  The new transfer keeps the local amplitude through a tubular Morse--Bott expansion and records the precise exponent and determinant integral before any phase contraction.

## Sources deliberately not promoted to active proofs

- `ROUND17_POSITIVE_CLOSURE.tex` and all earlier active-slot files remain historical only.
- `ROUND21_INTERNAL_HARSH_REREVIEW.md` remains evidence of an internal check, but its PASS is not inherited.
- JSON certificates and build records remain reproducibility evidence, not mathematical lemmas.
- References to established literature identify standard platform inputs, but no citation is used to replace a model-specific interface that the downstream proof needs.

## Active-source provenance

Every paper now contains:

1. `ROUND23_POSITIVE_CLOSURE.tex` — active mathematical source;
2. `main.tex` — wrapper naming `ROUND23-REFEREE-POSITIVE-CLOSURE` and importing that source;
3. `AUTHOR_RESPONSE_ROUND22.md` — paper-specific response;
4. existing prior sources and responses — unchanged historical record.

The full source identity and dependency requirements are machine-checked by `tools/verify_round23.py`.  Clean PDFs and cryptographic hashes are generated only after the active-source and regression gates pass.

## Audit conclusion

Historical material was valuable where it supplied a correct platform or exposed a dependency.  It was not treated as authority when the latest report produced a counterexample.  Round Twenty-Three keeps the positive programme but replaces every refuted shortcut by a new type, state variable, normalization, compactness mechanism, geometric gain, or limiting theorem.  The resulting branch is intended for a fresh independent review; this audit does not pre-judge that review.
