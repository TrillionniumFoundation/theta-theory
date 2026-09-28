# Independent referee-style report on A2 v31

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Author branch:** `revision/a2-v31-native-complete-build-top4-2026-09-12`  
**Reviewed source commit:** `e1f6304f6069869ac323e7d1a634a619faa4bc32`  
**Reviewed tree:** `d01225c3db774300fc6f97075d25732be534cc04`  
**Previous review head:** `3825654904d396c4fd90b7965ff2a1b3e8197c83`  
**Native entry:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Review branch:** `review/a2-v31-external-harsh-top4-2026-09-12`  
**Date:** September 12, 2026.

This is an author-requested, AI-assisted independent referee-style assessment against the standards sought for Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, and Acta Mathematica. It is not a commissioned journal report, an editorial decision, or a representation of affiliation with those journals. Source labels identify the mathematics; no unverified manuscript PDF page numbers are supplied. The accompanying [source audit](SOURCE_AUDIT.md) records exactly which sources were examined and which computations were executed.

## Recommendation to the editor

**I do not recommend acceptance of the assembled submission on the present record. The v31 coupling integration is technically sound, and this expanded review has not established a new fatal mathematical counterexample. However, the requested complete native submission verification, C2, remains unfulfilled, and the active submission identity is still inconsistent. The appropriate next step is completion and resubmission of the existing article, not an automatic demand for another round of unrelated mathematical expansion.**

This recommendation must not be shortened to “everything is proved and only typesetting remains.” The current review independently examines the moving-support statistical arguments, the charged physical calibration and global estimation construction, the explicit density inverse, and selected active appendices, in addition to the v31 insertion. It does not rederive every inherited forward estimate, every contact-jet recursion, every analytic gluing result, or every compiled appendix. Earlier positive module assessments are not a certificate for the whole paper. Equally, a workflow which never executed a build is not a counterexample to a theorem.

The mathematical ambition should be assessed through the relative nonlinear boundary law and the unsymmetrized all-order contact inverse, together with their genuinely justified consequences. Neither the number of revisions nor a collection of elementary identities and successful finite diagnostics establishes the exceptional significance expected at the requested level.

| Item | Finding | Disposition |
|---|---|---|
| V31 physical coupling and stopped comparison | Correct under the displayed kernel and collar hypotheses; the model/observation wording is improved | Technical insertion passes |
| C2: complete native-main verification | Current source run failed before any step; no artifacts were produced | Open, submission-blocking |
| I1: active revision identity | Main identifies v31; both principal README entries still identify v29 | Open, integration correction required |
| Moving-ceiling Poisson comparison | Explicit forward and reverse kernels account for layer, bulk and corner errors | No new defect found in the inspected proof |
| Endpoint logarithmic Gaussian limit | Common-collar censoring, score estimates and identifiable quotient are properly separated | No new defect found under the stated regularity assumptions |
| Charged physical reconstruction | Pilot, onset coordinate, finite tests, cap failure and raw preparation cost are retained | No new defect found in the inspected construction, conditional on its geometric dependencies |
| T1 and C1 from earlier rounds | No v31 change to the previously repaired anchor/quotient modules and no new contrary evidence | Remain closed at the previously reviewed scope, not newly certified in full |
| E1: convergence terminology and revision-era prose | The multirate statement should make its convergence mode explicit and remove “v22” prose from the mathematical narrative | Clarification, not a demonstrated false theorem |

## 1. The actual reviewed revision

The branch called `revision/a2-v31-integrated-native-submission-top4-2026-09-12` still pointed to the v30 review commit when inspected. It is not the source reviewed here. The actual v31 source is the immutable commit in the header, and its author-branch head was checked again before recording this report. This distinction matters: a review of the branch name alone could mistakenly review an old report as a new manuscript. [S1]

