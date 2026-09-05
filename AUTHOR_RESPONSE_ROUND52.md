# Response to Round 52 — Round 53 revision

**Manuscript:** *Boundary Identification from Recurring Fast Probes: Energy-Robust Posteriors and Bound Observable Certificates*  
**Author:** Qian Qi  
**Date:** 5 September 2026  
**Revision branch:** `revision/round53-bound-certificates-energy-robust-posterior-2026-09-05`  
**Controlling review:** `REFEREE_REPORT_ROUND52_GPT6_ASTRA_PRO_HARSH.md`  
**Frozen review HEAD / parent:** `8e3e6f663fde9942384298eb9c60cf217a926bac`  
**Reviewed Round 51 manuscript HEAD:** `f991a17a5d99bf0cce9f1e457df91097e69dcd8a`

## Central response

We retain logarithmic physical recovery depth, the complete working posterior, bounded nonreset forcing, tail-uniform physical inversion and the all-policy comparison in readout count. We do not replace those results with a weaker target or an impossibility assertion. The new article strengthens the exploration hypothesis, the actual-clock remainder, and, substantially, the posterior's discrepancy class. It repairs the executable observation contract rather than relabeling a scalar arithmetic test as an end-to-end certificate.

The active article is `ROUND53_REVISION.tex`. It is a complete proof sequence with two explicitly declared, unchanged source inputs: `round51/model_inverse.tex` and `round51/likelihood.tex`. Historical roots, derivations, reports and programs are preserved by branching from the controlling review. The argument does not treat prior upload receipts as proof premises.

## R52-C1 — close the observation-map contract

**Article:** Section 8, Theorem `thm:outer`, equations `eq:bound-grid` and `eq:diameter-contract`.  
**Implementation:** `tools/round53_certificates.py`, `CertificateSpec`, `validate_certificate`, `canonical_observable`, `validate_grid`, `certify_outer`.  
**Tests:** `tests/test_round53.py`.

The referee's three witnesses are valid defects of unrestricted composition of the old interface. They do not refute the analytic theorem with its sampled-grid premise. We reproduce all three against the unchanged, blob-verified old module: zero observable, extremely early nonzero step observation, and 61 identical nonzero observations. The old predicate returns true while the retained prefix has diameter 1 rather than the requested 1/8. We also test 42 identical observations, matching the new clock certificate's lag count.

The active certifying entry point now receives the model/depth and a bound immutable specification. It recomputes every certificate field, canonicalizes all observable coefficients and rational times, verifies every required pulse lag exactly once, and orders observations together with their bands. Equal-time terms are combined, canceled terms removed, and arbitrary terms at time zero are omitted using the known identity `h(0)=0`. Missing/extra/duplicated lags, wrong pulse scale/sign/clock, substituted model or depth, altered derived certificate values, floats and invalid representations cannot obtain a successful certificate through this entry point.

The wrapper internally executes exhaustive outer enumeration. It never accepts a caller's alleged outer-radii list or outer-set result. The immutable output binds the model certificate, ordered grid and bands, full witnesses, prefix projections, all five budgets and enumeration counts. Its statuses distinguish `enclosed`, `certified`, and `empty`; an empty result is not declared parameter recovery. Resource limits raise rather than producing a certified partial union.

The old predicate remains only in preserved historical source. The current arithmetic helper is named `radius_budget_satisfied` and explicitly does not certify observation identity. Statistical confidence is still conditional on the coverage of the supplied statistical bands; arithmetic cannot manufacture that coverage. The contract concerns actual outputs of the unmodified entry point, not authenticity of arbitrary user-constructed Python objects.

A positive test runs the complete grid through a nonempty, genuinely passing end-to-end enclosure. It deliberately uses a very narrow rational model box to keep exhaustive enumeration finite and small. This demonstrates the positive interface path, not practical feasibility for a wide high-depth box. Wide-box complete-grid tests correctly return `enclosed`, not `certified`.

## R52-Q1 — atomless exploration included in the principal theorem

**Article:** Theorem `thm:main`; Lemma `lem:block-floor`.  
**Code:** `success_probability`, `CertificateSpec`.

The hypothesis is now recurring fast duration with `p=1-rho+rho*w>0`, where `w=chi({t0})` may be zero. For `rho<1`, an arbitrary exploration law, including an atomless one, is admissible. The successful block probability is `p^m`; in the atomless case it is `(1-rho)^m`. All-sign block energy and the complete likelihood are unchanged. We also include `rho=0`. For `rho=1,w=0`, this particular certificate has no positive fast-event floor; we make no universal impossibility inference.

## R52-Q2 — actual clock norm used in proofs, rates and code

**Article:** Lemma `lem:sampled`, Proposition `prop:envelope`, equations `eq:tau`–`eq:clock-constants`.

With `x=Delta*Lambda<=1/64`, set `tau=2*x/(1-x)<=2/63`. The analytic correction remains exactly the same integrated-pulse transform, but its pairwise remainder becomes

`E = Delta^(-R) tau^N`.

The proof bounds the omitted pair-tail by this quantity using `12*Delta*tau/(1-tau)<=1`. It chooses the least integer `N>=R` with `L*E<=delta/2` in exact rational arithmetic. With `ell_tau=log(1/tau)`, the sufficient accuracy exponent is

`p_tau = 2 + (log(1/p)+log(16))/ell_tau`.

The depth constant includes all ceiling, inverse-amplification and entire-block probability costs; it is displayed once in the article. For the exact example used by the referee, the old order 60 becomes 41, with `tau=18/1015`. The actual code checks the minimality and remainder inequality. Smaller clocks can improve the accuracy exponent but can worsen the depth constant; no sharp joint frontier is claimed.

