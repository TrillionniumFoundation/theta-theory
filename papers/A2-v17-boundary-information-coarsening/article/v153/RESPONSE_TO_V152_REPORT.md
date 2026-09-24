# Response to the independent report on A2 revision 152

**Controlling report:** `reviews/a2-v152-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md`, commit `60f1a3c5f8078c31019dfab249d334d0e717e225`.

**Revision:** 153. **Article:** *Finite failure schemes and the reconstruction of quadratic pencils*. The submitted scope continues to include all complex quadratic pencils and the sharp unmarked inverse. None of the inherited theorem or proof blocks is removed.

## Principal response: global structure rather than another isolated slice

The report asks for at least one theorem on a natural large class or a structural theorem about the reciprocal fibres. We supply both.

Theorem `thm:squarefree-v153` treats the entire squarefree-common-divisor open set of every binary Grassmannian divisor image, for all admissible ranks and divisor degrees. Its completed local ring is a uniform block monomial ring. It determines all branches and every multiple scheme-theoretic branch intersection, including their smooth dimensions; the conductor is exactly the ideal of the next common-divisor-degree image. The theorem also computes depth, multiplicity, the Cohen--Macaulay cases and seminormality. The formula descends under root permutations and is an equality of global conductor sheaves on that open set. It does not replace a scheme by its reduced support in order to calculate the conductor.

Theorem `thm:binary-fibres-v153` covers every binary exact-gcd stratum, not only the squarefree locus. The finite normalization restricted to gcd degree s is a base change of the finite flat binary factorization morphism of degree binomial(s,g). At every partition of the common roots, its full fibre is a product of tensor products of reciprocal complete intersections. Lengths, weighted Hilbert series, socles and the partition closure order are determined uniformly. Theorem `thm:atlas-v153` supplies the entire formal incidence diagram for arbitrary higher and simultaneous collisions, rather than a test slice. The classical binary reciprocal/Grassmannian ring is explicitly attributed; the geometric base-change theorem and its application to the unframed Grassmannian are distinguished from that classical algebra.

Theorem `thm:reciprocal-structure-v153` treats every pure-power divisor fibre in every number of variables. It proves that the minimal relation module is the direct sum of the full coefficient representations in weights g+1 through g+k. This gives an exact minimal equation count and a complete-intersection classification. The proof uses specialization to the binary regular sequence and irreducibility to prove that no coefficient representation disappears modulo the variable ideal times the relation ideal. The binary and k=1 cases also have explicit lengths and socles. The actual ternary-pencil limit has 44 variables but **9867 minimal equations**, with 3432 and 6435 in its two weighted pieces. This is a structural conclusion about the fibre, not a relabelling of its embedding dimension as its length.

These results do not assert a classification of all multivariate overlaps, all full first-relation orbit closures, or the Segre data of pencils from their common extreme limit. The new global theorem is on the explicitly specified large binary class, and the arbitrary-dimensional theorem concerns the reciprocal fibre algebra. The earlier all-pencil inverse, multivariate split model and common full-orbit degeneration remain in the article.

## Responses to the twenty specific points in Section 10

