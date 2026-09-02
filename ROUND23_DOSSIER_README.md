# Canonical Round-Twenty-Three review dossier

The next referee round has one independently compilable entrypoint:

- source: `ROUND23_REVISION_DOSSIER.tex`
- generated PDF: `ROUND23_REVISION_DOSSIER.pdf`
- content manifest: `ROUND23_DOSSIER_MANIFEST.json`
- explicit counterexample appendix: `ROUND23_REFEREE_REGRESSION_APPENDIX.tex`

The dossier inputs all eleven `ROUND23_POSITIVE_CLOSURE.tex` sources, the shared specialist bibliography, and the permanent regression appendix.  Its workflow is `.github/workflows/build-round23-revision-dossier.yml`.

The per-paper wrappers and PDFs remain part of the submission.  The dossier is the canonical reading bundle when a reviewer wants to follow the dependency graph without switching directories.
