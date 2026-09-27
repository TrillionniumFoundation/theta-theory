# Referee Report — General Theta Foundations I, Revision 55

**Manuscript:** *Stochastic Purification and Sharp Noise Thresholds for Compact Group Experiments*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v55-stochastic-purification-2026-09-27`
- `revision/general-theta-foundations-i-v55-referee-ready-2026-09-27`

**Reviewed publication head:** `00a0864003790aa3efcdc7f88358b6fa27ffe868`  
**Validated native-source commit:** `22609df8f2db2f480f708aa33e48d2813690cedc`  
**Workflow trigger:** `9ccf1431b811db39b42fa23b86c10a9fb0ade2f4`  
**Qualification workflow:** `36313303021`  
**Source predecessor:** Revision 54 publication `1eb16a3f857d17a91dc1c82906ef16a5965a47d2`  
**Controlling prior report:** r36, `9c92a08458b92fd831010dca835de8e2239f82fc`  
**Review branch:** `review/general-theta-foundations-i-v55-stochastic-purification-harsh-top4-r37-2026-09-27`  
**Date:** 27 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

**Mathematical disposition:** Revision 55 is a substantial advance over Revision 54. It resolves the most conspicuous structural question left open in r36: for stationary realizations, transition randomness can be removed without increasing either the number of labels or the uniform approximation error. It also gives an exact characterization of the unrestricted stationary minimum, treats all nonempty exact-return languages by length phase, establishes strict-side and zero-boundary results for compact groups with infinitely many components, and supplies a sharp linear-width profinite example.

I did **not** find a fatal counterexample to the following new results in their declared scope:

1. the minimum-rank-idempotent reduction in the joint physical/stochastic closure;
2. the recurrent-simplex permutation action;
3. width- and error-preserving stationary purification;
4. the permutation-closure characterization of the unrestricted stationary minimum;
5. the open-normal-subgroup criterion for finite stationary realizability;
6. the five-state versus six-state cyclic example;
7. the eventual arithmetic form of every nonempty exact-return language;
8. the phasewise clocked thresholds and all-residue occupation bounds;
9. the strict-side theorem for arbitrary compact component groups;
10. the exact zero-error clocked finite-quotient criterion;
11. the nonattained zero-radius boundary on the 2-adic integers;
12. the linear exact-width and all-width occupation law for that 2-adic experiment;
13. the positive-error unit-amplitude planar matching law; and
14. the effective stationary minimization procedure for rational orthogonal polynomial data.

The top-four rejection is therefore **not** a correctness dismissal. It rests on the gap between a strong specialized realization theorem and a theorem of sufficiently broad mathematical consequence for the four leading general journals.

The central purification argument is built on classical compact-semigroup and nonnegative-matrix-group structure. The manuscript's application to uniform numerical error and its coupling to the physical compact-group coordinate are useful and appear nontrivial, but the independent priority boundary remains unresolved. The clocked theory still requires group reversibility and an exact synchronization language; the general positive-error boundary for compact groups with infinitely many components remains open; the sharp quantitative laws cover two highly structured families; and the resource model continues to make arbitrary real tables, exact arithmetic, and exact sampling free.

**Disposition outside the four leading general journals:** the manuscript is now a credible and potentially strong specialist paper in positive realization, probabilistic or weighted automata, compact semigroup dynamics, control, or theoretical computer science. It deserves conventional external priority review against the compact stochastic-semigroup and numerical-automata literature. Subject to that audit and several clarifications below, I would not require another wholesale architectural rewrite before specialist submission.

---

## 1. Scope, genealogy, and material reviewed

At the final branch survey used for this report, Revision 55 was the latest referee-ready General Theta Foundations I revision. The work branch and referee-ready branch both pointed to

```text
00a0864003790aa3efcdc7f88358b6fa27ffe868.
```

No Revision 56 branch and no pre-existing Revision 55 review branch were present at that survey.

I reviewed the complete active article and the repository records required to assess correctness, scope, provenance, reproducibility, literature positioning, and relation to the wider paper pipeline. In particular, I examined:

- `papers/GTF-I-v55-stochastic-purification/main.tex`;
- `sections/00-introduction.tex`;
- `sections/09-purification.tex`;
- `sections/01-classification.tex`;
- `sections/02-localization.tex`;
- `sections/10-return-phases.tex`;
- `sections/11-profinite-boundary.tex`;
- `sections/03-consequences.tex`;
- `sections/04-width-laws.tex`;
- `sections/05-algebraic-circle.tex`;
- `sections/06-effective.tex`;
- `sections/07-comparison.tex`;
- `sections/08-bibliography.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `README.md`;
- `PROOF_STATUS.json`;
- `HISTORY_AND_PIPELINE_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `FROZEN_R36_REPORT.md`;
- `PRESERVATION_MANIFEST.json`;
- the new and inherited exact-check programs;
- `evidence/BUILD_RECEIPT.json` and the source identity records;
- the isolated native rebuild and referee package;
- the branch-specific qualification workflow;
- the complete r36 report;
- the Revision 54 radius article and its source relevant to the inherited clocked theorem;
- the retained v53/v52 realization material used in the local derivation chain; and
- the frozen Round-Seventeen repository dependency ledger.

I also made a targeted external comparison with Peter Flor's 1969 paper *On groups of non-negative matrices* and the earlier stochastic-semigroup work of Štefan Schwarz. Those sources confirm that the nonnegative-idempotent and bounded stochastic-group geometry is classical. This was not an exhaustive independent priority search for the full uniform-error purification statement.

The genealogy is clean. The readable theorem source was committed at `22609df8...`, source-bound qualification was run on that exact source, and the final publication commit added derived evidence and PDFs without changing the native theorem source. The review branch created for this report has the publication head as its unique base and does not modify any previous revision, review, or unrelated manuscript branch.

A successful source-bound build is strong delivery and regression evidence. It is not independent proof verification, priority clearance, or editorial acceptance. Conversely, the recommendation below is not based on a packaging failure.

---

## 2. Executive assessment of the new mathematics

Revision 55 adds four major mathematical layers beyond Revision 54.

### 2.1 Width-preserving stationary purification

The manuscript starts from an arbitrary stationary stochastic realization on `k` labels. It forms the compact joint semigroup

```text
closure{(u_w^{-1}, T_w)} subset H x Stoch(k).
```

A minimum-rank element is powered along a simultaneous return subnet. Its stochastic component converges to a minimum-rank stochastic idempotent `E` over the physical identity. The corner

```text
(1,E) T (1,E)
```

is then a compact group whose first projection remains all of `H`.

The recurrent probability set

```text
Delta_k E = {p in Delta_k : pE=p}
```

is a simplex with exactly `rank(E)` vertices. Every stochastic element of the corner group acts by an affine automorphism of that simplex and therefore permutes its vertices.

Sandwiching each command row by `E`, expressing each initialized row `alpha_s E` in recurrent-simplex coordinates, and evaluating the old decoder on the recurrent vertices yields a permutation machine on at most `k` labels. The closed joint error inequalities give the same uniform error bound for every word, including the empty word.

This is a genuine purification theorem. It does not assume that a physically trivial word acts trivially on the original hidden register, and it does not require deterministic initialization.

### 2.2 Exact unrestricted stationary minimization

After purification, each fixed width `k` has only finitely many command-permutation tuples. For one tuple, the joint compact group

```text
L_sigma = closure{(u_w^{-1}, Pi_w)}
```

records all physical and hidden relations simultaneously. Feasibility is exactly the existence of seed distributions and legal decoders satisfying the error inequalities on every point of `L_sigma`.

The manuscript correctly concludes that the stationary minimum is attained and that randomized initialization cannot be discarded. The cyclic `Z/6Z` example realizes a least-period-six numerical sequence using a disjoint two-cycle and three-cycle with five total labels, while every deterministic component quotient requires six.

### 2.3 Phasewise clocked synchronization

The set of positive exact-return lengths is additive. If it is nonempty and has gcd `d`, finitely many return lengths already have gcd `d`, so all sufficiently large multiples of `d` are returns and no other lengths are.

The closure of all products of lengths divisible by `d` is an open normal subgroup `J`, and the reachable products at length residue `r` are dense in one coset `a^r J`. This produces a precise phase decomposition of the clocked problem.

For compact groups with finitely many connected components, each residue class has its own sharp component-radius threshold. The proof reduces every cut residue to a block machine over the `d`-letter alphabet and then applies the cofinite-return theorem. It counts all cuts, not merely the selected block endpoints.

### 2.4 Infinite component groups and a profinite boundary

For an arbitrary compact group, the component quotient `H/H^0` is profinite. Open normal subgroups approximate the identity component, so finite-quotient radii decrease to the component radius `R_0`.

A finite-dimensional Lie quotient approximates any finite continuous compact-convex interface. This transfers the strict subcritical clocked occupation theorem from the finite-component case to arbitrary compact groups.

At zero error, a separate finite-rank argument shows that bounded clocked width forces each coordinate's left-translate span to be finite-dimensional. Since the coordinates are constant on connected components, the resulting finite-dimensional representation factors through the profinite component quotient and consequently has finite image. Thus all outputs factor through one finite quotient.

The explicit 2-adic example then separates three phenomena:

```text
R_0 = 0;
every positive error has a bounded finite-quotient realization;
exact stationary and exact clocked width are unbounded.
```

Its discrete derivative produces an invertible dyadic circulant response matrix, proving linear exact width and an all-profile occupation bound.

---

## 3. Detailed correctness audit

### 3.1 The minimum-rank idempotent

The proof of Lemma `idempotent55` is essentially correct.

Choose a matrix component `T` of minimum rank in the compact joint semigroup. Stochastic powers are bounded. Hence unit-modulus eigenvalues have semisimple Jordan blocks, while all eigenvalues inside the unit disk vanish under large powers.

In the product of the monothetic compact group generated by the physical coordinate and the finitely many peripheral unit circles, one can choose a subnet of positive exponents tending simultaneously to the identity. Along that subnet, `T^n` converges to the real spectral projection `E` onto the peripheral subspace.

Because `E` is a limit of stochastic matrices, it is stochastic and nonnegative. It is idempotent. Its rank is at most the chosen minimum rank and cannot be smaller because `(1,E)` belongs to the same compact semigroup. Thus equality holds.

The argument should explicitly say that rank-minimality is taken over the compact semigroup before choosing the powering subnet, but the logic is sound.

### 3.2 The corner is a group

Every matrix `B` in `eTe` satisfies

```text
B = EBE
```

and therefore has rank at most `rank(E)`. Minimum-rank choice gives the reverse inequality. Restriction to the row space of `E` is consequently invertible.

This embeds the corner into a topological group. A compact submonoid of a topological group is a group because positive powers return to the identity and hence approximate the inverse. The inverse element remains inside the corner and remains stochastic.

Sandwiching does not change the physical coordinate, so the first projection of the corner remains surjective onto `H`.

### 3.3 The recurrent simplex

For a finite stochastic idempotent, every row is stationary. Its stationary distributions are convex combinations of the unique stationary rows on its closed communicating classes. Transient mass is zero in a stationary distribution.

The class-supported stationary rows have disjoint supports and are linearly independent. Their span equals the row space of the idempotent. Hence their number is exactly the matrix rank, and the fixed probability set is a simplex with that many vertices.

A stochastic corner-group element and its stochastic inverse induce inverse affine self-maps of this simplex, so they permute its vertices.

This is classical Markov-chain geometry and is applied correctly.

### 3.4 Closure of the error inequalities

The inverse physical coordinate in

```text
(u_w^{-1}, T_w)
```

is necessary for chronological matrix multiplication to match semigroup multiplication. The manuscript handles this correctly.

For word points, the original stationary error bound is

```text
||alpha_s T_w D_j - F_{s,j}(u_w)|| <= epsilon.
```

On a limiting joint element `(h,B)`, continuity gives

```text
||alpha_s B D_j - F_{s,j}(h^{-1})|| <= epsilon.
```

The empty word is handled by the minimum-rank idempotent `(1,E)`, while nonempty purified words are products in the corner group. Thus no unproved hidden-state group relation is inserted.

### 3.5 Construction of the purified machine

Let the recurrent-simplex vertices be `nu_i`. The command corner matrices permute these vertices. Writing

```text
alpha_s E = sum_i beta_s(i) nu_i
```

produces legal randomized initialization. The new decoder values

```text
nu_i D_j
```

belong to the compact convex output set.

The output of the vertex-permutation machine equals the output of the sandwiched corner product against the old decoder. The closed error inequality therefore proves the same error bound.

A useful editorial improvement would be to display the intertwining identity

```text
V B_a = Pi_a V
```

for the matrix `V` of recurrent vertices. This would make the row/column convention completely transparent, but no mathematical gap results from its omission.

### 3.6 Exact stationary minimum

For fixed `k`, there are finitely many permutation tuples. The remaining seed and decoder variables lie in compact products of simplexes and output sets. The worst error is a continuous supremum over the compact joint group.

Hence the optimum at fixed width is attained, and the first feasible width is the unrestricted stationary minimum.

This is an exact structural characterization, although not a closed-form formula and not an efficient algorithm in general.

### 3.7 The finite observable quotient criterion

For a purified permutation machine, define

```text
U = {h in H : (h,I) belongs to L_sigma}.
```

Conjugation inside the joint group makes `U` normal. Fibers over a fixed hidden permutation are cosets of `U`; at most `k!` hidden permutations occur, so `U` has finite index and is open.

A single legal output vector approximates the entire target image on each inverse fiber. Normality converts inverse fibers into ordinary `U`-cosets, so `r(U)<=epsilon`.

Conversely, storing the seed and the finite coset `gU`, updating by the command action, and decoding with a constrained center gives a finite stationary permutation realization.

The index bound is only an existence bound and is not confused with the exact stationary minimum.

### 3.8 The five-versus-six-state example

The displayed six-periodic sequence is correct. A five-state permutation machine formed from a two-cycle and a three-cycle, with half the initial mass on each component, reproduces it exactly.

A permutation of at most four labels has order in `{1,2,3,4}`. Every numerical sequence generated by repeatedly applying that permutation has period dividing the permutation order. It therefore cannot have least period six.

The example successfully demonstrates that deterministic component quotients are not the unrestricted stationary minimum and that randomized initialization may save a state.

### 3.9 Return-language arithmetic

The exact-return lengths form an additive subsemigroup of the positive integers. A finite subset realizes the full gcd, and the standard numerical-semigroup argument gives all sufficiently large multiples.

The phase subgroup `J` is the compact group closure of all length-`d` block products. All command letters occupy the same coset of `J`; `J` is normal; and the quotient is finite cyclic of order dividing `d`.

The closure of products at residue `r` is the coset `a^rJ`. The quotient order can be strictly smaller than `d`, as the manuscript correctly notes.

### 3.10 Phasewise thresholds

For a fixed horizon residue, every reachable physical product lies in one phase coset. Component centers give the phasewise upper realization.

For the converse, the manuscript treats each cut residue separately. A fixed prefix and suffix align that residue with a block machine over `J`. The block target has the same connected-component image as the selected original component.

The exact-return language for the block alphabet is cofinite in block length, so the inherited radius theorem applies. Prefix and suffix losses are uniformly bounded, and summing over all residues counts every positive cut.

This closes a genuine gap left by merely treating block endpoints of one residue.

### 3.11 Strict-side arbitrary-component theorem

Open normal subgroups of the profinite quotient approximate the identity component. Uniform continuity shows that their coset radii converge down to `R_0`.

Peter–Weyl approximation produces a finite-dimensional compact Lie quotient and a legal output approximation. Projection back into the compact convex output set is continuous and can be made uniformly accurate.

If an original component radius is strictly above the error, the approximation retains a strict margin. A machine for the original target is then a machine for the approximating target at slightly larger error, so the finite-component occupation theorem applies to the same registers.

The proof correctly avoids claiming density of executable products inside a non-open identity component.

### 3.12 Exact zero-error clocked boundary

Assume a uniform exact width bound `k`. Cofinite exact returns allow any finite collection of executable prefixes and suffixes to be padded to common lengths without changing their physical products.

At the common cut, the matrix

```text
(f(y_l x_i))
```

factors through at most `k` hidden labels and therefore has rank at most `k`.

Density and continuity extend this rank bound to arbitrary group elements. Consequently, the left-translate span of each real output coordinate has dimension at most `k`.

The finite sum of these translate spaces gives a finite-dimensional continuous representation of `H`. Zero component radius makes `H^0` act trivially. The resulting representation of the profinite quotient has finite image, so its kernel is open normal and all interfaces factor through one finite quotient.

This is a clean exact-boundary theorem and does not rely on the stationary purification result alone.

### 3.13 The 2-adic example

The ternary-weight digit map

```text
f(x) = sum_n 2 x_n / 3^(n+1)
```

is continuous and injective on the 2-adic integers. Truncation after `m` digits factors through `Z/2^m Z` with error at most `3^{-m}`. Thus every positive tolerance has a finite quotient realization, while exact finite quotient realization is impossible.

For nonnegative integers, the increment difference is

```text
b(z) = (5/3) 3^{-v_2(z+1)} - 1.
```

On dyadic blocks, the resulting response matrix becomes a circulant after a row permutation. Its zero Fourier eigenvalue is positive, and every nonzero eigenvalue is negative because the final dyadic divisibility term is always present. Thus the matrix is invertible.

At any cut, prefixes with `i` increments and paired suffixes with `j+1` and `j` increments factor this matrix through the actual register. Hence the register width is at least the dyadic block size.

Choosing a middle cut yields a linear peak lower bound. The same argument confines every cut of width at most `k` to an `O(k)` neighborhood of one endpoint, proving the all-profile occupation estimate. Counting increments gives the linear upper bound.

The theorem is sharp for the stated interface.

### 3.14 Unit amplitude at positive error

At `rho=1`, the inherited harmonic lower bound remains valid for every fixed positive subcritical error.

For the upper bound, the paper reduces amplitude to `rho'=1-eta`, constructs an exact polygon realization for the smaller-amplitude target, and uses the amplitude discrepancy as a total-variation error budget. Choosing `eta<2 epsilon` gives the claimed upper bound.

