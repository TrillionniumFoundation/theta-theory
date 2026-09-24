# Referee Report — General Theta Foundations I, Revision 28

**Manuscript:** *General Theta Foundations I: Robust Saddles, Causal Memory, and Validation Order*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/general-theta-foundations-i-v28-referee-ready-2026-09-24`  
**Reviewed head:** `cdc749027c5f7a6f66c572ea498cd15e1b1a3391`  
**Native mathematical source commit recorded by the manuscript:** `0bc3eabddc3c08b8d736cc939937b0cc349e1a89`  
**Controlling previous pipeline-aware report:** `63f52685341e0121f5494c63768bf53999f3c6c5`  
**Previous reviewed manuscript:** `7a659e0a2a41cd91f1f6f4ddc3b01c50a77882e3`  
**Review branch:** `review/general-theta-foundations-i-v28-pipeline-harsh-top4-r13-2026-09-24`

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level in the present form.**

This recommendation is substantially different in basis from the preceding v27 recommendation. Revision 28 genuinely resolves two of the most important objections raised against v27. I no longer regard the fixed-clock validation-order problem or the positive-noise exact-memory problem as open within the manuscript's declared interface. The new full-support saddle theorem, exact Brownian identification, all-twenty-interleaving comparison, and reverse-order support-boundary jump are real mathematical advances over v27.

I also did not find a short fatal counterexample to the new v28 arguments. In particular, I independently rechecked the finite continuation-channel counts underlying the principal schedule lower bounds: the relevant strict rows produce 8 deterministic generators at the two/zero cut, 10 at the one/one cut, 12 at the two/one cut, and 8 at the ideal one/three cut, agreeing with the manuscript's face-capacity calculations. The microscopic common-signal mixture formula for the Brownian target is also internally consistent.

The reason for the negative four-journal recommendation is therefore no longer that the paper fails to close its own local technical loop. The reason is that the strongest general statements remain certificate/normal-form results built from classical positive realization and finite-machine ideas, while the deepest exact conclusions remain concentrated in a highly tailored finite binary experiment. Revision 28 has made the paper mathematically sharper; it has not yet made the central theory broad or intrinsic enough, nor has it made this manuscript a genuine root theorem for the repository-wide pipeline.

The paper is now much closer to a strong specialist contribution than v27. I do not regard the current result as four-journal mathematics.

---

## 1. Scope of this review

I reviewed the v28 canonical source and the new modules most directly relevant to the response to the previous reports:

- `positive-noise-saddle.tex`;
- `physical-noise-law.tex`;
- `facial-scheduling.tex`;
- `validation-order.tex`;
- `saddle-realization.tex`;
- `exact-memory.tex`;
- `two-preparation-saddle.tex`;
- `physical-bridge.tex`;
- the introduction and theorem hierarchy;
- `RESPONSE_TO_REFEREE.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `RESOURCE_LEDGER.md`;
- `HISTORY_AUDIT.md`;
- `LITERATURE_CROSSWALK.md`;
- the v28 exact-regression record and build receipt.

I also re-read the repository-level `ROUND17_PROOF_DEPENDENCY_LEDGER.md` and checked the new manuscript against the historical A2/A3/A4, B2/B1/B3/B4, C1/C2, and D1 proof gates recorded there.

This is a mathematical referee audit, not a claim to have mechanically re-proved all 842 pages of preserved development. I treat build receipts, source hashes, and regression checks as reproducibility evidence, not as substitutes for proof.

---

## 2. What revision 28 genuinely fixes

### 2.1 The fixed-clock validation-order objection is resolved

The previous report's central objection was that the sharp twelve-state whole-schedule theorem was tied to a selected candidate-first serial order. Revision 28 no longer has that defect.

Theorem `thm:all-clock-orders` analyzes all twenty interleavings of the two three-slot tapes under the manuscript's declared-clock convention. The argument gives:

- peak 12 for `XXXYYY`;
- peak 12 for `YYYXXX`;
- a lower bound of at least 14 for every nonserial interleaving.

This is enough to determine the exact minimum over the declared-clock class and to identify precisely the minimizing schedules.

That is a material strengthening. It is not merely another implementation table.

