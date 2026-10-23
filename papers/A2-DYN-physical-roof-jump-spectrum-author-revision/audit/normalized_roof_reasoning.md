# Independent author-proof audit: the physical SBV and jump-spectrum continuation

This is an author-revision research record, not a referee report. It records what the new proof establishes, what is inherited, and the checks performed on native drafts 336 and 337. It does not certify the original normalized raw pointwise local limit theorem as complete.

## Frozen source and actual scope

The baseline is the full native article at commit `d6c3c6754fb3a1b4ad3eea8e6dcc51642e312b28`, directory `papers/A2-DYN-section-multipliers-exact-inversion-author-revision`, article tree `381d0aa576a93d874bf974b0edcf090378aaa41b`. The proof uses its original triangular billiard, actual first-hit flight, all collision words, original section, collision count `m`, real roof `L_m`, exact occupation/displacement labels, and conditioned source with exactly one factor `c_*^{-1}`.

Native336 uses the whole observation class already paid in native332: `w=1` or the original smooth guard `W^epsilon`, bounded complex `C^1` endpoint functions, and the exponential of the sum of real `C^1` observations along the actual finite collision chain. No analyticity or definability of those observation functions is added. The guard width is fixed when a bound involving its derivative norm is used. An arbitrary discontinuous Borel trajectory selector is outside this derivative theorem.

## Historical novelty audit

The complete archive was searched, not just the currently included source files. Blob-to-native-name identities come from `baseline/audit/NATIVE_SOURCE_CONTENT_IDENTITIES.json`.

| Historical result | Native source / exact preserved identity | Consequence for the new claim |
| --- | --- | --- |
| Finite first-hit semialgebraic physical graph, exact moving section and least third-disk clearance | native164, `164_explicit_tame_physical_graph.tex`, blob `b89eeee9d3af96ae495f29f00cdf3ac69e7d04d6`; first source commit `0933e9b44f5b0fd1d1a624d37ffd881d352496f8` | Inherited input, not a new finite-geometry theorem. |
| Finite-count analytic/power-log singular germ preparation | native40, blob `1366315e736816336979d1670f4c6041b353fa74`; native92, blob `5d51041a82313d8a637a5b35e34faf16f715e26c`; native93 | The older constructible scalar subclass already has finite analytic preparation. Combined with retained BV, that subclass cannot have a Cantor derivative. Native336 explicitly acknowledges this. |
| Signed projected physical boundary current on selected Morse charts, including coincident-interface combination | native153, `153_signed_radial_boundary_current.tex`, blob `a6a0fcfcd97fee51a0cbd1c9030082b71831dc5b` | The signed-current principle is inherited too. New336 extends to the whole current smooth observation class and complete physical source; it does not claim the principle anew. |
| Reversing periodic critical orbit, optical Hessian and monodromy coefficient | current native275, `275_critical_roofs_reversibility_and_stability.tex`; related native285 | The self-retracing `2m`-periodic orbit, determinant coefficient and critical-orbit identities are not new contributions. |
| Directed/Jordan and paired-flux local charges | native162, blob `403ac23fe35c7c44610c854f8275f7639918682c`; native165, blob `d9b1c9d3b63d8e0094e70bc72d6f2b0d828cc6af`; native176, blob `7b291428cf38455404fae326651a986b1697cf97` | Merely replacing total variation by a directed charge or a paired short-excursion charge would repackage old work. |
| Prior mean-square averaging | native45, blob `67fb87fc5b6ad38d8fa2d679fc12b75312f2f3b1` | This is an average of return-count/unitary correlations, not the full marked roof-frequency squared-jump identity. The new invariant is distinct. |
| Complete physical scalar and all-label BV; smooth tests; exact finite-interval inversion | current native323–325,330,332–334 | Inherited proof inputs; none is relabeled as newly established. |

The new content is the full signed physical derivative formula for the entire current smooth observation class, its geometry-only finite atomic support, exact critical and constant-roof-side coefficients, and its transfer to the exact full-three-torus roof-frequency invariant. Scalar fixed-count tameness alone is not advertised as a breakthrough.

## Native336: geometric and measure-theoretic checks

### Complete finite geometry

