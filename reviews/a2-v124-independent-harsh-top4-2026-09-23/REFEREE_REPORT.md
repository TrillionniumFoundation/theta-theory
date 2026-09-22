# Independent harsh top-four referee report — A2 revision 124

**Manuscript:** *Intrinsic nilpotent depth, Reye geometry, and higher-corank structure in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v124-intrinsic-nilpotent-reye-boundary-2026-09-23  
**Reviewed branch head:** 27cac99489fc8537f4e6636599059fd6f5d1a453  
**Mathematical source commit:** d238a6716e826cc8ea156a1a2d4a9cf0566f09fa  
**Parent revision:** revision/a2-v123-polarized-k3-corank-two-2026-09-23  
**Controlling previous report:** reviews/a2-v123-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md  
**Principal referee object:** papers/A2-v17-boundary-information-coarsening/article/v124/geometry.pdf, 24 pages  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report.

I reviewed the revision-124 mathematical source, not merely the response letter, issue matrix, build receipt, or generated PDF. In particular I checked the new nilpotent-depth construction, the inherited full Fitting theorem from revision 123, the claimed all-corank block theorem, the root-free rank-two residual normal form, the collision theorem, the global degree-four contact cover and discriminant calculation, the revised Reye/Enriques moduli discussion, the response to the revision-123 report, and the literature audit. I also compared the new all-corank statement directly with the inherited proposition from revision 123 from which it is derived.

I independently spot-checked the external historical claims most relevant to the new framing. Arrondo–Sols do state that the Hilbert scheme of Reye congruences is smooth of dimension 24 and rational, so the manuscript is right to stop presenting 24−15=9 as a novelty signal. The modern theorem of Martin–Mezzedimi–Veniani confirms the classical Reye status of nodal Enriques surfaces. The Wiley record for Ballico 1993 confirms the bibliographic item, but the complete theorem text was not available in the present review environment; I therefore agree with the manuscript that no anticipation or non-anticipation conclusion should be inferred from metadata alone.

The standard below is the standard of an exceptionally selective general mathematics journal. Correctness is necessary but not sufficient. The paper must isolate a genuinely new theorem after the classical geometry is removed, prove it in its natural scope, and close the priority boundary well enough that the journal is not being asked to certify novelty against a known nearest predecessor that neither author nor referee has read at theorem level.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

Revision 124 is a serious revision, and several objections from the revision-123 report have been materially improved. In particular, I no longer regard the classical nine-dimensional Reye/Enriques issue, the lack of any unifying language, or the absence of a global contact cover as unchanged defects. The authors have made real progress.

However, the revision does not yet deliver the theorem suggested by its new title and response matrix.

The central problem is now very precise:

**the manuscript promotes an exact block rewriting of the already-known whole-Grassmannian Fitting formula into an “all-corank structural replacement,” but it does not classify the higher-corank boundary outside the mixed-regular rank-two locus.**

The new functorial schemes
\[
Z_j=V(\operatorname{Ann}(N^j))
\]
are intrinsic and useful, but the paper computes them only on different open strata: \(Z_1\) on the smooth-reduction/corank-one locus and \(Z_2\) on the mixed-regular corank-two locus. It does not give a global theorem describing the nested filtration through the rank-two boundary, the mixed-rank-drop locus, the rank-one-kernel locus, the containment locus \(h_H\equiv0\), projection corank three, or projection corank four. The difficult geometry identified by the previous referee has therefore not been replaced by a global structure theorem; it has been surrounded by a correct universal presentation formula.

There is also a concrete overstatement in the globalization paragraph. The complement of the contact discriminant controls the splitting of the four roots of the binary quartic. It does **not** by itself impose the mixed-regular hypotheses required for the \(P_i\) to be the primary branches occurring in the revision-123 decomposition. The primary interpretation is valid on the intersection of the simple-contact locus with the mixed-regular locus, not on the whole discriminant complement. Similarly, the fact that the ideal \(\mathfrak m^5\) glues as an ordinary fifth power does not prove that it remains a primary component of the failure scheme outside the open on which the primary decomposition was established.

Finally, the nearest historical failure-locus source, Ballico 1993, remains unread at theorem level. The manuscript handles this limitation honestly, but honesty about an unresolved priority boundary does not close that boundary for a top-four publication decision.

