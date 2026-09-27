# Referee Report — General Theta Foundations I, Revision 53

**Manuscript:** *General Theta Foundations I: Sharp Noise Thresholds for Stochastic Realizations of Compact Group Experiments*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v53-component-oscillation-2026-09-27`
- `revision/general-theta-foundations-i-v53-referee-ready-2026-09-27`

**Reviewed publication head:** `825d1d302cfca6c6b5abe8497bddb4df8680d810`  
**Validated native-source commit:** `cc598ea21ac7ffa0a4701b850a05efa1cbb64e71`  
**Workflow trigger:** `5380aadd750854751efb8b58e4a930df6debbc9a`  
**Source predecessor:** Revision 52 publication `7641901c2ef957542aa50d9918f272ac7a72ca1c`  
**Controlling prior report:** r34, `4b1eb39eacdb741354e8c4faaedb1c3aabb3a14c`  
**Review branch:** `review/general-theta-foundations-i-v53-component-oscillation-harsh-top4-r35-2026-09-27`  
**Date:** 27 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

**Mathematical disposition:** Revision 53 is a genuine and substantial advance over Revision 52. It replaces the previous sufficient small-noise finite-group rigidity statement by a sharp classification for every finite continuous binary-mean interface on a compact matrix-group closure. I did not find a fatal counterexample to the component-oscillation threshold, its attainment at equality, the arbitrary-width narrow-cut occupation theorem, the observable-quotient criterion, the compact-similarity extension, or the explicit full-subcritical algebraic-circle bounds.

The new principal theorem is clean:

```text
uniformly bounded horizon-dependent stochastic width
        if and only if
error >= one quarter of the largest componentwise mean oscillation
        if and only if
one stationary finite permutation realization attains that error.
```

Below the threshold, every fixed width has a horizon-independent occupation budget even when all intervening registers are unrestricted. This is a real class-wide statement with the correct all-machine quantifier. It is not merely a verification procedure for one proposed machine, a rank-tight special case, or a compactness corollary with an unspecified upper construction.

The top-four rejection is therefore **not** a correctness dismissal and is not a repetition of r34. It rests on significance, scope, effectiveness, and priority positioning.

1. The theorem remains tied to compact reversible group dynamics with an executable identity command. Noninvertible compact semigroups, general switched positive systems, and interfaces without a padding mechanism are outside the classification.
2. The primary width model remains highly permissive: the horizon, clock, arbitrary real row tables, their construction and lookup, exact arithmetic, and exact atomic sampling are free.
3. The theorem classifies the bounded/unbounded transition but does not determine the subcritical growth of `W_{N,epsilon}`. Even for one algebraic irrational rotation the new explicit lower bound is logarithmic and is not matched.
4. The output interface consists of finitely many separately selectable binary means. Simultaneous categorical laws, joint query semantics, and general stochastic outputs are not classified.
5. The general theorem is non-effective for arbitrary real compact-group data. Its extrema, polynomial approximation, and executable word law are existence objects rather than outputs of a finitely encoded algorithm.
6. The proof uses classical compact-group closure, Haar averaging, finite-dimensional tensor representations, Stone–Weierstrass approximation, polynomial localization, and a midpoint construction. Their combination is effective and elegant, but the article has not yet demonstrated sufficiently broad consequences to meet the four leading general-journal standard.
7. The targeted literature audit is useful but too narrow for a definitive priority assessment. The closest real-valued probabilistic-automata, weighted-automata, almost-periodic-function, compact-semigroup, and quantitative group-language literature is not yet mapped theorem by theorem.
8. The result remains independent of the repository’s A/B/C/D analytic dependency graph. Repository accumulation and the “Foundations” series title do not supply general-journal significance.

**Disposition outside the four leading general journals:** major revision followed by submission as a focused specialist article in probabilistic/weighted automata, positive realization, compact-group dynamics, or theoretical computer science. The fourteen-page main paper is now coherent enough to be assessed independently. If the priority comparison survives a conventional external audit, the component-oscillation theorem should be publishable in an appropriate strong venue.

---

## 1. Scope, genealogy, and materials reviewed

At the final branch survey used for this report, Revision 53 was the latest referee-ready `General Theta Foundations I` revision. Both reviewed revision branches pointed to

```text
825d1d302cfca6c6b5abe8497bddb4df8680d810.
```

No Revision 54 branch and no pre-existing Revision 53 review branch were present at that survey.

I reviewed the complete focused article and the repository records needed to assess its correctness, scope, provenance, reproducibility, literature positioning, and relation to the larger paper pipeline. In particular, I examined:

- `papers/GTF-I-v53-component-oscillation/main.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `README.md`;
- `PROOF_STATUS.json`;
- `HISTORY_AND_PIPELINE_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `FROZEN_R34_REPORT.md`;
- `FROZEN_PIPELINE_LEDGER.md`;
- `supplement-notes.tex`;
- the complete retained Revision 52 source inventory under `retained-v52/`;
- `PRESERVATION_MANIFEST.json`;
- the new and inherited exact-check programs;
- `evidence/BUILD_RECEIPT.json`;
- `evidence/SOURCE_HASHES.json`;
- the isolated rebuild records and referee package;
- the branch-specific workflow;
- the complete r34 referee report;
- the Revision 52 source relevant to arbitrary-width positive-error rigidity; and
- the repository-level Round-Seventeen dependency ledger.

The new main article is independently complete. The sixty-eight-page predecessor theory is now a separately buildable supplement rather than an implicit forward dependency of the principal theorem. This is a genuine editorial improvement over the accretive organization criticized in earlier reports.

The genealogy is cleanly recorded. The workflow was triggered at `5380aadd...`, materialized and committed the readable theorem source at `cc598ea2...`, qualified that exact source, and then added derived publication artifacts at `825d1d30...`. The work and referee-ready branches were atomically published at the same final commit. Earlier revision, review, and unrelated manuscript branches remain unchanged.

A source-bound successful build is useful reproducibility evidence. It is not independent proof verification or priority clearance. Conversely, the recommendation below is not based on a packaging defect.

---

## 2. Executive assessment of what Revision 53 accomplishes

Revision 53 materially answers nearly every central mathematical objection in r34.

### 2.1 A sharp component-oscillation threshold

Let `H` be the compact closure of the group generated by the command matrices, `K=H^0`, and `C=H/K`. For each finite seed-query interface function `f_{s,j}:H -> [-1,1]`, define

```text
m_{s,j,c} = min_{h in c} f_{s,j}(h),
M_{s,j,c} = max_{h in c} f_{s,j}(h),

