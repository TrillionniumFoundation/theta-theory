# A2-DYN: signed physical roof derivatives and the full marked jump spectrum

**Author revision, 23 October 2026.** The paper remains *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*. This packet continues the latest complete native author manuscript through 335 and adds the complete proofs of 336–337. It is an author revision, not a new referee review.

The mathematical source of the immediate predecessor is commit `85f206907f56773e32fae9b61302924ca16603aa`; its later evidence carrier and this branch's parent is `d6c3c6754fb3a1b4ad3eea8e6dcc51642e312b28`. Their active mathematics is identical. The source/carrier distinction, actual article trees and controlling report are recorded in `SOURCE_PROVENANCE.md`.

The original triangular lattice, radius range `R in [9/20,47/100]`, all genuine first-hit collisions, unit-speed physical roof, five original section rectangles, exact occupation/displacement labels and normalization `c_*=91/(10000pi)` are retained. Occupation counts collisions `0,...,m-1`, and terminal section membership is tested separately. The four coordinates remain `(k_1,k_2,t,n)` at the actual fixed collision count `m`.

## Mathematical additions in this iteration

**Native 336 identifies the complete signed roof derivative for the current smooth observation class.** The real finite first-hit graph and fiberwise geometric decomposition give a common finite set of possible roof atoms at each fixed collision count, uniformly over the original radius interval. Smooth observation weights need not be definable. All actual section sides, unvisited boundaries and critical entrances are included. Nonconstant boundary roof maps contribute integrable densities; constant-roof sides and positive-visited critical fans contribute atoms. The result is

\[
Df_\ell=d_\ell(t)\,dt+\sum_u a_\ell(u)\delta_u,
\qquad
\sum_\ell\left(\|d_\ell\|_1+\sum_u|a_\ell(u)|\right)\le D.
\]

There is no singular-continuous derivative for the specified full smooth class. The coefficients combine all contributions at the same physical roof and same exact label with their signs. They include constant-roof boundary terms, so critical germs are not silently treated as the entire atomic part. The theorem retains the complete inherited all-label budget without multiplying by the number of labels. Historical native 40, 92 and 93 already contain finite-count germ structure for their own subanalytic observation classes; those results are preserved and are not presented as new discoveries here.

**Native 337 computes the full marked physical jump spectrum.** For the actual joint transform and each fixed `m,R`, the derivative identity and its symmetric roof-frequency energy are

\[
-is\mathcal F=\mathcal A+\mathcal G,
\qquad
\lim_{S\to\infty}\frac{1}{2S(2\pi)^3}
\int_{-S}^{S}\int_{[-\pi,\pi]^3}
 s^2|\mathcal F(\vartheta,s)|^2\,d\vartheta\,ds
=\sum_{\ell,u}|a_\ell(u)|^2.
\]

The finite-band error retains the exact interactions between nearby roof values. This limit is taken at fixed physical parameters; it is not moved through the radius supremum or collision limit. The original raw pointwise theorem necessarily forces the central all-label jump energy to vanish at scale `m^2`, as well as its maximum central jump. These are necessary conditions, not a sufficient replacement for the original objective.

The new energy formula also preserves the already-proved native 322 zero-clearance positive-visited critical-fan payment. Its once-only physical subcomponent has total absolute coefficient at most

\[
B_m=A_VC_{\rm pc}m(47/59)^{(m-1)/2},
\]

and its removal changes the complete signed energy by at most `2D B_m+B_m^2`, even when other sources share the same roof. This is an application of the inherited payment, not a new claim that all critical or positive-width sources have been eliminated.

The original section multiplier reconstruction in 333, exact physical-interval inversion and fixed-window bridge in 334, and complete selected endpoint kernel in 335 remain inherited results. Their complete proofs and qualifications are unchanged.

## Current theorem status and the unchanged objective

**The full original raw pointwise local limit theorem and the full four-coordinate local inverse are not completed by this revision.** The new signed structure is proved at its stated scope; it does not make the remaining normalized source automatically small.

The original same-roof closing condition remains native 329, `eq:lc-final-shortage`, with its complete remaining low-load endpoint/shallow source, the same full comparison pool and the original order

\[
\lim_{B\to\infty}\limsup_{m\to\infty}\sup_{R,n,k}
m^2\operatorname*{ess\,sup}_{t\in\mathcal C_{m,R,n,k}(M)}.
\]

