# Independent Referee Report — General Theta Foundations I, Revision 41

**Manuscript:** *General Theta Foundations I: Intrinsic Action Gaps and Numerical Memory*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v41-referee-ready-2026-09-26`  
**Reviewed head:** `08773b2705c5ac92716df5daf42a54f3b61bca34`  
**Native mathematical source recorded by the manuscript:** `282bc34bbbeaa56a2ec36c6daf438e545dcfeb37`  
**Controlling previous report:** `9707844addcd9eb478eb863514f288923f9d40fd`  
**Existing first review of this head:** r26, commit `f43279f315562bb00e9410da59755c5bb7b4ca9f`  
**This independent review branch:** `review/general-theta-foundations-i-v41-intrinsic-action-independent-harsh-top4-r27-2026-09-26`  
**Date:** 26 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is an independent second review of the same Revision-41 manuscript head. A fresh remote branch survey found no Revision 42 or later referee-ready branch at the time of review. I therefore do not pretend that a new manuscript has arrived. This branch starts directly from the reviewed v41 head, does not contain or amend r26, and adds only this report.

Revision 41 is a serious specialist contribution. It repairs several concrete defects of Revision 39: the expansion hypothesis is attached to the effective command action rather than to an arbitrary presenting group; activation is canonicalized at the isotypic level; arbitrary finite seed sets are reduced to their actual invariant span; and only one dominant active type is required to expand. The faithful `SO(3) x SO(2)` example demonstrates that the new statement is genuinely broader than a full-effective-group-gap theorem. The adjoint and exterior-square calculations also make the orbit exponent less formal than in the preceding revision.

I did **not** find a short fatal counterexample to the principal displayed results. In the precise finite-horizon, wordwise, nonuniform, clocked, atomic stochastic-row model defined by the paper, the following arguments appear internally coherent:

- presentation invariance of the action operator;
- equality of the sphere and Lebesgue action gaps;
- the constituent-level entropy occupation argument;
- the commutant covariance formula for Euclidean activation;
- the query-calibrated terminal correlation;
- the exact paid-branch upper construction;
- the faithful mixed expanding/nonexpanding example;
- the deleted-root formula for compact simple adjoint actions;
- and the skew-congruence stabilizer calculation for `wedge^2 C^n`.

The negative recommendation is therefore not an allegation that the theorem is false. It is an editorial and mathematical judgment about what the theorem actually classifies, how effectively its hypotheses can be checked, how much is inherited, and whether the result has the breadth and conceptual finality expected at the four leading general mathematics journals.

The decisive objections are these.

1. **The paper still proves only a sufficient expansion theorem, not a classification of numerical memory.** A positive action gap on one dominant active type yields a matching exponent. The theorem does not show that such a gap is necessary, and it does not determine the width when every maximal-orbit type is nongapped. The dominant-nongapped regime is not a small endpoint case; it is the main region excluded by the headline.
2. **The quantity called “intrinsic action gap” is not canonical until the proof-side command law is optimized or included as part of the datum.** The numerical experiment specifies a finite alphabet and matrices, not a probability law. Different test laws on the same alphabet can produce gap zero or a positive gap and can change every lower-bound constant. Because the target law is wordwise, the referee is free to choose the test law. The natural alphabet invariant is therefore an optimization over the probability simplex, not an arbitrary fixed certificate.
3. **Even after that canonicalization, gap positivity is infinite-dimensional and generally non-effective.** It is the norm of a Koopman operator modulo invariant functions, equivalently a supremum over all harmonic degrees. The paper explicitly disclaims certification by finite truncation. No algorithm, semialgebraic criterion, quantitative lower bound, or finite witness is supplied for general rational or algebraic command matrices.
4. **The actual error threshold remains only partly computed.** The paper gives a clean spectral formula for the Euclidean activation `a_lambda`, but the theorem uses the query-calibrated quantity `c_lambda`. This is a nonconvex optimization over isometric intertwiners with an `l^1` operator norm. No closed formula, useful dual, optimizer structure, perturbation theory, or algorithm is provided.
5. **The representation-theoretic part is selective rather than classificatory.** The adjoint table is a classical centralizer calculation; the defining and low-rank spin cases are standard transitive actions; and the exterior-square calculation is one valuable infinite family. There is no general highest-weight formula, no classification of minimizing stabilizers for irreducible modules, and no treatment of most spin, tensor, symmetric-power, or exceptional fundamental representations.
6. **The novelty boundary with compact transformation-group geometry is not adequately audited.** Orbit-type strata, quotient-equivalence, reductions, polar representations, taut representations, cohomogeneity and metric orbit spaces form a mature literature. The current bibliography does not compare its minimum-orbit invariant and all-strata chart argument theorem-by-theorem with that literature.
7. **Most of the difficult hidden-state converse is inherited from the predecessor chain.** Revision 41 improves the hypothesis and calibration and adds examples and orbit calculations. The entropy occupation theorem, arbitrary-hidden-state mechanism, uniform orbit concentration framework and minimum-orbit compiler were already established. The new paper is a strong consolidation and refinement, not a second general-journal-scale breakthrough.
8. **The resource model is highly permissive and nonuniform.** Horizon, epoch, machine redesign, complete real transition tables, table construction and lookup, exact arithmetic, and atomic sampling from arbitrary real stochastic rows are free. This is a positive-realization label-width theorem, not a uniform-space lower bound, total branching-program lower bound, finite-random-bit implementation theorem or autonomous-memory theorem.
9. **The theorem is narrow in several further quantifiers.** The effective group is assumed connected; dimension, signal and tolerance are fixed before the horizon grows; only one terminal coordinate query is selected; adaptive experimental design, simultaneous query channels, disconnected actions, finite groups and uniform high-rank regimes are excluded.
10. **The repository-wide Foundations pipeline remains open at every difficult analytic gate.** Nothing in Revision 41 proves the branchwise Fourier/local-limit theorem, stopped large deviations, global renewal kernel, nonlinear Nisio semigroup, graph core, filtering regularity, optional projection or typed contraction required by the controlling A/B/C/D dependency chains.

Revision 41 could become a strong specialist paper after substantial repositioning. It is not close to the standard of the four leading general mathematics journals, and the prefix “General Theta Foundations I” continues to overstate both the theorem's mathematical scope and its role in the repository's main analytic program.

---

## 1. Scope and independence of this report

The latest remote referee-ready branch was Revision 41. No Revision 42 branch was visible. I therefore reviewed the exact same manuscript head independently rather than assigning a new revision number to unchanged mathematics.

I examined:

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
- `GAP_CERTIFICATE.json`;
- the reviewed publication and native source commits;
- the existing r26 report, only as a record of the first referee's conclusions;
- and the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I also made targeted external comparisons with primary or author-hosted work on compact representation orbit spaces, quotient-equivalent representations, polar and taut representations, cohomogeneity, orbitopes, manifold quantization, compact-group spectral gaps, positive-semidefinite rank and current strict-cutpoint quantum-automata simulation.

In particular, the orbit-space boundary should be compared directly with work such as:

- Claudio Gorodski and Alexander Lytchak, *On orbit spaces of representations of compact Lie groups*, arXiv:1109.1739;
- Claudio Gorodski and Alexander Lytchak, *Isometric actions on spheres with an orbifold quotient*, arXiv:1407.5863;
- Claudio Gorodski and Gudlaugur Thorbergsson, *Representations of compact Lie groups and the osculating spaces of their orbits*, arXiv:math/0203196;
- and the classical polar-representation and transformation-group literature cited through those works.

I am not asserting that any one of these papers contains the dynamic memory theorem. I am asserting that a four-journal originality claim involving minimum orbits, orbit strata and representation quotients requires a substantially deeper comparison than the current article supplies.

This review branch starts at the manuscript head and adds only this report. It does not merge, copy, amend or supersede r26.

The focused article is thirty pages and sufficiently self-contained for the new claims. The 545-page mathematical archive and 1098-page development archive are provenance records, not additional mathematical weight. Clean builds, hashes, page comparisons and negative controls are useful engineering, but they are not proof, priority review or evidence of journal significance.

---

## 2. What Revision 41 actually proves

### 2.1 The experiment and resource

The prescribed response is

```text
Pr(B=b | x,w,j)
  = [1 + b rho <e_j,A_w x>]/2,
