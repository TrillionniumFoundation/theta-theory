# A1 — English revision 13

**Sparse observation algebras and certified memory across exponent collisions**  
Qian Qi · 6 September 2026

This directory contains the complete English manuscript and retained appendices,
not an addendum-only response. Build `main.tex` or run `python3 validate.py`.

The controlling v12 review is
`reviews/a1-english-v12-certified-memory-2026-09-06/` at
`f2638b4910ee6245e9df4f641a2ed861bc4960b7`. Its reviewed submission is
`71907d83ba4eb235949e2a929b4b7f85349e96e5`. The new branch is
`revision/a1-english-v13-referee-response-2026-09-06`. Original submission,
review, historical directories and branches are preserved.

## Reading and reproduction

Read `main.pdf` or `main.tex`, then `RESPONSE_TO_REFEREE.md`. The response maps
P12.1–P12.3 and E12.1–E12.3 to exact statements and executable evidence.
`PROOF_LEDGER.md` records dependencies and quantifiers;
`HISTORICAL_DERIVATION_MAP.md` identifies the actual source basis;
`NUMERICAL_EVIDENCE.md` states the finite domains and limitations.

```sh
python3 validate.py
# Source structure and preservation without a TeX build:
python3 build.py --prepare-only
```

The original adjacent v11/v12 directories are used only for historical fault
reproductions; they are included in the repository. A complete repository run
also executes the unchanged original v12 referee script. Offline source-only
packages without that separate review script report the omission explicitly
and still run the blob-pinned author reproduction.

## What is new

`sections/uncertainty_geometry.tex` proves a two-sided common-moment minimax law
`Xi_N(M,a)+delta^2` uniformly across all collision strata, with explicit interior
prior and numerical-name margins. It also proves the full anisotropic advice
saturation threshold and the three-phase noisy counterpart of the original
four-cell five-trial intersecting arrangement. The center model is not supplied
to the one common program. No calibration-only or boundary-name converse is
asserted. The original arbitrary fixed full-support-prior theorem is unchanged.

`ConstructionRequest` binds requested precision, horizon, stage/query schema,
rounding allowance and the complete frozen numerical name before synthesis.
Both adaptive compilers use that independent request. The running `Program`
and `Machine` remain unchanged. The common physical test constructs one program
per budget from one fixed table and executes it against four compatible models,
including exact collision and its two sides.

## Preservation and evidence

All 68 v12 complete proofs and 71 named results remain. Six additional proved
results give 74 proof blocks and 77 named results. Ten pinned inherited core
files, the v10/v11 tests and low-level compiler retain their bytes. The original
v12 test source is preserved; its direct inspector calls are ported to the new
explicit request interface without removing any of its 26,158 assertions.

The four author suites execute 55,213 assertions, with historical counterexample
reproductions separately recorded. The complete source manifest, preservation
report, three-pass TeX build report and exact JSON diagnostics identify the
actual deliverable. Hashes and tests are not formal proof certificates or
statements of acceptance at the requested journal level.
