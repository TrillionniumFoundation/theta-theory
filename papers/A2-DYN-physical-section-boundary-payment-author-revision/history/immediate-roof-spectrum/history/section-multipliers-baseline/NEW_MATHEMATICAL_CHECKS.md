# Mathematical reconstruction and checks of native 333--335

Audit date: 2026-10-23. These are author-side mathematical checks of the actual new proof bodies and their explicit inherited interfaces. They are not a new referee review, a journal decision, or an independent expert reconstruction of the entire historical dynamical chain. The full proofs are in the native LaTeX source; the finite programs described below are auxiliary checks.

## 1. Fixed model, observable and quantifier scope

The physical model throughout is the original triangular periodic Lorentz gas with circular scatterer radius `R in [9/20,47/100]`, genuine first collisions, unit speed, the original section `Y_R^*`, collision probability `d alpha dp/(4pi)`, and `c_*=91/(10000pi)`. No marked clearance foot is made into a reflection. The full physical collision count is `m>=1`. The occupation counts times `0,...,m-1`; terminal section membership is separate. The four observed coordinates are `(k_1,k_2,t,n)` at that fixed collision count, so Fourier inversion has three torus coordinates and one real roof coordinate.

| Result | Radius and collision scope | Labels and observations | Roof or boundary scope | Conclusion actually established |
|---|---|---|---|---|
| 333 section multipliers | Uniform original radius interval; no collision dependence in multiplier constants | Exact section indicator and occupation phase | Original unsmoothed rectangle sides | Explicit strong multiplication and a weak moving-section bound on the qualified common construction |
| 334 exact interval inversion | Every `R,m`; uniform inherited variation budget for the specified tests | Every exact occupation/displacement label; specified smooth endpoint tests and trajectory phases | Any actual bounded interval union, with its exact positive length | Absolutely convergent interval formula, paid sharp cutoff and actual-event conditional test |
| 334 raw bridge | All radius and label suprema; original central region | Original raw arithmetic reference | Width fixed at outer stage before collision limsup | Retained native 87 pays the fixed-window scalar comparison and reference modulus; normalized local charge remains a sufficient closing condition |
| 335 selected endpoint kernel | Uniform `R,m,j,a,v`; `a,v in (-1,1)`, `0<=j<m` | Complete regular roots; arbitrary original selectors by positive restriction | Actual unvisited clearance event, `0<delta<=delta_*` | Kernel `C_end(delta+theta_r^max(j,m-1-j))` |
| 335 critical tightness | Same physical parameters; finite germ limits before positive exhaustion | One-copy original exact records and critical-value restrictions | Positive visited incidences; actual physical sides with finite analytic conditions | Complete unscaled leading coefficient bound; no common-roof nonleading remainder or normalized raw height |

## 2. Native 333: explicit section interface

### Geometry and coordinate scaling

The arclength stable slopes have magnitudes between `100/47` and `170/9`. Since `s=R alpha`, multiplying by the extreme radii gives the common containing slopes `45/47` and `799/90`. This inclusion is geometric and does not assert invariance of all arcs in the enlarged family. The two coordinate maps have uniformly bounded derivatives on the actual compact radius interval. Strong and weak comparisons must be made on the stated fixed norm construction or explicitly qualified radius-specific spaces; no unproved identification of different dynamical spaces is used.

For a graph `varphi=varphi(alpha)` with derivative `v`, the arclength ratio between `(s,varphi)` and `(alpha,varphi)` is

`sqrt(R^2+v^2)/sqrt(1+v^2)`.

It is positive with uniform bounds for the displayed radius and slope ranges. This confirms that the geometric restriction and transverse-angle calculations have no hidden singular radius factor.

`lem:sm-grid` partitions using at most ten coordinate side values of each orientation. The `11*11=121` count includes the common angular seam outside the section rectangles. For tangent `(1,v)`, the sine angle with a vertical side is at least `1/sqrt(1+Kbar^2)` and with a horizontal side at least `abar/sqrt(1+Kbar^2)`. Thus `eq:sm-transversality` is a simultaneous lower bound for all sides, including artificial seams.

### Moving-side derivative and grazing cap

