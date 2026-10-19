# A2-DYN — summable physical-source author revision

Complete native continuation of the original triangular Lorentz gas paper, not a new referee report. The active main contains every260–303 body:260–299 from the latest complete native local source,300–301 from the actual later remote continuation, and new302–303 with complete proofs. The original model, exact event, physical clock and raw four-coordinate target are unchanged.

New mathematics is a collision/incidence-uniform **sum** of fourth-power physical displacements controlled by one positive gap; critical fixed-word singular compactification; simultaneous full-flight/all-center clearance summability; and exact section/phase/source discrepancy accounting on the original roof. Neither full raw pointwise LLT nor the remaining normalized shortage is claimed proved. See `PROOF_LEDGER.md` and the point-by-point `RESPONSE_TO_REFEREE.md`.

## Native qualification

Install Python with the pinned dependencies in requirements.txt, TeX Live including amsart/lmodern/mathtools/microtype/hyperref, and poppler-utils. Then run:

```sh
python3 tools/qualify_revision.py all
```

The qualifier first verifies immutable hashes and every retained predecessor file, then runs all20 mathematical programs in ordinary and optimized modes, compares raw results, typesets the COMPLETE native main three times, audits references/labels/overfull boxes and records actual commands. It fails closed and preserves failed logs. `build/revision/current-validation.json` is the actual receipt for that execution; a prior build receipt is not a current run. `tools/check_current_census.py --recover DESTINATION --details INDEX.json` restores all343 historical proof variants and91 review blobs from the verified object DAG.

## Publication without modifying old paths

`tools/publish_revision.py --workspace EMPTY_DIRECTORY --receipt RECEIPT.json` uses existing ordinary Git authentication, checks the exact upstream base796e70b65ec17bccb165e047534ed07dd4b148e0 and publishes only the new article directory and its dedicated workflow to the paired new refs. No force push. An offline addition-only bundle is not a replacement repository and must never be pushed as its root. Static `PUBLICATION_STATUS.json` is preparation metadata; actual transport/CI status lives in separate delivery receipts. Successful compilation is neither remote CI completion nor mathematical certification.

## Records

Source/identity: `REVISION_BASE.json`, `SOURCE_MANIFEST.json`, `GLOBAL_PREDECESSOR_FILE_MAP.json`, `PROOF_INDEX.json`. Author response/proofs: `RESPONSE_TO_REFEREE.md`, `PROOF_LEDGER.md`, `MATHEMATICAL_AUDIT.md`. History/literature: `HISTORY_PRESERVATION_AUDIT.md`, `LITERATURE_AUDIT.md`, all frozen provenance and exact failed CI. Current command logs are derived outputs outside the self-referential source manifest.
