# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r56-balanced-task-transfer-2026-10-14`  
**Reviewed exact branch head:** `a47d5f4c13bf93e82e7eaeef5dbb53c2c2a0c764`  
**Reviewed branch root tree:** `88aa2cf11c8d887ab352519e284ef374efbb23a5`  
**Ordinary mathematical-source commit:** `808ef512a73d5b1911257af2669a4e7ed97107ed`  
**Ordinary source tree:** `85495b8a2f77b1459530520548137e619fbe199b`  
**Stored binary artifact commit:** `5db80e9d1ffeb7345456ef3dedbb167d7bcdf926`  
**Hosted native PDF SHA-256:** `fd03113de038975377544ae1de95fade1cc88e97cba245c1a6147f1096a8c7bd`  
**Native article length:** 19 pages  
**Complete deposited packet:** twenty-eight PDFs, 688 pages  
**Predecessor external report:** R53 review head `e8eed6849b34afd200bf9532eaa1a68f32e9ee48`, report blob `9c86a6fe706ad991765720f48fb78dde6b597a2b`  
**Intervening author material:** completed R54 mathematics and R55 research contract  
**Review branch:** `review/general-theta-restart-r56-balanced-task-transfer-external-top4-referee-r56-2026-10-14`  
**Date:** 14 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof certificate, an independent priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

Unlike several earlier reports in this restart sequence, the present report identifies a **load-bearing model-semantics gap in the headline autonomous exact theorem**. The gap appears repairable, and it does not invalidate the checkpoint theorem, the all-strategy reference lower, the common balanced-program upper, or the raw classical and quantum verifications. It does, however, affect the claimed autonomous width `M-B`, the exact equality

```text
R_aut^Theta(N,B+m)=Q_m(N/kappa),
```

the assertion that the heralded interface requires at least three states, the Gaussian transition between one and two terminal values at total budgets three and four, and every corollary that substitutes `M-B` for the number of available terminal outputs.

The issue is precise. Proposition 4.4 proves that at least `B` distinct labels must occur while the observer is live in physically incompatible mandatory contexts. The proof of Theorem 3.1 then says that these live labels leave only `M-B` labels for terminal values. But the formal transducer model, as presently written, does not state that a label used while live is forbidden from also carrying a terminal readout after commitment. It says that the fixed alphabet includes every live routing state and every terminal value, and that command law and readout are determined by the state and current permitted input. It does not define a fixed state-only halt map or a disjoint partition of the alphabet into live and terminal types.

Under the natural reuse interpretation, the two-port gate can be run with two labels: a gate label `G` and an acquisition label `A`; gate failure remains at `G`, success moves to `A`, productive rejection returns to `G`, and productive acceptance halts while retaining `A` as the terminal output label. With two terminal outputs, acceptance can move to `G` or `A` and halt, while those same labels remain the two live routing labels on nonterminal paths. No history tape, seed, or uncounted persistent register is used. Therefore Proposition 4.4 alone does not prove that live and terminal roles consume disjoint labels.

If the intended model has a fixed halt/readout typing that makes every terminal label globally disjoint from every live label, that restriction must be stated as a primitive axiom before the autonomous value is defined. The theorem would then concern a typed absorbing-output automaton, not an arbitrary finite-state observer. If reuse is intended to be legal, the lower width must be replaced by an overlap-aware automaton invariant; the universally safe dictionary bound is at most `M`, not `M-B`.

Subject to that correction, R56 contains a coherent and useful stopped minimax transfer theorem. Its principal mathematical step is a clean quantifier split:

- one fixed admitted reference model supplies a lower bound against **every** legal competing strategy through actual report-count domination and an all-strategy effort inequality; and
- one parameter-independent task-balanced program supplies an upper bound for **every** model and every surviving history through equality of the joint report measure and unnormalized squared-loss measure.

This avoids the exact common finite primary row that carried much of R53. The lower and upper are not obtained by a minimax interchange, and the program does not store a true-model posterior. The proof of the checkpoint equality is, in my assessment, mathematically sound under the stated reference, balance, effort, and export hypotheses.

The negative top-four judgment is therefore based on two independent considerations:

1. the autonomous headline currently needs a formal correction or an explicit strengthening of the observer model; and
2. even after that correction, the theorem is a strong sufficient-class result built around a matched reference member and a common task-balancing operation, rather than an intrinsic or near-necessary classification of general causal acquisition.

For a strong specialist journal in mathematical statistics, stochastic control, information theory, quantization, selective prediction, absorbing control, or mathematical quantum information, I would regard a substantially revised paper as potentially publishable after the state-semantics issue is resolved and the novelty is repositioned against the trimmed-quantization literature.

