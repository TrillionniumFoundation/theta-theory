# R11 final read-only verification

## Immutable inputs and actual delivery

- Mathematical source commit: `6ef290d21064b1e6514b343d3d451ad0a77e0c04`.
- Native mathematical source tree (31 manifest members plus the manifest): `f37f42455e99419d118156ecb122d9826e651c2d`.
- Complete PDF/artifact commit: `4eb34d48cb7ba5b3fff9ad8cc958ce14a70fbda9`.
- Successful complete delivery run: `37673245843`; artifact `11506380133`.
- Canonical restart anchor: `18000b21e4bfd89180ccb069e46ac0f21621f34d`.
- Reviewed external R10 report head: `6f3ca64beec4b054dba8cb5def1a6c69fbc46d52`.

The source was committed once and did not change during the delivery repairs. The ancestry after source is a receipt-only commit `f12056e34660bf98e2ae1098943a0134550707ed`, the artifact-publication workflow repair `53f40a056ba5b057aa58c4af59fb45d7a4107a68`, and the complete artifact commit above. The complete artifact commit is therefore not asserted to be the direct child of the mathematical source commit.

The final verification commit adds only `INDEPENDENT_REBUILD.json`, this document, and `REFEREE_PACKET.md` in this evidence directory. Mathematical source and PDF objects remain those of the artifact commit. Its actual commit identity and the three delivery refs are read back from GitHub after publication and included in the external delivery binding, avoiding a self-referential commit hash in this document.

## Independent execution and file identity

The complete hosted archive SHA256 is `cb4206b138f83368313b8ab01d35ab1731f6c07c81278d9af1b8add666359c73`. Its 303 exported file hashes were verified before execution. Including `DELIVERY_BINDING.json`, 304 input files were snapshotted. A fresh reconstruction of the native Git tree matched the immutable source tree. All 304 input files remained byte-for-byte unchanged during an independent complete build to an external output directory.

The hosted and independent environments each ran ten isolated PDF builds, three TeX passes per build: two native R11 builds, two complete R10 builds, two complete R6 builds, two Supplement S cover builds and two Supplement T cover builds. Ordinary and `python -O` regressions agree; the native source audits agree across environments. No undefined references or overfull boxes were detected. These tests are finite checks, not proofs of continuum statements.

The native audit has 51 labels, 73 cross-references, 19 bibliography entries and 12 formal statements. Native exact-rational regression has 6,789 checks. Retained native groups are R10: 2,734; R9: 4,850; R8: 39,364; R7: 14,483; R6: 27,027. Nested wrapper invocations are not counted as additional independent mathematical evidence.

TeX Live 2023 and 2025 produce different PDF bytes. For the 16-page main article, 49-page integral Supplement T and 23-page integral Supplement S, normalized extracted text and all 88 page renders are identical at 97.2 dpi using MuPDF. All pages were rendered and inspected in contact sheets. Hashes and renderer comparison results are in `INDEPENDENT_REBUILD.json`; full raw receipts and all page hash pairs are in the delivery archive.

The actual PDF Git blobs, independently recomputed from the downloaded bytes and matched to the GitHub contents API at the artifact commit, are:

| PDF | Git blob |
|---|---|
| Main R11 | `322e6e12eb072e8146958e1537d3e61c49df45d9` |
| Integral Supplement T | `1bcabf5155e7ebe45c43fbbd4d322d2a31c4ae1d` |
| Integral Supplement S | `9923114cedf6b692acdf06f1fc37c2d413478ecf` |

## Control and history preservation

The downloaded bytes of all four controls and the latest report match their pinned Git blobs:

| Input | Git blob |
|---|---|
| `General_Theta_Foundations_v0.1.md` | `2f07620415114d870ac80b7feeffb9cbb514c6a1` |
| `RESTART_CHARTER.md` | `863318cd21012e4259aa26538d7c99c21e615666` |
| `THEOREM_TARGETS.md` | `ce06d7e4b738bfd489df2d073e4303fd79cfaac6` |
| `REALIZATION_REGISTRY.md` | `7da262b0564aad606dc06daada2cbaf76b8fbfa7` |
| R10 external report | `3b60c8fd6bd915dc8585c029478e83180f18a67e` |

`HOSTED_PUBLICATION.json` records preserved R4-R10 and review-input subtree identities. The artifact repair modifies only new R11 artifacts/evidence and a new publication workflow; it does not alter those historical subtrees. Old review, realization and frozen-archive refs were not written by this revision. The canonical and pinned review refs were checked again by the successful publication job.

## Publication failures retained, not hidden

Run `37670827053` failed on the unchanged R6 supplement because scalable T1 fonts were missing. Installing `cm-super` fixed this environment issue. Run `37671715086` then completed every build, but repository ignore rules excluded generated PDFs/logs from its commit and packet. The missing files were detected during independent delivery verification. Run `37673245843` rebuilt the same source, explicitly staged the new artifact directory, asserted that all three PDFs existed in the committed Git tree, and exported the complete packet. Only ordinary non-force ref pushes were used. Both issues are recorded in `ARTIFACT_DELIVERY.json`; neither is represented as a mathematical advance.

## Scope of verification

The rebuilding scope is the complete R11 article, complete retained R10 and R6 texts and their integral covers. It is not every historical paper in the repository. Historical retention is not a new line-by-line audit of v1-v96. The source contains the general proofs; neither regression success, render identity nor Git identity certifies originality, top-four-journal significance or independent mathematical correctness. The unresolved mathematical boundaries are explicit in `SCOPE_AUDIT.md` and the referee response.
