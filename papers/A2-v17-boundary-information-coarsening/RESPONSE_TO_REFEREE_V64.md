# Response to the independent referee report on A2, revision 63

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Revision:** 64, September 16, 2026  
**Report addressed:** `reviews/a2-v63-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md`, at review commit `493196e4f6f1d9a46c062df0e3669c3ca26c4fcc`.  
**Reviewed mathematical source:** `f5517519440b897707ddc60deeafba19e86bb5a5`, manuscript tree `b042811c7ceb2c5fd841b2a03ab0b8c232c39dce`.

We thank the referee for distinguishing the mathematical status of the examined arguments from the assessment of exceptional significance. The report closes the preceding concrete correction and literature request and establishes no new mandatory core repair within its stated coverage. We do not recast that conclusion as a new defect to repair, nor as certification of all the manuscript's results.

The revision makes a substantive extension of the same geometric relative mechanism. It is not another correction-only iteration. Both complete manuscripts now contain a fully proved periodic-itinerary relative theorem, its physical phase-volume law, and an explicit nonnormal realization. The signed alternating-contact inverse and all its analytic, global and statistical consequences remain active, with their previous hypotheses and conclusions. The general-journal submission objective is unchanged.

## 1. R63-E1: depth and demonstrated reach of the relative/action mechanism

The referee's central reservation concerns the demonstrated reach of the relative normalization beyond a specially chosen alternating channel. The new section `article/10a_periodic_itinerary_relative_v64.tex`, actively included in both manuscripts after the original two-boundary proof and its differentiated-operator subsection, addresses exactly that issue.

**Geometric extension.** For a selected clear nongrazing periodic itinerary of a smooth planar dispersing billiard, scaled signed arclength gives the actual geometric Jacobi operator

\[
 (H^0x)_i=(k_{i-1}+k_i+m_i)x_i-k_{i-1}x_{i-1}-k_ix_{i+1},
 \qquad k_i=L_i^{-1},\quad m_i=2\kappa_i/\nu_i>0.
\]

Lemma `lem:v64-geometric-jacobi` derives these coefficients from the chord Hessian and proves uniform coercivity, persistence, and physical clearance. This is not an abstract theorem which assumes the desired endpoint estimates. Neither normal incidence nor equal flight lengths is assumed. An odd primitive orbit is handled by doubling its oriented period.

**Exact normalization.** Lemma `lem:v64-reference` proves the reference twist for `N=nP` flights:

\[
 D_{N,b}=\frac{\sinh\chi}{(\mathcal M_b)_{12}\sinh(n\chi)},\qquad
 \mathcal M_b=\prod_{i=b}^{b+P-1}\begin{pmatrix}1+m_i/k_i&1/k_i\\m_i&1\end{pmatrix},
 \quad\operatorname{tr}\mathcal M_b=2\cosh\chi.
\]

The product is chronologically ordered as printed in the manuscript. The derivation retains the half endpoint mass in the stationary boundary derivative and proves agreement with the tridiagonal cofactor; an unspecified exponential equivalent would not suffice.

**The relative theorem.** Theorem `thm:v64-periodic-relative` constructs distinct future and past half-line actions and amplitudes on a flight-independent collar and proves

\[
 W_{N,b}-nL+p_bu-p_bv=S_b^-(u)+S_b^+(v)+O_{C^k}(\tau^N),\qquad
 -W_{N,b,uv}/D_{N,b}=B_b^-(u)B_b^+(v)+O_{C^k}(\tau^N).
\]

Its proof supplies weighted Green bounds, the finite-to-half-line reflected-kernel estimate, nonlinear gluing, summable perturbations, two-end compressions and the differentiated trace-series estimate. All derivative orders remain separately fixed. The actual finite mixed cofactor is normalized before taking the limit; no absolute action error is divided by the exponentially small reference twist.

**Physical and nonlinear interpretation.** Theorem `thm:v64-physical-law` restores the oblique endpoint momenta before using the physical clock. The limiting positive-window density is proportional to

\[
 B_b^-(u)B_b^+(v)\{d-S_b^-(u)-S_b^+(v)+p_bu-p_bv\}.
\]

The unconditioned endpoint measure carries the exact factor `D_{N,b}/(2 pi A)`, including the charged exponentially small acceptance mass. The first/last collision interpretation and the residual-time interval are proved, not inferred from a conditional density. This is explicitly a selected windowed itinerary, not the entire maximal-collision event.

Corollary `cor:v64-transmission` identifies the connected action at its relative scale: after division by `D_{N,b}`, it tends to the product of the two integrated amplitudes, with remainder `O(tau^N |uv|)`. The same amplitudes linearize the future stable and reversed unstable period maps. Double integration and scalar linearization are presented as consequences, not as independent exceptional innovations.

**A realized departure from the alternating setting.** Proposition `prop:v64-triangle` constructs a clear nongrazing three-obstacle orbit in a periodic table, with normal cosine `sqrt(3)/2`, and an open family with unequal flight lengths and incidence angles. The reference example is checked geometrically, including the third-obstacle clearance. The construction by a scalene contact triangle and nearby radii gives explicit nonsymmetric realizations. Thus the new hypotheses have physical examples outside the original normal two-contact setting.

