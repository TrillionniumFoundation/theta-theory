# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r4-causal-resolvent-2026-10-07`  
**Reviewed exact referee-ready head:** `7c5012b308d3cdd5514913db7d16f6d25545d82b`  
**Reviewed artifact commit:** `ed677d9e7060e0e0eee283b3ac93e0542029aa89`  
**Native mathematical source:** `e00ab7e7be3d55a9ef47326264a8d40a7169804b`  
**Predecessor source:** `fb26f6588d08e7da7e48ec1c6503b8d319929977`  
**Previous external report:** `f458dbd31fcbe894dadf3f4610c3d7d623298f0c`  
**Canonical restart base recorded by the submission:** `18000b21e4bfd89180ccb069e46ac0f21621f34d`  
**Rendered-paper SHA-256:** `60ae917c12135be8076a96a9e01419ace29398c417be064cd622bda77e33b005`  
**Review branch:** `review/general-theta-restart-r4-causal-resolvent-external-top4-referee-r4-2026-10-07`  
**Date:** 7 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned decision of any named journal, and it is not an independent certification of priority, formal correctness, or acceptance.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This recommendation is **not a technical-correctness rejection**. Revision r4 is the strongest version of this project that I have reviewed. It directly answers the principal structural objection in the r3 report: the new central theorem permits old approximation error to cross predictive strata without being erased, and its proof controls that error before any normalization by rare terminal component masses. I did not find an elementary error that invalidates the central nonreset inequality or the two new model calculations in the portions checked.

More specifically, the following load-bearing arguments appear internally coherent under their stated hypotheses:

- the finite-overlap arbitrary-center small-ball lower bound in Lemma `lem:nr-overlap`;
- the marked-kernel weighted-energy recursion in Lemma `lem:nr-energy`;
- the exact treatment of deterministic independent suspension in equation `eq:nr-mixture`;
- the invariant-reference occupation comparison in Proposition `prop:nr-reference`;
- the positive gain-matrix criterion in Proposition `prop:nr-matrix`;
- the non-erasing singular symbolic calculation in Theorem `thm:nr-moran`;
- the atomic actual-law and common-oracle decomposition in Proposition `prop:nr-acquisition`;
- the finite-read acquired-depth law in Theorem `thm:recurrent-acquisition`; and
- the inherited quotient, resource-morphism, minimax, information-converse, finite-chart, reset-preserved, and realization results, subject to their original hypotheses.

The negative top-four recommendation instead concerns **mathematical level, intrinsic breadth, naturality, and the concentration of the main novelty**. The new theorem is a useful and nontrivial sufficient certificate. Its generality is real. Nevertheless, the hard recursive implementation is substantially encoded in hypothesis `(L)`, the actual-law comparison is substantially encoded in `(O)`, and the principal raw verification mechanism combines a standard positive-moment drift with a common invariant reference and two-sided preparation-density bounds. The manuscript does not yet extract an intrinsic characterization of finite-memory predictability, solve an established hard problem in a natural stochastic model, or obtain a matched region for the full resource vector advertised by the foundational programme.

At the level of a strong specialist journal in probability, mathematical statistics, information theory, stochastic control, nonlinear filtering, quantization, or applied probability, my outlook is **favorable after a focused substantial revision**. Revision r4 has crossed an important threshold: the central theorem is no longer confined to reset-preserved cross-component dynamics, and the finite-read model genuinely couples acquisition and memory in one actual predictive law. The remaining objections are therefore substantially more editorial and structural than those in r3.

---

## 1. Review object, provenance, and pipeline inspected

The referee-ready branch is pinned to the read-only verification commit

```text
7c5012b308d3cdd5514913db7d16f6d25545d82b.
```

That verification record binds the rendered artifact

```text
ed677d9e7060e0e0eee283b3ac93e0542029aa89
```

to the native source

```text
e00ab7e7be3d55a9ef47326264a8d40a7169804b.
```

The artifact commit adds only the rendered PDF and build/regression receipts to the native source. The review therefore concerns a fixed mathematical source, a fixed rendered paper, and a separate immutable verification receipt rather than a moving working branch.

I reviewed the submission as a mathematical and provenance pipeline rather than as an isolated PDF. The inspection included:

- `main.tex` and all eighteen TeX source files;
- the new central section `sections/02_nonreset_transfer.tex`;
- the new singular realization `sections/07_nonreset_moran.tex`;
- the new finite-read model `sections/07_recurrent_acquisition.tex`;
- the quotient, resource, realization, comparison, minimax, and algorithm sections;
- `REFEREE_RESPONSE.md`, `THEOREM_MAP.md`, `PROOF_LEDGER.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `PIPELINE_DERIVATION.md`, `SCOPE_AUDIT.md`, `NOTATION_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, and `INHERITANCE.json`;
- the controlling `RESTART_CHARTER.md`, `THEOREM_TARGETS.md`, the general-foundations outline, and the realization registry;
- the r3 source, artifact, external report, and the r4 point-by-point response;
- the source manifest, publication policy, build scripts, verification script, three regression programs, and committed evidence; and
- the branch topology separating the canonical restart, research, revision, referee-ready, verification, and review lines.

The committed evidence records:

```text
56 pages
38 formal statements
38 proof environments
168 labels
19 cited bibliography items
39 manifested source files
18 TeX source files
15,407 inherited finite checks
9,418 new finite checks
17,337 exact transport checks
125 + 201 + 535 rejected negative controls
byte-identical independent PDF rebuilds
identical ordinary and optimized regression outputs
zero overfull boxes
```

These checks are useful for source integrity, arithmetic regression, and reproducibility. The repository correctly records that they do not prove the continuum theorems.

The preservation discipline is also satisfactory. All twenty-seven formal results from r3 remain present with their original hypotheses. The old v1–v96 development and the separate realization families are not silently promoted into the role of the new general theorem, and no historical branch is overwritten.

---

## 2. Executive assessment of the r4 revision

The r3 report identified a single dominant mathematical obstruction and several secondary ones. Revision r4 makes a genuine theorem-level advance on the dominant obstruction and a meaningful advance on one secondary obstruction.

| r3 structural issue | r4 assessment |
|---|---|
| Old error was erased whenever a trajectory changed predictive component | **Resolved for a broad sufficient class.** The marked gain kernel retains every off-diagonal edge, and the forward weighted drift controls the old error before terminal weighting. |
| Terminal rare-mass normalization could destroy constants | **Resolved under `(O)`.** The proof controls global allocation-weighted risk and derives `(O)` from an invariant-reference comparison without inverse component probabilities. |
| Singular recurrence relied on state-revealing refreshes | **Resolved in an explicit symbolic class.** Both cross-mode transitions preserve a nonconstant old tail, expanding deletion steps recur, and no recurrent refresh reveals the hidden remainder. |
| Countable geometry required separated components | **Substantially improved.** The lower now allows finite overlap multiplicity and arbitrary decoder centers. Unbounded multiplicity remains open. |
| Acquisition and memory were not coupled by one recurrent law | **Materially improved.** The finite-read experiment produces an explicit atomic acquired law and a common depth-dependent acquisition–memory profile. |
| Full multi-resource matching law | **Still open.** Persistent state and selected acquisition/calibration coordinates have lower bounds; program, workspace, runtime, simulator state, numerical precision, and general causal deficiency do not form a matched region. |
| Adaptive acquisition, unknown kernels, and pilot design | **Open and explicitly disclaimed.** |
| Natural hard application beyond designed examples | **Not yet supplied.** The symbolic models are exact and useful, but deliberately constructed; the filtering example is a classical uniformly contracting one-dimensional class. |

This is a materially better paper than r3. The strongest previous criticism can no longer be repeated: it would be inaccurate to describe the main theorem as reset-preserved. The remaining editorial question is whether the new nonreset theorem and its realizations have the depth and natural reach required by a leading general mathematics journal. In my judgment they do not yet meet that exceptional threshold.

---

## 3. Summary of the revised contribution

The paper starts from a prepared controlled experiment on standard Borel spaces. Actions, reports, failed attempts, clocks, and resource increments are part of the visible causal interface. Executable future tests define predictive equivalence, and a compact continuous-instrument certificate supplies pointwise report updates without dividing by zero-probability events.

For a fixed finite squared-prediction task, the actual terminal score law is quantized by either:

1. a checkpoint encoder that reads the full terminal history and retains at most `M` labels; or
2. an online encoder that recursively updates at most `M` persistent labels and cannot reread discarded reports.

Conditional projection identifies checkpoint excess risk with quadratic quantization of the actual predictive score. The central issue is whether the same scale is attainable by a recursive machine when the predictive dynamics move between rare or singular strata.

The new theorem introduces four certificates.

- `(G)` gives actual conditional covering and arbitrary-center small-ball estimates, with countably many components and finite overlap multiplicity.
- `(L)` gives an executable local recursive approximation for every finite allocation, with a marked one-step gain and destination-dependent forcing radius.
- `(D)` gives a positive Lyapunov weight `v` and a pointwise squared-gain drift for the complete marked active kernel, including all cross-stratum edges.
- `(O)` compares seed and active-injection masses with the actual terminal component weights.

If these hold, the theorem proves

