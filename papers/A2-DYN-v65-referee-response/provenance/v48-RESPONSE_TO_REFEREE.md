# Response to the external referee: A2-DYN revision 48

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v47-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Review commit / blob:** `c7401a143332921b42cd532ea1f23617ad59e1bc` / `1d45f2c8bbf9664a4a1e188c80004d44ed4f9cfc`.  
**Reviewed author SHA:** `ec4e7cca65ee3cbdc441c8264b39aca3ead112ac`.  
**Revised article:** `papers/A2-DYN-v48-referee-response/main.tex`.

We thank the referee for the detailed distinction between a fixed endpoint layer and an unbounded family of decision depths. The new revision proves a pointwise theorem for every section-decision depth on the physically protected source. It does not obtain that conclusion by interchanging a limsup with a sum of qualitative finite-history estimates. The finite-count bound needed for the sum is proved first. The original four-coordinate raw-return problem, title, physical record and arithmetic main term are retained.

## R1. The residual pointwise criterion

The three-source criterion is reduced to two physical sources by a new positive decomposition, not by declaring the old middle-decision mass estimate pointwise. Write the full guard as `Xi=H D`, with `H` containing every incidence and clearance factor and `D` every section-decision factor. Then

`1-Xi = H(1-D) + (1-H)`.

Theorem `thm:v48-all-decision-smallness` proves that the exact-index density of `H(1-D)` has normalized essential height at most `C epsilon^(1/16)` after the collision limit, uniformly in the radius and exact labels. The result includes arbitrary bounded measurable insertions. It therefore controls the complete smoothing correction of this part at all reconstruction bands.

The physical remainder `b` is the original source weighted by `1-H`. It splits positively and disjointly by the first physical factor strictly below one into incidence and clearance parts. Combined with the inherited protected correction, `thm:v48-two-source-reduction` gives a paid error `O(B^(-1/192))` at `epsilon(B)=A B^(-1/12)`. The full arithmetic raw law is equivalent to the signed correction of `b` vanishing in the same ordered limit.

This revision does not prove the latter physical correction. The old first-bad-middle source can contain a subsequent physical defect; those states are assigned to `b`, not discarded or relabeled as controlled. This precise reassignment is essential to the new assertion.

## R2. Physical-word boundaries

Every new continuation preserves the actual physical word, displacement and collision count. All incidence and clearance margins remain protected. Only section-membership cuts are freed. Neither a near-grazing crossing nor a competing-hit crossing is treated by the decision flow. The local measure is explicitly `nu/c` after an endpoint leaves the original section.

The two remaining physical sources still have mass bounds only. No small-mass argument or exponential finite-count height estimate is used to infer their `m^(-2)` correction bound. A physical-word transition theorem or a signed cancellation argument is still required for them.

## R3. Interior decisions: a uniform finite-count theorem

This is the main new proof, in modules 102 and 103.

First, a union of a fixed number of thin coordinate strips around the section sides has a uniformly bounded strong multiplier norm and a strong-to-weak norm `O(s^(1/8))`. The weak estimate is obtained directly by cutting each stable curve into finitely many intervals of length `O(s)` and using its strong stable length normalization. Width below matching distance is charged wholly to the unmatched pieces. No inverse width and no long-pullback multiplier appears.

Second, on each moving resonance chart, the full occupation Doeblin--Fortet estimate and the spectral splitting give the interpolation bound

`norm(Pi h) + sup_a |ell(Q^a h)| <= C norm(h)^(1/2) |h|_w^(1/2)`.

The proof chooses a logarithmic iteration length from the weak norm. The peak charts are fixed in one small roof neighborhood before any outer band is enlarged. Thus a thin-strip insertion costs `s^(1/16)` in the principal amplitude, uniformly even at an initial or terminal mark. Expanding whichever chronological block is at least half the collision count gives, for a fixed roof interval of length `h`,

`m^2 P(K=k,A=l,S-t in I,strip_s at j) <= C s^(1/16)(h+1/B) + C_B(1+Bh)m^2 rho_B^(m/2)`.

The leading constant is independent of the outer band; the remainder may depend on it. The bound is uniform in strip width and mark, so those may depend on `m`. This is an upper bound, not an asymptotic Gaussian amplitude for a shrinking selector.

Third, order the section guard by endpoint depth. The positive telescope `Z_a=G_a-G_(a-1)` frees every decision of depth at most `a`, retains all deeper decisions and all physical margins, and has one bad mark at depth `a`. A single continuation radius, gradient scale and auxiliary roof band work for every layer. At most `2a+2` occupation summands can change, and this allowance is used only in the upper comparison.

