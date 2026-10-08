# A2-DYN, revision 44

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The complete article is `main.tex`. The author baseline is v43 at `f3fb2858b2c10aa2f4f857d56132491a5ea25861`. The controlling report is the v43 report at `0418466ec7a126b032e64cc8c54238770104cf68`, blob `6d223bd63ddd76a5a2efc3351c475d0261e93839`. This revision preserves the original physical family, actual-return record, raw arithmetic endpoint and all 93 inherited core modules.

## New results

`core/94_complete_density_bounds.tex` proves a uniform exponential height bound for the full collision roof density and all bounded measurable actual-return restrictions. It uses positive endpoint action curvature, bounded-degree auxiliary collision graphs and coarea; it does not remove grazing neighborhoods or infer a density bound from discarded mass.

`core/95_jump_cusp_separation.tex` excludes all divergent physical density germs, proves finite-count BV regularity, and separates intrinsic jumps from continuous positive-exponent singularities. The latter have an arbitrarily prescribed summed supremum budget, while keeping their coefficients unchanged. The associated signed smoothing error is quantitatively negligible at the central local scale. The remaining jump and residual inverses are not declared small.

The full signed correction `m^2 D_B`, the complete pointwise arithmetic raw LLT, useful long-time second-derivative/bandwidth bounds and arbitrary weighted pointwise conditioning are not proved by this revision. The exact arithmetic transition kernel and fixed-radius residues remain in the target.

## Reading and reproducibility

Read the new introductory paragraph, modules 94--95, and `RESPONSE_TO_REFEREE.md` for the direct response to the latest report. `SPECIALIST_AUDIT_MAP.md` identifies the additional continuum checks. `build.sh` verifies the frozen source tree, all inherited modules/scripts, exact manifest, reference closure and normal/optimized diagnostics before compiling the whole article. The read-only GitHub workflow builds and renders the exact event SHA separately on the response and referee-copy branches. Only dynamic receipts identify actual completed executions.
