# Independent reconstruction: a complete physical roof BV majorant

This is an author-side proof reconstruction for the next A2-DYN revision, not a referee report. It does not modify the manuscript. It reconstructs the proposed implication of the existing native proofs through 322 and distinguishes the theorem actually obtained from the original normalized local-limit target.

## 1. Conclusion and necessary scope

I find the proposed mechanism valid, provided the fixed-time stitching argument below is included. No additional positive boundary term remains after that argument. In particular the absence of a uniform critical-chart radius does not obstruct this theorem: the chart/excision limit is taken first at a fixed physical radius and collision count, and its resulting inequality has constants independent of those choices.

The assertion is **directional variation in physical roof time**, not full two-dimensional BV in roof and Gauss angle. It yields BV of the unconditioned cap-majorant roof density. Arbitrary physical Borel selectors inherit its nonnegative density domination and hence its L-infinity bound; they do **not** inherit BV. Taking a selector that oscillates infinitely often as a function of the roof already disproves such a stronger BV claim.

The constant is finite and independent of collision count, radius, collision word, exact record, incidence margin, clearance margin and target roof. It is not an `m^{-2}` estimate. It does not establish normalized shallow-source payment, the full raw local limit theorem, a conditional denominator, an arithmetic factor or the four-coordinate inversion theorem.

## 2. Exact measure and constants

Fix the unchanged triangular Lorentz gas, radius `R in [9/20,47/100]`, unit physical speed, and an integer `m >= 1`. The original collision measure is

\[
d\nu=\frac{d\alpha_0\,dp_0}{4\pi},\qquad
d\nu_R^*=\frac{\mathbf1_{Y_R^*}}{c_*}\,d\nu.
\]

Let `a=5/6`, let `C_{m,R}` be the entire regular actual `m`-flight source with `|p_0|,|p_m|<a`, and define the positive majorant

\[
\overline\mu_{m,R}
 =(L_{m,R})_*\left(\frac{\mathbf1_{C_{m,R}}}{c_*}\,d\nu\right).
\tag{1}
\]

The use of `<` or `<=` makes no bulk-measure difference, by the physical endpoint-momentum kernel. This is a finite positive majorant, with mass at most `1/c_*`; it is not redefined as the original probability measure. The cap contains the entire original exact event: native 311 proves

\[
\frac{10600}{12809}+\frac1{200}<\frac56.
\]

For the original source measure `mu_{E,H}` of native 314, with any physical Borel `E` and `0<=H<=1`, one has `0<=mu_{E,H}<=overline mu`. Thus all original initial/terminal section tests, exact return and displacement labels, every actual collision, the original roof, and arbitrary record selectors remain on the left side of the comparison. No selector is differentiated or assumed to factor across collisions.

Use the retained constants

\[
\lambda_\circ=\frac{9\sqrt{19}}{200},\quad
\Lambda_\circ=\frac{47}{6},\quad
R_-=\frac9{20},\quad \sigma=\frac{47}{59},\quad U_2=\frac{320}{9}.
\]

Define

\[
C_0=\frac{\Lambda_\circ}{\lambda_\circ}
       \left(C_\omega+\frac{2C_F}{\lambda_\circ}\right),
\]

where `C_omega` and `C_F` are exactly the constants in native 289 and 288. Let `J_cross` be the full unconditioned singular-multiplier constant of native 315, `C_mom` the all-time physical endpoint-momentum kernel constant of native 284, and `C_ab` the complete marked regular-boundary constant of native 320. Then a valid total-variation constant is

\[
\mathcal V
 =\frac{C_0J_\times}{c_*}
 +\frac{2C_{\rm ab}}{1-\sigma}
 +\frac{\Lambda_\circ C_{\rm mom}}{2c_*R_-^2}
 +\frac{U_2 C_{\rm mom}}{2c_*}.
\tag{2}
\]

The intended theorem is

\[
\overline\mu_{m,R}=\overline\rho_{m,R}(t)\,dt,
\quad
\overline\rho_{m,R}\in BV(\mathbb R),
\quad |D\overline\rho_{m,R}|(\mathbb R)\le\mathcal V,
\quad \|\overline\rho_{m,R}\|_\infty\le\frac{\mathcal V}{2}.
\tag{3}
\]

