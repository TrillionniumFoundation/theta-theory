# Ninth Independent External Harsh Referee Report

## General Theta Foundations I: Controlled Experiment Duality and Exact Marked Minimax Laws — Revision 25

**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed branch:** revision/general-theta-foundations-i-v25-referee-ready-2026-09-24  
**Frozen reviewed branch head:** 818ca30bab506cfedaf6aee4c32bedff70c1e251  
**Recorded source-build commit:** 35e28bbf5d75615f8f6c9f3ac599f445abea2cd9  
**Reviewed predecessor:** revision/general-theta-foundations-i-v24-referee-ready-2026-09-24 at ad1336e48e414b2c01e928b844c796ab4765178b  
**Controlling prior report:** reviews/general-theta-foundations-i-v24-external-harsh-top4-r8-2026-09-24/REFEREE_REPORT.md at c5c1a0d64f830bc3f036292357d8bbe2dbd04ca6  
**Canonical article:** 24 pages  
**Complete mathematical manuscript:** 136 pages  
**Complete preserved development:** 689 pages  
**Review date:** 24 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Review type:** independent external-referee-style, pipeline-aware harsh review

# Recommendation

## Reject in the present form at the requested top-four general-mathematics standard

Revision 25 is a serious mathematical revision. It is not a metadata response, not a larger diagnostic bundle, and not merely another finite certificate. It directly attacks two of the central mathematical objections in the eighth report:

1. it extends the outer statistical dual to finite controlled experiments with genuinely informative, non-dominating actions; and
2. it solves the one-preparation marked minimax problem exactly, with a matching optimal response and least-favorable prior.

It also imports the physical bridge into the canonical article and gives a separate exact preparation/decision-memory formula for an erasure-revelation family.

Those are real advances. Several objections from the eighth report must therefore be withdrawn.

Nevertheless, my recommendation remains rejection at Annals/Inventiones/JAMS/Acta. The reason has changed again.

The current controlled theorem is, in mathematical form, a finite-horizon partially observed control / zero-sum-game dynamic program with a special terminal testing functional. Its proof proceeds by enumerating finitely many deterministic policy trees, convexifying them by ex ante mixing, applying minimax against probability measures on the fixed parameter, and evaluating the Bayes best response by backward induction. This appears correct and useful. But the equality is explicitly unrestricted-memory: the policy tree and its random selector may be retained without a resource cap. The theorem therefore does not solve the hard resource-constrained controlled experiment. It supplies an architecture-uniform upper certificate after memory is relaxed.

The exact marked minimax theorem is also correct-looking and substantially stronger than the old rational certificate. However, it solves one training preparation, parameterized by a continuous target-bias variable. It does not solve a nontrivial family in the preparation number N, it does not determine U2, and it does not produce the original collision sample-memory Pareto frontier.

The exact revelation formula genuinely contains both N and K, but it does so in a deliberately separable erasure model. Its proof reduces the all-erasure part to a parameter-independent channel and the revealed part to balanced partition geometry. This is an exact theorem, but at the requested venue level it is too elementary and too model-engineered to carry the paper's broad foundational claim. It is particularly important that K in this theorem is a decision-cut atomic width, not the collision machine's bit-level peak.

Finally, the repository-level pipeline makes the title problem sharper, not weaker. The repository's own General Theta Foundations blueprint describes the first foundations paper as a typed theory of causal experiments, predictive quotients, causal morphisms, and resource-aware attainable resolution, with A0–A5, T01–T04, T06a, T07–T08 and a substantive G1/G3 theorem as its canonical spine. Revision 25 has evolved into a focused paper on finite controlled validation, one marked minimax family, one physical collision application, and one erasure memory model. The preserved volumes contain much more, but preservation is not the same as making that material the mathematical spine of the 24-page submitted article.

The current paper is therefore stronger as a specialized mathematical statistics / information / controlled-experiment paper than as "General Theta Foundations I." At top-four general-mathematics level, I do not yet see a theorem whose conceptual reach justifies the foundational title or whose downstream indispensability is demonstrated by the eleven-paper program.

# 1. Provenance and review scope

I reviewed the actual v25 referee-ready branch at the frozen head above. At the time this report was created, there was no existing v25 external-review branch.

I read the canonical v25 main source in full and the four new substantive modules:

- controlled-dual.tex;
- marked-minimax.tex;
- physical-bridge.tex;
- joint-revelation.tex.

I also read the v25 response to the eighth report, README, proof-status record, pipeline-status record, resource ledger, history audit, literature crosswalk and build receipt. I re-read the entire eighth report and the v24 pipeline status that v25 preserves.

