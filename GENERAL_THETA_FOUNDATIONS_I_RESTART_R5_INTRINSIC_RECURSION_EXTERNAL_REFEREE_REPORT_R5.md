# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r5-intrinsic-recursion-2026-10-07`  
**Reviewed exact referee-ready head:** `4a03a516fc780d1cfe6ccb5c00f0b05fac8a9494`  
**Native mathematical source commit:** `e78b9b54f3f6c7fe8bc7fb23bb9575f7763ea545`  
**Native paper-subtree SHA:** `0c82472de3707069e03726d700351184838eb865`  
**Published evidence commit audited by the referee-ready record:** `29d5461d7d7d91bc6d830a17c1f78674a1c4faf7`  
**Canonical restart parent:** `18000b21e4bfd89180ccb069e46ac0f21621f34d`  
**Predecessor r4 referee-ready head:** `7c5012b308d3cdd5514913db7d16f6d25545d82b`  
**Previous external report blob:** `fbaa8ac345f170971ffb0ee960369263016153b0`  
**Recorded rendered-paper SHA-256:** `e06a2bdeae6b85ce0dcf1e551e643c90b9cb12f5eadf50092f93fb9921c4493a`  
**Review branch:** `review/general-theta-restart-r5-intrinsic-recursion-external-top4-referee-r5-2026-10-07`  
**Date:** 7 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned decision of a named journal, a formal proof certificate, an independent priority certificate, or a claim of journal acceptance.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not a technical-correctness rejection**. Revision r5 is a substantial and conceptually clean advance over r4. The principal structural objection in the previous report has been answered: the central theorem no longer assumes a supplied recursive quantizer, and it no longer requires terminal occupation domination or comparison with a common invariant reference. Instead, it constructs a legal finite-label recursion from a static inward cover and two inequalities stated directly for the raw true-report kernel. The filtration and suspension hypotheses are now explicit, the actual acquired law is retained in the lower bounds, and the paper has been reorganized around one mechanism and two genuinely different realizations.

In the load-bearing arguments checked, I did not find an elementary gap invalidating:

- the conditional-projection identity and exact checkpoint quantization formula;
- the inward-envelope induction;
- the true-law two-point error recursion and exact-hold mixture;
- the multidimensional exponential compander;
- the intermittent-filter contraction and actual final-gate Jacobian lower bound;
- the completed-domain singular gain calculation;
- the actual depth/atomic-law computation and common-oracle lower bridge;
- the finite-horizon report coupling; or
- the typed serial resource-composition and executable-interface converse.

The remaining negative top-four judgment concerns **mathematical level, intrinsic breadth, natural reach, and concentration of novelty**, rather than an identified fatal error. The main theorem is an elegant sufficient principle under a uniform all-pair true-law contraction, a candidate Lyapunov envelope, and a global inward cover. It does not characterize finite-memory predictability, nor does it derive those hypotheses for a recognized difficult natural class where the memory law was previously unknown. The two realizations are mathematically meaningful, but both are deliberately structured so that the key inequalities can be proved explicitly. The full resource vector, adaptive acquisition, unknown kernels, and arbitrary stopping remain outside the theorem.

For a strong specialist journal in probability, information theory, nonlinear filtering, stochastic control, quantization, or applied probability, my assessment is **favorable after a focused major revision**. In that setting the paper's constructive theorem, exact acquired-law converses, and two detailed realizations constitute a publishable contribution, provided the closest prior art is treated at theorem level and the morphism/coupling formalism is made fully self-contained.

---

## 1. Review object, provenance, and pipeline inspected

The review concerns the exact referee-ready head

```text
4a03a516fc780d1cfe6ccb5c00f0b05fac8a9494.
```

That commit is a read-only verification record. It identifies the native source commit

```text
e78b9b54f3f6c7fe8bc7fb23bb9575f7763ea545
```

and the native paper tree

```text
0c82472de3707069e03726d700351184838eb865.
```

I reviewed the manuscript as a source-and-derivation pipeline, not merely as an abstract or a rendered PDF. The inspection included:

- `main.tex`, all seven native sections, and `references.tex`;
- `README.md`, `REFEREE_RESPONSE.md`, `THEOREM_MAP.md`, `PROOF_LEDGER.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `PIPELINE_DERIVATION.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, `NOTATION_AUDIT.md`, and `PINNED_INPUTS.md`;
- the source manifest, build program, regression program, verification program, and committed evidence records;
- the canonical restart charter, general-foundations outline, realization registry boundary, and `THEOREM_TARGETS.md`;
- the r4 manuscript/supplement relation, the r4 external report, and the r5 point-by-point response;
- the branch topology separating canonical, research, revision, referee-ready, verification, and review lines; and
- a targeted independent search for nearby finite-memory POMDP, approximate-information-state, recursive quantization, and zero-delay coding results.

