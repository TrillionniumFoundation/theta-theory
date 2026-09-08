# Response to the independent referee report on A1 v33

**Revision:** A1 v34, *Attainable information and causal compression at exponent collisions*  
**Author:** Qian Qi  
**Date:** 8 September 2026  
**Controlling report:** `review/a1-english-v33-harsh-independent-2026-09-08`, commit `7643c3532ea9f70eaa3010cd13abcb58c1c31a8f`  
**Reviewed manuscript:** commit `e7dfc3a0e1c8d7a9d3be6b7f52944c5c7c59bb0c`  
**New branch:** `revision/a1-english-v34-attainment-blackwell-2026-09-08`

We thank the referee for distinguishing the surviving mathematical theorem from the remaining editorial judgment. The report finds no fatal counterexample to the examined collision classification, and acknowledges the concrete v33 answers to several earlier objections. This revision acts on the narrower remaining requests. It neither weakens the all-budget collision theorem nor substitutes a collection of execution receipts for its mathematical contribution.

The main article is now organized around the attained collision classification. The controller section is its realization theory, stated at its natural finite-cell generality and located explicitly in comparison-of-experiments theory. All previous proof modules, the exact example, finite compatibility and arbitrary-precision results, and the complete companion remain available. Stable theorem labels are retained; the display title of `thm:v33-moment-program` now records its finite-cell scope.

## R33.1 — The precise Blackwell interpretation

**Action:** incorporated as a proved proposition, not merely a bibliographic addition.

In `v34/moment_controllers.tex`, Proposition `prop:v34-blackwell` defines the auxiliary experiment

\[
\mathsf E_k(dg,dx)=\nu(dg)\{g_k\delta_k(dx)+(1-g_k)\delta_\dagger(dx)\}
\]

and proves exactly

\[
\mathscr A_M(\nu)=\{\mathsf E U:U\text{ is a Borel Markov kernel to }[M]\}.
\]

The proof identifies the accepted term by weighted averaging and requires one shared failure kernel. It also states that the physical observation law conditional on the latent parameter is the mixture \(\sum_k k_k^a(t)\mathsf E_k\). The auxiliary raw-cell index is therefore not an extra observation supplied to the controller after failure.

The proposition derives the support functional as the Bayes reward for a finite decision table and derives the row-overlap bound by pushing the common failure submeasure through the same Markov kernel. Lemma `lem:v33-body` retains its complete compactness and explicit support calculation. Blackwell's 1953 *Equivalent comparisons of experiments* is cited at the point of interpretation and in the main bibliography. The new comparison section separates the classical framework, the acceptance/failure formula, its polynomial iteration, and the attained collision geometry.

## R33.2 — Contribution hierarchy and the common-controller formula

**Action:** follow the report's second stated alternative: make the attained all-budget classification the central contribution, and present the exact controller algebra as realization theory.

The title, abstract and introduction now lead with the collision-uniform theorem, its acquisition-dependent truncation, the simultaneous acquired-mass flags, the whole-image cover and the common causal realization. The persistent-bit envelope, collision-tree allocation formula, and intersecting-locus example are presented as substantive consequences of that theorem. These are retained results, not newly claimed v34 theorems.

The exact finite program remains in the main article, with its full proof and parameter counts. Its interpretation is explicit: it is an attained representation over a compact coefficient domain, not an efficient global algorithm or a classification of all optimal label allocations. The fixed coefficient integral \(B_n\) can still be costly. We do not claim a sharp finite-budget causal price, an optimal transition-partition phase diagram, or a new multi-checkpoint optimization theorem.

The continuous-command \(N=M=2\) example and its analytical global lower bound are preserved without alteration. It is described as an exact original-model realization example. Since it has only one acquisition checkpoint, it is not offered as evidence of a multi-checkpoint trade-off. No extra decimal precision has been substituted for that distinction.

## R33.3 — The experiment-level content of the collision law

**Action:** the introduction and the first subsection of `v34/comparison.tex` expose the theorem's logical dependencies.

The comparison distinguishes four necessary steps. Classical confluent interpolation supplies test coordinates, but not the attainable product tangent. A generic rectangle quantization bound supplies a conclusion conditional on a rectangle, but not actual acquisition mass. A local attained chart supplies a lower bound, but not a cover over every report word. Separate checkpoint covers do not alone supply one causal state process.

The article now attaches these gaps to the corresponding proved inputs: `lem:binomial-tangent`, `lem:newton-attainment`, `lem:tame-rectangle` and `thm:intrinsic-checkpoint`, followed by `thm:intrinsic-streaming`. The distinction between command density and a possibly singular latent prior is visible. The failure evidence remains in the unconditional minorization. The normalization argument loses exactly one rank; it is not an ambient-dimension assertion.

