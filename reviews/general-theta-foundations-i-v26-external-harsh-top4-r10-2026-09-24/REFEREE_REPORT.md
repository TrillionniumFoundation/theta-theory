# Tenth Independent External Harsh Referee Report

## General Theta Foundations I: Causal Experiments, Finite-Memory Control, and Exact Minimax Laws — Revision 26

**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed branch:** `revision/general-theta-foundations-i-v26-referee-ready-2026-09-24`  
**Frozen reviewed branch head:** `466bfcdcb8b7d594d3924dbfa82b4c6e29368858`  
**Recorded native source commit:** `92fd55a9541acfc14665f6275b455dc148fda2d3`  
**Reviewed predecessor:** revision 25 at `818ca30bab506cfedaf6aee4c32bedff70c1e251`  
**Controlling prior report:** `reviews/general-theta-foundations-i-v25-external-harsh-top4-r9-2026-09-24/REFEREE_REPORT.md` at `568301ff5d8991af9a99a478371c1c4993d0bcd1`  
**Canonical article:** 40 pages  
**Complete mathematical manuscript:** 177 pages  
**Complete preserved development:** 730 pages  
**Review date:** 24 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Review type:** independent external-referee-style, pipeline-aware harsh review

# Recommendation

## Reject in the present form at the requested top-four general-mathematics standard

Revision 26 is the first revision in this sequence for which several of my previous structural objections have to be withdrawn rather than merely softened.

This is a substantial revision. It does not respond to the ninth report by adding more certificates, larger preservation volumes, or a longer metadata graph. It adds new mathematics at exactly several of the places where the previous report asked for it:

1. a genuine finite-register controlled family with informative, non-dominating sensing actions and a strict gap between a legal (K)-label controller and a free convexification over complete controllers;
2. an exact two-preparation marked minimax value (U2), with a full-parameter lower certificate and a matching least-favorable prior;
3. a continuous two-preparation target family, rather than a single isolated (N=2) numerical point;
4. a restored A0–A5 / predictive-quotient / acquired-resolution / causal-transport spine in the canonical article;
5. a theorem-level local downstream consumer using the exact (U2) value and the acquired transport theorem;
6. an improved theorem-level literature comparison with active testing, controlled sensing, imperfect recall, and finite-memory testing.

I have not found a fatal counterexample to the new mathematical core in the source I inspected. In particular, the finite-memory routing ceiling, the free-selector gap, the two-preparation saddle factorization, the posterior coefficient sign argument, and the stated causal transport accounting appear internally coherent. The build and exact-regression records are also consistent with the source, although I do not treat those records as proof certification.

Therefore this rejection is no longer based on the objections that drove the v24 and v25 reports. I do **not** maintain that the paper has failed to impose a real finite memory constraint. I do **not** maintain that the marked theory stops at (N=1). I do **not** maintain that the canonical article has abandoned the repository's own General Theta Foundations blueprint. Those criticisms are obsolete for v26.

My remaining objection is narrower and more demanding.

The revision now contains a collection of serious exact results, but I still do not see a single unifying theorem of the conceptual reach expected at Annals/Inventiones/JAMS/Acta. The strongest general finite-memory statement is an exact Bellman/supersolution formulation for a **specified profile and interface**; the genuinely new exact finite-memory value is then proved for a specially engineered routing bottleneck. The strongest exact multi-preparation result is an impressive but highly structured (N=2) marked-product saddle. The restored foundations theorems make the article architecturally coherent, but their general mechanisms are primarily conditional expectation, quantization, contraction, coupling, and explicit resource bookkeeping under hypotheses that already encode the relevant rate. The physical result identifies the exact score on the entire (W >= 12) segment, but not the least width or the hard (3 <= W <= 11) part of the sample-memory Pareto frontier. Finally, the new local consumer is real, but the repository-wide eleven-paper DAG remains multiple-root and does not yet make this paper an indispensable mathematical foundation for the major A2/B4/C2 chains.

This is now a strong specialized paper in causal statistical experiments, finite-state control, exact minimax calculations, and a carefully priced physical application. The issue is no longer whether there is substantive mathematics. There is. The issue is whether the present bundle of results has been compressed into a theorem of sufficient breadth, invariance, or downstream necessity to justify a top-four general-mathematics placement.

My answer remains no.

# 1. Provenance and scope of this review

I reviewed the actual v26 referee-ready branch frozen above, not an earlier working branch. The branch is four commits ahead of the reviewed v25 head. The publication marker identifies the native source commit `92fd55a...`; the referee-ready branch head is `466bfcdc...`.

I read the 40-page canonical source and, in particular, the following new or materially revised modules:

- `foundations.tex`;
- `controlled-memory.tex`;
- `two-preparation-saddle.tex`;
- `two-preparation-family.tex`;
- `integer-revelation.tex`;
- `consumer-transfer.tex`.

I also re-read the inherited controlled dual, marked (U1) theorem, physical bridge, physical resource compilation, joint revelation theorem, and the relevant parts of `main.tex`.

For revision provenance and program context I inspected:

- `RESPONSE_TO_REFEREE.md`;
- `PROOF_STATUS.json`;
- `PIPELINE_STATUS.json`;
- `RESOURCE_LEDGER.md`;
- `HISTORY_AUDIT.md`;
- `LITERATURE_CROSSWALK.md`;
- `evidence/BUILD_RECEIPT.json`;
- `evidence/THEOREM_LOCATIONS.json`;
- the General Theta Foundations blueprint at `foundations/general-theta/General_Theta_Foundations_v0.1.md`;
- the original implementation note `foundations/general-theta/GTF_I_IMPLEMENTATION_2026-09-22.md`;
- the repository-wide Round-Seventeen proof-dependency ledger and status;
- the complete ninth external report on v25.

The Round-Seventeen ledger records the principal historical DAG as

`A2 -> A3 -> A4 -> C2 -> D1`

on the Sinai side, and

`B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`

on the hard-sphere side, while its historical A1 remains an independent root. The v26 pipeline file is appropriately explicit that historical A2 remains independent and that B4, broad C2, and eleven-paper closure are not claimed.

The v26 build receipt records a successful 40-page article build, 177-page complete manuscript, 730-page complete preserved development, ordinary/optimized agreement, 24 negative-control executions, exact predecessor-page comparisons, and the v24/v25/v26 regression suites. I regard these as useful evidence that the submitted source and artifact are reproducible. I do not regard them as independent proof verification, originality clearance, or evidence for journal significance.

I also performed independent algebraic spot checks of the new U2 constants and the displayed factorization modulo `2 r^3 + 25 r^2 - 3 = 0`. The positive root is `r = 0.341769415564857...`, the stated `tau = 0.168823644779073...`, and `U2 = 0.426112778796656...` agree with the formulas in the source. This is a consistency check, not formal verification.

# 2. Disposition of the ninth report

The ninth report explicitly said that the next useful revision should contain theorem-level progress, not more certification. Revision 26 does that. To avoid moving the goalposts, I record the disposition point by point.

## 2.1 Route A / request 15.1: informative controlled selection under actual finite memory

**Materially resolved.**

Theorem 7.1 gives an exact dynamic optimization at a prescribed clocked register profile. More importantly, Theorem 7.2 is not merely a formulation: it gives an exact controlled family with incomparable actions and a genuine finite bottleneck,

`V_{m,K} = 1 / (2 ceil(m/K))`,

while a free ex ante mixture over complete K-label controllers has value

`Vbar_{m,K} = K / (2m)`.

The gap is strict when K does not divide m, for example

`V_{3,2} = 1/4 < 1/3 = Vbar_{3,2}`.

The controller's chosen action is separately retained in an m-state buffer, and the profile is explicitly `(1,K,m,3,6,3)`. This is therefore not the old unrestricted policy-tree theorem disguised as a finite-memory theorem.

The full-support perturbation result also removes the objection that the separation is caused only by zero-probability reports.

The old statement "the paper has no exact informative finite-memory controlled theorem" is no longer tenable.

## 2.2 Route B / request 15.2: original collision sample-memory frontier

**Substantially strengthened, but not closed.**

The exact two-preparation value is now determined on the physical segment W >= 12. This is much stronger than the old deterministic lower construction.

However, the least peak width at two preparations and the complete widths 3,...,11 frontier remain open. The manuscript says so clearly.

Thus the physical result now gives an exact vertical segment of the frontier, not the full Pareto boundary.

## 2.3 Route C / request 15.3: exact multi-preparation marked theory

**Resolved at N=2, including a continuous family.**

The exact original value U2(b,Q*) is proved, and Theorem 12.1 gives an interval of exact N=2 target biases

`6/25 <= gamma <= 13/50`.

The old criticism that the exact marked theory stops at one training preparation is obsolete.

What remains open is not "do N=2" but whether the N=1,2 formulas expose a structural mechanism that persists for N >= 3, large N, or a broader class of experiment families.

## 2.4 Request 15.4: arbitrary integer revelation laws

**Meaningfully improved, still partial for K >= 3.**

The paper correctly distinguishes the uniform-prior balanced-partition value from the minimax value when K does not divide m. Proposition 14.1 gives a low-reveal exact range and the perfect-reveal endpoint, and Theorem 14.2 gives the complete K=2 law

