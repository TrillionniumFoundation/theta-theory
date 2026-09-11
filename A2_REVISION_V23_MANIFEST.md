# A2 v23 revision manifest

**Revision branch:** `revision/a2-v23-intrinsic-multiscale-top4-2026-09-11`  
**Revision base:** `review/a2-v22-independent-harsh-top4-2026-09-11` at `7057ec51b341264fa3752a0e5eb466650579bab1`  
**Active manuscript entry point:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Referee response:** `responses/a2-v23-referee-response-2026-09-11/RESPONSE_TO_REFEREE.md`

## Revision policy

This revision keeps the v22 all-order signed inverse, fixed-laboratory physical model, non-dominated/common-collar Gaussian theory and stopped finite-to-boundary transfer.  It does not lower the target theorem level or delete accepted mathematical content to avoid the v22 referee objections.  The new work strengthens the global periodic geometry and physical information architecture and supplies a growing-order bridge to analytic global loss.

## Active v23 source changes

- `papers/A2-v17-boundary-information-coarsening/main.tex`
  - new title and abstract centered on intrinsic periodic rigidity and multiscale physical information;
  - theorem-first two-part architecture;
  - retains the inherited proof modules supporting the accepted v22 results;
  - activates the new v23 global, physical and analytic bridge modules.

- `article/01_introduction_v23.tex`
  - presents the active theorem chains rather than revision chronology;
  - uses the repository's native lifted-channel index `e=(a,b,ell)`;
  - separates intrinsic periodic gluing from laboratory coordinates used in local statistics;
  - states the three nested physical observation levels and their distinct limit experiments;
  - states the fixed-order versus growing-order distinction explicitly.

- `article/01b_observation_hierarchy_v23.tex`
  - defines five observation levels from full collision history through endpoint output;
  - identifies which finite-to-boundary comparison applies at which sigma-field;
  - records the Poisson, count--endpoint and endpoint-Gaussian information hierarchy.

- `article/23c_analytic_continuation_v23.tex`
  - standalone analytic continuation lemma for registered connected analytic boundary germs;
  - proof via real-analytic curvature continuation and uniqueness of the Frenet system.

- `article/23b_intrinsic_multichannel_rigidity_v23.tex`
  - defines intrinsic signed **lifted-channel** data using the same `(a,b,ell)` convention as the geometric setup;
  - supplies no inter-channel Euclidean placement and no channel-to-lattice orientation;
  - introduces an unknown oriented Euclidean realization of the marked abstract periodic lattice;
  - defines the periodic gluing space by translating recovered obstacle lifts back by their deck offsets;
  - proves a classification of all periodic realizations modulo one simultaneous `SE(2)` motion;
  - identifies complete curvature-signature coincidences with Euclidean symmetry orbits;
  - proves obstacle-placement propagation along a signature-rigid spanning tree;
  - identifies a signature-rigid cycle with nonzero accumulated deck displacement as a lattice-anchoring holonomy;
  - proves full intrinsic periodic rigidity from the spanning tree plus an anchoring cycle;
  - treats a known ambient lattice frame and the fully registered v22 theorem as special cases.

- `article/18c_full_endpoint_time_information_v23.tex`
  - studies the exact endpoint/residual-time selected record used by the historical transfer theorem;
  - derives the fastest-scale Poisson boundary-shift experiment from the positive moving-ceiling density;
  - identifies all fixed finite contact-jet coordinates by a finite positive design;
  - proves waiting counts ancillary at this fastest scale under `j_n=o(sqrt(k_n))`;
  - transfers the complete stopped endpoint--time transcript to actual finite bridges.

- `article/18d_count_endpoint_multirate_v23.tex`
  - retains waiting counts after residual time is removed;
  - decomposes the shape tangent into the hyperbolic-exponent direction and its kernel;
  - proves negative-binomial LAN for the fast count direction;
  - proves the endpoint Gaussian factor is insensitive to that fast direction under an explicit rate condition;
  - obtains an independent two-speed count--endpoint Gaussian limit;
  - transfers the result to actual finite bridges.

- `article/18e_compatible_rates_v23.tex`
  - provides one explicit sequence satisfying all relevant endpoint/count/transfer conditions;
  - cites the exact uniform threshold theorem/equation feeding the reference-cap success-ratio estimate.

- `article/25_analytic_global_bridge_v23.tex`
  - finite-coordinate resolution theorem for compact analytic classes with singleton **periodic** intrinsic gluing;
  - records a signature-rigid spanning tree plus lattice-anchoring cycle as a sufficient intrinsic model;
  - diagonal `M_n -> infinity` reconstruction theorem from uniformly consistent fixed-order estimators;
  - global `C^q` consistency without an assumed uniform-in-order signed-jet condition number.

- `.github/workflows/a2-v23-native-build.yml`
  - exact-branch native build, diagnostic and hash workflow for the new revision.

## Referee blockers mapped to v23 source

| Referee item | V23 source |
|---|---|
| C22-M1 / R22-1 intrinsic global theorem and registration ambiguity | `23b_intrinsic_multichannel_rigidity_v23.tex`, `23c_analytic_continuation_v23.tex` |
| C22-M2 top-four global consequence | periodic gluing/holonomy classification + spanning-tree/anchoring-cycle global corollary |
| C22-M3 finite-jet statistics versus analytic/global recovery | `25_analytic_global_bridge_v23.tex` |
| C22-M4 incomplete physical information / waiting channel | `18c_full_endpoint_time_information_v23.tex`, `18d_count_endpoint_multirate_v23.tex` |
| C22-M5 canonical native build | `.github/workflows/a2-v23-native-build.yml`, verification record |
| R22-4 preserve v22 repairs | inherited active v22 modules remain in `main.tex` |
| R22-6 theorem-driven organization | `main.tex`, `01_introduction_v23.tex`, `01b_observation_hierarchy_v23.tex` |

## Results deliberately preserved from v22

The active manuscript continues to use:

- `article/23a_signed_endpoint_rigidity_v22.tex` for the weighted all-order inverse, envelope identity, homogeneous jet filtration and determinant-one blocks;
- `article/18a_vector_boundary_information_v22.tex` for the non-dominated/common-collar Gaussian boundary experiment;
- `article/18b0_anchored_realization_v22.tex` for realized finite contact-jet models in one fixed laboratory chart;
- `article/18b_raw_physical_multirate_v22.tex` for the endpoint-output fixed-window Gaussian theorem, reference caps and stopped transfer statement;
- `v6/10_experiment_transfer.tex` and `article/17_adaptive_experiments.tex` for the per-preparation and stopped endpoint--time finite-to-boundary comparison.

No uniform-in-jet-order conditioning theorem is inserted into these inherited results.  The v23 compactness/sieve bridge is designed precisely so that the growing-order conclusion does not require such an unproved bound.

## Scope of the new global and physical claims

The intrinsic global theorem uses finitely many **lifted channel families**, each carrying a continuum signed support germ; it does not call this finitely many scalar observations.  It reconstructs relative channel placement and periodic lattice holonomy except for genuine obstacle-symmetry / gluing ambiguity, and gives explicit sufficient conditions for uniqueness.

The physical theorem is complete for the stopped endpoint--time transcript at the declared record level, not for the full growing collision array.  The endpoint-output Gaussian theorem is retained as a coarsening, not as an efficiency claim for richer observations.

The analytic/global bridge supplies growing-order consistency and global loss on compact analytic classes.  It does not claim a sharp analytic minimax rate.
