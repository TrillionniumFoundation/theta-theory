# A2 v8 — canonical revision for independent mathematical review

**Article:** *Relative boundary laws and inverse experiments in dispersing billiards*  
**Author:** Qian Qi  
**Source date:** September 9, 2026  
**Branch:** `revision/a2-v8-relative-boundary-fixed-offset-2026-09-09`

The submission is `main.tex`, not any earlier introduction in the retained version directories. The independent fixed-window companion is `two_collision.tex`. The clean local build produces a **79-page article and a 7-page companion**. This is one canonical successor to the two reviewed v7s, not two competing revised introductions.

## Mathematical entry points

Theorem 1.1 and Section 6 present the smooth relative boundary law and its full nonlinear determinant/integration proofs. Section 7 exhibits nonlinear information at fixed leading data. Section 9 treats endpoint experiment comparison, including unequal contacts, heterogeneous products, and the supercritical projection argument. Sections 13–15 establish the exact four-window inverse, joint curvature/gap minimax order, and a separate reconstruction theorem with unknown smooth remainders. Full contact-jet, calibration, count lower-bound, record-response, and circular proofs are retained in the appendices.

The two principal referee comparisons are addressed by Theorems 13.2 and 14.2: curvature-only acquisition in the exact analytic family has order `epsilon^-6 log(1/eta)`, whereas simultaneous gap accuracy `delta` changes the optimal order to `(epsilon^-6 + delta^-2) log(1/eta)` in the specified bounded-flight, fixed-collar binary experiment. Theorem 15.1 does not give the estimator an exact higher-order probability formula.

## Read and reproduce

Read `RESPONSE_TO_REFEREES.md`, `PROOF_LEDGER.md`, `SOURCE_PINS.json`, and `VERIFICATION.json` alongside the article. `verification/build.json` records the actual local build, not remote CI. The proof ledger distinguishes written arguments from finite checks and from editorial judgment.

With Python 3, SymPy, SciPy, and a TeX installation providing `latexmk`, `pdflatex`, and the packages in `preamble.tex`, run from this directory:

```sh
python tools/verify_revision.py
python -O tools/verify_revision.py --output verification/diagnostics-optimized.json
python tools-v7/verify_revision.py --output verification/inherited-v7-diagnostics.json
python tools/build.py
```

The build uses an auxiliary-free temporary directory, compiles the companion first, resolves references, rejects unresolved LaTeX references and overfull boxes, and writes `main.pdf` and `two_collision.pdf`. PDF metadata time is fixed; identical bytes across different TeX installations are not promised. Full local PDFs, logs, and diagnostic outputs are also in the separately delivered revision packet. The Git branch stores the manuscript sources, provenance, reproducible checks, and build evidence; it does not depend on a pre-existing PDF to compile.

## Preservation

Every one of the **130 formal theorem/lemma/proposition/corollary/proof environments** in the critical v7 active manuscript remains byte-identical in the active v8 manuscript. The check reconstructs the old inclusion graph from `history/main-v7.tex`. Unchanged version directories are reused from their pinned Git trees, including the archived v5 introduction absent from the earlier delivery ZIP. The three distinct sharp-v7 chapters are retained by their original blob identities under `retained/sharp-v7/`; their stronger experiment and confidence statements are integrated into the active general formulation. Existing repository manuscripts and review branches are not overwritten.

The historical Fourier-inversion files retain their original hypotheses. No formal proof-assistant certification, exact numerical solver for nonlinear finite-offset probabilities, computationally efficient optimizer, remote CI success, or journal acceptance is asserted.
