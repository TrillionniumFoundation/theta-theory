# Independent referee-style report on A2 v30

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Author branch:** `revision/a2-v30-complete-native-submission-top4-2026-09-12`  
**Reviewed commit:** `46f4b1dc2f9609963cae6a80b3a0f458d88250e1`  
**Reviewed tree:** `3f0e5d977e7fd85a71b246d72e893c1959e4cc09`  
**Previous review / parent:** `8582aa1839dad65ae370e0920e94d7cfe5b1dfa4`  
**Native entry:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Review branch:** `review/a2-v30-external-harsh-top4-2026-09-12`  
**Date:** September 12, 2026.

This is an author-requested, AI-assisted independent referee-style assessment against the standards sought for Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, and Acta Mathematica. It is not a commissioned report, an editorial decision, or a representation of affiliation with those journals. The reviewed object is the immutable A2 source above. Source labels, rather than unverified manuscript PDF page numbers, identify the mathematics. The accompanying [source audit](SOURCE_AUDIT.md) distinguishes direct readings, executed finite diagnostics, inherited evidence, and work not performed.

## Recommendation

**I do not recommend acceptance of the assembled submission on the evidence presently available. The new measurable-coupling lemma is correct under its stated hypotheses, and its use in the stopped physical comparison is justified. No new fatal mathematical counterexample was established. Nevertheless, v30 has not supplied the complete native-main verification requested under C2. The appropriate disposition is return for completion of that submission package and renewed assessment of the assembled article, not an automatic demand for another major mathematical reconstruction.**

The qualification is substantive. Approval of a 75-line measure-theoretic insertion does not certify all inherited forward estimates, statistical limit theorems, global acquisition arguments, and auxiliary mathematics. Conversely, the absence of a verified complete build is not a proof that one of those theorems is false. Neither a version number nor a sequence of favorable module-level reports substitutes for a complete, inspectable article or establishes exceptional mathematical significance.

| Issue | Finding in this review | Disposition |
|---|---|---|
| V30 physical measurable coupling | Explicit measurable overlap/residual construction; correct handling of injective physical embeddings and the failure atom | Technical addition accepted |
| Adaptive success-weighted comparison | First-disagreement bound and predictable-success identity remain valid for the stated capped policies | No new objection |
| T1: off-model fixed-anchor equivariance | Transported-anchor extension re-examined; the old witness does not refute the new convention | Remains closed |
| C1: common-orientation classification | Quotient/equivariance step re-examined under its inherited signed-classification hypotheses | Remains closed at that scope |
| Fixed-policy stopped-history hierarchy | Retained designs, failures, terminal censoring and stopping information are distinguished from a changed acquisition policy | Remains closed |
| C2: complete native submission | No new complete-main evidence in the four-file revision; inherited verification expressly leaves this open | Open |
| Revision identity and navigation | Main activates v30, but both principal README entries still identify v29 | Integration correction required |

“Remains closed” is not a new independent certification of every dependency of the earlier result. This review establishes no basis for reopening those particular objections. [S1–S4, S8–S11]

## 1. What was actually revised

The authenticated comparison from the previous review head to the reviewed commit has one new commit and no divergence. It lists four changed paths: the new 171-line adaptive section, the new 75-line coupling lemma, a one-line input replacement in `main.tex`, and the preserved 125-line previous main entry. No file is deleted. Thus v30 is a bounded measure-theoretic addition to the inherited complete entry, not a newly verified reconstruction of the whole submission. [S1]

The active `main.tex` has 50 literal direct inputs. Its new adaptive input, in turn, inputs the coupling lemma. The locally materialized main and lemma were checked against their authenticated Git blob identities; both matched exactly. This confirms the object examined and the activation of the new mathematics. It does not check the full recursive dependency graph. [S2; `source_identity_checks.json`]

The root README and manuscript README still announce v29 and point to v29 response and verification files. The four-file v30 delta contains no new point-by-point response or complete-main verification record. This should be corrected before another submission is represented as integrated. The stale navigation does not justify ignoring the active v30 source or accusing the author of a mathematical inconsistency. It does prevent a reader from treating the repository's entry pages as an accurate guide to the latest revision. [S1, S3]

## 2. The new measurable-coupling lemma is sound

### 2.1 Construction, marginals, and the degenerate branch

Lemma `lem:v30-physical-coupling` starts with the same fixed scalar space in both models,

