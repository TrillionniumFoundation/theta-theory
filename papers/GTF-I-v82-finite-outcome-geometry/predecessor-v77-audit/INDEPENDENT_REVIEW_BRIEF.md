# Independent rereview brief — Revision 77

This brief identifies concrete mathematical and priority questions for an independent specialist. It addresses the v76 report r50. No outside reviewer has been contacted or commissioned, and no independent human specialist priority judgment has been obtained. The author-side source comparison is in `LITERATURE_AUDIT.md`; its preparation does not close the request for independent review. The preceding brief is preserved in `predecessor-v76-audit/INDEPENDENT_REVIEW_BRIEF.md`.

## Controlling material and the revision to be assessed

The controlling report is **General Theta Foundations I, Revision 76 (r50)**, preserved verbatim as `FROZEN_R50_REPORT.md`. Its review branch is `review/general-theta-foundations-i-v76-external-referee-r50-2026-10-04`; the exact reviewed manuscript head is `c041c011274973728a8cc55029192c057696aa43`. The associated proof and pipeline assessment is preserved as `FROZEN_R50_PIPELINE_AUDIT.md`.

Review `quantitative.tex` as the focused quantitative article. Its source graph contains the exact qubit comparison and learning statements needed by the matrix proofs. `main.tex` preserves the complete research edition; `structural.tex` is the inherited structural companion. The history and predecessor directories record the earlier derivation pipeline. Those materials provide provenance and supporting proofs; their unrelated results are not additional conclusions of the quantitative article.

The Revision 77 work branch is `revision/general-theta-foundations-i-v77-r50-response-2026-10-04`. Assess the submitted package at its final recorded publication head. A branch name, reproducible build, finite regression suite, or source hash does not imply an independent human opinion about correctness, priority, or journal suitability.

Revision 77 retains the matrix comparison and entropy theorems and extends the statistical and constructive results to arbitrary input dimension:

| Source object | Domain | Result to assess |
|---|---|---|
| Section 53, **thm:matrixmetric76** | Every pair in the ordered binary effect body, every finite dimension and horizon | Explicit midpoint comparison with a nonadaptive lower bound and adaptive upper bound |
| Section 54, **thm:matrixcover76** | The complete closed matrix interval, fixed dimension | Sharp small-error covering order including its logarithmic factor |
| Section 55, **thm:commonlearn76** | The complete binary qubit body | Common learner used as a subroutine; bias removal, unknown-noise block selection, and scalar converse |
| Section 56, **thm:matrixlearning77** | The complete binary effect body in every dimension | Common learning with at most \(Cd^4N\delta^{-2}\log(d/\eta)\) calls and fixed-dimensional minimax optimality |
| Section 57, **thm:matrixcodec77** | Every finite dimension; supplied Gaussian-rational effects and certified real approximations | Deterministic finite exact encoder and decoder with optimal-order payload |

## Interface and resource conventions

The unknown device is the memoryless consuming qc channel
\[
 \mathcal M_E(\rho)=\operatorname{tr}(E\rho)|1\rangle\langle1|
 +\operatorname{tr}((I-E)\rho)|0\rangle\langle0|,
 \qquad E=E^*,\quad0\preceq E\preceq I_d.
\]
The outcomes are ordered. The device returns a classical outcome and no postmeasurement quantum system or environment. A tester may retain an external reference. Its retained state and adaptive controls remain available between calls. The nonadaptive tester class allows entangled block inputs and a reference, while excluding feedback between calls.

The unhalved operational loss \(d_N\) measures a future experiment with at most \(N\) calls. The training budget \(M\) counts separate calls used to construct a classical estimate. Entangled block length, classical arithmetic, dictionary reconstruction, transmitted payload, and any nonpublic parameter header are additional resources. Training and coding must not be identified: the learner receives a physical unknown device; the supplied-description encoder receives a matrix or a certified coordinate approximation.

All four principal conclusions retain this binary interface. Multiple outcomes, disturbing instruments, residual quantum outputs, and the repository-wide Theta A/B/C/D programme are separate subjects. The inherited contact result also retains its specific subset and regularity hypotheses.

## Exact theorem objects for comparison

### A. The finite-pair midpoint-resolvent comparison

