# Referee Report — General Theta Foundations I, Revision 77 (r51)

**Focused quantitative manuscript:** *Finite-Use Geometry and Learning of Ordered Binary Quantum Measurements*  
**Structural companion:** *Finite Physical Actions and a Strong Converse for Repeatable Observations*  
**Complete research edition:** *General Theta Foundations I: Stochastic Realization and Finite-Use Measurement Geometry*  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branches:**
- `revision/general-theta-foundations-i-v77-native-source-2026-10-04`
- `revision/general-theta-foundations-i-v77-r50-response-2026-10-04`
- `revision/general-theta-foundations-i-v77-referee-ready-2026-10-04`

**Reviewed exact final head:** `5650842e0bc89ca6a8b6d6730115784f0d9ecc12`  
**Candidate publication:** `dadb88a90d37f18f19af1db45a89cfe2e7aad7f4`  
**Qualified native source:** `91df620ec7b6e02a6f0fe1c7798639c2626c742b`  
**Completed predecessor:** Revision 76 final head `c041c011274973728a8cc55029192c057696aa43`  
**Controlling external report:** v76/r50, `fc197f98fe40c7fb9319ff67c8ee42ecbb542ae1`  
**Controlling proof/pipeline audit:** v76/r50, `4f6381884b79b4165ee3e4be1d887d0537b12e36`  
**Exact-head read-only reconstruction:** Actions run `37204165960`, conclusion `success`  
**Review branch:** `review/general-theta-foundations-i-v77-external-referee-r51-2026-10-04`  
**Date:** 4 October 2026

## Recommendation

**Reject at the Annals / Inventiones / JAMS / Acta level.**

This is **not a correctness rejection**. Revision 77 is a serious and technically successful response to the two principal mathematical limitations identified in r50. The common unknown-device learner is no longer confined to qubits: it now covers the entire matrix effect body

\[
\mathfrak E_d=\{E=E^*\in M_d(\mathbb C):0\preceq E\preceq I_d\}
\]

in every finite dimension. Separately, the previously existential rational-centre covering is converted into one deterministic, finite, exact encoder and decoder whose reusable index has the optimal fixed-dimensional order. The qubit subroutine's first-rejection stopping rule, exceptional-record fallbacks, conditional confidence allocation, and every-record budgets are also stated explicitly.

I did not find a fatal mathematical gap in the simultaneous endpoint calibration, the harmonic-mean variance comparison, the compression-leakage identity, the conditional use of fresh qubit learners, the weighted coordinate assembly, the finite rational legalization step, the scalar minimax converse, the exact positive-semidefinite tests, the rational Sylvester comparisons, the inward grid rounding, the greedy codebook separation, or the payload converse. The new statements appear correct in their declared ranges and resource models.

The four-leading-general-journal conclusion nevertheless remains negative. The paper gives a strong theory for one important but specialized quantum interface: memoryless **ordered binary** measurements with classical output and no residual quantum system. Its central finite-use metric is determined only up to dimension-dependent constants; the sharp entropy law is fixed-dimensional and small-error; the learner's displayed `d^4` upper dependence is not matched in growing dimension; and the exact codec is finite but deliberately exhaustive rather than efficient. The methods synthesize established horizontal Kraus gauges, channel-extension bounds, path integration, inverse-Sylvester geometry, spectral volume, tomography, concentration, and multiscale phase recovery. The synthesis is substantial, but I do not see a theorem whose breadth or external consequence reaches the threshold of the four leading general journals.

The independent priority boundary also remains unsettled. Mele--Bittel already give essentially optimal one-use diamond/operator-norm learning results for channels and binary POVMs, while Zambrano--Ramos-Calderer--Kueng give dimension-optimal nonadaptive single-copy POVM tomography bounds. These papers do not imply the present anisotropic future-`N` loss, the closed-body midpoint-resolvent geometry, or the exact operational code. They do, however, substantially narrow the novelty claim and make a direct theorem-by-theorem comparison indispensable. An author-side literature audit, exact CI reconstruction, and this AI referee-style report do not replace an independent human specialist priority judgment.

**Disposition outside the four leading general journals:** the focused 45-page article is a strong, coherent, and potentially publishable contribution in mathematical quantum information. I would support serious specialist review after a human priority assessment, tighter positioning against current tomography results, and modest editorial compression. I do not recommend another wholesale reconstruction of the mathematics.

