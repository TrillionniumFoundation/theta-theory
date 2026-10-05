# Referee Report — General Theta Foundations I, Revision 82 (r52)

**Focused quantitative manuscript:** *Finite-Use Geometry and Learning of Ordered Quantum Measurements*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v82-finite-outcome-native-2026-10-05`
- `revision/general-theta-foundations-i-v82-finite-outcome-publication-2026-10-05`
- `revision/general-theta-foundations-i-v82-finite-outcome-review-ready-2026-10-05`
- `revision/general-theta-foundations-i-v82-r51-response-2026-10-05`

**Reviewed exact final head:** `57937576a6f413594589d0509a6816ca4ea3a83e`  
**Candidate publication:** `4fe7ac00523cbff0e437d06fa2fe1969eb15cc73`  
**Qualified native source:** `868c841240f62a35cf7fc16ace388b0d11dfa920`  
**Completed predecessor:** Revision 81, `67ada63a593d452f23e8d26540504b8fb8ab8acc`  
**Controlling external report:** v77/r51, `96a3666ed516ea12fcdb8ede341b7082e4ff2c78`  
**Controlling proof/pipeline audit:** v77/r51, `d01b5b4d48955e8c6f0c5592213b8628e12a66dd`  
**Source qualification run:** `37254696596`, conclusion `success`  
**Exact-head read-only reconstruction:** `37255323514`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v82-external-referee-r52-2026-10-05`  
**Date:** 5 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 82 is a mathematically substantive response to the principal scope objection in r51. The new Sections 65–66 are not cosmetic. They extend the binary interior theory to a full-dimensional family of ordered, noncommuting, finite-outcome POVMs,

```text
sum_j E_j = I_d,
I_d/(2k) <= E_j <= 3I_d/(2k),
```

with no common eigenbasis assumption. The paper proves a finite-use operational comparison, sharp affine covering order, an exact public rational code, a common learner, a coherent-adaptive lower bound, a matching joint `d,N,delta,eta` query law for every fixed outcome count, and a finite exact risk-certificate transfer. I did not find a fatal mathematical gap in the horizontal matrix lift, the adaptive cross-slot cancellation, the affine-volume argument, the normalization-preserving rational grid, the binary-relabeling upper reduction, the split-label coherent lower reduction, the clipping step, the description-length converse, or the Choi-record continuity estimate.

The strongest new statements are, with `p=(k-1)d^2`,

```text
(1/128) min{1, sqrt(N) max_j ||E_j-F_j||_op}
    <= D_N^na(E,F)
    <= D_N(E,F)
    <= min{2, 2k sqrt(N) max_j ||E_j-F_j||_op},
```

```text
log_2 C_(N,k)(delta)
    = (p/2) log_2 N + p log_2(1/delta) + O(p log(k+1)),
```

and, for every fixed `k`,

```text
M^*_(d,k)(N,delta,eta)
    = Theta_k(N delta^(-2) [d^2 + d log(1/eta)]).
```

These are serious specialist-level contributions. They materially strengthen the v77 object reviewed in r51 and answer the binary-only objection on a noncommuting interior family.

The four-leading-general-journal conclusion nevertheless remains negative. The new multi-outcome theorem is an **interior** theorem, not a boundary theory for the full POVM body. Its lower query bound is independent of growing `k`, while the constructive upper has a displayed `k^3` factor. Thus the theorem is sharp only after fixing the outcome count. The exact code is finite but intentionally exhaustive; no efficient synthesis or general physical learner is executed. The focused article is now eighty-one pages and combines an already large binary closed-body theory with a second finite-outcome interior theory, several learning models, exact codecs, confidence converses, finite-control synthesis, and certificate machinery. The breadth is substantial within mathematical quantum information, but I do not see a single theorem of sufficient generality or an external consequence of sufficient reach to justify one of the four leading general mathematics journals.