For \(A=(E+F)/2\), \(H=F-E\), \(V=A(I-A)\), define
\[
 Q_N(E,F)^2
 =N\langle H,(L_V+R_V+N^{-1}\operatorname{Id})^{-1}H\rangle_{\rm HS}.
\]
Theorem **thm:matrixmetric76** states
\[
 \frac{\min\{1,Q_N(E,F)\}}{8192d}
 \le d_N^{\rm na}(E,F)
 \le d_N^{\rm ad}(E,F)
 \le\min\{2,8Q_N(E,F)\}.
\]
The constants and the positive horizon cutoff are part of the claim. The theorem covers noncommuting effects, repeated eigenvalues, scalar and deterministic effects, arbitrary support changes, and the projective endpoint. \(Q_N\) is a comparison modulus; neither a triangle inequality for it nor equality with the adaptive optimum is asserted.

**Priority question.** Is this explicit closed-body midpoint form, with a lower estimate of the same finite-horizon order, equivalent to an earlier result under a change of variables? A local Fisher information identity or a generic channel-extension bound should be compared through its actual finite-pair consequences.

### B. Global operational entropy on the effect interval

For each fixed \(d\), uniformly in \(N\ge1\) and \(0<\delta\le\delta_d\), Theorem **thm:matrixcover76** states
\[
 \mathcal C_N(\mathfrak E_d,\delta)
 \asymp_d N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}.
\]
Covering centres are arbitrary legal effects in the same interface; rational legal centres attain this order. The lower bound ranges over all such centres. The constants and error cap may depend on \(d\).

**Priority question.** Does an existing spectral volume or effective metric entropy theorem give this exact combination of the variance tensor, two support endpoints, and the exponent \(\lfloor d/2\rfloor\)? The ordinary Bures pullback under \(E\mapsto E(I-E)\) has a different differential and should not be substituted without an explicit argument.

### C. Common learning in arbitrary input dimension

Theorem **thm:matrixlearning77** supplies one procedure, for every \(d,N\ge1\), \(0<\delta\le\delta_0\), and \(0<\eta\le1/8\), such that
\[
 \sup_{E\in\mathfrak E_d}
 \mathbb P_E\{d_N(\mathcal M_E,\mathcal M_{\widehat E})>\delta\}
 \le\eta,
 \qquad
 M\le Cd^4N\delta^{-2}\log(d/\eta).
\]
The constants \(C,\delta_0\) are absolute. Every record obeys the call bound, and every entangled input block has length at most \(N\). The procedure receives no candidate pair, contrast, bias, eigenbasis, or spectral separation promise. It returns a legal classical estimate throughout the closed effect body.

The converse allows arbitrary reference-assisted adaptive training and bounded public stopping and states
\[
 M\ge cN\delta^{-2}\log(1/\eta).
\]
Consequently the minimax order is \(\Theta_d(N\delta^{-2}\log(1/\eta))\) for each fixed \(d\). There is no matching lower bound for the \(d^4\) factor and no assertion of optimal growing-dimension complexity.

**Priority question.** Do previous tomography guarantees imply this future-loss law with the same horizon, accuracy, confidence, and unknown-noise quantifiers? In particular, compare the simultaneous regularized endpoint calibration and controlled two-dimensional compression with relative-error tomography methods. A sharper analysis of an existing estimator under \(d_N\) would be directly relevant even if its published theorem uses a one-use loss.

### D. A terminating exact matrix codec with optimal-order payload

For integers \(d,N\ge1\) and rational \(0<\delta\le1\), Theorem **thm:matrixcodec77** constructs a finite ordered list of Gaussian-rational legal effects. Every target has an assigned centre within \(11\delta/16\) in \(d_N\). The dictionary has at most
\[
 C_dN^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}
\]
entries. For \(0<\delta\le\delta_d\), its fixed-length index has
\[
 \frac{d^2}{2}\log_2N+
 \lfloor d/2\rfloor\log_2\log(N+2)+
 d^2\log_2(1/\delta)+O_d(1)
\]
bits, matching the covering lower bound up to the additive dimension-dependent constant. This is optimal-order payload; the literal dictionary is not asserted to have minimum possible finite cardinality.

Both parties regenerate the dictionary from public \((d,N,\delta)\). Encoding a supplied Gaussian-rational target and decoding its index terminate using exact arithmetic. The all-real coverage statement has a separate computational interface: certified coordinate approximations at the stated finite precision suffice. No oracle for exact arbitrary real entries is provided. Unused words decode to a specified legal effect, and a nonpublic header is charged separately.

**Priority question.** Does an existing constructive covering result yield this optimal payload for the operational metric, including singular effects, without uncharged target-dependent advice? The terminating grid enumeration is explicit; polynomial running time, practical large-dictionary construction, and arithmetic efficiency are not claimed.

## Detailed proof questions

### Matrix geometry and entropy

