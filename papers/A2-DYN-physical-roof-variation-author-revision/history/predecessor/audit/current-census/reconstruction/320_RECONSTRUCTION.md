# Mathematical reconstruction of native author module 320

Date: 2026-10-20 UTC. This document reconstructs a new author proof from its physical source and inherited analytic identities. It is not a new referee report, independent expert certification, or a claim that the final raw pointwise theorem is complete. The reconstruction itself changes no mathematical source.

## Source and conclusion

The complete draft read was `/workspace/scratch/35c64a3513c5/math-boundary/320_all_offset_marked_boundary_turning.tex`, SHA-256 `a1da0d46bae1f7553ae4fd2927e076b311e5edff464838748c5fba0dfb720737`. The proof was checked against the complete new module 319 (SHA-256 `ea974d39e39822598fb38ba78083702900559e04615ff00a59decbea73b25845`) and the actual native proof bodies 260, 279, 281–284, 316 and 317. These are source identities at the time of reconstruction, not identities of an as-yet-unwritten final commit.

**Result:** the claimed full regular marked-boundary bound follows with the displayed constants and scope. No concrete mathematical defect was found in the new deductions. The proof supplies a mechanism that controls the complete angular turning integral, including nonzero critical offsets and arbitrarily short source pieces. It does not require a uniform pointwise bound on the normal speed at those offsets.

The mechanism depends on two genuinely different estimates: module 319 sums the actual two-sided inverse-weight suprema; module 320 bounds total angular turning on each of those same pieces. The inherited endpoint Hölder-distortion statement alone would not imply the latter. The new proof correctly returns to the absolute logarithmic derivative and integrates it before summing intermediate times.

The theorem concerns the full indicated **regular clearance-boundary measure**, with the separately defined incoming critical fan and distinct visited-grazing, section, pairing and corner measures retained as separate obligations. It gives total variation of the physical-roof pushforward, not the essential height of its roof density.

## 1. Curve class, length bounds and absence of a terminal subdivision

Keep the original radius range `[9/20,47/100]`, true physical collision map and unit-speed flight clock. The existing invariant graph class has

\[
k_-\le V=\frac{d\varphi}{ds}\le U,
\quad k_-={100\over47},\quad U={170\over9},
\quad |V_s|\le B_2=B_{cv}(1+U^2)^{3/2}.
\]

The `B_2` bound follows from the native geometric curvature class in 281. It is not an unproved invariant rectangular bound on the graph's second derivative. All constants `B_cv,k_0,ell_*` are fixed for the original radius family before the collision count and outer limits.

On any connected regular image graph, `phi` is strictly increasing in its unwrapped boundary coordinate and remains in `(-pi/2,pi/2)`. Consequently its entire arclength is at most

\[
L_0=\frac{\pi\sqrt{1+U^2}}{k_-}.
\]

This does not require an artificial subdivision of the terminal graph. On a signed homogeneous strip `H_k`, its angle range has width `k^{-2}-(k+1)^{-2}<=3k^{-3}`, so a segment of arclength `r` satisfies

\[
r\le L_h k^{-3},\qquad L_h=3\sqrt{1+U^2}/k_-,
\quad c\ge(2/\pi)(k+1)^{-2}.
\]

The physical endpoint cap `|p|<=9/10` follows from the original section in 260. It is not a newly imposed observed event. Since `k_0>=2` and `arcsin(9/10)<pi/2-1/4`, the entire cap is inside the existing central strip `H_0`. Because terminal momentum is strictly monotone on the actual branch, restricting to this cap gives one interval, possibly empty. Thus all images used by the new Jacobian-variation argument are homogeneous, while the final actual collision needs neither an infinite homogeneous subdivision nor an extra fixed-length subdivision.

## 2. Absolute logarithmic variation of the physical Jacobian

Native Lemma `uc-logjac` in 282 derives the logarithmic derivative of the Euclidean collision-curve Jacobian directly from the circular graph transform. On a smooth image graph it bounds the absolute derivative per unit **image arclength** by

\[
\left|\partial_{\ell_1}\log J_C T_R\right|
 \le U/c_1+D_B.
\]

