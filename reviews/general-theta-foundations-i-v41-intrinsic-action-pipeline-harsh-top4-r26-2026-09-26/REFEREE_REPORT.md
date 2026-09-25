# Referee Report — General Theta Foundations I, Revision 41

**Manuscript:** *General Theta Foundations I: Intrinsic Action Gaps and Numerical Memory*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v41-referee-ready-2026-09-26`  
**Reviewed head:** `08773b2705c5ac92716df5daf42a54f3b61bca34`  
**Native mathematical source recorded by the manuscript:** `282bc34bbbeaa56a2ec36c6daf438e545dcfeb37`  
**Controlling previous report:** `9707844addcd9eb478eb863514f288923f9d40fd`  
**Previous reviewed manuscript:** `28890c62dd69f217bf2f1c205ff9542eb537c2ef`  
**Review branch:** `review/general-theta-foundations-i-v41-intrinsic-action-pipeline-harsh-top4-r26-2026-09-26`  
**Date:** 26 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

Revision 41 is a substantive and technically serious response to the twenty-fifth report. It repairs the most concrete nonintrinsic defects of Revision 39. The lower-bound hypothesis is now stated on the actual command action rather than on an arbitrarily enlarged presenting group; seed activation is defined canonically on an isotypic component rather than through a chosen decomposition into equivalent copies; the original finite seed set need not span the ambient representation; and the matched exponent needs expansion only on one active type attaining the largest minimum-orbit dimension. The manuscript also supplies a faithful `SO(3) x SO(2)` experiment for which the full effective group has no regular spectral gap but the dominant `SO(3)` constituent still yields linear width. Finally, it evaluates the minimum-orbit invariant on all compact simple adjoint representations and on several classical infinite families.

I did **not** find a short fatal counterexample to the principal mathematical chain. In the exact model that the paper defines—finite horizon, wordwise specification, nonuniform clock, arbitrary real atomic stochastic rows, one terminal coordinate query—the following arguments appear coherent:

- invariance of the action gap under redundant presentations;
- equality of the sphere and Lebesgue action gaps;
- the constituent-level entropy occupation bound;
- the canonical isotypic activation formula;
- the terminal-correlation calibration using the actual query norm;
- the paid-branch exact upper realization;
- the faithful mixed expanding/nonexpanding example;
- the root-deletion computation for compact adjoint actions;
- and the skew-congruence stabilizer calculation for `wedge^2 C^n`.

The negative recommendation is therefore not an allegation that the headline theorem is false. It is an assessment of scope, originality, conditionality, effectiveness and relation to the advertised program.

The four-journal case fails for the following decisive reasons.

1. **The headline theorem remains a conditional expansion theorem, not a classification of numerical memory.** A positive action gap on a dominant type is a strong sufficient condition. It is neither shown necessary nor characterized for general finite command alphabets. The entire dominant-nongapped regime remains open, even though the repository's earlier circle and rotation examples show that substantial memory growth can occur without a spectral gap.
2. **The new “intrinsic” gap is still an infinite-dimensional and generally non-effective certificate.** It is the norm of a Koopman operator after removing invariant functions, equivalently a supremum over all harmonic degrees. The paper explicitly concedes that no finite harmonic truncation certifies it. For general rational or algebraic command matrices there is no decision procedure, quantitative lower bound, or finite certificate supplied by the article.
3. **The proof-side command law is not itself part of the numerical experiment.** The response problem specifies an alphabet and matrices, while `g_E` depends on a selected probability `p`. Existence of a useful law is a property of the alphabet, but the displayed gap and every lower-bound constant vary with an analyst-chosen certificate. A genuinely canonical formulation would optimize over `p`, or would state the theorem explicitly as conditional on a supplied test law rather than calling the quantity intrinsic without qualification.
4. **The error calibration that enters the headline remains only partly computed.** The Euclidean activation `a_lambda` has a clean commutant spectral formula. The actual threshold, however, uses `c_lambda`, an optimization involving the physical query `l^1` norm over all isometric intertwiners. No eigenvalue formula, structural optimizer, efficient computation, or useful general closed bound beyond `a_lambda/sqrt(D) <= c_lambda <= a_lambda` is given.
5. **The representation-theoretic section evaluates selected classical families but does not provide a general orbit classification.** The adjoint table is an elementary classical centralizer computation. The defining and low-rank spin examples are standard transitive actions. The exterior-square calculation is useful, but it is one fundamental family. The paper still has no highest-weight formula, systematic treatment of minimizing stabilizers for irreducible modules, or meaningful classification of `s(U)` beyond the stated examples.
6. **Most of the difficult dynamic converse is inherited.** The genuinely nontrivial entropy occupation theorem, uniform hidden-state treatment and minimum-orbit compiler were already established in the predecessor chain. Revision 41 contributes a better hypothesis, a canonical calibration, a direct-sum refinement and classical orbit calculations. This is a good consolidation and extension; it is not a second general-journal-scale breakthrough.
7. **The resource model remains highly permissive and nonuniform.** The horizon, epoch, machine redesign, complete transition tables, their construction and lookup, real arithmetic and exact sampling from arbitrary real rows are uncharged. The result is a positive-realization label-width theorem, not a uniform-space theorem, total branching-program lower bound, autonomous-memory theorem or finite-random-bit complexity result.
8. **The theorem treats only connected effective matrix groups, fixed representation dimension, fixed positive signal and fixed error below a sufficient calibration threshold, with one selected terminal query.** Disconnected compact actions, finite groups, simultaneous query laws, vanishing signals, uniform-in-dimension regimes and adaptive experimental design are outside the theorem.
9. **The bibliographic boundary around minimum orbit geometry is still too thin for a classification claim.** The paper cites a root-system text, orbitopes and one quantization paper, but does not engage theorem-by-theorem with the mature transformation-group literature on orbit-type strata, slice geometry, polar and taut representations, cohomogeneity, and metric quotients of compact representations. No prior containment is asserted here; the point is that the novelty boundary is not yet independently established.
10. **The repository-wide Foundations pipeline remains unchanged at every hard analytic gate.** Revision 41 does not prove the branchwise Fourier/local-limit theorem, stopped large deviations, global renewal kernel, nonlinear Nisio semigroup, graph core, filtering, optional projection or typed contraction required by the controlling A/B/C/D dependency chains.

Revision 41 is a strong specialist-paper candidate. It is not close to the standard of the four leading general mathematics journals, and the prefix “General Theta Foundations I” continues to overstate both its mathematical scope and its role in the repository's principal analytic program.

---

## 1. Scope of this review

I reviewed the focused Revision 41 article and the repository records needed to assess both the new mathematics and its relation to the full paper pipeline. In particular, I examined:

- `papers/GTF-I-v41-intrinsic-action/main.tex`;
- `introduction.tex`;
- `machine-model.tex`;
- `intrinsic-action.tex`;
- `orbit-strata.tex`;
- `orbit-entropy.tex`;
- `orbit-synthesis.tex`;
- `canonical-activation.tex`;
- `mixed-expansion.tex`;
- `representation-minima.tex`;
- `matrix-families.tex`;
- `numerical-semantics.tex`;
- `comparison.tex`;
- the retained reducible, conjugation, projective, effective-gate and arithmetic-normalization appendices;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `LITERATURE_AUDIT.md`;
- `PRIMARY_SOURCE_AUDIT.json`;
- `HISTORY_AUDIT.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `GAP_CERTIFICATE.json` and the executed build records;
- the complete independent r25 report;
- the Revision 39 arguments inherited or reformulated here;
- and the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I also made targeted comparisons with primary or author-hosted work on compact-group spectral gaps, orthogonal representation orbit spaces, compact transformation groups, orbitopes, manifold quantization, nonnegative/PSD factorization, probabilistic ordered programs and current strict-cutpoint quantum-automata simulation. This was not an exhaustive priority certification.

