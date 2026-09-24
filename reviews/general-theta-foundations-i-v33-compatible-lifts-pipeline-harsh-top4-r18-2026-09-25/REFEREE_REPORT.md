# Referee Report — General Theta Foundations I, Revision 33

**Manuscript:** *General Theta Foundations I: Compatible Polyhedral Lifts and Quantitative Causal Width*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v33-referee-ready-2026-09-25`  
**Reviewed head:** `aab96108125317342e51e6a946efc4d778429338`  
**Native mathematical source recorded by the manuscript:** `243e670a5be8628b9f4eaf60338348032357bcab`  
**Controlling previous report:** `eaa2661530ed473f8b79407eba7a1182c8e0a450`  
**Previous reviewed manuscript:** `d38fca741135d147dfdbd99cfd9a1a716a88a5`  
**Review branch:** `review/general-theta-foundations-i-v33-compatible-lifts-pipeline-harsh-top4-r18-2026-09-25`  
**Date:** 25 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

Revision 33 is a substantial and intelligent response to the seventeenth report. It restores the missing positive-realization and extension-complexity precedents, formulates the hidden-state problem as a sequence of compatible stochastic lifts, improves the all-hidden-state profile inequality, improves the exact upper construction from square-root to cube-root width, proves a matching cube-root order in a clearly defined vector-state subclass, replaces formal rational-angle effectiveness by an explicit rate, and proves a linear theorem for a stronger anytime autonomous specification.

I did not find a short fatal error in the principal new arguments. In the exact finite-horizon, wordwise, clocked, atomic stochastic-row model actually stated, the normalization of bounded extensions, the stochastic-extension feasibility criterion, the reachable-section interpretation, the mean-support budget, the continued-fraction lower bound, the resonant polygon construction, the rational denominator estimate, and the Cayley--Hamilton anytime lower bound appear internally coherent.

The negative recommendation is therefore not an allegation that the displayed theorems are false. It is an editorial judgment about what has and has not been proved.

The decisive issue is now very sharp: the manuscript solves the **vector-state** problem at bounded-type angles, but it does not solve the **hidden compatible-lift** problem that motivated the revision. For the unrestricted width it still proves only

```text
Omega_alpha(log N) <= W_N(alpha) <= O_alpha(N^(1/3)).
```

The exponential gap between the two sides is precisely where genuinely lifted hidden states could matter. The paper gives a definition and a fixed-instance linear-programming test for compatibility, but no nontrivial construction exploiting a small hidden lift and no lower bound that defeats the logarithmic face-count conversion. The central object has been identified; its complexity has not been determined.

Several additional problems prevent a four-journal recommendation.

1. The fixed-lift criterion `ET=B` with a row-stochastic post-processing matrix is a finite Blackwell garbling problem. Its support-function dual is a form of the Blackwell--Sherman--Stein comparison criterion, and the uniform total-variation optimization in the `1/4` example is a finite deficiency calculation. The manuscript calls the criterion elementary convex separation but omits this direct statistical-experiment lineage, despite the repository's repeated use of experiment comparison and deficiency terminology.
2. The closest extension-complexity comparison is not merely static logarithmic formulations of regular polygons. It is the literature on **symmetric and equivariant lifts**. That literature shows that requiring a lift to respect dynamics or symmetry can radically change its size. In particular, regular polygons have logarithmic nonsymmetric LP lifts, whereas equivariant LP lifts can require linear size; equivariant PSD lifts exhibit a different logarithmic behavior. Revision 33 does not compare its stochastic compatibility with these established notions.
3. The exact `1/4` extension defect is a useful warning example, but it is a four-point product section unrelated to the rotation family. It proves only that positivity on a section does not automatically extend to a stochastic map. It gives no lower bound on the compatible extension complexity of the polygons used in the main theorem.
4. The anytime autonomous theorem changes the task. One fixed decoder must answer correctly at every stopping length from zero through `N`. This is a stronger specification than the original fixed-length problem with no external clock. The linear lower bound is correct for the stronger task, but it is not a theorem about the autonomous complexity of the original single-length experiment.
5. The rational-angle lower bound is explicit but extremely weak: the unrestricted conclusion is doubly logarithmic. It does not identify the arithmetic order of the rational rotation family.
6. The resource model remains permissive: horizon-specific machines, an external epoch for `W_N` and `V_N`, exact atomic sampling of computable-real rows, uncharged tables and arithmetic, and one terminal query. This is a legitimate positive-realization model, not ordinary streaming-space complexity.
7. The repository-wide Foundations pipeline remains open at every difficult analytic gate. Revision 33 explicitly leaves A2, B4, C2, the eleven-paper aggregate, fully adaptive collision scheduling, sharp hidden rotation width, and noisy-tag composition unresolved.

The appropriate conclusion is that Revision 33 contains serious specialist mathematics and a potentially useful research formulation. It is not close to the standard of the four leading general mathematics journals, and it should not continue to be marketed under a Foundations title as though the remaining hidden-lift gap were a secondary technicality.

---

## 1. Scope of this review

I reviewed the focused Revision 33 article and the repository records needed to evaluate both the new mathematics and its place in the project pipeline. In particular, I examined:

- `papers/GTF-I-v33-compatible-lifts/main.tex`;
- `introduction.tex`;
- `machine-model.tex`;
- `compatible-lifts.tex`;
- `mean-support.tex`;
- `resonant-synthesis.tex`;
- `rational-rate.tex`;
- `autonomous-comparison.tex`;
- `literature-and-scope.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORY_AUDIT.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `verify.py` and the executed build records;
- the complete seventeenth referee report;
- the Revision 32 source arguments reused or sharpened here;
- the repository-level Round-Seventeen proof-dependency ledger.