Consequently

\[
0\le\rho_{E,H}\le\overline\rho_{m,R}\quad\text{a.e.},
\qquad \|\rho_{E,H}\|_\infty\le\mathcal V/2.
\tag{4}
\]

The `1/2` in (3) uses the compact roof support and nonnegativity. The weaker bound by `V` would also suffice if the manuscript prefers not to use this final elementary sharpening.

## 3. Unweighted regular interior

On one actual endpoint-action chart write

\[
q=(\alpha_0,\alpha_m),\quad F=L_m,\quad
g=\nabla_qF=z e(\theta),\quad G=D_q^2F,
\quad \chi=e^{\perp T}Ge^\perp,
\quad b=\frac{\omega}{4\pi c_*\chi}.
\tag{5}
\]

The coarea map is `(q -> (t,theta))=(F,arg g)` and its absolute determinant is `chi`. It uses original physical time, not an optical or rescaled clock. The exact density identity is

\[
b\,dt\,d\theta=\frac{\omega}{4\pi c_*}\,dq
 =\frac{d\nu}{c_*}
\tag{6}
\]

on the one-copy actual branch.

For this interior estimate it is essential to set `W=1` directly in the derivation of native 289. One cannot take a limit in the displayed guarded estimate containing `epsilon^{-1}`. The proofs of native 288 and 289 use only the actual physical itinerary and the endpoint cap; section membership or exact labels play no other role. Since `5/6<9/10`, all their constants apply to (1).

At fixed Gauss angle, native 260 and 289 give

\[
\frac{dq}{dt}
 =\frac{G^{-1}e}{z e^TG^{-1}e},\qquad
\left\|\frac{dq}{dt}\right\|_\infty
 \le\frac{\Lambda_\circ}{\lambda_\circ z},\qquad
|\partial_t\chi|
 \le 2C_F\left\|\frac{dq}{dt}\right\|_\infty.
\]

Also `|D_q log omega[eta]| <= C_omega I_m ||eta||_infty`. Therefore

\[
|\partial_t b|
 \le C_0\,b\frac{I_m}{z}.
\tag{7}
\]

There is no derivative of `e` because the derivative is at fixed `theta`; no guard derivative remains; and `c_*` occurs once. Sum the nonnegative integrals over the actual one-copy source, then use native 315:

\[
\sum_{\rm sheets}\int|\partial_t b|\,dt\,d\theta
 \le\frac{C_0}{c_*}\int\frac{I_m}{|\nabla_qF|}\,d\nu
 \le\frac{C_0J_\times}{c_*}.
\tag{8}
\]

This integrates the actual incidence insertion at every interior collision. No word-count factor, positive incidence cutoff, or probability independence is introduced.

## 4. Why finite-time boundary stitching is legitimate

This is the substantive proof-completeness step that must appear in the new native manuscript.

### 4.1 Finite physical words and compact closures

At fixed `R,m`, finite horizon bounds every flight and bounds each relative next-center choice to a finite set. Hence only finitely many lifted visited-center words occur after fixing the initial center. For each such word the closure of its actual cap configurations is compact in the finite product of contact-angle circles. The true flight lengths remain at least `tau_-=3/50`; the endpoint incidences remain positive because of the cap.

Native 292 supplies an analytic formal endpoint lift at every point of each closure, including simultaneous visited-grazing limits. This is an auxiliary chart used to describe a one-sided boundary; it never declares the continued trajectory physical beyond that boundary. Native 260 supplies the continuous reduced Hessian at that limit and the positive lower bound `G>=lambda_circ I`. Thus the formal endpoint-gradient map is locally invertible there. A finite collection of these charts covers the compact closures.

Within these charts physical admissibility is a finite Boolean combination of analytic inequalities. The designated signed incidences must be positive. For each of the finitely many possible nonincident disks, either the perpendicular projection falls outside the open flight or the squared line distance exceeds `R^2`. All expressions are analytic because flight lengths do not vanish. Original endpoint caps are the four analytic inequalities in `p_0,p_m`. Strict positivity is sufficient to recover the actual next-hit word by the same geometric argument as native 292; no earlier hidden collision is allowed.

