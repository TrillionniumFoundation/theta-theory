# Build and read-only verification

Requirements: Python 3 with numpy and pypdf; pdflatex with amsart, geometry, lmodern, microtype and hyperref; pdfinfo and pdftotext. No network lookup occurs in the mathematical build. The source publication workflow installs its declared dependencies before the read-only build.

From this directory:

```sh
export PYTHONDONTWRITEBYTECODE=1
python verify.py
python regression.py > /tmp/r43-normal.json
python -O regression.py > /tmp/r43-optimized.json
cmp /tmp/r43-normal.json /tmp/r43-optimized.json
python native_build.py --output /tmp/r43-native --receipt /tmp/r43-native.json
python build.py --output /tmp/r43-complete --receipt /tmp/r43-complete.json
```

Published builds additionally pass the exact ordinary `--source-sha` and `--expected-tree` from the publication receipt. A local preflight without source SHA says uncommitted local preflight only. Native builds use two isolated ordinary-source copies, three pdflatex passes each, no shell escape, fixed SOURCE_DATE_EPOCH and an input recorder. Labels, citations, active source list, manifest hashes, overfull boxes and repeat PDF bytes are checked. Ordinary and optimized Python regression outputs must be identical; `require`, not removable assert, enforces validation.

The full builder first constructs the native article, then invokes the unchanged R38 builder with its pinned source and projection. It preserves the complete companion hierarchy. Output is outside ordinary mathematical source or in excluded artifacts/evidence directories. Byte hashes of inputs before/after independent reconstruction detect mutation. Normalized PDF text and raster comparisons distinguish same-source cross-engine equivalence from byte identity, which is not presumed across TeX versions.

The manifest excludes review_inputs (separately blob-pinned), artifacts/evidence, cache directories and itself from its per-file list; the ordinary Git-tree projection includes the manifest. Actual directory tree SHA, full source commit, artifact commit and final verification commit are different identities and are recorded separately. No finite check, TeX compilation or CI run replaces a continuum proof.