My overall view is therefore:

**revision 124 has a credible and mathematically interesting core, but the present “all-corank / global nilpotent-depth” formulation overstates how much of the singular boundary has actually been classified. The paper remains potentially strong for a specialist algebraic-geometry or commutative-algebra venue; it is not yet at the structural completeness and priority threshold I would require for Annals/Inventiones/JAMS/Acta.**

# 1. What revision 124 genuinely improves

A new report should not recycle solved objections.

## 1.1 The manuscript now treats nine-dimensional Reye geometry correctly as classical

This is the cleanest improvement.

Revision 123 proved a 24-dimensional embedded-quartic image and then obtained nine dimensions after quotienting projective coordinates. That argument was mathematically valid, but the previous report objected that the number nine itself sits inside classical Reye/Enriques geometry.

Revision 124 now says exactly that.

The new Section 9 separates:

1. the classical 24-dimensional parameter space of Reye congruences;
2. the 15-dimensional projective-coordinate orbit;
3. the resulting nine-dimensional Reye/nodal-Enriques moduli locus;
4. the exact 25-by-25 determinant used only to show that the specific source-Jacobian quartic map occurring in this multiplication problem sees the full tangent space.

This is the correct conceptual hierarchy.

I independently checked the Arrondo–Sols source. Their discussion of the Reye congruence states that its Hilbert scheme is smooth of dimension 24 and rational. Thus the revised manuscript is right to say that \(24-15=9\) is classical geometry rather than a new dimension phenomenon.

I would not repeat the revision-123 objection in its previous form.

## 1.2 The nilpotent-depth construction is a legitimate intrinsic organizing device

For a noetherian scheme \(Z\) with nilradical \(N_Z\), the construction
\[
Z_j(Z)=V(\operatorname{Ann}(N_Z^j))
\]
is canonical under abstract scheme isomorphism and commutes with localization.

That fact is elementary, and the paper does not claim otherwise.

What is useful here is its application to the two local models already present in the manuscript.

On the smooth-reduction locus, the local equation
\[
t(t,f)
\]
has nilradical generated by \(t\), and
\[
\operatorname{Ann}(t)=(t,f).
\]
Thus \(Z_1\) recovers the embedded ramification support \(E_R\).

On the mixed-regular rank-two locus, the new root-free argument gives a local ring with nilradical generated by \(\delta\), exact nilpotency index three, and
\[
\operatorname{Ann}(\delta^2)=\mathfrak m.
\]
Thus \(Z_2\) recovers the rank-two Schubert support there.

This is a real conceptual improvement over merely placing two unrelated normal forms in adjacent sections.

## 1.3 The simple-root condition has been removed from the depth-two statement

The root-free lemma is a worthwhile extension of the revision-123 calculation.

On the mixed-regular locus the residual ideal is written
\[
J=\delta\mathfrak m+(g_0,\dots,g_4),
\]
and modulo the rank-one cone \((\delta)\), the degree-four generators span
\[
h_H(u)\operatorname{Sym}^4(\mathbf C_v^2).
\]

The proof does not factor \(h_H\). Therefore repeated roots do not affect the degree argument giving
\[
N^3=0,\qquad N^2\ne0,\qquad \operatorname{Ann}(N^2)=\mathfrak m.
\]

This directly improves the revision-123 theorem, which required four distinct contacts in order to split the residual contact ideal into four primary branches.

I do not see a contradiction in the new collision-depth proof.

## 1.4 The global contact incidence is a natural and useful geometric object

The construction
\[
\mathcal R_R=
\{(H,[\alpha])\in\operatorname{Gr}(2,V)\times Y_R:
 H\subset\ker\alpha\}
\]
is the correct global object behind the four local contact roots.

The projection to \(Y_R\) has fibre \(\operatorname{Gr}(2,\ker\alpha)\simeq\mathbf P^2\), so the total incidence is smooth and irreducible.

Over the locus on which the restricted quartic is not identically zero, the projection to \(\operatorname{Gr}(2,V)\) is a degree-four finite flat cover. The binary-quartic discriminant has determinant weight 12, giving a discriminant section of \((\det Q)^{12}\) and divisor class \(12H\) when nonzero.

Off the discriminant, the cover is finite étale, and irreducibility gives transitive monodromy.

