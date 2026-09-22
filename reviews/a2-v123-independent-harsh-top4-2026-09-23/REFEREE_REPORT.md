# Independent harsh top-four referee report — A2 revision 123

**Manuscript:** *Polarized ramification and higher-corank structure in multiplication failure*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision:** revision/a2-v123-polarized-k3-corank-two-2026-09-23  
**Reviewed branch head:** 89c3ef67319b56e6eaeae4e06b45d93def19ffa0  
**Controlling previous report:** reviews/a2-v122-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md  
**Previous reviewed product:** revision/a2-v122-intrinsic-primary-k3-boundaries-2026-09-23 at 37480f3872b5c9f4ae18731e60a799986114c427  
**Principal reading object:** geometry.pdf, 16 pages  
**Complete archival companion:** paper.pdf, 147 pages  
**Date:** 23 September 2026

## Status of this report

This is an owner-requested, AI-assisted external-referee-style report. It was not commissioned by *Annals of Mathematics*, *Inventiones Mathematicae*, *Journal of the American Mathematical Society*, *Acta Mathematica*, or any other journal, and it must not be represented as a journal-issued report.

I reviewed the revision-123 mathematical source, not merely the response letter or generated PDFs. In particular I checked the relation/ramification construction, the full Fitting presentation and corank-one normal form, the section-ring reconstruction of the polarization, the 24-dimensional Jacobian-image calculation and nine-dimensional quotient statement, the fixed-tensor projection-corank-two calculation, the comparison with the classical determinantal order profile, the exact finite certificates, the response to revision 122, and the literature audit.

The standard applied below is the standard of an exceptionally selective general mathematics journal. At that level correctness is necessary but not sufficient: the paper must also have a conceptual theorem of exceptional scale, a closed priority boundary against the closest literature, and a natural formulation that does not stop at the first exceptional stratum created by its own mechanism.

# Recommendation

## Reject in the present form at a general top-four mathematics journal.

This recommendation is substantially different in basis from my recommendation on revision 122.

Revision 123 is a real mathematical revision. It does not merely repackage the previous manuscript. It directly addresses most of the mathematical objections in the revision-122 report:

1. it reconstructs the quartic polarization from the intrinsic nilpotent structure rather than only the abstract K3 surface;
2. it proves that the actual family of polarized quartics has a nine-dimensional moduli image and that the relation system has generically finite projective ambiguity over that image;
3. it crosses projection corank two on a nonempty fixed-tensor open and finds a genuinely new embedded associated support with nilpotency index three;
4. it explicitly derives the retained weighted determinantal formula from the classical symbolic-order profile rather than implicitly presenting classical determinantal structure as new;
5. it rewrites the relative smoothness, flatness, intrinsic torsion, and base-change arguments in a cleaner form.

I do **not** find a fatal contradiction in the new local algebra or in the new section-ring reconstruction. The displayed determinant-line cancellation is coherent; the 24-dimensional differential witness proves what it is claimed to prove; and the corank-two primary decomposition is compatible with the residual matrix calculation under the stated admissibility hypotheses.

The remaining objections are now about the *top-four theorem*, not about whether revision 123 contains serious mathematics.

The decisive obstacles are:

- the nearest historical failure-locus source, Ballico 1993, is still unread at theorem-text level by the authors' own audit;
- the nine-dimensional Reye/Enriques geometry is classical, and the revision does not yet isolate theorem-by-theorem which part of Theorem 1.2 is new rather than a reparametrization or infinitesimal verification of that classical nine-dimensional family;
- the advertised “higher-corank structure” is proved only on an admissible open of projection corank two, while the exceptional corank-two locus and coranks three and four remain unclassified;
- the two strongest new mechanisms are not yet unified: polarized reconstruction deliberately throws away the higher-corank singular part by restricting to the smooth locus of the reduction, while the higher-corank theorem is a separate local calculation;
- the generic-finite reconstruction stops short of a Torelli-type classification: the generic degree is not computed, exceptional fibres are not described, and the actual relation tensor/quadratic map is not recovered;
- the moduli theorem is established by an exact 25-by-25 rank certificate at one point. That is a valid proof of generic immersion, but at this level it is not yet a conceptual description of the deformation map or of the resulting special K3 locus.

