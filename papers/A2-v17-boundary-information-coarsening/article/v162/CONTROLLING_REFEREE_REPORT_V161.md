# Independent harsh referee report — A2 revision 161

## Manuscript and review object

**Submission package:**

1. *Finite failure schemes and the reconstruction of quadratic pencils* (Paper I, 68 pages);
2. *Power ideals and the Hilbert boundary of quadratic pencils* (Paper II, 65 pages);
3. the 126-page preservation master containing the complete mathematical bodies of both papers.

**Author:** Qian Qi  
**Revision reviewed:** A2 revision 161  
**Revision branch:** `revision/a2-v161-multiple-incidence-contact-singularities-2026-09-25`  
**Locked branch tip:** `9e3b6639021a5f1fdb725961c7a7b6bb9cf55779`  
**Authored mathematical-source commit:** `da3ce030046e2651cf81a76be472329214373c88`  
**Complete manuscript materialization commit:** `5c3aaa92ce605a43ae31a98ed9cf652202a161dd`  
**Controlling prior report:** `review/a2-v160-independent-harsh-top4-2026-09-25`  
**Controlling prior-report commit:** `596df442f9155c79b6b33378c0a208259385b2ae`  
**Principal new sources:**

- `papers/A2-v17-boundary-information-coarsening/article/v161/multiple-incidence-v161.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v161/higher-contact-v161.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v161/effective-boundary-v161.tex`.

**Complete focused sources:** `reconstruction.tex` and `divisor-geometry.tex`.

**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, and expository standard expected at *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I reviewed the complete materialized v161 package rather than a source-lock shell or an encoded staging object. I read the revised introductions, the full multiple-incidence argument, the higher-contact Jordan-slice argument, the effective-stack and relative-lifting section, the response to the v160 report, the theorem index, the build and preservation records, and the source-comparison audit. I also re-read the inherited v157–v160 results needed to evaluate whether the new boundary geometry is mathematically controlled by the sharp failure algebra or merely transported after reconstruction.

The publication seal records complete sources and PDFs, successful independent compilation, preservation of all predecessor mathematical blocks, and a rerun of the inherited v160 finite checks. I use those records to identify the object under review and to assess reproducibility. They are not proof certificates, priority certificates, or evidence for the editorial threshold.

## Recommendation

**Reject the v161 package in its present form for a top-four general mathematics journal.**

Revision 161 is a genuine and substantial mathematical advance over v160. It directly addresses the strongest concrete demands of the preceding report:

- the single-incidence theorem is enlarged to the full reduced corank-two incidence open;
- independence of the local incidence conditions is proved from the distinct pencil radicals rather than imposed as a genericity hypothesis;
- the entire normalized Hilbert fibre at a pencil with `k` reduced incidences is computed as `(P^1)^k`;
- the unlabelled global centre is expressed by the Fitting ideal of the finite incidence algebra;
- arbitrary contact order is exhibited in explicit symmetric Jordan slices;
- the corresponding Hilbert limits have nonreduced thick tails, length-`m` attachments, and transverse `A_(m-1)` graph singularities;
- the exact local Rees equations, cotangent deformation module, ramified normalization, and stable-map comparison are written down;
- the effective stack, multi-Rees algebra, and relative lifting equations are placed in explicit categories.

These are real theorems. They are not cosmetic revisions, metadata, enlarged test suites, or merely a repetition of v160. I did **not** find a simple counterexample to the multiple-incidence theorem, the independence-of-radicals lemma, the contact-slice theorem, the thick-tail calculation, the `A_(m-1)` singularity statement, the stable-map comparison, or the relative lifting equations. My recommendation is therefore not a concealed correctness rejection.

The top-four problem is one of scale, necessity, and conceptual reach.

The reduced-incidence theorem is global on a natural open, but on that open its geometric mechanism is exactly the independent smooth-centre arrangement model. Once the normal evaluations are independent, the Fitting ideal is a product of disjoint-coordinate codimension-two ideals, the modification is the corresponding wonderful/product blow-up, and the fibre is the expected product of projective lines. The pencil-specific independence lemma is useful and nontrivial, and the Hilbert-graph identification requires work, but the overall geometry remains a particularly clean application of standard arrangement and Rees machinery.

