# Independent referee-style report on A2 v32

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed author branch:** `revision/a2-v32-compact-lecam-native-submission-top4-2026-09-12`  
**Reviewed submission commit:** `a4fe5c11f18070fc03d878ba683e014b48e921af`  
**Reviewed tree:** `2968770619cd9be6e2692ada43bbe1ad34d13bae`  
**Mathematical-source commit:** `35fd4ccef1b5785692de512635f7240a4df0d641`  
**Previous review head:** `9edd5f48d91b74d09718149de6e2c3550c375f20`  
**Native entry:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Review branch:** `review/a2-v32-external-harsh-top4-2026-09-12`  
**Date:** September 12, 2026.

This is an author-requested, AI-assisted independent referee-style assessment against the requested standards of Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, and Acta Mathematica. It is not a commissioned journal report, an editorial decision, or a claim of affiliation with those journals. Equation and theorem labels below refer to the immutable source above, not to uninspected PDF page numbers. The accompanying [source and execution audit](SOURCE_AUDIT.md) defines the scope precisely.

## Recommendation

**Do not accept the assembled submission on the present record. The v32 mathematical increment passes the checks performed here: the compact-experiment argument genuinely closes E1, and the submission identity correction closes I1. The complete native submission verification, C2, remains open. A targeted major revision completing and coherently presenting this article is appropriate; another automatic escalation to unrelated new theorems is not.**

This is not a finding that a main theorem is false. No new fatal mathematical counterexample was established in this review. Nor is it a certification that every theorem in the assembled manuscript is proved and only typography remains. This round examines the new statistical arguments in detail and independently checks substantial portions of the relative-law and all-order contact-inverse backbone. It does not freshly verify every finite-bridge foundation, global gluing argument, acquisition theorem, companion proof, and active appendix. Earlier reports cannot supply that certification by accumulation.

The strongest potential contribution remains the nonlinear relative boundary law and its unsymmetrized contact inverse, with the global consequences that follow under the stated data and incidence hypotheses. The new compactness lemma is a useful completion of that programme, not by itself evidence of exceptional mathematical significance.

| Item | Finding | Disposition |
|---|---|---|
| E1: convergence mode | Uniform continuity and finite-net arguments now prove compact two-sided Le Cam convergence; the count chapter includes the necessary product comparisons | Closed for the stated local models |
| I1: current identity | Main and both principal README entries identify v32 and its actual ancestry | Closed |
| C2: native main and companion | The source-pinned hosted job failed with no executed steps and no artifacts | Open; submission-blocking |
| Relative factorization and contact inverse | No defect found in the inspected trace, envelope, finite-remainder and last-jet arguments | Positive module assessment, not whole-paper certification |
| T1/C1 from earlier rounds | The relevant off-model equivariance and orientation modules are unchanged; this round supplies no contrary evidence | Not reopened; no new complete certification |
| M1–M3 below | Remaining logical wording, navigation and theorem-level citation issues | Targeted corrections, not counterexamples |

## 1. What has actually changed

The authenticated comparison with the v31 review head is two commits ahead, zero behind, and contains nineteen changed paths without a deleted file. The two new mathematical sources contain 160 and 272 lines. The other changes concern the main entry, navigation, preservation, response, verification records and build tooling. The substantial geometric sources were not replaced by new v32 proofs. Both principal README entries now correctly distinguish the mathematical-source commit from the later assembled submission commit. [S1–S3]

This distinction matters to the recommendation. V32 responds positively to a precise request: it supplies the previously unstated convergence mode with an actual proof, rather than weakening the conclusion to a finite-parameter statement. It does not, and should not be described as having, independently re-established the entire inherited manuscript.

The native main still activates the auxiliary compendium. Its thirty-six listed inputs are part of the submission, not merely archival files. Preserving them is legitimate. Their presence is neither evidence that they have been compiled successfully nor an exemption from mathematical correctness and readability. [S2, S12]

## 2. The finite-to-compact passage is now a proof, not terminology