This does not improperly infer the exact unit-amplitude endpoint by continuity.

### 3.15 Effective stationary minimization

For rational orthogonal commands and rational polynomial categorical outputs, the augmented generators

```text
diag(u_a^{-1}, Pi_a)
```

are rational orthogonal matrices. Existing group-closure algorithms produce the joint compact group for each permutation tuple.

The seed and decoder variables are algebraic-simplex variables. Uniform error on the joint closure is an existential–universal real semialgebraic formula because physical inversion is transposition. Real quantifier elimination decides it and supplies algebraic witnesses.

The finite component-radius bound gives a terminating width range. The method is therefore computable, although factorial enumeration and real-algebraic elimination make no claim of practical complexity.

---

## 4. Why the paper still falls short of the four-journal standard

### 4.1 The main structural mechanism is close to classical compact-semigroup theory

The minimum-rank idempotent, compact group corner, recurrent-class simplex, and permutation action are classical features of finite stochastic semigroups and nonnegative matrix groups. Flor's 1969 paper and Schwarz's earlier work are directly relevant.

The manuscript's joint physical/stochastic closure and error-preserving application are useful. However, the paper does not yet establish by independent comparison that its central purification theorem is sufficiently far from the classical kernel/minimal-ideal theory to support a four-journal novelty claim.

