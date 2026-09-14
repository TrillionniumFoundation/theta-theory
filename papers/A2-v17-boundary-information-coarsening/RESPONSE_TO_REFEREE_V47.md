# Response to the independent referee report on A2 revision 46

**Author:** Qian Qi  
**Revision:** 47, September 14, 2026  
**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*

The report addressed is `reviews/a2-v46-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md`, frozen at commit `45b42eee377c7fd3cff81c24c95acb91d6f46ab6`. Its reviewed mathematical source is `ab99196fadc20682c1ee44d6bb433a788c7274ab`, with the final 243-page main and 7-page companion. The new author branch is `revision/a2-v47-calibration-aware-histograms-2026-09-14`, based on the report commit, not on an older default-branch manuscript.

We thank the referee for distinguishing a mathematical objection from an editorial assessment. In particular, the report credits the quantitative inverse from finite transverse-law histograms to the complete periodic table and unknown marked lattice, and does not identify a fatal error in its fresh proof coverage. This revision does not reinterpret that finding as an unresolved quantitative-inverse gap. It addresses the concrete calibration clarification and gives a proved extension at precisely that acquisition interface. The original inverse and its scope are retained.

## R46-P1: exact-offset bias, amplified timing error, and hard categories

**Requested clarification.** The finite-flight term next to equation (19.19) is conditional on exact signed contact charts and the true fixed offset. It should not also be read as a bound for timing or chart error. The existing same-flight physical pilot is not refuted by this observation.

**Change at the requested location.** Immediately after equation (19.19), within Corollary 19.6, we now state that `b_j` accounts only for finite-flight error in those exactly calibrated laws. We print the actual offset `d_0+j(ghat_e-g_e)`, distinguish hard-cell crossing error, and refer both to the existing observable-calibration theorem and to the new calibration-aware theorem. No hypothesis or conclusion of Corollary 19.6 has been withdrawn.

**A proved acquisition extension.** Sections 19.7–19.9 give two lemmas, a theorem, and a corollary, each with its complete proof. They are contained in `article/23l_calibrated_histograms_v47.tex`.

1. **Lemma 19.7, uniform offset continuity.** For the normalized endpoint density `f_d=Z_d^{-1}w(d-A)_+`, a common positive-offset interval and forward constants give `TV(P_d,P_d') <= C_off |d-d'|`. The proof controls both the unnormalized density and its normalization using the positive-part inequality. A full-box density bound is specified, including neighborhoods outside the recorded square. An interior density bound is not silently used at its outer edges.

2. **Lemma 19.8, hard-category perturbations.** If the endpoint projection has uniform coordinate error at most `r`, coupling the two categories of the same endpoint pair gives vector error at most `2 min(1,H_* V_delta(r))`. Here `V_delta(r)` is the area of the sup-norm tube around all grid edges, including the outer edges and complement category. For a `q` by `q` grid we prove `V_delta(r) <= 8r(r_1+r)(q+1)`. This is not an application of a Lipschitz-test bound to indicators. It also covers an image map that puts mass on a grid edge, with the declared half-open convention.

3. **Theorem 19.9, estimated-calibration confidence reconstruction.** For a final even flight number chosen before the pilot, gap error `v_g`, clock error `v_t`, and chart error `r`, the successful categorical-law bias is bounded by

   `b_cal = 2 C_0 tau^j + 2 C_off (j v_g+v_t) + 2 H_* V_delta(r)`.

   The terms are kept separate throughout. The proof applies the same estimated projection to the finite and limiting laws on a fixed true boundary; it makes no false total-variation comparison between ambient position laws supported on different curves. The existing inverse yields

   `D(T,Ttilde) <= Omega(2 v_g, 2(u_n+b_cal)+C_bin delta)`.

   The theorem includes the marked lattice and its Gram estimate, approximate measurable selection, uniform conditioning on good pilot histories, and deterministic preparation caps. Concentration is applied to the uncapped iid successful stream before adding cap failure, not after conditioning on cap completion.

4. **Corollary 19.10, charged finite-resolution acquisition.** On the persistent compact analytic position-sensor class, the existing pilot and the new categorical estimate are combined through an explicit finite prescription. It selects an observation accuracy from equation (19.17), a finite grid, the final even `J`, a pilot resolution at that same `J`, and a finite sample size. The pilot resolution controls both `J|ghat-g|` and the grid-dependent crossing term. The displayed choices leave a strict error budget after adding a positive selection tolerance. All failed preparations are charged, and every flight in a newly acquired transcript can exceed any prescribed minimum.

The stronger acquisition corollary retains the physical sensor used by the existing pilot. Longitudinal positions are used for calibration and observable projection, not passed to the subsequent law-to-table inverse. We do not claim that unknown charts or unmarked channels are discovered from histograms alone. The referee did not require this extension to validate the old conditional corollary; it is supplied as a positive, precisely scoped strengthening.

