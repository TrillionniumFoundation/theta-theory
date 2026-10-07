# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r3-terminal-bridge-2026-10-07`  
**Reviewed exact artifact head:** `c2537e20cb9bc197956063334aa8a1240e6a5b41`  
**Native mathematical source:** `fb26f6588d08e7da7e48ec1c6503b8d319929977`  
**Read-only verification record:** `c553f1d8df2beefd1508f4364696f72e87934e41`  
**Canonical restart base:** `18000b21e4bfd89180ccb069e46ac0f21621f34d`  
**Reviewed r2 artifact:** `593c3f3077ef9565bcc4b71fdeed9c99287d23c2`  
**Previous external report:** `32350573ac91d4fbf2f79343622e43e4555dce2e`  
**Rendered-paper SHA-256:** `71becea64ab2288a40bf01f9863a2e311a88c89d5bbe9572a73642a893774b17`  
**Review branch:** `review/general-theta-restart-r3-terminal-bridge-external-top4-referee-r3-2026-10-07`  
**Date:** 7 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned decision of any named journal, and it is not an independent certification of priority, correctness, or acceptance.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not a technical-correctness rejection**. Revision r3 is a substantial and serious response to the preceding report. I did not find an elementary error that invalidates the principal new inequalities in the portions checked. In particular:

- the forward finite-error-measure induction in Theorem `thm:bridge`;
- the raw refresh-versus-expansion calculation in Proposition `prop:recharge-flow`;
- the arbitrary-center lower bound and countable allocation argument;
- the nonhomogeneous binary small-ball estimate and oscillatory quantization profile;
- the Fano/entropy retained-information converse in Theorem `thm:soft-state`;
- the exact risk decomposition and online overwrite construction in Theorem `thm:single-probe`; and
- the inherited quotient, finite-chart, positive-resolvent, causal-morphism, minimax, and realization chains

are internally coherent under the hypotheses stated in the manuscript.

The negative recommendation instead concerns **the depth, naturality, and structural breadth of the main theorem at the exceptional standard of the four leading general journals**.

The revision closes a genuine problem left by r2: it obtains terminal-component error control before dividing by terminal component mass. It also replaces finite chart geometry by a countable multiscale profile in one important class, softens the exact continuation-tag lower to an information converse, and gives a one-probe nonseparable minimax law. These are meaningful advances.

However, the strongest general theorem remains a sufficient certificate theorem. Its dynamic hypothesis either assumes the terminal-mass recharge inequality directly or derives it in a reset-preserved partition where every cross-component move erases old approximation error and where incoming refresh mass dominates expanding continuation flow component by component. The difficult general case—nonreset transport of old error among changing rare strata—is still outside the theorem. The countable singular realization is mathematically valid but deliberately engineered around revealed refreshes and strong recharge. The resource converses remain partial, and the one-probe coupling is an exact scalar fixed-protocol model rather than a broad recurrent exploration/calibration/compression theorem.

For a leading specialist journal in probability, mathematical statistics, stochastic control, information theory, nonlinear filtering, quantization, or applied probability, my outlook is **favorable after a focused substantial revision**. The manuscript is now much closer to a publishable specialist paper than r2. At the top-four general-journal level, changing the recommendation would require another genuinely broad theorem, not merely further polishing or additional examples.

---

## 1. Review object, provenance, and pipeline inspected

The revision and referee-ready branches point to the artifact head

```text
c2537e20cb9bc197956063334aa8a1240e6a5b41.
```

Its immediate parent

```text
fb26f6588d08e7da7e48ec1c6503b8d319929977
```

is the native mathematical source. The artifact child changes only `paper.pdf` and the build/regression evidence. The separate verification record at

```text
c553f1d8df2beefd1508f4364696f72e87934e41
```

records a successful read-only check of the artifact head without moving the referee snapshot.

I reviewed the submission as a mathematical pipeline rather than as an isolated PDF. The review included:

- `main.tex`, all numbered sections, the algorithm appendix, and the bibliography;
- the new terminal bridge, singular recurrence, noisy-state, and one-probe sections;
- `REFEREE_RESPONSE.md`, `THEOREM_MAP.md`, `PROOF_LEDGER.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `PIPELINE_DERIVATION.md`, `SCOPE_AUDIT.md`, `NOTATION_AUDIT.md`, `LITERATURE_COMPARISON.md`, and `HISTORY_COVERAGE.md`;
- the controlling restart charter, theorem targets F1–F4, the general-foundations outline, and the realization registry;
- the exact r2 subtree, the r2 external report, and the r3 point-by-point response;
- `SOURCE_MANIFEST.json`, `PUBLICATION_POLICY.json`, `build.py`, `verify.py`, both regression programs, and the committed verification evidence;
- the branch topology separating the canonical restart, research, revision, referee-ready, verification, and review lines.

The verification record reports:

```text
43 pages
27 formal statements
27 proof environments
121 labels
18 cited bibliography items
33 manifested source files
15 TeX source files
15,407 inherited finite checks
9,418 new finite checks
125 + 201 rejected negative controls
byte-identical independent rebuilds
identical ordinary and optimized regression outputs
```

These records provide useful source integrity, reproducibility, and finite-identity checks. They do not prove the continuum theorems, and the repository correctly states this.

The historical separation is also handled correctly. The r3 paper is a native restart revision. It does not silently continue the frozen v1–v96 numbering, does not overwrite the old archive, and does not promote an ordered-measurement or HMM realization into the role of the general theorem.

---

## 2. Executive assessment of the r3 revision

The previous report identified five possible directions that could materially change the assessment. Revision r3 makes real progress on four of them.

| Previous structural request | r3 assessment |
|---|---|
| **A multi-chart recurrent acquisition theorem deriving terminal mass rather than normalizing by it** | **Materially advanced, but not fully closed.** Theorem `thm:bridge` propagates error measures against the actual forward laws, and `prop:recharge-flow` supplies a nonstationary countable-component class. The remaining limitation is essential: non-overwrite transitions preserve their component, and every component change is an overwrite. General nonreset cross-stratum transport is still open. |
| **A natural coupled minimax model** | **Partially answered.** Theorem `thm:single-probe` uses one hidden scalar and one Bernoulli task, so acquisition, memory, packet precision, thinning, and calibration act on the same quantity. This is a genuine improvement over an independently selected terminal menu. It remains a scalar, known-kernel, fixed-action experiment and does not couple recurrent instability, adaptive exploration, simulator state, and calibration learning. |
| **A true multi-resource converse** | **Partially advanced.** Theorem `thm:soft-state` replaces exact support separation by a retained-information cut and charges surviving workspace bits. It is a meaningful converse for fused randomized states. It does not give a matching upper for every error level or characterize program length, transient workspace, runtime, pilot cost, or calibration acquisition. |
| **A multiscale singular-geometry theorem** | **Substantially answered for a scale-separated class.** The new `(MG)` condition allows finitely or countably many components, arbitrary-center small-ball bounds, approximate allocations, and oscillatory profiles without a limiting dimension. Arbitrary countable intersecting accumulations and general singular measures remain outside the theorem. |
| **Adaptive exploration or unknown-kernel learning** | **Open.** The main matching laws still fix the exploration independently of the encoder, use known protocol data, and work at deterministic horizons. |

The revised editorial question is therefore no longer whether the paper contains a real theorem chain. It does. The question is whether the strongest theorem has sufficient breadth and intrinsic depth for a four-leading-general-journal contribution. In my view it does not yet meet that threshold.

---

## 3. Summary of the revised contribution

The paper begins with a prepared causal experiment on standard Borel spaces. Legal actions, reports, stopping conventions, and resource increments are part of the visible interface. Executable future tests determine predictive equivalence. Under either a compact instrument certificate or an explicit Borel realization, the predictive quotient has declared pointwise update versions without division by zero-probability report events.

For a finite squared-prediction menu, the terminal full-history conditional prediction vector has actual acquired law. A checkpoint encoder retains at most `M` labels after the history; an online encoder updates at most `M` persistent labels recursively and cannot reread discarded reports. Conditional projection reduces checkpoint excess risk to ordinary quadratic quantization of the actual score law.

The inherited finite-chart theorem treats anisotropic component charts, actual conditional density bounds, online innovation recurrences, positive moment transport, and exact versus finite-precision implementation. The new r3 theorem replaces the finite-chart geometry by a profile

```text
Q_N(M)
  = inf_{sum_j k_j <= M}
      sum_j w_{N,j} r_j(k_j)^2,
