# Response to the referee — A1, English revision 16

**Manuscript:** *Attainable information geometry in positive experiments*  
**Author:** Qian Qi  
**Date:** 7 September 2026  
**Controlling report:** `reviews/a1-english-v15-positive-history-2026-09-07/REFEREE_REPORT.md` at `d89bc35dc5d50240c8ae3c82aa251437dcc2165a`  
**Reviewed submission:** `e1d0ff2ef04a8641ac77923b664c4d3e8386f212`  
**Revision branch:** `revision/a1-english-v16-referee-response-2026-09-07`

We thank the referee for distinguishing the mathematical findings from the significance recommendation. The report finds no blocking defect in the new positive-history and circular chain or in the retained monomial chain examined there. It also records the substantive resolution of E14.1 and E14.2. We do not reinterpret this scoped finding as a certificate of the entire paper or as acceptance by a journal.

The present revision answers the remaining positioning request and makes the mathematical case for the existing classification more precise. It does not replace complete results with weaker ones, append an unrelated application, or present another equivalent phase formula as a new theorem. All complete v15 proofs and named theorem statements remain verbatim in the compiled manuscript. The exposition, literature comparison and response are new; no additional theorem is claimed merely to enlarge the result count.

## E15.1 — Comparison with Bayesian Fourier filtering

**Request.** Compare the closest Fourier posterior/update literature at the levels of representation, physical experiment, information convention and quantitative conclusion. Do not confuse coefficient count with the number of persistent labels.

**Revision.** The new introduction subsection *Relation to Bayesian Fourier filtering* (`sec:fourier-filtering-comparison`) explicitly credits van den Berg, Quantum 5 (2021), 469, Section 2.2, equations (12)–(15), for the established Fourier representation and update machinery. It also compares de Neeve–Lebedev–Negnevitsky–Home, Physical Review Research 7 (2025), 023070, using the versioned preprint's Section II, equations (1)–(3), and Section IV. Both sources are now included in `references-v16.tex`. The inspected primary sources and verification boundary are recorded in `LITERATURE_VERIFICATION.md`.

The comparison is not only bibliographic. It distinguishes four different assertions:

1. **Representation and update.** Trigonometric posterior closure, neighboring-coefficient Bayesian updates and finite Fourier state representations are inherited machinery, not originality claims of this paper.
2. **Experiment and decision.** The circular theorem uses a physical four-cell lookup detector, charges all acquisition trials and failures, and predicts a menu of actual future queries selected independently only after the memory index is formed. Its squared conditional-probability loss is not identified with phase-estimation error, evolution time, sharpness or entropy gain.
3. **Resource.** The restriction is a persistent alphabet of size at most `M`. A finite vector of exact real coefficients ranges over continuously many values and does not satisfy that restriction merely by having finite dimension. Known contrast, a read-only program and transient arithmetic are explicitly separated from persistent state.
4. **Quantitative result.** Lemma `lem:circle-attainment` gives a subprobability minorization for normalized acquisition flags under the actual command-and-report law. Lemma `lem:circle-query-metric` identifies the paired physical scales. Theorem `thm:circle-resolution` matches unconditional lower and worst-history upper bounds and proves one stage-compatible causal realization of the maximum checkpoint profile.

A new paragraph adjacent to the circular theorem repeats the information convention exactly where it is needed. Its one-past/one-future calculation shows both attenuation factors directly:

\[
q_l(z)=\tfrac12+\rho\tau^2\Re(ze^{i\varphi_l}),\qquad
\tfrac13\sum_l|q_l(z)-q_l(z')|^2
=\tfrac12\rho^2\tau^4|z-z'|^2.
\]

This is a transparent illustration, not a new result or a replacement for the higher-dimensional acquisition, covering and causal proofs. We make no claim that the cited authors' phase-estimation theorems are subsumed by ours, or that a priority question is settled by the absence of an identical formula in the passages inspected. **The concrete comparison requested in E15.1 is supplied.**

## E15.2 — Mathematical significance of the classification

**Request.** Make the best case for the proved results at the correct structural level. The report expressly does not require an endless sequence of additional applications or deletion of valid results.

**Revision.** The opening of the paper now formulates the problem as the finite resolution of the geometry of predictions acquired by actual histories. The new subsection *Acquisition, observation, and the resolution invariant* (`sec:acquisition-observation-comparison`) separates the two coordinate chains and identifies what their common coding expression does, and does not, establish.

Our case for the principal result rests on the following mathematical content.

**The invariant is operational and past-limited.** For a fixed full-support prior, the monomial theorem identifies the entire collision-sensitive exterior-volume profile after truncation by the true past dimension. It does not take an arbitrary vector in the future test space and call that vector an attainable posterior. The separated product tangent, complete Newton/Hermite flags and normalized rank argument identify precisely the required acquired directions, with a genuine lower history measure. Their pairing is uniform through simultaneous future additive collisions and does not impose a density assumption on the prior.

**The same invariant controls three different obligations.** The local lower measure alone cannot provide a global upper bound, and independently optimal checkpoint codes need not be causal. The rational posterior image and the real dimension-truncated covering argument give the same initial products as the attained flags; the gap-free raw-moment recurrence then makes that scale attainable by one filter. This match is the principal classification, rather than a spectral estimate followed by an unproved interpretation. The proof dependencies remain visible in `lem:newton-attainment`, `lem:tame-rectangle`, `thm:intrinsic-checkpoint` and `thm:intrinsic-streaming`.

**The circular theorem identifies acquisition as a second source of degeneration.** Its normalized coordinates are `S_j`, its acquired coefficients are `c_j=tau^j S_j`, and its physical prediction coordinates are `Y_j=tau^(2j) S_j`. The two contrast factors occur within the same physical experiment and information convention. Thus an observation spectrum alone cannot determine the attainable finite-resolution law. This is a resolved second mechanism, not an extra observation matrix attached to an assumed nondegenerate posterior body.

The introduction expresses both proved profiles as

\[
\mathcal Q_M(s;p)=\max_{1\le\ell\le p}
\left(M^{-1}\prod_{i=1}^{\ell}s_i\right)^{2/\ell}.
\]

For monomials, `s=d` and `p=p_(n,m)`; for the circle the real side list is paired. This notation explains the common structure but is **not** announced as an additional theorem or as a classification of arbitrary positive detectors. Positivity alone does not imply the needed submersion. Proposition `prop:product-criterion` and Theorem `thm:positive-attainment` retain their actual-tangent hypotheses.

**The consequences test different sources of information.** The monomial ambiguity theorem uses the full future flag rather than the attained past-dimensional truncation. Its width orders, the exact-prefix problem and the common-name regret law therefore remain separately stated. Bounded duality is credited as such; it is not promoted to a second physical-attainment theorem. All finite numerical construction and contract results remain complete, with their original scope.

This is a positive argument for the mathematical significance of the proved classification, not a claim that a wording change compels a particular editorial decision. The report's significance recommendation is a judgment, not a missing lemma with a binary test. **We submit the clarified contribution for renewed independent assessment while retaining the full strength of the results.** Neither source-preservation counts nor arithmetic diagnostics are offered as evidence of exceptional importance.

## Limited editorial guidance

The revised abstract and the two comparison subsections state fixed-horizon uniformity. In the circular theorem, `tau_*` and the comparison constants may depend on `N`, `eta` and `rho`; uniformity is in `M` and contrast on that interval, not in unbounded horizon. The known-contrast and read-only-program conventions appear next to the causal claims. At zero contrast the physical information state is constant; the normalized extension is not called physical rank.

The body consistently retains **width orders**, not an exact ellipsoid assertion. Exact lower-moment constraints and an imperfect common moment name are not interchanged. The circular intrinsic code is not described as an effective compiler; the monomial numerical realization remains in the appendices.

## Source continuity and verification

The new branch descends from the immutable controlling review, preserving that report and the reviewed v15 package. `history/V15_*` archives the replaced expository and verification files. `V15_PRESERVATION_MANIFEST.json` pins hashes of all 84 complete proof blocks and all 87 complete named statements in the expanded v15 manuscript. The revised build checks their exact inclusion and all cross-references. This establishes continuity of content, not correctness of the mathematics.

`validate.py` executes all six unchanged author suites rather than copying their old receipts, then compiles the full paper in three passes. Its current results and source digests are written to `validation/EXECUTION_REPORT.json`. When invoked with `--prior-review`, it additionally executes the pinned v15 referee diagnostic as a regression check; this is explicitly not a new independent review. Visual inspection is documented separately. No old execution receipt is counted as a fresh run.

## Reading order for the next referee

Read the two new introduction subsections and the circular paragraph against E15.1 and E15.2; then inspect the unchanged principal monomial theorem and its attainment/global/causal proof chain, followed by the circular theorem and its two supporting lemmas. The response does not ask the referee to reopen repaired issues without new evidence, nor to infer acceptance from compliance. It asks that the operational, collision-uniform classification and the acquisition–observation law be assessed with their classical inputs and distinct resource convention made explicit.