For the normal alternating specialization the exact factor reduces to the inherited `a_b/sinh(2n gamma)`, and the half-line functions and intrinsic density agree after the stated coordinate conversion. This is one mechanism on a larger geometric domain, not an unrelated inverse problem. It does **not** extend the two-contact inverse block formula to arbitrary periodic itineraries; the existing inverse retains the geometry it uses.

## 2. R63-E2 and D4: no nominal repair cycle and no verdict by bookkeeping

The new section is integrated into the theorem/proof sequence of both manuscripts. The introductions identify which part of the argument has broader scope and which part uses the alternating geometry. They do not substitute a theorem count, another certificate, or a placement claim for the new proof. The principal article and the full technical manuscript remain distinct; all original proof inputs remain active. No unrelated information principle or global finite-data theorem has been appended to answer the report.

The proposed significance case is now that a relative physical transmission law survives throughout the class of selected nongrazing dispersing periodic itineraries, whereas the complete geometric inverse exploits a further two-contact structure. This is a mathematical account of the mechanism's reach. Whether that account meets the exceptional-significance threshold remains a matter for independent expert and editorial assessment. We request assessment of the actual new theorem together with the retained inverse, rather than reconsideration of a ceiling correction already accepted.

## 3. R63-M1, M2, M3 and D1: pilot and complete acquisition budget

The entire active finite-experiment module `article/23f2_finite_experiment_analytic_inverse_v62.tex` is byte-identical to the v63 source, not merely its five statement bodies. The exact all-history ceiling identity, its distinction from successful stopping, every programmed scan, and the complete preparation cap are preserved. The physical position pilot in `article/25a_common_observables_v25.tex` is likewise unchanged.

Both confidence powers remain:

\[
 \left(\frac{\log(CN/\alpha)}{N}\right)^{\vartheta\omega/(4\omega+\Gamma)},\qquad
 \left(\frac{[\log(C_0B/\alpha)]^2}{B}\right)^{\vartheta\omega/(12\omega+\Gamma)}.
\]

The first refers to the calibrated policy, the second to the complete calibration-inclusive budget. Their target remains the complete local analytic contact pair on a smaller disc. They remain constructive upper bounds for the specified observation policies, not minimax exponents. The new periodic-itinerary law is not inserted as an unproved substitute for the original alternating-channel statistical interface.

## 4. R63-M4, M5, S1 and D3: normalization, realizability and analytical scope

We retain the distinctions the report expressly credits: independent preparation count versus successful marks; conditioning on the binomial count versus an arbitrarily stopped stream; outside-category retention; measurable approximate realizable-image selection versus a finite computational algorithm; and finite-bridge density versus its limiting factorized law. The histogram is not differentiated or assumed realizable. The inverse acts only after fitting a realizable law and obtaining the required real control.

The finite-density normalization floor, charged physical success probability, actual-smooth stationary envelope, complete local analytic inverse, and prior-dependent smaller-disc estimate are all preserved. The analytic prior is not inferred from the observed finite record. Neither the new forward extension nor the retained local statistical theorem claims a new global quantitative reconstruction from finitely many observations. All previously proved exact global and conditional global results remain under their own hypotheses.

The new proof follows the report's emphasis on the relative determinant rather than a dimension-times-operator-norm argument. Its trace-norm estimates use entrywise summability of the localized geometric perturbation; the Green comparison retains the boundary reflection and opposite-end terms. The original proof remains printed as well. No fresh certification of all inherited proofs is asserted.

## 5. R63-L1, L2 and D2: literature and attribution

The shared published-theorem comparison `article/00d_orbit_local_comparison_v63.tex` and both inherited bibliographies are unchanged. The published Zelditch comparison remains a comparison of hypotheses and observation maps, not a reduction between a full spectrum and endpoint laws. The internal realized leading-data comparison is not promoted to equal full spectral data.

The refreshed primary records still distinguish the enriched marked-length datum in Finamore--Leguil, the analytic open-billiard setting and symmetry assumptions in De Simoi--Kaloshin--Leguil, and the removed geometric claim in Florio--Leguil's version-5 notice. See `LITERATURE_CHECK_V64.md` for the precise scope of this record check. We do not infer an exhaustive priority claim for the new geometric extension from that check. The ordinary tools in the proof—positive Jacobi recurrences, contraction, trace-class continuity and scalar linearization—are not claimed as newly invented general techniques.

## 6. Retention and reproducibility

All 784 inherited source paths are present. Of these, 779 are byte-identical; the five modified files have byte-exact originals under `history/v63-review-baseline/`. The modified files are the two entry points, their two introductions and the manuscript README. All 127 inherited active inputs remain; the two shared v64 inputs bring the active union to 129. The original two-collision companion is unchanged.

`tools/check_revision_v64.py` checks this retention and the complete unchanged statistical module, 360 exact rational transfer/cofactor cases, actual oblique three-disk Hessians, 32 two-ended geometric bridge comparisons and six restored-gauge checks with negative controls. It uses no removable assertions and produces identical output under ordinary and optimized Python on the checked toolchain. The numerical tests are finite diagnostics, not rigorous substitutes for the proofs.

The retained immutable-source builder compiles all three complete entry points, supplies producer-matched external auxiliaries and records actual source consumption. Final source commit, manuscript tree, native products, build findings and actual selected-page inspection coverage are identified in the repository-root `A2_REVISION_V64_INDEX.md` and delivery records. Compilation and source identities do not establish exceptional significance or certify every theorem.
