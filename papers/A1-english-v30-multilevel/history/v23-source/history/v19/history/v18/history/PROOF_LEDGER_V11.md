# A1 v11 proof and resource ledger

The old 52 named-result labels and 49 complete proof blocks remain in the expanded manuscript. Their SHA-256 multiset is recorded in `V10_PRESERVATION_MANIFEST.json`; the ten inherited body files are additionally checked against their Git blob hashes. These are syntactic preservation checks, not formal mathematical verification.

| New result | Dependencies | New conclusion and boundary |
|---|---|---|
| Proposition 7.1, `prop:separated-floor` | Formal future labels; fixed one-step separation | Explicit separated-chain floor for the full Xi profile; attributed to the controlling referee note |
| Corollary 7.2, `cor:uniform-resources` | 7.1; old finite compiler and finite moment lemma | Stronger uniform sufficient precision, program size and rational-operation bounds |
| Lemma 7.3, `lem:radius-certificate` | Finite history net; classical greedy separation | Two-sided finite certificate for unrestricted-centre covering radius |
| Theorem 7.4, `thm:adaptive-compiler` | 7.3; raw Lipschitz recurrence | Terminating first-success mesh at the covering scale, for positive e(M); no prior knowledge of e |
| Corollary 7.5, `cor:absolute-tolerance` | 7.3–7.4 | Tolerance-limited termination including e(M)=0, without an equality test |
| Proposition 7.6, `prop:program-certificate` | Certified representative/transition/query evaluations | Separate finite residuals for actual transition and decoder tables; corruption changes the certificate |
| Lemma 7.7, `lem:explicit-moment-certificate` | Coefficient l1 telescoping; positive evidence | Explicit finite input, denominator and quotient allowances; coincident labels need not have equal advice values |
| Lemma 7.8, `lem:cover-profile` | Old reachable cover and checkpoint lower theorem | Both directions of e(M)^2 comparable to Xi; no dependence on the new adaptive causal conclusion |
| Theorem 7.9, `thm:profile-adaptive` | 7.1, 7.4, 7.7, 7.8; old common-exploration lower law | Adaptive sufficient precision and program bounds for the complete profile with exactly the same upper M-label budget |
| Corollary 7.10, `cor:resource-phases` | 7.9; old two-parameter law | Three sufficient read-only program scales at intersecting collision lines |

## Counted resources

Persistent state: at most M indices at each stage with supplied clock; an autonomous clock costs only the displayed fixed-horizon factor. Current input codes and returned outputs are transient. The read-only program and temporary numerical workspace are not called persistent state.

Input interface: known calibration and finite coefficient/moment approximations with certified bounds, requested at successive tolerances offline. The online program has neither an exact-real oracle nor a history tape. A memoryless input coder is required to compare with the original label converse.

Guarantees: full Xi regret, uniformly over the fixed compact calibration set and M. The prior is arbitrary full support for the intrinsic theorem; a numerical procedure or supplied advice is an additional realization interface, not an assumed density. Constants are fixed-horizon and may depend on that prior.

Converse: the persistent-label regret is sharp. Input precision, program length, total work and moment-oracle running time have no matching lower theorem in this revision. The exact first-success precision formula describes the constructed algorithm, not all possible algorithms.

The diagnostics exercise signed input errors, all queries, intentional output corruption, nontrivial off-grid recurrences and known covering certificates. None is used as a substitute for the continuum proof.