The nonreduced result is more interesting locally, but it is a **slice theorem** for a deliberately engineered family. The manuscript constructs, for each `m`, a symmetric Jordan block whose submaximal-minor ideal is `(x^m,u,v)` and then computes the blow-up of `(x^m,t)`. This yields an attractive exact model, but it does not classify a neighbourhood of the nonreduced-incidence locus in the pencil Grassmannian, does not prove versality of the slice as an embedded pencil/Hilbert problem, and does not determine the ambient normalized Hilbert fibre at an arbitrary pencil with the same Smith exponents. The difficult boundary—interacting nonreduced contacts, mixed contact orders, higher corank, singular pencils in the Hilbert problem, nonnormal fibres, and wall crossing between boundary types—remains outside the theorem.

The improved failure-algebra interpretation also remains mediated by reconstruction. The envelope is a functor constructed after the first relation has recovered and oriented the source projective space. The incidence ideal is then obtained on the recovered pencil line from the classical determinantal ideal `I_(n-1)`. This is a legitimate and careful consequence of the sharp inverse. It is not a theorem that the original closed finite algebra carries, before reconstruction, a newly visible boundary singularity or compactification. A closed algebra determines the entire possible direction space; a deformation family supplies the chosen normal direction. This is the universal behaviour of a blow-up, not a new Torelli invariant of the closed algebra.

For a strong specialist venue, Paper II is now coherent, technically serious, and potentially publishable after proof polishing and sharper novelty positioning. Paper I contains a striking inverse theorem and deserves independent specialist scrutiny. The combined package nevertheless remains below the threshold of the four general journals named above.

---

## 1. What v161 genuinely fixes

### 1.1 The full reduced corank-two incidence open is treated

The manuscript no longer restricts the Hilbert modification to pencils with at most one corank-two incidence. It defines the open `U_red` of regular pencils avoiding corank at least three and having a finite reduced intersection with the corank-two determinantal locus. The finite incidence algebra

\[
\mathcal Q=q_*\mathcal O_D
\]

is used to define the centre

\[
\mathcal I=\operatorname{Fitt}_0(\mathcal Q).
\]

This is the right unlabelled global object. It handles monodromy among the incidence points and avoids choosing a global ordering.

### 1.2 Independence of distinct incidence points is proved

The key pencil-specific lemma chooses a nonsingular member `Q_0`, writes the pencil through the self-adjoint operator `T=Q_0^{-1}Q_1`, and uses the direct sum of eigenspace radicals at distinct spectral points. Restriction

\[
\operatorname{Sym}^2V\longrightarrow
\bigoplus_i\operatorname{Sym}^2(K_i^*)
\]

is surjective, and quotienting by the pencil tangent lines gives the required joint normal evaluation.

This materially strengthens v160. The product structure of the boundary is no longer based on an undeclared generic transversality assumption.

### 1.3 The whole reduced-incidence Hilbert fibre is computed

Theorem `thm:multiple-incidence-v161` identifies the normalization of the reduced Hilbert graph with

\[
\operatorname{Bl}_{\operatorname{Fitt}_0(q_*\mathcal O_D)}U_{\rm red}.
\]

At a pencil with `k` incidence points, the scheme fibre is `(P^1)^k`. Each factor records a line through the fixed tangent-normal point in the corresponding exceptional `P^2`. The universal curve is a reduced nodal main component with `k` embedded tails, and the local equations are

\[
x_i y_i=t_i.
\]

The theorem classifies the complete fibres over the stated open, not merely the limits of selected arcs.

### 1.4 The local multi-Rees algebra is explicit

In labelled local coordinates the incidence ideals are `I_i=(u_i,v_i)`, and the multi-Rees algebra is presented as

\[
R[U_1,V_1,\ldots,U_k,V_k]/(v_iU_i-u_iV_i)_i.
\]

The diagonal subalgebra is the ordinary Rees algebra of the product ideal. This is a useful correction to the earlier tendency to count the formal expression `direct sum I^d` as a separate structural theorem without giving its relations.

### 1.5 Every contact order occurs in an explicit symmetric-pencil slice

The Jordan family has exact residual Schur complement

