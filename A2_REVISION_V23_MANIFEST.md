# A2 v23 revision manifest

**Branch:** `revision/a2-v23-intrinsic-multiscale-top4-2026-09-11`  
**Base:** `review/a2-v22-independent-harsh-top4-2026-09-11` at `7057ec51b341264fa3752a0e5eb466650579bab1`  
**Active manuscript:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Referee response:** `responses/a2-v23-referee-response-2026-09-11/RESPONSE_TO_REFEREE.md`

## Revision policy

V23 preserves the v22 all-order signed inverse, fixed-laboratory physical realization, non-dominated/common-collar endpoint theory and stopped finite-to-boundary transfer.  It strengthens the global periodic geometry and the physical-information architecture and supplies a growing-order bridge to analytic global loss.  No accepted v22 theorem is weakened or removed merely to improve the venue assessment.

## New active v23 modules

### `article/01_introduction_v23.tex`

Theorem-first introduction organized around two chains:

`relative law -> all-order signed inverse -> intrinsic lifted-channel gluing -> periodic rigidity`

and

`endpoint-time Poisson -> count-endpoint multirate Gaussian -> endpoint Gaussian coarsening -> growing-order analytic recovery`.

It uses the native periodic channel index `e=(a,b,ell)` and separates global intrinsic geometry from the fixed laboratory coordinates used in local statistics.

### `article/01b_observation_hierarchy_v23.tex`

Defines five nested record levels:

1. full growing collision history;
2. per-preparation endpoint--time record plus failure;
3. stopped endpoint--time transcript;
4. count--endpoint transcript;
5. endpoint-output experiment.

It records which finite-to-boundary theorem applies and why the three coarsened local experiments have different critical scales.

### `article/23c_analytic_continuation_v23.tex`

Standalone analytic-continuation lemma for connected strictly convex analytic boundaries.  Equality of a registered nonempty germ gives a common analytically continued curvature function; positivity and total turning force equality of the arclength periods; Frenet uniqueness gives equality of the complete boundary images.

### `article/23b_intrinsic_multichannel_rigidity_v23.tex`

This replaces the under-specified v22 unregistered extension.

- Intrinsic channel data retain `(a,b,ell)`, onset, signed endpoint-law germs and transverse orientation, but no Euclidean placement relative to the periodic lattice or other channels.
- The all-order inverse plus analytic continuation recovers complete oriented analytic copies of both incident obstacle lifts in each edge frame.
- An unknown oriented Euclidean realization `iota` of the marked abstract lattice is reconstructed jointly with the edge-frame placements.
- Algebraic gluing translates recovered lifts back by their deck offsets before matching quotient obstacle copies.
- Only **admissible** gluings are retained: periodic obstacle closures must be disjoint and the declared measured edges must remain the prescribed facing closest-pair channels.
- The quotient admissible gluing space `G_per(D)` is in bijection with periodic table realizations modulo one simultaneous global `SE(2)` motion.
- Complete analytic curvature signatures coincide exactly along orientation-preserving obstacle-symmetry orbits.
- A cycle-holonomy lemma proves that a signature-rigid closed channel cycle has translational holonomy `tau_{v_c}` and every realization satisfies `R_{e0} v_c = iota(eta_c)`, where `eta_c` is the accumulated marked deck displacement.
- A nonzero `eta_c` gives a lattice-anchoring cycle.
- A lattice-anchoring cycle plus a signature-rigid spanning tree rooted on that cycle makes the admissible periodic gluing unique and yields fully intrinsic periodic table rigidity.
- If the lattice realization and **one root channel frame relative to it** are supplied as ambient calibration, the anchoring cycle may be omitted; a common registration of all channels is only a further special case.

### `article/18c_full_endpoint_time_information_v23.tex`

Analyzes the exact endpoint--time record used by the historical finite-to-boundary transfer.

- Successful boundary density has positive trace at the moving residual-time ceiling.
- At shape scale `1/k_n` and gap scale `1/(j_n k_n)`, scaled ceiling slacks converge to a generally non-dominated Poisson boundary-shift experiment.
- The proof explicitly controls the codimension-two `r=0, w=0` corner by coarea (`O(k_n^{-2})` one-record mass), uses a binomial-to-Poisson total-variation bound in the boundary layer, and shows the common bulk contributes only the Poisson compensator.
- The v22 finite positive design makes the support-velocity map injective for every fixed finite contact-jet model.
- Waiting counts are ancillary at this fastest scale under `j_n=o(sqrt(k_n))`.
- The entire capped stopped endpoint--time transcript transfers to actual finite bridges under `k_n tau^{j_n}->0`.

