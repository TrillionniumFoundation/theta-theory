# Research status — General Theta Foundations I, R77

## Identity and controlling evidence

This is a new author revision of **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, by Qian Qi. The Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the AMS objective is retained. The current research centre is the general structure and implementation of finite causal resources, together with exact and approximate memory laws and their connection to optimal experiments. Particular group families and qubit phases are applications and sharp boundary tests of that programme; they do not define its entire scope.

The complete R76 mathematical source is the predecessor: source commit `891643799f2dfb2737ad5c147bf8def2d460630b`, source subtree `38930b53fb64ca4ca1ebcc7e20919f2ed0ba74ae`, publication commit `6943acf6ef96340c0387a18fe51d4855cac52823`. The latest substantive deposited report remains R65 at `358481b21ceeeedb1205ebd30f86982e32a2cb04`, whose target was R65. Later author work and scoped proof clarifications are dependencies or historical evidence, not invented independent reviews of the current paper. The current provenance and preservation records fix the selected identities and all retained content.

This revision develops three connected mathematical directions: common-device realization for many preparations; lower memory certificates for arbitrary classical terminal decoders; and exact optimal controller memory with tied actions in a positive reset class. They add 15 numbered statements. Final statement numbers, pages, and the full count are determined by the compiled main/supplement index, not by inferred numbering from the source filenames.

## 1. Shared preparations give a general structural theorem

The new common-device problem asks when a finite family of prepared response laws can use the same transitions and decoder. It forbids the terminal decoder from receiving the preparation identity as free side information. The pure convention counts every prescribed initial label; the mixed convention permits an externally prepared initial probability row. Both conventions are explicit and neither measures the bit cost of the external preparation selection.

| Result | What is now proved | Scope and boundary |
|---|---|---|
| `thm:r77-shared-normal-form` | For every finite group, finite preparation and output families, and closed convex specifications imposed on every command word, one permutation core suffices. The exact pure charge is the core size plus the number of distinct nonpoint projected preparation rows. | The original stochastic command matrices need not satisfy the group relations. Projected actions may have a kernel. The common transition/decoder condition and all-word quantifier are essential. |
| `thm:r77-shared-polytope` | Mixed shared memory is the minimum vertex count of an invariant polytope in the full response simplex containing the targets. Pure memory minimizes that vertex count plus the number of prescribed nonvertex targets. Both minima are attained and implementable. | The containing polytope can extend beyond the target span. This is an exact structural variational formula, not an efficient algorithm or a claim that the target convex hull itself is always optimal. |
| `lem:r77-joint-multiplicity` | The joint response module is measured by the rank of the horizontally concatenated preparation Fourier blocks, giving simultaneous orbit-copy lower bounds. | A joint multiplicity can exceed the irreducible degree. Optimizing every preparation separately does not solve the common-device problem. |
| `thm:r77-shared-low-contrast` | With a common group mean, sufficiently small positive common contrast attains the complete joint multiplicity-cover bound by one positive decoder and simultaneous prepared rows. The proof gives an explicit positivity threshold. | The equality is for mixed preparation; pure memory also obeys the exact polytope formula and the displayed bounds. Unequal means can obstruct the equality even for a trivial group. No general high-contrast formula is inferred. |
| `thm:r77-joint-robust` | Weighted joint Fourier singular values above `sqrt(2) delta` force multiplicities for any shared controller with all-word TV error at most `delta`. | The number of preparations does not multiply the error constant. The certificate is necessary; it does not solve every error optimum or automatically add an initializer. |
| `prop:r77-shared-involution` | For a fixed two-element group, `q` strictly positive preparation laws each individually need two labels, while simultaneous mixed and pure memory is exactly `2q`. The separation survives the stated positive TV margin. | The increasing resource is caused by joint preparation multiplicity, with fixed group. This is a matching family, not a lower for every family of `q` preparations. |
| `prop:r77-many-initializers` | For the same fixed group and binary outputs, a family with two mixed core labels has exact pure memory `r+1` for `r` distinct prepared amplitudes. | The pure initialization cost for a family can grow without bound. The inherited one-extra-label theorem for its stated single-preparation/stationarity problem remains valid. |