\[
\begin{pmatrix}x^m+u&v\\v&x^m-u\end{pmatrix},
\]

and therefore

\[
I_{n-1}(A)=(x^m,u,v),
\qquad
\det A=c_m(x^{2m}-u^2-v^2).
\]

The special pencil has local Smith exponents `(m,m)` and incidence length `m`. This is an exact construction for every `m>=2`, not extrapolation from low-order computations.

### 1.6 The thick Hilbert tail is computed scheme-theoretically

After blowing up the parameter origin, the graph is locally the blow-up of `(x^m,t)`, with Rees equation

\[
tU-x^mV=0.
\]

The special Hilbert curve is

\[
C_0\cup T_m,
\qquad
T_m\simeq\mathbf P^1_{\mathbf C[x]/(x^m)},
\qquad
C_0\cap T_m\simeq\operatorname{Spec}\mathbf C[x]/(x^m).
\]

The tail is genuinely nonreduced, has no embedded associated points, and contributes cycle multiplicity `m`. This is stronger than a reduced-support or valuation statement.

### 1.7 The singular total graph and the stable-map limit are separated

The second Rees chart has equation

\[
x^m=tz,
\]

so the total graph has transverse `A_(m-1)` singularity. Its abstract hypersurface deformation module is

\[
T^1\simeq\mathbf C[[x]]/(x^{m-1}),
\qquad
T^i=0\quad(i\ge2).
\]

After the base change `t=s^m` and normalization, the tail becomes reduced and maps with degree `m` to the residual line. Thus the Hilbert limit and stable-map limit have the same cycle but different scheme objects. This distinction is mathematically worthwhile.

### 1.8 The deformation categories are more responsibly stated

The effective failure stack is explicitly distinguished from the stack of all raw Artin algebras of the same length. The lifting classes

\[
[v_i'-u_i'\widetilde w_i]\in J/u_i'J
\]

are stated as relative obstructions for a fixed base deformation, not as absolute obstructions on a smooth stack. This resolves an important categorical ambiguity in the previous presentation.

---

## 2. Correctness audit of the reduced-incidence theorem

I did not find a correctness blocker in this argument. Several steps are credible but should be expanded before publication.

### 2.1 The definition of `U_red` is appropriate

After removing lines meeting the lower-rank locus, the universal corank-two incidence is proper and quasi-finite, hence finite. Removing the finite image of the support of relative differentials is a natural way to impose reduced geometric fibres in characteristic zero.

The final version should state explicitly that a finite complex algebra has vanishing Kähler differentials exactly when it is a finite product of copies of `C`. It should also explain whether `U_red` is intended to include the empty incidence fibre; the present conventions do, and the Fitting ideal of the zero module is correctly taken to be the unit ideal.

### 2.2 The local splitting of the finite incidence algebra is credible

After strict henselization, the finite algebra splits by idempotents. Each length-one factor has a unit map from the base whose cokernel has zero closed fibre; Nakayama then makes the map surjective after shrinking. This produces a closed immersion of the factor into the base.

This is the correct scheme-theoretic argument. It is stronger than merely labelling the closed points of a reduced fibre.

### 2.3 The normal-coordinate lemma is standard but load-bearing

With a nonzero curve tangent in the normal space, one rank-locus equation can be used as the relative coordinate `x_i`; the remaining equations restrict to base parameters `u_ij`. Surjectivity of the joint normal evaluation then gives disjoint parameter blocks.

The manuscript should isolate the exact tangent sequence and identify every quotient map. The current proof is convincing, but the normal-space identifications are sufficiently central that they should not be compressed into prose.

### 2.4 The independence-of-radicals argument is plausible

At distinct spectral points, the radicals lie in distinct generalized eigenspaces and hence have direct sum. A symmetric form can prescribe arbitrary restrictions on those subspaces. The two pencil directions restrict to the one-dimensional tangent-normal lines, so the map descends to the Grassmannian tangent space and remains surjective after quotienting.

The paper should explicitly treat the possible nonsemisimplicity of `T`: the argument only needs directness of the eigenspaces for distinct eigenvalues, not diagonalizability. It should also state how the harmless projective twists are removed from the normal-space comparison.

### 2.5 Product and intersection of the local centre ideals agree

In independent coordinate blocks,