The derivative estimate in `lem:sm-grid` uses the actual defining polynomial of the physical root. On the whole enclosing interval `49/100<=q<=53/100`, its displayed bound gives `F_q<=-2.6842844<-2`, while `0<F_R<6`. Implicit differentiation therefore gives `0<q'_R<3` and `|theta'_R|<6`. The original momentum side coordinates stay strictly inside `|p|<5/6`, so `p=sin(varphi)` gives side speed at most `36/sqrt(11)<11`. This is a compact geometric bound, not a sampled plot or an inference about long-time collision derivatives.

### Strong multiplier, weak perturbation and physical pairing

`thm:sm-multipliers` uses constant values on each cell, so the piecewise Hölder norms equal their constant magnitudes. `eq:sm-analytic` follows from the idempotence of the exact indicator. For real frequency `zeta`, the cell values have modulus one; no factor proportional to `|zeta|` is needed for this multiplier estimate.

For `thm:sm-moving`, the eight swept strips have widths at most `11|R-S|`. Both stable-arc coordinate speeds have a uniform positive lower bound. Each nonzero subarc has length at most `11|R-S|/vartheta_sec`; partitioning at both grids and allowing the seam costs at most 82 pieces. The strong stable norm gives `|integral_V h psi|<=||h||B |V|^alpha ||psi||C^q`. Restriction of a unit weak `C^p` test has a uniform `C^q` bound because `q<p`. Summing proves the exponent `alpha` in `eq:sm-weak-move`; it is not a claim about the perturbation exponent for the collision map itself.

The density convention in `cor:sm-transfer` is relative to the original `nu`. Thus `1` represents `nu`, and `M_eta 1` represents the original unnormalized section measure. The occupation multiplier is placed before each collision; the final `M_eta` is a separate endpoint test. There is exactly one division by `c_*`. A bounded physical realization of the other twist is an explicit hypothesis of this corollary. Entire occupation multiplication by itself does not supply that realization or spectral estimates at all roof frequencies.

**Priority check:** historical native 77 and 84 already contain the corresponding multiplier and weak-motion arguments. Native 333 supplies explicit constants and makes the external assumptions inspectable. It is not presented as a newly discovered spectral theorem. Written fixed-band native 84--87 remain preserved.

## 3. Native 334: unchanged intervals and exact normalization

### Inversion, signs and absolute convergence

`eq:ui-transform` is the Fourier transform of the exact physical record law with the original section conditioning. The positive mass bound and total derivative budget are those of `thm:wo-bv`, summed over all exact labels before taking parameter suprema. With the plus-sign transform convention,

`F(theta,s)=sum_j exp(i theta.j) integral exp(i s t) f_j(t) dt`.

The inverse uses `exp(-i theta.j) widehat(1_I)(-s)` and the factor `(2pi)^-4`. Three full torus integrals select exactly the given label. None of the arithmetic peaks or zero classes is omitted.

For a union of at most `J` bounded intervals of total length `d`, direct integration yields

`|widehat(1_I)(s)|<=min(d,2J/|s|)`.

The exact marked transform satisfies `|F(theta,s)|<=min(A_V,D_V/|s|)`. Their product is bounded near zero and by `2J D_V/s^2` in the tail. This proves genuine absolute convergence of `eq:ui-inversion`. The compact kernel used in its proof is an intermediate approximate identity. The inherited BV translation estimate gives convergence in `L^1`; the just-proved integrable bound permits dominated convergence on the Fourier side. No smoothing survives in the resulting interval event. Absolute continuity of the physical roof law justifies either convention for interval endpoints.

### The exact sharp cutoff

After torus integration and the two real tails, the correct scalar coefficient is `D_V/pi`. The remaining positive integral is

`integral_S^infinity min(d/u,2J/u^2) du`.

It equals `d[1+log(2J/(dS))]` when `dS<=2J`, and `2J/S` when `dS>=2J`. Both formulas agree at equality. The integrand is always at most `2J/u^2`, so the coarser bound `2J D_V/(pi S)` is valid also below the crossover. `thm:ui-inversion` does not assert positivity of the sharply truncated integral.

For different windows at different labels (`cor:ui-all-labels`), torus orthogonality is used first and each component is charged to its own `||Df_j||TV`. The sum of these charges is at most `D_V`. Charging the total budget separately to every label would be wrong and is not done. Finite horizon makes the attained label set finite at fixed `m`, but no constant depends on its size.

### Original `m^2/d` payment and the conditional denominator

