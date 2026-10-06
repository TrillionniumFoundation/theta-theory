# Referee Report — General Theta Foundations I, Revision 84 (r54)

**Focused quantitative manuscript:** *Finite-Use Geometry and Learning of Ordered Quantum Measurements*  
**Current auxiliary supplement:** *Binary Foundations and Auxiliary Proofs*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I*  
**Repository:** `TrillionniumFoundation/theta-theory`  

**Reviewed branches:**
- `revision/general-theta-foundations-i-v84-support-native-2026-10-05`
- `revision/general-theta-foundations-i-v84-support-publication-2026-10-05`
- `revision/general-theta-foundations-i-v84-support-review-ready-2026-10-05`
- `revision/general-theta-foundations-i-v84-r53-response-2026-10-05`

**Reviewed exact final head:** `9ee14476f539a38f2f45f9bd4ed99a658a7eb14d`  
**Candidate publication:** `71681519882357a080106d571f478f5f13b9e541`  
**Qualified native source:** `bd90865ed1d755399bcf047ec4d353cac0f48206`  
**Completed predecessor:** Revision 83, `58cbb2608fa65f1fba1b5d56ab1fd55dfd9dacd7`  
**Controlling external report:** v83/r53, `0077ff4b39633c3e9b6947e89f0bbcdd8e5ffe2e`  
**Controlling proof/pipeline audit:** v83/r53, `89c8c9cb3d1494d90c3d449d981a7424665256ab`  
**Source qualification workflow:** `37269000936`, conclusion `success`  
**Exact-head read-only reconstruction:** `37269932771`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v84-support-geometry-external-referee-r54-2026-10-05`  
**Date:** 5 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 84 is a serious and mathematically useful response to r53. It is also a materially better journal object than Revision 83: the primary article has been reduced from ninety pages to twenty-four pages, the complete auxiliary binary corpus is separated into a reconstructible seventy-eight-page supplement, and the structural article remains an independent object. The principal new theorem is no longer merely a one-sided covariance upper. It gives a complete support description of the covariance kernel and a finite-angle classification on every fixed unitary orbit.

I did not find a fatal mathematical gap in the new Sections 69–71. In particular, the following proof components are coherent in the form submitted:

1. the real-linear parameterization of the complete covariance kernel, including zero effects and arbitrary rank patterns;
2. the exact dimension formula
   ```text
   dim ker(C_E|_T)
     = d^2 - dim(W_E) + sum_j (d-rank(E_j))^2;
   ```
3. the unitary range criterion
   ```text
   i[G,E] in Ran(C_E|_T)  iff  G in W_E;
   ```
4. the square-root finite-use upper and product-input lower when the tangent lies in the covariance range;
5. the support-complement code, Knill–Laflamme correction, and finite-angle logical-channel estimate in the linear regime;
6. the explicit accumulated error
   ```text
   ||Phi_t^m-U_t^m||_diamond <= 4 m t^2 ||G||_op^2;
   ```
7. the choice of the integer number of calls in the finite-angle lower, including its floor and small-angle bookkeeping;
8. support-span monotonicity under classical output processing;
9. the transported-weight regularized data-processing theorem; and
10. the exact rational support-span decision and Gram projection.

The strongest new operational statement is the trichotomy, for every fixed measurement `E` and generator `G`,

```text
D_N(E,E(t)) = 0                         on stationary orbits,
D_N(E,E(t)) = Theta_{E,G}(min(1,sqrt(N)|t|))  if G in W_E and the orbit moves,
D_N(E,E(t)) = Theta_{E,G}(min(1,N|t|))        if G not in W_E,
```

on a two-sided angle interval depending on `E,G`. This is a genuine finite-pair trace-distance theorem, not merely an inference from asymptotic quantum Fisher information. The manuscript correctly states that the tester is pair-dependent, that its ideal recovery depends on the known pair, and that no general learner or efficient recovery synthesis follows.

The four-leading-general-journal conclusion nevertheless remains negative for reasons of **scope, priority, and general mathematical reach**.

The exponent dichotomy and its quantum-error-correction mechanism are the measurement-channel specialization of the established Hamiltonian-not-in-Kraus-span criterion. Zhou–Jiang already provide the linear-versus-quadratic asymptotic channel-metrology criterion and error-correction attainability. Revision 84 contributes a useful covariance-support identity, an explicit kernel parameterization, and a direct finite-angle trace-distance ledger, but it does not replace the conceptual source of the dichotomy. The complete arbitrary-pair boundary geometry remains one-sided. There is still no matching lower certificate for the midpoint covariance on the whole ordered-POVM body, no complete boundary volume or entropy theorem, no full-boundary common learning law, and no growing-outcome minimax classification.

Moreover, the priority audit is not yet current. The repository states that the full text of Yoshida–Okigami–Posta–Grinko, arXiv:2609.39280, could not be obtained. At the time of this review, the complete arXiv HTML is available at `https://arxiv.org/html/2609.39280` and is dated 4 October 2026. Its main results concern collective tomography of invariant states and covariant channels, parameter-count query laws, and gate-efficient implementations of the Hayashi measurement. I did not find an immediate theorem there that subsumes the present fixed-pair support trichotomy, but the comparison is no longer unavailable and should be carried out at theorem level. More importantly, the manuscript still lacks an independent specialist priority assessment of the support-kernel formula and its relation to existing channel-metrology and operator-valued-measure geometry.

