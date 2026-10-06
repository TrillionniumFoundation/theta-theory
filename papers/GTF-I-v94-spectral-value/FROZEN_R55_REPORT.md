# Referee Report — General Theta Foundations I, Revision 85 (r55)

**Focused quantitative manuscript:** *Finite-Use Geometry and Learning of Ordered Quantum Measurements*  
**Current auxiliary supplement:** *Binary Foundations and Auxiliary Proofs*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`  

**Reviewed branches:**
- `revision/general-theta-foundations-i-v85-smooth-boundary-native-2026-10-05`
- `revision/general-theta-foundations-i-v85-smooth-boundary-publication-2026-10-05`
- `revision/general-theta-foundations-i-v85-smooth-boundary-review-ready-2026-10-05`
- `revision/general-theta-foundations-i-v85-r54-response-2026-10-05`

**Reviewed exact final head:** `ca39533970c77a156cafe916ee6287c54c91fa00`  
**Candidate publication:** `05ba736ff51e1d3d6de89f6902df063bce7ace90`  
**Qualified native source:** `81e17daffff86fe0ac1762f06a4785eb9c4339bc`  
**Completed predecessor:** Revision 84, `9ee14476f539a38f2f45f9bd4ed99a658a7eb14d`  
**Controlling external report:** v84/r54, `e96b4d271e60ec636e1e6022d1708b755a9e4d4a`  
**Controlling proof/pipeline audit:** v84/r54, `57d23a10cb08171b2ab23464fca8ba89e808f253`  
**Source qualification workflow:** `37278772761`, conclusion `success`  
**Exact-head read-only reconstruction:** `37280001888`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v85-smooth-boundary-external-referee-r55-2026-10-05`  
**Date:** 5 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This remains **not a correctness rejection**.

Revision 85 makes a genuine mathematical advance over Revision 84. The fixed-unitary-orbit theorem has been extended to every fixed two-sided `C^2` curve of ordered measurements with nonzero first derivative, without a constant-rank assumption and without assuming that the actual curve admits differentiable canonical Kraus factors. The new theorem also permits second-order rank openings. The proof is not merely an asymptotic Fisher-information argument: it constructs a normalized horizontal surrogate with the same first jet, controls the actual-versus-surrogate channel error to second order, and proves a corrected logical-channel derivative and finite-angle lower bound in the singular branch.

I have not found a fatal mathematical gap in the new Sections 72–74. In particular, I find the following components coherent as written:

1. the uniform finite Bernoulli-product lower bound, including endpoint cases and the finite truncation in the number of observations;
2. the necessary two-sided tangent condition `Q_j H_j Q_j=0` and its converse realization by normalized analytic factors;
3. the support generator
   ```text
   Gamma_E(H) = (i/2) sum_j [P_j,H_j]
   ```
   and the range criterion
   ```text
   H in Ran(C_E)  iff  Gamma_E(H) in W_E;
   ```
4. specialization of that criterion to the v84 unitary-orbit criterion modulo the support span;
5. construction of a horizontal normalized surrogate with the same value and first derivative as the given curve;
6. the `sqrt(N)|t| + O(Nt^2)` finite adaptive upper bound, including the orthogonality of differentiated call slots;
7. the pair-dependent support-complement code and recovery applied to `Gamma_E(H)`;
8. the calculation of the corrected logical derivative `-i[Gamma_L,·]` from the complete recovery identities;
9. the one-cycle remainder
   ```text
   ||Phi_t - Ad(exp(-it Gamma_L))||_diamond <= kappa t^2,
   kappa = L/2 + 2||Gamma||_op^2;
   ```
10. the integer-call choice and finite-angle lower yielding the linear `N|t|` branch;
11. the explicit projective-to-full-rank example showing that the theorem is not merely a unitary-orbit restatement;
12. the refusal to classify a zero first derivative as stationarity;
13. the deterministic control-error ledger and its angle-dependent sufficient budgets; and
14. the exact represented-input first-jet classification with explicit exclusions of curvature estimation, recovery synthesis, and physical execution.

