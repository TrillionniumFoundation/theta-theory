# External Referee Report — General Theta Foundations I (v3)

**Manuscript:** *General Theta Foundations I: Causal Experiments, Predictive Quotients, and Resource-Aware Reduction*  
**Author:** Qian Qi  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed snapshot:** `revision/general-theta-foundations-i-v3-referee-ready-2026-09-22`  
**Principal mathematical source commit:** `50bf6fdd41ae478adce2b14c5f27af793c5d4da9`  
**Publication/build commit:** `a4b703201308dca4cd3d09997e731263d4b44413`  
**Previous referee-ready base:** `75d8f3f8672ab78a844cc0a7a68808b46edf56f5`  
**Controlling v1 referee report:** `01d3e78bd40985651f5b4ff24364e1dba5d481f0`  
**Historical eleven-paper snapshot:** `c04845b6613208406703695c9c184ae461f95805`  
**Requested standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the American Mathematical Society*  
**Recommendation:** **REJECT at the requested four-journal standard. I would not invite another revision of this integrated manuscript in its present architecture.**

> This is an owner-requested, AI-assisted external-style mathematical assessment. It was not commissioned by any named journal and must not be represented as an official referee report from Annals, Acta, Inventiones, JAMS, or any other journal.

## 1. Scope and method of review

This report is a fresh review of the v3 referee-ready edition, not a restatement of the v1 report.

I read the new mathematical centre in:

- `papers/GTF-I-v3/introduction.tex`;
- `papers/GTF-I-v3/regenerative.tex`;
- `papers/GTF-I-v3/calibration.tex`;
- the principal retained v2 chains in `retained-results.tex`;
- `PROOF_LEDGER.md`, `HISTORY_AUDIT.md`, and `RESPONSE_TO_REFEREE.md`;
- the master programme `foundations/general-theta/General_Theta_Foundations_v0.1.md`;
- the GTF-I implementation addendum;
- the historical dependency DAG and the Round-18/Round-20 reports for all eleven pipeline components.

I also checked the current bibliography against several bodies of literature directly relevant to the new claims: finite-rate estimation/control and the data-rate theorem, dynamical rate-distortion/metric mean dimension, and invariant/minimax decision theory for shift experiments with nuisance parameters.

I did **not** treat the successful build, hashes, source-preservation tests, finite diagnostics, negative controls, or pixel-identical rendering as mathematical proof. They are unusually careful reproducibility records and are useful for identifying the reviewed object, but they do not bear on whether the infinite-dimensional quantifiers, minimax equalities, asymptotic rates, or top-journal significance are correct.

I did not independently reprove every inherited lemma in the 52-page integrated manuscript. I did, however, spot-check the load-bearing retained v2 arguments used by the current narrative: acquired-law resolution, intermittent block contraction, the every-positive-refresh HMM result, the measured-calibration contact theorem, and the finite-reference optimal-control comparison.

## 2. Executive assessment

The third revision is a **substantial mathematical improvement** over v1.

The v1 manuscript was vulnerable to the criticism that its "foundations" were largely careful typing of classical material plus a tractable strongly refreshing HMM calculation. That criticism no longer describes the entire paper. Version 3 now contains two genuine new centres:

1. a regenerative future-orbit quantization converse and a sharp three-regime causal-memory law for the doubling experiment; and
2. an exact minimax elimination of unrestricted additive calibration for a correlated paired Gaussian experiment, followed by a matched contact-plus-label theorem under a global two-sided contact hypothesis.

I do **not** find, from the source audit performed here, a demonstrated fatal counterexample to Theorems 2.1, 3.1, 4.1, or 4.2. The reset-time disjointness argument in Theorem 2.1 is coherent; the suffix-machine accounting charges the persistent age information rather than hiding it; the critical logarithm in the doubling example is genuinely produced by the geometric sum; the diffuse-nuisance simulation in Theorem 4.1 preserves the label budget; and the contact theorem's testing/covering arguments are consistent with its stated hypotheses.

That positive mathematical assessment does **not** change my editorial recommendation at the requested level.