The repository records two byte-identical twenty-page PDF builds, nineteen formal statements, nineteen proof environments, seventy labels, seventeen bibliography items, twenty-seven manifested source files, nine TeX files, 11,510 finite regression checks, eight rejected negative controls, and zero overfull boxes. The recorded build uses isolated temporary directories and disables TeX shell escape. The verification program checks the source manifest, native Git-tree identity, active TeX inputs, labels, references, citations, and statement/proof counts.

These are useful provenance and reproducibility controls. The repository correctly states that there was no hosted CI run and that finite tests do not prove continuum theorems. I treat the receipts as source-integrity evidence, not as mathematical certification. I did not independently rerun the private repository's local TeX/regression commands outside the source-bound evidence already deposited.

The preservation discipline is satisfactory. The r4 paper subtree is retained unchanged as a complementary mathematical supplement, with its thirty-eight formal statements and original hypotheses. The v1–v96 archive, old review branches, and realization families are not overwritten or silently promoted into the new main theorem.

---

## 2. Executive assessment of the r5 revision

Revision r5 is the most important conceptual improvement in the restart sequence so far. The new main theorem replaces the r4 certificate stack by a substantially more intrinsic constructive implication:

```text
static inward cover
+ true-report-law two-point moment bound
+ true-report-law candidate-envelope drift
+ legal finite seed
        =>
constructed recursive M-label encoder
+ uniform online prediction bound.
```

The checkpoint lower remains tied to the actual terminal score law, either through an actual positive submeasure or through an exact conditional-projection/oracle identity when finite acquisition makes that law atomic.

This changes the mathematical status of the paper. In r4, a significant portion of the online construction was encoded in the local recursive-machine hypothesis `(L)`, and the passage to terminal allocations relied on occupation condition `(O)`. In r5, neither is a premise of the new central theorem. The machine is constructed by updating a representative with the physical report and then applying a least-index selector from a static inward cover. A Lyapunov envelope controls where the representative process travels, and a true-law pair inequality controls its distance from the physical predictive state.

The two applications also improve the paper's reach:

1. the filtering theorem is now finite-dimensional, time-inhomogeneous, and intermittently mixing, with arbitrarily long informative but noncontracting realized runs; and
2. the singular theorem permits arbitrary initial mode law, time-varying mode probabilities, creation or disappearance of mode masses, expanding deletion steps, nonreset transport of unrevealed tails, and only finite paid acquisition.

These are genuine improvements. It would be inaccurate to repeat the r4 objection that the recursive machine is assumed or that the new theorem depends on a common invariant preparation.

The top-four limitation has therefore moved. It is no longer primarily a logical objection. It is now the question whether the sufficient theorem and its two realizations constitute a breakthrough of exceptional general-mathematics significance. In my judgment they do not yet cross that threshold.

---

## 3. Response to the r4 report

| r4 issue | r5 assessment |
|---|---|
| The local hypothesis `(L)` supplied much of the recursive machine | **Resolved in the new main theorem.** The finite recursion is constructed from a static inward cover after the raw candidate update. |
| Terminal occupation domination `(O)` and a common invariant reference were strong premises | **Resolved for the new sufficient class.** The envelope is controlled directly under the true report kernel; no terminal occupation comparison occurs. |
| The conditional marked-kernel/filtration hypothesis needed formalization | **Resolved.** Equation `(conditional)` conditions on the complete observed past, retained label, and used algorithm randomization, while excluding hidden state and latent apparatus coins. |
| Deterministic horizon and exact independent holds were insufficiently foregrounded | **Resolved.** They are explicit in the abstract, theorem statement, and scope audit. |
| The infinite/full-tail interface was operationally too strong | **Resolved in the new main.** The singular realization starts from a finite paid prefix and computes its actual finite atomic acquired law. |
| Full-resource language risked overstating matched converses | **Largely resolved.** The manuscript distinguishes matched label/output/acquisition/calibration laws from constructive resource accounting. |
| The article carried too many inherited mechanisms | **Resolved editorially.** The new main is twenty pages, one central mechanism, two realizations, and a separate preserved supplement. |
| The literature comparison needed theorem-level treatment | **Improved but not fully resolved.** Several close modern finite-memory and zero-delay coding precedents remain absent. |
| A natural hard application or intrinsic characterization was needed for a top-four case | **Not resolved.** The applications are stronger than before, but remain purpose-built or strongly regularized sufficient classes. |

