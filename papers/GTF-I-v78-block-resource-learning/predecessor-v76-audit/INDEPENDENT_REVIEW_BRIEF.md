# Independent rereview brief — Revision 76

This brief identifies concrete mathematical and priority questions for another referee. It addresses the v75 report r49. No outside reviewer has been contacted or commissioned, and the independent specialist opinion requested by the preceding reports has not been supplied. The previous brief is preserved in `predecessor-v75-audit/INDEPENDENT_REVIEW_BRIEF.md`.

## Manuscripts and controlling report

Review `quantitative.tex` as the quantitative article and `structural.tex` as the separate structural article. The complete research edition retains the derivation history. Structural statements remain inherited and require their own assessment.

The controlling report is **General Theta Foundations I, Revision 75 (r49)** on review branch `review/general-theta-foundations-i-v75-external-referee-r49-2026-10-04`. It reviewed final v75 head `16b78c8edef566300ea21300908854ad83455879`. The report found no fatal defect in the biased-qubit package but requested broader mathematics, additional measurement-discrimination comparisons and independent priority scrutiny. Revision 76 adds three results with distinct quantifiers:

| Result | Domain | Finite statement |
| --- | --- | --- |
| Section 53, **thm:matrixmetric76** | Every ordered binary effect \(0\le E\le I_d\), every fixed \(d\) | Global midpoint comparison for all pairs and \(N\ge1\), with matching nonadaptive lower tests and an adaptive upper bound |
| Section 54, **thm:matrixcover76** | The entire matrix interval in each fixed \(d\) | Covering order \(N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}\) in a dimension-dependent small-error range |
| Section 55, **thm:commonlearn76**, **cor:learncode76** | The entire ordered binary **qubit** body | One unknown-device learner, minimax training cost \(\Theta(N\delta^{-2}\log(1/\eta))\), legal classical estimate, and subsequent finite coding |

Here \(N\) in the loss is a future discrimination horizon. It is not the training budget. All unknown-device calls are memoryless and consuming, with ordered classical outcomes. References and coherent intermediate control are allowed to discrimination testers; the learning construction uses trusted preparations of finite entangled blocks and classical feedback.

## Matrix comparison: questions for a detailed proof check

1. **Explicit quantity and endpoints.** For \(M=(E+F)/2\), \(H=F-E\), \(V=M(I-M)\), check
   \[
   Q_N^2=N\langle H,(L_V+R_V+N^{-1}\mathrm{Id})^{-1}H\rangle
   \]
   and the constants in **thm:matrixmetric76**. Its quantifiers include noncommuting effects, repeated eigenvalues, scalar effects, deterministic effects and arbitrary support changes. The positive \(N^{-1}\) term must be retained.

2. **Horizontal derivative.** Check the binary qc dilation and its Sylvester equation involving \(\sqrt{E(I-E)}\). Verify \(W^*\dot W=0\), the expression for \(\dot W^*\dot W\), and cancellation after arbitrary parameter-independent tester controls. General Kraus-gauge and channel-extension facts are credited; the specific construction still needs verification.

3. **Regularization and finite path.** Check the decomposition into a horizontal derivative and residual term, the hybrid control of the latter, and the midpoint variance inequality along the straight segment. Confirm that integration gives a finite-pair bound uniformly when the segment meets a singular face. No infinitesimal Fisher information approximation should substitute for this step.

4. **Matching legal witnesses.** Check diagonal Bernoulli probes and two-dimensional compressions in the midpoint eigenbasis, including the inherited qubit comparison. The chosen witness may depend on the pair, but every preparation and processing map must be independent of which hypothesis is true. Entrywise selection must recover the Hilbert–Schmidt sum with only the stated dimension factor. Constant-factor adaptive/nonadaptive comparability is different from equality of their optimal values.

## Operational volume and entropy

5. **Balls on the closed interval.** Check **lem:matrixball76**, including uniform local tensor comparison, determinant comparison and the inward translation used to retain a definite ellipsoid fraction inside \(0\le E\le I_d\). A calculation only on the positive definite interior would not prove the covering claim.