This is an appropriate globalization of the **roots** of the contact quartic.

The qualification in the final sentence is important: it globalizes the roots/contact sheets. It does not automatically globalize every primary component of the failure ideal.

## 1.5 The journal object is now much cleaner

Revision 124 has one principal article, 24 pages, with the older revision included only as source for unchanged proof blocks.

For refereeing purposes this is substantially cleaner than asking the reader to decide which of several archival manuscripts is authoritative.

The build receipt also makes sensible distinctions:

- exact K3 witness passed;
- exact corank-two regression passed;
- general proof machine certification is false;
- priority certification is false;
- Ballico 1993 complete-text-read is false.

These flags are appropriately conservative.

# 2. Correctness audit of the new algebra

My negative recommendation is not based on finding the new central local calculation false.

## 2.1 The all-corank block identity is correct

The inherited full Fitting theorem says
\[
I_{\widehat D}=(\det M)I_6(\gamma_R\operatorname{Sym}^2M).
\]

At a point of projection rank \(r\), Schur reduction gives
\[
M=\operatorname{diag}(I_H,T).
\]
With
\[
\operatorname{Sym}^2V=
\operatorname{Sym}^2H\oplus(H\otimes W)\oplus\operatorname{Sym}^2W,
\]
the induced map is
\[
I_{\operatorname{Sym}^2H},\qquad
1_H\otimes T,\qquad
\operatorname{Sym}^2T.
\]

Therefore
\[
I_{\widehat D_R}
=
(\det T)
I_6\!\left[
 A_H,\,
 B_H(1_H\otimes T),\,
 C_H\operatorname{Sym}^2T
\right].
\]

I agree with this identity.

The problem is not correctness. The problem is what theorem-level work the identity is being asked to do. I return to that below.

## 2.2 The root-free rank-two normal form is coherent

Under mixed regularity, the revision-123 Gaussian elimination reduces to
\[
I_{\widehat D_R}=\delta J,
\qquad
J=I_3[L(T),CT^{(2)}].
\]

On the rank-one cone \(T=uv^t\), the linear columns occur in two scalar pairs, while the quadratic columns are scalar multiples of one vector \(C(u^2)\).

Hence:

- the minors of the linear block generate \(\delta\mathfrak m\);
- the minors with one column from each linear pair and one quadratic column restrict to the quartic contact form times the five degree-four monomials in \(v\);
- minors with at least two quadratic columns vanish on the rank-one cone and are divisible by \(\delta\).

This supports
\[
J=\delta\mathfrak m+(g_0,\dots,g_4)
\]
without factoring the contact quartic.

The degree bookkeeping used in the collision theorem is also coherent.

## 2.3 The annihilator computation at rank two is credible

Because \(\delta\in\mathfrak m^2\) and \(\delta\mathfrak m\subset J\),
\[
\delta^2\in J,\qquad \delta^3\in\delta J.
\]
Since \(J\) has no transverse degree-two term,
\[
\delta\notin J,
\]
so
\[
\delta^2\notin\delta J.
\]

Thus the local nilradical has exact index three.

For the square,
\[
(\delta J:\delta^2)=(J:\delta).
\]
The inclusion
\[
\mathfrak m\subset(J:\delta)
\]
is immediate from \(\delta\mathfrak m\subset J\). Conversely, the transverse grading excludes a degree-zero coefficient in an element \(r\) satisfying \(r\delta\in J\), so
\[
(J:\delta)=\mathfrak m.
\]

This yields the claimed annihilator support.

I do not see a hidden use of distinct roots in this argument.

## 2.4 The discriminant class is plausible and correctly separated from the exact arithmetic witness

For a binary quartic, the discriminant is degree six in the coefficients and has determinant weight 12. Therefore a quartic section of \(\operatorname{Sym}^4Q\) has discriminant in \((\det Q)^{12}\).

Thus the global discriminant divisor has Plücker class \(12H\), assuming the section is not identically zero.

This is a useful geometric statement and should remain.

# 3. Decisive blocker E124.1 — the “all-corank theorem” is a repackaging, not an all-corank structure theorem

This is the main reason I do not regard the revision-123 higher-corank objection as closed.

The new Theorem 8.1 is presented as the global structural replacement requested by the previous report. But its proof is only substitution into a theorem already proved in revision 123.