| Point | Revision and proof location |
|---|---|
| 1. Formal branch lemma | `lem:formal-image-v153` states and proves the finite completed-image formula and the implication from cotangent surjectivity to a closed formal immersion into that image. |
| 2. Completed-image fibre product | The same lemma proves reducedness using excellence, kernel preservation by exact completion, and the two-ideal exact sequence. The coprime Artin intersection is then used, not inferred from tangent dimensions. |
| 3. Separated normalization germs | The product decomposition of the completed finite algebra is obtained from lifted orthogonal idempotents; a local Artin lift remains in its selected component. |
| 4. Positive codimension | `lem:coprime-lifts-v153` proves directly that c is at least (r-1)(s_g-1), hence positive. |
| 5. Binary versality | `thm:atlas-v153` identifies the incidence functor over every Artin base; independent jets, monic division, the full finite image and invariance under frame and root-coordinate changes are all included. |
| 6. General singular ideal | `thm:fitting-v153` evaluates it for all m as (I^(m+1)+Delta I^m) direct-sum I^m t. The proof gives both inclusions and explicit generating minors, rather than leaving the minors unevaluated. |
| 7. Linear power divisor | The inherited common-part proposition now explicitly assumes that a_0 is a nonzero linear form in its final assertion. |
| 8. Reduced versus full intersection | The multivariate common-part formula remains labelled a reduced-support formula. Full binary degree-image intersections and all squarefree multiple branch intersections are separate scheme-theoretic statements. |
| 9. Acting group | The introduction, the definition of the boundary theorem's scope and its title explicitly distinguish full GL(E) first-relation orbits from PGL(V) congruence orbits. |
| 10. Choice dependence | The fixed standard flag, scalar direction and complement are stated. No coordinate-free distinguished point is asserted. The existence and containment theorem is retained. |
| 11. Two stages | The main introduction explicitly records the pencil-to-flag and flag-to-contraction stages; no common one-parameter subgroup for all initial pencils is inferred. |
| 12. Flat relation subbundle | The inherited proof now says that the maximal minors generate the unit ideal in C[tau] and that their principal opens give actual splittings over Spec C[tau]. |
| 13. Coefficient span | The flag-jet proof now cites `lem:pencil-irreducibility` and the nonzero matrix-coefficient inclusion `eq:general-coefficient-map`, rather than an unnamed span assertion. |
| 14. Variables versus equations | The sentence is corrected to “The number of coefficient variables is”. The new theorem gives the genuinely different minimal equation count. |
| 15. Reciprocal invariants | The full minimal relation representation, exact minimal relation count and complete-intersection classification are now proved uniformly. Length and socle are calculated in the binary and k=1 cases; a general multivariate Gorenstein classification is not claimed. |
| 16. Abstract | Rewritten around two packages: sharp unmarked reconstruction and divisor-boundary structure. The list of separate infrastructure programs is removed from the abstract, not from the article. |
| 17. Terminology | The common-point theorem title and introductory language no longer assert a canonical or universal distinguished moduli point. Genuine incidence universal properties retain their precise meaning. |
| 18. Ballico | The documentary limitation is retained in the new main introduction and in the detailed comparison appendix. Full theorem/proof text has not been obtained. This item is **documentary-open**, not marked closed. |
| 19. Computation | All new assertions have written proofs. The new exact script is a consistency check only, and its receipt says explicitly that computation does not certify the universal proofs. |
| 20. Architecture | The complete article is reordered around reconstruction followed by divisor geometry. Detailed original formulations, moving families, recognition, rigidification, coverings and spectral consequences are retained as article appendices. No mathematical block is deleted. |

## Preservation and reproducibility

`assemble_v153.py` verifies every inherited input byte-for-byte against the controlling reviewed Git tree. It checks that each principal part occurs exactly once, allows only recorded textual corrections, preserves every inherited label and theorem/proof block, and produces a self-contained `geometry.tex`. The native v152 directory, applications manuscript, historical archives and reviews remain untouched. `NONDELETION_V153.json` records the exact preservation audit when assembly is run.

`check_v153.py` tests four families over exact rational arithmetic: the block monomial image/conductor ideals; binary reciprocal Hilbert series, lengths and socles, including cluster length sums; evaluated Fitting minors; and multivariate reciprocal minimality. `EXACT_CHECKS_V153.json` records actual execution and hashes. The old receipt's 28 scripts are not represented as rerun by this revision. `BUILD_RECEIPT_V153.json` is generated only after an actual successful full-article build and reference audit.

## Literature and remaining scope

The binary reciprocal presentation is classical. Grinberg, *A basis for a quotient of symmetric polynomials*, arXiv:1910.00207, version of September 24, 2021, Theorem 2.7, provides a primary algebraic Schur-basis comparison. The existing comparisons with Chipalkatti, Kurmann, Hu--Lin--Shao, Ferrand and AOV are preserved. Ballico 1993 remains unavailable at complete theorem/proof level; neither anticipation nor nonanticipation is inferred from metadata or an access failure. No exhaustive historical-priority certification or journal-acceptance claim accompanies this revision.
