# Build and audit

Requirements: Python 3, NumPy, PyMuPDF, a pdflatex distribution with amsart, lmodern, microtype and cm-super. Historical companions additionally require the inherited LaTeX packages. Install system fonts/packages rather than editing old mathematics to hide environment failures.

```
python verify.py
python regression.py
python -O regression.py
python build.py --output /absolute/outside/native
python build.py --retained --prepared-root /absolute/prepared --output /absolute/outside/full
```

The build runs ordinary and optimized finite checks, source/hash/label/citation/input checks, two isolated three-pass native builds, byte comparison and undefined-reference/overfull detection. Full mode calls the unchanged R46 retained builder on isolated prepared copies and records its nested receipt without adding nested test counts as independent tests. The source projection is checked before/after.

The final independent reconstruction must use a packet downloaded from the new remote workflow, not the pre-publication working copy. Record actual source SHA, artifact SHA, environments, page counts, normalized text, and render differences. Cross-environment byte equality is not promised. PDF rendering is a layout check, not mathematical verification.