Indeed revision 123 already had the whole-Grassmannian identity
\[
I_{\widehat D}
=
(\det M)I_6(\gamma\operatorname{Sym}^2M),
\]
and its proof already says that near a point of projection rank \(r\), an invertible \(r\)-minor reduces \(M\) to
\[
\operatorname{diag}(I_r,T).
\]

Revision 124 decomposes \(\gamma\) according to
\[
\operatorname{Sym}^2H\oplus(H\otimes W)\oplus\operatorname{Sym}^2W
\]
and rewrites the same ideal as
\[
(\det T)I_6[A_H,B_H(1\otimes T),C_H\operatorname{Sym}^2T].
\]

That is correct, but it does not determine:

- the radical of the residual factor on the exceptional rank-two locus;
- associated primes when \(A_H\) loses injectivity;
- associated primes when the mixed map loses surjectivity;
- the case in which the mixed kernel has rank one;
- the nilpotency indices on those loci;
- the containment locus \(h_H\equiv0\);
- projection corank three;
- projection corank four;
- specialization and collision of embedded components across these strata.

In other words, the difficult question has not been solved; it has been restated in a uniform matrix.

A universal presentation is valuable. It is not the same thing as a structure theorem for its degenerations.

This distinction matters because the title now advertises “higher-corank structure,” the abstract says the second stage is governed by an exact presentation valid at every rank-two point, and the issue matrix records E123.3 as “global-structural-replacement-proved.”

I do not accept that status.

### What would close this blocker

A top-four revision needs at least one of the following.

**Option A: classify the remaining rank-two boundary.**  
Stratify by the ranks of \(A_H\), \(\overline B_H\), and the tensor rank of \(\ker\overline B_H\), and determine the radicals, associated primes, nilpotency indices, and collision laws on each stratum.

**Option B: continue through all projection coranks in dimension four.**  
Give an intrinsic stratified description of the failure scheme for ranks three, two, one, and zero, not merely the same maximal-minor formula.

**Option C: prove a genuinely global replacement theorem.**  
For example, identify the associated graded algebra of the nilradical filtration, a Rees algebra, a normal cone, or a canonical filtration whose graded pieces are vector bundles/sheaves on explicitly described Schubert/contact strata and whose specialization theorem controls every boundary.

The current Theorem 8.1 does none of these.

# 4. Decisive blocker E124.2 — the nilpotent-depth “unification” is only partially global

The construction
\[
Z_j=V(\operatorname{Ann}(N^j))
\]
is global and functorial.

The **computation** of that construction is not global.

Revision 124 proves:

- on the smooth locus of the reduction, \(Z_1=E_R\);
- on the mixed-regular rank-two locus, \(Z_2=\Sigma_R\).

These are good local statements, but they occur on different strata.

For any nilpotent ideal,
\[
N^{j+1}\subset N^j
\quad\Longrightarrow\quad
\operatorname{Ann}(N^j)\subset\operatorname{Ann}(N^{j+1}),
\]
so the closed schemes satisfy
\[
Z_{j+1}\subset Z_j.
\]

A genuinely global depth theorem should exploit this nesting.

The manuscript does not tell the reader:

1. what \(Z_1\) is in a neighborhood of a mixed-regular rank-two point;
2. how the closure of the corank-one embedded support meets the rank-two stratum;
3. what \(Z_2\) does on the mixed-rank-drop or rank-one-kernel boundary;
4. whether additional nonzero powers appear at deeper projection corank;
5. whether the associated graded pieces of \(N\) are flat along any natural stratification;
6. whether the polarization line on \(Z_1\) extends or degenerates in a controlled way across rank two;
7. whether the contact cover is literally the normalization, projectivization, or another intrinsic construction from one of the graded pieces.

Without these compatibility statements, the phrase “consecutive functorial stages of one nonreduced multiplication invariant” is true only in a weak formal sense: both objects are extracted from powers of the same nilradical.

That is an elegant organization of known local calculations. It is not yet the global mechanism that the paper advertises.

### Required strengthening

The next revision should compute \(Z_1\) and \(Z_2\) **simultaneously on a neighborhood crossing the corank-one/corank-two boundary**, and then formulate the result without reference to a chosen rank chart.

