# Response to the v72 external report — A2-DYN v73

Controlling report: `reviews/a2-dyn-v72-external-top4-review-2026-10-11/REFEREE_REPORT.md`, at `fad5823b36f2c68595c6b17bebf62c70032d30a9`; report blob `f10920ea44a658b3b0ab75eac1f1d910a0946417`. Reviewed author manuscript: `295800b658aa2ff3aada1707d5785ff757d60724`, paper tree `bd761b97e603b666ed97b27241f9ab83c7f2550b`.

We thank the referee for separating the valid full-source construction from the missing collision-uniform estimate. The revision keeps the original exact-return problem. It proves an additional property of the complete physical source, strengthens the local-flux comparison, and makes the scalar-to-path implication explicit. We have not replaced the desired pointwise law by an interval law, changed the billiard family, normalized a zero arithmetic class, or removed a physical remainder. The four new modules are 160–163; the preceding 159 modules remain unchanged and compiled.

## 22.1. Decay of the complete current excess

The new Lemma `lem:v73-paired-flux` proves, for the full nonnegative BV density,

\[
[b-2A_\delta b]_+(t)\le\min\{(Db)^+([t-\delta,t]),(Db)^-([t,t+\delta])\}.
\]

This improves the available sufficient quantity, rather than simply renaming the old sum of directed variations. An isolated entrance or exit atom can leave the old directed supremum positive while the paired quantity is zero. A narrow positive pulse still has positive excess and is retained. The proof compares the left and right averages separately and uses their nonnegativity. The Jordan parts belong to the complete physical current after all legitimate interface cancellations.

The reserve is the constant two. Thus its cost is compatible with the required `K(B) B^(-1/192) -> 0`, with no collision-dependent band. Theorem `thm:v73-paired-budget` gives

\[
\mathcal E_M\le C_M B^{-1/192}+\mathcal P_{\varepsilon(B)}(\delta(B)).
\]

The desired uniform decay of the last term is not proved in this revision. Its power-bound hypothesis is labeled as a hypothesis, and its scale substitution is displayed explicitly. Corollary `cor:v73-central-excess` also proves a two-sided comparison between the central excess and the original scalar error; localization is only to the central set already present in the original theorem. No physical state or exact label is removed. This request has substantive new estimates but is not reported as a completed uniform decay theorem.

## 22.2. The full current as a finite measure

Theorem `thm:v73-full-source-bv` now proves this for the complete original scalar source at every fixed collision count, uniformly in radius, guard width and exact labels at that count. It does not assume it from wordwise BV or from a distributional exhaustion.

The proof first writes the unchanged smooth cutoff as an exact Stieltjes threshold integral. A signed Stieltjes measure is allowed, so monotonicity or definability of the original smooth cutoff is not silently assumed. Each threshold source is positive and dominated by the old complete finite-count density. Its sublevel mass is constructible by parameterized integration on the original two-dimensional initial chart. Auxiliary collision variables are used to establish the physical graph, not integrated with ambient volume on that graph. The roof derivative is definable; the argument does not need closure of the constructible algebra under differentiation. Uniform o-minimal monotonicity at each fixed count gives a finite number `J_m` of monotonicity pieces. Distributional integration against the finite signed threshold measure yields

\[
\|Db\|_{TV}\le4(J_m+1)(CA^m/c_*)\|d\Theta\|_{TV}^{2m+1}.
\]

This includes first incidence and first clearance outside the selected disks. Exactly one inherited status flag changes: the full-source finite-measure flag. There is no bound on the growth of `J_m` or on `m^2 C_m`; the collision-uniform flux part of the request remains quantitative. The theorem does not assert BV for arbitrary bounded marks or for capacity-allocated weights.

## 22.3. The original unconditional pointwise theorem

Equation `eq:intro-v73-target` keeps the original normalized exact-label density, the same central target and the finite arithmetic transition kernel through zero classes. The leading theorems state finite BV, paired flux and equality of scalar/path errors; they do not relabel an averaged theorem as a pointwise one. Completing the original scalar theorem still requires uniform decay of the paired flux or directly of the equivalent central excess. The manuscript states this precisely after the leading theorems and in the proof ledger. The mathematical target has not been reduced or changed.

## 22.4. Marked numerators, same-roof bridges and forward likelihood

Theorem `thm:v73-scalar-path-equality` proves a new exact equality of ordered errors on the inherited common positive path-remainder theorem. With `Pbold-G W = bbold_B+Ebold_B` and `bbold_B` positive, one has on the common versions

\[
|P-G|\le\|\mathbf P-G\mathsf W_R\|_{BL^*}\le|P-G|+2\|\mathbf E_B\|_{BL^*}.
\]