epsilon_c = (1/4) max_{s,j,c} (M_{s,j,c}-m_{s,j,c}).
```

The manuscript proves, including equality, that

```text
sup_N W_{N,epsilon} < infinity
        iff
one stationary finite permutation realization works at every horizon
        iff
epsilon >= epsilon_c.
```

The factor `1/4` is correct: the best constant mean approximation on one component has mean error one half of the oscillation, and binary total variation is one half of mean error.

The boundary is attained by storing the seed and the component of the current group product, and decoding with the midpoint of the component range. This is an actual stationary construction, not an unattained compactness infimum.

### 2.2 A lower bound against the full nonuniform model

The converse permits:

- different state sets at every cut;
- different rows at every epoch;
- redesign for every horizon;
- arbitrary real stochastic coefficients;
- arbitrary intermediate widths;
- zero-probability and unreachable labels;
- no state-mass lower bound; and
- no observable-coordinate assignment to arbitrary hidden states.

For each fixed terminal width `k`, the article constructs an executable finite word distribution in the identity component which contracts the norm of every conditional centroid in a finite-dimensional moving representation. Tensor-polynomial features and nonnegative localization at two output extremes then force a nonzero terminal conditional moment whenever the permitted mean error is below one half of the relevant oscillation.

Repeated contraction gives a bound on the number of cuts of width at most `k`, while all other cuts may be arbitrarily wide. This is stronger than a uniform-peak obstruction and correctly handles separated bottlenecks.

### 2.3 Partial and nonlinear interfaces

The principal theorem no longer requires signed coordinate seeds, spanning families, or all coordinate queries. The interface can be any finite collection of continuous binary-mean functions on `H`.

For linear interfaces, the observable-quotient theorem identifies the exact zero-error obstruction: uniformly bounded exact width is equivalent to finiteness of the group image on the reachable space modulo the invisible subspace.

The paper also treats:

- invisible fixed directions in an otherwise infinite group action;
- nonlinear continuous readouts;
- measure-once unitary acceptance probabilities after realification; and
- uniformly bounded real matrix groups after conjugation to an invariant Euclidean metric.

These are genuine scope improvements over Revision 52.

### 2.4 A sharp planar threshold

For an alphabet containing an irrational planar rotation, signed coordinate seeds, and coordinate queries, the connected component is `SO(2)` and each visible coordinate mean ranges over `[-rho,rho]`. Therefore

```text
sup_N W_{N,epsilon} < infinity
        iff
