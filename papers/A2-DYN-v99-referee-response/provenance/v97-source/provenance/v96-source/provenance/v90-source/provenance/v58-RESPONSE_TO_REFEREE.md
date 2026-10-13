# Response to the external referee: A2-DYN revision 58

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling review:** `reviews/a2-dyn-v57-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Frozen review commit / blob:** `4ffcf6bea86fabad719e8d893e4ae43bbb56da26` / `8293a37ac814e4028d0af8e831102d77d245c69e`.  
**Reviewed author SHA / complete paper tree:** `8dbfac97a74e2b498c77d1afd663dd1e7db18c91` / `c379f1471b26a29a16a74b267d90c544516afbfb`.  
**Active article:** `papers/A2-DYN-v58-referee-response/main.tex`.

We thank the referee for the detailed analysis of the global transition tails and graph-coupled bridge theorem. This revision responds to that report, not the earlier v35 report. It retains the original title, circular family, actual four-coordinate return record, exact occupation and clearance conventions, complete arithmetic transition and unrestricted pointwise target. All 122 inherited core modules are unchanged. The new result addresses the report's request for a reusable spectral statement and also strengthens the actual Lorentz formula: the Gaussian shape no longer depends on the individual moving peak.

## 26.1--26.4: the two physical heights and their pointwise consequences

We checked the complete physical-source definitions in modules 104--106, the positive raw identity and height criterion in 108--109, the protected height estimate in 115, the cap-free boundary mass and weak endpoint in 117--118, and the all-resolution conclusions in 119--120. They do not already contain either missing essential-height bound. In particular the protection cost `epsilon^(-9)` cannot be multiplied by the thin mass gain `epsilon^(1/16)` and called a vanishing height estimate.

The new proofs do not make that substitution. Neither physical source is deleted, moved across a seam, or replaced by a nearby word. The incidence and clearance estimates remain required in the original pointwise criterion. Thus this revision does not claim closure of 26.1--26.4, unrestricted same-roof bridges, forward essential likelihood, or the strong critical integrability endpoint. This records exactly which assertion remains to be proved; it is not an impossibility conclusion or a replacement of the original research problem.

## 26.5: independent specialist verification

No independent human audit has been obtained. `SPECIALIST_AUDIT_MAP.md` separates the inherited continuum inputs from the new scalar argument. The pressure witnesses and the equality of Hessians at a true resonance remain load-bearing imported manuscript results. The new proof does not treat source hashing, symbolic series or a successful typesetting run as their certification.

## 26.6: a reusable flat-pressure-contact theorem and two realizations

New module 123 formulates the theorem in arbitrary dimension for probability-preserving systems. Its hypotheses are separate: a positive physical exponential-moment bound, uniform analytic visible-branch data, nonzero bounded endpoint witnesses near the zero-damping locus, and equality of the branch and physical Hessians there. The observation amplitude is not one of the nonzero-witness hypotheses. A finite cover is selected around the compact zero-damping locus, exactly where it is needed.

The new calculation retains the quadratic term lost in the v57 optimization. For the positive gap

`F_j(t)=P_R(t)-Re log(tilde_lambda_j(a_j+i*t))`,

its value, gradient and Hessian at zero are respectively

`kappa_j`, `mu_j-mu_R`, and `Omega_R-Re H_j`.

Writing `h_j=||Omega_R-Re H_j||`, nonnegativity and a uniform cubic remainder give

`|mu_j-mu_R| <= C (sqrt(kappa_j*h_j)+kappa_j^(2/3))`.

Since `h_j -> 0` uniformly as the damping tends to zero, this proves `|mu_j-mu_R|^2=o(kappa_j)`, not merely the v57 `O(kappa_j)` bound. A surviving peak with `m*kappa_j=O(1)` has a vanishing diffusive center displacement. Corollary `cor:v58-common-shape` supplies a Gaussian-weighted error modulus in the Hessian mismatch. It does not claim a polynomial count rate from a qualitative parameter modulus.

The Lorentz occupation realization is checked hypothesis by hypothesis in `cor:v58-lorentz-contact`, with references to 77, 84, 87 and 121. It includes the actual section occupation, not the constant collision step. The second realization is the area-preserving three-strip baker map, an invertible piecewise-linear hyperbolic map with singular cuts and a geometry different from the dispersing table. Its physical characteristic pairing is an exact finite exponential sum, so the pressure, visibility and contact hypotheses are proved independently of the billiard operator theory.

In that example the maximum, damping, drift and Hessian are calculated in the article. In particular `kappa_e=pi^2 e^2/9+O(e^3)` but `v_e=pi^2 e^3/18+O(e^4)`. It exhibits a nontrivial surviving damped arithmetic peak whose separate Gaussian center disappears. The example verifies the spectral principle, not a continuous-density local theorem for a finite-support observable. No broad class of unverified singular systems is advertised as an application.

## Consequence for the same exact-return law

New module 124 proves that the entire evaluated transition kernel equals, with a uniformly vanishing Gaussian-weighted error,

`Phi_{m,R}(y) * g_{Omega_R}((y-m*mu_R)/sqrt(m))`,

where `Phi=(1/c) Re sum_j exp(-i*a_j.y) z_j^m B_j`. Every original branch, amplitude, damping, phase and arithmetic zero is retained; the roof component of a moving phase is not discarded. Only the moving Gaussian centers and complex Hessians have been removed.

After the exact covariance change, the full original fixed-return law is approximated in total variation by

`n^(-2) alpha_{m,R}(k,n,u) g_{D_R}(V_{n,R})`, with `alpha=Phi/c`.

Unlike the v57 fixed-radius Gaussian specialization, this common physical-covariance formula is uniform through changes of arithmetic type. At a fixed radius its coefficient reduces to the inherited finite residue. The signed density and its normalized positive part remain distinct.

A separate proposition proves vanishing negative reference heights on exact-label central sets, using slow roof variation, positivity of the original local interval mass and the complete local `L1` error. It does not bound positive heights of the original density. The graph-bridge and full-output selection statements transfer to the new reference by variation contraction and normalization, with the same factors one half and two as before.

## 26.7--26.8: endpoint and journal architecture

We have not adopted the proposed retitling or sequel route. The paper keeps the original raw-return endpoint. The new front matter presents two principal statements and the next two sections contain the complete new scalar proof and its Lorentz consequence. The existing global-tail and joint-clock modules immediately follow. All old core proofs and labels remain compiled; the complete v57 post-title front matter is retained in a compiled appendix, and the old main file is archived verbatim.

This provides a short route through the new result, not a claim that the full source has become short or that its inherited verification burden has disappeared. The accumulated historical statements remain available for the next referee without controlling the new opening narrative.

## 26.9: theorem-level comparison

The existing DPZ endpoint cell-index theorem and DN suspension local-limit comparison remain in the bibliography and the retained literature section. They are not differentiated to obtain a roof value, and the baker example is not presented as a new discovery of a Bernoulli shift. The new result is the flat-contact implication for visible moving resonances and the resulting uniform common Gaussian shape, including the original occupation arithmetic. The weaker quadratic drift bound allows nonzero displaced Gaussian shapes at inverse-count damping; the new bound rules them out under the additional contact hypothesis. The novelty claim is confined to this proved implication and application, not an assertion of priority for positive-pressure domination, Taylor optimization or Markov-kernel contraction.

## Technical comments 1--25

Comments 1--5: equation `eq:v58-cell-bookkeeping` displays `O(n^2)` unit cells and `m^(-2)=O(n^(-2))` together. The limit variable is fixed return index `n`; collision count `m` is summed. The transition remains signed, its negative mass vanishes, and its probability reference is explicitly normalized. Fixed-radius zero residues are retained.

Comments 6--11: the record is independent of the **coupled pair**, not of two independently sampled bridges. The mixed norm is observation variation and path bounded-Lipschitz dual. A record-only kernel retains its entire output and selection event. Path-reading selection is excluded. The condition `r_n>Delta_n` and convergence requirement `Delta_n/r_n->0` remain visible. There is no inferred polynomial or microscopic selection rate.

Comments 12--16: all pressure arguments use a fixed complex neighborhood. Physical witnesses are distinct from `B_j`; finitely many witness neighborhoods cover the zero-damping set. The accretive domain and determinant branch are specified. Source fourth-moment tightness and reference Gaussian tightness remain separate inputs.

Comments 17--25: common reference shape and asymptotic reference positivity do not imply physical essential-height control. The old exceptional-set result and the global record result remain distinct. Conditional pair-bridge convergence in record mean is retained, not promoted to every prescribed roof. Probability TV retains its factor one half. The source normalization occurs once; the second `1/c` in `alpha=Phi/c` is the explicitly calculated covariance/count-scale conversion, not a second change of source. Occupation remains at `0,...,m-1`, and flight clearance is read at `j+1`. Exact-source evidence is separate from proof verification. All unresolved height and independent-review flags remain false, and provenance material is outside the new principal proof route.

## Reproducibility

The v57 baseline has two successful exact-SHA runs, `37915773999` and `37915793125`. The downloaded response artifact `11609473217` has archive SHA-256 `7dd8f4b116cc3849b709e507f28a9c62c38206daacf531e3b31e61ea1ed34776`. These are baseline evidence, not v58 execution evidence. The v58 workflow checks its own event SHA, full source tree, unchanged inherited files, report blob, finite diagnostics, native build and theorem-page renders. The dynamic receipt, not this static response, records the successful new execution and PDF hash.
