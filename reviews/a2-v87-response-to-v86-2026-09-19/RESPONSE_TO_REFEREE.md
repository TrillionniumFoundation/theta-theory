# A2 revision 87: response to the independent report on revision 86

**Date:** 19 September 2026.  
**Report answered:** `reviews/a2-v86-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md`, corrected report commit `18de3872c705b5be9582429567877aac8d1a5fbe`.  
**Reviewed manuscript source:** `bf67e3f33d394c80d7d7daeb51e52de12ec3d180`.  
**Revision branch:** `revision/a2-v87-gap-free-singular-quotient-2026-09-19`.  
**Principal manuscript:** `papers/A2-v17-boundary-information-coarsening/rigidity_v87.tex`.  
**Preserved companion:** `papers/A2-v17-boundary-information-coarsening/rigidity_v87_companion.tex`.

The report distinguishes proof-level repairs from the requested change in mathematical scale. We have addressed the latter by replacing the accumulation of regimes in the principal article with a single arbitrary-rank singular-spectrum theorem. The exact clock quotient, its one-sided modulus, honest inference and two matching singular families are now parts of the same argument. The previous mathematics is retained in a separately compiled companion, rather than discarded or presented as a collection of new breakthroughs.

The substantive response follows the higher-latent-rank route in item 14.1 and reorganizes the clock-pencil and singular-statistical results as requested in item 14.5. The article retains the original affine action law and two unknown channels. It allows rectangular alphabets, repeated actions and rank-deficient competitors. The companion also adds an unlabelled four-anchor calibration certificate and the six requested proof clarifications. The other proposed routes in section 14 are alternatives, not assertions that this revision has also proved a universal optimal meromorphic sampling theorem or a new boundary-rigidity theorem.

## 1. Main change of mathematical scale: report sections 4, 5, 9 and 14.1

Theorem 1.1 (`thm:v87-main`) treats every fixed latent capacity k, with m1,m2 at least k. Write

    P(T) = A + B/(T-h),
    kappa = sigma_k(U) sigma_k(V),
    gamma = ||B||_F,
    theta = kappa gamma/(kappa + gamma).

