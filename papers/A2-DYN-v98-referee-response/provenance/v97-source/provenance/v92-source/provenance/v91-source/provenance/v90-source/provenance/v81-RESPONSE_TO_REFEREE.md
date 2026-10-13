# Response to the external report on A2-DYN revision 79

**Author:** Qian Qi. **Revision:** 81, 11 October 2026.

**Controlling report:** `reviews/a2-dyn-v79-external-top4-review-2026-10-11/REFEREE_REPORT.md`, commit `6764d25a4e3aaeb826d4ec24a12a55d16989d9e2`, blob `dd7a2e7ee91757cdb253eaf8e605cd330ca11e3f`.

**Preserved author baseline:** v80, commit `d05c5ed180fb0e0a9488700e30523dc336fef00a`, paper tree `36fd73cb74917dcd1af315fd9696ac3026ff7bab`. At task initialization v79 was the latest visible external report and v80 was already an author response. We continue that response rather than overwrite it or describe it as a new external review. All 185 inherited core modules and the complete v80 article are preserved.

We thank the referee for requiring quantitative estimates on the original exact-label source. The new argument combines both endpoint momenta and an internal incidence in one characteristic pairing. It yields a critical-width exponent strictly greater than one simultaneously with an incidence exponent greater than one. Positive layer cake then gives actual untruncated fractional mixed insertions and a first inverse-gradient estimate with a fixed lower cutoff whose leading constant is independent of that cutoff. On the original coarea survivor graph this improves the all-incidence optical/grazing height from `C r/a` to `C r`. It also pays the nongrazing pullback drift with the same uniform constant. The initial critical tail and outgoing nongrazing flux remain explicit proof obligations. The title, topic, exact pointwise target, labels, normalization, original guard and full arithmetic reference are unchanged.

## 1. Complete true-exit height — request 1; report §§13–16

Theorem `thm:v81-optical-height` bounds genuine grazing *starting mass* together with surviving optical loss by `C r` in the ordered collision-normalized roof norm, for every previously fixed initial cutoff `a>0`, with a constant independent of `a`. For starting states in `a<=|g|<b`, it gives the sharper annular estimate `C r (b^2+2 Lambda_circ r)^(delta/2)`, where `delta=1/128`. The target remains the same exact event up to its true first exit. Vanishing boundary optical density is not used to discard positive initial mass.

The nongrazing theorem retains the one-sided outgoing flux and its backward lifetime. Its compression cost is paid by the mixed volume insertion instead of bounded by `1/a`. This is a quantitative improvement, but not a bound for the entire outgoing surface source. The full true-exit flag is therefore not promoted. Simultaneous failures keep the disjoint grazing/nongrazing classification already made in v80.

## 2. Complete inverse-twist height — request 2; §§10–12 and 15.2

Module 186 proves the joint local estimate with critical-width exponent `alpha=129/128` and incidence exponent `beta=17/16`. The characteristic pairing retains both endpoint tests, the internal mark and the exact occupation coefficient. The two chronological cases are proved separately; time reversal is not used to alter the occupation convention.

There are two important safeguards. The small strong norm `||1_{|p|<b}|| <= C b^(7/8)` is a statement about a particular vector, not about an arbitrary small-norm multiplier. A peak vector is localized using a physical unit-modulus peripheral vector with a nonzero smooth test, rather than by dividing by `Pi 1`, which can vanish at a nontrivial arithmetic peak. Every real-frequency cap is retained before Fourier extraction.

Module 187 integrates the capped incidence estimate before taking limits. Its finite-count critical-volume remainder is `C_B m^2 b^(1/2) rho_B^(m/4)`. It proves actual untruncated insertions `I_m |g|^(-eta)` for `0<eta<1/2`, and the first inverse power with fixed cutoff `a`. For that first power the leading bound is uniform in `a`, while the finite-count error contains `a^(-1/2)`. This distinction is not suppressed. Module 188 uses the retained inverse-gradient target weight to prove the complete fixed-cutoff optical/grazing bound `C r`, removing the former divergence `C r/a`.

The untruncated first inverse-gradient concentration theorem and the unrestricted optical height remain unproved. Uniformity of a limit bound over fixed cutoffs is not an exchange of the cutoff and collision limits.

## 3. Keep the mechanisms separate — request 3

