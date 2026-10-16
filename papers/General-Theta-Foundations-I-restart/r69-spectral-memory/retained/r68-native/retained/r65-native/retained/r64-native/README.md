# General Theta Foundations I — R64 author revision

**Start with `main.tex`, `supplement.tex`, and `RESPONSE_TO_REFEREE.md`.** These are the complete current English manuscript, current technical supplement, and author response. This is not a referee report or an editorial decision. The title remains **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer** and the research objective remains Annals / Acta / Inventiones / JAMS.

## Mathematical center

The revision adds boundary attainment of constrained bounded task risk, compactness and a complete finite-score criterion for performed stopped laws at fixed dictionary and budget, an exact resource-price dual, and sparse pure-preparation certificates for the compact-model finite problems. A common backward recursion evaluates the witnesses; a counted fallback restores the original budget and supplies finite-label approximations. Several additive expected resources can be imposed simultaneously using one jointly safe fallback. Separate cost and risk witnesses, and the nonconvexity caused by freely optimizing hard dictionary width, have exact counterexamples. A delayed-release task has an exact expected-call curve, exact one-live-label curve, and a sharp K-live-label attainment threshold for delay K, with an explicit positive gap below it. These are scoped mathematical statements, not a declaration that the whole Foundations programme is complete.

All previous valid main proofs remain in the current manuscript. The complete original R63 paper tree is retained byte-for-byte in `retained/r63-native/`, including the prior R62/R61/R58 and independent-source maps. The current technical supplement is separate from the complete 37-page historical R58 companion. No original author, review, or other-paper folder is overwritten.

## Controlling objects

- Author baseline: remote R63 commit `2bb08a6323fb0198e8ba93a4870b74304431fedc`, paper tree `37326a02aecf6f211efeef9cf1d3bfae66a4fb2c`.
- Controlling newly deposited report: R59 round 3, commit `c39922c242f9bd03d2e0d7f05d6e9b483362e26d`, report blob `eb9e20db36ae1297f4ee13369be8460e786d7546`.
- That report reviews R59 source `29de5433c2c4f45d5174a87a8588fd3a24d3f84a`, not R63 or R64. Its accepted proof closures are inherited. Its unresolved breadth and significance concerns are not treated as acceptance of later results.

The three R59 reports remain separately pinned in `inputs/review/`; their original commits are not merged into the author lineage. Source and report selection are recorded in `provenance/BASELINE_R64.json`.

## Rebuild and inspect

Install the pinned Python dependencies in `requirements.txt` and a native TeX distribution including amsart, lmodern, mathtools, microtype, geometry and hyperref, together with Poppler utilities. Run:

```sh
python3 verify.py --out /tmp/theta-r64-independent --source-commit <exact-checkout-SHA>
```

The verifier checks the complete retained source tree and all current source hashes, separately verifies all three R59 report blobs, runs four diagnostic generations normally and with `python -O`, and builds the current main, current supplement and retained companion in three native LaTeX passes. It rejects unresolved references, citations, overfull boxes, source mutation and theorem-map mismatches. Its output is outside the source tree. Actual checkout HEAD is checked when a Git checkout is available; a source-tree identity is not mislabeled as a local checkout.

`THEOREM_MAP.md` uses the actual native build's numbering and pages. `PROOF_AUDIT.md`, `PRESERVATION_MAP.md`, `LITERATURE_AND_PRIORITY.md`, and the source manifest distinguish mathematical proof, finite arithmetic diagnostics, source reproducibility and unresolved research.

The companion and historical corpus are preservation/evidence, not additional newly refereed main articles. The downloadable review package includes the original exported text corpus and a fresh hash scan. The scan covers 1,709 exported text objects, not every intermediate Git object or a reproof of all historical mathematics. A fresh enumeration found 488 matching branch names, including the newly created R64 branch; it is not represented as a fresh SHA/content read of every historical head.

## Publication and verification status

The isolated R64 workflow is read-only and runs on the new revision branch. Its result is successful only when an actual completed run names the correct SHA. A separate publication record binds the final native outputs to the mathematical source commit without embedding a future commit SHA in its own source. Prior R59 CI success, a queued R63/R64 run, local finite checks and native compilation do not imply R64 independent-host success, formal proof, human approval, exhaustive priority certification or journal acceptance.
