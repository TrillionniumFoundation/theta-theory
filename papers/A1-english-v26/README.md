# A1 English v26

**Attainable information, exponent collisions, and adaptive order**  
Qian Qi — 7 September 2026

Revision branch: `revision/a1-english-v26-separator-capacity-2026-09-07`.

## Read the revised submission

`main.tex` is the complete principal-article entry point. It retains the direct scalar collision classification, the entire v25 adaptive graph development and its original proofs, and adds the separator-capacity and collision-path phase results. `companions.tex` is the complete, separately compiled companion, with its original source and proof routes retained. This is a native source directory: it does not depend on a neighbouring manuscript directory or a network download.

`RESPONSE_TO_REFEREE.md` answers the controlling v25 report point by point. `PROOF_LEDGER.md` is the supplied, versioned proof ledger requested in E25.2. `review-basis-v25/REFEREE_REPORT.md` is the exact controlling report, not a rewritten summary. `NATIVE_SOURCE_RECORD.json` pins the input commits and inherited Git objects.

The three definite corrections are the Amarilli–Groz bibliography metadata, the missing proof-ledger delivery, and actual quantifier/individual-cap negative controls. The additional mathematics comprises a finite-selection lemma, a separating-set theorem for adaptive paths, an explicit first-block-evidence graph converse on the subset lattice, a profile-recovery corollary, a subset recursion, a general analytic collision-path phase law, and the full four-phase analysis of the existing positive 24-trial star. The classical flow–cut certificate is credited and proved as a supporting proposition.

The new quantitative theorem uses the original visited-set/label decoder. The old qualitative theorem for a stronger free-order-prefix decoder remains unchanged. Graph size, query recovery, local density and common-event mass are not hidden behind a claim of graph-size-uniform constants.

## Build offline

From a checkout of this branch, with Python 3.10 or newer:

```sh
python papers/A1-english-v26/build.py --prepare-only
python papers/A1-english-v26/build.py
```

The second command requires `pdflatex`, `pdfinfo`, the AMS/Latin Modern/geometry/microtype/booktabs/mathrsfs packages and `xr-hyper`/`hyperref`. It produces `main.pdf`, `companions.pdf`, both expanded TeX files in `build/`, and `BUILD_REPORT_V26.json`. Five alternating passes resolve cross-volume labels. Undefined, duplicate, overfull or unsettled-reference warnings are treated as failures by the inherited builder. The first command performs source, reference, preservation and diagnostic checks without asserting that TeX ran.

The builder reconstructs only the redundant historical audit expansions, verifies the historical manifests and the pinned v25 source blobs, checks complete inherited formal-block identities and multiplicities, and runs the exact diagnostics normally and under `python -O`. `build_legacy_v24.py` and `materialize_legacy_v24.py` are preserved original helpers, explicitly named as historical code. The new `materialize.py` prepares v26; it does not restore an older main entry point.

For the finite checks alone:

```sh
python papers/A1-english-v26/diagnostics.py
python -O papers/A1-english-v26/diagnostics.py
```

## What was actually checked in the revision session

The exact suite completed **843 checks**, with byte-identical normal and optimized output. `DIAGNOSTICS.json` gives category counts, actual witnesses and the tested script hash. The newly written mathematical sections were locally typeset in a seven-page isolated harness, with inherited references explicitly marked as external; the rendered pages were inspected. That harness is not the complete principal article and does not establish full cross-volume compilation.

**A full native two-volume build was not executed in this session. No successful GitHub Actions run is asserted.** `SESSION_VALIDATION.json` records that distinction. A full-build success receipt is generated only after the documented build command really completes. Source identity, successful finite tests and typesetting are not independent referee approval or formal mathematical certification.

## Preservation and historical attribution

The native v24 directory tree `79d66f7b4fd132923d28068f283b88f59276ec21` supplies the scalar source, full companion and historical derivation files. The v25 mathematical subtree is copied from `032901b816d2adbe383f0a4d617b71fcb6088255`, with only its active bibliography metadata corrected. The reviewed v25 main entry point is retained as `baseline-v25-main.tex` for expanded-source preservation comparison. Older repository directories and branches remain untouched.

The deterministic shared-memory and additive-bit calculations are credited to the actual v10 shared-memory manuscript at `da5abea9f40244879115d5fbcfbda375bc9a123e`, Sections 8–9. The controlling review assessed v25 at `8a84075ee518035069d38fd9262bd455aff4ac86`; its report was read at `ab0ebddd80f1e46712650eb6730e113e5c66562f`. New results are submitted for renewed review of both their proofs and significance, without weakening the retained theorems or predicting a venue decision.
