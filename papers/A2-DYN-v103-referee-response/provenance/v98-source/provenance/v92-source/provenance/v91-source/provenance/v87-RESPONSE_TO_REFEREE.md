# Response to the external report on A2-DYN revision 85

**Author:** Qian Qi. **Revision:** 87, 12 October 2026.

**Controlling report:** `reviews/a2-dyn-v85-external-top4-review-2026-10-12/REFEREE_REPORT.md`, commit `af90a4e75bb4262cf16e64ff5e62a688bc21c007`, blob `86ecdfdf87d9ad7f6ecbe20c97f10cc75967eec5`.

**Immediate author baseline:** the already completed v86 revision at `1fdba61e1d541339b9c7b55d417bbfbb70ca886d`, paper tree `bc6482866a2375d1d7ec1371bc660b084948de26`. The latest visible external report at initialization was v85. This revision continues its response on top of v86; it neither overwrites that work nor represents it as a new external report. All 201 inherited cores and the complete preceding article are preserved.

We thank the referee for insisting on an estimate valid before microscopic cutoffs are removed. The new envelope has this quantifier order. It treats **all** optical sensitivities on a complete geometrically specified initial family, whose gradient and total-residence thresholds both tend to zero with the roof width. This is distinct from the high-sensitivity sector already estimated in v86. The resulting scalar theorem keeps the complementary mass as its original weighted starting source rather than enlarging it to an optical potential. The model, exact labels, guard, section, source normalization, arithmetic reference and pointwise target are unchanged.

## 19.1. Fractional optical concentration

Modules 202–203 prove an actual finite-count envelope. The positive-density trace lemma applies the fundamental theorem of calculus to `A^(1/p)`, where `A=omega/(4 pi c_* chi)` is the exact angular density. The longer side of each maximal regular segment supplies an interior reference interval. Radial growth keeps its joining paths above a controlled positive gradient. The Borel segment bijection converts the complete sum of these trace energies into the actual `I_m^p` volume source with multiplicity one.

The two Holder inequalities in Theorem `thm:v87-trace-drift` then control the whole reachable optical drift of this initial family, not merely its positive density change. All internal incidences and all sensitivity values are included. The finite-count spectral remainder is displayed explicitly in `eq:v87-finite-drift`.

For `p=33/32`, initial gradient at least `h^(1/128)` and total residence at least `h^(1/64)`, Theorem `thm:v87-moving-envelope` gives

`sup_(m,R,n,k) m^2 ||V_h^reg||_infinity <= K h^(31/1408)`.

One admissible auxiliary band remains fixed for the whole estimate. This is not obtained by taking separate fixed-width collision limits and then summing them. Both physical thresholds shrink before the collision limit, and the bound holds for all finite counts and all sufficiently small widths simultaneously.

The original fractional charge is not declared zero. The new theorem pays a larger, differently selected physical variation sector and removes it from the direct scalar proof. The complementary starting mass is charged explicitly in module 204.

## 19.2. Zero residence concentration

The new trace bound requires a positive amount of total residence relative to the current microscopic width, not a new word or guard. Its reference interval can lie backward or forward on the same maximal segment; a trajectory near a true forward exit is handled by its long backward side. No continuation through that exit is assumed.

For the surface term we retain the existing theorem at every fixed positive residence cutoff, with its cutoff-independent leading constant. At each fixed outer width `h`, its application uses `delta(h)=h^(1/64)` before the collision limsup. It is never applied at cutoff zero. Shorter segments are paid by their **original weighted starting mass**, with all endpoint types retained, rather than by a claimed boundary-height theorem.

The new residual source is precisely

`R_h^epsilon(t) = integral W^epsilon 1_{z<h^(1/128) OR ell<h^(1/64)} dmu_t`.

The union does not double count, and includes grazing as well as nongrazing forward endpoints. It is therefore distinguished from the earlier `q_delta`, which selected nongrazing forward ends. Neither source is replaced by a boundary collar or a pooled occupation event.

Theorem `thm:v87-original-localization` proves that the full original bad-source height differs from the ordered charge of this restriction by at most `C epsilon^(1/16)`. This is a localization theorem, not a proof that the residual charge is zero.

