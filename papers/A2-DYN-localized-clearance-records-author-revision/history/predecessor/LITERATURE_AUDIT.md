# Primary mathematical literature audit

The current native manuscript cites four external mathematical sources, in addition to its exactly preserved internal historical articles. Each external source was inspected at an actual primary version. No external theorem is used to replace a missing physical hypothesis. The current full-word pressure theorem has its own native proof.

## Retrieved versions

The actual public PDF retrieval and native `pdfinfo`/`pdftotext` extraction ran on **21 October 2026, 00:51:41–00:51:42 UTC**. The receipt is `audit/literature/FETCH_PRIMARY_PDFS.json`. The version identifiers below come from the downloaded first pages; the unversioned public URLs currently served these exact bytes. Earlier web inspection used the same versions. A subsequent attempt to open version-suffixed arXiv URLs in the browsing service returned a service error; the successful direct public downloads, hashes and extracted statements are the evidence for this audit.

| Key | Primary source and actual inspected version | PDF pages | SHA-256 of downloaded PDF |
|---|---|---:|---|
| DZUniform | Demers–Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, [arXiv:1210.1261](https://arxiv.org/pdf/1210.1261), v1, 3 October 2012 | 45 | `f20938fe161c0b4acd775bcd26ed2df1e1dba6901b8d04438359648b528f5e7f` |
| BDPressure | Baladi–Demers, *Thermodynamic formalism for dispersing billiards*, [arXiv:2009.10936](https://arxiv.org/pdf/2009.10936), v3, 31 August 2022 | 62 | `3b8efc436aa4e276821252d2c1b23297d486928c3ebb0f44c6e2d56296f3d2e3` |
| DNFlow | Dolgopyat–Nándori, *On mixing and the local central limit theorem for hyperbolic flows*, [arXiv:1710.08568](https://arxiv.org/pdf/1710.08568), v1, 24 October 2017 | 35 | `b2f683268e2406d7933812b26d3d33429d09cfd5ab92ad135db3377030bf2d60` |
| BVNotes | Boyd–Vandenberghe, *Convex Optimization: Duality*, [official Stanford slides](https://web.stanford.edu/class/ee364a/lectures/duality.pdf), retrieved current version, with revised-slide attribution to Parth Nobel | 40 | `67237c18e9150db5597acaa5d656dc5a70196e4c1c5ad0fce6dd12a96a188fc6` |

The public PDFs need not be duplicated in the article: their exact content identities, URLs, extraction metadata and inspected locators are supplied. Earlier downloaded literature and its original audit remain unchanged in the predecessor. Published bibliographic entries and these preprint/slide versions are distinguished; their pagination need not agree.

## DZUniform: the particular growth lemma used

**Inspected:** Lemma 3.2(b), PDF page 12; H2–H4, pages 9–10; the separate anisotropic-space construction, pages 10–11. The lemma bounds a sum of homogeneous branch inverse arclength-Jacobian suprema uniformly over the qualified map and short-curve families. Its constant depends on the subdivision scale, one-step contraction, norm-comparison and distortion data. Its proof explicitly uses H2–H4.

The physical application supplies invariant bounded-curvature cone curves, adapted one-step expansion and the requisite distortion in native 281–283. The momentum/canonical sources use the enlarged allowance and its **own** cutoff, short length and growth constant in 284 and 324. The first nonhomogeneous source image is constructed before the lemma is applied. Time reversal changes the curve orientation with the actual physical map. A pointwise terminal-momentum kernel is not substituted for a sum of branch suprema.

The full spectral perturbation theorem additionally uses its strong/weak spaces and further hypotheses. The present source-growth application does not verify that entire theorem for the joint marked operator. The current notes correct the retained page-14 locator to page 12 for this inspected version.

## BDPressure: no implicit radius-uniform pressure import

**Inspected:** Lemma 3.6 and its cell argument, PDF pages 16–20; Proposition 3.14, pages 25–27, with its potential conditions and the preceding homogeneity choices. The latter compares long-curve weighted complexity with the full pressure partition, using actual Cantor rectangles and a mixing crossing time. Its potential regularity/bounds, parameter intervals, long-curve condition and thermodynamic partition data are part of the statement and proof.

Those objects are not identified with the native `q=2` partition merely by notation, nor made uniform over the radius family by compactness alone. The relation `q t_0/2>=2` must not be silently applied with a different exponent. New 326 instead proves the original physical-word pressure through actual boundary stopping, native cross-curve comparison, and complete canonical/marked source budgets. This external paper provides context, not the unproved uniformity in that proof.

## DNFlow: actual tested limit and arithmetic hypotheses

**Inspected:** Definition 2.2 and its continuation, PDF pages 3–4; the finite-horizon Sinai-billiard application, Section 6.4 and Proposition 6.3, page 32. The mixed local limit concerns a square-integrable vector observable, a bounded almost-everywhere continuous coboundary, a closed subgroup/translation and positive covariance. It is stated against bounded continuous endpoint tests and a continuous compactly supported observable test, with the indicated compact-set uniformity. The billiard-flow proposition retains its minimality and linearized-group alternatives; its further nonarithmetic conclusion has its additional hypothesis.

The physical finite-horizon flow is relevant, but this tested convergence does not establish the current exact-label roof essential supremum or its full four-coordinate arithmetic reference. The original observable, conditioning, near-unit spectral peaks and probability quantifiers therefore remain. No averaged or tested limit is substituted for the raw target.

## BVNotes: background only

**Inspected:** weak/strong duality and Slater qualification, PDF pages 14–15, and the convex KKT statements, pages 22–23. Strong duality requires a suitable qualification; it is not automatic for an arbitrary formal action domain. Native 297 proves the special disk-product duality directly. The slides supply background terminology, with no new dynamical or physical-orbit claim inferred from them.

## Internal source references and new proof dependence

The bibliography's historical A2-DYN articles are supplied through their pinned native source graph and complete preserved article trees. `CURRENT_SOURCE_ANCHOR.json`, `HISTORY_PRESERVATION_AUDIT.md` and the predecessor's original source ledgers identify the exact commits and mathematical objects. They are read with subsequent proved corrections, rather than treated as external expert validation.

The new 323–326 proofs use the identified native statements, ordinary finite-dimensional differential/coarea calculations, elementary interval arguments, finite analytic expansions, integration by parts and positive exhaustion. Their text supplies the needed arguments. No newly invoked external spectral, analytic-stratification, clearance-abundance or local-limit theorem is left as an unidentified black box.
