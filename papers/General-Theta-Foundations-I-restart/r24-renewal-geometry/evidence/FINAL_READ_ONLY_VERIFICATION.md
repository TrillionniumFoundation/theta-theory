# Final read-only verification — General Theta restart R24

## Immutable chain

Ordinary mathematical source: `5cb42423f8ea62139bd51093a5b6ba69379337b4`. Native ordinary-source tree: `c5a5a0c63abf76f4535c544ce75f82ee93b14c7f`.

Built-artifact commit: `7c5eb175ab6553952ff7d62766441fd9f1723bfb`, whose sole parent is that source commit. Its root tree is `ec2cff82e79358705c2d22b88f44d2b27648c219`.

The final verification commit is the append-only child containing this file. Its exact SHA is obtained from Git metadata and the read-back delivery refs; a file cannot embed its own containing commit hash. Its complete diff from the artifact commit must add only:

- `evidence/INDEPENDENT_REBUILD.json`
- `evidence/FINAL_READ_ONLY_VERIFICATION.md`
- `evidence/REFEREE_PACKET.md`
- `evidence/REVIEW_HANDOFF.md`

No mathematical source, manifest, PDF or prior receipt changes in this final commit.

## Actual execution

GitHub Actions run `37953630756`, attempt 1, job `113898482901` completed successfully. The ordinary source was committed and pushed before the full build. Artifact publication was a distinct direct child. The actual downloaded artifact was `11626892691`, SHA256 `6da621609b707cdc792119bbad224087aac311c9ead64620964d374bd2c3394f`.

Independent reconstruction used that downloaded source/artifact packet, not an uncommitted local copy. A complete independent process exited zero. All 572 downloaded input file hashes remained unchanged; outputs were written outside the input tree. The detailed execution record notes an earlier tool-timeout interruption and does not count it as a successful build.

Both the hosted TeX Live 2023 and independent TeX Live 2025 environments completed 24 isolated PDF builds, three passes each (18 technical builds and six inherited cover builds). Native and inherited normal/optimized regressions agree. Native checks: 4,993, comprising 4,971 exact rational assertions and 22 finite matrix diagnostics. Nested historical test counts are not added as new independent tests.

The final native source audit covers 33 ordinary files plus manifest, 10 active TeX inputs, 64 labels, 84 cross-references, 16 bibliography entries, and 19 formal statements with 18 proofs. No undefined references, multiply defined labels or overfull boxes were found. The new article has 20 pages; the eight complete companions have 234 pages; the nine delivered PDFs total 254 pages.

Repeated builds inside each environment were byte-identical. Cross-environment PDF hashes differ, but all nine page counts and normalized texts agree. All 254 pages rendered identically with MuPDF 1.26.7 at 97.2 dpi. The corrected native 20 pages were visually inspected. No claim is made that automated render comparison re-referees historical proofs.

## Preservation and review baseline

Canonical remains `18000b21e4bfd89180ccb069e46ac0f21621f34d`; latest retrieved R22 review remains `212bec0b6f254990552584db35473e0ac108e2d7`; R23 research contract remains `6dd51dd292bb70e8bd3015d3c376f8c335862d66`. The publication receipt checks 27 inherited path/object identities, including the controls, report and old restart subtrees. No earlier canonical, review, realization or frozen-archive ref was updated. The final review-branch enumeration returned 15 restart reviews through R22 and an empty continuation page; no later restart report was found in that enumeration.

`REBUILD_NOTE.md` records the correction made after the first successful R24 build: the full-program calibration loss bound is `diam(K)^2+5`, because arbitrary calibration readouts can have squared error `4 delta^2`. The attaining zero readout still has error `delta^2`, and the matching law is unchanged. The final source and both full rebuilds include this correction. The first artifact remains in Git ancestry and is not the referee object.

The audit and build scope is exactly the native article and stated complete companions. This is not a new certification of every v1–v96 proof, every historical report or every realization paper. The claimed mathematical results remain subject to independent correctness, novelty and significance review.