\[
I_1\cap\cdots\cap I_k=I_1\cdots I_k.
\]

This is correct. The equality can be checked monomially after completion and descended by faithful flatness.

### 2.6 The product blow-up description is credible

For independent pairs `(u_i,v_i)`, the blow-up of the product ideal is covered by the same charts as the fibre product of the individual blow-ups. The exceptional fibre is consequently `(P^1)^k`.

The final paper should make the diagonal-Proj argument explicit and separate it from the multigraded `MultiProj`. Many readers will otherwise wonder whether the ordinary blow-up of the product ideal is being silently identified with a fibre product in unjustified generality.

### 2.7 The Hilbert-graph normalization argument is essentially sound

The displayed Rees surjection gives a closed immersion of the strict-transform family into the base-changed complete-quadric blow-up. The family agrees with the original graph over the dense nonincident open. Distinct exceptional directions produce distinct embedded lines, so the map to the Hilbert graph has finite geometric fibres. Proper plus quasi-finite gives finite; the smooth source is then the normalization of the reduced integral graph.

The paper should explicitly record that the graph closure is integral and that the source and target have the same function field. These are true in the stated setting, but they are currently distributed across several paragraphs.

### 2.8 The degree formulas are consistent

At each corank-two point only the `(n-1)`-minor system has a base point. Removing `k` simple base points from the main component and placing degree one on each tail gives

\[
\deg_{F_i}H_q=\mathbf1_{q=n-1},
\qquad
\deg_{C_R}H_q=q-k\mathbf1_{q=n-1}.
\]

The determinant degree gives `2k<=n`. The Hilbert polynomial and Euler characteristic of the nodal tree are consistent with these formulas.

---

## 3. Correctness audit of the higher-contact slice

Again, I found no simple contradiction, but this part requires especially careful scoping.

### 3.1 The Jordan block calculation is credible

Deleting the first row and column of `L_m(x)` leaves a constant invertible block, and the scalar Schur complement is `x^m`. The two-block perturbation therefore has the displayed residual `2x2` matrix. The submaximal-minor and determinant formulas follow.

A short standalone matrix lemma, including the sign and determinant constant, would make the construction easier to verify than the current elimination prose.

### 3.2 The incidence Fitting ideal is correct

The incidence algebra is

\[
\mathbf C[x,u,v]/(x^m,u,v),
\]

which is a direct sum of `m` copies of `\mathcal O_S/(u,v)` as an `\mathcal O_S`-module. Hence its zeroth Fitting ideal is `(u,v)^m`, and its blow-up is the ordinary point blow-up.

This is a useful exact example of how nonreduced incidence multiplicity is lost by the base blow-up but retained by the universal curve.

### 3.3 The Rees presentation is correct for a regular sequence

For the ideal `(x^m,t)` in `C[x,t,w]`, the Rees algebra has the single relation

\[
tU-x^mV.
\]

The two charts are therefore

\[
t=x^my,
\qquad
x^m=tz.
\]

The first is smooth; the second is a normal hypersurface with singular locus of codimension two. This supports the claimed transverse `A_(m-1)` singularity.

### 3.4 Flatness should be referenced more precisely

Both charts are flat over the parameter blow-up, but the proof should state the exact fibrewise Cartier or local-flatness criterion being used. In the second chart one can also observe directly that the equation is monic in `x` over the polynomial algebra in `z`, which gives a transparent module-theoretic proof.

### 3.5 The thick-tail gluing is convincing

At `t=0`, the charts are

\[
\mathbf C[x,y]/(x^my),
\qquad
\mathbf C[x,z]/(x^m).
\]

The component `y=0` is the main strict transform; the `x^m=0` pieces glue to `P^1` over `C[x]/(x^m)`. Their intersection has length `m`. The principal hypersurface has only the component primes as associated primes, so there are no embedded points.

### 3.6 The complete power-system statement over the Artin base is plausible

The manuscript does more than identify the reduced base locus: it claims that, after removing the determinant factor, the actual coefficient span is every binary form of degree `delta_j` over `C[x]/(x^m)`. The invertible unit-block congruence and split socle multiplication make this credible.