The priority boundary also remains open. Mele and Bittel's 2026 revision of *Optimal learning of quantum channels in diamond distance* already treats finite-output measurement channels in its general channel theorem and supplies the binary operator-norm primitive used here. Zambrano, Ramos-Calderer, and Kueng's 2026 *Fast quantum measurement tomography with optimal error bounds* gives outcome- and dimension-optimal sample complexity for nonadaptive single-copy POVM tomography under its worst- and average-case losses. Those models do not imply the present future-`N` operational metric, arbitrary-coherent-adaptive converse, exact public description law, or finite certificate transfer. They do, however, prevent any broad claim that finite-outcome POVM learning or dimension-optimal measurement tomography is newly introduced here. The author-side literature audit recognizes this, but an independent human specialist priority review has still not been obtained.

**Disposition outside the four leading general journals:** the quantitative paper is a strong and technically mature candidate for a leading specialist journal in mathematical quantum information after an independent priority review and editorial compression. The structural companion should be submitted separately. I would not request another wholesale mathematical reconstruction.

---

## 1. Frozen object, genealogy, and material reviewed

The v82 response and referee-ready aliases coincide at

```text
57937576a6f413594589d0509a6816ca4ea3a83e.
```

The final head is a metadata-only child of the publication commit. It adds the exact-head read-only reconstruction request and records that no manuscript source changes were made after publication. The publication is a direct child of the qualified native source. The completed mathematical predecessor is v81, not the v77 object reviewed in r51.

Revision 82 preserves the complete v81 native corpus and adds two principal mathematical sections:

- `sections/65-finite-outcome-geometry.tex`;
- `sections/66-finite-outcome-learning.tex`.

The new focused quantitative article is 81 pages, the unchanged structural companion is 41 pages, and the complete preservation edition is 220 pages.

I reviewed, in particular:

- `quantitative.tex`, `structural.tex`, and `main.tex`;
- Sections 53–64, insofar as they are prerequisites for the v82 reductions;
- Section 65, including the horizontal ODE, finite-use comparison, affine entropy, rational grid, and exact code;
- Section 66, including the common learner, coherent converse, description-length converse, and finite certificate;
- `FINITE_OUTCOME_PROOF_AUDIT.md`;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `RESOURCE_LEDGER.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- `finite_outcome_certificate.py` and `finite_outcome_check.py`;
- the finite-risk and inherited learner dependencies actually invoked by v82;
- the source and publication genealogy from v81;
- the build receipt, source hashes, theorem locations, page checks, preservation inventory, and standalone packages;
- the source-qualification and exact-final-head workflows;
- the complete r51 external report and proof/pipeline audit; and
- the frozen repository-wide A/B/C/D analytic dependency ledger.

I also made a targeted current-literature check of the primary Mele–Bittel and Zambrano–Ramos-Calderer–Kueng records. This was not an exhaustive novelty search and should not be mistaken for the independent specialist review still requested in r51.

---

## 2. Executive assessment of the new mathematics

### 2.1 A noncommuting finite-outcome interior

The target family

```text
P_(d,k) = {(E_1,...,E_k): sum_j E_j=I,
           I/(2k) <= E_j <= 3I/(2k)}
