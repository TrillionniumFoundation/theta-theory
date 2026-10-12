# Rebuild guide

Use Python 3 with NumPy and pypdf, pdflatex (AMS/Latin Modern/microtype packages), and poppler's pdfinfo/pdftotext. Hosted receipt records exact versions. All shell calls disable TeX shell escape and all checks use explicit exceptions, including in optimized Python mode.

```
python verify.py
python regression.py
python -O regression.py
python native_build.py --output /tmp/r32-native --receipt /tmp/r32-native.json
python build.py --output /tmp/r32-full --receipt /tmp/r32-full.json
```

A local preflight with no `--source-sha` is not a published build. The published workflow passes the actual ordinary-source SHA and its verified projection using `--source-sha` and `--expected-tree`; it requires the exact pinned review input. The full build invokes the complete pinned R29 build (including corrected F and all older companions), then adds the new provenance cover to F and retains the complete R29 main as G. It does not modify historical sources. New native and cover builds are repeated in isolated directories; each TeX build has three passes. Normal and `-O` regression output must match exactly.

The source projection deliberately excludes generated evidence, artifacts and immutable review inputs; their Git identities are separately recorded. Source manifest, actual TeX recorder inputs, citations, labels and proof environments are verified. The full build records each delivery PDF's pages, bytes, hash and normalized text. Independent reconstruction must use an actual downloaded remote package and snapshot its input bytes before/after. All these checks establish delivery integrity, not continuum mathematical correctness.
