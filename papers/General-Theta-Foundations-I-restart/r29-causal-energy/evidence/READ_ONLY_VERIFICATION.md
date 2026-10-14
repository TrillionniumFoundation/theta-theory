# R29 final read-only verification

Ordinary source: `31d06e6f21ccfe072016a7f0c9d39aeee4f6836f`.
Actual native directory tree at that commit: `7110d104216f244ab7521716015a21953634d7ef`.
Ordinary text projection, excluding the pinned review and later evidence/artifacts: `8e7a5a5ba3cb01124005a3c7a032197759a88e66`.
Built artifact: `ecdd25b0d87fba16cbc92675a6ba68866d166887`; root tree `2fb866785bd0a0f05321a9773e2f8439ce4e7147`. Its sole parent is the ordinary source.

The final review object is the evidence-only child containing this file. Its identifier is obtained from the remote ref, not written circularly inside the commit. It adds exactly `INDEPENDENT_REBUILD.json`, `READ_ONLY_VERIFICATION.md`, `FINAL_SCOPE_AND_GAPS.md`, and `REFEREE_PACKET.md` in this evidence directory. No ordinary source or PDF is changed. New revision/referee-ready refs point to that same object; the research ref is fast-forwarded with an expected-head check. No forced push is used.

## Remote provenance

The research branch was created at canonical `18000b21e4bfd89180ccb069e46ac0f21621f34d`, then joined the complete R28 tree without editing the old branch. R28 remains `37826ed38311e247874c35674e668855402ed6ff`. Latest completed R27 remains `c5f05d1944251a95619d5cdad814c5c83646429c`. Latest located external report is R27 at `00cad841267ee714f20d71ca9734dc5d4014ee4f`, exact report blob `79c032f1bd1697722d44206dfb28f48b1cdf2311`. A final review-branch query returned 18 entries and its continuation was empty. No later R28/R29 external report was located.

The source publisher checked all earlier restart entries against the R28 tree by Git object identity, all four controls against canonical, the pinned review blob, and its five declared read-only anchor heads. Canonical, R27 review, and R28 were again read remotely before final publication. Old review, realization and archive refs were not written. The source-only branch remains at the ordinary source; the artifact-only branch remains at the artifact commit.

## Reproduction

GitHub Actions run `38054227009`, attempt 1, job `114219280132`, completed successfully. Ordinary text sources were committed and pushed before compilation. Transport blobs and a pinned source delta were only the publication mechanism: the referee reads ordinary TeX/Python/Markdown, not encoded transport.

The ordinary-source export was actually downloaded from artifact `11670747995` and rebuilt in a second environment. All 682 export files remained byte-identical. The final artifact `11670283938` was then downloaded and its 681 ordinary inputs matched to the rebuilt export. The only excluded export file is the publication-stage binding metadata. Source, artifact, hashes, command environment, and per-PDF results are recorded in `INDEPENDENT_REBUILD.json` and the hosted `BUILD_RECEIPT.json` / `SOURCE_PUBLICATION.json`.

Each environment performed 34 isolated PDF builds: 28 mathematical-text builds and six cover builds. Technical rebuilds use three TeX passes. The full normal/optimized regression chain passed with identical output. New checks: 16,469 exact-arithmetic checks and 2,406 floating-point sanity checks, total 18,875. Inherited nested counts are not added as new independent checks.

Native audit: 48 ordinary files plus manifest, 12 active TeX inputs, 68 labels, 55 references, 13 bibliography entries, 22 formal statements and 22 written proofs. Complete corrected Companion F: 14 active TeX inputs, all 103 original R27 labels preserved, 143 references, 15 bibliography entries and 33 formal statements. The original R27 subtree was not overwritten; its full mathematical text was independently rebuilt too. Source checks and label counts do not certify proof correctness.

All 13 delivery PDFs, 352 pages, have identical page counts, normalized text and RGB pixels at MuPDF / 97.2 dpi across TeX Live 2023 and 2025. Their PDF bytes differ across those TeX versions; repeated builds within each environment are byte-identical. All new native and corrected F pages were visually inspected; inherited first/last pages were sampled, while every inherited page was rendered and pixel-compared. No undefined references or overfull boxes were reported. The unchanged eleven companion PDFs also match their old R27 hosted PDF bytes exactly.

Build scope is the complete R29 article and complete retained companion chain, not all historical papers in theta-theory. Preservation and rebuilding are not fresh mathematical certification of every v1-v96 proof, every old report, or every independent realization.