I also made targeted external comparisons with:

- David Blackwell, *Equivalent Comparisons of Experiments*, Ann. Math. Statist. 24 (1953), 265--272, DOI `10.1214/aoms/1177729032`;
- Erik Torgersen, *Comparison of Statistical Experiments*, Cambridge University Press, 1991;
- João Gouveia, Pablo A. Parrilo and Rekha R. Thomas, *Lifts of Convex Sets and Cone Factorizations*, Math. Oper. Res. 38 (2013), 248--264, DOI `10.1287/moor.1120.0575`;
- Volker Kaibel, Kanstantsin Pashkovich and Dirk Oliver Theis, *Symmetry Matters for Sizes of Extended Formulations*, SIAM J. Discrete Math. 26 (2012), 1361--1382, DOI `10.1137/110839813`;
- Hamza Fawzi, James Saunderson and Pablo A. Parrilo, *Equivariant Semidefinite Lifts of Regular Polygons*, Math. Oper. Res. 42 (2017), 472--494, DOI `10.1287/moor.2016.0813`.

This was a targeted audit, not an assertion of exhaustive priority clearance.

The publication genealogy is clean. Revision 33 descends from the controlling r17 report, retains Revision 32 unchanged as supporting material, and adds a branch-specific package rather than overwriting prior manuscripts. That is good provenance practice. It is not evidence for correctness, originality, or journal significance.

The 14-page article is self-contained enough to evaluate its new claims. The 421-page mathematical archive and 974-page development archive are therefore optional historical records, not proof supplements that increase the mathematical weight of the submission. I did not treat hashes, regression counts, negative controls, page comparisons, or successful compilation as substitutes for proof.

---

## 2. What Revision 33 genuinely improves

### 2.1 The previous literature defects are partly repaired

The article now credits the fixed-McMillan-degree/unbounded-positive-order family of Benvenuti--Farina and the positive-Hankel factorization/intertwining distinction. It also places the projected reachable section inside the language of polyhedral lifts and explicitly cites Yannakakis, Fiorini--Rothvoß--Tiwary, and Vandaele--Gillis--Glineur.

This is not cosmetic. The paper no longer suggests that rank three versus unbounded positive order, or factorization without compatible dynamics, is an entirely new conceptual phenomenon.

### 2.2 The hidden-state problem is formulated more accurately

A hidden realization produces a section

```text
Q_t = aff{reachable state distributions} intersect Delta_(K_t)
```

and an observable projection `pi_t`. The command rows restrict to affine maps between these sections and must extend to stochastic maps on the ambient simplices. The final decoder must likewise extend from the section to the whole simplex.