epsilon >= rho/2.
```

At equality, the fair decoder with one command label attains the bound. Below it, every fixed width has a finite occupation budget. This closes the entire positive-error interval left open in Revision 52.

### 2.5 Explicit arithmetic bounds throughout the subcritical interval

For an algebraic unit-circle eigenvalue which is not a root of unity, the manuscript combines:

- explicit harmonic localization;
- separated powers;
- a nonzero integer resultant; and
- the same endpoint contraction mechanism

to obtain finite-horizon and occupation inequalities for every `epsilon<rho/2`.

The resulting logarithmic width lower bound is coarse but explicit. The rational Gaussian-integer case is a sharper specialization, and the displayed degree-four nonrational example is correctly checked.

### 2.6 A genuinely focused article

The main article is fourteen pages and has one central theorem. The four-page companion note records local refinements, while the complete prior theory is preserved in a separate supplement. The main theorem does not rely on an omitted argument hidden in the supplement.

This resolves the most serious presentation objection in r34.

---

## 3. Detailed correctness audit

### 3.1 Compact-group structure and positive words

The use of the identity component is appropriate. A closed subgroup of `O(D)` is a compact Lie group, so its identity component `K` is open and normal and the component group `C=H/K` is finite.

The positive-word semigroup is dense in `H`. For one orthogonal generator `U`, recurrent powers approximate the identity, so positive powers approximate `U^{-1}`. The closed positive semigroup therefore contains the full generated group and hence its closure.

Intersecting with the open subgroup `K` gives density of executable positive words in `K`. The explicit identity letter then pads any finite collection to one common positive length without changing the physical matrix product.

This is correct. One small expository repair would help: compactness of the powers should explicitly be used to obtain a near-return with exponent difference at least two. For an infinite orbit, take three powers in one sufficiently small cell; for a finite orbit, take a sufficiently large multiple of the order. The intended assertion is standard and the omission is local.

### 3.2 The finite executable quantization gap

For a finite-dimensional orthogonal representation of connected `K` with no nonzero fixed vector, the manuscript defines

```text
g = min_{u,v_1,...,v_k}
      integral_K [1-max_j <v_j,R(h)u>] d mu(h).
```

The parameter space is compact and the integrand is nonnegative. If the minimum were zero, full support of Haar measure would force every orbit point `R(h)u` to coincide with one of finitely many unit centers. The orbit is connected, hence a connected finite set, hence a singleton. This contradicts the absence of fixed vectors.

Thus `g>0`. Uniform operator-norm approximation of Haar measure by finitely many executable atoms preserves a positive fraction of this defect. The estimate is uniform over the starting direction and every choice of `k` terminal directions.

This part is sound and does not assume a spectral gap for any preassigned random walk.

### 3.3 Conditional-centroid contraction

Let `Z` be the moving feature and `S` the current hidden state. An independent external block word is sampled, and the machine applies its actual block kernel. Conditional on the current state and the external block, that kernel is independent of the earlier physical history.

The identity

```text
P(S'=j) E[R(U_w)Z | S'=j]
  = sum_s P(S=s) E_w T_w(s,j) R(U_w) E[Z|S=s]
