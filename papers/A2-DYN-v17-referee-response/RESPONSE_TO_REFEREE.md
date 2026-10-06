# Response to the latest referee: A2-DYN revision 17

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v17-referee-response`  
**Controlling report:** `reviews/a2-dyn-v16-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Report commit / blob:** `b0b7ddfcd90f493e02254742b33174e9108fc5a7` / `805f04cd60d144bc6321ce3f4304ebe1cda34999`  
**Reviewed author baseline:** `2054310e587e576ce593112c30cdfabac6742105`  
**Date:** 6 October 2026

We thank the referee for the detailed audit of the collision and actual-return function estimates. This revision addresses the newly isolated peripheral spectral parameter and supplies a concrete operator reconstruction and residual comparison for finite-rank compressions of the actual return operator. It also strengthens the regularity budget in the near-origin theorem. The new results are Theorem H and Sections 31--32. They are not obtained by relabeling a one-step defect as a Fourier tail.

The title, triangular Lorentz family, actual section, four-coordinate displacement/count/flight-time record, and raw mixed-density endpoint remain unchanged. All 37 inherited core modules and their theorem statements remain byte-identical. The new arguments use the existing centered collision covariance, middle-block damping, modulus control, genuine return tower, cumulative return tail, and quantitative finite-record variation theorem.

## A. Spectral parameters, reconstruction, and an actual operator comparison

### A.1. An exact lift for every return phase

Write the physical frequency as `z`, the return spectral phase as `xi`, and the unit resolvent parameter as `lambda=exp(i xi)`. The collision constant phase is separately denoted by `sigma`.

The new exact identities are

`b_{R,xi}=eta_R+exp(i xi)(1-eta_R)`,

`L_{R,z,xi} f=b_{R,xi} L_{R,z} f`,

`sigma=c* xi`, `w=z-sigma e_3`, and

`sigma+w.h_R=z.h_R+xi eta_R`.

They use the exact third-coordinate relation `h_{R,3}=1-eta_R/c*`. At age zero the extra tower multiplier is one; at every strictly positive age it is `exp(i xi)`. Its BV norm is uniform in `xi`. At the true tower top the remaining defect is exactly

`f o F_R^* - exp(i(xi+z.g_R)) f`.

The norm identity has the height weight `c* integral r* |f|^p`, whereas the defect identity has `c* integral |E f|^p` with no height weight. Both are displayed together in `lem:exact-peripheral-lift`, including returns of length one. The full lift is still not presumed BV; multiplying the previous finite-age approximant by `b_{R,xi}` gives the same approximation errors and only a fixed factor in its BV budget.

Thus the arbitrary return phase now has an exact collision representation. It is not simply substituted as a constant per collision: the simultaneous shift of the four-dimensional frequency is essential.

### A.2. Quadratic endpoint budgets and the shifted cancellation line

The old endpoint deletion used boundedness to charge `O(r ell)` for two collision segments of length `ell`. The new proof uses centering and the established collision covariance bound to charge `O(r sqrt(ell))`. The endpoint weights have modulus at most one, and the integral is against the stationary collision measure, so Cauchy--Schwarz applies without independence. All other terms in the original middle-block argument are unchanged.

Consequently the collision phase estimate holds under `r^2(1+log H)` small, not merely `r(1+log H)` small. This is Lemma `lem:quadratic-endpoint-budget`.

The shifted frequency `w` may vanish although `(z,xi)` does not. Lemma `lem:joint-collision-phase-defect` treats this case instead of dividing by `|w|`. For a collision constant phase `sigma`, put `s=dist(sigma,2 pi Z)` and `t^2=|w|^2+s^2`. When the constant phase is dominated by `|w|^2`, diffusive damping applies. Otherwise choose a mixing time at which the constant phase has negative real part. The centered sum costs `C|w|sqrt(j)`, and the phase iteration costs `j` times the defect. This gives a joint lower bound `c t^2` under `t^2(1+log H)` small, including `w=0`. Modulus variance and BV circle truncation then give the complex-function lower bound `c t^2/[1+log(H/t)]`, with no positive lower-modulus assumption.

