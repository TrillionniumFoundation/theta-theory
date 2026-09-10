# Independent referee report on A2 v10

**Manuscript:** Qian Qi, *Relative boundary laws and inverse experiments in dispersing billiards*.

**Date:** 10 September 2026. **Requested standard:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the American Mathematical Society.

**Status of this document:** independent AI-assisted referee-style assessment requested by the author. This is not a journal-commissioned report, an editorial decision, or a formal proof certificate.

## 1. Source identity and recommendation

This report concerns the completed revision on `revision/a2-v10-observable-boundary-profiles-2026-09-10`, frozen at commit `f46dca20f3d1b73077522bb2041f463af033cb70`. The manuscript directory is `papers/A2-v10-observable-boundary-profiles`; its native Git tree is `452a9003b03ff8f6eed47e1f609a36a054271455`. The author commit has parent `b756f4851669e34c7074ba61b5bcf48689756406`, the completed-v9 review, whose reviewed author source was `33ef794a398b23015651482e93be7667c08d6fad`.

The parallel v9 initialization at `12a3f50e143cc4951d8e9bea888206d965b90e51` is not the source under review. An objection that v10 merely republishes that initialization would be factually wrong. A live recheck of the A2 revision refs still identified v10 at the frozen commit before publication of this report.

**Recommendation: reject at the requested four-journal level in its present form.** This is a judgment about the strength and organization of the contribution offered at that level, not a claim that the new acquisition theorem is false. I found no fatal mathematical error in the new theorem or in the central dependency chain examined below. The revision is a genuine, technically coherent improvement, and several previous objections must now be closed.

The most important positive change is that the full-profile inverse no longer stops at a differentiated-data oracle. Theorem 11.1 constructs a Borel estimator from finitely many charged binary preparations, and Corollary 11.2 gives a valid sufficient preparation bound. The regularization, endpoint treatment, variance scaling, and separation of structured bridge bias from unstructured scalar noise survive scrutiny. Calling the new section merely a restatement of deterministic inversion would be unfair.

Nevertheless, the statistical addition is principally a carefully executed reduction from an already available relative physical law and a deterministic inverse. It does not establish a sharp information limit, a new general inversion mechanism, or recovery of unrestricted asymmetric geometry. None of those stronger assertions is falsely made in the manuscript. Their absence matters to my assessment of the significance achieved by this particular addition, not to its correctness. The exceptional-contribution case must therefore rest chiefly on the nonlinear physical boundary law and its invariant, rather than on the size of the preparation exponent or the number of subsidiary results. That case remains unconvincing to me at the requested level.

This negative recommendation is not a demand to abandon the program, remove valid generality, or manufacture a stronger theorem. An editor could reasonably weigh the physical invariant differently. No claim is made that a published theorem already subsumes the complete billiard result.

## 2. What changed, and disposition of the previous comments

I compared the completed-v9 source with the authenticated v10 source. The new TeX inputs are `article/22_deautoconvolution.tex`, `article/25_profile_acquisition.tex`, and `article/72_observable_comparison.tex`. The modified TeX files are `main.tex`, `article/01_introduction.tex`, `article/20_boundary_compatibility.tex`, and `v5/references.tex`. Expanding the active input chains gives 168 statement/proof environments in completed v9 and 176 in v10. All 168 previous environments are retained verbatim. This is a source-retention fact, not verification of 168 proofs.

| Previous request | Disposition in this review |
| --- | --- |
| E1: give an operational meaning to full-profile recovery, accounting for rare-event observation | **Closed as a mathematical acquisition objection.** Theorem 11.1 genuinely supplies finite observations and charges failures. The separate editorial question of top-four importance remains open; it must not be relabelled as a missing estimator. |
| E2: compare with the closest deautoconvolution literature and specify the functional setting | **Closed for the requested comparison.** Section 10 correctly separates causal autoconvolution regularization, the real `L^2` support framework, and the present normalized `x^{-1/2}V(x)` kernel. This is not an exhaustive priority search. |
| E3: separate exact-family inversion, smooth-nuisance experiments, and full-profile observations | **Closed.** The introduction's dependency table and Section 11 explicitly state the supplied calibration, labels, smoothness bounds, target, and observation. Lower bounds from the other experiments are not transferred to full-profile recovery. |
| E4: distinguish even-law reconstruction from odd-law validation and improve organization | **Substantively closed.** The even laws reconstruct; separately observed odd laws validate compatibility. The three-part organization and table help. A small wording refinement is identified below, not a renewed structural objection. |

