# Preservation and mathematical changes — v11

No existing repository file is edited by the v11 source release. All 238 predecessor inputs in `INHERITED_INPUTS.json` are required byte-for-byte unchanged. The release writes only a new paper directory and a dedicated branch-scoped workflow. Old review, v10, A1, A2 and default branches are left untouched.

## Canonical mathematical core

Every mathematical body in v10 `core.tex` is retained in the v11 canonical view. References still import the same old files. The only local copy is `common-membership.tex`: its median-index sentence is corrected by choosing d whose p_d is a median before applying the task-d affine argument. It does not alter the result 1, 1/2, 2/9 or its mathematical argument. The original v10 file remains intact.

The v11 title and author are retained; the abstract and introduction are rewritten to state the resource-comparison thesis. New sections are added on concrete state costs and complete-state fusion, conditional singular compactness, task completion, computational distinctions, and the microscopic hard-sphere domain/acquisition theorem. References are augmented, not pruned.

## Complete development

The entire predecessor companion body is retained. Its v10 introduction is additionally imported as a historical introduction, followed by the already preserved v9–v5 introductions and mathematical bodies. No previous theorem is silently reclassified as a premise of a new theorem. The build compares every label in the actual v10 complete-development auxiliary file with the v11 complete view and checks all inherited labels actually compiled.

The v10 auxiliary label map is pinned in `PREDECESSOR_LABELS.json`; the original auxiliary-file SHA-256 and source identity are recorded there. This is an explicit preservation test, not a theorem-certification test.

## Evidence

`SOURCE_MANIFEST.json` pins each new plaintext input. The build checks inherited and new hashes both before and after compilation, creates both manuscript views, checks stable numbering and absence of broken references/overflows, and creates a complete source archive. The actual page counts and hashes are in `evidence/BUILD_RECEIPT.json`. No finite diagnostics or source hashes are described as proofs of the analytic theorems.
