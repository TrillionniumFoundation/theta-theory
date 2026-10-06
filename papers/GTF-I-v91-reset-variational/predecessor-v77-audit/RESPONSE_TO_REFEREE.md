# Response to v76/r50 — Revision 77

**Paper:** General Theta Foundations I.  
**Focused manuscript:** *Finite-Use Geometry and Learning of Ordered Binary Quantum Measurements*.  
**Revision directory:** `papers/GTF-I-v77-operational-learning`.

## 1. Reviewed object, controlling reports, and submission identity

| Object | Exact identity |
|---|---|
| Reviewed completed revision | v76, `c041c011274973728a8cc55029192c057696aa43` |
| Reviewed native theorem-source parent | `a107cd1a0f7ec4e356e807f5f49c7ab998553552` |
| External report | `GENERAL_THETA_FOUNDATIONS_I_V76_REFEREE_REPORT_R50.md` at `fc197f98fe40c7fb9319ff67c8ee42ecbb542ae1` |
| External review branch | `review/general-theta-foundations-i-v76-external-referee-r50-2026-10-04` |
| Proof/pipeline audit | `GENERAL_THETA_FOUNDATIONS_I_V76_PROOF_PIPELINE_AUDIT_R50.md` at `4f6381884b79b4165ee3e4be1d887d0537b12e36` |
| Audit branch | `review/general-theta-foundations-i-v76-proof-pipeline-audit-r50-2026-10-04` |
| Frozen local reports | `FROZEN_R50_REPORT.md` and `FROZEN_R50_PIPELINE_AUDIT.md` |
| Successful reconstruction of the reviewed predecessor | GitHub Actions run `37198984154`; this is evidence for v76 |

`CONTROLLING_REPORTS.json` records the exact report paths, commits, blobs, and SHA256 values. Both reports are frozen verbatim. The r49 reports remain historical material and are not substituted for r50.

The v77 source and publication SHA values are assigned by the source-freeze and publication process. This response does not invent those identities or reuse a v76 receipt as a v77 result. The machine-generated source hashes, build receipt, theorem locations, page checks, and exact submitted-head reconstruction identify the successor actually produced. A later alteration requires a new matching receipt. The review reports concern v76; no external review of v77 is represented as already obtained.

We thank the referee for distinguishing the correctness of the mathematical arguments from the question of their reach and presentation. The r50 audit accepts the matrix comparison, all-strata operational-ball estimate, spectral integral, covering law, and learning converse. Its direct procedural correction is to terminate the high-contrast dyadic search at the first rejection. Revision 77 makes that control flow explicit and addresses the remaining requests through additional proofs, a focused presentation, and a theorem-level literature comparison.

The mathematical response has two further parts. The common learner now extends from qubits to the entire ordered binary effect body in every fixed input dimension. A separate exact finite encoder and decoder now attain the full matrix covering order. These conclusions are proved in new sections; they are not inferred by changing the dimension in a qubit statement or by calling rational density an algorithm. All inherited theorem statements and their proofs remain in the complete research edition. The four-leading-journal objective and the subject of the manuscript are retained.

## 2. Principal mathematical response

### 2.1 The unchanged operational object and retained geometry

For a positive integer `d`, the target is

\[
\mathfrak E_d=\{E=E^*\in M_d(\mathbb C):0\preceq E\preceq I_d\}.
\]

The device consumes one input system and returns one of two ordered classical labels, with effects `E` and `I_d-E`. It returns no residual quantum system. The distance `d_N` is the supremum of the unhalved final trace norm over common reference-assisted adaptive testers with at most `N` calls and bounded public stopping. Its nonadaptive restriction permits entangled input blocks and a retained reference, with no feedback between calls. Pair-dependent discrimination witnesses and a common unknown-device learner have different quantifiers.

The retained theorem `thm:matrixmetric76` gives, with `M=(E+F)/2`, `H=F-E` and `V_M=M(I_d-M)`,

\[
Q_N(E,F)^2
=N\langle H,(L_{V_M}+R_{V_M}+N^{-1}\mathrm{Id})^{-1}H\rangle_{\rm HS},
\]

