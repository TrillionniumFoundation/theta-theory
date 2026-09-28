# Referee Report — General Theta Foundations I, Revision 61 (r40)

**Quantitative manuscript:** *Spectral Entropy and Sharp Stochastic Widths of Compact Group Experiments*  
**Structural manuscript:** *Finite Physical Actions and Repeatable Observation Processes*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v61-sharp-width-2026-09-28`
- `revision/general-theta-foundations-i-v61-referee-ready-2026-09-28`

**Reviewed final head:** `2c215579336a253585499328f19a647446445dc4`  
**Candidate publication:** `36a75595e46da636bd967b0d30f6395fdc05d029`  
**Qualified native source:** `776ba0fec6ec7ddd57a5fc188764763700cd5008`  
**Source predecessor:** Revision 59 final head `310dabfa4020a7c4da2d7999c59ea692dede7850`  
**Controlling located reports:** Revision 58 r39 report `6daa50db42873a4a32cd3c1610f19630f5739b51` and proof/pipeline audit `849cbc2fb4d589d8fd13d8c7d34492af191e0f75`  
**Final-head verification:** Actions run `36378669691`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v61-external-referee-r40-2026-09-28`  
**Date:** 28 September 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is again **not a correctness rejection**. Revision 61 is materially stronger than Revision 58. The principal quantitative objection in r39—the logarithmic loss in the nonabelian converse—has been answered by a genuinely different argument rather than by a change of notation. The new entropy--transport proof yields an occupation bound of order `k^(2/p)` under a full action spectral gap and an all-direction cap bound, with arbitrary intervening widths. It therefore gives matching polynomial powers whenever the least unit-orbit dimension and target-orbit dimension agree. The qubit density-matrix law becomes `Theta(N^(d-1))` at every fixed positive subcritical error. A second explicit rational Bloch experiment imports the classical LPS norm `sqrt(5)/3`, producing fully numerical linear-width bounds, while retaining an exact profile `5^t` stable up to error `25^(-N)/16`.

Revision 59 also contributed a separate causal theorem for repeatable classical probes: bounded whole-transcript width below total-variation error one is equivalent to finiteness of a future-response quotient and to an exact stationary finite physical action; below error one half, the quotient cardinality is the eventual minimum. I did not find a fatal gap in that inherited chain either.

The top-four disposition nevertheless remains negative. The paper studies a specialized nonuniform label-width resource in which the horizon, external clock, horizon-dependent real tables, their construction and lookup, exact arithmetic, and exact sampling remain outside the invariant. The sharp quantitative theorem requires a full Koopman/action `L^2` spectral gap, not merely contraction of the advertised finite-dimensional representation, and it uses a physical identity letter or an exact-return substitute. The causal classification relies on repeatable, nondisturbing fresh probes—an oracle-like classical observation model, not a general partially observed or irreversible system and not repeated quantum measurement. The leading constants and joint error/horizon crossover remain open. Most importantly for a four-leading-journal decision, the precise theorem-level priority boundary across positive realization, compact stochastic semigroups, probabilistic and weighted automata, controlled hidden-state realization, quantization, and entropy methods has still not been independently settled. The manuscript itself correctly describes its literature audit as author-side and incomplete.

**Disposition outside the four leading general journals:** the focused quantitative manuscript is now a substantial specialist contribution, and the structural manuscript contains a coherent specialist-level theorem package. I would encourage separate submissions to strong specialist venues after an independent priority review and editorial compression. I would not request another wholesale mathematical reconstruction.

---

## 1. Scope, genealogy, and material reviewed

The two Revision 61 branches are identical at `2c215579...`. No higher `General Theta Foundations I` revision was present in the branch survey used for this report. The final head is a direct successor of the candidate publication and changes only the final-head request record. The candidate publication is a direct successor of the qualified native source.

The stated predecessor is the completed Revision 59 final head, not Revision 58 and not the abandoned Revision 60 preparation anchor. No separate Revision 59 referee report was located. I therefore independently reviewed the new Revision 59 causal material needed to assess Revision 61, rather than treating its presence in a preservation tree as an external certification.

I reviewed, in particular:

- `quantitative.tex`, `structural.tex`, and the complete research edition;
- `sections/25-spectral-entropy.tex`;
- `sections/26-effective-sphere.tex`;
- the retained least-orbit and rational-endpoint proofs from Revision 58;
- `sections/23-causal-process.tex`;
- `sections/24-adaptive-compiler.tex`;
- the inherited stationarization, purification, finite-action, quotient-radius, and phase chains;
- `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `RESPONSE_TO_REFEREE.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the generic compiler, exact regression program, build script, and final-head verifier;
- the source-bound build receipt and preservation manifests; and
- the exact-head read-only Actions run.

I also checked the primary LPS restatement used for the explicit norm. For the norm-five six-rotation set, the cited theorem gives the one-step Koopman discrepancy

```text
2 sqrt(p)/(p+1),
```

and hence exactly `sqrt(5)/3` at `p=5`. This constant is therefore a legitimate imported theorem, not an extrapolation from finite harmonics or numerical experiments.

This report is not a formal proof-assistant verification and not an exhaustive independent novelty search. Where the priority boundary remains open, I treat that as an editorial limitation rather than pretending that repository ancestry settles it.

---

## 2. Executive assessment of the new mathematics

### 2.1 The entropy potential

The pointwise block proof in the earlier manuscript paid an `O(log k)` mixing cost at every selected narrow cut. Revision 61 instead attaches relative entropy to a compactly supported smoothing of the probability law of conditional-centroid directions, weighted by hidden-label mass times centroid norm. A full action spectral gap forces a fixed entropy drop whenever the smoothed law is supported in at most `k` sufficiently small caps. The cost of moving from one directional law to the next is bounded by the loss of total centroid mass. Summing over selected cuts produces one additive initial entropy range and a square-root transport budget, rather than a repeated mixing-time factor.

This is the conceptual center of the revision. It is a real change of method and not merely a constant improvement.

### 2.2 Sharp occupation and width powers

For cap exponent `p`, fixed subcritical residual amplitude `zeta>0`, and full action spectral contraction `kappa<1`, the theorem proves

```text
# { positive cuts of width <= k } = O_zeta(k^(2/p)).
```

Consequently, a horizon-wide width bound satisfies

```text
W_(N,epsilon) >= c_zeta N^(p/2).
```

The previously established quadratic inner-orbit-hull construction gives an upper law of order `N^(q/2)`, where `q` is the target-orbit dimension. When the least orbit dimension `p_*` equals `q`, the powers match. For conjugation on legal `d x d` density matrices, this gives `Theta(N^(d-1))` at every fixed positive subcritical error.

### 2.3 The effective LPS experiment

The new rational Bloch rotations are the adjoint actions of the six norm-five Lipschitz quaternions. The exact LPS norm supplies a numerical full-action spectral constant. The theorem obtains the explicit, deliberately conservative bounds

```text
(1-sqrt(2) epsilon) N / 6500
    <= W_(N,epsilon)
    <= 52 + 104 N/epsilon
```

for `0<epsilon<1/sqrt(2)`.

The same experiment has exact cut profile `5^t`. The seed stabilizer is the cyclic subgroup generated by one free generator, so the orbit is a right-coset ball rather than the whole free-group ball. The exact profile persists through `epsilon <= 25^(-N)/16` by a denominator-five lattice separation argument.

### 2.4 Causal finite-label classification

For compact-group experiments with repeatable fresh probes, the inherited Revision 59 theorem identifies bounded whole-transcript width at every fixed error below one with a finite future-response quotient, an open-normal finite physical quotient, and an exact stationary causal realization. The converse uses one common separating itinerary and repeated probes to create disjoint statistical events, then applies a nonnegative-mixture bound across a finite cut register. It allows adaptive policies and arbitrary intervening widths.

This is logically distinct from terminal numerical realization. Correct one-time means do not produce a correct path law, and the manuscript does not use terminal purification as a substitute for a causal instrument.

### 2.5 Constructive causal approximation

For rational rotations, a rational unit seed, and strictly positive rational affine probes, the generic compiler constructs a causal machine with whole-transcript total-variation error `epsilon` and width `O(N^2/epsilon^2)`. The proof couples the physical and hidden geometric trajectories, controls probe-law KL divergence along the entire adaptive path, and then rounds the actual joint emission/transition kernels to dyadic probabilities.

