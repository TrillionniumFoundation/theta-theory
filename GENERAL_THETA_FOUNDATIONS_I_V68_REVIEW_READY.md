# General Theta Foundations I — Revision 68 referee entry

Controlling v67/r44 report: `68c69a4a2e8b4e3b11c43a181806ab578584b719`; companion audit: `7a9586cd8cf7995152fbbf501f3e47da4aa89900`.
Base v67 qualified publication: `98a4b12126502ea41c620b58bad4b9aa30f9c72c`. The controlling reports review this exact v67 publication.

Quantitative: `papers/GTF-I-v68-boundary-uniform-coding/paper.pdf` (18 pages).
Structural: `papers/GTF-I-v68-boundary-uniform-coding/STRUCTURAL_PAPER.pdf` (40 pages).
Complete research edition: `papers/GTF-I-v68-boundary-uniform-coding/COMPLETE_REVISION.pdf` (118 pages).

Native source: `9e52ce69cd1270f49249889c85a446f9cdde44ac`.
Builder run: `37111159523`.

Main additions: uniform joint code length (s/2) log2 N+s log2(1/delta)+O(1) on a fixed positive Choi body, and rank-stratified boundary preparation code length (v/2) log2 N+v log2(1/delta)+O(1), v=sum_y r_y(2n-r_y)-1. Remainders are independent of N and delta for N>=1 and 0<delta<=1/32. A rational triangular-factor codec preserves zero outcomes and never increases ranks.
The adaptive bound covers a common tester with quantum memory, initially entangled reference, feedback and bounded public stopping. The preparation family admits an exact product-state reduction, while the general positive-body theorem uses the inherited classical-programme bound. Unitary boundary examples are retained, not contradicted by the restricted preparation theorem.
These are description lower bounds, not general mutable-space lower bounds, channel-learning query bounds, or physical finite-classical-message simulation of unknown quantum input. All inherited spectral, numerical, causal and crossover hypotheses remain.
The response treats all fourteen required r44 items and twenty-four detailed comments. The bibliography compares Naik et al., current channel-learning results, adaptive binary channel discrimination, quantum population compression and the classical-programme metrology antecedent. Independent expert priority clearance is not represented as obtained.

New quantitative locations:
- `lem:binarylocal68`: 6.1, page 12.
- `cor:localchoi68`: 6.2, page 13.
- `thm:jointcode68`: 6.3, page 13.
- `lem:productreplacer68`: 7.1, page 14.
- `thm:factorcode68`: 7.2, page 15.
- `thm:rankentropy68`: 7.3, page 16.
- `cor:fullboundary68`: 7.4, page 17.
- `rem:boundaryscope68`: 7.5, page 17.

New exact regression: 8421 assertions and 35 named negative controls; ordinary and optimized outputs agree. All five inherited suites also execute.
Preserved: 115 predecessor native files and 394 prior complete-edition labels; current complete edition has 419 labels. Zero unresolved references/citations and zero overfull/underfull boxes.
The native source archive rebuilds in isolation and the journal package rebuilds without historical PDFs. These are executed source, arithmetic and typesetting checks, not universal mathematical or independent priority certificates.
No cryptographic author signature, journal acceptance or A/B/C/D analytic aggregate completion is asserted.

Work branch: `revision/general-theta-foundations-i-v68-boundary-uniform-coding-2026-10-03`.
Referee branch, created after exact-head verification: `revision/general-theta-foundations-i-v68-referee-ready-2026-10-03`.
Package digests: `papers/GTF-I-v68-boundary-uniform-coding/evidence/PACKAGE_MANIFEST.json`. The final-head attestation is external to the checked tree.