`V_er(N,m,2) = min(2 w b rho, w)`.

This is a genuine correction and strengthening of the divisible model.

The remaining K >= 3, high-reveal range is explicitly left as an exact constrained optimization rather than filled with an unsupported formula.

## 2.5 Route D / request 15.5: restore the General Theta foundations spine

**Resolved architecturally.**

The canonical article now begins from A0-A5, prepared path laws, predictive quotients, barycenters, checkpoint resolution, an online resolution theorem, causal morphisms, and an acquired transport theorem.

This matches the direction of the repository blueprint:

`prepared causal experiment -> predictive quotient -> causal simulation -> finite-resource resolution`.

I withdraw the v25 objection that the title and the canonical article describe materially different papers.

The remaining question is not whether the spine is present. It is whether the mathematics in that spine rises to the requested venue level.

## 2.6 Route E / request 15.6: theorem-level downstream necessity

**Resolved locally, not program-wide.**

Theorem 18.1 is an actual proof dependency. It uses the exact (U2) margin, the finite-precision implementation, the physical bridge, and the acquired causal transport theorem to obtain a confidence result with explicit preparation and memory costs.

This is materially better than a metadata edge.

The paper correctly does not claim that A2, B4, or C2 now depends on this result. Accordingly, the local consumer should be credited, while the stronger program-wide indispensability claim remains open.

## 2.7 Request 15.7: adjacent literature

**Substantially improved.**

The introduction and crosswalk now discuss Chernoff, Smallwood–Sondik, Naghshvar–Javidi, Nitinawarat–Atia–Veeravalli, recent imperfect-recall optimization, and recent memory-constrained adversarial testing. The paper explicitly declines to claim novelty for Bellman recursion, adaptive sensing itself, or the mixed/behavioral distinction.

Norberg's filtered-experiment comparison remains without a complete proof-level non-overlap audit, but the manuscript now states that limitation rather than claiming a priority theorem it has not established.

Literature positioning is no longer a principal reason for rejection.

# 3. Source-level mathematical checks

## 3.1 The finite-profile dynamic theorem is logically clean

For a fixed legal interface, the parameterwise occupation bundle `x_theta(h,s)` is an offline design state. The executing controller does not receive x, theta, or an unrecorded history.

The recursion

`B_T(x) = min_theta sum_{h,s} x_theta(h,s) r_theta(h,s)`

and

`B_t(x) = max_{q in Q_t} B_{t+1}(T_{t,q} x)`

therefore optimizes a single common stochastic prescription at each scheduled stage.

I do not see a hidden parameter-dependent runtime oracle in this statement.

The Lipschitz estimate follows from contraction of l1 mass under stochastic matrices. Compactness of the row simplices and of the parameter space gives the stated attainment under the manuscript's continuity assumptions.

The supersolution identity is exact, although mathematically it is close to the Bellman principle itself rather than an unexpected duality theorem.

The autonomous/shared-row caveat is also correctly stated: a row reused at different times must be selected once and held fixed; maximizing it afresh at each time would solve a different problem.

## 3.2 The routing converse has the right bottleneck constant

For `p_i = sum_s E(s|i) D(i|s)`, the score for at least one value of the hidden bit is at most `p_i/2`.

Let `L = ceil(m/K)`. If every `p_i > 1/L`, then for each i some decoder row satisfies `D(i|s) > 1/L`. A single stochastic row can contain at most `L-1` such indices, while `K(L-1) < m`. This yields the claimed upper bound.

Balanced fibers attain it.

For the free mixture, the uniform-prior calculation `(1/m) sum_i p_i <= K/m` is correct, and the cyclic interval mixture attains the resulting `K/(2m)` value.

The theorem therefore gives a real mixed-versus-behavioral resource gap, not just an example of adaptive sensing.

## 3.3 The positive-noise routing persistence is consistent

Each of the two training rows moves by at most epsilon in total variation. Coupling until the first discrepancy gives at most `2 epsilon` path disagreement. For a reward in [-1,1], the value of either controller class moves by at most `4 epsilon`. Thus the gap decreases by at most `8 epsilon`, matching the stated condition `epsilon < Delta_{m,K}/8`.

I find no constant mismatch here.

## 3.4 The exact U2 lower certificate is genuinely global

Theorem 11.1 does not certify only a grid or only the diagonal p=q.

With `u = (p+q-1)^2` and `v = (p-q)^2`, the new response has score `G(u,v) = H(u,v) + tau J(u,v)`. The cubic equation gives `J(r,0)=0`, and tau is chosen so that the u-derivative vanishes at r.

Modulo the cubic, the displayed factorization is

`G(u,0)-v2 = (u-r)^2 (75+12r+6u-37r^2-74ru) / (64 r (3r+25))`.

