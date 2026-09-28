# A2 revision 76 — completed delivery verification

Date: September 17, 2026.

This record concerns the completed revision and its downloaded native products. It is outside the frozen manuscript subtree and does not change the compiled mathematical source.

## Immutable objects

- Latest report: `reviews/a2-v75-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md` at `ab44ba96a9fceeaa69bf4dbc98e5bfdd33b0cb5c`.
- Inherited manuscript source: `89d5a3aa3e9f00a806d48f19f6f6831770184d76`; subtree `8a1a76ffba5009a6c3d9ed2e3c93e48a59f3ac1d`.
- Frozen revision-76 source: `d43885eee3d05be2e896a8ac4785f4852c123131`; subtree `950c448c8e8f19c6181fee26e425a9ac23b7dca9`.
- Source branch: `revision/a2-v76-relative-envelope-2026-09-17`.
- Immutable native-product commit: `6da5d093c3b4320b114fbc2c0578136b268ab647`.
- Native branch: `revision/a2-v76-native-products-35201525106-1`.
- Product directory: `deliveries/a2-v76/d43885eee3d05be2e896a8ac4785f4852c123131/`.

The branch heads include handoff records after the immutable source and product commits. The manuscript directory retains its historical name, `papers/A2-v17-boundary-information-coarsening/`; its active entries are revision 76.

## Completed native execution

GitHub Actions run `35201525106`, job `105137158445`, completed successfully. The checked steps include source materialization against the expected tree, all three isolated native builds, publication, fetching and verification of the committed products, and artifact upload. The default branch was not changed or merged.

Seven finite-diagnostic programs passed in ordinary Python and under `python -O`, with byte-identical paired JSON outputs: adaptive, v32, v38, inherited-v73-on-baseline, v74, v75, and v76. Their scopes are stated in their outputs; these are not proof certificates.

The preservation checker verified all 1,017 inherited source files. The two replaced entrypoints are retained byte-for-byte in `archive/v75-before-v76/`; all other inherited source files remain at their original paths. All 1,435 inherited active mathematical labels remain reachable; the current three-entry union contains 1,457 labels. The three inherited principal core proof bodies are unchanged. The principal reference check accounts for its six declared full-entry aliases.

The final native logs contain no unresolved references or citations, missing-character messages, or overfull-box warnings. Ordinary nonblocking TeX warnings are not represented as proof or layout failures.

| Product | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| `rigidity.pdf` | 54 | 712510 | `d50742e5dfab201c9afa8356d574360b9f575b0f20f99e589b94e7f937e41db8` |
| `main.pdf` | 375 | 2616085 | `5700b9866bcb138afadb10bf819131e7f3a443a559364fa0906673336eb5efec` |
| `two_collision.pdf` | 7 | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |

These overlapping entries should not be counted as disjoint mathematical results.

## Independent download checks

Artifact `10487444638`, named `a2-v76-native-35201525106-1`, was downloaded after workflow completion. Its ZIP SHA-256 is `a7963e0bda20d38997729d2eb26e927ec6bc1b2b03e2dc1b5417c2ac0c17dd62`, equal to the connected artifact metadata.

All 1,035 frozen source files in the downloaded native source archive were compared with the locally tested authorial source, including executable modes. All agreed. The three downloaded PDF hashes and page counts agree with the native build report and repository provenance record.

Across all 436 PDF pages, extracted page text and uncompressed page content streams agree with the successful local isolated build. The comparison found no text blocks outside the page media boxes. This is an automated content/layout comparison, not a claim of manual inspection of every page or a fresh audit of every retained theorem.

## Sampled visual inspection

The principal-page sample included pages 1, 2, 13, 14, 15, 17, 18, 24, 25, 26, 27, 28, 45, 46, 47, 48, and 54. The new phase-weighted proof and conditioning table were also inspected at higher resolution. No blocking clipping, overlapping mathematics, or broken-glyph issue was found in this sample.

The downloaded principal page 48 was rendered with Poppler and inspected; its image was pixel-identical to the corresponding inspected local rendering. The all-page content-stream comparison above supplies a separate check, not a substitute for the limited visual scope stated here.

## Mathematical and editorial boundary

Revision 76 corrects R75-P1, adopts R75-C1, and adds the relative-determinant and phase-weighted actual-envelope arguments described in `RESPONSE_TO_REFEREE_V76.md`. Its phase-dependent bound retains common interpolation-class assumptions, the weight condition number, finite-jet alignment, and observation floors. All finite-flight and charged-preparation terms remain in the statements.

Compilation, finite algebra, preservation, and visual inspection do not amount to formal proof verification, exhaustive originality certification, or editorial acceptance. The next referee should assess the strengthened mathematical arguments and their significance. The full technical programme and the normal-incidence two-offset route have not been removed.
