# Independent source audit — A2 v40

This internal, AI-assisted independent audit records mathematical reasoning about the new source files. It reports the drafting audit and the incorporation of its clarifications into the submitted primary; it is not an external journal report. It is not a formal proof certificate or an experimental validation of the commanded apparatus.

## Exact two-command theorem

Audited source: `core/21_two_field_rigidity.tex` (exact theorem portion). The central data consist of two spatial forward mean fields for the fixed commands `a = te` and `-a` with one stationary launch probability. The length is strictly positive and fixed.

### Endpoint balance and prefix inverse

The identity

\[
B_a(y)-B_{-a}(y+a)=1_{\mathcal O}(y+a)-1_{\mathcal O}(y)
\]

holds pointwise with the repository's closed solid/swept-set convention, including atoms landing on boundaries. After integrating the same stationary law, the measured difference is `r(x)=v(x+a)-v(x)`.

For `M=floor((D+Delta)/t)+1`, each negative prefix sum equals `v(x)-v(x+ma)` and is at most `v(x)`. Starting at a positive-occupation point, the directed grid exits its compact expanded component within `M` steps. The gap `d-Delta>t` prevents the exit point from belonging to another expanded component. One prefix therefore attains `v(x)`. This proves the finite max-prefix formula and its `M`-Lipschitz bound for arbitrary errors in the increment data. Two mean-field errors of size `epsilon` give at most `2M epsilon` occupation error.

No continuity is required. Finitely many translated null sets remain null, so a.e. input fields determine the a.e. occupation. The physical representatives satisfy the identity pointwise.

### Support geometry

The occupation measure has components `P_C=C-A`. The two collision measure supports have components

\[
K_{+,C}=\Gamma_{+,C}+[-t,0]e-A,
\quad K_{-,C}=\Gamma_{-,C}+[0,t]e-A.
\]

An incoming strip is the closure of its connected positive-area interior. Convolution of positive measures has support equal to the sum of supports, so this conclusion applies to arbitrary compact launch probabilities, including atoms and singular probabilities. Convexity of the support `A` gives connectedness even when `A` is a point or a segment. Components belonging to different bodies have distance at least `d-t-Delta`. Each `K_{sign,C}` meets exactly the expanded component `P_C`, which verifies observable matching.

The planar-null difference between the collision-start set and the closed strip remains a.e. null after convolution with an arbitrary finite measure, by Fubini. It must not be asserted to vanish at every nominal point for atomic laws; the draft correctly uses measure supports.

### Footprint cancellation and chord recovery

For `p_+,p_-` the support points with normals `e_perp,-e_perp`, put `L=[p_-,p_+]`. The incoming arc has support `h_C` on one normal hemisphere and `h_L` on the other. The two arc supports sum to `h_C+h_L`. Therefore

\[
H=2h_P-h_{K_+}-h_{K_-}+t|u\cdot e|=h_C-h_L.
\]

This identity cancels the arbitrary unknown footprint before any support-direction differentiation. The chord is generally slanted; its normals are not assumed equal to the commanded directions.

For a strictly convex body, the planar surface area measure `S_C=h_C''+h_C` has no atoms. This follows either from the usual edge-length formula for its atoms or from `h_C` being continuously differentiable. Consequently

\[
H''+H=S_C-|L|(\delta_n+\delta_{-n})
\]

is already the Jordan decomposition. Its negative part identifies the chord length and its unoriented direction. Adding the centered chord support recovers the body up to translation. The positive part recovers the full surface area measure, even if it has a singular continuous component. Thus the main exact result needs strict convexity and no boundary smoothness or curvature lower bound.

### Common frame, launch probability and periods

The Steiner-centered body plus `s(P)` equals `C-s(A)`. Subtracting this recovered support from `h_P` gives `h_{-A_0}`. All bodies recover the same centered footprint.

Isolating one component gives `v_P=1_{C_0}*check(mu_0)` as an integrable compactly supported function. The Fourier transform of `1_{C_0}` is entire and nonzero at zero, and its real zero set has empty interior. The quotient therefore recovers the continuous Fourier transform of `mu_0` on a dense set and everywhere by continuity. Fourier uniqueness for finite measures recovers the entire law, with a.e. density identification as a special case.

Equality of the two a.e. fields therefore gives exactly the common-translation fiber. Once the table and law are fixed, every physical finite-length forward mean is fixed pointwise under the prescribed boundary convention. An a.e. field period preserves the occupation support and permutes `C-A`; support cancellation gives a table period. Its converse is pointwise, so the two definitions of period coincide for physical representatives.

