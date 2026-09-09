# Response to the A2 v5 referee reports

## Submission and controlling sources

**Revised title:** *Relative boundary laws and statistical reconstruction in periodic dispersing billiards*.  
**Author:** Qian Qi.  
**Date:** September 9, 2026.  
**New manuscript:** `papers/A2-v6-relative-transfer-count-experiments/main.tex`.  
**New branch:** `revision/a2-v6-relative-transfer-count-experiments-2026-09-09`.

This revision answers both the statistical-contact-rigidity report at `9975aa037d5d9eb1f339b9220f9cd21fb54c0876` and the later second report at `0421836a5868967f90093281c7ca43aab9815a0d`. The actual reviewed author manuscript is the v5 statistical-contact-rigidity source at `1e57d9c024f90f0304e5572c0e320707bab88074`. The parallel boundary-factorization v5 branch is not substituted for that source. The previously inspected branch whose name included v6 contained only a review snapshot; it is neither overwritten nor represented as a mathematical revision.

The new submission is a complete English article, locally compiled to 63 pages, not an outline or an intended future revision. Its new directory is built on the complete selected v5 paper tree. All original repository paths and both reviews are retained. The new driver keeps the full active forward, relative-factorization, contact, acquisition, inverse, record-response and circular-appendix proofs. The unchanged two-collision companion also compiles, to seven pages. Source labels below are controlling; page numbers refer to the delivered build.

The reports distinguish proof correctness from the importance judgment at the requested journal level. We address the mathematical and presentation requests by precise statements, complete additional proofs, and an integrated account of the observation models. We do not treat either the previous absence of an identified fatal error or the current successful diagnostics as an acceptance recommendation.

## SCR-R1: actual and effective curvatures

**Request.** The general nonsymmetric forward setting does not allow separate endpoint curvatures to be recovered from a scalar channel exponent.

**Revision.** The abstract, introduction, opening of the four-amplitude section, and both new scalar acquisition sections now state the equal-facing-curvature hypothesis whenever the recovered scalar parameters are called actual curvatures. Equation `eq:v6-effective-curvature` prints the effective parameter in the general case:

\[
\kappa_e^{\mathrm{eff}}=
\frac{\sqrt{(1+g\kappa_{e,0})(1+g\kappa_{e,1})}-1}{g}.
\]

The four-amplitude observation map remains valid with these effective parameters. It is not an inverse for both endpoints of an asymmetric channel. The general forward theorem, Theorem 1.1 (`thm:g-stability`), and the relative boundary theorems retain their nonsymmetric hypotheses and do not acquire a finite-horizon assumption. Actual unequal endpoint curvatures remain recoverable by the separate two-variance theorem, using conditional positions. Thus the general forward result and the stronger observation result are preserved rather than replaced by a symmetric-only setup.

## SCR-R2 and second-report formula (F): finite jets, finite flights and conditioning

**Request.** Distinguish exact analytic uniqueness, fixed-order coefficient inversion, high-order sensitivity, and extraction of coefficients from noisy probability values. Incorporate the finite-flight comparison without attributing new information exclusively to the long-bridge limit.

**Revision.** Section 9, `v6/20_finite_jet_stability.tex`, gives the complete finite-flight calculation in Theorem 9.1 (`thm:v6-finite-jets`, pp. 26-27). With the notation printed there,

\[
-\partial_{q_{2m}}f_{j,m-1}
=\alpha_m\left(\sum_{i=0}^j w_i\nu_i^m+
4m\sum_{i=1}^{j-1}G_{ii}\nu_i^{m-1}\right)
\ge 2\alpha_m a^{-m}>0.
\]

The proof separates the first action variation from the relative interior-determinant variation, verifies that the edge-product term vanishes at the relevant degree, and integrates both with the physical residual-time weight. It justifies the finite-degree dependence at arbitrary lower jets. The endpoint terms give an explicit lower bound independent of flight number. Combining it with the uniform coefficient-derivative estimates and a finite triangular recursion yields inverse neighborhoods and Lipschitz constants uniform in all `j >= 1` at each fixed recovered order `M`.

Accordingly, coefficient error `delta` gives jet error `C_M delta` using the finite-flight inverse, or `C_M(delta + tau^j)` using the limiting inverse. This is a positive uniform-in-length improvement, not an inverse estimate uniform in `M`. The one-flight reduction and the two separated half-line sums are proved explicitly. The old all-order limiting inverse, analytic-boundary corollary, realization theorem and one-flight proof remain active in Section 8.