```

is therefore valid. Pairing each terminal centroid with its unit direction, relaxing a stochastic average to a maximum over at most `k` directions, and applying the quantization gap yields the contraction.

The proof correctly allows zero-probability states and places no restriction on intermediate register sizes. Identity gaps cannot increase the conditional-centroid norm by conditional Jensen.

### 3.4 Tensor-polynomial features

The direct sum

```text
V_l = direct sum_{m=0}^l End((R^D)^{tensor m})
```

contains a coefficient representation for every polynomial in the matrix entries of degree at most `l`. Left multiplication by `g^{tensor m}` is orthogonal in Frobenius norm and sends the feature of `h` to the feature of `gh`.

Haar averaging is the orthogonal projection onto the fixed subspace. Removing that projection gives a moving representation with no fixed vector. A polynomial which is nonconstant on `K` has a nonzero moving coefficient and the starting moving feature at the identity is nonzero.

The conditional calibration identities then follow directly from splitting a polynomial coefficient into fixed and moving parts and applying Cauchy–Schwarz.

The coefficient vector is not unique because of polynomial identities on the group. The article already says that a choice is fixed whenever a norm is used. It would be useful to repeat this immediately before defining the constant `L`, because the numerical value of `L` depends on that choice even though the theorem does not.

### 3.5 Localization at two extreme values

For a nonconstant polynomial `F` on `K`, the normalized powers of `F-m` and `M-F` are nonnegative polynomial weights of Haar mean one. As the power grows, their weighted means converge to the maximum and minimum of `F`.

Therefore, whenever

```text
M-m > 2 delta,
```

one can choose two weights whose weighted means differ by more than `2 delta`.

The proof using full support of Haar measure and a ratio of high powers is correct even when the extremal sets themselves have Haar measure zero.

### 3.6 The residual conditional moment

Wordwise approximation gives

```text
|E[D|word]-F(h)| <= delta.
```

Multiplying by a nonnegative polynomial weight and averaging is legitimate. The conditional polynomial estimates compare both `E[pD]` and `E[pF]` with their Haar counterparts up to a constant times the moving conditional moment `Q`.

Using the same scalar `E D` for the two localized weights and subtracting the resulting inequalities yields

```text
Q >= Delta/L.
```

The direction and constants are correct. No claim of total-variation convergence of the hidden physical distribution is made.

### 3.7 Stone–Weierstrass reduction for a continuous interface

After choosing one component with oscillation larger than the allowed mean-error budget, the paper fixes an executable prefix whose product lies in that component. Subsequent test blocks lie in `K`, so the remaining observable is a continuous function on `K` with the same oscillation.

Matrix-coordinate polynomials separate points of `K` and contain constants. Real Stone–Weierstrass therefore gives a polynomial approximation. The manuscript chooses the approximation error with enough slack to preserve the strict oscillation inequality.

The conversion from target error to polynomial error is correctly charged once:

```text
delta = 2 epsilon + approximation_error.
```

### 3.8 Repeated contraction and the occupation bound

The test word starts with the fixed component prefix. At that point the physical feature is deterministic, so its conditional-centroid norm is the full starting norm regardless of the hidden-state distribution.

Independent executable blocks are placed immediately before greedily selected narrow cuts. Identity words fill every gap. The blocks do not overlap, and every complete test word has the prescribed horizon.

At each selected endpoint of width at most `k`, the conditional feature contracts by the same factor. At the terminal decoder, the residual lemma forces a positive lower bound. This gives

```text
J chi <= log A.
```

The greedy spacing count then converts the bound on selected block endpoints into a bound on all narrow cuts.

The quantifiers are correct: the test law may depend on the advertised width profile and on `k`, but not on the machine’s private state. Correctness is required for every deterministic word, so testing under this external law is legitimate.

The displayed `L_k` need not be an integer. Since it bounds an integer count, the theorem should either use its ceiling or call it a real upper constant. This is editorial, not substantive.

### 3.9 Divergence of the minimum peak

A horizon-`N+1` realization can be truncated to horizon `N` by appending the executable identity command and absorbing its stochastic row into the decoder. The target product is unchanged and the new decoder remains in `[-1,1]`.

Thus `W_{N,epsilon}` is nondecreasing. Since every fixed peak violates the repeated-block inequality for sufficiently large `N`, the minimum width diverges.

### 3.10 The stationary boundary construction

The state `(s,c)` stores the seed and the current component. Each command acts by left multiplication in the finite component group, hence by a permutation.

For query `j`, the midpoint

```text
(M_{s,j,c}+m_{s,j,c})/2
```

has worst mean error one half of the component oscillation. Binary total variation divides this by two. The construction attains `epsilon_c` exactly.

This proves a sharp boundary, not merely a sufficient upper estimate.

The component multiplication convention should be stated explicitly once: after current component `c=[U_w]`, the next component is `[U_a]c`, consistent with the execution-order convention.

### 3.11 Observable quotient

The reachable space and invisible subspace are invariant. Because the action is orthogonal, the orthogonal complement of the invisible subspace inside the reachable space is also invariant.

If all interface functions are constant on components, normality of `K` shows that `(k-I)` sends every reachable generator into the invisible subspace. On the observable invariant complement, the same vector lies in both the observable and invisible subspaces and must vanish. Thus `K` acts trivially and the observable action factors through the finite component group.

The converse is immediate from the quotient decomposition. The argument correctly handles a zero-dimensional observable quotient.

For clarity, the notation `V_o=V_r cap V_n^perp` should be described as the orthogonal complement **inside `V_r`**, although the present formula is correct because `V_n` is a subspace of `V_r`.

### 3.12 The planar and toral consequences

An irrational planar rotation makes the identity component `SO(2)`. Each specified coordinate mean ranges over the full interval `[-rho,rho]` on every component, so the threshold is exactly `rho/2`.

The fair decoder attains equality. The rational noncommuting example has infinite rotation order by the stated algebraic-integer argument.

The toral sum-of-amplitudes formula is correct when the actual component is the full product torus with independent coordinates. The manuscript appropriately declines to use it on a proper subtorus. The phrase “parameterized by independent angles” should be interpreted as surjectivity onto that product torus, not merely as an ambient coordinate presentation.

### 3.13 Nonlinear and unitary readouts

The measure-once unitary acceptance function is a continuous polynomial in the realified unitary matrix entries. Its binary mean is `2p-1`, so one quarter of the mean oscillation is one half of the acceptance-probability oscillation.

This is a numerical-probability statement and is correctly distinguished from recognition of a language at an isolated cutpoint.

### 3.14 Compact similarity and the identity hypothesis

A uniformly bounded group in `GL(D,R)` has a compact closure and an invariant positive-definite quadratic form obtained by Haar averaging. Conjugation makes the action orthogonal without changing the numerical interface or stochastic width.

The proof is correct. The proposition should repeat that the executable identity/padding assumption remains in force after conjugation.

The scalar contraction example and the single-letter irrational-rotation example correctly show that neither bounded positive semigroup dynamics nor omission of a padding command is covered by the classification.

### 3.15 Explicit harmonic localization

The normalized polynomials

```text
(1+cos phi)^r,
(1-cos phi)^r
```

have the stated Haar means and weighted cosine expectations. The central-binomial coefficient gives the displayed coefficient-sum bound.

Multiplication by `rho cos phi` increases the maximum frequency from `r` to `r+1`; this explains the feature degree `m=r+1`. The coefficient estimates yield the stated lower bound on the conditional harmonic moment.

The article deliberately replaces the sharper starting norm `sqrt(m)` by `m` in the rational constant `A_r`. This is valid but should be identified as a deliberate weakening in the theorem statement as well as the proof.

### 3.16 Separated powers and the block defect

The first `2k` orbit points in the direct sum of frequencies are pairwise separated whenever every power up to `2mk` is separated from one.

Each of `k` balls of radius smaller than half the separation contains at most one orbit point. At least half the orbit points therefore remain at distance at least half the separation from all centers. The inner-product defect is one half the squared Euclidean distance, producing the factor `sigma^2/16`.

The open-ball boundary wording is handled correctly.

### 3.17 The resultant estimate

For an algebraic unit-circle number which is not a root of unity, no conjugate is a root of unity. The resultant with `z^n-1` is therefore a nonzero integer.

Bounding the other conjugates by the Cauchy root radius gives

```text
|lambda^n-1| >= 2^{-(d-1)} B_P^{-n}.
```

Substitution into the separated-power lemma yields the finite-horizon and occupation bounds. The logarithmic rate follows by taking logarithms and separating the case in which the candidate width is already a large multiple of `log N`.

The proof is correct in its stated coarse form. The hidden constant in the `O(log log N)` term should be explicitly declared to depend on the polynomial, `rho`, and `epsilon`, as the text does.

### 3.18 The rational-circle and degree-four examples

For a rational unit-circle point `(a+ib)/c`, the numerator of `lambda^n-1` is a nonzero Gaussian integer and therefore has modulus at least one. This removes the conjugate factor and gives the sharper denominator bound.

The displayed degree-four polynomial is irreducible modulo two, and its other real trace conjugate exceeds two, so the chosen unit-circle root is not torsion. The value `B_P=8` follows from the coefficient-height definition.

The numerical calibration `rho=1/10`, `epsilon=1/25`, `r=5`, `Delta=1/150`, and `A=23364` is arithmetically consistent.

---

## 4. Why the four-journal standard is still not met

### 4.1 The theorem classifies a deliberately permissive invariant

The lower model gives the simulator:

- the terminal horizon for free;
- the current epoch for free;
- an entirely new machine at every horizon;
- arbitrary real row descriptions;
- free construction and lookup of those rows;
- exact real arithmetic; and
- exact atomic sampling from arbitrary real distributions.

The theorem is impressive precisely because the lower bound survives this advice. Nevertheless, the invariant is not ordinary memory, program size, description complexity, uniform workspace, or finite-random-bit complexity.

The separate finite-bit compiler in the supplement concerns a much more restrictive setting. It does not retroactively price the general component-oscillation theorem.

### 4.2 Reversibility and executable padding are essential

The theorem is about compact group closures. The paper itself gives counterexamples showing that:

- a bounded positive semigroup with irreversible contraction can have constant stochastic width despite an infinite inverse group; and
- without an identity or another padding mechanism, a single word per horizon can be decoded by horizon-specific advice.

These are not technical edge cases; they mark the central boundary of the result. A broader theory of compact semigroups or a precise necessary-and-sufficient padding condition would substantially increase the theorem’s reach.

### 4.3 The main quantitative problem is left open

Below the threshold, the classification yields divergence and an occupation theorem. It does not determine the order of the minimum peak.

For algebraic rotations the new bound is logarithmic:

```text
W_{N,epsilon} >= [log N - O(log log N)] / constant.
```

At smaller errors the retained arithmetic theory gives stronger power laws under additional Diophantine hypotheses. The relationship between the sharp noise threshold and the true subcritical growth remains unresolved.

A top-four-level continuation would likely require a sharp or nearly sharp growth theorem over a broad class, not only the bounded/unbounded boundary.

### 4.4 The general theorem is non-effective

For arbitrary real command matrices and continuous functions, the proof uses:

- exact compact-group components;
- exact extrema of arbitrary continuous functions;
- Stone–Weierstrass approximation;
- a Haar partition;
- executable positive-word approximants; and
- coefficient norms in tensor features.

None is supplied algorithmically from a finite input representation. The theorem is a mathematical classification, not a decision procedure.

This is acceptable for pure mathematics, but it weakens the computational interpretation and should be reflected in the title, abstract, and venue positioning.

### 4.5 The boundary-state count is not characterized

The midpoint construction uses at most `|S||C|` command states. The article explicitly does not claim this is minimal.

There is an interesting unresolved finite problem even at the threshold: identify the least stationary or nonstationary width needed to approximate all component functions within the critical error. Seeds, components, and queries may admit substantial quotienting.

A Myhill–Nerode-type equivalence or a minimal positive-realization theorem at the boundary would give the classification more structural depth.

### 4.6 The output semantics remain marginal

Queries are selected alternatives and only one binary marginal is requested. The theorem does not prescribe a joint distribution of several answers.

It does not immediately classify:

- one categorical output with a probability simplex constraint;
- simultaneous vector-valued probabilities;
- correlated multiple queries; or
- controlled output processes rather than one terminal answer.

These distinctions should remain explicit, particularly in comparisons with probabilistic and quantum automata.

### 4.7 The matrix-group setting is probably not the conceptual endpoint

The proof uses finite-dimensional matrix coordinates to invoke Stone–Weierstrass and tensor powers. For a general compact group, Peter–Weyl theory supplies finite-dimensional matrix coefficients which separate points.

The present theorem may therefore admit a more intrinsic formulation for compact groups or compact group actions. Either proving that formulation or explaining why the finite matrix embedding is essential would improve the conceptual statement.

### 4.8 Broader consequences are still limited

The article gives several correct examples, but the main external consequences are still concentrated in:

- planar rotations;
- partial linear interfaces;
- measure-once unitary readouts; and
- uniformly bounded matrix groups.

It does not yet produce a major theorem in positive systems, control, harmonic analysis, or complexity beyond the realization invariant itself.

### 4.9 The series branding remains disproportionate

The title after the colon is accurate. The prefix “General Theta Foundations I” still suggests a role in a broad foundational program.

The repository dependency graph shows that the theorem is mathematically independent of most of that program and closes none of its analytic gates. A conventional submission should use the descriptive title alone.

---

## 5. Novelty and literature positioning

The article’s comparison with Brodsky–Pippenger and Blondel–Jeandel–Koiran–Portier is careful and useful.

It correctly distinguishes:

- language recognition at an isolated cutpoint;
- preservation of a cutpoint language with a changed cutpoint;
- strict-threshold decision for quantum automata;
- positive realization of fixed system data; and
- worst-word additive approximation of a numerical interface by horizon-dependent stochastic machines.

In particular, the manuscript does not misstate the quantum-automata simulation result as uniform additive preservation of every acceptance probability.

However, the current audit is not broad enough for a definitive originality claim. Before publication, the author should provide a theorem-level comparison with at least the following bodies of work:

1. classical probabilistic automata and stochastic languages beyond the one Paz reference;
2. reversible and group automata, including quantitative rather than only language semantics;
3. real-valued weighted automata and rational series;
4. positive realization and hidden Markov realization of controlled numerical responses;
5. almost-periodic functions, Bohr compactification, and finite-state recognition of compact-group actions;
6. quantitative approximation of matrix coefficients of compact groups;
7. measure-once quantum finite automata under additive acceptance-probability error; and
8. approximate Myhill–Nerode or metric-automata formulations.

I am not asserting that one of these sources already contains Theorem `classification53`. The problem is that the present priority search is too narrow to establish the opposite.

The paper should include a table with columns

```text
present theorem | closest prior theorem | same hypotheses | changed hypotheses |
new quantifiers | genuinely new conclusion
```

for the component classification, the occupation result, the observable quotient, and the algebraic-circle bound.

The classical ingredients should continue to be credited as they are now. The novelty claim should be the complete combination of:

- arbitrary finite continuous numerical interfaces;
- horizon-dependent nonuniform stochastic realizations;
- a sharp componentwise error threshold;
- attainment by a finite component permutation machine; and
- occupation bounds below the threshold.

---

## 6. Relation to the repository-wide paper pipeline

Revision 53 has a clear local mathematical dependency chain:

```text
common-row endpoint compatibility
    -> finite-orbit/moving-space reduction
    -> positive executable word contraction
    -> tensor-polynomial conditional calibration
    -> localization at two output extremes
    -> sharp component-oscillation threshold
    -> fixed-width occupation below threshold.
