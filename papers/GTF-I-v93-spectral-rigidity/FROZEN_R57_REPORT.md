# Referee Report — General Theta Foundations I, Revision 87 (r57)

**Focused quantitative manuscript:** *Finite-Use Discrimination Geometry of Ordered Quantum Measurements*  
**Current auxiliary supplement:** *Binary Foundations and Auxiliary Proofs*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`  

**Reviewed branches:**
- `revision/general-theta-foundations-i-v87-entanglement-width-native-2026-10-05`
- `revision/general-theta-foundations-i-v87-r56-response-2026-10-05`

**Reviewed publication head:** `aab076189b7276f6a0b4113b472ea09a7ac640cc`  
**Qualified native source:** `d4fc44a02ee0585bf9da899239c3f976d75cc9cf`  
**Completed predecessor:** Revision 86, `0a7d65923c12334ecc60ec42084bdd0c612e2e49`  
**Controlling external report:** v86/r56, `9098548d4c8e347193141b34f4a631344500695a`  
**Controlling proof/pipeline audit:** v86/r56, `884087a1a62d5d8af4861fed4c4535d8e6eacd0f`  
**Source qualification and publication workflow:** `37303228873`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v87-entanglement-width-external-referee-r57-2026-10-05`  
**Date:** 5 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**.

Revision 87 makes a substantial and mathematically coherent advance over Revision 86. The principal unresolved resource class in r56—arbitrary entangled parallel acquisition—has now been addressed. The manuscript introduces a block-width interpolation in which complete probe–reference groups of at most `b` calls may be internally entangled but are independent across groups. For every fixed base measurement `E`, nonzero one-sided tangent `H`, and quadratic remainder allowance `Lambda`, the paper proves, uniformly in every integer pair `1 <= b <= N`, in every legal remainder in the tube, and at every sufficiently small scale `s`, the three orders

```text
regular tangent:       min{1, sqrt(N) s},
coherent tangent:      min{1, sqrt(N b) s},
support opening:       min{1, N s}.
```

At the endpoint `b=N`, arbitrary entangled parallel acquisition has the same local order as the fully adaptive strategy. At `b=1`, one recovers the previously audited independent probe–reference model. The proof pays the complete quadratic remainder before amplification, rather than extrapolating a Fisher-information law or silently exchanging a sequential protocol for a parallel one.

I did not find a fatal mathematical gap in the new Sections 77–78. In particular, the following components are coherent in the form submitted:

1. the explicit simultaneous normalization producing a legal measurement at every sufficiently small positive scale;
2. the Schur-complement treatment of nonzero supports, zero effects, cross-support blocks, and singular opening directions;
3. the exact finite remainder estimate and the sufficient, explicitly quantified allowance `Lambda_*`;
4. the represented-rational construction of a support floor and nonemptiness certificate;
5. the definition of block width on complete probe–reference groups, including the distinction from a shared reference across nominal blocks;
6. the finite Bures upper for an arbitrarily entangled input inside one block;
7. retention of the `n r s^2` tube-to-surrogate channel error before conversion to Bures distance;
8. multiplication of root fidelities only between genuinely independent blocks;
9. the second-moment estimate `sum n_r^2 <= b N` leading to the `sqrt(N b)` upper;
10. the corrected logical channel applied in tensor product rather than sequential composition;
11. the pre-encoded logical GHZ construction, with all recoveries postponed until after acquisition;
12. tensor-channel telescoping giving the full `m kappa s^2` error;
13. the fixed binary readout whose event does not depend on the unknown tube remainder;
14. the integer block choice
    ```text
    m = min{b, floor((2 Delta s)^(-1))},
    ell = floor(N/m),
    ```
    and the two-case proof needed for uniformity when `b` grows;
15. the use of a fully finite Bernoulli lower across independent blocks;
16. the recovery of the v86 regular and opening rows by correct inclusion of strategy classes;
17. the conclusion that parallel and adaptive strategies have matching **local orders**, without claiming equality of distances or absence of adaptive advantages for general fixed channel pairs;
18. the explicit qubit probability law and its parity readout; and
19. the power-law corollary under the actual `O(t^(2q))` remainder hypothesis.

The v87 theorem is therefore a genuine strengthening of the local finite-neighborhood theory. It is not merely a reformulation of the adaptive theorem, and it closes an important logical gap left in r56.

