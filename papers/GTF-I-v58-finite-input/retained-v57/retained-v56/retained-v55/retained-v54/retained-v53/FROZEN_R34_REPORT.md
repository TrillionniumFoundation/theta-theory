# Referee Report — General Theta Foundations I, Revision 52

**Manuscript:** *General Theta Foundations I: Quantitative and Noisy Finite-Group Rigidity for Stochastic Realizations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v52-quantitative-lifts-2026-09-27`
- `revision/general-theta-foundations-i-v52-referee-ready-2026-09-27`

**Reviewed publication head:** `7641901c2ef957542aa50d9918f272ac7a72ca1c`  
**Validated native-source commit:** `eb73ed400b3b77aaee8bf52a06a587f8d207d011`  
**Workflow trigger:** `d499667fd538ca6882368cd793b6e19600ca28ea`  
**Source predecessor:** Revision 51 publication `6363748923a5623801a53cfdb507a776aad414c3`  
**Controlling prior report:** r33, `9d2f516b4113016f57fc8193c24ba192f8f782d5`  
**Review branch:** `review/general-theta-foundations-i-v52-quantitative-noisy-rigidity-harsh-top4-r34-2026-09-27`  
**Date:** 27 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

**Mathematical disposition:** Revision 52 is the strongest revision in the recent sequence. It answers the central mathematical limitation identified in r33: the exact arbitrary-width finite-group criterion is now extended to a fixed positive-error regime without a reachability-rank, minimum-state-probability, or conditioning hypothesis. I did not find a fatal counterexample to the finite-orbit reduction, the Haar-gap argument, the construction of a finite executable word law, the moving-component endpoint contraction, the terminal calibration, the resulting positive-error finite-group classification, the rational-height logarithmic lower bound, the effective one-surplus expansion, the conditioned stable-section theorem, the terminating unconditional six-state separation procedure, the global residual hierarchy, or the priced rational finite-group compiler.

The negative top-four recommendation is therefore **not** a correctness dismissal and is not a repetition of r33. Revision 52 makes a real conceptual advance:

```text
for every fixed 0 <= epsilon < rho/(2D),

uniformly bounded nonuniform clocked stochastic width
        if and only if
finiteness of the generated orthogonal command group
        if and only if
one exact stationary finite permutation realization exists.
```

The theorem applies at arbitrary hidden width and arbitrary reachability rank. It is substantially stronger than the rank-tight noisy theorem in Revision 51.

The present rejection rests instead on the following independent considerations.

1. **The interface remains highly specialized.** The theorem uses a finite orthogonal alphabet containing the identity, all signed coordinate seeds, and all coordinate queries. These hypotheses provide both the moving-subspace calibration and the full observability needed by the realization theory. Partial query families, nonspanning seeds, nonorthogonal commands, and more general controlled positive systems remain untreated.
2. **The universal noise range is sufficient and visibly nonsharp.** The paper proves the classification only for `epsilon < rho/(2D)`. A one-label fair answer works at `epsilon >= rho/2`, and the entire intermediate regime is open.
3. **The general quantitative mechanism is existential.** The Haar gap and the finite executable block exist for each fixed width, but no effective bound on their word length or contraction is supplied for arbitrary real input. The explicit logarithmic rate is restricted to a planar rational rotation and is intentionally coarse.
4. **The effective six-state results are still weak in scale or effectiveness.** The exact sufficient horizon `9,216,009` at `rho=1/10` is extremely coarse. The unconditional positive-error interval is only produced by a terminating real-algebraic search that was not run at that horizon. The explicit interval requires a supplied reachable-basis condition number.
5. **Much of the auxiliary machinery is classical.** Haar approximation, invariant subspaces, cap quantization, stochastic trace estimates, Farkas separation, Putinar positivity, Lasserre hierarchies, and exact rational rejection sampling are used competently, but do not individually constitute new general theories.
6. **The primary resource model remains exceptionally nonuniform.** Horizon-specific arbitrary real row tables, their construction and lookup, exact arithmetic, and atomic exact sampling are free in the main width invariant. The rational finite-group compiler is a valuable separate theorem, but it does not price the general lower-bound model.
7. **The article remains too accretive.** The complete article is sixty-eight pages and retains the two-state tensor theory, simplex theory, Gram and grid certificates, arithmetic exponents, Liouville fluctuations, and finite-bit compiler. The twenty-three-page focused excerpt demonstrates that a much more coherent specialist article is available.
8. **Priority positioning remains incomplete.** The manuscript compares positive realization, invariant polytopes, weighted and probabilistic automata, and polynomial positivity. It still needs a direct comparison with reversible automata, group languages, and measure-once quantum finite automata, where finite-group or permutation structure is already central under different recognition semantics.
9. **The repository-wide analytic pipeline remains open.** None of the new finite-dimensional realization theorems supplies the model-specific Fourier/local-limit, stopped-LDP, global-kernel, nonlinear-semigroup, filtering, operator-domain, or labelled-contraction results in the frozen A/B/C/D dependency graph.

**Disposition outside the four leading general journals:** major revision and substantial compression before submission to a strong specialist journal in positive realization, finite automata, switched systems, convex geometry, or algebraic optimization. A focused paper centered on the positive-error finite-group criterion, the reachable-section converse, the rational-height rate, and the effective one-surplus consequence could be a substantial contribution if its priority survives a conventional independent audit.

---

## 1. Scope, genealogy, and materials reviewed

At the final branch survey used for this report, Revision 52 was the latest referee-ready `General Theta Foundations I` revision. The work and referee-ready branches both pointed to

```text
7641901c2ef957542aa50d9918f272ac7a72ca1c.
```

No Revision 53 branch and no pre-existing Revision 52 review branch were present.

I reviewed the complete active input graph and the repository records needed to assess correctness, provenance, reproducibility, literature positioning, and relation to the wider paper pipeline. In particular, I examined:

- `papers/GTF-I-v52-quantitative-lifts/main.tex`;
- `introduction.tex`;
- `inherited/machine-model.tex`;
- `inherited/hankel-compatibility.tex`;
- `reachable-lifts.tex`;
- `all-width-rigidity.tex`;
- `noisy-rigidity.tex`;
- `effective-surplus.tex`;
- `global-certificates.tex`;
- `uniform-resources.tex`;
- `priority-comparison.tex`;
- `conclusion.tex`;
- the complete retained simplex, two-state, Gram, profile, arithmetic, and finite-bit appendices;
- `RESPONSE_TO_REFEREE.md`;
- `README.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `RESOURCE_LEDGER.md`;
- `HISTORY_AUDIT.md`;
- `LITERATURE_AUDIT.md`;
- `PRESERVATION_MANIFEST.json`;
- `EXPECTED_V50.json` and `EXPECTED_V51.json`;
- the new and inherited exact-check programs;
- the SOS certificate verifier;
- the build receipt, active-input manifest, theorem-location map, source hashes, focused excerpt, isolated-core receipt, and workflow status;
- the complete r33 report;
- the Revision 51 source package relevant to reachable sections and exact all-width rigidity;
- the earlier compatible-simplex, two-state, and word-profile predecessors used by the proof; and
- the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I also made targeted comparisons with the positive-realization and invariant-cone literature, invariant-polytope criteria, probabilistic and weighted automata, reversible/group automata, measure-once quantum finite automata, and classical polynomial positivity. This was not an exhaustive independent priority search.