---

## 1. Review object and pipeline inspected

A fresh complete enumeration of `referee-ready/general-theta-restart-*` branches identified

```text
referee-ready/general-theta-restart-r56-balanced-task-transfer-2026-10-14
```

as the latest completed referee-ready revision. The continuation page was empty. The external-review catalogue stopped at R53; no R56 review branch existed before this report.

The exact review object is the evidence-bound head

```text
a47d5f4c13bf93e82e7eaeef5dbb53c2c2a0c764.
```

Its sole parent is the stored binary artifact commit

```text
5db80e9d1ffeb7345456ef3dedbb167d7bcdf926.
```

The immutable mathematical source is

```text
808ef512a73d5b1911257af2669a4e7ed97107ed,
```

with reconstructed source tree

```text
85495b8a2f77b1459530520548137e619fbe199b.
```

I reviewed the 19-page native article as the editorial object. The twenty-seven retained PDFs were used for provenance and theorem ancestry, not treated as hidden premises of the native theorem.

The inspection included:

- `main.tex`, all twelve native section and appendix files, and `references.tex`;
- `README.md`, `REFEREE_RESPONSE.md`, `REFEREE_COMMENT_CONCORDANCE.md`, `THEOREM_MAP.md`, `PIPELINE_DERIVATION.md`, `PROOF_LEDGER.md`, `PROOF_AUDIT.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, `NOTATION_AUDIT.md`, and `PINNED_INPUTS.json`;
- the complete R53 external report and the R56 point-by-point response;
- the role of R54 as intervening author mathematics and R55 as a research contract rather than an external decision;
- the canonical restart charter, theorem targets, original outline, and predictive-quotient boundary;
- the source and binary-preservation receipts, independent rebuild, final validation, read-only verification, and referee packet; and
- targeted comparison with invariant decision theory, rejection/selective prediction, absorbing occupation measures, trimmed quantization, finite-memory POMDP reachability, and finite-command randomization.

The reconstruction records 1,301 unchanged source inputs, sixty-six isolated PDF builds in each TeX environment, three passes per build, 2,631 exact finite checks and 188 floating checks with identical ordinary and optimized Python output, and equal normalized text and rendered pixels for all twenty-eight PDFs and 688 pages. The PDF byte hashes differ across TeX Live versions, while repeated builds inside each environment are byte-identical. These controls are valuable source-integrity and reproducibility evidence; they are not mathematical proof, novelty certification, or journal acceptance.

I did not re-prove every historical companion, every v1--v96 theorem, or every independent realization branch. The repository's own history audit states the same limitation.

---

## 2. Executive mathematical assessment

R56 replaces R53's exact finite common primary driver by a reference-and-balance mechanism.

The experiment supplies a productive report and a later bounded audit `Z`. A fixed admitted model `theta_0` has a genuine report--audit law `K_0(dx,dz)` with report marginal `nu`, conditional mean

```text
f(x)=E[Z|X=x],
```

and residual squared loss

```text
w(x)=E[||Z-f(x)||^2|X=x].
```

At the same reference model, every legal observer satisfies an experiment-level effort inequality

```text
E C_tau >= kappa E A_tau,
```

where `A_tau` is the number of productive calls through commitment.

This gives a lower bound against every competitor. The terminal report measure `zeta` of any expected-cost-`N` procedure satisfies

```text
zeta <= E A_tau * nu <= (N/kappa) nu.
```

Hence its density relative to the actually acquired law is capped by `b=N/kappa`.

The upper uses one parameter-independent program `G`. On every history and every model, one attempt produces a virtual mark with law `nu` and balances the complete unnormalized squared-loss measure:

```text
E[1_{x in D} ||Z-T_j r||^2]
  = integral_D [w(x)+||f(x)-r||^2] nu(dx).
```

Accepting mark `x` with probability `h(x)/b` therefore gives a constant conditional hazard `1/b`, exact terminal loss, and expected core cost at most `kappa b` without any physical renewal assumption.

The resulting variational profile is

```text
Q_m(b)
 = min integral [w(x)+dist(f(x),C)^2] h(x) nu(dx),
