# Mathematical audit of the new proof bodies

This is the author's explicit derivation audit, not a new referee report or a formal certificate. The actual program outputs are auxiliary evidence in `build/radial`; they do not prove continuous geometry or an infinite-time theorem.

## 286: signs, units and matrix bounds

With `D=diag(-1,1)`, the physical first variation is `grad_q F=R D zeta`. Differentiation gives `D_q zeta=R^{-1}DG`, so `D_zeta q=R G^{-1}D` and `grad_zeta L=D(G/R^2)^{-1}D zeta`. Both matrix order and the two factors of R are retained. `D` is its own transpose/inverse; no angle-dependent Hessian square-root differentiation is substituted for this exact identity.

The full second variation minimizes over actual interior reflection coordinates. The positive endpoint term proves `G >= R diag(c_0,c_m)`. On `|zeta|<rho`, `c_0,c_m >= sqrt(1-rho^2)`, hence `G/R^2 >= (100/47)sqrt(1-rho^2) I`. For `m>=2` the unreduced endpoint block is diagonal, each entry divided by `R^2` at most `20/9+50/3=170/9`; the Schur term is positive semidefinite and subtracted. For `m=1` the mixed block is present, and the row-sum bound is `20/9+100/3=320/9`. The exceptional one-flight constant is not suppressed. No interior `c_i` is bounded below.

The map `(alpha_0,p_0)->(p_0,p_m)` has determinant `-partial_alpha0 p_m`. Its reciprocal magnitude is `u=R|G_0m|/det G`, by the exact generating matrix. The positive optical denominator makes `G_0m` nonzero at every regular finite physical orbit; near-zero values are not rounded to zero in the proof.

Polar source measure is `u*r dr dtheta/(4*pi*c_*)`; the actual roof differential is `dL=r*h dr`, where `h=e^T D(G/R^2)^{-1}D e`. Thus the exact coarea density is `u/(4*pi*c_*h)`. There is no missing radial factor, radius R, initial-fibre mass `2*pi`, terminal-section normalization, or angular Jacobian. The new angle is the direction of physical endpoint momenta; it is not the Hessian-normalized sector angle used in 285.

## 286: full source, boundaries and exact integration

All chart overlaps are disjointized on actual source points. The angular seam is counted once. Change of variables is first used for bounded nonnegative tests on finitely many relatively compact regular inverse charts. Monotone convergence then gives the full sum and unbounded integrable weights. General Borel selectors stay inside the integrals; no continuity or sector density is assumed for them.

A critical-origin arm is genuinely regular for every `0<r<r_+(theta)` on its actual visited word. It is not continued through an unvisited obstacle. Integrating `r/U_m <= dL/dr <= r/K_rho` first between two positive radii and then taking the lower one to zero proves the two-sided quadratic bound with no asymptotic error. The same metric gives `|dq/dr| <= 1/(R K_rho)`. It permits a visited incidence to tend to zero at the endpoint without defining the physical derivative there.

On a connected physical fan with a common positive radial interval over each compact angular subinterval, the exact angular derivative is `r^2 e_perp^T D(G/R^2)^{-1}D e`, bounded by `r^2/K_rho`. Integrating at fixed positive r and then taking r to zero proves constancy of its limiting roof. This uses compactness within a fan, not a common radius for all words or collision counts.

Band points satisfy `r <= min(rho,sqrt(2U_m*s))=A_s`. Complete joint-kernel domination yields the exact polar integrals `2*pi*A_s^(2-gamma)/(2-gamma)`, `0<=gamma<2`. Mass has coefficient `C_mom/(4*c_*)`; the inverse-gradient budget has coefficient `C_mom/(2*c_*R)`. At `gamma=2` the argument diverges logarithmically and the theorem does not include that exponent. Singular endpoint traces are not discarded as bulk-null; the theorem controls only actual interior collision-source mass approaching them.

## 287: global geometric covering, not sampling

The lattice covolume is `sqrt(3)/2`. For a primitive row direction of length l, nearest-row and nearest-point choices give a rectangle of half-widths `l/2` and `sqrt(3)/(4l)` around every point. A projection onto a physical line therefore has the exact normal bound used in `eq:eh-projections`. Lattice dihedral symmetries reduce unoriented directions to the closed wedge `[0,pi/6]`; every wedge endpoint is included.

The four intervals in `t=tan(theta)/sqrt(3)` are `[0,1/60]`, `[1/60,1/12]`, `[1/12,1/5]`, `[1/5,1/3]`. They cover without a gap. The first width increases; the other widths decrease on their specified intervals because the absolute-value expression has the correct sign `s*t<=1`. The four endpoint squared-width gaps are strictly positive rational numbers displayed in the proof. Thus a lattice center is always at distance strictly below `9/20` from the line, uniformly in position and direction.

The largest longitudinal rectangle bound is `sqrt(3847/124)/2`. A segment longer than twice this number has the chosen center's perpendicular foot strictly inside the segment and strictly inside a scatterer. This proves the horizon for every actual free segment, including limiting grazing segments. No Markov model, rational-direction exclusion, simulated maximum or compactness-only existence estimate is used.

For the rational enclosure `28/5`, squared candidate radii lie respectively in `[42,43)`, `[42,43)` and `[43,44)`. Integer squared lattice length is `Q=a^2+ab+b^2`. The complete row table proves 150 and 162 nonzero candidates; `Q<=43` implies `|a|,|b|<=7`, so the enumeration is exhaustive by an analytic bound, not by a chosen floating search box. Intrinsic counts are only bounded by these enclosing counts. They do not count words or pairing multiplicity.

## Independent finite checks and acceptance boundaries

`check_radial_coarea.py` checks symbolic matrix/normalization identities, 81 exact rational Schur chains (interior incidence as small as `1/1000000`), four exact polar integrals, all rational horizon margins and exhaustive quadratic-form counts. It also differentiates actual nearest-disk specular trajectories analytically and compares against independent same-word finite differences; 480 attempted orbits and 900 actual inverse-momentum points on alternating critical-origin families are recorded. Exclusions are reported, not silently classified as passed cases. Normal and `-O` outputs, including raw case arrays, must agree.

These computations test formulas and implementations. They do not establish all-root kernel bounds, uniform curve-growth assumptions, root sums evaluated at different branch radii, original roof essential height, paired trace domination, capacity abundance, exact arithmetic remainders or the ordered shortage limit. Those distinctions are preserved in every current status file.
