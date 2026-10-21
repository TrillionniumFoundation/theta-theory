# Actual validation and execution record

## Frozen mathematical source

The final local release was executed on the mathematical input digest

`52e7443237ebdcc1b2feb6a845c56ab0d87fb61312a781e13572371992bdb5c9`.

The frozen `SOURCE_MANIFEST.json` has SHA-256

`6a8672fb626e605fe9a93f64187421d953d5259cca3ecca5253cd8f11e42ba86`.

These are different explicitly defined identities: the first is the validation driver's current mathematical-input digest; the second hashes the full frozen 130-file manifest, including the dedicated CI mirror. Neither is a Git commit SHA or a mathematical proof certificate. The manifest has 67 native core files, 260–326, and 78 reachable TeX inputs. The active source has 1,031 unique labels and 733 references, all resolved.

The immediate predecessor's 4,393 files and 544,226,975 bytes reconstruct its original article tree `7bcaba2bc1ef7ab393c81a7df84f3e45983c4dfa`. Its 65 active proof/model files remain byte-identical. The inherited preservation gates and complete current-ref applicability audit also passed.

## Actual local release entrypoint

The actual command was `bash build.sh` with the recorded Python 3.12 environment active. The current `all` phase ran from **2026-10-21 00:56:39 UTC** to **00:57:23 UTC**. Its source, mathematics and native typesetting phases all passed. The historical rebuild ran from **00:57:23 UTC** to **00:57:57 UTC**, with exit code zero. Exact subsecond times, commands and process results are in the receipts; these rounded times are a reading aid.

The environment was Python **3.12.14**, with the pinned NumPy **2.3.5**, SymPy **1.14.0**, SciPy **1.17.0** and mpmath **1.3.0**. The actual environment command outputs, TeX version and Poppler version are preserved in `evidence/current-execution/release/LOCAL_ENVIRONMENT.json`.

### Mathematical programs

All **34 programs** were actually executed in ordinary and optimized Python: **68 successful commands**. All **59 normal/optimized stdout or mathematical-JSON comparisons** matched. Runtime timestamps and flags are compared separately where an inherited checker explicitly includes them; actual execution records are never replaced with deterministic fictional timestamps.

The three new programs each succeeded in both modes:

| Program | Exact auxiliary checks per execution | Scope |
|---|---:|---|
| `check_complete_roof_variation.py` | 10,148 | Exact cofactor/scaling identities, rational Hessian cases, physical critical profiles, endpoint and normalization budgets, BV-height and selector-scope counterexamples |
| `check_canonical_collision_boundaries.py` | 34 | Canonical optical conjugacy, two-half determinants, terminal incidence and endpoint identities, original rectangle mass/cap, jump/Fourier/depth constants |
| `check_326_boundary_pressure.py` | 1,251 | Exact polynomial matrix identities, rational coefficient rectangles, geometric depth sums and original homogeneity-tail majorants |

The rational coefficient cases are not claimed to be independently realizable billiard trajectories. The continuous first-hit coverage, all-word source assignment, singular endpoint exhaustion and original-order limits are proved in the native mathematical text and reconstructed internally. A large finite check count does not prove them.

The original 31 mathematical programs were also retained and executed. Their original scopes remain; local samples and finite optical diagnostics are not promoted into a global dynamical theorem.

### Current native manuscript

Three actual `pdflatex` passes succeeded. The compiler recorder contains exactly the declared **78** native TeX inputs. The result has **233 pages**, with no undefined references or citations, duplicate labels, missing characters, TeX errors or overfull boxes. The inherited `amsmath` foreign-command advisories remain recorded and do not hide any failed diagnostic.

The local release PDF is `compiled/A2-DYN-complete-author-manuscript.pdf`, **1,870,750 bytes**, SHA-256

`52ed3bfe006b31ae404c0ff54ffa432a221bfa97484bb003cf30aefa01251528`.

New complete native sections are 67–70. The central results are Theorem 67.4 (complete roof BV/height, page 198), Theorems 68.2 and 68.6 (canonical sources and charges, pages 201 and 205), Theorem 69.2 and Corollary 69.3 (exact records and Fourier bound, pages 208–209), and Theorem 70.4 with Corollary 70.5 (full word pressure and completed geometric input, pages 213–215). The current dependency notes are on pages 231–232.

The final PDF was also rendered and visually inspected: every page in six overview contact sheets, and pages 1–6, 194–215 and 231–233 at higher resolution. No missing pages, clipped text, formula overlap or illegible glyphs were observed in that scope. The historical documents were sampled at their first and last pages. The actual render commands, image hashes, inspected images and scope are preserved in `audit/pdf-visual-qa/`. Theorem 67.4 starts on actual PDF page 198; this corrects the auxiliary-label page 197 without modifying the frozen mathematical source.

### Preserved historical mathematics

The original **390-source** assembler was actually run in an isolated copy, followed by six actual LaTeX passes. The rebuilt historical main has **26 pages** and the technical supplement **883 pages**. Their SHA-256 values are respectively

- `e54610c05e0d81a2491f2cf5c965a57658fae8f7b07d6c7fb23eb56ee0400602`;
- `369dba79746fe3204ec11f49244f61e49c6c0f1fa29914d418edaa74e7fe3116`.

