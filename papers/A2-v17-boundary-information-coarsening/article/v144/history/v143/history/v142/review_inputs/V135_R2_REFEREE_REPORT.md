# Second independent harsh top-four referee report — A2 revision 135

**Manuscript:** *Intrinsic reconstruction of webs from nonreduced multiplication-failure schemes*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v135-structural-support-proof-2026-09-23  
**Reviewed head:** 003fb13458c8ed11e2973963493a662f31c700c0  
**Source/assembly commit recorded by the manuscript:** 390ae3a73f097fdbdc0a84771fd35e155ad79ed8  
**Controlling v134 report:** reviews/a2-v134-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md at a08b157800c27c0f73f0c5c9a52155265ef4f395  
**Date:** 23 September 2026

## Status and scope

This is an owner-requested, AI-assisted independent external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report or editorial decision.

A separate v135 review branch already existed when this assessment was performed. I therefore did not amend, overwrite, or inherit that branch. This report is deliberately placed on a second review branch based directly on the immutable v135 manuscript head above.

I audited the focused reconstruction article, the v134 response, the new shear-descent proof, the full SO4 exterior-cube character calculation, the contraction-kernel theorem, the exact support table, the secant/tangent exclusion, the intrinsic deepest-normal-cone argument, the residual Cartier-section lemma, the global rank/Fitting-ramification formulation, the source-bound build receipt, and the v135 literature audit. I also checked the most directly relevant exterior/skew-flattening literature independently.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

This recommendation is **not** based on a discovered counterexample to the headline inverse theorem. Revision 135 is mathematically much stronger than revision 134, and the two representation-theoretic proof bottlenecks identified in the previous report have been repaired in a serious way. I did not find a fatal algebraic contradiction in the new contraction/support spine.

The reason for rejection has shifted. The present paper has three remaining problems at the top-four threshold:

1. **the novelty boundary of the central support mechanism is still not established against the closest exterior/skew-flattening literature;**
2. **the closest historically relevant Ballico 1993 source remains unread at theorem level, so the paper itself cannot certify the priority boundary it asks a referee to accept;**
3. **the decisive reconstruction step is an exceptionally low-dimensional representation-theoretic phenomenon, and the manuscript does not yet make a convincing top-four-level case for its conceptual reach beyond this specific four-dimensional web/K3 problem.**

In addition, two functoriality steps in the intrinsic inverse theorem should be written in a coordinate-free bundle/ideal language before publication: the passage from the oriented relative Segre cone to one regular constant projective transformation, and the recovery of the residual degree-twelve ideal by “division by the determinant.”

Thus my assessment is now quite different from an ordinary correctness rejection. The proof spine appears credible; the scholarly positioning, conceptual significance, and two intrinsic descent steps are not yet at the standard required for a general top-four journal.

# 1. Revision 135 genuinely closes the two main v134 proof objections

A harsh report should not recycle objections that have actually been repaired.

## 1.1 The singular contraction-kernel argument is now audit-ready

The new shear-descent lemma is a real mathematical repair.

Let
\[
V=A\oplus B,\qquad B\neq0,
\]
and let \(N\subset \det(V)\otimes\operatorname{Sym}^mV\) be invariant under the \(B\)-scaling torus and the unipotent shears
\[
a+b\longmapsto a+b+L(a),\qquad L\in\operatorname{Hom}(A,B).
\]
The manuscript records the actual torus weight on
\[
\det(V)\otimes\operatorname{Sym}^kA\otimes\operatorname{Sym}^{m-k}B
\]
as
\[
\dim(B)+m-k.
\]
These weights are distinct, so an invariant subspace splits by \(A\)-degree before any differentiation is applied. This removes the filtration ambiguity in v134.