The publication genealogy is clean. Revision 41 descends from r25, preserves the reviewed Revision 39 article, and does not overwrite either of the existing v40 work branches. This is good repository practice. It is not evidence for correctness, originality or editorial significance.

The focused article has grown to thirty pages and is sufficiently self-contained to audit the new statements. The cumulative mathematical and development PDFs are provenance records, not additional theorem weight. Clean builds, source hashes, page comparisons and negative controls are useful delivery evidence but do not certify universal mathematics or priority.

---

## 2. What Revision 41 genuinely repairs

### 2.1 It removes the redundant presenting-group defect

Revision 39 assumed a norm gap on the full regular representation of a chosen group `G`. The same numerical experiment could be represented by `G x T` with a trivially acting compact factor, destroying that gap without changing a single command matrix or response probability.

Revision 41 correctly begins with the closure

```text
H = closure <A_a : a in A> subset O(V)
```

of the actual command matrices. On an invariant subspace `E`, it defines

```text
g_E = 1 - ||P_E - Pi_E||^2,
```

where `P_E` averages the actual commands and `Pi_E` is Haar averaging for the effective image on `E`. This is invariant under an orthogonal intertwiner, duplicate letters with unchanged total mass, and redundant compact extensions with the same pushed-forward command law.

This is the right repair. It addresses the main conceptual defect in r25 rather than merely changing notation.

### 2.2 It identifies the exact action norm used by the entropy proof

The equality between the sphere and Lebesgue action gaps is valid. Polar coordinates decompose Lebesgue `L^2(E)` into a radial factor and the sphere `L^2`, while both command averaging and Haar averaging act only on the angular factor. The entropy-production inequality therefore needs precisely the sphere action gap that the paper defines.

The harmonic decomposition formula

```text
1 - g_E = sup_l ||P_{E,l} - Pi_{E,l}||^2
```