At minimum, the literature discussion should compare the precise theorem—not only ingredients—with:

- compact stochastic matrix groups;
- kernels and minimum ideals of compact semigroups;
- Rees-type structure of completely simple semigroups;
- probabilistic and weighted automata minimization;
- Markov representations of group actions; and
- positive realization under uniform approximation.

### 4.2 Stationary purification does not solve the general clocked problem

The stationary minimum `M_epsilon` is now well characterized. The horizon-specific clocked width `W_{N,epsilon}` remains a different invariant.

The manuscript explicitly records that stationary and clocked widths are not identified. The single irrational-letter example shows that they can differ radically without synchronization.

Even with cofinite returns and infinitely many components, the unrestricted positive-error clocked boundary at `epsilon=R_0` is not classified. The paper settles the strict sides and the zero boundary, but the positive boundary remains a natural missing piece adjacent to its headline theorem.

### 4.3 The physical dynamics remain reversible

All principal theorems concern compact group dynamics. The scalar contraction example shows why arbitrary irreversible semigroups behave differently, but no replacement invariant is developed.

A general theory of compact semigroup experiments, switched positive systems, or mixed reversible/dissipative dynamics would be substantially broader. The current paper supplies counterexamples to naive extension rather than a classification in that setting.

### 4.4 Synchronization remains exact and algebraic