Thus r5 should not be judged as a cosmetic rewrite. It answers most of the actionable mathematical and expository points of the previous report. The remaining rejection at the top-four level is narrower and more demanding.

---

## 4. Summary of the main theorem

Let the realized predictive state take values in a standard Borel metric domain `(S,d)`. At an active step, the physical report kernel and update are

```text
J_t(dy | x),      F_t(x,y).
```

For a budget `M`, the theorem assumes only static Borel covering data with representatives `c_i` and cells `A_i` such that

```text
d(x,c_i) <= r_M w(x),       w(c_i) <= w(x)
```

whenever `x in A_i`. No online coding rule is included in this assumption.

The active indicator is conditionally independent of the complete past with deterministic probability `vartheta_t`. On an inactive step, both the predictive state and retained representative are copied exactly. On active steps the manuscript assumes, uniformly in all true states `x`, candidate states `z`, and deterministic times,

```text
∫ d(F_t(x,y),F_t(z,y))^2 J_t(dy|x) <= kappa d(x,z)^2,

∫ w(F_t(z,y))^2 J_t(dy|x) <= a w(z)^2 + b,
```

with `kappa<1` and `a<1`. The second integral is deliberately under the physical report law generated by `x`, not the candidate's imagined law.

The algorithm updates the old representative using the physical report, then selects the first static covering representative for the candidate. With

```text
H   = max{H_0, b/(1-a)},
E_M = max{e_0, r_M sqrt(H)/(1-sqrt(kappa))},
```

it proves

```text
B_T + q_M(nu_T)
      = R_cp(T,M)
      <= R_on(T,M)
      <= B_T + L^2 E_M^2.
```

An actual positive submeasure satisfying a small-ball bound supplies a matching checkpoint lower. When finite acquisition makes the actual score law atomic, the common-oracle identity retains the acquisition variance and uses the latent ideal law only as a lower witness.

This is a clear and useful theorem. Its logical contribution is real: the recursive machine and its invariant error radius are conclusions, not assumptions.

---

## 5. Audit of the central proof

### 5.1 Predictive quotient

The compact continuous-instrument proposition handles an important version issue. The evaluation image is compact metrizable; density-weighted closure implies that equal evaluation fibers have equal report densities; division is used only at positive density; and the normalized update descends on the declared positive-density domain. The final standard-Borel factorization is performed coordinatewise and extended off the image by a fixed state.

This is a sufficient certificate rather than a general quotient theorem, and the manuscript says so. I found the proof coherent under its stated closure assumptions. For publication, it would help to state more explicitly the topology and measurable domain on which the descended update is continuous, as opposed to merely pointwise well defined.

### 5.2 Conditional projection and checkpoint quantization

The identity

```text
E||Y-a||^2 = B_T + E||P_T-a||^2
```

is applied correctly after conditioning on the full history and independent algorithm randomization. Replacing a randomized decoder by its label-conditional mean, then choosing the nearest center, proves that shared independent randomization cannot improve the `M`-center checkpoint value. This gives the exact formula

```text
R_cp(T,M)=B_T+q_M(nu_T).
```

The use of the actual score law `nu_T` is consistent throughout.

### 5.3 Envelope induction

The least-index selector is Borel for a finite Borel cover and preserves the inward envelope. Conditional on the complete past and an active call,

```text
E[w(hat S_t)^2 | past, active]
    <= a w(hat S_{t-1})^2+b.
```

Mixing with the exact hold branch yields the invariant expectation bound `E w(hat S_t)^2 <= H`. The handling of `vartheta_t=0` is explicit, so there is no conditioning on a null active event.

This step correctly controls the approximate trajectory itself. It is precisely what was absent from a cover-only argument.

### 5.4 True-law error recursion

On an active step,

```text
d(S_t,hat S_t)
 <= d(F_t(S_{t-1},Y_t),F_t(hat S_{t-1},Y_t))
    + r_M w(tilde S_t).
```

The first term is controlled under the physical report law by the pair inequality, and the second by the candidate-envelope bound. Minkowski is applied on the active branch. The inactive branch retains the old squared error exactly. The resulting recursion

```text
e_t^2 <= (1-vartheta_t)e_{t-1}^2
          + vartheta_t(sqrt(kappa)e_{t-1}+r_M sqrt(H))^2
```

