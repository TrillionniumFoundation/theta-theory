# Response to the external referee: A2-DYN revision 60

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v59-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Frozen review commit / blob:** `546a82be685897355e4918598f2d06847aa9f69c` / `72cc0cbaeafba69f070740ea5311c34148a12e59`.  
**Reviewed author SHA:** `69ab2afcceff0a8a2892910b335ac180678b5f4b`.  
**Frozen complete paper tree:** `7ca1775bcf25516a93fea04e834da38652f75687`.  
**New article:** `papers/A2-DYN-v60-referee-response/main.tex`.

We thank the referee for distinguishing the continuous-roof model theorem from the two physical Lorentz source heights. We retain the original title, four-coordinate actual-return record, full arithmetic reference, integrated theorem and unrestricted pointwise target. This revision addresses a specific substantive gap identified in Sections 17 and 20.6 of the report: moving pressure contact, pointwise density inversion and positive heights are now proved on the same nonzero perturbation family, not on separate parameter regimes.

## 20.1--20.4. The original incidence and clearance endpoint

The two Lorentz essential-height estimates are not proved by this revision. Their exact labels, positive first-defect source and next-collision clearance convention are retained. All inherited modules, including the positive raw-error representation and the canonical arithmetic reference, remain byte-identical. No source is discarded and no trajectory is continued across a competing-hit seam.

The new positive coarea criterion states explicit sufficient inputs with an auxiliary exact label. Applied at the Lorentz scale, it would require the wordwise derivative and positive conditional-cylinder estimates for those same physical sources. Neither the existing local variation bounds nor the new Markov estimates verify those Lorentz inputs. Thus the unrestricted pointwise Lorentz law, unrestricted same-roof consequences and forward essential likelihood are not promoted in the theorem statements or metadata. The finite arithmetic coefficient and its zero classes remain.

## 20.5. A reusable positive source-height criterion

New module `128_positive_coarea_criterion.tex` proves `prop:v60-coarea-height` by disintegration and a positive coarea sum. It separates two sufficient mechanisms. A cylinder-covered source requires a residual local strip bound after the cylinder is fixed; small cylinder mass alone is insufficient. An endpoint-localized source requires a joint exact-label interval envelope and a summable projected envelope; an unconditioned endpoint marginal is insufficient. The conditional coordinate density and coarea derivative appear explicitly. Auxiliary exact labels are never silently summed away.

The theorem allows countably many words, overlapping cylinder covers, bounded supported insertions and parameter-uniform constants. It is a sufficient source-height theorem, not a claim that its dynamical hypotheses hold for every singular hyperbolic system. The present application verifies it in the original correlated Markov family. Verification in multiple genuinely different non-Markov systems remains a further requirement for the breadth route proposed by the referee.

## 20.6. Moving contact and pointwise density on one family

This item is resolved by two new modules, with the proof summarized in a third introductory theorem.

`129_perturbed_markov_density.tex` retains both integer counts
`A_m = sum I_r` and `B_m = sum I_(r-1) I_r`. Their mean is `(3/7,2/7)` and covariance is `[[204,192],[192,198]]/343`. The two-variable Fourier matrix has no nonzero peripheral torus frequency: the 00 loop fixes the eigenvalue, the 10 edge equates the state phases, the 01 edge fixes the first frequency and the 11 loop fixes the second. This gives a full-lattice exact-state LLT with the terminal factor `pi_j`.

A separate small real tilt proves the positive Gaussian coefficient envelope, without using a signed LLT error. Summation along a bounded scalar strip then gives uniform anti-concentration for `A_m + epsilon B_m`, regardless of whether epsilon is rational, irrational or depends on m. Detailed balance and a suffix decomposition give a joint stable-interval estimate. Its positive Gaussian version uses depth at most `min(m/2,sqrt(m))`; the local-limit version sums transition weights, not the number of cylinders.

The original exact roof is
`3m + A_m + epsilon B_m + b_w - (1-a_w)y_0`.
The coarea derivative `1-a_w` is unchanged by the perturbation. The proof keeps it in every word. First summing over the integer A-count produces the same endpoint overlap `Theta`; the B-count remains in an explicit two-dimensional Gaussian lattice sum. The scalar arithmetic type therefore need not be frozen.

