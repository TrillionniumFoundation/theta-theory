# Referee Report — General Theta Foundations I, Revision 34

**Manuscript:** *General Theta Foundations I: Fourier Budgets for Hidden Causal Memory*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v34-referee-ready-2026-09-25`  
**Reviewed head:** `47bc47e5995e4b1b99a18aaa472a1309f1668f40`  
**Native mathematical source recorded by the manuscript:** `5d773fb7dddb007887119b35cc29e0b3bae7406f`  
**Controlling previous report:** `ee524c3e210ede7d6ff927c2bd2a2a1a104cb28c`  
**Previous reviewed manuscript:** `aab96108125317342e51e6a946efc4d778429338`  
**Review branch:** `review/general-theta-foundations-i-v34-compatible-dynamics-pipeline-harsh-top4-r19-2026-09-25`  
**Date:** 25 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

Revision 34 is a genuine mathematical advance over Revision 33. It directly addresses the central hidden-lift objection in the eighteenth report: the unrestricted lower bound no longer passes through the exponentially many vertices of a projected simplex section. The new conditional-phase/Fourier argument applies to arbitrary hidden states, arbitrary cut-dependent stochastic matrices, and a new machine at every horizon. It upgrades the unrestricted bounded-type lower bound from logarithmic to polynomial, survives a fixed uniform output error, and transfers to a nonvanishing accumulated deficiency obstruction for every proposed small stochastic diagram of the same experiment.

I did not find a short fatal counterexample to the principal new proof. In the finite-horizon, wordwise, clocked, atomic stochastic-row model actually stated, the conditional-amplitude monotonicity, homogeneous angular estimate, moment recursion, Fejer witness, occupation budget, terminal calibration, rational-angle arithmetic bound, and executable deficiency composition are internally coherent. The negative recommendation is therefore **not** based on an allegation that the headline theorem is false.

The four-journal case nevertheless fails.

1. The central quantitative problem remains open. At bounded-type angles the manuscript proves only

   ```text
   Omega_alpha(N^(1/5)) <= W_N(alpha) <= O_alpha(N^(1/3)).
   ```

   The difference is not a secondary constant or endpoint issue. It is exactly the remaining question of whether genuinely hidden stochastic lifts beat the vector-state construction and, if so, by how much.
2. The manuscript still omits the closest computational-model literature. A clocked transducer with one binary command per layer, two stochastic transition matrices, width `K_t`, and a terminal affine readout is naturally a nonuniform probabilistic generalization of an oblivious read-once branching program or probabilistic OBDD. Fourier analysis and Fourier-growth bounds for read-once branching programs, including permutation, regular, and width-three models and generalized group products, form a direct neighboring literature. None appears in the bibliography or audit.
3. The fair-command proof process `L_t alpha mod 1` is a Bernoulli random walk on the circle whose Fourier damping and dependence on Diophantine approximation belong to a developed probability literature. This does not subsume the memory lower bound, but omission prevents the reader from separating the new compression argument from known harmonic and arithmetic behavior of the underlying walk.
4. The main theorem concerns one highly structured planar rotation experiment, one final two-coordinate query, and bounded-type arithmetic. The paper gives no general compact-group, representation-theoretic, higher-dimensional, or spectral criterion from which the rotation theorem emerges as one instance.
5. The deficiency theorem is operationally correct but largely derivative. Its diagram defect is an additive executable upper certificate for terminal error, not the exact dynamic deficiency and not a characterization of optimal cancellation. The lower bound follows by converting a diagram into a machine and invoking the main theorem.
6. The resource model remains permissive: the epoch and horizon are free, transition tables and arithmetic are uncharged, exact computable-real kernels are atomic, rows may vary by cut, and only one terminal query is required. This is a legitimate positive-realization width, not conventional streaming-space or uniform branching-program complexity.
7. The repository-wide Foundations pipeline is unchanged at every difficult analytic gate. A2, B4, C2, the eleven-paper aggregate, fully adaptive collision scheduling, the noisy-tag problem, and the sharp hidden exponent all remain open in the manuscript's own status records.

Revision 34 is a serious specialist-paper candidate. It is not close to the standard of the four leading general mathematics journals, and the word “Foundations” continues to overstate its relation to the repository's main analytic program.

---

## 1. Scope of this review

I reviewed the focused Revision 34 article and the repository records needed to evaluate both the local mathematics and its position in the larger pipeline. In particular, I examined:

- `papers/GTF-I-v34-compatible-dynamics/main.tex`;
- `introduction.tex`;
- `machine-model.tex`;
- `fourier-budget.tex`;
- `rotation-consequences.tex`;
- `deficiency-diagrams.tex`;
- `symmetry-and-autonomy.tex`;
- `literature-and-scope.tex`;
- `references.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `LITERATURE_AUDIT.md`;
- `HISTORY_AUDIT.md`;
- `RESOURCE_LEDGER.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `verify.py` and the executed build records;
- the complete eighteenth referee report;
- the Revision 33 lower- and upper-bound arguments reused or sharpened here;
- the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md`.

