# Author response to the R64 report — General Theta Foundations I, R65

## Controlling objects and the present revision

This is an author revision of **General Theta Foundations I: Acquired Geometry and Causal Resource Transfer**, continuing the complete R64 mathematical source `7e397f934457894d1dba961cb126e9aef9023dfc`, delivered at `6ec637d01349ff4525fdc064ab00489442798aaf`. The entire source tree `2fb9a4d5c12c65bab080e3a5b29b397d34823098` is preserved without byte changes in `retained/r64-native/`.

The controlling report is the 809-line R64 report at commit `0a66ca2ede7835ede2a62fe2363ba5dd3ccd2ed8`, blob `370ad771cf2e2482beefac866445bd384a161911`. Its exact original filename and review scope are pinned in `inputs/review/R64_REFEREE_REFERENCE.json`. The full immutable report remains in its review branch and is reused by its Git blob in the new publication directory. It reviews R64, not R65. Neither its title nor this response establishes commissioned human review or an editorial decision.

The report accepted the checked boundary-attainment, performed-law, sparse-witness, Bellman, multi-resource and timing arguments. We inherit those results and their qualifications. The work below addresses the open boundary-memory question and the concentration of the main article without changing the research identity or the Annals / Acta / Inventiones / JAMS objective.

## Mathematical changes

The new main section `22-boundary-memory.tex` treats prepared heralded channels with a finite failure alphabet, one charged command, a protected prospective audit and a fixed actual dictionary. A predictable counting identity forces first-herald commitment at the least possible cost. Compact minimax then yields an attained least-favorable measure and an exact nonnegative decision-slack decomposition. When its decisions are unique at every positive-probability failure word, finite stochastic boundary optimality is equivalent to a finite residual decision quotient, whose index is the exact live-label count. Randomness cannot lower that exact count; the proof derives determinization from zero slack, not from a false assertion about stochastic cutpoint automata. Single-model ties have a separate finite-congruence criterion. A two-model tied example shows why robust determinization can fail.

An algebraic rotating qubit realizes infinite index. The full-history optimum is attained but every fixed finite stochastic memory has an attained, strictly larger optimum. This also holds for a compact unknown-polarization family with a least-favorable preparation derived from its loss. Finite memory nevertheless approximates the optimum exponentially at exactly the boundary budget. A finite distinguishing-depth certificate gives an explicit positive lower gap for each prescribed memory count.

Positive exact-memory results accompany the obstruction. On unitary orbits, uniqueness makes finite realization equivalent to pure periodicity. Uniform contraction with a strict limiting decision gap gives an exact finite prefix-and-tail implementation, with a stated label bound. Depolarizing rotation shows that contraction alone is insufficient when the limiting task is tied. We further solve the entire one- versus two-live-label optimization for the noisy qubit at every rotation angle, damping strength and herald rate. At the algebraic example's half-herald rate the exact values are `12/13` and `43/52`; the second label helps exactly when `q alpha > 1/3`. The proof optimizes all stochastic transition matrices and all randomized decoders, not a selected controller family.

Finally, a unary rational-channel theorem gives a direct precision-synthesis procedure at the least budget. It separates the number of live labels, transition-table bits, numerical dictionary encoding, working storage and rational arithmetic. Its polynomial precision bound requires the herald rate bounded away from zero. It is not a general efficient robust-control theorem or a matching complexity lower bound.

The main article is reorganized around these results and the accepted performed-law/optimality theory. The complete actual-history comparison and transfer proof remain in the main article. Every other inherited mathematical section is compiled in the current technical supplement, except historical introductory exposition, which remains byte-preserved and explicitly mapped. The complete R64 article and prior companions are retained independently.

## Major requests — report section 15