The conversion from boundary coordinate `s_1` to image arclength costs at most one, since `|ds_1/dell_1|<=1`. The native formula has no inverse initial incidence. The constant `D_B` is explicitly given in 282 from the already fixed curve class.

On a segment of length `r` in a signed `H_k`, with `k>=2`,

\[
\int|d\log J_C T_R|
 \le(2\pi U+D_B)k^2r
 \le(2\pi U+D_B)L_h^{2/3}r^{1/3}.
\]

The first inequality is conservative: `(k+1)^2<=4k^2`, and `D_B<=D_B k^2`. The second follows from `r<=L_h k^{-3}`. On `H_0`, `c_1>=c_H=sin(k_0^{-2})` and `r<=L_0`, so

\[
\int|d\log J_C T_R|
 \le(U/c_H+D_B)L_0^{2/3}r^{1/3}.
\]

Taking the maximum of the two displayed constants gives exactly `D_1^{var}` in the module. These bounds estimate the integral of the **absolute** derivative. They therefore prove total variation, including arbitrarily many oscillations of the derivative. They are stronger than a bound merely on the difference of the endpoint values of `log J`.

The adapted expansion is at least `59/47` at each actual collision. Its Euclidean-to-adapted norm equivalence is paid only at the two endpoints of a multi-step product. If `L_i` is the length of the `i`th image of one connected branch ending at time `l`, then

\[
L_i\le\Gamma\varrho^{l-i}L_l,
\qquad\Gamma=\sqrt{1+k_+^2},\quad\varrho=47/59.
\]

Variation is unchanged under the injective monotone parametrization of a regular curve. Writing the logarithm of the actual `l`-step Jacobian as the sum of its `l` one-step logarithms, and applying the triangle inequality, gives

\[
\operatorname{Var}\log J_C T_R^l
 \le D_1^{var}\sum_{i=1}^l L_i^{1/3}
 \le\frac{D_1^{var}\Gamma^{1/3}}{1-\varrho^{1/3}}L_l^{1/3}
 \le V_J.
\]

There is one factor `Gamma^{1/3}`, not a new such factor at every time. The geometric series is uniformly convergent. At `l=0`, the Jacobian is one and its variation is zero. Exhaustion by compact regular subarcs establishes the same inequalities for open intervals with singular limiting endpoints; it does not assert derivatives at a singularity.

## 3. The exact half-momentum chain rule, including the inverse density

For a half-ray with `l>=2` true collisions, the first image `C` has its exact angular source density

\[
\rho_C=\frac{c_1}{a\sqrt{1+V_1^2}}.
\]

The true source differential is `d vartheta=rho_C d ell_C`. At the terminal image, the physical momentum differential per curve arclength has magnitude `c_l V_l/sqrt(1+V_l^2)`. Thus the complete chain rule is

\[
A_l^p=|\partial_\vartheta p_l|
 =\frac{c_lV_l}{\sqrt{1+V_l^2}}
    \frac{J_C(T_R^{l-1})}{\rho_C}.
\]

The inverse initial density is essential. Replacing it by the density itself or by a constant would reverse the grazing factor and invalidate the argument. Module 320 has the correct formula. The identity is taken before multiplication by any Borel selector; the original selectors are never differentiated.

The logarithmic variation of each factor is finite and uniform:

* For the first-image density, `log rho_C=log c_1-log a-(1/2)log(1+V_1^2)`. Monotonicity of `phi_1` bounds the variation of `log c_1` by `-2 log c_H` on `H_0`, or by `log(pi/2)+2 log(1+k_0^{-1})` on either signed strip. A passage through `phi_1=0` in the central strip is correctly paid by the factor two.
* Native 279 gives `a_s=p+bc/a`, `|a_s|<=1+b_*/a_circ`, and `|V_{1,s}|<=K_0`. Integrating on a first piece of arclength at most `ell_*`, and using `V/(1+V^2)<=1/2`, gives exactly `V_rho=V_H+(a_circ^{-1}+b_*a_circ^{-2}+K_0/2)ell_*`.
* The preceding absolute Jacobian argument gives `Var log J_C(T^{l-1})<=V_J`. Every intermediate image is homogeneous under the partition already used in 319, and the capped final image lies in `H_0`.
* At the terminal cap, `c_l>=c_circ=sqrt(19)/10`, so `Var log c_l<=-2log c_circ`. The geometric curvature bound gives `|partial_s log(V_l/sqrt(1+V_l^2))|=|V_{l,s}|/[V_l(1+V_l^2)]<=B_2/k_-`. Its integral is at most `B_2 L_0/k_-`. This is the displayed `V_t`.

