# General Theta Foundations I — Revision v21

## Multicut Continuation Complexity and Stable Causal Certification

Author: Qian Qi. Revision date: 24 September 2026.

Start with **paper.pdf**, **RESPONSE_TO_REFEREE.md**, and **evidence/THEOREM_LOCATIONS.json**. `main.tex` and its local inputs are the complete English article. `complete-development.pdf` appends the full frozen 400-page predecessor development. `evidence/BUILD_RECEIPT.json` records the executed build, source identity, page counts, and tests.

The controlling external report is the v20 round-five report at `14bcfe767940f8cbd196637049524d0b14eaee19`, reviewed source head `b488b2f28bec42a555999070759d715678b87db8`. This revision answers the principal structural objection by replacing unrestricted upstream histograms with an explicitly realized, bounded-state, finite-horizon training algorithm.

For a finite observation alphabet of size d, a compact behavior image B, fixed target Q, and strict expected-score threshold c, Theorem 7.2 proves

**κ_c ≤ W_c ≤ W_c^rat ≤ 12d κ_c.**

Here W charges the largest retained-state alphabet across the entire training, randomization, decision, and validation schedule; κ is the former decision-cut complexity. The clock and read-only descriptions are separate, explicitly priced resources. The theorem is not a sample-optimality assertion, and its long training schedule is not hidden. An autonomous clock conversion is given.

For the original positive-noise collision family, the new machine has three states at the decision cut and at most twelve states at every bit-acquisition or validation epoch. Its complete physical task satisfies **3 ≤ W_phys ≤ 12**. The exact integer peak optimum is not claimed. The previous 399-training-trial, 40,602-state construction is retained as a different preparation–memory regime. The twelve-state construction has an enormous finite preparation count; it is a mathematical resource comparison, not a practical replacement.

The article also proves compatible approximate continuation realization, finite-precision full-profile value bounds, cut refinement and simulator composition, a shared-capacity multicut residual obstruction, matching growth examples, and two confidence-level certification theorems with charged accumulators. The complete eleven-component historical dependency graph and its outstanding model obligations are preserved, not relabeled as solved.

## Reproduction

From a repository checkout with Python, the pinned requirements, and a LaTeX installation including amsart and lmodern:

```sh
python -m pip install -r papers/GTF-I-v21-multicut-resources/requirements.txt
python papers/GTF-I-v21-multicut-resources/build.py
```

The portable `evidence/SUBMISSION_SOURCES.zip` contains the same source and the required frozen predecessor PDF/inputs. Extract it and run `python GTF-I-v21-multicut-resources/build.py` from the extracted directory. No font files are distributed.

The build executes new and inherited diagnostics in ordinary and optimized Python, runs deliberate negative controls, compiles three LaTeX passes, rejects unresolved references and overfull boxes, and compares all 400 appended predecessor pages by extracted text and raster bytes. These are reproducibility checks, not independent certification of the analytic proofs or an acceptance assessment.

## Publication boundary

The new theorems have written proofs and reproducibility evidence. Independent mathematical review remains necessary. The original Norberg full text was not obtained; its proof-level novelty comparison remains explicitly incomplete. The exact physical peak between three and twelve, an optimal preparation–memory frontier, singular/many-particle extensions, and the general historical B4/C2 aggregates are not certified here. Their targets and original sources remain intact.