---

## 3. Correctness audit: spectral entropy

### 3.1 The required spectral hypothesis

The new argument correctly uses a bound on the full Koopman action on `L^2(Sigma)`, off all invariant functions:

```text
||P f - Pi f||_2 <= kappa ||f - Pi f||_2.
```

This is stronger than contraction on the finite-dimensional representation `E`. The manuscript explicitly gives circle actions as an obstruction to confusing the two: high harmonics can remain nearly invariant although the first harmonic contracts. For a compact group, a regular-representation spectral bound does transfer to every nontrivial irreducible block occurring in the action, while `Pi` retains all trivial summands in a nontransitive action. This use is correct.

### 3.2 Compactly supported spherical smoothing

The kernel

```text
K_h(u,x) = Z_h^(-1) (1-||x-u||^2/h^2)_+^2
```

has the necessary `C^1` boundary behavior. The proof obtains:

- pointwise density bound of order `h^{-(m-1)}`;
- entropy range `0 <= H <= log(D_m h^{-(m-1)})`;
- Fisher information of order `h^(-2)`; and
- entropy Lipschitz continuity under quadratic Wasserstein transport of the centers.

The moving-center interpolation is legitimate. Rotation invariance gives the continuity equation; the mixture flux satisfies the required kinetic-energy bound by pointwise Cauchy--Schwarz. Regularization by adding a positive constant justifies entropy differentiation at common zeros. I found no hidden positivity assumption on the unsmoothed directional law.

For `S^2`, the direct constants are also correct: chordal squared distance is uniform on `[0,4]` under normalized area, giving `Z_h=h^2/12` and Fisher information `24/h^2-4`.

### 3.3 Fixed entropy loss on thin support

For a density supported in `A`, orbital Cauchy--Schwarz gives

```text
(Pi sqrt(f))^2 <= (Pi 1_A)(Pi f).
```

If `Pi 1_A <= theta`, the invariant part of `sqrt(f)` has squared norm at most `theta`. The full action gap contracts the orthogonal part. The pointwise relative-entropy/Hellinger inequality then yields

```text
H(f)-H(Pf) >= (1-kappa^2)(1-theta).
```

This step does not require a logarithmic Sobolev inequality, pointwise mixing, transitivity, or a positive lower bound for `f`. The treatment of nontransitive actions through `Pi`, rather than projection only onto global constants, is essential and correct.

### 3.4 Centroid-loss transport

Let `c_s=E[X|S=s]`, and weight direction `c_s/||c_s||` by `p_s||c_s||`. After one random physical letter and any identity-product hidden processing, the exact flow identity is

```text
sum w_(s,a,i) ||u_(s,a)-v_i||^2 = 2(q_i-m_i).
```

It implies monotonicity of total centroid mass and provides a coupling from the rotated old direction law to a law supported on the new directions. The excess scalar mass is transported separately. Converting chordal to geodesic distance gives

```text
W_2(lambda*nu,nu')^2 <= 3 pi^2 (alpha-alpha')/zeta.
```

Zero centroids and arbitrarily small label masses are harmless because the directional law is weighted by centroid mass and zero terms are omitted. I find this lemma correct.

### 3.5 Telescoping across narrow cuts

The external word distribution is chosen from the advertised width profile, not from private machine state. In each gap between selected narrow cuts it inserts one independent physical letter with law `lambda` and fills the remaining positions with the identity command. Hidden rows on the identity command may perform arbitrary processing.

Wordwise terminal correctness and legal decoder norm at most one imply residual centroid mass at least `zeta`. Centroid mass cannot increase along gaps or the fixed suffix, so total lost mass is at most `1-zeta`.

At every narrow cut, the smoothed direction density lies in at most `k` caps. The all-direction cap bound makes their orbitwise occupancy at most one half. Thus each gap incurs a fixed entropy defect, while the entropy restoration needed to reach the next directional law is at most a constant times `sqrt(delta_j)/h`. Summation and Cauchy--Schwarz give

```text
gamma M <= L_h + C h^(-1) sqrt(M(1-zeta)/zeta).
```

