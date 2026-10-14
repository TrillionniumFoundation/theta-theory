# Read-only R58 build

Requirements: Python 3 with NumPy, SciPy and pypdf; TeX Live with amsart, lmodern, microtype, geometry and hyperref; Poppler utilities. New finite checks use explicit exceptions and run identically with `python -O`.

```
python verify.py
python regression.py
python -O regression.py
python build.py --prepared-root /path/to/pinned-prepared-tree --retained --output /outside/source/output
```

`seal.py` is used only before the ordinary-source commit; build and verify never reseal. `build.py` verifies the exact retained R52 builder blob and changes only the new publication names and direct retained R57 input. The exact prepared R56 archive is reconstructed separately, all of its original bytes checked unchanged, and R57/R58 sources are overlaid additively. The full R56 review input remains byte pinned. The retained chain supplies all prior native manuscripts, not just their abstracts.

Each native and retained manuscript is built in two isolated workspaces with three LaTeX passes. Duplicate or undefined labels/citations, undeclared inputs and overfull boxes are fatal. Native normal/optimized finite output must agree. Builds use SOURCE_DATE_EPOCH=1791849600 and no shell escape. The final receipt records actual page counts, file hashes, engine versions, regression counts and source SHA supplied from the publishing checkout. A supplied SHA is externally read back before completion; a local preflight without one is explicitly uncommitted.

The first retained build was independently reconstructed from exact artifact 11863579443, not from the earlier R57 workflow's missing named artifact. After remote publication a fresh artifact download is independently rebuilt without source changes. Cross-engine byte identity is not presumed; normalized text, page counts and rendered pages are compared and differences reported. Verification adds only evidence and never modifies the mathematics or generated PDFs.