### 2.1 A single parameter-independent kernel is used

Lemma `lem:v32-finite-net` is correct. Fix a finite r-net F of the compact parameter set K. A kernel selected to approximate the experiment on F remains one kernel on the entire sample space. For t in K, a nearby point s in F is used only to estimate its error. Total-variation contraction gives, in each direction,

\[
 \Delta(\mathsf E_n,\mathsf E)
 \le \Delta(\mathsf E_n|_F,\mathsf E|_F)
       +\omega_n(r)+\omega(r).
\]

The proof first takes the sample-size limit for the fixed net and then sends r to zero. It does not allow the simulator to receive the unknown parameter or its nearest net point. That would have been a serious defect; it is not present here. Standard Borel sample spaces and the use of arbitrarily near-optimal kernels avoid an unnecessary attainment assumption. [S4]

The extra modulus is a real hypothesis. To see why, let K consist of zero and the points 1/m. At sample size n set P at parameter 1/n equal to the point mass at one, and set it equal to the point mass at zero at every other parameter. Let the proposed limit be a one-point experiment. Every fixed finite restriction is eventually trivial, but the full compact-indexed Le Cam distance is exactly one half: a reverse kernel must approximate both point masses, and the optimal parameter-independent output is their equal mixture. Thus finite-subexperiment convergence alone is insufficient. This is a diagnostic counterexample to an invalid general inference, **not a counterexample to the manuscript**, whose new continuity estimate excludes it.

### 2.2 The moving-boundary estimate supplies the required modulus

The inherited support-stability lemma is used with the right strength. For densities a(w)_+ and a-tilde(w-tilde)_+, a defining-function displacement epsilon contributes epsilon squared times log(e/epsilon) to squared Hellinger distance; a smooth amplitude displacement contributes its square. Near the boundary, a strip of width epsilon has density of order epsilon and therefore mass of order epsilon squared. Away from that strip the square-root difference is bounded by a constant times

\[
 \eta^2s+\varepsilon^2/s,
\]

and integration in the normal coordinate s supplies the logarithm. Uniform collar regularity and positive amplitude bounds are essential. They are among the displayed hypotheses, not consequences of mere pointwise smoothness. [S6]

For two local parameters separated by s, joint smoothness gives a displacement of order delta_n s. The v32 proof consequently obtains

