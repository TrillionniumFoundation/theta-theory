# Proof and dependency ledger

This ledger locates mathematical proofs; it is not a proof-assistant certificate.
The first manuscript contains 11 theorems, 13 propositions, 6 lemmas, 2 corollaries,
32 proof blocks, 3 definitions, and 12 boundary examples. Classical antecedents are
attributed in the article and the literature record.

## Principal chains

1. Positive kernels -> path law -> instrument update -> future-test quotient.
2. Executable causal machines -> predictable telescoping -> composition/risk transfer.
3. Physical squared loss -> exact checkpoint quantization -> small-ball lower bound.
4. Admissible invariant domains + finite covers + same-input stability -> finite-state emulation.
5. Refreshing hidden dynamics -> Bayes contraction + invariant domain + physical Jacobian
   -> actual density bound + fixed global cover -> time-uniform matching memory law.
6. Parameter-independent postprocessing -> posterior/entropy/score identities.
7. Positive test functionals -> response and product fibres; exponential transforms
   -> exact pressure composition, with LDP and unbounded dynamics remaining conditional interfaces.

## Formal statements

| Type | Statement | Stable label | Native source |
|---|---|---|---|
| proposition | Path construction | `prop:paths` | `sections/02_experiments.tex` |
| proposition | Normalized update | `prop:bayes` | `sections/02_experiments.tex` |
| theorem | Minimal future prediction | `thm:quotient` | `sections/03_predictive_quotients.tex` |
| theorem | Compact continuous realization | `thm:compact-quotient` | `sections/03_predictive_quotients.tex` |
| proposition | Positive finite-coordinate update | `prop:coordinate-update` | `sections/03_predictive_quotients.tex` |
| lemma | Predictable telescoping | `lem:telescoping` | `sections/04_causal_reductions.tex` |
| theorem | Composition and risk transfer | `thm:composition` | `sections/04_causal_reductions.tex` |
| proposition | One-step realization | `prop:one-step` | `sections/04_causal_reductions.tex` |
| theorem | Posterior barycentre and convex order | `thm:barycentre` | `sections/05_information.tex` |
| theorem | Entropy loss and a common recovery kernel | `thm:entropy-gap` | `sections/05_information.tex` |
| theorem | Score projection | `thm:score` | `sections/05_information.tex` |
| proposition | Sequential score decomposition | `prop:sequential-score` | `sections/05_information.tex` |
| theorem | Exact checkpoint identity | `thm:quantization` | `sections/06_checkpoint_geometry.tex` |
| lemma | Mass obstruction | `lem:small-ball` | `sections/06_checkpoint_geometry.tex` |
| lemma | A positive attained chart | `lem:attained-chart` | `sections/06_checkpoint_geometry.tex` |
| theorem | Finite-state emulation | `thm:emulation` | `sections/07_causal_emulation.tex` |
| corollary | Contractive implementation | `cor:contractive` | `sections/07_causal_emulation.tex` |
| theorem | Refreshing experiment memory law | `thm:refresh` | `sections/08_dynamic_model.tex` |
| lemma | Uniform contraction | `lem:refresh-contraction` | `sections/08_dynamic_model.tex` |
| lemma | An invariant shrinking domain | `lem:refresh-domain` | `sections/08_dynamic_model.tex` |
| lemma | Posterior Jacobian and unconditional density | `lem:refresh-density` | `sections/08_dynamic_model.tex` |
| corollary | Persistent bits and double attenuation | `cor:double-attenuation` | `sections/08_dynamic_model.tex` |
| proposition | Normalized response | `prop:normalized-response` | `sections/09_response_and_modules.tex` |
| theorem | Product-observation fibre | `thm:product-fibre` | `sections/09_response_and_modules.tex` |
| proposition | Normal second jet | `prop:normal-jet` | `sections/09_response_and_modules.tex` |
| proposition | Finite continuous algebras have finite quotients | `prop:finite-algebra` | `sections/09_response_and_modules.tex` |
| theorem | Exponential composition and entropy duality | `thm:pressure` | `sections/10_pressure_and_interfaces.tex` |
| proposition | Second-order chain rule for a random channel | `prop:pressure-chain` | `sections/10_pressure_and_interfaces.tex` |
| proposition | Finite-horizon exponential dynamic programming | `prop:exp-dp` | `sections/10_pressure_and_interfaces.tex` |
| proposition | Quadratic constrained reduction | `prop:quadratic` | `sections/10_pressure_and_interfaces.tex` |
| proposition | Bi-Lipschitz readout comparison | `prop:readout-comparison` | `sections/A_measurable_and_geometric_lemmas.tex` |
| proposition | Exact scalar uniform quantization | `prop:uniform-quantization` | `sections/A_measurable_and_geometric_lemmas.tex` |

## Scope controls

No abstract measurable quotient is automatically called standard Borel. The compact
continuous realization theorem supplies one explicit sufficient condition. No unknown
parameter is read by a causal simulator. The dynamic lower law fixes one independent
uniform acquisition strategy. The same codebook works at every positive time, but it
may depend on known calibration. The contraction interval excludes vanishing refresh.
Checkpoint prediction excess and common-target decision risk are never identified.
All independent-noise, score-noise, finite-precision, and command-quantization variants
retain their separate observation meanings. Conditional LDP statements do not establish
model-specific LDPs, CLTs, LAN, or unbounded operator memory identities.
