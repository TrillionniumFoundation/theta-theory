# Independent harsh referee report — A2 revision 162

## Manuscript and review object

**Submission package:**

1. *Finite failure schemes and the reconstruction of quadratic pencils* (Paper I, 69 pages);
2. *Power ideals and the Hilbert boundary of quadratic pencils* (Paper II, 75 pages);
3. the 137-page preservation master containing the complete mathematical bodies of both papers.

**Author:** Qian Qi  
**Revision reviewed:** A2 revision 162  
**Revision branch:** `revision/a2-v162-versal-contact-neighborhoods-2026-09-25`  
**Locked branch tip:** `299a77c6f77c4d5aec6e5737e1b1ba471ce5b7c8`  
**Authored mathematical-source commit:** `5f0cb5538faddf20af4ebea70615058677f1c9df`  
**Complete manuscript materialization commit:** `4abda6bcfecbc66fe17576be8ea8f40d7d7b25bc`  
**Complete reviewed v161 baseline:** `9e3b6639021a5f1fdb725961c7a7b6bb9cf55779`  
**Controlling prior report:** `reviews/a2-v161-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md`  
**Controlling prior-report commit:** `3d22c10f34d889081000232bb8f2241d5988fc37`  
**Principal new sources:**

- `papers/A2-v17-boundary-information-coarsening/article/v162/versal-contacts-v162.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v162/euclidean-boundary-v162.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v162/technical-completions-v162.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v162/invariant-deformations-v162.tex`.

**Complete focused sources:** `reconstruction.tex` and `divisor-geometry.tex`.

**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, and expository standard expected at *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I reviewed the complete materialized v162 package rather than a source-lock shell or an encoded staging object. I read the revised introductions, the contact-deformation module and ambient realization theorem, the Euclidean division chart, the primitive jet-tail theorem, the non-equidimensional-fibre theorem, the technical completion appendix, the invariant deformation appendix, the response to the v161 report, the theorem index, the build and publication records, and the source-comparison audit. I also re-read the v161 multiple-incidence and higher-contact arguments and the inherited power-ideal and sharp-inverse statements needed to understand the claimed ambient and failure-algebra interpretations.

The publication seal records complete standalone sources and PDFs, successful compilation, preservation of all predecessor mathematical blocks, and a rerun of the inherited v161 finite checks. I use these records to identify the review object and assess reproducibility. They are not proof certificates, priority certificates, or evidence for the editorial threshold.

## Recommendation

**Reject the v162 package in its present form for a top-four general mathematics journal.**

Revision 162 is a genuine and substantial mathematical advance over v161. It directly addresses the preceding report's most serious mathematical objection: the nonreduced results are no longer presented only through a deliberately chosen two-parameter Jordan slice. The revision now supplies a full formal contact parameter space for regular symmetric pencils, proves that actual pencil perturbations realize the contact directions, constructs an explicit open chart of the embedded Hilbert graph with a regular inverse, identifies an open primitive-tail locus in the actual normalized pencil fibre with a product of jet schemes, and exhibits an actual contact-`(2,2)` fibre having components of different dimensions.

These are real theorems. They are not cosmetic editing, source repackaging, repository bookkeeping, or an enlarged finite experiment table. I did **not** find a simple counterexample to the contact-module formula, the ambient-realization theorem, the Euclidean division chart, the exact gcd fibre law, the primitive jet-tail description, or the conic-tail construction. My recommendation is therefore not a concealed correctness rejection.

The top-four problem is one of scale, proof transparency at the principal comparison step, and conceptual reach.

The contact deformation module and congruence-miniversal principle are classical in nature. The new contribution is the passage to a particular embedded Hilbert graph. The Euclidean chart is elegant and useful, but it is an open chart governed by polynomial division and the two-generator Rees equation `gU-fV=0`. The exact gcd law is a strong local description, yet it classifies only the primitive line-tail open, not the whole proper fibre. The non-equidimensionality theorem is the first convincing ambient phenomenon beyond that open, but it is proved for one contact type `(2,2)` and establishes only the existence of a two-dimensional component and a distinct component of dimension at least four. It does not determine the second component, all components, their intersections, the normalization of the fibre, or a wall-crossing theory.

The most delicate proof step is the comparison between formal congruence normal coordinates and the embedded deformation functor in a fixed complete-quadric target. An `x`-dependent congruence is an automorphism of a relative incidence bundle over the parameter disc; it is not one constant automorphism of the fixed projective target in which Hilbert points live. The manuscript recognizes this distinction and gives a gluing and completion argument, followed by an algebraic line-subbundle construction. I find the strategy plausible, but the proof remains compressed exactly where the main theorem changes category: from formal matrix germs modulo congruence to embedded curves in a fixed target. For a top-four paper this comparison should be formulated as a separate theorem about completed embedded deformation functors, with all source, target, frame, descent, and algebraization maps written explicitly.

Even granting the new theorems, the package does not yet provide a global modular compactification of the difficult boundary. Higher corank, singular pencils in the Hilbert problem, arbitrary nonprimitive tails, all components of nonreduced fibres, interactions among different nonreduced contacts, and global wall crossings remain outside the classification. The failure-algebra interpretation still uses the sharp inverse to reconstruct the source and pencil before transporting the Hilbert geometry. This is a legitimate consequence of reconstruction, but it is not a new internal boundary operation on the closed finite algebra.