has the stated invariant radius. No false inverse activity factor is introduced, and no independence between the report and the old approximation error is assumed.

I found this argument correct under the uniform all-pair hypotheses.

### 5.5 Actual acquired lower

The union-of-balls argument is elementary but correctly formulated for an arbitrary positive submeasure of the actual score law. Open balls carry at most half the submeasure; outside their union, including boundary points, the distance to every center is at least the chosen radius. This gives the displayed lower for arbitrary decoder centers and randomized encoders.

The theorem does not claim that upper and lower scales automatically match. It states the additional comparison `s_M ≳ r_M`, bounded acquired mass, and seed control explicitly. This is an important qualification.

### 5.6 Strength and limitation of the hypotheses

The theorem is genuinely more intrinsic than r4, but it is still a sufficient stability theorem. The all-pair inequality is uniform over true and candidate states, including representatives never generated by the physical posterior. The envelope drift must also hold under every true/candidate pair. A global inward cover must be available at every budget, with an exact or separately certified membership operation.

These assumptions are mathematically transparent, and the paper does not disguise them. Nevertheless, they may exclude recursively predictable experiments whose stability is local, path-dependent, nonquadratic, or only visible after a random regeneration structure. This is the principal reason the theorem is not yet a characterization of finite-memory predictability.

---

## 6. Audit of the intermittently mixing filter

### 6.1 Model and quotient

The hidden state has `d+1` values. At each call an observed Bernoulli gate either applies an arbitrary declared positive stochastic matrix or leaves the hidden state fixed. The matrices may vary with time and need not share an invariant distribution. Conditional on the hidden state, a continuous affine-density observation is generated. Gate-zero calls remain informative and are not relabeled as exact holds.

The strictly positive posterior and its log odds determine the declared continuations. The indexed terminal Bernoulli probe separates posterior coordinates. This realizes the relevant predictive quotient.

### 6.2 Physical-law contraction

In oscillation distance, the additive observation log likelihood cancels when two candidate updates are driven by the same report. For a mixing gate, the directional derivative of each predicted log coordinate is an expectation under a probability vector. Two such vectors share the subprobability `s P(l)`, giving contraction factor `1-s`. Averaging the squared gains over the observed gate gives

```text
kappa_f = 1-p+p(1-s)^2 < 1.
```

This calculation is pointwise in the observation and therefore remains valid under the physical report law. It is stronger than a negative average logarithmic contraction and is exactly the hypothesis required by the main theorem.

### 6.3 Candidate envelope and compander

The gate-zero branch can increase oscillation by at most the fixed observation range, while the positive-mixing branch enters a bounded log-odds region before the same observation increment. An exponential Lyapunov function therefore satisfies the required true-law candidate drift.

The signed logarithmic compander is a useful explicit construction. It covers the whole unbounded log-odds domain with `(2K-1)^d` representatives, moves every coordinate toward zero, and has error bounded by the exponential envelope divided by `K`. The unbounded last cell is treated by the same estimate rather than by truncating the actual law. This removes the logarithmic loss that a naive bounded truncation could create.

### 6.4 Actual geometric lower

On the actual event that the final gate mixes, every predicted coordinate is at least `s`. The report-to-posterior map is injective and has determinant

```text
a^d product_i r_i / D_v^(d+1),
```

bounded below uniformly in the declared matrix sequence. Dividing the bounded report density by this Jacobian gives a bounded density for the actual posterior submeasure. Proposition `prop:submass` then yields the `M^{-2/d}` checkpoint lower.

This is a genuine actual-law argument: no bounded density is assumed for the gate-zero part of the posterior law.

### 6.5 Common task, output precision, and calibration

The executed terminal probe selects one coordinate and produces one Bernoulli report. The vector norm is the average of the separately executable coordinate losses, so no joint counterfactual observation is introduced. The acquisition variance, persistent-label lower, fixed dyadic output-grid cut, and hidden calibration sign all refer to this one task. The two-sign expansion correctly retains the bias cross term in the general upper and removes it only for an unbiased nominal decoder.

The final rate

```text
A_T + M^{-2/d}+2^{-2b}+delta^2
```

is therefore meaningful and matched up to constants depending on the fixed model parameters.

### 6.6 Significance boundary

This realization is much stronger than the scalar uniformly contracting example in r4. It has arbitrary finite dimension, time-varying positive matrices, and arbitrarily long realized runs without hidden-state mixing. Still, the gate is exogenous and independent, the positive matrices have a uniform entry floor, the observation family is chosen so that log-likelihood increments cancel exactly, and the final Jacobian event is deliberately available with fixed probability.

