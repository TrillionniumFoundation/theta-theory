# Executable evidence for revision 14

Mathematical arguments are in the manuscript. The checks below are finite
arithmetic and source-preservation diagnostics, not proofs of all continuous
claims. `validate.py` reproduces this revision's own evidence without adjacent
historical source folders; `--prior-review` adds a separately scoped baseline
probe when the full repository is available.

## Reruns and new checks

The four unchanged author suites were executed locally against the unchanged
production compiler: v10 7,904, v11 8,207, v12 26,158, v13 12,944 assertions,
total 55,213. Exact JSON outputs are in `validation/V*_AUTHOR_RERUN.json`.
The current revision does not rename these as independently designed tests.

The new `tests/test_v14.py` executed 7,400 additional assertions, using exact
fractions and closed-form integrals of `t^a (log t)^k`. It imports neither a
production compiler nor an old test helper. The 21 cases combine seven
calibrations (both sides, shrinking gaps and the exact collision) with an
empty, constant-failure or nonconstant-failure history. In each case eleven
complete dual vectors are tested, including both signs of every coordinate
and a simultaneous all-coordinate displacement.

The diagnostics check exact confluent Newton reconstruction, monotone pivots,
exterior-volume comparisons, strict covariance Schur pivots, simultaneous
moment duality, normalized prior mass, a rigorous relative-envelope bound,
posterior-coordinate identities, all raw-coordinate shifts, exact-prefix
constraints and physical query values. The fifth raw/query direction is
exactly zero at the collision. Nonconstant histories detect that omitting the
prior normalization would fail mass one. These probes diagnose the new
mathematical construction; they do not allege a previously closed compiler
fault. The new report is `validation/V14_DIRECTIONAL_DIAGNOSTICS.json`.

Combined author-side diagnostic count: 62,613. It is not used as an argument
for mathematical significance or as a count of independently checked theorems.

## Independent-review baseline

The latest review's original script remains at
`reviews/a1-english-v13-common-moment-2026-09-06/reproduce_review.py`.
The optional repository validation command runs it on `papers/A1-english-v13`,
not on v14: its manifest deliberately pins the old submission. It writes a
separate `PRIOR_REVIEW_RERUN.json` and is counted separately in
`EXECUTION_REPORT.json` only when actually executed successfully. Its finite
physical setting is N=3, two acquisition commands, four reports and an M=64
floor-stop program, not continuum enumeration or the five-trial phase example.

## Source and build checks

The unmodified v13 artifact's 62 source hashes were checked before editing.
Every complete v13 named mathematical statement (77) and proof block (74)
is required to remain byte-identical by `build.py`; the complete expanded v14
has 80 named results and 77 proof blocks. The earlier v9--v12 checks remain.
The source manifest covers the current text, code and history records.
Three-pass compilation checks undefined references and overfull boxes.
`BUILD_REPORT.json`, `PRESERVATION_REPORT.json`, `SOURCE_MANIFEST.json` and
`validation/EXECUTION_REPORT.json` record distinct identities and outcomes.

The new continuum covariance lower bound and all-body inclusions are proved
in Section 6; they are not inferred from these 21 cases. No proof assistant,
unrestricted malicious-code verification, calibration-only lower bound,
infinite-horizon bound or optimal program-bit converse is claimed.