The obstacle is now clearer: **the new theorems are interesting, but the generality and depth are still one major theorem short of a four-journal paper.** The "general" future-orbit result is a one-sided lower bound obtained by renewal disjointness plus ordinary M-centre quantization. The matching phase transition is proved only in a deliberately solvable one-dimensional reset/doubling model. The statistical theorem assumes, rather than derives, the global bi-Lipschitz contact geometry that carries the difficult singular structure. And the surrounding 52-page framework still contains a large amount of infrastructure whose mathematical novelty is much lower than that of the new centre.

There is a second, programme-level issue. The historical theta pipeline does not provide independent support for the current paper. On the fixed historical branch, every one of the eleven load-bearing papers was still rejected in Round 20, with explicit unresolved main theorems. Version 3 correctly refuses to pretend otherwise. But once that restraint is imposed, GTF-I must stand as an independent paper, and its present theorems are not broad enough to support the rhetoric of a general foundation for that entire programme.

My recommendation is therefore a **significance/general-theory reject**, not a finding that the new central calculations are obviously false.

## 3. What is genuinely improved since v1

### 3.1 Theorem 2.1 is a real conceptual advance over checkpoint-only geometry

For a regenerative experiment, the manuscript maps an acquired state (u) to the weighted future orbit
[
Z_q(u)=left(sqrt p,q^{k/2}f(T^ku)ight)_{kge 0}inell^2.
]
The lower bound says that one persistent label created at a reset has to quantize the entire family of future readouts that may be needed before the next acquisition.

This is the right object for the stated resource model. It is strictly more informative than the geometry of the current checkpoint alone, and the proof correctly handles arbitrary randomized, time-dependent M-label machines by conditioning on a reset, freezing independent coding randomness, and summing disjoint last-reset events.

This is the strongest conceptual addition in v3.

### 3.2 Theorem 3.1 gives a clean separation between checkpoint and causal complexity

For the doubling map, every checkpoint distribution is uniform and hence has exact scalar quantization risk (1/(12M^2)). The causal problem nevertheless exhibits
[
M^{-2},qquad (1+log M)M^{-2},qquad
M^{-log(1/q)/log 2}
]
in the three regimes (q<1/4), (q=1/4), and (q>1/4).

The upper construction is refreshingly explicit. The persistent state is the union of binary suffixes of lengths (0,dots,B), so the state count is exactly (2^{B+1}-1). There is no uncharged reset-age register. The lower bound is not restricted to interval quantizers, and the dyadic discontinuities are handled rather than suppressed behind a false global Lipschitz estimate.

This directly answers an important part of the v1 criticism: the paper now contains a phenomenon that cannot be read off from the one-time acquired law.

### 3.3 The exact nuisance quotient is stated with the correct limitation

Theorem 4.1 does not claim full statistical sufficiency for ((	heta,eta)). It proves equality only of the minimax decision problems for (	heta), with unrestricted additive nuisance and bounded loss, under the same M-label constraint.

That distinction matters. The proof's increasingly diffuse Gaussian nuisance distribution is a legitimate route to the reverse minimax inequality; it does not invoke an improper prior as if it were an actual experiment.

### 3.4 The contact theorem now uses the actual noise metric and allows correlation/nonseparability

Theorem 4.2 is stronger than the independent-coordinate v2 theorem. Cross-covariance enters through the covariance of the observed difference, and the mean map need not be coordinate-separable. The manuscript also gives a concrete nonlinear coupled example rather than merely asserting that such examples exist.

### 3.5 The revision is more honest about the historical programme

This deserves explicit credit. The v3 history audit does not use a Gaussian paired-measurement theorem as a substitute for the old Sinai local-limit theorem, does not use finite-label quantization as a substitute for a particle LDP, and does not promote finite-dimensional Schur algebra into an unbounded-operator theorem.

That is a genuine improvement in mathematical hygiene.

## 4. Decisive objection E1: the general future-orbit theorem is only a converse, not yet a general theory

Theorem 2.1 is stated at impressive generality: arbitrary standard Borel state space, arbitrary Borel map, arbitrary acquired law, arbitrary bounded Borel readout, and arbitrary randomized nonstationary M-label machines.