\[
K_\partial=K\sqcup\{\partial\},\qquad
\nu=\operatorname{Leb}_K+\delta_\partial,
\]

jointly measurable probability densities \(f_{\xi,a},g_{\xi,a}\), and a jointly measurable physical embedding \(\iota_{\xi,a}\). For each parameter/design pair this embedding is a Borel isomorphism onto a Borel image and sends the failure point to the common failure symbol. These hypotheses are enough. In particular, no common ambient density on the space of planar records is needed. [S4]

Suppress the indices and write \(h=\min(f,g)\), \(m=\int h\,d\nu\). The manuscript constructs a measure on the physical product space by a diagonal overlap term and an independent residual term:

\[
C(D)=\int 1_D(\iota x,\iota x)h(x)\,d\nu(x)
 +\frac{1}{1-m}\iint 1_D(\iota x,\iota y)
 (f-h)(x)(g-h)(y)\,d\nu(x)d\nu(y).
\]

The second term is defined to be zero when \(m=1\). Both residual measures have mass \(1-m\). Their normalized product therefore has mass \(1-m\), not \((1-m)^2\); the displayed denominator is correct. Integrating out either coordinate yields the corresponding residual marginal. Adding the overlap gives exactly \(P=\iota_*(f\nu)\) and \(Q=\iota_*(g\nu)\). When \(m=1\), the densities agree almost everywhere and the diagonal term alone is the required probability coupling. The failure mass is included in this calculation, not subsequently inserted without normalization.

### 2.2 Joint measurability and maximality are different requirements

For every Borel set \(D\subset Y^2\), the integrands are nonnegative jointly measurable functions of the parameters and integration variables. Parameterized integration makes the overlap mass and both contributions measurable. The reciprocal on \(\{m<1\}\), with the declared zero branch on \(\{m=1\}\), is measurable. Standard Borelness of \(Y\) also ensures that its diagonal is measurable. Thus this is a probability kernel, rather than a collection of pointwise couplings with an unproved measurable choice. [S4]

Maximality uses the stronger embedding hypothesis. The two residual measures are carried by the disjoint scalar sets \(\{f>g\}\) and \(\{g>f\}\). Injectivity keeps their physical images disjoint, so the residual term gives no diagonal mass. The disagreement probability is \(1-m\). At each fixed parameter, the Borel inverse makes the image of \(\{f>g\}\) measurable; the difference of its marginal probabilities is also \(1-m\). Therefore

\[
\|P-Q\|_{\rm TV}=1-m.
\]

No jointly measurable family of inverse maps or Hahn-set selections is needed for this last lower bound: it is an equality verified at each fixed parameter. The joint kernel was already constructed in the forward direction. This distinction is correctly handled in the new proof.

Injectivity must not silently be removed from the equality claim. Under an arbitrary later observation map, only total-variation contraction is automatic: two distinct atoms can be mapped to the same point. V30 uses equality for the embedding and contraction for subsequent common coarsenings. That is the correct division of labor. The basic maximal-coupling mechanism is classical; compare [L1]. The useful addition here is the explicit measurable realization for the manuscript's physical kernels, not a new general coupling principle.

### 2.3 A parameter-dependent proof device is not an observed parameter

For the billiard application, scalar coordinates consist of the two transverse endpoints and residual time, together with failure. The finite and boundary densities use the same scalar box. At a fixed table, the same contact graphs embed both laws into physical positions. The inverse is transverse projection in those contact frames, with time and labels unchanged. Countably many discrete flight and channel components can be combined without losing measurability. [S4, S5]

It would be a mistake to reject this proof simply because the embedding depends on the unknown table. A coupling used to bound the distance between two laws at the same parameter need not be an executable parameter-free simulator. The resulting laws already live on the specified common observation space. The last paragraph of the new source states this distinction explicitly.

It would be an equally serious mistake to use this construction to compare physical densities on two different unknown boundaries. For illustration, the same scalar law on \(0<u<1\), mapped by \(u\mapsto(u,\theta u^2)\), has disjoint successful images for distinct \(\theta\). Their total variation can be one while their scalar laws coincide. This is a measure-theoretic illustration, not a counterexample within the manuscript's billiard class. It explains why same-parameter finite-to-boundary comparison and cross-parameter information loss must remain separate.

There is one minor wording improvement: “the supplied contact graphs” could read “the contact graphs defining the forward model.” The current wording may momentarily suggest that the observer is supplied the unknown graphs. The subsequent explicit disclaimer prevents this from becoming an actual oracle assumption; it is not a new theorem-level objection.

