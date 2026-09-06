# Referee report — A1, English revision 11

**Manuscript:** *Sparse observation algebras and certified memory across exponent collisions*  
**Author named in the manuscript:** Qian Qi  
**Date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation: REJECT at the requested four-journal level in its present form.**

This is an owner-requested, AI-assisted external referee-style assessment, not a report commissioned by any named journal. The recommendation is an editorial judgment about this submission, not a claim that its principal rate is false, that an identical theorem has been located elsewhere, or that the research program cannot succeed.

## 1. Submission, independence, and scope

```text
repository:       TrillionniumFoundation/theta-theory
revision branch:  revision/a1-english-v11-referee-response-2026-09-06
submission SHA:   f2f7bd3cf2544c3c57f09d015cb10bf0efe6c1c0
submission tree:  e4281eaee6beb548f8bb29126693a272fa7b595b
commit time:      2026-09-06T09:29:46Z
principal path:   papers/A1-english-v11/
controlling review: 1aa4599eedca650d34c3778a00f3ad854c2bc9d7
prior submission: d9f48fe08fd694e636c287be7646ae7d723ce3b8
new review branch: review/a1-english-v11-harsh-referee-2026-09-06
```

The target is the certified-memory revision of the effective-finite-memory paper, not the separate v10 shared-memory-composition submission. All manuscript references below concern this exact SHA. Source labels, rather than unverified PDF theorem/page numbering, identify the mathematical locations. The source index records the actual read ranges. [S0–S12]

I examined the complete new certified-resources section, the effective compiler's principal chain, and the critical inherited experiment, tangent, Hermite, collision, and global-covering arguments. I independently reconstructed the two-sided certificate, first-success estimates, finite-input perturbation estimates, and their connection to the collision law. I also reran the exact new author suite after verifying three source SHA-256 hashes, introduced a transition-table mutation, and ran an independent rational interval diagnostic.

I did **not** rebuild LaTeX, inspect the rendered manuscript PDF, rerun the legacy v10 or legacy referee suites, verify the entire proof-preservation inventory, or certify every retained appendix and historical branch. The 55-page build and 59-proof preservation counts remain author-reported here. This report is not a formal proof certificate. Detailed calculations and execution boundaries appear in the accompanying audit and receipts. [S1, S12, X1]

## 2. Overall mathematical assessment

V11 is a genuine revision. The numerical scale is now chosen by an observable finite certificate rather than prescribed from a uniform floor. The algorithm retains the exact M-label budget, uses certified coefficient/moment data, and does not decide exponent equalities. The distinction between a reachable representative and its approximate numerical coordinates is maintained throughout. These improvements deserve credit. [S7–S9]

**No blocking counterexample or essential unfilled step was found in the examined principal classification and profile-adaptive compilation proofs under their printed hypotheses.** In particular, the new covering-profile comparison is not circular; the adaptive stopping rule does terminate when the covering radius is positive; and a corrupted program receiving a larger residual certificate does not invalidate the residual theorem. The exact-arithmetic sentence identified below needs correction, but does not refute the stated sufficient input/output precision law. [S7–S9]

My recommendation nevertheless remains negative at the requested level. The strongest part of the whole paper is the uniform attainment of a collision-sensitive prediction geometry by actual positive experiments, together with a global cover and a compatible causal converse. It would be inaccurate to dismiss that achievement as merely a Vandermonde identity. However, the additional adaptive realization proceeds through a classical greedy covering estimate, a dyadic stopping argument, and fixed-horizon Lipschitz propagation. Its profile-dependent resource phases follow by substitution into a sufficient table-size count. The manuscript has not yet made a persuasive case that this combination constitutes an advance of exceptional general-mathematical importance, rather than a technically careful specialized classification and realization theorem. [S3–S9; L1–L4]

This assessment concerns the combined submission, not simply the incremental change since v10. Neither a list of ten added results nor a count of successful tests resolves the significance question. Conversely, the diagnostic defects below are not substitutes for an argument about mathematical significance.

## 3. Disposition of the preceding report

| Earlier request | What is actually supplied | Present disposition |
|---|---|---|
| P10.1: sensitive decoder and off-grid checks | Independent exponent-keyed truth, all stored queries checked, explicit domain restriction, smaller bounds | **Closed for the old zero-decoder defect.** A different transition-sensitivity defect is established in P11.1. |
| P10.2: genuine finite numerical inputs | Signed coefficient/moment perturbations, broken numerical coincidence identities, explicit quotient certificate | **Substantively addressed.** Integrated adaptive physical coverage remains limited; see P11.2. |
| P10.3: stronger sufficient numerical resources | Separated-chain floor with attribution, followed by full-profile adaptive selection | **Addressed and strengthened.** Do not demand an unclaimed universal precision/program converse. |
| P10.4: theorem-specific literature comparison | Separate assumptions, objectives, data interfaces, and resources | **Substantially improved.** A version/theorem-number mismatch still needs correction; see P11.4. |
| P10.5: preservation and proof order | New preservation inventory; principal chain separated from appendices | The organization was examined; the complete preservation count was **not independently rerun** here. |
| Editorial significance | More precise claim and additional realization theorem | **Not resolved by technical checklist completion.** See Section 5. |

