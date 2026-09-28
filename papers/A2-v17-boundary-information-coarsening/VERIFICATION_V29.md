# A2 v29 — execution record and remaining native-main requirement

Mathematical source: `78852f2ccf828385fd45063c1b58c0d474ddf6c5`.  
Review base: `5f10927a6399ebec0492b7f87b622ec80a4df631`.  
Branch: `revision/a2-v29-equivariant-density-stability-top4-2026-09-12`.

The following are distinct checks. A successful finite diagnostic, source comparison, or selected-module fixture is not a successful native-main build. **C2 remains open for the full main submission package.**

## 1. Executed exact finite diagnostics

`tools/check_revision_v29.py` was run in ordinary and optimized Python; the outputs are byte-identical. The 12,443 rational checks cover asymmetric exact-model action/amplitude recovery, transported ratios/radicals/numerators for nonfactorized perturbations, the fixed-anchor counterexample, finite polynomial-jet reflection and anchored projection, and terminal censored failure encoding. The diagnostic does not use Python `assert`, so optimization does not remove its checks.

The witness gives squared values `107/22500` and `4/837`, with difference `-49/2092500`. The script SHA-256 is `efa21131f44d3af8a5740f96f78b0c0ae3d3bb4c16819dc3dabaff9446e3a458`.

Outputs: [ordinary](diagnostics/v29-normal.json) and [optimized](diagnostics/v29-optimized.json). These are finite implementation checks, not a certification of infinite-dimensional proofs or a journal-significance assessment.

## 2. Executed changed-source and preservation checks

The locally materialized sources were checked against their Git-blob identities. The [changed-source audit](diagnostics/v29-changed-source-audit.json) records the 50 direct native inputs, the unchanged 36-input auxiliary entry, the unchanged abstract, and the exact preservation of the orientation classification prefix, all inherited orientation labels and the final folded-record remark. It records SHA-256 and Git-blob identities of the relevant sources.

The GitHub comparison from the pinned review to the first mathematical commit shows no removed files and changes only the existing main entry, with the other mathematical changes added as versioned files. The second mathematical commit changes only the new hierarchy paragraph. Exact prior-entry and navigation archives are retained. This does not amount to executing the recursive native-main scanner locally.

`tools/check_preservation_v29.py` is also supplied for a full Git checkout. It rejects deletion of any review-base path and requires exact archives for the narrowly permitted inherited-entry changes. Its presence is not presented as a locally executed full-checkout test.

## 3. Complete native companion: executed successfully

The complete `two_collision.tex`, with no substituted or shortened sections, was materialized and its blob checked:

- Git blob: `df44402b17031525c087d39dfedf8dac3ada611d`.
- Source SHA-256: `ae7199a03a72b9822b345a971717d70ebd03e228d26b8fd0afcaaf39da6507f7`.
- Source size: 20,663 bytes. Its repository TeX-input closure consists of this one file; system packages and fonts are resolved by the native engine.

The following command returned exit code zero:

```sh
SOURCE_DATE_EPOCH=1789084800 FORCE_SOURCE_DATE=1 TZ=UTC LC_ALL=C.UTF-8 \
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
  '-pdflatex=pdflatex -no-shell-escape %O %S' two_collision.tex
```

Engine: `pdfTeX 3.141592653-2.6-1.40.26 (TeX Live 2025/dev/Debian)`. Driver: `Latexmk, John Collins, 11 Dec. 2024. Version 4.86`.

The resulting native PDF has **7 pages**, 333,376 bytes, SHA-256 `98dfd9a5a9792edce676d61e7f872c7f29a2e9d401bb37fa0cf6b06bac8b4748`. The final engine log has no unresolved references or citations, duplicate labels, missing glyphs, or overfull/underfull boxes. The literal source scan finds 18 labels, 13 distinct referenced labels and two cited bibliography keys, all resolved. All seven pages were rendered and inspected without observed clipping or overlap; the bibliography-only final page remains intact.

The one retained engine warning is `Package epstopdf Warning: Shell escape feature is not enabled.` No EPS conversion is used; shell escape is deliberately disabled.

[Native companion report](diagnostics/v29-companion-native.json) records the exact scope. The [losslessly encoded evidence bundle](diagnostics/v29-companion-logs.json) contains the complete final engine log, complete latexmk transcript, auxiliary file, recorder file, PDF metadata and tool versions. Its decoder verifies every length and SHA-256 before writing, never executes decoded content, and refuses to overwrite files:

```sh
python3 diagnostics/unpack_native_logs_v29.py --output-dir /tmp/a2-v29-companion-evidence
```

The final engine-log SHA-256 is `b46ccd3b5193b29c7bfd8046fe4a69d16684e3921a8cda626b7bc16bb55b3314`; the complete driver-transcript SHA-256 is `cd0cea21d354600e51c0df3b6552676158c808761c3baeae9d433bbe2ea5d2f5`. The decoder was executed and all eight members verified. The PDF itself accompanies the separately delivered revision-evidence archive; it is not a PDF of the main article.

## 4. Limited changed-module fixture: executed, not the main article

A ten-page typesetting fixture includes the exact new hierarchy, the inherited single-offset inverse, the new equivariant-density extension and the revised orientation subsection. The entry explicitly identifies itself as a fixture. Its [entry recipe](diagnostics/v29-module-fixture-entry.txt) has a text suffix so it cannot be confused with a native entry point. The companion auxiliary file supplies its external companion links.

Two native `pdflatex` passes completed. All new v29 references resolve. There are no missing glyphs, duplicate-label diagnostics, or overfull/underfull boxes. All ten pages were rendered and inspected. The fixture deliberately retains **18 unresolved reference occurrences involving 17 inherited labels outside its input set**; their exact names are in [the fixture report](diagnostics/v29-fixture.json). They are not suppressed or replaced with fabricated theorem numbers.

Fixture PDF SHA-256: `fe5ea29be2b9ec8e96b7e91dcb64655b3288f5e24bae28dc1e19025b4593c0fb`. This output is not the full native `main.tex`, does not validate its full reference graph and does not close C2.

## 5. Hosted complete-native attempts: no build steps executed

The [recorded run observations](diagnostics/v29-hosted-runs.json) come from the authenticated GitHub Actions run/jobs endpoints.

| Run | Source | Job | Observed outcome |
|---|---|---|---|
| `34679614994` | `e468c075b0e57e015e774829f5886ce2322e6c02` | `103515663273` | completed/failure; `steps=[]`, `runner_id=0`, empty runner name |
| `34680067058` | `78852f2ccf828385fd45063c1b58c0d474ddf6c5` | `103516970408` | completed/failure; `steps=[]`, `runner_id=0`, empty runner name |

The second run started at `2026-09-12T07:11:17Z` and ended at `07:11:21Z`. No source-checkout, diagnostic or TeX step is recorded. This is not evidence of a TeX source failure, and the infrastructure cause has not been established. Trusted runner guards, branch protection, membership and permissions were not changed.

The bounded workflow `.github/workflows/a2-v29-native-build.yml` uses a full checkout, immutable source archive, normal/optimized checks, the complete source scanner and the complete native builder. It preserves logs and failures as artifacts when a runner executes it. A workflow definition is not an execution certificate.

## 6. Reproduce the outstanding complete-native check

From an authorized **full** checkout at the pinned mathematical source, run the following, using a fresh output directory outside the manuscript tree. The repository's complete builder compiles the companion before the main, retains all active auxiliary inputs and bibliography, and rejects unresolved references/citations, duplicate labels and missing glyphs.

```sh
git checkout --detach 78852f2ccf828385fd45063c1b58c0d474ddf6c5
P=papers/A2-v17-boundary-information-coarsening
OUT=/tmp/a2-v29-complete-native
mkdir -p "$OUT"
git rev-parse HEAD > "$OUT/source-commit.txt"
git archive HEAD "$P" .github/workflows/a2-v29-native-build.yml \
  | gzip -n > "$OUT/native-source.tar.gz"
python3 "$P/tools/check_revision_v29.py" > "$OUT/v29-normal.json"
python3 -O "$P/tools/check_revision_v29.py" > "$OUT/v29-optimized.json"
cmp "$OUT/v29-normal.json" "$OUT/v29-optimized.json"
python3 "$P/tools/check_preservation_v29.py" > "$OUT/preservation.json"
python3 "$P/tools/audit_native_sources_v27.py" --output "$OUT/native-graph.json"
python3 "$P/tools/build_submission.py" --output-dir "$OUT/native-build"
```

The required native tools are `latexmk`, `pdflatex`, and `pdfinfo`, with the packages in the workflow. Render and inspect every page of both resulting PDFs and retain source/product hashes and the complete logs. **A successful execution of the full-main part of this procedure, plus its full-PDF inspection, remains outstanding.** No abbreviated article or stubbed bibliography is offered in its place.
