# Response to the complete-materialized A2 v153 report — revision 155

## Review object, ancestry, and reading order

The controlling report is `reviews/a2-v153-materialized-independent-harsh-top4-2026-09-25/REFEREE_REPORT.md`, commit `52ebb8183433ad398f61958219b2af809f721824`. It concerns the complete 80-page v153 article. It is not the earlier report on an incomplete source-lock shell. The immediate mathematical predecessor of this revision is the complete v154 at `a3a59510072f8d012f4436807c83c66d1475573d`; its source SHA-256 is `908fa5461d7978f3ee0f7bfbfec16aa5748be191e3486cfb7e73628cc5b062d1`.

We thank the referee for identifying the missing connection between the divisor-fibre algebra and the intrinsic spectral geometry, and for insisting on an actual separation of the manuscript. We have retained the v154 proof repairs and added two general results with full proofs. We have also produced two genuinely separate complete companion papers, not just another contents page for one cumulative submission:

* Paper I, **Finite failure schemes and the reconstruction of quadratic pencils**, contains the sharp unmarked inverse, relative and recognition forms, polarized moduli compatibility, rigidification, covering constructions, and native spectral specialization theory.
* Paper II, **Divisor-incidence fibres and spectral power-zero schemes**, contains divisor normalization, binary collision geometry, reciprocal-fibre algebra, the new exact sections and spectral power-zero theorem, and the full-coordinate-change common boundary application.

References prefixed I or II identify the companion paper; their numerical reference maps are embedded in the complete sources. Each source compiles independently without an external auxiliary file. The mathematical proofs of the inverse in I and the incidence and section results in II are independent. The intrinsic interpretation and pencil applications explicitly use the named results of the other paper. These are companion papers, not a claim that no result in one ever cites the other.

`geometry.pdf` is the full preservation master. It is retained for checking that no previous theorem or proof has disappeared; it is not proposed as the only submission architecture. The local build has 93 pages in the master, 60 in I, and 36 in II. The native `BUILD_RECEIPT_V155.json` is authoritative for the published page counts. Every one of the predecessor's 301 labels and all 207 theorem/lemma/proposition/corollary/definition/example/remark/proof blocks is retained in the master. Every mathematical body block is allocated exactly once across the two companions. The earlier introduction is archived rather than discarded.

## 1. Entire quadratic sections, uniformly in all reciprocal parameters

**Location:** Paper II Theorem 12.1 and Corollary 12.2; master Theorem 20.1 and Corollary 20.2. Stable source labels are `thm:quadratic-section-v155` and `cor:boundary-size-v155`.

For every `g >= k >= 2`, with `d = dim W` and `h = floor(g/2)`, setting all reciprocal coefficients except `Q_2` to zero gives exactly

`F_(g,k)(W)/(coeff Q_i, i != 2) = B_(d,h) = Sym((Sym^2 W)^*)/(coeff Q_2^(h+1))`.

This is an equality of ideals for the entire coefficient section. Unlike the earlier v154 quotient by `coeff Q_2^2`, it does not add an extra quadratic relation when the reciprocal equations permit a higher power. The proof identifies the first even reciprocal index and proves that all later equations specialize into its coefficient ideal.

The section is the apolar algebra of a power of the generic symmetric determinant. Its degree-p representation is the sum of the Schur modules `S_(2 lambda)(W*)` for partitions of p in the rectangle `(h^d)`. The theorem gives the entire Hilbert function, a closed product for its length, its socle representation and degree, and the nilpotence index `hr+1` of every rank-r degree-one element. The determinant-power apolar ideal, representation decomposition and strong Lefschetz theorem are explicitly attributed to Nagaoka–Wachi, arXiv:2403.05492v1, with exact result numbers. The length product is obtained by spelling out the symplectic Weyl factors. These classical results are not represented as newly discovered.