\[
\frac{\min\{1,Q_N(E,F)\}}{8192d}
\le d_N^{\rm na}(E,F)\le d_N(E,F)
\le\min\{2,8Q_N(E,F)\}.
\]

The inner product is on the real Hilbert space of Hermitian matrices. The identity `d_1(E,F)=2\|E-F\|_{\rm op}` fixes the normalization. The comparison is uniform in the horizon, ranks, multiplicities, and effects, with its displayed dimension dependence. No exact adaptive optimum, triangle inequality for `Q_N`, or dimension-free comparison is asserted.

The entropy theorem `thm:matrixcover76` retains the order

\[
N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}
\]

for each fixed `d` and `0<\delta\le\delta_d`. Its converse allows arbitrary legal centres. The actual operational-ball estimate, inward displacement of order `r/N`, real-Hermitian determinant, squared Vandermonde, signed-prefix upper bound, and matching separated endpoint boxes remain part of the proof.

### 2.2 An exact stopping rule for the qubit subprocedure

Section `55-common-measurement-learning.tex` retains `thm:commonlearn76` and supplies explicit first-rejection pseudocode for `lem:noiseblock76`. A stage is accepted only if both empirical complex amplitudes pass the prescribed threshold. Acceptance updates the direction and allows the next doubling, subject to the public cap. Rejection immediately terminates the search and returns the preceding accepted length and direction. If no length was accepted, a prescribed legal fallback is returned. Fixed conventions also cover zero complex estimates, ambiguous arguments, and invalid local reconstructions.

The cone invariant is proved against this control flow. There is no stage after the first rejection. The stage failure allowances are conditional on preceding records, and their sum is controlled by the geometric sum of tested block lengths. The public budgets apply on exceptional records as well. The confidence ledger records the coarse decision, product branch, dyadic stages, fine phases, and fresh endpoint samples. Independent random signs, both transverse planes, and fresh endpoint data remain explicit.

### 2.3 Common learning in every fixed dimension

The new `thm:matrixlearning77` in `sections/56-fixed-dimensional-learning.tex` proves that, for absolute constants and sufficiently small absolute `\delta>0`, one common procedure satisfies

\[
\sup_{E\in\mathfrak E_d}
\mathbb P_E\{d_N(E,\widehat E)>\delta\}\le\eta
\]

with at most

\[
Cd^4N\delta^{-2}\log(d/\eta)
\]

training calls on every record, for `d,N\ge1` and `0<\eta\le1/8`. Every entangled block contains at most `N` calls. A scalar converse gives

\[
M\ge cN\delta^{-2}\log(1/\eta).
\]

Thus the dependence on horizon, accuracy, and confidence is optimal for each fixed `d`. The dependence on `d` in the upper bound is not asserted to be optimal.

The extension has a separate calibration proof. With `\tau=N^{-1}`, product-input experiments construct a legal estimate `A` satisfying, on a common high-probability event,

\[
\tfrac12(A+\tau I)\preceq E+\tau I\preceq2(A+\tau I),
\]

\[
\tfrac12(I-A+\tau I)\preceq I-E+\tau I
 \preceq2(I-A+\tau I),
\qquad
\|E-A\|_{\rm op}^2\le\tau.
\]

At each dyadic scale the inputs are eigenvectors and real and imaginary superpositions in the basis of the preceding estimate. Conditional Bernstein bounds control both endpoints. The raw estimate already has spectrum in a small enlargement of the effect interval on the good event; clipping is then the identity, and an affine contraction gives the legal update. The argument does not assume that general spectral clipping preserves a relative Loewner order.

The harmonic identity

\[
\left((G+\tau I)^{-1}+(I-G+\tau I)^{-1}\right)^{-1}
=\frac{G(I-G)+(\tau+\tau^2)I}{1+2\tau}
\]

converts the two endpoint comparisons into a comparison of regularized variances. For a projection `P` commuting with `A`, the exact compression identity is

\[
(PEP)(I_P-PEP)=PE(I-E)P+PE(I-P)EP.
\]

Its second term is positive and at most `\tau P`, by the operator-norm calibration bound. This is the step that controls the noise introduced by a selected two-dimensional subspace.