## 3. The stopped comparison retains the right experiment and budget

### 3.1 First disagreement, not an iid argument at a random sample size

Lemma `lem:v16-kernel-comparison` uses one parameter-independent policy, common auxiliary randomness, a deterministic preparation cap, and a transcript retaining every design, failure and stopping decision. While the two histories agree, both policies make the same next decision. Coupling the next observations maximally then bounds the first disagreement at step \(i\) by the one-step error at its common design. After disagreement each marginal continues according to its own rule. [S6]

For any nonnegative measurable bound \(e_\xi(a)\), summation gives

\[
\|\mathsf P_\xi^\pi-\mathsf Q_\xi^\pi\|_{\rm TV}
\le \min\left\{1,
E_{\mathsf P_\xi^\pi}\sum_{i=1}^T e_\xi(a_i)\right\}.
\]

Replacing the indicator of agreement before step \(i\) by one yields the expectation under the physical marginal. Interchanging the marginals gives the analogous expectation under the boundary law. No independence of the adaptive designs is used, and there is no claim that observations become iid after conditioning on completion of a random acquisition procedure. The newly supplied measurable coupling closes the technical existence assumption for the physical application.

### 3.2 Why the error is weighted by successes

The inherited physical theorem supplies

\[
e_\xi(a)=C p_\xi(a)\tau^{j(a)},
\]

not merely the conditional successful-record bound \(C\tau^{j(a)}\). The event \(\{T\ge i\}\) and the next design are known before the fresh observation. Thus

\[
E_P\sum_{i=1}^T p_\xi(a_i)\tau^{j(a_i)}
=E_P\sum_{i=1}^T Y_i\tau^{j(a_i)}.
\]

This predictable-success identity is valid for the stated finite cap. If all flights are at least \(J\) and the policy stops no later than its \(k\)-th success, the realized weighted success count is at most \(k\tau^J\). The raw preparation cost remains \(T\), including failures. Conflating this error budget with a cost of only \(k\) preparations would invalidate the statistical interpretation, but the current source does not do so. [S5, S6]

The pilot corollary also has the right structure. The exact pilot is coupled identically in both models. On its good event the collar hypotheses permit the post-pilot comparison; on bad histories a specified completion is allowed and charged by their probability. The good-pilot indicator is measurable before each subsequent observation, so the same success identity applies. A bound of the form \(\eta_0+C E_P[1_{\rm good}\sum Y_i\tau^{j_i}]\) follows without supplying the unknown excess to the observer.

These are statements about the specified endpoint-time transcript and its common coarsenings. They do not compare full growing arrays of intermediate collision positions. Nor does deleting residual time from the output retroactively change a policy that used that time to choose a retained later design. The active hierarchy makes both qualifications explicit. [S9]

## 4. Re-examination of the inherited mathematical spine

### 4.1 Relative convergence is not obtained by dividing an absolute error

I reread the two-boundary construction, the separated operator argument, and the physical transfer proof, rather than relying only on the previous referee's disposition. In the inspected factorization proof, localization gives a summable perturbation of the tridiagonal Hessian along the stationary bridge. The finite bridge is compared with two half-line segments; its gluing residual has exponentially small \(\ell^1\) norm up to fixed polynomial factors in the flight number. [S5, S7]

The determinant comparison retains the first and last \(\lfloor j/3\rfloor\) sites, bounds the discarded perturbation in trace norm, and compares the compressed finite Green operator with the two half-line operators. Remote-boundary reflections and off-diagonal blocks are exponentially small. The trace-log telescoping estimate then gives a relative amplitude estimate. It does not divide an absolute stationary-action error by an exponentially small reference twist. Fixed strict exponential margins absorb polynomial factors at each fixed differentiation order.

For normalized physical integration, the common Morse-coordinate construction places the integral on a fixed disk. Evenness in the square-root offset gives a smooth right extension in the offset itself, with the explicitly permitted finite derivative loss. For the raw observation laws, the action difference has zero value and gradient at the origin. Hence its scaled error is bounded by \(C\tau^j|z|^2\); the positive-part length of each residual-time fibre is Lipschitz. Integrating the amplitude difference and the fibre symmetric difference gives the rare-event-preserving bound \(Cp_{j,d}\tau^j\), including the missing-event atom. These are the estimates actually needed by v30.

