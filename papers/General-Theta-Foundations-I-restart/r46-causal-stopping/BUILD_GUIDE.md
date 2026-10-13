# Build and validation guide

Native mathematical source is ordinary UTF-8 LaTeX. No encoded native manuscript or historical publisher is executed. `verify.py` checks the complete ordinary inventory, SHA-256/Git blobs, active inputs, citation and label targets, and paired mathematical environments. `regression.py` contains finite exact-algebra and numerical sanity checks, not continuum proofs.

Run:
```
python verify.py
python regression.py
python -O regression.py
python build.py --output /absolute/path/to/build-output
```

The native build makes two isolated source copies, three pdflatex passes each with `-no-shell-escape`, checks the final log and recorder, compares PDF bytes within the environment, and records source hashes before and after. Output is outside ordinary source. The SOURCE_DATE_EPOCH is 1791763200 (2026-10-12 UTC).

A `--prepared-root` may supply the verified complete retained source tree. With `--retained`, the complete R45 build chain is executed from those ordinary verified mathematical sources, including all its earlier complete companions. The native and full retained build scopes are explicitly distinguished in the receipt. Source export/recovery verifies fixed data hashes and only creates a temporary tree. It never runs `.github/scripts/*publish.py`, invokes a repository write, or changes old branches.

The read-only hosted workflow builds the same immutable source and exports its source/output receipt. A second clean reconstruction uses the downloaded remote input packet rather than a preexisting local build. Cross-environment byte equality is not assumed; PDF text/page/renders and within-environment bytes are checked separately. A failed or still-running hosted job must be reported as such.

Final evidence binds ordinary source commit, output receipt/artifact commit and final verification commit separately. Test and build success establish arithmetic/layout/provenance only, not theorem correctness or top-four significance.