Paper II is now a serious and potentially strong specialist paper. Paper I contains a striking inverse theorem and deserves independent specialist scrutiny. The combined package nevertheless remains below the threshold of the four general journals named above.

---

## 1. What revision 162 genuinely fixes

### 1.1 The old Jordan slices are no longer misrepresented as ambient neighbourhoods

The v161 report emphasized that one exact slice for every contact order is not a versal theorem. Revision 162 responds correctly. For

\[
D=\operatorname{diag}(x^{d_1},\ldots,x^{d_c}),
\]

the tangent quotient under identity congruences is computed as

\[
\mathcal T_D=
\bigoplus_i\mathbf C[x]_{<d_i}
\oplus
\bigoplus_{i<j}\mathbf C[x]_{<\min(d_i,d_j)}.
\]

The formally miniversal matrix retains one polynomial of the indicated bounded degree in each unordered entry. This is the correct infinitesimal quotient: diagonal congruence directions generate `(x^{d_i})`, while an off-diagonal entry is changed by `(x^{d_i},x^{d_j})`.

The manuscript explicitly states that the classifying map need not be unique in the presence of stabilizers. That is an important and correct qualification.

### 1.2 Actual pencil perturbations realize the formal contact parameters

Theorem `thm:ambient-versal-v162` does more than quote a normal-form theorem for arbitrary matrix-valued power series. It uses symmetric Jordan blocks and constant symmetric perturbations of the pencil coefficients to produce every monomial in the contact quotient. Distinct primary spectral subspaces are treated independently.

The parameter count

\[
N=\sum_{\lambda,i}d_{\lambda,i}
 +\sum_\lambda\sum_{i<j}\min(d_{\lambda,i},d_{\lambda,j})
\]

is reconciled with the congruence orbit and its stabilizer. This directly answers the v161 demand that the slice directions be compared with the full pencil neighbourhood.

### 1.3 The corank-two normal coordinates are explicit and useful

For positive exponents `a<=b`, the residual matrix is put in the Euclidean form

\[
S(x)=
\begin{pmatrix}
 f(x)&g(x)\\
 g(x)&f(x)k(x)+r(x)
\end{pmatrix},
\]

where `f` is monic of degree `a`, `k` is monic of degree `b-a`, and `g,r` have degree less than `a`. The total number of parameters is `2a+b`.

The incidence module is then represented exactly as

\[
q_*\mathcal O_D=\operatorname{coker}[M_g\ M_r]
\]

on `A_f=O[x]/(f)`, and its zeroth Fitting ideal is the ideal of maximal minors of the displayed multiplication matrix. This is a scheme-theoretic formula over arbitrary coefficient algebras, not a reduced-point reconstruction.

### 1.4 The Euclidean family is identified with an open Hilbert chart

The strongest new local result is Theorem `thm:division-chart-v162`. It introduces

\[
(f,g,w)\longmapsto
(f,g,r=\operatorname{rem}_f(gw)),
\]

with `q=(gw-r)/f`, and embeds the two-generator Rees graph

\[
gU-fV=0
\]

using the third coordinate

\[
[F:G:R]=[U:V:wV-qU].
\]

The paper does not stop at pointwise injectivity. It constructs a regular inverse from a Hilbert neighbourhood using a cohomological recovery map

\[
\Psi:(w,q)\longmapsto wG-qF.
\]

This is a substantial improvement over the earlier use of selected one-parameter families.

### 1.5 The exact gcd law unifies splitting and collision inside the chart

If `d=gcd(f,g)`, then the embedded fibre is

\[
C\cup T_d,
\qquad
T_d=\mathbf P^1_{\mathbf C[x]/(d)},
\qquad
C\cap T_d=\operatorname{Spec}\mathbf C[x]/(d).
\]

The attaching section is determined by the coprime residual pair. The Chinese remainder theorem separates distinct support points while preserving their nilpotent thicknesses. The calculation gives the degree on the main component, the cycle degree on the tail, and the absence of embedded associated points.

This is a real collision law, not only a list of examples.

### 1.6 Primitive tail directions form jet schemes in the actual pencil fibre

Theorem `thm:ambient-jet-tails-v162` identifies the primitive line-tail locus over a fixed regular pencil with no corank at least three as

\[
\prod_i\operatorname{Res}_{\mathbf C[x_i]/(x_i^{a_i})/\mathbf C}
\mathbf P^1
=
\prod_i J_{a_i-1}(\mathbf P^1).
\]

Its dimension is `sum a_i`. In particular, for a nonreduced contact the constant exceptional direction is only the zero-jet section. This corrects the overly small direction space implicit in the old constant-parameter slice.

The theorem also gives completed local product charts and an exact resultant boundary. It explicitly states that this primitive open is not the whole proper fibre.

### 1.7 The revision produces an actual non-equidimensional fibre

For one contact of type `(2,2)`, Theorem `thm:nonequidimensional-v162` obtains:

- a two-dimensional component with open part `J_1(P^1)`;
- a distinct component of dimension at least four, witnessed by smooth conic tails through the attaching point in the exceptional `P^2`.

The conic arcs have three independent quadratic generators whose ideal is `(x,t)^2`. The exceptional map is a complete Veronese conic. Smooth conics through a fixed point form a four-dimensional family, and the proof passes to a finite surjective inverse image under normalization rather than assuming an automatic lifting of a nondominant family.

This is the first result in the A2 sequence that proves genuinely different ambient Hilbert behaviours for the same closed contact data.

### 1.8 The requested technical details are largely supplied

Appendix T now records:

- the finite/reduced incidence criterion;
- the exact tangent-normal sequence;
- étale splitting and descent of incidence factors;
- the diagonal Rees versus MultiProj distinction;
- integrality and normalization steps;
- Jordan determinant constants;
- flatness and normality of thick charts;
- associated-prime calculations;
- coefficient surjectivity over Artin tails;
- the transverse intersection number;
- the ramified normalization and marked stable-map automorphisms.

These additions materially improve proof auditability.

### 1.9 The deformation target and chart obstruction are now invariantly stated

Paper I, Appendix F, gives an algebraic finite-type classifying stack for the specified envelope forms and identifies the chart defects with an `Ext^1` class of the relative cotangent complex. The overlap transformations are written explicitly. The statement remains restricted to the effectively rigidified pencil-failure image and is not generalized to all Artin algebras of the same length.

---

## 2. Correctness audit of the contact-module and ambient-realization theorem

I found no direct contradiction in this part. The statements are plausible and mostly well supported, but several hypotheses and identifications should be made more explicit.

### 2.1 The tangent quotient is correct

For an infinitesimal congruence `1+epsilon H`, the variation is

\[
H^{\mathsf t}D+DH.
\]

The diagonal entry is adjustable modulo `x^{d_i}`, and the `(i,j)` entry modulo

\[
(x^{d_i},x^{d_j})=(x^{\min(d_i,d_j)}).
\]

The direct-sum formula follows. The factor two on the diagonal is harmless over `C`.

### 2.2 Formal reduction by successive congruences is credible

The `m`-adic induction divides the order-`q` error by the appropriate power of `x`, places the remainders in the bounded polynomials, and removes the quotients by an order-`q` congruence. Cross terms have higher base order, so the process converges.

The paper should state exactly which topology is used on the matrix entries and whether the coefficient ring is `R[[x]]` or a completed localization in both the base and pencil parameter. The proof uses both `m`-adic convergence and polynomial degree bounds in `x`; the two structures should be formally separated.

### 2.3 The actual-pencil surjectivity calculation is a real contribution

The identity

\[
L_d(x)(1,x,\ldots,x^{d-1})^{\mathsf t}=x^d e_1
\]

and constant perturbations of the block produce the required monomials in the Schur complement. This shows that the contact quotient is reached by honest variations of the pencil coefficients.

For publication, the Schur-complement derivative should be displayed as a coordinate-free map from the Grassmannian tangent space to the contact quotient. The current block calculation proves surjectivity, but the final theorem is stated on a framed atlas and then descended. A commutative diagram would remove ambiguity about which frame and parameter directions have been factored out.

### 2.4 The stabilizer count should be isolated

The dimension of homomorphisms between two Jordan blocks at the same eigenvalue is `min(d_i,d_j)`. The skew-adjoint centralizer contributes one copy for each unordered pair and no diagonal copy. Distinct primary eigenvalues contribute zero.

This is plausible and gives the second sum in `N`. A concise lemma identifying the orthogonal stabilizer Lie algebra would make the equality-of-dimensions argument easier to audit. The present paragraph combines centralizer, adjointness, orbit dimension, and the determinant-degree identity in one step.

### 2.5 Formal smoothness is not the same as an algebraic étale chart

The theorem correctly states a formally smooth map of completed bases. Later algebraization comes from the explicit Hilbert family, not automatically from the formal normal form. This distinction must remain visible. The phrase “full regular-pencil neighbourhood” should always mean a formal neighbourhood on the framed atlas until Theorem 7.2 supplies the algebraic open immersion.

### 2.6 Stabilizers prevent uniqueness

The manuscript notes that the miniversal classifying map is not unique. This matters when using contact coefficients as coordinates on an embedded moduli problem. The Hilbert chart must be invariant under precisely the residual stabilizer that preserves the embedded pencil data. The proof currently resolves this by retaining the parameter and constructing an inverse from the curve. That strategy is sound, but the logical dependence should be made explicit in the theorem statement.

---

## 3. Correctness audit of the Euclidean division chart

This theorem is attractive and, in my view, likely correct. It should nevertheless be presented with greater categorical precision because it is one of the main originality claims.

### 3.1 The base and graph object must remain explicit

`Gamma_a` is the reduced closure of the graph of the map from `B_a` to a Hilbert scheme. Thus a point of `Gamma_a` retains the base coefficients `(f,g,r)` as well as the embedded curve. This retention is essential: the inverse construction recovers `(w,q)` from the curve only after `(f,g,r)` are known from the projection to `B_a`.