The classical status of total positivity, divided differences, real entropy bounds, quantization and filtering error recurrences is stated in the main text. The inherited nonlinear-filter comparison, including the distinction between signal-grid size and the number of posterior labels, informs that text rather than being left only as a companion qualification. The detailed v33 comparisons with action quantization, team approximation and observation-channel continuity are retained. The revision does not claim that these different theories are subsumed, or that an exhaustive priority search has been completed. Whether the resulting central theorem has the distinction required by the intended journals remains an editorial assessment; it is not certified by the revision itself.

## R33.4 — Generality and quantifier boundaries

**Action:** the finite-cell generality observation is now a theorem-level extension with the corresponding proof changes.

The revised controller section starts on an arbitrary standard Borel latent space with any probability measure and finitely many nonnegative Borel cells summing to one. Acquisition remains prescribed and independent. The full necessity-and-sufficiency recursion, finite-moment centroid formula, compact attainment and purification proofs are given at this scope. Strict positivity of individual cells is not needed for these algebraic conclusions.

In the baseline integral, zero evidence is handled explicitly: \(0\le\mu(LH)\le\mu(L)\), so \(\mu(LH)^2/\mu(L)\) extends by zero and is bounded by \(\mu(L)\). Zero occupancies retain the continuous perspective convention. Every prior-dependent coefficient still uses moments of cell products through degree \(N\). No uniform denominator bound is asserted for this generalization.

Proposition `prop:v34-evaluation` identifies the filtered cell-product space and proves \(\mathcal F_m(k^a)=W_{mA}\) in the monomial specialization. It expressly does not infer acquired rank from formal coefficient counts. Proposition `prop:v34-two-cell` gives a positive two-valued, nonmonomial experiment: its future test algebra has dimension two, and a directly calculated nonzero posterior-weight derivative gives a one-dimensional attained interval when the menu contains a distinguishing query. This illustrates which assertions are algebraic and which require the monomial tangent.

The final controller subsection explicitly returns to the positive compact monomial family before stating collision continuity. The main collision theorem is unchanged. The following boundaries occur beside their conclusions in the abstract, introduction or controller text: fixed prior/detector/horizon; prescribed acquisition for the controller-independent offset; mean-vector, not worst-history, purification; no removal of a persistent public seed; scalarization without a minimax exchange; fixed-\(M\) compact transfer versus the separate all-budget geometry. Equation `eq:v34-ties` specifies strict inequalities against lower-index competitors and weak inequalities against higher-index competitors, so atomic mass on ties is not discarded.

## R33.5 — Preservation and reproducibility

**Action:** preserve the complete source tree and report execution at its actual scope.

The new manuscript directory is based on the complete reviewed directory tree `97a03f2e39f5192aaac2a0009ffd5e85e1e70567`. The old v33 directory is untouched. Within the new directory all old modules remain; the new main entry selects the revised introduction, controller, comparison and bibliography. The old main and README are also retained as named baselines. `companions.tex` and every underlying companion module are inherited unchanged. No theorem proof is deleted to create an appearance of concentration.

The included exact-arithmetic diagnostics exercise the Blackwell support formula, common-submeasure overlap, formal occupancy identities and all three checkpoint risks in two finite-cell experiments, including zero evidence and zero occupancy. They also test the atomic tie convention and the two-cell derivative. Normal and optimized Python executions give byte-identical output. These tests are not global controller optimization or formal verification of the general proofs.

Changed-module TeX smoke compilation includes the new abstract, introduction, controller section, comparison and bibliography. External labels use explicit test stubs, and the unchanged main theorem is represented by a test marker in that harness. Its successful compilation and layout inspection are **not** represented as a full two-volume build or complete native cross-reference verification. The native build entry remains available in the complete checkout. Inherited v33 build receipts remain historical evidence, not newly executed v34 receipts. `VALIDATION_V34.json` and `v34/SMOKE_RECEIPT.json` record this separation.

## Earlier objections retained as closed or substantially answered

The revision does not reopen the already answered precision-versus-rate issue (R32.1), the concrete history-indexed-variable issue (R32.2), the original-model admissibility objection (R32.4), or the earlier absence-of-delivery objection (R32.5). The theorem-level finite-approximation comparison answering R32.3 is retained. We distinguish the report's closure of those concrete objections from its still adverse overall publication recommendation. No acceptance or external endorsement is asserted.
