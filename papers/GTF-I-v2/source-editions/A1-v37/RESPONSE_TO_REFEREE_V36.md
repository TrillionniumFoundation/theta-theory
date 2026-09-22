# Response to the independent referee report on A1 v35

**Manuscript:** *Attainable information and causal compression at exponent collisions*, A1 v36.  
**Author:** Qian Qi.  
**Controlling report:** `reviews/a1-english-v35-harsh-independent-2026-09-08/REFEREE_REPORT.md`, commit `30ea5daf9c1f5cf345061f940b55bd559e2e1686`, blob `d041356c0ca6b6a17750011717af51a7b479d380`.  
**Reviewed manuscript:** `02a19f2ddb83cf68bfbf8361c137613e2ffd3925`.  
**Revision branch:** `revision/a1-english-v36-common-normalization-2026-09-08`.

We thank the referee for the favorable assessment and for specifying the two remaining clarifications. The present revision addresses R35.1 and R35.2 in the main article, retaining its principal theorem, proof chain, finite-cell realization results and complete companion. The discussion below records the changes and current production checks; it does not represent a further referee decision or journal acceptance.

## R35.1 — One normalization for the fixed-future comparison

**Location:** Corollary 13.3 and its proof, main p. 38; `v36/spectral_comparison.tex`, label `cor:v35-fixed-future`.

The corollary now chooses **H = 16 once for all three total horizons**, and the same fixed integer **L >= 8**. It states explicitly that, at each fixed calibration, the nine normalized future nodes and the Fourier matrix are identical in the three acquisition problems. This is literal equality of the auxiliary matrices, not equality only up to a change of spectral scale.

The proof begins with the admissibility calculation

\[
5\max_{|u|,|v|\le1/16}(3+v)=\frac{245}{16}<16.
\]

The three total horizons are 3, 4 and 5. Thus H = 16 satisfies the original normalization requirement for every one of them, throughout the original calibration square; no square or horizon is reduced. With the common H, their shared two-trial normalized node list is

\[
\frac1{16}\bigl(1,2,2+u,3+u,3+v,4+2u,4+v,5+u+v,6+2v\bigr),
\]

with formal labels retained at collisions. The node list and fixed L determine one and the same auxiliary matrix independently of the past acquisition length. The acquired cutoffs remain 3, 6 and 9. All three displayed regret comparisons, both risk criteria, the exact-collision conventions, and the former proof following this calculation are unchanged.

This clarification uses the original normalization definition and the complete two-parameter derivation in `text/collision_consequences.tex`, rather than introducing a new experiment. Its positive detector, fixed full-support prior and admitted command cube are unchanged.

## R35.2 — Meaning of the flat-path crossover orders

**Location:** Remark 13.4, main p. 39; `v36/spectral_comparison.tex`, label `rem:v35-flat-path`.

Immediately after the balancing calculation, the remark now says:

> These are crossover orders of the comparison envelope, not exact optimizer transition thresholds.

The two expressions remain

\[
\rho^{-6}\asymp e^{6/\theta^2},\qquad
\rho^2\tau^{-8}\asymp e^{8/\theta^4-2/\theta^2}.
\]

They are obtained by balancing adjacent terms of the established risk envelope. The bounds are comparisons up to constants, so the calculation does not identify exact integer budgets at which an optimal controller changes. The analogous qualification already appears in the inherited two-parameter corollary and is now local to this remark as requested. No asymptotic regime, lower bound or upper bound has been removed. The determinant theorem still applies directly to the smooth flat path; only its finite-power collision-tree specialization has the additional finite-power hypothesis.

## Preservation and manuscript integration

The new repository directory is based on the complete v35 native subtree. All historical sources, the original v35 modules, earlier response documents and companion material remain in the repository. The v35 entrypoint, README and build wrapper are also preserved under `history/`.

Only the active comparison module is redirected to its v36 counterpart; the introduction, abstract, principal theorem, collision proofs, controller section, compatibility, precision and exact-instance sections are unchanged. The active source closure has 80 TeX inputs in both versions. Of these, 77 have identical paths and bytes; the remaining entries are the main entrypoint and the two selected comparison-module paths.

All 222 theorem-like blocks and 210 proof blocks remain present. Of the statement blocks, 220 are verbatim; only the corollary and remark identified above receive the requested clarification. Of the proof blocks, 209 are verbatim; the remaining proof gains the explicit common-normalization bound before its unchanged former argument. No statement or proof is deleted. All companion source files are byte-identical, and all 159 companion PDF pages have text identical to the supplied v35 companion.

The labels containing `v35` are intentionally retained, so historical references continue to identify the same results. The new paths identify the selected revision, not new theorems or an expansion of the mathematical claims.

## Current execution and production evidence

The current complete native build compiles `main.tex` and `companions.tex`, generates their actual external-label exports and checks convergence. It produces a **42-page main article and 159-page companion**. All six compiler invocations succeed, the labels stabilize after three paired cycles, the TeX-recorder inputs match the declared source closure, and the final logs contain no unresolved references or citations, changing or multiply defined labels, or overfull boxes. No reference stubs or substitute theorem statements are used.

The v35 source package was checked against its exact published source manifest: the manifest blob matches `1e5f92cf41b563779ad702c85ee440a470a689fe`, and all 80 input objects agree with its recorded Git hashes. The new build identifies its own inputs by content; its source-commit field is null because execution precedes publication. The compact repository receipt reconstructs its entire source manifest from the preserved v35 manifest and three replacements. The full execution receipt and compiler stdout logs are included in the native review package.

The exact clarification checker verifies the common-H bound over the full square, equality of the affine normalized node lists, their short-arc range, and the two envelope balancing identities. The three inherited finite-cell, collision-core and spectral diagnostics are also rerun. Each program has byte-identical ordinary and optimized-Python output. These executions are regression and algebra checks, not an optimization over all controllers or a formal verification of the main theorem. The additional 200-check program authored in the v35 referee report is not claimed as replayed in this revision.

Rendered layout inspection covers main pp. 1, 37–40 and 42 and companion pp. 1, 80 and 159, using MuPDF sample renders and a Poppler render of the changed crossover page. No clipping, overlapping text or missing glyphs was identified in these samples. This is explicitly sampled inspection, not a claim to have visually read every page.

The source diff, preservation record, build receipt, execution record and visual-inspection record are stored with the revision. We submit the clarified manuscript for the next referee assessment, with no additional mathematical requirement or weakened conclusion introduced by this revision.
