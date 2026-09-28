# A2 v20 proof ledger

**Branch:** `revision/a2-v20-raw-physical-multirate-lan-2026-09-11`  
**Controlling review:** `review/a2-v19-independent-harsh-top4-2026-09-11`  
**Purpose:** identify the exact source of each promoted claim and the scope under which it is proved. This is a navigation ledger, not a proof certificate.

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

**Promoted conclusion**

After normalization by the exponentially small endpoint twist, the finite alternating bridge converges on a fixed offset collar to the half-line action/amplitude product, uniformly with every fixed mixed geometric/offset derivative. No reflection symmetry or finite-horizon hypothesis is added to the general forward theorem.

**Status:** retained from the reviewed chain; no v20 change to the mathematical statement.

## 2. Signed endpoint rigidity

**Active source**

- `article/23a_signed_endpoint_rigidity_v19.tex`

**Dependencies**

- half-line action construction from the relative law;
- historical highest-jet envelope calculation in `article/23_two_contact_rigidity.tex`;
- finite stationary benchmark in `article/29_two_flight_benchmark.tex`.

**Promoted conclusions**

1. The support threshold of the same-type signed endpoint law is `T_b(u,v)=S_b(u)+S_b(v)`.
2. The slice `T_b(u,0)` recovers the unsymmetrized action `S_b`.
3. Onset `g` and `S_b''(0)` recover both contact curvatures.
4. At every degree `n>=3`, the highest new graph jets enter through the block

   `[[coth(n gamma), r_0^n csch(n gamma)], [r_1^n csch(n gamma), coth(n gamma)]]`

   with `r_0 r_1=1` and determinant one.
5. Arbitrary labelled smooth contact jets, odd and even, are recursively determined; analytic germs determine the participating analytic contact germs.

**Scope:** labelled signed contact frames are essential. One local channel does not recover unrelated obstacles.

**Status:** v19 referee found no direct contradiction under the printed fixed-frame hypotheses; retained unchanged in v20.

## 3. Scalar boundary information

**Active source**

- `article/18_boundary_information_v18.tex`

**Promoted conclusion**

For a linearly vanishing density on a moving smooth boundary,

`H^2(f_t,f_0) = (I_Sigma/4) t^2 log(1/|t|) + O(t^2)`.

**Status:** retained.

## 4. Self-contained vector boundary LAN

**Active source**

- `article/18a_vector_boundary_information_v20.tex`

**New explicit lemmas**

- uniform vector collar covariance and third/fourth score moments;
- truncated-score centering and collar mass;
- uniform compact-set likelihood expansion;
- CLT for the central sequence and convergence of the quadratic term.

**Promoted conclusion**

At `n p_n delta_n^2 log(1/delta_n) -> 1`, the thinned moving-support experiment with failure atom is LAN with

`J_Sigma = integral_Sigma a_0 V V^T / |grad w_0| d sigma`.

The theorem gives the Gaussian testing profile, a local central-sequence estimator around the specified reference parameter, and the local asymptotic minimax lower bound first for truncated quadratic losses and then for quadratic loss by monotone convergence/uniform integrability.

**Scope:** the estimator is explicitly local; no global unknown-table implementation is inferred from the abstract theorem alone.

## 5. Fixed-window physical local experiment

**Active source**

- `article/18b_raw_physical_multirate_v20.tex`

**Observation rule**

- registered labelled endpoint coordinates are fixed;
- physical times are fixed at `t_{j,l}=j g_0+d_l` from the reference geometry;
- the local alternative does not change the acquisition times;
- each batch has a deterministic preparation cap and stops at target successes or cap.

**Local scales**

`g=g_0+delta_n a/j_n`, `vartheta=delta_n h`.

Hence the raw fixed-window excess is `d_l-delta_n a` and the full support velocity is

`U_b(u,v)(a,h)=a+D_h S_b(u)+D_h S_b(v)`.

**Finite-design injectivity**

If `(a,h)` lies in every information kernel, the `v=0` support slice and `u->0` force `a=0`; then both action derivatives vanish and the signed-rigidity recursion forces `h=0`. Compactness gives finitely many positive offsets with positive-definite summed information.

**Rate assumptions**

- `k_n delta_n^2 log(1/delta_n) -> 1`;
- `j_n delta_n -> 0` for uniform comparison of rare-event prefactors/costs to the reference geometry;
- design allocations converge to positive weights.

**Status:** new v20 theorem; this is the principal repair of C19-M1 and C19-M2.

## 6. Capped stopping and finite-bridge experiment transfer

**Active sources**

- `article/18b_raw_physical_multirate_v20.tex`
- `article/17_adaptive_experiments.tex`
- `v6/10_experiment_transfer.tex`

**Construction**

Deterministic caps are chosen from a compact-neighborhood lower success-probability bound so that the expected number of successes at the cap is at least twice the target. Chernoff gives exponentially small cap failure.

**Promoted conclusion**

For the complete finite-bridge stopped transcript and the boundary transcript under the identical common policy,

`sup_{z in K} ||P^{fin}_{n,z}-Q^{partial}_{n,z}||_TV <= C k_n tau^{j_n}`.

Thus `k_n tau^{j_n}->0` gives uniform experiment-level transfer on compact local sets, including failures and stopping times. Every common coarsening inherits the bound.

**Important scope:** the endpoint-output LAN is a declared coarsening. Waiting counts may contain additional information and are not claimed to be ancillary. Raw preparation cost remains charged.

**Status:** new theorem-level specialization of the retained adaptive-transfer result; repairs C19-M3.

## 7. Pilot-centered equivalence

**Active sources**

- `article/18b_raw_physical_multirate_v20.tex`
- `v5/50_self_calibration.tex`
- `article/17_adaptive_experiments.tex`

**Condition**

Historical self-calibration gives `j|g_hat-g| <= C r_n^{m+1}`. If

`k_n r_n^{2m+2} log(1/r_n) -> 0`,

then the post-pilot centered endpoint experiment is Hellinger/Le Cam equivalent to the oracle centered experiment. The pilot cost remains

`O(e^{j gamma} r_n^{-(2m+2)} log(1/eta_n))`.

**Status:** new v20 corollary; closes the optional calibration route requested in C19-M1/C19 Blocker 3.

## 8. Fixed-table observation hierarchy

**Active sources**

- `article/19_endpoint_critical.tex`
- retained comparison modules in the auxiliary compendium.

**Promoted conclusion**

Complete records, endpoint-only records and success indicators exhibit distinct finite-versus-boundary scales. This is a fixed-table coarsening comparison and is not used to claim a global unknown-table estimator.

## 9. Literature positioning

**Active narrative**

- `article/01_introduction_v20.tex`
- `LITERATURE_VERIFICATION_V20.md`

The introduction compares information sets directly with marked-length/enriched-length rigidity and explicitly concedes the classical origins of generic nonregular support-dependent asymptotics.

## 10. Explicit nonclaims

V20 does not claim:

- recovery of unrelated obstacles from one selected channel;
- removal of the labelled-frame hypothesis from signed rigidity;
- that absolute Euclidean pose or an unknown frame registration is estimated for free;
- that the waiting transcript is ancillary;
- that the local central-sequence estimator is a global estimator without localization;
- that classical parameter-dependent support or generic nonregular LAN is new;
- successful native compilation until an actual v20 workflow run completes successfully.

## 11. Build status

A v20 workflow is added after all active source changes so that it targets the final revision branch. `VERIFICATION_V20.json` is authoritative only after that workflow is inspected. Source-level consistency documents do not substitute for a native build.
