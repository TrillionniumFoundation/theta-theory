# Proof ledger and internal proof audit

This is an author-side proof audit, not an independent referee certificate. Finite regressions are not entries in the logical dependency graph.

| Result | Load-bearing proof obligation | Audit disposition |
|---|---|---|
| thm:bridge, lower | Arbitrary centers, actual conditional mass, countable summation, zero allocations | Written: unique neighborhood assignment, small-ball union bound, Tonelli; no center assumed on support |
| thm:bridge, causal bound | Conditioning error measure through raw kernel | Written: explicit factor conditional independence, Young inequality on active edges, exact holds, zero gain on overwrites, positive measure induction |
| thm:bridge, budget | Countable allocation need not attain infimum; anchor uses a state | Written: finite-support approximate allocations and Q(M-1)<=D_r Q(M); M>=2 explicit |
| thm:bridge, precision | Local errors in same state metric | Written: R_j=C_g r_j+xi_j and weighted Minkowski before squaring; effectiveness not inferred from Borel covering |
| prop:recharge-flow | Terminal weights obtained from raw kernels, not assumed stationary | Written: forward recursion and scalar deficit (D-C_b)y-(D A_G+C_b)x; holds cancel |
| lem:moran-profile | Nonhomogeneous shift, arbitrary-center small balls | Written: first differing digit/gap bound; product-law shift invariance; level n+2 cylinders |
| thm:moran | Quotient, raw laws, executable state count, report continuity | Written: terminal Bernoulli separates states; independent fresh reveal; retained prefix labels; anchor does not retain latent j |
| cor:no-dimension | Claimed oscillation not an approximation artifact | Written: dominating block lengths and exact subsequential logarithmic limits |
| thm:soft-state | No hidden retained randomness; finite state information cut | Written: independent shared seed, conditional entropy chain rule, Fano proof and Gaussian relative-entropy bound |
| thm:single-probe | Same oracle for both parameters; one task; online optimum | Written: two-sign average and unbiased centroid decoder; exact copy/overwrite implementation without a free acquisition flag |
| prop:terminal-deficiency | Lower over all randomizations, not just imputation | Written: common cell-guessing decision gap; exact imputation upper; terminal-only scope |

Critical audit checks: (i) allocation-independent recharge functions; (ii) shared encoder randomness independent of the entire prepared path under the fixed exploration; (iii) no nonreset cross-stratum error is lost; (iv) seed belongs to the paid initialization; (v) no countable minimum is asserted attained; (vi) raw thinning rho, complete path allowance and terminal deficiency have separate names; (vii) neither deterministic-time domination nor TV proximity is extended to stronger asymptotics without proof.

The inherited formal results are preserved, with seed notation clarified. This pass checked their interfaces and the relevant proofs against r1/r2 reports; it is not a fresh independent certification of every historical v1--v96 derivation. The new conclusions do not depend on unaudited archive results.
