# R75 verifier and provenance port audit

This is an author-workflow implementation audit, not a mathematical referee
report. It records the port from the exact R74 files archived under
`inputs/r74/`. The fresh starting baseline is fixed by
`BASELINE_LOCK_R75.json`; the port changes only the independent R75 source.

## Fixed identities and full preservation

`seal_source.py` now fixes R74 source
`29b999abf11c43709e64be58765aa1984d13ac91`, publication/base
`c2c05ee3dccd23588790cd92d2aa2b0b3dac00e0`, source path
`papers/General-Theta-Foundations-I-restart/r74-positive-memory-structure`
and tree `1a8cb2a174e5fbb1aa680f95cac62bd2db5f3d6d`.
The full original source manifest is fixed independently by SHA-256
`f67520ba70140c15fc77ea51fa8ecd51dce549c7427dbd4aed9585636a072e92`.

The new `complete_predecessor_checks()` requires all 275 original files,
including the original manifest itself. It rejects missing or duplicate
original paths, duplicate preserved destinations, changed original metadata,
wrong predecessor identities, altered modes, altered bytes and omitted
preservation rows. The old manifest's fixed hash prevents a shortened local
map from approving its own omissions. All 275 files currently pass: 253
same-path originals and 22 originals archived under `inputs/r74/`.

Strict Git verification additionally obtains the actual recursive old Git
tree, requires its path set to equal the complete preservation map, and
compares every original blob and mode with the actual preserved copy.
It verifies both the source and publication contain the fixed R74 paper
tree, the new source commit descends from the publication, and all committed
changes from that base lie in the independent R75 source directory.

`CURRENT_RETAINED_BODY_IDENTITIES.json` now fixes 55 native proof/support
bodies at R74, including all newly inherited R74 sections. The exact
32,284-byte inherited supplement suffix remains fixed at SHA-256
`a1505059fc305c8918875445ca07b5c69e79b16f1d247e402bad8089b101ead7`.
The entire 34-file R58 companion and exact controlling R65 report remain
unchanged gates.

## Explicit inventories and execution gates

The old compiled index is now `inputs/r74/THEOREM_INDEX.json`: all **197**
labels must survive in the current native pair. The fixed expected current
count is **208**. At the final port inventory check, actual active-source
labels were exactly 208, with eleven additions and no missing or duplicate
inherited labels. These source counts do not replace the verifier's actual
compiled label, statement number, page and source checks. Current entries
use `inherited_from_r74`, and the current schema is
`theta.r75.compiled-theorem-index.v1`.

The inherited diagnostic list contains exactly **18** unchanged scripts.
Strict verification compares each with its actual R74 Git blob. The final
fixed full inventory has **20** suites, adding only:

- `diagnostics_r75_nonabelian.py`;
- `diagnostics_r75_conditional.py`.

Every declared suite must exist, run normally and under Python `-O`, have
byte-identical outputs, have no checks implemented as removable `assert`
statements, declare PASS and report consistent positive exact/floating group
counts. Duplicate suite names or filenames fail. The explicit final suite
count must be 20. The initial port deliberately had fail-closed unfinished
counts; the earlier syntax receipt preserves that intermediate observation,
while `VERIFIER_PORT_FINAL_INVENTORY.json` records the final explicit values.

All existing strict gates remain: exact full current Git HEAD; current source
tree equality; immutable source before and after execution; actual paired
LaTeX and retained-companion compilation; no final undefined reference,
citation, duplicate-label, changed-label or overfull warning; exact compiled
index matching; complete source manifest equality; fresh external output
directory; and separate failed-run receipts. PDF names and current manifest,
index, success and failure schemas are ported to R75. Historical R74 names
remain where they identify inherited objects.

Draft mode remains visibly distinct from strict mode. It cannot claim an
exact source commit or issue final PASS; diagnostic skipping is permitted
only for a draft build. A strict local PASS remains distinct from hosted CI,
remote publication, mathematical proof, human assessment and editorial
judgment.

## Evidence copied and verification actually performed

The `R75-baseline/` folder contains 25 byte-identical selected receipts from
the completed starting audit, listed in `COPIED_RECEIPTS.json`. The baseline
lock, head delta, all source/publication identities, the full historical
per-member recheck, PDF readability and native-input closure receipts retain
their original content. The large source, validation and historical archives
remain available from the immutable R74 publication; their recorded hashes
are not assertions that those archives were copied into this folder.

Both ported Python files were parsed for syntax. Direct pinned preservation
checks were run and passed. The explicit active-source statement inventory
was independently counted. These results are recorded in
`VERIFIER_PORT_FINAL_INVENTORY.json`, including script hashes at that check.
No diagnostic suite, native compilation, source sealing, strict current-Git
run or hosted workflow was executed by this port audit. Those execution
results, if subsequently completed, belong to their own actual receipts.
