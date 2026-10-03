# Focused literature audit for the external A2 v25 rereview

## 1. Scope

This is a focused theorem/input comparison for the new v25 claims. It is not an exhaustive priority search. The review distinguishes:

- the manuscript's selected periodic endpoint-density experiment;
- classical conditional analytic continuation;
- boundary/lens rigidity;
- exterior obstacle travelling-time rigidity;
- standard numerical differentiation, interval certification and sequential error spending.

No citation or finite computation is used as a substitute for checking the manuscript's proof.

## 2. Analytic continuation

### Lloyd N. Trefethen

*Quantifying the ill-conditioning of analytic continuation*, BIT Numerical Mathematics 60 (2020), 901–915; arXiv:1908.11097.

The official abstract emphasizes that a priori boundedness in a complex region makes analytic continuation conditionally possible but can leave it extremely ill-conditioned, particularly along strips and channels. This is the closest methodological comparison for the v25 interval-to-strip estimate.

The manuscript's Lemma 3.1 is self-contained: it uses equispaced interpolation, a Cauchy remainder and a chain of three-circles inequalities. It does not claim a new optimal continuation principle. Its doubly extreme threshold is consistent with the severe conditioning discussed by Trefethen.

Primary record: `https://arxiv.org/abs/1908.11097`.

## 3. Boundary and lens rigidity

### Plamen Stefanov, Gunther Uhlmann and András Vasy

*Local and global boundary rigidity and the geodesic X-ray transform in the normal gauge*, Annals of Mathematics 194 (2021), 1–95; arXiv:1702.03638.

The primary abstract states local recovery of a Riemannian metric from boundary distance near a strictly convex point, modulo diffeomorphism, and global/semi-global lens-rigidity consequences under convexity hypotheses.

This is a different unknown and observation model from a periodic Euclidean obstacle table with selected local records, absolute Liouville normalization and active local chart access. The comparison is nevertheless relevant because the retained endpoint law first reconstructs a local action/travel-time function and then differentiates it to recover geometry.

Primary record: `https://arxiv.org/abs/1702.03638`.

## 4. Exterior obstacle travelling-time rigidity

### Lyle Noakes and Luchezar Stoyanov

*Travelling times in scattering by obstacles*, arXiv:1404.4147; J. Math. Anal. Appl. 430 (2015), 703–717.

The official abstract gives time-preserving conjugacy of non-trapping exterior flows under generic hypotheses and describes constructive recovery for a union of two strictly convex planar components.

Primary record: `https://arxiv.org/abs/1404.4147`.

### Lyle Noakes and Luchezar Stoyanov

*Rigidity of Scattering Lengths and Traveling Times for Disjoint Unions of Convex Bodies*, arXiv:1402.6445; Proc. Amer. Math. Soc. 143 (2015), 3879–3893.

The official abstract states uniqueness of finite disjoint unions of strictly convex `C^3` bodies from almost-equal scattering length spectra or travelling times. The later planar paper below supplies a separate proof for the two-dimensional gap in the earlier argument.

Primary record: `https://arxiv.org/abs/1402.6445`.

### Lyle Noakes and Luchezar Stoyanov

*Lens Rigidity in Scattering by Unions of Strictly Convex Bodies in R^2*, SIAM J. Math. Anal. 52 (2020), 471–480; arXiv:1803.02542; DOI 10.1137/19M1270409.

The publisher and arXiv abstracts state that a finite disjoint union of strictly convex planar bodies is determined by exterior travelling times or scattering length data, supplying the separate planar proof not properly covered in the earlier higher-dimensional article.

Primary records:

- `https://arxiv.org/abs/1803.02542`;
- `https://doi.org/10.1137/19M1270409`.

### Tal Gurfinkel, Lyle Noakes and Luchezar Stoyanov

*Travelling Times in Scattering by Obstacles in Curved Space*, J. Differential Equations 269 (2020), 9508–9530; arXiv:2003.12261.

The paper treats obstacles in a two-dimensional Riemannian manifold, proves time-preserving flow conjugacy on non-trapping parts from almost-equal travelling times, and proves convex-obstacle uniqueness under non-positive curvature.

Primary record: `https://arxiv.org/abs/2003.12261`.

## 5. Current developments missing from the manuscript's comparison

### Tal Gurfinkel, Lyle Noakes and Luchezar Stoyanov

*Uniqueness of Obstacles in Riemannian Manifolds from Travelling Times*, arXiv:2309.11141 (2023).

The official abstract states uniqueness for disjoint unions of strictly convex obstacles under curvature assumptions and an additional restriction on how many components a geodesic intersects.

Primary record: `https://arxiv.org/abs/2309.11141`.

### Tal Gurfinkel, Lyle Noakes and Luchezar Stoyanov

*Rigidity of Travelling Times for Strictly Convex Obstacles in Riemannian Manifolds*, arXiv:2311.07813 (2023).

The official abstract removes a prior tangency-equivalence condition and proves travelling-time rigidity in dimensions at least three. The source was still identified as a preprint in the current records checked for this review.

Primary record: `https://arxiv.org/abs/2311.07813`.

These two papers do not subsume v25: they use global exterior travelling-time data, not selected periodic endpoint-density records with active local values, absolute cell normalization and a completion defect. They should nevertheless be included in a 2026 theorem-level comparison because they are current work in the nearest obstacle travel-time information category.

## 6. Relation to the v25 novelty claim

The current literature supports the following restrained novelty account.

1. Recovering geometry from rich boundary/lens/travelling-time data is an established inverse-geometry paradigm.
2. Conditional analytic continuation with severe prior-dependent instability is classical.
3. Finite differences, interval contraction, quadrature, rational subgroup reduction, coupon bounds and summable error spending are standard mechanisms.
4. The v25-specific contribution is the explicit **within-one-table** bridge-recognition calibration, its conversion to a value-only fingerprint, its coupling to the local periodic-record construction, and the subsequent absolute-area completion certificate.

That contribution is mathematically nontrivial. It remains strongly conditional on numerical analytic, shape, symmetry, separation and sensor priors. The literature comparison does not by itself decide venue significance, but it reinforces the referee report's conclusion that the conceptual advance lies in a specialized certification architecture rather than a new general obstacle-rigidity principle.

## 7. Limits of this audit

The abstracts, publisher records and the manuscript's stated theorem distinctions were checked. This audit does not claim a complete reading of every cited proof or an exhaustive search of all inverse scattering, billiard rigidity, computable analysis or sampling literature.