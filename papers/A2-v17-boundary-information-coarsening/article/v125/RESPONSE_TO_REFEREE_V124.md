# Response to the independent A2 revision-124 referee report

**Manuscript:** *Nilpotent depth, stratified contact algebra, and polarized reconstruction in multiplication failure*  
**Revision:** 125  
**Controlling report:** reviews/a2-v124-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md  
**Revision branch:** revision/a2-v125-stratified-nilpotent-contact-boundary-2026-09-23  
**Date:** 23 September 2026

We thank the referee for isolating the exact structural gap in Revision 124. Revision 125 does not answer that report by adding terminology around the former block formula. It adds a global theorem on the nilpotent algebra itself, then computes the first singular boundary in explicit primary form.

The principal new theorem is the following. Let \(\widehat\Delta_R=(\widehat D_R)_{\mathrm{red}}\) be the Schubert divisor and set
\[
 \mathcal J_R^{\mathrm{res}}
 =
 (\mathcal I_{\widehat D_R}:\mathcal I_{\widehat\Delta_R}).
\]
For every \(j\ge1\), define the canonical colon scheme
\[
 W_j=
 V_{\widehat\Delta_R}\!\left(
 (\mathcal J_R^{\mathrm{res}}:
  \mathcal I_{\widehat\Delta_R}^{\,j-1})
 +\mathcal I_{\widehat\Delta_R}\right).
\]
Revision 125 proves on the **whole Grassmannian**, at every projection corank and every rank-drop point,
\[
 \operatorname{Ann}_{\mathcal O_{\widehat D_R}}
 (\widehat{\mathcal N}_R^{\,j})
 =
 \frac{
 (\mathcal J_R^{\mathrm{res}}:
  \mathcal I_{\widehat\Delta_R}^{\,j-1})
 }{\mathcal I_{\widehat D_R}}
\]
and
\[
 \operatorname{gr}_{\widehat{\mathcal N}_R}
 \mathcal O_{\widehat D_R}
 \simeq
 \mathcal O_{\widehat\Delta_R}
 \oplus
 \bigoplus_{j\ge1}
 \mathcal L^{\otimes j}\otimes\mathcal O_{W_j},
 \qquad
 \mathcal L=
 \mathcal I_{\widehat\Delta_R}/
 \mathcal I_{\widehat\Delta_R}^{\,2}.
\]
On a Schur chart \(\mathcal I_{\widehat\Delta_R}=(d)\),
\(\mathcal I_{\widehat D_R}=dJ\), this becomes
\[
 \operatorname{Ann}(N^j)=(J:d^{j-1})/(dJ),\qquad
 N^j/N^{j+1}\simeq
 A/\bigl((d)+(J:d^{j-1})\bigr),
\]
with exact nilpotency index
\[
 1+\min\{k\ge0:d^k\in J\}.
\]
This is the requested global replacement of the former formal all-corank rewrite.

On the mixed-regular projection-corank-two locus the abstract colon schemes are then computed explicitly. If
\[
 \delta=ad-bc,\qquad
 \mathfrak m=(a,b,c,d),\qquad
 I_H=(\delta,g_0,\ldots,g_4)
\]
is the unsplit contact ideal, Revision 125 proves
\[
 J=I_H\cap\mathfrak m^3,\qquad
 \mathcal I_{\widehat D_R}
 =\delta I_H\cap\mathfrak m^5.
\]
Thus \(\mathfrak m^5\) is an actual irredundant vertex-primary component throughout the mixed-regular collision boundary. If
\[
 h_H=\prod_{\nu=1}^s\ell_\nu^{e_\nu},
 \qquad \sum e_\nu=4,
\]
then the associated primes are
\[
 (\delta),P_1,\ldots,P_s,\mathfrak m,
\]
and the generic \(P_\nu\)-primary type is
\[
 (\delta^2,\delta q_\nu^{e_\nu},q_\nu^{e_\nu+1}).
\]
Moreover
\[
 N/N^2\simeq P/I_H,\qquad
 N^2\simeq P/\mathfrak m,
\]
so the first two graded layers are computed simultaneously on a neighborhood crossing the corank-one/corank-two boundary.

The revision also treats the two boundary phenomena specifically requested in the report. If \(h_H\equiv0\), then
\[
 I_H=(\delta),\qquad
 J=\delta\mathfrak m,\qquad
 \mathcal I_{\widehat D_R}
 =\delta^2\mathfrak m
 =(\delta^2)\cap\mathfrak m^5,
\]
and the containment locus is canonically the finite reduced Fano scheme \(F_1(Y_R)\) of lines on the smooth quartic. If the one-dimensional mixed kernel crosses from tensor rank two to a decomposable tensor, under the stated transverse nonvanishing condition the second colon support becomes
\[
 Z_2=V(c,d,a^2,ab,b^2),
\]
a canonical length-three nonreduced thickening of the rank-two vertex. This gives the first non-mixed-regular wall scheme-theoretically rather than only through a block presentation.