The theorem should say this directly every time it calls `W_a` an open subscheme of `Gamma_a`. Without the graph projection, the asserted inverse would be false as a statement about the Hilbert point alone.

### 3.2 The Rees presentation is correct

Because `f` is monic and `g` contains independent coefficient variables, `(f,g)` is a regular sequence in the total polynomial ring. Its Rees algebra has the single linear relation

\[
gU-fV=0.
\]

The identity `r=gw-fq` makes `(f,g,r)=(f,g)` on the division locus. The third graph coordinate is therefore compatible with the original three-coordinate map.

### 3.3 Flatness is adequately justified

The homogeneous Rees equation is nonzero in every geometric fibre. The fibrewise Cartier criterion in a flat smooth ambient family applies. This is much better than the vague fibre-flatness argument used in earlier versions.

### 3.4 The cohomology calculation deserves a standalone lemma

For the central curve `Z_w`, the line bundle

\[
L=O_{P^1\times P^2}(a-1,1)|_{Z_w}
\]

has degree `a-1` on the main component and is `O(1)` over the length-`a` tail. The union sequence gives `H^1=0` and `h^0=2a`.

This calculation is plausible. It should state the exact short exact sequence of sheaves on the nonreduced union and prove surjectivity of the tail restriction map over the Artin algebra. This is a load-bearing cohomology-and-base-change input, not merely a dimension check.

### 3.5 The recovery map has the expected ranks

The domain of

\[
\Psi:(w,q)\mapsto wG-qF
\]

has dimension `2a-1`, and the target has dimension `2a`; hence the cokernel is a line bundle after shrinking. Injectivity at the central fibre is correctly checked by restricting first to the main component and then to the tail.

The statement that the class of the homogenized `R` vanishes on a dense open and therefore globally requires that the neighbourhood in the graph be integral and reduced and that the cokernel be locally free of rank one. These hypotheses are present but distributed across the proof. They should be assembled into one lemma.

### 3.6 Equality on the dense open extends correctly

Once `w,q` are regular, `r=gw-fq` holds on the dense resultant-nonzero locus and hence on the integral graph neighbourhood. The separatedness of the Hilbert scheme then identifies the reconstructed family with the universal one.

This is a valid way to obtain a scheme-theoretic inverse, not only a bijection on closed points.

### 3.7 The gcd fibre decomposition is credible

Factoring the Rees equation as

\[
d(g_1U-f_1V)
\]

with coprime `f_1,g_1` produces the main graph component and the tail over `C[x]/(d)`. Their intersection is the section `[f_1:g_1]`. The hypersurface is Cohen–Macaulay and has no embedded associated primes.

For repeated irreducible factors of `d`, the manuscript should distinguish component primes from primary thickenings. The phrase “the associated primes are precisely its component primes” is correct locally, but the global Chinese-remainder discussion should not suggest that a repeated root splits into several components.

---

## 4. The formal-to-embedded comparison is the central proof obligation

Theorem `thm:ambient-jet-tails-v162` is the conceptual bridge of v162. It is also the least transparent part of the proof.

### 4.1 An `x`-dependent congruence is not a fixed-target automorphism

The Hilbert scheme parametrizes subschemes of one fixed complete-quadric target. A congruence matrix depending on the pencil parameter `x` is a gauge transformation of a trivial vector bundle over the parameter disc. It does not arise from one element of `PGL(V)` acting on the fixed target.

The manuscript explicitly acknowledges this and moves to an incidence target over the universal pencil line. That is the right response. However, the proof should define this incidence target and the morphism to the fixed Hilbert target in a formal diagram, rather than describe the distinction in prose.

### 4.2 The claimed equality of embedded deformation functors needs a theorem

The proof says that the first complete-quadric projection recovers the line coordinate, the punctured-disc curves agree, the local ideals glue uniquely, and equality and flatness are detected after faithful completion. These observations are plausible, but the conclusion is strong: the completed embedded deformation functor of the pencil graph is identified with the polynomial normal-graph functor times smooth factors.

For top-four proof standards, this should be isolated as a proposition with:

- the source deformation category;
- the fixed target or relative incidence target;
- the frame group acting on each side;
- the exact ideal sheaves being compared;
- the faithfully flat completion argument;
- the descent from framed to unframed pencils;
- compatibility with normalization.

At present this crucial category change occupies several paragraphs inside a longer proof.

### 4.3 Completion does not automatically algebraize the open immersion

The paper does not make this mistake; it later constructs an algebraic morphism from the jet space using the universal line subbundle and attaching section. That construction is the correct algebraization mechanism.

The logic should be reordered so that the algebraic family is constructed first, then its completed local rings are compared with the Hilbert graph, and finally an étale-monomorphism criterion yields the open immersion. This would make clear that formal normal coordinates are used to prove local isomorphism, not to create the algebraic morphism.

### 4.4 Completed local isomorphism implies étaleness only with hypotheses

The finite-type condition, equality of residue fields, and Noetherian excellence are available. They should be stated at the point of use. A citation to the formal criterion for étaleness would help. The current sentence is correct in spirit but too compressed for the principal theorem.

### 4.5 The normalization/fibre distinction must remain explicit