```

where `w_{N,j}` are actual terminal component masses and `r_j(k)` are verified cover/small-ball scales.

The new dynamic device is a finite error measure

```text
E_{t,j}(C)
  = E[e_t^2 ; Z_t in C cap D_j].
```

On non-overwrite edges, old error remains in the same component. Overwrites kill old error. A positive old-error kernel `A_{t,j}` and a forcing kernel `F_{t,j}` satisfy the one-step recharge inequality

```text
(v_{t-1,j} mu_{t-1}^j) A_{t,j}
  + mu_{t-1} F_{t,j}
  <= v_{t,j} mu_t^j,
```

with `1 <= v_{t,j} <= V`. Positive induction gives

```text
E_{t,j} <= R_j^2 v_{t,j} mu_t^j,
```

and hence a terminal conditional error bound with no inverse terminal mass. Combined with the multiscale lower, this yields

```text
B_N + c Q_N(M)
  <= R_cp(N,M)
  <= R_on(N,M)
  <= B_N + C V Q_N(M).
```

A raw-flow proposition verifies the recharge inequality when holds, within-component continuations, and state-revealing refreshes have known probabilities and when refresh flow into every component dominates its expanding continuation flow.

The countable singular realization uses nonhomogeneous binary product measures on infinitely many scale-separated components accumulating at an anchor. It gives checkpoint and online risks with an oscillatory quantization profile for which no limiting power-law dimension exists.

The resource layer retains causal morphisms and a full implementation ledger. The new noisy continuation theorem proves that approximate recovery of a latent continuation tag consumes retained mutual information that otherwise could resolve an anisotropic target. The one-probe theorem computes an exact common-oracle minimax risk in which acquisition failure, finite memory, packet precision, calibration ambiguity, and report thinning act on the same Bernoulli mean.

---

## 4. Assessment against the controlling targets F1–F4

### F1 — Causal acquired-geometry transfer

**Achieved for a substantial certified class.**

Theorem `thm:bridge` is a genuine class theorem. Its lower bound uses actual terminal conditional laws and arbitrary decoder centers. Its upper bound is realized by an executable recursive label machine. The same terminal masses appear in the geometric profile and in the error-measure domination. No optimum is assumed as a hypothesis.

The qualification is that `(TB)` is close to the exact domination needed by the proof, and the raw sufficient condition is structurally restrictive. Thus F1 is met as a transfer theorem, not as a general characterization of when causal acquired geometry admits matching online resolution.

### F2 — Resource–resolution–risk composition

**Achieved constructively and in selected converses, not as a universal full-vector law.**

The causal-morphism theorem carries raw acquisitions, representative states, simulator states, controller states, phase states, workspace, program data, calibration precision, numerical precision, and physical time. It separates pathwise, mean, and tail semantics and measures complete interactive defects on the loss-relevant transcript.

The exact tag theorem, noisy retained-information theorem, robust minimax family, and one-probe family provide real lower bounds. They do not yet characterize the optimum across the entire resource vector for a broad experiment class.

### F3 — Singular or nonuniform extension

**Achieved in a meaningful, nontrivial sense.**

The paper now contains:

- finite intersecting and rank-changing strata;
- recurrent expansion governed by a positive second-moment operator;
- countably many accumulating components;
- nonhomogeneous singular product measures;
- arbitrarily long exact waits;
- nonstationary component masses; and
- an oscillatory quantization profile without a limiting dimension.

This is far beyond a fixed finite designed ensemble. The remaining boundary is that the countable theorem requires relative scale separation and the recurrent multi-component route resets old error whenever the component changes.

### F4 — Distinct raw-kernel realizations

**Achieved.**

The binary nonlinear filter, absorbing stratified sensor, recurrent fold/refresh process, and countable singular shift/refresh process are structurally different. Their quotient, actual-law, update, and implementation hypotheses are verified from raw kernels. None is used as a premise of the general theorem.

---

## 5. Audit of the new terminal-mass theorem

### 5.1 Multiscale geometry

Condition `(MG)` separates four ingredients that are often conflated:

1. actual terminal component weights;
2. valid online cover radii;
3. arbitrary-center small-ball upper bounds for the terminal score laws; and
4. relative scale separation of score neighborhoods.

The countable profile uses finite-support allocations automatically, since the total integer budget is finite. The infimum need not be attained. The one-label regularity inequality

```text
Q_N(M-1) <= D_r Q_N(M)
```

is correctly proved by removing one representative from an approximate allocation, using `r_j(0)=r_j(1)` at a singleton allocation and the displayed regularity for larger allocations.

The geometric lower correctly handles off-support centers. Pairwise disjoint component neighborhoods assign each decoder center to at most one component. Unassigned centers remain farther than the lower radius. The union of `k_j` score balls has conditional mass at most one half, and the complement yields a distortion of order `r_j(k_j)^2`. Summation uses the actual masses.

This is a useful extension of the finite-chart lower. It is still a certificate: the small-ball and separation profile must be separately verified.

### 5.2 Error-measure induction

The key new idea is to propagate `E_{t,j}` as a measure rather than to control only an unconditional second moment.

Under the stated Markov-factor condition, the next analysis mark is conditionally independent of retained approximation error given the factor. Young's inequality gives

```text
e_t^2
 <= (1+eta) g_t^2 e_{t-1}^2
    + (1+eta^{-1}) b_t^2 R_j^2