I also made a targeted external comparison with the directly adjacent literature on:

- Fourier analysis of oblivious read-once branching programs;
- width-three and regular branching-program Fourier growth;
- generalized group products and modular sums;
- random walks on the circle and Diophantine approximation.

This was targeted, not exhaustive priority clearance.

The publication genealogy is clean. Revision 34 descends from the controlling r18 report, preserves Revision 33, and adds a branch-specific package rather than overwriting prior manuscripts. This is good provenance practice. It is not evidence for correctness, priority, or journal significance.

The 13-page article is self-contained enough to audit its new claims. The 435-page mathematical archive and 988-page development archive are therefore optional provenance records, not proof supplements that increase the mathematical weight of the submission. I did not treat hashes, regression counts, negative controls, page comparisons, or successful compilation as substitutes for mathematical proof.

---

## 2. What Revision 34 genuinely repairs

### 2.1 It answers the strongest mathematical demand in r18

Revision 33 identified compatible hidden lifts correctly but retained an exponential loss in the converse: a `K`-state simplex section can project to a polygon with up to exponentially many vertices. Consequently the unrestricted lower bound was only logarithmic, while the vector-state subclass had cube-root width.

Revision 34 abandons projected-vertex counting. Under an externally chosen fair-command test law, it studies

```text
z_t(s) = E[zeta^(-L_t) | S_t=s],
q_t    = sum_s P(S_t=s) |z_t(s)|.
```

There are at most as many phase atoms as positive-probability hidden states, regardless of the number of vertices in any observable projection. This is precisely the kind of all-hidden-state argument requested by the previous report.

### 2.2 The lower bound is an occupation theorem, not only a peak bound

For every `k`, the manuscript proves

```text
#{0 <= t < N : K_t <= k} beta_(2k)(alpha)
    <= 18 k^3 / kappa^2.
```

Other cuts may have arbitrarily large registers. Thus the theorem controls how often small memory can occur in a nonuniform profile and is stronger than merely lower-bounding the minimum peak.

### 2.3 The result is robust to fixed output error

The proof needs only a final correlation. Uniform binary row-TV error `epsilon` changes each coordinate mean by at most `2 epsilon`, giving terminal amplitude

```text
kappa = 1/10 - 2 epsilon.
```

For every fixed `epsilon < 1/20`, the polynomial bounded-type lower bound survives. This is materially stronger than an exact-only obstruction that disappears under arbitrarily small perturbation.

### 2.4 The rational rotation receives an explicit rate

The Gaussian-integer estimate for `(3+4i)^l - 5^l` gives

```text
N <= 7200 K^3 25^(2K),
```

and hence a logarithmic unrestricted lower bound. This improves the preceding abstract or doubly logarithmic discussion and uses fully explicit arithmetic data.

### 2.5 The deficiency discussion is now attached to the main family

The previous `1/4` toy defect did not constrain the rotation experiment. Revision 34 defines common-row deficiencies for a complete prefix-indexed diagram, composes minimizing garblings into an actual machine, and invokes the Fourier converse. This yields a lower bound on the total certified defect for every bounded-width diagram of the main experiment.

### 2.6 Earlier literature defects are substantially repaired

The article now credits Blackwell comparison, one-sided deficiency, symmetric and equivariant lifts, static polygon extensions, fixed-degree positive-realization lower bounds, and the distinction between fixed-length and anytime autonomous tasks. The contribution table is more honest than in earlier revisions.

