# Response to the independent A2 v47 referee report

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Revision:** A2 v48, September 14, 2026  
**Author:** Qian Qi

The report addressed here is `reviews/a2-v47-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md`, frozen on review branch `review/a2-v47-independent-harsh-top4-2026-09-14` at commit `757f2ee4e3bf766d2eb56d972e6d2f621b3fd2a6`. Its mathematical source is v47 commit `219b39e94b14187561dc3b7e5bdbae49dbd92cc2`, not the workflow-preparation or product-retention commit. This is an author-requested, AI-assisted referee-style exchange, not a commissioned journal report.

## 1. The editorial issue and the substantive response

We thank the referee for distinguishing the correctness of the v47 calibration results from the separate question of their significance. We do not treat the favorable checks of Lemmas 19.7–19.8, Theorem 19.9 and Corollary 19.10 as an endorsement at the requested journal level. Nor do we respond by adding another concentration estimate or by declaring a stronger sensor equivalent to the intrinsic observation.

Revision 48 is organized around **Theorem A**, a single structural statement about the same marked, single-offset boundary-law map. Its exact global clause brings the existing relative-law, signed finite-remainder and unknown-lattice inverse into one visible statement. Its differential and finite-dimensional coordinate clauses are proved in the new Section 20, rather than inferred from exact injectivity.

The new geometric conclusion is **infinitesimal periodic rigidity with movable contacts, obstacle shapes and marked lattice**. Vanishing gap derivatives and vanishing interior law derivatives imply that the entire analytic table variation is one common infinitesimal proper Euclidean motion. After fixing that gauge, the derivative is injective. On every immersed finite-dimensional common-strip analytic-support model, a finite selection of gaps and smooth interior law expectations gives local coordinates, with a local inverse bound in every fixed real support norm.

The proof has four geometric stages. First, the parameter derivative of the law is justified, including differentiation of its moving-support normalizing integral. Second, the four-density identity and the smooth finite-jet recursion are differentiated at each fixed order, preserving the odd labelled contact terms. Third, analyticity of the *variation* propagates a stationary contact jet to an entire stationary channel-frame image. Fourth, a finite Bezout harmonic witness makes incidence registration differentiable, and the displacement cochain gives `dot L = (dot v_1, dot v_2) M^{-1}` for the unknown lattice. Only then are finite-dimensional duality and the inverse function theorem applied to select scalar coordinates.

We regard the final finite-dimensional linear-algebra and inverse-function steps as standard. The result requiring the geometric proof is that their common derivative kernel is exactly the Euclidean gauge for the full periodic table and the same single-offset observation. We make no claim that the elementary last step is a new general embedding principle. The significance of the completed structural theorem remains a matter for the next referee; neither a new theorem statement nor a successful build decides that editorial judgment.

## 2. R47-C1: offset variation, normalization and onset amplification

The entire v47 proof and its actual observation assumptions remain active and byte-identical. In the new numbering, Lemma 19.7 is Lemma 21.7. The fixed-box positive-part estimate and normalization bound retain both the numerator and normalizer errors. The true offset remains `d_0 + j (g_hat-g)` before any additional timing term. Nothing in the new differential section replaces this finite-error statement with an infinitesimal estimate.

The inherited exact quadratic-cap control and the flight-amplified control are rerun through `check_revision_v48.py`, in ordinary and optimized Python. They are explicitly classified as finite functional controls, not independently realized billiard examples or a proof of the relative law.

## 3. R47-C2: hard-cell edges and possibly singular chart maps

The complete cell-coupling proof is retained without changes (old Lemma 19.8, now Lemma 21.8). Its tube contains internal and outer edges. The factor two in the probability-vector norm is retained. No absolute continuity or invertibility of the estimated chart map is inserted, and no outer escape category is omitted. The dependence of the chart tolerance on grid resolution remains part of the acquisition prescription.

The new scalar tests in Section 20 have smooth compact support in a positive-density square because they serve a *different, model-local exact-coordinate theorem*. They do not replace the hard categories in the existing full-class histogram theorem. Thus the cell-edge issue has not been evaded by silently changing the physical estimator.

## 4. R47-C3: conditioning order and calibrated confidence radius

The v47 confidence theorem, now Theorem 21.9, is unchanged. The final flight number is fixed before its pilot. The proof still conditions on the good pilot history, separates finite-flight law, actual offset, nominal offset and chart errors, and applies the quantized inverse only after this accounting. Sampling is analyzed in the uncapped fresh experiment; cap failure is then charged as a separate event. We have not conditioned on success of a cap and declared the resulting data iid.

The finite-order new differential argument is not a substitute for finite-noise conditioning, and the new introductory statement identifies the physical pilot as the richer planar-position experiment it actually is.

## 5. R47-C4 and the closed R46-P1 issue

The finite joint prescription and its strict `15 eta_*/16` budget are unchanged (old Corollary 19.10, now Corollary 21.10). Grid, final even flight number, same-flight pilot precision and sample size are chosen in the proved order. All preparation failures remain charged. Corollary 21.10 retains the exact physical-clock hypothesis; the bounded groupwise timing-error form remains separately in Theorem 21.9. Neither result is recast as a theorem for arbitrary per-shot timing jitter.