For `l=1`, there is no first-image homogeneous subdivision in 319. The proof correctly handles this separately using `A_1^p=kappa a+c`. The exact native first-flight identities give

\[
\partial_s(\kappa a+c)
 =\kappa(p+bc/a)-p(\kappa+c/a)
 =c(\kappa b-p)/a.
\]

Since `A_1^p>=k_- a_circ`, the absolute logarithmic derivative is at most `(k_+ b_*+1)/(k_- a_circ^2)`. Integrating over length at most `L_0` gives `V_1`. This avoids introducing an unnecessary divergent terminal strip count at an endpoint flight.

Combining the cases proves `Var log A_l^p<=V_A=max(V_1,V_rho+V_J+V_t)`. Reversal changes the physical momentum sign and transports the original selector, while preserving the angular and curve arclength magnitudes. It leaves this absolute variation estimate unchanged. Neither a new collision nor a new independence assumption appears.

## 4. Radial turning and a genuine origin crossing

For a regular nonzero plane curve `P`, let continuous angles on a compact subarc be `alpha=arg P`, `psi=arg P'`, and put `delta=psi-alpha`. The exact identity is

\[
\alpha'=\frac{|P'|}{|P|}\sin\delta.
\]

The Lipschitz periodic triangular function `h(delta)=arccos(cos(delta))` ranges in `[0,pi]` and has derivative `sgn(sin(delta))` except at multiples of `pi`. The absolutely continuous chain rule yields

\[
|\alpha'|=\operatorname{sgn}(\sin\delta)\psi'-\frac{d}{ds}h(\delta)
\quad\text{a.e.}
\]

At a level set `delta in pi Z`, its derivative is zero almost everywhere on that set; also `alpha'=0` there. Hence the identity is valid with the sign set to zero. Integrating proves

\[
\int|d\arg P|\le\operatorname{Var}\arg P'+\pi.
\]

This bound is independent of how close the curve comes to the origin. If there is one actual zero, apply the result separately on both punctured sides. The tangent variations on those disjoint sides sum to at most the full tangent variation, while the endpoint charges contribute at most `2pi`. Exhaustion is monotone for the nonnegative integral.

For the physical endpoint vector `P=(-p_0,p_m)` on an overlap from 319, both coordinate derivatives are nonzero with fixed signs. Therefore its tangent remains in one open quadrant and `P` has at most one origin crossing. The original simultaneous endpoint cap is still an interval because each momentum is monotone. In a fixed quadrant, the tangent angle as a function of `log(A_+^p/A_-^p)` has derivative magnitude

\[
\frac{A_+^p/A_-^p}{1+(A_+^p/A_-^p)^2}\le\frac12.
\]

Each half logarithm has variation at most `V_A`, so tangent turning is at most `V_A`. Consequently every actual capped overlap satisfies

\[
\int_{P\ne0}|\partial_\vartheta\arg P|\,d\vartheta\le 2\pi+V_A.
\]

The omitted jump at an actual zero is not declared to be a vanishing critical fan. The module explicitly keeps that different measure outside the regular integral. Restricting by an original Borel selector between zero and one only decreases this nonnegative integral; no component count of that selector is taken.

## 5. Physical coefficient and exact normalization

The original roof-angle boundary coefficient in native 317 is

\[
f^\varepsilon=\frac{W^\varepsilon u_x}{4\pi c_*h_x},
\qquad h_x=\frac{R^2\chi}{\det G}.
\]

For the physical endpoint Hessian `G`, `chi=e^{perp T}G e^perp` with `e=g/|g|`. The two-dimensional cofactor identity gives exactly

