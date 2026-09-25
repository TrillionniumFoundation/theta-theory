# Independent harsh referee report — A2 revision 160

## Manuscript and review object

**Submission package:**

1. *Finite failure schemes and the reconstruction of quadratic pencils* (Paper I, 65 pages);
2. *Intrinsic power geometry and the boundary of quadratic pencils* (Paper II, 58 pages);
3. the 117-page preservation master containing the complete mathematical bodies of both papers.

**Author:** Qian Qi  
**Revision reviewed:** A2 revision 160  
**Revision branch:** `revision/a2-v160-intrinsic-blowup-boundary-2026-09-25`  
**Locked branch tip:** `58c33453bf01d1f73083cb744d0479ecdc3dcf2f`  
**Authored mathematical-source commit:** `c5e0d49ede9f49d452943346875f1ea1b9361358`  
**Complete manuscript materialization commit:** `a6e49fb0014ad8641ac4625a5d6aa382abe1aabb`  
**Preserved v159 derivation commit:** `a27bd7fcea5c4ef04cdd8748411cdeab7ba42855`  
**Controlling prior report:** `review/a2-v157-independent-harsh-top4-2026-09-25`  
**Controlling prior-report commit:** `b81ba4a2fac700f17b26163079bd17ef54947509`  
**Principal new source:** `papers/A2-v17-boundary-information-coarsening/article/v160/incidence-blowup-v160.tex`  
**Complete focused sources:** `reconstruction.tex` and `divisor-geometry.tex`  
**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, and exposition standard expected at *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I reviewed the complete materialized v160 package. I read the new simple-incidence centre lemma, the normalized Hilbert blow-up theorem, the exceptional power-system proposition, the intrinsic incidence/Rees theorem, the v158 intrinsic-envelope and singular-pencil additions, the v159 ordinary-collision and boundary-moduli additions, the revised introductions, the point-by-point response to the v157 report, and the build, preservation, theorem-index, and literature records. I also re-read the inherited power-ideal and reconstruction statements needed to evaluate whether the new boundary construction is genuinely controlled by the original failure multiplication.

The publication seal records complete sources and PDFs, successful compilation, clean references, exact preservation of predecessor mathematical blocks, and a rerun of the inherited v159 finite checks. I use those records to identify the review object and assess reproducibility. They are not proof certificates, priority certificates, or evidence for the editorial threshold.

## Recommendation

**Reject the v160 package in its present form for a top-four general mathematics journal.**

Revision 160 is a serious and mathematically substantive response to the v157 report. It corrects the most obvious noncanonicity in the previous bridge: the determinant-apolar power diagram is now constructed on the source projective space extracted from the first relation, with scalar twists cancelled by an algebra bundle rather than by choosing an auxiliary coefficient section. It also identifies, on a natural simple corank-two open, the entire normalized Hilbert incidence modification with the blow-up of a smooth codimension-two centre. The exceptional fibre, every embedded nodal tail, all exceptional power systems, and the first normal direction are described. The intervening v158 and v159 additions supply all-rank power graphs, singular-pencil minimal-index data, arbitrary ordinary collision trees, and explicit residual boundary moduli.

These are genuine theorems. They are not cosmetic changes, repository bookkeeping, larger experiment tables, or a restatement of v157. I did **not** find a simple counterexample to the new incidence-centre lemma, Theorem 10.2, Proposition 10.3, the intrinsic-envelope theorem, the singular-pencil recovery formulas, or the ordinary-collision theorem. My recommendation is therefore not a concealed correctness rejection.

The top-four problem is one of scale, necessity, and conceptual independence.

The new Hilbert theorem is proved only on the open where a regular pencil meets the corank-two locus in at most one reduced point and avoids all lower-rank matrices. In that range the mechanism reduces to a very controlled general pattern: a line meets a smooth codimension-three centre once and transversely; after blowing up the centre, the Hilbert graph of strict transforms is the blow-up of the line parameter space along its codimension-two incidence locus. The proof is elegant, but its geometry is largely the standard local model `(x,u,v)`, the standard blow-up of `(u,v)`, and the nodal chart `xy=t`. The difficult boundary—multiple incidence points, nonreduced intersection, higher corank, interacting tails, singular pencils, and nonnormal Hilbert fibres—remains outside the theorem.

The revised “intrinsic” connection is also weaker than the headline can suggest. The envelope is not a subalgebra, quotient, deformation, or canonical piece of the original finite failure algebra. It is a functor newly built after the first relation has already reconstructed the source projective space. Theorem 12.1 then recovers the incidence ideal because the reconstructed pencil line carries the classical determinantal ideal `I_{n-1}`, and the Rees algebra is obtained by taking the ordinary powers of that recovered ideal. This is a legitimate functorial consequence of the inverse. It does not show that the original finite multiplication has an independently visible boundary singularity, obstruction theory, or modular compactification before one has essentially reconstructed the pencil.