Thus the example demonstrates the theorem effectively, but it does not yet settle finite-memory prediction for a broadly recognized nonuniformly stable filtering problem with endogenous degeneracy, unknown kernels, or state-dependent observation loss.

---

## 7. Audit of the finite-read nonreset singular realization

### 7.1 Physical experiment and actual acquisition

The physical coordinate is encoded by a nonhomogeneous binary Cantor construction with ratios in `[1/5,1/3]`. The completed predictive domain also contains every finite-word fair-tail center. The initial protocol reports only the mode and then reads `B` paid bits. Thereafter each opportunity reports a mode transition, an operation, and at most six newly prepended fair bits. Deleted bits and the surviving old tail are not reported.

The full history knows a finite prefix whose depth follows the displayed recursion. Conditional on terminal mode and depth, the known word remains uniform and the unrevealed remainder remains fair. The resulting score law is the explicit finite atomic mixture in equation `(atomic-law)`. This correctly distinguishes actual acquired geometry from the latent Cantor law.

### 7.2 Completed-domain geometry

Including finite cylinder centers is essential. Deletion has Lipschitz gain at most `30` on this completed domain, not the smaller physical-Cantor-point gain. Prepending a fixed word of length `s` has gain at most `6·3^{-s}`. The finite cover retains every center of depth at most `m` in both modes and truncates only longer centers or infinite sequences. The label count includes mode and word length.

The proof's first-difference gap estimates justify these constants. The cross-mode distance makes the two-mode metric legitimate and ensures that once a report sets both candidates to the same destination mode, a cross-mode pair contracts strongly.

### 7.3 Raw pair matrix

For same-mode pairs the squared gains are summarized by

```text
[(1-alpha_t)85/128,  900 alpha_t]
[2/59049,             1/2          ].
```

With weight vector `(1800,1)`, both source rows are bounded by `(17/20)` times the corresponding source weight, uniformly in `alpha_t`. For a cross-mode pair, the old squared distance is `4·1800`, while after any common reported operation the squared distance is at most `1800`. Thus the all-pair true-law inequality holds without an occupation comparison.

The six-bit return on the `1 -> 0` edge and the completed-domain deletion gain are load-bearing. The counterexample ledger correctly records that a shorter return or the physical-only deletion constant would not certify the displayed matrix.

### 7.4 Acquisition variance and online machine

Within a depth-`h` cylinder, the unresolved tail variance is comparable to `ell_h^2`, and the terminal score has slope `1/8`. Hence

```text
A_{B,T} ≍ E ell_{H_T}^2.
```

The online encoder retains only a bounded prefix and its mode. It prepends and truncates, deletes the first retained bit if present, or copies. It never reconstructs discarded bits. Because operation histories are independent of bit values, the retained prefix center is the conditional mean of the physical score given the retained label. The exact calibration cancellation is therefore justified for the nominal decoder.

### 7.5 Oracle lower and final profile

Every physical tail remains fair under all operations. Conditional on at least one terminal mode of mass at least one half, level-`k` cylinders provide an ideal-score small-ball lower. The common-oracle inequality then implies that the actual acquisition variance plus actual atomic-law quantization cannot beat that ideal geometric scale. Combining the lower with the online construction gives

```text
delta^2 + E ell_{min(H_T,floor(log_2 M))}^2
```

up to universal constants.

This is a genuine joint acquisition-memory-calibration theorem. The ideal Cantor law is used only as a lower witness; it is not substituted for the atomic acquired law in the exact checkpoint identity.

### 7.6 Significance boundary

The example is mathematically sharp and resolves the r4 invariant-preparation limitation. Mode masses may begin at zero, appear, disappear, or vary arbitrarily with time. Expanding deletion and nonreset cross-mode transport are both present.

At the same time, the operation probabilities, prefix lengths, deletion frequency, metric weights, and terminal score are deliberately designed to make a strict positive squared-gain inequality available. This is an excellent feasibility and sharpness construction. It is not yet a theorem for a natural singular filtering or random-dynamical class already central to the literature.

---

## 8. Report continuity and resource transfer

The finite-horizon report comparison uses a shadow recursion driven by physical reports and successive measurable maximal couplings until the first disagreement. Before disagreement, the two controllers receive the same transcript and choose the same actions. The union bound gives

```text
TV <= min{1,(T L_J+L_Y)E_M}.
```

