# A2 v37 — actual execution and verification scope

Date: September 13, 2026. This ledger is not a full native-main build certificate.

## Immutable identities

Repository: `TrillionniumFoundation/theta-theory`. Revision branch: `revision/a2-v37-referee-closure-native-submission-2026-09-13`.

| Object | Identity |
|---|---|
| Latest report commit | `01e772030042ffde9df125c0d40401aee2aabd17` |
| Submission reviewed by that report | `0802bfa20533feff55bf5620d39d6399d5e778f5` |
| V37 mathematical-source commit | `b0c21cd799bbe4d96bab4a7e1e369d5d7152b294` |
| V37 mathematical-source tree | `bf71bcf4f7db673f7a239702c28558e5b78a960b` |
| Native main Git blob | `c67badf42e0e6d1c30c73a54c19918ffe7508621` |
| Edited single-offset chapter Git blob | `63ed36efd417cd23e6f869952627719de00e6ef7` |
| Unchanged companion Git blob | `df44402b17031525c087d39dfedf8dac3ada611d` |

The later documentation/evidence commit adds the runnable checks, historical baselines and this ledger without changing the native mathematical sources above. The tests' source-commit field identifies those mathematical sources, not a claim that the complete repository tree at that SHA contained the later verification files.

## 1. Executed companion build

The native self-contained `two_collision.tex` was copied with its Git blob hash checked. From the paper directory, the following command was actually executed; stdout and stderr were retained together as `companion-build.txt`:

```sh
SOURCE_DATE_EPOCH=1789257600 FORCE_SOURCE_DATE=1 TZ=UTC \
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  '-pdflatex=pdflatex -no-shell-escape %O %S' \
  -outdir=/mnt/data/theta-a2-v37/evidence-v37/companion two_collision.tex
```

Exit status: **0**. Output: **7 pages, 333376 bytes**. Tool identification: Latexmk 4.86 (11 December 2024); `pdfTeX 3.141592653-2.6-1.40.26 (TeX Live 2025/dev/Debian)`. The exact invocation is [retained as JSON](verification/v37/companion-command.json).

| Actual product | SHA-256 |
|---|---|
| `two_collision.pdf` | `9f2a4dc2b68b70a4f931a4c65371675ab8e895bc439dec55c843a84e66fc3670` |
| Final `two_collision.log` | `28c32cc3c31ed29c8c674a84f63796f1304c5f7d1ee3fa710f26bf4f95252c21` |
| Driver `companion-build.txt` | `6e5fb2dc0a4d2175a85d7317e2d3307aa6775ee87c149e19a7b5f0b8e495ed24` |
| `companion-command.json` | `b1841d7a6764902241cf6d798f611479d3a0ee79ee0aa532773237861d73a846` |

The repository retains losslessly compressed complete logs as `verification/v37/two_collision.log.gz` and `verification/v37/companion-build.txt.gz`; the hashes above are of their decompressed bytes. The actual PDF, rendered overview and uncompressed logs are in the `A2-v37-verification-evidence.zip` attachment to the revision conversation, with the PDF also attached separately. They are not represented as a committed full-main PDF or a complete-source archive.

The final companion log contains no unresolved references or citations, multiply defined labels, missing characters or overfull boxes. One `epstopdf` warning reports disabled shell escape; shell execution was intentionally disabled. Visual coverage: all seven pages in a PyMuPDF rendered overview, plus page 5 at larger scale. No clipping or missing glyph was observed in that coverage. This is not a claim that every companion page received full-resolution inspection or that any main-manuscript page was inspected.

## 2. Executed focused checks

From a local source mirror with the exact pinned mathematical files and the added historical baselines:

```sh
python papers/A2-v17-boundary-information-coarsening/tools/check_revision_v37.py > diagnostics.normal.json
python -O papers/A2-v17-boundary-information-coarsening/tools/check_revision_v37.py > diagnostics.optimized.json
cmp diagnostics.normal.json diagnostics.optimized.json
```

All three commands exited zero. Both JSON outputs are byte-identical. Environment: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0. Checks use explicit exceptions, not removable Python assertions.

Script SHA-256: `8e757ce1e6c1fd4d5f6b43f504bc4d6f9e97224877f58541ea87403b6a4f3a04`. Each output SHA-256: `0a8b1b601a04e60b68f0d22949aefa35f0c857770d3ad4c9a8a9001a83a1cbcd`. The ordinary output is [committed here](verification/v37/diagnostics.json); its identical optimized copy is retained in the attachment. The original referee diagnostic source remains unchanged, with SHA-256 `b0794bb7ddbe26503898c56df07b1fdf3fa37d2a230196804ce2b01f670e93bc`.

The eight families are source guards; a four-orbit rooted-tree/gauge example; signed four-density inversion; ninety last-jet blocks and leading recovery; four nonlinear 64-flight stationary/envelope calculations; lattice and reflection identities with marked determinant six; twelve explicit moving-ceiling layer/corner cases; and the original-alternative radial mean example. Maximum nonlinear stationarity residual is `3.0682921481339775e-17`; maximum symmetric envelope discrepancy is `4.763849426048239e-7` against tolerance `2e-6`.

The source guards preserve 52 direct main inputs, 36 inputs in the auxiliary wrapper, and thirteen labels in the edited chapter. **Those counts are not a recursive input-availability audit.** The finite examples do not certify the general theorems or billiard realizability of the illustrative radial models.

## 3. Hosted run and complete-main status

New v37 run: `34735598451`; job: `103666347616`; source commit: `b0c21cd799bbe4d96bab4a7e1e369d5d7152b294`. The queried job is completed with conclusion `failure`, `steps: null`, `logs_url: null`; the artifact list is empty. No cause was established. No TeX execution or source-archive upload is inferred from this run.

**The complete native main was not built or PDF-inspected in this session. C2 is OPEN.** The local source mirror was partial, not a complete checkout. The available companion and finite diagnostics do not replace the main. No success is asserted for an isolated chapter or a shortened replacement manuscript.

The following is the inherited full-checkout build procedure, **not a command reported as successfully executed here**:

```sh
git switch revision/a2-v37-referee-closure-native-submission-2026-09-13
git rev-parse HEAD
git rev-parse HEAD^{tree}
python3 papers/A2-v17-boundary-information-coarsening/tools/build_submission.py \
  --output-dir /tmp/a2-v37-complete-native
```

The output directory must lie outside the manuscript tree. The driver traverses the native inputs, runs its retained finite checks, builds `two_collision.tex` and `main.tex`, and saves actual products and logs before temporary-directory cleanup. A successful run must still be followed by inspection of the complete PDFs and an accurate record of inspection coverage. Any subsequent native source changes require a new source identity and assessment of the need to rebuild. Merely retaining this command, a workflow, or this ledger does not close C2.
