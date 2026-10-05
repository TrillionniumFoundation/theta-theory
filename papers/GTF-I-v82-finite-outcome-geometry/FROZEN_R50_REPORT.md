# Referee Report — General Theta Foundations I, Revision 76 (r50)

**Focused quantitative manuscript:** *Finite-Use Geometry of Ordered Binary Quantum Measurements*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v76-r49-response-2026-10-04`
- `revision/general-theta-foundations-i-v76-native-source-2026-10-04`
- `revision/general-theta-foundations-i-v76-referee-ready-2026-10-04`

**Reviewed exact final head:** `c041c011274973728a8cc55029192c057696aa43`  
**Native theorem-source parent:** `a107cd1a0f7ec4e356e807f5f49c7ab998553552`  
**Completed predecessor:** Revision 75 exact head `16b78c8edef566300ea21300908854ad83455879`  
**Controlling external report:** v75/r49, commit `4de14a3fe5c271c77de64e410e1bd67fa2e7dce8`  
**Controlling proof/pipeline audit:** v75/r49, commit `8ee073109d5911c6526ff81314bede13bafe9f6c`  
**Exact-head read-only reconstruction:** Actions run `37198984154`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v76-external-referee-r50-2026-10-04`  
**Date:** 4 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 76 is a substantial and mathematically serious response to r49. It removes the principal qubit-only limitation of Revision 75 by proving an intrinsic finite-use comparison on the complete matrix interval

\[
 \mathfrak E_d=\{E=E^*\in M_d(\mathbb C):0\preceq E\preceq I_d\}
\]

for every fixed finite input dimension. It then determines the small-error covering order of this entire body, including every support rank and every spectral multiplicity, and separately constructs a common unknown-device learner on the complete binary qubit body with matching training-call upper and lower bounds.

I did not find a fatal gap in the horizontal-dilation argument, the regularized Sylvester split, the adaptive path integration, the two-dimensional compression lower bound, the singular-boundary operational-ball estimate, the spectral determinant calculation, the balanced-prefix logarithmic count, the bias-cancelling GHZ observation, the data-dependent dyadic block selection, or the scalar minimax converse. The main statements are correctly separated by scope: the matrix metric and entropy theorems hold for every fixed dimension; the common learner and implemented exact codec remain qubit results.

The four-leading-general-journal conclusion nevertheless remains negative. The new work is broad within one important quantum interface, but that interface is still the family of memoryless ordered **binary** measurements with classical output and no residual quantum output. The comparison modulus is equivalent to the adaptive distance only up to dimension-dependent constants, rather than an exact finite-use formula. The arbitrary-dimensional codebook theorem is existential, the sharp common learner is confined to input dimension two, and neither the metric nor learning theory covers multiple outcomes or disturbing instruments. The principal methods combine established horizontal Kraus gauges, channel-extension bounds, inverse-Sylvester/Bures forms, spectral matrix integration, tomography, and multiscale phase estimation in an effective new way, but the resulting theorem package remains more naturally a major specialist contribution than a transformative theorem of general mathematics.

A bounded priority search did not identify a theorem directly matching the midpoint-resolvent comparison, the full matrix-interval entropy

\[
 N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2},
\]

or the future-horizon qubit learning law

\[
 \Theta\!\left(N\delta^{-2}\log(1/\eta)\right).
\]

That search is not an independent priority clearance. Recent work on optimal diamond-distance channel learning, finite-sample POVM tomography, and adaptive channel discrimination substantially narrows the novelty that may be claimed. The contribution should therefore be described as the specific finite-horizon operational geometry, its global matrix-effect entropy, and the induced future-loss qubit learner—not as the first general theory of measurement tomography, channel geometry, or adaptive discrimination.

**Disposition outside the four leading general journals:** the focused quantitative article is a strong and potentially publishable contribution in mathematical quantum information. I would support serious specialist review after the authors make the priority boundary completely explicit, remove the remaining ambiguity in the block-selection procedure, and compress the journal-facing article. I do not recommend another wholesale reconstruction of the mathematics.

---

## 1. Frozen object and material reviewed

