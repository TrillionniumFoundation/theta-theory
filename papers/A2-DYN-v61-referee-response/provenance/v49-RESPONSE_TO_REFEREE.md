# Response to the external referee: A2-DYN revision 49

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v48-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Review commit / blob:** `3c8a41dd89f8491ac85c1ba40d85c68dc040e6dc` / `931f8f23563434275fb6d02b7077bfccda740954`.  
**Reviewed author commit:** `418000c216e9efa7c259a9bee9dac4fcf288ee1d`.  
**Frozen full paper tree:** `8918ca0a31f4966750326217f15b79ad71ba6df7`.  
**New article:** `papers/A2-DYN-v49-referee-response/main.tex`.

We thank the referee for isolating the two genuinely physical sources and for recognizing the all-depth decision argument. This revision uses the actual remotely qualified v48 source, not the older local draft previously circulated. It retains the same title, model, exact return record and pointwise arithmetic raw target. It adds a complete density-norm theorem on the unmodified source. No small-mass assertion is relabelled as a pointwise estimate.

## R1. The physical residual criterion

Modules 105--107 establish a new local-variation bound for the whole physical remainder, including every incidence and clearance depth, and then a full-source arithmetic density local limit in that norm. For every fixed roof length h, uniformly in all translated windows and the exact n,k,m labels,

`(1/h) integral_[t,t+h] |m^2 p_n(k,m,u) - L_(m,R)(k,u,n)| du -> 0`.

This is stronger than an interval-probability statement: the absolute value is taken before integration. Equivalently, every bounded measurable roof selector supported in the interval is allowed, even when chosen after m. The proof also yields total-variation convergence of the central mixed measure at a fixed return index and of the exact-window conditional roof law under a positive transition denominator.

The essential-supremum criterion in equation `eq:v48-physical-residual-criterion` is not thereby proved. Narrow roof spikes are compatible with local L1 convergence. That original target is retained verbatim in the compiled inherited module 104 and continues to govern the pointwise raw theorem. The new norm result is an additional theorem for the same full measure, not a replacement definition of that target.

## R2. Grazing control

The incidence event `cos(phi)<s` is handled in the original collision angle, without an inverse p-to-phi coordinate change at grazing. It is a pair of angle bands of width at most 2s. Stable slopes are bounded away from zero, so every homogeneous stable curve has a bounded number of intersections of length O(s), including the strips accumulating at grazing.

The piecewise multiplier criterion gives a uniformly bounded strong multiplier; the stable length normalization gives a strong-to-weak gain s^(1/8). The existing moving-peak interpolation then gives an exact-coefficient local gain s^(1/16), uniformly in the marked collision and the strip width. This estimate applies to the actual nearly grazing trajectories; it neither reflects a ghost trajectory nor changes their collision count. It is a new finite-band Fourier/local estimate near the physical singularity, not a pointwise seam-transport theorem.

## R3. Competing-hit clearance control

A clearance defect of flight j is observed at collision j+1 from the preceding incoming flight. If q=R n_alpha is that image contact, v^- the backward incoming unit velocity and d a candidate nonincident center, set

`L_d=(d-q).v^-`, `Z_d=(d-q).(v^-)^perp`.

The physical small-clearance event is contained in the positive upper envelope `L_d>0, R<=|Z_d|<=R+s` over a fixed finite candidate set. The foot is uniformly separated from zero. The exact derivatives are

`partial_r Z_d = -cos(phi)-L_d/R`, `partial_phi Z_d=L_d`.

Hence its boundary slope is `1/R+cos(phi)/L_d>0`, transverse to the negative stable slopes. Fixed partition complexity and uniform matching estimates are verified before the multiplier criterion is invoked. The clearance observable is not incorrectly inserted at the forward flight's initial state, where its singularity orientation is different.

This controls both physical sides through the actual orbit integrals; it does not identify their actions, Jacobians or arithmetic phases across a seam. Each side retains its own exact labels. The positive envelope is used only for an upper bound. There is no cancellation claim between differently labelled branches.

## R4. Ordered parameter ledger

For arbitrary bounded source insertions, the summed physical estimate is

`m^2 ||b^(epsilon,w)||_(1,h,loc) <= C M epsilon^(1/16)(h+B_*^(-1)) + C_(B_*) M(1+B_*h)m^3 rho_(B_*)^(m/2)`.

