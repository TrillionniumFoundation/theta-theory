# Theorem-level literature comparison — Revision 78

Current primary-source checks were made on 4 October 2026. This author-side comparison responds to **FROZEN_R51_REPORT.md**, especially Sections 6.3, 6.5 and required revisions 2, 4, 5 and 10. That report reviewed completed Revision 77 head `5650842e0bc89ca6a8b6d6730115784f0d9ecc12`. The full preceding audit is preserved as `predecessor-v77-audit/LITERATURE_AUDIT.md`, with its older predecessor comparisons intact. Original focused and complete bibliographies were copied into the matching `predecessor-v77-audit` paths before appending new entries.

The principal R51 increment is a theorem about **fresh quantum training blocks for the entire unknown ordered binary effect body under future-use loss**. The block dependence uses established metrological and fidelity methods. A sharper Mele–Bittel analysis is also supplied on a promised interior class. Those two claims distinguish exactly where estimator reanalysis can improve the horizon rate and where a direct acquisition lower bound rules it out. No independent human specialist has supplied a correctness or priority judgment; the actionable questions remain open in `INDEPENDENT_REVIEW_BRIEF.md`.

## Objects submitted for comparison

The target class is the entire matrix interval
\[
\mathfrak E_d=\{E=E^*:0\le E\le I_d\},\qquad
\mathcal M_E(\rho)=\operatorname{tr}(E\rho)|1\rangle\langle1|
+\operatorname{tr}((I-E)\rho)|0\rangle\langle0|.
\]
The outcomes are ordered. Calls are memoryless and consume the input; no residual quantum system or measurement environment is returned by the device. A tester can retain an external reference and use intermediate channels and classical feedback. Trace distance is unhalved. In particular, \(d_1(E,F)=2\|E-F\|_{\mathrm{op}}\). The nonadaptive class still permits entanglement across the input block and a retained reference; it excludes feedback between calls. All finite dimensions are included, and covering constants may depend on dimension.

Section 53, **thm:matrixmetric76**, compares the nonadaptive and adaptive distances for every pair and every finite horizon. With \(A=(E+F)/2\), \(H=F-E\), \(V=A(I-A)\), and left and right multiplication denoted by \(L,R\),
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
The lower bound allows arbitrary legal centres; rational legal centres achieve the same order. Section 55, **thm:commonlearn76**, supplies the common binary-qubit learner used as a subroutine in the following all-dimensional result.

Section 56, **thm:matrixlearning77**, proves that one procedure, without supplied spectral data, returns a legal classical estimate satisfying
\[
 \sup_{E\in\mathfrak E_d}
 \mathbb P_E\{d_N(\mathcal M_E,\mathcal M_{\widehat E})>\delta\}
 \le\eta,
 \qquad
 M\le C d^4N\delta^{-2}\log(d/\eta).
\]
Here \(d,N\ge1\), \(0<\delta\le\delta_0\), and \(0<\eta\le1/8\); \(C,\delta_0\) are absolute. The bound holds on every record, and each entangled input block has length at most \(N\). Its scalar-subfamily converse is
\[
 M\ge cN\delta^{-2}\log(1/\eta)
\]
even for arbitrary reference-assisted adaptive training with bounded public stopping. Thus the minimax order is \(\Theta_d(N\delta^{-2}\log(1/\eta))\) for each fixed \(d\). Optimality of the displayed \(d^4\) factor is not asserted. The future comparison horizon \(N\), training calls \(M\), entangled block length, and classical computational work are separate resources.

Section 57, **thm:matrixcodec77**, constructs an ordered dictionary by finite exact rational arithmetic for every \(d,N\ge1\) and rational \(0<\delta\le1\). Encoding a supplied Gaussian-rational effect and decoding its index both terminate. The decoded effect has error at most \(11\delta/16\). The dictionary size has the covering order above as an upper bound throughout this range, and its index length, for \(0<\delta\le\delta_d\), is
\[
 \frac{d^2}{2}\log_2N+
 \lfloor d/2\rfloor\log_2\log(N+2)+
 d^2\log_2(1/\delta)+O_d(1).
\]
Both parties reconstruct the dictionary from public \((d,N,\delta)\); no centre coordinates or target-dependent advice are omitted from the payload. This is a finite exact optimal-order description theorem. The construction does not claim polynomial running time in the payload length. Earlier structural results, the contact results, and the direct qubit code remain available under their own hypotheses.

## Measurement discrimination: direct antecedents