The strongest new theorem is therefore the following fixed-curve local classification. For every fixed two-sided `C^2` measurement curve `E(t)` with `H=E'(0) != 0`, there are curve-dependent `c,C,t_0>0` such that for all integers `N>=1` and `|t|<=t_0`,

```text
D_N(E(0),E(t)) = Theta(min(1,sqrt(N)|t|))
    if Gamma_E(H) belongs to W_E,

D_N(E(0),E(t)) = Theta(min(1,N|t|))
    if Gamma_E(H) does not belong to W_E.
```

This is a useful and nontrivial finite-pair boundary theorem. It is stronger than the v84 fixed-orbit statement because it includes nonunitary first jets and second-order rank changes.

The four-leading-general-journal conclusion nevertheless remains negative.

The first reason is scope. The new result is local along one fixed smooth curve, with constants depending on its tangent, curvature, nonzero support eigenvalues, and support-complement gap. It is not a uniform comparison on the ordered-POVM body. It does not give a matching lower bound for the midpoint covariance certificate on arbitrary pairs, a complete stratified boundary metric, a full-boundary volume or entropy theorem, or a common learning theorem at the boundary. Curves with zero first derivative and one-sided rank openings are expressly outside the theorem. These exclusions are mathematically correct, but they are precisely the regimes that prevent the local theorem from becoming a global geometry of the body.

The second reason is conceptual priority. The square-root versus linear exponents and the error-correction mechanism are still manifestations of the established Hamiltonian-not-in-Kraus-span/Kraus-product-span metrological dichotomy and the Knill–Laflamme correction principle. The manuscript now states this boundary accurately. Its genuine contributions are the complete support-coordinate kernel, the first-jet support generator, the normalized effect-coordinate surrogate through rank openings, and the direct finite-angle error ledger. These are worthwhile, but they do not replace the conceptual source of the metrological phase distinction.

The third reason is breadth. The balanced-interior entropy and learning conclusions remain fixed-`k`; the constructive upper retains a visible `k^3` factor and no growing-outcome minimax theorem is obtained. Exact support and first-jet decisions are polynomial on represented rational inputs, but the public entropy-optimal dictionary, general recovery synthesis, and arbitrary collective readout synthesis remain potentially exhaustive or existential. The structural companion and the wider A/B/C/D Theta programme are independent objects and cannot add significance to the measurement paper unless their own central analytic chains are completed.

The fourth reason is priority certification. Revision 85 has corrected the outdated statement that the full text of Yoshida–Okigami–Posta–Grinko was unavailable. The current theorem-level comparison is materially better and, on inspection, the cited known-symmetry tomography paper does not directly subsume the present fixed-pair support-generator theorem. Nonetheless, the support-kernel parameterization, the `Gamma_E(H)` range formula, and the normalized-surrogate boundary proof still need an independent specialist priority assessment. An author-side audit, exact reconstruction, or AI referee report is not a substitute for that assessment.

**Disposition outside the four leading general journals:** the focused quantitative article is now a strong candidate for a leading specialist journal in mathematical quantum information or quantum statistical theory, subject to a final priority check and several exposition revisions listed below. I would not request another wholesale reconstruction of the paper or the historical corpus.

---

## 1. Frozen object and genealogy

The latest General Theta Foundations I object located in the complete branch survey is Revision 85. No Revision 86 branch was present when this review branch was created.

The review-ready and response aliases identify the exact final head

```text
ca39533970c77a156cafe916ee6287c54c91fa00.
```

This is a metadata-only child of publication commit

```text
05ba736ff51e1d3d6de89f6902df063bce7ace90,
```

which is a direct child of qualified native source

```text
81e17daffff86fe0ac1762f06a4785eb9c4339bc.
```

The final child adds only `GENERAL_THETA_FOUNDATIONS_I_V85_FINAL_HEAD_REQUEST.json`. The publication child adds the four rendered documents and source-bound evidence. The theorem source is the native object.

The exact baseline is the completed v84 final head `9ee14476...`. The two controlling r54 review commits are frozen and identified above. The v85 mathematical delta is concentrated in:

- `sections/72-finite-product-prerequisite.tex`;
- `sections/73-smooth-boundary-curves.tex`;
- `sections/74-certified-control-stability.tex`;
- `editions/operational-introduction85.tex`;
- `editions/current-comparison85.tex`;
- `curve_geometry.py` and `curve_check.py`;
- the updated bibliography, response, proof audit, literature audit, resource ledger, and build records.

All inherited mathematical sections are reported byte-identical. This matters: v85 extends the v84 support theorem rather than silently modifying the premises that were previously reviewed.

---

## 2. Mathematical assessment

### 2.1 Finite Bernoulli premise

The new main-text lemma proves, in unhalved `l1` distance,

```text
||Ber(p)^N - Ber(q)^N||_1
  >= (1/128) min(1,sqrt(N)|p-q|)
```

for all `p,q in [0,1]` and every integer `N>=1`.

The characteristic-function proof is valid. For `u=m^{-1/2}` and `z(a)=1-a+a exp(iu)`, the modulus lower and the derivative of the argument give angular separation proportional to `sqrt(m)|p-q|`. The bounded complex statistic converts expectation separation to an `l1` lower. The truncation `m=floor((16h^2)^(-1))` is positive and no larger than `N` in the relevant case. Endpoint and large-gap cases are handled separately. The final observation that a two-sided differentiable probability with nonzero derivative cannot start at zero or one is also correct.

This addition successfully removes an opaque dependence of the new discrimination theorem on the long binary supplement.

### 2.2 Two-sided first jets

For a two-sided positive curve, every vector in the missing support sees a nonnegative scalar function with a local minimum at zero, so `Q_j H_j Q_j=0`. Polarization gives the full block identity. Normalization gives `sum_j H_j=0`.

The converse construction is also valid. With `A_j=sqrt(E_j)` and

```text
B_j=(sqrt(E_j))^+ H_j (I-P_j/2),
```

one obtains

```text
A_j^*B_j+B_j^*A_j=H_j,
sum_j A_j^*B_j=-i Gamma_E(H).
```

The stacked first normalization derivative is therefore anti-Hermitian. The curve

```text
(A+tB)(I+t^2 B^*B)^(-1/2)
```

is normalized and analytic for small two-sided `t`, and its induced effects have the prescribed value and derivative. The support inverse is used only on the fixed support. No inversion of a singular effect on the whole space occurs.

The certificate implementation uses only exact support projectors and rational linear algebra; it does not need to represent the algebraic square roots used in the existence proof. The manuscript should preserve this distinction prominently.

### 2.3 The support generator

Pairing a realizable tangent with the complete v84 covariance kernel eliminates both the tuple mean and the missing-support variables. The remaining pairing is

```text
<H,K(A,Z)> = -2 tr(A Gamma_E(H)).
```

Since the covariance is self-adjoint in finite dimension, its range is the orthogonal complement of its complete kernel. Hence

```text
H in Ran(C_E) iff Gamma_E(H) in W_E.
```

The sign and factor two are consistent. For a unitary tangent, `Gamma_E(H)-G` belongs to the support span, so the criterion specializes to the v84 theorem. The manuscript correctly avoids extending the stationary-generator conclusion to a general zero first jet.

### 2.4 Horizontal surrogate and square-root branch

When `H` lies in the covariance range, the retained covariance factorization gives a horizontal factor perturbation `B` with `A^*B=0` and `T_A B=H`. The normalized curve

```text
A(t)=(A+tB)(I+t^2 S)^(-1/2),  S=B^*B,
```

satisfies the displayed derivative identities. In particular, no noncommuting factors are reordered. The operator derivative bounds are sufficient for the subsequent Stinespring estimate.

For an adaptive purified tester, differentiated-call terms are orthogonal because `W^*W'=0`. This yields the finite path derivative bound `2b sqrt(N)`. Comparing the actual curve and the surrogate by their common first jet and second-derivative channel bounds produces an `O(Nt^2)` hybrid error. For `sqrt(N)|t|<=1`, that term is absorbed into the desired square-root scale; for larger values the distance is capped. The product Bernoulli lemma supplies the matching lower from one state and one label event.

I find this branch correct. The proof would benefit from one explicit sentence stating that the norm `L` used later is the supremum of the sum of the effect second-derivative operator norms on the fixed interval; the present notation is recoverable but slightly dispersed.