My assessment is therefore: **mathematically substantial and potentially strong for a specialist venue, but not yet at the conceptual and priority threshold of Annals/Inventiones/JAMS/Acta.**

# 1. What revision 123 genuinely fixes

A harsh report should not recycle objections that the authors have actually solved.

## 1.1 The polarized reconstruction is a real strengthening

Revision 122 recovered the abstract K3 surface from the intrinsic embedded support and stable-birational cancellation. The new proof is stronger and cleaner.

On the intrinsic embedded support
\[
E=\operatorname{Tot}_{Y\times\mathbf P(S)}(\mathcal H^*\otimes Q),
\]
the paper identifies the nilradical line and canonical bundle as
\[
\mathcal N\simeq
\pi^*(A^{-1}\boxtimes B^{-1}),
\qquad
\omega_E\simeq
\pi^*(A^{-(p-1)}\boxtimes B^{-(p+e-1)}),
\]
and hence
\[
\omega_E\otimes\mathcal N^{-(p+e-1)}
\simeq
\rho^*A^e.
\]

The “no extra fibrewise functions” lemma proves
\[
\rho_*\mathcal O_E=\mathcal O_Y.
\]
Consequently the intrinsic graded ring is
\[
\bigoplus_{n\ge0}
H^0\!\left(E,
(\omega_E\otimes\mathcal N^{-(p+e-1)})^{\otimes n}
\right)
\simeq
\bigoplus_{n\ge0}H^0(Y,A^{en}).
\]

For a K3 surface, torsion-freeness of the Picard group then recovers the fourth root \(A\) from \(A^4\).

This is not the earlier stable-birational argument in disguise. It recovers a polarized projective model.

## 1.2 The K3 case now has an actual moduli theorem

Revision 122 only showed that the algebras \(B_R\) have moduli. Revision 123 calculates the differential of the actual Jacobian map
\[
R\longmapsto [F_R],
\qquad
F_R=\det J_R,
\]
on a 24-dimensional Grassmannian chart.

At the explicit integral point \(C_*\), the manuscript produces 24 parameter derivatives whose classes modulo the line spanned by \(F_{C_*}\) are independent. The specified 25-by-25 determinant is
\[
4279473148893659522379284480\neq0.
\]

This proves a 24-dimensional image in the space of embedded smooth quartics. Quotienting the 15-dimensional projective-coordinate orbit gives a nine-dimensional image in polarized quartic K3 moduli, and equivariance plus generic finiteness before quotienting gives generic finite ambiguity after quotienting.

This directly addresses revision-122 blocker B3.

## 1.3 The fixed-tensor theorem now crosses projection corank two

The new residual matrix
\[
[L(T),\,C\,T^{(2)}],
\qquad
T=\begin{pmatrix}a&b\\c&d\end{pmatrix},
\]
is not a continuation of the corank-one two-parameter normal form.

On the stated admissible open, the manuscript derives
\[
J
=
I_3[L(T),CT^{(2)}]
=
\delta\mathfrak m+(g_0,\ldots,g_4)
=
\left(\bigcap_{i=1}^4P_i\right)\cap\mathfrak m^3,
\]
where
\[
\delta=ad-bc,\qquad
\mathfrak m=(a,b,c,d).
\]

It then obtains the fixed-tensor failure ideal
\[
\mathcal I_{\widehat D}
=
(\delta)
\cap P_1^2\cap P_2^2\cap P_3^2\cap P_4^2
\cap\mathfrak m^5.
\]