The bracket is positive on the claimed region, and the manuscript's derivative bounds `partial_v H >= 7/32` and `partial_v J >= -3/64` give strict transverse monotonicity after `0 < tau < 1`.

Thus the lower bound is a full-square statement.

## 3.5 The U2 upper bound does not silently restrict the response class

Under the two-point diagonal prior, conditional on the total number S of ones among the four training report bits, the ordering of those bits and the two independent marks are parameter-independent.

The manuscript then evaluates the signed predictive coefficients for every validation coordinate. The sign pattern

`(0,-,+,+), (+,-,+,+), (+,+,+,+), (+,+,-,+), (+,+,-,0)`

selects exactly the stated response. Off-support validation atoms have nonpositive coefficient because the target gives them zero mass.

Thus grouping by S is a proof device for the Bayes coefficients, not an imposed restriction on competitors.

Equality at the two prior support points closes the minimax match.

I do not see the old "symmetric response only" loophole.

## 3.6 The continuous N=2 family is a theorem, not a perturbative remark

Theorem 12.1 proves an explicit root, response parameter, square factorization, transverse monotonicity, and coefficient sign pattern uniformly over `6/25 <= gamma <= 13/50`.

This deserves more credit than a stability corollary around gamma=1/4. It is an exact continuous saddle family.

## 3.7 The physical W >= 12 exactness is correctly one-sided in width

The construction fits in peak twelve.

The converse uses the admissible common-garbling private subfamily and the architecture-uniform outer dual, so it applies even to larger-memory or feedback competitors. Consequently the exact score for W >= 12 follows.

This does **not** imply that width twelve is necessary. The paper explicitly says so.

That distinction is important and correctly maintained.

## 3.8 The integer revelation correction is mathematically important

For `m = Kq+s`, the balanced-fiber Bayes value is

`B_{m,K} = 1 - ((K-s)q^2 + s(q+1)^2)/m^2`.

The manuscript correctly observes that this need not be minimax-attainable without a stored partition selector. The low-reveal initialization is nonnegative exactly in the stated range, and the perfect-reveal upper bound follows from the largest unavoidable fiber.

The complete K=2 formula then gives a real phase transition for odd m.

This section improves the conceptual honesty of the resource theory: Bayes symmetrization and implementable finite-memory minimax are not conflated.

## 3.9 The acquired causal transport theorem is careful about feedback

Theorem 3.4 couples the exact and approximate transducers only while their **external visible histories agree**. Therefore a downstream controller, even if discontinuous as a function of an internal belief coordinate, receives identical inputs before the first discrepancy and can use the same randomization.

This avoids a common but serious mistake: comparing two approximate posteriors and assuming that an arbitrary feedback policy must choose the same action at nearby beliefs.

The resulting defect bound

`Delta = min(1, epsilon_mod + eta + sum_{t<T}(epsilon_t + L_t e_t + b_t a))`

and the state product `C_cal R_t M_t K_t` are consistent with the declared execution model.

Again, I find this careful and useful.

# 4. The central remaining objection: the general finite-memory theorem is exact as a formulation, not yet structural as a theory

The paper's strongest new conceptual theme is that experiment choice and retained continuation are simultaneous resources.

This is the right theme.

But there is a distinction between:

1. writing the exact optimization for a specified finite interface; and
2. obtaining a structural theorem for a broad resource class.

Theorem 7.1 does the first.

Once the architecture, scheduled cuts, legal visible inputs, and row-sharing constraints are fixed, the occupation bundle gives an exact dynamic program. This is valuable because it prevents illegal posterior access or free policy-tree mixing.

But mathematically the theorem is still the principle of optimality applied to a very large design state. Its supersolution formula is attained by the value function itself. It does not reduce the complexity of the constrained problem, reveal a convex geometry comparable to the unrestricted posterior-predictive dual, or characterize the outer optimization `V_out(R) = sup_{A in A(R)} V(A)` over architectures satisfying a resource budget.

The new routing theorem then supplies one exact nontrivial family. This is the actual novelty-bearing finite-memory result.

That family is good, but it has an important limitation already acknowledged by the authors: (K) is a bottleneck coordinate, not the uniform peak. The chosen sensing action is kept in a separately charged (m)-state buffer. The exact profile is
(1,K,m,3,6,3).

Thus as (m) grows, the construction does not exhibit a separation at uniformly bounded total peak memory. It exhibits a sharp multicut tradeoff in which one cut is restricted to (K) labels while another cut grows with (m).

There is nothing wrong with this theorem. The paper states the resource profile honestly.

But this is why I do not regard it as a general finite-memory control duality theorem of top-four breadth. It is a sharp bottleneck theorem inside a larger exact but non-simplified dynamic program.

