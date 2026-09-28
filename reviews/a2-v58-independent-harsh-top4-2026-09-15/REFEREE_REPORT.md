# Independent referee report on A2, revision 58

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 15, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted referee-style assessment. It is not a commissioned report from any of these journals, an editorial decision, or a formal proof certificate. Mathematical correctness, reproducibility, and exceptional significance are assessed separately.

## 1. Recommendation and frozen object

**Recommendation: decline at the requested highest general-journal level on the present case for exceptional mathematical significance.** I do not recommend acceptance merely because another revision has passed its checks. Equally, I have not established a new fatal error in the central analytical and geometric interfaces examined here. The new Proposition 12.9 is correct within that examination and implements the optional refinement R57-M3 from the preceding report. It does not provide an order-uniform inverse for the complete nonlinear reconstruction, and the manuscript expressly does not claim one.

This distinction is essential. A negative placement recommendation is not evidence that a theorem is false. Conversely, the absence of a newly demonstrated error in a bounded review is not certification of all statements in a 401-page delivery. The present report does not manufacture a mathematical defect in order to preserve an adverse recommendation.

| Object | Immutable identity |
|---|---|
| Review-ready branch | `revision/a2-v58-review-ready-2026-09-15` |
| Review-ready head | `76535b285378923bacc7eaf17809dd3ab7a3bf6d` |
| Actual compiled mathematical source | `92a6d946c98e19c33ebff15997c0116ac158b89d` |
| Manuscript subtree | `39d14581fd018149f2dcce7c306d04ad8e286c0f` |
| Source branch | `revision/a2-v58-uniform-admissible-blocks-2026-09-15` |
| Manuscript directory | `papers/A2-v17-boundary-information-coarsening/` |
| Native workflow / attempt / artifact | `34969789751` / `1` / `10397425264` |

The principal article, `rigidity.tex`, has **109 pages**; the full technical manuscript, `main.tex`, has **285 pages**; `two_collision.tex` has **seven pages**. The historical directory name does not identify the current version. The preparation commit is not the compiled source. Comparing the compiled commit with the review-ready head shows no intervening modification of a compiled mathematical input. Page references below are to the principal PDF unless prefixed by F. [D1]

### Coverage

The fresh mathematical reading includes the headline statements and proof map; the finite Jacobi formula and relevant bridge interface; the two-ended relative determinant argument; the actual-smooth finite-jet factorization and homogeneous isolation; all of the new block proposition; the single-offset density inverse; interior-window extraction; clear-skeleton construction; the complete finite-congruence fiber argument; and the moving-family differential kernel and finite-coordinate argument. The graph-to-support appendix and the direct fixed-order estimation argument in the full manuscript were also examined. [S1–S10]

This is not a fresh line-by-line verification of all 401 pages. In particular, the entire earlier finite-action and full-phase construction, every prerequisite of the physical calibration theorem, the complete adaptive transcript-comparison catalogue, and the companion's mathematics are not certified by this report. The direct estimation argument is assessed with its cited calibration and test-implementation inputs, not presented as a fresh proof of those inputs. All-page mechanical reproduction has a different scope from mathematical review.

## 2. Disposition of the previous report