Thus the first higher-corank stratum actually creates an additional embedded associated support. The nilradical satisfies
\[
\widehat{\mathcal N}^3=0,
\qquad
\widehat{\mathcal N}^2\neq0,
\]
and the annihilator of \(\widehat{\mathcal N}^2\) recovers the rank-two support on this open.

That is a genuine answer to revision-122 blocker B2, although only on the stated admissible open.

## 1.4 The determinantal priority boundary is materially improved

Appendix A now states the classical product formula
\[
I^\rho
=
\bigcap_j I_j(A)^{(\gamma_j(\rho))}
\]
and derives the weighted formula coefficient by coefficient after adjoining the scalar \(t\).

The manuscript is now explicit that the weighted identity is a consequence of the classical symbolic-order profile plus the scalar coefficient rule, not a new straightening theorem.

This is the correct scholarly direction and substantially answers revision-122 blocker B4.

## 1.5 The previous formal proof-architecture objections are mostly closed

The relative Cartier/flatness argument is more explicit. The intrinsic generic torsion is defined as a coherent kernel rather than by informal localization language. The arbitrary-base-change statement is isolated through a Tor argument. The exact \(e=4\) witness is in the principal article. The older MRC argument is demoted to a remark rather than carrying the principal reconstruction theorem.

I would not repeat revision-122 objections M4–M8 as though nothing had changed.

# 2. Correctness audit of the new mathematical core

My negative top-four recommendation is not based on finding the new central formulas false. I record what I checked.

## 2.1 Relative ramification family

The restriction/contraction exact sequence
\[
0\to\operatorname{Sym}^2\mathcal H
\to\operatorname{Sym}^2V\otimes\mathcal O
\to V\otimes\mathcal O(1)
\to0
\]
is correct in characteristic zero with the stated normalization.

For a basepoint-free \(R\), the quadratic map
\[
\phi_R:\mathbf P(V^*)\to\mathbf P(R^*)
\]
is finite because \(\phi_R^*\mathcal O(1)=\mathcal O(2)\) is ample and a positive-dimensional fibre would contain a curve on which this pullback is trivial. Its degree is \(2^{e-1}\).

The equivalence
\[
R\text{ basepoint-free}
\quad\Longleftrightarrow\quad
\gamma_R(HV)=S_R
\text{ for every hyperplane }H
\]
follows from
\[
(HV)^\perp=\mathbf C\alpha^2.
\]

The universal bad-incidence codimension counts are also consistent with \(e=3,4\).

## 2.2 Full Fitting presentation and corank-one normal form

The cube-zero multiplication gives the presentation
\[
\begin{pmatrix}
1&0&0\\
0&M&0\\
0&A_0&\gamma\operatorname{Sym}^2M
\end{pmatrix}.
\]

The maximal-minor argument yields
\[
\mathcal I_{\widehat D}
=
(\det M)\,I_p(\gamma\operatorname{Sym}^2M).
\]

At projection corank one,
\[
M=\operatorname{diag}(I_{e-1},t),
\]
and the first-order spanning condition turns the quadratic block into the same column module as \([A,tI]\). Along smooth ramification, Schur reduction gives
\[
\mathcal I_D=(t^2,tf)=t(t,f).
\]

Hence
\[
\mathcal I_D
=
\mathcal I_\Delta\mathcal I_E
=
\mathcal I_\Delta\cap\mathcal I_E^2
\]
with exactly the two associated supports claimed.

I see no new defect in this chain.

## 2.3 Intrinsic section-ring reconstruction

The vector-bundle total-space formula
\[
\omega_{\operatorname{Tot}W}
=
\pi^*(\omega_Z\otimes\det W^{-1})
\]
gives the exponents printed in the paper.

The proof that
\[
\rho_*\mathcal O_E=\mathcal O_Y
\]
is also credible. A positive-degree global section would define a homogeneous polynomial on \(\operatorname{Hom}(H_0,S)\) that factors through every quotient \(S/\Lambda\), hence is invariant under translations by every \(\operatorname{Hom}(H_0,\Lambda)\). These directions span the full translation space, so the polynomial is constant; its positive homogeneous part is zero.