```

for every seed, complete command word and selected terminal coordinate query.

A horizon-`N` classical realization has finite label sets at every cut, command-dependent stochastic rows and bounded terminal decoder columns. The optimized quantity is the maximum number of available labels, including unreachable padding and the final held two-label output cut.

The resource does **not** charge:

- the epoch;
- the horizon;
- redesign of the machine for every horizon;
- the transition and decoder tables;
- construction or lookup of those tables;
- real arithmetic;
- or exact sampling from arbitrary real stochastic rows.

This is a mathematically legitimate positive-realization width. It should not be identified with ordinary computational space.

### 2.2 The effective action

The manuscript sets

```text
H = closure <A_a : a in A> subset O(V)
```

and restricts to the invariant span of the seed orbits. On an invariant irreducible model `E`, a chosen command law `p` defines

```text
P_E f(u) = sum_a p(a) f(A_a^{-1}u),
Pi_E f(u) = integral_H f(h^{-1}u) dh,
g_E = 1 - ||P_E-Pi_E||^2.
```

This removes the spurious dependence on an arbitrarily enlarged presenting group. The gap is invariant under equivalent orthogonal realizations and redundant compact extensions that induce the same matrices and pushed-forward law.

### 2.3 The orbit exponent

For each active irreducible type `lambda`, let

```text
s_lambda = min_{||u||=1} dim(Hu).
```

The geometric theorem gives a uniform orbital small-ball upper bound of order `r^(s_lambda)` for every unit direction, including directions arising from mixed hidden conditional centroids. A minimum-dimensional orbit gives the matching local geometric exponent.

### 2.4 Canonical activation

The active seed span has a canonical isotypic decomposition. Rather than selecting displayed irreducible copies, the paper optimizes over all isometric intertwiners

```text
J : E_lambda -> R_lambda.
```

It defines

```text
a_lambda = max_(x,J) ||J^*x||,
B(J)      = ||J^*||_(l_infinity -> l_2),
c_lambda = max_(x,J) ||J^*x||/B(J).
```

The Euclidean activation satisfies the commutant covariance formula

```text
a_lambda^2
  = d_lambda max_x lambda_max(C_(lambda,x)).