The genealogy is clean. The workflow first materialized the readable mathematical source at `eb73ed400...`, validated and rebuilt that source, and then atomically published the generated package at `7641901c...`. The final publication commit is one commit beyond the validated mathematical source and does not silently change theorem source. Earlier revision and review branches remain untouched.

A successful source-bound build is useful evidence of delivery and regression control. It is not independent mathematical proof or priority certification. Conversely, the editorial recommendation below is not based on a packaging failure.

---

## 2. What Revision 52 genuinely accomplishes

### 2.1 Positive-error rigidity at arbitrary width

The principal theorem is new relative to Revision 51.

For an infinite generated orthogonal group `G`, the paper defines

```text
F = {v : Gv is finite}
```

and proves that `F` is an invariant linear subspace on which the group image is finite. Its orthogonal complement `E` is invariant and every nonzero vector of `E` has an infinite orbit under the compact closure `H` of `G`.

On the unit sphere of `E`, for any fixed endpoint width `k`, the paper considers the Haar-averaged quantization defect

```text
g_E(k)
  = min_(u,v_1,...,v_k)
      integral_H [1-max_j <v_j,hu>] d mu(h).
```

Compactness gives attainment. If the minimum were zero, full support of Haar measure would force the whole orbit of one nonzero vector to lie in a finite center set, contradicting the definition of `E`. Thus `g_E(k)>0`.

The positive word semigroup is dense in `H`. A finite operator-norm net and a measurable Haar partition therefore replace the Haar law by a finite distribution on executable positive words, uniformly over all unit starting directions and all `k` centers. Identity padding gives one common block length.

The inherited endpoint-centroid argument then contracts the conditional mean of the moving component at every selected block endpoint. Terminal numerical accuracy calibrates that moving component from below. This yields both a peak obstruction and an occupation bound for cuts of width at most `k`, while all other cuts may be arbitrarily wide.

The result is a true arbitrary-width theorem. No hidden state is assigned an unjustified observable vector, no rank-tight projection is imposed, and no lower bound on individual state probability appears.

### 2.2 Nonuniform approximate boundedness forces exact stationarity

The classification theorem concludes, for every fixed

```text
0 <= epsilon < rho/(2D),
```

that the following are equivalent:

1. `W_{N,epsilon}` is bounded over all horizons, even though a different machine and different real rows may be chosen at every horizon;
2. the generated orthogonal group is finite; and
3. one exact stationary permutation realization works at every horizon.

This is an attractive rigidity statement. Approximate, nonuniform, horizon-by-horizon realizability collapses to one exact uniform finite-group machine.

The proof does not merely invoke the exact result. It supplies a separate positive-error contraction on the moving representation and uses monotonicity in the horizon to convert unboundedness into divergence.

### 2.3 A direct rational-height width rate

For a planar rational rotation with eigenvalue

```text
(a+ib)/c,
```

not a root of unity, the paper uses the first `2K` powers of the rotation. The Gaussian-integer estimate

```text
|(a+ib)^q-c^q| >= 1
```

separates the orbit points by at least `c^{-2K}`. The cap argument then supplies a finite word distortion of order `c^{-4K}`. The endpoint theorem yields

