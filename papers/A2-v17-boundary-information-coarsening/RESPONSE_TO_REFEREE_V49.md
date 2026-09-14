# Response to the independent A2 revision 48 report

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Revision:** 49, September 14, 2026

The report addressed is `reviews/a2-v48-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md`, frozen at review commit `a512f70ca77d711bd6c9ee61988f1e8dd4dba790`. It reviewed mathematical source `fe21046e47a89ec3b3df8493f4d885b087e3ad7f`, as delivered on review-ready snapshot `5babd4cd1515b7f64488d997d89d0860a4eff96c`. The report and its audit record were read in full. They are author-requested AI-assisted assessments, not commissioned journal reports.

## 1. The response in its proper mathematical scope

We thank the referee for separating the supported derivative-kernel proof from the editorial evaluation of its significance. The report does not identify a new false theorem, and we do not convert that assessment into a fictitious algebraic repair. We have followed its two concrete mathematical suggestions and its recommendation to reorganize the dependency path.

The revised **Theorem A** separates three conclusions for the same signed, single-offset observation. On the class of noncircular analytic obstacles, the exact periodic reconstruction has finitely many branches. On the properly asymmetric subclass there is a single branch, retaining the previous unrestricted exact uniqueness conclusion. On the larger noncircular class the derivative kernel is precisely the common Euclidean motion, and immersed finite-dimensional models have finite scalar local coordinates. The conditional full-class histogram and physical acquisition theorems retain their own original hypotheses.

The main new section, **Section 19**, is not an unrelated acquisition or information theorem. It completes the incidence stage of the same structural inverse in the presence of finite symmetry. Lemmas 19.1–19.2 distinguish a finite set of exact congruences from a locally followed angular velocity. Theorem 19.3 enumerates all compatible exact reconstruction branches and bounds their number by a product of obstacle symmetry orders along a channel-incidence spanning tree. Proposition 19.4 supplies the referee's circular-table comparison, with its clearance proof and observation model printed. Section 20 then uses the local branch to extend its existing differential conclusions.

We credit the noncircular differential strengthening and the circular-lattice comparison to Section 4 of the report, in the manuscript's acknowledgments and bibliography. The finite enumeration of compatible global branches is developed here from that distinction and the existing image/cochain inverse. Neither the finite group count nor the final finite-dimensional inverse function theorem is presented as a new general dynamical mechanism. The principal nonclassical content remains the nonlinear relative law and the actual-smooth signed contact inverse. Reorganization and the sharpened symmetry statement make their reach more precise; they do not mechanically settle the journal-placement judgment.

## 2. R48-C1: print the functional-family amplitude derivative

The requested intermediate identity is now printed inside the proof of **Lemma 20.1**, next to the amplitude step, rather than supplied only in the response. The proof defines the moving reference Hessian `H_t^0`, its Green operator `G_t`, the subtracted Hessian perturbation `Delta H_t`, and `T_t=G_t Delta H_t`. It explicitly retains

\[
\dot G=-G\dot H^0G,\qquad
\dot{\Delta H}=\dot H(u)-\dot H^0,\qquad
\dot T=\dot G\,\Delta H+G\dot{\Delta H}.
\]

The entrywise geometric majorant gives trace-norm differentiability after subtraction of the moving reference. It also explains why the edge-product derivative has no infinite-volume constant: `g_t[-ell_{t,uv}(0,0)]=1` identically. Cyclicity in each finite trace power, the bound `q^(n-1)||dot T||_1`, and its summation justify

\[
\frac{\dot B}{B}=\dot U-\operatorname{tr}((I+T)^{-1}\dot T).
\]

Fixed endpoint derivatives produce fixed polynomial factors in the trace-series index and remain summable. Thus this is a proof at the actual functional-family interface, not differentiation of an arbitrary limiting sequence or use of a frozen Green operator. The common-strip assumption, the contact Hessian argument and the moving-cap normalizer derivative are retained. The normalized density derivative is still claimed only in the interior norms needed for the inverse.

The finite diagnostic verifies the moving-reference identity on an explicit positive two-by-two matrix family and detects omission of `dot G`. This is an algebra control, not a replacement for the printed trace-norm proof or an infinite-operator certificate. R48-C1 was classified by the report as an expositional improvement; we retain that classification.

