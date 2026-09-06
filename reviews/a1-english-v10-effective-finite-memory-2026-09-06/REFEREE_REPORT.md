# Referee report — A1, English revision 10: effective finite memory

**Manuscript:** *Sparse observation algebras and effective memory across exponent collisions*  
**Author named in the manuscript:** Qian Qi  
**Date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation:** **REJECT at the requested four-journal level in its present form.**

This is an owner-requested, AI-assisted external referee-style assessment. It is not a report commissioned by any named journal. The recommendation concerns the mathematical significance demonstrated by this submission. It is not a claim that the research program is impossible, that an identical theorem is already published, or that the principal rate has been disproved.

## 1. Exact submission and scope

```text
repository:       TrillionniumFoundation/theta-theory
revision branch:  revision/a1-english-v10-effective-finite-memory-2026-09-06
submission SHA:   d9f48fe08fd694e636c287be7646ae7d723ce3b8
submission tree:  ec1599926cc2a90a7fe8f3315ebf07599487528e
commit time:      2026-09-06T07:53:19Z
principal path:   papers/A1-english-v10/
controlling v9
review/parent:    7a499e3cb32396b18eda869342ec8e9c70d8d028
v9 submission:    e3e5ba14de94eb3ff37a46ef6ed76c16929f98a5
review branch:    review/a1-english-v10-effective-finite-memory-harsh-2026-09-06
```

There are two contemporaneous v10 branches. The other, `revision/a1-english-v10-shared-memory-composition-2026-09-06`, points to `da5abea9f40244879115d5fbcfbda375bc9a123e`, dated 06:44:18Z. The effective-finite-memory branch is later by commit time and is the target here. Results from the shared-memory branch are not imported into this assessment. The selected revision head was checked again before the review branch was created and remained unchanged.

This is a detailed audit of the new principal chain and its critical inherited dependencies, not a claim to have independently certified every legacy appendix. I read the current main statements, the complete new effective and classical sections, the full intrinsic collision section, the experiment and transversality sections, the relevant finite-state definition, confluent-positivity and global-covering arguments, the response letter, the proof/resource ledger, the bibliography, and the controlling review's relevant conclusions and requests. Source labels are used below; no theorem number or page number is inferred from an unexamined PDF. The source index specifies the partial inherited-section reads.

I independently reran the two pinned author Python files after verifying their Git blob hashes. I also executed an intentional output-table mutation and a separate exact diagnostic program written without importing author code. The receipts are part of this directory. I did **not** rebuild LaTeX, inspect a rendered manuscript PDF, execute GitHub Actions, independently verify the claimed preservation inventory, rereview every historical branch, or rereview all eleven planned papers. The manuscript's reported 48-page build and preservation counts remain author-reported facts, not newly certified executions. [S0, S10–S12]

## 2. Executive assessment

V10 genuinely closes an implementation gap left by v9. Under a specified finite-data interface, it replaces calibration-dependent exact-real transition functions by integer transition tables and dyadic output tables. The running filter retains only an index. The proof does not secretly use a posterior vector at runtime, apply an update to an infeasible approximate posterior, reread the discarded history, or require deciding whether two exponent sums coincide. These are substantive and correctly handled operational points. [S8–S10]

**No blocking counterexample or essential unfilled step was found in the examined principal classification and finite-compilation proofs under their printed hypotheses.** The earlier closures concerning failure evidence, attainable rather than ambient dimension, zero-pivot handling, full-image covering, and accumulation of causal compression error should remain closed. An adverse recommendation must not reopen them merely to sound severe. [S2–S8]

My recommendation remains negative at the specifically requested four-journal level. The new compiler is a clean finite-net construction followed by classical farthest-first selection and finite-horizon Lipschitz error propagation. Its application verifies the finite moment data and imports the already established attainable covering profile. The paper has not yet demonstrated why this additional compatibility result, together with the inherited classification, constitutes an advance of exceptional general-mathematical importance. Correctness, priority and editorial significance are separate judgments.

