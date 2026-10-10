# Final read-only verification — General Theta restart R25

## Immutable chain

- Canonical: `18000b21e4bfd89180ccb069e46ac0f21621f34d`.
- Reviewed R24 report: `36422feadc4ccb99aaf12efb33a18bfd44cb3646`, blob `4cbd264815d33cfda32298429f2775e5b0d8f091`.
- Ordinary source: `ca41b009579e7db5293feb20c1eb3d04daea2b51`.
- Native ordinary-source tree: `9b0100d1724d24c1ff8dc55c6e1250a7417720db`.
- Artifact child: `c85c5fe49a920ec74112a7567133dd9efc8ffaa0`, root tree `474d68c8f814b4c494f09b4bd2bfd298b740c645`, direct parent the ordinary source.
- Final evidence head: the direct child of that artifact commit containing this record, obtained from Git metadata and the delivery-ref readback. Its only changes are `evidence/INDEPENDENT_REBUILD.json`, `evidence/FINAL_READ_ONLY_VERIFICATION.md`, `evidence/REFEREE_PACKET.md`, and `evidence/REVIEW_HANDOFF.md` beneath the R25 directory. Neither ordinary source nor any PDF is changed.

The canonical-first import is `16fbfe516d3a8bd993ae8f1b6784ee07d52c4957`. The initial research anchor remains at canonical; the separately published manuscript remains at `0ffcb5c85ccf9b5d199f240506314d0cf507eecd`. Final research delivery uses a newly named `research-final` ref. An earlier blocked anchor-update attempt is not claimed successful. No existing source, review, realization or archive ref is overwritten.

## Executed hosted build

Run `38018966325`, attempt 1, job `114115499129`, completed all steps successfully. It validated the ordinary tree and inherited object identities, performed full builds, and created the artifact branch without force. The source branch remains fixed. Run `38018812103` previously stopped at the shallow-clone parent check before mathematical compilation; only pipeline checkout/parent verification was repaired, with the native ordinary tree unchanged.

The native audit covers 34 ordinary files plus manifest, 11 active TeX inputs, 83 labels, 130 cross-references, 14 bibliography entries, and 21 formal statements with 21 proofs. There are 7,066 native finite checks: 7,022 exact rational checks and 44 explicitly labeled finite quantum diagnostics. Normal and optimized Python outputs agree. The complete retained regression chain passes; nested historical counts are not summed as new tests.

## Independent downloaded-input rebuild

The actual workflow artifact `11657192734` was downloaded, not reconstructed from prose. Its outer ZIP SHA-256 is `bbe2c4597b140be9031ec0195df688766c184ac92991967b5798eca8c2505ff7`; its inner source/build ZIP is `818055f3db85a057ab943ed3700e25a147d27538d31fde8aee79434fd4dba9d3`.

All 625 input files were hashed before and after the independent full build and remained unchanged. The completed invocation returned zero. An earlier foreground invocation reached a tool wait limit and was terminated; it is not counted as a complete build. The successful independent full receipt hashes to `c03a43f905360c8012ff2e98ef8e825658fa1d6075ec7b6500068ffe1d22186b`; the input hash manifest hashes to `8af507ef38b8d3c04a55a12243ac322c07810b211b392516e8802b2c8b70fa25`.

Each environment completed 26 isolated PDF builds, with three TeX passes each: 20 technical builds and six inherited covers. Ten delivery PDFs contain 280 pages: native 26, C/B/A/X/W/V/U/T/S respectively 20/16/48/37/25/19/17/49/23. No undefined references or overfull boxes were found. The 26 native pages were visually inspected; all 280 pages were rendered for parity comparison.

Within each environment repeated PDFs are byte-identical. Between TeX Live 2023 and TeX Live 2025/dev, all ten PDF byte hashes differ, while page counts, normalized extracted texts, and every rendered RGB page agree. Rendering used PyMuPDF 1.26.7 / MuPDF 1.26.12 at 97.2 dpi. `INDEPENDENT_REBUILD.json` records per-document hashes. The downloadable packet also contains the full independent receipt, input hash list, per-page parity details and comparison program.

These are source-integrity, arithmetic, build and rendering results, not proofs of the continuous-parameter theorems, independent priority judgments, or journal decisions. Complete-companion preservation is not a fresh line-by-line certification of every historical theorem.
