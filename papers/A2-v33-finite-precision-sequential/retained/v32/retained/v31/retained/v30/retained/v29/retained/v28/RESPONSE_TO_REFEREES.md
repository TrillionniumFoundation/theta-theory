# Response to the latest A2 v26 referee report

**Manuscript:** Qian Qi, *Reference-free certification from intrinsic boundary laws*  
**Report:** 3 October 2026; commit `24b9c5f6a586a35975e6f6b67d25ec431390f57a`; blob `49d522f04930a0c4d9b3fd3ac3c555a8895596eb`  
**Reviewed author:** v26, `8c6f1113296c5401258ff052e5ce734fabfb3909`  
**Intervening author revision:** v27, `f230e014911f3b7104db0ec742969789ed5a88c9`  
**Current revision:** v28, 3 October 2026

We thank the referee for separating the correctness assessment from the observation-model and significance objections. We retain the original topic and all prior mathematical results. The intervening v27 already removed adaptive recentering, growing apertures and endpoint histograms from a new global route. The present revision does not recount those changes as new. It removes a further structural assumption: exact first-impact rigidity now allows arbitrary repeated shapes and a nonprimitive bounded presentation. The new argument recognizes a period by its action on a complete central patch, not by an individual shape fingerprint.

## 1. Endpoint bodies and clearance

The corrected passage in Section 6, `core/03_recognition.tex`, is preserved byte-for-byte from v27. The middle-segment distance test excludes exactly the two physical endpoint components, not every component of the same shape. Other bodies retain the cloud-distance enclosure, while the two endpoints are treated by their facing supports and explicit collar/tube inequalities. Thus equal-shape copies are not inadvertently deleted from the obstruction test. The original v26 text is preserved as a historical source, not silently declared corrected in that source. The new fixed-aperture repeated-motif route does not use a clear-return network at all.

## 2. Full sensor contract in headline statements

The abstract, Definition 1.1 and Theorems 1.2 and 1.6 specify uniform resettable launch positions in one fixed laboratory square, independent uniform directions, a fixed short first-impact cutoff and certified collision-position error. A solid start, no hit or discarded outer hit counts as an attempted launch. Only first-impact positions are retained. No later impacts, return selection, arclength marks, incoming/outgoing angles, endpoint histograms, free-area normalization or adaptively placed cloud squares are required by the new route.

This is a restriction of the previously declared controlled collision apparatus, not a reduction to passive trajectories, counts or marked lengths. In the exact theorem even the weights of the position law are unnecessary: its support provides the complete protected boundary patch. In the finite theorem probabilities enter through physical first-hit coverage. The common laboratory frame and numerical presentation bound remain important inputs and are not concealed.

## 3. Smooth-class priors and repeated shapes

Definition 1.1 keeps numerical component-count, bounded-presentation, separation, diameter, positive-curvature and fixed `C^(6,beta)` bounds. It removes both pairwise individual shape separation and asymmetry. Several copies of the same disk or other symmetric body can occur within a nonprimitive cell.

Lemma 1.3 proves a finite local-to-global period criterion. Since the unknown bounded presentation puts a representative of every component orbit in the central patch, a translation which preserves all those bodies in both directions preserves the whole union. Lemma 1.4 proves `[Pi:Lambda_0] <= r_0` and identifies a protected finite list generating the *full* period lattice `Pi`, not merely the supplied existential presentation. The primitive orbit count and free area follow only after period recovery.

The exact theorem requires no positive shape or patch mismatch margin. For uniform finite-confidence recovery, Definition 1.5 states a numerical margin for *nonperiod patch defects*. This is pointwise automatic because the protected candidate list is finite, but not uniformly bounded away from zero near a translation-symmetry increase. Proposition 1.8 exhibits that distinction with two equal disks per rectangular cell. Corollary 1.7 gives eventual pointwise recovery without a known numerical margin; it does not mislabel an unobservable eventual stage as a finite stopping certificate. These are complementary conclusions, not a weakening of an earlier theorem.

## 4. Launch counts versus computational complexity

Theorem 1.6 inherits the compensated-support exponent only after proving that the new finite geometric tests tolerate the same raw hull error. Every comparison has error at most `14 e`, with a further `6 e` budget for certified numerical operations. True periods and nonperiods then lie on opposite sides of the displayed threshold. Coverage uses `q` of order `nu^(3/4)` and localization error of order `nu^(3/2)`, giving the stated launch bound.

The abstract and theorem distinguish attempted launches from localization bit cost, numerical quadrature, rational/Hermite arithmetic and apparatus travel/setup. The theorem does not assert a new general random-polytope rate, end-to-end polynomial complexity or minimax optimality.

## 5. Exact-source qualification

The v26 archive-only run is not represented as a mathematical build. We separately verified the intervening v27 exact-SHA run `37123466579` and artifact `11274262739`: its receipt has `source_commit=f230e014911f3b7104db0ec742969789ed5a88c9`, `full_package_qualified=true` and `hosted_full_package_qualified=true`, and contains the ten declared document builds. The artifact digest and native tree match the sources used here. This is prior v27 evidence, not a v28 pass.

The current revision contains its own complete native checker, source/receipt negative controls, source pins and fail-closed exact-SHA driver. Its workflow installs and builds unconditionally. All-volume mode requires a clean source checkout, verifies the entire retained v27 tree, rebuilds its ten declared documents and checks that the inherited receipt belongs to the *current* source SHA. The current primary brings the declared package to eleven documents. Ordinary and optimized outputs must agree. Missing files, changed sources, a stale SHA, partial scope or a false qualification flag are explicit failures.

Actual local and hosted outcomes are recorded separately in `DELIVERY_STATUS.md` and execution receipts. The new primary is not allowed final TeX warnings. Existing stage-only layout adjustments in old volumes remain disclosed alongside their raw warnings, rather than being presented as changes to historical mathematical sources. Compilation and finite diagnostics are not human proof review, a physical experiment or a journal decision.

## The mathematical contribution and preservation

The new Section 1 addresses the generic-prior objection by a positive extension: equal-shape components no longer need unique names, and the observer need not know a primitive cell. A false root-to-copy displacement is rejected by a witness elsewhere in the central patch. Period generation, primitive component counting and area recovery therefore survive repeated motifs.

The eight v27 core files remain active and unchanged. The complete native v27 tree, including all earlier retained manuscripts and Supplement S, is supplied at `retained/v27`. The record-local intrinsic inverse, area defect and sequential results are not deleted or replaced. The literature comparison distinguishes the new bounded-period reconstruction from local crystallinity criteria for general Delone sets and from boundary/lens or exterior travelling-time rigidity. No claim of unique priority or of automatic four-journal acceptance is inferred from the finite checks.