There are also two concrete shortcomings in the numerical evidence: every reported off-grid accumulation check has a threshold larger than the entire possible error range, and the published suite accepts a deliberately corrupted program whose entire output table is zero. These are test-coverage failures, not counterexamples to the unmodified compiler or the analytic theorem. The original output tables pass additional referee checks. Section 6 records the exact distinction.

Finally, the numerical resource statement is unnecessarily weak even as a consequence of the present proofs. The accompanying [technical note](TECHNICAL_NOTE.md) proves, with no additional hypotheses or collision oracle, that sufficient precision can be reduced to

\[
 \frac{\log_2(M+1)}{(r-1)\lfloor N/2\rfloor}+O(1),
\]

with a corresponding improvement in program size. The printed log_2(M+1)+O(1) sufficient bound remains true. It should not be elevated into a sharp precision law.

## 3. Disposition of the controlling v9 report

| Item | What v10 supplies | Present disposition |
|---|---|---|
| E9.1: distinguish classical spectral content from the residual contribution | Explicit exterior spectral comparison and a separate finite compiler | Correctly separated. The compiler's significance is assessed below; the spectral statement is not misrepresented as new. |
| E9.2: consequences beyond another collision-tree calculation | Finite numerical realization without resolving the smallest additive gap | A real additional assertion. Its precision conclusion follows from stability plus a profile floor; it does not by itself resolve the editorial objection. |
| E9.3: clarify breadth and resource quantifiers | General compact Lipschitz compiler, with separately verified monomial inputs; explicit state/program/oracle distinctions | The effective model is genuinely broader than the original scalar example. The sharp geometric classification remains experiment-specific. |
| P9.1: explicit spectral proposition | `prop:exterior-profile` | Closed in the examined source. |
| P9.2: isolated arbitrary-prefix Hermite lemma | `lem:prefix-hermite`, with attribution | Closed in the examined source. |
| P9.3: a single principal dependency chain | Main input order places the intrinsic theorem and effective compilation before special-case appendices | Source organization improved. No fresh compiled-document or preservation-inventory certification is given here. |
| P9.4: distinguish preservation from reproduction | Explicit response plus local receipts | The distinction is maintained. The author suite was rerun here; its coverage limitations are newly identified below. |

The response should receive credit for answering the actual v9 requests. It would be inaccurate to call this merely v9 with a changed title. Equally, completing a previous report's presentation checklist does not settle a journal's significance judgment. [S0, S4, S10–S12, R9]

## 4. Audit of the mathematical chain

### 4.1 Experiment, exact tangent and normalization

The acquisition experiment counts rejected reports and uses a single shared hidden parameter. The future-only continuation cannot read the discarded prefix. Spanning failure probes therefore identify precisely the future monomial moments, not arbitrary hidden-parameter losses or an uncharged past-dependent payoff automaton. [S2]

At the interior factors F_i=(1+c_i t^D)/2, the unnormalized tangent has the explicit monomial support consisting of jD and a_i+jD. Its n(r−1)+1 exponents are distinct. The mixed-moment determinant is strictly positive for every full-support prior by the determinant integration identity and positivity on ordered disjoint intervals. The product belongs to the tangent, so subtracting its normalized constant component removes exactly one rank. This supports the stated minimum of past capacity and future test dimension. The argument does not require a density for the prior or extrapolate generic rank through a singular limit. [S3]

The exact continuous encoding is permitted to distinguish histories with equal posteriors; it is not asserted to be a global minimal quotient chart. The factor-to-moment changeover preserves this distinction. I found no new defect in this inherited exact-state claim. [S1, S3]

### 4.2 Newton flags, spectral content and collision uniformity

