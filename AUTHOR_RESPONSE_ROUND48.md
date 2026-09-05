# Author response to Round 48 — Round 49 revision

**Controlling report:** `REFEREE_REPORT_ROUND48_GPT6_PRO_HARSH.md`, commit `cd21a42e47faa8aee0979137da64bf77b016a201`.  
**Reviewed predecessor:** Round 47 source `ce0e531d65974ca46642e374df61f4299fadf786`, distribution `1d10fbf2d1c06e875b5124d39266c7dbb0dd8735`.  
**New main manuscript:** `ROUND49_REVISION.tex`, *Logarithmic-Depth Boundary Identification with Bounded Probes and Retained State*.  
**Retained supplement:** `ROUND49_RETAINED_RESULTS.tex`.

**Delivery distinction:** the GitHub write tool blocked the three-program upload workflow. No alternative upload route was used. The implementation, test suite, and verifier are therefore supplied in the accompanying `ROUND49_REVIEW_BUNDLE.tar.gz`, with their SHA256 hashes fixed in the committed manifest. The full mathematical sources, response, index, manifest, and actual validation records are on GitHub. References to `tools/` and `tests/` below are paths in that accompanying bundle; they are not assertions that these new programs were committed to GitHub.

## Central advance

The two operational defects are repaired directly, and the main mathematical advance addresses the report's proposed bounded-window **unreset** direction. No earlier valid posterior theorem is withdrawn.

The original bounded-support exploration law already supports an attainable logarithmic depth order. The new construction chooses an explicitly small existing diagnostic atom with duration `t_0`, fixes baseline gaps to `t_0`, and commits bounded baseline profiles within blocks before their signs/readouts. Profiles may depend arbitrarily on earlier blocks. Every exploration draw still uses the original law, every sign is fresh and independent, and every individual probe remains bounded by the original horizon. There is no reset, washout, or new long probe.

For explicit `C_b,p_b>0`, the exact posterior of **all readouts in all completed blocks** recovers

\[
J_n=\lfloor r\log n\rfloor,\qquad \delta_n=n^{-s},\qquad C_b r+p_b s<1.
\]

An explicit pair is `r=1/(4 C_b)`, `s=1/(4 p_b)`. The clock is bounded deterministically by `(t_0+T)n'` for the readouts used. The prior is a product coefficient prior with a common positive density lower bound; the working initial-state law remains arbitrary on the fixed Hilbert ball. Coordinate medians give an actual estimator. The all-policy information comparison from two-way propagation supplies the matching **logarithmic order**, not an optimal leading constant or an exact joint depth–accuracy curve.

The fast clock and block commitment are stated in the abstract/model/main theorem and proof, not hidden in the estimates. This is an attainable design in the existing experiment class, not a claim that every within-block feedback controller achieves it or that an arbitrary externally imposed coarse sampling clock is unaliased. The earlier unrestricted-feedback conclusions are retained and quantitatively strengthened separately.

## R48-M1: separate sampling mass from confidence allocation

**Text:** `round49/confidence.tex`, `eq:bands`, `prop:visits`, `eq:visit-constants`, `eq:visit-budget`.

The manuscript now uses `w_q` exclusively for the exploration-law mass and `eta_q` for the confidence-error allocation. For a predetermined grid,

\[
\pi=\rho\min_{q\in G}w_q,\qquad
\eta_{\min}=\min_{q\in G}\eta_q,\qquad
C_v=4/(\alpha_c\eta_{\min}).
\]

The Chernoff count bound uses `pi`. The response-radius logarithm uses `eta_min`. Equal masses are an optional specialization, not a silent identification. The corrected deterministic budget is proved for arbitrary positive allocations with the prescribed sum, including extremely small allocations on a selected grid. Coverage, the sufficient diameter threshold, and the count budget for a predetermined grid remain separate claims.

**Implementation:** `visit_budget` in `tools/round49_certificates.py` has distinct required arguments `sampling_floor` and `confidence_weight_min`. Its log bounds and returned sufficient integer budget are computed using conservative rational/integer arithmetic.

**Regression:** the suite reproduces the old allocation obstruction algebraically, checks that making an allocation tiny increases the budget while the sampling floor is fixed, and checks the exact inverse-information identity noted in the report. The code never turns the old sampling-only budget into a claimed arbitrary-weight diameter guarantee.

## R48-M2: carry input-enclosure error and retain full-box witnesses

**Text:** `round49/enclosures.tex`, `eq:representation`, `eq:outer-radius`, `thm:outer`.

A reference statistical band, its represented interval, and its representation budget are now distinct inputs. Under

