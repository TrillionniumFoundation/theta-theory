# Second independent harsh referee report — A2 revision 144

## Manuscript and immutable review object

**Manuscript:** *Finite failure schemes and the reconstruction of quadratic pencils*  
**Author:** Qian Qi  
**Revision reviewed:** A2 revision 144  
**Revision branch:** revision/a2-v144-referee-integrated-reconstruction-2026-09-24  
**Exact revision-branch head used to create this review branch:** 542bcd5027e96ca41568f3eb9c3481dc0f296fed  
**Immutable mathematical source recorded by the revision:** fb4e7c4d00167e422fdb7ee73876a74f6649fb68  
**Immediate mathematical predecessor:** 40ef003998cbeb20f418e1b5e0dcfa9cfef9416d (v143)  
**Controlling earlier referee report recorded by v144:** 3afecca5e65d7fe9c6784020ea6e813122938140  
**Earlier independent v144 review branch:** review/a2-v144-independent-harsh-top4-2026-09-24  
**Review standard:** external-referee-style assessment at the level of *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is a second owner-requested, AI-assisted independent referee-style report. It is not a journal-commissioned editorial decision. I have treated the immutable source SHA above, rather than a movable branch name, as the mathematical object under review.

The v144 source lock records a 33-page principal article, a 102-page supplement, and a 130-page complete compilation. The build receipt records 415 current mathematical labels, 282 inherited mathematical blocks, twenty executed exact/symbolic scripts, and a successful native build. I inspected the principal inverse/spectral/critical chain in detail, including the intrinsic rank-one ruling argument, coefficient reconstruction, all-pencil theorem, sharp finite-neighbourhood theorem, universal relative neighbourhood, spectral readout, fixed-spectral specialization, real likelihood theorem, reconstructed critical correspondence, and the new projective critical-divisor/ramification section. I also read the current response, issue matrix, source lock, literature audit, build receipt, the relevant earlier referee report, and the rank-one Fano-scheme lemma supporting the intrinsic orientation argument.

I did **not** formally verify every inherited result in the 102-page supplement, and the repository's scripts do not amount to such a verification. My recommendation below therefore distinguishes proof-level findings on the principal chain from editorial claims about the complete 130-page object.

## Recommendation

**Reject in the present form for a general top-four mathematics journal.**

This recommendation should not be misread as a claim that the central v144 theorem is false. On the contrary, after a deliberately hostile rereading, I do **not** currently see a fatal proof-level defect in the sharp finite reconstruction theorem, the universal relative-neighbourhood theorem, the spectral-sheaf reconstruction, or the new v144 projective critical-divisor theorem. Several technical issues that were serious in earlier revisions are now genuinely repaired.

The rejection is nevertheless firm. At top-four level the remaining problems are no longer ordinary local-proof repairs. They are structural.

1. **The closest identified historical predecessor, Ballico 1993, is still not compared at theorem level.** The manuscript itself admits this. Because the headline object is a nonreduced multiplication-failure scheme and the historical paper is explicitly about failure loci of higher-order embedding properties, the central novelty boundary cannot responsibly be certified without the actual theorem/proof text.
2. **The top-four significance case for the main invariant remains under-calibrated.** In fixed tensor coordinates, the order-\(d\) relation-space map factors through the Pluecker embedding and a fixed linear coefficient inclusion. This is mathematically clean but makes clear that a substantial portion of the parameter theorem is an encoding theorem for a deliberately constructed cube-zero quotient. The genuinely difficult part is the unmarked intrinsic recovery of the tensor orientation and Pluecker line. The paper must make that conceptual point sharper and show why it has reach beyond this engineered family.
3. **The complete publication object is still not a coherent single paper.** A 33-page principal article accompanied by a 102-page supplement containing active, fully proved web, contraction, K3, polar, boundary, and degeneration theorem clusters is not a conventional technical supplement. It is a multi-paper research program packed into one submission.
4. **The new v144 critical-divisor theorem is sound-looking but does not resolve the preceding two problems.** Once the split semisimple score form is available, the finite-flatness and ramification argument is relatively elementary one-variable algebra on a projective line. It is a useful continuation, not a substitute for closing the novelty audit or defining the publication object.
5. **Several large “classification of all specializations” claims rely on classical symmetric-space orbit theory more heavily than the current citation precision acknowledges.** This does not presently look false, but a top-four paper should pin those inputs to exact theorem statements and hypotheses rather than citing a section, page, and nearby formula.

