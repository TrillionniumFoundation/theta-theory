# A2 revision 77 — review entry

**Statistical action recovery and smooth rigidity of dispersing billiards**  
Qian Qi — September 17, 2026

## Current manuscripts

- Principal article: `papers/A2-v17-boundary-information-coarsening/rigidity_v77.tex` (70-page native PDF in the accompanying product set).
- Complete technical manuscript: `papers/A2-v17-boundary-information-coarsening/main_v77.tex` (390 pages).
- Point-by-point response: `papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V77.md`; printable source `response_v77.tex` (4 pages).
- The original `two_collision.tex` companion remains unchanged (7 pages).

The six opening sections contain the new physical observation model and all deterministic proof inputs: three-clock absolute action recovery with unknown joint weights, nonlinear shared-prefix cancellation, finite distance certificates, Euclidean registration, actual finite coverage and finite-order stability. The globally identifying class and a persistent nonanalytic smooth family are proved in the text. The earlier periodic contact, analytic, multichannel and statistical arguments remain in the enlarged manuscript.

## Immutable baseline

Reviewed source branch: `revision/a2-v76-relative-envelope-2026-09-17`  
Reviewed source head: `ba8e40b92887e2cd8dcc92f3358401aac8c961d2`  
Review branch: `review/a2-v76-independent-harsh-top4-2026-09-17`  
Review commit: `fd4c9f57b9d0b142b60e163b266a708b61d80c94`  
Manuscript subtree: `950c448c8e8f19c6181fee26e425a9ac23b7dca9`.

All 1,035 inherited manuscript files remain byte- and mode-exact. The 1,433 inherited labels in the complete native entry and 191 in the principal native entry are all retained; the current counts are 1,481 and 239. The new entry points and notation copies do not overwrite their predecessors.

## Verification

Run `bash tools-v77/build_revision_v77.sh` from the manuscript directory. Native compilation uses shell escape disabled. The included verification records separately report source preservation, reference retention, symbolic identities, actual nonlinear billiard fixtures, and sampled PDF layout inspection. There are no undefined references, multiply defined labels or overfull boxes in the four products. Underfull-box warnings and the limited scope of visual inspection are recorded, not concealed.

These are integrity and diagnostic checks. They are not formal verification of the mathematical proofs, an independent referee review, or a journal decision. In particular the significance of the new observation-to-global-geometry theorem remains for the next referee to assess.

## Branch and publication provenance

The source patch targets a **new** branch named `revision/a2-v77-three-clock-smooth-atlas-2026-09-17` at the reviewed upstream head. Native products use a second **new** branch named `revision/a2-v77-native-products-2026-09-17`. Neither `main` nor any review or earlier revision branch is to be modified.

This delivery was prepared in a local repository reconstructed from the verified A2 subtree. Its packaging parent is **not** the complete upstream commit. The accompanying publisher applies the additive source patch to the actual pinned upstream head in an isolated worktree, checks preservation and creates the two true upstream-descended branches. Local packaging commit IDs must not be represented as already published GitHub commits.

At preparation time no remote write was performed: the connected GitHub actions were read-only and the container could not resolve GitHub. The external package includes the source patch, complete A2 source archive, native products and a publisher with non-force atomic push and read-back verification. This source entry does not itself certify a later push; the publisher's verified receipt records actual remote refs after success.