## R46-C1–C4 and the inherited quantitative proof

The favorable findings are preserved rather than relabelled as defects.

| Report finding | Treatment in revision 47 |
|---|---|
| C1: finite histogram vectors control fixed-order density jets under the stated forward priors | Lemma 19.1 and its proof are unchanged. The original mesh term is retained. Calibration crossing error is an additional term, not a replacement for the mesh term. |
| C2: the finite Bellman recipe includes lower-order remainders and finite conditioning constants | Lemma 19.2, the complete lower-order recursion, the finite smooth-remainder justification, and the graph-to-support conversion are unchanged. |
| Continuation and noncircular finite accuracy prescription | Lemma 19.3, Theorem 19.5, and equation (19.17) are unchanged. The new physical prescription starts from those explicit tolerances; it does not replace them with a compactness separation constant. |
| C3: arbitrary finite asymmetry witnesses and common-frame lattice registration | Lemma 19.4 and the generic skeleton, common-frame cochain, nonunimodular gain-matrix inverse, and representative correction are unchanged. No lattice metric is supplied to the new estimator. |
| C4: categorical concentration, selection, and charged caps | Corollary 19.6 retains its conclusion. The added theorem repeats the conditioning and cap argument at the actual estimated-calibration laws, with a separate pilot failure term. |
| Earlier zero-net-gain backtrack correction | The corrected v46 generic-registration text is unchanged. No individually zero-marked edge is imposed. |

The exact local signed inverse, generic `N+1` channel result, intrinsic global rigidity, conditional quantitative inverse, local statistical experiments, physical reconstruction, auxiliary proofs, and full two-collision companion all remain active. There is no narrowing to symmetric contacts, a special harmonic family, a known lattice, or a finite-dimensional boundary model.

## R46-E1: contribution and the requested journal standard

We take the significance objection seriously, without treating it as an algebraic claim that can be marked proved by another diagnostic. The paper's central mechanism remains the nonlinear relative long-bridge profile and its signed smooth finite-remainder inverse. The geometric consequences are complete analytic obstacle reconstruction, generic finite-channel availability, and recovery of an unknown marked Euclidean lattice in one common frame. The quantitative and statistical results explain how that mechanism survives specified losses of observation and finite acquisition.

The new introductory subsection, `article/01h_calibration_overview_v47.tex`, makes this relation explicit. It separates the structural inverse from the classical normalization, coupling, continuation, and concentration arguments that propagate it. It also separates the transverse-law record from the richer position record. The complete previous introduction and all previous mathematical conclusions are retained; editorial correspondence and source certificates remain outside the mathematical article.

We do not present the four added environments as four independent major breakthroughs, or the five additional main-manuscript pages as evidence of significance. Nor do we claim that this revision settles the referee's placement judgment. The strengthened theorem and clarified architecture are offered for renewed substantive assessment at the requested level. No sharp minimax theorem, fixed-finite-scalar exact reconstruction, unmarked discovery, or reduction to an enriched marked length spectrum has been invented to close a moving checklist.

The observation-specific literature distinctions remain as printed. Finamore–Leguil's enriched marked length datum is not identified with the selected endpoint-law datum. The version-sensitive Florio–Leguil notice remains intact. No exhaustive priority conclusion is asserted.

## Preservation, verification, and the next review

The modified inherited mathematical files are only `main.tex` and `article/23k_quantized_law_stability_v46.tex`. Their exact v46 originals, including pinned Git blob identities, are archived under `history/v46-review-baseline/`. The first receives additive abstract and input lines plus revision metadata; the second receives only the adjacent calibration clarification. All inherited input order is preserved.

The verification script compares every entry of the frozen native active-source manifest: 101 inherited active files across the main and companion, of which 99 remain byte-identical in place and two are verified against exact archived originals and their prescribed additive edits. There are precisely two new active modules. All 233 inherited main theorem-style environments, 22 remarks and 224 main proofs remain; the new module adds four theorem-style environments and four proofs. The companion remains unchanged.

The local complete native build has 248 main pages and 7 companion pages. Source preservation and finite calibration diagnostics pass under ordinary and optimized Python with identical JSON; the inherited quantitative, adaptive, v32 and v38 diagnostics also pass in both modes. These are source, algebraic and implementation checks, not formal certification of the entire mathematics. The delivery ledger records the actual remote materialized source, complete native products and rendered-inspection scope after publication. The preparation commit is not represented as the compiled source.

The new report should be read against the complete v47 manuscript, with the exact-offset clarification on page 92 and the new acquisition proofs on pages 94–97 of the local 248-page build. The old 243-page pagination is not used for those additions. A renewed referee remains free to reassess the mathematical contribution and the journal-placement question independently.
