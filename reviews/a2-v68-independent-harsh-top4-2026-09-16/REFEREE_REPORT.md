# Independent referee report on A2, revision 68

**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 16, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted external-referee-style assessment, not a commissioned journal report, an editorial decision, or a formal proof certificate. Correctness, originality, exceptional significance, and reproducibility are assessed separately. Author-side responses and verification records are claims to check.

## 1. Recommendation and frozen object

**Recommendation: do not accept at the requested highest general-journal level on the present exceptional-significance case. The smooth functional extension is substantive, and no new fatal mathematical error or mandatory core proof repair is established within this review's coverage.** All six statements in the new Section 11 withstand the examination below. There is one nonblocking archive-metadata issue, R68-P1; it has no effect on the theorems or the successful builds.

The previous formulation identified all smooth jets and used analyticity to identify contact germs. Revision 68 supplies a different final step: a weighted estimate on actual real functions removes a possible flat difference. It also gives complete real-profile stability with a finite-smoothness prior and an actual equal-area flat family. It would be incorrect to continue describing the contact-germ conclusion as analytic-only, or to object that the author has simply equated smooth functions with their Taylor series. My adverse placement assessment is reconsidered on the stronger theorem, not automatically inherited from the previous reports.

| Object | Immutable identity |
|---|---|
| Actual compiled mathematical source | `de0deffc2ca7b0fd2f0d2d5ad5fbdff1eee0f0a6` |
| Reconstructed manuscript subtree | `23f07201ea4c6a33270cf4d4a977da1eddf8e8fe` |
| Source branch | `revision/a2-v68-smooth-contact-rigidity-2026-09-16` |
| Referee-ready branch | `revision/a2-v68-referee-ready-2026-09-16` |
| Referee-ready head used as review parent | `419cd901ec5ed72f05e65fe6131a7463645660c9` |
| Native run / attempt / artifact | `35088239966` / `1` / `10442234606` |
| Previous v67 report | `2786efc1351e82f61a24ba4f827712e3e04ca39f` |
| Actual source reviewed in that report | `97b0c5bf15d6581c42b0f503bbe902c9d89b42db` |

The manuscript directory remains `papers/A2-v17-boundary-information-coarsening/`; its historical name is not a version identifier. The principal article has **157 pages**, the full technical manuscript **333 pages**, and the companion **seven pages**. The source-to-referee-ready comparison contains six later delivery commits and no changed compiled mathematical input. The new module was also fetched directly at the immutable source; its Git blob `1424b5fdd7e09f74e0f3900439704d6f21f39563` agrees with the downloaded archive. Page numbers below refer to the principal article. [D1]

### Coverage and exclusions

The complete 445-line new module `article/10d_smooth_contact_rigidity_v68.tex` was read, including every statement and proof. The review follows its dependencies through the signed one-step Jacobi construction, actual stationary envelope and finite-jet factorization, global curvature comparison, and two-offset extraction. The periodic weighted construction and relative determinant interface were re-examined. The revised central theorem, response, cover letter, historical audit, dependency ledger and literature note were checked against that chain. [S1–S6, R1–R2]

This is **not** a fresh line-by-line proof audit of all 497 pages. The complete older finite-chain/full-phase prerequisites, every analytic Banach-inverse detail, all global registration/lattice and moving-family proofs, the full calibration/statistical catalogue, and the companion are not freshly certified. In particular, retained acquisition results are not turned into a new smooth general-period statistical theorem by this review. All-page mechanical reproduction is a different assertion from mathematical coverage.

## 2. Disposition of the preceding report

| Previous issue or scope distinction | Disposition |
|---|---|
| R66-m1, closed in v67: propagate curvature stopping error through higher jets | Remains closed. The current change to the old module is a scope paragraph, not a reversion of the corrected recursion or bound. |
| Exact curvature and finite-jet uniqueness without candidate closeness | Retained and used as a genuine prerequisite. |
| Equal smooth Taylor series do not determine smooth germs | Still true for jets alone. The complete action identity now supplies the missing functional information. |
| Analytic norm inversion is distinct from exact identification | Retained. The new real estimate does not become a same-disc holomorphic estimate. |
| Mechanism-led central statement | Retained and materially strengthened, rather than enlarged only by another stopping correction. |
| Highest-level significance | Reassessed in Section 6; not settled by the absence of a mathematical error. |