is also correct. It clarifies that the condition concerns every harmonic degree and cannot be checked by testing a few low-dimensional blocks.

### 2.3 It removes the arbitrary-copy calibration

In an isotypic component, projecting a seed onto a displayed irreducible copy depends on a noncanonical splitting. Revision 41 replaces this by optimization over all isometric intertwiners

```text
J : E_lambda -> R_lambda.
```

This is the correct invariant object. The set of such `J` is compact, and the definitions

```text
a_lambda = max_(x,J) ||J^*x||,
B(J)      = ||J^*||_(l_infinity -> l_2),
c_lambda = max_(x,J) ||J^*x|| / B(J)
```

are independent of a chosen decomposition into copies.

The diagonal-copy example in the manuscript accurately illustrates why taking a minimum or maximum over a displayed copy decomposition would be meaningless.

### 2.4 The commutant covariance formula is valid

For

```text
C_(lambda,x) = integral_H (hP_lambda x)(hP_lambda x)^* dh,
```

Haar averaging projects the rank-one operator onto the matrix commutant. If `J` is an isometric intertwiner, the operator `J^* C J` is self-adjoint and commutes with an irreducible real representation. Its eigenspaces are invariant, so it is scalar, including complex and quaternionic commutant types. Taking traces gives

```text
a_lambda^2 = d_lambda max_x lambda_max(C_(lambda,x)).
```

Conversely a top eigenspace contains an irreducible copy of the active type. This argument is coherent.

### 2.5 It allows arbitrary finite seed sets

The article now restricts first to the invariant reachable span

```text
R_X = span(H X).
```

Nothing outside this subspace affects the prescribed responses. The upper construction decomposes only this reachable representation, and the lower bound selects an active type within it. Thus no artificial spanning assumption on the original ambient representation remains.

### 2.6 Expansion is required only on one dominant active type

Let `sigma_X` be the maximum of the minimum orbit dimensions among active nontrivial types. If one type attaining that maximum has a positive action gap, its constituent-wise conditional-centroid process yields the full lower exponent. Other active types may be nongapped.

This is a real strengthening. Requiring every active type to expand would be unnecessary for a maximum-exponent theorem.

### 2.7 The faithful mixed example is genuinely outside the full-group-gap class

The ten block-diagonal commands on `R^3 + R^2` generate `SO(3) x SO(2)`. The `SO(3)` marginal is algebraic, adapted and qualitatively expanding by the external Benoist–de Saxcé theorem. The irrational circle marginal has Fourier multipliers approaching modulus one, so the full product has no regular norm gap.

The standard three-dimensional constituent has orbit dimension two and supplies a linear lower bound. The circle constituent has orbit dimension one and an exact `O(sqrt(N))` upper realization. The paid branch union therefore has width `Theta(N)`.

This example establishes that the v41 theorem is more than quotienting out a trivial factor.

### 2.8 The previous version discrepancy is responsibly version-pinned

The repository now separates the April and August versions of arXiv:2604.07058, records dates, titles and theorem locations, and makes the numerical/cutpoint distinction independent of either external upper constant by proving an internal attenuating sign simulator.

The source record has been materially improved. I do not use the earlier version mismatch as a principal mathematical objection to Revision 41.

---

## 3. Technical audit of the machine model

### 3.1 The optimized resource is explicit

For each prescribed horizon, the machine has cut-dependent finite label sets, one stochastic transition matrix for each layer and command, and one bounded decoder column for each final coordinate query. The objective is maximum binary total variation over every seed, word and query.

Available labels, including unreachable padding, are charged. The final retained binary output contributes a two-label cut. Only the updated label survives each command.

The following are free:

- the epoch;
- the horizon;
- redesigning the entire machine for each horizon;
- complete transition and decoder tables;
- construction and lookup of those tables;
- real arithmetic;
- exact atomic sampling from arbitrary stochastic rows.

The article now states these conventions clearly. They define a legitimate positive-realization width, but not an ordinary algorithmic-space measure.

### 3.2 The converse test law is legitimate

The target specification is wordwise. A lower bound may therefore place any independent command distribution on the externally supplied words. The conditional centroids are proof-side variables and do not become runtime information.

The identity

```text
Z_(t+1) = E[U_a Z_t | S_(t+1)]
```

follows from the stochastic update rule and independence of the fresh command. Conditional expectation gives the telescoping quadratic loss. No false conditional independence of the past given the new label is assumed.

### 3.3 The query columns may be combined only in the proof

Forming a proof-side vector from the terminal coordinate columns does not ask the machine to answer all queries jointly. Every coordinate is a separate permitted final query. The `l^1` factor in `B(J)` correctly accounts for coordinatewise error when pairing with a word-dependent vector in the chosen copy.

This part of the resource accounting is sound.

---

## 4. Technical audit of the intrinsic action gap