\[
h_x=R^2e^{\mathsf T}G^{-1}e.
\]

The original endpoint-cap Hessian estimate is `G<=Lambda_circ I`, uniformly in the actual word and radius. Therefore

\[
h_x\ge R_-^2/\Lambda_\circ,
\qquad f^\varepsilon\le\frac{\Lambda_\circ}{4\pi c_*R_-^2}u_x,
\]

using the actual bound `0<=W^epsilon<=1`. At an unvisited zero-clearance boundary the bad-source weight can equal one; it is not suppressed in this argument. The coefficient has precisely one original conditioning factor `c_*^{-1}`. The radius factor in `u_x` was already derived by comparing the same physical line and endpoint-momentum measures in 319; it is not inserted a second time here.

Apply the exact positive flux identity from 317 on every actual regular overlap. Taking the supremum of `u_x` on the same physical interval and using its turning bound gives

\[
\mathfrak B^{reg}_{j,u_0}
 \le\frac{\Lambda_\circ(2\pi+V_A)}{4\pi c_*R_-^2}
       \sum_O\sup_Ou_x.
\]

Module 319 sums these genuine suprema, including both impact signs, every actual half-word and every overlap. Its constant is `Q_mb=(607/90)H_nm(94/sqrt(1827))`. Thus the resulting constant is exactly

\[
C_{ab}=\frac{\Lambda_\circ(2\pi+V_A)}{4\pi c_*R_-^2}
       \frac{607}{90}H_{nm}\frac{94}{\sqrt{1827}}.
\]

No additional factor for impact signs, translated initial disks, formal words, source-component length or conditional probability is missing. The fixed-clearance measure is for one specified incident side; if both incident sides of a positive level are requested, their charges must be added, as the source definition states.

## 6. Countable exhaustion, depth and remaining measures

The full regular integral is obtained first on finite compact regular subfamilies and then by nonnegative exhaustion. The countable artificial source cuts are null for the absolutely continuous angular integrals being estimated. This step does not remove a distinct singular or atomic boundary measure. Actual endpoint and record tests are retained as selectors on already defined incident germs; no boundary value is assigned to an arbitrary new Borel function without an existing one-sided trace.

The direct one-sided trace source at `u_0=0` is the one constructed in 316 and 319. The proof therefore applies at that level without exchanging a weak limit and a variation norm. Later genuine marked-disk hits remain real collisions, and there is no fictitious reflection at the initial marked foot.

For each index `j`, the completed estimate is

\[
\mathfrak B^{reg}_{j,u_0}
 \le C_{ab}(\varrho^j+\varrho^{m-1-j}).
\]

Summing over `min(j,m-1-j)>=D` gives `2 C_ab varrho^D/(1-varrho)` for every integer `D>=0`, including the empty index range. The constant is uniform before taking any supremum over radius, exact labels and prescribed levels. With `D=ceil(theta_*m)` and fixed `0<theta_*<1/2`, multiplication by `m^2` leaves a constant times `m^2 varrho^{theta_*m}`, which tends to zero. This is an ordinary geometric estimate; it does not exchange the original outer limits.

Pushforward under the unchanged physical roof cannot increase the total variation of this positive measure. That statement remains a mass estimate. It does not control a microscopic roof density's essential supremum, and it does not pay a fixed shallow-source mass after multiplication by `m^2`.

The all-offset regular turning argument therefore closes the regular marked-boundary angular summation that was left after the earlier zero-offset calculation. The complete incoming critical fan, distinct visited-grazing and section/pairing boundary measures, shallow low-load same-roof comparison shortage, whole physical comparison capacity, and the original spectral, arithmetic and normalization interfaces are not discharged by this theorem. This is the correct scope of its positive mathematical advance.

## 7. Verification character

This reconstruction checked the absolute integrals, homogeneous strip exponents, complete Jacobian chain rule, inverse initial density, endpoint-cap location, adapted metric payment, radial-turning identity, actual origin crossing, physical cofactor identity, radius powers, conditioning, mark multiplicities and finite-count depth sum. No script, floating-point sample or successful compilation was used as a premise for a continuous geometric statement.
