# General Theta Foundations I — v18

**Continuation, Testing, and Microscopic Transport**  
Qian Qi · 23 September 2026 · Full English revision

The canonical article is `paper.pdf`, compiled from `main.tex` and local TeX inputs. `complete-development.pdf` places this article before the unchanged 256-page v17 complete development. The second volume preserves the inherited mathematical record, including results not needed on the present canonical proof chain; its historical introductions are not current proof-status declarations. No predecessor file is edited or removed.

The organizing result is Theorem `thm:v18-microscopic`: one explicit rational finite-reset audit certifies a positive private resource gap uniformly over a nontrivial family of genuinely changing two-sphere trajectories, while the same microscopic estimates give whole-process likelihood/posterior transport, a projected stochastic exponential, a bounded entropic backward equation, and stopping-value stability. Theorem `thm:v18-spine` states the overall architecture. Continuation covers and the exact erasure-cut spectrum supply the structural resource layer. The finite-reset game has a non-Dirac moment dual and a matching uniform sample-complexity lower bound.

## Reading order

- `RESPONSE_TO_REFEREE.md`: every E17-R3 and E17-P requirement, including what is not claimed resolved.
- `PROOF_LEDGER.md` and `PROOF_STATUS.json`: theorem-level statements, assumptions, proof credit and dependency identities; the build publishes `evidence/BOUND_PROOF_STATUS.json` with the exact source commit.
- `HISTORY_AUDIT.md`, `PIPELINE_GRAPH.json`, `PIPELINE_STATUS.md`: the eleven components, exact historical B4/C2 sources, and explicit supersession/proof-gap semantics.
- `LITERATURE_COMPARISON.md`: primary-source subtraction, including the positive-cone antecedent and the still-unverified Norberg original-text comparison.
- `PRESERVATION_MAP.json`: canonical relocation and complete historical retention.
- `evidence/BUILD_RECEIPT.json`: source-bound build, diagnostics and artifact hashes. It is not a mathematical certification.

## Reproduce

For the canonical article, extract `evidence/SUBMISSION_SOURCES.zip` and run `pdflatex main.tex` three times. All its TeX inputs are local; no historical directories are needed. For the full release from a repository checkout:

```sh
python -m pip install -r papers/GTF-I-v18-continuation-transport/requirements.txt
python papers/GTF-I-v18-continuation-transport/build.py
```

A Debian/Ubuntu TeX installation needs `texlive-latex-extra`, `texlive-fonts-recommended`, `lmodern`, and `poppler-utils`. The complete-source archive contains the pinned predecessor input closure and the new sources, but no font files. The inherited PDF is deliberately preserved, not silently rewritten to agree with present theorem-status dispositions.

## Scope that matters mathematically

The reset auditor has declared independent restart access and reads completed marked trials. It does not see a candidate probability law or its private state. Reset samples are conditionally independent for one fixed design; resampling the design is a different game. The physical model has two particles, one collision, positive observation noise and a common preparation; the microscopic flow itself changes with contact distance. The entropic backward theorem is bounded and scalar, with an observation-measurable terminal certainty equivalent. The main theorem is not a particle-number-uniform Boltzmann--Grad theorem or a proof of every historical C2 assertion. A2's primary geometric chain remains independent. The new C2 consumer uses the GTF theorem chain explicitly. External review of this revision is pending.