```

has real affine dimension `(k-1)d^2`. It is exactly the radius `1/(2k)` ball about the uniform measurement in the norm

```text
r(E,F)=max_j ||E_j-F_j||_op
```

inside the affine subspace `sum_j H_j=0`. This observation is elementary but important: the entropy calculation takes place in the genuine affine norm ball, not in a commuting or diagonal submodel.

### 2.2 Horizontal finite-use comparison

For the line segment `A_j(t)=E_j+t(F_j-E_j)`, the paper solves

```text
dot X_j = (1/2) X_j A_j^(-1) H_j,
X_j(0)=sqrt(E_j).
```

Uniqueness gives `X_j^*X_j=A_j`, and hence

```text
X_j^* dot X_j = H_j/2,
dot X_j^* dot X_j = H_j A_j^(-1) H_j /4.
```

The Stinespring lift duplicates the classical label into an inaccessible environment. Exact normalization gives

```text
W_t^* dot W_t = (1/2) sum_j H_j = 0.
```

This cancels cross-slot derivative terms for a common purified adaptive tester. The diagonal terms contribute only `N` times the one-slot tangent energy, producing the `sqrt(N)` path bound. The argument is genuinely noncommutative; no step requires `A_j H_j=H_j A_j`.

This is the conceptual center of the new geometry.

### 2.3 Affine entropy and exact rational coding

The lower metric comparison turns every sufficiently small operational ball, even one centred at an arbitrary legal measurement outside the target interior, into an `r`-ball of radius `O(delta/sqrt(N))`. Volume comparison in the `(k-1)d^2`-dimensional affine space gives the lower covering order.

The upper covering is the usual maximal-net argument in the same norm. The new effective point is the normalization-safe grid: move inward, round only the first `k-1` effects, define the last effect as the exact residual, and retain tuples satisfying both spectral inequalities. This avoids the invalid independent-rounding shortcut `sum_j E_j != I`.

The resulting public dictionary has the correct fixed-length order. It is exact and finite, but its reconstruction may be enormous. The manuscript correctly treats transmitted bits, dictionary construction, workspace, and trusted controls as different resources.

### 2.4 Common learning at fixed outcome count

For each outcome `j`, public classical relabeling converts one call to the unknown `k`-outcome measurement into one call to the binary effect

```text
F_j = I/4 + E_j/2.
```

The inherited confidence-optimal binary procedure estimates each component. A complete finite tuple-grid search then legalizes all estimates simultaneously. The operational comparison converts component operator error into future-`N` loss. A public exact dictionary supplies the reusable word without further device calls.

This upper construction is common to the entire target family and does not use the pair-dependent eigenvectors from the metric lower bound.

### 2.5 Coherent-adaptive converse

The lower reduction embeds a binary interior effect `F` into `k` ordered effects by splitting the two binary labels into two groups and, when `k` is odd, adding one erasure label. The survival probability

```text
q = 2 floor(k/2)/k
```

is at least `2/3`. The simulation is valid on subnormalized reference states, so it survives entangled inputs and arbitrary adaptive training.

Coarse-graining a learned tuple gives an effect close to `qF` in the actual finite-use metric. The general Bernoulli lower witness gives operator error, and spectral clipping returns an interior binary effect. The inherited binary confidence lower bound then yields the full `d^2+d log(1/eta)` term.

The lower bound does not scale with growing `k`; consequently the paper correctly restricts its minimax sharpness claim to fixed `k`.

### 2.6 Finite certificate transfer

The one-call maximally entangled record is

```text
Omega(E) = (1/d) direct_sum_j E_j^T.
```

The tuple operator norm controls its trace norm by `k r(E,F)`. Tensor telescoping over `M` acquisitions gives `Mk r`, and any fixed readout contracts this to index-law total variation at most `Mk r/2`.

The proof transfers one fixed set of good output labels from a nearby net point. It does not assume that the decision boundary moves continuously. This is the correct way to pass a finite exact risk table to the continuum.

---

## 3. Detailed correctness audit

### 3.1 Matrix ODE and horizontal identities

The ODE coefficient is continuous because every segment effect stays uniformly positive. If `B_j=X_j^*X_j`, then

```text
dot B_j = (1/2) H_j A_j^(-1) B_j
          + (1/2) B_j A_j^(-1) H_j.