1. **Horizontal dilation and adaptive cancellation.** In **lem:matrixpath76**, verify that the prescribed factor derivatives are realized by genuine local qc dilations. Check \(W^*\dot W=0\), \(\dot W^*\dot W=K^2\), and the cancellation of derivatives in distinct slots after arbitrary parameter-independent controls. Confirm the treatment of retained references, purification of classical feedback, and padding of publicly stopped testers. Fujiwara–Imai's gauge formula and its adaptive channel-extension antecedents are credited at this step.

2. **Residual term, finite path, and singular boundary.** Verify the regularized Sylvester split, its linear residual bound, and the operator-concavity estimate along the straight segment. Check the order of operations: integrate the output derivative for each fixed tester, then take the supremum, and finally extend to the closed body. A pointwise Fisher information calculation alone does not establish these quantifiers.

3. **Legal lower witnesses.** Verify diagonal Bernoulli inputs and the two-dimensional compressed pair, including its reference action and the exact inherited qubit hypothesis. A witness may depend on the pair being tested, but not on the unknown true hypothesis. Check that selecting a weighted entry controls the Hilbert–Schmidt sum with the displayed dimension factor.

4. **Uniform operational-ball volume.** Check **lem:matrixlocal76** and **lem:matrixball76**, including comparison of the endpoint and midpoint forms, determinant control, the inward displacement, and a legal ellipsoid fraction independent of the effect's rank. The measure used to count balls must be uniformly controlled at every face, including the singular boundary.

5. **Spectral integration and logarithmic multiplicity.** In **prop:matrixvolume76**, verify the real Hermitian determinant, Weyl Jacobian, ordered endpoint sectors, and balanced-prefix count. Check the lower bound from nested boxes with same-end eigenvalue separation. Determine whether the \(\lfloor d/2\rfloor\) logarithm count has an antecedent under an equivalent spectral parametrization.

### Common learning

6. **The qubit subroutine and its stopping record.** In Section 55, verify the random-sign cancellation of unknown bias, two-plane phase recovery, safe-angle induction, and first-rejection termination in the dyadic block search. Each accepted length must have the claimed amplitude margin. The last accepted length, the public horizon cap, and the treatment of rejected and failed records must define one finite procedure. Fresh experiments following a data-dependent choice require conditional probability estimates.

7. **Simultaneous endpoint calibration.** In **lem:matrixcalibration77**, verify the factor-two Loewner comparisons for \(E+\tau I\) and \(I-E+\tau I\), with \(\tau=N^{-1}\), together with \(\|E-A\|_{\rm op}\le\sqrt\tau\). Check the variance bounds for the diagonal and four superposition probe groups, both quadratures, the rational clipping and inward update, and the induction from one dyadic regularization scale to the next. The basis selection must be deterministic at repeated eigenvalues. The failure allocation and geometric sum must give \(Cd^4N\log(d/\eta)\) calls without an additional \(\log N\) factor.

8. **Variance under a data-selected compression.** In **lem:matrixcompression77**, check the harmonic expression used to combine the two endpoint orders, the constants comparing \(W_E\) and \(W_A\), and the exact compression identity. The noise term \(PE(I-P)EP\) must be bounded at the cutoff scale using \(P(E-A)(I-P)\). The compression may be selected from calibration data; verify that all subsequent samples are fresh and the qubit subroutine is valid conditionally on that record.

9. **Assembling and legalizing the estimates.** In **thm:matrixlearning77**, verify the conversion of a small operational error on each compression to its endpoint quadratic form. Check the weighting and multiplicities of off-diagonal and diagonal coordinates when assembling \(B\); duplicated estimates of a diagonal entry are not assumed consistent. Check the legal rational selection in the known \(g_{N,A}\) norm, its finite grid approximation, and the final conversion to \(d_N\). The classical selection must not query the unknown effect.

10. **Uniform budgets and minimax converse.** Confirm \(\eta/2\) for calibration, \(\eta/(2\binom d2)\) for each pair learner, and pair accuracy proportional to \(\delta/d\). The resulting \(Cd^4N\delta^{-2}\log(d/\eta)\) bound must hold on every record. For the converse, check that scalar effects reduce every permitted training network to common processing of independent Bernoulli bits, including its retained references and stopping record. Verify disjoint future-loss success balls and the full \(\log(1/\eta)\) dependence. This proves fixed-dimensional optimality and does not prove optimality in \(d\).

### Exact coding

