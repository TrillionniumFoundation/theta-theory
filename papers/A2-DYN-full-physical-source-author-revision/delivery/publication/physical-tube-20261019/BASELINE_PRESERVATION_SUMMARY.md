# Final predecessor preservation census

**Status: PASS.** Observation completed at 2026-10-19T01:35:06.201634Z.

The fixed predecessor is commit `15ad3962de63f50911b765fe6608e722fe9b8c82`, root tree `a1eccaf41b953cbcba430cf0ecf78195771db4a8`, article tree `39f02eb2dab466bb742c7f96139a6535d7bb10ef`. Its complete 1,645-file blob list independently recomputes that article Git tree.

All 1,645 of the 1,645 published predecessor files were read from the predecessor article and compared with their pinned Git blob ID, byte count, and Git file mode. Every retained new-article location listed in the JSON was also compared byte for byte with its verified predecessor file.

| Preservation class | Baseline paths |
| --- | ---: |
| Exact at original path in new article | 1,624 |
| Exact at a retained path in new article | 21 |
| Missing exact copy in new article | 0 |
| Predecessor mismatches | 0 |

The 50 core files 260–309 and all eight model/input source files remain byte-identical at their active paths: **PASS**.

## Paths with changed current content and exact retained copies

| Baseline path | Exact retained location in new article | Baseline Git blob |
| --- | --- | --- |
| `BASELINE_AND_HISTORY_AUDIT.md` | `history/global-minimizer-predecessor-documents/BASELINE_AND_HISTORY_AUDIT.md` | `21084a7c3453901907580355616664b4f1f7db14` |
| `HISTORY_PRESERVATION_AUDIT.md` | `history/global-minimizer-predecessor-documents/HISTORY_PRESERVATION_AUDIT.md` | `924b1896fa99a29e96e0b8b138af8492aaea6ce0` |
| `LITERATURE_AUDIT.md` | `history/global-minimizer-predecessor-documents/LITERATURE_AUDIT.md` | `5e9f1b6fbc93fb6e8e5c8cf8a19896d83d231270` |
| `MATHEMATICAL_AUDIT.md` | `history/global-minimizer-predecessor-documents/MATHEMATICAL_AUDIT.md` | `3311565a99532d360a4c95c7f3e2b914564d528e` |
| `PROOF_INDEX.json` | `history/global-minimizer-predecessor-documents/PROOF_INDEX.json` | `fba9a240946bf24d9058495624ed142540f90ebd` |
| `PROOF_LEDGER.md` | `history/global-minimizer-predecessor-documents/PROOF_LEDGER.md` | `3772baea7b920bb574c29389369fa2552c1903af` |
| `PUBLICATION_STATUS.json` | `history/global-minimizer-predecessor-documents/PUBLICATION_STATUS.json` | `a628fedfbd9d00a948441e21e8b5cf08889db392` |
| `README.md` | `history/global-minimizer-predecessor-documents/README.md` | `0908b08fb549b519cd16ad255b415a8c1343310a` |
| `RESPONSE_TO_REFEREE.md` | `history/global-minimizer-predecessor-documents/RESPONSE_TO_REFEREE.md` | `8d9e23a0831bc6ac014c2c3db8c401b3feba0dec` |
| `SOURCE_IDENTITIES.json` | `history/global-minimizer-predecessor-documents/SOURCE_IDENTITIES.json` | `231d1c12582f130faefa0dd47404def1f225c989` |
| `SOURCE_MANIFEST.json` | `history/global-minimizer-predecessor-documents/SOURCE_MANIFEST.json` | `b8e116ca5d8def73ffa9870b2823c652d44b12e0` |
| `VALIDATION.md` | `history/global-minimizer-predecessor-documents/VALIDATION.md` | `1ba43781d962c3b761c757653cae5c3affea8440` |
| `delivery/PROOF_NAVIGATION.md` | `history/global-minimizer-proof-navigation/PROOF_NAVIGATION.md` | `b7d76e1efa68b6c52abb1e5829a37bb02070df29` |
| `history/historical-v108/build/main.log` | `evidence/current-execution/historical-recovery/20261018T164336583551Z/main.final.log` | `f5d2c9671a473dbb7bf8dba0c2184a119f1e685f` |
| `history/historical-v108/build/main.pdf` | `delivery/A2-DYN-historical-v108-main.pdf` | `7d94b05e1ff99fb811923ea6e8aff59ffc45ef9a` |
| `history/historical-v108/build/supplement.log` | `evidence/current-execution/historical-recovery/20261018T164336583551Z/supplement.final.log` | `a6a52e2c2521b88b3d3a4fa7a7b3ed506ba97e9a` |
| `history/historical-v108/build/supplement.pdf` | `delivery/A2-DYN-historical-v108-supplement.pdf` | `b579f69a1d9c7b99e60b46c18c9df29dc040575f` |
| `main.tex` | `history/global-minimizer-predecessor-documents/main.tex` | `0a42265da2042c60ec7e3c9374ba3d2e3abc6906` |
| `tools/build_proof_index.py` | `history/global-minimizer-predecessor-documents/tools/build_proof_index.py` | `c511f525cabf723febb32c6ad601aceb335e062d` |
| `tools/package_source_manifest.py` | `history/global-minimizer-predecessor-documents/tools/package_source_manifest.py` | `50f1d7b1051e414eb460373a9a351b713515d19a` |
| `tools/validate_revision.py` | `history/global-minimizer-predecessor-documents/tools/validate_revision.py` | `192e90a0c88985b83a64819b83903851a30bfb21` |

## Interpretation and reproducibility

The retained predecessor documents include the exact earlier source manifest, proof index, proof ledger, main manuscript, response, audit documents, and source identity record. The earlier proof navigation remains under its dedicated history directory. Historical main/supplement logs and PDFs regenerated during this revision are covered by their exact earlier execution-log and delivery copies.

This is a path-level preservation check. It records the snapshot of baseline paths and their retained copies; newly created execution, delivery, or publication receipts may continue to accumulate. It does not assert a new mathematical theorem, replace proof review, or claim a current-head CI pass.

The predecessor contains 0 local files outside the pinned 1,645-file publication list; those paths, if any, are separately enumerated in the JSON and are not silently added to the published source identity.

Reproduce with Python 3 using the saved verifier and these explicit read-only inputs:

```bash
python verify_baseline_preservation.py \
  --baseline-blobs '/workspace/scratch/b5cc344d4c8e/iteration-20261019/source-audit/BASELINE_ARTICLE_BLOBS.json' \
  --old-article '/workspace/scratch/b5cc344d4c8e/theta-theory/papers/A2-DYN-global-minimizer-localization-author-revision' \
  --new-article '/workspace/scratch/b5cc344d4c8e/theta-theory/papers/A2-DYN-physical-tube-source-height-author-revision' \
  --output-dir '/workspace/scratch/b5cc344d4c8e/iteration-20261019/publication-preflight'
```

Path-level JSON SHA-256: `54aafb3c16e024a2b4b6163542d71640797a54048c3c2d52ab0d1ef8d17761ae`.