`cor:ui-normalization` multiplies the actual event error by `m^2/d`, giving

`2J D_V m^2/(pi dS)`.

Choosing `S=m^(P+2)/d` pays this explicit tail by `2J D_V m^-P/pi` whenever the displayed variation budget is uniformly bounded. The formula permits arbitrarily small original windows; it does not provide a spectral evaluation on that large band. The collision count is never silently replaced by physical roof time or an induced return count.

For `prop:ui-conditional`, `p` is the mass of exactly the selected original event and `N` is its tested mass. The errors are `|p-D_S|<=E_0`, `|N-N_S|<=E_V`. The certificate `D_S>E_0` implies `p>0`. Using `|N|<=A_V p`, the exact identity

`N/p-N_S/D_S=(N-N_S)/D_S+N(D_S-p)/(p D_S)`

gives `(E_V+A_V E_0)/D_S`. This is the denominator actually appearing in the certificate; no containing event or asymptotic average probability is substituted. If `p=0`, the certificate cannot hold. The tested conditional conclusion is restricted to the explicit smooth endpoint and trajectory-phase observations; it is not a total-variation assertion for arbitrary Borel information.

### Ordered raw bridge and analytical spike

For `prop:ui-raw-bridge`, the exact-label density is extended with its existing physical support and complete derivative measure. At a Lebesgue point `t`, its distance from the average over `(t-h_B,t+h_B)` is at most the variation charge of the closed interval. Inserting the exact average, its sharp cutoff and the reference average gives four separately displayed terms: normalized local variation, reference modulus, full-band comparison, and the paid Fourier tail. All radius and label suprema are applied after those valid pointwise estimates.

The analysis width `h_B>0` is fixed before `limsup_m`. The outer limit in `B` comes last. A frequency cutoff may depend on `m`; this does not exchange the physical geometric limits. The bandwidth `m^(P+2)/h_B` directly pays the explicit last term. The subsequent proposition applies the retained fixed-window theorem to identify which other terms have already been paid by the historical chain.

### The retained fixed-window theorem pays the scalar comparison

`lem:ui-reference-modulus` and `prop:ui-inherited-bridge` use exactly the original event and finite-peak reference in current `model.tex`, including continued branches off the unit circle. Historical native 87 gives `E_m(h)->0` for every fixed `h>0`, where

`E_m(h)=sup_R,n,k,t |m^2/(2h) integral_(t-h)^(t+h) p(u) du - L(t)|`.

This theorem is invoked at its inherited analytic scope, with no claim that its full spectral dependency chain has newly been independently certified. Its fixed-window quantifier permits `h=h_B` at each fixed outer stage; it does not permit an arbitrary collision-dependent window.

The reference modulus is checked directly from its finite Gaussian sum. Put `kappa_j=-log|z_j|>=0` and let `b_j` be the roof coordinate of the real peak. The retained no-roof-resonance input gives `kappa_j=0 => b_j=0`; it does not set the roof coordinate of every nonunit continued branch to zero. Continuity on compact parameter supports therefore implies

`omega_m=max_j sup_R |b_j| exp(-m kappa_j) -> 0`.

Indeed the part with `|b_j|<epsilon` costs at most epsilon, while its complement has a strictly positive minimum damping exponent. The common lower bound `Re H_j>=a I_4` gives Gaussian bounds `M_0=(2pi)^-2 a^-2` and `M_1=M_0 sqrt(2/(pi a))` for `|G_H|` and `|partial_3 G_H|`. Thus

`sup |partial_t L| <= D_m=(N_pk B_pk/c_*)[M_0 omega_m+M_1 m^-1/2] -> 0`.

The average absolute displacement on the symmetric interval is `h_B/2`, so `Omega_g<=h_B D_m/2`. The estimate holds globally in the roof target, and does not need an enlarged central window. The triangle inequality through the actual interval probability gives

`Xi <= E_m(h_B)+h_B D_m/2+D_all^1 m^2/(pi h_B S_mB)`.

All three terms vanish with `B` fixed and the stated cutoff. This is an evaluation of a particular scalar integral; it is not an assertion of a new strong spectral gap on growing bands. An even sharper direct estimate inserts the exact interval average without Fourier truncation:

`raw_error_m <= Omega_p(m,B)+E_m(h_B)`.

