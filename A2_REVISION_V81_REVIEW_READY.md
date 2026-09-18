# A2 v81 — source review entry

## Fixed revision

**Blind clock pencils and action rigidity** — Qian Qi (inherited author attribution; author verification is not presumed).

Mathematical source commit: **`49c1a5f90deb185189c29844dee3c35118b3a76b`**.  
Revision branch: **`revision/a2-v81-blind-clock-pencils-2026-09-18`**.  
Reviewed v80 source: `831dc905d139377e117138238d20d96833f4122d`.  
Controlling review head: `2edd50e3f97228432ab3c7a1e1f11618f8f45a09`.

The full revised manuscript is [rigidity_v81.tex](papers/A2-v17-boundary-information-coarsening/rigidity_v81.tex). Its shorter [core reading edition](papers/A2-v17-boundary-information-coarsening/rigidity_v81_core.tex) contains the new development only. The core is not described as the full manuscript.

The [point-by-point response](revisions/a2-v81/RESPONSE_TO_REFEREE.md) addresses R80-M1–M20 and R80-T1–T15. The [controlling report](reviews/a2-v80-calibrated-records-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md) remains available unchanged.

## Mathematical changes

The principal theorem reconstructs an unknown visible count, absolute actions and two unknown readout channels from two raw clock matrices. With at least two separated actions, three projective matrices suffice despite unknown endpoint-dependent exposure and common detector functions. Spectral projectors give a finite-order inverse without derivative loss. Unpaired regular phase sheets then determine lifted return systems on the covered target.

The revision includes an actual nonconvex three-sheet shear, an explicit common-deadline delayed protocol, two-projective-clock and one-readout ambiguities, a fixed-source branch-selective physical lower bound, and a finite-record bound without audited calibration. It does not turn full-rank sensor capacity, spectral separation or regular phase coverage into inferred facts. Inherited marked-billiard statements retain their semantic labels and atlas assumptions.

## Preservation and input graph

All seven mathematical paths changed by the source commit are new files. No inherited paper source or review file is modified or deleted. Every substantive input of `rigidity_v80.tex` remains active in `rigidity_v81.tex`, with its original path and theorem labels. The inherited bibliography entries are retained in the combined v81 bibliography; the old bibliography file remains unchanged. The convex companion's displayed heading distinguishes six conditional laws from four raw laws, without editing its source.

The native script recursively checks active inputs and retained bibliography keys. The [core SHA-256 manifest](revisions/a2-v81/CORE_INPUT_SHA256.json) records the source used for the local reading-edition build. The preceding root README is preserved byte-exactly in [README_before_v81.md](revisions/a2-v81/README_before_v81.md).

## Build and verification status

The core was natively compiled with pdfTeX 1.40.26 / latexmk 4.86: **14 pages**, with no undefined references, undefined citations or overfull boxes in the final log. Rendered manuscript pages were inspected. Its PDF SHA-256 is `f70f4f5c0a9343e76c26a2b53847c20cd122d61feb341be529cbe88e4416ffb6`. This PDF was delivered separately; this entry does not claim a PDF binary has been committed to GitHub.

**Eleven numerical regression tests passed**, with seed 810918. They are finite-dimensional algebra checks, not formal mathematical certification. See [local verification](revisions/a2-v81/LOCAL_VERIFICATION.json).

**The full integrated manuscript has not been natively compiled in the local session. No successful remote full build is asserted here.** A dedicated [native workflow](.github/workflows/a2-v81-native.yml) builds both entries, checks the complete active graph and citations, and publishes source-head-named artifacts. An absent, queued, skipped or failed run must not be treated as a successful build. The workflow uses read-only repository permissions and cannot commit or publish a release.

From a checkout of this revision, run:

```sh
python3 tools/test_a2_v81.py
bash tools/build_a2_v81.sh
# Reading edition alone:
bash tools/build_a2_v81.sh --core-only
```

The build requires NumPy, latexmk, the standard LaTeX recommended/extra packages and Latin Modern; the workflow installs them. Output goes to `build/a2-v81/`, including PDFs, actual logs, active-input hashes and environment details.

The [assistance record](revisions/a2-v81/AI_ASSISTANCE.md) distinguishes manuscript preparation from human author approval or journal submission. This branch is a new mathematical revision for independent assessment, not an acceptance decision.