For the program-level assessment, I inspected the current General Theta Foundations blueprint in foundations/general-theta/General_Theta_Foundations_v0.1.md and its implementation note. I also checked the historical eleven-paper dependency statements recorded in the repository. Those historical records say, in particular, that the older A1 is independent, the Sinai chain is A2 -> A3 -> A4 -> C2 -> D1, and the hard-sphere chain is B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1. Revision 25 itself is appropriately cautious and does not claim to have closed those historical chains.

I do not treat build success, exact-check counts, PDF identity checks, source hashes or negative controls as proof certification. The build receipt records, among other things, 8432 inherited checks, 66071 deterministic revelation channels, 18 negative-control executions, successful compilation, and exact symbolic checks. These are useful reproducibility evidence. They are not the basis of the recommendation.

I performed targeted independent source-level checks of the new arguments. In particular:

- I checked the policy-tree/minimax logic in the controlled theorem;
- I independently reconstructed the 3 by 3 nonadaptive payoff table in the adaptive-action example;
- I checked the algebraic structure and endpoint inequalities in the exact marked theorem;
- I checked the collision bridge's principal numerical inequalities and Gaussian-tail coupling;
- I checked the channel decomposition and balanced-fiber calculation in the revelation law.

I have not found a fatal counterexample to the new v25 core.

This matters. The rejection below is not a disguised allegation that the exact value is numerically wrong or that the controlled recursion has an obvious minimax gap.

# 2. What v25 genuinely resolves from the eighth report

The eighth report asked for theorem-level progress rather than more diagnostics. Revision 25 provides it.

## 2.1 The common-dominating-row limitation is no longer the general controlled theorem

Theorem thm:controlled permits a finite family of actions whose experiments need not be garblings of one common row. The unknown parameter is fixed through the execution, action choice stays inside the dynamic recursion, and the adversarial prior is selected once outside the recursion.

This directly answers the conceptual limitation identified in the eighth report.

The strict adaptive example is also useful. The three actions R, L and H are genuinely incomparable. With two training preparations, the adaptive policy has value 3/4, whereas every nonadaptive schedule mixture has value 5/8. I independently reconstructed the displayed exact table:

\[
\begin{pmatrix}
1/2&5/8&5/8\\
5/8&7/16&1/2\\
5/8&1/2&7/16
\end{pmatrix}.
\]

The full-support perturbation argument then shows that the distinction is not an artifact of disjoint supports.

The old criticism "the paper can handle action choice only when all actions are garblings of one experiment" is obsolete.

## 2.2 The exact U1 problem is solved

For the marked product family, Theorem thm:marked-exact gives an explicit primal/dual match for every

\[
0\le\gamma\le 1-\frac{1}{\sqrt2}.
\]

The value is

\[
U_1(\gamma)=\frac{3+u_\gamma^2}{8},
\qquad
u_\gamma=\gamma-2+\sqrt{\gamma^2-2\gamma+5}.
\]

The response is explicit; the least-favorable prior has two symmetric support points; and the lower bound is certified by the global square identity

\[
G_\gamma(p,q)-\frac{3+u_\gamma^2}{8}
=
\frac{2-\tau_\gamma}{16}
\left(
\big((p+q-1)^2-(p-q)^2-u_\gamma\big)^2
+4(p-q)^2
\right).
\]

The upper argument checks every coordinate of the full marked-word response space rather than restricting competitors to symmetric or count-based rules.

At gamma=1/4, the exact collision value becomes

\[
U_1(b,Q_*)=\frac{85-7\sqrt{73}}{64}
=0.393624590355895\ldots.
\]

This is a genuine resolution of request 17.2 from the eighth report.

The old criticism "the one-preparation rational prior is not known to be least favorable" is obsolete.

## 2.3 The physical bridge is now locally self-contained

The current article no longer asks the reader to recover the physical all-on law and the TV < 1/300 estimate from a 649-page unpublished predecessor.

Definition def:physical-class states the simulator/auditor interface. Lemma lem:local-scattering gives explicit collision-time and outgoing-signal estimates. Theorem thm:local-physical gives the positive-noise coupling to Q* and carries the actual mark through the comparison.

The old criticism "the headline physical corollary delegates crucial hypotheses to the unpublished companion" is substantially resolved.

## 2.4 The paper now contains an exact two-resource formula

The erasure/revelation family satisfies

\[
V_N^{\rm er}(K)
=
\bigl(1-(1-\alpha)^N\bigr)\left(1-\frac1K\right).
\]

The converse allows stochastic encoders and stopping, and the matching implementation uses K training states without an uncharged revelation flag.

This is genuinely an N–K equality, not merely a point or a numerical certificate.