## 3. R48-C2 and R48-C3: preserve the actual-smooth and analytic-variation steps

The four-density and scalar-anchor derivatives, including the positive sign of the anchor contribution, are unchanged. The density squares remain explicitly contact-centered and contain the required axis slices and nonzero anchors. The finite-jet differential still retains both `dot R_n` and `dot M_n q_n`. Its validity rests on the actual smooth finite-remainder factorization before the order-by-order recursion is differentiated. No inverse of an unrestricted infinite jet series is introduced.

The analyticity hypothesis remains a `C^1` family in a fixed-strip holomorphic-support Banach space, with a smaller strip after changing contact frames. The support variation, not merely each parameter slice, is analytic. Zero contact variation propagates by exact analytic uniqueness. This is not a bounded inverse of analytic continuation, nor a noisy continuation estimate. None of these steps uses the absence of finite rotational symmetries, so no extra assumption is needed to apply them on the noncircular class.

## 4. R48-C4 and Section 4 of the report: exact branches versus local angular velocity

The original gcd-one registration lemma and its Bezout formula are retained for the asymmetric subclass. Its complete cochain proof is also retained. The lemma now additionally states its local-branch version for noncircular obstacles and proves that version using Lemma 19.2.

A noncircular obstacle has some nonzero support harmonic `z_k`, `k>=2`. For two of its copies along the actual table family, the ratio satisfies `r=z_k(C_t)/z_k(C_s)=exp(-ik alpha)`. The local logarithm through the actual base alignment gives the rotation branch and

\[
\dot r/r=-ik\dot\alpha.
\]

The lemma explicitly assumes the continuously followed actual congruence branch. This branch exists in the application because the physical table and its contact frames move continuously. We do **not** claim that every symmetry of a symmetric base obstacle extends after that symmetry is broken. For instance, a small third-harmonic perturbation of a second-harmonic body can destroy its half-turn symmetry. The actual branch persists, which is all the derivative proof uses.

This is not an observation of an unknown pose. The actual alignment is used only to analyze the local kernel, exactly as the actual table is used to differentiate the law. It does not select one globally preferred branch from an unmarked record.

For exact reconstruction, Theorem 19.3 supplies the discrete matching argument instead of extending global uniqueness without one. First the existing local law inverse recovers each entire analytic channel-frame image. An obstacle with symmetry order `m_a` has exactly `m_a` proper congruences between two of its copies. A rooted tree on the channel vertices, with a fixed common obstacle occurrence at each link, enumerates finitely many rotation assignments. For each assignment we then enforce all repeated-image equalities, compute the center displacement cochain, recover `L=(v_1 v_2)M^{-1}`, and test full periodic admissibility and the specified clear-channel collars. Every actual realization is in the list, and every retained candidate realizes the data. Failed compatibility choices are discarded, not arbitrarily phased.

The product bound counts assignments, can overcount duplicates, and is not claimed sharp. The known integer gain matrix is inverted as given, without a unimodularity assumption. The number and scale of the unknown Euclidean lattice are not supplied as calibration. Exact analytic image equality and geometric admissibility are tests on function-valued data, not a claimed finite-precision decision procedure.

The circular comparison is included at the same location to explain the continuous stabilizer. The two selected disk channels retain their gaps and laws while the Gram form changes. Clearance is proved uniformly using separation, an eight-neighbor reduction, and a strict perturbation margin. This example is outside the noncircular theorem; it is not a counterexample to a retained result, a finite-horizon claim, or a universal impossibility statement for other designs.

## 5. R48-C5 and R48-C6: retain the observation and the proved consequences

**Theorems 20.5 and 20.6** now apply to noncircular base obstacles, not only to those with trivial proper symmetry. Their original derivative-kernel, dual separation, inverse-function and convex-ball lower-Lipschitz arguments remain. The registration lemma supplies the required local interpretation. The exact unique branch is still asserted on the asymmetric subclass. Finite cyclic alternatives are not misreported as continuous infinitesimal symmetries.

