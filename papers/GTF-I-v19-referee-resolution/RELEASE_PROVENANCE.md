# General Theta Foundations I — v19 verified referee handoff

**Continuation Complexity and Stable Causal Certification**  
Qian Qi · Full English manuscript · 23 September 2026

## Exact release identities

- Repository: `TrillionniumFoundation/theta-theory`.
- Working revision branch: `revision/general-theta-foundations-i-v19-referee-resolution-2026-09-23`.
- Referee-ready snapshot branch: `revision/general-theta-foundations-i-v19-referee-ready-2026-09-23` (points to the commit containing this handoff record).
- Inherited v18 publication: `e7d020c49959009a775081ea9aa70c7e7fec5d52`.
- Controlling r3 review: `a94ec98d6e33d9719f72deec160f5c8270ce006f`; additional pipeline r2 review: `9f4787221c086e25f7d95b36e97aff870bd2b0c5`.
- Canonical source commit: `9ba7cc9801e4b977281ced917c7f5fa9d3dddcb3`.
- PDF and evidence publication commit: `9a8ac8fb395d1d33daa716d1ebef7cfa10da8186`.
- Successful GitHub Actions run: `35858164389`, job `107171580676`, completed 2026-09-23T12:06:25Z.
- Retrieved Actions artifact: `10748880071`, name `GTF-I-v19-referee-resolution`.
- Downloaded artifact ZIP SHA-256: `12391d31cd73c14622941c034e91920b933c1462f8031458afe6a2f93e5cb345`.
- Aggregate canonical TeX fingerprint: `fa27a4e69e6c854b7db6434cdb326a20d71aefb1aca3e1a2c70e7de93f9ff67d`.

This handoff record is added after the successful publication and does not change the mathematical source, compiled PDFs, or executed evidence. The source commit, publication commit and handoff commit therefore have deliberately distinct roles.

## Referee reading entry points

All paths below are relative to `papers/GTF-I-v19-referee-resolution/`.

- `paper.pdf`: 46-page canonical article; main theorem 1.1 on page 2.
- `complete-development.pdf`: 340 pages, including all 294 predecessor pages unchanged.
- `RESPONSE_TO_REFEREE.md`: point-by-point response to E17-R3.1–12 and E17-P1–8, distinguishing inherited answers, new proofs and the unresolved original-literature audit.
- `PROOF_LEDGER.md`, `PROOF_STATUS.json`, `evidence/THEOREM_LOCATIONS.json`: contribution subtraction, exact statement identity and compiled locations.
- `HISTORY_AUDIT.md`, `PIPELINE_STATUS.json`, `PRESERVATION_MAP.json`: historical scope, all eleven components, actual consumer edges and source preservation.
- `evidence/BUILD_RECEIPT.json`: executed source-bound build record.
- `evidence/SUBMISSION_SOURCES.zip`: portable local-input canonical source archive.
- `evidence/COMPILED_SOURCES.zip`: full available GTF source closure, including the pinned predecessor PDF; 1,668 archive entries.

## Principal additions submitted for review

Theorems 5.1 and 5.2 (pages 15–17) give a stochastic continuation-width obstruction and the exact width profile attaining the optimal odd-sample binary audit value. Lemma 14.1 and Theorem 14.2 (pages 41–43) give the two-count physical audit: 400 training resets, 402 trials including validation, at most 504,008 retained auditor states, and expected signed score greater than 2/5 against every private width-one candidate in the stated collision family. Theorem 12.2 (pages 36–38) gives global innovation and bounded entropic-integrand transport and convergence of the backward martingale integral. Theorem 14.2 transports the same implemented audit and the global conditional-law consumer through changing microscopic trajectories.

## Executed verification and visual inspection

The successful remote build used three pdfLaTeX passes, resolved 134 labels, indexed 43 named mathematical statements, and recorded 85,631 exact finite diagnostic checks. Ordinary and optimized Python results agreed. All 12 negative-control executions were rejected at their intended checks. The inherited v18 and v17 diagnostic scripts were also rerun successfully. No unresolved references/citations, multiply defined labels, or overfull boxes were reported.

After publication the Actions ZIP was downloaded into the working environment. Its hash, all four artifact hashes below, archive sizes, canonical TeX fingerprint and PDF page counts were checked independently against the remote receipt. The source archive has 21 entries and contains no distributed font files; the full archive was checked for the same exclusion.

The remote PDF was rendered with PyMuPDF. Pages 1, 37, 38, 42, 44 and 46 were visually inspected at readable resolution, including the title/abstract, global transport proof, concrete certificate theorem, canonical dependency diagram and bibliography. No clipping, overlapping text, broken mathematical glyphs or unreadable diagram labels were observed on those inspected pages. Automated geometry checks cover all 46 canonical pages. Every one of the 294 inherited pages has matching extracted text and matching raster in the build's preservation check.

The GitHub comparison from the frozen v18 publication to the PDF publication returned 49 added files and no modified or deleted predecessor files. Changes are confined to the new manuscript directory, one new workflow and one new root entry point. This handoff adds one further file in the new manuscript directory only. No main, review, other manuscript, or predecessor branch was updated.

## Published artifact SHA-256

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `paper.pdf` | 633402 | `15b13cc023f7070f2ed94250bf3e2a1128717a8071dc408532e8f835184fba43` |
| `complete-development.pdf` | 3016650 | `479c27d73c280429c00288ba3c51a2c8cafafbda9a06dbf44fa78467ca709221` |
| `evidence/SUBMISSION_SOURCES.zip` | 78047 | `2c74e6070831ca8b146a4c9ea5a15fe075dc19c5649bf977b26ee6f4e5286983` |
| `evidence/COMPILED_SOURCES.zip` | 8120068 | `fc663461301c19019861bf14648b45444be4db4e7788b2de7b987d276752718a` |

## Review boundaries

Build success, exact finite tests, hashes and visual inspection are reproducibility evidence, not independent certification of the analytic proofs, mathematical novelty or journal acceptance. New proofs await external review. The original Norberg proof-level crosswalk remains unverified. The common-preparation, bounded-signal, positive-noise and bounded scalar entropic hypotheses remain explicit; the physical family is fixed-particle and single-collision. All historical program targets are preserved, without fabricating an A2 dependency or declaring the full eleven-paper program closed by this revision.