The authenticated comparison from the previous review head to this source is two commits ahead and zero behind. It contains exactly five changed paths: a new 66-line native-build workflow; the 171-line v31 adaptive section; the 75-line v31 physical coupling lemma; a preserved v30 main entry; and a small modification of the active main entry. No file is deleted in that comparison. The mathematical sections bearing most of the article's weight were not replaced by new v31 proofs. V31 is primarily an integration and verification attempt, not a new solution of the entire set of mathematical problems advertised in the abstract. [S1, S2]

The main source activates the v31 adaptive section, which activates the coupling lemma. It also still compiles the auxiliary compendium. That compendium lists 36 retained inputs. Preservation is appropriate, but compiled material remains part of the submission: it cannot be exempted from correctness or readability merely because it originated in an earlier revision. This report inspects two of those appendix modules in full, not all 36. [S2, S13]

## 2. The measurable coupling survives a direct examination

Lemma `lem:v30-physical-coupling`, now in the v31 source file, has an adequate measurable construction. Its scalar space includes the failure atom. With respect to the fixed scalar measure, write

\[
 h=\min(f,g),\qquad m=\int h\,d\nu.
\]

The diagonal overlap has mass \(m\). The residual product is divided by \(1-m\), so its total mass is \(1-m\), and its marginals are exactly the residual parts of the two densities. Defining this term to be zero when \(m=1\) handles the degenerate case correctly. Joint measurability follows from parameterized integration of jointly measurable nonnegative functions. There is no unproved measurable choice of a maximal coupling. [S3]

Injectivity of the physical embedding is used at the correct point. The residual scalar supports \(\{f>g\}\) and \(\{g>f\}\) are disjoint, and an injective embedding keeps their images disjoint. The Borel inverse makes the image of the first set measurable for each fixed parameter. Consequently the disagreement probability and total variation are both \(1-m\). No jointly measurable family of inverse maps is needed for that pointwise lower bound, since the joint coupling has already been constructed in the forward direction.

The argument does not establish equality of total variation under arbitrary coarsening. A map collapsing two distinct points can reduce total variation from one to zero. The manuscript uses the embedding for equality and a later common observation map for contraction; that distinction is correct. The accompanying exact finite checks include disjoint and identical laws and this strict-contraction example. They check normalization and the logical role of injectivity, not billiard geometry.

The physical embedding may depend on the table because it compares the finite and boundary laws at the same table. It is not an unknown-parameter simulator required of the observer. The new wording, “contact graphs defining the forward model,” resolves the earlier potentially misleading suggestion that these graphs are supplied observations. Conversely, this same-parameter construction cannot be used to compare ambient densities on two different unknown boundary surfaces. The source expressly excludes that inference. [S3]

The stopped comparison also uses the right experiment. While two coupled pasts agree, the common parameter-independent policy chooses the same next design. First-disagreement events then give

\[
 \|\mathsf P^\pi_\xi-\mathsf Q^\pi_\xi\|_{\rm TV}
 \le E_{\mathsf P^\pi_\xi}\sum_{i=1}^{T}e_\xi(a_i).
\]

The physical one-step error is success-weighted, \(e_\xi(a)=Cp_\xi(a)\tau^{j(a)}\). Since activity and the next design are predictable, conditional expectation replaces the success probability by the success indicator inside the expected sum. Stopping no later than the \(k\)-th success bounds the error by \(Ck\tau^J\), although the raw preparation cost is still \(T\), including every failure. The exact-pilot corollary charges bad pilot histories separately and supplies a completion of the comparison experiment on those histories. No iid argument at a random completed sample size is substituted for this construction. [S4]

The underlying coupling principle is elementary and should not be represented as a new general probability theorem. Its value here is closing a concrete measurability dependency in the physical comparison.

## 3. The moving-ceiling experiment: the reverse direction is present

The manuscript's Poisson assertion is stronger than convergence of extracted extreme points. In the inspected two-sided-deficiency chapter, the missing bulk must be reconstructible by a parameter-independent kernel. The chapter supplies the necessary extra hypothesis,

