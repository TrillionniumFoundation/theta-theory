# General Theta Foundations I — Revision 72 referee entry

Controlling v71/r46 report: `b78c1dddd41de645edf207bc415406b3fc1b5e83`; audit: `43e6713de2aa65f65e649df7cd90e2a95fc83a06`.
Base: completed v71 final head `8c053f4820da3abcbb04daab628aa94379fd01e3`. The existing incomplete v72 work anchor was continued, not treated as a prior verified publication.

Quantitative: `papers/GTF-I-v72-varying-readout/paper.pdf` (35 pages).
Structural: `papers/GTF-I-v72-varying-readout/STRUCTURAL_PAPER.pdf` (40 pages).
Complete research edition: `papers/GTF-I-v72-varying-readout/COMPLETE_REVISION.pdf` (136 pages).

Native source: `f9ced3761b5c0497dfe5ec363126a393b6641e6e`.
Builder run: `37139560991`.

Main theorem: observable varying projective readout has joint description length (b+V/2)log2N+(b+V)log2(1/delta)+O(1), with b=d^2-d and V=sum_x(sum_y r_xy(2n-r_xy)-1), at fixed dimensions/ranks, N>=1 and 0<delta<=1/32.
The direct rational projector codec uses bounded pivoted triangular coordinates, not normalized algebraic eigenvectors or exhaustive unitary search. Upper centres preserve conditional zeros and ranks; the lower cover permits arbitrary legal memoryless centres.
Uniform ambient-domain environment seizing transfers family covering numbers exactly, including arbitrary centres. The inherited full submaximal-error rank-state law yields a Pauli/Bell coding corollary. Centre retraction itself may increase Choi rank.
The imported measurement-discrimination and environment-state principles are cited separately from the new family-covering and coding arguments. Readout must remain observable or be recovered by fixed orthogonal output supports.
All sixteen required and twenty-six detailed r46 comments are mapped in RESPONSE_TO_REFEREE.md. No independent priority opinion, author signature or journal acceptance is claimed. Every analytic A/B/C/D aggregate flag remains false.

New quantitative locations:
- `thm:readoutentropy72`: 12.1, page 28.
- `lem:readoutmodulus72`: 12.2, page 28.
- `lem:readoutmetric72`: 12.3, page 29.
- `lem:flagatlas72`: 12.4, page 29.
- `cor:observablereadout72`: 12.5, page 31.
- `rem:unflagged72`: 12.6, page 31.
- `thm:seizablecover72`: 13.1, page 31.
- `cor:paulicoding72`: 13.2, page 32.

New exact regression: 1462 assertions; 150 chart cases; 44 codec cases; 28 negative controls. Normal and optimized outputs agree. All eight inherited suites execute unchanged.
Preserved: 176 predecessor native files and 460 prior complete-edition labels; current complete edition has 482 labels. Zero unresolved references/citations and zero overfull/underfull boxes.
The native archive and minimal journal package rebuild independently without historical PDFs. Finite regression, written proof, source identity, independent priority and acceptance remain distinct assertions.
Work branch: `revision/general-theta-foundations-i-v72-varying-readout-2026-10-03`.
Referee branch after exact-head reconstruction: `revision/general-theta-foundations-i-v72-referee-ready-2026-10-03`.
Package hashes: `papers/GTF-I-v72-varying-readout/evidence/PACKAGE_MANIFEST.json`. Final-head attestation remains external.