---

## 1. Frozen object, genealogy, and material reviewed

The three Revision 77 manuscript aliases identify one theorem package. The response and referee-ready branches point to

```text
5650842e0bc89ca6a8b6d6730115784f0d9ecc12.
```

The native-source branch points to `91df620e...`. The candidate publication `dadb88a9...` is its direct child. The exact final head changes only review/provenance metadata and leaves manuscript sources, PDFs, archives, and mathematical claims unchanged. Its read-only Actions run checked out that exact SHA, rebuilt the submitted sources and every PDF page, independently rebuilt the focused journal package, and completed successfully.

Revision 77 is five commits beyond the completed v76 object. The principal native-source commit adds the all-dimensional learner, exact matrix codec, corrected qubit control flow, focused article, response, proof/literature/history audits, implementations, and source-bound evidence. The final review head is metadata-only.

I reviewed, in particular:

- `quantitative.tex`, `main.tex`, and `structural.tex`;
- `editions/operational-introduction77.tex` and the active comparison section;
- `sections/53-matrix-effect-metric.tex`;
- `sections/54-matrix-effect-entropy.tex`;
- `sections/55-common-measurement-learning.tex`;
- `sections/56-fixed-dimensional-learning.tex`;
- `sections/57-effective-matrix-codes.tex`;
- the full qubit prerequisite graph loaded by the focused article;
- `matrix_metric.py`, `matrix_codec.py`, their schemas and exact checks;
- `RESPONSE_TO_REFEREE.md`, `PROOF_AUDIT.md`, `PROOF_STATUS.json`, `LITERATURE_AUDIT.md`, `INDEPENDENT_REVIEW_BRIEF.md`, and `HISTORY_AND_PIPELINE_AUDIT.md`;
- the frozen r50 external report and proof/pipeline audit;
- the source hashes, preservation manifests, theorem locations, resource ledger, page checks, visual review, journal package, and build receipt;
- the exact-head read-only workflow; and
- the frozen repository-wide A/B/C/D pipeline ledger and history.

The focused article is 45 pages, the structural companion 41 pages, and the complete historical edition 185 pages. The complete edition is useful as a preservation object, but the focused article is the proper journal-facing submission.

This report is a referee-style mathematical assessment. It is not a formal proof-assistant certificate, a cryptographic authorship attestation, or an exhaustive independent human priority search.

---

## 2. Executive assessment of the mathematical contribution

### 2.1 Retained closed-body finite-use geometry

For

\[
 M=\frac{E+F}{2},\qquad H=F-E,\qquad V=M(I-M),
\]

the retained theorem defines

\[
 Q_N(E,F)^2
 =N\left\langle H,
 (L_V+R_V+N^{-1}\operatorname{Id})^{-1}H
 \right\rangle_{\mathrm{HS}}
\]

and proves

\[
 \frac{\min\{1,Q_N(E,F)\}}{8192d}
 \le d_N^{\mathrm{na}}(E,F)
 \le d_N(E,F)
 \le\min\{2,8Q_N(E,F)\}.
\]

This includes noncommuting effects, repeated eigenvalues, scalar effects, rank changes, and projective boundary points. It yields a uniform-in-horizon constant-factor bound on adaptive advantage in each fixed dimension. It is a comparison theorem, not an exact distance formula and not equality of adaptive and parallel optima.

### 2.2 Retained global operational entropy

For each fixed dimension and sufficiently small error, the full effect body has covering order

\[
 N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}.
\]

The proof first establishes two-sided weighted-volume bounds for actual operational balls at every boundary stratum, then evaluates a spectral integral. Balanced approaches to the two opposite support endpoints generate the logarithmic exponent. The converse permits arbitrary legal memoryless binary centres.

This remains one of the most distinctive results in the package.

### 2.3 New common learning on the complete matrix body

Revision 77 proves that one procedure, common to all unknown effects, has risk

\[
 \sup_{E\in\mathfrak E_d}
 \mathbb P_E\{d_N(E,\widehat E)>\delta\}\le\eta
\]

using at most

\[
 C d^4N\delta^{-2}\log(d/\eta)
\]

training calls on every record. Each entangled training block has at most `N` calls. A scalar Bernoulli subfamily gives

\[
 M\ge cN\delta^{-2}\log(1/\eta)
\]

