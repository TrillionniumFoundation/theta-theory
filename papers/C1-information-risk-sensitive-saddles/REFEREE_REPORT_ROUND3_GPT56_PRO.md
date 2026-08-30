# Round-Three Referee Report — GPT-5.6 Pro

**Manuscript:** C1 — *Typed Control, Information, and Saddle Envelopes for Kinetic Cotangent Phases*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round3-full-positive-closure-11paper-2026-08-30@6a31720e5b0b6ab156b575f947596f9b66f56efe`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `303c6d140376e9776fba29dccd66ae9879828eae`

## Executive assessment

This revision makes a real modeling correction: it separates one-time preparation, reward-only feedback, and adaptive changes of canonical path law into three distinct games. It also distinguishes smooth saddle manifolds from finite action envelopes and retains deterministic continuation under complete microscopic observation.

The adaptive game is still invalid. The finite-volume likelihood ratio is written in the compensator form appropriate to a point process with predictable intensity, but the microscopic hard-sphere contact process is deterministic conditional on the initial state. `A_{pi^epsilon}` is not its finite-volume compensator, and the displayed exponential is not an exact mean-one density. The repository’s own hostile audit identified this exact error and wrote a block-normalized replacement under `revision/round3-rereview/`; that replacement is not included in the controlling paper.

The posterior-contraction theorem also gives the wrong generic exponent. Expected posterior error is controlled by testing/Chernoff information, not generally by the Kullback–Leibler/path-relative-entropy rate governing almost-sure log odds. The proof confuses typical posterior odds with their expectation.

After removing those two claims, the remaining one-time envelope, reward-only Isaacs equation, and Schur-complement calculation are useful organizational facts but do not form an independent top-four-journal theorem.

## Improvements relative to the preceding circulation

1. The one-time preparation game correctly retains the same action pair through every time block.
2. The paper explicitly states that reoptimizing at an intermediate time defines a different game.
3. Reward-only control changes the running cost but not the kinetic transition law.
4. Finite action sets are treated as nonsmooth active-branch envelopes, not through a fictitious smooth Hessian.
5. The smooth optimizer-response Hessian is stated with an explicit signed-curvature condition.
6. Complete observation is handled as deterministic reduction rather than by inventing filtering noise.

These corrections should be retained.

## Major mathematical objections

### 1. The finite-volume adaptive likelihood is not a likelihood ratio

The active paper defines

\[
Z_T
=
\exp\left\{
\sum_c\log q(c)
-
\mu_\epsilon\int(q-1)dA_{\pi^\epsilon}
\right\}.
\]

This is the stochastic exponential for a point process whose predictable compensator is `mu_epsilon A_{pi^epsilon}`. The microscopic hard-sphere contacts do not have such a compensator. Conditional on the initial hard-sphere state, every future contact time and mark is deterministic. In general,

\[
E[Z_T]\ne1,
\]

and the product over contacts is not normalized by the displayed integral.

The limiting Boltzmann collision intensity can appear in a large-deviation Hamiltonian; it is not an exact finite-particle stochastic intensity. Confusing these levels changes the microscopic game.

### 2. The internal block-normalized repair was not materialized

The repository’s hostile audit correctly replaces the false compensator by the exact conditional block normalizer

\[
K_{\epsilon,j}(\psi)
=
\mu_\epsilon^{-1}
\log E\left[
 e^{\mu_\epsilon\langle\psi,
 \Gamma_{(t_j,t_{j+1}]}^\epsilon\rangle}
 \mid\mathcal F_{t_j}
\right].
\]

That construction appears in

```text
revision/round3-rereview/C1_BLOCK_NORMALIZED_CONTROL.tex
```

but `papers/C1-information-risk-sensitive-saddles/main.tex` inputs only `ROUND3_POSITIVE_CLOSURE.tex`, which still contains the false Poisson-compensator formula. The paper’s principal adaptive theorem therefore reviews and proves the wrong finite-volume model.

Even the separate repair would require a uniform conditional B2 pressure theorem over all feedback histories and strategies; this is not proved elsewhere in the series.

### 3. The adaptive Isaacs limit has no established microscopic dynamic programming principle

Because the displayed density is not normalized, there is no finite-volume controlled probability law and hence no valid discrete dynamic programming recursion. The subsequent claims—uniform cluster estimates over strategies, half-relaxed limits, and convergence to

\[
\partial_tU+\sup_u\inf_v\mathbb H^{u,v}(f,DU)=0
\]

have no starting point.

For the corrected block-normalized model, one must prove that conditional log-partitions converge uniformly as functions of the complete hierarchy/history state, establish stability under nonanticipative strategies, and identify the vanishing-mesh Hamiltonian. Unconditional source convergence from B2 is insufficient.

### 4. The expected posterior exponent is generally not relative entropy

The paper claims

\[
\limsup_{\epsilon\to0}
\mu_\epsilon^{-1}\log E_{z_0}\rho_T(O^c)
\le
-\inf_{z\notin O}\mathcal K_T(z_0\Vert z),
\]

where `K` is the path-pressure relative-entropy rate.

Under the true law, the log posterior odds against a fixed alternative can indeed have typical rate `-D(P_{z_0}||P_z)`. The expectation of posterior error, however, is dominated by rare likelihood-ratio events and is governed generically by a hypothesis-testing or Chernoff exponent. Even for two iid simple hypotheses,

\[
E_{P_0}\frac{aL_n}{1+aL_n}
\]

need not decay at the Kullback–Leibler rate; its optimal exponential order is tied to the overlap of the two laws.

The proof’s instruction to “integrate the posterior odds” illegitimately interchanges a typical log-likelihood limit with expectation. The displayed bound is therefore false without much stronger uniform moment assumptions and usually remains too strong even then.

### 5. A pressure Hessian alone does not give local asymptotic normality of the posterior

The statement that the Laplace-scaled posterior has a Gaussian tangent with information matrix equal to the B3 Hessian requires a LAN expansion of the full likelihood process, including a score central limit theorem and uniform quadratic remainder in the phase parameter. A fluctuation CLT for selected observables is not enough. No LAN theorem is stated or proved.

### 6. Uniform phase regularity is inherited rather than established

The first lemma invokes B2 complex normal convergence and B4 semigroup convergence to obtain two phase derivatives. B2 does not prove global source continuation, B4’s containment/comparison framework is invalid, and no topology on the phase-dependent semigroups is specified. Thus the smooth saddle theorem has no verified model input.

### 7. The reward-only Isaacs theorem is mostly formal

At a fixed transition law, optimizing a bounded running reward is standard. The manuscript still needs measurable-selection and comparison hypotheses for the infinite-dimensional state. Those are delegated to B4, whose comparison theorem is not proved. Even after repair, this result is not an independent top-four contribution.

### 8. Complete-history posterior sufficiency remains the exact general state

For a finite phase family, the posterior weights are finite dimensional only if the observation likelihood can be updated from those weights and the current observation state. The paper states an “exact finite-dimensional filter” without specifying the observation kernel or the state variable needed to evaluate future likelihoods. The phase-weight vector alone need not be dynamically sufficient for path-dependent observations.

### 9. The controlling manuscript is not standalone

The active source is a preamble and one closure module. It does not define the B4 phase semigroups, B2 controlled source laws, observation model, strategy filtration, or path-relative entropy at the level required for a submission.

## Editorial recommendation

**Reject.** The separation of the three games is a genuine improvement, but the only genuinely new game is built from a false finite-volume likelihood, and the filtering theorem uses the wrong expected-error exponent. A viable reconstruction should incorporate an exact block-normalized canonical control law, prove conditional source convergence uniformly over feedback histories, derive the Isaacs limit from that model, and replace the posterior statement by a correctly formulated testing/LAN theorem. The one-time and reward-only results can then serve as supporting propositions rather than a standalone top-journal paper.