First take the collision limit at fixed `B`, then let `B` grow. The ordered path-numerator error equals the scalar error. A separate vanishing-height theorem for each bounded-Lipschitz numerator is therefore unnecessary **on that inherited input chain**. The new result does not independently reprove the spectral input, cylinder inversion or variation tightness; their audit remains necessary.

On `G>=d>0`, the common scalar lower bound gives `P>=d/2` once the scalar error vanishes. The corollary proves the conditional bounded-Lipschitz bound and both scalar density ratios. For the original window-normalized forward arithmetic likelihood it gives `||dP/dQ-1||_infinity <= 2r/(1-r)`, where `r=||P-G||_infinity/d`. The inherited collision-to-return clock transfer is retained. Neither a path-space total-variation theorem nor normalization on a zero class is asserted. These endpoint consequences remain conditional on the scalar decay, not fulfilled by finite BV alone.

## 22.5. Common versions and physical interfaces

Module 160 constructs one finite source kernel `D_t=p(t)Q_t`, supported on the original roof fiber, before defining weighted densities and path numerators. Chosen Borel physical weights are integrated against this same kernel. It verifies the complementary capacity weights, including the `r=0` convention. It distinguishes simultaneous evaluation of actual weights from an invalid simultaneous choice of representatives for every measurable equivalence class. A countable bounded-Lipschitz norming class fixes the path exceptional set. The order is `sup_R ess_sup_t`; no uncountable union of radius-dependent null sets is taken.

Proposition `prop:v73-interface-ledger` gives the two oriented patch fluxes. Matching artificial cuts cancel before Jordan decomposition; true source jumps, physical itinerary boundaries and exact-event boundaries are retained. The full window derivative includes both the entrance and negative exit atoms. The full current is now finite by module 161, but convergence of arbitrary patch exhaustions in total variation is not inferred. The notation `e70` is explicitly first clearance outside the selected disks, with incidence separate; the older opening is retained with this clarification.

## 22.6. Independent specialist audit

No independent human audit is represented as having occurred. `independent_human_review` and `formal_proof_certificate` remain false. `SPECIALIST_AUDIT.md` identifies the requested specialist checks, including the semialgebraic physical graph, parameterized integration, full-count density input, occupation spectral chain and common path remainder. Numerical fixtures and native TeX qualification are not evidence that these infinite-dimensional arguments have been independently certified.

## 22.7. Mathematical breadth without changing the problem

The revision does not switch to a nonsingular model or present an abstract criterion as a realization of the original endpoint. The source-specific addition is a finite-measure theorem for the complete original Lorentz source with its actual smooth guard. The paired-flux lemma and positive-kernel error comparison have general statements, but their application here retains the original geometry, source and arithmetic. Previously retained Markov realizations remain in the archive; no new independent realization is claimed. The broader completion request is not substituted for the original unresolved quantitative estimate.

## 22.8. Reading route and preservation

The revised opening has three leading theorems with proofs pointing to four consecutive new sections. `JOURNAL_ROUTE.md` gives a short first-reading route and separates the necessary inherited inputs from historical derivations. Every prior core proof is still compiled in the unchanged order; the old opening is compiled as a historical appendix. Exact snapshots and deterministic extraction avoid rewriting the archival chain by hand. The full manuscript remains a large proof archive; this organization is not represented as a completed submission-length reduction or journal acceptance.

## 22.9. Theorem-level literature comparison

The standard disintegration step in module 160 is not claimed as a new general theorem. The source-specific content is the common physical allocation and interface accounting. In module 161, Cluckers–Miller, Theorem 1.3, supplies parameterized integration; Coste supplies fixed-formula monotonicity; the distributional BV characterization is standard (Ambrosio–Fusco–Pallara). None supplies the Lorentz height bound, the collision-uniform growth of `J_m`, or the requested local limit theorem. The exact original-guard threshold representation and its full-source application are the additional argument here.

Module 162 proves its elementary two-sided inequality in full and explains why it is strictly less demanding than the prior directed-sum bound for isolated atoms. Module 163 derives the scalar/path error equality directly from the inherited positive remainder, not from an external conditional local-limit theorem. The earlier comparisons with Szász–Varjú, Dolgopyat–Nándori and the billiard spectral literature remain in modules 75 and the retained bibliography. Their hypotheses are not declared to imply the present unrestricted four-component exact-label pointwise endpoint without the missing physical estimate.

## Qualification and handoff

The workflow checks the exact reviewed tree and report blob, byte preservation of all inherited mathematical inputs, all 163 actual TeX core inputs, rational sign/capacity/path fixtures in ordinary and optimized Python, the six inherited finite checks, stabilized references and rendered page geometry. The exact checkout SHA is included in every evidence record. Passing this workflow means source and typesetting qualification only. The next referee is asked to examine the new finite-BV proof, the paired-flux strengthening and the scalar/path equivalence, while retaining the original uniform endpoint as the remaining mathematical objective.
