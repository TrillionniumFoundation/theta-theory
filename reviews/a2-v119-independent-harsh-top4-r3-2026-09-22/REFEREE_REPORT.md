# Independent harsh top-four referee report on A2 revision 119 — Round 3

**Manuscript:** *Codimension bounds and primary structures in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** \`revision/a2-v119-codimension-primary-conductor-2026-09-22\`  
**Frozen mathematical-source commit:** \`59437d7eb88b4791769eaf856bb6dd0f9c6c3a2b\`  
**Controlling prior report:** \`reviews/a2-v118-independent-harsh-top4-2026-09-22/REFEREE_REPORT.md\`  
**This report branch:** \`review/a2-v119-independent-harsh-top4-r3-2026-09-22\`  
**Date:** 22 September 2026

## Referee status and scope

This is an owner-requested, AI-assisted external-referee-style assessment. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report or editorial decision.

This Round-3 report is intentionally distinct from the two earlier v119-labelled reports already present in the repository. Those reports inspected the stale branch \`revision/a2-v119-full-failure-embedded-conductor-2026-09-22\`, which had not yet materialized new v119 mathematics and therefore fell back to v118. The present report instead reviews the actual v119 mathematical source frozen at \`59437d7...\`.

I read the new v119 theorem/proof delta, the full codimension-two section, the connected embedded-primary family, the regularity-controlled conductor transport, the revised higher-defect formalism, the response to R118, the literature audit, the primary article organization, and the current GitHub build state. I also checked the cited Sidman regularity statements against the source and rechecked the public bibliographic record for Ballico 1993. I distinguish throughout:

1. mathematical correctness of the stated theorems;
2. completeness and precision of the proofs;
3. originality and relation to prior literature;
4. breadth and conceptual force at a general top-four mathematics journal;
5. reproducibility and repository provenance.

These are separate questions.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

This recommendation is substantially different in basis from the R118 recommendation.

Revision 119 is a **real and mathematically substantive revision**. It directly answers several of the strongest objections in R118:

- it proves a coefficient-ring codimension stabilization theorem;
- it gives exact equations for the **full** codimension-two zeroth-Fitting failure scheme in degree three;
- it identifies the corank-one open functorially with a relative Grassmannian over the rank-two quotient-algebra scheme;
- it constructs a proper conductor incidence and computes its fibres over the two codimension-two action-rank strata;
- it produces a connected local-algebra family whose full multigenerator failure scheme has an **embedded associated prime**, non-Cartier support, higher-contact-dependent equations, and unbounded nilpotent complexity;
- it transports finite-algebra multiplication cokernels to arbitrary zero-dimensional projective schemes under a regularity bound;
- and it corrects several formal deficiencies in the relative statements.

I did **not** find a fatal counterexample to the new headline theorems during this review.

The top-four recommendation nevertheless remains negative for four main reasons.

First, the nearest-source priority obligation, Ballico 1993, is still explicitly unresolved. For a paper whose principal significance claim is a new scheme-theoretic theory of multiplication/failure loci, this is still a serious originality blocker.

Second, the new “full codimension-two” theorem gives a complete **presentation** of the full Fitting scheme and a complete **normal form off the extreme-corank locus**, but it still does not classify the global geometry along the boundary \(T\). Components may lie entirely in \(T\); the proper incidence is only proved surjective on geometric points; no global component theorem, associated-prime theorem, normalization theorem, or scheme-theoretic boundary classification is given. The revision has crossed the previous Fitting-index barrier, but it has not yet converted the equations into a general geometry of the full codimension-two failure scheme.

Third, the embedded-primary theorem is a convincing answer to the specific R118 request to move beyond a pure Cartier power, but it remains one deliberately structured family and one supplementary disconnected three-generator example. The paper still lacks a general theorem explaining how conductor strata determine associated primes, primary components, or nilpotent orders in a broad class of finite algebras.

Fourth, the delivered v119 branch is not reproducibly green. The mathematical source was successfully frozen, but every current v119 workflow attempt has failed or been cancelled. The latest run fails before the TeX build because \`verify_revision.py\` imports a nonexistent \`inherited-v118/verify_revision.py\`. This is not a mathematical counterexample, but it contradicts the branch's current portability/reproducibility narrative and must be repaired before the revision is referee-ready as a source-bound product.

The result is a manuscript that is now much closer to a strong algebraic-geometry / commutative-algebra paper than v118 was, but whose current general-top-four case still rests on significance claims that have not been fully demonstrated.

# 1. What v119 genuinely changes

A harsh review should begin by recording that the authors did not merely rephrase v118.

## 1.1 The previous Fitting-index obstruction has been materially addressed

R118 emphasized that the higher-defect conductor theory naturally controlled
\[
\operatorname{Fitt}_{r-1}
\]
of the multiplication cokernel, whereas the ordinary nonsurjectivity scheme is
\[
\operatorname{Fitt}_0.
\]

Revision 119 now proves, in codimension two, an actual theorem about the latter.

On the unital codimension-two Grassmannian, after a splitting \(B=W\oplus M\) with \(\operatorname{rank}M=2\), the manuscript introduces
\[
\mathcal K=
[\,\beta\mid C_{w_1}\beta\mid\cdots\mid C_{w_{d-2}}\beta\,]
\]
and proves for every \(m\ge3\)
\[
\operatorname{coker}\mu_m\simeq\operatorname{coker}\mathcal K,
\qquad
\mathcal I_D=I_2(\mathcal K),
\qquad
\mathcal I_T=I_1(\beta)=I_1(\mathcal K).
\]

This is an exact scheme-theoretic statement, not a radical computation and not a theorem only on an exact-rank stratum.

That is a substantial advance over v118.

## 1.2 The codimension stabilization theorem is useful and genuinely ring-level

Theorem \(\ref{thm:codimension-stabilization}\) proves that if \(W\subset B\) contains \(1\) and \(B/W\) has rank \(r\), then
\[
W^{r+1}=\mathcal O[W],
\qquad
W^j=W^{r+1}\quad(j\ge r+1),
\]
over a \(\mathbb Q\)-scheme and after arbitrary base change.

The proof does not pass to geometric fibres and then appeal to semicontinuity. It introduces the residual filtration
\[
W^{j+2}=W\oplus N_j,
\]
uses the compressed-commutator identity
\[
[C_w,C_v]=\beta_vD_w-\beta_wD_v,
\]
and combines adjacent transpositions modulo \(N_{r-1}\) with the polarized Cayley--Hamilton identity for an \(r\times r\) matrix.

I find this proof conceptually clean. The main point is precisely that the compressed operators need not commute, but their commutators drop into the lowest residual layer. That is the right coefficient-ring issue to address.

## 1.3 The proper incidence now connects the corank-one geometry to the conductor boundary

The new morphism
\[
Z\to D
\]
from a relative Grassmannian over \(\operatorname{Hilb}^2(B)\) is not just decoration.

On
\[
D\setminus |T|
\]
the paper proves an isomorphism of schemes, including nonreduced test schemes, with the quadratic-generation open \(Z^\circ\). Thus the corank-one part of the full failure scheme has a genuine quotient-algebra normal form.

The fibre calculation over \(T\) then recovers the two conductor mechanisms from v118:

- action rank one gives \(\operatorname{Hilb}^2(Q)\) for a rank-three quotient \(Q\), cut out on \(\mathbb P(Q/\mathcal O)\) by the binary cubic \(v\mapsto \bar v\wedge\overline{v^2}\);
- action rank two gives \(\operatorname{Spec}C\) for the rank-two conductor quotient algebra.

This is the first place where the higher-defect conductor theorem and the full \(\operatorname{Fitt}_0\) failure scheme genuinely interact.

## 1.4 The new nonreduced family is no longer a pure Cartier power

For
\[
B_h=\mathbb C[x,y]/(x^2,xy,y^h),
\qquad h\ge5,
\]
the manuscript obtains a local ring of the **full** multigenerator failure scheme with coefficient ideal
\[
I_h=(F_h,vF_{h-1},bv,b^2u)
\subset\mathbb C[b,u,v].
\]

It proves
\[
I_h=(u,v)\cap(b^2,bv,F_h,vF_{h-1}),
\]
with associated primes
\[
(u,v),
\qquad
(b,u,v),
\]
the latter embedded.

This directly answers the strongest conceptual criticism of the truncated-fat-point theorem in v118. The new geometry is not of the form \((\delta^N)\) for one prime Cartier divisor. The support has codimension at least two, the higher contact coefficients enter the equations, and the nilradical complexity grows with \(h\).

This is genuine new primary geometry.

## 1.5 The global conductor theorem is much broader than the old monomial fat-point transport

For an arbitrary nonempty zero-dimensional
\[
Z\subset\mathbb P^e
\]
with saturated homogeneous ideal \(I\), the paper sets
\[
r=\operatorname{reg}I,
\qquad
s=\operatorname{reg}(I^2)
\]
for the ordinary homogeneous square and proves the global/finite multiplication-cokernel comparison when
\[
n\ge\max\{r,s-1\}.
\]

Using the standard bound
\[
\operatorname{reg}(I^2)\le2\operatorname{reg}I
\]
for zero-dimensional schemes yields the uniform sufficient range
\[
n\ge2\operatorname{reg}I-1.
\]

The proof fills the conormal layer first and the ordinary-square layer second. This is a real generalization of the earlier monomial interval argument and applies to mixed supports and nonmonomial finite schemes.

# 2. Proof audit: codimension stabilization

I found no fatal error in the new stabilization theorem, but several aspects deserve emphasis.

## 2.1 The residual filtration identity is the critical structural step

With \(B=W\oplus M\), multiplication by \(w\in W\) is written
\[
L_w=
\begin{pmatrix}
A_w&D_w\\
\beta_w&C_w
\end{pmatrix}.
\]

The manuscript defines \(N_0\) from the images of the \(\beta_w\), and \(N_j\) by applying words of length at most \(j\) in the \(C_w\). The identity
\[
W^{j+2}=W\oplus N_j
\]
is the correct way to turn algebra generation into a finite-rank linear problem.

This is stronger than a fibrewise “dimension can grow at most \(r\) times” argument because it keeps the nilpotent coefficient structure.

## 2.2 The commutator estimate is used in the right direction

From commutativity of the full \(L_w\),
\[
[C_w,C_v]=\beta_vD_w-\beta_wD_v,
\]
so the compressed commutator has image in \(N_0\).

The proof then shows that adjacent swaps in a word of length \(r\) change its action on \(N_0\) only by \(N_{r-1}\). This is enough to symmetrize the top Cayley--Hamilton coefficient.

The requirement that \(r!\) be invertible is explicit. Thus the theorem is appropriately stated over a \(\mathbb Q\)-scheme.

## 2.3 The novelty position of this theorem is not yet adequate

The theorem may well be new in the precise relative commutative form stated here. I am not asserting anticipation.

However, a central theorem about the length needed for words/products of a generating subspace to span a finite-dimensional algebra belongs near a substantial pre-existing “length of finite-dimensional algebras” literature. Pappacena's 1997 *Journal of Algebra* paper, for example, studies bounds on word length needed for a generating set to span a finite-dimensional algebra, building on older length questions.

The manuscript currently compares the result mainly with generator/polygenerator schemes and says that the elementary dimension bound is not the same as the scheme-theoretic stabilization theorem. That is true but insufficient as a top-four priority audit.

A revision should explain precisely:

- what earlier algebra-length bounds assume;
- whether commutativity changes the optimal bound;
- whether the codimension \(r+1\) estimate is known over fields;
- what part is new only at the relative/nonreduced coefficient-ring level;
- and whether the proof produces an optimal bound in a natural class.

Without this, one of the paper's cleanest new theorems is not placed adequately in the literature.

# 3. The phrase “full codimension-two failure scheme” is mathematically defensible but editorially stronger than what is classified

The paper now does have equations for the whole scheme \(D\). I therefore would not repeat the v118 objection that the manuscript only studies the extreme-corank locus.

But there is a new and more precise distinction.

## 3.1 The theorem presents \(D\); it does not classify \(D\)

The identity
\[
\mathcal I_D=I_2(\mathcal K)
\]
is a presentation theorem.

The isomorphism
\[
Z^\circ\simeq D\setminus|T|
\]
is a classification theorem on the corank-one open.

The fibre descriptions over exact conductor strata describe the set/scheme of incidence lifts over points of \(T\).

What is still missing is a theorem describing the global geometry of \(D\) **along** \(T\).

The manuscript itself says that a component of \(D\) may be contained entirely in \(T\). Once that is admitted, the following remain open for a general finite algebra \(B\):

- the irreducible components of \(D\);
- which components meet \(D\setminus|T|\);
- closure relations of conductor strata;
- generic multiplicities along \(T\);
- associated primes along \(T\);
- embedded components supported in \(T\);
- normality or Cohen--Macaulayness of components;
- whether \(Z\to D\) is scheme-theoretically surjective;
- whether it is finite, birational, a normalization, or a blow-up in any broad class;
- and which boundary singularities occur.

Thus the paper now controls the whole equation ideal but not the whole geometry.

For a specialist paper, this is already meaningful. For a general top-four paper, the title and narrative should not blur “equations for the full scheme” into “classification of the full scheme.”

## 3.2 Geometric-point surjectivity is much weaker than the property one wants from the incidence

The theorem proves that the proper morphism \(Z\to D\) is surjective on geometric points.

That is enough to say every geometric failure point has a hyperplane-algebra lift.

It is not enough to transport arbitrary nilpotent boundary structure from \(D\) to \(Z\), nor to identify local rings on \(T\).

The strongest local-ring transfer occurs only on \(D\setminus|T|\).

If the incidence is meant to be the organizing object of the theory, the next theorem should determine its scheme-theoretic behavior over the boundary.

## 3.3 The fibre computations are useful but do not solve the gluing problem

Over an exact action-rank stratum, the two fibres are concrete and elegant.

But a list of fibres does not determine a morphism.

The hard geometry is how those fibres vary, degenerate, acquire embedded structure, and interact with the local equations \(I_2(\mathcal K)\) as one approaches rank jumps.

This is exactly where the earlier example with the nonreduced rank-one locus \(s^2=0\) suggests genuinely interesting structure.

The manuscript should exploit that phenomenon globally rather than stop at fibre identification.

# 4. The connected embedded-primary family is a serious improvement, but its generality should not be overstated

Theorem \(\ref{thm:embedded-multigenerator}\) is probably the most important new example in v119.

## 4.1 The primary decomposition is explicit and nontrivial

On the chart of \(\operatorname{Hilb}^2(B_h)\) with quotient basis \(1,y\), the equations
\[
y^2=uy+v,
\qquad
x=b(y-u)
\]
lead to
\[
I_h=(F_h,vF_{h-1},bv,b^2u).
\]

The decomposition
\[
I_h=(u,v)\cap(b^2,bv,F_h,vF_{h-1})
\]
is not a generic formal consequence of a divisor power.

The minimal and embedded primes are different, and the \(b\)-terms really couple the extra square-zero tangent direction to the higher contact algebra.

This is exactly the sort of phenomenon R118 asked for.

## 4.2 The incidence realization matters

The paper does not merely compute a Hilbert-scheme chart and call it multiplication failure.

It chooses a point \(W_0\) whose quadratic image is the conductor hyperplane and localizes at a nonzero quadratic-generation coefficient. The corank-one incidence theorem then identifies this chart with an open neighborhood in the actual full multiplication failure scheme.

That step is important and, in my reading, legitimate.

## 4.3 The theorem is still a family, not a conductor-primary classification

The construction is highly structured:

\[
B_h=\mathbb C[x,y]/(x^2,xy,y^h).
\]

It gives unbounded nilpotent complexity and a connected local family, which is enough to defeat the “pure Cartier power only” criticism.

But it does not yet prove a general principle such as:

> embedded associated primes of the multiplication-failure scheme correspond to specified degenerations of the conductor action.

Nor does it classify primary components for all codimension-two finite local algebras of a given length, embedding dimension, Hilbert function, or socle type.

The paper currently has a striking example and a mechanism for realizing it. A top-four theory should turn that example into a theorem about a natural class.

# 5. The three-generator corollary should remain secondary

The supplementary example
\[
(\mathbb C[x,y]/(x^2,y^2))\times\mathbb C^s
\]
produces the local ideal
\[
(ab,b^2)=(b)\cap(a,b)^2,
\]
and \(s=1\) gives a three-generator instance.

This is useful because it prevents a reader from dismissing embedded structure as requiring arbitrarily many generators.

But the algebra is disconnected and contains an appended reduced factor. It should not carry major conceptual weight. The connected \(B_h\) theorem is the real result.

# 6. The regularity-controlled transport theorem appears sound, but its novelty burden is not yet discharged

I checked the main classical input.

Sidman's theorem on regularity of products implies, for a zero-dimensional projective scheme,
\[
\operatorname{reg}(I^2)\le2\operatorname{reg}(I).
\]

The manuscript uses this correctly as an input rather than claiming it.

## 6.1 The kernel-filling proof is coherent

Choose \(g\in U\) invertible on \(Z\).

The first step lifts the conormal class using
\[
K_t\to H^0(Z,(\mathcal I/\mathcal I^2)(t)),
\]
then subtracts \(gq\) so the remainder lies in the ordinary-square layer.

The second step uses generation of \(I\) in degrees at most \(r\) to prove
\[
(I^2)_{t+n}=I_nI_t
\]
when \(n,t\ge r\), and uses saturation in degree at least \(s\).

This gives
\[
K_{t+n}=UK_t
\]
and hence the iterated kernel identity.

I did not find a contradiction in this argument.

## 6.2 The relative theorem should be expanded slightly

The relative theorem passes from a uniform fibre regularity bound to locally free pushforwards and arbitrary base change.

This is standard in spirit, but the statement is broad enough that the proof should be completely explicit about the exact relative regularity/cohomology-and-base-change theorem being used.

In particular, state clearly:

- from which degree onward each \(R^1p_*\mathcal I_{\mathcal Z}(t)\) vanishes;
- why \(p_*\mathcal I_{\mathcal Z}(t)\) is locally free and base-changing;
- how uniform bounds for \(\operatorname{reg}(I_z^2)\) are used when that stronger hypothesis is chosen;
- and why the fibrewise surjectivity of the kernel-filling map over the relative Grassmannian gives global surjectivity after arbitrary pullback.

The current proof is probably correct, but it is terse relative to the strength of the statement.

## 6.3 The originality discussion is incomplete

The theorem's genuinely new claim is not the regularity inequality. It is the identification of the actual multiplication cokernel of an incomplete series with the finite-algebra cokernel under the regularity range.

That distinction is correctly stated.

However, because the nearest historical literature is literally about failure loci of higher-order embedding properties, the unresolved Ballico comparison is directly relevant here.

Until that comparison is closed, I cannot assess whether the transport theorem is a genuinely new general bridge or a refined formulation of an existing failure-locus argument.

# 7. The Ballico 1993 comparison remains a real top-four blocker

The paper deserves credit for not pretending this problem is solved.

The v119 literature audit explicitly says that complete theorem text for

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, *Mathematische Nachrichten* 163 (1993), 5--13,

has not been obtained.

The public publisher record confirms the paper's bibliographic existence, but the currently accessible route did not provide the theorem text in this review either.

The correct conclusion is therefore limited:

- I do **not** claim that Ballico anticipates the v119 theorems.
- I also do **not** certify that it does not.

For a specialist revision, this could remain an editorially manageable literature item for a short period.

For a general top-four submission, it is much more serious. The paper's significance case depends on asserting a broad new scheme-theoretic failure-locus package. The nearest historical source cannot remain unread at the theorem level.

# 8. The finite-generator / polygenerator comparison needs updating

The manuscript cites the Arpin--Bozlee--Herr--Smith generator-scheme work and correctly distinguishes the generator open from the closed multiplication Fitting schemes studied here.

That comparison should be retained.

However, the bibliography still presents the work essentially as an arXiv item, whereas *The Scheme of Monogenic Generators I: Representability* was published in *Research in Number Theory* in 2023.

A top-four submission should cite the published source where available and perform the closest theorem-level comparison with its explicit equations, Hilbert/configuration-space relations, and polygenerator constructions.

This is minor compared with Ballico, but it is part of the same general issue: the paper now has enough mathematical substance that its literature audit must be correspondingly professional.

# 9. The title and abstract need one more round of scope calibration

The abstract is much more accurate than earlier versions.

Still, two phrases can be read too strongly.

## 9.1 “We determine multiplication failure”

The paper determines several major families and gives a powerful codimension-two presentation.

It does not determine multiplication failure for arbitrary codimension and arbitrary finite algebra.

A safer opening would say that the paper develops a scheme-theoretic framework and determines the codimension-two presentation plus several primary families.

## 9.2 “the entire failure scheme”

This is correct if understood as “the entire ideal \(I_2(\mathcal K)\) is presented.”

It is not correct if read as “the entire irreducible/primary geometry is classified.”

The abstract should make the distinction explicit in the same sentence.

# 10. The pipeline position of A2 is now less clear, not more clear

As a standalone article, v119 has become substantially more coherent: its strongest new core is algebraic geometry and commutative algebra of multiplication Fitting schemes.

But within the repository's larger theta-theory paper pipeline, the A2 lineage still contains extensive earlier statistical, boundary, wall, and information-theoretic material, much of which survives only as complementary sections and appendices.

This creates a programmatic ambiguity:

- Is A2 now intended to be the algebraic-geometric foundations paper for multiplication failure?
- Is it still supposed to be the second logical step of the original theta-theory chain?
- Which theorems of A1 are used materially by the new v119 core?
- Which later A3--D1 papers depend on the codimension/conductor results proved here?

For journal refereeing this is not, by itself, a correctness defect. A paper may stand alone.

But if the “theta-theory pipeline” is part of the significance narrative, the repository should contain a short dependency map showing why this paper is A2 rather than an independent algebraic-geometry branch.

The current full manuscript's retention of many historical developments does not substitute for that logical dependency map.

# 11. The current build failure must be fixed before the next round

The branch was not reproducibly green at the time of this review.

The v119 workflow history on
\[
\texttt{revision/a2-v119-codimension-primary-conductor-2026-09-22}
\]
shows multiple cancelled or failed runs.

The latest source-freezing run successfully created the mathematical source commit
\[
\texttt{59437d7eb88b4791769eaf856bb6dd0f9c6c3a2b}.
\]

It then failed in the “Exact checks and all reading editions” step before reaching PDF publication.

The concrete error is:

\[
\texttt{FileNotFoundError: v119/inherited-v118/verify\_revision.py}.
\]

The current \`verify_revision.py\` unconditionally imports
\[
\texttt{HERE/'inherited-v118/verify_revision.py'},
\]
but that path is absent in the frozen v119 source tree.

This has two consequences.

1. The canonical \`build.sh\` does not currently reproduce the claimed complete v119 build.
2. The README statement that the retained manifest makes an isolated v119 build portable is false as committed, because the diagnostic runner still has a hard dependency on a missing inherited file.

Again: this does not falsify any theorem.

But the revision should not be called source-bound/reproducible until a clean run succeeds from the frozen tree.

# 12. Formal issues requiring revision even outside the top-four significance question

## 12.1 Expand the rank-two incidence-fibre representability proof

In Proposition \(\ref{prop:codim-two-incidence-fibres}\), the rank-two action case identifies the fibre with \(\operatorname{Spec}C\) via characters of \(C\).

The argument is plausible, but for a theorem explicitly advertised as valid on arbitrary nonreduced test schemes, give the functor-of-points proof in complete detail:

- a \(T\)-point of \(\operatorname{Spec}C\);
- the induced ideal \(I\subset C_T\);
- the subbundle \(IM_T\subset M_T\);
- the quotient-line property;
- the resulting hyperplane algebra;
- and inverse compatibility under arbitrary pullback.

The current phrase “as can be checked after trivializing \(M\) over \(C\)” is shorter than the rest of the paper's standard of relative precision.

## 12.2 Clarify the scheme notation \(D\setminus|T|\)

Because \(T\) is nonreduced, the notation means restriction to the open complement of the **support** of \(T\), not a scheme-theoretic difference.

State this once in the theorem.

## 12.3 Separate presentation, classification, and incidence properties in the theorem roadmap

The paper now proves three different strengths of statement:

- a global equation theorem for \(D\);
- an isomorphism theorem off \(T\);
- a proper incidence with fibre descriptions over \(T\).

These should be labelled distinctly in the introduction rather than grouped under one “full codimension-two” slogan.

## 12.4 Explain optimality of the codimension bound

The theorem gives \(r+1\).

Is this sharp for every \(r\), for a natural family, or only a sufficient universal bound?

A clean family showing sharpness would greatly improve the theorem's conceptual status.

If no general sharpness is claimed, say so explicitly.

## 12.5 Update published bibliographic metadata

Where papers cited as arXiv preprints now have published versions, cite the published articles.

This matters especially for the nearest generator-scheme literature.

# 13. Disposition of the R118 mandatory items

My assessment is as follows.

| R118 item | v119 status | Round-3 assessment |
|---|---|---|
| E118.1 Ballico 1993 theorem-level comparison | **Open** | Still a genuine priority blocker |
| E118.2 separate stable-image flags / extreme-corank locus / full failure scheme | **Closed** | The new text distinguishes these correctly |
| E118.3 theorem on the full codimension-two failure scheme | **Substantially addressed, not conceptually exhausted** | Exact \(I_2(\mathcal K)\) presentation and corank-one normal form are real; boundary geometry along \(T\) remains unclassified |
| E118.4 move beyond pure Cartier-power nonreducedness | **Closed in the requested sense** | \(B_h\) gives a connected embedded-primary, non-Cartier family |
| E118.5 make higher-defect and nonreduced mechanisms interact | **Substantially addressed** | The same conductor incidence transfers local rings and has boundary fibres governed by conductor strata |
| E118.6 broaden global transport beyond one fat point | **Closed mathematically** | Arbitrary finite projective schemes under regularity bounds |
| E118.7 formal cleanups | **Largely closed** | Remaining points are refinements, not the old defects |

A future referee should not recycle E118.2, E118.4, or E118.6 as if v119 had not changed.

# 14. New mandatory revisions arising from v119

## E119.1 — Close the nearest-source comparison before making a top-four originality case

Obtain and read the complete Ballico 1993 article.

Prepare a theorem-by-theorem table covering:

- the definition of the relevant failure locus;
- whether scheme structure or only support/cycles are retained;
- whether incomplete linear series are allowed;
- fixed versus moving finite contacts;
- multiplication versus higher-order embedding/osculating conditions;
- quotient-algebra/Hilbert incidences;
- conductor or residual mechanisms;
- nonreduced structure;
- and global degree/regularity hypotheses.

Also add the finite-dimensional algebra-length literature to the discussion of Theorem \(\ref{thm:codimension-stabilization}\).

## E119.2 — Prove a boundary theorem for the full codimension-two scheme

The next mathematical step should concern \(D\) **along \(T\)**.

A convincing theorem would do at least one of the following for a broad class of finite algebras:

- classify irreducible components contained in \(T\);
- identify associated primes supported in \(T\);
- determine a scheme-theoretic image of \(Z\to D\);
- prove finiteness/birationality/normalization on a natural component;
- give a local normal form near an action-rank jump;
- or compute how the binary-cubic and quadratic-algebra fibres glue across conductor strata.

The current fibre list is not enough.

## E119.3 — Generalize the conductor-to-primary mechanism beyond the \(B_h\) family

The embedded \(B_h\) family is excellent evidence.

Now formulate a theorem that predicts embedded components from structural data of the conductor quotient.

Possible natural classes include:

- embedding-dimension-two Artin local algebras with a prescribed Hilbert function;
- stretched or almost-stretched local algebras;
- codimension-two complete intersections;
- finite Gorenstein algebras of small socle dimension;
- or another class for which the conductor incidence can be analyzed uniformly.

The objective is a theorem, not a longer list of examples.

## E119.4 — Establish the status and sharpness of the \(r+1\) stabilization bound

Give a precise comparison with existing algebra-length results and either:

- prove sharpness in every codimension \(r\), or
- characterize when stabilization happens earlier, or
- state clearly that the theorem is a universal sufficient bound and identify the open optimality problem.

## E119.5 — Repair the reproducible build and publish one clean source-bound run

Remove the missing inherited-script dependency or actually vendor the required inherited diagnostic source.

Then run the canonical build from the frozen source tree and produce a successful workflow whose receipts identify:

- the mathematical source SHA;
- the PDF/product SHA;
- the exact diagnostic output;
- and the fact that no earlier revision directory was mutated.

No new mathematical claim is required here; this is a delivery requirement.

## E119.6 — Expand the relative representability/base-change proofs

Strengthen the functor-of-points proof of the rank-two incidence fibre and the relative regularity-conductor theorem.

The statements are broad enough that these proofs should not rely on phrases such as “check after trivializing” where nilpotent bases are part of the advertised result.

## E119.7 — Clarify the paper's role in the theta-theory pipeline

Add a short nontechnical dependency note identifying:

- what A2 takes from A1;
- what its new finite-algebra/conductor theorems provide to A3 or later papers;
- and which retained complementary sections are historical context rather than logical prerequisites.

This does not require deleting any mathematics.

# 15. What would materially change the top-four assessment

A larger diagnostic matrix, more values of \(h\), or more archived earlier versions will not change the recommendation.

Nor is another isolated embedded example likely to be enough.

A renewed top-four case would be materially stronger if it contained the following package:

1. **Priority closure.** The nearest failure-locus literature is compared theorem by theorem, including Ballico 1993.

2. **Boundary geometry.** The full codimension-two presentation is converted into a theorem about components/associated primes/normalization/local boundary geometry along \(T\).

3. **A general conductor-primary theorem.** The \(B_h\) example becomes an instance of a structural class.

4. **Optimality or structural sharpness of codimension stabilization.** The \(r+1\) bound is placed correctly against algebra-length theory.

5. **Clean reproducibility.** The branch builds successfully from its frozen source.

If those are achieved, the paper would no longer look like a sequence of increasingly sophisticated exact families. It would look like a general theory with examples.

# 16. Correctness assessment of the new v119 mathematics

Within the scope of this review, I found no fatal counterexample to the following new claims:

- codimension-\(r\) stabilization \(W^{r+1}=\mathcal O[W]\) over the coefficient ring;
- stability of Fitting ideals in the corresponding degree range;
- the degree-three residual presentation in codimension two;
- the equality \(\mathcal I_D=I_2(\mathcal K)\);
- the equality of the extreme-corank/subalgebra ideal with \(I_1(\beta)\);
- the corank-one incidence isomorphism on \(D\setminus|T|\);
- the rank-three binary-cubic fibre;
- the rank-two \(\operatorname{Spec}C\) fibre;
- the explicit \(B_h\) quotient chart;
- the primary decomposition \(I_h=P_h\cap Q_h\);
- the existence of the embedded associated prime;
- the stated nilradical growth mechanism;
- the realization of that coefficient ring as a local ring of the full failure scheme on the specified open;
- the general kernel-filling identity under \(n\ge\max\{r,s-1\}\);
- or the resulting global/finite coherent-cokernel comparison.

This is **not proof certification**. It means only that my negative recommendation is not based on a discovered contradiction in these headline statements.

# 17. Overall significance assessment

Revision 119 is the first version in this sequence for which I think the paper has a genuinely coherent new core:

\[
\text{codimension stabilization}
\Longrightarrow
\text{full codimension-two Fitting presentation}
\Longrightarrow
\text{conductor incidence}
\Longrightarrow
\text{embedded primary local rings}
\Longrightarrow
\text{global transport}.
\]

That chain is much stronger than the parallel mechanisms in v118.

The weakness is no longer “there is no full failure theorem” in the literal sense.

The weakness is that the paper has not yet extracted the global geometry encoded by its own full equations, and has not yet demonstrated that the new chain is historically and conceptually large enough for a general top-four journal.

This is a materially better position than v118.

# 18. Final recommendation

I recommend **rejection in the present form at a general top-four mathematics journal**.

I would not reject this version because it lacks mathematical content. It has substantial content:

- a clean relative codimension stabilization theorem;
- a full degree-three Fitting presentation in codimension two;
- a quotient-algebra incidence that is an actual scheme isomorphism on the corank-one open;
- conductor-controlled boundary fibres;
- an explicit connected non-Cartier embedded-primary family;
- unbounded nilpotent complexity;
- a general regularity-controlled transport theorem;
- and markedly improved formal precision.

The present blockers are instead at the level appropriate to a very high-end general journal:

- the nearest-source priority comparison is still incomplete;
- the full codimension-two **equations** have not yet become a full codimension-two **boundary geometry**;
- the conductor-to-primary mechanism is demonstrated by a strong family rather than proved as a general structural theorem;
- the novelty and sharpness of the central stabilization theorem are not adequately situated against algebra-length literature;
- and the committed v119 build is currently broken by a missing diagnostic dependency.

A specialist submission built around the new core would now be credible after ordinary revision and literature cleanup.

A renewed Annals/Inventiones/JAMS/Acta-level submission should, in my view, be driven by the boundary/conductor-primary theorem in E119.2--E119.3, together with complete priority closure, rather than by another round of additional examples or diagnostics.
