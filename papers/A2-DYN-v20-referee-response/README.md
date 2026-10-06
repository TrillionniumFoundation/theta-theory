# A2-DYN revision 20

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

Active article: `main.tex`. Controlling report: the substantive v19 review at `da89f3ae6f0b9e5fedb1ae6aa7a9dcfc20f623aa`, report blob `c41b48727e3b3278f65ea8aed6c861fb0086c88e`. Author baseline: `e56eed31c3b7d70ceb71a7f4b075092c2bd3e98d`, ordinary paper tree `57ea4229c9e344f9d61fd08be6ef7f7954d29feb`.

## New mathematical content

Theorem K and `core/44_direct_orbit_bounds.tex`, `core/45_weighted_spectral_averages.tex` give a direct alternative to concatenating the incompatible grid budgets. A pointwise short-lag Gaussian estimate bounds the Gram matrix of exact orbit vectors. With `m(r)=floor(r^(-200/99))`, its absolute row sum divided by `m` is at most `C r^(2/99)`. Analysis and synthesis of this finite orbit segment then give uncompressed moving mean-square bounds on every later time window, uniformly over the physical radius and every peripheral angle.

On the physical annulus `2 n^(-99/200) <= |z| <= n^(-2/5)`, the same choice has `m<n/4`. For every averaging length `T>=n`, the mean-square bound is `C n^(-4/495)`. Initial weights may be arbitrary square-integrable functions; an unchanged event of probability `p` costs exactly `1/p`. Fixed actual-return marks and actual terminal marks are included. The paper also proves peripheral spectral-arc and exterior Abel-resolvent estimates for the constant vector, and a Cauchy scaling limit for its exact spectral measure. The physical record retains its Gaussian limit.

The scale calculation from the referee is now in the article, not omitted: requiring the displayed grid error to vanish forces `rho^2 Lambda_h` to grow at least like `n^(1/100)` at the lower annular radius. The new direct argument uses no mesh. It proves averaged bounds, not fixed-return power decay or the full raw complementary integral. Those endpoints, the uniform raw derivative/edge bounds, and exact physical-event replacement remain in the original problem.

## Preservation and execution

All 43 inherited core modules remain. Forty-one are byte-identical; the other two receive only an explicit scale pointer and an analytic-unit convergence clarification. Every inherited Python file and all bibliography entries are unchanged. `INHERITED_EDITS.json` records seven exact edits across the introduction and those two modules. All inherited theorem labels are retained.

Run `bash papers/A2-DYN-v20-referee-response/build.sh` from a repository checkout. The verifier checks the frozen v19 tree, complete file hashes, exact edit replay, source inclusions, retained labels, normal/optimized finite diagnostics and all inherited regression routines. The workflow qualifies the committed ordinary source and emits an exact-run receipt. Compilation and finite models are not continuum proof certification.