### A.3. New actual-return spectral neighborhood

Let

`rho^2=|z|^2+xi^2`, `Lambda=1+log(H/rho)`, `K=Lambda log(2+Lambda)`.

Theorem `thm:joint-return-spectral-defect` proves, uniformly in the radius,

`||E_{R,z,xi}q||_1 >= b rho^2`

for unit section phases, and

`||E_{R,z,xi}f||_2 >= b rho^2/K`

for normalized complex section functions of supremum plus zero-extension BV norm at most `H`, whenever `0<rho<=rho_0` and `rho^2 K<=a`. The proof explicitly includes the pure return-spectral direction `z=0` and the shifted-frequency cancellation line. It fixes the approximation accuracy before the smallness constants, displaying the logarithmic dependence that prevents a circular budget choice.

At `xi=0` the theorem strengthens the sufficient v16 condition from `|z| K<=a` to `|z|^2 K<=a`. For polynomial `H`, the same physical annulus now admits peripheral phases of size a sufficiently small constant divided by `sqrt(log n log log n)`. More generally, on

`2 n^(-99/200) <= |z| <= n^(-2/5)`, `|xi|<=n^(-gamma)`,

the theorem permits `H<=H0 exp(n^beta)` whenever `0<beta<min(4/5,2 gamma)`. The rescaled annulus remains `2 n^(1/200)<=|sqrt(n) z|<=n^(1/10)`. For example `gamma=2/5`, `beta=79/100` has strictly positive slack. This is a larger proved reconstruction budget, not a change of the physical datum.

The exact lift treats all `xi`; the quantitative estimate is local in the joint parameters. The remaining unit-circle arcs with a growing regularity budget are not declared controlled.

### A.4. Explicit finite-rank reconstruction and a resolvent theorem

Section 32 defines `U_{R,z}f=exp(-i z.g_R) f o F_R^*` on the actual section probability, and compresses it by conditional expectation `P_{R,h}` on a grid fitted to the five section rectangles. The finite matrix is `A=P U|_V`. Its entries are exact integrals over `B intersect F^{-1} C` with the full unbounded multiplier. No return-length cutoff occurs in the matrix definition.

Lemma `lem:section-grid-reconstruction` proves rank `O(h^(-2))` and supremum plus zero-extension BV budget `H_h=C/h` for every normalized vector. The proof counts both internal jumps and section-boundary traces. It does not assume a nonzero pointwise modulus.

Lemma `lem:compression-defect-comparison` is an exact Hilbert-space calculation. For an arbitrary normalized approximate vector and `|lambda|=1`, the orthogonal identity is

`||(U-lambda)f||^2 = ||(A-lambda)f||^2 + 1-||Af||^2`.

If the compressed residual is `epsilon<=1`, the physical defect squared is at most `3 epsilon`. Applying the new physical function theorem gives a lower singular value `b rho^4/K_h^2`, not just an assertion about exact eigenvectors. Theorem `thm:compressed-peripheral-resolvent` therefore proves

`||(exp(i xi)-A)^(-1)|| <= C K_h^2/rho^4`

on the stated joint region, with an explicit inward radial neighborhood, exterior radial bounds, and the corresponding adjoint estimate. Non-normality does not invalidate this argument because it uses the smallest singular value.

This closes reconstruction and the residual-to-resolvent comparison for the specified compressed actual operators. It is not an anisotropic-to-BV reconstruction for arbitrary distributional spectral vectors and is not advertised as one.

## B. From the operator comparison toward complementary integrals

Proposition `prop:compressed-finite-time-comparison` supplies a separate, quantitative consistency theorem for the unmodified characteristic function. With `L>=n`, the error between that function and `<1,A^n1>` is at most