For an arbitrary ordered multiset, prefix divided differences are independent on the monomials of degrees 0 through p−1 and belong to the full Hermite-data space. Consequently they span complete derivative blocks, including when repetitions are not adjacent. Substitution of t^(Hz) gives complete exponential-polynomial blocks. This is a classical interpolation fact, separately distinguished from posterior attainment in the revision. [S4]

The Leja factorization has a uniformly invertible active triangular block and a zero tail. Completing inactive columns by coordinate vectors gives the bounded invertible factors used in the exterior spectral proposition; no zero pivot is inverted. The inequalities between maximal Vandermonde products and products of Leja pivots follow by a finite determinant expansion. These statements survive exact collisions. [S4, S7]

The statistical content is the pairing of the complete flag with the actual product tangent. Strict confluent positivity establishes rank at the collision itself. Bounds on t^c|log t|^j, positivity of evidence, compactness and the finite number of formal orderings then yield uniform local inverse bounds. The exploration measure includes the all-failure likelihood before complementary command coordinates are integrated out. A prior-density assumption has not been smuggled into this step. [S3, S5, S7]

### 4.3 Global cover and the lower-law geometry

For each report word, attainable moment coordinates are rational functions of command entries with positive polynomial evidence. Prior integrals are real coefficients; they need not vary semialgebraically with calibration. Individual factor normalization gives the dimension bound n(r−1). The inherited rectangle lemma combines bounded component counts of affine sections with the classical real entropy inequality, and bounds projected rectangle volumes by products of its largest side lengths. This is a global bounded-format argument, not a local-submersion argument applied to the entire image. Its budget inversion includes small M and recenters on reachable states. [S6, S7]

On the lower-bound side, the fixed physical/raw map and active Leja inverse have uniformly bounded norms. Projecting arbitrary decoder centers onto an attained scaled cube and applying a union-of-balls volume estimate gives each determinant term. Zero-volume terms vanish rather than require division. The same independent exploration law supplies every checkpoint converse, so taking a maximum is legitimate for a single filter. [S7]

These arguments are mathematically substantial parts of the inherited paper. Describing the entire result as nothing but a Vandermonde identity would be unfair. Their presence, however, does not automatically establish the editorial importance of each successive realization theorem.

### 4.4 Approximate greedy selection

`lem:finite-greedy` proves

\[
 R\le 2e_S(M)+a+4\tau.
\]

The farthest-first argument first bounds the covering radius of the approximate list by 2e_S(M)+2tau, allowing arbitrary centers; transferring back to exact samples and then to S adds a+2tau. Duplicate approximate points and the case with at most M indices are treated correctly. This is a valid numerical allowance around the acknowledged classical greedy mechanism, not a new clustering principle. [S8; L1]

### 4.5 Actual finite-table compilation

Grid histories form an A_n h-net of S_n. Each selected center is defined analytically by an actual history. To construct a transition, the proof appends the finite command/report to that history and evaluates the resulting reachable state offline. It never assumes that a numerically perturbed vector lies in S_n.

The resulting recurrence is

\[
 E_{n+1}\le L_nE_n+G_nh+2e_{n+1}(M)+A_{n+1}h+8\tau.
\]

The four-tau transition allowance and the four-tau covering allowance are both included. The finite horizon controls accumulation, and K_nE_n+tau controls query error. Rational comparisons, including ties, terminate under the evaluation hypothesis. The running machine needs neither histories nor an oracle; those belong to synthesis. No central proof gap was found in `thm:compact-compiler`. [S8]

The theorem does assume that every rational grid history can be evaluated. It is not an effective extraction theorem from an arbitrary presentation of a compact set. That assumption is explicit and appropriately verified for the monomial application; it should not be omitted in broad descriptions of the result.

### 4.6 Finite moment data and precision

The formal degree-N moment table supplies every state numerator and prefix evidence denominator. Since the latter is at least kappa^n, bounded coefficient perturbations give certified quotient errors without cancellation-based rank tests. Coincident labels are retained, which is harmless even when perturbed numerical entries do not satisfy exact coincidence identities: the approximations are used for offline selection, not treated as exact attainable states. [S8]

