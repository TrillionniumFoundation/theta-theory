# A2 v21 proof ledger

**Branch:** `revision/a2-v21-nondominated-registered-transfer-2026-09-11`  
**Controlling review:** `review/a2-v20-independent-harsh-top4-2026-09-11`  
**Canonical entry:** `main.tex`

This ledger is a navigation map to the promoted proofs. It is not a substitute for the proofs and not a correctness certificate.

## 1. Nonlinear relative boundary law

**Active sources**

- `article/01c_geometric_setup_v18.tex`
- `article/02_finite_results.tex`
- `v3/10_geometry_action.tex`
- `v3/20_integration.tex`
- `v4/10_boundary_layers.tex`
- `v5/15_differentiated_operators.tex`
- `article/15_operator_comparison.tex`
- `article/16_hyperbolic_coordinates.tex`
- `article/16c_strict_margin.tex`

**Promoted statement.** After normalization by the exponentially small endpoint twist, the finite alternating bridge converges on a fixed offset collar to the half-line action/amplitude product, uniformly with every fixed mixed geometric/offset derivative. This part is unchanged mathematically in v21.

## 2. Signed arbitrary-jet rigidity and its differential

**Active source**

- `article/23a_signed_endpoint_rigidity_v21.tex`

**Historical inputs**

- `v3/10_geometry_action.tex` — local flight action, alternating Jacobi operator, weighted finite-bridge Green estimates;
- `v4/10_boundary_layers.tex` — half-line Green kernel, weighted half-line stationary solution and derivative bounds;
- `article/23_two_contact_rigidity.tex` — historical highest-new-jet envelope mechanism in the even two-contact problem;
- `article/29_two_flight_benchmark.tex` — finite low-order benchmark.

**New theorem-level closure.** V21 writes the half-line Euler–Lagrange system in the weighted sequence space, proves uniform invertibility of the nonlinear Jacobi operator, establishes finite-jet dependence at every degree, proves the stationary envelope identity by truncation, computes the arbitrary-degree signed block and its determinant one, and derives a compact finite-order inverse.

**New tangent theorem.** On each finite registered labelled jet chart at fixed gap, the action-jet map has injective differential and a uniformly bounded left inverse on compact positive sets.

## 3. Scalar moving-boundary information

**Active source**

- `article/18_boundary_information_v18.tex`

**Promoted statement.** For a linearly vanishing density at a moving smooth boundary,

`H^2(f_t,f_0) = (I_Sigma/4) t^2 log(1/|t|) + O(t^2)`.

The scalar proof already separates the common-support likelihood calculation from support-exclusive mass.

## 4. Non-dominated vector Gaussian experiment

**Active source**

- `article/18a_vector_boundary_information_v21.tex`

**New proof architecture.** The original local family is not assumed dominated. The parameter-independent collar map with

`q_n = delta_n (log(1/delta_n))^(1/4)`

produces a dominated experiment satisfying

`Delta(E_n^K,Etilde_n^K) <= C_K n p_n q_n^2 = o(1)`.

The likelihood expansion is written only for the collapsed dominated family. Collar covariance, third/fourth score moments, centering, Lindeberg and quadratic-term concentration give compact-uniform LAN. Le Cam comparison transfers the Gaussian shift, bounded-local contiguity, testing profile and local minimax conclusions to the original non-dominated family.

**Additional transfer tool.** The same source proves

`H^2 <= C { epsilon^2 log(e/epsilon) + eta^2 }`

for a defining-function perturbation `epsilon` and amplitude perturbation `eta` in a compact regular linearly vanishing family.

## 5. Registered fixed-window physical endpoint experiment

**Active source**

- `article/18b_raw_physical_multirate_v21.tex`

**Common record space.** The primary statistical family is anchored in one fixed Euclidean chart:

- contact origins and tangent axes are fixed model data;
- the unknowns are gap and graph shape in those fixed axes;
- signed endpoint coordinates are literal laboratory coordinates;
- programmed times are `t_{j,l}=j g_0+d_l` for every local alternative.

The section explicitly overrides the channel-centered derivative convention for the statistical theorem.

**Multirate local coordinate.** `g=g_0+delta_n a/j_n`, `vartheta=delta_n h`.

## 6. Exact-to-ideal boundary experiment transfer

**Active proposition**

- `prop:v21-exact-ideal-transfer` in `article/18b_raw_physical_multirate_v21.tex`.

The exact normalized endpoint density has

`w_ex = w_0 - delta_n U z + R_n`, `||R_n||_{C^2}=r_n=o(delta_n)`,

and amplitude displacement `O(delta_n)`. One record satisfies

`H^2(exact,ideal) <= C { r_n^2 log(e/r_n) + delta_n^2 }`.

At `k_n delta_n^2 log(1/delta_n)->1`, product Hellinger and Le Cam distance tend to zero. This is the quantitative interface between the billiard endpoint law and the abstract vector theorem.

## 7. Finite physical information design

**Active lemma**

- `lem:v20-finite-positive-design` in the v21 physical source.

The information-kernel slice first removes the gap direction. The remaining vanishing action derivative is passed to the v21 differential signed-jet inverse, not to nonlinear injectivity. Compactness gives a finite positive-offset design for every fixed finite labelled jet order; the dependence on that order is stated explicitly.

## 8. Endpoint Gaussian limit and complete stopped transfer

**Endpoint theorem**

- `thm:v20-fixed-window-lan` in the v21 physical source.

The exact potentially non-dominated endpoint-output experiment is at `o(1)` Le Cam distance from a dominated ULAN companion and therefore converges to a Gaussian shift with positive-definite finite-design information.

**Complete transcript theorem**

- `thm:v20-stopped-local-transfer` in the v21 physical source;
- dependencies: `article/17_adaptive_experiments.tex`, `v6/10_experiment_transfer.tex`.

If `k_n tau^{j_n}->0`, the complete actual finite-bridge and boundary stopped transcripts are uniformly close in total variation. Failures, designs and stopping times remain in this comparison. Endpoint-output is then a common coarsening.

**Scope.** The minimax theorem applies to endpoint output. The complete waiting transcript may contain faster information and is not declared ancillary.

## 9. Charged onset/registration calibration

**Active source**

- v21 physical source, with historical input `v5/50_self_calibration.tex` and adaptive-transfer input.

The pilot comparison explicitly retains the same pilot transcript in both experiments and compares post-pilot successful endpoint outputs conditionally on it. The Hellinger stability lemma gives the calibration scale. All pilot preparation cost remains charged.

## 10. Build and source identity

- `ACTIVE_SOURCE_MANIFEST_V21.md` lists the active source graph.
- `CANONICAL_SOURCE_V21.md` identifies the exact canonical entry point despite the historical directory name.
- `.github/workflows/a2-v21-native-build.yml` is the native build/diagnostic workflow for the exact v21 branch.

## Explicit nonclaims retained

V21 does not claim that one local channel determines unrelated obstacles, that unknown registration is free, that the waiting transcript is ancillary, that one finite design identifies an infinite jet, or that classical parameter-dependent-support asymptotics are new. These scope statements do not weaken the promoted local theorems; they specify the observation model on which the stated conclusions are proved.