Independent comparison verifies retention of all **855** inherited source paths: **846 unchanged** and nine modified with byte-exact originals archived. All **134** inherited active inputs remain; the new module makes **135**. The two old mathematical modules edited in this round have only the displayed smooth-jet/germ scope paragraphs changed. These are source-level findings, not a census of independent theorems. [D1]

## 3. The new functional argument

### R68-M1. A constant-one contraction is proved before the weight is chosen

Lemma 11.1, p. 52, needs more than a bound of the form $C\rho^j|u|$. Raising that estimate to a high vanishing order would introduce $C^m$, and a first visit with $C\rho>1$ would not be controlled by increasing $m$.

The source instead uses uniqueness of the actual decaying half-line to identify its shifted tail with the half-line at the next physical phase. Thus

$$x^t_{b,j}(u)=X^t_{b+j-1}\circ\cdots\circ X^t_b(u).$$

The signed Jacobi construction gives $(X_i^t)'(0)=\sigma_i(t)$ with $\max_{i,t}|\sigma_i(t)|<1$. Compactness of the finite set of phases and the parameter segment permits one collar with $\sup|(X_i^t)'|\le a<1$. Since every $X_i^t(0)=0$, successive mean-value estimates give $|x^t_{b,j}(u)|\le a^j|u|$. This is an actual orbit identity, not a newly assumed scalar model. [S1, S2]

The same collar controls the normal projection weights: the initial weight is between $1/2$ and $3/2$, and each internal weight between 1 and 3. At the reference orbit their values are 1 and 2. Finitely many clear nongrazing chords and uniform continuity justify these simultaneous bounds even though the tangent coordinates can have alternating signs. No normal-incidence assumption is inserted.

The ordering matters. For exact smooth uniqueness, the real collar and $a$ are chosen first; only then is a finite vanishing order selected. For the quantitative class, the enlarged positive quadratic box fixes the contraction margin, the order is fixed, and a sufficiently small common real collar is chosen using the stipulated finite derivative bounds. I found no circular choice in either construction. Uniformity is not claimed as curvature, incidence or clearance degenerates. [S1]

### R68-M2. The pair-dependent envelope is a valid separation estimate

Proposition 11.2, pp. 52–53, sets $h=G-F$ and integrates the actual shape derivative along $F^t=F+t(G-F)$:

$$g_b(u)=\overline\alpha_b(u)h_b(u)+(Kh)_b(u),\qquad g=\mathcal S(G)-\mathcal S(F).$$

For the fixed segment,

$$(Kh)_b(u)=\int_0^1\sum_{j\ge1}v^t_{b,j}(u)h_{b+j}(x^t_{b,j}(u))\,dt.$$

Although the coefficients depend on both candidates, this is a linear operator in a test function once that segment is fixed. Using it to estimate the actual difference is legitimate. It would not be legitimate to call this an observation-only reconstruction algorithm; the source expressly does not do so. [S1]

On the weighted real space,

$$\|h\|_{m,R}=\max_b\sup_{0<|u|\le R}|h_b(u)|/|u|^m,$$

one has

$$\|K\|\le\frac{3a^m}{1-a^m},\qquad
\|\overline\alpha^{-1}\|\le2.$$

Consequently, if $\theta_m=6a^m/(1-a^m)<1$,

$$\|h\|_{m,R}\le\frac{2}{1-\theta_m}\|g\|_{m,R}.$$

The weights are not required to be small on the whole unweighted function space. Only their high-vanishing tail must be small. Uniform domination by $a^{jm}|u|^m$ justifies the integral and series. The antecedent envelope retains the finite terminal term, bounds it and its stipulated derivatives, and sends it to zero before this parameter integration. Thus no terminal contribution is discarded merely by calling the series an action. [S1–S2]

