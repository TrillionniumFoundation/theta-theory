# Literature audit for the external A2 v19 rereview

## Scope

This audit addresses the information category and nearest mechanisms introduced by the v18/v19 local theorem. It is not an exhaustive novelty or priority search, and it does not independently referee the cited papers.

The central v19 datum is a pair of endpoint-arclength density functions on one strictly active selected return branch. Proposition 2.2 of the manuscript proves that these data are equivalent to a local generating/travel-time action `W` and the normalization `A`; the positive twist converts `W` into a local canonical scattering graph. Consequently the nearest comparison class is boundary-distance, lens/scattering, and obstacle travelling-time rigidity, not only marked-length spectral rigidity for dispersing billiards.

The manuscript now makes this equivalence explicit and does not claim that the affine two-time elimination, endpoint differentiation, or passage from a generating function to a canonical relation is a new general inverse-geometric principle.

## Primary sources and theorem-level comparison

### 1. Stefanov–Uhlmann–Vasy

P. Stefanov, G. Uhlmann, and A. Vasy,  
*Local and global boundary rigidity and the geodesic X-ray transform in the normal gauge*,  
*Annals of Mathematics* 194 (2021), 1–95; arXiv:1702.03638.

Primary access:

- https://annals.math.princeton.edu/2021/194-1/p01
- https://arxiv.org/abs/1702.03638

Locations used:

- Theorem 1.1;
- Theorem 1.3;
- introductory distinction between local boundary-distance recovery and global lens rigidity under convex foliation.

Relation to A2 v19:

- SUV recover a Riemannian metric near a strictly convex boundary point from boundary-distance data, modulo the natural boundary-fixing gauge, in the dimensions and regularity stated there.
- Their global result uses lens data and a convex-foliation hypothesis.
- In A2 the ambient Euclidean metric is known, but two reflecting curves are unknown.
- The measured coordinates are intrinsic arclengths on an unknown source obstacle.
- The diagonal action is twice a positive nearest-point distance, not the zero diagonal of a standard boundary-distance function.
- The intermediate specular reflection enters through a stationary Schur complement.

The cited SUV theorems do not directly yield A2's two-reflector curvature formulas. Conversely, A2's selected planar return data do not imply the general metric-rigidity results of SUV.

### 2. Gurfinkel–Noakes–Stoyanov

T. Gurfinkel, L. Noakes, and L. Stoyanov,  
*Travelling Times in Scattering by Obstacles in Curved Space*,  
*Journal of Differential Equations* 269 (2020), 9508–9530; arXiv:2003.12261.

Primary access:

- https://arxiv.org/abs/2003.12261
- https://doi.org/10.1016/j.jde.2020.05.049

Locations used:

- Theorem 1;
- Theorem 2;
- Lemma 7.

Relation to A2 v19:

- GNS use travelling times measured between points on a known enclosing observation boundary.
- Their results relate travelling-time data to scattering-flow conjugacy and, in the stated two-dimensional nonpositively curved setting, to obstacle determination.
- Lemma 7 explicitly connects endpoint differentiation of travelling time to incident and outgoing directions.

A2 uses a selected source–opposite–source return whose endpoint coordinates lie on an unknown reflecting obstacle. It reconstructs both local reflecting arcs and later descends an unlabelled finite collection to a periodic table. The information geometry differs, but endpoint travel time and scattering direction are a close mechanism and must be credited.

### 3. Noakes–Stoyanov

L. Noakes and L. Stoyanov,  
*Travelling Times in Scattering by Obstacles*,  
*Journal of Mathematical Analysis and Applications* 430 (2015), 703–717; arXiv:1404.4147.

Primary access:

- https://arxiv.org/abs/1404.4147
- https://doi.org/10.1016/j.jmaa.2015.05.013

Locations used:

- Theorem 1;
- Lemma 4;
- Sections 3–4.

Relation to A2 v19:

- NS connect travelling-time data and the scattering relation.
- They also give a constructive reconstruction in a planar two-convex-obstacle setting.

This is arguably the nearest conceptual comparison to A2's local theorem. It does not obviously contain the selected three-impact action quotient or the intrinsic diagonal Schur formulas, and its external observation boundary differs from A2's unknown reflecting boundary. Nevertheless, a top-level novelty discussion must explain the distinction at theorem level rather than relying only on marked-length comparisons.

### 4. Stoyanov and Santaló-type volume recovery

L. Stoyanov,  
*Santaló's formula and stability of trapping sets of positive measure*,  
*Journal of Differential Equations* 263 (2017), 2991–3008; arXiv:1601.03828.

Primary access:

- https://arxiv.org/abs/1601.03828
- https://doi.org/10.1016/j.jde.2017.04.019

Relation to A2 v19:

- Santaló-type identities and travelling-time averages already connect dynamical observations with geometric volume.
- A2's formula for `A` is instead a local algebraic consequence of the unconditional residual-time density.
- Its new use is to combine the recovered free area with the areas of one representative of each recovered obstacle class, thereby obtaining the period covolume and a finite arithmetic index.

The manuscript correctly does not claim general priority for recovering volume from dynamical data.

### 5. Marked-length rigidity for dispersing billiards

J. De Simoi, V. Kaloshin, and M. Leguil,  
*Marked length spectral determination of analytic chaotic billiards with axial symmetries*,  
*Inventiones Mathematicae* 233 (2023), 829–901; arXiv:1905.00890v4.

D. Finamore and M. Leguil,  
*A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*,  
arXiv:2510.18983v1 (2025).

Primary access:

- https://arxiv.org/abs/1905.00890
- https://arxiv.org/abs/2510.18983

Relation to A2 v19:

- These works use global marked or enriched marked length information and different dynamical/geometric mechanisms.
- A2 uses a finite selected collection of local endpoint laws.
- A2 does not identify those laws with a marked length spectrum and does not derive a stronger spectral theorem.
- The absence of a finite-horizon hypothesis in A2 concerns the selected local channels; it is not a comparison theorem for arbitrary global data.

### 6. Conditional analytic continuation

L. N. Trefethen,  
*Quantifying the ill-conditioning of analytic continuation*,  
*BIT Numerical Mathematics* 60 (2020), 901–915; arXiv:1908.11097.

Primary access:

- https://arxiv.org/abs/1908.11097
- https://doi.org/10.1007/s10543-020-00802-7

Relation to A2 v19:

- The global finite-data theorem propagates local arc error to complete analytic images through a standard two-constants/harmonic-measure estimate.
- The exponent depends on the analytic strip and continuation geometry.
- A2 does not claim a new theorem of complex analysis or a universal stability exponent.

## Assessment of the repaired comparison

The v19 primary and its `LITERATURE_AUDIT.md` substantially close the v18 literature objection.

In particular, the manuscript now states:

1. two endpoint densities are function-valued data, not two real numbers;
2. the densities are exactly equivalent, on the active physical class, to local lens/scattering information plus a normalization;
3. the affine elimination is elementary;
4. endpoint travel-time differentiation is established inverse-geometric technology;
5. A2's specific local increment is an explicit intrinsic inverse for two unknown reflecting arcs through the diagonal stationary Schur complement;
6. A2's global increment is the recovery of incidence and a finite-index unmarked period lattice from a shape-separated collection.

This is a fairer novelty statement than the v18 comparison.

The repair also narrows the editorial claim. Once the local datum is recognized as lens-equivalent, the primary conceptual novelty is not “two windows reveal geometry” in isolation. It is the combination of:

- the two-reflector intrinsic curvature formulas;
- whole-image analytic synchronization;
- incidence recovery from shape classes;
- local volume normalization;
- finite-index lattice descent;
- physical realization of the arithmetic ambiguity.

That combination appears plausibly new, but it is built from a rich selected information set and strong generic/analytic hypotheses. The literature repair therefore improves correctness and attribution without, by itself, elevating the work to the four-journal significance threshold.

## Remaining literature and attribution recommendations

1. Add a standard reference for Hermite normal form, finite-index sublattices of `Z^2`, and the divisor-sum enumeration. The proof is elementary, but a reference would fix conventions.
2. Keep Noakes–Stoyanov visible in the main introduction rather than only in a later comparison section; it is the closest local mechanism.
3. State explicitly that the periodic incidence/covolume descent, rather than the local affine quotient, is the principal v19 addition.
4. Avoid suggesting that the selected local law is a conventional unmarked lens data set. Its local origins, itinerary branches, record grouping, and coverage are experimental marks.
5. Do not compare the conditional upper exponent with unrelated minimax rates or with the older moment experiment without aligning the error parameter and information model.
6. Preserve the exact analytic count-only disclaimer; none of the cited travelling-time or marked-length theorems resolves that retained problem.

## Limits

No exhaustive bibliography or priority search was performed. I did not verify every historical version of every cited paper. The audit checks the theorem-level comparisons that carry the v19 novelty statement and the principal cited primary versions available in the manuscript.

The conclusion is that the nearest-comparison defect from v18 is substantially repaired. The remaining negative venue recommendation rests on the richness and selected nature of the information, the generic primitive scope of the global theorem, and the conditional character of the stability result—not on the continued absence of the obvious lens/travelling-time literature.
