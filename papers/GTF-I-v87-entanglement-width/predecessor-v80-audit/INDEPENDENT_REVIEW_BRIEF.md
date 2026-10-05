# Independent human specialist review brief — Revision 80

**Status: material prepared; an independent human correctness, overlap and priority judgment remains pending.** No outside reviewer has been contacted or commissioned, and no such opinion is represented here. This is an actionable packet for a specialist, not a referee report, endorsement or clearance. The author-side source comparison is `LITERATURE_AUDIT.md`; the current article comparison is `editions/operational-comparison80.tex`.

The controlling report remains **R51 on v77**, preserved as `FROZEN_R51_REPORT.md`, reviewing exact head `5650842e0bc89ca6a8b6d6730115784f0d9ecc12`. Revision 80 follows published v79 head `0daec5b3e20e5bf778caa90a0cf54f26c1ea53fe`. The new mathematical objects are Sections 62–63; Sections 58–61 and the earlier geometry, entropy, calibration and coding results remain part of the candidate. The complete prior v79 brief follows verbatim and is also archived separately. Its branch and version descriptions are historical. Please identify the exact current candidate publication head in any eventual signed opinion.

The journal objective is unchanged. An author-side comparison, AI-assisted proof review, compilation, preserved source, publication branch or unsigned commit does not meet the report's request for independent human specialist judgment or resolve its assessment of journal positioning.

## Interface and claims to assess first

The device is the memoryless consuming binary channel
\[
\mathcal M_E(\rho)=\operatorname{tr}(E\rho)|1\rangle\langle1|
+\operatorname{tr}((I-E)\rho)|0\rangle\langle0|,
\qquad 0\preceq E\preceq I_d.
\]
Outcomes are ordered; no residual quantum system or environment is returned. External references and coherent adaptive controls are allowed in the unrestricted model. The loss \(d_N\) is the largest unhalved trace distance of allowed future tests with at most \(N\) calls. Training calls, future calls, transmitted bits, control accuracy and computational complexity are distinct resources.

The promised interior is \(\mathcal I_d=[I/4,3I/4]\). In the fresh-block acquisition model, \(b=1\) permits independent entangled input/reference pairs and unrestricted collective final processing, but quantum systems retained from previous outputs cannot coherently enter subsequent probe preparations. Mele–Bittel's acquisition belongs to this class despite its collective output measurement. The new lower bounds permit the stronger unrestricted coherent adaptive training model.

| Result | Exact principal assertion | Main review issue |
|---|---|---|
| Section 62, **thm:interiorconfidence80** | For all integers \(d,N\ge1\), \(0<\delta\le2^{-13}\), \(0<\eta\le1/8\), interior learning has absolute-constant order \(N\delta^{-2}[d^2+d\log(1/\eta)]\). The upper is \(b=1\); the lower is unrestricted. | Are the confidence and dimension arguments valid under this interface, with uniform constants and every stated confidence? Is an equivalent joint future-loss theorem already available? |
| Section 62, **cor:operatorconfidence80** | Binary operator learning has order \(\epsilon^{-2}[d^2+d\log(1/\eta)]\) for \(0<\epsilon\le2^{-14}\). | Does the stated derivation correctly combine an existing estimator, standard repetition, the retained dimension lower bound and the credited diagonal-coin converse? Does prior work already state this all-confidence order? |
| Section 63, **lem:algebraicreadout80** | A rational first-order risk formula decides feasibility of a finite conditional collective readout and yields algebraic POVM entries when feasible. | Does the universal formula cover every real interior effect, exact good-label sets, zero-probability blocks and all positivity/completeness constraints? |
| Section 63, **thm:effectiveinterior80** | For rational public errors in the same range, finite synthesis and trusted precision attain the joint query order while the transmitted word has \(B=A_d+O(d^2)\), \(A_d=d^2\log_2(\sqrt N/\delta)\), and decodes to an exact legal rational effect. | Does the feasibility search terminate by the claimed statistical count, and does the full-instrument error allocation preserve the claimed failure probability? Which equivalent finite implementations predate it? |
| Sections 58 and 62, combined full-body upper | For \(d\ge2\), \(1\le b\le N\), \(0<\delta\le\min\{2^{-13},\delta_*\}\), \(0<\eta\le1/8\), the sufficient budget is \(C N^2\delta^{-2}\min\{d^2+d\log(1/\eta),(d^4/b)\log(d/\eta)\}\). | Does the public choice between independent Choi tomography and horizon blocking respect the same every-record cap? Keep the remaining joint-dimensional gap explicit. |
| Retained Sections 58–61 | Full-body fixed-dimensional fresh-block minimax law, near-fair information lower bound, interior covering and exact/prefix descriptions. | Do the existing unresolved overlap and correctness questions in the prior brief remain, and how do the new results affect the overall contribution assessment? |