At a zero unvisited clearance the perpendicular foot is strictly interior: the two incident endpoints have distance at least `1-2R>=3/50` from every other disk boundary. Near such a boundary, after fixing impact sign, the line clearance itself is analytic and its differential is nonzero by the native marked-coordinate determinant. Consequently no endpoint-foot switch creates an additional zero-clearance boundary.

### 4.2 Noncritical slices and artificial seams

Away from `g=0`, `(F,arg g)` is a local analytic diffeomorphism since `chi>=lambda_circ`. Take a smooth finite partition of unity in the auxiliary charts, subordinate to compactly supported smaller chart neighborhoods. At fixed `theta`, each physical part is a union of intervals in `t`. On a compact smaller chart the admissibility functions are analytic in `t`, so each has finitely many zeros unless it vanishes identically on that slice. Such an identically vanishing strict physical constraint contributes no open physical interval; exceptional tangential slices can be discarded on their angular null sets or treated by direct zero contribution. The point is a fixed-chart, fixed-slice statement; there is no uniform collision-dependent count in the estimate.

Integrate by parts on these actual intervals. The derivative terms of the partition of unity cancel after summation, before taking absolute values, because its sum is one on the original source. Coordinate and homogeneity seams therefore create no physical charge. One does not bound their separate absolute endpoint contributions and then multiply by an atlas or word count.

Every genuine noncritical interval endpoint is one of:

1. an endpoint cap;
2. an unvisited zero-clearance boundary;
3. a visited grazing boundary.

If several conditions are active, first assign visited-grazing endpoints their zero trace. Among the remaining endpoints, assign an active unvisited clearance before assigning a cap, and choose the least active marked constraint in a fixed finite ordering. The residual cap arcs are then actual regular physical roots, exactly as required by native 284. Bounding the assigned unvisited terms by the full nonnegative marked boundary sum can only enlarge the charge. There is no separate codimension-two corner term in one-dimensional integration by parts: the interval endpoint is already the complete endpoint contribution. At a smooth cap or unvisited boundary, one-dimensional coarea converts the integral of traces over `theta` to `b |dtheta|` along the real boundary, with the actual multiplicity. This is exactly the flux convention of native 317. Points where its angular derivative vanishes do not add a charge; native 317 proves the corresponding null-image fact.

One may equivalently work with maximal regular Gauss segments. Native 260 gives finite `q` limits at both endpoints and strict increase of `z` with `t`. The analytic endpoint-chart description above classifies all the possible limiting endpoints and prevents an unclassified limit from entering the sum.

### 4.3 Visited grazing, including a critical visited-grazing endpoint

If any actual interior incidence tends to zero, native 260 gives `omega -> 0` and `chi>=lambda_circ`. Hence `b -> 0`. This proves zero endpoint trace in the integration-by-parts formula. It is not an inference from bulk singular-nullness.

The convergence is also uniform near a fixed limiting configuration: `omega` has continuous zero extension while `chi` has the fixed positive lower bound. Thus, even if `g->0` simultaneously, the integral of `b` over an auxiliary small gradient circle is at most `2pi sup b`, tending to zero. The gradient chart is locally one-to-one; after one-copy identification no uncontrolled angular multiplicity appears. No derivative of the singular physical collision map is assigned.

### 4.4 Critical points and their complete incoming fans

All formal critical configurations in the compact closures are isolated by the positive Hessian and local gradient inverse. They are therefore finite at fixed `R,m`; otherwise an accumulation point would contradict that same local invertibility. Choose disjoint small auxiliary neighborhoods of them. The neighborhood sizes may depend on `R,m` and the words.

Excise each neighborhood by `|g|<delta` in its local gradient coordinates. Its new boundary is `g=delta e(theta)`. Along a Gauss segment `z` increases with `t`, so these are incoming boundaries. Integration by parts produces the actual positive term `b(t_delta(theta),theta) dtheta` on the admitted angular set.

