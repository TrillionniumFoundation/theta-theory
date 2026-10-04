# General Theta Foundations I — Revision 74 referee entry

Controlling v73/r47 report: `fa857238020a0b5f2befd936b39820a9b426390a`; audit: `62ffc56f0911b939f3e6b79ae0a5e38563e5a988`.
Base: completed v73 final head `ab67d30dc8ad190f1e4cea150a306c8ca3a4dc1f`. This revision continues the existing v74 anchor.

Quantitative: `papers/GTF-I-v74-coupled-boundary-geometry/paper.pdf` (46 pages).
Structural: `papers/GTF-I-v74-coupled-boundary-geometry/STRUCTURAL_PAPER.pdf` (41 pages).
Complete research edition: `papers/GTF-I-v74-coupled-boundary-geometry/COMPLETE_REVISION.pdf` (146 pages).

Native source: `82f9f5c9868f7ad5847784bf92109f297ae0b876`.
Builder run: `37172756259`.

New metric: for all unbiased binary qubit measurements, s=min(|x|,|y|) and D=sqrt(N/(1-s²+1/N))|x-y| give (1/256)min(1,D)<=d_N<=min(2,6D). Visibility and direction may both change.
New geometric criterion: a compact k-Ahlfors-regular identifiable subfamily has small-error covering order delta^(-k) integral [N/(1-|x|²+1/N)]^(k/2) dmu. Lower centres are arbitrary legal memoryless instruments; upper centres lie in the family.
Boundary-depth order t^alpha gives a contact trichotomy. The jointly encoded disk has cover order N log(N+2)/delta²; the ball has N²/delta³. These statements retain a fixed small-error cap and explicit geometric hypotheses.
An exact rational codec accepts Cartesian rational inputs with possibly irrational norm. One index charges both visibility and direction. Every word decodes to a legal rational instrument; target replay is a separate check.
All 17 required and 30 detailed r47 comments are mapped. Sedlak–Ziman (2014) and Puchala et al. (2018) are directly compared. Independent human priority and author signing remain external, not fabricated. No change of journal target is made.

New quantitative theorem locations:
- `thm:ballmetric74`: 15.1, page 38.
- `lem:radial74`: 15.2, page 39.
- `thm:weightedcover74`: 15.3, page 40.
- `cor:contact74`: 15.4, page 41.
- `cor:jointball74`: 15.5, page 41.
- `thm:jointcodec74`: 15.6, page 42.
- `rem:jointscope74`: 15.7, page 43.

New exact regression: 2265 assertions; {'algebraic_comparisons': 180, 'binomial': 150, 'codec': 60, 'legal_words': 96, 'monotonicity': 450}; 33 negative controls. Normal/optimized results agree. All ten inherited suites run unchanged.
Preserved: 222 predecessor native files, 502 prior complete-edition labels; current total 522. No unresolved references/citations or overfull/underfull boxes.
Native ZIP and minimal journal package reconstruct independently. CI certifies source/artifact identity, not universal proof, independent priority, authorship or acceptance.
Work branch: `revision/general-theta-foundations-i-v74-coupled-boundary-geometry-2026-10-04`.
Referee alias after exact-head verification: `revision/general-theta-foundations-i-v74-referee-ready-2026-10-04`.
Package hashes: `papers/GTF-I-v74-coupled-boundary-geometry/evidence/PACKAGE_MANIFEST.json`. The final-head attestation remains an external artifact.