Similarly, the statement that a first normal deformation selects an exceptional tail is the universal behavior of a blow-up. The closed algebra determines the pencil and hence the entire projective line of possible directions; an actual one-parameter family supplies the chosen direction. This is mathematically correct and appropriately stated, but it is not a new Torelli phenomenon of the closed failure algebra.

The v158 and v159 results are valuable specialist mathematics and careful synthesis. The all-rank graph theorem packages classical complete singular quadrics through multiplication powers. The singular-pencil theorem recovers minimal indices from finite Toeplitz-kernel dimensions and elementary divisors from Smith/contact data, using the classical symmetric Kronecker classification. The ordinary-collision theorem reduces, under strong transverse and squarefree hypotheses, to powers of the maximal ideal and blow-ups of smooth surface points. None of these, separately or together, supplies the single new global principle of unmistakable reach expected at the four general journals named above.

The closest named failure-locus predecessor, Ballico 1993, remains unavailable at theorem/proof level. The manuscript is commendably explicit about that limitation, but the broad historical originality of the failure-locus-to-reconstruction program remains uncertified. The new incidence audit is also too narrow: it does not compare the main blow-up statement with the general literature on Hilbert schemes of strict transforms of lines, Fano schemes under blow-ups, incidence blow-ups of Grassmannians, or wonderful models of subspace incidence.

Paper II is now a coherent and potentially strong specialist paper. Paper I contains a striking inverse statement and deserves independent specialist scrutiny. The two-paper package nevertheless remains below the top-four threshold.

---

## 1. What revision 160 genuinely adds

### 1.1 The intrinsic source-envelope construction repairs a real defect

The v157 report objected that the native complete-quadric boundary was produced from a chosen determinant-apolar section of an auxiliary reciprocal fibre. Revision 158, retained in v160, replaces that construction by the following sequence:

1. recover the cotangent space and first relation of the unmarked algebra;
2. recover and orient the two determinant rulings;
3. select the native source projective space `S_A` before recovering the final pencil coefficient line;
4. form the first-jet bundle `Hom(J^1L,L)`;
5. apply the Cartan quotient fibrewise;
6. cancel scalar lift ambiguities by the twists `O(2p)`.

In a source lift this gives

\[
\mathscr B_{A,h}
 =\bigoplus_{p=0}^{nh}B_h(V)_p\otimes\mathcal O_{\mathbf P(V)}(2p).
\]

The scalar cancellation is genuine: a scalar acts with opposite weights on the coefficient representation and the line-bundle twist. This is a materially better construction than choosing an `n`-plane in the old `n^2-1` dimensional coefficient complement.

The universal property added in v159 is also clean. The algebra bundle is the graded algebra generated by `Sym^2 E_A` subject to vanishing of every rank-one `(h+1)`st power. In characteristic zero, polarization identifies the generated relation module. At `h=1` the construction requires no extra integer choice.

This closes the most literal canonicity objection in the v157 report.

### 1.2 The all-rank power graph is a useful uniform statement

Revision 158 proves that the closure of the power graph on the rank-`r` locus is the relative complete-quadric space over `Gr(r,V)`. Retaining the top nonzero power recovers the image `r`-plane through the degree-`2h` Pluecker embedding. The total-transform formula for each power ideal is the expected rank-`r` specialization of the complete-quadric boundary formula.

This is a good theorem. It keeps the image-plane projection, not merely the isomorphism type of a fibre of complete quadrics. It also makes the singular-rank geometry compatible with one fixed algebra `B_h(V)`.

The geometry of complete singular quadrics and its orbit strata is, however, classical. The new contribution is the exact realization by the specified multiplication powers.

### 1.3 The singular-pencil data are genuinely more complete than the v157 contact theorem

Theorem 7.2 of Paper II combines two finite data sets:

- power/contact valuations recover the nonzero Smith exponents and their spectral positions;
- nullities of the finite Toeplitz maps `C_j(R)` recover the minimal-index multiplicities by second differences.

The formulas

\[
\kappa_j=\sum_a(j-\varepsilon_a+1)_+,
\qquad
\#\{a:\varepsilon_a=j\}
 =\kappa_j-2\kappa_{j-1}+\kappa_{j-2}
\]

are correct consequences of the kernel-bundle splitting. The conservation identity relating boundary contacts, the Grassmannian degree, and the normal rank is also natural and useful.

This materially improves the all-pencil scope: power contacts alone do not see minimal indices, and the manuscript now says so and supplies the missing finite syzygy data.