```text
B_T + c Q_T(M)
    <= R_cp(T,M)
    <= R_on(T,M)
    <= B_T + C H_* Q_T(M),
```

where

```text
H_* = V A max{1, b_*^2/(1-sqrt(kappa))^2}.
```

The constants contain no inverse terminal component mass, no inverse activity probability, and no dependence on the number of components.

A finite-mode raw criterion obtains `(D)` from a nonnegative gain matrix `C_2=(p_ij L_ij^2)` with spectral radius below one. A common invariant reference and two-sided preparation-density comparison obtain `(O)` without replacing the actual law by the reference law.

The first new realization is a nonhomogeneous symbolic Cantor/Moran process with two modes. Deletion expands the predictive coordinate, prepending contracts it, both cross-mode maps preserve an unknown old tail, and the active chain may spend arbitrarily long periods in expanding transitions. The theorem yields a matching persistent-state law with constants uniform in a rare-mode parameter and in arbitrary deterministic independent holds. By alternating scale ratios, the model has no limiting quantization exponent.

The second new construction begins with only finitely many paid bit observations. The full-history predictive state is a mode and a finite known prefix whose random depth evolves under the same recurrent nonreset dynamics. The acquired law is an explicit finite atomic mixture. A two-point terminal calibration ambiguity is coupled to the same Bernoulli task. The resulting worst-case excess risk is

```text
delta^2
  + E[ell_{min(H_T, floor(log_2 M))}^2]
```

up to universal constants, with an exact checkpoint decomposition into calibration, acquisition variance, and actual-law quantization.

The inherited causal-morphism theorem then records acquisition, simulator state, controller state, phase/clock state, workspace, program data, calibration, numerical precision, and complete interactive total-variation defect. The paper carefully distinguishes constructive upper accounting from converses.

---

## 4. Assessment against the controlling targets F1–F4

### F1 — Causal acquired-geometry transfer

**Substantially achieved as a sufficient class theorem.**

The main theorem begins from a prepared experiment, its actual law, an executable local update, and a marked raw-error kernel. The checkpoint lower uses actual terminal weights and arbitrary decoder centers. The online upper is realized by recursive labels rather than by reusing a checkpoint map. Report continuity and resource composition remain separately typed.

The qualification is important. `(G)`, `(L)`, `(D)`, and `(O)` are certificates, not an intrinsic characterization. In particular, `(L)` contains much of the constructive content: for every claimed allocation, one must already possess a Borel recursive finite-label rule with the stated gain and forcing structure. `(O)` can also be demanding in nonstationary systems with creating or disappearing strata. The theorem is therefore a strong transfer principle, not a classification of finite-memory predictability.

### F2 — Resource–resolution–risk composition

**Partially achieved, with one genuinely matched joint law.**

The finite-read recurrent model couples raw acquisition count, persistent memory, and an unobservable calibration sign in one task. This is considerably stronger than adding unrelated error floors. The exact checkpoint identity and online construction use the same actual predictive law.

The full programme stated in the charter is not yet matched. Simulator states, controller states, phase states, workspace, program length, arithmetic time, numerical precision, and complete causal deficiency are carefully accounted for constructively, but most lack corresponding lower bounds. The product-state formula is an implementation upper bound, not an optimality theorem. The total-variation defect term is also an upper allowance unless separate alternatives create a lower witness.

Thus F2 is achieved for a selected subvector and selected raw model, not as a general full-resource region.

### F3 — Singular or nonuniform extension

**Achieved in a meaningful nonreset sense.**

The new symbolic process has:

- a singular invariant reference;
- nonhomogeneous scales;
- recurrent expanding and contracting updates;
- cross-stratum transport of an unrevealed old tail;
- arbitrarily rare modes;
- arbitrarily long exact waits;
- nonstationary actual laws comparable to the reference; and
- a profile with two distinct subsequential logarithmic exponents.

The general lower also permits finitely overlapping countable components. This is well beyond a fixed finite ensemble or a reset-only recurrence.

The boundary is that the principal explicit singular system is purpose-built, the overlap multiplicity is bounded, and the raw occupation theorem relies on a common reference comparison. The paper does not classify general singular filters, regime-switching diffusions, nonuniformly hyperbolic observations, or systems with state-dependent stopping.

### F4 — Distinct raw-kernel realizations

**Achieved.**

The non-erasing symbolic process and the nonlinear binary hidden-state filter are genuinely different raw experiments. The former is singular and has recurrent expansion; the latter has a scalar posterior with a uniform same-report contraction derived from an observation density. The finite-read symbolic model adds a third actual-acquisition calculation.

The two principal realizations do not enter the proof of the general theorem. This separation is correct and important.

---

## 5. Audit of the central nonreset theorem

