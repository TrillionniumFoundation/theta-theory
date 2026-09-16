# Response to the referee on A2, revision 66

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*, Qian Qi.  
**Revision:** 67, September 16, 2026.  
**Report answered:** `reviews/a2-v66-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md` at `3d49684cc6c9bad36d80c99dc46af276f53fae18`.  
**Reviewed mathematical source:** `38f798a9b28237420f070a032d3601f0bee72cde`; manuscript subtree `c693d717577dc5f501f2a86ec937cfa36bf6ce4e`.

We thank the referee for distinguishing the exact identification theorem, the finite-iteration estimate, the observation model and the significance assessment. We accept the quantitative point R66-m1 and correct it in the existing proposition, with a full propagation proof and a specified implementable recursion. We retain the global exact theorem at its established strength. The revised opening asks that the paper be assessed for one combined mechanism: a relative physical boundary law on a fixed collar and its actual geometric boundary-response inverse. It does not present this small correction as a new principal theorem or as an answer by itself to the importance question.

Both `rigidity.tex` and `main.tex` contain the revised abstract, opening and full correction. The three complete entry points remain, and no inherited proof input is removed. Filenames bearing earlier version numbers remain stable to keep the source graph and references transparent. References below use source labels rather than page numbers, which are generated from the final compiled source.

## R66-m1 and R66-D2: finite-iteration error and stopping terminology

**Disposition: corrected with an explicit proof.** The exact-fixed-point estimate in Proposition `prop:v66-finite-flight` is retained. Its finite-iteration extension now reads

\[
 \|\widehat q_{\le M}^{(m)}-q_{\le M}\|_\infty
 \le C_M(\tau^N+\varepsilon)+L_M E_m
 \le\widetilde C_M(\tau^N+\varepsilon+E_m).
\]

The first-increment estimate in Theorem `thm:v66-curvature` is identified as an **a priori** bound. The same theorem now states and proves the **a posteriori** residual bound

\[
 E_m=\frac{\|\Phi_s z^{(m)}-z^{(m)}\|_\infty}{1-q(s)}.
\]

For an inexact evaluation with certified error at most eta, the numerator is replaced by the computed increment plus eta. The test `min_i z_i^(m)>E_m` is a sufficient certificate that the exact fixed point lies in the strictly positive quadratic image. It is not a certificate of realization by arbitrary globally closed obstacles.

The subsequent use of an approximate curvature is no longer implicit. At fixed extracted action jets t and a positive approximate curvature v, we use the observed Schur ratios

\[
 \widehat\sigma_i(v;t_2)=
 \frac{\epsilon_i k_i}{k_i+t_{2,i+1}+v_{i+1}},\qquad
 D_n=(I-\widehat T_n)(I+\widehat T_n)^{-1},
\]

where `(T_hat_n w)_i=sigma_hat_i^n w_(i+1)`. The recursion is

\[
 \mathcal J_2(v;t)=v,\qquad
 \mathcal J_n(v;t)=D_n(v;t_2)
 \{t_n-\mathcal R_n(\mathcal J_2,\ldots,\mathcal J_{n-1})\}.
\]

At the exact fixed point these are the actual signed Jacobi factors and the actual finite-jet inverse. Away from the fixed point this is an expressly specified smooth algebraic extension; we do not claim it solves a physical nonstationary half-line problem. The lower-order remainders remain the smooth functions proved by the actual boundary envelope, not arbitrary formal remainders.

On the common positive jet boxes, let alpha<1 bound the ratios and let d_* bound their curvature derivatives. With U_n bounding the residual action coefficient and r_n bounding the joint derivative of R_n, the proof gives

\[
 b_n=\frac{1+\alpha^n}{1-\alpha^n},\quad
 \beta_n=\frac{2n\alpha^{n-1}d_*}{(1-\alpha^n)^2},\quad
 L_2=1,\quad
 L_n=\max\{L_{n-1},\beta_n U_n+b_n r_n L_{n-1}\}.
\]

Here the matrix differentiation uses `D_n=2(I+T_hat_n)^(-1)-I`; it does not commute a perturbation with a cyclic shift. Difference induction in the joint maximum norm proves the stated Lipschitz propagation. These are finite, class-dependent, fixed-order constants. They are neither claimed observable from noisy densities alone nor uniform in M. The correction changes no exact uniqueness statement, statistical exponent or density-error topology.

The referee's coefficient-one control is reproduced independently in `tools/check_revision_v67.py`. In the normal two-contact example, the first-increment bound is 12/77, whereas using the observed Schur ratios gives cubic error 48740/189931, strictly larger. The alternative actual-tail computation is checked by exact squaring. The script also checks a sufficient cubic propagation constant 2160/343. These are local jet/algebraic controls, not globally realized table counterexamples. Attribution to the report is retained in the acknowledgments and bibliography.

## R66-M1: endpoint multiplicities and the actual Schur converse

**Disposition: retained.** Lemma `lem:v66-schur` and its proof are unchanged. The initial curvature has weight one; the next interior contact receives the combined contribution of the first edge and the remaining half-line. The converse uses the decaying solution of the positive Jacobi problem and coercivity, not an arbitrary algebraic Riccati branch. Physical curvature is still `nu_i F_i''(0)`. The signed scaled sensor coordinates and their normalization are unchanged.

## R66-M2: positive image, clipping and iteration

**Disposition: retained and the stopping interface made explicit.** The global contraction on the closed orthant, its strictly positive image characterization, its nonimage example and its nonmonotone iteration example remain. Positivity of the action Hessians alone is still not sufficient for an admissible positive curvature tuple. The new residual certificate does not turn the clipped extension outside the image into a physical inverse or prove a global obstacle-realization theorem.

