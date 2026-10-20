# Theorem and dependency map — current R73 author revision

The current article continues **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**. This map distinguishes a general response theorem, an exact model calculation, a local geometric result and a separate research obligation. It does not infer one from another merely because they share a resource vocabulary.

**Compiled locations.** `THEOREM_INDEX.json` records the actual document, theorem number and page from the final paired native LaTeX build. This map deliberately uses stable source labels; the R72 page numbers are not current locators. The source assembly retains all 171 previously compiled statement labels and adds 14 statements, including the classical finite-group lemma and the explicit cyclic-module proposition. A statement count is an inventory, not a measure of novelty.

## Central proof chain

| Statement | Document and native source | Mathematical role and proof dependencies |
|---|---|---|
| `lem:r73-lazy-convergence` — A lazy finite-chain projection | supplement; `supplement-normal-form.tex` | Every finite row-stochastic matrix with positive diagonal; a stated class-preservation condition for EQE=E. Dependencies: Elementary proof is included; no numbered dependency. |
| `thm:r73-normal-form` — Reversible stochastic normal form | main; `sections/33-reversible-normal-form.tex` | Every finite stochastic realization of a finite-dimensional compactly reversible probability response; arbitrary finite command and terminal alphabets; prescribed pure start. Dependencies: `thm:r72-reversible`, `lem:r73-lazy-convergence` |
| `thm:r73-memory-formula` — Exact memory formula | main; `sections/33-reversible-normal-form.tex` | The same finite observable-group class, with probability-valued terminal rows. Dependencies: `thm:r73-normal-form`, `thm:r72-reversible` |
| `cor:r73-group-bound` — Sharp group bounds | main; `sections/33-reversible-normal-form.tex` | All M-label realizations in the compactly reversible class; the stronger factorial uses M<N. Dependencies: `thm:r73-normal-form`, `thm:r72-reversible` |
| `cor:r73-rank-rigidity` — Rank rigidity | main; `sections/33-reversible-normal-form.tex` | All finite compactly reversible responses, including the constant case. Dependencies: `thm:r73-normal-form`, `thm:r72-reversible` |
| `prop:r73-symmetric-family` — Exact symmetric-group family | main; `sections/33-reversible-normal-form.tex` | The explicitly specified two-command natural S_k action, nonconstant probability preparation and bounded nonconstant decoder, k>=3; degeneracies stated separately. Dependencies: `thm:r73-memory-formula` |
| `prop:r73-decoder-obstruction` — A strict bounded-decoder obstruction | main; `sections/33-reversible-normal-form.tex` | The stated S3 endpoint response and its prepared qubit realization; not a formula for all rank-three responses. Dependencies: `thm:r73-normal-form`, `thm:r73-memory-formula` |
| `prop:r73-cyclic-module` — Cyclic permutation-module minimum | supplement; `supplement-normal-form.tex` | Multiplicity-one real cyclic character modules, allowing equal orders for distinct character pairs. Equality kappa=nu is asserted only for the retained probability-valid positive-amplitude periodic family. Dependencies: `thm:r73-memory-formula`, `thm:r72-periodic-memory` |
| `lem:r73-minkowski` — Classical finite-group bound | main; `sections/34-algebraic-synthesis.tex` | Finite matrix groups over the supplied real number field; a conservative effective enumeration bound. Dependencies: Elementary proof is included; no numbered dependency. |
| `thm:r73-algebraic-synthesis` — Decidability and minimal algebraic synthesis | main; `sections/34-algebraic-synthesis.tex` | Supplied finite algebraic linear representation, promised probability validity and compact reversibility on its minimal observable quotient. Dependencies: `thm:r72-reversible`, `lem:r73-minkowski`, `thm:r73-normal-form`, `thm:r73-memory-formula` |
| `cor:r73-unitary-algorithm` — Prepared algebraic unitary experiments | main; `sections/34-algebraic-synthesis.tex` | Algebraic density matrix, finitely many algebraic unitary commands and an algebraic finite POVM, in every finite protected dimension. Dependencies: `cor:r72-unitary`, `thm:r73-algebraic-synthesis` |
| `thm:r73-finite-tests` — Finite obstruction and effective separation | main; `sections/35-finite-certificates.tex` | Any supplied finite linear probability response of dimension d and any candidate label bound M; compact reversibility is not needed. Dependencies: Elementary proof is included; no numbered dependency. |
| `thm:r73-memory-plateau` — Stable exact memory under background damping | main; `sections/35-finite-certificates.tex` | A nonconstant finite compactly reversible response, damped toward its group-averaged response with command-specific factors; constant case separately. Dependencies: `thm:r73-normal-form`, `thm:r73-finite-tests` |
| `prop:r73-period-four` — A certified four-label interval | main; `sections/35-finite-certificates.tex` | The unary damped period-four response (1+alpha^n cos(pi n/2))/2. Dependencies: `thm:r73-finite-tests` |