Young's inequality yields `M=O(h^(-2))`; with `h~k^(-1/p)` this is `O(k^(2/p))`. The logarithmic entropy range remains only an additive term and is absorbed by the power. The endpoint `zeta=1` correctly reverts to an exponential obstruction rather than a positive-error polynomial upper law.

I did not find a missing independence, stationarity, positive-mass, or bounded-intervening-width assumption in this proof.

### 3.6 Limits of the theorem

The sharp theorem does **not** cover an arbitrary command alphabet. It requires a physical identity letter, or in the stated extension exact identity-product words at all sufficiently large lengths. Approximate returns with accuracy-dependent thresholds are not included in this quantitative argument. It also requires the full action gap and an all-direction cap estimate for the fixed representation. These are substantive hypotheses and should remain in every headline statement.

---

## 4. Correctness audit: the effective sphere

### 4.1 Identification of the LPS set

At `p=5`, the norm-five Lipschitz quaternions with positive odd scalar coordinate are exactly

```text
1 +/- 2i,  1 +/- 2j,  1 +/- 2k.
```

Their adjoint actions are the six displayed rational rotations. The cited primary restatement gives the exact one-step `L^2_0(S^2)` norm `2 sqrt(p)/(p+1)`, hence `sqrt(5)/3`. The manuscript correctly treats the automorphic/Deligne input as imported deep mathematics.

The direct density check is also adequate. Each generator has rotation cosine `-3/5`, so its angle is not a rational multiple of `2pi`; its powers are dense in the corresponding coordinate-axis circle. The three axis circles generate `SO(3)`.

### 4.2 Numerical occupation constants

A chordal cap of radius `h<=1` on normalized `S^2` has area `h^2/4`. Taking `h=k^(-1/2)` gives `theta=1/4`. With `kappa^2=5/9`, the entropy defect is `gamma=1/3`. Using `D_3=12` and `B_3=24` produces

```text
1 + 6 log(12k) + 648 pi^2 ((1-zeta)/zeta) k.
```

The subsequent coarse bound by `6500 k/zeta` is numerically valid. No hidden numerical Bourgain--Gamburd constant is imported into this example.

### 4.3 Exact coset profile

The three projective rotations freely generate a rank-three free group. The stabilizer of the first-axis seed is exactly the cyclic subgroup generated by the first rotation: any rotation fixing the axis commutes with that generator, and the centralizer of a primitive free generator is its cyclic subgroup.

Every right coset has a unique shortest reduced representative with no terminal first-generator letter. There are `4*5^(ell-1)` such representatives of positive length `ell`, so the coset ball of radius `t` has cardinality

```text
1 + 4 sum_(ell=1)^t 5^(ell-1) = 5^t.
```

Identity padding makes this the set reachable at command length `t`. The extreme-output theorem therefore gives the simultaneous exact profile at all cuts.

### 4.4 Robust profile

Products of the rational rotations applied to the rational seed lie in `5^(-t) Z^3`. Distinct cut targets are therefore separated by at least `5^(-t)`. A fixed suffix preserves distance. The same decoder-cap argument used in Revision 58 shows that error at most `25^(-N)/16` yields disjoint positive-mass decoder caps at every cut. The constant is conservative and correct.

### 4.5 Constructive upper law

The generic rational compiler applies to the seven-letter Bloch list. Choosing amplitude `1-epsilon/2` and `m^2>=2N/epsilon` gives at most `52+52N/epsilon` exact-amplitude labels. The stated dyadic precision adds a smaller error budget, and passing through a rational tolerance between `epsilon/2` and `epsilon` justifies the looser real-tolerance bound `52+104N/epsilon`.

The output is a classical hidden-label machine with a numerical density-matrix decoder. It is not a quantum-state preparation procedure.

---

## 5. Correctness audit: causal processes

### 5.1 Future-response quotient

The future-response function

```text
Theta_(s,g)(x,j)=p_(s,j)(xg)
```

is the correct behavioral object for left command updates. Equality of types is preserved and reflected under common future commands. If the type set is finite, the compact group acts continuously on this finite set; the kernel is open and normal. Evaluation at the identity shows that probe laws are constant on its cosets. Conversely, those types themselves form the exact stationary causal labels.

