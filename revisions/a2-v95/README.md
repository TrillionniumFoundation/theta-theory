# A2 revision 95: real valuations and identifiable singularities

Controlling report: `reviews/a2-v94-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md` at `dbbad2d84c6a3b358bddabf84dc16f0b09b38634`.

New branch: `revision/a2-v95-real-valuations-cubic-classification-2026-09-19`.

## Manuscript

The complete entrypoint is `papers/A2-v17-boundary-information-coarsening/rigidity_v95.tex`. It includes every previously active mathematical/bibliography module. The separate `core_v95.tex` is a marked main-argument reading copy, not the full retained-appendix manuscript.

From the paper directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error rigidity_v95.tex
```

The central new results are the finite real-valuative Newton formula, the necessary-and-sufficient fibre classification of the boundary double/triple cubic family, and its explicit joint leading fibre and Fisher constant. The response maps every substantive and smaller referee request to its treatment.

## Evidence

From the repository root:

```sh
python revisions/a2-v95/diagnostics_v95.py --output build/a2-v95/diagnostics.json
python revisions/a2-v95/verify_a2_v95.py --receipt build/a2-v95/source-audit.json
# After the full manuscript has actually compiled:
python revisions/a2-v95/verify_a2_v95.py --compiled --receipt build/a2-v95/exact-head.json
```

Python dependencies: numpy, scipy, sympy. Typesetting dependencies follow the existing native workflow and add no custom fonts. The exact-head workflow has no restrictive path filter and runs only on this revision branch (or explicit dispatch). It has read-only repository permissions.

Local evidence covers the new 12-page core and finite regression checks. It does not cover a full inherited-appendix build or a Git audit of an exact checkout. The workflow's actual conclusion and receipt, not the presence of a workflow file, determine those statuses. Source and numerical audits are not mathematical proof verification.
