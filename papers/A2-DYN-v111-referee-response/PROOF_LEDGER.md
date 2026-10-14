# A2-DYN v111 — proof and dependency ledger

The original organizing assertion is `eq:v76-target`. The model source remains Git blob `6af1dcb4548e1b5dd82b9a330dead6e04fd09797`. The exact v110 packet is archived as tree `89ec727b370bf21d66d7086041f75d7868671d4b`; its 264 numbered modules are retained, and modules 265–267 are added.

| Statement | Location | Proof and scope |
|---|---|---|
| Two-trajectory support inequalities | Lemma 9.1, module 265 | Convexity of the Cartesian broken-path length; physical first variations. No interpolating physical path or convex angular domain. |
| Global roof–angle uniqueness | Theorem 9.2, module 265 | The support inequalities order lengths strictly along any common endpoint-gradient ray. Includes disconnected components of one lifted itinerary. |
| Uniform roof range within a word | Lemma 9.3, module 265 | Interior contact minimization over the product of closed disks; endpoint triangle inequalities. It does not bound occupation-label variation. |
| Physical target-roof sum | Equation (9.6), module 265 | Local endpoint twist and positive coarea determinant, global injectivity, disjoint chart summation, and null-set passage. |
| Multiple stable-factor removal and physical block sum | Lemma 10.1, module 266 | Historical optical stable comparison and one-step incidence removal; full words reconstructed from blocks and at most D^s deleted symbols, including adjacent marks. |
| Target-roof multiple-incidence insertion | Theorem 10.2, module 266 | The new global roof–angle multiplicity bound and the retained uniform pressure theorem. Finite-count essential-roof bound, unscaled; no m^(-2) factor claimed. |
| Changing-witness factorial estimate | Corollary 10.3, module 266 | Positive elementary-symmetric expansion, summed marked bounds, e_s <= (sum eta_i)^s/s!. No whole-segment witness required. |
| c_per <= f <= A | Lemma 11.1, module 267 | Full variation dominates the decrement from an endpoint minimum. Uses the actual positive surviving coefficient. |
| Collision-deep incidence and high-multiplicity payments | Theorem 11.2, module 267 | Full target-roof witness estimates, summable original depth thresholds, finite-count logarithmic substitutions and factorial bound. Zero m^2-normalized limsup height at fixed B. |
| Exact retained source and collision-zero residual difference | Corollary 11.3, module 267 | Original positive restriction, unit-Lipschitz positive-part map, proved pointwise payment, unchanged scalar reduction and full nongrazing pool. |
| Full remaining raw pointwise estimate | Equation (11.12), `eq:v111-remaining` | **Not proved here.** Shallow incidence and arbitrary-depth clearance witnesses remain; no averaged replacement or negative theorem is asserted. |

## Source-pinned historical inputs

Three complete proof anchors are copied to `provenance` without changes:

- Module 238, `238_global_momentum_uniqueness_and_stable_weight.tex`, blob `c79fb9d660ab90370700c4fbfe4d4311175ac60f`: Cartesian monotonicity, omega <= C_0 c_m J^s T^m, and J^s T/c <= C_1.
- Module 239, `239_marked_pressure_comparison_and_growth.tex`, blob `fc76d61faeb70c0eeca6217c2c09daea4c3b2bde`: physical-word pressure, finite step alphabet, and single-mark block reconstruction. Its fixed-radius theorem alone is not used as a family-uniform bound.
- Module 241, `241_uniform_geometric_pressure_by_finite_tests.tex`, blob `fa0f71468d1f304da492687d949ad00c953402e7`: the uniform geometric pressure bound sup_{R,l} P_l(R)<=Q_star. The new theorem uses this source-pinned result and does not independently reconstruct its entire external geometric chain.

The current optical and endpoint proofs in modules 260–261 and 264 are unchanged. Modules 262–263 receive only the requested Borel endpoint-completion and positive-denominator explanations, with their complete original versions preserved in the archive. The full original paired-source construction and scalar equivalence retain the scope stated in `inputs.tex`.

## Quantifier audit

The marked inequalities hold at every finite collision count and every choice of distinct indices, nonnegative thresholds and depth/multiplicity cutoffs. Taking a supremum over roofs is justified only after the positive physical word sum. Radius uniformity remains sup_R esssup_t; null sets may depend on R.

The logarithmic L_m and s_m are inserted into those finite-count inequalities, not into a spectral estimate stated only at fixed width. At each outer B, epsilon(B), h_B, r_B, gamma_B and K_B remain fixed before the collision limsup. The outer limit B tends to infinity last.

The pressure constants do not contain an m^(-2) factor. The depth and factorial factors are what make the particular removed sources small after multiplication by m^2. The all-incidence O(epsilon) bound alone is insufficient for the organizing theorem. The remaining clearance source is not estimated by replacing a clearance with an incidence.

## Validation boundary

Exact rational tests verify finite combinatorial and optical identities. Actual two-disk trajectory tests additionally check the support-inequality signs at valid physical configurations and within the original endpoint section; these tests are floating-point diagnostics, not interval certificates. Compilation and visual inspection check the manuscript, not the full continuum proof. No independent human-review or formal-proof status is claimed.
