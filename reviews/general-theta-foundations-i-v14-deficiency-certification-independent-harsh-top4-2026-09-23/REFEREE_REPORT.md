# Independent Harsh Referee Report — General Theta Foundations I, fourteenth deficiency-certification revision

**Manuscript:** *General Theta Foundations I: Intrinsic Causal Deficiency and Finite-State Decisions*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed frozen revision:** `revision/general-theta-foundations-i-v14-deficiency-certification-referee-ready-2026-09-23`  
**Reviewed frozen branch HEAD:** `52c7049ea50f5964598797b59e738ff127ab6846`  
**Exact mathematical source checkout recorded by the revision:** `a9b8731647f54f6d8fa457cb0ae944f58287d8a8`  
**PDF/evidence publication commit:** `b0fb0e7a8e377d8d29df4fdc5a1e0ea9177fe32e`  
**Immediate mathematical parent (v13):** `e8a5354659a65c3c909cd927c2f4f628ea1b1a6c`  
**Controlling predecessor report:** commit `a03a574936230aedbe1a8d3f4cb5b1fbd9c8ceb3`, report blob `69fd7069f0902ef6d17790c388fd51322407b7bf`  
**Canonical article:** `papers/GTF-I-v14-deficiency-certification/paper.pdf`, 24 pages  
**Complete preserved development:** `papers/GTF-I-v14-deficiency-certification/complete-development.pdf`, 215 pages  
**Review date:** 23 September 2026  
**Standard requested:** external-referee standard appropriate to Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica

**Provenance note.** This is an owner-requested, AI-assisted independent referee-style report. It is not an official report commissioned by any of the named journals.

---

## Recommendation

**Reject / return in the present form at the requested top-four general-mathematics standard.**

This recommendation is materially different from the one I gave to v12. The fourteenth revision has answered several of the most important mathematical objections in the previous report. In particular, the resource cost is no longer merely an exogenous label carried by a supplied simulator: v13 defines optimized private, hidden-selector and visible-selector deficiencies at fixed persistent-state budgets, and v14 gives a same-budget local testing converse with convergent lower and upper certificates. The endogenous task theorem is genuinely policy dependent. The nonsummable average-risk theorem has a precise reset signature. The hard-sphere application now uses interventions that alter the physical dynamics, not merely passive observation selection. The canonical article has also been reduced from 92 pages in v12 to 24 pages in v14. Those are substantial improvements.

I do **not** find a short decisive counterexample to the principal new v14 statements that I audited: the fixed-budget local certificate theorem, its stateless stability consequence, or the finite-space graph/intervention residual estimate. The finite proofs are internally coherent at their stated scope, and the domain bookkeeping in the active microscopic section is substantially better than the sort of informal Galerkin/Mori argument that often fails on unbounded generators.

The remaining problems are now more structural and, at the requested venue level, more consequential.

The central advertised chain is still not closed end to end. The local certification theorem applies to **finite rational causal experiments**. The flagship active hard-sphere presentation still has continuous Gaussian reports and a nonfinite physical carrier. The residual theorem gives a two-sided marked comparison error, but it does not itself produce the finite rational experiment to which the local certificate algorithm applies. The paper explicitly concedes this point: a finite-dimensional vector presentation is not automatically a finite report experiment and a further finite-report bridge must actually be proved before the rational local algorithm can be invoked. Thus the two strongest new ingredients — fixed-budget finite certification and active microscopic a posteriori comparison — coexist in the article, but the manuscript does not yet supply the theorem that composes them into the promised executable physical resource certificate.

Second, the closest-source priority audit remains explicitly unfinished. Norberg's filtered-experiment paper is directly about an extension of Le Cam deficiency to sequential decisions under filtration and gives equivalent risk criteria; Weisshaupt's later discussion identifies Norberg's Theorem 1 as a filtered randomization criterion. The manuscript has now inspected Weisshaupt carefully, which is good, but it still has not performed a proof-level comparison with Norberg or with the Paull–Unger state-minimization source that sits close to the compatible-cover side. When the claimed novelty is a connection among classical comparison, finite memory, common encoders, compatible covers, minimax and finite-state realization, this is not an optional bibliographic clean-up. It is part of establishing that the theorem-sized remainder is actually new.