Theorem `thm:lift-equivalence` correctly records that these data are operationally equivalent to the original hidden-state machine. This makes explicit what static extension complexity omits.

### 2.3 The quantitative potential is materially better

Replacing area by integrated support, or perimeter divided by `2*pi`, removes the squaring loss in the old Hausdorff-to-area argument. The manuscript obtains a one-step defect of order `1/(M^2 q)` for a convergent denominator `q`, and hence order `M^(-3)` for bounded-type angles.

At the golden angle this improves the all-hidden-state profile inequality from

```text
sum 2^(-6 K_t) <= 24,000,000
```

to

```text
sum 2^(-3 K_t) <= 320.
```

This is a real advance, not a change of constants alone.

### 2.4 The exact upper construction is sharpened

The regular polygon is chosen resonantly, with order equal to a continued-fraction denominator. The residual angle is of order `q^(-2)`, and the required logarithmic radial expansion is of order `q^(-3)`. Choosing `q` of order `N^(1/3)` yields an exact machine.

The transition rows are written explicitly. The active row uses two adjacent vertices; the idle row mixes the old vertex with the zero barycenter. The construction realizes the exact conditional mean rather than approximating the irrational rotation.

### 2.5 The vector-state subclass is solved at the correct order

Within the statewise-intertwining model, the observable polygon has at most `K_t` vertices rather than at most `2^(K_t)`. The same mean-support budget therefore yields a cube-root lower bound, matching the resonant upper construction.

The paper is careful to state

```text
V_N(alpha) = Theta_alpha(N^(1/3))
```

only for bounded-type angles and only in the vector-state class. This honesty is essential.

### 2.6 The rational and autonomous comparisons are more explicit

For `(3+4i)/5`, the Gaussian-integer norm gives an explicit denominator estimate and hence an explicit, though weak, hidden-state lower rate. The previous reliance on an abstract real-algebraic optimization is no longer the only quantitative statement.

The anytime autonomous section also clearly states its stronger specification. The Cayley--Hamilton argument gives a clean linear lower bound once one fixed decoder must work at all stopping lengths.

These are all worthwhile improvements. They do not close the principal hidden-lift problem.

---

## 3. Technical audit of the new arguments

### 3.1 Machine definitions and the separate minimum

The definitions of `W_N`, `V_N`, and `A_N` are now separated properly.

- `W_N` counts available labels in an unrestricted, cut-dependent clocked realization.
- `V_N` imposes a predictive vector on every available state and a statewise intertwining identity.
- `A_N` uses one state set, fixed command matrices, and one decoder correct at every allowed stopping length.

The separate minimum remains three. Residual rows are affine in a two-dimensional predictive vector, and the idle prefixes span that affine plane. The fixed triangle contains all reachable predictive vectors and gives three legal continuation generators. Embedding a selected-cut factorization by allowing large registers elsewhere is legitimate.

I see no residual-state restriction hidden in this argument.

### 3.2 Normalization of bounded extensions

Proposition `prop:slack` is correct in the stated bounded, finite-facet setting. For an irredundant facet description, boundedness makes the facet normals positively span the dual space. Strictly positive balancing coefficients normalize the slacks to sum to one. The resulting map is injective, and nonnegativity of the normalized coordinates recovers the original polytope.

The proposition does not cover unbounded extensions, and the article does not claim otherwise.

### 3.3 The stochastic-extension criterion

For fixed spanning rows `E` and prescribed images `B`, the set

```text
{ E T : T is row-stochastic }
```

is compact and convex. Its support function at `Z` is

```text
sum_i max_j (E^T Z)_(i,j),
```

because each row of `T` is optimized independently over a simplex. Separation therefore gives the stated necessary and sufficient inequalities.

This proof is correct. Its originality is another matter: it is the finite garbling problem for statistical experiments. The existence of `T` is Blackwell sufficiency, and the right side is the value of a finite decision problem. The manuscript should not present this only as an unnamed support-function dual.

### 3.4 The `1/4` extension defect

The calculation is correct. At the four vertices of the section, the first output target is one or zero according to the first block. For a fixed second-block coordinate, the two realized probabilities can differ by at most one half. Their two errors therefore sum to at least one half, so one is at least one quarter. The displayed stochastic row attains one quarter.