No new defect was found in these inspected arguments. This statement is narrower than independently rederiving every finite-geometric estimate and every differentiated-operator lemma cited by them. Those additional dependencies were not all reread in this round; the source audit records that boundary.

### 4.2 The contact inverse has a genuine finite-smooth-jet argument

The active signed-rigidity chapter was read in full. Its weighted Green estimate uses both summable ratios \(e^{-\gamma_-}/\rho<1\) and \(\rho e^{-\gamma_-}<1\). Small local Hessian perturbations therefore preserve an inverse on the same weighted space. Differentiating the stationarity equations leaves this inverse on the highest derivative. [S8]

More importantly, the action-jet filtration is not inferred from formal stationarity derivative counting. Finite truncation of the action cancels interior orbit variations and leaves a terminal product tending to zero with the required fixed derivatives. For graph pairs with equal jets through order \(M\), interpolation of their actual smooth remainders yields the direct flight variation

\[
\partial_t\ell_t(y,z)
=\frac{h_t(y,z)}{\ell_t(y,z)}
 \{\Delta\psi_0(y)+\Delta\psi_1(z)\}.
\]

On the localized orbit this has a summable majorant \(C_M|u|^{M+1}\rho^{(M+1)i}\). Integrating the finite identity before passing to its limit gives equality of the finite action jets. The stated functional smooth bounds, not a bounded list of Taylor coefficients alone, support this conclusion.

The pure degree contribution then counts the initial site once and each interior site twice. The resulting next-jet block has diagonal \(\coth(n\gamma)\) and off-diagonal entries \(\mathfrak r_b^n\operatorname{csch}(n\gamma)\); its determinant is one because \(\mathfrak r_0\mathfrak r_1=1\). Together with the separate quadratic inverse this gives the lower-triangular finite-order reconstruction. It is not an infinite-order condition-number bound. Analyticity enters only when equal recovered jets are used to identify boundary images.

The earlier smooth-remainder objection should not be reopened on the ground that smooth Taylor series need not converge: the present source expressly avoids that inference. At the same time, this local calculation does not by itself certify the subsequent whole-network gluing or global statistical acquisition theorems.

### 4.3 The previous equivariance repair survives re-examination

For the perturbed-density extension, the anchor changes sign with the common orientation. Direct substitution gives

\[
R_{f^r}(u,v)=R_f(-u,-v),\qquad
q_{-\alpha}(f^r)=q_\alpha(f),
\]

and hence the transported action and normalized amplitude are the reflected outputs. The positive density, radical and denominator margins define the domain before the formula is used. Pairwise finite-order bounds use product and reciprocal identities; they do not assume that a line segment stays inside a nonlinear formula domain. [S10]

The old fixed-anchor witness was independently recomputed: its squared outputs are \(107/22500\) and \(4/837\), with difference \(-49/2092500\). This remains a regression example for the old, incorrectly fixed convention, not a refutation of the transported-anchor extension. It does not establish physical-table nonidentifiability.

The common-orientation subsection also retains the necessary simultaneous transformation of the lattice realization, channel placements and curves,

\[
(\iota,A_e,C)\longmapsto(J\iota,JA_eJ,JC).
\]

The two conjugations keep placements proper, and the deck-corrected incidence identity is preserved. This supports the quotient step under the inherited signed classification. It does not replace the latter's incidence and uniqueness hypotheses. The tagged orbit of complete laws remains distinct from pointwise sign erasure, independent channel reversals, or mixing a law with its reflection. C1 and T1 therefore remain closed at their stated scopes. [S10, S11]

## 5. Independent executed diagnostics and their limits

The accompanying `independent_checks.py` was written for this review and executed with Python 3.13.5 in ordinary and optimized modes. Both exited successfully, and their JSON outputs were byte-identical. The checks use explicit exceptions, not Python `assert`, so optimization does not remove them.

The script examines all 1,225 ordered pairs of the 35 four-symbol probability vectors with denominator four. It checks coupling positivity, unit mass, both marginals, and equality of disagreement with total variation, including 35 full-overlap and 162 zero-overlap cases. Three injective embeddings per pair preserve the distance. A noninjective collapse explicitly demonstrates that only contraction survives arbitrary coarsening.