The advance is the simultaneous structural and exact initialization law, including arbitrary finite groups and noncyclic joint response modules. Classical representation theory and positive-realization geometry are used openly as ingredients. The new proofs specify where common means, shared decoders, convexity, and counted preparation labels enter, instead of hiding them in an abstract realization assumption.

## 2. Unrestricted decoder lower bounds now include the original phase

`lem:r77-robust-antichain` supplies an explicit robust version of a classical support-antichain certificate. `thm:r77-operational-antichain` derives its hypotheses from finite observable preparation/test experiments and full joint stopped-record TV, controlling herald probabilities before conditioning. The simulator may use arbitrary stochastic terminal response tables; no density matrix or Born rule is assigned to an individual hidden label. The later test and the policy's future test code are unavailable before the herald.

For `J` heralded preparations of probability at least `p_*`, with own-test rejection zero and cross-test rejection at least `s`, the finite sufficient condition

`delta <= p_* s^2/(32J^2)`

forces at least `a(J)=min{m:binom(m,floor(m/2))>=J}` labels. This theorem applies to any causal experiment satisfying the stated accessible-preparation/test conditions. It does not assume that a report-only experiment has those tests, nor that a simulator may inspect uncounted history.

In the undamped qubit instrument, the preparation prefix `1 0^n`, aborted on a mismatch, has bounded target expected cost even as `n` grows. Terminal projector tests provide the exposing matrix. Let `zeta=min(1,7B/8)` and fix `B>0`. `thm:r77-unrestricted-qubit` proves for the original Bloch phase `z=(3+4i)/5` that

`delta <= 25 zeta/(128*200^J*J^2)  =>  N_cl^mixed, N_cl^pure >= a(J)`.

The proof uses integer real numerators of `z^q`; it needs no unproved badly-approximable property of its angular frequency. The same theorem gives a separate bound under an explicitly stated badly-approximable hypothesis. `cor:r77-algebraic-unrestricted` extends the lower growth to every algebraic unit phase that is not a root of unity, with explicit constants obtained from the norm of a nonzero algebraic integer.

Consequently, for the original phase and every such algebraic phase,

`liminf_(delta -> 0) N_cl(B,delta) / log_2 log_8(1/delta) >= 1`.

This is a new unrestricted quantitative divergence result. The inherited orbit-seed construction gives a logarithmic upper at a fixed phase; the original phase has its explicit rational seven-seed construction. The resulting current comparison is therefore **an unrestricted log-log lower and a logarithmic upper**, not matching rates. The earlier physical-dictionary theorem retains its matching leading logarithmic law for fixed badly approximable phases under fixed density matrices and Born decoders. Its stronger lower is not exported to arbitrary decoder tables.

The target expected budget, fixed positive `B` asymptotic, cost-free terminal test convention, and absence of an additional entangled side register remain explicit. Program-table bits, policy storage, precision, workspace, and exact sampling are different resources. No extra pure initializer is inferred from the unrestricted lower.

## 3. Optimal reset memory is now classified with arbitrary ties

The inherited reset theorem already identifies the optimal Bellman continuation vector, the spectral initial value, and a dual preparation. The new section asks exactly how many counted controller labels attain that optimum when each reset state can have several optimal actions.

Under positive definite failure effects, a positive call-cost floor, and the absence of a closed failure set, define `A_i^*` as the optimal-action set at reset state `i`, `P_*` as the optimum initial command rows, and `I(p)={i:supp(p) subset A_i^*}`. If `t(J)` denotes the minimum number of actions hitting every `A_i^*` indexed by `J`, then `thm:r77-reset-cover` proves

