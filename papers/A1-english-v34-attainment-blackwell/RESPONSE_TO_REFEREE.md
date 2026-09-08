# Response to the second independent referee report on A1 v30

**Manuscript:** *Attainable information, exponent collisions, and adaptive memory*  
**Revision:** v32, causal compatibility and finite certificates  
**Date:** 8 September 2026  
**Controlling submission:** `dc8c1bd475b870cd222627c0cfd6d784363e1728`  
**Controlling review:** `b9296a7b4736225e72f95cc275c31df220442772`, `reviews/a1-english-v30-harsh-second-independent-2026-09-08/REFEREE_REPORT.md`  
**Intended new branch:** `revision/a1-english-v32-causal-certificates-2026-09-08`  
**Intended native directory:** `papers/A1-english-v32-causal-certificates/`

## Preparation-session status (before application)

This package contains new English proof modules, a compiled new-results packet, a preservation-oriented integration program, and executed finite diagnostics. It is not a receipt for a GitHub push. The remote revision branch has not been created in this session. The complete inherited article and companion have not been compiled together here. The packet's successful compilation does not close the referee's full-native-build requirement.

The supplied integration creates a new branch from the pinned review commit, verifies the principal manuscript blob identities, copies the entire tracked v30 native directory, and incorporates the new material into that copy. It preserves the original directory, reports, and proof modules. This operation is supplied for execution in an authenticated checkout; it has not been executed against the complete repository in this session.

## Overview of the mathematical revision

The attained collision classification remains the leading theorem. We have not replaced its shared latent parameter by regenerative blocks, reduced its class of priors, or removed the existing graph and occupation developments. The new analysis keeps the original common-filter resource: one of M persistent labels, the current command and report, a read-only clock, fresh private coins, and no persistent public seed.

The central addition is a finite characterization and a uniform approximation of this nonregenerative decision problem. For a finite command alphabet, joint history–state occupancies must satisfy one common collection of update equations. These equations are necessary and sufficient for a realizable finite-state controller. They give a compact, generally nonconvex polynomial optimization, not a relaxation obtained by independently assigning local losses.

For the positive monomial command cube, replacing commands by representatives of cells of radius δ changes the optimal mean risk by at most T(1+2/κ)δ and the optimal worst-history risk by at most 2Tδ/κ in the stated one-sided comparison. The proof allows arbitrary Borel coding kernels. Its constants do not contain an inverse exponent gap. A complete rational net of feasible controllers then gives a global lower certificate and an implementing upper certificate. With δ ≤ M^−3 and transition denominator M^4, certified interval width O(M^−3) combines with the attained lower bound cΞ_N ≥ cM^−2 to give relative width O(M^−1), uniformly across collision strata.

This last inference uses the collision theorem for its operational lower scale. The finite characterization and absolute approximation are proved independently of that theorem. The construction is exhaustive rather than computationally efficient, and certified numerical evaluation requires access to the finite prior-moment list. Neither a polynomial-time bound nor computability of an arbitrary abstract prior is asserted.

## R2.1 — Identify the publication-bearing advance

**Response.** The introduction now identifies the attained, collision-uniform classification as the principal geometric theorem. It distinguishes four logically different conclusions: the acquired image and its truncated determinant scales; one common causal realization; exact finite history–state compatibility; and uniform global certification of the same nonregenerative optimum.

The new positioning subsection compares mathematical objects rather than attributing novelty to their generic tools. Graf–Luschgy concerns quantization of specified measures; the acquired measure and its causal realization remain additional obligations here. Clustered Vandermonde spectral results do not themselves establish positive acquired mass in a nonlinear statistical image. Zero-delay Markov coding does not automatically charge the complete persistent state in the same way as the present transducer. Finite-state POMDP controllers have already been formulated by nonlinear optimization; we explicitly cite that precedent rather than claiming this formulation principle as new.

**Locations.** `v32/introduction_compatibility.tex`, `v32/positioning.tex`; inherited `thm:resolution-main`; new `thm:v32-finite`, `thm:v32-grid`, and `cor:v32-relative`.

**Scope of the comparison.** This is a targeted primary-source comparison, not an exhaustive priority determination or a theorem-by-theorem audit of every cited external paper. The submission's significance remains a matter for independent assessment. It is not certified by a build, a diagnostic count, or the authors' choice of theorem titles.

## R2.2 — A consequential operational result with retained future information

**Response.** The new compatibility equations operate on the original shared latent parameter. If α_h(i) is the joint mass of a history h and retained label i, then

    α_hcx(j) = r_x(h,c) Σ_i α_h(i)b_(t+1)(c,j | i,x).

The same update row must be used at every history reaching label i. For state-controlled acquisition, the constraints Σ_j b_t(c,j|i,x)=a_t(c|i) for every report x enforce command selection before that report. A factorization proof shows that the latent posterior conditional on the full command/report history is the likelihood-product posterior, including when commands are chosen from the retained state. This supplies the coefficients of the optimization without giving that posterior to the decoder.

Every feasible point is implemented by one transducer, and every admitted transducer gives a feasible point. Eliminating these common-row restrictions is not allowed. The formulation thus retains the causal condition missing from a flow of current-target marginal distortions. Its nonconvexity is not disguised by an invalid minimax interchange.