\[
 \sup_{z\in K}\|\rho_{n,z}/\rho_{n,0}-1\|_\infty\le C_K/k
\]

on the common bulk. This is explicitly verified by smooth dependence in the anchored fixed-window model; it is not inferred merely from convergence of the trace at the moving ceiling. That is a substantive improvement over an insufficient trace-only argument. [S5]

Take the reference layer \(|k(w-r)|\le R\), with \(R\) beyond all displacements on the fixed compact local parameter set. The one-record layer probability is \(O(k^{-1})\). The support and trace errors give convergence in total variation mass of the scaled layer measure to

\[
 \rho(u,v)\mathbf1_{\{y>U(u,v)z\}}\,du\,dv\,dy.
\]

The intersection with the fixed face \(r=0\) is not negligible merely by its codimension. The proof supplies the actual estimate: an endpoint strip of area \(O(k^{-1})\) times residual thickness \(O(k^{-1})\) has one-record mass \(O(k^{-2})\), and hence total sample cost \(O(k^{-1})\). This also controls support created immediately outside the reference endpoint domain.

The forward kernel extracts the layer and uses binomial-to-Poisson comparison. The reverse kernel maps Poisson points back, fills the remaining sample with independent draws from the reference conditional bulk law, and uniformly interleaves the two collections. It defines outputs for too many points and for reconstructed nonpositive residual times. Those conventions are necessary to have a kernel on the whole configuration space, not only a high-probability subset.

Normalizing the bulk densities preserves their \(O(k^{-1})\) relative difference. Therefore their squared Hellinger distance is \(O(k^{-2})\); over at most \(k\) reconstructed bulk records the total variation cost is \(O(k^{-1/2})\). Together these estimates give the stated bound

\[
 \Delta(\mathsf E_{n,K}^R,\mathsf P_K^R)
 \le C_K(\varepsilon_{n,K}+k^{-1/2}).
\]

I found no new gap in this inspected argument under its displayed support, positivity and relative-density hypotheses. This conclusion is conditional on the geometric model furnishing those hypotheses; it does not independently certify all earlier finite-bridge estimates. [S5, S7]

The source also correctly distinguishes a common Poisson envelope from domination by the zero-shift member. A support-expanding alternative can put positive mass where the reference intensity vanishes, while every member is still dominated by the Poisson process on the full finite strip. The likelihood relative to that envelope includes the exponential mass correction and the product of support indicators, including the empty-configuration case. Thus “moving support implies absence of any common dominating measure” would be a false criticism of this scalar experiment. [S8]

For an independent algebraic diagnostic I used the normalized triangular family with density \(2/(1-z/k)^2\) on \(u,r>0\), \(u+r<1-z/k\). Exact rational integration includes the moving ceiling and the fixed-face corner. The checked layer-intensity errors are \(O(k^{-1})\). This example has identical normalized common-bulk laws, so it cannot certify the general bulk estimate; the report does not use it for that purpose.

## 4. The endpoint Gaussian and count experiments are not the same theorem

For a linearly vanishing endpoint density \(f_\theta=a_\theta(w_\theta)_+\), the inspected vector chapter uses the score

\[
 \mathsf S=D_\theta\log a_\theta|_0+V/w_0,
 \qquad
 \mathcal J_\Sigma=\int_\Sigma a_0VV^t/|\nabla w_0|\,d\sigma.
\]

The coarea calculation gives the logarithmically divergent second score moment and the required third and fourth moment bounds. With \(q_n=\delta_n(\log(1/\delta_n))^{1/4}\), the mass removed by common-collar censoring has product probability \(o(1)\) at the critical scale \(np_n\delta_n^2\log(1/\delta_n)\to1\). The reverse censoring kernel can send the rare cemetery observation to a fixed original record. This establishes equivalence with a reference-dominated representative without pretending that the original reference member dominates its alternatives. [S6]

The error budgets are compatible:

