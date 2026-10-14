# Response to the external referee: A2-DYN revision 65

## Manuscript and frozen documents

We thank the referee for separating finite-count geometric estimates from the ordered essential-height requirement. The subject and the unrestricted arithmetic pointwise target are unchanged. This response addresses the latest located external report, `reviews/a2-dyn-v62-external-top4-review-2026-10-10/REFEREE_REPORT.md`, blob `4d0a4e354df2b7f7b14667332b0a40c2c959160f`. Its reviewed manuscript is author commit `45425f65832e3f1e69336c791de5fc32f8ed22bb`.

Revision 63 at `ae14ecbfa39d0d9005574155de86acecd2e8a166` is incorporated without deleting its mathematical content. The later v64-named branch pointed to this same v63 manuscript when inspected. We therefore issue a separately identified revision 65, with three new complete modules, a new leading theorem, and an itemized response. The author revision is available for further referee review; it is not a claim of acceptance or an external referee report.

## Substantive mathematical changes

**Module 137: reversible critical weights.** The generating equations in canonical endpoint arclength and momentum give `bc = det(H)/(F_uv)^2`. Reversal closes a regular normal-to-normal half-word and gives `P = S M^{-1} S M`, with `det(I-P) = -4bc`. With the original section normalization the quadratic coefficient is

`J_z = 1/(R c_* sqrt(|det(I-P_z)|)) = (R c_*)^{-1} lambda_z^{-1/2}/(1-lambda_z^{-1})`.

The determinant is a square root, not the ordinary inverse determinant of a periodic-orbit trace. We also prove the uniform comparison with a normal-section crossing weight and the individual exponential bound without imposing an interior incidence margin. The half-word labels are not read from the doubled orbit, the period need not be primitive, and no cyclic quotient or period divisor is inserted. At a competing-hit seam, `P_z` is explicitly the physical-side branch expression, not an asserted derivative of the singular billiard map.

**Module 138: density inside a simple roof-critical clearance seam.** For the actual one-sided strip `0<g<s` at a nondegenerate roof minimum, the density is

`(J_z/pi) asin(min(1, s/(kappa_z sqrt(2h)))) + O_z(J_z h^(1/4))`.

The estimate is uniform across the width-to-roof transition, including its threshold. It is obtained directly from the original source by Morse coordinates and polar coarea. Its one-sided coefficient is `J_z/2`, not an estimate inferred from tube mass. The existing smooth first-clearance source is sandwiched between the strips at its own widths `epsilon e'_j` and `2 epsilon e'_j`. A positive weighted-cluster bound retains coincident critical values and the complete source outside the selected neighborhoods.

**Module 139: affine profiles for multiple seams and every exact section decision.** A width-uniform Stieltjes comparison for the inherited monotone guard permits all clearance first jets to be retained with their nonzero constant offsets. A Boolean evaluation of the original section visits preserves occupation at times `0,...,m-1`, with terminal membership at `m` separate. The summed error over all exact labels is at most `C_z J_z h^(1/4)`, and the explicit affine angular profiles have total angular mass at most `2 pi`. There is no target-count factor. Multiple active seams, coincident boundary gradients and section junctions are permitted as long as each retained scalar margin gradient is nonzero and all selected incidences stay positive in the local disk. The error constant is expressed through first and second margin jets and the relative density derivative in equation `eq:v65-jet-budget`.

These are calculations on the original circular Lorentz collision graph. The numerical fixtures test their algebra and generic local profiles; they do not certify the existence of a particular new Lorentz caustic or the uniform long-count coverage needed below.

## Replies to the major requests

### 30.1 — Ordered incidence essential-height limit

The first-incidence source and its original depth weights remain unchanged. Module 131's finite-count estimate is preserved with its exponential count factor. The new reversible identity controls actual individual critical coefficients without a lower interior incidence margin, but it does not estimate the complete first-incidence density at the central `m^{-2}` scale. The requested order remains `B` fixed, then `m -> infinity`, then `B -> infinity`. We have not substituted a rapidly growing `B(m)` or marked this ordered limit proved.

### 30.2 — Full clearance source, including the retained caustic

Modules 138 and 139 enter the retained caustic rather than discarding it. They calculate a local roof-critical source which is not in a nonzero roof-pivot carrier. The general affine formula includes multiple competing seams and section junctions and retains every exact label. The original smooth guard and its first-defect partition are used before pushforward. Inside an incidence-capped local disk all incidence factors are one, so the sum of the original first-clearance pieces equals the full physical defect there; no pieces are reclassified by an artificial trajectory.

The simple angular coefficient and the general angular trace are multiplied by the reversible weights from module 137. The positive source outside the selected neighborhoods remains in the exact decomposition. Selected grazing contacts and noncritical-roof rank degeneracy are not assigned the roof-minimum profile. Accordingly the complete ordered clearance-height limit is still a separate required estimate, not a consequence claimed from the local formula.