The proof also correctly addresses a subtle loophole that would otherwise invalidate a channel argument: a random output with mean zero need not be a deterministic-zero channel when fresh independent gate coins are allowed. The v28 witnesses avoid this by choosing prefixes that exclude simultaneous occurrence of the indifferent atom, so at least one event indicator is fixed. This is the right level at which to formulate the converse.

I therefore withdraw the v27 criticism that the exact whole-schedule count is still schedule-specific within the fixed-clock interface. It is not.

### 2.2 The positive-noise physical classification is now exact and quantitative

Theorem `thm:positive-saddle` is a substantial improvement over the former compactness persistence argument.

The manuscript now treats the two-parameter family
[
Q_{gamma,kappa},
qquad
(gamma,kappa)in[6/25,13/50]	imes[0,1/1000],
]
with positive off-diagonal mass for (kappa>0), identifies an exact saddle through a cubic root, proves a global square factorization, checks the posterior coefficient signs, and recovers the same five contact-forced response rows with a nontrivial tie coordinate.

More importantly, Theorem `thm:physical-noise-form` derives the original Brownian target exactly as
[
gamma=rac14-rac{mu_1}{2},
qquad
kappa=rac{mu_1-mu_2}{2},
]
with (mu_1=mathbb E e), (mu_2=mathbb E e^2).

This is the correct common-signal structure. Replacing (mu_2) by (mu_1^2) would indeed amount to an unjustified unconditional-independence assumption, and the manuscript does not make that mistake.

The symmetry argument is also meaningful rather than cosmetic: reflection in the transverse coordinate changes the preparation bit while preserving the magnitude of the outgoing signal, and the mark lives in an independent center-of-mass coordinate. Within the stated preparation model, this supports the claimed label-independence of the distribution of the conditional error rate.

Thus the exact five-state decision classification and fixed-clock peak-twelve result genuinely hold throughout the stated positive-noise range (0<sigmale1/24), for each specified physical target.

I therefore also withdraw the v27 criticism that physical exact memory rests only on an unevaluated compactness gap.

### 2.3 The support-boundary discontinuity is a real new conclusion

Theorem `thm:reverse-jump` gives reverse-serial peak 10 at the ideal support-restricted target and peak 12 at every positive (kappa) in the proved rectangle.

This is one of the cleaner conceptual points of v28:

> exact realization complexity can jump at a support boundary even while the statistical law and minimax value vary continuously.

That observation is mathematically legitimate and useful. It is much stronger than a statement that one chosen compiler happens to use more states after adding noise.

---

## 3. Technical audit of the principal new arguments

### 3.1 Full-support saddle

I do not see a fatal algebraic defect in the displayed saddle proof.

The proof has the correct architecture:

1. isolate the relevant cubic root (r);
2. determine the tie parameter (t) through stationarity;
3. prove a global lower certificate on the diagonal through a square factorization;
4. use transverse monotonicity to force the minimizer onto the diagonal;
5. verify the Bayes coefficient signs for the two-point least-favorable prior;
6. use contact and stationarity to force the two formerly indifferent extreme coordinates;
7. transfer the resulting forced rows into the five-generator lower bound.

The parameter inequalities are deliberately overconservative but appear adequate on the stated rectangle. The exact-regression script checks the polynomial identities and the delicate sign cases, and the manuscript supplies analytic inequalities rather than replacing them by a grid.

This part is significantly better than a numerical saddle claim.

### 3.2 Physical target identification

The physical mixture calculation is coherent.

Given the stated preparation law, if (e) is the conditional sign-error probability shared by the two disjoint Brownian windows, then averaging the conditional Bernoulli pair gives the diagonal and off-diagonal probabilities displayed in the manuscript. The dependence through the common random signal is retained through (mathbb E[e^2]).

The strict full-support conclusion also follows from (0<e<1): (mu_1-mu_2=mathbb E[e(1-e)]>0).

I have one scope caution, not a correctness objection. The exact state counts are known-target statements. The tie probability depends on the target law through (gamma,kappa), hence ultimately through target-specific physical integrals. The manuscript is now explicit about this and gives an acquired-calibration proposition with finite counters and finite-bit approximation. That proposition, however, gives approximate score recovery, not exact recovery of the algebraic stochastic row. The paper should continue to keep these two notions sharply separate.

### 3.3 Facial scheduling theorem

Theorem `thm:facial-schedule` is correct in the form in which it is stated, but its mathematical status should be described accurately.