As a scope check, the printed sufficient condition is exactly $a^m<1/7$. For $a=1/2$, $m=3$ works; for $a=19/20$, the first integer $m\ge3$ that works is 38. Constants can consequently be poor near weak contraction. This illustrates the declared dependence, not a contradiction or a claim that the threshold is optimal. Independent rational controls check these thresholds and six nonlinear composition models with the stated tail majorant; they are not substitutes for the geometric proof. [D2]

### R68-M3. Smooth germ identification uses the full data twice

Theorem 11.3, pp. 53–54, first applies two-offset extraction and global curvature uniqueness, then the signed finite-jet recursion. The curvature step is not inferred from nonsingularity of a Jacobian everywhere: the retained positive Schur fixed-point argument gives global injectivity and a two-point comparison. In particular, for equal Hessian data,

$$c_i-\widetilde c_i=-a_i\widetilde a_i(c_{i+1}-\widetilde c_{i+1}),$$

and the product around the cycle has absolute value below one. After this step, the same signed higher-order blocks and lower-jet remainders identify every finite jet. [S2–S3]

At this point the graph difference is flat, but the proof does **not** conclude that it is zero. It forms the segment of actual local graph representatives, chooses the common contraction collar, then picks a finite $m$ satisfying the weighted condition. Flatness makes $\|h\|_{m,R}$ finite by Taylor's theorem. Equality of the **complete actions** gives $g=0$ in the separation estimate, hence $h=0$ on the collar. No analyticity or initial candidate closeness is needed. [S1]

This is a correct way to bridge formal and functional identification. All jets are not being claimed as a sufficient observation. They are an intermediate consequence of a stronger, function-valued observation that is used again at the end. Once the contraction margin is fixed, the final step needs only one sufficiently high finite order. The pairwise exact theorem allows its neighborhood to depend on the candidates; it does not assert a universal collar for all smooth tables without bounds.

### R68-M4. The finite-smoothness stability proof aligns jets before estimating the tail

Lemma 11.4 and Theorem 11.5, pp. 54–55, assume a fixed positive quadratic box and a $C^{m+3}(I_0)$ graph bound. Their conclusion is a complete $C^0$ profile estimate from $C^m$ action or law error. It is not a same-regularity Banach inverse or a derivative-free error bound. [S1]

Let $\eta=\|\mathcal S(F)-\mathcal S(G)\|_{C^m(I)}$. The global two-point curvature bound identifies the degree-two error uniformly. Subtracting successive signed inversions then gives $|\Delta F_i^{(j)}(0)|\le C\eta$ for $2\le j<m$: only finitely many smooth remainder derivatives on bounded positive jet boxes are used. The proof does not assume that an everywhere invertible derivative alone gives global Lipschitz inversion. [S1, S3]

Define the actual polynomial correction

$$P_i(u)=\sum_{j=2}^{m-1}\frac{F_i^{(j)}(0)-G_i^{(j)}(0)}{j!}u^j,
\qquad G^\sharp=G+P.$$

Finite dimensionality gives $\|P\|_{C^{m+3}(I_0)}\le C\eta$. For sufficiently small error the two interpolation segments stay in one enlarged bounded positive class. The required estimate

$$\|\mathcal S(G+P)-\mathcal S(G)\|_{C^m(I)}\le C\|P\|_{C^{m+3}(I_0)}$$

is proved from the differentiated weighted equations and envelope, rather than assumed as a same-space differentiability theorem for composition. For $k\le m$, the coordinate derivatives decay exponentially. A term involving $P'$ obtains another decaying factor from $P'(x)=O(x)$; a term with at least two derivatives of $P$ has at least two coordinate-derivative factors. Thus the $C^m$ norm of $P\circ x_{b,j}$ is bounded by $C\rho^{2j}\|P\|_{C^m}$ and the series is summable. The stipulated derivative allowance is sufficient for this argument; no optimal derivative count is established or needed. [S1]