### 1.4 The ordinary-collision theorem is a substantial embedded calculation

Under the stated transverse ordinary-cluster hypothesis, the simultaneous exterior/power graph on the total pencil surface is the blow-up of the collision points. The special fibre is a reduced nodal tree whose tails are the complete-quadric lifts of the residual pencils. The theorem computes the multidegrees and the exact local power ideals

\[
J_p(A)=\mathfrak n_a^{\delta_{a,p}}(\det S_a)^{s_p}.
\]

The proof uses a real local result: distinct tangent factors force all lower minor ideals to be powers of the surface maximal ideal. The block-product lemma then identifies the first normal multiplication term.

The subsequent boundary-moduli theorem shows that a fixed limiting pencil may have positive-dimensional families of distinct embedded limits. This is an important correction to any suggestion that the limiting algebra alone selects a compactification point.

### 1.5 The simple-incidence blow-up theorem is the strongest new v160 result

Let `U` be the open of regular pencils whose lines avoid the corank-at-least-three locus and meet the corank-at-least-two locus in either no point or one reduced point. The incidence centre `Sigma_2` is shown to be smooth of codimension two, with normal space

\[
N_{\Sigma_2/U,R}
 \simeq N_{Z_{n-2}/P,p}/a_R.
\]

Theorem 10.2 identifies the whole normalized Hilbert graph over this open as

\[
\widehat G\times_G U\simeq\operatorname{Bl}_{\Sigma_2}U.
\]

The exceptional fibre is the complete projective line of lines through the tangent-normal point in the exceptional projective plane. Each member is a reduced nodal union of the strict transform of the pencil line and one tail. The local family `xy=t` gives flatness and excludes embedded components.

This is substantially stronger than exhibiting selected one-parameter limits. It determines the entire normalized Hilbert modification over a nontrivial open.

### 1.6 Every exceptional power system is computed

After splitting off the nonsingular `(n-2)`-block, the residual problem is binary. The universal ideal formula reduces the coefficient space to

\[
\mathfrak a^b
\quad\text{or}\quad
\mathfrak a^{2h-b}f^{b-h},
\]

and removal of the common determinant factor leaves the complete degree-`delta_j` ternary system. Therefore every exceptional plane and every tail carries a complete Veronese system of the stated degree. This includes tangent residual directions, not only squarefree residual pencils.

The result is exact and useful, although its proof is a direct binary specialization of the universal ideal identity.

### 1.7 The root review entry and publication state are now coherent

The branch root identifies revision 160, the authored source commit, the materialization commit, the two focused papers, and the preservation master. The earlier stale entry is archived. This closes the provenance inconsistency noted in the v157 report.

---

## 2. Correctness audit of the incidence-centre lemma

I find the lemma credible, but the final paper should slow down several load-bearing steps.

### 2.1 Smoothness and codimension are consistent

On `P \ Z_{n-3}`, the rank-`n-2` symmetric determinantal locus is smooth of codimension three. The universal evaluation from the universal line is smooth, so its inverse image is smooth. Its dimension is two less than the pencil Grassmannian, agreeing with a codimension-two incidence centre after projection.

The tangent quotient

\[
T_pP/(T_pZ_{n-2}+T_pL_R)
\]

has dimension two at a reduced intersection, giving the stated normal-space formula. I see no dimension inconsistency.

### 2.2 The closed-immersion argument is reasonable but too compressed

After removing lines contained in the rank locus and lines meeting the lower-rank locus, the incidence projection is finite. On the locus where the fibre has length at most one, the unit map

\[
\mathcal O_U\to q_*\mathcal O_D
\]

is fibrewise surjective. For a finite morphism this does imply global surjectivity of the coherent cokernel and hence a closed immersion.

The manuscript should nevertheless state the finite open and the base-change step explicitly. The proof currently moves quickly from a set of excluded lines to finiteness and then to upper semicontinuity. A reader should not have to reconstruct which proper incidence projection supplies each closed exceptional set.

### 2.3 The local ideal `(x,u,v)` is the correct normal form

Choosing one rank-locus equation with nonzero relative derivative and using it as the line coordinate is legitimate after an étale base change. Restricting the other two equations to the resulting section produces two independent base parameters. This yields the ideal `(x,u,v)` and the centre `(u,v)`.

This is the central local normal form for everything that follows. It would be useful to state it as an instance of a general transverse-incidence lemma for a family of curves meeting a smooth codimension-three centre. Doing so would both clarify the proof and expose how much of Theorem 10.2 is general blow-up geometry rather than pencil-specific mathematics.

---

## 3. Correctness audit of the normalized Hilbert blow-up theorem

I did not find a fatal defect in Theorem 10.2. The proof is plausible and substantially more complete than the earlier Hilbert-graph discussion.