In particular, the previous report's objection that derivative observations were supplied without a raw-data acquisition theorem is no longer available. Nor is it appropriate to criticize the finite dictionary as though its lack of a running-time bound made it nonmeasurable: the manuscript explicitly distinguishes statistical existence from computational complexity.

## 3. Correctness audit of the new finite-preparation theorem

References in this section are to the frozen source; the main new file is `article/25_profile_acquisition.tex`, lines 1–324. Theorem 11.1 and Corollary 11.2 appear on manuscript page 30; their proof is on pages 32–33.

### 3.1 The observation and the class are stated honestly

Lines 10–45 supply the gap `g`, free area `A`, multiplier parameter `gamma`, patch labels, and common regularity/relative-convergence bounds. Each observation is a selected-event bit from an independent physical preparation. The experiment is not the unlabelled four-window model.

The class consists of normalized positive `C^{m-1,1}` profiles with a **sum** norm bound, for `m >= 4`. The larger class is used for regularization; arbitrary candidates are not declared realizable by billiards. This is legitimate for an upper bound. A lower bound over that larger class would require a different argument before being called a physical billiard lower bound.

### 3.2 Compactness and the finite dictionary do not hide an oracle

The `C^{m-1,1}` ball is compact in `C^{m-1}` on the fixed collar: the highest retained derivative is equicontinuous, and the lower derivatives inherit the required uniform control. The normalization, positivity, and sum bound survive the limit. The forward simplex integral maps this class into a uniformly bounded `C^{m-1,1}` class by differentiation and the product rule under its integrable fixed-domain weight.

For fixed grid size, the interpolated forward map has a compact finite-dimensional image. An ordered finite net therefore exists. Minimizing over it with a fixed first-minimizer tie rule is Borel measurable. The net may be prohibitively large or nonconstructively specified; that does not invalidate a sample-count theorem that expressly excludes computation cost. No exact unknown profile enters its definition.

### 3.3 The first-cell extrapolation is valid

Lemma 11.3 uses only positive nodes. On the first cell the nodes are `h,2h,...,mh`; no noiseless value at zero is smuggled in. The number of possible rescaled stencil configurations is finite. Taylor's formula with a Lipschitz highest derivative gives approximation error `O(h^{m-3})` in the broken `C^3` norm. Polynomial reproduction and scaling give the `h^{-3}` amplification for arbitrary nodal errors.

The separate stability bound `||I_h f||_{3,h} <= C ||f||_{C^3}` is essential. It follows by subtracting the quadratic Taylor polynomial and bounding the residual before differentiating the interpolation polynomial. It applies to the smooth bridge error as a function, not merely to its nodal maximum.

### 3.4 The deterministic inverse applies to the chosen regularization class

The extension from smooth physical profiles to `C^{m-1,1}` candidates needs justification; the proof supplies it rather than assuming it. For two candidates, put

$$f(x)=x^{-1/2}(V(x)-W(x)),\qquad a(x)=x^{-1/2}(V(x)+W(x)).$$

Normalization makes `f` continuous at zero. With `k_*(x)=x^{-1/2}` and `Q=(pi/2)(d^2[T(V,V)-T(W,W)])''`, the identities are

$$k_* * a=2\pi+R,\quad R(0)=0,\quad \|R'\|_\infty\le\pi B,$$
$$2\pi f+R'*f=k_* *Q'.$$

