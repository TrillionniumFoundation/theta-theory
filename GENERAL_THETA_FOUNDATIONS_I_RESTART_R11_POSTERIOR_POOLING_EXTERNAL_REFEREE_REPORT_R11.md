# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r11-posterior-pooling-2026-10-08`  
**Reviewed exact branch head:** `e77c0aaedd5e3872b1e5348f5c78154ccc2ac479`  
**Reviewed branch root tree:** `b71d50ba7ba4253af4b83c0077af1456fd581d69`  
**Immutable mathematical-source commit:** `6ef290d21064b1e6514b343d3d451ad0a77e0c04`  
**Native mathematical source tree:** `f37f42455e99419d118156ecb122d9826e651c2d`  
**Complete PDF/artifact commit:** `4eb34d48cb7ba5b3fff9ad8cc958ce14a70fbda9`  
**R11 paper-directory tree:** `7704c91729b1a771428a700b316330e9e89ffbbe`  
**Main PDF blob / SHA-256:** `322e6e12eb072e8146958e1537d3e61c49df45d9` / `061c47d4e17e347176f4bfdc705c1bb1eb5bbaea3aeee39f3e82b0191d1af467`  
**Integral Supplement T blob:** `1bcabf5155e7ebe45c43fbbd4d322d2a31c4ae1d`  
**Integral Supplement S blob:** `9923114cedf6b692acdf06f1fc37c2d413478ecf`  
**Predecessor external report:** R10 review commit `6f3ca64beec4b054dba8cb5def1a6c69fbc46d52`, report blob `3b60c8fd6bd915dc8585c029478e83180f18a67e`  
**Review branch:** `review/general-theta-restart-r11-posterior-pooling-external-top4-referee-r11-2026-10-08`  
**Date:** 8 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof certificate, an independent priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This recommendation is **not a technical-correctness rejection**. Revision R11 is a major mathematical advance over R10 and substantially resolves the principal structural objection in the preceding report. The previous adaptive-completion theorem required separated response refinements. R11 treats genuinely overlapping noisy observations, optimizes the full-history sensor policy, and constructs an autonomous finite-state observer whose retained labels carry their true conditional posteriors under the implemented observer's own law. The resulting excess risk is represented exactly as a telescoping sum of Bellman–Jensen defects. A new integrated-curvature argument makes those defects second order even when the optimal action switches and the Bellman value is nonsmooth. The paper then supplies a uniform actual-posterior density converse, counts every phase-labelled state, derives its smoothing assumptions from raw continuous sensor kernels, and proves a strict analytic feedback advantage over every fixed two-sensor schedule.

In the load-bearing arguments I checked, I did not find an elementary gap invalidating:

- the deterministic-seed reduction for the optimized checkpoint problem;
- concavity, Lipschitz continuity and measurable minimization for the finite-horizon Bellman values;
- the all-incoming posterior aggregation identity;
- the exact Bellman–Jensen telescope;
- the integrated second-order Jensen estimate for nonsmooth concave values;
- the policy-uniform terminal density lower and resulting `M^{-2/d}` checkpoint converse;
- the complete `1+sum_t L_t` autonomous state count;
- the raw Bayes inverse, Jacobian and posterior-density bound for the continuous sensor family;
- the strict two-call observation-dependent sensor advantage;
- the facewise stratified extension and validation-channel realization;
- the finite-precision first-mismatch argument;
- the common-task calibration/early-deficiency construction; or
- the compact measurable predictive-realization proposition on its stated class.

The R10 report identified overlapping-noise adaptive sensing as the central remaining mathematical challenge. R11 answers that challenge on a nontrivial class. The reason the top-four recommendation nevertheless remains negative is now narrower: the theorem is still a finite-horizon sufficient principle for uniformly smoothing finite-state kernels and a full categorical squared-loss audit; its autonomous constant deteriorates explicitly with the horizon; its principal raw realization is a calibrated affine-likelihood family with uniformly positive transitions; and neither an intrinsic criterion nor a broadly recognized hard natural application is obtained. The mathematical combination is elegant and, in my view, publishable at a strong specialist level after revision. It does not yet have the intrinsic breadth, natural-problem impact, or concentration of novelty expected for the four leading general mathematics journals.

For a strong specialist journal in probability, information theory, stochastic control, nonlinear filtering, statistical decision theory, or quantization, my assessment is **strongly favorable after a focused major revision**. The central theorem and proof deserve serious consideration there.

---

## 1. Review object, provenance, and pipeline inspected

A fresh branch search immediately before creating this report identified R11 as the latest branch matching `referee-ready/general-theta-restart-*`. No R12 referee-ready branch was present. The exact reviewed head is

```text
e77c0aaedd5e3872b1e5348f5c78154ccc2ac479.
```

The final referee packet identifies the immutable mathematical-source commit

```text
6ef290d21064b1e6514b343d3d451ad0a77e0c04
```

and native source tree

```text
f37f42455e99419d118156ecb122d9826e651c2d.
```

The terminal referee-ready head is a verification/evidence child of the complete artifact commit. I reviewed the actual mathematical source at the pinned head, not an uncommitted working copy.