Because this is one of the genuinely stronger statements of v161, it should be isolated as a lemma with a completely explicit coefficient-module map. The present proof is terse relative to the strength of the assertion.

### 3.7 The deformation module is the standard hypersurface calculation

For

\[
A_m=\mathbf C[[x,t,z]]/(x^m-tz),
\]

one obtains

\[
T^1=A_m/(mx^{m-1},t,z)
   \simeq\mathbf C[[x]]/(x^{m-1}),
\]

and no higher cotangent cohomology for the lci hypersurface. The miniversal equation perturbations are standard.

The final version must continue to state that these are abstract deformations of the total graph singularity—not deformations of the fixed-base relative curve, not embedded deformations in complete quadrics, and not deformations of the raw failure algebra.

### 3.8 The `Q`-Cartier and resolution statements need a more global anchor

The local cyclic-quotient presentation is correct, and the `A_(m-1)` resolution chain is standard. The self-intersection assertion `F^2=-1/m` is made “in a transverse surface.” The paper should specify the transverse surface globally enough that this intersection number is unambiguous and explain how the local tautological line bundle determines it.

### 3.9 The stable-map comparison is credible

After `t=s^m`, adjoining `x/s` normalizes the blow-up of `(x^m,s^m)` to the ordinary point blow-up. On the exceptional line the original graph coordinates are `[X^m:S^m]`, giving a degree-`m` map with finite deck group `mu_m`.

The paper should state the marked point and stability condition explicitly. The nonconstant map makes the component stable, but readers should not have to infer the automorphism calculation.

---

## 4. Audit of the effective stack and relative lifting section

### 4.1 The categorical restriction is now honest

The source stack is the effectively rigidified pencil-failure image, not the stack of all finite algebras with the same Hilbert function. This is essential. The paper no longer treats a statement about deformations inside the effective pencil image as a statement about all raw algebra deformations.

### 4.2 The envelope morphism is credible

The scalar weight on `B_h(V)_p` cancels the opposite weight on `O(2p)`, so the algebra bundle descends along a `PGL(V)` torsor. The construction does not require a global `O(1)` on a Brauer-nonsplit projective bundle.

The target “stack of algebra bundles with power diagram” should be given an explicit algebraicity statement or described merely as a fibreed category if algebraicity is not needed. Calling it a stack is not itself a proof that it is an algebraic stack of manageable type.

### 4.3 Representability of the boundary modification is plausible

For the same group acting on an equivariant morphism `B_red->U_red`, the quotient-stack map is representable; after a test map, the pullback is the associated projective scheme. Properness and birationality descend.

### 4.4 The multi-Rees presentation is useful but standard

With disjoint regular parameter pairs, the kernel is generated by the individual `2x2` syzygies. The diagonal algebra is the Rees algebra of the product ideal. This is a correct local presentation and a worthwhile clarification.

It remains an application of the standard Rees algebra of independent complete-intersection ideals. It should not be presented as a second global structural theorem independent of the incidence calculation.

### 4.5 The relative obstruction classes are correct chart equations

For a square-zero extension, the defect

\[
v_i'-u_i'\widetilde w_i
\]

lies in the kernel, and changing the slope lift changes it by `u_i'J`. Vanishing of its class in `J/u_i'J` is necessary and sufficient. The solution set is a torsor under the annihilator kernel of multiplication by `u_i'`.

The paper should explain transition between the two blow-up charts and show that these local classes glue to the expected relative cotangent-complex class. As written, the equations are correct in a selected chart, but their invariant formulation is only implicit.

---

## 5. Why the top-four threshold is still not met

### 5.1 The multiple-incidence theorem is a clean application of classical arrangement geometry

Once the pencil-specific independence lemma is proved, the remainder is the independent-centre wonderful model:

- each local centre is smooth of codimension two;
- the Fitting ideal is their product;
- the blow-up is the product of the individual blow-ups;
- the exceptional boundary is normal crossing;
- the fibre is a product of projective lines.

The Hilbert-graph identification adds real content, but the central birational geometry is not a new general mechanism. For a top-four paper, one would expect either a far more difficult boundary class or consequences of unmistakable importance beyond the construction itself.

### 5.2 The nonreduced theorem treats designed slices, not the ambient singular locus