The object is the fibre of the normalization of the total reduced Hilbert graph, not the normalization of the Hilbert fibre. These operations need not commute. The proof works by constructing regular total charts that normalization does not change. This is the right argument. Every summary should preserve that distinction.

---

## 5. Correctness audit of the primitive jet-tail locus

### 5.1 The Weil restriction description is natural

A primitive line through a fixed section in a projective plane over the length-`a` algebra is parametrized by `P^1` over that algebra. Weil restriction to `C` gives a smooth scheme of dimension `a`, canonically identifiable with the `(a-1)`-jet scheme of `P^1`.

The paper should fix its jet convention explicitly: `J_{a-1}(P^1)` represents maps from `Spec C[x]/(x^a)`. This avoids an off-by-one ambiguity.

### 5.2 The two affine charts glue by inversion in the Artin algebra

The slopes `w` and `w'` satisfy `w'=w^{-1}` where the slope is a unit. This is the standard atlas of the Weil restriction. The construction includes nilpotent coefficients and is not only a reduced parameterization.

### 5.3 The algebraic monomorphism is plausible

The universal primitive line subbundle is recovered from the embedded tail, so the map to the Hilbert fibre is a monomorphism. The union with the fixed strict transform is flat by the union exact sequence and surjectivity on the attaching scheme.

The paper should state the relative Hilbert polynomial in this construction directly, rather than rely on the later multidegree paragraph. Flatness of the union plus constant Hilbert polynomial are related but logically distinct.

### 5.4 “Every point is a limit of genuine pencils” needs algebraic wording

Every point of the smooth division chart lies in the closure of the dense resultant-nonzero locus. Over `C`, one can choose an algebraic curve through the point meeting that locus, or use the explicit `g=t` family. The theorem should say “an algebraic or formal one-parameter specialization” and identify which is actually constructed. Properness then produces the same Hilbert limit.

### 5.5 The resultant boundary can be complicated

The chart is smooth, but the resultant divisor can be singular and non-normal-crossing. This is honestly stated. A useful next step would be to compute its local multiplicities and stratification by gcd partition. Without that, the exact gcd law is a fibre classification inside a smooth chart, not a full boundary stratification theorem.

---

## 6. Correctness audit of the non-equidimensional-fibre theorem

I find the construction plausible and potentially important. It should nevertheless be strengthened substantially before it carries the principal significance burden of a top-four submission.

### 6.1 The two-dimensional component argument is valid if the open-immersion theorem is accepted

The primitive tail locus `J_1(P^1)` is smooth irreducible of dimension two and open in the normalized fibre. Its closure is therefore an irreducible component of dimension two.

The theorem should cite the elementary irreducible-component argument, because an open subset of a fibre being irreducible is the exact reason its closure is a component rather than merely a subvariety.

### 6.2 The conic arcs have the claimed base ideal

For

\[
\begin{aligned}
f&=x^2+t\alpha_1x+t^2\alpha_0,\\
g&=t\beta_1x+t^2\beta_0,\\
r&=t\gamma_1x+t^2\gamma_0,
\end{aligned}
\]

the determinant condition

\[
\beta_1\gamma_0-eta_0\gamma_1\ne0
\]

makes the three quadrics a basis of `(x,t)^2`. The blow-up is the ordinary point blow-up, and the exceptional line maps by a complete quadratic system to a smooth conic through `[1:0:0]`.

This calculation is correct.

### 6.3 The four-dimensional conic family is correctly counted

Plane conics form `P^5`; passage through one fixed point is one linear condition, leaving `P^4`. Smoothness is open. Thus smooth conics through the attachment form a four-dimensional family.

### 6.4 The locally closed immersion should be proved as a relative residual construction

The manuscript says that the conic is recovered as the residual component to the fixed main curve. This is plausible, but in families the residual operation should be expressed through an ideal quotient or a relative Hilbert flag. This would prove representability and the locally closed immersion without relying on a sentence about recovery.

### 6.5 Passage through normalization is handled in the right direction

The proof does not claim that the conic family lifts to the normalization. It takes the finite surjective inverse image under normalization. A component of that inverse image has dimension four and lies in the normalized fibre. This is correct.

The argument should state explicitly that finite surjective pullback preserves dimension and that every component dominating the irreducible conic family has dimension four. “Some component has dimension four” follows after selecting a dominating component.

### 6.6 Distinctness from the jet component follows by dimension, but geometry is still unknown

A component of dimension at least four is distinct from the two-dimensional component. This proves reducibility and non-equidimensionality.

It does not identify:

- the generic curve of the higher-dimensional component after normalization;
- whether its dimension is exactly four;
- whether more components exist;
- how the two components intersect;
- whether their closures meet along degenerate conics, doubled lines, or thicker primitive tails;
- the local ring of the fibre at an intersection point;
- whether the fibre is reduced, Cohen–Macaulay, connected, or normal in any component.

These are not minor omissions if non-equidimensionality is intended as the main global theorem.

### 6.7 The theorem treats one contact type

The first interesting case `(2,2)` is a natural test. A top-four-scale result would need a systematic description for general `(a,b)`, or at least a structural principle predicting components from degree partitions of the contact multiplicity. At present the conic component is an existence theorem in one fibre.

