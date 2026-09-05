# Response to the English-v2 referee — A1 revision 3.0

Controlling report: `reviews/a1-english-v2-2026-09-05/REFEREE_REPORT.md`, at commit `40be02de7479712d866a575c4b0b9ec930699282` on `review/a1-english-v2-harsh-referee-2026-09-05`. The report and its frozen source are unchanged. This response concerns the new principal manuscript `papers/A1-english-v3/main.tex` and the complete corrected foundation under `foundations/`.

## 1. The contribution objection is answered by a stronger theorem

We agree that adjoining classical entropy, an array of all future tests and a generic Bellman statement to a one-collision formula was not the integrated result the paper needed. The revised Theorem 1.1 has new substantive model content. It follows the referee's positive routes of a verified apparatus/realizability/control family and a genuine finite-budget state reduction, together rather than as unrelated examples.

**One counted mechanical experiment.** Section 2 prepares all placement coordinates, launch angles and apparatus seeds independently of the unknown radius. A physical placement guard produces a failure record when insertion is blocked. Every attempt is charged. Collision-coordinate readout uses an explicit inverse-CDF map driven by a prepared uniform coordinate; the map uses the measured impact coordinate, not an oracle value of the radius. The whole collision tube is integrated with no deleted positive-mass grazing strip. Proposition 2.1 calculates all raw densities and their positive coefficient margins.

**An exact realizable family.** Theorem 3.1 gives a necessary and sufficient condition for the whole radius-indexed accepted family: its ratio to the raw density must be one common radius-independent gate. The complementary failure probability is part of the instrument. The proof constructs the comparator and proves chronological composition from the product cartridge preparation. It does not assume mixing of a single billiard trajectory. Bounded-source tilts and capped failure/cost formulas are derived for this same apparatus.

**A genuinely reduced state, and a matching lower bound.** Theorem 4.1 retains the complete unknown-radius likelihood in `3n+1` positive Bernstein coefficients after n charged attempts, with a four-term positive convolution per output coefficient. A uniform prior gives an explicit beta mixture. Theorem 4.2 proves a general positive-polynomial/rational closure result by uniform degree elevation. Theorem 4.3 proves that the `3n` free coordinates are sharp for a continuous exact likelihood state of the full command family: attainable failure cubics contain an open four-dimensional set; products of pairwise coprime cubic factors have rank `3n+1`; normalized likelihoods have local dimension `3n`. This is not a count of formal coordinates and not an assertion about a single fixed policy or a minimal linear predictive rank.

**Attained control, not merely a formal recursion.** Lemma 5.1 constructs the exact five-dimensional gate moment body and its support function. Theorem 5.2 proves continuous values, compact maximization, Borel gate realization, and equality with optimization over full-history policies. Four moments determine a censored likelihood; the fifth coordinate is the current accepted continuation integral. The selected body point is implemented by an actual gate, not substituted for the full instrument. Finite interval gates and finite command menus approach the ideal optimum uniformly at each fixed budget. This is a proved positive implementation approximation, not a claim of polynomial-time global optimization.

**No artificial acceptance floor.** Theorem 5.3 extends all these conclusions to every Borel gate `0 <= g <= 1`. For a possible failure, each failure coefficient lies between `h_* s(g)` and `H_* s(g)`, where `s(g)=integral(1-g)dnu`; normalizing removes the potentially tiny probability. At a zero-probability branch the posterior need not be continuous, but its probability-weighted Bellman contribution converges to zero. This proves the continuity actually required for attainment on the closed gate class.

The one-flight hypothesis verifies the polynomial kernel; it is not rebranded as a theorem about an uninterrupted many-collision orbit. The old whole-equilibrium response construction remains in the complete companion. The new main result is the positive operational and sharp finite-budget inference/control theorem. No negative conclusion about the broader research program is used as a replacement for this result.

## 2. M1 — retain the biased objective

**Revised source:** principal Proposition A.1, `sections/A_scope_repairs.tex`, label `prop:biased`; companion Proposition 4.4, `foundations/sections/04_selection.tex`, label `prop:constraints`.

For `Q^{xi,B}=exp(xi.C+B)P/Z` with the required mean c, the corrected identity is

`D(Q||P) - QB = D(Q||Q^{xi,B}) + xi.c - log Z`.

The optimizer minimizes `D(Q||P)-QB`. Bare entropy is recovered by explicitly setting B=0 or assuming QB is constant throughout the constraint class. The proof retains B, handles infinite entropy by subtracting only bounded quantities, and gives uniqueness. The event-conditioning result is retained separately. The referee's two-point example is preserved as a diagnostic and stated in the text; it is not treated as a refutation of the corrected biased problem.

## 3. M2 — retain both physical density traces

**Revised source:** principal Theorem A.2, label `thm:two-trace`; companion Theorem 12.2, `foundations/sections/12_response.tex`, label `thm:shape`.

