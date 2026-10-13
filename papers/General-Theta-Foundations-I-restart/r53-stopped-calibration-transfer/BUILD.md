# Build and verification

Requirements: Python 3.11+, pdflatex, pdfinfo/pdftotext, pypdf, numpy; retained scripts may use scipy. Build outside the ordinary native directory.

```sh
python papers/General-Theta-Foundations-I-restart/r53-stopped-calibration-transfer/verify.py
python papers/General-Theta-Foundations-I-restart/r53-stopped-calibration-transfer/regression.py
python -O papers/General-Theta-Foundations-I-restart/r53-stopped-calibration-transfer/regression.py
python papers/General-Theta-Foundations-I-restart/r53-stopped-calibration-transfer/build.py --output /tmp/r53-build --retained --prepared-root . --source-sha FULL_SOURCE_COMMIT
```

Each native article is built twice in isolated copied directories, three LaTeX passes each. Actual recorder inputs, references/labels and manifests are checked. Normal and optimized regression outputs must agree. The complete R52 manuscript and its full retained chain are built, not merely linked. Inputs are hashed before and after. No old publishing script is executed. Prepared source exports contain no font files.

A source-bound run declares the exact immutable source commit; remote tree readback binds that declaration externally. Source commits, artifact commits and final verification commits are separate. Independent reconstruction downloads actual remote artifacts, checks their source binding, and rebuilds read-only. Cross-engine PDF bytes need not agree; any text/render comparison is reported with its exact scope rather than assumed.

Finite checks are exact arithmetic witnesses, not continuum proofs, exhaustive program synthesis or a journal decision.
