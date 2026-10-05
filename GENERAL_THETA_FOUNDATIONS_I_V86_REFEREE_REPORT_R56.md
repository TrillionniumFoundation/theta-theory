# Referee Report — General Theta Foundations I, Revision 86 (r56)

**Focused quantitative manuscript:** *Finite-Use Geometry and Learning of Ordered Quantum Measurements*  
**Current auxiliary supplement:** *Binary Foundations and Auxiliary Proofs*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`  

**Reviewed branches:**
- `revision/general-theta-foundations-i-v86-one-sided-native-2026-10-05`
- `revision/general-theta-foundations-i-v86-one-sided-publication-2026-10-05`
- `revision/general-theta-foundations-i-v86-one-sided-review-ready-2026-10-05`
- `revision/general-theta-foundations-i-v86-r55-response-2026-10-05`

**Reviewed exact final head:** `0a7d65923c12334ecc60ec42084bdd0c612e2e49`  
**Candidate publication:** `a5701ac81e0f6d40cbff61736a1e2e649286fae3`  
**Qualified native source:** `7f86bddb2309417edaa74430073a1bdf5329d8bf`  
**Completed predecessor:** Revision 85, `ca39533970c77a156cafe916ee6287c54c91fa00`  
**Controlling external report:** v85/r55, `107182f19e0534ae99cd68fc10cd71dddd1563a7`  
**Controlling proof/pipeline audit:** v85/r55, `7dc5d76ace1aa993c946770e0b5b2d8b853e5419`  
**Source qualification workflow:** `37289363662`, conclusion `success`  
**Exact-head read-only reconstruction:** `37290886448`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v86-one-sided-external-referee-r56-2026-10-05`  
**Date:** 5 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**.

Revision 86 is a substantive advance over Revision 85. The principal theorem is no longer restricted to one prescribed two-sided smooth curve. At a fixed ordered measurement `E`, a fixed nonzero one-sided direction `H`, and a fixed quadratic remainder allowance `Lambda`, the paper classifies every legal finite perturbation

```text
F = E + s H + R,
||R||_Sigma <= Lambda s^2,
```

uniformly over the whole stated remainder neighborhood, all integers `N>=1`, and all sufficiently small `s>0`. It also separates three acquisition mechanisms: regular tangent directions, coherent tangential directions, and first-order support openings. In the middle case, independent product probe–reference acquisition has only square-root order while an adaptive coherent correction protocol has linear order. The paper further gives controlled higher-order consequences and an exact scalar mixed-rate family.

I did not find a fatal mathematical gap in the new Sections 75–76. In the form submitted, the following components are coherent:

1. the reference-uniform diamond-norm estimate for Hermitian classical-output channel differences;
2. the exact one-sided tangent-cone condition
   ```text
   Q_j H_j Q_j >= 0;
   ```
3. the normalized analytic realization of every direction satisfying that condition;
4. identification of the cone lineality with `Q_jH_jQ_j=0` for all outcomes;
5. the full covariance-range criterion
   ```text
   H in Ran(C_E)
     iff Q_jH_jQ_j=0 for all j and Gamma_E(H) in W_E;
   ```
6. the finite normalized-factor remainder estimate;
7. the square-root upper bound with the full `Ns^2` remainder retained before truncation;
8. the impossible-output lower in the support-opening branch;
9. the finite corrected-logical-channel lower in the coherent tangential branch;
10. uniformity of the two lower constructions over the permitted finite remainder;
11. the independent-product converse based on one-copy Bures control and fidelity tensorization;
12. the distinction between independent product acquisition and arbitrary entangled parallel acquisition;
13. the power-jet corollary under the actual `O(t^(2q))` hypothesis;
14. the mixed scalar rate
    ```text
    min{1, sqrt(N)t^a + N t^b};
    ```
15. the represented-rational cone and supplied-pair certificate; and
16. the continued refusal to infer stationarity from an unspecified zero first jet.

The strongest statement is therefore a finite-neighborhood theorem, not merely a curve theorem. For fixed `E,H,Lambda`,

```text
D_N(E,F) = Theta(min{1,sqrt(N)s})
    when H belongs to Ran(C_E),

D_N(E,F) = Theta(min{1,Ns})
    otherwise,
```

uniformly over all legal `F` in the quadratic tube. Moreover, for the independently acquired product-probe class,

```text
regular tangent:       product sqrt / adaptive sqrt,
coherent tangent:      product sqrt / adaptive linear,
support opening:       product linear / adaptive linear.
```