### 5.1 The geometric lower

Lemma `lem:nr-overlap` assigns each decoder center to every component neighborhood containing it. Finite multiplicity gives at most `Lambda M` assignments. Within a component, the arbitrary-center small-ball estimate implies that the union of assigned balls carries at most one half of the conditional mass. Unassigned centers remain outside the prescribed neighborhood. Summing the component lower bounds against the actual terminal weights gives a lower at budget `Lambda M`.

The dyadic regularity of `r_j(k)` then coarsens an allocation from `Lambda M` to `M`. The proof correctly treats zero and singleton allocations through `r_j(0)=r_j(1)`. Countable partitions create no summability difficulty because every finite label allocation has finite support and all component contributions are nonnegative.

This argument is sound as a sufficient lower-bound device. It should not be oversold as a general theorem for overlapping singular measures: finite overlap at the declared relative scales is essential, and the small-ball bound is itself a substantial actual-law hypothesis.

### 5.2 The weighted energy recursion

The key new point is the weighted energy

```text
a_t^2 = E[v(Z_t) e_t^2].
```

On an active step, the conditional marked-kernel hypothesis and `(D)` bound the old-error contribution by `sqrt(kappa) a_{t-1}` in weighted `L^2`. The forcing contribution is bounded through `(O)` by the terminal allocation norm. Minkowski is applied inside the active branch. The exact hold branch copies both state and label, so the squared energies—not their square roots across different branches—are mixed:

```text
a_t^2
 <= (1-vartheta_t) a_{t-1}^2
    + vartheta_t (sqrt(kappa) a_{t-1} + b_* q)^2.
```

The interval

```text
a <= q max{1, b_*/(1-sqrt(kappa))}
```

is invariant, including when the activity probability vanishes. This is the correct mechanism for avoiding a false inverse-activity loss.

The proof does not discard error arriving from another component and does not divide a global covariance by a terminal rare mass. This is precisely the structural improvement required by the r3 report.

The manuscript should nevertheless formalize the filtration condition as sharply as possible. The active marked kernel must be the conditional law given the complete past and algorithm randomness through the declared factor, so that the next mark cannot retain an undeclared dependence on the previous label error. The prose states this, but a displayed conditional-law hypothesis would make the theorem easier to reuse and audit.

### 5.3 Occupation comparison

Condition `(O)` compares both initialization and every active candidate law with the terminal component weights. It is not merely a technical convenience. Without it, forcing can enter a component that later has negligible or zero terminal mass, and the terminal allocation profile need not pay for that forcing.

Proposition `prop:nr-reference` is correct: positivity and invariance preserve the two-sided comparison `c lambda <= mu_t <= C lambda`, and terminal weights then dominate active candidate masses up to `C/c`. No inverse component weight is introduced.

The mathematical limitation is that a common invariant reference with a uniformly bounded preparation density is a strong structural assumption. It excludes important finite-horizon systems with substantial creation, extinction, absorption, or transport between measures of changing support. The older reset-preserved theorem covers a different class, but the paper does not supply a unified criterion or a necessity theorem.

### 5.4 The gain matrix

For a finite fiber decomposition, the matrix `C_2=(p_ij L_ij^2)` collects all off-diagonal and diagonal old-error gains. The Neumann-series construction of a positive vector when `rho(C_2)<1` is standard and correct. The invariant mixture calculation is also correct when every edge sends the source reference law to the destination reference law.

The manuscript appropriately disclaims novelty for the positive-matrix criterion itself. The new content is its coupling to actual-law geometry and an executable online code. At a top-four level, however, that coupling must carry almost all of the claimed novelty; the proof technology on the dynamic side is otherwise classical positive stability.

### 5.5 The local implementation hypothesis

Hypothesis `(L)` deserves more emphasis than it currently receives. It is not a minor measurability clause. It requires, for every allocation, an executable recursive finite-label machine whose local error obeys the exact gain-plus-forcing inequality, including transitions from discarded components sharing a common anchor.

This is where a substantial portion of model-specific difficulty resides. In the symbolic and filtering examples the authors verify it explicitly, which is valuable. For a general theorem intended as a foundation, however, one would like either:

1. a broad raw-kernel theorem that derives `(L)` from geometric and continuity assumptions; or
2. a sharper statement that presents the central result explicitly as an a posteriori stability theorem for a supplied recursive quantizer.

Without such clarification, readers may overread the theorem as constructing an online encoder from covering data alone. It does not.

### 5.6 Constants and uniformity

The displayed dependence

```text
H_* = V A max{1, b_*^2/(1-sqrt(kappa))^2}
```

is transparent. The absence of `min_j w_{T,j}`, component count, and minimum activity is a real strength.

