# Response to the Round 50 referee report — Round 51

**Manuscript:** *Single-Atom Boundary Identification with Retained State and Logarithmic Physical Depth*  
**Author:** Qian Qi  
**Date:** 5 September 2026  
**Revision branch:** `revision/round51-single-atom-response-transfer-2026-09-05`  
**Controlling report:** `REFEREE_REPORT_ROUND50_GPT6_PRO_HARSH.md` at `a7b9ffcfd79d2f8cd5179238db9124486c1d9f0a`  
**Previously reviewed distribution:** `abae39b7efeec5f6995f85fcbe1cc1d10e27fba6`

## Central response

We retain and strengthen the positive mathematical conclusion surviving the report: bounded individual probes, retained state, a chosen fast clock and committed blocks give logarithmic recovery depth for labeled infinite Jacobi coefficients, using the complete working posterior and deterministically linear elapsed time. No weaker depth target is substituted. The all-policy upper bound on information remains in the article, establishing the matching fixed-accuracy depth order.

The revision does not answer a contribution objection by declaring acceptance. It supplies a broader theorem, stronger explicit certificates, a response-to-physical reduction, a compatible finite-response estimator, and a dimension-uniform truncation calculation. The analytic proofs are in the article; finite regression checks are supplementary evidence, not formal proof certification.

## R50-Q1 — enlarged event, all signs and a sharper channel remainder

**Locations:** `round51/sampled_generator.tex` (Lemma `lem:sampled`, Proposition `prop:envelope`); `round51/blocks.tex` (Lemma `lem:block-floor`).

The original nonexploration action already uses the short atom. We therefore count each stage as successful when it either does not explore or explores and selects that atom. With mass `w`, the run probability is exactly `p_*^m`, where `p_*=1-rho+rho*w`. For a labeled distribution we count the designated label; coincident labels can enlarge the event. No implemented action or likelihood is changed.

Averaging all independent block signs gives the exact identity

\[
 E_S\sum_{k=0}^{m-1}f_k^2=\sum_{k=0}^{m-1}P_k^2
   +a^2\sum_{k=0}^{m-1}(m-k)d_k^2.
\]

We use this identity rather than only record it. If `T_rl` are the explicitly computed sampled-transform coefficients, define

\[
 W=\max_{1\le r\le R}\sum_{l=0}^N T_{rl}^2/(N+1-l)\le A^2.
\]

Weighted Cauchy--Schwarz yields the improved information certificate
`kappa_W=p_*^m delta^2/(4 L^2 W)`, which is at least the simpler certificate with `A^2`. Both are exact rational numbers for rational inputs.

A further independent improvement retains the actual geometric remainder already present in the convergent-series argument:

\[
 12\Delta^{1-R}\frac{16^{-(N+1)}}{1-1/16}
 =\frac45\Delta^{1-R}16^{-N}\le\Delta^{-R}16^{-N}.
\]

The new choice of `N` therefore uses `log 16` rather than `log 8`, without the old factor `16`. The explicit sufficient region remains `C_b r+p_b s<1`, now with

\[
 p_b=3+\log(1/p_*)/\log16.
\]

The entire run probability and ceiling costs are included in `C_b`. The article provides every constant once. We do not identify the resulting conservative inner region with the minimax joint exponent frontier.

## R50-Q2 — a single atom is the principal theorem

**Locations:** `round51/introduction.tex`, Theorem `thm:main`; `round51/sampled_generator.tex`, Corollary `cor:original`.

The principal theorem now allows any bounded-duration law with an atom of positive mass `w` at `t0`, subject to `2*t0*Lambda<=1/64`. Its remaining mass need not be dense, multiscale, or discrete. The original exploration distribution is an explicit corollary using its actual atom mass; no mass is reassigned. A degenerate single-atom law is included and gives `p_*=1`, `p_b=3`.

The meaningful mechanism is the retained age of a short pulse, its channel-corrected sampled inverse, and chronological information transfer. The selectable fast gap and commitment before all signs/readouts in a block remain explicit in the abstract and theorem. Between-block feedback is unrestricted within the force bound. This is a generalization of the reviewed result, not an arbitrary-clock claim.

## R50-M2 — the finite-response reduction is now a theorem, not a contrast in words

**Locations:** `round51/response_transfer.tex`, Theorems `thm:transfer`, `thm:response-estimator`, Proposition `prop:finite-section`; `round51/introduction.tex`; `round51/LITERATURE_AUDIT.md`.

The revised argument has four independently inspectable interfaces.

