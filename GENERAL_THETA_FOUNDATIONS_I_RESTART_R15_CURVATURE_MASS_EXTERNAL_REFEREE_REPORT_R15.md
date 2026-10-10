# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r15-curvature-mass-2026-10-08`  
**Reviewed exact branch head:** `b2bbef2354b52cd774bf6c242ac43039a05a1e7f`  
**Reviewed branch root tree:** `91b87befa7c4691dc6f1ba8d3138429b315ddbd5`  
**Ordinary mathematical-source commit:** `0f391dd67b2fc8d47685e91d86253898451e2730`  
**Native mathematical-source tree:** `1447a5858bbb75d35367299df5f9f24362e89904`  
**Complete PDF/artifact commit:** `142d68d6fbb00e5ce2de82848f54237940caf404`  
**R15 paper-directory tree:** `b04297f1354759a39c7386160156052c9a58b595`  
**Committed native PDF blob:** `e2d331bea31349619fd6ee7ecf274f0bb4f19182`  
**Predecessor completed revision:** R11 referee-ready head `e77c0aaedd5e3872b1e5348f5c78154ccc2ac479`  
**Predecessor external report:** review commit `801faac37eaf1c66e9d9554fa704ad0e1e8c6bfc`, report blob `d0d0cfc7d806f07275a5e7aca3a91d832447d28c`  
**Review branch:** `review/general-theta-restart-r15-curvature-mass-external-top4-referee-r15-2026-10-08`  
**Date:** 8 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof certificate, an independent priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This recommendation is **not a technical-correctness rejection**. Revision R15 is a major and mathematically substantive advance over R11. It directly answers the principal quantitative objection in the preceding report: the autonomous approximation constant no longer grows polynomially with the horizon on the newly declared block-stable class. The paper proves a joint horizon--state law

```text
R_cp(n,M)-B_n^*  asymp  M^(-2/d),
R_aut(n,M)-B_n^* asymp (M-n)^(-2/d),
```

with constants uniform in both `n` and `M`, and it proves rather than merely assumes that an internally timed exact-`n` observer must consume `n` nonterminal phase states when report supports are clock-neutral. The boundary-valid curvature estimate removes the compact-interior restriction of R11, the integer allocation follows the actual continuation-sensitivity profile, and the two principal raw realizations now include untruncated Gaussian observations and genuinely noncommuting finite-dimensional quantum instruments.

In the load-bearing arguments I checked, I did not find an elementary gap invalidating:

- the checkpoint variational identity over policies and terminal partitions;
- the all-incoming posterior calibration identity;
- the exact Bellman--Jensen telescope;
- the global convex extension and boundary-valid mass--curvature estimate;
- the continuation-sensitivity recursion and unequal integer allocation;
- the clock-support converse, under the intended phase-independent finite-machine model;
- the actual-law small-ball and strong-task-curvature converse;
- the Gaussian posterior-density calculation up to the simplex boundary;
- the positive-instrument coupling estimate;
- the inverse and Jacobian argument for the noncommuting quantum instrument;
- the finite-stratum upper and actual-submass lower;
- the finite-precision first-mismatch bound;
- the typed common-task simulator composition; or
- the attained same-task acquisition--memory--calibration--deficiency example.

The remaining negative top-four judgment is narrower than in the R11 report. It concerns the **intrinsic breadth and concentration of the advance**, not an identified fatal error. The central theorem is still a sufficient theorem for a strongly regularized class: finite affine predictive closure, a policy-uniform upper density for every one-step acquired law, a common finite action family, report-support equivalence across phases, summable block Wasserstein sensitivity, and a terminal task that is strongly concave in every acquired direction. The sharp `M-n` term is tied to a deliberately strict internally timed, clock-neutral resource interface. Under the more usual convention that a finite-horizon controller may consult an external stage index, the clock lower disappears. The Gaussian and quantum examples verify the theorem cleanly, but they remain calibrated known-kernel models rather than solutions of a widely recognized difficult natural problem whose finite-memory law had previously been open.

For a strong specialist journal in probability, information theory, stochastic control, statistical decision theory, nonlinear filtering, quantization, or mathematical aspects of quantum information, my assessment is **strongly favorable after a focused major revision**. At that level the new theorem and its proof form a coherent and publishable contribution. The paper should not, however, present the current result as if it were already an intrinsic classification of causal finite-memory completion.

---

## 1. Review object, provenance, and pipeline inspected

A fresh branch search immediately before depositing this report identified R15 as the latest completed branch matching `referee-ready/general-theta-restart-*`. R12, R13 and R14 are preserved research starts, not later completed referee-ready manuscripts. The exact object reviewed is the evidence-bound head

```text
b2bbef2354b52cd774bf6c242ac43039a05a1e7f.
```

The referee packet identifies the ordinary mathematical source commit

```text
0f391dd67b2fc8d47685e91d86253898451e2730
```

and native source tree

```text
1447a5858bbb75d35367299df5f9f24362e89904.
```

The terminal referee-ready head is an evidence-only child of the complete artifact commit. I reviewed the ordinary source and the final branch contents, not an unpinned working copy.

The inspection included:

- `main.tex`, all eight native section files and `references.tex`;
- `README.md`, `REFEREE_RESPONSE.md`, `REFEREE_COMMENT_CONCORDANCE.md`, `THEOREM_MAP.md`, `PIPELINE_DERIVATION.md`, `PROOF_LEDGER.md`, `PROOF_AUDIT.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, `NOTATION_AUDIT.md`, `RESEARCH_CONTRACT.md`, and `PINNED_INPUTS.md`;
- the canonical restart charter, foundational outline, theorem targets and realization-registry boundary;
- the complete R11 external report and the R15 point-by-point response;
- the theorem and provenance roles of integral Supplements U, T and S;
- `SOURCE_MANIFEST.json`, `verify.py`, `regression.py`, `build.py`, the build receipt, final verification record and referee packet; and
- a targeted independent search of nearby belief-space covering, finite-memory POMDP approximation, finite-window control, conditional-mean information design, recursive quantization, zero-delay finite-memory coding and experiment-comparison results, including work available through October 2026.

The delivery records report a nineteen-page native article, a seventeen-page complete Supplement U, a forty-nine-page complete Supplement T and a twenty-three-page complete Supplement S, for 108 rendered pages in total. The native audit records thirty-three listed source files plus the manifest, ten active TeX inputs, fifty-one labels, seventy-four cross-references, twelve bibliography entries and eighteen formal statements. The native regression suite records 8,837 finite checks; the retained suites are separately identified. Each of two environments performed fourteen isolated PDF builds. The normalized text and rendered pixels of all 108 pages agree across the recorded TeX environments, while the PDF bytes differ, which is an appropriately limited reproducibility claim.

The verification scripts are relevant to source binding, active inputs, labels, references, citations, finite posterior-pooling identities, finite clock graphs, integer allocation, matrix inversion, Gaussian formulas and selected resource calculations. They are not mathematical proofs, and the repository correctly says so. I treated them as evidence of what was executed, not as a substitute for reading the arguments.

I did not independently re-audit every theorem in the frozen v1--v96 archive, every old referee branch, or every separate realization paper. I also do not treat rebuilding Supplements U, T and S as a fresh theorem-by-theorem certification of those papers. The current R15 article re-proves the inherited load-bearing identity in the form needed for its new theorem, and that native proof is what I assessed here.

The preservation discipline is satisfactory. The canonical first-parent identity and the four controlling files remain fixed; the complete R11 article is retained as U; R10 and the earlier technical article remain T and S; incomplete R12--R14 records are not misrepresented as completed revisions; and no old review, realization or archive ref is rewritten.

---

## 2. Executive assessment of R15

R15 is the strongest manuscript in the restart sequence so far. Its conceptual center is now a theorem about the joint cost of resolution and internal timing, rather than a fixed-horizon approximation estimate with an uncontrolled horizon constant.

The pipeline may be summarized as

```text
prepared positive causal kernels
        -> executable future tests
        -> finite affine predictive carrier K
        -> actual post-report laws Lambda_t(s,a)
        -> calibrated finite observer under its own deployed law
        -> exact Bellman--Jensen information-loss identity
        -> mass x continuation-curvature upper
        -> sensitivity-weighted state allocation
        -> compulsory internal clock states
        -> matching checkpoint and autonomous risk curves.
```

The theorem separates four issues which were entangled in earlier versions.

First, all predictive representatives used by the finite machine are **actual conditional barycenters under the law generated by that machine**. There is no hidden exact filter or uncharged posterior register.

Second, the loss caused by each pooling cut is exactly a Jensen defect of the optimal continuation value. This remains true at action switches because differentiability of the Bellman value is not assumed.

Third, continuation sensitivity decays under the block Wasserstein condition. The observer therefore allocates one baseline state to each phase and spends its remaining states unequally, according to the future sensitivity of that phase. This removes the equal-allocation factor that caused the R11 autonomous constant to grow with the horizon.

Fourth, the paper proves a lower on the timing resource itself. If all report traces have equivalent supports and the machine receives no free phase variable or terminal request, a label appearing at two different cuts would induce the same reference trace law from both cuts and would force premature stopping from the earlier cut. Hence the positive-probability label supports of the `n+1` cuts are disjoint.

This is a real theorem and not a repackaging of R11. In particular, the `M-n` law is not obtained merely by constructing phase-labelled codebooks and declaring the phase overhead necessary. The converse is proved for every machine in the stated class.

The main limitation is equally clear. The result does not characterize finite-memory predictability in a model-independent manner. It identifies a powerful sufficient regime in which three strong ingredients coexist:

1. every post-report acquired law is uniformly full-dimensional and has bounded density;
2. future sensitivity is summable through uniform block products; and
3. time is hidden from the machine except through its counted labels.

The title “Foundations” therefore remains aspirational relative to the theorem's present intrinsic scope. The manuscript is a general theorem over a meaningful class, but not yet a universal foundation or a near-necessary classification.

---

## 3. Response to the R11 external report

R15 is not a cosmetic response. It answers several of the R11 report's most serious requests.

| R11 issue | R15 assessment |
|---|---|
| Autonomous constants deteriorated with the horizon | **Substantially resolved on the new block-stable class.** Sensitivity-weighted allocation gives constants uniform in `n` and `M`. |
| Equal resolution at every phase was wasteful | **Resolved.** Lemma `lem:allocation` allocates according to the continuation-sensitivity profile and retains one baseline state at every phase. |
| Phase-disjoint labels were only a safe construction | **Resolved under a precisely stated interface.** Lemma `lem:clock` proves disjoint positive-probability supports for an internally exact-`n`, clock-neutral machine. |
| The interior-support hypothesis excluded ordinary unbounded reports | **Resolved.** The global convex extension makes the curvature estimate valid at the carrier boundary, and the Gaussian posterior law may approach every simplex face. |
| The rate was tied too closely to quadratic categorical loss | **Improved.** The theorem separates the exact identity from strong task curvature and includes a nonquadratic class of strongly proper losses. |
| The closest aggregation and information-design literature needed theorem-level comparison | **Improved but still incomplete.** Grover--Dimitrakakis, Li--Hammar--Bertsekas and Lyu--Suen--Zhang are now discussed at the result level. Additional current belief-metric, finite-memory and zero-delay-coding comparisons remain necessary. |
| A more natural raw realization was needed | **Improved materially.** The Gaussian theorem uses ordinary unbounded Gaussian emissions, and the quantum theorem is genuinely noncommuting. Neither result is advertised as resolving a known open problem. |
| Exact-real state counting and finite-bit execution were conflated | **Resolved conceptually.** Cardinality, programme, workspace, numerical precision and runtime are separated, although computational synthesis remains conditional. |
| A full resource region was absent | **Only partially resolved.** The attained product task combines selected coordinates, but there is no matching optimal region for the full computational resource vector. |
| An intrinsic completion criterion was absent | **Still open.** The block-density theorem is a strong sufficient route, not a necessary or near-necessary characterization. |

The R11 report proposed horizon-uniform completion with a sharp joint horizon--memory law as one route that could materially alter the assessment. R15 pursues that route successfully. The negative top-four judgment therefore rests on a higher and narrower objection than before: whether the theorem's new combination has enough natural and intrinsic reach to meet the exceptional threshold of a leading general-mathematics journal.

---

## 4. Statement and conceptual status of the main theorem

Let `K` be a compact convex predictive carrier of affine dimension `d`. Executable future-test expectations are affine and separate points. For each phase and legal action, the actual post-report predictive law is

```text
Lambda_t(s,a) = Law(F_t(s,a,Y)),  Y ~ J_t(s,a).
```

The theorem assumes, uniformly over phases, states and actions:

- every report law is equivalent to one action-dependent reference probability measure which is common across phases;
- every `Lambda_t(s,a)` has density at most `rho` relative to `d`-dimensional Lebesgue measure on `K`;
- `Lambda_t` is Wasserstein-Lipschitz with coefficient `beta_t`;
- complete blocks of length `b` have coefficient product at most `theta<1`;
- report kernels are jointly Borel and total-variation continuous; and
- the terminal Bayes risk is Lipschitz and strongly concave in all acquired directions.

For the same exact-`n` terminal experiment, the theorem proves

```text
c M^(-2/d)
  <= R_cp(n,M)-B_n^*
  <= C M^(-2/d),
