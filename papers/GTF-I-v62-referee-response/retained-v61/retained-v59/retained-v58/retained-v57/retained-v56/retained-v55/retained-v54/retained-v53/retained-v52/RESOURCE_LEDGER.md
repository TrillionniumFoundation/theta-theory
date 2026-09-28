# Resource ledger — Revision 52

| Resource | General structural theorems | Rational finite-group compiler (`thm:uniform52`) |
|---|---|---|
| Persistent labels | The primary width invariant; all hidden persistent state is counted | At most the signed-seed orbit size `M <= 2D|G|` |
| Row description | Arbitrary horizon-specific real tables are permitted; not priced by width | One permutation table of `O(|A| M log M)` bits and rational readout data of `O(MDL)` bits |
| Sampling | Exact prescribed stochastic rows are part of the atomic model | Deterministic command updates; exact rational query sampling with fewer than `2L` expected fair bits under the stated encoding |
| Working storage | Not bounded by a width theorem alone | `O(log M + L)` for the stated readout procedure |
| Time and uniformity | Clock and horizon can be free; a new machine may be chosen for every horizon | Same orbit tables for every horizon; initialization depends on the supplied seed, not the horizon; rejection has unbounded worst-case time |

The local degree-three criterion has explicitly counted variables, equalities, and interval inequalities. These polynomial description counts do not imply polynomial-time quantifier elimination. The positive-error prefix formula may enumerate exponentially many words. The global SOS theorem guarantees a finite certificate for an infeasible fixed instance but does not bound the required degree usefully or implement a general search engine.

The exact rational verifier rejects floating-point coefficients and nonpositive claimed margins. Resource exhaustion yields `undetermined`, not a favorable feasibility verdict. No general exact algebraic-number sampler is asserted by the rational finite-group theorem.