Fresh qubit learners are run on the `\binom d2` compressions, each at accuracy proportional to `\delta/d`. Their coordinate errors combine in the known form `g_{N,A}`. Projection into the convex legal effect body in this norm, or a finite rational approximation to that projection, gives a legal common estimate. Variance comparison then transfers the error to `g_{N,E}` and the operational metric. Dyadic confidence allocation avoids an extra `\log N` factor. Neither calibration nor compression accesses the unknown matrix as supplied data.

### 2.4 A finite exact matrix encoder and decoder

The new `thm:matrixcodec77` in `sections/57-effective-matrix-codes.tex` supplies the construction missing from the reviewed v76 object. For integer `d,N\ge1` and rational `0<\delta\le1`, it reconstructs one deterministic finite dictionary from the public parameters.

Set

\[
K=\left\lceil\frac{32dN}{\delta}\right\rceil,
\qquad s=\frac{2d}{K},
\qquad \zeta=\frac{\delta}{16}.
\]

The algorithm enumerates a fixed lexicographic grid of Gaussian-rational Hermitian matrices, retaining precisely the legal effects. It builds its dictionary greedily: a candidate is retained exactly when `Q_N(G,C)^2>\zeta^2` for every previously retained centre. Legality and `Q_N^2` are decided by exact Schur elimination and a rational Sylvester solve. No spectral numerical threshold or preassigned list of centres is used.

An inward displacement followed by exact coordinate rounding sends a supplied target to a legal grid point within operator-norm error `3\delta/(32N)`. The selected dictionary centre is within `Q_N`-error `\delta/16` of that grid point. The hybrid and matrix upper bounds therefore give total operational error at most `11\delta/16`.

Distinct retained centres are operationally separated. Disjoint operational balls, their uniform lower measure, and the total volume bound control the dictionary cardinality by the established optimal order. Both encoder and decoder reconstruct the same dictionary. A codeword contains only its index; unused words decode to a fixed legal effect. On the small-error range `0<\delta\le\delta_d`, the fixed-length payload is

\[
\frac{d^2}{2}\log_2N
+\lfloor d/2\rfloor\log_2\log(N+2)
+d^2\log_2(1/\delta)+O_d(1).
\]

The corresponding exact kernel `matrix_codec.py` implements the specified finite procedure. Its ambient candidate count is bounded by

\[
(K+1)^d(2K+1)^{d(d-1)}.
\]

This is an exhaustive construction, with no polynomial-runtime or optimal-workspace claim. A resource cutoff denotes incomplete enumeration and does not produce a completed codebook. Finite complete cases and exact kernel checks are distinguished from the theorem that the unrestricted finite algorithm terminates.

The learned-description consequence `cor:matrixlearnedcode77` combines the common learner, a rational output, and this public dictionary with constant-factor error slack and no additional unknown-device calls. Its payload converse follows because positive success probability for every target forces the decoded alphabet to cover the whole effect body. Training calls, dictionary reconstruction, and transmitted bits remain separate resources.

## 3. Twenty required revisions in the external report

The identifiers below are those of **section 8 of the controlling r50 report**. They are not the r49 numbering retained in `predecessor-v76-audit/RESPONSE_TO_REFEREE.md`.