The noncancellation argument is also explicit. Writing
\[
F=\sum_{|\beta|=k}a^\beta f_\beta,
\]
choosing \(\beta\) with \(f_\beta\neq0\), and taking \(\alpha=\beta-e_i\), the coefficient of \(a_i\) in \(\partial_A^\alpha F\) is exactly \(\beta!f_\beta\). No other monomial contributes to that coefficient. Repeated infinitesimal shears give
\[
b^{k-1}\partial_A^\alpha F,
\]
which is nonzero because multiplication by a nonzero \(b\) is injective in the polynomial algebra \(\operatorname{Sym}B\).

In the application to a singular bilinear form \(q\), the shears really do lie in the stabilizer because \(B=\operatorname{rad}(q)\). The determinant factor is correctly tracked: the unipotent shears have determinant one, while the scaling torus contributes the additional \(\dim B\) weight.

Finally, the degree-one piece
\[
\det(V)\otimes A\otimes\operatorname{Sym}^3B
\]
is irreducible for the full \(O(A)\times GL(B)\), including the rank-two orthogonal case, and the manuscript supplies an explicit nonzero value
\[
4\kappa_q(\epsilon\otimes ab^3)
=(bx_2)\wedge(bx_3)\wedge b^2.
\]
The shear lemma then excludes every other positive \(A\)-degree kernel vector.

I regard the previous singular-\(q\) proof objection as closed.

## 1.2 The nondegenerate determinant-character argument is now substantially adequate

The new decomposition
\[
\begin{aligned}
\bigwedge^3\operatorname{Sym}^2V\simeq{}&
[6,0]\oplus[0,6]\oplus[4,4]
\oplus2[4,2]\oplus2[2,4]\\
&\oplus[2,2]\oplus2[2,0]\oplus2[0,2]
\end{aligned}
\]
under \(SL_2\times SL_2\to SO_4\) is the right replacement for the compressed parity argument in v134.

The manuscript derives the decomposition using the skew Cauchy formulas for
\[
T=\operatorname{Sym}^2U\otimes\operatorname{Sym}^2U'
\]
and lists all required one-factor \(SL_2\) decompositions. The dimension check is correct:
\[
84+36=120=\binom{10}{3}.
\]
There is no \([0,0]\) summand. Since the determinant character of \(O_4\) restricts trivially to \(SO_4\), any \(O_4\)-equivariant copy of the determinant line inside the target would produce an \(SO_4\)-fixed vector. None exists.

The harmonic source decomposition
\[
\det V\otimes\operatorname{Sym}^4V
=
(\det V\otimes\mathcal H_4)
\oplus
(\det V\otimes\rho\mathcal H_2)
\oplus
(\det V\otimes\mathbf C\rho^2)
\]
then behaves exactly as required: the scalar determinant line is killed, while explicit coefficients \(2\) and \(2/3\) prove that the other two irreducible restrictions are nonzero and therefore injective.

I do not see a reason to reopen the v134 objection here.

# 2. The exact support theorem and secant/tangent exclusion are internally coherent

The main new mechanism of the paper is now clear enough to audit.

For
\[
j:\det V\otimes\operatorname{Sym}^4V
\longrightarrow
\bigwedge^4\operatorname{Sym}^2V,
\]
the contraction-kernel theorem gives:

- if \(q\) is singular,
  \[
  \ker(\iota_qj)=\det V\otimes\operatorname{Sym}^4(\operatorname{rad}q);
  \]
- if \(q\) is nondegenerate,
  \[
  \ker(\iota_qj)=\det V\otimes\mathbf C(q^{-1})^2.
  \]

Using
\[
s(z)=10-\dim\{q\in(\operatorname{Sym}^2V)^*:\iota_qz=0\},
\]
the exact support table follows:
\[
4,\quad7,\quad9,\quad10,
\]
with support \(9\) also for a four-variable nondegenerate quadratic square.

This part is clean. In particular, a smooth quartic has support \(10\): it is neither a cone nor a nonreduced quadratic square.

The second half of the argument is elementary but decisive. A sum of two decomposable four-vectors has support at most eight, and every vector in the affine tangent space
\[
\bigwedge^3R\wedge W
\]
is supported on at most eight directions. Therefore the Jacobian Schur component of a quartic with at least three essential variables cannot be a secant or tangent direction of the Grassmannian.

