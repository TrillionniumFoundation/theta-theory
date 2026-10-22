# Independent author reconstruction of native 316

This is an internal reconstruction of the author's mathematical proof, not a new referee report or an independent journal decision. The source read for this reconstruction is `core/316_marked_clearance_momentum_and_trace.tex` in the new marked boundary-source article: 16,238 bytes, SHA256 `cb307ab780f56011e9729a7e58f64c2943da88ec2b6153263c668934d0b852c6`.

**Conclusion:** the momentum kernel, marked joint estimate, incidence moments and stated one-sided trace follow from the cited native source and growth theorems. The argument retains the actual collision count, actual physical roof, complete original event and one conditional normalization. No whole-cylinder pressure premise, independence assumption, common exceptional set across radii, or unproved inverse-incidence payment is inserted. One minor phrase should be made explicit: a roof restriction preserving the same right-hand side is an indicator or a selector with values in `[0,1]`; an arbitrary bounded multiplier incurs its supremum norm. This is a statement-precision issue, not a change in the underlying theorem.

## Exact sources read

All paths below are relative to the new article. Each is a retained native body except 316; their identities are recorded to delimit the reconstruction.

| Source | SHA256 |
|---|---|
| `model.tex` | `7ca3c885023e7e08e62e0aa16696336840b4b0ac271f9d5b105c4aba88406bb8` |
| `core/270_exact_clearance_flux.tex` | `66ebe59f8e0a9696ef2c2bafbad054ba715a02966a400d0edd583e04dcabc8d4` |
| `core/273_record_disintegration_and_bridge.tex` | `02da67a1053cc7407686e0ca9642537fa7ed1827c8204794ac15dbec58679c12` |
| `core/277_cross_flight_clearance_jacobi.tex` | `0d6387b3b58b4bfa5e7c152e886529a2117165e6b7148c2dcb7f43e96d5625af` |
| `core/279_angular_source_homogeneous_budget.tex` | `48e39ae1faf359b127e8587e64b9865c420a70328a05c936589f6e9f5934ea90` |
| `core/281_uniform_curvature_graph_transform.tex` | `28a8ccf451caad3b22c6c50cad319fb6f0cb5a7127ae2b1f8fc30b12c723fe21` |
| `core/282_physical_complexity_and_distortion.tex` | `b82876b8522552f2b14bbf29702d6ef83977f050703ce02c8affaff55b4d786c` |
| `core/283_admissible_growth_and_clearance_consequences.tex` | `71748a69d7c44e9e145c48e8d3aa8715ea382bffff9ad95e4020b44badb4e403` |
| `core/284_physical_momentum_fibres.tex` | `b0bb3aa89040ef29d0354f6c1b974b12cc0d92519e1282e00d8119ac3700d320` |

The finite original section formula was also checked against historical native164 and the retained v85 main source. It agrees with the active `model.tex`: four moving open squares and the specified open rectangle `U`, with mass `c_*=91/(10000π)`.

## 1. Simultaneous quantifiers and the physical source

The radius is any fixed member of `[9/20,47/100]`, the speed is one, and the signed marked line is based at

\[
q_f=-\sigma(R+u)v_\vartheta^\perp,
\qquad \sigma\in\{-1,1\},\quad 0<u\le3/200.
\]

The foot is strictly outside every disk when `u>0`. For any other center, its distance from the foot is at least `1−R−u>R`; the marked line misses the marked disk by construction. Both adjacent collisions are genuine first physical hits. The foot causes no reflection, no occupation increment and no reset of the physical clock.

Native277's standoff is uniform for either adjacent collision:

\[
a^2\ge(1-R_+)^2-(R_++\delta_*)^2
=\frac{1827}{40000},\qquad
a_\circ=\frac{\sqrt{1827}}{200}>\tau_-=\frac3{50}.
\]

The comparison uses the endpoint-to-marked-center distance and the actual perpendicular foot. It does not substitute a whole line for the event on the physical segment. The same strict lower bound remains valid at the one-sided limit `u=0`.