| Item | Layer | Response and controlling location | Disposition |
|---|---|---|---|
| 15.1 Reorganize around the central theorems | Editorial organization | `main.tex` now concentrates on primitive feasibility, boundary attainment, performed-law comparison, sparse witnesses/Bellman equality, new boundary memory, exact timing, and actual-history transfer. Other full technical proofs are in `supplement.tex`; placement is explicit in `EDITORIAL_LAYOUT.json` and `PRESERVATION_MAP.md`. | Substantively reorganized, not deleted |
| 15.2 Occupation-measure and finite-mixture comparison | Priority and theorem scope | The new introduction compares Piunovskiy–Zhang's extreme occupation measures and J+1 primal mixtures with Dufour–Prieto-Rumeau's face/minimal-mixture and finite-reward results. R64's k_T+1 objects are dual model/preparation atoms, not primal policies. A stationary policy reading a continuous Markov state is not a finite-label implementation without that state input. | Native theorem-level comparison added |
| 15.3 Highlight performed-law compactness | Mathematical organization | The opening argument identifies the positive reserve, fixed dictionary, finite-prefix coefficients and bounded terminal tails. Full law compactness is not occupation compactness or continuity of expected duration. The accepted complete proof remains in `20-primal-dual.tex`. | Inherited proof promoted, not claimed new |
| 15.4 A less engineered substantive application | Mathematical consequence | The new protected random-horizon quantum prediction problem has a primitive instrument, derived boundary cost, exact memory classification, uncertain-polarization extension, noisy-channel analysis and a globally optimized two-label risk law. No reference-balancing group or externally supplied decision string is used. | New exact application; no assertion of priority for a recognized open problem |
| 15.5 Boundary finite-label attainment | Missing structural theorem | `lem:boundary-herald`, `thm:boundary-regularity`, `prop:boundary-ties`, `thm:qubit-boundary`, `prop:contractive-boundary` and `cor:noisy-boundary` give exact criteria, positive realizations, counterexamples and same-budget density in the declared class. | Resolved for prepared heralded channels; unrestricted boundary classification remains open |
| 15.6 Keep the actual dictionary fixed | Quantifier and convexity | All new stochastic-memory and minimax statements fix C. The optimized hard-width counterexample and the distinct cost/risk witnesses are inherited unchanged. Prefix approximation does not mix different dictionaries. | Preserved throughout |
| 15.7 Deepen timing only with a genuine result | Application scope | The accepted timing theorem is retained without claiming its pumping bound is the exact intermediate curve. The new exact two-label formula concerns a different, explicitly specified quantum prediction task; it is not relabeled as a solution of intermediate phase-type timing. | Timing closure preserved; intermediate timing optimum remains open |
| 15.8 Honest computational content | Effectiveness and resources | `thm:boundary-algorithm` proves a polynomial precision construction for unary rational channels at a bounded herald rate. The existing sparse witness evaluation remains distinct from discovering a globally feasible witness. No universal bit/workspace lower is claimed. | A positive subclass complexity theorem added |
| 15.9 Actual hosted rebuild | Reproducibility | `verify.py` performs source-identity, diagnostic parity and native builds; a separate isolated read-only workflow is supplied. The new publication receipt reports only the actual matching run status. The R64 run was still queued at the recorded observation. | Local and hosted evidence explicitly separate |
| 15.10 Clear editorial packet | Delivery and provenance | Current main, current technical supplement, preserved R58 companion, complete source, exact theorem index, response, proof audit and source-bound publication records have separate entries. R64's whole source remains unchanged. | Supplied |

## Technical comments — report section 16

