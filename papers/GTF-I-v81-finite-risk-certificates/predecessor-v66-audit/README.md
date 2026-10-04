# General Theta Foundations I — Revision 66

## Current manuscripts

**Quantitative:** *Reference-Stable Rational Instruments, Positive Streaming, and Spectral Space Bounds* — `quantitative.tex`, compiled as `paper.pdf`.

**Structural:** *Finite Physical Actions and a Strong Converse for Repeatable Observations* — `structural.tex`, compiled as `STRUCTURAL_PAPER.pdf`.

**Complete research edition:** `main.tex`, compiled as `COMPLETE_REVISION.pdf`. All 347 predecessor complete-edition labels remain active. Computational Sections 32–33 leave only the structural focused graph; their 16 prior labels remain in both quantitative and complete graphs and the relocation is explicitly checked.

## New results

Section `36-reference-instruments.tex` constructs genuine rational instruments from calibrated Choi grids, with exact positivity and joint trace preservation. For input dimension `d`, output dimension `n` and `m` outcomes it gives diamond error at most `6mn^2d^2(1+mn)/B`, an explicit integer denominator, and additive error under arbitrary common adaptive quantum testers, entangled references and bounded public stopping. It distinguishes a mathematical instrument description from a classical physical device acting on unknown quantum input.

Section `37-uniform-choi-streaming.tex` supplies a single numerical program with variable dimension and rational Choi data. It explicitly charges input length, denominator lengths, polynomial validation, temporary arithmetic and streaming storage. No rational Kraus factorization is required. Exact and fixed-state-grid modes preserve positivity, zero outcomes and the mass-weighted history estimate. Runtime/fair bits are expected; storage is worst-case on every rejection trial.

The stopped posterior proposition supplies an expectation bound `2 delta`, a tail bound `2 delta/eta`, and a pooled-event bound `2 delta/alpha`. It does not guarantee every rare normalized posterior. The scalar diagonal clarification corrects one suggested r42 warning without changing the need for positive matrix repair.

The inherited spectral lower theorems remain fixed-program, numerical-matrix theorems under full-action gap and cap assumptions. The new general upper construction supplies no blanket noisy transcript-only lower bound or disturbing-process finite-state classification, and does not close the v63 multiplicative crossover gap.

## Implementation and reproduction

    python choi_streaming.py compile --input inputs/rectangular-choi.json --grid 4096
    printf '8\n2\nxxxxxxxx\n' | python choi_streaming.py stream --input inputs/choi-channel-stream.json
    python check_choi.py
    python build_revision.py --isolated

The Choi compiler, validator and streamer use standard-library integer/reduced-rational arithmetic. Read `CHOI_INPUT_SCHEMA.md` for the tensor convention, zero-outcome format, precision parsing, exact sampling and runtime distinctions. The retained v65 instrument, v64 streamer and v63 exclusion suites are run unchanged in normal and optimized modes.

Build dependencies are pdflatex with AMS/Latin Modern packages, Python, PyMuPDF 1.26.7 and SymPy 1.14.0. `evidence/BUILD_RECEIPT.json` records actual results. The builder typesets all three articles, verifies proof-graph preservation and hashes, and reconstructs the native archive in an empty directory. The journal package has only the two focused proof graphs, response, PDFs and verifier; the research package also includes the complete edition and programs. Predecessor PDFs are not hidden compilation inputs.

## Remote ancestry and review

Base final v65 head: `34e5719ce5c7109c8c31f98079716b8ce6dcfffe`.
Controlling r42 report: `5c0796bc1f0ea24d379dfd28888f16d88315a525`.
Controlling proof/pipeline audit: `b5d71e67b879f9ada861993caedf8151734f85ba`.

Work branch: `revision/general-theta-foundations-i-v66-reference-stable-instruments-2026-09-29`.
Referee branch, created at the verified final head: `revision/general-theta-foundations-i-v66-referee-ready-2026-09-29`.

`RESPONSE_TO_REFEREE.md` answers all 14 required changes and 24 detailed comments. `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md` and `HISTORY_AND_PIPELINE_AUDIT.md` distinguish new proofs, inherited arguments, primary precedents and independent analytic obligations. All 85 predecessor native files remain unchanged at their existing repository paths. No independent priority clearance, author signature, journal decision or A/B/C/D completion is inferred from the new source and regression evidence.
