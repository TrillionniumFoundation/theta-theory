# Response to the external referee: A2-DYN revision 63

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v62-external-top4-review-2026-10-10/REFEREE_REPORT.md`.  
**Review commit / blob:** `0ed5b59fdcf9e4f38e621307da4a864cc5a83c8b` / `4d0a4e354df2b7f7b14667332b0a40c2c959160f`.  
**Reviewed author commit:** `45425f65832e3f1e69336c791de5fc32f8ed22bb`.  
**Frozen complete v62 paper tree:** `14b9b23b4048ed810f098c8d78aa92ed92ddfa0e`.  
**New full manuscript:** `papers/A2-DYN-v63-referee-response/main.tex`.

We thank the referee for separating the genuine finite-count source estimates from the ordered central-scale problem. This revision addresses the v62 report, including its review of the v61 determinant and transverse-coarea inputs. It retains the title, original Lorentz trajectory, exact return and displacement labels, collision count, arithmetic transition kernel, and unrestricted pointwise endpoint. It does not substitute the successful Markov realization for the Lorentz source.

The principal addition is quantitative control of a buffered geometric caustic reference. Two new modules, 135 and 136, give complete proofs. Their constants are explicit in collision count and incidence cap, but are very large. The revision does not identify that achievement with the ordered height closure demanded in sections 30.1 and 30.2.

## 30.1. Ordered incidence height

The exact inverse-incidence identity and the original first-incidence bound remain unchanged in module 131. Their exponential count factor is not removed by the present proof. We retain the required order: fix the reconstruction band, let the collision count tend to infinity, and only then enlarge the band. In particular, no exponentially count-dependent choice of the band is made in a local-limit assertion.

The new positive localization continues to retain every low incidence after a first clearance. The same actual-source inequality `1_{min_i c_i<chi} <= (m+1) chi I_m` pays that piece. This does not reclassify it as the first-incidence source and does not establish its ordered central-scale smallness.

## 30.2. The complete clearance source

The exact three-way positive partition is retained: later low incidence, capped source near the reference caustic, and capped source away from it. The new determinant lower bound controls the third part. The middle part remains the complete original positive restriction; there is no signed cancellation, averaging of its roof, or deletion of a caustic tube.

The order-two finite-type carrier of module 133 is preserved but is not called the whole rank-zero source. The new tube estimate is used only for a mass bound, not an essential-height bound. Thus this item is advanced through a quantitatively specified remainder, not recorded as fully closed.

## 30.3. Count and cap dependence of the caustic geometry

This is the main mathematical response. For a fixed constant C0 determined by the finite algebraic format, the new budgets are

`E_m = ceil(2^(C0 (m+1)^16)),  K_m = 2^E_m`.

The source is capped at chi. The reference is the critical image of the specified weak-first-hit graph at cap chi/2. It contains the corresponding physical caustic; equality is not asserted. The use of this larger reference is explicit and enlarges, rather than discards, the retained positive source. No source measure is placed on the overcover.

The proof has four parts.

1. **Graph format and critical strata.** The auxiliary contact variables and first jets are retained instead of eliminating intermediate collisions. Each word has O(m) variables and fixed-degree atoms. The exponentially many word formulas reuse the same variable blocks. Integer coefficient bit lengths are polynomial in m; the triangular coefficient sqrt(3) is represented by one algebraic variable. The weak graph is compact under a positive cap. Simple selected roots preserve the jet identities on weak first-hit boundaries. On every fixed-radius seam/rank stratum, dZ is nonzero, dF is proportional to dZ, and F is constant along every path. Continuity identifies the constants across stratum junctions. The same sign-component bound also controls the number of interval components in a horizontal-strip projection.
2. **A positive scalar modulus.** Lemma `lem:v63-effective-modulus` applies a pinned effective real quantifier-elimination theorem, including coefficient-bit control. It then proves the lower modulus directly from a nonzero integer leading coefficient of a polynomial on the graph. Monotonicity handles the rest of the parameter interval. No unproved quantitative Puiseux statement or continuity of a cap-dependent distance is used.
3. **Buffered separation.** If source points with caps chi_l tend to a critical point, that limiting point belongs to every sufficiently late reference with cap chi_l/2. This is why the cap buffer is present. The literal infimum formula uses a bounded number of quantifier blocks. The result is `(chi d)^E_m <= K_m (abs(abs(Z)-R)+abs(J))`, uniformly in the real cap and radius, where d is the clipped parameter-roof distance to the buffered reference.
4. **Tube modulus without integrating a definable function.** A second positive infimum asks for the least horizontal width that permits a vertical interval of a specified length. Interval inclusion is written with one universal scalar and one existential collision graph block. Fixed-radius finite fibers prove positivity. Effective elimination gives `sup_R length(h-tube) <= K_m chi^(-1) h^(1/E_m)` after one enlargement of C0.

Consequently the separation and tube quantities for this **buffered overcover** may be taken as

`N=E_m, C=K_m chi^(-E_m), D=K_m chi^(-1), beta=1/E_m`.

These are not claims about equality with the old unbuffered physical caustic. They supply controlled replacements in a new exact-source localization. They quantify previously unspecified dependence, but their growth is not compatible with a claimed vanishing central error at fixed reconstruction band. That remaining analytical distinction is displayed after the theorem.

## 30.4. The unrestricted pointwise arithmetic theorem

Module 136 gives, under `4 K_m epsilon <= (chi h)^E_m`,

`ess sup_t sum_{n,k} |b_clr - b_hat_cau| <= C M A^m [(m+1)chi + K_m epsilon (chi h)^(-E_m)]`.

Substitution into the inherited positive raw-error identity leaves the original signed canonical arithmetic reference G and the original positive caustic source. Exact-label restrictions are dropped only for positive domination and then restored as a disjoint partition; there is no factor counting targets. The section normalization is introduced once. The full pointwise LLT flag remains false: the caustic height and the ordered incidence/clearance estimates have not been proved here.

## 30.5. Exact-roof consequences

No unrestricted same-roof bridge, forward essential likelihood limit, or pointwise roof-conditioned path law is deduced from the new mass estimate. The fixed-radius arithmetic residues and zero classes are unchanged. The sum of variation densities in the coarea theorem is not probability TV; the factor one half in probability TV is retained elsewhere. No conditional probability is assigned to a zero arithmetic denominator.

## 30.6. Independent specialist verification

No independent human specialist audit has been obtained in this author revision. The new audit map distinguishes the inherited contact determinant, physical graph, implicit jets, rank strata and positive source partition from the imported effective elimination theorem and the elementary coefficient argument. The finite checks do not run real quantifier elimination and do not certify continuum geometry. The exact-SHA build is reproducibility evidence only.

## 30.7. Principal contribution and article architecture

The original pointwise target and the complete integrated arithmetic/bridge results remain in one manuscript. No valid inherited proof has been deleted. Modules 131-136 are adjacent at the start of the physical-source route. The compiled article now contains a six-row dependency table for these modules, so that the new local analysis can be audited without first traversing the pressure and model-realization chain. The number of leading theorems is unchanged. All 134 inherited core modules, 183 Python files, compiled appendices, 1788 mathematical labels, and the A-X synopsis are retained.

## 30.8. Quantitative novelty and primary sources

Effective quantifier elimination and coefficient bounds are standard inputs; the bibliography pins Basu--Mohammad-Nezhad, Theorem 4 in arXiv:2211.10034v2, with the published Forum of Mathematics, Sigma citation. The proof does not advertise a new elimination algorithm. Finite fibers alone, without coefficient and format bounds, do not imply the printed count/cap budgets.

The contribution within this paper is the controlled-format Lorentz graph, the buffered cap construction that stabilizes the positive separation modulus, the interval-inclusion formula for the tube, and their insertion into the unchanged exact-label source identity. The conclusions are distinct from a fixed-observable collision or suspension local limit and from the finite-state Markov height theorem. No historical-priority claim or assertion of top-four acceptance is made.

## Technical comments 1-30

The inherited finite-type order and its variable-coefficient derivatives remain untouched. The new notation distinguishes epsilon, chi, h, the band B, the collision count m, and the effective budgets E_m,K_m from the old derivative thresholds. Weak first-hit inequalities now define an explicitly named geometric reference as well as a counting overcover; this changed use is stated before its first appearance. It never creates a new physical source. The image mark j+1 and the full two-sided roof remain visible. Parameter-roof distance, positive cap buffering, exact-label domination, later incidence, separate mass and height assertions, zero arithmetic classes, and the fixed-band order are all stated locally. The source/build and specialist-verification boundaries are separate.

The revision is offered for further substantive review of these quantitative physical-source reductions together with the retained unrestricted pointwise problem.