A genuinely structural advance would identify some invariant of a causal experiment and a memory profile that controls the constrained value across a broad class of interfaces, or derive a nontrivial dual/relaxation with matching conditions beyond a single routing geometry.

Revision 26 has crossed from "the finite-memory problem is missing" to "the finite-memory problem is present but not yet organized by a general theorem."

That is real progress. It is also the main remaining limitation.

# 5. The exact (U2) theorem is impressive but still an algebraic island

Theorem 11.1 is the cleanest exact calculation in the revision.

It solves a problem that v25 explicitly left open. The proof has a good primal/dual structure:

- choose a response with two randomized extreme-count rows;
- reduce the lower bound to a polynomial in (u,v);
- force a double contact at (u=r,v=0);
- prove positivity globally;
- choose the matching two-point prior;
- verify the sign of every predictive coefficient.

This is genuine minimax mathematics.

The continuous (gamma)-family then shows that the result is not one isolated target.

Nevertheless the mechanism is still tightly tied to this marked Bernoulli product model. The same five-event pattern and the same diagonal two-point geometry survive on a relatively short target interval. There is no recurrence in (N), no description of what replaces the cubic at (N=3), no asymptotic law, no phase diagram in (N), and no theorem characterizing which experiment families admit this finite-support saddle structure.

Again, I am not asking the authors to solve (U_N) for every (N) as a matter of completeness. The issue is conceptual leverage.

For a top-four paper, one hopes that an exact (N=2) calculation reveals a principle that is visibly larger than the calculation itself.

At present I see a very well executed algebraic saddle, but not yet the invariant that would turn the calculation into a general theory.

# 6. The foundations spine is now present, but much of its general mathematics remains conditional packaging

This section is much improved, and the v25 title objection should be withdrawn.

A0–A5 are sensible and prevent many category errors:

- resource costs are tied to the actual experiment;
- parameter-dependent tables are not free constants;
- predictive and inferential objects are separated;
- the future-test quotient is not automatically a global sufficient statistic;
- a simulator's memory multiplies the downstream controller's memory unless a quotient is proved.

The predictive quotient theorem is also stated with appropriate measurable-realization caveats.

The problem is not correctness. The problem is top-four novelty.

Several of the central general results have the following form.

## 6.1 Checkpoint resolution

The exact checkpoint objective is finite-center squared quantization under the actual acquired law. Randomization does not improve it.

This is clean, but the mathematical engine is classical conditional-mean reduction and vector quantization.

## 6.2 Matched online (M^{-2/d}) law

Theorem 3.2 assumes:

- a (d)-dimensional covering-number upper bound;
- a contraction factor rho < 1;
- a Lipschitz prediction map;
- an acquired small-ball upper-mass bound of order (a^d).

Under these hypotheses the (M^{-2/d}) lower and upper rates follow by the standard packing/quantization logic and stable repeated projection.

This theorem is useful because it forces the rate to refer to the **acquired law** and gives a causally updatable encoder.

But the exponent is substantially encoded in the hypotheses. The theorem does not derive the effective dimension, the small-ball exponent, or the contraction from the abstract causal experiment.

## 6.3 Joint transport

Theorem 3.4 is a careful error budget:
calibration error + state recursion + output-kernel stability + model mismatch + product memory.

This is exactly the kind of theorem a program needs operationally.

But its proof is a coupling/union-bound argument once the stability recursion and kernel bounds are supplied.

The manuscript correctly does not claim that such tools are new.

The consequence for editorial assessment is important: the foundations layer now makes the paper coherent, but it does not by itself supply the missing top-four conceptual theorem.

A stronger foundations result would derive a nontrivial resource monotonicity, equivalence, or sharp lower/upper law from the object/morphism structure itself, rather than packaging classical mechanisms after their decisive geometric hypotheses have been assumed.

# 7. The physical theorem is now exact in score but not in memory

The exact physical two-preparation score on (W >= 12) is a real advance.

The paper now has:

- exact (U1);
- exact (U2);
- a self-contained positive-noise collision presentation;
- a peak-twelve implementation;
- a universal upper bound from the common-garbling subfamily.

This makes the physical application much stronger than in v24 or v25.

But the paper's resource language naturally raises the missing inverse question:

> how much memory is actually necessary to attain the exact two-preparation score?

The current answer is only:
`W >= 12  =>  exact ideal score = U2`.

It does not say whether (W=12) is sharp. It does not exclude (W=11), (W=8), or another smaller width. The entire region (3 <= W <= 11) is still outside the exact frontier.

This matters more in v26 than it did in v25 because finite memory is now in the title and has become a central mathematical theme.