The constants `M_*`, `A_*`, `C_g` and `J_f` have their original meanings. In particular `A_*` already sums **both** impact signs, `C_g` is the growth constant for the original angular-source graph class, and `J_f=2N_f+1` counts physical next-hit branches on a sufficiently short graph. This is not the enlarged initial-momentum-fibre class of native284.

## 2. The first incidence cancels in the true first-image derivative

Native279 gives, with actual arclength `s`, incidence `c=cosφ` and `p=sinφ`,

\[
\frac{ds}{d\vartheta}=-\frac ac,
\qquad V=\frac{d\varphi}{ds}=\kappa+\frac ca,
\qquad \rho=\left|\frac{d\vartheta}{d\ell}\right|
=\frac{c}{a\sqrt{1+V^2}}.
\]

Therefore

\[
\frac{dP_1^+}{d\vartheta}
=cV\frac{ds}{d\vartheta}=-(\kappa a+c),
\qquad |\partial_\vartheta P_1^+|\ge k_-a_\circ.
\]

The factor `c` is multiplied before any estimate. The resulting lower derivative bound has no reciprocal incidence. Native279 provides at most `M_*=8N_*+1` injective, seam-free physical first-hit intervals for each sign. Momentum is strictly monotone on each. Summing the one-dimensional inverse derivative over both signs consequently costs exactly `2M_*/(k_-a_∘)`.

No terminal homogeneous subdivision is needed for this `l=1` calculation. At this stage an angular coordinate seam is a bookkeeping cut, not an additional physical initial point or an extra root.

## 3. The later kernel uses exactly `l−2` intermediate collisions

For `l≥2`, first push the angular source to the outgoing state at the **first** actual collision. Its source-labelled decomposition has

\[
\sum_C\|\rho_C\|_\infty\le A_*.
\]

The first-image slopes and geometric curvature satisfy precisely the class verified by native281. Its homogeneous restrictions and short subdivisions remain in that class. Thus native283 applies with its original `C_g`; using the enlarged momentum-fibre allowance and then silently reusing the smaller class's constant is unnecessary and does not occur.

Propagating a first-image curve through `l−2` further collisions puts its image at collision `l−1`. The sum of the density supremum bounds on the resulting short curves is at most `C_g‖ρ_C‖∞`. Exactly one physical collision remains. This includes `l=2`: the intermediate map is the identity and the growth sum is one, already bounded by `C_g`.

On the last incoming graph, native281's exact transform gives, with `d=c_next`, `w=κ+V` and `A=c+τw`,

\[
\left|\frac{dp_{\rm next}}{d\ell}\right|
=\frac{\kappa A+dw}{\sqrt{1+V^2}}
\ge\kappa\tau\frac{w}{\sqrt{1+V^2}}
\ge k_-\tau_-.
\]

The last inequality follows from `(κ+V)²−(1+V²)=κ²+2κV−1>0`, since `V≥κ>1`. The exact lower constant is `k_-τ_-=6/47`. The small terminal incidence `d` has cancelled in the differential; it is not dropped from an inequality.

The short length fixed in native283 includes the preliminary geometric scale of native282. Hence there are at most `J_f` physical next-hit branches, each strictly monotone in terminal momentum. Their direct coarea costs `J_f/(k_-τ_-)`. No infinite terminal strip count is introduced. Tonelli summation over all intermediate pieces and all first-image labels proves the second constant

\[
\frac{A_*C_gJ_f}{k_-\tau_-}.
\]

The maximum of the first and later constants is therefore the printed `H_nm`. There is no extra factor two after `A_*`, no word count, and no factor growing with `l`.

## 4. Singular coverage, every regular root value and time reversal

Native279's discarded first-hit tangencies and seams are finite, and its homogeneity boundaries have countably many preimages. Native283 checks at each actual forward step that a short unstable graph has finitely many physical tangency cuts, that a regular image has strictly monotone collision angle, and that the subsequent homogeneous and short-length cuts are countable. Its graph maps are regular and injective on every retained restriction. The absolutely continuous labelled source therefore pulls all these omitted points back to an angular-null set for each finite collision count. This is a fibre argument; it does not infer an angular trace statement from a two-dimensional null set.

