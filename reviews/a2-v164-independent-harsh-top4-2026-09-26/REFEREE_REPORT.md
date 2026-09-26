# Independent harsh referee report — A2 revision 164

## Manuscript and review object

**Submission package:**

1. *Finite failure schemes and the reconstruction of quadratic pencils* (Paper I, 73 pages);
2. *Power ideals and the Hilbert boundary of quadratic pencils* (Paper II, 89 pages);
3. the 155-page preservation master containing the complete mathematical bodies of both papers.

**Author:** Qian Qi  
**Revision reviewed:** A2 revision 164  
**Revision branch:** `revision/a2-v164-collision-wall-crossing-2026-09-26`  
**Locked branch tip:** `d7d476adbbbef0b91f55264bde030c72fc324e2b`  
**Authored mathematical-source commit:** `7a855e8cec0eb570ab2a1fa68a989644e876323a`  
**Complete manuscript materialization commit:** `1e52c491a84d948a7bee859ea300dc9702c63058`  
**Complete post-report v163 baseline:** `40a72ddfd85e16363385a1b64b922d61055e875c`  
**Controlling prior report:** `reviews/a2-v162-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md`  
**Controlling prior-report commit:** `7e9c057907cc4502858a54f32ab0c0cfa264680f`  
**Principal new sources:**

- `papers/A2-v17-boundary-information-coarsening/article/v163/embedded-comparison-v163.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v163/complete-contact-fibre-v163.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v163/products-and-strata-v163.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v164/collision-wall-crossing-v164.tex`;
- `papers/A2-v17-boundary-information-coarsening/article/v164/effective-collisions-v164.tex`.

**Complete focused sources:** `reconstruction.tex` and `divisor-geometry.tex`.

**Review standard:** the proof-completeness, originality, conceptual depth, inevitability, and expository standard expected at *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*.

A higher-numbered branch, `revision/a2-v165-general-contact-boundary-2026-09-26`, was present when this report was prepared, but it pointed to the same commit as v164 and its root review entry still designated revision 164 as the complete review object. I therefore did not treat that alias as a distinct manuscript.

This is an owner-requested independent-referee-style report, not a journal-commissioned editorial decision. I reviewed the complete materialized v164 package and the substantive post-v162 v163 inputs retained in it. I read the fixed-target embedded comparison, the Hilbert–Burch conic charts, the complete first nonreduced fibre theorem, the product-fibre theorem, the collision specialization, the ordered quadratic base change, the global nilradical calculation, the genuine symmetric-pencil realization, the response records, and the publication and literature audits. I also re-read the inherited universal power-ideal and sharp-inverse statements needed to evaluate the claimed interaction with failure multiplication.

The publication seal records complete standalone sources and PDFs, successful compilation, preservation of all predecessor mathematical blocks, and a rerun of the inherited exact checks. I use those records to identify the object and assess reproducibility. They are not proof certificates, priority certificates, or evidence for the editorial threshold.

## Recommendation

**Reject the v164 package in its present form for a top-four general mathematics journal.**

Revision 164, together with the unreviewed v163 material that it preserves, is a genuine and substantial mathematical advance over v162. The manuscript now does several things that earlier versions only gestured toward:

- it states the formal-to-embedded change of category as an equivalence of completed fixed-target quotient functors rather than silently quotienting by parameter-dependent congruences;
- it gives Hilbert–Burch charts with regular recovery maps around every conic tail;
- it determines the entire first nonreduced scheme fibre, not only selected line-tail and conic-tail families;
- it identifies the two reduced components as `P^4` and `F_2`, computes their intersection, and writes the exact nilpotent local ring;
- it proves product formulas for any number of distinct contacts of first nonreduced type;
- it computes a moving-support collision in which two reduced incidences merge into a contact of type `(2,2)`;
- it separates the flat horizontal closure from the nonflat full pullback and calculates the vertical excess and base torsion exactly;
- it gives an ordered quadratic cover with a normal-crossing central model and computes the monodromy;
- it globalizes the nilradical as `j_* O_{P^2}(-1)`;
- it realizes the collision by an explicit genuine `4 x 4` symmetric pencil in the fixed complete-quadric target.

These are real theorems. They are not cosmetic changes, source repackaging, repository bookkeeping, or enlarged experiment tables. I did **not** find a simple counterexample to the fixed-target comparison, the Hilbert–Burch family, the complete first-contact fibre, the product-fibre theorem, the horizontal quotient model, the torsion calculation, the ordered normalization, or the genuine-pencil realization. My recommendation is therefore not a concealed correctness rejection.

The top-four problem is instead one of mathematical scale, modular necessity, and conceptual reach.

The new collision theorem is a precise calculation along one discriminant curve,

`(f,g,r) = (x^2-delta,0,0)`,

inside the already computed first nonreduced contact neighbourhood. Its local algebra

`(eA,eB,e^2 C + delta)`

and its ordered blow-up quotient are elegant. But this remains the most elementary collision of two simple corank-two supports, producing the first balanced nonreduced contact `(2,2)`. The products in the multiple-collision corollary are products of independent copies at disjoint supports. The paper does not classify interacting collisions, unequal contact orders, higher contact length, higher corank, collisions through the singular-pencil locus, or global wall crossing among the components of the proper Hilbert fibre.

The phrase “wall crossing” is therefore too strong unless it is read informally. No stability parameter is varied, no chamber structure is constructed, and no birational transformations among modular compactifications are classified. The manuscript itself now correctly calls the result a collision specialization and distinguishes it from Mori or GIT wall crossing. The title and surrounding rhetoric should obey the same restriction.