```

The theorem's error threshold, however, uses `c_lambda`, not merely `a_lambda`.

### 2.5 The matched law

Let `sigma_X` be the maximum of `s_lambda` over active nontrivial types. If one type attaining this maximum has positive action gap and

```text
epsilon < rho c_lambda/2,
```

then

```text
W_(N,epsilon) = Theta(N^(sigma_X/2)).
```

The lower bound uses the actual whole-machine hidden state and a conditional-centroid occupation argument. The exact upper bound uses minimum-orbit polytopes in every active irreducible copy, randomizes over copies with paid disjoint branch labels, and uses common command rows with a horizon-dependent decoder.

### 2.6 The faithful mixed example

The ten rational block commands on `R^3 + R^2` generate `SO(3) x SO(2)`. The standard `SO(3)` constituent is qualitatively expanding through an external algebraic spectral-gap theorem, while the circle constituent has no spectral gap. The dominant minimum-orbit dimension is two, so the theorem gives linear width; the circle branch contributes only `O(sqrt(N))` labels.

This is a meaningful example beyond full effective-group expansion.

---

## 3. Technical audit of the action-gap reformulation

### 3.1 Presentation invariance is correctly repaired

The operators depend only on the probability measure supported on the actual matrices acting on `E`. Orthogonal intertwiners conjugate both the command and Haar operators unitarily. Haar probability on a compact presenting group pushes forward to Haar probability on the compact image. Thus adding a trivially acting factor no longer changes the hypothesis.

This directly repairs the central defect of Revision 39.

### 3.2 Sphere and Lebesgue gaps agree

Polar coordinates identify

```text
L^2(E,dz)
 = L^2((0,infinity),r^(d-1)dr)
   tensor L^2(S(E)).
```

Both command averaging and Haar averaging act trivially on the radial factor. The operator norm modulo invariant functions is therefore identical in the sphere and Lebesgue spaces. This is exactly the form needed by the inherited entropy-production lemma.

I see no missing Jacobian or radial normalization issue in this argument.

### 3.3 Harmonic decomposition is a description, not a certificate

The identity

```text
1-g_E
  = sup_l ||P_(E,l)-Pi_(E,l)||^2