The final momentum derivative is nonzero on every regular original branch because the first-image derivative, regular tangent propagation and last-collision derivative are nonzero. Coarea gives the root-density bound for almost every target momentum. To reach every `v_0∈(−1,1)`, take an arbitrary finite collection of distinct regular roots, with disjoint local source arcs. The inverse branches exist on a common neighborhood of `v_0`, and their positive inverse derivatives are continuous there. Their finite sum is bounded almost everywhere by the complete density bound, so continuity gives the same bound at `v_0`. Taking the supremum over all finite root collections proves the full nonnegative series bound. This also handles true roots lying on artificial cuts; those cuts do not duplicate the root.

The reversal of the marked line is exactly

\[
(\vartheta,\sigma,u)\mapsto(\vartheta+\pi,-\sigma,u).
\]

It keeps the physical foot fixed and reverses the direction. The outgoing collision momentum in the reversed record is the negative of the original forward momentum, so `P_l^−=−P_l^+` after this parameter change. Angular measure, the two-sign sum, and the length of a Borel momentum set are preserved. The original selector is transported through that bijection. The proof does not replace the original section by its reflected section or assume the section is reversal invariant.

## 5. Full record indices and the single physical normalization

For a mark on original flight `j`, the first backward collision is collision `j`, and the first forward collision is collision `j+1`. Thus the two exact counts are

\[
l=j-i+1\quad(i\le j),\qquad l=i-j\quad(i\ge j+1).
\]

They are positive at every contact index `0≤i≤m`, including `j=0`, `j=m−1`, `i=0` and `i=m`. The full `m`-flight record has `m+1` contacts; the source's two sides together recover exactly those contacts without treating the foot as an additional collision.

Native270 supplies the one-copy marked flux. In the original collision coordinates,

\[
\left|\det D_{(\alpha,p)}(\vartheta,b)\right|=R,
\qquad d\nu=\frac{d\vartheta\,db}{4\pi R}.
\]

Both signs have `|db|=du`. The inverse correspondence is between a physical flight with a distinct marked nonincident disk and its line relative to that marked center. Different near misses on one flight remain different marked copies. Original exact labels and the lifted displacement relative to the initial collision remain inside the transported selector.

Since the original event is a subset of `Y_R^*`, replacing `dν_R^*` by `c_*^{-1}dν` inside the event is exact. It is the invariant **unconditional collision area** `ν`, rather than the conditional measure, which is shifted by `T_R^j`. The resulting prefactor is exactly `1/(4π R c_*)`. The momentum kernel is an angular estimate, not a probability normalization; neither another `R` nor another `c_*` appears.

Applying the kernel on each clearance fibre and integrating over a Borel set `E` gives

\[
\int h\mathbf1_\Pi N_E(T_R^jx)\mathbf1_{\{p_i\in I\}}\,d\nu_R^*
\le\frac{H_{\rm nm}}{4\pi R c_*}|E|\,|I|.
\]

This is domination of a marked positive measure. It does not imply any independence between incidence, return, displacement, collision count or roof. A roof indicator or a `[0,1]` roof selector can be included without changing the constant. For a general bounded nonnegative roof multiplier `g`, the corresponding immediate statement has an additional `‖g‖∞` factor. The phrase “any bounded Borel original-roof restriction” should be read in this precise selector sense, or clarified accordingly.

## 6. The original interior incidence load and its moments

The load remains

\[
I_m=1+\sum_{i=1}^{m-1}\frac{q_0^{\min(i,m-i)}}{c_i},
\qquad q_0=47/53.
\]

In particular the new proof does not silently add either endpoint incidence to this definition. At `m=1` the sum is empty and `I_m=1`. The safe finite bound on the total weights is `Σ_i w_i≤2/(1−q_0)`, so the printed constant is `W_0=1+2/(1−q_0)=56/3`.

For `γ≥1`, Jensen's inequality with the additional weight one for the constant term gives exactly