---

## 7. The failure-algebra interpretation remains derivative of reconstruction

Revision 162 is careful and honest about this point.

The effective-family transfer is:

1. use the sharp inverse to recover the oriented source and pencil;
2. form the determinant-apolar envelope and its power ideals;
3. identify the contact ideal on the recovered pencil line;
4. transport the Hilbert charts and their families through the effective equivalence.

This is a valid functorial consequence. It shows that the boundary geometry is an invariant of effective failure-algebra families.

It does **not** show that the closed finite algebra contains, before reconstruction, a canonical internal boundary operation or an intrinsic deformation direction. The closed algebra determines the possible fibre; a family supplies the point of that fibre. The manuscript now says this explicitly, and that honesty should be retained.

For top-four significance, however, the distinction matters. The boundary theory remains an application of a very strong inverse theorem to classical and newly computed pencil geometry, not an independently emergent geometry of finite algebras.

---

## 8. Originality and significance at the top-four level

### 8.1 The ambient step is a genuine advance, but still local

Revision 162 substantially closes the “slice versus ambient neighbourhood” objection. The primitive-tail locus is now an open piece of the actual normalized fibre, and the conic family lies in that same actual fibre.

Nevertheless, the result remains local around regular corank-two contacts. It does not produce a global compactification theorem covering all pencils or all Hilbert boundary components.

### 8.2 The principal mechanisms are classical

The construction relies on:

- congruence-miniversal deformation theory of symmetric pencils;
- complete quadrics and rank-locus blow-ups;
- Euclidean division in `C[x]/(f)`;
- two-generator Rees algebras;
- cohomology and base change on a rational union;
- Weil restriction and jet schemes;
- resultant strata;
- standard Hilbert residual-component arguments;
- finite normalization maps.

The manuscript combines these tools intelligently. The editorial question is whether the resulting theorem exposes a principle of broad mathematical necessity. The current result is better viewed as a precise specialist analysis of one compactification problem.

### 8.3 Non-equidimensionality alone is not enough

Showing that an actual fibre is reducible and non-equidimensional is interesting. For a general journal, one would expect either:

- a classification of all components;
- a general component theorem for arbitrary contact type;
- a new invariant controlling component dimensions;
- a wall-crossing or adjacency theory;
- a consequence for a recognized moduli problem outside the manuscript's internal pipeline.

None is presently supplied.

### 8.4 The difficult cases remain open

The package still does not classify:

- corank at least three Hilbert neighbourhoods;
- singular pencils in the Hilbert compactification;
- nonprimitive tails;
- interactions of several nonreduced contacts beyond the primitive product open;
- collision of spectral support points with changing primary decomposition;
- all components of a single nonreduced fibre;
- global monodromy and intersection theory of the boundary;
- wall crossings between thick lines, reduced curves of higher degree, and mixed components.

These are the cases in which a genuinely new compactification theory would emerge.

### 8.5 No major external application is obtained

The new theorems do not yet solve a recognized independent problem about complete quadrics, symmetric pencil moduli, Hilbert schemes, quasimaps, stable maps, determinantal ideals, or finite-algebra deformation theory. Their applications remain internal to the A2 reconstruction/boundary programme.

### 8.6 The literature audit is responsible but not exhaustive

The comparisons with Dmytryshyn, Hu–Lin–Shao, Chung–Hong–Kiem, complete quadrics, and the Stacks Project are useful. The main Hilbert statement should also be positioned against broader work on:

- graph spaces and quasimap compactifications;
- Hilbert schemes of graphs of rational maps;
- strict transforms of linear spaces under blow-ups;
- Fano schemes in wonderful compactifications;
- stable quotients and resultant compactifications;
- component structure of Hilbert fibres under birational transformations.

The manuscript explicitly disclaims an exhaustive priority certificate, which is correct. That also means exceptional originality has not yet been established.

### 8.7 Ballico 1993 remains unresolved

The theorem/proof-level comparison with the closest named failure-locus predecessor remains unavailable. The papers disclose this limitation and do not invent a conclusion. That is responsible scholarship. It still prevents certification of broad historical originality for the failure-locus-to-reconstruction programme.

### 8.8 Paper I still lacks an independent proof audit

The sharp inverse theorem is central, long, and technically ambitious. Preservation manifests and repeated internal responses do not replace an independent mathematical proof audit. The v162 response correctly marks this request as open.

---

## 9. Architecture and exposition

The reading route is much better than in early revisions. Paper II now has a recognizable principal sequence:

1. universal power ideals;
2. contact parameters;
3. Euclidean Hilbert charts;
4. primitive jet-tail loci;
5. a non-equidimensional actual fibre;
6. reduced multiple incidence and exact contact slices;
7. inherited structural appendices.

Nevertheless, the package remains cumulative. Between the two papers it retains:

- the sharp inverse and its family forms;
- automorphism, recognition, covering, and rigidification results;
- all-rank power graphs;
- regular and singular spectral reconstruction;
- complete-quadric boundary geometry;
- divisor normalization and conductors;
- collision atlases;
- reciprocal-fibre homology;
- reduced multiple incidence;
- all-order slice singularities;
- stable-map comparisons;
- effective stack constructions;
- Euclidean Hilbert charts;
- jet-tail loci;
- the conic component.

