# Response to the v21 referee report

**Paper:** Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
**Report:** `b263abc35b2aacb038185d66c5cb13f488d3fe93`, report blob `38f9de41c756221a86718e897ec548faecbfcff5`  
**Reviewed author:** `5ab3be483386dab1b2f53575f47dbf7aebd92bd3`  
**Revision:** A2 v22, 29 September 2026

We thank the referee for separating the correctness of the preceding results from their information contract. The central question in this revision is whether the observed records themselves can certify that no obstacle or period is missing. The new answer uses the absolute free-area normalization already present in the local law. It does not add a sensor, change the billiard topic, or infer correctness from a venue aspiration.

For a connected observed component, let I be its recovered shape types and Gamma its recovered rank-two cycle group. Theorem 1.2 proves

`covol(Gamma) - A - sum_{i in I} area(C_i) = ([Lambda:Gamma]-1)covol(Lambda) + sum_{i not in I} area(C_i)`.

Both right-hand terms are nonnegative. Vanishing of the observable left side certifies both full obstacle coverage and full period generation, without assuming either. The arithmetic must be recovered before substituting any area calibration; Lemma 4.3 provides precisely that noncircular step. The main paper then proves reference-free finite-error certification and a separate sharp physical area-testing result.

## 5.1. Geometry-aware scanner versus data-based certification

Section 6.1 retains the finite-aperture scanner as a sufficient producer and states its geometry primitives explicitly. We do not claim to learn those primitives from unmarked trajectories. Theorem 1.2 and Corollary 3.4 instead apply to any finite genuine record collection. Neither a scanner's exhaustiveness assertion nor the existence of an unobserved reference witness is an input. The completion defect certifies sufficiency from the received laws, including their absolute normalization. A complete aperture scan guarantees eventual acceptance, but the certificate can justify stopping before the scan is finished.

This is a change in the mathematical acquisition guarantee, not a claim that all local experimental access has disappeared. Local origins, branches, paired windows and the absolute phase law remain. Fabricated records and arbitrary mixtures of unknown branches are outside the physical observation model.

## 5.2. Per-table finiteness and uniform complexity

Section 6.1 explicitly separates a finite aperture for each fixed periodic table from a uniform number of bodies/tests. The latter requires the separation prior d0 and the packing estimate, not merely r0, D0, rho0 and R. The new noisy certificate states its separate lower covolume V0 and lower obstacle area a0 inside the prior definition and Theorem 1.3. These bounds have different roles: V0 gives rational-denominator and rank separation, while min(V0,a0) gives the completion gap. No hidden uniform scan bound is claimed.

## 5.3. Reference-free rather than reference-chart recovery

Theorem 1.3 is uniform on a closed bounded analytic class that need not lie in one local deformation chart. The inputs are bounds and separation margins, not a reference table, known shapes, known incidence, known copy labels or witness-key neighborhoods.

Lemma 4.2 clusters the recovered individual shapes using the fixed distinct-shape margin, retains every observation as a multigraph edge and aligns sources using asymmetry. It deliberately does not classify distinct edge keys; loops, repetitions and near-coincident surplus channels cause no edge-clustering requirement. Lemma 4.3 selects a determinant-separated cycle pair, recovers rational coordinates by a finite denominator bound, and computes the integer group before the area test. This directly addresses the reference dependence identified in the report.

## 5.4. Qualification, omissions and witness retention

Uniform physical branch validity and the stated density/geometry margins remain model assumptions. They cannot be inferred for an arbitrary fabricated pair of functions by an algebraic quotient. This boundary remains explicit in the abstract, Theorem 1.3, Proposition 2.4 and Section 4.

Actual witness retention, however, is no longer assumed for the certificate's soundness. Corollary 3.3 proves a positive gap for every incomplete rank-two component. The test in (4.6) distinguishes complete saturated components from incomplete ones on a simultaneous error event. Rank-deficient components receive no certificate. Arbitrary omissions, including data-dependent deletions of the controlled finite list, cannot produce false completeness in the model; they may prevent acceptance. Corollary 5.2 gives error-spending control over repeated inspections and a separate explicit probabilistic encounter condition for eventual acceptance. The latter is not asserted for an unspecified unmarked-trajectory scanner.

## 5.5. Function-valued sensor and normalization

The abstract and Section 1.1 say two endpoint density functions or two growing histograms, not two scalar observations. Failure and outside-rectangle outcomes are kept, and preparations are not conditioned on success or renormalized to the spatial aperture. This is essential rather than incidental: hidden bodies change A even if they never enter a selected successful return. The completion identity would not follow from success-conditioned densities.

The local lens-information equivalence and its proof are retained byte for byte in Section 2. No claim of ordinary collision-count, marked-length or unmarked-trajectory rigidity is substituted for the endpoint-law theorem.

## 5.6. Analyticity and genericity

Analyticity still extends observed arcs to full bodies; asymmetry gives unique relative placement; distinct-shape separation identifies types. These assumptions are prominent in all whole-table statements. Symmetric and repeated-shape results remain in the original registered/finite-candidate information categories in the retained volumes. No exact analytic count-only rigidity or nonrigidity is inferred. The local two-arc inverse itself remains smooth and independent of an all-order jet recursion.

## 5.7. Mathematical certificate versus efficient algorithm

The primary gives an explicit finite arithmetic stage, implemented in `tools/certificate.py`, after physical shapes and cycle estimates have been recovered. It uses rank separation, bounded rational reconstruction, column Hermite reduction and the defect gap. Its error bounds are inputs; the implementation is a floating diagnostic for that conditional arithmetic stage, not interval-certified analytic-body reconstruction.

The preceding physical fitting and analytic continuation remain compact-class existence operations. We do not transfer polynomial-time integer normal-form results to the entire inverse or scanner. The new mathematical content is the global completion identity and its reference-free noisy realization, not an unsupported efficiency claim.

## 5.8. Source qualification and previous queued run

The revision starts from the latest review head and preserves the complete reviewed v21 paper tree exactly at `retained/v21`. Its nested historical tree and both earlier supplements are unchanged. The v21 local evidence and queued workflow are not relabelled as v22 evidence.

The new validator has a v22 schema, full source hashes and a read-only exact-triggering-SHA workflow. Local execution actually passed 5,110 new finite checks and 3,635 explicitly selected retained local checks, including 90 nonlinear curvature comparisons. Both Python modes agree. The 17-page primary compiled without final TeX diagnostics; all pages were visually inspected. This local run is source-content execution, not a Git checkout, and did not rebuild retained volumes. The hosted all-volume outcome must be read from its own run; the response does not assert a pass before one exists.

## Conceptual and statistical contribution

The previous all-cycle index formula used a covolume calibrated after coverage was assumed. Here the unobserved area is retained as a positive term. This makes the same normalization a certificate against both hidden obstacle types and unsaturated periods. Bounded-denominator decoding prevents circular use of the conclusion in recovering the subgroup.

Theorem 5.3 also constructs actual analytic tables with a small unseen obstacle whose only effect on the selected endpoint laws is the exact normalization tilt. A Bernoulli relative-entropy argument proves a lower testing scale N^{-1/2}, and the success proportion gives a matching upper scale in that fixed-window physical family. This explains the need for a lower area margin for uniform completeness decisions. It is not a whole-table minimax theorem or a sharp analytic-continuation rate.

The primary is organized around this completion question. All preceding results are supplied intact rather than discarded. The new claims, including their conceptual significance, remain subject to independent mathematical and editorial judgment; finite diagnostics and compilation are not that judgment.
