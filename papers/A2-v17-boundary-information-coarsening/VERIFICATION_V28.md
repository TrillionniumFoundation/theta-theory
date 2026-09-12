# A2 v28 execution and verification record

This record separates mathematical proof, exact finite diagnostics, changed-source preservation, revised-module typesetting and complete native execution. None substitutes for another.

## Source identity

Review base: `e5a153b1bbb663c4a5e3153c6a7bdedb7fcd5864`.

Mathematical revision: `6d8f158c60f3636c572daa64779f57c9c9ec757b`, tree `768f467572a3a884073e69065d1239825be8f25e`.

Branch: `revision/a2-v28-common-orientation-quotient-top4-2026-09-12`.

The Git blob identities in [ACTIVE_SOURCE_MANIFEST_V28.md](ACTIVE_SOURCE_MANIFEST_V28.md) were checked against the local source bytes used in the executions below. Subsequent response/navigation/evidence commits preserve those mathematical bytes.

## Executed exact finite diagnostics

With Python 3.13.5, both commands completed and produced byte-identical output:

```sh
python3 tools/check_revision_v28.py > finite-normal.json
python3 -O tools/check_revision_v28.py > finite-optimized.json
cmp finite-normal.json finite-optimized.json
```

The script uses `fractions.Fraction` and explicit exceptions, not removable assertions. It executed 883 finite checks: lattice orientation, Gram invariance, rank-two recovery, conjugation of proper placements, incidence equivariance, holonomy conjugation, finite polynomial-jet parity, normalization and positivity of the density example, folded-density equality, distinct law-valued orbits, and diagonal versus independent channel reversals. Most cases are inexpensive grid identities; the count is not a measure of theorem coverage.

Script Git blob: `8467debd339b36a7c51db0486fb542b28497485b`. Script SHA-256: `d5f1b366689e8773ddc5a0ddc25be7d1105fd5a8dd1e6da22fc44b23444b5c65`.

Result: `diagnostics/v28-finite-checks.json`, Git blob `8edbf8a22284816c1dc555c026dd962068fbb3bd`. No v27 author or referee test count is included in the 883, and those historical suites were not rerun locally in this revision.

## Executed changed-source audit

`diagnostics/audit_changed_sources_v28.py` was executed in ordinary and optimized modes with byte-identical output. It verifies four fetched original source blobs, the exact replacement of the ambiguous orientation sentence, preservation of all sixteen multichannel labels and the entire old observation hierarchy, and the ordered direct-input change from 48 to 49. New v28-labelled references resolve within the revised modules. Its output is `diagnostics/v28-changed-source-audit.json`.

This is not an executed complete recursive graph or inherited-reference audit. Only the full-checkout scanner `tools/audit_native_sources_v27.py`, together with actual engine builds, addresses that separate requirement.

## Executed revised-module typesetting

A local fixture loaded the actual preamble and all three revised mathematical modules. It inserted no artificial labels for missing inherited sections and was explicitly titled as a revised-module fixture, not the main article or companion. Three pdfLaTeX passes completed using:

```sh
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
  -file-line-error revised_modules_fixture.tex
```

Engine: `pdfTeX 3.141592653-2.6-1.40.26 (TeX Live 2025/dev/Debian)`.

The fixture has eight pages. Its final log has zero overfull boxes, zero missing-glyph messages and zero duplicate-label messages. It has **ten unresolved-reference occurrences involving eight distinct inherited labels** because the fixture does not load the full native manuscript. There are no unresolved-citation messages. These unresolved references are not counted as a clean submission-level reference check.

The pages containing the new orientation definition, equivariance proof, classification theorem and corollary were rendered and inspected; no clipping or overlap was found on those pages. This is not inspection of the complete main or companion PDF.

Fixture PDF SHA-256: `eeab6edda905de03d96756256afb4befaccc81971e38b3e7479d42ac6a6606de`.

Fixture log SHA-256: `ff70f7087b5c1bca1248b0feca1bb2d74d4f9bbb0b8cd0659d9de51053310743`.

Result metadata: `diagnostics/v28-revised-module-typesetting.json`. The fixture source is retained at `diagnostics/revised_modules_fixture_v28.tex`; it can be compiled from the paper directory. A recreated fixture has its own PDF metadata/hash. Neither its page count nor its hashes describe the complete A2 article.

## Complete native build: attempted, not executed

A new full-native workflow was actually triggered on the mathematical revision. The live workflow-run and job responses gave:

| Field | Observed value |
|---|---|
| Workflow | `A2 v28 complete native build` |
| Run | `34677164341` |
| Job | `103508962672` |
| Source commit | `6d8f158c60f3636c572daa64779f57c9c9ec757b` |
| Conclusion | `failure` |
| Executed steps | `[]` |
| Runner ID | `0` |
| Runner name | Empty |
| Job completion | `2026-09-12T06:03:58Z` |

The job executed no checkout, diagnostic, source audit or TeX command. It yielded no successful complete-native build evidence. No account or scheduling cause was established; a pre-step failure is not evidence of a TeX failure. Normalized observations are retained in `diagnostics/v28-native-run-attempt.json`.

The workflow archives the pinned complete paper source, runs v27/v28 ordinary/optimized diagnostics, invokes the full recursive native source audit, builds the complete companion before the complete main manuscript, and retains engine versions, logs, PDFs, metadata and hashes. These are the configured steps; they did not execute in the observed run.

**C2 remains open:** no successful complete-native build, full recursive reference/citation audit or complete-PDF visual review is claimed for v28. The revised-module fixture and this record do not close it. This is a submission-validation limitation, not a mathematical counterexample or a change of research scope.

## Reproduction from a functioning complete checkout

From the paper directory, use an output path outside that directory:

```sh
OUT=/absolute/path/outside/the/manuscript/tree
mkdir -p "$OUT"
python3 tools/check_revision_v28.py > "$OUT/v28-normal.json"
python3 -O tools/check_revision_v28.py > "$OUT/v28-optimized.json"
cmp "$OUT/v28-normal.json" "$OUT/v28-optimized.json"
python3 diagnostics/audit_changed_sources_v28.py > "$OUT/changed-source-audit.json"
python3 tools/audit_native_sources_v27.py --output "$OUT/native-source-audit.json"
python3 tools/build_submission.py --output-dir "$OUT/native-build"
```

The retained build utility requires `latexmk`, `pdflatex` and `pdfinfo`, scans both entry points, builds `two_collision.tex` before `main.tex` for the external `TC-` references, and rejects unresolved references/citations, duplicate labels and missing glyphs. It records remaining layout warnings for inspection. C2 can be closed only after successful execution on the complete pinned source and review of the resulting products; a particular hosted runner is not required.
