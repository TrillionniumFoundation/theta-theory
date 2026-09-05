# Author response to the Round 46 report

**Revision:** Round 47, September 5, 2026.  
**Main manuscript:** `ROUND47_REVISION.tex`, *Sharp Depth Scales for Adaptive Boundary Identification of Infinite Damped Jacobi Lattices*.  
**Controlling report:** `REFEREE_REPORT_ROUND46_GPT6_PRO_HARSH.md` at `0c2f4c9f10bcf7c9f5a37538d869061e6e0fbfb8`.  
**Preceding source freeze:** `c67f80f34fc128ba3eaece0fd8ad4ea262aa9cd1`; artifact distribution: `00fee70834ee5e2a1fadc55c5d118a23a4637477`.

## Central change

This revision supplies a different mathematical centerpiece, rather than treating the already-repaired Round 45 conclusions as a sufficient answer to the report. There are now two explicit positive experiments and information comparisons identifying their depth orders.

Under the **unchanged fixed-window multiscale law**, oversampling gives

\[
D_\omega(\beta,\gamma)\ge \exp\{-C_c(J+1)\log(e(J+1))\}\delta^{12}
\quad\text{when }d_J(\beta,\gamma)\ge\delta.
\]

The exact no-washout posterior consequently recovers depths
\(J_n=o(\log n/\log\log n)\) at polynomially shrinking coefficient radii. For a fixed positive coefficient separation, the logarithm of the worst-case response separation is of order \(J\log J\), with an explicit two-way propagation comparison.

A **new, separately declared exploration-duration law** gives

\[
D_\nu(\beta,\gamma)\ge e^{-C_\infty(J+1)}\delta^8.
\]

It has unbounded support but finite mean and an exponential moment. With bounded predictable baselines, no reset, and an arbitrary working initial-state prior on the declared ball, it attains \(J_n=\lfloor r\log n\rfloor\) and radius \(n^{-s}\) whenever \(C_\infty r+8s<1/2\). In particular, \(r=1/(8C_\infty)\), \(s=1/64\) are explicit choices. The total elapsed time is linear in the number of observations with an explicit exponential clock tail. This does **not** assert a deterministic maximum duration for each long probe.

An all-time propagation estimate, combined with the chronological Gaussian relative-entropy chain rule, shows that **every** bounded-force adaptive policy has vanishing two-point information at depths \(J_n\gg\log n\). Together with the construction, this identifies the attainable logarithmic depth **order**, not an optimal constant. Coordinatewise posterior medians supply an actual coefficient estimator at the same attainable rates.

## R46-1: replace avoidable condition losses and investigate what remains

**Response.** The report's structural improvements are acknowledged explicitly and proved with complete secant calculations in `round47/inverse.tex`.

The block identity \(A^2+cA=-\operatorname{diag}(\mathsf J,\mathsf J)\) gives the closed response--moment inverse in `eq:closed-moment`. It removes repeated recursive amplification of previously estimated moments. The factorization
\(H_{k-1}^{-1}=\sum_{r<k}\rho_r^{-1}p_rp_r^T\) gives an exponential, rather than quadratic-exponential, Gram bound. The coefficient-ratio estimates include the shallow case \(J=0\). Theorem `thm:jet` obtains

\[
d_J\le Q^{25(J+1)}\max_{r\le4J+8}|\Delta h^{(r)}(0)|.
\]

We do not present this route as independent of the report's suggestion. The new step is to separate the reconstruction jet order \(R\) from the interpolation order \(N\). Lemma `lem:grid` bounds the interpolation amplification by \(8^Nu^{-R}\); Taylor terms above degree \(N\), not above degree \(R\), control the residual. On a fixed physical window this suppresses the residual through extra nodes without shrinking the entire window with the inverse condition number.

Theorem `thm:compact` proves the first displayed bound above with all constants specified in `eq:compact-constants`. The diagnostic cells used are already in the original law: \(K=(N_c-8)/4\), scale \(s=1\), and positive times \(kT/(4N_c)\). No new sampling mass or zero-time observation is inserted. This improves the report's sufficient quadratic-depth exponent as well as the preceding cubic-depth exponent.

