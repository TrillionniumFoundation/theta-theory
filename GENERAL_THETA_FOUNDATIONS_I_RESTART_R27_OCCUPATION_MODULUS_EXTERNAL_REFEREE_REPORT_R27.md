# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r27-occupation-modulus-2026-10-10`  
**Reviewed exact branch head:** `c5f05d1944251a95619d5cdad814c5c83646429c`  
**Reviewed branch root tree:** `62ad4c13b1da26fe7951c90452fc523d7f1c53da`  
**Ordinary mathematical-source commit:** `4a9f9a36f6ad02561f8e8eae112674f3f3c5d777`  
**Native ordinary-source tree:** `36c91366f880989e6e2836d7e7bf55e6666d4953`  
**Hosted artifact commit:** `6ca75d078bc710cdbdf2feedf5744409947aaa37`  
**Native PDF SHA-256:** `5ae294d145b6e245a8d12b0c94015359fdbff7269407da23c5516a49730438fe`  
**Native article length:** 31 pages  
**Complete deposited packet:** twelve PDFs, 332 pages  
**Predecessor external report:** R25 review head `623837ecd254175c0e0cc055d3f0ccf758f57516`, report blob `7b5b8fa3af91c2545563c41e8bce8fb5b95b7657`  
**Unreviewed intervening research:** completed R26 artifact head `193059765dd245472032f85b8924f49eee10d85d`  
**Review branch:** `review/general-theta-restart-r27-occupation-modulus-external-top4-referee-r27-2026-10-10`  
**Date:** 10 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof certificate, an independent priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not a technical-correctness rejection**. Revision R27 is a genuine and substantial advance over the reviewed R25 manuscript and over the unreviewed R26 research article from which it inherits its qualitative task-visible theory. The new paper no longer treats a uniform group-inverse or a fixed recurrence sublevel as the only temporal regularity mechanism. Instead it introduces a task-dependent residual--oscillation approximation functional for the marked Poisson equation, proves a two-sided comparison with the largest normalized physical-prefix discrepancy, obtains an exact signed linear-programming dual, and transfers the resulting temporal modulus to actual acquired occupation at the target geometric resolution.

The strongest new theorem is mathematically coherent. For the actual retained-boundary matrix `P`, the joint duration--exit matrix `T`, the complete-excursion reward vector `r`, and the classwise physical-time gain `g`, the manuscript uses the correct marked residual

```text
b = r - T g,
```

rather than replacing `T` by a product of a mean-duration diagonal and `P`. It defines

```text
k_N = inf_u { ||b-(I-P)u||_infinity + osc(u)/N }
```

and proves that its family supremum is equivalent, up to the actual physical-return remainder, to the largest prefix discrepancy

```text
max_{1<=t<=N} ||t(J_t-g)||_infinity / N.
```

The reverse inequality is not a formal duality argument. It is obtained by averaging the actual first-excursion renewal equations for the physical prefixes and constructing an approximate corrector from those discrepancies. The proof retains the dependence between duration and exit label and retains the terminal strip of the first excursion. Periodic cancellation explains why a terminal-time discrepancy alone is insufficient, and a front-loaded deterministic excursion explains why a boundary-only calculation cannot delete the physical remainder.

The exact dual is also useful and correctly typed. A feasible signed vector measures approximate boundary balance; it is neither an occupation probability nor information supplied to the observer. The manuscript explicitly warns that the resulting lower certificate concerns the displayed supremum over entering rows and does not automatically give a lower bound from one prescribed initial law. The actual-occupation and all-history decision lower bounds are proved separately where such accessibility is available.

The finite-resolution theorem is another real contribution. By testing occupation with a truncated squared distance whose Lipschitz constant is proportional to the target radius `r`, the manuscript transfers a genuine small-ball submeasure from the limiting occupation to the `N`-call occupation with an error of order `r zeta_N`, rather than losing an error independent of the geometric scale. The true submeasure mass is retained. The matching upper remains correctly separated: it requires a common executable predictive initialization, globally valid candidate covers, report continuity, an actual-law update-stability estimate, and a counted controller--predictor product state.

The raw controlled-load theorem also improves the paper materially. Its lower bound is proved from predictable starts early enough to guarantee the first scored service call. It does not subtract an unweighted “last mark,” which would be invalid when the unfinished event depends on the mark. This yields an actual finite-acquisition submeasure for every adaptive controller under a uniform conditional service-mean bound. Queue drift and a dual trace-survival inequality give two independent primitive verifications. The arbitrary revelation-profile theorem then shows that the temporal modulus is attained against all history-dependent strategies, including nonalgebraic logarithmic acquisition rates.

In the load-bearing arguments checked, I did not find an elementary gap invalidating:

- the finite-product weak-star continuity argument for one reused Borel report row;
- continuity of the marked excursion arrays under the stated response and return hypotheses;
- the classwise physical-time gain and the marked residual `r-Tg`;
- the physical-prefix upper bound from an approximate marked corrector;
- the first-excursion renewal converse and the construction of the averaged corrector;
- the two-sided comparison between `K_N` and the maximal normalized prefix discrepancy;
- attainment of the finite-dimensional residual--oscillation infimum;
- the signed boundary-balance linear-programming dual;
- the necessity of both the prefix qualifier and the physical-return remainder;
- the factor-two comparison with the uniform approximate-corrector price;
- the qualitative task-visible equivalence retained from R26;
- robust attainment and finite-model determination when the task criterion holds on the whole declared program class;
- the finite semialgebraic decidability and polynomial-growth conclusions at the level at which they are stated;
- the actual class-weighted occupation formula and checkpoint quantization identity;
- the resolution-localized small-ball transfer using clipped squared distance;
- the counted `QJ` causal upper and the explicitly quantified optimized matching corollary;
- the exact diagnostic and arbitrary revelation-profile minimax formulas;
- the controlled-queue and noncommuting rank-changing quantum temporal realizations;
- the predictable-start controlled-load occupation lower;
- the two raw geometric realizations based on queue drift and unnormalized quantum survival;
- the task-compatible simulator comparison requiring bridges at both endpoints;
- the same-task memory--calibration--deficiency sandwiches and profile laws; or
- the source, artifact, and independent-rebuild claims at the level at which they are stated.