\[
I_q\subset I_q^{\rm rat}\subset
[\widehat y_q-R_q-\epsilon_q,\widehat y_q+R_q+\epsilon_q],
\]

the retained full box satisfies the corrected bound

\[
|y_q(\beta)-\widehat y_q|\le R_q+\epsilon_q+2E_q.
\]

The five reported budgets are statistical radius, representation error, tail truncation, coordinate mesh, and Taylor numerical error. Computational refinement does not erase an independent input error. For nonrational data, a certified reference enclosure must be formed and its additional error included; the implementation does not infer such a certification from a floating-point value.

Every retained **full** box has the stated universal completion bound. A projected prefix has an existential witnessing full box, returned alongside it. Arbitrary tails attached to that projection are not asserted to preserve feasibility. The two-witness argument proves the prefix diameter bound on a complete identifying grid.

**Implementation:** `Band` validates the represented interval against its declared rational reference and input-error budget. `OuterResult` exposes the five components and full witness boxes. `radius_budget_satisfied` checks radius arithmetic only; it deliberately does not certify that an arbitrary collection of bands is an identifying grid. The theorem's complete-grid hypothesis is additionally necessary for a coefficient-diameter conclusion. Resource exhaustion raises `ResourceLimit` before enumeration, never an incomplete empty result.

**Regression:** the exact Round 48 witness is retained. Declaring zero representation error for the coarse `[-1,1]` enclosure of `[-10^-7,10^-7]` is rejected. A correctly budgeted coarse enclosure can retain a box but fails a small-radius test; the original narrow rational input returns an empty union. The old inequality `H-E>R+2E` is reproduced exactly, and the corrected effective radius includes the necessary error.

## Stronger posterior region, not just a confidence-set corollary

**Text:** `round49/likelihood.tex`, `thm:variance`, `thm:posterior`, `cor:stage-rates`.

The report correctly distinguished the old `kappa^-1` confidence budget from the `kappa^-2` posterior concentration proof. We now supply a new variance-sensitive posterior proof. For chronological Gaussian score `S_n`, empirical square `A_n`, and group-start conditional square `V_n`, the common event is

\[
|S_n|\le A_n/16+nq/64,\qquad A_n\ge V_n/2-nq/32.
\]

A self-normalized Gaussian exponential martingale controls the score. A conditional exponential chord inequality controls nonnegative group square increments. A deterministic net and interpolation preserve the bounds uniformly. With groups of size at most `m`, the failure term has the explicit form

\[
3\exp\{\overline{\mathcal H}(e_q)-nq/C_m\}+e^{-n},
\qquad C_m=1024\max(1,\sigma^2,mM^2).
\]

The exact integrated nuisance likelihood is bounded with the original summable transient budget. Numerator and prior-ball denominator estimates yield posterior mass at most

\[
\exp\{\mathcal P(\sqrt q/4)-nq/(16\sigma^2)\}
\]

with an explicit transient tail. The proof retains all constants and the correct prior-mass direction. For `m=1`, the unrestricted-feedback posterior regions now become `C_c r+12s<1` for the compact-law `log n/log log n` scale and `C_infty r+8s<1` for the finite-mean law. This is an exact-posterior theorem, not an unsupported transfer from confidence coverage.

## Retained-state bounded-probe logarithmic depth

**Text:** `round49/sampled_generator.tex`, `lem:sampled-log`, `prop:block-certificate`; `round49/blocks.tex`, `lem:block-floor`, `thm:block-posterior`.

Write `Delta=2t_0`, `U=exp(Delta A)`, `X=U-I`, and `H=int_0^{t_0} exp(uA) du`. The selected existing atom ensures `Delta Lambda<=1/64` and `||X||<=1/32`. The delayed response of one short pulse is

\[
b_{k,\beta}=\ell U_\beta^kH_\beta B
=h_\beta(k\Delta+t_0)-h_\beta(k\Delta).
\]

The convergent sampled-generator transform

\[
F_r(x)=\Delta^{-r}[\log(1+x)]^{r-1}
\frac{\log(1+x)}x(\sqrt{1+x}+1)
\]

satisfies `F_r(X)H=A^{r-1}`. Its truncated polynomial in `U` has explicit row-sum and remainder bounds

\[
\mathcal A_{N,R}=8\Delta^{-R}4^N,
\qquad \mathcal E_{N,R}=16\Delta^{-R}8^{-N}.
\]

Combining them with the previously audited `Q^{25(J+1)}` physical-jet inverse produces a finite delayed-pulse separation certificate. The coefficient transform is independent of the unknown parameter and rational at rational sampling times.