The phase theorem treats every nonempty exact-return language, which is a genuine improvement. Nevertheless, it requires at least one physically exact return.

Many natural controlled systems have only approximate returns, a regular return language without exact identity, or synchronization through an observable quotient rather than the physical group. The paper does not identify the sharp condition in such cases.

### 4.5 Quantitative breadth is still limited

The matched polynomial law is for badly approximable planar rotation tuples. The linear law is for one specially constructed 2-adic digit interface.

There is no matched theory for:

- a general connected compact Lie group;
- nonabelian representations;
- broad profinite interfaces;
- generic algebraic rotations;
- higher-dimensional categorical or joint outputs; or
- the exact unit-amplitude planar endpoint.

Two sharp families do not yet constitute a general quantitative classification.

### 4.6 The primary resource model remains extremely permissive

The model charges only persistent label count. It leaves free:

- the horizon and external clock;
- redesign at every horizon;
- arbitrary real transition and decoder tables;
- table construction and lookup;
- exact real arithmetic;
- exact sampling; and
- potentially enormous nonuniform advice.

The lower bounds are stronger for surviving this permissive model. But the connection to ordinary automaton size, uniform memory, random-bit complexity, finite precision, or implementable positive systems remains indirect.

### 4.7 Effectivity is not complexity theory

