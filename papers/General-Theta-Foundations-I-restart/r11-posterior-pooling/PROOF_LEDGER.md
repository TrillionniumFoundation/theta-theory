# Proof ledger

| Claim | Proof mechanism | Status / boundary |
|---|---|---|
| Checkpoint seed reduction | Fix independent whole seed only in full-history relaxation; integrate deterministic lower | Full proof; explicitly not an autonomous purification claim |
| Exact retained posterior | Coordinate identity P(X'=k,J=j)=E[W_k 1{W in cell}] | Full proof; pool across all incoming labels |
| Bellman–Jensen identity | Minimize at conditional label belief; telescope E V_t(Q_t)-E V_t(W_t) | Full proof; actual controller law, not optimal-policy law |
| Integrated O(h^2) gap | Convex tangent, subharmonic averaging, radial derivative, Laplacian mass, cutoff and mollification | Full proof for bounded-density measures on fixed compact interior carriers; no differentiability or margin assumption |
| Optimal adaptive memory lower | Last action-before-report conditioning; mixture density bound; M-ball union; projection | Full proof; same full-history policy class and absolute Bayes baseline |
| Total state upper | Disjoint phase-labelled cells plus initial label | Full proof; 1+sum L_t, not just terminal labels |
| Raw sensor geometry | Explicit inverse; Jacobian lambda^d product(q_i)/D^(d+1) | Full proof for arbitrary declared dimension, not finite checks only |
| Strict feedback | Monotone positive power series for information gain; both sides have positive noisy mass | Full two-call proof; longer-horizon thresholds not asserted |
| Stratified upper/lower | Facewise Jensen, atom exactness, actual submass small-ball | Full proof; terminal lower exponent need not dominate arbitrary intermediate dimensions |
| Validation realization | Flagged positive-noise/physical-state readout mixture | Full proof; changes acquired support dimension in the recursion |
| Digital implementation | Approximate Bellman slack; first grid mismatch; actual boundary slab mass; terminal projection | Conditional certified precision proof; no arbitrary Borel computability assertion |
| Attained joint resource law | One direct-sum audit; same product prior; early channel TV lower | Full fixed-n proof; no automatic allowed-error floor |
| Predictive quotient | Compact evaluation images + explicit Borel section + determining tests | Full sufficient-class proof; not a general quotient measurability assertion |

Continuous proofs are in the mathematical source. Exact finite rational regressions are independent sanity witnesses, not certificates of those proofs. External correctness and priority remain for independent review.
