# A2-DYN revision 76: qualification contract

Run `bash build.sh` in an exact checkout. The script checks the v75 paper tree and controlling report blob, verifies byte-preservation of all 170 inherited cores, appendices, Python sources and bibliographies, and checks that no inherited Boolean claim has been promoted. It assembles the entire retained mathematical pipeline, including the full v75 article, and compiles the journal and supplement natively. Recorder coverage must equal all 173 active cores. Ordinary and optimized Python outputs must agree; unstable references, warnings, overfull boxes, undefined references and missing characters fail the build. PDF text geometry is checked.

`bash build.sh --journal-only` is an explicitly limited local mode. It checks only new finite fixtures and the new journal. It cannot certify a remote checkout or preservation/build of the full inherited supplement and is forbidden in GitHub Actions.

Workflow: `.github/workflows/a2-dyn-v76-qualification.yml`. Its artifact records the exact commit, source archive, hashes, TeX logs/recorders and PDFs. A workflow result must be observed before full remote qualification is claimed. Continuum correctness, complete weighted dynamical decay, specialist review and editorial acceptance are outside this qualification contract.