This is the key technical point that makes the section ring intrinsic rather than polluted by affine-bundle functions.

For \(e=4\), the short Picard-torsion argument is correct: a nontrivial torsion line bundle and its inverse have no sections, while Riemann–Roch on a K3 gives Euler characteristic two, a contradiction.

Thus the fourth root of the recovered \(A^4\) is unique.

## 2.4 Moduli-image calculation

The exact differential witness proves that the projective Jacobian map has differential rank 24 at \(C_*\). Since the source chart has dimension 24, the map is generically finite onto a 24-dimensional embedded-quartic image.

The smooth-quartic projective stabilizer is finite. Therefore a generic projective orbit has dimension 15, and the invariant image has quotient dimension
\[
24-15=9.
\]

The manuscript's equivariance argument for finite projective-equivalence ambiguity is legitimate: a relation system mapping to a projectively equivalent quartic can be moved into the finite fibre over one chosen embedded quartic.

I do not see a dimension-theoretic error here.

## 2.5 Corank-two residual ideal

Under the admissibility hypotheses, the reduction to
\[
[L(T),CT^{(2)}]
\]
is structurally plausible: the injective \(\operatorname{Sym}^2H\) block can be eliminated, the mixed map has a one-dimensional rank-two kernel, and bases put the quotient mixed block in the displayed symmetrization form.

Modulo \(\delta\), the rank-one cone is the diagonal Segre ring. Requiring the image line of \(T\) to lie in one of four simple ramification directions imposes divisibility by the binary quartic \(h\). This gives the four degree-four lifts \(g_j\), and the linear minors contribute \(\delta\mathfrak m\).

The primary intersection
\[
(\delta)\cap\bigcap_iP_i^2\cap\mathfrak m^5
\]
then follows from the stated colon calculations. The nilradical-index-three conclusion is compatible with
\[
\delta^2\notin\delta J,\qquad
\mathfrak m\delta^2\subset\delta J,\qquad
\delta^3\in\delta J.
\]

The finite SymPy calculation is only a regression check at one split example, as the manuscript correctly states; the general proof is not being outsourced to the script.

## 2.6 Weighted determinantal formula

The coefficientwise rule
\[
\sum_ut^uf_u\in(t,I_j)^{(b)}
\Longleftrightarrow
f_u\in I_j^{(\max(b-u,0))}
\]
is consistent with the associated graded regular-local calculation.

Applying the classical one-factor symbolic-order formula coefficientwise yields the displayed weighted intersection. The revised text now correctly attributes the determinantal profile to the classical theory.

# 3. Blocker E123.1 — Ballico 1993 is still unresolved

This remains a straightforward top-four priority blocker.

The manuscript's own literature audit says:

- the complete Ballico 1993 article has not been read;
- the requested theorem-level crosswalk remains unfilled;
- no anticipation or non-anticipation conclusion is drawn;
- priority certification remains false.

The source is:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, *Mathematische Nachrichten* **163** (1993), 5–13, DOI 10.1002/mana.19931630102.

This is not a remote title coincidence. It sits directly in the historical failure-locus program to which the paper claims to contribute.

The revision is right not to infer novelty from lack of access. But a general top-four journal cannot decide priority on the basis “nearest predecessor not yet obtained.”

### Required action

Obtain and read the complete paper, then provide a theorem-by-theorem comparison covering at least:

1. the parameter space;
2. the precise multiplication/evaluation map;
3. the scheme structure used to define failure;
4. moving versus fixed linear systems;
5. higher-order/jet conditions;
6. nonreduced and embedded structure;
7. the relation to Fitting ideals;
8. the degree and global hypotheses;
9. what, if anything, survives after specializing to the cube-zero relation algebras used here.