The issue is no longer whether v25 contains any joint law. It does. The issue is whether this particular joint law has the depth, robustness and connection to the main physical resource problem needed to carry a top-four foundations paper.

## 2.5 The article remains disciplined about scope

The README, response, proof-status and pipeline-status files explicitly say that the following remain unsolved:

- the least collision peak at two preparations;
- the collision width-3-through-11 frontier;
- global collision U2;
- a generic fixed-width controlled minimax recursion;
- a matching autonomous finite-time precision-state law;
- the Norberg proof-level comparison;
- historical B4 aggregate closure;
- broad C2 aggregate closure;
- eleven-paper closure.

This is responsible. I do not penalize the manuscript for falsely claiming these results, because it does not falsely claim them.

# 3. Targeted mathematical checks

## 3.1 The controlled minimax equality appears sound

The crucial move is to replace a randomized causal policy by a distribution over deterministic policy trees. Because the horizon, action sets, observation alphabets and protocol states are finite, there are finitely many pure trees. Sampling all internal random decisions in advance indeed produces a mixed tree with the same law.

With no memory cap, retaining the sampled tree is allowed. Thus the unrestricted payoff set is the convex hull of the pure-tree payoff vectors.

The resulting game is bilinear between a finite simplex of trees and probability measures on compact Theta. The pure-tree payoffs are continuous in theta. Minimax therefore gives

\[
\max_\lambda\min_\theta\sum_\pi\lambda_\pi g_\pi(\theta)
=
\min_\mu\max_\pi\int g_\pi\,d\mu.
\]

For a fixed prior, backward induction on the unnormalized posterior measure gives exactly the recursion F_n. The terminal positive-part expression is the event-optimization value.

I do not see a hidden re-selection of theta after observations.

## 3.2 The theorem's exact equality is unrestricted-memory

This point is mathematically explicit in the manuscript and becomes central to the editorial assessment.

The equality is obtained after allowing an ex ante mixture over complete deterministic trees and retaining whichever tree was sampled. That is legal without a memory cap. It need not be legal at a specified finite register width.

Accordingly, for a finite-memory class the theorem gives

\[
V_{\text{memory-constrained}}
\le
\min_\mu F_N(e_0,\mu),
\]

not an exact finite-memory recursion.

This is not a flaw in the proof. It is a limitation in what the theorem solves.

## 3.3 The adaptive-action example is exact, not merely illustrative numerics

Using the uniform prior, the fixed-schedule Bayes values reproduce the displayed table. The mixture of schedules (R,L) and (R,H) gives 5/8 for every fixed parameter. The adaptive rule "take R, then use L or H according to the observed i" identifies the parameter and reaches 3/4.

I therefore accept the example as a real demonstration that the new theorem reaches beyond a common-dominating-row model.

## 3.4 The marked saddle calculation is internally coherent

The positive root u_gamma satisfies

\[
u^2+(4-2\gamma)u-(1+2\gamma)=0.
\]

The endpoint gamma_* is used to guarantee the sign condition needed at mixed training histories. The lower square identity is global on the parameter square. At the two prior support points, its right side vanishes. Under the same prior, the coefficient signs select the displayed response.

I do not currently see an algebraic gap in the primal/dual match.

## 3.5 The physical coupling estimates are plausible at source level

The preparation boxes force first contact for d in [9/10,11/10] after time 4/5 and before 3/2, with a uniform signed transverse outgoing velocity. The two Brownian sensor windows are disjoint. The normalized noise standard deviation is at most 1/12 and the signal magnitude exceeds 1/4, yielding a three-standard-deviation sign margin.

The union bound through two reports gives the advertised < 1/300 coupling defect.

I have not found a numerical contradiction in these estimates.

## 3.6 The revelation law is correct-looking but structurally elementary

On the event that all N potential reports are erasures, the decision-state channel is parameter-independent. On the complement, the remaining decision-state channel is arbitrary. The uniform prior annihilates the parameter-independent component.

The residual optimization over K-state channels is convex, hence maximized at a deterministic partition. For fiber sizes n_j, the value is

\[
1-\sum_j(n_j/m)^2,
\]

maximized by equal fibers under the paper's divisibility assumptions, giving 1-1/K.

The matching machine attains the product with the reveal probability.

I accept the formula as stated.

# 4. The central new objection: the controlled dual is not yet a controlled finite-resource dual

The strongest theorem in v25 is thm:controlled. It is also the theorem whose exact mathematical scope prevents me from treating it as the missing general resource theory.

The paper begins from a resource motivation: finite preparation, finite memory, controlled action choice, executable architectures. But the controlled equality removes the memory resource before solving the game.

This distinction is fundamental.