### `article/18d_count_endpoint_multirate_v23.tex`

After residual time is removed but waiting counts are retained:

- decompose shape tangent into the hyperbolic-exponent direction and `ker D gamma`;
- use fast scale `(j_n sqrt(k_n))^{-1}` in the hyperbolic direction and endpoint scale `delta_n` in iso-hyperbolic directions;
- prove negative-binomial LAN for the waiting-count component;
- prove the fast count direction is asymptotically invisible to the endpoint factor under `log(j_n sqrt(k_n))/j_n^2->0`;
- obtain an independent product of a one-dimensional Gaussian count shift and the v22 endpoint Gaussian shift restricted to the iso-hyperbolic subspace;
- transfer the joint experiment to finite bridges.

### `article/18e_compatible_rates_v23.tex`

Provides an explicit common rate regime:

`delta_n=n^{-1}`, `k_n=floor(n^2/log n)`, `j_n=2 ceil(C log n)`, `C>|log tau|^{-1}`.

It also cites the exact cap input to Theorem `thm:g-stability`, equation `eq:g-competition`.

### `article/25_analytic_global_bridge_v23.tex`

Closes the fixed-order/global analytic gap.

- On a compact analytic class with singleton admissible periodic gluing, finitely many action jets resolve any prescribed global `C^q` tolerance.
- A sufficient fully intrinsic model is a persistent lattice-anchoring cycle plus a rooted signature-rigid spanning tree.  With ambient calibration, the lattice realization **and one root channel frame** replace the anchoring cycle.
- If every fixed finite action-jet vector is uniformly consistently estimable, one deterministic `M_n->infinity` can be diagonalized simultaneously over all fixed integer `q` to give global `C^q` consistency.
- No uniform-in-jet-order condition number and no sharp analytic minimax rate are assumed.

## Preserved v22 mathematical modules

The active manuscript continues to use, without weakening:

- `article/23a_signed_endpoint_rigidity_v22.tex` for the weighted all-order inverse, envelope cancellation, homogeneous filtration and determinant-one blocks;
- `article/18a_vector_boundary_information_v22.tex` for the non-dominated/common-collar moving-endpoint Gaussian theory;
- `article/18b0_anchored_realization_v22.tex` for finite labelled contact-jet realization in one fixed laboratory chart;
- `article/18b_raw_physical_multirate_v22.tex` for fixed physical windows, reference caps, endpoint-output Gaussian limits and stopped transfer;
- `v6/10_experiment_transfer.tex` and `article/17_adaptive_experiments.tex` for per-preparation and stopped endpoint--time finite-to-boundary comparison.

## Referee blocker map

| Referee item | V23 source |
|---|---|
| C22-M1 / R22-1 registration ambiguity and intrinsic global theorem | `23b_intrinsic_multichannel_rigidity_v23.tex`, `23c_analytic_continuation_v23.tex` |
| C22-M2 top-four global consequence | admissible periodic gluing classification + anchoring-cycle/tree rigidity corollary |
| C22-M3 exact analytic theorem vs fixed-jet statistics | `25_analytic_global_bridge_v23.tex` |
| C22-M4 waiting/success and richer physical information | `18c_full_endpoint_time_information_v23.tex`, `18d_count_endpoint_multirate_v23.tex` |
| C22-M5 canonical native build | `.github/workflows/a2-v23-native-build.yml`, `A2_REVISION_V23_VERIFICATION.md` |
| R22-4 preserve v22 repairs | inherited active v22 proof modules |
| R22-6 theorem-driven organization | `main.tex`, `01_introduction_v23.tex`, `01b_observation_hierarchy_v23.tex` |

## Active scope

The global theorem uses finitely many lifted **channel families**, not finitely many real scalars; each channel supplies a continuum signed support germ containing all action jets.

The complete physical local limit is proved for the stopped endpoint--time transcript at the declared record level, not for the full growing collision array.  The endpoint Gaussian theorem remains a coarsening, not an efficiency claim for richer observations.

The analytic/statistical bridge gives growing-order global consistency on compact analytic classes, not a sharp analytic minimax rate.

## Verification policy

`.github/workflows/a2-v23-native-build.yml` records the exact source head, archives the exact source, runs the native TeX build and numerical diagnostics, rejects unresolved references/fatal TeX diagnostics, hashes PDFs and uploads artifacts.  The revision is not marked native-build verified unless those runner steps actually execute and pass.  Zero-step GitHub runner failures are recorded as infrastructure failures, not converted into either a successful certificate or a TeX failure.
