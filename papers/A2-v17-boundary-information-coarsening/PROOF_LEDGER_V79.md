# A2 v79 proof and dependency ledger

This is an author-side map for independent checking, not a proof certificate.
The principal PDF is `rigidity_v79.pdf`; theorem numbers below refer to that file.
The controlling source is recorded in `RESPONSE_TO_REFEREE_V79.md`.

## New chain

| Statement | Written content | Dependencies and nonclaims |
|---|---|---|
| Proposition 4.1, p. 9 | Homeomorphism from the ambient positive-law quotient to anchored log contrasts; complete explicit metric | Positive `C^m` functions on a compact rectangle. No billiard realization assumption or statistical sufficiency kernel. |
| Theorem 4.2, p. 10 | Explicit global split coordinates on an open inverse chart; smooth retraction; no spatial derivative loss | Distinct clocks, a nondegenerate two-point action anchor, positive reciprocal residual. Degenerate constant-action data are outside this chart. |
| Corollary 4.3, p. 11 | Residual comparable to distance from the shared-weight model locally | Bounded smaller/larger chart neighborhoods with margins. Not a global condition-number bound. |
| Theorem 4.4, p. 11 | Controlled misspecification bias and complete exact action-confounding formula | Finite-order product/reciprocal bounds and the split inverse. Extra clocks do not distinguish the explicitly confounded alternatives. |
| Proposition 4.5, p. 12 | Tangent left inverse and complementary nuisance components | Differentiation of the smooth split coordinates; second-order remainder on bounded charts. |
| Proposition 5.1, p. 12 | Residual validation with finite-record type-I and separated-power bounds | A high-probability `C^m` contrast estimate. Does not assert optimal testing separation or physical model realization. |
| Theorem 5.2, pp. 13–14 | Matching expected `C^m` action-risk upper/lower bounds: uniform Hölder rate plus linear misspecification | Explicit nondegenerate class and fixed number of independent samples per clock. Kernel upper bound, bounded measurable fallback, multiple-bump information lower bound, identical-law ambiguity pair. Not billiard minimax. |
| Lemma 10.1, pp. 23–24 | Global exact twist map, unique finite actions, explicit twist lower bound, positive matching Schur complement | Intrinsic two-variable Hessian and negative-twist inequalities. All trajectory and positivity hypotheses are derived on this class. |
| Proposition 10.2, pp. 24–25 | Contact quotient and actual Reeb first-return time | Exact symplectic primitive plus positive roof. Classical construction, attributed and proved to fix signs and observations. |
| Theorem 10.3, pp. 25–27 | Class-fixed six-deadline recovery of unknown `L` on a prescribed square; robust finite-order stability | Backward bounds, convexity, positive roof, fixed release delay, source box and deadlines; clock inverse then physical prefix cancellation. Contact time, not unsuspended ordinary time. |
| Proposition 13.2, pp. 33–34 | Raw-launch success mass with classification and entry costs | No false branch/lift labels; all failed launches counted; actual source normalization. Conditional laws alone do not determine success probabilities. |
| Theorem 13.3, p. 34 | Robust finite-record output is an actual periodic table on the stated event | Fixed bounded reference-atlas neighborhood, true acceptance floor, smooth densities, small recording and sharing errors; original geometric reconstruction is retained. Not a universal billiard acquisition theorem. |

Definition 13.1 specifies the observation/cost convention. Theorem 7.2 strengthens the explicit physical-domain hypothesis of the retained root-selection-free statement; its proof is retained. Section 3 retains the exact quotient, canonical comparison and two-clock ambiguity with corrected topology language. The contact map is not used as an assumption in the proof of the statistical quotient, so there is no circular dependence.

## Retained chain and proof-body preservation

The reviewed principal article has 24 `proof` environments. All 24 bodies occur exactly in the active v79 input graph; v79 has 36 such environments. This checks preservation of text, not the truth of the retained results. All 71 old labels survive among 116 distinct labels, and all four old bibliography keys survive among ten keys.

- Section 2: physical flow-box law, clock design and absolute action inverse.
- Section 3: exact law quotient, canonical graph comparison and two-clock ambiguity.
- Sections 6–7: finite physical branch action, local prefix cancellation, global downward-zero matching and scalar generating-action consequence.
- Section 8: explicit finite distance certificate and overlap/lattice registration.
- Section 9: regular extension, visibility, finite whole-table coverage, persistence and nonanalytic examples.
- Section 11: complete mass/potential theorem on a prescribed interval, including the original proof and conditioning bounds.
- Section 12: explicit geometric margins, corner anchors, reference-uniform stability and constructive finite-record geometric output.

The periodic companion's existing branch files are neither removed nor merged into the principal article. The patch does not modify them. Their full dependency graph was not rebuilt in this local delivery.

## Suggested independent mathematical checks

The most consequential new checks are the global chart inverse in (4.4)–(4.9), the necessity direction of the exact nuisance formula (4.13), the admissibility and normalization in both lower-bound constructions of Theorem 5.2, the sign of the contact deck transformation (10.5), and the uniform phase/deadline bounds in Theorem 10.3. The statistical and contact proofs are separate; neither is evidence for a universal branch-free billiard inverse.