even against arbitrary reference-assisted adaptive training with bounded public stopping. Hence the dependence on horizon, accuracy, and confidence is optimal for every fixed `d`; the displayed dimension exponent is not claimed sharp.

The proof has three nontrivial layers:

1. simultaneous relative calibration near both support endpoints at cutoff `1/N`;
2. control of the additional variance created by data-selected two-dimensional compressions; and
3. assembly and legalization of separately learned matrix coordinates in a calibrated quadratic norm.

This is a real extension, not a change of notation in the qubit theorem.

### 2.4 New deterministic exact matrix codec

The paper constructs one finite legal Gaussian-rational grid with denominator

\[
 K=\left\lceil\frac{32dN}{\delta}\right\rceil,
\]

then greedily retains a point precisely when its exact midpoint modulus exceeds `delta/16` from every earlier centre. Legality is decided by exact positive-semidefinite elimination and the modulus by an exact rational Sylvester solve.

An inward displacement followed by coordinate rounding sends any target to a legal grid point within operator-norm error `3delta/(32N)`. A retained predecessor then gives total operational error at most `11delta/16`. Distinct centres are separated in the actual metric, so disjoint operational balls and the volume theorem control the codebook size. Encoder and decoder reconstruct the same dictionary from public parameters.

The resulting fixed-length payload has order

\[
 \frac{d^2}{2}\log_2N
 +\lfloor d/2\rfloor\log_2\log(N+2)
 +d^2\log_2(1/\delta)+O_d(1).
\]

This closes the constructive description gap identified in r50. It does not close an algorithmic-efficiency gap: the enumeration may be enormous.

### 2.5 Learning directly into an optimal-order word

Running the learner at accuracy `delta/2` and the codec at accuracy `delta/2` yields a public fixed-length word with decoded operational error below `delta`, no additional device calls, and the same failure probability. The scalar learning lower bound and the operational covering lower bound separately establish fixed-dimensional optimal training and payload orders.

Training calls, classical reconstruction time, dictionary storage, and transmitted payload remain distinct resources. This separation is correct and important.

---

## 3. Correctness audit of the all-dimensional learner

### 3.1 Simultaneous endpoint calibration

The calibration uses dyadic regularization scales down to order `1/N`. At every stage it probes diagonal vectors and the four real/imaginary superpositions for every pair in a deterministically selected eigenbasis of the previous estimate. Fresh samples follow every data-dependent basis choice.

Conditional Bernstein bounds control each matrix entry simultaneously in terms of both the success and failure endpoint variances. Normalizing by the previous regularized estimate gives a small operator perturbation in both endpoint geometries. The clipping-and-inward update is always legal; on the good event the clipping is inactive, and the factor-two Loewner invariant propagates.

The procedure also obtains

\[
 \|E-A\|_{\mathrm{op}}\le N^{-1/2}.
\]

The failure allowances form a geometric sum. Since the sample count at scale `t` is proportional to `t^{-1}` and the confidence logarithm grows only linearly with the reverse scale index, the total is `O(d^4N log(d/eta))` rather than `O(d^4N log N log(d/eta))`.

I find the induction and budget coherent. The deterministic treatment of repeated eigenvalues through projections of a public basis avoids an unstated eigenvector oracle.

### 3.2 Calibrated variance and compression leakage

The proof combines the two endpoint Loewner comparisons by the exact harmonic identity

\[
 \left((G+\tau I)^{-1}+(I-G+\tau I)^{-1}\right)^{-1}
 =\frac{G(I-G)+(\tau+\tau^2)I}{1+2\tau}.
\]

This gives constant-factor comparison of the regularized variances of `A` and `E`.

For a projection `P` commuting with `A`, the compressed effect `C=PEP` satisfies

\[
 C(I-C)=PE(I-E)P+PE(I-P)EP.
\]

The second term is positive. Because `P` commutes with `A`, its cross block is `P(E-A)(I-P)` and its square is bounded by the calibration operator-norm error, hence by the horizon cutoff. It can therefore be absorbed into the regularization. This is the necessary argument that a data-selected two-dimensional subspace does not create uncontrolled noise.

The constants are conservative but logically adequate.

### 3.3 Conditional qubit learning

