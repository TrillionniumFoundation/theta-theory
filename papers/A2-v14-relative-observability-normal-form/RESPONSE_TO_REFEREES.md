# A2 v14 — response to the v13 referee reports

**Article:** *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*.
**Date:** 28 September 2026.

The controlling report is `reviews/a2-v13-external-harsh-top4-rereview-2026-09-28/REFEREE_REPORT.md` at `a02d58d2b77e3337f001cf13676c5ff70e1ba97c`. We also address the earlier v13 report and its analytic-normal-form companion at `b3f0ad5843782c221651c9189fc156d20865cab1`. Both reviewed the author source `0e54099f079232df233316ae6fe7986fc51b7ea1`, native tree `ee946ef91770778839f15c8c35416d401e99ea1c`.

The 28 September canonical branch name was an alias of the 10 September author source. It was not a new mathematical response. This revision adds new source and proofs on a separate revision line based on the latest report. The old author manuscript and review branches are not changed.

## 1. The finite-family quantifier

**Objection.** The abstract claimed positive-window observation for every fixed finite-dimensional family. A remote-obstacle translation preserving the selected channel and area disproves that reading. The actual v13 theorem concerned the constructed physical contact families.

**Response.** The abstract now states the constructed-family result and a separate precise regular-rank principle. `article/01a_relative_observability.tex` identifies the two claims before the theorem development. `article/31_regular_observability.tex`, Theorem `thm:v14-rank`, proves the equivalence between injectivity of the tangent observation map, a nonsingular set of positive-window evaluations, and a local bi-Lipschitz window map. For analytic tangent germs the same condition holds on every nonempty open subinterval of the common connected collar. The proof is the finite-dimensional duality argument selecting a basis of evaluation covectors, followed by the quantitative local inverse-function argument.

Corollary `cor:v14-observable-quotient` also identifies the local observable quotient when the tangent rank is constant. It does not infer regularity from exact injectivity at a singular point, and does not identify noisy statistical experiments. The remote-obstacle example is included with its precise local information-set interpretation.

The full statement and proof of `thm:v13-two-flight-observation` remain active. Thus the correction is not a replacement of a positive theorem by a prohibition: it supplies the missing general criterion and verifies it in an additional physical family below. The elementary rank principle is not advertised as a new general inverse-function theorem.

## 2. The closest analytic forward comparator

**Objection.** Comparing the relative law only with cofactor identities and global inverse-spectral theorems omitted the relevant local analytic hyperbolic mechanism, including the physical projection step.

**Response.** `article/16_normal_form_comparison.tex` gives the entire comparator, with the following steps and hypotheses.

The input is a supplied analytic canonical normal form

\[
N(s,p)=(\Delta(sp)s,\Delta(sp)^{-1}p),\qquad \Delta(0)=\lambda\in(0,1),
\]

and transverse analytic physical endpoint charts. For a two-step billiard return, `n` counts returns, `j=2n`, and `lambda=exp(-2 gamma)`. The proof does not confuse this with a one-flight multiplier.

Lemma `lem:v14-mixed-normal-form` solves the mixed-boundary equation on a fixed complex box and derives