| Item | Treatment in Revision 77 |
|---|---|
| **R01. Freeze the reviewed object** | The exact v76 final head, theorem-source parent, two report commits and branches, title, and predecessor reconstruction run are recorded in section 1 above and `CONTROLLING_REPORTS.json`. Successor source/publication identities and executed reconstruction results belong to the generated v77 records. They are not inferred from v76. The source response is complete; a build or final-head check is reported successful only when its corresponding receipt exists. |
| **R02. Restrict the novelty claim precisely** | The focused introduction and `editions/operational-comparison77.tex` state the concrete increments: the finite-horizon midpoint-resolvent comparison, all-strata matrix entropy, common learning under future-`N` loss, and the finite exact matrix code. The manuscript does not claim the first general POVM tomography, channel-learning theory, or adaptive path method. |
| **R03. Obtain independent priority review** | **Pending independent human specialist review.** `INDEPENDENT_REVIEW_BRIEF.md` specifies the four v76 theorem objects requested by the report and the two additional v77 results, with the source statements and closest comparisons. The author-side literature audit and internal technical cross-checks do not supply an independent human opinion. No specialist has been contacted or an external clearance represented as obtained. This item is not marked closed. |
| **R04. Expand the Mele–Bittel comparison** | The active comparison identifies Theorem I.1, Lemmas III.7–III.8, Corollary III.9, and the confidence amplification in Remark III.4 of the checked version. It separates channel input/output dimensions and Kraus rank from effect rank; independent maximally entangled probes and collective Choi processing from the present data-dependent blocks; one-use diamond/operator loss from `d_N`; and their stated confidence range from repetition to arbitrary confidence. Substituting `\epsilon=\delta/(2N)` gives a sufficient quadratic-horizon baseline, not a lower bound for their estimator under this different loss. See `LITERATURE_AUDIT.md` and bibliography key `MB67`. |
| **R05. Expand the Zambrano–Ramos-Calderer–Kueng comparison** | The active comparison states their Definition 1 one-use worst-input outcome total variation, Theorem 2 sample bound, number of outcomes, single-copy nonadaptive known probes, absence of retained references and inter-call entanglement, effect-rank range, and access-specific lower bound. For binary effects that loss is `\|E-F\|_{\rm op}`. The future-horizon learner uses a different loss and training interface. See `LITERATURE_AUDIT.md` and key `ZRK76`. |
| **R06. Credit adaptive-metrology path methods at use** | `lem:matrixpath76` retains attribution to horizontal Kraus and channel-extension methods; the introduction and comparison identify finite-path antecedents separately. The new claim is the explicit regularized closed-body binary-effect comparison and its matching witnesses and consequences. The variance form is not described as the ordinary Bures pullback under `G\mapsto G(I-G)`. |
| **R07. Separate fixed-`d` and dimension-uniform statements** | The metric keeps the explicit factor `1/(8192d)` and feedback comparison `65536d`. Entropy constants and the matching payload error cap depend on `d`. The new learner supplies the explicit upper bound `Cd^4N\delta^{-2}\log(d/\eta)` with absolute constants, but its optimality statement is for fixed `d`; sharp dimension dependence is not claimed. |
| **R08. Keep the binary qc interface in headlines** | The title, abstract, introduction, principal statements, and resource ledger identify ordered binary, input-consuming, classical-output measurements with no residual quantum output. The full body is exactly `0\preceq E\preceq I_d`. No multi-outcome POVM or disturbing-instrument theorem is inferred. |
| **R09. Distinguish comparison from exact distance** | `Q_N` remains a comparison modulus. `thm:matrixmetric76` retains its explicit bounds, and `cor:matrixadaptivity76` gives a bound on advantage, not equality of optima. The exact codec computes `Q_N^2` to decide a specified greedy construction; it does not compute the adaptive supremum or use a triangle inequality for `Q_N`. |
| **R10. Preserve the small-error range** | The matching covering and payload formulae retain `0<\delta\le\delta_d`. The learners retain their stated small absolute error and `0<\eta\le1/8` range. The new code is a finite valid construction for rational `0<\delta\le1`, with its upper cardinality bound, but the matching payload asymptotic still uses the inherited small-error lower theorem. No full submaximal-error matrix entropy result is asserted. |
| **R11. Keep the learner's qubit scope explicit** | The reviewed `thm:commonlearn76` is still stated as a qubit theorem. Its scope is extended by a new theorem and full proof, `thm:matrixlearning77`, rather than by changing its wording. The new calibration, variance-compression, coordinate-assembly, legality, confidence, and call-count arguments are given in section 56. The abstract and result summaries distinguish the inherited qubit subprocedure from its proved matrix extension. |
| **R12. Specify first-rejection semantics** | `lem:noiseblock76` now includes explicit stopping pseudocode and legal fallback conventions. Rejection returns immediately. Its proof checks the cone invariant only along accepted continuations. No larger dyadic scale is attempted after rejection. |
| **R13. Display the confidence ledger** | Section 55 displays the qubit stage allocations, including conditional dyadic allowances and fresh endpoint observations. Section 56 adds the calibration allocation and the per-compression allowances `\eta/(2\binom d2)`. Both analyses bound costs on every record. Conditional guarantees are used after the selected basis or axis is fixed. |
| **R14. Separate all resources** | `RESOURCE_LEDGER.md` and `RESOURCE_LEDGER.json` distinguish future horizon, training calls, maximum entangled block, retained quantum memory, trusted preparation, known input representation, dictionary reconstruction, reusable payload, arithmetic, and workspace. Rationalization and encoding use no further device calls. The call theorem charges idealized training access; it makes no optimal hardware, preparation-time, or classical-complexity assertion. |
| **R15. Separate rational existence from implementation** | The v76 density proof remains an existence proof in section 54. Section 57 now adds `thm:matrixcodec77` and the exact implementation of its finite deterministic enumeration, greedy separation, rounding, and decoder reconstruction. This strengthens the constructive result to every dimension. Its exhaustive candidate bound and cutoff semantics are explicit; optimal payload does not imply an efficient encoder. |
| **R16. Compress the focused article** | `quantitative.tex` contains the matrix metric, entropy, qubit subprocedure, matrix learner, matrix code, required biased-qubit geometry/code, and a self-contained prerequisite appendix. Most earlier instrument/preparation/readout material is retained in `main.tex`, rendered as `COMPLETE_REVISION.pdf`. The structural companion remains a separate entry. This changes placement without deleting the inherited proof corpus. Page counts are taken from generated receipts rather than predicted in this response. |
| **R17. Keep the core proof self-contained** | The focused graph includes sections 51–57 and `editions/qubit-prerequisites77.tex`. It supplies the exact biased-qubit nonadaptive theorem, Bernoulli estimates, angular upper bound, and readout prerequisites used by the matrix converse and learners. The journal package includes its active sources; no core premise depends on an absent historical PDF. Label and package reconstruction checks are part of the generated build evidence. |
| **R18. State the finite-check boundary** | The proof/resource audits describe matrix and common-learning checks as finite identities, arithmetic, legality, budget, and control-flow evidence. New codec checks separately test its exact finite kernels and completed small dictionaries. These checks do not quantify over continuum effects, arbitrary adaptive testers, all statistical risk events, or every large-dimensional enumeration. The written proofs establish those theorem statements. |
| **R19. Describe provenance accurately** | Hashes, manifests, Git ancestry, and exact-head reconstruction records establish identities and reproducibility of the objects actually checked. They do not establish human authorship or mathematical certification. No human cryptographic signature is supplied or inferred. Internal cross-checks are not described as independent human referee reports. |
| **R20. Keep A/B/C/D separate** | `HISTORY_AND_PIPELINE_AUDIT.md` retains the full historical dependency graph and model-specific gates. The five aggregate flags remain false in `PROOF_STATUS.json`. The new geometry, learning, exact code, and finite validation provide no replacement for raw local limits, controlled stopped LDP, Mosco/Nisio, filtering/LAN, changing-filtration response, or labelled posterior contraction. |