The effective results establish termination through matrix-group closure and real quantifier elimination. They do not give a meaningful total complexity bound for deciding the stationary minimum or producing occupation constants.

The localizer degree and executable contraction law are found by terminating searches with no useful a priori bounds. The fixed-horizon problem has exponentially many word constraints before algebraic compression.

A genuine complexity classification would materially strengthen the paper.

### 4.8 The terminal interface remains finite-dimensional and offline

The output is selected only after the command word and belongs to a finite-dimensional compact convex set. The article does not treat:

- online observations;
- output processes;
- adaptive queries;
- path-law approximation;
- feedback depending on sampled outputs; or
- infinite-dimensional output spaces.

These are not minor variants of the current terminal-decoder model.

### 4.9 The repository pipeline is logically independent

The local realization theory is self-contained and should be judged on its own merits. It neither uses nor proves the model-specific analytic gates in the Round-Seventeen A/B/C/D program.

The number of repository revisions, cumulative preserved pages, and success of unrelated derivations do not increase the journal significance of this standalone result.

---

## 5. Relation to the repository paper pipeline

The legitimate local ancestry of the present article is:

```text
common stochastic-row compatibility
  -> reachable positive sections and exact all-width rigidity
  -> moving conditional-feature contraction
  -> representative-function localization
  -> compact-convex component radius and clocked occupation.
```

