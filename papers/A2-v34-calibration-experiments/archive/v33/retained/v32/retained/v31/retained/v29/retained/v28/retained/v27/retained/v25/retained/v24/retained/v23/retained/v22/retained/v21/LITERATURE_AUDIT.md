# Primary-source comparison audit — 29 September 2026

This ledger records the nearest additional literature requested by the v20 referee. It is not an exhaustive priority search. Existing lens, travel-time, marked-length, analytic-continuation, voltage-graph and integer-normal-form references remain in the primary and unchanged historical comparison.

## Toussaint: relative-neighborhood graph

G. T. Toussaint, *The relative neighbourhood graph of a finite planar set*, Pattern Recognition 12 (1980), 261–268, DOI 10.1016/0031-3203(80)90066-7.

The author's full retypeset PDF was accessed at https://cgm.cs.mcgill.ca/~godfried/publications/relng.pdf. The title/abstract and proof of Theorem 1 were inspected in page images as well as parsed text. The theorem places the Euclidean minimum spanning tree inside the finite-point relative-neighborhood graph. The strict third-neighbor edge replacement is the direct antecedent of the gap-relative argument; it is explicitly credited in Section 7.5.

Difference of scope: our gaps are between extended bodies and need not obey the triangle inequality; the graph is infinite periodic and the conclusion includes deck-period generation. Proposition 7.10 supplies the direct additional proof. We do not claim the general descent principle as new.

## Jaromczyk–Toussaint: survey

J. W. Jaromczyk and G. T. Toussaint, *Relative neighborhood graphs and their relatives*, Proceedings of the IEEE 80 (1992), 1502–1517, DOI 10.1109/5.163414.

The publisher-indexed metadata and abstract were checked. The publisher page itself was access-limited. No claim is made to have audited every result in the full survey, and no unverified theorem number is cited. It is used to identify the classical family of proximity graphs, variants and algorithmic questions, not as an unexamined premise of a proof.

## Pocchiola–Vegter: visibility complex

M. Pocchiola and G. Vegter, *The visibility complex*, Proc. 9th Annual ACM Symposium on Computational Geometry (1993), 328–337, DOI 10.1145/160985.161159.

The authors' institutional record and abstract were checked at https://research.rug.nl/en/publications/the-visibility-complex/. Its linked proceedings PDF was access-restricted. The detailed algorithmic comparison below is instead pinned to an accessible full author report, not attributed to an unseen page of this proceedings paper.

## Pocchiola–Vegter: free bitangents and pseudo-triangulations

M. Pocchiola and G. Vegter, *Computing Visibility Graphs via Pseudo-triangulations*, LIENS-95-15, April 1995. Full primary report: https://www.di.ens.fr/reports/1995/liens-95-15.A4.pdf.

The 36-page report was opened; the introduction and Theorem 1 (printed p. 3; PDF page index 4) were checked in the page image. Theorem 1 computes k free bitangents of n given disjoint convex obstacles in O(k+n log n) time and O(n) working space, assuming pairwise bitangents are computable in constant time; it also permits the visibility graph/complex. Sections 2–3 describe the visibility complex and greedy pseudo-triangulation algorithm. The report identifies a preliminary version in SCG 1995.

This is a theorem-level forward-computation comparison: the geometry is supplied, the segments are tangent, and the computational primitives are stated. Our local return bridge is normal and non-grazing; its density determines previously unknown arcs. The finite padded scan still presumes geometric selection primitives and does not inherit the visibility algorithm or its complexity. The manuscript's new contribution is the finite-aperture quotient reduction and persistence of sufficient inverse data, not a claimed replacement of these classical algorithms.

## Limitations

No formal literature-priority certificate, exhaustive survey, or top-journal significance conclusion follows from these checks. The referee's editorial judgment is not treated as a mathematical hypothesis. All bibliography entries cited by the new proof have a reachable identifier, and the test suite checks citation resolution rather than scholarly originality.