With unrestricted memory, a randomized causal policy is equivalent to an ex ante mixture of complete policy trees. That convexification is exactly what makes the minimax theorem clean.

At fixed width K, the sampled tree, its branch-contingent action plan, or the random selector that chose it may not fit in the register. Mixtures of controllers are not automatically admissible at the original width; the paper correctly says this elsewhere.

Thus the theorem does not answer the harder question:

> what is the exact minimax value when informative action choice and a genuine finite state budget are imposed simultaneously?

That is the point where the causal control and resource parts truly interact.

At present the controlled theorem says:

- exact equality for informative action choice with unrestricted memory;
- upper certificates for every smaller-memory architecture.

The revelation theorem says:

- exact finite decision-memory law for a very special erasure channel without nontrivial controlled experiment selection.

What is missing is their intersection.

A top-four "controlled experiment duality and resource foundations" theorem would become much more compelling if it derived an exact or sharp structural dual for informative action selection under a nontrivial finite-state constraint, or proved a matched obstruction showing precisely how finite memory destroys the unrestricted policy-tree saddle.

# 5. The mathematical skeleton of the controlled theorem has substantial classical ancestry

Revision 25 cites Smallwood–Sondik and correctly says that finite-horizon belief recursion and piecewise-linear value geometry are classical.

That is necessary but not sufficient for the present novelty claim.

Adaptive selection among statistically different experiments is also a classical subject. The literature crosswalk should directly compare the current theorem with at least the following lines of work:

- H. Chernoff, "Sequential Design of Experiments," Annals of Mathematical Statistics 30 (1959), 755–770, DOI 10.1214/aoms/1177706205;
- R. D. Smallwood and E. J. Sondik, "The Optimal Control of Partially Observable Markov Processes over a Finite Horizon," Operations Research 21 (1973), 1071–1088;
- M. Naghshvar and T. Javidi, "Active Sequential Hypothesis Testing," Annals of Statistics 41 (2013), 2703–2738, DOI 10.1214/13-AOS1144;
- S. Nitinawarat, G. K. Atia and V. V. Veeravalli, "Controlled Sensing for Multihypothesis Testing," IEEE Transactions on Automatic Control 58 (2013), 2451–2464, DOI 10.1109/TAC.2013.2261188.

I am not asserting that any of these papers contains Theorem thm:controlled in the present frozen-validation formulation.

I am asserting that "actions are statistically incomparable and adaptive action selection can be strictly useful" is not itself a novelty boundary. Controlled sensing and active hypothesis testing already study causal choice among observation actions and explicitly analyze adaptive versus nonadaptive policies.

The burden on v25 is therefore to say theorem-by-theorem what is new:

- the fixed unknown parameter under this validation score;
- the one-prior outer minimax representation;
- the exact terminal posterior-predictive TV functional;
- the architecture-uniform upper certificate;
- the particular resource accounting;
- or some combination of these.

The current crosswalk does not yet perform that comparison.

This is a significant omission because the controlled dual is now the main reason the paper claims broader foundations-level significance.

# 6. The exact U1 theorem is a real advance, but it is still an N=1 theorem

The eighth report explicitly asked the authors to solve U1 or U2. V25 solves U1 cleanly. I credit that fully.

But one should distinguish two kinds of "family."

The manuscript has a continuous family in gamma. The number of training preparations remains fixed at one.

Thus this is not yet an exact law in N. It does not show how the least-favorable prior, the event alphabet, the posterior predictive geometry, or the value evolve when N increases.

The current two-preparation result still consists of a particular deterministic selector whose worst-case value is exactly m2. The manuscript continues to say, correctly, that this selector is not proved globally optimal.

Therefore:

- U0 is exact;
- U1 is exact for the gamma family;
- the displayed two-preparation selector has an exact worst-case score;
- U2 remains unknown.

This is much better than v24, but it still stops immediately before the first genuinely nontrivial training-history family.

For a top-four structural theorem, a calculation of U_N for a nontrivial range of N, a recurrence for the extremal priors, a sharp asymptotic law, or even an exact U2 with a qualitatively new saddle structure would carry far more weight than a continuous target perturbation at N=1.

# 7. The joint revelation law does not resolve the original resource-frontier problem

The revelation theorem is exact and should stay if the paper is presented as a resource-examples paper.

But its role in the foundations claim should be sharply limited.

The family has three properties that make the formula unusually separable:

1. each training observation either reveals theta exactly or reveals nothing;
2. the erasure event has parameter-independent probability;
3. after a reveal, the decision-memory problem reduces to partitioning a finite parameter set into K groups.

This is why the value factorizes into

\[
\Pr(\text{at least one reveal})\times \text{best K-partition value}.
\]