Finally, the finite inverse problem is upgraded from qualitative finiteness to a finite étale monodromy theorem on dense opens.

## E124.1 — replace the formal all-corank rewrite by actual structure

**Resolved by the referee's Option C.**

Revision 124 used the all-corank block identity as more structural language than the identity justified. Revision 125 keeps that identity only as a computational presentation and proves a different theorem: the global residual-colon filtration and associated-graded algebra above. It is intrinsic, valid at all projection coranks and all rank-drop points, and computes every annihilator layer and every nilpotency index from the residual colon tower.

The explicit rank-two calculation then identifies the first two global graded supports, proves the entire mixed-regular collision specialization law, and computes the first decomposable mixed-kernel wall. The manuscript now consistently calls the matrix identity a *projection-rank residual block presentation* and reserves *structure theorem* for the residual-colon/associated-graded result.

**Locations:** Theorem thm:global-residual-colon in parts/09-stratified-nilpotent.tex; headline Theorem thm:main-depth in parts/01-introduction.tex; parts/08-corank-boundary.tex.

## E124.2 — compute nilpotent depth across strata

**Resolved globally and then geometrically at the first boundary.**

The canonical schemes \(Z_j=V(\operatorname{Ann}(N^j))\) are now identified globally by colon ideals, and the associated graded algebra is explicitly
\[
 \mathcal O_{\widehat\Delta_R}
 \oplus
 \bigoplus_{j\ge1}
 \mathcal L^{\otimes j}\otimes\mathcal O_{W_j}.
\]
This is one sheaf-theoretic identity on the whole Grassmannian, not a comparison of unrelated strata.

At corank one, \(W_1\) is the ramification support \(E_R\). On the adjacent mixed-regular corank-two chart,
\[
 Z_1=V(I_H\cap\mathfrak m^3),\qquad
 Z_2=V(\mathfrak m).
\]
The decomposable-kernel theorem records the first change of \(Z_2\) beyond mixed regularity.

**Locations:** parts/04-depth.tex; Theorems thm:global-residual-colon, thm:graded-nilpotent, and thm:decomposable-kernel-wall.

## E124.3 — correct and strengthen contact-cover globalization

**Resolved.**

The revision now separates three objects that were too close in Revision 124:

1. the globally defined discriminant divisor \(V(\operatorname{Disc}(h_R))\);
2. the branch divisor only on the finite-flat locus \(G_R^{\mathrm{fin}}\);
3. the interpretation of four étale contact sheets as primary branches only on
\[
 G_R^{\mathrm{mr}}
 \cap
 (G_R^{\mathrm{fin}}\setminus\mathfrak D_R).
\]

The fifth-power statement is no longer inferred from the existence of the global ideal. The saturated contact theorem proves
\[
 \delta J=\delta I_H\cap\mathfrak m^5
\]
and proves \(\delta I_H\) is \(\mathfrak m\)-saturated when \(h_H\ne0\); hence \(\mathfrak m^5\) is genuinely irredundant. When \(h_H=0\), the separate calculation
\[
 \delta^2\mathfrak m=(\delta^2)\cap\mathfrak m^5
\]
shows the same vertex component survives the nonfinite containment geometry.

Repeated contacts are no longer described by forcing the simple-root formula onto the boundary; their generic primary types are
\[
 (\delta^2,\delta q^e,q^{e+1}).
\]

**Locations:** parts/08-corank-boundary.tex; Theorem thm:saturated-contact and Proposition prop:containment-lines in parts/09-stratified-nilpotent.tex.

## E124.4 — Ballico 1993

The mathematical revision does not use an assertion of non-anticipation by Ballico 1993. We repeated the documentary search against the official Wiley volume/DOI record on 23 September 2026. The issue record exposes a PDF action, but the accessible endpoint in the present environment resolves to the article record rather than complete theorem text. We therefore continue to mark ballico_1993_complete_text_read=false.

The full 1996 Ballico paper remains inspected at theorem level and is compared explicitly. Revision 125 does not use the unread 1993 source as evidence either for or against novelty. The new mathematical theorem is stated independently as the residual-colon/associated-graded structure theorem above.

**Locations:** parts/10-reye-priority.tex; LITERATURE_AUDIT.md; build receipt flag.

## E124.5 — advance the inverse problem

