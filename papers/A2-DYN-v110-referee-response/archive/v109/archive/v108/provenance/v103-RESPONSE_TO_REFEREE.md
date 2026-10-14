# Response to the external report on A2-DYN revision 102

Author: Qian Qi. Revision: 103, 13 October 2026.

Controlling report: `reviews/a2-dyn-v102-external-top4-review-2026-10-13/REFEREE_REPORT.md`, commit `37faf38478a5b561c3aa4a1faf63da378caf8189`, blob `6c6bbd2fc9fd5e6da575ac6db9827448e091af3d`.

Frozen author baseline: `0cc27da5fbfb480e9a8fdbe7631ed3f869c99cd9`, paper tree `2ac230d86ffc9c4907e57f0e425b80d97971a6c9`. The author branch begins at the controlling review commit. All 246 inherited core files and the complete preceding article are retained; overwritten top-level files are snapshotted under `provenance/v102-*`. Both revision-88 variants remain separately pinned.

We thank the referee for requiring control of the positive endpoint minimum itself and for identifying the degeneracy `v=s b'` at a backward-critical entrance. The new argument changes the comparison direction on the same positive measure. It fixes distance in roof time to one endpoint rather than relative position between the endpoints. The resulting densities are `c^epsilon/|a'|` and `c^epsilon/|b'|`; neither the small residence nor the relative-position factor occurs. We prove complete pointwise bounds for the newly admitted source and for an expanding-endpoint class uniform in every relative position. We do not claim that these certificates cover every physical pair.

## 1. The entire failure source and quantitative recovery — requests 17.1, 17.2, 17.5

Theorem `thm:v103-gap-height` proves, at finite collision count and at the original target roof, the estimate for the positive source admitted by either endpoint-distance clock. The measure is the original minimum of the two weighted endpoint traces before projection. Its original selector is held at the starting roof. Its transported image is bounded by the complete short paired source in the same exact event, not by an averaged substitute on the left.

Theorem `thm:v103-recovery` applies this estimate specifically to the preceding positive failure source. It splits that source exactly into a recovered part `V_B` and a remainder `U_B^rem`. The recovered part has ordered essential height `O(B^-1/384)` under the original schedule. Pointwise and at finite count, `0 <= U_B^rem <= U_B`; this is not a reassignment to a signed difference. The full scalar budget becomes `E_M <= H_M(U_B^rem) + C_M B^-1/384`.

The full-source request is advanced but not claimed closed. Failure of all three comparisons can still carry positive mass, and no bound proving its height vanishes has been established here. In particular the new equivalence in the scalar theorem is not itself presented as a smallness theorem for the remainder.

## 2. Backward-critical corners — request 17.3 and report sections 6, 12

Proposition `prop:v103-critical-trace` supplies the previously compressed local calculation at a regular nongrazing critical extension. All angular rays approach the same critical point by local inversion of the positive endpoint Hessian. The incoming roof is constant. The incoming weighted trace is exactly `omega(q*) W(q*) / (4 pi c_* e_perp^T K_* e_perp)` and can be positive. Its logarithmic angular derivative, when the numerator is positive, is bounded by `2 Lambda_circ/lambda_circ`.

The actual paired weight remains the minimum with the outgoing trace. We explicitly do not infer a bound for that minimum's relative derivative merely from the incoming formula.

The outgoing-endpoint-distance flow preserves `b-u`. If `a` is constant and `b` increases on the comparison side, the residence increases while the gap stays fixed. The entire source position remains inside its segment, uniformly as `s` approaches zero. There is no division by `s` in its Jacobian or admission radius. Theorem `thm:v103-certificate` and Corollary `cor:v103-corners` prove the conclusion under the stated endpoint speed, positive-weight variation and reach conditions. Thus the geometrical corner responsible for the previous coordinate degeneration is actually treated, not removed or assigned zero trace.

## 3. Folds and exact zero speed — request 17.2

When the two endpoint slopes have opposite signs, take an angular side which expands the interval. If the chosen endpoint has the larger speed, residence growth is at most twice that speed. The new certificate applies through the entire relative-position range, including a zero of `(1-s)a'+s b'`. It needs no relative logarithmic derivative of the residence. With collar `4 delta` and comparison width `delta`, the residence constraint is automatic for the certified slope class.

