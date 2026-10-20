# Actual validation and execution scope

## Final frozen local source

The complete final source includes 63 core proof bodies, numbered 260–322, and 74 reachable native TeX files. All 59 inherited core bodies and model.tex/inputs.tex are byte-identical to the complete parent. SOURCE_MANIFEST.json fixes 123 mathematical and build input files, including the dedicated workflow mirror.

- Mathematical-source SHA-256: **cbe6dac9cab2bf80dd73119aaeda4d9f3122b42898807a4d0b6ac869eaecbc82**
- Source manifest SHA-256: **775943e1aa70d53e725956c8ab9eb01edb710c555b89cdcc5f1f9064d463f6c1**
- Final main.tex SHA-256: **73e0365b10bd86cda608c5b4e7853d4b4d3dd4595211f36defba8496e5d1b04c**
- Local execution interval: **2026-10-20T03:11:56.049198+00:00** to **2026-10-20T03:12:34.429481+00:00**
- Final main PDF SHA-256: **8eb1f67c250590ee5dc6c78994f710743ad5bf2f442c5071f7c0d60671235efb**

The mathematical-source digest is computed from the ordered path/hash list of root TeX, all core TeX, Python programs, pinned requirements and build.sh. The workflow mirror has its own entry in the manifest. The actual compiler recorder, rather than source-name inference alone, matches the declared native graph exactly.

## Completed local executions

| Scope | Actual completed result | Limit of the evidence |
|---|---|---|
| Complete parent reconstruction | Original 195-page main, three pdflatex passes; source check; all 26 retained programs in ordinary and optimized Python with pinned dependencies | Verifies the selected complete source is readable/buildable; does not mean the latest evidence carrier was its older CI checkout |
| Final immutable-source audit | 3,864 original files / 485,851,107 bytes; exact reconstructed article tree a1d21789f9d7c1be801ff4a54d1befad2a47340f; all 61 active inherited proof/model files; four older anchors; 91 reports; five compressed census inventories | No historical proof claim is strengthened by byte preservation |
| Final finite mathematics | **31 programs, 62 actual commands, all exit 0**; normal/optimized mathematical outputs agree | Exact rational/polynomial and stated diagnostic checks, not continuum certification |
| Final native typesetting | **211 pages**, three actual pdflatex passes and pdfinfo; 74 recorded native TeX inputs; no undefined citations/references, duplicate labels, overfull boxes or missing font characters | Layout and build reproducibility, not proof of the raw LLT |
| Rendered final-PDF inspection | **29 pages**: 1–5, 177–194, 206–211; five contact sheets and individual formula-page images; no clipping, overlap, missing glyphs or unresolved labels | Scoped visual QA; the other 182 pages were not visually re-inspected. Minor readable bibliography spacing is recorded. |
| Original historical assembly | **390 source files** checked, original assembler executed, six pdflatex passes plus two pdfinfo commands; **26-page main and 883-page supplement** | The old whole-repository gate was not executed; the original full source and build evidence are preserved |
| Branch inventory before publication | All **1,296** remote heads still exactly matched the initial snapshot; zero changed, removed or added refs | Publication of the new branch is recorded separately |
| Dedicated GitHub Actions run | Run **39424256218**, source **86c947eccea6029258d9a362624866a475118a66**, was **queued** in the latest recorded observation ending **2026-10-20 13:09:41 UTC**; job **118632668769** had no step summaries and the artifact list was empty | No remote command, checkout, build or success has been verified in that observation; the actual state is pinned in PUBLICATION_STATUS.json |

The new checks cover interval overlays and a counterexample outside the interval hypothesis; optical determinants, exact half counts and radius/conditioning factors; absolute variation and radial turning; true-fiber metric, endpoint assignment, capacity/pressure distinctions; and the all-mark critical-fan exponent and normalization. Formal rational optical test families are explicitly not presented as realized Lorentz trajectories.

The 320 checker and the second independent 322 checker include actual execution timestamps and the optimization flag. Only those two metadata fields are excluded when comparing ordinary and optimized mathematical JSON. Their raw outputs and original hashes are both retained. All other program comparisons are byte-identical; no mathematical failure is filtered from the comparison.

## Failed and intermediate executions retained