### 2.5 Corrected derivative and linear branch

The v84 support-complement code applies to the Hermitian support generator `Gamma`. Its residual outside the support span is traceless and has positive and negative parts of equal trace, producing a logical gap

```text
Delta=||Z||_HS^2/tr(Z_+)>0.
```

The complete CPTP recovery operates on the actual classical label and the retained reference, not on a discarded input or an inaccessible environment.

Using the normalized first-order factor realization, the complete recovery identities imply

```text
sum conjugate(c_lmu) R_l dot(L_mu) J
  = J^* sum L_mu^* dot(L_mu) J
  = -i Gamma_L.
```

The adjoint contribution gives the logical commutator derivative. The actual corrected channel and the ideal logical unitary have equal value and first derivative, while their second derivatives are bounded by `L` and `4||Gamma||_op^2`, respectively. Taylor's integral remainder gives the stated `kappa t^2` one-cycle error.

Telescoping `m` cycles, choosing

```text
m=min{N,floor((|t|Delta)^(-1))},
```

and imposing the displayed fixed-curve angle cap yields a positive multiple of `min(1,N|t|)`. The ordinary channel hybrid gives the matching upper. The floor and sign bookkeeping are correct.

### 2.6 Rank opening and excluded jets

The binary example

```text
E_1(t)=(1-t^2)U_t P U_t^*+(t^2/2)I
```

is projective at zero and full rank for every nonzero sufficiently small angle. Its nonzero first jet lies in the linear branch. This demonstrates that the theorem is genuinely broader than the unitary-orbit result.

The scalar example `(t^2,1-t^2)` correctly shows that a zero first derivative need not mean stationarity and can have an `Nt^2` scale. One-sided rank openings may have nonzero missing-support first-order blocks and are also correctly excluded.

These examples should remain close to the theorem statement because they explain both its reach and its exact boundary.

### 2.7 Certified controls

The control theorem is a conditional stability result, not a synthesis theorem. The ledger pays the ideal curvature error once and the preparation, per-cycle, and readout errors under both hypotheses. The factor two in front of these implementation errors is therefore correct.

The sufficient budgets scale with `|t|Delta`, so a fixed nonzero hardware error generally fails as `t` tends to zero. The manuscript states this. No independence of errors is assumed. No physical recovery or compiled circuit is represented as executed.

---

## 3. Literature and priority

The full text of Yoshida–Okigami–Posta–Grinko, arXiv:2609.39280v1, is now available and the revised comparison is substantially more accurate. That paper studies collective tomography under known symmetry, gives parameter-count copy/query bounds for invariant states and covariant channels, and constructs a specialized efficient approximation to the Hayashi measurement. It does not directly state the present support-kernel or fixed-pair `C^2` curve theorem. Its resource model and losses are also different.

The comparison should nevertheless be kept conservative. In particular:

- parameter-count sharpness at fixed accuracy is not the same as joint accuracy sharpness;
- a gate-efficient Hayashi measurement is not a diamond-error implementation of the pair-dependent recovery used here;
- known-symmetry common learning is not known-pair discrimination;
- the absence of an identical theorem in this targeted comparison does not establish firstness.

The closest conceptual antecedent remains channel metrology: the Kraus-span phase distinction and error-correction attainability are established. The paper's novelty must continue to be described as a support-coordinate identification and direct finite-pair boundary proof, not as a discovery of the exponent dichotomy.

---

## 4. Editorial and structural assessment

The primary article is now thirty pages and contains the complete probability, covariance, kernel, correction, and smooth-curve premises needed for its main discrimination theorem. This is a substantial improvement over relying on the complete binary supplement for a small but essential Bernoulli step.

The supplement remains long but current and reconstructible. The new prerequisite table usefully distinguishes actual dependencies from preserved historical material. The structural article is independent and should remain a separate submission object. The 236-page complete edition is an archive, not a journal-facing manuscript and not evidence of additional novelty.

For a specialist submission, I recommend retaining the focused primary, the current binary supplement, and a short machine-readable reproducibility package. The complete edition and repository-wide programme ledger should remain available but outside the normal article narrative.

