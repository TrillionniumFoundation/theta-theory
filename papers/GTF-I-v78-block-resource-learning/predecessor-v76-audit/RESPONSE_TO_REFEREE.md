# Response to v75/r49 — Revision 76

**Paper:** General Theta Foundations I, focused quantitative manuscript on the finite-use geometry of ordered binary measurements.

**Controlling external report:** `GENERAL_THETA_FOUNDATIONS_I_V75_REFEREE_REPORT_R49.md`, commit `4de14a3fe5c271c77de64e410e1bd67fa2e7dce8`, on `review/general-theta-foundations-i-v75-external-referee-r49-2026-10-04`.

**Controlling proof/pipeline audit:** `GENERAL_THETA_FOUNDATIONS_I_V75_PROOF_PIPELINE_AUDIT_R49.md`, commit `8ee073109d5911c6526ff81314bede13bafe9f6c`, on `review/general-theta-foundations-i-v75-proof-pipeline-audit-r49-2026-10-04`.

**Reviewed predecessor:** Revision 75, final head `16b78c8edef566300ea21300908854ad83455879`, with theorem-source parent `efa7b14e2a42c6276f6748f98e3a15f2da018db3`. Both controlling reports concern this object. Their frozen texts and exact identities accompany the revision.

We thank the referee for separating the validity of the v75 arguments from the question of their mathematical breadth. Revision 76 answers the principal breadth objection with three additional results: an intrinsic finite-use comparison for the complete binary effect body in every fixed input dimension, the matching covering law including all support and spectral strata, and a common statistical learner for the complete binary qubit effect body. The last result has matching upper and lower device-call bounds and is proved independently of the pair-dependent discrimination witnesses. The general-journal objective is retained. The inherited statements and their proofs remain available with their original hypotheses.

Two details identify the reviewed manuscript precisely. The quantitative title at the reviewed v75 head was *Finite-Use Geometry of Binary Qubit Measurements*, rather than the title given in the report's header. Also, v75 extended and retained the unbiased theorem of section 50; it did not remove that theorem. The reported commit, formulas, source sections, and compiled objects otherwise identify the intended predecessor. These corrections do not affect the mathematical questions raised by the reports.

## Principal mathematical response

### The complete binary effect body in arbitrary input dimension

For each integer `d>=1`, the target is

\[
 \mathfrak E_d=\{E=E^*\in M_d(\mathbb C):0\preceq E\preceq I_d\}.
\]

The device has the ordered effects `E,I_d-E`, consumes its input, and returns its classical outcome with no residual quantum output. The metric `d_N` uses the unhalved trace norm and allows a retained reference, common adaptive operations, and at most `N` calls with bounded public stopping. Its nonadaptive restriction permits entangled input blocks. Both distances are suprema over tests that may depend on the known pair. Equation `eq:matrixoneuse76` gives the exact normalization

\[
 d_1(E,F)=2\|E-F\|_{\rm op}.
\]

Put `M=(E+F)/2`, `H=F-E`, and `V_M=M(I_d-M)`. The new intrinsic comparison modulus is

\[
 Q_N(E,F)^2
 =N\left\langle H,
 (L_{V_M}+R_{V_M}+N^{-1}{\rm Id})^{-1}H\right\rangle_{\rm HS}.
\]

Here `L` and `R` denote left and right multiplication on the real Hilbert space of Hermitian matrices. The definition is independent of any eigenbasis choice, including at repeated eigenvalues. Theorem `thm:matrixmetric76`, in `sections/53-matrix-effect-metric.tex`, proves

\[
 \frac1{8192d}\min\{1,Q_N(E,F)\}
 \le d_N^{\rm na}(E,F)\le d_N(E,F)
 \le\min\{2,8Q_N(E,F)\}.
\]

This is a uniform comparison for all pairs and all horizons. The constants are not optimized, and `Q_N` is not asserted to be an exact distance or to satisfy a triangle inequality. The theorem includes arbitrary ranks, noncommuting effects, repeated spectra, and all intermediate support faces. Corollary `cor:matrixadaptivity76` also bounds the advantage of feedback in this binary interface by `65536d` at the level of these trace distances.