```

The effective arithmetic branch is likewise clear:

```text
harmonic localization
    -> algebraic power separation
    -> finite orbit-point packing
    -> explicit contraction
    -> logarithmic subcritical width bound.
```

These are legitimate local advances.

The frozen Round-Seventeen repository ledger contains the independent chains

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1 -> C2 -> D1,
```

with A1 independent.

Their gates require, among other things:

- raw unsmoothed Fourier and density local limits;
- stopped entropy/LDP recovery;
- one global past kernel and weak-Harris control;
- interacting canonical coefficients and shell conditioning;
- process CLT and Mosco recovery;
- nonlinear Nisio resolvents and graph-core approximation;
- model-derived filtering and QMD/LAN;
- strict/form response with changing-filtration projection; and
- labelled posterior contraction.

The compact-group realization theorem proves none of these model-specific analytic statements and does not use them as premises.

Accordingly, Revision 53 should receive **no** credit for:

```text
historical A2 replacement,
B4 aggregate closure,
C2 aggregate closure,
eleven-paper aggregate closure,
or completion of the wider Theta program.
```

The repository’s history audit is appropriately explicit about this separation. It should remain so in any public submission.

---

## 7. Reproducibility and publication status

The publication chain is materially sound.

Workflow `36302217480` completed successfully. It:

1. checked that the work branch still matched the trigger commit;
2. fetched the pinned predecessor and r34 report;
3. materialized the frozen readable source;
4. committed the source at `cc598ea21ac7ffa0a4701b850a05efa1cbb64e71`;
5. installed fixed dependencies;
6. ran the new and inherited exact checks;
7. compiled the focused article, companion notes, and complete supplement;
8. rebuilt the native source archive without repository or network access;
9. compared all text and raster pages;
10. verified source and PDF hashes; and
11. atomically published the work and referee-ready branches without changing theorem or verifier source.

The receipt records:

```text
focused article:       14 pages
companion notes:         4 pages
complete supplement:    68 pages
new exact assertions: 1402
new negative controls:   18
total named negative controls: 122
normal/optimized agreement: true
isolated text equality: true
isolated raster equality: true
```

The retained Revision 52 inventory contains fifty-nine native files, thirty-three active inputs, and 242 loaded labels.

This is strong engineering and provenance evidence. It does not certify the universal proof or independent novelty.

The workflow materializes source and publishes artifacts in one job. The branch-head checks, source-commit binding, path fences, prohibition on theorem-source changes during publication, and atomic two-ref push make the procedure acceptably fail-closed. A future simplification could separate source publication and read-only validation into different jobs, but I do not regard the present arrangement as a release blocker.