It is a **certificate theorem**.

The lower field (c(v)) is not an intrinsic quantity produced canonically from the experiment. It is defined as the largest certificate found inside a declared finite witness family. The upper field (r(v)) is produced from an explicitly supplied compatible residual family. Exactness occurs when the author supplies enough lower faces and a matching compatible upper realization.

This is useful and reusable, but it is not a classification theorem for causal memory.

The bottleneck dynamic program is elementary once the capacity field is known. The hard mathematics remains the discovery and proof of the contact-forced continuation faces.

That distinction matters greatly for venue assessment.

### 3.4 The all-orders theorem

The combinatorial logic of the proof is sound at the level I checked.

A nonserial interleaving must encounter either a (1/1) consumed-prefix configuration or a (2/1) configuration before one tape finishes. The manuscript supplies a 14-generator facial obstruction in both cases. The two serial paths avoid those obstructions and have compatible residual realizations of peak 12.

The proof therefore establishes the claimed exact **minimum over fixed declared clocks**.

The paper is also correct to say that this does not solve observation-dependent scheduling. A feedback scheduler is a different controlled protocol because the choice of which tape to read next can itself depend on retained observations and has a storage cost.

This is no longer a defect in the fixed-clock theorem; it is a boundary on the generality of the theory.

### 3.5 Reverse support jump

The ideal reverse upper construction uses support restrictions in an essential way: the first target report can be discarded because the second agrees with it almost surely. The lower bound then uses eight deterministic continuation vertices plus two separated mixed faces.

This is exactly the kind of phenomenon that can disappear under arbitrarily small full-support perturbation.

I find the conclusion plausible and structurally well motivated.

---

## 4. Why the paper is still below the four-journal level

### 4.1 The general theory is still a normal-form/certificate framework, not an intrinsic complexity theorem

This is now the main issue.

The paper's most general realization statements say, roughly:

- every finite controller admits a positive continuation factorization;
- minimax contact can force rows of that factorization;
- vertices and disjoint faces provide lower bounds;
- compatible residual functions provide upper bounds;
- a bottleneck recurrence optimizes over a finite schedule graph.

All of these are useful.

But the theory stops exactly where a foundational four-journal result would need to begin: it does not provide an intrinsic, computable, or structurally characterized invariant that equals causal memory for a substantial class of experiments.

In particular, (c(v)) depends on a chosen witness family. The theorem does not tell the reader how to obtain all necessary faces, whether the resulting lower field is complete, or when facial packing is exact. Likewise, the matching upper residual family is an external certificate.

Thus the general theorem is not an analogue of a rank theorem, a minimization theorem, or a classification theorem. It is a rigorous language for proving such results in examples.

For a specialist paper, that can be enough. For the four journals, the paper needs a theorem that turns the language into structure.

### 4.2 The deepest exact mathematics is still concentrated in one small bespoke experiment

The exact numbers 5, 10, 12, and 14 are derived for a very specific architecture:

- two candidate training preparations;
- binary report slots;
- one binary mark;
- five particular frozen events;
- a two-point least-favorable prior;
- a three-slot-by-three-slot validation schedule graph;
- a highly symmetric two-parameter target family.

The result is nontrivial, but its scale is tiny.

Revision 28 proves much more about this example than v27 did. It does not yet prove that the same contact/facial mechanism governs a broad hierarchy of experiments, or that memory exhibits a general law under increasing horizon, alphabet size, preparation number, or schedule complexity.

A four-journal version should not merely add another exact finite number. It should identify a structural theorem whose content becomes stronger as the experiment grows.

Examples of genuinely stronger directions would include:

- a class in which the saddle-contact capacity equals exact causal memory at every cut;
- a theorem deriving the complete capacity field from a geometric object associated with the saddle face;
- a scalable family with an exact asymptotic memory law;
- a nontrivial equivalence between causal memory and a recognized invariant of positive realization or experiment comparison.

At present the general theory does not deliver this.

### 4.3 The adaptive scheduling problem remains outside the theory

The authors are correct that report-dependent scheduling is a different interface.

Nevertheless, from the perspective of the title and conceptual ambition, it is also the natural next problem.

Once scheduling itself is a causal action, the experiment no longer reduces to choosing one path in a finite schedule DAG before observations. One needs a controlled scheduling theorem in which schedule decisions are part of the same retained state and are subject to the same contact/realization constraints.

