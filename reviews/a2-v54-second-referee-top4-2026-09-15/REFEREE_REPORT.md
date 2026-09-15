# Second independent referee memorandum on A2, revision 54

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 15, 2026  
**Requested standard:** the highest general mathematics journals. This is an author-requested, AI-assisted referee-style assessment, not a commissioned report or a decision of any journal.

## 1. Recommendation and the object actually reviewed

**I do not recommend acceptance at the requested highest general-journal level on the present contribution and article-level case. This is not a finding that the principal rigidity theorem is false.** In the mathematical coverage specified below, I find **no mandatory correction to the strengthened Corollary 23.3 or new Theorem 23.4**, and no newly established fatal error in the inherited proof interfaces examined. The v53 Hellinger and waiting-record requests are closed. A severe assessment should not manufacture an error, reopen a correctly resolved objection, or confuse a negative placement judgment with a demand for an endless sequence of additional theorems.

The frozen review-ready object is `802cb27e731a3a821903a7308cba9d5da29bbf79`, on `revision/a2-v54-review-ready-2026-09-15`. Its actual compiled mathematical source is `2cedae961195f97df802aaa81112d95cd32974e1`, with manuscript subtree `407b278984b14e57468e727fb56b0fa4163a7207`. The historical directory name `papers/A2-v17-boundary-information-coarsening` does not identify the current version: this is **A2 v54**, comprising a 281-page main article and a seven-page companion. The default branch's older A1 is not the reviewed manuscript. [D1]

This assessment includes the complete new Section 23, its actual-table realization and likelihood calculation, the current response and introduction, the nonlinear relative-law module, the signed finite-jet mechanism, interior-window extraction and geometric-fiber proof, the differential inverse, selected finite-symmetry matching arguments, and the calibrated-histogram interface. It is **not a fresh line-by-line certification of all 288 pages**, all older local statistical experiments, the complete selected-skeleton construction, every full-phase event construction, or the companion's mathematics. The exact reading coverage and source identities are recorded in [the audit ledger](AUDIT_AND_REPRODUCTION.md).

A v54 report already existed at `1030ca91a96ca1be8ecd0347ecbdac7084cdd8d4` when the destination branch was checked. It is preserved. This memorandum is deposited separately, not substituted for that report. Its stopped-count reductions overlap the reductions in Section 5 of that earlier memorandum; I acknowledge that overlap and make no priority claim for those elementary consequences. The local byte verification, rebuild and finite checks accompanying the present memorandum were performed for this assessment. [R3, D2]

## 2. Disposition of the preceding requests

The author's response correctly identifies the v53 report at `000ce24f65f8381d2180cbd1f080d3d8470c8157`, concerning mathematical source `42cc62f230473c34d78af1d06b9ca5c2651ae86d`. That report did not identify a mandatory correction to its three new statements. The present changes are strengthenings, not admissions that those previous statements were false. [R1, R2]

| Item | Finding in the present audit | Disposition |
|---|---|---|
| Quadratic Hellinger error and square-root product comparison | Correct positive-density argument and tensorization | Closed |
| Direct mean test without full-product approximation | Correct separation of the two arguments and their hypotheses | Closed |
| First waiting count for the same actual table/profile pair | Exact stopping factorization; both deficiency directions proved | Closed |
| Deterministic cap rather than expected completion | Full capped-record risk, necessity, sufficiency and charge all proved | No correction identified |
| Actual nonlinear realization and fixed recording profiles | Higher action coefficients retained; profiles fixed as the window shrinks | Retained correctly |
| Smooth versus statistical topology, nuisance projection, finite symmetry and attribution | Distinctions preserved in the inspected source | Not reopened |
| Highest-journal significance | A separate editorial judgment | Not a mathematical repair ticket |

The revision replaces an existing corollary and its proof, adds the stopping theorem in the same section, and credits the Hellinger and uncapped waiting-record contributions to the v53 memorandum. It does not silently promote their provenance into independent journal endorsement. Preservation counts are useful source-management information, not a mathematical measure of importance. [R2, D1]

## 3. Technical examination of the changed results

### M1. The fixed physical collar, not weak convergence alone, controls the shrinking crop

The corollary uses a uniform interior density bound before the crop. With the source's notation,