```

where `|C|<=m`, `0<=h<=b`, and `integral h dnu=1`.

For checkpoint procedures, I find the lower and upper arguments persuasive. They keep the selected mass, use one actual reference model, and implement one common program for all hidden dynamics. The exact checkpoint equality in the export-invariant case is the strongest technically sound conclusion of the paper.

The autonomous theorem adds live-state accounting. Its upper with `B+D_0m` states is a valid construction. The lower replacement of dictionary width by `M-B`, however, requires the unresolved disjoint-role issue described above.

---

## 3. Response to the R53 external report

R56 makes real progress on several R53 objections.

| R53 issue | R56 assessment |
|---|---|
| Exact finite primary row common to all models carried the stopped flow | **Substantially resolved.** The lower needs one reference model; the upper needs one common task-balanced program, not a common primary row for every model. |
| Pointwise calibration required a positive residual-variance floor | **Resolved for the new theorem.** Balance is imposed on unnormalized report, first-moment, and squared-norm measures, and permits pure/zero-variance histories. |
| Mandatory state count depended on action names | **Improved.** Proposition 4.4 uses physical command intersections and is invariant under duplicated names and stateless recoding. |
| Full stateful-simulator invariance was absent | **Still open.** The paper expressly does not claim it. |
| Gate cost had to remain paid | **Resolved.** `kappa=1+1/p_0` is proved by predictable counts, including `p_0=1`. |
| Raw examples depended on a positivity floor `q` | **Resolved for the sign/Pauli examples.** Pure and rank-changing histories are allowed. The gate floor `p_0>0` remains essential. |
| A nonintervening natural application was requested | **Improved.** The Gaussian section keeps the target fixed and gives a one-value obstruction and uniform ratio-one large-budget asymptotic. |
| Exact output/state accounting was needed | **Not yet resolved.** The live/terminal disjointness needed for `M-B` is not formally stated. |
| Efficient implementation was missing | **Partially improved.** A finite-description approximation and a complete dyadic example are given; generic synthesis remains potentially exhaustive. |
| External top-four impact was not established | **Still unresolved.** The reference/balance class and examples do not yet solve a recognized broad natural problem. |

Thus R56 is not cosmetic. It supplies a new proof architecture. The remaining technical issue is narrower but affects the most strongly advertised autonomous equalities.

---

## 4. The all-strategy reference lower

### 4.1 Quantifiers

The lower uses one fixed `theta_0` that belongs to the uncertainty class. It is not chosen after observing a competing code, and it is the same witness used for the cost inequality and the mandatory-context certificate.

This is the correct minimax direction:

```text
inf_program sup_theta risk_theta(program)
  >= inf_program risk_theta0(program).
```

No minimax interchange is used.

The reference condition is strong but clearly stated. After every legal productive command and every surviving history, the report mark has law `nu`, and the full current report contains no further audit information beyond the conditional first and second moments derived from `K_0`.

### 4.2 Terminal measure domination

For each Borel set `D`, predictability and the reference row give

```text
E sum_{t<=tau, productive} 1_{X_t in D}
  = E A_tau * nu(D).
```

The report at commitment is one of those productive reports, so its terminal measure is dominated by the acquired report-count measure. Almost-sure commitment gives total mass one. The effort inequality then supplies the density cap.

The proof correctly establishes measure domination before taking a Radon--Nikodym derivative. It does not condition away failed attempts or normalize a rare favorable stratum to mass one.

### 4.3 Risk projection

Conditioning on the full current report, previous history, and chosen output gives the squared-loss decomposition

```text
E[||Z-r||^2 | full report, history]
  = w(X)+||f(X)-r||^2.