The scalar coordinate functions remain model-local exact gaps and compactly supported expectations. They need not be fixed uniformly over all models or over the infinite-dimensional analytic class. We do not change the intrinsic, moving-contact, fixed-offset derivative experiment into a fixed-laboratory-origin experiment. Nor is a finite-sample efficiency result inferred from the coordinate theorem.

All v47 calibration and v46 quantitative proofs are byte-identical in their active source files. They move to Part III: old Lemmas 21.7–21.8, Theorem 21.9 and Corollary 21.10 become **38.7–38.10**. They retain amplified onset error, moving normalization, internal and outer grid edges, singular chart maps, the fixed-final-flight pilot, conditional uncapped concentration, separately charged cap failure, and strict budget slack. The resolved R46-P1 clarification remains present. No closed calibration issue is reopened and no histogram-only pilot is claimed.

## 6. The writing and dependency-path revision

Part I now begins with the geometric setup and proceeds directly through the relative law, the actual-smooth signed inverse, analytic images, intrinsic registration, the finite symmetry branches and the derivative kernel. It no longer begins with a second detailed introduction followed by successive revision overviews. Those complete statements and extended comparisons have been moved to the **compiled Appendix A.1**, with their labels, theorem statements and proofs retained. Their purpose as alternative formulations and comparisons is explicit.

Part II keeps the local information theory and now introduces its observation spaces at the start. Part III keeps together the quantified law-to-table inverse, hard-histogram acquisition, direct-position and short-flight benchmarks, and global physical estimators. Their assumptions do not enter the core exact proof. The revised introduction states the datum, the separate symmetry classes and Theorem A once, then gives the proof chain and observation-specific literature comparison. No extra collection of routine acquisition corollaries has been appended.

All 105 inherited active source inputs remain active; 100 are byte-identical in place. Five edited original inputs are archived exactly. The edits are the main entry/organization, the structural introduction, the catalogue heading and organization paragraph, the differential proof/hypothesis changes, and the bibliography acknowledgment. Their mathematical statements are retained or strengthened, and every old label and theorem/proof-environment count is retained. The new section adds two lemmas, one theorem, one proposition and four proofs. The final graph has 106 active inputs; it includes all 239 inherited combined main/companion proof environments. The companion itself is unchanged.

## 7. Literature and attribution

The relevant primary records were checked again on September 14, 2026. Finamore–Leguil, arXiv:2510.18983, remains v1 and concerns the enriched marked length spectrum of finite-horizon Sinai billiards. De Simoi–Kaloshin–Leguil, arXiv:1905.00890, remains v4 and concerns analytic open billiards with non-eclipse, symmetry and genericity hypotheses. Florio–Leguil, arXiv:2010.04120v5, retains the explicit correction notice and dynamical conjugacy conclusions. Trefethen's publisher record gives BIT 60 (2020), 901–915, DOI 10.1007/s10543-020-00802-7. The revised introduction includes all four relevant comparisons through the existing bibliography.

Primary records: https://arxiv.org/abs/2510.18983 ; https://arxiv.org/abs/1905.00890 ; https://arxiv.org/abs/2010.04120v5 ; https://link.springer.com/article/10.1007/s10543-020-00802-7 .

No reduction from marked length data to our endpoint laws, or conversely, is asserted. The earlier removed spectral-rigidity statement is not a premise. This targeted comparison is not an exhaustive priority audit. The new acknowledgment credits the referee's mathematical suggestion rather than presenting it as independently originated here.

## 8. Verification and the next assessment

The complete main and companion were compiled locally, companion first, with shell escape disabled. The local main is 259 pages and the companion seven. The v49 preservation, symmetry, moving-reference and circular controls pass in ordinary and optimized Python, including the retained v48 and v47 functional checks. The version-scoped native workflow separately materializes the complete readable sources, records their actual commit, compiles both complete entries from a frozen Git snapshot, and publishes both products and their evidence on a new products branch. Final source/product identities, observed warnings, post-download checks and sampled visual coverage are recorded in `REVIEW_READY_V49.md` at handoff.

These checks do not certify the mathematical proofs or establish exceptional journal significance. The next referee should evaluate the moving-reference expansion, the finite-branch classification and the noncircular differential theorem, then assess the unified structural inverse on its merits. The technical disposition of the already resolved calibration interfaces and the editorial placement judgment remain separate.