$$\|f_{s,J}-f_s\|_{C^0([-h_0,h_0]^2)}\le C\tau^J.$$

The recording weight $w_s$ and its reciprocal are bounded on that fixed square. Hence the recorded window normalizers obey

$$A_{s,J}(h)\asymp h^2,\qquad
|A_{s,J}(h)-A_{s,\infty}(h)|\le Ch^2\tau^J.$$

Subtracting the rescaled quotients

$$q_{s,J,h}(z,w)=\frac{h^2w_s(hz,hw)f_{s,J}(hz,hw)}{A_{s,J}(h)}$$

cancels the area factors. This proves the stated $C\tau^J$ supremum error without an inverse-area loss. A generic conditional-total-variation inequality would be weaker; pointwise weak convergence for each fixed window would be insufficient. The manuscript uses the stronger hypothesis actually established by its relative-law argument. [S2, lines 320–346; S3]

Both rescaled densities are bounded below by a common $m>0$. For the convention $H^2=\int(\sqrt p-\sqrt q)^2$ on a square of area four,

$$H^2(P,Q)=\int\frac{(p-q)^2}{(\sqrt p+\sqrt q)^2}
\le m^{-1}\|p-q\|_\infty^2.$$

Affinity tensorization and $\operatorname{TV}\le H$ therefore give

$$H^2(Q_{s,J,h},Q_{s,h})\le C\tau^{2J},\qquad
\operatorname{TV}\!\left(\bigotimes_{k=1}^nQ_{s,J,h}^{(k)},
\bigotimes_{k=1}^nQ_{s,h}^{(k)}\right)
\le\min\{1,C\sqrt n\,\tau^J\}.$$

The bound applies to a fixed allocation among the four labels and passes to optimal equal-prior risks by taking infima over tests. Consequently $n\tau^{2J}\to0$ is sufficient. The old condition $n\tau^J\to0$ remains sufficient; it has not been rendered false. The absence of a density floor would invalidate the quadratic conclusion, and the independent finite controls deliberately test that failure. [S2, lines 346–368; D2]

### M2. The direct exponential test is a different argument

The ideal exact mean contrast for $F(z,w)=1/9-z^2w^2$ is $D_h=c_0h^4+O(h^6)>0$. Each finite-flight mean differs from its ideal counterpart by $O(\tau^J)$. If $\tau^J=o(h^4)$, the ideal midpoint is on the correct side of every finite-flight mean at distance at least $D_h/4$. Since $F$ has range length one, the same bounded-variable exponential estimate gives