After calibration, the paper runs the complete qubit learner on every two-dimensional compression, with fresh observations, accuracy proportional to `delta/d`, and confidence `eta/(2 binom(d,2))`. The guarantee of the qubit subroutine is uniform over legal compressed effects, so it remains valid conditional on the calibration record.

The corrected qubit control flow stops at the first rejected dyadic scale and returns the previous accepted scale. No later stage is executed after rejection. Ambiguous phase estimates and failed concentration records have deterministic legal fallbacks, and every record respects the advertised call bound. This resolves the direct procedural defect identified in r50.

### 3.4 Coordinate assembly

For each off-diagonal coordinate, the proof uses the corresponding two-dimensional estimate. Each diagonal coordinate is chosen from one fixed incident pair; it does not assume that duplicate diagonal estimates agree.

The pairwise endpoint forms dominate the calibrated global coordinate weights. Summing the nonnegative coordinate contributions therefore bounds the complete error form. Although the sum of all pair forms contains duplicate diagonal terms, discarding unused duplicate terms only improves the inequality.

This assembly step is sound.

### 3.5 Legal rational selection

The assembled Hermitian matrix need not be an effect. The proof minimizes distance to the legal effect body in the known positive quadratic norm induced by `A`. Since the true effect is feasible, an exact minimizer is within twice the assembly error.

For a finite procedure, the proof replaces the minimizer by a legal rational grid approximation in the fixed public basis. The inward displacement and sufficiently fine rational rounding preserve both positivity and the complement constraint. The quadratic norm is evaluated from observed/algebraic data and public parameters, not by querying the unknown effect.

The finite selection may be computationally expensive, but it is mathematically effective in the declared device-call model.

### 3.6 Transfer to operational risk

The variance comparison transfers the legalized estimate's calibrated form error to the true endpoint form. Local midpoint/endpoint comparison then bounds `Q_N`, and the global metric upper theorem gives operational error at most `delta`.

The proof keeps the small-error threshold explicit. It does not use the local comparison outside its stated range.

### 3.7 Call count and converse

There are order `d^2` pair learners. Each has target accuracy `delta/d`, hence order `d^2 N delta^{-2}` calls, and multiplying by the number of pairs gives the displayed `d^4` order. The logarithmic confidence factor is `log(d/eta)`.

The lower bound restricts to scalar effects. Every call then produces a Bernoulli observation independent of the chosen input and reference. An arbitrary adaptive protocol is a common processing of independent Bernoulli bits and parameter-independent resources. Two separated future-loss balls give a test, and the relative-entropy/fidelity bound yields the full `log(1/eta)` factor.

This proves fixed-dimensional optimality in `N`, `delta`, and `eta`, but no growing-dimensional optimality. The paper states this correctly.

---

## 4. Correctness audit of the deterministic matrix codec

### 4.1 Exact finite grid and legality

The independent real coordinates of a Hermitian matrix range over finite rational grids. The implementation prunes by necessary two-by-two principal-minor inequalities but retains full exact positive-semidefinite tests for both `G` and `I-G`.

The written zero-pivot Schur rule is valid: for a positive-semidefinite matrix, a zero diagonal pivot forces the corresponding row and column to vanish; otherwise the candidate is rejected. Positive pivots reduce to exact Schur complements. The process terminates on singular strata.

### 4.2 Exact midpoint-modulus comparisons

For a legal rational pair, the midpoint variance is Gaussian rational, and the regularized Sylvester operator is invertible. Solving the finite rational linear system gives an exact rational value of `Q_N^2`. Thus the strict greedy comparison has a definite answer even at equality; no floating threshold or spectral decomposition is used.

The implementation follows this logic.

### 4.3 Inward rounding

The inward map places the target spectrum a distance `s=2d/K` from both support endpoints. Coordinate rounding changes the operator norm by at most `d/K`, leaving a margin `d/K` to both boundaries. The total target-to-grid displacement is at most `3d/K`, which is at most `3delta/(32N)`.

The hybrid inequality contributes at most `3delta/16`. The greedy predecessor contributes at most `8(delta/16)=delta/2`. Their sum is `11delta/16`.

The constants and legality argument are consistent.

### 4.4 Codebook size

Two retained centres have `Q_N>delta/16`. The metric lower theorem converts this to positive separation in the actual operational metric. Small actual metric balls around the centres are therefore disjoint. The uniform lower measure of operational balls and the total volume theorem give the desired codebook upper bound.

