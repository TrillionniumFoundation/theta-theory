# Literature audit for the external A2 v21 rereview

**Reviewed source:** `5ab3be483386dab1b2f53575f47dbf7aebd92bd3`  
**Date:** 29 September 2026

This is a targeted theorem-level comparison for the new finite-aperture and persistence chapter. It is not an exhaustive priority search, a novelty certificate, or a substitute for mathematical review of the manuscript. The boundary-distance, lens, travelling-time, marked-length, voltage-graph and integer-normal-form references already retained in v20 were not re-audited in full.

## 1. Relative-neighborhood graphs

G. T. Toussaint, *The relative neighbourhood graph of a finite planar set*, Pattern Recognition **12** (1980), 261–268, DOI `10.1016/0031-3203(80)90066-7`.

The full author PDF was inspected. Its Theorem 1 proves that the Euclidean minimum spanning tree of a finite planar point set is contained in the relative-neighborhood graph. The familiar contradiction replaces an excluded edge by shorter connections through a third point. This is the nearest classical antecedent of the strict shorter-gap replacement used in A2 v20 and recast in v21 as the gap-relative subgraph.

The comparison does not subsume the manuscript. In A2:

- vertices are extended strictly convex bodies rather than points;
- body gaps need not satisfy a triangle inequality;
- the graph is an infinite periodic lift with a finite quotient;
- the desired conclusion includes generation of the deck-period lattice, not only finite connectivity or containment of an MST;
- edges are closest normal bridges and must also be physically clear.

Version 21 now credits the third-neighbor mechanism and supplies its own proof of component equivalence and period generation. It no longer advertises shorter-neighbor descent as a new abstract proximity-graph principle.

## 2. Survey context for proximity graphs

J. W. Jaromczyk and G. T. Toussaint, *Relative neighborhood graphs and their relatives*, Proceedings of the IEEE **80** (1992), 1502–1517, DOI `10.1109/5.163414`.

The indexed metadata and abstract were checked. This source is appropriately used as a survey reference for the family of relative-neighborhood, Gabriel and related proximity graphs and their algorithmic questions. The v21 article does not assign an unverified theorem number to the survey and does not use it as a proof premise.

No direct theorem was found in the checked material that simultaneously treats periodic families of extended convex bodies, shortest normal bridges, obstruction by third bodies, and generation of the full translation group. That observation is not an exhaustive absence claim.

## 3. Visibility complexes and free bitangents

M. Pocchiola and G. Vegter, *The visibility complex*, Proc. 9th ACM Symposium on Computational Geometry (1993), 328–337, DOI `10.1145/160985.161159`.

M. Pocchiola and G. Vegter, *Computing Visibility Graphs via Pseudo-triangulations*, LIENS-95-15, April 1995.

The accessible full 1995 author report was inspected. Its Theorem 1 gives an output-sensitive construction of the free bitangents and the visibility graph/complex of a supplied finite family of pairwise disjoint convex obstacles, under a constant-time pairwise-bitangent primitive. The stated bounds are `O(m log m+k)` time and `O(m)` working space for `m` obstacles and `k` free bitangents.

This is a relevant forward-geometric comparison, but the objects and information contract differ:

- a free bitangent is tangent to its endpoint obstacles;
- the A2 bridge is a closest common normal and its billiard return is non-grazing;
- Pocchiola–Vegter start from an explicit obstacle representation;
- A2 starts its inverse stage from local endpoint probability laws;
- the v21 scanner nevertheless assumes geometric shortest-pair and blocker tests on the unknown bodies, so it cannot inherit the visibility algorithm or its complexity for free.

The manuscript now states these distinctions and does not conflate the two graphs.

## 4. Boundary-distance, lens and travelling-time context

The retained bibliography includes:

- P. Stefanov, G. Uhlmann and A. Vasy, *Local and global boundary rigidity and the geodesic X-ray transform in the normal gauge*, Ann. of Math. **194** (2021), 1–95;
- T. Gurfinkel, L. Noakes and L. Stoyanov, *Travelling times in scattering by obstacles in curved space*, J. Differential Equations **269** (2020), 9508–9530;
- L. Noakes and L. Stoyanov, *Travelling times in scattering by obstacles*, J. Math. Anal. Appl. **430** (2015), 703–717.

These remain the nearest information-category comparison for the local two-density inverse inherited from v18–v20. Two endpoint densities recover a generating/travel-time action by an affine quotient, and diagonal derivatives recover local geometry. The cited rigidity results do not obviously contain the exact two-reflection Liouville-density formula, the explicit two-curvature Schur-complement inverse, or the periodic aperture/witness theorem. Conversely, A2's sensor is richer and more purpose-built than a conventional marked-length invariant.

Version 21 does not materially change this local comparison; its novelty claims concern finite acquisition of enough local laws and persistence of a sufficient global witness.

## 5. Periodic graph and lattice algebra

J. L. Gross, *Voltage graphs*, Discrete Mathematics **9** (1974), 239–246, and H. Cohen, *A Course in Computational Algebraic Number Theory*, Chapter 2, remain suitable references for the graph-cover and Hermite/Smith-normal-form viewpoints used in the retained all-cycle theorem.

The new sparse-witness lemma is an elementary subgroup argument: adjoining an element outside a finite-index subgroup produces a proper divisor of the index, hence at least a factor-two decrease. I found no need for a stronger external theorem, and the manuscript does not claim this elementary lemma as a broad new result in group theory.

## 6. Editorial consequence

The v21 literature revision substantively closes the concrete omission identified in the v20 report. The closest proximity and visibility mechanisms are now acknowledged at theorem level, and the manuscript carefully separates its periodic inverse conclusion from classical finite forward-construction algorithms.

This repair does not by itself establish top-four significance. The principal remaining editorial question is whether a rich endpoint-law sensor, a geometry-aware exhaustive scanner, strong analytic/generic priors and a local retained-witness theorem reveal a sufficiently universal inverse principle. The referee report answers that question negatively at the requested benchmark while recognizing serious specialist-journal potential.

## 7. Limitations

- No exhaustive search of convex-body proximity structures, periodic visibility graphs, inverse scattering, or billiard rigidity was performed.
- Access limitations prevented a complete line-by-line audit of every cited survey or proceedings paper; detailed algorithmic statements were pinned to an accessible full primary report.
- No assertion is made that the checked sources establish or refute historical priority for the exact combination in A2 v21.
- Bibliographic comparison does not certify the mathematical proofs or determine a journal decision.