This is a useful structural refinement. It shows that a linear finite-use scale can arise either from a purely classical impossible event or from coherent accumulation, and that these mechanisms have different acquisition requirements.

The four-leading-general-journal conclusion nevertheless remains negative. The new theorem is still local and nonuniform in the base point, tangent, and second-order allowance. It does not provide a uniform metric equivalence on the full measurement body, a matching arbitrary-pair lower for the midpoint covariance certificate, a complete stratified boundary geometry, a full-boundary entropy or learning theorem, or a classification of unrestricted higher-order approaches. The product converse applies to a deliberately narrow acquisition class and leaves arbitrary entangled parallel inputs open. The one-sided cone itself is standard positive-semidefinite cone geometry, while the square-root/linear coherent mechanism remains conceptually downstream of the established Kraus-span and quantum-error-correction metrological criterion. Independent priority clearance has not been obtained.

**Disposition outside the four leading general journals:** the focused quantitative manuscript is a strong candidate for a leading specialist journal in mathematical quantum information, quantum statistics, or operator-theoretic information theory, after the priority and scope revisions listed below. I would not request another wholesale reconstruction of the historical corpus.

---

## 1. Frozen object and genealogy

The latest General Theta Foundations I object located in the final branch survey is Revision 86. No Revision 87 branch was present when the review branches were created.

The review-ready and response aliases identify

```text
0a7d65923c12334ecc60ec42084bdd0c612e2e49.
```

This exact final head is a metadata-only child of publication commit

```text
a5701ac81e0f6d40cbff61736a1e2e649286fae3,
```

which is a direct child of qualified native source

```text
7f86bddb2309417edaa74430073a1bdf5329d8bf.
```

The final commit adds only `GENERAL_THETA_FOUNDATIONS_I_V86_FINAL_HEAD_REQUEST.json`. The publication commit adds the four rendered manuscripts and source-bound evidence. The mathematical source reviewed is the native object.

The exact predecessor is completed Revision 85 at `ca395339...`. The two controlling r55 reports are frozen by commit identity. The v86 mathematical delta is concentrated in:

- `sections/75-one-sided-tangent-neighborhoods.tex`;
- `sections/76-independent-probes-and-higher-jets.tex`;
- `editions/operational-introduction86.tex`;
- `editions/current-comparison86.tex`;
- `cone_geometry.py` and `cone_check.py`;
- the response, proof audit, resource ledger, literature audit, and current build records; and
- registered explanatory insertions in Sections 73–74.

The insertions in Sections 73–74 clarify the local curvature norm and the reference-uniform channel norm. The registry states that exact removal restores the complete predecessor section bytes. I found no disguised change to the v85 theorem through these insertions.

---

## 2. Main mathematical contribution

### 2.1 One-sided tangent cone

Let `P_j=supp(E_j)` and `Q_j=I-P_j`. If `H` is the right derivative of a legal measurement curve, positivity gives

```text
J_j=Q_j H_j Q_j >=0.
```

The converse is proved constructively. For sufficiently large `c`,

```text
E_j^c(s)=(E_j+sH_j+c s^2 I)/(1+k c s^2)
```

is positive for small `s>=0`, sums to the identity, and has right derivative `H`. The Schur-complement estimate correctly handles singular opening blocks and cross-support terms. Zero effects reduce to `H_j>=0` and cause no gap in the construction.

The cone lineality is exactly `J_j=0` for every `j`. This is the correct one-sided enlargement of the two-sided tangent space. The result should, however, be positioned as an application of standard tangent-cone geometry of the positive-semidefinite cone plus the coupled normalization constraint, rather than as a newly discovered primitive of convex analysis.

### 2.2 Complete covariance range

Pairing an arbitrary zero-sum Hermitian direction with the full v84 covariance kernel first exposes the independent missing-support variables. Orthogonality to them forces all `J_j` to vanish. The remaining pairing is

```text
-2 tr(A Gamma_E(H)),
Gamma_E(H)=(i/2) sum_j [P_j,H_j].
```

Finite-dimensional self-adjointness then gives

```text
H in Ran(C_E)
  iff J_j=0 for all j and Gamma_E(H) in W_E.
```

The sign, factor two, and real-Hermitian convention are consistent with the unitary and two-sided specializations. I find this extension correct.

### 2.3 Uniform finite tangent neighborhoods

The tube

```text
||F-E-sH||_Sigma <= Lambda s^2
```

is a finite-pair condition. No curve or differentiable factorization of `F` is assumed. This is an important improvement in quantifier structure.