A nontrivial width lower bound for the original physical model would connect the new finite-memory control perspective to the flagship collision example much more tightly.

# 8. The repository-wide pipeline is preserved honestly, but it does not yet make this paper indispensable

The pipeline accounting in v26 is one of its strengths.

The authors do not use the size of the repository as a substitute for a theorem. The new `PIPELINE_STATUS.json` says:

- historical A2 is independent;
- B4 aggregate closure is false;
- broad C2 aggregate closure is false;
- eleven-paper closure is false.

The Round-Seventeen proof-dependency ledger independently confirms that the main historical chains retain their own hard gates in Fourier/LLT, LDP, semigroup, belief-filter, strict-dual, and phase-contraction analysis.

The new consumer theorem is therefore exactly what the response says it is: a **local** theorem-level consumer.

I credit this.

But for the word "Foundations" to gain programmatic force beyond article architecture, I would expect a later major theorem to use the new predictive quotient, constrained controlled value, or causal transport theorem in a way that replaces a genuinely independent derivation.

At present the flagship historical chains do not do this.

This is not a logical defect in v26. A paper can be foundational without already being cited by its descendants.

It does, however, remove one possible source of top-four significance. The article must therefore reach that level on the intrinsic force of its own main theorem.

I do not think the current collection quite does so.

# 9. Literature positioning is now responsible

The v26 introduction is notably more disciplined than earlier versions.

It explicitly states that:

- Bellman recursion and piecewise-linear belief geometry are classical;
- adaptive experiment choice is classical;
- controlled versus open-loop sensing has an established literature;
- imperfect-recall mixed/behavioral separation is classical;
- finite-memory testing and randomization have a long history;
- general filtered-experiment comparison is not claimed as an invention.

The comparison with Naghshvar–Javidi and Nitinawarat–Atia–Veeravalli is particularly important because it prevents the strict adaptive example from being advertised as the novelty.

The recent memory-constrained adversarial testing and imperfect-recall optimization literature also makes clear that finite-state stochastic decision problems remain active.

The unresolved Norberg boundary should stay exactly as it is: a limitation on the breadth of the originality claim, not a hidden assertion of non-overlap.

I would not reject v26 merely because the Norberg proof-level comparison remains incomplete, since the manuscript no longer claims priority for general filtered comparison.

# 10. The paper is now coherent, but the central theorem hierarchy remains diffuse

The 40-page canonical article is not bloated in the sense of the old preserved volumes.

Its difficulty is different.

There are many theorem families:

- predictive quotient;
- online resolution;
- causal transport;
- unrestricted controlled duality;
- finite-profile dynamic optimization;
- routing gap;
- exact (U1);
- exact (U2);
- continuous (U2(gamma));
- physical realization;
- revelation laws;
- finite-architecture subdivision;
- autonomous finite-memory comparison;
- transported confidence consumer.

Each is connected to the others, but no single statement visibly dominates the paper in the way a top-four general paper usually needs.

The title now matches the subject, but the theorem hierarchy still reads as an integrated research program rather than one decisive theorem with a chain of consequences.

That difference is editorial rather than formal.

At a strong specialized probability/statistics/information/control venue, breadth of this kind can be a strength. At the requested four general mathematics journals, the same breadth needs a correspondingly strong unifying mathematical principle.

I do not yet see it.

# 11. What has materially changed in my assessment since v25

It is important to state this explicitly.

After v25 I viewed the paper as a focused controlled-experiment article that did not yet solve its own finite-memory controlled problem and had drifted away from the repository's foundations blueprint.

After v26 I no longer hold that view.

Revision 26 is now a coherent foundations article in the sense that:

- the object and resource conventions are in the main paper;
- finite-memory control is not replaced by unrestricted policy-tree convexification;
- multi-preparation exact minimax theory exists;
- the physical experiment consumes those values exactly;
- a local downstream theorem uses the transport layer.

This is a major improvement.

If the editorial target were simply "publishable mathematical contribution," my report would be substantially more favorable than the previous one.

The negative recommendation survives only because the requested target is Annals/Inventiones/JAMS/Acta and because I still regard the new results as several exact islands connected by a careful framework, rather than one theorem of exceptional general reach.

# 12. Principal requests for any future top-four resubmission

I would strongly discourage another revision whose principal contribution is more regression coverage, more preservation evidence, another special finite table, or another response document.

The current paper already has enough infrastructure.

A future revision aimed at the same venue level should add **synthesis**, not volume.

The following are examples of mathematically relevant routes. I do not require all of them.

## 12.1 A structural constrained-control theorem beyond one routing geometry

The exact routing law is a strong example. The next step would be a theorem characterizing a nontrivial class of finite-memory controlled experiments.

