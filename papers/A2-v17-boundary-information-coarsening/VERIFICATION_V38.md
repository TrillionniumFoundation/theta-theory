# A2 v38 — execution and verification ledger

Date: September 13, 2026. This ledger separates software tests, finite mathematical diagnostics, genuine miniature TeX integration, native companion execution and the still-unbuilt complete main. It is not a universal proof certificate.

## 1. Version identities

| Object | Identity |
|---|---|
| Latest referee report commit | `377efa79597776e75e3cc1d399c1986edd097aaf` |
| Reviewed v37 submission | `6c311aa389e3af833f06f14ae98de7bfc28c1327` |
| v38 mathematical-source commit | `c206a27ba01f20f1a21b780e6d71c77a837ef11d` |
| v38 complete inherited source and repaired-tools commit | `7d34d96a7c2dd974ab3725e009bbb584d3228114` |
| Tree at the latter commit | `45dad0720f58927125e506875504fcd49a9bf12d` |

Later documentation/evidence changes do not change the native mathematical source at the latter commit. A local integration-fixture commit or partial companion-mirror commit is not the remote full-tree identity.

## 2. Forty-one source-provenance regressions — executed

From the paper directory:

```sh
python -B tools/check_revision_v38.py > diagnostics.normal.json
python -B -O tools/check_revision_v38.py > diagnostics.optimized.json
cmp diagnostics.normal.json diagnostics.optimized.json
```

Both Python executions returned zero; the comparison returned zero. All 41 checks passed. The saved [normal output](verification/v38/diagnostics.normal.json) and [optimized output](verification/v38/diagnostics.optimized.json) have identical SHA-256:

`5ae4f5224efa06dcc3a52f6ded2068ae19270bb3682e54ac9c2553737f57c99f`.

Exact tested source identities:

| File | Git blob | SHA-256 |
|---|---|---|
| `tools/build_submission.py` | `faa4310cb5fe41f2869f3d840b760a4a6ea381f3` | `f5d3adf010bcb7361db404e72856086b00dce63201ba24c5dc63ab02588df478` |
| `tools/source_provenance.py` | `d944aac5604f123795f5c744c2042176c353b981` | `495061bf4962dd07f2e7b551a1488c9c9e09769a8e7ea4cda353f06bc8a47739` |
| `tools/check_revision_v38.py` | `aed637e0574429039b26d5cbfb66a58219a8f139` | `3c6c5736088bbd7062fb226fd181630d114b21478e8763c1ce97dd80118b4189` |

The exact-driver negative cases mock TeX and `pdfinfo`; their fixture PDF bytes are deliberately not genuine PDFs. Those tests validate rejection behavior, not typesetting. Independent cases exercise actual Git objects, working-tree checks, source archives, recursive input coverage and imported companion-auxiliary provenance. Explicit exceptions remain active under `python -O`.

## 3. Six retained finite mathematical families — re-executed

The original referee script remains at [reviews/a2-v36-external-harsh-top4-2026-09-13/diagnostics.py](../../reviews/a2-v36-external-harsh-top4-2026-09-13/diagnostics.py). Its Git blob is `39f24673fc43580fcc8c7f39d79f26cfa9138d01`; SHA-256 is `b0794bb7ddbe26503898c56df07b1fdf3fa37d2a230196804ce2b01f670e93bc`. The local execution copy was verified against both identities without modification.

```sh
python -B reviews/a2-v36-external-harsh-top4-2026-09-13/diagnostics.py > mathematical-regressions.normal.json
python -B -O reviews/a2-v36-external-harsh-top4-2026-09-13/diagnostics.py > mathematical-regressions.optimized.json
cmp mathematical-regressions.normal.json mathematical-regressions.optimized.json
```

Both executions and comparison returned zero. All six families passed. The [normal](verification/v38/mathematical-regressions.normal.json) and [optimized](verification/v38/mathematical-regressions.optimized.json) outputs share SHA-256 `3849a226b037bc14b24b25aab2cfa8bf316bf1ffa0d32889ce871eb44d37cd11`.

