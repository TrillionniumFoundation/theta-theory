# General Theta Foundations I — R11 referee packet

## Fixed mathematical and delivery objects

**Title:** General Theta Foundations I: Acquired Geometry and Causal Resource Transfer.

**Source:** `6ef290d21064b1e6514b343d3d451ad0a77e0c04`.
**Native source tree:** `f37f42455e99419d118156ecb122d9826e651c2d`.
**Complete PDF/artifact commit:** `4eb34d48cb7ba5b3fff9ad8cc958ce14a70fbda9`.
**Latest reviewed report:** `6f3ca64beec4b054dba8cb5def1a6c69fbc46d52`, the external R10 top-four report dated 8 October 2026.
**Canonical origin:** `18000b21e4bfd89180ccb069e46ac0f21621f34d` on `foundation/general-theta-foundations-i-restart-2026-10-06`.

The revision was started at the canonical ref and integrated the pinned review ancestry without changing any historical ref. The final referee-ready head is the commit containing this packet, not the earlier receipt-only head. Its public delivery branches are:

- `foundation/general-theta-restart-r11-posterior-pooling-research-2026-10-08`
- `revision/general-theta-restart-r11-posterior-pooling-2026-10-08`
- `referee-ready/general-theta-restart-r11-posterior-pooling-2026-10-08`

## Reading order and full mathematical contents

1. `../artifacts/General_Theta_Foundations_I_restart_r11.pdf` — new 16-page main article. Start with Theorem 2.2, then Lemmas 2.3-2.4, the raw sensor proof in Theorem 3.1, stratified Theorem 4.1, and the implementation/composition statements in Section 5.
2. `../artifacts/General_Theta_Foundations_I_Supplement_T.pdf` — integral complete R10, 49 pages including its cover. Its 48-page mathematical text is unchanged, not an abbreviated collection of selected lemmas.
3. `../artifacts/General_Theta_Foundations_I_Supplement_S.pdf` — integral complete R6 technical text, 23 pages including its cover. All 22 mathematical pages are retained.
4. `../REFEREE_RESPONSE.md`, `../PROOF_LEDGER.md`, `../PROOF_AUDIT.md`, `../THEOREM_MAP.md`, `../ASSUMPTION_MATRIX.md`, `../COUNTEREXAMPLE_LEDGER.md`, `../RESOURCE_ACCOUNTING.md`, `../PIPELINE_DERIVATION.md`, `../NOTATION_AUDIT.md`, `../LITERATURE_COMPARISON.md`, `../HISTORY_COVERAGE.md` and `../SCOPE_AUDIT.md`.

The response addresses the R10 report's eight major issues and 32 specific comments. It does not assert that the referee's significance or originality concerns have been independently resolved by a build.

## New general mechanism and exact limits

Theorem 2.2 treats prepared finite hidden-state kernels with finite legal actions, continuous reports and a fixed categorical squared-loss audit. Every incoming belief and action, including those produced by earlier compression, must satisfy the experiment-level acquired smoothing condition. It assumes neither separated posterior supports nor a differentiable Bellman value nor pathwise filter contraction.

The observer stores the true conditional posterior given its finite label, pooled under its own actual law. Its excess over optimal full-history feedback risk is exactly the sum of acquired Jensen defects. Lemma 2.3 integrates distributional convex curvature against the actual mass to obtain a second-order bound even at nonsmooth action switches. The deployed abstract controller has at most `1 + sum_t L_t` total states, including phases, action instructions and terminal readouts.

Writing `B_n*` for the optimal full-history risk, the proved bounds are `R_cp(n,M)-B_n* ~ M^(-2/d)` and `c M^(-2/d) <= R_aut(n,M)-B_n* <= C n floor((M-1)/n)^(-2/d)`. Thus the autonomous exponent matches for each fixed horizon. The displayed n-dependence is retained: no horizon-uniform noisy completion or sharp joint large-n profile is claimed.