At a positive-visited critical configuration, the only active full-source physical constraints are unvisited clearances. Their nonzero linear differentials give the finite tangent-sector family used in native 285. At normal endpoints the cap is strict. Almost every angular direction has a stable physical sign as `delta` decreases, so the admitted angular indicator converges to the tangent fan. Continuity of `omega,G` and the lower Hessian bound justify dominated angular convergence. The resulting total incoming weight is exactly

\[
\int_{\rm admitted\ Gauss\ fan}
 \frac{\omega_*}{4\pi c_*\,e^{\perp T}G_*e^\perp}\,d\theta
 =\mathfrak J(x)\,\beta_y(x).
\tag{9}
\]

Here `y=G_*^{1/2}(q-q_*)` is the native normalized critical coordinate. To check (9), the angular map from `y` direction to `g` direction has Jacobian `sqrt(det G_*)/(e_y^TG_*e_y)`, whereas `chi_g=det G_*/(e_y^TG_*e_y)`. Their ratio is `1/sqrt(det G_*)`; integration gives `omega_*/(2c_*sqrt(det G_*))` times the normalized sector fraction. Thus the factor is precisely the retained `J`, with no extra `2pi`, radius, or angular-fraction substitution.

For a visited-grazing critical configuration the same excision term tends to zero by 4.3, even if the physical tangent set has no asserted sector form. Merge sectors and representations of the same limiting strict-word physical germ before summing. Native 285 then gives the complete positive-visited fan bound, including fully regular critical points,

\[
\sum_x\mathfrak J(x)\beta_y(x)
 \le\frac{U_2 C_{\rm mom}}{2c_*}.
\tag{10}
\]

Do not add the separate regular-critical estimate to (10): fully regular critical points are already included.

### 4.5 Limit order and absence of a nonleading error budget here

For a fixed `R,m`, integrate first on compact regular pieces with the indicated critical excisions. Then remove all artificial cuts and send the finitely many excision radii to zero. The interior derivative is absolutely integrable by (8); the entire regular unvisited-boundary charge is integrable by native 320; cap charges are integrable by the calculation below; visited traces are zero; critical flux limits are (9). These bounds justify the exhaustion of the integration-by-parts identity.

This proves an exact distributional identity and a uniform total-variation inequality. It does not sum local `O(sqrt(s))` remainders using a collision-dependent word count. The variation of the actual density away from the limiting critical boundary is already part of the integral in (8) and of the complete regular boundary measures. Only after establishing the exact finite-count inequality is its uniform constant used to take suprema in `R,m`. No microscopic width is changed, and no original outer/collision limit is interchanged.

## 5. Regular unvisited boundaries

At zero clearance the unweighted trace has `W=1`; this also agrees with the original bad-source weight at that boundary. The proof of native 320 therefore applies directly. Although its theorem is phrased with original selectors retained, native 319 explicitly constructs the entire regular angular source before any such selector; no section test is used in its capacity, distortion or turning estimate. The cap `5/6` is contained in its `9/10` cap.

Summing the complete marked budget at `u_0=0` over every actual flight gives

\[
\sum_{j=0}^{m-1}\mathfrak B_{j,0}^{\rm reg}
 \le C_{\rm ab}\sum_{j=0}^{m-1}
       (\sigma^j+\sigma^{m-1-j})
 \le\frac{2C_{\rm ab}}{1-\sigma}.
\tag{11}
\]

This includes shallow as well as deep flights, both impact signs, all physical words and all simultaneously active marked candidates. Assigning each actual domain endpoint only once reduces the positive bound. No factor counting words, charts or unvisited disks is appended.

## 6. Four cap boundaries: exact calculation

For every regular endpoint-momentum root, not only at a critical point, the exact generating-function identity gives

\[
u_x=\frac1{|\partial_{\alpha_0}p_m|}
     =\frac{R^2\omega}{\det G},\qquad
h_x=\frac{R^2\chi}{\det G}
     =R^2 e^TG^{-1}e,
\qquad b=\frac{u_x}{4\pi c_* h_x}.
\tag{12}
\]

Thus `b <= Lambda_circ u_x/(4pi c_* R_-^2)`. At `p_0=a`, parameterize the actual cap arc by `v=p_m in [-a,a]`. The gradient direction is `arg(-a,v)` and

