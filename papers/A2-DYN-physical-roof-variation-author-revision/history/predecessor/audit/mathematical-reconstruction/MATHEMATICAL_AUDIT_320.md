# Mathematical and execution audit: native module 320

## Source identity and exact improvement

`320_all_offset_marked_boundary_turning.tex` is an author proof developed from the complete A2-DYN source at commit `6cdd9ae88cd358d524ecb89092361ac1522ba351`, article tree `a1d21789f9d7c1be801ff4a54d1befad2a47340f`, and the new physical interval-supremum theorem in module 319. It is not an external referee report and does not claim independent expert certification.

The new theorem bounds the complete **regular** fixed-clearance boundary charge by

\[
\mathfrak B^{\rm reg}_{j,u_0}\le C_{\rm ab}
\left((47/59)^j+(47/59)^{m-1-j}\right),
\qquad 0\le u_0\le3/200.
\]

It includes every critical offset, all genuine connected angular overlay pieces, and arbitrarily small positive visited incidences. It does not infer that the nonzero-offset normal speed is uniformly pointwise bounded. The actual integrated variation of the Gauss angle pays the offset contribution.

The mechanism is two precise additions: (1) the absolute derivative bound already proved in 282 gives uniform **total variation**, after integrating its absolute value and summing its geometric contraction; (2) the radial angle of a plane curve has total variation at most its tangent turning plus a universal constant. Module 319 supplies the complete positive sum of inverse optical weights. No word-count factor or independent geometric-pressure premise is inserted.

## Reconstruction of every main step

| Step | Source and calculation | Scope and check |
|---|---|---|
| Original cap | Native 260 proves `|p_0|,|p_m| <= 9/10` on the original initial/terminal section. | This is an inherited implication of the original event. It is not a new restriction. Since `k_0 >= 2`, the cap lies in original `H_0`. |
| Curve arclength | `k_- <= d phi/ds <= U` and the available phi range has length pi. | Every connected unstable graph has length at most `L_0 = pi sqrt(1+U^2)/k_-`; this also bounds a full final-cap image that is not artificially divided into short pieces. |
| Absolute one-step log variation | Native 282 gives `|d log J/d ell_image| <= U/c + D_B`. In `H_k`, `r <= L_h k^-3` and `c >= (2/pi)(k+1)^-2`. | Integrate the **absolute derivative** to get `(2 pi U+D_B) k^2 r <= (2 pi U+D_B)L_h^(2/3)r^(1/3)`. The proof does not infer BV from a Holder endpoint estimate. |
| Full log Jacobian | Native 282's adapted contraction gives `L_i <= Gamma (47/59)^(l-i)L_l`. | The full logarithm is a sum of actual one-step logarithms. Their absolute variations are bounded by a geometric series, with **one** `Gamma^(1/3)`, not an exponentially repeated metric constant. |
| Initial angular density | Native 279 gives `rho = c/(a sqrt(1+V^2))`, `a_s = p+bc/a`, and `|V_s| <= K_0`. | `Var log c` is bounded on each existing initial homogeneous piece. The `a` and `V` terms integrate on the original short piece, using `a >= a_circle`. The grazing factor is retained before the positive family sum. |
| Terminal factor | The exact chain rule is `A_l^p = [c_l V_l/sqrt(1+V_l^2)] J_C(T^(l-1))/rho_C`. | Terminal-cap monotonicity gives one interval and bounded `Var log c_l`. Fixed geometric curvature bounds `|V_s|`, hence the remaining log variation. All intermediate images are exactly the homogeneous ones used in 319. |
| One-hit endpoint case | `A_1^p = kappa a+c`; substitution yields `(A_1^p)_s = c(kappa b-p)/a`. | It is treated directly, without an infinite final homogeneous strip sum. Lower bound `A_1^p >= k_- a_circle` supplies the displayed logarithmic bound. |
| Plane turning | With `alpha=arg P`, `psi=arg P'`, `delta=psi-alpha`, `h(delta)=arccos(cos delta)`, the exact a.e. identity is `|alpha'|=sgn(sin delta)psi'-(h(delta))'`. | The absolutely continuous chain rule covers the triangular function's corners. Because `0 <= h <= pi`, total radial turning is at most tangent turning plus pi. If the curve crosses the origin once, use both punctured sides and add `2 pi`; the missing critical fan is kept separate. |
| Optical tangent turning | Native 317 gives fixed nonzero signs of both endpoint-momentum derivatives. Its tangent slope is `A_+/A_-`; `r/(1+r^2) <= 1/2`. | Each log derivative has variation at most `V_A`, hence tangent turning at most `V_A`. The coordinatewise monotone curve has at most one origin. No minimal interval length, positive momentum cutoff, or number of selector components occurs. |
| Physical normalization | Native 317: `f = W u_x/(4 pi c_* h_x)` and `h_x = R^2 e^T G^-1 e`. Native 260: `G <= Lambda_circle I`. | Therefore `f <= Lambda_circle u_x/(4 pi c_* R_-^2)`. There is exactly one conditioning factor `c_*`, and the `R_-^2` comes from `h_x`, independently of the marked-source factor already present in 319's inverse-weight bound. |
| Complete positive sum | Module 319: `sum_actual_overlaps sup u_x <= (607/90) H_nm (94/sqrt(1827)) [sigma^j+sigma^(m-1-j)]`. | Use the supremum only on each genuine physical piece. Countable exhaustion follows after finite compact regular subfamilies. Both signs are already in `H_nm`; no duplicate sign or word multiplier appears. |
| Deep-source summation | Sum over `D <= j <= m-1-D`. | The two endpoint series give `2 C_ab sigma^D/(1-sigma)`; an empty range contributes zero. At `D=ceil(theta_* m)`, `m^2 sigma^D -> 0` for fixed `0<theta_*<1/2`. |