```

on non-holds. Holds copy exactly. Overwrites set the old-error coefficient to zero. Because every non-overwrite transition preserves the component, no incoming old error from another component is omitted. These facts yield the measure recursion

```text
E_{t,j}
 <= E_{t-1,j} A_{t,j}
    + R_j^2 mu_{t-1} F_{t,j}.
```

Positivity and `(TB)` then give

```text
E_{t,j} <= R_j^2 v_{t,j} mu_t^j
```

by induction. Countable summation is justified by monotone convergence. A component of zero terminal mass automatically receives zero terminal error measure. This successfully removes the inverse-rare-component normalization problem present in the stationary matrix route.

I find this proof correct under the declared hypotheses.

### 5.3 Nature of the recharge hypothesis

The main limitation is not a hidden algebraic gap; it is the strength and geometry of `(TB)`.

The theorem permits cross-component entry only through an overwrite that destroys dependence on the previous exact state. A non-overwrite edge is required to stay in the same component. Thus the error-measure vector is diagonal in the old-error channel. General transitions carrying nonzero old approximation error from component `i` to component `j` require a matrix-valued balance and are explicitly excluded.

Moreover, `(TB)` itself is an allocation-independent domination of precisely the forcing and old-error measures that appear in the desired induction. This is an acceptable theorem hypothesis, but it means the theorem is a transfer principle rather than a structural classification.

---

## 6. Audit of the raw refresh-flow proposition

The algebra in Proposition `prop:recharge-flow` is consistent.

Writing

```text
x = u_t w_{t-1,j},
y = v_t pi_{t,j},
A_G = max{(1+eta)G^2-1,0},
C_b = (1+eta^{-1}) b_*^2,
```

the difference between the target measure `D w_{t,j} sigma_j` and the proposed upper bound is

```text
[(D-C_b)y - (D A_G + C_b)x] sigma_j.
```

Under `y >= Kx`, `K>A_G`, the displayed choice

```text
D >= C_b (K+1)/(K-A_G)
```

makes this nonnegative. Holds cancel exactly, and the constant remains finite as activity or terminal component mass tends to zero.

This is a real answer to the rare-terminal-mass objection. The proposition allows nonstationary component weights, creation of new strata, and arbitrarily long exact waiting periods.

Its structural meaning should nevertheless be stated even more prominently. For each component, incoming refresh mass must dominate the expanding within-component flow. In the countable singular example with `eta=1` and `G=15`, one needs `K>449`; the displayed concrete choice uses `K=500` and an active refresh-to-expansion probability ratio of `2000`. Expansions recur, but the example is strongly recharge dominated. This does not diminish correctness; it limits how broadly the result represents naturally recurrent transport.

---

## 7. Audit of the countable singular realization

The nonhomogeneous binary construction is internally coherent.

For contraction ratios in `[1/5,1/3]`, length-`n` cylinders have mass `2^{-n}` and diameter `ell_n`. Choosing one representative per level-`n` cylinder gives the cover. A ball of diameter `ell_n/50` meets at most one level-`n+2` cylinder because the first differing digit creates a gap of at least `ell_n/15`. This gives the arbitrary-center small-ball bound. The profile changes by at most a factor `25` when the budget crosses a dyadic threshold.

The digit shift preserves the fair product law and is globally `15`-Lipschitz in the nonhomogeneous coding. Scaling copies of this set by `a_j=10^{-(j+2)}` produces disjoint score neighborhoods accumulating at the anchor.

The online machine is explicit. An allocated component stores a component/prefix pair as one label; holds copy; expansion shifts the word; refresh overwrites from the revealed new prefix; unallocated components use the common anchor. No latent analytic component mark is supplied to the decoder. The raw integration gives the actual acquired mixture.

The alternating superexponential blocks of ratios `1/3` and `1/5` produce two distinct subsequential logarithmic slopes, so the quantization profile has no limiting exponent. Uniform multiplicative constants do not change this conclusion.

This is a nontrivial F3 realization. At the same time, it is designed to fit the diagonal recharge mechanism: the only cross-component moves are fresh state-revealing resets. It does not settle recurrent nonreset movement through an accumulating stratification.

---

## 8. Audit of the retained-information converse

Theorem `thm:soft-state` is a clean and useful extension of the exact continuation-tag theorem.

Fano's inequality in the stated range gives

```text
I(C;S | R) >= f_L(eta).
```

Since the complete retained state has at most `M` values conditional on the independent seed,

```text
I(U;S | C,R) <= log M - f_L(eta).
```

For the first `l` anisotropic coordinates, the uniform prior entropy and the Gaussian maximum-entropy inequality imply

```text
D >= [l/(2 pi e)]
     (prod_{i<=l} a_i)^(2/l)
     exp{2(f_L(eta)-log M)/l}.
