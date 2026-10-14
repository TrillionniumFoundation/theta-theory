# Response to the v52 external referee: A2-DYN revision 53

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v52-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Review commit / blob:** `b487df93e48dbf455b3ed04680c1f7ae3613f45e` / `9f50c9909cc137d67babfd69f6508de2ce3254cf`.  
**Reviewed author SHA / full paper tree:** `4449ba65b59d2670fb1231515e860d874b466b87` / `a5f687493f1f574c700cf28c10f24f25841ad0d7`.  
**New complete manuscript:** `papers/A2-DYN-v53-referee-response/main.tex`.

We thank the referee for distinguishing the common positive path remainder from an assertion that the scalar physical heights are small. This revision keeps that distinction and the original raw pointwise problem. It supplies a stronger estimate for the original exact-event path source, not a replacement event or a packet average, and isolates the reusable measure-valued principle requested in item 7. The results and proofs are in modules 112--114 and the third leading theorem.

## 1--4. Physical heights, the two-sided raw theorem, and the pointwise bridge

The new estimate is not a physical-seam continuation. Keeping the differentiation-order constants in the inherited moving-peak analytic argument gives, for every integer r>=1,

`int_E |S_(a+l)-S_a-(l/m)S_m|^(2r) dnu* <= (2r)! C_J^(2r) l^r m^(-2)`.

The constants are independent of r and the exact labels. One roof majorant and one spectral band are fixed before r or m varies. The proof uses a Cauchy circle of radius proportional to L^(-1/2) on each peak, a fixed complex circle off the peaks, exact three-block drift cancellation, and the four-frequency inverse. It does not infer a factorial bound from an unspecified constant in a fourth-moment theorem.

A dyadic L^q maximum argument, with a geometric sum uniform for all even q>=4, proves an exponential supremum moment of the entire unguarded pinned collision path in the finite measure `(m^2/h) 1_E nu*`. The exact half-open return clock transfers it to the actual return path on central windows. No rare-event denominator is used until the conditional theorem.

For the positive incidence/clearance subsource, Cauchy--Schwarz now gives exponentially weighted local mass `O(epsilon^(1/32))`. Thus even large path amplitudes of that same physical subsource have a vanishing local moment budget. This is stronger than its unweighted local mass bound and does not require differentiating a path selector on a physical seam.

It does not prove either positive scalar essential-height estimate. A path-amplitude moment does not rule out concentration on a very narrow roof set. Consequently the two-sided pointwise raw law and the unconditional essential-supremum same-roof bridge are not claimed proved. The original incidence and clearance criteria remain explicit. No endpoint flow is extended across a grazing or competing-hit boundary.

## 5. Intrinsic arithmetic

Every uniform raw formula retains `G=mathcal L_(m,R)`; the fixed-radius specialization retains the section-residue factor. All moment estimates are for the exact original labels `(n,k,m)` and the unchanged roof coordinate. Neither the nonresonant complement nor the multiple moving peaks are discarded. The conditional reference uses `G_+`; the unnormalized raw reference remains signed `G`. No concrete residue is replaced by one.

## 6. Specialist verification

No independent human audit has occurred in this author revision. `SPECIALIST_AUDIT_MAP.md` states the additional continuum checks and pins the inherited ones. In particular the new all-order argument requires the *same* complex circle to work independently of the derivative order, not just a separate estimate for each order. Source hashes, finite calculations and a PDF build do not verify the billiard operator input.

## 7. Reusable path-valued principle

Module 112 first proves a standalone signed-measure lemma. Its hypotheses separate bounded total variation, tight total variations, mass convergence and convergence of rational-time characteristic cylinders. Jordan parts, or the explicitly positive measures `tau_m +/- sigma_m` when `|sigma_m|<=tau_m`, give subsequential compactness. A finite equicontinuous net on a compact path set gives convergence in the bounded-Lipschitz dual norm, not path-space total variation.

The following theorem separates four independent assumptions: fixed-band scalar/cylinder inversion, variation compactness, controlled-source correction, and the local mass of one positive remainder common to all tests. It proves a common path remainder, roof-integrated path local variation, same-roof convergence in conditional mean, and the pointwise implication under an *additional* positive-height assumption. The final paragraph verifies each hypothesis using the actual source-pinned billiard statements. The abstract theorem contains no unverified billiard assertion inside its assumptions.

Module 114 adds two quantitative tail-upgrade lemmas. A mean bounded-Lipschitz error e and a common exponential path moment imply polynomial-growth test convergence and mean p-transport cost at most `C e(1+|log e|^p)` for every fixed finite p. This is a modulus in e, not a convergence rate in the collision count.