The finite word graph uses actual collision contact points, normals, velocities and positive flight lengths. Its polynomial equations retain reflection and the first-hit inequalities against every relevant obstacle. The nearest-third-disk list is finite for the original physical horizon, rather than imposed as a model restriction. All original section cuts are inserted before any observation weight. Fixed real angular constants are legitimate coefficients of semialgebraic descriptions.

The geometric lemma works **fiberwise at each fixed radius**. An ambient closure in `(R,r,t)` is insufficient: it could create a spurious two-dimensional limiting fiber at an exceptional radius. The final proof instead defines the closure by a quantified same-radius neighborhood formula, then uses semialgebraic quantifier elimination. At each radius the regular image is open in its two roof/Gauss variables, so the actual boundary has dimension at most one. A finite cylindrical decomposition includes exceptional radius cells.

Each nonvertical genuine side is subdivided until its roof is either constant or has derivative of fixed nonzero sign in a rational Gauss-angle parameter. A constant Gauss-angle side has zero angular flux. Finite point cells have zero regular angular flux. Positive-visited critical fans are retained separately; they are never dismissed on the ground that their original collision-area measure is zero. Positive endpoint Hessian makes such critical points isolated, and their fixed-radius semialgebraic family is finite. This does not require an extra claim that every global physical word has only one critical point.

Artificial seams and cuts cancel between their incident copies before the signed source is formed. Coincident genuine constraints describe one interface with its actual incident traces. The complete actual section/record label partition is used throughout. No incidence cutoff or changed collision/event definition appears.

### Exact regular side coefficient

In a rational Gauss-angle coordinate, `dtheta=2 dr/(1+r^2)` up to orientation. If `C^-` and `C^+` denote traces immediately below and above the genuine roof side, the distributional derivative coefficient is `(C^+ - C^-) |dtheta/dr| dr`. Thus entrances and exits have opposite signs. A physical exterior trace is zero. Multiplication by the smooth test is taken before this signed difference.

For a monotone `C^1` side map `t=gamma(r)`, the pushforward density is

`b(gamma^{-1}(t)) / |gamma'(gamma^{-1}(t))|`.

Its `L^1` norm equals the `L^1` norm of `b`. The proof exhausts open parameter intervals by compact subintervals, so it does not assume an artificial uniform lower derivative bound at the endpoints. An isolated turning point carries no `b(r) dr` mass. A derivative vanishing at an endpoint can create an unbounded integrable density, but does not create a singular-continuous pushforward.

For a constant-roof side, the pushforward is instead exactly `integral b dr` times the point mass at its roof. Such sides must not be omitted without a physical exclusion theorem. Positivity of the endpoint Hessian by itself does not exclude all constant-roof section-side arcs.

### Exact critical coefficient and completeness

For a one-copy positive-visited critical germ `x`, the retained physical sector formula gives

`c_{ell,x} = w_x V_x * omega(x)/(2 c_* sqrt(det G_x)) * beta_{ell,y}(x)`.

The tangent sector is measured in `y=G_x^(1/2)(q-q_x)`, includes the actual original endpoint memberships and exact label, and is computed before any artificial partition is squared or made positive. The `C^1` tests have actual one-sided finite-chain limits. All incidences are those of the real branch. A visited-grazing critical limit uses the inherited zero optical trace at its proved scope, not collision-area nullness.

Every critical coefficient and every constant-roof side charge at the **same label and same real roof** is combined with its sign. Labels with different arithmetic records remain distinct. The formula can exhibit genuine cancellation and can also have a zero resulting atom.

The complete native332 integration-by-parts identity has a finite positive source budget, not only a bound on the final canceled derivative. Its interior derivative is absolutely integrable, including the already paid inverse-gradient factor for the new smooth observations. Fubini gives an `L^1` roof density for that part. The finite regular side decomposition gives only `L^1` densities and atoms. The retained critical incoming sources give atoms. The inherited endpoint/section classification is exhaustive, hence no Cantor component remains.

The equality

`sum_ell ( ||d_ell||_1 + sum_u |a_ell(u)| ) = sum_ell ||D f_ell||_TV`

is exact because the AC and atomic measures are mutually singular, including for complex tests. The inherited all-label bound is used after same-roof cancellation. No count of labels multiplies it. Finite atomic support is uniform in radius only at fixed collision count; no bound on its collision growth or minimum separation is asserted.

