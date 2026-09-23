# A2 revision 133 — universal readout and exceptional fibres

**Branch:** `revision/a2-v133-schur-readout-exceptional-fibres-2026-09-23`  
**Controlling review commit:** `d76f34db1aaa8e196a7b50f4ec04be381d45236e`  
**Reviewed manuscript:** v132, `6d8fcb430efa95624a15aa684cfccab79c793350`.

## Referee entry points

The complete new article is in `papers/A2-v17-boundary-information-coarsening/article/v133/`:

- `geometry.pdf` and `geometry.tex`: complete reconstruction-first manuscript, not an addendum.
- `RESPONSE_TO_REFEREE_V132.md`: point-by-point response to the controlling report.
- `ISSUE_MATRIX.json`: distinguishes addressed proof requests from documentary-open priority.
- `LITERATURE_AUDIT_V133.md`: actual primary-source access and inverse-data comparison.
- `PROVENANCE_MANIFEST.json` and `evidence/BUILD_RECEIPT.json`: source and execution hashes, inherited-input/label preservation, actual tests, and explicit non-machine-certified proof scope.

The principal new results are `lem:universal-schur-readout`,
`lem:readout-exterior-twist`, `lem:common-g-functoriality`,
`thm:exceptional-component-fibres`, and `cor:exceptional-candidate-bound`.
The generic full-scheme reconstruction theorem is retained without weakening.
The new fibre theorem distinguishes double points, distinct secant candidates,
discarded pure endpoints, and flag-line fibres; it does not infer exceptional
scheme isomorphism from equality of the component invariant.

All inherited compiled mathematical inputs and labels are preserved. The
complete higher W3/W4 embedded-primary atlas is not falsely declared computed.
The independent report is an owner-requested AI-assisted report, not a
journal-issued decision. **Ballico 1993 full-text priority comparison remains
documentary-open**; the issue matrix does not claim all scholarly obligations
closed.

## Reproduction and branch isolation

The revision recipe expands the complete source at the immutable controlling
review commit, verifies its existing hashes, and applies a SHA-256-checked
transfer payload. The expanded human-readable source is committed by the
branch-restricted workflow after all eight exact scripts and the three-pass
LaTeX build succeed. The payload is only a byte-preserving transfer container;
the referee-facing mathematical source is the expanded article directory.

Run `python revisions/a2-v133/assemble.py` from this branch, then
`bash papers/A2-v17-boundary-information-coarsening/article/v133/build.sh`.
The recipe never edits v132 or any review. Its receipt distinguishes finite
coordinate checks from the written structural proofs. The workflow only
publishes to the named new revision branch; no merge or force-push is used.
