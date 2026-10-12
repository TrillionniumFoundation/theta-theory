# Adversarial proof audit

The following are the vulnerable steps rechecked in this revision.

**Minimization and concavity.** A finite minimum of concave functions remains concave. The full-history value is identified by discounted backward induction, not by assuming a finite controller is optimal. Overlap is uniform over all b-call feedback policies, so the span contraction can compare policies selected at different inputs.

**Physical versus programmed barycenter.** A codepoint controls the routing rule, not the actual raw hidden state. The raw frozen map is linear on physical ensembles even when the actual posterior differs from the programmed q. This is why the resolvent describes execution, and why numerical boundary mass uses both x and q.

**Initialization.** The new construction is Z=s B0+beta PZ. The coefficient s normalizes a terminal probability measure, not an occupation of total mass 1/s. The initial label is never reused. At s=1, beta=0 and all equations remain valid. At small s the statistical span bound uses raw overlap; computational sensitivity can still grow as 1/s.

**Nonlinear fixed point.** Existence is from Kakutani, not Banach iteration. Frozen P has a unique injected solution but the calibration table need not be unique. Compactness alone is not a numerical algorithm; the effective compiler has its own computability/modulus hypotheses.

**Geometry and boundary.** A row upper density gives an anti-concentration lower, not a density lower on all of K. The curvature upper uses true density times a positive curvature measure. Neither claim uses volume on a merely reachable support. Relative strata need their own conditional densities and actual weights.

**All-observer lower.** The decoder is label-only, even in the enlarged lower class with time-dependent actions/updates. A time-dependent free decoder would have more than M readouts. The independent hazard is conditional on the entire history including private coins; marginally geometric stopping alone is insufficient.

**Core/bit composition.** Given the early bit information, any adaptive core policy still has risk at least the same core full-history optimum. The core contains no later source of bit information conditional on actions and reports. Product-prior lower terms therefore coexist. Bit U is 0/1 here, so complete-erasure squared loss is 1/4, not the +/-1 convention used in old independent tasks.

**Effective risk.** Frozen table perturbations remain genuine positive stochastic programs. A rational program can approximate risk without preserving exact calibration. The reported lower in prop:effective is within the explicitly stated common-cell family, not a computational characterization of all Borel programs. The all-Borel lower remains the analytic acquired-mass bound.

The raw instrument proofs are finite-dimensional. No unknown-model adaptation, LDP equivalence, arbitrary optimal stopping or unbounded-operator extension is inferred.