```

and, for the internally timed autonomous class,

```text
c (M-n)^(-2/d)
  <= R_aut(n,M)-B_n^*
  <= C (M-n)^(-2/d),
```

when `M>=n+1`; the autonomous class is empty for `M<=n`. The constants depend on the declared experiment class and task constants, but not on `n` or `M`.

Without block summability the paper retains the more informative upper

```text
R_aut(n,M)-B_n^*
 <= C A_n^((d+2)/d) (M-n)^(-2/d),
```

where `A_n` is the sum of fractional powers of continuation sensitivities. This is preferable to silently renaming a horizon-dependent constant “uniform.”

The theorem's conceptual status should remain explicit throughout the paper:

- it is a **sufficient causal realization theorem**;
- it is not a characterization of all finite-state observers;
- the density hypothesis is much stronger than positivity of the raw kernels;
- the `M-n` law is a theorem for one internally timed interface, not for externally clocked finite-horizon controllers;
- the exponent is a task-sensitive acquired-law exponent, not the formal dimension of every reachable carrier; and
- the exact pooling identity is more general than the quantitative `2/d` law.

The current manuscript states these boundaries in several places. They should be made even more prominent in the theorem's first informal presentation, because much of the paper's apparent breadth depends on not suppressing them.

---

## 5. Audit of the central proof

### 5.1 Checkpoint variational identity

For a deterministic acquisition policy, the terminal predictive state `S_n` determines every conditional terminal readout risk affinely. Replacing a history-dependent randomized label assignment by least conditional loss among the available readouts cannot increase risk. Optimizing each cell readout gives the conditional barycenter and hence the task distortion `D_M^g`.

Conditioning the independent policy seed then reduces the full checkpoint relaxation to deterministic policy/code pairs. The manuscript correctly warns that this seed argument is not a purification theorem for an autonomous machine whose random tape might otherwise function as hidden persistent state.

The identity

```text
R_cp(n,M)=inf_pi { B_n^pi + D_M^g(nu_n^pi) }
```

is therefore valid under the stated affine task and measurability assumptions. It also correctly keeps the two policy-dependent terms inside the same infimum.

### 5.2 All-incoming calibration

This is the load-bearing causal identity inherited from R11 and re-proved in the native article. At phase `t`, every current label carries its actual conditional predictive state. After the label's Bellman action and physical report, the pre-pooling state is `W_t`. For a cell `C`, the next programmed state is

```text
q_C = E[W_t | W_t in C]
```

under the actual finite mixture generated by all current labels and all incoming report edges.

For every affine executable future test `f`, disintegration gives

```text
E[f(X_t) | next label C] = f(q_C).
```

Separation by the declared test family proves that `q_C` is the actual predictive state conditional on the next label. This is not an edgewise representative, an approximation to an unavailable full-history filter, or a barycenter computed under a different policy.

The forward construction avoids circularity: at each phase the current finite mixture and programmed actions are already fixed before the next acquired law and its cell barycenters are computed.

### 5.3 Exact Bellman--Jensen telescope

At a calibrated state `Q_{t-1}`, the programmed action attains the Bellman minimum. Therefore

```text
E V_t(W_t)=E V_{t-1}(Q_{t-1}),
Q_t=E[W_t | retained label].
```

Subtracting the two sides after pooling and summing over phases gives

```text
R-B_n^* = sum_t J_{V_t}(lambda_t,P_t).
```

No pathwise comparison with a discarded exact posterior is used. The identity remains meaningful when `V_t` is nonsmooth at an action switch because only concavity and conditional expectation enter.

I found this argument coherent at the stated quantifiers.

### 5.4 Boundary-valid mass--curvature estimate

The new analytic lemma is a genuine improvement over the compact-collar argument in R11.

For a concave Lipschitz value `v` on compact convex `K`, the proof takes all supporting affine functions of `-v` at interior points. The Lipschitz bound controls every supporting slope. Their supremum is a globally convex Lipschitz extension agreeing with `-v` on the interior and hence, by continuity, on the boundary.

After subtracting a tangent plane at a grid center, the resulting smooth convex function `w` is nonnegative and vanishes at the center. The submean inequality, radial monotonicity, the inequality

```text
w(z+R omega) <= R partial_r w(z+R omega),
```

and the divergence theorem bound the local oscillation by

```text
C R^(2-d) integral_{B_R} Delta f.
```

Affine terms cancel at the conditional barycenter. Global mollification and weak convergence of the positive Laplacian measures give the nonsmooth statement with a slightly enlarged closed ball.

Finally, the acquired density bound supplies `lambda(C)<=rho h^d`, bounded overlap controls the sum of local curvature masses, and a compactly supported cutoff bounds the total Laplacian mass of a Lipschitz convex function on the relevant bounded region. This yields the `O(rho Lip(v) h^2)` grid loss without an interior support margin.

The proof is concise and uses standard convex-analysis ingredients, but I did not find an elementary defect. For publication, the authors should preserve the present explicit normalization of spherical averages, the `R^(2-d)` dimensional factor and the closed-ball passage in the mollification limit; these are not expository luxuries.

### 5.5 Continuation sensitivity

The common finite action set permits comparison of the same action at two incoming states. The Wasserstein inequality therefore yields

```text
Lip(V_t) <= beta_t Lip(V_{t+1}).
```

Taking the minimum over actions preserves the bound. Iteration gives the displayed future-product sensitivity `a_t`.

The argument does not compare two independently optimized shadow controllers on different report streams. It compares action-indexed continuation integrals and then takes a common finite minimum, which is the correct route.

### 5.6 Integer allocation

Writing `p=2/d` and `w_t=a_t^(1/(1+p))`, the allocation

```text
L_t = 1 + floor((m-1) w_t / sum_j w_j)
```

uses at most `n+m-1` phase labels. The leading `1` is essential: even a phase with tiny continuation sensitivity still needs one real state in the internally timed machine.

The displayed inequality follows directly from `L_t >= (m-1)w_t/A` for `m>=2`, with the `m=1` case handled separately. Under the block-product assumption, the future sensitivities decay geometrically by complete blocks; hence the fractional-power sum is bounded independently of the horizon.

This is a clean closure of the R11 equal-allocation loss. It should nevertheless be described as an optimized sufficient allocation, not as a general characterization of every optimal controller's internal state distribution.

### 5.7 Clock-support converse

This is the most conceptually delicate new lemma.

Suppose one positive-probability label `z` appears at two cuts `s<t`. From `z`, run the same observer against a reference report process which draws each report from the common action-dependent reference measure. Strict equivalence of the physical report law to that reference at every phase implies equivalence of every finite actual and reference trace law, even after mixing over the unobserved incoming physical state and the observer's fresh transition randomness.

Starting from `z` at cut `t`, the observer stops after `n-t` further calls almost surely. The corresponding trace event has reference probability one. Because the reference machine dynamics from label `z` are the same at the earlier cut, the same trace event has reference and hence actual probability one from cut `s`; the machine would stop before call `n`, a contradiction.

The logic is sound **provided the autonomous machine is formally phase-independent once its current label is fixed**. The prose model says that action, stop and next-label behavior depend on the current label and report alone, and excludes an uncharged instruction pointer. That intended meaning should be encoded in a formal definition by a single label-indexed action/stop kernel and a single label/report transition kernel, rather than left to prose. A family of externally time-indexed transition tables would invalidate the reference-trace identification while effectively reintroducing a free clock.

This is not merely a stylistic request. The sharp `M-n` law depends on the machine model at exactly this point.

The paper correctly records the complementary boundary: an exact time stamp in the report or a free external terminal request permits state reuse and destroys the lower. Thus the theorem should not be advertised as the universal finite-horizon memory law for POMDP controllers.

### 5.8 Actual-law lower

Condition immediately before the final action and report. The uniform density assumption holds for every incoming state and legal action, so mixtures over the full history, policy randomness and action selection preserve the upper density bound.

If `Z` is an `L`-valued terminal label and `Q=E[S|Z]`, affine conditional loss implies that the best label readout has risk `E g(Q)`. Strong concavity gives

```text
E g(Q)-E g(S) >= (alpha/2) E|S-Q|^2.
```

The union of `L` radius-`r` balls has probability at most `rho L v_d r^d`; choosing the radius so that this is one half gives the standard `L^(-2/d)` distortion lower. The argument covers randomized encoders because `Q` still has at most `L` possible values.

For checkpoint risk use `L=M`; for autonomous risk the clock lemma gives `L<=M-n`. The full-history terminal Bayes risk under any policy is at least `B_n^*`, so the policy optimization does not weaken the lower.

This is an actual-law argument, not a packing of the formal carrier.

### 5.9 Completion of the theorem

The checkpoint upper quantizes the actual terminal law of an attained Bellman-optimal full-history policy. The autonomous upper constructs the observer forward using the calibrated pooling lemma and the unequal phase allocations. Phase supports are disjoint in the construction, so the total is

```text
1 + sum_t L_t <= M.
```

The exact telescope plus the curvature estimate and allocation bound gives the upper. The clock and actual-law lemmas give the lower. No realization theorem is used to prove the general result.

Subject to the machine-model clarification above, I found the proof internally coherent.

---

## 6. Audit of the Gaussian realization

The hidden state has `d+1` values. A legal action first applies a known strictly positive stochastic matrix and then emits an ordinary Gaussian report in an ambient dimension `m_obs>=d`. Means are affinely independent, covariance matrices are positive definite, and the parameter family is restricted to a compact nondegenerate class.

For predicted hidden-state probabilities `q`, the posterior logits satisfy

```text
z = B_a y + c_a + log(q_j/q_0).
```

The matrix `B_a` has full row rank. The logit law is therefore a finite Gaussian mixture with a uniformly nonsingular `d`-dimensional covariance and uniformly controlled means, since strict positivity of the transition matrices keeps every `q_j` away from zero.

The softmax change of variables has Jacobian `product_j u_j`. Its reciprocal grows at most exponentially in `|z|`, whereas the Gaussian mixture density decays quadratically in the exponent. The posterior density

```text
h_q(logit(u)) / product_j u_j
```

is consequently bounded uniformly even though the posterior can approach every face of the simplex. No clipping, rejection, conditioning or compact posterior collar is introduced.

The Dobrushin row coefficient contracts the predicted state in `l^1`. Lemma `lem:instrument` transfers this to the acquired posterior law with a sufficient Wasserstein coefficient `3 kappa_t`, and supplies report total-variation continuity. The theorem permits individual certified coefficients above one so long as complete block products are uniformly below one.

Predictive separation is also checked rather than assumed. A Gaussian mixture with distinct affine exponents identifies its mixture weights; an available invertible transition matrix then recovers the incoming belief. The terminal categorical audit separates the coordinates.

I found the calculation valid under the stated compact parameter bounds. The result is substantially more natural than the specially affine observation family of R11. Its significance boundary is that it remains a finite hidden-state, known-kernel, uniformly positive and block-stable class equipped with a deliberately full-dimensional terminal audit. It does not establish a new finite-memory law for nonlinear, degenerate, unknown or nonparametric filtering.

The manuscript should make a standard-task corollary more visible. A reader from filtering or control should be told precisely what familiar prediction or decision problem receives the `M-n` law, beyond the flexible class of injected proper audits used to certify all directions.

---

## 7. Audit of the noncommuting quantum realization

The physical carrier is the finite-dimensional density-matrix body, of affine dimension `D^2-1`. The channel

```text
C_t^a(rho)=(1-alpha_t^a) tau_t^a + alpha_t^a U_a rho U_a^*
```

keeps the state uniformly positive. The report effect

```text
E_y=I+s sum_i y_i H_i
```

is positive throughout the cube and spans every traceless Hermitian direction. The matrices need not commute.

For fixed positive `q`, the normalized congruence map is

```text
E -> E^(1/2) q E^(1/2) / tr(Eq).
```

Given a positive output `sigma`, the manuscript defines the unique positive solution `A` of `AqA=sigma` and recovers

```text
E = D A^2 / tr(A^2).
```

This is a two-sided smooth inverse between the relevant trace hyperplanes. Restricting to the affine report cube yields an injective full-rank map. Uniform positivity and compactness give a positive lower Jacobian bound, so the actual acquired state has uniformly bounded density.

The channel contracts trace distance by `alpha_t^a`, and the positive-instrument coupling gives the required Wasserstein and report-TV estimates. The report density identifies the post-channel state; injectivity of the channel identifies the incoming state. A finite informationally complete audit supplies an injective affine task map.

The proof is finite-dimensional and does not diagonalize the effects. I found no elementary error in the inverse or density argument.

The top-four significance should not rest heavily on the word “noncommuting.” The instrument family is deliberately constructed so that the normalized congruence map is globally invertible and uniformly nondegenerate. The theorem is an effective independent verification of the general mechanism, but it is not a broad theorem about arbitrary quantum filtering, quantum control, unbounded operators or experimentally constrained measurement design. The article generally observes this boundary and should continue to do so.

---

## 8. Singular strata and changing rank

The finite-stratum theorem correctly separates the exact causal identity from the full-dimensional density assumption. Each report-readable type has a compact convex affine carrier; positive-dimensional component laws carry their own unnormalized densities; singleton strata cost labels but have no quantization exponent.

For the upper, type-cell barycenters preserve the all-incoming calibration identity. Fixed fractions of a large allocation are assigned to the finitely many positive-dimensional types, while finitely many small allocations are absorbed by a uniform coarse bound. The largest stratum dimension controls the exponent.

For the lower, one terminal `r`-dimensional subprobability component has actual mass at least `w` and subdensity at most `rho_*`. The union-of-balls argument is applied without renormalizing that component, yielding the correct factor

```text
alpha w^(1+2/r) rho_*^(-2/r).
```

The validation/noise quantum example genuinely moves between rank-one atoms and a full-dimensional continuously acquired law: a later positive preparation channel can return an atom to the interior. The terminal continuous mass factor `1-vartheta` is retained rather than conditioned away.

This is a meaningful singular extension. It remains finite-type, report-readable and uniformly nondegenerate on each positive-dimensional carrier. Countably accumulating, degenerating or unobservably overlapping strata remain outside the theorem, as the scope audit states.

---

## 9. Numerical execution, causal morphisms and the attained product task

### 9.1 Exact-real versus finite-bit observers

The cardinality theorem permits programmed exact barycenters and Bellman actions. The manuscript does not equate this with efficient synthesis.

The numerical proposition separately charges:

- Bellman action slack;
- coordinate evaluation error;
- exceptional evaluation events;
- grid-boundary mismatch probability;
- complete physical/scored-law coupling error;
- terminal output error through a task modulus;
- programme bits, report precision, workspace and runtime.

The first-mismatch proof uses the unconditional ideal acquired density to bound the mass of slabs around grid hyperplanes. It does not condition on survival of all earlier numerical comparisons, which would generally bias the acquired law. This is the correct argument.

The result remains conditional on certified integration, barycenter and kernel routines. It is not a general computational-complexity theorem for POMDP planning or quantum filtering.

### 9.2 Typed common-task composition

The simulator proposition uses a parameter-independent strategy lift, report transformation, legal action interface, internal state, physical clock and common scored readout. Complete scored-law total variation, not marginal report distance, controls bounded loss. Predictor and simulator labels multiply in the direct implementation; complete-law errors add under composition.

The proposition correctly states that a reverse risk lower requires a reverse certificate covering every source policy in the comparison class. An upper simulator alone gives no converse.

This is a clear resource-aware restatement of a classical experiment-comparison mechanism, not a new total-variation inequality.

### 9.3 Same-task four-coordinate example

The product preparation combines:

- an early erased bit with an irreversible write-only deadline;
- the geometric engine;
- an inaccessible calibration offset; and
- the terminal audit.

The bit's unavoidable squared error is proportional to `epsilon`, the offset contributes exactly `delta^2`, and the engine contributes its acquired-law quantization term. The source-to-exact-bit deficiency is exactly `epsilon`, proved by the contraction/triangle lower and attained by a fair guess on erasure.

The three components are scored under one product law, so their lower terms legitimately add. The early write-only output is essential: a terminal-recall bit would require a different persistent-state account. The manuscript states this boundary explicitly.

This corollary demonstrates simultaneous attainability of selected resource coordinates. It does not yet give a matched optimal region for programme length, workspace, physical time, numerical precision, reset count and minimal simulator state.

---

## 10. Assessment against the controlling targets F1--F4

### F1 — Causal acquired-geometry transfer

**Substantially achieved as a strong sufficient theorem.**

The theorem begins with prepared experimental kernels and executable tests, constructs a legal finite observer under its own actual law, and proves matching checkpoint and autonomous curves from acquired density, continuation sensitivity and an explicit timing interface.

The qualification is important: finite affine closure, full-dimensional one-step density, block summability and clock neutrality remain substantial hypotheses. R15 is not a necessary-and-sufficient theory of recursive realizability.

### F2 — Resource--resolution--risk composition

**Substantially advanced but not fully achieved as an optimal region.**

Persistent labels, compulsory timing states, acquisition count, calibration ambiguity and an attained deficiency are combined in one scored product experiment. Numerical and simulator resources receive explicit feasible accounts.

There is still no single theorem matching upper and lower bounds for the full vector of programme length, planning complexity, workspace, arithmetic precision, simulator state, reset cost and physical time.

### F3 — Singular extension

**Achieved for a meaningful finite-stratum class.**

The theorem permits atoms, full-dimensional laws and repeated changes of rank, and its converse retains the actual mass of the terminal high-dimensional component.

General countable, degenerating and non-readable stratifications remain open.

### F4 — Distinct raw-kernel realizations

**Achieved.**

The Gaussian hidden-state model and the noncommuting quantum instrument are genuinely different raw experiments. Neither is used as a premise of the general theorem.

---

## 11. Novelty and literature positioning

The manuscript now treats several close antecedents responsibly. In particular, it does not claim novelty for Bellman recursion, conditional means, depth-dependent discretization, Wasserstein filter stability, static curvature-sensitive information design, convex supporting planes, small-ball quantization or classical comparison of experiments.

The proposed new combination is more specific:

- all-incoming conditional calibration under the deployed machine's law;
- an exact sequential Bellman--Jensen loss identity;
- a boundary-valid actual-mass/distributional-curvature estimate;
- continuation-sensitivity-weighted integer state allocation;
- a converse forcing internal clock states from report-trace equivalence; and
- two independent raw-kernel verifications.

I found no evidence in the inspected materials that this exact theorem is a restatement of one cited result. The combination is mathematically nontrivial.

The literature map is nevertheless still too narrow for a paper with the present title and scope. At minimum, the next revision should compare assumptions and conclusions with the following nearby routes.

1. **Belief-space metric covering and stability.** Zhu and Lu, *A Covering Framework for Offline POMDPs Learning Using Belief Space Metric* (AISTATS/PMLR 2026), explicitly couples belief-space metric coverage, policy stability, horizon and memory effects. Its object is offline evaluation and sample coverage rather than hard causal state cardinality, but the comparison is now unavoidable.

2. **Finite-memory belief approximation in Wasserstein distance.** Mintae Kim, *Finite Memory Belief Approximation for Optimal Control in Partially Observable Markov Decision Processes* (arXiv:2601.03132, 2026), develops policy-conditional finite-memory performance bounds along closed-loop trajectories. It does not appear to give the R15 acquired-law lower or compulsory clock count, which is exactly why a direct comparison would sharpen the novelty claim.

3. **Refined finite-window POMDP bounds.** The 2024 work of Demirci, Kara and Yüksel on expected Wasserstein and pathwise total-variation stability should be distinguished from the current block-sensitivity allocation, rather than represented only through the earlier JMLR theorem and average-cost paper.

4. **Finite belief-model quantization.** Saldi, Yüksel and Linder's finite-model approximation results for discounted POMDPs provide a nearby global belief-quantization route under weak continuity. The current theorem has a different task, exact timing interface and actual-law lower, but those distinctions should be stated.

5. **Zero-delay finite-memory coding.** Ghomi, Linder and Yüksel's 2022 theorem on stationary zero-delay coding and near-optimal finite-memory codes for linear vector Markov sources, together with Wood, Linder and Yüksel's finite-source results, is directly relevant to any broad claim about finite causal state, quantization and horizon effects. Coding state is not the same object as a predictive quotient label, but this difference requires explanation, not omission.

6. **Nonanticipative rate-distortion and causal coding.** Information-rate constraints do not equal a pointwise persistent-alphabet bound, yet the causal reconstruction and directed-information literature is close enough that the relation should be mapped explicitly.

7. **Finite automata and controller state complexity.** The clock-support lemma is mathematically elementary once the resource interface is fixed, but its conceptual role should be compared with standard conventions for time-dependent finite-horizon controllers and with automata whose control location is counted as state. The paper should explain which convention is new, which is standard, and which conclusion changes under an external stage index.

An exhaustive independent priority determination is beyond a referee report. The targeted search above is sufficient, however, to show that the formal bibliography of twelve entries is not yet adequate for a “Foundations” paper spanning filtering, finite-memory control, causal coding and quantum instruments.

---

## 12. Major issues before specialist-journal publication

### 12.1 Formalize the autonomous machine as a phase-independent kernel

The clock converse requires that from a reused label the machine has the same action, stop rule and report-to-next-label transition law, independent of absolute phase. The prose excludes a free instruction pointer, but the formal definition should introduce one stationary label-indexed machine tuple and state explicitly that no time-indexed family of transition tables is admissible unless the phase is included in the counted label.

This clarification should appear in the theorem statement or a formal definition immediately before it. It is the most important technical revision requested in this report.

### 12.2 Separate the clock theorem from conventional finite-horizon memory accounting

Many control papers allow the stage index as an externally known variable and count only the controller's information state. Under that convention the `n` term vanishes. The manuscript knows this, but the title and abstract make the joint law easy to overgeneralize.

The revision should present, side by side:

- the internally timed law proved here;
- the externally clocked counterpart, where phase labels may be reused; and
- the exact conversion between the two accounting conventions.

This would turn a possible model-choice objection into a useful theorem about resource interfaces.

### 12.3 Foreground the strength of the acquired-density hypothesis

Condition (ii) is imposed for every incoming carrier state and every legal action, including compressed mixture states never generated by one preferred full-history policy. This is far stronger than positivity or ordinary observation noise.

The introduction should say this before displaying the universal-looking rates. It should also distinguish:

- density with respect to a fixed affine chart;
- lower-dimensional or atomic acquired laws;
- selected-policy density bounds; and
- the uniform all-state/all-action condition actually used.

### 12.4 Clarify what the block condition contributes beyond the conclusion

Horizon uniformity is obtained by assuming summability of continuation sensitivity through uniform block products. This is a meaningful mechanism, but it is not an intrinsic conclusion from acquired density alone.

The paper should state whether there are natural examples where the true optimal continuation sensitivity is summable even though the displayed sufficient `beta_t` products are not, and whether the mass--curvature expression suggests a weaker theorem. At present the weighted upper is proved, but the gap between that bound and an intrinsic criterion remains large.

### 12.5 Give a standard decision problem with the full lower exponent

The nonquadratic proper-audit class is mathematically legitimate, but it is flexible enough to inject strong curvature in every predictive direction. A reader may reasonably ask whether the lower is driven by a specially chosen audit rather than by the natural loss of the sensing problem.

For each principal realization, state at least one conventional prediction, filtering, discrimination or control task for which the strong-concavity and full-rank audit hypotheses hold and interpret the resulting rate operationally.

### 12.6 Expand the theorem-level literature comparison

The current comparison is improved but incomplete. The belief-metric, finite-memory approximation, refined finite-window, finite-model quantization, zero-delay coding and nonanticipative rate-distortion lines listed above should be compared by:

- object being approximated;
- controller/predictor information pattern;
- whether time is free or charged;
- memory metric;
- task and horizon criterion;
- upper versus matching lower;
- known versus learned kernels; and
- actual-law versus reachable-set geometry.

### 12.7 Moderate the role of the quantum realization

The noncommuting example is valid and useful. Its contribution is to show that the affine predictive theorem is not merely a commutative-simplex statement. It should not be used to imply a broad quantum-memory or quantum-control completion theorem. The finite dimension, uniformly positive preparation channel, specially spanning effects and informationally complete paid audit should remain visible wherever the example is summarized.

### 12.8 Keep exact-real and computational claims sharply separated

The finite-bit proposition is conditional on certified Bellman, barycenter, kernel and coordinate routines. The abstract phrase “numerical execution is certified” could be read more broadly than the theorem proves.

State explicitly that the paper gives an error-composition theorem **given** numerical certificates; it does not prove polynomial-time synthesis, computability for every Borel model, or a matched bit-complexity law.

### 12.9 Reconsider the submission architecture

The delivery is admirably complete, but a nineteen-page main article accompanied by three integral supplements totaling another eighty-nine pages creates an editorial object of 108 pages, with several generations of overlapping foundations claims.

For journal submission, provide a one-page dependency and novelty statement identifying:

- exactly which R15 results are new;
- which results are re-proved because they are load-bearing;
- which complete supplements are archival rather than required reading; and
- which claims can be evaluated without reading the older articles.

The current theorem map is a good start, but the editorial hierarchy should be unmistakable from the submission cover letter and table of contents.

### 12.10 Reassess the title against the theorem's intrinsic reach

The title may be retained, but “Foundations” places an unusually high burden on the theorem. The abstract and first page should state in direct language that the present result is a sharp theorem for a finite affine, uniformly smoothing, block-stable class with an internally charged clock. It is not yet the final foundations-level classification announced by the broader programme.

---

## 13. Detailed mathematical and expository comments

1. In the autonomous-machine definition, write the action kernel, stop indicator and next-label kernel explicitly and declare them independent of absolute time unless time is part of the label.

2. State whether fresh randomization is sampled anew at every transition and erased, and whether any pseudorandom-generator state must be counted as persistent.

3. In Definition `def:hypotheses`, clarify that equivalence means mutual absolute continuity, not a uniform lower likelihood-ratio bound. The clock proof uses null-event equivalence, not quantitative comparison.

4. Make explicit that the reference trace process in Lemma `lem:clock` uses the same label-transition randomization law as the actual machine and therefore has the same law from a reused label at different cuts.

5. In the clock proof, state separately why mixing over different incoming physical states preserves equivalence to the reference trace.

6. The nonemptiness construction for `M=n+1` should specify a legal action at each chain label and one terminal readout, while noting that its risk need not be small.

7. In Theorem `thm:main`, list norm-equivalence dependence among the constants, because density and strong concavity are stated in Euclidean coordinates while Wasserstein stability may use another norm.

8. Repeat near the main theorem that `B_n^*` may change with `n`; the result is not automatically a monotone learning curve for one fixed latent quantity.

9. In the checkpoint identity, retain the explanation that policy-dependent baseline and distortion are minimized jointly.

10. In the curvature lemma, preserve the distinction between the grid center, which may lie outside `K`, and the programmed conditional barycenter, which lies in `K` and is the only predictive state used by the observer.

11. In the nonsmooth limit, identify the precise bounded region on which mollified curvature measures are tested and why the enlarged closed balls suffice for the Portmanteau step.

12. The cutoff estimate for total Laplacian mass should retain the sign convention and compact support of the cutoff; the current displayed integration-by-parts formula is helpful.

13. In Lemma `lem:allocation`, the `m=1` case deserves its own line in the statement because it corresponds to the sharp minimum `M=n+1`.

14. When bounding block sensitivities, display the constant multiplying `theta^{floor((n-t)/b)}` and explain the last incomplete block controlled by `B`.

15. In Lemma `lem:lower`, use one symbol consistently for Euclidean norm and for the norm in the Wasserstein condition; absorb equivalence constants only after stating them.

16. For randomized encoders, explicitly note that the conditional barycenter `Q=E[S|Z]` still has at most `L` values even if the transition into `Z` is randomized.

17. In the Gaussian theorem statement, promote the compact nondegeneracy conditions on means and covariances from surrounding prose into the formal hypotheses.

18. In the Gaussian density proof, state the uniform lower and upper bounds on each predicted coordinate `q_j` that follow from the transition floor.

19. The Gaussian mixture-identifiability argument should cite a standard source or retain the present one-line exponential-linear-independence proof.

20. The example with coefficients `0.8,0.8,0.02` is useful. State clearly that these are row-contraction coefficients before multiplication by the factor three.

21. In the quantum theorem, specify the affine volume form used for the density-matrix carrier and the report cube.

22. In the quantum inverse, state that `A` is positive definite and hence the positive square root of `A^2` is exactly `A`; this makes the substitution into `E^(1/2)` immediate.

23. The uniform Jacobian lower follows from invertibility of the differential on a compact set. State explicitly that the report-cube boundary is null and no multiplicity factor occurs.

24. In the stratified theorem, distinguish a report-readable type from a type inferred from an unretained incoming state. The current formulation intends the former.

25. The low-allocation stratum argument absorbs finitely many budgets into a constant. State the threshold and its dependence on the number of types in the proof ledger.

26. In Proposition `prop:digital`, explain how certified coordinate error is measured when the carrier is a simplex or a trace-one matrix chart and how grid hyperplanes are counted in that chart.

27. The slab probability term `rho b_t/h_t` should be capped at one before being multiplied by `H`, as the theorem already permits for the full bracket.

28. For the Brier readout example, distinguish Euclidean output error from predictive-coordinate error used to select cells.

29. In the morphism proposition, keep the complete stopped/scored-law quantifier visible; marginal report total variation is insufficient for adaptive policies and common tasks.

30. The same-task product theorem uses one early-interface label and `M-1` engine labels. Retain the explicit explanation of why the early bit output is write-only and cannot serve as a free persistent register.

31. The calibration offset is deliberately unobservable rather than an unknown kernel to be learned. This distinction should remain in every summary table.

32. The final audit is physically charged but inaccessible to the predictor before scoring. Repeat this convention in the theorem statement of the product task.

33. The bibliography should include final publication data when available and pin preprint versions when a version-specific theorem is discussed.

34. Add the current 2026 belief-metric and finite-memory references before claiming that the literature map is up to date.

35. The source audit counts twelve bibliography entries. That number is too small for the breadth of the claimed interface unless the literature section is explicitly presented as selective and supplemented substantially.

36. Preserve the verification statement that cross-environment PDF bytes differ while normalized text and rendered pixels agree; do not replace it by “byte-identical builds.”

37. Preserve the exact limitation that the 108-page rebuild is not a fresh mathematical audit of every historical theorem.

38. The theorem map should mark which arrows use inherited ideas and which formal proofs are completely native, even though the native article currently re-proves every load-bearing step it uses.

39. The abstract says “the decision loss need not be quadratic.” Add “but the matching full-dimensional lower requires strong concavity of its Bayes risk.”

40. The abstract says “the optimal excess risk” without immediately qualifying the machine interface. Add “for the internally exact-`n`, clock-neutral autonomous model defined below.”

---

## 14. What would materially change the top-four assessment

R15 has already completed one of the strongest routes requested in the R11 report. Further polishing, more build receipts or another similarly calibrated realization would not by itself change the recommendation. A top-four case would now require an advance of a different order, for example one of the following.

### 14.1 An intrinsic completion criterion

A necessary-and-sufficient, near-necessary or dual characterization of when checkpoint acquired geometry can be causally realized with the same memory order, unifying:

- overlapping-noise posterior pooling;
- separated refinements;
- continuation cuts;
- clock resources;
- singular strata; and
- failure of summable continuation sensitivity.

### 14.2 A natural hard application

A theorem resolving a recognized finite-memory problem for a nonuniformly stable nonlinear filter, regime-switching partially observed system, singular sensing model, physically constrained quantum instrument, or related natural class where the memory--risk law was previously unknown.

The task should be standard for that field, rather than introduced primarily to make every predictive direction strongly curved.

### 14.3 A converse beyond the exact-clock interface

A broad lower identifying which part of online memory is intrinsically required for prediction and control, rather than required only to encode an internal deadline. Such a result could explain when the `n` timing overhead is present, absent or replaced by a smaller causal synchronization complexity.

### 14.4 Adaptive acquisition with unknown kernels

Matching acquisition--memory--risk bounds when actions must learn or calibrate the raw kernel while sensing, rather than operating under a fully known model with precomputed Bellman actions and barycenters.

### 14.5 A genuine multi-resource optimal region

One theorem with matching upper and lower bounds for several intrinsic coordinates among persistent labels, programme description, workspace, numerical precision, raw calls, reset cost, simulator state and physical time.

Any one of these could concentrate the current architecture into a result of exceptional general-mathematics significance.

---

## 15. Final evaluation

Revision R15 is a serious and successful mathematical response to the R11 report. It proves a sharp joint horizon--state law on a nontrivial class, removes the posterior-collar restriction, optimizes phase resolution by continuation sensitivity, and supplies a genuine converse for the internal timing resource. The Gaussian and noncommuting quantum realizations verify the theorem from two different raw-kernel structures. The singular and resource layers are carefully separated from the center, and the source/provenance pipeline is unusually disciplined.

I found no elementary fatal error in the principal arguments checked. The clock lemma requires a formal phase-independent-machine definition, but the intended model is clear and the proof is coherent under that interpretation.

The manuscript nevertheless remains below the exceptional threshold of the four leading general mathematics journals. The main theorem is still a highly conditioned sufficient principle. Its sharp `M-n` form is inseparable from a restrictive but defensible timing convention. Its lower exponent requires a strongly curved task in every acquired direction. Its natural examples are mathematically clean but do not yet resolve a broadly recognized hard problem. The full foundations programme remains open at the intrinsic-classification, unknown-kernel and multi-resource levels.

Accordingly:

**Top-four general-journal recommendation:** reject in the present form.  
**Reason:** insufficient intrinsic breadth, natural-problem impact and concentration of novelty for that exceptional level; not an identified fatal correctness defect.  
**Specialist-journal outlook:** strongly favorable after a focused major revision addressing the autonomous-machine formalization, clock-interface positioning, task naturality, literature map, computational boundary and submission architecture.