Now $F,G^\sharp$ and their actions have equal jets through degree $m-1$. Taylor's integral remainder gives

$$\|\mathcal S(F)-\mathcal S(G^\sharp)\|_{m,R}
\le\frac1{m!}\|\mathcal S(F)-\mathcal S(G^\sharp)\|_{C^m(I)}\le C\eta.$$

Applying weighted separation and removing $P$ proves $\|F-G\|_{C^0(I)}\le C\eta$. This polynomial-alignment step is essential: applying the weighted norm directly to two arbitrary noisy candidates would generally give infinity. The manuscript does not make that mistake.

Two-offset extraction is locally Lipschitz in $C^m$ under the stated density, residual and offset-separation bounds. It therefore gives the printed law-to-profile estimate. A finite-flight fit gives the stated deterministic comparison only in this same differentiated density norm and with uniform forward constants. Neither total variation nor a finite histogram alone supplies those derivatives. The earlier charged statistical conclusions remain separate. [S1, S2]

### R68-M5. The flat equal-area family is an actual geometric distinction

Proposition 11.6, pp. 56–57, adds $\varepsilon\chi(u)e^{-1/u^2}$ at one contact and uses a disjoint remote normal bump to preserve obstacle area. Positive curvature, embedding, disjointness and clearance persist for a sufficiently small parameter interval. The finite collection of contact collars leaves a boundary arc for the correction. Its nonzero area derivative permits the ordinary implicit function theorem; it does not change local half-lines contained in the contact collars. [S1]

All contact jets, and hence all future-action jets, remain fixed. Yet the initial envelope coefficient is positive and the perturbation is nonnegative, so

$$S_b^{-,\varepsilon}(u)-S_b^{-,0}(u)\ge\frac\varepsilon2 e^{-1/u^2}>0.$$

The stronger displayed asymptotic follows from $\alpha=1+O(|u|)$ and

$$a^{-2j}-1\ge j(a^{-2}-1),$$

which makes the normalized later-visit contributions a geometric tail. The same argument applies between any two nearby parameter values. The two-offset inverse then forces different complete laws on every sufficiently small common square. This is not a claim of identical normalized density jets: normalizing constants can change. Nor is it an equal-marked-length-spectrum example. These restrictions are printed and material. [S1]

There is an independent, particularly concrete realization check. Start with a unit disk and apply only to that obstacle the area-preserving shear

$$H_\varepsilon(x,y)=(x-\varepsilon\psi(y),y),\qquad
\psi(y)=\chi(y)e^{-1/y^2},\quad\psi(0)=0,$$

where $\chi$ is supported in $|y|<1/2$ and equals one near zero. Its Jacobian is identically one. The positively oriented boundary

$$R_\varepsilon(t)=(\cos t-\varepsilon\psi(\sin t),\sin t)$$

has curvature numerator

$$R_\varepsilon'\mathbin\times R_\varepsilon''
=1+\varepsilon\psi''(\sin t)\cos^3t.$$

It remains strictly convex for $|\varepsilon|\|\psi''\|_\infty<1$. Its right-contact normal graph is exactly $1-\sqrt{1-u^2}+\varepsilon\psi(u)$, with all jets unchanged. A second unit disk centered at $(4,0)$ gives a clear normal channel of gap 2; a sufficiently large fixed lattice keeps its translates disjoint. The opposite arc of the first obstacle automatically compensates area, and is not visited by this channel. Thus even a two-contact subclass has a direct exact-area witness of the asserted formal/functional distinction. This auxiliary construction does not replace the paper's arbitrary-marked-table construction.

The accompanying program checks the shear identities symbolically and computes twelve finite Euclidean stationary-chain configurations at 75 decimal digits. Their flat action signals are nonzero and approach the initial coefficient as the endpoint approaches zero. The program is a finite diagnostic, not a certificate of an infinite-orbit limit or of a numeric global cutoff margin. The general argument is the envelope and geometric construction above. [D2]

## 4. Retained interfaces and observation limits