For a true parameter with theta > 0 and **every** competitor in the closed model, it proves

    d_infinity(spectrum, spectrum') + |h-h'|
      <= C min(1, ||P-P'|| / theta).

There is no competitor rank floor and no lower bound on individual action gaps. Only a positive weight floor, fixed dimensions and a compact clock/action geometry enter the uniform constants. With a lower bound on total action spread, theta is bounded below by a constant times kappa; partial eigenvalue collisions remain allowed. Full-spectrum collapse is different from partial collision and is explicitly included as a second singular boundary.

The proof does not take a higher-degree determinant and invoke separated-root derivatives. It clears the recovered common pole and multiplies the candidate affine pencil by the **true** two channel inverses, used for comparison only. The pole error remains diagonal in these coordinates. The coefficient error is therefore delta/kappa + delta/gamma, not delta/(kappa gamma). An invertible candidate leading coefficient forces both reduced candidate factors to be invertible, so the candidate roots, with multiplicity, are exactly the target spectrum. Lemma 3.1 proves the required gap-free matching bound by a disk-counting homotopy. No channel inverse is supplied to the estimator.

This is the point that replaces the special binary determinant bookkeeping. Section 8 recovers the v86 determinant-product law from sigma_2(U) comparable to |det U|, and the same statement for V. The historical arbitrary-rank exact pencil theorem is explicitly credited; exact identification alone is not presented as new.

## 2. A quotient-invariant formulation and attained statistical orders

A weakest-channel product need not be invariant under the additional factorization gauges of a repeated spectrum. Equation (1.5) therefore defines theta_*(P) as the maximum of theta over the compact exact observation fibre. Theorem 1.1 makes its spectrum and pole well defined whenever theta_* is positive. At simple spectra, normalized stochastic factors are unique up to simultaneous permutation and theta_* = theta. At repeated spectra the definition remains representation-independent without assuming an unproved explicit factorization formula.

Theorem 4.2 constructs a minimum-residual estimator and a confidence region over the entire closed model. Neither signal floor is supplied. The risks and expected diameters have orders

    min(1, 1/(N theta_*^2)),    min(1, 1/(sqrt(N) theta_*)).

Sections 5 and 6 give different positive families attaining these two losses. For every k and every admissible rectangular alphabet, the first family changes a pair of actions and reciprocally rescales two channel contrasts. Both observable marginals stay **exactly** fixed at every clock; the joint-law difference is an explicit multiple of epsilon_u epsilon_v (lambda^{-2}-1) e f^T. Its channel singular product is computed exactly. Setting either contrast to zero gives an exact nonidentification fibre.

The second family keeps both channels full rank and shrinks the whole action spread. It satisfies

    P_t(T) - P_0(T) = t B / ((T-a-t)(T-a)),   ||B|| comparable to spread.

At zero spread the common action is unobservable. Thus the extra contrast term cannot be discarded even with well-conditioned channels. Theorem 7.1 proves matching minimax orders on theta_*-bounded classes and matching honest-diameter lower bounds at the displayed families. A conditional relative-entropy argument proves the same lower bounds for predictable randomized clock selection anywhere in the fixed clock interval. They are finite-experiment statements, not asymptotic normality assertions.

The claim is a uniform sharp order with explicit attaining strata, not an unproved classification of every anisotropic direction in every detector model. The abstract, theorem hypotheses and closing discussion use the same scope.

## 3. Shared apparatus: report sections 2 and 12.1–12.2

The exact two-clock theorem and its one-clock geometric alternatives remain in the companion, with all their original hypotheses.

Companion Lemma 19.1 (`lem:v87-finite-level`) isolates the finite-level topological argument. It proves density of the complement of finitely many action levels and extends equality by continuity. The proof expressly does not require eigenvector continuation or locally constant label choices.

Companion Proposition 19.2 (`prop:v87-anchor-certificate`) adds a quantitative **unlabelled** four-anchor result. Over the sixteen inversion patterns it defines two finite certificates: the least active singular value lambda and the least inactive residual d over a compact positive calibration rectangle. Both are proved positive by the four-distinct-level obstruction argument. When the odds error is small compared with d, the residual minimizer selects an active pattern and its calibration error is at most C epsilon/lambda. Thus nearly repeated anchor levels and nearly admissible swapped calibrations appear as distinct conditioning factors; correct labels need not be supplied.

This is a genuine addition beyond the correctly-labelled inverse. Matrix-to-odds conversion still requires regular anchors, and neither this proposition nor the principal theorem is advertised as a global spatial Lipschitz/minimax theorem through two-clock profile collisions. The exact spatial theorem and its quantitative domain are now explicitly distinguished, as requested in 12.2.

## 4. Geometry, divisor counts and the original physical action law: sections 3 and 6–8

The geometric lower example uses actual metric alternatives and remains intact. The metric reconstruction step continues to cite its classical boundary-rigidity hypotheses. The revision does not manufacture a new geometric theorem by renaming that transfer.

Every rational, compact-surface and branched-clock theorem is retained in the companion. The sufficient divisor clock budgets retain their stated scope. The principal article instead has one sharp clock threshold within its arbitrary-rank affine experiment: Proposition 2.2 gives the exact fixed-channel two-clock fibre, and Theorem 1.1 gives its three-clock resolution. This threshold and the singular modulus arise from the same rational curve.

The unchanged logarithmic ratio law is displayed in section 1 of the principal paper. The positive-genus original-action branched-clock example is also preserved. Companion section 19 gives more precise whole-fibre support candidates, not merely membership of an action value in the image of supp(D).

## 5. Article architecture and preservation: report sections 9–10

The principal article is now a self-contained ten-page theorem paper. Its progression is: projective model; exact clock fibre; gap-free one-sided inverse; residual inference; product singularity; whole-spectrum collapse; sharp statistical orders. The latter results use the same model and inverse theorem, rather than unrelated observation premises.

The 122-page companion contains every mathematical input of the previous expanded edition. Static source verification checks inclusion of all 47 inherited TeX inputs other than the three obsolete wrappers/frontmatter, and preservation of all 402 inherited cross-reference labels. Independently, all 1,764 files in the reviewed-source archive were checked byte-for-byte against the local preserved tree. These files are not rewritten on the revision branch. New wrappers repair compilation while leaving the historical mathematical sources intact.

This implements the report's distinction between an article and a research archive. The companion is part of the revision package; it is not a deletion list.

## 6. Adversarial literature positioning: report section 11

The principal predecessor discussion is organized around the strongest immediate comparisons: latent-structure diagonalization, bilinear identifiability modulo transformations, matrix spectral perturbation, statistical observation moduli, weak identification and mixture singularities. `LITERATURE_AUDIT.md` records the corresponding challenge to each principal assertion and the exact additional statement established here.

In particular, neither ordinary spectral identification, the abstract modulus-to-risk principle, nor the general phenomenon of nonshrinking honest sets is claimed as new. The contribution to test is the two-loss, one-sided, gap-free projective action modulus and its attaining arbitrary-rank families, including adaptive-design lower bounds. The Ho–Nguyen bibliographic entry was checked against the publisher and corrected to SIAM Journal on Mathematics of Data Science 1 (2019), 730–758. The literature comparison is a delimited audit, not a claim to have mechanically certified priority against all publications.

## 7. All six proof-level requests in section 12

| Request | Revision location and mathematical action |
| --- | --- |
| 12.1 Finite-level global argument | Companion Lemma 19.1; closed finite preimages, dense complement and continuity, with arbitrary pointwise label switching allowed. |
| 12.2 Collision and stability scope | Companion Proposition 19.2 and surrounding discussion; quantitative unlabelled anchor certificate, with regular odds extraction and no hidden global profile-collision bound. |
| 12.3 Determinant coefficient cancellation | Companion equation (19.3) explicitly expands det(K-eQ)-det(K); both affine scalar interpolants and all three determinant coefficients are written out. The second perturbation has a bounded-set C(R+1)nu estimate before division by rho. The principal proof supplies its higher-rank diagonal counterpart. |
| 12.4 Hoeffding radius | Principal Theorem 4.2 and companion section 19; entrywise error t gives sqrt(q)t, hence exactly 2t for binary four-cell matrices. |
| 12.5 Imaginary periods | Companion section 19; handle periods plus puncture loops are specified, with the latter equal to 2 pi i times their real residues. |
| 12.6 Whole branched fibres | Companion section 19; secant fibres require the entire reduced fibre bounded by D, while tangents require sum(ep+1)p bounded by D. These necessary support tests do not replace membership in E. |

## 8. Actual build and verification status: report section 13

The reviewed v86 workflow subsequently failed at native full compilation; it was not merely awaiting evidence. Its wrapper used a digit-containing TeX control sequence. In the new companion wrapper this is bypassed without changing the inherited mathematical files. Full compilation also exposed the limit of alphabetic appendix numbering after 26 sections; the new wrapper uses an unbounded A1, A2, ... convention.

Both v87 editions have been built locally with native latexmk/pdflatex, with resolved references and citations, no duplicate labels/bibliography keys and no overfull boxes in the final logs. `verification/v87-local-verification.json` binds the diagnostics to SHA-256 hashes of every included source. `verification/v87-local-build.json` records actual PDF hashes, page counts and the diagnostic program hash. The branch-specific workflow independently rebuilds the two editions and records its own exact source commit, logs, PDF hashes and verification output. A local record is not presented as a successful GitHub Actions run; those are distinct evidence files.

The executable diagnostics check seven symbolic identities, twenty matrix-curve cases, twenty spectral matching cases, 120 positive/singular product-family cases, twenty collapse cases and all sixteen four-anchor patterns. They supplement the written proofs and source review. They do not certify a mathematical theorem or an editorial decision.

## Reading order for renewed review

Read Theorem 1.1 and its proof in section 3 first; then the exact families in sections 5–6 and Theorem 7.1. These are the proposed answer to the report's main scale objection. Companion section 19 contains the six requested proof clarifications and the additional unlabelled calibration certificate. All preceding mathematical regimes remain available in the same companion and unchanged historical sources.

This response concerns the owner's independent, external-referee-style review of the pinned repository manuscript; it does not represent a journal decision or a commissioned journal report.
