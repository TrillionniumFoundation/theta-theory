# A2 v35 execution record

## Identities

Addressed referee: `d51c06689ba540711b2f890beb35eb235dba13e4`. Reviewed v33 submission: `b577cffcb3ca5597cb4905269bea9de3bd4ead38`. Preserved v34 predecessor: `127f9334f15c5fb12307bd691973d1eb44e499e8`. None of these is substituted for a tested v35 assembled-source SHA.

The initial v35 source identifies its mathematical inputs by exact blobs: `main.tex` is `d21ea5c3c3926890505a8e44683b8e5de91e9d8b`; the revised vector chapter is `8ff3ce7334954d6544555e9867a12fa805ca5ea0`; the unchanged companion is `df44402b17031525c087d39dfedf8dac3ada611d`. A subsequent execution-ledger update records the immutable assembled commit and actual hosted attempt separately.

## Actually executed local checks

The companion source was retrieved from v34 and verified byte-for-byte by its Git blob (20,663 bytes; SHA-256 `ae7199a03a72b9822b345a971717d70ebd03e228d26b8fd0afcaaf39da6507f7`). It was compiled without alteration using the native command below, not a shortened fixture:

```sh
SOURCE_DATE_EPOCH=1789257600 FORCE_SOURCE_DATE=1 TZ=UTC LC_ALL=C.UTF-8 \
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  '-pdflatex=pdflatex -no-shell-escape %O %S' two_collision.tex
```

The command returned zero and produced a seven-page, 333,376-byte PDF with SHA-256 `9276b3a1391099bc390406cfc33cdfec32c9ad89088799e0f88e8a80d82c7e8a`. The engine was pdfTeX 1.40.26. The final log contains no unresolved references or citations, multiply-defined labels, missing-character reports, or overfull/underfull boxes. The `epstopdf` shell-escape warning records the deliberately disabled shell escape. All seven pages were rendered and inspected in a contact sheet; this is a layout inspection, not a new proof certification of the companion.

`tools/check_revision_v35.py` was executed with ordinary Python and `python -O`. Both runs passed 24 finite arithmetic and source-preservation checks with byte-identical JSON output (SHA-256 `9fbe4f211b53dbae1e385657e96e3983c83bd467853b1a983969d6aec9ee5794`). The checks retain all eight theorem/lemma statements in the changed chapter, the abstract, 52 direct inputs and 36 auxiliary inputs. Finite numerical examples are diagnostics, not proofs of asymptotic theorems.

An isolated seven-page syntax check of the complete revised vector chapter with the actual preamble also returned zero and had no overfull/underfull boxes. Its genuinely external theorem references and bibliography citations remained unresolved. It is not `main.tex`, is not a submission PDF, and is not evidence of full-main completion.

## Complete-native requirement

The branch-specific workflow `.github/workflows/a2-v35-native-build.yml` archives the complete immutable source before installing tools and invokes the existing `tools/build_submission.py` on `two_collision.tex` and `main.tex`, with all active inputs and bibliography. It retains real failure logs as well as successful products. This section records the initial evidence state: the full main has not yet been certified by the local companion or syntax checks above. The workflow definition itself does not close C2. Any actual attempt, source commit, product hashes and subsequent PDF inspection are recorded explicitly rather than inferred from a configured job.

Successful compilation would verify the assembled artifact, not establish journal acceptance or certify all mathematics. Existing theorems are not weakened because an execution check is incomplete.