The four-leading-general-journal conclusion nevertheless remains negative. The result is still a local, fixed-object theorem. Its constants and scale interval depend on the base measurement, tangent, support spectrum, correction gap, and remainder allowance. It does not provide a uniform metric equivalence over the ordered-POVM body, a matching arbitrary-pair lower for the midpoint covariance certificate, a complete stratified boundary geometry, full-boundary entropy or learning, or unrestricted higher-order classification. The new block model is precise and useful, but it does not classify every intermediate resource class, such as classical input feedback, separable probe marginals with a shared quantum reference, or general network constraints.

The conceptual mechanisms entering the proof are also largely established: semidefinite tangent geometry, isometric-extension/Bures bounds, fidelity tensorization, entanglement-depth metrology, GHZ phase accumulation, and the Kraus-span/quantum-error-correction dichotomy. The paper's genuine contribution is their finite effect-tube synthesis, the uniform handling of unknown quadratic remainders, the exact support-coordinate trichotomy, and the sharp interpolation in block width. This is strong specialist mathematics, but in my judgment it does not yet attain the breadth and conceptual displacement expected of the four leading general mathematics journals.

There is also a current priority issue. The manuscript's literature audit does not yet compare two directly relevant recent works:

- Z. Huang, J. J. Meyer, T. Nuradha, and M. M. Wilde, *Query complexities of quantum channel discrimination and estimation: A unified approach*, arXiv:2511.10832v2. That paper treats parallel and adaptive query models through channel Bures distance and isometric extensions; its parallel Bures upper is identified there as previously known from Yuan–Fung. The present theorem is not subsumed by that work because it has a specific shrinking measurement tube, a block-width interpolation, a uniform unknown-remainder statement, and matching lower constructions. Nevertheless, the block upper must be compared theorem by theorem with that channel-Bures framework and its antecedents.
- P. Ghosal, P. Halder, A. Patra, and A. Sen, *Quantum hypothesis testing of non-mixed-unitarity: A multifaceted hierarchy of quantum channel discrimination*, arXiv:2609.40355. That paper studies a different composite testing task and asymptotic Stein exponents, but it formalizes block-i.i.d. probes with arbitrary correlations within fixed-size blocks and independent repetition across blocks. It is therefore directly relevant to the resource taxonomy and should be discussed.

Neither source appears to immediately replace the submitted finite-tube theorem. Their omission does, however, prevent the present author-side audit from being considered current or exhaustive.

**Disposition outside the four leading general journals:** the focused quantitative article is a strong candidate for a leading specialist journal in mathematical quantum information, quantum statistics, or operator-theoretic information theory, after the priority, provenance, and exposition revisions below. I would not request another wholesale reconstruction of the historical corpus.

---

## 1. Frozen object and genealogy

The latest General Theta Foundations I object located in the final branch survey is Revision 87. No Revision 88 branch was present when the review branches were created.

The current native branch points to

```text
d4fc44a02ee0585bf9da899239c3f976d75cc9cf,
```

and the response branch points to its direct child

```text
aab076189b7276f6a0b4113b472ea09a7ac640cc.
```

The child adds the four rendered manuscripts and source-bound reconstruction evidence. No separate metadata-only final-head commit or named review-ready branch was present. I therefore treat `aab076...` as the reviewed publication head and `d4fc44...` as the qualified theorem source.

The exact predecessor is completed Revision 86 at `0a7d659...`. The controlling r56 report and pipeline audit are frozen by commit and digest. The v87 mathematical delta is concentrated in:

- `sections/77-nonempty-tangent-neighborhoods.tex`;
- `sections/78-entanglement-width.tex`;
- `editions/operational-introduction87.tex`;
- `editions/current-comparison87.tex`;
- `block_geometry.py` and `block_check.py`;
- the response, proof audit, literature audit, resource ledger, and build records.

The package reports that all predecessor mathematical sections are byte-identical and active. This is important: v87 answers r56 by adding a parallel/block theorem, rather than modifying the previously reviewed tube theorem or product converse.

I reviewed the new sections in full, their inherited premises in Sections 67, 69, 70, 72, 75, and 76, the current introduction and comparison, the exact implementations, the build receipt, the source workflow, the frozen r56 materials, and the wider A/B/C/D dependency ledger.

---

## 2. Nonempty tangent neighborhoods