The phrase “every contact order” is accurate only inside the displayed Jordan families. The theorem does not establish that every nonreduced corank-two pencil germ is formally or étale locally of this type. It does not classify the possible ideals replacing `(x^m,u,v)`, the resulting normalized Hilbert fibres, or the interactions of several thick contacts.

Thus the result gives one exact model for each integer `m`; it does not give the local geometry of the full nonreduced-incidence stratum.

### 5.3 The hardest complement remains almost untouched

The principal theorem excludes:

- corank at least three;
- nonreduced incidence in the ambient moduli problem;
- simultaneous contacts with different multiplicities;
- collisions between incidence points;
- singular pencils in the Hilbert-boundary theorem;
- nonnormal or reducible normalized graph fibres;
- wall crossings between different tail configurations;
- global boundary-component monodromy and intersection theory beyond the reduced open.

These are precisely the cases where a new compactification theory might become conceptually deep.

### 5.4 The failure algebra does not bypass reconstruction

The positive functorial statement is:

1. recover the first relation;
2. recover and orient the source;
3. recover the pencil line;
4. evaluate classical determinantal power ideals on that recovered line;
5. take a Fitting ideal and a Rees modification.

This is rigorous. It also means that the boundary is an invariant because the entire pencil has already been reconstructed. The manuscript does not exhibit a boundary operation internal to the original finite algebra that is visible before the inverse has essentially solved the problem.

### 5.5 A deformation direction is not data of the closed algebra

The manuscript now says this correctly: the closed algebra determines the projective space of possible boundary directions, while a family selects one direction. The selected tail is therefore family data. This is the standard universal property of a blow-up and should not be advertised as an additional closed-point Torelli theorem.

### 5.6 Much of the surrounding structure remains classical synthesis

The package relies on:

- classical complete quadrics and complete singular quadrics;
- classical invariant ideals of symmetric matrices;
- Smith and Kronecker pencil data;
- wonderful models for arrangements;
- standard Rees and strict-transform constructions;
- `A`-type hypersurface singularities and their resolutions;
- standard blow-up lifting equations;
- standard stable-map multiple covers.

The manuscript uses these ingredients intelligently and often exactly. The general-journal question is not whether the synthesis is competent. It is whether the new principle extracted from them is sufficiently deep and inevitable. I remain unconvinced.

### 5.7 No major external application is obtained

The revision does not solve a recognized problem about:

- moduli of quadratic pencils;
- compactifications of symmetric matrix pencils;
- singularities of complete quadrics;
- Hilbert schemes of curves in blow-ups;
- invariant theory of symmetric determinantal ideals;
- deformation theory of finite algebras;
- enumerative geometry of pencil degenerations.

The applications remain largely internal to the constructed failure-algebra pipeline.

### 5.8 Paper I's principal invariant is still deliberately information-bearing

The sharp inverse theorem is striking. Nevertheless, the failure algebra is engineered so that its first relation contains the determinant factor and the pencil coefficient data. The achievement is to recover that encoding intrinsically after forgetting grading, coordinates, and markings.

This is substantial specialist work. It is different from proving that a classical independently central invariant unexpectedly determines a pencil.

### 5.9 The historical comparison remains incomplete

The accessible Ballico 1996 theorem is now compared responsibly. The closest named 1993 failure-locus paper remains unavailable at theorem/proof level. The paper does not fabricate a conclusion, which is commendable, but exceptional historical originality remains uncertified.

### 5.10 The architecture is improved but still cumulative

The new reading hierarchy is better. Yet the two papers contain, between them:

- the sharp inverse;
- family and stack forms;
- automorphism and recognition results;
- covering and rigidification results;
- all-rank power graphs;
- regular and singular spectral recovery;
- complete quadrics;
- divisor normalization and conductors;
- collision atlases;
- reciprocal-fibre homology;
- reduced multiple incidence;
- nonreduced contact slices;
- effective stack modifications;
- relative lifting equations.

The 126-page preservation master makes the cumulative pipeline explicit. Top general journals do publish long papers, but usually because one central theorem forces a long proof. Here the length still reflects the retention of a large sequence of extensions.

---

## 6. Specific technical and expository requests

These points should be addressed even for a specialist submission.