This is correctly stated for one prescribed finite horizon and the same declared controller, not as unrestricted policy optimization or infinite-path equivalence.

The morphism theorem distinguishes target labels, simulator states, controller states, phase/clock states, temporary workspace, program description, physical calls, and time. A serial implementation retains the tuple and hence has the constructive upper

```text
K <= M R D Q.
```

Complete interactive total-variation defect is charged against the same bounded scored outcome. Composition uses the total-variation triangle inequality and closure of the certified strategy class.

The executable continuation cut supplies a genuine converse when an exact post-cut challenge forces recovery of an interface tag. It correctly does not infer that every private simulator state is indispensable.

This section is conceptually sound, but its formalism remains more compressed than the rest of the paper. Before specialist publication, the measurable objects, parameter-uniform strategy classes, stopping conventions, transcript spaces, and compatibility maps should be given in a fully typed definition rather than primarily in prose. The existence of a jointly measurable maximal-coupling kernel should also be cited or isolated as a lemma.

---

## 9. Assessment against the controlling targets F1–F4

### F1 — Causal acquired-geometry transfer

**Substantially achieved as a sufficient theorem.**

The theorem begins at the experiment/kernel level, constructs a recursive encoder, uses actual acquisition geometry for the lower, and separates report continuity and resource accounting. The central r4 logical weakness has been removed.

The qualification is that the theorem remains sufficient rather than intrinsic: all-pair contraction, candidate-envelope drift, and global inward geometry are significant hypotheses.

### F2 — Resource-resolution-risk composition

**Partially achieved.**

The filter combines acquisition uncertainty, persistent labels, output precision, and calibration in one scored task. The singular theorem combines paid acquisition, persistent memory, and calibration in one exact law. The morphism theorem adds simulator/controller/clock/defect accounts constructively, and the interface challenge gives selected lower bounds.

There is not yet a matched optimal region for the full vector `(N,M,R,D,Q,W,L_prog,time,precision,deficiency)`. In particular, workspace, program length, arithmetic time, minimal simulator state, and complete causal deficiency do not enter one common matching upper/lower theorem.

### F3 — Singular or nonuniform extension

**Achieved in a meaningful explicit class.**

The singular realization has nonhomogeneous scales, expanding updates, nonreset tail transport, changing mode masses, finite actual acquisition, and no common invariant-preparation comparison. The filter adds arbitrarily long informative noncontracting realized runs.

What remains open is a theorem for a broader naturally occurring nonuniformly stable or changing-support class not designed around the certificate.

### F4 — Distinct raw-kernel realizations

**Achieved.**

The intermittent finite-state filter and finite-read singular symbolic experiment are genuinely different raw experiments. Neither is used as a premise of the general theorem.

---

## 10. Novelty and literature positioning

The manuscript responsibly disclaims novelty for conditional projection, nearest-center quantization, small-ball bounds, average contraction, classical filter quantization, predictive-state representations, experiment comparison, and nonanticipative information constraints. The new contribution is the specified coupling of:

- actual acquired score geometry;
- a constructed hard finite-label recursion;
- physical-report-law contraction;
- an inward candidate envelope;
- exact finite-acquisition decomposition; and
- typed resource transfer.

That coupling is nontrivial. I found no evidence in the supplied materials that the main theorem is merely a restatement of one cited result.

However, the bibliography and comparison table remain too narrow for the breadth of the title. At minimum, the revision should compare its operational object and conclusions with the following nearby routes:

1. M. Ghomi, T. Linder, and S. Yüksel, *Zero-Delay Lossy Coding of Linear Vector Markov Sources: Optimality of Stationary Codes and Near Optimality of Finite Memory Codes*, IEEE Transactions on Information Theory 68 (2022), 3474–3488, DOI `10.1109/TIT.2021.3138769`.
2. R. G. Wood, T. Linder, and S. Yüksel, *Optimal Zero Delay Coding of Markov Sources: Stationary and Finite Memory Codes*, arXiv:1606.09135 and its published descendants.
3. J. Subramanian, A. Sinha, R. Seraj, and A. Mahajan, *Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems*, JMLR 23(12) (2022), 1–83.
4. A. D. Kara, *Learning POMDPs with Linear Function Approximation and Finite Memory*, arXiv:2505.14879 (2025).
5. The subsequent agent-state and recurrent approximate-information-state literature, insofar as it treats recursively updated finite or compressed predictive states.

