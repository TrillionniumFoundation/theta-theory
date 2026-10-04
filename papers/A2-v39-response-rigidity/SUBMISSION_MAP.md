# A2 v39 submission and source map

## 1. The article to review

The sole primary is [main.tex](main.tex), Qian Qi,
_Scalar collision laws and recognition of periodic dispersing billiards_.
It compiles the complete new argument and every inherited proof.
The exact-source qualification produces `A2-v39-primary.pdf` and
the associated journal-source archive under `verification/current/`.
Generated files are execution evidence, separate from the committed
source manifest.

The revision responds to the v38 report at
`5dd7a7e346a9d31d7541efe791335d4e965cadb0`, which reviewed v38
author commit `a346669928e5147cf2c0ef86c3bc2a455b512d14`.
The source branch is `revision/a2-v39-response-rigidity-2026-10-04`;
the identical referee-copy alias is
`revision/a2-v39-referee-copy-2026-10-04`.

## 2. Main-body reading order

| Section | Question answered | Principal source |
|---|---|---|
| 1 | What is observed, controlled and charged? What are the exact and finite hypotheses? | `core/00_setting.tex`, `core/00h_single_law_overview.tex` |
| 2 | Can one unknown launch law and the table be recovered jointly? What is the complete ambiguity? | `core/19_single_law_rigidity.tex`, `core/19a_one_resolved_component.tex` |
| 3 | How is the new geometric inverse implemented with finitely many forward bits and rational controls? | `core/20_single_law_finite.tex` |
| 4 | What is the sharp stationary polynomial power for the retained fixed known disk law? | `core/16_sharp_stationary.tex`, `core/16a_shrinking_upper.tex` |
| 5 | Which operations are classical, and what do the different data models identify? | `core/05_comparison.tex` |

Theorem 2.3 is the direct single-law inverse with uniformly separated
angular density copies. Theorem 2.6 gives the broader exact
single-resolved-obstacle hypothesis. Theorem 3.3 gives finite periodic
geometric acquisition under quantitative uniform priors; Corollary
3.4 treats a complete finite nonperiodic cloud. Corollary 4.6 is the
retained fixed-known-disk minimax bracket. These statements have
different inputs, and their assumptions are not interchanged.

## 3. Appendices, all active

| Appendix | Subject | Source |
|---|---|---|
| A | Global occupation and exact translation periods | `core/14_global_response.tex` |
| B | Finite-stencil stopping inverse and pointwise sampling | `core/17_finite_stencil.tex` |
| C | Fixed stationary-jitter reconstruction | `core/09_stationary_jitter.tex` |
| D | Unknown homothetic footprint | `core/10_unknown_footprint.tex` |
| E | Rare pooled collision queries | `core/12_rare_stationary.tex` |
| F | Unknown homothety ratio and scalar calibration | `core/13_unknown_scale.tex` |
| G | Unregistered homothetic launch laws | `core/15_unregistered_footprints.tex` |
| H | General centered and isotropic commands | `core/18_isotropic_rigidity.tex` |
| I | Earlier stationary information bound | `core/11_stationary_information.tex` |
| J | Complete retained statements and resource summaries | `core/00a` through `core/00g`, reached through `core/00i_retained_summaries.tex` |
| K | Localized occupation queries | `core/01_local_queries.tex` |
| L | Adaptive boundary recovery | `core/02_adaptive_boundary.tex` |
| M | Finite binary control descriptions | `core/06_finite_precision.tex` |
| N | Period recognition | `core/03_period_recognition.tex` |
| O | Physical packing and transcript information | `core/04_information_bound.tex` |
| P | Quotient gauge and random stopping | `core/07_sequential_gauge.tex` |
| Q | Table-dependent bounded-error resolution converse | `core/08_calibration_resolution.tex` |

The primary reaches 34 TeX inputs, including 32 core files and
`references.tex`. No manuscript TeX file is inactive. All 265
reviewed labels and 66 reviewed proof bodies are present; the proof
bodies are byte-identical. The current totals are 322 labels, 76
proof environments and 79 formal blocks.

## 4. Files accompanying the article

| File | Purpose |
|---|---|
| [RESPONSE_TO_REFEREES.md](RESPONSE_TO_REFEREES.md) | All seven section 9 requests and the new response to the conceptual assessment |
| [PROOF_LEDGER.md](PROOF_LEDGER.md) | Exact and finite proof chains, dependencies, technical qualifications and preservation |
| [HISTORICAL_DERIVATION_AUDIT.md](HISTORICAL_DERIVATION_AUDIT.md) | Historical source identities and distinct observation models |
| [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md) | Verified primary references and the scope of attribution |
| [SOURCE_PINS.json](SOURCE_PINS.json) | Every current source hash, the active TeX closure, controlling review and preserved trees |
| [tools/verify_v39.py](tools/verify_v39.py) | 622,976 self-contained finite diagnostics |
| [tools/test_contract_v39.py](tools/test_contract_v39.py) | 66 qualification-contract tests |
| [tools/validate_v39.py](tools/validate_v39.py) | Source checks, diagnostics, primary build, receipt and source packaging |
| `.github/workflows/a2-v39-verify.yml` | Hosted execution bound to the triggering commit |

## 5. Reproducible qualification

In a clean checkout of the delivered commit, with Python 3, LaTeX,
`latexmk` and Poppler installed, run from the paper directory:

```sh
python3 tools/validate_v39.py --expected-head "$(git rev-parse HEAD)"
```

The command checks the actual checkout against the requested full
SHA and the committed source bytes. It verifies all manifest entries,
the recursive TeX closure, citations, labels, proof preservation and
the original historical Git trees. Both Python test programs run in
normal and optimized modes and must emit identical successful outputs.
The complete primary is then compiled; the final log must have no
unresolved reference, citation, warning, overfull or underfull finding.

The evidence directory contains:

- `receipt.json`: source SHA, exact-commit status, command outcomes,
  diagnostic summaries, manuscript counts and hashes;
- `source-pins.json`: the committed manifest bytes;
- `A2-v39-primary.pdf`: the compiled complete article;
- `A2-v39-journal-source.zip`: all 34 active TeX inputs with journal
  package paths;
- `A2-v39-repository-source.zip`: the full current source package,
  documentation, manifest and workflow with repository paths;
- `final-main.log` and `final-main.fls`: the final native build log
  and recorded inputs;
- command logs, and in hosted execution `artifact-binding.json`:
  the run identity and hashes binding the complete uploaded evidence.

The source archives are created before the build, and a receipt and
available logs are retained on failure. A successful workflow step
must also have an exact-commit successful receipt. The Actions
artifact name includes the source SHA and run attempt; its retention
is 30 days. The committed source and reproduction command remain
available after that artifact retention period.

For editing before a release, `--freeze-manifest` updates the manifest
after the source is finalized, and `--allow-dirty` checks those source
bytes without claiming an exact committed release. The publication
command above is the one that qualifies the delivered Git commit.
Finite checks and a build are reproducibility evidence; the continuum
proofs and their stated hypotheses remain the mathematical object
submitted for review.