`m_* = 1 + min_(p in P_*) t([s] \ I(p))`.

The minimum ranges over arbitrary stochastic autonomous controllers with a prescribed pure initial label. One optimal initial command row, pure continuing command rows, and deterministic post-report routing attain it. Randomized post-report transitions and mixed continuing command rows cannot improve the minimum. Event stopping has the same total-label count; state stopping requires the separate terminal label under the inherited interface.

The necessity proof uses one dual maximizing preparation. Positive effects expose every first failure report at that preparation, and equality in the Bellman residual identity forces the corresponding continuing row to be optimal. Thus the transversal appears as a necessary and sufficient resource invariant, without a unique-action assumption. This directly advances the previously unresolved tied-action optimal-control direction for a substantive finite-dimensional class.

`thm:r77-reset-gap` adds an attained finite variational certificate `D_M`: every robustly proper controller with at most `M` live labels has cost at least `V_*+D_M`, and `D_M>0` exactly when `M<m_*`. It keeps the first post-failure residual and drops later nonnegative residuals. It therefore certifies strict suboptimality below the exact memory threshold, without asserting equality with the full constrained frontier.

`thm:r77-reset-universality` realizes every finite nonempty proper optimal-action cover in an explicit rational quantum reset experiment with commuting cost/effect operators, constant success probability, bounded costs, and an explicitly uniform optimal initial row. Its exact memory is the transversal number plus one. The explicit polynomial-encoding reduction makes optimal memory NP-hard even in this restricted family. The elementary unrestricted value does not make its memory implementation trivial. The reset maps themselves are not asserted to commute.

`ex:r77-reset-exposure` shows why the primitive positive-exposure hypothesis matters: with merely positive semidefinite effects a robust worst-case preparation can avoid the reset report, so a locally nonoptimal continuation may remain below the robust value. The displayed two-dimensional example has a one-label optimum where the unqualified cover formula would give two. No theorem is being claimed for the inaccessible-report case without new analysis.

The exact algebraic procedures prove finite computability of the value, optimal supports, cover, realizing controller, and gap certificate. They do not assert that a general elimination was executed, that numerical ties are exact, or that the procedures run in polynomial time.

## 4. Established earlier content remains active

This revision continues the latest complete source rather than restarting the paper. The original causal experiment semantics, predictable state quotient and compression, finite-resource bounds, finite-order quantum measurement, two-stage reset experiments, communication and memory accounting, rank constraints, optimal discrimination, variational and dual principles, spectral geometry, optimal implementations, local geometric results, historical derivations, and independent companions remain traceable. File preservation and statement-continuity records provide the complete mapping.

The following are inherited established results at their declared hypotheses: R66/R67 weighted stopping rigidity and robust optimal-face/anchored-polytope results; R68 posterior-interiority simulation, sparse rows and adaptive full stopped-law control; R69 stochastic first-sector, equality and worst-phase geometry; R70 relative-spectrum/leakage results; R71 arithmetic envelopes; R72 reversible finiteness; R73 exact normal form, pure-start accounting and synthesis; R74 contrast saturation and normal-quotient duality; R75 Fourier multiplicity/cover, nonabelian contrast, stationarity, complete noisy-instrument and stopped-law results. The R69 four-period transition remains closed.

All eleven R76 additions also retain their scopes: closed-convex all-word normal form; attained finite-group error optimization; robust Fourier multiplicity; the exact prime-group error law; simultaneous positivity; the bounded-coefficient existence and boundary classification; the full displayed symmetric-group mean–contrast law; the sharp excursion event bound; return-polytope approximation; finite-alphabet polylogarithmic upper bounds; and the physical-dictionary logarithmic theorem. In particular the mean–contrast result is a corollary despite its historical `thm:` label, the coefficient theorem equates parameter-feasibility regions rather than every off-boundary pair, and sharpness of an excursion event does not imply sharpness of memory.