This argument does not assume a triangle inequality for `Q_N`; it uses the triangle inequality only for `d_N`. That distinction is correctly maintained.

### 4.5 Public reconstruction and payload

Both encoder and decoder reconstruct the finite ordered list from public `(d,N,delta)`. The payload is only the fixed-length binary index. Unused words decode to a specified legal effect. No target-dependent dictionary or uncharged centre coordinates are hidden in the message.

Since the constructed family is a radius-`delta` cover, the covering lower theorem supplies the opposite payload bound in the fixed-dimensional small-error regime.

### 4.6 Computational limitations

The ambient enumeration has size at most

\[
 (K+1)^d(2K+1)^{d(d-1)}.
\]

Every candidate may be compared against a growing retained list by exact rational linear algebra. This is a terminating construction, not an efficient codec in the length of the payload. The implementation correctly treats a resource cutoff as an incomplete construction and emits no codebook or purported payload.

The theorem should continue to use “finite exact” or “constructive” rather than “efficient.”

---

## 5. Reproducibility and evidentiary status

The exact final-head workflow run `37204165960` completed successfully. It checked out `5650842...`, installed fixed dependencies, rebuilt the submitted sources and every PDF page read-only, rebuilt the focused journal package independently, and preserved source-bound reconstruction evidence.

The committed build receipt records:

- 45 pages for the focused article;
- 41 pages for the structural companion;
- 185 pages for the complete edition;
- 330 native files in the qualified revision;
- 296 predecessor native files;
- 658 preserved predecessor labels and 707 active complete-edition labels;
- 15 exact suites under ordinary and optimized Python with identical outputs;
- isolated reconstruction;
- no unresolved references or citations and no overfull or underfull boxes; and
- page-text and raster reproduction.

The final metadata correctly notes that raw pdfTeX logs retain font-expansion warnings even though no rendered layout defect was found. This is more accurate than claiming that every engine warning vanished.

The finite tests check arithmetic identities, positive-semidefinite legality, budgets, parser behavior, replay, and small complete enumeration cases. They do not prove continuum covering, stochastic minimax risk, the horizontal adaptive theorem, asymptotics, or priority. The repository generally states this boundary correctly.

The final commit and its ancestors are unsigned. Source reconstruction establishes object identity and reproducibility, not human authorship.

---

## 6. Priority and relation to current literature

### 6.1 Horizontal channel geometry

Horizontal Kraus gauges, channel-extension bounds, adaptive metrological recursions, and integration of local distinguishability along finite paths are established methods. The paper credits Fujiwara--Imai, Demkowicz-Dobrzański and coauthors, Yuan--Fung, and Sieniawski--Demkowicz-Dobrzański at the relevant steps.

The potentially new object is not the existence of a local Fisher form. It is the explicit regularized midpoint-resolvent comparison on the complete binary effect body, including singular strata, together with matching one- and two-dimensional finite-pair lower witnesses.

### 6.2 Spectral volume

Inverse-Sylvester/Bures forms and spectral matrix-volume calculations are classical. The potentially new global statement is the exact effect-body operational covering order and the logarithmic multiplicity generated by paired approaches to both support endpoints.

I did not locate an obvious source that states this exact law. That is not a proof of priority.

### 6.3 Measurement and channel learning

Mele--Bittel prove essentially optimal channel learning in diamond distance and, as a by-product, essentially optimal operator-norm learning for binary POVMs. Their principal access uses nonadaptive Choi-state preparation and collective processing. Zambrano--Ramos-Calderer--Kueng give dimension-optimal, nonadaptive single-copy POVM tomography under one-use worst-input outcome distance. Recent lower-bound work on channel learning further sharpens the surrounding sample-complexity landscape.

These results do not contain the present future-`N` anisotropic metric or the simultaneous endpoint calibration/compression proof. Conversely, the present paper should not advertise “optimal measurement learning” without immediately specifying the future-horizon loss, binary interface, fixed-dimensional interpretation, and unoptimized dimension factor.

A direct analysis of existing one-use estimators under `d_N` remains an important priority question. The substitution `operator error about delta/N` gives only a coarse sufficient baseline and does not prove optimality or separation from those estimators.

### 6.4 Exact coding

