# Exact-source qualification — revision 90

`bash build.sh` requires an exact Git checkout. `bash build.sh --local` is allowed only outside CI and still requires the complete exact-baseline archive. Neither mode skips the technical supplement.

The source verifier pins the v89 paper tree `85ffb2f2b372670cf5ccb3dbf3c2032d4c835a51`, complete top-level snapshot tree `1453a92647c1fbb8e44e9b0c988f21a0109a357d`, controlling v89 report blob `1dba5b7de5447a59483fc790e6072f9e165aa8e3`, and both distinct preserved v88 variant trees. It checks every inherited core, Python source, appendix, provenance record, bibliography, included v89 problem/input file and executable mode.

The complete prior status is inherited from a pinned blob. No flag is deleted by that convention: the verifier emits every inherited and new flag as `source.resolved_claims` and rejects disagreement on repeated keys.

Finite checks cover interval multiplicities, prefix product differences, anchor geometry, radial kernels, physical caps, exponent arithmetic and the interpolation integral. They run in normal and optimized modes with explicit exceptions, not disabled assertions. All recent inherited finite checks also run.

Native TeX must compile both article and complete supplement with stable references and no warning, missing glyph or overfull box. Actual recorder coverage must be three new journal cores, all 210 inherited supplement cores and their 213-core union. Page geometry is checked and article pages are rendered.

Workflow: `.github/workflows/a2-dyn-v90-qualification.yml`. Success requires a completed run on the actual new author SHA. These checks establish source/build evidence, not continuum correctness, independent expert approval or pointwise closure.