Consequently `E_M <= limsup_m Omega_p(m,B)` for each fixed `B`. Under the retained fixed-window theorem, the sole additional sufficient condition on this route is `lim_B limsup_m Omega_p(m,B)=0`. The condition is not asserted necessary. This use of an already written theorem prevents an inherited fixed-window evaluation from being incorrectly relisted as missing work.

The analytic example `q_m=m^-2 1_[m tau_0,m tau_0+exp(-m)]` has variation `2m^-2`, mass `m^-2 exp(-m)`, vanishing normalized fixed-window integrals and vanishing normalized sharp expressions on every polynomial band, but normalized essential height one. Its derivative charge remains visible locally. This verifies that the local-variation hypothesis cannot simply be dropped from that inference. It is not claimed to be an actual billiard source or a counterexample to the physical research objective.

## 4. Native 335: complete clearance-selected endpoint kernel

### Exact first-image density and length budget

The new `lem:ce-first` was reconstructed against native 284 (`eq:mc-density`) and 327 (`lem:lc-cover`, `eq:lc-source-budgets`). The horizontal source is unnormalized `d alpha_0`. On a first physical image,

`rho=d/[R A sqrt(1+V_1^2)]`, `A=sqrt(1-a^2)+tau/R`, `d=cos(varphi_1)`.

The bound `A>=t_*/R_+` pays even arbitrarily small initial incidence. At fixed `R`, the radius cancels in the ratio of two densities on one curve. A target homogeneous strip bounds its incidence ratio by `C_H`; the other factors give exactly `D_first` in `eq:ce-first-ratio`. Hence `sup rho |C|<=D_first integral_C rho`.

At most `K_c` initial cover intervals per preliminary arc multiply the inherited first-image supremum budget by `K_c`, giving `S_first`. Their exact integrals sum to at most `J_0 L_c delta/R_-`, because the cover is disjoint after merging and `ds=R d alpha_0`. Thus `M_first` retains actual selected source length. No density ratio is claimed across different grazing strips. Every covered state is evolved to its actual first collision, including states added by a positive overcover.

### Collision indexing, terminal Jacobian and roots

For `j>=1`, the substitution into `thm:lc-local-half` is `h=j-1`, `n=m-j-1`, so `l=h+n+2=m`. For `j=0,m>=2`, the count is exactly `1+(m-2)+1=m`. The complete renewal gives `Gamma S_first theta_r^(m-2)+C_ell M_first delta`; `eq:mc-last-cancellation` multiplies by `J_f/(k_-t_*)`. The factor `theta_r^-1` is included in `C_first` before writing the exponent `m-1`. At `m=1`, the unselected one-flight derivative bound supplies the stated constant.

The last physical collision is handled before any infinite terminal homogeneous subdivision. Its exact cancellation removes the terminal incidence factor and gives the derivative lower bound `k_-t_*`. Thus no terminal grazing loss has been erased by an unsupported inequality. Intermediate singular preimages retain the inherited zero-arclength proof; no physical derivative is assigned at a visited tangency.

Almost-everywhere coarea alone would not prove the displayed value at every regular root. The proof correctly fixes finitely many strict selected roots, continues their inverse branches and witnesses locally, and uses continuity of their positive weights. It then exhausts finite root collections. Artificial coordinate and homogeneous seams represent a physical root once.

### Reversal gives the longer direction

In `(alpha,p)` coordinates the physical map has determinant one. The lower-left entry of its inverse has the same magnitude as the original lower-left entry. Conjugation by `(alpha,p)->(alpha,-p)` therefore preserves the inverse root weight. Recentring the terminal scatterer in the lattice quotient is unique; invertibility prevents two distinct original physical roots becoming one reversed root. The endpoints become `(-v,-a)`.

For a selected flight, the same disk and foot remain unvisited, its foot coordinate becomes `tau-t_z`, and its index becomes `m-1-j`. Thus the reverse forward estimate has exponent `j`. Taking the smaller of the two estimates yields `theta_r^max(j,m-1-j)` in `eq:ce-kernel`. No multiplication of event probabilities, conditional independence, or Markov composition occurs. Restoring the section measure costs exactly `1/(4pi c_*)` in `eq:ce-joint`.

### Actual critical sides and coefficient normalization

