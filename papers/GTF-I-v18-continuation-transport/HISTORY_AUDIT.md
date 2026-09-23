# Frozen source history and proof-status audit

## What was read

The controlling third v17 report (`a94ec98d6e33d9719f72deec160f5c8270ce006f`) and the pipeline second report (`9f4787221c086e25f7d95b36e97aff870bd2b0c5`) were read against their common manuscript `e5a81e26e9a1b366f5863b00e09d62512f32f5ea`. The first independent report is discussed by both; it is not described here as a separate full-text audit.

The successful v17 artifact 10739552465, run 35836335685, was retrieved. Its SHA-256 is `afb67b427556058b5200aa28986827669d9a5a21c8d7058a80fe3f9839c1f966`. The 446-file compiled-source closure was extracted and the canonical v17 definitions/proofs, its response/proof/history/literature ledgers, its typed eleven-component graph and its preservation machinery were used. The full historical mathematical development remains attached. Reading and preserving this closure is not represented as independently re-proving every theorem in the eleven external component papers.

The GTF ancestry develops source-consuming retained state, common task-blind encoders, actual marks, continuation quotients, separately priced private/hidden/visible randomness, finite-task comparison/completion, intrinsic marked deficiency, strict polynomial certificates and physical finite presentations. V18 retains this structure and adds continuation normalization, a finite-reset information budget, exact resource/sample obstructions and a changing-microscopic-path consumer. Later version numbers are not theorem-status evidence.

## The exact external B4 and C2 sources examined

Historical commit: `c04845b6613208406703695c9c184ae461f95805`.

B4 source: `papers/B4-nonlinear-kinetic-semigroups/ROUND17_POSITIVE_CLOSURE.tex`, blob `1e6c5a870ca1ecf3319c1f1d950a1f0f1564dfb4`.

C2 source: `papers/C2-cotangent-rigidity-tangent-representations/ROUND17_POSITIVE_CLOSURE.tex`, blob `6fa8639339ebae9a19122cbdba339ec6f275b562`.

These files do not merely list desired gates: they contain theorem statements **asserting** their closure. That source assertion is distinct from current proof credit. Both files were read as derivation sources, not accepted as certified inputs to v18.

### B4: an explicit normalized-resolvent mismatch

The source defines the discounted operator using `lambda h` in the running reward. Nonnegative action and a zero-cost trajectory give `R_lambda 1 = 1` for every positive lambda. Its displayed formula

`R_lambda - R_mu = (mu-lambda) R_lambda R_mu`

then has value zero on the left and `mu-lambda` on the right when applied to 1. The literal formula therefore cannot hold for distinct parameters. In a linear normalized setting the identity instead reads `mu J_lambda - lambda J_mu = (mu-lambda) J_lambda J_mu`; an appropriate nonlinear resolvent relation must be formulated and proved, not borrowed as a linear difference formula. For `J_lambda=(I-lambda^{-1} H)^{-1}`, the usual graph rearrangement would require the nonlinear identity `J_lambda f = J_mu((lambda/mu)f + (1-lambda/mu)J_lambda f)` on its justified domain. This observation alone neither establishes that domain nor proves range, comparison or convergence.

Consequently the historical aggregate B4 theorem is not used to establish current GTF scope. The separate action-sublevel, corrector, recollision, graph-domain and nonlinear-limit requirements remain in the program, with their exact original statements preserved. They are not replaced by the two-particle theorem.

### C2: replacing an unsupported tightness inference

The proof of `thm:r17-c2-optional` identifies finite-dimensional optional projections and then says that Doob's maximal inequality supplies tightness. Amplitude control alone does not control the temporal modulus. The explicit two-jump bounded-martingale example `ex:v18-fiditightness` isolates that failure. This is not a claim that every strengthened version of the source's conditional-kernel assumptions is false.

Within the common-preparation bounded-Gaussian observation class, the old optional-projection step is replaced by `thm:v18-gaussian`: a direct full/projected likelihood S2 estimate and a common-latent posterior supremum bound. `prop:v18-innovation` identifies the projected stochastic exponential before taking its limit; `thm:v18-entropic` proves the bounded entropic backward consequence and localized integrand convergence. `thm:v18-microscopic` discharges these hypotheses for changing collision trajectories. The old full `thm:r17-c2-main` remains conditional on all its independent inputs, rather than receiving proof credit for strict duality, form response or rigidity from this scoped replacement.

## Eleven components and exact credit

A1,A2,A3,A4,B1,B2,B3,B4,C1,C2,D1 are retained. The prior graph's component declarations are preserved verbatim inside `PIPELINE_GRAPH.json` under `inherited_v17_declarations`. Current credit is separately namespaced. A2 remains independent: no GTF arrow is manufactured into its primary geometric chain. The actual new consumer is the C2 bounded Gaussian/entropic/stopping branch, whose proof uses the microscopic comparison and transport estimates. No aggregate global-closure flag is inferred from this fact.

The authoritative statement identities for this release are in `PROOF_STATUS.json`, resolved to the build checkout by `evidence/BOUND_PROOF_STATUS.json`. Historical branches and files are immutable evidence of their statements, not automatically current endorsements.
