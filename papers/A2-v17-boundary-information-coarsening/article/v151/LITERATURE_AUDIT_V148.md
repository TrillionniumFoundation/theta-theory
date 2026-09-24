# A2 v148 literature audit — 24 September 2026

## Newly inspected primary source: the algebraic-group quotient

J. S. Milne, *Algebraic Groups: The Theory of Group Schemes of Finite Type over a Field*, Cambridge Studies in Advanced Mathematics 170, Cambridge University Press, 2017.

Author-hosted full text: https://www.jmilne.org/math/Books/iAG2017.pdf

The full PDF parsed successfully. PDF page 120 (zero-based index 119), printed page 108, was rendered and inspected. Theorem 5.39 states the homomorphism theorem: an algebraic-group homomorphism factors through a faithfully flat quotient and a closed immersion. Its proof uses the quotient by the kernel. Remark 5.42 identifies the image as the least algebraic subgroup through which the map factors. These are used explicitly in the proof of `thm:exact-coefficient-stabilizer-v148`. A subsequent screenshot request for zero-based page 120 failed with a cache error; no content from that failed request is asserted as inspected.

This supplements, rather than replaces, the inherited characteristic-zero smoothness reference to Stacks Project Lemma 39.8.2 (Cartier). Equality of complex points alone is not used as a substitute for equality of nonreduced subgroup schemes.

## Ballico 1993: fresh retrieval attempts and the unresolved comparison

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Mathematische Nachrichten 163 (1993), 5–13. DOI: 10.1002/mana.19931630102.

Fresh primary-source metadata:
https://onlinelibrary.wiley.com/toc/15222616/1993/163/1

The searchable publisher issue record exposes the exact title, author, pages 5–13, year 1993, and first-page/PDF entries. It does not supply the theorem/proof text. Opening the issue page directly returned an access failure in the retrieval tool.

Fresh attempted full-text endpoints:

* https://onlinelibrary.wiley.com/doi/pdf/10.1002/mana.19931630102
* https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/mana.19931630102

Neither endpoint returned readable full text. Exact-title/author, title/institutional-repository, and DOI searches did not yield a usable legitimate complete copy. Search hits for unrelated articles were not treated as evidence. No paid acquisition, authenticated library login, author contact, or document-delivery order was performed or claimed.

The previous revision records inspection of the publisher's opening-page image. That record is preserved in `history/v147-root/LITERATURE_AUDIT_V147.md`; it is inherited evidence, not a claim of a newly obtained complete article.

### Six-axis comparison ledger

| Axis | This manuscript | Ballico 1993 theorem/proof-level status |
|---|---|---|
| Underlying objects | All quadratic pencils and their cube-zero multiplication algebras | Unverified beyond the inherited opening-page record |
| Failure scheme structure | Fitting/maximal-minor structure and its nonreduced first relation | Unverified |
| Infinitesimal order | Uniform d=n²+2n−4; lower orders independent | Unverified |
| Relative hypotheses | Smooth projective reduced bases for the unmarked inverse; arbitrary marked complex base change separately | Unverified |
| Isomorphism data | Abstract scheme or ungraded local algebra; no ambient/tensor marking | Unverified |
| Inverse conclusion | Coefficient orbit, actual source bundle and moving pencil; covering equivalence and exact ambiguity | Unverified |

**Result:** no anticipation or nonanticipation judgment can be justified from the material obtained. This item remains documentary-open. New proofs and regression checks do not change that status.

## Classical ingredients and the boundary of the new claims

The Cauchy formula and complete reducibility identify invariant subspaces after a tensor decomposition is recovered; the v147 Cheng–Wang reference is retained. No new theorem of representation theory is claimed. The determinant/Segre preserver argument and Marcus–Moyls reference are retained with their full in-paper proof. The commutant descent is proved in the paper and uses an actual tensor-bundle map, not just projective-bundle data. The projective-to-linear distinction is also explicit in the new full-support global proposition.

The new recognition theorem addresses the image of the determinantal coefficient construction, the exact number of admissible orientations, and the unrestricted linear stabilizer. It is not a classification of every homogeneous ideal. The new covering theorem addresses morphisms P¹→P¹ modulo independent projective transformations; it is not a statement about covers of arbitrary curves or a full deformation-stack equivalence.

## Inherited audits used, without pretending a new full-text inspection

The Elias–Rossi short and compressed Gorenstein comparisons, Marcus–Moyls precise rank-one theorem, Stacks Cartier statement, Ballico 1996 comparison, and Ohta/spectral references remain in the preserved v147 sources and audits. Their prior retrieval and comparison records are not recreated or re-dated as new work. The corresponding proofs and citations remain in the principal manuscript where applicable.

## Evidence boundary

The build receipt separately records source hashes, executed exact regressions, compilation and preservation. It explicitly sets mathematical proof certification by computation, historical priority certification, Ballico-1993 full-text completion and journal acceptance to false. Those flags are not a withdrawal of the mathematical claims: they distinguish written proofs submitted to scrutiny from engineering and documentary evidence.