This uniform section yields both a length lower bound and a Loewy-depth lower bound for the original multivariate normalization fibre. For the actual ternary common boundary `F_(6,2)(C^8)`, the section has exact length **922268360**, ordinary socle degree **24**, and reciprocal-weight socle **48**. Therefore the full fibre has at least that length and has nonzero 24th maximal-ideal power. This replaces neither 44 (embedding dimension) nor 9867 (minimal equation count) by another mislabeled invariant. It also does not assert that the original fibre is Gorenstein or that its length equals its section's length. The result is a uniform structural theorem, not extrapolation from the five-variable example.

## 2. Every spectral Fitting scheme inside one reciprocal multiplication algebra

**Location:** Paper II Lemma 13.1, Theorem 13.2 and Corollary 13.4; master Lemma 21.1, Theorem 21.2 and Corollary 21.4. Labels: `lem:power-valuation-v155`, `thm:power-Fitting-v155`, `cor:power-order-v155`.

Given any complex pencil `R in Sym^2 V` and any positive integer h, consider the actual degree-2h normalization fibre over the divisor-incidence point `a^(2h+2)(C a + V*)`. Its quadratic section is `B_(n,h)` and its degree-one space is `Sym^2 V`. Thus one algebra contains the pencil line itself.

Let `J_p` be the ideal of the universal p-th power on that line. We prove, as an equality of coherent ideal sheaves,

`J_(h(n-j)) = Fitt_j(T_R)^h`, for every `0 <= j <= n`.

For h=1 this is an exact equality of the spectral Fitting schemes with power-zero schemes, including their nonreduced multiplicities. This construction does not first compute a Fitting polynomial and then encode it in a separate binary normalization fibre, as in the retained v154 spectral tower. One reciprocal algebra and its embedded pencil line realize all the Fitting ideals simultaneously.

The proof contains a local formula for every power p, not only for multiples of h. After symmetric diagonalization over `C[[t]]`, the coordinate ideal has valuation

`h(e_1 + ... + e_q) + s e_(q+1)`, where `p = hq+s` and `0 <= s < h`.

An apolar injection splits over the ground field, so computing coefficient ideals after that injection is legitimate. Expanding `det(X+zA(t))^h` gives a lower bound on valuations, and a diagonal-X monomial with nonzero binomial coefficient attains it. The proof handles infinite Smith exponents and zero ideals explicitly. Faithfully flat completion then gives the global ideal identity. There is no replacement of a Fitting ideal by its radical.

For a regular pencil the successive local power-zero lengths recover the full Segre symbol together with its common projective support. For singular pencils the same identity recovers normal rank and every spectral Fitting ideal; these ideals alone are not asserted to recover singular minimal indices. The unmarked inverse in Paper I supplies the intrinsic interpretation.

The fixed-spectrum full-orthogonal closure order was already proved in the inherited appendix. We do **not** claim it as a new v155 orbit classification. The new corollary expresses that order as inclusions of power-zero divisors inside this reciprocal model, with finite jet equations for the reduced closure condition. The inherited flat realization by actual finite failure neighbourhoods is retained. Scheme-theoretic reducedness of those jet equations is not asserted.

For families, the algebra and the coefficient ideals commute with arbitrary base change. The equality with powers of Fitting ideals is proved on every complex pencil line and on a regular one-dimensional base by the local proof; equality over arbitrary nonreduced parameter bases is not inferred from geometric fibres. No flatness across length jumps is claimed.

## 3. Response to the 24 numbered requests

