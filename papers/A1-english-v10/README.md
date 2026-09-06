# A1 English revision 10

## Sparse observation algebras: collision geometry and shared memory

Author: Qian Qi. Date: 6 September 2026.

This revision answers the v9 referee report at immutable commit `7a499e3cb32396b18eda869342ec8e9c70d8d028`, whose reviewed submission is `e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5`. The new branch is `revision/a1-english-v10-shared-memory-composition-2026-09-06` and descends from that review. No earlier manuscript or review is overwritten.

The principal is `main.tex`, compiled as `main.pdf`. Its dependency spine is the experiment, the persistent-memory task, attained transversality, complete Hermite flags, a global dimension-truncated cover, the intrinsic collision law, and the shared-memory composition and scheduling theorems. The full observation-algebra, affine, fixed-calibration streaming/control, five-/seven-trial, decision and mechanical proofs remain in the printed appendices. All 42 v9 named result labels and all 40 v9 proof blocks are retained. The principal has 53 result labels and 50 proof blocks; these numbers are inventories, not counts of independent new advances.

The additional central result is a sharp composition law for independent sparse experiments with heterogeneous detectors, priors, calibrations and horizons, observed under a deterministic schedule. The hidden parameter is a vector with a product prior. Future probes form the full tensor query menu. There is one shared M-valued persistent index, and the lower bound allows arbitrary joint encoding rather than assuming product codes. At each checkpoint the determinant volumes compose by a capped max-product convolution. Logarithmic inversion gives the sum of the component bit profiles, followed by the maximum over checkpoints. Serial schedules attain the largest individual peak; overlapping schedules can attain their sum. A two-exponent example changes the sharp memory exponent without adding a new collision parameter.

`RESPONSE_TO_REFEREE.md` addresses E9.1–E9.3 and P9.1–P9.4 individually. `PROOF_LEDGER.md` distinguishes the main composition assertion, its consequences and the explicitly credited classical results. `HISTORICAL_DERIVATION_MAP.md` records the sources actually consulted. `REFERENCE_AUDIT.md` states the literature comparison and its limits.

## Reproduction

Use Python 3 with SymPy and NumPy, and pdfLaTeX with AMS, Latin Modern, mathtools, geometry, microtype, booktabs and hyperref. The publication workflow pins SymPy 1.14.0 and NumPy 2.2.6. The standalone bundle includes the exact v9 inputs, the v7 sibling required by the unchanged inherited tests, and the source-pinned v9 reviewer program.

From the repository root or the same layout in the standalone bundle:

```sh
python3 papers/A1-english-v10/build.py --context standalone
```

The generator `scripts/materialize_a1_v10.py` checks each inherited Git blob, copies or relocates the full proofs, and writes only this new principal directory. Its templates are in `templates/`; the generated English sections are committed as ordinary readable source files. No generator is needed merely to read the manuscript or to compile its committed sources with three pdfLaTeX passes.

The build runs the inherited v7, v8 and v9 programs in a temporary copy, not by editing their assertions or writing over the original sources. It also runs `tests/test_v10.py`, reruns the unchanged referee code, compiles the principal, and checks for undefined references, duplicate labels and overfull boxes. The author's rerun of referee code is expressly not a new independent referee review.

Fresh receipts are separated by context in `validation/local/`, `validation/ci/`, or `validation/standalone/`. Each context has its own build report, execution logs and source manifest. `validation/PRESERVATION.json` records the 42 inherited labels and 40 proof hashes. A source-preservation receipt is not a mathematical certificate; finite diagnostics are not the continuum proofs; a successful build is not an originality or journal acceptance judgment.

The transducers may depend on known calibration and budget. Priors and finite horizons are fixed. Read-only exact-real codebooks are within the stated memory model; effective finite-precision synthesis is not assumed. The product prior and future-only query convention are explicit mathematical hypotheses, not implicit claims about arbitrary coupled hidden states or retrospective payoffs.