Third, the new “complete local testing” theorem is mathematically useful but, in its present form, is an exhaustive compact finite-dimensional certification scheme. The proof is driven by separate affinity, rational box subdivision, vertex interpolation, a coupling modulus and real quantifier elimination. These ingredients are classical and the manuscript says so. The theorem gives a history-independent **error modulus**, but the certificate itself assigns a test to every policy cell and can be enormous as the number of rows, histories and events grows. No polynomial-time claim is made, so this is not a correctness defect. It is, however, central to the top-four novelty/depth assessment: the current private converse is a convergent local cover, not yet a structural duality or an economical characterization of the nonconvex fixed-resource feasible set.

For those reasons I would return the paper again at Annals / Inventiones / JAMS / Acta level, while emphasizing that the mathematical status of v14 is stronger than v12 and the reasons for return have changed.

---

# 1. Scope of this review

I reviewed the exact frozen v14 referee branch, not a moving working branch. I inspected in particular:

- `GENERAL_THETA_FOUNDATIONS_I_V14_REVIEW_READY.md`;
- `frontmatter.tex`, `introduction.tex`, `core.tex`, `development.tex` and `preserved-core.tex`;
- the inherited v13 `intrinsic-deficiency.tex`, `endogenous-tasks.tex`, `regenerative-risks.tex` and `active-hard-spheres.tex`;
- the new `local-certificates.tex` and `residual-certificates.tex`;
- `RESPONSE_TO_REFEREE.md`;
- `PROOF_LEDGER.md`;
- `LITERATURE_COMPARISON.md`;
- `HISTORY_AUDIT.md`;
- `PIPELINE_GRAPH.json`;
- the v14 README and review-ready source/publication identities;
- the exact v13-to-v14 repository comparison;
- the controlling independent v12 report; and
- the historical A1–D1 pipeline status recorded in the current typed dependency graph.

I also made a limited external bibliographic check of the two unresolved nearest-neighbour directions. Public bibliographic records confirm the scope of Norberg's 2002 filtered-experiment paper: it extends Le Cam deficiency to experiments generated by stochastic processes in which the statistician makes successive decisions while observing a parameter-dependent process and gives equivalent risk-comparison criteria. Publicly accessible secondary text by Weisshaupt explicitly refers to Norberg's Theorem 1 as a randomization criterion for filtered statistical experiments. I did not obtain Norberg's original full proof through that check. The IEEE Paull–Unger landing page was also not a usable proof-level source in this review. Hence the manuscript's own statement that these two original-source comparisons remain unresolved is accurate.

I did **not** treat successful LaTeX compilation, source hashes, diagnostic counts, example certificate checks or pipeline-label validation as proofs of the analytic theorems. The authors now draw this distinction correctly.

---

# 2. What v14 has genuinely fixed

A new harsh report should not recycle objections that have been answered.

## 2.1 The resource quantity is now intrinsic

The most important v12 request was to stop treating (K) as an externally supplied implementation label and define the actual least simulation error at a prescribed resource.

The inherited v13 theorem does this. It defines private deficiency
[
delta^{m p}_K(E,F)
]
by minimizing over the common finite-state causal transducer itself, and separately defines fixed-cardinality hidden and visible selector variants. The distinction is not cosmetic. The delayed three-symbol example shows that hidden convexification can change the zero set at the same private width, while visible selection has the private zero set once the selector is included in the compared joint interface.

The composition theorem also tracks the state width multiplicatively rather than dropping it from the comparison.

This is a substantive response to E12.1.

## 2.2 The private nonconvexity is no longer hidden behind a convex hull