Consequently:

- a distinct second decomposable point on the component pencil is impossible;
- a double point is impossible;
- a pure endpoint is impossible;
- a Grassmann line is impossible.

This is exactly the missing global step in earlier revisions. I did not find a direct counterexample to it.

# 3. The scheme-level passage from pointwise exclusion to the full smooth locus is acceptable

The manuscript defines the rank defect by the \(2\times2\) minors of the two-column coefficient matrix of restricted Plücker quadrics. On the reduced open \(G_4^\circ\), every geometric point has rank two by the support theorem. Hence the closed finite-type complement has no geometric points.

Over \(\mathbf C\), a nonempty finite-type scheme has a closed geometric point. Therefore the closed complement is empty as a scheme; there is no hidden nilpotent closed subscheme with empty underlying topological space.

Thus the conclusion
\[
G_4^{\mathrm{rec}}=G_4^\circ
\]
as open subschemes is legitimate.

I do not regard this as a remaining gap.

# 4. The residual involution and Fitting-ramification terminology are materially improved

The new residual Cartier-section lemma works over the actual rank-one determinantal scheme rather than only over geometric points.

On the rank-one chart the restricted Plücker ideal has the form
\[
((b-a)(ca+db)),\qquad (c,d)=\mathcal O_T.
\]
After inverting \(cd(c+d)\), the two factors define disjoint effective Cartier sections
\[
[1:1],\qquad[d:-c].
\]
Because a unimodular linear form cuts a Cartier section over an arbitrary base, the construction survives nonreduced bases and arbitrary base change. The Chinese remainder argument gives the scheme-theoretic disjoint union, and the change of component frames shows that the residual section maps back into the determinantal rank-one scheme. The involution therefore exists as a morphism, not merely as a pointwise exchange.

Likewise, the manuscript now calls
\[
V(\operatorname{Fitt}_0\Omega_{X^\times/Y})
\]
on the quasi-finite part the “Fitting ramification locus of the quasi-finite part” and explicitly disclaims a global finite-flat double-cover interpretation.

These are satisfactory repairs.

# 5. Blocking issue R2-B135.1: the literature audit still misses the closest exterior/skew-flattening formulation

This is the most concrete new scholarly problem I found.

Revision 135 compares its support mechanism with Landsberg–Weyman tensor-product subspace varieties. That comparison is not wrong, but it is not the closest precedent. There is direct literature on **exterior subspace varieties and skew-flattenings in the same ambient exterior power used by the manuscript**.

In particular, J. M. Landsberg and G. Ottaviani, *Equations for secant varieties via vector bundles*, arXiv:1010.1825, §6.1, explicitly introduce for exterior tensors
\[
\operatorname{Sub}_p(\bigwedge^kW)
=
\{[z]\in\mathbf P(\bigwedge^kW):
z\in\bigwedge^kW'\text{ for some }\dim W'=p\}.
\]
They describe this set by the rank/minors of the first skew-flattening and state the standard containment
\[
\sigma_r(\operatorname{Gr}(k,W))
\subset
\operatorname{Sub}_{rk}(\bigwedge^kW).
\]
That is essentially the classical ambient language behind the manuscript’s “exterior support” and the support-eight containment for \(\sigma_2(\operatorname{Gr}(4,W))\).

A second directly relevant formulation appears in John Sheridan, *Divisor Varieties of Symmetric Products*, IMRN 2022, 9830–9863, where the enclosing space of a skew tensor is identified via contraction and the corresponding exterior subspace variety is formulated as a contraction-rank degeneracy locus.

These references do **not** appear, on the material I inspected, to prove the manuscript’s specialized all-ranks kernel theorem for
\[
\iota_q\circ j:
\det V\otimes\operatorname{Sym}^4V
\to
\bigwedge^3\operatorname{Sym}^2V.
\]
Nor do they obviously give the exact support pullbacks \(4,7/8,9\) for this particular Schur embedding. The specialized theorem may therefore still be genuinely new.

