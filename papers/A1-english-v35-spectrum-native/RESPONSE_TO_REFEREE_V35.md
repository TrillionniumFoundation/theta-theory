# Response to the independent referee report on A1 v34

**Revised manuscript:** *Attainable information and causal compression at exponent collisions*, A1 v35.  
**Author:** Qian Qi.  
**Controlling report:** `reviews/a1-english-v34-harsh-independent-2026-09-08/REFEREE_REPORT.md`, at `a177077ede2b64e11af1efb016eaa6bb5ddf2a13`.  
**Reviewed manuscript:** `03a4788efb3cf643bc2cd60257c5ed290bb0570d`.  
**New branch:** `revision/a1-english-v35-spectrum-native-2026-09-08`.

We thank the referee for identifying a bounded remaining revision: a closer theorem-level comparison for the principal attained collision law, a current native publication build, and a more economical presentation of the one-step realization algebra. The revision addresses these requests without changing the principal theorem, imposing a prior density, reducing the horizon, enlarging the retained resource, or removing companion results. This response concerns the controlling v34 report, not the separate second v33 report.

## R34.1 — Clustered spectra, superresolution, and acquired information

**Location:** Main article §13.1–§13.2, pp. 37–39; introduction; bibliography [14]–[15]. Source: `v35/spectral_comparison.tex`, `v35/introduction.tex`, `v35/references_main.tex`.

The comparison now starts with the full Fourier–Vandermonde spectrum. It cites the precise single-cluster and multicluster statements of Batenkov–Diederichs–Goldman–Yomdin, Theorems 2.2–2.3 in arXiv:1909.01927v2, rather than treating this literature as a bound only on the least singular value. The article records their cluster-separation, cluster-diameter and bandwidth regime, the single-cluster scales, and the comparison with the ordered union of cluster spectra. Their dependence on a varying bandwidth is not claimed by our fixed-horizon result.

The connection is mathematical, not only terminological. Proposition 13.1 (`prop:v35-exterior-spectrum`) proves, for fixed matrix size and sampling length, that every initial product of singular values is uniformly comparable to the corresponding maximal Vandermonde volume, including exact repeated labels. The proof uses alternating-polynomial factorization, bounds for the exterior matrix, and an explicit consecutive-row minor. No division by a vanishing numerical gap is used. We identify this as an elementary comparison result, not a new sharp growing-bandwidth spectral estimate.

Corollary 13.2 (`cor:v35-spectral-envelope`) rewrites the acquired all-budget envelope in these spectral products. Its upper index is the acquired cutoff `min{n(r−1),q_m}`. The interpretation as unconditional or worst-history prediction regret, and as the risk of one common causal controller, still uses the acquired tangent, actual command-and-report minorization, whole-image covering theorem and reachable raw-moment recursion. This identifies exactly what an auxiliary matrix estimate supplies and what the experiment-level proof must additionally establish.

Corollary 13.3 (`cor:v35-fixed-future`) gives a positive comparison inside the existing detector family. With the same two-trial future menu, the nine spectral scales are comparable to `(1,1,1,1,1,1,rho,rho,tau)`. Acquisition lengths one, two and three truncate this same spectrum at dimensions three, six and nine and give the stated distinct checkpoint envelopes. Their respective total horizons are explicitly `n+2`. This is not a new multi-checkpoint causal-price claim or a change to the five-trial example.

Section 13.2 separately addresses Batenkov–Demanet–Goldman–Yomdin, Definition 3.13 and Theorem 3.14 in arXiv:1809.00658v2. It acknowledges their statistical minimax consequences for unknown-support, complex-amplitude sparse-grid recovery from noisy Fourier data. The bandwidth, grid spacing, normalized noise, coefficient loss, clustering parameter and separate upper/lower quantifiers are stated. A persistent-label budget is not substituted for bandwidth or inverse noise. Their reconstruction experiment and loss are not described as having no statistical content.

Remark 13.4 (`rem:v35-flat-path`) makes the already valid distinction between the determinant theorem and the finite-power collision-tree corollary concrete. A smooth flat two-parameter path has exponential crossover budgets and is treated directly by the determinant law. No extra finite-order path assumption has been imposed on the principal theorem.

The exceptional-journal case is consequently stated in terms of the actual mathematical conclusion: the collision scales of the future test system become a jointly calibration-and-budget-uniform memory law through the family that the past experiment acquires, and the upper law is achieved by one per-report label process. The comparison does not purport to certify worldwide priority or to subsume the cited varying-bandwidth results.