## Finite moment, probability and prediction proof

Audited source: `core/23_two_field_law.tex`, including the subsequent uniform raw-prediction addition recorded below. The mathematical audit found the following chains valid under the referenced finite geometry theorem.

1. **Occupation quadrature:** condition on the launch displacement. A translated convex indicator has only `O(ell)` area of boundary cells in a bounded window. The polynomial/cutoff weight varies by `O(m ell)` on the remaining cells. The bound is uniform for every displacement, so averaging it works for arbitrary probability measures. Mesh `ell` of order `a/m`, `a`-accurate sampled means, fixed prefix depth, and Hoeffding's inequality give `C m^2 a^{-4} log(Cm/(a delta))` bits. All moments share the same observations.

2. **Triangular moment conditioning:** the binomial convolution formula has diagonal coefficient `(-1)^k`. The discrepancy recurrence is bounded by `D_k <= 2 a 8^k k!`; substituting it reduces the recursive sum to the factor `exp(1/8)-1`, leaving sufficient room for the forcing term.

3. **Polynomial approximation:** the normalized fourth power of the Dirichlet sine quotient is a nonnegative kernel of trigonometric degree `2(m-1)` and first absolute angular moment `O(1/m)`. Tensor convolution gives `O(1/m)` approximation of every Lipschitz test after the cosine substitution. Total algebraic degree is at most `4m`; the sum of monomial coefficients is at most `C m^2 3^{4m}`. Combining this with the factorial conditioning gives `W1 <= C/m+a(Cm)^{Cm}`.

4. **Finite positive reconstruction:** a rational-grid probability simplex and finitely many moment discrepancy constraints give a rational linear program. A discretization of the true law is a feasible comparison to within the moment error. The additional `2^{4m}` arising from separately certified geometric moments is explicitly retained and is absorbed by the chosen tolerance `a_m=exp(-C m log(Cm))`. The fitted law is positive, has total mass one, and has the claimed transportation error.

5. **Costs:** substituting any fixed polynomial geometric acquisition bound at tolerance `a_m` into the decomposed cost gives `exp(C epsilon^{-1} log(C/epsilon)) log^2(C/delta)`. The coordinates need `O(epsilon^{-1} log(C/epsilon))` bits, apart from confidence/count overhead. This is a sufficient bound, without a matched minimax claim.

6. **Prediction:** the collision-start set for any finite command `b` is the union of the swept convex bodies `C+[-b,0]`, with the solid union removed. The total variation of its indicator on a bounded enlarged window is bounded uniformly for `|b|<=T`. Matched Hausdorff geometry error changes this indicator in local `L1` by `O(error)`. The local BV translation bound and an optimal coupling of launch laws then give uniform local spatial `L1` response error `C_{U,T}(geometry error+W1)`. The result does not claim pointwise response stability for atomic laws.

7. **Strong density conclusion:** a known BV bound on the zero-extended density gives `||rho_h*j-j||1 <= C V h`. Transportation error `epsilon^2` contributes `C h^{-1} epsilon^2` after smoothing. With `h=epsilon`, the density error is `C(V+1)epsilon` and the sufficient cost has exponent `epsilon^{-2} log(C/epsilon)`.

Two presentational clarifications were sent to the authoring agent: certified area and geometric moments used as linear-program coefficients must be rational approximations, and an optional restriction of the law grid to the estimated footprint needs a padding reserve larger than the footprint Hausdorff error plus one mesh cell. Neither requires a change in rates or theorem scope.

Both clarifications were subsequently applied. The later addition of uniform raw prediction under the same BV-density hypothesis also checks: the planar BV Sobolev estimate `||j||2 <= C |Dj|` follows from layer cake, Minkowski, the planar isoperimetric inequality and coarea. A uniformly `O(xi)` area of geometric collision-indicator disagreement therefore has density-weighted mass at most `C V sqrt(xi)`, uniformly in the nominal center in a fixed window and in bounded command lengths. The density `L1` error adds directly. At the displayed `epsilon^2` transportation tolerance the actual geometry tolerance is the much finer `a_m`, so `sqrt(xi)<=C epsilon`. This gives the claimed uniform prediction without a density upper bound.

## Finite geometry proof

Audited source: `core/22_two_field_finite.tex`. The following parts were checked independently.