The earlier objections about discarded failure evidence, ambient rather than attainable dimension, division by a zero pivot, and uncharged exact-history access should not be reopened without new evidence. The examined source continues to handle those points correctly. [S2–S9, R1]

## 4. Concrete findings requiring a response

### P11.1 — The complete new suite accepts collapsed transition tables

**Severity: major diagnostic deficiency, not a theorem counterexample.**  
**Locations:** `tests/test_v11.py`, `physical_tests`, `adaptive_tests`; `certified_compiler.py`, `verify_program`; `finite_compiler.py`, `compile_tables`.

The unmodified v11 suite passes **8,207** checks. Its output controls detect **495** fully zeroed decoder entries and **444** separately zeroed nonconstant entries. Those repairs are real.

I then replaced every compiled transition target by index 0, without changing output tables, representative histories, source files, state budgets, or the evaluation callbacks. The wrapper was installed at both compiler call sites: the physical tests and the adaptive compiler. Across 52 compiler invocations, including refinement attempts, **775 of 1,389 transition entries changed**. The same suite still passed **all 8,207 checks**. These are executed counts, not a hypothetical mutation. [X1]

The reason is important. `verify_program` recomputes residuals for the table it receives. That is correct for `prop:program-certificate`, which expressly allows corrupted tables. The tests then compare trajectories against those recomputed bounds and broad acceptance thresholds. They do not independently require the stored target to satisfy the nearest-centre construction, nor require the returned residual to have the asserted covering order. Thus they can accept a program that largely discards its inputs while still carrying a truthful but inferior error certificate.

An exact witness explains why this matters asymptotically. Let

\[
 U=[1/4,3/4],\qquad s_0=1/2,\qquad T(s,u)=(s+u)/2,\qquad Q(s)=s.
\]

Then \(S_1=[3/8,5/8]\) and its unrestricted M-centre covering radius is \(e_1(M)=1/(8M)\). The first representative is at 3/8. Collapsing every transition to it gives error 1/4 at command 3/4, for every M. The ratio to the optimal covering radius is 2M. Our exact diagnostic checks M=1,2,4,8,16,32; the unmodified compiler's maximum grid error is at most \(2e_1(M)\), while the collapsed program's is always 1/4. The identity for the continuum radius has its elementary proof in the technical note. This is a compact-system example, not an alleged physical-collision counterexample. [X1, T1]

**Required response.** Add an independently computed per-transition contract using the actual approximate target and selected approximate centres, including the fixed tie rule or the proved approximation allowance. Include negative controls that collapse targets and otherwise destroy state/report dependence. Separately test covering-order residuals on an exact family as M increases. Do not repair this by adding assertions against a freshly enlarged mutation-dependent allowance. Retain the valid residual theorem and its existing decoder controls.

### P11.2 — The physical and adaptive numerical chains are tested separately

**Severity: substantive evidence gap; the analytic theorem is not disproved.**

The physical fixtures call the fixed-precision compiler with `MomentAdvice`; the adaptive fixtures use an explicitly solvable one-dimensional interval system. No fixture in this suite combines the physical monomial experiment, successively requested perturbed moment data, adaptive stopping, and execution of the resulting physical program. The nine physical programs have three cells and horizon three. The four-cell, five-trial intersecting-collision program-size phases are not empirically exercised. [S10–S11]

The physical off-grid points belong to a small neighbourhood of the command vertices, not a fine net of the full command cube. V11 states this limitation honestly; it is not an undisclosed violation. Nevertheless, separate successful component tests do not establish that the flagship implementation has been exercised end to end.

**Required response.** Supply at least one feasible integrated adaptive physical family, covering exact collision, a small nonzero gap, and a separated calibration. Record the finite input tolerances, actual command-domain coverage, stopping brackets, transition contracts, and program sizes. A modest finite example suffices for a diagnostic; do not claim it proves the continuum theorem or all resource phases. Preserve the existing distinction between theorem and experiment.

### P11.3 — Exact intermediate bit lengths are not an additive precision overhead

**Severity: localized numerical-model correction.**  
**Location:** final paragraph of the proof of `thm:profile-adaptive` in `sections/certified_resources.tex`.