```

The function `A_j` solves the same linear matrix equation and has the same initial value. Uniqueness therefore gives `B_j=A_j`. The displayed first- and second-derivative identities follow in the stated order. In particular, the proof does not commute `H_j` past `A_j^(-1)`.

I find this step correct.

### 3.2 Adaptive path derivative

Purifying all controls and retaining a fresh inaccessible dilation environment for each call is legitimate. In the inner product between derivative terms from two different slots, cancel the later common isometries. At the later differentiated slot the remaining operator is `W_t^* dot W_t` or its adjoint, which is zero. This cancellation does not depend on the incoming state and remains valid for controls coherently conditioned on previous classical labels.

The norm of the derivative of the purified final vector is therefore at most `sqrt(N)||dot W_t||`. Passing to a rank-one density operator introduces the factor two; trace and final processing contract trace norm. Padding stopped branches by discarded dummy calls covers bounded public stopping.

I found no missing stationarity, independence, or no-reference assumption here.

### 3.3 Tangent-energy bound

Since `A_j(t)>=I/(2k)`,

```text
A_j(t)^(-1) <= 2k I.
```

Congruence by the Hermitian `H_j` gives

```text
H_j A_j(t)^(-1) H_j <= 2k H_j^2.
```

Summing, taking the operator norm, and using `H_j^2<=r^2 I` yields the displayed `O(k sqrt(N) r)` bound. The constants are conservative but valid. Dependence on growing `k` is not hidden.

### 3.4 Nonadaptive lower witness

Select one outcome whose effect difference attains the tuple norm and use an extremal eigenvector repeatedly. Coarse-graining the ordered record to the indicator of that outcome produces a product Bernoulli experiment with parameter gap exactly `r(E,F)`. The inherited finite product lower bound yields the stated absolute constant.

The witness is pair dependent, which is permitted in a metric lower bound. The paper does not use it as an estimator.

### 3.5 Covering lower bound with arbitrary centres

When operational distance is below `delta<1/128`, the lower metric inequality forces the centre to lie within operator tuple radius `128 delta/sqrt(N)`. This remains true for any legal ordered measurement, not only for a centre in the balanced interior. Consequently, each covering ball captures no more affine volume than an `r`-ball of that radius. Dividing by the target-ball volume proves the lower entropy order.

This correctly addresses the arbitrary-centre issue emphasized in the earlier referee reports.

### 3.6 Rational grid

The inward displacement gives margin `2e` from both spectral faces. Coordinate rounding of each of the first `k-1` matrices costs at most `d/K` in operator norm; the exact residual effect costs at most `(k-1)d/K=e`. The chosen denominator gives `e<=t/4`. Hence every rounded effect stays legal and the full tuple is within `3t/4` of the target.

Legality and tuple-distance tests reduce to exact rational positive-semidefinite predicates. Equality is included. The finite grid is therefore a genuine net, not a floating-point sample.

### 3.7 Greedy exact dictionary

A point is retained only when its tuple distance from all previous retained points is strictly greater than the separation threshold. Rejected points are assigned to an earlier centre at closed distance at most that threshold. Combining the grid error and greedy error gives the stated cover. Disjoint half-radius norm balls give the cardinality upper bound.

For real inputs supplied by certified rational approximations, the grid lemma leaves a strict margin, so progressively finer certificates eventually establish membership in one assignment ball. The paper does not pretend that arbitrary unrepresented real numbers can be compared exactly.

### 3.8 Upper learner and legalization

The public `3/4,1/4` relabeling exactly implements `I/4+E_j/2`, including the external reference. The `k` binary learners use fresh records. A union bound is sufficient; no independence of their final readout events is required.

On the common good event, the raw Hermitian estimates are within `epsilon` of the target effects. A complete grid at radius `epsilon/2` contains a legal tuple within `epsilon/2` of the target and therefore within `2epsilon` of every raw estimate. The finite search must therefore terminate on the good event. On every other record the uniform tuple is a defined legal fallback.

The final error ledger is conservative:

```text
r <= 3 epsilon,
D_N <= 3 delta/8,
public code adds <= delta/4,
total <= 5 delta/8.
```

The call count is `k` times the binary cost at accuracy `delta/(16k ceil(sqrt N))`, hence the displayed `k^3` upper factor.

### 3.9 Coherent binary embedding

For even `k`, the two groups of split labels exactly reproduce the binary instrument. For odd `k`, the extra effect is `I/k`. Erasing the internal binary outcome on the extra-label branch sums the two subnormalized reference states and therefore gives exactly `rho_R/k`. The reduction is valid for arbitrary entangled probes and adaptive controls.

This is a stronger statement than equality of scalar outcome probabilities and is proved at the right instrument level.

### 3.10 Coarse-graining and clipping

Postprocessing the learned tuple by coarse-graining cannot increase the operational distance. The lower metric comparison then gives

```text
||H-qF||_op <= 128 delta/sqrt(N).
```

The spectrum of `H/q` can exceed the binary interior, but Weyl's inequality shows that its excursion beyond `[I/4,3I/4]` is at most its distance from `F`. Clipping therefore moves it by at most that distance. A triangle inequality, rather than an unsupported operator-Lipschitz assertion, gives the factor two.

The accuracy cap `delta<=2^-24` is more than sufficient for the inherited binary lower theorem.

### 3.11 Description converse

Under a fixed public deterministic decoder, a learner with failure strictly below one must have at least one successful word at every target. The decoder image therefore covers the whole target body. The operational entropy lower bound applies independently of the number of training calls.

This is a fixed-length public-decoder statement. It should not be conflated with the retained shared-randomness expected-prefix model.

### 3.12 Finite certificate

The normalized Choi record is correct, and

```text
||Omega(E)-Omega(G)||_1
    <= k r(E,G).