The nonlinear finite half-line test solves four 64-flight stationary systems for two starting types and two signed endpoint values. Its maximum stationary residual was approximately `3.0683e-17`; the maximum symmetric envelope-coefficient discrepancy was approximately `4.7639e-7`, below the stated `2e-6` diagnostic tolerance. These are finite numerical checks, not the general analytic theorem. The script's historical manuscript field is deliberately preserved and is not a v38 complete-source certification. Earlier v37 version-only source guards were not relabelled as current tests after the intentional v38 edits.

## 4. Genuine TeX integration of the complete new CLI — executed on fixtures

The full `build_submission.py` CLI was genuinely executed in a small local Git repository, commit `40c6fc374ce4a03cec32888b1b3d173500c2928f`. Both entries are explicitly labelled one-page integration documents, not the A2 main or companion. The two inherited diagnostic scripts are labelled stubs in this fixture; the new 41-test script and both new build modules are the exact tested sources above.

Both entries built with exit code zero. The main fixture uses `xr-hyper` to consume the first fixture's verified auxiliary file, so this run exercises the generated cross-document input path as well as normal source recording. Genuine PDF pages, logs, tool versions, actual-input manifests, generated-input provenance and the frozen fixture source archive were produced. [The summary](verification/v38/real-tex-integration-summary.json) records the result. The raw evidence and source archive are included in the attached revision evidence packet, prominently labelled as fixtures. No A2-main build or visual-inspection conclusion is drawn from this run.

## 5. Genuine native companion — executed and visually inspected

The unchanged `two_collision.tex` at remote source commit `7d34d96a7c2dd974ab3725e009bbb584d3228114` has Git blob `df44402b17031525c087d39dfedf8dac3ada611d`. Its 20,663 local bytes were verified against that blob. A partial local mirror containing this exact source and the exact new build/provenance modules was frozen through Git objects; local mirror commit `8f7da5db82289383f8affddea92cc80ae60cf86e` is not the remote complete repository commit.

The exact new `build_entry` implementation was executed for `two_collision.tex`, using the frozen-source and actual-recorder checks. The recorded command was:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder \
  '-pdflatex=pdflatex -no-shell-escape -recorder %O %S' two_collision.tex
```

It returned zero and produced a genuine seven-page PDF, 333,376 bytes, SHA-256:

`9276b3a1391099bc390406cfc33cdfec32c9ad89088799e0f88e8a80d82c7e8a`.

The final log has no unresolved references/citations, duplicate labels/destinations, missing characters or overfull-box report. It contains the expected package warning that shell escape is disabled. Actual compilation bytes matched the frozen source and declared remote companion blob. [The native-companion summary](verification/v38/native-companion-summary.json) records the local/remote identity distinction, command, return code, source verification and PDF identity.

All seven pages were rendered with `pdftoppm` at 105 dpi and inspected in two labelled contact sheets. No visibly clipped or overlapping text or equations, broken glyphs or black squares were observed. The short bibliography occupies page 7. This is a companion layout review, not a fresh proof audit. The PDF, full raw logs, recorder inputs, tool versions, frozen companion source and inspection sheets are included in the revision conversation's attached evidence packet; no standalone font files are included.

## 6. Complete native main — not built; C2 open

The committed hosted workflow was actually triggered for source commit `7d34d96a7c2dd974ab3725e009bbb584d3228114`: run `34743133630`, job `103686134246`. The returned metadata show failure, no executed steps, runner ID zero and no artifacts. [The recorded metadata](verification/v38/hosted-run.json) do not determine the underlying cause. No executed TeX command is recorded.

A complete local checkout was not materialized for this session; the local source used for the actual companion build was explicitly partial. No complete-main PDF was generated, no complete-main final log or recorder was obtained, and no complete-main PDF inspection occurred. Thus C2 remains open. The full native source remains available on the new GitHub revision branch, with all inherited inputs retained. Configuration of the [complete build protocol](NATIVE_BUILD_PROTOCOL_V38.md) is not counted as its execution.

## 7. Preservation and limits

[The preservation record](PRESERVATION_V38.md) and [machine-readable comparison](verification/v38/manuscript-preservation.json) identify every changed native mathematical file. Proof blocks and labels are preserved; counts are structural evidence, not a correctness certificate. The response does not convert finite diagnostics, a companion build or a hosted task into complete-main delivery or a journal decision.
