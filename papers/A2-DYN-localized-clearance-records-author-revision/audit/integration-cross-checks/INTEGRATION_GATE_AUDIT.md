# Read-only author integration and CI gate audit

## Conclusion

The current integrated manuscript passes the source/history identity checks and the complete native-closure check inspected here. The two initially identified corrections have been incorporated by the root author: the two analytical checkers now receive their actual CLI contract, and the general bounded-label translation statement in 332 now includes the coefficient supremum norm. No remaining deterministic configuration blocker was found in the requested build, validation, preservation, proof-index and workflow files.

This audit also independently re-read the actual current execution artifacts. All **74 mathematical command receipts** are present, have exit code zero, match their logged bytes and SHA256 values, and form exactly the set of **37 programs times normal/optimized Python**. All **65 normal/optimized comparisons** were recomputed from the actual output files: **61 are byte-identical**, and **4 compare identical mathematical JSON after removing exactly the two declared runtime fields**. The current native typeset receipt passes, belongs to the same mathematical source identity, records **255 pages**, and matches the actual PDF and auxiliary bytes. The proof index's **1,125 destinations** were independently read back from that actual PDF.

These are source, execution and document checks. They do not certify a continuous billiard proof, a strong spectral theorem, the raw pointwise local limit theorem, or four-coordinate inversion. No remote CI completion was inspected or asserted by this audit.

## Scope and snapshot identity

Audited article:

`papers/A2-DYN-localized-clearance-records-author-revision`

The inspection was read-only within the repository. It did not execute the writing build driver, alter any manuscript or program, alter a Git ref, or perform a remote write. Pure source-verifier calls, parser calls, receipt reads and actual-PDF reads were used. This report is the only file written for this follow-up audit, outside the article tree.

Current mathematical/build source identity from the actual driver:

`cecca59e06fc83d0e3bab89e41e347b6c831c50dd78e7603d63377ca4be4feb0`

Current frozen `SOURCE_MANIFEST.json` SHA256:

`5745a5abe9bb95de6dc64d53d28e018549c41f330b2895fb3382d9019bb8ae55`

The manifest contains **140 mathematical/build input files, 1,563,890 bytes**. The mathematical-source digest and the manifest-file digest are different kinds of identity; neither is presented as a new Git commit SHA.

| Audited current file | SHA256 |
|---|---|
| `build.sh` | `8ad4e8d1c19693e03d9c5877e70fc228a3361084d5ef6400a86114daf1f4e043` |
| `tools/validate_revision.py` | `3422075db9b0e4d6faeb829ce687b73cc7c5e89c8e1e095aed1ab9503689b10e` |
| `tools/check_source_preservation.py` | `f8296ae728d650f7a7c5083551b4e3746a88a39e41667eb8e726a1006edae228` |
| `tools/build_proof_index.py` | `b6b5aa0de0b4efe637be8c76c4d068d3583feaca4f70779810c3c1f2285e9266` |
| `tools/rebuild_preserved_history.py` | `aa46f9b3cfb0c69dac53a42495152d5055eca188cdb12e98921cc3152c72097a` |
| `tools/analytic_check_support.py` | `102c65d915223d1836bf3f7f9be761905361a457f67d9ccaa8067fba5f43a21b` |
| `tools/check_marked_weak_operator.py` | `d5541e2a41a83872378356e55dc86567a36cdab95ac46c2fd997b03eb9dcd602` |
| `core/332_endpoint_tested_marked_roof_operator.tex` | `618aaa348f7ebe40cc62a54f26a458ee9863194364b7c84a000046f79a86e16d` |
| `ci/a2-dyn-localized-clearance-records-20261021.yml` | `215f1252ead1b95955dfe772afd795ce7d5f4581cc0d66036b5d9ac55ead4b84` |

The corrected integrated332 and its checker supersede the earlier component handoff bytes for the current article. The earlier component packet, hashes and executions remain historical evidence; they are not relabeled as executions of these changed integrated files.

## Two corrections identified and closed

### Analytical checker CLI

The initial integrated driver put both new analytical programs in `DETAILS` and constructed `--details PATH` for them. Their shared parser defines `--details` as a Boolean `store_true` flag and `--output` as the path option. The initial command would therefore have exited with argparse status 2 and would not have produced the required `.details.json` files.

The current driver explicitly constructs:

```text
--details --output PATH
```

for `check_all_label_likelihood` and `check_marked_weak_operator`, while retaining the inherited contracts of the other programs. A read-only parser invocation verified both corrected argument lists and resolved the actual integrated article as their source root. The current 74-command artifacts then confirm that the corrected commands actually executed successfully. The checker/helper source contracts were not weakened to accommodate a wrong call.

### Arbitrary bounded label coefficients in 332

The original wording allowed any bounded coefficients but stated the unit-coefficient translation bound. The current `cor:wo-fourier` retains the generality and correctly states the bound with

`sup_l |c_l| * V_m^w(a,b,Psi) * |h|`.

