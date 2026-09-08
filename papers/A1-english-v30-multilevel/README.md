# A1: multilevel statistical realization revision

**Native article:** `main.tex`. **Complete accompanying volume:** `companions.tex`.
The article and companion retain the inherited native source tree; this is not an extract-only submission.

Revision branch: `revision/a1-english-v30-multilevel-minimax-2026-09-08`.
Revision directory: `papers/A1-english-v30-multilevel/`.
Review baseline: `90c7acd0e4efe3280eb1a8faa3c6d9461870c36f`, branch `review/a1-english-v29-harsh-independent-2026-09-08`.
Reviewed submission: `610233410ff6600e76167fad98a3f610faa6191b`.
The report remains at `reviews/a1-english-v29-harsh-independent-2026-09-08/REFEREE_REPORT.md`.

## Mathematical revision

The unified introduction follows the mathematical dependency chain: attainable collision geometry; a common causal filter; adaptive and reusable graph acquisition; local-path versus predictable information; statistical network realization. It replaces the six cumulative introductions in the active entry point. Every historical introduction remains in the native source copy. No inherited proof module is removed from the active article or companion.

`v30/menu_finiteness.tex` corrects E29.1 by proving fixed-calibration eventual optimality of one order and finiteness of the optimized menu excess on the whole accuracy interval. It also characterizes when a prescribed menu has infinite excess, gives a finite critical-resolution formula, and proves uniform boundedness when retained volumes stay uniformly positive. The collision-path theorems are preserved with their actual calibration-dependent quantifier.

`v30/multilevel.tex` gives an exact all-budget minimax theorem for arbitrary finite regenerative committed-route experiments and an actual positive-detector realization. The full acquired mixed law, including both atoms, yields atom-aware capacities with event mass one. Their pre-acquisition gap is bounded independently of the number of checkpoints. A realized J-checkpoint family has an exact consistency penalty J + 1 - 1/J over invalid separate-checkpoint optimization.

`v30/predictable_networks.tex` removes initial commitment under conditional regeneration at every vertex. It allows branching, recombination and full-history adaptive scheduling in the converse. The exact statistical optimum is a common-flow minimax with a shortest-path dual; a distribution on at most J+1 deterministic paths and one M-label causal reset controller attain it. The predictable refinement is stronger than the initial-anchor and unanchored relaxations. For the positive block family, the true-risk/certificate ratio is at most 8306688/64800 < 129 at every budget and converges uniformly over finite networks and gains to a constant in (4.05, 4.06).

The original tensor-only graph loss, the augmented local-and-tensor loss, and the new regenerative attenuated readout are not identified. Public finite vertex descriptors, optional descriptor storage costs, independent seeds, and the timing of each acquisition are explicit. The new theorems do not assume that a correlated nonregenerative posterior regenerates.

## Reading and reproducibility

`RESPONSE_TO_REFEREE.md` maps the report's concerns to statements and proofs. `PROOF_LEDGER.md` records hypotheses and directions of the bounds. `PRESERVATION_V30.json` records the source-tree construction. Current execution evidence is in `SESSION_VALIDATION_V30.json`; older version-numbered receipts are historical evidence, not new verification.

From this directory in a full checkout:

```sh
python build.py --prepare-only
python build.py
```

The builder checks inherited source and active proof-body preservation, native cross-volume labels and citations, normal/optimized diagnostics, and five alternating TeX passes per volume. It fails on unresolved or duplicate references and overfull boxes. Its actual result is written to `build-v30/BUILD_RECORD_V30.json`, including failures. Preparing the source does not count as a full build.

The separately compilable `new-results.tex` is only a proof packet for the new modules. It uses explicitly identified source-label locators for background references. Its locally executed three-pass build produced ten pages with no unresolved references, duplicate labels or overfull boxes; all ten rendered pages were inspected. This does **not** establish successful native two-volume compilation. The new exact-rational diagnostics passed in normal and optimized Python modes with identical output. Neither finite tests nor TeX execution certify the continuum theorems or a journal decision.

The complete original `papers/A1-english-v29/`, the review branch and `main` are unchanged by this revision. In the new native copy only `main.tex`, the two pinpointed legacy exposition passages and current handoff/build metadata are replaced; the previous versions are also retained in `history/v29/`.