The v163 complete-fibre theorem is the strongest result in the package. It determines the first nonreduced fibre exactly, including its nilpotent structure. Yet it treats only the case in which the smaller positive Smith exponent is at most two. For contact length at least three, the manuscript retains only a primitive open, resultant strata, and a conjecture about components. Thus the new global picture is still a first nontrivial model, not a compactification theorem for quadratic-pencil degenerations.

The failure-algebra interpretation also remains mediated by reconstruction. The finite algebra recovers the source and pencil; classical determinantal and complete-quadric geometry is then applied to that recovered pencil. This is a legitimate functorial consequence of the sharp inverse. It is not a boundary operation visible internally in the closed finite algebra before the inverse has essentially reconstructed the classical object.

Paper II is now a serious and potentially strong specialist paper. Paper I contains a striking inverse theorem and deserves independent specialist scrutiny. The combined package nevertheless remains below the threshold of the four general journals named above.

---

## 1. What v163 and v164 genuinely accomplish

### 1.1 The fixed-target comparison is finally formulated in the correct category

The manuscript now distinguishes three objects that earlier versions risked conflating:

1. formal symmetric matrix germs modulo parameter-dependent congruence;
2. relative incidence targets over the pencil parameter disc;
3. embedded curves in the fixed complete-quadric target.

The functor `D_X` retains the framed coefficient base, the universal pencil line, the fixed target, the Hilbert polynomial, and the forced lift away from the contact supports. Equality means equality of embedded ideal quotients; no ambient automorphism quotient is imposed.

The comparison functor applies a formal Schur splitting and congruence only on the completed incidence target, then explicitly undoes it before patching the ideal into the fixed target. This is the correct architecture. It directly addresses the principal categorical objection in the v162 report.

### 1.2 The use of actual image Rees algebras is responsible

The proof records the surjection

`R_R(J) tensor_R R' -> R_{R'}(JR')`

and uses the induced closed immersion of the actual image graph. It does not claim that arbitrary nonflat base change commutes with blow-up. This distinction is essential in precisely the nonflat situations later encountered in v164.

### 1.3 The Hilbert–Burch chart is a strong local theorem

The matrix

```
[ H    AF+CG ]
[-G    H+BF  ]
[ es   -z    ]
```

produces a height-two determinantal family whose minors define curves of Hilbert polynomial `3l+1`. At `e=0` the fibre is the scheme-theoretic union of the fixed main curve and a plane conic through the attaching point. The family includes smooth conics, reducible conics, and doubled lines.

The recovery argument is not merely a parameter count. It uses cohomology and base change to recover the quadratic equation and the two bilinear equations, and hence the parameters `lambda,A,B,C,c,e`, regularly from the Hilbert point together with its retained coefficient base.

### 1.4 The first nonreduced fibre is determined scheme-theoretically

At the central coefficient point `(x^2,0,0)`, the local fibre ring is

`C[lambda,e,A,B,C]/(eA,eB,e^2 C)`.

Its two minimal components are:

- the conic component `P^4`, given locally by `e=0`;
- the compactified primitive component `F_2`, given locally by `A=B=C=0`.

Their reduced intersection is the projective line of doubled lines. The embedded associated prime and the square-zero nilradical are also visible in the primary decomposition.

This is a genuine improvement over v162, where only a two-dimensional jet component and a distinct component of dimension at least four had been established.

### 1.5 The proper-fibre exhaustion is no longer a dimension guess

The two algebraic families are shown to be proper closed subschemes of the fibre. Their union is locally open in the support because the explicit charts contain no further branch. Connectedness of the fibre of the proper birational normal total graph then makes this union the entire support.

The argument is conceptually sound. It is stronger than inferring completeness from dimensions or from a list of closed points.

### 1.6 Distinct first contacts factor as products

For contacts with smaller Smith exponent `a_i` in `{1,2}`, the manuscript identifies the complete scheme fibre as

`X_2^r x (P^1)^s`.

It computes all `2^r` reduced components, all their intersections, the exact nilpotence order `r+1`, and the Euler characteristic. This is an actual scheme-product theorem, not only a product formula for supports.

### 1.7 The moving-support collision is computed exactly

For the coefficient curve `(x^2-delta,0,0)`, the manuscript distinguishes:

- the full pullback `H` of the normalized total Hilbert graph;
- the schematic horizontal closure `Y` of the generic fibres after base change.

The local chart

`C[lambda,e,A,B,C,delta]/(eA,eB,e^2 C+delta)`

makes this distinction transparent. Eliminating `delta` gives the reduced union `(eA,eB)=(e) cap (A,B)`, while saturation by `delta` removes the vertical component and leaves `(A,B)`.

### 1.8 The quotient model explains the multiplicity-two component

The horizontal space is identified with

`Bl_{Delta x {0}}(P^1 x P^1 x A^1_t) / ((l_+,l_-,t) ~ (l_-,l_+,-t))`,

with `delta=t^2`. Its central Cartier divisor is

`F_2 + 2 P^2`.

After the quadratic root cover and normalization, the two components become reduced and meet normally. This gives a clean geometric explanation for the multiplicity two: it records the loss of ordering of the colliding support points.

### 1.9 The vertical excess and torsion are not hidden

The full pullback has a vertical `P^4` of conics through the attaching point. It meets the horizontal model along the singular-at-the-attachment `P^2`. The structure-sheaf union sequence is exact, and the entire `delta`-torsion is

`i_* I_{P^2/P^4}`.

This is a precise and useful distinction between a flat horizontal limit and a nonflat pullback.

### 1.10 The nilpotent module is globalized

The local nilpotent generator does not determine its global twist. The collision divisor calculation proves

`N_{X_2} = j_* O_{P^2}(-1)`, `N_{X_2}^2=0`.

The coherent cohomology calculation then follows from exact sequences for the reduced union and the acyclicity of `O_{P^2}(-1)`.

### 1.11 A genuine symmetric-pencil family realizes the model