They are supplied in `compiled/`. The original archive is not edited by this rebuild. The historical repository-wide gate was **not** executed; the receipt explicitly records that distinction. These are actual source assembly and document builds, not a claim that every historical dynamical theorem was newly independently certified.

## Preliminary work retained

The first integrated native compile produced a 232-page PDF but failed the layout gate on two overfull displays. Its logs, PDF, exact source identity and changed-source snapshots remain under `evidence/current-execution/pre-freeze/`. Only display alignment and line breaks were corrected, with a preserved diff and hash map. The corrected 233-page three-pass build succeeded in `layout-confirmation/`, before the frozen release entrypoint above.

The independent auxiliary integration through 325, its 226-page PDF, original checker versions and actual normal/optimized receipts are preserved separately in the canonical-boundary audit archive. They are not represented as builds of the complete 326 manuscript. The pressure research archive similarly preserves each preliminary source, proof-scope correction and actual execution, including the observed initial dependency failure.

## Remote CI and publication

The previous complete article's successful run at `86c947eccea6029258d9a362624866a475118a66` was freshly re-read under `audit/prior-ci-readback/`. That predecessor execution remains separate from this revision.

The complete new source was published as **`6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9`**, root `ad34fd91ad2f1c6e594d3bbe437417aba524bf87`, article `4f41b3a98487a1ae0507d40390aca030c5520e19`, on `revision/a2-dyn-physical-roof-variation-2026-10-21`. All 5,261 source additions were confined to the new article and its dedicated workflow. Independent readback verified all **130** frozen file modes, Git blobs and SHA-256 values, the 78-file native TeX closure, workflow mirror and 129-file driver digest. The earlier local release executed these same frozen bytes before publication.

The actual [new remote run **39526895726**, attempt 1](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/39526895726) **succeeded** at exactly `6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9`. Job **118983561729** ran from **2026-10-21T01:39:52Z** to **01:44:23Z**; all **11 steps** succeeded. The artifact's checkout receipt independently records the same source SHA and a successful build. No source/workflow repair or manual rerun was required.

Artifact **12314306857** was actually downloaded: **10,808,391 bytes**, **225 file members**, SHA-256

`e83672d52e5e90b9f256d31c316a8a1f7ec17dd0da0b9f7ddf5e5d605278c475`.

All ZIP member CRCs and extracted bytes were verified. The independent artifact readback completed **1,333 receipt/byte/identity consistency checks**. These are readback checks, not 1,333 extra mathematical executions. The actual remote execution comprises **68 mathematical commands**, **59** matching normal/optimized comparisons, three native LaTeX passes, the **233-page** native document with **78** actual TeX inputs, and the **390-source** historical assembly with **26-/883-page** PDFs. Every recorded command exit, source digest, actual log hash, comparison and declared compiler-input closure was reconstructed. The historical repository-wide gate remains explicitly unexecuted.

The actual remote native PDF has SHA-256

`6b8714ff679ade78593da4b63244a5c6ca906d81b38bf40334c8e9a30e1d4239`.

It is retained separately in `audit/current-ci-success-readback/artifact/current/native/main.pdf`. The local release PDF and its distinct hash above remain preserved. Neither PDF is substituted for the other execution's output.

The decoded job log is retained with narrowly identified authentication-header-reference lines removed. `JOB_LOG_RETRIEVAL.json` preserves its raw decoded-content hash, saved-content hash, exact redaction line list and reason. No credential or temporary signed download URL is stored. Mathematical and compilation logs from the artifact are retained exactly.

The first **readback-verifier** attempt expected a generated untracked build directory; the actual post-run status was empty, a clean checkout. That attempt, its script and output remain preserved. Only this readback predicate was corrected to accept clean status or the sole declared generated directory; the exact diff and successful subsequent execution are retained. This was not a CI, manuscript or mathematical-program failure, and no source repair or CI rerun was performed.

At the earlier observation `2026-10-21T01:37:28.119Z`, the run was still queued with no runner, steps or artifacts. That real snapshot is preserved in `audit/current-ci-readback/` and the pending evidence carrier `d46ba004ff1ac8d44dab04549daff7e3c0e5f205`. The later success is added under **`audit/current-ci-success-readback/`**; it does not rewrite the earlier observation. The source-stage metadata remains under `audit/remote-publication/source-release/`, and the complete pending-carrier metadata remains under `audit/remote-publication/pending-carrier/`.

This later evidence-only carrier preserves every frozen mathematical/build input and the workflow. Its `[skip ci]` commit records the actual successful source run, not a new mathematical test target. `PUBLICATION_STATUS.json` records source, local release, actual tested checkout, pending history and verified artifact as distinct identities.

## Mathematical status

The current source contains complete author proofs of the new physical-roof, canonical-source, exact-record and full physical-word pressure theorems. The original normalized same-roof shortage and remaining joint spectral/arithmetic/conditional interfaces are explicitly unclosed. Neither the raw pointwise local limit nor the full four-coordinate inverse is claimed complete. Internal author reconstruction, finite computations, source preservation, document compilation and CI have separate evidentiary roles.