The upper proof gives an explicit horizontal measurement dilation. Writing `S=sqrt(G(I_d-G))`, its derivative in a tangent direction `SK+KS` has `W* dot W=0` and `dot W* dot W=K^2`. Differentiated insertions at distinct calls are therefore orthogonal in every purified common tester. A regularized Sylvester equation

\[
 SK+KS+N^{-1/2}K=H
\]

splits a general tangent into this horizontal part and a remainder controlled by the hybrid bound. Integrating the resulting path inequality, and using operator concavity of `G(I_d-G)` along a straight segment, gives the finite-pair upper estimate. The proof works first in the interior and passes to the closed body with the fixed `1/N` cutoff. Horizontal gauge and channel-extension methods have established antecedents, which the revised literature comparison credits; the new assertion is the displayed boundary-uniform matrix comparison with its matching witnesses and consequences.

For the converse, a diagonal entry in an eigenbasis of `M` is tested by repeated Bernoulli input. An off-diagonal entry is tested inside the corresponding two-dimensional compression. The compressed channel is exactly a binary qubit channel, so the preserved v75 nonadaptive theorem applies. The identity

\[
 V_M=\tfrac12V_E+\tfrac12V_F+\tfrac14(F-E)^2
\]

on that compression controls its two endpoint variances without subtracting lower bounds. The strongest matrix entry has size at least `Q_N/d` in the weighted norm. Lemma `lem:matrixspectral76` additionally proves spectral noncancellation for each ordered eigenvalue in every input dimension by an intersecting-subspaces argument.

### The full-dimensional covering law and its logarithmic multiplicity

Theorem `thm:matrixcover76`, in `sections/54-matrix-effect-entropy.tex`, proves that for every fixed `d` there are `c_d,C_d,delta_d>0` such that for all `N>=1` and `0<delta<=delta_d`,

\[
 c_dN^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}
 \le\mathcal C_N(\mathfrak E_d,\delta)
 \le\mathcal C_N^{\rm rat}(\mathfrak E_d,\delta)
 \le C_dN^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}.
\]

Centres may be any legal memoryless ordered binary measurement of the same input dimension. The superscript `rat` restricts centres to rational real and imaginary matrix entries. The corresponding optimum fixed-length reusable payload, on this same small-error range, is

\[
 \frac{d^2}{2}\log_2N
 +\lfloor d/2\rfloor\log_2\log(N+2)
 +d^2\log_2(1/\delta)+O_d(1).
\]

The proof establishes an actual measure estimate for operational balls. The determinant density of the regularized matrix form defines a measure `mu_N`. Lemma `lem:matrixball76` proves, uniformly at every point of the closed effect body, that sufficiently small radius-`r` operational balls have measure comparable to `r^(d^2)`. At a support boundary the lower proof explicitly moves inward by a distance proportional to `r/N` and places a full legal ellipsoid inside the operational ball. No fixed proportion of an ambient ellipsoid is assumed at a singular stratum.

Proposition `prop:matrixvolume76` evaluates the total regularized volume. In spectral coordinates the Vandermonde factor and the matrix-form determinant produce coupled endpoint singularities. Ordering endpoint depths gives cumulative exponents `A_j=S_j^2/2`, where `S_j` is the difference between the numbers of eigenvalues approaching zero and one in a prefix. A vanishing prefix can occur at most `floor(d/2)` times. Separated, nested pairs of eigenvalues approaching opposite endpoints give a matching lower bound. Thus the logarithmic power is determined by the complete spectral integral, including all nested endpoint scales. For dimensions three and four, the covering orders are respectively `N^(9/2) log(N+2) delta^-9` and `N^8 [log(N+2)]^2 delta^-16`, on their stated small-error ranges.

Rational legal centres are obtained by density and a constant-factor radius allowance. This is an existence theorem in arbitrary dimension. The implemented exact optimal encoder remains the separate full qubit construction `thm:biasedcodec75`. In that implementation, the schema parameter `dimension` taking values two or three counts Bloch coordinates of a qubit slice or body; it is not the Hilbert input dimension of the new matrix theorem.