6. **Spectral integral and multiple logarithms.** Check **prop:matrixvolume76**: the determinant, the Weyl eigenvalue Jacobian and every ordered endpoint sector. In the upper bound, verify prefix exponents and count zero exponents. In the lower bound, verify nested balanced endpoint boxes, separation of same-end eigenvalues and their joint measure. Explain why the logarithmic exponent is \(\lfloor d/2\rfloor\), rather than a parameter count or an unproved product of corner contributions.

7. **Centres, accuracy and constructive content.** Check that volume comparison permits arbitrary legal covering centres and that maximal separated sets give the reverse inequality. Verify the declared error cap and the dependence of constants on \(d\). Rational legal centres must retain the same order. Distinguish their existence from the explicit inherited qubit enumeration and from a polynomial-time coding algorithm.

## Common learning

8. **One experiment for every effect.** Check that the coarse branch choice, adaptive frames, block lengths and returned legal effect depend only on public parameters and observed data. At small contrast, verify variance-sensitive estimates and endpoint recovery uniformly at a zero variance or repeated eigenvalue.

9. **Unknown bias and contrast.** Check the random-sign GHZ identity that removes the bias contribution, the two-plane direction recovery, the safe-angle induction, and the amplitude stopping rule without an input noise promise. Every entangled block must fit the public horizon cap. Fresh observations after data-dependent choices must satisfy the stated conditional bounds.

10. **Risk, lower bound and coding.** Verify the failure allocation over geometric block lengths and the worst-case call count on every record, including exceptional records. Check final Bernoulli endpoint errors and their conversion to \(d_N\). For the matching lower bound, show that any adaptive training strategy on the scalar subfamily is a common processing of independent Bernoulli bits. Verify the two separated loss balls and the confidence dependence. Finally, distinguish estimating an unknown target from applying the supplied-description codec to that estimate.

## Primary-source comparison requested

The detailed source locations and stable links are in `LITERATURE_AUDIT.md`. The following are especially close comparisons:

- **KPP76 and DBSA76:** repeated rank-one POVM discrimination and single-use entanglement-assisted discrimination. Preserve the distinction between the number of candidate measurements and the number of outcomes.
- **FM75, SZ74, PPKK74 and PPKKO72:** two-use projective protocols, unequal-visibility single-use reduction, projective diamond distance and exact multiple-use projective distance. Their ancillary interfaces differ.
- **FI76, DKG67, DM76 and KGAD76:** horizontal Kraus representations, channel extension and adaptive derivative bounds.
- **YF76 and SD76:** quantum Fisher information integrated along finite channel paths, including adaptive discrimination.
- **Dittmann76 and SZGeom76:** inverse Sylvester Bures tensors and spectral matrix-volume methods. The present variance map is not used with its ordinary pullback differential.
- **MB67, ZRK76 and BDPS76:** one-use classical estimation, restricted-probe measurement tomography and measurement learning with quantum programme storage.
- **HB76 and KLY76:** multiscale phase estimation and robust calibration; KLY76 includes its 2021 erratum.

The priority question is whether the specific closed-body midpoint comparison, the multiple-logarithm operational entropy or the horizon-adapted common qubit learner is equivalent to an established result under another parametrization. Established tools are not presented as new. Identifying these tools also does not by itself settle the priority of the resulting statements.

## Inherited results and evidence

Sections 49–52 remain available with their stated noise, regularity and dimensional assumptions, including the unbiased-body contact trichotomy and the explicit biased-qubit code. The matrix theorem does not silently extend the contact theorem to every singular higher-dimensional subset. Learning is proved in dimension two; binary outputs and memoryless consumption remain explicit premises.

The work branch is `revision/general-theta-foundations-i-v76-r49-response-2026-10-04`. Review any referee-ready alias at its final recorded publication head. Source hashes, reconstruction receipts and CI identify the submitted artifacts and check reproducibility. They are separate from mathematical correctness, priority and journal suitability. No external opinion or human signature is implied by the branch name or this brief.