The quadratic tube theorem is meaningful only when legal perturbations exist. Revision 87 now supplies an explicit sufficient construction.

Let `P_j=supp(E_j)`, let `a` dominate all component operator norms of `H`, and let `lambda` be a positive lower bound for each nonzero effect on its support. The manuscript sets

```text
c        = 1 + 2 a^2/lambda,
s_*      = min{1, lambda/(2a), 1/a},
Lambda_* = c k (1+2k),
```

and defines

```text
F_j^c(s) = (E_j+sH_j+c s^2 I)/(1+k c s^2).
```

For a nonzero support, the support block is bounded below by `lambda/2`, and the Schur correction from the cross block is at most `2a^2 s^2/lambda`. The missing-support block retains the positive first-order opening plus a nonnegative quadratic margin. For a zero effect, the cone condition says directly that `H_j` is positive semidefinite. Summing the numerators gives exactly the common denominator times the identity.

The exact subtraction identity

```text
F_j^c(s)-E_j-sH_j
 = c s^2 (I-kE_j-k s H_j)/(1+k c s^2)
```

implies the stated tuple remainder. This proves nonemptiness for every scale in the displayed interval whenever the allowance is at least `Lambda_*`.

I find the proposition correct. The bound is deliberately coarse and should not be described as a feasibility threshold. The example later in the paper, where allowance `2` works but the generic formula gives `30`, makes this distinction concrete.

The exact rational certificate is also plausibly polynomial in represented input size. For publication, the eigenvalue-lower-bound argument controlling the number of support-floor halvings should remain explicit; the finite implementation cap is not itself a complexity proof.

---

## 3. The block resource model

The new class is carefully defined. A block consists of a complete probe system, its reference, and at most `b` channel inputs. Different blocks begin in a tensor product, although public mixtures with a retained classical record are allowed. Within a block, arbitrary entanglement and arbitrary reference dimension are allowed. No output influences any device input. All outputs and references may be processed jointly after acquisition.

This gives

```text
D_N^[1] = D_N^prod,
D_N^[N] = D_N^par
        = ||M_E^(tensor N)-M_F^(tensor N)||_diamond.
```

The definition is suitable for the theorem. It is not identical to every notion called entanglement depth in the literature. In particular, probe marginals that are separable across groups but share one quantum reference do not satisfy the stated product of complete probe–reference blocks. The phrase “entanglement width” is acceptable only if this distinction remains on the first page and in the theorem statement.

---

## 4. Finite Bures upper for one block and many blocks

In the tangential cases, the paper uses the canonical first-order factor, not the horizontal factor used in the regular adaptive upper. Let `beta_0=||B||`, let `K=k beta_0^2(2+h)`, and put `r=Lambda+K`.

For one block of `n` uses, tensor telescoping of the Stinespring isometries gives a purified displacement at most

```text
(3/2) beta_0 n s.
```

The tube-to-surrogate channel error is at most `n r s^2`. The fidelity–trace inequality converts this to Bures distance at most `s sqrt(rn)`. Thus the block Bures distance is at most

```text
s[(3/2) beta_0 n + sqrt(rn)].
```

This bound is uniform over arbitrary entangled inputs and references inside the block. It retains the quadratic channel error and does not rely on a product-state assumption within the block.

Different blocks do produce product outputs before final processing. Root fidelities therefore multiply, and

```text
2(1-prod f_r) <= sum_r 2(1-f_r).
```

The unhalved trace norm is at most twice the Bures distance. Since `n_r>=1`, one may bound `sqrt(r n_r)` by `sqrt(r)n_r`, and

```text
sum_r n_r^2 <= b sum_r n_r <= bN.
```

This proves the submitted `O(s sqrt(Nb))` upper. A retained public randomization record gives direct sums with common weights, so the same estimate survives mixing.

I find this proof sound. The result should be positioned as a specialized finite-tube consequence of established channel-Bures/isometric-extension methods, not as a new tensor-fidelity principle.

---

## 5. Parallel corrected phase accumulation

For a coherent tangential direction, the inherited support-complement construction supplies a fixed encoding and a fixed completed recovery, depending on `E,H` but not on the unknown remainder. The one-call logical channel satisfies

```text
Phi_E = Id,
||Phi_F-U_s||_diamond <= kappa s^2,
kappa = Lambda + 2||Gamma||_op^2.
```