## R34.2 — Complete current native publication build

**Locations:** `v35/build_native.py`; `verification-v35/NATIVE_BUILD_V34_CURRENT.json`; `verification-v35/NATIVE_BUILD_V35.json`; `verification-v35/VISUAL_INSPECTION.json`.

Both requested publication objects were built: the exact reviewed v34 main and companion, followed by the revised v35 main and companion. A cached historical source package was used only after Git-object verification against the pinned repository. Overlaying 79 cached TeX objects on the reviewed native tree returned that same tree hash. The current v34 main and its four changed modules were separately checked against their exact repository blob hashes. The alternate local-only v34 export was not substituted for the reviewed manuscript.

Each native build started without generated external-label exports. The builder compiled both full entrypoints, generated exports from their actual auxiliary files, and reached a stable pair after three paired cycles. Initial bootstrap warnings were not treated as final resolution; both final logs were separately checked. The TeX-recorder source closure matched the declared active input closure. No theorem marker, fabricated external reference or smoke-build input was used.

The current v34 build produced a 39-page main article and 159-page companion from 79 active TeX inputs. The current v35 build produced a 42-page main article and 159-page companion from 80 active TeX inputs. Final logs contain no unresolved references or citations, multiply defined labels, changing labels, or overfull horizontal or vertical boxes. Receipts record every active source Git hash, compiler, pass return code, log hash, converged external-label hash and PDF hash.

The new build was executed before creating its revision commit, so its source-commit field is deliberately null. The source-object manifest identifies the exact compiled text; the publication can be checked against those objects without pretending that an uncreated commit was built. Full execution receipts, stdout logs and generated PDFs accompany the downloadable review package. The repository contains the native source, executable builder and compact receipts retaining all active Git source hashes and execution facts.

Rendered visual inspection covered main pp. 1, 37–39 and 42, and companion pp. 1, 80 and 159. No clipping or overlapping material was identified in those samples. This is not represented as visual inspection of every page. All 159 companion pages have identical extracted text to the independently rebuilt current v34 companion. This is current integration evidence; it neither retracts nor repurposes the genuine historical v33 build.

## R34.3 — Economical Blackwell exposition and preserved quantifiers

**Location:** §8.1, `v35/moment_controllers.tex`; preservation record `verification-v35/PRESERVATION.json`.

The Blackwell proposition retains the complete identification proof, Bayes support interpretation and common-submeasure argument. The following lemma retains the full weak-star compactness proof and explicit support maximization; its duplicated kernel-identification calculation now cites the preceding proposition. The overlap corollary uses that established common-submeasure bound, treats equal rows directly, and retains the positive overlap and proper-inclusion conclusions. A short transition states the separate role of each result.

All inherited theorem-like statements in the active two-volume source remain verbatim: 218 blocks consisting of 67 theorems, 54 lemmas, 39 propositions, 47 corollaries, nine definitions and two remarks. Of 207 inherited proof blocks, 205 remain verbatim; the two just described have proof integration, not a removed mathematical assertion. The original complete proof text remains in the inherited `v34/` module and on the untouched v34 branch. All companion sources and historical subtrees are retained.

The distinctions requested by the referee remain beside the relevant statements: finite-dimensional representation versus effective global computation; prescribed acquisition versus controlled acquisition; mean versus worst-history loss; fresh private randomization versus a persistent decoder-indexing seed; fixed-budget continuity versus joint all-budget collision estimates; and the determinant theorem versus its finite-power tree specialization. No additional optimization, density or efficiency assumption has been introduced.

## Executions and evidentiary scope

The unchanged author diagnostic and independent referee diagnostic were rerun with ordinary Python and `python -O`. Their respective outputs agree byte for byte; the independent core program again passes its 298 explicit exact checks. The new comparison program likewise agrees across the two modes and checks 52 exact polynomial factorizations, 28 high-precision exterior comparisons, 72 exact arrangement-volume brackets and two symbolic crossover identities. Its checks use explicit failures, not removable Python assertions.

These are finite diagnostics. They are not proofs of uniform estimates over a continuum, a formal proof-assistant certificate, or an exhaustive search for optimal continuous controllers. The analytic proofs are contained in the complete manuscript. We submit this revision for a fresh assessment of the theorem's originality, significance and presentation; neither the build nor the diagnostics determine an editorial decision.
