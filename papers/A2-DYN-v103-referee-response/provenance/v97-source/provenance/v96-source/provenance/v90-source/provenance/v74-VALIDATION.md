# A2-DYN revision 74: validation contract

Authority: `SOURCE_MANIFEST.json`.

Run `bash build.sh` in an exact Git checkout. For the separately materialized, SHA-verified baseline artifact, `bash build.sh --local` performs the same source, rational, TeX and geometry checks without claiming an exact remote checkout. CI forbids local mode.

The build compiles all 167 core modules across the journal article and technical supplement, preserves all 163 inherited cores, and records the actual checkout SHA in generated evidence. Workflow: `.github/workflows/a2-dyn-v74-qualification.yml`.

Passing source checks, finite fixtures, compilation and page geometry is not a certificate of the continuum proofs, independent human review, or closure of the dynamical endpoint. Current results are in `LOCAL_FULL_BUILD_RECORD.md` and the exact-SHA workflow artifact.