The raw state and command Lipschitz estimates are gap-independent. Applying the compiler and squaring gives C(Xi+h^2+tau^2). The stated h,tau=O(M^−1) choice is sufficient because Xi>=M^−2. The calibration estimate follows from the bounded derivative of t^b for b bounded away from zero. These are sound arguments, but their logical conclusion is sufficient precision, not a matching precision converse. Section 5 sharpens the floor used in this application. [S8]

### 4.7 Resource and lower-bound quantifiers

A fixed memoryless input coder can be simulated by an exact-command filter, so the original M-state lower law remains applicable. A history-dependent input naming rule would be a side channel and is excluded. The read-only program, supplied clock, transient workspace, approximation advice, and oracle running time are distinguished in the source. Noncomputable arbitrary priors retain an existential classification, not an algorithm for producing unsupplied noncomputable data. [S8–S10]

The operation count is polynomial in M for fixed dimensions and horizon, not polynomial in the persistent bit budget log M, and not a bound on an arbitrary oracle's running time. Those are stated limitations, not newly discovered errors. The significance assessment must nevertheless respect the resource problem actually solved.

### 4.8 Tree and contact consequences

The pair-order tree computes valuations of finitely many determinant products. The displayed two-parameter example groups the nine future exponents into six separated clusters, with three internal gaps |u|, |v−u| and |v−2u|. Its interpolation of the seven-dimensional term and the two crossover exponents are consistent with the stated three-term profile. The digital corollary realizes that existing profile; it does not produce a new classification of collision arrangements. [S7, S8]

## 5. A substantive quantitative improvement already available from the proof

Set

\[
 d_0=(r-1)\lfloor N/2\rfloor.
\]

At the balanced checkpoint, the future sumset contains the explicit separated chain jD and a_i+jD. Compactness in the one-step chamber makes its gaps uniformly positive, even when other additive gaps vanish. Thus a d_0-node determinant witness is uniformly positive and

\[
 \Xi_N(M,a)\ge c_K M^{-2/d_0}.
\]

The full proof, including the chain cardinality and the exact determinant constant, is in [TECHNICAL_NOTE.md](TECHNICAL_NOTE.md), Propositions 1–2. The unchanged compiler therefore permits

\[
 h,\tau=O(M^{-1/d_0}),\qquad
 b(M)=d_0^{-1}\log_2(M+1)+O(1),
\]

and has a sufficient read-only program size

\[
 O(M^{1+J/d_0}\log(M+1)).
\]

No additive-gap oracle is needed. For the four-cell, five-trial example, d_0=6 and J=4, giving sufficient precision (1/6)log_2(M+1)+O(1) and program size O(M^(5/3)log(M+1)), rather than the displayed sufficient log_2(M+1)+O(1) and O(M^5 log(M+1)). The entire collision-dependent regret profile is retained; it is not replaced by its baseline floor.

This observation does **not** refute either printed upper bound. It does show that the advertised numerical resource accounting is not yet the strongest direct consequence of the manuscript's own structure. Both the original and improved statements are one-sided numerical resource bounds. A converse for persistent labels alone cannot establish optimal input precision or optimal program length.

## 6. Reproduction: what passes, what the tests fail to detect

### T10.1 — The reported off-grid error checks are vacuous

In `tests/test_v10.py`, each `accumulated_offgrid_error` assertion compares the raw-state error with

```text
128 * previous_error + 192 * (1/4) + sample_cover_radius + 4 * tau.
```

Every term is nonnegative, so the threshold is at least 48. Both compared exact raw vectors consist of posterior moments in [0,1], so their maximum-norm distance is at most 1. Consequently all 432 such assertions are true regardless of which valid representative index is selected. They cannot detect a violation of useful off-grid error control. This is a defect in diagnostic sensitivity, not an invalidation of the conservative analytic Lipschitz constants. [S11]