```text
N < 2K {1+16 c^(4K) log(1/kappa)}
```

and hence

```text
W_{N,epsilon}
   >= [log N - O(log log N)]/(4 log c).
```

The alphabet may contain additional noncommuting commands. This is an explicit hidden-label lower bound which avoids the projected-vertex blowup in the exact all-width geometric proof.

### 2.4 An effective one-surplus expansion

The trace lemma gives a quantitative origin-asymmetry bound for a `D`-polytope with fewer than `2D` vertices or facets:

```text
s_0(P) >= D/(k-D).
```

A support-cone argument converts this into a volume increment. In dimension three the paper obtains

```text
beta_3(rho) >= 1+rho^3/1024.
```

For signed-permutation alphabets containing `I` and `-I`, this gives an explicit sufficient exact six-state horizon. At `rho=1/10`, the stated sufficient integer is `9,216,009`.

The constant is crude, but it replaces the purely compactness-based `beta_3(rho)>1` in Revision 51 by an actual formula.

### 2.5 Two positive-error six-state statements

The paper carefully separates two different results.

First, under a supplied reachable-basis condition number `A`, approximate physical sections obey a quantitative containment with

```text
b = rho-D delta,
h = A(1+sqrt(D)) delta,
Lambda = 1+Dh/b.
```

This yields a geometric occupation bound at arbitrary width and an explicit conditioned six-state interval.

Second, without conditioning, an exact finite-horizon separation and compactness imply a positive five-state error gap. Real-algebraic elimination can test dyadic tolerances and must eventually find an infeasible one. Identity truncation propagates that positive interval to every longer horizon.

The second theorem is unconditional but computationally impractical; the first is explicit but applies only to the conditioned class. The manuscript does not conflate them.

### 2.6 A complete global residual hierarchy

The bounded projector criterion is encoded as polynomial equalities on a compact variable box. The residual polynomial

```text
q = sum_j h_j^2
```

has minimum zero exactly for a feasible realization. Adding a redundant ball generator makes the quadratic module Archimedean. Putinar's theorem and the Lasserre hierarchy then give convergent lower bounds and finite detection of strict infeasibility.

This is a valid global certificate hierarchy over the unknown sections and transitions. It is not merely the local Farkas alternative for supplied geometric data.

### 2.7 A priced rational finite-group realization

For rational finite-group data, the orbit construction yields one horizon-independent deterministic permutation transducer. The paper separately prices:

- command-state labels;
- transition-table bits;
- rational decoder descriptions;
- persistent workspace;
- terminal workspace; and
- expected fair random bits.

This is an important clarification because it shows that the finite-group upper direction can be implemented without arbitrary real transition rows.

---

## 3. Detailed correctness audit

### 3.1 The finite-orbit subspace

Lemma `finite-orbit52` is correct.

If `v` and `w` have finite orbits, then the orbit of any linear combination is contained in the finite set of corresponding linear combinations of orbit points. Thus `F` is linear. It is invariant because `G(gv)=Gv`.

Choose a basis of `F`. The union of its finite orbits is a finite spanning set permuted by `G`; therefore the induced image of `G` on `F` is finite. Orthogonality makes `E=F^perp` invariant.

If `E=0`, the action on a basis has only finitely many possible images, so `G` is finite. If a nonzero vector in `E` had finite `G`-orbit, it would belong to `F`, a contradiction. Passing to the closure `H` does not enlarge a finite orbit.

Finally,

```text
sum_i ||P_E e_i||^2 = tr(P_E)=dim E,
```

so the displayed seed-moving lower bound follows.

The proof should explicitly say once that `P_E` commutes with every `U_a`, because `E` and `F` are orthogonal invariant subspaces. This fact is used later in the calibration.

### 3.2 Positivity of the Haar gap

The compactness argument for `g_E(k)>0` is sound.

The objective is continuous on the compact product of the unit sphere and `k` center spheres. If the attained integral were zero, its nonnegative continuous integrand would vanish on the full support of Haar measure. Hence the orbit of the chosen nonzero vector would lie in the finite center set. This contradicts the infinite-orbit property on `E`.

This proof uses the full numerical orbit, not a spectral gap. It remains valid for compact closures with invariant tori or more complicated compact subgroups.

The manuscript should state explicitly that an infinite compact orthogonal orbit is not required to be equidistributed under any fixed random walk. Haar measure is only an analyst's testing law, later replaced by a finite executable word law.

### 3.3 From Haar measure to actual words

The positive-word construction is correct.

For each generator, compactness of its positive powers gives positive powers approaching the identity, and the preceding powers approach its inverse. Hence the closure of the positive word semigroup contains all generator inverses and equals the group closure.

A finite operator-norm net of positive word matrices approximates `H`. The defect functions are uniformly Lipschitz in the group element, so pushing Haar masses to the representatives loses at most the covering radius. Choosing that radius at most `g_E(k)/2` leaves a positive defect. Identity padding makes all words have one common positive length.

For readability, I recommend using two symbols: one for the Haar minimum and one for the net radius. The current proof uses a closely related `eta` at both stages and then repairs the possible equality by saying “using a strictly smaller covering radius if necessary.” A direct choice `eta<g_E(k)/2` would be cleaner.