Its proof now bounds the derivative norm by that same coefficient supremum before using the BV translation inequality. The integrated checker adds five exact coefficient examples and the explicit nonzero step-density regression showing why the missing factor fails. Hence the current 332 checker has **28,388** finite checks per run, rather than the earlier component's 28,382. Both current normal and optimized executions report 28,388. The correction is confined to that general coefficient statement; the unit-modulus mark characters in the weak operator already had the required normalization.

The root preserved the preceding manuscript/checker/driver bytes and correction identities under the article's `audit/integration-proof-correction/`. This audit did not edit those files.

## Program census and actual normal/optimized evidence

The actual `PROGRAMS` assignment was parsed, rather than inferred from a version number:

- 37 entries and 37 distinct names; every corresponding `tools/<name>.py` exists.
- Two jobs per program, yielding 74 intended jobs.
- `DETAILS` contains 28 programs.
- One stdout comparison per program plus one details comparison per details program yields `37+28=65` comparisons.

The current driver keeps the four inherited programs with an `--output PATH` contract in `OUTPUT_FLAG`. The geometry checker accepts `--details PATH`; the two analytical exceptions use the corrected Boolean/details-plus-output form. The additional explicit manuscript/source arguments for the inherited transversal-capacity, positive-fan and localization programs retain their actual source targets.

Actual evidence inspected:

`build/math-final-cli/mathematical-checks.json`

SHA256:

`41012a72a0ca2c18d8e3efbc7460dcbdabfddee160448cdb4cb45fd0d205d180`

The audit checked the exact tag set, each separate command receipt, each embedded receipt's equality to its file, exit code, mathematical-source digest, log byte count and log SHA256. It then recomputed every normal/optimized comparison from the two actual files, independently of the summary's stored `match` values.

| Actual check | Result |
|---|---:|
| Current command receipts verified | 74 |
| Nonzero command exits | 0 |
| Recomputed normal/optimized comparisons | 65 |
| Matching comparisons | 65 |
| Strict byte-identical comparisons | 61 |
| Mathematical JSON comparisons with the declared runtime exclusions | 4 |
| Missing programs, tags or comparison files | 0 |

The four JSON comparisons concern stdout and details for `check_all_offset_boundary` and `check_positive_critical_fans`. Only `executed_utc` and `optimized` are removed from each parsed JSON payload. All remaining mathematical data must agree. Therefore it would be inaccurate to describe all 65 comparisons as strict byte comparisons; the current driver appropriately distinguishes them.

The new analytical programs' current logs report 74,071 checks per 330–331 invocation and 28,388 checks per 332 invocation. They are finite auxiliary checks with explicit failure exceptions, not substitutes for the native continuous proofs.

## Source and historical identity gates

The current preservation verifier was actually invoked without an output-file option. Its optional-unfrozen mode was used while the author was completing the freeze; by the time the verifier reached the manifest, the current manifest existed and was fully checked. The returned manifest status was `passed`, not `not_frozen`.

The verifier confirmed:

| Identity or quantity | Verified value |
|---|---|
| Complete predecessor commit | `03d651b8709d28d90aa435fc12d608ad9c945e23` |
| Predecessor repository root tree | `d65973a6db0eb2c477359d10b43194cc5f99fa2f` |
| Predecessor article tree | `3010c90e2363dfe1808101a3e992eb02643c28f1` |
| Preserved predecessor files | 5,938 |
| Preserved predecessor bytes | 688,244,624 |
| Unchanged active inherited proof/model files | 69 |
| Current anchor SHA256 | `ca3d5e4d2204230a21e3e3e6ed8439d5b79484a38a98ff3ab8456db03394ae6c` |

The path/mode/blob map reconstructs the actual predecessor article tree. The actual archived path set must equal that map, and every file's bytes, SHA256, Git blob and mode are checked. The 69 inherited active files consist of the complete 260–326 core and the unchanged model/input files. The verifier recursively passed the unchanged 4d83 predecessor verifier and the earlier 6cdd verifier, preserving their respective identities and historical checks. The fresh current manuscript is not treated as an independently refereed extension merely because these identity gates pass.

The current frozen manifest checks exactly the mathematical/build input set: top-level native TeX, every active core, all Python tools, the paper-owned CI YAML, requirements and build entrypoint. It checks both identities and the declared native closure. Execution evidence and publication metadata are outside that mathematical manifest's stated scope; the complete eventual repository tree remains a separate publication identity.

## Complete current native closure and proof index

The reused native TeX parser is a literal input-graph checker, not a TeX interpreter. It rejects missing files, cycles, repeated active inputs, dynamic names, duplicate core numbers, gaps, unresolved labels and references, unresolved bibliography keys, and invalid document wrappers. It also requires the active core set to equal the actual files under `core/`. The current wrapper then requires the exact endpoints 260 and 332. Combined with the contiguous-range test, this enforces the full 73-core chain.

Actual current closure result:

- 84 reachable native TeX files.
- All 73 core files 260–332, each included once.
- 1,125 unique source labels.
- 807 distinct active references.
- No duplicate labels or unresolved references.
- Exactly one document class, one document start and one document end.