The new smooth theorem does not prove its own forward input. The retained relative proof normalizes the exact corner cofactor before taking a limit. Its Green comparison, summable endpoint perturbations and trace-series continuity yield a relative mixed-derivative estimate despite the exponentially small reference twist. An absolute action error divided by that twist is not an acceptable replacement. The relevant weighted construction and two-end determinant interface were re-examined; no new defect was established there. This is not certification of every earlier finite-chain prerequisite. [S4]

The actual graph sensor records a scaled tangent projection, not the unknown normal graph value. The physical endpoint actions contain the restored linear momenta. Two-offset cancellation assumes common amplitudes across the offsets and unrelated positive normalizers; it does not license arbitrary offset-dependent detector changes. The new theorem's phrase “without a flux model” means that the stipulated common amplitude functions need not be supplied, not that every possible recording mechanism is admissible. [S2]

Smooth contact identity does not determine unvisited smooth arcs. Whole-obstacle identity still uses the analytic continuation, placement/lattice and full-visitation hypotheses of its separate theorem. The local bounded-holomorphic inverse also remains a different normed-space conclusion. The corrected finite-iteration error remains $C_M(\tau^N+\varepsilon)+L_ME_m$, not coefficient-one propagation or an all-order unweighted bound. [S1, S3, S5]

## 5. Primary-literature context

The targeted primary-source check was refreshed. Bálint–De Simoi–Kaloshin–Leguil's Theorem D and Corollary E give general-period length asymptotics and marked Lyapunov recovery in their open-billiard setting. Their Remark 2.3 explains a contact-separation limitation of those asymptotic relations; it is not an impossibility theorem for every use of the marked length spectrum. Printed pp. 9–10 were inspected. The present fixed polygon and phase-resolved endpoint functions are different observations. The flat example does not supply equal full marked length spectra. [L1]

De Simoi–Kaloshin–Leguil's analytic open-billiard result has non-eclipse, symmetry and genericity assumptions. Finamore–Leguil's Sinai result uses an **enriched** marked length datum. Removing analyticity from the present contact theorem is not a removal of hypotheses from either of those different inverse problems. The primary Florio–Leguil version-5 notice explicitly removes the affected geometric spectral-rigidity assertion while retaining dynamical conclusions; that removed assertion is not an available competing theorem. [L2–L4]

This is a targeted statement/observation comparison, not an exhaustive priority search or a proof audit of those works. I make neither a first-priority claim nor an allegation that the manuscript's central theorem is already known. The abstract contraction inequality is readily checked once the actual envelope and one-step collar are available; that fact alone does not establish prior art for their geometric combination.

## 6. Exceptional significance and editorial judgment

### R68-E1. A genuine smooth extension, but not a different observation problem

Revision 68 removes a real limitation. The earlier formal inverse could not exclude smooth flat changes. The complete law now identifies them, with a finite-smoothness profile estimate and an actual area-preserving witness. This is not another arithmetic amendment, and it cannot fairly be dismissed as merely replacing the word “analytic” by “smooth.” It materially strengthens the central relative-law/contact mechanism.

Nevertheless, I remain unconvinced by the requested highest general-journal placement. The decisive input is still an independently resolved function-valued law at each phase of a supplied collision polygon, in fixed signed coordinates and at separated controlled offsets. Once that law has provided the complete action, the new functional step exploits an invertible pointwise contribution and strictly contracted later evaluations. The high-weight contraction and polynomial alignment are effective, but the new section does not exhibit an additional analytical obstruction beyond the geometric envelope and uniform collar already carrying the mechanism. Its value is the correct completion of that mechanism in the smooth category, not a new general theory of ill-posed inversion.

The flat family establishes a precise distinction between formal local data and complete real data. It does not establish superiority to the full observation maps in the cited inverse-spectral literature. Likewise the smooth extension is contact-local, whereas whole-boundary smooth rigidity and a general-period weak-noise acquisition theorem are not consequences of it. These facts are not hidden errors, and I do not impose those different theorems as repairs. They do limit the breadth that can be inferred from the new statement and example.