These works do not appear to supply the paper's exact actual-small-ball lower or its inward-cover theorem. That is precisely why a theorem-by-theorem comparison would strengthen rather than undermine the novelty claim. The paper should say explicitly how its hard retained-alphabet model differs from a finite observation window, a finite-state coding policy, an information-rate constraint, and an approximate information state measured only by one-step prediction errors.

An exhaustive independent priority determination is beyond a referee report. The present literature search nevertheless shows that the missing comparisons are close enough to be required before publication.

---

## 11. Major issues before specialist-journal publication

### 11.1 State the theorem's exact conceptual status in the introduction

The introduction should say in one sentence that the theorem is a **sufficient raw-kernel construction under a uniform all-pair square-moment contraction, a candidate Lyapunov envelope, and a static inward cover**. It is not a necessary condition, an equivalence, or a classification of finite-memory predictability.

The current scope section says this, but the condition should be visible before the broad foundational motivation.

### 11.2 Expand the closest theorem-level literature comparison

The finite-memory POMDP, approximate-information-state, zero-delay Markov coding, recursive filter quantization, and causal rate-distortion comparisons should be made at the level of assumptions and conclusions. A field-level sentence is not sufficient.

The comparison should address at least:

- finite window versus hard persistent-state cardinality;
- encoder/decoder coding state versus predictive quotient state;
- average or discounted control cost versus a fixed squared prediction task;
- upper approximation bounds versus actual acquired-law geometric converses;
- information rate versus a pointwise finite alphabet; and
- known kernels versus adaptive or learned models.

### 11.3 Fully type the morphism and complete-defect theorem

The resource theorem is important enough that it should not rely mainly on prose. Define the source and target transcript spaces, parameter-indexed kernels, declared strategy classes, lift, stopping compatibility, simulator state, clock map, terminal task map, and uniform defect as mathematical objects. Then state composition as a theorem within that formalism.

This will also make clear exactly when total variation is taken over the task variable, when the source and target Bayes baselines differ, and how the lifted adaptive policy remains in the certified class.

### 11.4 Add a precise measurable-coupling reference or lemma

The report-continuity proof invokes measurable maximal couplings of standard-Borel kernels. This is standard, but the parameterized measurability is load-bearing. A citation or self-contained lemma would remove an avoidable technical question.

### 11.5 Make the condition numbers prominent

The constants deteriorate as:

- `kappa -> 1`;
- `a -> 1`;
- the mixing probability or matrix entry floor vanishes;
- the observation Jacobian degenerates;
- the exponential-envelope parameter approaches its admissible boundary; or
- the cover ceases to be inward.

A compact table should identify these condition numbers and state which bounds are uniform in horizon, schedule, dimension, and model parameters. This would prevent readers from overinterpreting the uniform-in-`T` result as uniform near instability.

### 11.6 Separate exact Borel construction from finite implementation in theorem summaries

The manuscript already records the distinction in detail. It should be maintained consistently in the abstract, introduction, and theorem synopses. Borel cell membership and exact real-valued report processing are not finite workspace or finite communication. The certified enclosure discussion supplies a constructive route, but not a general complexity theorem.

### 11.7 Preserve the honest scope boundaries

The candid scope audit is a strength and should remain. In particular, no later revision should paraphrase the paper as proving:

- a necessary-and-sufficient memory criterion;
- optimal adaptive acquisition;
- unknown-kernel learning;
- arbitrary stopping-time transfer;
- an infinite-horizon transcript comparison; or
- a full multi-resource optimal region.

---

## 12. Technical and expository comments

1. In Proposition `prop:quotient`, distinguish more sharply between continuity of density-weighted instrument evaluations and continuity of the descended normalized update on the positive-density quotient domain.

2. In Theorem `thm:inward`, consider displaying the indicator-form expectation before conditioning on `D_t=1`. This makes the `vartheta_t=0` case and the use of conditional independence immediately transparent.

3. The phrase “static cover” should always be accompanied by “inward”; ordinary covering alone is not enough for the envelope induction.

4. The matching statement depends on the seed error scaling with `r_M`. Keep `e_0` visible in all summaries of the asymptotic law.

5. In the filter compander lemma, a one-line verification of the budget inequality for the largest `K` with `(2K-1)^d <= M`, including the smallest budgets, would improve readability.

6. In the filter lower, display the actual conditional density bound after change of variables, not only the determinant lower. This would make the dependence on `d,s,a` completely explicit.

7. In the output-grid lower, state explicitly the elementary comparison between `min(M,(2^b+1)^d)^{-2/d}` and `M^{-2/d}+2^{-2b}`.

