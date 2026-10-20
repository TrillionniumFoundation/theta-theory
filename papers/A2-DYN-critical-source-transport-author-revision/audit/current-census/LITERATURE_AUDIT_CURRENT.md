# Fresh primary-source applicability audit

The three cited author PDFs were fetched on 20 October 2026 (UTC), hashed and read at the theorem statements, definitions and indicated proof steps. Selected theorem pages were also rasterized and visually checked. `PRIMARY_SOURCE_READBACK.json` records the actual download identities; `THEOREM_LOCATORS.json` gives PDF-page locators. Original bibliography and prior audits remain unchanged in the historical source.

## Demers–Zhang

Primary source: [A functional analytic approach to perturbations of the Lorentz gas](https://arxiv.org/pdf/1210.1261), 45 pages; arXiv v1 header 3 October 2012, internal date 12 March 2018. SHA256: `f20938fe161c0b4acd775bcd26ed2df1e1dba6901b8d04438359648b528f5e7f`.

Theorems 2.2–2.3 (PDF pp. 3–4) require one class with uniform H1–H5: hyperbolicity/singularities, invariant curve families, one-step expansion, distortion and Jacobian control. Section 3.3 (pp. 10–11) uses closures of C1 in stable-test weak and strong stable/unstable norms, with `0<p≤1/3`, `q<p`, `α<1−ς0`, `β≤min(α,p−q)`. The operator perturbation norm maps the strong unit ball into the weak norm. Corollary 2.4 requires a spectral gap and the stated Hölder regularity. Remark 2.7(b), p. 5, handles sufficiently small arclength reparametrizations. Lemma 3.2(b), p. 12, bounds the sum of stable Jacobians on its specified fragmented inverse curves uniformly in curve, map and time.

**Native applicability:** the A2-DYN cross-curve result supplies its own displayed estimate; extending it to every marked transfer operator requires all those hypotheses and the original source/measure factors. The cited theorem alone does not supply the raw roof essential height.

## Baladi–Demers

Primary source: [Thermodynamic formalism for dispersing billiards](https://arxiv.org/pdf/2009.10936), 62 pages. SHA256: `3b8efc436aa4e276821252d2c1b23297d486928c3ebb0f44c6e2d56296f3d2e3`.

For a fixed finite-horizon Sinai map, Theorem 1.1 (p. 4) treats `−t log JuT` for `0<t<t*`, with pressure gap `Λ^(−t)<exp P(t)`. Spaces `B(t0,t1)` and their bounds depend on a compact subinterval; the displayed gap deteriorates at the range endpoints. Partition (2.4) and Lemma 2.2 (pp. 7–8) compare curves in the same specified homogeneous cell. Homogeneity-strip boundaries are allowed; real singularity lines are excluded.

Lemma 3.6 (pp. 16–18) controls a fixed positive fraction of the complete pressure sum on cells with sufficiently large unstable width, uniformly in `n` and `t∈[t0,1]`. The perturbation is C1 and satisfies (3.6): `2||g||∞<−t0 log θ` and `||∇g||∞≤(C*δ0)^(−1)`.

**Native applicability:** arbitrary conditioned positive-source indicators and singular physical multipliers are not covered by those potential hypotheses. Applying the abundance conclusion to the exact microscopic comparison pool still requires a source-level comparison and its normalization.

## Dolgopyat–Nándori

Primary source: [On mixing and the local central limit theorem for hyperbolic flows](https://arxiv.org/pdf/1710.08568), 35 pages. SHA256: `b2f683268e2406d7933812b26d3d33429d09cfd5ab92ad135db3377030bf2d60`.

Definition 2.2 (pp. 3–4) assumes square-integrable vector observations and a decomposition `f=g−h+h∘T` with bounded, almost-everywhere-continuous `h`. Its subgroup/translate, positive covariance and admissible centering sequences are explicit. The limit tests bounded continuous endpoint functions and compactly supported continuous record functions; its uniformity keeps the centering tolerance fixed and the scaled center in a compact set. Remark 2.5 permits indicators only with the stated zero-boundary-mass conditions.

Section 6.4 and Proposition 6.3 (p. 32) use the genuine finite-horizon unit-speed Sinai flow, collision section and piecewise Hölder flow observation. Minimality and linearized-group cases A–C are hypotheses; the simpler product limit additionally assumes non-arithmeticity.

**Native applicability:** the precise collision occupation/displacement labels, roof-window source heights and four-coordinate inverse target require their own verified arithmetic and uniform conditional interfaces. An integrated test-function local limit cannot be substituted for the unresolved raw pointwise statement.

## Use in this continuation

The new native proofs must be supported by their displayed geometric or analytic arguments. These citations keep the interfaces above and do not certify an unproved positive-source shortage, unrestricted marked pressure, exact arithmetic factor or inverse theorem. The three PDFs are external reading evidence; the revision records links and hashes rather than republishes the papers. This audit is author-side applicability checking, with no claim of independent human specialist certification.