\[
 np_n\delta_n q_n\to0,\qquad
 np_n\delta_n^3/q_n\to0,\qquad
 np_n\delta_n^4/q_n^2\to0.
\]

They respectively control centering, the cubic remainder, and the quadratic statistic's variance. The manuscript treats singular information on its identifiable range rather than inverting a singular matrix. Its Gaussian experiment theorem expressly limits the Le Cam-distance conclusion to finite local subexperiments; it does not silently equate uniform LAN with a separately proved strong deficiency statement over an uncountable compact set.

As an independent check of the constants and boundary order, the one-dimensional density \(2(1+\theta-x)_+/(1+\theta)^2\) on \([0,2]\), for small nonnegative \(\theta\), has score \((1-x)^{-1}-2\) at zero and boundary information two. Exact integration gives

\[
 P_0(0<1-X<q)=q^2,
\]
\[
 E_0[\mathsf S\mathbf1_{\{1-X\ge q\}}]=-2q+2q^2,
\]
\[
 E_0[\mathsf S^2\mathbf1_{\{1-X\ge q\}}]
 =2\log(1/q)-4+8q-4q^2.
\]

The support-exclusive mass is \(\theta^2/(1+\theta)^2\). These identities agree with the manuscript's distinction between one-record reference singularity and negligible product support-exclusive mass at the logarithmic scale. They are a model diagnostic, not an independently realized billiard family.

The waiting-count chapter has a separate faster coordinate. In its stated coordinates the fast displacement is \(\eta_n=(j_n\sqrt{k_n})^{-1}\), whereas the slow shape direction lies in \(\ker D_\vartheta\gamma\). The quadratic slow drift of the exponent is controlled by \(j_n\delta_n\to0\). The negative-binomial score for \(\log p\) is \((k-pT)/(1-p)\), with information \(k/(1-p)\), and the fast coordinate produces the displayed information-one Gaussian count factor. Its effect on endpoint marks is negligible because

\[
 k_n\eta_n^2\log(1/\eta_n)
 =\log(j_n\sqrt{k_n})/j_n^2\to0.
\]

The factorization is for the uncapped Bernoulli-mark experiment; cap error is added afterward. At the faster endpoint-time scale, the distinct condition \(j_n=o(\sqrt{k_n})\) makes the count component asymptotically ancillary. These are compatible but different local experiments. [S7, S9]

**E1, requested clarification.** The multirate theorem says “joint local limit uniformly on compact parameter sets,” while the precise vector theorem distinguishes LAN/finite-subexperiment convergence from strong deficiency convergence on an uncountable set. State the intended mode directly in `thm:v23-count-endpoint-joint` and identify what is transferred to the finite bridges. I have not proved that a stronger statement is false; this is a precision request, not a newly discovered counterexample. Similarly, replace mathematical prose such as “the v22 endpoint information matrix” with a direct theorem or equation reference. The relevant references already exist, so this is not an allegation of a missing proof.

## 5. The global acquisition argument accounts for the physical observations

The calibration theorem is genuinely formulated in common physical record coordinates. A channel detector supplies two planar endpoint positions in the same frame for both types of that channel; frames of different channels are not registered. Marked labels are supplied, but contact centers, tangent directions, gaps and the lattice metric are not. This is richer than the intrinsic transverse-law datum, and the source says so. [S10]

The near-onset pilot uses two ingredients: no success is possible before \(jg\), and on a grid point with excess between \(h\) and \(2h\) the success probability has a uniform positive lower bound \(ch^2e^{-j\gamma_+}\). It does not infer zero probability from a finite run of failures. With the specified repetitions, a union bound makes every first success occur before \(jg+2h\), except on the charged pilot event. Strict convexity localizes endpoints within \(C\sqrt h\), yielding contact and tangent estimates; subtracting the midpoint \(h\) in the gap estimate gives \(j|\widehat g-g|\le h\).

