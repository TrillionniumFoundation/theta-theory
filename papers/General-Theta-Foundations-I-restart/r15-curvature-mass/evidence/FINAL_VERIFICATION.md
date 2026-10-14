# Final read-only verification — restart R15

Date: 8 October 2026. Status: PASS for the stated build and delivery scope.

## Immutable chain

- Canonical origin: `18000b21e4bfd89180ccb069e46ac0f21621f34d`.
- Latest external review used: `801faac37eaf1c66e9d9554fa704ad0e1e8c6bfc` (R11).
- Canonical-first-parent research integration: `3f3571147297a9511f9c888ffcc0e3b8346f42bc`; its second parent preserves R14/R13/R12 research and the complete R11 predecessor.
- Transport/build integration: `9b2436079d5f7cb010fda30769a2b7f3fec37df5`.
- Ordinary mathematical-source commit: `0f391dd67b2fc8d47685e91d86253898451e2730`.
- Native source tree: `1447a5858bbb75d35367299df5f9f24362e89904`.
- Artifact commit: `142d68d6fbb00e5ce2de82848f54237940caf404`, whose parent is the ordinary source commit.
- Hosted successful run: `37782575273`; downloaded artifact: `11551979793`.

The final commit containing this record adds only four evidence files to the artifact commit. It does not alter mathematical source, hosted PDFs, prior evidence, controlling files, or preserved subtrees. The containing Git commit, rather than an impossible self-referential hash inside this file, identifies the final verification head.

## Independent reproduction

The actual hosted ZIP was downloaded and its SHA-256 checked against the artifact digest. All 344 bound files were verified. A separate build ran the downloaded scripts against the pinned source/tree in a second operating environment. The complete 345-file downloaded tree, including its delivery binding, remained byte-for-byte unchanged.

Both environments passed the source audit and ordinary/optimized regressions. Native checks: 8,837 finite arithmetic or deterministic numerical witnesses, not 8,837 continuum proofs. The retained R11/R10/R9/R8/R7/R6 suites also passed; their nested counts must not be summed as unique independent tests. The native audit covers 33 manifest-listed files plus the manifest, 51 labels, 74 cross-references, 12 bibliography entries, 18 formal statements, and all 10 active TeX inputs.

Each environment performed 14 isolated PDF builds, three passes each: eight mathematical builds and six cover builds. The final components have 19, 17, 49 and 23 pages, respectively. No undefined references or overfull boxes were found. Isolated repetitions within each environment are byte-identical. TeX Live 2023 and 2025 produce different PDF byte hashes; all normalized texts, page counts, and all 108 page renderings are identical across environments at 97.2 dpi in MuPDF 1.26.7. All pages were visually inspected, with native theorem/proof pages also inspected individually.

`FINAL_READ_ONLY_VERIFICATION.json` records the cross-environment hashes and comparison. `INDEPENDENT_BUILD_RECEIPT.json.xz` losslessly preserves the complete independent JSON receipt, including every nested inherited build and regression record. Its decompressed JSON SHA-256 is `150629d29aaf2be061a834c291e7fc7f0e2a3281f75478263e42254fa7b026be`. It can be inspected using `xz -dc INDEPENDENT_BUILD_RECEIPT.json.xz` or Python's standard `lzma` module.

## Preservation and scope

`SOURCE_PUBLICATION.json` records unchanged Git identities for the four control files, R4-R11 mathematical subtrees, review inputs, and R13/R14 research records. Canonical and R11 review refs were checked by the hosted job. A final complete branch search, including its empty continuation page, found no newer restart external report than R11.

This is a complete R15 plus complete integral U/T/S rebuild, not a full-repository rebuild or a new line-by-line certification of all v1-v96 mathematics. The independent build uses the same checked scripts in a separate environment; it is not an independent mathematical referee or a priority/acceptance certificate. The genuine remaining mathematical objectives are recorded in `../SCOPE_AUDIT.md` and the referee packet.