Until this is done, the originality boundary of the *failure-scheme* part is not closed.

# 4. Blocker E123.2 — the nine-dimensional Reye/Enriques geometry is classical, and the new boundary is not isolated sharply enough

Revision 123 has improved its discussion of webs of quadrics, but the top-four priority analysis is still incomplete.

The manuscript itself proves that the bilinear incidence surface
\[
Z_R\subset\mathbf P^3\times\mathbf P^3
\]
is the ramification K3 \(Y_R\), and that transposition induces a fixed-point-free involution. It then explicitly places this construction in the classical web-of-quadrics / Enriques picture.

That is important, because a nine-dimensional family here is not historically surprising.

At minimum the following sources are unavoidable:

- F. R. Cossec, *Reye congruences*, *Transactions of the American Mathematical Society* **280** (1983), 737–751, DOI 10.1090/S0002-9947-1983-0716848-4;
- the classical Reye-congruence and nodal-Enriques literature summarized in modern form by I. Dolgachev and S. Kondō, *Enriques Surfaces II*, chapter “Reye Congruences,” 2025;
- C. Ingalls and A. Kuznetsov, *On nodal Enriques surfaces and quartic double solids*, *Mathematische Annalen* **361** (2015), 107–133.

Standard accounts explicitly describe the Reye-congruence locus as a nine-dimensional family, and modern accounts identify a general nodal Enriques surface with a Reye congruence.

Therefore the bare number
\[
\dim(\text{image})=9
\]
cannot itself carry novelty weight in this geometric setting.

I emphasize what I am **not** saying. I am not claiming that the paper's nilpotent reconstruction theorem is classical. I am not claiming that Cossec or the Enriques literature contains the failure-scheme Fitting ideal or the corank-two embedded component. I am saying that once the manuscript itself identifies its K3/involution with the classical construction, it must separate the classical nine-dimensional geometry from the genuinely new nonreduced-scheme theorem with much more precision.

### The missing crosswalk

A top-four version should compare, theorem by theorem:

1. the Grassmannian of four-dimensional relation spaces / webs of quadrics;
2. the bilinear incidence K3;
3. the free involution and Enriques quotient;
4. the classical moduli dimension of the Reye locus;
5. the source-Jacobian quartic polarization used here;
6. the relation between classical web equivalence and projective equivalence of \(R\);
7. whether generic finite ambiguity of \(R\) over the polarized K3 is already implicit in the classical parameterization;
8. if the generic degree is known classically;
9. exactly which information comes only from the nilpotent multiplication-failure scheme.

The current literature audit says that the “mere existence of a nine-dimensional web family” is not claimed as new. That is good, but it is not enough. Theorem 1.2 is one of the three headline theorems. The paper must tell the reader what theorem-level residue of 1.2 remains new after the classical Reye/Enriques theory is subtracted.

# 5. Blocker E123.3 — “higher-corank structure” is still only an admissible open calculation

Revision 123 crosses the first omitted stratum, but it does not classify it.

Theorem 1.3 applies only when:

- \(\gamma_R|_{\operatorname{Sym}^2H}\) is injective;
- the mixed map is surjective;
- its one-dimensional kernel is rank two;
- the pencil meets the ramification quartic in four distinct points.

These conditions define a nonempty open, and the manuscript proves that open is substantial.

But the excluded complement is precisely where the geometry becomes more singular:

- the kernel tensor can drop to rank one;
- the mixed map can lose rank;
- ramification roots can collide;
- the binary quartic can acquire multiple roots;
- the fixed-tensor corank can rise to three or four.

In a paper whose novelty is *embedded associated structure*, these exceptional loci are not a technical nuisance that can automatically be ignored. They are the places where new embedded primes, higher nilpotency, and nonreduced collisions are most likely to occur.

The title now advertises “higher-corank structure,” but the theorem gives “generic first higher-corank structure.”

That is a legitimate specialist theorem. It is not yet the natural closed theorem suggested by the title.