Revision 55 adds the independent branches:

```text
joint physical/stochastic compact semigroup
  -> minimum-rank idempotent
  -> recurrent simplex
  -> stationary purification
  -> stationary minimum and finite observable quotients;

exact-return arithmetic
  -> phase subgroup
  -> phasewise thresholds and occupation;

finite Lie quotient approximation
  -> arbitrary-component strict-side clocked obstruction;

cofinite padding + finite response rank
  -> exact profinite clocked boundary;

2-adic digit interface + circulant spectrum
  -> linear exact width and endpoint occupation.
```

These are genuine local advances.

They do **not** supply any of the following repository gates:

```text
A2 raw vector-return-roof Fourier/density local limit
A3 entropy-controlled stopped LDP
A4 one global past kernel and forced memory
B1 direct canonical coefficient and shell conditioning
B2 joint large deviations
B3 process CLT and Mosco tangent
B4 nonlinear Nisio resolvent and graph-core recovery
C1 model-derived filtering and QMD/LAN
C2 strict/form response under changing filtrations
D1 labelled posterior contraction
```

Accordingly, this report assigns no credit for:

```text
historical A2 replacement;
B4 aggregate closure;
C2 aggregate closure;
eleven-paper aggregate closure;
whole Theta program completion.
```

The manuscript's `PROOF_STATUS.json` correctly keeps those flags false.

---