The initial baseline run used an environment without Sympy: 18 commands succeeded and **34 commands failed at import**. The source digest was identical in the complete pinned rerun, where all 52 commands succeeded. The audit reconstructs all 104 baseline command-log hashes and byte counts and identifies every initial failure as ModuleNotFoundError for sympy. There was no mathematical counterexample in those import failures. Dependency installation output and both complete runs remain available.

A preliminary 207-page native build through 321 also succeeded. It is preserved explicitly as an intermediate build and is not substituted for final verification through 322. Source-closure preparation found a duplicate equation/lemma label in 322; the final source uses distinct labels and the frozen checker passes. Initial internal reconstruction and auxiliary-run hashes retain the exact versions they read.

One initial local invocation of the new 319 diagnostic omitted the required destination after --details and exited with argparse status 2 before checks ran. It was corrected and the real successful invocations are retained; there is no invented per-command file for that tool-only invocation.

## Evidence and reproduction

[evidence/EVIDENCE_INDEX.json](evidence/EVIDENCE_INDEX.json) gives the path, size and SHA-256 of all **492 files** in five deterministic execution bundles and the hash of each bundle. All bundles were reopened and verified byte for byte. Actual receipts retain their real original working paths, command arguments, times, exit codes and log hashes. Uncompressed final source, mathematical, typesetting and historical summary JSON files are exact copies for convenient inspection.

Standalone PDFs are in [compiled/](compiled/). The published final PDF is the actual local build identified above. Earlier PDFs and any subsequently executed remote build have separately recorded identities; timestamps and the TeX environment can change PDF bytes without changing the mathematical source.

Install Python 3.12 and the exact requirements.txt dependencies, plus pdflatex, lmodern, the AMS/standard LaTeX packages and Poppler. From this directory, run:

    bash build.sh

Use a fresh checkout or fresh build output. For separately located fresh outputs, the equivalent explicit phases are:

    python3 -B tools/validate_revision.py all --output /absolute/fresh/current
    python3 -B tools/rebuild_preserved_history.py --output /absolute/fresh/history

The historical wrapper refuses an existing isolated-source target and never edits history/predecessor. The source checker requires the already frozen manifest during final execution. It is not regenerated as a way to accept unexpected source changes.

## Actual source publication and the evidence carrier

The new revision branch was actually pushed at source commit **86c947eccea6029258d9a362624866a475118a66**, whose parent is **6cdd9ae88cd358d524ecb89092361ac1522ba351**. Its root tree is **4624f0eef13e655c39d6313f6779e6c72a86870e** and its article tree is **6830d79a554645422869c3531715f1a32161ce20**. The exact mathematical/build bytes are those of the completed local executions; their immutable-source readback passes every frozen manifest entry.

The subsequent documentation/evidence carrier records that publication and the observed CI state. It fixes the prose-only manifest-filename/PDF substitution in the source-commit validation document, qualifies the response's intermediate-collision count for the separately handled one-hit case, and makes already-retained evidence paths explicit. No native TeX, mathematical program, build input, compiled PDF or historical file changes. The original audit and the two original source-commit explanatory documents are retained at [audit/post-publication-source/](audit/post-publication-source/).

The actual source-commit readback reports **4,369 additions, zero modified or deleted preexisting paths**. The subsequent full remote-head readback found **1,297 heads**: the new revision branch was the only addition, and all **1,296** earlier heads were unchanged. Those are observations of the published source; the carrier's commit identity supplies its own later evidence identity.

The complete API-returned run, source-commit and branch-ref observations, job summaries and artifact lists are retained in [audit/remote-publication/](audit/remote-publication/). The run was created by the actual push at **2026-10-20T12:41:42Z**. Its recorded queued state is an uncompleted remote verification, not a successful CI result. The service supplied no explanation for the queue in these readbacks. The already completed local mathematical and compiler executions retain their separate actual scope.

## Mathematical status

Modules 319–322 have complete native author proofs with their exact inherited hypotheses and internal reconstructions. No independent human expert reconstruction is claimed. The full original raw pointwise LLT, roofwise positive-source shortage and four-coordinate inverse consequence remain unclosed as stated in the proof ledger. Neither any finite program nor the local or remote build is a premise that proves those continuous estimates.
