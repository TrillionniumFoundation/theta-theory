# Exact-source qualification — revision 86

`bash build.sh` qualifies an exact Git checkout. `--local` is forbidden in CI and is an archive-only mode; it does not establish a remote SHA. Both modes build the complete supplement.

The verifier pins the v85 paper tree `55c3282d300f87c688a66abacc3cc597a7668721` and controlling v85 report blob `86ecdfdf87d9ad7f6ecbe20c97f10cc75967eec5`. It checks inherited core, Python, appendix, bibliography and provenance bytes and all root-file snapshots. It keeps inherited claim flags unchanged and rejects promotion of the still-unproved endpoint.

Finite explicit-exception fixtures run in ordinary and optimized Python. Native TeX must stabilize references with no LaTeX/package or pdfTeX warning, overfull box, undefined reference or missing character. Actual recorder union must equal all 201 core files: three new cores in the article, all 198 inherited cores in the supplement. PDF text boxes are checked on every page; article pages and selected supplement pages are rendered.

The full preceding article is retained with scoped reference and page-reference namespaces. Only its bibliography formatting wrapper is closed by the deterministic assembler; its source snapshot and bibliography remain unchanged. Historical module 189 remains explicitly superseded in place. The assembled archive uses globally unique hyperref destination names so that repeated historical equation and appendix numbers do not create duplicate PDF targets; displayed numbers and source snapshots are unchanged. The build gate explicitly rejects pdfTeX warnings, including duplicate destinations.

The exact-SHA workflow is `.github/workflows/a2-dyn-v86-qualification.yml`. Completed run results, artifacts and source hashes are the source/build evidence. Such evidence does not certify continuum mathematics or substitute for a specialist review.