The interface contribution is now

`integral_Sigma v_Sigma [rho_- exp(V_-) F_- - rho_+ exp(V_+) F_+] dS`.

Both density traces appear in the statement and in the transported-domain proof. Branchwise bulk derivatives and the derivative of the normalizer are retained. A common density can be factored only when its traces agree. Fixed external boundary support and moving external fluxes are distinguished. The compactly supported bump example gives the required negative derivative. The whole-equilibrium theorem's ambient smooth density remains a common-trace special case; that result is not weakened.

## 4. M3 — separate smooth trajectories from smooth preparation

**Revised source:** principal Theorem A.3, label `thm:transport-prep`; companion Theorem 13.3, `foundations/sections/13_hybrid.tex`, label `thm:chamber`.

The trajectory conclusion is proved jointly in the physical parameter and initial state using the variational ODE, implicit event equation, reset and comparison-time correction. Integrated response uses either a fixed finite measure or explicitly

`mu_a = Z_a^{-1} (X_a)_#(w_a lambda)`.

The source measure lambda is fixed, weights/transports are jointly measurable and C^r almost everywhere in the parameter, the normalizer stays positive, and every required derivative product has a common integrable envelope. The proof retains weight, transport, observable and normalizer derivatives. The negative-Sobolev conclusion uses weighted Dirac jets with `s>d/2+r`. The cusp weights are excluded by these preparation hypotheses, not by pretending identity dynamics are nonsmooth. The cartridge model separately uses a fixed ambient preparation and exact moving-guard integration.

## 5. S1 — the same nontrivial detector is used throughout

Section 2.4 explicitly retains the referee's separation: the complete collision record recovers R on its hit tag, hence has infinite relative entropies between different radii. No total-variation score is inferred from negative-Sobolev response. The no-collision overlap means we do not assert mutual singularity of the entire laws.

The operational detector is a different, fully specified push-forward. Proposition 2.1 proves its density rather than assuming a Gaussian or an unrelated sensor. Section 6 differentiates this exact raw/gated kernel. Theorem 6.1 proves common-support likelihood response and quadratic-mean differentiability for each fixed adaptive controller, including gates with endpoints 0 and 1. Its proof uses bounded relative derivatives, not a false positive density floor on impossible outcomes. The censoring score is `f'/f` on the possible failure branch and is not discarded. The collision-coordinate mark has an explicit strictly positive information gain over the same placement and collision flags when epsilon>0.

An optimizer may switch as the radius changes. We therefore prove continuity/attainment of the optimized value and derivatives of fixed controllers, without confusing these different assertions.

## 6. Historical derivations and literature comparison

Appendix B and `HISTORICAL_DERIVATION_MAP.md` state exactly what was consulted and reused. The local exact branch primitive and canonical-pointer mechanism are checked directly. Historical global quotient, conormal, spectral, renewal and central-limit claims are not imported through a PASS label. The complete reviewed foundation is preserved as a corrected source companion instead of being silently dropped.

Section 1.2 credits classical billiard flux, predictive representations, moment-body support functions, adaptive censoring and partially observed control. The candidate contribution is the explicit joint mechanical likelihood algebra, sharp finite-budget state and attained realizable control theorem with these verified model inputs. This is a targeted comparison, not a certification of exhaustive priority or journal suitability.

## 7. Publication and actual validation

The new branch stores ordinary `main.tex`, all inputs, the complete corrected foundation, response, proof map and executable checks. It does not depend on a publication workflow extracting an orphan Git tree. The controlling review and previous branches are not overwritten.

The original referee program is reused byte-for-byte (Git blob `6944dc95538e69029e435d1094e11fca756cce6a`) and its 12 diagnostics were rerun. The new program ran 27 diagnostics. All 39 passed. Checks include exact identities, positive coefficient updates, failure posteriors, finite-order rank diagnostics for the dimension proof, a finite two-step policy enumeration, boundary gates, and independent ambient line–circle sampling with recorded seeds. Finite rank tests are not the all-n proof; that proof is in Theorem 4.3. Finite policy enumeration is not a numerical solution of the entire continuous command problem.

The principal manuscript was compiled with three LaTeX passes: 22 pages, 13 proof-bearing entries, no duplicate/missing source labels and no unresolved overfull/undefined-reference diagnostics. All 22 pages were rendered and inspected for layout. The corrected foundation companion was not compiled in this execution; its old validation material is explicitly historical. The historical eleven-paper author suite was not rerun. Neither formal verification nor independent acceptance of this revision is claimed.

## 8. Precise targets for the next referee

Please examine the parameter-independent insertion/readout specification; the coefficient margins including normalized rare failures; the coprime-factor dimension proof; the common representative and compact selection arguments; and the full-interval, probability-weighted zero-evidence extension of the Bellman objective. These are the substantive new claims offered for review, alongside the three corrected general statements.