---

## 5. Required revisions before specialist resubmission

1. **Keep the novelty boundary in the theorem discussion.** State immediately after the main theorem that the exponents and QEC mechanism are established, while the new objects are the support-coordinate first-jet criterion, the rank-opening surrogate argument, and the direct finite-angle ledger.

2. **State `L` locally wherever it is used.** The curvature norm is defined earlier, but the logical-channel lemma and control theorem should repeat its precise definition or point to a numbered definition.

3. **Separate existence from computation.** The analytic factor construction uses support square roots and pseudoinverses; the rational certificate uses projectors and elimination. Do not let “exact polynomial decision” suggest exact symbolic construction of the recovery or full curve.

4. **Retain fixed-curve quantifiers in every summary.** Constants and the angle interval may degenerate near support transitions, small residual gaps, or large curvature. Avoid “boundary classification” without the fixed-curve qualifier.

5. **Do not promote the result to arbitrary-pair equivalence.** The midpoint covariance remains a global upper only. A local theorem along all nonzero first jets is not a uniform metric theorem on pairs.

6. **Preserve the zero-jet and one-sided exclusions.** They should remain in the theorem vicinity, not only in an audit file.

7. **Clarify the one-call channel norm estimate.** State explicitly that the relevant Hermiticity-preserving maps are trace-annihilating derivatives/differences of channels, so the diamond norm may be optimized over input states with a reference.

8. **Keep pair-dependent controls separate from learning.** The code, recovery, target angle, call count, and Helstrom readout are known-pair resources and cannot be transferred without charge into the common unknown-device learner.

9. **Retain the angle-dependent implementation budget.** Do not summarize the control theorem as fixed-noise robustness.

10. **Update priority only through primary sources.** The new covariant-learning comparison is current; an independent specialist should still assess the support-kernel and first-jet formulas against channel-metrology and operator-statistical literature.

11. **Keep growing-`k` open.** The fixed-`k` optimal order and the constructive `k^3` dependence must remain visibly distinct.

12. **Keep computational claims narrow.** Polynomial support/first-jet classification, covariance evaluation, and affine legalization do not imply polynomial dictionary, recovery, or collective-readout synthesis.

13. **Maintain the primary/supplement dependency table.** This is now an effective editorial control and should not be removed in a shorter revision.

14. **Do not use the wider Theta programme as a significance multiplier.** Its A/B/C/D analytic gates remain independent and open.

15. **Preserve fresh release identities.** Any subsequent revision must have its own native-source, publication, and exact-final-head reconstruction chain; v85 receipts cannot qualify altered theorem source.

---

## 6. Minor comments

- In the smooth-curve theorem, “all sufficiently small two-sided `t`” is preferable to language suggesting a neighborhood uniform over the measurement body.
- The notation `Gamma_E(H)` should be introduced before the first prose use in the abstract or first paragraph, as is now mostly done.
- In the first-jet realizability lemma, one may explicitly record that the normalized inverse square root is analytic because `I+t^2B^*B` stays positive definite.
- In the horizontal surrogate proof, the relation between stacked factor operator norm and the Stinespring derivative norm could be stated in one line.
- In the linear lower, specify once that the trace/diamond norms are unhalved; the manuscript is consistent, but the convention is easy to miss when comparing external sources.
- The exact first-jet certificate should keep `higher_order_undetermined` for zero tangent. It should never return `stationary` without a complete curve.
- The rank-opening example is useful and should remain in the primary rather than only in regression evidence.
- The current full-text literature retrieval record is valuable provenance, but its digest is not a priority certificate.

---

## 7. Final disposition

The new proof package is mathematically serious, internally coherent in the parts inspected, and materially stronger than Revision 84. The paper now contains a clean finite-use theorem for every fixed two-sided smooth measurement curve with nonzero first jet, including second-order rank changes, together with an exact support criterion and a conditional control-stability ledger.

It still does not meet the breadth, conceptual novelty, priority certainty, or global reach expected of the four leading general mathematics journals. The rejection recommendation is therefore maintained, without a correctness objection and without recommending that the authors abandon the theorem. A focused specialist submission is justified after the revisions above.
