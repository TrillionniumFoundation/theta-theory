# A2 revision 97

**Article:** Projective polynomial observations: real spectral atlases and identification walls.

**Controlling review:** `b4ab165062f3625e06717002fb419bd44ab8e7f7`,
`reviews/a2-v96-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`.

**New branch:** `revision/a2-v97-real-singularity-atlas-weight-wall-2026-09-20`.

## Reading order

Read `papers/A2-v17-boundary-information-coarsening/rigidity_v97.tex`
(the principal article), then `RESPONSE_TO_REFEREE.md` in this directory.
The independent review should pin the actual branch head, not a date or a
workflow display name. `SOURCE_MANIFEST.json` binds the new source set.

The complete historical article is retained through
`rigidity_v97_archive.tex`. No inherited mathematical or bibliography file
is edited. `rigidity_v97_complete.tex` assembles the principal and archival
PDFs after both have been built. The archive is a historical companion,
not an assertion that every old proof is needed by the new main theorem.

## Reproduction

From the repository root:

```sh
python -m pip install sympy==1.14.0
python scripts/verify_a2_v97_math.py --output /tmp/a2-v97-diagnostics.json
python scripts/audit_a2_v97.py --repo
cd papers/A2-v17-boundary-information-coarsening
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder rigidity_v97.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder rigidity_v97_archive.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -recorder rigidity_v97_complete.tex
cd ../..
python scripts/audit_a2_v97.py --repo --build --output /tmp/a2-v97-runtime.json
```

The TeX toolchain needs amsart, Latin Modern, microtype, mathtools,
mathrsfs, geometry, hyperref, booktabs, longtable and pdfpages; the archive
may use additional standard TeX Live packages. The workflow installs the
corresponding TeX Live collections and Poppler.

The exact diagnostics are finite regressions, not proof verification.
`LOCAL_VALIDATION.json` distinguishes the local principal build from the
repository/archival audit. A successful runtime receipt includes HEAD,
all three PDF hashes and page counts, logs, and the actual TeX input lists.
