# Revision 83 exact-source qualification

`bash build.sh` requires an exact Git checkout. `bash build.sh --local` is permitted only outside CI for an exact-baseline archive and does not qualify a remote SHA. Neither mode skips the full supplement.

The verifier pins v82 paper tree `d1908253a6d134b5b1e4c732e84ad111ad4f836a`, reviewed v81 tree `1d68fef5bbd1abc573d8e517e845cf889fe6431c`, and controlling v81 report blob `818e5932c895aea686da68fe37cec6018d2de759`. The exact Git mode verifies report bytes and checkout SHA. All 189 inherited cores, Python sources, appendices, bibliographies and provenance are compared byte-for-byte. Every v81/v82 top-level file is snapshotted, including the full articles.

The new finite fixtures check rational exponent relations, two-sided optical variation and coarea normalization, complete depth sums, deterministic kernel integrals, dyadic offset translations, kernel bounds and envelope tails. Recent inherited diagnostics also run in normal and optimized Python, with matching output and explicit exceptions active in both modes.

Native TeX must produce stable references without LaTeX/package warnings, overfull boxes, undefined references or missing characters. Actual recorder coverage must be all 192 cores: 3 new journal cores and 189 inherited supplement cores. All journal pages and selected supplement pages are rendered; word geometry is checked on every page.

Workflow: `.github/workflows/a2-dyn-v83-qualification.yml`. Only its actual completed exact-SHA runs establish remote source/build qualification. Source intake, the existence of the workflow, and old author builds are not final qualification. None of these checks is a continuum proof certificate or independent specialist review.