1. **Response estimation.** Any finite response estimator satisfying `||bhat-b_N(beta0)||_infty<=e` can be used. The deterministic minimum-residual rule over an admissible finite response net has physical error at most `L[A(2e+eta)+E]`. The corresponding response confidence set has physical diameter at most `L(2Ae+E)`. Thus a compatible existing FIR theorem can be inserted; we no longer suggest that finite response methods are intrinsically inadequate.
2. **Compatible statistical experiment.** We prove an estimator for this bounded-input, nonreset, block-committed record. Its finite probability bound is `exp(-B p_*^m/8)+2m exp(-a^2 e^2 B p_*^m/(4v_*))`, including the shared success-count event. It handles bounded initial-state and baseline contributions through sign centering. The proof uses stopped/exponential supermartingales, not conditional Gaussianity at a terminal random count. Its response requirement has the same explicit sufficient joint depth region. This estimator is separate from the complete-posterior theorem; unsuccessful blocks are never removed from the posterior.
3. **Channel and physical inversion.** We give the integrated-pulse correction, its rational finite transform and weighted budget, then the inherited quantitative moment/Gram inverse. The latter is not advertised as a new inverse spectral principle. `round51/model_inverse.tex` is byte-for-byte the reviewed source blob `a61a885f02fbbe9ffa3f3e5524c1cb7e3076360e`.
4. **Finite-section uniformity.** For the cut at site `K`, lag horizon `S=N*Delta+t0`, and response error `epsilon`, we prove a uniform factorial bias bound and an explicit sufficient `K`. Both infinite and finite chains share the same stability constants. On the theorem's logarithmic lag and polynomial error scales, `K=O(log n)` suffices. A cut chain is a computational approximation, not an admissible infinite chain with a forbidden zero edge. We separate approximation error from response estimation error and from nonlinear inverse amplification.

Goldenshluger (1998) is now cited explicitly as a nonparametric predecessor for stable transfer functions with polynomial/exponential impulse tails. We verified its institutional bibliographic record and abstract; we did not obtain a complete theorem-level copy and do not claim otherwise. Our new reduction and estimator are proved here, so their validity does not depend on an unverified transplantation of a theorem from that paper.

For Sarkar--Rakhlin--Dahleh, we checked the author preprint `arXiv:1902.01848v6`, Assumption 1, Algorithm 1, Theorem 5.1, Proposition 5.1 and Corollary 5.1. Its response-estimation component is a genuine interface. Its raw Gaussian-input algorithm is not automatically an almost-sure bounded-force policy, and its zero initial state and finite-order constants cannot be silently transferred. We explicitly bound the finite-section response norm uniformly and supply the compatible bounded-input proof instead. We do not infer that every alternative implementation of their methods must fail.

The paper's contribution is consequently stated as an explicit end-to-end theorem for a nonlinear labeled physical target, not originality of FIR estimation, inverse Jacobi reconstruction, matrix logarithms, or logarithmic rates in isolation. The theorem map identifies exactly where each quantitative lemma is needed.

## R50-M1 — durable current executable source, with honest historical scope

**Locations:** `tools/round51_certificates.py`, `tests/test_round51.py`, `tools/verify_round51.py`, `round51/SOURCE_MANIFEST.json`.

The current revision supplies new executable implementation source directly on its revision branch. The module computes sampled transforms, the sharpened and weighted certificates, moment reconstruction, representation checks and complete exact-rational outer boxes. Resource caps raise `ResourceLimit` before enumeration rather than passing off a partial union as complete. Statistical, input-representation, tail, mesh and Taylor errors remain separate. The historical `[-10^-7,10^-7]` to `[-1,1]` witness is tested with the required representation cost.

The verifier hashes all declared source inputs, checks the literal TeX dependency closure, executes the actual Round 51 test suite and optionally requires a three-pass PDF build. Missing dependencies, digest mismatches, failed tests, undefined references and overfull boxes cause failure. It does not regenerate its manifest on verification. Commands and actual execution receipts are in the review index.

These are newly written Round 51 programs. They are not claimed to be the missing exact Round 49 programs, nor a recovery of the old 43-test workflow. The Round 50 referee's 104 cases are also a separate suite. We resolve current reproducibility by making the current implementation self-contained, while leaving the historical non-retrieval plainly recorded. The old reviewed source, reports and publication records are preserved in the parent history.

## R50-E1 — standalone article and preserved prior results

Review-round narration, upload discussion and proof-status bookkeeping have been moved to this response and artifact documentation. The main article is organized by theorem dependencies and contains the complete proofs of its positive and negative depth statements.

The earlier stagewise unrestricted-feedback laws and homogeneous inference results are preserved unchanged in `ROUND49_REVISION.tex`, `ROUND49_RETAINED_RESULTS.tex`, `round49/` and `round45/` on this full-history branch. They are not withdrawn, substituted for the new theorem, or counted again as newly proved results. The new active article does not require their publication receipts as mathematical premises. Only the new active root is covered by this round's recorded build; a second historical-root build is not claimed.

## Requested re-review

We request examination of the actual strengthened theorem and its declared hypotheses: the `16^-N` channel remainder, weighted block information, complete working posterior, compatible finite-response estimator, dimension-uniform finite-section bound, and the committed reproducibility path. The retained logarithmic depth order is not downgraded. Acceptance and exceptional-significance judgments remain matters for independent review, not conclusions certified by an author response or by finite tests.