The direct sum of two copies of

```
[-delta s   t]
[    t     -s]
```

has two reduced corank-two incidences for `delta != 0` and one contact of type `(2,2)` at `delta=0`. The displayed polynomial congruence reduces it to the retained coefficient triple `(x^2-delta,0,0)` on the relative incidence target, and is undone before returning to the fixed target.

This makes the collision theorem an actual statement about symmetric pencils rather than only a universal polynomial graph.

---

## 2. Correctness audit of the fixed-target comparison

I did not find a fatal correctness error in the comparison theorem, but this is the most technically delicate inherited input and it still deserves substantial expansion.

### 2.1 The deformation functors should be stated as categories, not only sets

The current exposition says that objects are embedded ideal quotients and that isomorphism means equality. That is enough for the intended Hilbert functor, but the comparison is repeatedly called an equivalence of functors. The final version should specify the base category, the retained coefficient maps, and whether the functors are set-valued, groupoid-valued, or fibre categories.

Because equality is imposed in the fixed target, the intended object is set-valued. Saying this explicitly would remove needless stack-theoretic ambiguity.

### 2.2 The formal patching theorem is load-bearing

The patching lemma invokes completion plus the open complement and permits quotients with torsion at the contact. This is exactly what is needed. The final version should nevertheless list, in one place:

- the Noetherian hypotheses;
- the closed support along which completion is taken;
- the punctured-completion overlap;
- finite presentation of the quotients;
- compatibility of the algebra structures and incidence equations;
- the criterion used to descend base flatness.

At present these facts are distributed between the lemma and later applications.

### 2.3 Completion and saturation require an explicit lemma

The argument that the closure ideal commutes with completion uses stabilization of a sequence of colon ideals and flatness of completion. This is plausible, but it should be isolated as a statement:

`(I : J^infinity) completed = (I completed : (J completed)^infinity)`

under the exact Noetherian and faithful-flatness hypotheses used here.

The proof should identify the finite exponent at which both sides stabilize. It should not rely on a general slogan that completion commutes with schematic closure.

### 2.4 Reducedness of completed graph charts should be cited precisely

The manuscript uses excellence of complex finite-type algebras to assert that the relevant reduced completions remain reduced. The precise analytically-unramified or geometrically reduced formal-fibre result should be cited at the point of use.

### 2.5 Parameter-dependent congruence remains conceptually dangerous

The paper now treats it correctly, but the proof would be much easier to audit if it contained a commutative diagram showing:

- the original incidence target;
- the completed normal-coordinate target;
- the isomorphism `Theta_i`;
- the fixed complete-quadric target;
- the maps that undo `Theta_i` before the Hilbert point is formed.

This is the central distinction on which the entire post-v162 programme rests.

### 2.6 Algebraization should be separated from formal comparison

The proof now has the correct order:

1. construct an algebraic finite-presentation family;
2. compare completed local rings;
3. use the formal criterion for étaleness;
4. use recovery to prove monomorphism;
5. conclude open immersion.

This should be made a named proposition. It is presently embedded inside a long proof, where a reader can too easily mistake the completed equivalence itself for an algebraization theorem.

### 2.7 Changes of frames need an explicit cocycle check

The text states that alternative congruences conjugate the two functors and cancel after returning to the fixed target. This is plausible. The final paper should write the overlap transformation and verify the cocycle identity on triple overlaps of the framed atlas.

### 2.8 The retained coefficient base is indispensable

Several recovery maps would fail if one forgot the projection to `B_a`. The manuscript now says this. It should be repeated in every theorem summary: the Hilbert point alone is not being inverted; the coefficient-base point is part of the graph object.

---

## 3. Correctness audit of the Hilbert–Burch chart

### 3.1 Fibrewise height two is the key hypothesis

The use of the Hilbert–Burch complex is appropriate if the minors have the asserted height in every geometric fibre. The proof checks the generic graph and the special conic union. It should state why no intermediate parameter value causes a height drop.

The simplest organization would be to prove directly that the three minors have no common codimension-one factor on any fibre, then invoke the standard perfect-height-two criterion.

### 3.2 Flatness of the cokernel should cite the exact criterion

The complex consists of base-flat locally free sheaves and is exact on every geometric fibre. The manuscript should cite the fibrewise exactness criterion used to conclude exactness and flatness over the parameter space.

### 3.3 The conic at infinity is handled correctly

At `s=0`, the equations force `G=H=0`, so no hidden component or additional choice appears. This small calculation is load-bearing and should remain in the main proof.

### 3.4 The recovery of `A,B,C,lambda` is credible

The line of quadratic equations and the rank-two space of bilinear equations are recovered by cohomology and base change. Normalizing the `R^2` coefficient and completing the square recovers the conic parameters. The coefficient projection recovers `f` and hence `c`; the normalized bilinear equations recover `e`.

The manuscript should display the ranks of all ambient restriction maps and identify the open minors whose nonvanishing defines the recovery neighbourhood.

### 3.5 Doubled lines must remain included

The proof correctly uses the exact sequence of a degree-two plane hypersurface, so the cohomology dimensions remain valid for a doubled line. This should be highlighted because the entire component-intersection theorem depends on it.

### 3.6 The target-coordinate changes are charts, not quotient identifications

The manuscript says this correctly. The final prose should avoid any phrase suggesting that conics related by a target automorphism define the same Hilbert point.

---

## 4. Correctness audit of the complete first nonreduced fibre

### 4.1 The fibre ideal is computed without radicalization

Specializing the base map gives exactly

`(c,eA,eB,e^2 C)`.

This is the correct scheme-theoretic input. In particular the nilpotent structure is not reconstructed after first passing to the reduced support.

### 4.2 The primary decomposition is consistent

The decomposition

`(eA,eB,e^2 C) = (e) cap (A,B,C) cap (A,B,e^2)`