The normal form first uses the finite-group criterion inherited as `thm:r72-reversible`. The lazy-chain lemma produces a simplex of recurrent stationary rows before the observable quotient is applied. Only the sandwiched identity `E Q_loop E = E` is required. Inverse words make the induced action invertible on that simplex, and faithfulness follows from observability. A mixed start requires a transient label, which is the source of the exact extra charge.

The formula `m(b)=min{N,1+kappa_G(b)}` minimizes genuine probability factorizations. Linear rank and permutation-module dimension provide lower bounds; they do not remove the decoder constraints. The two S3 responses have the same observable group, rank three and six residuals, but their stochastic minima are four and six. The endpoint example therefore blocks the tempting identification `kappa=nu` outside the class where a bounded decoder has actually been constructed.

Finite-group recognition, nonnegative matrix-group structure, finite weighted-automaton equivalence and real-algebraic minimization are classical ingredients and are credited in the article and `LITERATURE_AND_PRIORITY.md`. The synthesis theorem states exactly the promised input class, supplies a complete terminating procedure, and uses the new normal form to return a smallest permutation core with the counted initializer. No claim of first decidability or polynomial running time is attached to it.

## Retained mathematical branches

| Native source family | Status in the current proof architecture |
|---|---|
| `sections/02-experiments.tex`, `03-main-theorem.tex`, `04-proof.tex` | Original actual-history causal experiment and acquired-geometry transfer chain, retained in the main article. Its hypotheses are independent of the new finite-group response class. |
| `sections/31-reversible-control.tex` | Inherited compactly reversible finiteness criterion and prepared-unitary corollary; the controlled two-involution arithmetic law remains a separately scoped model theorem. |
| `sections/32-periodic-memory.tex` | Exact periodic partition memory, counted initialization, synthesis and leakage, under the stated nonzero frequency and probability-mixture hypotheses. Complete proofs now appear in the current supplement. |
| `sections/28-spectral-memory.tex`, `29-leakage-memory.tex`, `30-diophantine-spectrum.tex` | Complete spectral, arbitrary-phase arithmetic, relative-spectrum and physical-leakage results. Their arithmetic exponents and stopping interpretation are retained without promotion to general feedback optimality. |
| `sections/25-stopping-rigidity.tex`, `26-squared-memory.tex`, `27-interior-instruments.tex` | Prior resolved stopping rigidity, actual squared-task embedding, and positive instrument realization with quantitative dimension dependence. |
| `sections/22-boundary-memory.tex`, `23-robust-realization.tex`, `21-timing-memory.tex` | Prior boundary regularity, scoped robust ties, finite realization, exact two-label law and timing result. The old arbitrary-M risk frontier is not declared solved. |
| `sections/09-causal-synthesis.tex`, `10-width-defect.tex`, `11-loss-transfer.tex`, `12-finite-memory.tex`, `17-primitive-risk.tex`, `19-compact-risk.tex`, `20-primal-dual.tex` | General performed-law and resource-constrained synthesis, width and risk transfer, compact attainment, variational and dual results with their own quantified model classes. |
| `sections/13-two-detectors.tex`, `14-reusable-continuation.tex`, `15-zero-spectrum.tex`, `16-reset-control.tex` | Report-resolved continuation, reset experiments, general and special zero-risk structure, spectral rank constraints and exact discrimination formulas; all remain independently available. |
| `sections/05-task-order.tex`, `06-geometry.tex`, `07-realizations.tex`, `08-composition.tex`, `18-strata-phase.tex`, `A-predictive-quotient.tex` | Task order, acquired geometry and local spectral strata, classical/quantum realizations, composition and the fixed-law predictive quotient. Local conclusions retain their actual regularity and fixed-law hypotheses. |
| Inline retained `supplement.tex` and its technical inputs | Full preparation-face, legality, deadlock, audit compilation, tail, selection and sparse-dual arguments. |
| `companion-r58/` and independently pinned historical companion trees in `PRESERVATION_MAP.md` | Separate absolute-calibration and original ordered-measurement/reset developments, retained with their own provenance rather than relabelled as corollaries of the response theorem. |