### 30.3 — Quantitative dependence and useful geometric data

The buffered finite-format budgets in modules 135 and 136 are retained unchanged. The new profile comparison instead gives a finite-jet budget `C (1+W_z+sum_f sqrt(L_f/A_f))`, with every derivative, norm and positive denominator specified. Its constant is independent of the individual guard widths, including exponentially depth-weighted ones. Affine offsets avoid the unjustified assumption that a fixed band makes epsilon smaller than every nonzero clearance margin.

This does not assert a count-uniform lower bound for all margin gradients, a common Morse radius for every long word, or a long-count critical-cluster estimate. Uniformity on a compact family of neighborhoods with the stated common bounds follows directly from the proofs. The missing passage from local geometric data to all long words is visible in the compiled text.

### 30.4 — Full pointwise law and arithmetic transitions

The original pointwise target, the signed canonical finite arithmetic kernel, transition residues and zero classes are retained. Every one of the inherited A–X statements and all 1809 baseline mathematical labels remain in the compiled manuscript. The new leading theorem states only the reversible identity and the proved local source profiles. The full pointwise roof-density local law has not been toggled to proved in the manifest.

### 30.5 — Exact-roof consequences

No exact-roof bridge, singleton conditional law, or essential likelihood convergence is inferred from the finite-jet profiles alone. The inherited integrated results remain in their stated norms. The scalar positive-source height condition is still required for the corresponding unrestricted pointwise consequences, with a genuine nonzero arithmetic denominator wherever conditioning is asserted.

### 30.6 — Specialist audit

The revised specialist map isolates reversal signs, the factor four in the determinant, the square-root weight, boundary branch interpretation, the polar Jacobian, affine threshold uniformity, and the exact occupation Boolean formula. All have proofs in the manuscript and separate finite diagnostic checks where appropriate. Neither this author response nor the build log is represented as independent human specialist review.

### 30.7 — Principal mathematical contribution and presentation

The manuscript does not change its principal problem, discard content, or replace the physical source by a realization. Three new sections, a leading theorem and a compiled dependency route expose the actual additional mathematics. The full historical derivation remains available and compiled. We have not represented a local calculation as the unrestricted endpoint.

### 30.8 — Theorem-by-theorem comparison with existing methods

The action–monodromy principle and reversible Hill theory are classical; Bolotin–Treschev is added as a primary reference, and the exact two-dimensional identity is proved rather than attributed as a new general theorem. The Morse-coordinate arcsine profile is an elementary coarea calculation. The paper-specific content is its original Lorentz normalization, the physical-side interpretation, the unaltered first-clearance guard, the positive half-word weight sum, and the affine profile for the original exact-label vector. The inherited fixed-window local law is not silently upgraded to a transverse trace theorem. The conditional ordered trace transfer identifies that extra input explicitly.

## Technical comments 31.1–31.21

The revision keeps separate names for the band, strip width, roof distance, incidence cap, collision count and monodromy entries. Physical derivatives are taken along the full original two-sided roof. The clearance witness is always read at collision `j+1`; incident disks remain excluded. All later incidences are checked in the local cap, and no first-defect transition region is dropped. Simple-root extensions and affine sign patterns carry no new source probability.

The new local profile does not assert a globally bounded finite type or fill a physical seam. Each scalar margin derivative is justified separately, and no determinant of two boundary gradients is assumed nonzero at a multiple seam. All positive complements remain explicit. Exact-label variation is bounded through a partition of the source and a pointwise label-vector distance of at most two, not by multiplying an estimate by the number of labels.

Mass, tube length, pointwise height and critical atomic trace remain different quantities. The finite-count normal-strip trace takes its small-strip limit at fixed `m`; the fixed-width local theorem takes its long-count limit at fixed strip width. The two limits are not exchanged. Variation uses the full-mass convention; no hidden factor one half is introduced. Arithmetic signs and zero classes are unchanged. Density identities are stated almost everywhere with coarea representatives for one-sided traces. Source checks and finite fixtures remain distinguished from continuum proofs and specialist review. The compiled modules include the dependency route and the exact remaining dynamical inputs.

## Status after this revision

Proved locally in the manuscript: reversible critical-weight identity; crossing-weight comparison; individual count decay; simple width-uniform seam profile; original guard sandwich; positive cluster bound; affine exact-label profile at multiple capped roof-critical seams; finite-jet error budget; angular boundary traces.

Conditional only: transfer from an independently established uniform reversible-weight concentration estimate and verified neighborhood coverage to ordered local height removal.

Not claimed closed: the complete ordered incidence and clearance height limits, the unrestricted two-sided pointwise roof-density local law, or its unrestricted exact-roof conditional consequences. These remain the same target of the paper rather than being replaced by a weaker subject.
