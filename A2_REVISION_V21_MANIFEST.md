# A2 revision v21 manifest

## Canonical revision

- Branch: `revision/a2-v21-nondominated-lan-registered-transfer-2026-09-11`
- Fork point / controlling review head: `a0dfdc85ba8fa6a0908a5b167deb563a085042e4`
- Canonical manuscript-source commit: `672b159ef204ba75a63ab92a4d52ae3960304337`
- Reviewed v20 manuscript head named by the controlling report: `f3839d34fcc045da47f257fbbf61fb1699adc76e`
- Controlling report: `reviews/a2-v20-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`

The source commit above is the v21 paper state after all theorem-level repairs
and after activation of the anchored physical realization module in
`main.tex`.  Later root-level manifest or verification commits do not alter
the manuscript source.

## Active v21 controlling files

The canonical manuscript remains in the repository's historical A2 source
directory for provenance compatibility, but `main.tex` now selects the v21
controlling modules at every interface changed in response to the referee:

- `papers/A2-v17-boundary-information-coarsening/main.tex`
- `papers/A2-v17-boundary-information-coarsening/article/01_introduction_v21.tex`
- `papers/A2-v17-boundary-information-coarsening/article/23a_signed_endpoint_rigidity_v21.tex`
- `papers/A2-v17-boundary-information-coarsening/article/18a_vector_boundary_information_v21.tex`
- `papers/A2-v17-boundary-information-coarsening/article/18b0_anchored_realization_v21.tex`
- `papers/A2-v17-boundary-information-coarsening/article/18b_raw_physical_multirate_v21.tex`
- `papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V21.md`
- `.github/workflows/a2-v21-native-build.yml`

Earlier v19/v20 theorem files are intentionally retained in the repository as
historical derivation/provenance material but are no longer selected by
`main.tex` for the interfaces repaired in v21.

## Referee-blocker map

### R20-1 / C20-M1 — non-dominated moving-support experiment

Closed at source level by `18a_vector_boundary_information_v21.tex`:

- exact Lebesgue decomposition relative to the null;
- compact-uniform `O(p_n delta_n^2)` support-exclusive mass bounds;
- common-collar censoring at
  `q_n=delta_n(log(1/delta_n))^(1/4)`;
- explicit Le Cam distance `O((log(1/delta_n))^(-1/2))` from the original
  non-dominated product experiment to a genuinely dominated representative;
- literal LAN expansion only for that dominated representative;
- transfer of Gaussian experiment, contiguity, testing and minimax statements
  back to the original family;
- compact-local fourth-moment/uniform-integrability argument under local
  alternatives.

### R20-2 / C20-M2 — one physical common-coordinate family

Closed at source level by `18b0_anchored_realization_v21.tex` and
`18b_raw_physical_multirate_v21.tex`:

- one fixed Euclidean laboratory chart;
- fixed labels, transverse origin and tangent orientation;
- explicit anchored graph family
  `(-psi_0(u),u)` and `(g+psi_1(v),v)`;
- parameter-independent raw endpoint observation map returning literal
  laboratory `y` coordinates;
- physical realization of arbitrary finite labelled contact jets and gap by
  local billiard perturbations while preserving convexity/disjointness/channel
  isolation;
- explicit frame-motion term for generic nearby-table nuisance coordinates,
  so registration is not silently treated as free.

### R20-3 / C20-M3 — abstract-to-billiard critical-scale transfer

Closed at source level by:

- `Lemma (Quantitative stability of a linearly vanishing support)` in v21
  vector boundary information;
- `Proposition (Quantitative fixed-window reduction)` in v21 physical
  experiment.

The exact support remainder is
`r_n=delta_n^2+delta_n/j_n`, the regular amplitude error is `O(delta_n)`, and
one-record squared Hellinger error is bounded by

`C{r_n^2 log(e/r_n)+delta_n^2}`.

At `k_n delta_n^2 log(1/delta_n)->1` the product error is `o(1)`.

### R20-4 / C20-M4 — tangent-level finite design

Closed at source level by
`Proposition (Tangent injectivity of the finite signed-jet map)` and
`Lemma (Finite positive-offset design)`:

- the leading curvature block has an explicit smooth inverse;
- every higher diagonal block is the determinant-one signed block `M_n`;
- the finite-jet differential is block lower triangular with invertible
  diagonal blocks;
- compactness gives a quantitative lower singular-value bound;
- finite positive designs are selected from tangent detection and may depend
  on the finite jet order.

### R20-5 — all-order signed jet proof

Closed at source level in `23a_signed_endpoint_rigidity_v21.tex` by:

- weighted half-line stationary equations;
- the positive half-line Jacobi operator and explicit Green inverse;
- differentiated implicit equations with uniform weighted bounds;
- stationary-action envelope identity;
- explicit own-contact and opposite-contact geometric sums with correct
  endpoint/interior multiplicities;
- determinant-one all-order block and explicit inverse recursion;
- finite-order local Lipschitz inverse and fixed-frame coordinate convention.

### R20-6 — endpoint output versus complete transcript

Closed at source level in the v21 introduction and physical experiment:

- the Gaussian information/minimax result is explicitly an
  `endpoint-output` statement;
- the complete stopped transcript is used for finite-to-boundary total
  variation transfer and cost accounting;
- waiting counts are explicitly allowed to carry additional information and
  are not declared ancillary.

### R20-7 — native-build certificate

The workflow implementation is present and pinned to this revision, but an
actual GitHub-hosted runner has not executed.  See
`A2_REVISION_V21_VERIFICATION.md`.  This is kept separate from the mathematical
closure status; no successful build is claimed without an executed job.

## Strength preserved

V21 does not replace the paper by a no-go theorem or reduce it to a known-gap,
even-contact, or abstract-only model.  The following conclusions remain active
and are strengthened at their proof interfaces:

- uniform nonlinear relative long-bridge law;
- recovery of gap and both curvatures;
- arbitrary odd and even labelled contact jets;
- analytic participating-contact germ determination;
- unknown gap in the physical local experiment at rate `delta_n/j_n`;
- unknown anchored registered geometry at rate `delta_n`;
- positive-definite finite-design endpoint information on each finite labelled
  jet model;
- actual finite-bridge stopped-transcript transfer with failed preparations
  charged;
- Gaussian testing and local minimax conclusions for the declared
  endpoint-output experiment.
