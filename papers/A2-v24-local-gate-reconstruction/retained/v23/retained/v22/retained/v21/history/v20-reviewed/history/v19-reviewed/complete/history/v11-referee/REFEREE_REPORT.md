# Independent referee report on A2 v11

**Manuscript:** Qian Qi, *Nonlinear boundary laws and stable energy invariants in dispersing billiards*.

**Date:** 10 September 2026. **Requested standard:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the American Mathematical Society.

**Status:** independent AI-assisted referee-style assessment requested by the author. This is not a journal-commissioned report, an editorial decision, or a formal proof certificate.

## 1. Source identity, scope, and recommendation

The source under review is the completed revision on `revision/a2-v11-abel-stable-boundary-profiles-2026-09-10`, frozen at author commit `c8af2cf4201deae5b447b490d44e3cba1aaa8ae0`. Its manuscript directory is `papers/A2-v11-abel-stable-boundary-profiles`, and its native subtree is `35a9fad03d7f1ee41f2c8661ee3c7aa58047bbad`. Its parent, `2b893b931a894dfc9e7730b853f575124ffb5c55`, contains the completed-v10 independent report. That report reviewed author commit `f46dca20f3d1b73077522bb2041f463af033cb70`. The source pins matter: this is a review of v11, not a recycled verdict on a preliminary v9 branch or the older eleven-paper A2.

Unless explicitly stated otherwise, manuscript paths below are relative to this frozen v11 directory. Theorem numbers are supplemented by TeX labels so that the objections remain traceable after renumbering. `SOURCE_AUDIT.json` records the source identities and coverage.

**Recommendation: reject at the requested four-journal level in its present form.** The recommendation is principally about the significance of the contribution demonstrated, not about a newly discovered false central theorem. I found no fatal mathematical error in the new Abel stability theorem, its stated acquisition bound, or the smooth-class self-calibration argument. Those additions are substantial responses to the preceding report and deserve explicit credit.

There is, however, a concrete mathematical reason not to treat the new preparation exponent as a mature quantitative result: the proof discards two derivatives of regularity already supplied by the exact integrated-flux identity. Without strengthening the profile class, assuming more regularity of the finite-bridge error, or adding observations, the same method gives the strictly better sufficient exponent

$$
2+\frac{6}{m-1/2}+\frac{\gamma}{|\log\tau|},
$$

rather than the displayed

$$
2+\frac{6}{m-5/2}+\frac{\gamma}{|\log\tau|}.
$$

For the minimum stated regularity, $m=4$, the accuracy power excluding the bridge term decreases from $6$ to $26/7$. Section 5 supplies a proof, including the unknown-calibration case. This does **not** falsify the author's weaker sufficient bound, and it is **not** a minimax claim. It does demonstrate that the headline improvement is still a conservative implementation-level estimate rather than a resolved information law.

The strongest part of the submission remains the nonlinear relative physical boundary law and the geometric meaning of its function-valued invariant. The current paper establishes meaningful information beyond leading amplitudes, but in my assessment it has not yet made a sufficiently compelling case for exceptional significance at the requested venue level. An editor could weigh that contribution differently. I do not claim that an earlier published theorem already contains the entire billiard result.

## 2. Disposition of the previous review

A severe review must not keep moving a closed objection under a new name. The following dispositions concern the actual v11 proofs, not just the response letter.

| Previous issue | Disposition for v11 |
| --- | --- |
| R1: identify the genuinely physical contribution and the information in the invariant | **Presentation improved; significance remains an editorial objection.** The introduction now leads with relative physical flux and explains the weighted energy pushforward. Existing realizations at fixed leading data are genuine evidence. They are not a characterization of the complete physical image or of all geometric fibres. |
| R2: resolve the integer-norm loss and justify any improved acquisition design | **The requested mathematical response is supplied.** Theorem 10.1 gives a linear Abel discrepancy with a valid triangle inequality; Section 13 redesigns interpolation and sampling. A different, newly identified inefficiency remains: the unused two-derivative regularity gain proved in Section 5 of this report. |
| R3: do not import calibration from an exact-family inverse into an unknown-smooth-remainder model | **Closed in the explicitly specified class.** Section 14 constructs and charges a one-/two-flight pilot. It no longer assumes the actual values of gap, area, and multiplier. Labels, coarse boxes, a gap bracket, and common regularity/convergence bounds are still supplied. |
| R4 and the odd-law wording | **Substantively addressed.** The introduction distinguishes even-law identification from separately observed odd-law validation. The result hierarchy remains broad, but there is no missing third identifying datum. |