In other words: v144 has moved from “possibly structurally unsound” to “mathematically serious but not yet top-four-certifiable.” That is real progress, but it is not acceptance.

---

## 1. The sharp finite reconstruction theorem survives a hostile proof audit

The core local computation is

\[
I_{\widehat D_R}=(\det T)\,I_p(\gamma_R\operatorname{Sym}^2T),
\qquad
p=\binom{n+1}{2}-2,
\]

near the socle Grassmannian. Every generator has degree

\[
d=n+2p=n^2+2n-4.
\]

This factorization does two different jobs, and the manuscript now keeps them separate.

First, it explains formally why every lower ideal-adic neighbourhood is independent of the pencil: there are no relations before degree \(d\). Second, and much less formally, the degree-\(d\) relation space must be recovered from an **abstract unmarked finite scheme** and decoded back to the pencil.

That second step is the actual theorem. I rechecked the sequence:

- the reduction of the order-\(d\) thickening is the socle Grassmannian \(B\);
- the nilradical recovers the degree-one conormal bundle;
- multiplication in the finite algebra recovers the degree-\(d\) kernel;
- because the normal-cone ideal is generated in that degree, the complete graded normal cone is recovered;
- the reduced determinant cone inside that normal cone has an intrinsic rank-one locus;
- its Fano scheme of maximal linear rank-one spaces has exactly two components;
- the projectively trivial component gives the \(V\)-ruling, while the tautological ruling is detected as nontrivial on a Schubert line;
- this orientation forces one constant projective coordinate transformation on \(V\), rather than unrelated transformations over different points of \(B\);
- determinant cancellation recovers the residual coefficient module;
- for pencils, \(\bigwedge^2\operatorname{Sym}^2V\cong\mathbb S_{(3,1)}V\) is irreducible, so there is only one left coefficient line;
- exterior duality identifies that line with the Pluecker line of \(R\).

I do not presently see a circular use of the ambient tensor presentation in the unmarked part of this argument. The proof does not assume that an abstract isomorphism of finite neighbourhoods extends to the ambient Grassmannian. That distinction matters and is now handled correctly.

### 1.1 The rank-one Fano-scheme lemma is not merely set-theoretic

A previous vulnerability would have been to identify the two rulings only on closed points and silently ignore infinitesimal structure. The current lemma does more.

At a point \(\ell\otimes F\), the tangent calculation reduces each component of a Grassmannian tangent vector to an operator \(A:F\to F\) satisfying

\[
u\wedge A(u)=0.
\]

Polarization forces \(A\) to be scalar. Hence the tangent space has the expected dimension \(n-1\), and the two evident projective families already have that dimension. The resulting local rings are regular; over \(\mathbb C\) this eliminates nilpotent or embedded thickening. The argument is then spread to arbitrary complex bases by equation-level base change.

I find this adequate for the advertised purpose.

### 1.2 The descent to one constant projective transformation is also adequate

The manuscript uses that an isomorphism of the trivial projective-space rulings gives a morphism

\[
B\longrightarrow \operatorname{PGL}(V),
\]

and that \(\operatorname{PGL}(V)\) is affine while \(B\) is connected projective with \(H^0(B,\mathcal O_B)=\mathbb C\). The morphism is therefore constant.

This is precisely the step that prevents the reconstruction from degenerating into fibrewise coefficient recovery with uncontrolled gauge. It is conceptually one of the strongest parts of the proof.

I do not regard this point as open.

---

## 2. The meaning of “sharp” is now mostly correct, and it must remain so

The theorem proves that \(d=n^2+2n-4\) is the **smallest uniform order** that classifies all pencils. It does so because:

- all orders \(k<d\) are independent of \(R\); and
- at order \(d\), every pencil is recovered.

That does **not** mean that for every inequivalent pair there is a meaningful pair-specific hierarchy of different lower orders and that both members “first separate exactly at \(d\)” for some independent reason. The reason is stronger and simpler: no pencil information exists at all below \(d\) in this ideal-adic filtration.

The current source is generally careful about this. It should stay careful. “Smallest uniform reconstruction order” is the right global formulation.

The conceptual content is not the integer \(d\) by itself. The integer is largely forced by the degrees in the Fitting factorization. The conceptual content is that the **abstract unmarked** order-\(d\) thickening intrinsically recovers the tensor orientation and the relation plane.

---

## 3. The fixed-coordinate parameter theorem is correct-looking but should not be oversold

The closed immersion

\[
\Phi:\operatorname{Gr}(2,\operatorname{Sym}^2V)
\longrightarrow
\operatorname{Gr}\!\left(M,\operatorname{Sym}^dH^*\right)
\]

is cleanly proved. But the proof itself shows why its significance must be calibrated.

The relation space is

\[
K_R=\nu\bigl(\mathbb C\beta_R\otimes F(U)\bigr),
\]

where \(\nu\) is one fixed injective linear map and the map

\[
R\longmapsto \mathbb C\beta_R
\]

is, after exterior duality, exactly the Pluecker embedding of the pencil Grassmannian.

Thus the fixed-coordinate parameter theorem factors through:

1. the classical Pluecker embedding;
2. the elementary closed immersion \(\ell\mapsto \ell\otimes F(U)\);
3. one fixed linear inclusion.

That is a good theorem to have because it supplies family-level faithfulness and base change. It is not, by itself, evidence of a new deep moduli phenomenon. It is a precise encoding statement.

For a top-four submission, the paper should therefore stop treating every formal consequence of this closed immersion as another independent major theorem. The genuinely nonformal contribution is the passage from the **unmarked finite failure scheme** back to the oriented coefficient line.

This distinction is currently visible in the proofs but not sufficiently reflected in the significance narrative.

---

## 4. The universal finite neighbourhood is now a genuine relative theorem

Theorem on the universal order-\(d\) neighbourhood is one of the repairs I accept.

The source gives a coordinate-free relation-bundle morphism

\[
\det V^*\otimes\det\mathcal U\otimes\det\mathcal S^*
\otimes\bigwedge^p\operatorname{Sym}^2\mathcal U
\longrightarrow
\operatorname{Sym}^d\mathcal E^*,
\]

whose image is a rank-\(M\) subbundle. On frame charts this is the fixed coefficient inclusion, and the determinant character matches the change of graph coordinates. Therefore the ideals glue in the **actual graph neighbourhood** of the relative socle.

Quotienting by the \((d+1)\)-st power of the zero-section ideal gives the actual relative ideal-adic neighbourhood, not just a collection of fibrewise isomorphic truncated algebras.

The manuscript also correctly warns that over a nonreduced base the specified relative socle ideal need not equal the absolute nilradical, since the base itself may contribute nilpotents.

These points were previously dangerous. In v144 they are stated at the right level.

The conclusion “finite locally free over the relative socle, projective and flat over the pencil parameter scheme, compatible with arbitrary complex base change” is credible: finite locally free followed by the smooth projective socle Grassmannian gives flatness and projectivity of the composite.

---

## 5. Spectral reconstruction is a legitimate consequence, not a second Torelli miracle

The spectral torsion sheaf

\[
0\to V^*\otimes\mathcal O(-1)
\to V\otimes\mathcal O
\to \mathcal T_R\to0
\]

encodes the similarity class of \(A^{-1}B\) on an affine chart. The manuscript now explicitly proves this through the module \(\operatorname{coker}(zI-C)\), rather than hiding it behind a classical-classification citation.

The polynomial square-root lemma is also adequate over \(\mathbb C\): an invertible operator admits a polynomial square root by truncated local binomial series and Chinese remaindering. This is enough to pass from similarity to congruence for the symmetric pencil.

