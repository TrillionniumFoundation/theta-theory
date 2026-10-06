# Response to the v19 referee: A2-DYN revision 20

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revised directory:** `papers/A2-DYN-v20-referee-response`  
**Controlling report:** `reviews/a2-dyn-v19-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Report commit / blob:** `da89f3ae6f0b9e5fedb1ae6aa7a9dcfc20f623aa` / `c41b48727e3b3278f65ea8aed6c861fb0086c88e`  
**Author baseline:** `e56eed31c3b7d70ceb71a7f4b075092c2bd3e98d`  
**Baseline paper tree:** `57ea4229c9e344f9d61fd08be6ef7f7954d29feb`  
**Date:** 6 October 2026

We thank the referee for the detailed audit of revisions 17--19 and, especially, the explicit scale calculation. Revision 20 retains the original physical family, return section, joint record, title, and raw mixed-density objective. It adds a direct estimate for the uncompressed dynamics rather than asserting that the two incompatible compressed estimates can be concatenated. The new theorem concerns actual moving averages, weighted coefficients, and a specified cyclic spectral measure. Its scope is stated in each conclusion; a moving mean-square theorem is not presented as fixed-return raw Fourier decay.

## A. The compression-scale calculation and the new direct argument

### A.1. Exact accounting of the two grid budgets

`prop:grid-scale-separation` writes out the calculation requested in report Sections 7 and 16A. If the grid term `n sqrt(h(1+|z|) exp(C_g L))` tends to zero with `L>=n`, then `log(1/h)>=C_g L+2 log n+omega(1)`. Thus the reconstructed budget has `Lambda_h>=c n`. At `|z|>=2 n^(-99/200)`, the local resolvent quantity is at least `c n^(1/100)`, outside its stated domain. This is a statement about simultaneous use of the displayed upper bounds, not a lower bound on the actual error for every possible grid.

The finite-rank results and their exact residual identities remain intact. A pointer to the scale calculation now appears before the finite-time comparison in the compressed-operator section.

### A.2. Short-lag Gaussian estimates, not a long-orbit reconstruction

`lem:pointwise-lag-Gaussian` derives a pointwise estimate directly from the inherited collision estimate and stopping comparison. It does not infer a supremum bound from an integrated major arc. For physical `|z|<=2 j^(-99/200)`,

`|c_j(R,z)-exp(-j z^T D_R z/2)| <= C j^(-43/1400) sqrt(log(2+j))`.

The unique slow error is the single observable-smoothing term; the proof lists every competing exponent and the two analytic-domain checks. Uniform covariance ellipticity controls the Gaussian term.

For `r=|z|`, choose `m=floor(r^(-200/99))`. All lags below `m` lie within that proved pointwise band. Summing them gives

`B_m=1+2 sum_{j<m}|c_j| <= C[r^(-2)+m^(1-43/1400) sqrt(log(2+m))]`,

and hence `B_m/m <= C r^(2/99)`. The logarithm is absorbed using the exact positive margin `29/693`.

### A.3. An estimate on the actual uncompressed dynamics

The vectors are the exact functions `U_z^(N+j)1`, not fitted-cell approximations. Their Gram matrix is Toeplitz, with entries `c_(j-i)`, and is independent of the starting index `N`. Its row-sum bound yields both an analysis inequality for an arbitrary Hilbert-space test vector and a synthesis inequality for arbitrary scalar coefficients. This finite Hilbert-space argument is proved in full.

Partitioning an arbitrarily long averaging interval into blocks of length `m` gives

`T^(-1) sum_{j<T}|<b,U_z^(N+j)1>|^2 <= C r^(2/99) ||b||_2^2`,

and

`||T^(-1) sum_{j<T} exp(-ij xi) U_z^(N+j)1||_2^2 <= C r^(2/99)`

for every `T>=m`, every integer `N`, and every real `xi`. There is no local peripheral-angle restriction. No spatial mesh, BV reconstruction of a time-n vector, induced mixing assertion, or independence assumption is used.

### A.4. A common feasible annular scale

On `2 n^(-99/200)<=r<=n^(-2/5)`, the same lag window satisfies `m<=2^(-200/99)n<n/4`. Its averaged error is at most `C n^(-4/495)`. Thus one explicit parameter choice works over the full small annulus for all averaging horizons `T>=n`. The rescaled radii remain `2 n^(1/200)` and `n^(1/10)`.

This resolves the mesh issue for the new direct averaged conclusions. It does not supply the fixed-return contour-to-power estimate asked for in its strongest form. The paper neither silently changes the old resolvent domain nor calls a cyclic-vector average an operator-norm estimate.

## B. Peripheral spectral information and the complementary integral

`thm:cyclic-peripheral-bounds` applies the Gram estimate to the exact spectral probability of the constant vector. Every peripheral arc of radius `1/m(r)` has mass at most `C r^(2/99)`. The normalized exterior resolvent `(1-s)(I-s exp(-i xi)U_z)^(-1)1` has squared norm at most the same bound when `(1-s)m<=1`. The argument covers every angle but applies to that specified vector, not to arbitrary input vectors or a unit-circle inverse.

`thm:spectral-Cauchy-limit` identifies the rescaled principal spectral angle `theta/r^2`: for `z=r u`, it converges to the Cauchy law of scale `u^T D_R u/2`, uniformly in the radius and direction. The proof uses the actual one-return second moment to control rounding from real to integer Fourier indices, then applies the inherited physical Gaussian theorem at lag `floor(t/r^2)`. The spectral Cauchy law is distinct from, and does not replace, the physical Gaussian law.

The new annular integral is explicitly normalized by the annulus volume and averaged in the return count. The raw inversion theorem needs an unnormalized complementary residual integral at one prescribed count, with factor `n^2`. The paper calculates that Cauchy--Schwarz on the new bound alone would yield the nondecaying budget `n^(2/5-2/495)` after that raw normalization. It therefore does not declare the raw complement closed. Compact nonzero physical frequencies, growing roof frequencies and fixed-count residual decay still require their stated estimates.

## C. Finite-count preparation and long-time derivative budgets

The proof of `lem:power-log-jet` now identifies exactly why its germs are convergent. It cites the analytic-neighborhood convention and strong-unit definition in Cluckers--Miller Definitions 2.2--2.3, with Theorem 2.4 applied to the subanalytic generators, as well as the inherited constructible preparation theorem. Bounded rational monomials become nonnegative integral powers after clearing denominators; the analytic function extends to their limiting image. This justifies the convergent series before two differentiations.

The constant/slope extraction, full finite-count graph, and trace cancellation remain. None of the new spectral or averaging estimates bounds the actual germ radii, coefficients, exponent separation or derivative sum `A_2(n,L_n,R,w)` at growing `n`. The uniform long-time derivative and local extracted-edge estimates remain explicit obligations for the same raw theorem, not consequences asserted from initial-coordinate BV or fixed-packet finiteness.

## D. Weighted results and exact conditioning

`thm:weighted-annular-averages` permits any square-integrable initial weight. For an unchanged event `A` with probability `p`, the weight `1_A/p` has squared norm exactly `1/p`, giving an averaged squared conditional-characteristic bound `C p^(-1)n^(-4/495)`. In particular polynomial rarity `p>=p_0 n^(-beta)` with `beta<4/495` is admissible. The proof also gives an explicit bound for the fraction of exceptional return counts.

The event may contain many observations or depend on the physical trajectory, but it must be the same event across the averaging window. The result does not cover an independently reselected indicator at each averaging index. Fixed actual-return marks are treated by exact recentering; actual terminal marks use the inverse unitary. No extra collision-count condition is inserted in the final event and no denominator is factored.

These are weighted averaged bounds. The earlier single-mark and logarithmic-window central/moment laws remain unchanged. Weighted raw derivative growth, local-edge correction and the fixed-event raw denominator asymptotic are not inferred from the new average.

## E. Exact physical-event replacement

No replacement of a completed-return event by an exact physical-time/lattice event is performed. The same event and its exact probability occur in the new conditional theorem. The relative comparison required by the original downstream application remains distinct. Neither a small unfinished-return displacement nor an averaged conditional-characteristic bound is presented as that comparison.

## F. Independent review and presentation

The new direct proof requires no new billiard regularity input beyond the inherited pointwise collision estimate, stopping comparison, true return-map invariance, uniform ellipticity and finite one-return moments. Its Hilbert-space component is elementary and included in full. The spectral-measure formulation uses the ordinary unitary spectral theorem and the characteristic-function continuity theorem. No independent human specialist review or formal certification is claimed.

All sixteen presentation comments are reflected in the source or retained distinctions. The old phase variables, top-versus-height norm identities, smallest-singular-value statements, constant/slope extraction, cutoff radii, four window margins, unchanged-event denominators and BV/subanalytic class distinction remain. The requested scale calculation and convergence clarification are added rather than substituting a different paper topic.

## Source and execution record

All 43 old core modules and every inherited mathematical label are retained. Forty-one old core files, all inherited Python files and the bibliography are byte-identical. Seven exact edits affect only the introduction and two old core files; two complete new core files contain the new proofs.

After the referee's freeze, the baseline response run `37455890344` produced artifact `11410545675`, archive SHA-256 `ac494c939bce535df5704acc0ad7447889b17e175c6132d851d29fd4d3359eee`. Its exact source and receipt were downloaded and checked before revision. This is baseline evidence, not v20 qualification.

The new read-only workflow qualifies the exact committed v20 source, compares normal/optimized diagnostics, compiles the full paper, and emits a run-bound receipt with source and PDF hashes. Static prose does not predeclare that run successful. The finite tests include Gram/analysis/synthesis checks, full-circle spectral kernels, Abel resolvents, event normalization, a wrapped-Cauchy scaling model, and negative controls preventing either single-time decay or index-dependent events from being inferred from an average. These finite models are not the physical billiard.
