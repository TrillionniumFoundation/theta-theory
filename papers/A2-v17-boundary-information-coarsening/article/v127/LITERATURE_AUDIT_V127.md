# Literature audit for A2 v127

## Ballico 1993

E. Ballico, “On the failure locus of higher order properties of
embeddings in projective spaces,” *Mathematische Nachrichten* 163
(1993), 5--13, DOI 10.1002/mana.19931630102.

On September 23, 2026 the publisher issue record and DOI metadata were
rechecked. They verify the bibliographic data and expose a PDF route,
but a readable complete article text was not obtained in the available
research environment. Accordingly:

- v127 makes no theorem-level anticipation or nonanticipation claim
  about the unread 1993 article;
- metadata are not substituted for hypotheses or theorem statements;
- the accessible 1996 continuation remains the source for the
  theorem-level comparison already present in the manuscript;
- none of the new v127 boundary-atlas theorems depends on a priority
  claim against Ballico 1993.

This is a documentary limitation, not a mathematical premise.

## Standard deformation to the normal cone

The extended Rees construction and normal cone are now explicitly
cited as standard:

- W. Fulton, *Intersection Theory*, 2nd ed., section 5.1.
- The Stacks Project, Section 31.20, Tag 062Z.

Flattening stratification is cited to The Stacks Project, Section
38.21, Tag 052F.

## Representation-theoretic input

The only representation calculation newly used in v127 is the
multiplicity-one decomposition
\[
 \bigwedge^6\operatorname{Sym}^2\mathbf C^4
 =
 \mathbb S_{(5,4,2,1)}
 \oplus
 \mathbb S_{(4,4,4,0)}
\]
and the elementary \(GL_3\) exterior-symmetric-square decompositions
printed in the proof. The manuscript gives the exact decompositions
it uses; Fulton--Harris is added as a general representation-theory
reference. checks/boundary_atlas.py independently verifies the
characters.
