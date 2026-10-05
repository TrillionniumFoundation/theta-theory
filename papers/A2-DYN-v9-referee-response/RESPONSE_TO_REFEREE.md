# Response to the referee on A2-DYN revision 8

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revision:** 9, 5 October 2026  
**Controlling report:** `reviews/a2-dyn-v8-external-top4-review-2026-10-05/REFEREE_REPORT.md`  
**Report commit / blob:** `9d1904397400529aae4a5d3cccede9081b4dfb33` / `17c4b2e9fac7fe8ec2dfa17caa2b43cb5b95f088`  
**Reviewed author source:** `36427a184ea256f0336fbc431dc76110a9b14592`

We thank the referee for distinguishing the genuine return-tail and renewal results from the missing analytical steps of the raw local theorem. We have kept the original topic, physical record, and density endpoint. The principal revision is a proof of Gaussian laws for the actual return process, not another conditional operator interface. Its construction bypasses an induced spectral expansion at low frequencies by compensating on the collision clock and stopping at the genuine return times.

The complete article retains all twenty-one inherited mathematical core files. Three new sections provide the new proofs. Four inherited files have expository updates: the final synthesis, the closing paragraph of the first-order clock section, the introduction to the stronger induced covariance criterion, and the common-renewal section. In the last of these the complementary projection is renamed, normalizations are recalled, the complex domain is clarified, and the compatibility diagram is added. All inherited theorem and proof environments are retained, up to the projection rename. Source chronology and validation prose remain in these supporting documents rather than being inserted into the proof flow.

## 1. The main new proof chain

In `core/22_collision_covariance.tex`, put `eta_R=1_(Y_R^*)`, `h_R=f_R-bar G_R eta_R`, and `c_*=nu(Y_R^*)`. The collision observable `h_R` is bounded and centered, although the induced record is unbounded. The finite-horizon collision root has uniformly bounded variation in the initial collision coordinates: in finitely many rational angular charts it belongs to a bounded semialgebraic family, and uniform slice monotonicity bounds its two distributional first derivatives. The moving section has uniformly bounded perimeter. This is an initial-coordinate BV statement, not a statement about the variation of an inverse coarea density.

Mean-preserving smoothing has `L^1` error `O(delta)` and `C^2` cost `O(delta^(-2))`. The existing smooth collision spectral splitting, combined with these estimates, gives exponentially summable correlations for bounded BV observables. It follows that the collision Green–Kubo matrix `Gamma_R` is absolutely convergent, has uniform exponential tails, and is continuous in `R`. A small-L1 residual has sum variance at most `C m delta(1+|log delta|)`, a bound needed to remove smoothing without an error growing like `sqrt(m) delta`.

In `core/23_stopped_gaussian.tex`, the genuine smooth collision twists have an analytic simple eigenvalue on a disk of radius proportional to `delta^2`. Its Hessian is calculated from the collision correlation series and its cubic remainder is bounded by `C delta^(-6)|z|^3`. Taking `delta=(1/4)m^(-1/13)` yields the stated `m^(-1/26) sqrt(log m)` characteristic estimate, including the section initial density.

The exact identity `J_(n,R)-n bar G_R = S_(N_(n,R),R) h_R` then transfers the estimate to the actual induced record. A return-count window bound and a dyadic maximal estimate control the stopping error without independence. Thus `D_R=Gamma_R/c_*` is the covariance of the actual Gaussian limit. Its zero directions are characterized by a genuine induced `L^2` coboundary, obtained from bounded collision-sum variances and a weak Hilbert-space limit.

In `core/24_functional_gaussian.tex`, fourth derivatives of the smooth spectral pairing give `E|S_m h_delta|^4 <= C[m^2+(m+1)delta^(-8)]`. A slower smoothing scale `delta=(1/4)n^(-1/32)` and a coarse grid of length `ceil(delta^(-8))` prove tightness, while the dyadic small-residual estimate removes smoothing uniformly on paths. Products of the chronological smooth twisted powers give joint, not merely marginal, Gaussian limits. The actual return-time functional law then gives the induced functional CLT. Finally, a linear compensation cancelling the mean induced record yields the unconditioned stationary physical-time joint fluctuations of lattice displacement and collision count.

## 2. Request A: actual anisotropic induced operator

The common-renewal section now states the exact compatibility diagram requested by the referee. The collision resolvent, first-return sum, direct block-scale operator, and physical inserted pairing agree on their common damped domains. We distinguish these proved arrows from the additional anisotropic realization required for high frequencies.

The new Gaussian proofs use actual collision-space endomorphisms with smooth multipliers. They do not claim that the discontinuous section projection is an anisotropic multiplier, that the unbounded induced twists are quasi-compact, or that an approximate distributional eigenvector has a nonvanishing regular phase. The construction and phase reconstruction requested in A, together with quantitative high-frequency Fredholm/resolvent control, are not discharged by these low-frequency results. The existing periodic coercivity and exact renewal identities remain the compatibility targets, without a new unverified hypothesis being promoted to a theorem of the billiard.

## 3. Request B: covariance, low frequencies, and cohomology

The actual Gaussian covariance and its continuity are now proved rather than assumed. Their proof uses an absolutely summable **collision** Green–Kubo series and the exact stopping identity. The central characteristic estimate and the induced functional limit are unconditional consequences of the stated collision-theory input. This answers the part of the report observing that the Gaussian law of the actual record had no established uniform covariance.