```

is correct because the spherical harmonic spaces form an orthogonal invariant decomposition and the operator is block diagonal.

But this formula exposes the major limitation: the hypothesis concerns infinitely many harmonic degrees. A finite numerical computation can only produce lower bounds on the norm, not certify a uniform upper bound strictly below one.

### 3.4 The test law remains an analyst-selected certificate

The numerical experiment is wordwise. The lower proof may impose any command distribution. This freedom is legitimate, but it means the object

```text
g_E(p)
```

is not determined by the experiment until `p` is supplied.

For a fixed alphabet, the map

```text
p -> ||P_E(p)-Pi_E||
```

is continuous in operator norm, because `P_E(p)` depends linearly on `p` and every command operator has norm one. The probability simplex is compact. Hence the canonical quantity

```text
g_E^*(A)
  = max_(p in Delta(A))
      [1-||P_E(p)-Pi_E||^2]
```

is well-defined and attained.

The article should formulate its alphabet-level theorem using this optimized gap, or state explicitly that a probability vector `p` is an externally supplied certificate. Calling a nonoptimized `g_E(p)` “intrinsic” is too strong.

### 3.5 Positivity is not characterized

Even the optimized gap does not yield a complete theorem. The paper supplies sufficient certificates through deep external group-expansion results in selected semisimple cases. It does not characterize when a given finite matrix alphabet has positive action gap on its represented sphere.

For tori the gap can vanish because Fourier multipliers approach one. For algebraic generators of compact simple groups a deep theorem can supply a qualitative gap. Between these regimes lie numerous reducible, nonsemisimple, disconnected and arithmetic cases that the paper does not classify.

---

## 4. Technical audit of canonical activation

### 4.1 The isotypic formulation is the correct invariant object

Equivalent irreducible copies are not canonically split. Optimizing over all isometric intertwiners avoids decomposition-dependent projection norms. Compactness follows from the finite-dimensional intertwining equations and `J^*J=I`.

The diagonal-copy example correctly illustrates the defect of a coordinatewise copy calibration.

### 4.2 The commutant covariance formula is coherent

The Haar covariance

```text
C_(lambda,x)
  = integral_H
      (hP_lambda x)(hP_lambda x)^* dh
```

commutes with the action. For an isometric intertwiner `J`, the self-adjoint operator `J^*CJ` commutes with an irreducible real representation. In real, complex and quaternionic commutant types, a self-adjoint element of the division-algebra commutant is a real scalar. Taking traces gives

```text
J^*CJ = ||J^*x||^2 I/d_lambda.
```

Choosing an irreducible copy inside the top eigenspace proves the reverse inequality. The displayed spectral formula for `a_lambda` is therefore sound.

### 4.3 The query-calibrated constant is still opaque

The actual terminal bound uses

```text
B(J)=||J^*||_(l_infinity -> l_2)
    =max_(||u||=1)||Ju||_1.