### A common learner, with matching device-call complexity

Theorem `thm:commonlearn76`, in `sections/55-common-measurement-learning.tex`, supplies a separate common experiment for the complete ordered binary qubit effect body. For `N>=1`, sufficiently small `delta>0`, and `0<eta<=1/8`, it returns a legal estimate `Ehat` with

\[
 \sup_{E\in\mathfrak E_2}
 \Pr_E\{d_N(E,\widehat E)>\delta\}\le\eta,
\]

using at most `C N delta^-2 log(1/eta)` training calls on every record. Every entangled block has length at most `N`. A matching lower bound `c N delta^-2 log(1/eta)` holds for any common learner under the same worst-record call convention. Here `N` is the future horizon used to measure the estimate's loss; it is distinct from the number of training calls.

The learner first selects a contrast regime from a fixed coarse experiment. At low contrast it uses variance-sensitive product observations, followed by fresh endpoint observations along the estimated direction. At high contrast a random sign cancels the unknown bias in a GHZ parity statistic. Two transverse planes recover both angular components. Empirical amplitudes select a block length without prior knowledge of the noise. The dyadic stage costs form a summable weighted series, so no additional `log log N` factor is needed in the call bound. Fresh endpoint samples then recover the spectrum. The lower bound uses the scalar Bernoulli subfamily and relative entropy, and applies to arbitrary common adaptive training operations.

For rational requested accuracy, the estimate can be rounded to a legal rational effect and encoded with the preserved qubit code, using radius slack and no further device calls. Its payload has the same optimal qubit order on the established small-error range. This statistical theorem is proved for qubits; the arbitrary-dimensional metric and covering theorems stand independently. Neither an optimal classical runtime nor a physical measurement processor is inferred from the device-call bound.

## Twenty required revisions

The identifiers follow section 7 of the controlling r49 report. They are a new response to r49, not a relabelling of the r48 response preserved under `predecessor-v75-audit/`. Source labels are stable audit anchors; generated theorem locations identify the corresponding compiled statements.