Theorem 2.7 / `thm:v14-local` addresses exactly the problem raised by the v12 report.

For a fixed private or finite-selector resource signature, every fixed feedback/event discrepancy is separately affine in the stochastic rows. A rational clipped-simplex cover is placed on the actual policy space. On each cell, one chooses a testing inequality and uses the exact vertex minimum of that fixed separately affine test. The lower certificate therefore stays on the nonconvex private image. The upper certificate is an actual rational row table at the same width.

The delayed-channel separation correctly explains why this is doing work that one global separator on the convexified behavior set cannot do.

I find the logical distinction between “one fixed test is separately affine” and “the maximum of all tests need not be separately affine” correctly maintained in the proof.

## 2.3 The endogenous task theorem is genuinely controlled

The v13 common-encoder theorem is no longer a fixed open-loop restart theorem.

Each task may select its own control, the physical transition depends on that action, and the common encoder sees the realized action but not the task identity. Reachability is policy dependent. The occupation-regret identity is then used to characterize the exact zero face by compatible covers on the actually reached support.

This is a much more convincing answer to the previous request for an endogenous controlled task family.

## 2.4 The average-risk extension is truly nonsummable, within its reset signature

The average criterion is not a relabeled summable infinite-horizon problem. The joint physical-register kernel has an explicit reset component
[
P^pi_j=eta N_j+(1-eta)Q^pi_j
]
and the reset clears both the physical preparation and the within-policy register. This gives a genuine average-risk theorem for singular or deterministic between-reset physical dynamics.

The scope is narrow — I return to that below — but the theorem is correctly described as nonsummable under the declared regenerative signature.

## 2.5 The hard-sphere intervention is active

The v12 report criticized the physical consumer for choosing observations without changing the microscopic dynamics. That criticism no longer applies.

The v13/v14 model applies an orthogonal velocity intervention and then the true hard-sphere flow. Different interventions alter subsequent positions on a positive-measure set. The graph-core argument also avoids assuming that the intervention preserves the domain of the unbounded generator.

This is a genuine improvement.

## 2.6 The canonical paper is now focused

The v12 canonical article was 92 pages. The v14 canonical article is 24 pages. The 215-page complete development is explicitly an archival/preserved companion.

This substantially answers the old architectural objection. I would **not** ask the author simply to shorten the canonical article again.

---

# 3. The finite local certificate theorem appears coherent on its stated finite scope

I stress this because the report below is severe for top-four reasons, not because I found an elementary contradiction.

Let
[
delta=min_{qinmathcal P}F(q),qquad F(q)=max_{iin I}f_i(q).
]
For the finite causal experiment, the test set (I) is finite, including deterministic feedback trees and marked events. Along a complete path a time-indexed simulator row is encountered at most once. Therefore each (f_i) is separately affine in the row blocks even though (F) generally is not.

For a product cell (C), separate affinity gives
[
min_{qin C}f_i(q)=min_{vin V(C)}f_i(v).
]
This justifies the local lower witness. The upper witness is a true policy vertex, not a mixture of designs.

The oscillation proof is also plausible. Two rows in one mesh cell have bounded total variation. Maximal coupling at each time, conditional on previous agreement, gives the product survival bound. Hidden and visible selectors are treated differently; in particular the visible bound contains the second selector contribution because the reference joint experiment changes with the selector distribution as well.

The dyadic monotonicity argument is consistent with the chosen rational grid, and the real-closed-field argument for rational finite data gives the claimed exact boundary decidability and algebraicity.

Thus my concern with Theorem 2.7 is not an identified false inequality. It is what the theorem does — and does not — provide as the proposed conceptual centerpiece.

---

# 4. Major blocker I: the local-certificate theorem and the physical realization do not form one closed executable chain

This is the most important remaining structural issue.

Theorem 2.7 assumes a **finite** marked causal experiment. Its effective statements further assume **rational** instrument probabilities. The test set is finite because the report/control/mark transcript spaces and the parameter set are finite.