But the mathematical conclusion at that level of generality is only
[
mathcal R_M^{m ca}ge e_M^2(Z_q).
]

The proof is essentially:

1. after a reset, one M-valued state induces at most M possible finite future decoder strings;
2. quantization of the truncated future-orbit vector therefore gives a lower bound;
3. geometric reset probabilities supply the weights;
4. disjoint last-reset events convert the one-reset obstruction into a time-average bound.

This is useful and clean. It is not yet the kind of structural theorem I would expect to carry an Annals/Acta/Inventiones/JAMS paper.

A genuinely general result would need substantially more: for example, conditions under which causal M-state risk is **equivalent** to a geometric quantity of the weighted orbit image; a characterization of when the orbit quantization lower bound is realizable by a causal machine; a theorem in terms of entropy/covering/regularity invariants for a broad class of expanding, hyperbolic, random, or controlled systems; or a converse/achievability theory that survives noisy or partial acquisitions.

At present the general theorem tells us an obstruction. The only matching realizability theorem is the hand-built binary suffix machine for one special dynamical system.

That gap between "general converse" and "general theory" is the central editorial weakness of v3.

## 5. Decisive objection E2: the flagship phase transition is mathematically clean but too engineered

The three-regime law is attractive, but its mechanism is exceptionally transparent:
[
4^{-B}sum_{k=0}^{B-1}(4q)^k + q^B.
]
The critical value (q=1/4) is the point at which the squared expansion factor (2^2) balances geometric survival (q).

This is exactly why the theorem is a good benchmark. It is also why I do not regard it as a four-journal centre.

The model has several simplifying features simultaneously:

- the reset state is observed perfectly;
- every reset is a complete regeneration independent of the past;
- between resets the dynamics are deterministic;
- the map is the binary doubling map;
- the target is the scalar state itself;
- the distortion is squared Euclidean error;
- the reset law is Bernoulli and independent;
- the optimal upper machine is essentially the symbolic dynamics already built into the map.

The lower bound is broad with respect to the *coder*, but the underlying *experiment* is very narrow.

The natural top-level theorem would explain which parts of this trichotomy persist for a nontrivial class of expanding maps, Markov partitions, nonconstant expansion, vector-valued readouts, nongeometric regeneration, noisy reset observations, partial acquisitions, or controlled observation times. The current paper proves none of these.

The manuscript therefore establishes a striking solvable example, not yet a universality theorem.

### Near-critical scaling is also missing

The theorem fixes (q) and lets (M) vary. Its constants may depend arbitrarily on (q). That leaves out the mathematically most revealing crossover regime (q=q_M	o1/4), where one should see a scaling function interpolating between the power law and the critical logarithm.

A four-journal treatment of a claimed phase transition should normally address at least some version of the critical window, not only three fixed-parameter asymptotic regimes.

## 6. Decisive objection E3: the paper is not sufficiently positioned against finite-rate estimation/control and dynamical rate-distortion

The bibliography discusses predictive states, predictive rate-distortion, filter quantization, approximate information states, and finite-memory POMDP policies. Those are relevant.

But the new central phenomenon is also directly adjacent to another large literature: **estimation and control of unstable/expanding dynamics under finite communication or finite-rate representations**.

Classic examples include:

- G. N. Nair and R. J. Evans, *Stabilization with data-rate-limited feedback: tightest attainable bounds*, Systems & Control Letters 41 (2000), 49–56, DOI 10.1016/S0167-6911(00)00037-2;
- S. Tatikonda and S. K. Mitter, *Control Under Communication Constraints*, IEEE Transactions on Automatic Control 49 (2004), 1056–1068, DOI 10.1109/TAC.2004.831187;
- A. S. Matveev and A. V. Savkin, *Estimation and Control over Communication Networks*, Birkhäuser, 2009.

That literature explicitly connects instability/expansion to the information rate required for state estimation or stabilization. The present references contain none of Nair, Evans, Tatikonda, Mitter, Matveev, or Savkin.

The paper is not identical to the data-rate theorem setting: it constrains the cardinality of a persistent state rather than a per-time communication channel, and regeneration changes the problem substantially. That difference should be made a theorem-level comparison, not used as a reason to omit the literature.