But the paper’s present novelty language is too broad unless it makes the following distinction explicitly:

- **classical:** enclosing/exterior-support spaces, their contraction-rank description, skew-flattenings, and the containment of Grassmannian secants in support-\(rk\) subspace varieties;
- **potentially new:** the restriction of that contraction machinery to the specific determinant-twisted quartic Schur summand inside \(\bigwedge^4\operatorname{Sym}^2V\), the exact kernel for every bilinear rank, the resulting support table, and the incidence consequence for the component line.

The revised literature audit should compare theorem-by-theorem against the direct exterior literature, not only against tensor-product subspace varieties.

Until this is done, I would not endorse the manuscript’s present novelty boundary at a top-four venue.

# 6. Blocking issue R2-B135.2: Ballico 1993 remains an unresolved historical source

The manuscript is commendably explicit that this issue remains open:

- the full text has not been obtained;
- historical priority is not certified;
- no anticipation or nonanticipation claim is made.

That honesty is correct, but it does not close the problem.

The paper is:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, **Mathematische Nachrichten** 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

The overlap in vocabulary and historical subject is close enough that a general top-four referee should not be asked to validate the novelty of a “failure-scheme” program while the manuscript itself says the nearest old failure-locus paper remains unread.

I am **not** asserting anticipation. The problem is precisely that the evidence currently supports neither anticipation nor nonanticipation.

Before a top-four resubmission, the paper should obtain the source by a legitimate library route and compare exact theorem statements along at least the six axes already identified by the authors:

1. parameter spaces;
2. reduced locus versus scheme/Fitting structure;
3. multiplication maps or higher-order properties varied;
4. infinitesimal, nilpotent, colon, or normal-cone data;
5. relative/base-change statements;
6. inverse/reconstruction statements.

If the old paper is genuinely remote from the present inverse theorem, the comparison should make that fact easy for a referee to verify.

# 7. Blocking issue R2-B135.3: the top-four significance case is still too dependent on a four-dimensional coincidence

This is the main venue-level issue even if every proof is correct.

The decisive mechanism uses the very special decomposition
\[
\bigwedge^4\operatorname{Sym}^2\mathbf C^4
=
\mathbb S_{(4,3,1,0)}
\oplus
\mathbb S_{(5,1,1,1)},
\]
together with the identification of the \(35\)-dimensional summand as
\[
\det V\otimes\operatorname{Sym}^4V,
\]
the quartic Jacobian/K3 geometry, and the numerical support gap
\[
9\text{ or }10 > 8.
\]

This is beautiful. It is also highly dimension-specific.

A general top-four paper can absolutely be built around an exceptional low-dimensional phenomenon, but then the manuscript has to explain why that phenomenon solves a central problem whose importance is commensurate with the venue. Revision 135 currently does not do enough of that work.

The reader is left with a theorem of the following form:

- a specific Hilbert function \((1,4,6)\);
- a four-dimensional relation web of quadrics;
- a specific nonreduced multiplication-failure scheme;
- a smooth quartic Jacobian;
- one special two-summand plethysm;
- one exact support gap;
- one inverse reconstruction consequence.

What is not yet clear is whether the theorem reveals a **general mechanism** or an **isolated representation-theoretic accident**.

For a fresh top-four submission I would require one of two things:

### Option A: a genuine conceptual extension

Give a theorem or program showing that the method survives beyond the exact \(4\)-by-\(4\) coincidence. It need not reproduce the same support numbers, but it should identify a structural criterion on Schur components, contraction kernels, or failure schemes that implies reconstruction in a family of inverse problems.

### Option B: a much stronger significance argument for the exceptional case itself

If dimension four is intrinsically exceptional, explain why the web/K3 reconstruction problem is important enough that solving precisely this exceptional case is a major theorem. This would require a sharper connection to established moduli/inverse problems, not merely to the internal eleven-paper pipeline.