The endpoint budget retains exactly the critical initial defect and nongrazing outgoing flux defined in v80. The newly paid optical drift is `C r`; it does not absorb a true positive exit into the signed occupation current. The unchanged guard and angular errors are separately bounded by `C_Theta (1+epsilon^(-1)) sqrt(r)`. No protected-word source or altered section is substituted.

## 4. Legal order of limits — request 4

The peak refinement is fixed independently of collision count and both localization widths. The incidence layer cake is completed with its physical cap before the collision limit. Fractional critical powers are integrated only in the range where both their leading term and finite-count remainder are integrable. The first inverse-gradient lower cutoff, roof width and Fourier band are fixed before the collision limit; the auxiliary band is enlarged afterwards. The outer reconstruction parameter is last.

The improved endpoint budget no longer requires `r(B)/a(B)->0` to control the paid drift. It still requires estimates of the two original residual heights and `(1+epsilon(B)^(-1)) sqrt(r(B))->0`. The fractional Abel comparison is stated as an extended nonnegative inequality, not as a pointwise consequence of fixed-width concentration.

## 5. Mixed-coordinate cubic calculation — request 5

The v79 stationary cubic identity and v80 normalization audit are retained verbatim and remain in the article. The current change uses their uniform endpoint Hessian bounds and radial speed, without modifying endpoint angles, internal arclengths or any factor of `R`. The critical localization is in `|g|=R sqrt(p_0^2+p_m^2)`; its comparison with two momentum strips uses the fixed lower radius `R_-`, explicitly. The distinction between momentum width and gradient width is stated in module 187.

## 6. Common coarea versions — request 6

The common-kernel lemma of v80 is retained in full. The new truncated target insertions are nonnegative Borel weights on its same injective survivor graph, so no new density representatives are chosen for different words or truncations. Fractional untruncated insertions use positive limits on those kernels. Target-direction covariance keeps the physical Jacobian, initial weight and exact displacement/occupation/terminal tests in their original roles.

## 7. Optical normalization — request 7

The identities `omega=|K_0m|/R=R c_0 c_m/y_m` and `J_h=(omega_h/omega_0)(chi_0/chi_h)` are unchanged and remain in the article. The new proof retains `|g|^(-1)` in the target source of the negative optical variation. It does not replace `J_h` by its inverse or equate boundary flux with initial source mass. All low-dimensional optical fixtures and normalization checks are preserved.

## 8. Exit exhaustion — request 8

The precompact rational flow-box exhaustion, the disjoint assignment used only for summation, and the monotone fixed-count first-exit limit are unchanged. New estimates apply before taking the positive source limits within the permitted truncated source. No uniform convergence in the collision count is inferred from that fixed-count exhaustion. The one-sided nongrazing boundary source is not estimated by a volume multiplier theorem.

## 9. Specialist review — request 9

No independent human specialist review or formal proof certification has been obtained. The updated audit map identifies the small strong endpoint vector, bounded transverse cuts, arbitrary peak normalization, two chronological amplitudes, doubly capped layer cake, target coarea transport and noncommutation of limits. The reference norm convention and multiplier criterion were checked against the primary Demers–Pene–Zhang source already in the bibliography. The broader four-record spectral statements remain explicit inherited repository inputs, not attributed to that reference. Finite fixtures and native builds are not continuum proof certificates.

## 10. Journal/supplement architecture — request 10

The article retains the full physical formulation and the eight immediately needed inherited modules, followed by three new theorem-proof modules. The complete v80 article is assembled in the supplement with a scoped reference wrapper that resolves its external supplement references inside the retained archive. Original files are byte-preserved. All 185 inherited core modules, Python sources, appendices, bibliographies and prior provenance are preserved; every top-level v80 file is additionally snapshotted under `provenance/v80-*`. Historical papers and review branches are not edited.

## Qualification and exact scope

The new workflow pins the v80 paper tree and controlling v79 report, checks preservation, normal/optimized diagnostics, full native article and supplement builds, actual coverage of all 188 core modules, stable references and PDF geometry. Its actual final-SHA runs, not successful baseline runs or the presence of a workflow file, determine remote source qualification.

The original scalar pointwise theorem and unconditional path, clock and likelihood conclusions remain the target. This revision proves a genuinely stronger complete fixed-cutoff transport estimate and actual fractional mixed insertions. It does not mark the critical tail, nongrazing surface height, untruncated first inverse gradient or full endpoint as closed.