The inspection included:

- `main.tex`, all seven native section inputs, and `references.tex`;
- `README.md`, `REFEREE_RESPONSE.md`, `THEOREM_MAP.md`, `PIPELINE_DERIVATION.md`, `PROOF_LEDGER.md`, `PROOF_AUDIT.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, `NOTATION_AUDIT.md`, `RESEARCH_CONTRACT.md`, and `PINNED_INPUTS.md`;
- the canonical restart charter, theorem targets, foundational outline and realization-registry boundary;
- the complete R10 external report and R11 point-by-point response;
- the complete R10 article supplied as integral Supplement T and the complete earlier technical article supplied as integral Supplement S, insofar as they define the retained pipeline and prevent silent deletion or promotion of earlier results;
- `SOURCE_MANIFEST.json`, `verify.py`, `regression.py`, `build.py`, the build receipt, artifact-delivery record, independent rebuild record, final read-only verification and referee packet; and
- a targeted independent search of nearby belief aggregation, belief discretization, finite-memory POMDP planning, active sensing, information design, filter quantization and conditional-mean partition results, including recent work not yet discussed in the manuscript.

The delivery records report a sixteen-page main article, a forty-nine-page integral Supplement T, and a twenty-three-page integral Supplement S. The native audit records thirty-one manifested source members plus the manifest, fifty-one labels, seventy-three cross-references, nineteen bibliography entries and twelve formal statements. The native exact-rational suite contains 6,789 checks, including finite witnesses for posterior aggregation, physical path risk, the Bayes Jacobian, nonsmooth kink defects, strict feedback and the resource/deficiency formulas. Ten isolated builds per environment reproduce the main article and both complete supplements with their covers. Cross-environment PDF bytes differ, while normalized text and all eighty-eight rendered pages agree at the recorded resolution.

These are unusually careful source-binding and reproducibility controls. They do not prove the continuum arguments or originality, and the submission correctly says so. I inspected the verification and regression programs as evidence of what was checked, not as substitutes for the proofs.

I did not independently re-audit every theorem in v1–v96, every old review branch, or every separate realization article. Exact preservation of a Git tree is not fresh mathematical certification. The history ledger makes this limitation explicit, and I adopt the same boundary.

---

## 2. Executive assessment of R11

R11 replaces the strong-support-separation mechanism of the R10 main article by a different principle. Let `Q_t` be the true hidden-state posterior conditional on the finite retained label at phase `t`, and let `W_t` be the posterior after applying the label's selected action and observing the next physical report, before the next pooling cut. The observer partitions possible `W_t` values into finitely many cells and assigns one next label to each cell. Crucially, the representative attached to a cell is not a nearest grid point and is not an approximate copy of a discarded full-history filter. It is the actual conditional barycenter

```text
b_{t,j}=E[W_t | W_t in C_{t,j}]
```

under the law generated by the finite observer itself, pooling every incoming edge assigned to that cell. Hence

```text
b_{t,j}=Law(X_t | Z_t=j).
```

At each retained posterior, the observer uses an action minimizing the full-history Bellman value. If `V_t` is the optimal continuation risk from belief `p`, the paper proves

```text
E V_t(W_t)=E V_{t-1}(Q_{t-1}),
Q_t=E[W_t | Z_t].
```

The excess over the optimal full-history Bayes risk is therefore exactly

```text
sum_t sum_j {
  P(Z_t=j) V_t(E[W_t|Z_t=j])
  - E[V_t(W_t) 1{Z_t=j}]
}.
```

This is an exact information-loss identity. It does not compare an approximate filter pathwise with an exact filter, and it remains meaningful at policy switches because `V_t` is concave even when it is not differentiable.

The new analytic step is an integrated Jensen estimate. For a bounded-density measure on a compact interior carrier and a Lipschitz concave value, the sum of cellwise Jensen gaps over a grid of side `h` is `O(h^2)`. The proof integrates the distributional curvature of the convex function `-V_t`; it does not assume a bounded Hessian, a differentiable optimizer, or a margin separating competing actions.

Under a uniform acquired-smoothing condition for every incoming belief and legal action, Theorem `thm:pooling` obtains

```text
R_cp(n,M)-B_n^*  asy  M^{-2/d}
```

with horizon-uniform constants when the one-step kernel constants are uniform, and constructs an autonomous observer with

```text
S=1+sum_{t=1}^n L_t
```

total states and excess at most

```text
C sum_{t=1}^n L_t^{-2/d}.
```

Equal allocation gives

```text
R_aut(n,M)-B_n^*
    <= C n floor((M-1)/n)^(-2/d).