## R66-M3: global exact inverse versus uniform bounds

**Disposition: retained.** The equal-data cyclic contraction proof of injectivity, the data-dependent two-point bound, openness of the image and its analytic inverse remain. No convexity of the image is asserted. The action-Hessian floor in the contraction constant remains essential. The stopping estimate is proved on the same compact positive classes and does not assert a uniform estimate at zero curvature or grazing.

## R66-M4: actual smooth jets and analytic function-space inversion

**Disposition: retained.** The signed recursion still follows the actual stationary envelope, including the estimated terminal term and finite-jet factorization by interpolation of smooth representatives. Odd-degree signs are not discarded through orientation doubling. The exact analytic conclusion follows from coefficient equality on a common smaller neighborhood, without a candidate-closeness assumption. Smooth equality of jets is not called equality of smooth germs. The complete local analytic norm inverse and the real-law conditional stability theorem remain separately proved; global coefficient uniqueness is not substituted for their full-operator estimates.

## R66-M5 and R66-D3: exact whole-obstacle identification

**Disposition: retained at full strength and with its stated observations.** Entire connected closed analytic obstacle images are identified, without closeness, when the lattice and placement are fixed and every labelled obstacle is visited. The revised leading theorem keeps these hypotheses next to the conclusion. The alternating unregistered and unknown-lattice results retain their own weaker-data model. We do not transfer their strongest conclusions into the marked general-period theorem without proof.

## R66-M6: finite physical laws, extraction and charging

**Disposition: retained and integrated into the leading statement.** The revised principal theorem displays the relative fixed-collar action and twist estimates, the exact reference twist and the physical density before conditioning. Its proof points to the complete retained cofactor, trace-class and boundary-envelope proofs, not to the new stopping estimate as a substitute. Finite bridges are compared with realizable limiting densities before the two-offset extraction. The density error remains an interior C^M error with positivity and separated-offset margins. No derivative estimate is inferred from total variation alone, no exact factorization is imposed on finite bridges, and no general-period preparation budget is asserted.

## R66-E1: the significance case concerns the combined mechanism

**Disposition: substantively restated for reconsideration; not declared settled.** We retain the requested general-journal ambition. The principal result is now stated as a single forward/inverse theorem rather than leading with the newest finite-dimensional inverse. Its two noninterchangeable steps are visible on the first pages:

1. The exponentially small reference twist is divided out exactly at the corner-cofactor identity. A two-ended trace-class comparison then yields the nonlinear physical law on a collar independent of flight length. An absolute action expansion divided by a rare-event scale does not supply this result.
2. The boundary response is obtained from actual reflecting graphs, with the endpoint multiplicity and vanishing terminal term proved before the limit. This converts the nonlinear law into geometric jets and analytic contact germs. An inverse for arbitrary formal generating functions would not supply this conclusion.

The curvature contraction, successive signed jet steps and continuation complete this one mechanism. They are not counted as independent breakthroughs. We make two already proved consequences concrete. The area-preserving analytic support-function family in `thm:v4-jet-fiber` has identical gap, area, curvatures and all leading endpoint/count data but is distinguished by the nonlinear laws. Also the recovered amplitudes integrate to the actual stable coordinates, so the relative law determines nonlinear stable returns through `cor:v64-transmission`, not merely their multiplier. The family is an actual geometric construction, not an arbitrary tuple of quadratic data. Neither consequence is advertised as a new theorem of this revision or as a marked-length reconstruction.

These points give a specific mathematical basis on which to assess depth and reach: rare-event normalization retains nonlinear geometry lost by the complete leading record, and the retained information has an actual geometric and dynamical inverse. Whether that combined result reaches the exceptional-significance threshold remains an editorial judgment. We do not infer it from a build, file count, corrected constant or absence of a counterexample. The primary-literature comparison continues to identify different observations and does not claim exhaustively established priority.

## R66-E2 and R66-D4: no auxiliary-theorem repair loop

**Disposition: no new headline theorem and no arbitrary deletion.** The existing main theorem incorporates its forward physical content and proof dependencies; the existing finite-flight proposition receives its quantitative correction. No new active proof module is introduced. The abstract, common opening and cover letter are organized around the same mechanism, while all older results and their detailed proofs remain accessible and active in the corresponding full/principal entries. The manuscript is not rescaled into a smaller problem to obtain a nominally closed review.

We respectfully request a renewed assessment of the combined relative/contact theorem under this presentation. The referee's negative placement recommendation is not rewritten as an author-certified positive decision. Nor is a new version number presented as evidence of importance.

## R66-D1 and reproduction

The exact theorem, its hypotheses and the scope distinctions credited by the report are preserved. All 837 inherited paths remain: 829 are byte-identical in place and the eight edited framing/entry/bibliography/correction files have byte-exact originals in `history/v66-review-baseline/`. The active graph is unchanged: 134 distinct inputs, comprising 123 full, 55 principal and one companion input, with overlaps. All inherited labels in the corrected module remain.

The normal and optimized new diagnostic outputs agree. It checks 64 positive periodic quadratic data sets, 832 first-increment and 832 residual inequalities, 832 inexact-evaluation controls, 768 sufficient positivity certificates, 64 two-point bounds and 256 signed block norm/Lipschitz controls. These checks support debugging; the general statements are proved in the manuscript. Build and publication identities are recorded only after native execution in the final delivery, not anticipated here. Neither source retention nor compilation certifies all inherited mathematics.
