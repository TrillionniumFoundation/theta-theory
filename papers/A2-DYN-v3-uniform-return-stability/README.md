# A2-DYN v3: uniform stability of actual return records

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

This is a complete native TeX revision of A2-DYN, not a change of topic. It retains all 24 proof bodies and all 66 labels of the locally delivered v2 article and adds four results on genuine moving return events. The v1 manuscript and the frozen A2-GEOM article remain untouched in their original repository paths.

## Reading and building

Read `main.tex` and the eleven files under `core/` in the order printed by `main.tex`. Compile with `bash build.sh`; the only manuscript input closure is this directory. The output is `main.pdf`. Build requirements are Python 3, latexmk, pdfLaTeX, Latin Modern and the standard AMS/LaTeX packages.

The new section `core/11_return_stability.tex` proves fixed-return-count continuity of the raw mixed density in L1 and of the zero-extended record in first moment. The exact Kac means imply compact L1 families and uniform integrability. Consequently stationary unfinished time, collision count and displacement are negligible on the square-root-time scale uniformly over the whole radius interval. Bounded weighted insertions have a positive-denominator conditional comparison.

The complete joint periodic annihilator, strict period-excess theorem, raw critical-edge calculations, exact local inversion, mean identities and prior interfaces remain active. A full geometrically uniform raw density LLT is still the target; its common operator realization, measurable-cohomology/variance criteria and central all-branch residual bounds are not asserted without proof.

## Review provenance

Remote starting commit: `36f1365041de95ca478739a1e2984734c72f95aa`.
Frozen A2-GEOM v43: `4557df22f5c72bc80943690ecd6c2e39de3734ab`.

The requested A2-DYN-specific referee report was **not located** in the branch searches made for this revision. The available A2-DYN v1 `SPECIALIST_REVIEW_BRIEF.md` explicitly describes a handoff, not an independent report. The latest located A2 review, `reviews/a2-v43-external-top4-final-rereview-2026-10-04/REFEREE_REPORT.md` at `af2390e3073acf8ccd90b10d7566e30cbf18c425`, reviews the geometric article, not A2-DYN. Its favorable recommendation is not attributed to this dynamics paper.

Accordingly the response document addresses verified review items and author-side proof scrutiny, not invented comments from a missing report. Neither an independent human review nor formal continuum certification is claimed. Source/build checks and finite diagnostics do not replace the mathematical proofs.
