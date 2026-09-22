# Response to the independent v126 referee report

**Manuscript:** *Determinantal boundary atlas, nilpotent depth, and polarized reconstruction in multiplication failure*  
**Revision:** v127, September 23, 2026  
**Controlling report:** reviews/a2-v126-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md  
**Revision branch:** revision/a2-v127-determinantal-boundary-atlas-2026-09-23

We thank the referee for separating the genuinely new geometry already
present in v123--v125 from the standard deformation-to-the-normal-cone
mechanism introduced in v126. Revision 127 keeps every prior theorem,
primary calculation, collision law, reconstruction argument, and
classical comparison. It does not delete the difficult boundary.
Instead it replaces the open-ended higher-corank discussion by a finite
determinantal atlas and computes new strata explicitly named in the
report.

The central new theorem is not the Rees construction. On every Schur
chart
\[
 I_{\widehat D_R}=dJ,\qquad
 J=I_6[A_H,B_H(1\otimes T),C_H\operatorname{Sym}^2T],
\]
we prove \(d^5\in J\) by completing the six-row quotient map to a
\(10\times10\) isomorphism and expanding
\(\det(G\operatorname{Sym}^2M)\). Hence the intrinsic nilradical
satisfies \(N^6=0\) globally. There are at most five positive graded
layers on every projection-rank stratum.

We then compute the higher-dimensional mixed-kernel boundary at
projection corank two, give a finite rank-drop atlas for \(A_H\), prove
that projection corank three has only the exact depth alternatives five
and six, and prove that projection corank four has exact index five.
The latter uses
\[
 \bigwedge^6\operatorname{Sym}^2\mathbf C^4
 =
 \mathbb S_{(5,4,2,1)}
 \oplus
 \mathbb S_{(4,4,4,0)}
\]
and identifies the second summand with the Jacobian-quartic covariant
of the web.

## E126.1 — geometric classification of the associated graded object

The formal colon tower is now uniformly finite and is supplemented by
an explicit geometric and determinantal stratification.

Theorem thm:finite-all-corank-depth proves \(N^6=0\) and identifies
every multiplication map
\[
 N^i/N^{i+1}\otimes N^j/N^{j+1}
 \longrightarrow N^{i+j}/N^{i+j+1}
\]
as the canonical quotient multiplication
\[
 \mathcal O_{W_i}\otimes\mathcal O_{W_j}
 \twoheadrightarrow\mathcal O_{W_{i+j}},
\]
with the Schubert-line twist. Thus the multiplication law is not an
additional uncomputed datum once the support schemes are known.

Definition def:macaulay-atlas replaces an unspecified membership
condition \(d^k\in J\) by finite coefficient matrices. Since
\(d^5\in J\), only \(k=1,\ldots,5\) can occur. The strata are cut out
by minors of the Macaulay matrices and of their augmentations by the
coefficient vector of \(d^k\). Colon modules and multiplication
cokernels are included in the same finite flattening refinement.

On the first singular Schubert boundary the theorem is substantially
more explicit: Theorem thm:corank-two-mixed-kernel-atlas gives the
actual projective kernel geometry, exact nilpotency indices, Hilbert
functions or lengths of \(W_2,W_3\), and the first-layer contact
scheme.

## E126.2 — exceptional rank strata

### Rank drop of \(A_H\)

Proposition prop:rankdrop-coranktwo-depth treats every possible
corank-two pair
\[
 a=\operatorname{rank}A_H,\qquad
 b=\operatorname{rank}\overline B_H.
\]
After eliminating \(\operatorname{im}A_H\), every nonzero residual
minor has transverse degree at least \(2(6-a)-b\). Therefore
\[
 \min\{k:d^k\in J\}\ge 6-a-\lfloor b/2\rfloor.
\]
Together with \(d^5\in J\), this leaves a finite list of depth strata,
all defined by explicit augmented-rank equations. In the extreme type
\((a,b)=(0,3)\) the index is exactly six.

### Failure of mixed surjectivity and higher-dimensional mixed kernels

Assume first that \(A_H\) is injective. The quotient mixed map
\[
 \beta_H:H\otimes W\to E_H
\]
has nine orbit types under
\(GL(H)\times GL(W)\times GL(E_H)\): rank-three kernel points off or
on the Segre quadric; rank-two secant, tangent, \(H\)-ruling, and
\(W\)-ruling kernel lines; rank-one dual tensors of rank two or rank
one; and the zero mixed map. The two ruling families are kept
separate because their nilpotent behavior is different.

On the coefficient-transverse opens the exact nilpotency indices are
\[
 3,3,3,3,4,3,4,4,4.
\]
The second-layer lengths in the zero-dimensional cases are
\(1,3,8,8,15\); the remaining cases have the precise Hilbert
polynomials printed in the theorem. The third layer is computed in all
nine cases.

