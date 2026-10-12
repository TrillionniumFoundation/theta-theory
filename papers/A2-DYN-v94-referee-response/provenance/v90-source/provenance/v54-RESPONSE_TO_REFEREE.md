# Response to the v52 external referee: A2-DYN revision 54

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v52-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Report commit / blob:** `b487df93e48dbf455b3ed04680c1f7ae3613f45e` / `9f50c9909cc137d67babfd69f6508de2ce3254cf`.  
**Reviewed v52 author source:** `4449ba65b59d2670fb1231515e860d874b466b87`.  
**Immediate qualified v53 baseline:** `9d3891615c3e09d8e40b7ba8e24d410ee6e9c76d`; complete paper tree `95d7b6f3239a487cf83f2690fb8acf84e14f1f86`.  
**New complete manuscript:** `papers/A2-DYN-v54-referee-response/main.tex`.

We thank the referee for isolating positive physical height as the remaining scalar obstruction. The intervening v53 revision had already addressed the technical path comments and proved whole-path exponential moments. This revision preserves that work and returns to the scalar density. It proves stronger integrability of the complete, unguarded exact-label roof density and closes the forward relative-entropy conclusion listed as unproved in the report. It does not rename finite-norm convergence as essential-supremum convergence.

## 1--2. Positive incidence and clearance sources

New module 115 begins with one fixed auxiliary roof band, independent of the protection scale and collision count. Its finite-count positive interval upper bound retains the term inversely proportional to the roof-window length. This permits the flow-box estimate to be used at a window of length proportional to epsilon^9 without substituting a shrinking window into a separate asymptotic theorem.

The high-gradient protected source has normalized height at most C epsilon^(-9)(1+m^2 rho^(m/2)). The low-gradient source is completed to its protected normal critical centers. Disjoint physical collars of roof width proportional to epsilon^6 have mass at least a_* r J_z and density at most A_* J_z. A finite-band upper comparison, with the normal-strip condition dropped only on the upper side, gives the smaller epsilon^(-6) budget. Every collar is charged once; the original exact n,k,m labels and section normalization are preserved.

Thus `prop:v54-protected-height` proves a simultaneous finite-count polynomial bound, not a family of unrelated fixed-epsilon limsups. Separately, the actual thin incidence, clearance and section strips give local remainder mass at most C(1+h)[epsilon^(1/16)+m^3 rho^(m/2)], for every width, before any limit.

At a density level L choose epsilon=(2C_A/L)^(1/9). The protected density is then at most L/2. On the source-density superlevel {P>L}, the positive unprotected remainder is at least P/2. The resulting tail-mass bound has the power L^(-1/144), plus the retained finite-count error. It is an estimate for the original density, not for a different observation event.

The error floor cannot be integrated to infinity. We use the inherited complete exponential height cap P<=C_H exp(Gamma m) and integrate the finite inequality only up to that cap. For every s<min(1/144,kappa/Gamma), the floor contributes at most C exp[-(kappa-s Gamma)m]. This proves a strictly nonempty higher-integrability range. `eq:v54-admissible-exponent` chooses a fixed interior exponent explicitly.

Module 116 then proves local L^q-smallness, for 1<q<q_*, of each positive incidence and clearance remainder, including arbitrary bounded measurable source insertions. Their all-band signed corrections have the same local norm control. This is a stronger scalar physical-source theorem than small mass. It is not either missing essential-height theorem. No trajectory is transported across a grazing or competing-hit seam, and no collision is inserted or deleted.

## 3--4. Raw arithmetic law and pointwise bridge

`thm:v54-raw-Lq` upgrades the complete scalar arithmetic local law from L^1 to L^q in the roof coordinate, for 1<q<q_*. It also upgrades the roof norm of the full bounded-Lipschitz path-valued law. The positive scalar source bounds the path measure's norm, and the actual return-clock transfer is retained on its original central target class.

The two-sided scalar essential-supremum theorem and the uniform same-roof bridge are not claimed complete. The physical positive-height criterion is still the exact criterion of `cor:v51-positive-criterion`, and the v52 path charge still makes it sufficient for the pointwise bridge. A new finite-norm theorem does not remove that hypothesis. The original title, four-coordinate return record and pointwise target remain in the article with all their proof materials.