### 3.1 The local family is the standard semistable model

After blowing up `(u,v)` and using a chart `u=t`, `v=tw`, the pulled incidence ideal is `(x,t)`. Blowing it up gives the familiar charts

\[
\mathcal O_B[x,y]/(xy-t),
\qquad
\mathcal O_B[z],\;x=tz.
\]

Over the regular base used here, the first ring is flat and its special fibre has two reduced branches crossing transversely. The second chart completes the projective tail. This correctly produces a nodal strict transform plus one exceptional line.

The manuscript's explicit module-basis argument for flatness is acceptable, although a standard semistable-blow-up lemma would be cleaner.

### 3.2 The embedding into complete quadrics is scheme-theoretic

The base-changed Rees algebra of the ambient rank-locus ideal maps onto the Rees algebra of its image on the universal line. The resulting surjection gives a closed immersion of Proj. This correctly avoids the false assertion that arbitrary blow-up formation commutes with arbitrary base change.

The paper should make the graded surjection and the relevant saturation entirely explicit. The finite checks include a Rees saturation, but the theorem must remain readable without them.

### 3.3 The exceptional curves are genuinely distinct

A normal direction modulo the tangent direction determines a line through `[a_R]` in the exceptional projective plane. Distinct quotient directions give distinct embedded lines, hence distinct nodal unions. This supports the quasi-finiteness of the map from the blow-up to the Hilbert graph.

### 3.4 The normalization argument is credible

The constructed blow-up maps properly to the reduced Hilbert graph closure, contains the dense nonincident graph, and has finite geometric fibres. Proper plus quasi-finite gives finiteness. Since the map is birational and the source is normal, it identifies the source with the normalization of the graph closure.

The paper should define the reduced Hilbert graph object again immediately before this argument, rather than forcing the reader back to the older proposition. It should also explicitly cite the standard fact that normalization localizes over an open subset.

### 3.5 The theorem is much narrower than a compactification of pencil moduli

The proof establishes the result over `U`, not over the whole pencil Grassmannian and not on a quotient stack. It excludes:

- two or more corank-two incidence points;
- a nonreduced corank-two intersection;
- any corank-three point;
- singular pencils;
- collisions of exceptional tails;
- nonnormal or reducible Hilbert graph components outside the simple open.

This is not a correctness objection. It is the principal limitation of the theorem's scale.

---

## 4. Audit of the exceptional power systems

The calculation in Proposition 10.3 is convincing.

With a nonsingular `(n-2)`-block removed, the first normal coefficient lies in the binary determinant-apolar algebra. If `b=j-h(n-2)`, the universal ideal formula becomes

\[
J_b=\mathfrak a^b \quad (b\le h),
\qquad
J_b=\mathfrak a^{2h-b}f^{b-h} \quad (h\le b\le2h).
\]

After dividing by the common determinant factor, the coefficient space is the entire space of ternary forms of degree

\[
\delta_j=(j-h(n-2))_+-2(j-h(n-1))_+.
\]

Restriction to any line gives the complete binary system of that degree. This justifies the Veronese assertion, including tangent lines to the residual determinant conic.

For publication, the proof should state more explicitly why the degree-`b` generators span the entire indicated homogeneous piece after passage from ideals to coefficient maps. The conclusion is correct in the binary polynomial ring, but the identification between an ideal's homogeneous component and the actual multiplication coefficient space is a recurring place where notation can hide a representation-theoretic step.

The result is exact, but its conceptual content is limited: once the universal ideal theorem and the residual binary reduction are in place, the proposition is nearly forced.

---

## 5. Audit of the intrinsic envelope

The envelope is mathematically well designed. It should not, however, be oversold as a hidden part of the original finite algebra.

### 5.1 The jet construction is credible

On `P(V)`, first jets of `O(1)` give the constant bundle `V^*`, so

\[
\mathcal Hom(J^1O(1),O(1))\simeq V\otimes O(1).
\]

The Cartan relations yield the stated determinant-apolar algebra bundle. Scalar changes of a lift act with opposite weights on the coefficient module and the line-bundle twist, so the bundle descends from a `PGL(V)` torsor. This is the right way to resolve the central-character obstruction.

### 5.2 The family statement needs a precise stack-level home

The theorem speaks of descent over arbitrary complex bases, including nonreduced bases. On a projective-space bundle with Brauer obstruction there need not be a global `O(1)`, and the paper correctly replaces it by associated-bundle descent. The final version should formulate the construction as a morphism of the effective failure groupoid to the stack of graded algebra bundles, rather than alternating between local vector bundles, projective torsors, and ordinary schemes.