### 5.2 One common separating itinerary

For finitely many distinct types, the proof does not use incompatible pair-specific terminal suffixes. It processes all pairs sequentially. Distinctness survives each common command prefix. At the chosen physical state, one probe coordinate separates the current pair. Repeating the probe at each recorded location gives empirical-frequency events that are simultaneously disjoint and have arbitrarily high probability under their corresponding types.

This is a sound use of repeatability. The probes leave the physical state fixed and emit fresh classical draws.

### 5.3 Testing across a finite cut register

After marginalizing prefix outputs, causality makes the fixed suffix law depend only on the cut label. If target type `i` assigns at least `1-delta` to event `A_i`, transcript TV error `epsilon` gives approximate probability at least `1-delta-epsilon`. Summing over the disjoint events gives

```text
|S_t| >= m(1-delta-epsilon).
```

When the success probability exceeds one half, each type requires a distinct label whose suffix law places probability greater than one half on its event. This gives the exact cardinality lower bound below error one half.

The proof does not condition on a rare observed prefix and does not assume a per-step error budget.

### 5.4 Scope

The theorem is strong inside its declared oracle model, but the model is not a general HMM/POMDP or quantum-measurement classification. Repeatable probes are fresh nondisturbing observations of the same classical physical state. Without them, the common testing continuation and its padding mechanism may fail. The manuscript states this, but the limitation remains central to significance.

---

## 6. Correctness audit: the adaptive compiler

The auxiliary law uses the true physical state for probe emissions and the constructed hidden net only for hidden transitions; its public marginal is exactly the target experiment under every adaptive policy. The physical and hidden controls are coupled through the same observed transcript.

The rotation-row mean identity gives the unconditional recursion

```text
E ||V_t-X_t||^2 <= 2t/m^2,
```

without a posterior bound after rare observations. Strict positivity of every affine probe law provides an elementary conditional KL bound. The trajectory chain rule cancels the common policy and transition kernels, and summing over probe times gives total KL of order `N^2/m^2`. Pinsker supplies half the error budget.

Dyadic rounding is applied to the actual joint emission/transition rows. Coupling the two adaptive processes until their first discrepancy bounds the additional whole-transcript error by the sum of one-step TV errors. The width and fair-bit estimates follow.

The algorithm is polynomial in the numerical horizon and inverse accuracy and in the explicitly enumerated net size; it is not polynomial in the binary length of the horizon and is not a minimum-width algorithm.

---

## 7. Reproducibility and source identity

Revision 61 materially improves the evidentiary architecture criticized in r39.

The final reviewed head `2c215579...` triggered a separate workflow with `contents: read`, checkout credentials disabled, and the exact triggering SHA checked out. The verifier confirms:

- the direct source -> publication -> final-request genealogy;
- source hashes against both the checkout and the native archive;
- committed PDF digests;
- compiler example digests;
- exact finite regression results;
- all page text and raster comparisons under a native-only rebuild; and
- absence of tracked repository modifications by the verifier.

The Actions run completed successfully. This is credible final-head reproducibility evidence. It remains distinct from mathematical proof, independent novelty assessment, a cryptographic author signature, or editorial acceptance.

The package still contains far more historical evidence than a normal referee needs. For journal submission, a minimal source archive, the two focused PDFs, the response, and a short reproducibility manifest would be preferable to exposing the entire preservation stack as part of the submission narrative.

---

## 8. Novelty and priority

Revision 61 makes a plausible new combination of ideas:

1. a mass-weighted law of conditional-centroid directions;
2. compactly supported spherical entropy smoothing;
3. a full-action spectral entropy defect on thin orbital support;
4. a Wasserstein transport cost paid by loss of centroid mass; and
5. an all-profile occupation argument for horizon-specific stochastic realizations with unrestricted intervening widths.

The manuscript correctly does not claim novelty for Wasserstein continuity of entropy, Fisher-information convexity, Hellinger inequalities, LPS expansion, homogeneous-orbit covering, or compact stochastic-semigroup structure.

The difficulty is that the closest theorem-level boundary remains incompletely surveyed. A top-four recommendation would require independent expert comparison with, at minimum:

- positive and nonnegative realization with approximate vector outputs;
- controlled hidden Markov and predictive-state realization;
- quantization and rate-distortion of compact group actions;
- entropy-dissipation arguments for finite-memory filters;
- probabilistic and weighted automata with advice or horizon dependence;
- compact stochastic semigroups and recurrent-simplex reductions; and
- behavioral/minimal causal-state constructions under repeated testing.

The existing audit is thoughtful, but it expressly does not exclude equivalent formulations in these literatures. That is acceptable for a specialist submission accompanied by normal peer review. It is not enough to carry a paper into the four leading general journals.

---

## 9. Why the four-leading-journal threshold is still not met

### 9.1 The invariant is specialized

The theorem counts persistent hidden labels while leaving the horizon, clock, full real table descriptions, table construction, exact arithmetic, and exact atomic sampling uncharged. This makes the lower bounds mathematically strong within the model, but it prevents a direct interpretation as ordinary memory, workspace, or algorithmic state complexity.

### 9.2 Sharpness is conditional on a strong global gap

The new lower power is sharp under a full `L^2` action spectral gap and an all-direction cap law. Many natural compact actions do not satisfy this gap for a given finite alphabet. Contraction of the physical representation alone is insufficient. The theorem therefore does not provide a universal sharp-width law for compact group experiments.

### 9.3 Synchronization remains substantive

The quantitative proof uses a physical identity command or exact identity words of all sufficiently large lengths. The terminal structural theorem uses eventual approximate returns. Neither result is an arbitrary-clock-removal theorem for general alphabets or irreversible semigroups.

### 9.4 The causal model uses repeatable oracle probes

The process theorem is not a general classification of finite hidden-state approximations to controlled stochastic processes. Its repeatable fresh probes are precisely what amplify distinct response types into disjoint events and what provides physical holds. This is mathematically legitimate but narrows the scope.

### 9.5 Important quantitative questions remain

The paper does not determine optimal leading constants, the full joint `N`--`epsilon` crossover, matching powers for every representation with `p_*<q`, or a sharp exponent for the causal process model. The older rational-unitary example still has a non-effective Bourgain--Gamburd constant.

### 9.6 No external major problem is resolved

The revision resolves important internal objections in the manuscript's development: the logarithmic loss, explicit spectral constants for one alphabet, and the terminal/process distinction. I do not see a consequence settling a widely recognized open problem outside this realization framework.

### 9.7 The wider Theta program remains open

The spherical entropy potential is unrelated to the stopped-path entropy/LDP gate in the independent analytic pipeline. It supplies no raw local limit, stopped LDP, global past kernel, Mosco/Nisio core, filtering/LAN theorem, changing-filtration response, or labelled posterior-contraction result. Every aggregate A/B/C/D completion flag correctly remains false.

---

## 10. Required changes before specialist submission

1. **Submit the quantitative and structural manuscripts separately.** The complete 76-page research edition should remain archival rather than being treated as a third submission object.

2. **Commission an independent priority review.** The author-side audit should be supplemented by theorem-level comparison from experts in positive realization/automata and controlled stochastic processes.

3. **State the full action gap in every sharp-width headline.** A reader must not infer that a matrix spectral radius or first-harmonic gap is sufficient.

4. **Keep the synchronization hypothesis visible.** The identity-letter and exact-return variants should not be blended with approximate terminal stationarization.

5. **Keep the resource convention on page one.** In particular, the entropy density is only a proof potential, while the clock and real tables remain uncharged by definition.

6. **Separate the two explicit alphabets.** The old rational-unitary pair has a non-effective Bourgain--Gamburd constant; the new rational Bloch action has the LPS constant. They should never be conflated in summaries.

7. **Maintain the exact/robust/fixed-error distinction.** The intervals `625^(-N)/16` and `25^(-N)/16` shrink with the horizon and do not give exponential width at one fixed positive error.

8. **Frame the causal theorem as a repeatable-probe theorem.** It should not be advertised as a general HMM, POMDP, irreversible-process, or quantum-measurement classification.

9. **Reduce the journal-facing evidence bundle.** Preserve the full archive in the repository, but give referees a minimal source and reproduction manifest.