The paper's strongest placement case must therefore rest on the combined relative physical law and actual geometric envelope, including this smooth completion, rather than on treating every inversion, interpolation, area correction and downstream consequence as another independent breakthrough. After examining the new step, I do not find the present case for exceptional depth and mathematical influence sufficiently persuasive. This is an evaluative recommendation, not proof of lack of novelty, and another specialist may assess the mechanism more favorably.

### R68-E2. No manufactured mathematical repair cycle

The earlier stopping correction is closed. The contact conclusion is no longer analytic-only. The absence of a newly established fatal error should neither be promoted to complete certification nor converted into a demand for an unrelated stronger theorem merely to keep producing adverse reports. I request no arbitrary deletion of the mathematical corpus or another detached abstraction section.

A further independent editorial assessment should engage the actual relative-law/smooth-contact theorem, with its fixed marks, its full functional datum and its genuine flat-information consequence. The nonblocking packaging issue below is worth correcting but cannot settle that mathematical importance judgment.

## 7. Nonblocking delivery issue and disposition codes

### R68-P1. Two source-ZIP permission headers differ from the recorded Git modes

Both the v67 baseline and v68 `native-source.zip` contain the following entries with raw ZIP mode `100644`, while their source manifests record `100755`:

- `tools/check_adaptive.py`;
- `tools/retain_native_v65.py`.

All their bytes and Git blob identities verify. The recorded Git modes are unchanged between revisions, and reconstructing the manuscript tree **with the manifest modes** gives the expected subtree. Thus this is an inherited archive-metadata discrepancy, not a demonstrated change of the remote Git modes or a source-integrity failure. It does not affect invoking the scripts with Python or the successful manuscript builds. [D1]

For a fully faithful archive, preserve the executable bits in these ZIP entries. Alternatively, make the manifest-based permission-restoration step explicit for users who reconstruct the Git tree. The present review does not claim that every raw ZIP permission header agrees with the manifest. This is a nonblocking reproducibility correction, not a mathematical blocker.

**R68-D1 — New mathematics:** the six statements of Section 11 withstand the scoped examination; no mandatory core repair or fatal counterexample is established.

**R68-D2 — Updated scope:** credit complete smooth contact-germ identification without candidate closeness and finite-smoothness real-profile stability. Do not resurrect an analytic-only or “jets imply functions” objection.

**R68-D3 — Retain qualifications:** fixed polygon and observation coordinates, common two-offset amplitudes, density derivative norm, finite-smoothness prior, class-dependent collar, and the separate analytic-global/acquisition conclusions remain essential and correctly declared.

**R68-D4 — Delivery:** address the nonblocking ZIP-mode discrepancy or document restoration precisely. It does not reopen the mathematical stopping correction.

**R68-D5 — Placement:** do not accept at the requested level on the current exceptional-significance case. This is not a priority verdict or a demand for another nominal theorem-repair iteration.

## 8. Reproduction and evidentiary limits

The downloaded artifact SHA-256 is `d4544c5f2b523877bb660835d1162afed4ccccfb9cd6066548b53934c08bc5c6`. Independent verification checked **876 frozen files**, **135 distinct active inputs** and **47 native build-report evidence entries**. The manifest-mode reconstruction matches the manuscript subtree. The v67 comparison independently verifies the retention figures above and detects R68-P1. Per-entry active counts are 124 full, 56 principal and one companion. [D1]

Fresh companion/full/principal builds succeeded with shell escape disabled and regenerated auxiliaries. All **497 pages** agree with the native PDFs in extracted text and same-renderer **72-dpi RGB arrays**. PDF bytes differ. Final logs retain seven full and two principal underfull notices, none in the companion; the additional scan found no undefined references/citations, multiply-defined-label, missing-character, overfull-box or LaTeX-error match. Actual visual inspection covered principal pp. **53, 55 and 56** at **108 dpi**. No clipping or unreadable expression was observed on those pages. Rendering additional pages for possible inspection is not counted as actually inspecting them. [D1]