Within a block of `m=N+1` short probes, the event that every stage explores and selects the chosen atom has probability `(rho w_0)^m`. The proof pays this **whole-run probability**. On that event the first sign has a lagged linear response at all subsequent endpoints. Block commitment makes the remaining intercept independent of the first sign. Averaging the squared contrast gives a lower bound on the group-start conditional information of the **full unconditioned record**. The unsuccessful blocks contribute nonnegative square contrast and remain in the likelihood.

The resulting information is at least `a^2 kappa_b/m` per readout, with `kappa_b>=exp(-C_b(J+1)) delta^{p_b}`. For logarithmic depth and polynomial accuracy, groups have size `O(log n)`. The variance-sensitive theorem then has effective exponent at least a positive constant times `n^{1-gamma}/(log n)^2` for `gamma=C_b r+p_b s<1`, dominating the `O((log n)^2)` entropy/prior terms. No discarded-data likelihood or terminal-design Gaussian conditioning occurs.

`prop:pulse-confidence` separately gives direct simultaneous pulse bands from successful blocks. It is not substituted for the full-likelihood posterior proof. The signed-pulse option in the rational outer implementation covers the same observables.

## Information comparison and actual scope

`round49/frontier.tex` preserves the two-way propagation and all-history chronological KL proof, and states the necessary joint region separately from sufficient regions. The reset-window `J log J` comparison is not applied to unreset histories. The new positive block construction instead shows why retained history can exceed the one-step compact-law floor even though every individual probe is short.

The result is logarithmic **depth-order** attainability and limitation for the declared bounded-probe clock, with explicit sufficient joint exponent regions. We do not assert equality of leading constants or that the displayed sufficient and necessary joint curves coincide. The new contribution answers one of the report's suggested substantive directions without claiming to solve every clock, controller, or optimal-constant question.

Actual adaptive information and its exploration floor remain separate in `round49/retained_limits.tex`. Stagewise information, not grouped information, is used for the retained Laplace-tracking/LDP statements. The weighted operator consequence remains a product-topology estimate. The original nonlinear homogeneous quasi-BvM, strong filter jets, memory Gaussian image and finite preparation mixture use five unchanged Round 45 source blobs in the retained supplement.

## Literature and navigation

Section 1.1 adds finite-time partially observed system identification and severely ill-posed inversion comparisons. Sarkar–Rakhlin–Dahleh concerns finite latent-order FIR/Hankel and realization errors; labeled infinite Jacobi coefficients are a different target, with stronger structural assumptions here. Agapiou–Stuart–Zhang explains the familiar linear exponential-singular-value/logarithmic-rate mechanism; logarithmic behavior alone is not claimed as novel. Sampled matrix logarithms and aliasing are explicitly compared with Yue–Thunberg–Goncalves. Mikhaylov–Mikhaylov's deterministic lineage remains acknowledged. The Du–Nair–Janson comparison now identifies Corollary 1 as basis-vector/bandit uniformity and distinguishes its anisotropic linear information regime from the stronger nonlinear homogeneous assumptions here.

The root `README.md` and `ROUND49_REVIEW_INDEX.md` identify the active article, supplement, response, source manifest, and actual verification receipt. All historical sources and both controlling reports remain in the full review branch.

## Source-bound verification and submission status

`tools/verify_round49.py` resolves an existing full Git commit SHA, checks ancestry, compares the manifest and every covered regular-file byte against that commit, and requires exact closure of both literal TeX input graphs plus mandatory supporting documents. Separately delivered validation programs must match the SHA256 hashes in that committed manifest; they are not represented as committed program blobs. It runs the regression suite, builds **both** roots in isolated directories with three no-shell-escape passes and recorder-input checks, and checks source hashes again afterward.

The source-capsule commit is a genuine GitHub repository object containing the complete mathematical input and supporting-document closure. The full review-tree commit preserves the historical repository and carries those same covered blobs; the capsule is an ancestor. A local checkout of that exact capsule can execute the full active-source verifier without pretending that every historical file was cloned. Actual commit identities, executed checks, build results, PDF hashes, and publication relationship are recorded in `ROUND49_PUBLICATION.json` and the verifier-generated `ROUND49_VERIFICATION.json`. No remote CI success or mathematical proof-assistant certification is inferred from them.

The regression suite includes exact finite formula tests, both old counterexamples, corrected budget tests, and adversarial Git fixtures. It is subordinate to the written all-depth proofs. This response submits those proofs and implementations for independent review; it does not transform a proof ledger into a journal decision.
