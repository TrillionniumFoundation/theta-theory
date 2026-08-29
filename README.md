# θ-Theory active manuscript tree

This branch is the clean active development tree for the five-paper θ-Theory series.
Historical manuscripts, cumulative canonical volumes, CM2 evidence, legacy tools,
and superseded source variants are preserved on the archive branch:

```text
archive/full-v4-pre-governance-2026-08-29
archive marker commit: 0662b24c2ad652f64fa3153b62190f925e802b32
source snapshot commit: bf88e63b9cb75709a42075d0d5e0fc54299c0661
```

## Current controlling sources

The current baseline remains the v4 five-paper set under `papers/referee-ready/`.
In every paper folder:

```text
main.tex        controlling manuscript
references.bib  controlling bibliography
```

Versioned manuscript copies are not stored in the active tree. Git commits and the
archive branch preserve their history.

## Active layout

| Path | Purpose |
| --- | --- |
| `papers/referee-ready/` | Five current manuscripts, normative appendices, series manifests and review material. |
| `status/ACTIVE_TREE_STATUS.yaml` | Machine-readable governance state. |
| `platforms/` | Current platform decisions and future theorem-platform registry. |
| `tools/verify_active_tree.py` | Repository hygiene verifier. |
| `ARCHIVE_POINTER.md` | Exact archive and source-commit pointer. |
| `GOVERNANCE.md` | Rules separating active theorem sources from research provenance. |

## Verification

```bash
python3 tools/verify_active_tree.py
make -C papers/referee-ready all
```

The first command checks repository governance only. LaTeX compilation and finite-
dimensional checks do not certify the analytical proofs. The current series remains a
research manuscript set awaiting independent line-by-line review.