The resulting actual same-roof bridges converge in every finite Wasserstein order under the original conditional roof law. Conditional first moments, covariance kernels uniformly over the path times, and moments of path maxima converge in that same mean sense. The original roof value and return index are not changed.

## 8. Scope and prior art

We do not claim that the abstract weak-to-Wasserstein implication, Gaussian bridge moments, or bounded-cost duality are historically new. The latter is cited to Villani, with the exponential-tail estimate proved explicitly here. The model-specific new input is a factorial-order spectral estimate uniform over the original microscopic arithmetic event and its exact labels, followed by an unguarded whole-path exponential moment. It is not a consequence of scalar roof total variation alone.

The same new estimate supports both collision-clock and actual-return-clock statements, but those are two observables of this system, not two independent dynamical models. No second singular-hyperbolic application is claimed in this revision. The existing circular, compact-family, interval, arithmetic, posterior and bridge results are retained. The top-four significance assessment remains for the next referee; the response does not label an unfinished pointwise theorem as complete to obtain a venue claim.

## 9. Proof route and preservation

The third leading theorem now includes the new transport conclusion with its exact roof-law qualification. Modules 112, 110--111, 113 and 114 form the short route: signed compactness; the common physical path remainder; same-roof bounded tests; factorial moments; exponential tails; transport and conditional moments. Existing geometry and raw inversion remain in place with their prior labels and full proofs.

Of the 111 inherited core modules, 109 are byte-identical. The exact notation, Fourier-normalization, domination and joint-measurability changes in modules 110--111 are recorded as individual replacements in `INHERITED_EDITS.json`; both old files are archived verbatim. All 143 inherited Python files and the compiled appendices are unchanged. The old bibliography is retained entry-for-entry, with one new reference and its old full version archived. No inherited mathematical label is deleted.

## 10. Topologies and an important reference-law qualification

The new Wasserstein metric uses the unbounded path supremum distance. The theorem concerns its pth power in mean under the true conditional roof law. The exponential moment is also controlled in mean, not uniformly at every roof. The conditional kernels are defined almost everywhere, and no assertion assigns positive mass to an individual roof singleton.

For the reference roof law, a further hypothesis is needed for this stronger topology. A small roof total-variation distance cannot control an unbounded transport cost. We therefore require a pointwise reference floor `G>=d_0` on the window before invoking the inherited domination `pi_m>=alpha_m pi_hat_m`. That domination transfers the nonnegative transport costs. Under only a positive *integrated* reference mass, the existing bounded-Lipschitz reference-law theorem remains true and unchanged; the new unbounded reference-law conclusion is not asserted.

## Technical comments 1--26

Comments 1--4: the deterministic return matrix is now `mathsf A_(m,R)`, distinct from occupation. The two-sinc-square dominator uses the explicit transform `hat f(xi)=int exp(-i xi s) f(s) ds`, inverse factor `1/(2 pi)`, and integrable compact transform `pi(1-|xi|/2)_+(1+exp(i pi xi/2))`. Its name `mathsf q^[B]` denotes a B-dependent multiple, not a rescaled support.

Comments 5--10: module 112 isolates signed compactness; the domination of variations is explicit; roof selectors are jointly Borel; the countable norming class and common roof-null versions are retained. No path-space total-variation theorem is inferred.

Comments 11--16: the reconstruction and auxiliary spectral bands are fixed before every collision limit. Central windows use the explicit enlargement `M_0+h/sqrt(m)`. Signed G and positive G_+ have distinct roles. Conditional kernels remain almost-everywhere objects.

Comments 17--20: conditional mean is not an externally prescribed-roof statement. The pointwise scalar height condition remains conditional, the collision limit precedes the reconstruction-band limit, and the positive physical path remainder is common to all tests.

Comments 21--26: the source remains `nu*=nu|Y*/c`; occupation is half-open at times `0,...,m-1`; the exact return index and roof value survive disintegration and time change. Unbounded polynomial-growth locally Lipschitz tests are not arbitrary measurable path selectors. Reverse roof likelihood is not forward roof likelihood. Qualification is not continuum proof certification.

## Exact execution evidence

The initial remote v53 commit records the frozen lineage, and a separate read-only source-snapshot run supplied the exact report bytes for local verification. That snapshot run is not a manuscript build. The final dedicated workflow qualifies the complete manuscript at its own event SHA on both branches. Static text does not predeclare a future run successful: `evidence/build-receipt.json`, its matching GitHub run and the artifact digest are the execution records.