## 19.3. Scalar pointwise theorem and downstream laws

Theorem `thm:v87-endpoint` proves the two-sided squeeze

`R_{epsilon(B),M} <= E_M + C_M B^(-1/192)`,

`E_M <= R_{epsilon(B),M} + C_M B^(-1/192)`.

Consequently the original pointwise error is exactly the outer limit of the original exceptional-source charge. Unlike earlier sufficient optical-majorant conditions, this criterion is an equivalence for the original target. The squeeze does not require the smooth guard function to be monotone.

The argument splits starting sources **before** estimating exits. On the exceptional source, exit and survivor are disjoint and their defect is bounded by the original weight. On its complement, nongrazing first-exit traces are retained and their pullback cost is paid by optical variation. The complete source-shift inequality, not a smoothed target, then gives the result.

The vanishing of the remaining charge is not established in this revision. Thus the raw pointwise theorem and its unconditional same-roof path, clock and likelihood consequences are not marked proved. Positive-reference normalization and arithmetic zero classes are unchanged. The previous sufficient pairs remain valid in the complete preserved article; we do not claim that its larger optical charges have vanished.

## 19.4. Specialist verification

The v85 report and complete v86 response were read in full. The new proof was checked directly against the active v86 source, the Borel segment and residence theorems in modules 196–197, the actual mixed moment in module 199 and reachable-fiber comparison in module 201, as well as the explicit geometric, source-shift and scalar inputs restated in the journal.

The new trace argument is written in full and does not import a hidden surface spectral estimate. Its load-bearing checks are: local absolute continuity of the physical angular density; the `A^(1/p)` derivative; the Borel longer-side choice; the radial lower bound on the reference paths; multiplicity one after the angular sum; the complete, untruncated `I_m^p` source; and the pointwise payment of each exceptional starting state.

The existing Demers–Pene–Zhang local-limit reference was checked as primary background on anisotropic billiard estimates, not treated as a proof of the repository's four-record or new trace statements. No independent human specialist audit or formal proof certification is asserted.

## 19.5. Reusable envelope and explicit parameters

Lemma `lem:v87-positive-trace` is a positive-density trace theorem independent of the billiard. Theorem `thm:v87-trace-drift` records its complete physical application with the full finite-count remainder. The final paragraph of module 203 states the general exponent condition: for `a(h)=h^xi`, `delta(h)=h^upsilon`, put `b=max(2xi,upsilon)` and require `b<1` and `(1-1/p)(1-b)-xi>0`.

The explicit exponent `31/1408` is one admissible value, not an optimality claim. Unlike a conditional Dini criterion, this envelope is established for the stated source using the retained mixed-moment input. Its exceptional-source complement remains the exact proof obligation in module 204.

## Expository comments 20.1–20.10

The distinction between a cutoff-independent leading constant and a zero-cutoff theorem remains explicit. Endpoint roofs carry subscripts `a_j,b_j`; the gradient threshold is `a(h)` and total residence is `ell`, with the distinction stated at definition. The common fiber/product null-set convention appears at first use. The finite physical residence-band sum remains in the inherited proof; no infinite band sum is moved through a limsup.

The critical-band exponents and every preceding proof are preserved. The new theorem displays its own exact exponent arithmetic and both directions of the original-source squeeze. The prior equivalent sufficient pairs remain identified in the closing paragraph. The corrected offset convention and the superseded notice for module 189 remain active in the supplement, with source bytes intact. Build and finite fixtures remain separate from proof-certification language.

The abstract names the remaining original-source zero-charge requirement explicitly. The title, principal pointwise objective and journal target are not replaced. The new archive includes the complete v86 article and a page-resolved v87 dependency guide.

## Qualification

The new workflow pins the exact v86 paper tree and controlling v85 report blob, checks preservation of all inherited sources and root snapshots, compares ordinary/optimized finite fixtures, and builds both the focused article and the complete supplement with all 204 cores in the recorder union. Final source/build qualification is established only by actual successful workflow runs at the v87 author SHA. Previous v86 success and a local archive build are baseline evidence, not substitutes for that run.
