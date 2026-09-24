# Response to the independent A2 v132 report

**Revision:** A2 v133, 23 September 2026.  
**Controlling report:** `reviews/a2-v132-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md` at `d76f34db1aaa8e196a7b50f4ec04be381d45236e`.  
**Reviewed full manuscript:** `6d8fcb430efa95624a15aa684cfccab79c793350`.  
**New branch:** `revision/a2-v133-schur-readout-exceptional-fibres-2026-09-23`.

We thank the referee for distinguishing the repaired descent and inverse
arguments from the remaining proof obligations. The full generic intrinsic
web reconstruction theorem is retained. We supply the missing universal
coefficient argument, isolate its functorial use, and add a geometric theorem
about the exceptional fibres. All inherited compiled mathematical inputs
and labels remain in the complete manuscript. A statement below that an
issue is addressed refers to the submitted proof, not to independent
referee approval or machine verification of that proof.

## E132.1 — universal coefficient readout

**Addressed by two standalone lemmas and a rewritten readout proof.**

`lem:universal-schur-readout` defines the full product-group equivariant map
Phi(beta tensor xi)(T) = beta((wedge^6 Sym^2 T)xi). It gives the precise
source, target, action on functions, dual representations, and the two
partitions (5,4,2,1) and (4,4,4,0). The proof treats all four source blocks:
the off-diagonal blocks vanish, and each diagonal block is a scalar times
the unique Cauchy inclusion. Highest-weight vectors are printed for both
blocks. Their coefficients on diagonal matrices are t1^5 t2^4 t3^2 t4 and
t1^4 t2^4 t3^4; both are one at the identity. Thus nonvanishing is proved
without a numerical sample or trusting the exact script.

Only after this universal statement do we fix beta_R. Independent variation
of the two right summands proves exactly the specific left-line formula
`eq:minor-coefficient-readout`. The rewritten `lem:plucker-component-readout`
extracts each line by contraction of the right factor. It never regards a
fixed-beta slice as a GL(V) representation.

`lem:readout-exterior-twist` writes exterior duality as
(w tensor omega)(eta)=omega(w wedge eta), checks it on a basis extending R,
and identifies both labels with the common (det V)^(-5) twist. All seven
requested points in the report are explicitly addressed.

## E132.2 — abstract isomorphisms and one common g

**Addressed by `lem:common-g-functoriality`.**

The lemma first constructs the graded map from the isomorphism of the powers
of the deepest-stratum ideal. The canonical symmetric-algebra surjection
then transports the actual homogeneous ideal. The intrinsic trivial versus
nontrivial ruling distinction is retained. In fact the argument supplies
one projective g over the whole deepest stratum: its value is a morphism
from the projective connected Grassmannian to the affine group PGL(V), and
therefore is constant. At a fibre the map is T -> g T h^(-1).

A commutative coefficient square is displayed and checked by evaluation.
Both left coefficient lines transform through F(g)^*, whereas h acts only
on the right factor. Exterior duality converts this to the same g on both
Pluecker components. The final reconstruction proof now invokes this lemma
instead of compressing these steps into prose. No ambient extension is used.

## S132.1 — geometry of exceptional reconstruction fibres

**Addressed by a new fibre theorem, candidate bound, and example.**

`thm:exceptional-component-fibres` gives an exhaustive scheme-theoretic
classification of fibres of the two-component morphism on the open where
both components are nonzero. The Pluecker quadrics restrict to (b-a)H_w.
Rank two gives a reduced point. Rank one gives the length-two divisor
[1:1]+[d:-c], whose second point can be distinct, doubled, or an excluded
pure endpoint. Rank zero gives a whole Grassmann line, equivalently the
four-planes between a fixed three-plane and five-plane. The flag description
is proved in a graph chart, not cited from a computation.

On the genuine reduced-secant locus the residual point operation is a regular
fixed-point-free involution. The tangent criterion Qw_R in wedge^3 R wedge W
distinguishes a double point from two distinct candidates. An explicit pair
of pure highest-weight endpoints proves the flag stratum nonempty in the
ambient component domain. Its failure of basepoint freeness is stated,
rather than misrepresenting it as a smooth-Jacobian example.

