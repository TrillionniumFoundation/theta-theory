# A2-DYN — revision 68

Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

The active complete manuscript is `main.tex`. This revision responds to the revision-67 external report at `d3321f707ba556bd25bb586178eed89038133cc8`, without changing the Lorentz table, exact return record, arithmetic factor, or unrestricted pointwise target.

The new proof route is `core/146_analytic_angular_germs.tex`, `core/147_relative_radial_persistence.tex`, and `core/148_annular_height_and_full_source.tex`. Analytic angular germs include nonlinear sectors with zero tangent fraction. A positive outer-annulus comparison gives original-source ordered essential height on fixed persistence strata, uniformly over every finite birth order. Positive-center-guard non-seam centers are included. This is not a proof of the physical angular-condition tail or the complete incidence and complementary clearance heights.

All 145 inherited core modules, 197 Python files, seven appendices, and the bibliography are byte-identical. All inherited compiled inputs and mathematical labels remain. The preceding abstract and introduction are compiled verbatim in `appendices/v67_frontmatter.tex`; the complete old main and replaced metadata are archived in `provenance/v67-*`.

Run `bash build.sh` from this directory, with the frozen revision-67 directory present beside it. The workflow `.github/workflows/a2-dyn-v68-qualification.yml` checks both author refs independently at their actual SHA and uploads the complete PDF, exact source archive, native build logs, finite diagnostics, and theorem-page renderings. A branch name or a copied artifact is not a successful workflow run.

See `RESPONSE_TO_REFEREE.md` for the item-by-item mathematical response and `SOURCE_MANIFEST.json` for preserved theorem status. No independent human specialist review or formal proof certificate is claimed.