For example, one could seek a dual or sharp relaxation for (V^{
m out}(R)), an invariant of the experiment/profile that controls the loss from unavailable persistent mixing, or a theorem identifying when the nonlinear occupation program collapses to a tractable finite-dimensional object.

The point is not computational efficiency alone. The point is a reusable mathematical structure.

## 12.2 A genuine physical sample-memory converse

Determine the least peak at (N=2), or exclude a nontrivial interval of widths below twelve with a matching or nearly matching construction.

This would fuse the finite-memory theory with the physical collision model instead of leaving them linked mainly in the forward direction.

## 12.3 A structural law in the marked preparation number

The (N=1) and (N=2) saddles now provide enough exact data to ask for a recurrence, phase structure, asymptotic law, or classification of extremizing priors/responses.

An (N=3) formula by itself would be less interesting than a theorem explaining why the two-point diagonal saddle and finite event alphabet persist or fail.

## 12.4 A foundations theorem whose conclusion is not already encoded in its metric hypotheses

The online (M^{-2/d}) theorem is correct, but its dimension and mass assumptions already carry the rate.

A stronger result would derive an intrinsic predictive dimension, an attainable metric entropy law, or a resource monotonicity/equivalence principle from a broad causal experiment class.

Such a theorem would make the A0–A5 layer mathematically indispensable rather than primarily organizational.

## 12.5 A major downstream theorem that truly consumes the foundations layer

The local confidence consumer is a good start.

A later theorem in A2, B4, C2, or another central branch that genuinely uses the causal-morphism or finite-memory theorem in place of an independent construction would give the repository-wide word "Foundations" stronger mathematical meaning.

This should arise from an actual proof, not from a dependency manifest.

# 13. What I would not ask the authors to do again

To avoid a moving target, I explicitly would **not** ask for:

- another demonstration that adaptive sensing can beat open-loop sensing;
- another rational (U1) upper certificate;
- another proof that the physical bridge is self-contained;
- another build or preservation audit;
- another exact divisible revelation formula;
- another restatement of A0–A5 without a new theorem;
- another metadata dependency edge;
- another argument that free controller mixing can violate a finite register constraint.

Revision 26 has already settled these points.

# 14. Editorial assessment by component

### A0–A5 and predictive quotient

**Assessment:** clear, careful, and useful. The article now has a legitimate foundations architecture. Most underlying mechanisms are classical; the novelty lies in the typed integration and later resource applications.

### Online resolution theorem

**Assessment:** mathematically sound-looking and properly tied to the acquired law. The matched (M^{-2/d}) rate is conditional on hypotheses that already encode the effective dimension and contraction. Useful, but not by itself a top-four foundations theorem.

### Acquired causal transport

**Assessment:** technically careful and operationally valuable. The identical-visible-prefix coupling is the right way to handle discontinuous downstream control. The theorem remains a resource/error composition result rather than a deep equivalence theorem.

### Unrestricted controlled dual

**Assessment:** inherited from v25; useful and correct-looking. Classical policy-tree/minimax machinery remains appropriately acknowledged.

### Finite-profile dynamic value

**Assessment:** exact and correctly prevents free hidden memory. As a general theorem it is essentially a large nonlinear Bellman formulation on occupation bundles. Its importance is conceptual cleanliness, not a new solvable duality.

### Routing gap

**Assessment:** one of the strongest new results. Exact, sharp, genuinely finite-memory, and robust to full-support perturbations. Its (K) coordinate is a specified bottleneck, while an (m)-state action buffer is separately charged. Therefore it is not a fixed-total-peak law.

### Exact (U2)

**Assessment:** excellent exact minimax calculation, with a global lower certificate and full response-class upper bound. This fully answers a central v25 request.

### Continuous (U2(gamma)) family

**Assessment:** a real family, not a perturbative corollary. Still tightly model-specific and limited to (N=2).

### Exact physical score for (W >= 12)

**Assessment:** meaningful and substantially stronger than the previous construction. It determines score, not minimal width. The difficult width converse remains open.

### Integer revelation theory

**Assessment:** improved and conceptually useful because it separates Bayes partition geometry from implementable minimax. The complete (K=2) law is clean. The family remains an illustrative resource model rather than the central physical frontier.

### Quantitative finite-architecture certificates

**Assessment:** useful effective certification for fixed finite problems. Not the conceptual bottleneck of the paper.

### Downstream confidence consumer

**Assessment:** a genuine proof consumer and a good response to the prior report. It establishes local utility, not program-wide necessity.

### Literature and scope

**Assessment:** substantially improved. The article now credits the relevant classical mechanisms and states unresolved priority boundaries honestly.

### Repository pipeline