The first layer is also extended beyond mixed regularity. Modulo
\(\delta\), every surviving residual minor has exactly two mixed
columns and one quadratic column, giving
\[
 J+(\delta)=(\delta,h_H(u)\operatorname{Sym}^4(v)).
\]
Thus the unsplit contact quartic remains the first graded symbol for
every \(A_H\)-injective corank-two point.

### Projection corank three

Theorem thm:corank-three-depth covers the whole corank-three locus,
including all \(A_H\)- and mixed-block rank drops. A Schur-type
calculation proves \(d^3\notin J\). Since \(d^5\in J\), the exact
nilpotency index is five or six, and the two cases are separated by
one degree-twelve augmented Macaulay rank condition
\(\varepsilon_4(J)\).

### Projection corank four

Theorem thm:corank-four-jacobian gives
\[
 d^3\notin J,\qquad d^4\in J,
\]
so the deepest Schubert stratum has exact index five. The first
statement follows from the absence of \((\det V)^3\) in
\(\bigwedge^6\operatorname{Sym}^2V\). The second follows because the
\(\mathbb S_{(4,4,4,0)}\) component is dual, up to determinant twist,
to the Jacobian-quartic covariant of \(\bigwedge^4R\); its nonzero
value on \(G_4^\circ\), followed by the Pieri product, supplies
\((\det V)^4\), i.e. \(d^4\).

### Deeper nilpotent layers

There are no layers beyond degree five. This is now a theorem, not an
expectation or a finite experiment.

## E126.3 — scope of the headline claim

The broad v126 sentence about computing the special fibre across the
first singular Schubert boundary has been replaced by a precise
theorem list: global \(N^6=0\), the nine-orbit corank-two atlas, the
finite rank-drop atlas, the corank-three exact dichotomy, and the
corank-four exact index-five theorem. This is stronger mathematically
but no longer identifies the standard Rees container with the
classification itself.

## E126.4 and E126.6 — Ballico 1993 and standard DNC citations

The complete Ballico 1993 theorem text is still not available in the
repository. On September 23, 2026 we rechecked the publisher record
for DOI 10.1002/mana.19931630102; it verifies the article metadata but
a readable complete article text was not obtained from the available
routes. We therefore continue not to infer anticipation or
nonanticipation from its title or metadata.

This documentary limitation is no longer used to support any novelty
claim. The theorem-level comparison with the accessible 1996 paper is
retained and the 1993 item is explicitly fenced in
LITERATURE_AUDIT_V127.md.

The deformation-to-the-normal-cone construction is now cited to
Fulton, *Intersection Theory*, section 5.1, and the Stacks Project,
Tag 062Z. Flattening stratification is cited to Stacks Tag 052F. The
manuscript explicitly labels these as standard mechanisms.

## M126.1 and E126.5 — the inverse problem

The v123 polarized reconstruction theorem remains unchanged: the
first nilpotent layer reconstructs the polarized quartic K3 and the
web-to-K3 map is generically finite on the stated regular locus.

Revision 127 adds intrinsic information beyond the polarized quartic:
the higher graded supports, their orbit types, depth jumps, and
multiplication laws. These invariants are preserved by an abstract
isomorphism of the failure scheme and therefore refine the finite
Torelli packet. We do not convert the previously proved finite-etale
cover into a claimed degree-one theorem without a separate lattice
enumeration; instead the new boundary atlas supplies the concrete
extra structure on which such separation can be tested. The principal
novelty claim of v127 no longer rests on the formal finite-etale
statement.

## M126.2 and M126.3 — standard versus manuscript-specific geometry

Section sec:rees-specialization-v127 now has a separate novelty-boundary
remark. Standard items are the extended Rees algebra, deformation to
the normal cone, and flattening stratification.

The manuscript-specific items are the multiplication Fitting
factorization, \(d^5\in J\), the global depth-six cutoff, the nine
mixed-kernel normal forms and graded supports, the corank-three Schur
exclusion, the corank-four Jacobian-covariant calculation, the primary
collision laws, and the polarized K3 reconstruction.

## M126.4 — residual colons versus geometry

The residual-colon identity is retained because it is the
coordinate-free formula for the graded pieces. It is no longer
presented as the geometric classification by itself. The geometry is
supplied by the Segre incidence type of
\(\mathbf P(\ker\beta_H)\), the explicit normal forms and Hilbert
functions at corank two, the rank-drop degree table, the finite
Macaulay determinantal strata, and the exact corank-three/four depth
theorems.

## Verification

checks/boundary_atlas.py independently recomputes the integer
normal-form colons and Hilbert functions and verifies the representation
characters used in the corank-three/four proofs. These checks are
regression evidence only; the proof is in the TeX.

The v127 workflow reruns the inherited v125 exact K3, corank-two, and
stratified-rank-two regressions, runs the new boundary-atlas
regressions, compiles the principal article three times, checks
citations and references, and publishes the source-bound PDF and
evidence only on the v127 branch.