The active microscopic experiment in Section 5 is different. It has:

- a continuous hard-sphere initial physical state;
- a finite-dimensional vector approximation but not a finite latent-state experiment;
- continuous Gaussian reports before any optional partitioning; and
- physical expectations/Gram data that are not rational merely because a finite matrix representation exists.

Theorem 5.5 gives a two-sided stateless marked comparison bound between the exact and approximate Gaussian acquisition models. This is valuable. It lets one transport risk statements and intrinsic deficiency inequalities abstractly.

But the manuscript does **not** supply the next bridge needed to invoke Theorem 2.7 on the physical approximation.

The paper itself says this explicitly in Corollary 5.6:

> a finite-dimensional vector model is not automatically a finite report experiment; a further finite-report bridge must actually be proved before invoking the rational local testing algorithm.

That sentence is mathematically responsible. It is also an admission that the headline physical “a posteriori realization” does not yet instantiate the headline local certificate theorem.

A top-four version centered on certification should close this gap.

At minimum I would require a theorem of the following form.

1. Starting from the finite-dimensional Gaussian acquisition presentation, construct a finite-report marked causal experiment by a declared quantization/truncation scheme.
2. Prove a two-sided **feedback** deficiency bound for that report discretization, uniformly over the fixed consumer resource budget and preserving the actual mark.
3. If rational exact certification is claimed, replace the resulting finite real transition probabilities by a rational experiment with an explicit additional two-sided error.
4. Compose those errors with Theorem 5.5 and Theorem 2.9.
5. Apply the local certificate to the resulting rational experiment and state the resulting interval for the original physical intrinsic deficiency.

Without this theorem, the article contains a finite exact certification theory and a continuous physical comparison theory, but not a completed physical certificate.

This is not a minor expository request. It is exactly the bridge needed to make the paper's two strongest ingredients one theorem chain.

---

# 5. Major blocker II: asymptotic approximation and a posteriori residual certification are not yet a convergent certified scheme

The active section contains two logically distinct positive statements.

The inherited graph-core theorem proves strong convergence of the controlled-word approximations for each fixed horizon. Hence the true acquisition deficiency tends to zero.

The new residual theorem gives, for a **particular** finite subspace (V), an a posteriori majorant computed from
[
R=((I-P)Liota)^*((I-P)Liota),qquad
S_a=((I-P)C_aiota)^*((I-P)C_aiota)
]
and the corresponding finite-dimensional word defects.

These are both useful. But the manuscript explicitly states that the residual majorants need not converge to zero along every graph-core sequence. Cancellation can make the actual orbit error small even when the residual bound stays large.

Therefore the paper still lacks a theorem producing a sequence of **certifiably shrinking** physical residual bounds.

For an “a posteriori certification” flagship result, this distinction matters. The current theory says:

- some graph-core sequence converges in the actual dynamics; and
- any one finite space with rigorously enclosed residual data has a valid computable upper bound.

It does not say that the computable upper bounds along the convergent sequence actually tend to zero.

A stronger and more compelling result would identify an important class of approximation spaces for which the residual certificate is complete in the limit, for example under a quantified graph-norm approximation property stable under the finite intervention family. Alternatively, prove a posteriori/enriched-space bounds that dominate the true error and converge under verifiable hypotheses.

As written, “analytic convergence” and “finite certified convergence” remain separate.

---

# 6. Major blocker III: “complete local testing” is complete by exhaustive localization, not yet a structural private-resource duality

The private feasible image is nonconvex, so one should not demand a false global linear dual.

The v14 solution is to localize. This works mathematically.

But the cost of localization is enormous. A certificate assigns one test to every product cell of the row-simplex cover. The number of cells grows roughly like a power of the mesh size in the total row dimension, and the total row dimension itself grows with the number of time/state/action/source-report row blocks. The available tests range over parameters, deterministic feedback trees and marked events; the event family alone is exponential in the finite transcript cardinality.

