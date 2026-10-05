# Theorem-level literature comparison — Revision 77

Primary sources checked on 4 October 2026. This author-side comparison addresses the v76 referee report r50, particularly R02–R06, and the additional matrix learning and effective coding theorems of Revision 77. The controlling report is preserved as `FROZEN_R50_REPORT.md`; it reviewed completed v76 head `c041c011274973728a8cc55029192c057696aa43`. The complete preceding comparison is preserved in `predecessor-v76-audit/LITERATURE_AUDIT.md`, with earlier comparisons retained in their predecessor directories.

This audit records the authors' source comparisons. No outside reviewer has been contacted or commissioned, and no independent human specialist has supplied a priority judgment. R03 therefore remains a request for independent assessment; `INDEPENDENT_REVIEW_BRIEF.md` supplies concrete theorem objects and questions for that assessment. A bounded source comparison, a repository referee report, a build receipt, and an independent human opinion have distinct evidentiary roles.

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

## Common estimation: theorem-level access and loss comparison

The parameters below use a common convention: \(M\) is the number of training calls, \(\epsilon\) is a one-use accuracy, and \(\eta\) is the failure probability. The source papers' sample-size variables are renamed accordingly. Both cited tomography theorems already return a common classical estimator of an unknown measurement.

**Antonio Anna Mele–Lennart Bittel (2026), MB67, _Optimal learning of quantum channels in diamond distance_.** [Version checked: arXiv:2512.10214v3](https://arxiv.org/pdf/2512.10214v3), [version record](https://arxiv.org/abs/2512.10214v3). Theorem I.1 gives \(O(d_{\rm in}d_{\rm out}k\epsilon^{-2})\) calls at fixed confidence for Kraus rank at most \(k\) and \(0<\epsilon<1\). Lemmas III.7–III.8 identify the binary one-use loss and extract a legal effect. Corollary III.9 gives
\[
 M=1024d^2\epsilon^{-2}
   +O(d\epsilon^{-2}\log(1/\eta)),\qquad
 \mathbb P\{\|\widehat E-E\|_{\rm op}\le\epsilon\}\ge1-\eta,
 \qquad \eta>4e^{-4d^2}.
\]
It uses \(d_{\rm out}=2\), \(k=2d\), and imposes no effect-rank restriction. Calls prepare independent input/reference maximally entangled pairs in parallel, followed by collective processing of Choi outputs; no measurement environment is accessed. Theorem III.2 permits arbitrary confidence through its unsimplified bound. Remark III.4, equation (165), also gives amplification with \(O(d^2\epsilon^{-2}\log(1/\eta))\) calls. The simplified Theorem III.3 has a confidence restriction too. Proposition IV.17 matches the dimension dependence at fixed accuracy; separate dimension and accuracy lower bounds must not be multiplied into an unstated joint lower bound.

**Leonardo Zambrano–Sergi Ramos-Calderer–Richard Kueng (2026), ZRK76, _Fast quantum measurement tomography with optimal error bounds_.** [Version checked: arXiv:2507.04500v3](https://arxiv.org/pdf/2507.04500v3), [published article: _Quantum_ **10**, 2162](https://quantum-journal.org/papers/q-2026-07-15-2162/), DOI [10.22331/q-2026-07-15-2162](https://doi.org/10.22331/q-2026-07-15-2162). Definition 1 uses worst-input one-use outcome total variation, without a reference. Theorem 2, equation (13), gives the sufficient budget
\[
 M\ge\frac{8(d^2+\epsilon(d^2+1)/6)}{\epsilon^2}
       \log\frac{2^{L+1}9^{2d}}{\eta}
\]
for \(L\)-outcome POVMs using known global \(2\)-design probes. Least squares and legal projection give a classical estimate for arbitrary effect ranks. Training is nonadaptive and single-copy, without retained references or entanglement between calls. Theorem 9, equation (43), gives the matching \(\Omega((d^3+d^2L)\epsilon^{-2})\) lower bound at constant confidence within that probe model. For \(L=2\), its loss equals \(\|E-F\|_{\rm op}\). The theorem's local-product-design variant has a different dimension bound.

### Direct guarantee conversion and the new finite-horizon statement

The manuscript's hybrid inequality is
\[
 d_N(\mathcal M_E,\mathcal M_{\widehat E})
 \le2N\|E-\widehat E\|_{\rm op}.
\]
Taking \(\epsilon=\delta/(2N)\) transfers either one-use theorem to the future loss. The following entries are sufficient budgets from that substitution and the cited confidence bounds:

| Guarantee being applied | Sufficient training calls for future loss at most \(\delta\) | Meaning of the comparison |
|---|---|---|
| MB67, binary specialization and amplification | \(O(d^2N^2\delta^{-2}\log(1/\eta))\) | One-use guarantee transferred by the hybrid inequality |
| ZRK76, Theorem 2 with \(L=2\) and global designs | \(O(d^2N^2\delta^{-2}[d+\log(1/\eta)])\) | The same transfer for its restricted probes |
| Revision 77, **thm:matrixlearning77** | \(Cd^4N\delta^{-2}\log(d/\eta)\) | Direct risk theorem for \(d_N\), with entangled blocks and data-dependent calibration |

This comparison certifies sufficient budgets. It makes no converse assertion about the future-loss performance of the first two estimators, and no claim that adaptive training is necessary for the displayed horizon improvement. The \(N\)-dependence of the new minimax theorem is sharp for each fixed \(d\). The table does not establish a dimension-uniform advantage: the present \(d^4\) factor is not optimized, and the scalar converse does not provide a matching dimension factor. ZRK76's restricted-model lower bound cannot serve as a converse for a stronger entangled or adaptive training model.

The finite-use geometry explains the changed statistical target. Interior scalar displacement has a \(\sqrt N\) amplification scale; angular displacement at a projective endpoint has an \(N\) scale. Substituting the single tolerance \(\delta/N\) into an isotropic operator-norm guarantee does not use this anisotropy. Section 55 estimates endpoint probabilities at their variance-sensitive scale and selects phase-amplifying block lengths from observed amplitudes. Section 56 makes that experiment applicable in arbitrary dimension by calibrating both \(E+N^{-1}I\) and \(I-E+N^{-1}I\), controlling the variance introduced by two-dimensional compression, and assembling the estimates in the calibrated quadratic form. The result is a single procedure for the complete closed effect body, including all ranks and repeated spectra.

### Learning and discrimination resources retained from earlier revisions

**Bisio–D'Ariano–Perinotti–Sedlák (2011), BDPS76.** [Full text](https://arxiv.org/pdf/1103.0480v2), [published article](https://doi.org/10.1016/j.physleta.2011.08.002). Their learning and retrieval network stores information from an unknown von Neumann measurement in quantum memory and later reproduces a measurement on a new input. The paper optimizes training with one and two examples and identifies a nonparallel feature with three examples. That stored programme and retrieval criterion differ from the present high-probability classical estimate.

**Multiscale phase methods.** Higgins and collaborators (2009), HB76, [full text](https://arxiv.org/pdf/0809.3308v4), develop unambiguous phase estimation using increasing phase powers and controlled error probabilities. Kimmel–Low–Yoder (2015), KLY76, [corrected version](https://arxiv.org/pdf/1502.02677v3), extends the approach to robust gate calibration; its 2021 erratum corrects the phase-unwrapping analysis. Section 55 credits this background and proves its own safe-angle induction and conditional concentration bounds instead of importing the original numerical threshold.

Theorem 5 of Gutoski, Gutoski66, [full text](https://arxiv.org/pdf/1008.4636v4), gives a common discriminator for two convex sets of strategies. Repetition maps an effect nonlinearly to its \(N\)-use strategy, so convexity of the effect body does not ensure convexity of that image. A two-set discriminator is also not by itself a common estimator for an entire packing. The learning proof constructs its decision tree explicitly.

## The additional arbitrary-dimensional calibration and coding objects

The new learning lemma **lem:matrixcalibration77** returns a legal \(A\) satisfying simultaneous multiplicative Loewner comparisons for both regularized support endpoints, together with \(\|E-A\|_{\rm op}\le N^{-1/2}\). It uses at most \(Cd^4N\log(d/\eta)\) product-input calls, including on unsuccessful records. **lem:matrixcompression77** uses the harmonic endpoint expression and the exact identity
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

## Version locators and the scope of this conclusion

The detailed learning comparison uses MB67 v3 and ZRK76 v3, the current versions located for the cited results. Their labels are stable in the specified PDFs: MB67 Theorem III.2 is on page 32, Theorem III.3 on page 35, Remark III.4 on page 36, and Corollary III.9 on page 39; ZRK76 Theorem 2 is on page 5 and Theorem 9 spans pages 8–9. Bibliographic keys refer to `editions/coding-bibliography.tex` and are inherited identifiers rather than revision numbers of the external sources. The journal reference for ZRK76 is _Quantum_ **10** (2026), 2162; its published title omits the word “dimension” appearing in some older citations.

The package under comparison consists of the finite-pair midpoint-resolvent comparison, the closed matrix-interval entropy, the common learner in every fixed dimension, and the finite exact matrix codec with optimal-order payload. All four statements have the same memoryless ordered binary qc interface. Exact adaptive values for every pair, multi-outcome measurements, residual quantum outputs, optimal growing-dimension statistical complexity, and efficient dictionary construction are distinct questions. The earlier contact theorem retains its own class of subsets and regularity assumptions.

The checked statements do not provide the combined finite-horizon conclusions in the forms specified above. That observation identifies concrete targets for further comparison; it is not a proof of novelty or an independent priority clearance. An independent specialist should examine equivalent formulations in measurement discrimination, statistical channel geometry, relative-error tomography, spectral matrix-volume asymptotics, and effective metric entropy. This audit supplies no human opinion, journal-level verdict, or closure of the repository-wide Theta A/B/C/D programme. Earlier results and bibliographic entries remain preserved and must be assessed under their original hypotheses.