### 3.4 Endpoint contraction on the moving subspace

The repeated endpoint computation is valid.

A complete random block is independent of the past. Composing every internal stochastic row gives one endpoint kernel. The endpoint conditional mean satisfies

```text
z'_j = E[U_W z_S | S'=j].
```

Choosing each decoder center in the direction of `z'_j` and relaxing the executable assignment to the best of the `k` centers gives

```text
q' <= (1-d)q.
```

Intermediate widths are unrestricted. Hidden states with zero moving centroid contribute zero. Deterministic gaps cannot increase the conditional-mean norm by conditional Jensen and orthogonality.

This is the correct all-hidden-state quantifier. The proof does not assign an observable point to an arbitrary hidden basis state.

### 3.5 Terminal calibration

The moving-component calibration is also correct.

For the selected seed `e_i`, put

```text
Y_w = U_w P_E e_i / s_*.
```

Because `E` and `F` are invariant and orthogonal,

```text
<Y_w, U_w e_i> = s_*.
```

The realized terminal mean vector differs from `rho U_w e_i` by at most `2 epsilon` in every coordinate. Pairing with the unit vector `Y_w` loses at most `2 sqrt(D) epsilon`. Thus

```text
E <Y_N,D(S_N)> >= rho s_* - 2 sqrt(D) epsilon.
```

Conditioning on the hidden state and using `||D(S_N)||_2<=sqrt(D)` gives

```text
q_N >= rho s_*/sqrt(D) - 2 epsilon.
```

The paper combines the separately selectable coordinate decoder columns into one vector only as a proof device. It does not require the machine to output all coordinates jointly. This should be restated adjacent to the calibration to prevent a semantic misreading.

### 3.6 The universal small-noise range

The uniform range follows correctly from

```text
s_* >= 1/sqrt(D).
```

Therefore

```text
rho s_*/sqrt(D) >= rho/D,
```

and `epsilon<rho/(2D)` makes the final calibration strictly positive.

For any fixed peak `k`, the finite executable block gives a fixed contraction. Repeating disjoint blocks contradicts the calibration at large horizon. Hence no uniform finite peak exists for an infinite group.

For a finite group the exact orbit-permutation realization supplies a fixed upper bound. Horizon monotonicity follows by composing one final identity transition into the decoder. Thus unboundedness implies divergence.

I regard Theorem `noisy-finitegroup52` as proved.

### 3.7 The rational-height theorem

The height calculation is correct and deliberately crude.

For distinct powers among `I,R,...,R^(2K-1)`, their quotient exponent lies between one and `2K-1`. Since the eigenvalue is not a root of unity,

```text
(a+ib)^q-c^q
```

is a nonzero Gaussian integer and has modulus at least one. Thus the orbit separation is at least `c^{-2K}`.

A cap of half that radius contains at most one of the `2K` orbit points. The union of `K` caps has mass at most one half. Outside the union the Euclidean loss controls the scalar-product loss. The displayed `c^{-4K}/16` bound is conservative but valid.

Applying the block theorem at length `2K` gives the peak and occupation inequalities. Taking logarithms yields the stated lower rate.

Local clarifications:

- say whether `c` is assumed positive and whether the triple is primitive; the proof works with the displayed denominator even when it is not minimal, but the rate then depends on that choice;
- state that the `O(log log N)` constant depends on fixed `rho`, `epsilon`, and `c`; and
- distinguish this universal height rate from the stronger Diophantine power laws retained later.

### 3.8 The stochastic trace bound

The trace proof is correct.

At optimal origin asymmetry `lambda`, barycentric representations of the reflected vertices give a nonnegative row-stochastic matrix `T` with

```text
T 1 = 1,
T Z = -lambda^{-1} Z.
```

Full dimensionality makes the columns of `[1,Z]` independent. Therefore `1` is an eigenvalue and `-lambda^{-1}` has geometric multiplicity at least `D`. Every remaining eigenvalue lies in the unit disk. Since the trace is a nonnegative real number,

```text
0 <= tr T <= m-D-D/lambda.
```

This gives `lambda>=D/(m-D)` and hence the weaker uniform bound with `k`.

For completeness, the proof should say that nonreal remaining eigenvalues occur in conjugate pairs and that their real parts are at most one. This is implicit but worth making explicit.

The polarity argument correctly transfers the result from vertices to facets because the origin lies in the interior.

### 3.9 From asymmetry to volume

The support-cone proof is valid.

A direction attaining the support ratio supplies an apex in `-P`. The inner Euclidean ball supplies a perpendicular disk. The portion of the cone beyond the supporting hyperplane of `P` is disjoint from the interior of `P` and has the stated base radius and height. Dividing by the cube-volume upper bound yields the volume ratio.

A diagram would materially improve this proof. The argument is elementary but geometrically dense.

Substitution of `k=D+2`, `r=rho/sqrt(D)`, and `L=D/2` gives the displayed effective `beta_D`. The simplified three-dimensional rational constant is valid.

The numerical horizon at `rho=1/10` is a sufficient value only. The paper correctly does not call it the first transition.

### 3.10 Stable sections under a supplied conditioning bound

The conditioned theorem is sound.