The theorem's modulus
[
1-prod_t(1-ho_t(M))
]
does not depend on the number of histories. That is a useful stability fact. It must not be confused with history-independent certificate size or synthesis complexity.

The README is candid that enumeration can be large and that the code rejects rather than truncates an oversized cover. The article should make the distinction equally sharp whenever “effective”, “executable” or “complete certificate” is used.

For top-four depth, I would want more than a convergent mesh oracle unless the authors can show that this localization principle itself yields a surprising structural consequence.

Possible routes include:

- a finite witness theorem with support size controlled by an intrinsic dimension rather than the number of policy cells;
- a nonconvex duality in a richer class of tests;
- a semialgebraic stratification theorem reducing the relevant cells;
- a sharp certificate-complexity theorem for a nontrivial family;
- a lower bound showing that exponential localization is genuinely necessary in the private setting; or
- a structural characterization of the zero or positive-error spectra for a broad model class extending the nonnegative-rank slice.

At present the theorem is exact and honest, but its proof reads primarily as compact finite-dimensional global optimization with a tailored causal modulus.

That is significant mathematics. I am not yet persuaded it is Annals / Inventiones / JAMS / Acta mathematics by itself.

---

# 7. Major blocker IV: the originality audit is still incomplete exactly where it matters most

The paper's contribution is deliberately formulated after “classical subtraction.” This is the right way to present it.

But that makes the nearest-neighbour audit especially important.

The manuscript now gives a serious comparison with Weisshaupt's filtered randomization theorem. This is useful. It identifies that Weisshaupt works with a compact convex operator family and does not impose the same persistent finite-state budget.

However, the author still has not obtained and compared the full theorem/proof text of Norberg's *Comparison of Statistical Experiments with Filtered Probability Spaces*. Public records make clear that this is not a remote citation: its stated object is a Le Cam-style deficiency for parameter-dependent stochastic processes with successive decisions, and it gives equivalent comparison-of-risks formulations. Accessible secondary text by Weisshaupt refers specifically to Norberg's Theorem 1 as a filtered randomization criterion.

Likewise, the full Paull–Unger proof-level comparison remains unresolved on the finite-state compatible-cover side.

This matters because the claimed novelty is not a new general convex-separation theorem, a new quantifier-elimination theorem, a new Trotter theorem, or a new variation-of-constants formula. The manuscript correctly disclaims all of those. The claimed contribution is the **resource-sensitive conjunction**:

- causal/filtered deficiency;
- fixed private memory;
- hidden versus visible selectors;
- common encoders;
- exact compatible covers;
- local nonconvex testing; and
- physical presentation transport.

At a top-four journal, that conjunction must be shown not to be an existing theorem in another language.

I therefore regard E12.5 as still open and editorially blocking.

---

# 8. The nonsummable average theorem is correct in spirit, but the hard part is supplied by the reset mechanism

The regenerative average theorem is a real answer to the word “nonsummable.” It deserves credit.

But its compactness and stability come from the explicit Doeblin-type structure
[
P=eta N+(1-eta)Q
]
with a physically supplied reset that also clears the controller register.

This immediately yields uniform total-variation contraction by (1-eta), an explicit invariant law, uniform Cesaro and Abelian bounds, and a geometric cycle decomposition.

There is nothing wrong with that. The authors state the scope honestly.

For top-four positioning, however, this theorem should not be presented as crossing the difficult general average-cost/strategic-measure boundary. It crosses that boundary only for a deliberately regenerative class in which the main ergodic obstruction has been externally removed.

A stronger future theorem would allow weaker regeneration/minorization, state-dependent returns, Harris recurrence with finite-memory control, or another genuinely nontrivial long-time compactness mechanism. Alternatively, keep the current theorem as a clean application of the intrinsic resource invariant, but do not rely on it as a separate source of top-four depth.

---