However, the quantity

```text
min_T max_h TV((E T)_h, B_h)
```

is a finite one-sided deficiency. The example is best understood in that established language. It does not establish a new general theory of extension defects, nor does it say anything quantitative about the regular-polygon lift used later.

### 3.5 Operational equivalence of compatible lifts and machines

A machine supplies the sections, observable maps, stochastic extensions, and decoder. Conversely, ambient stochastic extensions preserve membership in the sections and propagate the required observable means. The equivalence is correct.

Substantively, this theorem is a faithful normal form. It does not compress the global search problem. The unknown sections, projections, and stochastic maps are nearly the same data as the desired realization, and the theorem gives no tractable optimization over them.

### 3.6 Mean-support accumulation

The identity between mean support and perimeter in the plane is used correctly. The one-step potential

```text
D_alpha(P) = m(conv(P union R_alpha P)) - m(P)
```

is nonnegative, rotation invariant, and telescopes along a compatible polygon chain.

The orbit accumulation lemma is valid: pointwise, a maximum over the first `q` rotated support functions is bounded by the sum of positive consecutive increments. Integrating identifies every increment with the same one-step defect.

### 3.7 The inscribed-polygon estimate

Radially pushing vertices to the circle of maximal radius produces a containing polygon because the origin lies in the original polygon. The angular gaps are at most `pi`, and concavity of sine yields the regular-polygon perimeter upper bound. This gives the required deficit from the circle.

I do not see a missing origin-containment assumption: it follows from the inner disk hypothesis.

### 3.8 The continued-fraction one-step gain

A convergent with `|alpha-p/q|<q^(-2)` gives a `3*pi/q` orbit net. The orbit hull therefore has mean support at least `r cos(3*pi/q)`. Subtracting the maximal mean support of an `M`-vertex polygon and using `q>=8M` gives the displayed coefficient.

The numerical chain leading to `301/384 > 3/4` is crude but consistent. Dividing the accumulated orbit gain by fewer than `q` steps yields

```text
D_alpha(P) >= 3a/(4 M^2 q).
```

### 3.9 Hidden and vector-state profile laws

For a hidden `K_t`-state realization, the reachable simplex section can project to at most `2^(K_t)` vertices. Inserting `M=2^(K_t)` into the mean-support gain yields the logarithmic lower bound.

For vector-state realizations, the state vectors themselves give a polygon with at most `K_t` vertices. Inserting `M=K_t` yields the cube-root lower bound.

This distinction is mathematically legitimate. It is also the central limitation of the paper: the proof has no way to prevent a small simplex section from projecting to a polygon with exponentially many vertices.

### 3.10 Resonant exact synthesis

The residual rotation angle satisfies `|delta|<2*pi/q^2`. The chosen radial factor

```text
lambda = cos(pi/q - |delta|)/cos(pi/q)
```

places the rotated vertex on an edge of the next polygon. The two adjacent-vertex weights are nonnegative and sum to one. The idle row uses the zero barycenter and compensates for radial expansion.

The estimate

```text
log lambda <= 40/q^3
```

follows from integrating tangent. With `q^3>=40N`, the terminal radius remains below one, while the initial inradius contains the seed square. This gives an exact vector-state realization with `q` labels.

The command matrices can indeed be epoch independent for the chosen horizon. The decoder remains horizon dependent.

### 3.11 Rational-angle estimate

The Gaussian integer `(3+4i)^r-5^r` is nonzero and therefore has modulus at least one. This yields

```text
||r alpha|| >= 5^(-r)/(2*pi).
```

Combining this with consecutive convergent denominators gives the stated exponential upper bound on `Q_alpha(M)`. Substitution into the profile theorem yields the doubly logarithmic hidden lower bound and logarithmic vector-state lower bound.

The argument is correct but quantitatively very weak. It is not an asymptotic classification of the rational rotation.

### 3.12 Anytime autonomous theorem

If a `K`-state stochastic matrix with one fixed decoder reproduces `zeta^j` for `j=0,...,K`, Cayley--Hamilton forces `zeta` to be an eigenvalue. A unit-modulus eigenvalue of a finite stochastic matrix is a root of unity, contradicting infinite rotation order.

