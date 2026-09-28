# Written proof audit — spectral entropy

This is an author-side proof audit, not an independent certificate.

| Step | Invariant and edge cases |
|---|---|
| Smoothing | Round-sphere kernels have support in chordal h-caps and C1 boundary behavior. The Fisher integral is finite despite zeros. The regularized entropy path uses no pointwise lower bound on density. |
| Entropy transport | Centers, coupling and rotations are finite; antipodal paths can be chosen arbitrarily. The flux has the correct continuity equation and kinetic bound. Every mixture, not merely an endpoint, has the Fisher bound. |
| Spectral defect | The projection is onto all G-invariant functions. Nontransitive actions do not justify replacing it by global constants. The assumption is a full L2 action bound; a first-harmonic contraction is insufficient. |
| Thin support | Haar caps are required uniformly over all unit directions. The density is supported on k such caps, even when conditional directions are not on the prescribed physical orbit. |
| Flow transport | Weights are p_s times the norm of the conditional centroid. Zero centroids contribute no mass. The excess scalar mass is nonnegative and transported separately; normalization is bounded using alpha >= zeta. |
| Terminal residual | Only conditional mean correctness on deterministic words is averaged. A decoder for an individual hidden label need not approximate the target. Legal decoder norm at most one is essential. |
| Occupation | The external word law depends on advertised cut widths, not private state. One random physical letter spans each selected gap; deterministic identity-product fillers may perform arbitrary hidden processing. Cauchy–Schwarz is over selected gaps, not all N steps. |
| Endpoint | At zeta=1 the transport budget vanishes. The logarithmic entropy range then gives an exponential obstruction, not the positive-error polynomial upper construction. |
| LPS input | The exact six-rotation set is identified with the cited norm-five quaternion set. The identity letter is available for padding but is not included in its uniform spectral measure. Unitary lifts are algebraic; Bloch matrices are rational. |
| Exact profile | The first-axis stabilizer is cyclic, so coset-ball size is 5^t, not the free group ball size. The fixed suffix is injective and preserves the denominator-lattice separation. |
| Effectivity | The numerical lower constant comes from the imported explicit norm plus displayed elementary inequalities. Finite tests do not certify that norm. The old five-letter alphabet is not silently replaced in its theorem. |

The decisive budget is

```
gamma (J-1) <= log(D_m h^(-(m-1)))
              + pi sqrt(3 B_m)/h * sqrt((J-1)(1-zeta)/zeta).
```

Taking h proportional to k^(-1/p) gives J=O(k^(2/p)) at fixed zeta>0. Only the additive initial entropy is logarithmic. The proof does not assume total-variation mixing of the finitely supported physical word law, a logarithmic Sobolev inequality, positive state masses, or convergence of microscopic clocked rows.
