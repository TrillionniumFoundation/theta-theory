# Author-side mathematical check: physical volume and original-roof height

This is an author-side derivation and verification record for the current
revision. It is not a new referee report, a journal decision, or independent
human specialist certification.

## New mechanism and actual scope

Module 310 proves original-roof essential-height payment for the full
observable exceptional source of module 309 **on the already constructed
guarded critical-tube union**. Module 311 extends the physical volume
mechanism to **all regular physical records satisfying the stated original
depth guard and endpoint cap**, including records without a physical critical
origin. The extension uses a finite momentum grid and a uniform overlap
bound, not an assumed density at a source-selected momentum value.

The physical model is unchanged: original triangular lattice and circular
scatterers, radius in `[9/20, 47/100]`, actual first-hit collisions, original
clock `L_m`, original section, exact displacement/occupation/terminal tests,
and collision probability `d alpha d p/(4 pi)`, conditioned on the original
initial section exactly once when evaluating the requested source.

## Checks of the critical-tube proof (310)

1. **Physical injectivity and disjointness.** A physical initial state has a
   unique finite lifted word. Every point of a tube carries its center's
   word by the previously proved physical continuation theorem 292. Two
   critical centers of the same word coincide by the global disk-product
   certificate in 297. Thus distinct-center tubes are physically disjoint;
   no optical multiplicity was hidden by a chart assignment.

2. **Both directions of optical distortion.** The absolute derivative bound
   for `log u` in 293 yields both `u <= C_dist u_center` and
   `u >= u_center/C_dist` on the common physical endpoint segment. The proof
   does not infer lower density from an upper estimate alone.

3. **Unconditioned volume normalization.** On a disk of momentum radius
   `rho_epsilon`, the original collision source has density `u/(4 pi)`.
   Therefore its mass is at least
   `rho_epsilon^2 u_center/(4 C_dist)`. In particular neither `R` nor
   `c_star` enters this lower volume. The original conditioned roof density
   has its single `1/c_star` factor later.

4. **Source saturation uses whole physical tubes.** If a tube contains a
   clearance/incidence/collar witness, every point of that tube satisfies
   the appropriately enlarged witness. Endpoint path diameter is at most
   `2 s_epsilon`, so the transport constants are exactly
   `4 C_Delta s_epsilon` and `4 C_c s_epsilon`, times `sigma^depth`.
   The full least clearance is Lipschitz under Hausdorff movement of a
   segment; all third centers and changes of nearest center are included.

5. **Tangential momentum and terminal state.** Differentiating the actual
   tangential component gives the same constant `C_c` as incidence.
   At the terminal contact the incoming velocity is used; specular
   reflection preserves its tangential component. The resulting circle
   distance is no larger than the lift distance. Thus no endpoint section
   test or terminal flight is omitted.

6. **Physical positive-source sum.** The invariant marginal bounds are
   `nu(clearance <= u) <= u/R_minus`,
   `nu(incidence <= u) = 1 - sqrt(1-u^2) <= u^2`, and
   `nu(section collar <= u) <= u/(2 pi)` in their respective proved
   ranges. At most two contacts/flights have a given depth. The union bound
   therefore includes the full positive physical source without a word
   cardinality or independence assumption.

7. **Original-roof coarea and critical origin.** In polar endpoint momentum,
   `dt = r h dr` and `d zeta = r dr d theta`. The factors `r` cancel
   for unweighted bulk source. At a fixed roof/angle each tube contributes
   at most one point. Integrating `2 pi` in angle after the positive
   coefficient sum yields exactly
   `2 U C_dist^2/(c_star rho_epsilon^2)` times the enlarged physical
   source mass. This is an actual common-roof estimate, not a synchronized
   momentum estimate evaluated at different unproved points.

8. **Exact width certificate.** The displayed
   `D_cv = 20,861,442,654` is deliberately conservative. It follows from
   the exact Bernoulli certificate `q_a^kappa <= 1/2`,
   `kappa=3,263,680`, and `sigma^4 < 1/2`. Bounds
   `A_Gamma <= 12552`, `A_c <= 4`, `A_phi <= 485` and the exact tube
   diameters certify all clearance, incidence and collar regimes without
   evaluating an enormous floating-point power.

9. **Original linear multiplier.** On physical half-guard tubes the actual
   `I_m = 1 + sum q0^depth/c_i` obeys
   `I_m <= 1 + (4/epsilon) q0^(3/4)/(1-q0^(3/4))`. This uses precisely
   the inherited `q0=47/53`; the anchor contraction `q_a` is not substituted
   for this guard. The bound is uniform in collision count at each fixed
   positive guard width.

10. **Order of limits.** All source bounds hold at every finite `m,D`.
    Substitution `D=ceil(theta m)` is made into those exact inequalities.
    The guard width is fixed before the collision limit. The output is a
    vanishing `m^2 L_infinity` height on the stated source, uniformly in
    radius, exact labels, roof, and bounded source selectors. No outer
    width or microscopic observation event is changed.

