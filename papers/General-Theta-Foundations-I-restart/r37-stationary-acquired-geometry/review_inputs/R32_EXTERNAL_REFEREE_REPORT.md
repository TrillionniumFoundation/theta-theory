# Referee Report — *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*

**Submission:** *General Theta Foundations I: Acquired Geometry and Causal Resource Transfer*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed referee-ready branch:** `referee-ready/general-theta-restart-r32-bayesian-curvature-2026-10-11`  
**Reviewed exact branch head:** `0982c854ddc20c2725f12f0fed67d61111776158`  
**Reviewed branch root tree:** `dc1f6cbc0f67cbcc5863fc2231cd882f25e605d3`  
**Ordinary mathematical-source commit:** `6a62f90eff5357d6e47b3faeba13a25e8500dee8`  
**Ordinary mathematical-text projection:** `97c35f107294a7a07308ce06813507895f4a529c`  
**Native directory tree:** `cd1b073ffda928e27e34009df120ac997f05bcc8`  
**Hosted artifact commit:** `20838ed65f7ff50cda2cb726f393929e42d37c74`  
**Native PDF SHA-256:** `cd52269725ce8e64b39b54ce9d0b85c1cf422a5546f711579d0e8a87b7711a9e`  
**Native article length:** 23 pages  
**Complete deposited packet:** fourteen PDFs, 376 pages  
**Predecessor external report:** R29 review head `204a9cc62c2c1ce48d0668f35c4bbc326118ebd7`, report blob `dd9a1681b0e807e892c4c053640ec8e332ca94e1`  
**Intervening research-only intakes:** R30 and R31  
**Review branch:** `review/general-theta-restart-r32-bayesian-curvature-external-top4-referee-r32-2026-10-11`  
**Date:** 11 October 2026

This is an author-requested external mathematical assessment deposited in the repository. It is not a commissioned editorial decision of a named journal, a formal proof certificate, an independent priority certificate, or a claim of acceptance by any journal.

---

## Recommendation

**Reject at the level of the Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica in the manuscript's present form.**

This is **not a technical-correctness rejection**. Revision R32 is a genuine and substantial advance over R29. It answers the most important mathematical request in the preceding report: the central causal compression mechanism is no longer restricted to state-independent report laws or Haar relative transport. The manuscript now treats informative state-dependent likelihoods and normalized Bayesian updates through one experiment-level theorem, and it verifies that theorem in a nonlinear Gaussian hidden-state filter and in a noncommuting positive quantum instrument.

The central identity is mathematically coherent. If the unnormalized report/test response is affine,

```text
U_t(y,u)=a_t(y)+A_t(y)u,
ell_t(y,u)=ell_t^0(y)+c_t(y)u,
F_t(y,u)=U_t(y,u)/ell_t(y,u),
```

and if `X_t` is the full-history predictive vector while `V_t=E[X_t|S_t]` is the predictive vector retained by a finite observer label, the paper introduces the convex perspective potential

```text
Phi_t(u)=integral ||U_t(y,u)||^2/ell_t(y,u) d lambda_t(y)
```

and proves the exact decomposition

```text
r_t = E Phi_t(X_(t-1)) - E Phi_t(V_(t-1))
      + D_row,t + D_pool,t.
```

The first term is the information about the old predictive state that remains inaccessible after observing the current report when only the old finite label is retained. The second is ordinary within-row finite quantization. The third is the additional loss caused by assigning incompatible conditional centroids from different predecessor labels to one outgoing label. All three terms are nonnegative. The lower bound covers every legal Borel randomized finite-state observer, not merely a chosen recursive quantizer.

The manuscript also correctly separates three logically different notions of compatibility:

1. attainment of the static quantization optimum in each incoming row;
2. equality of the incoming centroids pooled into one outgoing label at a single update; and
3. existence of a globally compatible recursion over the whole experiment.

It does not infer the third from the first two. Instead, the matching upper uses either common calibrated cells and a likelihood-curvature recursion, or an explicitly stable same-report posterior recursion on a global cover.

The load-bearing proofs I checked did not reveal an elementary defect invalidating:

- the likelihood-reweighted conditional barycenter identity;
- the convex-perspective/Jensen decomposition;
- the exact row and cross-row pooling decomposition;
- the all-Borel randomized-observer converse;
- the likelihood-weighted Hessian formula under the declared domination;
- the checkpoint quantization identity and actual-law small-ball lower;
- the common-cell curvature upper;
- the same-report metric-recursion upper;
- the positive-support internal-clock obstruction;
- the geometric integer allocation yielding the total-state upper;
- the Gaussian log-odds density and Hilbert-metric realization;
- the weak-effect quantum Jacobian and cone-metric realization;
- the bounded-gap noncontracting quantum extension;
- the full-rank/pure-rank weighted acquired-stratum result;
- the complete-task simulator and finite-precision perturbation propositions;
- the exact erased-bit deficiency;
- the retained-bit phase lower and the two-lane upper construction; or
- the source, artifact, and independent-rebuild claims at the level at which they are stated.

