# A2 v166 — final visual and remote publication audit

This is an internal delivery and reproducibility audit, not an external independent mathematical referee report.

## Locked source and actual publication

- Repository: `TrillionniumFoundation/theta-theory`.
- Revision branch: `revision/a2-v166-universal-flattening-2026-09-26`.
- Controlling review commit: `e795bc76e458260f0efcc8182c292f19d0610ca0`.
- Final authored build source: `60304100b64960e8e3e3a704b23c38fb38b37a67`.
- Verified complete-manuscript publication commit: `a616fe75e0a6aec0579a7583a450220b6c40579d`.
- Published tree: `2832509cc2392c3938ed77e66b9514ec88af44c6`.
- Successful GitHub Actions run: `36217566409`, job `108336488366`.
- Downloaded build artifact: `10898112804`, `a2-v166-complete-review-build`.

The workflow's compilation, inherited-check, artifact, and publication steps all completed successfully. The remote branch head was fetched after publication; publication was not inferred merely from an uploaded artifact. The controlling review branch was fetched again and still pointed to the locked review commit.

## Complete outputs checked against the downloaded artifact

| Manuscript | Pages | PDF SHA256 |
| --- | ---: | --- |
| Paper I, reconstruction.pdf | 74 | a8fe771fee240c2bdb2aab61534c7413aa02b02caa65446cde3784a0a38ecec6 |
| Paper II, divisor-geometry.pdf | 102 | e31b5839482789f0c62c99a38209c5a58b2bcccd07624db6a0aa83aa04090f60 |
| Preservation master, geometry.pdf | 168 | 256b8171fafa0f744766acf6a1c04b4780511ef27594dcfddf5f62777548202a |

The downloaded PDF and LaTeX hashes matched `BUILD_RECEIPT_V166.json`. All three complete LaTeX files also matched the independently compiled local copies byte for byte. The final logs contained no undefined references, undefined citations, multiply defined labels, or overfull horizontal boxes. Companion-paper reference numbering and pagination had stabilized.

## Preservation and branch isolation

The exact preservation checks retained all 358 predecessor mathematical environment blocks and all 539 predecessor master labels. The new master has 390 such blocks and 585 labels; its mathematical blocks partition exactly once between the two complete companion papers. Historical sources and the controlling report were not edited. Superseded front matter and the prior root review entry and README were archived.

The GitHub comparison from the controlling review commit to the complete publication commit was inspected. Its merge base was the controlling review commit; it was six commits ahead and zero behind. Changed paths were confined to the new v166 directory, its new build workflow, and the root README and review entry. No historical manuscript file was modified or deleted. All branch-ref writes in this revision targeted only the new revision branch.

## Visual inspection scope

Text-span bounds were checked programmatically on all 344 pages of the three PDFs. No text span extended beyond the page boundary. This check is not a claim that every page was read visually.

The actual final artifact was rendered again and the following 27 pages were visually inspected as page contact sheets:

- Paper I: 1, 71, 72, 73, 74.
- Paper II: 1, 2, 3, 4, 5, 6, 7, 24, 25, 26, 27, 31, 32, 33, 34, 36, 37, 38, 39, 40, 41.
- Preservation master: 1.

No clipping, overlapping equation blocks, broken glyphs, or missing content was observed on those rendered pages. The previously isolated run-in saturation heading was supplied with its introductory sentence, and the all-arc forward reference was changed to an explicit numbered section reference before the final build.

## Exact checks and remaining external obligations

The full inherited v164 verification chain was rerun, and the new exact coefficient, conic-coverage, extension-module, saturation, ramification, invariant-lattice, and overlap checks passed. Finite examples do not certify the general proofs, global gluing, historical novelty, or acceptance by any journal.

No external independent full audit of the sharp inverse was obtained. The legitimate Ballico 1993 full text was not retrieved, so its theorem-level comparison remains incomplete. These matters are disclosed in the manuscripts, the 54-item response, and the separate audit handoff and literature record. The universal relative-Hilbert construction is attributed to classical representability and is not presented as a proof of every higher-contact component conjecture.