**Resolved by the precise finite-fibre/monodromy alternative requested in the report.**

Let \(\mathcal W\) be the irreducible nine-dimensional regular-web quotient on the finite-stabilizer open and \(\mathcal K\) the nine-dimensional polarized-K3 image. Revision 125 proves that there are dense opens
\[
 \mathcal W^\circ\to\mathcal K^\circ
\]
forming a finite étale cover of constant degree
\[
 d_{\mathrm{Tor}}=[\mathbf C(\mathcal W):\mathbf C(\mathcal K)].
\]
Its geometric monodromy is transitive, and is identified field-theoretically through the normal closure of the function-field extension.

The contact incidence and its discriminant descend from the polarized quartic and are therefore constant on a Torelli fibre. This shows precisely which rank-two data cannot by themselves split \(d_{\mathrm{Tor}}\), and localizes further separation to genuinely web-dependent boundary structure.

No generic-degree-one assertion is inserted without proof.

**Location:** Theorem thm:torelli-monodromy in parts/10-reye-priority.tex.

## E124.6 — isolate the theorem after classical Reye geometry is removed

Revision 125's nonclassical theorem can be stated without the number nine:

> From the abstract multiplication-failure Fitting scheme one obtains an intrinsic residual-colon filtration whose associated graded algebra is determined at every projection corank. Its first layer reconstructs the polarized quartic K3. Across the first singular Schubert boundary the next graded layers are the unsplit contact cone and the rank-two Schubert support; the complete mixed-regular collision primary law, the zero-quartic containment algebra, and the first decomposable mixed-kernel wall are determined scheme-theoretically.

The classical Reye/nodal-Enriques family and the equality \(24-15=9\) remain explicitly credited as classical context.

## M124.1 — finite Torelli packet

The packet is now a finite étale monodromy cover on dense opens, with a constant field-theoretic degree and transitive geometric monodromy. The revision also proves that the contact cover descends from the K3 side and hence is constant on the finite fibre.

## M124.2 — parameter-to-Hilbert bridge

Revision 125 adds an explicit \(\PGL(V)\)-equivariant morphism from the regular web Grassmannian to the Reye Hilbert component and identifies the general tangent map
\[
 \operatorname{Hom}(R,\operatorname{Sym}^2V/R)
 \xrightarrow{\sim}
 T_{[\operatorname{Reye}(R)]}\operatorname{Hilb}_{\mathrm{Reye}}.
\]
Quotienting its projective-coordinate orbit yields the nine-dimensional tangent quotient. The exact \(25\times25\) determinant remains only the arithmetic maximal-rank witness for the particular Jacobian-quartic map.

**Location:** Proposition prop:web-hilbert-bridge in parts/10-reye-priority.tex.

## M124.3 — zero-quartic containment

**Resolved as a separate geometry, not a collision partition.**

The locus \(h_H\equiv0\) is exactly \(F_1(Y_R)\). For a line \(L\subset Y_R\),
\[
 N_{L/Y_R}\simeq\mathcal O_{\mathbf P^1}(-2),
\]
so the Fano scheme is zero-dimensional and has zero Zariski tangent space at every point; hence it is finite reduced. The contact-incidence fibre is \(\mathbf P^1\), and the local failure ideal is the exact containment algebra above.

## M124.4 — presentation versus structure

The terminology is changed systematically. parts/08-corank-boundary.tex contains the *projection-rank residual block presentation*. The all-corank *structure theorem* is the residual-colon/associated-graded theorem in parts/09-stratified-nilpotent.tex.

## M124.5 — scope in the headline theorem

The Introduction now states, in order:

1. the polarized reconstruction theorem;
2. the whole-Grassmannian residual-colon/associated-graded theorem;
3. the complete mixed-regular rank-two collision law;
4. the containment theorem;
5. the first decomposable mixed-kernel wall;
6. the separate exact block presentation at every projection rank;
7. the finite étale Torelli-monodromy theorem.

Thus a reader does not have to recover the scope boundary from qualifications distributed later in the paper.

## Verification

Revision 125 carries forward the exact K3 and split-corank-two regression checks and adds a deterministic symbolic regression for:

- a repeated-contact quartic \(u^2(u-v)(u-2v)\);
- the identity \(J=I_H\cap\mathfrak m^3\);
- the identity \(\delta J=\delta I_H\cap\mathfrak m^5\);
- the zero-quartic containment identity \(\delta^2\mathfrak m=(\delta^2)\cap\mathfrak m^5\);
- the decomposable-kernel wall and its length-three quotient.

These certificates remain regression evidence only. The general proofs are the written algebraic arguments in the manuscript.