# 9. The endogenous task theorem is conceptually clean, but remains a finite zero-face theorem

The exact endogenous compression theorem is one of the clearest parts of v13.

The occupation-regret identity makes the zero-face characterization transparent. Policy-dependent reachable supports correctly avoid constraints on unused actions. Private and independently seeded exactness agree because all task excess coordinates are nonnegative and a randomized design is a mixture of deterministic tables.

The quantitative positive gap is finite-table and model dependent, as the manuscript acknowledges.

The lossy positive-error theory is less complete. Hidden-selector minimax has the ordinary finite convex dual after sampling whole deterministic designs; private finite-width positive-error optimization remains the nonconvex polynomial problem.

This is precisely why the v14 local theorem is needed.

I view this section as a good finite decision-theoretic consumer of the intrinsic deficiency. I do not view it as an independent top-four theorem at its current finite level.

---

# 10. The active hard-sphere theorem is a meaningful application, but it does not close the historical hard pipeline targets

The current pipeline graph is admirably explicit.

For all eleven historical components A1, A2, A3, A4, B1, B2, B3, B4, C1, C2 and D1, the field
`full_historical_target_closed_by_v14`
is false.

In particular:

- the primary A2 chain remains `independent_not_consumed`;
- A4 retains an operator-domain consumer but not the historical Sinai spectral/left-strip closure;
- B4 receives the new active microscopic residual consumer, but explicitly not the nonlinear action-sublevel, BBGKY/Boltzmann–Grad or kinetic closure; and
- C2 retains only an operator-domain compression edge, not the broader form/optional-projection targets.

This is good scientific bookkeeping.

It also means the pipeline cannot be used as evidence that GTF-I has become the foundational theorem from which the historical program follows. The current manuscript itself no longer makes that strong claim, and it should continue not to.

For editorial purposes I would treat the pipeline as motivation and dependency documentation, not as a substitute for a flagship mathematical consequence.

---

# 11. The article architecture is now substantially better

This point deserves a separate positive section because it changes my assessment from v12.

The 24-page v14 canonical article has a visible spine:

[
	ext{intrinsic fixed-resource deficiency}
longrightarrow
	ext{local private certificates}
longrightarrow
	ext{endogenous / regenerative decisions}
longrightarrow
	ext{active physical comparison}.
]

The 215-page development preserves history without forcing the canonical submission to reproduce every predecessor introduction and model.

This is much closer to an acceptable research-paper architecture.

I would therefore **not** make “shorten the paper” a main revision request now.

The remaining architectural request is more mathematical: close the missing bridge between the finite certificate and the physical presentation, so that the 24-page article ends in one actual certification theorem rather than two adjacent theories.

---

# 12. Detailed technical comments

## 12.1 State explicitly that modulus complexity and certificate complexity are different quantities

The error modulus is independent of the number of histories. The certificate cardinality is not.

A theorem or proposition should bound the number of cells and inequalities in terms of the number of row blocks, row alphabet sizes, mesh (M), feedback-tree count and transcript/event cardinalities.

Even a crude bound would prevent readers from reading “history-independent modulus” as “history-independent certification cost.”

## 12.2 Separate strict finite certificates from exact boundary decision

For (delta>arepsilon) and (delta<arepsilon), the mesh certificates are finite and explicit.

For equality at a rational tolerance, the proof invokes general real quantifier elimination. The shipped certificate program does not implement that algorithm.

This distinction is already in the README and proof ledger. Put it directly beside every “decidable” summary statement.

## 12.3 The physical application needs a finite-report and rationalization theorem, not a sentence

This is the central technical request of this report.

The theorem should quantify:

- report truncation;
- binning/quantization;
- Gaussian boundary mass;
- feedback propagation of report mismatch;
- mark preservation;
- rational approximation of the finite transition probabilities; and
- the accumulated stateless bridge error.

Only after that can the local certificate be honestly called a physical resource certificate.

