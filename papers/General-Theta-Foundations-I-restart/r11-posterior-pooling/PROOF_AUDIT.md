# Proof audit and stress points

1. The retained finite-state posterior is P(X_t | Z_t), not P(X_t | all discarded observations). The proof never equates them. The transition uses the former, which is exactly the Bayes input given the machine's information.
2. The new actual law is computed after choosing actions at existing label barycenters. This is a forward offline recursion, not a circular definition through unknown future labels. Every cell pools all incoming edges; edgewise representatives without the incoming-edge identity would fail.
3. V_t is an infimum of affine risks of fixed future policies, with uniformly bounded coefficients. It is concave and uniformly Lipschitz even at switches. The second-order estimate integrates curvature, rather than assuming a bounded Hessian.
4. The integrated Jensen proof uses a fixed interior collar. No uniformity as kappa tends to zero, rho diverges or a stratum degenerates is asserted. Submeasure mass is not renormalized.
5. The lower conditions before the final action/report under every admissible history; uniform incoming-belief smoothing includes compressed beliefs as well as full-history beliefs. A density bound for one exploration policy would not suffice.
6. Bellman comparison optimizes the legal action class. In raw sensor-selection examples actions change measurement channel; the general finite-state theorem also permits controlled transitions. Both procedure classes use that same control class.
7. The autonomous proof stores all phases. The checkpoint lower relaxes prior acquisition; independent seed conditioning is not incorrectly used to construct a clock-free autonomous deterministic policy.
8. Digital mismatch is bounded using the unconditioned ideal posterior law and first-disagreement inclusion. Conditioning on no earlier mismatch is not assumed to preserve its density bound.
9. Terminal numerical forecasts are simplex-valued; projecting onto the simplex does not enlarge Euclidean output error. Their reference loss is bounded by two, and its squared centroid error is computed before coupling to a changed trajectory.
10. For the joint lower, hidden prediction, calibration and bit uncertainty are lower bounded under the same product prior, so their risks can actually be added. The exact-bit virtual output has a compulsory early deadline.
11. The finite programme may contain known real integrals abstractly. Certified digital approximations require coefficient, report, comparison and output certificates separately; policy planning can be costly. No computational bound follows from label count alone.
12. Source verification includes control-character checks, exact citation/label sets, isolated recorder inputs and normal/-O equality. These do not decide mathematical correctness.

Unclosed: horizon-uniform overlapping-noise matching; near-necessary intrinsic completion criterion; arbitrary unknown kernels; degenerating or infinite stratifications; full optimal computation/simulator resource region; unbounded stopping and infinite-path transfer.