### 4.1 Presentation invariance is proved at the correct level

The operators depend only on the finite probability measure on actual orthogonal matrices and on the effective compact image. Redundant group kernels and identical command letters do not change them. Orthogonal intertwiners give unitary conjugacies.

This resolves the exact counterexample raised in r25.

### 4.2 Sphere/Lebesgue equality is correct but does not make the gap effective

Polar decomposition transfers the norm exactly, but the resulting hypothesis is still an infinite-dimensional spectral statement. The harmonic formula is a supremum over all degrees. The article explicitly says that a finite truncation is not a certificate.

Consequently, for a newly supplied rational alphabet, the theorem generally does not tell the reader how to decide whether the assumption holds. One must import a deep spectral-gap theorem, or leave the conclusion conditional.

### 4.3 The action gap depends on an analyst-chosen probability law

The numerical experiment itself contains an alphabet and command matrices. The law `p` is introduced only for the converse. Different laws on the same alphabet can have very different norms, including zero mass on useful letters.

For the exponent theorem, it is enough that some law have a positive gap. The article should therefore define an alphabet invariant such as

```text
g_E^* = sup_p [1 - ||P_E(p)-Pi_E||^2]
```

or state consistently that `p` is an additional supplied certificate. Calling a particular `g_E(p)` intrinsic to the experiment is too strong unless this distinction is made.

### 4.4 Positive action gap is sufficient, not necessary

The predecessor rotation family and the circle component of the mixed example show that a zero action gap does not imply constant numerical width. Arithmetic and nonuniform finite-horizon effects can still force growth.

Revision 41 identifies a broad expanding class with a sharp exponent. It does not classify finite alphabets or numerical experiments outside that class.

### 4.5 The dominant-nongapped regime is the central missing case

The theorem matches upper and lower exponents only if a type attaining the largest `s_lambda` has positive action gap. Suppose every maximal-orbit type is nongapped while a smaller type expands. The exact upper construction still has order `N^(sigma_X/2)`, but the current converse sees only the smaller exponent.

The paper provides no theorem deciding whether the upper exponent is sharp in that situation. The faithful mixed example is chosen so that the expanding type is already dominant and therefore does not address this gap.

This is not a minor endpoint. It is the boundary between a conditional expansion theorem and an actual classification of the command experiment.

---

## 5. Technical audit of canonical activation

### 5.1 Compactness and copy invariance are handled correctly

The intertwining equations are linear and the isometry condition is closed, so the set of isometric intertwiners is compact. Equivalent copies are treated simultaneously.

The covariance operator lies in the commutant and its eigenspaces are invariant. The spectral formula for `a_lambda` is sound.

### 5.2 The terminal correlation lower bound is coherent

Choose a seed and intertwiner attaining `c_lambda`. The target correlation with the normalized constituent process is `rho a`. Coordinatewise mean error contributes at most `2 epsilon B(J)`, while the terminal decoder pairing is at most `B(J) q_N`. Thus

```text
q_N >= rho c_lambda - 2 epsilon.
```

This correctly uses the actual whole-machine register. No constituent label is supplied to the machine.

### 5.3 The main calibration is still opaque

The quantity entering the theorem is not `a_lambda` but `c_lambda`. The manuscript gives no commutant spectral formula for it. It is an optimization over an isotypic Stiefel manifold with a nonsmooth `l^1` objective induced by the physical queries.

For a general experiment, the reader is left with:

- no closed form;
- no structural description of the maximizing copy;
- no complexity bound for computing it;
- no robust lower estimate beyond division by `sqrt(D)`;
- and no analysis of how it changes under perturbations of the query family.

The definition is canonical, but a canonical optimization is not the same as a computed invariant.

### 5.4 The error range is only sufficient

The threshold

```text
epsilon < rho c_lambda / 2
```

comes from one correlation argument. The paper does not show it is optimal, or even of the correct order for every representation and query family. Near that boundary the theorem gives no width law.

This should be described as a sufficient calibrated regime, not as a complete fixed-error classification.

---

## 6. Technical audit of the exact upper realization

### 6.1 The branch selector is correctly charged

Choose an invariant irreducible decomposition of the reachable space. A branch of real dimension `d_i` receives probability `d_i/r`; its label set is disjoint from every other branch. The conditional target is amplified by the reciprocal branch weight.

The signal assumption

```text
rho <= 1/(8r)
```

ensures that the amplified initial vector lies inside the ball supplied by the minimum-orbit hull. Weighted terminal means sum to the original response. There is no free selector.

### 6.2 Common command rows are genuinely obtained

The minimum-orbit net encloses a contracted copy of the orbit hull. For each command and each label, a convex representation of the contracted command image gives one stochastic row. Since the radial scale changes by the reciprocal contraction, the expected represented vector evolves exactly.

The row choices do not depend on the epoch, although the final decoder depends on the horizon. This is stronger than a merely clocked upper bound.

