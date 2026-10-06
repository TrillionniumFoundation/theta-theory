# Response to the latest substantive referee: A2-DYN revision 19

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active manuscript:** `papers/A2-DYN-v19-referee-response`  
**Controlling report:** `reviews/a2-dyn-v16-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Review commit / blob:** `b0b7ddfcd90f493e02254742b33174e9108fc5a7` / `805f04cd60d144bc6321ce3f4304ebe1cda34999`  
**Immediate ordinary paper baseline:** v18 subtree `e19803bed418d2a1402781124f91737c136b595b`  
**Frozen baseline commit on this revision branch:** `68618cdaad6824912b49b505d58c9a9fcb0ab823`  
**Date:** 6 October 2026

We thank the referee for separating the function-defect theorem from operator powers, raw density derivatives and exact conditioning. We also take account of the v17 and v18 derivations already in the repository. Revision 17 supplies the exact arbitrary-return-phase lift and a local finite-rank reconstruction/resolvent theorem; revision 18 supplies the complete finite-count raw extraction and the corrected count-localized inversion identity. Neither is presented here as having a separately located referee report.

The principal additions in this revision are an exponential finite-record variation theorem, an improved single-logarithm joint return defect, and central Gaussian and actual moment estimates under multiple observations in a logarithmically growing actual-return window. All are stated as Theorem J and proved in two complete sections. The title, physical family, actual section, four-coordinate record and raw mixed-density objective are unchanged. All 41 inherited core modules remain byte-identical; the new argument does not replace the original single-mark theorem by a weaker one.

## A. Operator realization, reconstruction and peripheral phases

### A.1. Sharpen the actual finite geometry rather than assume a new regularity theorem

The finite polynomial collision graph in `lem:finite-record-variation` has both `k=O(L)` variables and `s=O(L)` sign tests, with a fixed degree and exponentially many label alternatives. The exact BPR finite bound used there is

`d(2d-1)^(k-1) sum_{j=0}^k binom(s,j)4^j`.

Keeping its binomial form gives a bound by `d(2d-1)^(k-1)5^s`, hence `C exp(C L)`. The earlier `exp(C L log L)` estimate was valid but unnecessarily coarse. `lem:linear-sign-complexity` states the finite bound, including Boolean unions and projections. `thm:exponential-finite-record` checks that the actual first-admissible-flight and exact membership graph meets it and carries the bound through slice coarea. No arbitrary long pullback is declared BV without this argument.

This refinement is uniform in the real coefficients, hence in the radius and moving section rectangles. It uses the finite equation (3.3) of the existing BPR reference, not its fixed-dimension asymptotic theorem. The primary source and the distinction are recorded in `EXPONENTIAL_WINDOW_INPUT_MAP.md`.

### A.2. The return spectral estimate loses only one logarithm

`prop:exponential-tower-regularization` retains the exact v17 lift for every return phase, with the same height-weighted norm and unweighted-top defect identities. The approximation error remains `C[L epsilon V_f+M_f exp(-cL)]`, but its variation budget becomes `C M_f exp(C L)(1+epsilon^(-1)+|z|)`.

Consequently, with `rho^2=|z|^2+xi^2` and `Lambda=1+log(H/rho)`, `thm:single-log-return-defect` proves

`||E_{R,z,xi} q||_1 >= b rho^2`,

`||E_{R,z,xi} f||_2 >= b rho^2/Lambda`

under `0<rho<=rho_0` and `rho^2 Lambda<=a`. The complex function is L2-normalized and may vanish. The proof includes the pure spectral direction and the shifted-frequency cancellation line by comparability of the full joint frequency, not division by the shifted spatial part.

The regular approximation accuracy is fixed before the smallness constants. For complex functions it is `epsilon_0 rho^2/Lambda`; the logarithm of its resulting regularity budget is at most `C(1+|log epsilon_0|)Lambda`. The absorption is valid because `epsilon_0(1+|log epsilon_0|)` tends to zero. This makes the improvement quantitative and noncircular.

For polynomial reconstruction budgets, the physical annulus remains `2n^(-99/200)<=|z|<=n^(-2/5)` and its rescaling remains `2n^(1/200)<=|sqrt(n)z|<=n^(1/10)`. The local return-spectral range now includes `|xi|<=a_0/sqrt(log n)`, and the complex lower bound has denominator `log n` rather than `log n log log n`.

### A.3. Precise compressed consequences, not an unproved uncompressed theorem

The existing fitted-grid reconstruction has budget `H_h=C/h`. The exact orthogonal residual identity bounds the physical defect squared by three times the normalized compressed residual. `cor:single-log-compressed` therefore gives

`||(exp(i xi)-A_{R,h,z})^(-1)|| <= C Lambda_h^2/rho^4`

on the stated joint region, and a quantitatively specified neighboring resolvent disk. This is a smallest-singular-value argument, not an eigenvalue-only bound for a non-normal matrix.

`prop:exponential-compression-consistency` independently improves the finite-time consistency budget to

`C n[exp((a_t n-c_t L)/2)+sqrt(h(1+|z|)exp(C L))]`.

The matrix entries and the compared characteristic function remain those of the full actual return record. Its Fourier sign is displayed explicitly. These estimates sharpen the existing reconstruction route, but we do not infer mesh-uniform uncompressed powers, or full-circle peripheral control, from the local resolvent alone. The required common mesh/time choice and remaining spectral arcs are still named in the paper.

## B. The complete complementary-frequency integral

The revision improves the quantitative input on the annulus and the approximation budget feeding the operator comparison. It does not rename a defect or compressed-resolvent estimate as an integrated Fourier tail. A radius-uniform growing-budget estimate on the remaining compact bands, high roof-frequency control and an appropriate contour-to-power argument remain necessary for the complete complementary integral.

For the enlarged window-weight class below, the paper supplies a proved central integral and then displays exactly where the weighted complementary residual must enter the raw identity. This is additional progress in the conditioning application rather than an assertion that the unweighted complement has disappeared.

## C. Raw critical/singular extraction and derivative sums

The full finite-count constructible extraction of v18, all one-sided Puiseux-log terms of exponent at most one, trace cancellation and the finite W2,1 residual sum remain unchanged. The new finite graph estimate concerns first derivatives in initial collision coordinates. It is not a bound for inverse Jacobians, local raw-density edge coefficients, or the uniform long-time sum of second derivatives.

In particular the actual finite extraction constants and their n/radius growth remain separate from `C exp(C L)`. The paper does not use compactness to suppress collisions of singular values or vanishing cutoff widths. The count-localized inversion retains its high-count low-frequency convolution correction. No singular branch or edge contribution is deleted.

## D. A new multiple-time conditioning theorem with the original event

### D.1. Approximate the whole window, not its individual variation budget

Let `W_R(y)=prod_j u_j((F_R^*)^(ell_j)y)` with `0<=ell_1<...<ell_q<=m`, each factor bounded by one and with BV zero extension. This product need not have a usable BV norm. `lem:window-weight-approximation` smooths each initial-coordinate factor and then restricts to the proof event `N_m<=L`.

Invariance of the actual first-return map, before imposing that restriction, bounds the smoothing error by `C epsilon sum_j V_j`. The actual cumulative-return tail controls the excluded part. Resolving the first L binary membership symbols fixes the collision indices of all observations on each word. Exponential finite-record variation then gives

`||W-W_{L,epsilon}||_1 <= C[epsilon V+exp(a_t m-c_t L)]`,

`||W_{L,epsilon}||_infinity<=1`,

`||(W_{L,epsilon})^0||_BV <= C(1+q/epsilon)exp(C_w L)`.

Word jumps and the section trace are included. No independence or mixing of the induced returns is used.

### D.2. Central integral with four explicit margins

The original marked spectral proof is retained at smoothing scale `n^(-1/14)`. On a chosen rescaled subband `|v|<=2n^theta`, `0<=theta<=1/200`, it yields margins `s_0=1/28-5theta` and `s_1=1/14-4theta`. At `theta=1/200` these are exactly the original `3/280` and `9/175`.

Apply this estimate to the whole-window approximation at its actual start return, then remove the approximation and its mass in the original measure. Theorem `thm:window-central-integral` proves an error bounded by

`C[n^(-s_0)sqrt(log n)+(1+q/epsilon)exp(C_w L)n^(-s_1)+n^(4theta)(epsilon V+exp(a_t m-c_t L))]`.

For `m<=a log n`, `L=ceil(b log n)`, `epsilon=n^(-d)/4`, `V<=C n^kappa(log n)^r`, the four margins are

`1/28-5theta`, `1/14-4theta-C_w b-d`, `d-kappa-4theta`, `c_t b-a_t a-4theta`.

The paper gives an explicit strictly nonempty choice for every positive complexity and tail constants, without assuming an unproved favorable ratio between them. For example take `d=1/56`, `b=1/(56 C_w)`, `a=min(b/2,c_t b/(4a_t))`, `theta=min(1/448,c_t b/32)` and `beta=min(1/448,c_t b/16)`, with `kappa=0`. Every margin is strictly greater than beta. This permits logarithmically many observations of uniformly bounded individual variation.

### D.3. Exact rare event and actual moments

For indicator factors the final event is precisely

`A_{n,k,R}=intersection_j {x:(F_R^*)^(k+ell_j)x in E_j}`.

Its probability is independent of the start return k by invariance, but is not asserted to factor into the individual masses. If it is at least `p_0 n^(-beta)`, with beta below all the margins, division by that unchanged probability proves the conditional integrated central Gaussian comparison. The proof cutoff `N_m<=L` is absent from the final event.

`thm:window-weighted-moments` combines the original marked moment theorem with the actual fourth-moment bound. The weight replacement costs the square root of its L1 error, by Cauchy--Schwarz; this is displayed rather than omitted. It yields convergence of the conditional normalized mean and covariance under separate explicit margins, and the exhibited choice satisfies these as well.

This extends the single-return-state class to multiple actual observations within a growing window, including a terminal window. The auxiliary positive central exponent may be smaller; the original Theorem C and its `n^(1/200)` band remain unchanged for their original class. We do not extend the new result to arbitrarily separated full paths without a proof.

### D.4. Weighted raw identity and exact physical observations

When the factors additionally meet the v18 finite-record subanalytic weight hypothesis, the exact finite extraction applies to this same original multiple-time weight. The new section writes its raw identity, including the high-count convolution term, with physical cutoff `2n^(-1/2+theta)` and rescaled cutoff `2n^theta`. On central count labels a linear count cutoff makes the high-count convolution smaller than any fixed power after normalization, by support separation and the Schwartz proof kernel.

The new central integral supplies the first term. The weighted local edge correction, complementary residual integral and actual long-time derivative sum remain explicit. A BV observation is not automatically subanalytic. An event defined by a different exact physical-time or final lattice observation is not silently replaced by this return-window event; its relative event comparison remains an additional task. Thus this is a substantive same-event extension, not a claim of a completed conditional raw LLT.

## E. Independent checking and presentation comments 1--14

The new proofs reuse the precise collision graph, tower identities, joint collision estimates and actual moment theorems. The only external inequality used for the sharpening is already present in the bibliography and is cited at its finite equation. Independent human specialist review has not been obtained by this author revision.

The inherited v17 clarification beside Theorem G and the separate variables `z`, `sigma`, `xi`, `lambda` remain. The exact lift for all return phases is distinguished from the local quantitative bound. Both frequency scales, the height/top normalizations, the shifted cancellation line, modulus control, the exact physical cover and the finite sign-condition input remain explicit. The fixed-radius/fixed-budget compactness distinction is not erased. First initial-coordinate variation, raw second derivatives, finite compressed resolvents and uncompressed powers continue to be distinguished. The new weighted identity specifies which central terms are proved and which raw terms require further bounds.

The exact inherited-edit ledger is retained, and all original modules, labels, scripts and bibliography entries remain. Publication metadata continues to mean author revision for further review, not journal acceptance, independent human review or formal proof certification.

## F. Source chronology and qualification

At the beginning of this task the v18 refs still named an assembly staging commit, but the immutable ordinary paper subtree had already been created. We pinned that exact tree on a new v19 branch and verified its archived bytes before revising. The original v18 and review refs were not moved. This response does not invent a prior final v18 qualification or a v17/v18 referee report.

The new article consists of ordinary committed source, not source generated by qualification. The verifier checks the frozen v18 subtree, all inherited file hashes, all 43 core inclusions and the five exact introduction edits. Normal/optimized finite diagnostics and the original mechanical checks run before the complete native article build. The dynamic receipt is bound to the actual event SHA and run ID. Static prose does not predeclare a future workflow successful.

The revision is offered for substantive review of the new exponential reconstruction and multiple-observation proofs within the original raw mixed-density program.