The clarification adjacent to the former equation (19.19), which the report regards as resolving R46-P1, is retained in the unchanged quantized-law source. There is no reopening of that issue and no substitution of a historical v46 density formula for the corrected v47 discussion.

## 6. Observation scope and the new differential hypotheses

All inherited exact and quantitative theorems retain their original classes and conclusions. The new differential assertions have their own expressly stated regularity: a `C^1` family into one common-strip Banach space of holomorphic support functions, with `C^1` lattice columns. This ensures that the support derivative is analytic. Pointwise analyticity of every parameter slice is not used to assert analyticity of an uncontrolled derivative.

The exact theorem remains infinite-dimensional and does not impose a finite-dimensional parametrization. Finite dimensionality is introduced only in Theorem 20.6 to obtain finitely many scalar local coordinates. Those observables can depend on the base table and model. They are exact expectations, not an unproved finite-sample optimal estimator or a fixed finite vector identifying every analytic boundary.

The datum continues to include obstacle labels, channel and deck marks, transverse signs, and gap information. It continues not to supply the Euclidean lattice, its scale, its Gram form, or a common channel registration. Finite asymmetry witnesses are used in the new proof locally; the proof covers the full properly asymmetric locus by arbitrary finite gcd-one harmonic sets, not only the nonzero second-and-third-harmonic locus. The known gain matrix is inverted as given and need not be unimodular.

The complete orientation-quotient statement, the absence of a general pointwise sign-erasure inverse, the signed odd-jet recovery, the smooth finite-remainder factorization, the continuation order-before-noise argument, the direct-position benchmark and all local information results remain in the active article.

## 7. Relation to the historical variation-bundle theorem

The earlier `article/25c_analytic_variation_bundles_v25.tex` is retained unchanged. It constructs compatible fixed-contact finite-jet bundles and finite positive information designs, allowing a finite collection of positive offsets. It does not posit a finite-dimensional tangent space for an arbitrary compact analytic class.

The new Section 20 does not rename that theorem. It considers whole analytic-support families in which contact points, gaps and the lattice can move; it uses one fixed positive offset for each same-type law on each channel; it proves the precise Euclidean derivative kernel; and it obtains local scalar coordinates on any stipulated immersed finite-dimensional model. Its last paragraph makes this distinction explicit. The support-function analytic identity and the differentiated lattice cochain are necessary to pass beyond the earlier fixed-contact finite-jet statement.

## 8. Literature and significance controls

The primary records were checked again on September 14, 2026:

* Finamore–Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, submitted October 21, 2025. Its stated rigidity datum is the enriched marked length spectrum for finite-horizon Sinai billiards. We assert no reduction from that datum to the boundary-law map, or conversely. Primary record: https://arxiv.org/abs/2510.18983v1.
* Florio–Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120v5, June 3, 2021. The version record explicitly removes the earlier geometric spectral-rigidity assertion affected by Proposition 3.1 and retains the dynamical conjugacy results. The bibliography and comparison continue to cite this version. Primary record: https://arxiv.org/abs/2010.04120v5.
* Trefethen, *Quantifying the ill-conditioning of analytic continuation*, BIT 60 (2020), 901–915, DOI 10.1007/s10543-020-00802-7. This gives context for conditional continuation, not a substitute for the internal continuation proof and not a bounded-inverse justification for the new kernel theorem. Primary record: https://doi.org/10.1007/s10543-020-00802-7.

This targeted comparison is not an exhaustive priority search. We do not label the acquisition synthesis, finite-dimensional duality, or analytic identity theorem as new general mechanisms. We do not claim a spectral-data reduction, unmarked discovery, sharp minimax acquisition complexity, or fixed-finite-scalar recovery on the complete analytic class. None is used as an unproved premise of the revised structural theorem.

## 9. Preservation, writing and verification

The article has a new concise abstract and a structural introduction. The full earlier introduction is retained as “Local mechanisms and observation-specific consequences”; only its heading changes. Part I now contains that detailed local development. The inherited input order, all mathematical statements and all proof environments remain active. Exact originals of the two amended active files and the v47 source-matched active manifest are archived in `history/v47-review-baseline/`.

The preservation check verifies all 103 inherited active inputs against the actual v47 native manifest: 101 remain byte-identical in place, and the two archived originals are byte-identical before their deterministic editorial amendment. There are 105 active inputs after adding the structural introduction and differential section. The inherited combined main/companion source contains 232 proof environments, all retained; the new modules add seven proved statements, comprising Theorem A, four lemmas and two theorems. The companion is unchanged.

`tools/check_revision_v48.py` verifies source retention, active references, differentiated density/anchor identities, a three-harmonic Bezout witness, non-unimodular lattice-tangent recovery, finite contact blocks, negative controls, and the retained v47 finite calibration calculations. The native workflow builds both complete entries from the actual committed source and separately retains and verifies the published Git objects. Numerical and symbolic controls, byte identities, and successful typesetting are evidence of the checks stated, not a mathematical certification of the theorem or an acceptance recommendation. The completed source/product identities and actual visual coverage are recorded in the final v48 verification ledger.
