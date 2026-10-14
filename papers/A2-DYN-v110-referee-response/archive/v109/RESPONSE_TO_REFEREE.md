# Response to the controlling revision-108 report

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revision:** 109  
**Controlling report:** `reviews/a2-dyn-v108-canonical-capacity-external-top4-review-2026-10-14/REFEREE_REPORT.md`  
**Frozen review commit / report blob:** `e863e8c110ffee472b3d10163a129a2bcfe9c0e1` / `5080564a78a192984acc272bc31c7ef8165bda4e`

We have retained the original problem, section, guard, normalization, exact occupation and displacement labels, finite-peak arithmetic reference, and essential-height topology. The complete prior packet is preserved byte-for-byte under `archive/v108`; the old author directory and all reports are unchanged. The journal-facing article is now a single exposition, not a shell that adds further hooks to an accumulated article.

## 1. The principal mathematical request: a physical scarcity estimate

The report correctly distinguishes construction of an optimal scalar allocation from proving abundance of the available physical capacity. Revision 109 does not add another certificate class. It proves a geometric endpoint theorem on the actual Lorentz trajectories and a quantitative estimate for one entire physical component of the canonical shortage.

### Actual optical action and a marked bound

Module 260 derives the second variation of the broken-path action with all collision angles in their actual orientation. Its interior Schur complement is the endpoint Hessian. In particular,

`(9 sqrt(19)/200) I <= D_q^2 F <= (47/6) I`.

The optical denominator is the positive `(1,2)` entry of the product of free-flight and reflection matrices. Writing `varrho = 47/59`, the exact identity and bounds are

`omega = R c_0 c_m / b_m`,

`omega <= (47/6) varrho^(m-1)`,

`omega/c_j <= (2209/72) varrho^(m-2)` for every visited interior collision.

These are proved on the original trajectories without a lower incidence cutoff. The resulting estimate for the full inherited insertion is `omega I_m <= 500 varrho^((m-2)_+)`. We explicitly do **not** sum this wordwise estimate over collision words and declare a local limit bound: that would require a separate physical summation theorem.

### Endpoint passage is proved rather than assumed on an unspecified subspace

The reduced Hessian has a continuous formula with no inverse incidence. The relevant inverse matrix is `Z^-1`, where `Z >= 2I`, even when visited incidences tend to zero. At constant Gauss angle, `dq/dz = G^-1 e` and `2 lambda_circ <= d(z^2)/du <= 2 Lambda_circ`. This proves existence of the endpoint coordinates and integrability of `1/z` up to both physical ends, including a critical incoming end.

The finite visited trajectory has one-sided limits by the flight quadratic and continuity of reflection. Its clearance limits exist as well. Thus the original coarea trace has a finite limit on every positive-length segment in the inherited pairing space. The regular-point weighted derivative estimate has an integrable majorant there, so its passage to the endpoints is established. A per-sheet one-half Holder bound is also proved.

These results do not reconstruct the inherited global incident-component pairing model or re-prove the spectral averaged estimates; those dependencies are stated explicitly in Section 2 of the current article.

### Visited grazing versus an unvisited third-disk tangency

If an endpoint limiting trajectory has an actually visited interior grazing collision, the marked optical estimate forces `omega -> 0`. The endpoint trace vanishes, and the original positive paired minimum on that entire segment is exactly zero at every finite count.

This is **not** asserted for an unvisited third-disk tangency. There the guard can have `W=1` while all visited incidences and the optical density remain positive. These tangencies, section cuts, nongrazing critical entrances, flat sheets and short-reach sheets are all retained.

A zero paired minimum also does **not** imply zero comparison capacity. On the visited-grazing class `Gamma`, the endpoint maximum equals the full endpoint difference. Module 261 therefore keeps that capacity and proves

`P_r^gr(t) <= C (1+epsilon^-1) integral_[t-Delta,t+Delta] v^0(u) du`.