For the range branch, a fixed horizontal factor solution supplies a legal surrogate `G(s)` with

```text
D_N(E,G(s)) <= 2 b sqrt(N) s
```

and

```text
||G(s)-E-sH||_Sigma <= K_b s^2.
```

The comparison with `F` therefore gives

```text
D_N(E,F)
 <= 2 b sqrt(N)s + (Lambda+K_b)N s^2.
```

The proof correctly retains the quadratic term. With `x=sqrt(N)s`, the second term is `O(x^2)` and is absorbed only when `x<=1`; for `x>=1` the distance is capped at two. This yields the claimed square-root upper uniformly in the tube.

A fixed component of the nonzero `H` gives a Bernoulli gap uniformly over the same tube, hence the matching square-root lower. This part is sound, including probability endpoints.

### 2.4 Two linear mechanisms

If some `J_j` is nonzero, a vector in the missing support has zero base probability and positive first-order probability under every allowed `F`. The at-least-one-occurrence event gives

```text
2[1-(1-lambda s/2)^N],
```

which has the truncated linear order. This is a product-input, classical lower and does not use quantum memory.

If all `J_j` vanish but `Gamma_E(H)` lies outside `W_E`, the support-complement code is applied to `Gamma_E(H)`. The corrected first derivative is the logical commutator, while the finite pair contributes at most `Lambda s^2`. Comparison with the logical exponential gives

```text
||Phi_F-Ad(exp(-is Gamma_L))||_diamond
 <= (Lambda+2||Gamma||_op^2)s^2.
```

The same integer-call argument as in v85 yields the linear lower. The code, recovery, and Helstrom readout depend only on the known base, direction, scale, and call count, not on the unknown tube remainder. The construction is therefore genuinely uniform over the tube.

### 2.5 Product acquisition

The manuscript defines a precise restricted class: one probe–reference pair per call, no correlation between different pairs, no feedback into later inputs, arbitrary final joint processing, and public randomization. This class is narrower than arbitrary nonadaptive acquisition with an entangled many-call input.

When all missing-support blocks vanish, canonical normalized factors give a uniform one-copy Bures displacement of order `s`. The `O(s^2)` channel difference between the surrogate and `F` gives another Bures displacement of order `s`. The triangle inequality, multiplicativity of root fidelity, and the unhalved trace/fidelity inequality yield

```text
D_N^prod(E,F) <= C sqrt(N)s.
```

The constants are consistent. A joint final readout cannot increase trace distance, and public randomization preserves the bound by convexity. This proves the submitted product column.

The result does **not** settle arbitrary entangled parallel inputs. This middle resource class is important in channel discrimination and must remain visibly open.

### 2.6 Higher orders and mixed scales

The power-jet corollary is correctly conditional on

```text
F(t)=E+t^q H+O(t^(2q)).
```

A first nonzero coefficient alone does not imply this remainder. The manuscript states that limitation.

The scalar three-outcome family with exponents `1<=a<b<2a` has two independent mechanisms. The third label gives `Nt^b`; the conditional binary bias gives `sqrt(N)t^a`. Since the scalar-input full record dominates all stopping or adaptive processing, the product law is the optimal experiment. The lower and upper arguments give

```text
Theta(min{1,sqrt(N)t^a+Nt^b}).
```

I find the proof correct. It is a valuable warning against reducing all zero-jet behavior to one leading coefficient.

---

## 3. Reproducibility and implementation

The exact classifier correctly distinguishes:

- `regular_tangent`;
- `coherent_tangent`;
- `support_opening`; and
- `higher_order_undetermined`.

It performs exact Gaussian-rational legality checks, support projection, positive-semidefinite tests, real support-span rank, Hilbert–Schmidt projection, and optional componentwise finite-pair remainder checks. A support-opening certificate includes an exact rationally represented witness probability. It does not compute the local theorem interval, a curvature bound, an optimal adaptive tester, a recovery circuit, or a physical implementation.

The new finite suite is appropriately classified as regression evidence. It does not prove the continuum theorem. The current receipt records 353 new positive checks, 27 negative controls, 56 complete finite classical laws, and eight direct covariance-range cross-checks, with all predecessor suites rerun under ordinary and optimized Python.

The source qualification and exact-head reconstruction both completed successfully. The exact-head workflow checks out `0a7d659...` itself and verifies native ancestry, all four manuscripts, all exact suites, and the linked journal package read-only. This is a strong reproducibility record, though not a formal proof certificate or a human authorship signature.

---

## 4. Relation to the literature and priority