For every fixed `epsilon_0<1/4`, the resulting theorem is uniform for `|epsilon|<=epsilon_0`:

`ess sup_t |sqrt(m) p_(m,epsilon)(t) - g_(sigma_epsilon^2)((t-m bar_tau_epsilon)/sqrt(m))| <= C log(2+m)^(3/2)/sqrt(m)`.

The same rate holds with Lipschitz endpoint weights and their retained arithmetic profile, not a product of means. The two-count sum is first restricted by a positive Gaussian envelope; summing a uniform error over all m possible second counts would be invalid and is not done.

`130_perturbed_heights_and_contact.tex` proves all three original positive boundary heights uniformly on that same interval. Vertical and terminal stable strips have error `C(s+rho_0^floor(m/2))`; the initial-age argument has `C(s+rho_0^L_m)` with `L_m=min(floor(m/2),floor(sqrt(m)))`. Both age-side intervals and the full-word endpoint enlargement are retained. The estimates use only positive coefficient bounds. Central same-roof source probabilities follow by division by the independently proved density lower bound, for almost every original roof value.

Finally, for `epsilon=c_m/sqrt(m)` with bounded `c_m`, the actual fixed witness pair `exp(2 pi i y_0), exp(-2 pi i y_m)` has leading normalized density

`g_(204/343)(z) exp[-2 pi i(r_epsilon-(16/17)c_m z)] exp[-12 pi^2 c_m^2/119]`.

The conditional Gaussian variance is `6/119`. The last exponential agrees exactly with the pressure damping coefficient in the retained v59 theorem. Thus moving contact, continuous pointwise inversion and positive height control coexist in a genuinely nonzero parameter family. This does not identify the unweighted factor, which is one by triangle periodization, with the endpoint-weighted arithmetic factor.

## 20.7. Independent verification

No independent human specialist audit has been obtained. `SPECIALIST_AUDIT_MAP.md` separates the new two-variable Fourier, tilted positive envelope, joint cylinder and coarea arguments from the inherited Lorentz continuum obligations. Finite exact arithmetic and source checks are not proof certification.

## 20.8. Journal proof route and preservation

The two Lorentz introductory theorems remain unchanged. A third theorem states the perturbed density/height result. The direct additional proof route is modules 128--130, after the retained model definitions and pressure theorem. All 127 inherited core modules, all 171 inherited Python scripts, all compiled appendices and all 1,713 inherited mathematical labels are retained. Thirteen superseded front-matter and status files are archived verbatim. The bibliography is append-only. No other paper or old review is edited.

## 20.9. Literature comparison

The article retains the comparison with classical finite-state Markov additive density theory. It additionally cites the authors' companion material, which already includes a uniform compact-transition-matrix theorem. Neither a matrix spectral LLT nor compact-family uniformity alone is claimed as new. The new calculation within this manuscript is the exact joint-label projection across scalar arithmetic transitions, the deterministic endpoint coarea profile, and the positive original-source heights in the moving-contact family. The source-height criterion does not claim a new general mixing theory or an independently verified Lorentz realization.

## Technical comments 1--37

The original pi-weighted measure, detailed balance, coded-state correlations, positive roof range, physical operator and fixed witnesses are unchanged. The two-count theorem keeps terminal-state normalization and displays the full torus phase argument. It distinguishes the full-word endpoint from a suffix-cylinder endpoint, imposes all depth restrictions, and retains the coarea denominator and lower/upper inclusions. The proof exposes the Gaussian-tail truncation before summing local-limit errors. All three positive boundary sources and both age-side formulas remain separate.

The former restriction of the density theorem to epsilon=0 is now extended only through the new proved theorem; the old theorem remains unchanged. The weighted theorem covers the stated Lipschitz endpoint class. Arithmetic zero classes, signed references before normalization, probability TV as half variation mass, graph-coupled clocks, complete output selection events and the record-only observation restriction remain in the inherited source. Independent review and Lorentz pointwise status flags remain false. Reproducibility discussion remains in supporting documents rather than replacing mathematical proofs.