There is also a modern dynamical rate-distortion literature that is even closer to the manuscript's use of orbit geometry. In particular:

- E. Lindenstrauss and M. Tsukamoto, *From Rate Distortion Theory to Metric Mean Dimension: Variational Principle*, IEEE Transactions on Information Theory 64 (2018), 3590–3609, DOI 10.1109/TIT.2018.2806219.

The present bibliography does not contain Lindenstrauss or Tsukamoto.

I am **not** asserting that these works already prove Theorem 3.1. I am saying that without a serious comparison to them, the novelty claim "future-orbit geometry under a hard persistent-cardinality constraint" is not adequately located.

For a four-journal submission this is a major defect, because the central contribution must be evaluated against the strongest adjacent theory, not only against the author's preceding A1/A2 papers and the POMDP literature.

## 7. Decisive objection E4: Theorem 4.1 is elegant but belongs to classical invariant/minimax decision theory unless a sharper distinction is proved

The exact nuisance-elimination theorem is correct-looking and nicely adapted to the label constraint. But its basic structure is a translation nuisance in a Gaussian shift experiment. The proof itself uses the canonical invariant/minimax device of diffusing the nuisance law until the nuisance-dependent residual becomes asymptotically parameter-independent.

This sits close to classical invariant decision theory and Hunt–Stein/Le Cam theory. Standard references treat Gaussian shifts with nuisance parameters, reduction by invariance, minimax theorems, and Hunt–Stein type results.

The manuscript should explain precisely what is new relative to that framework. Is the new content:

- exact preservation for every hard label budget M?
- the particular correlated two-channel reduction?
- an extension to arbitrary bounded decision problems with a constrained encoder?
- something stronger than what translation invariance would already imply?

At present the theorem is proved self-containedly, which is good, but it is not adequately *situated*. A self-contained proof of a classical invariant phenomenon does not become a four-journal result merely because a finite-label encoder is carried through the argument.

The correct comparison should include, at minimum, classical Gaussian-shift nuisance/invariance references and explain why the M-label restriction is not already covered by a standard invariant minimax reduction.

## 8. Decisive objection E5: the singular/contact theorem assumes the difficult global geometry