The preceding report is `reviews/a2-v57-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, frozen at `e14138660e716daf60471f3b98e8f1d30cb61a34`. It reviewed mathematical source `e39315c1fbb79ce71d1da91186a0d7e99a5ad8d6`. The current response was checked against the printed source, rather than treated as proof of compliance. [R1–R2]

| Previous issue or observation | Present disposition |
|---|---|
| R56-C1, already closed in v57: substantive acquisition input to Corollary 19.9 | **Remains closed.** The input and additional observation assumptions are explicit. |
| Equality of contact jets versus functional bounds on a common collar | **Remains closed.** Equalities are at anchored contacts; smooth bounds are on collars. |
| R57-M3: uniform conditioning of geometrically admissible highest-degree blocks | **Satisfactorily incorporated.** Proposition 12.9 proves the bound and credits its source. This was an optional refinement, not a previously fatal gap. |
| Separation of principal geometric article from the full technical corpus | **Retained.** The new proof is inside the existing contact section, not another independent probability appendix. |
| Exceptional mathematical significance | **Not resolved by the diagonal refinement.** This remains an evaluative reservation, not an allegation of a false theorem. |

The v57 memorandum is used for attribution, not as a substitute for the new printed proof. The coefficient-space and fixed-lower-jet consequences are correctly presented as consequences of the same estimate, not as separate general inversion principles. Already closed objections should not be reopened without a specific new reason.

## 3. The actual addition in v58

### R58-M1. Proposition 12.9 uses admissibility, not determinant one alone

The new source is `article/23a1_uniform_blocks_v58.tex`, with the statement and proof on principal pp. 48–49. Put

$$c_b=1+g\kappa_b>1,\qquad c=\sqrt{c_0c_1}=\cosh\gamma,\qquad t=e^{-\gamma},\qquad r_b=\sqrt{c_b/c_{1-b}}.$$

The decisive observation is

$$r_b=c/c_{1-b}<c,\qquad \lambda_b=r_bt<ct=\theta:=\frac{1+t^2}{2}<1.$$

This inequality restricts the apparent curvature asymmetry. It is stronger information than the relation $r_0r_1=1$. The two matrices are exactly

$$M_n^{\pm1}=\frac{1}{1-t^{2n}}
\begin{pmatrix}
1+t^{2n}&\pm2\lambda_0^n\\
\pm2\lambda_1^n&1+t^{2n}
\end{pmatrix}.$$

The signs on the off-diagonal entries change together. Thus the matrix and inverse have the same absolute row sums. For every $n\ge3$,

$$\max\{\|M_n\|_\infty,\|M_n^{-1}\|_\infty\}
\le\frac{1+t^{2n}+2\theta^n}{1-t^{2n}}
\le\frac{3+t^6}{1-t^6}=:C_\gamma.$$

Subtracting the identity and using $t^{2n}\le\theta^n$ gives

$$\max\{\|M_n-I\|_\infty,\|M_n^{-1}-I\|_\infty\}
\le\frac{4\theta^n}{1-t^6}=:K_\gamma\theta^n.$$

Replacing $t$ by $e^{-\gamma_*}$ gives uniform constants for $\gamma\ge\gamma_*>0$. No additional upper bound on the curvature ratio is needed for this isolated estimate. The constants deteriorate when the hyperbolic margin vanishes; that is not concealed. These calculations justify the displayed claim. [S4]

The independent rational controls check 2,790 admissible blocks at orders 3–64, including strongly unequal parameters and small positive hyperbolic margins. They also contain an inadmissible determinant-one example that violates the bound. That example illustrates why positivity matters; it is not a counterexample to the theorem. The general argument is the calculation above, not the finite sample. [D2]

### R58-M2. The smooth comparison is correctly restricted to a fixed-lower-jet slice

For two actual smooth graph pairs with the same gap and identical anchored jets through degree $n-1$, the lower-order remainder in

$$s_n=M_nq_n+R_n$$

is identical. The same is true of the leading geometry determining $M_n$. Consequently

$$\Delta s_n=M_n\Delta q_n,\qquad
C_\gamma^{-1}\|\Delta q_n\|_\infty
\le\|\Delta s_n\|_\infty
\le C_\gamma\|\Delta q_n\|_\infty.$$

The manuscript invokes the actual-smooth factorization before making this deduction. This ordering is correct: the identity is not being applied to a merely formal Taylor series and then asserted for arbitrary smooth boundaries. Odd coefficients are retained. The constant in this two-sided coefficient comparison is independent of the degree, whereas the functional assumptions and remainder bounds used to justify each finite jet are not declared order-uniform. [S3–S4]

This is a useful result, but it controls differences on a slice where all lower jets agree. It is not a stability estimate for two general noisy data vectors whose lower coefficients also vary. The distinction is material to the significance of the revision.

### R58-M3. The coefficient-space statement is valid, but only the correction gains radius

The norm is explicitly

$$\|x\|_R=\sum_{n\ge3}\frac{R^n}{n!}\|x_n\|_\infty.$$

Absolute summation gives a bounded block-diagonal isomorphism $\mathcal D=\operatorname{diag}(M_n)$ on $\mathcal A_R$. The exponential estimate gives bounded maps $\mathcal D-I$ and $\mathcal D^{-1}-I$ from $\mathcal A_R$ to $\mathcal A_{R/\theta}$. The stated truncation estimate is an operator estimate on the original $\mathcal A_R$, not a vanishing tail bound in the stronger target norm. The manuscript keeps these assertions separate. [S4]

A useful scope check is the formal coefficient sequence

$$x_n=\frac{n!}{R^n n^2}(1,0),\qquad n\ge3.$$

It belongs to $\mathcal A_R$ but not to $\mathcal A_{R/\theta}$. Since the first diagonal entry of $M_n$ is at least one, $\mathcal D x$ does not belong to the stronger space either. Thus the full diagonal operator is not a radius-improving operator. This is an illustration on the stated coefficient space, not a claim that this sequence is realized by a billiard. It agrees with, rather than contradicts, the printed restriction to the correction.

The complete finite derivative is different. Equation (12.36) writes

$$L_M=D_M+N_M,\qquad
L_M^{-1}=\left[\sum_{k=0}^{M-3}(-D_M^{-1}N_M)^k\right]D_M^{-1},$$

where $N_M$ is strictly block lower triangular. The new estimate controls $D_M^{-1}$, not the finite sum of powers. An abstract eight-dimensional lower-bidiagonal map with identity diagonal and subdiagonal $-3$ has inverse maximum row sum 3,280. This is a control for the logical distinction, not a realized billiard obstruction. The manuscript itself identifies the remaining lower-order coupling, density differentiation, and analytic continuation issues. **There is no demonstrated overclaim to repair here.** [S4, D2]

## 4. Re-examination of the mechanism carrying the paper

### R58-M4. Relative normalization is the important analytical step

The small reference twist is

$$d_j^0=\frac{\sqrt{a_0a_p}}{\sinh(j\gamma)},\qquad p=j\bmod2.$$

An absolute error estimate cannot simply be divided by this quantity. Theorem 7.2 instead starts from the exact normalized cofactor identity

$$\log b_j=\sum_i\log\{g[-\ell_{uv}(y_i,y_{i+1})]\}
-\log\det(I+G_j\Delta H_j).$$

The two-ended orbit gluing, summable endpoint localization of the Hessian perturbation, and compressed Green comparison are the steps that make this relative statement credible. The source does not estimate the trace norm by the number of interior sites times a crude uniform operator bound. It removes summable endpoint tails, then compares the two retained end blocks with the half-line operators. Reflected and cross-end terms are exponentially small. Fixed differentiation orders introduce polynomial factors that are absorbed using a strict exponential margin. [S2]

The logarithmic determinant comparison uses the appropriate estimate

$$|\operatorname{tr}(T^m-\widetilde T^m)|
\le m q^{m-1}\|T-\widetilde T\|_1,\qquad
\|T\|,\|\widetilde T\|\le q<1.$$

Together with absolute convergence of the differentiated trace series, this supports the passage from the finite relative determinant to the product of half-line amplitudes. The normalizing integral is subsequently placed on a common Morse-coordinate domain; the conditional-law step does not infer high-derivative density control from weak convergence alone. The finite Jacobi inverse and normalized cofactor were independently checked in 117 exact rational configurations. Those controls address finite algebra, not the trace-class limit. [S2, D2]

I have not established a fatal error in this interface. It should neither be dismissed as the determinant formula alone nor treated as certified by a successful finite computation. It is one of the substantive parts on which the paper's placement case must rest.

### R58-M5. The finite smooth remainder is not bypassed

Lemma 12.4, beginning on p. 45, interpolates actual graph functions with equal finite jets. On finite stationary actions the interior variations cancel. The terminal term is retained, estimated, and removed only after its decay is established. The direct graph perturbation is evaluated on orbits satisfying $|x_i(u)|\le C|u|\rho^i$. Integration in the interpolation parameter gives

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|
\le\frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

This argument uses functional smooth bounds on a collar, not just bounds on the first $M$ Taylor coefficients. The interpolation is local; it need not be a family of globally realized periodic tables to prove a local action-jet identity. Smooth flat remainders are therefore not a counterexample to the finite-order conclusion. Equality of complete smooth germs is not inferred. [S3]

In the highest-degree calculation, the endpoint is counted once and each interior contact twice. The resulting geometric series give the diagonal $\coth(n\gamma)$ and off-diagonal $r_b^n\operatorname{csch}(n\gamma)$. Nonlinear corrections to the orbit raise the endpoint degree, so they do not alter the new homogeneous block. The actual-smooth argument precedes the affine recursion. I found no new error in that ordering or in these multiplicities. [S3, D2]

## 5. What the downstream conclusions do and do not establish

### R58-G1. The law inverse retains signs but assumes strong, specified observations

On a positive interior square the four-density ratio cancels the unknown separate factors:

$$1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}=t(u)t(v),\qquad t=\frac{S}{d-S}.$$

A nonzero anchor fixes a positive scalar square root. This avoids differentiating a pointwise square root at the degenerate minimum and preserves odd action coefficients. The fixed-order stability proof uses positive density and anchor margins in a differentiable density norm. It is not a theorem that total variation controls high derivatives. [S5]

For a cropped window the mixed log derivative is

$$\partial_{xy}\log p(x,y)
=-\frac{S'(x-\xi)S'(y-\eta)}{[d-S(x-\xi)-S(y-\eta)]^2}.$$

The unique vertical and horizontal zero lines identify the origins under the printed visibility assumptions. The proof needs both origins inside the window, a positive denominator, noncentral slices with simple roots, and an anchor margin. Its local extension explicitly uses three extra derivatives. No unobserved cap boundary is substituted for these assumptions. Known signed units, directions, and excess time remain part of the observation model. [S5]

The exact law is a full function-valued datum, not a finite sample or a finite vector of histogram probabilities. Moreover, multiplying two recording efficiencies by $\varepsilon$ leaves the conditional law unchanged while multiplying recorded-success probability by $\varepsilon^2$. Thus exact conditional identification cannot by itself imply a uniform charged acquisition budget over arbitrary recording efficiencies. The manuscript acknowledges this distinction.

### R58-G2. The finite fiber argument includes the necessary admissibility checks

The clear-skeleton construction is an actual geometric construction. A blocked closest segment is replaced by shorter pairs whose total gap is no larger; uniform positive separation makes the descent finite. The resulting object is a graph path, not a specular billiard trajectory. Paths to representatives and two deck translates yield a finite quotient graph with two independent gains. A tree plus two additional edges gives $N+1$ channels. Uniform separation and a finite-translate bound justify persistence rather than assuming infinitely many clearance inequalities persist automatically. [S6]

In Theorem 20.3, noncircularity gives a finite proper symmetry group. A finite set of incidence congruence choices is enumerated. The proof tests agreement of all centered occurrences, reconstructs the lattice and centers, and then tests orientation, nonsingularity, disjointness, and selected-channel clearance. It does not infer realizability from a cochain equation alone. The lattice formula is

$$L=(v_1\ v_2)M^{-1},$$

with the actual invertible integer gain matrix, not an assumed unimodular one. Both inclusions in the fiber statement are supplied. The reverse inclusion uses equality of entire ordered channel pairs and cancellation of the global phase-volume factor under conditioning. [S6]

Finite ambiguity is not global uniqueness for every noncircular table. The asymmetric case is different. Likewise, the procedure is a finite-branch inverse of exact analytic images, not an effective numerical decision algorithm for equality of arbitrary analytic shapes. These limitations are printed and should not be converted into invented contradictions.

### R58-G3. The differential theorem does not confuse injectivity with immersion

The common holomorphic-strip assumption makes the parameter variation itself analytic. Pointwise analyticity of every member of a family would not suffice for the printed identity-theorem argument. The source supplies the stronger hypothesis, shrinks the strip when changing frames, and differentiates the moving reference operator in the amplitude:

$$\dot G=-G\dot H^0G,\qquad
\dot{\Delta H}=\dot H(u)-\dot H^0.$$

The nondecaying reference terms cancel before trace-class summation. The positive-part normalizer is differentiated using its regular level set and dominated convergence, not by introducing an unjustified boundary distribution. The finite graph-to-support appendix supplies the geometric change of coordinates used after the contact-jet derivative vanishes. [S7]

At a finitely symmetric base obstacle, the proof follows the actual local angular branch through the base congruence. It does not assume that a symmetry survives a symmetry-breaking perturbation. This gives the stated common infinitesimal Euclidean kernel. Theorem 21.6 then selects finitely many scalar test differentials only on a fixed immersed finite-dimensional model. Its lower Lipschitz estimate uses closeness to one invertible base derivative on a convex neighborhood, not pointwise nonsingularity alone. I found no new defect in these distinctions. [S7]

### R58-G4. Acquisition remains a substantive, additional theorem input

Corollary 19.9 explicitly invokes full Theorem F.47.3. The physical pilot includes planar endpoint positions, a clock, and preparation outcomes; the two types share one frame within a channel. Discarding longitudinal coordinates later does not turn the pilot into a transverse-histogram-only experiment. Its compact analytic family lies in one persistent asymmetric skeleton neighborhood. No common design across arbitrary unrelated neighborhoods is proved. [S8]

In the direct fixed-order risk argument, the separators and sample target are chosen before the final flight number; the pilot then uses that same final flight. Concentration is applied to the uncapped fresh success streams conditional on the pilot, with cap failure charged separately. It is not inferred that conditioning on successful completion of a cap preserves iid marks. The budget-indexed policy executes its chosen stage afresh, rather than claiming to run all previous stages within that cap. These parts of the direct argument are sound conditional on their cited inputs. [S9]

The full adaptive transcript comparison and every calibration prerequisite are outside a fresh complete certification here. The direct proof and the corrected dependency declaration should not be conflated with such a certification. There is no demonstrated circular use of this downstream acquisition theorem in the examined proofs of Theorem 1.1 or Theorems A/B. R56-C1 remains closed.

## 6. Originality and significance at the requested level

### R58-E1. The correct refinement does not change the principal importance question

The central relative long-bridge limit and its actual-smooth inverse constitute a coherent mathematical mechanism. Recovering the unknown lattice and registering channel images are real conclusions, not supplied answers. The work should not be dismissed simply because its later algebra can be summarized succinctly.

Nevertheless, the global statement uses deliberately selected alternating clear-channel bridges, marked incidences and gains, signed physical coordinates, known offsets, and complete conditional laws. It reconstructs full local action germs from rich function-valued observations and then invokes analyticity to propagate the images. This is a different information regime from a finite scalar inverse problem. The graph count $N+1$ does not change that regime. The model-local scalar-coordinate theorem and the compact-class consistency theorem do not turn it into one unrestricted finite-information reconstruction theorem. [S1, S5–S9]

Once the relative law and smooth contact inverse are established, several later operations have more limited independent novelty: cancellation of separate marginals, analytic propagation of an already known germ, finite congruence matching, the lattice cochain, and selection of a basis of test differentials. Their combination matters, but counting every consequence as a separate major innovation exaggerates the case. The new diagonal estimate is useful precisely because it localizes one conditioning issue; it neither controls the complete lower-triangular inverse nor supplies an effective general acquisition rate.

The leading-data comparison does establish a genuine distinction. The family with support $1+s\sin^4\theta+z(s)\sin^6\theta$ preserves the specified area and leading horizontal contact geometry while changing its fourth contact jet. Thus the nonlinear law carries information absent from the stated leading quadratic threshold record. It is not a pair with equal complete marked length spectra. The source says so. This comparison should be credited for its actual conclusion, not promoted into a comparison with every existing billiard inverse datum. [S10]

My placement judgment is therefore adverse: the current presentation and results do not make a sufficiently compelling case, to this reviewer, that the relative/smooth mechanism has the exceptional breadth and impact required for the requested general journals. This is not a categorical judgment that the mechanism lacks novelty or that another specialist could not value it more highly. A specialist recommendation in the opposite direction would need to explain the significance of this particular mechanism; revision numbers and build certificates cannot supply that explanation.

### R58-E2. The primary literature supports distinctions, not a redundancy or priority claim

The targeted primary-source check was refreshed. Finamore–Leguil's finite-horizon Sinai result uses an **enriched** marked length datum; its definition and Theorem A were checked on printed pp. 4–5. It should not be represented as an ordinary marked-periodic-length theorem. No reduction between that datum and the present conditional endpoint-law datum is established by this review. [L1]

De Simoi–Kaloshin–Leguil treats analytic open billiards under non-eclipse and the stated symmetry/genericity hypotheses with marked length data. Both its class and observation map differ from the present setting. The primary record was checked, not its complete proof. Its existence neither makes the present theorem redundant nor lets the present theorem claim to solve that different inverse problem. [L2]

Osius supplies established association-model context for separating marginal information from odds-ratio information. It does not supply billiard realization, the relative determinant theorem, or the actual-smooth contact inverse. Florio–Leguil's version-5 record expressly removes an affected geometric open-billiard spectral-rigidity assertion while retaining dynamical conclusions. The removed assertion must not be used as an established comparison theorem. [L3–L4]

These checks are not an exhaustive priority search. I make no first-priority claim and no assertion that the paper's main theorem is already known. A fair adverse review must engage its actual observation map and proof, not infer priority or redundancy from overlapping titles.

## 7. Required disposition

**R58-D1 — Mathematics:** no new mandatory core mathematical repair is established within the stated coverage. Proposition 12.9 and its scoped consequences are accepted by this audit. This is not certification of every theorem in either entry.

**R58-D2 — Existing corrections:** retain the anchored-contact wording, explicit acquisition dependency, restricted observation conventions, and the separation between diagonal and full nonlinear conditioning. These points are correctly implemented, not outstanding repair requests.

**R58-D3 — Placement:** decline at the requested level on the present exceptional-significance case. I do not recommend another repair-only round as though adding a small proposition, a stopping lemma, or another delivery certificate would resolve that judgment. Any substantive editorial reassessment should concentrate on the relative/smooth mechanism and its mathematical reach. Proving an unrelated stronger inverse problem is not being imposed as a correction to the stated theorems.

**R58-D4 — Scope and presentation:** preserve the principal article and the complete technical corpus without arbitrary mathematical deletion. The principal article should continue to distinguish exact law-valued rigidity, fixed-order density stability, model-local scalar coordinates, and physical acquisition under additional assumptions. The present source does so. No new probability section or blanket rewrite is requested.

## 8. Independent reproduction and evidentiary limits

The native artifact SHA-256 is

`4a3d7c6eaed1f4b927b0a05efe94b675a03c4463c4809da81238100dcfc2a868`.

The independent verifier checked all **699 frozen source files**, their lengths, SHA-256 values and Git blob identities, and reconstructed the manuscript subtree in Section 1. The active inputs comprise 111 main, 42 principal, and one companion path, with **121 distinct paths** in their union. All **45** native build-report evidence entries were checked. [D1]

Fresh builds, with shell escape disabled, succeeded for all three entries. All **401 pages** agree with the native PDFs in extracted text and same-renderer 72-dpi RGB arrays. The rebuilt PDFs are **not byte-identical**. The checked logs contain two principal and three full-manuscript underfull-box notices; no undefined-reference, undefined-citation, missing-glyph, overfull-box or LaTeX-error match was found. Actual visual inspection covered principal pp. **3, 19, 48 and 49**. No clipping or unreadable formula was observed on those pages. All-page computational parity is not described as all-page visual inspection. [D1]

The author's v58 checker was rerun under ordinary and optimized Python with identical successful output. Its preservation counts remain author diagnostics, not an independent semantic proof census. The separate independent script imports no author checker. It checks admissible blocks, 8,370 two-sided vector comparisons, finite coefficient sums, 117 finite Jacobi inverses/cofactors, signed density cancellation and mixed log derivatives, and scope controls for lower-triangular coupling and a nonunimodular gain matrix. Ordinary and optimized runs agree. [D2]

No finite diagnostic proves arbitrary-order smooth factorization, trace-class convergence, probability inequalities, analytic continuation, or global rigidity. Reproducibility is a necessary discipline; it is not a substitute for those arguments or a journal-significance judgment.

## Source keys

All S-keys refer to the actual compiled source `92a6d946c98e19c33ebff15997c0116ac158b89d`, under the manuscript directory in Section 1. Immutable source root:

https://github.com/TrillionniumFoundation/theta-theory/tree/92a6d946c98e19c33ebff15997c0116ac158b89d/papers/A2-v17-boundary-information-coarsening

- **S1:** `rigidity.tex`; `journal/00_principal_introduction_v56.tex`; `journal/01_structural_statements_v56.tex`. Theorem 1.1 and its proof map, especially principal p. 3; Theorems A/B and observation conventions.
- **S2:** `v3/10_geometry_action.tex`, especially lines 111–225; `v4/10_boundary_layers.tex`, lines 1–386. Theorems 7.2–7.3, principal pp. 18–20. The complete earlier finite-action construction is not freshly certified.
- **S3:** `article/23a_signed_endpoint_rigidity_v27.tex`, lines 1–600; smooth factorization, terminal envelope, homogeneous isolation, last-jet block and tangent inverse. Lemma 12.4, p. 45; Proposition 12.6, p. 47.
- **S4:** `article/23a1_uniform_blocks_v58.tex`, lines 1–124; Proposition 12.9 and equation (12.36), principal pp. 48–49.
- **S5:** `article/23f_single_offset_law_inverse_v42.tex`, lines 1–270; `journal/shared/23q_support_and_interior_windows_v52.tex`, lines 1–271. Theorem 13.1, p. 50; Theorem 14.6, p. 62.
- **S6:** `article/23j_generic_finite_channel_rigidity_v45.tex`, clear-skeleton and selected-locality arguments; `article/23n_finite_symmetry_v49.tex`, lines 1–243. Theorem 19.3, p. 84; Theorem 20.3, p. 91.
- **S7:** `article/23m_differential_rigidity_v48.tex`, moving reference, local kernel, analytic propagation, registration and finite coordinates; `journal/02_graph_support_v56.tex`. Theorems 21.5–21.6, pp. 99–100.
- **S8:** `article/23j_generic_finite_channel_rigidity_v45.tex`, lines 492–544; Corollary 19.9, beginning p. 89; `journal/DEPENDENCY_LEDGER_V58.md`.
- **S9:** `article/25b_augmented_global_reconstruction_v26.tex`, lines 1–254; direct finite-order risk and increasing-order budget argument, including full Theorem F.47.3, p. 194. Calibration prerequisites and the complete adaptive comparison are not freshly certified.
- **S10:** `v4/20_nonlinear_information.tex`, especially the area-preserving leading-data comparison at lines 116–195; current contribution discussion. No fresh certification of the entire older quartic calculation is claimed.
- **R1:** The v57 report at `e14138660e716daf60471f3b98e8f1d30cb61a34`, path specified in Section 2.
- **R2:** `RESPONSE_TO_REFEREE_V58.md`; `HISTORICAL_DERIVATION_AUDIT_V58.md`; `journal/DEPENDENCY_LEDGER_V58.md`; `LITERATURE_CHECK_V58.md`; review-ready README. The README is pinned to the review-ready head, not substituted for mathematical source.
- **D1:** `AUDIT_AND_REPRODUCTION.md`, `verify_artifact.py`, and `ARTIFACT_VERIFICATION.json` in this review directory.
- **D2:** `independent_checks.py` and `INDEPENDENT_CHECKS.json` in this review directory.

### External primary records

- **L1:** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1. https://arxiv.org/abs/2510.18983 ; versioned PDF https://arxiv.org/pdf/2510.18983v1 . Primary record and printed pp. 4–5 inspected.
- **L2:** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4; DOI 10.1007/s00222-023-01191-8. https://arxiv.org/abs/1905.00890 . Primary abstract and version metadata inspected.
- **L3:** G. Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37 (2009), 459–489; DOI 10.1214/07-AOS572. https://arxiv.org/abs/0903.0702 . Primary record inspected.
- **L4:** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120v5. https://arxiv.org/abs/2010.04120v5 . Version-specific abstract and correction notice inspected.