The order of design choices is important and is correct in the inspected proof. The final even flight number \(J\) is chosen before the pilot, and the pilot itself uses that same \(J\). Thus its error controls \(J|\widehat g-g|\), not merely the error at an earlier shorter flight number. This prevents an uncontrolled onset error when programming the final observation time.

The comparison of estimated and ideal transverse coordinates is a bounded-Lipschitz test bound. It does not claim total-variation continuity of ambient position laws on different unknown curves. At a fixed table, the physical-to-boundary comparison uses the same embedding; replacing the estimated projection by the ideal one is then charged by its coordinate error. This is a valid use of a parameter-dependent quantity inside an error calculation, rather than an oracle operation required of the estimator. [S10]

The single-offset separator construction includes every onset coordinate in the estimation criterion. Compactness gives a finite collection of bounded Lipschitz tests and a separation margin; a finite template rule with a specified tie convention is measurable. In the post-pilot sampling argument, concentration is applied to an uncapped fixed-design success sequence, and the probability of hitting the deterministic cap is subsequently added. Tests sharing a sample need not be independent for the union bound. All raw preparations, not just successes, enter the cap. [S11]

The global diagonal argument runs the selected stage afresh under a prescribed budget. It does not assert that an archive containing earlier short flights has a diverging minimum flight number. Non-effective dependence of the finite library and inverse modulus on the compact analytic class is admitted. These are legitimate existence conclusions, not effective minimax or polynomial-time guarantees. The theorem remains conditional on the earlier compact geometric inverse and finite-data modulus, which were not rederived completely in this round.

The direct-position benchmark must remain visible. Exact planar positions give graph samples in the same long-even-flight physical protocol, so the mere use of long flights does not make half-line inversion necessary there. The intrinsic contribution is recovery from the coarser law-valued datum and its implementation by transverse tests after calibration. The introduction already makes this distinction; it would be inaccurate to repeat the former criticism as though it remained unanswered. [S12]

## 6. The explicit inverse and the support-singular position comparison

The four-density calculation is correct. On the positive interior square,

\[
 R_f(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}
 =1-\frac{S(u)}{d-S(u)}\frac{S(v)}{d-S(v)}.
\]

Strict convexity makes the scalar anchor denominator positive. Recovering the action by a fixed nonzero anchor avoids differentiating a pointwise square root at the minimum. The fixed-order stability proof states the required positive density and anchor bounds, permits general off-model perturbations, and does not infer high derivative control from total variation. The finite-flight corollary removes zeroth and first action terms before applying the anchored contact recursion. No error was found in these operations. The passage from actions to arbitrary contact jets still depends on the separate weighted half-line and finite-remainder proof, not on the cancellation alone. [S14]

The position/scalar comparison also has the necessary observed-type qualification. On a varying homothetic obstacle the successful physical laws have disjoint supports after removing the common anchor, while the finite scalar sample family is dominated. Any kernel applied to a commonly dominated family remains dominated by the pushforward of one common probability measure. That measure can charge at most countably many disjoint output supports, giving worst-case deficiency one over the uncountable parameter interval. If both observed endpoints instead lie on the fixed obstacle, a parameter-independent graph embedding and transverse projection are inverse kernels, and the matched endpoint experiments are equivalent. [S8]

There is no contradiction between maximal finite-sample deficiency in the varying-type family and injectivity of an exact law-valued data map. Nor may residual time be retained in one experiment and removed from the other while invoking the matched-record equivalence. The active source is careful about these distinctions.

T1, the older fixed-anchor off-model equivariance objection, and C1, the common-orientation classification objection, concern separate unchanged modules. This round supplies no evidence to reopen their earlier dispositions. It does not claim a new line-by-line certification of those complete modules or of the analytic gluing dependencies. [S15]

## 7. Active appendices and significance at the requested level