```

Tensor telescoping gives the `Mk r` record bound. A fixed readout contracts trace distance, giving the factor `1/2` for total variation. Transferring one fixed success event yields the radius and failure buffers in the theorem.

The exact checker reconstructs the complete scalar ternary grid and all classical strings. It does not accept a prefix as a certificate. The executed example is a valid instance of the theorem, but it is not execution of the general matrix learner.

---

## 4. Relation to the inherited binary theory

Revision 82 does not replace the complete binary effect-body results. Those results cover all spectral boundary strata and have a different anisotropic metric and logarithmic entropy. The new multi-outcome theorem imposes a uniform positive spectral margin and obtains a simpler affine geometry.

This distinction must remain explicit:

- binary full-body geometry is global but has unresolved growing-dimensional learning gaps;
- finite-outcome geometry is dimension sharp for fixed `k` but only on a balanced interior;
- no theorem presently treats the complete multi-outcome boundary with matching entropy and minimax learning;
- no theorem presently closes the growing-`k` query complexity.

The two theories are complementary rather than one being a formal corollary of the other.

---

## 5. Priority and literature assessment

### 5.1 Mele–Bittel

The current primary version of Mele–Bittel gives essentially optimal channel learning in diamond distance and includes finite-output measurement channels in its general scope. Its binary POVM operator-norm result is the upper primitive inherited by this manuscript.

The v82 contributions not supplied by that source are the future-`N` path metric, the balanced-tuple horizontal comparison, the coherent-adaptive minimax lower under that loss, the exact affine description order, and the finite certificate transfer. The paper should continue to describe its learner as a reduction using an existing tomography primitive, not as the first multi-outcome POVM learner.

### 5.2 Zambrano–Ramos-Calderer–Kueng

Their projected least-squares protocol gives optimal sample complexity in dimension and number of outcomes for nonadaptive single-copy measurement tomography under their worst- and average-case distances. Their access model, loss, and lower-bound class differ from the present independent Choi acquisition with collective final processing and from the arbitrary-coherent-adaptive lower theorem.

A direct substitution at component accuracy of order `delta/(k sqrt(N))` supplies a meaningful sufficient future-loss comparison. This should remain in the main article, not only in an audit file.

### 5.3 What remains genuinely open

The targeted literature check did not identify a prior theorem identical to the combined v82 package. That is not an exhaustive priority clearance. The following remain necessary before strong novelty language is justified:

- an independent expert comparison with finite-outcome channel/POVM learning;
- a comparison with adaptive and collective tomography lower bounds beyond the two sources above;
- clarification of whether the horizontal normalized-tuple lift has appeared in finite-use measurement discrimination or multiparameter channel-extension form;
- a sharper account of which parts are standard affine geometry and which part is the new operational synthesis.

---

## 6. Why the four-leading-journal threshold is not met

### 6.1 The main generalization is interior and fixed-alphabet

The new theorem is uniform in dimension and horizon, but it assumes every outcome effect stays between fixed multiples of `I/k`. Multi-outcome spectral boundary strata, vanishing effects, changing ranks, and coupled support geometry are excluded. These are precisely where the binary theory was most distinctive.

### 6.2 Growing outcome count is unresolved

The affine dimension grows linearly in `k`, and the description entropy records that growth. The statistical lower bound, however, comes from one embedded binary subfamily and has no corresponding growing-`k` term. The constructive upper pays `k^3`. Fixed-`k` sharpness is mathematically legitimate, but it is not a complete multi-outcome minimax law.

### 6.3 The methods are a substantial synthesis of known tools

Horizontal Kraus gauges, purification, path integration, Bernoulli witnesses, volume packing, confidence amplification, binary tomography, rational inward rounding, and finite-net transfer are established ingredients. Their normalized tuple synthesis is nontrivial and appears useful, but the manuscript does not yet demonstrate a broad new principle extending beyond this interface.

### 6.4 Computational efficiency is not addressed

The public code, tuple legalization, and readout certificate are finite and exact. They may require exhaustive enumeration of enormous grids, dictionaries, classical strings, and conditional POVMs. The theorem carefully separates these costs, but the lack of an efficient construction narrows the practical and computational impact.

### 6.5 The journal-facing article is still accretive

The 81-page quantitative article contains the complete binary boundary theory, several generations of learners and codes, finite-control machinery, confidence-optimal interior results, finite-risk certificates, and the new multi-outcome extension. The complete research edition is an excellent archive; it should not determine the architecture of a journal submission.

### 6.6 No external major problem is resolved

The work advances its own realization/measurement programme substantially. I do not see a consequence settling a broadly recognized open problem outside that programme at a level commensurate with the four leading general mathematics journals.

### 6.7 Independent priority remains open

The repository itself correctly marks independent human priority clearance as false. CI, exact tests, internal audits, and this referee-style report cannot substitute for specialist judgment across quantum tomography, channel learning, and finite-use discrimination.

---

## 7. Scope and resource limitations

1. The device is memoryless, input consuming, and classical output. It returns no residual device quantum system.
2. Outcomes are ordered; quotienting by outcome relabeling is not studied.
3. The finite-outcome sharp law is for a balanced interior and fixed `k`.
4. The upper learner uses independent one-call probe–reference pairs, although completed outputs may be processed collectively.
5. The lower learner permits coherent adaptive training and bounded public stopping.
6. Unknown-device calls, future horizon, transmitted bits, readout storage, dictionary reconstruction, workspace, trusted controls, and physical execution are separate resources.
7. The exact dictionary and certificate are finite but not efficient.
8. The executed certificate is scalar and ternary; higher-dimensional tests verify local identities only.
9. The structural companion's repeatable-probe model remains logically separate.
10. None of the measurement theorems closes a gate in the independent A/B/C/D analytic programme.

---

## 8. Required revisions before specialist submission

1. **Separate the journal objects.** Submit the quantitative measurement paper and the structural stochastic-realization paper separately. The 220-page complete edition should remain archival.
2. **Obtain independent human priority review.** This remains the most important nonmathematical gate from r51.
3. **Put the finite-outcome theorem first.** The new result is now the best entry point. Move much of the inherited binary implementation history to appendices or companion material.
4. **State “balanced interior” in every finite-outcome headline.** Do not allow the title or abstract to suggest a complete POVM-body theorem.
5. **State “fixed outcome count” in every minimax sharpness claim.** The `k^3` upper and `k`-independent lower leave growing-`k` optimality open.
6. **Expand the direct tomography comparison.** Give theorem-level parameter substitutions for Mele–Bittel and Zambrano–Ramos-Calderer–Kueng in the main text.
7. **Separate pairwise geometry from common learning.** The eigenvector witness is a lower-bound experiment and is not available to the estimator.
8. **Keep the actual operational metric in the coding converse.** Do not replace it by an unproved surrogate triangle inequality.
9. **Preserve every-record and stopping quantifiers.** They materially strengthen the lower theorem.
10. **Keep public dictionaries honest.** Reconstruction cost and public parameters are not transmitted payload, but target-dependent private advice would have to be charged.
11. **Clarify the finite-control guarantee.** The ideal certificate and actual-control learner have different hypotheses and error ledgers.
12. **Do not advertise the scalar replay as execution of the general learner.** Its role is exact theorem instantiation and software regression.
13. **Report exact ranges next to theorem summaries.** In particular, distinguish geometry, entropy, learning, rational synthesis, and certificate ranges.
14. **Reduce historical revision language in the article.** Provenance belongs in the repository package, not in the mathematical narrative.
15. **Retain the full multi-outcome boundary and growing-`k` questions as explicit open problems.** They are the clearest next mathematical directions.

---

## 9. Detailed comments

1. In the horizontal ODE proof, retain the order `H A^{-1} H`; a commuting shorthand would be misleading.
2. State explicitly that the duplicate label in the dilation is environmental and unavailable to the device user.
3. The stopping reduction should continue to say that the original stopped output is a common postprocessing of the padded experiment.
4. The lower witness may be chosen separately for every pair; this should not be described as one common design.
5. In the entropy theorem, emphasize that arbitrary legal centres still satisfy the lower component witness.
6. The phrase “exactly the closed `r`-ball” depends on working inside `sum_j H_j=0`; keep the affine subspace in the sentence.
7. In the grid lemma, record the coordinate-rounding convention and the dependent final effect before invoking legality.
8. The strict greedy separation and closed assignment tests are intentionally different; retain both equality conventions.
9. The real-input encoder requires certified approximations. Do not state an algorithm for an unrepresented arbitrary real tuple.
10. The public dictionary may be target independent but enormous. Avoid the word “explicit” when it might be read as efficient.
11. The component learners use fresh unknown-device calls for different outcomes. The upper budget should continue to charge their sum.
12. The `3/4,1/4` relabeling is exact only because all original outcomes are retained in the classical postprocessing; keep the instrument-level explanation.
13. On bad learning records, the fallback must remain defined before the finite search is invoked.
14. The final `5delta/8` good-event error is stronger than the advertised `delta`; this useful slack should remain visible.
15. In the odd-`k` lower reduction, retain the subnormalized-reference calculation for the erased branch.
16. The coarse-graining step is a channel postprocessing and therefore contracts the actual operational distance; say this rather than appealing only to outcome probabilities.
17. Spectral clipping uses Weyl plus a triangle inequality. It is not an operator-Lipschitz theorem.
18. The lower confidence theorem is invoked on the binary interior after clipping; cite the exact inherited label and range at the invocation.
19. The fixed-length description converse needs success probability strictly greater than zero at every target, not merely average success over a prior.
20. In the certificate theorem, the good-label set is fixed at the nearby grid point before probability transfer. This is the essential logical point.
21. The factor `1/2` between trace norm and total variation should remain explicit in the certificate ledger.
22. Exact finite verification requires the complete tuple net and every classical string. A cutoff or prefix is not a certificate.
23. A separately certified implementation-law error must be added to the ideal certificate's failure allowance.
24. The finite matrix tests do not verify the universal ODE theorem; they only pin exact identities and regression cases.
25. Current commits are unsigned. Reproduction verifies bytes, not human authorship.
26. The structural companion is unchanged and should not be used to inflate the novelty of the measurement theorem.
27. The full-body binary `d^4` learning upper remains unmatched in growing dimension; v82 does not close it.
28. The multi-outcome entropy is sharp in affine dimension, while the statistical query theorem is only fixed-`k` sharp. These are different optimality statements.
29. The direct comparison with nonadaptive single-copy POVM tomography should state both the access restriction and the loss conversion.
30. The paper's strongest specialist message is the combination of future-use operational geometry, coherent-adaptive converse, public description entropy, and fixed-`k` learning—not the existence of POVM tomography itself.

---

## 10. Reproducibility and evidentiary status

The source-bound workflow committed the native source, built all three manuscripts, ran twenty regression suites under ordinary and optimized Python, reconstructed the complete source and standalone journal package, and verified the publication head. The separate exact-head workflow checked out `57937576...` read-only and verified ancestry, manuscripts, regressions, and the journal package.

The build receipt records:

- 81 pages for the focused article;
- 41 pages for the structural companion;
- 220 pages for the complete edition;
- 465 source files;
- 438 preserved predecessor native files;
- 800 preserved complete-edition labels;
- 302 preserved focused labels;
- 116 preserved structural labels;
- twenty regression suites;
- normal/optimized identity;
- an isolated native rebuild; and
- a standalone journal rebuild.

The finite-outcome suite reports 88 positive checks, 11 negative controls, noncommuting `d=2,k=3` identities, and one complete scalar ternary certificate with 3169 legal grid points and nine strings. It explicitly reports that no physical learner and no general matrix-grid certificate were executed.

These are strong source and regression practices. They are not formal proof verification, an independent priority opinion, or experimental implementation of the general learner.

---

## 11. Repository-wide pipeline assessment

The independent analytic chains remain

```text
A1 independent;
A2 -> A3 -> A4 -> C2 -> D1;
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