Theorem `thm:long` then proves the exponential-depth bound for the new law
\(t_{K,k}=k/(256\Lambda)\), \(\nu_{K,k}=2^{-K-1}/(4K+8)\). Its exact mean is \(13/(512\Lambda)\), and Proposition `prop:clock` gives the elapsed-time bound. The changed support assumption is stated in the abstract, model, theorem, and clock proof.

Both geometries are propagated through the **finite-sample** posterior inequality, rather than a fixed-resolution LDP argument. Corollary `cor:rates`, the explicit budget `eq:sample-budget`, and the improved confidence threshold `eq:diameter` use the same certificates.

## R46-2: make the nearest comparisons precise

**Response.** Section 1.1 compares the relevant claims at theorem level; the bibliography now includes the closest papers identified in the report and banded-matrix decay methodology.

Du, Nair and Janson (NeurIPS 2025, arXiv:2511.06639), Theorem 1, already provide a random-information adaptive linear-regression BvM. Their Corollary 1 also provides policy uniformity under corresponding uniform growth conditions. We therefore do not claim either absence of a deterministic information limit or policy uniformity by itself as new. Their Appendix F discusses obstacles to general parametric extensions. The retained homogeneous theorem uses smooth nonlinear mechanical means and arbitrary working priors on a bounded Hilbert initial-state space, with mechanical contrast and nuisance estimates; it also imposes stronger regularity and contrast. It is not asserted to subsume their linear result. Posterior Gaussian approximation remains distinct from frequentist coverage.

Mikhaylov and Mikhaylov (2019, *Inverse Problems and Imaging*; 2020, *Journal of Mathematical Analysis and Applications*, article 123970, preprint arXiv:1907.11153) already connect boundary dynamics, moments, positive connecting matrices, and finite Jacobi reconstruction. In particular, Theorem 2 and Proposition 10 of the preprint are relevant comparisons. The deterministic response--moment--Jacobi mechanism is treated as background. The present continuous-time damping, noisy chronological experiment, explicit duration allocation, and statistical depth-order comparison are the components requiring separate proofs.

Benzi and Razouk's banded-matrix functional decay work is acknowledged. The elementary two-way Duhamel/path estimate is tailored here to the damped block generator and integrated in time; it is not a claim to invent spatial decay of matrix functions. The roles of Teschl, Vollmer, Shalizi, and Howard and coauthors are retained. This comparison is targeted, not a claim of an exhaustive priority search.

## R46-3: identify a substantive boundary-inference frontier

**Response.** Section 7 supplies explicit comparisons for the two experiments rather than equating a chosen exploration floor with the full information available to a controller.

For a pair differing only in \(b_J\), the first changed step-response derivative occurs at order \(4J+4\). Lemma `lem:two-way` bounds the return response by a factorial tail. Theorem `thm:fixed-frontier`, together with `thm:compact`, yields the \(J\log J\) order for the original fixed-window response metric. Its testing corollary is carefully stated for reset, zero-state, fixed-window experiments; it is **not** transferred to arbitrary no-washout histories.

Theorem `thm:global-frontier` instead integrates the two off-boundary propagators over all time, using short-time path vanishing and long-time common stability. It obtains

\[
\mathrm{KL}(P_\beta^{\pi,n},P_\gamma^{\pi,n})
\le \frac{nU^2\delta^2D_0^4}{2\sigma^2}
 e^{-4\vartheta(2J+1)}
\]

for every parameter-independent bounded-force chronological policy, even with arbitrarily long finite waiting times. The proof compares conditional means on the same realized history and uses cancellation of the action kernels. It does not condition the experiment on its final design. The two-point testing inequality and the positive finite-mean construction give matching logarithmic depth orders. Under a minimum inter-readout time, the same comparison is in physical time.

