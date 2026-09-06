# Reference and contribution audit — A1 v8

Primary sources were checked on 6 September 2026. This is a targeted comparison and dependency check, not an exhaustive priority certification.

**Batenkov–Diederichs–Goldman–Yomdin.** *The spectral properties of Vandermonde matrices with clustered nodes*, arXiv:1909.01927v2, printed page 6, Theorems 2.2–2.3 and Corollary 2.1. Their Fourier/Vandermonde node clusters have multiplicity-dependent spectral scales, with N^(1/2)(Nh)^(j−1) in the single-cluster theorem. The introduction explicitly credits this hierarchy. The additional assertions here concern attainable normalized posterior geometry, acquisition evidence, dimension-truncated global entropy, and causal finite-state compression; no identical-prior-work or universal priority claim is made.

**de Boor.** *Divided differences*, Surveys in Approximation Theory 1 (2005), 46–69, arXiv:math/0502036. The Genocchi–Hermite formula (52), printed page 64, is the classical divided-difference input already credited by v7.

**Yomdin–Comte.** *Tame Geometry with Application in Smooth Analysis*, Lecture Notes in Mathematics 1834, Springer, 2004, Theorem 3.5. The real entropy inequality used in `lem:tame-rectangle` is explicitly stated. Its formulation and attribution were cross-checked in the primary paper below; this is not a claim that the entire monograph was read.

**Comte–Halupczok.** *Motivic Vitushkin invariants*, arXiv:2206.15412v2, introduction equations (4)–(5), printed pages 3–4. These recall classical real variations as affine-section component integrals and their metric-entropy bound. Only those recalled real facts are used; the paper's new nonarchimedean theory is not used as if it were a real theorem.

**Zhang–Kileel.** *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, arXiv:2311.05116, Lemma 2.18. Bounded-format real semialgebraic sets have coefficient-independent section component bounds. We do not substitute its isotropic covering theorem for an unproved anisotropic bound: the latter is derived explicitly from real variations and projected-box volumes.

**Subramanian–Sinha–Seraj–Mahajan.** JMLR 23(12) (2022), 1–83. Approximate recursive information states and policy-loss transfer are the appropriate broad context. The exact ticket score identity is not counted as a new general transfer principle or an optimal-exploration theorem.

**V7 referee technical note.** `reviews/a1-english-v7-2026-09-06/TECHNICAL_NOTE.md` at `72eb41e358bd9af122367fea66d0de9bdda07456`. The necessary-budget deduction and seven-trial ambient/attainable boundary are credited to that note. It did not claim the uniform seven-trial law or the general flag truncation proved in v8.