Native 329 already pays its proved deep-clearance class; this work is retained. Native 335's positive-width leading-coefficient bound is unscaled and cannot be multiplied by `m^2` at fixed outer width to declare closure.

On native 334's alternative route, the inherited fixed-positive-window theorem already evaluates its scalar comparison and the full finite-peak reference modulus. The remaining sufficient condition is the complete normalized local derivative charge. Native 336 now expresses that charge exactly as local `L1` derivative mass plus local absolute atomic mass, with no Cantor remainder. The vanishing of neither complete term is proved here, and the squared-jump necessary condition does not replace this sufficient criterion. The analysis window is not substituted for the original microscopic conditioning event.

The arithmetic reference, continued near-unit peaks, conditional event denominator and genuine long-time inverse Jacobian retain their original hypotheses and scope. Compilation, finite scripts and an author proof body are distinct from independent expert reconstruction. No journal acceptance or expert certification is claimed.

## Complete native source and preservation

The active manuscript has **90 native inputs and 78 core files, 260–337**. The predecessor has 87 native inputs: **85 remain byte-identical**, including all 76 predecessor core proofs and `current-dependency-notes.tex`. Only `main.tex` and `revision-introduction.tex` change among those 87. The current qualification is added separately in `revision-dependency-notes.tex`; it does not overwrite the inherited notes.

`audit/IMMEDIATE_PREDECESSOR_FILE_IDENTITIES.json` is the verification manifest for all 158 predecessor files outside its evidence directory. Changed originals are retained in `history/section-multipliers-baseline/`. The 660 distinct historical native objects are preserved in the content-addressed archive and were rehashed in the fresh census. Original branches, reports, companion papers and unrelated paths remain in the parent tree.

| File or directory | Purpose |
| --- | --- |
| `main.tex`, `core/260_*.tex`–`core/337_*.tex` | Complete native main manuscript and technical proofs |
| `revision-dependency-notes.tex` | Current scope, separate from unchanged inherited notes |
| `RESPONSE_TO_REFEREE.md` | Located author responses to the controlling report and applicable historical concerns |
| `PROOF_DEPENDENCY_LEDGER.md`, `HISTORICAL_DEPENDENCY_STATUS.md` | Proven, inherited, conditional and unclosed dependencies |
| `SOURCE_PROVENANCE.md`, `SOURCE_MANIFEST.json` | Source/carrier commits, trees, scoped census and file identities |
| `HISTORY_PRESERVATION_AUDIT.md`, `history/` | Original materials, historical source bodies and preservation checks |
| `LITERATURE_HYPOTHESIS_AUDIT.md` | Fresh primary-source versions, actual hypotheses and retrieval limitations |
| `NEW_MATHEMATICAL_CHECKS.md`, `audit/` | Physical geometry, signs, normalization, singularity and limit-order checks |
| `VALIDATION_REPORT.md`, `PUBLICATION_STATUS.json`, `evidence/` | Actual completed execution receipts and current publication/CI status |

## Reproduction and evidence status

Install the pinned Python dependencies in `requirements.txt`, a working `pdflatex` installation with the AMS and Latin Modern packages, and Poppler. From this article directory run:

```bash
python3 -m pip install -r requirements.txt
bash build.sh
```

The validator checks the complete native input graph, inherited active and predecessor file identities, all historical archive members and the controlling report. It executes six mathematical programs: section constants, exact interval inversion, endpoint-kernel algebra, historical analytic arithmetic, physical SBV formulas and the roof jump spectrum. It runs three LaTeX passes and compares the actual recorder inputs with the native closure, while checking unresolved references, missing characters and overfull boxes. The generated output is under `build/current/`. Run Python without `-O`, since the programs retain their assertions.

The immediate predecessor was actually rebuilt locally: its four mathematical programs passed, all 87 native inputs were recorded, and its 271-page PDF compiled successfully. Its fresh source and carrier GitHub observations, runs `39907443910` and `39908709982`, were `queued` with `conclusion=null`; those observations are not completed CI. The current revision's completed runs and any later remote state must be read from `VALIDATION_REPORT.md` and `PUBLICATION_STATUS.json`. No planned run or inherited success is counted as verification of the current source.

This packet is isolated to `papers/A2-DYN-physical-roof-jump-spectrum-author-revision` on `revision/a2-dyn-physical-roof-jump-spectrum-2026-10-23`, with the new scoped workflow `.github/workflows/a2-dyn-physical-roof-jump-spectrum-20261023.yml`. Existing workflows and earlier scientific directories are preserved.