At high gradient the roof flow retains the bad depth-`a` strip. At low gradient the critical collar retains it as well, since the state response is `C zeta^(-1) q^(3a/4)` whereas the bad width is `epsilon q^(a/4)`. Choosing a fixed `delta <= c epsilon zeta` keeps every collar inside a constant enlargement of that strip. This replaces the depth-independent normal-strip comparison, which by itself could not be summed.

Each layer is bounded by `C(a+1) epsilon^(1/16) q^(a/64)` plus an error `C_(eta,epsilon)(a+1)m^2 rho^(m/2)`. Sum this finite telescope before taking the limit. The summed error is at most `C_(eta,epsilon)m^4 rho^(m/2)`. The exact geometric sum yields the tail factor `(J+2)q^((J+1)/64)`. In particular no uncontrolled family of depths can escape to infinity. This addresses the quantifier issue in report sections 7, 15.3 and technical comment 7 directly.

## R4. Arithmetic main term

The full occupation coefficient remains present in every local upper bound. All surviving moving spectral peaks are included; none is discarded by an unmodulated approximation. At a fixed radius the candidate raw main term stays `c mathfrak a_R(k,n,m) g_Omega_R` (or its original return normalization); uniformly through arithmetic changes it stays `mathcal L_(m,R)`. No assertion that the concrete residues vanish has been added.

## R5. Weighted theorem and conditioning

The new entire decision source and its all-band correction admit every bounded measurable source insertion by Radon--Nikodym domination. No derivative of that insertion is taken. The inherited protected regular bound still needs its own endpoint-gradient budget, and the physical remainder must be controlled for the same insertion at the same roof value. A full weighted raw LLT or pointwise roof-conditioned bridge is therefore not claimed. The distinction between regular Gaussian amplitudes and arbitrary bounded posterior tests remains unchanged.

## R6. Independent verification

No independent human billiards specialist audit has been obtained in this author revision. `SPECIALIST_AUDIT_MAP.md` specifies the new multiplier, interpolation, marked pairing, all-depth continuation, critical-strip retention and summed-error steps requiring review. Finite diagnostics test algebra, source identities and explicit finite models only. They do not verify the continuum anisotropic or singular geometry.

## R7. Novelty comparison

The new result is neither another stationary physical singleton theorem nor a reformulation of a fixed-window LLT. Existing fixed-band occupation estimates and the existing protected geometric continuation are the inputs. The new step is their uniform marked thin-strip combination, followed by a positive all-depth source telescope and a critical-collar comparison that preserves the small marked strip. Its output is a pointwise exact-index bound for a collapsing decision source, not a sum over return indices. The exponent is not claimed sharp and no claim of historical priority beyond the verified comparison is made.

The direct route in the introduction identifies this distinction. The earlier theorem-level literature comparison and all references remain intact.

## R8. Route, preservation and qualification

A new leading theorem states the all-depth bound and its finite-count tail. Three new core modules provide the full proof and physical-only remainder. All 101 inherited core modules, all 127 inherited Python scripts, the bibliography, the A--X synopsis and all old mathematical labels remain byte-identical or, for front-matter labels, remain compiled. The old main source and four companion records are archived verbatim. No previous branch or unrelated paper is changed.

The workflow checks the event SHA, frozen full baseline tree, report blob, all 104 core inclusions, label and bibliography retention, the ordinary-source Merkle tree, ordinary/optimized diagnostic agreement, native compilation and theorem-label-based rendering. The dynamic receipt identifies the actual run, SHA and PDF. Baseline v47 runs `37789082590` and `37789105202` are evidence for v47 only, not for this revision. No successful v48 execution is predeclared in a static record.

## Technical comments 1--24

The proof distinguishes collision count `m`, return index `n`, reconstruction band `B`, auxiliary fixed spectral band `B_*`, physical and decision margins `eta,epsilon`, layer `a`, tail cutoff `J` and fixed gradient scale `delta`. Occupation includes times `0,...,m-1` only. The ambient factor `1/c`, almost-everywhere corner derivatives, forbidden physical boundaries and single charging of collars remain explicit. A collar and its source share the same retained occupation, so its allowance is not doubled. The new finite-count uniform error, rather than the old finite-history envelope, justifies the depth sum. All-band conclusions are convolution consequences; no growing-band spectral constants are controlled. First-defect sets include the transition region. The legacy exponential finite-count height flag is explicitly scoped in the manifest and is not used as central deconcentration. A fixed interval is not cited as a pointwise density value. Arithmetic modulation and the distinction between source qualification and proof certification are preserved throughout.