\[
I_m^\gamma\le
(1+\textstyle\sum_iw_i)^{\gamma-1}
(1+\textstyle\sum_iw_ic_i^{-\gamma}).
\]

The momentum kernel and monotone approximation bound every incidence integral on a complete angular fibre by `H_nm J_γ`, where

\[
J_\gamma=\int_{-1}^1(1-v^2)^{-\gamma/2}\,dv.
\]

Under the required convexity range `γ≥1`, the upper integrability threshold is exactly `γ<2`. For example `1−v²≥1−|v|` yields the explicit sufficient bound `J_γ≤4/(2−γ)`. No such moment at `γ=2` is asserted. The constant angular mass is exactly `4π`, and integrating the displayed Jensen bound therefore gives the native `W_0^{γ−1}B_γ`.

The grazing set has momentum length

\[
2(1-\sqrt{1-\eta^2})\le2\eta^2,
\qquad 0<\eta\le1.
\]

Substitution into the marked joint estimate proves the printed factor `H_nm δ η²/(2π R c_*)`. Finally, summing nonnegative marked measures against `b_j≥0` replaces `δ` by `Σ_j b_jδ_j`; this requires neither disjoint marked events nor separated flights. All shallow flights are included.

## 7. The zero-clearance family is an actual one-sided strict-record limit

At `u=0` the foot lies on the marked circle. Its distance from every other center is at least `1−R≥1−R_+>R_+`. Both tangent half-rays avoid the interior of the marked disk. The uniform horizon supplies a true nonmarked hit in either direction. The first-hit exceptional angles are finite by the same candidate equations as native279; away from those angles, the first contacts have positive incidence and the standoff above remains strict.

Consequently each one-sided first-image family has the same exact derivative, density decay and curvature bounds as the `u>0` family. Its source remains in the original admissible class with the same `A_*`. For the forward portion use the ordinary future dynamics after the first forward hit. For the backward portion reverse the line first, then use the corresponding ordinary future dynamics of that reversed first-hit source. This avoids applying the undefined ordinary collision map through the prescribed tangent foot.

After those first true hits, the marked disk is an ordinary possible next scatterer. It is not erased from the table. Any later tangency with it, or with any other disk, is among the forward singular cuts in the appropriate original or reversed growth family. A finite iteration removes only a countable angular-null set. The finite record remaining outside that set has strictly positive visited incidences and no other nonincident tangency.

The latter assertion supplies the required visibility stability. Each finite physical segment has only finitely many candidate disks; every nonincident candidate has positive clearance except the designated original tangent foot. The minimum of those finitely many positive clearances is positive for this particular finite record. The first-entry root at a positive incidence depends analytically on its incoming state, and no earlier disk can appear under a sufficiently small perturbation. Inducting through the finite forward and reversed words gives a one-sided neighborhood in `u` with the same entire actual word. The marked flight itself misses its marked disk for all `u>0` because its exact prescribed impact is `R+u`.

The neighborhood is allowed to depend on the radius, angle, sign and full finite word. No uniform neighborhood size over all words or collision counts is inferred. The source at `u=0` is a strict-record limit: it does not assign a new collision-map value at the foot, insert a reflection there, or delete a collision of any positive-clearance trajectory.

## 8. Every finite original section and roof-interval test has its stated limit

At fixed radius the five original section rectangles have fixed endpoints. A local circular lift makes each membership test a finite Boolean combination of inequalities in analytic `α_i(u)` and `p_i(u)`. Equivalently, an angular membership test can use the analytic contact normal through `n_i(u)·n_center>cos h`, which handles a coordinate seam without any artificial discontinuity. The lifted center word is constant, so the integer displacement is constant.

For a real-analytic scalar function at zero, either all Taylor coefficients vanish and it is identically zero locally, or its first nonzero Taylor coefficient determines its sign on a sufficiently small positive interval. Each original strict or nonstrict section inequality consequently has a one-sided indicator limit. The occupation sum uses exactly `i=0,…,m−1`, while the terminal membership at `i=m` remains separate. Taking the finite Boolean combination for the original event therefore preserves all its exact labels and its initial/terminal conventions.

