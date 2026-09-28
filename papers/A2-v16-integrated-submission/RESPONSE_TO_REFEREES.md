# Response to the independent A2 v15 report

**Reviewed author:** `627c16b951994fa65acfbf3a621d0e4306131db3`  
**Report:** `a108adf17c4b9360e340a2d5708b20a375d69283`, `reviews/a2-v15-independent-harsh-scalar-transport-2026-09-11/REFEREE_REPORT.md`  
**Revision:** A2 v16, `papers/A2-v16-integrated-submission`  
**Date:** September 11, 2026

We thank the referee for distinguishing the mathematical audit from the negative four-journal significance assessment. We retain the complete mathematical scope and respond by integrating the physical relative theorem with complete observation protocols, making the hierarchy of contributions explicit, and preserving the referee's exact mixed-derivative benchmark with attribution. We do not represent the report as a commissioned journal review or an editorial decision.

## 1. Status of the preceding technical comments

The report closes C14-1 and C14-2 in their stated scope. This revision preserves both repairs. The smooth scalar product lemma remains a constructive account of classical one-dimensional linearization, not a new linearization theorem. The separately proved Schur-composition identity identifies that classical density with the physical half-line determinant amplitude. The one-flight parameter, two-flight return multiplier, curvature ratio, and derivative of the first-hit projection remain distinct. None is silently substituted for another.

The symmetrized width is another expression of the already defined complete energy profile. We do not count it as an additional independent invariant, and we do not infer unrestricted asymmetric graph recovery from it. The smooth Volterra uniqueness proof, rather than convergence of a Taylor series, remains the basis for complete profile determination.

## 2. Significance and organization: C15-2

The abstract and cover letter now state the contribution hierarchy in the following order.

1. The principal theorem concerns normalized **physical** probabilities and endpoint twists, uniformly over flight number, a nonshrinking offset collar, compact smooth geometric families, and every prescribed finite collection of mixed derivatives. Its proof retains exact cofactor normalization, dimension-free trace estimates, separated endpoint layers, and physical residual-time integration.
2. The independent two-contact inverse and the complete symmetrized profile inverse are separate geometric consequences, with different hypotheses and targets. The two-flight benchmark remains visible, including equality of the facing curvatures. Long records are not claimed to create finite-jet parameters absent from two-flight nonlinear data.
3. Observable full-profile reconstruction retains its positive finite-preparation conclusion, supplied uniform certificates, patch labels, regularization, and charged pilot. Its preparation power is sufficient; it is not recast as a minimax theorem for unrestricted smooth billiards.

The full fixed-schedule experiment transfer, previously in the auxiliary material, is moved immediately after the physical density identification. The new adaptive theorem follows there. Thus the operational role of the relative estimate is exhibited in the proof sequence, rather than added as an unsupported interpretation of scalar linearization.

Serial review chronology and verification counts are not used as claims of mathematical novelty. The long original acknowledgments and entry point are retained verbatim in `history/v15/main.tex`; the current acknowledgments retain specific attribution and direct readers to the submission history. All 52 old direct inputs remain active, and every original mathematical proof file is retained.

This addresses C15-2 as an author revision. It does not establish that the referee's significance judgment must change. In particular, the coupling method and the strict-margin example are not presented as major independent innovations.

## 3. Additional complete theorem: adaptive physical transfer

`article/17_adaptive_experiments.tex` proves a stopped kernel comparison and applies it to the physical relative law. For a parameter-independent policy with a deterministic preparation cap, fresh conditionally independent preparations, and all-history collar admissibility, the total variation error of the **complete stopped transcript** is at most

`C E_P[sum_{i <= T} p_xi(a_i) tau^{j(a_i)}] = C E_P[sum_{i <= T} Y_i tau^{j(a_i)}]`.

The transcript retains the designs, failure symbols, success records, and stopping time. The proof couples the policies only until their first disagreement, dominates that common-history submeasure by the physical marginal, and then uses predictable conditional expectation. It does not assume independence of adaptively chosen designs. Measurable maximal couplings are explicitly constructed from the common physical densities and the failure atom.