```

Taking the maximum over `l` is valid. Surviving workspace bits enlarge the retained alphabet by `2^W`; erased workspace carries no information across the cut. The theorem applies to fused randomized state and does not rely on a preferred product-register decomposition.

The limitation is explicit: this is a lower bound only. There is no general matching noisy-tag upper over all `eta`, `M`, and anisotropies, and no implication for registers that are not distinguished by an executable continuation.

---

## 9. Audit of the one-probe minimax theorem

Theorem `thm:single-probe` is the strongest conceptual response to the previous objection that the robust family was a direct sum of independent terminal blocks.

The oracle risk

```text
b_* = 1/4 - a^2/12 - delta^2
```

is correct for the Bernoulli mean `1/2+U+theta`. Averaging the two calibration signs removes the cross term and forces the `delta^2` contribution. Conditional projection separates:

- unresolved variance on no acquisition;
- within-packet cell variance after acquisition; and
- finite-state quantization of the posterior-mean distribution.

This yields the exact formula

```text
delta^2
 + h a^2/12
 + (1-h) a^2/(12L^2)
 + q_M(h delta_0 + (1-h)L^{-1} sum_l delta_{u_l}).
```

The online implementation starts at the label assigned to zero, overwrites after the first success, and copies on every later erasure symbol. Absorption makes a separate retained success flag unnecessary. The resulting scale

```text
delta^2
 + a^2 [ h + (1-h)(M^{-2}+2^{-2b}) ]