The constants are not uniform when the drift approaches criticality, when occupation comparison deteriorates, when overlap multiplicity grows, or when the local rule becomes unstable. This is mathematically natural, but the introduction should make these are the true condition numbers of the theorem.

---

## 6. Audit of the non-erasing singular realization

### 6.1 Raw experiment and quotient

The state consists of a two-state mode and an infinite fair binary tail encoded by a nonhomogeneous Cantor/Moran map. Reports reveal the mode transition, the operation, and newly prepended bits but never reveal the remaining old tail. The terminal Bernoulli mean separates the two modes and then identifies the coded tail. This gives the claimed predictive quotient for the designated continuation tests.

The full-tail version has an initialization report containing the complete mode and sequence. Mathematically this is a legitimate standard-Borel report. Operationally it is a strong interface. The paper partly repairs this by charging a finite prefix reader and, more decisively, by introducing the separate finite-read experiment in the next section. The distinction should remain prominent: the full-tail theorem is not by itself a finite-packet physical acquisition theorem.

### 6.2 Gain calculations

The first-difference estimates give:

```text
deletion gain       <= 15
prepend two gain    <= 1/3
prepend four gain   <= 1/27
copy gain           = 1.
```

With deletion probability `1/4096`, the conditional squared gain on the `0 -> 0` edge is

```text
(1-gamma)/9 + 225 gamma = 85/512.
```

The resulting matrix

```text
[(1-alpha) 85/512, 225 alpha]
[1/1458,             1/2      ]
```

satisfies the displayed drift with `v=(450,1)` and `kappa=17/20`, uniformly in `alpha`. The expanding cross-mode deletion is fully retained. No inverse stationary rare-mode mass appears.

These computations are coherent. They also show why the example is carefully designed: the large deletion gain is offset by very strong prepending contraction and a specifically chosen rare deletion probability.

### 6.3 Actual acquisition and geometry

Every edge preserves the fair product tail, and the two-state mode chain has the displayed invariant distribution. A prepared law bounded above and below relative to that invariant mixture stays comparable. This yields actual conditional tail laws comparable to the fair product law in each mode.

Cylinder covers and first-difference gaps then supply arbitrary-center small-ball estimates. The terminal mode intervals are separated, so the overlap multiplicity is one. The online prefix machine uses only its retained word and current report; the destination mode does not survive as an uncharged side channel.

The profile comparison

```text
Q_T(M) ~ ell_floor(log_2 M)^2
```

is correct up to uniform constants. Alternating superexponentially long blocks of ratios `1/3` and `1/5` produces the two claimed subsequential logarithmic exponents.

### 6.4 Significance of the example

The model genuinely demonstrates nonreset transport through recurrent expansion. It is not a disguised state-revealing refresh. That is a substantial improvement.

Its limitation is naturality. The symbolic operations, transition probabilities, contraction lengths, and deletion frequency are selected to make the positive drift transparent. This is an excellent sharpness and feasibility example. It is not yet evidence that the theorem resolves a difficult phenomenon in a naturally occurring filtering, statistical, dynamical, or control model.

A top-four case would be much stronger if the same mechanism were derived for a nonuniformly stable hidden Markov model, regime-switching nonlinear filter, partially observed expanding map, or another model already central to the literature.

---

## 7. Audit of the nonlinear filtering realization

The binary hidden-state filter has a scalar posterior quotient. Direct normalization gives the update. In log-odds coordinates, the hidden flip contributes a same-report contraction factor at most `1-2q_0`; the observation adds a report-dependent term independent of the old posterior coordinate.

The lower bound on the report-to-posterior Jacobian and the upper bound on the report density give a uniform upper density bound for the actual posterior law at every positive horizon. An interval grid supplies covers, and the actual density supplies the small-ball estimate. The one-component partition makes occupation comparison trivial.

This is a valid second realization of the new theorem. It is structurally different from the symbolic model and satisfies F4.

For significance, however, it is a uniformly contracting one-dimensional filter with a strictly positive observation density. Quantized nonlinear filters in such stable regimes are classical territory. The manuscript's novelty is the common theorem that also handles the nonreset singular model, not this realization by itself.

---

## 8. Audit of the finite-read recurrent acquisition theorem

### 8.1 Actual predictive law

The preparation reports only the mode. The next `B` paid calls reveal one old bit each. There are then `T` recurrent opportunities, every hold and active report is charged, and a final terminal call is charged:

```text
N_raw = B + T + 2.
```

The full-history known-prefix depth obeys an explicit mode/operation recurrence. Conditional on the mode and depth, the known word is uniform and the remaining tail is fair. The resulting acquired law is therefore the finite atomic mixture written in `eq:ra-law`; no continuous latent law is substituted for it.