The powers-of-two assumptions m=2^d and K=2^k further guarantee perfectly equal fibers. A more general statement for arbitrary m and K would naturally expose the balanced-integer-partition correction rather than hide it.

More importantly, the theorem's K is a decision-cut state count on an atomic-symbol model. It is not the physical collision bit-level peak W. The manuscript states this correctly.

Therefore the theorem does not answer the main unresolved physical question:

\[
\text{what is the least peak width for a successful two-preparation collision audit?}
\]

Nor does it give a matched N–W frontier for the collision system.

The eighth report's highest-value Route A remains open.

# 8. The physical theorem is improved, but its resource exactness remains one-dimensional

The exact U1 value enlarges the interval of thresholds on which one preparation is impossible. This is a genuine sharpening.

The two-preparation construction remains the same peak-twelve machine. No new lower bound on width is proved.

Consequently the physical theorem still establishes:

\[
N_c^{\rm phys}(W,Q)=2
\quad\text{for all }W\ge12
\]

on a wider threshold segment, while leaving open:

- whether peak 12 is necessary;
- whether peak 11, 10, ..., 3 can succeed at N=2;
- whether decision width 5 is necessary;
- the exact two-preparation minimax value;
- a Pareto lower curve coupling N and peak width.

The exact U1 theorem makes the one-dimensional preparation boundary sharper. It does not turn it into a joint frontier.

I would not describe the current physical result as a solved sample-memory theory.

# 9. The physical bridge is self-contained, but it remains highly model-engineered

The self-contained bridge is a major editorial improvement. I no longer object that the reader must search a huge companion for the physical hypotheses.

The remaining issue is different.

The physical model is deliberately tuned to the marked experiment:

- the preparation table has four B,W combinations with the target masses built into it;
- the detector is chosen to separate the collision/no-collision regimes;
- the observation windows are selected after the collision;
- the private simulator class is explicitly Bernoulli-row based;
- the lower-bound subfamily is chosen so every gate is a garbling of the all-on product row.

This is legitimate mathematics. But it means the physical theorem should not be counted as evidence that the controlled dual captures a broad class of naturally arising physical simulators.

The theorem shows that one carefully specified microscopic collision/sensor construction realizes the finite experiment needed by the statistical result.

For top-four foundations significance, I would want either:

- a robust class of physical systems satisfying an intrinsic criterion that implies the same statistical structure; or
- a theorem extracting the experiment from substantially weaker physical assumptions.

At present the bridge is self-contained but still bespoke.

# 10. Revision 25 has drifted away from the repository's own General Theta Foundations blueprint

This is the most important pipeline-aware issue.

The repository contains a detailed General Theta Foundations blueprint. It defines the broad theory as a layered structure involving:

- positive causal experiments and complete path laws;
- future tests and predictive quotients;
- causal simulation morphisms;
- Bayesian / information geometry;
- attainable resolution and finite memory;
- singular observation geometry;
- pressure and entropy;
- large deviations;
- dynamic closure and memory.

The same blueprint says the first foundations paper should have the spine

\[
\text{real experiment}
\to
\text{future predictive quotient}
\to
\text{causal simulation}
\to
\text{finite-resource attainable resolution},
\]

and should include A0–A5, T01–T04, T06a, T07–T08 plus a substantive G1/G3 theorem.

The implementation note for the original foundations v1 says that version did exactly this and supplied a dynamic hidden-Markov memory law of order epsilon^2 M^{-2/d}, with a further epsilon^4 M^{-2/d} query law.

The canonical v25 article no longer has that architecture.

Its 24 pages are centered on:

- a finite controlled validation game;
- an N=1 marked saddle calculation;
- a particular collision experiment;
- an erasure/partition memory formula;
- a generic finite-architecture Bernstein certificate;
- a classical autonomous testing comparison.

These are not irrelevant to the blueprint. They fit parts of the causal-experiment and resource program.

But the canonical article no longer presents the blueprint's foundational object/morphism/predictive-quotient spine as its main theorem architecture.

Appending the unaltered 136-page and 689-page preserved volumes does not solve this mismatch. A reader evaluating the 24-page journal submission should not have to infer that its title is justified by material relegated to archival volumes.

The authors therefore face a structural choice:

1. make this paper the actual General Theta Foundations I paper described by the blueprint, with the controlled dual and exact minimax results as major consequences; or
2. keep the present focused mathematics and use a title that says what the article actually proves.

At present the paper occupies an unstable middle position: a specialized finite controlled-experiment article carrying the title of a much broader foundational program.

# 11. The eleven-paper pipeline does not presently make v25 indispensable

The current pipeline-status file is commendably explicit:

- A2 remains an independent geometric chain;
- historical B4 obligations remain open;
- broad C2 obligations remain open;
- collision peak-frontier closure is false;
- eleven-paper closure is false.

The historical dependency ledgers are even clearer. They record older A1 as independent and the principal Sinai and hard-sphere chains as separate dependencies.

This means the program cannot presently supply significance to v25 by saying "all later papers require it."

Some later finite-statistical modules in the new foundations sequence use the same continuation/resource language, but the flagship A2 geometric chain is still independent and the old long chains retain their own spectral, LDP, semigroup and contraction obligations.

That is not a mathematical defect.

It does mean that "Foundations I" must earn its force intrinsically, from the theorem in this article, rather than from the size of the repository.

At present I do not see a major downstream theorem whose proof becomes possible only because of the v25 controlled dual or marked minimax saddle.

# 12. The auxiliary quantitative and autonomous results still do not change the top-four assessment

The HS/m subdivision theorem is useful. It gives an effective finite certificate for a fixed finite architecture and is careful about shared rows and causal interpretation.

But it remains a generic discretization / Bernstein / coupling estimate whose size can be enormous.

The autonomous section is also well written, but the stationary optimum is explicitly classical Hellman–Cover. The finite-time dyadic estimate is an upper construction and the paper correctly declines to call it a sharp precision-state law.

These sections strengthen the paper as a coherent resource-accounting article.

They do not supply the missing foundational theorem.

# 13. Literature boundary: Norberg remains unresolved, and active experiment design must now be added

The v25 literature crosswalk is responsible in one respect: it does not pretend to have completed the proof-level comparison with Norberg's filtered-experiment theory.

That boundary remains open.

But v25 creates a new literature obligation by making controlled informative action selection central.

The paper should now contain a serious comparison with the controlled sensing / active hypothesis testing / sequential design literature, not only POMDP value-function literature.

In particular, the current adaptive-versus-nonadaptive example should not be presented in a vacuum. Prior work already studies strict benefits of causal observation control in multihypothesis settings.

Again, I am not claiming theorem duplication. I am requiring the authors to establish the exact novelty boundary before asking a top-four referee to credit "controlled experiment duality" as a foundational new direction.

# 14. Disposition of the eighth report's main requests

## 14.1 Request 17.1 — genuine joint preparation-memory obstruction

**Partially resolved in a separate model, not resolved for the collision problem.**

The revelation theorem is a genuine N–K equality. The original collision peak-width frontier remains open.

## 14.2 Request 17.2 — solve one minimax value exactly

**Resolved for U1, and done well.**

The least-favorable prior and optimal response match, with a global identity.

## 14.3 Request 17.3 — extend beyond a single dominating experiment

**Resolved at the unrestricted-memory finite-horizon level.**

The controlled theorem admits incomparable actions and retains action choice in the recursion.

The stronger finite-memory controlled minimax problem remains open.

## 14.4 Request 17.4 — prove a scaling law

**Partially resolved.**

The erasure family has an exact N–K scaling law. Its structural simplicity and different resource coordinate limit how much this changes the main paper's significance.

## 14.5 Request 17.5 — make the physical bridge self-contained

**Resolved in substance.**

The current article contains the required microscopic and positive-noise estimates.

## 14.6 Request 17.6 — finish or delimit filtered-experiment comparison

**Delimited, not closed.**

The manuscript appropriately narrows its claim rather than asserting a comparison it has not proved.

# 15. New principal requests for a future revision

These are theorem-level requests. I would not recommend another revision whose main change is more tests, more retained pages or a longer response document.

## 15.1 Solve controlled experiment selection under an actual finite-state constraint

This is the highest-value continuation.

Define a controlled finite-memory game in which:

- actions are genuinely incomparable;
- the same finite state must encode both posterior-relevant information and future action choice;
- ex ante mixtures of complete policy trees are not free;
- stopping and validation freezing remain legal;
- the resource count is explicit.

Then prove either an exact dual, a sharp obstruction, or a matched upper/lower theorem.

This would combine the strongest new idea in v25 with the resource question that currently disappears under unrestricted-memory convexification.

## 15.2 Determine a nontrivial part of the original collision N–W Pareto frontier

The cleanest target remains the least peak width at N=2.

Even a theorem excluding a nontrivial range W <= W0 would be meaningful if matched to an explicit construction.

This would connect the statistical dual directly to the paper's flagship physical example.

## 15.3 Go beyond N=1 in the marked minimax family

Determine U2, or a recurrence/asymptotic law for U_N, with matching least-favorable priors and optimal responses.

A theorem in which the training history genuinely grows is much more likely to reveal an invariant than another continuous deformation of the N=1 target.

## 15.4 Strengthen the revelation theorem or reduce its role