Theorem 4.2 assumes
[
lambda|b(	heta)-b(	heta')|
le
|V^{-1/2}(f(	heta)-f(	heta'))|
le
Lambda|b(	heta)-b(	heta')|
]
for every pair in the full parameter box.

Once this is granted, the rest of the theorem is a robust combination of:

- minimum-distance estimation;
- inversion of the contact powers;
- a product quantization cover;
- finite-hypercube testing;
- a representation covering lower bound.

That is mathematically sound infrastructure. But the genuinely difficult singular problem is often **proving** an appropriate two-sided modulus from the physical or geometric observation model, especially near changing rank, nonconvex fibres, multiple contacts, unknown marks, seams, or changing active strata.

Version 3 does not solve that problem in the historical A2/Sinai/hard-sphere settings. Instead it posits a global contact equivalence and then derives the minimax/label law.

The nonseparable shear example confirms consistency of the assumptions; it does not show that the assumptions arise in a difficult model.

This is not enough for the paper to claim a general solution of the singular-geometry side of theta theory.

### The statement about constant independence should also be qualified

The manuscript says the comparison constants are independent of contact orders, widths, noise scales, label budget, and unknown calibration. Formally, the displayed constants depend on (d,m,lambda,Lambda), not explicitly on the other quantities.

However, in actual model verification, (lambda) and (Lambda) may themselves encode severe dependence on contact order, scale, conditioning, or distance to degeneracy. The text should not let "independent of contact orders/noise scales" be read as a uniform physical statement unless (lambda,Lambda) are independently controlled in those regimes.

## 9. Decisive objection E6: the historical eleven-paper pipeline remains mathematically unresolved

The current `HISTORY_AUDIT.md` is honest about this, but the consequence needs to be stated more strongly.

The fixed historical dependency chains are
[
A2	o A3	o A4	o C2	o D1
]
and
[
B2	ext{-GC}	o B1	o B2	ext{-MC}	o B3	o B4	o C1/C2	o D1,
]
with A1 as a separate line.

The repository's Round-18 and Round-20 external-style reports give the following status:

| Component | Round-18 mathematical status | Round-20 recommendation |
|---|---|---|
| A1 | Main theorem package not proved | Reject without reconsideration |
| A2 | Unsmoothed four-dimensional local limit theorem not proved | Reject without reconsideration |
| A3 | Collision- and physical-clock path LDPs not proved for the Sinai billiard | Reject without reconsideration |
| A4 | Global spectral platform and renewal/memory theorem not established | Reject without reconsideration |
| B1 | Interacting exact-number Fourier majorant and shell coefficient theorem not proved | Reject without reconsideration |
| B2 | Grand-canonical pressure and both joint LDPs not proved | Reject without reconsideration |
| B3 | Observability, process CLT, and Mosco identification not proved | Reject without reconsideration |
| B4 | Nisio resolvent, m-dissipativity, graph-core corrector, and nonlinear semigroup limit not proved | Reject without reconsideration |
| C1 | Filter chart, belief-state DPP, LAN, and Bernstein–von Mises conclusions not proved | Reject without reconsideration |
| C2 | Model-specific rigidity, optional-projection limit, and universal contraction claims not proved | Reject without reconsideration |
| D1 | No model-specific phase theorem or posterior semigroup proved | Reject without reconsideration |

Version 3 does not silently import these failed claims. That is correct.

But then the historical pipeline contributes **no theorem credit** to the present paper beyond motivation and a list of interfaces. The current GTF manuscript advances an independent memory/statistical branch; it does not validate the old theta chain.

For the programme as a whole, this means that "General Theta Foundations" is not yet a foundation in the ordinary sense that downstream flagship theorems are established from it. It is a proposed common language plus several independent model theorems.

A four-journal foundation paper would need at least one major theorem showing that a genuinely difficult downstream model—rather than a designed benchmark—verifies the new axioms and obtains a result that was previously inaccessible.

## 10. Decisive objection E7: the integrated 52-page architecture dilutes rather than strengthens the new theorem

The v3 paper contains 20 theorems, 9 lemmas, 15 propositions, 4 corollaries, 48 proofs, and 13 examples. The source-preservation discipline is excellent.

Editorially, however, retaining nearly all of v1/v2 inside the same paper is now counterproductive.

The genuinely interesting v3 contribution is concentrated in:

- the future-orbit lower bound;
- the doubling-map phase transition;
- the exact additive-calibration quotient;
- the correlated contact/label law.

Much of the rest is a mixture of:

- classical probability/statistics identities;
- general bookkeeping lemmas;
- previously established filter stability;
- finite-reference control perturbation;
- interfaces to unresolved future work.

A top-tier paper is not made stronger by carrying every historical foundation into appendices. It is made stronger by isolating a deep theorem, proving the strongest natural form of it, and showing why it changes the subject.

I would strongly prefer two focused papers over the present integrated object:

1. a causal-memory/dynamical quantization paper that substantially generalizes the orbit theorem and phase transition; and
2. a calibrated singular-statistics paper only if the contact geometry can be derived in a genuinely nontrivial experiment.

The general axiomatic material could remain as a separate programme document or technical companion.

## 11. Major objection M1: the resource model is legitimate but still much narrower than ordinary "memory complexity"

The v3 text has improved this issue substantially. Persistent labels, program description, transient workspace, numerical error, and acquisitions are explicitly separated.

Nevertheless, Theorem 3.1 counts only the persistent M-state register. It permits:

- a free absolute clock;
- an arbitrary fixed program;
- unbounded computation between checkpoints;
- transient workspace not charged to M;
- time-dependent decoding in the lower bound;
- exact knowledge of the dynamical map and readout.

This is a perfectly coherent **state-cardinality** problem. It should not be rhetorically conflated with total storage, communication rate, algorithmic memory, or computational complexity.

This is another reason the comparison with the data-rate/control literature is necessary: the manuscript must explain exactly which resource is stronger or weaker than a per-time communication-rate constraint.

## 12. Major objection M2: the hard part of the doubling example starts only after perfect acquisition

At every reset the observer acquires an exact uniform real (U_t). The difficulty is entirely in how much of that exact observation can survive a random number of expanding unobserved steps.

That isolates the transport-of-information phenomenon beautifully, but it removes the interaction with noisy filtering at the acquisition moment.

The next serious theorem should combine:

- noisy or partial acquisition;
- expanding transport between acquisitions;
- a hard persistent-state constraint;
- and a matched lower/upper law.

Without such a result, the new theorem remains a purified benchmark rather than a general memory law for partially observed dynamics.

## 13. Major objection M3: the "phase transition" should be tested beyond dyadic symbolic exactness

The upper machine is almost perfectly aligned with the binary symbolic dynamics of the doubling map. This raises an unavoidable robustness question.

What happens for:

- (T(x)=axmod 1) with noninteger or variable expansion?
- piecewise expanding maps with nonconstant slopes?
- higher-dimensional toral endomorphisms?
- Markov expanding maps with nonuniform branch probabilities?
- a readout not equal to the state coordinate?
- small dynamical noise?
- a nongeometric reset law?

If the answer is that the threshold is determined by a pressure/entropy/Lyapunov equation, that could become a deep theorem. If the answer depends sharply on the exact symbolic coding, then the present result is less universal than the introduction suggests.

Version 3 does not resolve this.

## 14. Major objection M4: no general achievability theorem for orbit quantization

The lower bound allows arbitrary off-image centres in (ell^2), which is mathematically stronger than a current-state cover.

But the manuscript has no theorem explaining when an optimal or near-optimal orbit codebook can be implemented causally by an M-state machine. That is a highly nontrivial issue: an arbitrary M-centre quantizer of an infinite future-orbit vector need not admit a closed state update after applying (T).

This causal-realizability gap is precisely where a major theorem could live.

A satisfying "General Theta" result would identify a structural condition—finite automaton closure, Markov partition compatibility, approximate bisimulation, contracting quotient dynamics, or another invariant—under which future-orbit quantization is both a converse and an achievable memory law.

The current paper handles this only by an explicit suffix construction in the doubling example.

## 15. Major objection M5: v2 results are preserved, not independently upgraded by preservation

The build certifies that the v2 quantitative body is byte-identical. This is useful provenance.

It does not imply that v2 has received an independent mathematical referee pass. The current v3 submission treats several v2 results as established infrastructure. I spot-checked the main chains and did not find an immediate fatal defect, but a journal referee cannot substitute a byte-preservation test for mathematical validation.

If the paper remains integrated, the author should give a much shorter dependency map identifying exactly which inherited results are needed for the v3 claims and which are included only for completeness.

At present too much historical material is carried forward simply because it existed.

## 16. Major objection M6: the literature comparison should be theorem-by-theorem, not field-by-field

The introduction has improved since v1, especially in acknowledging Kara–Yüksel and approximate-information-state results.

For the new centre, however, I would require a table with columns such as:

- resource constrained (persistent states / bits per time / mutual information / block code);
- underlying dynamics (stable / unstable / expanding / regenerative);
- noisy or exact observations;
- causal vs noncausal encoding;
- objective (prediction / stabilization / rate distortion / control);
- converse class (all coders?);
- achievability class;
- invariant controlling the exponent/threshold.

The paper should then compare Theorem 3.1 directly with the strongest data-rate, quantized-estimation, causal rate-distortion, and dynamical rate-distortion results.

Likewise, Theorem 4.1 should be compared directly with invariant minimax reductions for Gaussian shifts with nuisance parameters.

Without that, the novelty audit is incomplete.

## 17. Major objection M7: the title still overstates what has been generalized

The title *General Theta Foundations I* suggests a base layer from which the rest of theta theory can be derived or organized with substantial theorem-level closure.

What is actually established is more specific:

- a typed framework for causal experiments and reductions;
- several general but mostly standard information/statistics identities;
- a general regenerative **lower bound**;
- one sharp expanding benchmark;
- one exact additive-nuisance Gaussian reduction;
- one contact theorem conditional on a strong global metric equivalence;
- several earlier finite-dimensional filter/control results.

That is a coherent research paper. It is not yet a general foundation of the historical spectral/LDP/kinetic/operator/phase programme.

The name would become justified if later papers really verify the interfaces. At present it functions as a programme label, not as a mathematical conclusion.

## 18. Point-by-point disposition of the controlling v1 objections

Because the author supplied a response to E1–E5 and M1–M7, I record explicitly what has and has not been closed.

### E1 — stronger mathematical centre

**Materially improved, not closed at the four-journal level.**

Theorem 3.1 is unquestionably a stronger centre than the v1 refreshing-HMM theorem. The remaining issue is breadth/universality, not absence of a theorem.

### E2 — beyond strong known-calibration refreshing

**Materially improved.**

The expanding nonacquisition intervals are genuinely noncontracting and arbitrarily long. However the replacement model is a perfect-regeneration benchmark, not a general weak/nonuniform filtering theorem.

### E3 — strict distinction from A1

**Substantively answered.**

The orbit metric captures information that the checkpoint law cannot. This is a real distinction from the A1 acquired-geometry theorem. I no longer regard "merely re-proving A1 in isotropic form" as the main objection.

The new question is whether that distinction can be made into a broad theorem beyond one symbolic model.

### E4 — relation to the whole pipeline

**The bookkeeping objection is answered; the mathematical pipeline objection remains.**

The revision correctly identifies the old gates and avoids circular substitutions. But no old hard gate is closed by v3.

### E5 — actual singular noisy measured-nuisance experiment

**Materially improved, but not fully closed.**

The correlated paired Gaussian experiment is actual and the nuisance is genuinely measured. The contact theorem is matched under its hypothesis. What remains missing is derivation of the two-sided contact geometry in a hard model.

### M1 — persistent labels/program/workspace/acquisition

**Largely closed as a definition issue.**

The remaining issue is interpretation and comparison with other resource models.

### M2 — acquisition laws

**Improved.**

The paper now includes distinct continuous, discrete, singular, and regenerative acquisition mechanisms. A broad theorem unifying their effective causal dimension remains open.

### M3 — control comparison

**Improved in v2 but not central to v3.**

The retained finite-reference Bellman theorem does compare against unrestricted discounted optimal control under explicit assumptions. It is a conventional perturbation result and should not carry the novelty burden.

### M4 — constants and dimension

**Partly closed.**

The manuscript displays many constants. It still does not analyze joint high-dimensional, weak-refresh, or near-critical scaling.

### M5 — paper architecture

**Not closed editorially.**

The mathematical centre is stronger, but the paper remains over-integrated.

### M6 — theorem-level literature

**Not closed.**

The POMDP/filtering comparison is better; the finite-rate control/dynamical rate-distortion/invariant-minimax comparisons remain missing.

### M7 — stable editions and reproducibility

**Closed to an unusually high standard.**

The source identities, build inputs, inherited trees, generated artifacts, and rendering checks are carefully pinned. This is excellent research engineering. It does not affect the editorial significance judgment.

## 19. Technical comments on the new proofs

These are not currently fatal objections, but they should be addressed in any focused successor paper.

### 19.1 Formalize randomized machines as kernels rather than "coding tapes"

The proof of Theorem 2.1 is intuitively correct when all independent randomness is frozen. A formal statement in terms of standard Borel stochastic kernels and a measurable randomization representation would remove any concern about the existence/measurability of the global "coding tape" construction.

### 19.2 State more explicitly why full history determines (X_t) in the checkpoint problem

The exact checkpoint risk (1/(12M^2)) is correct because full acquisition history plus observed modes and known deterministic dynamics determine the current state exactly. This should be stated in the theorem proof before invoking scalar uniform quantization.

### 19.3 The lower orbit metric and the causal state metric are not equivalent in general

The current text knows this, but it should become a proposition or explicit boundary example: small orbit distance need not imply existence of a stable finite-state causal update. This is the central obstruction to reversing Theorem 2.1.

### 19.4 Distinguish fixed-q asymptotics from uniform phase-transition asymptotics

The constants (c_q,C_q) are allowed to degenerate as (q) varies. Thus Theorem 3.1 is not a uniform critical theorem. The abstract/introduction should make that limitation explicit.

### 19.5 Theorem 4.1 is not full experiment equivalence

The manuscript already says this. Keep the limitation prominent. Equality of minimax risk for bounded losses about (	heta) under an unrestricted nuisance is weaker than a parameter-uniform Blackwell equivalence of the pair and difference experiments.

### 19.6 Theorem 4.2's global contact assumption should be accompanied by verification lemmas

At least one example substantially more difficult than a globally bi-Lipschitz shear of coordinatewise powers is needed if the theorem is to carry singular-geometry significance.

## 20. Reproducibility and presentation

The repository engineering is excellent.

The reviewed index records:

- a 52-page PDF;
- separate source and publication commits;
- source-manifest hashes;
- three stable TeX passes;
- 132 inherited mathematical labels;
- ordinary/optimized diagnostic agreement;
- negative controls for the critical logarithm and cross covariance;
- independent archive-only rebuild;
- page-level text and pixel comparison.

These checks make it unusually easy to know which manuscript has been reviewed.

They should remain supplementary. The manuscript is strongest when it does what the v3 response letter now says explicitly: the new lower/upper bounds, not the build receipts, are the answer to the mathematical objection.

## 21. What would be required to change my recommendation

I do not think another conventional revision—more examples, more diagnostics, a longer literature section, or additional interface lemmas—would be enough.

At least one of the following would materially change the paper.

### Route A: a true orbit-complexity theorem

Prove matching lower and upper causal-memory laws for a broad class of regenerative or partially observed dynamical systems, with the rate expressed through a recognizable invariant of the weighted future-orbit geometry.

A serious version might connect:

- covering/quantization dimension of orbit images;
- Lyapunov expansion or pressure;
- regeneration tails;
- causal realizability;
- and the M-state prediction risk.

The doubling theorem would then become the first exact example of a general result.

### Route B: a universality/critical-window theorem

Show that the (q=1/4) transition is one instance of a general pressure balance and derive the near-critical crossover (q=q_M), including nonconstant expansion or higher-dimensional examples.

That would make the "phase transition" a theorem about a class rather than a geometric-series accident of one map.

### Route C: noisy acquisition plus expansion

Prove a sharp law when each reset is only partially/noisily observed, so filtering uncertainty and post-acquisition information transport interact. This would genuinely connect the v2 filter geometry with the v3 orbit geometry.

### Route D: derive the singular contact metric in a hard model

Rather than assuming a global two-sided contact law, prove it—possibly stratified or local with matching global testing bounds—from an actual nontrivial observation geometry arising in the intended pipeline.

### Route E: close one historical hard gate from the new foundation

Show that the new GTF language resolves a theorem that the historical pipeline could not establish: for example, a genuine spectral/local-limit, particle-LDP, nonlinear-semigroup, unbounded-operator, or model-specific phase result.

That would provide evidence that "General Theta Foundations" is more than a clean parallel theory.

## 22. Final recommendation

**REJECT at the requested Annals/Acta/Inventiones/JAMS standard.**

This is a stronger and more serious paper than v1. The v3 regenerative phase transition is mathematically interesting, the exact nuisance quotient is clean, and the manuscript's boundary discipline is much improved. I do not base the rejection on a fabricated fatal proof error.

I base it on the fact that the paper still falls between two levels:

- its most general statements are infrastructure or one-sided reductions; while
- its sharpest new statements are solved in specially structured benchmark experiments.

The missing step is a theorem that turns the new future-orbit/contact viewpoint into a **broad structural result** with consequences beyond the designed examples.

The historical eleven-paper programme does not supply that missing depth, because its own load-bearing theorems remain unresolved in the latest fixed external-review record. The current manuscript is therefore best judged on its own mathematics, and on that basis I do not regard it as a plausible four-journal paper in its present form.

A focused successor centred on a genuinely general causal orbit-complexity theorem could be considerably stronger than the current integrated "Foundations I" presentation.
