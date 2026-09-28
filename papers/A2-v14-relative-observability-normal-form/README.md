# A2 v14 — relative observability and the physical normal-form comparison

**Article:** *Nonlinear boundary laws and two-contact rigidity in dispersing billiards* — Qian Qi, 28 September 2026.

This is the full native-source revision responding to the v13 reports at
`a02d58d2b77e3337f001cf13676c5ff70e1ba97c` (28 September) and
`b3f0ad5843782c221651c9189fc156d20865cab1` (10 September).
The reviewed author source is `0e54099f079232df233316ae6fe7986fc51b7ea1`.
The September canonical branch alias was not a later manuscript revision.

## Manuscript

`main.tex` retains every previously active chapter and proof. It adds an
introductory overview and two active mathematical sections:

- `article/16_normal_form_comparison.tex`: analytic mixed-boundary estimate,
  exact physical projection, reference normalization, action limit, geometric
  identification of the half-line amplitudes, and the precise smooth increment.
- `article/31_regular_observability.tex`: regular rank and local observable
  quotient; exact-germ versus finite area normalization; a physical free-area
  construction; and joint area–jet recovery from `2M-1` positive two-flight windows.

The original independent even-contact inverse, equal-curvature case,
fixed-leading physical family, complete smooth profiles and charged acquisition
results remain active. No other manuscript or review directory is modified.
`history/v13-reviewed` is the exact reviewed native source tree, including its
historical verification and response documents. Those are not v14 evidence.

## Build and checks

From this directory in a Git checkout:

```sh
python3 tools/verify_v14.py
python3 -O tools/verify_v14.py
latexmk -pdf -interaction=nonstopmode -halt-on-error two_collision.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The checker uses only the Python standard library. `--algebra-only` deliberately
omits the full-source preservation check. `tools/build_v14.sh` captures command
logs, source identities and artifact hashes for a full local build. The narrow,
read-only workflow `.github/workflows/a2-v14-verify.yml` runs on this revision
branch; it cannot change source or push to the repository.

Read `RESPONSE_TO_REFEREES.md`, `PROOF_LEDGER.md`, `HISTORICAL_DERIVATION_AUDIT.md`,
`SOURCE_PINS.json`, and `VERIFICATION.json` for the exact scope and provenance.
Finite algebra, successful typesetting and journal-level mathematical review are
different forms of evidence. The actual GitHub run, not a historical `pass` field,
determines the status of the full build of a pushed source commit.