is correct as a monomial calculation. The two minimal primes and the embedded associated prime give the stated failure of Cohen–Macaulayness.

### 4.3 The nilradical calculation is correct

The radical is `(eA,eB,eC)`, so the nilradical is generated by `eC`, with

`Ann(eC)=(e,A,B)` and `(eC)^2=0`.

The support condition `A=B=0` is exactly the plane of conics singular at the attaching point.

### 4.4 The compactified primitive component is plausibly `F_2`

The transition

`e'=-w_0^2 e`

is the transition of the compactification of `T P^1 = O(2)`, with the infinity section of self-intersection `-2`. The adjacency family gives the doubled-line boundary.

The final paper should give the convention for `P(O plus O(2))`, since quotient-line and subline conventions reverse which section has self-intersection `-2`.

### 4.5 The exhaustion argument is acceptable but should be tightened

The union of the two constructed families is proper and closed. The local charts show it is open in the support at every one of its points. Connectedness of the proper fibre then forces it to equal the support.

The final version should explicitly state:

- why `tilde Gamma_2 -> B_2` is proper and birational;
- why `B_2` is normal;
- why Stein factorization gives geometrically connected fibres;
- why the constructed union is nonempty and open-and-closed in the underlying topological fibre.

These facts are present, but the logical chain should be placed in one paragraph.

### 4.6 Support exhaustion is not by itself scheme exhaustion

The scheme structure is recovered because the Hilbert–Burch and jet charts cover every point of the support and give the displayed local fibre ring. The paper should say this immediately after the connectedness argument. Otherwise a reader may think connectedness alone determined the nilpotent structure.

### 4.7 The statement about exactly two irreducible components is justified

The reduced components are smooth, distinct, proper, and cover the support. Their intersection is reduced. No third branch is visible in any local chart, and connectedness rules out a disjoint hidden component.

I found no contradiction in this part.

---

## 5. Correctness audit of the product-fibre theorem

### 5.1 Disjoint supports make the local data independent

At distinct spectral points, the finite supported ideal quotients live on disjoint neighbourhoods. The use of the fixed main curve and forced lift outside the supports makes it plausible that the local families patch as a product.

### 5.2 The nilpotent parameters are finite, not merely formal

At a length-two contact, the quotient of the main ideal by the curve ideal is killed by `x^2`; at a length-one contact it is killed by `x`. This is an important observation. It permits algebraic gluing using only finite contact neighbourhoods.

### 5.3 The open-immersion argument should identify its representability input

The completed local maps are isomorphisms and recovery makes the morphism a monomorphism. The formal criterion then gives an étale monomorphism, hence an open immersion. The final version should state the exact finite-type representability theorem used for the morphism to the Hilbert fibre.

### 5.4 Proper plus open immersion gives an open-and-closed image

The source product is proper, so the open immersion is also closed. Connectedness of the fibre then gives surjectivity. This is sound provided the preceding representability and completed-local statements hold at nilpotent points, not only closed reduced points.

### 5.5 The arbitrary larger exponent `b_i` needs a clear invariant explanation

The theorem depends only on the smaller exponent `a_i`. The text explains that the polynomial `k_i` is a smooth factor removed by an invertible generating-row operation and then restored in the fixed incidence target.

This is plausible but should be stated as a lemma about the embedded graph ideal, not only as an observation inside the proof.

### 5.6 The nilpotence order `r+1` is correct

The total nilradical is the sum of the pullbacks of the square-zero radicals. Every monomial of degree `r+1` repeats a factor and vanishes, while the tensor product of one nonzero nilpotent from each factor survives on a product affine chart.

### 5.7 The theorem remains sharply limited to `a_i <= 2`

This scope restriction is mathematically essential. It must remain visible in the abstract, introduction, and every top-level claim about “complete fibres.”

---

## 6. Correctness audit of the collision theorem

### 6.1 The base-changed local ring is the right starting point

Substitution into the conic chart gives

`C[lambda,e,A,B,C,delta]/(eA,eB,e^2 C+delta)`.

The calculation retains the coefficient base and occurs in a regular chart of the normalized total graph. No fibre normalization or pointwise radical is introduced.

### 6.2 Horizontal saturation is computed correctly

After eliminating `delta`, the ideal is `(eA,eB)`. Saturating by `delta=-e^2 C` removes the component `e=0` and leaves `(A,B)`. The horizontal chart is therefore `C[lambda,e,C]` with `delta=-e^2 C`.

The paper should write the finite colon calculation explicitly, not only state the saturation result.

### 6.3 The full pullback is reduced

The identity

`(eA,eB)=(e) cap (A,B)`

exhibits the two reduced components. Their intersection is the reduced plane `e=A=B=0`.

This is compatible with the fact that the special fibre is nevertheless nonreduced after imposing `delta=0`.

### 6.4 The invariant quotient charts are convincing

On the ordered blow-up charts, the involution has invariant rings

- `C[lambda,e,C]`, with `C=-d^2` and `delta=-e^2 C`;
- `C[lambda,u,delta]`, with `delta=t^2`.

These are polynomial rings. Thus smoothness of the quotient is proved directly even along the fixed exceptional divisor; no false free-action theorem is used.

### 6.5 The global cover by common affine direction coordinates should be expanded

The proof says that one may choose a point of `P^1` outside either of two specified directions as infinity. This gives affine charts covering all ordered pairs. The quotient gluing is plausible, but the final version should write the transition functions for the direction coordinate and the descended ample line bundle.

### 6.6 Projectivity of the quotient is not automatic from finiteness

The manuscript gives a valid route: take a relatively ample bundle on the blow-up, tensor its translates, take an even power to trivialize stabilizer actions, and descend. This should be stated as a separate lemma or cited precisely.

