# A1 English revision 9

## Sparse observation algebras and memory across exponent collisions

**Author:** Qian Qi. **Date:** 6 September 2026.

Complete English revision responding to the v8 report at `5f52bf456272b53bcb4df8d949effd2ab59bb79f`, based on submission `5d3d7e04b172f98bddfd037c488d93d516d20a98`. New branch: `revision/a1-english-v9-intrinsic-collision-geometry-2026-09-06`. Earlier manuscripts and reviews are unchanged.

The principal is `main.tex`, with the complete new proof in `sections/06b_collision_geometry.tex`. The intrinsic checkpoint and causal classification is the first named theorem of the introduction. All 34 v8 result labels and all 33 v8 proof blocks remain. The exact, affine, five-/seven-trial, decision and mechanical developments keep their complete proofs and separate assumptions.

The new invariant is the maximal Vandermonde product V(m,l) of l positive formal future exponents. The checkpoint profile is max_l (V(m,l)/M)^(2/l), truncated at the attainable past capacity. Its maximum over checkpoints is realized by one M-label causal filter for each known calibration and budget. Constants are uniform on compact subsets of the one-step exponent chamber, including additive sum collisions. A collision-tree rule gives pathwise phases. An intersecting two-parameter arrangement has peak ranks 9, 8 and 6 and arbitrarily separated transitions along tangent paths.

`RESPONSE_TO_REFEREE.md` answers E8.1–E8.3 and P8.1–P8.4. `PROOF_LEDGER.md` gives the new proof dependencies. `HISTORICAL_DERIVATION_MAP.md` records the derivations consulted. `REFERENCE_AUDIT.md` pins the primary sources checked.

## Reproduction and delivery status

Complete sources are committed directly, without a source-generating script. The automated publication script and proposed inherited-test rewrite were blocked by the tool and are not included. No fresh GitHub Actions success is claimed. The PDF and fresh local execution receipts are supplied in the accompanying standalone review archive.

Use Python 3 with SymPy and NumPy, and pdfLaTeX with AMS, Latin Modern, mathtools, geometry, microtype, booktabs and hyperref. From this principal directory run:

```sh
python3 tests/test_v7.py
python3 tests/test_v8.py
python3 tests/test_v9.py
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The inherited v8 suite requires the exact predecessor input at sibling `../A1-english-v7/sections/` for its final assertion. That input exists in the repository and is explicitly included in the standalone archive. All 256 assertions therefore execute in either delivered layout. The inherited v8 program itself is unchanged. The v9 preservation test uses packaged `validation/V8_PREDECESSOR.json` and checks all 34 result labels and all 33 proof hashes without sibling sources. Do not remove the packaged v7 input and count its conditional assertion as executed.

Local results: 97 inherited v7 checks, 256 inherited v8 checks and 642 new v9 checks passed; 45 PDF pages, no undefined references/citations or overfull boxes. `LOCAL_BUILD_REPORT.json` and the archive manifest distinguish local execution, source integrity and remote publication. Finite diagnostics are not analytic proofs, formal verification, independent referee approval or journal acceptance.
