# Actual validation and reproducibility — full physical source revision

This document describes the actual 19 October 2026 author-revision executions. The native proof bodies establish the asserted mathematical arguments. Finite programs, source hashes, compilation, visual inspection and CI verify their stated computational or publication facts; none is a certificate of the unrestricted raw pointwise local limit theorem or four-coordinate inversion. Both final-theorem completion flags remain false.

## Current release evidence

All paths below are relative to this complete article. The current release directory is `evidence/current-execution/full-physical-source-release/`.

| Check | Actual result | Authoritative record |
| --- | --- | --- |
| Latest complete baseline | All 2,088 files of `fdf2603c8bf422314f199fa431086485a0d1ebb5`, 215,569,322 bytes, match article tree `f5c90ecd279dd116330c5d90fa31cae2b0d6f61e`; the baseline was actually rebuilt to 164 pages | `audit/full-physical-source-20261019/source-census/BASELINE_LOCAL_REMOTE_BYTE_VERIFICATION.json` and its baseline-build receipt |
| Current mathematical execution | 23 programs, each in normal and optimized Python: all 46 actual commands passed; all 37 stdout/details comparisons are byte-identical | `PHASE_math.json`, `mathematical-checks.json` and every individual command/output in the release directory |
| Current native typesetting | Three actual pdfLaTeX passes and pdfinfo passed; 174 pages; no unresolved references, duplicate labels, missing glyphs or overfull boxes | `PHASE_typeset.json`, `native-typeset.json`, all four command receipts and logs in the release directory |
| Native proof navigation | 66 reachable TeX files, 56 complete core bodies 260–315, 811 source labels and actual PDF destinations; all 49 new labels checked | `PROOF_INDEX.json`, `delivery/PROOF_NAVIGATION.md` |
| Historical mathematical assembly | The unchanged assembler, six TeX passes and two pdfinfo commands all completed: 9 commands, 390 original source identities, 26-page main and 883-page supplement | `evidence/current-execution/historical-recovery/20261019T081533713628Z/REBUILD_RECEIPT.json` |
| Full inherited-file preservation | All 2,088 predecessor files and all three immutable anchors checked, with 74 exact original files at explicit historical-copy placements; canonical predecessor tree reconstructed | `HISTORY_PRESERVATION_AUDIT.md`, `history/PHYSICAL_TUBE_SOURCE_ANCHOR.json` and `audit/full-physical-source-20261019/mathematics/FINAL_AUTHOR_CONSISTENCY.md` |
| Final source/dependency gate | Exact current schema4 manifest membership, all immutable anchors, all original reports and the complete native dependency graph are checked after the documentary freeze | Release `source-checks.json` and `PHASE_source.json`; consult their actual result fields |
| Actual PDF visual inspection | All 174 pages inspected on six overview sheets; detail inspection of pages 1–2, 148–158 and 174 | Release `visual/RENDER_RECEIPT.json`, `visual/VISUAL_INSPECTION.json` and the actual twenty PNG files |

The final mathematical phase actually ran from **2026-10-19T08:21:11.832698+00:00** to **2026-10-19T08:21:46.603262+00:00**. The separately executed native typesetting phase ran from **2026-10-19T08:21:11.852640+00:00** to **2026-10-19T08:21:18.500734+00:00**. They have the same 101-file mathematical-source fingerprint:

    ebe48d08b94fc0dceecce96ecef8e0bc81d91918521ee1ba24558d549d558b26

This fingerprint covers exact root/core TeX and Python tools. Every current mathematical command receipt records it, and the driver compares source identities before and after execution. These local phases were deliberately recorded separately: no local `PHASE_all` is claimed for this release. The dedicated GitHub workflow runs the actual complete `all` phase, and its result is recorded only after the remote job and artifact are read.

The current delivered native PDF is the exact successful local output:

| Object | Bytes or scope | SHA-256 |
| --- | --- | --- |
| `delivery/A2-DYN-full-physical-source-author-revision.pdf` | 1,538,419 bytes; 174 pages | `cbf13c010cb2eff0ca1f8fa14a4753aa32c8418c0d75c00135c7db8f016c0de9` |
| `main.tex` | Full native manuscript entry point | `0653b9bfc530af09cea0316dd0b737c9c3cb8957c19a456d91c09a42e748be1d` |
| Actual release `main.aux` | Generated cross-reference information | `08953321181571d1b4f2f2a08e7d82dbec449ab19fff54bc22bdcb9d3c7c2b67` |
| `PROOF_INDEX.json` | Source/aux/PDF navigation map | `90b7ef080c76824d4bdb09bb9d6ae6af03c6d656027d60cf74f58dd000411c68` |