### T10.2 — A zero-output program passes the complete author suite

The unmodified author suite was freshly executed and passed all **7,904** assertions. The two source files were reconstructed from the connector's decoded contents and verified against the repository's Git blob hashes before execution; they were not silently patched.

The referee then replaced **every integer in each returned `Program.outputs` table by zero**, leaving transitions, state counts, output precision and the original `Machine` class unchanged. All nine compiled fixture programs were corrupted in this way. The same author suite still passed **7,904** assertions.

This has a simple explanation: the runtime checks ask only query 0 and assert that the returned number lies in [0,1], not that it approximates the true prediction. At checkpoint n=2 with N=3, query 0 is the constant factor 1/2. The corrupted program returns 0 and has squared error exactly **1/4** on that query. A zero output table would retain this nonvanishing error for every M; the existing test does not notice. [S11]

The distinction is important. The referee's extra **495** all-query checks confirm that the **original** stored outputs match their true representative predictions within the dyadic rounding allowance on these fixtures. The same checks detect **495** corrupt entries after zeroing. I am not reporting that the submitted compiler actually outputs zero, nor presenting this deliberate mutation as a counterexample to its theorem. [MUTATION_DIAGNOSTICS.json](MUTATION_DIAGNOSTICS.json)

### T10.3 — The new finite-input hypothesis needs direct perturbation tests

The author's fixtures use exact rational prior integrals before dyadic rounding. They therefore do not directly exercise the certified perturbation of the finite coefficient and prior-moment input table, which is an important addition in v10. This is a coverage omission, not evidence that `lem:finite-moments` is false. [S8, S11]

The separate referee program uses no author imports and passes **36,960 exact assertions**. It tests signed approximation errors in greedy selection; exact and near-collision determinant volumes; perturbed coefficient and moment inputs with certified denominator/quotient errors; all physical query outputs in its finite monomial fixtures; and complete index-based causal filtering of a separate compact Lipschitz example on off-grid input histories. Its 4,608 state-error recurrence checks have bounds strictly below the entire unit error range. It also checks 35 instances of the separated-chain witness used in Section 5. [INDEPENDENT_DIAGNOSTICS.json](INDEPENDENT_DIAGNOSTICS.json)

The independent count includes elementary range, budget and algebra checks, as does the author's count. Neither is a count of independent mathematical propositions. Neither establishes continuum entropy, asymptotic sharpness, exhaustive priority, or editorial merit. The purpose is to produce sensitive, reproducible tests rather than a larger acceptance-looking number.

## 7. Grounds for the negative editorial recommendation

### E10.1 — The new theorem is a useful compilation lemma, not yet a demonstrated major new mechanism

Once a finite-horizon state representation, Lipschitz constants and finite evaluation access are supplied, the proof enumerates grid histories, performs acknowledged farthest-first selection, compiles their continuations and sums a stability recurrence. The posterior application adds bounded rational evaluation from a finite moment table. The sharp profile is supplied by the inherited attainable geometry, not discovered by the compiler. [S7, S8]

This does not mean short arguments cannot be profound, or that combining classical tools cannot give a major theorem. It means the present paper must defend the importance of the precise combination it proves. I do not find that defense sufficiently persuasive for the requested journals. The strongest original mathematical burden remains the experiment-specific attainable classification; the new computational packaging has not yet given it a comparably far-reaching consequence.

### E10.2 — The numerical novelty needs a sharper comparison and resource statement

There is an established literature on finite approximations of control models, finite-memory partially observed control and approximate information states. Saldi–Yüksel–Linder study finite-state approximations with convergence rates in compact-state MDP settings; Kara–Yüksel study finite-memory feedback policies; Subramanian and coauthors study approximate information states and planning bounds. The latter two are already in the inherited bibliography, so their existence is not an accusation of omitted citations. [L2–L4; S12]