1. An upper curvature-radius bound supplies a global circumscribed disk tangent at each boundary point of `P=C-A`. In a collar of depth less than `t^2/(32R)`, every approximately maximizing choice among the two fixed horizontal directions starts outside that disk after the shift `tv`. This remains true at a horizontal tangency. For exterior targets a true maximizing direction always misses, so conjunction of the candidate marks is an exact exterior zero test. Interior depth `e` gives hit probability at least `c e^{gamma+3/2}`. The distance bound `Delta+t+d_c<d_0` excludes other obstacles from every such flight.

2. A small ball of radius `epsilon` centered at any point of the closed incoming strip contains strip area at least `c epsilon^3`. Near tangent endpoints the Jacobian contributes one additional power of `epsilon`; away from them the bound is conservative. The footprint cap has probability at least `c epsilon^{gamma+3/2}`. Their product gives cap probability `c epsilon^{gamma+9/2}` for a uniformly drawn nominal center whose bit is positive.

3. Conditioning on the launch displacement makes a grid cap event an indicator of a translated difference of convex sets intersected with a half-plane. Its boundary cells have area `O(mesh)`, uniformly in that displacement. Thus the rational grid preserves the cap lower bound at mesh `epsilon^{gamma+9/2}` without a density continuity assumption. Positive records assigned by the coarse component-distance thresholds form an inscribed hull. A support-direction net and a union bound use the same records for every direction and give the stated hull sample count.

4. The exact cosine difference of `H` integrates its signed curvature measure against `sin(b-|u|)`. At scale `b=L epsilon`, a fixed negative threshold detects an atom within `O(epsilon)`; the nonnegative curvature density cannot create a spurious distant atom. The chord normal remains a fixed angular distance from the selection boundary because `n·e >= w_*/D_0`.

5. A signed plateau with vanishing moments through degree four integrates the `C^{4,beta}` curvature density with error `b^{5+beta}`. The data error is `O(epsilon/b)`. At `b=epsilon^{1/s}` these errors match at `epsilon^{(s-1)/s}`. The atom is exactly in the plateau, so its `O(epsilon)` location error does not create a further mass error.

6. Smoothing the estimated chord uses its special support `|sin(phi-theta)|`. Its smoothed `C2` norm is `O(b^-1)` and its angle derivative has `C2` norm `O(b^-2)`. Consequently length and angle errors contribute `O(epsilon^{(s-2)/s})`, the same order as smoothing the data and the true smooth support. This verifies the stated `C2` rate, the stronger `C0` rate and the final exponent `Q_pair=(gamma+9/2)s/(s-2)`.

7. One calibrated body identifies the common centered footprint. Subtracting it from every expanded component recovers all bodies in the same canonical frame. The positive curvature margins make the small-error support outputs genuine strictly convex bodies. The inherited period locking uses the same fixed positive patch margin; the complete finite-cloud alternative omits that step.

Three small clarifications were sent to the authoring agent: a missing backslash in the sine-difference summation index, a display that should use a lower-bound sign for one strip's contribution when other obstacles may also hit the cap, and an explicit threshold adaptation for coarse occupation labels. The latter uses the lower mass `lambda=c d^{gamma+3/2}` at fixed depth `d`, estimates occupation to `lambda/4`, and retains nodes at threshold `lambda/2`. It avoids using the old localized-kernel threshold `1/2` literally. These changes preserve all theorem statements and rates.

The finite probability and predictive statements remain conditional on the quantitative geometry priors. Their moment stage itself requires no absolute continuity of the launch probability. The exact result permits arbitrary convexly supported laws, while a uniform finite recovery of the footprint retains a lower mass hypothesis from the geometric acquisition theorem.

## One-orientation example

The final proposition of `core/21_two_field_rigidity.tex` constructs `h_lambda=1+lambda b` with a nonzero smooth bump supported in the outgoing normal semicircle. For small nonzero `lambda`, the curvature radius remains positive while the entire incoming semicircle is unchanged. All positive-length forward bits in the one fixed direction consequently have the same exact strip description, including tangency and solid-endpoint conventions. The support perturbation is not a linear translation term. Thus a known fixed compact launch law gives identical one-orientation response fields for bodies with different outgoing arcs. This is a statement about one directional field family, not about scalar sample counts or statistical minimax optimality.

The one-orientation proposition was separately checked by the finite-geometry auditor, including tangent sections and atomic laws. All small clarifications recorded above were incorporated. The integrated source also specifies the dimensionless footprint grid, the local scalar moment-tolerance notation, the known coarse mass threshold and conditionally independent fresh preparations. Compilation and finite diagnostics are recorded separately by the qualification receipt.