The mark and width can vary with m; the finite-count error cannot. There are 2m+1 physical marks and at most four at each depth. The geometric leading terms and finite errors are summed before the collision limit. A first-defect tail above J gains `(47/53)^((J+1)/64)`.

For the signed reconstruction correction, convolution contracts the local L1 norm up to `||K_1||_1`; positivity of K is not assumed. Combine this bound with the previously proved protected and all-depth decision corrections. With `epsilon(B)=A B^(-1/12)` and `A^12>=C_2`, the full local-variation correction is `O(B^(-1/192))` in collision limsup. First fix reconstruction B and its margin, then take the collision limit and enlarge the auxiliary band B_*, and finally let B grow. This is not a rate in m and not a substitution B=B_m in a fixed-band spectral theorem.

## R5. Arithmetic main term

The exact transition kernel `mathcal L_(m,R)` is retained uniformly through arithmetic transitions. At fixed radius the factor is `c mathfrak a_R(k,n,m) g_(Omega_R)`, with the unchanged conversion to the D_R return normalization. No arithmetic residue is assumed zero and no finite occupation packet replaces a target coefficient. The new conditional theorem uses a positive-part transition mass bounded below; it does not normalize a zero arithmetic class.

## R6. Weighted and conditioned assertions

The physical remainder bound permits every measurable source insertion of modulus at most M by Radon--Nikodym domination. The full weighted correction theorem additionally retains the inherited protected endpoint-gradient budget. No Gaussian amplitude is assigned to an arbitrary trajectory selector.

The unweighted density theorem is dual to arbitrary measurable selectors of the roof variable on a fixed interval. It gives total-variation convergence of the exact conditional roof law on the unchanged K_n=k, N_n=m, T_n in [t,t+h] event. The probability-distance convention is one half of the variation norm; the normalization estimate is written explicitly. A path conditioned at the single roof equation T_n=t still requires the original pointwise estimates and is not asserted here.

## R7. Independent verification

No independent human specialist audit has been obtained. `SPECIALIST_AUDIT_MAP.md` states the new continuum checks and the inherited spectral dependencies. The new finite diagnostics test exact signed-distance derivatives, finite transversality samples, mark shifts, depth and error sums, signed convolution inequalities and conditional normalization. They do not establish a continuum multiplier theorem or certify any inherited spectral argument. The native build and exact-source receipt have the same restricted evidentiary meaning.

## R8. Theorem-level novelty comparison

The new conclusion is not obtained from a fixed-interval local limit by differentiation. Uniform local total variation allows the bounded roof test to be selected after m and controls the original unsmoothed density, including physical defects. The additional input is the image-side physical-layer geometry, spectral weak-smallness estimate, all-depth local control, and protected density regularity. General mixing local limits, anisotropic spaces and suspension local limits remain attributed to the cited literature. No unverified historical-priority or venue-acceptance claim is added.

## R9. The principal reading route and preservation

The front matter now states one new leading density-norm theorem and its three-section proof route. All eleven preceding leading statements and their proofs are compiled in an appendix; the only textual adjustment there replaces an obsolete literal theorem number by its label. The full v48 introduction remains archived under provenance. All 104 inherited core files, all 131 inherited Python scripts, the bibliography and the A-X synopsis are byte-identical. All inherited mathematical labels remain compiled.

The original return-density program is neither deleted nor detached into a different topic. Its pointwise criterion remains visible in the new introduction and is distinguished from the newly proved norm theorem.

## Technical comments and source qualification

The new sections distinguish m,n,B,B_*,epsilon,h and the defect depth. The ambient factor 1/c is written whenever section endpoint constraints are dropped on the upper side. Occupation still counts 0,...,m-1; a clearance mark at m adds no terminal occupation. No upper-comparison event is averaged into the target coefficient. The strong bound and weak gain of the multiplier remain separate; the inherited square-root interpolation is used only on its stated moving-peak neighborhoods. The finite-count physical remainder is m^3 rho^(m/2), whereas the unchanged decision theorem retains its own m^4 remainder. All-band assertions use convolution norms, not growing-band spectral constants. The norm result is not called a pointwise density theorem.

Both new revision branches start from the exact controlling review. The read-only workflow checks the baseline tree, current report blob, all preserved source, compiled label retention, the ordinary payload Merkle tree, normal/optimized diagnostics, native build and theorem-page renders. Dynamic receipts carry the actual event SHA and run ID. No execution or human proof audit is predeclared successful in this response.