```

The fresh stop coin is conditionally independent of the audit, so report-dependent stopping does not invalidate the identity. Randomization among a fixed dictionary cannot beat nearest-center assignment.

I find the checkpoint lower correct under the stated witness assumptions.

---

## 5. The common balanced rejection upper

### 5.1 Joint task balance is the right object

The paper correctly insists that balancing only the report marginal is insufficient. Selection depends on the report, so a common upper requires equality of the unnormalized task-loss measure for every output value, not merely equality of primary report laws.

The finite moment criterion separates the required order-zero, first-moment, and squared-norm identities. This is a clean linear verification theorem for a specified finite command family.

It should remain explicit that this criterion is necessary and sufficient only inside the declared finite convex hull of commands. It is not a necessary condition for arbitrary history-dependent causal algorithms.

### 5.2 Conditional hazard, not renewal

Given a feasible `(C,h)`, each attempt accepts with probability

```text
integral h/b dnu = 1/b
```

conditional on every surviving history and every model. Rejection returns the observer's routing label to its start, but the physical hidden state need not reset.

The probability of surviving `j` attempts is therefore `(1-1/b)^j` by conditional hazards. Summing conditional expected attempt costs gives `kappa b`; summing unnormalized terminal losses gives the exact profile value.

This part of the proof is sound and does not assume independent attempts.

### 5.3 Export multiplicity

If command-dependent exports transform a virtual dictionary into at most `D_0m` physical outputs, the upper width expands accordingly. This is correctly charged.

The paper should emphasize in the theorem statement, rather than only afterward, that exact equality at width `m` additionally requires either `D_0=1` or an invariant dictionary under all export maps.

---

## 6. Major technical issue: live-state and terminal-state overlap

### 6.1 What Proposition 4.4 proves

For mandatory contexts `i` with legal physical command sets `U_i`, one live label that is reached in several contexts must have a fixed command distribution supported on their intersection. Covering the contexts by subsets with nonempty intersections gives a semantic lower `b_phys` on the number of distinct **live** labels.

This correctly eliminates artificial lower bounds obtained merely by duplicating command names.

### 6.2 What it does not prove

It does not show that those live labels cannot also be terminal output labels after commitment.

The proof of Theorem 3.1 nevertheless argues:

```text
there are at least B live labels;
therefore an M-state observer has at most M-B terminal values.
```

That implication needs a disjoint typing axiom.

The formal model currently says:

- the observer has one fixed alphabet of at most `M` states;
- the alphabet includes live routing states and terminal values;
- command law and readout are determined by state and current permitted input; and
- commitment occurs only after a productive report.

It does not say that a state with a terminal readout cannot have a live command in a different interface context, nor that halt is a fixed function of the state alone.

### 6.3 Explicit reuse construction

For the two-port gate, take labels `G` and `A`.

- At `G`, call the gate. Failure returns to `G`; success moves to `A`.
- At `A`, call the productive acquisition.
- On rejection, move to `G`.
- On acceptance with a single output, halt while retaining `A` and use its readout.

This uses two persistent labels, not three.

For two outputs, acceptance can halt in `G` or `A`, assigning the two terminal readouts to those labels. On nonterminal paths, the same labels continue to serve the two physical ports. No additional persistent state is present.

If the intended semantics prohibit this, the prohibition must be formalized. A standard way is to specify a fixed map

```text
halt:S->{0,1}
```

and require live states to have `halt=0` and output states to have `halt=1`, with no context-dependent interpretation. The theorem would then be correct for the resulting typed automaton model, assuming all other arguments hold.

### 6.4 Affected results

Until this is resolved, the following statements are unsupported as written:

1. `Q_{M-1}(b) <= R_aut(N,M)` from the mere existence of one live state;
2. the sharpened `Q_{M-B}(b)` lower;
3. exact `R_aut(N,B+m)=Q_m(b)`;
4. the declaration that the two-port gate is infeasible below three states;
5. `R_aut(N,3)=1` and the claim that two terminal values require `M>=4` in the Gaussian theorem;
6. autonomous regular-rate corollaries using `M-B`;
7. state-width components of the joint resource law.

The checkpoint theorem, the autonomous upper, and all risk lower bounds that use an explicitly supplied output dictionary remain intact.

### 6.5 Required resolution

The revision should choose one of two paths.

**Typed-state path.** Explicitly define terminal labels as globally absorbing/halt-typed and disjoint from live labels. Recheck every realization and resource statement under that model. Describe the resulting count as a typed protocol-state budget, not a presentation-independent minimal memory invariant.

**Reuse-permitted path.** Allow labels to carry live and terminal roles in different contexts. Replace `M-B` by a genuinely overlap-aware invariant of the complete transducer. At minimum, the safe terminal dictionary cardinality is `M`. The two-port and Gaussian thresholds must be recomputed.

This issue should be resolved before any specialist-journal submission, not left as a stylistic clarification.

---

## 7. Profile attainment and the relation to trimmed quantization

The compactness proof for `Q_m(b)` is correct. Dictionaries lie in compact `H^m`, repetitions allow fewer than `m` points, and feasible densities form a weak-star compact slice of `L^infinity(nu)`. Uniform continuity in the dictionary and weak-star pairing with a fixed bounded loss give attainment. The use of nets avoids an unjustified sequential compactness claim.

The left-continuity argument

```text
h_lambda=(1-lambda)h+lambda
```

is also correct for `b>1`.

However, the statistical geometry of `Q_m(b)` is close to the population formulation of **trimmed k-means / trimmed quantization**. A density cap `0<=h<=b` with unit selected mass is fractional trimming at retained mass `1/b`, with an added fixed mark `w`. The classical literature includes:

- J. A. Cuesta-Albertos, A. Gordaliza and C. Matran, *Trimmed k-means: an attempt to robustify quantizers*, Annals of Statistics 25 (1997), 553--576, DOI `10.1214/aos/1031833664`;
- L. A. Garcia-Escudero and A. Gordaliza, *Robustness Properties of k Means and Trimmed k Means*, JASA 94 (1999), 956--969, DOI `10.1080/01621459.1999.10474200`.

The paper need not concede that its causal theorem is contained there; it is not. But it should state clearly that the density-capped variational profile and optimal selection of low-distortion mass have a mature trimmed-quantization ancestry. The new claim is the exact paid causal realization and robust minimax transfer, not the population trimming functional by itself.

The same comment applies to the Gaussian threshold: selecting the smallest conditional variance at a fixed acceptance rate is a classical rejection/selective-prediction principle, as the manuscript already acknowledges.

---

## 8. Raw moment balance and singular instrument stability

### 8.1 Finite command criterion

For a finite command family, the order-zero, first-moment, and squared-norm measure identities are exactly what is needed to balance all squared losses after isometric exports. The proof by expanding the quadratic loss is correct.

If no mixture exists, compactness of the finite simplex and finite-dimensional separation give a finite inconsistent family of scalar moment constraints. This is a useful certificate for the declared command list.

The manuscript should avoid language suggesting that this is an intrinsic characterization of causal balance. It is a finite convex-hull test.

### 8.2 Integrated stability

The unnormalized classical or quantum instrument inequality

```text
integral ||A_x-B_x||_1 dx <= ||s-t||_1
```

follows from positivity, Jordan decomposition, and integrated mass preservation. The report total-variation and mass-weighted normalized-posterior bounds then follow without division by zero-mass reports.

This is the right stability notion for pure states and likelihood zeros. The paper correctly refrains from calling it a strict normalized-filter contraction or an expected-time bound.

---

## 9. Marked geometry and atomic transitions

The rectangle hypothesis for the actual pushforward

```text
sigma=(f,sqrt(w))_#nu
```

produces the two familiar obstructions

```text
b^(-2/alpha),
(bm)^(-2/(d+alpha)).
```

The lower arguments retain actual selected mass. The upper uses separated location centers and low-reliability rectangles at a common scale. The manuscript explicitly handles the large-`b` radius and packing conditions and treats bounded `b` uniformly over unbounded integer `m`; this responds correctly to the R53 comments.

The exact atom proposition also appears sound. An atom of mass `lambda` at zero task loss yields the exact threshold `b lambda >=1`. Below threshold, the remainder mass is retained and not renormalized away.

These calculations are valuable but inherited in substance. The article says so. Their presence supports self-containment rather than independent novelty.

---

## 10. Raw realizations

### 10.1 Gate cost

With gate success bounded below by known `p_0`, the common program reaches one productive call at conditional expected cost at most

```text
kappa=1+1/p_0.
```

Under the reference model with constant success `p_0`, predictable counting gives equality between expected productive and gate counts. This is valid without independent cycles.

The feasibility statement `N>=kappa` is correct as a cost statement. The associated state threshold is subject to the live/terminal issue above.

### 10.2 Controlled classical sign

A fresh fair identity/flip command makes the **post-command** sign fair for every incoming sign distribution. Linearity then balances the full joint report--audit law, not merely its report marginal.

The reference model prepares a fresh fair sign and remains invariant under each individual command. Hence it supplies the lower against arbitrary competitors, while the randomized command supplies a common upper for arbitrary hidden sign evolution between interactions.

This verifies the theorem without a positivity floor. It is also purpose-built: the target is the post-command audit. The paper correctly does not present it as free estimation of a pre-existing sign.

### 10.3 Quantum Pauli realization

Averaging the four Pauli commands maps every qubit state to `I/2`. The reference member prepares `I/2` and is invariant under each command separately. The subsequent equatorial instrument can have pure and full-rank posterior strata and noncommuting effects.

The audit of `sigma_z` is fair under the reference, producing the stated `f` and `w`. The proof uses unnormalized positive instruments and does not divide by a minimum eigenvalue.

I find this verification correct in finite dimension. As in the classical example, it is a charged post-command task, not an arbitrary unknown-state estimation theorem.

---

## 11. Gaussian nonintervening sensing

The Gaussian section is the most natural application in the native article.

For the fair reference sign,

```text
f(x)=tanh(a x/sigma^2),
w(x)=sech^2(a x/sigma^2).
```

The all-strategy lower selects a terminal report density bounded by `b` and minimizes the residual variance. Since `w` decreases with `|x|`, the optimal selected mass is the two-sided tail of probability `1/b`.

The common upper accepts the same two-sided tail and outputs `sign(X)`. Reflection symmetry gives the same conditional acceptance and unnormalized loss for either current sign and therefore for every history-dependent mixture.

The inequalities

```text
D(b) <= R <= U(b) <= 2D(b)
```

and the ratio-one asymptotic follow from the posterior identity and Gaussian tail concentration. The stated asymptotic constant is consistent with

```text
w(t_b) ~ 4 exp[-2(a/sigma^2)t_b],
t_b = a+sigma sqrt(2 log b)+o(1).
```

I did not find a defect in that argument.

The one-terminal-value minimax obstruction from the two static sign models is also correct. What changes after the state-semantics correction is the total number of labels needed to combine two live ports with one or two outputs.

The application remains elementary in its statistical content: a known two-point Gaussian experiment with reject/wait capability. The paper should present the novelty as the paid stopped minimax implementation and uniformity over finite-memory budgets, not as a new rejection principle.

---

## 12. Finite descriptions and the dyadic certificate

The relative-acceptance proposition correctly places approximation error on the rare-selection scale. An absolute one-attempt error `e` becomes relative error `be`, and terminal loss is divided by the actual acceptance probability.

The finite-description proposition correctly separates Borel existence from effective implementation. It requires certified report partitions, integration, probabilities, dictionary points, and execution costs. It is not an efficient synthesis theorem.

The dyadic example is useful because it records:

- a concrete gate floor and cost;
- a three-role implementation;
- finite coordinate precision and threshold integers;
- exact rational acceptance and loss bounds;
- persistent labels, read-only bits, scratch, call count, and physical-time upper bounds; and
- an independently derived all-program profile lower.

Its stated arithmetic is consistent with the displayed constants and the repository's exact finite checks. The example's use of three persistent labels again depends on the chosen typed-state implementation; it is a valid upper, not evidence that two labels are impossible.

---

## 13. Composition and the joint task

The typed simulator proposition correctly compares complete stopped/scored transcript laws, not just terminal outputs. It charges product states and demands a separate cost or drift certificate because terminal total variation cannot control waiting time.

The joint erasure/calibration theorem adds three lower contributions on a single task:

1. the core profile under the fixed reference model;
2. the erased fair sign, which remains conditionally fair throughout the core; and
3. a fixed calibration sign whose two alternatives have identical pre-audit laws.

The last two alternatives are combined correctly by averaging over the calibration signs while keeping the same core reference and erasure model. Thus the lower terms are not obtained from incompatible separately chosen models.

The early-report deficiency is indeed `epsilon` under the paper's total-variation convention: on the branch erased with probability `2epsilon`, an immediate independent fair replacement disagrees with the true sign with probability one half.

The risk lower's core dictionary has at most `M` coordinate projections and is therefore safe. The upper's explicit tagged construction is safe. Any claim that its state allocation is minimal would inherit the live/terminal role issue, but the manuscript labels it as a sufficient construction.

---

## 14. Predictive quotient and finite occupation appendix

The predictive quotient proposition explicitly assumes a Borel image, a Borel section, legal-domain fiber consistency, and representative-independent factorization. It proves minimality only for the declared executable tests. This is appropriately scoped.

The finite-occupation proposition is adjacent to classical absorbing-MDP occupation theory. The minimal Green occupation removes residual finite circulation that can exist only on zero-acceptance rows, preserving the terminal measure and reducing nonnegative costs. The proof is useful and appears correct under its legal-default and finite-occupation hypotheses.

It should remain separate from the main finite-state theorem. It neither produces a finite-memory implementation of an arbitrary Borel policy nor merges model-dependent policies into one unknown-model program.

---

## 15. Novelty, breadth, and top-four significance

Even after correcting the autonomous state semantics, the top-four case remains unpersuasive for the following reasons.

### 15.1 Matched reference and balance are strong sufficient hypotheses

The uncertainty class must contain a fixed reference model that is unpredictable in exactly the required sense after every legal productive command, and every competitor must obey the same effort inequality there. Separately, the physical interface must provide a single parameter-independent operation that balances the joint report and task-loss measures on every history and every model.

These assumptions are elegant and verifiable in invariant examples, but they are close to the desired lower and upper mechanisms. The paper does not give a near-necessary criterion for when such a pair exists.

### 15.2 The profile has classical trimmed-quantization ancestry

The density-capped selected-law problem is a marked form of population trimmed quantization. The paper currently credits inherited General Theta geometry and ordinary quantization/rejection tools, but it does not compare the variational profile with the foundational trimmed-k-means literature.

That omission makes the novelty appear broader than it is. The causal paid realization is new content; the selected-mass quantization functional is not an uncharted object.

### 15.3 The invariant realizations are designed around exact symmetrization

The sign flip and Pauli twirl examples are valid and useful, but the command set was chosen precisely to erase the input dependence relevant to the task moments. They do not demonstrate that an important uncontrolled physical system unexpectedly satisfies the theorem.

### 15.4 The natural Gaussian application is narrow

The Gaussian theorem is clean, but it concerns a known binary amplitude/noise experiment with a known gate floor and squared sign loss. It does not solve unknown-sensor learning, adaptive sensing, general sequential regression, or a recognized open finite-memory decision problem.

### 15.5 General synthesis and intrinsic memory remain open

The paper does not classify all history-dependent balancing strategies, does not supply invariance under arbitrary stateful simulation, and does not give matched lower bounds for program bits, workspace, precision, time, or minimal simulator state.

These are not defects in a specialist paper. They are decisive at the level of the title and a top-four general-mathematics submission.

---

## 16. Major revision requests

### 16.1 Formalize the autonomous transducer

Give a complete mathematical definition of:

- when the halt decision is made;
- whether halt is a fixed function of the retained state;
- whether a label may be used both live and terminal on different paths or in different physical contexts;
- whether the final readout is stored in the retained state or may depend on the current report; and
- whether physical protocol context is an external input to the transition/halt rule.

Then re-prove the autonomous lower from that definition.

### 16.2 Repair all affected state thresholds

Revisit Theorem 3.1, Corollary 3.2, Lemma 7.1, Theorems 7.2--7.3, Theorem 8.1, the dyadic example, and Theorem 10.2. Separate valid upper constructions from minimal-state conclusions.

### 16.3 Split the headline theorem

State the checkpoint exact equality independently. State the autonomous upper independently. State the autonomous exact equality only after the additional terminal/live typing hypothesis is formally introduced and named.

### 16.4 Put the reference and balance assumptions in the theorem title or first sentence

The result is not a theorem for arbitrary positive prepared kernels. It is a theorem for an admitted reference/effort witness and a common joint-task-balancing program.

### 16.5 Compare explicitly with trimmed quantization

Explain how `Q_m(b)` relates to population trimmed k-means and impartial trimming, and isolate the new causal realization theorem from the inherited variational geometry.

### 16.6 Clarify the status of the effort match

The lower needs `E C >= kappa E A` at the reference; the upper needs expected cost at most `kappa` per productive attempt. Exact equality of risk at budget `N` uses the same scalar `kappa` on both sides. Discuss what survives when the constants differ.

### 16.7 Give a failure theorem for absence of balance

The report-only counterexample is helpful. A stronger theorem or finite example should show that no parameter-independent finite-state program can attain the reference profile when the first task moment fails to balance.

### 16.8 Distinguish post-command and pre-command tasks in the abstract

The classical and quantum exact realizations balance post-command targets. The Gaussian section is nonintervening. That distinction should appear in the abstract rather than only in later scope text.

### 16.9 Sharpen the Gaussian novelty claim

State exactly which conclusion is new relative to R52 and to classical reject-option theory: zero-prior-floor robustification, paid attempts, the one-value obstruction, and uniform ratio-one asymptotics over all larger dictionaries.

### 16.10 Strengthen the natural-application layer

A top-four case would require a consequence for a recognized problem not engineered around a balancing group action—for example, a controlled sensing or quantum decision model in which balance is derived rather than built into the primitives.

### 16.11 Separate exact Borel and effective theorems visually

A theorem diagram should show which hypotheses are required for measurable existence, finite description, certified integration, and computational complexity.

### 16.12 Reassess the title

If the article remains centered on the reference/balance sufficient class, the title and abstract should make that class unmistakable. The current “Foundations” title suggests a broader intrinsic classification than is proved.

---

## 17. Technical comments

1. In Section 2, define terminal values as state labels, readout symbols, or state/readout pairs; the proof currently uses all three intuitions.
2. State whether the current permitted input includes the physical port identity. This matters for state reuse.
3. If terminal states are absorbing, state whether they possess legal command rows and whether those rows count in physical command intersections.
4. In Theorem 3.1, replace “every terminating observer must use at least `B` live states” by a formally defined typed-state hypothesis if disjointness is intended.
5. The general lower `Q_{M-1}` already assumes one label unavailable for output; justify this separately from Proposition 4.4.
6. The checkpoint upper uses a stopped acquisition program; clarify that its full-history memory is not counted but its terminal dictionary is.
7. In Lemma 4.2, state explicitly that a procedure commits exactly once; otherwise the terminal measure wording could be misread.
8. In Lemma 4.3, distinguish the expected cost of an attempt from the expected cost conditional on reaching the productive report.
9. In Proposition 4.4, command distributions, not individual commands, are selected. Explain why nonempty intersection of legal command sets is equivalent to existence of a common supported distribution.
10. In Proposition 5.1, state the dimension of the affine hull of `H` and phrase the first-moment identities in that affine hull.
11. The finite separating family in Proposition 5.1 is a finite set of scalar moment constraints; it is not automatically an efficiently found certificate.
12. In Proposition 5.2, say whether the dominating report measure is fixed for the two inputs or chosen pairwise. The inequalities themselves are representation independent.
13. The rectangle geometry assumes both upper and lower bounds for every location center in `K`; indicate whether examples satisfy them globally or only on a regular component.
14. In Proposition 6.2, explain the `m=1` below-threshold case separately; the displayed upper uses `m-1`.
15. In Lemma 7.1, “both ports require distinct live states” is valid; “therefore at least three total states” is not valid without terminal/live disjointness.
16. The phrase “charged within-call preparation” in the Pauli proof should not be confused with an additional physical call; state the exact call convention.
17. In the Gaussian theorem, separate the all-dictionary residual-variance lower from the one-value static-sign lower, since they use different admitted models.
18. The Gaussian uniformity over `M>=4` should be restated after correcting the state-count threshold.
19. In Proposition 9.2, the `b=1` case uses first-report acceptance. Confirm that finite partition approximation does not alter robust almost-sure commitment.
20. The dyadic example's equality `R_aut(161,3)=5/(161 pi)` depends on the autonomous exact theorem and therefore on the disputed state semantics.
21. In Proposition 10.1, state whether the simulator may stop the source before the target would stop; complete transcript total variation should encode the stopping time.
22. In Theorem 10.2, clarify whether the initial sign-call state can be reused inside the core under the chosen typed-state convention.
23. The predictive quotient appendix should use a distinct symbol from the task mark `x` when both appear in the same discussion.
24. The occupation proposition's notation `r=d\bar\xi/d\xi` should be introduced as a density and not confused with a task readout.
25. Add the trimmed-k-means references to the native bibliography rather than only an audit file.
26. The literature table should compare the paper's fixed-density-cap profile with the retained-mass parameter convention used in trimmed quantization.
27. The phrase “zero positivity floor” should always be qualified: there is no transition/variance/eigenvalue floor, but there remains a strictly positive gate floor `p_0`.
28. The abstract should say that exact autonomous state equality uses a mandatory typed-live-state certificate, if that is the repaired formulation.

---

## 18. What would materially change the general-journal assessment

Any one of the following would substantially strengthen the case:

1. an intrinsic necessary-and-sufficient balance criterion over all legal causal programs, not only a specified finite command family;
2. a semantically invariant finite-memory theorem that permits state-role reuse and is stable under general stateful simulation;
3. a natural nonintervening application resolving an open controlled-sensing, selective-prediction, or quantum-decision problem;
4. matching computational lower bounds coupling persistent states with program description, precision, workspace, and execution time;
5. a theorem deriving the reference/effort witness from primitive structural assumptions rather than assuming an admitted member; or
6. a broader state-dependent observation theorem in which joint task balance is approximate and the exact profile is recovered with a sharp stability modulus.

---

## 19. Final assessment

R56 is a mathematically serious revision. It replaces the most restrictive R53 assumption by a more flexible and conceptually cleaner pair of mechanisms: a one-model all-strategy converse and a one-program all-model implementation. The terminal-measure domination, joint task balance, conditional-hazard rejection rule, finite moment criterion, singular instrument estimate, checkpoint exact profile, and zero-floor raw realizations form a coherent article.

The present autonomous equality is not yet established under the written observer semantics. This is a concrete, localizable issue, not a vague objection. It can be repaired either by strengthening and clearly naming the automaton model or by developing a more intrinsic overlap-aware state invariant. The choice will affect several advertised thresholds.

Even after repair, I do not regard the current paper as meeting the breadth and external-impact standard of a top-four general mathematics journal. Its strongest abstract theorem remains a sufficient transfer theorem for experiments equipped with a matched reference member and a common joint-task symmetrization. The profile belongs near classical trimmed quantization, and the principal exact realizations are designed around finite group balance. The Gaussian example is natural but narrow.

My recommendation is therefore:

- **Top-four general mathematics journal:** reject in the present form.
- **Strong specialist journal:** potentially favorable after a major revision that repairs the autonomous state model, repositions the profile against trimmed quantization, and sharpens the natural-application claim.