1. **State the exact finite/unramified criterion used to define `U_red`.** Explain geometric reducedness over `C` and the empty-fibre convention.

2. **Prove openness and finiteness in one proposition.** The current construction is correct but fragmented.

3. **Write the tangent-normal sequence in the general incidence lemma.** Identify the source, target, and quotient maps precisely.

4. **Separate strict henselization from étale descent.** State where the idempotents descend and how the neighbourhood is shrunk.

5. **Make the codimension computation explicit.** It should follow from the smooth evaluation map and the codimension-three rank locus.

6. **Clarify nonsemisimple pencils in the independence lemma.** Only directness of distinct eigenspaces is used.

7. **Track the projective twists in the normal spaces.** “Harmless” is not a mathematical identification.

8. **Give a standalone lemma for `Bl_(I_1...I_k)`.** State the hypotheses under which it equals the fibre product of the individual blow-ups.

9. **Distinguish ordinary Proj, diagonal Proj, and MultiProj.** These are not interchangeable without a standard-graded argument.

10. **Describe the unlabelled exceptional boundary globally.** Explain the monodromy permutation of local components.

11. **State that the Hilbert graph closure is integral.** This is needed for the normalization argument.

12. **Prove finite geometric fibres of the map to Hilbert scheme in one place.** Distinct support lines are enough, but the argument should be formal.

13. **Explain why no ambient automorphism identifies two tails.** Hilbert points concern embedded subschemes in a fixed target.

14. **Cite the proper-plus-quasi-finite finiteness theorem exactly.** Keep the finite birational normalization step separate.

15. **State the exact polarization and Hilbert polynomial before both graph constructions.** Do not rely on inherited context.

16. **Give the Jordan block and Schur complement as a separate matrix lemma.** Include signs and determinant constants.

17. **Verify the projective chart at infinity for the contact slice explicitly.** The claim that infinity is nonsingular is easy but load-bearing.

18. **Cite the flatness criterion used for the Rees charts.** The fibres are nonreduced, so the hypotheses matter.

19. **State the Serre-criterion proof of normality.** Record Cohen–Macaulayness and codimension of the singular locus.

20. **Give an explicit associated-prime calculation for the thick fibre.** This supports the “no embedded points” claim.

21. **Isolate the coefficient-span theorem over `C[x]/(x^m)`.** It is stronger than equality of ideals on reduced fibres.

22. **Explain the graph line-bundle twists on the thick tail.** The local trivialization of the original `O(j)` twist should be visible.

23. **Specify the transverse surface used for `F^2=-1/m`.** Local quotient coordinates alone do not define a global intersection number.

24. **Orient the multiplicity chain in the minimal resolution.** Identify which end meets the main component and which meets the tail.

25. **Distinguish abstract, embedded, relative, and `Q`-Gorenstein deformations.** The `T^1` computation concerns only the first.

26. **State the stable-map markings and automorphism group.** Explain why the degree-`m` tail is stable with one attachment.

27. **Clarify normalization after ramified base change.** State the common function field and the finite integral charts.

28. **Give an invariant version of the relative lifting class.** Show how the chart equations transform on the other blow-up chart.

29. **Establish the algebraicity, or limit the claim, for the target envelope stack.** A fibreed category is enough if no moduli theorem is needed.

30. **Keep the effective-stack limitation in every summary.** It is not the raw Artin-algebra deformation stack.

31. **Do not count the Rees algebra definition as an independent recovery theorem.** The actual contribution is the relation presentation and its geometric identification.

32. **Keep `h=1` distinguished.** For larger `h`, the exponent remains an auxiliary choice even when the graph is unchanged.

33. **Do not call the Jordan slices a classification of higher contact.** They are exact models of every order, not all models of that order.

34. **Expand the literature comparison for Hilbert curves in blow-ups.** Li and Gathmann do not exhaust the relevant Fano/Hilbert/strict-transform literature.

35. **Retain the Ballico limitation in both submitted objects.** Do not move it only to repository metadata.

36. **Separate finite checks from theorem evidence.** The current receipts do this correctly; the final prose must continue to do so.

37. **Reduce the cumulative claim surface.** A specialist version of Paper II should emphasize the multiple-incidence theorem and contact slices, moving much of the inherited reciprocal-fibre material out of the submission.

