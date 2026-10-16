# Validation — A2-DYN 112

## Actual local build

The complete `bash build.sh` run finished with exit status 0 on 14 October
2026. The active manuscript has **31 pages**. Three pdflatex passes
stabilized the references. The final audit found **zero unresolved
references, zero multiply-defined labels and zero overfull boxes**.

PDF: `manuscript/A2-DYN-v112.pdf`  
SHA-256: `69d73dba9130ff1c632090e44e79430215a72f4603abd2b01726c8024fb3fb75`

The 21 active manuscript/build/test files matched `SOURCE_MANIFEST.json`.
The original `model.tex` retains its exact v111 blob identity. Every
finite checker ran in both normal Python and `python3 -O`; its JSON outputs
were compared byte-for-byte and agreed. Assertions disabled by optimized
Python are not used as the sole test mechanism.

## Executed checks

The new `check_load.py` completed **36,372 finite checks**: 420 depth
coefficients, 180 balanced depth minima, 16,380 exact fractional-power
product cases, 15 exact Chernoff optimizations, 256 positive-source
identities, 19,116 strict-threshold boundary checks, two negative controls
and three explicitly labeled asymptotic classification illustrations.
The finite algebra uses exact rational arithmetic. The last three
illustrations use floating arithmetic and make no physical realizability
claim for their synthetic incidence patterns.

The inherited optical checker also passed: 56 optical, 1,016 marked,
108 localization and 4,096 positive-source cases. The inherited research
checker passed 10,922 marked-block, 1,641 witness and 702 depth-tail exact
cases, and 144 actual two-disk trajectory-pair diagnostics. The trajectory
diagnostics use floating-point Newton solutions; they are not exact
certificates of all physical trajectories.

The actual JSON outputs are preserved in `evidence/local-*.json`.

## Rendered inspection

All 31 pages were rendered at 80 dpi. Both whole-document contact sheets
(pages 1–16 and 17–31) were inspected. The new theorem pages 24, 25 and 26
were also inspected individually. No visible clipping, overlap or
malformed equation placement was observed in those inspections.
`evidence/visual-inspection.json` records this scope precisely; it does
not claim a line-by-line human inspection of every page.

## Exact source and remote qualification

`tools/check_source.py` verifies the original v111 manuscript tree,
the complete byte-identical `archive/v111` tree, the frozen controlling
report, the three historical pressure/optical anchors, and the additions-
only revision scope. It must be run on the committed revision, not on a
branch whose working files have not yet been committed.

The dedicated v112 workflow repeats this check and the build at its exact
checkout SHA, on both response and referee-copy branches. **No successful
v112 remote workflow is asserted by this local validation record.**
The separately observed successful v111 runs are recorded in
`provenance/v111-ci-observed-2026-10-14.json` without rewriting v111.

## Mathematical boundary

The checks validate finite algebra, source identity and assembly. They
do not independently prove the original physical pairing-space input,
uniform geometric pressure, every singular endpoint convention or the
complete low-load shortage. `eq:v112-remaining` and the organizing raw
pointwise LLT remain unproved; the publication flags say so explicitly.
