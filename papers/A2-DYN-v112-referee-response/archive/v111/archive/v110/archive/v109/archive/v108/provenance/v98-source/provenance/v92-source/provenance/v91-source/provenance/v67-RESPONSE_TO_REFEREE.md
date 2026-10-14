# Response to the external report on A2-DYN revision 66

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**New revision:** 67, 10 October 2026.  
**Controlling report:** `reviews/a2-dyn-v66-external-top4-review-2026-10-10/REFEREE_REPORT.md`.  
**Report commit / blob:** `31eae1cab4ac138d0d9c892cb76c63286cb73307` / `e3e06c75e0b6a73b613c944223423c0dc03b3854`.  
**Reviewed author commit:** `e96761c0b12dbc46c187f4aeb4ee8d537863dec5`.  
**Frozen complete paper tree:** `fdf737e94888a540c05d86c458d77b500895e713`.

We thank the referee for identifying the distinction between a finite-width physical collar trace and the zero-width physical coefficients. We agree that fixed-count dominated convergence does not settle the ordered angular loss, and that a positive subset of the source cannot stand for the complete essential height. The revision addresses the first passage by a new relative angular estimate and positive absorption. It also proves an actual essential-height bound for the resulting caustic collars. The full original pointwise problem, including its exact labels and arithmetic factor, remains the objective.

## 1. The new mathematical step

For every normal critical clearance-seam chart satisfying the inherited incidence taper, choose a disk on which the complete physical and section margin description is verified. For a scalar margin write

\[
b_f=f(0),\quad A_f=|Df(0)|,\quad L_f=\tfrac12\|D^2f\|_\infty.
\]

The inactive-sign radius `rho_z` includes both that description radius and the offset bound `|b_f|/[2(A_f+L_f bar_r_z)]`. The active budget is

\[
\kappa_z=\sum_{b_f=0}L_f/A_f,
\qquad
\mathfrak a_{z,\lambda}=\max\{\rho_z^{-1},\kappa_z/\theta_{z,\lambda}\}
\]

for positive physical angular fraction `theta`. An active homogeneous sign can differ from its tangent sign only where `|Df(0) dot omega| <= L_f r`; its angular fraction is at most `L_f r/A_f`. Inactive signs do not change below `rho_z`. The Boolean output vectors are zero or one-hot, so the error is charged to the input margins, never to the number of output labels. This gives

\[
(1-K\sqrt{2u})\theta_{z,\lambda}
\le a_{z,\lambda}(u)
\le(1+K\sqrt{2u})\theta_{z,\lambda}
\]

on the explicit stratum `mathfrak a <= K`. The source remains nonlinear and physical; tangent signs supply only the reference fraction.

The lower physical profile now gives a positive estimate **before either limit**:

\[
\mathcal B^K_m(I)
\le\frac{\exp(K_\chi\sqrt{2s})}{1-K\sqrt{2s}}\mathcal Q^K_{m,s}(I).
\]

Take the collision limsup with `s,K,chi,epsilon,h` fixed, apply the inherited two-strip collar bound, and then let `s` decrease to zero. The result is

\[
\limsup_m\sup_{R,\lambda,t}m^2
\mathcal B^K_m([t-h,t+h])\le2Ch.
\]

The constant is independent of `K`; convergence is not claimed uniform in `K`. The upper physical profile also proves

\[
\limsup_m\sup_{R,\lambda}m^2\|b^{K,H}_{m;\lambda,R}\|_\infty
\le CH\exp(K_\chi\sqrt{2H})(1+K\sqrt{2H}).
\]

This is an ordered essential-height estimate on a specified part of the original clearance source, not a mass or finite-width surrogate. No concentration theorem for the full reversible trace is assumed.

## 2. Response to the nine required changes in Section 20

### 20.1. Prove the angular-loss estimate

**Advanced, with the full-family tail still explicit.** Module 143 proves the relative angular estimate from every primitive physical and section margin. Module 144 proves the ordered angular loss on every fixed finite-jet stratum:

\[
\limsup_m\sup m^2\mathcal D^K_{m,s}([t-1,t+1])
\le\tfrac43 CK\sqrt{2s}.
\]

Module 145 defines the positive physical tail `E(K)` of the coefficients `J_z theta` with `mathfrak a > K` and proves

\[
\limsup_m\sup m^2\mathcal D_{m,s}([t-1,t+1])
\le\tfrac43 CK\sqrt{2s}+E(K).
\]

Thus `E(K) -> 0` is a concrete sufficient weighted-tightness condition for the complete seam-chart angular estimate. It is not asserted as established. We do not exchange fixed-count exhaustion with the collision limit merely because every individual condition number is finite. An optional moment criterion is proved only as an implication; no unrestricted polynomial rate is attached to it.

The new statement is stronger than the preceding fixed-word profile and finite-width trace: it establishes zero-width concentration and essential height on explicitly verified Lorentz strata. It does not relabel the full remaining angular estimate as proved.

### 20.2. Control the positive chart complement

**Not yet closed.** The revised positive partition is `b^{epsilon,clr} = b^{K,H} + r^{epsilon,chi,K,H}`, with `r >= 0`. The new first term has an essential-height bound. The second retains failed incidence taper, selected grazing, noncritical rank components, non-seam critical centers, zero-tangent-fraction labels, large-condition strata and every omitted annulus. Its full ordered essential height remains to be estimated. In particular a zero tangent fraction does not justify deleting the nonlinear source; a finite negative-control fixture demonstrates this distinction.

### 20.3. Complete the first-incidence height

