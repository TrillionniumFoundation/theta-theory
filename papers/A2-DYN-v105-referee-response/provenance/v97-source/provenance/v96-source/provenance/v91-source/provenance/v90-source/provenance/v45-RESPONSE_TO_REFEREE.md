# Response to the external referee: A2-DYN revision 45

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v43-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Review commit / blob:** `0418466ec7a126b032e64cc8c54238770104cf68` / `6d223bd63ddd76a5a2efc3351c475d0261e93839`.  
**Reviewed author SHA:** `f3fb2858b2c10aa2f4f857d56132491a5ea25861`.  
**Immediate intervening author revision:** v44, `848582734b94a6cda2d27484be2d6dcf646744a4`.  
**New complete article:** `papers/A2-DYN-v45-referee-response/main.tex`.

We thank the referee for requiring an estimate of the signed correction, not another representation. Revision 44 established full-source height control and separated finite jumps from continuous singular germs. The present revision supplies a dynamical `o(m^(-2))` estimate for a specified positive part of the original exact-index source and for its intrinsic critical jumps. The arithmetic main term, original section, prescribed integer labels and full raw-density target are retained.

## 17.1. Signed correction: the new part actually estimated

Theorem `thm:v45-critical-source-smallness` proves pointwise smallness of the complete collection of physical critical collars in the protected class. It estimates the original positive source, not a correction whose coefficients have been reduced. The result is uniform over the radius, exact return index, collision count and displacement, and over all bounded measurable insertions on that source. Corollary `cor:v45-critical-unsmoothing` removes its contribution from `p-K_B*p` with an `o(m^(-2))` essential-supremum error uniform in every `B>0`.

The full remaining signed correction is not proved small. Words outside the stated protection envelope, their singular/decision-boundary contributions, and the noncritical inverse remain. The statement is not described as a complete raw LLT or used to mark the corresponding manifest flags true.

## 17.2. Intrinsic critical coefficients, including coalescing values

Module 96 proves a word-length-independent endpoint collar. At contact `j`, write `d_j=min(j,m-j)` and require incidence and section margin at least `epsilon q^(d_j/4)`, where `q=47/53`; flight clearance has the analogous distance from flight endpoints. This includes every fixed-margin word and permits exponentially small interior margins.

The normalized internal contact Hessian is tridiagonal with a diagonally dominant positive potential. Its inverse has exponentially decaying entries. In an endpoint response one incidence factor cancels, giving a contact displacement bounded by `C epsilon^(-1) q^(3d_j/4)` times endpoint displacement. Dividing by the permitted margin leaves summable decay. The source cross-Jacobian is the exact product of adjacent inverse lengths divided by the internal determinant. Its logarithmic derivative costs `C epsilon^(-3)`, not a factor growing with the word length. Consequently an endpoint square of radius `r_* epsilon^3` remains physical with all original return decisions and has relative source-density ratio between `e^(-1)` and `e`.

Uniform endpoint curvature then gives a positive roof collar of width `h_* epsilon^6`. Its mass is bounded below by a universal constant times `h J_z`, and its density above by a universal constant times the unaltered intrinsic jump `J_z`.

Module 97 uses a distinct dynamical input: the exact-index arithmetic local law with two smooth normal-strip endpoint majorants. Their physical masses are `O(d)`, so the limsup of `m^2` times the probability of a fixed roof interval `J` is at most `C d^2 |J|`. The proof retains every resonance through radius transitions and bounds its physical amplitude; it does not set the arithmetic factor to one.

For all critical values in `[t-h,t+h]`, the disjoint physical collars lie in the unchanged exact-index event with roof in `[t-h,t+2h]` and both endpoints in strips of width `C sqrt(h)`. Thus `h` times the full sum of intrinsic jump coefficients is bounded by a positive local probability of order `h^2 m^(-2)` in the limsup. The conclusion is `limsup m^2 J^epsilon([t-h,t+h]) <= C h`, without counting words or separating their critical values. Letting `h` decrease after the collision limit proves that the entire atom, including exactly coalescing critical values, is `o(m^(-2))`.

