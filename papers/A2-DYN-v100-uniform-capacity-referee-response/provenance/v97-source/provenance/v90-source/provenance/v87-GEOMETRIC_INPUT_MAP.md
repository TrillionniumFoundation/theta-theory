# Qualitative geometry used in revision 14

## Primary source

L.-S. Young, *Statistical properties of dynamical systems with some hyperbolicity*, Annals of Mathematics (2) 147 (1998), 585--650. The author PDF is `https://math.nyu.edu/~lsy/papers/towers-billiards.pdf`. Section labels, rather than publication/preprint page offsets, identify the input.

| Required property | Source location | Use in the new proof |
|---|---|---|
| Transverse stable and unstable graph cones | Section 8.2B | Simple local four-corner quadrilaterals |
| Adapted contraction and ordinary arc-length control | Section 8.2C, Facts 1(b), 2(a); end of Section 8.3 | Vanishing action integrals on forward stable and backward unstable images |
| Homogeneous local curves and regular iterates | Sections 8.2D and 8.3, Sublemma 1 | Fixed physical branch labels on the appropriate arcs |
| Positive-area hyperbolic product set | Section 8.3, paragraph before verification of (P3)--(P5) | Restricted invariant measure has a bounded ambient density |
| Absolute continuity with positive holonomy Jacobian | Section 1, (P5)(b), verified in Section 8.3; reverse-time statement for the inverse map | Product measure-class equivalence and four-corner Fubini |
| Ergodicity of finite-horizon dispersing collision maps on a torus | Section 8.1, discussion preceding Theorem 6 and Theorem 6 | The actual four-scatterer finite-cover obstruction |

The physical hypotheses are checked in the article: disjoint circular scatterers, smooth strictly positive curvature, connected free domain and finite horizon. The rectangular covers are Euclidean covers of the table, not affine deformations of specular reflection. Restricting the initial product chart away from grazing makes the invariant measure equivalent to coordinate area. Only the forward map `p=sin(phi)` is used for length control near grazing; its inverse is not used there.

## Derived here, not quoted from the source

The conditional-pair estimate has both marginals equal to the normalized restriction of collision measure. Its `L1` approximation error is controlled by `2/nu(P)` at every iterate. This is what permits measurable phases, without a uniform modulus or a periodic representative. The forward and backward action formulas, their identical holonomy signs, four-corner cancellation, arbitrarily small nonzero symplectic area, rotation products and the invariant finite-cover function are derived in Sections 25--26.

The local product constants are allowed to depend on the fixed radius. Parameter uniformity of the final lower eigenvalue follows instead from pointwise exclusion of every kernel direction and the previously proved continuous covariance on a compact interval. Neither a uniform measurable Livsic theorem nor approximate-vector regularity is imported.

## Boundary

These qualitative inputs do not give a quantitative induced resolvent, a complete complementary Fourier integral, a many-return coarea derivative bound or an exact-event replacement estimate. The raw-density requirements therefore retain their separate hypotheses.