| Item | Response and source location |
|---|---|
| R01. Independent focused article | `quantitative.tex` is the journal-facing entry point, with its own active introduction, comparison, and bibliography. It places the matrix metric, entropy, and common learner first, followed by the qubit metric/code and an appendix retaining the earlier supporting proofs. The complete research edition keeps the historical order and appends the new results; the structural companion remains separately buildable. The README identifies the focused manuscript, native source, and this response directly. |
| R02. Precisely qualified headlines | The principal scope is now ordered binary measurements in arbitrary input dimension, because `thm:matrixmetric76` and `thm:matrixcover76` prove the full matrix-body assertions. Dimension dependence and the absence of residual quantum output are explicit. The common learner and implemented optimal codec remain explicitly qubit results. Every use of the full effect body refers to its stated ordered binary interface. |
| R03. Krawiec–Pawela–Puchała | The active comparison and bibliography include *Discrimination of POVMs with rank-one effects*, QIP 19 (2020), 428, arXiv:2002.05452, key `KPP76`. The comparison distinguishes its finite perfect-discrimination criteria and its two-use adaptive example for a nine-outcome qutrit SIC pair from the present binary quantitative comparison and covering problem. Its adaptive example is not a binary-outcome counterexample to `cor:matrixadaptivity76`. See `LITERATURE_AUDIT.md`. |
| R04. Nonprojective entanglement-assisted boundary | The active comparison includes Datta–Biswas–Saha–Augusiak, NJP 23 (2021), 043021, arXiv:2012.07069, key `DBSA76`. Its single destructive measurement and outcome-conditioned reference measurement, including the three-outcome qubit advantage in Theorem 5, are distinguished from finite-use geometry, body entropy, and future-horizon learning. No multiple-use or covering conclusion is attributed to that paper. |
| R05. Independent priority review | `INDEPENDENT_REVIEW_BRIEF.md` identifies the new matrix comparison, nested-endpoint entropy, and common learner, together with their direct antecedents. No independent human specialist opinion has been obtained or represented as obtained. The author-side proof and literature audits provide material for that review and do not substitute for it. |
| R06. Metric versus covering range | The abstract and principal statements separate the all-pair/all-horizon comparison `thm:matrixmetric76` from the small-error covering theorem `thm:matrixcover76`. The common learner has its own accuracy and confidence ranges. No small-error statement is promoted to a result uniform over all errors below two. |
| R07. Comparison up to constants | Both the inherited `H_N` and the new intrinsic `Q_N` are comparison moduli. Theorems `thm:biasedmetric75` and `thm:matrixmetric76` keep explicit inequalities. Exact identities are confined to the proved one-use normalization, scalar Bernoulli problem, and separately identified inherited exact projective results. |
| R08. Payload error cap | The matrix payload formula is stated for `N>=1` and `0<delta<=delta_d`; the qubit payload and learning-code consequence retain their common sufficiently small-error range. The existence or validity of a particular code at a larger error does not extend the matching converse. See `eq:matrixbits76`, `thm:biasedcodec75`, and the resource ledger. |
| R09. Arbitrary legal centres | The v75 packing converse is retained. The v76 converse uses the uniform upper measure bound for every operational ball in the full body, so its centre can be any legal memoryless binary effect of the stated input dimension. Neither converse restricts centres to a spectral box, a fixed rank, a commuting family, or the centres of the upper construction. |
| R10. Pair-dependent witnesses and a separate common learner | The known-pair quantifier remains explicit in `thm:matrixmetric76` and `lem:matrixspectral76`. Theorem `thm:commonlearn76` separately constructs a single data-dependent experiment, independent of the unknown qubit effect, and proves its uniform risk. Its decision tree, conditional concentration, training cost, and minimax converse are supplied rather than inferred from a packing witness. |
| R11. Both endpoint probabilities | Section 51 retains `V=p(1-p)+q(1-q)` and `K_N=(p-q)sqrt(N/(V+1/N))`, including scalar and one-sided-face conventions. The matrix theorem uses the entire variance matrix `E(I-E)` and its left-plus-right action. No distance to a single support face is substituted. |
| R12. Dilation mechanism before asymptotics | Section 51 retains the exact pairwise scalar overlap and its iteration through a common tester before converting the finite bound to the angular scale. The new introduction explains the horizontal construction, and section 53 gives its derivative identities, regularized Sylvester equation, and finite path estimate before the geometric consequences. The environments remain inaccessible and the observed channel stays fixed. |
| R13. One-use normalization | The operational model displays `d_1(E,F)=2||E-F||op` beside the definition of the finite-use distance. Equations `eq:matrixoneuse76` and `eq:biasedoneuse75` provide the reference-assisted duality proof and the qubit Cartesian form. Classical total variation is half the corresponding classical trace norm. |
| R14. Coding, learning, and implementation | The exact qubit codec still encodes supplied rational Cartesian data. Section 55 supplies a new, separately analysed training experiment before coding an estimate. Training calls, reusable payload, classical arithmetic, input length, workspace, expanded output, quantum memory, and trusted preparation/hardware are distinct resources. No physical processor or optimal classical runtime follows from either theorem. |
| R15. Actual complexity | The inherited exact layout uses `O(B^2)` arithmetic operations and `O(B)` retained spectral values and row starts, with `B=ceil(sqrt(64N/delta^2))`. No polynomial bound in all encoded numerical lengths is claimed. The new learner's complexity statement concerns device calls. The full-dimensional rational-centre theorem is existential and is not described as an implemented optimal encoder. |
| R16. Exact submitted-source verification | The revision's reconstruction protocol binds native source, focused package, PDFs, theorem locations, and emitted checks to the source object actually recorded. Final-head verification is read-only and must identify the actual submitted SHA. The successful v75 reconstruction remains predecessor evidence. New success and numerical counts are asserted only through the corresponding generated record, not inferred from an earlier source parent. |
| R17. Human authorship signature | No human signing credential has been used or human signature asserted. Source hashes and an exact-head reconstruction identify bytes and execution results; they do not establish human authorship. The conditional request for a signed release is therefore recorded honestly, without relabelling an unsigned revision as signed. |
| R18. Structural companion | The structural article remains separate and inherited. Its fresh, classical, nondisturbing-probe assumptions are retained. It is not counted as a new consequence of the binary matrix geometry or common learning theorem. |
| R19. Analytic A/B/C/D flags | The separate analytic dependency graph and aggregate completion flags are retained in `HISTORY_AND_PIPELINE_AUDIT.md` and `PROOF_STATUS.json`. Neither finite-dimensional measurement geometry, device learning, exact arithmetic tests, nor reconstruction supplies any of the unrelated analytic proofs. |
| R20. Focused exposition and preserved history | The focused introduction and comparison centre the intrinsic matrix form, its boundary-uniform proof, the nested-endpoint entropy, and the separate common qubit learner. These new results precede the retained qubit metric and code. The earlier Choi, validation, and sections 38–50 supporting proofs remain active in the focused appendix. The full edition retains its historical development, while inherited author documents and the original comparison are preserved in archival paths. No supporting proof or inherited theorem label is removed by the reordering. |

