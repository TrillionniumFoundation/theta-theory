# Final read-only verification — General Theta restart R32

Date: 2026-10-11. This receipt validates the artifact parent below. It does not contain a circular assertion of its own future commit SHA.

## Immutable chain

- Canonical restart: `18000b21e4bfd89180ccb069e46ac0f21621f34d`.
- Preserved R31 intake: `155677ec098ea24c45d93cd4848fbeb03577e94e` (R30/R31 contain contracts, not completed new manuscripts).
- New R32 research intake: `e799647343c5d2b6c892c3c2dde887439fd98a91`, canonical first parent and R31 second parent.
- Build bootstrap: `2d06d6c41a0764b478b3bd1b11b1b7d48ea5dd4c`, direct child of the intake.
- Ordinary mathematical source: `6a62f90eff5357d6e47b3faeba13a25e8500dee8`.
- Artifact-only child: `20838ed65f7ff50cda2cb726f393929e42d37c74`.
- Artifact root tree: `624cb55ec36834c2a2f622ee6d6ebf4520e56709`.
- Actual source directory tree (includes pinned review input): `cd1b073ffda928e27e34009df120ac997f05bcc8`.
- Ordinary-source projection: `97c35f107294a7a07308ce06813507895f4a529c`.
- Source manifest SHA-256: `b41a6288e197e068e652cc23d56b83a97e9630a916424b42fdd2b6edd75b1e94`.

The ordinary TeX/Python/Markdown/JSON sources were committed and non-force pushed before any hosted build. Compressed Git blobs were transport, not a substitute for ordinary manuscript sources. The source branch still pins the ordinary-source commit; the artifact branch separately pins its direct child. Neither ref is advanced to the final evidence commit.

## Hosted and independent verification

GitHub Actions run `38098908126`, job `114350537056`, completed successfully: ordinary-source export, dependencies, full read-only build, artifact-only publication and upload. Source artifact `11686603529` was downloaded; its actual ZIP, not the local authoring tree, was independently extracted and rebuilt. Full artifact `11687650249` was also downloaded, hash checked and used for the PDF comparison.

Each environment executed 38 isolated PDF builds, three TeX passes each, including the complete native manuscript and all retained companions. All 725 independently extracted input files remained byte-identical. The native regression contains 1183 rational, 6625 integer and 578 floating sanity cases (8386 total); normal and Python -O outputs agree. The recursively invoked historical cases are not added as independent counts. The native source audit verifies 38 ordinary files plus manifest, 12 actual TeX inputs, 64 labels, 69 cross-references, 13 bibliography entries and 13 formal statements. No undefined references or overfull boxes were reported.

The delivery contains 14 PDFs, 376 pages. Hosted TeX Live 2023 and independent TeX Live 2025 produce different PDF bytes for every document; all normalized texts, page counts and all 376 rendered pages coincide at MuPDF/DeviceRGB/97.2 dpi. Within each environment, the declared isolated duplicate builds are byte-identical. All pages were visually reviewed in contact sheets; the native paper and corrected F cover were also inspected more closely. See the two JSON receipts for exact hashes and limitations.

## Read-only historical boundary

The hosted publication checked 35 pinned source/control/review objects and read back canonical, R29 review/ready, R31 intake and R32 intake refs without changing them. Latest review-branch search at final verification returned 19 matching restart review branches and then an empty continuation page; the latest found report remains R29 at `204a9cc62c2c1ce48d0668f35c4bbc326118ebd7`. The immutable report blob is `dd9a1681b0e807e892c4c053640ec8e332ca94e1`.

The final child is restricted to `INDEPENDENT_REBUILD.json`, `PDF_RENDER_COMPARISON.json`, `FINAL_READ_ONLY.md` and `REFEREE_PACKET.md` in this evidence directory. It changes no mathematical source, PDF, old review, realization, frozen archive or canonical branch. New revision and referee-ready refs are created at that child, and only the new R32 research ref is fast-forwarded. Final ref readback is performed after creation and is reported externally, not presumed by this receipt.

## What this does not certify

Builds, finite cases and pixel comparison do not certify continuum mathematics, priority or top-four acceptance. The mathematics is for declared known-kernel passive experiments and separately stated retained results; no unrestricted control or unknown-kernel theorem is inferred. Historical preservation/rebuilding is not a claim that every v1-v96 proof and every old report was independently re-read. See `HISTORY_COVERAGE.md`, `SOURCE_LINEAGE.md`, `PROOF_AUDIT.md` and `SCOPE_AUDIT.md`.