These sources do not, on the evidence consulted here, supply an identical theorem with the present all-history, fixed-M, reachable-representative and finite-table quantifiers. Their objectives and hypotheses differ. A useful comparison should identify that difference precisely, and explain why preserving the collision-sensitive attainable covering order is consequential beyond another finite abstraction. Merely citing them or calling the compiler general is insufficient. This targeted source comparison is not a theorem-level subsumption proof or an exhaustive priority search.

The improvement in Section 5 further shows why the present log M precision statement should be presented as a convenient sufficient choice, not as a sharply resolved computational frontier. Program size and numerical precision have no matching lower bounds here. The paper is honest about much of this; the problem is the weight placed on a resource conclusion that has not been optimized even within the current method.

### E10.3 — A resolved implementation issue is not automatically a resolved significance issue

The known calibration, fixed positive likelihood margin, finite horizon, fixed full-support prior and specified finite query menu are mathematically legitimate. Dropping those assumptions without proofs would be worse, not better. The revision correctly distinguishes them from the abstract compact-state compiler. [S1, S2, S8–S10]

Nevertheless, the manuscript still establishes a sharp persistent-state order in this particular acquisition/prediction family, with separately counted read-only program and numerical advice. It does not thereby establish a sharp general law of total computational memory, arbitrary decision quality or growing-horizon filtering. The retained affine, decision and mechanical material is not a substitute for demonstrating the importance of the exact principal problem solved. I have not freshly re-audited those appendices and do not use an unexamined appendix as evidence for rejection.

Adding more preserved proof blocks, broader wording or additional diagnostic counts would not address this judgment. A genuinely consequential application, a sharply differentiated approximation theorem, or a new structural restriction could change the assessment, but no particular one of those is imposed as a mandatory research direction and none guarantees acceptance.

## 8. Concrete revision requests and next-review handoff

**P10.1 — Repair the diagnostic oracle.** Check every stored query output against an independent exact prediction or certified interval, including nonconstant queries. Retain a deliberate decoder/output-table corruption as a negative control. Replace the >=48 off-grid thresholds with informative recurrences or exact finite-domain checks. State clearly what each assertion family can detect.

**P10.2 — Exercise the finite numerical inputs.** Perturb the supplied moment and coefficient tables within declared error budgets; check positive denominators, quotient error certificates and end-to-end predictions. Keep exact-collision labels separate and include perturbations that destroy their numerical equality, as the mathematical compiler allows.

**P10.3 — Strengthen the sufficient resource accounting.** Address the separated-chain improvement in the attached note, or explain precisely why a different claimed resource model would prevent its use. Preserve the full Xi profile. Label precision and program-size conclusions as sufficient unless an appropriate converse is proved.

**P10.4 — Give a theorem-specific literature comparison.** Compare the compiler's hypotheses, output guarantee, effective input representation, exact M-label budget and finite program with finite-model approximation and approximate-information-state results. Do not claim an identical predecessor without a theorem establishing it; do not count the classical spectral and greedy facts as new mechanisms.

**P10.5 — Keep the mathematical contribution distinct from the publication target.** Present the attained geometry, finite compilation and separate specializations with their correct scopes. The direct proof chain and attribution improvements in v10 should be retained. No arbitrary deletion of valid content or weakening of the established theorem is requested.

P10.1–P10.4 are concrete mathematical or evidentiary improvements. Completing them would not by itself reverse the four-journal recommendation. The unresolved editorial burden is the demonstrated depth and independent consequence of the contribution, not a fabricated impossibility or a demand to abandon the program.

**Final recommendation: reject at the requested four-journal level in the present form.** The new finite-table theorem appears sound on the evidence examined and genuinely improves the operational realization. The submitted numerical validation is less probative than its assertion count suggests. A stronger sufficient precision bound is already derivable from the paper's own structure. The submission has not yet established the exceptional significance required for the requested destination, in this referee's judgment.

