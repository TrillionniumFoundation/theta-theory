# Theorem-level literature comparison — Revision 76

Primary sources checked on 4 October 2026. This author-side comparison addresses the v75 referee report r49 and the antecedents relevant to the new matrix theorem. The preceding comparison is preserved in full in `predecessor-v75-audit/LITERATURE_AUDIT.md`. No outside reviewer was contacted or commissioned; this document records source comparisons and does not represent independent priority clearance.

## Objects submitted for comparison

The target class is the entire matrix interval
\[
\mathfrak E_d=\{E=E^*:0\le E\le I_d\},\qquad
\mathcal M_E(\rho)=\operatorname{tr}(E\rho)|1\rangle\langle1|
+\operatorname{tr}((I-E)\rho)|0\rangle\langle0|.
\]
The outcomes are ordered. Calls are memoryless and consume the input; a tester can retain a reference and use intermediate channels and classical feedback. Trace distance is unhalved. The dimension is arbitrary but fixed; covering constants may depend on it.

Section 53, **thm:matrixmetric76**, compares the nonadaptive and adaptive distances for every pair and every finite horizon. With \(M=(E+F)/2\), \(H=F-E\), \(V=M(I-M)\), and left and right multiplication denoted by \(L,R\),
\[
Q_N(E,F)^2=N\langle H,(L_V+R_V+N^{-1}\mathrm{Id})^{-1}H\rangle_{\mathrm{HS}},
\]
and
\[
\frac{\min(1,Q_N)}{8192d}\le d_N^{\mathrm{na}}(E,F)
\le d_N^{\mathrm{ad}}(E,F)\le\min(2,8Q_N).
\]
Section 54, **thm:matrixcover76**, gives, uniformly in \(N\ge1\) and in a sufficiently small positive error range depending only on \(d\),
\[
\mathcal C_N(\mathfrak E_d,\delta)\asymp_d
N^{d^2/2}[\log(N+2)]^{\lfloor d/2\rfloor}\delta^{-d^2}.
\]
The lower bound allows arbitrary legal centres; rational legal centres achieve the same order. Section 55 separately gives a common unknown-device learner on the full binary **qubit** body, with training cost of order \(N\delta^{-2}\log(1/\eta)\) for loss \(d_N\) and failure probability \(\eta\). The matrix covering theorem and qubit learning theorem have different dimension ranges. The inherited explicit qubit codec and earlier structural and geometric results remain active with their own hypotheses.

## Measurement discrimination: direct antecedents