### Required action for top-four reconsideration

One of the following is needed.

1. **Complete the projection-corank-two stratification.** Classify the rank-one-kernel and multiple-root degenerations, including associated primes and nilpotency indices.

2. **Continue to all projection coranks in \(e=4\).** Give a finite stratification of the whole Schubert boundary and an intrinsic formula for the failure scheme on each stratum.

3. **Prove a global structural theorem.** For example, construct an intrinsic filtration of \(\mathcal O_{\widehat D}\) whose associated graded pieces are controlled by the ramification/contact data and whose generic corank-two formula specializes correctly to every boundary type.

Without such a result, “higher-corank” remains a first generic chart rather than a theory of the higher-corank boundary.

# 6. Blocker E123.4 — the two headline mechanisms are additive rather than unified

There is a conceptual disconnect in the current theorem architecture.

Theorem 1.1 says that the *whole* failure scheme \(\widehat D_R\) determines the polarized K3. But the proof obtains this by an intrinsic operation that discards the higher-corank part:

1. take the reduction of \(\widehat D_R\);
2. take its smooth locus;
3. restrict \(\widehat D_R\) to that locus;
4. recover the corank-one embedded support \(E_R\);
5. reconstruct the polarized K3 from \(E_R\).

Thus the singular higher-corank structure of \(\widehat D_R\) plays no role in polarized reconstruction.

Theorem 1.3, meanwhile, computes one generic higher-corank chart, but it is not used in Theorem 1.1 and does not strengthen its reconstruction conclusion.

The result is two good theorems sitting next to each other:

- a corank-one intrinsic reconstruction theorem;
- a generic corank-two primary-decomposition theorem.

A top-four paper would be much stronger if these were manifestations of one global structure.

### What would unify them

For example:

- a canonical nilpotent filtration on the entire \(\widehat D_R\);
- a global associated-support hierarchy indexed by projection corank;
- a theorem that recovers the polarized K3 and the ramification-contact stratification from successive annihilators of powers of the nilradical;
- a Rees/normal-cone description explaining both \(t(t,f)\) and the corank-two \(\delta J\) model as adjacent cases of one construction.

At present the whole-scheme statement is logically true, but “whole” contributes no more information to reconstruction than its intrinsic smooth-reduction restriction.

# 7. Blocker E123.5 — the moduli theorem is computationally valid but conceptually thin for a top-four headline

The exact 25-by-25 determinant is a perfectly legitimate proof that one differential has full rank.

The problem is one of theorem scale.

The key statement
\[
\dim\operatorname{im}(R\mapsto[Y_R,A_R])=9
\]
ultimately rests on:

1. an explicit chart;
2. one explicit integer matrix;
3. one nonzero large determinant;
4. the subtraction \(24-15=9\).

This proves the dimension. It does not explain the deformation map.

Given that the target nine-dimensional locus is tied to the classical Reye/Enriques geometry, a top-four paper should provide a structural infinitesimal description:

- identify the differential in cohomological terms;
- identify its kernel with infinitesimal projective equivalences;
- compare the tangent space with deformations of the Enriques quotient or the K3 with involution;
- or derive generic finiteness from a geometric Torelli/period argument.

An exact rank certificate is valuable verification. It is a weak conceptual substitute for understanding why the map has the expected rank.

If the authors want Theorem 1.2 to remain a headline theorem, it should be upgraded from “one point has full-rank Jacobian” to “the deformation map is generically injective for a geometric reason.”

# 8. Major issue M123.1 — generic finite ambiguity is not yet a Torelli-type classification

Theorem 1.1 plus Theorem 1.2 gives:

\[
D_R
\rightsquigarrow
(Y_R,A_R)
\rightsquigarrow
\{\text{finitely many projective classes of }R\}
\]
for a general polarized point in the image.

This is a significant improvement over revision 122.

But the inverse problem remains only partially solved.

The manuscript does not determine:

- the generic number of projective classes of \(R\);
- whether the generic map is birational onto its image;
- whether distinct \(R\)'s in a general fibre yield isomorphic or nonisomorphic failure schemes;
- the geometry of the exceptional positive-dimensional fibres;
- the quadratic morphism \(\phi_R\) from the failure scheme;
- a canonical choice of the relation tensor among the finite possibilities.

At top-four level, “finite ambiguity” is often the beginning of a Torelli-type theorem rather than its endpoint.

A particularly strong revision would compute the generic degree or prove generic injectivity. Even a precise monodromy description of the finite fibre would materially raise the conceptual content.

# 9. Major issue M123.2 — the nonreduced reconstruction mechanism needs its own literature comparison

The strongest genuinely new-looking object is not the K3 surface itself. It is the way the polarization is extracted from the nilpotent multiplication-failure scheme:
\[
\mathcal L
=
\omega_E\otimes\mathcal N^{-(p+e-1)}.
\]

The current bibliography compares:

- determinantal primary decomposition;
- webs of quadrics / Enriques surfaces;
- standard K3 moduli;
- MRC cancellation.

It does not give a comparable survey of reconstruction from nonreduced schemes, multiple structures, ribbons/ropes, or canonical line bundles built from conormal/nilradical data.

I do not assert that an existing theorem subsumes the present construction. The point is the opposite: if this determinant-line cancellation is the genuinely novel mechanism that survives the classical web-of-quadrics comparison, then the paper should make that case against the literature closest to *that* mechanism.

At top-four level the novelty audit must follow the new theorem, not only the ambient classical geometry.

# 10. Major issue M123.3 — globalize the corank-two associated support, not only its étale-local primary factors

The manuscript is appropriately careful that the four \(P_i\) may permute under monodromy and therefore should not be advertised as four global irreducible components.

However, the new intrinsic object
\[
\operatorname{Ann}(\widehat{\mathcal N}^2)
\]
deserves a global theorem.

At present the corank-two section tells me that, on the admissible open, the rank-two stratum is recovered locally as the annihilator support of \(\widehat{\mathcal N}^2\), and that the square is an invertible module there.

A stronger formulation should identify:

1. the global admissible corank-two support \(\Sigma_R\) as a scheme;
2. its class/codimension inside the Schubert singular locus;
3. the line bundle represented by \(\widehat{\mathcal N}^2|_{\Sigma_R}\);
4. the branch divisor where the four ramification lines collide;
5. the monodromy of the four branches;
6. how the local \(\mathfrak m^5\) component glues globally.

This would turn a strong local computation into a geometric theorem.

# 11. Major issue M123.4 — the classical incidence section should identify the exact Reye object, not only say that the construction is classical

Section 7 is an improvement, but its current message is still qualitative:

- the bilinear incidence K3 is classical;
- the free involution is classical;
- the web discriminant and source Jacobian live in different projective spaces;
- the new invariant comes from the failure scheme.

For a specialist reader in Enriques geometry, that is not enough.

The paper should state precisely:

- what Enriques surface is obtained as \(Y_R/\langle\iota\rangle\);
- whether it is the standard Reye congruence attached to the same web \(R\);
- how the quartic polarization \(A\) relates to the classical Enriques/K3 polarization lattice;
- which lattice polarization characterizes the nine-dimensional image;
- whether the image equals the general Reye locus, an open subset of it, or a finite cover of it.

Once this is done, the period/moduli theorem may become conceptual rather than certificate-driven.

# 12. Major issue M123.5 — the 16-page principal article is cleaner, but the archival companion should not be confused with the journal object

The repository now has a good distinction:

- geometry.pdf: 16-page principal article;
- paper.pdf: 147-page complete archival companion preserving the prior 130-page manuscript.

For review, this is manageable.

For submission, however, there must be exactly one mathematical object whose claims are being refereed. Historical preservation is a repository concern, not a journal-article theorem.