This matters because the raw unmarked algebra has a large tangent-identity automorphism group. The construction is really made after the first-relation/effective rigidification and the orientation of a ruling. The word “intrinsic” is justified only with those operations stated.

### 5.3 The construction remains derivative of the full inverse

The envelope is explicitly **not** a subalgebra or quotient of `A`. It is a new universal algebra constructed from `S_A`. Once the main inverse has recovered `S_A` and then the pencil, every functorial construction on the source and pencil becomes an invariant of `A`.

That is mathematically legitimate. It is also why the envelope does not by itself transform the significance of the original inverse theorem. It shows that the inverse can transport classical complete-quadric geometry; it does not show that the finite multiplication unexpectedly contains a pre-existing compactification before reconstruction.

---

## 6. Audit of the singular-pencil theorem

The singular-pencil theorem is a useful synthesis, but much of its substance is classical once the pencil is known.

### 6.1 The finite-difference recovery of minimal indices is correct

A minimal-index block of size `2 epsilon + 1` contributes `O(-epsilon)` to the kernel bundle. Therefore

\[
\kappa_j=h^0(K(j))
 =\sum_a(j-\varepsilon_a+1)_+,
\]

and second differences recover the multiplicities. The bound `j <= floor((n-1)/2)` follows from the block size.

### 6.2 The Smith/contact formulas are consistent

Local symmetric diagonalization over `C[[t]]` produces the nonzero Smith exponents. The universal power ideal formula gives the piecewise-linear valuations, and boundary contacts are their successive differences. The global conservation identity follows from the determinant of the induced map on the saturated image bundle.

I see no simple contradiction in these formulas.

### 6.3 “Complete data” relies on the classical classification

The theorem does not prove a new classification of symmetric pencils. It reads the classical Kronecker invariants through two finite constructions after the pencil has been recovered. This is a useful invariant-theoretic packaging, but it should be presented as such.

The literature audit records only publisher/abstract access for Thompson rather than a fresh full proof inspection. Since the theorem explicitly invokes the classical congruence classification as a completeness input, an accessible theorem-level reference should be supplied.

---

## 7. Audit of the ordinary-collision and boundary-moduli theorems

### 7.1 The local minor-ideal calculation is sound under the stated hypothesis

If the residual linear pencil has squarefree determinant, its tangent factors are pairwise nonproportional. Products omitting one factor span every required binary form, which forces the lower minors to generate the full powers of the surface maximal ideal. This is a clean argument.

### 7.2 The blow-up description follows

Once the product of the noninvertible minor ideals is a positive power of the maximal ideal at each cluster, the simultaneous graph is the blow-up of the disjoint collision points. The special fibre is the standard nodal tree. The component multidegrees and power systems follow from the residual complete-quadric pencil.

This is credible and useful.

### 7.3 The hypotheses remain restrictive

The theorem assumes:

- a regular special pencil;
- generically simple spectrum;
- ordinary transverse clusters;
- a squarefree residual determinant at each cluster;
- disjoint cluster points;
- control by the first normal jet.

The v160 theorem removes the squarefree residual condition only in the single corank-two simple-incidence case. It does not provide a general collision theory for arbitrary multiplicities, tangencies, and simultaneous lower-rank incidence.

### 7.4 The boundary-moduli lower bound is not a fibre classification

The explicit residual-pencil families prove that the Hilbert fibre can be positive-dimensional and that the closed limiting algebra does not select a unique embedded curve. The lower bound is meaningful. The paper correctly stops short of claiming that these families exhaust the fibre.

For a top-four boundary theorem, exhaustion, component structure, normalization, and intersection behavior would be the natural next steps.

---

## 8. The central conceptual issue: reconstruction versus intrinsic boundary control

Revision 160 narrows but does not eliminate this issue.

### 8.1 What is now proved

From the unmarked failure algebra, after passing to the effective first relation and orienting its determinant ruling, one recovers the source projective space. On that source one constructs a determinant-apolar envelope. After the pencil line is recovered, one restricts the power ideal `J_{h(n-2)+1}` to it. Its zero scheme is the corank-two incidence, and the kernel of the unit map is the centre ideal. Taking ordinary powers produces the Rees algebra whose Proj agrees with the normalized Hilbert graph over `U`.

Every step is functorial on the stated effective image.

### 8.2 What is not proved

The manuscript does not show that:

- the original finite algebra contains the envelope as a canonical subquotient;
- the Rees algebra is visible without first recovering the pencil line;
- the raw unrigidified algebra stack has the asserted compactification;
- multiplication controls obstruction spaces or singularities of the Hilbert boundary;
- two nonisomorphic failure algebras can be compared through a new boundary invariant not already determined by the recovered pencils;
- the compactification extends the effective pencil-failure moduli problem with a modular interpretation on the complement of `U`.

