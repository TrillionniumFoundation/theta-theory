# Source index and audit boundary — A1 v13

All manuscript paths below are relative to `papers/A1-english-v13/` at **`fc6465b86fbc7ee6a4e8f3ccfb54ea32a64dc8b6`**. Line numbers refer to the committed UTF-8 sources, not generated relocation files. Named labels are the primary mathematical locators.

## Repository sources

| ID | Source and relevant ranges | Use in this review |
|---|---|---|
| S0 | `main.tex`, 1–84; `README.md`, 1–65 | Submission identity, input order, abstract, claimed scope; claims checked separately below. |
| S1 | `RESPONSE_TO_REFEREE.md`, especially 145–235; `PROOF_LEDGER.md`, 1–68 | Claimed mathematical response, preserved theorem chain, and what is not claimed. |
| S2 | `core/02_experiments.tex`, 1–111; `core/03_transversality.tex`, 1–202; `core/05_confluence.tex`, 117–180 | Positive experiment, physical basis, attainable tangent rank, strict confluent pairing. |
| S3 | `core/06b_collision_geometry.tex`, 11–354 and 381–558; `core/06a_attainable_filtration.tex`, 97–227 | Core flag, determinant volumes, global cover, causal classification, tree orders and intersecting-strata example; thin-rectangle proof. |
| S4 | `sections/construction_stability.tex`, 26–389 | Construction recurrence, paired-history stability, dominated-prior uniformity, common-advice upper realization. |
| S5 | `sections/uncertainty_geometry.tex`, 1–368 | Entire new consistency-class definition, joint theorem, tilt and overlap proofs, saturation and noisy intersections. Theorem `thm:sharp-common-moments` is Theorem 9.1, inspected on rendered page 38. |
| S6 | `sections/certified_resources.tex`, 96–235 and 348–426; `certified_compiler.py`, 171–253 | Two-sided radius, adaptive stopping, relation between covering and prediction profiles, actual adaptive entry points. |
| S7 | `sections/request_conformance.tex`, 1–83; `construction_contracts.py`, 1–282; `finite_compiler.py`, 1–120; `certified_compiler.py`, 1–117 and 171–253 | Bound request and frozen input, independent reconstruction, moment advice, actual runtime representation. Proposition 10.2 was inspected on rendered page 42. |
| S8 | `tests/test_v13.py`, 1–351; current `tests/test_v10.py`, `tests/test_v11.py`, `tests/test_v12.py` as executed | V13 fault/evidence design and all four suite reruns. Execution is not a claim that every author test was independently designed or reviewed line by line. |
| S9 | `sections/introduction.tex`; `sections/comparison.tex`, 1–93; `main.tex`, 60–83; `build.py`, 1–136; `validate.py`, 1–72 | Theorem hierarchy, selected literature comparisons, expanded-source preservation and build pipeline scope. |
| R | `reviews/a1-english-v12-certified-memory-2026-09-06/REFEREE_REPORT.md` at **`f2638b4910ee6245e9df4f641a2ed861bc4960b7`**, Sections 1–5 | Controlling prior objections. The prior manuscript SHA is `71907d83ba4eb235949e2a929b4b7f85349e96e5`. No claimed rerun of that report's original script. |
| X | This directory's `EXECUTION.json`, `INDEPENDENT_PROBES.json`, `reproduce_review.py` | New execution receipts and independent exact-rational diagnostic; neither author attestations nor a proof assistant. |

## Integrity and acquisition

Repository workflow run `34032338068`, artifact `9989053872` (`A1-v13-referee-ready`) supplied the complete v13 package. The archive SHA-256 was checked against the connector metadata:

`2e567e4267501d0ca6789e485f817656169b34a0b27940f002c32728419dd0dd`.

The GitHub-fetched manifest blob is `de4345eb94c864f2e102f4a013f95f1cfc5be1ab`. The artifact's manifest has that Git blob, and all 62 listed source-file SHA-256 values match. The fetched `main.tex` blob also matches the artifact: `50c7fe555fe98cfb74b2ebf9a8207789d7105f95`. Thus the workflow's earlier trigger SHA is not silently substituted for the reviewed submission: the source package is anchored to the published fc6465b commit through its manifest and main source.

The build checker additionally checks ten inherited core bodies against their pinned blobs and proof-block inventories against the supplied preservation manifests. That is not an independent historical audit of every old branch. All present source files were left unchanged; the rebuild was performed in a separate working copy.

## Selected public primary sources

**L1.** Y. Zhang and J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, arXiv:2311.05116, version 4. Lemma 2.18, PDF page 11, and its regularity context. The page was rendered and inspected. This supplies a coefficient-independent bounded-format input, not the manuscript's positive-history attainment theorem. Source: https://arxiv.org/pdf/2311.05116v4

**L2.** G. Comte and I. Halupczok, *Motivic Vitushkin invariants*, arXiv:2206.15412, version 2. Introduction, equations (4)–(5), recalling the real section-component variations and real metric-entropy inequality. The HTML equations were inspected. Only the recalled real inequality is used for this comparison, not the paper's new nonarchimedean theorem. Source: https://arxiv.org/html/2206.15412v2

**L3.** C. de Boor, *Divided Differences*, arXiv:math/0502036, version 1. Genocchi–Hermite formula (52), PDF page 19 / printed page 64. The page was rendered and inspected. This supports the repeated-node integral formula, not the model-specific uniform probability minorization. Source: https://arxiv.org/pdf/math/0502036

**L4.** N. Saldi, S. Yüksel and T. Linder, *On the Asymptotic Optimality of Finite Approximations to Markov Decision Processes with Borel Spaces*, arXiv:1503.02244, version 3. Section 5.1 and Theorem 5.2, PDF page 32 / printed page 32, rendered and inspected. It is the discounted-cost theorem with the stated Lipschitz/discount conditions. The earlier theorem-number objection is not renewed. Source: https://arxiv.org/pdf/1503.02244v3

These are targeted checks of mathematical inputs and citation scope. No exhaustive literature search, exact-priority refutation, or independent verification of every comparison in the manuscript is asserted.

## Execution boundary and reproduction

From the repository root:

```sh
python3 reviews/a1-english-v13-common-moment-2026-09-06/reproduce_review.py \
  --source-root papers/A1-english-v13 \
  --output /tmp/a1-v13-independent-probes.json

cd papers/A1-english-v13
python3 tests/test_v10.py /tmp/a1-v13-v10-rerun.json
python3 tests/test_v11.py /tmp/a1-v13-v11-rerun.json
python3 tests/test_v12.py /tmp/a1-v13-v12-rerun.json
python3 tests/test_v13.py /tmp/a1-v13-v13-rerun.json
# In a separate working copy, to avoid overwriting the submitted PDF:
python3 build.py
```

The four test commands and the separate build were executed in this review. The all-in-one `validate.py` was not executed because the downloaded artifact lacks adjacent historical directories and the original prior-referee script. This does not imply those files are absent from the repository.

The independent physical experiment uses N=3, T=2, two commands and four reports; all 64 complete paths are enumerated for each of four compatible models. It is not a continuum-command validation or a five-trial phase experiment. The fresh-query menu is the full ordered physical product basis at each checked prefix. Exact rational arithmetic, not floating-point agreement, decides the checks.

The PDF was rebuilt in three passes. All 68 extracted page texts match the submission; only manuscript pages 38 and 42 were visually inspected. The report's examination of retained appendices is restricted to the principal dependencies listed above. No statement here certifies every preserved proof.