---

## 8. Required revision before a serious external submission

### 8.1 Submit the focused article under a standalone title

Use

```text
Sharp Noise Thresholds for Stochastic Realizations of Compact Group Experiments
```

without the series prefix. Treat the complete supplement as optional background or a separately cited companion manuscript.

### 8.2 Complete the conventional literature audit

The paper needs a substantially broader theorem-by-theorem comparison with probabilistic/weighted automata, almost-periodic functions, compact-semigroup recognition, positive realization, and quantitative quantum-automata approximation.

Repository-internal revision citations should not substitute for archival references when conventional sources exist.

### 8.3 State the conceptual level of generality

Either:

- extend the main theorem from compact matrix groups to an intrinsic compact-group formulation using finite-dimensional matrix coefficients; or
- explain precisely why the finite matrix embedding is essential.

The current proof strongly suggests that the matrix dimension is a vehicle rather than the intrinsic object.

### 8.4 Develop a quantitative subcritical theory

At least one broad class should have matching or nearly matching lower and upper growth rates for fixed `epsilon<epsilon_c`.

The current logarithmic algebraic lower bound is valuable as an effective extension to the whole subcritical interval, but it does not determine the stochastic width scale.

### 8.5 Characterize minimal boundary width

The component midpoint construction proves boundedness but not minimality. A finite quotient, convex factorization, or approximate Myhill–Nerode characterization at `epsilon_c` would strengthen the structural result.

### 8.6 Clarify the effective-input problem

Define one finitely encoded input class—such as rational orthogonal matrices and polynomial/algebraic interface functions—and state which of the following are decidable or computable:

- the compact component group;
- the critical threshold;
- a boundary machine;
- one occupation constant `L_k`;
- and a subcritical width bound.

The current general theorem should remain explicitly non-effective.

### 8.7 Investigate the identity/padding boundary

Give a precise sufficient replacement for an identity command, such as a uniformly bounded padding language or a return-word condition. The single-letter counterexample shows that some hypothesis is necessary, but the exact boundary is not identified.

### 8.8 Preserve the output-semantics boundary

Either extend the theorem to one categorical output or vector-valued simplex-constrained probabilities, or state prominently that separately selectable binary marginals are essential to the midpoint construction.

### 8.9 Keep pipeline claims local

Do not present the theorem as closure of the repository-wide Foundations program unless a formal downstream dependency is proved. The current local derivation chain is sufficient and should stand on its own.

---

## 9. Possible routes to a substantially stronger paper

The following would materially change the editorial assessment.