The bounds leave room for feedback to improve constants or actual predictable information. They do not assert an optimal controller, optimal depth constant, or exact minimax radius. Proposition `prop:ldp` retains the actual \(Q_n\), Laplace tracking, full LDPs on uniformly convergent information subsequences, and the unconditional exploration-floor upper bound. A floor is never substituted for the actual rate function without its required information identity.

The older homogeneous quasi-BvM, strong filter jets, memory Gaussian image, and finite preparation mixture are preserved with unchanged source inputs in `ROUND47_RETAINED_RESULTS.tex`. They are not needed for the new depth proofs. The weighted operator conclusion remains explicitly a weighted/product-topology consequence, not ordinary operator-norm recovery. The washed LDP and polynomial-times-exponential derivative envelopes are retained in Section 6.3.

## Operational request: observations, elapsed time, coverage, and computation

**Response.** Proposition `prop:budget` gives a predetermined finite observation requirement for selected \(J,\delta\), posterior error, and failure probability, retaining the likelihood constants, entropy, prior thickness, and initial-state remainder. Proposition `prop:clock` translates it to elapsed time with the appropriate deterministic or exponential-tail statement.

Theorem `thm:confidence` supplies a single frequentist coverage event for all labels and observation times. Its stopped exponential-supermartingale proof does not claim Gaussianity conditional on an adaptive visit count. The origin is deterministic and is not counted as a measured cell. The improved grid threshold separately certifies shrinking coefficient diameter. Proposition `prop:visits` gives a predetermined visit budget and explicitly distinguishes that budget from data-selected coverage.

Proposition `prop:outer` and `tools/round47_certificates.py` implement a finite rational outer construction: finite-chain truncation, coefficient mesh, rational Taylor response enclosures, band intersection, and projection to the requested coefficients. Separate explicit errors control tail, mesh, and numerical truncation. A retained box is allowed only by conservative interval intersection; every completion satisfies enlarged bands. The algorithm terminates for each prescribed tolerance with unrestricted finite resources. The implementation raises `ResourceLimit` before an excessive search and never reports an incomplete search as an empty confidence set. We do not assert practical or polynomial-time complexity at large depth.

## Verification request: bind the actual source, not a SHA-shaped string

**Response.** `tools/verify_round47.py` requires the full named SHA to resolve to an existing Git commit and to be an ancestor of the checked-out state. It compares the working manifest with the committed manifest, computes the active literal TeX graph for both manuscript roots, requires exact coverage together with mandatory supporting files, and compares each covered regular-file blob and its bytes with that commit. Artifact-only descendants are permitted; covered source changes are rejected.

The build uses a fresh isolated directory containing only verified source inputs, three no-shell-escape TeX passes, and the recorder's local input list. Old auxiliaries and untracked local packages cannot silently enter this build. Undefined references and overfull boxes are build failures. The manifest binds the supplement's five unchanged historical input blobs as well as the new main manuscript.

The standard-library regression suite has 34 tests, including exact finite moment/Gram/reconstruction/path identities, both grid certificates, law masses and means, outer enclosures, and adversarial source-binding fixtures. The negative fixtures include a nonexistent 40-character SHA, an omitted input, a false manifest, changed source bytes, a missing local package, and undeclared recorded TeX inputs. An artifact-only descendant is a positive fixture. These tests are subordinate to the analytic all-depth proofs.

Actual executions and their scope are recorded in the artifact-only `ROUND47_PUBLICATION.json` and local validation receipt. A local main-manuscript build is not represented as a successful remote CI run or as a build of the retained supplement. The verifier writes `ROUND47_VERIFICATION.json` only from its own execution; no passing verifier receipt is manufactured. The source freeze and publication receipt are separate commits.

## Submission status

Every named Round 46 request is mapped above to a written proof, explicit operational construction, comparison, or source-integrity change in this revision. Those are the claims submitted for independent scrutiny. Finite tests are not formal proof certification; neither a proof ledger nor this response establishes editorial acceptance. The report itself is an AI-generated referee-style assessment, not a journal decision.
