# A2-DYN revision 45

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

Complete article: `main.tex`. Immediate baseline: v44 at `848582734b94a6cda2d27484be2d6dcf646744a4`. Controlling external report: v43 at `0418466ec7a126b032e64cc8c54238770104cf68`; report blob `6d223bd63ddd76a5a2efc3351c475d0261e93839`. The v43 report remains the latest external report located for this revision; v44 is the intervening author response, not a new external review.

## New pointwise estimate

Theorem 8 and modules 96--97 prove deconcentration of intrinsic regular critical edge clusters at the original exact labels. Endpoint influence permits margins `epsilon (47/53)^(distance-to-endpoints/4)` rather than a fixed interior margin. A physical endpoint collar of radius `r_* epsilon^3` has a relative density distortion bounded by `e`; its roof width is `h_* epsilon^6`, independently of collision count. A positive two-endpoint local estimate then gives

`limsup_m sup_(R,n,k,t) m^2 J^epsilon([t-h,t+h]) <= C h`.

Every coalescing atom is consequently `o(m^(-2))`. The entire original positive source in any shrinking collection of these critical collars has density `o(m^(-2))` in essential supremum, including after arbitrary bounded measurable insertions. Its signed smoothing correction is negligible uniformly over all roof bandwidths. No unproved growing-band spectral estimate or coefficient cancellation is used.

The protection parameter is fixed before the collision-count limit. Critical words failing that envelope and the remaining noncritical signed inverse are still to be controlled. The full arithmetic raw-density theorem is not certified by this partial estimate.

## Preservation and entry points

All 95 inherited core modules, 115 inherited Python scripts, the bibliography, and the compiled A--X synopsis are byte-identical. The v44 front matter and supporting records are preserved under `provenance/`. The new response follows report items 17.1--17.9; `CRITICAL_CLUSTER_INPUT_MAP.md` lists the exact proof dependencies. `SPECIALIST_AUDIT_MAP.md` records the continuum questions for independent review.

Run `bash papers/A2-DYN-v45-referee-response/build.sh`. The exact-SHA workflow checks ordinary Git source, the complete inherited corpus, labels, finite regressions in normal and optimized Python, native TeX and proof-page renders. Its receipt, not this static README, identifies successful execution and the actual PDF hash. No independent human proof audit is claimed.
