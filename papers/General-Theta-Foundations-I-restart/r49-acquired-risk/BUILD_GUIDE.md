# Build and audit

Requirements: Python3, NumPy, SciPy, pypdf, mpmath; pdflatex with amsart, lmodern, microtype and the complete retained LaTeX dependencies, plus poppler tools. Historical environment requirements are installed rather than changing old mathematics.

```
python verify.py
python regression.py
python -O regression.py
python build.py --output /absolute/outside/native
python build.py --retained --prepared-root /absolute/prepared --output /absolute/outside/full
```

Native mode runs ordinary/optimized checks, source/hash/label/citation/input audits and two isolated three-pass builds. Full mode invokes the unchanged R48 builder on a copied prepared tree; it in turn rebuilds the complete R46/predecessor chain. No old publisher is executed. Outputs remain outside ordinary source. Nested test totals are not summed as independent tests.

The remote workflow publishes ordinary source, then builds and commits artifacts. A separate reconstruction must use the actual newly downloaded remote prepared-source packet, with its binding manifest. Verify the source and artifact SHAs by GitHub readback; compare within-environment repeated PDF bytes, cross-environment normalized text/page counts, and renders where appropriate. Record any differences instead of claiming byte equality across TeX releases. Finally publish read-only evidence, then point new revision/referee-ready branches to it. A build/visual audit does not certify continuous proofs or mathematical priority.
