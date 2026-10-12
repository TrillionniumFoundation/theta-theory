# Build and evidence binding

Requirements: Python 3.11+; pypdf 5.9.0; numpy 2.3.5 for the full inherited regression chain; pdflatex with amsart/lmodern/microtype/hyperref and standard math packages; pdfinfo and pdftotext. The native regression itself uses the standard library only.

```
PYTHONDONTWRITEBYTECODE=1 python verify.py
PYTHONDONTWRITEBYTECODE=1 python regression.py
PYTHONDONTWRITEBYTECODE=1 python -O regression.py
PYTHONDONTWRITEBYTECODE=1 python native_build.py --source-sha FULL_SOURCE_SHA --expected-tree ORDINARY_PROJECTION_SHA
PYTHONDONTWRITEBYTECODE=1 python build.py --source-sha FULL_SOURCE_SHA --expected-tree ORDINARY_PROJECTION_SHA
```

Outputs and receipts default to `artifacts/` and `evidence/`, never to mathematical source files. For an independent extracted-source rebuild use `--output` and `--receipt` outside the downloaded tree, and verify its file hashes before and after. The native builder performs two isolated three-pass compilations, audits actual TeX recorder inputs, references and overfull boxes, and compares normal versus optimized regression output. The full builder recursively rebuilds all complete R34 and earlier companions without editing them.

SOURCE_MANIFEST.json records each ordinary file's SHA256 and Git blob SHA. Its full ordinary-text projection has a Git tree hash that excludes pinned review_inputs and artifacts/evidence; the actual native directory Git tree is separately recorded at publication. Source commit, artifact-only direct child and final evidence-only child have separate SHAs. A local preflight receipt has no remote source SHA until ordinary source is actually committed. No rebuild claim is made before a successful execution.

The source export includes the exact review input and canonical controls. Complete companion retention is not independent proof certification of every historical paper. Cross-environment PDF bytes may differ; compare normalized text and rendered pages without claiming byte identity unless verified.
