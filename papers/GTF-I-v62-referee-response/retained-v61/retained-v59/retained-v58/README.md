# General Theta Foundations I — Revision 58

## Referee reading order

**Quantitative article:** `paper.pdf`, source `quantitative.tex`: *Stochastic Width of Compact Orbits and a Rational Exact–Noisy Separation*. It contains the least-orbit-dimension theorem, all-centroid width mechanism, legal density matrices, the explicit rational robust endpoint, and the uniform rational compiler.

**Structural article:** `STRUCTURAL_PAPER.pdf`, source `structural.tex`: *Clock Removal and Finite Physical Actions in Stochastic Realization*. It is an independent presentation of same-width stationarization, purification, finite physical quotients, boundary and phases, with algebraic and finite-group consequences. These structural theorems are inherited, not newly relabelled discoveries.

**Complete preservation edition:** `COMPLETE_REVISION.pdf`, source `main.tex`. It retains all active mathematical results from v57, including arithmetic/profinite refinements and the older existential higher-dimensional endpoint in an appendix. It is not required to supply missing proofs in either focused article.

Read `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, and the actual `evidence/BUILD_RECEIPT.json` for scope, theorem status and qualification. `evidence/THEOREM_LOCATIONS.json` gives compiled theorem numbers and pages. `evidence/REFEREE_PACKAGE.zip` includes all articles, retained documents and the native-only source archive.

## Exact rational compiler

```sh
python qubit_compiler.py --horizon 2 --amplitude 1/2 --max-labels 100 --output example.json
python qubit_compiler.py --horizon 2 --error 1/2 --max-labels 100 --output noisy.json
python check_revision.py
python -O check_revision.py
python build.py --check-isolated
```

The literal complex matrices and seed are in `EXPLICIT_INPUT.json`. A compiled example is generated in `evidence/COMPILED_EXAMPLE.json`. Optional SciPy proposes hull facets; **every row is independently verified using exact rational arithmetic**, and exhaustive triple enumeration is the fallback. SciPy is an accelerator, never a positivity or correctness oracle. A preallocation label limit prevents accidental large tables. The elementary polynomial algorithm can still be slow for large horizons; the tested example is horizon two, not an unreported large-scale benchmark.

The output is a classical hidden-label process with a numerical legal density-matrix decoder. It does not physically prepare a quantum state. The rational compiler does not compute a width minimizer or a spectral-gap constant. Its runtime is polynomial in the numerical horizon and inverse accuracy, not their binary encoding lengths.

## Provenance

Base: `0e07470b9693a2789af00222f063e715a83ff454`. Controlling r38: `5b2fb03f87a6b28bddcef51d498a0c78429bfa22`, report blob `c530ec0f755d2aa9a9d23b3d99dc4675fcacc679`.

All 181 native predecessor files are retained byte-identically. Earlier rendered manuscripts are provenance, not independent proof certificates. All separate analytic A/B/C/D completion flags remain false. No priority clearance or editorial acceptance is inferred from a successful build.