Thus the lower bound `K>=N+1` is correct for the anytime specification. The counter construction gives the linear upper bound.

The theorem must remain quarantined from claims about the original fixed-length autonomous task. The proof uses correctness at every intermediate length in an essential way.

---

## 4. The hidden compatible-lift problem remains unsolved

The article's most important conceptual contribution is the distinction

```text
static extension  !=  compatible stochastic lift.
```

But after making that distinction, the paper does not determine the complexity of the latter.

For bounded-type angles it proves

```text
(1/3) log_2 N - O_alpha(1) <= W_N(alpha) <= O_alpha(N^(1/3)).
```

This is not a small quantitative gap. It is the difference between genuinely hidden logarithmic memory and direct geometric cube-root memory.

The exact vector-state theorem does not settle the issue because vector states remove the lift advantage by definition. The entire point of an extension is that a `K`-coordinate simplex section may have exponentially many projected vertices. Proving optimality only after replacing `2^K` by `K` solves the unlifted problem.

A top-four paper centered on compatible lifts would need a decisive theorem on this gap. Examples of adequate advances would include:

1. a superlogarithmic lower bound for unrestricted hidden lifts;
2. a sub-cube-root hidden construction using a nontrivial extension;
3. an exact order in a broad symmetry-restricted but genuinely lifted class;
4. a dynamic slack-factorization invariant equivalent to hidden compatible width and amenable to lower bounds;
5. a structural theorem proving that hidden lifts cannot beat vector states for this rotation family;
6. a counterexample showing an exponential advantage of compatible hidden lifts over vector-state chains.

Revision 33 provides none of these. It formulates the research question and solves a restricted class.

---

## 5. The Blackwell and deficiency lineage is missing

Theorem `thm:extension-dual` is not merely an LP feasibility observation in isolation.

Interpret the rows of `E` and `B` as two finite experiments on the same parameter set. Then

```text
B = E T
```

with `T` row stochastic says that `B` is obtained by garbling the signal of `E`. Blackwell's comparison theorem identifies this with domination in every finite decision problem. The manuscript's support-function expression is precisely the optimization of such a decision problem over output actions.

Similarly, the minimum over stochastic `T` of the worst row total-variation error is a finite deficiency quantity. The exact value `1/4` is therefore a small explicit deficiency computation.

This matters for three reasons.

1. It changes the novelty boundary of the fixed-lift criterion.
2. It provides established language for approximate compatibility, which the manuscript currently does not develop.
3. It connects directly to the repository's earlier claims about filtered experiments, deficiency, and comparison, rather than treating the new LP as an isolated construction.

At minimum the paper should cite Blackwell's 1953 theorem and Torgersen's monograph, state the precise finite-experiment translation, and distinguish its new multi-epoch coupling problem from the classical one-step garbling criterion.

A more substantial paper could define a sequential or diagrammatic deficiency for a proposed lift chain and prove composition or stability theorems. Revision 33 does not do so.

---

## 6. Equivariant and symmetric lifts are the closest omitted extension literature

Revision 33 now discusses static small extensions of regular polygons, but it stops one step too early.

The central issue is whether a geometric action can be lifted to an action on the extension. This is exactly the motivation of symmetric and equivariant extended formulations.

Established results show that symmetry requirements can radically alter extension size. In particular:

- nonsymmetric LP lifts of regular `N`-gons can have logarithmic size;
- for prime-power orders, equivariant LP lifts can require linear size;
- equivariant PSD lifts of regular polygons have a different logarithmic theory.

The stochastic maps in Revision 33 are not identical to classical equivariance. They may vary with time, need not be invertible, and act between different sections. Therefore these results do not settle `W_N`.

That is precisely why they must be discussed. They show that the distinction between static and dynamically compatible lifts is part of a well-developed symmetry-lift phenomenon, and they suggest natural intermediate problems:

- one fixed section with a stochastic lift of a cyclic action;
- one section per radius with a common lifted command;
- permutation-equivariant simplex extensions;
- semigroup-equivariant rather than group-equivariant lifts;
- approximate equivariance measured by deficiency.