These changes make Revision 34 a much stronger paper than Revision 33. They do not close the central problem or establish four-journal depth.

---

## 3. Technical audit of the Fourier argument

### 3.1 The test distribution is legitimate

The specification is wordwise. Therefore a converse may impose any distribution on the external command words. Taking independent fair commands does not weaken the simulation requirement or give additional information to the machine.

The process may have different state spaces and different stochastic matrices at every epoch. The proof does not assume stationarity, reversibility, a common transition, or a statewise predictive vector.

### 3.2 Conditional phase amplitude

With `Y_t = zeta^(-L_t)` and

```text
z_t(s) = E[Y_t | S_t=s],
q_t    = E |z_t(S_t)|,
```

the identity

```text
z_(t+1)(S_(t+1)) = E[zeta^(-C_(t+1)) z_t(S_t) | S_(t+1)]
```

follows from the stochastic update and independence of the fresh command from the past. Conditional Jensen gives `q_(t+1) <= q_t`, so the total amplitude loss telescopes and is at most one.

This part is correct and uses no illicit conditional independence of the past given the retained state.

### 3.3 The homogeneous angular estimate

For

```text
f_l(r exp(i theta)) = r exp(i l theta),
```

the claimed estimate

```text
|E f_l(Z) - f_l(EZ)|
    <= (l^2+1)(E|Z| - |EZ|)
```

is valid. The proof handles `EZ=0` and atoms at zero correctly.

There is, however, a small expository gap in the displayed estimate. From

```text
u^l - 1 - l(u-1) = (u-1) sum_(j=0)^(l-1) (u^j-1)
```

one should retain the sharper bound

```text
|u^l - 1 - l(u-1)|
    <= l(l-1)(1-cos theta),
```

obtained from `sum j = l(l-1)/2` and `|u-1|^2=2(1-cos theta)`. Adding the remaining `(l-1)(1-cos theta)` term gives `(l^2-1)(1-cos theta)`, and hence the stated result. The manuscript first coarsens this to `l^2(1-cos theta)` and then says “consequently”; that coarse line alone does not transparently imply the next displayed constant. This is readily repaired and does not affect the later `2l^2` budget.

### 3.4 Moment recursion

Rotation covariance gives

```text
E f_l(zeta^(-C_(t+1)) z_t(S_t))
    = a_l m_(t,l),
    a_l = (1+zeta^(-l))/2.
```

The angular averaging error at epoch `t` is charged to the same scalar loss `ell_t=q_t-q_(t+1)` for every harmonic. The recursion

```text
m_(t+1,l)=a_l m_(t,l)+e_(t,l),
|e_(t,l)| <= 2 l^2 ell_t
```

is therefore justified. Since both terms have modulus at most one, the squared recursion with a `4l^2 ell_t` error follows.

This common-loss feature is the real technical contribution of the paper.

### 3.5 The finite-atom Fejer witness

The positive measure

```text
nu_t = sum_s p_t(s)|z_t(s)| delta_(arg z_t(s))
```

has mass `q_t`, at most `K_t` atoms, and Fourier moments `m_(t,l)`. Positivity is essential. Integrating the Fejer kernel against `nu_t tensor nu_t`, retaining the nonnegative diagonal terms, and applying Cauchy--Schwarz to the atom weights gives

```text
q_t^2 + 2 Phi_t^(M) >= (M+1)q_t^2/K_t.
```

At `M=2k`, every cut with at most `k` positive-probability states has `Phi_t >= q_t^2/2`. This step is correct.

### 3.6 Summation and the occupation budget

The weighted harmonic-square sum is

```text
sum_(l=1)^(2k) (1-l/(2k+1)) l^2
    = k(k+1)(2k+1)/3 <= 2k^3.
```

Initial potential is `k`, total amplitude loss is at most one, and final potential is nonnegative. Summation gives the `9k^3` global budget. Each small cut contributes at least

```text
beta_(2k)(alpha) kappa^2/2,
```

which proves the stated constant `18`.

I found no missing dependence on the widths of the other cuts.

### 3.7 Terminal calibration