The negative top-four judgment concerns the **intrinsic breadth, necessity of the hypotheses, novelty relative to mature belief compression/filter stability/recursive quantization theories, and external mathematical impact**, rather than an identified fatal proof gap.

The exact identity is general for a finite affine family of executable tests, but the sharp resource law requires strong uniform certificates: every possible incoming retained barycenter must have a row law with the same small-ball exponent; a global legal cover must be supplied; the report law must have common support for the autonomous clock theorem; and either likelihood curvature or same-report posterior transport must have a summable product. These assumptions are verified in the displayed classes, but they are sufficient conditions rather than an intrinsic or near-necessary characterization of causal compressibility.

The two principal realizations are worthwhile. The Gaussian result covers every entrywise-positive invertible transition, including weakly mixing examples outside an earlier sufficient coefficient regime. The quantum result treats genuinely state-dependent noncommuting effects and every strictly positivity-improving channel in the stated family. Nevertheless, both are fixed passive filtering protocols with known kernels and a terminal prediction task. The paper does not solve an established difficult open problem in nonlinear filtering, zero-delay coding, partially observed control, quantum filtering, or unknown-model learning.

For a strong specialist journal in probability, stochastic control, information theory, quantization, mathematical statistics, or mathematical quantum information, my assessment is **favorable after a focused major revision**.

---

## 1. Review object, provenance, and pipeline inspected

A fresh complete enumeration of `referee-ready/general-theta-restart-*` branches identified

```text
referee-ready/general-theta-restart-r32-bayesian-curvature-2026-10-11
```

as the latest completed `General Theta Foundations I` revision. The continuation page was empty. The corresponding review-branch enumeration stopped at R29, so no later R30, R31, or R32 external report existed before this review.

The exact object reviewed is the terminal evidence-bound head

```text
0982c854ddc20c2725f12f0fed67d61111776158.
```

Its sole parent is the artifact commit

```text
20838ed65f7ff50cda2cb726f393929e42d37c74.
```

The referee packet identifies the ordinary mathematical source

```text
6a62f90eff5357d6e47b3faeba13a25e8500dee8
```

and the ordinary mathematical-text projection

```text
97c35f107294a7a07308ce06813507895f4a529c.
```

I reviewed the 23-page native article as the editorial object and treated the thirteen companion PDFs as technical provenance, not as one undifferentiated 376-page submission. The inspection included:

- `main.tex`, all ten native section files, the appendix, and `references.tex`;
- `README.md`, `REFEREE_RESPONSE.md`, `REFEREE_COMMENT_CONCORDANCE.md`, `THEOREM_MAP.md`, `PIPELINE_DERIVATION.md`, `PROOF_LEDGER.md`, `PROOF_AUDIT.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `SCOPE_AUDIT.md`, `LITERATURE_COMPARISON.md`, `HISTORY_COVERAGE.md`, `SOURCE_LINEAGE.md`, and the pinned-input record;
- the complete R29 external report and the R32 response/concordance;
- the status of R30 and R31 as research-only intakes rather than completed intervening submissions;
- the canonical restart charter, theorem targets, realization boundary, and retained source lineage;
- the full source manifest, verification and regression programs, build guide, source-publication record, independent reconstruction, render comparison, and referee packet; and
- a targeted primary-source comparison with sequential vector quantization, finite-state quantization, belief-state compression, recursive quantization, nonanticipative rate-distortion, filter stability, and current finite-memory belief approximation.

The independent reconstruction records 725 unchanged input files, 38 isolated PDF builds with three passes in each environment, 8,386 native finite checks, and equal normalized text and rendered pixels for all fourteen PDFs and 376 pages across the two TeX environments. Cross-environment PDF bytes differ, as the receipts explicitly state. These are useful delivery and finite-arithmetic controls. They are not continuum proofs, priority certificates, or journal decisions.

I did not independently re-prove every result in every historical companion, every v1--v96 branch, or every independent realization paper. Companion G preserves the complete R29 article; Companion F preserves a corrected temporal article with an explicit provenance cover. Their presence does not turn their entire historical content into newly refereed R32 mathematics.

---

## 2. Executive mathematical assessment

R32 moves the center of the paper from neutral transport to informative Bayesian normalization.

In R29, a report transported a finite predictive vector through a state-independent law. Conditional energy could therefore be propagated by a quadratic form. In R32, the report probability depends on the incoming predictive state. The forgotten histories inside one observer label are reweighted after the report, and the old linear energy recursion is false.

The paper handles this by working before normalization. The report likelihood and unnormalized test numerator are affine in the incoming predictive vector. The normalized posterior map is their ratio, and the expected squared posterior norm is the convex perspective of the numerator and likelihood. This produces an exact information-loss identity rather than an upper estimate.

The central result has two levels.

First, without stability, it gives a one-step identity and an all-observer converse. This is the conceptually strongest part of the article.

Second, under actual-law geometry and stability certificates, it gives matching finite-memory curves:

```text
R_cp(n,m)-B_n  asymp  m^(-2/d),
R_aut(n,M)-B_n asymp (M-n)^(-2/d),  M>=n+1.
```

The checkpoint observes the complete report history once. The autonomous machine must encode all phases and halt internally. These are distinct architectures, and the paper keeps their resource accounting separate.

The theorem is not an optimal sensing theorem. The preparation, passive report protocol, horizon, and terminal audit are fixed before the observer is optimized. The result is therefore best understood as a sharp finite-state posterior-compression theorem for a certified class of positive instruments.

---

## 3. Response to the R29 external report

R32 is not a cosmetic revision. It responds positively to the major mathematical criticisms of R29.

| R29 concern | R32 assessment |
|---|---|
| The central theorem used state-independent reports | **Resolved on a nontrivial finite affine class.** Likelihoods depend on the incoming predictive state and Bayes normalization is explicit. |
| The row/pooling identity might be a Haar artifact | **Resolved.** The three-defect identity is proved before any realization. |
| A nonlinear-filter consequence was requested | **Resolved for a passive known-kernel class.** The Gaussian hidden-state filter is genuinely nonlinear. |
| The quantum example used neutral Haar reports | **Resolved.** The weak-effect report density depends on the incoming density operator. |
| Global compatibility was not characterized | **Improved, not closed.** Local equality is exact; global matching uses sufficient common-cover or posterior-stability certificates. |
| A recognized substantive consequence was missing | **Improved but still insufficient for top-four impact.** The positive-transition Gaussian theorem is clean, but it does not settle a standard open problem. |
| Internal clock accounting needed to survive informative reports | **Resolved under equivalent positive supports.** Possible-edge support is phase independent even when probabilities differ. |
| The exact hard-state law needed a same-task error extension | **Improved.** The retained-bit theorem gives an attained deficiency and a two-lane phase bottleneck. |
| Finite-bit execution was under-specified | **Improved.** Boundary mass, arithmetic failures, readout precision, program bits, workspace, and primitive evaluation are separated. |
| The title remained broader than the theorem | **Still an editorial concern.** The paper now states its class clearly, but it is not a classification of general causal experiments. |

The revision also preserves the R29 article and the corrected temporal companion rather than silently rewriting the reviewed objects. This is good scholarly practice.

---

## 4. Audit of the normalized conditional barycenter

### 4.1 Affine unnormalized response

For a positive-mass incoming observer label `s`, put

```text
u_s = E[X_(t-1) | S_(t-1)=s].
```

Because both the report likelihood and the unnormalized test numerator are affine in the incoming predictive vector, integration over the histories pooled into `s` gives

```text
P(Y_t in dy | S_(t-1)=s)=ell_t(y,u_s) lambda_t(dy),
E[X_t 1_{Y_t in dy} | S_(t-1)=s]=U_t(y,u_s) lambda_t(dy).
```

Dividing the second identity by the first yields

```text
E[X_t | S_(t-1),Y_t]=F_t(Y_t,u_S).
```

This is the correct Bayes reweighting. It does not interchange a nonlinear normalized map with expectation under the old history law.

The proof includes the observer's previous private randomizations in the conditioning and excludes future audit outcomes. Fresh update randomization does not change the conditional mean after `(S,Y)`. The measurable conditional-integration argument avoids conditioning a continuous report on a singleton of positive probability.

I find this step correct under the stated affine closure and Borel hypotheses.

### 4.2 Scope of the affine closure

The finite affine closure is a substantive hypothesis. It says that the chosen finite family of future tests is closed under the unnormalized report instrument. The theorem does not derive such a closure for arbitrary nonlinear physical experiments.

This is an acceptable theorem class, but it should remain prominent. In particular, a finite-dimensional physical state or a finite-dimensional filter does not by itself imply the required finite test closure. The raw Gaussian and finite-dimensional quantum examples verify it directly.

---

## 5. Audit of the three-defect identity

Let

```text
W=F_t(Y_t,V_(t-1)),
c_sj=E[W|S_(t-1)=s,S_t=j],
v_j=E[W|S_t=j].
```

The paper defines

```text
D_row  = E||W-c_(S,J)||^2,
D_pool = E||c_(S,J)-v_J||^2.
```

Two nested conditional Pythagorean identities give

```text
E||W||^2 = D_row + D_pool + E||v_J||^2.
```

The raw moment identities give

```text
E||X_t||^2 = E Phi_t(X_(t-1)),
E||W||^2   = E Phi_t(V_(t-1)).
```

Subtracting from

```text
r_t=E||X_t||^2-E||E[X_t|S_t]||^2
```

proves the central identity.

The Jensen term also has the exact probabilistic form

```text
E Phi_t(X_(t-1))-E Phi_t(V_(t-1))
=E||X_t-E[X_t|S_(t-1),Y_t]||^2.
```

Thus its sign does not depend on differentiability. It measures information about the old exact predictive state that is lost inside the old finite label and is not recovered by the new report.

This decomposition is clean and correct. It is also the principal conceptual advance of R32.

### 5.1 Perspective curvature

For affine numerator `U` and likelihood `ell`, the scalar integrand is the quadratic perspective

```text
||U||^2/ell.
```

Its second variation is

```text
1/2 D^2(||U||^2/ell)[v,v]
=ell ||D F[v]||^2.
```

The manuscript's displayed intermediate numerator should be typeset unambiguously as

```text
||A v - c(v) F||^2 / ell
```

rather than the visually ambiguous `A v-F(c v)`. Here `c(v)` is a scalar. This is a notation correction, not a mathematical defect.

Under the declared integrable differentiation bound, integration gives the stated Hessian formula. The metric is generated by the actual report law and normalized update; it is not a Fisher metric inserted by assumption.

### 5.2 Nonsmooth and zero-likelihood boundary

The identity itself permits zero likelihood through the closed perspective convention. Positivity and bounded coordinate tests imply that the numerator vanishes whenever the report has zero probability at the relevant state. The sharp resource theorem, clock argument, and raw examples use common positive support. The paper distinguishes these levels correctly.

---

## 6. Audit of the all-observer converse and equality conditions

At a fixed incoming label, the law of `W` is the actual row law

```text
mu_(t,u)=(F_t(.,u))_#(ell_t(.,u) lambda_t).
```

The new finite label is a randomized measurable assignment of that law to at most `m_t` outputs. Conditional minimization under squared loss shows that no fractional assignment beats the best finite-center quantizer. Hence

```text
D_row >= sum_s P(S=s) q_(m_t)(mu_(t,u_s)).
```

The Jensen and pooling terms are nonnegative, giving the lower against every scheduled Borel randomized observer.

The local equality statement is also correctly limited. Equality in the sharper one-step bound requires:

- rowwise static quantization optimality in every positive-mass row; and
- equality of all incoming centroids assigned to the same outgoing label.

It does **not** establish a global compatible recursion. The common-cover upper is deliberately weaker and bounds `D_row+D_pool` together.

This distinction should remain central in any revised introduction. It is where the paper most clearly goes beyond simply applying static quantization at each time.

---

## 7. Audit of actual acquired geometry

The uniform row small-ball certificate is imposed on every incoming barycenter in the declared compact domain. The actual full-history law satisfies

```text
nu_t = integral mu_(t,u) nu_(t-1)(du),
```

and therefore inherits the same small-ball upper. A union-of-balls argument gives

```text
q_m(nu_t) >= c m^(-2/d).
```

A global legal cover of the prediction domain gives the matching upper. Conditional projection of the terminal audit first onto the complete history and then onto a checkpoint label yields

```text
R_cp(n,m)=B_n+q_m(nu_n).
```

The proof uses the actual acquired probability law, not volume on a reachable set. It retains the true mixture weights in the singular extension.

The price is that the row small-ball hypothesis is stronger than a lower-dimensional statement only on the preparation or only on a typical posterior trajectory. It must hold uniformly for every barycenter that a legal finite observer can create. The raw examples verify this through density/Jacobian arguments.

---

## 8. Audit of the two matching implementations

### 8.1 Curvature implementation (C)

The program chooses one common codebook covering the full legal prediction domain. For every incoming label and current report it computes

```text
W=F_t(Y_t,u_s)
```

from the stored programmed barycenter `u_s`, sends `W` to the common nearest cell, and programs the new cell representative as its conditional mean under the actual implemented observer law.

Because the common codepoint itself is an admissible competitor,

```text
D_row,t + D_pool,t <= h_t^2.
```

The Jensen defect is bounded by the curvature coefficient times the previous retained error. Iteration gives

```text
r_n <= C sum_t (product_(j>t) b_j) m_t^(-2/d).
```

The construction is an exact Borel program. It does not make its calibrated barycenters computationally free: finite forward integration and certified constant representation are separate requirements. The paper now states this explicitly.

### 8.2 Same-report transport implementation (P)

The program stores a legal codepoint and updates it using the same report received by the true predictive process. Projection back to the global cover gives

```text
dist(X_t,Xhat_t)
 <= a_t dist(X_(t-1),Xhat_(t-1)) + C m_t^(-1/d).
