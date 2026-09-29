# Targeted literature audit for the A2 v20 rereview

## 1. Scope

This note is a targeted theorem-category check for the new v20 material. It is not an exhaustive novelty or priority search.

The retained v19 comparison already places the two-density local inverse in relation to:

- local boundary and lens rigidity;
- obstacle travelling-time/scattering rigidity;
- Santaló-type volume normalization;
- marked-length rigidity for dispersing billiards;
- conditional analytic continuation.

That comparison remains relevant and is not repeated here. The new question in v20 is different: how the graph of all bounded-length clear shortest normal bridges relates to classical proximity and visibility graphs, and how the quotient cycles recover the period group.

## 2. References newly added by the author

Version 20 adds two appropriate standard references.

### Henri Cohen

H. Cohen, *A Course in Computational Algebraic Number Theory*, Graduate Texts in Mathematics 138, Springer, 1993, Chapter 2, pp. 45--107.

The cited chapter is a standard source for Hermite and Smith normal forms and finite-index integer lattices. The manuscript also proves the rank-two lattice statements it actually uses, so the reference supplies attribution and convention rather than an unseen proof step.

### Jonathan L. Gross

J. L. Gross, “Voltage graphs,” *Discrete Mathematics* 9 (1974), 239--246, DOI `10.1016/0012-365X(74)90006-5`.

This is an appropriate attribution for the graph-cover viewpoint. The manuscript proves the needed path-lifting statement directly: a lifted path from a root copy to one of its translates projects to a closed quotient walk whose signed edge translation is the deck transformation.

Neither integer normal forms nor graph-cover lifting is advertised as a new theorem.

## 3. Missing closest proximity-graph comparison

### Godfried Toussaint, relative neighborhood graphs

G. T. Toussaint, “The relative neighbourhood graph of a finite planar set,” *Pattern Recognition* 12 (1980), 261--268, DOI `10.1016/0031-3203(80)90066-7`.

Toussaint defines a graph by keeping a pair when there is no third point closer to both endpoints. The paper proves that the relative neighborhood graph contains the Euclidean minimum spanning tree and is contained in the Delaunay triangulation.

The v20 obstruction-descent lemma has a visibly related logical form: if a shortest bridge is blocked by a third obstacle, each of the two replacement gaps is strictly shorter. Repeating this process retains connectivity while discarding obstructed pairs. The objects are convex bodies rather than points, the edge predicate is a clear shortest normal bridge rather than the standard lune predicate, and the setting is a periodic infinite family. Thus Toussaint's theorem does not by itself subsume v20. It is nevertheless a closer conceptual comparator than the present bibliography acknowledges.

### Jaromczyk--Toussaint survey

J. W. Jaromczyk and G. T. Toussaint, “Relative Neighborhood Graphs and Their Relatives,” *Proceedings of the IEEE* 80 (1992), no. 9, 1502--1517, DOI `10.1109/5.163414`.

This survey covers neighborhood/proximity graphs, their structural properties, algorithms and applications. It is a natural entry point for assessing whether the clear-bridge graph belongs to an established family of proximity graphs for extended objects or metrics. A submitted version should use this literature to state precisely what changes when the vertices are periodically repeated strictly convex bodies and when obstruction is defined by physical intersection of the unique closest segment.

## 4. Missing closest visibility-graph comparison

### Pocchiola--Vegter visibility complex

M. Pocchiola and G. Vegter, “The visibility complex,” *International Journal of Computational Geometry & Applications* 6 (1996), no. 3, 279--308, DOI `10.1142/S0218195996000204`.

The visibility complex organizes free rays among pairwise disjoint convex obstacles and has combinatorial complexity controlled by free bitangents. The paper is relevant to the category of data used by v20: visible tangent/normal relations between convex obstacles.

### Pocchiola--Vegter pseudotriangulation sweep

M. Pocchiola and G. Vegter, “Topologically sweeping visibility complexes via pseudotriangulations,” *Discrete & Computational Geometry* 16 (1996), 419--453, DOI `10.1007/BF02712876`.

This work constructs the free bitangents of disjoint convex obstacles and computes the corresponding visibility graph/complex. V20 uses only the unique shortest common normal segment between each pair, not all free bitangents, and imposes a metric range cutoff. The algorithms and cell structures therefore do not immediately imply the v20 covering-radius theorem. They do show that visibility structures of disjoint convex obstacles form a developed subject whose relation to the new “complete short clear normal catalogue” should be explained.

## 5. What the current comparison does and does not establish

The targeted search found no source among the references above that states the exact v20 theorem:

- periodic disjoint strictly convex bodies;
- all clear unique shortest bridges below `R`;
- connectivity when `R` exceeds twice the obstacle-union covering radius;
- generation of the full translational period lattice by quotient cycles;
- combination with intrinsic endpoint-law inversion and covolume calibration.

Accordingly, this audit does **not** conclude that the new theorem is already known.

It does conclude that the manuscript's present attribution is incomplete. The geometric heart of v20 lies close to two established areas:

1. proximity graphs whose sparse edge predicates preserve connectivity or spanning trees;
2. visibility and free-bitangent structures of disjoint convex obstacles.

A four-journal significance claim requires a theorem-level comparison with these areas, not only references for the subsequent voltage-graph and lattice-algebra steps.

## 6. Suggested comparison questions for a revised manuscript

A useful revision should answer the following questions explicitly.

1. Is the clear-shortest-bridge graph a known relative-neighborhood, Gabriel, or generalized proximity graph for convex sets under the set-distance metric?
2. Does a minimum spanning forest of the complete weighted graph on obstacle copies automatically consist of clear shortest bridges, giving another proof of connectivity?
3. Which part of the obstruction-descent theorem depends essentially on periodicity, and which is valid for any locally finite family?
4. How does the catalogue of shortest normal bridges sit inside the free-bitangent visibility complex?
5. Are there earlier connectivity or spanner results for visibility graphs of pairwise disjoint convex bodies that imply a comparable bounded-range statement?
6. Is the constant `2` in the covering-radius threshold sharp for the stated graph, or merely sufficient?

These questions do not create correctness objections to the supplied proof. They are necessary to assess novelty, optimality, and conceptual force.

## 7. Literature-audit conclusion

The retained travel-time/lens comparison and the new Cohen/Gross attribution are appropriate. The closest proximity- and visibility-graph literature is still missing.

The exact combination in v20 may be new, but the current source record does not establish that its geometric mechanism is conceptually outside classical relative-neighborhood, spanning-tree, visibility-complex, or free-bitangent principles. This omission materially weakens a top-four significance claim even though it does not invalidate the theorem.