Combining the two binary coordinate decoders into `d=d_1+i d_2` gives `|d|<=sqrt(2)`. At seed `(1,1)`, the target correlation has modulus `sqrt(2)/10`. Uniform row-TV error `epsilon` changes each binary mean by at most `2epsilon`, so the complex error is at most `2sqrt(2)epsilon`. Therefore

```text
|E[Y_N d(S_N)]| >= sqrt(2)(1/10-2epsilon),
```

and `q_N>=1/10-2epsilon` follows. Only correctness at the prescribed final length is used.

### 3.8 Bounded-type and rational consequences

If `b_alpha=inf_l l ||l alpha||>0`, then for `l<=2K`,

```text
|sin(pi l alpha)| >= 2||l alpha|| >= b_alpha/K.
```

Substitution gives the fifth-root lower bound. The golden-angle norm calculation yields the advertised explicit constant.

For `zeta=(3+4i)/5`, nonvanishing of the Gaussian integer `(3+4i)^l-5^l` yields the exponential-in-`l` separation and the logarithmic width bound. This is valid, though extremely far from a matched asymptotic law.

### 3.9 The inherited upper construction

The resonant regular-polygon construction remains coherent. A convergent denominator `q` makes the residual angle `O(q^(-2))`; the radial expansion per step is `O(q^(-3))`; and choosing `q` of order `N^(1/3)` keeps the terminal decoder bounded. The idle and active rows are explicit stochastic rows and realize the conditional means exactly.

This proves the upper order in the declared atomic-row model. It does not show that a genuinely hidden lift cannot do better.

---

## 4. The central exponent gap is still the central theorem

Revision 34 changes the open problem from

```text
log N versus N^(1/3)
```

to

```text
N^(1/5) versus N^(1/3).
```

That is a substantial advance. It is not a solution of the compatible hidden-lift problem.

The fifth-root exponent arises from two losses:

1. the angular averaging estimate costs approximately `l^2`;
2. the Fejer witness for `k` atoms uses frequencies up to `2k`, while bounded-type separation contributes another inverse power of `k`.

The upper construction is vector-state. The manuscript gives neither:

- a hidden construction of order `N^(1/5)`;
- a lower bound of order `N^(1/3)` against arbitrary hidden states;
- a structural theorem proving that hidden states can or cannot improve the vector-state order;
- a classification of which simplex-section lifts can saturate the Fourier budget.

Thus the exact question that justified the compatible-lift reformulation in Revision 33 remains unanswered.

Even the explicit golden lower bound exceeds the separate minimum three only after

```text
N > 16200 * 3^5 = 3,936,600.
```

The constant is not itself an editorial defect, but it illustrates how far the present inequalities are from a sharp finite theory.

At four-journal level, one would expect a matched exponent, a sharp invariant, or a general theory that explains the gap. Revision 34 has none of these.

---

## 5. The most direct computational-model literature is missing

The manuscript describes its object almost entirely through positive realization, convex lifts, and comparison of experiments. That is only part of the natural classification.

For a fixed horizon, the machine is a layered nonuniform computation:

- layer `t` has `K_t` states;
- it reads one binary command;
- command `c` applies a row-stochastic transition matrix `T_(t,c)`;
- a terminal real-valued affine readout produces the two binary answer laws.

This is naturally a probabilistic, real-output generalization of an oblivious read-once branching program or probabilistic OBDD. The paper's proof is explicitly Fourier analytic, and the target is a cyclic phase/modular-sum statistic. Therefore the following literature is not optional background:

- O. Reingold, T. Steinke and S. Vadhan, *Pseudorandomness for Regular Branching Programs via Fourier Analysis*, RANDOM 2013, LNCS 8096, 655--670;
- T. Steinke, S. Vadhan and A. Wan, *Pseudorandomness and Fourier Growth Bounds for Width 3 Branching Programs*, Theory of Computing 13 (2017), Article 12, 1--50;
- C. H. Lee, E. Pyne and S. Vadhan, *Fourier Growth of Regular Branching Programs*, APPROX/RANDOM 2022, LIPIcs 245, Article 2;
- the standard OBDD/branching-program framework, for example I. Wegener, *Branching Programs and Binary Decision Diagrams*, SIAM, 2000.