| Item | Response and current authority |
|---|---|
| 1. Positive cost floor and bounded loss | The first-page summary and `thm:boundary-attainment` state them. The new heralded model has unit call costs and bounded audit loss. |
| 2. Plan compactness is not cost continuity | The introduction and the complete proof retain the intersection of finite reserved constraints and monotone cost limits. No occupation compactness is inferred. |
| 3. Reserve after the depth decision | The inherited finite plan includes continuation after the depth-T report. The new boundary prefix also executes a real tail state, not a fictitious cutoff halt. |
| 4. The first call is charged | The new identity counts calls from i=1 and gives N_min=1/p, not a count of failures alone. The timing proof and primitive finite-cost reserve remain unchanged. |
| 5. Boundary price need not be finite | The resource-price corollary is inherited with its endpoint nonattainment qualification. Exact boundary memory is proved independently. |
| 6. Fixed tuple and repeated dictionary entries | Retained in the compact tuple arguments; all new exact-memory results use a fixed finite set C and never convexify a union of dictionaries. |
| 7. Tuple attainment does not imply convexity | The distinction and the exact hard-width duality gap remain in the main theorem section. |
| 8. Complete stopped word | `thm:complete-stopped-order` continues to include the full visible terminal word, commitment and prospective audit. The new heralded problem has the actual failure word as its history. |
| 9. Target law is data, not an oracle | Preserved at the definition of complete-law deficiency. The new quantum rule must be implemented from labels and cannot read a phase oracle. |
| 10. All-model budget feasibility in the inner dual | Preserved in the complete-score theorem and highlighted in the new introduction. |
| 11. No universal finite test list | The finite separating tests and sparse witnesses remain problem-, dictionary- and horizon-dependent. |
| 12. Total variation does not control duration | Kept adjacent to the complete-law theorem and in the retained tail counterexample. Boundary duration here is derived separately by a counting identity. |
| 13. Strict fallback for interior density | The original hypothesis remains. The new boundary density uses a different first-herald argument at exactly N_min and is not inferred by setting interior slack to zero. |
| 14. Initial branch role is counted | Preserved in primitive completion and the supplement's mixture lemma. No additional seed appears in the boundary automata. |
| 15. Zero deficiency needs compact attainment | The accepted argument remains unchanged. No finite diagnostic is substituted for it. |
| 16. Atoms depend on the finite problem | The sparse witness remains tied to its actual horizon, dictionary, model family and plan polytope. |
| 17. Affine rather than raw plan dimension | The k_T+1 count retains its affine-flow-eliminated meaning. It is not called a live-state count. |
| 18. Distinct risk and cost priors | The full counterexample and independent atom lists remain in the main article. |
| 19. Dual-minimizing tree is not enough | Primal feasibility plus dual equality remain necessary. The new two-label solution independently proves global primal optimality in its own model. |
| 20. Active positive atoms | Complementary slackness and the pure spectral interpretation are unchanged. |
| 21. One jointly strict fallback | The multi-resource theorem keeps this requirement. Distinct separately safe fallbacks are not substituted. |
| 22. One coercive resource and other bounded increments | Retained in the multi-resource statement and its completion proof. |
| 23. Hard program/space/width are not additive expected costs | Preserved in the current summary and supplemented by the new separate bit and working-storage accounts. |
| 24. Hard-width example uses a general bounded loss | It remains labeled as such; the new qubit example separately uses genuine squared Pauli-audit loss. |
| 25. Real budget versus integer K,M | The timing theorem keeps these domains. The new p,alpha,c parameters are real in their displayed ranges, while live-label bounds and failure lengths are integers. |
| 26. Event versus state stopping | The inherited definitions and packing proof are retained. New results report live labels first and explicitly state event maximum versus state sum for total labels. |
| 27. One-label timing has constant halt probability | The timing argument retains no free clock. At the new boundary, halt is forced at the first herald; one-label prediction instead has a constant decoder row. |
| 28. Positive paths in pumping | The accepted timing proof continues to pump only a positive-probability path. The new stochastic separation likewise keeps a positive selected internal path. |
| 29. A free clock changes the interface | Explicitly excluded in the new model and in every finite-memory construction. Offline synthesis is not runtime clock access. |
| 30. Timing marginal versus complete law | The timing terminal marginal remains constant; the complete law retains its stopping-time difference. The quantum application adds a nonconstant physical audit task instead. |
| 31. No infinite-horizon export of k_T+1 | No such inference is made. Infinite-history boundary optimality and finite residual index are separately proved. |
| 32. Analytic pure states are not controller memory | Repeated in the sparse-witness discussion. The protected qubit cannot be inspected or controlled beyond the one declared command. |
| 33. Review scopes stay version-specific | All R59 reports remain historical reviews of R59. The controlling new report is explicitly R64. None is described as a report approving R65. |
| 34. Local execution is not hosted success | The source-bound receipts identify the local build method. A remote queued/absent run is not a pass. |
| 35. Finite checks do not prove continuum claims | Exact algebraic checks and floating probes are separately counted and explicitly limited. The nonperiodicity and global two-label results have analytic proofs. |
| 36. Add the absorbing-mixture papers | Added to the native bibliography and theorem-level comparison with precise primal/dual distinctions. |
| 37. State mathematical scope early | The main abstract, introductory assumption chart and each new theorem state the applicable interface, dictionary and budget class. |
| 38. Label superseded retained claims | The entire R64 source is immutable ancestry, not the current section order. `PRESERVATION_MAP.md` maps current versus retained authority and preserves earlier explicit corrections. |
| 39. Predictive quotient remains fixed-law | Preserved in the current supplement and main scope statement. The new decision residual is task-specific, not a universal unknown-model quotient. |
| 40. Priority and editorial judgment remain external | The authors claim no commissioned expert approval, exhaustive priority proof or journal acceptance. The original research objective is unchanged. |

## Proof audit, inheritance and remaining mathematical obligations

The new proofs make every essential step explicit: the predictable cost identity; uniform geometric tails for compact minimax; nonnegative slack at every positive word; determinization under uniqueness; residual-class implementation and lower bound; compact fixed-memory parameter sets; exact irrational-rotation obstruction; contraction with a strict limiting gap; exact optimization of the two-state resolvent over all transition matrices; and rational prefix construction with charged memory. The references supply classical minimax, automata and convex-control context, not unproved replacements for these steps.

A literal inherited TeX corruption in the productive-call subscript is repaired in the current copy, and the distinction between a predictable productive-call flag in the geometric route and a random productive report in primitive instruments is stated explicitly. No accepted theorem is silently deleted or presented as newly disproved. The original bytes remain in `retained/r64-native/`.

The revision does not solve unrestricted boundary finite-memory density, arbitrary unknown-model predictive realization, general geometric exactness, the full intermediate phase-type timing curve, or matching optimal program/precision/workspace/time bounds. The exact quantum two-label law and rational-channel synthesis are stronger results in their declared natural class, not a renaming of those wider open goals. Their mathematical priority and top-four significance require independent evaluation rather than an author-generated success badge.

The historical scan rehashes and reads every text object in the supplied exported corpus and freshly enumerates 490 matching branch names. It does not assert a fresh SHA read of every old branch head or a reproof of every intermediate historical theorem. These coverage limits are explicit in the provenance record. No existing author folder, report, branch or other paper is changed by this revision.
