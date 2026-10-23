# Working proof dependencies and scope

Draft: /workspace/shared/paper-a2dyn-dot/derived338.tex. It is outside the repository and is not integrated or published.

## Exact native inputs

- core/335_clearance_selected_endpoint_kernel.tex: thm:ce-kernel, eq:ce-kernel, eq:ce-constants. The complete all-flight selected kernel, including the first selected flight, supplies both block estimates. Draft notation C_ce means only the C_end from this specific equation. The unconditioned coordinate density is C_ce times the factor divided by 4 pi; do not use conditioned eq:ce-joint and divide by c_* twice.
- core/315_full_physical_singular_multiplier.tex: definitions of r, Z_m, I_m; lem:sm-intersection, lem:sm-mixed-tail, thm:sm-full-multiplier; the actual deterministic sum of q0^{d_i} is at most 47/3. The draft reconstructs the annular split with two selected constants and optimizes its positive cutoff exactly.
- core/327_length_sensitive_physical_source_transport.tex: eq:lc-theta gives theta_r < 53/59; it fixes the physical constants and complete capacities used in 335. No new physical source family or cutoff is chosen.
- core/323_complete_physical_roof_variation.tex: eq:rbv-constants, eq:rbv-interior-pointwise, eq:rbv-majorant, eq:rbv-domination. These fix C_int, the exact unweighted interior coarea and positive cap domination.
- core/328_localized_clearance_physical_roof_height.tex: eq:lc-selected-roof, eq:lc-boundary-constants, eq:lc-old-boundary, eq:lc-new-boundary, lem:lc-selected-cap, eq:lc-right-endpoint. All outgoing boundary estimates remain unchanged. The visited-grazing zero trace and incoming direction of positive-visited critical endpoints are inherited exactly from thm:lc-selected-roof-height; no critical fan is set to zero.
- eq:cf-exact-mean and invariance, as used in 328, give the original unconditioned mass nu(E_j) <= delta/R.
- core/329_original_normalized_deep_clearance_payment.tex: eq:lc-original-depths, eq:lc-deep-event, eq:lc-log-depth, thm:lc-deep-payment. The same widths and actual union are used. Persistent-source domination is exactly eq:v111-domination, as used in 329. No same-pool or residual definition is changed.

## Reconstruction checkpoints

1. If j < i, use block 0..i, length i, selected index j, rectangle in (p0,pi). The exponent is max(j,i-1-j).
2. If i <= j, use invariance and block i..m, length m-i, selected index j-i, rectangle in (pi,pm). The exponent is max(j-i,m-1-j). The case i=j needs 335's proved first-flight case.
3. Both block exponents are at least d=min(j,m-1-j), while the full disk factor uses L=max(j,m-1-j).
4. With A=C_ce alpha/4 and B=C_ce beta_i/pi, the annular bound is A b^2 + 4B/(t^2 b). Its minimizer is (2B/A)^(1/3)t^(-2/3), giving 3 C_ce pi^(-2/3) alpha^(1/3) beta_i^(2/3) t^(-4/3).
5. The first moment multiplies this tail coefficient to power 3/4 by 4 a_h^(1/4). The weak exponent is exactly 4/3; no strong endpoint moment is asserted.
6. Under theta^d <= delta both factors are at most 2 delta. With a_h <= delta/R_-, the selected Z_m bound is linear in delta. Existing outgoing tails are also at most 2 delta. No endpoint-to-roof substitution is made.
7. For the original guard, rho=theta/q0^(1/4)<1. At a finite D require BOTH 2 epsilon q0^(D/4)<=delta_* and rho^D<=2 epsilon. The union roof height is at most 4 C_lin epsilon q0^(D/4)/(1-q0^(1/4)).
8. At fixed outer B, D_m=ceil(4(2+eta)log(m+1)/|log q0|) eventually meets both conditions. The original m^2 rate follows. The old coefficient is 16 because theta < q0^(1/4) < q0^(1/16).
9. Added cor:sc-linear-moments: under the same finite-count condition theta^d<=delta, the full physical Z_m has selected weak tail at most W_lin^(4/3) delta t^(-4/3), where W_lin=R_-^(1/4)J_lin. Its selected pth moment is at most [4/(4-3p)] R_-^(p-1) J_lin^p delta for 1<p<4/3, and the tail first moment above T is at most 4 W_lin^(4/3) delta T^(-1/3). This proves linear rare-source integrability, not a replacement conditional law. The original conditional version costs c_*^(-1) once.

## Novelty and limitations

The new deduction is the two-selected-block multiplier and its linear-width physical roof consequence. It enlarges the proven paid range by a fourfold reduction of the leading logarithmic boundary-layer coefficient. It does not remove shallow outgoing charges, establish comparison-pool abundance, prove local derivative-charge smallness, or close the raw LLT.

Local-source novelty check: searched current native TeX and retained history text, and read all 660 TeX objects in history/ALL_660_NATIVE_SOURCE_OBJECTS.tar.gz for selected-multiplier, linear-clearance and relevant exponent/kernel phrases. The matching q0^(D/4) bodies were earlier versions of 329's guard-size condition, not linear roof estimates. The one historical delta^(1/2) match was an unrelated modular-integral estimate. Predecessor mechanisms are explicitly credited to 315, 328--329 and 335. This is not a literature-wide priority claim.

The draft has not yet been independently reconstructed or typeset. No repository file was modified by this worker.