I accept the conclusion that, for regular pencils, the order-\(d\) invariant recovers the full root-labelled spectral torsion sheaf, including nonsemisimple elementary-divisor data.

The scheme-theoretic incidence construction using

\[
I_{n-h+1}\bigl((C-zI)^a\bigr)
\]

is also natural. The truncated-module lemma is elementary and base-change compatible. It correctly recovers local length profiles rather than merely reduced support or corank.

The paper should nevertheless present this as a **readout of a reconstructed pencil**, not as a logically independent Torelli theorem of comparable depth. Once the pencil is reconstructed, much of the spectral conclusion is classical linear algebra plus Fitting theory.

---

## 6. The fixed-discriminant classification needs more exact historical anchoring

The fixed-discriminant/fixed-reduced-rank section is mathematically plausible and useful. It packages:

- orthogonal orbits of self-adjoint nilpotents;
- their partition labels;
- the orbit dimension formula;
- dominance closure order;
- curve realization of every allowed specialization;
- transport through the finite-neighbourhood family.

The manuscript cites Trevisiol and correctly warns that full orthogonal orbits need not be connected. That warning is important: in even dimension, a full \(O(n)\)-orbit can be disconnected even though the partition still labels it.

My concern is not that the theorem is evidently wrong. My concern is that the citation burden is too loose for the strength of the packaged statement. A sentence such as “these are the statements in §1, p. 3, equation (2) and the following dominance criterion” is not enough for a top-four submission when the paper then asserts an “if and only if” classification of **every** admissible specialization.

The revision should isolate a precise classical lemma with exact source locations proving, for the orthogonal symmetric space \((\mathfrak{gl}_n,\mathfrak{o}_n)\):

1. parametrization of full \(O(A)\)-orbits by partitions;
2. the exact orbit-dimension formula used here;
3. closure order by dominance for the full orthogonal action;
4. the relation, if any, between the disconnected full \(O\)-orbit and its \(SO\)-components.

Then the paper can prove the family/curve consequences from that lemma.

This is not a fatal mathematical objection at present, but it is a top-four-level documentation requirement.

---

## 7. The real likelihood theorem does match the cited conjecture

I independently checked the formulation of Fevola–Mandelshtam–Sturmfels, Conjecture 4.5 in *Pencils of Quadrics: Old and New* (arXiv:2009.04334v2). The conjecture asks, for a definite pencil with \(r\) distinct eigenvalues, for the existence of a real data vector \(s\in\mathbb R^n\) such that the reciprocal log-likelihood has \(2r-3\) distinct real critical points.

It does **not** require the data matrix to be positive definite.

The manuscript's theorem therefore addresses the advertised scope rather than weakening the conjecture through an unstated positivity change. The separated-root construction with

