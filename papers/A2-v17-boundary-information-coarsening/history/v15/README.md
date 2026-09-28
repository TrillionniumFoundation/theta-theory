# A2 v15 — intrinsic scalar transport

## Complete English manuscript

**Nonlinear boundary laws and two-contact rigidity in dispersing billiards**  
Qian Qi · 11 September 2026

This is the complete native author revision responding to the latest A2 v14 report. Start with `main.tex`, not the isolated build wrapper. All original mathematical sections, appendices, historical derivations and the two-collision companion are retained. The title, general smooth physical theorem, two-contact inverse, physical realization and full-profile observation scope are unchanged.

Branch: `revision/a2-v15-intrinsic-scalar-transport-2026-09-11`.

The principal changes are the attributed classical scalar construction with all fixed mixed derivatives; its exact identification with the physical Fredholm determinant and finite product remainder; a uniform flight/return/curvature notation; and the explicit two-way width/profile equivalence. The added scalar lemma is presented as classical background, not as an independent new linearization theorem. The complete mathematical response, including the significance question, is in [RESPONSE_TO_REFEREES.md](RESPONSE_TO_REFEREES.md).

## Reading map

The introduction states the physical relative theorem, geometric and observation scope, and local multiplier convention. Section 8 contains the analytic comparison, the new scalar lemma, the retained physical Schur-concatenation theorem, the exact determinant/product corollary and the width interpretation. `article/23_two_contact_rigidity.tex` retains the complete geometric inverse under reversible notation changes only. The subsequent physical-image, two-flight, Abel-stability and observation sections and the full auxiliary appendix remain active.

[Proof dependencies](PROOF_LEDGER.md), [historical reading scope](HISTORICAL_DERIVATION_AUDIT.md), [literature verification](LITERATURE_VERIFICATION.md), [frozen source pins](SOURCE_PINS.json) and [executed verification](VERIFICATION.json) are separate from the research article. Overridden v14 files are archived in `history/v14-reviewed/`; all older history remains present.

## Build from a complete repository checkout

Run from this directory with a TeX Live installation containing the packages in `preamble.tex`, and `latexmk`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error two_collision.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The first command supplies the companion cross-references used by `xr-hyper`. The manuscript's full input graph is native to this directory; it does not require a generated textual patch or a previous manuscript directory to typeset.

## Reproduce the diagnostics

The new exact suite uses only Python's standard library. From a complete repository checkout, the sibling v14 directory supplies the independently pinned retention baseline:

```sh
python3 tools/verify_v15.py --scope full --output verification/full.normal.json
python3 -O tools/verify_v15.py --scope full --output verification/full.optimized.json
cmp verification/full.normal.json verification/full.optimized.json
```

`--scope edited` checks the locally reproduced six-file baseline and the revised mathematical source blocks; that is the mode actually executed for this revision. Its 10,549 checks pass with identical normal/optimized output. Full mode is supplied for a complete checkout and is not falsely recorded as having run in this session.

The latest referee's original script is copied unchanged, with its exact Git blob pin in `SOURCE_PINS.json`. It requires NumPy and SciPy:

```sh
python3 verification/referee_v14/verify_review.py --output verification/referee_v14/normal.json
python3 -O verification/referee_v14/verify_review.py --output verification/referee_v14/optimized.json
cmp verification/referee_v14/normal.json verification/referee_v14/optimized.json
```

Both executions were performed and pass 3,216 checks. The local Euclidean calculations use truncated stationary bridges, not a global periodic-table simulation or interval-certified estimates. The two recorded output paths contain identical bytes. Historical author scripts remain preserved for their original versions; their version-specific source-retention gates should not be relabelled as v15 gates.

## Build status and review status

The revised sections were compiled in an isolated 18-page integration smoke test, with two passes, no undefined control sequence and no overfull box. Selected new proof pages were rendered and inspected. The wrapper is `verification/changed_sections_smoke.tex`; references to inherited sections are intentionally unresolved there. It is not the complete manuscript PDF. No full-article/companion compilation or successful remote CI is claimed for this session. `VERIFICATION.json` records this distinction.

This branch is an author revision for further independent assessment, not a merge to `main`, journal acceptance, or formal proof-assistant certification. The existing review reports remain unchanged.
