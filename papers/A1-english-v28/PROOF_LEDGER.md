# A1 v28 proof ledger

All labels below are source locators, not PDF theorem numbers. The inherited ledgers are retained as `PROOF_LEDGER_V26.md` and `PROOF_LEDGER_V27.md`. Their mathematical modules remain active in `main.tex` or the unchanged `companions.tex`.

## New statements and dependencies

| Statement | Active file | Dependencies and important quantifiers |
|---|---|---|
| `thm:v28-localized` | `v28/localization.tex` | Independent complete edge tapes; acquired first-block subprobability densities; recovery from arbitrary query centres. One compulsory boundary, one common controller; finite side information counted as M J_S before the query. No adaptive conditional-density assumption. |
| `cor:v28-power-tail` | `v28/localization.tex` | Exact integration of the localized tail when witness dimensions coincide. The integral constant is not an asserted sharp statistical constant. |
| `lem:v28-local-recovery` | `v28/readout.tex` | Inherited scalar scaled recovery; local part has actual query mass 1/(2P). Gives norm sqrt(2P)L_ell without a tensor inverse or a zero-pivot inverse. |
| `prop:v28-uniform-upper` | `v28/readout.tex` | Scalar whole-image all-integer-budget cover; independent edges; atomic vertex batches. Quantize once at acquisition, retain unchanged, discard on completion. Tensor damping is proved as well as local control. One joint label, no graph-length error recurrence. |
| `prop:v28-explicit-tail` | `v28/growing_graphs.tex` | Localized theorem plus all r_0-edge witnesses at a fixed level and the local recovery norm. Actual unconditional event probability rho; no all-edge regularity factor. |
| `lem:v28-retention` | `v28/growing_graphs.tex` | Independent regular-edge indicators. Exponential Markov bound proved in the text and summed over the entire compulsory level before selection. |
| `thm:v28-size-uniform` | `v28/growing_graphs.tex` | Balanced cuts at least h v, P<=d v, beta_0 h/8>log 2; v>=v_0. Exact small-ball coefficient, Gaussian ball-volume bound, all integer bit budgets, factorial determinant comparison. Constants uniform in graph size, calibration and resolution. Enlarged menu, visited-set decoder. |
| `prop:v28-graph-existence` | `v28/growing_graphs.tex` | Self-contained random bipartite multigraph construction with labelled parallel edges. Linear edge count and sufficient balanced-cut expansion, not bounded maximum degree or a polynomial construction algorithm. |
| `cor:v28-joint-limit` | `v28/growing_graphs.tex` | Scalar analytic contact-order law and the additive size-uniform bit bounds. Remainders O(v), uniform for arbitrary simultaneous graph growth and collision approach. |

## Critical inherited inputs

`text/collision_direct.tex` supplies complete reachable-image covering and scalar causal classification. `text/collision_flags.tex` supplies complete acquired confluent flags and bounded scaled recovery. `v25/graph_model.tex` supplies the independent-edge protocol, product posterior identity and original tensor metric. `v25/adaptive_proof.tex` supplies the uniform regular acquired boxes. `v26/capacity.tex` supplies first-block evidence accounting and its arbitrary-centre recoveries. These inputs retain their original hypotheses; latent-prior densities are not added.

`v27/uniform_policy.tex`, `v27/policy_menus.tex` and `v27/evaluated_model.tex` are inherited in full. Their fixed-acquisition-law quantifier, finite-prefix oracle convention, exact mixed acquired law and same-model certificate comparison are not counted as new v28 proofs.

## Decoder and task separation

The v25 qualitative theorem permits a finite-prefix oracle. The v26 certificate uses the visited set. The v27 whole-curve and policy-menu converses permit the prefix but require a resolution-blind acquisition law. The new localized theorem counts any finite side value explicitly. The size-uniform theorem permits arbitrary resolution-dependent scheduling, but its decoder has only the finite label and visited-set query descriptor. Its query menu retains the original tensor probes with weight one half and explicitly adds local tests; all remaining raw trials are counted.

## Preservation and verification

`NATIVE_SOURCE_RECORD_V28.json` records the immutable submission, review, v27 base and inherited Git tree/blob identities. The entire original v26 and v27 directories are untouched. The v28 principal entry point restores the exact reviewed v26 bridge proof (finite maximum for upper constants and positive minimum for lower constants); both earlier principal entry points are retained. No inherited theorem is removed from the active volumes.

`validation/DIAGNOSTICS_V28.json` is the executed new finite-diagnostic receipt. Older receipt files inherited at the directory root retain their historical version meanings. `validation/SESSION_RECORD_V28.json` distinguishes the checked nine-page new-results extract from the full native two-volume build, which was not executed in this session. Code and PDF checks do not certify theorem correctness, novelty or venue significance.