```

For a fixed `J`, norm duality also gives the finite formula

```text
B(J)=max_(sigma in {+1,-1}^D)||J^*sigma||_2.
```

Thus one part of the optimization is explicit but combinatorial. The remaining maximization over the compact intertwiner manifold is nonconvex and may depend delicately on the physical query basis.

The paper gives only

```text
a_lambda/sqrt(D) <= c_lambda <= a_lambda.
```

For a headline theorem whose admissible error is `rho c_lambda/2`, this is not enough. A specialist version should at least provide:

- a finite-dimensional dual or semidefinite formulation;
- a structural description in the real, complex and quaternionic multiplicity models;
- perturbation bounds under changes of the seed and query frame;
- and computed values in its principal examples.

### 4.4 Terminal calibration is otherwise correct

Fix `x,J` attaining the ratio, normalize `J^*x`, and track the resulting constituent orbit under the same external command word. The target correlation is `rho ||J^*x||`; coordinatewise mean error contributes at most `2 epsilon B(J)`; and the decoder vector satisfies `||J^*d||_2<=B(J)`. Hence

```text
q_N >= rho c_lambda - 2 epsilon.
```

This lower bound uses the actual whole-machine state and does not give the machine free knowledge of `J` or the active type.

---

## 5. Technical audit of the dynamic lower bound

### 5.1 The conditional-centroid recursion remains valid

Under an independently chosen command law, let `Y_t` be the constituent orbit process and `S_t` the actual machine state. The stochastic update depends on the past only through `(S_t,a_(t+1))`, so

```text
Z_(t+1)=E[U_a Z_t | S_(t+1)].
```

The conditional-expectation projection identity gives a telescoping quadratic loss

```text
sum_t Delta_t <= 1.
```

No hidden conditional independence assumption is used.

### 5.2 The entropy occupation mechanism is the difficult inherited theorem

Gaussian smoothing converts each stochastic compression into a one-sided entropy loss controlled by `Delta_t/tau^2`. The action gap creates entropy away from invariant densities. The uniform orbital small-ball bound prevents a distribution supported on few conditional centroids from being nearly invariant. A single Gaussian scale is amortized through the entire horizon.

This is the central mathematical mechanism. It is not new to Revision 41; the present paper imports it with a complete proof from the predecessor chain.

### 5.3 The theorem is genuinely all-hidden-state

The conditional centroids are indexed by the actual positive-probability hidden labels under the converse law. No internal basis state is assumed to carry a predictive vector, and no bound on the number of vertices of a projected simplex section is used.

The lower bound therefore applies to hidden stochastic lifts, not only vector-state realizations.

### 5.4 The dominant-nongapped case is not controlled

Suppose `sigma_X` is attained only by types with zero action gap, while lower-dimensional types expand. The current theorem yields only a lower exponent from the expanding smaller type, whereas the exact upper construction still has order `N^(sigma_X/2)`.

The true order may depend on Diophantine, Fourier, representation-specific or compatibility phenomena not captured by `s_lambda` alone. Earlier rotation examples in the repository already show that nongapped actions can have nonconstant growing width.

This is the central missing case. Until it is addressed, the paper should not describe the exponent as classified by the representation.

---

## 6. Technical audit of the exact upper realization

### 6.1 Minimum-orbit geometry is used correctly

For a nontrivial irreducible orthogonal representation, the Haar covariance of a minimum-orbit unit vector is `I/d`. The orbit convex hull therefore contains a fixed Euclidean ball. A finite intrinsic `h`-net on the orbit has `O(h^-s)` points.

At a support maximum the first tangential derivative vanishes. Compactness bounds the second fundamental form, producing a quadratic support loss `O(h^2)`. With `h` of order `N^-1/2`, a slightly contracted orbit hull can be used at every layer while the represented scale expands by the reciprocal contraction.

This yields exact expected dynamics and `O(N^(s/2))` labels.

### 6.2 The branch selector is correctly charged

The reducible upper machine randomizes at initialization over irreducible copies and stores the selected branch in a disjoint state alphabet. Reciprocal branch weighting amplifies the conditional represented vector so that the weighted marginal outputs sum to the target response. No free selector or uncharged constituent identity remains.

### 6.3 Sparse rows do not imply efficient construction

Caratheodory's theorem bounds each row's support by at most `d+1` successors. It says nothing about:

- the number of rows in the full table;
- how the convex coordinates are found;
- their arithmetic complexity;
- their bit length;
- or exact sampling from irrational probabilities.

For width `K`, every command table may have on the order of `K` independently specified sparse rows, and the nonuniform description can be enormous. The article is honest that this cost is free, but the limitation is editorially important.

### 6.4 Fixed horizon and one final query are essential

The decoder depends on `N`; the construction need not answer correctly at earlier stopping lengths; and one coordinate query is selected only after the command word. An anytime decoder, a joint channel of all coordinates, or repeated queries would be a different task and could invalidate the direct-sum maximum law.

---

## 7. The faithful mixed example

### 7.1 The group generation argument is plausible

The rational rotations about two distinct axes generate dense one-parameter subgroups whose infinitesimal generators and bracket span `so(3)`. The irrational circle rotation generates a dense `SO(2)`. Because the product alphabet contains the necessary identities, its closure is `SO(3) x SO(2)` and the action is faithful.

### 7.2 The gap input is external and qualitative

The `SO(3)` action gap is obtained from the Benoist--de Saxce algebraic spectral-gap theorem after verifying algebraicity and density. No numerical gap is computed. The circle average has Fourier multipliers approaching modulus one, so the full product regular gap is absent.

The example successfully demonstrates the logical strengthening from full-group expansion to dominant-type expansion. It does not provide an effective lower constant.

### 7.3 The example does not address the missing dominant-nongapped regime

The expanding `SO(3)` constituent has minimum orbit dimension two; the nongapped circle has minimum orbit dimension one. Thus the expanding type is dominant. The example is exactly within the new theorem.

It does not answer what happens when a nongapped type has the largest orbit exponent. The paper should state this distinction more prominently.

---

## 8. Representation-theoretic calculations

### 8.1 Compact simple adjoint actions

For a compact simple Lie algebra, every vector is conjugate into a closed Weyl chamber. The centralizer roots are precisely those generated by simple roots vanishing at the chamber point. Maximizing the proper root subsystem gives

```text
s(Ad)
 = |Phi|-max_alpha |Phi_(Delta\{alpha})|.