The finite exact greedy construction is a useful conversion of an entropy theorem into a public reproducible code. Its main novelty is the combination of exact legality, exact `Q_N^2` comparisons, support-boundary-safe rounding, actual-metric packing, and charged index replay.

The construction's mathematical value is payload optimality, not computational efficiency.

### 6.5 Status of priority review

The repository's literature file is careful and useful, but it is author-written. The independent-review brief correctly leaves the human specialist priority task open. This r51 assessment is generated in an AI-assisted repository workflow and should not be represented as satisfying a request for independent **human** expert priority clearance.

---

## 7. Why the four-leading-journal threshold is not met

### 7.1 The physical interface remains narrow

All headline theorems concern memoryless, input-consuming, ordered binary measurements with classical output and no residual quantum system. Multiple-outcome POVMs, disturbing instruments, channels with residual quantum output, and sequential quantum measurement back-action are outside the theory.

This is a rich and important interface, but it is still specialized for a leading general mathematics journal.

### 7.2 The metric theorem is a comparison, not a classification

The constants depend on dimension, and the lower bound loses a factor proportional to `d`. The paper does not determine the exact adaptive distance, exact optimal tester, or equality between adaptive and nonadaptive strategies. It gives a powerful equivalence of scales, not a full intrinsic distance formula.

### 7.3 No sharp growing-dimensional theory

The covering theorem is fixed-dimensional. The learner has an explicit `d^4` upper bound but only a scalar dimension-free lower bound. Neither minimax learning nor entropy is sharp when dimension grows jointly with horizon and accuracy.

A sharp high-dimensional law would materially broaden the result.

### 7.4 Constructive does not mean efficient

The exact codec may require exhaustive enumeration and repeated exact rational linear algebra over a grid exponential in `d^2 log K`. The reusable payload is optimal, but public reconstruction time and workspace may dominate it enormously.

This does not invalidate the theorem. It limits the computational consequence.

### 7.5 Established methods carry much of the proof architecture

The package combines several classical or established mechanisms in a technically effective way. The resulting synthesis is original enough for specialist publication, but its main conceptual ingredients are not new general principles on the scale normally expected by the four leading general journals.

### 7.6 The wider Theta programme is independent and open

The finite-dimensional measurement theorems do not provide the raw unsmoothed local limits, stopped-path large deviations, global past kernel, nonlinear Nisio cores, filtering/QMD/LAN, changing-filtration response, or labelled posterior contraction required by the repository's independent A/B/C/D chains.

All five aggregate completion flags remain false. The size of the historical repository cannot be used as additional significance for this paper.

### 7.7 No comparably broad external consequence

The revision closes important internal gaps in its own development programme. I do not see a corollary resolving a recognized open problem of comparable visibility outside finite-use binary-measurement geometry and learning.

---

## 8. Required revisions before specialist submission

1. **Submit the 45-page focused article as the primary object.** Keep the 185-page complete edition as an archival research record, not as a competing journal manuscript.

2. **Obtain an independent human priority assessment.** The review should cover the midpoint comparison, the endpoint-log covering law, the future-`N` learner, and the exact matrix codec.

3. **Put the binary qc interface in every headline.** “Quantum measurements” alone is too broad; ordered binary, consuming, classical-output, no-residual-system should remain visible.

4. **State fixed-dimensional optimality precisely.** The learner is optimal in `N`, `delta`, and `eta` for fixed `d`; no sharp claim in `d` should be implied.

5. **Expand the current tomography comparison.** In particular, explain exactly why Mele--Bittel and Zambrano--Ramos-Calderer--Kueng do not already imply the future-horizon theorem, and whether their estimators admit a stronger `d_N` analysis.

6. **Keep the distinction between pair geometry and common learning.** Pair-dependent lower witnesses do not constitute a common estimator.

7. **Keep `Q_N` labelled as a comparison modulus.** Do not call it the adaptive distance or use an unstated triangle inequality.

8. **Separate payload, reconstruction time, workspace, and training.** The exact dictionary is finite but not efficient.

9. **Keep every range visible.** The matching covering/payload order is fixed-dimensional and small-error; the learner has an absolute small-error cap and `eta<=1/8`.

10. **State the preparation model for algebraic/rational training states.** Device calls are counted; exact classical arithmetic and state-preparation complexity are separate resources.

11. **Retain the exact-head provenance but shorten journal-facing evidence.** A compact reproducibility appendix is enough; detailed repository preservation belongs in the archive.