### 6.3 The construction is nonalgorithmic in the declared resource model

The proof uses existential convex decompositions for every command-label pair. Carathéodory bounds the number of nonzero successors, but not:

- the total table size;
- the bit complexity of the weights;
- the time required to find them;
- their robustness;
- or a finite-random-bit implementation.

This is legitimate under the definition and should remain sharply separated from computational-space rhetoric.

### 6.4 The signal restriction is structural for this compiler, not proved optimal

For arbitrary finite seeds the theorem uses `rho <= 1/(8r)`. Special minimal-orbit or projective seeds allow the larger inherited range `rho <= 1/10`.

The paper does not determine the optimal signal range for a general reachable seed span. This is another reason to regard the result as a sufficient asymptotic theorem rather than a complete resource classification.

---

## 7. Technical audit of the faithful mixed example

### 7.1 The effective group calculation is correct

The rational planar rotation has infinite order. Powers of the two three-dimensional axis rotations generate continuous one-parameter subgroups whose Lie algebra generators and bracket span `so(3)`. The circle command generates a dense `SO(2)` subgroup. Because the product alphabet contains the identities needed to isolate the factors, the effective closure is `SO(3) x SO(2)`.

### 7.2 The absence of a full product gap is correctly demonstrated

Functions depending only on the circle coordinate have multipliers

```text
(1 + exp(2 pi i l alpha))/2.
```

Diophantine approximation supplies integers for which the modulus approaches one. Hence the product regular operator has norm one on mean-zero functions.

### 7.3 The lower bound still depends on a deep qualitative theorem

The `SO(3)` marginal is declared expanding by Benoist–de Saxcé's algebraic-generator theorem. This is a valid external route if all hypotheses are met, but it supplies no numerical constant here.

Thus the example is explicit at the matrix level but not quantitatively effective. It proves existence of a linear asymptotic constant, not a usable finite lower bound.

### 7.4 The example does not address a nongapped dominant type

The dominant type is exactly the expanding three-dimensional summand. The nongapped circle summand has a smaller orbit exponent. Therefore the example confirms the theorem's hypothesis rather than testing its missing boundary.

A materially deeper result would handle a representation whose maximal minimum-orbit type has zero action gap and determine whether arithmetic or other mechanisms recover the geometric upper exponent.

---

## 8. Technical audit of the orbit calculations

### 8.1 The compact adjoint formula is correct and classical

For a compact simple Lie algebra, every vector is conjugate into a closed Weyl chamber. Roots vanishing on the vector form the subsystem generated by the zero simple roots. The orbit dimension is

```text
|Phi| - |Phi_I|.
```

Among proper subsets `I`, the largest root count occurs after deleting one simple node. This yields the displayed table. The minimizing vectors lie on the corresponding fundamental coweight rays.

The proof is coherent. It is also an elementary standard centralizer calculation. Its inclusion improves usability of the width theorem but does not constitute a new classification of compact adjoint orbits.

### 8.2 The defining and low-rank spin actions are standard

The transitivity of `SO(n)`, `SU(n)` and `Sp(n)` on their unit spheres, with the usual smaller stabilizers, is classical. The `Spin(3)`, `Spin(5)` and `Spin(6)` conclusions follow from low-rank identifications.

These are examples, not new representation theory.

### 8.3 The exterior-square stabilizer computation appears correct

Unitary congruence reduces a complex skew matrix to blocks `aJ` and a kernel. At a fixed rank, merging equal positive singular values enlarges the symplectic stabilizer and reduces the orbit. The stabilizer dimensions give

```text
k(4n-6k-1)
```

for rank `2k<n`, and

```text
n(n-1)/2 - 1
```

at full rank. Comparing endpoints gives the listed minimum dimensions.

The `SU(6)/Sp(3)` minimizer of dimension fourteen is a useful example showing that a decomposable highest-weight vector need not minimize the real unit-vector orbit dimension.

### 8.4 The general representation problem remains open

The paper does not supply:

- a highest-weight formula for `s(U)`;
- a classification of minimizing isotropy groups;
- a table for arbitrary fundamental representations;
- general spin representations;
- tensor, symmetric-power or exceptional modules;
- or a practical algorithm for succinct representation data.

Real quantifier elimination for fully listed infinitesimal matrices proves formal decidability in a very expanded input model. It does not amount to a representation-theoretic classification.

### 8.5 The literature comparison is incomplete

A paper whose central invariant is the minimum orbit dimension should compare directly with the compact transformation-group literature on slice theorems, orbit-type stratification, polar and taut representations, cohomogeneity and metric orbit spaces. Relevant bodies of work include the classical transformation-group framework and modern representation-orbit studies such as Gorodski–Thorbergsson and Gorodski–Lytchak.

These sources need not contain the present dynamic width theorem. They are necessary to determine which geometric statements are new, standard, or immediate from existing classifications.

---

