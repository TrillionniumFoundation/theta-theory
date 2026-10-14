# Response to the v101 submission-state and v100 mathematical reports

**Author:** Qian Qi. **Revision:** 102, 13 October 2026.

**Latest controlling report:** `reviews/a2-dyn-v101-submission-state-external-top4-review-2026-10-13/REFEREE_REPORT.md`, commit `35f4a36f5b14d93a9716029ddc03226cf86a5834`, blob `d64268f21394e8edf9e5b9bd2408ed94360966b6`.

**Substantive mathematical report:** `reviews/a2-dyn-v100-uniform-capacity-external-top4-review-2026-10-13/REFEREE_REPORT.md`, commit `61db130152c4f238f9bdd9f01c8d01bc049989fe`, blob `b44278830cf52568a010a659dc8e38d348b5d1a4`.

**Actual author baseline:** v100 uniform capacity, commit `7b2d9c999e987f61a38e9fcadd7fd7605192f35a`, paper tree `7b8524304ab2eebc935e4c25f74b30d39f80c995`.

We thank the referee for identifying both the submission-state error and the precise mathematical distinction between a trace difference and a positive common trace. This revision contains new author mathematics. Its three modules act on the minimum of the two original weighted endpoint traces itself. They introduce a transverse comparison between actual same-label trajectories, not a signed cancellation and not a volume replacement. The original pointwise target remains unchanged. The full positive paired-trace height is not declared closed: the new estimate pays its transversely admitted part, and retains the unadmitted part as an explicit positive source.

## 1. Actual author manuscript — v101 request 14.1

The revision branch starts at the latest report commit, preserving both frozen reports. The active directory is `papers/A2-DYN-v102-referee-response`; it has a new article, response, proof ledger, source manifest, three new cores and an exact-SHA workflow. Both response and referee-copy refs are intended to identify the same final author SHA. We do not count the old v101 alias as an author revision or invent an intervening mathematical manuscript. All 243 actual inherited cores and the complete v100 article are preserved.

## 2. Positive paired trace itself — v101 14.2; v100 11 and 14.1

Module 244 forms the exact positive measure `c(theta) ell(theta) dtheta ds`, where `c` is the same-segment minimum of the two original weighted endpoint traces and `s` is relative position between those ends. Its roof pushforward is exactly the original paired source. This is an equality before norms or collision limits; the minimum is never interchanged with physical projection.

On a regular pairing chamber the roof is `a(theta)+s ell(theta)`. Holding `s` fixed gives the transverse field `V_perp=(partial_theta F)^(-1) partial_theta`. Its Jacobian relative to the paired measure is the ratio of `c ell/|partial_theta F|`, not the original volume Jacobian with a missing endpoint factor. It keeps the identical exact event while varying the actual physical trajectory. Unlike radial transport, it need not terminate merely because original radial residence is short.

Module 245 proves the finite-count pointwise comparison `T_adm(t) <= (q_perp r_perp)^(-1) integral_[t-r_perp,t+r_perp] T_Delta(u) du`. The left side is the positive paired minimum at the original target roof. The right side is controlled by the original bad-source average and the already proved uncut trace-comparison error. Thus its ordered essential height is at most `C q_perp^(-1)(epsilon^(1/16)+(1+epsilon^(-1)) Delta)`. This is a new height estimate for the admitted common trace, not an estimate of outgoing minus incoming traces.

The theorem does not establish admission of every nongrazing short segment. The report's full deconcentration request is advanced but not marked complete. All unadmitted positive trace is retained.

## 3. Complete physical summation — v101 14.3; v100 14.2

The barycentric representation is based on the inherited Borel bijection of actual maximal segments. Fixed-count definable geometry supplies regular pairing chambers; there is no claim that their number or derivatives are uniform in the collision count. The coarea comparison sums physical sheets before using target domination. Uniqueness of the transverse flow gives multiplicity one on its graph at each time. No word-count, number-of-chambers or unproved transverse-overlap coefficient is multiplied into the bound.

The original target selector is held at the starting roof and is not differentiated. The comparison target drops that selector only for an upper bound by all short paired segments in the identical exact event. There is no neighboring occupation coefficient or displacement enlargement. Chart seams that are smoothly compatible are continued. Any actual loss of pairing regularity is a comparison failure, not an omitted original source.

## 4. Explicit geometric test — v100 14.3

Module 246 gives a relative two-ended certificate: on one angular side, a positive lower transverse speed and bounds on the logarithmic derivatives of the residence, positive common weight and speed guarantee capped-clock value at least one half. The radius is explicit. If the two endpoint derivatives have the same sign, the speed and its relative derivative can be checked at the two ends, uniformly for all relative positions.

No positive lower original residence enters this certificate. Parallel moving endpoint roofs demonstrate the exact cancellation of that small length in the paired Jacobian. This calculation verifies the certificate algebra; it is not asserted to be a new physical realization. A backward critical entrance has `a'=0`, and may still be transported at an interior relative position; no uniform estimate near the critical corner is inferred. Its possibly nonzero trace remains in the unadmitted source.

The uniform pressure theorem does not itself prove these relative transverse tests on all physical chambers. That further geometric obligation is stated explicitly rather than assumed.

## 5. Schedule-compatible essential-height rate — v101 14.4; v100 14.4

The original schedule is retained: `q=1/8`, `r0=c epsilon(B)^4`, `a=sqrt(q r0)`, `delta=6q r0`. Set `Delta=2delta`, `r_perp=delta` and `q_perp=epsilon(B)^(1/32)`. All of these are chosen before the collision limit. The admitted common trace is then `O(epsilon^(1/32)+epsilon^(95/32))` in the exact normalized height. The remaining explicit scalar costs are smaller. The new theorem is

`E_M <= H_M(U_B) + C_M B^(-1/384)`,

where `U_B` is precisely the original selected paired source on transverse-clock failure. It includes zero speed, insufficient transverse reach and positive critical traces when not admitted. The original pointwise assertion is equivalent along this schedule to `H_M(U_B)->0`; that last limit has not been proved. No narrower topic or weaker principal target is substituted.

## 6. Exact conventions and downstream order — v101 14.5–14.6

The section, original guard, source normalization, exact labels, actual-return interpretation, all arithmetic peaks and zero classes are unchanged. Both endpoint trace conventions remain those of the preceding source. No selector trace is introduced. The positive paired measure is used only to represent and compare the original paired term, not to renormalize the collision source.

The full upper pointwise half, raw LLT, unrestricted denominators, point-conditioned kernels, likelihoods, entropies and path laws remain unpromoted. The verifier rejects any inherited claim promotion. A family-uniform fixed-cutoff or admitted-source theorem is not relabeled a complete source theorem.

## 7. Source/build evidence and specialist audit — v101 3 and 14.7

The two actual v100 author workflows `38357156664` and `38357171483` succeeded at the frozen v100 SHA; these are baseline evidence only. Neither frozen report is edited to change its historical status. The new v102 workflow pins the v100 source tree, both reports and both v88 variants, verifies inherited bytes and modes and all root snapshots, compares ordinary/optimized finite fixtures, and compiles the complete article and archive with recorder and warning checks at the final author SHA.

No independent human specialist review has been obtained. The new audit targets are the fixed-count pairing-chamber decomposition, positive paired coarea, transverse Jacobian orientation, multiplicity-one target map, relative two-ended certificate and schedule. The uniform pressure and inherited four-record/coarea chains remain source-pinned inputs, not independently recertified by new software tests. The focused article gives the short active dependency route, while the entire historical mathematics remains compiled in the supplement.