## 12.4 Certified Gram entries need an analytic source

The residual formulas become rigorous only when the inner products involving (f,phi_i,Lphi_i,C_aphi_i) have certified enclosures.

The manuscript correctly says floating-point matrices are insufficient.

For a flagship physical theorem, give at least one nontrivial family of basis functions and hard-sphere preparations for which those enclosures can actually be produced analytically or by interval quadrature with a proof.

Otherwise the result remains a conditional a posteriori formula.

## 12.5 Give a class in which the residual majorants converge

The current warning that residual majorants need not converge is correct.

But a certification theory needs at least one useful positive convergence theorem for the majorants themselves.

This would materially strengthen Section 5.

## 12.6 Clarify finite versus compact parameter/task sets across the paper

The local deficiency theorem uses finite (Theta) and a finite test family. The regenerative section allows a compact row set (J). The physical preparation notation also permits a family (p_	heta).

High-level summaries should not blur these different index classes.

## 12.7 The nonnegative-rank example is an excellent sanity check; use it more structurally

The delayed channel currently shows strict separation between private and hidden resources.

It would be valuable to derive a larger class in which the private deficiency or its zero set has an established factorization complexity. This would demonstrate that the invariant captures nontrivial resource geometry beyond the one illustrative slice.

## 12.8 Do not use build counts as evidence of theorem truth

The current text mostly avoids this.

The 1,038 new checks, 18 negative-control executions, predecessor test reruns and source hashes are reproducibility evidence only.

Keep them in the repository-facing material, not in the novelty or correctness argument.

## 12.9 The visible-selector oscillation deserves a short independent lemma

The extra selector term is easy to miss and is a real interface issue. A standalone lemma would make the reason transparent and reduce the burden on the main local-certificate proof.

## 12.10 The lower certificate is a family, not one global test

This is the conceptual point of the theorem. The abstract phrase “testing certificates” is fine, but avoid formulations that a reader could interpret as a single Blackwell/Le Cam separator.

The per-cell dependence of the test is essential.

## 12.11 The average theorem should keep “regenerative” in every high-level label

“Nonsummable average-risk duality” is correct, but “regenerative nonsummable average-risk duality” would advertise the actual source of compactness immediately.

## 12.12 The complete development should remain archival

The 215-page preserved body is useful for provenance.

It should not be part of the editorial burden of the 24-page theorem paper except through precise references. The present separation is the right direction.

---

# 13. Status of the previous E12.1–E12.8 requests

## E12.1 — Define and characterize an intrinsic resource-deficiency spectrum

**Substantially closed in the finite causal setting.**

V13 defines the optimized fixed-resource deficiencies. V14 supplies a same-budget local testing converse and exact rational-data decision principle.

What remains is a more structural private duality / certificate-complexity theory and a nonfinite extension not dependent on an externally supplied finite rational bridge.

## E12.2 — Cross a genuinely hard infinite-time boundary

**Partially closed.**

The paper now has a nonsummable average criterion with nondominated singular between-reset physical transitions.

However, the decisive long-time regularity is supplied by an explicit synchronous geometric reset of both plant and finite register. General average-cost/strategic-measure compactness remains outside the theorem.

## E12.3 — Extend exact compression to endogenous controlled tasks

**Substantially closed.**

The v13 policy-dependent common-encoder theorem is a real controlled result. The remaining limitation is that the exact theorem characterizes a finite zero face; the positive-error private geometry is addressed only indirectly by the general local certificate.

## E12.4 — Make one downstream consumer genuinely transformative

**Partially closed.**

The intervention is now genuinely active and the finite graph residual theorem is useful.

But the flagship physical chain does not yet reach the rational local certificate, and no full historical A4/B4/C2 target is closed.

## E12.5 — Finish the nearest-neighbour theorem audit

**Open.**

The Weisshaupt comparison is much stronger. The full proof-level Norberg and Paull–Unger comparisons remain unfinished.

