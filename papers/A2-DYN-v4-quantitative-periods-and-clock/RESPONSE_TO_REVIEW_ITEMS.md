# A2-DYN v4: response to verified review items

## Provenance of the revision

The controlling manuscript is A2-DYN v3 at `55ab80ed1a4f11b58ce9a88c365b0cea2e2ce191`, not the previously delivered local v2 archive. The revision continues the same mechanical/raw-local-limit problem.

An A2-DYN-specific referee report was not located. The searches and their limitations are recorded in `SOURCE_AUDIT.md`. The actual dynamics document `papers/A2-DYN-v1-raw-local-limits/SPECIALIST_REVIEW_BRIEF.md`, blob `a22a2fd5a84de5a7860a4c20568df35ce844d903`, identifies itself as a handoff, not an independent report. The five tracks below correspond to that document and the analytical requirements printed in v3. They are not fabricated referee quotations. The separate A2-GEOM v43 report is not treated as a dynamics review.

## 1. Actual mechanical records and changing first returns

All prior mechanical definitions, selected returns, and the full marked suspension law are preserved. The original section Y_R and enlarged section Y_R* remain distinguished. No additional sensor, independent-flight approximation, or replacement of the preparation law is introduced.

The new uniform clock proof starts with the actual changing first-return records. Theorem 12.2 combines their fixed-record first-moment continuity with the exact Kac means and a compact subadditive lemma. It proves uniform convergence of the whole first-order return process. Lemma 12.3 supplies a truncated-tail maximum estimate without independence. Its length-biased change of initial law is explicit, rather than replacing the stationary base law by the return probability.

Theorem 12.4 inverts the cumulative physical roof and controls both initial and terminal pieces simultaneously over [0,t]. Visits are counted in (0,t], so the inverse identity remains correct at event times. The maximum marked unfinished return is o_P(t), uniformly in radius. The earlier o_P(sqrt(t)) result for finitely many stationary endpoints is retained, not relabelled as a growing-window Gaussian estimate.

## 2. Joint arithmetic, quantitative separation, and approximate phases

The complete joint periodic annihilator and the real period determinant remain intact. Section 5 now quantifies the previously qualitative infinite-cycle argument.

Lemma 5.1 bounds the Hessian of the exact nonlinear half action on its entire height box: 3I <= H <= 12I, diagonal <= 10, and neighboring negative entries have magnitude between 1/2 and 2. Applying the positive Neumann series to the averaged Hessian gives two-sided endpoint-height estimates. This is not a quadratic surrogate for the nonlinear trajectory.

Theorem 5.2 compares exact minimizing actions by appending zero and truncating the next minimizer. It proves 400^(-m)/10000 <= E_(m+1)-E_m <= (49/100)^(m-1)/300, uniformly over the radius interval and all m. The upper bound selects a cycle length at which the phase lies below one full turn; the lower bound prevents its disappearance.

Theorem 5.3 uses the exact three-period cancellation, including both physical and induced counts. At roof frequency b >= 1 it yields a discrepancy at least b^(-gamma)/(2400000000*pi), with gamma=log(400)/log(100/49)-1, using a longest word with 2m(b)+3 collisions and m(b)=1+ceil(log(b)/log(100/49)). Corollary 5.4 then gives an essential-supremum error lower bound for circle-valued approximate phases continuous at the selected periodic states.

This supplies a quantitative periodic input at unbounded roof frequencies. It does not assume that a merely measurable spectral transfer function has the continuity used by the corollary, nor that an operator eigenfunction has a uniform nonzero modulus. That bridge remains a precise functional-analytic task, rather than an implicit assumption.

## 3. Raw edges and all-frequency inversion

All old critical-word, coarea, Hessian, jump-coefficient and individual edge-decay proofs are unchanged. The local inversion identity retains every subtraction/addition correction, including the remote-edge term. The target remains the unmodified mixed density.

The new periodic estimate can be used only after proving an appropriate operator comparison. It is not itself the low/middle/high-frequency splice, an absolute-integrability estimate, or a sum over central singular branches. The full central-branch residual obligation remains in Section 13. The article does not infer an integrated frequency tail from finite-n density continuity or from a finite set of tested periods.

## 4. Conditioning, geometry, and physical prediction

The v3 positive-denominator comparison and the stronger shrinking-interval interface are both retained with their actual hypotheses. Corollary 12.5 adds a physical rate prediction bound. Writing b_* = min_R mean_tau_R and L_*=15/(4b_*^2), the observed collision rate differs from the rate at an estimated radius by a first-order stochastic error plus L_* times the geometric error. The exceptional probability is bounded by omega_t(epsilon) plus the failure probability of radius estimation. No independence is required.

The function omega_t tends to zero uniformly but is not assigned a fabricated numerical rate. The finite-subcover block budget is stated explicitly in Lemma 12.1. An effective resource bound requires effective finite-block estimates; a Gaussian or raw-density conditional bound requires its stronger printed inputs.

## 5. Complete manuscript and subsequent independent review

The article is a complete native AMS manuscript, not a patch-only fragment. Every v3 proof body and label is retained. Section 5 adds four results and Section 12 adds five; the source audit checks all 37 proof bodies and 107 labels. Old paper and review directories are not edited.

The next review should assess the nonlinear averaged-Hessian bounds, the append/truncate inequalities, three-period cancellation with actual returned counts, continuity/subadditivity of the centered norms, the length-biased transfer, and the event-time inverse convention. Finite rational checks and a clean PDF build are supporting evidence, not replacements for these analytical proofs. No independent human specialist review or journal acceptance is asserted.