The actual compiler recorder is a second, independent closure gate. After three successful `pdflatex` passes, the driver compares the `.fls` input set with the declared native closure and fails on mismatch. It also fails on undefined references or citations, multiply defined labels, overfull boxes, missing font characters and TeX errors. The source identity is checked again after the selected phase, so a source mutation during the build cannot be silently accepted.

`build_proof_index.py` derives its label count from the current source, joins source labels bijectively to actual auxiliary records, and requires every compiled source label to have an actual named PDF destination. It separately enforces cores 260–332 and all new bodies 327–332. It does not import an earlier page total, label count or page-offset list. It validates the auxiliary absolute page count against the real PDF, and optionally against `pdfinfo`; the navigation preserves actual PDF page destinations separately from auxiliary page labels.

Current typeset and index artifacts inspected:

| Artifact | SHA256 |
|---|---|
| `build/typeset-final-norm/native-typeset.json` | `842be908f56ce30dea8a3bbf6a3759041ea72ae0f4a2268cc4b698def9f1af14` |
| Current actual `native/main.pdf` | `60b08184ad7bfa001aae76deb98d99062212cc647723a8e096485e89861df6f5` |
| Current actual `native/main.aux` | `a70b100d598e8757d2ac139760a30d0337a65a5e7070739081bc78371184c56e` |
| Current `PROOF_INDEX.json` | `fbf2a10aea9fab7c7b466c9104b855c7bfcb687cc5510b57710baadf25101734` |

The native receipt has the current mathematical source digest, status `passed`, 255 actual pages, matching compiler closure and no listed layout/reference problems. The audit verified all four typeset-command receipts/logs, the actual PDF and auxiliary hashes, every source hash in the proof index, and all 1,125 named destinations directly using the actual PDF reader. No source entry differs from the current file.

Earlier preflight artifacts were explicitly distinguished: two failed due to overfull boxes, and a subsequent 255-page preflight used the previous 332 wording. Their source digests differ from the current source, so none is used as evidence for the present build.

## Build entrypoint, history isolation and workflow mirror

`build.sh` passes `bash -n`, enables `set -euo pipefail`, changes to the article directory, disables Python bytecode writes, and calls the complete current source/math/typeset driver before the isolated historical reconstruction. The current driver records actual commands and requires their successful exit. It does not convert checker output or successful compilation into a mathematical proof certificate.

The historical wrapper's source path resolves to the actual preserved 390-file historical assembly. It copies that source to an isolated output directory before running the unchanged assembler and six native TeX passes. Its result explicitly states that the historical repository-wide gate is not executed. This is a native historical rebuild claim with its actual scope, not a claim that every old qualification or workflow has been rerun.

One local run prerequisite remains visible: `build/current-history/isolated-source` already exists in this working checkout. The historical wrapper intentionally refuses to overwrite an existing isolated source. Consequently, a literal local rerun of the fixed `build.sh` path must retain the prior attempt and use a fresh historical destination before that step. This is an intentional preservation guard and a workspace-state prerequisite, not a clean-checkout workflow defect. The audit did not delete, move or overwrite that existing evidence.

The paper-owned CI YAML and the root workflow mirror are byte-identical, with the SHA256 shown above. The workflow:

- Triggers on the specified new revision branch and the corresponding article/workflow paths, with manual dispatch also available.
- Uses the actual article working directory and a sparse checkout containing the article and workflows.
- Has read-only repository contents permission and does not retain checkout credentials.
- Records the actual checkout SHA, compares the mirror byte for byte with the frozen paper-owned YAML, and records the entrypoint hashes before building.
- Selects Python 3.12, installs the pinned requirement versions, installs the native TeX/PDF tooling, and records the actual tool versions.
- Uses shell `pipefail` while teeing `bash build.sh`, so a failed build is not hidden by successful log capture.
- Retains the actual build outcome and uploads current and historical execution artifacts even on failure.

The mirror comparison makes a changed root workflow fail against the frozen paper-owned copy. The paper-owned copy itself is part of the frozen mathematical/build manifest. No workflow declaration or local success is treated here as an already completed GitHub Actions run.

## Publication statement and remaining scope

The current local publication metadata still sets `full_raw_pointwise_llt_complete` and `four_coordinate_inversion_complete` to false. The source phase requires those flags to remain false for this revision. The current CI field was still `not_started` in the inspected metadata; this audit supplies no remote result with which to replace it.

The verified result is therefore a coherent, actually executed current author build and its source/history gates, with the full 73-core native mathematical architecture retained. Mathematical truth remains determined by the complete statements and proofs, their inherited dynamical hypotheses and the explicit unresolved closure obligations. The raw pointwise target, strong joint spectral/arithmetic evaluation, selected-event denominator problem and remaining inverse estimates are not discharged by these checks.

This is a follow-up integration audit. It is an addendum to the previously frozen analytic component packet, not a retroactive modification of that packet's manifest or old execution hashes.