```

The resulting `A`, `B`, `C`, `D`, `G2`, `F4`, `E6`, `E7`, and `E8` table is consistent with the standard root counts. The minimizing rays and Levi centralizers are classical consequences of the same calculation.

This is a useful evaluation of the width exponent, not a new classification of compact simple Lie algebras or their adjoint orbits.

### 8.2 Defining and low-rank spin modules

The defining real, complex and quaternionic actions are transitive on their unit spheres, so their orbit dimensions are the sphere dimensions. The low-rank spin claims follow from the standard identifications `Spin(3)=Sp(1)`, `Spin(5)=Sp(2)`, and `Spin(6)=SU(4)`.

These examples are correct but classical.

### 8.3 Second exterior powers

The unitary skew-congruence normal form decomposes a skew matrix into repeated positive singular-value blocks and a kernel. The stabilizer dimension is maximized, at fixed rank, when positive singular values coalesce. The manuscript's formulas

```text
k(4n-6k-1)
```

for rank `2k<n` and

```text
n(n-1)/2-1
```

for full rank give the displayed minima. The special `SU(6)/Sp(3)` orbit of dimension fourteen is correctly smaller than the decomposable vector orbit of dimension seventeen.

This is a worthwhile example because it shows that a minimum real-vector orbit need not be the decomposable highest-weight orbit.

### 8.4 The general representation problem remains open

The paper still gives no systematic solution for arbitrary irreducible highest weights. In particular it does not classify:

- general spin and half-spin modules;
- higher exterior and symmetric powers;
- tensor products;
- exceptional fundamental representations;
- or minimizing stabilizers in general real, complex and quaternionic types.

The theorem expresses an exponent through `s_lambda`; it does not generally compute that invariant.

---

## 9. Missing transformation-group boundary

The paper's all-strata estimate is an elementary finite-chart consequence of a uniform rank floor. That proof may well be a convenient self-contained lemma. But its surrounding language—minimum orbits, orbit-type strata, effective actions, reductions and quotients—belongs to a large established field.

The literature contains, among other things:

- orbit-type stratification and slice-theorem methods;
- quotient-equivalence and reductions of compact representations;
- polar representations and sections;
- taut and variationally complete representations;
- classifications at low cohomogeneity and copolarity;
- metric quotient rigidity and orbifold quotient classifications.

The manuscript currently cites root-system background and orbitopes, but not the closest systematic representation-orbit literature. A top-four submission must answer, theorem by theorem:

1. Is the uniform `r^s` upper bound a known consequence of standard slice/tubular-neighborhood estimates?
2. How does the minimum orbit dimension behave under quotient-equivalent or orbit-equivalent representations?
3. Can polar reductions compute or alter the relevant dynamic construction?
4. Which classified representation families already determine all possible minimum strata?
5. Is the contracted orbit-hull construction related to known polar or taut orbit geometry?

The dynamic memory theorem is not automatically contained in those works. The originality claim nevertheless cannot be evaluated fairly without this comparison.

---

## 10. Quantum and automata comparisons

The manuscript now pins the April and August versions of the Chen--Wu preprint separately and keeps strict-cutpoint language simulation distinct from fixed numerical probability preservation. This is responsible.

The internal simplex sign simulator is especially useful. It gives a constant-width positive realization whose numerical amplitude decays exponentially while every sign relative to the cutpoint is preserved. Hence a strict-cutpoint simulation theorem cannot imply the fixed-accuracy width result.

The comparison remains narrow:

- one external reset seed;
- one command word of known length;
- one selected final numerical query;
- fixed positive tolerance;
- and a horizon-specific nonuniform classical competitor.

It is not a theorem about bounded-error language recognition, total PFA size, autonomous QFA simulation, process tensors, communication complexity or uniform classical space.

---

## 11. Pipeline assessment

The local Revision-41 proof chain is:

```text
actual command matrices
  -> effective action operator
  -> constituent action gap

arbitrary finite seeds
  -> invariant reachable span
  -> canonical isotypic activation
  -> query-calibrated terminal correlation

