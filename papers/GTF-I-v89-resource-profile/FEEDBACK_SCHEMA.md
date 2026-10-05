# Conditional reset-policy certificate — v88

`feedback_budget.py` accepts exactly `schema,N,b,s,gamma,root,nodes`. The schema is `gtf88.reset-policy/1`. N and b are positive integers with b<=N; booleans are not integers for this interface. s and gamma are canonical positive/nonnegative rational strings as enforced by the parser (integers use `"2"`, fractions use reduced positive-denominator `"1/32"`). Nodes are keyed by nonempty identifiers and have exactly `calls,children`. A terminal has zero calls and no children. An acquisition has positive calls<=b and at least one successor. Every node must be reachable, all successor identifiers must exist, children cannot repeat, and the directed graph must be acyclic.

Every path is checked, irrespective of its probability under either hypothesis. Recurrences return the maximum reserved calls and the maximum sum of squared reserved widths. A hard `--max-nodes` limit is an input safety cap: exceeding it raises an error. No prefix is returned as a full policy.

The supplied scalar gamma is **not** verified as a physical fidelity coefficient. Conditional on all fresh block pairs obeying `1-f<=gamma*n²*s²` and on the reset condition, the certificate reports:

- additive root-fidelity lower `(1-gamma*Q*s²)_+`;
- recursive root-fidelity lower `min_path product_nodes (1-gamma*n²*s²)_+`;
- the corresponding conservative trace-distance-square upper, capped by four;
- the policy digest, N,b, Q, number of reachable nodes and explicit scope flags.

The minimum-product recursion follows by applying the same conditional-fidelity induction with nodewise factors rather than replacing the product by one minus the sum. Final states need not be independent across feedback branches.

`--verify` reconstructs the entire certificate and requires exact equality. All canonical rational and structural errors fail closed. This verifier establishes arithmetic and complete-policy properties; it does not inspect hardware, establish fresh-state conditional independence, validate an external curvature/fidelity majorant, synthesize a quantum recovery, or compute the exact optimal distance.

The example `examples/feedback-policy.json` has hard budget N=5, width b=2, rational s=1/32 and declared gamma=2. The independent finite state-model replays in `feedback_check.py` justify that gamma for their specified rational fresh qubit states only. They are not realizations of the general measurement-tube code.
