# A2-DYN revision 108

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

This is the active revision-108 packet responding to the external report on revisions 105--107 at `reviews/a2-dyn-v107-positive-source-external-top4-review-2026-10-14/REFEREE_REPORT.md`, review commit `6811140ec51276247d75057980692d4a4d5e77b6`, report blob `82cff2e2fc14e6a1eaa12b75fb41012dd155bdae`.

## Manuscript and mathematical increment

The article entry is `main.tex`; the historical technical supplement is `supplement.tex`. The article uses the exact previous article at `provenance/v107-main.tex` as its inherited shell. LaTeX hooks update the visible revision date, add the new abstract paragraph, and insert the new proofs before the inherited appendices. Every prior article paragraph is still typeset. The original title, author, section, exact labels, normalization, arithmetic reference and raw pointwise target remain unchanged.

All 257 inherited numbered core modules are byte/mode preserved. Modules 258--259 prove a canonical roofwise comparison-pool construction, one-copy overlap, its finite-count envelope estimate, attained maximality within a specified certificate class, and pointwise domination of every compatible revision-107 allocation at the same total cost. The resulting original-source residual is `(U_B_micro - K_B P_rB)_+`.

The construction removes the need to select angular source blocks. It does **not** prove collision-uniform decay of the canonical shortage, a Lorentz logarithmic insertion, or every singular trace extension. The full raw LLT remains the organizing target, not an asserted completed theorem. See `PROOF_LEDGER.md` and `RESPONSE_TO_REFEREE.md`.

## Reproduction

From the repository root:

```sh
bash papers/A2-DYN-v108-referee-response/build.sh
```

The exact-checkout build verifies the frozen author and review sources, all inherited blob/mode pairs, source scope, active claim flags and the v106 metadata supersession. It runs 4000 rational diagnostics under normal Python and `python -O`, assembles the complete inherited supplement, compiles the article and supplement until references stabilize, retains the narrow inherited TeX advisory audit, checks recorder coverage of all 259 modules, and renders every article page. No bypass mode is provided. Native TeX, NumPy, mpmath, SymPy, SciPy and Poppler are installed by the dedicated workflow.

The workflow is `.github/workflows/a2-dyn-v108-canonical-capacity-qualification.yml`. Exact-SHA PDFs, complete TeX logs, recorder files, rendered pages and source evidence are uploaded as workflow artifacts. A successful workflow is source/build qualification, not mathematical proof certification. `evidence/v108-source-and-checks.json` records both the checked-out head and its theorem-bearing commit, so later qualification-only changes cannot be mistaken for new mathematics.

## Provenance and document authority

`SOURCE_MANIFEST.json`, `PUBLICATION_STATUS.json`, this README, `PROOF_LEDGER.md` and `RESPONSE_TO_REFEREE.md` describe the active v108 packet. Other inherited status notes and validation records are historical records, not current v108 qualification claims. Their source bytes are retained deliberately.

The frozen v106 local README and manifest incorrectly describe revision 105. The versioned correction `provenance/v106-metadata-supersession.json` explicitly replaces those identity claims without changing the historical v106 tree. Its workflow identity is not guessed from the stale manifest.

`provenance/v107-final-qualification.json` records the now-completed paired author runs at exact head `7f660346afea9500138920ca87fef46026a7e507`. The review's earlier queued status is retained as a valid freeze-time observation, not silently rewritten.

The paired v108 author branches are `revision/a2-dyn-v108-microscopic-referee-response-2026-10-14` and `revision/a2-dyn-v108-microscopic-referee-copy-2026-10-14`. No previous author branch, review report, historical paper directory or unrelated paper is overwritten.