These papers do **not** immediately imply Revision 34. Their principal models are deterministic, permutation, regular, or Boolean-output branching programs, whereas the manuscript permits arbitrary stochastic transitions and real terminal means. Their objectives concern Fourier growth and pseudorandomness rather than minimum width for exact conditional response laws.

That difference must be proved theorem by theorem, not assumed from terminology. The present bibliography does not even identify the comparison. As a result, the claimed originality of a Fourier width lower bound for a layered read-once finite-state model has not been adequately assessed.

The comparison should answer at least:

1. Which standard branching-program model exactly contains the manuscript's clocked transducers after allowing randomized transitions and real readout?
2. Can the two binary decoders be converted into one complex-valued branching-program output without changing width?
3. How does the manuscript's posterior-phase potential relate to standard matrix-valued Fourier coefficients and Fourier mass of a branching program?
4. Do existing generalized-group-product bounds imply any weaker or incomparable version of the occupation theorem?
5. Which feature of arbitrary row-stochastic transitions defeats regular/permutation branching-program methods?
6. Is the `N^(1/5)` bound a new stochastic-width hierarchy result in the OBDD sense, or only a positive-realization reformulation?

Until this comparison is supplied, the priority boundary is incomplete.

---

## 6. The circle-walk and Diophantine context is also incomplete

Under the proof's fair-command test law,

```text
L_t alpha mod 1
```

is a Bernoulli random walk on the circle. Its Fourier modes contract by

```text
(1+exp(-2 pi i l alpha))/2,
```

and the slow modes are governed by rational approximation of `alpha`.

This harmonic/arithmetic behavior is classical. A direct modern reference is I. Berkes and B. Borda, *Random walks on the circle and Diophantine approximation*, Journal of the London Mathematical Society 108 (2023), 409--440, which studies irrational and rational spans, best approximations, Fourier-analytic rates, and the transition between finite cyclic and circle behavior.

That paper does not study compression by a hidden finite register and does not supply the manuscript's occupation theorem. The new ingredient here is the information loss induced by stochastic coarse-graining and its use against a terminal correlation. Still, the underlying walk and its Diophantine Fourier damping should not appear without comparison to the probability literature.

A stronger exposition would separate three layers:

1. known Fourier behavior of the uncompressed circle walk;
2. the manuscript's new common-amplitude loss under hidden stochastic compression;
3. the finite-atom witness converting that loss into a width bound.

The current article does the second and third layers well but incompletely maps the first.

---

## 7. Assessment of the deficiency theorem

### 7.1 The one-step formula is classical and correctly labelled

For row-stochastic experiments `E` and `F`,

```text
delta(E,F)=min_T max_h TV((ET)_h,F_h)
```

is one-sided finite deficiency. The dual with a total row-oscillation budget is correct, and the zero-defect case is precisely finite Blackwell garbling. The triangle inequality follows by composing kernels and TV contraction.

The article now credits this lineage. This repairs a serious defect of Revision 33.

### 7.2 The diagram-to-machine construction is valid

At every command and terminal query, choose a common minimizing stochastic post-processing. Induction bounds the discrepancy between the actual state law and the proposed prefix-indexed law by the sum of preceding defects. The terminal decoder adds the final defect. Therefore the diagram gives an executable machine with output error at most `D(E)`.

### 7.3 The new lower bound is a corollary, not a new classification

Once the executable composition theorem is available, the diagram-defect lower bound follows by applying the Fourier width theorem with error `D(E)` and rearranging. It is useful because it rules out vanishing total certified defect for small-width diagrams of the main family.

However:

- `D(E)` is a sum of local worst-case deficiencies;
- it may substantially overestimate the best terminal error because local errors can cancel;
- the paper does not optimize globally over the proposed `E_t`;
- it does not define or determine an intrinsic dynamic deficiency equal to the optimal final simulation error;
- it supplies no matching low-defect construction at the fifth-root scale.

Thus this section is an operational reformulation of the main lower bound, not an independent top-level theorem of comparable depth.

---

## 8. Scope and resource model

The manuscript's model is mathematically legitimate, but unusually permissive if read as a memory-complexity theorem.

The counted resource is the number of persistent labels. The following are free:

- the external epoch;
- horizon-specific design;
- cut-dependent state spaces and transition matrices;
- exact sampling of arbitrary computable-real stochastic rows;
- read-only transition tables of unrestricted size;
- arithmetic and row-construction time;
- the final query symbol;
- a decoder tailored to the horizon.

Only one terminal query is answered. No uniform algorithm must construct the rows, and no autonomous device must recognize the stopping time.

These choices are appropriate for finite positive realization. They are not the conventional uniform computational meaning of streaming space or branching-program size. A comparison with branching-program literature must therefore state whether the relevant measure is width, total size, uniformity, description length, or random-bit complexity.

The rational fair-bit compiler in the preserved material uses extra sampler states and a self-paced interface. It does not identify atomic width with implementable bit space. The irrational resonant construction has no exact finite fair-bit compiler.

The title and abstract should make “clocked atomic stochastic-row width” impossible to overlook.

---

## 9. Fixed-length, anytime, cyclic, and equivariant comparisons

These sections are useful boundary markers but not central advances.

### 9.1 Exact cyclic closure

If one common stochastic matrix carries a finite cycle of experiments and the decoder sees a primitive `m`th root, the matrix has that root as a peripheral eigenvalue, so a recurrent class of period at least `m` is required. This is a standard finite Markov-chain spectral argument.

It does not apply to the finite irrational experiment with unrelated time-dependent matrices and no last-to-first closure. The article correctly says so.

### 9.2 Fixed-length autonomy

The inherited resonant construction already uses common command matrices, with a horizon-dependent decoder. Therefore fixed-length autonomous width has the same fifth-root lower and cube-root upper bounds as the clocked problem.

This does not determine its exact order.

### 9.3 Anytime autonomy

Requiring the same decoder to be correct after every length `0,...,N` is strictly stronger. Cayley--Hamilton gives the linear lower bound, and a counter construction gives a linear upper bound.

The article now distinguishes this from the fixed-length task. The result is correct but inherited and does not resolve the original problem.

### 9.4 Equivariant lifts

The manuscript accurately notes that a time-dependent chain of noninvertible stochastic maps is not the same object as one equivariant lift carrying a group action. Known equivariant polygon lower bounds therefore cannot simply be imported.

The new Fourier theorem is valuable precisely because it avoids imposing equivariance. Yet the remaining fifth-root/cube-root gap shows that the cost of dynamic compatibility is still not structurally understood.

---

## 10. The result is too specialized for the claimed foundational role

The new theorem is proved for a particularly clean family:

- a two-dimensional rotation;
- one Bernoulli command selecting identity or one fixed rotation;
- four seeds;
- two coordinate queries;
- binary outputs;
- a fixed small signal amplitude;
- bounded-type or one special rational-entry rotation.

This is an excellent test case. It is not a general theory of hidden causal memory.

The paper does not prove an analogous theorem for:

- higher-dimensional tori;
- several noncommuting command maps;
- general finite subsets of a compact group;
- arbitrary unitary representations or characters;
- hidden Markov output processes beyond one terminal linear statistic;
- general approximate experiment comparison;
- informative or adaptive action selection.

A genuinely foundational advance would identify a reusable invariant or theorem over a broad class. For example, a compact-abelian-group character theorem might explain the circle result as one-dimensional harmonic analysis rather than as a bespoke construction. Revision 34 does not attempt this.

---

## 11. Pipeline assessment

The repository-level dependency ledger has the principal chains

```text
A2 -> A3 -> A4 -> C2 -> D1
```

and

```text
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

Their gates concern branchwise Fourier/local-limit theory, stopped large deviations, unchanged global kernels, nonlinear semigroups, graph cores, filtering, optional projection, and typed contraction.

Revision 34 proves a local finite-register theorem for one rotation experiment. It does not discharge any of those gates. The manuscript's own `PIPELINE_STATUS.json` correctly leaves false:

- `historical_A2_replaced`;
- `B4_aggregate_closed`;
- `C2_aggregate_closed`;
- `eleven_paper_aggregate_closed`;
- `fully_adaptive_collision_solved`;
- `noisy_tag_composition_solved`;
- `sharp_hidden_rotation_width_solved`.

The new proof edges are internal:

```text
common amplitude loss
  -> homogeneous angular recursion
  -> finite Fourier occupation budget
  -> all-hidden rotation lower bound
  -> diagram deficiency obstruction.