This is a strong and correct modelling improvement over the full-tail initialization.

### 8.2 Acquisition variance

Within a depth-`h` cylinder, the unresolved physical tail variance is bounded above and below by constants times `ell_h^2`. The affine terminal score contributes the displayed factors. This gives the acquisition term

```text
A_{B,T} ~ E[ell_{H_T}^2].
```

The argument uses the actual history and actual posterior law.

### 8.3 Calibration minimax identity

The terminal calibration sign `theta in {-delta,delta}` affects only the final Bernoulli mean and is absent from all acquisition reports. Averaging the risks for the two signs gives the nominal squared prediction error plus `delta^2`. For the nominal conditional-mean decoder, the cross term vanishes for each sign, so the same value is attained.

Consequently the exact checkpoint identity

```text
R_cp = delta^2 + A_{B,T} + q_M(nu_{B,T})
```

is justified for the stated common baseline and fixed protocol.

### 8.4 Online finite-state construction

The encoder stores a mode and a word of length at most `m` in

```text
2^(m+2) - 2
```

states, including the word length and mode. It reads each paid input once, truncates prepended words, pops a retained bit on deletion, and never reconstructs discarded information.

On the enlarged domain of cylinder centers, deletion has gain at most `30`, prepend-two gain at most `2/3`, prepend-six gain at most `2/243`, and copy gain one. The choice of six prepended bits is essential. The gain matrix is stable with `v=(1800,1)` and `kappa=17/20`. The manuscript correctly distinguishes these constants from those of the full-tail Cantor-set model.

The retained word is a genuine prefix of the physical tail at its retained depth. Its origin pattern depends on mode and operations but not on the bit values. This justifies the conditional-mean decoder and the exact calibration cancellation. A biased numerical decoder would not have this property, and the paper correctly records that caveat.

### 8.5 Lower witness and final profile

The stationary physical mode-tail law supplies an ideal-score quantization lower. Proposition `prop:nr-acquisition` combines that lower with the actual acquisition variance and the online construction. The elementary identity

```text
max{E ell_{H_T}^2, ell_n^2}
 <= E ell_{min(H_T,n)}^2
 <= E ell_{H_T}^2 + ell_n^2
```

then yields the claimed profile.

The theorem is a genuine joint acquisition–memory–calibration result. Its limitation is scope: the kernel is known, `B` and `T` are fixed externally, the exploration is nonadaptive, the calibration ambiguity is deliberately unlearnable, and the scored task is one scalar Bernoulli prediction. It is not an optimal allocation theorem under a total acquisition budget and not a learning theorem.

---

## 9. Resource transfer and converses

The resource ledger is one of the manuscript's strengths. It distinguishes:

- raw calls and physical time;
- persistent label cardinality;
- simulator, controller, and phase states;
- temporary workspace;
- program description;
- calibration and input precision;
- numerical output precision; and
- complete interactive causal deficiency.

Metric approximation terms combine in root-mean-square before squaring. Complete total-variation defects add to a bounded common-task loss. Product-state cardinalities are used only for a stated serial implementation.

The manuscript also correctly distinguishes exact support converses, retained-information converses, scalar minimax examples, and constructive upper allowances.

The top-four difficulty is that there is no matched theorem for the complete vector. In particular:

- `R M D_c Q` is not shown necessary;
- program length and workspace have no general lower;
- arithmetic time has no general lower;
- numerical precision has no universal task-sensitive floor;
- a causal deficiency certificate gives an upper transfer but no universal lower; and
- acquisition scheduling is fixed rather than optimized.

The abstract and introduction should therefore avoid language that could be read as a fully matched “resource–resolution–risk region.” What is proved is a matched persistent-state law, selected acquisition/calibration couplings, and a typed composition theorem for further upper allowances.

---

## 10. Relationship to the general-foundations charter

The restart charter asks for a theorem beginning at the experiment/kernel level, using actual acquisition, global covering, stable predictive updates, report continuity, and explicit simulator-state accounting. Revision r4 now has such a theorem.

It also asks for matching resource–resolution laws over a class, not one finite designed ensemble. Revision r4 satisfies this in a literal and mathematically meaningful sense: Theorem `thm:nonreset` is a class theorem, and two different raw experiments verify it.

The tension is that the paper uses the word “foundations” at a level broader than the theorem's present intrinsic reach. The theorem does not determine when a general experiment admits a finite-memory law. It says that when one has:

1. actual geometric cover and small-ball data;
2. an executable local finite-label approximation for every allocation;
3. a common weighted squared-gain drift; and
4. terminal occupation domination,

then checkpoint and online risks match.