## 4. Thirty-six detailed comments

These identifiers follow **section 9 of r50**, independently of the required-revision list.

| Comment | Treatment and source anchor |
|---|---|
| **D01. Unhalved normalization** | `eq:matrixoneuse76` and `eq:biasedoneuse75` retain the factor two. Classical total variation is one half of the trace norm of the corresponding classical distribution difference. The same convention is used by the codec error budget and literature conversion. |
| **D02. Nonadaptive experiments** | Section 53 explicitly permits input-block entanglement and a retained reference in `d_N^{\rm na}`. The restriction excludes feedback between uses, not ancillary access. This convention is repeated beside the adaptive/nonadaptive comparison. |
| **D03. Dilation environments** | The proof's copied outcome and factor environment are inaccessible to the tester. They are retained only in a purification used for an upper bound; the operational output remains the declared classical outcome and external systems. |
| **D04. Anti-Hermitian gauge** | The gauge calculation in `lem:matrixpath76` retains multiplication by the square-root factors when proving `T_y+T_y^*=0`. The derivative identities are realized by actual local isometries. |
| **D05. Tangent residual** | The regularized Sylvester remainder is a differential tangent term controlled by the slotwise hybrid estimate. It is not represented as a convex decomposition of a finite pair of channels. |
| **D06. Public stopping** | Stopped testers are padded with fixed dummy inputs, and both dummy outcomes and environments are discarded. This leaves the original operational output unchanged. The scalar learning converse uses the corresponding common-processing convention. |
| **D07. Boundary limit** | The interior approximation in the path proof is taken at fixed `N`. Its use does not assert an interchange with a limit in the horizon. |
| **D08. Midpoint concavity** | Loewner comparison is transferred to `L_V+R_V` through its quadratic form on Hermitian matrices. No assertion that left multiplication alone is a positive operator on that real space is needed. |
| **D09. Weighted-entry maximum** | The factor `d` comes from the `d^2` weighted entries and the Euclidean maximum bound. It remains explicit and unoptimized. New learning dimensions are counted separately through the number of compressions and their accuracy. |
| **D10. Two-dimensional compression** | The matrix converse and matrix learner both specify a fixed isometric input embedding. The compressed binary channel is exact even when its input is entangled across calls or with a retained reference. |
| **D11. Scalar compressed effects** | A vanishing spectral gap has zero angular contribution. No eigendirection is introduced for that scalar component. Both the compression theorem and qubit fallback conventions retain this case. |
| **D12. Ordered spectral witnesses** | The vector from the eigenspace-intersection argument may depend on the known pair and on the ordered eigenvalue index `k`. `lem:matrixspectral76` does not claim one basis simultaneously witnesses every eigenvalue. |
| **D13. Local form comparison** | Operational smallness first forces a small midpoint modulus; only then is `lem:matrixlocal76` used to transfer to an endpoint form. Section 56 writes this implication explicitly for the dimension-two compression estimates. |
| **D14. Boundary ellipsoid** | `lem:matrixball76` retains the inward displacement of order `r/N` and the full legality proof for the contained ellipsoid. The matrix code uses its own explicit displacement of order `\delta/N`. |
| **D15. Operational-ball centres** | The covering lower bound uses the uniform upper measure bound at every legal centre in the full body. It does not restrict centres to the coordinate charts or centres chosen by the upper construction. |
| **D16. Determinant convention** | The determinant is on a real Hilbert–Schmidt orthonormal basis of Hermitian matrices. Each complex off-diagonal entry supplies two real directions. This yields the stated `N^{d^2/2}` factor. |
| **D17. Spectral Jacobian** | The complex-Hermitian Jacobian contains the squared Vandermonde. Unitary-orbit and permutation factors depend only on fixed `d`. |
| **D18. Balanced prefixes** | The proof distinguishes boundary-near eigenvalues from zero signed prefixes. A zero prefix has even index, so there are at most `\lfloor d/2\rfloor` critical logarithmic variables. |
| **D19. Lower nested boxes** | The separated opposite-endpoint-pair calculation remains in `prop:matrixvolume76`. Its two same-endpoint and two opposite-endpoint cross-factors cancel in depth order up to fixed constants; this supplies the matching lower estimate. |
| **D20. Rational codebooks** | Section 54 retains rational-centre density as its original existence argument. Section 57 separately supplies a deterministic grid order, exact greedy criterion, finite encoder and decoder, and payload proof. Its explicit ambient count states the computational cost boundary. |
| **D21. Coarse regime decision** | The coarse good event has error small enough that the threshold `3/4` implies `r\le7/8` on the product branch and `r\ge5/8` on the entangled branch. The source retains this numerical slack before invoking either lemma. |
| **D22. Endpoint Hellinger metric** | The endpoint estimates are sorted in the monotone `\arcsin\sqrt t` coordinate, and the proof retains uniform square-root/Hellinger control at support endpoints. |
| **D23. Fresh data** | The final endpoint groups are sampled after fixing the estimated axis. Their Bernstein estimates are conditional on that previous record. Matrix calibration and each compression learner likewise use fresh observations after their selected basis is fixed. |
| **D24. Fair random sign** | The GHZ coherence sign is fresh, fair, and independent of the device record. Multiplication by that sign cancels the diagonal bias contribution. Omitting or correlating it is not part of the defined procedure. |
| **D25. Two transverse planes** | Both complex transverse powers are measured. Their divided phases determine the two local angular coordinates; one phase is not treated as determining an arbitrary Bloch direction. |
| **D26. Principal argument** | The accepted-stage cone places the relevant phases strictly inside the principal interval. The reconstruction is a local argument with its own Lipschitz bound and legal exceptional-record conventions. No unproved global unwrapping theorem is imported. |
| **D27. Dyadic rejection** | The new pseudocode returns at the first rejection, as requested. The proof identifies the preceding accepted scale on that exact branch and never continues the cone induction beyond it. |
| **D28. Stage budget** | Conditional allowances are summed over tested lengths. Stage-failure independence is not assumed. The matrix calibration uses the same proportional-to-length principle with fresh conditional product samples. |
| **D29. No extra logarithmic loss** | The qubit dyadic proof displays the `2^{-k}` and `k2^{-k}` sums. Section 56 repeats the corresponding calculation for calibration. Their worst-record bounds have no added `\log\log N` or `\log N` multiplier. |
| **D30. Fine-phase cost** | The tolerance `\zeta_*=c_*\delta\sqrt{m_*/N}` gives `m_*\zeta_*^{-2}=O(N\delta^{-2})`. Block length and number of repeated blocks are multiplied before the final call bound is stated. |
| **D31. Scalar converse** | Under `E=pI_d`, a call produces a Bernoulli bit independent of the input, and each conditional reference block is the same reduced state multiplied by the scalar outcome probability. Arbitrary adaptive training is a common processing of independent bits. Section 56 uses this argument in every dimension. |
| **D32. Learned code** | The learner returns a legal estimate, made rational with error slack. `cor:matrixlearnedcode77` then applies the deterministic matrix code. This processing uses no further calls; payload and reconstruction work are accounted for separately. |
| **D33. Learner implementation** | Sections 55–56 define and prove mathematical training algorithms, including finite budgets and legal outputs. The repository's finite identity and concentration-budget checks, and the written calibration proof, are not a complete physical-device learner or an empirical uniform-risk certificate. The separately implemented exact matrix codec acts on supplied data and is identified as such. |
| **D34. Structural companion** | `structural.tex` remains the inherited theory with fresh nondisturbing classical probes. Its process statements do not describe repeated use of the destructive quantum measurement in the quantitative article. |
| **D35. Historical corpus** | The preservation baseline is now v76: 296 native files and 658 complete-edition labels. The figures 266 and 557 concern v75 and remain in its historical record. Preserving files and labels does not provide a new independent review of every inherited theorem. `HISTORY_AND_PIPELINE_AUDIT.md` records this distinction. |
| **D36. Editorial conclusion** | The r50 judgment is retained verbatim. The present response supplies new mathematical scope and a finite construction, together with a shorter focused source graph, while preserving the original programme and journal objective. It does not represent the earlier editorial judgment as either a theorem defect or a later acceptance decision. |

