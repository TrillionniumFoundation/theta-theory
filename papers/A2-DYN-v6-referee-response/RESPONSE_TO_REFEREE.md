# Response to the external A2-DYN referee report

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revision:** A2-DYN v6, 5 October 2026  
**Controlling report:** `reviews/a2-dyn-v4-external-top4-review-2026-10-05/REFEREE_REPORT.md` at `a81eb226c013ca062a6901bb472a90668de29eec`  
**Reviewed source:** `f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`  
**New mathematical checkpoint:** `65551575d46469c3b47c7bf53ff63d787be02085`

We thank the referee for distinguishing the proved mechanical and arithmetic results from the analytical steps needed for the original raw-density local limit. We retain that objective and the entire proof-bearing material of the reviewed article. We have not adopted a different topic or replaced the target by a smoothed or independent-flight model. The revision addresses the substantive gaps by proving exponential tails for the actual return process and the previously missing conditioned square-root unfinished-block estimate, strengthening the phase estimate, and expanding the moving-domain proof. The common induced-operator and all-branch residual constructions are not asserted to follow from these advances alone.

The responses below follow the seven requests in Section 10 of the report. The equation and theorem numbers refer to the 44-page v6 main article.

## 1. The endpoint and the central probabilistic theorem

The endpoint remains the parameter-uniform raw mixed-density LLT for `(K_{n,R},N_{n,R},T_{n,R})` and its weighted positive-denominator interface. Section 19 now states the exact chain from the mechanical results to that conclusion.

The main new unconditional mechanical advance is Theorem 14.3. A fixed smooth nonnegative function supported strictly inside the common square of the genuine return section is used only as a proof weight. The collision-space spectral decomposition and its smooth perturbation give a uniform exponential bound for avoiding its support. Avoidance of the actual return section implies avoidance of that support, so the theorem obtains

\[
\sup_R\nu_R^*(r_R^*>k)\le Ce^{-ck},\qquad
\sup_R\int e^{aQ_R}\,d\nu_R^*<\infty,
\quad Q_R=r_R^*+\tau_R^*+|\kappa_R^*|.
\]

The proof does not change the return event, multiply an anisotropic distribution by the discontinuous section indicator, or assume independence. Corollary 14.4 upgrades fixed-record continuity to every finite moment. The marked intensity argument then proves the conditioned unfinished-block theorem described under request 5.

These advances do not by themselves establish the complete raw LLT. The actual induced phase reconstruction, the infinite covariance criterion and the global raw residual sum remain explicit analytical requirements. This is a statement of what the proofs establish, not a change in the paper's endpoint or an impossibility claim.

## 2. Moving domains, common charts and critical neighborhoods

Lemma 15.1 gives a standalone common-chart estimate. On a fixed rectangle, the cumulative physical time has a coordinate derivative bounded away from zero. The inverse chart and its parameter derivative are written explicitly. A compactly supported smooth cutoff vanishes before the moving chart edge, so its transformed density has a common bounded support and an integrable parameter-derivative majorant. This proves a local Lipschitz bound in density `L^1`.

Proposition 15.2 applies that lemma to the genuine first-return domains. It first truncates the total physical count using Theorem 14.3, then removes neighborhoods of grazing, competing-root, return-boundary and critical initial states. Compactness supplies finitely many charts on which the entire physical itinerary and every intermediate return decision agree for nearby radii. The remaining measure is positive and has mass at most `epsilon` at both parameters because the section mass is constant. Consequently

\[
\|p_{n,R}-p_{n,S}\|_1\le2\epsilon+C_{\epsilon,n,R_0}|R-S|.
\]

The proof does not assume a uniform bound on the density near a critical value. The discarded neighborhoods are measured in initial collision space. The constant is not asserted to stay bounded as `n` or `epsilon^{-1}` increases. The original Theorem 13.2 remains active; the new section supplies the requested expansion rather than deleting the earlier argument.

## 3. From periodic phases to an operator estimate

The recovered periodic analysis in Section 6 proves a lower ratio for adjacent excess increments and a uniform positive phase discrepancy for a frequency-dependent triple of logarithmic-length physical periods. Its source provenance is distinguished from the reviewed v4 manuscript in `SOURCE_AUDIT.md`.

New Theorem 7.1 first locates a large one-step defect at a state of the selected period and thickens only that state. The invariant measure of the resulting ball is computed explicitly. For local Holder exponent `alpha`, norm bounded by `H_0 b^zeta`, and `1 <= p < infinity`, it gives

