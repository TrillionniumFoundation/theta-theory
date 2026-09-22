# Preservation and dependency record — v116

The controlling frozen source is v115 at review commit `1cb4e00c86699247454d21dbec2dcce01a9c6b8b`, whose parent is the reviewed head `acfd3d57e0053e1b03df53020fd8e79e14599c03`.

The original `article/v115/` directory is not modified. The v116 copy additionally contains `history/v115_source/` and `evidence/V115_SOURCE_MANIFEST.json`, with the 24 active old TeX files and their original hashes. Old revision documentation and the receipt generator are archived under `history/v115_*`. The prior v114 source archive and its manifest also remain.

The new verifier checks **158 old theorem/proof blocks verbatim**, **201 prior labels**, and **27 old bibliography keys**. **17 active TeX files are byte-identical** to v115. Reorganization of the title, abstract, introduction and nearest-literature prose does not remove a mathematical environment. New material is in `02j-proof-details.tex`, `02k-quartic-primary.tex` and `02l-conductor-primary.tex`; these are actual inputs of both the complete and geometry manuscripts.

The original polar theory, quadratic geometry, residual calculus, orientation descent, all-dimensional component optimization, wall geometry, higher-product sector calculations, native realization, contact calculations, uniform constants and statistical experiments remain active. The full article continues to include all application appendices. The separate application entry point is byte-identical to v115.

The new primary theorems use no application labels or assumptions. That separation is checked programmatically in `verify_v116.py`. The geometry and application reading copies exchange cross-reference labels exported from the complete article; this is a typesetting dependency, not a mathematical proof dependency.

The `--git-baseline` option checks every archived v115 source byte against the frozen Git object. The remote build runs that check, from both the repository root and the article directory, and records the result in `evidence/GIT_BASELINE_CHECK.json`. The ordinary build also works from a standalone source archive without inventing a Git provenance claim.