The physical roof is the sum of the same `m` actual flight lengths and is analytic on that fixed word. Applying the same argument to `L_m(u)−a` and `L_m(u)−b` proves existence of the selector limit for every specified roof interval. If a roof or section equality persists identically, its membership is its original open or closed convention. The limiting selector need not equal evaluation of a differently defined boundary section.

This reasoning does not imply convergence for an arbitrary Borel set in the roof line. The native statement correctly restricts automatic existence to the finite section tests and roof intervals; its more general bounded-test assertion explicitly requires an angular-almost-everywhere one-sided limit.

## 9. Passage to the trace and its momentum marginal

The angular measure of both signs is finite, namely `4π`. The physical record and the specified selector have their one-sided limits outside the fixed angular-null exceptional set. Dominated convergence therefore proves the exact trace equality for every stated bounded continuous record test, and for the expressly allowed bounded tests with an almost-everywhere one-sided limit. The normalizing factor remains `1/(4π R c_*)`.

The zero-clearance momentum domination can be proved directly by repeating the justified first-image/growth/last-coarea argument on the limiting strict source. It can also be obtained from the positive-clearance domination: test against a nonnegative continuous compactly supported momentum function, pass to the limit by dominated convergence, then use regularity of finite Borel measures to extend the bound to all Borel momentum sets. The limiting true visited momenta are in `(−1,1)` almost everywhere; no endpoint atom is introduced at a visited grazing state. Truncation of `c_i^{−γ}` followed by monotone convergence gives the same angular moments.

These are statements for each fixed radius and finite count. They assert uniform constants, not a null exceptional set common to uncountably many radii. They do not exchange the original outer localization limit and the collision limsup.

## 10. Scope and verification limits

Native316 establishes a positive marked angular source, its complete collision-momentum kernel in both directions, joint marked incidence estimates and a genuine one-sided trace with the original finite tests. The preceding arguments sum the complete countable physical source before taking a uniform kernel bound. They neither count only sampled trajectories nor infer the result from a script.

The inherited native283 growth theorem is a genuine dependency. Its stated external application is a common-constant homogeneous curve-sum lemma under the verified curve, expansion and distortion hypotheses; it is not the unrestricted physical-word pressure or a roofwise twisted spectral theorem. This reconstruction checks its use on the exact source class and every factor needed by the new proof. It does not claim to independently reconstruct all external spectral analysis or to replace the separate literature audit.

The marked angular trace is not itself the full roof/Gauss-angle boundary charge. The physical normal speed must still be included by the succeeding conversion theorem. Nullity for this angular source cannot be used to erase an unrelated positive endpoint pairing charge. No `m^{−2}` roof density, capacity abundance, whole-cylinder pressure, normalized shortage limit or final raw local limit follows merely from the present kernel or moments.

No source was edited and no additional mathematical test suite was run in this reconstruction. It is a proof-based check of the actual native bodies and their exact original model, separate from the retained auxiliary checker and compilation evidence.

## 11. Final amendment and resolved statement precision

The root author subsequently resolved the sole wording issue by replacing the corollary's two-line phrase with:

> The same domination holds with any Borel original-roof selector with values in `[0,1]`, including the indicator of an arbitrarily small physical time interval.

The final native316 source has SHA256 `64e8bb1b289b244f02ed06e4e56e2c5add54d6835ef48bf7d2b2a0c036a44383`. An exact byte comparison against the retained initial derivation verifies that this selector clarification is the only source change. All constants, equations, inequalities, indices, dependencies and proof bodies are identical. The reconstructed proof therefore applies to this final source with no outstanding correction. The original derivation remains at its original identity `cb307ab780f56011e9729a7e58f64c2943da88ec2b6153263c668934d0b852c6`; the findings above are retained to make the reason for the amendment traceable.

`FINAL_SOURCE_AMENDMENT_RECEIPT.json` records the actual old and final source identities, the exact text replacement and this completed check. The receipt is source verification rather than an additional mathematical execution or a CI result.