Proposition 9.2 (`prop:v6-sensitivity`) gives the limiting/one-flight ratio

\[
(\tanh\gamma)^m\{\coth(m\gamma)+2mD_m\}
=(\tanh\gamma)^m\{1+O_\gamma(m e^{-2(m-1)\gamma})\}.
\]

It is expressly a comparison of highest-jet diagonal sensitivities at fixed lower jets and equal absolute coefficient error. It is not identified with the condition number of the entire triangular map, a noisy analytic-continuation theorem, or a comparison of statistical minimax risks. Exact analytic continuation remains a uniqueness argument in the contact frame, not a stable global reconstruction algorithm.

**Attribution.** The limiting sensitivity formula was supplied in the first controlling report; formula (F) was supplied in the second. They are not claimed here as calculations first discovered in this revision. The extension to a uniform-in-flight fixed-order inverse is proved from the positive endpoint lower bound and the inherited differentiated estimates.

## SCR-R3: three physical amplitudes and four ambient amplitudes

**Request.** An independent area normalizer creates a four-parameter ambient model; area is constrained in the chosen physical family. The fourth amplitude should not be advertised as indispensable in that family.

**Revision.** Theorem 15.1 (`thm:v5-pairwise`) retains its full four-amplitude statement and proof for the independent-normalizer model. Section 16 proves the physical refinement, Theorem 16.1 (`thm:v6-three`, pp. 44-46). The exact support-family area identity is derived in elementary symmetric radius coordinates:

\[
A(R,e)=\frac{\sqrt3}{2}-\pi R^2-\frac{\pi R}{54}e_1
 +\frac{41\pi}{7776}e_1^2-\frac{5\pi}{432}e_2.
\]

The proof extends the symmetric sums analytically to a full coefficient neighborhood, supplies the derivative table, and computes at `R=1/4`, `g=1/2`,

\[
\det D_e\Psi_3=
-\frac{2\sqrt2(15804720 A_0+64253\pi)}{72930375 A_0^4}\ne0.
\]

Augmenting by the measured gap also allows nearby changes in `R`. The inverse-function argument precedes restriction to real-rooted physical parameters. It yields Lipschitz area and symmetric-coefficient recovery, and matching-curvature error of order `Delta^(1/3)` without a node-separation hypothesis. The retained physical two-sided path proves the exponent sharp in this three-amplitude setting. The theorem is local near the specified physical reference, not a universal minimal-data theorem for all radii or all periodic tables.

**Attribution.** The first controlling report supplied this three-amplitude sharpening and determinant. The present section incorporates a full derivation and the joint-gap formulation; it does not claim that the numerical or algebraic observation originated here.

## SCR-R4: a count-only experiment with charged fine calibration

**Request.** The selected-position sampling theorem must not be presented as a count-only acquisition theorem for an unlabelled coalescing triple.

**Revision.** Section 17 supplies the missing count-only chain. Lemma 17.1 (`lem:v6-amplitudes`) starts with the actual Bernoulli observations at finitely many physical windows and proves the amplitude error bound

\[
C_m\left(h^m+\sqrt{\frac{\log(C_m/\eta)}{nh^2}}
 +\frac{\log(C_m/\eta)}{nh^2}\right).
\]

Theorem 17.2 (`thm:v6-count-only`, pp. 47-48) also charges fine timing. Starting from the supplied coarse bracket `|g-g_0| <= h/4`, a count-only first-order pilot estimates the simple zero of square-root onset probabilities; its positive unknown normalizer cancels. Fresh counts at the first three or four flight orders then estimate the amplitudes. The safety shift `L=J+1` keeps every second-stage offset positive on every pilot outcome, not merely on the successful event. The proof conditions on the entire pilot, controls the uncancelled timing error by `C_m |g_hat-g|/h`, and charges both expected and high-probability raw preparation costs.

It gives gap error `O_m(h^(m+1))`, area error `O_m(h^m)`, and matching-curvature error `O_m(h^(m/3))`, with raw-preparation order `h^(-2m-2) log(C_m/eta)`. Thus curvature accuracy `epsilon` has sufficient cost

\[
C_m\epsilon^{-(6+6/m)}\log(C_m/\eta).
\]

