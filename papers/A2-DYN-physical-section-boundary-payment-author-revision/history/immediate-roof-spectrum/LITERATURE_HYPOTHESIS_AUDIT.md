# Fresh primary-source hypothesis audit

This current audit replaces the predecessor-facing summary. The exact preceding audit remains at `history/section-multipliers-baseline/LITERATURE_HYPOTHESIS_AUDIT.md`; `audit/FRESH_LITERATURE_AUDIT.md` preserves the fresh research note. Native 333–335 are inherited results, while the new native 336 geometric side lemma is the additional application discussed in the Coste addendum.

Author-revision audit, 23 October 2026. The four cited primary sources were opened and read directly, then downloaded afresh at 06:56:56 UTC. Their fresh byte counts and SHA-256 identities are in `audit/FRESH_PRIMARY_SOURCE_IDENTITIES.json`; all four hashes agree with the inherited source-download manifest. Exact primary PDFs are scratch verification material, not repository redistribution. PDF page numbers below are one-based in the inspected versions, not journal pagination.

## 1. Demers--Zhang: section multipliers and reference measure

M. F. Demers and H.-K. Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, Communications in Mathematical Physics 324 (2013), 767--830. The author publication list confirms the bibliographic data:
https://faculty.fairfield.edu/mdemers/research/pub.html

Inspected version: dated 10 October 2013, 53 pages, 662,784 bytes. Primary PDF:
https://faculty.fairfield.edu/mdemers/research/2013.10.10.perturbation16.pdf

**Actual hypotheses and scope.** Section 3.3 (pp. 12--13) defines anisotropic norms using stable-curve tests and matched-curve comparisons; the exponents satisfy (0<q<p\le 1/3) and (0<\beta\le\min\{\alpha,p-q\}). Lemmas 5.2--5.3 (p. 32) require a modulo-zero partition into simply connected open cells with uniformly bounded smooth boundary pieces transverse to the stable cone at a uniform positive angle. Lemma 5.3 additionally needs uniformly bounded cells per homogeneity strip and uniformly piecewise (C^\gamma) multipliers, (\gamma=\max\{p,2\beta+\epsilon\}). The regular-function embedding is relative to the collision invariant measure, not bare coordinate area (pp. 17--19). Perturbation conclusions additionally depend on the stated map-class hypotheses.

**A2-DYN applicability.** Native 333 supplies the actual original-section partition and multiplier estimates, including its parameter dependence. That verification must be retained. A moving or long-word selector is not automatically covered solely because it is an indicator. A scalar invariant integral must use the manuscript's physical collision density once; changing the reference measure and then multiplying by the density again would alter the law. No application here supplies the still-open complete normalized local derivative charge.

## 2. Baladi--Demers: the finite-horizon definition and pressure interval

V. Baladi and M. F. Demers, *Thermodynamic formalism for dispersing billiards*, Journal of Modern Dynamics 18 (2022), 415--493, DOI 10.3934/jmd.2022013. Official bibliographic record:
https://www.aimsciences.org/article/doi/10.3934/jmd.2022013

Inspected version: dated 19 September 2022, 62 pages, 907,905 bytes. Primary PDF:
https://faculty.fairfield.edu/mdemers/research/2022.09.19.thermo.postultimate.proofed.pdf

**Actual hypotheses and scope.** Section 1.1 (p. 2) uses finitely many disjoint closed (C^3) positively curved scatterers on a flat two-torus and unit-speed specular dynamics. Its finite-horizon convention excludes trajectories consisting entirely of tangential collisions; the text distinguishes this from merely bounded free-flight times. Theorem 1.1 (pp. 3--4) concerns the geometric potential (-t\log J^uT) for (0<t<t_*), with (t_*=sup\{t>0:\Lambda^{-t}<e^{P(t)}\}>1). Sparse recurrence is an additional hypothesis for the endpoint limit at (t=0). The spectral result (Theorem 4.1, pp. 31--32) uses the article's own anisotropic spaces and potential.

**A2-DYN inherited hypothesis closure.** The stronger no-all-tangential requirement is already implied by the retained native 282 proof. An irrational-direction half-line is dense modulo the triangular lattice and intersects an open radius-(R_-) disk. A rational line is parallel to a primitive lattice vector (z); neighboring lattice rows have spacing ((\sqrt3/2)/|z|\le\sqrt3/2). Every parallel line is therefore within (\sqrt3/4<9/20=R_-) of a row and intersects an open disk on that row. The same argument applies in the positive direction. Tangential reflection leaves velocity unchanged, so an all-tangential trajectory would be exactly a straight half-line avoiding all disk interiors, a contradiction. This is verification of an inherited physical hypothesis, not a newly discovered theorem.

This check does not establish uniform spectral estimates for arbitrary joint collision/section/displacement twists or interchange the original ordered limits. Native 326 and the fixed-band chain retain their precisely stated roles; the external citation alone adds no unproved uniformity in radius, frequency band or singular source selector.

## 3. Dolgopyat--Nándori: tests, arithmetic and flow normalization

D. Dolgopyat and P. Nándori, *On mixing and the local central limit theorem for hyperbolic flows*, Ergodic Theory and Dynamical Systems 40 (2020), 142--174, DOI 10.1017/etds.2018.29. Official record:
https://www.cambridge.org/core/journals/ergodic-theory-and-dynamical-systems/article/abs/on-mixing-and-the-local-central-limit-theorem-for-hyperbolic-flows/709E3FB8D66D25C4B699C4C0F727D475