If the joint law is intended as a central theorem, remove the powers-of-two/equal-fiber convenience and state the arbitrary m,K value. Then ask whether partial revelations, noisy reveals, or controlled reveal probabilities preserve a tractable resource law.

If the authors do not pursue this, present the current theorem as a clean illustrative model rather than a central foundation.

## 15.5 Reconcile the canonical article with the General Theta Foundations blueprint

Either restore the A0–A5 / predictive-quotient / causal-morphism / attainable-resolution spine to the canonical article and show how the v25 controlled theorem is a major theorem of that framework, or narrow the title.

The current 24-page article and the repository's stated foundations blueprint should not describe materially different papers under the same program name.

## 15.6 Demonstrate downstream necessity

A major theorem in A2, B4, C2 or another program component that genuinely uses the controlled dual in an essential way would materially strengthen the word "Foundations."

This should be a proof dependency, not a pipeline metadata edge.

## 15.7 Complete the adjacent literature comparison

Add Chernoff, Naghshvar–Javidi, Nitinawarat–Atia–Veeravalli and any other directly relevant controlled experiment / active testing results. State exactly which theorem ingredients are classical and which are claimed new.

The same principle continues to apply to Norberg: if proof-level comparison remains unavailable, maintain the narrow claim.

# 16. What I would no longer ask the authors to do

To avoid moving the goalposts, I explicitly withdraw several previous requests.

I would not ask for:

- another rational one-preparation certificate;
- another proof that the common-row reduction works;
- another finite diagnostic count;
- another copy of the physical companion inside the article;
- another demonstration that adaptive informative actions can matter;
- another metadata graph showing unresolved program nodes;
- another build/preservation audit.

V25 has already done enough on those fronts.

The remaining issue is structural mathematics.

# 17. What theorem would materially change my recommendation?

The paper is now mathematically stronger than v24. One genuinely deep next theorem could change the assessment.

I would reconsider the requested venue standard after one of the following, provided it is proved at the same level of rigor and positioned correctly against the literature.

## Route A: finite-memory controlled minimax duality

An exact or sharp theorem for genuinely informative controlled actions under a nontrivial finite-state budget, where the policy-tree mixture cannot be stored for free.

This would directly unify control and memory.

## Route B: a true collision sample-memory Pareto theorem

Determine the least peak width at two preparations or a matched N-versus-W curve over a nontrivial range.

This would make the physical resource theorem genuinely two-dimensional.

## Route C: an exact multi-preparation marked family

Solve U_N for N >= 2 on a nontrivial family, or derive sharp asymptotics with matching constants and extremizers.

This would elevate the posterior-predictive dual from an exact N=1 certificate engine to a structural theory.

## Route D: restore the repository's G1/G3 foundations theorem as the canonical spine

Prove a genuinely general causal simulation / attainable-resolution theorem with simultaneous preparation, memory, calibration and model-error control, and show the present controlled minimax results as nontrivial consequences.

This would make the title match the blueprint.

## Route E: an indispensable downstream theorem

Prove a substantial later theorem whose derivation essentially uses the v25 controlled dual or exact minimax structure and cannot be obtained from the older independent route.

This would give programmatic meaning to "Foundations."

# 18. Editorial assessment by component

### Controlled posterior-predictive dual

**Assessment:** mathematically sound-looking, elegant, useful, and genuinely broader than v24. Its equality is an unrestricted-memory finite-horizon policy-tree/minimax identity. The resource-constrained controlled problem remains unsolved, and classical controlled-sensing ancestry must be compared more fully.

### Adaptive action example

**Assessment:** exact and useful as a separation example. Not itself a foundations-level theorem; adaptivity gains in controlled sensing are classical phenomena.

### Exact marked U1 family

**Assessment:** the strongest explicit new calculation in v25. Clean primal/dual match and a good response to the prior report. Still N=1 and highly structured.

### Physical bridge

**Assessment:** self-contained and carefully quantified. This removes a serious v24 weakness. The physical construction remains bespoke.

### Two-preparation physical theorem

**Assessment:** real exact preparation theorem on an enlarged threshold segment. Still no width lower bound and no exact U2.

### Revelation N–K law

**Assessment:** correct-looking exact two-resource theorem. Too separable and elementary in its current erasure/equal-partition form to carry a top-four foundations claim; resource coordinate differs from the collision peak width.

### Finite-architecture certificates

**Assessment:** useful reproducibility / effective-analysis theorem, not a sharp resource-complexity law.

### Autonomous comparison

**Assessment:** careful presentation of a classical stationary optimum plus a conservative finite-time implementation. Limited new significance.

### Literature positioning