Without this comparison, the article overstates how novel it is to ask whether a small polygon lift supports the rotation.

The omission is especially conspicuous because Gouveia--Parrilo--Thomas already characterize symmetric cone lifts, and Fawzi--Saunderson--Parrilo use regular polygons as the basic test family for equivariant lifts.

---

## 7. The `1/4` example is too remote from the main obstruction

Proposition `prop:extension-gap` establishes only the logical statement that an affine map positive on a section need not extend stochastically to the whole simplex.

It does not show any of the following:

- that a logarithmic extension of a regular polygon fails the rotation test;
- that the defect accumulates through time;
- that every small extension has a nonzero command defect;
- that decoder extension creates an additional obstruction;
- that a hidden lift cannot improve the cube-root construction;
- that the relevant defect is robust under changing the section.

For the paper's main narrative, a meaningful next theorem would attach a quantitative stochastic-extension defect to an actual polygon extension or a family of cyclic lifts. The current four-vertex example is pedagogical, not foundational.

---

## 8. The quantitative conclusions remain limited

### 8.1 The unrestricted width has no identified order

The logarithmic lower and cube-root upper bounds leave the main complexity question open.

### 8.2 The vector-state theorem is planar and arithmetic-specific

The exact order uses a planar perimeter inequality, a one-dimensional continued-fraction net, and regular polygons. The paper mentions possible higher-dimensional analogues but proves none.

### 8.3 The rational angle is far from classified

The explicit lower bound is doubly logarithmic for hidden width, while the available rational upper bound is linear. No meaningful asymptotic scale is identified.

### 8.4 The constants remain proof constants, not a finite phase diagram

The improved golden-angle lower bound exceeds the trivial value three after `N>163,840`. This is vastly better than Revision 32, but it still does not determine a single nontrivial exact value of `W_N` for a general horizon.

### 8.5 No algorithm searches for optimal compatible lifts

The fixed-lift LP is finite once the sections and affine maps are supplied. The difficult problem is finding those objects. The manuscript gives neither a complexity classification nor a convergent optimization hierarchy for that search.

---

## 9. The autonomous comparison changes the question

The section title “Removing the clock” risks overstating the result.

The original clocked experiment asks for correctness after one fixed horizon `N`. A clock-free fixed-length machine could still exploit a horizon-specific decoder and need not answer earlier queries correctly.

The anytime model instead requires one fixed decoder to answer after every length `0,...,N`. The Cayley--Hamilton lower bound uses exactly those `K+1` consecutive output identities. It does not apply if only the length-`N` identity is required.

The theorem is valid and interesting, but the correct interpretation is:

> strengthening the query-time specification from one fixed length to all stopping lengths raises the state count to linear order.

It is not:

> removing the external clock from the original problem forces linear order.

A specialist version should rename the section and state the unresolved fixed-length autonomous problem explicitly.

---

## 10. Resource-model assessment

The primary width theorem grants the machine:

- an externally supplied epoch;
- cut-dependent state alphabets and transition rows;
- a horizon-specific decoder;
- exact sampling from arbitrary computable-real rows as one atomic operation;
- an uncharged read-only table of all rows;
- uncharged arithmetic and construction time;
- one terminal coordinate query;
- no obligation to answer multiple queries from one installation.

This is a coherent finite positive-realization model. It is not a standard bit-space or streaming-algorithm model.

The rational counter can be compiled into fair bits with separately charged workspace, but that does not extend to the irrational resonant rows. The article is now honest about this distinction. The title and significance claims should remain equally disciplined.

---

## 11. Pipeline assessment

The manuscript's own `PIPELINE_STATUS.json` records:

```text
historical_A2_replaced              false
B4_aggregate_closed                 false
C2_aggregate_closed                 false
eleven_paper_aggregate_closed       false
fully_adaptive_collision_solved     false
sharp_hidden_rotation_width_solved  false
noisy_tag_composition_solved        false
```

The Round-Seventeen proof ledger still contains independent Fourier/LLT, stopped-large-deviation, common-kernel, nonlinear-semigroup, graph-core, filtering, optional-projection, and typed-contraction gates.

Revision 33 supplies local proof edges involving:

- reachable simplex sections;
- stochastic lift compatibility;
- mean-support orbit budgets;
- continued-fraction resonance;
- Gaussian-integer denominators;
- an anytime Cayley--Hamilton argument.

None closes an indispensable gate in the A2/A3/A4/C2/D1 or B2/B1/B3/B4/C1/C2/D1 chains.

Thus the repository pipeline contributes provenance, not additional mathematical leverage for this submission. The “General Theta Foundations I” branding remains disproportionate to the actual theorem.

---

## 12. Minimum changes for a credible specialist submission

These are not a route to acceptance in a top-four journal. They are the minimum changes needed for an accurate specialist evaluation.

### 12.1 Retitle and reposition

Remove “General Theta Foundations I.” A defensible title would identify dynamic polyhedral lifts, compatible positive realizations, or finite-horizon stochastic realization width.

### 12.2 Add the statistical-experiment comparison

Explain explicitly that stochastic extension of fixed finite sections is Blackwell garbling. State how the dual inequality relates to decision problems and how the `1/4` quantity relates to deficiency. Cite Blackwell and Torgersen.

### 12.3 Add equivariant-lift literature

Compare compatible stochastic lifts with symmetric/equivariant LP and cone lifts, especially the regular-polygon results of Gouveia--Parrilo--Thomas and Fawzi--Saunderson--Parrilo. State carefully why those results neither prove nor refute the time-varying stochastic-lift bounds.

### 12.4 Center the unresolved hidden-lift gap

Do not allow the exact vector-state theorem to dominate the abstract or conclusion. The primary unrestricted problem remains open.

### 12.5 Produce a main-family extension obstruction

Replace or supplement the four-vertex `1/4` example with a quantitative theorem for an actual regular-polygon extension, a cyclic action, or a semigroup-compatible lift.

### 12.6 Separate fixed-length autonomy from anytime autonomy

State a separate definition and status for a clock-free device required to answer only at length `N`. Do not use the anytime theorem as evidence for that unresolved task.

### 12.7 Develop approximate compatibility

The Blackwell/deficiency interpretation makes an approximate theory natural. A robust dynamic deficiency or error-composition theorem would be more consequential than the current isolated exact defect.

### 12.8 Reduce repository-specific material

The journal article should not require internal A2/B4/C2 labels, cumulative archive history, or seventeen prior review rounds to explain its contribution.

---

## 13. Specific major and minor comments

1. **Theorem `thm:extension-dual` needs Blackwell attribution.** The stochastic post-processing problem is classical comparison of experiments.
2. **The `1/4` quantity should be called a one-sided finite deficiency or explicitly distinguished from it.**
3. **Add Torgersen or an equivalent standard reference.** The repository already invokes experiment comparison elsewhere.
4. **Add symmetric/equivariant lift references.** Static FRT/VGG citations are insufficient for a dynamics-respecting question.
5. **Explain the relation to equivariant LP lifts.** A stochastic permutation action is a special case of the paper's ambient stochastic extension.
6. **Do not infer the converse.** Time-varying noninvertible stochastic maps are more general than classical group equivariance.
7. **The compatible-lift equivalence is a normal form, not a complexity theorem.** Say this in the abstract or introduction.
8. **The vector-state model is not merely a convenient representation.** It removes the extension advantage and is a genuine restriction.
9. **Keep `W_N` and `V_N` visually separated in every theorem summary.**
10. **The abstract should lead with the unresolved general gap.** At present the exact vector-state result can dominate a quick reading.
11. **Qualify “sharp” in the root entry.** The `1/4` defect is sharp for one toy instance, not a sharp dynamic-lift theorem.
12. **The mean-support inequality deserves independent presentation.** It is the strongest genuinely new quantitative tool in the revision.
13. **State the dependence on bounded type before the cube-root order in every summary.**
14. **The rational rotation angle is not shown to be bounded type.** The manuscript correctly avoids this; preserve that boundary.
15. **The rational hidden lower is doubly logarithmic.** Do not describe it generically as a quantitative classification.
16. **Rename “Removing the clock.”** The theorem adds an anytime query obligation.
17. **Define the unresolved fixed-length autonomous quantity.** Even a short remark would prevent conflation.
18. **Clarify output-state counting in `A_N`.** The lower bound includes all declared states, while the upper adds two absorbing answer states.
19. **The contractive comparison is an application of invariant-polytope theory.** It should remain a corollary, not novelty evidence.
20. **Do not market exact computable-real rows as an implementation result.** The current resource ledger is appropriately cautious.
21. **The fixed-lift LP does not search over sections.** Avoid algorithmic language that obscures this.
22. **The face-count bound is very coarse.** Its use is valid, but it is exactly why the hidden lower remains logarithmic.
23. **A dynamic slack operator would be more informative than the present data-level equivalence.** This is the natural theoretical next step.
24. **The literature audit should record the Blackwell and equivariant-lift comparisons.** Their absence is now the principal priority defect.
25. **The positive-realization bibliography is improved.** Keep the precise stationary versus time-varying quantifier distinction.
26. **Do not use internal revision manuscripts as external validation.** They are provenance only.
27. **The archive sizes should remain outside the referee package.** The compact package is the correct submission unit.
28. **Finite regression scripts do not test the universal lift optimization.** The manuscript says this; retain the disclaimer.
29. **The contribution table should classify the fixed-lift dual as classical/derived, not as a central new theorem.**
30. **Seek a specialist venue after major repositioning.** Positive systems, stochastic realization, information comparison, or polyhedral optimization are plausible homes.

