# R75 starting-baseline evidence

This folder contains exact copies of the completed read-only baseline audit
at its recorded 2026-10-21 cutoff. `COPIED_RECEIPTS.json` lists each copied
file and its SHA-256. The original files are preserved byte for byte, including
historical source paths and observed recovery locations inside their receipts.
`BASELINE_LOCK_R75.json` is the current control; the older R74 baseline files
elsewhere in `provenance/` remain historical.

The complete 275-file R74 source and 48-file publication were recovered and
Git-blob-checked. The source ZIP, historical text corpus and original validation
ZIP are not duplicated in this evidence folder: the immutable R74 publication
contains their hash-verified parts and restoration instructions. Their current
paths are fixed in `SOURCE_PROVENANCE.md` and the baseline lock. Original
recovery directories mentioned in receipts are observations of the audit
workspace, not new repository dependencies.

`AUDIT_ARTIFACT_HASHES.json` is the original audit's artifact inventory; it
includes recovered archives and extracted PDF text outside this copied
subset. `COPIED_RECEIPTS.json` is the inventory of the subset actually included
here. Neither inventory is a mathematical proof, a native build, a hosted CI
run, a human assessment or an editorial decision.

## Final current verifier configuration

The current source uses the **209-statement** configuration documented in
`VERIFIER_PORT_FINAL_209_AUDIT_R75.md` and
`VERIFIER_PORT_FINAL_209_INVENTORY.json`. Earlier 208-statement port receipts
are retained unchanged as development snapshots; the added sharp
singular-coefficient lemma accounts for the one-statement increase.