## R52-M1 — correct the comparator at the theorem level

**Article:** Section 7.1 (`sec:comparison`), Theorem `thm:transfer`, Proposition `prop:finite-section`.  
**Audit:** `round53/LITERATURE_AUDIT.md`.

We accept the distinction the report requires. Sarkar–Rakhlin–Dahleh's Assumption 1 and Section 11 permit sub-Gaussian excitation. Their Gaussian pseudocode cannot justify a theoretical bounded-input exclusion. Scalar Rademacher inputs satisfy the appropriate condition.

The revised comparison explicitly derives the regular-duration sampled recurrence with transition `U=exp(Delta*A)` and input operator `a*H*B`, and uses the dimension-uniform cut-chain stability and response norm. In the relevant proof decomposition, zero process noise removes its upper-bound terms; the input-Gram excitation remains. This is not a false assertion that zero covariance satisfies their normalized noise assumption. A nonzero initial condition contributes a stable transient and must be charged separately.

We do not transplant a whole comparator theorem without its hypotheses. We identify what is directly reusable at the finite-response interface and what still needs argument: irregular durations, block feedback, quantitative labeled physical inversion and the complete posterior. Our own compatible front end remains proved. The improved posterior statement does not arise from a frequentist FIR bound alone.

The literature audit also records a 2026 primary abstract on misspecified nonlinear inverse posteriors to avoid presenting robustness in general as an unexplored subject. No complete priority search or full theorem-level audit of that additional paper is claimed.

## R52-M2 — strengthen the mathematical statement, not the acceptance rhetoric

**Article:** Theorems `thm:energy` and `thm:main-drift`; Corollary `cor:polynomial-drift`.

The report correctly distinguished summably transient initial-state uncertainty from wider misspecification. We now prove a chronological transfer principle for

`Y_i = m_i(beta0) + d_i + xi_i`,

where `d_i` is predictable before fresh Gaussian noise and `sum d_i^2<=D` pathwise. The working likelihood still integrates any bounded initial-state law. The result needs no sum of absolute values of the *true* discrepancy and permits sign-correlated predictable error within the stated energy budget.

For a separated set with conditional grouped information `V_n>=nq`, the new finite inequality is

`Pi_n(F) <= exp{ P(sqrt(q)/4) - 27*nq/(256*sigma^2) + 8*D/sigma^2 + 2*B_(n,D) }`,

where

`B_(n,D) = sigma^(-2) [2 sum r_i |xi_i| + 2 sqrt(R2 D) + 2 M R1 + R2]`.

The article proves the nuisance-integral bound uniformly before integration, the predictable score event, the Young-inequality loss, and the denominator bound on a deterministic prior ball. In particular, `D<=nq/1024` and `B_(n,D)<=nq/(64*sigma^2)` retain the posterior exponent `-nq/(16*sigma^2)`. Every constant is traced; the finite arithmetic tests supplement rather than replace this proof.

For the physical experiment, write `gamma=C_tau*r+p_tau*s<1`. Then `nq` has a uniform lower bound of order `n^(1-gamma)/log(n)`, so `D_n=o(n^(1-gamma)/log(n))` retains logarithmic physical depth. Errors bounded by `C*i^(-alpha)` allow every `gamma<min(1,2*alpha)`. For `alpha<=1/2`, their energy envelope need not be summable over an infinite horizon. This is a genuine extension beyond exponentially dying initial-state error, with a precise tolerance rather than a claim of arbitrary misspecification robustness.

The theorem's contrast-family formulation isolates the statistical statement from Jacobi inversion. Its physical corollary retains the nonlinear labeled target and between-block feedback. The separate cross-correlation estimator is **not** asserted unbiased under arbitrary additional sign-correlated discrepancy; only the posterior and its medians receive this extension.

This stronger theorem answers the mathematical direction of the significance objection. Whether the result meets an exceptional-journal threshold remains an independent editorial judgment. Neither finite tests nor the response asserts acceptance, a sharp joint minimax frontier, or absence of relevant prior results.

## Scope — elapsed time, feedback and retained historical work

**Article:** Corollary `cor:time`.

The broad all-policy KL bound is explicitly in readout count. Its elapsed-time consequence now restricts comparison policies to a positive lower bound on interreadout gaps, hence a deterministic count cap. The attaining experiment has stage lengths between `t0` and `t0+T`, so its time-order conclusion is retained. Unlimited readout frequency is not included in an elapsed-time minimax claim.

The fast chosen clock, pinned positive coefficient box, positive edge lower bound and within-block precommitment remain explicit. Earlier stagewise-feedback and homogeneous results are preserved in the historical roots; they are not silently replaced or asserted proved again in this article.

## Actual reproducibility and requested re-review

Run `python tools/verify_round53.py --pdf`. The verifier checks the committed manifest without regenerating it, traverses the actual TeX input closure, runs the unchanged 66-test Round 51 suite and the new 44-test Round 53 suite, and requires three successful TeX passes with no unresolved references or overfull boxes. The new suite reproduces the old defects and rejects their current unsafe compositions; a successful old suite alone would not demonstrate this repair.

The local execution recorded in `artifacts/round53/VERIFICATION.json` contains **110 tests, zero failures and zero errors** and a three-pass article build. These are finite executions and source/build checks, not a proof-assistant verification, independent journal review or posterior simulation. The manifest identifies the exact executable sources and the two inherited mathematical inputs. The article is 14 pages in the recorded build.

We request scrutiny of the bound observable contract, the squared-energy posterior theorem and its polynomial-drift corollary, the revised input comparison, the recurring-probe hypothesis, and the actual-clock constants. The positive logarithmic-depth conclusion is retained and strengthened.