The manuscript now correctly credits the Kraus-span metrological exponent criterion and exact correction mechanism. It also credits standard fidelity purification, multiplicativity, and trace-distance inequalities.

Two further comparisons are required.

First, the one-sided condition `QHQ>=0` is the standard tangent-cone condition for the positive-semidefinite cone, assembled here across outcomes with normalization. The paper should cite the semidefinite variational-analysis literature directly—for example, work computing first- and second-order tangent sets of the PSD cone—and identify the coupled measurement-specific addition.

Second, the three acquisition regimes should be compared with the channel-discrimination literature separating adaptive, nonadaptive, product-input, classical-feedback, sequential, and entangled-parallel strategies. At minimum, the revision should discuss:

- Harrow–Hassidim–Leung–Watrous, *Adaptive versus non-adaptive strategies for quantum channel discrimination*, arXiv:0909.0256;
- Salek–Hayashi–Winter, *Usefulness of adaptive strategies in asymptotic quantum channel discrimination*, arXiv:2011.06569; and
- Li–Hirche–Tomamichel, *Sequential Quantum Channel Discrimination*, arXiv:2210.11079.

These works do not immediately subsume the present local finite-neighborhood theorem: their models, objectives, and asymptotic criteria differ. They are nevertheless directly relevant to the resource taxonomy, particularly because “nonadaptive” may include entangled parallel inputs whereas the submitted product class does not.

The present author-side literature audit is careful but is not independent specialist priority clearance. I cannot certify historical firstness of the support-coordinate cone, remainder-uniform finite-pair law, or product/adaptive trichotomy from the repository audit alone.

---

## 5. Why the top-four threshold is not met

### 5.1 Local rather than global geometry

The theorem fixes `E,H,Lambda`. Its constants may degenerate with support eigenvalues, tangent size, the support residual, and the allowance. There is no uniform stratified metric on the full POVM body and no arbitrary-pair matching lower for the midpoint covariance.

### 5.2 Possible vacuity of a prescribed tube

For an arbitrarily small `Lambda`, the tube may contain no legal pair for small positive `s`. This does not make the theorem false, but it weakens the force of the phrase “whole finite neighborhood.” The paper should state a nonemptiness criterion or an explicit sufficient allowance from the cone realization.

### 5.3 An unresolved middle acquisition class

The product converse excludes inter-call entanglement. The adaptive theorem allows full quantum memory. The important class of arbitrary entangled parallel testers lies between them and remains unclassified.

### 5.4 Established conceptual mechanisms

The PSD tangent cone, fidelity tensorization, and Kraus-span/QEC exponent mechanism are established. The new contribution is their integration into a support-coordinate, finite-remainder theorem. That integration is strong specialist mathematics, but not yet a new general-journal-level paradigm.

### 5.5 Higher-order boundary remains partial

The power-jet theorem assumes an `O(t^(2q))` remainder; the mixed example shows other scales can intervene. There is no general Newton-polygon, jet-stratified, or multiscale classification for zero first jets.

### 5.6 Learning and computation remain restricted

The learning law is still fixed-`k`; the constructive upper retains a `k^3` factor. Polynomial exact cone decisions do not imply polynomial entropy-optimal dictionaries, general recovery synthesis, or collective readout synthesis.

### 5.7 Priority remains unsettled

The direct adaptive/nonadaptive literature comparison and independent specialist review are still missing.

### 5.8 The wider Theta programme is separate and open

The finite-dimensional measurement theorem does not discharge the repository's raw local-limit, shell-conditioning, process-CLT, Mosco, nonlinear semigroup, filtering, response, or posterior-contraction gates. All aggregate closure flags remain false.

---

## 6. Required revisions before specialist submission

1. **Add a direct adaptive/nonadaptive discrimination comparison.** State exactly how `D_N^prod` differs from arbitrary parallel, separable, classical-feedback, and fully adaptive strategy classes.

2. **Cite the PSD tangent-cone literature.** Present `QHQ>=0` as standard cone geometry and isolate the measurement-specific normalization and finite-use consequences.

3. **Address tube nonemptiness.** Give an explicit sufficient lower bound on `Lambda`, or state prominently that a prescribed tube can be empty.

4. **Keep the full `Ns^2` remainder visible.** The finite-neighborhood theorem should continue to display the actual finite upper before asymptotic simplification.

5. **Do not extend the product converse to entangled parallel strategies.** This limitation should remain in the abstract, theorem discussion, and comparison section.

6. **Separate the two linear mechanisms in every summary.** Impossible-event accumulation and coherent correction are mathematically and operationally different.

