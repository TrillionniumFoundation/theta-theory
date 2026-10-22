# Author reconstruction of canonical source charges and exact-record BV

This is an internal mathematical author reconstruction of draft modules 324 and 325. It is not an external referee report, a new expert review, or a proof inferred from finite computation. The repository source was not modified.

## Inspected versions

- `new-round-provenance/math-section-boundary/324_canonical_collision_boundary_budgets.tex`: SHA256 `59b827efe313cd8f71c172f18c14cfa193a4d1e44f66d1532958831338f3c9bb`.
- `new-round-provenance/math-section-boundary/325_exact_records_and_marked_roof_fourier.tex`: SHA256 `a60c8a70110c6b686a14bdc12a1dfbb17e719ea0eb39ec7609b0a8ce51128837`.
- Integrated `core/323_complete_physical_roof_variation.tex`: SHA256 `36eae03703168ed37d571a94bd8faf35398415163eaeb49d3b2d73c5b44bbdd8`.

The separate module-323 audit reconstructs its complete physical source derivative, genuine boundary endpoints, critical incoming fans, and domination-only scope. The present audit checks the additional canonical-source and finite-record steps against that precise interface. Inherited native optical, curve-growth, endpoint trace, and turning statements remain identified dependencies, rather than conclusions proved by this audit.

## 1. The source class and actual optical initialization

The horizontal source is the original collision line `p=b`, parameterized by alpha on its one physical collision circle. The vertical source is the original collision line `alpha=a`, parameterized by the actual angle phi on its outgoing semicircle. Neither source is declared a probability law. Their lengths are `2 pi` and `pi`, respectively.

Module 324 uses the qualified enlarged curve class from module 284, with its own curvature allowance, homogeneity cutoff, short length and growth constant. In particular it does not reuse the smaller marked-foot class constant for a first image whose curvature bound is `K_mom`.

For a horizontal source, its transverse initial variation is `(R c,1)` and the first outgoing displacement is `a_1=tau+R c`. This optical coefficient does not lengthen the physical roof. Its line foot is in general inside the departure disk, so the actual first-hit test must begin at the actual exit contact. The draft explicitly makes that distinction. For a vertical source the initial variation is `(0,1)` and `a_1=tau`; here the source is the actual fixed contact.

For both types the actual first-image identities are

\[
 |ds_1/d\vartheta|=a_1/d,
 \quad V_1=\kappa+d/a_1,
 \quad\rho_1=\frac{d}{a_1\sqrt{1+V_1^2}}.
\]

The pointwise first-image curvature bound is uniform because `a_1>=tau_-`, even when the initial source angle approaches grazing. The vertical source has a finite first-hit partition: an outgoing ray from its fixed contact cannot reenter the current convex disk, and all candidate other disks are covered by the proved finite-horizon candidate set. A physical first entry cannot exchange order with another without a common contact of disjoint disks. Thus the physical cuts are the actual disk-shadow endpoints, not a newly postulated partition.

The density factor d is retained when target homogeneity strips are summed. Its `k^{-2}` decay pays their infinitely many labels. The first-image family is then propagated with the enlarged class's own growth constant. The final collision is divided only by its finite physical first-hit partition, and the terminal derivative cancellation is applied before introducing any terminal homogeneity cuts. The final image has no infinite terminal homogeneity subdivision.

## 2. Branch-supremum estimates are stronger than a pointwise kernel

The inverse derivative sums in `thm:cs-half-sup` are actual whole-interval suprema. Their proof is a chain-rule estimate from the complete first-image density family, through the middle curve-growth partition, to the exact final momentum derivative. It does not replace a supremum sum by an almost-everywhere density bound.

For l flights, the positive transverse displacement satisfies

\[
 B_1\ge\tau_-=3/50,\quad
 B_{r+1}=(1+\tau_r k_r)B_r+\tau_rD_r,
 \quad k_r=2/(R c_r).
\]

Since `1+tau_r k_r>=59/47`, the terminal momentum row gives