## Independent challenge of the general physical atlas (311)

The first complete draft at
`311_finite_overlap_physical_source_height.tex` was read separately from
the derivation of 310. The following construction was checked.

- The original endpoint cap `5/6` has a positive spare margin:
  `5/6+1/64=163/192<17/20`, giving endpoint incidence greater than `1/2`.
  The physical endpoint ball of radius `a_epsilon` lies strictly inside
  the already proved physical continuation domain.

- Minimizing the true action minus the desired linear momentum term on
  this already physical ball gives a common inverse momentum neighborhood.
  Its outward radial derivative is strictly positive. Strong convexity
  gives both the unique inverse and the required displacement bound;
  no assertion of physicality follows merely from stationarity.

- At each fixed word and momentum grid point, global equal-momentum
  injectivity follows directly from the support-sum inequality 265.
  It remains valid across disconnected physical domains. Thus a tube
  built from one assigned source representative covers every other
  source point assigned to the same pair when their momenta lie in it.

- Each actual point has one physical word. A disk of radius `2 rho`
  can contain that point's momentum for at most 25 points of the grid
  `rho Z^2`: at most five choices per coordinate. This bounds all tube
  overlap before summation, regardless of the number of physical words
  or grid points. Finite grid size is not an extra factor in the bound.

- A radius-`2 rho` momentum disk has area `4 pi rho^2`; hence its
  unconditioned mass is at least `rho^2 u_center/C_dist`. Combining
  this with overlap 25 and the roof angular integral gives exactly
  `25 U C_dist^2/(2 c_star rho^2)`, as stated in the draft.

- The roof metric calculation extends to the componentwise endpoint
  cap because its lower bound uses only endpoint incidences. It does
  not require the vector momentum norm to be less than one. The draft
  explicitly performs this extension before using radial coarea.

- A disk not centered at the momentum origin has an interval intersection
  with every momentum ray. Strict radial monotonicity holds there;
  global roof-angle uniqueness 265 also prevents extra roots from
  disconnected exact-event cuts. The inverse momentum image need not
  be assumed convex in endpoint angles: the constructed image stays in
  one physical endpoint ball, which contains every straight segment used
  for distortion and observable transport.

No mathematical gap was identified in these stated construction steps.
This statement describes this author-side check of the draft and is not
independent specialist certification of the entire inherited manuscript.

## The proposed inverse-gradient volume extension

The separate proposed extension was also checked algebraically. For
actual source with `|zeta|<rho`, its physical inverse neighborhood contains
the whole disk `B(0,2 rho)`. Global wordwise momentum injectivity gives one
regular critical center per word and disjoint origin-centered tubes.
The same lower tube volume pays the full selected center sum.

The exact radial bound `h<=2R_plus` gives
`t-a <= R_plus r^2`, hence
`1/r <= sqrt(R_plus)/(sqrt(t-a))` on its physical radial arms.
Consequently the actual insertion `I_m/|grad_q F|`, with
`|grad_q F|=R r`, has a critical-roof envelope proportional to
`sum u_center (t-a_center)_+^(-1/2)`. Its roofs remain their own actual
physical critical values; they are not identified or shifted.

For a Borel roof set of finite measure `ell`, the exact layer-cake bound is
`integral_I (t-a)_+^(-1/2) dt <= integral_0^infinity min(ell,v^-2) dv
=2 sqrt(ell)`. The noncritical `|zeta|>=rho` part is controlled by
the already proved bulk height times `I_m/(R_minus rho)`.
The actual physical roof support has length at most
`m(tau_plus-tau_minus)`, so the resulting polynomial window losses can
also be paid against the exponential deep-source bound when integrating
over the full physical roof support. This remains an interior positive
volume estimate, not an unproved estimate of a separately prescribed
singular endpoint or paired trace measure.

## Remaining limits

At fixed finite `m`, the union of positive guard classes exhausts the
regular physical source. The proved cost grows as `epsilon^-2`, so this
fact alone provides no uniform normalized limit on the unguarded
complement. In particular, a dyadic clearance-shell argument cannot
silently combine a first-order collar mass with this inverse-square
volume cost. The original shallow source, boundary source, comparison
capacity, singular trace payment, spectral/arithmetic inputs and
conditional denominator remain to be proved in their original order.

## Executed auxiliary checks

`check_critical_tube_volume.py` was run normally and with Python `-O`.
Both passed, with identical stdout and empty stderr. Exact current
receipts and output are in `critical-tube-verification/`.
The checks verify inverse-Jacobian algebra, the `R`, `pi`, `c_star`
normalization, rational width certificates, 32,896 finite depth
multiplicities and all 94 partial block positions in the geometric
tail. These checks supplement the written continuous proof; they do
not certify physical continuation, global source coverage, or the full
local limit theorem by computation.
