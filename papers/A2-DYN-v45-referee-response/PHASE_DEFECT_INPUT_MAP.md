# Inputs and norm boundaries for the quantitative phase theorem

The collision probability is the common flat probability in (alpha,p). All new BV norms use these initial coordinates. The norm of a complex function is the sum of the real/imaginary BV norms. Defects are L1 for unit-circle phases and L2 for normalized complex functions. The induced return map and raw pushforward densities are not the operators or functions appearing in these new norms.

## Inherited dynamical inputs

Young, *Statistical properties of dynamical systems with some hyperbolicity*, Annals of Mathematics 147 (1998), Sections 1 (P3)–(P5) and 8.1–8.3. Author source: https://math.nyu.edu/~lsy/papers/towers-billiards.pdf. The retained v14 `GEOMETRIC_INPUT_MAP.md` specifies transverse cones, homogeneous regular arcs, adapted contraction and the actual-length conversion, positive-area product sets, holonomy absolute continuity, and ergodicity of finite-horizon physical torus covers.

The new proof uses exponential arc contraction on each fixed product set, but does not assume that its constants are uniform in R. It uses equivalence to a product measure, but not bounded density: if m=rho mu, then the stable-pair density is rho(u,s0)rho(u,s1)/rho_u(u), and the unstable density is rho(u0,s)rho(u1,s)/rho_s(s). Reference triple averages are compared by truncating their Radon–Nikodym derivatives. The finite tail choices enter the constants.

The finite covers modulo p times the lattice have the identical planar lift, p^2 physical scatterers and unchanged horizon. A rectangular Euclidean cover has 2p^2 scatterers. These are applications of the same finite-horizon billiard class, not a spectral assertion about an arbitrary skew product.

## Analytic inputs

Mean-preserving reflection/convolution and the first derivative smoothing bound follow from the existing smoothing construction. The exponentially summable collision covariance estimate is used for the modulus of a complex vector, after scaling by its actual supremum/BV norm.

L. Ambrosio, N. Fusco and D. Pallara, *Functions of Bounded Variation and Free Discontinuity Problems*, Oxford Mathematical Monographs, Clarendon Press, 2000, Chapter 3. Publisher record: https://academic.oup.com/book/53762/chapter-abstract/422178115. The chain, product and coarea rules give a level between 1/4 and 1/2 with finite perimeter and a controlled-BV circle truncation. No second derivative or many-return density result is imported.

## Unproved interfaces

The new normalized complex-vector theorem starts with an actual bounded-BV function. A distribution-space vector is not automatically one. Neither preservation of a BV ball by the twisted operator nor an anisotropic-to-BV map is asserted. Constants for a fixed compact nonzero band are not estimates in a shrinking central annulus or an unbounded roof band. Radius-uniform compactness with fixed H does not imply a radius-uniform logarithmic dependence on growing H.
