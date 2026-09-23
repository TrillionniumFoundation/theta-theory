# Response to the controlling v137 referee report — A2 revision 140

Manuscript: *Intrinsic reconstruction from nonreduced failure schemes*.
Controlling report: `reviews/a2-v137-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md`, commit `ba24a0b2d062897ee2d7a6b02add81c504fe0e71`.
Revision base: v139 transport at `4ebf4fbf7c07b72d80429aa23d38b290ac731150`; its complete v138 predecessor is pinned at `cf4925b91608b806580bc0cd4fd8ce2441870c08`.

We thank the referee for distinguishing the repaired structural proofs from the remaining requirements concerning natural geometry, precise attribution and external consequences. The smooth-web theorem, the all-ranks contraction theorem, the all-pencil theorem and the sharp finite-neighbourhood theorem are retained with their hypotheses and conclusions. No negative novelty conclusion is inferred from an incomplete source search.

## The mathematical addition in this revision

Section `sec:spectral-specialization` proves three results in the original quadratic multiplication construction.

1. **The full spectral torsion sheaf is reconstructed at the first relation.** Theorem `thm:spectral-finite-torelli` identifies the isomorphism class of the sheaf cokernel on the natural parameter line from the unmarked order-d neighbourhood. Its proof includes the precise converse from a torsion-module isomorphism to symmetric congruence, using a polynomial square root in the commutant. The lengths modulo successive powers of the local maximal ideal recover each elementary-divisor exponent.
2. **Fixed discriminant and fixed reduced rank data do not suffice, even in a flat family.** Theorem `thm:rank-preserving-specialization` constructs a polynomial family for every n >= 4 with the same full discriminant and the same corank at every point of the marked parameter line. The partition at the multiplicity-four root is (3,1) off the origin and (2,2) at the origin. All reduced determinantal loci agree, not merely the determinant hypersurface. The order-d neighbourhoods distinguish the fibres and form a flat projective family; all lower orders form constant families. The proof gives a fixed complement to the relation planes and then glues the degree-d relation subbundle. It does not assume flatness of the unrestricted failure schemes.
3. **An external geometric difference is explicit.** Corollary `cor:reciprocal-conic-line` computes the reciprocal curve directly: in dimension four it is a smooth plane conic off the origin and a line at the origin. The distinguishing order is exactly 20. Reciprocal curves and their Segre strata are an independently studied part of pencil geometry, rather than an invariant introduced just for this construction.

The old same-discriminant example is not removed. The new example strengthens it: the old pair had different pointwise ranks, while the new family has identical pointwise ranks. The old polar construction also remains, but no longer bears the burden of the natural-family application.

## B137.1 — Ballico 1993, six-axis comparison

The full article has not been obtained. The publisher table of contents confirms the title, journal, volume and pages 5–13; the available direct-PDF request did not return the article. The six-axis matrix is retained in `LITERATURE_AUDIT_V140.md`, with all assertions about the unread theorem text marked unverified. The manuscript does not assert that Ballico anticipated the theorem or that its results exclude anticipation. The new proof is not offered as a substitute for this documentary comparison. This item remains open for novelty assessment, not as an algebraic hypothesis or a reason to retract proved statements.

## B137.2 — A natural second family, rather than a coefficient-encoded block

The original generating-plane multiplication map for Hilbert function (1,n,N−2) supplies the entire family. The v138 all-pencil theorem is retained; v139 sharp order and parameter immersion are retained. The new spectral degeneration lives on the usual Grassmannian of symmetric pencils, within fixed-discriminant and fixed-reduced-rank data. The polynomial formulas, the actual flat family of finite neighbourhoods, and the reciprocal-curve calculation supply a concrete moduli application. No artificial block is inserted into the multiplication matrix.

## B137.3 — From a criterion to an automatically verified family

Theorem `thm:automatic-quadratic-coefficients` proves the coefficient hypotheses for the full range 1 <= r < N−n; this proof is unchanged. For r=2 the irreducibility of the exterior power gives the full pencil, including singular pencils. Theorem `thm:finite-parameter-immersion` remains the scheme-theoretic closed immersion on the entire Grassmannian, compatible with arbitrary complex base change in fixed tensor coordinates. The new flatness argument pulls back that subbundle and checks its descent across tautological frames. It does not confuse marked families with an equivalence of unmarked moduli stacks.

## B137.4 — A specified external significance statement

The paper now proves an explicit statement about established Segre strata and reciprocal curves: a flat family of intrinsic finite multiplication-failure neighbourhoods separates regular pencils even while the full discriminant and every reduced rank degeneracy locus remain fixed, and detects a conic-to-line change of reciprocal geometry. This statement is proved directly and announced in the introduction. Classical pencil classification, torsion-module invariants, and reciprocal curves are credited to their existing literature. We do not claim the first classification of pencils, a resolution of an undocumented open problem, or a journal-issued significance judgment.

## B137.5 — Map-specific novelty audit of the contraction theorem

The complete v138 operator-signature comparison, including Howe's harmonic branching, Olive's transvectants, the distinction between apolar and exterior contractions, the singular-rank kernels and the even-dimensional exception, is retained byte-for-byte. Its primary-source locations are inherited as documented in that audit, not claimed as newly reread here. The new spectral theorem is not used to certify an exhaustive priority search for the contraction theorem. The all-dimensional formula and its complete proofs remain intact; the report's request for broader expert comparison is expressly carried into the next review.

## Section 7 — Local proof clarifications

The v138–v139 repairs are retained: full polarization in the relative rank-one Fano tangent calculation, the implication from compact-real irreducibility to complex-group irreducibility, and the displayed polar block matrix. Reduced-support identities are not upgraded to ideal identities. In the new degeneration we explicitly display the distinction: the local three-row-minor gcd changes from z to z^2 although both radicals equal (z).

## Sections 8–10 — Presentation and preservation

The principal article contains the inverse theorems, their proofs and the new spectral application. Boundary-primary calculations and the full earlier development remain in the source-independent supplement and complete compilation. The article does not carry the response history as a mathematical argument. All 326 inherited labels are required to remain in the complete compilation. Changed predecessor inputs are archived exactly under `history/v139/`; unchanged mathematical files are SHA-256 checked. The actual counts and PDF pages are recorded only after execution in `evidence/BUILD_RECEIPT_V140.json`.

## Evidence and its limits

Fifteen scripts are executed: fourteen inherited scripts and the new exact symbolic specialization audit over Q(i)(t). The new audit verifies the full parameter identities, rank factorization, complementary subspace, power identities, determinant, all determinantal divisors for the four-dimensional block, and the inverse formula. It also checks spectator extensions in dimensions 4–8. These checks support the displayed formulas; they do not constitute a formal proof of the global all-dimensional theorems. LaTeX builds, label/source preservation and PDF checks are reported separately from mathematical and historical judgments.