The slogan “failure multiplication determines the boundary” is therefore true only in the same broad sense that a faithful invariant determines every functorial construction on the reconstructed object. The theorem is more concrete than that slogan—it singles out one power ideal—but the conceptual dependence remains.

### 8.3 The Rees-algebra recovery is formally weak once the ideal is known

Theorem 12.1 announces recovery of both `I_{Sigma_2}` and

\[
\bigoplus_{m\ge0}I_{\Sigma_2}^m.
\]

The second assertion is automatic after the first: the Rees algebra displayed is, by definition, the algebra of ordinary powers. The theorem does not compute a nontrivial presentation, defining equations, integral closure, torsion, or relation type of that Rees algebra from the original finite multiplication.

This should not be counted as a second independent structural result.

### 8.4 The normal direction belongs to a family, not the closed algebra

The paper now states this correctly. A closed algebra determines the full exceptional projective line, while a nonzero first normal derivative of a family selects one point. This distinction is important. It also means the strongest boundary datum is not an invariant of the closed algebra alone.

---

## 9. Originality and top-four scale

### 9.1 The simple-incidence theorem is a specialist theorem, not yet a general boundary theory

The local geometry is the universal model for lines meeting a smooth codimension-three centre. One expects the parameter space of simple transverse incidences to have codimension two and the resolved line to acquire one exceptional tail. The manuscript's contribution is to identify this model inside complete quadrics and connect its centre ideal to a multiplication power.

That is publishable. It is not, in my view, a top-four-scale resolution of the boundary of quadratic pencils.

### 9.2 The hard complement is exactly where new geometry should appear

The omitted locus includes the phenomena most likely to produce genuinely new mathematics:

- several corank-two points on one pencil;
- nonreduced incidence with `Z_{n-2}`;
- corank at least three;
- singular normal rank;
- interaction between minimal indices and complete-quadric tails;
- reducible or nonnormal Hilbert graph fibres;
- multiple exceptional components and their incidence complex;
- wall crossing between collision types;
- modular interpretation of extra and embedded components.

A top-four paper on the boundary should organize a substantial part of this complement, not only the easiest transverse open.

### 9.3 Much of the surrounding geometry is classical

Once the universal ideal identity is accepted:

- complete quadrics and complete singular quadrics are classical;
- their boundary divisors, flags, and orbit strata are classical;
- local Smith and Kronecker data are classical;
- the blow-up universal property and discrepancy are classical;
- the nodal chart `xy=t` is standard;
- multiplier ideals are inherited from symmetric determinantal theory;
- the exceptional Veronese systems follow from a binary specialization.

The manuscript carefully credits these facts, which is good. The remaining new core is not yet large enough for the claimed venue.

### 9.4 The relevant incidence literature comparison is missing

The literature audit discusses complete quadrics, symmetric invariant ideals, Stacks Project blow-up facts, and the failure-locus predecessor. It does not compare Theorem 10.2 with general results on:

- Hilbert schemes of strict transforms of lines under blow-ups;
- Fano schemes of lines and their modifications under birational maps;
- blow-ups of Grassmannians along incidence loci;
- wonderful compactifications of subspace incidence;
- stable maps versus Hilbert limits of lines meeting a centre;
- relative Rees and Nash-type graph modifications.

The new theorem may well be a clean original instance, but the present audit does not establish its position in this broader literature.

### 9.5 The Ballico comparison remains open

The manuscript's caution is correct. Inaccessibility is neither evidence of anticipation nor evidence of novelty. For a specialist paper, transparent disclosure may be enough. For an exceptional originality claim about a broad failure-locus reconstruction program, it remains a material unresolved issue.

---

## 10. Architecture and exposition

The division into two focused papers is an improvement over the unified v153 object. It does not fully solve the architecture problem.

Paper I is 65 pages and still contains:

1. the first-relation principle;
2. the all-pencil sharp inverse;
3. the one-point local algebra inverse;
4. moving-family and source-bundle reconstruction;
5. recognition and automorphism kernels;
6. covering-map reconstruction;
7. rigidification;
8. spectral specialization;
9. the intrinsic envelope;
10. the incidence-Rees application.

Paper II is 58 pages and contains:

1. the universal power identity;
2. determinant-apolar sections;
3. all-rank complete quadrics;
4. regular and singular pencil data;
5. the simple-incidence Hilbert blow-up;
6. ordinary arbitrary-multiplicity collisions;
7. boundary-moduli families;
8. binary normalization and conductors;
9. all-collision incidence atlases;
10. reciprocal-fibre homology and singularity calculations.