38. **Obtain an independent proof audit of Paper I.** The sharp inverse is too central and too long to be supported only by preservation receipts and repeated internal revisions.

---

## 7. Response-to-v160 scorecard

### Fully or substantially closed

- enlargement from one reduced incidence to all reduced corank-two incidences;
- proof of independence rather than a genericity assumption;
- scheme-theoretic fibre `(P^1)^k` and nodal universal curve;
- local multi-Rees equations;
- exact relative lifting equations;
- explicit nonreduced contact models for every order;
- thick Hilbert tails and covered stable-map tails;
- clearer effective-stack category;
- improved main-text/appendix hierarchy;
- accessible theorem-level reference for the classical singular-pencil block data.

### Partially closed

- intrinsic relation between failure multiplication and boundary geometry;
- classification beyond the simple reduced open;
- nonreduced ambient boundary geometry;
- deformation-theoretic interaction between the failure algebra and the Hilbert boundary;
- literature positioning for Hilbert strict-transform modifications;
- modular interpretation of the entire pencil boundary.

### Still open

- a global compactification theorem covering nonreduced and higher-corank pencils;
- classification of the actual ambient Hilbert fibres outside `U_red`;
- interaction and wall crossing of several thick or higher-corank tails;
- an internal boundary construction visible in the closed finite algebra before reconstruction;
- a major external application;
- theorem/proof-level comparison with Ballico 1993;
- a top-four-scale conceptual principle not formal from classical complete quadrics, wonderful arrangements, and Rees geometry.

---

## 8. Conditions for another top-four evaluation

I would not recommend another top-four round triggered by one more explicit slice, a larger finite check suite, another classical invariant of the power ideals, or further rearrangement of the appendices.

A serious new round should contain at least one result of genuinely new global scale, for example:

1. **A global modular compactification** of the effective pencil-failure problem that includes nonreduced incidence, higher corank, singular pencils, and interacting boundary points.

2. **A classification theorem for ambient Hilbert fibres**, not only selected slices, with local equations, normalization, components, multiplicities, and wall-crossing relations.

3. **A versal local theorem** showing that the Jordan models control all germs with specified Smith/contact data, or identifying the additional moduli when they do not.

4. **An intrinsic boundary operation on the finite algebra itself** that does not first reconstruct the full pencil and then apply classical determinantal geometry.

5. **A genuinely new theorem on complete quadrics or symmetric determinantal ideals** not already formal from the classical resolution and invariant-ideal theory.

6. **A major external application** demonstrating that the sharp failure algebra solves a recognized problem independently of this manuscript's internal pipeline.

The historical comparison with the closest named failure-locus predecessor should also be completed through a legitimate source, or the broad historical framing should remain permanently narrow.

---

## 9. Final assessment

Revision 161 deserves substantial credit. It is complete, reproducible, mathematically stronger than v160, and responsive to the preceding report. The multiple-incidence theorem is a real global improvement. The Fitting-centre formulation is the correct unlabelled construction. The higher-contact slices produce exact and attractive nonreduced Hilbert geometry. The distinction between thick Hilbert tails and covered stable-map tails is especially clear. The stack and relative-lifting statements are much more responsible than the earlier informal deformation rhetoric.

I therefore reject any characterization of v161 as cosmetic or merely engineered bookkeeping.

I nevertheless recommend rejection for *Annals*, *Acta*, *Inventiones*, or *JAMS*. On the reduced open, the geometry is an application of independent-centre wonderful blow-ups after a pencil-specific transversality lemma. Outside that open, the paper computes carefully chosen Jordan slices rather than the ambient boundary. The failure-algebra interpretation still passes through reconstruction of the source and pencil line. Most surrounding structures remain classical inputs or internal consequences of the constructed invariant. The closest historical comparison remains incomplete, and no major external application is obtained.

The appropriate assessment is therefore:

**Reject the v161 package in its present form for a top-four general mathematics journal.**

**Paper II is a credible candidate for a strong specialist venue in algebraic geometry, invariant theory, or moduli after narrowing its claims and strengthening the ambient-versus-slice distinction. Paper I likewise deserves specialist consideration after an independent proof audit and sharper historical positioning.**
