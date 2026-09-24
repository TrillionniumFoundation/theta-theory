# A2 revision 136

**Primary article:** `geometry.pdf` / `geometry.tex`.  
**Technical supplement:** `supplement.pdf` / `supplement.tex`.  
**Complete archival manuscript:** `complete.pdf` / `complete.tex`.

The primary article contains the full smooth-Jacobian intrinsic reconstruction proof and a new dimension-uniform contraction/support and component-pair inverse theorem. The separate supplement retains the primary-boundary and relative-specialization mathematics. No extra genericity condition has been imposed on the original smooth-locus theorem.

Read `RESPONSE_TO_REFEREES_V135.md` for the response to both v135 reports, `LITERATURE_AUDIT_V136.md` for the direct exterior comparison and the still-open full Ballico 1993 comparison, and `ISSUE_MATRIX.json` for issue status. Neither all-issue closure nor historical priority nor journal acceptance is asserted.

`PROVENANCE_MANIFEST.json` binds this source to the immutable reviewed v135 manuscript and reports. `evidence/BUILD_RECEIPT.json` records actual execution, not intended checks. The workflow builds and publishes only on `revision/a2-v136-functorial-support-reconstruction-2026-09-23`.

Reproduce from repository root:

```sh
python revisions/a2-v136/assemble.py
bash papers/A2-v17-boundary-information-coarsening/article/v136/build.sh
```

The assembler reads immutable predecessor source, overlays the revised editable text, and refuses to remove any compiled predecessor mathematical label. All eleven exact scripts run before the three LaTeX builds. The receipts explicitly distinguish finite exact checks from written general proofs. AI assistance in the new derivation, drafting, and checks is disclosed in the principal manuscript.