\[
 A_l\ge k_-\tau_- (59/47)^{l-1},
 \quad A_l^{-1}\le(47/6)(47/59)^{l-1}.
\]

This statement, the supremum sums, and the two-sided determinant below have no endpoint cap. The cap is needed only later when converting inverse weights to Gauss-angle charge. Module 326 may therefore use these three uncapped ingredients even for its terminal-grazing stopping groups.

## 3. Central determinant and its exact incidence factor

Let `(X_-,Y_-)` and `(X_+,Y_+)` be the actual backward and forward terminal momentum rows from an internal collision i. In coordinates `(alpha_i,phi_i)` the two endpoint momentum rows, up to their harmless full-row orientation signs, are

\[
 (R c_i X_-+Y_-,-Y_-),
 \qquad(R c_i X_++Y_+,Y_+).
\]

Their determinant is the positive sum of the two products. The source area is

\[
 d\nu=\frac{c_i}{4\pi}d\alpha_i\,d\varphi_i
      =\frac{u_x}{4\pi}dp_0\,dp_m.
\]

Consequently

\[
 u_x=\frac{c_i}{A_-^{\rm hor}A_+^{\rm hor}(d_-+d_+)},
 \quad d_\pm=Y_\pm/(R c_iX_\pm+Y_\pm),
\]

and also

\[
 u_x=\frac{c_i}{Y_-Y_+(h_-+h_+)},
 \quad h_\pm=1+R c_iX_\pm/Y_\pm.
\]

Factoring off the first actual free-flight matrix gives `Y_l>=tau_- X_l`, so

\[
 d_\pm\ge\frac{\tau_-}{\tau_-+R_+},
 \quad h_\pm\ge1.
\]

The horizontal coefficient is therefore `C_0 c_i` with `C_0=53/12`; the vertical coefficient is at most `1/2`. There is no extra `1/R` in a canonical collision source. Such a factor belongs to a different marked-foot coordinate change and must not be imported here.

The retained horizontal `c_i` is essential to pay the original infinitely many homogeneity boundary levels. It is uniform as the canonical source itself approaches grazing. The two disjoint one-sided families share a fixed source seam; the interval-overlay inequality then pays the complete overlaps without a collision-word count or a minimum interval length.

## 4. Turning estimates and cap scope

For angular charges only, the endpoint momenta are restricted to `[-9/10,9/10]`. Terminal momentum is strictly monotone on each regular source interval, so this cap leaves one interval. On a two-sided overlap the two components of the endpoint momentum derivative have fixed signs. Its tangent angle therefore varies by at most half the sum of the two logarithmic derivative variations. The inherited radial-turning lemma adds at most `2 pi` even if the momentum curve crosses the origin; that lemma is used on the punctured curve and does not pay the critical incoming fan.

The uniform logarithmic variation constants use the enlarged class throughout. At the final image, the endpoint cap lies in the central strip. The density factor in the first image, the middle Jacobian, and the terminal factor are kept separate in the exact chain rule before their absolute variations are summed. For l=1 the direct formula

\[
 A_1=\kappa a_1+d,
 \qquad \partial_{s_1}A_1=d(\kappa b_1-p_1)/a_1
\]

provides the stated bound without an artificial initial homogeneous cut.

For a fixed initial-angle side, the source derivative of `P=(-p_0,p_m)` is `(-c_0, +/- Y_m)`. Both endpoint caps are present. Thus its tangent variation is bounded by half the variation of `log c_0` plus half the variation of `log Y_m`, exactly the `V_end` appearing in the draft. Reversal gives the terminal-angle side with no change in absolute variation.

## 5. Exact regular flux and all four endpoint distinctions

The actual roof-angle coarea coefficient is

\[
 A=\frac{\omega}{4\pi c_*\chi}
  =\frac{u_x}{4\pi c_*h_x},
 \qquad h_x=R^2 e^{\mathsf T}G^{-1}e
          \ge R_-^2/\Lambda_\circ.
\]