The kernel theorem also replaces a mere zero-variance criterion with a proved equivalence to an actual `L^2` coboundary for both the collision and induced systems. Its transfer function is obtained as an `L^2` equivalence class. We have not silently evaluated that class at a chosen periodic point. Uniform positive definiteness therefore still requires the periodic-evaluable regularity step identified by the referee.

We keep the stronger induced-correlation criterion in `core/19_raw_closure_contracts.tex`. Neither absolute summability of that induced series, convergence of normalized induced second moments, nor a single induced leading-eigenvalue expansion is asserted by the collision stopping proof. The uniform cubic expansion is proved for the smooth collision family at its explicit shrinking scale. These distinctions prevent a weak-limit covariance from being misrepresented as every stronger form of the requested induced spectral theorem.

## 4. Request C: complete raw branch decomposition

All existing critical-word calculations and correction terms remain. In particular, the original-section edge calculation is not transferred to the enlarged section by changing a normalization. The cumulative collision-count cutoff still removes trajectories in total variation only. The new single-collision BV estimate concerns the initial collision coordinates only. Neither controls second derivatives of a many-return density.

We have not obtained the complete critical/singular decomposition with absolute residual derivative sums, true word multiplicities, and uniform return-count growth constants. Accordingly, no numerical frequency splice is invented. The raw residual criterion and the strict splice inequalities remain present as the precise additional estimates needed for the original raw theorem. This request remains an analytical requirement, not an accomplished branch-summation theorem.

## 5. Request D: raw and weighted local limits; physical conditioning

The completed physical return process now has an unconditional functional Gaussian theorem, and stationary physical-time displacement and collision-count fluctuations have their own unconditional functional consequence. This removes the previously assumed **unconditioned process** input from the clock analysis.

The same-event conditioned maximal unfinished-block estimate remains unchanged. An unconditioned functional CLT cannot be divided by a shrinking event probability to obtain a bridge theorem. Nor does it control the relative symmetric difference of exact physical and completed-block conditioning events. The raw mixed-density LLT, weighted inserted density estimates, and the exact-event replacement requested in D still require A, the remaining periodic regularity in B, and C. The title and main problem remain the raw density problem; we do not relabel a weak limit as a local density theorem.

## 6. Request E: specialist proof review

`COLLISION_INPUT_MAP.md` provides a theorem-to-hypothesis map for the imported Demers–Zhang collision framework, including boundary-length reparametrization, deck-invariant reduction, invariant measure convention, and smooth multiplier norms. The new BV, smoothing, stopping, and fourth-moment arguments are written as complete proofs in the article for direct review.

No independent human billiards specialist has been commissioned or contacted in this revision, and no such acceptance is claimed. The source audit, finite diagnostics, and native TeX build establish only the properties they test. The requested independent check of the collision input, periodic geometry, singular boundaries, and new Gaussian proofs remains an appropriate next referee task.

## 7. The ten expository and technical comments

**1. Unconditional synopsis.** A theorem at the start states the actual uniform Gaussian and functional results, their continuous positive semidefinite covariance, and the kernel characterization. The following paragraph separately identifies what raw inversion still requires.

**2. Complex-frequency domain.** The common-scale construction is stated on the universal cover `C^4`, with invariance under real `2pi Z^3` shifts and local complex charts. It is not described as a newly constructed globally holomorphic complex torus.

**3. Compatibility diagram.** The common-renewal section includes the diagram and the exact physical insertion equality. The possible anisotropic realization is specified as an additional compatibility obligation, not a proved arrow.

**4. Fixed-count versus long-time continuity.** Fixed-return common-chart continuity is retained in its original scope. The new infinite covariance continuity uses a separately proved uniform correlation tail; functional uniformity uses tightness, finite-dimensional convergence, and parameter compactness.

**5. Notation collisions.** The complementary projection is `E_R=I-P_R`, not `Q_R^perp`. The physical Gaussian covariance is `mathcal V_R`, distinct from the physical visit count `V_R(t)`.

**6. Normalization at renewal.** Immediately before the operator definition, the section mass `c_*=91/(10000pi)` and `dnu_R^*=c_*^(-1)1_(Y_R^*)dnu` are recalled.

**7. Renewal literature.** The section cites Gouëzel's operator-renewal work and identifies the contribution as the exact physical moving-record implementation, not abstract renewal algebra.

**8. Proof flow.** The article is organized by dependence: physical geometry, normalization and return estimates, common realization and clocks, new Gaussian proofs, then operator and raw inversion requirements. Version identity, hashes, and the point-by-point response stay in supporting documents. No inherited mathematical argument is removed to shorten the paper.

**9. Truncation versus density derivatives.** Both the manuscript and this response explicitly separate trajectory total variation, initial-coordinate BV, and inverse-coarea density derivative norms. The new covariance argument supplies no all-branch density regularity claim.

**10. Conditioned-clock boundary.** The same-event path comparison is retained. The new physical functional corollary is expressly unconditioned; changing an exact event remains a weighted local-density problem.

## 8. Resubmission position

Revision 9 supplies a new, complete low-frequency and functional Gaussian argument for the physical record while retaining the original raw local-limit problem and all earlier mathematical material. It does not represent the entire operator/periodic-regularity/raw-residual chain as closed. The report's observation that the central raw and weighted density theorems are not yet unconditional remains applicable to those endpoints, but no longer to the actual covariance, unconditioned Gaussian process, or measurable zero-variance cohomology proved here. These are the precise claims submitted for further referee examination.