I recommend:

- submit the 16-page article (expanded only where the present proofs are too compressed);
- keep the 147-page companion as archival supplementary material;
- do not make preservation of prior revisions part of the mathematical case for publication;
- make every theorem in the principal article independently referenceable without requiring a referee to reconstruct the version history.

# 13. Exact computations and reproducibility

The computational record is unusually careful and should be retained.

The revision correctly distinguishes finite verification from proof certification.

The exact K3 script checks:

- the 25-column differential rank;
- basepoint-freeness through a full-degree Macaulay rank;
- quartic smoothness through a Jacobian-ideal Macaulay rank;
- the explicit corank-two witness;
- the binary-quartic discriminant.

The corank-two regression script checks one split-root instance of the primary formula and the nilpotency index.

These are meaningful guards against transcription errors.

They do **not** prove:

- the general coefficient-ring cone lemma;
- the global primary decomposition;
- the literature priority claims;
- the global moduli identification.

The manuscript's current false certification flags correctly reflect this distinction. They should remain false unless independent formal work actually changes that status.

# 14. Required package for top-four reconsideration

I would not recommend another revision whose main change is more exact certificates or more formal corollaries. The remaining work is structural.

A credible top-four reconsideration would need most of the following.

## E123.1 — close the Ballico source

Read Ballico 1993 in full and add the completed theorem-level crosswalk.

## E123.2 — close the Reye/Enriques priority boundary

Read and compare the classical primary sources, especially Cossec's Reye-congruence work and the modern Enriques treatment, and state exactly which part of Theorem 1.2 is new after classical moduli theory is removed.

Do not use “nine-dimensional” itself as a novelty signal.

## E123.3 — complete the higher-corank boundary or produce a global structural replacement

At minimum classify the exceptional projection-corank-two degenerations. Preferably give a stratified theorem on the entire higher-corank locus.

## E123.4 — unify reconstruction and higher-corank structure

Construct a global intrinsic filtration or normal-cone/Rees mechanism from which both the corank-one polarization theorem and the corank-two embedded component emerge.

## E123.5 — replace the one-point rank certificate by a conceptual deformation theorem

Identify the tangent map geometrically or cohomologically and relate it to the classical Reye/Enriques moduli locus.

The exact determinant can remain as a reproducibility check.

## E123.6 — strengthen finite ambiguity

Compute the generic degree, prove generic injectivity, or otherwise describe the finite fibre and its monodromy.

## E123.7 — audit the genuinely new nilpotent reconstruction mechanism against the relevant nonreduced-scheme literature

If the main novelty is the intrinsic line
\[
\omega_E\otimes\mathcal N^{-9},
\]
make that novelty case explicit and complete.

# 15. Final assessment

Revision 123 is the strongest A2 version I have reviewed.

The previous report's mathematical blockers were not ignored. The authors have added real theorems:

- a section-ring reconstruction of the quartic polarization;
- a genuine K3-moduli variation statement;
- a fixed-tensor projection-corank-two primary decomposition;
- an intrinsic nilradical-square support;
- and a proper classical determinantal attribution.

I found no basis to call these additions vacuous or formally false.

But the standard requested is not “is there now a serious theorem?” The standard is one of the four most selective general mathematics journals.

At that level, the manuscript still has an unresolved nearest historical source; it sits on a classical nine-dimensional Reye/Enriques geometry whose exact overlap with the new moduli theorem is not yet pinned down; its higher-corank theorem is generic rather than complete; and its two strongest mechanisms have not yet been synthesized into one global structure.

The right next revision is therefore not another incremental patch.

It should decide what the paper's deepest theorem is after all classical geometry is subtracted, and then prove that theorem in its natural global scope.

**Recommendation: reject in the present form at a general top-four mathematics journal. I would encourage a substantive mathematical revision, and I would regard the current core as potentially publishable in a strong specialist venue if the remaining priority questions are closed.**