**Fiurášek–Mičuda (2009), FM75.** [Full text](https://arxiv.org/pdf/0909.2940), [published article](https://doi.org/10.1103/PhysRevA.80.042312). Sections I, III and IV compare two-use projective-qubit protocols; equation (16) treats adaptive product probes and equations (27)–(30) give entangled feed-forward constructions. Their interface excludes additional ancillary measurements. This restriction matters when comparing with the later reference-assisted projective theorem.

**Sedlák–Ziman (2014), SZ74.** [Full text](https://arxiv.org/pdf/1408.0934), [published article](https://doi.org/10.1103/PhysRevA.90.052312). Theorem 1 characterizes perfect single-use discrimination of binary measurements. Section VI, Example 4, equation (37), allows unequal white-noise visibilities and reduces the one-use problem to mixed-qubit-state discrimination. Those effects are unbiased. For \(E=((1+b)I+x\cdot\sigma)/2\), the elementary identity \(\Gamma(E)-(I-E)=bI\) explains why this particular spin-flip reduction does not itself treat bias.

**Puchała–Pawela–Krawiec–Kukulski (2018), PPKK74.** [Full text](https://arxiv.org/pdf/1804.05856), [published article](https://doi.org/10.1103/PhysRevA.98.042103). Theorem 1, equation (19), represents the single-use diamond distance between von Neumann measurements by a minimization over diagonal phases of a unitary-channel distance. Assigning this representation to arbitrary nonprojective effects would require another argument.

**Puchała–Pawela–Krawiec–Kukulski–Oszmaniec (2021), PPKKO72.** [Full text](https://arxiv.org/pdf/1810.05122v4), [published article](https://quantum-journal.org/papers/q-2021-04-06-425/). Corollary 1 gives an exact finite-use parallel distance for von Neumann measurements; Theorem 2 proves optimality among general networks with ancillary access. This supplies an exact projective endpoint. The new constant-factor comparison does not assert exact parallel optimality for all effects.

**Krawiec–Pawela–Puchała (2020), KPP76, requested in r49.** [Full text](https://arxiv.org/pdf/2002.05452v1), [published article](https://doi.org/10.1007/s11128-020-02883-3). Sections 2–3 allow retained references and adaptive intermediate channels and study finite-use perfect discrimination of rank-one POVMs. Section 4 constructs two differently ordered nine-outcome qutrit SIC measurements admitting a two-use adaptive perfect test but no finite parallel perfect test. This is a direct repeated-measurement antecedent. It concerns two hypotheses, not two outcomes. The checked results do not give the present binary-body midpoint comparison or covering law. Requiring both effects of a binary qubit POVM to have rank one forces a projective measurement; for \(d>2\) their ranks cannot sum to \(d\).

**Datta–Biswas–Saha–Augusiak (2021), DBSA76, requested in r49.** [Full text](https://arxiv.org/pdf/2012.07069v2), [published article](https://doi.org/10.1088/1367-2630/abecaf). A destructive unknown measurement on one half of an entangled input is followed by an outcome-dependent known measurement on the reference. Theorem 1 relates entanglement advantage to steerability; Theorems 2–4 construct perfect-discrimination examples with multiple outcomes. Theorem 5 gives an advantage using any pure entangled two-qubit state for a pair of three-outcome POVMs. These are single-use results; their hypothesis and outcome counts must remain distinct in the comparison.

## Kraus geometry and finite-use channel bounds

**Fujiwara–Imai (2008), FI76.** [Publisher](https://doi.org/10.1088/1751-8113/41/25/255304), [author-uploaded full text](https://www.researchgate.net/publication/231040616_A_fibre_bundle_over_manifolds_of_quantum_channels_and_its_application_to_quantum_statistics). Theorem 4 expresses maximal reference-assisted quantum Fisher information through minimization over differentiable Kraus representations. Theorem 5 identifies a vanishing Kraus cross derivative that gives linear growth for repeated parallel use. Horizontal Kraus lifts and the orthogonality mechanism are established tools.

**Channel extension and adaptive bounds.** Demkowicz-Dobrzański–Kołodyński–Guţă (2012), DKG67, [full text](https://arxiv.org/pdf/1201.3940v2), equations (10)–(13) in this arXiv version, bound parallel quantum Fisher information using the usual Kraus quantities \(\alpha,\beta\). Demkowicz-Dobrzański–Maccone (2014), DM76, [full text](https://arxiv.org/pdf/1407.2934v3), equation (9), gives an adaptive bound whose \(\beta=0\) specialization is \(4N\|\alpha\|\). Kurdziałek–Górecki–Albarelli–Demkowicz-Dobrzański (2023), KGAD76, [full text](https://arxiv.org/pdf/2212.08106v2), equations (5)–(9), provides an adaptive recursion with the same specialization. Cancellation under arbitrary controls is accordingly credited to the existing method.

**Integration to finite pairs.** Yuan–Fung, YF76, [full text](https://arxiv.org/pdf/1506.00819v3), Section III, equation (26), integrates quantum Fisher information along a path to bound the Bures angle between finite channel hypotheses in parallel discrimination. Sieniawski–Demkowicz-Dobrzański (2026), SD76, [full text](https://arxiv.org/pdf/2510.15506v3), Section IV.A, equations (14)–(22), uses this connection with adaptive metrological bounds. The latter expressly cites the earlier integration argument. Neither passage from a differential bound to a finite path nor its adaptive use is claimed as new here.

Section 53 instead supplies a specific Sylvester construction involving \(\sqrt{E(I-E)}\) for a binary qc dilation, controls a residual derivative at the finite-horizon scale, and integrates the straight segment to obtain the displayed midpoint resolvent. Legal scalar and two-dimensional compressions give its matching lower estimate. This explicit closed-body comparison is the object requiring priority assessment; a general local Fisher information bound alone does not identify it.

## Inverse Sylvester forms and spectral volume

**Dittmann (1999), Dittmann76.** [Full text](https://arxiv.org/pdf/quant-ph/9808044), [published article](https://doi.org/10.1088/0305-4470/32/14/007). Equations (1)–(2) give the Bures tensor on the positive matrix cone as
\[
g^B_W(H,H)=\tfrac12\langle H,(L_W+R_W)^{-1}H\rangle.
\]
Algebraically, \(Q_N^2/N=2g^B_W(H,H)\) at \(W=M(I-M)+(2N)^{-1}I\). The inverse Sylvester form itself is classical. This identity is not a Bures pullback through the variance map: that map has differential \(H-MH-HM\), whereas the operational comparison retains \(H\).

**Sommers–Życzkowski (2003), SZGeom76.** [Full text](https://arxiv.org/pdf/quant-ph/0304041), [published article](https://doi.org/10.1088/0305-4470/36/39/308). Section III, especially equations (3.12)–(3.17), develops spectral coordinates, the eigenvalue Jacobian and volume integration for Bures geometry. These are antecedents for calculating a unitarily invariant matrix volume. Its normalized state body and metric differ from the effect interval and finite-horizon variance tensor here.

In Section 54 the determinant computation yields a spectral density proportional to
\[
N^{d^2/2}\prod_i[2\lambda_i(1-\lambda_i)+N^{-1}]^{-1/2}
\prod_{i<j}\frac{(\lambda_i-\lambda_j)^2}
{\lambda_i(1-\lambda_i)+\lambda_j(1-\lambda_j)+N^{-1}}.
\]
The proof establishes uniform volume bounds for operational balls on the closed matrix interval before deriving coverings from this integral. It then counts nested scales near the two opposite spectral endpoints: balanced endpoint prefixes produce \(\lfloor d/2\rfloor\) logarithmic factors. The checked sources do not state this asymptotic or its operational covering consequence. That is a bounded search result, not proof that an equivalent result cannot exist elsewhere.

## Common estimation and its resource model

**Mele–Bittel (2026), MB67.** [Version checked](https://arxiv.org/pdf/2512.10214v3). Lemmas III.7–III.8 give the binary identity \(\|\mathcal M_E-\mathcal M_F\|_\diamond=2\|E-F\|_{\mathrm{op}}\) and conversion of a channel estimate to a legal effect. Corollary III.9 gives a common binary-POVM estimator of fixed-confidence cost \(O(d^2/\epsilon^2)\). The construction uses independent maximally entangled probes followed by collective processing of Choi outputs. Genuine common estimation is therefore already established; the present comparison concerns its loss and training scale.

**Zambrano–Ramos-Calderer–Kueng (2026), ZRK76.** [Version checked](https://arxiv.org/pdf/2507.04500v3), [published article](https://quantum-journal.org/papers/q-2026-07-15-2162/). Definition 1 uses worst-input one-use outcome total variation without an ancillary reference. Theorem 2 gives worst-case tomography cost \(O((d^3+d^2L)/\epsilon^2)\) for \(L\) outcomes using single-copy known probes, with bounds appropriate to that probe model. For binary effects the loss is \(\|E-F\|_{\mathrm{op}}\).

**Bisio–D'Ariano–Perinotti–Sedlák (2011), BDPS76.** [Full text](https://arxiv.org/pdf/1103.0480v2), [published article](https://doi.org/10.1016/j.physleta.2011.08.002). Their learning and retrieval network stores information from an unknown von Neumann measurement in quantum memory and later reproduces a measurement on a new input. The paper optimizes training with one and two examples and identifies a nonparallel feature with three examples. That stored programme and retrieval criterion differ from the present high-probability classical estimate.

**Multiscale phase methods.** Higgins and collaborators (2009), HB76, [full text](https://arxiv.org/pdf/0809.3308v4), develop unambiguous phase estimation using increasing phase powers and controlled error probabilities. Kimmel–Low–Yoder (2015), KLY76, [corrected version](https://arxiv.org/pdf/1502.02677v3), extends the approach to robust gate calibration; its 2021 erratum corrects the phase-unwrapping analysis. Section 55 credits this background and proves its own safe-angle induction and conditional concentration bounds instead of importing the original numerical threshold.

The hybrid inequality converts operator-norm error \(\epsilon\) to future-horizon loss at most \(2N\epsilon\). Combining just this conversion with the displayed fixed-dimension tomography bounds gives an \(O(N^2\delta^{-2})\) fixed-confidence baseline. This does not claim optimality for those algorithms. Section 55 proves \(\Theta(N\delta^{-2}\log(1/\eta))\) on the full biased qubit body using one data-dependent experiment, including unknown-noise selection and both endpoint estimates. Training uses, future horizon, maximum entangled block length and classical payload remain separate resources.

Theorem 5 of Gutoski, Gutoski66, [full text](https://arxiv.org/pdf/1008.4636v4), gives a common discriminator for two convex sets of strategies. Repetition maps an effect nonlinearly to its \(N\)-use strategy, so convexity of the effect body does not ensure convexity of that image. A two-set discriminator is also not by itself a common estimator for an entire packing. The learning proof constructs its decision tree explicitly.

## Scope of the author-side conclusion

The new package consists of the dimension-dependent finite-pair comparison, the matrix-interval entropy and the separate sharp common qubit learner. It retains ordered binary outputs and memoryless consumption. It does not give the exact optimal adaptive value for every pair, a classification of multiple-output instruments, or dimension-uniform constants. Arbitrary-dimensional rational-centre existence and the inherited explicit qubit codec have different constructive content.

An independent specialist should compare equivalent formulations in measurement discrimination, channel statistical geometry and learning, including boundary regularization and spectral integral asymptotics. No directly matching theorem was identified among the stated sources. No human opinion, novelty certificate or journal-level judgement has been supplied by this audit. Both active bibliographies retain all predecessor entries and include the newly checked references.