At the requested venue level, I regard this as blocking.

## E12.6 — Separate frozen pipeline history from mathematical dependency

**Closed as a bookkeeping issue.**

The graph is explicitly frozen, repository freshness is a separate snapshot, and A2 independence is stated.

## E12.7 — Rebuild the canonical article around one dominant theorem

**Substantially closed architecturally.**

The canonical paper is now 24 pages with a clear fixed-resource/certification spine. I withdraw the previous page-count objection.

The remaining issue is to make the finite certificate and physical realization one actual end-to-end theorem.

## E12.8 — State what remains after classical ingredients are removed

**Closed as a statement, not yet as a top-four originality judgment.**

The manuscript now clearly identifies the claimed remainder: original-budget local marked-feedback testing completeness with executable same-budget upper witnesses, causal modulus, presentation stability and active microscopic residual transport.

The unresolved question is whether that precise conjunction is both new and deep enough once the missing nearest-neighbour sources are checked.

---

# 14. What I would require for a top-four reconsideration

I would not ask for a fifteenth revision that merely adds more examples or more repository certificates.

I would require four mathematical closures.

## R14.1 — Close the physical-to-finite-rational certification chain

Prove a finite-report/rational presentation theorem for the active acquisition model with explicit two-sided marked feedback error and no hidden resource charge.

Then state one theorem that starts from certified physical residual/quantization data and ends with a lower/upper interval for the original fixed-resource intrinsic deficiency.

This would make the paper's two principal contributions genuinely interlock.

## R14.2 — Prove a convergent class of a posteriori residual certificates

Identify verifiable approximation spaces for which the Gram/intervention residual majorants tend to zero, or replace them by a convergent certified estimator.

The present combination of nonconstructive strong convergence plus potentially nonconvergent a posteriori majorants is not yet a complete certification method.

## R14.3 — Give structural content beyond exhaustive cell localization

Either derive an economical witness theorem, an intrinsic dimension bound, a genuine nonconvex dual object, a sharp certificate-complexity result, or a broad family with an explicit private-resource spectrum.

This is the step most likely to raise the finite theory from a correct certification scheme to a top-four theorem.

## R14.4 — Finish the nearest-neighbour source audit

Obtain and compare the full Norberg filtered-experiment theorem and the closest partial-machine/compatible-cover state-minimization theorem at statement-and-proof level.

The final novelty statement should be written only after those comparisons.

---

# 15. Final assessment

Revision 14 is a serious improvement over revision 12.

The strongest old objections have been answered:

- the resource cost is now optimized intrinsically;
- private, hidden and visible randomization signatures are distinguished correctly;
- the private nonconvex set has a same-budget testing converse;
- controlled common-encoder tasks are endogenous;
- nonsummable regenerative average risks are treated;
- the microscopic control genuinely changes the physical dynamics; and
- the canonical article is now focused.

I therefore do **not** recommend rejection on the ground that the project lacks a central invariant or that the latest theorems are obviously false.

I nevertheless recommend **reject / return in the present form** at the requested Annals / Inventiones / JAMS / Acta standard for three decisive reasons.

1. **The advertised certification chain is not closed.** The exact local certificate requires a finite rational experiment, while the flagship active Gaussian/hard-sphere realization remains outside that class and no finite-report rational bridge is proved.
2. **The theorem is complete by exhaustive localization rather than by a deeper structural characterization of the fixed-resource nonconvex geometry.** This is correct and useful, but I do not yet see the conceptual depth needed for the requested venue.
3. **The closest-source originality audit remains incomplete.** The unresolved Norberg and Paull–Unger comparisons sit directly next to the paper's claimed classical-subtraction remainder.

The next revision should not be broader. It should close those three gaps and make the final result read as one unavoidable theorem rather than a finite certification theorem plus a neighboring physical comparison theorem.

**Recommendation: reject / return for major mathematical revision at the requested top-four general-mathematics standard.**
