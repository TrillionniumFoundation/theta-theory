# Response to the substantive referee on A2-DYN revision 11

**Revised source:** `papers/A2-DYN-v12-referee-response`  
**Controlling report:** `reviews/a2-dyn-v11-substantive-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Review commit:** `fd84da57359a3ad2fefed532b0b5094ab8c6e436`  
**Reviewed author SHA:** `dfacd56110f80a9621671028d2aa0a5782659055`

We thank the referee for the substantive audit. We retain the title, physical family, raw mixed-density endpoint and all theorem-level mathematics of revision 11. This revision responds first to the report's prerequisite: the failed source packet is repaired at a new immutable SHA and requalified from that exact remote source.

## A. Exact source repair and requalification

The referee correctly identified that revision 11's source-preservation assertion was false at the reviewed SHA. The cause was a stray leading character in the inherited `core/06_downstream.tex`. Revision 12 restores that file exactly to the reviewed revision-10 blob `20df3335f2c8e2819e23dc1bfdc70d6f3bc96c4b`.

The two visible TeX defects are also repaired: the malformed `\nef` reference in `main.tex` is replaced by `\ref`, and the stray operator fragment in the marked-event display is removed. The manifest now describes the actual tree rather than asserting blanket identity.

## B. Covariance nondegeneracy

The paper continues to prove a continuous positive-semidefinite covariance and an exact L2 coboundary characterization of its kernel. We agree that the periodic-rank argument cannot be applied to an arbitrary measurable representative. The explicit periodic rank and phase-separation theorems remain in the article as the geometric input for the required periodic-evaluable regularity bridge; no such bridge is silently assumed.

## C. Complementary frequencies

The proved physical central radius remains `n^(-99/200)`. The annulus between that radius and the previously contemplated `n^(-2/5)` regime remains explicit. The complementary-frequency criterion and strict splice inequalities are retained as the next analytic closure step rather than being erased by a change of notation.

## D. Full critical/singular branch sum

All critical-edge calculations and exact jump subtraction are retained. The one-collision BV theorem remains a statement on initial coordinates and is not reused as a second-derivative estimate for many-return inverse-coarea densities. The global residual criterion therefore remains separate.

## E. Weighted and exact-event tails

The single marked-return theorem and same-event conditioning corollary are retained with their precise scope. They concern a bounded-BV function of one actual return state; they do not identify a terminal raw lattice indicator with a collision-state insertion or replace the relative event-replacement estimate required for exact physical conditioning.

## Technical and presentation comments

Theorem C now states its measure normalization locally; the separated `M_a` and `V_a` estimate remains primary; return-state, terminal-state, path and exact physical observation events remain distinguished; the backward-clock endpoint convention is preserved; “terminal insertion” is not used for a raw lattice indicator; the no-induced-mixing warning and both cutoff scales remain explicit; the identity-notice review is not represented as substantive acceptance; publication/proof-certification wording is removed; and the final validation record is tied to the actual exact-SHA workflow result.

Revision 12 therefore keeps the theorem and topic intact while supplying the exact reproducible object required for the next referee round.