$$\text{error}\le e^{-nD_h^2/8}\le e^{-c'nh^8}.$$

This is a direct test bound under the finite-flight laws, not a deletion of the product-comparison error. It remains useful when the product distributions are not known to be close. The explicit even-flight choice with coefficient $(4+\varepsilon)/|\log\tau|$ is a sufficient logarithmic choice, not an optimal convergence exponent. No correction is needed here. [S2, lines 369–408]

### M3. The retained realization and information constants are consistent

For even $C^4$ actions, $a_i=S_i''(0)>0$, and the source's exact window normalizer,

$$q_{i,h}=\frac14+\frac{a_i^2h^4}{16d^2}
\left(\frac19-z^2w^2\right)+O(h^6),\qquad
\int_{[-1,1]^2}\left(\frac19-z^2w^2\right)^2=\frac{224}{2025}.$$

Thus the leading squared Hellinger coefficient is $7(a_1^2-a_0^2)^2/(16200d^4)$. Omitting the denominator correction would change this coefficient. The critical likelihood variance coefficient is four times this number under the declared Hellinger convention. The bounded triangular-array likelihood argument and the exact-midpoint mean test justify the three stated testing regimes. [S2, lines 18–263; D2]

The geometric family is not a stipulated quadratic action. For $R=1/10$ and $s\in[R/128,R/64]$, its support is $k_s(\theta)=R+s(\cos4\theta-1)$, with radius of curvature at least $3R/4$. Integer translates are disjoint, and the axis closest-contact segments have a common gap $4/5$ and positive clearance from every third obstacle. Symmetries identify the displayed channel actions and make them even. The actual half-line Hessian gives

$$a_s^2=\kappa_s^2+2\kappa_s/g,\qquad
\kappa_s=(R-16s)^{-1},\qquad
\Delta=a_1^2-a_0^2=22900/441.$$

The chosen recording probabilities are bounded, positive, fixed on a common collar, and independent of the shrinking window. They may differ between the two alternatives. Their admissibility does not supply a detector that can be programmed from an unknown table, and the theorem does not claim that. Neither nonzero higher Taylor coefficients nor absence of a global finite-horizon hypothesis contradicts this local-channel construction. [S2, lines 95–216]

### M4. The waiting-record separation uses actual bridge probabilities

The two alternatives have

$$p_{i,h}\asymp h^2e^{-\gamma_iJ_h},\quad
\gamma_0=\operatorname{arcosh}(71/7),\quad
\gamma_1=\operatorname{arcosh}(35/3)>\gamma_0.$$

The $h^2$ factor is the recorded fraction; the exponential factor is the physical bridge probability. Their ratio tends to zero for any even $J_h\to\infty$. For this one-record statement no relation between $h$ and $\tau^{J_h}$ is required. Independent repeated preparations give the exact identity

$$\Pr_i(W_h=k,Y_h\in A)=(1-p_{i,h})^{k-1}p_{i,h}Q_{i,J_h,h}(A).$$

Discarding $W_h$ therefore gives the conditional mark from the same acquisition, rather than a different sampling policy. The mark distance is $O(h^4+\tau^{J_h})\to0$. The threshold $\lceil(p_{0,h}p_{1,h})^{-1/2}\rceil$ on $W_h$ has both errors tending to zero. Projection proves zero deficiency in the forgetting direction; contraction plus the triangle inequality gives reverse deficiency at least $1/2$ asymptotically; the equal-mixture kernel gives the matching upper bound. The kernel depends on the two stipulated laws, not on the unknown generating alternative. [S2, lines 417–547]

### M5. The deterministic-cap result establishes a lower bound as well as an upper bound

Write $a_i=1-(1-p_i)^b$, with $p_1<p_0$. The capped laws share a cemetery atom of mass at least $1-a_0$. Testing the event of acceptance and using that common atom yield

$$a_0-a_1\le\operatorname{TV}(F_0^{[b]},F_1^{[b]})\le a_0.$$

This does not assume equal terminal mark laws. If $bp_0\to\lambda<\infty$, then $bp_1\to0$, and the sandwich gives

$$R_h^*(b_h)\longrightarrow\frac12e^{-\lambda}.$$

The any-acceptance test attains this limit. For arbitrary caps with $bp_0\to\infty$, the threshold truncated at the cap remains observable and has vanishing errors. If $bp_0$ fails to diverge, a finite-limit subsequence gives a positive limiting risk. The necessity assertion is therefore proved, not inferred from a sufficient test. [S2, lines 548–582]

At enormous caps with $bp_1\to\infty$, the any-acceptance bit need not discriminate, but the manuscript correctly uses the finer waiting threshold in that regime. The independent negative control checks precisely this distinction; it is not a counterexample to the theorem. Finally,

$$\mathbb E_i\min(W_h,b_h)=\frac{1-(1-p_{i,h})^{b_h}}{p_{i,h}}$$

is the tail-sum identity with the correct convention that $W$ includes the successful preparation. The charge counts failures and never conditions on successful completion of the cap. The resulting scale $h^{-2}e^{\gamma_0J_h}$ is a specified-pair preparation scale, not the successful-mark scale $h^{-8}$ and not a complexity bound optimized over all acquisition designs. [S2, lines 583–595]

## 4. An independently checked reduction of the stopped experiment

The following calculation explains the extent of the new statistical conclusion. It agrees with the reductions already present in [R3, Section 5]; it is included as a verification and interpretation, not as a new requirement or priority claim.

Let $C_h^{[b]}$ retain the censored waiting count only, and let $F_h^{[b]}$ additionally retain the terminal mark. Put $\epsilon_h=\operatorname{TV}(Q_{0,J_h,h},Q_{1,J_h,h})$. Deleting the mark is exact. In the reverse direction, append a mark from $Q_{0,J_h,h}$ independently to each numerical count and preserve the cemetery outcome. The simulation is exact under alternative zero; its error under alternative one is exactly $a_{1,h}\epsilon_h$. Therefore

$$\delta(F_h^{[b]},C_h^{[b]})=0,\qquad
\delta(C_h^{[b]},F_h^{[b]})\le a_{1,h}\epsilon_h\le\epsilon_h\to0,$$

uniformly over deterministic caps. For equal-prior risks,

$$0\le R_C^*(b)-R_F^*(b)\le\tfrac12a_{1,h}\epsilon_h.$$

The count-only risk has a finite formula. For $0<p_1<p_0<1$, its accepted-count likelihood ratio is

$$\frac{p_0}{p_1}\left(\frac{1-p_0}{1-p_1}\right)^{k-1},$$

which decreases with $k$, while the cemetery likelihood ratio is below one. Set

$$t=\min\left\{b,\left\lfloor1+
\frac{\log(p_0/p_1)}{\log((1-p_1)/(1-p_0))}\right\rfloor\right\}.$$

Either decision at an equality gives the same risk, and

$$R_C^*(b)=\tfrac12\{(1-p_0)^t+1-(1-p_1)^t\}.$$

Exact rational enumeration of 30 finite laws verifies the formula, the simulation error, the full/count risk inequality, the common-cemetery bounds and the stopped charge. These checks use unequal marks. They do not assert this is the exact finite risk of the full mark/count experiment, or a relative-error approximation to a very small risk. [D2]

The conclusion is that the waiting count already carries the asymptotic discrimination in this particular stopped experiment. The genuinely geometric input is the realization of the probabilities and their different hyperbolic exponents. The final threshold and common-atom computations are elementary once that input is available. This confirms the theorem and also limits how much additional general inferential content should be assigned to it.

## 5. Checks of the inherited foundation and the acquisition interface

### M6. Relative normalization is a substantive analytical step

The exponentially small reference twist is not controlled by an arbitrary absolute action remainder. The relative proof instead combines the exact cofactor identity with

$$\log b_j=\sum_i\log\{g[-\ell_{i,uv}(y_i,y_{i+1})]\}
-\log\det(I+G_j\Delta H_j).$$

Localized tridiagonal perturbations are trace class. Gluing the two half-lines gives an exponentially small residual, controlled through diagonal dominance; endpoint-block truncation and comparison of reference Green kernels yield a trace-norm error. The trace-series estimate retains a trace-ideal factor rather than multiplying an unweighted norm bound by the entire flight length. Fixed-order differentiated estimates absorb polynomial length factors into strict exponential margins. The positive fixed-offset integral retains nonlinear actions. I found no new normalization defect in this inspected argument. Its earlier physical event construction is not independently recertified by this conclusion. [S3]

### M7. The signed contact inverse is not merely a formal-series calculation

The finite stationary envelope retains its terminal term until the half-line limit. For graph pairs sharing an $M$-jet, its actual remainder estimate is

$$|S_b^{[1]}(u)-S_b^{[0]}(u)|\le
\frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.$$

Only after representative independence is established does the last-jet block appear:

$$M_n=\begin{pmatrix}\coth(n\gamma)&r_0^n\operatorname{csch}(n\gamma)\\
r_1^n\operatorname{csch}(n\gamma)&\coth(n\gamma)\end{pmatrix},
\qquad r_0r_1=1,\qquad\det M_n=1.$$

The boundary/interior multiplicities are one and two respectively. The inverse is triangular at each fixed finite order, not uniformly conditioned as the order diverges. Equality of complete obstacle images subsequently uses analyticity; arbitrary smooth germs with the same Taylor series are not identified. The signed odd jets have not been removed. [S4]

### M8. Window and differential rigidity retain indispensable hypotheses

The mixed logarithmic derivative of the recorded density has the form

$$-\frac{S'(x-\xi)S'(y-\eta)}{[d-S(x-\xi)-S(y-\eta)]^2}.$$

Its zero fibers locate the origins because both critical lines remain inside the known positive window. A nonzero scalar anchor then recovers the action from the density ratio. This is a local smooth inverse with derivative loss, not a total-variation-to-derivatives estimate. Both inclusions of the geometric fiber are present: accepted ideal branches reproduce the local actions and amplitudes, and the original windows and profiles can be reused. The projected joint nuisance/table kernel is not identification of every nuisance profile. [S5]

The differential proof explicitly differentiates the moving reference, including $\dot G=-G\dot H^0G$ and both terms in $\frac{d}{dt}(G\Delta H)$. It differentiates the finite jet recursion, including the derivatives of the lower-jet term and the leading block. The common-strip family assumption makes the variation itself analytic. A local harmonic lift follows actual congruence branches, even through symmetry breaking; finite global rotations are not continuous derivative ambiguities. The lattice uses the actual gain-matrix inverse, not an assumed unimodular basis. Finally, finitely many scalar observables are selected only on an immersed finite-dimensional model, and the lower Lipschitz estimate compares the derivative to one fixed invertible matrix on a convex ball. These are the necessary arguments; undifferentiated injectivity would not substitute for them. [S6, S7]

### M9. The calibrated histogram result uses a genuinely richer experiment

I additionally examined the complete calibrated-histogram module rather than treating its introductory description as a proof. It keeps separate the fixed-offset density perturbation, the flight-amplified timing error $\Delta=Jv_g+v_t$, and the hard-cell crossing term. The categorical bound includes the complement of the recording square as well as internal grid edges. Conditioning on pilot histories is handled by uniform deterministic bounds; the capped acquisition is compared to uncapped independent records rather than conditioned on favorable completion. Its joint choice first fixes geometric tolerance and flight design, then reduces calibration and histogram errors. [S8]

This inspected interface is consistent with its stated quantitative assumptions. It is not calibration from transverse histograms alone: the pilot retains planar endpoint positions, an exact clock and preparation outcomes. Nor does it automatically extend to arbitrary vanishing recording efficiencies. Multiplying both efficiencies by a small constant leaves a conditional law unchanged while suppressing accepted mass quadratically. The manuscript explicitly states this distinction. It is a legitimate restriction, not a newly discovered hidden contradiction. This audit does not certify every underlying pilot or quantized-continuation theorem used by the module. [S1, S5, S8]

## 6. Publication-level assessment

**E1 — The principal relative/smooth inverse is serious, but its supplied observations must be counted honestly.** The strongest contribution is the nonlinear relative boundary law followed by actual-smooth signed inversion, with analytic image recovery and finite incidence matching. It should not be dismissed as elementary odds-ratio algebra. Nevertheless, the global theorem is supplied selected obstacle and deck marks, signed physical transverse conventions, gaps, known offsets and exact function-valued laws. The $N+1$ channel count is not a count of scalar measurements or successful preparations. The model-local scalar-coordinate result does not change that fact. The window theorem must retain both critical lines. These are meaningful rigidity statements under structured observations, not recovery from an arbitrary short unmarked record. [S1]

In my judgment, the demonstrated conceptual and informational reach does not yet make a sufficiently compelling case for exceptional placement in the requested general-journal tier. This is a judgment about the result actually proved, not a claim that structured data make it trivial, that it is already known, or that every editor must weigh it identically. I do not impose an unmarked inverse problem as a new mandatory target.

**E2 — Revision 54 resolves a concrete interpretation but does not supply a second geometric breakthrough.** Its Hellinger improvement is useful, and its stopped experiment is now correctly charged with a sharp limiting capped risk. Once the positive density floor and the two acceptance probabilities have been supplied, the improvements use standard distance inequalities, independent-product identities, a monotone likelihood ratio and a shared atom. The specified alternative-dependent profiles arrange the weak mark contrast. The count-only reduction shows that the new stopped discrimination does not require extracting the action-sensitive terminal mark. This is a coherent consequence of the central construction, not a uniform unknown-profile estimation theory. Correctness and usefulness should be credited without inflating that reach. [S2; Section 4 above]

**E3 — A common forward measure does not make all the observation models equivalent.** The unnormalized boundary measure genuinely connects the parts. The current introduction also correctly distinguishes exact law-valued rigidity, interior smooth inversion, finite-dimensional exact coordinates, two-point testing, and acquisition with a richer calibration sensor. The remaining reservation is not a missing disclaimer or an arbitrary page limit. It is whether the collection establishes a general consequence commensurate with the requested placement. I remain unpersuaded by the present article-level case. The number of preserved theorem blocks and the completeness of the build do not decide that question. [S1, S8]

The targeted primary-record check does not establish that the main result is prior work. Osius's association framework explains why cancellation of separate marginal factors is inherited algebra, not a new general association principle. Finamore–Leguil use enriched marked length data for finite-horizon Sinai billiards; De Simoi–Kaloshin–Leguil use marked lengths for analytic open billiards under symmetry and other conditions. These observations differ from the present boundary laws, and no reduction between them is proved here. The official fifth-version record for Florio–Leguil explicitly withdraws an earlier geometric assertion while retaining dynamical results; the manuscript does not rely on the removed assertion. These are scope checks, not an exhaustive priority search or a rereview of those external proofs. [L1–L4]

## 7. Reproduction, limits and final disposition

The official workflow artifact was downloaded through the authorized GitHub connector. Its 4,661,563 bytes hash to the digest returned by the workflow-artifact metadata. The independent verifier checks all **626 frozen source files**, reconstructs the recorded Git subtree, checks **111 active inputs** across the two entries and all **34 build-evidence files**, and verifies the four archived originals. Against the archived active manifest, 107 inputs are unchanged in place. No author checker was rerun for this memorandum, and the author's statement/proof-block counts are not represented as a new independent block audit. [D1, D2]

Both complete entries were rebuilt, companion first, with shell escape disabled. All **281 main and seven companion pages** agree with the native products in extracted text and in same-renderer 72-dpi RGB arrays. Native and rebuilt PDF byte hashes differ: byte-identical PDF reproduction is not claimed. Final-log scans find four retained underfull vertical boxes in the main, no overfull box, unresolved reference/citation or missing-glyph diagnostic in the scanned categories, and no corresponding warning in the companion. Direct visual inspection for this memorandum was limited to main pages **107, 109 and 110**, at 108 dpi. No clipping or formula overlap was found on those pages. Automated all-page comparison is not all-page visual inspection. [D2]

The reviewer-written finite checker imports no author code and produces byte-identical output under ordinary Python and `python -O`. Its exact rational laws, density-floor controls, tensorization, cap-regime tests and negative controls are corroborating diagnostics. They are not a numerical proof of the infinite-flight billiard construction and cannot replace the analytical arguments above. [D2]

**Final disposition:** the v53 technical improvements are correctly implemented; the new deterministic-cap theorem and strengthened transfer corollary require no mandatory correction identified in this audit. Previously closed issues remain closed. I nevertheless **do not recommend acceptance at the requested highest general mathematics journal level**, for the specific contribution and synthesis reasons in Section 6. This recommendation is neither a universal mathematical certificate nor a demand to weaken correct results, delete historical proofs, or append another narrowly tailored theorem.

## References and source keys

Exact source paths, line coverage and Git blob identities for S1–S8 are in `AUDIT_AND_REPRODUCTION.md`; all S-keys refer to mathematical source `2cedae961195f97df802aaa81112d95cd32974e1`.

- **R1:** v53 referee report, `reviews/a2-v53-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, at `000ce24f65f8381d2180cbd1f080d3d8470c8157`.
- **R2:** `RESPONSE_TO_REFEREE_V54.md` and `HISTORICAL_DERIVATION_AUDIT_V54.md` in the manuscript directory; final `REVIEW_READY_V54.md` and root README at the pinned review-ready commit.
- **R3:** earlier v54 memorandum, `reviews/a2-v54-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md`, at `1030ca91a96ca1be8ecd0347ecbdac7084cdd8d4`; opening disposition and Section 5 consulted after the independent local checks and destination-branch discovery.
- **D1:** frozen native delivery for source `2cedae961195f97df802aaa81112d95cd32974e1`; workflow 34934158178, attempt 1, artifact 10382712647, plus the pinned review-ready ledger.
- **D2:** `verify_delivery.py`, `independent_checks.py`, `independent_checks.json`, and `reproduction.json` deposited with this memorandum. Their distinct verification scopes are specified in the audit ledger.
- **L1:** G. Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37 (2009), 459–489; DOI `10.1214/07-AOS572`; primary record `arXiv:0903.0702v1`.
- **L2:** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, `arXiv:2510.18983v1`; Theorem A, printed p. 5, checked in the primary PDF.
- **L3:** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, `arXiv:1905.00890v4`; DOI `10.1007/s00222-023-01191-8`.
- **L4:** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, `arXiv:2010.04120v5`; official version comments checked for the removed geometric assertion.