I did find one concrete indexing error in an inherited physical-crossing proof. In Lemma `lem:physical`, the manuscript defines

```text
S_k = sum_{j<k} tau_j,
K_N = min{k>=1 : S_k >= N}.
```

Under this convention one has `K_N <= N+1`, not `K_N <= N`; for unit-length excursions, `K_N=N+1`. The number of summands with `k<K_N` is nevertheless at most `N`, which is what the stopped-sum argument needs. This appears to be a repairable off-by-one statement rather than a defect in the resulting inequality. The notation for crossing indices in the controlled-load proof should be standardized at the same time.

The negative top-four judgment concerns the **intrinsic reach, concentration, novelty relative to mature semi-Markov/Poisson approximation theory, and external mathematical impact of the advance**, not an identified fatal proof defect.

The temporal center is an exact theorem for a finite retained boundary and marked regenerative physical excursions with a uniform all-row first moment; its limiting equivalence additionally needs uniform integrability. This is broader and more task-sensitive than R25's bounded-group-inverse sublevels, but it is still not a theorem for arbitrary nonregenerative histories, general nondominated partially observed control, data-dependent unbounded stopping, or an infinite retained boundary. The physical renewal interface is mathematically meaningful and includes unbounded physical states, yet it remains a substantial structural restriction.

Moreover, approximation functionals for ergodic convergence, Poisson equations and their martingale representations, linear-programming duality, multichain Markov-renewal evaluation, quantization lower bounds, and finite-memory binary learning all have substantial classical theories. R27 is careful not to claim those tools individually. The proposed novelty is their marked physical-time converse, exact finite dual, and finite-resolution causal use. That synthesis is useful, but the paper has not yet shown that it changes the understanding of a recognized difficult natural problem to the degree expected at a leading general mathematics journal.

The optimized spatial theorem is conditional on unusually strong quantified inputs: every competing observer must generate its own common small-ball witness and baseline lower, while one fixed-size exploration must attain the benchmark and admit a common predictive initialization, global candidate-valid covers, and actual occupation stability. Those assumptions are verified in the fresh-load protocol, but the protocol is designed to make the mark exactly observable before delayed scoring. The theorem therefore does not yet produce a broad optimal acquisition/control curve for POMDPs, queue filtering, or quantum control.

The effective and semialgebraic layers are logically careful, but they remain decision and exhaustive-certification results. Their primitive descriptions, termination certificates, model nets, algebraic integrations, and support conditions carry much of the computational burden. They do not give a practically meaningful synthesis complexity theorem or a matched computational-resource region.

For a strong specialist journal in stochastic control, probability, information theory, semi-Markov processes, finite-memory learning, quantization, controller synthesis, queueing, or mathematical quantum information, my assessment is **favorable after a focused major revision**.

---

## 1. Review object, provenance, and pipeline inspected

A fresh two-page branch enumeration immediately before creating this report identified

```text
referee-ready/general-theta-restart-r27-occupation-modulus-2026-10-10
```

as the latest completed `General Theta Foundations I` referee-ready revision. The continuation page was empty, and no later R28 referee-ready branch was present in that enumeration. The exact object reviewed is the terminal evidence-bound head

```text
c5f05d1944251a95619d5cdad814c5c83646429c.
```

That commit is evidence-only and has artifact commit

```text
6ca75d078bc710cdbdf2feedf5744409947aaa37
```

as its sole parent. The packet identifies the ordinary mathematical source

```text
4a9f9a36f6ad02561f8e8eae112674f3f3c5d777
```

and the native source tree

```text
36c91366f880989e6e2836d7e7bf55e6666d4953.
```

I reviewed the native article and its source-and-derivation pipeline rather than treating the 332-page delivery packet as one undifferentiated manuscript. The inspection included:

- `main.tex`, all twelve native section files, and `references.tex`;
- `README.md`, `SUBMISSION_GUIDE.md`, `REFEREE_RESPONSE.md`, `REFEREE_COMMENT_CONCORDANCE.md`, `THEOREM_MAP.md`, `PIPELINE_DERIVATION.md`, `PROOF_LEDGER.md`, `PROOF_AUDIT.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, `NOTATION_AUDIT.md`, and `PINNED_INPUTS.md`;
- the canonical restart charter, foundational outline, theorem targets, and realization-registry boundary;
- the complete R25 external report and the R26/R27 point-by-point response chain;
- the status of R26 as completed but not independently externally reviewed before R27;
- the source manifest, verification and regression scripts, native/full build programs, source-publication record, independent-rebuild record, final read-only verification, referee packet, and delivery binding;
- the relation among complete Companions E/D/C/B/A/X/W/V/U/T/S and the native R27 dependency graph; and
- a targeted comparison with multichain Markov-renewal programs, generalized inverses and Poisson equations, ergodic approximation functionals, long-run POMDP values, finite-memory long-run strategies, strategic-measure existence, finite-memory belief approximation, and average-cost filter-contraction theory.

The native article is 31 pages. The eleven complete companions contain 301 pages, so the packet contains twelve PDFs and 332 pages. The companions preserve R26 and earlier complete articles. They are not hidden premises of the new two-sided theorem. Editorial assessment should therefore be based primarily on the 31-page native article, with the companions used for provenance and historical comparison.

The committed source audit records 40 ordinary native files plus the source manifest, 14 active TeX inputs, 103 labels, 145 cross-references, 15 bibliography entries, and 33 formal statements. The independent reconstruction used the actual downloaded workflow artifact, verified that all 730 input files remained byte-identical, and rebuilt the native article and all companions in a second TeX environment. The twelve PDFs have matching page counts, normalized texts, and rendered pixels across environments for all 332 pages. Raw PDF bytes differ across TeX Live versions, as the receipts explicitly state. The native finite suite records 7,534 exact checks, with ordinary and optimized Python output identical.

These controls are useful source-integrity, arithmetic, and reproducibility evidence. They are not proofs of the continuum statements, and the repository consistently says so. I did not independently re-audit every theorem in every historical companion, every v1--v96 branch, every old review branch, or every independent realization paper. Preservation and render parity are not fresh mathematical certification.

---

## 2. Executive assessment of Revision R27

R27 changes the center of the long-run argument from a qualitative or cost-universal recurrence condition to a **task-sensitive quantitative obstruction**.

R25 treated retained observer state across physical preparations by imposing bounded group-inverse recurrence sublevels. R26, according to the retained complete manuscript and response, replaced cost-universal recurrence by a qualitative task-visible condition: continuity of the specified gain is equivalent to uniform finite-acquisition and discounted convergence and to finite approximate-corrector prices. R27 adds the missing converse and the missing scale.

For every model--program pair it constructs the approximation functional

```text
k_N(x)=inf_u { ||b_x-(I-P_x)u||_infinity + osc(u)/N }.
```

The associated family quantity `K_N` is then compared in both directions with

```text
Delta_N = sup_x max_{1<=t<=N} ||t(J_t(x)-g_x)||_infinity / N.
```

The prefix maximum is mathematically necessary: periodic cancellation can make `J_N-g` vanish at selected terminal horizons while a nonzero temporal obstruction remains. The physical return term is also necessary: all boundary quantities may vanish while scores are front-loaded within a long excursion.

The upper direction is the familiar one: an approximate marked Poisson corrector telescopes along the retained boundary, and physical overshoot is paid separately. The converse is the new part. The actual first-excursion recursion for `H_t=t(J_t-g)` is averaged over `t=1,...,N`; the shifted future sums leave exactly the last `min(tau,N)` prefix values. This produces a concrete `u_N` whose residual and oscillation are bounded by the physical discrepancies and the true return remainder.

The exact dual then turns this approximation functional into a finite signed balance problem. For fixed rational response data it is an ordinary linear program. The dual does not synthesize the unknown-model observer, but it can certify that a claimed physical-prefix rate is impossible for the stated entering-row family.

R27 next applies the same mechanism to actual predictive occupation. The bounded-Lipschitz test family is treated as an additional compact parameter. A clipped squared-distance witness localizes the temporal comparison to the codebook radius. This improves the crude stability estimate one would obtain by transporting full squared distortion directly.

Finally, the paper supplies two complementary sharpness routes:

1. a primitive diagnostic continuum in which arbitrary continuous task amplitude and revelation intensity give an exact all-history minimax profile attained by two labels; and
2. a fresh-load delayed-score protocol in which every adaptive controller acquires a definite amount of the true mark law during a finite physical prefix.

These results form a coherent article. The strongest claims are no longer merely “there exists a compact sublevel” or “a finite table can be enumerated.” They identify a task-visible temporal functional, prove a converse, and connect its scale to acquired finite-memory geometry.

---

## 3. Response to the R25 external report

R27 is not a cosmetic revision. It addresses several of the most important limitations identified in the R25 report, while retaining the complete R26 qualitative article rather than pretending that R26 had already received an external verdict.

| R25 issue | R27 assessment |
|---|---|
| Uniform long-run transfer required a bounded group-inverse recurrence sublevel | **Substantially resolved for one task.** R26/R27 replace cost-universal recurrence by task-gain compatibility and approximate-corrector prices. |
| Recurrence exhaustion did not provide a converse or intrinsic scale | **Resolved temporally.** `K_N` is equivalent, up to the actual return remainder, to maximal normalized physical-prefix discrepancy. |
| A lower certificate for slow physical acquisition was missing | **Resolved at the response level.** The exact signed dual supplies boundary-balance certificates, with the all-row/fixed-start distinction made explicit. |
| Joint duration and exit information could be lost | **Resolved.** Both the bias and the renewal converse use the marked matrix `T_ij=E[tau 1_exit=j]`. |
| Geometry was conditional and asymptotic | **Improved.** The resolution theorem gives an `N`-call lower from actual limiting submass when occupation error is small at radius scale. |
| Fixed-exploration geometry could be overread as optimized control | **Improved in the statements.** The optimized corollary separately quantifies all-competitor witnesses and an attaining fixed-size exploration. |
| Actual finite-horizon mass for every controller was not derived broadly | **Resolved in a loaded-task raw class.** Predictable early starts give a common finite-prefix submeasure under an all-adaptive conditional service-mean bound. |
| Sharpness examples were tied to a power revelation profile | **Resolved.** Arbitrary continuous profiles, including logarithmic rates, are treated exactly. |
| Raw applications were too realization-specific | **Improved, but not fully resolved.** Queue and quantum mechanisms independently verify temporal and loaded-task hypotheses, but only for explicit task factors. |
| General nondominated/nonregenerative control remained open | **Still open.** Direct examples do not produce general compactness or a general history theorem. |
| Efficient synthesis and the full resource region were absent | **Still open.** Algebraic decidability and finite LP evaluation are not practical global synthesis. |
| A recognized difficult natural application was needed for a top-four case | **Still unresolved.** The exact profile and controlled-load protocols are sharp but purpose-built. |

The previous report asked for a theorem whose regularity condition was task-sensitive rather than a universal group-inverse bound. R27 delivers such a theorem and, importantly, gives a quantitative converse. The remaining top-four question is now whether this marked approximation functional and its occupation-geometric consequences have sufficient intrinsic breadth and external impact.

---

## 4. Audit of the physical-acquisition modulus

### 4.1 Correct physical-time data

The paper distinguishes the retained boundary from the physical experiment. The retained boundary is finite; the physical state may be infinite. One physical excursion started from retained label `i` produces a duration, complete reward, exit label, and full marked transcript. The conditional excursion law depends only on the fixed model, fixed program, and entering retained label.

The data

```text
P_ij = P_i(I_1=j),
T_ij = E_i[tau 1_{I_1=j}],
r_i  = E_i R
```

retain the dependence of duration on the exit label. This matters. In general

```text
T g != diag(E tau) P g.
```

The time-changed stochastic matrix

```text
S = I - D^{-1}(I-P)
```

has the same off-diagonal graph and closed classes as `P`; its stationary weights reproduce the correct classwise reward-to-duration ratios. The gain `g=Pi_S D^{-1}r` is therefore `P`-harmonic. On each closed class the marked residual `b=r-Tg` has stationary mean zero, which puts it in the range of `I-P`.

These are classical finite semi-Markov identities, but they are used correctly here.

### 4.2 Physical upper bound

For any approximate corrector satisfying

```text
||b-(I-P)u||_infinity <= a,
```

the stopped excursion sum produces three terms:

- an accumulated residual bounded by `aN`;
- a corrector boundary bounded by `osc(u)`; and
- the score/duration contribution after physical call `N`, bounded by the actual overshoot.

The martingale term from the harmonic gain has mean zero under predictable coefficients. Dependence among reward, duration and exit label is retained. The final estimate has the correct form

```text
||J_N-g|| <= a + osc(u)/N + physical return remainder.
```

This is an upper bound for the same program and same retained labels, not a comparison with a separately optimized program.

### 4.3 First-excursion converse

The converse begins from the exact recursion

```text
H_t(i)=b_i-a_t(i)+E_i H_(t-tau)_+(I_1),
```

where `a_t` is the difference between the unobserved tail reward and the duration-weighted future gain. Both components are bounded by the actual remaining duration. Averaging over `t=1,...,N` and shifting the future sums leaves exactly the terminal strip of the first excursion. The resulting averaged vector `u_N` satisfies

```text
||b-(I-P)u_N|| <= B_N + mu_bar Delta_N,
osc(u_N)/N <= 2 Delta_N.
```

This yields the reverse comparison. The proof does not sample duration independently of the exit label and does not initialize in stationarity.

The normalization of `Delta_N` by the total budget `N`, rather than by each prefix `t`, is essential for this exact converse and should remain prominent in the theorem statement.

### 4.4 Exact dual

Modulo additive constants, the primal is a finite coercive linear program. Fixing one coordinate gives attainment. The conjugate of the oscillation seminorm on zero-sum vectors is half the `l^1` norm, producing

```text
||z||_1 <= 1,
||(I-P)^Tz||_1/2 <= 1/N.
```

The dual vector is signed and approximately invariant. The manuscript correctly avoids calling it an occupation measure. It also correctly limits the lower conclusion to the maximum over entering rows unless a fixed-start accessibility argument is supplied.

### 4.5 Uniform limiting equivalence

Under all-row uniform integrability of the return time, `B_N` vanishes. The two-sided theorem then makes `K_N -> 0` equivalent to uniform finite-acquisition convergence. This does not require a uniform exact group-inverse bound. The exact corrector may diverge while approximate correctors at the physically relevant scale remain affordable.

The diagnostic family provides a convincing demonstration: the recurrent rank changes and the exact group inverse diverges, but the vanishing task amplitude makes the gain continuous and gives a finite approximate-corrector price with the sharp acquisition rate.

---

## 5. Concrete technical correction: crossing-index convention

The proof of Lemma `lem:physical` contains an off-by-one assertion. With

```text
S_0=0,
S_k=sum_{j<k} tau_j,
K_N=min{k>=1:S_k>=N},
```

positive integer durations imply

```text
K_N <= N+1,
```

not `K_N <= N`. If every excursion has duration one, `S_k=k-1` and `K_N=N+1`.

The proof sums over `k<K_N`, and there are at most `N` such indices. Thus the predictable stopped sum remains bounded by `N`, and the stated risk inequality appears unchanged. The manuscript should replace the incorrect bound and state explicitly whether `K_N` indexes the first boundary at or after `N`, the crossing excursion, or the first excursion after the crossing boundary.

The controlled-load section uses related notation for `K_N`, `K_{N-2}`, and excursion start times. That proof's predictable-start idea is sound, but the two sections should use one common convention and one short diagram or table of indices. This will prevent an otherwise repairable issue from obscuring a central physical-time argument.

---

## 6. Task-visible qualitative theorem and robust optimization

The inherited qualitative theorem is conceptually important. On a compact continuous-response family with uniformly integrable returns, the following are equivalent:

- continuity of the specified gain;
- compatibility of every limiting ergodic projection with that gain;
- uniform finite-acquisition convergence;
- uniform normalized-discount convergence; and
- finiteness of the approximate-corrector price at every positive residual tolerance.

The proof of continuity implying finite price does not assume a bounded exact group inverse. It uses uniform Cesàro annihilation of the particular marked residual `b`, then constructs finite Cesàro correctors. This is exactly the distinction required by the rare-revelation example: a slow recurrent mode can be invisible to the declared task.

When this criterion holds on the whole compact legal program class, the worst-model gain is continuous, robust attainment follows, and finite model families determine the value by the finite-intersection property. These conclusions are correct within the declared class. They should not be described as automatic consequences of positivity or compact report spaces; the manuscript generally respects this boundary.

The cost-universal group-inverse sublevels remain a useful special case. Their role is now correctly subordinated to the task-visible criterion rather than presented as necessary.

---

## 7. Algebraic and effective layer

For finite algebraic instruments the alive-state resolvent formulas are standard and appropriate. In particular the duration mark uses `(I-A)^{-2}`, while reward uses `(I-A)^{-1}`. The same finite-dimensional linear structure works for unnormalized completely positive maps on Hermitian blocks.

The ergodic projection and gain are semialgebraic on finitely many rank strata. Quantifier elimination can therefore decide continuity and formulate the worst-model optimization. If the approximate-corrector price is finite for every `a>0`, one-variable semialgebraic growth gives a polynomial upper near zero and hence an explicit, though not necessarily sharp, acquisition exponent.

This is a valid decision-theoretic conclusion under strong algebraic input. It is not a polynomial-time result. The size and complexity of the quantifier-elimination problem, the representation of algebraic randomization, report parsing, and finite-precision execution remain separate.

The near-optimal recurrence schedule is also carefully scoped. It requires a support graph that is common in the model parameter for each fixed program. It permits recurrence bounds to diverge along a near-optimal program curve and does not claim an optimizer at the limit. The rank-changing quantum family correctly lies outside this support-stable schedule and instead uses task compatibility.

---

## 8. Actual occupation and finite-resolution geometry

### 8.1 Occupation is the actual physical-time law

The class-weighted occupation formula divides each recurrent class's expected scored occupation by its own mean duration and only then mixes using absorption probabilities. Preparation and unscored calls remain in the denominator. Transient boundary occupation has zero long-run mass. This is the correct measure for a retained-state Markov-renewal process.

The checkpoint identity is an ordinary conditional-square projection applied to this actual subprobability measure. Every online observer with at most `J` fixed task responses has at least the corresponding `q_J` distortion under its own acquired law. Labels used jointly for control and prediction do not create additional readout values.

### 8.2 Temporal occupation criterion

Testing the occupation with the compact class of bounded one-Lipschitz functions reduces bounded-Lipschitz continuity of the measure to the task-visible gain criterion on the product family. This step is sound under the stated assumption that the predictive feature is executable and that finite responses for its Lipschitz tests are continuous.

The paper appropriately excludes an unrecorded posterior about a nonreset latent quantity. If such information is needed, it must be included in the retained boundary or supplied by a common predictive realization.

### 8.3 Resolution-localized lower

For a candidate codebook `C`, the function

```text
phi(p)=min{dist(p,C)^2,r^2}
```

is `2r`-Lipschitz. If a genuine limiting submeasure of mass `w` puts at most `A(r)` in every radius-`r` ball and `M A(r)<=w/2`, at least half the witness mass contributes `r^2`. Transporting `phi` from limiting occupation to `N`-call occupation loses only `2r d_K`.

This produces

```text
q_M(nu_N) >= (w/2)r^2 - 2r zeta_N.
```

The scaling is correct. The midpoint example shows that an occupation perturbation of order the cell radius can collapse an `M`-point lower even though the limiting continuous law has distortion of order the squared radius. Thus the acquisition condition must be calibrated at resolution `r`, not inferred from unquantified weak convergence.

### 8.4 Causal upper and optimized matching

The recursive upper is genuinely causal only because the manuscript separately supplies:

- a retained exploration coordinate;
- a common predictive initialization at preparation;
- a Borel update on a declared candidate domain;
- global candidate-valid covers;
- a same-report error recursion; and
- an actual occupation `L^2` stability bound.

The predictor coordinate is reset at preparation while the retained control coordinate survives. The product `QJ` is counted.

The optimized matching corollary does not follow from fixed-exploration geometry alone. It explicitly assumes that every competing observer, under its own law, has a common small-ball witness and full-history baseline lower, while a fixed `Q`-label exploration attains that baseline and has the required recursive implementation. These assumptions are strong but correctly visible. The paper should resist summarizing this corollary as a general optimal-control dimension theorem.

---

## 9. Raw controlled-load mass

The controlled-load protocol is a useful independent route to all-controller geometric mass. A fresh mark is prepared, a charged load call reveals it, and at least one scored service call follows. The conditional mean number of service calls is uniformly bounded for every mark, entering history, model, and adaptive strategy.

The lower must handle the fact that the crossing excursion can depend on the mark. The published proof correctly counts starts sufficiently early that their first scored service is guaranteed to occur before the prefix ends. The expected number of such predictable starts is controlled by the conditional mean duration, and each associated mark is still fresh with law `rho`. This yields a genuine measure inequality rather than an additive total-mass error.

For prediction risk, each guaranteed first service requires encoding a fresh mark into at most `M` fixed readouts, giving a direct `q_M(rho)` lower for every controller. A nearest-center load followed by holding the center gives the upper. This is a clean exact task, with zero full-history prediction baseline.

The queue and quantum subclasses verify the same conditional-return premise in different ways:

- negative workload drift gives a uniform conditional service-mean bound for every adaptive queue action; and
- an unnormalized alive completely positive map satisfying a dual trace contraction gives geometric survival and a uniform mean bound.

The loaded mark is an explicit task factor. These examples do not establish that the full workload posterior or full quantum predictive quotient has the same finite dimension, and the manuscript states this correctly.

---

## 10. Sharp diagnostic and profile theorems

The all-history lower is particularly clean. Under the equal prior on the two hidden signs, histories are identical until the first conclusive report. Every strategy, including history-dependent randomized strategies, therefore has conditional error one half before revelation. Summing the no-revelation probabilities gives the exact minimax expression.

A two-label stationary program attains this bound simultaneously at every horizon and every parameter value: it stores a fair sign initially, retains it on inconclusive reports, and overwrites it upon revelation. No horizon counter is used.

For arbitrary continuous task amplitude `a(t)` and revelation intensity `lambda(t)`, the physical modulus becomes

```text
Psi_n = sup_t a(t) min{1,1/(n lambda(t))}.
```

The exact diagnostic value lies between fixed multiples of this modulus. Power profiles give algebraic rates; a logarithmic amplitude gives a nonalgebraic rate. This is a strong sharpness result for the temporal theorem and demonstrates why compactness and gain continuity do not force a universal algebraic acquisition exponent.

The result should nevertheless be positioned carefully relative to classical finite-memory binary learning. Hellman and Cover already established a foundational theory of learning with finite memory. The novelty here is not that two states can retain a revealed binary sign, but the exact horizon-uniform task profile, its identification with the marked residual--oscillation functional, and its integration into the physical-call and multiresource framework.

---

## 11. Same-task multiresource law

The four-call protocol correctly charges preparation, diagnostic decision/report, fresh-mark load, and terminal audit. The diagnostic and calibration audit wires are not feedback. The mark is freshly prepared independently each round; the calibration sign is fixed and invisible.

The lower bounds add under one product prior:

- finite readouts give `q_M(rho)` for the fresh mark;
- the two invisible calibration signs give `delta^2`; and
- the two diagnostic signs give the exact no-revelation lower.

The upper stores the diagnostic sign and one of `floor(M/2)` mark centers, using at most `M` labels. It has no access to the model or a free horizon.

The erased revelation interface is an actual pair of experiments. The identity report map gives the upper deficiency, and indistinguishability at a parameter with `lambda(t)=e` gives the lower `e/2`. The paper correctly avoids asserting that the deficiency equals the input symbol `e` exactly.

The simplified asymptotic sum requires both acquisition-profile doubling and quantization doubling. Without those hypotheses the exact sandwich is the correct statement. The manuscript preserves this distinction.

This section proves a sharp selected slice of a multiresource region. It does not establish simultaneous optimality of program description, workspace, arithmetic precision, physical time, or simulator state.

---

## 12. Literature position and novelty

R27's native bibliography correctly cites classical multichain Markov-renewal programs, generalized inverses, sufficient statistics, quantization, finite-memory learning, real algebraic geometry, approximation functionals, and Poisson/martingale methods. It also explicitly credits Shaw for ergodic approximation functionals and Glynn--Infanger for Poisson representations.

The final version should, however, restore a theorem-level comparison with the modern long-run partially observed control literature that appeared more fully in earlier restart manuscripts. At minimum it should discuss:

1. **Venel and Ziliotto, “Strong Uniform Value in Gambling Houses and Partially Observable Markov Decision Processes,” SIAM Journal on Control and Optimization 54 (2016), 1983--2008, DOI 10.1137/15M1043340.** They prove a strong uniform value for POMDP-type models. R27 should explain precisely why its fixed-memory, marked physical-prefix modulus is neither implied by nor a substitute for that uniform-value theorem.

2. **Chatterjee, Saona and Ziliotto, “Finite-Memory Strategies in POMDPs with Long-Run Average Objectives,” Mathematics of Operations Research 47 (2022), 100--119, DOI 10.1287/moor.2020.1116.** They prove approximately optimal finite-memory strategies for long-run average POMDPs. The distinction between growing finite memory sufficient for near optimality and R27's exact fixed-`M` task profile is central.

3. **Yu and Bertsekas, “On Near Optimality of the Set of Finite-State Controllers for Average Cost POMDP,” Mathematics of Operations Research 33 (2008), 1--11.** R27 should compare its retained-boundary program class and same-budget lower/upper statements with their average-cost finite-state-controller approximation.

4. **Yüksel, “Another Look at Partially Observed Optimal Stochastic Control: Existence, Ergodicity, and Approximations without Belief-Reduction,” arXiv:2301.11244.** This work studies discounted and average control directly on history space and finite-window approximations. R27's regenerative marked-boundary topology is different and should be compared explicitly.

5. **Demirci, Kara and Yüksel, “Average Cost Optimality of Partially Observed MDPs: Contraction of Nonlinear Filters and Existence of Optimal Solutions and Approximations,” SIAM Journal on Control and Optimization 62 (2024), 2859--2883, DOI 10.1137/24M1643736.** Their filter-contraction route includes finite-memory near optimality. R27's task compatibility permits noncontractive and rank-changing examples but imposes a regenerative finite boundary; neither result subsumes the other.

6. **Yu, “On Strategic Measures and Optimality Properties in Discrete-Time Stochastic Control with Universally Measurable Policies,” Mathematics of Operations Research 49 (2024), 1734--1760, DOI 10.1287/moor.2022.0188.** This is relevant to the distinction between compactness/existence for broad policy-induced strategic measures and closure of R27's reused finite-row program class.

7. **Leizarowitz, “An Algorithm to Identify and Compute Average Optimal Policies in Multichain Markov Decision Processes,” Mathematics of Operations Research 28 (2003), 553--586.** This is relevant to claims about multichain optimal-policy existence and recurrence exhaustion.

These comparisons should be stated at the level of policy class, memory accounting, physical horizon, average criterion, robustness, and conclusion. A short bibliography paragraph is not enough for a paper whose top-four case depends heavily on distinguishing its fixed-memory causal obstruction from existing average-control and finite-memory results.

The precise candidate contribution I see is:

> a task-sensitive, two-sided, prefix-and-tail-qualified approximation functional for marked physical-time acquisition, with an exact finite boundary-balance dual, followed by resolution-localized transfer to actual acquired occupation and explicitly charged causal memory.

That is a coherent and potentially publishable specialist contribution. It is narrower than an intrinsic classification of finite-memory predictability or a general solution of average-cost partial observation.

---

## 13. Major revisions required before specialist-journal publication

### 13.1 Correct and standardize physical-crossing indices

Repair `K_N<=N` to `K_N<=N+1` under the current `S_k=sum_{j<k}tau_j` convention, explain that the number of indices `k<K_N` is at most `N`, and use the same indexing in the controlled-load proof.

### 13.2 Make the central novelty theorem-level and concise

The introduction should state in one paragraph exactly what is new relative to classical approximation functionals and semi-Markov Poisson equations: the actual duration--exit renewal converse, maximal physical-prefix normalization, explicit return remainder, exact finite signed dual, and finite-resolution occupation transfer.

### 13.3 Add the modern long-run POMDP comparison

Restore the direct comparisons listed in Section 12 above. The distinction from strong uniform values and finite-memory near optimality is essential to evaluating the result.

### 13.4 Separate three uses of “general”

The manuscript should visibly separate:

- the noncompact quantitative inequality for a fixed finite marked boundary;
- the compact-family qualitative/robust optimization theorem; and
- the spatial causal matching theorem with common predictive and cover/stability data.

These are mathematically different layers.

### 13.5 Clarify fixed-start versus all-row lower certificates

The theorem already contains the correct warning. Add one explicit proposition or example showing how accessibility converts an all-row dual witness into a lower from a prescribed initial law, and why it can fail without accessibility.

### 13.6 State `B_N` consistently as a family-dependent object

The return remainder depends on the family over which the supremum is taken. Use notation such as `B_N(X)` when several nested families occur, especially in the occupation-test product family.

### 13.7 Clarify subprobability bounded-Lipschitz conventions

State explicitly that the constant test belongs to the test class and therefore controls total scored occupation mass as well as location. This will make the occupation metric on subprobabilities completely transparent.

### 13.8 Keep optimized control separate from fixed exploration

The optimized matching corollary should be advertised only with its all-competitor witness and attaining-exploration hypotheses. The fixed-exploration theorem is already valuable without this stronger claim.

### 13.9 Strengthen one natural application

A top-tier specialist presentation would benefit from one application in which the policy is not designed merely to reveal and hold a fresh mark. A controlled partially observed queue or quantum experiment with a genuinely nontrivial acquisition/control tradeoff would materially improve external significance.

### 13.10 Sharpen the effective-complexity discussion

Give at least one nontrivial upper or lower complexity result for computing the fixed-response LP or the semialgebraic acquisition schedule, or explicitly move the exhaustive algebraic certification to a secondary role.

### 13.11 Reduce pipeline prose in the mathematical narrative

The native article is reasonably concentrated, but source provenance, complete companions, build parity and finite regression counts should remain outside the mathematical introduction and conclusion. They are delivery evidence, not part of the theorem's significance.

### 13.12 Reconsider the breadth signaled by the title

The title is historically fixed by the project, but the abstract and first page should make the finite-boundary marked-regenerative and task-visible scope unavoidable. “Foundations” should not suggest a necessary-and-sufficient spatial theory for arbitrary causal experiments.

---

## 14. Technical and expository comments

1. In Lemma `lem:physical`, correct the off-by-one bound for `K_N` as discussed above.
2. Use one notation for the crossing boundary, crossing excursion and number of started excursions throughout Sections 3, 7 and 9.
3. In the dual display write `||z||_1` and `||(I-P)^Tz||_1` unambiguously; the current TeX source is readable but visually compact.
4. State explicitly that a dual maximizer may depend on the fixed response `x` and is never a runtime object.
5. In the lower certificate, quantify “for each fixed `x` and each feasible `z`” before passing to the family `Delta_N`.
6. Give a one-line treatment of `K_N=0` in the factor-two balancing corollary rather than relying on the limiting `eta` argument implicitly.
7. Distinguish `N` as physical calls from the number of excursions in every displayed asymptotic rate.
8. The periodic two-state example should show the short computation of `Delta_N=1/(2N)` for odd and even prefix maxima, not only state the value.
9. In the front-loaded excursion example, say explicitly whether the preparation call is included in the four calls.
10. In Theorem `thm:occupation`, define the bounded-Lipschitz norm convention for subprobabilities in the theorem statement or immediately before it.
11. In Lemma `lem:quantization`, note that Euclidean projection into `conv K` does not increase distance to points of `K`.
12. The symbol `delta` is used for numerical relation error in the recursive theorem and for calibration magnitude in the joint task. Use different symbols in the final version.
13. State whether repeated task readouts attached to different control labels count once or several times in the checkpoint codebook; the lower only needs “at most `M` distinct values.”
14. In the optimized geometry theorem, state the exact range of `M` for which the small-ball radius lies within `r_0`.
15. In the resolution theorem, the test `phi/(2r)` is bounded by `r/2`; mention `r<=1` to show immediately that it belongs to the declared test class.
16. In the controlled-load theorem, clarify whether `rho` is model-independent in the robust family. The stated common codebook upper uses that fact.
17. In the controlled-load upper, explain in one sentence why including service loss after the finite prefix only enlarges the nonnegative score and hence is a valid upper estimate.
18. In the queue realization, distinguish the support-stable architecture theorem from the broader all-controller controlled-load theorem more visibly.
19. In the quantum USD example, record the complete physical call accounting next to the theorem statement, not only in its proof.
20. In the raw quantum geometric example, separate “finite response continuity” from the weaker measurable conditions sufficient for the direct mark theorem.
21. In the arbitrary profile theorem, state the limiting convention at `lambda(t)=0` in the exact diagnostic formula as well as in `Psi_n`.
22. In the deficiency lower, make explicit that the future fresh mark and the environment audit are not available before the target report deadline.
23. The phrase “all histories” should consistently mean all legal visible histories and fresh private randomization, not access to the environment audit.
24. In the semialgebraic theorem, state the representation model for algebraic coefficients and the output form of the certified exponent.
25. The real-algebraic optimum need not have a practical bit representation for direct sampling; retain the current caveat and move it closer to the theorem.
26. In the recurrence schedule theorem, emphasize in the statement that the common support graph is per fixed program over all models, not globally fixed over all programs.
27. The reference to Shaw is useful but relatively obscure. Identify the precise earlier discrete approximation-functional source credited there, if available.
28. Add the modern long-run POMDP references listed above to the native bibliography.
29. Keep the distinction between the finite task factor and the full queue/quantum predictive quotient in every summary table.
30. State explicitly that successful LP certificate checks and finite regressions verify only selected finite instances and algebra, not the continuum theorem.
31. The native article has 33 formal statements in 31 pages. A short roadmap grouping “new R27,” “retained R26,” and “realization” statements would help readers.
32. The appendix-like pipeline ledgers should not be cited as mathematical premises in the paper; the current dependency map correctly avoids that.

---

## 15. Routes that could materially change the top-four assessment

A further revision would materially change my general-journal assessment if it achieved one or more of the following, with complete proofs rather than only programmatic goals:

1. **A nonregenerative or history-space theorem.** Extend the task-sensitive two-sided obstruction beyond a finite marked regenerative boundary to a substantially broader partially observed process class.

2. **A near-necessary spatial causal criterion.** Complement the temporal approximation functional with a necessary-and-sufficient or dual spatial criterion for when an acquired-law quantizer admits an online finite-state realization.

3. **A recognized difficult natural application.** Resolve a concrete open or widely recognized hard question in average-cost POMDPs, robust filtering, causal coding, controlled queueing, or quantum control.

4. **A strong uniform-value connection.** Prove that the physical modulus yields a new fixed-memory strong-uniform or Blackwell-type theorem not covered by existing POMDP or semi-Markov theory.

5. **General nondominated common-program theory.** Replace product-dominated response compactness by a broader intrinsic topology while retaining one reused program.

6. **Nontrivial synthesis complexity.** Go beyond decidability/exhaustive enumeration and prove meaningful upper and lower complexity bounds for fixed-memory global synthesis.

7. **A matched joint resource region.** Establish lower as well as upper bounds for program description, workspace, numerical precision, physical time and simulator state, not only persistent labels and selected statistical errors.

8. **An intrinsic invariant.** Reduce the law-valued and task-parameterized conditions to a robust numerical or categorical invariant with clear necessity, sufficiency and composition properties.

Absent such an advance, the present R27 result is better viewed as a strong, carefully constructed specialist theorem than as a top-four general mathematics result.

---

## 16. Delivery and reproducibility assessment

The source/artifact/evidence chain is clearly separated:

```text
ordinary source: 4a9f9a36f6ad02561f8e8eae112674f3f3c5d777
artifact:        6ca75d078bc710cdbdf2feedf5744409947aaa37
review head:     c5f05d1944251a95619d5cdad814c5c83646429c
```

The evidence-only head is a direct child of the artifact and adds only the declared verification records. The independent reconstruction used the downloaded GitHub Actions artifact rather than an uncommitted working tree. All 730 input files remained byte-identical.

Hosted and independent environments each performed thirty isolated PDF builds, three TeX passes per build. The ordinary and optimized native regression outputs agree. The twelve delivered PDFs have equal page counts, normalized text and rendered pixels across TeX environments for all 332 pages. Cross-environment PDF bytes differ, while repeated builds within each environment are byte-identical. The 31 native pages were visually inspected.

The source audit reports 40 ordinary files plus manifest, 14 active TeX inputs, 103 labels, 145 cross-references, 15 bibliography entries and 33 formal statements. The finite suite reports 7,534 exact checks.

These records are unusually thorough and appear internally consistent at the level checked. They support provenance and reproducibility. They do not establish the continuum proofs, novelty, priority or journal significance, and the repository explicitly acknowledges this limitation.

---

## 17. Final assessment

R27 is a serious revision. It answers the most important technical limitation of R25's recurrence-sublevel theory by replacing a cost-universal exact regularity scale with a task-sensitive approximate-corrector functional and then proving a genuine physical-time converse. The exact signed dual, the resolution-localized occupation lower, the predictable-start raw mass theorem, and the arbitrary revelation-profile sharpness result are meaningful additions.

The paper is also more honest than many manuscripts of comparable breadth about its quantifiers and interfaces. It distinguishes all-row from fixed-start lower bounds, signed duals from acquired measures, limiting occupation from preparation law, fixed exploration from optimized control, task factors from full predictive quotients, actual deficiency from allowed tolerance, and persistent labels from total computational complexity.

Nevertheless, the main mechanisms remain close to classical finite semi-Markov evaluation, Poisson approximation functionals, linear programming, quantization and finite-memory learning. Their new marked causal synthesis has not yet produced an external mathematical consequence of the breadth normally required for the top four general journals. The most ambitious spatial and control statements still require strong supplied witnesses and purpose-built raw protocols.

I therefore recommend rejection at the top-four level in the present form, while regarding the manuscript as a potentially strong specialist-journal contribution after the technical correction, a sharper literature comparison, and a more concentrated account of the genuinely new theorem.