The unresolved obligations include raw unsmoothed local limits, stopped-path recovery, a global past kernel, exact shell conditioning, process CLT and Mosco recovery, nonlinear Nisio graph cores, filtering/QMD/LAN, changing-filtration response, and labelled posterior contraction.

The finite-dimensional POVM geometry, learning, code, and certificate theorems do not imply any of those analytic gates. All five aggregate flags correctly remain false:

```text
historical A2 replacement: false
B4 aggregate: false
C2 aggregate: false
eleven-paper aggregate: false
whole Theta programme: false
```

The local paper must therefore be judged on its own theorem package. The wider repository neither weakens its correctness nor increases its journal significance.

---

## 12. Final assessment

Revision 82 successfully answers the most important scope objection in r51 within a substantial domain. It moves from ordered binary effects to noncommuting ordered `k`-outcome POVMs on a full-dimensional balanced interior. The finite-use geometry, affine entropy, fixed-`k` minimax learner, exact code, and finite certificate form a coherent theorem package. I did not find a fatal correctness defect in the new proof chain.

The work has reached a level at which further value will come from sharper positioning and selected new mathematics, not another cumulative rewrite. The clearest open directions are:

- the complete multi-outcome boundary;
- sharp growing-`k` learning;
- efficient or complexity-controlled legalization and coding;
- a more general principle behind the normalized horizontal lift; and
- an external application beyond the manuscript's own measurement-resource programme.

For the four leading general mathematics journals, the balanced-interior/fixed-`k` scope, unresolved `k` dependence, reliance on established tomography primitives, exhaustive computational constructions, accretive article architecture, and open priority boundary remain decisive.

**Recommendation: reject at the Annals / Inventiones / JAMS / Acta level; encourage separate specialist submission after independent priority review and editorial compression.**