Preserving a proof is not a claim that every historical argument underwent a fresh independent review. The complete companion and historical bodies remain separately available at the locations specified by the preservation map.

## 5. Remaining research obligations

1. **Original general-`M` squared-sign decision risk.** The quantity `V_(p,alpha,M)-V_(p,alpha)` still has no general exact formula or matching asymptotic lower. New response counts, the unrestricted stopped-law lower, the reset optimum-memory formula, and `D_M` address different mathematical quantities. None closes this original risk problem.
2. **Control beyond the exposed reset class.** Arbitrary ties are now handled exactly when every reset report is exposed at an attaining dual preparation; positive definite effects give a direct sufficient primitive condition. Nonreset back-action, retained unknown states, inaccessible reports, additional observations, and different stopping/commitment freedoms need further theorems. The counterexample prevents simply discarding exposure.
3. **General high-contrast and differing-mean positive realization.** The new shared normal form and invariant-polytope formula are general for finite groups, and the common-mean small-contrast synthesis is exact. Closed formulas for arbitrary high-contrast families, differing means, nonreversible command semigroups, and efficient global synthesis remain unresolved. The complete symmetric-group family remains a solved special case.
4. **Sharp unrestricted approximation rates.** The absence of any quantitative lower for the original algebraic phase is repaired by the finite antichain certificate and the log-log growth theorem. Matching its logarithmic upper remains open. Matching continuum-command rates, joint budget/error asymptotics, and general policy-dependent tradeoffs are not supplied. The physical-dictionary matching law for badly approximable phases stays at its original scope.
5. **Complete-instrument spectral frontiers.** Outside the solved stochastic sectors, a necessary scalar spectral condition need not be sufficient for the complete instrument. Further damping transitions and equality classifications require proof.
6. **Arithmetic refinements.** The original algebraic phase now has an elementary exponential separation sufficient for unrestricted divergence. This is not a sharp polynomial Diophantine exponent, does not prove it badly approximable, and does not close joint favourable-scale questions. The general algebraic norm argument has the same limitation.
7. **Timing and other resource currencies.** Intermediate phase-type timing remains separate. Program bits, arithmetic precision, workspace, exact sampling, communication costs, preparation-selection resources, and learning unknown models require their own accounting. NP-hardness of an explicit reset cover does not settle every synthesis problem or establish an unproved complexity separation.
8. **The broader Theta programme.** A1, A2, B4, C2 and other independent construction goals are not assumptions silently supplying missing steps here, nor are they declared completed by a model-specific result. Each retains its own proof obligations.
9. **Priority and publication assessment.** Classical ingredients are acknowledged and primary literature has been checked to the extent recorded in the research handoffs. Proposed novelty is stated at the level of the proved resource invariants, synthesis, operational constants and exact physical reductions. Exhaustive priority and suitability for a top general mathematics journal require genuine independent assessment; neither a finite test nor an AI cross-check supplies it.

These obligations remain research questions. They are not inserted as hypotheses into the proved results, and the paper's target is not reduced to avoid them.

## 6. Validation status

The current proof audit identifies the decisive mechanisms and the scope corrections. The author team separately challenged the shared-preparation, unrestricted-lower, and reset arguments. Exact finite diagnostics accompany the new constructions and constants. The unrestricted development run contains 39,087 rational checks, and ordinary/optimized outputs agree; the shared suite covers the specified rational involution, initializer, obstruction, and nonabelian examples. These are bounded diagnostics, not proofs of arbitrary groups, all command words, all errors, or continuum claims.

Current source hashes, complete predecessor preservation, the full compiled theorem/dependency map, native main/supplement/companion compilation, and actual hosted execution are established by the final source-bound receipts after integration. This status record does not anticipate a final PASS, a future commit SHA, or an unexecuted CI run. The source seal, written proofs, finite checks, author-team AI challenges, native build, independent human review and editorial decisions retain their separate meanings.