**Assessment:** improved but incomplete for the new controlled-action emphasis. The active experiment-design literature is now essential.

### Journal architecture

**Assessment:** 24 pages is a focused article. The problem is no longer bloat. The problem is mismatch between the focused article and the broad foundations title/blueprint.

### Program pipeline

**Assessment:** transparent but still multiple-root. A2 is independent; B4/C2 and eleven-paper closure remain open. The program currently does not make this article an indispensable root.

# 19. Final assessment

Revision 25 deserves substantially more mathematical credit than revision 24.

The authors have now:

- removed the common-dominating-action restriction from the finite controlled theorem;
- exhibited a strict informative-action adaptive advantage;
- solved U1 exactly with an explicit least-favorable prior and matching optimal response;
- made the collision bridge self-contained;
- strengthened the physical threshold interval;
- supplied an exact N–K law in a separate revelation family.

I do not regard any of these as cosmetic.

But the requested journal standard is not "has the previous referee been answered point by point?" It is whether the resulting paper contains mathematics of the conceptual depth, breadth, novelty and necessity expected of Annals/Inventiones/JAMS/Acta.

My answer remains no.

The new controlled theorem obtains exact equality only after lifting the memory constraint and convexifying over complete policy trees.  
The exact marked theorem stops at one training preparation.  
The original collision peak-width frontier remains open.  
The joint N–K law is built from an erasure/revelation decomposition and balanced partitions rather than from the hard controlled-memory geometry.  
The main active-controlled-experiment literature has not yet been compared at theorem level.  
The canonical article has drifted away from the repository's own formal blueprint for General Theta Foundations I.  
The eleven-paper pipeline remains multiple-root and does not make v25 indispensable.

I therefore recommend **rejection in the present form at the requested top-four general-mathematics standard**.

The most promising next move is not another layer of certification. It is to solve the problem that v25 now exposes very cleanly:

> retain genuinely informative action choice and impose a genuine finite memory budget at the same time, then prove a sharp minimax/resource theorem.

That theorem, or a true collision N–W Pareto theorem, would materially change the status of the paper.

**Recommendation: reject in the present form at Annals/Inventiones/JAMS/Acta.**

---

## Referee checklist

- Latest General Theta Foundations I revision verified as v25.
- Reviewed referee-ready head frozen at 818ca30bab506cfedaf6aee4c32bedff70c1e251.
- Source-build commit recorded as 35e28bbf5d75615f8f6c9f3ac599f445abea2cd9.
- Controlling r8 report frozen at c5c1a0d64f830bc3f036292357d8bbe2dbd04ca6.
- Canonical 24-page main.tex read in full.
- controlled-dual.tex read in full.
- marked-minimax.tex read in full.
- physical-bridge.tex read in full.
- joint-revelation.tex read in full.
- README, response, proof status, pipeline status, history audit, resource ledger, literature crosswalk and build receipt inspected.
- General Theta Foundations blueprint and implementation note inspected.
- Historical eleven-paper dependency ordering inspected.
- Controlled policy-tree convexification checked at source level.
- Fixed-parameter / single-prior placement checked.
- 3 by 3 nonadaptive payoff table independently reconstructed.
- Adaptive 3/4 versus nonadaptive 5/8 claim accepted.
- Marked square identity proof route checked.
- Exact collision U1 expression checked.
- Physical collision-time/signal bounds spot-checked.
- Gaussian-tail TV coupling spot-checked.
- Revelation channel decomposition and balanced-fiber converse checked.
- No fatal counterexample found in the new v25 mathematical core.
- Old objection "controlled theorem needs a dominating action" withdrawn.
- Old objection "U1 is not solved exactly" withdrawn.
- Old objection "physical bridge is delegated to an unpublished companion" withdrawn.
- Exact N–K revelation law credited as a real theorem.
- Collision peak-width optimum still recognized as open.
- Global U2 still recognized as open.
- Generic fixed-width controlled minimax recursion still recognized as open.
- Equality in thm:controlled distinguished from finite-memory upper certification.
- Continuous gamma family distinguished from a multi-N family.
- Decision-cut atomic K distinguished from collision bit-level peak W.
- Classical POMDP / active testing / controlled sensing ancestry flagged for direct comparison.
- Norberg proof-level boundary recognized as unresolved.
- A2 recognized as independent.
- Historical B4 aggregate recognized as unresolved.
- Broad C2 obligations recognized as unresolved.
- Eleven-paper closure not inferred.
- Build/test evidence treated as reproducibility evidence, not proof, priority clearance or acceptance.
- Principal remaining top-four objection classified as insufficient resource-constrained controlled depth and insufficient foundations-level necessity, not failure of the v25 algebra.