| Report item | Present disposition and location |
|---|---|
| 1. Complete-local hypotheses | Retained `lem:complete-local-v154`: locality, continuity, completeness, Noetherian hypotheses and residue field are explicit. |
| 2. Reduced completions | Retained complete-local proof and Stacks citations, with minimal-prime injection. |
| 3. Miracle flatness | Retained `lem:residual-selection-v154`, with the hypotheses and standard reference stated. |
| 4. Residual-member selection and descent | The resultant-open cover, Artin cancellation and unique descent remain in that lemma. |
| 5. Weighted versus maximal-ideal grading | Both are kept distinct throughout. The new section has ordinary degree one and reciprocal weight two; its socle degrees are stated in both conventions. |
| 6. Hensel product argument | Retained `lem:hensel-products-v154` and its square-zero lifting proof. |
| 7. Partition-stratum closure | Retained proper power-map argument and coincident-root literature comparison. |
| 8. Coherent conductor globalization | Retained `lem:equalizer-v154`, with stalkwise coherent ideals and faithful flatness. The same discipline is used in the new power-Fitting theorem. |
| 9. Coordinate equalizer | Retained monomial coefficient proof; it is not extended to arbitrary non-coordinate unions. |
| 10. Hochster citation | Retained explicit Miller–Sturmfels attribution and full block Betti calculation. |
| 11. Skeleton/transversal positioning | Retained; novelty is attached to the geometric incidence identification, not to renaming a classical monomial ring. |
| 12. Atlas is not classification | All three new introductions call it an exact completed incidence atlas, not an analytic classification. |
| 13. Atlas finiteness | Retained `prop:atlas-functor-v154`: integral factor coefficients and monic-division quotient coefficients. |
| 14. Coordinate-independence | Retained represented marked-divisor functor and uniqueness of the whole completed diagram. The new quadratic section explicitly fixes the complement and its equivariance group. |
| 15. Fitting equivariance | Retained the simultaneous `GL_m` action and symmetric-power explanation in the double-root argument. |
| 16. Minimal-relation specialization | Retained the equality of the images of variable-ideal times relation-ideal under the surjective specialization. |
| 17. Equation counts are not geometry | The 44 and 9867 counts remain accurately labeled. The whole-section character, length, socle and power filtration provide distinct invariants and consequences. |
| 18. Higher reciprocal invariants | Uniform full-section Hilbert functions, lengths, Gorenstein duality, Lefschetz and rank-nilpotence statements are added. The full F22 resolution is retained. Whole-fibre and section assertions are separated. |
| 19. Acting groups | Native congruence, fixed-form full orthogonal action and full cotangent `GL(E)` are kept separate. The embedded spectral line is essential; the extreme point alone forgets it. |
| 20. Two-stage specialization | The original theorem and proof remain byte-for-byte; no single universal one-parameter subgroup is claimed. |
| 21. Ballico comparison | Bibliographic metadata and the full-text access limitation remain visible in the articles. No theorem-level comparison has been fabricated. |
| 22. Regression scope | The v154 exact suite, including its four v153 check families, has actually been rerun. The historical 28-check suite has not; receipts retain this explicit distinction. |
| 23. Infrastructure versus narrative | Source locks, hashes, build evidence and nondeletion manifests are repository documents, not mathematical significance claims. |
| 24. Split the submission | Two complete companion manuscripts with separate abstracts, introductions, numbering, resolved companion citations and PDFs are supplied. The preservation master remains an archival comparison object. |

## 4. Verification and remaining scope

`check_v155.py` performs independent rational Groebner checks of eight small section algebras, compares Schur-sum Hilbert functions with the symplectic Weyl product for 24 dimension/power pairs, and checks every relevant power ideal in six DVR examples, including polynomial unimodular congruences and singular matrices. The large section length is independently evaluated by the Schur sum and the product formula. The inherited exact v154 suite is actually executed, not just copied as a prior green receipt.

The native build recompiles all three complete manuscripts, checks that references and citations resolve, rejects overfull horizontal boxes, and records the actual source and PDF hashes. `NONDELETION_V155.json` and `PAPER_MAP_V155.json` record preservation and the exact allocation of mathematical sections. Finite calculations do not certify the universal proofs or determine a journal's editorial decision.

The revision addresses the referee's boundary-detection and reciprocal-algebra directions by a uniform section theorem and a scheme-theoretic power-Fitting identity. It does not assert a conductor formula at every collided multivariate image, the entire Hilbert function of every original reciprocal fibre, classification of every full `GL(E)` orbit closure, or a proper stack compactification. Those stronger assertions do not follow from the results proved here. The reconstruction theorem, including singular pencils and sharp order, is unchanged. The separation into companion papers does not remove any mathematical program from the archived revision.