## 6. Publication and reproducibility audit

The source-bound workflow was

```text
36313303021
```

and completed successfully.

The workflow:

1. committed readable native theorem source before qualification;
2. installed fixed Python and typesetting dependencies;
3. ran the new and inherited exact checks;
4. built the manuscript and all retained documents;
5. rebuilt the native archive in isolation;
6. compared every page's extracted text and raster;
7. published derived PDFs and evidence without changing native theorem source; and
8. preserved the actual qualification outputs.

The build receipt records:

```text
main article:                     32 pages
radius predecessor:               20 pages
scalar predecessor:               14 pages
companion notes:                   4 pages
complete supplement:              68 pages
native source files:              114
new exact finite assertions:      13,598
new named negative controls:       19
new negative-control executions:   38
normal/optimized agreement:       true
isolated source hashes equal:     true
isolated text equality:           true
isolated raster equality:         true
```

The final publication commit has the validated native-source commit as its parent and adds the qualified derived package.

This is unusually strong provenance and reproducibility discipline. It does not replace mathematical proof review or external priority assessment.

---

## 7. Major requests before any further high-level submission

### 7.1 Complete the priority comparison for purification

The paper should directly compare the exact width/error-preserving statement with the kernel and group structure of compact stochastic semigroups, not only cite Flor as an ingredient.

The comparison should identify precisely which of the following are classical and which are added here:

- existence of a minimum-rank idempotent;
- the stochastic group corner;
- the recurrent simplex;
- permutation action on recurrent classes;
- preservation of the external compact-group coordinate;
- preservation of all seed/query uniform error balls;
- preservation of the original width; and
- necessity of randomized initialization.

### 7.2 Separate the stationary and clocked theorem map more aggressively

The introduction is improved, but the article still contains many adjacent notions:

```text
stationary minimum M_epsilon;
clocked minimum W_{N,epsilon};
component radius;
open-normal quotient radius;
phase radius;
strict profinite radius R_0;
clocked zero boundary;
stationary positive boundary.
```

A one-page theorem map should state the assumptions and exact logical relations among them.

### 7.3 State the positive profinite clocked boundary as a primary open problem

At `epsilon=R_0>0`, stationary attainment has an exact open-normal-subgroup criterion. Clocked attainment is not identified.

This is the most immediate structural problem left by the paper and should be highlighted more prominently.

### 7.4 Explain whether purification extends beyond finite labels or compact outputs

The proof is intrinsically finite-dimensional on the hidden side. The manuscript should state explicitly which steps fail for countably infinite labels, compact convex state spaces, or operator-valued stochastic kernels.

### 7.5 Provide a quantitative or complexity theorem beyond termination

A nontrivial upper or lower complexity bound for the rational stationary-minimization problem would substantially improve the paper. Merely repeating that quantifier elimination terminates is not enough for a broad complexity claim.

### 7.6 Clarify the natural uniform resource counterpart

The paper should formulate, even if not solve, a companion invariant that charges finite descriptions, precision, and random bits. This would help readers understand exactly what the nonuniform width theorem does and does not imply.

### 7.7 Add at least one nonabelian quantitative application

The current sharp rates are abelian. A meaningful compact nonabelian example with matching or nearly matching width growth would materially strengthen the paper's breadth.

---

## 8. Local comments