\[
I=st\Delta(I)^n,\qquad
T_n=\frac{\Delta(I)^n}{1-nI\Delta'(I)/\Delta(I)}.
\]

It estimates `lambda^(-n) T_n - 1` before taking derivatives, using the analytic logarithm and Cauchy estimates on a smaller fixed box. This is genuinely relative control, not an absolute error divided after the estimate.

Proposition `prop:v14-physical-normal-form` derives the exact physical identity `J_n=|T_n/det D Phi_n|` from the symplectic two-form. It proves common physical-box inversion, the normalized product limit, the exact origin determinant (including the `lambda^(2n)` correction), and the stationary-action limit. Corollary `cor:v14-amplitude-identification` identifies the individual normalized factors with the half-line determinant amplitudes by uniqueness of limits. A worked canonical-shear example exhibits nonconstant physical amplitudes even for a linear normal form. It is explicitly not claimed to realize arbitrary canonical charts as billiards.

The local analytic normal-form input has been checked against De Simoi–Kaloshin–Leguil, arXiv:1905.00890v4, printed pp. 10 and 13. The mixed-boundary/projection benchmark was supplied by the 10 September referee memorandum and is acknowledged as such. It is not attributed to the published global inverse theorem or claimed as an independent discovery in this revision.

**The increment is now specified theorem by theorem.** The analytic comparator already explains a nonlinear relative product and its geometric interpretation. The retained physical theorem starts from arbitrary smooth geometric families, rather than supplied normalizing charts; constructs the half-line trace-class determinant; includes fixed mixed geometric derivatives, both parities, first-hit localization, and actual residual-time integration. Its complete symmetrized-profile inverse, compatibility identity and charged observation theorem are separate conclusions beyond the analytic forward comparator. No claim is made that a suitable smooth normal-form approach is impossible. Nor is the top-journal significance question treated as settled merely by adding the comparator.

## 3. Area normalization and a finite experiment without supplied area

**Objection.** The normalized finite law uses `A`, although the initial geometric data convention named only the gap and the two curvatures. Extracting the leading coefficient of an exact germ is not a finite noisy calibration procedure.

**Response.** The introductory data convention and subsection `sec:v14-normalization` distinguish three operations explicitly. A geometric inverse may take normalized exact germs as input. Raw exact probability germs determine their common leading coefficient `ell`, hence `A=1/(2 ell sinh(2 gamma))`. The original fixed-area finite-window theorem supplies `A` as part of its family. No zero-offset or limiting operation is counted as a finite noisy observation.

There is also a new constructive resolution using actual windows. Proposition `prop:v14-free-area` keeps the existing support coefficient of `sin^(2M+2)(theta)` free, instead of using it to impose fixed area. It does not change graph jets through order `2M`. Its exact area derivative is

\[
\partial_\zeta A=-\int_0^{2\pi}(h+h'')\sin^{2M+2}\theta\,d\theta<0.
\]

Together with the retained triangular support-to-contact Jacobian, this proves that `(A,q_2,...,q_M)` are coordinates on an actual `(2M-1)`-dimensional analytic billiard family, at fixed labelled `g,kappa_0,kappa_1`. The old fixed-area, fixed-leading-hierarchy family remains a slice of this construction.

Theorem `thm:v14-area-windows` then recovers these coordinates from `M` positive windows in one orientation and `M-1` in the other, all at two flights. In coordinates `(alpha,alpha xi_0,alpha xi_1)`, where `alpha=(2A sinh(2 gamma))^(-1)`, the nodal Jacobian is a Vandermonde matrix with a shared constant coefficient. The first block has `n+1` distinct nodes, the second `n` nonzero distinct nodes, with `n=M-1`; the shared-intercept kernel argument proves invertibility. Its inverse grows as `h^(-n)`, while the Taylor remainder is `O(h^(n+1))`, giving an `O(h)` preconditioned error. Only known `(ih)^2` row scalings are used on the raw probabilities.

The theorem includes complete finite-net measurability, confidence, squared-risk upper-bound, and adaptive two-point lower-bound proofs. The `2M-1` window count is minimal only for a regular coordinate map made of scalar window means on this full-dimensional family. It is not a minimax preparation count over other observation types or increasing dimensions. The separate labelled curvatures remain supplied; the general smooth-class profile pilot is not silently used as an uncharged contact-jet oracle.

## 4. Source chronology and preservation

The source identity in the report is respected. All previously active chapters, results and proofs remain in the new native manuscript, with its entire reviewed native tree preserved at `history/v13-reviewed`. The new arguments are active inputs of `main.tex`, not a proposed migration script or an unattached research plan. Earlier proof ledgers and verification claims are historical and are replaced by a new scoped ledger at the v14 root. They remain available in the exact source snapshot.

The source checker requires the snapshot tree to equal `ee946ef91770778839f15c8c35416d401e99ea1c`; checks reachability of all old inputs and the new inputs; compares old formal statements and proofs; and checks active labels and external companion references. Its exceptions remain enabled under optimized Python. The full manuscript build compiles the companion before the main file.

## 5. Distinct targets and experiments

The main theorem chain is retained: general smooth physical relative laws; complete symmetrized profiles and compatibility; independent individually even labelled contacts; finite-order inverses including equal curvatures; analytic physical realization; and the charged smooth-class profile experiment. Fixed `M` is not replaced by an unproved uniform growing-order statement. Analytic exact determination is not noisy analytic continuation. The selected-channel inverse is not whole-table isometry. The parametric `N^(-1)` risk is not a full-profile minimax claim. The supplied-family model and its geometric data are stated where they are used.

These distinctions specify the proven mathematical claims rather than changing the intended level or abandoning the geometric programme. The response addresses the technical requests with proofs and a physical extension. It does not claim a journal acceptance, an independent proof certification, or that the referee's significance judgment has already changed.

## Verification scope

At preparation of this response, 1,588 finite exact algebra checks passed in normal and optimized Python with identical outputs. The new arguments compiled in an isolated eight-page typesetting harness; references to the retained chapters are intentionally unresolved in that isolated harness. This is not a full-manuscript build claim. `VERIFICATION.json` records these limits and the source digests. The read-only GitHub workflow builds and checks the exact pushed source and archives its actual command output, PDF, source identity and hashes. Its queued, running, or completed state must be read from the actual workflow; the repository does not turn a queued build into a pass.