### 6.7 Flatness of the horizontal model is correct, but the sentence should be fixed

The relevant fact is that an integral `C[delta]`-algebra dominating the base is torsion-free over the PID `C[delta]`, hence flat. Equivalently, after localizing **the base** at a prime one obtains a field or a DVR, and torsion-free modules over a valuation ring are flat.

The manuscript currently risks sounding as if nonfield localizations of the coordinate ring of the threefold were DVRs. That would be false. The final wording must say explicitly that the localizations are those of `C[delta]`.

### 6.8 The divisor multiplicities follow from the local equation

In the horizontal chart,

`delta=-e^2 C`.

Thus `S=(e=0)` has multiplicity two and `E=(C=0)` has multiplicity one. Their reduced intersection is transverse.

### 6.9 The identifications `E=F_2` and `S=Sym^2 P^1` are natural

The strict transform of `t=0` in the ordered model quotients to the symmetric square. The exceptional divisor is `P(O(2) plus O)`, and the involution acts trivially projectively because it changes both normal coordinates by `-1`.

### 6.10 The normal bundle computation is consistent

Since `E+2S` is principal and `E|_S` is the doubled-line conic of degree two, one obtains `O_S(S)=O_{P^2}(-1)`.

The final paper should specify the divisor-class convention and explain why `Pic(P^2)` has no 2-torsion; it presently does this only briefly.

### 6.11 The union sequence is scheme-theoretic

The local intersection formula gives

`0 -> O_H -> O_Y plus O_{P^4} -> O_{P^2} -> 0`.

This is not merely an equality of supports. It is the correct structure-sheaf sequence for the reduced union.

### 6.12 The torsion calculation is plausible and exact

The annihilator of `delta=-e^2 C` in the full pullback ring is the ideal of the horizontal-intersection plane inside the vertical component. The standard two-term resolution of `C` over `C[delta]` identifies this annihilator with `Tor_1`.

The paper should explicitly state that higher `Tor` groups vanish because the base ring has projective dimension one for this quotient.

### 6.13 Exhaustion of the full pullback depends on v163

The assertion that there is no further vertical component uses the complete first-contact theorem to cover the central fibre and the reduced-incidence theorem to cover the generic fibres. This dependence is legitimate and now explicit.

The final theorem statement should mention the dependence rather than presenting the collision calculation as self-contained.

---

## 7. Correctness audit of the ordered model and monodromy

### 7.1 The normalization after `delta=t^2` is explicit

In the first chart the base-changed ring is

`C[lambda,e,C,t]/(t^2+e^2 C)`.

Adjoining `d=t/e` gives `d^2=-C` and the polynomial ring `C[lambda,e,d]`. In the second chart one already has `C[lambda,t,u]` with `d=tu`. These finite normal charts glue to the ordered blow-up.

### 7.2 The same-function-field assertion should be written carefully

The element `d=t/e` is considered in the common function field, where `e` is nonzero generically. The paper should state explicitly that the horizontal model is integral and that the finite extension is birational before invoking normalization.

### 7.3 The central ordered fibre is reduced normal crossing

The local equation `t=ed` gives the two reduced branches. This is a semistable model of the parameter space. The manuscript correctly warns that it is not automatically a stable-map replacement for every embedded curve represented by the parameter space.

### 7.4 The monodromy calculation is elementary but correct

On the root cover the generic family is the constant ordered product. Descent around `delta=0` interchanges the roots and hence the two ruling classes. The invariant and anti-invariant lines in `H^2` are therefore both one-dimensional.

### 7.5 This is not yet a general wall-crossing theory

There is no chamber decomposition, no variation of a stability parameter, and no classification of birational models. The result should be described as ordered semistable reduction of one collision family.

---

## 8. Correctness audit of the global nilradical and cohomology

### 8.1 The local nilradicals agree under the horizontal quotient

The full fibre chart and horizontal central chart both have nilradical generated by `eC`. The map identifies these modules on the singular-conic plane and they vanish away from it.

### 8.2 The divisor computation determines the twist

For the divisor `E+2S` in the smooth horizontal threefold, the nilradical of its scheme fibre is

`O(-E-S)/O(-E-2S) = O_S(-E-S) = O_S(S)`.

Together with `O_S(S)=O(-1)`, this gives the claimed global module.

### 8.3 The square-zero extension is not proved split

The manuscript correctly avoids this stronger assertion. The module identification alone does not determine the algebra extension class.

A worthwhile next step would be to compute that extension class in an appropriate `Ext^1` group and decide whether it contains additional moduli information.

### 8.4 The coherent cohomology calculation is straightforward

The reduced support is `P^4 union F_2` along `P^1`. Each component and the intersection have no higher structure-sheaf cohomology, and the map on constants is surjective. The nilpotent module `O_{P^2}(-1)` is acyclic. The stated cohomology follows.

### 8.5 Constant coherent cohomology does not imply flatness or reducedness

The manuscript explicitly says this. That warning should remain.

### 8.6 Product cohomology follows by Künneth

Over `C`, the product formula is routine once the one-factor result is known. It is not an independent originality claim.

---

## 9. Correctness audit of the genuine pencil realization

### 9.1 The polynomial congruence is correct

On the affine chart, the matrix

`U(x)=[[1,0],[x,1]]`

satisfies

`U(x)^T L_delta(1,x) U(x)=diag(x^2-delta,-1)`.

The determinant is one, and the congruence is polynomial in the pencil parameter.

### 9.2 The incidence behaviour is correct

The full determinant is `(t^2-delta s^2)^2`. For nonzero `delta` there are two reduced corank-two points; at zero there is one point with exponents `(2,2)`. The member at infinity is nonsingular.

### 9.3 The retained coefficient triple is obtained by an invertible row operation