The 137-page preservation master makes this accumulation explicit. For specialist publication, Paper II should be narrowed around the ambient Hilbert theorem, with inherited reciprocal-fibre and failure-orbit material moved to separate papers or an external reference. Paper I should be assessed independently on the sharp inverse.

---

## 10. Specific technical and expository requests

These points should be addressed even for a specialist submission.

1. **State the coefficient topology in Lemma 6.1.** Distinguish the base maximal-ideal completion from polynomial degree in the pencil parameter.

2. **Give a coordinate-free tangent map.** Write the morphism from the framed pencil tangent space to the contact quotient before choosing Jordan blocks.

3. **Isolate the orthogonal stabilizer lemma.** Prove its dimension and skew-adjoint block description separately.

4. **Separate framed and unframed dimensions.** Identify the source-frame, pencil-basis, and parameter-fixing directions in the count `N`.

5. **Keep miniversality formal.** Do not call the coefficient space an algebraic neighbourhood until the algebraic Hilbert chart is constructed.

6. **State the residual stabilizer action.** Explain which changes of miniversal coordinates preserve the embedded Hilbert point.

7. **Define `Gamma_a` as a graph over `B_a` in every theorem statement.** The inverse uses the retained base coefficients.

8. **Write the nonreduced union exact sequence for `Z_w`.** Include the restriction map and its surjectivity.

9. **Prove cohomology and base change uniformly near all central `w`.** The central locus has dimension `a`; the shrinking should work along the whole locus or be stated pointwise.

10. **Make the line-bundle cokernel argument explicit.** Record integrality, reducedness, rank, and the dense-open vanishing step.

11. **Track homogenization degrees in `Psi`.** The roles of the infinity coordinate and the missing leading coefficient of `q` should be visible in the displayed map.

12. **Clarify the chart at infinity.** State the exact affine cover and why no additional Hilbert choices occur there.

13. **Distinguish repeated-root primary structure from component decomposition.** The gcd law should use primary language at multiple roots.

14. **State the jet convention.** Explain why `Res_{C[x]/(x^a)/C} P^1=J_{a-1}(P^1)` under that convention.

15. **Prove smoothness and irreducibility of the Weil restriction.** Cite preservation of smoothness under finite locally free Weil restriction or give the two-chart argument.

16. **State the Hilbert polynomial in the algebraic primitive-tail construction.** Flatness of the union alone is not the complete Hilbert-functor check.

17. **Formulate the embedded deformation-functor comparison as a separate proposition.** This is the main proof obligation of Theorem 7.2.

18. **Draw the target diagram.** Distinguish the relative incidence target, the fixed complete-quadric target, and the Hilbert scheme.

19. **Explain `x`-dependent congruence precisely.** State why it does not identify distinct fixed-target Hilbert points and how it is undone in the comparison.

20. **State the ideal-sheaf gluing argument.** Identify the punctured open, the completed supports, and the faithful-flat descent step.

21. **Cite the formal criterion for étaleness.** List finite presentation and residue-field hypotheses.

22. **Separate normalization of the total graph from normalization of a fibre.** Use distinct notation throughout.

23. **Specify algebraic one-parameter realizations.** Do not alternate silently between formal arcs and algebraic curves.

24. **Stratify the resultant boundary by gcd type.** Even a set-theoretic partition with codimensions would clarify what the chart controls.

25. **Prove the irreducible-component closure lemma in Theorem 8.1.** State why the open jet locus lies in exactly one component.

26. **Construct the conic family through a relative ideal quotient.** This would prove the locally closed immersion in families.

27. **Show the conic parameterization is unique up to the source automorphisms already fixed.** The Hilbert family itself is unparameterized.

28. **State the finite-pullback dimension lemma.** Select a component dominating the conic family and prove its dimension is four.

29. **Determine whether the higher-dimensional component is exactly four-dimensional.** If not known, say so prominently.

30. **Describe at least one intersection point of the two components.** The current theorem proves distinct dimensions but no adjacency.

31. **Test the doubled-line boundary.** Degenerating smooth conics to doubled lines is the natural candidate for meeting the primitive thick-line component.

32. **Clarify reducedness of the normalized fibre.** A fibre of a normal total space can be nonreduced.

33. **Generalize or sharply motivate `(2,2)`.** Explain what is expected for `(a,b)` and which degree partitions should produce components.

34. **Do not call the primitive open a fibre classification.** It is an open chart, and Theorem 8.1 proves the complement is substantial.

35. **Keep the effective-stack limitation in every summary.** The transfer is not a theorem about all raw Artin-algebra deformations.

36. **Prove the semidirect-product automorphism group carefully.** Automorphisms of the source bundle and kernel automorphisms may form a nontrivial extension rather than a canonically split product without a chosen linearization.

37. **State the exact algebraicity claim for `BH_h`.** Specify the fixed object, topology, and automorphism functor.

38. **Keep `h=1` distinguished.** For `h>1` the envelope exponent is still an auxiliary choice even though the graph is unchanged.