## 5. Crosswalk to the twelve proof/pipeline acceptance gates

These are the twelve gates in **section 12 of `FROZEN_R50_PIPELINE_AUDIT.md`**. “Addressed in source” denotes a supplied statement, proof, or document; it is not a substitute for a future execution receipt or an independent human judgment.

| Gate | Status and evidence |
|---|---|
| **G01. Preserve the v76 theorems or strengthen them with complete proofs** | **Addressed in source.** The complete edition retains the v76 proof graph and its 658 labels. Sections 56 and 57 add full proofs of matrix learning and a finite exact matrix code. The preservation manifest and generated label checks determine the actual successor comparison. |
| **G02. Executable pseudocode with first-rejection termination** | **Addressed in source.** `lem:noiseblock76` supplies the exact branch rule, public cap, retained scale, and exceptional-record fallbacks. |
| **G03. One explicit confidence/resource ledger** | **Addressed in source.** The section 55 and 56 tables and the resource ledger allocate conditional failure probabilities, worst-record calls, maximum block length, and postprocessing costs. |
| **G04. Independent priority comparison of the four new objects** | **Pending independent human review.** The theorem-level comparison and specialist brief are supplied; the brief also includes `thm:matrixlearning77` and `thm:matrixcodec77`. Internal author-side checks do not close this gate. |
| **G05. Current channel/POVM learning comparison theorem by theorem** | **Addressed in source.** `editions/operational-comparison77.tex` and `LITERATURE_AUDIT.md` record the named theorem statements, access, losses, dimensions/ranks, accuracy, confidence, and the precise future-horizon conversion. |
| **G06. Separate arbitrary-dimensional geometry, qubit learning, and qubit coding** | **Addressed through explicit statements and proved extensions.** The inherited qubit theorems keep their scope. New sections 56 and 57 extend learning and exact finite coding to matrices by additional arguments. Different statistical, description, and arithmetic resources remain distinct. |
| **G07. Operational-ball proof before spectral volume** | **Retained.** `lem:matrixball76` precedes `prop:matrixvolume76` and the covering proof. The codec cardinality proof invokes these actual operational-ball estimates. |
| **G08. Identify general-dimensional rational-centre existence correctly** | **Strengthened with a separate construction.** The v76 density proof stays an existence proof. `thm:matrixcodec77` now supplies deterministic finite rational construction, exact encoding/decoding, and the optimal payload order; it makes no efficiency claim. |
| **G09. Compress the journal manuscript without deleting proofs** | **Addressed in the source organization.** `quantitative.tex` is self-contained around the current theorem chain. `main.tex` retains the complete corpus and is the research supplement; `structural.tex` remains separate. No uncreated supplementary entry point is required. |
| **G10. Rebuild exact submitted SHA and journal package** | **Execution-dependent gate.** The v77 source, publication, and read-only reconstruction records must identify the exact objects actually rebuilt. `SOURCE_HASHES`, `BUILD_RECEIPT`, `THEOREM_LOCATIONS`, and `PAGE_CHECKS` are generated after freezing. The journal package includes its active sources. A v76 receipt does not close this gate for v77. |
| **G11. Preserve false analytic aggregate flags** | **Retained.** Historical A2 replacement, B4 aggregate, C2 aggregate, eleven-paper aggregate, and whole-Theta-program flags remain false. The frozen model-specific dependency ledger is unchanged. |
| **G12. Do not equate finite checks/hashes with mathematical certification** | **Retained.** This response, the proof/history audits, and resource ledgers distinguish written proofs, finite computational evidence, reproducibility, independent priority, and human signatures. |