## 9. The inherited entropy occupation theorem

### 9.1 The dynamic lower mechanism remains the strongest part of the project

The conditional-centroid quadratic budget, Gaussian smoothing, entropy production and finite-centroid orbital sparsity combine into a cumulative occupation inequality valid for arbitrary hidden states and time-dependent rows.

This avoids the exponential loss of projected-vertex arguments and is a genuine specialist contribution.

### 9.2 Revision 41 does not substantially change this proof

The new action gap supplies exactly the norm inequality needed by the inherited entropy-production step. Canonical activation supplies a better terminal correlation. Uniform orbit geometry supplies the same small-ball exponent.

The hard amortized converse itself is inherited. The editorial case for v41 must therefore be assessed as a refinement and extension of one prior specialist theorem, not as an entirely new foundational theory.

### 9.3 The constants remain proof constants

The entropy argument uses a single Gaussian scale, crude cap unions, a Gaussian maximum-entropy bound and conservative norm estimates. The resulting constants are not optimized and may be enormous.

The paper determines an exponent under fixed calibration, not leading constants or finite integer widths.

---

## 10. Source and priority assessment

### 10.1 The Chen–Wu version record is no longer a decisive objection

The manuscript now records both versions, their dates, titles and theorem locations. The sign-versus-numerical separation is also proved internally, so the main theorem does not depend on the exact external strict-cutpoint upper constant.

Because rapidly changing preprints can be inconsistently indexed, the final submission should retain archived versioned copies or permanent source identifiers permitted by copyright. The present repository record is substantially better than v39.

### 10.2 The optional LPS bridge remains incompletely audited

The arithmetic appendix states exactly the imported inequality and proves the parity, quotient and normalization steps locally. It still does not provide an independently inspected original theorem/page from the LPS papers.

This is responsible disclosure. Since the v41 headline theorem and mixed example do not use LPS, it is not a correctness objection to the main result. It does mean the six-gate numerical constant should remain an optional external corollary rather than part of the editorial centerpiece.

### 10.3 The transformation-group novelty audit is insufficient

The manuscript's source audit is careful about quantum automata and spectral gaps but much thinner around the new headline invariant. Root tables and one orbitopes citation do not replace a serious survey of minimum orbit dimensions and stabilizer strata in compact representations.

Before any broad originality claim, an expert in compact transformation groups should assess the relation to established orbit-type and low-cohomogeneity classifications.

---

## 11. Resource and semantic limitations

### 11.1 Label width is not program size

A polynomial label count means logarithmic label bits, but the transition table may contain polynomially many rows with arbitrary real entries, and its construction is free. The theorem does not bound description length.

### 11.2 Exact atomic sampling is a strong oracle

The machine samples arbitrary real stochastic rows in one step. Rational projector coordinates do not imply rational transition weights for algebraic commands. Exact fair-bit compilation is a distinct resource problem and may require additional state, time and error.

### 11.3 Horizon-specific redesign is essential

The net scale, represented radius and final decoder depend on `N`. No one autonomous machine is required to work for all stopping lengths. The result is not an anytime memory theorem.

### 11.4 One selected query is weaker than a joint-output channel

The machine answers only one terminal coordinate chosen after the word. It need not maintain a compatible joint distribution of all answers or support repeated queries. A joint-output task may obey a different direct-sum law.

### 11.5 Numerical preservation is stronger than strict cutpoint, but narrower than general simulation

The attenuating constant-width sign machine correctly separates these semantics. The growing width theorem concerns fixed numerical accuracy for one structured family of matrix coefficients. It is not a general theorem on quantum automata, process tensors, bounded-error language recognition or classical simulation of arbitrary quantum channels.

---

## 12. Pipeline assessment

The local v41 chain is:

```text
actual command matrices
    -> effective compact action
    -> constituent sphere/Lebesgue gap

reachable seed span
    -> canonical isotypic activation
    -> terminal constituent correlation

uniform orbit geometry
    + inherited entropy occupation
    -> hidden-width lower exponent

minimum-orbit net
    -> contracted orbit hull
    -> exact common-row upper realization

one dominant expanding type
    -> matched exponent

root/stabilizer calculations
    -> evaluated representation examples.
```

This is a coherent local chain.

It is not a bridge in either controlling repository DAG:

```text
A2 -> A3 -> A4 -> C2 -> D1
```

or

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

Those chains still require, among other things:

- a branchwise raw Fourier/local-limit theorem;
- stopped large deviations with exact terminal contraction;
- a global past kernel and renewal resolvent;
- law–hierarchy realizability;
- a Nisio resolvent and nonlinear semigroup;
- a diagonal graph core;
- regular filtering and measurable selectors;
- changing-filtration optional projection;
- and typed latent-phase contraction.

The v41 status file correctly records as unresolved:

- historical A2 replacement;
- B4 aggregate closure;
- C2 aggregate closure;
- the eleven-paper aggregate;
- fully adaptive collision scheduling;
- all highest-weight orbit minima;
- finite width optima;
- independent review;
- and original-page LPS verification.

The local finite-memory theorem does not discharge any of those obligations. The “Foundations” branding therefore remains unsupported by the actual dependency graph.

---

## 13. Editorial assessment

Revision 41 is mathematically stronger and conceptually cleaner than Revision 39. It has successfully answered the two sharpest criticisms in r25:

1. the gap no longer depends on a redundant presenting group;
2. the calibration no longer depends on a chosen splitting of equivalent copies.

The faithful mixed example and the `SU(6)` exterior-square minimizer are useful additions. The article now has a coherent theorem spine.

Nevertheless, the paper still does not meet a top-four standard.

The central theorem is conditional on an unclassified infinite-dimensional expansion property and on fixed nonvanishing calibration. Its most difficult dynamic mechanism is inherited. Its new geometric calculations are largely classical. Its representation invariant is evaluated only on selected families. The model is deliberately nonuniform and oracle-like. The result has no effect on the repository's principal analytic program.

The correct editorial classification is a potentially strong specialist article at the intersection of positive realization, compact group actions, information theory and probabilistic automata.

---

## 14. Minimum changes before a credible specialist submission

These changes are not a route to Annals, Inventiones, JAMS or Acta acceptance. They are the minimum required for a fair independent specialist review.

### 14.1 Retitle the paper

Remove “General Theta Foundations I.” Use a subject title such as:

- *Action Gaps and Hidden Width of Numerical Group Experiments*;
- *Minimum-Orbit Exponents for Stochastic Positive Realizations*;
- *Entropy Occupation Bounds for Compact-Group Transducers*.

The repository program name has no role in the proof.

### 14.2 State the theorem as a conditional action-gap law

The abstract and introduction should say explicitly that the theorem classifies the exponent **within the class of experiments possessing an expanding dominant type at fixed calibration**. It is not an all-alphabet classification.

### 14.3 Canonicalize the proof law

Either optimize the action gap over command distributions or treat the distribution as an explicit certificate throughout. Do not call a particular proof-side choice intrinsic without qualification.

### 14.4 Address dominant nongapped types

This is the main mathematical frontier left by the paper. Give lower bounds or matching constructions when all maximal `s_lambda` types have zero action gap. Arithmetic rotations show that zero gap does not imply trivial memory.

### 14.5 Make `c_lambda` usable

Develop a dual formulation, semidefinite/convex program, commutant reduction, structural optimizer or representation-specific formulas for the query-calibrated activation. At present the actual error range remains opaque.

### 14.6 Complete the transformation-group literature map

Compare the minimum-orbit theorem with slice theory, orbit-type stratification, polar/taut representations, cohomogeneity classifications and metric quotient results. Explain exactly which geometric statement is new.

### 14.7 Separate inherited and new proof obligations

The article should make clear that the entropy occupation theorem is the main inherited converse, while v41 contributes intrinsic hypotheses, calibration and representation evaluations.

### 14.8 Keep resource models separate

Maintain distinct statements for:

- atomic label width;
- label bits;
- total table size;
- finite-bit or fair-bit implementation;
- autonomous state complexity;
- and uniform computational space.

### 14.9 Remove pipeline sales language

The focused article should not require a reader to understand A2/B4/C2 labels or thousand-page archives. Keep those records in repository metadata.

### 14.10 Obtain independent expert review

The entropy argument should be read by experts in information theory and positive realization; the action-gap input by random-walk/spectral-gap experts; and the orbit calculations by compact transformation-group and representation-theory experts.

---

## 15. Specific major and minor points