**Disposition outside the four leading general journals:** the focused quantitative article is a strong candidate for a leading specialist journal in mathematical quantum information, provided the authors update the priority comparison, make the exact novelty boundary more prominent, and keep the main theorem package editorially self-contained. I would not request another wholesale reconstruction of the mathematics.

---

## 1. Frozen object, genealogy, and material reviewed

The latest General Theta Foundations I revision located is Revision 84. No Revision 85 branch was present in the final branch survey.

The review-ready and response aliases identify

```text
9ee14476f539a38f2f45f9bd4ed99a658a7eb14d.
```

This exact final head is a metadata-only child of publication commit

```text
71681519882357a080106d571f478f5f13b9e541,
```

which is a direct child of qualified native source

```text
bd90865ed1d755399bcf047ec4d353cac0f48206.
```

The final-head commit adds only `GENERAL_THETA_FOUNDATIONS_I_V84_FINAL_HEAD_REQUEST.json`; it does not change theorem source. The publication commit adds the four rendered documents and source-bound evidence without changing the qualified native mathematical source.

Revision 84 is twelve commits beyond the exact reviewed v83 head. The mathematical delta is concentrated in:

- `sections/69-support-kernel.tex`;
- `sections/70-finite-angle-orbits.tex`;
- `sections/71-transported-regularization.tex`;
- the focused current introduction and literature comparison;
- the exact support decision and transported-energy implementation; and
- current source, preservation, response, and build records.

I reviewed, in particular:

- `quantitative.tex`, `supplement.tex`, `structural.tex`, and `main.tex`;
- the current introduction and comparison section;
- Section 67 as the covariance premise of the new results;
- Sections 69–71 in full;
- Sections 65–66 and 68 insofar as they remain current learning consequences;
- the retained binary finite-pair and Bernoulli lower results invoked by the orbit theorem;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `RESOURCE_LEDGER.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- `support_geometry.py`, `support_check.py`, and `SUPPORT_SCHEMA.md`;
- the source, page, theorem-location, preservation, and regression receipts;
- both r53 reports;
- the source-qualification and exact-head workflows; and
- the frozen repository-wide A/B/C/D dependency ledger.

This review is not a formal proof-assistant verification and is not an exhaustive novelty search. The statements below distinguish proof correctness, finite regression evidence, priority, and journal significance.

---

## 2. Executive assessment of the new mathematics

### 2.1 Complete support description of the covariance kernel

Let

```text
P_j = supp(E_j),   Q_j=I-P_j,
W_E = sum_j P_j H_d P_j,
A_E = W_E^perp.
```

The variance identity from v83 says that a zero-sum tuple `K` lies in the covariance kernel precisely when

```text
P_j K_j = P_j S_E(K)
```

for every outcome. Writing `S_E(K)=B+iA` with `A,B` Hermitian forces `P_j A P_j=0`. The support, off-support, and cross blocks of `K_j-B` are then exactly

```text
i[P_j,A] + Z_j,   Z_j=Q_j Z_j Q_j.
```

Subtracting the tuple mean enforces the zero-sum condition. Conversely, the identity

```text
sum_j E_j(i[P_j,A]+Z_j)=iA
```

reconstructs the kernel condition. If the mean-subtracted tuple vanishes, all pre-mean components coincide with one Hermitian matrix, while the same matrix equals `iA`; hence both vanish. This proves injectivity.

I find this argument correct. It handles zero effects without inversion, records all missing-support blocks, and explains why the kernel depends on supports rather than the nonzero eigenvalues of the effects.

### 2.2 Unitary tangent and covariance range

For `H_j=i[G,E_j]`, the missing-support blocks vanish. Pairing `H` with the kernel tuple removes the mean and the `Z_j` terms. The remaining calculation gives

```text
<H,K(A,Z)> = -2 tr(GA).
```

Since the covariance is self-adjoint in finite dimension, its range is the orthogonal complement of its kernel. Therefore

```text
H in Ran(C_E|_T)  iff  G in W_E.
```

The sign and factor two are consistent. The criterion also implies that a stationary generator belongs to the support span. The manuscript correctly distinguishes this range statement from an operational lower bound.

### 2.3 Square-root branch of the orbit theorem

When `H` is nonzero and belongs to the covariance range, the pseudoinverse energy is finite. Unitary conjugation transports both covariance and tangent, so the energy is constant along the orbit. The regularized path upper is therefore `O(sqrt(N)|t|)`.

For the lower, some component `H_j` is nonzero and hence has a vector with nonzero expectation. The corresponding one-label event has a first-order Bernoulli gap. At a two-sided unitary path, a nonzero first derivative cannot occur at a scalar probability endpoint, so the local Bernoulli experiment is nondegenerate. The inherited finite product bound gives the matching `Omega(min(1,sqrt(N)|t|))` lower with constants depending on `E,G`.

I find this branch correct.

### 2.4 Support-complement code

For `G` outside `W_E`, the orthogonal residual

```text
A=G-Pi_{W_E}G
```

is nonzero and traceless because `I` belongs to `W_E`. Its positive and negative parts have equal trace and define states `rho_+` and `rho_-`. The compression identity

```text
P_j rho_+ P_j = P_j rho_- P_j
```

holds for every support.

Flagged purifications of these two states define a logical qubit. The orthogonal flags kill off-diagonal code matrix elements, and the compression identity equalizes the diagonal matrix elements for every operator in `P_j M_d P_j`. Since the Kraus-product span of the classical measurement channel at label `j` is exactly this full support block, the Knill–Laflamme conditions hold.

The recovery acts on the actual classical label and the retained external reference. It does not use the discarded input or an inaccessible Stinespring environment. Diagonalizing the correction Gram matrix and completing the channel on the orthogonal complement gives a legitimate CPTP recovery. The reference dimension bound `2d` is consistent with the two flagged `d`-dimensional purifications.

The logical generator is diagonal and has positive gap

```text
Delta = tr(G(rho_+-rho_-)) = ||A||_HS^2 / tr(A_+).
```

I find this construction correct. It is existential and pair-dependent; no efficient synthesis follows.

### 2.5 Finite-angle corrected-channel estimate

If the completed corrected channel has Kraus operators `V_l` and corrects the code exactly, then

```text
V_l J = c_l I,
sum_l conjugate(c_l) V_l = J^*.
```

These identities give equality of the zeroth and first derivatives of the actual corrected channel and the logical unitary channel. The second derivative of unitary conjugation has diamond norm at most `4||G||_op^2`; Taylor’s integral remainder contributes `2t^2||G||_op^2` to each channel. Their difference is therefore at most `4t^2||G||_op^2`, and telescoping `m` compositions gives the submitted accumulated error.

Starting from an equal logical superposition, the ideal state separation is

```text
2|sin(m t Delta/2)|.
```

Subtracting the correction error yields the explicit finite-pair lower. The choice

```text
m=min{N,floor(1/(|t|Delta))}
```

is valid on the stated small-angle interval. The quantity `x=m|t|Delta` lies below one and above one half of `min{1,N|t|Delta}`. The additional angle cap makes the quadratic error at most `x/pi`; the sine bound then gives the displayed positive constant.

I find the finite-angle bookkeeping correct. The result is local with constants and an angle interval depending on the fixed pair. It is not uniform over support degenerations.

### 2.6 Examples and output processing

The full-rank, rank-one, informationally complete, and projective corollaries follow directly from the support span. In particular, for a rank-one POVM the support span is the real effect span, whereas for higher-rank effects it contains full matrix blocks and can be strictly larger.

For a column-stochastic output map, each processed positive effect has support containing every positively weighted original support. Since each original label enters at least one output row, `W_E` is contained in `W_{TE}`. Thus a moving square-root orbit can become stationary after processing but cannot become a linear orbit. Reversible splitting gives equality of support spans. This is the precise interpretation that should be retained in prose.

### 2.7 Transported-weight regularization

The public probability vector `w` defines the scalar measurement covariance

```text
(B_w K)_j = w_j(K_j-sum_l w_l K_l).
```

Both the physical covariance and this scalar covariance obey the same Jensen-square comparison under a stochastic output channel when `w` is transported to `Tw`. The linear pairing also transports. Taking the variational supremum gives

```text
E_{TE,Tw,tau}(TH) <= E_{E,w,tau}(H),
```

including infinite values. A stochastic left inverse gives equality.

The operational comparison uses only

```text
0 <= B_w <= w_max I.
```

With `tau=1/(N w_max)`, inverse order compares the transported ridge with the original Euclidean ridge. For uniform weights the exact parameter is `tau=k/N`, not `1/N`. The manuscript states this correctly and does not retroactively claim that a freshly uniformized ridge is monotone under arbitrary processing.

### 2.8 Exact represented-input computation

For Gaussian-rational effects, rational column bases give rational support projectors. A compressed rational Hermitian basis spans `W_E`; real coordinates are used for rank selection, while the Hilbert–Schmidt Gram system is used for metric projection. Exact commutators decide stationarity. Fraction-free elimination and determinant bounds support polynomial represented-input bit complexity.

The certificate determines a local regime for one known orbit. It does not compute `D_N`, construct the optimal tester, synthesize the recovery, or execute a device protocol. The implementation and schema preserve these distinctions.

---

## 3. Relation to Revision 83 and the complete pipeline

Revision 83 established the coupled covariance, its positive projection factorization, the complete-body adaptive upper, its exact binary restriction, a noisy-projector crossover, exact rational evaluation, and search-free affine legalization. Revision 84 uses this material rather than replacing it.

The new support theorem closes one important caveat from r53: the covariance kernel is no longer described only through the zero-operator/PVM characterization. Every null direction is now explicit. The unitary orbit theorem also extends the single noisy-projector example to every fixed unitary orbit and turns the regularized `sqrt(N)` versus `N` tangent decomposition into an actual finite-pair statement.

It does **not** close the principal general-boundary questions:

- arbitrary rank-changing pairs are not classified from below;
- the midpoint covariance is not proved equivalent to operational distance on the full body;
- complete-boundary entropy is open;
- complete-boundary common learning is open;
- growing-`k` dependence is open;
- entropy-optimal dictionary construction may be exhaustive; and
- general recovery/readout synthesis is not efficient or executed.

The finite-dimensional measurement results do not establish any independent A/B/C/D analytic programme gate. The historical A2 replacement, B4 aggregate, C2 aggregate, eleven-paper aggregate, and whole-program aggregate remain false. This separation is correct and should remain explicit.

---

## 4. Priority and literature boundary

The manuscript now makes several important corrections to its novelty language:

- the Hamiltonian-not-in-Kraus-span criterion is credited to Zhou–Jiang;
- the quantum-error-correction principle is credited to Knill–Laflamme;
- the finite-use upper is related to channel-extension and adaptive discrimination work;
- measurement Fisher/frame geometry and operator-valued kernel embeddings are distinguished from the present varying-measurement problem; and
- tomography primitives are not claimed new.

Nevertheless, independent priority is still unresolved.

The closest conceptual antecedent is the Zhou–Jiang dichotomy. The submitted theorem strengthens its presentation for this interface by identifying the Kraus-product span with the support span, deriving the entire covariance kernel, and proving a direct finite-angle trace-distance estimate. Whether the exact support-kernel parameterization or an equivalent quotient-space formula already appears in channel-metrology, sufficiency, operator-algebraic statistics, or measurement geometry has not been independently cleared.

The repository’s statement that the newest covariant-learning full text is unavailable is now stale. The full HTML of arXiv:2609.39280 is accessible. Its principal channel results concern known-symmetry collective learning, parameter-count query laws, and efficient implementation of covariant measurements. Those results do not immediately imply the present pair-discrimination theorem, but a current theorem-level comparison is required.

For a four-leading-general-journal submission, an author-side targeted search is insufficient. A specialist should be asked to assess at least:

1. whether the support-kernel bijection is already implicit in the HNKS semidefinite formulation;
2. whether the finite-angle corrected-channel lower is a standard nonasymptotic corollary of existing metrological error-correction proofs;
3. whether transported scalar-covariance regularization has an established form in information geometry or statistical experiments; and
4. whether the present fixed-pair result has consequences outside the ordered-measurement interface.

---

## 5. Journal architecture and exposition

The twenty-four-page primary is a major improvement over v83. The support kernel and orbit theorem now lead the paper, and revision history is kept outside the journal prose.

However, the quantitative proof package is still approximately one hundred and two pages once the seventy-eight-page binary supplement is included. Several main-text consequences rely on externally numbered supplement theorems. This is acceptable as a source package, but a reader should not need to reconstruct the historical binary programme to verify the new support/orbit theorem.

I recommend that the final specialist submission keep in the primary article a compact, self-contained statement of every imported prerequisite actually used:

- the exact covariance factorization and variance identity;
- the complete-body path upper;
- the finite Bernoulli product lower with the relevant endpoint qualification; and
- the measurement-channel interface and stopping convention.

The remainder of the binary corpus may stay in the supplement. The structural companion should remain a separate submission and should not be used to amplify the significance of the measurement paper.

---

## 6. Required revisions before specialist submission

### R01. Update the covariant-learning comparison

The full text of arXiv:2609.39280 is now available. Replace the “full text unavailable” statement by a theorem-level comparison of its state/channel models, losses, query architecture, parameter dimensions, and gate-efficiency claims with the present fixed-pair future-use problem.

### R02. Obtain independent priority assessment

Seek a specialist opinion specifically on the support-kernel formula, the finite-angle orbit theorem, and the transported ridge. Do not infer priority from a repository search or successful build.

### R03. State the novelty boundary in the first theorem discussion

Make explicit immediately after the trichotomy that the exponent dichotomy and QEC mechanism are established metrological principles; the submitted additions are the complete support-coordinate kernel, the covariance-range identification, and the direct finite-angle trace estimate for measurement channels.

### R04. Keep the arbitrary-pair limitation visible

The global covariance theorem remains one-sided. Do not let “complete-body” or “full support” be read as a two-sided arbitrary-pair boundary classification.

### R05. Keep fixed-pair constants explicit

State in every headline version that `c,C,t0` depend on `E,G` and may degenerate as supports, gaps, or the orthogonal residual vary.

### R06. Clarify output processing prose

Classical processing can make a moving square-root orbit stationary. The invariant statement is that it cannot turn a square-root orbit into a linear orbit when the processed orbit remains nonconstant.

### R07. Give a compact prerequisite lemma in the primary

Include the exact finite Bernoulli product estimate used in the square-root lower, or state it fully with a precise supplement reference and the local nonendpoint condition.

### R08. Separate pair discrimination from learning

Retain the statement that the correction code and recovery depend on known `E,G`. They are not admissible as advice to the unknown-measurement common learner.

### R09. Preserve the ideal-control qualification

The linear lower is an existence theorem with ideal encoding/recovery. No gate complexity, robustness to approximate controls, or physical implementation has been proved.

### R10. Preserve computational scope

Polynomial support decisions, covariance evaluation, and affine legalization do not imply polynomial dictionary construction, recovery synthesis, or general collective-readout synthesis.

### R11. Keep growing-`k` open

The balanced learner remains sharp only for fixed `k`; the displayed upper has a `k^3` factor and the lower comes from a binary subfamily.

### R12. Keep the primary/supplement dependency transparent

Provide a short dependency table identifying precisely which supplement results are logical premises of the primary and which are merely preserved historical material.

### R13. Distinguish proof from regression

The BB84 symbolic replay and the 280 positive checks are useful exact tests. They are not continuum proofs, physical executions, or synthesis of the general recovery.

### R14. Preserve exact release identities

Bind any subsequent revision to its own native source, publication, and exact final head. Do not reuse v84 receipts after source changes.

### R15. Preserve the independent programme boundary

Do not promote any A/B/C/D aggregate flag on the basis of this finite-dimensional measurement theorem.

---

## 7. Detailed comments

### D01. Real versus complex spaces

`W_E` is a real subspace of Hermitian matrices. The kernel parameter `A` is Hermitian, while `i[P_j,A]` is Hermitian. This convention is correct and should be reiterated whenever dimensions are counted.

### D02. The support span is not an algebra

The current warning is important. For higher-rank effects, `W_E` need not be the effect span and need not be closed under multiplication.

### D03. Zero effects

The convention `supp(0)=0` is consistently handled. The term `(d-r_j)^2` correctly contributes a full missing-support block for a zero effect.

### D04. Decomposition of `S_E(K)`

The proof must retain the fact that `S_E(K)` need not be Hermitian. The decomposition `B+iA` and compression argument are essential, not cosmetic.

### D05. Kernel injectivity

The step identifying a common Hermitian matrix with `iA` is the cleanest part of the injectivity proof. Keep it explicit.

### D06. Range criterion

The range is the orthogonal complement of the kernel because the covariance is self-adjoint in finite dimension. No closed-range issue is hidden.

### D07. Stationary generators

The proposition implies that every generator commuting with all effects lies in `W_E`. This nonobvious consequence is valid and may be mentioned as a corollary rather than left implicit.

### D08. Product lower

The square-root lower uses a single fixed input and one coarse-grained label event. It is not an entangled or adaptive lower construction.

### D09. Probability endpoints

A nonzero two-sided first derivative of a unitary probability curve cannot occur at probability zero or one. This explains why the inherited Bernoulli constant is legitimate locally; one sentence would help.

### D10. Actual output recovery

The recovery acts on the label and retained reference. The proof correctly does not expose the measurement environment.

### D11. Kraus representation

The product span for one label is `P_j M_d P_j` because `sqrt(E_j)` is invertible on its support. This should remain explicit in the closest-theorem comparison.

### D12. Flagged purifications

Orthogonal flags eliminate off-diagonal logical matrix elements. The dimension `2d` is a per-call reference bound, not the size of a compiled control circuit.

### D13. Recovery completion

Assigning a fixed state on the orthogonal complement is necessary to obtain a CPTP channel on the entire output space. The manuscript includes this and should not abbreviate it away.

### D14. Logical gap

`Delta` depends on the Hilbert–Schmidt residual and on `tr(A_+)`. It may become small near the support span; no uniform lower is available.

### D15. Derivative identity

Exact correction gives both `V_l J=c_l I` and the summed adjoint identity needed for the first derivative. The current proof is adequate.

### D16. Diamond-norm constants

The factor four is obtained by comparing two second-order Taylor remainders. It is conservative, not claimed optimal.

### D17. Composition error

The `m`-fold estimate is an ordinary telescoping bound for channels. It does not assume error independence.

### D18. Choice of `m`

The angle condition ensures `floor(1/(|t|Delta))` is at least two, so the chosen number of calls is positive. This can be recorded explicitly.

### D19. Sign of `t`

All operational lower estimates use `|t|`; the logical trace distance is symmetric. The submitted two-sided interval is consistent.

### D20. Full-rank example

One positive-definite effect makes `W_E=H_d`, so every moving orbit is square-root. This is a useful sanity check.

### D21. Rank-one informational completeness

For rank-one effects, `P_j H_d P_j` is one-dimensional and agrees with the real effect span. This equivalence fails at higher rank.

### D22. Projective measurements

For a PVM, the support span is the block-diagonal commutant; every moving orbit lies in the linear regime. This is consistent with the zero covariance operator.

### D23. Support processing

The support of a positive weighted sum contains the support of each positive summand. The proof does not rely on commutativity.

### D24. Extended energy

The variational definition correctly handles zero transported weights and infinite values. Avoid replacing it by an ordinary inverse in singular cases.

### D25. Transported versus refreshed weights

The same `tau` and the transported vector `Tw` are essential. A new uniform vector on the output alphabet defines a different ridge.

### D26. Uniform normalization

For uniform weights, the correct scalar-ridge coefficient is `k/N`; this reproduces the original `I/N` ridge on the zero-sum tangent space.

### D27. Exact projection

Real coordinates select an independent basis, while the Hilbert–Schmidt Gram matrix performs the orthogonal projection. Conflating these two matrices would be an error; the implementation keeps them separate.

### D28. Resource cap

The support certificate rejects an exceeded cap rather than returning a partial or heuristic classification. This is the correct contract.

### D29. Linked supplement

Cross-document references reconstruct successfully, but the logical dependency graph should be visible to a human reader without consulting preservation metadata.

### D30. Strongest message

The most defensible contribution is: a normalized covariance admits a complete support-kernel description, and on known unitary measurement orbits that description exactly determines the finite-use standard-versus-Heisenberg trace-distance scale. This is narrower and stronger than a general claim about optimal POVM learning.

---

## 8. Reproducibility and evidence

The current build receipt reports:

- primary quantitative article: 24 pages;
- binary supplement: 78 pages;
- structural article: 41 pages;
- complete preservation edition: 232 pages;
- 22 exact regression suites;
- 280 new positive support checks and 18 negative controls;
- isolated native reconstruction;
- independent linked journal-package reconstruction;
- no unresolved references or citations; and
- normal/optimized Python agreement.

The source qualification run and exact-head read-only run both completed successfully. The exact-head job checked out `9ee14476...`, reconstructed all four documents, reran exact regressions, rebuilt the linked package, and preserved a receipt.

These facts establish object identity and reproducibility. They do not establish theorem truth, priority, physical implementation, authorship signature, or journal significance.

---

## 9. Final assessment

Revision 84 contains a coherent new theorem package. The complete support-kernel formula is elegant, the range criterion is exact, and the finite-angle orbit proof converts an asymptotic metrological dichotomy into a direct operational statement with explicit error accumulation. The transported ridge is also cleanly scoped.

For a leading specialist journal, these results are potentially publishable after the priority and exposition revisions above. For Annals, Inventiones, JAMS, or Acta, the work remains too specialized and too dependent on a known metrological dichotomy, while the genuinely general arbitrary-pair boundary, entropy, and growing-outcome problems remain open.

**Recommendation: reject at the four-leading-general-journal level; encourage a focused specialist submission after revision.**