---

## 14. Scorecard

| Criterion | Assessment |
|---|---|
| Correctness in the stated model | Principal proofs appear coherent; no short fatal counterexample found |
| Advance over Revision 32 | Substantial: better potential, cube-root construction, exact vector-state order, explicit rational rate |
| Unrestricted main problem | Open: logarithmic lower versus cube-root upper |
| Originality boundary | Incomplete: Blackwell/deficiency and equivariant-lift literatures omitted |
| Mathematical depth | Strong specialist level, below top-four general-journal level |
| Generality | One planar rotation experiment; bounded-type exact order only in a restricted class |
| Quantitative strength | Exact for vector states; weak and nonmatching for hidden states; doubly logarithmic rational hidden bound |
| Algorithmic content | Fixed-lift LP only; no global lift search or complexity theorem |
| Autonomous comparison | Correct for a stronger anytime task, not the original fixed-length task |
| Resource model | External clock, atomic real rows, free tables/arithmetic, one terminal query |
| Pipeline impact | None on the decisive A2/B4/C2/D1 analytic gates |
| Presentation | Focused and much improved; program branding remains misleading |
| Reproducibility engineering | Strong, but not evidence of proof, novelty, or journal level |
| Editorial recommendation | Reject at top-four level; consider only after specialist repositioning |

---

## 15. Final assessment

Revision 33 is the strongest manuscript in this sequence. It takes the previous report's extension-complexity objection seriously, improves both sides of the quantitative theorem, and isolates a mathematically natural hidden-lift question. The mean-support profile budget and resonant exact synthesis are genuine advances. The vector-state cube-root theorem appears correct and nontrivial.

But the paper's most important problem remains unsolved. The unrestricted hidden width lies between logarithmic and cube-root growth. The compatible-lift equivalence tells us what a solution is made of; it does not determine the minimum size. The fixed-lift dual is classical garbling theory in finite-dimensional form. The extension defect is a toy example. The closest symmetry-respecting lift literature is not discussed. The anytime linear theorem answers a strengthened query specification rather than the original clock-removal problem.

The repository has therefore reached a useful research question, not a four-journal conclusion.

The program title and almost one thousand pages of preserved development cannot change that mathematical fact. Nor do repeated internal review cycles substitute for an external originality audit in positive realization, comparison of experiments, and extended formulations.

My recommendation is firm:

**Reject for Annals of Mathematics, Inventiones Mathematicae, Journal of the AMS, or Acta Mathematica.**

A retitled and literature-complete paper centered on finite-horizon compatible stochastic lifts, with the vector-state theorem as a solved benchmark and the unrestricted hidden gap stated honestly as open, could merit serious specialist review. A materially stronger submission would need either a nontrivial hidden lift or a lower-bound mechanism that goes beyond projected face counting.