# Revision 81 exact-source qualification

`bash build.sh` verifies the exact Git checkout. `--local` is forbidden in CI and only supports an archive check. Both modes require the complete supplement; there is no journal-only qualification route.

The verifier pins v80 paper tree `36fd73cb74917dcd1af315fd9696ac3026ff7bab` and v79 report blob `dd7a2e7ee91757cdb253eaf8e605cd330ca11e3f`. It checks all 185 inherited cores, Python sources, appendices, bibliographies and prior provenance byte-for-byte, plus every top-level v80 snapshot. All inherited claim flags must remain unchanged. Unsupported endpoint and limit-exchange claims must remain false.

New finite checks cover exact exponents, physical-cap layer cake, endpoint-vector scaling, terminal interpolation, truncated and fractional critical integrals, and negative optical variation. They use explicit exceptions rather than removable assertions. The new and inherited diagnostics must agree in normal and optimized Python.

Native TeX must compile the full supplement and journal, stabilize references, and pass the existing warning/undefined-reference/overfull/missing-character gates. Actual recorder coverage must contain 11 journal cores and 185 supplement cores, with union exactly all 188 active modules. PDF word boxes are checked on every page and the journal plus selected supplement pages are rendered for inspection.

Workflow `.github/workflows/a2-dyn-v81-qualification.yml` records the final source SHA, branch and paper tree and uploads exact sources, both PDFs, logs, recorders and checks. Only actual successful final-SHA runs qualify the remote source. These checks do not certify continuum mathematics or replace independent specialist review.