After the complete one-copy physical sum and in the required limit order,

`H_M(K_B P_rB^gr) <= C_M B^(-95/384)`.

For the original microscopic source and the complete and nongrazing-only pools, respectively,

`0 <= R_B^ng - R_B^full <= K_B P_rB^gr`.

The concrete outer choices are `h_B=delta(B)/2`, `r_B=delta(B)/8`, `Delta_B=8 delta(B)` and `K_B=max(1,epsilon(B)^(-1/32))`. They are all fixed before the collision limit. Consequently the change in the original shortage caused by removing the complete visited-grazing capacity has ordered height `O(B^(-95/384))`.

### Exact status of the organizing theorem

The current conclusion is

`E_M <= H_M(R_B^ng) + C_M B^(-1/384)`.

The original raw pointwise assertion is equivalent to decay of this **same-source**, two-nongrazing-ended shortage. No collision-uniform estimate proving that last decay is claimed. In particular, positivity of every endpoint incidence at fixed count is not promoted to a count-uniform lower incidence bound.

Thus the revision completes the visited-grazing component of Route C and the specified finite-itinerary endpoint trace passage. It does not claim closure of the report's principal capacity-abundance request on all nongrazing microscopic segments. The outstanding positive weights and the exact remaining limit are displayed in the main theorem and the appendix. The topic and target have not been replaced by a standalone allocation problem.

## 2. Specialist audit obligations in Section 17

The new derivation addresses existence of the finite endpoint traces, local-to-closed-segment absolute continuity, the endpoint passage of the weighted variation estimate, and critical/visited-grazing limits on the inherited physical pairing space. It supplies a positive matrix representation whose sign, incidence factors and continuous extension can be checked independently.

The global pairing construction, original one-copy coarea identification, common roof versions, and spectral/pressure inputs for the fixed-window averages are explicitly retained inputs, not certified by numerical checks. The limiting order is stated in Section 2 and used without a collision-dependent cutoff in the grazing payment.

## 3. Point-by-point response to the seven minor requests

1. **Source outside a restricted comparison subspace.** Section 6 states that it remains in the original source and can receive the global roofwise fraction. It is not described as retained with coefficient one.
2. **No individual-sheet coupling.** Both the allocation paragraph and Proposition A.1 state directly that the allocation is scalar at the roof, not a coupling of individual source and comparison sheets.
3. **Displayed width condition.** Proposition A.1 displays `0 < r <= r_old` together with the length and total-cost conditions.
4. **Strictness scope.** Proposition A.2 states in its heading and statement that the old class uses roof-independent angular source blocks and translated entire source intervals. It expressly distinguishes the interval diagnostic from a Lorentz realization.
5. **Explicit comparison space.** Equation (5.1) specifies the entire original positive-length incident-component pairing space. Theorem 4.3 supplies the trace and endpoint-variation properties used on it. No unspecified singular trace exclusion is hidden in the definition.
6. **Later v108 qualification.** `provenance/v108-qualification.json` records the two jobs' later successful completion. The controlling report's freeze-time observation that they were queued is unchanged.
7. **One current validation summary.** `VALIDATION.md` is the current summary. The old validation headings occur only in the clearly named, byte-preserved archive; they are not active v109 status records.

## 4. Preservation and verification

The original problem file is reused with its exact blob `6af1dcb4548e1b5dd82b9a330dead6e04fd09797`. The complete old packet retains tree `e66a1dec484f419d88c05f12a7e2ec5310430448` both in its original location and in the new archive. There are 259 preserved historical core modules and two new ones.

The current article compiles independently. The exact-checkout build also assembles and compiles the preserved historical article and supplement, checks recorder coverage, and retains the inherited narrowly scoped TeX-log audit for those historical documents. Normal and optimized finite diagnostics check optical matrix identities, Schur complements, continuous grazing limits and the positive-part residual inequality. They are reproducibility checks, not a formal proof certificate or evidence of uniform capacity abundance.
