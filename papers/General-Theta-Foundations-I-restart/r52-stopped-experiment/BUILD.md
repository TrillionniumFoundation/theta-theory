# Build and validation

From the repository root, with Python 3, NumPy/SciPy/mpmath/pypdf, TeX Live, Latin Modern and poppler:

```sh
python papers/General-Theta-Foundations-I-restart/r52-stopped-experiment/verify.py
python papers/General-Theta-Foundations-I-restart/r52-stopped-experiment/regression.py
python -O papers/General-Theta-Foundations-I-restart/r52-stopped-experiment/regression.py
python papers/General-Theta-Foundations-I-restart/r52-stopped-experiment/build.py \
  --prepared-root "$PWD" --retained --output /tmp/theta-r52-build
```

Use `--source-sha` only for a real immutable source commit whose byte projection has been verified. Native PDFs are built twice in isolated directories, each with three LaTeX passes. Input recorder, citations, labels, manifest, ordinary/optimized regressions, within-environment byte reproducibility and absence of undefined references/overfull boxes are checked. The retained invocation rebuilds the complete R51 chain, not every paper in the repository. Historical transport recovery is hash-pinned and never edits the original checkout.

The build writes only to an external output directory. Actual-download independent reconstruction must use the remote artifact's prepared-source package, verify its input hashes and source projection, and compare before/after snapshots. Different TeX releases may yield different PDF bytes; compare canonical text, page counts and specified-renderer pixels separately and report each outcome literally.

Generated table regeneration is explicit (`gaussian_certificate.py --write`); validation is read-only. No finite regression, build, hash or visual check substitutes for the written continuum proof or independent external mathematical review.