1. Define an optimized alphabet action gap, or state `p` as part of the theorem data.
2. Distinguish positivity of `g_E` from availability of a numerical lower bound for it.
3. State prominently that the harmonic supremum is not effectively certified by finite truncation.
4. Clarify whether positivity of the action gap is stable under small perturbations of command probabilities in every stated application.
5. Do not call the theorem an all-alphabet classification.
6. State the unresolved dominant-nongapped case in the introduction, not only in the conclusion.
7. Give a computational or dual formulation for `c_lambda`.
8. Separate the spectral formula for `a_lambda` from the non-spectral optimization defining `c_lambda`.
9. State how `c_lambda` changes under duplication or rescaling of query columns.
10. Explain whether the sufficient error threshold can be improved by using a non-coordinate test functional.
11. Keep the reachable dimension `r` distinct from the ambient query dimension `D` in every calibration.
12. In the mixed example, state explicitly that the `Theta(N)` lower constant is qualitative and gap-dependent.
13. Do not describe rational command matrices as giving a fully effective theorem when the gap is qualitative.
14. Add references on compact transformation groups, slice theory and orbit-type stratification.
15. Add references on polar, taut and low-cohomogeneity representations where relevant.
16. State that the adjoint table is a classical compact semisimple centralizer computation.
17. State that the exterior-square calculation is a family computation, not a general fundamental-representation classification.
18. Verify all exceptional root-deletion ties in a table or appendix, rather than only naming maximal subsystems in prose.
19. Keep compact real-vector orbits separate from complex nilpotent and projective orbits.
20. In the `SU(4)` exterior-square case, retain the distinction between the real six-dimensional form and its two-copy realification.
21. State that quantifier elimination is formal decidability for fully expanded algebraic matrices, not an efficient representation algorithm.
22. State whether disconnected effective groups can be reduced to the identity component without changing the numerical experiment or exponent.
23. Treat finite groups separately; orbit dimension zero alone should not be presented as a universal statement without an explicit constant-state construction.
24. Keep fixed dimension explicit in every asymptotic theorem.
25. Keep fixed nonvanishing signal and fixed error explicit in every exponent statement.
26. Do not infer any uniform-in-rank or uniform-in-highest-weight constant.
27. State the total number of table rows in the exact upper construction, not only the number of successors per row.
28. Do not use Carathéodory sparsity as a proxy for efficient table construction.
29. Keep arbitrary-real atomic rows separate from rational-row realizations.
30. Include the final two-label output cut consistently in finite-width statements.
31. Keep available labels distinct from positive-probability labels under the converse law.
32. State that the command word is externally supplied and not adaptively optimized.
33. State that the machine is horizon-specific and not an anytime recognizer.
34. Keep one selected query separate from a joint query channel.
35. Preserve the distinction between fixed numerical accuracy and cutpoint semantics.
36. Do not present the fixed quantum realization as a new quantum operation or general simulation model.
37. Keep Chen–Wu versioned citations pinned in the final submission.
38. Do not use finite verification to certify Benoist–de Saxcé or LPS gaps.
39. Do not use source hashes, archive length or regression volume as evidence of significance.
40. Remove “Foundations” from any specialist submission title.

---

## 16. Scorecard

| Criterion | Assessment |
|---|---|
| Correctness in the stated model | Main new proofs appear coherent; no short fatal counterexample found |
| Advance over Revision 39 | Substantial repair: effective action gap, canonical activation, arbitrary seeds, dominant-only theorem, mixed example |
| Originality boundary | Incomplete; transformation-group and orbit-classification literature not sufficiently audited |
| Mathematical depth | Strong specialist level; below top-four general-mathematics level |
| Sharpness | Matching exponent only under an expanding dominant type and fixed calibration |
| Action hypothesis | Intrinsic to a supplied action law, but infinite-dimensional, non-effective and not necessary |
| Calibration | Canonical but only partly computed; `c_lambda` remains an opaque optimization |
| Representation theory | Useful classical tables and one infinite family; no general highest-weight classification |
| Generality | Connected fixed-dimensional actions, fixed signal/error, one terminal query |
| Computational model | Horizon-specific nonuniform atomic rows; tables, arithmetic and sampling free |
| External dependencies | Deep qualitative algebraic gap; optional LPS source bridge still incomplete |
| Pipeline impact | None on decisive A2/B4/C2/D1 analytic gates |
| Presentation | More coherent and honest; program branding still misleading |
| Reproducibility engineering | Strong, but not proof, priority or significance |
| Editorial recommendation | Reject at top-four level; reconsider only after specialist repositioning |

---

## 17. Final assessment

Revision 41 is the strongest and cleanest version of this manuscript line so far. It has repaired the nonintrinsic presenting-group hypothesis, removed arbitrary multiplicity coordinates, allowed arbitrary seed spans, and proved that one dominant expanding type suffices. The faithful `SO(3) x SO(2)` example is a meaningful demonstration, and the representation tables make the abstract exponent more concrete.

Those are genuine accomplishments.

They do not establish a general foundations theory.

The action gap is a strong, infinite-dimensional and usually non-effective sufficient condition. The dominant nongapped regime is untouched. The actual error threshold depends on an unresolved query-norm optimization. The representation invariant is computed only on selected classical families. Much of the difficult dynamic converse is inherited. The model remains highly nonuniform. The main repository pipeline is unaffected.

Put bluntly:

**Revision 41 gives a clean conditional width law for compact numerical experiments with an expanding dominant action. It does not classify finite memory, positive realization, or quantum/classical simulation beyond that class.**

My recommendation is firm:

**Reject for Annals of Mathematics, Inventiones Mathematicae, Journal of the AMS, or Acta Mathematica.**

A substantially retitled paper centered on action-gap certificates and minimum-orbit exponents for hidden stochastic transducers could merit strong specialist review, especially after the proof law is canonicalized, the dominant-nongapped regime is isolated as the central open problem, the query calibration is made computationally usable, and the transformation-group literature is fully audited. That would be a new editorial submission rather than another internal revision marketed as approaching the four-journal threshold.