## Complete inherited statement locator

The following catalog is the 171-label compiled R72 inventory relocated to the current source assembly. It records current document and source, while all numbers and pages are regenerated by the current paired build.

| Stable statement label | Current document | Native source |
|---|---|---|
| `thm:r72-reversible` | main | `sections/31-reversible-control.tex` |
| `cor:r72-unitary` | main | `sections/31-reversible-control.tex` |
| `thm:r72-control-envelope` | main | `sections/31-reversible-control.tex` |
| `lem:r72-cycles` | supplement | `sections/32-periodic-memory.tex` |
| `thm:r72-periodic-memory` | supplement | `sections/32-periodic-memory.tex` |
| `cor:r72-synthesis` | supplement | `sections/32-periodic-memory.tex` |
| `lem:r72-critical` | supplement | `sections/32-periodic-memory.tex` |
| `thm:r72-periodic-leakage` | supplement | `sections/32-periodic-memory.tex` |
| `thm:r71-envelope` | supplement | `sections/30-diophantine-spectrum.tex` |
| `lem:r71-cf` | supplement | `sections/30-diophantine-spectrum.tex` |
| `thm:r71-exponents` | supplement | `sections/30-diophantine-spectrum.tex` |
| `thm:r71-cubic-rigidity` | supplement | `sections/30-diophantine-spectrum.tex` |
| `cor:r71-mixtures` | supplement | `sections/30-diophantine-spectrum.tex` |
| `thm:r69-spectral` | supplement | `sections/28-spectral-memory.tex` |
| `lem:r69-sector` | supplement | `sections/28-spectral-memory.tex` |
| `thm:r69-sector-phase` | supplement | `sections/28-spectral-memory.tex` |
| `lem:r69-arithmetic-tools` | supplement | `sections/28-spectral-memory.tex` |
| `thm:r69-worst-phase` | supplement | `sections/28-spectral-memory.tex` |
| `thm:r69-cubic` | supplement | `sections/28-spectral-memory.tex` |
| `cor:r69-algebraic-angle` | supplement | `sections/28-spectral-memory.tex` |
| `thm:r69-finite-mixture` | supplement | `sections/28-spectral-memory.tex` |
| `lem:r70-core` | supplement | `sections/29-leakage-memory.tex` |
| `prop:r70-relative-spectrum` | supplement | `sections/29-leakage-memory.tex` |
| `thm:r70-leakage` | supplement | `sections/29-leakage-memory.tex` |
| `cor:r70-rates` | supplement | `sections/29-leakage-memory.tex` |
| `thm:r70-physical` | supplement | `sections/29-leakage-memory.tex` |
| `thm:r70-finite-tests` | supplement | `sections/29-leakage-memory.tex` |
| `thm:r70-background` | supplement | `sections/29-leakage-memory.tex` |
| `thm:transfer` | main | `sections/03-main-theorem.tex` |
| `cor:relative` | main | `sections/03-main-theorem.tex` |
| `cor:exact` | main | `sections/03-main-theorem.tex` |
| `lem:attainment` | main | `sections/04-proof.tex` |
| `lem:comparison` | main | `sections/04-proof.tex` |
| `lem:roles` | main | `sections/04-proof.tex` |
| `lem:r68-hull` | supplement | `sections/27-interior-instruments.tex` |
| `thm:r68-instrument` | supplement | `sections/27-interior-instruments.tex` |
| `cor:r68-risk` | supplement | `sections/27-interior-instruments.tex` |
| `thm:r68-noise-exponent` | supplement | `sections/27-interior-instruments.tex` |
| `prop:r68-algebraic` | supplement | `sections/27-interior-instruments.tex` |
| `thm:r68-block` | supplement | `sections/27-interior-instruments.tex` |
| `lem:r68-cycle` | supplement | `sections/27-interior-instruments.tex` |
| `cor:r68-qubit-lower` | supplement | `sections/27-interior-instruments.tex` |
| `lem:r67-first-herald` | supplement | `sections/25-stopping-rigidity.tex` |
| `thm:r67-rigidity` | supplement | `sections/25-stopping-rigidity.tex` |
| `cor:r67-active-cover` | supplement | `sections/25-stopping-rigidity.tex` |
| `ex:r67-flat-margin` | supplement | `sections/25-stopping-rigidity.tex` |
| `ex:r67-nonrigid` | supplement | `sections/25-stopping-rigidity.tex` |
| `thm:r67-optimal-face` | supplement | `sections/25-stopping-rigidity.tex` |
| `thm:r67-polytope` | supplement | `sections/25-stopping-rigidity.tex` |
| `prop:r67-density` | supplement | `sections/25-stopping-rigidity.tex` |
| `thm:r67-embedding` | supplement | `sections/26-squared-memory.tex` |
| `thm:r67-hierarchy` | supplement | `sections/26-squared-memory.tex` |
| `prop:r67-finite-witness` | supplement | `sections/26-squared-memory.tex` |
| `cor:r67-finite-hierarchy` | supplement | `sections/26-squared-memory.tex` |
| `thm:r67-rank-three` | supplement | `sections/26-squared-memory.tex` |
| `thm:r67-algebraic-memory` | supplement | `sections/26-squared-memory.tex` |
| `thm:primitive-fallback` | supplement | `sections/17-primitive-risk.tex` |
| `thm:primitive-risk` | supplement | `sections/17-primitive-risk.tex` |
| `cor:primitive-width` | supplement | `sections/17-primitive-risk.tex` |
| `thm:interior-budget` | supplement | `sections/17-primitive-risk.tex` |
| `thm:boundary-attainment` | supplement | `sections/20-primal-dual.tex` |
| `cor:resource-price` | supplement | `sections/20-primal-dual.tex` |
| `thm:complete-stopped-order` | supplement | `sections/20-primal-dual.tex` |
| `thm:sparse-witness` | supplement | `sections/20-primal-dual.tex` |
| `prop:dual-bellman` | supplement | `sections/20-primal-dual.tex` |
| `cor:complete-certificate` | supplement | `sections/20-primal-dual.tex` |
| `thm:multi-resource` | supplement | `sections/20-primal-dual.tex` |
| `ex:distinct-dual-witnesses` | supplement | `sections/20-primal-dual.tex` |
| `prop:width-dual-gap` | supplement | `sections/20-primal-dual.tex` |
| `thm:weighted-rigidity` | supplement | `sections/23-robust-realization.tex` |
| `thm:weighted-face` | supplement | `sections/23-robust-realization.tex` |
| `thm:convex-memory` | supplement | `sections/23-robust-realization.tex` |
| `thm:calibration-realization` | supplement | `sections/23-robust-realization.tex` |
| `thm:calibration-k` | supplement | `sections/23-robust-realization.tex` |
| `thm:qubit-positive-phase` | supplement | `sections/23-robust-realization.tex` |
| `prop:finite-realization-test` | supplement | `sections/23-robust-realization.tex` |
| `lem:boundary-herald` | supplement | `sections/22-boundary-memory.tex` |
| `thm:boundary-regularity` | supplement | `sections/22-boundary-memory.tex` |
| `prop:boundary-ties` | supplement | `sections/22-boundary-memory.tex` |
| `prop:boundary-depth-gap` | supplement | `sections/22-boundary-memory.tex` |
| `thm:qubit-boundary` | supplement | `sections/22-boundary-memory.tex` |
| `cor:polarization-boundary` | supplement | `sections/22-boundary-memory.tex` |
| `cor:unitary-period` | supplement | `sections/22-boundary-memory.tex` |
| `prop:contractive-boundary` | supplement | `sections/22-boundary-memory.tex` |
| `cor:noisy-boundary` | supplement | `sections/22-boundary-memory.tex` |
| `thm:two-label-quantum` | supplement | `sections/22-boundary-memory.tex` |
| `thm:boundary-algorithm` | supplement | `sections/22-boundary-memory.tex` |
| `thm:timer-frontier` | supplement | `sections/21-timing-memory.tex` |
| `lem:common-plan` | supplement | `sections/09-causal-synthesis.tex` |
| `lem:synthesis-tail` | supplement | `sections/09-causal-synthesis.tex` |
| `thm:causal-hierarchy` | supplement | `sections/09-causal-synthesis.tex` |
| `cor:synthesis-attainment` | supplement | `sections/09-causal-synthesis.tex` |
| `thm:synthesis-dual` | supplement | `sections/09-causal-synthesis.tex` |
| `cor:synthesis-fallback` | supplement | `sections/09-causal-synthesis.tex` |
| `prop:tail-sharp` | supplement | `sections/09-causal-synthesis.tex` |
| `cor:balance-hierarchy` | supplement | `sections/09-causal-synthesis.tex` |
| `lem:compact-fallback` | supplement | `sections/19-compact-risk.tex` |
| `lem:occupation-perturbation` | supplement | `sections/19-compact-risk.tex` |
| `thm:compact-risk` | supplement | `sections/19-compact-risk.tex` |
| `cor:compact-width` | supplement | `sections/19-compact-risk.tex` |
| `thm:compact-cost` | supplement | `sections/19-compact-risk.tex` |
| `cor:compact-algebraic` | supplement | `sections/19-compact-risk.tex` |
| `cor:optimal-robustness` | supplement | `sections/19-compact-risk.tex` |
| `ex:boundary-discontinuity` | supplement | `sections/19-compact-risk.tex` |
| `ex:vertex-risk` | supplement | `sections/19-compact-risk.tex` |
| `ex:compact-limits` | supplement | `sections/19-compact-risk.tex` |
| `ex:cost-horizon` | supplement | `sections/19-compact-risk.tex` |
| `thm:width-defect` | supplement | `sections/10-width-defect.tex` |
| `thm:quadratic-defect` | supplement | `sections/10-width-defect.tex` |
| `prop:task-rigidity` | supplement | `sections/10-width-defect.tex` |
| `ex:strict-task-order` | supplement | `sections/10-width-defect.tex` |
| `thm:sharp-width` | supplement | `sections/10-width-defect.tex` |
| `prop:occupation-defect` | supplement | `sections/10-width-defect.tex` |
| `thm:width-transfer` | supplement | `sections/11-loss-transfer.tex` |
| `cor:bregman-profile` | supplement | `sections/11-loss-transfer.tex` |
| `thm:zero-general` | supplement | `sections/15-zero-spectrum.tex` |
| `thm:zero-spectrum` | supplement | `sections/15-zero-spectrum.tex` |
| `ex:two-zero-atoms` | supplement | `sections/15-zero-spectrum.tex` |
| `prop:selection-dual` | supplement | `sections/15-zero-spectrum.tex` |
| `lem:reachable-support` | supplement | `sections/12-finite-memory.tex` |
| `thm:memory-certificate` | supplement | `sections/12-finite-memory.tex` |
| `cor:memory-algebraic` | supplement | `sections/12-finite-memory.tex` |
| `ex:unreachable-loop` | supplement | `sections/12-finite-memory.tex` |
| `cor:memory-balance` | supplement | `sections/12-finite-memory.tex` |
| `thm:return-span` | supplement | `sections/14-reusable-continuation.tex` |
| `cor:reusable-balance` | supplement | `sections/14-reusable-continuation.tex` |
| `ex:return-span` | supplement | `sections/14-reusable-continuation.tex` |
| `prop:return-arithmetic` | supplement | `sections/14-reusable-continuation.tex` |
| `thm:borel-return` | supplement | `sections/14-reusable-continuation.tex` |
| `thm:sharp-return-depth` | supplement | `sections/14-reusable-continuation.tex` |
| `thm:reset-control` | supplement | `sections/16-reset-control.tex` |
| `prop:reset-rigidity` | supplement | `sections/16-reset-control.tex` |
| `cor:rank-one-family` | supplement | `sections/16-reset-control.tex` |
| `thm:detector-memory` | supplement | `sections/13-two-detectors.tex` |
| `cor:detector-saddle` | supplement | `sections/13-two-detectors.tex` |
| `thm:two-label-exact` | supplement | `sections/13-two-detectors.tex` |
| `cor:memory-minimax-gap` | supplement | `sections/13-two-detectors.tex` |
| `prop:matrix-order` | supplement | `sections/05-task-order.tex` |
| `thm:singular-order` | supplement | `sections/05-task-order.tex` |
| `prop:positive-order` | supplement | `sections/05-task-order.tex` |
| `prop:continuity` | supplement | `sections/05-task-order.tex` |
| `prop:sublevel` | supplement | `sections/06-geometry.tex` |
| `prop:regular` | supplement | `sections/06-geometry.tex` |
| `cor:uniform` | supplement | `sections/06-geometry.tex` |
| `thm:stratified` | supplement | `sections/06-geometry.tex` |
| `prop:atom` | supplement | `sections/06-geometry.tex` |
| `lem:drift` | supplement | `sections/06-geometry.tex` |
| `cor:metastable` | supplement | `sections/06-geometry.tex` |
| `prop:strata-phases` | supplement | `sections/18-strata-phase.tex` |
| `thm:classical` | supplement | `sections/07-realizations.tex` |
| `thm:quantum` | supplement | `sections/07-realizations.tex` |
| `prop:numerics` | supplement | `sections/08-composition.tex` |
| `cor:effective` | supplement | `sections/08-composition.tex` |
| `prop:composition` | supplement | `sections/08-composition.tex` |
| `thm:joint` | supplement | `sections/08-composition.tex` |
| `prop:pilot` | supplement | `sections/08-composition.tex` |
| `thm:quotient` | supplement | `sections/A-predictive-quotient.tex` |
| `prop:raw-quotient` | supplement | `sections/A-predictive-quotient.tex` |
| `prop:absolute-sharp` | supplement | `sections/B-boundaries.tex` |
| `thm:face` | supplement | `supplement.tex` |
| `prop:legal` | supplement | `supplement.tex` |
| `prop:deadlock` | supplement | `supplement.tex` |
| `prop:compile` | supplement | `supplement.tex` |
| `prop:tail` | supplement | `supplement.tex` |
| `lem:supp-mixture` | supplement | `supplement.tex` |
| `prop:supp-uniform` | supplement | `supplement.tex` |
| `prop:supp-solver` | supplement | `supplement.tex` |
| `prop:supp-dual-slack` | supplement | `supplement-primal-dual.tex` |
| `prop:r70-degenerate` | supplement | `supplement-leakage.tex` |
| `prop:r70-one-label` | supplement | `supplement-leakage.tex` |
| `prop:r69-degenerate` | supplement | `supplement-spectral.tex` |

## What this map certifies and what it does not

`THEOREM_DEPENDENCIES.json` contains the manually specified proof dependencies and scope of all new statements, every inherited compiled label, and the actual explicit statement/proof cross-references in the current source. Those syntactic references are not presented as a complete formal derivation graph. It also preserves exact historical dependency-ledger objects with their Git blob identities at the controlling R72 commit. Older labels in those raw objects are historical evidence; current locators use the current native source.

The new algebraic finite gap supplies a computable sufficient damping cutoff, and the period-four inequality supplies the explicit interval `[89/90,1]`. The exact first transition point in a general model, the old general-M squared-sign risk curve, the intermediate phase-type timing frontier, general multi-command optimal feedback, sharp arithmetic leading constants, full computational resource lower bounds, unknown-model predictive reconstruction, and independent A1/A2 pipeline obligations remain distinct open questions. The previously proved rigid-herald robust-tie criterion is inherited as a closure and is not reopened.

Finite exact diagnostics check specified identities and examples. The written proofs carry the general mathematical claims. Native compilation checks document consistency. None of these is a proof-assistant certificate, a human referee endorsement or an editorial decision.