7. **Clarify “rational curve.”** In the cone construction, specify whether “rational” means a rational function of `s`, rational coefficients on represented input, or merely the displayed normalized formula.

8. **Preserve the fixed-object quantifiers.** Constants and the small interval are uniform over the tube but not over base measurements or directions.

9. **Keep zero-jet results conditional.** Do not advertise a general higher-order classification from the power-jet corollary and one scalar example.

10. **Retitle or refocus the journal-facing object.** The strongest new content is finite-use discrimination geometry; the inherited learning material should not obscure the main theorem.

11. **Maintain the computational boundary.** Exact cone/pair certificates must not be described as computing adaptive distance, recovery, curvature, or implementation.

12. **Obtain independent priority review.** Experts in channel discrimination, quantum metrology, and semidefinite variational geometry should review the theorem-level novelty boundary.

13. **Keep finite regression separate from proof.** The current false continuum-proof and physical-execution flags should remain.

14. **Keep the structural and archival objects separate.** The structural companion and 242-page preservation edition are not additional evidence of novelty for the measurement paper.

15. **Do not use wider-pipeline history as a significance multiplier.** The A/B/C/D analytic programme is independent and open.

---

## 7. Detailed comments

1. Define `||·||_Sigma` before the first abstract-level use in any expanded summary.

2. The cone realization should say explicitly that the common denominator is positive for all sufficiently small `s` and that normalization is exact.

3. The Schur-complement proof should retain the zero-support case separately; it cannot be hidden inside a smallest-positive-eigenvalue notation.

4. The lineality statement concerns the largest vector subspace contained in the cone, not the affine hull of the cone.

5. The full range criterion applies to arbitrary zero-sum Hermitian tuples, not only feasible one-sided directions. This is stronger algebraically and should be stated carefully.

6. In the factor remainder, the ordering of the inverse roots matters; no commuting simplification should be introduced.

7. `K_b=k b^2(2+h)` is deliberately coarse. It need not be optimized, but its dependence should be retained.

8. The square-root branch uses a horizontal solution; the product converse uses the canonical, generally nonhorizontal solution. These should not be conflated.

9. In the generic Bernoulli lower, the chosen component expectation may have either sign. The absolute gap and sufficiently small `s` handle this.

10. In the opening branch, the decision event and input vector are fixed over the entire tube. This uniformity is an important point.

11. The coherent branch's ideal readout depends on `E,H,s,m`, but not on the unknown remainder. This should remain explicit.

12. The product model permits pair-dependent but independently acquired references; “product input” should not be read as “no reference.”

13. The product upper is a fidelity argument on output states, not a statement that the channel diamond distance is `O(s)` with a useful tensor-product bound.

14. Public randomization with a retained record should be described as a direct-sum convex combination, for which the same bound holds.

15. The mixed scalar equality between adaptive and product distance relies on input dimension one and the full iid record dominating every stopped protocol.

16. The power-jet conclusion applies after the substitution `s=t^q`; it does not require differentiating `t=s^(1/q)`.

17. The exact witness vector may be represented by a rational vector and a rational squared norm even when the corresponding normalized unit vector has irrational coordinates.

18. A supplied-pair certificate proves only the displayed component allowances at that `s`; it does not prove membership in a curve neighborhood for all small parameters.

19. The exact final commit is unsigned. This is a provenance issue, not a mathematical defect.

20. The 36-page primary is editorially manageable, but the title and abstract should foreground the finite-neighborhood trichotomy rather than the inherited programme breadth.

---

## 8. Final assessment

Revision 86 gives a real extension of the finite-use measurement theory. The main positive achievements are:

- the complete one-sided support-coordinate tangent cone;
- the full covariance-range test for arbitrary zero-sum Hermitian directions;
- a finite-pair dichotomy uniform over a fixed quadratic tangent neighborhood;
- separation of classical support-opening and coherent-correction linear mechanisms;
- a matching independent-product/adaptive acquisition table;
- controlled power-jet consequences and a nontrivial mixed-rate example; and
- exact represented-input cone and pair certificates.

I found no fatal gap in these new chains. The paper has reached a strong specialist level.

It has not reached the four-leading-general-journal threshold. The theory remains local and nonuniform, the middle entangled-parallel strategy class is open, the higher-order boundary is only partially classified, the key primitive mechanisms have established antecedents, the learning/computational extensions remain restricted, and independent priority clearance is absent.

**Recommendation: reject at Annals / Inventiones / JAMS / Acta; encourage a focused submission to a leading specialist journal after the revisions above.**