**Assessment:** transparent and non-circular as recorded. The new GTF-I route is integrated but not yet an indispensable root of the principal eleven-paper DAG.

# 15. Final assessment

Revision 26 is mathematically much stronger than revision 25.

The authors have now done several things I explicitly asked for:

- imposed a real finite-register constraint in an informative controlled setting;
- proved an exact mixed-versus-implementable resource gap;
- solved the original two-preparation marked minimax value;
- extended that value to a continuous (N=2) family;
- restored the causal-experiment / predictive-quotient / resource-aware foundations spine;
- made calibration, approximation and controller memory live in one executable transport theorem;
- corrected the nondivisible revelation theory;
- supplied an actual downstream theorem rather than a pipeline label.

These are not cosmetic accomplishments.

I also have not found a fatal mathematical gap in the new core through the source-level checks described above.

Nevertheless, the standard requested by the authors is unusually high.

At that standard, I still see the paper as a collection of several strong exact results organized by a careful general framework, rather than a single unifying theorem of exceptional conceptual reach.

The general finite-memory theorem is exact but largely formulational.  
The novel exact finite-memory value is tied to one routing geometry and a multicut profile.  
The exact (U2) theory remains highly structured and does not yet expose an (N)-general mechanism.  
The foundations theorems are careful but often package classical quantization/coupling ideas after strong geometric hypotheses are assumed.  
The flagship physical result gives the exact score above width twelve without solving the width converse.  
The local consumer is real, but the major historical A2/B4/C2 routes remain independent.

Thus my recommendation remains:

## **Reject in the present form at Annals/Inventiones/JAMS/Acta.**

This is a materially different rejection from the v25 report.

I would no longer characterize the submission as structurally incomplete or as failing to be a foundations paper. I would characterize it as a coherent, serious, and technically strong foundations paper whose current main theorem package still falls short of the exceptional unifying significance required for the four general journals named by the authors.

A future version would be most persuasive not by adding more exact submodels, but by extracting from the present achievements one general theorem that explains **why** the finite-memory routing obstruction, predictive quotient, marked saddles, and physical resource boundary are manifestations of the same mathematical structure.

---

## Referee checklist

- Latest General Theta Foundations I revision verified as v26.
- Referee-ready head frozen at `466bfcdcb8b7d594d3924dbfa82b4c6e29368858`.
- Native source commit recorded as `92fd55a9541acfc14665f6275b455dc148fda2d3`.
- Controlling ninth review frozen at `568301ff5d8991af9a99a478371c1c4993d0bcd1`.
- Reviewed v25 predecessor head recorded as `818ca30bab506cfedaf6aee4c32bedff70c1e251`.
- Canonical 40-page source inspected.
- `foundations.tex` inspected.
- `controlled-memory.tex` inspected.
- `controlled-dual.tex` re-inspected.
- `marked-minimax.tex` re-inspected.
- `two-preparation-saddle.tex` inspected.
- `two-preparation-family.tex` inspected.
- `physical-bridge.tex` inspected.
- `integer-revelation.tex` inspected.
- `joint-revelation.tex` inspected.
- `consumer-transfer.tex` inspected.
- Response, proof status, pipeline status, resource ledger, history audit, literature crosswalk, build receipt and theorem-location record inspected.
- General Theta Foundations blueprint and original implementation note inspected.
- Round-Seventeen eleven-paper dependency ledger inspected.
- Finite-profile occupation recursion checked for parameter/runtime separation.
- Routing `1 / (2 ceil(m/K))` pigeonhole converse checked.
- Free-selector (K/(2m)) average bound and cyclic construction checked.
- Positive-noise gap constant checked.
- (U2) positive root and numerical constants independently spot-checked.
- (U2) displayed diagonal factorization checked modulo the cubic relation.
- Full-response upper-bound grouping logic checked.
- Continuous (gamma) family proof route inspected.
- Physical (W >= 12) converse/construction logic inspected.
- Integer nondivisible Bayes/minimax distinction inspected.
- Joint causal transport visible-prefix coupling inspected.
- Build/test evidence treated as reproducibility evidence only.
- No fatal counterexample found in the new v26 core during this review.
- v25 objection "no genuine finite-memory controlled theorem" withdrawn.
- v25 objection "exact marked theory stops at (N=1)" withdrawn.
- v25 objection "canonical article does not match General Theta Foundations blueprint" withdrawn.
- Active-testing literature omission no longer treated as a principal defect.
- Remaining collision widths (3)–(11) recognized as open, exactly as the manuscript states.
- Historical A2 independence recognized.
- Historical B4/C2 and eleven-paper closure not inferred.
- Final negative recommendation based on top-four-level conceptual synthesis and significance, not on a claimed elementary proof failure.