**Fiurášek–Mičuda (2009), FM75.** [Full text](https://arxiv.org/pdf/0909.2940), [published article](https://doi.org/10.1103/PhysRevA.80.042312). Sections I, III and IV compare two-use projective-qubit protocols; equation (16) treats adaptive product probes and equations (27)–(30) give entangled feed-forward constructions. Their interface excludes additional ancillary measurements. This restriction matters when comparing with the later reference-assisted projective theorem.

**Sedlák–Ziman (2014), SZ74.** [Full text](https://arxiv.org/pdf/1408.0934), [published article](https://doi.org/10.1103/PhysRevA.90.052312). Theorem 1 characterizes perfect single-use discrimination of binary measurements. Section VI, Example 4, equation (37), allows unequal white-noise visibilities and reduces the one-use problem to mixed-qubit-state discrimination. Those effects are unbiased. For \(E=((1+b)I+x\cdot\sigma)/2\), the elementary identity \(\Gamma(E)-(I-E)=bI\) explains why this particular spin-flip reduction does not itself treat bias.

**Puchała–Pawela–Krawiec–Kukulski (2018), PPKK74.** [Full text](https://arxiv.org/pdf/1804.05856), [published article](https://doi.org/10.1103/PhysRevA.98.042103). Theorem 1, equation (19), represents the single-use diamond distance between von Neumann measurements by a minimization over diagonal phases of a unitary-channel distance. Assigning this representation to arbitrary nonprojective effects would require another argument.

**Puchała–Pawela–Krawiec–Kukulski–Oszmaniec (2021), PPKKO72.** [Full text](https://arxiv.org/pdf/1810.05122v4), [published article](https://quantum-journal.org/papers/q-2021-04-06-425/). Corollary 1 gives an exact finite-use parallel distance for von Neumann measurements; Theorem 2 proves optimality among general networks with ancillary access. This supplies an exact projective endpoint. The new constant-factor comparison does not assert exact parallel optimality for all effects.

**Krawiec–Pawela–Puchała (2020), KPP76, requested in r49.** [Full text](https://arxiv.org/pdf/2002.05452v1), [published article](https://doi.org/10.1007/s11128-020-02883-3). Sections 2–3 allow retained references and adaptive intermediate channels and study finite-use perfect discrimination of rank-one POVMs. Section 4 constructs two differently ordered nine-outcome qutrit SIC measurements admitting a two-use adaptive perfect test but no finite parallel perfect test. This is a direct repeated-measurement antecedent. It concerns two hypotheses, not two outcomes. The checked results do not give the present binary-body midpoint comparison or covering law. Requiring both effects of a binary qubit POVM to have rank one forces a projective measurement; for \(d>2\) their ranks cannot sum to \(d\).

**Datta–Biswas–Saha–Augusiak (2021), DBSA76, requested in r49.** [Full text](https://arxiv.org/pdf/2012.07069v2), [published article](https://doi.org/10.1088/1367-2630/abecaf). A destructive unknown measurement on one half of an entangled input is followed by an outcome-dependent known measurement on the reference. Theorem 1 relates entanglement advantage to steerability; Theorems 2–4 construct perfect-discrimination examples with multiple outcomes. Theorem 5 gives an advantage using any pure entangled two-qubit state for a pair of three-outcome POVMs. These are single-use results; their hypothesis and outcome counts must remain distinct in the comparison.

## Kraus geometry and finite-use channel bounds

**Fujiwara–Imai (2008), FI76.** [Publisher](https://doi.org/10.1088/1751-8113/41/25/255304), [author-uploaded full text](https://www.researchgate.net/publication/231040616_A_fibre_bundle_over_manifolds_of_quantum_channels_and_its_application_to_quantum_statistics). Theorem 4 expresses maximal reference-assisted quantum Fisher information through minimization over differentiable Kraus representations. Theorem 5 identifies a vanishing Kraus cross derivative that gives linear growth for repeated parallel use. Horizontal Kraus lifts and the orthogonality mechanism are established tools.

**Channel extension and adaptive bounds.** Demkowicz-Dobrzański–Kołodyński–Guţă (2012), DKG67, [full text](https://arxiv.org/pdf/1201.3940v2), equations (10)–(13) in this arXiv version, bound parallel quantum Fisher information using the usual Kraus quantities \(\alpha,\beta\). Demkowicz-Dobrzański–Maccone (2014), DM76, [full text](https://arxiv.org/pdf/1407.2934v3), equation (9), gives an adaptive bound whose \(\beta=0\) specialization is \(4N\|\alpha\|\). Kurdziałek–Górecki–Albarelli–Demkowicz-Dobrzański (2023), KGAD76, [full text](https://arxiv.org/pdf/2212.08106v2), equations (5) and (8)–(10), provides an adaptive recursion with the same specialization. In **lem:matrixpath76**, equation **eq:horizontaloverlap76** has \(\alpha=K^2\) and \(\beta=0\). The cancellation under arbitrary controls is consequently an application of the established method, explicitly checked for the present qc dilation and tester interface.

**Integration to finite pairs.** Yuan–Fung, YF76, [full text](https://arxiv.org/pdf/1506.00819v3), Section III, equation (26), integrates quantum Fisher information along a path to bound the Bures angle between finite channel hypotheses in parallel discrimination. Sieniawski–Demkowicz-Dobrzański (2026), SD76, [full text](https://arxiv.org/pdf/2510.15506v3), Section IV.A, equations (14)–(22), uses this connection with adaptive metrological bounds. The latter expressly cites the earlier integration argument. Neither passage from a differential bound to a finite path nor its adaptive use is claimed as new here.

These locators refer to the specified PDF versions. In particular, Yuan–Fung's v3 PDF labels the path integral equation (26), on page 8; its experimental HTML rendering numbers the same expression (28). The manuscript retains the PDF locator. For Sieniawski–Demkowicz-Dobrzański, equations (14)–(16) connect trace distance, Bures angle and the path integral; equations (19)–(22) apply adaptive quantum Fisher information bounds. These are the exact antecedents at the integration step of **lem:matrixpath76**.

Section 53 instead supplies a specific Sylvester construction involving \(\sqrt{E(I-E)}\) for a binary qc dilation, controls a residual derivative at the finite-horizon scale, and integrates the straight segment to obtain the displayed midpoint resolvent. Legal scalar and two-dimensional compressions give its matching lower estimate. This explicit closed-body comparison is the object requiring priority assessment; a general local Fisher information bound alone does not identify it.

## Inverse Sylvester forms and spectral volume

**Dittmann (1999), Dittmann76.** [Full text](https://arxiv.org/pdf/quant-ph/9808044), [published article](https://doi.org/10.1088/0305-4470/32/14/007). Equations (1)–(2) give the Bures tensor on the positive matrix cone as
\[
g^B_W(H,H)=\tfrac12\langle H,(L_W+R_W)^{-1}H\rangle.
\]
Algebraically, \(Q_N^2/N=2g^B_W(H,H)\) at \(W=A(I-A)+(2N)^{-1}I\). The inverse Sylvester form itself is classical. This identity is not a Bures pullback through the variance map: that map has differential \(H-AH-HA\), whereas the operational comparison retains \(H\).

**Sommers–Życzkowski (2003), SZGeom76.** [Full text](https://arxiv.org/pdf/quant-ph/0304041), [published article](https://doi.org/10.1088/0305-4470/36/39/308). Section III, especially equations (3.12)–(3.17), develops spectral coordinates, the eigenvalue Jacobian and volume integration for Bures geometry. These are antecedents for calculating a unitarily invariant matrix volume. Its normalized state body and metric differ from the effect interval and finite-horizon variance tensor here.

In Section 54 the determinant computation yields a spectral density proportional to
\[
N^{d^2/2}\prod_i[2\lambda_i(1-\lambda_i)+N^{-1}]^{-1/2}
\prod_{i<j}\frac{(\lambda_i-\lambda_j)^2}
{\lambda_i(1-\lambda_i)+\lambda_j(1-\lambda_j)+N^{-1}}.
\]
The proof establishes uniform volume bounds for operational balls on the closed matrix interval before deriving coverings from this integral. It then counts nested scales near the two opposite spectral endpoints: balanced endpoint prefixes produce \(\lfloor d/2\rfloor\) logarithmic factors. The checked sources do not state this asymptotic or its operational covering consequence. That is a bounded search result, not proof that an equivalent result cannot exist elsewhere.

## Common estimation: verified access, loss, confidence, and parameter ranges

The notation is standardized here: \(M\) counts training calls, \(N\) is the future comparison horizon, \(b\) bounds calls in one fresh quantum experiment, \(\epsilon\) is one-use operator accuracy, and \(\eta\) is failure probability. Both main tomography papers already construct one common classical estimator of an unknown measurement. The new theorem does not originate that statistical task.

**Mele–Bittel, MB67.** [Current version record](https://arxiv.org/abs/2512.10214v3), [full HTML](https://arxiv.org/html/2512.10214v3), [PDF](https://arxiv.org/pdf/2512.10214v3). The checked version is v3, 15 June 2026. Algorithm I.2, Figure 1 and Section III.2 prepare independent maximally entangled input/reference pairs; coherent purification and tomography subsequently act on the Choi copies. There are no additional unknown-channel calls during that processing. Therefore these acquisitions satisfy **def:freshblocks78** with \(b=1\), even though the source calls all simultaneous invocations a single parallel block. The operational restriction concerns connections between queried inputs, not simultaneous execution or the size of a final measurement.

Theorem I.1 gives \(O(d_{\rm in}d_{\rm out}k\epsilon^{-2})\) at fixed confidence for Kraus rank at most \(k\). Lemmas III.7–III.8 give the binary identity \(\|\mathcal M_E-\mathcal M_F\|_\diamond=2\|E-F\|_{\rm op}\) and extract a legal effect. Corollary III.9 uses \(k=2d\), allows every effect rank, and states
\[
 M=1024d^2\epsilon^{-2}+O(d\epsilon^{-2}\log(1/\eta)),
 \quad \mathbb P\{\|\widehat E-E\|_{\rm op}\le\epsilon\}\ge1-\eta,
 \quad 0<\epsilon<1,\quad 4e^{-4d^2}<\eta<1.
\]
The unsimplified Theorem III.2 permits arbitrary confidence. Remark III.4, equation (165), supplies the alternative sufficient order \(O(d^2\epsilon^{-2}\log(1/\eta))\) by repetition for all \(0<\eta\le1/8\); repetition and reconstruction preserve \(b=1\). At \(\eta=1/8\), Corollary III.9's restriction holds for every \(d\ge1\).

**Zambrano–Ramos-Calderer–Kueng, ZRK76.** [Current version record](https://arxiv.org/abs/2507.04500v3), [full HTML](https://arxiv.org/html/2507.04500v3), [published article](https://quantum-journal.org/papers/q-2026-07-15-2162/). The checked version is v3, 9 July 2026; the publication is *Quantum* **10** (2026), 2162. Section 3.1 collects the unknown POVM's outcomes on known individual probe states. The acquisition is nonadaptive and single-copy, without retained references, hence \(b=1\). Entanglement among the constituent qubits of a single \(d\)-dimensional global-design probe does not couple separate device calls.

Definition 1 uses worst-input one-use outcome total variation. For \(L=2\) this is exactly \(\|E-F\|_{\rm op}\). Theorem 2, equation (13), states the sufficient global-\(2\)-design budget
\[
 M\ge\frac{8(d^2+\epsilon(d^2+1)/6)}{\epsilon^2}
       \log\frac{2^{L+1}9^{2d}}{\eta}.
\]
The protocol uses least squares followed by legal projection and has no effect-rank promise. The displayed expression applies for positive accuracy and \(0<\eta<1\); the comparison table uses \(0<\epsilon<1\). Its local-product-design variant has a different dimension factor. Theorem 9, equation (43), proves \(\Omega((d^3+d^2L)\epsilon^{-2})\) at constant success probability within the stated nonadaptive single-copy known-input model.

### Theorem-level comparison table

The future-loss rows use an absolute sufficiently small \(\delta>0\). “Full body” means the entire ordered binary effect body; “interior” means the promised class \(I/4\preceq E\preceq3I/4\). The new block law has \(d\ge2\); the scalar exception is stated below.

| Theorem or conversion | Acquisitions and \(b\) | Loss and domain | Horizon \(N\) and dimension \(d\) | Confidence and call budget \(M\) |
|---|---|---|---|---|
| MB67, Corollary III.9 | Independent Choi probes, collective subsequent processing; \(b=1\) | One-use operator error \(\epsilon\); full body | Every \(d\ge1\); no future horizon in the theorem | \(4e^{-4d^2}<\eta<1\): \(1024d^2\epsilon^{-2}+O(d\epsilon^{-2}\log(1/\eta))\) |
| MB67, Remark III.4 amplification | Same fresh single-call acquisitions; \(b=1\) | One-use operator error \(\epsilon\); full body | Every \(d\ge1\) | All \(0<\eta\le1/8\): \(O(d^2\epsilon^{-2}\log(1/\eta))\) |
| ZRK76, Theorem 2, global designs, \(L=2\) | Known separate probe states, no reference; \(b=1\) | One-use operator error \(\epsilon\); full body | Every input dimension | All \(0<\eta<1\): \(O(d^2\epsilon^{-2}[d+\log(1/\eta)])\) |
| Direct hybrid transfer of MB67 | \(b=1\) | Future \(d_N\) error \(\delta\); full body | \(N\ge1\), every \(d\) | \(O(d^2N^2\delta^{-2}\log(1/\eta))\), a sufficient budget |
| Direct hybrid transfer of ZRK76 | \(b=1\) | Future \(d_N\) error \(\delta\); full body | \(N\ge1\), every \(d\) | \(O(d^2N^2\delta^{-2}[d+\log(1/\eta)])\), a sufficient budget |
| Revision 78, **thm:interiorlearning78**, using MB67 | Independent Choi probes; \(b=1\); converse permits fully coherent adaptive training | Future \(d_N\) error \(\delta\); promised interior | Joint dimension/horizon/accuracy order | \(\eta=1/8\): \(\Theta(d^2N\delta^{-2})\) |
| Retained **thm:matrixlearning77** | Fresh blocks of at most \(N\); classical adaptive calibration | Future \(d_N\) error \(\delta\); full body | \(N\ge1\), every fixed \(d\) | \(0<\eta\le1/8\): \(\Theta_d(N\delta^{-2}\log(1/\eta))\); upper \(Cd^4N\delta^{-2}\log(d/\eta)\) |
| Revision 78, **thm:blocklearning78** | Fresh quantum blocks of length at most \(b\), classical feedback, arbitrary output memory and joint processing | Future \(d_N\) error \(\delta\); full body | \(d\ge2\), \(1\le b\le N\) | \(0<\eta\le1/8\): \(\Theta_d((N^2/b)\delta^{-2}\log(1/\eta))\); upper factor \(Cd^4\log(d/\eta)\) |
| Revision 78, **cor:onecallseparation78** | Every acquisition in the larger fresh \(b=1\) class | Future \(d_N\) error \(\delta\); full body | \(d\ge2\), \(N\ge1\) | Necessary \(\Omega(N^2\delta^{-2}\log(1/\eta))\); applies to any reconstruction of MB67/ZRK76 acquisitions |

### The R51 estimator-reanalysis question has two different answers

The hybrid inequality \(d_N(E,F)\le2N\|E-F\|_{\rm op}\), by itself, certifies only sufficient budgets. Revision 77 correctly left stronger estimator analysis open on that evidence. Revision 78 adds an independent minimax converse for the actual acquisitions: every full-body learner with \(b=1\) has a worst-case \(\Omega(N^2\delta^{-2}\log(1/\eta))\) cost. Its adversarial projective pair is available in every \(d\ge2\). Therefore a new analysis or a different classical/collective reconstruction of the checked MB67 or ZRK76 acquisitions cannot yield the full-body \(O_d(N\delta^{-2}\log(1/\eta))\) law. The assertion concerns uniform worst-case risk, rather than pointwise difficulty at every effect or optimal dimension factors for those protocols.

On the promised interior class, a stronger analysis **does** help. If \(I/4\preceq E\preceq3I/4\) and a legal \(F\) satisfies \(\|E-F\|_{\rm op}\le1/8\), the horizontal path argument gives
\[
 d_N(E,F)\le4\sqrt N\|E-F\|_{\rm op}.
\]
Thus **thm:interiorlearning78** applies the actual legal binary estimator of MB67 Corollary III.9 at \(\epsilon=\delta/(8\sqrt N)\), \(\eta=1/8\), and obtains \(O(d^2N\delta^{-2})\) fresh single-call training. The new dimension lower bound matches it on this interior class. The improvement uses a promise excluding the projective boundary; it does not contradict **cor:onecallseparation78**. For smaller failure probabilities, MB67's amplification gives the sufficient interior budget \(O(d^2N\delta^{-2}\log(1/\eta))\); joint optimality of that multiplied dimension/confidence expression is not asserted.

## Fresh quantum blocks: exact claim, proof ingredients, and priority boundary

**Definition and range.** In **def:freshblocks78**, each classical history selects a length \(1\le t\le b\) and a fresh tester. Conditional on that history, the entire tester, including unused inputs and its reference, starts in a parameter-independent state tensor-separated from old quantum storage and remains isolated until its last call. Inside the block arbitrary reference-assisted adaptive quantum control is allowed. At boundaries all stored systems may be processed by a common instrument, whose classical result selects the next fresh tester. An arbitrary collective final readout is allowed. Declared block lengths are charged in full and sum to at most \(M\) on every record, including stopped and unsuccessful records. This is a restriction on feeding quantum information into future probes; it does not bound output-memory size.

For \(d\ge2\), \(1\le b\le N\), \(0<\delta\le\delta_*\), \(0<\eta\le1/8\), **thm:blocklearning78** gives
\[
 c\frac{N^2}{b\delta^2}\log\frac1\eta
 \le M_b^\star(d,N,\delta,\eta)
 \le Cd^4\frac{N^2}{b\delta^2}\log\frac d\eta.
\]
The constants are absolute, and \(\delta_*\) is at most the retained learner's small-error cap and \(1/4\). For \(d=1\), the correct law is instead \(\Theta(N\delta^{-2}\log(1/\eta))\), independently of \(b\). There is no projective angular subfamily in dimension one.

**Finite-pair and confidence argument.** The block lower bound uses a projective qubit rotation embedded in the full effect body. On the active two-dimensional space, the exact projective finite-use distance is \(2\sin(N|\theta|/2)\) in its local range; the multiple-shot projective discrimination theorem **PPKKO72** is a direct antecedent. **lem:blockfidelity78** bounds the root fidelity after a fresh \(t\)-call experiment by \(\cos(t|\theta|/2)\). When \(b|\theta|\le1\), the subnormalized classical–quantum branch calculation yields
\[
 \mathfrak f(\Gamma_0,\Gamma_\theta)\ge e^{-Mb\theta^2/4}.
\]
A history-weighted potential retains the actual charged call count. Tensor-product fidelity is used only conditionally on the same history; common instruments use direct-sum fidelity and data processing. Taking \(\theta=4\delta/N\) gives disjoint future-loss success balls. Testing them yields \(M\ge N^2\log(1/\eta)/(24b\delta^2)\). This establishes the confidence term for biased estimators and bounded stopping without converting a local Cramér–Rao bound into a global risk claim.

**Upper bound and synthesis.** **lem:blockhybrid78** gives \(d_N\le\lceil N/b\rceil d_b\). Applying the retained all-effect common learner with horizon \(b\) and accuracy \(\delta/\lceil N/b\rceil\) yields the upper bound. That reduction is a standard hybrid blocking argument. The hard part inherited by the common learner remains unknown-endpoint calibration, controlled compression, and noise-adapted phase learning across the closed body. The block interpolation is a resource consequence of that learner plus a finite-confidence converse; no separate invention of the standard metrological gain is claimed.

**Hyllus et al., Hyllus78; Tóth, Toth78.** [Hyllus PDF, v3](https://arxiv.org/pdf/1006.4366), [version record](https://arxiv.org/abs/1006.4366), [Tóth full text, v3](https://arxiv.org/html/1006.4368v3), [published Hyllus article](https://doi.org/10.1103/PhysRevA.85.022321), [published Tóth article](https://doi.org/10.1103/PhysRevA.85.022322). Hyllus et al., Section III.A, Observation 1, equation (9), and Tóth, Observation 3, equation (6), bound quantum Fisher information of \(b\)-producible qubit probes under linear phase encoding by
\[
 \lfloor M/b\rfloor b^2+(M-b\lfloor M/b\rfloor)^2\le Mb.
\]
These are established resource-tradeoff antecedents. The manuscript's blocks can also contain sequential adaptive quantum controls, so \(b\) is not asserted to equal entanglement depth of an arbitrary final state. The authors' literal derivation of the all-body law and finite confidence/stopping argument must be assessed beyond the shared scale.

**Salek–Hayashi–Winter, SHW68.** [Full text, arXiv:2011.06569v3](https://arxiv.org/html/2011.06569v3), [published article](https://doi.org/10.1103/PhysRevA.105.022419). Section II.2, equations (1)–(3), explicitly permits classical adaptive inputs, receiver quantum memory, instruments combining the new output with that memory, and a collective final test. Section V.2, Theorem 9, treats general channel inputs without input-side quantum memory through classical–quantum channel discrimination. This is a close model and method antecedent. Applying such a viewpoint to the classical alphabet of fresh tester specifications is natural. Its asymptotic exponent equalities do not themselves state the present uniform finite-budget, variable-length, high-confidence learning theorem.

**Wilde–Berta–Hirche–Kaur, WBHK72.** [Full text, arXiv:1808.01498v2](https://arxiv.org/html/1808.01498v2), [published article](https://doi.org/10.1007/s11005-020-01297-7). Lemma 14 supplies adaptive divergence meta-converses; Proposition 21, equations (156)–(160), uses fidelity to bound symmetric testing error, and Appendix B proves the generalized Fuchs–van de Graaf inequality. These are prior finite-testing tools. The conditional branch-potential proof is stated directly in Section 58 so its specific fresh-block restriction, stopping convention and confidence range can be checked.

**Bounds on joint measurements of supplied states are another resource.** Chen–Li–Liu, **CLL78**, [arXiv:2402.16353v1](https://arxiv.org/abs/2402.16353v1), study an entanglement/copy-complexity tradeoff when each tomography measurement acts on at most \(t\) supplied state copies. Nayak–Zhou, **NZ78**, [arXiv:2609.10514v1](https://arxiv.org/html/2609.10514v1), Theorems 1.1–1.2, give the small-error constant-confidence order \(\Theta(dr\epsilon^{-2}\max\{1,r/\sqrt t\})\) for rank-at-most-\(r\) states, with classical adaptation of successive joint measurements and no persistent quantum memory between them. These results constrain output measurement size. They cannot be read as the fresh-query \(b\) law, which permits unrestricted final joint processing. MB67 Section I.5's suggested blockwise Choi purification likewise concerns output-copy processing. These precedents prevent a claim to be the first resource interpolation for quantum learning.

## Growing-dimension binary lower bound and current channel-learning work

**Existing binary bounds.** MB67 Proposition IV.17 proves a projector-packing lower bound with \(\Omega(d^2)\) at fixed accuracy. Its Corollary IV.20 also proves
\[
 M=\Omega\bigl(d\epsilon^{-2}\log(d/\eta)\bigr)
\]
for operator-norm tomography of binary POVMs, \(0<\epsilon\le\epsilon_0\), \(0<\eta<1/4\), even with arbitrary adaptive quantum strategies. This second bound uses diagonal multi-coin effects. These are the actual binary conclusions of the checked source; separate bounds are not multiplied into an unstated theorem.

**Oufkir–Girardi, OG67.** [Version record](https://arxiv.org/abs/2601.04180v4), [full text](https://arxiv.org/html/2601.04180v4). The checked v4 is dated 16 January 2026. Theorem 4 (Section 3) gives the general-channel lower order \(\Omega(d_A d_B r/[\epsilon^2\log(d_Br/\epsilon)])\) when \(d_A\le rd_B/2\), at constant success probability, allowing fully coherent queries. The corresponding boundary order has \(\epsilon\) instead of \(\epsilon^2\) when \(d_A=rd_B\). Its hard families are general quantum channels, so setting \(d_B=2\) alone does not prove a binary classical-output statement.

**Chen–Zhang–Yu, CZY78.** [Version record](https://arxiv.org/abs/2601.10683v1), [full text](https://arxiv.org/html/2601.10683v1). Theorem 1.1, restating Theorem 4.2, proves the optimal order \(\Omega(rd_1d_2\epsilon^{-2})\) in the general-channel regime \(rd_2\ge2d_1\), with arbitrary coherent adaptive queries, for sufficiently small error and constant success. It removes OG67's logarithmic loss. The construction in Section 4, equations (17)–(18), retains quantum coherence between two output sectors. Consequently its stated general-channel lower bound is not used as a binary-qc theorem. Whether a suitable readout and restricted packing give an equivalent binary lower bound is an explicit priority question.

**Present binary argument.** **lem:weakmeasurementinfo78** directly treats effects near \(I/2\). For \(E_x=I/2+H_x\), \(\|H_x\|_{\rm op}\le r\), a query on any label-dependent input/reference state has conditional output branches \(\rho_R^x/2\pm\Delta_x\), with \(-r\rho_R^x\preceq\Delta_x\preceq r\rho_R^x\). Relative entropy against an independent fair output bit bounds the information added by that query by \(\log(1+4r^2)\le4r^2\), including arbitrary retained memory. An operator-norm packing of dimension \(d^2\), with radius of order \(\delta/\sqrt N\), gives **thm:dimensionlower78**:
\[
 M\ge c d^2N\delta^{-2}
\]
at constant confidence. The hard family lies in the promised interior. The theorem applies for every \(d,N\ge1\), \(0<\delta\le2^{-13}\), and \(0<\eta\le1/8\). It improves the manuscript's earlier scalar-only dimension comparison and, with the MB67 interior reanalysis, gives **thm:interiorlearning78**. The operator-loss specialization **cor:binaryoperatorlearning78** has \(0<\epsilon\le2^{-14}\) and failure at most \(1/8\). No priority claim is made for weak-channel information bounds, volumetric packing, Fano's inequality, or joint one-use dimension/accuracy scaling without comparison to equivalent channel results.

The full-body upper bound remains \(Cd^4(N^2/b)\delta^{-2}\log(d/\eta)\). Combining its block and dimension converses leaves a growing-dimensional gap; the sharp promised-interior theorem does not eliminate that gap on the whole effect body.

### Learning and discrimination resources retained from earlier revisions

**Bisio–D'Ariano–Perinotti–Sedlák (2011), BDPS76.** [Full text](https://arxiv.org/pdf/1103.0480v2), [published article](https://doi.org/10.1016/j.physleta.2011.08.002). Their learning and retrieval network stores information from an unknown von Neumann measurement in quantum memory and later reproduces a measurement on a new input. The paper optimizes training with one and two examples and identifies a nonparallel feature with three examples. That stored programme and retrieval criterion differ from the present high-probability classical estimate.

**Multiscale phase methods.** Higgins and collaborators (2009), HB76, [full text](https://arxiv.org/pdf/0809.3308v4), develop unambiguous phase estimation using increasing phase powers and controlled error probabilities. Kimmel–Low–Yoder (2015), KLY76, [corrected version](https://arxiv.org/pdf/1502.02677v3), extends the approach to robust gate calibration; its 2021 erratum corrects the phase-unwrapping analysis. Section 55 credits this background and proves its own safe-angle induction and conditional concentration bounds instead of importing the original numerical threshold.

Theorem 5 of Gutoski, Gutoski66, [full text](https://arxiv.org/pdf/1008.4636v4), gives a common discriminator for two convex sets of strategies. Repetition maps an effect nonlinearly to its \(N\)-use strategy, so convexity of the effect body does not ensure convexity of that image. A two-set discriminator is also not by itself a common estimator for an entire packing. The learning proof constructs its decision tree explicitly.

## The additional arbitrary-dimensional calibration and coding objects

The retained learning lemma **lem:matrixcalibration77** returns a legal \(A\) satisfying simultaneous multiplicative Loewner comparisons for both regularized support endpoints, together with \(\|E-A\|_{\rm op}\le N^{-1/2}\). It uses at most \(Cd^4N\log(d/\eta)\) product-input calls, including on unsuccessful records. **lem:matrixcompression77** uses the harmonic endpoint expression and the exact identity
\[
 (PEP)(I-PEP)
   =PE(I-E)P+PE(I-P)EP
\]
on the compressed space. The extra positive term is controlled at the \(N^{-1}\) cutoff because \(P\) commutes with the calibration estimate. This is the precise step permitting the qubit learner to be used inside an unknown matrix effect. The audit has not identified this calibration-and-compression statement in the cited one-use tomography theorems; independent assessment should compare equivalent regularized relative-error formulations as well as the final minimax law.

For **thm:matrixcodec77**, let
\[
 K=\left\lceil32dN/\delta\right\rceil.
\]
The algorithm enumerates a bounded coordinate grid, performs exact legality tests on both outcomes, and greedily retains a matrix when its squared \(Q_N\)-separation from every retained centre exceeds \((\delta/16)^2\). The squared comparison is rational and is obtained by solving a regularized Sylvester equation; spectral rounding thresholds are unnecessary. The proof uses the triangle inequality for \(d_N\) and the operational-ball volume theorem. It makes no triangle-inequality claim for \(Q_N\).

The ambient grid has at most
\[
 (K+1)^d(2K+1)^{d(d-1)}
\]
candidate tuples. This finite enumeration, exact rational centre selection, and deterministic decoder replay settle constructive existence with optimal-order index length. Their runtime and storage can be large. A physical unknown-device learner supplies observations; a supplied-description encoder receives a matrix or a certified approximation. Those inputs are different. Real-target coverage does not provide an oracle for exact coordinates; the finite encoder interface is stated separately. The implementation's completed small cases and matrix-kernel checks provide finite computational evidence, not a claim that large dictionaries have been fully enumerated.

Classical reconstruction, centre selection, and state preparation are excluded from the learner's device-call count and remain explicit resources. Public parameters determine the codebook; a nonpublic header must be charged. The priority question for the codec is the combination of this operational metric, the optimal-order dictionary size, and a terminating exact construction. Finite grid enumeration and packing arguments themselves are standard proof methods.

## Finite trusted controls and reproducibility boundary

Section 59, **thm:finitecontrollearning78**, transfers the common and block-restricted call orders to finitely described trusted preparations with certified trace error, and trusted controls with certified diamond error. **lem:controlhybrid78** sums the every-record trusted-instruction errors and bounds total variation of the entire classical output law. Running the ideal procedure at failure allowance \(\eta/2\) and distributing a further \(\eta/2\) allowance over the finite instruction count preserves the original risk target and exact legality of the returned effect. The argument includes discontinuous data decisions. It is an explicit use of the standard adaptive hybrid inequality, not a hardware-efficiency theorem. State-preparation time, workspace, and potentially exponential state descriptions remain charged separately from device calls.

## Version locators, search scope, and unresolved independent review

Current source checks in this audit specifically cover MB67 v3 (15 June 2026), ZRK76 v3 (9 July 2026), Hyllus78 v3, Toth78 v3, SHW68 v3, WBHK72 v2, OG67 v4 (16 January 2026), CZY78 v1 (15 January 2026), CLL78 v1, and NZ78 v1 (9 September 2026). The older discrimination/geometry comparisons above retain the exact source locators and caveats established in the preserved Revision 77 audit. The two main tomography versions were checked against arXiv's version records, and the ZRK76 journal record is *Quantum* **10** (2026), 2162. Bibliographic keys are inherited identifiers, rather than source revision numbers.

The search included primary-source queries about bounded entanglement depth, block-limited metrology, adaptive fresh-input channel discrimination, and recent channel and measurement tomography lower bounds. Stronger search was used to supplement routine lookup. This was a bounded author-side search, not a database-complete priority investigation. Unrelated search hits and abstracts without a checked relevant theorem are not used to infer a competing result. In particular, an output-side joint-measurement limit and an input-side fresh-block limit are kept distinct.

The new full-body block theorem, the positive interior reanalysis, the weak-binary dimension lower bound, and the finite-control transfer have concrete mathematical content for independent review. The pre-existing midpoint-resolvent comparison, endpoint-log entropy and exact codec remain separate priority objects. **INDEPENDENT_REVIEW_BRIEF.md** asks for a specialist to compare these exact statements, including equivalent reductions from current channel lower bounds. Review material has been prepared; independent human specialist judgment is pending. No outside reviewer has been contacted, no opinion has been supplied, and neither this audit nor the AI-assisted R51 report gives human priority clearance or a journal-level endorsement. The wider Theta A/B/C/D programme retains its separate unresolved status.