These are more coherent groupings than before, but each paper still reads as a cumulative research program. A top general-journal paper usually has one central theorem whose proof and consequences force the length. Here the length still comes from retaining every extension.

The repository preservation master is useful for auditing and should remain secondary. Its label counts, block counts, hashes, and rerun receipts should not appear in any significance argument.

---

## 11. Specific technical and expository points

These points should be addressed even for a specialist submission.

1. **Formulate a general transverse-incidence lemma.** The local model `(x,u,v)` and the blow-up conclusion are not special to quadrics. State the general theorem and then identify the pencil instance.

2. **Make the finite-incidence open precise.** List exactly which proper incidence images are removed before the projection becomes finite.

3. **State finite base change in the closed-immersion proof.** Explain why the fibre algebra of `q_*O_D` is the expected length-zero or length-one algebra.

4. **Separate openness of length at most one from reducedness.** Over the complex geometric fibres length one implies reducedness; the argument should say so.

5. **Define the Hilbert graph object locally before Theorem 10.2.** The reader should not have to recover its reduced closure and normalization conventions from an older section.

6. **Display the Rees-algebra quotient.** Give the actual graded surjection whose Proj yields the closed immersion into the base-changed complete-quadric graph.

7. **Clarify projective twists in the simultaneous multiplication graph.** Equality of base ideals and equality of projective coefficient maps are different statements.

8. **Prove flatness with a standard criterion.** The infinite module-basis description of `R[x,y]/(xy-t)` is correct here but distracts from the standard semistable local model.

9. **State why distinct exceptional directions give distinct Hilbert points scheme-theoretically.** Set-theoretic distinctness suffices for quasi-finiteness, but the embedded-line argument should be explicit.

10. **Cite localization of normalization.** This is used when restricting the global normalized Hilbert graph to `U`.

11. **Do not call the result a compactification of pencil moduli without the qualifier “over the simple-incidence open.”** It is a local modification of the pencil Grassmannian, not a global modular compactification.

12. **Distinguish the exceptional plane from the exceptional parameter line.** Several summaries move quickly between `P(N_{Z/P})=P^2` and `P(N_{Sigma/U})=P^1`.

13. **Expand the coefficient-space step in Proposition 10.3.** Show explicitly that the multiplication coefficients span every degree-`delta` form after removal of the determinant factor.

14. **State the stack or groupoid on which the intrinsic envelope lives.** Raw unmarked algebras, effectively rigidified first relations, and oriented-source torsors are not interchangeable categories.

15. **Keep `h=1` prominent.** For `h>1` the integer is an external choice even though the projective graph is independent of it.

16. **Do not describe the envelope as contained in the original algebra.** The current paper mostly avoids this; every abstract and summary should do the same.

17. **Temper the phrase “Rees algebra recovered from multiplication.”** Once the centre ideal is known, taking its ordinary powers is formal.

18. **Specify the deformation functor in the normal-direction statement.** Explain exactly which first-order algebra families correspond to tangent vectors of the effective pencil image.

19. **Separate nonlinear generator automorphisms from base deformation.** The assertion that higher-degree generator terms do not change the sharp relation should be stated over the dual-number base used for the tangent argument.

20. **Give an accessible theorem-level symmetric-pencil classification reference.** The current Thompson audit is bibliographic rather than a full-text theorem check.

21. **Clarify the finite range of Toeplitz maps.** Explain explicitly why no minimal index can exceed `floor((n-1)/2)` in the symmetric block decomposition.

22. **Distinguish local Smith exponents from global elementary-divisor positions.** “Complete data” requires both the partitions and their points modulo projective reparametrization.

23. **Do not call the ordinary-collision theorem an arbitrary collision theorem.** It assumes ordinary transverse clusters with squarefree residual determinant.

24. **State which v160 tangential directions are newly covered.** They are tangencies in the corank-two exceptional plane, not arbitrary nonordinary higher-corank collisions.

25. **Compare the Hilbert blow-up theorem with the general strict-transform literature.** This is essential for novelty positioning.

26. **Compute at least one boundary invariant beyond the simple open.** Even one controlled double-incidence or nonreduced-incidence fibre would materially strengthen the paper.

27. **Explain whether the blow-up centre is scheme-theoretically intrinsic before choosing the reconstructed pencil line.** At present the answer appears to be no; the line is an essential recovered object.

28. **Keep the Ballico limitation inside both submitted papers.** The repository audit is not a substitute.

29. **Keep finite checks out of the proof narrative.** They are useful reproducibility evidence only.

30. **Further focus Paper I.** The covering, rigidification, and broad spectral extensions should not obscure the sharp inverse theorem in a general-journal submission.

---

## 12. Scorecard against the v157 report

### 12.1 Canonical extraction of native power geometry