Choosing independent actual reachable rows as a basis makes each point of the positive section have a unique coefficient vector. The maximum `A_t` exists by compactness and continuity of the inverse coordinate map.

For a complete suffix, the actual basis-prefix response and the identity-suffix physical mean transformed by the target orthogonal product differ by at most

```text
(1+sqrt(D)) delta
```

per coordinate. Multiplying by the coefficient vector gives the defect `h`.

Reachability of the actual stochastic updates sends the positive section into the next positive section. Thus

```text
U_w S_s subset S_t + h[-1,1]^D.
```

The approximate signed coordinate points imply

```text
C_(rho-D delta) subset S_t.
```

Since the cube lies in `D` times the unit crosspolytope, the additive error is absorbed into the dilation `Lambda`.

Volume iteration then gives the conditioned all-width and one-surplus occupation inequalities.

The basis dependence of `A_t` is substantial. A useful refinement would define the minimum possible `A_t` over all reachable bases, relate it to a standard Banach-space basis constant, and state whether it is computable from the local semialgebraic data.

### 3.11 The explicit conditioned six-state interval

The constants in the corollary close.

With

```text
delta <= rho^4/(2^22 A),
```

one has `b>=rho/2` and a small dilation excess. The cubic estimate on `(1+u)^3`, the effective lower bound for `beta_3(b)`, and the ratio estimate yield the multiplier `1+rho^3/16384`.

The exact six-state permutation construction belongs to the conditioned class with `A=1`, so the upper bound is attained within the same class.

The result is explicitly not an unconditional numerical noise theorem. That distinction is handled correctly.

### 3.12 The unconditional computable six-state interval

The existence proof is mathematically valid.

At the fixed exact-separation horizon, padding every peak-five machine to five labels produces a compact parameter space. The finite worst-word error is continuous and has a strictly positive minimum because exact realization is excluded.

Feasibility at a fixed algebraic tolerance is a finite semialgebraic problem: the formula explicitly contains every prefix row and common epoch/letter transition matrix. Word enumeration is exponential but finite. Real quantifier elimination decides the formula.

Testing dyadic tolerances tending to zero must eventually find an infeasible value. Identity truncation propagates infeasibility to every longer horizon, while the exact six-state machine supplies the upper bound.

The units should be made completely explicit. The compact minimum may be defined in mean error or binary total variation, while the semialgebraic formula uses `2 epsilon`. Termination is unaffected, but a named symbol for each unit would remove needless ambiguity.

The theorem is effective only in the recursion-theoretic sense. It should not be highlighted as a practical numerical result until an instance is actually executed.

### 3.13 The bounded local criterion and Farkas alternative

The inherited projector characterization remains correct. Revision 52 now gives the complete equation and inequality counts and includes all three transition blocks:

1. row sums;
2. projector-range invariance; and
3. observable intertwining.

For fixed projectors and mean matrices, the transition problem is a rational linear feasibility problem. Equality-form Farkas separation gives the stated finite witness. The normalization `b^T y=-1` is legitimate after obtaining a strictly negative witness.

The local alternative does not solve the global unknown-section problem. The manuscript is explicit about this boundary.

### 3.14 The global residual hierarchy

The SOS theorem is a standard and correct application of Putinar and Lasserre.

The variable box contains all probability, transition, projector, and mean variables. The sum of squared equality residuals has minimum zero exactly when the realization equations are feasible. The interval generators encode the remaining inequalities.

Adding

```text
g_0 = n-sum_i x_i^2
```

makes the quadratic module Archimedean. For every `lambda<m_*`, strict positivity of `q-lambda` gives a finite Putinar identity. Thus strict infeasibility is detected at some finite degree, while feasible boundary cases need not have finite convergence.

With algebraic coefficients, coefficient matching and positive semidefiniteness form a finite semialgebraic system. Real-closed-field sampling supplies algebraic Gram matrices when a real certificate exists.

The notation `sigma_{-1}` for the free SOS term should be defined in the theorem statement. The exact verifier based on all principal minors may be exponentially large; the paper should distinguish certificate existence from economical verification size.

This hierarchy is generic. It does not strengthen the editorial significance of the paper unless accompanied by structure-specific degree bounds or solved nontrivial instances.

### 3.15 The rational finite-group compiler

The compiler theorem is correct.

A finite rational orbit can be enumerated by breadth-first closure under the alphabet. Commands act by deterministic permutations. Rational coordinate readout gives rational Bernoulli probabilities.

Rejection sampling from a power-of-two range produces the exact rational coin. The acceptance probability of each trial exceeds one half, so fewer than two trials and fewer than `2L` fair bits are used in expectation. The workspace bounds are plausible and the unbounded worst-case sampling time is correctly stated.

The orbit-enumeration time and the height of generated rational points are not bounded by the label width. The paper appropriately separates preprocessing from persistent memory.

---

## 4. Novelty and relation to prior theory

Revision 52 contains a genuine theorem, but its conceptual ingredients have substantial classical ancestry.

- Positive realization by invariant cones and nonnegative intertwiners is classical.
- Invariant polytope criteria and finite permutation actions are classical objects in switched systems and automata.
- Haar averaging and finite net approximation on compact groups are standard.
- The endpoint-centroid contraction is inherited from the manuscript's own earlier line.
- Farkas separation, real quantifier elimination, Putinar positivity, and Lasserre hierarchies are standard general-purpose tools.
- Rational rejection sampling is elementary.

