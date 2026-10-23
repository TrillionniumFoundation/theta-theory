# Primary literature audit for the localized-clearance author revision

Receipt paths are relative to `audit/current-provenance/`; paths explicitly described as predecessor paths refer to the unchanged `history/predecessor/` article. Current execution and remote status are reported by the integrated validation records and root `PUBLICATION_STATUS.json`. Native 327–332 are author proofs, not an independent expert review.

## Version identities and retrieval status

The new renewal proof was checked against two distinct primary versions of Demers–Zhang. Both PDFs were freshly downloaded, inspected and extracted on 21 October 2026, 22:59:13–22:59:14 UTC; the successful HTTP, PDF metadata and extraction receipts are `PRIMARY_RETRIEVAL_RECEIPT.json` and the two `demers-zhang-*-pdfinfo.txt` files. Unversioned URLs are not treated as version identifiers: the exact bytes below identify what was read. The manuscript need not redistribute third-party full PDF/text copies.

| Source version actually inspected | Pages | Bytes | PDF SHA-256 |
|---|---:|---:|---|
| Demers–Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, [author's 10 October 2013 PDF](https://faculty.fairfield.edu/mdemers/research/2013.10.10.perturbation16.pdf) | 53 | 662,784 | `1fa90861a949196bbb1c903e48a53217fbbd76ba24656c5aa1faeccac42fc66f` |
| Same work, [arXiv:1210.1261](https://arxiv.org/pdf/1210.1261), actually served v1, 3 October 2012 | 45 | 648,414 | `f20938fe161c0b4acd775bcd26ed2df1e1dba6901b8d04438359648b528f5e7f` |

The predecessor's other three primary mathematical sources remain the versions actually retrieved on 21 October 2026, 00:51:41–00:51:42 UTC, recorded in its `audit/literature/FETCH_PRIMARY_PDFS.json`. Those retained receipts and the predecessor's literature audit are covered by the fresh full-file identity verification; we do not describe those earlier readings as new downloads in this run.

| Retained primary version | Pages | PDF SHA-256 |
|---|---:|---|
| Baladi–Demers, *Thermodynamic formalism for dispersing billiards*, [arXiv:2009.10936](https://arxiv.org/pdf/2009.10936), v3, 31 August 2022 | 62 | `3b8efc436aa4e276821252d2c1b23297d486928c3ebb0f44c6e2d56296f3d2e3` |
| Dolgopyat–Nándori, *On mixing and the local central limit theorem for hyperbolic flows*, [arXiv:1710.08568](https://arxiv.org/pdf/1710.08568), v1, 24 October 2017 | 35 | `b2f683268e2406d7933812b26d3d33429d09cfd5ab92ad135db3377030bf2d60` |
| Boyd–Vandenberghe, *Convex Optimization: Duality*, [official Stanford slides](https://web.stanford.edu/class/ee364a/lectures/duality.pdf), actual retained current slide version with revised-slide attribution to Parth Nobel | 40 | `67237c18e9150db5597acaa5d656dc5a70196e4c1c5ad0fce6dd12a96a188fc6` |

## Demers–Zhang: the exact growth input

**Version-specific locators:** author PDF H2–H4 at pages 10–11, Lemma 3.2(b) at page 14, and the detailed renewal proof of Lemma 5.5 at pages 35–36. In arXiv v1 the corresponding locations are pages 9–10, page 12, and Lemma 6.2 at pages 32–33. Thus “Lemma 5.5, page 36” and “Lemma 6.2, page 33” describe different versions of the same renewal argument, not interchangeable pagination.

The relevant assumptions are an invariant bounded-curvature homogeneous curve family, uniform adapted one-step contraction of the complete inverse-Jacobian sum, and uniform distortion along homogeneous iterates. The full perturbation/spectral theory additionally builds strong and weak anisotropic spaces and imposes its other hypotheses. The short-curve sum alone does not establish that theory for a new marked operator.

The source's last-long-ancestor definition includes the terminal generation. Its final displayed summation uses a shorter index range. Native 327 avoids relying on that abbreviated display: it proves the entire renewal directly with last-long times **1 through n, including n**, so the terminal-long contribution has exponent zero. No omitted generation is absorbed by assertion.

### Native verification of the application

Native 327 is a complete derivation from the specifically named physical curve, expansion and distortion statements of native 281–284. Its enlarged momentum/marked curve class has its **own** curvature allowance, homogeneous cutoff, short length and constants. It is not enough that a smaller generic unstable-curve class had already qualified for a growth lemma. The first true image of each source is constructed before renewal, and physical reversal transports the exact observations.

The proof retains the source length explicitly. With the actual adapted contraction `theta_r<1`, Euclidean endpoint comparison `Gamma`, distortion factor `D_ell=exp(D ell^(1/3))` and subdivision length `ell`, it proves

\[
 \sum_{V\in\mathcal G_n(C)}\sup_V J_V(T_R^{-n})
 \le \Gamma\theta_r^n+
 \frac{3\Gamma D_\ell}{\ell(1-\theta_r)}|C|.
\]

The factor `Gamma` is paid once along a complete Jacobian. At each last-long time the true original preimages are disjoint in the source curve, which pays their total length. The proof uses every physical homogeneous descendant and nonnegative exhaustion. It does not use a pointwise common-final-momentum kernel, pressure, conditional independence or a Markov replacement. Native 327 then combines this estimate with a source-interval clearance cover. Native 328 separately pays the complete physical roof change of variables and its boundary terms; neither step is supplied merely by the external lemma.

These are native proofs with explicit inherited geometric dependencies. Reading the external paper and checking finite scripts is not an independent specialist reconstruction of every physical premise of native 281–284; that status remains distinguished in the proof ledger.

## Baladi–Demers: pressure and uniformity are separate obligations

The retained inspection covers Lemma 3.6 and its cell argument, pages 16–20, and Proposition 3.14, pages 25–27. The pressure comparison uses its specified potential, parameter interval, long-curve condition, homogeneous partition and Cantor-rectangle crossing structure. A native `q=2` partition or uniformity over the entire radius family does not follow by renaming these objects or appealing to compactness without proof.

The predecessor's native 326 supplies a complete native author proof of physical-word pressure, using the retained boundary-stopping and source comparison chain. That result is inherited with its precise native hypotheses, rather than claimed as a new theorem of this revision. An independent specialist reconstruction has not been obtained; that evidence distinction does not convert the supplied author proof into an absent proof. New 327–329 do not invoke that pressure theorem: their clearance payment follows length-sensitive physical transport, selected roof coarea, a singular moment and a summable depth estimate. Consequently this external source cannot hide an unpaid clearance or capacity term.

## Dolgopyat–Nándori: tested limits and raw local inversion

The retained inspection covers Definition 2.2, pages 3–4, and the finite-horizon Sinai-billiard application in Section 6.4/Proposition 6.3, page 32. Its mixed local limit uses its stated subgroup/translation, covariance, coboundary and test-function hypotheses; the billiard application retains its arithmetic alternatives. Convergence against the designated continuous tests does not imply an exact-label roof essential supremum at a shrinking microscopic window.

The present original observable remains `(kappa_1,kappa_2,tau,1_Y*)`, with actual return count, actual collision count, lattice displacement and physical roof. Its finite spectral-peak arithmetic reference, possible zero classes and near-unit peaks remain. Native 330–332 provide their own BV, smoothing, physical-return and weak Fourier estimates. They neither import a full raw local limit from this citation nor claim that a first-order weak Fourier bound is integrable at high frequency. A complete uniform joint-frequency inversion and the original microscopic denominator remain separate requirements.

## Convex duality: actual qualification, native proof

The retained Stanford-slide inspection covers weak/strong duality and Slater qualification, pages 14–15, and KKT statements, pages 22–23. The qualification is substantive. Native 297 provides the special disk-product duality argument directly; the slides are background, not a certificate for an arbitrary formal billiard action domain. No new physical-orbit or spectral result is derived from the citation alone.

## Status of internal mathematical sources

Internal A2-DYN references are supplied through complete pinned article trees and the preserved original proof corpus. Their theorem bodies, corrections, failed examples and qualifications are retained. An internal citation does not turn an inherited claim into an independently verified external theorem. The current ledger distinguishes (i) new complete native arguments from explicitly named inputs, (ii) inherited proved formulas and reductions, (iii) finite algebraic/executable checks and (iv) dynamical/spectral hypotheses still requiring full reconstruction.

Every new use of ordinary calculus, countable positive exhaustion, BV integration by parts, recurrence, compact Fourier support or conditioning is proved in native 327–332 at its actual measure and parameter scope. None is used to replace the original limiting target. The unresolved endpoint source and same-roof capacity, full joint arithmetic/spectral inversion and microscopic normalization are visible in the manuscript and response; no external source listed here closes them automatically.