## 9. Immutable source and evidence index

All S0–S12 below refer to submission `d9f48fe08fd694e636c287be7646ae7d723ce3b8`.

- [S0: Main source and input order](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/main.tex).
- [S1: Introduction](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/sections/introduction.tex) and [exact main statements](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/sections/exact_statements.tex).
- [S2: Experiment and future-only equivalence](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/core/02_experiments.tex).
- [S3: Complete transversality and exact-state section](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/core/03_transversality.tex).
- [S4: Complete classical interpolation section](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/sections/classical.tex).
- [S5: Inherited confluent section, examined lines 90–260](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/core/05_confluence.tex#L90-L260).
- [S6: Inherited bounded-format cover, examined lines 1–230](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/core/06a_attainable_filtration.tex#L1-L230).
- [S7: Complete intrinsic collision section](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/core/06b_collision_geometry.tex).
- [S8: Complete finite numerical compilation section](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/sections/effective.tex).
- [S9: Operational definition and inherited stability, examined lines 1–130](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/core/06_streaming.tex#L1-L130).
- [S10: Response to referee](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/RESPONSE_TO_REFEREE.md) and [proof/resource ledger](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/PROOF_LEDGER.md).
- [S11: Author compiler](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/finite_compiler.py) and [author test suite](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/tests/test_v10.py).
- [S12: New bibliography entries](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/references.tex) and [inherited bibliography](https://github.com/TrillionniumFoundation/theta-theory/blob/d9f48fe08fd694e636c287be7646ae7d723ce3b8/papers/A1-english-v10/references-v9.tex).
- [R9: Controlling v9 report](https://github.com/TrillionniumFoundation/theta-theory/blob/7a499e3cb32396b18eda869342ec8e9c70d8d028/reviews/a1-english-v9-2026-09-06/REFEREE_REPORT.md), particularly Sections 2, 4 and 7–9.

### Targeted primary-literature references

- **L1.** T. F. Gonzalez, *Clustering to minimize the maximum intercluster distance*, Theoretical Computer Science 38 (1985), 293–306, [doi:10.1016/0304-3975(85)90224-5](https://doi.org/10.1016/0304-3975(85)90224-5). Attribution is already present in the submission; the needed finite greedy argument was checked directly in S8. No claim of a fresh full-text reading of this original paper is made.
- **L2.** N. Saldi, S. Yüksel and T. Linder, *Asymptotic Optimality of Finite Approximations to Markov Decision Processes with Borel Spaces*, [arXiv:1503.02244v3](https://arxiv.org/abs/1503.02244v3). The primary abstract describes finite-state MDP approximations, compact-state rate bounds and order-optimality results under that paper's hypotheses.
- **L3.** A. D. Kara and S. Yüksel, *Near Optimality of Finite Memory Feedback Policies in Partially Observed Markov Decision Processes*, JMLR 23(11) (2022), 1–46, [primary article page](https://jmlr.org/papers/v23/20-1152.html).
- **L4.** J. Subramanian, A. Sinha, R. Seraj and A. Mahajan, *Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems*, JMLR 23(12) (2022), 1–83, [primary article page](https://jmlr.org/papers/v23/20-1165.html).
- **L5.** C. de Boor, *Divided Differences*, Surveys in Approximation Theory 1 (2005), 46–69, [primary arXiv record](https://arxiv.org/abs/math/0502036); Y. Zhang and J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, [arXiv:2311.05116v4](https://arxiv.org/abs/2311.05116v4). The record/version metadata were checked; the current audit does not claim a new full-text verification of every external theorem cited in the inherited real-geometry argument.

The new literature comparison is deliberately scope-level, based on retrieved primary records and abstracts plus the submission's explicit proofs. It is not an exhaustive priority certificate. The negative recommendation does not rely on alleging that any of L1–L5 already proves the complete A1 theorem.