The specific synthesis is nontrivial: a horizon-dependent stochastic realization with bounded positive error is shown to force finiteness of the underlying orthogonal action and one exact stationary realization. That implication is the principal claim requiring independent priority assessment.

The current literature discussion is improved but still incomplete. In particular, the paper should compare directly with the algebraic theory of reversible automata and group languages, and with measure-once quantum finite automata. Brodsky–Pippenger and subsequent work characterize important bounded-error unitary automata classes through group-like syntactic structure. Their semantics concern language recognition or cutpoints rather than uniform approximation of every prescribed numerical probability, so they do not immediately imply the present theorem. Precisely because the objectives differ, a theorem-level comparison is required:

```text
model | uniformity in word length | output semantics | error notion |
allowed advice/nonuniformity | algebraic conclusion
```

The paper should also search the literature on finite semigroup actions, compact group representations in probabilistic transducers, and bounded-order positive realizations. A targeted repository audit is not sufficient priority clearance for a top-four submission.

I do not regard the generic SOS hierarchy as a central novelty claim. It is best presented as an optional computational appendix or supplement.

---

## 5. Why the theorem is still too narrow for the four leading journals

### 5.1 Full signed-coordinate observability is essential

The lower calibration uses signed coordinate seeds and every coordinate query. It obtains a uniformly visible moving vector because the standard basis resolves every nonzero invariant subspace.

The theorem does not cover:

- a proper query subspace;
- an arbitrary finite seed set which does not span every moving component;
- selected scalar outputs without a uniform observability inequality;
- nonlinear or categorical outputs; or
- nonorthogonal stable command families.

A more general theorem should be formulated in terms of an intrinsic observability constant for the moving representation. The present `rho/(2D)` threshold is a coordinate-interface consequence, not an invariant classification of arbitrary numerical transducers.

### 5.2 The noise boundary is far from classified

The proof gives a universal sufficient range

```text
epsilon < rho/(2D).
```

The trivial fair answer works at

```text
epsilon >= rho/2.
```

Nothing sharp is proved in between. Even for planar irrational rotations, the critical error for uniformly bounded width is not determined.

A four-journal result would ideally identify an action-dependent critical tolerance, prove matching lower and upper statements, or exhibit a broad class where the current boundary is sharp.

### 5.3 The general width-growth result is nonquantitative

For a general infinite compact group action, the proof gives one positive contraction for each fixed width, but no computable block length or contraction from the input matrices. It therefore proves divergence without a rate.

The rational planar height theorem gives only a logarithmic rate. The retained arithmetic theory already gives stronger power laws under Diophantine hypotheses. The new theorem is broader in arithmetic assumptions but not sharp.

A significant next advance would quantify the Haar gap or executable net in terms of algebraic height, dimension, spectral data, or an effective compact-group presentation.

### 5.4 The one-surplus numerical consequence is extremely coarse

The explicit horizon `9,216,009` is mathematically legitimate but offers little geometric resolution. The paper does not determine the first six-state horizon, the sharp expansion constant, or a useful unconditional numerical noise interval.

The unconditional interval is obtained by a theoretically terminating elimination over a huge finite horizon and is not executed. This is not yet persuasive numerical evidence of stable six-state optimality.

### 5.5 The resource model remains nonuniform

The main lower-bound theorem allows:

- a different machine for every horizon;
- free horizon and clock;
- free horizon-dependent real row tables;
- free construction and lookup;
- exact real arithmetic; and
- atomic exact sampling.

This makes the rigidity theorem stronger in one direction: even this permissive model cannot hide an infinite action at small error. It also limits computational interpretation. Width is not total memory, description length, runtime, or random-bit cost.

The rational finite-group compiler is a valuable positive theorem, but it addresses only the finite-group upper side with rational data. It does not price arbitrary real approximate machines.

### 5.6 The paper is still an archive rather than one article

The sixty-eight-page complete manuscript includes a coherent twenty-three-page main chain followed by a very large inherited appendix. The appendix contains several independent research programs:

- two-state sign–magnitude duality;
- compatible simplices;
- Gram and moment certificates;
- distortion and enclosure profiles;
- arithmetic width exponents;
- Liouville fluctuations; and
- a separate finite-bit compiler.

Preservation in the repository is commendable. It is not a reason to submit every predecessor theorem in one journal article.

The focused excerpt should become the basis of the submission. Necessary inherited lemmas can be restated or cited. The remaining material should be split into companion papers or a clearly labelled supplementary archive.

---

## 6. Quantitative limitations requiring further work

1. **Action-dependent noise threshold.** Define an intrinsic visibility constant for the moving subspace and determine whether the classification holds up to that threshold. Supply examples showing sharpness or failure.
2. **Effective Haar-word block.** For algebraic orthogonal matrices, bound the finite word length and gap in terms of dimension, degree, height, and width.
3. **Broader algebraic groups.** Extend the rational-height argument beyond one planar rotation, for example to finitely generated algebraic compact groups or simultaneous toral rotations.
4. **Unconditional noisy one-surplus constant.** Produce an explicit numerical `epsilon_0`, not only a terminating elimination procedure, at a nonastronomical horizon.
5. **Sharp surplus expansion.** Determine or sharply bound `beta_3(rho)` and the first six-state horizon.
6. **Structure-specific certificate degrees.** Give a useful bound for the SOS hierarchy or solve a nontrivial unknown-section instance exactly.
7. **Partial interfaces.** Characterize what replaces finite-group rigidity when the seeds and queries observe only a quotient representation.
8. **Nonorthogonal commands.** Explain which parts survive for uniformly bounded invertible or contractive commands and which fail.