uniform minimum-orbit geometry
  + inherited entropy occupation
  -> constituent hidden-width lower bound

minimum-orbit net
  -> contracted convex hull
  -> exact common-row upper realization

root and singular-value calculations
  -> evaluated orbit exponents in selected families.
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

- branchwise Fourier and local-limit estimates;
- stopped large deviations with legal finite-memory relaxation;
- one global renewal or Doob kernel;
- nonlinear Nisio resolvents and semigroup range conditions;
- graph-core approximations;
- exact filtering and measurable selection;
- changing-filtration optional projection;
- and typed latent-phase contraction.

Revision 41 proves none of these.

Its own status records correctly leave unresolved:

- the historical A2 replacement;
- B4 and C2 aggregate closure;
- the eleven-paper aggregate;
- fully adaptive collision scheduling;
- all highest-weight orbit minima;
- exact finite width optima;
- original-page LPS verification;
- and independent expert review.

The phrase `closed_local_objectives` in repository metadata must not be converted into a statement that the Foundations program is closed or materially reorganized.

---

## 12. Required changes before a credible specialist submission

These are not a path to top-four acceptance. They are the minimum changes needed for a fair specialist evaluation.

### 12.1 Retitle the article

Remove `General Theta Foundations I`. A subject-specific title should name the actual theorem, for example:

- *Action Gaps and Hidden-State Width of Numerical Group Experiments*;
- *Minimum-Orbit Exponents for Positive Stochastic Realizations*;
- *Entropy Occupation Bounds for Expanding Orthogonal Actions*.

### 12.2 Canonicalize the command-law certificate

Define and use the optimized alphabet gap

```text
g_E^*(A)
  = max_(p in Delta(A))
      [1-||P_E(p)-Pi_E||^2].
```

State whether the maximum can be restricted to full-support laws, whether laziness changes only constants, and how the optimized law interacts across several active constituents.

### 12.3 Isolate the dominant-nongapped problem

State it as the central open problem rather than a minor limitation:

```text
What is W_N when every type attaining sigma_X
has zero action gap?
```

Give conjectures or upper/lower regimes for toral, nilpotent, virtually Abelian and mixed semisimple-toral actions.

### 12.4 Make `c_lambda` usable

Provide a finite optimization formulation, computed examples and stability bounds. At minimum exploit

```text
B(J)=max_(sigma in {+1,-1}^D)||J^*sigma||_2
```

to make clear what can and cannot be computed from the stated data.

### 12.5 Complete the transformation-group literature audit

Add a dedicated section comparing the orbit theorem with quotient-equivalence, polar reductions, orbit-type strata, slice geometry, cohomogeneity, copolarity and taut representation classifications.

### 12.6 Separate the resource models

Maintain distinct conclusions for:

- available atomic labels;
- positive-probability labels under one test law;
- label bits;
- total table size;
- fair-bit implementation labels;
- autonomous states;
- and uniform computational space.

### 12.7 Address disconnected actions

Explain what survives after passage to the identity component, how finite components permute isotypic types, and whether a finite extension can change the width exponent. Treat finite groups separately rather than allowing orbit dimension zero to suggest a universal answer.

### 12.8 Remove repository-pipeline sales language

The focused mathematical article does not need internal A2/B4/C2 labels or thousand-page archive references. Keep them in repository metadata.

---

## 13. Specific major and minor comments