Theorem 3.1 derives the acquired density and full rank directly from positive transition and report kernels through an explicit Bayes Jacobian. A two-state continuous sensor family has a strictly positive analytic gain of observation-dependent sensing over every fixed two-call sensor sequence. Theorem 4.1 treats actual subprobability strata, and Corollary 4.2 verifies a paid validation sensor repeatedly changing between vertex atoms and continuous posterior laws.

Propositions 5.1-5.2 charge simulator/interface-state products, actual calls and time, read-only programme description, erased workspace, calibration/kernel discrepancy, action approximation and numerical grid-boundary errors. Corollary 5.3 composes the noisy adaptive result with an attained early-channel defect and inaccessible calibration sign in the same scored task. It does not turn a mere allowed tolerance into a lower risk floor.

## Distinct realizations and preserved results

The new noisy controlled-sensor family verifies the posterior-pooling theorem from raw kernels. The genuinely distinct correlated singular refinement family remains fully proved in Supplement T and verifies its separated-acquisition completion theorem. It is not claimed that a separated refinement satisfies acquired smoothing, or that a noisy overlapping posterior satisfies support separation. The validation sensor is the new changing-rank extension, not an artificial relabeling of a second independent foundational theory.

The complete continuation-cut, serial-cover, changing-rank noisy regression, progressive-acquisition, filtering, block-stability, nonreset Cantor transport and stopped-task results are retained in the integral supplements and their original source subtrees. Ordered-measurement, quantum, finite-action and streaming-space papers remain independent realizations. No realization is used to prove a general theorem that is then used to prove the same realization.

## Remaining proof targets for external review

A single intrinsic necessary-and-sufficient criterion covering both overlapping-noise pooling and separated acquisition is not proved. Neither is a horizon-uniform noisy joint acquisition-memory profile, optimal synthesis/description/workspace/runtime/simulator-state region, unknown-kernel completion, a general infinite hidden-state theory, or an unbounded-stopping/infinite-transcript extension. These are substantive boundaries of the present proof, not a replacement of the General Theta mother problem by a survey or a renamed single realization.

The primary literature comparison includes finite-memory POMDP control, approximate information states, active sequential testing, controlled sensing, noisy decision trees, active feature acquisition, policy-induced acquisition shift and nonlinear-filter quantization. Standard conditioning, dynamic programming and variance identities are identified as standard tools. Targeted literature review is not a priority certificate.

## Build and independent verification

The complete successful artifact-delivery run is `37673245843`, with artifact `11506380133`. `BUILD_RECEIPT.json` and `ARTIFACT_DELIVERY.json` bind the remote PDFs to the source. `INDEPENDENT_REBUILD.json` records a fresh downloaded-packet build, all 304 unchanged input files, ten isolated builds per environment, ordinary/optimized checks, and the 88-page cross-environment comparison. TeX Live 2023 and 2025 yield different PDF byte hashes but identical normalized text and all page pixels at 97.2 dpi. `FINAL_READ_ONLY_VERIFICATION.md` records the two repaired publication defects and the exact limits of these checks.

From a complete checkout or the source-and-build packet, with Python, pypdf 5.9.0, pdflatex, the LaTeX packages used by the sources and scalable T1 fonts installed, reproduce without writing into the source tree:

```sh
python papers/General-Theta-Foundations-I-restart/r11-posterior-pooling/build.py \
  --source-sha 6ef290d21064b1e6514b343d3d451ad0a77e0c04 \
  --expected-tree f37f42455e99419d118156ecb122d9826e651c2d \
  --output /tmp/general-theta-r11-rebuild \
  --receipt /tmp/general-theta-r11-rebuild-receipt.json
```

The native manifest audit is 31 listed source files plus the manifest, 51 labels, 73 cross-references, 19 bibliography entries and 6,789 finite exact-rational checks. All retained regression chains and full mathematical texts are also rebuilt. No finite test or continuous-text rendering check replaces an independent reading of the proofs.
