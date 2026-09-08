# A1 English v23 — collision classification and saturated algebra geometry

*Attainable information geometry in positive experiments*, Qian Qi. Revision dated 7 September 2026.

This is the complete English revision responding to the v22 report at commit `325e89b9c012830cbd219fec0cff7c52b8e8d321`. Its manuscript basis is v22 at `5f745a863dac637496bd5eb20341f12cecb71ab1`. The new branch is `revision/a1-english-v23-collision-spine-saturated-proof-2026-09-07`.

## Reading route

`main.pdf` is the complete article, including all companion developments and alternative proofs. `main.tex` is its source entry point. The Introduction states the collision-uniform acquired-dimensional classification and now isolates its theorem-level contribution. The algebra section makes its finite observable quotient and immediate saturation explicit, defines all risk criteria locally, and gives a direct ellipsoid/acquisition/causal proof. The original transfer proof remains active in Appendix D. The direct nonlinear-filter quantization comparison is in Appendix G.

`RESPONSE_TO_REFEREE.md` maps every E22 request to the revised argument. `PROOF_LEDGER_V23.md`, `HISTORICAL_DERIVATION_MAP_V23.md` and `LITERATURE_VERIFICATION_V23.md` record the dependencies and the limits of the audit. No older revision directory or review report is changed by this revision.

## Reproduction from a repository checkout

Use Python 3 with SymPy (the tested dependency is SymPy 1.14.0), a standard TeX Live installation containing the AMS and article dependencies, and `pdfinfo`. Keep the sibling `A1-english-v20`, `A1-english-v21` and `A1-english-v22` directories: the build reconstructs inherited generated inputs from those pinned source chains in a temporary directory.

```sh
cd papers/A1-english-v23
python manifest.py
python build.py --prepare-only
python tests/verify_v23.py validation/V23_AUTHOR_RERUN.json
python validate.py
```

The manifest is verified rather than silently refreshed. `python manifest.py --write` is for intentional source revisions only. Full validation executes inherited diagnostics, the new exact tests, optimization and corruption controls, and the three-pass PDF build. The pinned v21 and v22 referee scripts are also rerun when present. The branch-scoped GitHub workflow can repeat the validation; it is not needed to materialize the readable sources now committed in this directory.

`PRESERVATION_REPORT.json` records full-block comparisons, not a theorem-correctness certificate. `BUILD_REPORT.json` records the actual PDF build. `validation/EXECUTION_REPORT.json` is written only after the complete author validation succeeds; a progress receipt alone is not completion. Any separately rerun referee script is identified as a rerun, not a fresh independent assessment.

The complete prior 129 formal statements, 127 proof blocks and 389 labels are required to remain in the active article. The new saturation proposition and direct proof clarify the second application's geometry; they do not change the hypotheses of the inherited theorem or purport to establish a publication decision.

## Publication and CI status

The initial workflow run `34097210136` failed before any step or runner was assigned. No GitHub-hosted test or build success is claimed for that attempt. Readable sources are therefore published directly through Git data commits; the complete author validation and pinned referee reruns were executed locally. The compiled PDF is supplied in the accompanying referee package and can be reproduced with `python build.py`. No v22 PDF is presented as the v23 PDF.

The compact `SOURCE_MANIFEST.json` is an exact delta against the pinned v22 manifest, not a sampling check: `manifest.py` expands it and verifies all 772 current source files. It can also read the full format. `validation/CI_STATUS_V23.json` records the actual failed attempt separately from the completed local execution receipts.