No impact positions, channel labels, or supplied fine gap enter this experiment. The coarse bracket, fixed finite extrapolation order, noiseless count/time recording, and compact local model are explicit assumptions. Its global coarse-location cost is not hidden in the displayed rate. The selected-position theorem remains Theorem 12.3 with its different sufficient cost `e^(j gamma) epsilon^(-(2+2/m))`. Neither acquisition rate is called minimax optimal. The first report's known-gap count baseline is acknowledged; the additional construction here includes the fine pilot and its unconditional safety/cost accounting.

## SCR-R5: the central mechanism and its experimental consequence

**Request.** Explain the relative physical boundary law as a central result, accurately compare related inverse strategies, and avoid substituting a list of different data models for a unified theorem.

**Revision.** The title, abstract and introduction are organized around the relative two-boundary law. The original nonlinear gluing, Fredholm determinant and differentiated integration proofs are retained. The new Theorem 6.1 and Corollary 6.2 (`thm:v6-transfer`, `cor:v6-risk`, pp. 18-19) give a direct experiment-level consequence under the same general forward assumptions.

In common endpoint/residual-time coordinates, conditional total variation is at most `C tau^j`. Restoring failed preparations gives one-preparation error `C p_{j,d} tau^j`, with `p_{j,d}` comparable to `d^2 exp(-j gamma)`. For `n` independent preparations, the product error is at most `min(1,C n p_{j,d} tau^j)`, and the same estimate transfers bounded risks. The proof uses the vanishing value and gradient of the action error to obtain `C tau^j |Y|^2`, controls the moving residual-time domain by one-dimensional fibres, and retains the normalized determinant factor. An absolute approximation to a vanishing twist would not supply this estimate.

Predetermined physical observation times are addressed explicitly: the parameter-dependent excess is used in the proof, not supplied as additional data. Fixed-excess designs still require a supplied or calibrated onset. The total-variation statement concerns the specified coarsened records; it is not extended without justification to growing arrays supported on distinct embedded surfaces. The original bounded-Lipschitz result for those arrays is retained.

Section 19 adds the comparison with Zelditch's localized wave-trace coefficient strategy and retains the distinctions from Hill identities, marked-length reconstruction, Prony accuracy, and other statistical asymptotics. The primary records were checked for the added comparison. A spectral trace, a marked-length spectrum, and a positive normalized phase-volume onset probability are not treated as interchangeable observations. This is an argument for the actual mechanism and its new consequences, not a declaration that the journal-level importance question is settled.

## Second-report calculation (V): what the realization preserves

Theorem 8.3, the abstract and the introduction now consistently say: all collision-order leading count and endpoint-metric coefficients of the selected horizontal ground channel, with its reverse orientation. The global free area is also fixed. Section 9.1 reproduces and explains the physical vertical-channel check inside the same support family, including `z'(0)=-6/5`, `g_v'(0)=2/5`, `r_v'(0)=3` and the nonzero logarithmic leading-amplitude derivative `21/10`. This calculation was supplied in the second report. It is included as a precise indexing clarification, not as a counterexample to the correctly stated horizontal realization or as a reason to delete it.

## Preservation, verification and remaining review responsibility

The unchanged `v2`, `v3`, `v4` and `sections` directory Git hashes were checked against the reviewed source. Six inherited v5 files were byte-verified before targeted edits. The original reviewed versions are retained in history, and the historical v1-v4 materials, existing ledgers and scripts remain in the new Git paper tree. A proof/dependency ledger identifies every new conclusion and its assumptions. Source pins identify the reports and the actual author base separately.

The local build contains no undefined references, multiply defined labels, LaTeX warnings or overfull boxes. All 63 pages were rendered; layout contact sheets and representative mathematical pages were inspected. The new diagnostic script completed 147 checks (112 exact and 35 ordinary floating), both normally and under `python -O`, with identical JSON. The latest referee's unchanged script was separately rerun in both modes: 166 checks (123 exact and 43 ordinary floating), also with identical output. Commands, environment and hashes are in `VERIFICATION_V6.json`; detailed outputs accompany the local revision packet.

These are finite diagnostics and build checks, not interval enclosures, a proof-assistant certificate, remote CI certification, or an exhaustive originality investigation. The old author's entire validation suite and every inactive historical branch have not been newly re-audited. The complete arguments, their strengthened consequences and the stated observation models are submitted for another independent mathematical review.
