# A2 v22 revision manifest

**Revision branch:** `revision/a2-v22-allorder-multichannel-top4-2026-09-11`  
**Revision base:** `review/a2-v21-independent-harsh-top4-2026-09-11` at `0d94442420c5b2117246962cd984c7795caa8738`  
**Canonical manuscript-source commit:** `82a19b18f35fee63819bcc99d530f52adf56c384`  
**Active manuscript entry point:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Referee response:** `responses/a2-v22-referee-response-2026-09-11/RESPONSE_TO_REFEREE.md`

## Active v22 source changes

- `papers/A2-v17-boundary-information-coarsening/main.tex`
  - activates the v22 theorem chain and revised abstract;
  - retains the historical supporting modules required by the proofs.
- `article/01_introduction_v22.tex`
  - theorem-first reconstruction of the introduction;
  - separates deterministic rigidity, non-dominated local asymptotics and physical record levels.
- `article/23a_signed_endpoint_rigidity_v22.tex`
  - quantitative weighted half-line inverse;
  - correct action-jet order bookkeeping;
  - finite-truncation envelope identity and tail cancellation;
  - homogeneous isolation of the first occurrence of each graph jet;
  - determinant-one all-order block;
  - compact quantitative tangent inverse.
- `article/23b_multichannel_rigidity_v22.tex`
  - new finite-channel analytic table-rigidity theorem.
- `article/18a_vector_boundary_information_v22.tex`
  - explicit Hellinger convention;
  - dominated common-collar representative;
  - parameter-independent comparison kernels;
  - bounded-sequence contiguity;
  - finite-subexperiment Gaussian convergence;
  - identifiable-subspace/pseudoinverse formulation for singular information;
  - local minimax theorem at the correct level.
- `article/18b0_anchored_realization_v22.tex`
  - statistical patch lies inside cutoff plateau;
  - preservation of embeddedness, strict convexity, disjointness and channel isolation is explicit.
- `article/18b_raw_physical_multirate_v22.tex`
  - even-flight parity for same-type experiments;
  - exact observation-sigma-field hierarchy;
  - fixed-time versus channel-centered derivative conventions;
  - finite tangent-level design;
  - one reference-based deterministic cap sequence independent of compact local parameter sets;
  - stopped finite-to-boundary transfer only at the declared endpoint/residual-time record level;
  - endpoint-output Gaussian conclusion without claiming complete-transcript efficiency.
- `article/01b_observation_hierarchy.tex`
  - references and terminology aligned with v22 active theorems.
- `.github/workflows/a2-v22-native-build.yml`
  - exact-branch native build and diagnostics workflow.

## Referee blockers mapped to source

| Referee item | V22 source |
|---|---|
| R21-1 all-order proof closure | `23a_signed_endpoint_rigidity_v22.tex` |
| R21-2 physical parity | `18b_raw_physical_multirate_v22.tex` |
| R21-3 cap quantifiers | `18b_raw_physical_multirate_v22.tex`, Lemma `Reference-based cap` |
| R21-4 observation sigma-field | `18b_raw_physical_multirate_v22.tex`, `01b_observation_hierarchy.tex` |
| R21-5 LAN/Le Cam/minimax levels | `18a_vector_boundary_information_v22.tex` |
| R21-6 top-four conceptual consequence | `23b_multichannel_rigidity_v22.tex` |
| R21-7 canonical native build | workflow added; runner execution remains externally blocked, see `A2_REVISION_V22_VERIFICATION.md` |

## Scope discipline

The revision does not remove the v21 signed all-order inverse, moving-support Gaussian theorem, physical fixed-window realization or finite-to-boundary transfer.  It strengthens their proofs and statements.  The new table-rigidity theorem is explicitly restricted to connected real-analytic labelled obstacle boundaries and a finite registered spanning channel cover.  The statistical information matrix remains an endpoint-output information statement and is not promoted to a full raw-collision-history efficiency theorem.