\[
\sigma_i=\frac{Q(\alpha_i)}{D'(\alpha_i)}
\]

and roots \(\beta_j>\alpha_r\) gives the required sign alternation. The degree count then exhausts all \(2r-3\) roots, proving they are real and simple.

I do not see a gap in the elementary root-count argument.

### Editorial problem

This theorem is nevertheless almost logically independent of the finite-failure reconstruction. The reconstruction theorem is not needed to prove the real-root statement. Conversely, the real-root statement is not needed to prove the finite-reconstruction theorem.

The current manuscript uses a later critical-correspondence theorem to connect them functorially, which is mathematically legitimate. But a functorial bridge does not automatically turn two independent theorem clusters into one top-four paper.

This result may be excellent material for a companion paper or a sharply delimited applications section. It should not function as significance ballast for the central failure-scheme theorem.

---

## 8. The new v144 projective critical divisor is mathematically coherent

The genuinely new v144 section starts on the split semisimple spectral-data open where:

- the spectral values \(\alpha_i\) are pairwise distinct;
- the projectors are supplied over nonreduced bases;
- the binary polynomial \(Q_h\) has simple projective zeros;
- these zeros are disjoint from the spectral poles;
- the discriminant of the **score** polynomial is *not* inverted.

The projective one-form is

\[
\omega
=
\sum_i(n-m_i)\,d\log L_i
-
n\,d\log Q_h.
\]

Homogeneity gives

\[
\eta=G(x,y)(x\,dy-y\,dx)
\]

for a binary form \(G\) of degree \(2r-3\).

I checked the main pieces of the proof.

### 8.1 Disjointness from poles

At a zero of \(L_i\), the logarithmic residue is \(n-m_i\). At a zero of \(Q_h\), it is \(-n\). These are nonzero in characteristic zero, and the poles are simple and disjoint on the chosen base. Therefore \(G\) does not vanish at a pole in any geometric fibre.

The scheme-theoretic conclusion is valid: a nonempty intersection would have a point and hence a geometric point in some fibre. There is no mysterious nilpotent-only intersection with empty support.

### 8.2 Finite local freeness

At a point of the base, one can choose a constant \(\mathbb Q\)-rational point of \(\mathbb P^1\) outside the finite zero set of the fibre of \(G\). After shrinking, evaluation there is a unit. A constant projective transformation sends that point to infinity, and the remaining affine equation becomes monic of degree \(2r-3\).

Hence the local algebra is free on

\[
1,t,\ldots,t^{2r-4}.
\]

This proves finite local freeness through critical collisions.

The manuscript should make the \(\mathbb Q\)-rational-point sentence explicit. “The residue field has characteristic zero” is enough only after one observes that it contains the prime field \(\mathbb Q\), providing infinitely many constant points.

### 8.3 Identification with the original two-score scheme

Writing \(K=\lambda K_0(t)\), the radial score gives

\[
\lambda=\frac{U_0(t)}n.
\]

The tangential score after elimination is exactly the projective one-form above. Because the projective divisor is disjoint from both \(D_h\) and \(Q_h\), every denominator used in this elimination is a unit in the critical algebra.

The inverse formula

\[
K=\frac{U(K_0)}nK_0
\]

is invariant under rescaling \(K_0\), so it glues projectively.

This is stronger than a point count and appears correct scheme-theoretically, including nilpotents.

### 8.4 Ramification and Hessian degeneracy

For a local monic presentation

\[
A=\mathcal O[t]/(g),
\]

one has

\[
\Omega_{A/\mathcal O}=A\,dt/(g'dt),
\]

so the ramification Fitting ideal is \((g')\). The eliminated tangential score is a unit times \(g\), and its derivative modulo \(g\) is therefore a unit times \(g'\). Since the radial Hessian entry is a unit, the Hessian determinant generates the same ideal.

This is the right statement.

I recommend adding the explicit coordinate-change formula: on the critical quotient, all terms involving first derivatives vanish, so under a smooth change of variables the Hessian transforms as \(J^{\mathsf t}HJ\); hence its determinant changes by a square of a Jacobian unit. The current text states the conclusion but one more line would make the nilpotent setting completely transparent.

### 8.5 Trace discriminant

For a monic algebra, the trace-pairing determinant is the polynomial discriminant. Projective coordinate changes alter the binary discriminant by a unit on the local base. The base-change statement is therefore credible for this finite locally free monogenic family.

The manuscript appropriately avoids claiming that the trace-discriminant divisor is the scheme-theoretic image of ramification with matching multiplicities.

### 8.6 Triple collision

For the fixed three-dimensional pencil in the example,

\[
D(t)=t(t^2-1),\qquad Q(t)=t^2+c,
\]

and the displayed score polynomial reduces to

\[
F(t)=-(6c+4)t^2+2c.
\]

Its projective cubic has discriminant

\[
64c(3c+2)^3.
\]

At \(c=-2/3\), the local algebra is \(\mathbb C[u]/(u^3)\), so the length-three collision and ramification ideal \((u^2)\) are consistent with the theorem.

I therefore do not identify a new fatal error in the v144 mathematics.

---

## 9. But the v144 critical-divisor theorem is not itself a top-four-level cure

The new theorem is useful, but its proof reveals its level.

Once the split semisimple score differential has been reduced to one binary form \(G\) on \(\mathbb P^1\), the essential new assertions are consequences of:

- a relative effective Cartier divisor of fixed degree;
- a local monic presentation;
- the elementary formula for relative differentials of \(\mathcal O[t]/(g)\);
- the classical trace discriminant.

The nontrivial point is that the score construction is functorially attached to the reconstructed pencil, not the one-variable algebra by itself.

This distinction matters editorially. Adding the finite-flat critical divisor does not compensate for an unresolved novelty audit on the headline reconstruction theorem. Nor does it justify retaining every independent result in the supplement.

If this section stays in A2, it should be presented as a concise structural continuation of the principal inverse chain. If it is advertised as another independent headline novelty, the paper becomes even less architecturally coherent.

---

## 10. The Ballico 1993 comparison remains an absolute novelty blocker

The manuscript identifies:

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Math. Nachr. 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

The v144 literature audit is admirably explicit that the full theorem text has not been obtained and that no theorem-level nonanticipation claim is being made.

I independently checked the publisher record during this review. The public Wiley route confirms the bibliographic record and article pages, but the accessible endpoint did not yield the theorem/proof text required for a six-axis mathematical comparison. I therefore also make **no** claim that Ballico 1993 anticipates the present theorem, and **no** claim that it does not.

That uncertainty is itself disqualifying for a top-four novelty certification.

The relevant comparison must answer, from the actual 1993 text:

1. What parameter space is varied?
2. What exact multiplication/evaluation map defines the failure locus?
3. Is the object only a support/reduced locus, a Fitting scheme, or a full nonreduced scheme?
4. Are infinitesimal neighbourhoods or nilpotent structures retained?
5. Is there a relative/base-change construction?
6. Is there any inverse statement reconstructing the original linear system, embedding, map, or coefficient data from the failure object?

The paper should quote theorem numbers and hypotheses and explain the comparison at the level of constructions, not titles.

The inspected 1996 Ballico paper is useful background and the current six-axis table for it is a real improvement. It does not discharge the 1993 obligation.

Until the 1993 paper has been read, I would not certify the central result as meeting a top-four novelty threshold.

---

## 11. The central significance question is still unresolved even if Ballico 1993 is favorable

Suppose the 1993 comparison eventually shows no inverse theorem and no comparable nonreduced neighbourhood reconstruction. Even then, the authors still need to make a stronger case for why the present inverse theorem belongs at the very top of the subject.

The construction starts from a deliberately tailored cube-zero algebra

\[
A_R=\mathbb C\oplus V\oplus(\operatorname{Sym}^2V/R),
\]

and then studies failure of a multiplication map whose degree-\(d\) coefficient space explicitly retains the quotient-volume line dual to \(R\).

In fixed coordinates, the parameter immersion is essentially the Pluecker embedding passed through a fixed representation-theoretic inclusion.

The theorem is **not tautological**, because the invariant is then stripped of its marking and the paper proves that the abstract nonreduced scheme intrinsically recovers the hidden tensor orientation and coefficient line. That is the difficult point.

But top-four significance requires the paper to articulate a principle broader than “this carefully designed nonreduced scheme remembers the data that created it.” For example, one would want one of the following:

- a general intrinsic reconstruction theorem applying to a broad class of multiplication-failure schemes;
- a conceptual characterization of when nonreduced degeneracy loci recover defining maps;
- a moduli-theoretic consequence not already formal from the Pluecker embedding once coordinates are retained;
- a genuinely new geometric application that depends essentially on the unmarked reconstruction mechanism.

The current structural coefficient criterion moves in this direction, but most of the surrounding theorem volume consists of specializations, formal readouts, or independent applications.

A top-four paper cannot win the significance case by accumulation of theorem count.

---

## 12. The 102-page supplement is still a publication-object failure

The source lock records:

- principal article: 33 pages;
- supplement: 102 pages;
- complete compilation: 130 pages;
- 415 mathematical labels;
- 282 inherited mathematical blocks.

The supplement actively retains full results and proofs on:

- four-dimensional web reconstruction;
- all-rank exterior contraction and Jacobian–Casimir identities;
- polarized and polar constructions;
- K3 geometry;
- hyperelliptic interpretations;
- boundary atlases;
- corank and primary-structure calculations;
- degeneration and specialization results.

The principal article explicitly says several of these are **not inputs** to the pencil theorem.

That statement improves logical clarity but makes the editorial problem sharper: if they are not inputs, why is a referee of the pencil paper responsible for certifying all of them as part of the same 130-page mathematical object?

Calling them a supplement does not solve the problem. A supplement is usually material needed to support the paper, not a warehouse for several adjacent research programs.

I am **not** recommending deletion of mathematics. I am recommending a publication architecture:

- A2 should contain the finite-failure reconstruction spine and only those consequences that illuminate that spine.
- The web/contraction/K3/boundary clusters should become companion papers or separately reviewable archival manuscripts, with precise cross-references.
- If the authors insist they belong together, they need a theorem-level explanation of why the clusters form one indivisible conceptual result.

At present, the complete object remains unreviewable at top-four standards without effectively commissioning several referee reports under one title.

---

## 13. The contraction theorem still has an unresolved role

The supplement retains an all-rank contraction theorem, an exact kernel statement, singular values, and a Jacobian–Casimir factorization. The manuscript now does a better job distinguishing classical harmonic ingredients from the specific normalized map it studies.

However, its editorial role remains unstable.

If the contraction theorem is merely support for the web branch and is irrelevant to the principal pencil theorem, then it should not be used as a major reason why A2 as a whole deserves a top-four venue.

If it is a major independent significance pillar, then its map-specific historical priority must be settled at the same level demanded for the failure-scheme theorem.

The paper cannot simultaneously minimize the theorem when priority is questioned and maximize it when significance is argued.

This is another reason to split the research program into reviewable units.

---

## 14. The provenance and regression discipline are excellent, but they must stay epistemically modest

The v144 repository records unusually strong engineering discipline:

- immutable source SHA;
- preserved predecessor archive;
- byte-identical inherited part/check files;
- preserved inherited theorem/proof/equation blocks;
- native PDFs;
- no unresolved labels or duplicate labels in the recorded build;
- twenty executed exact/symbolic scripts;
- source-bound hashes and receipts.

This is valuable. It makes review much easier and substantially reduces accidental regression risk.

It does **not** certify:

- the truth of all 415 labelled mathematical assertions;
- correctness of every inherited proof;
- exhaustive historical priority;
- top-four significance;
- equivalence of unmarked moduli stacks.

The current README and receipt already say this. That restraint should remain.

In particular, phrases such as “exact regression” should continue to mean exact verification of the finite identities actually encoded in a script, not formal verification of the geometric argument surrounding them.

---

## 15. Specific required revisions

Even if the major novelty and architecture problems are addressed, I would require the following local changes.

### 15.1 Expand the characteristic-zero rational-point step

In the finite-flat proof of the projective critical divisor, state explicitly:

- a characteristic-zero residue field contains \(\mathbb Q\);
- the nonzero binary form \(G\) has only finitely many zeros in the fibre;
- hence some point of \(\mathbb P^1(\mathbb Q)\) avoids them;
- evaluation is a unit after shrinking the base.

This removes an unnecessary ambiguity in the nonreduced-base argument.

### 15.2 Write the Hessian coordinate-change formula

Do not merely say the determinant changes by a square of a unit. State that under a smooth coordinate change,

\[
H' = J^{\mathsf t}HJ + \sum_a (\text{first score})_a \cdot (\text{second derivatives of the change}),
\]

and the second term vanishes in the critical quotient. Then the Hessian ideal is manifestly intrinsic even with nilpotents.

### 15.3 Pin the symmetric-nilpotent orbit input to exact theorems

Give exact theorem/proposition numbers for orbit parametrization, dimension, and closure order, and explain how disconnected full orthogonal orbits are handled.

### 15.4 Keep three different family statements distinct

The paper must continue to distinguish:

1. unmarked reconstruction over complex geometric objects;
2. framed first-relation families and the closed immersion into a Grassmannian;
3. relative constructions with the socle and split spectral data retained.

These are not interchangeable moduli statements.

### 15.5 Keep the domains of validity visible in every summary

The hierarchy is:

- **all complex pencils:** finite reconstruction;
- **regular pencils:** spectral torsion and critical correspondence;
- **split semisimple spectral data with simple/disjoint \(Q_h\)-poles:** projective finite-flat critical divisor;
- **supplied real definite realization plus separated real data:** totally real finite etale cover.

The abstract and talks should not compress this into one unconditional sentence.

### 15.6 Do not identify reduced rank data with full Fitting data

The fixed-discriminant examples are interesting precisely because reduced rank loci stay fixed while higher Fitting/spectral length data change. This distinction is currently correct and must remain explicit.

### 15.7 Preserve the sharpness qualifier

Continue to say “smallest uniform order.” Do not upgrade it to pairwise minimality, a universal local Artin statement, or an unmarked moduli-stack equivalence.

---

## 16. Minimum conditions before I would support a fresh top-four review

A new version should not merely append another theorem. It should close the following items.

1. **Obtain Ballico 1993 and perform the theorem-level six-axis comparison.** This is non-negotiable for the current novelty claim.
2. **Freeze one publication object.** Decide what A2 actually is. Preserve the other mathematics, but move independent web/operator/K3/boundary clusters into companion manuscripts or a clearly non-submitted archive unless a compelling logical unity is demonstrated.
3. **Reframe the significance argument around the unmarked inverse theorem.** Explicitly distinguish the deep intrinsic orientation/recovery step from the formal Pluecker-based fixed-coordinate parameter immersion.
4. **Give exact classical references for the symmetric-nilpotent orbit theorem used in the fixed-spectral classification.**
5. **Decide the editorial role of the real-likelihood and projective-critical sections.** Either make them concise consequences of the reconstructed-pencil spine or move them to a companion application paper. Do not use independent theorem accumulation as a substitute for conceptual unity.
6. **Resolve the role and priority burden of the all-rank contraction theorem.**
7. **Add the two short proof clarifications on the rational point and Hessian coordinate change.**
8. **Retain all current scope disclaimers on regularity, split semisimplicity, real structures, framed families, and base change.**
9. **Create a new immutable revision/source lock for any mathematical change.** Do not move the reviewed v144 object.

I do not request weakening the all-pencil inverse theorem, dropping nilpotent structure, retreating to generic pencils, or deleting proved mathematics. The correct response is sharper architecture and stronger external novelty evidence.

---

## 17. Final assessment

Revision 144 is substantially stronger than the earlier A2 objects.

The central finite-reconstruction proof now has a recognizable and nontrivial intrinsic mechanism. The rank-one rulings are treated scheme-theoretically; the global orientation argument forces one projective frame; the pencil coefficient line is recovered through irreducibility and exterior duality; the exact first relation yields a sharp finite order; the relative neighbourhood genuinely glues and survives arbitrary base change with the socle retained; the spectral sheaf and its Fitting incidence schemes are reconstructed; and the new projective critical divisor is finite flat through critical collisions with a coherent ramification/discriminant theory.

I did not find a new fatal mathematical counterexample to that principal chain.

That is not enough for a top-four acceptance recommendation.

The manuscript still asks the referee to certify a central novelty claim without having read the closest identified 1993 failure-locus predecessor. It still treats a 130-page multi-cluster research program as one submission even though the principal article itself admits that many supplement theorems are independent of its main proof. And its top-four significance narrative still does not cleanly separate the genuinely deep unmarked inverse step from formal consequences of a Pluecker-type coordinate encoding.

Accordingly, my recommendation is **reject in the present form**.

If the Ballico comparison is closed favorably, the publication object is rationalized without deleting the mathematics, the classical orbit inputs are pinned precisely, and the significance case is rebuilt around the intrinsic unmarked reconstruction mechanism, then the next version would merit a genuinely fresh top-four evaluation. At that point the right question would no longer be “is this proof architecture trustworthy?” but “is the resulting single theorem package important enough for one of the four journals?”

v144 is much closer to that question than its predecessors, but it has not yet answered it.