Revision 87 changes the acquisition architecture. It prepares a logical GHZ state, applies all tensor encodings before any channel call, and applies the tensor recovery only after all calls. The output is therefore `Phi_F^(tensor m)` acting on an entangled logical input, not `Phi_F` composed `m` times. Tensor telescoping yields the full error `m kappa s^2`.

The ideal logical unitary produces phase difference `m s Delta`. The pure-state trace separation is

```text
2|sin(m s Delta/2)|.
```

The submitted lower follows by subtracting the tensor-channel error. A Pauli-`Y` observable on the GHZ span, extended by zero on its orthogonal complement, supplies a legal fixed binary event. Its base probability is `1/2`; the alternative probability has the expected sine gap up to half the trace error.

The readout and all controls are independent of the unknown remainder. No recovered logical output is sent to a later device input. I therefore agree that this is genuinely parallel rather than a deferred sequential protocol.

---

## 6. Uniform block-width lower

The proof chooses

```text
m   = min{b, floor((2 Delta s)^(-1))},
ell = floor(N/m),
x   = m Delta s.
```

After shrinking the fixed scale interval, the floor before the minimum is at least two, `0<x<=1/2`, and `ell>=N/(2m)`. The fixed event on one block has a Bernoulli gap at least `x/(2pi)` after paying the complete `m kappa s^2` remainder. Repeating `ell` independent blocks and applying the finite Bernoulli lemma gives

```text
D_N^[b] >= (1/128) min{1, sqrt(ell) x/(2pi)}.
```

If `m=b`, then

```text
sqrt(ell) x >= Delta s sqrt(Nb/2).
```

If `m<b`, the floor estimate gives `x>=1/4`, hence a fixed positive lower. Since the target rate is truncated at one, this fixed positive value controls a fixed multiple of the target in the saturation regime.

This two-case step is essential. It prevents a hidden loss when `b` grows with `N` or `s`. I find the arithmetic and quantifiers correct.

---

## 7. The three rows and the parallel endpoint

The regular row is bounded below by the inherited product experiment and above by the inherited adaptive horizontal theorem. The support-opening row is bounded below by one fixed impossible-output event and above by the elementary adaptive hybrid estimate. Neither row requires entanglement.

The coherent row combines the new block upper and GHZ-block lower. At `b=N`, the rate is `min{1,Ns}`, which matches the adaptive tube theorem. Consequently

```text
D_N^par(E,F) asymp D_N(E,F)
```

in every fixed quadratic tube, uniformly in `N` and in the permitted remainder.

The corollary is correctly limited to local orders. It does not claim equality of exact distances, equality of optimal testers, equality of perfect-discrimination thresholds, or equality of fixed-pair Chernoff/Stein exponents. General adaptive-versus-parallel channel separations are therefore untouched.

---

## 8. Exact example and higher-order substitution

The explicit projective qubit family has the claimed first derivative and a tube remainder of order `s^2`. The stated GHZ input yields the complete probability law

```text
p_s(z)=2^(-m)[1+(-1)^|z| Im(w_s^m)],
w_s=(1+is)^2/(1+s^2).
```

The base law is uniform and parity is sufficient. The total variation calculation gives the exact sine signal. This is a useful finite illustration of the general lower construction.

The power corollary correctly substitutes `s=t^q` only when the full remainder is `O(t^(2q))`. It does not infer a rate from a leading coefficient alone and does not classify a general zero jet.

---

## 9. Why the top-four threshold is not met

### 9.1 Locality and nonuniformity

The theorem fixes `E,H,Lambda`. Constants can degenerate at changes of support, vanishing correction gap, small nonzero support eigenvalues, or large allowed remainder. No uniform stratified geometry of the full measurement body is obtained.

### 9.2 Remaining global geometry

The midpoint covariance remains a one-sided arbitrary-pair certificate. There is no matching arbitrary-pair lower, global geodesic theorem, complete boundary covering law, or full-boundary minimax learner.

### 9.3 Incomplete resource hierarchy

The block family is an important interpolation, but it does not cover every feedback, network, shared-reference, or causally constrained strategy. The paper should not call it a complete hierarchy of all nonadaptive resources.

### 9.4 Established conceptual mechanisms

The Bures upper, fidelity tensorization, GHZ amplification, semidefinite tangent cone, and Kraus-span/QEC mechanism have substantial antecedents. The novel synthesis is meaningful, but the conceptual center remains close to established quantum information theory.