12. **Do not use A/B/C/D history as a novelty multiplier.** The paper stands or falls on its measurement theorems.

---

## 9. Detailed comments

1. The phrase “full body of quantum measurements” should always be followed by “ordered binary effects” to prevent a multi-outcome interpretation.

2. The abstract's fixed-dimensional optimality sentence is accurate, but the `d^4` upper factor should be mentioned immediately when the learner is first advertised.

3. The distance normalization is unhalved trace norm. This should remain visible because several tomography papers use total variation or halved trace distance.

4. The nonadaptive class still allows entangled blocks and retained references. It is not “product input.”

5. Public bounded stopping is included in the adaptive distance and in the learning converse. Keep this in the model definition.

6. The basis-selection rule at repeated eigenvalues is important. It belongs in the main proof, not only an audit.

7. State preparation of algebraic eigenvectors is treated as classical/control work outside the call count. This should be stated once in the theorem discussion.

8. The calibration clipping is inactive only on the good event; off that event it exists to keep the procedure legal and the budget deterministic. This distinction is correct and worth retaining.

9. The two endpoint Loewner estimates, not the operator-norm estimate alone, are what control small eigenvalue and complement-eigenvalue noise.

10. The compression identity should be displayed prominently; it is the bridge from calibration to the qubit subroutine.

11. The qubit learner must continue to use fresh samples after every data-dependent scale and basis decision.

12. First rejection must terminate the dyadic search. The predecessor ambiguity should not reappear in pseudocode or implementation prose.

13. The pairwise learner confidence bounds are conditional on calibration. A conditional union bound, not an independence claim, is the correct argument.

14. The assembled diagonals come from designated incident pairs. No consistency of duplicate estimates is used.

15. The rational legalization grid is in the public input basis, even though the error form is defined from a random calibrated basis. The proof correctly separates these roles.

16. The exact codec's strict greedy inequality determines equality cases. Changing it to a floating comparison would change the reproducibility claim.

17. The matrix grid implementation's principal-minor pruning is only a necessary prefilter; full PSD tests remain required for `d>=3`.

18. The codebook upper bound is obtained from actual operational balls. It should not be presented as a packing theorem for `Q_N` itself.

19. A certified approximation is sufficient for real-input encoding, but an arbitrary real oracle representation is not supplied. Keep this computational boundary explicit.

20. The payload converse assumes a fixed public deterministic decoder into legal memoryless effects. It is not a lower bound on arbitrary interactive descriptions.

21. Complete small scalar dictionaries and finite prefixes in dimensions two and three are useful tests, but they do not execute a large theorem-scale matrix dictionary.

22. The build receipt and visual review establish reproducibility and formatting, not theorem correctness or priority.

23. Raw font-expansion warnings are harmless only insofar as page inspection shows no defect. The corrected final metadata states this accurately.

24. The final head is unsigned. No cryptographic authorship inference should be attached to the successful Actions run.

25. The structural companion remains logically independent of the new matrix-learning theorem. Its repeatable-probe scope should not be merged into the quantum measurement claims.

26. The paper's strongest specialist positioning is the joint package: finite-use closed-body geometry, exact entropy, common future-loss learning, and public optimal-order coding for ordered binary effects.

---

## 10. Final assessment

Revision 77 successfully addresses the central mathematical requests of r50:

- it specifies and repairs the qubit block-selection procedure;
- it extends common learning from qubits to the full matrix effect body;
- it proves fixed-dimensional optimal dependence on horizon, accuracy, and confidence;
- it converts the arbitrary-dimensional covering theorem into a terminating exact public codec; and
- it combines learning and coding without additional device calls.

I found no fatal gap in the new theorem chains. The paper has moved from a partly existential and partly qubit-limited package to a coherent full-dimensional theory for its chosen binary interface.

It has **not** crossed the Annals / Inventiones / JAMS / Acta threshold. The interface remains specialized, the metric and high-dimensional dependences are not exact or sharp, the codec is not efficient, the architecture relies substantially on established quantum-information methods, and independent human priority clearance remains open. The broader repository programme is mathematically separate and incomplete.

**Recommendation: reject at the four leading general mathematics journals; encourage a focused submission to a strong specialist journal in mathematical quantum information after independent human priority review and editorial tightening.**