Accordingly `A<=F_cs u_x`, with
`F_cs=Lambda_circle/(4 pi c_* R_-^2)`. Both the physical collision-area normalization and the original conditional factor are present. A regular physical side is counted once. The difference of its incident record weights multiplies this one-copy coefficient; adding the two traces separately would require a separate factor two.

At a horizontal endpoint `p_0=b != 0`, the exact polar differential under the true terminal momentum parameter v is

\[
 |d\arg(-b,v)|=\frac{|b|}{b^2+v^2}\,dv.
\]

Its integral over the endpoint cap is at most pi, uniformly in b, so the native pointwise kernel gives `E_hor=pi F_cs C_mom`. It is not bounded by `pi/2` uniformly for arbitrary section levels b. At b=0 the regular punctured polar angle is constant on each side of v=0 and the regular charge is zero; the critical incoming fan at the origin remains separately paid by the base physical source theorem.

For comparison, module 323's four artificial endpoint-cap sides have `|b|=a` and `|v|<=a`, so each integral is exactly `pi/2`, and their total is `2 pi`. This yields `Lambda_circle C_mom/(2 c_* R_-^2)`. Thus the different endpoint constants in 323 and 324 are consistent; a `pi/2` value for general section sides would have been an error, but the written 324 uses pi.

At a vertical endpoint, `u_x=1/(R c_0X_m+Y_m)<=1/Y_m`. The whole-interval supremum sum for the actual vertical source, multiplied by `F_cs V_end`, gives `E_ver`. No initial incidence is divided out. Time reversal covers both terminal endpoint types.

For an internal side, multiply its per-overlap turning bound by the full inverse-weight overlap sum. Restriction to the finite side of a rectangle or an additional positive Borel subsource can only reduce this positive charge. No differentiation or component count of that restriction occurs in the canonical-source theorem itself.

## 6. Original section, occupation convention and exact jump accounting

The original section consists of four squares and one rectangle. Each rectangle has two horizontal and two vertical sides, so its total is ten of each type, with their actual levels and side intervals. A square across the circular seam is glued there; the numerical seam is not another physical side.

The fixed lifted word fixes the displacement K. The occupation is

\[
 A_m=\sum_{j=0}^{m-1}\eta_R(T_R^j x).
\]

The exact record uses `eta_R(x) eta_R(T^m x) 1_{K=k,A=n}`. The marked twist uses the same endpoint factors times `exp(i(xi.K+zeta A+upsilon m))`. The initial visit contributes to occupation; the terminal visit is tested separately and does not create a term at j=m.

Within each regular word, all these weights are locally constant off the preimages of the original finite sides. A single changed interior visit changes A by one. The exact indicator jumps by at most one, while the unit-modulus twist has jump `2 |sin(zeta/2)|`. Coincident visit boundaries can be paid by telescoping one changed visit at a time. This is an upper bound by actual side occurrences, not a multiplicity claim that they are disjoint.

At the initial boundary the exterior weight is zero because of `eta_R(x)`. Crossing changes the complete product from zero to one complex number of modulus one; the initial occupation phase is part of that interior value. Its cost is one, not an additional interior-twist cost. The terminal endpoint factor likewise costs at most one and carries no new occupation at index m. Thus the endpoint budget is correctly independent of zeta.

For each fixed side type and level the internal depth sum is at most `2/(1-sigma)`. With ten sides of each type this yields

\[
 B_{\rm sec,int}
  =\frac{2(10C_{\rm hor}+10C_{\rm ver})}{1-\sigma}.
\]

Both endpoint indices together cost

\[
 B_{\rm sec,end}=2(10E_{\rm hor}+10E_{\rm ver}).
\]

There is no factor m. For m=1 the actual interior collection is empty and the displayed coarse uniform upper bound remains valid.

## 7. Why this proves BV for the specified finite tests, not arbitrary selectors

