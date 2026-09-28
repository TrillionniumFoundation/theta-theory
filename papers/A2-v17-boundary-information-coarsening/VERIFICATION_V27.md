# A2 v27 verification record

This record separates mathematical arguments, finite calculations, changed-source checks, revised-module typesetting, and complete native execution. It is not a journal decision or a proof-assistant certificate.

## Pinned source

The mathematical revision is `416124f13f182f8e2d876f93090865f13269c86b`, tree `da8779b9c2a7352486931a64252752f3c6eae0b5`, on `revision/a2-v27-observed-type-smooth-jets-top4-2026-09-12`. The preceding report is `a5b2d4b5a9ed31059e16e5011c8010579d713598`, reviewing `cefd89084682cc2e31d730eab1a4b8d8eaac0bbe`.

The new native source bytes checked locally match the Git blob hashes in `ACTIVE_SOURCE_MANIFEST_V27.md`. Later documentation and diagnostic-tool commits do not change that mathematical source snapshot.

## Actually executed finite diagnostics

`tools/check_revision_v27.py` was run with both ordinary Python and `python -O`. The outputs are byte-identical. The executed script's Git blob is `2b3c99f853ab99fba101cc6850d117a6731d7d7a`, matching the uploaded GitHub blob; SHA-256 is `e52a2d454834bdb6b11cf643043f46f0d66d1018b5c7eb385aaea967c349a4ab`.

The 884 cases comprise 99 exact signed density/amplitude identities, 108 determinant identities, 108 inverse-block checks, 432 support-gauge checks, 27 two-flight positive-core fixtures, 27 fixed-endpoint embedding checks, 12 varying-disk parameter checks, 66 exact smooth-remainder majorants, and five finite disjoint-output analogues. Required checks use explicit exceptions and are not disabled by optimization.

For the 27 two-flight fixtures, the largest stationarity residual was `6.938893903907228e-18`, largest excess `0.000799920047983349`, and smallest positive mixed flux `0.23638886647151064`. These are finite floating-point diagnostics, not continuum statements or certified interval computations.

Results: `diagnostics/v27-finite-checks.json`. No claim is made here to have rerun the v26 author's 3,343 checks or the referee's 347-case script. Their historical results remain attributable to their original records, not this execution.

## Actually executed changed-source checks

`diagnostics/v27-changed-source-audit.json` records local byte hashes and preservation checks on the fetched old/new introduction, old/new signed inverse, the new comparison and support subsection, and the full direct `main.tex` input list. The 32 old signed-inverse labels and nine old introduction labels are preserved. Exactly three direct main inputs are replaced, one is added, and all other input ordering is unchanged.

This limited check is not an executed recursive scan of every inherited native input. `tools/audit_native_sources_v27.py` is the separate full-checkout scanner; its full result is not inferred from the changed-source check. Both new Python programs passed local Python syntax compilation.

## Actually executed revised-module typesetting fixture

A clearly marked local fixture compiled the four new/revised article modules for three pdfLaTeX passes using `amsart` and the manuscript's mathematical packages. It did not replace either native entry point. It inserted no artificial labels for inherited results.

The result has 16 pages. The final log reports zero overfull boxes, zero missing-glyph messages, and zero duplicate-label messages. There are 23 unresolved-reference warnings and four unresolved-citation warnings because inherited sections and the full bibliography are not loaded in this fixture. These are not silently treated as a clean native reference check. Selected rendered pages were inspected for layout.

Engine: `pdfTeX 3.141592653-2.6-1.40.26 (TeX Live 2025/dev/Debian)`. PDF SHA-256: `b7318a34af4cf3150c66bfe9801bd67ba242966271c8ccb65d8b75a98efcdfe5`. Log SHA-256: `572502bd931426bb836ab92226d032b08f554b5e8549c379868c3b89831b8767`.

Result metadata: `diagnostics/v27-revised-module-typesetting.json`. The fixture is not the full A2 PDF, and its page count is not the full article's page count.

## Complete native build: not certified

A GitHub Actions run was actually triggered at the mathematical source commit:

| Field | Observed value |
|---|---|
| Workflow | `A2 v27 complete native build` |
| Run | `34674173652` |
| Source commit | `416124f13f182f8e2d876f93090865f13269c86b` |
| Job | `103500916466` |
| Status / conclusion | `completed / failure` |
| Executed steps | `[]` |
| Runner ID | `0` |
| Runner name | Empty |
| Job completed | `2026-09-12T04:53:41Z` |

The job did not execute checkout, dependency installation, or TeX. This supplies no native PDFs, logs, successful graph audit, or full-reference verification. It is not evidence that either manuscript fails to compile. The underlying scheduling/account cause has not been established from the available response and is not guessed here.

The final workflow and tools require complete native inputs, archive the exact source commit, record versions, run normal/optimized diagnostics and the full recursive scan, build both `two_collision.tex` and `main.tex` through the retained full build utility, and archive logs, PDFs, page metadata and hashes. Only an actual successful execution of those steps can close the referee's native-build request.

## Subsequent complete-checkout attempt and final evidence

After the mandatory full-audit tools and workflow were committed at `852bfc5981f067b0ad0f701137fbb819f56c2479`, a second run `34674631142` executed as an Actions scheduling attempt. Its job `103502162490` completed with `failure` at `2026-09-12T05:04:09Z`, again with `steps=[]`, `runner_id=0`, and an empty runner name. No diagnostic or TeX step executed. The normalized observations from both job-API responses are committed in `diagnostics/v27-native-run-attempts.json`.

The mathematical source bytes at this second source commit remain identical to the mathematical snapshot `416124f13f182f8e2d876f93090865f13269c86b`. The final evidence-only update changes no native source or workflow. Two pre-step failures do not constitute two failed TeX compilations, and neither is counted as a successful full native build. The pending native execution requirement is unchanged.

## Reproduction from a complete checkout

Use an output directory outside the manuscript tree:

```sh
P=papers/A2-v17-boundary-information-coarsening
OUT=/absolute/path/outside/the/manuscript/tree
mkdir -p "$OUT"
python3 "$P/tools/check_revision_v27.py" > "$OUT/v27-normal.json"
python3 -O "$P/tools/check_revision_v27.py" > "$OUT/v27-optimized.json"
cmp "$OUT/v27-normal.json" "$OUT/v27-optimized.json"
python3 "$P/tools/audit_native_sources_v27.py" --output "$OUT/native-source-audit.json"
python3 "$P/tools/build_submission.py" --output-dir "$OUT/native-build"
```

The build utility requires `latexmk`, `pdflatex`, and `pdfinfo`. Its source graph includes the complete auxiliary compendium and active bibliography. A successful shortened fixture is not an alternative to these commands. The mathematical revision is committed for re-review; the missing complete native execution remains explicitly open.