Without progress on several of these points, the paper remains a strong specialized theorem rather than a broad foundational result.

---

## 7. Relation to the repository-wide paper pipeline

The repository's frozen Round-Seventeen ledger contains the chains

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1 -> C2 -> D1,
```

with A1 independent.

Revision 52 establishes a self-contained finite-dimensional chain:

```text
reachable spans
 -> finite-orbit subspace
 -> executable moving-space distortion
 -> arbitrary-width noisy occupation
 -> finite-group rigidity
 -> effective height and surplus consequences
 -> finite certificates and a rational compiler.
```

This chain does **not** provide any of the following independent analytic gates:

- returned raw Fourier or density local-limit estimates;
- entropy-controlled stopped large deviations;
- one global past kernel and weak-Harris/renewal control;
- direct canonical coefficient and shell conditioning;
- process CLT and Mosco tangent recovery;
- Nisio resolvent, m-dissipativity, graph core, or nonlinear Trotter–Kato;
- model-derived filtering and QMD/LAN;
- strict/form response and changing-filtration optional projection; or
- labelled posterior contraction.

The manuscript's `PIPELINE_STATUS.json` correctly refuses to infer analytic closure. No A2, B4, C2, D1, or eleven-paper aggregate credit should be assigned from Revision 52.

The finite-dimensional theorem may eventually serve as a memory or realization lemma inside another paper. Such downstream use must be stated and proved explicitly; repository proximity does not establish it.

The series title “General Theta Foundations I” continues to suggest a repository-closing role which the dependency graph does not support. The mathematical subtitle is precise, but a specialist submission should remove or deemphasize the series branding.

---

## 8. Reproducibility and publication status

The source and build chain is substantially improved over earlier revisions.

The reviewed final head is

```text
7641901c2ef957542aa50d9918f272ac7a72ca1c.
```

The readable mathematical source was materialized at

```text
eb73ed400b3b77aaee8bf52a06a587f8d207d011.
```

Workflow `36298407771` completed successfully. Its single `qualify-and-publish` job successfully:

1. checked out the triggering branch;
2. materialized and committed the frozen native manuscript;
3. installed fixed dependencies;
4. validated the exact native source;
5. rebuilt the isolated source archive;
6. uploaded the validated package; and
7. atomically published the revision refs after checking source immutability.

The build receipt records:

- sixty-eight article pages;
- a twenty-three-page focused excerpt;
- thirty-three active input files;
- all 201 predecessor labels preserved and 242 current labels loaded;
- ordinary/optimized agreement;
- zero undefined references;
- zero overfull boxes;
- all-page text and raster equality for the isolated rebuild;
- 104 named negative-control executions, including thirty-six new v52 controls;
- exact finite checks of the trace, height, local-equation, sampling, and supplied SOS mechanisms; and
- a fail-closed resource-limit path.

This is strong reproducibility evidence. It does not independently prove Haar compactness, the universal noisy theorem, the asymmetry theorem, or originality. The receipt itself correctly states that boundary.

The unconditional six-state error search was not executed. The generic SOS search engine was not implemented. Those absences are honestly recorded and should remain explicit.

---

## 9. Required revision before specialist submission

### 9.1 Reduce the article to one theorem chain

The journal-facing paper should center on:

1. reachable sections and exact all-width rigidity;
2. finite-orbit reduction;
3. positive-error arbitrary-width classification;
4. the rational-height rate; and
5. the effective one-surplus consequence.

Move the two-state tensor optimizer, the full Gram/grid machinery, arithmetic exponents, Liouville fluctuations, and the finite-bit compiler to companion papers or supplementary references. Do not ask a referee to treat sixty-eight pages of cumulative revision history as one coherent contribution.

### 9.2 Add an invariant formulation of observability

Replace the coordinate-specific visibility estimate by a theorem stated for a seed/query interface with an explicit observability constant. Derive the current result as a corollary. Give a counterexample when the moving representation is invisible.

This would reveal the actual mathematical boundary and make the theorem more reusable.

### 9.3 Sharpen or contextualize the noise range

At minimum, compute the best threshold for one nontrivial family, such as an irrational planar rotation. Better still, characterize the critical tolerance in terms of the observable moving representation.

The present gap between `rho/(2D)` and `rho/2` is too large to leave unexplored in the main theorem paper.

### 9.4 Make one quantitative theorem genuinely effective

Choose one of the following and complete it:

- effective word-length and contraction bounds for algebraic compact actions;
- a practical unconditional six-state noise interval;
- a sharp or near-sharp `beta_3` estimate; or
- a structure-specific finite SOS degree bound.

A theorem whose algorithm terminates only through generic quantifier elimination at horizon nine million should be presented as decidability, not as a numerical quantitative result.

### 9.5 Complete the automata-theoretic priority comparison

Add a direct comparison with:

- reversible finite automata and group languages;
- Brodsky–Pippenger's characterization of one-way quantum finite automata;
- later measure-once quantum finite automata and algebraic-group work; and
- finite semigroup or probabilistic-transducer rigidity results.

Explain exactly why uniform approximation of the entire probability table, nonuniform horizon dependence, and stochastic hidden positivity make the present theorem different.

### 9.6 Keep computational claims separated

Retain the following distinctions in theorem statements and the abstract:

- mathematical existence versus implemented search;
- supplied certificate verification versus certificate discovery;
- recursion-theoretic computability versus useful complexity;
- atomic real-row width versus conventional memory; and
- exact expected-bit sampling versus worst-case runtime.

### 9.7 Preserve the pipeline boundary

Keep the A/B/C/D gates explicitly open. Either prove a concrete downstream dependency theorem or present this as an independent realization-theory paper rather than a repository foundation closure.

---

## 10. Local and editorial comments

1. In Lemma `finite-orbit52`, state explicitly that orthogonal invariance of `F` and `E` implies `P_EU_a=U_aP_E`.
2. Define the “positive word semigroup” before proving that its closure equals `H`.
3. Use a net radius strictly smaller than `g_E(k)/2`, then define `d` from the remaining gap. This avoids the explanatory parenthesis about a smaller radius.
4. State the dimension of `E` next to the sphere notation. If `G` is infinite, `E` cannot be one-dimensional under an orthogonal action; the proof does not need this, but readers may wonder.
5. Repeat that the vector of decoder means is a proof device assembled from separately selected coordinate queries, not a joint output channel.
6. In the noisy occupation theorem, say whether candidate endpoints include cut zero; align the convention with the displayed counting formula.
7. State all dependence of `B`, `d`, and `chi` on `k`, the action, and the selected representation.
8. In the universal theorem, separate the action-dependent range `epsilon<rho s_*/(2sqrt D)` from the coordinate-uniform corollary `epsilon<rho/(2D)`.
9. In the rational-height theorem, require `c>0` and explain that a nonminimal denominator only weakens the bound.
10. Put the dependence of the asymptotic `O(log log N)` term in the theorem statement or immediately after it.
11. In the cap argument, state whether caps are open or closed; the half-separation choice makes either convention harmless with a minor adjustment.
12. In the trace lemma, mention conjugate pairing of nonreal eigenvalues and use real parts explicitly.
13. Define `s_0(P)` through support functions as an equivalent formula before the cap-volume lemma.
14. Add a figure for the truncated support cone used in the volume increment.
15. In Theorem `beta52`, distinguish the exact coefficient involving `omega_{D-1}` from the deliberately weakened rational coefficient.
16. For the numerical horizon, put the exact rational verification in an appendix and keep only the conclusion in the main proof.
17. Define a basis-minimized version of `A_t` or explain why the supplied-basis formulation is preferable.
18. In the conditioned theorem, state explicitly that the whole suffix is evaluated once; this is the reason errors do not accumulate with its length.
19. Use different symbols for mean error and binary-TV error throughout the unconditional separation theorem.
20. The phrase “computable noise interval” should be accompanied every time by “not executed at the illustrative horizon.”
21. In the local count, explain whether repeated symmetry equations are deliberately retained for a simpler formula.
22. In the SOS theorem, define `sigma_{-1}` as the free SOS term.
23. Explain whether exact PSD verification is by principal minors, an algebraic LDL decomposition, or another certificate format; the output-size implications differ.
24. Move the generic Putinar–Lasserre discussion to an appendix unless a nontrivial realization instance is solved with it.
25. In the rational compiler, distinguish the bit length of a probability from the bit length of the orbit coordinates used to produce it.
26. State whether breadth-first orbit enumeration uses canonical reduced rational coordinates and how duplicate testing is performed.
27. The resource table is useful and should remain near the start of the paper.
28. The focused excerpt should not be called merely a reading aid; it is close to the appropriate submission manuscript.
29. Conventional references should replace internal revision citations wherever the inherited mechanism has a published antecedent.
30. The conclusion should state one primary open theorem rather than a broad list of future directions.

---

## 11. Final evaluation

Revision 52 is a major improvement and, in my view, the first revision in this line with a convincing positive-error arbitrary-width rigidity theorem. Its central proof is coherent:

```text
finite-orbit decomposition
 -> positive Haar quantization defect on the moving subspace
 -> finite executable block
 -> hidden-state endpoint contraction
 -> coordinate calibration
 -> bounded approximate width iff finite group.
```

I found no fatal mathematical gap in this chain.

Nevertheless, the result remains tied to a fully observable orthogonal interface and a conservative small-noise range. The general rate is ineffective, the explicit consequences are coarse, the computational additions are generic, the primary resource model is nonuniform, the article is still overgrown, and the wider repository pipeline remains untouched.

Accordingly:

```text
Annals / Inventiones / JAMS / Acta: Reject.

Strong specialist journal: potentially publishable after major
compression, a conventional priority audit, and sharper framing of the
observability, noise, quantitative, and resource boundaries.
```

The rejection should not be read as a claim that the main theorem is false. It is a judgment that the present theorem, scope, and presentation do not yet meet the breadth and transformative significance expected at the four leading general mathematics journals.