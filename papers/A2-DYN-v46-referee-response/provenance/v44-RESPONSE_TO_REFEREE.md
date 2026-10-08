# Response to the external referee: A2-DYN revision 44

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v43-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Report commit / blob:** `0418466ec7a126b032e64cc8c54238770104cf68` / `6d223bd63ddd76a5a2efc3351c475d0261e93839`.  
**Reviewed author SHA:** `f3fb2858b2c10aa2f4f857d56132491a5ea25861`.  
**Frozen ordinary paper tree:** `7e40f2a45fcb0658a938ae93d6473fb108f9ae28`.  
**New complete article:** `papers/A2-DYN-v44-referee-response/main.tex`.

We thank the referee for separating reconstruction from the signed local estimate. This revision supplies two direct bounds on the original full source, rather than another cutoff identity. It does not change the section, replace a singleton by a packet, suppress arithmetic residues, discard inherited content, or call the remaining correction small without estimating it.

## 17.1. The complete signed correction

The full assertion `m^2 D_B -> 0` is not proved here. The revision proves a pointwise estimate for the *entire continuous singular part* of a complete-component extraction, not for the jump plus residual inverse. The distinction is explicit in the abstract, introduction, new corollary, manifest and this response. The new proof first restricts the actual possible singularities by a complete-source height theorem, so it is not just another rearrangement of the v43 identity.

## 17.2. Direct control of singular and decision-boundary contributions

New module 94 proves `||rho_{m,R}||_infinity <= C A^m` for the roof of the full m-collision source, uniformly in the radius. It then proves the stronger restriction bound `esssup_t sum_{n<=m,k}|p^w_{n,R}(k,m,t)| <= M C A^m/c` for every family of bounded measurable insertions. No subanalytic assumption on these weights is needed for this height estimate.

The proof has three substantive ingredients. First, on each regular physical word the two endpoint angles are valid injective coordinates. The reduced action Hessian dominates the two endpoint curvature terms even as interior incidence tends to zero. Second, keeping intermediate states as auxiliary variables gives a graph with O(m) variables and sign conditions of uniformly bounded degree. The nonasymptotic sign-component bound (Basu--Pollack--Roy, Section 3.2, (3.3)) bounds slicing multiplicities and Gauss-map multiplicities exponentially in m, independently of polynomial coefficients. Third, the nonstationary direction controls the source away from both normal endpoints; near normal endpoints, positive level curvature bounds the coarea integral by total turning. Regular exhaustion includes every portion approaching a singular boundary. Restricting this positive source to an actual return event cannot increase its density.

This excludes negative powers and nonconstant logarithmic terms of exponent zero from *complete physical* component densities, including decision-boundary values. Such terms were permitted by the generic constructible L1 preparation class, not proved to occur physically. Module 95 consequently separates true finite jumps from positive-exponent cusps. Shrinking a cusp support now controls its supremum because the cusp tends to zero at the singular value; shrinking a jump support does not. The original coefficients of both are kept.

For budgets epsilon and delta, the complete decomposition `f_l=j_l+z_l+q_l` has `q_l in W^{2,1}`, summed correction mass at most epsilon, and `sum_l ||z_l||_infinity <= delta`. The only discontinuities of `j_l` are the intrinsic jumps. With `delta_n=(1+n)^(-P-3)`, the whole cusp contribution to `D_B` is `O(n^(-P-3))` in the sum of component supremum norms, hence negligible after central `m^2` scaling. This is a proved height estimate, not an inference from the mass budget.

The jump audit bound `esssup_{|t-s|<h}|D_B(t)| >= |Delta f_l(s)|/2` makes explicit what must still be estimated for each central jump. It is not a claim that a nonvanishing normalized jump has been found, nor an impossibility statement about the original theorem.

## 17.3--17.5. Bandwidth, dynamics and parameter uniformity

The new complete density-height bound is exponential in m, with coefficient-independent constants from the finite one-flight format. This supplies a uniform bound not present in the earlier adaptive germ ledger. It is not a bound on `A_{2,l}/b_l`. The localizations can still make the residual second-derivative norm large, and no growing-band operator estimate is asserted.

For each fixed collision count the unweighted components also have a common finite BV budget throughout the moving-radius family. The proof treats the finitely many section endpoints as independent parameters with the original fixed normalization c, and uses parameterized constructible integration and uniform monotonicity. It gives `sum ||p-K_B*p||_1 <= C_K V_m/B`. No usable rate for `V_m` as m grows is extracted. This L1 estimate is not called a pointwise local limit or evaluated through a spectral theorem at a growing band.

The height theorem itself bypasses parameter-continuous preparation: the algebraic component bound does not depend on polynomial coefficients; the curvature and nonstationary bounds do not require singular-value separation. The cusp budgets are uniform after summation, but the selected radii need not vary continuously. The extraction-independent full correction remains unchanged.

## 17.6. Arithmetic

The main term is still `L_{m,R}` in the radius-uniform theorem and `c a_R g_{Omega_R}` at fixed radius. The new estimates do not prove that every concrete section residue is zero. No residue is omitted or replaced by a unit coefficient. The exact section normalization and the distinct roles of collision count m and return index n are retained.

## 17.7. Weighted sources

The complete height theorem applies to all bounded measurable insertions by pushforward domination, including bounded path tests. The germ and jump--cusp construction applies to the existing finite-record subanalytic class; a uniform BV budget for a family requires a specified joint subanalytic description. These different scopes are stated separately. The continuous singular smoothing estimate is valid for that whole germ class. A weighted pointwise LLT and a general pointwise-roof conditioned path bridge still require the corresponding jump and residual cancellation estimates.

## 17.8. Independent specialist review

No independent human audit was obtained in this author revision. The new specialist map asks for direct checks of the endpoint Schur inequality, injectivity for each center word, the linear auxiliary-graph format, the nonasymptotic component theorem with dimension growing in m, the Gauss-map coarea bound on nonconvex branch images, full-source domination, and the jump--cusp trace matching. Finite tests and a successful build are not substitutes for these checks.

## 17.9. Route and preservation

The new introductory paragraph points directly to the two new sections and states their conclusions and boundary. All 93 inherited core modules and all 111 inherited Python files remain byte-identical. The previous main file, response, proof ledger and manifest are archived under provenance. All inherited mathematical labels and the compiled A--X synopsis remain. The title and original four-coordinate raw-density target are unchanged.

## Technical comments

Roof bandwidth B is not a collision derivative entry B_m. Null components are set to zero before any mass division. Full variation mass is used throughout. Finite jump traces are intrinsic; divergent trace assignments are unnecessary for the physical components by the new theorem. Localization of positive exponents controls height directly, whereas localization of jumps only controls mass. The cusp bound does not control q_l'' or the finite residual inverse. Every use of the arithmetic transition theorem still fixes B before m tends to infinity. No parameter continuity of localization radii, unconditional residue triviality, singleton-to-packet replacement, or pointwise conditioned bridge is inferred. The previous generic constructible germ results remain valid in their larger class; the new exclusion specializes them using physical geometry.

The new complete article is submitted for review of these direct full-source estimates and their role in closing the remaining jump and residual cancellation problem.