10. **Do not use repository-wide pipeline volume as significance evidence.** The local theorem packages must stand independently, and the A/B/C/D program remains open.

---

## 11. Detailed comments

1. In the spectral-entropy section, the projection `Pi` should remain defined as projection onto all invariant functions, not only constants. This matters for nontransitive actions.

2. The implication from a regular-representation gap to the action gap should retain the inverse/adjoint convention explicitly.

3. The kernel's compact support and zeros are not cosmetic. The regularization argument should remain in the submitted proof.

4. The entropy potential is relative entropy against normalized round measure, not Shannon entropy of the hidden register. This distinction belongs in the introduction.

5. The directional-law weights are `p_s ||c_s||`, not `p_s`. Using hidden-label probabilities alone would invalidate the transport accounting.

6. The proof uses only conditional mean correctness after averaging deterministic words. It never proves that an individual hidden label approximates the physical target.

7. The external word distribution may depend on advertised widths but not on private state. This quantifier should remain explicit.

8. The identity command may carry arbitrary hidden processing. No hidden identity row is assumed.

9. The additive logarithmic entropy range is still present; what is removed is its multiplication by the mixing-block cost. The wording “removes the logarithmic loss” is acceptable for the final width power, but the proof-level distinction should remain visible.

10. At exact amplitude and zero error, the matching polynomial corollary does not apply. The entropy budget instead permits the exponential obstruction.

11. The LPS theorem supplies the Koopman norm for the six nonidentity rotations. The physical identity used for padding is not part of that uniform spectral measure.

12. The rational Bloch matrices are the finite input; their unitary lifts are algebraic, not rational. The paper states this correctly.

13. The `5^t` count is a coset-ball count, not a free-group ball count. The cyclic stabilizer proof is therefore essential.

14. The stabilizer is for the vector `e_1`, not merely its unoriented axis. Powers of the first rotation fix the vector, and no additional free-group element does.

15. The numerical constant `6500` is a safe explicit constant, not a claimed optimum.

16. The causal theorem's threshold one is a boundedness threshold because TV is at most one. The exact minimum formula is asserted only below one half.

17. The common itinerary must remain one itinerary for all types, not pair-dependent incompatible continuations.

18. The testing lemma correctly marginalizes prefix outputs and avoids conditional correctness after a rare transcript. This is one of the strongest parts of the causal proof.

19. The adaptive compiler's auxiliary law is a proof coupling, not a realizable machine available to the algorithm.

20. Strict positivity of the affine probes is used for the KL upper bound. It should not be silently weakened to mere nonnegativity.

21. The causal fair-bit accounting includes actual probe emissions as well as hidden transitions; the terminal compiler's bit count does not sample a quantum output.

22. The read-only final-head workflow now resolves the final-SHA attestation weakness of Revision 58. It still does not provide a cryptographic author signature.

23. The finite regression suite is appropriately classified as regression evidence. It does not prove the universal entropy theorem or the LPS spectral input.

24. The title “sharp stochastic widths” is justified at the level of matching powers under `p_*=q`; it should not be read as sharp leading constants or a complete two-parameter asymptotic.

---

## 12. Final assessment

Revision 61 successfully answers the most important quantitative criticism of r39. The logarithmic factor has been removed under clearly stated full-action spectral and geometric hypotheses by a credible entropy--transport argument. The new LPS example makes the linear noisy law fully numerical. The inherited causal theorem addresses the previously unhandled distinction between terminal outputs and adaptive whole-transcript laws. Exact source identity and final-head reproduction are substantially better than in Revision 58.

I found no fatal mathematical error in the inspected new chains. The work is now a serious and potentially strong specialist contribution.

It still does not meet the Annals / Inventiones / JAMS / Acta threshold. The resource model is specialized and nonuniform; the sharp law depends on a strong full-action gap and synchronization; the causal theorem depends on repeatable oracle probes; several central quantitative and process questions remain open; independent theorem-level priority is unresolved; and the wider repository pipeline remains mathematically separate and incomplete.

**Recommendation: reject at the four leading general mathematics journals; encourage separate, tightened submissions to strong specialist venues after independent priority review.**
