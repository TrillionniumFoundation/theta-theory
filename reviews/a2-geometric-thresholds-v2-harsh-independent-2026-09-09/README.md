# A2 geometric-thresholds v2: independent referee package

Read [REFEREE_REPORT.md](REFEREE_REPORT.md) for the full assessment. The recommendation is rejection at the requested top-four-journal level in the present form, on the contribution demonstrated; no fatal in-scope theorem error is established. The previous concrete geometric, inverse-nonredundancy, and record-response objections are explicitly retired where addressed.

The source is frozen at `daeea828a7666acc42adcabdb9ab9057e9e1bac7`, on `revision/a2-geometric-thresholds-curvature-2026-09-09`. This package is added on a separate review branch. It is an AI-assisted referee-style assessment, not a journal decision.

`verification.json` pins the manuscript objects and records the independently executed checks and their limitations. `diagnostics.py` is self-contained apart from NumPy, SciPy, and SymPy; it imports no repository code, makes no network calls, and uses explicit checks instead of removable assertions.

```sh
python diagnostics.py > diagnostics_output.json
python -O diagnostics.py > diagnostics_output_optimized.json
cmp diagnostics_output.json diagnostics_output_optimized.json
```

Both executions passed 241 checks. The full output can be regenerated; its execution-environment hash is in `verification.json`. Floating-point byte identity with different numerical library versions is not guaranteed. Finite checks are corroboration, not a proof of arbitrary-length estimates or a simulation of the full equilibrium billiard. The author's build and verification suites were not replayed.
