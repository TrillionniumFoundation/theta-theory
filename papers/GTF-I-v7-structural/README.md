# General Theta Foundations I — seventh structural revision

**Author:** Qian Qi. **Date:** 22 September 2026.

The canonical article is **`paper.pdf`**, compiled from `main.tex`. It is a complete Volume-I argument, not an excerpt requiring an older principal edition. **`complete-development.pdf`**, compiled from `development.tex`, starts with exactly the same article and then preserves the earlier quantitative and foundational theorem bodies. It is the extended mathematical companion, not a second definition of the paper.

Controlling review: `review/general-theta-foundations-i-v6-markov-harsh-referee-2026-09-22`, commit `ff34427b2a5539ad23e2aea5cd57ce9f88d2b627`, report blob `14e052135fc188f51998aac81742e7cb0ef4e2c4`. Reviewed v6 snapshot: `f6f08bd529be23b7b97f5cc78829006c08e29e67`.

Working branch: `revision/general-theta-foundations-i-v7-structural-2026-09-22`. A separate `revision/general-theta-foundations-i-v7-structural-referee-ready-2026-09-22` is created after the published files are checked. The repository root index records the actual source, publication and final snapshot commits.

## Reading order

1. Sections 2–3 specify actual positive experiments, future-test quotients, attainable Bayes geometry, information loss, normalized response and implemented resource transformations.
2. Section 4 proves the abstract two-orientation predictive-tree theorem; Section 5 verifies it for Markov-renewal prediction and a continually observed infinite hidden shift.
3. Section 6 constructs a charged measure-valued approximation and verifies it in a nonlinear physical instrument without finite polynomial-moment closure.
4. Sections 7–8 prove the sharp finite-experiment cardinality theorem and its joint sample/register application to the actual A2 count protocol.

`RESPONSE_TO_REFEREE.md` follows the current report's numbered sections. `PROOF_LEDGER.md` records quantifiers and actual dependencies. `HISTORY_AUDIT.md` and its JSON manifest distinguish fresh consultation from preserved context. `LITERATURE_AUDIT.md` identifies the nearest primary sources and what was actually checked.

## Rebuild

From the repository root, with Python 3, `pdflatex`, and `pdfinfo` installed:

```sh
python3 papers/GTF-I-v7-structural/build.py
```

The TeX dependencies are the usual AMS/LaTeX packages, Latin Modern, `texlive-latex-extra`, and `texlive-science`. Python diagnostics use only the standard library. The builder checks the input hashes, preserves all inherited sources, runs diagnostics in normal and optimized modes, rejects deliberately incorrect variants, executes inherited diagnostics, and compiles both documents until their auxiliary state stabilizes. It checks all retained mathematical labels and equal numbering for the shared main article. No test is a substitute for the mathematical proofs.

For an isolated rebuild, unpack `evidence/COMPILED_SOURCES.zip` into an empty directory and run the same command there. The archive contains exact repository-relative inputs; no checkout or network access is required. Git provenance checks execute only inside an actual checkout with a supplied `GTF_SOURCE_SHA`. Compiler/container differences may change PDF bytes even when mathematical inputs and rendered pages agree.

## Resource convention

The default constrained resource is the number of data-dependent persistent register values. Current observations are update inputs, not free decoder-side inputs. All tree vertices, including unary vertices and the empty word, count. Programs, fixed real constants and transient computations are separate coordinates, explicitly unlimited unless an implementation gives a bound. The nonlinear measure-valued example supplies an exact rational transient implementation. A2's physical finite statistic is deterministic; jitter and reconstruction belong only to parameter-independent experiment-comparison kernels.

The article proves stated model theorems. It neither assigns a universal rate to all experiments nor declares an unrelated historical spectral, LDP, operator or phase claim established. Main and all predecessor branches and source editions are preserved.