```

That is a coherent local pipeline. It is not a bridge to the repository's main analytic DAG.

The 435-page and 988-page cumulative volumes preserve history. They do not increase the depth or relevance of the 13-page theorem. The compact referee package is the correct editorial object.

The title “General Theta Foundations I” remains misleading. Nothing in the focused paper explains a general theta foundation, and the status ledger expressly denies closure of the broader program.

---

## 12. Minimum changes before a credible specialist submission

These changes are not a route to top-four acceptance. They are the minimum for a fair independent specialist review.

### 12.1 Retitle and reposition

Remove “General Theta Foundations I.” A descriptive title should identify probabilistic branching-program width, hidden stochastic realization, or Fourier lower bounds for clocked transducers.

### 12.2 Add the branching-program comparison

Include a dedicated section mapping the machine model to probabilistic oblivious read-once branching programs. Compare assumptions, output conventions, width versus size, uniformity, stochastic versus deterministic transitions, and known Fourier-growth methods.

### 12.3 Add the circle-walk comparison

Explain which Fourier/Diophantine facts concern the uncompressed Bernoulli walk and which inequalities are genuinely caused by hidden-state compression.

### 12.4 Either close the exponent gap or reduce the claim

The strongest next advance would be one of:

- an `Omega(N^(1/3))` lower bound for arbitrary hidden states;
- an `O(N^(1/5))` genuinely hidden construction;
- a proof that hidden and vector-state widths have the same order;
- a structural characterization of diagrams saturating the Fourier budget;
- a separation showing that the two orders are genuinely different.

Without one of these, the paper should present `N^(1/5)` as the first polynomial unrestricted lower bound, not as a near-classification.

### 12.5 Generalize the harmonic method

State and prove a theorem for a broader class of compact-group or character-valued experiments, or explain why the method is intrinsically limited to the circle. This would materially strengthen the claim of conceptual depth.

### 12.6 Tighten the angular-lemma proof

Retain the exact `l(l-1)` coefficient before the final estimate so the displayed implication is transparent.

### 12.7 Clarify the deficiency objective

Use language such as “accumulated local deficiency certificate,” not wording that could be read as the intrinsic minimum final simulation error. Discuss cancellation and the absence of a global optimization theorem.

### 12.8 Keep implementation claims separate

Do not present exact atomic real kernels as finite random-bit algorithms. State table and arithmetic assumptions in every computational comparison.

### 12.9 Remove the cumulative archives from the submission

Keep them in the repository if desired, but submit only the focused article, response, core sources, and a modest reproducibility supplement.

### 12.10 Seek a specialist venue

Positive systems, stochastic automata, information/experiment comparison, or computational-complexity venues concerned with branching programs are the natural homes. A new specialist submission should not be framed as another internal step toward Annals/Inventiones/JAMS/Acta.

---

## 13. Specific major and minor points

1. Define explicitly whether `K_t` counts available or reachable states in every theorem. The occupation theorem can use positive-probability states under the test law, while `W_N` counts available labels.
2. State the exact equivalence or non-equivalence with a probabilistic OBDD in the introduction.
3. Explain why two real binary decoder means are the appropriate complex readout and how this compares with Boolean acceptance in branching-program work.
4. Add Reingold--Steinke--Vadhan, Steinke--Vadhan--Wan, and Lee--Pyne--Vadhan to the literature audit.
5. Add Berkes--Borda or another primary circle-random-walk reference.
6. Do not claim an exhaustive novelty boundary merely because the positive-realization and lift literatures are now cited.
7. Tighten Lemma `lem:angular34` as described above.
8. State whether the `l^2` angular loss is known to be sharp for the class of conditional mixtures that can arise from a stochastic register.
9. Discuss whether an alternative positive trigonometric kernel could improve the `k` dependence.
10. Explain whether using several test distributions or several terminal correlations can improve the fifth-root exponent.
11. Separate “badly approximable” from “bounded type” once and then use one terminology consistently.
12. The rational-entry rotation angle is irrational; “rational rotation” should always be explained as rational matrix entries, not rational angle.
13. The logarithm base `5000` is only a convenient coarse consequence. Do not give it rhetorical weight beyond explicitness.
14. State the exact threshold at which the polynomial lower bound beats the separate minimum, or avoid finite-scale rhetoric.
15. Clarify that the robust result fixes the signal amplitude `1/10`; it is not a uniform theorem as the amplitude tends to zero.
16. Explain whether the theorem extends to asymmetric command bias. The fair law is a proof choice, but the contraction coefficients and constants would change.
17. The deficiency dual is useful for convention fixing; keep it labelled classical.
18. Do not call `D(E)` the defect of the experiment without the modifier “accumulated local” or “diagram certificate.”
19. State explicitly that local deficiency cancellation is not ruled out.
20. The fixed-length autonomous upper construction uses a decoder depending on `N`; emphasize this in the theorem statement, not only prose.
21. Keep the anytime theorem out of the main novelty summary.
22. The cyclic proposition is a standard spectral lemma and should remain a comparison result.
23. Do not treat the number of internal revision rounds as independent peer review.
24. Do not use test volume, source hashes, or build receipts as evidence of mathematical significance.
25. Remove internal A2/B4/C2 labels from the focused article's mathematical conclusion; retain them only in repository status records.
26. Replace the Foundations title with a subject-specific title.
27. Add a neutral contribution table separating new, inherited, classical, and implementation statements.
28. State whether any lower-bound constant is optimized. The current constants are plainly proof constants.
29. Explain why the final one-query interface is the right notion for the intended application.
30. Do not imply that the theorem covers adaptive experimental design; the external command sequence is specified rather than optimized.

---

## 14. Scorecard

| Criterion | Assessment |
|---|---|
| Correctness in the stated model | Main new proof appears coherent; no short fatal counterexample found |
| Advance over Revision 33 | Substantial: unrestricted lower bound becomes polynomial and robust |
| Originality boundary | Incomplete; direct branching-program and circle-walk literatures are omitted |
| Mathematical depth | Serious specialist level, below four-journal general-mathematics level |
| Quantitative strength | `N^(1/5)` lower versus `N^(1/3)` upper; exact hidden order unresolved |
| Generality | One planar rotation family, binary commands, one terminal coordinate query |
| Computational model | Nonuniform clocked atomic stochastic rows; tables, arithmetic, and exact real sampling free |
| Deficiency result | Operationally useful but derivative and not an exact dynamic-distance theorem |
| Autonomous comparison | Correctly separated; fixed-length gap remains, anytime result is stronger-task and inherited |
| Pipeline impact | None on the decisive A2/B4/C2/D1 analytic gates |
| Presentation | Focused and much improved; branding still misleading |
| Reproducibility engineering | Strong, but irrelevant to proof, originality, and journal level |
| Editorial recommendation | Reject at top-four level; consider only after specialist repositioning |

---

## 15. Final assessment

Revision 34 is the strongest version of this project so far. It answers the previous report's most important mathematical objection. The hidden-state converse no longer relies on projected polygon vertices; the new conditional-phase measure sees the actual number of hidden states; and a common amplitude-loss budget produces a robust polynomial occupation bound. This is real mathematics and should be credited as such.

The paper nevertheless remains an opening result, not a completed theory.

The exact hidden width is unknown by a polynomial factor. The direct probabilistic branching-program literature has not been confronted. The underlying circle random walk is not situated in its probability-theoretic context. The deficiency theorem is a composed corollary rather than a characterization. The model is nonuniform and permissive. The theorem covers one structured planar family. The repository's main analytic pipeline remains open.

Put bluntly: **Revision 34 proves that arbitrary hidden lifts cannot collapse the rotation problem to logarithmic width, but it still does not determine what arbitrary hidden lifts can do.** That unresolved question is the paper's center, not a minor remainder.

My recommendation is therefore firm:

**Reject for Annals of Mathematics, Inventiones Mathematicae, Journal of the AMS, or Acta Mathematica.**

A retitled, literature-complete paper centered on Fourier lower bounds for probabilistic read-once transducers and dynamic Blackwell diagrams could merit serious specialist review. That would be a new editorial submission, not another internal revision under the claim that the manuscript is approaching the four-journal threshold.