A particularly convincing theorem would describe
\[
\operatorname{gr}_N\mathcal O_{\widehat D}
=
\bigoplus_j N^j/N^{j+1}
\]
on a canonical stratification and identify the geometric meaning of each nonzero graded piece.

That would turn the present organizing language into a genuine global theorem.

# 5. Decisive issue E124.3 — the global contact cover is correct, but its primary-component interpretation is overstated

The contact cover itself is a good addition.

The problematic sentence is the assertion that the complement of the discriminant is “exactly the global locus” on which the four local ideals \(P_i\) from the revision-123 primary decomposition arise by étale splitting.

This conflates two independent conditions.

The revision-123 \(P_i\)-primary decomposition requires an **admissible pair**, namely:

- \(A_H\) injective;
- the mixed map \(\overline B_H\) surjective;
- one-dimensional mixed kernel of tensor rank two;
- four distinct contact roots.

Revision 124 removes only the last condition when proving the annihilator theorem.

The global discriminant detects only the last condition.

Therefore
\[
G\setminus V(\operatorname{Disc}(h_R))
\]
is not, by itself, the locus on which the \(P_i\) occur as the four primary branches of the failure ideal. The correct locus is the simple-contact part of the **mixed-regular locus**.

The contact sheets themselves exist on the discriminant complement. Their interpretation as the \(P_i\)-primary components of the residual Fitting scheme requires the additional rank hypotheses.

This is not merely stylistic. It is exactly the distinction between globalizing the roots of a quartic and globalizing the primary decomposition of a different scheme.

### A second overstatement: the \(\mathfrak m^5\) component

The manuscript says that the fifth-power component also globalizes because \(\mathfrak m^5\) is the fifth ordinary power of the rank-two Schubert ideal.

The ideal sheaf
\[
I_{\Sigma}^5
\]
certainly globalizes.

What has been proved as a **primary component of the failure ideal** is
\[
\mathfrak m^5
\]
on the admissible/simple-contact open of the revision-123 decomposition.

Across repeated-root collisions, the new theorem proves that \(\mathfrak m\) remains an associated prime, because \(\operatorname{Ann}(N^2)=\mathfrak m\). It does **not** prove that the \(\mathfrak m\)-primary component remains exactly \(\mathfrak m^5\).

Those are different statements.

The paper should either prove that the \(\mathfrak m\)-primary component stays \(I_\Sigma^5\) throughout the mixed-regular collision boundary, or restrict the “fifth-power component glues globally” statement to the open where the primary decomposition is known.

### A third precision point: branch divisor versus discriminant divisor

Over \(G_R^{\mathrm{fin}}\), where the quartic restriction is not identically zero, the degree-four map is finite flat and the discriminant detects its branch locus.

On the separate containment locus \(h_H\equiv0\), the map is not finite.

Thus the globally defined section of \((\det Q)^{12}\) has a well-defined discriminant divisor of class \(12H\), but it is cleaner to call it the **global discriminant divisor**, reserving “branch divisor” for the finite-flat locus.

These corrections are straightforward, but they should be made before publication.

# 6. Decisive blocker E124.4 — Ballico 1993 remains a priority boundary

The manuscript deserves credit for handling this honestly.

It does not claim that Ballico 1993 fails to anticipate the current theorem. It records the access limitation and compares instead with Ballico 1996, whose theorem text was inspected.

That is good scholarly practice.

It does not, however, solve the top-four priority problem.

The bibliographic source is:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, *Mathematische Nachrichten* **163** (1993), 5–13, DOI 10.1002/mana.19931630102.

The title and historical line are close enough to the subject of the present paper that a journal claiming exceptional general significance should not leave the theorem-level comparison unresolved.

The 1996 continuation is useful, but it cannot logically substitute for the 1993 paper if the latter is the closer predecessor.

### Required action

Obtain the complete 1993 article through a research library, author archive, interlibrary loan, MathSciNet-linked library access, or direct author contact and provide a theorem-by-theorem comparison.

At minimum the comparison should cover:

- what “failure locus” means scheme-theoretically in Ballico;
- the parameter Grassmannian;
- the multiplication/evaluation map;
- higher-order conditions;
- whether nonreduced or embedded scheme structure is retained;
- whether Fitting ideals occur;
- whether local multiplicities or nilpotent filtrations are studied;
- whether any reconstruction of geometric data from the failure object appears;
- the relation between moving projective sections and the present cube-zero algebra family.