A later build can change PDF timestamps and therefore PDF bytes. Each actual execution's source/output receipt identifies that execution's own PDF; byte differences caused by rebuilding are not silently substituted into an older receipt.

## New mathematical verification and reconstruction

The only new mathematical program in this iteration is `tools/check_full_physical_source.py`, SHA-256

    5ce165494294167ac2215a798f621f4a1ab6e5f2cd396d0dcce7c76846f4a3ca

It supplements all 22 unchanged predecessor programs. Its eleven groups inspect the exact constants and exponents in modules 314 and 315: the physical margin tail and strict flux range; the unchanged incidence sum; finite-count roof exhaustion and weak-norm constants; strong-norm interpolation; full deep-source rates and collision normalization; exact floor/ceiling and central-index conventions; the original clock's negative compensating phase; the two actual same-orbit momentum-kernel bounds; the mixed weak tail and original conditioning factor; critical-disk and critical-band singular payments; and the singular roof and variation exponents. Every actual detailed output is retained. Analytic spike and marginal examples are expressly nonphysical negative controls, used to test an invalid inference, never presented as simulated Lorentz-gas evidence.

All gates use explicit exceptions and remain active under Python `-O`. The full driver requires successful return codes, expected output files and exact normal/optimized output equality. It does not manufacture command receipts from expected answers. The complete new proof bodies are six proofs in 314 and eight in 315, with source, theorem and equation locators in `PROOF_LEDGER.md`.

Independent author-side reconstruction is retained in:

- `audit/full-physical-source-20261019/mathematics/AUTHOR_PROOF_VALIDATION_FR_SM.md`;
- `audit/full-physical-source-20261019/mathematics/INDEPENDENT_RECONSTRUCTION.md`;
- `audit/full-physical-source-20261019/mathematics/FINAL_AUTHOR_CONSISTENCY.md`.

The final consistency audit actually reread all 46 command logs, 37 output pairs, all 101 fingerprint files and all 2,088 predecessor-preservation placements. It checked all 811 native definitions, 554 distinct referenced labels, all root-document native locators, and the new proof bodies. The document-format findings were corrected and are traced in release `FINAL_DOCUMENT_DISPOSITIONS.json`. This is an author-side audit, not an independent human referee reconstruction of every inherited dynamical input.

The mathematical conclusions retain their precise scope. Full-source weak roof regularity and the actual singular multiplier's uniform integrability are proved; the original deep exceptional source is controlled without a remaining positive margin in the stated norms. The regular-interior variation measure is finite uniformly before collision normalization, and its complete deep-source restriction has vanishing collision-normalized total variation. This does not assign a trace charge to singular pairings or remove roof spikes from an essential supremum. `MATHEMATICAL_AUDIT.md` records the original limiting target and its remaining minimal closure conditions.

The pressure research attempt is retained in `audit/full-physical-source-20261019/review-and-prior-ci/WHOLE_PRESSURE_CANDIDATE.tex`, with its independent reconstruction in the mathematics directory. The connected-rectangle lemma and renewal algebra are separated from unproved full physical singular-cell continuation and uniform distortion conversion. The candidate is not a native module 316 and is not a completed pressure theorem.

## Inherited programs and historical execution remain intact

All predecessor mathematical programs are retained and actually rerun: `check_finite`, `check_research`, `check_load`, `check_clearance`, `check_critical_coarea`, `check_two_mark`, `check_cross_flight`, `check_angular_source`, `check_uniform_growth`, `check_momentum_critical`, `check_radial_coarea`, `check_endpoint_localization`, `check_reflection_resolvent`, `check_physical_tubes`, `check_critical_clock`, `check_global_variational`, `check_sublevel`, `check_summable_source`, `verify_localization`, `check_critical_tube_volume`, `check_physical_source_height` and `check_explicit_optical`. Their older outputs, counterexamples and failed attempts remain preserved with their original identities and scope. Qualification scripts are not called completed mathematical manuscripts.

The historical 390-file mathematical source remains exact. The current historical output hashes are:

- 26-page main: `48b8848d0a750e0331ee158d2d2f5cb2f92124c1fd8986ede2b8cd077583190e`;
- 883-page supplement: `15c40ed07d80d4ef7fc19683f0f1956a2d586863aebf400b28ad677f6e16cdd2`.

An actual preliminary preservation check caught that rebuilding had overwritten tracked original historical build outputs. The failure log is retained. Every one of the thirteen original historical build files is now also preserved at an immutable historical-copy placement, and the three-anchor checker actually passed afterward. The initial 61-placement draft anchor and its helper are retained as preliminary artifacts; the final 74-placement anchor is fixed at SHA-256 `0e0570ca2a01aa274dd6e93e048a3a9db90539562d56d10c68405ee0ad6e3eff`. The older two immutable anchors were never reset. Normal verification cannot silently refreeze any inherited identity.

## Layout diagnostics and actual locations

The real preliminary 174-page native build failed its quality gate with a 2.79353pt title-page overfull box and a 15.01865pt introduction display overflow. Those logs remain under `full-physical-source-preliminary`. The title page received six additional points of space and the rate display was split across two rows. The final actual logs contain no overfull box, undefined reference or citation, duplicate label or missing glyph. Two retained AMS foreign-command advisories are explicitly recorded; they are not misreported as either absent or compilation failures.

The current new proofs appear in Sections 55 and 56, actual PDF pages 148–158. Their 49 labels have actual named destinations. The navigation builder also identifies the inherited one-page auxiliary-label offset for Theorem 52.4: its auxiliary label says 138 while its actual PDF heading is on page 139; navigation records the actual destination. The page map is generated from this PDF and does not presume inherited page numbers remain fixed.

## Distinct previous CI and present CI

The previous full author revision was actually tested by run **39187286448** at commit **8fbc6bd56bd9325600018f1aeb0cb2c2d0d8a4f2**. Its later metadata successor, the selected baseline **fdf2603c8bf422314f199fa431086485a0d1ebb5**, is distinct. This iteration reread the prior run, all eleven job steps, and artifact **12158866926**, then revalidated the retained exact 10,763,491-byte ZIP (SHA-256 `4b5c090e1a2ef608b48b08b4d0ffa648ffc34813243e597d4b85135464406406`). All 200 actual ZIP files, 1,408 frozen inputs, 98 native/tool identities, 44 mathematical commands, 35 paired outputs and its own 164/26/883-page builds matched. That prior success does not test 314–315.

The present dedicated workflow is `.github/workflows/a2-dyn-full-physical-source-20261019.yml`, with an exact copy under `ci/`. It checks out the actual new author commit, installs Python 3.11 and pinned dependencies, records environment and checkout identity, runs `bash build.sh`, and uploads actual current and historical outputs. A prepared workflow, a commit or a queued job is never called a successful run. `PUBLICATION_STATUS.json`, `PUBLICATION_RECEIPT.json` and `delivery/publication/full-physical-source-20261019/` record the actual post-push observations and any distinction between the tested head and a later metadata-only successor.

The independent artifact verifier is retained under `audit/full-physical-source-20261019/ci-verifier-preparation/`. It derives program counts, inputs, fingerprints and page requirements from the fixed tested source and final local receipts, requires the actual CI `PHASE_all`, checks every actual ZIP member and exact job-log bytes, and selects the historical receipt actually produced by that run. Its regression on the real previous ZIP, normal/optimized comparison, and rejection of a wrong head, wrong tree and altered job log are explicitly marked as verifier preparation; they are not present CI results.

## Reproduction

With the pinned Python dependencies and native TeX/Poppler installed, run from this article:

```bash
python3 -m pip install -r requirements.txt
bash build.sh
```

For separately recorded phases, use:

```bash
python3 tools/package_source_manifest.py . verify
python3 tools/validate_revision.py source --output build/current
python3 tools/validate_revision.py math --output build/current
python3 tools/validate_revision.py typeset --output build/current
python3 history/historical-v108/rebuild_history.py
```

The frozen source manifest includes native source, necessary helpers and retained audits. Its explicit exclusions are regenerable build/delivery/current-execution files, the manifest itself and mutable publication receipts. All excluded execution and delivery bytes are nevertheless supplied and covered by canonical remote transport inventories. The local runtime was Python 3.12.14; the actual remote runtime and package versions belong to its own environment log. Reproducibility, a favorable referee opinion, journal acceptance and completion of a continuous theorem are separate assertions; only assertions supported by the actual records are made here.