## Thirty-six detailed comments

These identifiers follow section 8 of r49 independently of the required-revision list.

| Comment | Treatment |
|---|---|
| D01. Identifiable dimension | The qubit effect body has real dimension four; `p=q` has no direction. The arbitrary-dimensional body is the real `d^2`-dimensional set of Hermitian effects itself. Its new form is coordinate-free, and the spectral integral includes the correct unitary-orbit Jacobian rather than treating a redundant spectral tuple as a regular chart. |
| D02. Ordered labels | The target effects remain ordered. A common outcome swap used in a qubit lower witness is a stated operation of that tester; it does not identify two labelled targets. The new matrix theorem and learner keep the same convention. |
| D03. Unhalved norm | The exact one-use normalization and the classical total-variation factor are retained throughout. The scalar lower experiment in the learning theorem uses the same unhalved finite-use loss. |
| D04. Horizon cutoff | The regularizer is exactly `N^-1`. In the symmetric notation `W_E=E(I-E)+(2N)^-1 I`, left plus right multiplication adds precisely `N^-1 Id`. This is the same finite-horizon regularization, not a new free smoothing parameter. |
| D05. No-success statistic | The Bernoulli block statistic remains a lower-bound device. The exact scalar problem is the full product-Bernoulli distance. No optimal decision rule is inferred from the statistic. |
| D06. Separate spectral witnesses | The two qubit endpoint witnesses remain separate. Lemma `lem:matrixspectral76` extends the statement to each ordered eigenvalue by a separate intersecting-subspaces experiment. Neither result claims simultaneous eigenvalue recovery from one eigenstate. |
| D07. Row-programme upper bound | The aligned two-row representation remains an upper programme bound. The arbitrary-dimensional aligned result uses `d` rows and bounds their product distance by the sum of row distances. No exact tensor-product equality for every commuting pair is asserted. |
| D08. Pairwise overlap | The scalar-overlap gauge in section 51 remains pair-specific. The new horizontal construction is local to a matrix and tangent. Neither construction is advertised as a global environment seizer for the effect body. |
| D09. Inaccessible environment | Section 53 realizes the prescribed derivatives by genuine factors with exactly unchanged effects; only the factor environment is rotated. The observed classical output and retained reference channel therefore remain the required measurement. Environment retention is solely a proof device for the upper bound. |
| D10. Public stopping | The at-most-`N` tester is padded by ignored calls on fixed dummy inputs. Public stopping is included, with no free hidden stopping record. The learning theorem separately gives a worst-record training-call cap even on exceptional records. |
| D11. One-sided singular face | `rem:biasedfaces75` retains the formula `K_N(p,0)=p sqrt(N/(p(1-p)+1/N))`. At fixed `0<p<1` this has square-root horizon order. Deterministic and projective endpoints are treated separately. The new figure labels the corresponding face. |
| D12. Scalar interval | At `p=q=t` the direction is absent and `d_N=B_N(t,t')` exactly. Scalar code layers have one word. This exact subfamily also supplies the lower bound for common learning; it is not assigned an angular coordinate. |
| D13. Projective endpoint | The inherited exact projective result is preserved. The new qubit and matrix formulas remain uniform comparisons. The projective fibre in the figure is labelled separately from a one-sided rank face. |
| D14. Nonoptimal constants | The constants `1/8192`, `1/(8192d)`, `8`, and the ensuing adaptivity factor are intentionally conservative. Neither finite regression nor a plot is used to claim their numerical optimality. |
| D15. Nonadaptive quantifier | The metric lower theorem takes the supremum over common tests chosen for each known pair. The common qubit learner is a different theorem with an explicit uniform statistical decision tree and its own call count. These two quantifiers are not interchanged. |
| D16. Both qubit depths | The preserved projective-corner construction discretizes both `alpha=1-p` and `beta=q`, as well as the angular coordinates. The new full-dimensional lower volume uses paired eigenvalue depths at both support endpoints, including independently nested pairs. |
| D17. Cross-scale separation | The v75 packing proof retains actual spectral endpoint tests between separated depth boxes. The new covering proof uses the proved operational-ball measure theorem; disjoint spectral integration boxes evaluate total measure and are not silently assumed to be a metric packing. |
| D18. Source of logarithms | The v75 lattice count keeps its horizon cutoff, excluding an extra `log(1/delta)`. In v76 the total spectral integral has `floor(d/2)` critical balanced prefixes and depends on `N`; the radius contribution is separately `delta^-d^2`. Every nested endpoint scale is included. |
| D19. Scalar code layers | The inherited exact code retains one word when the two spectral indices coincide. No angular digits are assigned to that word. The scalar collapse is also shown in the figure. |
| D20. Chart overlap | All signed stereographic chart words, including overlaps and ties, are counted in the exact qubit capacity. The arbitrary-dimensional volume proof uses the standard matrix Jacobian with its finite orbit/permutation constants, not an informal chart quotient. |
| D21. Signs before squaring | The exact rational encoder retains its sign tests before every radical squaring comparison, and the corresponding negative controls remain part of the finite suite. No floating-point comparison is substituted. |
| D22. One charged payload | The payload is one integer index into the full legal code. Syntax, tables, and expanded Choi data are accounted for separately. The learner's final qubit word uses this same union code after a stated accuracy allowance. |
| D23. Public and target parameters | Public horizon, requested tolerance, and declared interface dimension are separate from target data. Bias, spectrum, contrast, direction, and matrix coordinates are charged by the relevant covering index. The common learner obtains its target information from device observations. |
| D24. Legality and replay | Every in-range word decodes to a legal measurement. Deterministic target-bound replay checks that the supplied target selects that exact canonical word under the tie rules; it is not an injective identifier of targets or a universal distance oracle. Approximation follows from the proved encoder and its construction budget. |
| D25. Cache validation | Type and range validation remain before the cached layout lookup, including the Boolean/integer collision case after a valid key has populated the cache. The implementation and regression preserve this invariant. |
| D26. Finite capacity evidence | Capacity samples remain finite regression evidence. The qubit lattice bound is proved in section 52; the full-dimensional total-volume law is proved in section 54. The latter is not inferred from computed examples in several dimensions. |
| D27. Evidence boundary | The build receipt and this audit distinguish written proofs from finite arithmetic assertions, rendered-page checks, and byte reconstruction. Finite checks do not quantify over the adaptive supremum, the entire continuum, all training records, or unbounded horizons. |
| D28. Fresh-probe structural result | The structural companion concerns its stated fresh classical probe interface. It is not reinterpreted as repeated quantum measurement of the same system. The learner uses fresh prepared qubits or finite entangled blocks under an explicitly different model. |
| D29. Earlier width gap | The recorded v63 exponential-width multiplicative gap remains in the history audit. Matrix description entropy and training complexity do not discharge that separate obligation. |
| D30. Unsigned provenance | An unsigned publication or reconstruction record is not called a human signature. Any claim about the current source and checks must name their actual recorded object. |
| D31. Number of outcomes | The new matrix theorems still concern exactly two ordered outcomes. The added multi-outcome references make this distinction explicit. No theorem for arbitrary POVMs with three or more outcomes follows formally from the binary Sylvester form or its two-dimensional witnesses. |
| D32. Higher-dimensional strata | The report's observation is accurate for v75. Revision 76 supplies a new proof for the complete effect body in each fixed dimension, including noncommuting effects and all spectral multiplicities. Its intrinsic form, local ball theorem, and unitary-orbit integral address those strata directly. Constants and error caps depend on dimension; no dimension-independent or multi-outcome assertion is made. |
| D33. Supplied data and learned data | The inherited codec continues to start from exact rational Cartesian data. Section 55 separately learns a qubit effect from calls, rounds the resulting estimate legally, and then invokes the codec. It does not treat the unknown exact matrix as an oracle or claim a full-dimensional learner. |
| D34. Centre class | Covering centres remain legal memoryless measurements of the declared interface. Time-varying simulators are a different centre class and are not included in these converses. Adaptive testing of a fixed centre does not change that convention. |
| D35. Priority and history | Historical volume and preserved theorem counts establish continuity, not priority. The comparison identifies direct primary results and imported methods. The new full-dimensional and learning conclusions are supplied for independent specialist assessment. |
| D36. Stratum schematic | Figure `fig:effectbody76` shows the exact qubit spectral triangle and a separately labelled section `x_3=0` of the four-dimensional effect body. The caption distinguishes the scalar collapse, one-sided faces, projective `S^2` fibre, and the projective `S^1` in the section. It is an explanatory diagram, not evidence for an estimate. |