\[
\left|\frac{d\theta}{dv}\right|
 =\frac{a}{a^2+v^2},\qquad
\int_{-a}^a\frac{a}{a^2+v^2}\,dv=\frac\pi2.
\tag{13}
\]

At each common `(a,v)`, native 284 gives the actual regular inverse-root sum `sum_x u_x <= C_mom`. Hence this cap contributes at most

\[
\frac{\Lambda_\circ C_{\rm mom}}{4\pi c_*R_-^2}
 \cdot\frac\pi2
 =\frac{\Lambda_\circ C_{\rm mom}}{8c_*R_-^2}.
\tag{14}
\]

The other initial cap is identical. For `p_m=+/-a`, use `v=p_0` and the same joint endpoint root sum at `(v,+/-a)`; (12) is still the correct density and the angle variation is again (13). No new conditional law or time-reversal normalization is needed. The four cap boundaries therefore have total charge at most

\[
\frac{\Lambda_\circ C_{\rm mom}}{2c_*R_-^2}.
\tag{15}
\]

The cap corners have no extra interval-endpoint contribution beyond the assigned boundary terms. A cap cannot meet a critical point because a critical point has both endpoint momenta zero and `a>0`.

## 7. Distributional conclusion

Let `f(t,theta)` be the nonnegative sum of the densities (5) on the one-copy physical roof-angle sheets. It lies in `L^1(dt dtheta)` by (6), and its marginal is the density of (1). For every smooth compactly supported test function, the fixed-time stitching above gives the distributional `t` derivative as the sum of the regular interior derivatives, signed regular physical boundary terms, and the incoming critical fan measure. The sum of their absolute masses is bounded by (8), (10), (11), and (15). Consequently

\[
|D_t f|(\mathbb R\times\mathbb S^1)\le\mathcal V,
\qquad
|D\overline\rho|(\mathbb R)\le\mathcal V.
\]

This is a directional derivative estimate; no estimate for `D_theta f` is asserted. The density is supported in `[m tau_-, m tau_+]`, where `tau_+<28/5` is the unchanged physical flight bound. Extend it by zero outside this compact interval. For an a.e. representative, the variation from the zero left tail up to a value `M` and back to the zero right tail is at least `2M`. Taking essential suprema proves `||rho_bar||_infty <= V/2`. Positive measure domination then proves (4), without differentiating any selector.

## 8. Dependency and risk audit

The new implication is built from native 260 (Hessian, Gauss lengths and zero visited-grazing traces), 284 (complete actual endpoint-momentum kernel), 285 (complete positive-visited critical fans), 288–289 (physical derivatives and direct unweighted variation), 292 (formal analytic charts even at visited-grazing limits), 315 (entire physical singular multiplier), and 319–320 (complete regular marked-boundary capacity and turning). No external mixing or pressure theorem is invoked by the new stitching step.

The underlying native 284 and 319 kernel constants still depend on the physical curve-growth chain 279–283. This reconstruction checks the logical continuation from those proved native statements; it is not an independent reconstruction of every earlier curve-growth proof or an independent-expert endorsement. Their exact stated physical hypotheses must remain in the proof/dependency ledger.

The strongest justified new statement is the all-margin, complete-physical-source bound (3)–(4). The original microscopic roof intervals may now be bounded by `(V/2)|S|`, and every selected finite roof density with selector between zero and one has that uniform majorant. This does not give an L-infinity bound for the separately `I_m`- or `Z_m`-weighted roof measures: those insertions are unbounded and require a separate argument for any claimed density improvement. These facts do not imply that a source whose total mass is small has a small roof essential supremum, nor that multiplying (4) by `m^2` yields decay. Normalized localized shortage, effective comparison capacity, precise lattice arithmetic, conditional probabilities and the uniform spectral/local-limit inputs retain their original obligations.

## 9. Source readback

Read-only reconstruction used the native files in

`/workspace/scratch/35c64a3513c5/theta-theory-next/papers/A2-DYN-critical-source-transport-author-revision`.

No manuscript, workflow, historical proof, remote ref or review file was edited. The companion `SOURCE_IDENTITIES.json` identifies each input by SHA-256 and its repository-relative path. This memo is a proof reconstruction, not a finite-script or CI certificate of the continuous theorem.
