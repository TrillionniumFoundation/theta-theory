# Historical dependency audit for GTF I, third revision

## Fixed editions and scope of consultation

The controlling report is `reviews/general-theta-foundations-i-v1-2026-09-22/REFEREE_REPORT.md` at review commit `01d3e78bd40985651f5b4ff24364e1dba5d481f0`, blob `65b5bc0b50b8faac5dae4fd6770eb201f1ab49f2`. It reviews v1, not v2. The new work starts from the already published v2 referee-ready tip `75d8f3f8672ab78a844cc0a7a68808b46edf56f5`. Existing v2 improvements are retained and identified as such in the response; they are not presented as newly supplied by v3.

The historical pipeline is fixed at `c04845b6613208406703695c9c184ae461f95805`. Its complete Git-tree inventory and all archived TeX, bibliography, Markdown, JSON, Python, and text files were exported by GitHub Actions run `35690282042` into artifact `gtf-i-v3-complete-pipeline-context` (artifact ID `10677304186`). The export includes the full eleven-paper pipeline, rather than a selection inferred from the current GTF manuscript. The audit consulted the Round 13 and Round 17 dependency ledgers, the Round 17 historical derivation audit, the Round 13 internal rereview, the controlling Round 17 theorem/proof inventories of all eleven modules, and the relevant conditioning, filtering, regeneration, covariance, and semigroup passages. The complete current GTF quantitative development and controlling referee report were read. This is a dependency/proof-obligation audit, not a claim to have independently reverified every historical lemma in the archive.

The master programme `foundations/general-theta/General_Theta_Foundations_v0.1.md` and its GTF I implementation addendum locate the intended general results. The stronger preceding paper editions used for comparison are:

| Edition | Immutable commit | Original source path | Preserved local edition |
|---|---|---|---|
| A1 v37 | `90465076589f5e5c69227d624f278c47744f1c1d` | `papers/A1-english-v37-publication` | `../GTF-I-v2/source-editions/A1-v37` |
| A2 v112 | `0c696736e6ec22259c730672f61ebd8ef0d95460` | `papers/A2-v17-boundary-information-coarsening/article/v112` | `../GTF-I-v2/source-editions/A2-v112` |

The later A2 v112 contact-statistical edition and the historical A2 Sinai/vector-roof local-limit gate are distinct mathematical objects. A theorem about one is not silently substituted for a theorem about the other.

## Dependency order retained from the complete pipeline

The two load-bearing chains remain

```text
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1
```

The independent A1 attainable-geometry/memory line supplies a separate comparison. No argument here uses B4 to prove the upstream B2 large-deviation theorem, assumes a reduced C1 state to prove its own sufficiency, or manufactures a D1 phase by a spectral projection.

## Eleven-component audit and its mathematical consequence in v3

The following filenames lie under `revision/round17-referee-final/` at the fixed historical commit.

