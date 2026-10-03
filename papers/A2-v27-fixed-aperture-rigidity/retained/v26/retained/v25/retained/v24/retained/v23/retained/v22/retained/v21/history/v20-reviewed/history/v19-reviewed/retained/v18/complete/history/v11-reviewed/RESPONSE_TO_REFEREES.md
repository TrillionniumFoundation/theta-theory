# Response to the referee on A2 v10

**Revised manuscript:** Qian Qi, *Nonlinear boundary laws and stable energy invariants in dispersing billiards* (A2 v11, 10 September 2026).

**Report answered:** `reviews/a2-v10-observable-profiles-harsh-independent-2026-09-10/REFEREE_REPORT.md`, review commit `2b893b931a894dfc9e7730b853f575124ffb5c55`. Its parent is the completed v10 author commit `f46dca20f3d1b73077522bb2041f463af033cb70`, whose native manuscript tree is `452a9003b03ff8f6eed47e1f609a36a054271455`. The report itself has Git blob `fddd3e9ed0004c7ea0f80c662575f1d308413bff`; an unchanged copy is retained in `history/v10-referee/REFEREE_REPORT.md`.

## 1. The point of this revision

We thank the referee for separating the successful mathematical response in v10 from the remaining assessment of significance. We accept the report's disposition of the earlier E1--E4 comments: the finite-preparation theorem, the specified deautoconvolution comparison, the separation of observation models, and the even-reconstruction/odd-validation distinction are no longer missing arguments. We have not recast the venue recommendation as a newly discovered error in those theorems.

The new revision addresses the actual quantitative and information questions. It proves a two-sided nonlinear estimate in a weighted Abel norm of the integrated physical flux, reconstructs the unknown profiles using that linear discrepancy, and obtains a strictly better sufficient preparation bound. It also gives a calibration procedure inside the same smooth physical experiment. This last result estimates the unknown gap, area and multiplier from separately charged one- and two-flight observations rather than importing the exact-family four-window inverse. The finite-flight remainder functions remain unknown.

These additions leave the geometric hypothesis and full nonlinear forward theorem unchanged. The existing theorem on the complete function-valued symmetrized energy invariant is retained. All 176 active theorem, lemma, proposition, corollary and proof environments in the reviewed v10 main manuscript are retained byte-for-byte and in their previous relative input order. There are 192 such environments in the new main manuscript, a source-retention count rather than a count of independently certified theorems. The original two-collision companion is unchanged. Every pre-existing repository path is preserved by constructing the revision in a new directory on top of the completed review commit.

We do not infer a journal decision from these additions. The requested four-journal standard remains the target. The assertions below specify the new mathematics on which a subsequent assessment can be based.

## 2. R1: identify the physical contribution and the information in the invariant

The title, abstract, first page of the introduction, and dependency table now put the physical relative law first. The core chain is explicitly:

`localized nonlinear Dirichlet determinant -> relative physical flux -> full boundary energy profiles -> stable flux coordinate -> charged physical acquisition`.

The nonlinear limit concerns the actual mixed endpoint derivative divided by its exponentially small reference value. The proof still normalizes the cofactor formula before estimating the determinant; the error is not obtained by dividing an absolute estimate by an exponentially small denominator. The two endpoint perturbations are summable in trace norm. The common Morse domain then preserves the physical residual-time integral and the normalization `1/(2 pi A)`. The corresponding proofs in `v3/10_geometry_action.tex`, `v3/20_integration.tex`, `v4/10_boundary_layers.tex` and `v5/15_differentiated_operators.tex` remain active and unchanged.

The invariant reconstructed from the two even laws is the normalized pushforward of the half-line determinant-weighted endpoint measure under its excess action. It is a full function on a nonzero collar, not merely a list of Taylor coefficients. The existing physical realizations at fixed leading data are now placed next to this explanation in the introduction. The quartic and higher-jet realizations are not asserted to be new in v11: their full proofs were already present and are retained. They demonstrate that the nonlinear invariant is not determined by the selected gap and multiplier. They do not characterize the entire physical image of the abstract profile class, and they are not used as unproved lower-bound alternatives.