Inspected version: author-hosted `llt_flow13.pdf`, 35 pages, 467,506 bytes, server Last-Modified 24 October 2017. No identity with a differently dated journal or arXiv PDF is presumed. Primary PDF:
https://www.math.umd.edu/~dolgop/llt_flow13.pdf

**Actual hypotheses and scope.** Definition 2.2 and Remark 2.5 (pp. 3--4) concern square-integrable observables after a bounded almost-everywhere-continuous coboundary, with positive covariance, fixed endpoint tests, fixed compactly supported observation tests and a specified translated closed subgroup. Uniformity holds for fixed center-error bound and compact scaled centers. Boundary-null fixed sets are allowed; a nonminimal coboundary may yield an endpoint-dependent, nonproduct limit. The suspension measure is (\nu\otimes\mathrm{Leb}/\nu(\tau)) (p. 2). Theorem 3.7 retains hypotheses H1--H7 and arithmetic alternatives. Proposition 6.3 (p. 32) treats finite-horizon Sinai billiards and piecewise Hölder flow observables, requiring the integrated-observable/roof pair to be minimal and its linearized group to fall in cases A, B or C; its displayed nonarithmetic formula has an additional nonarithmetic assumption.

**A2-DYN applicability.** These tested-observable results cannot alone justify four-coordinate raw pointwise inversion, shrinking microscopic windows, exact lattice labels or a replacement conditional denominator. The original collision/flow normalization and exact arithmetic zero classes remain part of the native proof obligations. Native 334's conditional bridge uses the inherited fixed-band scalar comparison; a separate growing-band strong spectral theorem is not an additional mandatory premise of that bridge. The complete normalized local derivative charge used by the bridge remains unproved in the preceding source.

## 4. Boyd--Vandenberghe: convex duality background

S. Boyd and L. Vandenberghe, *Convex Optimization: Duality*, official Stanford EE364a notes; the inspected front matter credits revised slides to Boyd, Vandenberghe and Parth Nobel. Primary PDF:
https://web.stanford.edu/class/ee364a/lectures/duality.pdf

Inspected version: 40 pages, 266,066 bytes, PDF creation metadata July 2023, server Last-Modified September 2025. The downloaded hash fixes the version without inferring a mathematical revision date from the server header.

**Actual hypotheses and scope.** Slides 5.12--5.13 (PDF pp. 14--15) distinguish universal weak duality from strong duality, which requires a qualification such as strict feasibility for a convex problem. Slater's condition also gives dual attainment when the primal optimum is finite. Relative-interior refinements are stated explicitly. The convex KKT criterion is on slide 5.21.

**A2-DYN applicability.** Native 297 proves the needed disk-word duality directly on a compact product of the original closed disks. The positive separation between consecutive disk centers keeps the summed edge-length objective differentiable on a neighborhood; compact minimization, convexity and the first-order support condition give the asserted dual certificate. No unsupported minimax exchange is imported. A relaxed minimizer is not called a physical collision trajectory, and no relaxed edge replaces the actual physical roof. The citation is background, not an independent theorem establishing capacity abundance or raw local inversion.

## What this fresh audit establishes

The bibliographic references and inspected versions are real and recoverable; the fresh hashes match prior download identities. The finite-horizon tangency condition is already closed by preserved original geometry. The remaining external-to-native inference boundaries are explicit: anisotropic admissibility of the actual selectors, the true invariant measure, exact arithmetic classes, fixed versus shrinking tests, all collision words, supremum uniformity, normalization and ordered limits must continue to be established by the relevant native proof bodies. This audit provides neither a journal acceptance claim nor a proof of the final raw pointwise local limit theorem.

## Addendum: Coste, newly used for the geometric side lemma

M. Coste, *An Introduction to O-minimal Geometry*, author-hosted notes dated November 1999; the author's publication page identifies the Pisa 2000 printed volume. Primary URL:
https://perso.univ-rennes1.fr/michel.coste/polyens/OMIN.pdf

The primary PDF's indexed theorem text was independently read: Theorem 2.9 (p. 19) gives a common finite bound for finite fibers of one definable set; Theorem 2.10 gives a finite cylindrical definable decomposition adapted to finitely many definable sets. Theorems 6.6--6.7 (p. 71) supply its (C^k) adapted version and a finite (C^k) partition for a definable function. These assertions apply to semialgebraic sets. They do not assert a count-uniform complexity bound for a sequence of different formulas.

The new geometric lemma uses the original finite physical graph from native 164. It takes every closure and boundary with the radius held fixed, and only then forms the parameterized semialgebraic family. This prevents ambient parameter closure from creating false sources at an exceptional radius. Smooth arbitrary observations are inserted after the geometric decomposition and need not be definable.

Retrieval scope differs from the four PDFs above: direct web retrieval timed out, and a separate byte-download attempt returned HTTP 503 (`audit/COSTE_PRIMARY_RETRIEVAL.json`). This is primary indexed theorem-text verification, not a new full-PDF download or hash verification. No inaccessible-PDF claim is treated as a mathematical hypothesis check beyond the actual retrieved theorem statements.