The stopped-experiment tests enumerate 36 combinations of preparation caps, success caps and history-dependent policies, retaining random seeds, every chosen design and stopping information. They check both marginal-expectation bounds, the predictable-success identity, the pathwise success cap, raw preparation accounting, common coarsening, and an exact pilot with an arbitrary bad-pilot continuation. One representative case has 122 terminal transcripts in each model, total variation approximately 0.052032, physical expected cumulative one-step error approximately 0.057969, and expected success-weighted budget approximately 0.104335. Its expected preparation count is approximately 5.41005, while expected successes are only 0.669718; the distinction between error budget and acquisition cost is visible.

A separate information guard gives total variation \(1/2\) after deleting an earlier record while retaining the later design that encodes it, and zero after that design is deleted as well. Twenty transported-anchor slice checks and the preceding fixed-anchor witness provide regression coverage for the inherited convention.

Script SHA-256: `666919cb7714032ab584531f0826c3dce0c3e7c48ee53ef41a8cc4ce199aea25`.  
Result SHA-256: `5a7690187c1697f992c91b325d3807030b37383561b585c5e2136dc2e40452bf`.

These are finite rational diagnostics, not numerical billiard simulations, continuum measurability proofs, infinite half-line estimates, LAN proofs, or a certificate of whole-paper correctness. The author's earlier 12,443-check diagnostic was not rerun in this review. Its reported success remains inherited evidence, separate from the independently executed tests above.

## 6. C2 has not been answered by this revision

The v30 branch's authenticated Actions-run query returned `total_count: 0` and an empty run list. The inherited `VERIFICATION_V29.md` expressly states that complete native-main verification remains outstanding. The v30 comparison adds no new complete-main execution record. Taken together, these observations do not close C2. They do not prove a TeX failure, diagnose an infrastructure problem, or rule out an unprovided local build. [S1, S12, S13]

The author records a successful seven-page native companion build and separately labels a ten-page selected-module fixture. Those are different objects from the main article. In particular, the fixture's unresolved inherited references are not evidence of unresolved references in the complete main; nor can the fixture validate the full appendix and bibliography. I did not independently rebuild the companion, decode all its log evidence, inspect either manuscript PDF, or execute a complete recursive native-main source audit in this round.

**C2 remains a bounded existing request:** provide the actual complete `main.tex` and `two_collision.tex` package at an immutable source identity, with the complete recursive mathematical closure and native build commands, tool versions, logs, PDFs and hashes. Resolve references and citations, including companion auxiliary links, duplicate labels and missing glyphs; inspect remaining layout warnings and all pages. If the reviewed source and the build-source commits differ only in evidence or navigation, demonstrate identity of the mathematical input closure.

A local native build is sufficient. No particular hosted runner, permission change, or new workflow is required. The auxiliary mathematics should remain active; no shortened entry, stubbed bibliography, deleted proof, or selected-module replacement is requested. Adding another manifest without executing the complete build does not answer the request. Conversely, a successful build would answer this presentation/verification issue, not prove all theorems or automatically justify acceptance at a leading journal.

## 7. Significance and top-four presentation

The strongest potential mathematical contribution remains the geometry-specific chain from a uniform nonlinear relative boundary law to unsymmetrized action recovery, finite-smooth-jet inversion and intrinsic periodic determination under explicit network hypotheses. The elementary four-density cancellation, determinant-one identity, finite-group quotient, or matrix equation for lattice reconstruction cannot each be treated as independent evidence of exceptional depth. The introduction already distinguishes these structural steps and compares intrinsic law inversion with direct graph sampling in the richer planar-position experiment; that distinction should be preserved. [S7, S8, S14]

The new coupling subsection is useful proof completion but does not materially increase the flagship novelty. Classical coupling supplies the basic construction [L1]; the manuscript also appropriately distinguishes a Dirichlet cofactor calculation from the periodic Hill framework [L2]. A rigorous significance assessment should therefore focus on the difficult geometry-specific estimates and inverse mechanism, not on repackaging standard tools.

The limited primary-source comparison does not settle priority. De Simoi–Kaloshin–Leguil study marked-length determination for analytic chaotic billiards with axial symmetry and genericity assumptions [L3]. Finamore–Leguil's Theorem A gives marked-length rigidity for finite-horizon Sinai billiards using an enriched marked length spectrum [L4]. These observation maps and hypotheses differ from A2's channel-labelled, signed conditional endpoint laws, supplied marking conventions and calibrated physical records. One cannot conclude from the abstracts or introductory theorems alone that A2 follows from those works, or that it strictly subsumes them. No exhaustive novelty certification is issued here.

