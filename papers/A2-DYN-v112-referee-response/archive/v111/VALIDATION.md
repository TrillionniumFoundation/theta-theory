# Validation record — A2-DYN revision 111

## Actual local execution

The active manuscript compiled successfully to 25 pages with stable references. The final log reports zero unresolved references, zero duplicate labels and zero overfull boxes. All 25 pages were rendered; the full page set was inspected in contact sheets, with the main new proof pages checked separately. The source manifest verifies all 12 active TeX files, including the unchanged original model.

The new diagnostics passed:

- 10,922 exact marked-word reconstruction and block-length cases;
- 1,641 exact changing-witness insertion cases;
- 702 exact geometric depth-tail cases;
- 144 pairs of actual two-disk trajectories for 2, 4, 6 and 8 flights, three original radii and six gradient-ray angles.

The physical trajectory tests solve the stationary action equations by double-precision Newton iteration, verify specular reflections, check the original endpoint section squares, and exclude every possible nearby third disk. They test the signs of both Cartesian support inequalities and their sum. They are floating-point diagnostics, not interval proof certificates. The marked-word and witness calculations use exact rational arithmetic.

The previous v110 finite suite was also rerun: 56 optical configurations, 1,016 marked inequalities, 4,096 source identities and 108 segment-localization cases passed. Both suites and the source-manifest checks produced byte-identical normal/optimized Python outputs. Explicit failure checks remain enabled under `python -O`.

The complete production `build.sh` was executed locally, not merely inspected. Its exact outputs are retained in `evidence/local-research.json`, `evidence/inherited-finite-recheck.json`, `evidence/local-manifest.json` and `evidence/local-typesetting.json`.

## Observed v110 remote qualification after the report freeze

Run `38528720288` completed with conclusion `success` at reviewed author SHA `0abce3fcfbc735ff5cc6d085279abea5f32a7a22`, updated at `2026-10-14T07:55:16Z`. Artifact `11877977413`, digest `sha256:cd5a724b90b880fdd48070bf5cd6f241a9b5848ef114d12ad406701ba8ce1e46`, supplied the exact active source used for the local baseline. Its nine active manuscript blob hashes were checked before editing.

This later observation is stored separately in `provenance/v110-ci-observed-2026-10-14.json`. It does not alter the report's queued-at-freeze statement and is not evidence of a v111 run.

## New qualification and its limits

The new workflow checks its own exact checkout SHA, the unchanged original v110 tree, the exact archived v110 tree, the controlling report blob, and the three historical proof anchors. It permits only additions under the v111 directory and its dedicated workflow, builds the active article and uploads exact-SHA source and build evidence. It uses read-only repository permissions.

No successful v111 workflow is asserted in this source record before one is observed. The unchanged historical tree is preserved by Git identity; no new compilation of every historical supplement is claimed. Source checks, finite diagnostics and PDF rendering do not certify the remaining localized-shortage limit or independently reconstruct every inherited continuum input.
