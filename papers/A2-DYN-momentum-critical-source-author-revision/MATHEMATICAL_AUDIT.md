# Mathematical audit of new bodies 284–285

This is the author's proof-completeness audit, not a new referee report or an independent proof certificate. The original model and exact target are unchanged.

## 1. Actual source and first-hit geometry

The source is `p0=a`, measured by dα0, mass 2π. The original probability is still `1_Y* dα0 da/(4πc*)`. We do not condition on a smaller event or assume a joint product law. The first image is after exactly one true first collision. With initial graph slope V=0, direct contact projection gives `ds1/ds0=−A/d`, `V1=κ+dκ/A`, and `V1_s1=−p1 κ/A(κ+2dκ/A)−a d²κ²/A³`, where A=c+τκ. Substitution of V=κ instead would be an error; the symbolic test explicitly uses V=0.

`RA=Rc+τ≥t_*` proves the incidence-weighted density bound `ρ≤d/t_*`. `A≥t_*κ` proves the displayed curvature cap, exactly 74750/27. The fixed invariant curvature allowance is enlarged to include this source and 2C*. The growth constant is recalculated for that class, not silently reused.

The relative-angle derivative for a horizontal fibre is bounded by `(1−R_+)^{-1}−k_-<0`, weaker than but still consistent with the two-curvature unstable-graph estimate. Positive-foot intersection bands are intervals, and disjoint disks cannot exchange first-entry times without meeting at one point. The finite candidate set is justified by the continuum finite-horizon proof, not the numerical search box. Both homogeneous tails and all length subdivisions are counted in A_mom; no omitted grazing strip is assigned zero source.

## 2. Last collision and singularity budget

For an incoming unstable graph, the physical derivative is

`|dp1/dℓ| = d V1 (A/d)/sqrt(1+V²) = (κA+dw)/sqrt(1+V²) ≥ k_-t_* =6/47`.

The terminal d cancels algebraically. The last step is divided into physical first-hit branches only, at most J_f on each short incoming curve; it is not subdivided into infinitely many terminal homogeneous strips. For m≥2 the middle growth has m−2 steps after the first collision and before the last. For m=1 the exact derivative is `|dp1/dα0|=A+d≥k_-t_*`, treated separately. This avoids both an off-by-one collision and a false inverse-incidence factor.

Countable first-image/growth cuts and finitely many last-step tangencies are null on the actual fibre by its exact weights. This is not used to delete a positive pairing-endpoint trace. The finite second-derivative tests approach positive initial and terminal incidences; any chart changes or floating-resolution exclusions are counted, never treated as continuum singularity bounds.

The exact one-flight lattice kernel in `lem:mc-oneflight` also checks the base case without a preliminary-arc multiplier. The impact identity is `p1=a+z·v_perp/R`; the only forward angular root has projection `Q_z=sqrt(|z|²−R²(v−a)²)>0`. Its inverse derivative is R/Q_z and its true roof is `Q_z−R sqrt(1−a²)−R sqrt(1−v²)`. The mask is the actual first-hit indicator; a hidden disk is excluded as a candidate next target, never by hiding the earlier collision. Since `1−4R_+²=291/2500`, each root weight is at most `47/(2 sqrt(291))`. This exact source formula is not composed as a momentum-only Markov law.

## 3. Coarea and pointwise quantifiers

The proof sums all labelled physical source curves and all middle homogeneous branches before taking any supremum in R,m,a,v. No physical-word count multiplies a per-word bound. Positivity allows arbitrary original record and roof selectors; no derivative or factorization of their indicators is required.

Coarea initially gives the root density almost everywhere. At a prescribed regular v, select finitely many distinct roots, choose disjoint smooth inverse branches, take the continuous limit of their weights through values where the inequality holds, then exhaust the nonnegative series. This proves the advertised bound at every regular root value. It makes no claim at a singular physical derivative. The factor in the original-section joint density is exactly 1/(4πc*) with no extra R and no second c*.

## 4. Optical normalization and endpoint Hessian

The retained generating matrix has B21=−detG/(R e). Thus `u=R|e|/detG`, `ω=|e|/R`, and `J=sqrt(detG)u/(2R²c*)`. These identities are checked with the actual one-flight normal orbit at R=.45,.46,.47, as well as symbolically. The tests do not replace the finite-word optical proof.

The initial circular acceleration is −R n0 and the length gradient is −v, giving **+R c0**, not a negative circular term. At normal endpoints the unreduced diagonal is `R+R²/τ`. Positive interior elimination subtracts a positive semidefinite Schur term. Therefore `sqrt(detG)/R²≤κ+1/t_*≤170/9`. For m=1 the mixed term has magnitude ≤R²/τ, so the eigenvalue bound is `κ+2/t_*≤320/9`; for m≥2 the endpoint block is diagonal before elimination, giving the sharper κ+1/t_* bound. The weaker constant is used uniformly, including m=1.

## 5. Genuine one-sided critical source

No physical return derivative is assigned to an unvisited tangent state. With positive visited incidences, the auxiliary strict-word action and local endpoint inverse are smooth; they are used only on their actual physical side. At a fixed initial limit state the next strictly met disk is unique, and iteration fixes the strict visited word. A different word using an intervening tangency would have a visited zero incidence and is outside this smooth class. Duplicate coordinate germs are united, not counted again.

The joint inverse weight is `u_x(z)`, continuous at the auxiliary critical point. Finite actual-source restrictions are disjoint and dominated almost everywhere by the complete endpoint kernel. Polar Fubini provides almost every small radius; nonzero C¹ cut gradients give angular convergence away from finitely many rays. Taking this limit for a finite family, then positive exhaustion, proves the complete sector-weighted sum. General Borel selectors without a sector limit retain their exact old a_E(s); no new regularity is assumed of them.

The angular coordinate change is not measure-preserving: `L=R^{-1}diag(−1,1)G^{1/2}` and `|d arg(Leθ)/dθ|=sqrt(detG)/(eθ^T G eθ)`. The determinant and R² cancel exactly in that ratio. The comparison uses λmax(G), not an unnormalized Euclidean angle. Ninety-six anisotropic positive Hessian cases test the angular integral independently of the formula for the angle between its endpoint rays.

## 6. Limits and global consistency

For every fixed R,m, the sector limit is first taken on finitely many charts; positive exhaustion then gives a bound whose constant is common in R,m. This proves a uniform leading sum without choosing a common chart radius. It does **not** justify exchanging the local radius with m, summing all O(sqrt(s)) errors, or evaluating different branches at their own momentum point selected by a common original roof t. Those missing operations are explicitly excluded from the theorem.

No exponent in the original m² normalization, no lattice label, roof interval, conditioning mass, radius bound, physical clock, collision convention or original B/m limit order changes. The same normalized shortage is still the minimal governing closure. The new source theorem is a genuine all-time continuum statement in the written proof chain, not a conclusion inferred from its finite diagnostics; it has not received an independent specialist proof audit.
