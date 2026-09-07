# Referee Report — Round 20 (No-Revision Reconsideration)

**Paper:** A2 — *Homological Liouville Path Ensembles and Projective Empirical-Process Large Deviations*  
**Branch inspected:** `revision/round19-referee-positive-closure-11paper-2026-09-02`  
**Branch head inspected:** `4eb32f8ff66dbb93edaabcf96d8c62bf06f13bc2`  
**Active mathematical source:** `ROUND17_POSITIVE_CLOSURE.tex`  
**Active source blob:** `fe06bcbaeacd2ecf202d36648ba31626048d132a`  
**Prior detailed report:** `REFEREE_REPORT_ROUND18_GPT56_PRO.md`  
**Date:** 2 September 2026  
**Editorial recommendation:** **REJECT WITHOUT RECONSIDERATION**

## 1. Reconsideration status

No revised A2 manuscript is present on the declared revision branch. Its active theorem module has the same blob as the Round-Seventeen source reviewed previously. No corrected countable-branch estimate, Banach-space construction, computer-assisted proof, Dolgopyat argument, branchwise integration-by-parts proof, or revised LLT has been added. The previous detailed report therefore remains fully applicable.

## 2. Unresolved fatal defects

### 2.1. The branch-complexity hypothesis is still impossible as written

Item (iii) of `thm:r17-a2-bundle` still sums positive `C^4` roof norms and Jacobian-type norms over infinitely many branches with a growing factor `e^{\eta r_h}` and no compensating branch measure or inverse-Jacobian weight. For a countable induced map this cannot be the claimed finite complexity estimate unless the symbols mean substantially different weighted quantities, which are not defined. The proof later relies on exactly this invalid display to sum differentiated amplitudes and boundary pieces.

### 2.2. The uniform anisotropic bundle and certificate implication remain unproved

The paper still names parent labels, one-sided fold traces, Young magnets, a growth lemma, Keller–Liverani perturbation, and a finite parameter atlas without writing the common branch index, transport maps, strong/weak inequalities, compact embeddings, branch-birth rules, or parameter differentiability needed for a radius-uniform bundle. The JSON certificate is not integrated into a reproducible proof with interval equations, rounding model, covering argument, and an exact cohomological cancellation identity. A temporal derivative gap for two branches is not by itself the stated global arithmetic obstruction.

### 2.3. The high-frequency analysis is still a programme

`lem:r17-a2-ibp` continues to omit the branch domains, smooth partition with uniform derivatives, boundary-term formulae at singularity and homogeneity cuts, phase-coordinate Jacobians, derivative-growth estimates, regular-block large deviations, and treatment of the central insertion. Recording a boundary distribution in a trace component neither cancels that boundary contribution nor grants it `|b|^{-M}` decay. The asserted two independent coarea coordinates for every exceptional word are not proved.

### 2.4. The frequency split remains circular

The very-high-frequency argument still produces `C_M e^{c_M n}(1+|b|)^{-M}` and then chooses `M` so that an inequality involving `c_M` holds, without any bound on the growth of `c_M` with `M`. Repeated billiard differentiation can make those constants grow rapidly; existence of such an `M` is not a formal matter. The medium-frequency Dolgopyat estimate is likewise asserted from one UNI pair without the cone, cancellation, nonconcentration, and anisotropic norm proof required for this family.

### 2.5. The raw LLT and conditioning theorem therefore remain unavailable

Without the compact-minor-arc spectral estimate, medium-frequency Dolgopyat bound, and valid integrable high-frequency majorant, raw Fourier inversion has no proved complement estimate. Full covariance nondegeneracy and absolute continuity in the roof coordinate are also not established. The conditioning corollary still ranges beyond the central window stated in the LLT.

## 3. Editorial consequence

A genuine resubmission must replace the impossible branch sum, construct the parameter-uniform anisotropic bundle, embed a verifiable arithmetic/UNI proof, and provide complete quantitative Dolgopyat and branchwise-IBP estimates with controlled constants. No such revision exists on the inspected branch.

## 4. Recommendation

**Reject without reconsideration.** The unsmoothed four-dimensional local limit theorem remains unproved, and the manuscript is unchanged.