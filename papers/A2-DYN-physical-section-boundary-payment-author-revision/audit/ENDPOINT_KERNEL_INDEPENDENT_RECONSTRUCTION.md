# Independent mathematical reconstruction of the selected endpoint kernel

Date: 2026-10-23. This is an author-side proof challenge, not an external referee report or an independent journal certification.

## Source scope

The proposed continuation examined was `revision-prep/endpoint-geometry/clearance_selected_endpoint_kernel.tex`. The comparison used the complete native proof bodies:

- 284, `physical_momentum_fibres`: the exact first-image density, actual terminal cancellation, every-regular-root extension, and the original conditioning factor;
- 285, `complete_critical_sector_sum`: auxiliary inverse weight, the angular Jacobian, physical-side disjointization, and polar-Fubini passage;
- 322, `positive_critical_marked_source`: finite analytic physical-side predicates, higher-order active boundary terms, and their almost-everywhere angular limits;
- 327, `length_sensitive_physical_source_transport`: the complete renewal including its last generation, disjoint initial clearance cover, enlarged source class, and localized half-source theorem.

These are inherited inputs. This examination does not independently certify their entire earlier dependency chain, nor does it substitute a computational experiment for them.

## Checks and results

### 1. Weighted first image retains selected length

The horizontal source is unnormalized `d alpha_0`. On one fixed-radius first-hit branch its exact density is

`rho = d / [R A sqrt(1+V_1^2)]`, with `A = sqrt(1-a^2)+tau/R`.

The radius factor cancels in a ratio of values on the same curve. Uniformly in the initial momentum, `t_*/R_+ <= A <= 1+tau_+/R_-`; no initial incidence lower bound has been inserted. Within one target homogeneous strip, the cosine ratio is bounded by the displayed `C_H`; the signed-strip estimate follows from `sin x <= x` and `sin x >= 2x/pi` on `[0,pi/2]`. The proposed `D_first` is consequently an upper bound for `sup rho / inf rho`.

The first inequality `sum sup rho <= K_c A_hor` counts at most `K_c` source intervals on each preliminary arc. A restriction to a source subinterval cannot produce new first-hit cut locations, and monotonicity of the image momentum angle bounds each strip's occurrences exactly as in 284/327. For the second inequality, the first-image integrals sum to the mass of the disjoint source cover. `ds=R d alpha_0` gives the factor `R_-^{-1}`. Thus `sum sup rho |C| <= D_first J_0 L_c delta/R_-` is correctly normalized. No cross-strip bounded-distortion estimate is required.

### 2. First flight and collision indexing

For `j>=1`, the substitution `h=j-1`, `n=m-j-1`, `l=h+n+2=m` in 327 is exact. For `j=0`, the new weighted first-image argument has precisely `1+(m-2)+1=m` collisions. Applying the complete renewal with `n=m-2`, then the single terminal cancellation, gives the stated forward estimate. Its coefficient includes `theta_r^{-1}`, so replacing `theta_r^(m-2)` by a multiple of `theta_r^(m-1)` has been paid. For `m=1`, the unselected first-hit count controls the selected root sum and agrees with the proposed constant.

### 3. Pointwise roots and reversal

The proof first obtains a density estimate almost everywhere. A finite collection of strict selected regular roots persists on nearby inverse branches, so continuity extends the estimate to its original terminal value, including artificial subdivision seams. Exhaustion gives the full nonnegative root sum. This extension does not define a physical derivative at a visited grazing collision.

The billiard collision map preserves `d alpha dp` at fixed radius; its derivative determinant is one. If its lower-left entry is `c`, the inverse matrix has lower-left entry `-c`. Conjugating the inverse by the momentum reverser changes signs but not this magnitude. Each forward regular source root therefore corresponds to exactly one reversed regular source root with the same inverse derivative weight. Recentring the terminal obstacle to the fundamental cell is unique, and records with different winding histories cannot become the same reversed physical initial state because the physical map is invertible on regular orbits.

An unvisited disk near a chosen physical flight stays unvisited under reversal; its closest foot changes from `t_z` to `tau-t_z`, so strict interior-foot and clearance inequalities are preserved. Its index changes from `j` to `m-1-j`. Thus applying the forward bound to both orientations and taking the smaller number proves the exponent `max(j,m-1-j)`. It does not multiply two events or assume any independence. Original section and record selectors may be restored by positive restriction after this unrestricted kernel bound.

### 4. Critical physical-side transfer

At fixed radius, collision count, and finite germ family, each limiting width at most `delta` is strictly below `delta+eta` on a sufficiently small actual physical-side neighborhood. The interior foot persists; at zero clearance the actual unvisited side has positive clearance. The section source normalization is not needed in this step: one applies the unconditioned fibre root bound directly.

The disjoint physical inverse branches, positive continuous weights, and finite analytic side conditions permit exactly the polar-Fubini/good-radii argument of 285. Analytic boundary conditions whose linear part vanishes are covered by the first nonzero homogeneous polynomial argument of 322; its exceptional angular set is finite. The result is `sum u_x beta_z <= C_end (delta+eta+theta_r^max)`. Sending `eta` to zero and then exhausting finite families occurs at fixed physical parameters. The angular comparison in 285 introduces `lambda_max(G)/(2 R^2 c_*)`, bounded by `U_2/(2c_*)`; the proposed `C_crit` is correct. No extra `4pi` or radius factor is introduced.

### 5. Full guard and ordered limits

There are at most two flights at each depth. Hence the exact original guard widths sum to at most `4 epsilon(B)/(1-q_0^(1/4))`. Also `max(j,m-1-j)>=(m-1)/2`, so the exponent sum is at most `m theta_r^((m-1)/2)`. The latter vanishes under the collision limsup with `B` fixed. The remaining bound vanishes only in the subsequent outer limit as the original epsilon tends to zero. These are unscaled critical coefficient estimates.

## Wording recommendations and residual scope

No mathematical mismatch was found in the proposed incremental mechanism, conditional on the stated inherited native results. Two brief proof additions would improve reconstruction: explicitly give the reversed foot `tau-t_z`, and use the unconditioned fibre root estimate rather than mentioning the section-conditioned joint bound in the critical proof. Neither requires changing the constants.

The result pays a positive-width source in the endpoint-momentum and leading-critical-coefficient norms. It does not provide an `m^-2` bound, a uniform physical roof neighborhood for all critical germs, the nonleading coarea remainder at a common roof, the original shallow same-pool shortage, or the raw pointwise local limit. Multiplying the term proportional to epsilon(B) by `m^2` before the collision limsup is not permitted. The proposed scope paragraph correctly makes these distinctions.