## Other detailed findings in the controlling reports

The seven correctness subsections in external-report section 3 concern the Bernoulli endpoint estimate, reference-assisted row programme, scalar-overlap dilation, public stopping, projective-corner packing, cutoff lattice sum, and code legality/replay. All seven arguments are preserved in sections 51–52 and the exact qubit implementation. Their scope and evidence distinctions are addressed above. The new matrix theorem uses the already reviewed qubit lower comparison as an explicit two-dimensional dependency, while supplying its own all-dimensional upper proof and entropy calculation.

The proof/pipeline audit's mathematical, scope, priority, reproducibility, and editorial gates are addressed by the same itemized changes. Its independent analytic graph remains

`A1 independent; A2 -> A3 -> A4 -> C2 -> D1; B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`.

Raw local limits, stopped-path entropy/LDP recovery, the past kernel, exact conditioning, process limits, Mosco/Nisio obligations, filtering/LAN, changing-filtration response, and labelled posterior contraction remain separately recorded requirements. The new finite-dimensional theorem chain supplies no replacement proof for them.

## Preservation, verification, and further assessment

The reviewed v75 directory and all earlier revision paths remain available. The prior author response and written-proof audit are preserved under `predecessor-v75-audit/` before replacement here. `PRESERVATION_MANIFEST.json` and the generated theorem map account for inherited source and labels; counts should be read from those records rather than inferred from the length of the manuscript.

`PROOF_AUDIT.md` independently traces the new horizontal path bound, compression lower witnesses, legal boundary ellipsoids, nested spectral integral, and common learner, together with their retained qubit dependencies. Reproducibility records under `evidence/` identify the source hashes, actual finite tests, page checks, compiled theorem locations, and build receipt. A read-only final-head reconstruction establishes only what its stated commit and checks record. Neither that reconstruction nor this author-side audit is an independent human priority opinion or an authorship signature.

The revision supplies a full-dimensional quantitative theorem and a separate common learning theorem for further referee assessment while preserving the reviewed mathematics. Independent human priority clearance and human author signing are not supplied by this author-side revision. The significance and acceptance of the resulting manuscript remain matters for the referee and editor.