### 9.5 Learning and constructive gaps

The retained learning theorem is fixed-`k`; its constructive upper carries a `k^3` factor. General efficient public dictionaries, collective readouts, recovery circuits, and robust hardware implementations are not supplied.

### 9.6 Priority remains unsettled

The current literature audit omits directly relevant 2026 work on channel-Bures query bounds and block-i.i.d. discrimination strategies. Independent specialist priority clearance has not been obtained.

### 9.7 Wider Theta programme remains independent

The local discrimination theorem supplies none of the repository's raw local-limit, path large-deviation, global-kernel, exact-shell, Mosco/Nisio, filtering/LAN, changing-filtration, or posterior-contraction gates. It cannot be counted as closure of that programme.

---

## 10. Reproducibility and evidentiary status

The committed receipt records:

- a 42-page primary article;
- a 78-page binary supplement;
- a 41-page structural article;
- a 247-page complete preservation edition;
- 632 current source files;
- 600 predecessor native files;
- 25 regression suites;
- isolated native reconstruction;
- standalone journal-package reconstruction;
- normal/optimized Python agreement;
- no unresolved references, citations, or recorded bad boxes; and
- byte-identical inherited mathematical sections.

Workflow run `37303228873` succeeded. It formed the native source, built all four manuscripts and 25 suites, committed the publication child, and verified that publication child read-only inside the same job.

There is, however, no separate workflow run whose triggering head is the publication SHA `aab076...`, and there is no metadata-only final review object analogous to several preceding revisions. The present evidence is strong but not fully trust-separated: one write-capable workflow both produced and internally verified the reviewed publication. Before external release, the exact publication SHA should trigger a separate read-only reconstruction and receive its own check/status and long-lived artifact. This is a provenance issue, not evidence of a mathematical failure.

The finite suite contains complete small GHZ probability laws and many exact checks. It does not prove the continuum theorem, synthesize the general recovery, or execute a physical device. The current scope flags correctly say so.

---

## 11. Required revisions before specialist submission

1. **Add a theorem-level comparison with Huang–Meyer–Nuradha–Wilde, arXiv:2511.10832v2.** State exactly which parallel Bures/isometric-extension inequalities are inherited or specialized, including the Yuan–Fung antecedent identified there, and isolate what the finite tube and block-width theorem adds.

2. **Add a resource-model comparison with Ghosal–Halder–Patra–Sen, arXiv:2609.40355.** Explain the difference between finite local trace separation and asymptotic composite Stein exponents, while acknowledging the close block-i.i.d. strategy taxonomy.

3. **Obtain an independent specialist priority assessment.** The assessment should cover the support-kernel formula, the finite-tube trichotomy, the block-width interpolation, and the nonempty normalized realization.

4. **Keep “local order” in every parallel/adaptive headline.** Do not abbreviate the corollary to “parallel equals adaptive.”

5. **Clarify “entanglement width” on page one.** It is a product decomposition of complete probe–reference groups, not automatically the standard entanglement depth of probe marginals.

6. **Preserve the unknown-remainder quantifier.** The strongest aspect of the theorem is uniformity over the entire fixed quadratic tube. The statement should continue to say which controls and readouts are independent of the remainder.

7. **Retain the finite remainder in every proof sketch.** The `nrs^2`, `m kappa s^2`, and inherited `Ns^2` terms must not disappear in an informal summary.

8. **Separate the nonempty interval from the discrimination interval.** The constructive `s_*` verifies legality and allowance only; it is not a computed `s_0` for the width theorem.

9. **Do not call `Lambda_*` minimal or canonical.** The explicit qubit example demonstrates its coarseness.

10. **Retain the distinction between the two linear mechanisms.** Support opening is witnessed classically; coherent tangency needs inter-call entanglement or adaptive quantum memory.

11. **Retain the product-converse boundary.** The v86 product upper is not an upper for arbitrary entangled parallel inputs; v87 supplies a different proof for that class.

12. **Add a separate exact-head verification workflow.** Trigger a read-only build on `aab076...`, publish a status/check on that SHA, and preserve its receipt independently of the write-capable builder.

13. **State computational outputs narrowly.** The exact executable classifies represented tangents and constructs one sufficient tube. It does not compute `D_N`, optimal constants, a best tester, or a recovery circuit.