```

Thus the checkpoint and autonomous exponents match for every fixed horizon. The paper does not hide the corresponding `n^{1+2/d}` growth under equal allocation.

The raw sensor theorem is also a genuine improvement. Positive transition matrices and continuous affine likelihoods produce a full-dimensional posterior law with an explicit inverse and Jacobian. In the two-state case, the best second sensor changes with the sign of the first noisy report, and the manuscript proves a strictly positive analytic advantage over every fixed sensor sequence. This answers the central “overlapping noisy feedback” objection of the R10 report.

---

## 3. Response to the R10 external report

| R10 issue | R11 assessment |
|---|---|
| Adaptive completion required separated response supports | **Substantially resolved on a new class.** Uniformly smoothing overlapping-noise kernels are treated without any response-support gap. |
| The natural noisy examples had fixed acquisition order | **Resolved.** The raw two-state sensor has a genuinely observation-dependent optimal second action and a strict feedback advantage. |
| No mechanism unified action switches with second-order memory error | **Resolved.** Exact posterior barycenters remove first-order error, and integrated curvature handles nonsmooth Bellman envelopes. |
| Randomized-policy reduction and autonomous purification needed separation | **Resolved.** Lemma `lem:seeds` applies only to the optimized checkpoint relaxation and explicitly disclaims clock-free autonomous purification. |
| A finite controller might retain an uncharged exact posterior | **Resolved in the mathematical state model.** Execution retains only the phase-labelled finite state; exact barycenters are read-only programmed constants. Finite-bit realization is separately certified. |
| Every internal phase/action node had to be charged | **Resolved.** The state count is `1+sum_t L_t`; phases use disjoint state sets. |
| Planning existence and computational synthesis were conflated | **Resolved conceptually.** Bellman integration and programmed barycenters may be expensive; the article claims existence, while Section 5 gives only conditional finite-precision execution certificates. |
| Duplicate old mechanisms obscured the new theorem | **Improved substantially.** The native article is concentrated; complete older articles are delivered as integral supplements rather than interleaved into the new proof. |
| A natural noisy adaptive application was needed for a top-four case | **Partially resolved.** The continuous sensor example is genuine and analytically adaptive, but it remains a calibrated finite-state affine-likelihood model rather than a difficult natural filtering or sensing problem already central to the literature. |
| A near-necessary or intrinsic completion criterion was absent | **Still open.** R11 supplies a new sufficient mechanism, not a characterization unifying smoothing, separated refinement and continuation obstructions. |
| Horizon-uniform overlapping-noise matching was absent | **Still open and honestly displayed.** Only the fixed-horizon exponent is matched; the autonomous upper deteriorates with `n`. |
| Full computational-resource optimality was absent | **Still open.** Programme length, planning, scratch, runtime and simulator states have feasible accounts but no matched region. |
| The broad title required disciplined scope statements | **Improved, but the editorial burden remains.** The article states its boundaries clearly; the word “Foundations” still sets a higher intrinsic-breadth expectation than the main theorem currently meets. |

R11 is therefore not a cosmetic response. It resolves the most important actionable mathematical criticism in R10. The remaining negative top-four judgment should not be described as a repetition of the R10 objection.

---

## 4. Audit of the causal posterior-pooling theorem

### 4.1 Procedure classes and independent randomization

The checkpoint and autonomous classes are separated correctly. A checkpoint procedure may use the full acquired history during sensing and compress only at the terminal cut. An autonomous procedure must choose each action and final forecast from its current finite state. There is no free elapsed-time register, old report tape or private persistent random seed.

For a fixed deterministic full-history policy, conditional projection gives the exact checkpoint identity

```text
B_n^pi + q_M(nu_n^pi).
```

Lemma `lem:seeds` conditions on the entire independent seed only as a relaxation of the full-history checkpoint problem. For each fixed seed one has a deterministic policy/code, so randomization cannot beat the joint deterministic infimum. The manuscript explicitly does not use this argument to purify a randomized autonomous controller, where a fixed time-indexed tape might itself carry uncharged state. This distinction is correct and important.

### 4.2 Bellman values, concavity and measurable selectors

A fixed future policy and terminal forecast have risk affine in the incoming hidden-state distribution. The infimum over fixed future policies is therefore concave. Because the categorical squared loss is bounded and its coefficients are uniformly bounded, the stated Lipschitz bound in simplex coordinates is valid. Finite action sets and continuity in the incoming belief give a measurable minimizing action with deterministic tie-breaking.

The proof does not require the optimizer to vary continuously. This is essential: the raw realization deliberately has an action switch at posterior probability one half.

### 4.3 All-incoming posterior calibration

Lemma `lem:aggregation` is the load-bearing probabilistic identity. Suppose the old finite label `I=i` has actual conditional hidden distribution `p_i`. After choosing the programmed action and observing the report, the Bayes update `W` is exactly

```text
Law(X' | I,Y).
```

If the next label records only the cell containing `W`, then for each hidden coordinate `k`,

```text
P(X'=k,J=j)=E[W_k 1{W in C_j}].
```

Dividing by the actual cell mass gives the cell barycenter. This pools all incoming labels assigned to the cell. An edgewise representative without the incoming-edge identity would not be a sufficient next-state posterior; the manuscript does not make that mistake.

The forward construction of cell masses and barycenters is not circular. At phase `t`, the old finite distribution and instructions are already fixed. One pushes that finite mixture through the known physical kernels, partitions the resulting posterior law, and records the next finite mixture. Future labels are not needed to define the current law.

### 4.4 Exact Bellman–Jensen telescope

At a retained posterior `Q_{t-1}`, the selected action minimizes the full-history Bellman recursion. Conditional on the finite state,

```text
E[V_t(W_t) | Z_{t-1}]
    = V_{t-1}(Q_{t-1}).
```

The aggregation lemma gives

```text
Q_t=E[W_t | Z_t].
```

Therefore the increase caused by forgetting the precise `W_t` within its cell is exactly the Jensen gap

```text
E[V_t(Q_t)-V_t(W_t)].
```

Summing over phases telescopes from `V_0(p_0)=B_n^*` to the actual terminal risk `E[1-||Q_n||^2]`. No claim is made that `W_t` is the full-history posterior after discarded observations. It is the posterior generated from the information actually present before that report, which is the correct object for the implemented machine.

I found this argument coherent. It is the conceptual center of R11.

### 4.5 Integrated curvature and the second-order rate

The integrated Jensen lemma deserves attention because it replaces the usual first-order Lipschitz estimate. For smooth convex `f=-v`, the proof subtracts a tangent at the center of each small cube. The resulting nonnegative convex function `w` vanishes at the center. Subharmonic averaging and radial convexity give a local bound of the form

```text
sup_C w <= C h^(2-d) ∫_{B_{Ch}} Δf.
```

The cell mass is at most `rho h^d`, so the cell contribution is bounded by `C rho h^2` times the local curvature mass. Expanded grid balls have bounded overlap. A fixed cutoff supported inside the ambient open set bounds total curvature on the compact collar by the Lipschitz constant through distributional integration by parts. Mollification then passes the bound to nonsmooth convex functions.

The dimension bookkeeping is correct: the factor `h^d` from actual mass cancels the `h^{-d}` part of the local mean estimate and leaves `h^2`. No lower bound on cell mass is needed. Because the estimate integrates the positive curvature measure, action-switch hypersurfaces do not create a first-order loss.

For publication, I recommend expanding two transitions: the normalized spherical/ball mean inequalities leading to the local curvature formula, and the distributional cutoff argument after mollification. These are matters of exposition and independently checkable constants, not identified gaps.

### 4.6 Autonomous state count

Each phase uses a disjoint label set, and the initial state is separate. Thus the total number of possible persistent states is exactly bounded by

```text
1+sum_t L_t.
```

The label itself determines the phase, action instruction, Bayes routine, next-cell map and terminal readout. No free phase counter is used. This is the right comparison with an autonomous finite-state controller, not merely a bound on the number of terminal cells.

### 4.7 Policy-uniform lower bound

The lower is also stated at the correct quantifier level. Immediately before the last action/report, an arbitrary full-history policy has selected some incoming belief and legal action. Uniform acquired smoothing applies to every such pair, including random pairs generated by the policy. Conditional posterior laws have density at most `rho`; mixing them preserves the same bound. Consequently the actual terminal posterior law under every policy has a uniform small-ball bound.

The union-of-balls argument then gives `q_M >= cM^{-2/d}`. Since `B_n^pi >= B_n^*`, optimizing acquisition cannot evade the memory lower. The categorical one-hot squared audit makes the posterior itself the conditional mean and gives the exact projection decomposition. This is an actual-law converse, not a packing of a formally reachable belief set.

### 4.8 Exact scope of the theorem

The theorem is strong but specialized. Uniform acquired smoothing requires every legal action from every incoming belief—including compressed beliefs—to produce a full-dimensional posterior law on one fixed compact interior carrier with a uniform density upper bound. This excludes discrete observations, low-dimensional sensors, nearly revealing reports, boundary concentration and many degenerate filters unless they are separately stratified. It is not merely “positive noise.”

The matching autonomous conclusion is also fixed-horizon. Equal allocation yields approximately

```text
C n^(1+2/d) M^(-2/d)
```

rather than a horizon-uniform constant. This distinction is displayed honestly and is central to the top-four assessment.

---

## 5. Audit of the raw continuous-sensor realization

### 5.1 Posterior inverse and density

With `q=pT` and

```text
D=1+lambda sum_{j=1}^d q_j y_j,
```

the posterior coordinates are

```text
u_0=q_0/D,
nu_j=q_j(1+lambda y_j)/D.
```

Uniform positivity of `T` gives `q_j>=tau`; `D` lies in `[1-lambda,1+lambda]`. Every posterior coordinate is therefore bounded below by the displayed `kappa`.

The inverse

```text
y_j=lambda^(-1)(q_0 u_j/(q_j u_0)-1)
```

is correct, and differentiation gives

```text
det(du_1,...,du_d)/d(y_1,...,y_d)
   = lambda^d product_j q_j / D^(d+1).
```

Multiplying the report density `D/2^d` by the inverse Jacobian yields the displayed posterior density

```text
D^(d+2)/(2^d lambda^d product_j q_j),
```

uniformly bounded by `rho`. This verifies smoothing for every incoming belief and declared action, not merely along one exact-filter path.

### 5.2 Predictive minimality

When an invertible legal transition is available, next-report means recover the transitioned belief and hence the incoming belief. Together with phase and the terminal categorical audit, this separates relevant beliefs. Conversely equal beliefs generate equal future controlled laws. The result is correctly framed as a sufficient predictive realization for the declared experiment, not as a universal minimality statement for every parameter family.

### 5.3 Strict feedback advantage

In the two-state specialization, the one-step information term has a positive even-power expansion. The plus and minus sensors exchange under `q -> 1-q`, so their risk difference changes sign at `q=1/2`. After the first plus sensor from the symmetric preparation, the sign of the next predicted belief's displacement from one half is the sign of the continuous noisy report. Both report half-intervals have positive probability. Selecting the second sensor from that sign therefore strictly improves upon either fixed second sensor.

The manuscript goes beyond a qualitative argument and gives a positive analytic lower bound. The comparison includes fixed sequences starting with the other sensor by symmetry. Both hidden states retain positive posterior mass after every finite report, so the example genuinely lies outside separated-support refinement.

### 5.4 Significance boundary

This is a real adaptive noisy-sensing example and should not be dismissed as another digit-revelation construction. Nevertheless it is deliberately calibrated: finite hidden state, uniformly positive transitions, affine likelihoods on a cube, known kernels, a finite sensor family and the full categorical Brier audit. The example verifies the theorem cleanly; it does not settle a recognized difficult natural problem in nonlinear filtering, experimental design or controlled sensing.

A stronger top-four case would require the mechanism to survive in a broader natural class—for example, a nontrivial exponential-family or nonlinear observation model with endogenous degeneracy, an infinite or growing hidden state, unknown/calibrated-on-line kernels, or a setting in which the finite-memory rate was already a recognized open problem.

---

## 6. Stratified acquisition and changing rank

The facewise extension is mathematically consistent. Each one-step posterior law decomposes into finitely many actual subprobability laws supported on compact relative-interior carriers. Positive-dimensional components have density bounds in their affine coordinates; vertices are encoded exactly. Pooling is performed separately within each face, so conditional barycenters remain in the same face and the aggregation identity continues to hold. The phase and face identity are included in the state label.

The terminal lower uses an actual `r`-dimensional submeasure of mass at least `w` and density at most `rho_*`. The resulting factor

```text
w^(1+2/r) rho_*^(-2/r) M^(-2/r)
```

is the correct union-of-balls scale for an unnormalized submeasure. The proof does not normalize rare-stratum mass away.

The validation example gives genuine vertex atoms on validated reports and a continuous posterior component on nonvalidated reports. A positive transition can move a vertex posterior back into the interior before the next noisy observation, so the recursion repeatedly changes acquired rank. Substituting the actual continuous mass and subdensity into the lower yields the stated linear factor in `1-theta_n`.

The limitation is that the stratum family is finite, relative-interior margins are fixed, and the lower is controlled by a terminal positive-dimensional stratum. Degenerating, countable or dynamically accumulating strata are not covered.

---

## 7. Digital implementation, causal comparison and the joint task

### 7.1 Typed causal comparison

The morphism statement correctly requires a parameter-independent causal simulator, a specified target strategy class, compatible actions and clocks, simulator memory, complete joint stopped/scored law, and a common bounded loss. Matching report marginals alone is not enough. Product state overhead and additive complete-law defects are constructive upper accounts. Reverse risk transfer requires a reverse certificate covering the source strategy class being lower bounded.

### 7.2 First-mismatch implementation bound

The digital proposition recomputes pooling barycenters under the programmed controller rather than retaining barycenters from a different ideal policy. Bellman action slack enters additively in risk units. While ideal and digital labels agree, they issue the same action. A coordinate approximation changes a grid label only when the ideal posterior lies near a grid hyperplane. Uniform actual density bounds the total slab mass by `C_d rho beta_t/h_t`.

The proof uses the unconditioned ideal posterior law and intersects its boundary event with the no-previous-mismatch event. It does not incorrectly assume that conditioning on survival preserves a density bound. This is the right first-disagreement argument. Kernel calibration errors, numerical failure events, boundary mismatches and terminal readout error are kept distinct.

The result remains conditional on certified approximations to Bellman values, posterior coordinates and barycenters. It does not give an algorithm for obtaining those certificates in every Borel model. The manuscript says this explicitly.

### 7.3 Calibration and early-channel deficiency

The direct-sum audit places hidden-state prediction, an inaccessible calibration sign and an early erasure bit in one actual task under one product prior. The hidden-coordinate lower remains valid with unrelated side information; the sign contributes `delta^2`; and an erasure of probability `2 epsilon` leaves squared bit risk `epsilon/2`. These lower terms genuinely add under the same prior.

For the upper, retaining three channel statuses together with the phase-labelled pooling controller gives the safe count `4+3nL`. The early deadline prevents the simulator from using the terminal audit to repair the bit. The total-variation distance between the two source bit laws is `1-2epsilon`, while exact target bit laws have distance one, giving the matching deficiency lower `epsilon`. The construction correctly distinguishes an attained defect from a mere permitted tolerance.

---

## 8. Measurable predictive realization

The appendix does not assume that an arbitrary quotient of a standard Borel history space is standard Borel. Histories are covered by countably many compact metrizable pieces, and a countable determining family of continuous executable-test coordinates maps each piece into a compact subset of a countable product. The total image is `F_sigma`, hence standard Borel.

The nested compact-set construction supplies a Borel section on each compact image, and the least-piece convention supplies one on the union. Fiber equality includes legal interface and all executable continuation expectations. Statistics from which the coordinate map is recoverable factor onto the predictive state; Borel functions constant on fibers factor back through the section. Jointly defined fiber-constant kernels and updates descend measurably.

This is a sound sufficient realization theorem. It is not a general theorem about arbitrary conditional-law versions, and the paper does not represent it as one.

---

## 9. Assessment against the controlling targets F1–F4

### F1 — Causal acquired-geometry transfer

**Substantially achieved on a new overlapping-noise class.**

The theorem begins at controlled experiment kernels, optimizes the full-history policy, constructs a finite autonomous observer, obtains an exact information-loss identity and uses actual acquired geometry for a matching memory exponent. It materially advances the mother problem.

The qualification is that uniform full-dimensional smoothing and fixed horizon are strong structural restrictions. F1 is not converted into an intrinsic characterization.

### F2 — Resource–resolution–risk composition

**Partially achieved, with meaningful new content.**

Persistent state, phase, programme, scratch, physical calls, numerical precision, calibration error, simulator state and scored-law defect are separated. The joint example gives an attained same-task profile for memory, calibration and deficiency.

There is still no matched optimal region for programme length, planning cost, scratch, execution time, precision, simulator state and sensing calls. Most non-memory coordinates receive feasible upper accounts rather than lower bounds.

### F3 — Singular extension

**Achieved for finite nondegenerate strata.**

The theorem handles vertex atoms and positive-dimensional faces in one exact posterior recursion, preserving actual submass. The validation realization repeatedly changes rank.

Countable, degenerating and infinite-dimensional stratifications remain outside the result.

### F4 — Distinct raw-kernel realizations

**Achieved.**

The continuous positive sensor and the validation/noise hybrid verify the new theorem from raw kernels. The graph-directed separated realization and earlier filtering/singular mechanisms remain mathematically distinct integral supplements rather than circular premises.

---

## 10. Novelty and literature positioning

The manuscript responsibly disclaims novelty for Bayesian filtering, belief-state dynamic programming, conditional expectation, concavity of Bayes risk, ordinary quantization and classical experiment comparison. The new mathematical combination is:

1. exact calibration of each finite retained state by pooling all incoming posteriors under the implemented controller's actual law;
2. an exact Bellman–Jensen loss identity for adaptive sensing;
3. a second-order integrated-curvature bound valid at nonsmooth action switches;
4. a policy-uniform actual-posterior density converse;
5. complete phase-labelled autonomous state accounting; and
6. a raw overlapping-noise sensor verification with strict feedback advantage.

I found no cited theorem in the supplied materials that simply contains this combination.

The current comparison section is much improved, but it omits several close routes that should be discussed before publication.

### 10.1 Adaptive belief discretization

D. Grover and C. Dimitrakakis, *Adaptive Belief Discretization for POMDP Planning*, arXiv:2104.07276, construct depth-dependent belief covers, derive planning-error bounds and quantify planner memory. This is close to R11's use of phase-dependent label allocations. The important differences are that their representative beliefs approximate a planning tree and yield Lipschitz-type value error, whereas R11 calibrates every deployed label to its actual conditional posterior, obtains an exact Jensen telescope and proves an actual-law memory converse. These distinctions should be made explicitly rather than relying only on the older covering-number citation.

### 10.2 Feature-based belief aggregation

Y. Li, K. Hammar and D. Bertsekas, *Feature-Based Belief Aggregation for Partially Observable Markov Decision Problems*, arXiv:2507.04646, study finite-state POMDP belief aggregation using representative beliefs and dynamic programming, with approximation-error bounds and lower-bound conditions. It is a particularly close modern antecedent in vocabulary and mechanism. R11 differs in finite-horizon causal execution, exact posterior barycenters under the deployed machine, nonsmooth integrated curvature, hard total-state accounting and geometric lower bounds. A theorem-level comparison is required.

### 10.3 Coarse information design and curvature-weighted partitions

Q. Lyu, W. Suen and Y. Zhang, *Coarse Information Design*, arXiv:2305.18020, analyze finite signal spaces in which induced signals are conditional means and optimal cutoffs depend on value-function curvature. Their problem is static information design rather than causal finite-memory sensing, but the conditional-mean/curvature architecture is close enough that it should be acknowledged. R11's novelty claim should explain that its cells are fixed global execution cells, its barycenters are generated under an endogenous controlled law, and its theorem provides a causal autonomous implementation and actual-law converse rather than an optimal static persuasion partition.

These omissions do not establish that R11 lacks novelty. They prevent the current manuscript from supporting a fully mature priority and positioning claim. The independent search was targeted, not exhaustive, and should not be treated as a priority certificate.

---

## 11. Major issues before specialist-journal publication

### 11.1 State the conceptual status of uniform acquired smoothing more sharply

The introduction says that the theorem treats overlapping noise, which is true. It should also say immediately that it assumes a uniform full-dimensional density bound on one fixed compact interior carrier for every incoming belief and legal action. Many overlapping-noise experiments do not satisfy this condition. The theorem is not an arbitrary positive-noise result.

### 11.2 Separate the general pooling identity from the task-specific rate theorem

The exact posterior aggregation and Bellman–Jensen identity have broader conceptual scope than the final `M^{-2/d}` law. The latter uses a full categorical squared audit and a full-dimensional terminal posterior law. The manuscript should distinguish explicitly:

- the general exact information-loss identity;
- the analytic curvature upper;
- the categorical projection identity; and
- the full-rank small-ball converse.

This would clarify what survives for lower-rank or nonquadratic decisions.

### 11.3 Add the closest aggregation/discretization/information-design comparisons

The three works discussed above should appear in the paper's theorem-level comparison. The comparison should address representative-belief calibration, depth-dependent covers, exact versus approximate dynamic programming, conditional means, curvature, deployed controller state, and actual-law converses.

### 11.4 Clarify the horizon dependence as a mathematical problem, not a constant issue

For equal allocation, the autonomous upper grows as `n^{1+2/d}M^{-2/d}`. The paper correctly states this, but the conclusion should emphasize that overlapping-noise completion is not yet horizon-uniform and that the gap from the checkpoint constant may be structural or an artifact of disjoint phase allocation. A lower or improved construction addressing this question would materially strengthen the work.

### 11.5 Explain whether phase-disjoint pooling is close to optimal

The full phase count is honest, but it is only one construction. Can states from different phases be merged while preserving posterior calibration and legal action interfaces? Can a lower force phase overhead in any nontrivial class? Even a formal discussion separating necessary phase information from a safe disjoint union would improve the resource interpretation.

### 11.6 Strengthen the natural-application case

The affine sensor family is an excellent verification model, but the paper's broad title would benefit from one application less tightly designed around an explicit inverse. A theorem for a standard controlled observation family—multinomial-logit, general exponential-family, Gaussian location with state-dependent actions, or another recognized sensing model—would demonstrate that the raw Jacobian mechanism is robust rather than bespoke.

### 11.7 Keep abstract programme existence visibly separate from finite computation

Section 5 is careful, but headline phrases such as “finite causal observer” can still be read as a finite-bit algorithm. The main theorem permits exact known real barycenters and Bellman integrals in read-only instructions. The digital proposition is conditional on certified approximations. The abstract cardinality theorem and computable deployment theorem should remain separately named in the abstract, introduction and conclusion.

### 11.8 Reconsider the submission architecture and title

A sixteen-page article accompanied by seventy-two mathematical pages of two integral supplements is a substantial package. The preservation discipline is commendable, but an editor needs a clear statement of which theorems are part of the present submission's novelty claim and which are retained record. The title “Foundations” continues to imply an intrinsic general theory. Either the title should be narrowed or the introduction should make the sufficient-class architecture unmistakable on the first page.

---

## 12. Technical and expository comments

1. In Theorem `thm:pooling`, state next to the constants whether `C` is the same symbol in the checkpoint and autonomous bounds or merely a reusable class-dependent constant.

2. Give the elementary inequality converting `k_t=floor(L_t^{1/d})` into `h_t^2<=C L_t^{-2/d}` once, including the role of `L_0`.

3. In Lemma `lem:integrated`, explicitly note that for sufficiently small `h`, the centers of every cube meeting `K` and all enlarged balls lie in the fixed compact collar inside `Omega`.

4. Expand the derivation from subharmonic averaging and radial convexity to equation `localcurvature`. The current proof is credible but unusually compressed at its most novel analytic step.

5. State the distributional integration-by-parts identity used with the cutoff after mollification and indicate why no boundary term survives.

6. In the Bellman continuity argument, spell out that strict positivity of the report density makes the normalized update continuous in `p` for each report, while `2 sum_j f_j` gives the integrable dominator.

7. In Lemma `lem:aggregation`, keep emphasizing that the same next label pools all incoming old labels. This is the main distinction from nearest-neighbor belief rounding.

8. In the theorem proof, display the complete telescoping chain over `t`, rather than only its one-step equality. It would make the exact identity easier to verify independently.

9. In the lower-bound paragraph, state explicitly that a random full-history last action produces a mixture of conditional posterior laws and that a convex mixture of densities bounded by `rho` remains bounded by `rho`.

10. Clarify the existence of an optimal full-history policy used for the checkpoint upper. Finite action sets and continuity appear sufficient; one sentence would remove any ambiguity about using an unattained infimum.

11. In Theorem `thm:sensors`, the notation `(f_0,f_1)=(1,1+lambda y)/2` is standard but visually ambiguous. Write the two entries separately.

12. In the Jacobian calculation, specify that the determinant is positive on the report cube and that boundaries are null, so ordinary change of variables applies without multiplicity.

13. In the minimality statement, identify the legal invertible action whose next-report mean is used and explain how known coordinate permutations are inverted.

14. In the strict feedback proof, place the derivation of the explicit lower constant nearer the two half-interval estimates. At present the final constant is correct but terse.

15. In Theorem `thm:strata`, say “conditional immediately before the final action/report” when stating the uniform terminal mass assumption, matching the quantifier used in the full-dimensional lower.

16. In the validation corollary, give one displayed line showing how `w=1-theta_n` and `rho_*=(1-theta_n)rho` reduce the general lower to a linear factor in `1-theta_n`.

17. In Proposition `prop:digitalpool`, distinguish coordinate sup error from task-norm output error in the notation as well as prose.

18. The grid-boundary union has order `d/h_t` hyperplanes. Recording the elementary slab-volume calculation would make the `beta_t/h_t` factor transparent.

19. The phrase “projection at the terminal label adds exactly its squared readout error” relies on the ideal barycenter being the conditional mean. Cite that identity directly at this point.

20. In Corollary `cor:jointpool`, state explicitly that the early bit and sign are independent of the hidden preparation, so action dependence on these side variables can only select among policies already bounded below by `B_n^*`.

21. Repeat the total-variation convention in Proposition `prop:morphism`, because the bounded-loss constant and the exact early-channel deficiency use it.

22. In the quotient appendix, the phrase “maps onto `S` through `g`” should be read on the range of the statistic. A slightly more typed factorization statement would help.

23. The bibliography should add the recent aggregation/discretization/information-design works or explain their exclusion.

24. The conclusion should repeat that the raw sensor theorem assumes known kernels and a fixed finite action family. Nothing in R11 is a learning theorem.

25. Preserve the current language that build and regression evidence concerns the complete submitted packet but not every historical paper or every continuum proof.

---

## 13. What would materially change the top-four assessment

Further proof polishing, additional finite regressions, or another affine sensor example would not by itself change the recommendation. A top-four case would require an advance of a different order, for example:

1. **An intrinsic completion criterion.** A necessary-and-sufficient or near-necessary condition explaining when conditional-barycenter pooling, separated refinement, continuation geometry or another mechanism yields autonomous/checkpoint equivalence.

2. **Horizon-uniform overlapping-noise completion.** A theorem with constants uniform in the observation horizon, or a sharp joint `n,M` law identifying unavoidable phase/controller overhead.

3. **A broad natural application.** Resolution of a finite-memory law for a recognized nonuniform nonlinear filter, controlled sensing model, partially observed diffusion/map, or adaptive experimental-design problem whose answer was previously open.

4. **A task-general duality.** A theorem identifying which continuation-value curvature and acquired-law dimensions determine memory rates across a broad family of losses, rather than only the full categorical Brier audit.

5. **Unknown-kernel or adaptive-calibration completion.** Matching acquisition–memory bounds when the observation law itself must be learned or calibrated causally.

6. **A genuine multi-resource region.** Matching upper and lower bounds involving several intrinsic resources beyond persistent-state cardinality and the constructed calibration/erasure coordinates.

7. **A converse to smoothing.** A broad result showing that failure of an appropriate actual-law smoothing/curvature condition forces an online/checkpoint separation or a different exponent.

Any one of these, if carried out at sufficient depth, could turn the present architecture into a result of exceptional general-mathematics significance.

---

## 14. Final evaluation

R11 is a serious and successful response to the R10 report. It closes the most important structural gap in the restart programme: overlapping noisy observations and observation-dependent sensing are now treated in one finite-state completion theorem. The proof contains a clear new idea. Conditional barycentric pooling keeps every retained label exactly calibrated to the hidden state under the finite observer's own law; Bellman optimality turns the cost of forgetting into an exact Jensen telescope; and integrated distributional curvature makes the resulting loss second order even at policy switches. The actual posterior density supplies a matching checkpoint lower, and the complete autonomous state count is honest.

The continuous sensor theorem verifies the hypotheses from raw kernels and proves genuine feedback value analytically. The stratified, digital, morphism and same-task resource results are logically compatible with the central theorem. I found no elementary fatal defect in the principal arguments checked. The source/provenance pipeline is unusually disciplined and accurately limits what its build evidence establishes.

The manuscript nevertheless remains below the exceptional threshold of the four leading general mathematics journals. Uniform acquired smoothing is a strong sufficient condition; the matched autonomous law is fixed-horizon; the rate theorem is tied to a finite hidden state and full categorical squared audit; the raw example is clean but designed; the full computational-resource problem remains open; and several close modern belief-aggregation and conditional-mean partition works still require direct comparison.

Accordingly:

**Top-four general-journal recommendation:** reject in the present form.  
**Reason:** insufficient intrinsic breadth, natural-problem impact and concentration of novelty for that exceptional level; not an identified fatal correctness defect.  
**Specialist-journal outlook:** strongly favorable after a focused major revision addressing the closest literature, exact status of smoothing, task dependence, horizon/state overhead, computational boundary and editorial architecture.