39. **Expand the Hilbert-compactification literature.** Resultant map spaces and low-degree homogeneous-target comparisons are not the entire relevant field.

40. **Retain the Ballico limitation in both submitted papers.** Do not move it to repository metadata.

41. **Do not use finite checks as evidence of the general theorems.** The current seal correctly avoids doing so.

42. **Obtain an independent proof audit of Paper I.** This remains open and is essential before any general-journal evaluation.

43. **Reduce the claim surface.** A specialist Paper II should center Theorems 6.2, 7.1, 7.2, and 8.1 and move most inherited programmes elsewhere.

44. **Give a precise conjecture for the full fibre.** The new non-equidimensional example should lead to a testable component classification, not only another revision-specific extension.

---

## 11. Response-to-v161 scorecard

### Fully or substantially closed

- recognition that the old Jordan families were slices rather than versal neighbourhoods;
- computation of the full formal contact parameter module;
- realization of those parameters by honest pencil perturbations;
- an explicit open chart of the reduced Hilbert graph with a regular inverse;
- an exact gcd law inside that chart;
- algebraic primitive-tail loci in the actual normalized pencil fibre;
- proof that constant exceptional directions are too small for nonreduced contacts;
- an actual ambient non-equidimensional fibre at contact type `(2,2)`;
- many of the 38 technical requests concerning descent, Proj, flatness, normality, Artin coefficients, and invariant lifting classes;
- clearer separation of the effective failure category from all raw Artin algebras.

### Partially closed

- ambient classification of nonreduced incidence;
- comparison between formal congruence coordinates and the fixed-target Hilbert functor;
- component structure of nonreduced fibres;
- modular interpretation of the full pencil boundary;
- literature positioning for Hilbert graph compactifications;
- deformation-theoretic interaction with failure multiplication;
- focus and independence of the two papers.

### Still open

- classification of the entire fibre even for contact `(2,2)`;
- component and wall-crossing theory for general `(a,b)`;
- higher-corank and singular-pencil Hilbert neighbourhoods;
- interactions among multiple nonreduced contacts outside the primitive product open;
- a global compactification theorem encompassing all boundary types;
- an internal boundary operation visible in the closed finite algebra before reconstruction;
- a major external application;
- theorem/proof-level comparison with Ballico 1993;
- an independent proof audit of Paper I;
- a top-four-scale principle not assembled primarily from classical miniversality, complete quadrics, Rees geometry, and Hilbert-scheme formalism.

---

## 12. Conditions for another top-four evaluation

I would not recommend another top-four round triggered merely by one additional contact type, a larger check suite, another open chart, or further movement of inherited sections into appendices.

A serious new round should contain at least one result of genuinely new global scale, for example:

1. **A component theorem for general contact data.** Determine the irreducible components, dimensions, generic curves, and intersections of the normalized fibre for arbitrary corank-two Smith exponents.

2. **A global modular compactification.** Include nonreduced incidence, higher corank, singular pencils, and interacting support points in one proper moduli construction with a universal property.

3. **A wall-crossing or adjacency theory.** Explain how thick lines, reduced higher-degree tails, mixed tails, and multiple covers lie in common closures.

4. **A higher-corank ambient theorem.** Replace the binary Euclidean chart by a structural classification of the relevant matrix-gcd or module data.

5. **An internal finite-algebra boundary operation.** Construct boundary data directly from the closed algebra or its intrinsic deformation complex without first reconstructing the full pencil.

6. **A major external application.** Use the failure algebra or Hilbert boundary to solve an independently recognized problem.

The historical comparison with the closest named failure-locus predecessor should also be completed through a legitimate source, or the historical framing should remain permanently narrow.

---

## 13. Final assessment

Revision 162 deserves substantial credit. It is complete, reproducible, and mathematically stronger than v161. The contact directions are no longer represented by a misleadingly small slice. The Euclidean division family is promoted to an actual open Hilbert chart through a regular inverse. The primitive-tail locus is identified with jet schemes in the actual normalized fibre. Most importantly, the manuscript proves that a contact-`(2,2)` fibre has components of different dimensions, with thick line tails and reduced conic tails representing genuinely different embedded limits.

I therefore reject any characterization of v162 as cosmetic, merely computational, or merely repository engineering.

I nevertheless recommend rejection for *Annals*, *Acta*, *Inventiones*, or *JAMS*. The principal new geometry remains local to regular corank-two contacts. The formal-to-embedded comparison, while plausible, is compressed at the most category-sensitive step. The non-equidimensionality theorem treats one contact type and leaves the actual component geometry largely unknown. The global hard boundary, higher corank, singular-pencil Hilbert problem, component wall crossings, and external applications remain open. The failure-algebra interpretation still passes through reconstruction, the closest historical comparison remains incomplete, and Paper I still lacks an independent proof audit.

The appropriate assessment is therefore:

**Reject the v162 package in its present form for a top-four general mathematics journal.**

**Paper II is a serious candidate for a strong specialist venue in algebraic geometry, moduli, invariant theory, or Hilbert-scheme geometry after narrowing its scope and making the formal-to-embedded comparison completely explicit. Paper I likewise deserves specialist consideration after an independent proof audit and sharper historical positioning.**