**Not yet closed.** The incidence-normalized contact inverse and finite-count coarea results remain intact. The new angular theorem concerns a clearance-seam source on which the incidence guards are already one. It therefore cannot by itself prove the complete first-incidence height. The manuscript states this explicitly and retains the incidence term in the positive raw-error identity.

### 20.4. Complete the clearance height

**A new essential-height component is proved; completion still requires the positive remainder.** Corollary `v67-collar-height` controls the exact nonlinear density, almost everywhere in the roof, on the good caustic collars. It is combined with the nonnegative remainder in equation `v67-complete-height-budget`. Transverse, finite-type, buffered-caustic and other inherited routes remain compiled and are not treated as a complete partition with an already estimated remainder. A weighted atomic tail estimate alone would not estimate the nonlinear remainder height.

### 20.5. Deduce the unrestricted pointwise theorem

**Target preserved; not newly claimed.** The unrestricted two-sided arithmetic raw-density statement remains displayed in the introduction. The complete positive incidence and clearance estimates remain the inputs of the existing raw-error representation. The fixed reconstruction band is chosen before the collision limit. The finite arithmetic transition kernel, damped residues and zero classes are unchanged; no unmodulated Gaussian statement is substituted.

### 20.6. Derive unrestricted same-roof consequences

**Logical dependence retained.** Unrestricted same-roof collision and actual-return bridges, forward essential likelihood and the unrestricted pointwise roof-conditioned path statement are not promoted on the basis of the stratum result. Existing integrated, local `L^q`, good-set and finite-width conclusions retain their exact prior scope.

### 20.7. Obtain independent specialist review

**Not obtained in this revision.** The new proof and precise source dependencies are exposed for such review. We do not describe AI-assisted derivation, deterministic fixtures, two branch runs or TeX compilation as an independent human audit. Priority checks are the complete margin description on the chosen disk, inherited guard saturation, relative source normalization, the positive subfamily comparison, and the order of the three limits. The inherited billiard and anisotropic-space inputs still require specialist scrutiny.

### 20.8. Reduce the proof burden

**Implemented without deleting mathematical content.** The introduction states the two new leading results and the full target. Modules 143--145 form a short self-contained logical spine, with explicit citations to inherited inputs rather than reproducing their entire development. Historical leading material is compiled verbatim in a marked appendix. The response, qualification details and status ledger remain separate repository documents. All 142 inherited core modules, 194 Python files, six appendices, bibliography and previously compiled labels are retained byte-for-byte or, for the replaced leading material, verbatim in the appendix and full-main archive.

### 20.9. Sharpen the literature comparison

**Implemented at the level of the actual conclusion used.** The end of module 145 distinguishes the weak mixed local limit of Szasz--Varju, the cell-index endpoint local laws of Demers--Pene--Zhang, and suspension local-limit formulations of Dolgopyat--Nandori from the present geometric passage to physical zero-width coefficients. The original statements were checked, not inferred from titles. The argument here uses the already established exact-occupation/displacement two-strip law at fixed width and then proves a separate relative absorption. It does not differentiate an interval law. None of those cited formulations is claimed, without further hypothesis verification, to supply the physical condition-number tail or the complete positive density remainder. No claim of a new general theorem for all singular hyperbolic systems is made.

## 3. Technical comments in Section 21

Comments **1--4, 17--20, 28**: `Q`, `B` and `T` remain distinct. All inner and outer limits are stated. Positive loss is retained, coincident values add, endpoint strip width is `O(sqrt(s))`, roof width is `2h+s`, and no word-count factor or unconditional rate is inserted.

Comments **5--8, 15--16, 22--23, 26--27**: the full physical Boolean input vector is used, with initial membership, occupation at `0,...,m-1`, terminal membership at `m`, original image mark `j+1`, original half-word labels and no primitive-period division. No nonphysical continuation receives probability. Label sums use the pointwise one-hot bound. Guard saturation is used on the physical part only. Arithmetic zero classes and the distinction between probability total variation, variation mass and the path dual are unchanged.

Comments **9--14, 21, 24--25**: the Morse disk is a coordinate disk under the original incidence taper, excluding selected grazing. A separate verified Boolean-description radius is now included in the condition number. Disjointness is not completeness. Density control is relative, not an absolute lower bound on `J_z`, and retains the reversible square root. All densities use common coarea representatives and essential norms. The positive outside source is displayed; no small-mass argument replaces its essential height.

Comments **29--30**: source qualification and mathematical verification are separated in all active metadata. The new branch-specific workflow records the exact checkout and both frozen baseline/review objects. Two branch runs, when completed, are separate reproducibility executions, not independent mathematical reviews. Actual run conclusions must be read from GitHub; this response does not predeclare success.

## 4. Preservation and validation

The new directory begins as an exact Git-tree copy of the reviewed paper. The old directory and all review reports are unchanged. The source checker verifies every inherited core file, Python file, appendix, bibliography item source, compiled input and label, as well as the complete baseline tree and qualification-workflow hash. Replaced metadata and the complete old main are archived separately.

New deterministic fixtures check homogeneous threshold geometry, inactive offsets, near-coincident normals, one-hot exact-label partitions, positive absorption, the Cesaro factor `2/3`, coincident atoms and the conditional moment exponent. Negative controls reject four invalid shortcuts: bounded absolute jets without gradient control, inactive offsets without a stability radius, deletion of zero-tangent-fraction nonlinear source, and reversal of the fixed-width/collision limits. These are finite diagnostics, not verification of the complete billiard dynamics or of `E(K) -> 0`.

The revision offers the new positive stratum results and the explicit remaining estimates for another substantive review of the same paper and objective.