This is a useful architecture. Whether it is a foundational theorem in the sense expected by a leading general journal depends on showing that the certificates arise broadly, naturally, and unexpectedly—or on replacing them by a more intrinsic equivalence. The current paper does not yet do either at the required level.

---

## 11. Novelty and literature positioning

The manuscript responsibly disclaims novelty for conditional projection, probability quantization, cylinder coding, positive-matrix resolvents, total-variation data processing, and classical experiment comparison. This is good.

The claimed novelty is the coupling of these ingredients through:

- actual acquired component laws;
- nonreset marked old-error transport;
- an executable persistent-state encoder;
- a two-sided checkpoint/online law; and
- explicit resource accounting.

That coupling is nontrivial and, to my knowledge from the material supplied, not merely a restatement of one cited theorem. The report should not be read as a negative priority finding.

The literature discussion remains too narrow for the breadth of the title and claims. Nineteen cited items cannot plausibly map all nearby work across nonlinear filtering, causal/sequential rate distortion, finite-state prediction, belief compression, Markov jump systems, random dynamical systems, singular quantization, experiment comparison, and information-constrained control. The paper need not become a survey, but it should identify the closest theorem-level precedents and explain exactly which hypotheses and conclusions differ.

In particular, the role of `(L)` should be compared with realizable causal quantizers and recursive reconstruction schemes; `(D)` should be compared at theorem level with positive moment stability and random Lipschitz recursions; and the actual-law lower should be compared with operational causal rate-distortion and belief approximation results. A broad priority claim should not rest on a small bibliography plus repository-internal comparisons.

---

## 12. Major issues that should be addressed before specialist-journal submission

### 12.1 State the exact status of `(L)`

The introduction and main theorem should say plainly that global covering does not construct the recursive encoder. `(L)` supplies the model-specific online machine and its local stability inequality. The theorem then transfers its local certificate to a global actual-law risk law.

A stronger revision would derive `(L)` from a reusable raw continuity/selection theorem.

### 12.2 Separate the theorem's two nonstationary mechanisms

The nonreset theorem uses occupation comparison against terminal weights. The older bridge uses reset-preserved recharge and can handle different creation/extinction patterns. The paper should present a clear decision chart:

- when the invariant-reference route applies;
- when the recharge route applies;
- when neither applies; and
- what is presently unknown.

### 12.3 Make the conditional marked-kernel hypothesis formal

The theorem should specify the filtration and conditional-law identity that make the next mark independent of the past approximation error given the declared factor. This is essential when controller variables, exploration randomness, and algorithm shared randomness are present.

### 12.4 Foreground deterministic-horizon and suspension restrictions

Independent exact holds are handled elegantly. State-dependent waiting, error-selected stopping, and arbitrary stopping horizons are not. These restrictions should appear in the main theorem statement and abstract-level scope, not only in audits and the final comparison section.

### 12.5 Clarify the operational status of the full-tail model

A complete infinite initialization report is mathematically valid but physically strong. The finite-prefix reader and the separate finite-read experiment should be presented as distinct interfaces. No wording should suggest that an infinite Borel report is automatically a finite communication packet.

### 12.6 Moderate full-resource language

The complete ledger is valuable, but the matched lower concerns only selected coordinates. The manuscript should distinguish:

- two-sided persistent-state/acquisition/calibration laws;
- typed constructive composition; and
- still-open full-vector converses.

### 12.7 Expand theorem-level prior-art comparison

The revised literature section should identify the closest results, not merely fields or textbooks, and compare assumptions, operational resource models, and conclusions. The current discussion is candid but not exhaustive enough for a broad foundations claim.

### 12.8 Streamline the inherited material

Moving complementary results to appendices helps, but the paper still contains several different mechanisms and resource examples. A specialist submission would benefit from a sharper narrative centered on:

1. the nonreset theorem;
2. the singular realization;
3. the finite-read acquisition theorem; and
4. only the inherited results needed to make those statements self-contained.

The full historical preservation can remain in repository records without every branch of the earlier programme carrying equal expository weight in the article.

---

## 13. What would materially change the top-four assessment

Further polishing, more regression tests, or additional engineered examples would not by themselves change my recommendation. A top-four case would require at least one advance of a different order, such as:

1. **An intrinsic characterization.** A necessary-and-sufficient or near-necessary criterion for matching online/checkpoint memory laws, replacing the present certificate stack by a structural invariant of the causal experiment.

2. **A natural hard application.** A theorem for a recognized nonuniformly stable filter, switching system, random dynamical model, or singular observation process in which the finite-memory law was not previously understood and the present machinery resolves the obstruction.

3. **Adaptive acquisition.** A matched law when the experiment itself is selected causally under a raw budget, including the tradeoff between acquisition, recurrence, memory, and calibration or kernel learning.