The factor `2 pi`, the derivative of the constant convolution, and the condition `Q(0)=0` are all correct. Gronwall then yields the stated inverse. Neither Fourier continuation nor equality of infinitely many Taylor coefficients replaces full-collar uniqueness.

### 3.5 The noise allocation and rare-event charge are correct

Write `a=a_j(d)` and `Z=a` times the empirical success proportion. Direct calculation gives

$$\operatorname{Var}(Z)=\frac{aF_j(d)(1-p_j(d))}{N}.$$

The dependence is linear in `a`, not quadratic after using the small success probability. The Bernoulli exponential-moment argument gives

$$\Pr\{|Z-F_j(d)|>t\}\le 2\exp\left[-\frac{Nt^2}{2a(M+t/3)}\right].$$

There are `2L` sampled means. The factor `log(4L/eta)` and the allocation in (11.4) therefore suffice. Summing `d_k^{-2}=h^{-2}k^{-2}` gives an `h^{-2}` cost, rather than an additional factor `L` multiplying the worst-node bound. The ceilings contribute at most `2L`. This is a genuine deterministic all-preparation count, including failures.

### 3.6 There is no missing `h^{-3}` on the bridge bias

On the simultaneous concentration event, the interpolation estimates give

$$\|I_hZ-I_hF\|_{3,h}\le C(th^{-3}+C_0\tau^j).$$

Replacing this by `C h^{-3}(t+tau^j)` would unnecessarily discard the supplied `C^3` control. The minimum-discrepancy step, the dictionary approximation, and interpolation of the true and estimated forward profiles give

$$\|\widehat V-V\|_\infty\le C(h^{m-3}+\tau^j+th^{-3}+\delta).$$

Although the interpolants need not match derivatives across cell boundaries, the two forward laws being compared are globally `C^3`; the broken norm bounds their derivatives on every cell. The proof does not differentiate a discontinuous piecewise polynomial as a distribution.

### 3.7 The preparation exponent follows from the displayed choices

Take `h` comparable to `epsilon^{1/(m-3)}`, `t=c epsilon h^3`, and dictionary tolerance `c epsilon`. Choose the least admissible even `j` with `tau^j <= c epsilon`. Rounding changes `j` by less than two once the lower bound `j >= 2` is inactive. Consequently

$$h^{-2}t^{-2}\asymp\varepsilon^{-2}h^{-8},\qquad
 e^{j\gamma}\le C\varepsilon^{-\gamma/|\log\tau|}.$$

This gives exactly the stated exponent `2+8/(m-3)+gamma/|log tau|`, with the stated logarithmic confidence factor. The odd-law prediction estimate follows from the mass-one positive bilinear kernel. I find no arithmetic or logical defect in these steps. The bound is sufficient, as the author says, not a minimax conclusion.

## 4. The physical input has not been replaced by generic inverse-problem algebra

The central dependency chain was examined afresh, not accepted solely because an earlier report passed it. In `v3/10_geometry_action.tex`, shortest-channel localization uses positive separation, uniqueness of the convex closest chord, and a minimum roof. It does not require an upper roof bound. The alternating recurrence and its Green kernel have the correct unequal-curvature scaling.

The relative twist is handled by the cofactor identity

$$-W_{uv}=\frac{\prod_i(-\ell_{i,uv})}{\det H_{\mathrm{int}}},$$

followed by normalization before taking a limit. Endpoint localization makes the tridiagonal perturbation summable in trace norm. The determinant argument is not an absolute error estimate divided by an exponentially small reference twist.

In `v4/10_boundary_layers.tex`, the half-line gluing and two-block determinant comparison control the nonlinear perturbations, remote-boundary reflections, and mixed derivatives. The fixed exponential margin absorbs polynomial factors at each fixed derivative order. `v5/15_differentiated_operators.tex` correctly requires bounded differentiated trace norms, not small differentiated operators.