The assertion that fixed-degree rational products imply only an additive extra working precision is not justified as an assertion about exact arithmetic. For

\[
 x_b=(2^b-1)/2^b,
\]

\(x_b^N\) has reduced denominator \(2^{Nb}\), since its numerator is odd. Its exact fractional length is Nb, not \(b+O_N(1)\). The supplied implementation uses exact `Fraction` products and quotients. The attached diagnostic confirms this identity for several b and fixed degrees. [S9–S10, X1, T1]

This does **not** contradict the sufficient b-place input/output law. Fixed horizon, bounded coefficients and positive evidence can support a b-plus-constant rounded-arithmetic implementation, but that conclusion needs an explicit rounding-error argument. Alternatively, say that input and output accuracy is \(b+O(1)\), while the exhibited exact rational evaluation uses \(O_N(b)\)-bit intermediates, with the already excluded oracle time kept separate. The current rational-operation count need not be withdrawn. The resource model must state which of these claims is being made.

### P11.4 — Pin the literature theorem to the version actually linked

**Severity: localized citation/traceability correction.**

`sections/comparison.tex` and `references.tex` identify Saldi–Yüksel–Linder's discounted \(O(n^{-1/d})\) result as Theorem 5.3 and link arXiv:1503.02244v3. In the text returned for that specific version, the discounted result is **Theorem 5.2**, whereas **Theorem 5.3** belongs to the average-cost subsection and has a bound involving an additional time parameter. Correct the number/version pair, or provide the precise published version whose numbering is intended. This does not refute the substantive distinction being drawn between the two papers. The public-source access and rendering limitations are recorded in the source index. [S0, S12, L2]

## 5. Mathematical significance and presentation

### E11.1 — Identify the non-routine theorem, not just the non-identical conclusion

The comparison section appropriately avoids claiming that finite approximation, action compression, or a Lipschitz error recurrence originates here. The remaining claim is the synthesis of a budgeted finite filter from certified feasible-history evaluations, with a computable covering-scale certificate, tied to an independently attained collision law. That is a coherent contribution. Merely showing that the output format differs from other papers, however, does not demonstrate an exceptional mathematical advance. [S0, S7–S9; L1–L4]

The sharp law's strongest feature is the simultaneous control through arbitrary additive collisions for every fixed full-support prior. The author should state a precise comparison proposition isolating what cannot already be obtained from the cited finite-approximation statements plus the geometric inputs, and exhibit a substantial consequence of that extra mechanism. This can be done within the present scope; an infinite-horizon theorem or an unrelated broader theory is not a prerequisite imposed by this report. Another rearrangement of the same maximum into program-size exponents would not, by itself, answer the objection.

### E11.2 — Separate three meanings of certification

The manuscript largely makes the required distinctions, but the evidence package must preserve them rigorously: a certified evaluation bounds numerical input error; a residual certificate bounds the error of a particular table; a mathematical theorem compares an appropriate construction to the optimal M-label scale. None implies the other without its hypotheses. P11.1 demonstrates the danger of treating a valid residual bound as an acceptance test for optimal-order compilation. [S8–S11]

### E11.3 — Assess the submitted mathematics, not repository accumulation

The direct theorem–proof chain is considerably clearer than a chronological revision log. That improvement should remain. The manuscript's retained specializations have their own hypotheses and should not be used as a numerical tally of independent breakthroughs. Equally, arbitrary deletion of established proofs is not requested. The substantive issue is which central argument carries the paper's general mathematical significance, and how the remaining material supports it. [S0–S9]

## 6. Decision and conditions for another review

I do not recommend acceptance, or a minor revision, at the requested four-journal level. The author has addressed important earlier technical requests, and the examined principal theorem chain survives this audit. The negative recommendation rests on the significance case not yet being persuasive, together with a newly demonstrated transition-testing deficiency and the concrete evidence/resource/citation corrections above.

A useful next response must distinguish closed matters from new findings; reproduce and defeat the transition mutation with an independent contract; exercise the integrated adaptive physical interface; correct the working-precision and citation statements; and present a theorem-specific case for the significance of the complete contribution. Passing those engineering and traceability checks would remove those objections, **not predetermine an editorial recommendation**.

The report contains no request to replace the full collision profile by a weaker floor, impose a prior density, discard attainable transversality, or abandon the research direction. It also contains no claim of exhaustive priority clearance or complete formal verification.

---

Evidence keys and pinned sources: [SOURCE_INDEX.md](SOURCE_INDEX.md).  
Detailed proof audit: [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md).  
Exact diagnostic arguments: [TECHNICAL_NOTE.md](TECHNICAL_NOTE.md).  
Executed results: [EXECUTION.json](EXECUTION.json).  
Reproduction: [reproduce_review.py](reproduce_review.py).