Until then I would not certify the broad historical priority of the failure-scheme portion for a top-four journal.

# 7. Major issue M124.1 — the finite Torelli packet is localized rhetorically, not classified mathematically

Revision 124 gives a better geometric interpretation of the finite ambiguity.

The polarized K3 is recovered from the failure scheme. A compatible relation system also gives an involution and an Enriques/Reye structure. The Reye bundle has classical rigidity. The contact cover is determined by the recovered quartic.

All of that is useful.

But the theorem still says only:

\[
\text{general polarized K3 point}
\quad\leadsto\quad
\text{finitely many projective classes of }R.
\]

The paper does not determine:

- the generic degree;
- generic injectivity or noninjectivity;
- the monodromy group of the finite fibre;
- which Enriques involutions on the polarized K3 occur;
- whether distinct compatible involutions can produce isomorphic failure schemes;
- the exceptional locus where the fibre degree jumps;
- whether deeper nilpotent strata separate the remaining fibre.

The statement that the remaining packet is “concentrated” in finite choices of compatible Reye/Enriques data is an interpretation of the already-proved finiteness, not a classification theorem.

For a specialist paper, generic finiteness may be enough.

For a top-four theorem advertised as intrinsic reconstruction, I would want the inverse problem pushed materially further.

# 8. Major issue M124.2 — the moduli theorem is better framed, but the deformation theory remains thin

I withdraw the strongest version of the revision-123 criticism that the number nine was being explained only by one large determinant.

Revision 124 now correctly supplies the classical 24-dimensional Reye parameter space and 15-dimensional projective orbit as the conceptual reason for nine.

However, the proposition
\[
T_{[R]}\mathcal M_{\mathrm{Reye}}
\simeq
T_R\operatorname{Gr}(4,\operatorname{Sym}^2V)/\mathfrak{pgl}(V)
\]
still deserves a more explicit bridge from the source quoted to the exact web parameter used in this paper.

Arrondo–Sols describe the Hilbert scheme of Reye congruences as an open Grassmannian-type parameter and show dimension 24. The present article should spell out the identification between that parameter, the four-dimensional relation space \(R\subset\operatorname{Sym}^2V\), and the Hilbert point of the Reye congruence, including the finite stabilizer statement used in passing to the quotient.

This is likely routine for experts in the classical theory. At top-four level it should not be left as a sentence that asks the reader to identify the parameter spaces.

A stronger version would identify the tangent map cohomologically or via the period/lattice description of the K3/Enriques pair.

The exact 25-by-25 determinant should then remain what revision 124 now says it is: a useful arithmetic witness, not the conceptual theorem.

# 9. Major issue M124.3 — the containment locus \(h_H\equiv0\) is not a collision type and deserves separate treatment

The manuscript correctly lists the five partitions
\[
1111,\quad 211,\quad 22,\quad 31,\quad 4
\]
for a nonzero binary quartic, and then mentions separately the containment locus \(h_H\equiv0\).

This separate case is geometrically important.

If \(h_H\equiv0\), the line of hyperplanes containing \(H\) lies in the quartic \(Y_R\). The contact cover is no longer finite over \(H\).

The root-free depth-two algebra may still give the annihilator identity under mixed regularity, but the geometric interpretation by four contact points has disappeared.

The paper should therefore say explicitly:

- whether \(h_H\equiv0\) can occur on the mixed-regular locus;
- the dimension/codimension of the containment locus for a general \(R\);
- whether a smooth quartic in the specific Reye family contains such lines generically or only on a proper sublocus;
- what becomes of the contact-cover interpretation there;
- whether the local failure scheme acquires additional structure not seen by the simple discriminant stratification.

Treating \(h_H\equiv0\) as a parenthetical extra case leaves the most singular contact degeneration conceptually unfinished.

# 10. Major issue M124.4 — the manuscript should distinguish “presentation at every corank” from “structure at every corank”

Several places use language stronger than what has been proved.

The exact block formula is valid at every projection rank.

The **normal forms, associated-prime calculations, and nilpotent-depth interpretation are not**.

I recommend a systematic terminology change:

- “all-corank presentation theorem” for the block Fitting identity;
- “mixed-regular rank-two structure theorem” for the root-free depth result;
- “simple-contact primary decomposition” for the étale-local \(P_i\) formula.

Do not use “all-corank structure” as an umbrella unless the associated scheme structure on the remaining coranks is actually determined.

This is not cosmetic. It is the central scope boundary of the paper.

# 11. Major issue M124.5 — the current global depth theorem should display the missing loci in its statement

Theorem 1.2 is written so that a fast reader can come away with the impression that all higher-corank structure is controlled.

A more honest statement would explicitly divide the result into:

- corank one: complete intrinsic normal form and polarized reconstruction;
- corank two, mixed regular: complete depth-two statement, including repeated-root collisions;
- corank two, non-mixed-regular: only the exact residual block presentation is known;
- corank at least three: only the exact residual block presentation is known.

This would make the current theorem correct in both letter and emphasis.

At present the qualifications are present, but they are distributed across the text and response letter rather than built into the headline.

# 12. Computational evidence

The exact computations remain useful and appropriately limited.

The build receipt records that:

- the K3 witness passes;
- the corank-two regression passes;
- there are no undefined reference diagnostics;
- general proof-machine certification is false;
- priority certification is false.

This is the correct posture.

I would retain the exact computations because they are effective regression tests for a paper containing large explicit matrices.

I would not add more finite certificates as the main response to this report. The remaining issues are structural, not numerical.

# 13. What I would require for top-four reconsideration

A credible next revision should not be another layer of terminology around the same Fitting formula.

It should contain a genuinely stronger mathematical theorem.

The minimum package I would want is:

### E124.1 — replace the formal all-corank rewrite by actual higher-corank structure

Classify at least the entire projection-corank-two boundary, including mixed-rank drop and rank-one mixed kernel, with radicals, associated primes, nilpotency indices, and specialization laws.

Preferably continue to coranks three and four.

### E124.2 — compute the nilpotent-depth filtration across strata, not one power on one stratum at a time

Describe \(Z_1\), \(Z_2\), and any deeper nonzero stages on a neighborhood that crosses the rank-one/rank-two projection boundary.

Identify the associated graded pieces or an equivalent global Rees/normal-cone object.

### E124.3 — correct the contact-cover globalization claims

Restrict the \(P_i\)-primary interpretation to the mixed-regular simple-contact locus, or prove the missing rank statements globally.

Prove separately whether the \(\mathfrak m\)-primary component remains exactly \(I_\Sigma^5\) across contact collisions.

Treat \(h_H\equiv0\) as a distinct nonfinite geometry.

### E124.4 — close the Ballico 1993 source

Read the complete article and add the theorem-level comparison.

### E124.5 — advance the inverse problem

Compute the generic degree of the web-to-polarized-K3 map, prove generic injectivity, or give a precise finite-fibre/monodromy theorem.

### E124.6 — isolate the theorem that remains exceptional after all classical geometry is subtracted

The paper should be able to state in one paragraph, without invoking the classical nine-dimensional family, exact certificates, or future higher-corank work, what theorem is new enough and broad enough to justify a general top-four venue.

At present that theorem has not yet emerged in its natural final form.

# 14. Final assessment

Revision 124 is mathematically better than revision 123.

The authors correctly stopped using the nine-dimensional Reye locus as a novelty signal. They added a useful intrinsic nilpotent-depth language, removed the simple-root restriction from the depth-two annihilator theorem, and constructed a natural global contact cover with a clean discriminant calculation.

I also do not find evidence that the new root-free local algebra is simply wrong.

But the main top-four obstacle has shifted rather than disappeared.

The paper now calls a universal block presentation an all-corank structural theorem, while the non-generic higher-corank scheme structure remains unclassified. The global nilpotent filtration is defined everywhere but understood only on selected strata. The contact cover globalizes roots more completely than it globalizes primary components. The finite Torelli packet remains finite but uncomputed. And the nearest 1993 failure-locus predecessor remains unread.

These are not reasons to dismiss the project. They are reasons not to certify the present version as an exceptional general-journal theorem.

**Recommendation: reject in the present form at a general top-four mathematics journal. A further revision should be mathematical, not documentary: it should classify the missing higher-corank boundary or replace that classification by a genuinely global theorem on the nilpotent filtration, and it should close the remaining priority boundary.**