```

This yields the terminal squared upper

```text
B_n + C[sum_t (product_(j>t) a_j)m_t^(-1/d)]^2.
```

No exact posterior is stored. The approximate state is the codepoint named by the finite label.

The two alternatives are genuinely different. The rank-changing quantum theorem uses curvature because the cone metric degenerates on the pure-state boundary. The Gaussian and positive-interior quantum results use same-report transport.

---

## 9. Internal clock and total-state allocation

The autonomous machine has one reused transition row and one halt status for each label. All conditional report laws before stopping are equivalent to one common reference measure. Therefore the graph of possible label transitions is independent of phase and physical history.

If the same nonhalt label were reached at two different phases, a possible path from its later occurrence to a halt label would also have positive probability from the earlier occurrence, causing premature stopping. Thus the positive-probability phase supports are disjoint and

```text
1 + sum_(t=1)^n m_t <= M.
```

This proof does not require equal report probabilities; common null sets are enough. The physical experiment continues producing reports until the machine halts, so no free end marker is being used.

For the lower, the last phase has at most `M-n` labels. Applying the all-row quantization lower at that phase gives

```text
R_aut(n,M)-B_n >= c(M-n)^(-2/d).
```

For the upper, geometrically allocate the extra labels toward the later phases according to the continuation decay. Both stability alternatives then give the same order. The minimal legal budget is `M=n+1`; at that budget the excess is merely bounded by a constant, consistent with `(M-n)^(-2/d)=1`.

The argument is correct under the common-support and exact-halt interface. A visible phase-dependent support pattern would itself provide clock information and is correctly excluded from the lower.

---

## 10. Gaussian hidden-state realization

The classical realization has a finite hidden state, nondegenerate Gaussian reports conditioned on the pre-transition hidden state, and an entrywise-positive invertible transition `P` after the report. The prediction domain is `K=P Delta`, so every coordinate has a uniform positive floor.

The normalized Bayes multiplication by the Gaussian likelihood is an isometry in Hilbert's projective metric. The positive transition contracts this metric. The manuscript's elementary proof observes that the row weights for `P` share a common subprobability component of mass at least the entrywise lower bound. This yields a strict contraction for every positive transition, even when a cruder total-variation sufficient condition is unavailable.

The actual acquisition dimension is derived from log odds. Under each actual incoming belief, the log-odds vector is a finite mixture of nonsingular Gaussian distributions with uniformly controlled means and covariance. The inverse logistic Jacobian grows only exponentially, while the Gaussian density decays quadratically. Hence the posterior density is uniformly bounded on the simplex, including near its boundary. Invertibility of `P` preserves full dimension on `K`.

Global covers, report continuity, common support, and a Borel nearest-cell rule follow. I did not find a fatal gap in this verification.

The theorem is mathematically natural, but its external consequence remains a passive known-kernel one-step forecast. It would become considerably more compelling if tied to a standard filtering or zero-delay coding problem for which the fixed-total-state optimum was previously unknown.

---

## 11. State-dependent quantum realization

The quantum report instrument is

```text
I_H(rho)=T(K_H rho K_H) mu(dH),
K_H=(I+eta H)^(1/2),
T(sigma)=lambda U sigma U* +(1-lambda)tr(sigma)I/D.
```

Its report likelihood

```text
ell(H,rho)=1+eta tr(H rho)
```

really depends on the incoming state. The effects generally do not commute.

The positivity-improving channel confines predictions to an interior compact density-operator body. Positive congruence and normalization preserve Hilbert's cone metric. The channel `T` strictly contracts that metric for every `0<lambda<1`; the explicit estimate is uniform on compact parameter subintervals.

The acquired-density argument uses a smooth inverse for normalized positive congruence. On the compact effect body and interior state body the inverse and its derivative are uniformly bounded, and the Jacobian stays nonzero. The final channel is an invertible affine map on the trace-one hyperplane. The report density is bounded above and below. Thus each row law has a bounded full-dimensional density in dimension `D^2-1`.

The terminal audit randomly selects one bounded Hermitian coordinate after commitment. It separates the density operators without supplying a joint measurement of incompatible observables. The observer is classical and has no quantum memory.

The bounded-gap corollary permits unitary noncontracting phases, provided a uniformly improving channel appears in every fixed-length block. The spectral floor and product contraction are then uniform. This is a legitimate improvement over a per-step contraction theorem.

I find this realization correct on its declared finite-dimensional, strictly positive class.

---

## 12. Rank-changing acquired strata

The singular instrument first applies a positivity-improving channel and then chooses, with a visible branch mark, between:

- a weak full-rank effect branch of dimension `D^2-1`; and
- a rank-one projective branch of dimension `2(D-1)`.

The branch weights are exactly `omega` and `1-omega`; they are not normalized away after conditioning on survival. The pure branch has constant centered squared norm, so its integrated potential is affine and contributes no curvature. The weak branch has the displayed curvature coefficient. Under the stated strict inequality, the combined curvature is summable.

The weighted profile

```text
Xi_w(m)=sum_j w_j m^(-2/d_j)
```

is lower-bounded by applying the component small-ball bounds to every global codebook and upper-bounded by allocating centers among the finitely many visible components. The representative after pooling may lie in the full convex density body; this is compatible with the common-cell proof.

The result correctly retains both the true acquired mass and the true physical baseline. It is a substantive singular verification, although it is still a designed finite-dimensional instrument rather than a general rank-changing quantum filtering theorem.

---

## 13. Same-task composition and finite precision

The simulator proposition compares the complete stopped transcript, observer randomness, committed response, and protected audit. It multiplies simulator and observer state counts and composes physical call maps. It does not infer a reverse minimax inequality from a one-way simulator.

The finite-precision proposition uses a first-mismatch coupling. A label error can occur only if primitive coupling fails, arithmetic fails, or the ideal pre-quantization value lies near a cell boundary. The relevant boundary mass is unconditional under the ideal actual row law. This avoids the false claim that a discrete numerical report is close in total variation to a continuous raw report.

The manuscript now separates hard labels from:

- program constants;
- read-only codebook storage;
- report precision;
- arithmetic workspace;
- primitive evaluation cost;
- numerical integration for calibrated centroids; and
- physical time.

There is still no matching lower frontier for these computational resources, and the text correctly says so.

---

## 14. Retained-bit calibration and deficiency law

The joint experiment contains:

1. one paid bit-report call for an independent fair bit `U`, erased with probability `a`;
2. exactly `n` passive core filter calls;
3. one terminal protected audit of the core target, `U`, and an invisible calibration sign.

The source-to-exact-bit target deficiency is exactly `a/2`. A stateless simulator guesses fairly on an erasure, while the protected terminal bit audit supplies the matching lower.

For a checkpoint, the core quantization lower, the independent bit loss, and the calibration loss add under a common product prior. The upper uses two copies of a core code and the optimal linear bit response. This gives the stated order.

For an autonomous observer, the initial bit-action label cannot be reused at a core phase because the action row is fixed. The post-bit phases satisfy the common-support clock condition.

If any post-bit phase has only one reachable label, the independent bit is lost and cannot be recovered from the passive core. Otherwise each of the `n` preterminal post-bit phases needs at least two labels to retain the bit lanes, leaving at most

```text
M-2n-1
```

terminal labels for the core. This gives the lower in terms of

```text
Q(n,M)=max(1,M-2n-1).
```

The upper explicitly duplicates the core phase labels in the two bit lanes and charges the initial state. I find the dichotomy and count coherent under the declared passive-core and fixed-action-word interface.

This theorem is an attained same-task law. It is not a general statement that arbitrary calibration or simulator tolerances create necessary losses.

---

## 15. Novelty and literature position

The manuscript substantially improves its literature discussion. It now compares sequential vector quantization, finite-state vector quantization, recursive marginal quantization, nonanticipative rate-distortion, projective filter stability, finite-memory POMDP approximation, and zero-delay coding.

Three additional clusters should be incorporated before journal submission.

### 15.1 Value-directed belief compression

Poupart and Boutilier's value-directed belief-state approximation and compression work explicitly studies how a compressed posterior affects future task value rather than generic belief-space distance. The present finite test quotient and task-induced Euclidean loss are different, and the R32 theorem gives an all-hard-state converse absent from those approximation algorithms. Nevertheless, the conceptual proximity is direct. The introduction should explain why the affine test carrier and row/pooling identity are not simply a squared-loss special case of value-directed belief compression.

Relevant references include:

- P. Poupart and C. Boutilier, *Value-Directed Belief State Approximation for POMDPs*, UAI 2000;
- P. Poupart and C. Boutilier, *Vector-Space Analysis of Belief-State Approximation for POMDPs*, UAI 2001;
- P. Poupart and C. Boutilier, *Value-Directed Compression of POMDPs*, NeurIPS 2002.

### 15.2 Bayes-risk and Bregman quantization

The connection between Bayes-risk error and Bregman divergence has been used in prior-probability quantization and decision problems. R32's perspective potential and conditional Jensen defect are experiment-level and dynamically pooled, so the theorem is not subsumed by static prior quantization. Still, citing this line would sharpen the novelty claim around the exact Bayesian defect.

A relevant reference is K. R. Varshney, *Bayes risk error is a Bregman divergence*, IEEE Transactions on Signal Processing 59 (2011), 4470--4472.

### 15.3 Current finite-memory belief approximation

Recent work by Mintae Kim studies policy-conditional finite-memory belief approximation using Wasserstein mismatch, and a 2026 preprint on finite partition-based observations develops normalized class-restricted filters and finite-dimensional approximations. These works have different memory objects and control conclusions, but they are closer to R32's state-dependent normalized filtering direction than the current bibliography indicates.

The comparison should distinguish:

- hard total label budget versus history-window length or partition complexity;
- all-observer minimax lower versus fixed-policy approximation bounds;
- passive prescribed protocol versus adaptive control;
- terminal squared predictive task versus discounted value; and
- actual row small-ball geometry versus approximation of the full belief measure.

I did not locate a published theorem that combines R32's exact Jensen/row/pooling decomposition, all-Borel hard-state converse, common-support internal halt charge, and matching total-label law. This limited search observation is not a priority certificate.

---

## 16. Why the top-four recommendation remains negative

### 16.1 The exact identity is elegant but built from established structures

The central formula is a well-executed combination of:

- conditional projection;
- convex perspectives;
- Bregman/Jensen defects;
- finite-center quantization; and
- a second projection measuring pooled centroids.

The new point is its causal and instrument-level arrangement, not a new general principle of convex analysis or Bayesian decision geometry. For a top-four general mathematics journal, the paper must show that this arrangement resolves a broad obstruction beyond the displayed class.

### 16.2 The matching theorem is strongly conditional

The sharp law requires uniform row geometry and a global cover on the full declared domain, plus a summable stability certificate. These are not shown to be necessary, nearly necessary, or automatically generated by the experiment. The difficult nonsummable state-dependent case remains open; the exact Haar result in the companion shows that it can have a very different law.

### 16.3 The protocol is passive and known

The theorem optimizes the observer for a fixed preparation and fixed report sequence. It does not optimize sensing, actions, or stopping, and it does not learn an unknown transition or likelihood. Thus it does not yet connect to the hardest parts of POMDP control or adaptive information acquisition.

### 16.4 The natural examples do not yet solve an established problem

The Gaussian and quantum verifications are stronger and more natural than the earlier purpose-built examples. However, the paper does not identify a standard model whose fixed-total-state optimum was previously unknown and is now determined by the theorem. A concrete external application would materially change the assessment.

### 16.5 The title still overstates the completed class

The paper now gives a genuine theorem-and-proof article rather than a framework. Nevertheless, “General Theta Foundations I” suggests a breadth beyond finite affine predictive test closures with certified stable posterior transport. The authors may retain the mother-problem title, but the abstract and introduction should continue to foreground the precise theorem class and avoid universal language.

---

## 17. Major comments required for revision

### 17.1 State the theorem class in the first sentence of the abstract

The current abstract is accurate but dense. It should say immediately that the theorem concerns a **known finite-horizon passive experiment with a finite executable affine test closure**. This prevents readers from interpreting the result as a general finite-memory filtering or control theorem.

### 17.2 Separate the exact identity from the sharp resource theorem visually

The identity requires no stability or geometry. The matching law requires small-ball mass, covers, report continuity, common support, and (C) or (P). A two-part theorem or a displayed assumption hierarchy would make this distinction unmistakable.

### 17.3 Emphasize the strength of the uniform row small-ball condition

The condition is over every barycenter in the declared domain, not only the actual full-history law. Explain why this is the correct quantifier for the all-observer lower and identify settings in which it fails despite a full-dimensional terminal law.

### 17.4 Clarify local versus global compatibility

The one-step equality condition is necessary and sufficient locally. It is not a global recursive-compressibility criterion. State this immediately after the theorem and include a small counterexample in the article, not only in the ledger.

### 17.5 Add value-directed belief compression to the theorem-level comparison

The relation to Poupart--Boutilier is too close to omit. Compare the task metric, information object, hard-state budget, and form of guarantee explicitly.

### 17.6 Add Bayes-risk/Bregman quantization context

The current citation to proper scoring rules is useful but too broad. Cite the prior-quantization/Bayes-risk line and isolate the genuinely dynamic row/pooling contribution.

### 17.7 Compare with current finite-memory belief approximation

Add the 2026 policy-conditional Wasserstein work and distinguish its window-memory and value-comparison statements from the hard-state terminal converse here. Current literature should not be left only in an auxiliary audit.

### 17.8 Give a failure example for each stability route

Provide one positive instrument for which (C) fails but (P) holds, and one for which (P) fails but (C) holds. The rank-changing example partly serves the latter role, but the contrast should be explicit and quantitative.

### 17.9 Explain the autonomous budget in operational terms

The quantity `M-n` is the terminal width remaining after one state is paid for each prior phase, not an effective number of bits or an average per-phase width. Include a one-line phase table in the main text.

### 17.10 Turn the Gaussian theorem into a recognizable benchmark

Work out a two- or three-state numerical model end to end: explicit constants, actual code construction, and comparison with an unrestricted checkpoint. This would make the theorem more than an asymptotic existence result.

### 17.11 Strengthen the quantum positioning

State clearly whether the physical instrument has an intended measurement interpretation beyond being a convenient positive map. The theorem is mathematically valid, but a natural quantum filtering or reference-frame consequence would greatly improve impact.

### 17.12 Keep the companion hierarchy editorially separate

The native 23-page article is readable by itself and should remain so. Do not require the editor to treat 353 companion pages as part of the submitted paper. Companion F and G are valuable technical records but should be cited as independent preprints or appendices, not bundled as hidden premises.

---

## 18. Technical comments

1. In the perspective-Hessian display, write the numerator as `A v-c(v)F` to avoid the ambiguous `F(c v)` notation.
2. State once that `c_t(y)` is a row linear functional and `c_t(y)v` is scalar.
3. In the quotient lemma, distinguish the Borel realization of the attained image from the larger compact convex domain used for certificates.
4. Say explicitly whether all affine identities are required pointwise on the compact domain or only reference-almost everywhere in the report coordinate; the current formulation appears to require the latter uniformly in `u`.
5. For zero likelihood, record in the theorem statement that positivity and bounded tests force `U=0` on the relevant state.
6. The common-support autonomous theorem should state that equivalence holds at every possible finite history generated by every legal program, not merely along the exact posterior process.
7. In the clock proof, “some finite path” should be understood as a label path with each edge having positive reference-measure support. The proof does this; the statement can say it once.
8. The final-row lower uses at most `M-n` labels. Note explicitly that repeated readouts only reduce the number of distinct codepoints.
9. In the curvature allocation, identify the constant dependence as `rho` approaches one. Uniformity in horizon does not mean uniformity at loss of stability.
10. In the pathwise upper, remind the reader that the final response is the stored codepoint or its legal task map, not an independently retained real vector.
11. The Gaussian transition convention is report first, transition second. Keep this visible in the theorem statement because the interior domain depends on it.
12. The Gaussian log-odds density proof should explicitly name the determinant lower bound of the affine likelihood-rank matrix among the uniform parameter constants.
13. In the Hilbert contraction proof, the common subprobability component has mass at least the entrywise lower bound `alpha`; dimensions constrain the admissible range of `alpha`.
14. The quantum audit basis is Hilbert--Schmidt orthonormal. State that every basis element has operator norm at most one because Hilbert--Schmidt norm is one.
15. The congruence lemma's domain is the trace-`D` positive cone. Note that the effect ball `I+eta H` indeed lies in that hyperplane because `H` is traceless.
16. In the cone contraction, list the dependence of `H_0` and the contraction factor on `lambda` and `D`; this is important near `lambda=1`.
17. The bounded-gap corollary requires a phasewise interior domain before the first improving step. The proof supplies it through the prepared state; repeat this in the statement.
18. In the singular theorem, the phrase “actual predictive law has masses exactly” refers to the current branch mark at each phase, not persistence of an earlier rank branch. Clarify this.
19. For the projective small-ball formula, specify that centers outside the orbit are handled by choosing an orbit point in a nonempty intersecting ball and enlarging the radius.
20. In the weighted profile upper, equal allocation among components is sufficient because constants may depend on fixed weights. State that no optimal allocation claim is made.
21. In the simulator proposition, the target observer's fresh randomization is part of the complete joint law; this is correctly stated in the proof ledger and should remain in the proposition prose.
22. In the precision theorem, `omega_t(h_t)` is an unconditional row-bound summed over incoming labels; avoid language suggesting conditioning on the event of no prior mismatch.
23. The Gaussian numerical implementation treats the tail as a charged failure event. Do not describe truncation as a new physical report cell unless the experiment actually reports it.
24. In the joint theorem, explain why the core is independent of `U` not only marginally but conditional on all reports and actions allowed by the fixed passive protocol.
25. The bit squared loss on complete forgetting is one for a fair `±1` bit. Record the allowed bit response interval.
26. The checkpoint upper's response `(1-a)b` has risk `2a-a^2`; since `epsilon=a/2`, the displayed asymptotic constants absorb the factor four. A line noting this conversion would help.
27. In the autonomous upper, show the algebra comparing `M_0-n` and `Q(n,M)` for the smallest nontrivial budgets.
28. The loss normalization in composition should remain explicit when the audit vector norm depends on physical dimension.
29. Replace phrases such as “all-program” by “all legal Borel finite-state observers of the fixed protocol” when there is any risk of being read as an adaptive-control quantifier.
30. The bibliography should include publication years and DOI/arXiv identifiers consistently for newly added belief-compression and Bayes-risk references.
31. Keep build/test counts out of the mathematical introduction; the current native article does this correctly.
32. The final source lineage should continue to distinguish original R27, corrected Companion F, reviewed R29, and native R32.

---

## 19. Routes that could materially change the top-four assessment

A future revision would have a substantially stronger general-journal case if it achieved one or more of the following.

1. **An intrinsic recursive-compressibility theorem.** Replace the supplied global cover/stability certificates by a near-necessary criterion derived from the raw experiment and task.
2. **A nonsummable informative-likelihood converse.** Obtain a matching weighted lower and upper when posterior sensitivity does not decay, extending the exact relative-Haar phenomenon to genuinely informative reports.
3. **Unknown-kernel learning with finite memory.** Prove a joint learning/memory law under one fixed action, calibration, and evaluation interface.
4. **A recognized natural application.** Determine a previously unknown optimal finite-state curve in a standard filtering, zero-delay coding, relative sensing, or quantum measurement problem.
5. **A computational lower frontier.** Jointly lower-bound persistent states, program description, numerical precision, workspace, and execution time for a common task.
6. **A broad nondominated or changing-support theory.** Extend the all-observer identity and matching law beyond common positive report support without inserting phase information or conditioning away singular mass.

These are demanding directions, but they identify the gap between a strong specialist theorem and a top-four foundational result.

---

## 20. Final recommendation

R32 is mathematically serious, substantially improved, and technically more natural than its predecessors. It gives a correct likelihood-aware causal loss identity, an all-finite-state converse, two implementable matching routes, and credible Gaussian and quantum verifications. I found no elementary fatal defect in the central proofs reviewed.

The manuscript nevertheless remains too conditional and too limited in external consequence for a top-four general mathematics journal. Its sharp law is a theorem for a known passive finite affine filtering class with strong geometry and stability certificates; it is not yet an intrinsic classification or a solution of a recognized difficult problem.

Accordingly my recommendation is:

- **top-four general mathematics journal:** reject in the present form;
- **strong specialist journal:** favorable after major revision, particularly after broadening the belief-compression literature comparison, clarifying the exact assumption hierarchy, and adding a recognizable end-to-end application.

The rejection recommendation should not be read as a finding that the main theorem is false. It is a judgment about breadth and significance at the stated journal level.