The full-phase normalization and residual-time integration in `v3/20_integration.tex` retain the factor `1/(2 pi A)`. The constructive Morse change of variables fixes the sublevel domain before taking offset derivatives. This is what makes the normalized law smooth down to zero on a collar independent of flight number. Theorem 9.1 then produces the weighted, symmetrized energy profile; Theorem 9.2 gives its actual full-function inverse.

These are the genuinely physical parts of the contribution. The periodic Hill formula in Bolotin–Treschev [P1] supplies relevant determinant context, but its periodic Hessian is not the Dirichlet boundary problem here, and it does not by itself prove the nonlinear normalized physical probability limit. An originality assessment must respect that distinction.

I also checked the separation of assumptions in the exact four-window inverse and the smooth-envelope minimax argument, including the envelope's strict sum-norm slack and the support-compatible direction of the timing entropy comparison. This is not a fresh line-by-line certification of every inherited appendix, companion proof, or document in the eleven-paper program. The complete v10 acquisition proof and its central geometric/profile dependencies received the deepest examination.

## 5. New mathematical benchmarks supplied by this review

The following calculations are independent of the author's finite verification scripts. They clarify what the new theorem does and does not establish. They concern the abstract profile operator unless explicitly stated otherwise.

### 5.1 Exact linearization: a half-order distinction hidden by the integer norm

Let `F(V)=T(V,V)`. Bilinearity and integration in the unperturbed variable give

$$D F_1[w](d)=\frac{16}{3\pi d^2}\int_0^d x^{-1/2}(d-x)^{3/2}w(x)\,dx.$$

For `w(x)=x^n`, this is `lambda_n d^n`, where the simplex moment formula gives

$$\lambda_n=\frac{4(1/2)_n}{(n+2)!}
=\frac{4\binom{2n}{n}}{4^n(n+1)(n+2)}
\sim\frac4{\sqrt\pi}n^{-5/2}.$$

This exact polynomial benchmark does not support calling three derivatives the intrinsic sharp smoothing order. It does explain why the integer `C^3` estimate loses quantitative information relative to a more finely resolved inverse norm. No optimal statistical rate follows from this linearization alone.

### 5.2 A `C^2`-to-`C^0` Lipschitz inverse is impossible on a fixed nontrivial abstract class

Set `D=1`, fix `m >= 4`, `B>1`, and `beta<1`. Choose a sufficiently small constant `a>0`, independent of `n`, and for `n >= m` put

$$V_n^{\pm}(x)=1\pm a n^{-m}x^n.$$

Both signs belong to the same class `K_m(B,beta;1)`: each derivative through order `m` is bounded by `a n^{r-m}`, and choosing `a(m+1)<B-1` and `a<1-beta` suffices for the sum norm and positivity. The `m`th derivative bounds the Lipschitz constant of the `(m-1)`st derivative.

Because the quadratic perturbation terms cancel between the two signs,

$$F(V_n^+)-F(V_n^-)=2a n^{-m}\lambda_n d^n.$$

Using the maximum convention for the `C^2` norm, for `n >= 4` one gets exactly

$$\frac{\|V_n^+-V_n^-\|_\infty}
{\|F(V_n^+)-F(V_n^-)\|_{C^2}}
=\frac1{\lambda_n n(n-1)}\asymp n^{1/2}\longrightarrow\infty.$$

The sum convention changes only a bounded asymptotic factor. Thus the author's `C^3` estimate cannot simply be improved to `C^2` Lipschitz stability on that whole fixed class. This is stronger than the previous review's failure of a `C^0` Lipschitz inverse. It supports the need for differentiated information while still leaving a fractional-order question between the integer norms.

These are not realized billiard alternatives. They establish neither physical geometric nonuniqueness nor a minimax preparation lower bound for the labelled finite-bridge experiment. At the endpoint choices `B=1` or `beta=1`, this two-sided construction is not asserted.

### 5.3 A sharper mixed-norm deterministic bound