The latest completed GTF-I manuscript object located in the repository is Revision 76 at

```text
c041c011274973728a8cc55029192c057696aa43.
```

The referee-ready, response, and native-source branches identify the same theorem package through the direct source/publication genealogy recorded above. The final head is the publication/evidence child of the native theorem-source commit `a107cd1a...`. The exact-head workflow attached to the final SHA completed successfully. The focused paper is 69 pages, the structural companion 41 pages, and the complete research edition 174 pages.

I reviewed in particular:

- `quantitative.tex`, `main.tex`, and `structural.tex`;
- `editions/matrix-introduction76.tex` and `editions/matrix-comparison76.tex`;
- `sections/53-matrix-effect-metric.tex`;
- `sections/54-matrix-effect-entropy.tex`;
- `sections/55-common-measurement-learning.tex`;
- the inherited qubit metric and entropy sections 51–52;
- the v73–v75 lower-witness and exact-code inputs used by the new proofs;
- `RESPONSE_TO_REFEREE.md`, `PROOF_STATUS.json`, `PROOF_AUDIT.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- `RESOURCE_LEDGER.md`, codec schemas, and the independent review brief;
- the build receipt, preservation manifests, theorem locations, finite regressions, package manifests, and exact-head reconstruction record;
- the frozen r49 external report and proof/pipeline audit; and
- the repository-wide A/B/C/D analytic pipeline history and ledger.

This report is an external mathematical assessment, not a proof-assistant certificate, a cryptographic authorship attestation, or an exhaustive priority search.

---

## 2. Principal new mathematics

### 2.1 Intrinsic matrix comparison

For effects `E,F` let

\[
 M=\frac{E+F}{2},\qquad H=F-E,\qquad V=M(I-M),
\]

and define on Hermitian matrices

\[
 Q_N(E,F)^2
 =N\left\langle H,
 (L_V+R_V+N^{-1}\operatorname{Id})^{-1}H
 \right\rangle_{\rm HS}.
\]

Theorem `thm:matrixmetric76` proves

\[
 \frac{1}{8192d}\min\{1,Q_N(E,F)\}
 \le d_N^{\rm na}(\mathcal M_E,\mathcal M_F)
 \le d_N(\mathcal M_E,\mathcal M_F)
 \le\min\{2,8Q_N(E,F)\}.
\]

The definition is intrinsic at repeated eigenvalues. It includes all ranks and all singular strata, and it remains finite because of the `1/N` cutoff. The exact one-use identity is

\[
 d_1(\mathcal M_E,\mathcal M_F)=2\|E-F\|_{\rm op}.
\]

The theorem also yields a fixed-dimensional bound on adaptive advantage:

\[
 d_N\le65536d\,d_N^{\rm na}.
\]

This last statement is a constant-factor comparison, not parallel optimality or equality of the two optima.

### 2.2 Full matrix-effect entropy

For every fixed input dimension `d`, Theorem `thm:matrixcover76` proves

\[
 \mathcal C_N(\mathfrak E_d,\delta)
 \asymp_d
 N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}
\]

for all `N>=1` and `0<delta<=delta_d`. The converse allows arbitrary legal memoryless binary centres. Rational legal centres attain the same order existentially. The resulting reusable fixed-length description has length

\[
 \frac{d^2}{2}\log_2N
 +\lfloor d/2\rfloor\log_2\log(N+2)
 +d^2\log_2(1/\delta)+O_d(1).
\]

For `d=2` this agrees with the full biased-qubit theorem in Revision 75. The power `floor(d/2)` is not obtained by parameter counting. It arises from nested balanced approaches of eigenvalues to the two support endpoints.

### 2.3 Common unknown-device learning

Theorem `thm:commonlearn76` treats the entire ordered binary qubit body with unknown bias, contrast, and direction. For future loss measured by `d_N`, it gives one common learner with

\[
 \sup_E\Pr_E\{d_N(E,\widehat E)>\delta\}\le\eta
\]

using at most

\[
 C N\delta^{-2}\log(1/\eta)
\]

training calls on every record, with every entangled block of length at most `N`. A scalar Bernoulli subfamily gives the matching lower bound

\[
 c N\delta^{-2}\log(1/\eta).
\]

This is a genuine common-estimation theorem and is logically distinct from the pair-dependent witnesses used in the metric and packing arguments.

---

## 3. Audit of the matrix metric proof

### 3.1 Horizontal binary-measurement lift

At an interior effect `G`, set `S=sqrt(G(I-G))`. For Hermitian `K`, the proof prescribes the tangent

\[
 H_0=SK+KS
\]

through the factors

\[
 A_1=\sqrt G,\quad A_0=\sqrt{I-G},\qquad
 B_1=\sqrt{I-G}K,\quad B_0=-\sqrt G K.
\]

The identities

\[
 \sum_y A_y^*B_y=0,\qquad
 \sum_y B_y^*B_y=K^2
\]

are correct. The proposed anti-Hermitian gauges realize these derivatives by genuine nearby measurement dilations rather than merely formal Kraus tangents. The observed channel remains the prescribed binary measurement after the factor environment is traced out.

For a purified common tester, the derivative of the final purification is the sum of one-slot derivatives. Cross terms at distinct slots vanish because the surviving factor is `W^* dot W=0` as an operator on the full input space. This is strong enough for retained references, adaptive quantum memory, and coherent purification of classical feedback. The resulting horizontal tangent cost is

\[
 2\sqrt N\|K\|_{\rm op}.
\]

The argument does not expose the dilation environment to the tester.

### 3.2 Regularized tangent and finite path

The Sylvester equation

\[
 SK+KS+N^{-1/2}K=H
\]

has a unique Hermitian solution. Splitting `H` into the horizontal term and the residual `N^{-1/2}K`, and applying the one-slot hybrid bound to the residual, gives the derivative estimate

\[
 4\sqrt N\|K\|_{\rm op}
 \le4g_{N,G}(H).
\]

This is a linear decomposition of a derivative, not an assertion that the path is a physical mixture of two devices. Integrating separately for each fixed tester and taking the supremum afterward avoids an unjustified interchange between differentiation and optimization.

The passage to boundary paths by

\[
 G_\varepsilon=(1-2\varepsilon)G+\varepsilon I
\]

is legitimate at fixed horizon because the regularized form is continuous on the closed body and the hybrid inequality controls endpoint convergence.

### 3.3 Straight-segment midpoint bound

Operator concavity of `G-G^2` along the segment from `E` to `F` yields

\[
 V_{G(t)}\succeq2\min(t,1-t)V_M.
\]

The corresponding order passes to left-plus-right multiplication on Hermitian matrices and reverses under inversion. Since

\[
 \int_0^1[2\min(t,1-t)]^{-1/2}\,dt=2,
\]

the path inequality gives `d_N<=8Q_N`. The singular scalar factor at the endpoints is integrable, so no spectral margin is hidden in this step.

### 3.4 Nonadaptive converse

In an eigenbasis of the midpoint, diagonal entries of `H` are detected by repeated Bernoulli inputs. Off-diagonal entries are detected in the corresponding two-dimensional compression. The compressed pair is exactly an ordered binary qubit pair, including on a retained reference, so the v75 nonadaptive comparison applies.

The identity

\[
 V_M=\frac12V_E+\frac12V_F+\frac14(F-E)^2
\]

controls the endpoint variances of the compression. The elementary vector decomposition of the two Bloch radii controls its off-diagonal entry by the v75 spectral/angular comparator. Since the largest weighted matrix entry is at least `Q_N/d`, one of these one- or two-dimensional experiments supplies the asserted lower bound.

This maximum argument correctly uses different pair-dependent experiments for different entries. It does not construct, and does not claim, a single estimator extracting every entry simultaneously.

### 3.5 Spectral ranks and multiplicities

The intersecting-subspaces argument for each ordered eigenvalue is correct: the first `k` eigenspace of one effect intersects the orthogonal complement of the first `k-1` eigenspace of the other in a nonzero vector. Bernoulli monotonicity then gives spectral noncancellation. Eigenvalue multiplicities do not invalidate the dimension count.

I find the matrix comparison proof complete at the level claimed.

---

## 4. Audit of the entropy proof

### 4.1 Actual operational balls

The proof defines the regularized density

\[
 \rho_N(E)=\sqrt{\det G_{N,E}}
\]

for the fixed-endpoint quadratic form and the measure `dmu_N=rho_N(E)dE`. The local comparison between midpoint and endpoint forms is derived from the normalized perturbation of

\[
 W_E=E(I-E)+(2N)^{-1}I.
\]

For sufficiently small form norm, both the quadratic forms and their determinant densities are uniformly comparable. Combining this with the global metric theorem gives two-sided inclusion between a small operational ball and local ellipsoids.

At a support boundary, the lower-volume proof does not assume that a fixed fraction of a centred Euclidean ellipsoid remains legal. Instead it moves to

\[
 E_s=(1-2s)E+sI,\qquad s\asymp r/N,
\]

and places a full `d^2`-dimensional legal ellipsoid around `E_s`. The normalized positivity and complement-positivity estimates are adequate. This establishes

\[
 \mu_N(B_{d_N}(E,r))\asymp_d r^{d^2}
\]

uniformly at every centre and every boundary stratum.

### 4.2 Determinant and spectral Jacobian

In a spectral basis the determinant calculation gives

\[
 \rho_N(E)
 =2^{-d/2}N^{d^2/2}
 \prod_iw_i^{-1/2}
 \prod_{i<j}(w_i+w_j)^{-1}.
\]

Combining this with the Hermitian spectral Jacobian produces the integral

\[
 I_d(\tau)=\int_{[0,1]^d}
 \prod_i(v_i+\tau)^{-1/2}
 \prod_{i<j}
 \frac{(\lambda_i-\lambda_j)^2}{v_i+v_j+\tau}
 \,d\lambda.
\]

The repeated-spectrum set is null for this change of variables, while the operational-ball theorem has already treated those points metrically.

### 4.3 Balanced-prefix upper bound

After ordering endpoint depths, the sign sequence records whether an eigenvalue approaches zero or one. The cumulative exponent is

\[
 A_j=\frac{S_j^2}{2}\ge0.
\]

Under logarithmic variables, positive `A_j` give integrable exponential tails and each zero prefix contributes at most one logarithm. A zero prefix can occur only at an even index, so at most `floor(d/2)` logarithms occur. The sector summation is finite at fixed `d`.

### 4.4 Matching nested lower boxes

The lower bound places eigenvalues in opposite-endpoint pairs at separated scales. Each pair contributes a scale-independent amount after its two marginal singularities, its opposite-endpoint denominator, and the box volume are multiplied. Cross-interactions between pairs cancel in same-endpoint/opposite-endpoint pairs. Choosing `floor(d/2)` ordered scales gives the required logarithmic power.

This is the most distinctive global calculation in the revision. I did not find a missing spectral region or an incorrect logarithmic multiplicity.

### 4.5 Covering consequence

The lower covering bound follows from the uniform upper measure of arbitrary operational balls. The upper bound follows from a maximal separated set and disjoint smaller balls. Rational legal effects are dense after an inward move, and fixed-horizon continuity permits rational replacement at constant radius slack.

The arbitrary-dimensional rational-centre statement is existential. It is not an efficient encoder and should never be presented as one.

---

## 5. Audit of the common learner

### 5.1 Low-contrast product branch

The six Pauli-axis experiments estimate the Bloch vector with a variance-sensitive Bernstein bound. Under `r<=7/8`, feasibility gives a uniform comparison between the scalar variance and

\[
 V=p(1-p)+q(1-q).
\]

Normalizing the estimated vector controls both angular error and endpoint misalignment. Fresh observations along the estimated positive and negative axes then estimate both spectral endpoints in Hellinger distance, including at zero and one. The resulting spectral and angular contributions are of order

\[
 \sqrt{NL/n}+NL/n.
\]

The argument does not assume a positive lower bound on the contrast.

### 5.2 Bias cancellation and two-plane phase readout

For a GHZ block, multiplying the output parity by a fresh fair sign cancels every diagonal term involving the unknown bias and retains the off-diagonal coherence. The resulting complex means are

\[
 [x\cdot w+i x\cdot e_i]^m
\]

in two transverse planes. Two quadratures estimate each complex number. Within the maintained cone, the principal phase is unambiguous and division by `m` improves angular resolution by the expected factor.

The random sign must be genuinely independent and fair; the finite negative controls correctly recognize that omitting or biasing it changes the mean.

### 5.3 Data-dependent block length

The dyadic search maintains a shrinking angular cone after each accepted scale. Empirical amplitude acceptance guarantees that the selected block has nonvanishing coherence; rejection identifies the noise scale. Conditional failure allowances proportional to `eta m/N` sum over the dyadic stages, and the weighted logarithmic cost satisfies

\[
 \sum_m m\log(CN/(\eta m))=O(N\log(C/\eta)).
\]

There is one presentational ambiguity that must be removed: **the algorithm must explicitly terminate at the first rejected dyadic scale** and return the preceding accepted scale. Continuing to test larger scales after rejection would not preserve the cone invariant used for the next stage. The proof clearly uses first-rejection semantics, but the procedural statement should say so and should be accompanied by compact pseudocode.

### 5.4 Fine direction and endpoint estimation

At the selected scale `m_*`, the tolerance

\[
 \zeta_*=c_*\delta\sqrt{m_*/N}
\]

costs `O(N delta^{-2} log(1/eta))` calls and produces angular error `O(delta/sqrt(Nm_*))`. The selected-scale lower bound on `m_*(V+1/N)` turns this into future-`N` operational loss `O(delta)`. Fresh endpoint samples then contribute the remaining `O(delta)` loss in product Hellinger distance.

The regime selection from the coarse estimate has sufficient overlap: on the good event, the product branch satisfies the low-contrast premise and the entangled branch satisfies the high-contrast premise.

### 5.5 Minimax converse

The scalar effects

\[
 E_0=\tfrac12I,\qquad E_1=(\tfrac12+\Delta)I,\qquad
 \Delta\asymp\delta/\sqrt N
\]

are separated by more than `2delta` in the future-`N` distance. Under these devices, arbitrary reference-assisted adaptive training reduces to a common stochastic processing of independent Bernoulli bits. The KL bound and the testing reduction give

\[
 M\ge cN\delta^{-2}\log(1/\eta).
\]

This lower bound matches the declared worst-record training-call convention.

I therefore regard the learning theorem as mathematically credible, subject to the first-rejection clarification above.

---

## 6. Literature and priority boundary

The revised literature audit is substantially improved. It now includes the rank-one-POVM adaptive-discrimination work of Krawiec–Pawela–Puchała and the nonprojective entanglement-assisted examples of Datta–Biswas–Saha–Augusiak. It also credits the established roles of:

- horizontal Kraus gauges and channel quantum Fisher information;
- channel-extension and adaptive metrological bounds;
- integration of local channel distinguishability along paths;
- inverse-Sylvester/Bures tensors and spectral matrix integration;
- POVM and channel tomography; and
- multiscale phase-estimation methods.

Two recent comparison points are especially important.

First, Mele–Bittel, arXiv:2512.10214, gives a general diamond-distance channel-learning framework and explicitly includes measurements among its special cases. Second, Zambrano–Ramos-Calderer–Kueng, arXiv:2507.04500 and its 2026 Quantum publication, gives finite-sample POVM tomography in a one-use operational distance with dimension-dependent upper and lower bounds for nonadaptive single-copy probes. These results mean that Revision 76 must not claim the first common estimator of an unknown binary POVM or the first finite-sample measurement-tomography theorem.

The distinctive learning claim is instead the linear dependence on the **future-use horizon** under the anisotropic `d_N` loss, obtained by adapting entangled block size to the unknown noise. Likewise, adaptive channel-discrimination work based on metrological bounds precedes the differential/path methodology, whereas the specific matrix-effect midpoint form and its global entropy remain the claimed increment.

The repository's author-side search did not identify a directly matching all-rank matrix-effect comparison or nested-endpoint covering law. This is evidence for where an independent priority review should concentrate; it is not proof of novelty.

---

## 7. Significance at the four-leading-journal threshold

Revision 76 answers much of r49's mathematical-breadth objection. The paper is no longer merely a qubit calculation. It contains:

1. an intrinsic theorem on a `d^2`-dimensional compact matrix body for every fixed `d`;
2. a nontrivial global entropy law with a new nested logarithmic multiplicity;
3. a quantitative comparison between adaptive and nonadaptive discrimination; and
4. a separate minimax-optimal learner in the complete qubit model.

These are genuine advances.

The remaining obstacle is not a repairable lemma. It is the level of generality and conceptual reach expected by the four leading general mathematics journals. The binary-output identity `E,I-E`, the variance `E(I-E)`, and the two-dimensional compression mechanism are fundamental to the present proof. No theorem is supplied for a general POVM simplex, residual quantum outputs, or disturbing instruments. The constants deteriorate with dimension, the statistical theorem does not extend with the matrix theorem, and the exact all-pair adaptive value remains unknown. The broad historical GTF-I corpus and the unrelated A/B/C/D programme cannot be counted as new significance of this focused revision.

For these reasons I would not recommend another round at the same four-leading-journal target. The result deserves evaluation in a strong specialist venue on its own mathematical merits.

---

## 8. Required revisions before specialist submission

The following requests preserve the mathematical claims and do not ask the authors to downscale or abandon the topic.

### R01. Freeze the reviewed object

State the exact final SHA, native-source parent, manuscript title, and exact-head reconstruction run in the submission cover material. Do not use evidence from a predecessor SHA for an altered successor.

### R02. Restrict the novelty claim precisely

Describe the new contribution as the finite-horizon midpoint-resolvent comparison, the global matrix-effect entropy, and the future-`N` qubit learning law. Do not claim a first general theory of POVM tomography, channel learning, or adaptive channel discrimination.

### R03. Obtain independent priority review

Commission a specialist comparison of `thm:matrixmetric76`, `prop:matrixvolume76`, `thm:matrixcover76`, and `thm:commonlearn76`. The present author-side audit is useful but is not independent clearance.

### R04. Expand the Mele–Bittel comparison

Give a theorem-level comparison of access model, loss, accuracy regime, dimension/rank dependence, adaptive resources, and confidence dependence. Explain why the future-`N` loss changes the sample scale.

### R05. Expand the Zambrano–Ramos-Calderer–Kueng comparison

State their operational distance and probe restrictions explicitly, and separate their one-use tomography result from the present future-horizon qubit theorem.

### R06. Credit adaptive-metrology path methods at the exact point of use

The horizontal lift is specialized, but orthogonality under controls and integration of local distinguishability have direct antecedents. Keep the new claim at the level of the explicit closed-body binary-effect comparison.

### R07. Keep fixed-d and dimension-uniform statements separate

Every matrix covering constant and small-error cap may depend on `d`. Do not use language suggesting a dimension-free theorem or a uniform high-dimensional limit.

### R08. Keep the binary qc interface in every headline

“Full effect body” means all `0<=E<=I_d` for an ordered two-outcome, input-consuming, classical-output measurement. It does not mean all POVMs or instruments.

### R09. Distinguish comparison from exact distance

`Q_N` is not proved to be a metric, to obey a triangle inequality, or to equal the adaptive optimum. Preserve the explicit constants whenever the main theorem is summarized.

### R10. Preserve the small-error range

The entropy and payload formulae hold for `0<delta<=delta_d`. The common learner has its own absolute small-error and confidence ranges. Do not silently extend these to all submaximal errors.

### R11. Keep the learner's qubit scope explicit

The matrix metric and entropy hold in arbitrary fixed dimension. The matching common learner does not. This distinction belongs in the abstract, introduction, theorem summaries, and conclusion.

### R12. Specify first-rejection semantics

In `lem:noiseblock76`, say explicitly that the dyadic search stops at the first rejected scale and returns the preceding accepted scale. Add short pseudocode and list all fallback conventions.

### R13. Display the confidence ledger

Provide one table allocating failure probability to the coarse regime test, dyadic stages, fine phase estimates, and fresh endpoint samples. State which bounds are conditional on the previous record.

### R14. Separate all resources

Training calls, future horizon, maximum entangled block length, retained quantum memory, trusted state preparation, reusable payload, classical runtime, and workspace are different quantities. Keep them separate in the theorem and resource ledger.

### R15. Separate rational existence from implementation

The arbitrary-dimensional rational-centre upper bound is nonconstructive at the optimal order. The executable exact encoder is a qubit result. Do not combine these into an implemented matrix codec claim.

### R16. Compress the focused article

The new matrix and learner results should form the journal-facing paper. Move most inherited instrument/preparation/readout material to a separately cited companion or supplementary archive. The current 69-page article remains heavier than necessary for the new theorem chain.

### R17. Keep the core proof self-contained

The two-dimensional compression may invoke the fully stated v75 theorem, but the journal package must include the exact hypothesis and nonadaptive conclusion needed. Avoid dependence on a historical PDF not present in the submitted source graph.

### R18. State the evidentiary boundary of finite checks

`check_matrix_geometry.py` and `check_common_learning.py` are valuable regression suites. They do not quantify over continuum effects, arbitrary adaptive testers, all stopping records, or the probability-risk theorem.

### R19. Describe provenance accurately

The exact-head workflow and hashes establish reproducibility and source identity. The commits are unsigned and the workflow is not a human authorship or mathematical-certification signature.

### R20. Keep the A/B/C/D analytic programme separate

No matrix-effect theorem, covering calculation, codec regression, or bounded tester-stopping argument closes a raw local limit, stopped-path LDP, Mosco/Nisio, filtering/LAN, changing-filtration response, posterior contraction, or any aggregate pipeline flag.

---

## 9. Detailed comments

### D01. Unhalved normalization

Continue to state that `d_N` uses the unhalved trace norm. Classical total variation is one half of the corresponding classical trace norm.

### D02. Nonadaptive experiments

The notation `d_N^na` still permits entanglement across the input block and a retained reference; it excludes feedback between calls. Repeat this near the corollary comparing adaptive and nonadaptive values.

### D03. Dilation environments

State once more that the outcome copy and factor environment retained in the proof are inaccessible to the tester.

### D04. Anti-Hermitian gauge

The calculation proving `T_y+T_y^*=0` is short but central. Keep the multiplication by the square-root factors explicit.

### D05. Tangent residual

The regularized remainder is controlled at the differential level. It is not a convex decomposition of a finite channel pair.

### D06. Public stopping

Padding a stopped tester must use fixed dummy inputs and discard both their outcomes and environments. The original operational output is unchanged.

### D07. Boundary limit

The epsilon-interior approximation is taken at fixed `N`. No uniform interchange in `N` is claimed.

### D08. Midpoint concavity

When passing Loewner order to `L_V+R_V`, retain the quadratic-form calculation on Hermitian matrices rather than calling left multiplication alone positive.

### D09. Weighted-entry maximum

The factor `d` in the lower bound follows from `d^2` weighted entries and the Euclidean maximum. It is not an optimized dimensional constant.

### D10. Two-dimensional compression

Make clear that the compression is a legal restriction of the input interface and remains exact on inputs entangled with a reference.

### D11. Scalar compressed effects

When one compressed spectral gap vanishes, no eigendirection is chosen and the angular term is zero.

### D12. Ordered spectral witnesses

The intersection vector depends on the known pair and on `k`. The lemma does not provide one basis simultaneously witnessing all eigenvalues.

### D13. Local form comparison

The smallness cap in `lem:matrixlocal76` is used only after operational distance has been converted to a small midpoint modulus. Preserve this order.

### D14. Boundary ellipsoid

The inward displacement is of order `r/N`, not order `r`. This scaling is essential near a projection.

### D15. Operational-ball centres

The covering lower bound allows every legal centre in the full body, not merely centres in a regular spectral chart.

### D16. Determinant convention

Specify the real Hilbert–Schmidt orthonormal basis. Each complex off-diagonal entry contributes two real directions.

### D17. Spectral Jacobian

The Vandermonde is squared for complex Hermitian matrices. The unitary-orbit and permutation constants depend only on fixed `d`.

### D18. Balanced prefixes

A zero signed prefix requires an even index. Distinguish the number of zero prefixes from the number of eigenvalues near the boundary.

### D19. Lower nested boxes

The scale separation is used to make the four cross-pair factors cancel up to constants. Retain this computation instead of replacing it by a heuristic volume argument.

### D20. Rational codebooks

Density proves existence of rational centres at fixed `N`; it does not provide bit complexity or a canonical enumeration.

### D21. Coarse regime decision

Record the numerical slack showing that the low branch implies `r<=7/8` and the high branch implies `r>=5/8` on the coarse good event.

### D22. Endpoint Hellinger metric

Sorting is performed in the `arcsin sqrt(t)` coordinate. This is the clean way to retain endpoint uniformity.

### D23. Fresh data

The final endpoint groups are fresh conditional Bernoulli samples after the estimated axis is fixed. This conditional structure should remain explicit.

### D24. Fair random sign

The bias cancellation fails if the sign is omitted or correlated with the device record. State independence in the procedure definition.

### D25. Two transverse planes

Both angular coordinates are needed. One complex phase does not determine an arbitrary nearby direction on the Bloch sphere.

### D26. Principal argument

The maintained cone places all phases strictly inside the principal interval. No imported global phase-unwrapping theorem is being used.

### D27. Dyadic rejection

Terminate on first rejection. This is the only procedural ambiguity I found that directly affects a proof invariant.

### D28. Stage budget

The sum of the conditional stage allowances is bounded by the geometric sum of tested block lengths. No independence between stage-failure events is required.

### D29. No `log log N` loss

The weighted dyadic cost is `O(N log(1/eta))`; explain the convergent `2^{-k}` and `k2^{-k}` sums in the main text or an appendix.

### D30. Fine-phase cost

Multiplying block length by the number of blocks cancels `m_*` in `m_* zeta_*^{-2}`. This is the source of the linear `N` cost.

### D31. Scalar converse

Under scalar effects, entangled inputs and adaptive controls cannot create parameter dependence beyond the independent Bernoulli outcomes. This reduction should remain explicit.

### D32. Learned code

The learner first outputs a legal real effect. Rationalization and exact coding are postprocessing with radius slack; they use no additional device calls.

### D33. Learner implementation

The repository contains exact identity and budget checks, not a complete executable stochastic learner with certified risk. Describe it as a written algorithm unless such an implementation is added.

### D34. Structural companion

The structural paper is inherited. Its fresh nondisturbing classical probes are not repeated uses of the destructive quantum measurement considered in the quantitative paper.

### D35. Historical corpus

Preserving 557 predecessor labels and 266 native files is useful source stewardship. It is not evidence that every inherited theorem has received a new independent external review.

### D36. Editorial conclusion

The mathematical result is materially stronger than v75. The negative four-leading-journal recommendation rests on specialist scope and significance, not on a discovered counterexample or fatal proof defect.

---

## 10. Final assessment

| Question | Referee conclusion |
|---|---|
| Is v76 the latest completed GTF-I revision? | Yes. |
| Is the reviewed object exactly identified? | Yes: `c041c011...`. |
| Is the matrix metric theorem credible? | Yes; no fatal gap found. |
| Is the all-strata covering law credible? | Yes; no fatal gap found. |
| Is the logarithmic multiplicity justified? | Yes, by balanced prefixes and matching nested boxes. |
| Is the common learner genuinely common? | Yes. |
| Is its training order matched by a converse? | Yes, in the stated qubit model. |
| Is the block-selection procedure perfectly specified? | Not yet; first-rejection semantics must be explicit. |
| Is arbitrary-dimensional optimal coding implemented? | No; rational-centre existence only. |
| Is independent priority clearance complete? | No. |
| Is the whole Theta A/B/C/D programme closed? | No. |
| Does the paper meet the four-leading-general-journal threshold? | In my judgment, no. |
| Is it a strong specialist contribution? | Yes. |

**Final recommendation: reject at the four leading general mathematics journals; encourage a compressed, priority-cleared specialist submission without mathematical downscaling.**