The earlier finite-preparation, measurability, functional-setting, and experiment-separation objections that the v10 report closed are not reopened here. In particular, the following criticisms would now be inaccurate: that the inverse only accepts derivative observations; that failures are not charged; that the pilot assumes an exact nonlinear probability oracle; that the finite dictionary is nonmeasurable; or that full-profile reconstruction has been replaced by equality of Taylor series.

Conversely, closing those objections does not itself constitute a positive recommendation for one of the four journals. Correctness of a revision and exceptional significance of a submission are different questions.

## 3. Detailed audit of the new arguments

### 3.1 The Abel coordinate is a genuine nonlinear estimate

**Source:** `article/21_abel_stability.tex`, Theorem 10.1, `thm:v11-abel-inverse`; equations `eq:v11-abel-transform`, `eq:v11-weighted-volterra`, and `eq:v11-two-sided`.

Write $H_V(d)=d^2T(V,V)(d)$. The manuscript defines

$$
(\mathscr A H)(x)=\frac\pi2\left[H''(0)+\sqrt{x}\int_0^x\frac{H'''(s)}{\sqrt{x-s}}\,ds\right],
\qquad (\mathscr A H)(0)=\frac\pi2H''(0).
$$

This is an explicit linear transform of the data, not a discrepancy defined by an unknown inverse. Its endpoint term must be retained on general inputs. Its nullspace is exactly the affine functions, and hence it is a norm on the physical flux differences satisfying $H(0)=H'(0)=0$.

The weighted Volterra calculation checks out. Set $u=V-W$, $f=x^{-1/2}u$, $a=x^{-1/2}(V+W)$, and $k_*=x^{-1/2}$. Normalization makes $f$ continuous at zero. With $Q=(\pi/2)(H_V-H_W)''$, the convolution identities give

$$
Q=a*f,\qquad k_* *a=2\pi+R,\qquad R(0)=0,\qquad \|R'\|_\infty\le\pi B.
$$

Consequently

$$
\mathscr A(H_V-H_W)(x)
=2\pi u(x)+\sqrt{x}\int_0^xR'(x-s)\frac{u(s)}{\sqrt{s}}\,ds.
$$

The direct estimate follows by integrating $s^{-1/2}$. For the inverse, if $E=|H_V-H_W|_{\mathscr A}/(2\pi)$ and $v(x)=\int_0^x|u(s)|s^{-1/2}ds$, then

$$
v'(x)\le E x^{-1/2}+(B/2)v(x),\qquad
v(x)\le2E\sqrt{x}\,e^{Bx/2}.
$$

Substitution gives the stated constant $(1+BD e^{BD/2})/(2\pi)$. No illegitimate division of a uniform forcing bound by $\sqrt{x}$ occurs. No perturbative smallness of $V-1$ is needed.

The mixed estimate also follows from the stated near-/far-kernel split:

$$
|H|_{\mathscr A}\le\frac\pi2|H''(0)|+
2\pi\sqrt D\sqrt{\|H''-H''(0)\|_\infty\|H'''\|_\infty}.
$$

The square-root product is used only to estimate the linear seminorm, not as a purported norm in the minimum-discrepancy argument. This distinction resolves a real potential pitfall.

Proposition 10.2 correctly retains the monomial multiplier, the endpoint case $n=0$, and the fixed-class $C^2$ instability construction. The alternatives $1\pm a n^{-m}x^n$ remain in one nontrivial sum-norm ball. Their interpretation is appropriately restricted to the abstract profile operator. They are not physical billiard alternatives or a sample-complexity lower bound.

### 3.2 Positive-node reconstruction and the original v11 rate

**Source:** `article/26_abel_acquisition.tex`, Theorem 13.1, Corollary 13.2, Lemma 13.3; labels `thm:v11-acquisition`, `cor:v11-budget`, and `lem:v11-interpolation`.

The smooth partition of unity has a denominator bounded below after rescaling. At most two weights are positive at a point. All active Lagrange stencils stay a bounded rescaled distance away, including the first stencil $h,\ldots,mh$. Thus the reconstruction is globally smooth and uses no observed or inserted value at zero. Differentiating it is not distributional differentiation of a broken interpolant.

Polynomial reproduction, Taylor subtraction, and the mixed Abel estimate give the three bounds claimed for this particular stencil order:

$$
|J_hf-f|_{\mathscr A}\le Ch^{m-5/2}\|f\|_{m-1,1},\quad
|J_hf|_{\mathscr A}\le C\|f\|_{C^3},\quad
|J_hz|_{\mathscr A}\le Ch^{-5/2}\max_k|z_k|.
$$

The second bound is essential. It applies to the smooth finite-bridge error without a negative power of $h$. Only arbitrary scalar observation errors receive the $h^{-5/2}$ amplification. Replacing these two effects by a single nodal worst-case bound would weaken the theorem unnecessarily; there is no missing such factor in the author's proof.

For $c_j=2A\sinh(j\gamma)$ and $Z=c_j\overline Y$,

$$
\operatorname{Var}(Z)=\frac{c_jH_{j,b}(d_k)(1-p_{j,b}(d_k))}{N}
\le\frac{c_jMd_k^2}{N}.
$$

The small success probability has been used correctly. Bernstein's denominator is $2c_j(Md_k^2+t/3)$, and a union bound over $2L$ means explains $\log(4L/\eta)$. Summing the allocations, not the successes or waiting times, gives

$$
N_{\rm tot}\le2L+C A\sinh(j\gamma)h^{-1}t^{-2}\log(4L/\eta).
$$

The compact profile class has a compact nodal forward image. A finite ordered net and a first-minimizer tie rule produce a Borel estimator. A bound on computation time is not proved, but is expressly excluded from this statistical preparation count. That exclusion does not invalidate measurability.

The stated error bound and the exponent in Corollary 13.2 follow from $h\asymp\varepsilon^{1/(m-5/2)}$, $t\asymp\varepsilon h^{5/2}$, and the least admissible even flight number. The arithmetic is correct. The criticism in Section 5 is that a stronger approximation estimate is available after a small change of stencil order, not that this calculation is false.

### 3.3 Plug-in calibration does not reintroduce a singular offset normalization

**Source:** `article/27_profile_calibration.tex`, Theorem 14.1, `thm:v11-plug-in`.

Conditionally on the pilot, the mean of the newly scaled bit is exactly

$$
R H_{j,b}(d+\Delta),\qquad
R=\frac{\widehat A}{A}\frac{\sinh(j\widehat\gamma)}{\sinh(j\gamma)},\qquad
\Delta=j(\widehat g-g).
$$

The factor $(1+\Delta/d)^2$ belongs to the alternative procedure that divides by $d^2$ before regularization. It is absent here for a valid algebraic reason, not because calibration has been ignored.

The supplied uniform $C^{3,1}$ flux bound gives a $C^3$ translation error $O(\Delta)$. Positive compact multiplier boxes and $j|\widehat\gamma-\gamma|\le1$ control the logarithm of the hyperbolic-sine ratio. Hence

$$
\|R H_{j,b}(\cdot+\Delta)-H_b\|_{C^3([0,D])}
\le C(\tau^j+\alpha+j\zeta+j\rho).
$$

The one-sided gap estimate and the fixed margin $D<D_+$ are necessary parts of the argument. They keep every translated offset within the supplied nonnegative collar, including the origin used in the analysis. The theorem does not discard the energy origin. Applying $C^3$ stability of reconstruction to this structured bias is legitimate.

For $H=d^2$, translation adds an affine function annihilated by $\mathscr A$. The manuscript uses this only as a normalization benchmark. Its proof for nonlinear physical fluxes uses the smooth translation bound, so it does not assume an exact quadratic billiard realization.

### 3.4 The charged pilot is valid in the class stated

**Source:** the same file, Lemma 14.2 and Theorem 14.3, `lem:v11-calibration` and `thm:v11-self-calibrated`.

The one- and two-flight models have unknown, unrelated remainder functions, but their exact leading coefficients are

$$
c_r=[2A\sinh(r\gamma)]^{-1},\qquad r=1,2.
$$

These coefficients are supplied by the physical finite-flight law, not by an assumed exact positive-offset formula.

The noisy bracket uses $q=l+3w/4$. A success cannot occur below the onset and permits the upper update. On a correct incoming bracket, a false lower update requires $g\le l+w/2$; then $q-g\ge w/4$, giving the advertised exponential bound. The union bound is over histories with a correct incoming bracket. The width contracts by either $3/4$ or $1/2$ on every history, so the number of stages and the sum of preparation allocations are deterministically bounded even after an erroneous update. This separates high-probability correctness from unconditional cost control.

The extrapolation weights $(-1)^{k-1}\binom mk$ reproduce the value at zero of polynomials through degree $m-1$. With $s\asymp\xi^{1/m}$ and $\rho\asymp\xi s$, the remainder bias is $O(s^m)$ and the gap bias is $O(\rho/s)$. Since the physical success probabilities at these windows are $O(s^2)$, the variance of a normalized summand is $O(s^{-2})$, not $O(s^{-4})$. This gives the stated pilot cost $\xi^{-(2+2/m)}$ up to logarithms.

The identities $c_1/(2c_2)=\cosh\gamma$ and $A=(2c_1\sinh\gamma)^{-1}$ are correct. Projection onto supplied positive compact boxes makes the maps uniformly Lipschitz and keeps the profile-stage allocation bounded on bad pilot histories. Fresh preparations restore conditional independence. Taking $\xi\asymp\varepsilon/j$ and adding the two failure probabilities completes the argument.

Thus the old known-normalization information assumption has genuinely been removed in this specified smooth class. It would be unfair to call the result merely an interpretation of the exact-family four-window theorem. It would be equally wrong to describe it as label-free recovery, recovery without common regularity certificates, or recovery of arbitrary asymmetric contact graphs.

## 4. The physical theorem and its geometric content

The following chain was examined in the source, rather than accepted solely on the previous report's authority.

In `v3/10_geometry_action.tex`, separated positive curvature supplies a positive minimum roof, finitely many relevant lifted pairs, and unique closest chords. Near the onset, reflection forces a short itinerary to alternate within one selected channel. This uses a lower roof bound, not finite horizon. The alternating Jacobi scaling and effective endpoint Hessian retain the unequal-curvature factors and give the ratio $d_j^0/\sqrt{\det\mathsf H_j}=\operatorname{csch}(j\gamma)$.

The cofactor formula

$$
-W_{uv}=\frac{\prod_i(-\ell_{i,uv})}{\det H_{\rm int}}
$$

is normalized before the limit. Endpoint localization controls the tridiagonal perturbation in trace norm. The logarithmic determinant estimate costs one trace norm and bounded operator norms, not the number of interior sites. This is the decisive distinction from dividing an absolute approximation by an exponentially small twist.

In `v4/10_boundary_layers.tex`, the half-line contraction constructs the action and amplitude. The finite bridge is compared with two glued half-lines in an $\ell^1$ norm. The determinant comparison retains two endpoint blocks, controls discarded tails in trace norm, and estimates the remote Green reflections and cross blocks exponentially. Fixed derivative orders introduce polynomial factors absorbed by a strict exponential margin. `v5/15_differentiated_operators.tex` correctly requires bounded differentiated trace norms, not small differentiated perturbations.

In `v3/20_integration.tex`, the full-phase factor $1/(2\pi A)$ and the residual-time integral are retained. The common Morse coordinate construction fixes the integration domain before offset differentiation. This is what makes the normalized physical law smooth down to zero on a collar independent of flight number. The construction is not an arbitrary endpoint ensemble substituted for the physical preparation law.

The energy change of variables in `article/20_boundary_compatibility.tex` identifies the normalized symmetrized pushforward and gives the full Volterra convolution identity. Its uniqueness proof applies on a collar to functions, not only to jets. The separately measured odd law tests a constraint predicted by the two even laws; it is not a third independent coordinate of this invariant.

There is also genuine physical separation beyond leading data. `v4/20_nonlinear_information.tex`, Theorem `thm:v4-jet-fiber`, constructs an analytic support-function family on $3\mathbb Z\times4\mathbb Z$ with fixed selected gap, free area, and both contact curvatures. The higher coefficient varies, with the displayed derivative $\sqrt3/2$. The proof uses an exact area adjustment and the quartic action/determinant calculation. Therefore an objection that the manuscript contains no physical example distinguishing its nonlinear invariant from leading amplitudes would be false.

What this establishes is a local invariant associated with selected near-period-two collision channels, together with observations of that invariant. It does not classify the full fibres of the map from arbitrary asymmetric contact geometry to the two symmetrized profiles. Nor does the absence of a finite-horizon assumption turn this particular near-onset theorem into a global mixing or general long-time statistical theorem. These are scope distinctions, not defects in the assertions actually proved.

## 5. New quantitative objection: two available derivatives are discarded

**Classification:** substantive quantitative objection to the strength of the highlighted result; **not** a counterexample to its stated sufficient upper bound.

**Location:** `article/26_abel_acquisition.tex`, the first paragraph of “The estimator and its full preparation charge,” and the use of `eq:v11-approx` in the proof of Theorem 13.1. The text retains only a $C^{m-1,1}$ bound for $H_V$, citing the corresponding bound for $T(V,V)$ and multiplication by $d^2$. That bound is true but unnecessarily weak. The exact identity `eq:v9-kernel-def` supplies two more derivatives globally, including at zero.

### 5.1 Uniform two-derivative gain

Keep precisely the author's class $\mathcal K_m(B,\beta;D)$, $m\ge4$, and define $H(V,W)=d^2T(V,W)$. Then

$$
H(V,W)''(d)=\frac2\pi\int_0^1
\frac{V(ds)W(d(1-s))}{\sqrt{s(1-s)}}\,ds. \tag{R1}
$$

The identity follows by differentiating twice the residual-time convolution, or directly from `eq:v9-kernel-def`. It is not an assumption of additional observed data.

**Claim.** There is $C=C(m,D)$ such that

$$
\sup_{V,W\in\mathcal K_m}\|H(V,W)\|_{m+1,1}\le C B^2. \tag{R2}
$$

Here the norm has the same sum convention as the manuscript, with derivatives through order $m+1$ and the Lipschitz seminorm of the last derivative.

**Proof.** Put $Q=H(V,W)''$. For $0\le r\le m-1$, differentiation of (R1) gives

$$
Q^{(r)}(d)=\frac2\pi\sum_{a=0}^r\binom ra
\int_0^1\frac{s^a(1-s)^{r-a}
V^{(a)}(ds)W^{(r-a)}(d(1-s))}{\sqrt{s(1-s)}}\,ds. \tag{R3}
$$

All derivatives in this expression are bounded by the profile norm; the weight is integrable and the remaining powers are at most one. Thus $\|Q^{(r)}\|_\infty\le 2^{r+1}B^2$. Dominated convergence justifies these differentiations up to the endpoints.

Every derivative $V^{(a)}$ with $a<m-1$ is Lipschitz with constant at most $B$ by its next derivative. The same assertion for $a=m-1$ is part of the class definition. The difference of each product in (R3), evaluated at $d$ and $e$, is therefore bounded by $C B^2|d-e|$. Integrating proves a uniform Lipschitz bound for $Q^{(m-1)}$. Hence $Q\in C^{m-1,1}$ uniformly.

Finally $H(0)=H'(0)=0$ and

$$
H'(d)=\int_0^d Q(s)\,ds,\qquad
H(d)=\int_0^d(d-s)Q(s)\,ds.
$$

These control the two lower derivatives and establish (R2). No extension across zero, physical realization of dictionary elements, or derivatives of $V$ of order greater than $m-1$ are required. The Lipschitz highest derivative is sufficient. This proves the claim.

### 5.2 Higher-order positive stencils, without a stronger profile class

Use the same smooth partition of unity, but interpolate at $q=m+2$ positive nodes per stencil, with polynomial degree $q-1=m+1$ and $L\ge q$. Denote the resulting operator by $J_h^{[q]}$. The first stencil is $h,\ldots,qh$. The unknown profile and dictionary still belong to $\mathcal K_m$; they are **not** replaced by a smoother class $\mathcal K_{m+2}$.

The proof of Lemma 13.3 applies with this fixed stencil size. From (R2), Taylor subtraction gives

$$
\|(J_h^{[q]}H_V-H_V)''\|_\infty\le Ch^m,\qquad
\|(J_h^{[q]}H_V-H_V)'''\|_\infty\le Ch^{m-1}.
$$

The mixed Abel estimate consequently yields

$$
|J_h^{[q]}H_V-H_V|_{\mathscr A}\le Ch^{m-1/2}. \tag{R4}
$$

The endpoint second-derivative contribution is $O(h^m)$ and is smaller than this bound when $h\le1$. The same result holds for every candidate flux $H_W$ in the dictionary.

The two other estimates do not deteriorate in their powers:

$$
|J_h^{[q]}f|_{\mathscr A}\le C\|f\|_{C^3},\qquad
|J_h^{[q]}z|_{\mathscr A}\le Ch^{-5/2}\max_k|z_k|. \tag{R5}
$$

For the first, subtract the quadratic Taylor polynomial exactly as in the manuscript. For the second, use the second- and third-derivative scales $h^{-2}$ and $h^{-3}$. Constants can depend on the fixed integer $m$; none depends on accuracy. Global smoothness and positive-node extrapolation are preserved.

In particular, the argument does **not** demand a $C^{m+1,1}$ bound on the finite-flight bias. That bias is still controlled by the first bound in (R5) from the original supplied $C^3$ estimate. Only the limiting candidate fluxes use (R2). Confusing these two roles would incorrectly add a new hypothesis.

### 5.3 The improved estimator and deterministic charge

For fixed $h$, choose a finite ordered dictionary in $\mathcal K_m$ approximating $\mathscr A J_h^{[q]}H_V$ in uniform norm. The same compact nodal-image argument supplies it, and the first minimizer is Borel. Use exactly the Bernoulli allocations of Theorem 13.1.

On its simultaneous concentration event, (R5) gives

$$
|J_h^{[q]}Z_b-J_h^{[q]}H_b|_{\mathscr A}
\le C(th^{-5/2}+\tau^j).
$$

The minimizing property, dictionary tolerance $\delta$, and triangle inequality compare the two reconstructed candidate fluxes. Applying (R4) to both candidates, followed by Theorem 10.1, gives

$$
\max_b\|\widehat V_b-\mathcal V_b\|_\infty
\le C\{h^{m-1/2}+\tau^j+th^{-5/2}+\delta\}. \tag{R6}
$$

The odd-law prediction follows with the existing $2B$ factor. All scalar observations, including failures, are unchanged. Their deterministic count is still

$$
2L+C A\sinh(j\gamma)h^{-1}t^{-2}\log(4L/\eta). \tag{R7}
$$

Choose $h$ comparable to a sufficiently small multiple of $\varepsilon^{1/(m-1/2)}$, $t=c\varepsilon h^{5/2}$, and $\delta=c\varepsilon$. Choose the least even $j\ge2$ with $\tau^j\le c\varepsilon$. Rounding the grid and the even flight number changes only constants. Then $h^{-1}t^{-2}=c^{-2}\varepsilon^{-2}h^{-6}$, and

$$
N_{\rm tot}\le
C\varepsilon^{-\left(2+\frac6{m-1/2}+\frac\gamma{|\log\tau|}\right)}
\log\frac{C}{\eta\varepsilon}. \tag{R8}
$$

The ceiling contribution $2L$ is smaller. This proves the improved sufficient bound under the same calibrated observation assumptions.

### 5.4 Unknown calibration remains subordinate

Repeat Theorem 14.1 with $J_h^{[q]}$. Its structured calibration bias is still controlled by (R5), so the error in (R6) acquires exactly the same additional term $C(\alpha+j\zeta+j\rho)$. No inverse power of the finer or coarser grid multiplies it.

Keep the pilot at its original regularity $m$, with $\xi=c\varepsilon/j$. Its total cost is bounded by

$$
C(j/\varepsilon)^{2+2/m}
\log\frac{C\log(Cj/\varepsilon)}{\eta}.
$$

Since

$$
2+\frac6{m-1/2}+\frac{\gamma_+}{|\log\tau|}>2+\frac2m,
$$

this cost, including its logarithmic factors, is absorbed by the improved profile-stage bound for sufficiently small accuracy. Projection of the pilot estimates preserves the unconditional deterministic charge. Thus (R8) holds with $\gamma_+$ in place of $\gamma$ under the unchanged hypotheses of Theorem 14.3.

For clarity, the powers below omit the common bridge contribution; they are sufficient bounds for the respective constructions, not competing minimax exponents.

| Profile regularity index $m$ | v11 profile-stage power | Bound proved here | Pilot power |
| --- | ---: | ---: | ---: |
| 4 | $6$ | $26/7$ | $5/2$ |
| 5 | $22/5$ | $10/3$ | $12/5$ |
| 6 | $26/7$ | $34/11$ | $7/3$ |
| 8 | $34/11$ | $14/5$ | $9/4$ |

### 5.5 A conditional modulus, and the limits of this benchmark

A deterministic consequence makes the role of the regularity gain explicit. Let $V,W\in\mathcal K_m$, and put $e=\|H_V-H_W\|_\infty$. From (R4), (R5), and the inverse theorem,

$$
\|V-W\|_\infty\le C\{h^{m-1/2}+e h^{-5/2}\}.
$$

For sufficiently small positive $e$, choose $h\asymp e^{1/(m+2)}$. This gives

$$
\|V-W\|_\infty\le C e^{(m-1/2)/(m+2)}. \tag{R9}
$$

The case $e=0$ follows by letting $h\downarrow0$; larger bounded errors are covered by enlarging the constant. This is a conditional Hölder estimate on a fixed regularity class of forward images, not an unconditional uniform-data Lipschitz inverse. It does not contradict the fixed-class $C^2$ instability benchmark.

Neither (R8) nor (R9) is claimed optimal. There may be further gains from using the convolution structure, spatially varying noise, or a different regularization. The proof above needs none of those possibilities. Nor does it construct physically realizable alternatives for a lower bound: the larger profile class is used for an upper-bound estimator only.

The requested response to this objection should acknowledge the gain (R2), check the modified estimator, and state the status of the published exponent accordingly. Merely saying “we never claimed minimax optimality” is logically true but does not answer why an elementary consequence of the paper's own central identity was omitted from a highlighted quantitative advance. Conversely, it would be wrong to describe this report as having disproved Theorem 13.1 or 14.3.

## 6. Remaining objections at the requested venue level

### R1 — The exceptional-contribution case still rests on the physical invariant

The relative flux law is the technically distinctive part of the submission. The subsequent weighted Volterra estimate, compact-net estimator, concentration inequality, and finite-order calibration are coherent consequences once that physical input is available. They increase the usefulness of the invariant, but do not by themselves demonstrate a broadly new inversion mechanism or an exceptionally strong geometric consequence.

The explicit physical family at fixed leading data is valuable. It establishes that the new observable is not redundant. It does not, on its own, describe how much arbitrary asymmetric geometry is determined by the full pair of profiles, what the remaining fibres look like, or what substantial inverse problem is thereby resolved. Those are different questions from finite-jet nonconstancy. The paper correctly does not claim their solution; their absence matters to the strength of the significance case, not to the truth of its current theorems.

A stronger case could come from a consequential theorem about the physical image or fibres of the invariant, a suitably specified geometric rigidity/separation result, or a genuinely discriminating observation theorem with physical alternatives. These are possible routes, not a demand to prove all of them or a claim that every top-four article must contain a minimax lower bound. Adding the numerical improvement in Section 5 alone would not settle this editorial issue.

### R2 — The quantitative narrative is still implementation-dependent

Section 5 gives a concrete reason, rather than a general complaint about sharpness. The new sufficient rate loses two regularity orders that the integrated-flux identity already recovers. In addition, the bridge contribution depends on a supplied certificate: a larger admissible $\widetilde\tau<1$ makes $\gamma/|\log\widetilde\tau|$ arbitrarily worse without changing the billiard. The manuscript acknowledges this, so it is not a false complexity claim. It remains a limitation on using the exponent as the submission's principal exceptional achievement.

The separate smooth-envelope and finite-dimensional minimax results cannot supply a lower bound for full-profile acquisition without an experiment comparison and physically admissible alternatives. The author keeps these models separate. That separation must survive any next revision.

### R3 — Known labels and class bounds are still substantive information

Theorem 14.3 removes the actual values of $g,A,\gamma$, not the entire information set. The selected patch labels, parameter boxes, coarse gap bracket, common positive collars, and regularity/convergence constants remain supplied. These are legitimate hypotheses. They must stay visible whenever the result is summarized as a physical inverse theorem.

Likewise, two symmetrized energy profiles are full functions, not merely finitely many coefficients, but they are not the two unsymmetrized branches of arbitrary contact graphs. Neither overstating nor dismissing that target is acceptable. The revised introduction is substantially accurate on both points.

### R4 — Preservation of source history is not a substitute for a decisive result hierarchy

The author records a 107-page main article and retention of all 176 previous active statement/proof environments, with 192 in v11. Those are author-reported build and retention facts, not independent certificates from this review. Length alone is not an objection, and no arbitrary deletion of correct proofs or weakening of valid generality is requested.

The difficulty is that a local relative-law theorem, a function-valued inverse, two generations of acquisition, endpoint experiments, exact-family curvature recovery, nuisance minimax theory, and historical applications still compete for prominence. The author should distinguish the main theorem and its essential proof chain from auxiliary benchmarks more decisively. Historical material can remain completely available and correctly cross-referenced without every inherited result having equal narrative status.

This is not a request to restart a correctly proved argument merely to generate another version. It is a request for a contribution-level explanation of what the completed paper establishes that most strongly warrants the chosen venue.

## 7. Targeted comparison with primary literature

The literature check in this review is deliberately limited. I consulted the official arXiv abstracts for [P1] and [P3] and the official publisher abstract and bibliographic record for [P2]. I did not re-referee their complete proofs in this session.

[P1] concerns Hill-type relations between periodic monodromy and action Hessians, including discrete Lagrangian systems. This supplies relevant determinant context. It does not, on the evidence checked here, identify the manuscript's Dirichlet, nonlinear, relatively normalized physical flux theorem as a mere restatement.

[P2] develops causal local regularization for nonlinear autoconvolution, with convergence and rates for continuous and $L^2$ data. Thus causality and regularization of autoconvolution are not new subjects introduced by A2. The publisher abstract is not enough to assert an exact theorem-level reduction of the present weighted problem to that paper.

[P3] studies real $L^2$ full- and limited-data deautoconvolution, including nonnegative uniqueness under a support condition. The present normalized kernel $x^{-1/2}V(x)$ has square asymptotic to $1/x$ and is not in ordinary $L^2$ near zero. That is a genuine functional distinction. It is not, by itself, proof of historical priority or exceptional significance.

No exhaustive novelty clearance has been performed. The limited comparison supports neither the assertion that the entire physical theorem is already known nor the assertion that its full combination is unprecedented. The author's detailed new proofs must carry their own mathematical content, and the submission must explain the significance of that content without relying on a citation count or a verification count.

## 8. Reproducibility, independent checks, and limits

The central source files were read through the authenticated GitHub connector at the frozen commit. The main new stability, acquisition, and calibration files were examined in full, together with the core geometric, relative-determinant, integration, and profile-inverse chain described above. The response letter and the previous completed report were consulted. This is not an exhaustive audit of every retained appendix, the companion, or the eleven-paper program.

I did **not** reconstruct the entire local manuscript tree, rerun the author verification suites, compile the manuscript, or visually inspect its PDFs in this session. The author's `VERIFICATION.json` reports those author-session activities; this report does not relabel them as independent reproductions. No remote CI status is claimed.

The separate `verify_review.py` was actually executed in normal and optimized Python modes. It uses only the standard library, imports no manuscript code, and makes no network calls. The two JSON outputs are byte-identical. It performs **534 finite exact-rational checks** covering polynomial integrated-flux identities, the weighted nonlinear Volterra identity, Abel monomial inversion and affine annihilation, differentiation coefficients, positive-node reproduction, pilot extrapolation, Bernoulli variance, calibration algebra, all 34 terminal histories of a finite bracket-width diagnostic, and the preparation-power calculations.

The normal output SHA-256 is `7f9a5a22213439b9f191f4001067f974b8c31518b93996190a846fbbe9b9214f`. The script SHA-256 is `5dfe3e1f9634ded1579af9a46be28fdec84c35636ff3ee722a9f8459b92bc104`. `checks.json` and `VERIFICATION.json` record the actual results and limitations. Reproduce them with:

```sh
python verify_review.py --output checks.normal.json
python -O verify_review.py --output checks.optimized.json
cmp checks.normal.json checks.optimized.json
```

These finite checks do not prove the function-space estimates, asymptotics, concentration theorems, or physical realizations. The proof of the new benchmark is the mathematical argument in Section 5, not a test count. The checks overlap and must not be presented as independent proof obligations. They are also not a physical billiard simulation, a formal proof certificate, or a journal decision.

## 9. Final disposition and requested response

The accurate disposition is: **substantive and technically coherent revision; a new, demonstrable quantitative inefficiency; unresolved exceptional-significance case at the requested venue level**.

A further response should preserve the closed status of the old acquisition and calibration objections, address the two-derivative gain and its consequences explicitly, and identify the principal physical theorem or geometric consequence on which the top-four case rests. It should not describe the present report as finding a fatal error in the Abel inverse, a free-calibration assumption, or a failure to charge rare events. None of those findings was made.

I would not recommend acceptance of the current submission at the requested level. That recommendation is not a no-go claim about the research program, a reason to remove correct generality, or a promise that one more rate improvement would secure acceptance. Complete valid proofs and accurate scope should be retained.

## References and source anchors

**[M]** Qian Qi, A2 v11, author commit `c8af2cf4201deae5b447b490d44e3cba1aaa8ae0`, manuscript root `papers/A2-v11-abel-stable-boundary-profiles`. Source: https://github.com/TrillionniumFoundation/theta-theory/tree/c8af2cf4201deae5b447b490d44e3cba1aaa8ae0/papers/A2-v11-abel-stable-boundary-profiles . Individual paths and TeX labels are specified at each substantive finding above.

**[R10]** Independent completed-v10 report, review commit `2b893b931a894dfc9e7730b853f575124ffb5c55`, blob `fddd3e9ed0004c7ea0f80c662575f1d308413bff`, path `reviews/a2-v10-observable-profiles-harsh-independent-2026-09-10/REFEREE_REPORT.md`. Source: https://github.com/TrillionniumFoundation/theta-theory/blob/2b893b931a894dfc9e7730b853f575124ffb5c55/reviews/a2-v10-observable-profiles-harsh-independent-2026-09-10/REFEREE_REPORT.md . This is an author-requested memorandum, not a commissioned journal report.

**[P1]** S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65, no. 2 (2010). DOI `10.1070/RM2010v065n02ABEH004671`; arXiv `1006.1532`. Official abstract consulted 10 September 2026: https://arxiv.org/abs/1006.1532 .

**[P2]** Z. Dai and P. K. Lamm, *Local Regularization for the Nonlinear Inverse Autoconvolution Problem*, SIAM Journal on Numerical Analysis 46 (2008), 832–868. DOI `10.1137/070679247`. Official publisher abstract and bibliographic record consulted 10 September 2026: https://epubs.siam.org/doi/10.1137/070679247 .

**[P3]** B. Hofmann, F. Werner, and Y. Deng, *On uniqueness and ill-posedness for the deautoconvolution problem in the multi-dimensional case*, arXiv `2212.06534`. Official abstract consulted 10 September 2026: https://arxiv.org/abs/2212.06534 .