The new diagnostic imports no author code. It checks five exact weighted thresholds, 720 exact nonlinear evaluation bounds in six averaged models, one constant-one negative control, the symbolic two-offset identity and 54 rational instances, twelve flat-derivative recurrences, the exact shear area/curvature formulas, and twelve actual finite chord configurations. Its largest scaled finite envelope discrepancy is below $9\times10^{-25}$ at 75-digit working precision. Twelve doubled-initial-contact controls are detected. Normal and optimized Python emit identical JSON. These are exact finite algebra and high-precision numerical controls, not interval certificates or proofs of infinite-dimensional limits. The author's mathematical/preservation checker was not rerun. [D2]

The report, evidence summary and reproduction utilities accompany this review. Only review files are added to the new branch; manuscripts, prior reports, native deliveries, default-branch refs and repository permissions are not edited.

## Source keys

All S-keys refer to actual source `de0deffc2ca7b0fd2f0d2d5ad5fbdff1eee0f0a6` under `papers/A2-v17-boundary-information-coarsening/`.

- **S1:** `article/10d_smooth_contact_rigidity_v68.tex`, lines 1–445; all six statements in Section 11. Lemma 11.1 and Proposition 11.2 begin p. 52; Theorem 11.3 p. 53; Lemma 11.4 p. 54; Theorem 11.5 p. 55; Proposition 11.6 p. 56.
- **S2:** `article/10b_periodic_contact_inverse_v65.tex`, particularly lines 15–347: graph marks/sensor, signed half-line contraction, two-offset identity, actual envelope, finite-jet factorization and cyclic response.
- **S3:** `article/10c_global_curvature_inverse_v66.tex`, quadratic Schur identity and global fixed-point inverse, two-point bound, exact identification and retained v67 stopping/propagation formulas. The whole stopping proof is not presented as a newly independently certified result here.
- **S4:** `article/10a_periodic_itinerary_relative_v64.tex`, weighted construction, half-line actions and relative determinant comparison, especially lines 190–350. Not a complete fresh certification of every finite-chain/full-phase prerequisite.
- **S5:** `article/00g_contact_synthesis_v66.tex`; `article/00h_abstract_v66.tex`; `rigidity.tex`; `journal/DEPENDENCY_LEDGER_V68.md`. Main statement, observation separation and dependency route.
- **S6:** `RESPONSE_TO_REFEREE_V68.md`, `COVER_LETTER_V68.md`, `HISTORICAL_DERIVATION_AUDIT_V68.md`, `LITERATURE_CHECK_V68.md`; author-side scope and provenance, not proof substitutes.
- **R1:** v67 report at `2786efc1351e82f61a24ba4f827712e3e04ca39f`, path `reviews/a2-v67-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md`.
- **R2:** source-to-referee-ready comparison and `A2_REVISION_V68_REVIEW_READY.md` at `419cd901ec5ed72f05e65fe6131a7463645660c9`.
- **D1:** `AUDIT_LEDGER.md`, `AUDIT_RESULTS.json`, `verify_delivery.py`, `compare_baseline.py` in this review directory. Full emitted records, logs and sampled images are retained in the accompanying local audit archive.
- **D2:** `independent_checks.py`; results summarized in `AUDIT_RESULTS.json`. The program emits the detailed records and explicitly limits their interpretation.
- **L1:** P. Bálint, J. De Simoi, V. Kaloshin, M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, DOI 10.1007/s00220-019-03448-x, arXiv:1809.08947; author manuscript, printed pp. 9–10: https://leguil.perso.math.cnrs.fr/Articles/Balint_DeSimoi_Kaloshin_Leguil.pdf .
- **L2:** J. De Simoi, V. Kaloshin, M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4, DOI 10.1007/s00222-023-01191-8: https://arxiv.org/abs/1905.00890v4 .
- **L3:** D. Finamore, M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1: https://arxiv.org/abs/2510.18983 .
- **L4:** A. Florio, M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120v5, including the explicit correction notice: https://arxiv.org/abs/2010.04120v5 .