I specifically examined the smooth-envelope minimax appendix because an artificial nuisance lower bound can easily be misrepresented as a physically realized billiard lower bound. The active text does not make that error. Its nuisance functions are explicitly free within a fixed smooth envelope, with an additional strict interior slack assumption. The splice has the prescribed leading amplitudes and respects the same norm budget. Beyond its shrinking splice window the two query probabilities agree. The stopped entropy calculation handles adaptive queries and random stopping, and the timing comparison uses the support-compatible entropy direction. The final paragraph expressly declines to infer a new lower bound for exact nonlinear billiard laws. [S16]

The upper bound in that appendix depends on the earlier nuisance acquisition theorem; I did not independently rederive that entire dependency. Likewise, reading the compendium's input list is not reviewing all its proofs. The expanded scope of this round should be stated honestly rather than converted into an all-appendix certificate.

The active introduction and comparison appendix already distinguish this work from marked-length rigidity, from Prony/root stability, and from other nonregular statistical experiments. De Simoi, Kaloshin and Leguil consider analytic open dispersing billiards with no-eclipse, symmetry and genericity hypotheses. Finamore and Leguil's Theorem A concerns finite-horizon Sinai billiards and an enriched marked length spectrum arising through a geodesic approximation. The latter enriched datum contains more than the ordinary periodic billiard length list. Neither is the same observation map as the signed channel laws and onsets used here. No implication between those data maps has been established in this review. [S12, S17; L1, L2]

Meister and Reiß already give a nonregular regression/Poisson asymptotic-equivalence theorem. Therefore a Gaussian/Poisson contrast or Poissonization is not, by itself, a new principle. This does not make A2's model-specific construction redundant: its finite-bridge control, explicit nonlinear density and contact inverse are different mathematical inputs. [L3]

My assessment is that the strongest potential contribution lies in proving those inputs at the stated level of generality and propagating them without an observation mismatch. The four-density cancellation, the identity \(L=VM^{-1}\), maximal coupling, and finite separation by compactness are not individually a persuasive top-four case. Their connection to a genuinely nontrivial geometric theorem may be. A broad abstract and a long series of private referee memoranda cannot substitute for demonstrating that connection in the assembled article. This is a judgment about the presentation and evidentiary burden, not a proof of lack of novelty or a request to lower the programme's ambition.

## 8. C2 is still open: the workflow did not execute

The source-pinned Actions run is `34695581681`, titled “A2 v31 complete native submission.” Its job `103558378093` has `conclusion: failure`, `steps: []`, and `runner_id: 0`. The run's artifact collection contains zero artifacts. These are direct authenticated observations for the reviewed SHA. They establish that this attempt supplies neither a compiled native main article nor execution evidence from its promised source and mathematical diagnostics. They do not establish a LaTeX error, and the service-level cause was not determined. [S18]

The workflow and native build script are reasonable intended procedures: they archive source, enumerate literal TeX dependencies, build both native entries, retain logs and product hashes, and reject unresolved references, duplicate labels and missing glyphs. But an intended procedure is not a completed result. The script records layout warnings rather than proving every page readable; even a future successful run would still need the resulting article inspected. I have not compiled the native main or companion in this round and have not inspected a manuscript PDF. [S19]

The commit message explicitly says that full-build evidence is not asserted by the source commit. It would therefore be unfair to describe it as a fabricated successful build. The accurate conclusion is narrower and still adverse: C2 was requested and has not been closed.

The root and paper README entries remain v29, linking v29 response and verification records. Their old companion and fixture claims are inherited evidence, not new execution on the v31 native main. No new v31 response or completed native verification record appears among the five changed paths. The source can be identified by SHA, but the active entry pages are not an adequate submission guide. [S20]

## 9. Required response and final disposition

The next submission should provide one unambiguous current manuscript entry and a source-pinned response addressing C2 and I1. Complete the native main and companion build on the entire active graph, preserve the actual commands, versions, logs and product identities, and supply the resulting complete article for inspection. A shorter fixture, a companion-only PDF, an input inventory, or a failed unexecuted workflow is not the requested native-main evidence. Correct the active README navigation without deleting the preserved historical sources.