That would be a substantial general theorem.

The present manuscript solves the static path problem exactly and explicitly carves the adaptive problem away. This is mathematically honest. It is also evidence that the current "memory of causal experiments" theory is not yet complete at the level suggested by the title.

### 4.4 The large-(N) side remains too coarse

The v27 report asked for a deeper large-(N) theory as one possible route to a higher-level paper. Revision 28 consciously chose the order/noise route instead.

That was a reasonable choice and should not be penalized as failure to answer every request.

However, the retained all-(N) result is still an endpoint/localization theorem based on empirical approximation and a growth estimate. It does not determine:

- a first nontrivial correction to the minimax value;
- the support law of least-favorable priors;
- a finite-(N) contact transition;
- a fluctuation or moderate-deviation regime;
- a scalable memory law coupled to (N).

Accordingly, the manuscript still lacks a second axis of depth that could compensate for the specialized finite-state nature of the exact v28 theorem.

### 4.5 The repository pipeline still demonstrates local rather than foundational reach

The v28 pipeline accounting is responsible and should be preserved.

The manuscript does **not** claim that the new finite-state theorem closes the independent Round-Seventeen gates. That is correct.

But the consequence is important for evaluation.

The repository ledger still records, among other things:

- A2: branch bundle, lattice rank, returned UNI, physical integration by parts, unsmoothed tail control, raw 4D density LLT;
- A3: exact predictable entropy, stopped-state map, compact rate sublevels, terminal contraction;
- A4: global kernel, Harris/drift, renewal resolvent, forced Mori–Zwanzig identity;
- B3: closed range, process CLT, correct Gaussian normalization, Mosco recovery;
- B4: law-hierarchy realizability, Nisio resolvent, m-dissipativity, graph core, nonlinear Trotter–Kato;
- C2: weighted strict dual, operator/form compression, rigidity, changing-filtration optional projection;
- D1: positive latent labels, labelled LDP, semigroup and typed contraction.

Revision 28 does not eliminate or materially simplify these gates.

Its new local proof edges are real:

physical symmetry -> exact target moments -> full-support saddle -> contact-rigid rows -> facial schedule capacities -> exact fixed-clock memory.

But that is a local branch of the program.

Calling the paper "Foundations" is defensible as an internal project label. It is still not justified by repository-level indispensability or by a theorem from which the major analytic branches flow.

### 4.6 The originality boundary remains insufficiently established for the conceptual claims

The literature crosswalk is more careful than before. It correctly acknowledges classical sources for:

- convex minimax and experiment comparison;
- finite-horizon belief recursion and controlled sensing;
- positive stochastic realization and invariant cones;
- nonnegative-rank geometry;
- incompletely specified sequential-machine minimization;
- finite-memory randomized testing.

This is good.

But the crosswalk also explicitly concedes that there is no complete proof-level non-overlap audit for the closest positive-realization and filtered-experiment literature.

That concession matters.

The broad conceptual claim is not the cubic calculation. It is the mechanism:

> minimax saddle contact forces otherwise Bayes-indifferent continuation coordinates, and those forced coordinates yield causal positive-realization lower bounds.

For a four-journal submission, I would expect the paper to isolate that mechanism as a theorem whose hypotheses and conclusion can be compared directly with the closest realization/filtered-experiment results, and then demonstrate a genuinely new consequence that those frameworks do not already encode.

At present the originality case is still inferred from a synthesis of known ingredients plus a sharp example.

That is not enough for the venue level under discussion.

### 4.7 The manuscript remains overpacked

The canonical article has grown to 59 pages and retains a very large theorem inventory:

- causal foundations;
- controlled minimax;
- exact one- and two-preparation saddles;
- physical collision construction;
- positive-noise saddle;
- schedule optimization;
- revelation;
- autonomous testing;
- finite-architecture certification;
- all-(N) localization;
- transport and consumers.

The 289-page complete manuscript and 842-page preserved development are valuable repository artifacts. They should have essentially no editorial weight in favor of publication.

The article would be stronger if it were organized around one theorem spine:

1. saddle contact;
2. positive continuation geometry;
3. an intrinsic schedule/memory theorem;
4. one physical example demonstrating a phenomenon not visible from value continuity.

