# Build and independent-reconstruction protocol — R51

Dependencies: Python 3.11 or later; numpy, scipy, pypdf, mpmath for the retained chain; pdflatex with latex-extra, fonts-recommended, lmodern and cm-super; Poppler pdfinfo/pdftotext. No network access or repository mutation is performed by `build.py` itself.

```bash
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
D=papers/General-Theta-Foundations-I-restart/r51-causal-acquisition
python3 "$D/verify.py"
python3 "$D/regression.py" > /tmp/r51.normal.json
python3 -O "$D/regression.py" > /tmp/r51.optimized.json
cmp /tmp/r51.normal.json /tmp/r51.optimized.json
python3 "$D/gaussian_certificate.py"   # checks stored certificate; --write is development-only
python3 "$D/build.py" --output /tmp/r51-output --retained --prepared-root "$PWD"
```

For an immutable checkout, additionally pass `--source-sha <full source commit>` and independently verify that the actual source projection agrees with that commit. A supplied string is not a repository readback. The artifact receipt binds source, workflow trigger, run, PDF hashes and input projection. Final evidence must be a separate child commit which leaves ordinary source and artifacts unchanged.

The native article is compiled in two independent temporary directories, three passes each. Normal/-O regression outputs must be byte-identical. Undefined references, duplicated labels, unresolved citations, overfull boxes, and a mismatch in actual TeX recorder inputs are failures. The entire unchanged R49 build is then run with its full retained chain, not just a selected old PDF. Historical source-recovery files are hash-verified and decoded statically; old publication workflows are not executed. All ordinary source is checked before and after.

The returned `R51_prepared_sources.zip` is sufficient for a second isolated reconstruction with the same commands. Before extracting, reject traversal and symlink entries. Hash the actual extracted input set; compare it again after the build. Compare each PDF's page count and normalized text, then rendered pages at a declared renderer/resolution. Only claim cross-environment byte equality when observed: TeX versions may change PDF bytes without changing text or rendered pages. Review all native pages for clipping and layout. Full companion rebuild is delivery evidence, not independent re-proving of all historical theorems.

Failures are preserved in evidence, not erased by silently weakening checks. The publication must not create a referee-ready branch on the basis of an unfinished build. The source and artifact commits can remain available as research evidence if a later verification fails.