**Substantially addressed, with an important qualification.**

The source-normalized algebra bundle is functorial and cancels scalar twists. It is not a canonical subquotient of the original finite algebra; it is a new envelope constructed from the recovered source.

### 12.2 Native source versus auxiliary reciprocal complement

**Closed.**

The paper now clearly distinguishes the `n`-dimensional native source from the `n^2-1` dimensional complementary coefficient space.

### 12.3 Boundary interaction beyond formal pullback

**Partially and materially addressed.**

A specific multiplication power cuts out the simple corank-two incidence centre, and the normalized Hilbert graph over `U` is its blow-up. This is more than pulling a flat algebra back along an arbitrary map. The construction still occurs after the source and pencil line have been recovered.

### 12.4 Classification of limiting Hilbert fibres

**Closed only on a narrow open.**

Every fibre over the simple-incidence open is classified. The global complement remains unclassified.

### 12.5 Singular pencils and minimal indices

**Addressed at the invariant level.**

Finite syzygy nullities recover minimal indices, and contact powers recover elementary divisors. The completeness statement relies on the classical congruence classification.

### 12.6 Literature positioning of the new boundary theorem

**Still inadequate.**

The complete-quadric and blow-up inputs are cited, but the general Hilbert/incidence-blow-up literature is not surveyed.

### 12.7 Historical comparison with Ballico 1993

**Open.**

The limitation is honestly disclosed; theorem-level comparison remains unavailable.

### 12.8 Submission focus

**Improved, not fully solved.**

Two independently compiling papers are supplied, but both remain broad cumulative packages.

---

## 13. Conditions for another top-four evaluation

I would not recommend another top-four round triggered by another source audit, more finite checks, one additional exceptional coefficient formula, or a further reorganization of the same results.

A serious new round should contain at least one theorem of substantially greater global scale. Examples include:

1. **A global description of the normalized Hilbert incidence space** over a large open allowing multiple and nonreduced corank-two contacts, with component and intersection data.

2. **A higher-corank boundary theorem** computing the modification and fibres near corank at least three, including interactions among several exceptional tails.

3. **A modular compactification of the effective failure-algebra problem**, not merely the normalized graph closure inside a Hilbert scheme.

4. **A deformation-theoretic equivalence** showing that the failure-algebra deformation groupoid, after the stated rigidifications, intrinsically carries the boundary modification and its obstruction theory.

5. **A direct algebraic boundary invariant** that distinguishes degeneration types without first reconstructing the full pencil and then applying classical geometry.

6. **A classification of substantial singular-pencil boundary fibres** incorporating minimal indices, not only their numerical recovery on the original pencil.

7. **A genuinely new theorem about complete quadrics or symmetric determinantal ideals** not formal from their classical blow-up resolution and the universal power identity.

8. **A major external application** in which the failure invariant solves an independently recognized problem.

The authors should also complete a serious comparison with the literature on Hilbert schemes of strict transforms and incidence blow-ups, and obtain the theorem-level Ballico 1993 text through a legitimate source or permanently narrow the historical claims.

---

## 14. Final assessment

Revision 160 deserves substantial credit. It is the strongest A2 package I have reviewed. It fixes the stale review object, separates the native source from the auxiliary reciprocal complement, constructs a genuinely functorial source-normalized power envelope, recovers minimal indices of singular pencils, computes broad ordinary-collision families, and identifies the full normalized Hilbert modification over the simple corank-two open. The proof of the blow-up theorem is concrete and, in my reading, credible. The exceptional power systems and first normal direction are computed rather than guessed.

I therefore reject any characterization of v160 as cosmetic, merely engineered, or only metadata-driven. It contains substantial new mathematics.

I nevertheless recommend rejection for *Annals*, *Acta*, *Inventiones*, or *JAMS*. The principal new boundary theorem is confined to the easiest transverse incidence open and is governed by a standard blow-up model. The intrinsic-envelope bridge remains a construction made after the source and pencil have essentially been recovered; it is not a canonical part of the original finite algebra. The Rees-algebra statement is formal once the centre ideal is known. The hard global boundary, higher corank, multiple incidence, singular Hilbert fibres, and modular interpretation remain open. Much of the surrounding power, orbit, Smith, Kronecker, and complete-quadric geometry is classical. The relevant incidence literature and the closest named historical failure-locus predecessor remain incompletely compared.

The appropriate assessment is therefore:

**Reject the v160 package in its present form for a top-four general mathematics journal.**

**Paper II is a credible candidate for a strong specialist algebraic-geometry or invariant-theory venue after narrowing its claims and strengthening the incidence-literature comparison. Paper I likewise deserves specialist consideration after independent proof verification, sharper focus, and completion of the historical positioning.**