Lemma `lem:v103-flat` also identifies the exact zero-speed measure. Unless both endpoint derivatives vanish, zero relative speed occurs at at most one relative position and is paired-measure null by Tonelli. Definability of the endpoint maps reduces the remaining regular positive zero-speed measure to intervals with two constant endpoint roofs. Their positive rectangular roof pulses are displayed explicitly, not declared small. Near-stationary neighborhoods, flat pulses and short comparison reach remain separate from the certified fold estimate.

The two affine examples in module 249 demonstrate positive-measure old-clock failure regions recovered by the new clock. They are model checks of the coordinate argument, not claims to additional realized Lorentz families.

## 4. Physical summation — request 17.4

Theorem `thm:v103-gap-coarea` constructs each flow on the same actual disjoint pairing sheets. Its stopped graph is one-to-one, and the coarea identity is proved before physical summation or a norm. Borel selectors and compatible coordinate seams do not create copies of a trajectory. Actual loss of pairing regularity is still a stopping event.

The union of the two new admission sets is disjointized by first successful direction. The factor two in the finite-count comparison counts these two explicitly chosen comparison fields, not the number of physical words, chambers or interfaces. No unweighted word cardinality appears.

## 5. Jacobian convention — request 17.6

The new theorem states the pullback convention directly next to the Jacobian: integration of `phi(Theta_h y) J_h(y)` against the starting paired kernel equals integration of `phi` against the target kernel on the image. In endpoint-distance coordinates the ratio is `(c/|e'|)(Theta_h y)/(c/|e'|)(y)`. The absolute speed is retained. The barycentric residence factor disappears by an exact coordinate change; it is not omitted from the original measure.

## 6. Schedule and pointwise topology — request 17.5

The old relative clock uses its unchanged collar `2 delta`. The two new clocks use `r_g=delta`, `Delta_g=4 delta`, `q_g=epsilon^(1/32)`. Hence the recovered height is bounded by `C(epsilon^(1/32)+epsilon^(95/32)) = O(B^-1/384)`. On the expanding-endpoint certificate the clock is at least one half, and the whole certified positive source has the stronger bound `O(epsilon^(1/16)) = O(B^-1/192)`.

Every parameter is fixed as a function of the original outer `B` before the collision limit. The target remains the unaveraged essential height; only the right-hand comparison is averaged. The source, section, original smooth guard, exact displacement and occupation coefficient and all arithmetic classes are unchanged. No lower original residence, incidence or gradient cutoff is introduced.

## 7. Qualification and preservation — request 17.7

The new workflow pins the v102 author tree, the v102 report blob and both v88 variant trees. It verifies inherited Git blobs and executable modes against the new source and the exact working checkout, checks the fourteen overwritten root snapshots, and requires the actual recorder union of all 249 mathematical cores. The complete preceding article is assembled using its preserved original main source. Normal and optimized finite diagnostics run without assertions that disappear under optimization. Both native PDFs must stabilize references and pass the warning and page-geometry gates.

No local full-source qualification is claimed for this revision. Remote qualification is reported only from an actually completed run at the final author SHA. The workflow's existence is not a passing run, and the completed v102 baseline artifact does not qualify v103.

## 8. Independent verification and architecture — requests 17.8, 17.9

No independent human specialist review or formal proof certificate has been obtained. The new dependency appendix separates the inherited optical/coarea/pressure inputs from the explicit endpoint-distance changes of variables and clock comparison. The regular critical-extension calculation, physical-sheet continuation, positive minimum and one-sided certificates are identified as the new audit targets.

The manuscript remains centered on the original exact-label pointwise problem. It contains the retained relative comparison and the three new theorem-proof modules. Full scalar closure, unrestricted point-conditioned kernels, denominators and likelihood laws are not promoted while `H_M(U_B^rem) -> 0` is unproved. The existing article, mathematical archive and review history are preserved, rather than deleted, reframed as another topic or represented as a completed upper pointwise theorem.