1. Include the probability law `p` in every theorem statement using `g_E`, or replace it by the optimized alphabet gap.
2. State whether the optimizer over `p` is unique; it need not be.
3. Record continuity of the gap in `p` and attainment on the probability simplex.
4. Do not call gap positivity effectively checkable from rational matrices without a proof.
5. Distinguish qualitative external gap theorems from numerical certificates.
6. State that a finite harmonic computation cannot certify the infinite supremum.
7. Give a formal statement of the dominant-nongapped open regime.
8. Compute `c_lambda` in the projective, standard spherical and mixed examples.
9. Give the sign-vector formula for `B(J)`.
10. Explain how `c_lambda` behaves under repeated query coordinates or a nonorthonormal query frame.
11. Clarify whether the theorem is stable under deleting unused coordinate queries.
12. State the total number of table rows in the upper construction, not only successors per row.
13. Do not treat Caratheodory sparsity as an efficiency theorem.
14. Separate arbitrary-real rows from rational-row special cases.
15. Keep exact atomic sampling distinct from finite random-bit implementation.
16. Treat disconnected effective groups separately.
17. Treat finite groups separately.
18. Keep fixed dimension explicit in all asymptotic statements.
19. Keep fixed positive signal explicit.
20. Keep the sufficient error threshold explicit.
21. Do not imply a variable-signal theorem.
22. Keep one selected terminal query separate from a joint output channel.
23. State that the command word is externally supplied rather than adaptively optimized.
24. State that the machine is horizon-specific and not anytime.
25. Keep available labels distinct from positive-probability labels.
26. Include the final two-label cut consistently in finite statements.
27. Add direct references on quotient-equivalent representations and orbit spaces.
28. Add references on polar and taut representations.
29. Explain whether known polar reductions can simplify `s_lambda`.
30. Do not present classical root counts as a new Lie-theoretic classification.
31. State that the adjoint table concerns actual compact real-vector orbits.
32. Keep nilpotent/projective/real-vector orbits clearly separated.
33. For `wedge^2 C^n`, keep Pfaffian-phase and special-unitary conventions explicit.
34. Do not infer all-highest-weight classification from one exterior-power family.
35. Keep the `SO(3) x SO(2)` gap qualitative.
36. State that the mixed example does not solve the dominant-nongapped case.
37. Keep Chen--Wu citations version-pinned.
38. Do not use finite checks to certify external spectral-gap theorems.
39. Do not use hashes, page counts or regression volume as mathematical evidence.
40. Remove `Foundations` from a specialist submission title.

---

## 14. Scorecard

| Criterion | Assessment |
|---|---|
| Correctness in the stated model | Principal proofs appear coherent; no short fatal counterexample found |
| Independence of this report | Fresh second review of the same v41 head; r26 left untouched |
| Advance over Revision 39 | Substantial repair and extension |
| Advance beyond Revision 41 r26 assessment | Same editorial conclusion; sharper focus on `p`, nongapped dominance and orbit-space literature |
| Originality boundary | Incomplete, especially in compact transformation-group geometry |
| Mathematical depth | Strong specialist level, below top-four general-mathematics level |
| Sharpness | Matching exponent only with an expanding dominant type and fixed calibration |
| Gap hypothesis | Intrinsic to a supplied action law, but not to the unweighted alphabet until optimized |
| Effectiveness | Poor in general; infinite-dimensional gap and opaque query calibration |
| Representation theory | Useful selected families, not a general classification |
| Resource model | Horizon-specific nonuniform atomic-row width with free advice and arithmetic |
| Quantum comparison | Correct semantic separation, narrow task |
| External dependencies | Deep qualitative expansion theorems; optional LPS bridge still incomplete |
| Pipeline impact | None on decisive A2/B4/C2/D1 analytic gates |
| Presentation | Improved and honest, but branding remains misleading |
| Editorial recommendation | Reject at top-four level; reconsider after specialist repositioning |

---

## 15. Final assessment

Revision 41 is the strongest and cleanest version of this manuscript line. It correctly replaces the nonintrinsic presenting-group gap, removes arbitrary multiplicity coordinates, allows arbitrary finite seed spans, proves a dominant-only matched theorem, and gives a faithful mixed example. The representation calculations also make the abstract orbit exponent more concrete.

These are genuine accomplishments.

They do not establish a general foundations theory.

The theorem remains conditional on an expanding dominant type. The gap depends on a proof-side law unless optimized. Gap positivity is infinite-dimensional and usually non-effective. The dominant-nongapped regime is unresolved. The actual error threshold depends on a partially opaque query optimization. The representation invariant is evaluated only in selected families. Much of the difficult dynamic converse is inherited. The computational model is highly nonuniform. The main repository pipeline is unaffected.

Put bluntly:

**Revision 41 proves a clean conditional exponent law for numerical group experiments admitting an expanding dominant action. It does not classify finite memory, positive realization or quantum/classical simulation outside that class.**

My recommendation is firm:

**Reject for Annals of Mathematics, Inventiones Mathematicae, Journal of the AMS, or Acta Mathematica.**

A substantially retitled paper centered on action-gap certificates, canonical activation and minimum-orbit exponents for hidden stochastic transducers could receive strong specialist consideration. Before that submission, the authors should optimize or explicitly certificate the command law, elevate the dominant-nongapped regime to the central open problem, make the query calibration computationally usable, and complete the compact transformation-group literature comparison.