8. The filter constants are dimension dependent. This is allowed, but every phrase such as “uniform over the class” should repeat whether `d` is fixed.

9. In the singular completed-domain lemma, keep emphasizing that finite-word centers are predictive states and are not physical Cantor points.

10. Label the rows and columns of the singular gain matrix by source and destination mode. The present calculation is correct but terse.

11. The sentence in the singular lower concerning “score diameter” is potentially ambiguous between the ball diameter and cylinder diameter. Rewrite it with both quantities named explicitly.

12. In the exact sign-minimax checkpoint identity, give the lower-by-averaging and upper-by-unbiased-conditional-mean steps in adjacent displayed equations.

13. The phrase “all waits and initial reads are charged” is correct. Retain the same convention in every table and abstract summary.

14. In Proposition `prop:report`, repeat the total-variation convention in the theorem statement, since the bounded-loss constant depends on it.

15. The serial product `MRDQ` is only an upper unless an executable challenge supplies a lower. This distinction is clear in Section 6 and should remain equally clear in the abstract and conclusion.

16. The source-binding evidence concerns the native paper subtree, not a complete repository checkout. The receipt states this correctly; preserve that exact language.

17. The absence of hosted CI is not a mathematical defect, but the final submission package should make reproduction from a clean checkout as simple as the current build command suggests.

18. The bibliography should prefer final published versions where they exist and identify preprint versions only when version-specific arguments were consulted.

19. The word “positive” for kernels means nonnegative and normalized in the paper, not uniformly bounded below. This is stated, but repeating it near later uses would prevent confusion.

20. The title “Foundations” creates an unusually high expectation of intrinsic breadth. The paper may retain the title, but the abstract and introduction should make the sufficient-class status unmistakable.

---

## 13. What would materially change the top-four assessment

Further polishing, more regression checks, or another purpose-built example would not by itself change the recommendation. A top-four case would require an advance of a different order, for example:

1. **An intrinsic criterion.** A necessary-and-sufficient, near-necessary, or dual characterization of when checkpoint geometry is recursively realizable with the same memory order.

2. **A natural hard application.** A theorem for a recognized nonuniformly stable filter, regime-switching nonlinear system, partially observed expanding map, or singular observation model whose finite-memory law was previously unresolved.

3. **Adaptive acquisition.** Matching bounds when the experiment itself is selected causally under a raw budget, including kernel learning, calibration, or stopping.

4. **A genuine multi-resource region.** One theorem with matching upper and lower bounds for several intrinsic coordinates beyond persistent labels and a selected output/calibration cut.

5. **A sharp converse to the all-pair sufficient conditions.** A result showing that failure of an appropriate intrinsic contraction/envelope invariant forces a separation between online and checkpoint curves in a broad class.

Any one of these could concentrate the architecture into a theorem of broad general-mathematics significance.

---

## 14. Final evaluation

Revision r5 is a serious and successful response to the preceding referee report. The authors have replaced an assumed recursive quantizer by an explicit raw-kernel construction, removed the common-reference/terminal-occupation premise from the new central theorem, formalized the relevant conditional law, retained the actual acquired distribution in the lower bounds, and streamlined the paper into a coherent twenty-page argument.

The main proof is elegant. A static inward cover controls quantization relative to a Lyapunov envelope; the true-law pair inequality controls propagation of old error; exact holds mix squared energies without an inverse activity loss; and actual score geometry supplies the converse. The intermittent filter and finite-read singular process verify the mechanism by distinct calculations. The singular theorem, in particular, gives a nontrivial exact acquisition-memory-calibration law under changing mode masses and nonreset expanding dynamics.

I found no elementary fatal error in the load-bearing arguments checked. The source/provenance pipeline is unusually careful and accurately limits what its finite tests certify.

The paper nevertheless remains below the exceptional threshold of the four leading general mathematics journals. Its main theorem is a strong sufficient principle rather than an intrinsic characterization. Its applications are instructive and nontrivial but still built around verifiable strict moment stability. The full resource programme, adaptive acquisition, and unknown-model problem remain open. The closest modern finite-memory and zero-delay coding literature also requires a broader theorem-level comparison.

Accordingly:

**Top-four general-journal recommendation:** reject in the present form.  
**Reason:** insufficient intrinsic breadth and natural-problem impact for that exceptional level, not an identified fatal correctness defect.  
**Specialist-journal outlook:** favorable after a focused major revision addressing the literature map, formal resource/morphism definitions, measurable coupling, condition-number presentation, and exact scope framing.