After placing the two unit blocks first, the residual matrix is `f I_2`. Replacing the third normal coordinate by its difference with the first gives `(f,0,0)`.

### 9.4 The use of `U(x)` in a fixed target is properly scoped

The congruence acts on the relative incidence target over the parameter line and is undone before the curve is regarded as a fixed-target Hilbert point. This is exactly the distinction demanded in the v162 report.

### 9.5 The full-pullback comparison still depends on completed functors

The proof constructs an algebraic finite supported quotient and then uses the embedded comparison to show it is inverse to restriction from the actual pencil family. This is credible, but the dependency should be emphasized in the proposition statement.

### 9.6 The effective failure-family transfer adds no new internal operation

The transfer is through the established equivalence on the effective pencil image. It does not extend to all raw Artin-algebra deformations and does not produce a boundary directly from a closed failure algebra before reconstruction.

---

## 10. Why the top-four threshold is still not met

### 10.1 The complete classification stops at the first nonreduced contact

The paper completely handles contacts with smaller Smith exponent one or two. For exponent at least three, the full fibre is not classified. The manuscript itself labels the proposed component picture as a conjecture.

A top-four compactification paper would normally identify a general organizing principle, not stop after the first nontrivial fibre.

### 10.2 The new collision is one special discriminant path

The base curve `(x^2-delta,0,0)` merges two simple supports symmetrically. It does not treat:

- unequal moving residual directions;
- collisions with nonzero `g` or `r` jets;
- asymmetric ramification of support points;
- a simple point colliding with an already thick contact;
- collision of contacts of different lengths;
- collision through corank at least three;
- singular pencils in the Hilbert problem.

The products of independent copies do not address these interactions.

### 10.3 “Wall crossing” is not established

The manuscript computes a specialization and an ordered semistable model. It does not vary a stability condition, construct chambers, or compare modular birational models. The literature audit itself acknowledges this.

The revision and any paper title should use “collision specialization,” “support collision,” or “semistable collision model,” not “wall crossing,” unless an actual wall-crossing theorem is added.

### 10.4 The horizontal closure is path-dependent data

For the chosen curve, saturation by `delta` selects the flat horizontal component. The paper does not construct a universal flattening modification of the full contact base whose pullback gives these horizontal closures for all arcs.

A genuinely global theorem would identify a canonical flattening stratification, blow-up, logarithmic modification, or modular compactification controlling all collision directions simultaneously.

### 10.5 The vertical excess has not been given a modular meaning

The extra `P^4` consists of all conic tails at the central point, while only the singular-at-the-attachment `P^2` is reached horizontally from two separated incidences along this path. This is an attractive observation.

But the paper does not explain whether the vertical component represents:

- limits requiring a different base direction;
- a separate modular boundary condition;
- an obstruction to flatness of a universal compactification;
- a component selected by another stability parameter;
- an excess normal cone or derived intersection.

Without such an interpretation, the calculation remains local geometry rather than a broad moduli principle.

### 10.6 The quotient model is built from standard ingredients

The ordered blow-up, symmetric-square quotient, quadratic root cover, and normal-crossing central fibre are classical mechanisms. The manuscript uses them accurately. Their application to this coefficient Hilbert graph is new in context, but not of unmistakable general-journal scale by itself.

### 10.7 The nilradical twist is elegant but fibre-specific

`O_{P^2}(-1)` is a satisfying global answer. It does not yet lead to a general formula for nilpotent sheaves in contact fibres of arbitrary length or for interactions among several nonreduced contacts.

### 10.8 Independent collision products are formal consequences

Once one collision factor and the static product theorem are known, the `r`-fold component list and multiplicities are obtained by products. They are useful, but they should not be counted as a second global classification theorem.

### 10.9 Higher corank remains outside the Hilbert classification

The package contains all-rank power graphs and singular-pencil invariants, but these do not classify Hilbert boundary fibres at higher corank. The hardest geometric cases remain separate from the complete-fibre theorem.

### 10.10 Singular pencils remain outside the moving-boundary theorem

Minimal indices are recovered by the inherited invariant theorem. There is still no Hilbert compactification theorem describing how singular Kronecker blocks contribute components, multiplicities, or nonnormalities to the boundary.

### 10.11 The failure algebra still does not bypass classical reconstruction

The boundary is an invariant of the failure algebra because the pencil itself is already recovered. The programme has not yet exhibited a deformation or boundary construction internal to the multiplication table that reveals new geometry before reconstruction.

### 10.12 Paper I's invariant remains deliberately information-bearing

The sharp inverse theorem is striking, but the algebra is constructed so that its first relation contains the determinant factor and residual pencil data. The achievement is intrinsic recovery after forgetting coordinates, grading, and markings.

This is substantial specialist mathematics. It is not the discovery that a classical independently central invariant unexpectedly determines a pencil.

### 10.13 No major external application is obtained

The new results do not solve a recognized problem about:

- compactifications of matrix pencils;
- Hilbert schemes of rational curves in complete quadrics;
- singularities of complete quadrics;
- deformation theory of symmetric determinantal ideals;
- enumerative geometry of pencil degenerations;
- wall crossing for stable maps, quotients, or quasimaps;
- flattening of a known universal family.

The applications remain mainly internal to the constructed failure-algebra pipeline.

### 10.14 The historical comparison remains incomplete

The theorem/proof-level text of Ballico 1993 has still not been obtained. The manuscript is honest about this, which is commendable. It also means that exceptional historical originality of the broad failure-locus programme remains uncertified.

### 10.15 The literature positioning for collisions is too narrow

The v164 audit adds one paper on moduli of conics and correctly distinguishes its object. A stronger comparison should address:

- relative Hilbert schemes and flattening stratifications;
- degenerations of embedded rational curves;
- expanded and logarithmic degenerations;
- symmetric products and Hilbert–Chow type collisions;
- wonderful compactifications of incidence arrangements;
- stable pairs and stable quotients in fixed targets;
- normal cones and excess intersection in nonflat pullbacks.

### 10.16 The architecture remains cumulative

Between the two papers the package contains:

- the sharp inverse;
- family and stack forms;
- recognition and automorphism results;
- complete quadrics and all-rank power graphs;
- regular and singular spectral reconstruction;
- common-divisor normalization and conductors;
- homological fibre invariants;
- reduced multiple-incidence blow-ups;
- arbitrary-order slices;
- formal contact coordinates;
- Euclidean Hilbert charts;
- the full first nonreduced fibre;
- product fibres;
- collision specialization;
- effective failure-family transport.

Long papers are appropriate when one central theorem forces a long proof. Here the length still reflects a research pipeline of successive extensions. The top-four case would be stronger if Paper II were rebuilt around one global compactification theorem and the rest separated into companion work.

### 10.17 Paper I still lacks an independent proof audit

The publication seal explicitly says no new external independent audit of the 73-page sharp inverse was obtained. Since all intrinsic interpretations of the boundary rely on that inverse, this remains a material confidence issue.

I do not treat preservation manifests or repeated internal revisions as a substitute for an independent mathematical audit.

---

## 11. Specific technical and expository requests

These points should be addressed even for a specialist submission.

1. **Rename the collision result accurately.** Avoid “wall crossing” unless a stability parameter and chamber structure are introduced.

2. **State the review object unambiguously.** Explain that the higher-numbered v165 branch is an alias of the v164 tip, not a new revision.

3. **Define the embedded deformation functors as set-valued functors or fibre categories.** Specify morphisms and retained base maps.

4. **Give a single target diagram for every formal comparison.** Include the incidence target, normal-coordinate target, fixed complete-quadric target, and undoing maps.

5. **State the exact formal patching theorem and hypotheses.** Include torsion quotients and flatness detection.

6. **Isolate completion–saturation compatibility as a lemma.** Record the finite stabilization exponent.

7. **Cite reducedness of completed excellent complex algebras precisely.** Do not use “excellent” as a one-word proof.

8. **Write the frame-change cocycle explicitly.** Verify the triple-overlap identity.

9. **Separate algebraic construction, completed comparison, and étale monomorphism into distinct propositions.**

10. **State that the coefficient-base projection is part of every graph point.** Do not advertise inversion from an unlabelled Hilbert curve alone.

11. **Give the fibrewise height-two argument for the Hilbert–Burch minors in one place.** Cover all parameter values.

12. **Cite the fibrewise exactness and flatness criterion for the Hilbert–Burch complex.**

13. **Display the ambient restriction-map ranks used in conic recovery.** Identify the open minors.

14. **Keep doubled conics in every cohomology statement.** Their inclusion is essential.

15. **Fix the projectivization convention for `F_2`.** Identify the negative section without ambiguity.

16. **Write the connectedness argument as a complete lemma.** State properness, birationality, normality, and Stein factorization.

17. **After support exhaustion, explicitly invoke the local charts to recover the whole scheme structure.**

18. **State the exact associated primes of the first-contact fibre globally.** Explain where the embedded prime disappears.

19. **Compute or at least locate the square-zero extension class of `O_{P^2}(-1)`.** The module alone is not the algebra.

20. **Give a named lemma showing that the larger Smith exponent is a smooth graph factor.** This is load-bearing in the product theorem.

21. **State representability of the product-to-Hilbert morphism before applying the formal étaleness criterion.**

22. **Check completed local isomorphisms at nonreduced points, not only closed reduced points.**

23. **Explain unlabelled descent of the product fibres without choosing global spectral labels.**

24. **Write the horizontal saturation colon calculation explicitly.**

25. **Correct the flatness wording.** The DVRs are localizations of `C[delta]`, not arbitrary localizations of the threefold coordinate ring.

26. **Prove the finite quotient is projective in a separate lemma.** Include the descended ample bundle.

27. **Give all overlap maps of the invariant quotient charts.** Do not rely only on a common-affine-coordinate sentence.

28. **State where the involution is fixed and why the invariant rings remain regular there.**

29. **Separate the strict-transform and exceptional divisors on the ordered blow-up before quotienting.** Track their ramification indices.

30. **Derive `O_S(S)=O(-1)` with explicit divisor classes.**

31. **State the exact global ideal of the singular-at-the-attachment plane inside the conic `P^4`.**

32. **Identify all higher Tor groups of the full pullback over `C[delta]`.**

33. **Explain why the conic and primitive charts exhaust every point of the central pullback.** Cite the exact v163 results.

34. **State the common function field in the quadratic-base-change normalization.**

35. **Distinguish normalization of the total space, normalization after base change, and normalization of a fibre in every theorem statement.**

36. **Make the monodromy local system explicit.** State the base point, loop, and identification of ruling classes.

37. **Do not call the ordered parameter-space model a stable reduction of the embedded curves.** The manuscript currently warns against this; retain the warning.

38. **Compute the extension class of the nonreduced central fibre or state it as an open problem.**

39. **Give a functorial formulation of horizontal closure.** Clarify its dependence on the chosen base curve.

40. **Develop a universal flattening question.** Explain whether the horizontal model is pulled back from a modification of the full contact base.

41. **Explain the modular meaning of the vertical `P^4`.** At present it is an excess component with no broader universal property.

42. **Distinguish collision of supports from variation of stability.** Update title, abstract, and section headings consistently.

43. **Extend the literature review beyond one conic-moduli paper.** Compare relative Hilbert and logarithmic degeneration frameworks.

44. **State precisely which collision arcs are covered.** The theorem treats `(x^2-delta,0,0)`, not a miniversal collision family.

