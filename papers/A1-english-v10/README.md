# A1 English revision 10

## Sparse observation algebras and effective memory across exponent collisions

**Author:** Qian Qi. **Date:** 6 September 2026.

This complete English revision responds to the v9 review at `7a499e3cb32396b18eda869342ec8e9c70d8d028`, based on manuscript `e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5`. Branch: `revision/a1-english-v10-effective-finite-memory-2026-09-06`.

Start with `main.tex` and `RESPONSE_TO_REFEREE.md`. The principal new proofs are in `sections/effective.tex`; the isolated classical comparisons are in `sections/classical.tex`. All ten original v9 body sources are retained unchanged in `core/`, and all 42 predecessor named results and 40 complete proof blocks appear in the compiled paper. The exact, affine, five-/seven-trial, decision and mechanical results keep their separate hypotheses and complete proofs.

The new theorem compiles the collision-uniform sharp memory law into integer transition tables and dyadic outputs. At most M persistent labels are used; numerical precision is log2(M+1)+O(1), independent of the smallest additive gap. The finite read-only program is separately charged and may be much larger than the mutable state. The compact-state compiler is proved for general Lipschitz systems with finite evaluation data. Its monomial application verifies those data through finite prior moments and positive evidence.

## Build and diagnostics

Python 3 and pdfLaTeX with AMS, Latin Modern, mathtools, geometry, microtype, booktabs and hyperref are required. From this directory:

```sh
python3 tests/test_v10.py V10_DIAGNOSTICS.json
python3 build.py
```

`python3 build.py --prepare-only` performs source/hash/proof preservation checks and prepares the reordered includes without TeX. `build.py` otherwise runs three pdfLaTeX passes and fails on unresolved references/citations or overfull boxes. It moves existing proof blocks into the principal argument; all mathematical source is directly present in the repository. The complete expanded TeX is also emitted locally as `build/expanded.tex`.

`finite_compiler.py` is a reference implementation. Runtime `Machine` has only an index field. `Program` contains integer transitions and fixed-point outputs; the separately returned `Audit` is for offline diagnostics, not runtime memory. The explicit candidate limit prevents accidental exponential jobs. The fixtures use a coarse fixed input grid and exact rational moments; they are not numerical evidence for a continuum asymptotic rate.

Fresh local status: 7,904 finite assertions passed; all 42 predecessor named results and 40 complete proof blocks retained; 48-page PDF; three TeX passes with no undefined references/citations or overfull boxes. These are local executions, not GitHub Actions results. The older author suites and independent referee suite were not freshly rerun in this revision. No finite check or source-preservation receipt is a proof certificate, priority verdict or journal acceptance.

`PROOF_LEDGER.md` separates assumptions and resources. `HISTORICAL_DERIVATION_MAP.md` identifies the historical sources actually consulted. Earlier repository sources and reviews are unchanged. The accompanying standalone PDF and source archive are review artifacts; a new referee judgment remains outstanding.
