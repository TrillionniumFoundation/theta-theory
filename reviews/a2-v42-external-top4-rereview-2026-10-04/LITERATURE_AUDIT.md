# Focused literature audit for the external A2 v42 rereview

This audit compares the theorem package with the closest primary mathematical mechanisms and observation models. It is not an exhaustive priority search and does not certify novelty against every publication.

## 1. The object being compared

The principal A2 datum is the ordered pair of whole-plane fields produced by two fixed opposite forward commands `a` and `-a`, of one fixed positive length, under one unknown stationary compact probability. The output of each attempt is one first-collision bit; starts, impacts, times, and the launch displacement are hidden. The exact theorem allows atomic and lower-dimensional laws and nonsmooth strictly convex obstacles, subject to `t+diam(A)<d`.

The proof first recovers occupation by a finite endpoint prefix. It then uses matched occupation and collision supports to obtain

\[
2h_P-h_{K_+}-h_{K_-}+t|u\cdot e|=h_C-h_L.
\]

The negative atoms of the signed support measure identify the contact chord, support subtraction identifies the footprint, and an isolated occupation convolution identifies the full probability law. The complete ambiguity is common translation.

## 2. Covariograms and two-factor geometric inversion

Averkov and Bianchi prove that the planar covariogram of one convex body determines it up to translation and reflection. Bianchi's cross-covariogram results determine substantial classes of pairs, with common translation and reflected interchange as natural associates and explicit exceptional polygonal families. Bianchi's Fourier--Laplace analysis gives corresponding uniqueness for smooth positively curved planar bodies. Bianchi, Gardner, and Kiderlen also provide noisy-grid reconstruction and consistency results for covariogram observations.

These are direct precedents for two-factor geometric inversion. In the uniform full-dimensional launch submodel, one isolated occupation component is a normalized cross covariogram. The A2 input is nevertheless different: the covariogram is not directly supplied. The two ordered collision fields first produce the occupation and two additional support components. Their signed support identity removes the reflected-interchange ambiguity in the stated strictly convex collision class and permits a general compact probability rather than only a uniform convex-body factor.

Primary sources inspected or pinned in the author audit include:

- G. Averkov and G. Bianchi, *Confirmation of Matheron's conjecture on the covariogram of a planar convex body*, JEMS 11 (2009), Theorem 1.1;
- G. Bianchi, *The cross covariogram of a pair of polygons determines both polygons, with a few exceptions*, Adv. Appl. Math. 42 (2009), Theorem 1.1;
- G. Bianchi, *The covariogram and Fourier--Laplace transform in C^n*, Proc. Lond. Math. Soc. 113 (2016), Theorem 6.3;
- G. Bianchi, R. J. Gardner, and M. Kiderlen, *Phase retrieval for characteristic functions of convex bodies and reconstruction from covariograms*, JAMS 24 (2011), Theorems 4.10 and 6.4.

## 3. Blind probe reconstruction

Villarrubia's scanned-probe reconstruction represents image formation through morphological dilation and constructs the largest probe consistent with supplied dilation constraints. This is a close unknown-Minkowski-summand precedent. It explains why support envelopes and contact information are natural tools.

The A2 theorem has stronger identifying information in its collision fields. Three matched supports determine an obstacle-minus-chord support; the chord atoms separate from the strictly convex obstacle measure; and the occupation values determine the probability carried by the recovered footprint. The proof is not merely an application of blind-tip morphology.

## 4. Unknown-noise deconvolution

Gassiat, Le Corff, and Lehéricy prove multivariate unknown-noise identifiability up to opposite translations under independence of specified noise-coordinate blocks and an entire-transform nondegeneracy condition. Capitao-Miniconi, Gassiat, and Lehéricy give support criteria and quantitative compact-signal inference in related product-noise models.

There is a genuine overlapping submodel. After occupation recovery, the normalized component occupation is the law of `U_C-Z`, with `U_C` uniform on the obstacle and independent of `Z`. When the launch law has the required product structure, the cited unknown-noise results are relevant. The A2 theorem does not assume coordinate-product structure. Instead, the collision-support identity separates the geometric factor first, after which the compact probability is recovered from a known-factor convolution.

The literature comparison should therefore avoid any claim that unknown-noise joint identification or singular-law inference first appears here. The collision-specific advance is the derivation of the factor separation from two fixed first-collision fields for a general planar compact probability.

## 5. Signed support measures

Martinez-Maure's theory of Minkowski differences associates signed length measures with differences of support functions and determines the generalized support difference up to translation from the corresponding zero-first-moment measure. This is the correct classical framework for `h_C-h_L`.

A signed support difference alone does not generally identify its ordered convex summands. In A2, strict convexity makes the obstacle surface-area measure nonatomic, while the segment contributes exactly two atoms. Their mutual singularity makes the Jordan decomposition identify the chord and obstacle under the theorem's hypotheses. The v41 proof explicitly establishes the atom/exposed-face convention rather than assuming smooth curvature density.

## 6. Compact-transform uniqueness and zero-aware deconvolution

Compact-support deconvolution through local or zero-avoiding Fourier information has an established literature, including Meister and Delaigle--Meister in one-dimensional settings. In the exact A2 theorem, once the compact obstacle indicator is known, its Fourier transform is entire and nonzero at the origin. Its real nonzero set is dense; quotient recovery there and continuity identify the launch characteristic function everywhere.

This is an exact uniqueness argument. It is not a quantitative stability theorem through the factor's zero set. The finite A2 theory correctly uses moments and positive finite fitting instead.

## 7. Moment-to-transport reconstruction

Quantitative control of transportation distance by finitely many moments is classical; the author cites Rigollet and Weed for a univariate form and supplies the bivariate tensor approximation and triangular factor estimates needed here.

Version 42 adds a collision-specific acquisition result. It does not assume samples from `U_C-Z`. A protected first-exit prefix converts two fresh fixed-command collision bits into a bounded signed record with expectation equal to component occupation at the selected nominal point. Shared records estimate all required moments. The concentration and polynomial approximation ingredients are classical, but the reduction from the physical two-bit records is new to the current proof chain.

## 8. Assessment of comparative significance

The closest prior work shows that factor identification, blind morphology, signed support measures, compact-transform uniqueness, and moment transportation are well-developed subjects. The A2 theorem should not claim novelty for these tools.

The combined collision-specific contribution is nevertheless substantial:

1. only two opposite fixed commands of one positive length are used;
2. occupation is recovered by a finite physical endpoint prefix;
3. three observable supports cancel the unknown footprint;
4. strict convexity separates the chord and obstacle by Jordan decomposition without smoothness;
5. the entire compact probability, complete translation fiber, period group, and all forward responses follow;
6. a finite bit experiment reconstructs geometry and, at explicit sufficient cost, the law and response family.

I did not identify in the inspected sources a theorem containing this complete ordered two-field collision chain. This observation is not a universal priority claim. It supports the view that the exact theorem has significance beyond a routine assembly of existing inversions.