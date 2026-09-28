# General Theta Foundations I — Revision 59

## Referee entry

`paper.pdf` is the focused quantitative article, **Stochastic Width of Compact Orbits: Rational and Causal Realizations**. `STRUCTURAL_PAPER.pdf` is the independently complete **Finite Physical Actions and Repeatable Observation Processes**. `COMPLETE_REVISION.pdf` retains the full combined development. Neither focused paper requires the archival PDFs as a hidden proof premise.

The new structural result classifies bounded finite-label simulation of complete observation transcripts under adaptive control for repeatable compact-group experiments. At any fixed total-variation error below one, a finite future-response quotient is necessary and sufficient. Below one half its cardinality is the eventual minimum. The new quantitative result constructs rational/dyadic causal instruments with a whole-path error proof and gives an effective repeated-probe converse. The original terminal rational separation, cap theorem, clock removal, purification, phase/radius results and compilers are retained.

## Build

Run `python build.py --check-isolated` in a Python/TeX environment with SymPy 1.14.0 and PyMuPDF 1.26.7. SciPy 1.17.0 is an optional acceleration only; every proposed row is checked exactly and exhaustive triples are the fallback. The native archive is self-contained. `--local-missing-evidence` is a preflight-only mode and cannot qualify a publication.

## Generic rational inputs

`GENERIC_INPUT.json` supplies a nondefault rotation list, a rational unit seed and positive affine probes. All numeric values are integers or rational strings; floats are rejected. Rotations must lie exactly in SO(3). Probe probabilities must sum to one on the ball and have the specified positive floor. The CLI exposes two different error objects:

```sh
python qubit_compiler.py --input GENERIC_INPUT.json --horizon 2 --amplitude 1/2 --max-labels 100 --output terminal.json
python qubit_compiler.py --input GENERIC_INPUT.json --horizon 3 --process-error 1/2 --max-labels 100 --output process.json
```

`--error` means a terminal Frobenius tolerance, while `--process-error` means total variation of the complete classical adaptive transcript. The process model supplies nondisturbing fresh probes, not a procedure for measuring one unknown quantum state repeatedly. The public history is available to the control policy, not as an uncharged history input to the simulator. Allocation limits are checked before constructing tables.

## Evidence

`evidence/BUILD_RECEIPT.json`, `SOURCE_HASHES.json`, `THEOREM_LOCATIONS.json` and exact compiler examples record actual source-bound results. `FOCUSED_REVIEW_PACKAGE.zip` is the compact two-paper deliverable; `REFEREE_PACKAGE.zip` also includes archival PDFs. Both are committed artifacts, not only expiring Actions downloads.

A separate read-only workflow, `gtf-i-v59-final-head.yml`, runs on the exact final request commit, which is then pinned as the referee-ready head. Its external `FINAL_HEAD_ATTESTATION.json` is not written back into that same head. No signing identity, independent priority clearance, formal proof certificate, log-free terminal bound or whole-Theta analytic closure is asserted.