45. **Do not count independent products as interacting collision theory.** They are disjoint-support consequences.

46. **Keep the restriction `a_i in {1,2}` in all complete-classification summaries.**

47. **Separate higher-contact conjectures visually from proved theorems.**

48. **Do not infer a Hilbert-boundary classification for singular pencils from recovery of Kronecker invariants.**

49. **Keep the effective-image restriction in every failure-algebra application.**

50. **Do not present the boundary as internal to the closed algebra before reconstruction.**

51. **Narrow Paper II around the fixed-target comparison, first complete fibre, and collision model.** Move older reciprocal-fibre material to a companion or appendix volume.

52. **Obtain an independent proof audit of Paper I.** The sharp inverse is too central to rest only on internal preservation records.

53. **Complete the Ballico 1993 comparison through a legitimate source or maintain permanently narrow historical claims.**

54. **Separate finite symbolic checks from evidence for universal proofs.** The current receipts do this; keep it that way.

---

## 12. Response-to-v162 scorecard

### Fully or substantially closed

- a separate fixed-target embedded comparison theorem;
- explicit retention of the coefficient base;
- formal ideal patching with torsion allowed;
- actual image Rees algebras rather than unrestricted blow-up base change;
- algebraic construction before formal comparison;
- complete first nonreduced fibre, not only lower bounds on components;
- exact component dimensions `4` and `2`;
- reduced intersection along the doubled-line `P^1`;
- explicit nonzero square-zero nilradical;
- scheme-product fibres at distinct contacts of lengths one and two;
- exact nilpotence order in those products;
- a moving-support collision calculation;
- a genuine fixed-target symmetric-pencil realization;
- explicit distinction between horizontal closure and nonflat pullback;
- exact vertical torsion;
- quadratic ordering cover and monodromy;
- global nilradical line-bundle twist.

### Partially closed

- fixed-target algebraization beyond the displayed finite contact classes;
- complete classification of nonreduced fibres;
- modular meaning of the different components;
- collision and adjacency among boundary components;
- deformation-theoretic interaction with the failure algebra;
- literature positioning for embedded Hilbert degenerations;
- organization of Paper II around one central theorem.

### Still open

- full fibres for contact length at least three;
- higher-corank Hilbert fibres;
- Hilbert boundary of singular pencils;
- interacting collisions of unequal or nonreduced contacts;
- a miniversal collision theorem rather than one discriminant path;
- a global flattening or logarithmic compactification;
- chamber or stability wall crossing;
- an internal boundary operation on the finite algebra before reconstruction;
- a major external application;
- an independent proof audit of Paper I;
- theorem/proof-level comparison with Ballico 1993;
- a top-four-scale global principle not assembled from classical complete quadrics, Hilbert–Burch charts, Rees geometry, and finite quotients.

---

## 13. Conditions for another top-four evaluation

I would not recommend another top-four round triggered by another special one-parameter collision, a larger exact-check suite, a further product corollary, or another local invariant of the first nonreduced fibre.

A serious new round should contain at least one result of genuinely global scale, for example:

1. **A classification of the complete contact fibre for arbitrary smaller Smith exponent `a`.** This should include components, dimensions, intersections, nilpotent structure, and normalization.

2. **A miniversal collision theorem.** It should classify horizontal closures and vertical excess for all arcs in a neighbourhood of a collision stratum, not only `(x^2-delta,0,0)`.

3. **A universal flattening or modular compactification.** The horizontal models should arise from a canonical modification of the full pencil base with a universal property.

4. **A higher-corank and singular-pencil Hilbert theory.** This should connect Kronecker data to actual boundary components and scheme structures.

5. **A genuine wall-crossing theorem.** Introduce a stability parameter, chambers, birational models, and transformations of boundary strata.

6. **A boundary operation internal to the finite algebra.** It should reveal the modification without first reconstructing the complete pencil and importing classical determinantal geometry.

7. **A major external application.** Use the sharp invariant or the boundary calculation to solve a recognized problem independent of this internal pipeline.

8. **An independent audit of the sharp inverse and a completed historical comparison.** These are prerequisites for the broadest claims of the programme.

---

## 14. Final assessment

Revision 164 deserves substantial credit. The authors have responded to the previous reports with mathematics rather than with rhetoric. The fixed-target comparison is now stated in the right category. The first nonreduced contact fibre is computed completely, including its embedded associated prime and nilpotent structure. The moving-support collision calculation is exact, and the distinction between the flat horizontal closure and the nonflat full pullback is particularly clear. The ordered quotient explains the multiplicity-two component, and the vertical `P^4` gives a concrete geometric reason that the complete fibre is larger than the set of limits reached by colliding two reduced incidences. The globalization of the nilradical to `O_{P^2}(-1)` is a satisfying refinement.

I therefore reject any description of v164 as cosmetic, merely computational, or only repository engineering.

I nevertheless recommend rejection for *Annals*, *Acta*, *Inventiones*, or *JAMS*. The complete classification stops at the first nonreduced contact. The collision theorem treats one symmetric discriminant path, while independent products do not constitute interacting collision theory. Higher contact, higher corank, singular pencils, universal flattening, and genuine stability wall crossing remain open. The failure-algebra application still passes through complete reconstruction. Much of the surrounding machinery is classical, the closest historical comparison remains incomplete, no major external application is obtained, and the foundational sharp inverse still lacks an independent audit.

The appropriate assessment is therefore:

**Reject the v164 package in its present form for a top-four general mathematics journal.**

**Paper II is a credible candidate for a strong specialist venue in algebraic geometry, Hilbert-scheme geometry, moduli, or invariant theory after narrowing its claim surface, renaming the collision result accurately, and making the fixed-target comparison maximally transparent. Paper I likewise deserves specialist consideration after an independent proof audit and sharper historical positioning.**