A top-four submission should be one self-contained mathematical argument with an accurate submission identity, not a reader's reconstruction of the history of patches. Preservation of historical versions is appropriate in the repository; stale active navigation and a missing complete native-main package are not substitutes for editorial readiness. The private referee-style memoranda must remain provenance, never outside validation. This is a criticism of the present submission evidence, not a demand to lower the mathematical scope or abandon the programme.

## 8. Final requests and disposition

The next response should complete C2 on the full native article and companion, update the active v30 navigation and provide a point-by-point response tied to immutable source identities. It should preserve the correct measurable coupling, the same-parameter physical comparison, the success-weighted stopped budget, the transported-anchor convention and the exact law-valued common-orientation datum. The wording concerning model contact graphs can be clarified without changing any theorem.

No new counterexample or unresolved mathematical error in the v30 insertion was established. Several inherited proof components were independently re-examined, but the statistical and global chapters and the full auxiliary compendium were not all checked line by line. The present report must therefore not be summarized as “the entire manuscript is now mathematically certified, with only typesetting left.” It also supplies no basis for reopening a resolved objection merely to require another revision number.

**Final disposition: the v30 technical addition passes this review; the earlier specifically closed issues remain closed; C2 and revision-package integration remain open. Acceptance of the assembled top-four submission is not recommended on the current evidence. Complete the existing submission and assess its demonstrated mathematical contribution, without arbitrary deletion or escalation to unrelated new results.**

## Source key and primary literature

Repository paths below are relative to `papers/A2-v17-boundary-information-coarsening` at the reviewed commit unless expressly stated otherwise. Full reading and execution scopes appear in `SOURCE_AUDIT.md`.

- **S1:** Authenticated commit metadata and comparison of `8582aa1839dad65ae370e0920e94d7cfe5b1dfa4` with `46f4b1dc2f9609963cae6a80b3a0f458d88250e1`.
- **S2:** `main.tex`; local byte-identity and direct-input enumeration in `source_identity_checks.json`.
- **S3:** Repository-root `README.md` and manuscript `README.md`.
- **S4:** `article/17a_measurable_physical_coupling_v30.tex`, especially `lem:v30-physical-coupling` and `eq:v30-physical-coupling-tv`.
- **S5:** `v6/10_experiment_transfer.tex`, especially `thm:v6-transfer` and its common-physical-coordinate qualification.
- **S6:** `article/17_adaptive_experiments_v30.tex`, especially `lem:v16-kernel-comparison`, `thm:v16-adaptive-transfer`, `cor:v16-pilot-transfer`.
- **S7:** `v4/10_boundary_layers.tex` and `article/15_operator_comparison.tex`.
- **S8:** `article/23a_signed_endpoint_rigidity_v27.tex`.
- **S9:** `article/01b_observation_hierarchy_v29.tex`.
- **S10:** `article/23f1_equivariant_density_extension_v29.tex`.
- **S11:** `article/23h_global_orientation_quotient_v29.tex`.
- **S12:** `VERIFICATION_V29.md`; author-supplied evidence, not newly executed native builds.
- **S13:** Authenticated Actions-run collection queried for the v30 author branch; extracted observation in `REPOSITORY_OBSERVATIONS.json`.
- **S14:** `article/01_introduction_v27.tex`, inspected introductory relative-law, intrinsic-inverse and physical-acquisition discussion; not a complete bibliography audit.
- **S15:** Repository-relative `reviews/a2-v29-external-harsh-top4-2026-09-12/REFEREE_REPORT.md`, read for prior dispositions and scope, not adopted as an independent certificate.

**L1.** D. A. Levin and Y. Peres, with contributions by E. L. Wilmer, *Markov Chains and Mixing Times*, second edition, 2017, Proposition 4.7 and the maximal-coupling discussion, printed pages 50–51. Author-hosted PDF pages 65–66 in zero-based indexing were rendered and inspected. This is the only PDF inspected in this review; it is not the manuscript.

**L2.** S. Bolotin and D. Treschev, *Hill's formula*, arXiv:1006.1532. Abstract-level comparison only; the full paper and its exact theorem dependencies were not audited.

**L3.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4, August 17, 2022. Related journal DOI: `10.1007/s00222-023-01191-8`. Abstract and version metadata inspected; no whole-proof priority comparison.

**L4.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, October 21, 2025. Abstract, introductory description of enriched marking and Theorem A inspected. No claim about a later publication or complete proof audit is made.
