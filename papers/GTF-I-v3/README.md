# General Theta Foundations I — third revision

**Title:** General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction  
**Author:** Qian Qi  
**Edition:** v3, 22 September 2026  
**Revision branch:** `revision/general-theta-foundations-i-v3-2026-09-22`

Read `paper.pdf` for the complete integrated manuscript, `RESPONSE_TO_REFEREE.md` for the response to every E1–E5 and M1–M7 objection, and `PROOF_LEDGER.md` for theorem dependencies. `HISTORY_AUDIT.md` identifies the full pipeline and stable source editions used. This is a revision for further referee assessment, not an acceptance certificate.

The new mathematical centre is a future-orbit quantization converse and a matching sharp causal-memory transition in an expanding regenerative experiment. An exact minimax nuisance quotient and a correlated, nonseparable contact theorem supply the second main development. All v2 quantitative proofs and the v1 foundations/boundaries are retained.

## Build

From the repository root:

```sh
python3 papers/GTF-I-v3/build.py
```

Required executables: Python 3, `pdflatex`, and `pdfinfo`. The Python scripts use only the standard library. TeX uses the same AMS/Latin Modern package set as the preceding edition. No network access is required once the repository sources are available.

The build deterministically materializes `retained-results.tex` from the unchanged mathematical suffix of `../GTF-I-v2/revision.tex`, and `references.tex` from the inherited bibliography additions and `new-references.tex`. Their expected hashes are fixed in the manifest. Existing generated files must agree byte for byte; the build does not silently overwrite a modified proof. The workflow publishes both generated native TeX files, the PDF, and the execution records on this revision branch only.

The source checkout commit and generated-product commit are distinct. `evidence/BUILD_RECEIPT.json` identifies the actual source checkout and PDF hash. `evidence/COMPILED_SOURCES.zip` contains the complete compilation inputs in repository-relative layout, including the inherited sources needed by the paper and diagnostic scripts. The archive is sufficient to rebuild the manuscript independently of moving branch names.

## Stable antecedents

The base is v2 referee-ready commit `75d8f3f8672ab78a844cc0a7a68808b46edf56f5`. The controlling referee report is at `01d3e78bd40985651f5b4ff24364e1dba5d481f0`. Complete pinned A1 v37 and A2 v112 source editions remain under `../GTF-I-v2/source-editions/`; the original foundational edition remains under `../GTF-I-v2/legacy/`. Main and all preceding review/revision branches are left unchanged.