## Suggested proof checks

1. **Source upper bound and its confidence extension.** Check Mele–Bittel **Corollary III.9** in [2512.10214v3](https://arxiv.org/html/2512.10214v3), including \(0<\epsilon<1\), \(4e^{-4d^2}<\eta<1\), the operator normalization and legal-effect step in **Lemmas III.7–III.8**. Verify \(q_d=2^{-3d}>4e^{-4d^2}\) for every \(d\ge1\), the independent repetition count, deterministic majority-cluster output selection and its accuracy factor. Distinguish this dimension-dependent repetition from the sufficient \(d^2\epsilon^{-2}\log(1/\eta)\) budget explicitly printed in **Remark III.4**. The existing estimator is credited; neither amplification nor the tomography primitive is presented as an invention here.

2. **Coherent confidence converse.** Compare **lem:diagonalconfidence80** directly with Mele–Bittel **Lemma IV.19** and **Corollary IV.20**. Follow the revealed diagonal index and verify that the resulting conditional state update is parameter-independent even after arbitrary coherent adaptive controls. Check null-versus-coordinate transcript laws, absolute continuity, bounded stopping or padding, the Bernoulli relative-entropy estimate, and the event distinguishing the null success ball from each alternative. Check that the scalar future-use witness separates the alternatives at the claimed \(\delta/\sqrt N\) scale. Summing expected coordinate counts must yield the confidence term without conditioning on a hypothesis-dependent quantum residual state.

3. **Joint lower bound.** Recheck the retained **thm:dimensionlower78** and **lem:weakmeasurementinfo78**, particularly their support conventions and conditional mutual-information bound. The dimension and confidence bounds are combined by \(\max(a,b)\ge(a+b)/2\). No multiplication of independent lower bounds is claimed. The \(d=1\) case, very small \(\eta\), and fixed versus growing dimension should all be covered by the stated constants.

4. **Universal semialgebraic risk.** In Section 63 the classical-block Choi operators are subnormalized polynomials in the effect coordinates. Verify that each conditional POVM acts only on the retained references for its observed classical string, with positive operators summing to identity. The success criterion uses all subsets of labels to encode the exact set of centres within operator distance \(a\); boundary equality must be assigned consistently. Confirm that eliminating universal effect variables leaves a rational semialgebraic feasible set in the readout variables, with no unmentioned integration, oracle for the unknown parameter, or use of coherent access to the classical output register.

5. **Effectiveness and termination.** Check the application of Basu–Pollack–Roy, [second-edition book](https://doi.org/10.1007/3-540-33099-2), **Theorems 2.77 and 2.80, Chapter 14**. Quantifier elimination supplies a decision procedure and real-closed-field transfer supplies an algebraic point. The exact enumeration starts only after nonemptiness is decided. For sample counts tried in increasing order, each rejected count must terminate. The imported estimator and fixed dictionary provide existence within the query bound; the algorithm need not compute that estimator's original measurement entries. Check that the proof certifies all real effects even though the returned entries are algebraic.

6. **Dictionary and control precision.** The exact public dictionary is the retained one from **thm:interiorcodec79**, fixed before data acquisition. Recheck the operator-error margins, clipping, Borel coarse graining and conversion to future loss. Then inspect every classical readout branch, including those with zero probability under some effects, and the algebraic dilation. The trusted-control budget applies to complete instruments, with specification and realization errors both counted; unhalved trace error is converted to total variation only once. A successful decoded word is exact and legal, and its length has no confidence term. The asserted existence of finite instructions must not be read as a polynomial gate or runtime bound.

The full-body upper improvement should also be checked as a direct conversion: one-use accuracy \(\epsilon=\delta/(2N)\) and \(d_N\le2N\|E-F\|_{\rm op}\) give its first branch; the retained fresh-block theorem gives its second. A learner may choose either procedure using only public parameters. This minimum of sufficient bounds is an upper improvement, not a matched growing-dimensional full-body law, and introduces no claim that the existing tomography primitive or the hybrid argument is new.

## Closest algorithmic and priority comparisons

Please compare the actual theorem objects, interfaces and resource measures, not only similar asymptotic expressions. The statistical upper bound comes from Mele–Bittel; its diagonal-coin argument is also a direct lower-bound antecedent. The new future-loss law uses the dimension-free interior metric comparison. Whether this combination, or its one-use all-confidence consequence, already appears explicitly or follows immediately in a comparably formulated source is a concrete open overlap question.

For finite implementation, compare Pelecanos–Spilecki–Tang–Wright, [2511.15806v1](https://arxiv.org/html/2511.15806v1), **Theorems 1.1–1.3, Section 3.3, Figures 8–9 and Theorem 4.2**. They already provide efficient purification and state-tomography constructions with discrete approximate-design ingredients. The present text does not describe that literature as infinite or merely existential. Determine whether a known efficient substitute preserves exactly the covariance and binary operator-error guarantee required in the imported channel estimator, or already yields the complete query/dictionary/precision statement. Section 63 synthesizes a different measurement through feasibility and does not claim to implement their or Mele–Bittel's algorithm. Standard quantifier elimination, algebraic sampling, finite POVM dilation and perturbation bounds are credited mechanisms, not candidates for novelty.

The earlier measurement-discrimination, metrological entanglement-depth, adaptive fidelity, full-body boundary entropy, general-channel lower-bound and exact-code comparisons remain in the preserved detailed brief and audit. In particular, output-copy joint-measurement restrictions differ from fresh-query blocks, and general quantum-output channel lower bounds do not automatically specialize to binary classical-output devices.

## Requested form of an independent assessment

A useful eventual opinion would identify the candidate head and checked source versions, distinguish a proved gap from a request for exposition, and list closest prior theorem statements with their access model, loss normalization and parameter ranges. Please give separate conclusions on correctness of Sections 62–63, overlap of the one-use and future-loss statements, computational scope of the finite synthesis, and whether the retained complete package supports the proposed journal positioning. A negative or unresolved priority conclusion is an acceptable outcome. Nothing in this packet presupposes approval.

Full-body sharp growing-dimensional learning, dimension-uniform boundary entropy, efficient exact reconstruction, residual quantum outputs and general outcome number remain open scope. An assessment of the promised-interior theorem should not be generalized to those tasks. No outside messages should be sent on the basis of this brief without a separate instruction.

## Complete predecessor v79 brief (historical text)

The following text is preserved verbatim as the prior review packet. Its version-specific branch references and then-current theorem scope are historical, while its still-open questions remain available for review.

---

# Independent human specialist brief — Revision 79

No independent human specialist opinion has been obtained or fabricated. This is an actionable brief for the next referee. The journal objective is unchanged. R51 is the controlling report on v77; the candidate now contains v78 plus the new Section 61.

Please assess the exact relation of the dimension-free interior future-use comparison and near-fair adaptive information lower bound to known measurement tomography. Then examine whether the growing-dimensional covering law with arbitrary legal centres, the public exact rational dictionary without an entrywise `d^2 log d` payload loss, and the combined query-optimal learned words occur under equivalent interfaces in prior work. The randomized prefix result expressly uses classical Fano–Kraft and public-erasure ideas; assess the operational formulation rather than novelty of these ingredients. In particular, check the unknown-parameter-independent finite coarse graining and the distinction between ideal trusted operations and efficient synthesis.

Full-body endpoint entropy, the sharp fixed-dimensional independent-block law and their priority questions remain unchanged. The complete previous brief follows, as history and additional questions, not as evidence that a human review has occurred.

---

# Independent specialist review brief — Revision 78

**Status: review material prepared; independent human specialist correctness and priority judgment pending.** No outside reviewer has been contacted or commissioned. This brief is an actionable assessment packet, not an opinion, endorsement, or priority clearance. The author-side source comparison is `LITERATURE_AUDIT.md`. The complete preceding brief, including its detailed geometry/calibration/codec questions, remains at `predecessor-v77-audit/INDEPENDENT_REVIEW_BRIEF.md`.

## Controlling object and purpose

The controlling report is **General Theta Foundations I, Revision 77 (r51)**, preserved verbatim as `FROZEN_R51_REPORT.md`. It reviewed exact head `5650842e0bc89ca6a8b6d6730115784f0d9ecc12` on review branch `review/general-theta-foundations-i-v77-external-referee-r51-2026-10-04`. R51 found no fatal mathematical gap in the retained theorem package, rejected the four-leading-general-journal positioning, and requested independent human priority review, a direct current-tomography comparison, precise fixed-dimensional claims, and a stated preparation model.

The response branch is `revision/general-theta-foundations-i-v78-r51-response-2026-10-04`. Assess the final recorded publication head and its source-bound evidence. `quantitative.tex` is the focused submission; `main.tex` preserves the complete research edition, and `structural.tex` is the separate inherited structural companion. A build receipt, AI-assisted report, exact source reconstruction, unsigned commit, or branch name does not supply an independent human judgment.

Revision 78 adds a training-block resource law, a positive reanalysis of the existing Mele–Bittel estimator on a promised interior, a dimension/accuracy lower bound for weak binary measurements, and a finite trusted-control formulation. The principal full-body learning claim is a minimax theorem in a specified acquisition model. Standard metrological block scaling, fidelity inequalities, hybrid arguments, information inequalities, and packing methods are credited as antecedents.

## Interface and resources to keep fixed

The unknown device is the memoryless consuming channel
\[
 \mathcal M_E(\rho)=\operatorname{tr}(E\rho)|1\rangle\langle1|
 +\operatorname{tr}((I-E)\rho)|0\rangle\langle0|,
 \qquad E=E^*,\quad0\preceq E\preceq I_d.
\]
Its two outcomes are ordered. The device returns no residual quantum system or environment. External references remain available to the tester. The future loss \(d_N\) permits arbitrary reference-assisted adaptive tests with at most \(N\) calls and public bounded stopping. Trace norm is unhalved; \(d_1(E,F)=2\|E-F\|_{\rm op}\).

Training calls \(M\) are separate from those future calls. In **def:freshblocks78**, a classical history chooses a length \(1\le t\le b\) and a fresh quantum tester. Conditional on the history, the complete tester, including its reference and unused inputs, starts tensor-separated from retained systems and is isolated from them until its last call. It may have arbitrary coherent adaptive control internally. Common instruments on all completed outputs are permitted at block boundaries, and an unrestricted collective final readout is permitted. The resulting classical record can choose future probes. Every declared block is charged in full, with total at most \(M\) on every record.

Consequently \(b=1\) includes independent input/reference Choi preparations followed by an arbitrarily large joint measurement. It is a restriction on quantum access to the next queried input, not a restriction on output-memory size, simultaneity, or the number of outputs measured jointly. Neither a general quantum channel with a two-dimensional output nor a two-hypothesis problem is automatically a two-outcome classical-output measurement problem.

State-preparation precision, gate count, reconstruction time, workspace, dictionary storage and transmitted payload are separate resources. Finite trusted controls are an accuracy interface, not an efficient physical synthesis theorem. A supplied-description encoder receives a matrix or a certified coordinate approximation; a physical learner receives an unknown device.

## Exact conclusions to assess

| Source object | Scope and quantitative conclusion | Main comparison question |
|---|---|---|
| Section 58, **thm:blocklearning78** and **cor:onecallseparation78** | Entire effect body, \(d\ge2\), \(1\le b\le N\), \(0<\delta\le\delta_*\), \(0<\eta\le1/8\): \(M_b^*=\Theta_d((N^2/b)\delta^{-2}\log(1/\eta))\); explicit upper \(Cd^4(N^2/b)\delta^{-2}\log(d/\eta)\) | Does an earlier finite-confidence fresh-block measurement-learning theorem imply this common full-body law, including the allowed output memory and stopping? |
| Section 60, **lem:weakmeasurementinfo78**, **thm:dimensionlower78** | Effects near \(I/2\); arbitrary coherent adaptive training: \(M\ge cd^2N\delta^{-2}\) for \(d,N\ge1\), \(0<\delta\le2^{-13}\), \(0<\eta\le1/8\) | Is the conditional information bound or its binary packing consequence equivalent to an earlier channel lower-bound construction? |
| Section 60, **thm:interiorlearning78** | Promised \(I/4\preceq E\preceq3I/4\), future loss, \(\eta=1/8\), \(0<\delta\le2^{-13}\): \(\Theta(d^2N\delta^{-2})\) with absolute constants; upper uses MB67 with \(b=1\), lower allows arbitrary coherent training | Is the dimension-free interior metric comparison and resulting sharper analysis of the existing estimator already available in an equivalent form? |
| Section 60, **cor:binaryoperatorlearning78** | Entire binary effect body, operator error \(0<\epsilon\le2^{-14}\), failure \(1/8\): \(\Theta(d^2\epsilon^{-2})\); upper is MB67 | Compare the joint lower bound with the actual binary results of MB67 and reductions from current general-channel theorems; no first-result claim is requested. |
| Section 59, **thm:finitecontrollearning78** | Original common and block-restricted learning orders with finite trusted control specifications and certified norm errors | Do the finite descriptions, every-record error allocation and exact legal classical output justify the claimed control model? |
| Sections 53–54, **thm:matrixmetric76**, **thm:matrixcover76** | Full binary body: explicit midpoint-resolvent comparison and fixed-dimensional small-error entropy \(\asymp_d N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}\) | Identify equivalent earlier closed-body finite-pair and endpoint-log volume statements. |
| Sections 55–57, **thm:commonlearn76**, **thm:matrixlearning77**, **thm:matrixcodec77** | Retained qubit and matrix common learners; finite exact public codec with optimal-order index | Assess the prerequisites used by the new block upper bound and the surviving calibration/code priority questions. |

For \(d=1\), the block-learning law is instead \(\Theta(N\delta^{-2}\log(1/\eta))\), independent of \(b\). The projective lower bound requires \(d\ge2\). The full-body upper factor \(d^4\) remains unmatched. On a common small-error range the full body has the simultaneous lower bound
\[
 M\ge c\delta^{-2}\left(d^2N+\frac{N^2}{b}\log(1/\eta)\right),
\]
but a matching joint law on the full body is not claimed. The promised-interior theorem has joint dimension/horizon/accuracy optimality only at the stated fixed confidence.

## New proof questions, in order of dependence

### 1. Fresh acquisition and memory separation

Read **def:freshblocks78** literally. Determine whether tensor separation and isolation are sufficient to include all stated fresh input/reference acquisitions while excluding quantum feedback into future probes. At a given classical history, the tester specification is common under both hypotheses even though the history distributions and stored conditional states differ. Confirm that preparatory classical randomness, boundary instruments, unequal record supports, variable block lengths and public stopping are all represented. An uncharged pre-shared quantum register linking distinct fresh blocks would change the model.

Verify the applicability to the actual source algorithms. Mele–Bittel v3, Algorithm I.2, Figure 1 and Section III.2, prepares independent Choi copies and performs its coherent processing only after channel acquisition. Its phrase “single parallel block” does not make those query inputs entangled across copies. Zambrano–Ramos-Calderer–Kueng v3, Section 3.1 and Theorem 2, uses separate known probe states. Both fit \(b=1\), despite their different reference and output-processing resources.

### 2. Finite fidelity with adaptive fresh blocks

In **lem:blockfidelity78**, check the embedded projective family
\[
 E_\phi=\tfrac12(I_2+\cos\phi\,\sigma_1+\sin\phi\,\sigma_2)
            \oplus I_{d-2}/2.
\]
The one-call unitary comparison gives Bures angle at most \(|\theta|/2\) uniformly over reference-assisted input states. Its adaptive triangle bound gives root fidelity at least \(\cos(t|\theta|/2)\) for a common \(t\)-call tester. With \(t\le b\) and \(b|\theta|\le1\), verify the exponential lower estimate.

For the branch potential
\[
 \Psi=\sum_h e^{-a(M-m(h))}\mathfrak f(A_h,B_h),\qquad a=b\theta^2/4,
\]
check each common-instrument and fresh-tensor-product update on subnormalized states. Histories with different charged call counts must remain distinguished in this calculation. Verify terminal weights, stopped branches, final collective readout, and the passage to general measurable outcome spaces. The conclusion must be \(\mathfrak f(\Gamma_0,\Gamma_\theta)\ge e^{-Mb\theta^2/4}\), with no unconditional independence assertion.

The exact local projective distance \(2\sin(N|\theta|/2)\) is a known type of projective-discrimination statement; PPKKO72 is credited. Taking \(\theta=4\delta/N\) gives disjoint radius-\(\delta\) success balls. Verify the classical test's root fidelity bound \(2\sqrt\eta\) and the displayed \(1/24\) lower-bound constant for \(\eta\le1/8\). A local Fisher-information or unbiased-estimator inequality alone is insufficient to check these high-confidence claims.

### 3. Full-body block upper bound

Check **lem:blockhybrid78**, including reference memory carried into each future group and padding of stopped testers. Applying **thm:matrixlearning77** at horizon \(b\) and accuracy \(\delta/\lceil N/b\rceil\) must preserve a common legal estimator, the fresh-block model and the every-record call cap. Verify \(b\lceil N/b\rceil^2\le4N^2/b\). The original qubit procedure's first-rejection stopping rule, conditional confidence allocation and matrix calibration/compression proof remain prerequisites; their detailed retained questions are in the preceding brief.

### 4. Information gain of a weak measurement

In **lem:weakmeasurementinfo78**, the input \(\rho^x_{AR}\) may already depend on the unknown label through earlier calls. Check positivity of the partial-trace perturbation and support containment:
\[
 -r\rho_R^x\preceq\Delta_x\preceq r\rho_R^x,
 \qquad \Delta_x=(\rho_R^x)^{1/2}K_x(\rho_R^x)^{1/2},\quad\|K_x\|\le r.
\]
Verify the noncommuting collision calculation with support inverses,
\[
 \operatorname{tr}[(\omega_{YR}^x)^2((I_Y/2)\otimes\rho_R^x)^{-1}]
 =1+4\operatorname{tr}(\rho_R^xK_x^2)\le1+4r^2,
\]
and the Jensen proof of the relative-entropy bound. The average-minus-mixture identity gives \(I(X:Y\mid R)\), and data processing compares the old \(AR\) information with the retained \(R\) information. Both steps are needed to justify the per-query bound with arbitrary coherent memory.

In **thm:dimensionlower78**, check the operator-norm ball packing in real dimension \(d^2\), its location inside \([I/4,3I/4]\), the dimension-free Bernoulli witness, and the constants \(r=2048\delta/\sqrt N\), separation \(4\delta\), and \(\delta\le2^{-13}\). Fano's inequality must use the complete final quantum/classical record after adaptive data processing. The nearest-packing reduction is a mathematical test and does not give the learning algorithm an oracle for computing \(d_N\).

### 5. Positive reanalysis of Mele–Bittel on the interior

In **lem:interiormetric78**, check the path constraint \(I/8\preceq G(t)\preceq7I/8\), \(S=\sqrt{G(I-G)}\succeq I/4\), the integral solution of \(SK+KS=H\), and \(\|K\|_{\rm op}\le2\|H\|_{\rm op}\). The retained horizontal derivative bound then yields \(d_N(E,F)\le4\sqrt N\|E-F\|_{\rm op}\), with no dimension factor.

MB67 Corollary III.9, supported by Lemma III.8, returns a legal effect even if its internal estimate is a general CPTP map. At \(\eta=1/8\), its condition \(\eta>4e^{-4d^2}\) holds for every \(d\ge1\). Verify the substitution \(\epsilon=\delta/(8\sqrt N)\), the success-event placement of the estimate in \([I/8,7I/8]\), and the upper budget \(O(d^2N\delta^{-2})\). This is a use and reanalysis of an existing estimator. The full-body \(b=1\) lower bound rules out the same horizon rate without the interior promise.

### 6. Finite controls and the original risk event

In Section 59 check the finite classical decision-tree description, computable rounding of sample budgets, algebraic spectral/tie rules and phase-root representation. In **lem:controlhybrid78**, errors are charged to full quantum instruments with their outcome flags; branch errors alone must be summed. The every-record error sum bounds the ideal-law expectation of adaptive errors and the total variation of the final classical output.

Verify the rational approximation plus exact normalization of prescribed vectors, and the corresponding isometry correction \(W=A(A^*A)^{-1/2}\) for controls. Running the ideal learner with failure \(\eta/2\) and allocating state-preparation trace error \(\eta/M_*\) transfers the unchanged classical failure event, including discontinuous choices, without rounding the returned legal effect. Workspace is reset or discarded before a fresh block. The direct state description may be exponential in block width; polynomial physical synthesis is not asserted.

## Priority comparisons a specialist should resolve

| Primary source or family | Exact assessment requested |
|---|---|
| **MB67**, arXiv:2512.10214v3: Algorithm I.2; Theorems III.2–III.3; Remark III.4 eq. (165); Lemmas III.7–III.8; Corollary III.9 | Confirm the \(b=1\) acquisition classification with collective Choi processing. Assess the positive interior reanalysis and the full-body acquisition converse as distinct statements. Keep the restricted-confidence corollary and all-confidence amplification separate. |
| **MB67**, Proposition IV.17 and Corollary IV.20 | Compare the actual binary projector-packing and diagonal-coin converses with the new joint \(d^2\epsilon^{-2}\) lower bound. Do not multiply source bounds that are stated separately. |
| **ZRK76**, arXiv:2507.04500v3; *Quantum* **10**, 2162; Definition 1, Theorems 2 and 9 | Check the binary normalization, known single-copy probes, dimensions, accuracy and confidence. Its lower bound's no-reference nonadaptive restriction cannot become a converse for a larger coherent access model. |
| **Hyllus78**, Observation 1 eq. (9), and **Toth78**, Observation 3 eq. (6) | Credit the established \(F_Q\le Mb\) bounded-entanglement-depth scale. Determine the actual increment supplied by common full-body learning, finite confidence, reference memory, variable blocks and stopping. |
| **SHW68**, Sections II.2 and V.2, and **WBHK72**, Lemma 14, Proposition 21 and Appendix B | Compare the classical-input/output-memory model and finite fidelity/converse tools. Identify whether an equivalent earlier result directly implies the conditional branch-potential bound, beyond asymptotic exponent statements. |
| **OG67**, arXiv:2601.04180v4, and **CZY78**, arXiv:2601.10683v1, Theorems 1.1, 3.2 and 4.2 | Examine reductions of their general-channel hard families to binary qc effects. CZY78 keeps coherence between output sectors; a fixed readout or different packing might yield an equivalent weak-binary lower bound, but the printed general-channel statement cannot simply be specialized by output dimension. Check this possibility explicitly before any priority claim. |
| **CLL78**, arXiv:2402.16353v1, and **NZ78**, arXiv:2609.10514v1, Theorems 1.1–1.2 | Compare resource definitions: these bound joint measurements on supplied state copies; the present block cap limits coherent query acquisition and permits arbitrary final joint processing. No first-interpolation claim is made. |
| **FI76, DKG67, DM76, KGAD76, YF76, SD76** | Verify at-use credit for horizontal Kraus gauges, channel extension and path integration. Assess the specific global regularized variance form and the dimension-free interior consequence. |
| **Dittmann76, SZGeom76** | Compare the actual tangent and domain of the inverse-Sylvester form, uniform operational-ball volume, and the paired-endpoint logarithmic exponent; an ordinary variance-map Bures pullback has a different differential. |
| **FM75, SZ74, PPKK74, PPKKO72, KPP76, DBSA76** | Compare ordered outcomes, residual-system/reference access, pair versus family statements, and exact versus constant-factor discrimination. Retain hypothesis counts separately from outcome counts. |
| **BDPS76, HB76, KLY76, Gutoski66** | Compare stored quantum programmes with classical estimates, inherited multiscale phase tools with the explicit safe-angle and stopping analysis, and pair-dependent discrimination with common estimation. Account for the KLY76 erratum. |

The exact source URLs and checked version dates are in `LITERATURE_AUDIT.md`. For each requested comparison, the useful outcome is an equivalent theorem or an explicit derivation with matching hypotheses and quantifiers, a precisely narrower overlap, a substantive new increment after attribution, or a named unresolved point. The existence of an author-side search is not evidence that no equivalent statement exists.

## Retained objects requiring human review

The new work uses the earlier closed-body geometry, common matrix learner and codec. Review the midpoint form
\[
 Q_N(E,F)^2=N\langle F-E,
 (L_{A(I-A)}+R_{A(I-A)}+N^{-1}\mathrm{Id})^{-1}(F-E)\rangle_{\rm HS},
 \qquad A=(E+F)/2,
\]
with its two-sided constant-factor operational comparison and singular-boundary extension. For the entropy law, review actual operational-ball volume before the spectral integral, the Weyl Jacobian and balanced-endpoint logarithmic count. For learning, review simultaneous calibration of both regularized support endpoints, noise introduced by data-selected compressions, fresh conditional experiments, coordinate assembly and legal rational selection. For the codec, review exact PSD and Sylvester tests, boundary-safe inward rounding, actual-metric packing, public replay and charged payload. The complete inherited checklist remains archived; these matters are not closed by the block theorem.

## Requested independent deliverable

Provide a written specialist assessment tied to the exact revision head. For each principal object, identify correctness under its specified interface, precise overlap with primary sources, any remaining proof gap, and the mathematical increment after attribution. Give separate conclusions for the full-body block law, the interior theorem, the binary dimension/accuracy lower bound, the retained geometric/entropy objects and the exact codec. Report any counterexample or hidden change of resource model with an explicit construction or source locator.

An independent priority judgment and a journal-suitability judgment should be recorded separately. No general-journal threshold or repository-wide Theta A/B/C/D closure follows from a correct specialized learning theorem. **Human assessment remains pending; this packet does not fill in or simulate the requested opinion.**