\[
 H^2(f_{\delta_nh},f_{\delta_nh'})
 \le C_K\delta_n^2s^2
       \{1+\log(1/\delta_n)+\log(1/s)\}.
\]

The failure atoms in this theorem have equal masses. Multiplying by n p_n, using the critical rate, and taking products therefore yields

\[
 H^2(P_{n,h}^{\otimes n},P_{n,h'}^{\otimes n})
 \le C_Ks^2\{1+\log(1/s)\}.
\]

Since s times the square root of this logarithmic factor tends to zero, the required total-variation modulus follows. The calculation uses the manuscript's convention H squared equal to the integral of the squared difference of square roots; no hidden factor-of-two change is needed. [S4, S6]

The finite Gaussian limits come from the common-collar representative, not a nonexistent likelihood ratio on support-exclusive observations of the original family. At q_n equal to delta_n times the fourth root of log(1/delta_n), the discarded product mass tends to zero. The centering, third-moment and fourth-moment budgets in the inherited LAN proof are compatible with that choice. I found no new defect in the inspected statistical chain. [S6]

### 2.3 Singular information and the physical endpoint output

For the Gaussian family, direct integration on the identifiable range gives

\[
 H^2(Q_h,Q_{h'})
 =2\{1-\exp[-(h-h')^t\mathcal J_\Sigma(h-h')/8]\}.
\]

This requires no inverse on the kernel of the information matrix. It also covers the zero-dimensional limit. The proof's treatment of singular information is therefore adequate. [S4, S6]

The fixed-window corollary does not require the exact boundary densities themselves to have a parameter-independent support. It first treats the normalized ideal densities, then uses the uniform exact/ideal Hellinger comparison, reference cap errors and success-weighted stopped transfer. Independent design batches add their error bounds. Restriction to a linear subspace cannot increase deficiency. This chain is valid at the declared scalar endpoint-output level. It is not a theorem about the complete collision array or noiseless planar endpoint positions. [S4, S7]

**Disposition of E1 for the endpoint theorem: closed.** The compact result is stronger than the previously explicit finite-restriction conclusion, and the missing argument has actually been supplied. Its kernels may depend on a fixed compact local set and reference design; no uniform equivalence over an unbounded parameter space or an infinite-dimensional analytic class has been proved or is needed for this statement.

## 3. The two-speed waiting-count argument also survives examination

### 3.1 The mixed remainder budget is sufficient

The coordinates are

\[
 \eta_n=(j_n\sqrt{k_n})^{-1},\qquad
 g=g_0+\delta_na/j_n,\qquad
 \vartheta=\eta_nbv_\gamma+\delta_nh,
 \quad h\in\ker D_\vartheta\gamma.
\]

The derivative of gamma in the chosen fast direction is one. The success log ratio is therefore minus b divided by the square root of k_n, with a remainder bounded by

\[
 C_K(\delta_n+\eta_n+j_n\delta_n^2
                    +j_n\delta_n\eta_n+j_n\eta_n^2).
\]

Multiplication by the square root of k_n sends every term to zero under the stated critical scale and j_n delta_n tending to zero. In particular, the quadratic slow drift of gamma and the mixed fast–slow term have not been silently discarded. This is an important part of the revised proof. [S5]

For a waiting count T stopped at k successes, the score for log p is (k-pT)/(1-p), with variance k/(1-p). The two displayed higher likelihood derivatives are also correct. Representing T as a sum of independent geometric waits gives uniformly controlled normalized third moments as p tends to zero. The resulting normal count factor has information one with the sign convention used in the chapter. [S5]

### 3.2 An exact affinity calculation independently checks the comparison

The geometric square-root-curve argument proves

\[
 H^2(G_p,G_q)\le
 \frac{(\log p-\log q)^2}{4(1-p_*)},\qquad p,q\le p_*<1.
\]

An independent calculation is useful here. The geometric affinity is

\[
 A(G_p,G_q)=
 \frac{\sqrt{pq}}{1-\sqrt{(1-p)(1-q)}}.
\]

For negative-binomial total waits at k successes it is **exactly** the kth power of that expression. Indeed, the square root of the product of the two mass functions has the same binomial coefficient, and summing it uses the series for (1-x) to the power minus k. Thus the manuscript's product upper bound is fully consistent with the sufficient waiting-count statistic; no Poisson approximation is being smuggled into this discrete experiment.

Replacing the true batch probabilities by p at the reference times exp(-b/sqrt(k_n)) costs o(1) in squared product Hellinger distance, because their log difference is uniformly o(k_n to the power minus one half). The ideal family has both its finite LAN limit and a uniform pairwise Hellinger modulus. Applying the new finite-net lemma is justified. [S5]

### 3.3 Independence, caps and finite bridges occur in the right order

The uncapped Bernoulli-mark model factors exactly into waiting times and successful marks. This factorization cannot simply be assumed after deterministic capping. The revised proof appropriately removes caps first, makes its two product comparisons, and restores caps afterward.

The fast displacement changes endpoint defining functions and amplitudes by order eta_n. Its total mark error is bounded by

\[
 C_K k_n\eta_n^2\log(e/\eta_n)
 =C_K\frac{1+\log(j_n\sqrt{k_n})}{j_n^2}=o(1).
\]

The remaining endpoint factor has the compact Gaussian approximation from the new corollary. Taking product kernels on the compact coordinate projections and restricting to K is legitimate even when K itself is not a Cartesian product. The cap discrepancy is bounded by the sum of exp(-c k_{n,ell}), and the finite-bridge discrepancy is C_K k_n tau to the power j_n. Failed preparations remain charged. [S4, S5, S7]

The rates are not vacuous. For example, take delta_k equal to the square root of 2/(k log k), and j_k equal to twice the ceiling of A log k. Any fixed A with 2A times the absolute value of log tau greater than one satisfies all the displayed conditions asymptotically. This is an analytic compatibility check, not a statement that the finite diagnostic values already equal their limits.

**Disposition of E1 for the count–endpoint theorem: closed.** The two compact Le Cam limits are now explicit and supported by more than a joint likelihood expansion. This does not certify a Gaussian limit for every richer observation space.

## 4. Examination of the geometric backbone

A referee should not evaluate this paper solely through the two new statistical sections. I therefore independently examined the following inherited arguments. Their positive assessment is bounded by the dependencies stated in the audit.

### 4.1 Relative control does not divide by an exponentially small error scale

The Dirichlet cofactor identity gives minus W_uv as the product of positive mixed-edge magnitudes divided by the interior Hessian determinant. Its normalized version separates an edge product from det(I+G_0 Delta H). The identity is elementary; its application here needs localization of the nonlinear perturbation. [S8]

The boundary-layer proof provides that localization. It glues two half-line orbits, controls the stationary residual and solution difference in the l1 norm, and cuts the determinant perturbation to blocks of size floor(j/3) at each end. The removed perturbation has exponentially small trace norm, rather than merely small operator norm multiplied by an uncontrolled dimension. Remote-boundary reflections and cross-block Green terms are exponentially small. The trace-log series then transfers the comparison with constants independent of truncation dimension. Fixed derivative orders introduce polynomial factors that can be absorbed using a strict exponential margin. [S8, S9]

The normalized sublevel integral is treated separately through a uniform Morse change of variables and an even smooth integral on a fixed disk. This correctly accounts for the additional finite derivative orders needed to differentiate with respect to the offset down to zero. A sharp moving boundary is not differentiated formally. Nor is an absolute action estimate divided by an exponentially small reference twist. These are substantive strengths of the inspected proof.

The quadratic Green formulas, finite stationary construction and full physical flux identities remain inputs to this examination. I have not independently rederived every earlier source establishing them. The bounded-Lipschitz statement for additionally retained end collisions in the older boundary-layer chapter must not be mistaken for the stronger scalar total-variation transfer used elsewhere.

### 4.2 The all-order inverse has the necessary envelope and remainder arguments

In the signed inverse chapter, the weighted Green operator is bounded because both convolution ratios are strictly below one. The nonlinear stationarity operator is locally invertible with a uniform weighted bound. For finite truncations of the action, interior orbit-variation terms cancel by stationarity; the right-end remainder decays geometrically twice. This justifies the envelope limit instead of appealing to a formal infinite-dimensional differentiation rule. [S10]

The smooth finite-jet factorization lemma is particularly important. Interpolating two local graph pairs with equal jets through order M gives direct flight variations of order the endpoint coordinate to the power M+1. The weighted orbit bound makes their sum absolutely convergent. Integrating the finite envelope identity before passing to the limit gives an action difference of order u to the power M+1. Consequently the finite action jet is independent of arbitrary smooth remainders, including flat variations. The argument correctly demands functional smoothness bounds; a bounded list of Taylor coefficients alone would not suffice. [S10]

For a new degree n, the envelope contribution is the pure nth endpoint power evaluated on the linear half-line orbit. The starting site occurs once and interior sites twice. The sums give coth(n gamma) on the diagonal and r_b to the power n times csch(n gamma) off the diagonal. Since r_0 r_1=1, the determinant is one. The new pair of graph jets enters affinely, and the full finite-order map is block lower triangular with an invertible leading curvature block. The fixed-order local stability conclusion follows. [S10]

This reasoning is materially stronger than displaying a determinant-one matrix without proving that it is the actual last-jet block. I found no such omission in the inspected chapter. It is also correctly limited: fixed-order stability is not uniform conditioning of the infinite-jet map, and equality of smooth jets is not equality of smooth boundary images. The latter conclusion uses analyticity.

### 4.3 One density law supplies the correct unsymmetrized action input

The four-density ratio cancels the unknown flux factors and satisfies

\[
 1-R_f(u,v)=t(u)t(v),\qquad t(u)=S(u)/(d-S(u)).
\]

A fixed nonzero anchor recovers t and then S without differentiating a pointwise square root at the minimum. Positivity and a lower bound on the anchor control the off-model fixed-order inverse. The finite-flight corollary separately controls normalization and the interior density norm, and removes the zeroth and first action terms before applying the anchored jet inverse. These steps are correct in the inspected source. [S11]

The result concerns an exact law and, for quantitative perturbations, a specified interior C^M norm. It does not make isolated density values directly observable from a finite sample, and total variation does not automatically control high derivatives. The manuscript observes these distinctions. My exact asymmetric diagnostic checks the algebra, not realization by a nonlinear billiard table.

## 5. Remaining corrections to the mathematical presentation

**M1 — Logical wording and integration.** The inherited `thm:v22-fixed-window-gaussian` still uses “Equivalently” between an asymptotically equivalent uniformly LAN representative and finite-subexperiment Gaussian convergence. These are not equivalent assertions in general. Replace it with “In particular,” and refer explicitly to `cor:v32-compact-fixed-window` for the compact-distance conclusion. Similarly, the introduction and the closing terminology remark of the vector chapter should point to the new compact theorem rather than leave the reader with only the older finite-restriction summary. The stronger result now exists; this is a coherence correction, not a request for another theorem. [S2, S6, S7]

**M2 — State the observation map at the multirate theorem.** Near `thm:v23-count-endpoint-joint`, identify the retained endpoint pairs explicitly as the laboratory transverse coordinates (y_first,y_last) of `eq:v22-laboratory-endpoint-map`. The surrounding hierarchy already makes this interpretation available. Repeating it at this theorem would prevent a reader from importing noiseless normal coordinates, for which the support geometry is different. This is not an allegation that the present proof actually uses those richer records. [S5, S7]

**M3 — Cite the imported convergence theorem precisely.** The finite-parameter likelihood-to-experiment theorem is invoked in the vector chapter and again for the ideal waiting family. Give an identifiable theorem-level reference, or state the finite-experiment result with the normalization/integrability conditions used. The Gaussian likelihood limits have mean one, and the preceding contiguity discussion supplies the appropriate setting; I have not identified a failure of that step. Nevertheless, a full mathematical submission should not require a referee to infer which classical convergence theorem is intended. [S5, S6]

The unchanged off-model orientation extension, global signature matching, physical calibration and complete Poisson reconstruction kernels were not fully re-audited in this round. Their previous dispositions are not reopened without evidence, but they must not be relabelled as newly certified by this report.

## 6. C2 remains open on direct execution evidence

The authenticated Actions run for the reviewed submission SHA is `34701204570`, titled **A2 v32 complete native submission**. Its job `103573170687` reports failure, an empty step list, and runner_id zero. The run has zero artifacts. The job completed on September 12, 2026, at 15:06:06 UTC. This is evidence of no executed native build in that attempt, not evidence of a LaTeX error or of a mathematical contradiction. The service-level cause was not determined. [S13]

The author correctly distinguishes the five-page changed-section fixture, sixteen unresolved external labels, finite Python diagnostics and build-utility regression from a complete native-main build. The record does not fabricate a successful full compilation. However, the promised full-native execution remains absent, and the record still speaks prospectively about observing an attempt that has now failed. Append the actual run and job disposition. [S3]

A five-page fixture cannot answer whether the native main plus companion resolve every reference, whether the preserved appendices create collisions, or whether the complete article is readable. Conversely, successful compilation alone would not prove the mathematics. The requested evidence has two distinct functions: establish an unambiguous complete submission, then make that submission available for substantive inspection.

I did not compile the native manuscript or companion in this review and inspected no manuscript PDF. The independent diagnostics accompanying this report are explicitly not substitutes. C2 therefore remains open; its closure must not be inferred from this review branch or its passing script.

## 7. Significance and the requested journal level

The introduction already differentiates the intrinsic law-valued inverse from geometric point sampling and from marked-length spectral rigidity. Those qualifications should remain. De Simoi, Kaloshin and Leguil consider analytic open dispersing billiards with non-eclipse, symmetry and genericity assumptions; Finamore and Leguil consider finite-horizon Sinai billiards through an enriched marked length spectrum. Their data are not the signed channel laws, onsets and marked deck information used here. Neither inclusion between these observation maps has been proved in this review. [S2; L1, L2]

Meister and Reiss already establish a nonregular regression/Poisson asymptotic-equivalence theorem. Thus neither Poissonization nor a contrast between Gaussian and Poisson limits is, alone, a new general principle. This does not settle the novelty of the billiard-specific geometry. [L3]

My adverse editorial assessment is not that the work has been shown to be unoriginal. The primary-literature check here is deliberately narrower than an exhaustive priority audit. It is that the current assembled record does not yet justify a top-four acceptance recommendation. Elementary cofactor algebra, finite-net compactness, four-density cancellation and the final lattice matrix inversion cannot individually bear that recommendation. The case must be made through the simultaneous nonlinear relative estimates, the unsymmetrized arbitrary-order contact inverse, and the genuinely justified intrinsic consequences. The inspected proof spine is substantial enough to deserve completion, not blanket dismissal; it is not enough to certify everything advertised in the abstract.

Do not substitute a longer title, more preserved modules, or another private review iteration for a coherent mathematical submission. No arbitrary deletion of mathematics is requested. Preserve the historical sources while ensuring that every active part has a clear role, correct hypotheses and a verifiable relationship to the main claims.

## 8. Required response and final disposition

The next response should close C2 with an executed build of the complete native `main.tex` and `two_collision.tex`, using the unchanged full active source graph. Retain the exact tested source SHA, commands, compiler versions, logs, resolved-reference and citation checks, and product hashes. Supply the resulting complete PDFs for inspection. A local build on another functioning environment is acceptable; success of this particular hosted service is not a mathematical requirement. An unstarted job or a shorter fixture is not the requested evidence.

Correct M1–M3 in place, maintain the now-correct v32 entry identity, and update the verification record with actual rather than prospective execution. Preserve the observation-space distinctions, the scalar versus physical position separation, reference versus common domination, all charged failures, and fixed-order versus infinite-order stability qualifications.

**Final disposition:** E1 and I1 are closed at the stated scope. C2 remains open. The new compact and count–endpoint arguments pass this review's mathematical checks; the examined geometric backbone contains no newly established fatal defect. Acceptance of the complete submission at the requested journal level is not recommended on the present evidence. Complete and present the existing work, rather than weakening it or indefinitely expanding its claims.

## Sources and reproducibility

Source keys S1–S13, immutable paths and blob identities, review coverage, execution commands and limitations are recorded in [SOURCE_AUDIT.md](SOURCE_AUDIT.md). The independently executed [diagnostics.py](diagnostics.py) and its [output](diagnostics.json) accompany this report. Ordinary and optimized Python executions produced byte-identical output. Exact identities and finite numerical checks are distinguished from proofs throughout.

**L1.** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), revised August 17, 2022; related DOI `10.1007/s00222-023-01191-8`. Abstract and version metadata checked, not a full proof or priority audit.

**L2.** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983v1](https://arxiv.org/abs/2510.18983v1), October 21, 2025. Abstract and version metadata checked. No later publication status is asserted.

**L3.** A. Meister and M. Reiss, *Asymptotic Equivalence for Nonparametric Regression with Non-Regular Errors*, [arXiv:1101.5248v1](https://arxiv.org/abs/1101.5248v1), January 27, 2011. Abstract checked for the stated nonregular regression/Poisson comparison. No external-paper PDF was inspected.