## Forward likelihood and relative entropy

The report explicitly lists forward likelihood and forward relative entropy as unproved. The first term requires a topology. Under the same pointwise arithmetic reference floor G>=d used for the inherited reverse minorization, `thm:v54-forward-likelihood` now proves L^q convergence of dP/dQ to one for a nonempty range of q>1. It proves forward relative-entropy convergence and every fixed forward Renyi divergence with order in that range. The reverse and forward relative entropies therefore both converge to zero.

The proof normalizes the same original roof event on both sides. Higher-integrable density convergence controls the likelihood in L^q of the reference; the elementary inequality x log x-x+1<=C_q |x-1|^q then proves forward entropy. It does not assume a uniform upper likelihood. `forward_essential_likelihood_convergence_proved` remains false, and a merely positive integrated reference mass is not substituted for the pointwise floor.

## 5. Arithmetic and source identity

Every uniform formula retains G=mathcal L_(m,R), including all moving occupation peaks. At fixed radius the section residue remains in the Gaussian specialization. No residue is assigned value one. The exact return index n, displacement k, collision count m and continuous roof u are unchanged. The guard is a temporary positive subsource in a finite decomposition, not a replacement datum.

In the fixed-band upper comparison the ambient enlargement has factor 1/c. The protected flow and critical collars are still in the original section source. The terminal section membership at time m is not an extra occupation summand. These conventions are restated in module 115.

## 6. Independent specialist audit

No independent human audit has been obtained. The additional audit map pins the new finite-count unmarked spectral inequality, the polynomial protection loss, the critical-collar multiplicity, the simultaneous all-margin estimate, and the truncated tail integration. The inherited continuum inputs remain load-bearing. Source qualification, exact rational tests, negative controls and typesetting do not certify them.

## 7--8. Reusable principles and significance

The v53 signed-measure/path-transfer principle remains intact. The new `lem:v54-tail-principle` is a separate scalar principle with four independent inputs: a polynomial protected height, small positive remainder mass, an exponentially small finite-count error, and a complete exponential height cap. It proves a nonempty range of higher density moments. Each input is verified for the same mechanical source in the surrounding proof.

We do not claim that Holder interpolation or continuity of entropy under an L^q likelihood bound is new. The substantive additional input is the simultaneous finite-count protection bound and its use with the full-source cap. This is not inferred from a mixing theorem for a different observable or from the path exponential moments of v53. No additional independent dynamical model is claimed in this revision. The venue-level significance is left for the next substantive review.

## 9. Short route and full preservation

The first leading theorem now states the stronger scalar norm and forward-likelihood conclusions, with their precise exponent and reference-floor qualifications. Modules 115--116 give the short new route: one band; polynomial protected height; all-margin local mass; truncated density-tail integration; physical L^q remainders; full raw L^q convergence; forward likelihood. The original three-theorem hierarchy is retained.

All 114 inherited core modules and all 147 inherited Python files are byte-identical. All inherited mathematical labels, the 19-entry bibliography, the compiled A--X synopsis and all appendices are retained. The previous main source and metadata are archived verbatim. No old proof is silently edited, removed or replaced by an interface.

## 10. Topologies and technical comments

The v53 repairs to the deterministic matrix notation, positive dominator normalization, joint Borel selectors, signed compactness and common-null-set arguments remain byte-identical. The new scalar conclusions distinguish roof L^q, path BL* with a roof L^q norm, forward relative entropy, finite-order Renyi divergence and forward essential likelihood. No path-space total variation or new pointwise conditional law is asserted.

The protection scale may vary with m only in explicitly finite inequalities. The auxiliary Fourier band is chosen once and never varied with m or with the density level. The reconstruction bandwidth is a separate approximate-identity parameter. No rate in m is claimed for the qualitative raw or likelihood limits. The finite-error floor is integrated to the proved exponential cap before any limit is taken.

## Execution evidence

The initial v54 remote lineage commit is not a manuscript build. The complete manuscript is qualified by a dedicated read-only workflow at its own final event SHA on both branches. The verifier checks the frozen v53 tree and all reports without a local exception. Dynamic receipts identify the actual run, clean scoped source, source Merkle tree and PDF hash. Only observed completed runs are reported as successful; no static manuscript text predicts a future build result.