At present the manuscript demonstrates technical strength more convincingly than field-level significance.

That distinction matters at Annals/Inventiones/JAMS/Acta level.

# 8. Serious issue R2-S135.1: the common-projective-transformation step should be made intrinsically bundle-theoretic

I did not find a counterexample to the common-\(g\) mechanism, and earlier reports have already accepted its basic idea. Nevertheless, it remains the most delicate functorial bridge in the inverse theorem.

The relative rank-one cone over
\[
\Sigma_0(R)=\operatorname{Gr}(4,S_R)
\]
has two ruling families. The manuscript distinguishes them by projective triviality and thereby recovers the \(V\)-ruling. An abstract scheme isomorphism then induces fibrewise projective transformations of that trivial ruling, and the proof invokes projectivity of the base plus affineness of \(PGL(V)\) to conclude that the transformation is constant.

The missing sentence is the one that upgrades a fibrewise family to a **regular morphism**
\[
\Sigma_0(R)\longrightarrow PGL(V).
\]

For publication, I recommend isolating a lemma on isomorphisms of the oriented relative Segre cone. It should:

1. identify the two ruling parameter spaces over the induced base isomorphism;
2. show that preservation of the projectively trivial ruling gives a regular automorphism of the trivial \(\mathbf P^3\)-bundle;
3. account for the usual possibility of twisting a vector-bundle lift by a line bundle on the base;
4. show that this twist disappears projectively and does not change the two recovered left Schur lines;
5. only then use the fact that every morphism from the connected projective Grassmannian to affine \(PGL_4\) is constant.

I regard this as a serious auditability issue, not evidence of falsehood.

# 9. Serious issue R2-S135.2: “division by the determinant” should be replaced by an intrinsic residual-ideal construction

The fibre calculation says
\[
I_{16}=d\,(J_R)_{12},
\qquad d=\det T.
\]
In a chosen polynomial ring this is perfectly clear, and multiplication by \(d\) is injective.

But the inverse theorem is stated intrinsically under arbitrary abstract scheme isomorphisms. Globally, \(d\) is not a preferred scalar polynomial; it is a local generator of the determinant hypersurface ideal, transforming by a unit/line-bundle factor.

The paper should therefore recover the residual degree-twelve data by an invariant construction, for example:

- an ideal quotient by the reduced determinant ideal;
- or a line-bundle-twisted multiplication isomorphism of graded pieces.

Schematically, the relevant object should look like the degree-twelve part of
\[
(I_{\mathscr C_R}:I_{\mathscr C_{R,\mathrm{red}}}),
\]
with the exact grading and line-bundle twists stated correctly.

This would turn the phrase “divide by the determinant equation” into a functorial operation that an abstract isomorphism visibly preserves.

Again, this looks repairable. But because the resulting degree-twelve space is the input to the universal Schur readout, the invariant formulation belongs in the principal proof.

# 10. The new support-pullback proposition is useful, but the paper must keep its reduced/scheme-theoretic boundary precise

The proposition identifying the reduced inverse images
\[
j^{-1}\operatorname{Sub}^{\wedge}_4,\qquad
j^{-1}\operatorname{Sub}^{\wedge}_{7,8},\qquad
j^{-1}\operatorname{Sub}^{\wedge}_9
\]
is a useful geometric packaging of the support table.

The manuscript is careful to say these are equalities of **reduced closed subvarieties** and does not claim that the pulled-back skew-flattening minors generate radical ideals. That caution should remain.

Once the direct exterior-subspace literature is cited, the reader will naturally ask a stronger scheme-theoretic question: what are the actual pullback ideals and multiplicities? The present inverse theorem does not need that answer. The paper should resist upgrading the reduced statement unless it is actually proved.

This is not a defect; it is an important scope boundary.

# 11. Reproducibility and evidence

The v135 evidence package is unusually disciplined.

The recorded build receipt states:

- focused article: 24 pages;
- supplement: 66 pages;
- complete archival manuscript: 86 pages;
- all listed LaTeX reference/citation/duplicate-label checks pass;
- ten exact scripts were executed;
- the new \(SO_4\) character, shear coefficient, dual-number CRT, and support-table checks are recorded;
- the accepted universal-readout and common-\(g\) source files are preserved byte-identically;
- the receipt explicitly lists the structural statements **not** machine-certified.

This is the correct relationship between computation and proof.

I did not independently reproduce the full build environment through a separate CI run during this referee pass. The branch head is an artifact-publication commit whose message contains “[skip ci]”, and the available commit-status wrapper did not expose an independent status check for that head. Therefore this report treats the source-bound receipt as manuscript evidence, not as an external certification.

That limitation does not affect the mathematical objections above.

# 12. Technical comments

1. The notation \(q\in(\operatorname{Sym}^2V)^*\) and \(q^{-1}\in\operatorname{Sym}^2V\) is standard once nondegeneracy is fixed, but one coordinate-free sentence identifying \(q:V\to V^*\) and \(q^{-1}:V^*\to V\) would make the determinant twists easier to track.

2. In the singular proof, the rank-two statement that the standard \(O_2\)-representation is irreducible over \(\mathbf C\) is correct for the full disconnected orthogonal group; it would help to state explicitly that the reflection interchanges the two one-dimensional \(SO_2\)-weight spaces.

3. The support-eight tangent bound is classical and should be advertised as such in the main article itself, not only in the literature section.

4. The phrase “three essential variables suffice” is mathematically correct for the support exclusion, but the headline smooth-quartic theorem has four essential variables. A short sentence distinguishing the stronger algebraic support theorem from the geometric smooth application would improve exposition.

5. The 86-page combined manuscript should remain an archival object. For an actual journal submission, the 24-page reconstruction article should be the primary file; otherwise the editorial repair achieved in v135 is largely undone.

6. The exact support table is stronger and cleaner than many of the retained ambient-boundary calculations. It should be visually promoted as the central theorem of the proof, rather than presented as one more technical proposition among a long historical chain.

# 13. Required work before another top-four submission

I would require the following before recommending another general top-four review:

1. **Direct exterior literature audit.** Compare the support theorem against the skew-flattening/exterior-subspace literature, in particular Landsberg–Ottaviani §6.1 and later enclosing-space formulations. State exactly what remains new.

2. **Ballico 1993 theorem-level comparison.** Obtain and read the complete article; fill the six already-defined comparison axes.

3. **Conceptual significance.** Either provide a structural extension beyond the \(4\)-dimensional two-summand coincidence or give a substantially stronger field-level argument for why this exceptional reconstruction problem is itself top-four significant.

4. **Intrinsic common-\(g\) lemma.** Make the regularity/descent from the oriented relative Segre ruling to one constant \(PGL(V)\)-element fully bundle-theoretic.

5. **Intrinsic residual ideal.** Replace informal determinant division by an invariant ideal quotient or line-bundle-twisted graded construction.

6. **Keep computation subordinate.** Preserve the exact checks, but do not treat them as replacements for items 4–5.

# 14. Final assessment

Revision 135 is the first version in this sequence for which I regard the central smooth-locus reconstruction theorem as a serious, internally coherent mathematical result rather than a theorem still visibly blocked by an unresolved representation-theoretic step.

That is substantial progress.

I nevertheless recommend **rejection at a general top-four journal in the present form**. The remaining reason is not that the new shear or \(SO_4\) arguments obviously fail; they appear to work. The reason is that the manuscript has not yet established the exact scholarly boundary and conceptual scale of the theorem it now proves, and two intrinsic functoriality transitions should still be made formally transparent.

If the direct exterior literature and Ballico comparisons confirm that the specialized kernel/support theorem is genuinely new, and if the authors can explain why the four-dimensional reconstruction phenomenon has significance beyond an isolated plethysm accident, then the focused 24-page article would deserve a fresh external assessment on its merits.

Until then, I would not recommend acceptance, and I would not treat the remaining work as a minor revision.