The proof of `thm:ce-critical` was checked against native 285 (`eq:mc-sector-comparison`, `thm:mc-critical-sectors`) and 322 (`pc:representatives`). At fixed `R,m,j` and a finite one-copy germ family, a limiting width at most `delta` lies in the strict width `delta+eta` event on sufficiently small actual physical-side neighborhoods. Interior feet persist; limiting zero-clearance witnesses are approached on the positive unvisited side. All visited incidences remain positive.

The relevant inequality is the unconditioned fibre root bound. Physical inverse branches are disjoint after one-copy merging. Their weights are continuous, and finite analytic inequalities have angular limits away from finitely many rays, including when an active inequality has higher-order leading Taylor term. Polar Fubini and bounded convergence along good radii give the selected sum `sum u_x beta_z`. Only then are `eta` sent to zero and finite families exhausted. The angular Jacobian comparison contributes `lambda_max(G)/(2 R^2 c_*)`, bounded by `U_2/(2c_*)`. This is precisely the constant in `C_crit`; there is no additional radius or `4pi` factor.

For the full original guard, at most two flights occur at each depth. Its widths sum to at most `4 epsilon(B)/(1-q_0^(1/4))`, while the transient sum is at most `m theta_r^((m-1)/2)`. Taking the collision limsup first removes the latter. Only the subsequent original outer limit removes the former. This proves unscaled leading-coefficient tightness, including the shallow endpoint layers in that norm.

It does not prove `m^2 L^infinity(dt)` payment. At fixed `B`, multiplying the first term by `m^2` is not a vanishing bound. Finite-germ local limits do not provide a common neighborhood, an all-germ sum of nonleading coarea errors, or a comparison at different momentum values corresponding to a common roof. The original shallow same-pool shortage and raw local limit remain explicit research obligations.

## 5. Actual finite verification and its limits

The retained execution of `verify_exact_interval_inversion.py` reports seven check groups PASS in `exact_interval_verification.json`: symbolic tail integration/crossover; 36 exact rational normalization cases; the four-coordinate Fourier coefficient; 60 closed-form sharp interval calculations at 90 decimal digits; exact conditional denominator algebra; the analytical spike limit; and exact Gaussian majorants `M_0`, `M_1` together with the symmetric-window average `h/2`. The tested examples include unions of intervals, complex box densities, widths down to `10^-21`, and cutoffs up to `10^24`. The maximum observed numerical error/bound ratio was `0.6404705763387595116500103`. The actual environment was Python 3.12.14, SymPy 1.14.0 and mpmath 1.3.0. The script does not certify compactness, the absence of roof resonances, or the retained spectral dependency chain.

`verify_endpoint_kernel_algebra.py` and `endpoint_kernel_algebra_results.json` report PASS for 20,100 finite collision/reversal index checks, 200 finite guard/transient count checks, 630 exact area-preserving matrix examples, six normalization checks, and an explicit check that no false normalized closure is asserted. These checks corroborate formulas and indexing. The continuous first-hit geometry, complete singular partition, countable positive exhaustion and local sector passage are mathematical arguments in the proof bodies, not consequences of the finite program.

Compilation, reference-resolution checks, source-identity checks and continuous-integration execution are separate evidence classes. A successful build cannot prove a geometric estimate, spectral gap, or raw local limit. The actual build and remote CI records must be reported from their own completed executions, not inferred from these mathematical script results.

## 6. Remaining minimal closure, without changing the target

The new results preserve all original observations and normalization. On the scalar analysis-window route, after applying the retained native 87 theorem at its original scope, a bound paying the complete normalized local derivative charge is sufficient. The present global BV bound does not supply it. The original same-pool positive-source shortage remains the alternative native closing condition. A new strong estimate on growing frequency bands is a possible additional research route, not a logical prerequisite of this fixed-window implication. Other observation classes or collision-dependent microscopic asymptotics must use their own actual hypotheses and cannot inherit a wider conclusion silently.

The inherited fixed-band native 84--87, the arithmetic reference, conditional microscopic event probabilities, and the long-time inverse Jacobian keep their input-specific scope. Their written proof bodies remain intact. No independent expert reconstruction of all these dynamical inputs is claimed. The distinction between a proved finite algebraic estimate, a theorem conditional on inherited native estimates, and full completion of the physical raw pointwise target is maintained throughout.
