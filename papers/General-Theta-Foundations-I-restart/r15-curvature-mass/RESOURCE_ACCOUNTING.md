# Resource accounting

| Resource | Construction / charge | What is not claimed |
|---|---|---|
| Sensing calls n | every physical instrument report, including failed/validation outcomes | successful samples only |
| Total measurement budget N | n+1 for engine plus audit; n+2 for early-channel engine plus audit | audit supplied free to the predictor |
| Autonomous persistent labels | 1+sum L_t <= M; at least n nonterminal labels | labels count only terminal codewords |
| Same-task joint labels | one early-interface label plus M-1 engine labels; k=n+1 compulsory nonterminal labels | terminal-recall channel statuses can be merged without a different interface |
| Bits | ceil(log2 M) for the persistent label | total bit complexity equals this |
| Clock | encoded in label supports, proven necessary for exact deadline | external requests/timestamps satisfy the same lower |
| Programme description | O(M(dp+log |A|)) plus model, integration and numerical routine descriptions | exact Bellman planning is efficient or uniformly computable in every Borel model |
| Temporary workspace | grid evaluation, matrix/likelihood routines, output calculation; erased at cuts | a persistent exact posterior hidden in scratch |
| Calibration | conditional complete-kernel/scored-law coupling; independent inaccessible offset in matched example | every kernel-calibration problem has the same delta lower |
| Numerical precision | coordinate b_t, output u, event xi_t; explicit boundary b_t/h_t | coordinate error equals task error |
| Simulator internal labels | S times target M is a safe serial implementation | S*M is generally optimal |
| Simulator deficiency | complete common scored-law TV; serial defects add up to one | marginal report TV or fixed-time equality automatically transfers all stopping tasks |
| Physical preparation/reset | each preparation branch of C_t^a charged and recorded separately | repeat-until-success resetting is free |
| Physical time | sum declared instrument, planning and evaluation costs under the selected model | a matched universal clock-time complexity theorem |
| Early output | irreversible, write-only, cannot be read as a register | free persistent output tape |

With n engine calls, the central excess laws are M^(-2/d) and (M-n)^(-2/d). In the product task k=n+1 before audit and N=k+1 including audit; the autonomous geometric term is (M-N+1)^(-2/d), M >= N. Both error coordinates are actual independent components of that same task. Numerical and causal comparison bounds are additional feasible upper certificates, not an optimal multi-resource region.