11. **Finite construction, legality, and equality cases.** In **thm:matrixcodec77**, check exact Schur elimination at zero pivots for both \(G\) and \(I-G\). Verify that solving the regularized Sylvester equation makes \(Q_N(G,C)^2\) rational and that the strict greedy threshold decides every equality case. Check the inward move, nearest-grid rounding, tie convention, and the \(11\delta/16\) error bound. For certified real approximations, verify the coordinate precision sufficient to retain legality and the same guarantee.

12. **Size, replay, and charged resources.** Check that distinct retained centres yield disjoint operational balls through the actual metric \(d_N\), without using a triangle inequality for \(Q_N\). Verify the cardinality bound from the volume theorem, decoder reconstruction from public parameters, fixed-length padding, and unused-word behavior. Compare payload size separately from the ambient-grid bound \((K+1)^d(2K+1)^{d(d-1)}\), storage, and rational arithmetic. Resource cutoffs in a partial enumeration must be reported as incomplete constructions. Small regression cases do not certify complete large dictionaries or the continuum theorem.

## Competing results and the comparisons requested from a specialist

The exact primary links, version locators, loss normalizations, and formulas are in `LITERATURE_AUDIT.md`. The comparisons below specify the judgments still requested.

| Antecedent | Exact comparison requested |
|---|---|
| **MB67:** Mele–Bittel, arXiv:2512.10214v3, Theorem I.1, Theorems III.2–III.3, Remark III.4, Lemmas III.7–III.8, Corollary III.9, Proposition IV.17 | Compare one-use operator-norm learning, parallel input/reference pairs, collective Choi-state processing, arbitrary effect ranks, dimension dependence, and confidence. The restricted-confidence simplification and arbitrary-confidence amplification must both be included. Assess whether a stronger future-loss analysis recovers the current horizon law. |
| **ZRK76:** Zambrano–Ramos-Calderer–Kueng, _Quantum_ **10** (2026), 2162; arXiv:2507.04500v3, Definition 1, Theorem 2 equation (13), Theorem 9 equation (43) | Compare one-use worst-input outcome variation with the future loss. Keep its known-input, nonadaptive single-copy training restriction attached to the lower bound. Compare both accuracy and confidence after specializing to two outcomes. |
| **FI76, DKG67, DM76, KGAD76:** Kraus gauges and channel extension | Verify that established differential constructions are correctly credited at the horizontal cancellation step. Identify whether the binary regularized Sylvester split and global midpoint form have an equivalent prior statement. |
| **YF76 and SD76:** Yuan–Fung, PDF v3 Section III equation (26); Sieniawski–Demkowicz-Dobrzański, Section IV.A equations (14)–(22) | Distinguish the parallel integration antecedent from the later adaptive metrological application. Assess the additional explicit finite-horizon variance bound and its matching lower witnesses. |
| **Dittmann76 and SZGeom76:** inverse Sylvester Bures forms and spectral volume | Compare tensors with their actual tangent variable and domains. Assess the operational-ball proof and the nested two-endpoint logarithmic asymptotic, together with the shared eigenvalue-integration method. |
| **FM75, SZ74, PPKK74, PPKKO72, KPP76, DBSA76:** projective and nonprojective measurement discrimination | Compare retained-reference access, exact versus constant-factor statements, ordered outcomes, finite use, and rank restrictions. Keep the number of hypotheses separate from the number of outcomes. |
| **BDPS76, HB76, KLY76, Gutoski66:** measurement learning and retrieval, multiscale phase methods, convex strategy discrimination | Compare classical estimates with stored quantum programmes, inherited phase techniques with the proven safe-angle and confidence bounds, and pair-dependent discrimination with one common estimator. Account for the KLY76 erratum. |

The direct hybrid conversion from a published one-use estimate is only a sufficient budget for future loss. It is not a lower bound on that estimator's future-loss performance. No claim of general adaptive advantage follows from comparing those certificates. A specialist should identify a matching theorem, a derivation with matching quantifiers, a narrower overlap, or an unresolved comparison, with the relevant source and hypotheses stated explicitly.

## Requested independent outcome

The independent assessment should address the four exact objects above and the hypotheses linking them. For each, report whether the statement is correct under the specified interface, whether a cited antecedent or another primary source already implies it, and which precise mathematical increment remains after attribution. In particular, assess the new endpoint calibration and the finite exact code independently of the broader history of the paper.

The current status is **review material prepared; independent human specialist judgment pending**. This brief records neither an endorsement nor a priority clearance. It does not change the mathematical claims into journal-level or repository-wide closure claims. The submitted source and evidence package should allow a subsequent referee to make those assessments on a concrete, reproducible manuscript.