The weighted Abel result strengthens the available characterization of this invariant. For `H_V(d)=d^2 T(V,V)(d)`, define

\[
 (\mathscr A H)(x)=\frac\pi2\left[H''(0)+\sqrt x\int_0^x\frac{H'''(s)}{\sqrt{x-s}}\,ds\right].
\]

Theorem 10.1 proves, for normalized profiles with first derivatives bounded by `B`,

\[
 |H_V-H_W|_{\mathscr A}\le2\pi(1+BD)\|V-W\|_\infty,
\qquad
 \|V-W\|_\infty\le\frac{1+BD e^{BD/2}}{2\pi}|H_V-H_W|_{\mathscr A}.
\]

No perturbative smallness of `V-1` is assumed. The data transform is explicit and linear; it is not defined through the unknown inverse. Its nullspace on general `C^3` functions is exactly affine, so it is a norm on physical profile-law differences, which have zero value and first derivative at zero. The proof is a weighted second-kind Volterra estimate. This is a precisely stated stable coordinate for the existing physical invariant, not a claim to have invented a general deautoconvolution principle.

## 3. R2: the half-order benchmark and the redesigned acquisition theorem

We acknowledge the referee's exact monomial multiplier, fixed-class `C^2` instability, and mixed-norm calculation. Proposition 10.2 includes the complete argument and expressly credits the report. It also records the exact cancellation

\[
 \mathscr A(\lambda_n d^{n+2})=2\pi d^n,
 \qquad \lambda_n=\frac{4(1/2)_n}{(n+2)!}\asymp n^{-5/2}.
\]

The two-sided alternatives remain in a single nontrivial abstract sum-norm ball; their smoothness radius does not grow with `n`. They are not represented as physical billiard alternatives. This proves neither a full-profile minimax bound nor a sharp fractional Holder endpoint theorem.

The new estimator does not simply insert a mixed estimate into the previous `C^3` proof. Section 13 makes three separate changes and proves their interaction.

First, the raw bit is multiplied by `c_j=2A sinh(j gamma)`, not by `c_j/d_k^2`. Its mean is the integrated flux `H_{j,b}(d_k)=d_k^2 F_{j,b}(d_k)`, and its variance is at most `c_j M d_k^2/N`. Thus the sum of the allocated integrated-flux variances has order `h^{-1}`, not the `h^{-2}` sum produced by the old normalization. No success is conditioned upon and every preparation is charged.

Second, we construct a globally smooth positive-node reconstruction. A smooth partition of unity combines degree-`m-1` Lagrange polynomials on fixed-size stencils. All sampled nodes are strictly positive; the first stencil is `h,...,mh`. The value at zero is extrapolated, never supplied. The reconstruction is globally smooth, so no distributional differentiation across interpolation cells occurs.

Third, the dictionary criterion is the seminorm of the **linear** Abel transform. We do not treat the geometric mean of two norms as a norm. The triangle inequality in the minimum-discrepancy argument is therefore valid. Lemma 13.3 proves separately

\[
 |J_h f-f|_{\mathscr A}\le C h^{m-5/2}\|f\|_{m-1,1},\quad
 |J_h f|_{\mathscr A}\le C\|f\|_{C^3},\quad
 |J_h z|_{\mathscr A}\le C h^{-5/2}\max_k|z_k|.
\]

The second estimate applies to the smooth finite-bridge bias. Only the last estimate amplifies arbitrary scalar observation errors. Compactness supplies a finite ordered dictionary and a first-minimizer tie rule supplies Borel measurability. Its size and computational running time are not included in the statistical preparation count.

Theorem 13.1 gives the new error bound

\[
 \max_b\|\widehat V_b-\mathcal V_b\|_\infty
 \le C\{h^{m-5/2}+\tau^j+t h^{-5/2}+\delta\}.
\]

The preparation allocation and all ceilings are stated in the theorem. Corollary 13.2 chooses `h` of order `epsilon^{1/(m-5/2)}`, scalar tolerance `t` of order `epsilon h^{5/2}`, and the least admissible even bridge length. It proves the sufficient bound

\[
 N\le C\varepsilon^{-[2+6/(m-5/2)+\gamma/|\log\tau|]}
                  \log\frac{C}{\eta\varepsilon}.
\]

For `m=4`, the accuracy power excluding the relative-convergence term is six rather than ten. Both exponents refer to specified constructions and certificates. We expressly retain the referee's observation that worsening an admissible `tau` worsens this bound; the exponent is not declared an intrinsic complexity of a billiard. The old theorem and its entire proof remain in Section 12 as an integer-norm comparison.

## 4. R3: calibration is now acquired in the same smooth model

The previous calibrated theorem is kept exactly as stated. The additional Section 14 proves what is required for a different information set. It does not reinterpret the old exact-family inverse.

### 4.1 Plug-in errors are smooth after the correct preprocessing

If the pilot gives an upper gap estimate and clipped positive area and multiplier estimates, the exact mean of a bit sampled at `j g_hat+d` and scaled by `2 A_hat sinh(j gamma_hat)` is

\[
 R H_{j,b}(d+\Delta),\qquad
 R=\frac{\widehat A}{A}\frac{\sinh(j\widehat\gamma)}{\sinh(j\gamma)},
 \quad\Delta=j(\widehat g-g).
\]

Theorem 14.1 proves that on a fixed subcollar this differs from the limiting integrated flux in `C^3` by at most

`C(tau^j + alpha + j zeta + j rho)`,

where `alpha`, `zeta` and `rho` bound the relative area, multiplier and one-sided gap errors. A supplied uniform `C^{3,1}` finite-flux bound controls the translation. It is a consequence of the physical smooth relative law on compact families when four derivatives are supplied. The gap estimate is one-sided to keep all translated offsets nonnegative. The target is `[0,D]` with a fixed margin `D<D_+`; the origin is not discarded.

The corresponding contribution to the profile error has no negative power of the grid width. The referee's formula with `(1+Delta/d)^2` is fully consistent: it describes dividing the same bits by `d^2` before estimation. The new procedure avoids that division. The exact annihilation of the affine shift of the quadratic benchmark illustrates the effect; the proof for nonlinear physical fluxes uses the stated smooth translation bound, not an assumed exact quadratic realization.

### 4.2 The pilot is constructed and charged

Lemma 14.2 works with the exact finite-flight onset coefficients but **unknown, unrelated smooth remainders**:

\[
 P_r(rg+d)=c_r d^2 F_r(d),\quad
 c_r=[2A\sinh(r\gamma)]^{-1},\quad r=1,2,
\]

with `F_r(0)=1`, a common positive lower bound, and a supplied `C^{m-1,1}` sum bound. A known coarse gap bracket of width at most a common collar and compact positive area/multiplier boxes are part of the theorem. These are class bounds, not exact parameter values.

A charged noisy bisection first obtains an upper gap estimate. A success cannot occur below the onset. A failed batch above a specified fraction of the current bracket has exponentially small probability. The bracket always contracts, so both its maximum number of decisions and its preparation charge are deterministic even on a bad history.

Fresh one- and two-flight samples at `r g_hat+k s`, `1<=k<=m`, then estimate the two leading coefficients by positive-node polynomial extrapolation. The exact weights are `(-1)^{k-1} binom(m,k)`. The remainder bias is `O(s^m)` and the gap bias is `O(rho/s)`. Choosing `s` of order `xi^{1/m}` and `rho` of order `xi s` yields coefficient accuracy `O(xi)` and gap accuracy `O(xi^{1+1/m})`. The scaled Bernoulli variance, rather than a constant-variance bound, gives total pilot cost

\[
 C\xi^{-(2+2/m)}\log\frac{C\log(C/\xi)}{\eta_0}.
\]

The identities `c_1/(2c_2)=cosh(gamma)` and `A=[2c_1 sinh(gamma)]^{-1}`, with projections into supplied boxes, give stable estimates of the multiplier and area. This uses the exact leading physical coefficient, not an exact positive-offset probability oracle. Independence is restored by taking fresh profile-stage preparations after the pilot.

### 4.3 The new information-set theorem

Theorem 14.3 takes `xi` of order `epsilon/j`. Its pilot errors then contribute `O(epsilon)` to Theorem 14.1. The pilot has a strictly smaller accuracy power than the profile stage, including its logarithmic factors. Since pilot estimates are clipped even on bad outcomes, the total charge remains deterministic. Uniformly over the supplied multiplier box,

\[
 N\le C\varepsilon^{-[2+6/(m-5/2)+\gamma_+/|\log\tau|]}
                     \log\frac{C}{\eta\varepsilon}.
\]

This removes the exact `g,A,gamma` information in that explicitly specified smooth class without increasing the box-uniform sufficient exponent. It does not replace `gamma_+` by an unobserved optimal complexity constant. Patch labels, common regularity/convergence bounds and a coarse bracket are still supplied. The output remains both symmetrized energy profiles, with the odd law predicted from them. No claim of unrestricted asymmetric contact-graph recovery, unlabelled recovery, or a full-profile minimax lower bound is made.

## 5. R4 and the presentational comments

The manuscript remains a complete article rather than a response memorandum with proof sketches. The abstract identifies the physical relative law and its stable invariant before presenting observational consequences. The introduction's dependency map separates the central physical chain from endpoint experiments, contact-graph jet applications, exact-family curvature inversion, and the smooth-envelope minimax benchmark. All inherited proofs remain active in the main manuscript or its existing appendices; none is dropped to manufacture a shorter result hierarchy.

The phrase about an independent odd compatibility constraint has been replaced by the precise statement that separately observed odd records test the compatibility predicted by the two even laws. The corresponding reconstruction theorem already had this meaning and is unchanged. Both the new acquisition theorem and its proof make positive-node extrapolation and structured-bias versus scalar-noise amplification explicit.

The deautoconvolution section preserves the comparison with Dai--Lamm and Hofmann--Werner--Deng and adds the role of the new data norm. The normalized `x^{-1/2}V(x)` kernel is not an ordinary square-integrable unknown near zero. This functional distinction is stated without elevating it to a historical-priority claim. The Hill comparison still distinguishes periodic determinant identities from the present nonlinear Dirichlet relative flux estimate. The report's calculations are acknowledged as such. We do not claim exhaustive novelty clearance.

## 6. Historical derivations and verification

`HISTORICAL_DERIVATION_AUDIT.md` records which source chain supports each assertion. The baseline was authenticated against the live GitHub tree, not trusted by archive name. All 104 native v10 files reproduce the reviewed tree. The new full source retains every previous active formal environment; the independent new retention diagnostic pins their ordered length-prefixed digest.

A clean local build with fresh auxiliary state and shell escape disabled produces the complete main article and unchanged companion. The build script checks unresolved references, duplicate labels and overfull boxes and records its actual PDF hashes, pages and notices. Selected rendered pages are inspected separately and identified in the verification record. The ordinary and optimized runs of the inherited, v9, v10 and v11 finite suites are byte-identical within each suite. The suites overlap and their totals are not additive proof obligations. New exact arithmetic tests cover the weighted Volterra polynomial identity, Abel multipliers, interpolation/extrapolation identities, calibration and variance algebra, bisection charge arithmetic, and exponent calculations.

These checks are finite diagnostics and source-integrity evidence. They are not formal proofs of the analytic or probabilistic theorems, physical simulations, an exhaustive audit of the eleven-paper program, or a claimed GitHub Actions success. The new proofs are supplied in the manuscript for the next referee to examine. The remaining judgment of exceptional significance is not declared settled by a longer paper, a lower sufficient exponent, or a successful build.