The same estimate bounds the full physical collar density for any roof-excess widths `r_m -> 0`. The roof intervals are proof devices for a positive-source comparison; the theorem does not replace the requested integer singleton or average the return index.

## 17.3. Adaptive derivative budgets

For the protected critical part, the new proof bypasses `A_(2,ell)/b_ell` and component bandwidths completely. It estimates the source density and intrinsic jumps directly, using a collar whose size has an explicit polynomial dependence on its protection parameter and no dependence on word length. It supplies no corresponding bound for the complete residual derivative budget. That part of the original request remains open in the manuscript.

## 17.4. Beyond fixed bands

The spectral proof fixes the endpoint width and roof band before letting `m` tend to infinity, and enlarges the band only through the ordered envelope argument. The later uniformity over all `B>0` is the inequality `||f-K_B*f||_infinity <= (1+||K_1||_1)||f||_infinity` for a physical part already proved small. It is not an extrapolation of fixed-band operator constants. There is no claimed polynomial convergence rate for this qualitative local estimate.

## 17.5. Parameter uniformity

The endpoint collar and relative distortion constants are uniform over the circular radius interval and permit the stated exponentially relaxed interior margins. The positive endpoint estimate uses the existing finite continuous spectral-peak charts, including near-resonant branches whose moduli approach one. At a limiting actual resonance its amplitude is bounded by the product of the small physical endpoint masses. This gives uniform upper control without a continuous global choice of exact phase groups or critical values. The protection parameter is fixed; the theorem gives no rate valid for a prescribed `epsilon_m -> 0`.

## 17.6. Arithmetic

The final target continues to use `L_(m,R)` uniformly through radius transitions and `c a_R g_(Omega_R)` at fixed radius. The new positive upper bound sums the absolute amplitudes of all surviving resonances. It neither proves nor needs triviality of the concrete section residues, and it asserts no positive denominator for a residue of zero mass.

## 17.7. Weighted sources

Pushforward domination extends the protected-critical source estimate to every measurable insertion with a common supremum bound. This does not require a multiplier norm or a finite-record subanalytic description for that insertion. The separate statement on localized jump profiles applies whenever their coefficients are bounded by the corresponding physical `M J_z`; it does not identify every boundary jump with such a coefficient. The remaining weighted raw inverse and pointwise-roof bridge still require their own estimates.

## 17.8. Independent audit

No independent human specialist audit has been obtained. The new audit map asks for checks of the exact contact Hessian, incidence cancellation, graded continuation, cross-determinant formula, word-length-independent relative distortion, positivity/disjointness of the actual collars, the small-source amplitude at limiting resonances, and the order of the four limits. Finite matrix and residue models only test algebra and regression; they are not evidence that these continuum estimates have been independently certified.

## 17.9. Route and preservation

The new introductory route and Theorem 8 lead directly to modules 96--97. All 95 inherited core modules, all 115 inherited Python scripts, the bibliography, all inherited mathematical labels and the compiled A--X statements remain. The old main file and relevant records are archived verbatim under provenance. No old theorem, raw target, section, arithmetic term or historical report has been deleted or silently overwritten.

## Technical comments and exact-source evidence

The source uses `m` for collision count, `n` for return index, `B` for roof bandwidth and `J_z` for an intrinsic local jump. Full variation mass and essential-supremum norms retain their original conventions. Source collars use the original probability normalization `c^(-1)` and keep both endpoint visits. Fixed `h`, fixed endpoint width and fixed band precede the collision limit; the subsequent small-width conclusion uses domination, not a uniform quantitative LLT. The inherited right-trace convention is unaffected.

The frozen v44 response build is run `37747045842`, artifact `11536760644`, archive SHA-256 `34d0d0660328b4754ba845f5964a20389b94407fe37a729e520a71be3f05705e`. This is baseline evidence only. The v45 dynamic receipt and its matching GitHub Actions run identify actual new execution; no future success is predeclared here.