The current manuscript still reads partly like a consolidation of a large research program rather than a maximally distilled top-journal paper.

---

## 5. A concrete conceptual weakness in the new facial-capacity formulation

I want to emphasize this because it is the most important point for a next revision.

Definition `def:facial-certificate` defines a lower capacity from a *certificate*. Theorem `thm:facial-schedule` then optimizes those certified capacities over paths.

But a lower certificate is only as strong as the witness family supplied by the analyst.

Thus the object denoted (c(v)) is not, in the current theorem, an invariant of the experiment. It is an invariant of the experiment **plus a chosen finite stock of discovered certificates**.

The manuscript partly acknowledges this by saying that facial packing need not always be exact.

For the specific v28 experiment this is fine, because the authors exhibit enough witnesses and matching upper residuals.

For the general theory this is a serious limitation.

A foundational theorem should replace "find a good family of faces" by something closer to one of the following:

- (c(v)) equals the minimum cardinality of a generating set for the entire contact-forced continuation set;
- (c(v)) equals a positive-rank / extension-complexity / covering invariant with a theorem of equivalence;
- the contact-forced continuation set has a canonical facial decomposition from which (c(v)) is computable;
- a broad class of saddle faces is shown to be facially complete, so the packing lower bound always matches a compatible realization.

Without such a result, the general theorem is a proof template.

A beautiful proof template is not the same thing as a new theory of causal memory.

---

## 6. Known-target exactness versus acquired-target implementation

The manuscript is much more careful here than earlier versions, but the distinction should be elevated in the main theorem statement.

For a specified (Q_{d,sigma}), the exact optimal stochastic row uses a target-dependent tie probability. In the atomic stochastic-row convention, this is a valid exact row.

An experimenter who does not know the target parameters has to acquire them. Proposition `prop:physical-acquisition` then gives:

- a calibration concentration bound;
- a score-loss bound (9a+2^{-b});
- explicit counter-state costs;
- explicit finite-bit workspace.

This is good resource accounting.

But the acquired controller is an **approximate-score** controller. It is not an exact realization of the algebraic optimum with the same five/twelve state numbers.

That should remain visually explicit throughout the abstract/introduction/conclusion. The phrase "exact physical memory" is correct only under the specified-target convention.

I do not regard this as a theorem error because the manuscript states the convention. I regard it as an important semantic boundary for readers outside the repository.

---

## 7. What would materially change my assessment

A further revision should not respond by adding more regression files, more preservation manifests, or another isolated exact state count.

One genuinely strong route would be enough.

### 7.1 Upgrade facial scheduling from a certificate theorem to an intrinsic theorem

Prove that for a nontrivial class of finite causal experiments, the exact memory profile is characterized by a canonical geometric invariant of the saddle-forced continuation set.

The theorem should tell the reader what the invariant is and why it is complete, not merely how to verify a lower bound after discovering the right faces.

This is the most direct route.

### 7.2 Solve controlled/adaptive scheduling as part of the same state complexity problem

Let the next tape/action be chosen from retained observations, charge its protocol state, and obtain an exact or structurally sharp memory theorem.

If the fixed-clock optimum 12 changes under feedback scheduling, classify the change.

If it does not, prove an architecture-uniform adaptive lower bound.

Either result would make the current scheduling theorem substantially more intrinsic.

### 7.3 Produce a scalable family, not another finite instance

Generalize the contact/facial mechanism to a parameterized sequence of experiments and derive an exact growth law for memory or schedule bottlenecks.

A theorem with nontrivial asymptotic scaling would materially change the perceived depth.

### 7.4 Give the theory a real downstream consumer

It is not necessary for GTF-I to close the whole repository.

But if an A2/B4/C2 theorem genuinely used the new saddle-realization theorem to replace an otherwise independent proof obstruction, that would strengthen the claim that this is a foundations paper rather than a local branch.

The dependency should be mathematical and indispensable, not documentary.

### 7.5 Complete a theorem-level originality comparison

The paper should explain, at the level of hypotheses and conclusions, why the central contact-forced realization theorem is not already contained in classical stochastic realization, filtered experiment comparison, incomplete sequential-machine minimization, or finite-memory testing.

A bibliography table is not enough for the venue claim.

---

## 8. What I would not request

I would not request:

- more source hashes;
- more build receipts;
- more negative-control executions;
- another exact regression table;
- more preservation pages;
- a larger archived companion;
- another compactness-only robustness argument;
- another fixed finite example with a new integer state count.

Revision 28 already has enough infrastructure.

The next advance must be conceptual.

---

## 9. Editorial comments

1. The abstract is much improved because it now states the fixed-clock quantifier and separates the zero-noise reverse result from the positive-support theorem. Keep that precision.

2. The phrase "all declared orders" should always remain paired with "externally declared" or "fixed clock." The paper does this in most places; do not let shorter prose collapse the distinction with feedback scheduling.

3. The known-target convention should be stated in the main theorem summary, not only in resource remarks.

4. The literature section should be tightened. The strongest useful sentence is not a list of classical areas; it is a theorem-level statement of what contact adds to positive realization.

5. The paper would benefit from one diagram showing:
   unrestricted saddle -> forced continuation set -> cut capacity -> schedule bottleneck -> physical memory.
   This would replace several pages of repeated roadmap prose.

6. The preserved-development page count should not be used rhetorically as evidence of depth. It is archival provenance.

7. The v28 response correctly says that the large-(N) route was not pursued. Keep that honest rather than adding weak asymptotics merely to answer a checklist.

---

## 10. Final assessment

Revision 28 is a serious revision.

It closes the two most important concrete gaps in v27:

- the exact memory statement is now optimized over every fixed declared validation order;
- the positive-noise Brownian model now has an exact full-support classification on the entire stated noise range.

It also adds a clean support-boundary memory jump and a reusable language for schedule lower certificates.

These are genuine achievements.

I therefore would not repeat the earlier criticism that the paper is merely an infrastructure document, and I would not claim that its principal new results are numerically unsupported or obviously false.

The remaining problem is deeper and more structural.

The paper's general machinery is still principally a framework for constructing certificates, while its sharp exact theorems remain tied to a specially engineered finite experiment. The schedule capacity is not yet an intrinsic invariant, adaptive scheduling is outside the theory, the large-(N) side remains coarse, the major repository pipeline gates remain independent, and the originality boundary of the general contact/realization principle is not yet established at theorem level.

That combination is not sufficient for Annals / Inventiones / JAMS / Acta.

**Recommendation: Reject at the four-journal level in the present form.**

I would regard a substantially condensed version centered on the full-support saddle, exact schedule classification, and support-boundary jump as a credible strong-specialist submission. A future four-journal version would need a genuinely intrinsic realization-complexity theorem or comparably broad structural advance.

---

## Referee checklist

- Repository confirmed: `TrillionniumFoundation/theta-theory`.
- Latest General Theta Foundations I revision found: v28.
- Reviewed `revision/general-theta-foundations-i-v28-referee-ready-2026-09-24`.
- Reviewed head pinned at `cdc749027c5f7a6f66c572ea498cd15e1b1a3391`.
- Compared v28 against v27 referee-ready branch.
- Confirmed v28 is four commits ahead of the v27 referee-ready base and contains the new causal-response package.
- Read the v28 response to the r11/r12 reports.
- Read the full-support saddle proof.
- Read the exact Brownian target-identification proof.
- Read the facial scheduling theorem.
- Read the all-twenty-fixed-order theorem.
- Read the ideal reverse-order support-jump theorem.
- Re-read the inherited five-state and forward-serial twelve-state arguments.
- Re-read the saddle-face/positive-realization normal form used by the lower bounds.
- Re-read the Round-Seventeen repository dependency ledger.
- Checked that v28 does not claim historical A2/B4/C2 aggregate closure.
- Checked that v28 does not claim a report-dependent scheduling theorem.
- Checked that v28 does not claim the ideal ten-state reverse value is the global ideal optimum over all orders.
- Checked that v28 does not claim all nonserial orders have exact peak fourteen.
- Independently reconstructed the key finite strict-channel counts used in the schedule certificates: 8, 10, 12, and 8 at the relevant cuts.
- No short fatal counterexample found to the v28 full-support saddle.
- No short fatal counterexample found to the v28 physical target mixture.
- No short fatal counterexample found to the fixed-clock 12-versus-14 schedule separation.
- The remaining negative recommendation is based on four-journal breadth, intrinsicness, generality, originality boundary, and repository-wide foundational reach rather than an asserted elementary algebraic failure.