This is a geometric fibre theorem, not a computation of every invariant
exceptional component or its codimension. In particular, the rank-two
certificate can fail even when deleting a pure endpoint leaves one reduced
candidate. Equality of component pairs is necessary for a failure-scheme
isomorphism; a converse on exceptional fibres is not asserted.

## S132.2 — higher residual primary geometry

**Addressed by a precise hierarchy without deleting or weakening results.**

All corank-two orbit tables, collisions, determinant identities, relative
primary and Galois descent proofs, quotient-induced families, global support
laws and the sharp index-five theorem are preserved in the compiled article.
The complete embedded W3/W4 atlas at coranks three and four is not declared
computed. The abstract and `sec:primary-table-scope` distinguish the scope of
the complete primary tables from the all-corank support and nilpotence laws.
The full-scheme inverse theorem is unchanged and uses the maximal-minor
space directly, not a supposed uncomputed primary decomposition. This follows
the inverse-theorem route explicitly accepted in the report.

## M132.1 — Ballico 1993 and classical inverse geometry

**Classical inverse-data comparison expanded; Ballico 1993 full-text audit
remains documentary-open.**

The new `sec:inverse-data-comparison` compares actual inverse inputs against
Martin--Mezzedimi--Veniani, Proposition 3.6, Theorem 3.7 and Remark 3.8. A Fano
polarization/Reye bundle and its exchanged K3 line bundles are distinguished
from one unmarked quartic polarization. We explicitly acknowledge the
classical reconstruction of a web from appropriate Reye data. The new input
here is the abstract nonreduced failure scheme and its oriented deepest cone.
The full text and relevant diagrams of this primary source were inspected.

The complete available 1996 Ballico theorem text was inspected as well.
Its Grassmannian incidence/multiplication construction is a substantive
antecedent, not dismissed on terminology. Additional publisher and
institutional retrieval attempts for the distinct 1993 paper did not provide
the full text. `LITERATURE_AUDIT_V133.md` records the actual access outcomes.
No theorem numbers or nonanticipation conclusions are invented. The issue
matrix therefore does not mark the 1993 priority comparison closed. This
remaining documentary requirement does not change the reconstruction theorem.

## M132.2 — role of the universal relative-primary theorem

**Addressed by `sec:relative-tool-positioning`.**

The theorem is presented as a simultaneous finite-diagram relative-algebra
tool, using standard generic freeness, flattening, associated-point theory and
descent. The text identifies its application-specific combination: the finite
colon tower, exactness under base change, associated-point exhaustion,
downstairs support packets and the torsion modules computing lengths. It does
not claim primary existence or generic freeness as new foundational principles.

## Editorial organization and preservation

The introduction now defines the scheme before its invariants and states the
web reconstruction theorem before the polarized first-layer theorem. The
full inverse section follows the initial Fitting, filtration and polarization
sections, before the boundary atlas. The new exceptional-fibre theorem is
part of that inverse section. Universal/relative details have been relocated
within the outline instead of removed. The complete inherited mathematics,
including the already repaired packet descent, remains in the article;
weighted models and reproducibility material retain their appendix status.

## Verification and its limits

The build executes all seven inherited exact scripts plus
`checks/revision133_exact.py`, compiles the complete article three times, and
checks the input graph, inherited labels, citations, source hashes and PDF.
The new script checks 24 raising-operator identities, both diagonal coefficient
witnesses, a nontrivial left/right naturality calculation, all 30,240 quadratic
Pluecker relations on the printed flag line, and residual-involution, tangent
and endpoint polynomial identities. The structural proofs remain written
mathematics and are expressly not claimed to be machine certified.

The source-bound receipt records actual execution, not a prospective promise.
Neither the inherited AI-assisted report nor this response is a journal-issued
referee decision. The manuscript is submitted for renewed independent review.