The audit's risk register is covered by the same crosswalk. P0-1 maps to R12/D27/G02. P1-1 maps to the open R03/G04 gate; P1-2 to R02/R04–R06; P1-3 to R07/R10; P1-4 to R11 and the proved extension in section 56; P1-5 to R15 and section 57; P1-6 to R16/R17; and P1-7 to R18/D33. P2-1 through P2-6 map respectively to D01, D02, D11, R07/D09, R15/D20, and R19.

## 6. Publication organization and evidence boundary

The focused entry `quantitative.tex` produces `paper.pdf`. It includes the complete active prerequisites for its current theorem chain. The separate `structural.tex` produces `STRUCTURAL_PAPER.pdf`. The full historical research entry `main.tex` produces `COMPLETE_REVISION.pdf` and preserves the earlier instrument, preparation, readout, structural, and numerical developments. `JOURNAL_PACKAGE.zip` contains the focused and structural submission sources; the complete edition remains available as the preserved research supplement.

The controlling reports, the predecessor manuscript, and the historical files are retained. This response does not reinterpret an older “pass”, code test, branch name, or certificate as a proof. The new algorithmic claims are supported by the displayed mathematical constructions, while executed code checks support their reported finite cases. Generated successor receipts establish which native, rendered, and packaged objects were actually reconstructed.

Independent specialist priority remains open. The revision neither changes that status through internal cross-checks nor asks it to carry any mathematical premise of the proofs. The submitted source is ready for that external comparison on the specific claims stated above.