1. **A compact-semigroup classification.** Extend the component-oscillation theorem to an intrinsic compact semigroup or identify the exact obstruction created by irreversible directions.
2. **Sharp subcritical growth.** Determine `W_{N,epsilon}` up to constants or matching exponents throughout a nontrivial family and across the full interval below `epsilon_c`.
3. **Effective algebraic classification.** Give an algorithm with explicit complexity for rational/algebraic compact-group inputs and polynomial interfaces.
4. **Minimal boundary realization.** Compute the least finite width at the critical threshold from an intrinsic quotient or convex-geometric invariant.
5. **General output laws.** Replace separately selectable Bernoulli means by categorical or joint probability outputs.
6. **A broad external application.** Derive a new theorem in positive systems, quantum automata, or controlled hidden Markov realization which was previously inaccessible.

Any one of these, if sufficiently complete, would give the main theorem broader mathematical force.

---

## 10. Minor and local comments

1. In Lemma `positive53`, explicitly justify the near-return with exponent difference at least two.
2. In the same lemma, state that `K` is open in `H`, so a relatively open subset of `K` is open in `H`.
3. In Lemma `gap53`, ignore zero-Haar-mass partition cells or state that their chosen atoms are irrelevant.
4. State the operator norm used for the finite approximation of `R(K)`.
5. The definition of `g` permits repeated centers; this is harmless but could be said once.
6. Immediately before `L53`, remind the reader that coefficient vectors have been fixed despite nonuniqueness.
7. In Proposition `residual53`, distinguish clearly between conditional mean error and pointwise decoder error; the proof uses the former.
8. In the lower proof, spell out once that every random test law is supported on executable deterministic words and correctness is applied word by word before averaging.
9. Replace `L_k` by `ceil(L_k)` if it is intended as an integer occupation count.
10. Explain the degenerate case `A=1`: it means no selected narrow block is compatible with the terminal residual, not that the proof has lost a logarithm.
11. In the boundary machine, specify left multiplication in the component group to match the word convention.
12. State whether unreachable seed/component pairs are counted in the displayed width bound. Under the manuscript’s available-label convention they are.
13. In Theorem `observable53`, describe `V_o` as the orthogonal complement of `V_n` inside `V_r`.
14. In the toral proposition, replace “parameterized by independent angles” by an explicit statement that the component is the full product torus under those coordinates.
15. In Proposition `similarity53`, repeat the identity-letter hypothesis.
16. In the scalar-semigroup counterexample, name which command is the identity and which is the contraction.
17. In Lemma `harmonic53`, identify the normalization of the real Fourier coefficient vector.
18. State in the theorem that `sqrt(m)` was weakened to `m` in `A_r` for a rational closed form.
19. In Lemma `separated53`, use one notation for the frequency-block representation and define it before the proof.
20. In Theorem `algebraic53`, say that the conjugates are listed with `lambda_1=lambda`.
21. State that irreducibility in characteristic zero implies the conjugates are distinct, although multiplicity would not affect the coarse bound.
22. In the resultant estimate, display the elementary inequality `|z^n-1|<=2 max(1,|z|)^n` used for the other conjugates.
23. In the logarithmic rate proof, give one line formalizing the case split which absorbs `log k` into `O(log log N)`.
24. In the rational-circle specialization, state that a nonminimal positive denominator is allowed and only weakens the bound.
25. The degree-four example is often recognizable as a reciprocal Salem-type polynomial; avoid naming a number class unless all conventional definitions are met.
26. In the measure-once unitary paragraph, repeat that only one terminal query is selected.
27. The automata comparison table should include the exact error norm and whether the machine is fixed or horizon-dependent in every row.
28. The effectivity remark should be echoed in the abstract by avoiding language that suggests an algorithm for arbitrary continuous input data.
29. The main article bibliography is intentionally short; the eventual submission bibliography should contain the full closest-prior-work comparison rather than relying on the supplement.
30. The complete supplement should be editorially optional. A referee of the focused theorem should not be assigned responsibility for recertifying every inherited revision.

---

## 11. Final assessment

Revision 53 is the first version in this sequence whose main theorem is both sharp and broadly formulated within its declared model. The component-oscillation formula, its boundary construction, and the arbitrary-width occupation converse appear correct. The manuscript has also become a genuine focused article.

The remaining objection is not that the work lacks mathematics. It is that the present theorem still concerns a specialized, highly nonuniform realization invariant, with compact reversibility and executable padding built in, and with most quantitative and effective questions left open. The novelty comparison is not yet broad enough to establish a four-journal priority claim.

I therefore recommend:

```text
Reject at the Annals / Inventiones / JAMS / Acta level.

Encourage a focused specialist submission after a conventional priority audit,
standalone retitling, and sharper explanation of the theorem’s intrinsic scope.
```

This recommendation assigns full credit to the mathematical advance actually proved. It assigns no credit for unrelated repository pipeline goals, cumulative revision history, or successful software qualification beyond reproducibility.