14. **Keep growing-`k` and full-boundary learning open.** The retained fixed-`k` theorem should not be used to broaden the discrimination result into a global learning claim.

15. **Submit the focused quantitative paper separately.** The binary supplement may accompany it; the structural paper is independent; the complete edition should remain archival.

---

## 12. Detailed comments

1. The main theorem should repeat the definition of `||·||_Sigma`; readers should not have to recover it from the preceding section.

2. The theorem's constants are uniform in `N,b,F` but not in `E,H,Lambda`. This should be stated in the abstract exactly as in the theorem.

3. The regular row uses a horizontal factor, whereas the block upper uses the canonical generally nonhorizontal factor. The distinction is mathematically important and should remain explicit.

4. In the block upper, the passage from diamond remainder to Bures distance should cite the exact fidelity–trace normalization used for unhalved trace norm.

5. The phrase “root fidelity multiplies” should always be restricted to the product of independent block outputs, not to the internal calls of an entangled block.

6. The direct-sum argument for public randomization is preferable to a generic appeal to convexity because the retained public record matters.

7. The Pauli-`Y` event is legal after extension by zero. Retain this sentence; otherwise the binary readout can look defined only on the GHZ subspace.

8. The reference bound `2d` is per call. The total pre-existing reference in an `m`-call block grows accordingly.

9. The GHZ construction uses ideal known-direction controls. The theorem does not inherit a gate-complexity guarantee from the exact classical certificate.

10. The block allocation depends on `s`, `b`, and `N`, which are public fixed-pair parameters. It does not depend on the unknown remainder.

11. In the saturated `m<b` case, explicitly note that the target rate is at most one; that is why a fixed positive lower controls it.

12. The qubit example is a useful exact sanity check, but it should not be described as a physical implementation of the general support code.

13. The one-sided cone and its normalized realization should be credited to standard PSD tangent geometry plus the manuscript's coupled normalization, not presented as a new cone theorem.

14. The polynomial support-floor search requires a represented-input eigenvalue lower bound. Keep that argument in the proof rather than leaving it only to the implementation cap.

15. A zero tangent remains higher-order undetermined. The power corollary applies only with its full remainder hypothesis.

16. The resource model permits arbitrary final joint processing. Therefore the lower construction's blockwise binary readout is an admissible special case, not a restriction on the upper class.

17. The comparison with adaptive strategies is order-theoretic in a shrinking neighborhood. It is not a statement that feedback is globally useless.

18. The publication and native commits are unsigned. Source identity is established by Git history and reconstruction, not by verified human authorship.

19. The primary has grown from thirty to forty-two pages. This is still manageable, but the historical learning consequences should not obscure the new discrimination theorem.

20. The complete edition is useful for preservation but should not be sent as a competing journal object.

---

## 13. Whole-program pipeline assessment

The active analytic ordering remains

```text
A1 independent,
A2 -> A3 -> A4 -> C2 -> D1,
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1.
```

The following remain open independently of v87:

- raw unsmoothed local limits;
- stopped-path recovery and large deviations;
- a global past kernel and weak-Harris control;
- exact shell conditioning;
- process CLT and positive Mosco recovery;
- nonlinear Nisio resolvents and graph cores;
- filtering, QMD, and LAN;
- changing-filtration response; and
- labelled posterior contraction.

Accordingly,

```text
historical_A2_replacement = false,
B4_aggregate             = false,
C2_aggregate             = false,
eleven_paper_aggregate   = false,
whole_Theta_program      = false.
```

This separation is correct and must remain intact.

---

## 14. Final assessment

Revision 87 successfully answers the central mathematical criticism of r56 concerning arbitrary entangled parallel inputs. It proves a sharp block-width interpolation, pays all finite tube remainders, identifies the distinct classical-opening and coherent mechanisms, and gives an explicit nonempty neighborhood. I found no fatal defect in these new arguments.

The resulting paper is a serious and potentially publishable specialist contribution. It still falls short of the four leading general mathematics journals because the theorem is local and nonuniform, the conceptual mechanisms have close established antecedents, the global geometry and learning questions remain open, two recent directly relevant literatures are not yet compared, and independent priority clearance is absent.

**Recommendation: reject at the Annals / Inventiones / JAMS / Acta level; encourage a focused submission to a leading specialist journal after the revisions above.**