## Boundary, selector, and limit audit

- All local integrations use actual regular physical branches and then compact exhaustion. At original `u_0=0`, the source is the already proved positive-`u` trace. The mark is an unvisited disk and introduces no collision or physical time increment.
- Exact return, displacement, collision, section, roof, and original guard tests remain nonnegative selectors bounded by one. They are neither differentiated nor converted into extra branch counts.
- Artificial chart seams are assigned once. An actual critical origin is punctured for the regular boundary measure; its incoming fan is not assigned zero. Separate visited-grazing, section, and pairing trace measures are not claimed to be included by area-nullness.
- No positive lower bound on an interior incidence is imposed. The actual homogeneous strips and uniform curvature class control its logarithmic contribution.
- The theorem is uniform in every prescribed clearance level, physical radius, exact label, and collision count. It first proves the complete finite-count positive estimate and only then permits these suprema.
- The only vanishing assertion in 320 is the complete deep regular-boundary **total charge** at a linearly increasing original collision depth. Its pushforward by the actual roof has bounded total variation. No total-variation-to-roof-essential-height implication is used.
- The original fixed outer widths, collision limsup, subsequent outer limit, `m^2` normalization, and four-coordinate raw inversion target are unchanged. Shallow positive source, incoming critical fans, other singular measures, same-roof height/comparison capacity, arithmetic, spectral, pairing, and conditional-denominator inputs retain their exact obligations.

## Executed finite mathematical checks

`check_all_offset_boundary.py` has no Python `assert` statements. Every failed check raises an explicit exception, so optimization cannot erase its acceptance conditions. Two real executions completed:

1. Ordinary Python 3.12.14: `ALL_OFFSET_CHECKS.json`, UTC `2026-10-20T01:43:26.021101+00:00`.
2. Python 3.12.14 with `-O`: `ALL_OFFSET_CHECKS_OPTIMIZED.json`, UTC `2026-10-20T01:47:43.306471+00:00`.

Both passed **49,128** finite checks: rational identities for the physical first-hit derivative; positivity; the tangent logarithmic sensitivity and its exact nonnegative defect; the two-dimensional cofactor and inverse metric normalization; the turning differential identity; the complete finite depth sums, including empty ranges; and the exact family constants. Five explicitly marked affine-offset illustrations show concentration of the pointwise turning density with bounded total turning. They are normal-form illustrations and are not Lorentz-gas data.

Source SHA-256: `a1da0d46bae1f7553ae4fd2927e076b311e5edff464838748c5fba0dfb720737`.

Checker SHA-256: `741d3a77f1fc994389a0b8dddac2933a6a5c50b211f7861bd30fde12f0cadbab`.

These executions are finite algebra diagnostics. The continuum claims depend on the full native proof bodies and their stated geometric hypotheses; no script, CI status, or compilation is used as their proof. Module-level compilation is to be recorded by the integrating author build, not claimed in these standalone execution records.