A policy using flight numbers at least J and stopping no later than its kth success therefore has error at most `C k tau^J`, while its acquisition charge remains **every raw preparation**, not k. A common exact pilot may precede the comparison; its cost is retained. On a bad pilot event, a valid specified probability kernel completes the comparison experiment, and that event's probability is added. No boundary formula is evaluated outside its certified collar.

This is an additional consequence of the existing physical relative theorem. The ordinary coupling inequality is credited to classical probability, with a primary reference. The result is not a parameter-free simulator for an unknown table and does not compare full growing collision arrays on singular supports.

## 4. Additional complete theorem: adaptive critical overlap

`article/31_adaptive_critical.tex` extends the existing known-simple-pair tangent calculation to adaptive stopped transcripts. At a design a, let h(a) be the one-preparation exclusive mass, equal to `p^0_{j,d} (2/pi) arcsin(exp(-j gamma))`. Normalize each common restriction to a probability kernel R_a. Under the same policy driven by those common kernels, the exact remaining common mass is

`m_pi = E_{R^pi}[product_{i <= T}(1-h(a_i))]`.

The tangent transcript distance is exactly `1-m_pi`, and the equal-prior testing error is `m_pi/2`. The proof includes the reverse erasure randomization. Its erasure branch uses the **product-weighted common transcript law**, not the unweighted auxiliary law; those laws generally differ under adaptation.

The same stopped kernel comparison bounds the physical-to-tangent error by the two expected accumulated raw tangent errors. A convergence-in-probability criterion for the cumulative hazards then gives the critical limit. The earlier predetermined-schedule formula and the sharper homogeneous supercritical subsample theorem are retained unchanged. No optimal adaptive design or geometric minimax lower bound is inferred from this simple-pair equivalence.

## 5. Exact mixed-derivative benchmark

`article/16c_strict_margin.tex` incorporates, with attribution to this report, the rational family `R(u)=lambda u/[1+a(1-lambda)u]`. It proves the exact iterate, density, conjugacy remainder, and cocycle identities. At a=0 the mixed derivative of the normalized conjugacy error is `n lambda^(n-1) u^2`. Consequently the strict exponential margin already used in the physical proof cannot be replaced by the endpoint multiplier for that mixed norm.

The benchmark is not claimed to be a billiard realization or a new scalar linearization theorem. It explains why the existing theorem's mixed-parameter quantifier is correct, rather than adding an artificial restriction or alleging that the previously closed comment has reopened.

## 6. Complete build request: C15-1

The native entry point keeps every old direct input, the complete companion, all appendices, and the bibliography. `tools/build_submission.py` checks the full dependency graph, compiles the companion first, then the complete article, and rejects unresolved references/citations, duplicate labels, and missing glyphs. It writes final logs, page counts, hashes, and the exact active-source manifest. It never produces an abbreviated replacement without saying so.

At this source-publication checkpoint the original companion has been compiled locally and the new exact finite checks have been executed. The full native main compilation has **not yet been verified**, so C15-1 remains open in `VERIFICATION.json`. A failed hosted workflow with no executable steps or available logs is not treated as a successful build, or as evidence that the manuscript itself fails to compile. The verification record will distinguish an actual complete build from source-level preparation.

## 7. Historical derivation and retention

The revision is made from the complete pinned v15 Git tree, not a hand-selected replacement. The exact quadratic Schur action, physical first-hit law, boundary layers, trace determinant argument, differentiated estimates, scalar construction, two-contact block, physical realization, two-flight comparison, Abel/Volterra inverses, charged observation results, critical experiments, coalescing-amplitude inverses, smooth-envelope comparisons, and marked-record material remain available and active in the same complete article.

The original v15 submission metadata are archived under `history/v15/` before being superseded. Earlier author trees and all review directories remain unchanged in the repository. Numerical diagnostics are ancillary finite checks; neither their number nor the fact that the source is complete is offered as evidence of four-journal significance.