Density domination is used only to establish absolute continuity, pointwise height, and the modulus bound for the complex density. It cannot prove bounded variation; the explicit arbitrary-Borel counterexample retained with module 323 continues to apply.

For the new BV conclusion, module 325 actually differentiates the finite section tests. On each regular `(t,theta)` chart, each side equation is analytic. On a compact regular fixed-angle interval, a nonconstant analytic side function has finitely many zeros. Constant-zero angular slices form a null set: in a local analytic product chart, an accumulating set of such theta values would force every t-power coefficient to vanish identically, hence the whole side function to vanish on an open set. A genuine canonical side under a regular iterate cannot do that, since the iterate is a local diffeomorphism. A countable chart cover and exhaustion cover the full regular source.

Inside every resulting chamber the record multiplier is constant, of modulus at most one. Its interior derivative is therefore bounded by the original unweighted or guarded derivative already paid in module 323. Artificial subdivisions cancel before absolute values.

At true unvisited boundaries and artificial cap boundaries, multiplication by a bounded one-sided trace cannot increase the positive base charge. At visited grazing the original optical trace is zero. At a positive visited critical endpoint, the finitely many original side inequalities have almost-everywhere ray limits: their first nonzero homogeneous analytic terms have finitely many zero directions. Consequently the exact record or phase has a ray limit of modulus at most one and its incoming charge is dominated by the complete positive critical sector charge already paid in 323. No zero-area critical source is silently deleted.

The remaining regular section interfaces contribute their actual jumps times one-copy flux, with the budgets reconstructed above. Integrating by parts over finite chamber exhaustions is legitimate after angular integration because all absolute interior, physical-endpoint and section-jump budgets are finite. The source integral against the test-function derivative is integrable. This produces the stated real or complex distributional derivative of finite variation. It is an explicit finite-test argument, not BV inheritance through measure domination.

## 8. Conditioning, support and Fourier scope

The original initial factor restores the exact source normalization:

\[
 c_*^{-1}\int\eta_R\,d\nu=1.
\]

Thus both positive exact-record mass and complex total variation are at most one. The larger unconditioned cap majorant has only the `c_*^{-1}` mass bound, and the draft correctly distinguishes them. The terminal section is retained. The physical roof is still the sum of the actual m flights, so support stays in `[m tau_-,m tau_+]`.

The variation budgets are therefore

\[
 D_{\rm exact}^w=D_{\rm base}^w+B_{\rm sec,end}+B_{\rm sec,int},
\]

\[
 D_{\rm twist}^w(\zeta)
 =D_{\rm base}^w+B_{\rm sec,end}
  +2|\sin(\zeta/2)|B_{\rm sec,int}.
\]

The latter is uniformly bounded by replacing its sine factor by two. The roof Fourier inequality follows from the actual finite derivative measure and the L1 bound, giving `min(1,D/|s|)`. Translation in L1 is bounded by `D |h|`, including for a complex density, by integrating the total variation measure. Squaring the high-frequency majorant gives the two-sided tail `2D^2/S`.

These bounds are uniform in the discrete-mark frequencies because they enter only in constant phases or the already bounded visit jump. They retain displacement, exact occupation, the collision-count phase, and physical roof frequency. The `|s|^{-1}` majorant is not integrable over the whole high-frequency line and does not pay collision-normalized `m^2` pointwise inversion by itself. No contrary claim is made in the drafts.

## Reconstruction outcome

No defect was found in the inspected 324/325 implication after these source-class, determinant, cap-flux, jump, conditioning, critical-sector and BV-scope checks. The boundary factor two is used where there are two endpoint indices; regular section interfaces are paid once by their jump. The initial occupation and final conditioning conventions match the original model. The new exact-record BV theorem uses the actual finite geometry of the original section and does not assert BV for arbitrary dominated Borel selectors.

This is an internal author reconstruction against the exact hashes above. It does not certify external theorem inputs or convert auxiliary finite checks into proof of the continuous physical dynamics.
