# Theta-Theory: executed next steps, September 8, 2026

This is an execution package, not another wholesale replacement of A1.

## Delivered work

| Track | Output | Status and boundary |
|---|---|---|
| Statistical A1 v36 | Frozen release reference, submission manifest, cover-letter draft and companion role map | Original manuscript unchanged; no actual journal submission or new acceptance claim |
| DYN-A1 | Full-source proof audit, unchanged-source rebuild, independent diagnostics | Three principal proof chains examined; no fatal gap established in that scope; contribution/priority review remains distinct |
| A2 | `research/A2_Two_Collision_Response.tex` | Full-equilibrium two-collision count law and smooth radius response at T=0.11 for R in [0.45,0.47]; not a full-path or long-time theorem |
| B2 | `research/B2_Chronological_Contact_Reduction.tex` | Chronological Schur reduction, metric-correct coarea, forest estimate and exact two-contact example; not an all-genealogy or Boltzmann--Grad result |

The author and current review commits of statistical A1 are pinned in `submission/A1_V36_SUBMISSION_MANIFEST.json`. The release branch is `release/a1-v36-submission-2026-09-08`, pointing to `8f074b8027627a71a81a362b9d15f47975e1f3ae`; the associated review is `1e7af61f0812638d00ee0efad8fc9a68e2776c3c`. The latest primary-source hard-sphere baseline includes Deng--Hani--Ma's long-time derivation, not only Lanford's short-time regime. See `research/LITERATURE_SCOPE.md`.

## Reproduce the current new work

From this directory, with Python 3.10+, NumPy, SymPy, PyMuPDF and a TeX installation:

```sh
python tools/verify_new_results.py --output evidence/NEW_DIAGNOSTICS.json
python -O tools/verify_new_results.py --output evidence/NEW_DIAGNOSTICS_OPTIMIZED.json
python tools/build_documents.py
```

In the complete local archive, add `--include-audit` to rebuild the formatted audit PDF as well; its complete text is also supplied as Markdown.

The 17 independent test cases mix exact algebra with explicitly floating quadrature. Normal and optimized outputs are identical. The separate DYN replay contains 35 inherited author tests, not 35 newly authored checks. New-document builds use no shell escape. The DYN native source has also been rebuilt unchanged in split and single forms; v36's 201-page unit was not rebuilt in this execution.

The local delivery archive includes the three new PDFs, source, original dynamical source snapshot and extraction, current logs, evidence and manifests. GitHub publication uses the new text sources, audit, scripts and compact receipts; the PDF binaries are supplied in the conversation package. The work branch is for review, not an automatic merge into main. No manuscript, historical referee report, or permission was deleted or overwritten on an existing branch.

## Next proof targets, not claimed completed

A2-Next: the joint physical two-impact record with sampled velocities and sources, then an assembled multi-itinerary response estimate usable in long-time statistics. The current count identity alone does not provide it.

B2-Next: derive the surplus Schur matrices for the selected actual genealogies, establish their rank or stratified degeneracy bounds with all labels retained, and sum source-dependent contributions. Then perform dynamic exact conditioning in the B2-GC -> B1 -> B2-MC order.

DYN-Next: specialist theorem-level novelty comparison against multibaker and parameter-response theory. Keep the present dynamical model separate from both statistical exponent collisions and specular billiards.

A1-Submission: the author selects a journal and approves actual submission declarations. Existing AI-assisted referee recommendations do not supply those declarations.