1. In Lemma `idempotent55`, state explicitly that the minimum matrix rank is attained because the rank values are integers and a nonempty rank stratum occurs in the compact semigroup.
2. When taking the simultaneous powering subnet, name the compact monothetic group containing the physical coordinate and peripheral phases.
3. Record explicitly that power boundedness rules out nontrivial Jordan blocks on the unit circle.
4. In the corner-group proof, display why restriction to `row(E)` is injective for matrices satisfying `B=EBE`.
5. In Lemma `simplex55`, it would be cleaner to cite or prove directly that every row of a stochastic idempotent is stationary and is a convex combination of closed-class stationary rows.
6. Display the matrix intertwining identity between recurrent vertices and the new permutation matrices.
7. Clarify that the permutation machine may have fewer than `k` labels and that padding is used only when comparing a fixed proposed width.
8. In Theorem `stationaryminimum55`, distinguish the closure topology on `H x S_k` from the finite topology on the permutation factor.
9. In Theorem `finitequotient55`, write the one-line proof that inverse fibers are ordinary `U`-cosets because `U` is normal.
10. The `k!` index bound is very coarse; state whether the actual quotient is the image of the joint group in `S_k` modulo the physical-identity kernel.
11. In Proposition `C655`, state the convention for the generator direction on the two- and three-cycles, although the symmetric numerical sequence makes the present computation unambiguous.
12. In Lemma `returnperiod55`, distinguish `N={1,2,...}` from a convention containing zero; the empty word is excluded from the return language there.
13. In Lemma `phasegroup55`, display one explicit executable concatenation realizing `a x a^{d-1}` under the reversed physical-product convention.
14. State whether `epsilon_r` is repeated when the order of `H/J` is a proper divisor of `d`.
15. In the phasewise occupation proof, list the uniform bound for cuts lost in the fixed prefix and suffix for each residue.
16. The notation `d` is used both for return period and elsewhere for contraction defects; the current warning helps, but different symbols would reduce cognitive load.
17. In Lemma `infradius55`, state explicitly that every open subgroup contains `H^0` because its finite discrete quotient receives a connected image.
18. In Lemma `Lieapprox55`, specify the norm-equivalence constants used when projecting in an auxiliary Euclidean norm but measuring error in the original norm.
19. In Theorem `zero55`, name the left-translate convention and the orientation of the matrix `f(y_lx_i)`.
20. Give a short standalone lemma that bounded ranks of all finite evaluation matrices imply finite translate-space dimension.
21. In the profinite representation step, cite the closed-subgroup theorem or no-small-subgroups fact used to conclude that a compact totally disconnected matrix group is finite.
22. In Proposition `adic55`, write the exact tail sum giving the `3^{-m}` truncation error.
23. In Theorem `adiclinear55`, state the Fourier-transform sign convention. Invertibility is convention-independent, but the displayed eigenvalue formulas are easier to verify with it.
24. Explain why the row permutation `i -> -i-1` turns the Hankel matrix into the stated circulant.
25. The terminal cut is outside the rank argument; the occupation proof correctly adds it separately. State this in the theorem proof rather than only implicitly.
26. In Corollary `unitnoise55`, remind the reader that binary total variation is one half of mean error.
27. In the effective stationary theorem, distinguish equations describing the joint closure from equations merely vanishing on the generated subgroup.
28. The phrase "at most `(k!)^{|A|}` augmented closures" counts permutation tuples before quotienting simultaneous conjugacy. Mention that this is a deliberately crude bound.
29. The literature section should cite the exact theorem numbers from Flor only after independently checking that their hypotheses match the corner group used here.
30. The main comparison table should include a row for classical compact stochastic-semigroup kernels and identify the additional external-error quantifier.
31. The abstract is dense. Consider separating the stationary purification theorem, clocked synchronization theorem, and quantitative examples into three sentences with their different assumptions.
32. The paper should avoid allowing the term "purification" to suggest deterministic initialization; the present text is careful, and that warning should appear in the abstract or first theorem statement.

---

## 9. Final disposition

Revision 55 is mathematically serious. It contains a plausible width-preserving stationary purification theorem, a useful exact stationary-minimum formulation, a complete phase treatment of exact returns, an exact profinite zero-boundary theorem, and a sharp 2-adic width example. These are genuine improvements over r36.

Nevertheless, the paper does not yet meet the breadth, independent priority clarity, and cross-area impact expected by Annals, Inventiones, JAMS, or Acta. Its central algebraic mechanism is close to classical compact stochastic-semigroup theory; its clocked classification still depends on reversible group structure and exact synchronization; its general positive profinite boundary remains open; and its quantitative and effective theories are confined to structured cases.

My recommendation is therefore:

```text
Reject at the four leading general mathematics journals.

Encourage submission to a strong specialist venue after:
- an independent priority audit of the purification theorem;
- a sharper stationary/clocked theorem map;
- explicit presentation of the unresolved positive profinite boundary;
- final clarification of resource and complexity scope; and
- the local proof-exposition revisions listed above.
```

No repository-wide analytic closure should be inferred from this report or from the success of the manuscript's reproducibility workflow.