```

is correct up to universal constants.

The fixed-time packet deficiency calculation is also correct. The report-thinning complete-path quantity is properly presented only as an upper certificate, not as an exact causal deficiency.

This theorem gives a genuine nonseparable effect because the acquired mass `1-h` weights both memory and packet resolution while the complementary mass produces unresolved variance. It remains an elementary scalar, fixed-protocol, known-interface experiment. It does not yet show how recurrent instability, exploration, calibration learning, simulator state, and memory resolution interact in a natural broad class.

---

## 10. The inherited theorem chain

The inherited parts remain important and, in the portions checked, coherent.

### Predictive quotient

The completed-measurability factorization and compact instrument descent avoid null-event Bayes division. Pointwise descent at positive-density reports follows from event-instrument closure, uniqueness of signed measures, continuity, and full support. Zero-density values are used only through separately declared fibre-compatible extensions.

### Finite anisotropic geometry

The checkpoint projection is standard and correct. The finite-chart upper uses explicit anisotropic product grids. The actual-density small-ball lower permits arbitrary decoder centers. Widths can vanish without entering denominators, and the finite intersecting-stratum corollary does not require a positive separation distance.

### Positive forced moments

The reverse-edge first- and second-moment recursions and their positive resolvents are correct under stationary environment preparation and the one-step Lyapunov inequality. Exact state-independent suspension cancels in the fixed-point equations while remaining in the physical resource ledger. In multiple charts, however, the normalized matrix can still diverge when forcing energy is not commensurate with terminal masses; the new bridge theorem closes only the reset-preserved forward-flow class.

### Causal morphisms

The morphism data include legal controller lifts, causal microsteps, stopping indices, clocks, costs, terminal readouts, complete transcript defects, and monotone resource maps. Composition is the correct total-variation triangle/data-processing argument on compatible controller classes. The result is principally a well-typed constructive upper theorem, not a general optimal-resource converse.

### Realizations

The binary filter derives an actual posterior-density upper and a uniform one-dimensional law. The absorbing sensor treats intersecting finite strata and rank collapse. The recurrent fold/refresh model exercises the positive moment theorem with active gains `2` and `1/4` and second moment `73/160<1`. These are genuinely different raw experiments.

---

## 11. Why the top-four threshold is still not met

### 11.1 The central theorem is sufficient rather than intrinsic

The paper's deepest conceptual claim is that actual acquisition mass and causal approximation transport must be controlled together. Theorem `thm:bridge` implements this insight elegantly, but the coupling is encoded in `(TB)`. The raw theorem verifies `(TB)` only for a diagonal old-error flow with resets on component changes.

A top-four-level foundational result would more plausibly characterize a broad class of raw kernels through an intrinsic matrix or operator condition that permits nonreset transitions among rare strata and derives the terminal weights rather than assuming a componentwise domination tailored to the proof.

### 11.2 The main countable realization is engineered around the sufficient condition

The singular realization is not trivial, and the no-dimension conclusion is genuine. Nevertheless the dynamics are designed so that refresh reveals a fresh state, kills old error, and supplies enough incoming mass to dominate expansion. The displayed quantitative regime is strongly refresh dominated.

A natural stochastic filtering, partially observed control, random dynamical, or interacting-stratum model satisfying a nontrivial multi-component bridge would materially strengthen the paper.

### 11.3 The resource theory remains asymmetric

The full ledger is impressive as an accounting language, but most coordinates receive constructive upper bounds rather than matching lower laws. Persistent information is lower-bounded through exact or noisy executable challenges. Program length, transient workspace, runtime, pilot acquisition, and calibration acquisition remain generally unclassified.

The one-probe theorem and robust family show that several terms can coexist. They do not establish a universal resource–resolution region.

### 11.4 Fixed exploration and known protocol data remain essential

The main risks are evaluated under an exploration fixed independently of the encoder. The recharge probabilities, refresh distributions, scales, and effective prefixes are known protocol data. Unknown-kernel learning, pilot design, adaptive exploration, and joint acquisition/compression optimization are outside the theorem.

This scope is mathematically legitimate, but narrower than the word “Foundations” and the top-four venue suggest.

### 11.5 The geometry is broad but still separated and certified

Countably many components and oscillating scales are substantial improvements. Yet the lower requires disjoint relative-scale neighborhoods, and the upper requires valid covers and executable local rules. Arbitrary countable intersections, overlapping singular measures, and dynamically changing nonidentifiable strata are not covered.

### 11.6 No single theorem dominates the architecture

The manuscript combines:

- predictive quotient descent;
- actual-law quantization;
- a forward error-measure bridge;
- a refresh-flow sufficient condition;
- countable Moran geometry;
- positive forced moments;
- causal experiment comparison;
- information cuts;
- exact scalar minimax calculations; and
- several realizations.

The synthesis is thoughtful. Many constituent arguments are classical or elementary once their certificates are supplied. The paper still lacks one theorem with the breadth, surprise, and difficulty normally associated with the four leading general journals.

---

## 12. Revisions recommended before a specialist submission

These requests would substantially improve the paper, although they would not alone change the top-four recommendation.

### 12.1 Recenter the article around the terminal bridge

The introduction should state plainly that the main new theorem is the forward finite-error-measure bridge and that the principal verifiable class is a reset-preserved nonstationary partition. The inherited finite-chart theorem, stationary resolvent, resource framework, and minimax examples should be presented as supporting branches.

At present the number of parallel mechanisms makes it difficult to identify the dominant mathematical contribution.

### 12.2 State the structural limitation at theorem level

The phrases

```text
non-overwrite transitions preserve the component
```

and

```text
component changes are overwrites
```

should appear in a boxed or otherwise prominent hypothesis summary. They are not minor implementation details; they determine the scope of the terminal-mass mechanism.

Likewise, the raw-flow proposition should explain immediately that the displayed inequality is an incoming-refresh-versus-expansion domination, not merely a generic recurrence condition.

### 12.3 Separate exact Borel, effective finite-input, and complexity results

The paper now distinguishes these models correctly, but several theorem statements still carry all three layers at once. A clearer presentation would use:

1. an exact Borel finite-label theorem;
2. a finite-input stability corollary with explicit metric errors; and
3. model-specific complexity propositions where algorithms and bit costs are actually supplied.

### 12.4 Strengthen theorem-level literature positioning

The comparison section is candid, but the bibliography remains selective for a paper advertised as a foundation. Before specialist submission, the authors should make a more systematic theorem-by-theorem comparison in:

- causal/predictive-state minimality;
- finite-state and quantized nonlinear filtering;
- rate-distortion and sequential quantization;
- Markov jump affine recursions and regenerative systems;
- singular and Moran-measure quantization;
- information-constrained control and finite-memory policies;
- automata/state complexity; and
- Le Cam/Blackwell experiment comparison with implementation constraints.

The goal is not a broad survey. It is to identify exactly which combined theorem is new and which parts are classical tools.

### 12.5 Simplify notation and indexing

The notation audit correctly records several local collisions, but the article reader still encounters:

- `v_{t,j}` as recharge densities and `v_t` as refresh probability;
- `rho_n` as geometric contraction and `rho` as report thinning;
- multiple meanings of `N` across initialized recurrence and attempt protocols;
- `xi_j` as local precision allowance and `xi_t` as an environment variable.

These are legal but unnecessarily costly in a 43-page paper. Renaming at least the recharge weight and raw refresh probability would help.

### 12.6 Clarify the effective countable input interface

In the exact Borel singular model, a refresh can reveal a countable component index and an infinite digit sequence. The finite-input discussion correctly truncates this through a declared primitive, active component set, prefix depths, and tail certificate. This distinction should be moved closer to Theorem `thm:moran`, so that no reader mistakes the Borel label result for a finite-bit implementation with free infinite input.

### 12.7 Distinguish the three notions of thinning error visually

The manuscript correctly separates:

1. the raw single-call thinning parameter;
2. a complete finite-horizon path-law upper allowance; and
3. the exact fixed-time packet deficiency.

These should receive distinct notation in the theorem statements and a short comparison table. They answer different experiment-comparison questions.

### 12.8 Shorten the architecture where possible

The paper is mathematically richer than r2, but it has also grown from 31 to 43 pages. Some inherited framework material and the direct-sum robust family may be better compressed or moved to an appendix/companion treatment so that the new bridge theorem and its realizations receive the conceptual space they need.

---

## 13. What would change the top-four assessment

A future revision could materially change the recommendation if it supplied at least one theorem of the following kind.

1. **Matrix-valued nonreset terminal transport.**  
   Derive a forward measure inequality for old error moving among multiple rare strata, with constants controlled by raw nonstationary kernels and without reset on every component transition.

2. **A natural recurrent singular model.**  
   Verify such a theorem in a model not designed around revealed refreshes—for example a nonlinear filter, partially observed controlled process, random dynamical system, or stratified diffusion with genuine cross-stratum memory.

3. **A broad coupled minimax theorem.**  
   Prove a sharp law in which exploration, calibration learning, recurrent transport, causal simulation, and memory resolution interact within one dynamics and cannot be decomposed into scalar or terminal blocks.

4. **A matched multi-resource region.**  
   Establish a nontrivial state–workspace–time, state–program, or pilot–calibration tradeoff for a broad experiment class, with both constructive upper and decision/information lower bounds.

5. **Adaptive acquisition.**  
   Optimize or lower-bound the joint policy that acquires the predictive geometry and compresses it, with unknown kernels, pilots, failed calls, and stopping information fully charged.

6. **Overlapping countable singular geometry.**  
   Replace relative scale separation by a broad multiscale overlap condition while retaining arbitrary-center checkpoint lower bounds and executable online upper bounds.

Any one of these, carried through at the present level of care, would be a major paper-level advance. Without such a theorem, further examples and editorial refinement would strengthen a specialist submission but would not alter the general-journal scale.

---

## 14. Minor and technical comments

1. In Theorem `thm:bridge`, give the Markov factor and algorithm state different letters throughout; the suppressed extra coordinates make the first reading harder than necessary.
2. Define explicitly whether all component sets are subsets of the factor space or their predictive-coordinate projections; the current text explains this, but only after notation is introduced.
3. In `(MG)`, state once that `r_j(k) <= a_j` follows from monotonicity and `r_j(1)=a_j`; this is used in the separation lower.
4. In the geometric lower, name the center-assignment map. The proof is correct, but the countable case becomes easier to follow when this map is explicit.
5. In `(TB)`, use a symbol other than `v` for recharge densities because `v_t` is immediately reused for refresh probability.
6. In `prop:recharge-flow`, display the special case `x=y=0` in the theorem statement or a remark; this is the reason exact long waits cost no inverse activity.
7. Quantify the strength of the example condition near the example itself: with `eta=1`, `G=15`, one needs `K>449`.
8. In Theorem `thm:moran`, state in the theorem line that a component-changing report reveals the fresh state and is an overwrite.
9. The finite-bit paragraph after Theorem `thm:moran` should specify whether the current component index has bounded packet length on the active finite set.
10. In Corollary `cor:no-dimension`, call the two subsequential slopes “quantization exponents” only with the sign convention made explicit.
11. In Theorem `thm:soft-state`, repeat that `D` is the total Euclidean mean squared distortion, so use of the same `D` for every coordinate prefix is transparent.
12. State the conversion from the unscaled `U` distortion to the prediction loss in a separate corollary or remark.
13. In Theorem `thm:single-probe`, distinguish the packet cell count `L=2^b` from the continuation-tag size `L` used elsewhere.
14. The exact formula in `thm:single-probe` is stronger than the asymptotic law and deserves to appear before the `asymp` statement.
15. In the thinning subsection, label the complete-law bound explicitly as a nonoptimal simulator certificate.
16. Keep the total-variation convention adjacent to Proposition `prop:terminal-deficiency`.
17. In the recurrent fold/refresh theorem, repeat that the terminal Bernoulli probe is an additional paid call beyond the preforecast indexing.
18. In the abstract, the phrase “one-step recharge inequality yields terminal-component error bounds” is accurate; add “under reset-preserved cross-component transitions” to avoid overreading.
19. The title “General Theta Foundations I” is a project title. A specialist submission would benefit from a descriptive title led by the mathematical theorem, such as *Terminal acquired-mass bounds for causal finite-memory quantization*.
20. The article should preserve its current candor that successful compilation and regression do not certify continuum mathematics.

---

## 15. Positive assessment

The negative top-four recommendation should not obscure how much the paper has improved.

- The revision responds directly to the latest report rather than relabeling an old manuscript.
- It solves the rare-terminal-normalization problem for a real nonstationary reset-preserved class.
- It propagates finite error measures against actual forward laws rather than against a formal reachable envelope.
- It treats countably many accumulating components and an oscillatory singular profile without a limiting dimension.
- It proves its lower bound for arbitrary decoder centers and nonattained countable allocations.
- It keeps zero-mass components, exact holds, null reports, shared randomness, timing channels, and finite-input interfaces logically separate.
- It advances the exact continuation-tag lower to a noisy retained-information converse.
- It replaces the direct-sum objection with an exact one-probe coupling on a common physical quantity.
- It retains a full causal/resource ledger without falsely claiming that every constructive register is universally necessary.
- It separates the canonical general theorem from archived model-specific realization lines.
- Its scope audit openly records the remaining mathematical responsibilities.

This is the strongest and most coherent restart revision I have reviewed. It is a serious mathematical manuscript with a clear specialist-journal future.

---

## 16. Final recommendation to the editor

**Decision: reject for a four-leading-general-journal venue.**

**Reason:** Revision r3 contains a correct-looking and genuinely new terminal error-measure bridge, a meaningful countable singular extension, and improved resource converses. Nevertheless the central dynamic theorem remains a sufficient certificate whose main verifiable multi-component class resets old error at every component change and requires componentwise refresh to dominate expansion. General nonreset cross-stratum transport, adaptive acquisition, and a matched full-resource region remain open. The strongest coupled minimax theorem is exact but scalar and fixed-protocol. The combined architecture is substantial, but no single result yet has the breadth and depth expected at this venue.

**Specialist-journal outlook:** favorable after a focused substantial revision that sharpens the central novelty, foregrounds the reset-preserved scope, strengthens prior-art comparison, and streamlines the exact-Borel/finite-input/resource layers.
