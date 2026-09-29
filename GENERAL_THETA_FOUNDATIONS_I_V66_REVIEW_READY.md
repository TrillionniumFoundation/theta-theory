# General Theta Foundations I — Revision 66 referee entry

Quantitative: `papers/GTF-I-v66-reference-stable-instruments/paper.pdf` (58 pages).
Structural: `papers/GTF-I-v66-reference-stable-instruments/STRUCTURAL_PAPER.pdf` (40 pages).
Complete research edition: `papers/GTF-I-v66-reference-stable-instruments/COMPLETE_REVISION.pdf` (105 pages).

Native source: `3050a45908c5de2858fe578b9383e17ca43b7d74`.
Builder run: `36546520706`.

Controlling v65/r42 report: `5c0796bc1f0ea24d379dfd28888f16d88315a525`; companion audit: `b5d71e67b879f9ada861993caedf8151734f85ba`. Base v65 final head: `34e5719ce5c7109c8c31f98079716b8ce6dcfffe`.

New results: explicit positive, trace-preserving rational Choi rounding with diamond error at most `6 m n^2 d^2 (1+mn)/B`; additive error under a common adaptive quantum tester with arbitrary entangled reference and bounded public stopping; posterior tail control; and a single numerical trajectory program with variable rational Choi input and explicit dimension/input bit costs.
The diamond theorem compares genuine instrument descriptions. It does not claim that a classical program physically implements an instrument on unknown quantum inputs. Numerical trajectories have a separate charged input and joint dimension. Inherited spectral lower bounds retain fixed-program and matrix-output assumptions.
All prior complete-edition proofs remain. Duplicated constructive sections are relocated from the focused structural article into the quantitative article and complete edition. The r42 claim that the trace-completed diagonal can leave [0,1] is corrected for promised density inputs; a matrix can still be indefinite through off-diagonal entries.

New quantitative theorem locations:
- `lem:choidiamond66`: 19.1, page 44.
- `thm:choiround66`: 19.2, page 45.
- `cor:instrumentnet66`: 19.3, page 46.
- `thm:adaptivediamond66`: 19.4, page 46.
- `prop:posterior66`: 19.5, page 47.
- `lem:choitrajectory66`: 20.1, page 47.
- `thm:uniformchoi66`: 20.2, page 48.
- `cor:jointsimulation66`: 20.3, page 49.
- `rem:diagonal66`: 15.3, page 39.

Exact new regression: 4853 assertions; 36 named negative controls. Ordinary and optimized results agree. Inherited v65/v64/v63 suites also execute.
Preserved predecessor: 85 native files and 347 mathematical labels. Current complete edition: 368 active labels.
The response maps all 14 required revisions and 24 detailed r42 comments. The literature comparison credits projected least-squares Choi positivity repair, positive quantum filtering, classical diamond hybrid bounds, and strategy norms.
Independent priority clearance, cryptographic author signing, journal acceptance, general noisy transcript-only lower bounds and whole A/B/C/D analytic closure are not asserted. Finite tests do not certify universal mathematics or imported full-action gaps.

Work branch: `revision/general-theta-foundations-i-v66-reference-stable-instruments-2026-09-29`.
Referee alias after final-head qualification: `revision/general-theta-foundations-i-v66-referee-ready-2026-09-29`.
Package hashes: `evidence/PACKAGE_MANIFEST.json`. Final-head attestation is external to the checked tree.