| Component and controlling source | Load-bearing distinction consulted | Consequence for this revision |
|---|---|---|
| A1: `A1_GLOBAL_HYBRID_CONORMAL_FCLT.tex` | Global hybrid geometry and seam behavior cannot be replaced by a local smooth chart. | The new doubling-map proof explicitly handles dyadic jumps through fractional-part separation; it does not call the doubling map globally Euclidean-Lipschitz. The modern A1 v37 G/A/C transfer remains an explicitly identified corollary in the retained development. |
| A2: `A2_MATRIX_COEFFICIENT_RAW_LLT.tex` | The raw dynamical experiment and its vector-roof/spectral inputs precede any local-limit or coarsening conclusion. | The correlated contact theorem starts from an actual paired Gaussian observation law. It does not claim a Sinai local limit or replace the physical collision experiment by that Gaussian law without a comparison theorem. |
| A3: `A3_ENTROPY_CONTROLLED_STOPPED_LDP.tex` | Conditioning, stopping, and predictable histories must be kept in the correct experiment. | The regenerative converse uses disjoint events for the last reset, integrates over the actual prior history and independent coding tapes, and takes the time limit before the orbit-truncation limit. No finite-horizon TV estimate is promoted to an LDP. |
| A4: `A4_GLOBAL_HARRIS_FORCED_MEMORY.tex` | Regeneration and coupling refer to the unchanged process; their tail estimates require their actual hypotheses. | The reset law is specified as independent Bernoulli acquisition, so its geometric weights are derived directly. A summability assertion is never promoted to a geometric tail. The expanding process is not modified into a contracting comparison process to obtain the lower bound. |
| B1: `B1_DIRECT_CANONICAL_COEFFICIENT.tex` | Positive laws and the order of canonical conditioning are essential; formal coefficient manipulations do not supply probability measures. | Nuisance elimination averages over genuine finite-variance Gaussian nuisance laws and takes a uniform bounded-risk limit. It is not an improper-prior identity or a formal conditional density. |
| B2: `B2_GLOBAL_PRECONTACT_POSITIVE_RECOVERY.tex` | Grand-canonical construction, canonical transfer, and microcanonical recovery have different obligations. | No finite-label or Gaussian testing argument is presented as a collision-marked particle LDP or source-dependent microcanonical transfer. These historical source files are unchanged. |
| B3: `B3_CUMULANT_MOSCO_PROCESS.tex` | Joint fluctuations require the correct covariance and normalization, not independent marginal replacements. | The new statistical theorem retains both cross-covariance blocks in `V = Sigma_YY + Sigma_WW - Sigma_YW - Sigma_WY`. Exact matrix diagnostics detect omission of those blocks. No process CLT follows merely from this calculation. |
| B4: `B4_CONTROL_TRANSFER_TROTTER_KATO.tex` | State-dependent controls, process comparison, and nonlinear semigroup limits are separate steps. | The retained finite-reference Bellman theorem compares with unrestricted optimal control under its explicit assumptions. The new orbit converse is a resource lower bound, not a kinetic semigroup theorem. |
| C1: `C1_REGULAR_FILTER_QMD.tex` | Dominated disintegration/filter regularity and parameter-uniform conditional versions cannot be inferred from weak convergence alone. | The exact nuisance quotient is an equality of minimax risks for the target parameter with unrestricted additive calibration, not sufficiency for the pair `(theta, eta)`. The positive-filter stability results retain their actual positivity hypotheses. |
| C2: `C2_ACCRETIVE_FORM_FUNCTOR.tex` | Form-domain closure and unbounded resolvents cannot be replaced by finite-dimensional Schur algebra. | The Gaussian regression uses an explicitly positive definite finite covariance matrix. The retained finite-dimensional memory identities remain distinguished from unbounded-operator closure. |
| D1: `D1_LATENT_PHASE_SEMIGROUP.tex` | A physical latent event, its posterior label, and its evolution have different meanings. | The reset is an actual observed event. Its elapsed age is not supplied as a free decoder variable: all word lengths are charged in the explicit machine, and all other persistent registers are excluded in the converse. No latent phase is created by relabeling. |

## What is proved here and what is imported

The future-orbit converse, the three-regime expanding regenerative memory law, the exact correlated nuisance quotient, and the correlated nonseparable contact/label theorem are proved in the new manuscript. Their proofs do not depend on unresolved legacy spectral, particle-LDP, kinetic, or unbounded-operator inputs. The retained v2 results and v1 foundational appendices remain part of the compiled manuscript with their proofs and assumptions unchanged.

A1 v37 is cited for its model-specific geometric hypotheses, not as a source for the new infinite-horizon phase transition. A2 v112 is cited as the preceding contact-statistical work, not as proof of the new correlated-nuisance equivalence. Classical filtering, predictive rate-distortion, approximate-information-state, and Gaussian testing tools are attributed in the paper. The new exact calculation and lower bounds, rather than provenance or diagnostic counts, bear the mathematical argument.

The new paper therefore advances the causal-memory and calibrated singular-statistical branches without declaring that all eleven historical model-specific gates have been closed. This is a positive choice of theorem, not deletion of the pipeline or a replacement of its open obligations by weaker terminology.

## Preservation and reproducibility

The preceding `papers/GTF-I-v2` tree is not edited. The build checks its original compilation/input hashes and, on GitHub, the exact Git trees of the preserved first edition and both fixed A1/A2 editions. The integrated v3 body contains the byte-identical quantitative suffix of v2, followed by all original foundational sections and both mathematical appendices. All their mathematical labels must resolve after compilation. Previous introductions and project documents remain in their original complete editions.

`SOURCE_MANIFEST.json` fixes every new mathematical and executable input. `evidence/BUILD_RECEIPT.json` records the actual source checkout and generated PDF; source hashes, finite diagnostics, and successful typesetting are reproducibility evidence, not independent mathematical refereeing.