The command-partition theorem then shows that this exact finite problem approximates the continuous monomial problem uniformly. For mean risk, averaging a continuous kernel over each command cell implements the reverse comparison using fresh private coins, not a retained cell-location seed. For worst-history risk, restriction and rounding keep the coding expectation inside the history supremum. An additional corollary handles state-controlled acquisition, while explicitly not transferring to it the prescribed-exploration collision lower bound.

**Exact positive example.** The revision also solves a nonregenerative two-checkpoint problem. Its centered targets are γX_j+eU_j, with 0<γ≤1/8 and 0<e≤γ/2, obtained from uniformly positive binary acquisition and readout experiments. Both schedules acquire the same four reports once, execute one selected query, use two labels at block boundaries, and have no persistent public seed. The optimal risks are

    V_jit(e) = e²,
    V_early(e) = γ² + e² − max{γ²/3, (2γ+e)²/15}.

The proof optimizes over all private randomized binary encoders, not only deterministic partitions. Conditional-centroid reduction and an upper-tail argument reduce the optimization to eight explicit tail endpoints; two deterministic encoders attain the result. Thus two admitted common-controller designs with identical information charges have an unbounded risk ratio as e tends to zero.

The referee's control used a persistent public seed. Its value is not contradicted by this unseeded formula. The manuscript identifies that distinction, including a public-seed upper construction. The finite example has block-boundary memory charging, which is not silently identified with the monomial theorem's per-report charging.

**Locations.** `thm:v32-finite`, `prop:v32-centroids`, `lem:v32-perturbation`, `thm:v32-grid`, `cor:v32-controlled`, `lem:v32-controller-net`, `thm:v32-certificates`, `cor:v32-relative`, and `thm:v32-delayed`, all in `v32/new_results.tex`.

## R2.3 — Preserve the model ledger

**Response.** `v32/model_ledger.tex` records acquisition information, decoder access, seed access, score feedback, memory-charge boundary, risk quantifiers, and the target family for each principal model. The original scalar theorem and new certificates share one row. State-controlled acquisition is separate. Fixed-graph tensor loss, size-uniform mixed loss, regenerative public-descriptor experiments, and the block-charged delayed-use example are not conflated.

The new derivations repeatedly state the operational convention at the point where it affects a theorem: selection before the report in the row constraints; no persistent seed in exact finite realization; expectation inside the worst-history supremum; and the distinct block charge in the exact example.

## R2.4 — Preserve closed repairs and supply a complete build

**Preservation response.** The integration copies every tracked file from the pinned v30 native directory. It does not alter `v27/policy_menus.tex`, `v30/menu_finiteness.tex`, the existing scalar or graph proofs, or any companion proof. The old main entry point is additionally archived in the new directory. The v30 introduction remains available as a historical file; the revised entry uses one generated introduction that retains the original definitions, main theorem input, graph summaries and qualified regenerative claims.

The optimized fixed-calibration menu finiteness correction remains in force. The original tensor, mixed, and attenuated regenerative tasks remain distinct. No new theorem asserts conditional regeneration for the shared monomial posterior, horizon-uniform error propagation, or equivalence of all three loss metrics.

**Build response: partially fulfilled.** The new-results packet was compiled and inspected separately. Exact diagnostics were executed under ordinary Python and `python -O` with byte-identical JSON output. Their scope is recorded in the receipts. The complete native article and companion have not been built in this session; their cross-volume references and page output have not been inspected as a complete pair. A supplied native-build program performs repeated cross-reference passes and rejects unresolved citations and references, but an unexecuted program is not a successful build receipt. Consequently R2.4 remains open for the full native publication object.

## Remaining editorial observations S2.1–S2.5

**S2.1.** The regenerative result remains a correct separable realization. The new theorem does not rename it as a nonregenerative solution: it introduces the common history–state constraints and proves a uniform approximation for the original nonregenerative class.

**S2.2.** The inherited network-uniform scalar-factor ratio is retained with its original meaning. The new uniformity is in command approximation and certificate width at a fixed horizon, across calibration and M. It is not an error-propagation theorem uniform in network size or all priors.

**S2.3.** The earlier J+1−1/J ratio remains identified as a common-design consistency penalty. The new early/just-in-time ratio compares two admitted schedules under one charge and seed convention. It is a timing comparison, not an unproved adaptive-scheduling advantage.

**S2.4.** The contribution comparison now names the mathematical objects and inherited methods. In particular, finite-controller nonlinear optimization, ordinary quantization, convex duality and Vandermonde spectral analysis are not relabelled as original principles.

**S2.5.** The intended main article proceeds from attained geometry to nonregenerative compatibility and certificates, then to graph and regenerative consequences. All inherited derivations are preserved. The remaining complete-build limitation is recorded rather than hidden by the existence of the source archive or packet PDF.

## Reproducibility and independent reassessment

`tests/check_revision.py` uses exact fractions and explicit exceptions. It compares the compatibility recurrence with direct latent/state-path enumeration, checks centroid and controller-rounding identities, tests the positive likelihood perturbation bounds at rational collision calibrations, and exhausts all 32,768 unordered deterministic binary partitions at seven parameter values. Additional stochastic encoders are diagnostics only; the proof for all stochastic encoders is the analytic argument in the manuscript. The full finite controller net for arbitrary monomial experiments was not enumerated.

The packet contains detailed proofs for the new statements. No formal proof-assistant verification, exhaustive novelty certification, external journal endorsement, or successful full-repository build is claimed. The requested next assessment is of these substantive mathematical additions together with the preserved attained-information theorem, with the exact information conventions and outstanding native-build requirement visible.
