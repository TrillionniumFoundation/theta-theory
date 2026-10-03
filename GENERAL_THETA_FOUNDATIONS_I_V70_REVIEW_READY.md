# General Theta Foundations I — Revision 70 referee entry

Controlling v68/r45 report: `e862e5c963ef36b9caa3b1b814b495ae4428a088`; companion audit: `a3fd5b80549a855c46151fd7183b3fc7139abac7`.
Mathematical base: completed v68 head `d9d8c464282157485813041d181e909e648b1f4f`. The preserved v69 continuation is an anchor, not a theorem premise.

Quantitative: `papers/GTF-I-v70-coherent-boundary-coding/paper.pdf` (24 pages).
Structural: `papers/GTF-I-v70-coherent-boundary-coding/STRUCTURAL_PAPER.pdf` (40 pages).
Complete research edition: `papers/GTF-I-v70-coherent-boundary-coding/COMPLETE_REVISION.pdf` (124 pages).

Native source: `33da5258148daac2687879c6d761a590d838189c`.
Builder run: `37120436191`.

New main result: for F_(U,sigma),y(X)=U X U* tensor sigma_y, let u=d^2-1 and v=sum r_y(2n-r_y)-1. The optimal reusable description length is (u+v/2)log2N+(u+v)log2(1/delta)+O(1), uniformly for N>=1 and 0<delta<=1/32 at fixed dimensions/ranks. The converse permits all legal memoryless centres; rational upper centres retain zero outcomes and do not increase preparation ranks.
The family retains coherent data and permits singular support-changing preparation blocks. Outcome probabilities are input independent; the theorem is not a classification of all disturbing-instrument directions. The metric includes common adaptive quantum testers, references, feedback and bounded public stopping.
A separate exact preparation-centre retraction C -> R_(C(I/d)) is valid at every positive covering radius and may increase centre rank. It does not prove the full-error coding-law proposal in the v69 anchor.
A general-d rational unitary atlas with d^2-1 digits and an exact finite search encoder is proved and implemented. The direct qubit codec uses three stereographic quaternion digits and the inherited preparation factor codec. It uses exact rational arithmetic and a valid triangle-error certificate.
The response addresses fourteen required and twenty-four detailed r45 comments and directly compares Cooney–Mosonyi–Wilde and classical unitary-discrimination antecedents. Independent priority review is not represented as obtained. All earlier mathematical results and analytic status flags remain.

New quantitative locations:
- `thm:retraction70`: 8.1, page 18.
- `thm:coherententropy70`: 9.1, page 19.
- `lem:coherentmetric70`: 9.2, page 20.
- `lem:unitaryatlas70`: 9.3, page 21.
- `cor:qubitcodec70`: 9.4, page 22.

New exact regression: 4712 assertions and 25 named negative controls; ordinary and optimized outputs agree. All six inherited suites also execute.
Preserved: 136 predecessor native files and 419 prior complete-edition labels; current complete edition has 438 labels. Zero unresolved references/citations and zero overfull/underfull boxes.
The native source archive rebuilds in isolation and the journal package rebuilds without historical PDFs. These are executed source, arithmetic and typesetting checks, not universal mathematical or independent priority certificates.
No cryptographic author signature, journal acceptance or A/B/C/D analytic aggregate completion is asserted.

Work branch: `revision/general-theta-foundations-i-v70-coherent-boundary-coding-2026-10-03`.
Referee branch, created after exact-head verification: `revision/general-theta-foundations-i-v70-referee-ready-2026-10-03`.
Package digests: `papers/GTF-I-v70-coherent-boundary-coding/evidence/PACKAGE_MANIFEST.json`. The final-head attestation is external to the checked tree.