The same forced Volterra equation gives a refinement without new geometric assumptions. Let `Q(0)=0`, `M_0=||Q||_infinity`, and `M_1=||Q'||_infinity`. If either norm vanishes, the result is immediate. Otherwise split the Abel integral at distance `ell=M_0/M_1` from its upper endpoint. Since `Q(0)=0`, `ell <= D`.

For `x <= ell`, direct integration gives `|k_* *Q'(x)| <= 2M_1 sqrt(x)`. For `x>ell`, integrate by parts on `[0,x-ell]` and estimate directly on the remaining interval. The two bounds are `2M_0/sqrt(ell)` and `2M_1 sqrt(ell)`. Hence

$$\|k_* *Q'\|_\infty\le4\sqrt{M_0M_1}.$$

Applying the same Gronwall step as in the manuscript gives the valid refinement

$$\|V-W\|_\infty\le
\frac{2\sqrt D}{\pi}e^{BD/2}
\sqrt{\|Q\|_\infty\|Q'\|_\infty}
\le C_{B,D}\sqrt{\|F(V)-F(W)\|_{C^2}
                         \|F(V)-F(W)\|_{C^3}}.$$

For the monomial alternatives above, the product of the second- and third-derivative scales has precisely the compensating `n^{5/2}` factor. This is a concrete norm benchmark, not a proof that a particular fractional Hölder endpoint space is optimal.

In particular, one cannot insert this inequality into Corollary 11.2 and announce an improved preparation exponent without redesigning and analyzing the discrepancy criterion and the separate approximation, noise, and bridge-bias terms. I do not make that leap. The calculation identifies a real place where a sharper quantitative acquisition theory could begin.

### 5.4 Calibration cannot be imported for free from the exact-family experiment

The supplied calibration in Section 11 is an actual information assumption. To see its sensitivity exactly, suppose the design uses `g+Delta g`, `A_hat`, and `gamma_hat`. The programmed window is `j(g+Delta g)+d`; its true offset is `z=d+j Delta g`. Whenever `z` lies in the physical collar, the normalized mean used by that design is

$$\frac{\widehat A}{A}
\frac{\sinh(j\widehat\gamma)}{\sinh(j\gamma)}
\left(1+\frac{j\Delta g}{d}\right)^2F_{j,b}(d+j\Delta g).$$

Setting `F_{j,b}=1` only to isolate the normalization factors, without asserting an exact nonlinear billiard realization, gives first-order gap sensitivity `2j Delta g/d` and multiplier sensitivity `j coth(j gamma) Delta gamma`. At the smallest grid offset, a direct sufficient way of keeping this additional normalized-mean error below the scalar tolerance `t` is

$$|\widehat A/A-1|\lesssim t,\qquad
|\widehat\gamma-\gamma|\lesssim t/j,\qquad
|\Delta g|\lesssim th/j,$$

with appropriately small constants and positive offsets retained. Under the theorem's choices, the last requirement is of order `epsilon h^4/j`. These are conservative sufficient tolerances for this plug-in implementation, not necessary rates for every joint estimator.

The exact four-window theorem estimates parameters in a different, specified analytic family. It does not establish these tolerances, or their charged cost, uniformly over the general full-profile class. The present manuscript correctly does not claim otherwise. Any future claim of calibration-free full-profile recovery would need an actual theorem addressing this issue.

### 5.5 The displayed exponent depends on a certificate, not just on a billiard

If the supplied estimate holds with `tau`, it also holds with any larger `tau_tilde<1`, with the same constant. Yet `gamma/|log tau_tilde|` can become arbitrarily large as `tau_tilde` approaches one. Thus Corollary 11.2 expresses the cost of a construction using a supplied convergence certificate. Its exponent is not, without further work, an invariant measure of the difficulty of recovering the physical boundary profile. This is fully consistent with the author's sufficient-bound wording, but important when assessing the headline contribution.

## 6. Remaining objections at the requested publication level

**R1 — The significance case remains the principal obstacle.** Section 11 completes a previously missing operational link, but once one supplies the physical relative estimate, the proof proceeds through compactness, positive-node polynomial reconstruction, a second-kind Volterra inverse, and Bernoulli concentration. The author now acknowledges the classical status of these ingredients. The paper should therefore make its strongest case around the new physical law and the information carried by its nonlinear invariant, not around general recovery machinery or a conservative exponent. The existing nonlinear realizations are relevant positive evidence; they do not by themselves identify the full physical image of the profile map or establish an optimal observation theory. Those latter results are possible directions, not assertions that the current theorems need them to be valid.

**R2 — Quantitative sharpness is not established by the present cost accounting.** The exact calculations in Section 5 show both that `C^2` Lipschitz stability fails on a nontrivial abstract class and that the `C^3` argument has a finer mixed-norm structure. This is a more informative benchmark than simply calling the loss three derivatives. The current paper correctly avoids claiming optimality. To elevate the sampling result itself into the main exceptional contribution would require substantially more understanding of information loss, design, or physically realizable alternatives. A matching lower bound is not mandatory for every useful theorem, but its absence cannot be filled by borrowing the unrelated envelope bound.

**R3 — The statistical target must remain the calibrated energy invariant.** The abstract, the table, and Section 11 largely get this right. Recovery of both full symmetrized profiles is meaningful and should not be dismissed as finite-jet recovery. It is also not arbitrary asymmetric contact-graph recovery, unlabelled recovery, or calibration-free recovery. Section 5.4 quantifies one reason the distinction is substantial. Keeping these qualifications is not a retreat; it is the correct theorem.

**R4 — The result hierarchy is improved but still diffuse.** The 97-page article contains a general relative law, full-profile inversion and acquisition, endpoint testing, exact-family root recovery, nuisance minimax theory, and numerous retained applications. Length alone is not an objection. The difficulty is that several mathematically distinct achievements compete for the central narrative, while the new operational theorem depends on a much narrower chain. A focused theorem-level account of what is physically new, what is an observation consequence, and what belongs to a separate benchmark would help more than another layer of general-purpose lemmas. No deletion of valid proofs or arbitrary weakening of scope is requested.

These are not four newly discovered fatal gaps. R1 is the reason for the venue recommendation; R2–R4 explain why the successful response to the earlier technical requests does not, in my judgment, settle that editorial question. The revision should receive full credit for having addressed those requests.

## 7. Specific presentational and literature comments

The introduction says that the odd subsequence carries an “independent compatibility constraint.” Since the same-type laws determine the mixed law, replace this with wording such as “separately observed odd records test the compatibility predicted by the two even laws.” This avoids confusing independent observation with independent identifying information. The detailed statements already have the correct meaning.

Make the positive-node extrapolation and the distinction between smooth bridge bias and arbitrary scalar noise as visible in the theorem's explanation as they are in the proof. They are the two places where a skeptical reader is most likely to suspect a hidden oracle or a missing factor. They are not errors to repair.

The deautoconvolution comparison is materially improved. Dai–Lamm [P2] establish causal local regularization, with convergence and rates for continuous and `L^2` data. I checked the publisher's abstract and bibliographic record, not an inaccessible full proof, and do not assert a detailed theorem-level reduction. Hofmann–Werner–Deng [P3] formulate real `L^2` full/limited-data problems and limited-data nonnegative uniqueness with support at the origin. Their square-integrable setting differs from the present kernel, whose square behaves as `1/x` near zero. This is a genuine functional distinction, not by itself a claim of a new general inversion principle.

No exhaustive novelty clearance has been performed. The exact combination of nonlinear billiard localization, relative flux, finite-collar inversion, and calibrated finite-preparation observation has not been shown here to be contained in one earlier result. Equally, a short targeted comparison cannot establish its historical priority over all related literature.

## 8. Reproducibility and limits of verification

The local packet was not trusted by filename. Every one of its 104 native files was rehashed as a Git blob, and its directory tree was reconstructed independently. The result matches the live GitHub tree `452a9003b03ff8f6eed47e1f609a36a054271455`. The completed-v9 manifest has SHA-256 `53ad7d0d5ff948758c4dedf437dc78f623303ba404449ce49d527233ec0d6218`; all 118 listed files were checked, in addition to the manifest itself. Source-retention comparison was then performed on expanded active TeX inputs.

A clean local build was run with fresh temporary auxiliary state and shell escape disabled. It produced byte-identical copies of the supplied PDFs:

| Document | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Main article | 97 | 1008928 | `492076686a51d7863ff4190ce5ef3b0deb10f3b5e76185b89c4ceb75bacbb375` |
| Companion | 7 | 333376 | `1aaf0d2ed11571e3744aa7126adeec95d6781b8a5116e28c12955d9c232be241` |

The build records no unresolved references or overfull boxes. Nonfatal font-expansion notices, one main-document underfull-box notice, and the expected disabled-shell-escape warning remain recorded. Actual rendered main pages 5, 30, and 32 were visually inspected; the table and displayed acquisition formulas were legible and not clipped on those pages. This is not a page-by-page visual inspection of all 104 pages.

The author suites were actually rerun: inherited 249 checks, completed-v9 407 checks, and v10 223 checks, each in normal and `python -O` modes. Each suite's two outputs are byte-identical. These suites overlap; their totals must not be advertised as independent proof obligations.

The separate `verify_review.py` imports no manuscript code. Its final normal and optimized runs give byte-identical output. It performs **139 finite exact mathematical checks**, plus **225 source, manifest, tree, and retention checks**. The mathematical checks cover simplex moments, monomial multipliers and fixed-ball bounds, Abel benchmark constants, positive-node interpolation and its scaling, the Bernoulli exponent, the preparation exponent, and calibration derivatives. The analytic arguments in Section 5 are proved in prose; finite arithmetic checks do not prove their asymptotic or functional-analytic conclusions. In developing the diagnostic I corrected an overly strong small-index monotonicity test: the displayed `C^2` ratio is eventually increasing, not increasing from every small index. This was a check-design issue, not a manuscript defect or a change to the asymptotic argument.

`VERIFICATION.json` records the actual source identities, build outcomes, suite summaries, and independent-output hash. These are local results, not a claimed GitHub Actions success, formal proof verification, statistical simulation, or an exhaustive audit of the whole research program.

## 9. Final disposition

The accurate assessment is **technically successful revision; unresolved top-four significance case**. I would not recommend acceptance at the requested level on the current submission. I would also not ask the author to redo the correctly proved finite-preparation theorem merely to generate another version number.

The next response should first acknowledge which earlier objections are closed, then address the actual contribution-level issue. The new norm and calibration calculations in this report are offered as concrete mathematical benchmarks, with their abstract-versus-physical limits stated explicitly. They are not compulsory additions, claims of priority, or a promise that adding them would secure acceptance. Correct generality and complete proofs should be preserved.

## Primary references used for the targeted comparison

**[P1]** S. V. Bolotin and D. V. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191–257. DOI: `10.1070/RM2010v065n02ABEH004671`; arXiv: `1006.1532`, Theorem 2.1. The periodic discrete determinant identity and relevant setup were consulted; the entire 78-page preprint was not re-refereed.

**[P2]** Z. Dai and P. K. Lamm, *Local Regularization for the Nonlinear Inverse Autoconvolution Problem*, SIAM Journal on Numerical Analysis 46 (2008), 832–868. DOI: `10.1137/070679247`. The official publisher abstract and bibliographic record support the limited comparison stated above.

**[P3]** B. Hofmann, F. Werner and Y. Deng, *On uniqueness and ill-posedness for the deautoconvolution problem in the multi-dimensional case*, arXiv: `2212.06534`. The retrieved 14-page preprint's real `L^2` setup, Section 2, and Section 3, especially Theorem 3, were consulted. Online PDF text was available; screenshot requests failed, so no independent visual verification of those external PDF pages is claimed.