For E1, state the convergence mode of the count-endpoint local theorem explicitly and remove revision-era prose from the mathematical narrative. Preserve the already correct distinctions between same-parameter coupling and cross-parameter simulation, common domination and reference domination, finite-sample deficiency and law injectivity, intrinsic transverse data and richer position records, and success-weighted comparison error and raw preparation cost.

**Final disposition:** the v31 technical integration passes the inspected mathematical checks; no new fatal counterexample has been established; the previously specifically closed objections are not reopened without evidence. C2 and the active package identity remain open. Acceptance at the requested journal level is not recommended on the current assembled record. Complete and present the existing work, and then assess the full proof chain and its demonstrated significance. This is not a demand for arbitrary deletion, a no-go conclusion, or automatic escalation to unrelated new theorems.

## Source key

Unless otherwise stated, paths are relative to `papers/A2-v17-boundary-information-coarsening` at commit `e1f6304f6069869ac323e7d1a634a619faa4bc32`. Sources marked as dependencies or prior dispositions are not represented as newly proved in this review.

- **S1:** Authenticated author-branch commit collection and comparison `3825654904d396c4fd90b7965ff2a1b3e8197c83...e1f6304f6069869ac323e7d1a634a619faa4bc32`.
- **S2:** `main.tex` and its active input structure.
- **S3:** `article/17a_measurable_physical_coupling_v31.tex`, especially `lem:v30-physical-coupling`.
- **S4:** `article/17_adaptive_experiments_v31.tex`, including `lem:v16-kernel-comparison`, `thm:v16-adaptive-transfer`, `cor:v16-pilot-transfer`.
- **S5:** `article/18c1_endpoint_time_deficiency_v25.tex`, especially the bulk relative-density hypothesis and `thm:v24-two-sided-deficiency`.
- **S6:** `article/18a_vector_boundary_information_v26.tex`, including the collar lemmas, dominated LAN and finite-subexperiment Gaussian theorem.
- **S7:** `article/18c_full_endpoint_time_information_v26.tex`.
- **S8:** `article/18f_domination_and_position_comparison_v27.tex`.
- **S9:** `article/18d_count_endpoint_multirate_v23.tex`.
- **S10:** `article/25a_common_observables_v25.tex`.
- **S11:** `article/25b_augmented_global_reconstruction_v26.tex`.
- **S12:** `article/01_introduction_v27.tex`.
- **S13:** `article/99_auxiliary_compendium_v19.tex`; input inventory, not all referenced proofs.
- **S14:** `article/23f_single_offset_law_inverse_v26.tex`.
- **S15:** Repository-relative `reviews/a2-v30-external-harsh-top4-2026-09-12/REFEREE_REPORT.md`; prior dispositions and their limitations.
- **S16:** `article/65_envelope_minimax.tex`.
- **S17:** `article/70_comparison.tex`.
- **S18:** Authenticated Actions run `34695581681`, job `103558378093`, and its empty artifact collection.
- **S19:** Repository-relative `.github/workflows/a2-v31-native-build.yml`; `tools/build_submission.py`.
- **S20:** Repository-root `README.md` and manuscript `README.md` at the reviewed SHA.

## Primary literature checked

**L1.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4, revised August 17, 2022; related DOI `10.1007/s00222-023-01191-8`. Abstract and version metadata checked. No whole-proof priority audit is claimed.

**L2.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, October 21, 2025. HTML abstract, introductory definition/discussion of the enriched datum and Theorem A checked. No later publication status is asserted.

**L3.** A. Meister and M. Reiß, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, arXiv:1101.5248v1, January 27, 2011. Abstract checked for the stated regression/Poisson comparison, not for every technical theorem dependency.

No manuscript or external-paper PDF was inspected in this round. External literature checks used HTML/abstract sources. Finite diagnostics and their execution limitations are recorded separately, rather than presented as substitutes for these papers or for the manuscript's proofs.