4. **A genuine multi-resource region.** A theorem giving matching upper and lower bounds for more than label cardinality and one selected calibration/acquisition mechanism, with simulator/controller/workspace/time costs entering intrinsically rather than only through one implementation.

Any one of these would give the paper a single unmistakable theorem of broad general-mathematics significance. The current manuscript instead offers a carefully assembled architecture with several strong but certificate-based results.

---

## 14. Minor and technical comments

1. The notation `T` for initialized recursion and `N_raw` for paid calls is now clear. Preserve this distinction consistently in captions and theorem summaries.

2. In the main theorem, restate that the geometric partition need not be observable and that `J_t` is not an encoder register.

3. When discussing `rho(C_2)<1`, continue to state that the equivalence concerns the chosen gain comparison matrix, not optimal finite-state prediction.

4. The finite-overlap lower should explicitly note that boundary points outside the open neighborhoods have distance at least the neighborhood radius; this is used for unassigned centers.

5. The small-ball hypothesis is only for positive-mass terminal components. The treatment of zero-mass components in `(O)` is correct and should be kept adjacent to the theorem.

6. The exact Borel-label model and finite-bit implementation should remain notationally distinct. “Zero-error implementation” should not be used without the qualifier “exact Borel” where appropriate.

7. The randomized-decoder lower uses conditioning on the shared seed and conditional-mean replacement. It would help to state the independence of that seed again in Lemma `lem:nr-overlap`.

8. In the full-tail symbolic model, state early that the finite-access routine is an interface restriction on the infinite report, whereas the finite-read model changes the physical experiment.

9. The role of the anchor in unallocated components is subtle. The local-machine proof handles it, but a schematic would improve readability.

10. The proof of the finite-read theorem should keep emphasizing that cylinder centers are not physical Cantor points; the changed gap, gain `30`, and six-bit return are load-bearing.

11. The exact calibration identity depends on unbiased conditional-mean decoding. The numerical-rounding paragraph correctly separates unbiased rounding from arbitrary finite arithmetic; this distinction should appear in the theorem synopsis.

12. The expected random-bit cost of exact rational rejection sampling is not a worst-case time bound. The current caveat is correct.

13. The nonlinear-filter corollary is not uniform as `q_0` tends to zero. This should be visible in any summary table of constants.

14. The phrase “same multiscale order as the checkpoint optimum” is justified only under the complete certificate stack and fixed exploration. Add that qualifier whenever the phrase appears outside the theorem.

15. The bibliography should use stable published references where available and reserve arXiv references for material without a final publication or where version history matters.

16. The source audits correctly say that finite tests do not prove continuum results. Keep this disclaimer in all future build receipts.

17. The paper's use of “positive” for kernels means nonnegative and normalized, not uniformly lower-bounded. This is stated once; repeating it near the raw criteria would prevent confusion.

18. The common invariant reference is an analytic comparison device, not the actual acquired law. The manuscript already says this; preserve the distinction in the abstract and conclusion.

19. The resource corollary should not be paraphrased as a product-state lower bound.

20. The final scope section is unusually candid and should be retained, although some of its most important restrictions belong earlier.

---

## 15. Final evaluation

Revision r4 contains a real mathematical advance over r3. The authors have constructed a coherent nonreset transfer theorem in which old error crosses predictive strata, rare terminal masses do not appear in denominators, and exact holds do not create artificial activity losses. They verify the theorem in a singular recurrent process with genuine expanding nonreset edges and in a nonlinear filtering class. They also give a finite-read recurrent model whose actual atomic predictive law yields a coupled acquisition–memory–calibration minimax profile.

I found no elementary fatal flaw in the load-bearing arguments checked. The repository pipeline is exceptionally careful about provenance, exact source/artifact binding, preservation of earlier results, finite-regression scope, and resource-interface distinctions.

The remaining top-four objection is that the central theorem is still a sufficient certificate architecture whose difficult model-specific content is distributed across `(G)`, `(L)`, `(D)`, and `(O)`. Its principal raw criterion uses standard positive stability and a common invariant-reference comparison. The realizations prove feasibility and sharpness but do not yet solve a recognized broad problem in a natural difficult class. The full resource vector remains unmatched, and adaptive or unknown-kernel acquisition is outside scope.

Accordingly:

**Top-four general-journal recommendation:** reject in the present form.  
**Reason:** insufficient intrinsic breadth and concentration of a single transformative theorem, not an identified fatal correctness error.  
**Specialist-journal outlook:** favorable after a focused substantial revision addressing scope, prior art, the status of `(L)`, and the distinction between matched laws and constructive resource accounting.