\[
\|\mathcal D_q\|_{L^p(\nu_R^*)}
\ge C b^{-\lambda}(1+\log b)^{-\eta},\quad
\lambda=\frac2p\max\{1,\zeta/\alpha\},\quad
\eta=1+\frac2{\alpha p}.
\]

The whole-period tube's geometric expansion exponent is absent. The hypotheses still concern controlled regular circle-valued phases; they do not provide such a representative for an arbitrary measurable spectral vector.

Theorem 7.2 is the requested operator-level dependency statement. A quantitative reconstruction of such a phase from every normalized approximate spectral vector, together with the Fredholm index-zero hypothesis, yields a polynomial resolvent bound. The proof includes surjectivity: a lower bound and injectivity alone would not suffice. The reconstruction, modulus lower bound and regularity budget remain to be proved on the actual induced spaces. The separate collision-space realization in Lemma 14.1 is used for a smooth weight near zero and is not mislabeled as the unbounded induced high-frequency operator.

## 4. Individual edges and the complete residual sum

All physical edge calculations and exact subtraction terms remain unchanged. Lemma 18.2 gives an explicit absolute summation criterion for genuine residuals `q_w`, indexed by every physical word including multiplicities:

\[
A_0=\sum_w\|q_w\|_1<\infty,\qquad
A_2=\sum_w\|D^2q_w\|_{TV}<\infty.
\]

Under precisely these hypotheses, the summed residual transform is integrable and its outer-frequency integral is at most `2(2pi)^3 A_2/B`. The proof uses distributional differentiation and Tonelli, and includes all word multiplicities. A residual jump violates the derivative-measure hypothesis; it is not hidden in the remainder.

The new return tail also supplies an exact finite-band physical-count truncation error, `V M_0 C_1 exp(-a_1 L/n)`, for a band of volume `V`. We explicitly distinguish this from an infinite-band or pointwise-density estimate. Neither the per-word jump bound nor the scalar return tail proves the required global derivative sum. Its verification for central and singular branches remains outstanding.

## 5. First-order, square-root and conditioned clocks

This request now has a stronger mechanical theorem, not merely a separation of assumptions. Lemma 17.1 proves the exact marked visit intensity in the stationary induced suspension. The initial block has the length-biased law; subsequent blocks are counted by that intensity. For the maximum full marked block meeting `[0,t]`, Theorem 17.2 proves

\[
\mu_R\{\mathcal M_R(t)>q\}\le C_2(1+t)e^{-a_2q}.
\]

For every event `B_{R,t}` with probability at least `d_t>0`, the conditional bound is the same right side divided by `d_t`. If `d_t >= d(1+t)^{-A}`, all unfinished blocks over the whole interval are `O_P(log t)` and hence `o_P(sqrt(t))`, uniformly in the radius and in the events. No independent-return or independent-conditioning assumption occurs.

Corollary 17.3 proves the deterministic prefix comparison and the resulting conditional bounded-Lipschitz path error of order `log(t)/sqrt(t)` in that probability range. More generally the residual conclusion requires only `log((1+t)/d_t)=o(sqrt(t))`.

The remaining boundaries are exact. This removes the unfinished-block premise, not the functional Gaussian theorem for completed records. The two conditional path laws use the same event. Replacing one exact lattice event by another requires a symmetric-difference bound divided by the actual conditioning probability. A continuous singleton of probability zero is not covered by event conditioning. Remark 17.4 records these distinctions, so no local-limit input is silently inferred from path closeness.

## 6. Version identity and preservation

The reviewed v5-named branch was an alias of v4. Revision 6 has a new directory, consistent metadata, a new mathematical commit and a dedicated workflow. Its author and referee-copy revision branches are intended to identify the same final source, not two differently labeled manuscripts.

All 37 reviewed proofs and 107 labels are retained in active files with their original Git blob hashes. Section 6 also preserves eight proofs from the located unpublished v5 archive. Thirteen proofs are new in v6. The 58 active proofs and 173 labels are checked as source facts, not treated as mathematical acceptance criteria. The old manuscript paths, original report and unrelated papers are unchanged.

## 7. Independent dynamics-specific review

No independent human specialist report has been completed in this execution. We do not relabel author-side checking, finite calculations or a successful build as such a report. The next referee should examine, in order: the collision-space import and smooth-multiplier estimate in Lemma 14.1; the uniform spectral perturbation in Proposition 14.2; the moving-domain compact-chart construction in Proposition 15.2; the selected-period neighborhoods and one-step thickening in Theorem 7.1; and the stationary marked intensity and unchanged-event conditioning in Section 17.

The final realization section and proof ledger identify each unverified premise for the full raw LLT. The revision is submitted for another substantive proof review, without claiming that source qualification or finite diagnostics can replace that review.