`C n [ exp((a n-c L)/2) + sqrt(h(1+|z|) exp(C1 L log(2+L))) ]`.

The proof first writes a finite return-count event as an explicit union of binary membership words. It combines the existing finite-collision variation bound with BV product and chain inequalities to control the truncated phase. The exact projection telescoping identity then bounds the power error, and the true cumulative-return tail bounds the discarded high-count event. This is a proved approximation error, not an unproved spectral convergence claim.

The two kinds of estimates are kept separate. A mesh/time choice suitable for the raw LLT must satisfy this error bound and the joint resolvent budget simultaneously, control the other peripheral arcs, and provide contour-to-power bounds. Neither eigenvalue separation of a non-normal finite matrix nor fixed-time consistency supplies this conclusion by itself. The complete radius-uniform complementary integral, including compact nonzero and growing/far roof-frequency regimes, remains a requirement of the original inversion theorem.

## C. Complete critical and singular raw branch extraction

Every inherited raw edge, localized inversion, and second-derivative sum statement remains unchanged. The new cutoff-phase variation concerns bounded initial-coordinate functions and includes their itinerary jumps. It does not estimate inverse-coarea Jacobians, second distributional derivatives of raw densities, or local jump magnitudes after pushforward.

Thus all regular critical words, central critical branches, grazing and competing-root boundaries, and dynamically generated image boundaries remain in the full extraction problem. No part of that sum is removed from the endpoint.

## D. Weighted exact conditioning

The original initial and single-marked central and moment theorems retain their exact measures, indicators and denominators. The new operator reconstruction is for a specified bounded function class; it does not identify path indicators or exact physical observation events with that class. Weighted complementary tails, weighted edge estimates, and the relative comparison of completed-return and physical observation events remain explicit. No conditioning event is replaced in the new proofs.

## E. Specialist checking and presentation comments

The new arguments introduce no additional external dynamical theorem. Their inherited inputs are the collision covariance and spectral splitting, BV smoothing and circle truncation, the exact tower and its finite-age approximation, and finite-record variation. The new endpoint estimate, dephasing time selection, affine phase shift, grid reconstruction, orthogonal residual identity, and projection power identity are proved in the article. These are concrete focal points for the next independent specialist review; no human review or formal proof certification is claimed here.

Comments 1--3 and 7 are addressed by the note immediately beside Theorem G, the separate notation `z`, `sigma`, `xi`, `lambda`, both annulus scales, and the joint norm/defect display. Comments 4--6, 10--11 retain their original distinctions and source maps. Comments 8--9 and 12 are addressed by specifying exactly which operator reconstruction and resolvent are proved, and separating them from the uncompressed power and Fourier estimates. Comments 13--14 are addressed by the exact inherited-edit ledger, full source hashes and dynamic execution receipt. The phrase in the abstract that could suggest an already complete distributional phase reconstruction has been replaced by the precise collision-function statement.

## Source qualification

All 37 inherited core files, all inherited Python scripts, and the bibliography are byte-identical. Six exact edits occur in `main.tex`: revision identity, two abstract changes, the spectral clarification and Theorem H, the proof-route update, and the two new core inclusions. No inherited mathematical label is deleted.

New finite diagnostics test arbitrary return phases on variable-height towers, including one-level returns; the affine frequency shift and its cancellation line; dephasing time choices; exact orthogonal compression identities and residual inequalities; projection telescoping; grid boundary variation; and strict subexponential exponent slack. Negative controls reject replacing a per-return phase by an unshifted per-collision phase and discarding projection leakage. These finite models do not prove billiard mixing or continuum spectral convergence.

The read-only workflow checks and archives the exact committed source, runs normal and optimized diagnostics, builds the complete article natively and emits the event SHA, run ID and PDF hash. This static reply does not predeclare a future run successful. The revision is offered for substantive review of the new proofs in the original raw mixed-density program.