The canonical primitive of the derivative is fixed using a point to the left of the compact physical support. Its left and right traces differ by the exact atomic coefficient. This proves the trace statement without treating an arbitrary pointwise representative of an `L^1` density as canonical.

## Native337: independent formula audit

The entire draft was checked independently, including the following signs and constants.

1. With transform `hat f(s)=integral exp(i s t) f(t) dt`, distributional integration by parts gives `hat{Df}(s)=-i s hat f(s)`. Therefore `-i s F=A+G` and `s F-i A=i G`; the displayed signs are correct, including the zero-frequency mass identity.
2. The exact finite torus is three-dimensional: two displacement labels and one occupation label, at the fixed collision count. Its Haar normalization is `(2 pi)^-3`. Orthogonality is applied before roof averaging, so no label-count factor is produced.
3. Each coincident `(label,roof)` coefficient is combined before squaring. The distinct-roof cross average is exactly `sin(S(u-v))/(S(u-v))`. An ordered cross sum is appropriate for the expansion of the squared modulus; no factor one-half is missing.
4. The cross bound `min(1,1/(S|u-v|))` and the mixed bound `2 D sqrt(Q_S)` are correct. `sum |hat d_ell(s)|^2 <= D^2`, so the Cesaro term tends to zero at fixed `m,R` by the elementary Riemann–Lebesgue proof supplied in the text.
5. Distinct roofs may coalesce with radius. The exact interval example has atomic energy two and finite-frequency energy `2-2 sin(S delta)/(S delta)`, proving that no uniform radius or collision-limit interchange follows from bounded variation alone.
6. The central cutoff derivative has the bound `2 M_1 ||psi'||_infinity / sqrt(m)`. The product rule adds the continuous measure `(chi d + chi' p) dt` and multiplies every jump by the continuous value `chi(u)`. Its all-label variation bound follows from `sum ||p||_1<=1`.
7. The central cutoff family is not literally an endpoint test of native332. Its spectrum follows by reusing the proof of the Fourier theorem on this explicit product-rule decomposition. The root was asked to make that logical scope explicit.
8. At a roof where the cutoff is nonzero, the roof lies in the interior of the larger original central interval. Approaching from Lebesgue points on both sides and using continuity of the complete arithmetic reference gives `m^2 |jump| <= 2 E_m(M_1)`. Squaring uses the global unscaled `l^1` variation budget once, giving `sup_R m^2 J^chi <= 2 D_0 E_m(M_1)`. No illicit essential-supremum or radius-null-set interchange occurs.
9. The already paid zero-clearance critical fan source has an all-label `l^1` bound because exact-label sectors partition each actual physical fan. The once-only assignment of multiple witnesses is bounded by the full positive witness sum. It is not an extra model selection. The resulting estimate `B_m=A_V C_pc m sigma^((m-1)/2)` has one conditioning factor inherited in `C_pc`.
10. For complex atomic vectors, `abs(||a||_2^2-||a-b||_2^2) <= 2 ||a||_2 ||b||_2+||b||_2^2 <= 2 D B_m+B_m^2`. This correctly retains all coincident-roof cross terms and can be centrally cut off without increasing either norm bound.

## What remains unresolved

The new finite-count structure and frequency identity do not prove uniform decay of the normalized central jump spectrum, positive-clearance critical sources, constant-roof side charges, or the continuous local derivative charge. Smooth narrow spikes can have no jumps at all, so vanishing atomic energy is only a necessary condition for the raw theorem.

The full original shortage in native329 remains open on that route. The alternative bridge in native334 still requires the complete normalized local derivative charge in its original order of limits. The new frequency limit is taken only at fixed collision count and radius. The complete microscopic pointwise estimate, actual conditional denominator bounds, and long-time four-coordinate inverse Jacobian are not replaced by this Fourier identity or by a weak transform estimate.

No finite script or finite-frequency sample can certify the absence of a Cantor source, the all-word continuum source accounting, or the original limiting theorem. Those assertions rely on the explicit proof above and its retained geometric inputs. Scripts may verify algebraic signs, sinc coefficients and elementary negative controls only.
