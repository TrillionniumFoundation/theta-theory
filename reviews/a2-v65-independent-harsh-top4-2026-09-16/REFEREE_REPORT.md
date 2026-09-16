# Independent referee report on A2, revision 65

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 16, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted external-referee-style assessment, not a commissioned journal report, an editorial decision, or a formal proof certificate. Correctness, originality, exceptional significance, and reproducibility are assessed separately. Author responses and numerical checks are not substitutes for mathematical proofs.

## 1. Recommendation and frozen submission

**Recommendation: do not accept at the requested highest general-journal level on the present exceptional-significance case. No new fatal error or mandatory core proof repair is established within the coverage of this report.** The new marked periodic contact inverse is a real inverse theorem, not merely a relabeling of the v64 forward result. The nine statements in Section 9 withstand the examination below, including the variable-curvature block and the complete analytic function-space inverse.

The earlier unqualified objection that general periodic itineraries have only a forward theorem must therefore be retired. The important qualification is different: the new inverse fixes the collision polygon, its signed frames and phase labels, and uses two positive-offset laws at every phase. It does not transfer the weaker-data alternating experiment's unknown-lattice or charged preparation conclusions to this new observation model. The author states that distinction correctly. The adverse placement recommendation is reassessed on this stronger, but differently marked, result. [S1–S3]

| Object | Immutable identity |
|---|---|
| Actual compiled mathematical source | `06a197e4d11bc3d4193e9f0b7904105df35875fa` |
| Reconstructed manuscript subtree | `469aba06035399f96f07417b172653228df36114` |
| Source branch | `revision/a2-v65-referee-response-2026-09-16` |
| Native-products branch | `revision/a2-v65-native-products-35059519641-1` |
| Products head used as review parent | `5425d9846069a0d23d454d20fe19ed0586d39270` |
| Manuscript directory | `papers/A2-v17-boundary-information-coarsening/` |
| Native workflow / attempt / artifact | `35059519641` / `1` / `10432052220` |
| Preceding v64 report | `838e62dd0435f350ca9f398df09374e189a6e44c` |
| Source reviewed in that report | `ee2380ceb76808dd2969d6b5faaa180737020eff` |

At the branch-discovery snapshot, the source and completed native-products branches were present; a separately named v65 review-ready branch was not listed. The source-to-products comparison contains two delivery commits and no changed mathematical input. The principal article has **143 pages**, the full technical manuscript **319 pages**, and the companion **seven pages**. Page references below are to the principal article. The new proof module's Git blob, fetched directly at the compiled commit, is `fb311379b077bfbbe88e862b7f5818136d3e59b8`, matching the archive. [D1]

### Coverage

The complete 708-line new module, `article/10b_periodic_contact_inverse_v65.tex`, was read, including all nine statements and proofs. The shared introductory theorem, abstracts, response, cover letter, historical derivation audit, dependency ledger, and literature note were checked for consistency. The audit also follows the graph-coordinate interface through the retained periodic Jacobi, relative determinant, and physical-law construction, and reads the contracted-evaluation criterion and real-to-disc lemma used by the new analytic conclusions. [S1–S5, R2]

This is **not** a fresh line-by-line proof audit of all 469 pages. The complete earlier finite-chain/full-phase prerequisites, every inherited alternating inverse, global matching/lattice and moving-family proof, the full calibration/statistical catalogue, and the companion are not freshly certified in their entirety. Byte identity of the old periodic, finite-experiment, and position-pilot modules is separately verified; identity is retention evidence, not a new proof of their contents. All-page mechanical reproduction has a different scope from mathematical review.

## 2. Disposition of the preceding report

| Previous point | Current disposition |
|---|---|
| R64-D2: broader periodic forward law but alternating-only inverse | Substantively changed. There is now a local marked periodic inverse, with its own additional data. |
| R64-M1/M6: signed scaling and physical endpoint momenta | Retained and correctly transported to graph-coordinate sensors. |
| Odd-period orientation and chronological reference normalization | The old forward module is unchanged; the new inverse preserves signs on the physical contact cycle. |
| Full analytic inverse cannot follow from diagonal bounds alone | The new proof supplies a Banach-holomorphic action and an actual low-degree/tail inverse. |
| Corrected all-history pilot cap and prior scope qualifications | Remain closed. The full old finite-experiment and pilot modules are unchanged. |
| Exceptional significance | Reassessed in Section 6; not automatically settled either by the extension or by previous negative reports. |

The v64 report did not require an arbitrary-itinerary inverse as a correctness repair. Revision 65 should be credited as an extension, not described as repairing a theorem previously shown false. Conversely, the existence of that extension does not prove the new observation model equivalent to the old one. [R1–R2, D1]

## 3. The new geometry and law-to-action map

### R65-M1. The graph sensor does not already measure the unknown graph

Lemma 9.1, p. 35, uses

$$R_i(x)=q_i+\nu_i^{-1}(t_i x-n_iF_i(x)),\qquad F_i(0)=F_i'(0)=0.$$

Because $t_i\cdot n_i=0$, the observed scaled tangent projection is exactly $x$, whereas the unknown normal projection is $-F_i(x)/\nu_i$. Thus the sensor coordinate is not circularly defined by an unknown arclength conversion or by the graph height it is meant to reconstruct. The marks do provide substantial first-order geometry: contact locations, tangent/normal choices, flight directions and lengths, incidence cosines, and the closing translation. Curvatures are not among those marks. [S1, lines 14–48]

Direct chord differentiation gives the stated same-end entries $k_i+c_i$ and $k_i+c_{i+1}$, with $c_i=F_i''(0)$ and physical curvature $\kappa_i=\nu_i c_i$. The mixed entry has magnitude $k_i$ and its geometric sign is retained. After diagonal sign conjugation, the interior operator has mass $2c_i>0$.

The strict one-step contraction is justified, rather than inferred from a period multiplier alone. A positive decaying Dirichlet solution satisfies

$$z_{j+1}=k_{b+j}(y_{j+1}-y_j)=-\sum_{h\ge j+1}2c_{b+h}y_h<0.$$

Therefore $0<y_{j+1}<y_j$. Tail uniqueness identifies the ratio with the phase-dependent $a_i$, and compactness supplies a uniform upper bound strictly below one. Returning to the physical charts gives $\sigma_i=\epsilon_i a_i$. A negative signed step is not a failure of contraction. The physical cycle has $r$ germs even if the oriented forward construction uses $2r$ steps. [S1, lines 49–127]

### R65-M2. The nonlinear coordinate change includes its necessary gauge correction

The scaled arclength corresponding to the graph coordinate is

$$\phi_b(x)=\int_0^x\sqrt{1+F_b'(s)^2}\,ds=x+O(x^3).$$

The graph future action is $S^-_{\rm arc}\circ\phi_b+p_b(x-\phi_b(x))$, not merely $S^-_{\rm arc}\circ\phi_b$. The past correction has the opposite sign. Consequently $S^-_{\rm graph}-p_bx$ and $S^+_{\rm graph}+p_bx$ are the physical arclength actions composed with $\phi_b$. The physical clock is unchanged. The endpoint twist acquires $\phi_b'(u)\phi_b'(v)$; its reference value is unchanged because $\phi_b'(0)=1$. [S1, lines 128–146]

This matters at cubic and higher orders. Omitting the correction would generally introduce an incorrect nonlinear action before applying the otherwise correct inverse. The source does not omit it. The graph-coordinate law is derived for each candidate geometry; the inverse does not need the unknown conversion as observed input.

### R65-M3. Two offsets separate unequal actions under the actual shared-amplitude model

Proposition 9.2, pp. 36–37, starts from

$$f_d(u,v)=Z_d^{-1}B^-(u)B^+(v)\{d-A(u)-C(v)\}.$$

For $h=A(u)+C(v)$ its quotient gives

$$Q=\frac{1-h/d_1}{1-h/d_2},\qquad
h=\frac{d_1d_2(1-Q)}{d_2-d_1Q},\qquad
d_2-d_1Q=\frac{d_2(d_2-d_1)}{d_2-h}>0.$$

The normalizers need not coincide. Axis restriction and anchoring recover the individual actions, and another axis ratio recovers the normalized amplitudes. No square root at a degenerate critical point is used. Fixed-order stability follows by bounded slicing, products and reciprocals with the printed denominator floors. The formula is also defined near the realizable density image; it does not require a noisy density itself to satisfy exact separation. [S1, lines 148–206]

There is a precise observation boundary here. Cancellation uses the same amplitude factors at both offsets. It is not cancellation of arbitrary offset-dependent recording distortions. For example, replacing only the second-offset density by its renormalized product with $1+u/20$ changes $Q$ to $Q/(1+u/20)$ and generally changes the reconstructed $h$. This is a control outside the printed hypotheses, not a counterexample to Proposition 9.2. The manuscript does not claim to calibrate such distortions. The distinction should remain in any short description of the new result. [D2]

## 4. The all-order and complete analytic inverse

### R65-M4. The smooth envelope counts visits correctly and establishes finite-jet factorization

Lemma 9.3, p. 37, differentiates actual Euclidean chords. A graph variation changes position by $-n_i\eta_i/\nu_i$, so each flight contributes its outgoing normal projection at the left endpoint and minus its incoming projection at the right endpoint. After summing, the initial contact appears once and each internal contact twice. This yields

$$(D\mathcal S(F)\eta)_b(u)=\alpha_b(u)\eta_b(u)
 +\sum_{j\ge1}v_{b,j}(u)\eta_{b+j}(x_{b,j}(u)),$$

with $\alpha_b(0)=1$ and $v_{b,j}(0)=2$. The marked gauges have zero shape variation. The terminal orbit term is retained in a finite sum and removed only after both factors have their required exponential estimates. [S1, lines 208–267]

For two actual smooth profiles with matching jets through $M$, local interpolation and the envelope bound give an action difference $O(|u|^{M+1})$. This supplies smooth-jet factorization before formal coefficient inversion. Interpolation need not extend to a global family of analytic obstacles for this local smooth statement. Equality of all smooth jets is not confused with equality of smooth germs.

Independent finite stationary-chain tests on equilateral and scalene contact geometries, with unequal curvatures and nonzero cubic terms, verify the shape derivative and detect deliberately doubling the initial visit. They are finite tests of this identity, not a proof of the infinite sum or all differentiated estimates. [D2]

### R65-M5. The cyclic blocks include curvature, and their signs are essential

Theorem 9.4, p. 38, has a genuine nonlinear degree-two map. For a fresh variation $\eta_i=z_ix^n/n!$, the first nonzero coefficient of the envelope is

$$z+2\sum_{j\ge1}T_n^jz=(I+T_n)(I-T_n)^{-1}z,
\qquad (T_nz)_i=\sigma_i^nz_{i+1}.$$

For $n=2$ this computes the derivative of the curvature map; it does not make that map affine. For $n\ge3$, the orbit linearization and constant visit weights depend only on the quadratic jets. Together with actual smooth factorization this proves the affine recursion in the new degree. [S1, lines 269–346]

Since $\|T_n\|_\infty\le a_*^n<1$, both $I-T_n$ and $I+T_n$ are invertible. The row-sum bounds follow from their convergent geometric series. The determinant is

$$\det\mathcal C_n=\frac{1-(-1)^r\Lambda^n}{1-\Lambda^n}>0.$$

It equals one for even $r$, but need not for odd $r$. As an algebraic sign control, three steps $\sigma_i=-1/2$ at degree three give determinant $511/513$, whereas replacing all signs by positive ones gives $513/511$. These are checks on the formula, not assertions that an arbitrary rational configuration is globally realized. Orientation doubling is not permission to discard odd contact information. [D2]

There is an independent check of the particularly important curvature derivative. With $c_i=F_i''(0)$ and $s_i=(S_i^-)''(0)$, elimination of the linear future tail gives

$$a_i=\frac{k_i}{k_i+k_{i+1}+2c_{i+1}-k_{i+1}a_{i+1}},
\qquad s_i=k_i+c_i-k_i a_i.$$

Differentiating these equations at fixed $k_i$ yields

$$\dot s_i=\dot c_i+a_i^2(\dot c_{i+1}+\dot s_{i+1}),
\qquad (I-T_2)\dot s=(I+T_2)\dot c.$$

Thus the same $\mathcal C_2$ follows from the Riccati relation, independently of the homogeneous envelope calculation. This confirms that curvature has not been supplied as hidden data. It proves no global uniqueness of the nonlinear curvature map, and the manuscript claims only local inversion.

### R65-M6. Variable curvature is handled in the function-space construction

Lemma 9.5, pp. 39–40, works in $F^*+X_{R,2}$, not the fixed-quadratic space used by the earlier two-contact lemma. This change matters. For $\|\eta\|_R<\delta R^2$, factorization $\eta=z^2v$ and inner-disc Cauchy estimates control the first two derivatives where they occur. The changed quadratic coefficients contribute $O(\delta R)$ to the residual and $O(\delta)$ to its Lipschitz constant. The source explicitly retains those terms rather than treating the entire perturbation as cubic. [S1, lines 348–454]

The initial endpoint is uncontracted, but its graph enters an interior stationarity equation through its value, not through differentiation there. Differentiated graph arguments are strictly internal. The weighted fixed-point ball and Schwarz estimate give

$$|x_{b,j}(u)|\le\{a_*^j+C_0(\delta+R)\beta^j\}|u|\le\rho^j|u|.$$

The last inequality follows uniformly in $j$ after shrinking $\delta,R$, since $a_*<\beta<\rho<1$. It verifies the protected domains used by the fixed-point map. Holomorphic dependence is Banach-valued and follows from uniformly convergent holomorphic iterates and summable gauged action terms. Pointwise analyticity alone would not establish this assertion, but is not the argument used.

The same-norm derivative identity follows by estimating the terminal term with the Banach-parameter Cauchy bound. Nearby real graphs remain physical on a smaller real collar. This does not assert that every member of the complex function-space neighborhood continues to a closed periodic obstacle. I find no unresolved boundary differentiation-loss problem in this construction.

### R65-M7. The full inverse is not inferred from its diagonal

Theorem 9.6, pp. 40–41, writes $L=A+K$ with an invertible initial multiplier. Every vanishing tail is invariant, and

$$\|K|_{X_{R,m}}\|\le\frac{W\rho^m}{1-\rho^m}.$$

Choose one finite $m$ making $a^{-1}W\rho^m/(1-\rho^m)<1$. A norm-convergent Neumann series then inverts the restriction to that tail. The finite quotient of degrees $2,\ldots,m-1$ has invertible diagonal blocks $\mathcal C_n$; its lower part need not be small. Solving the quotient first leaves a residual in the tail, where the already constructed inverse applies. No uncontrolled nilpotent sum grows with the requested jet order. [S1, lines 456–539; S5]

Holomorphic inverse-function reasoning, supplied by a contraction argument, gives the nonlinear inverse. The two-point lower bound uses closeness to one invertible base derivative on a convex neighborhood, not merely pointwise nonsingularity. Invariance under the inverse follows from finite triangular induction, justifying the order-independent finite-jet quotient bounds. Cauchy's inequality gives the factorially weighted coefficient estimate on each smaller disc. These are induced analytic quotient norms, not uniform bounds on unweighted derivatives.

This is an actual infinite-dimensional local coordinate theorem for contact germs. It includes curvature and all lower-degree couplings. It is stronger than a list of individually invertible jets, though its operator-theoretic mechanism is the retained contracted-evaluation criterion after the new geometric verification.

## 5. Physical consequences, realization, and comparison with other data

### R65-G1. The finite-flight and real-noise consequences use the correct order of operations

Corollary 9.7, p. 41, first compares the finite bridge densities to their realizable limiting laws. The rational extraction is stable on the positive square. For a noisy gauged action, removal of its constant and linear Taylor terms is a bounded projection that fixes the true anchored action. Only then does the local curvature/finite-jet inverse apply. This gives $C_M(\tau^N+\epsilon)$ for a fixed $M$; it does not assert exact limiting factorization for a finite bridge. [S1, lines 541–590]

Theorem 9.8, pp. 41–42, fixes the larger analytic neighborhood and smaller-disc inverse neighborhood before looking at the data error. Restriction is bounded; the action constructions agree on restriction by uniqueness on the common real collar and analytic continuation. The real-to-disc lemma applies to action differences with a uniform outer bound. Composing it with the inner-disc inverse gives $C\epsilon^\theta$, or $C(\epsilon+\tau^N)^\theta$ in the stated finite-flight comparison. The marks make the momenta identical in this comparison. [S1, lines 603–650; S5]

The radius loss and prior are substantive. A monomial $\eta_N(z)=\varepsilon(z/R)^N$ can retain its outer-disc norm while becoming arbitrarily small on a smaller real interval, but it also becomes small on the smaller output disc. It is not a counterexample to this conditional theorem. A finite-flight density estimate is not a confidence bound from finitely many preparations, and no such new general-period budget is claimed.

### R65-G2. Exact whole-table identity is conditional on supplied placement and coverage

For actual connected closed embedded analytic obstacle boundaries, an open common arc continues to the entire image by the one-variable identity theorem in local tangent charts. Every labelled obstacle must be visited, and the lattice is fixed. Under those printed conditions the contact inverse implies equality of all obstacle images, not merely congruence of unregistered local arcs. [S1, lines 592–600]

The same statement must not be summarized as unmarked whole-table reconstruction or as recovery of the unknown lattice by this new theorem. Those tasks are distinct inherited results with different hypotheses. Nor does local inversion prove a global inverse branch for arbitrary separated candidate germs. These qualifications are explicit, and should not be turned into invented contradictions.

### R65-G3. The nonnormal realization has independently varying curvatures

Proposition 9.9, pp. 42–43, perturbs actual closed obstacles, not just scalar recurrence coefficients. For

$$R_i(\vartheta)=1+\delta_i(1-\cos\vartheta)(1+\eta_i\sin\vartheta),$$

one has $R_i(0)=1$, $R_i'(0)=0$, $R_i''(0)=\delta_i$. Hence the contact point and tangent remain fixed, while the polar curvature formula gives $\kappa_i(0)=1-\delta_i$. The three curvature derivatives are independent. Strict convexity and the previously realized disjointness/clearance margins persist under sufficiently small perturbations. [S1, lines 652–695; S4]

For an explicit convexity cross-check, if $|\delta|\le d$, $|\eta|\le e$, set $D=2d(1+e)$. Then $|R-1|\le D$ and $|R''|\le d(1+5e)$, so

$$R^2+2(R')^2-RR''\ge(1-D)^2-(1+D)d(1+5e).$$

The independent rational controls give positive floors for three small parameter boxes. This supplements, but is not needed to repair, the source's continuity argument. Six oriented steps still represent only three physical unknown germs. [D2]

### R65-L1. The literature comparison is about different observations

Bolotin–Treschev's discrete Hill formula and odd-period orientation discussion provide established determinant/monodromy context. Their cyclic action Hessian is not the Dirichlet corner cofactor used before conditioning here, and neither formula alone supplies the contact shape derivative. Theorem 2.1 and the adjacent discussion on printed p. 12 were checked in the primary PDF, including a screenshot. [L1]

Bálint–De Simoi–Kaloshin–Leguil's Theorem D and Corollary E concern general-word length asymptotics and marked Lyapunov recovery in their non-eclipsing open-billiard setting. Their following Remark 2.3 discusses difficulty separating individual higher-period contact parameters from those asymptotics. The present supplied polygon plus phase-resolved function laws is a different source of information: it provides individual action responses rather than only those scalar length asymptotics. This is useful context for the new inverse, not evidence that it solves their marked-length problem. The relevant primary text was read; a screenshot request failed and is not claimed successful. [L2]

The primary record of De Simoi–Kaloshin–Leguil retains its analytic open-billiard symmetry/genericity assumptions. Finamore–Leguil uses an enriched marked-length datum. Florio–Leguil's version-5 notice removes the affected earlier geometric spectral-rigidity assertion while retaining dynamical conclusions. None supplies a demonstrated reduction to this observation model. These are targeted statement/record checks, not complete audits of those papers or an exhaustive priority search. No redundancy or first-priority claim is established. [L3–L5]

## 6. Exceptional significance and article-level judgment

### R65-E1. The stronger inverse changes the assessment, but not my recommendation

The new result answers a real mathematical question left open by the preceding formulation: how the distinct actions of a general periodic orbit identify the contact geometry. The signed cyclic response is a clean explanation, and the variable-curvature analytic inverse is not an automatic consequence of the v64 forward theorem. The combined relative physical law and actual contact response is the strongest current contribution. It should not be dismissed as a density-ratio identity alone.

Nevertheless, I remain unconvinced by the requested exceptional general-journal placement. In the new theorem, substantial orbit geometry is fixed before inversion: locations, tangent frames, flights and incidences. There is an independent function-valued law at every phase and at two offsets. After action extraction, the positive-mass scalar recurrence makes each step strictly contracting; the boundary derivative has an invertible initial multiplier and exponentially contracted later evaluations. The cyclic algebra then makes every graded block nonresonant, and the retained analytic criterion handles the full inverse. This is a coherent and useful local rigidity mechanism, but the new theorem has not demonstrated the same reconstruction from the weaker geometric data of the original channel experiment.

That data distinction does not invalidate the result. It does limit what importance can be inferred simply from saying the inverse now holds for general periods. Likewise exact global continuation with every obstacle visited is a real conclusion, but after anchored contact images and a fixed lattice are known it is not a second independent global geometric reconstruction mechanism. The smaller-disc real estimate adds useful stability, not an unconditional or general-period acquisition theorem.

My concern is thus not a count of assumptions, the presence of function-valued data, or the use of standard tools in isolation. Important inverse problems often have all three. It is whether this particular combination establishes enough depth and influence beyond its calibrated local setup to justify the requested placement. The manuscript makes a stronger case than v64, and its core appears mathematically coherent within the audit, but I do not judge that case sufficient. Another specialist may value the combined relative/contact mechanism more highly; neither this targeted search nor my judgment establishes that it lacks novelty.

### R65-E2. Do not turn an editorial reservation into another artificial technical defect

There is no newly demonstrated mandatory core repair to close here. I am not imposing unmarked reconstruction, grazing limits, unbounded-period uniformity, a general-period preparation rate, global curvature-map injectivity, or marked-length rigidity as corrections to the printed theorems. They are different possible research directions, not missing hypotheses discovered in this report.

The present manuscript should also not rely on growth of its theorem list to carry the significance argument. The principal abstract and introduction now traverse several observation models: general marked polygons, weaker-data alternating channels, unregistered global channel images, and charged statistical experiments. The distinctions are mostly explicit. The editorial task is to foreground the decisive relative/contact mechanism and the exact relations between those models, rather than allow the catalogue to suggest one theorem simultaneously enjoys all their strongest properties. This is an emphasis and synthesis issue, not a request for arbitrary deletion of proofs or another detached abstraction section.

The two-site specialization and the new signed cycle calculation are enough to explain the local algebraic relation. A further referee should evaluate why that geometric mechanism is exceptional, not repeatedly resurrect closed objections or ask for a new lemma merely because earlier recommendations were adverse.

## 7. Disposition codes

**R65-D1 — Mathematical status:** the nine new statements withstand this scoped examination. No fatal counterexample or mandatory new core proof repair is established. This is not certification of every inherited theorem.

**R65-D2 — Updated scope:** retire the unqualified claim that general-period results are forward only. Credit the marked periodic contact inverse, including unknown curvature and the complete analytic function-space conclusion.

**R65-D3 — Observation distinctions:** retain the fixed polygon and signed phase coordinates, common two-offset amplitudes, local inverse branch, analytic prior and radius loss, fixed-lattice/all-obstacles-visited global clause, and separation from acquisition. These are correctly stated restrictions, not outstanding hidden errors.

**R65-D4 — Placement:** do not accept at the requested level on the current exceptional-significance case. Do not present this recommendation as a remaining sign error, an established prior theorem, or an instruction for another nominal repair-only cycle.

## 8. Independent reproduction and limits

The downloaded artifact SHA-256 is `8aa528bb293e31daecb88522210f2f8418779d2a3ac11536041b308b13a983d3`. Independent checks verify lengths, SHA-256 values and Git blob identities for **818 frozen files**, reconstruct the manuscript subtree, check **131 distinct active inputs**, and verify **45 native build-report evidence entries**. The per-entry active counts are 120 full, 52 principal and one companion. Baseline comparison verifies all 800 inherited paths: 793 unchanged, seven modified with byte-exact originals archived. All 129 inherited active paths remain. [D1]

Fresh builds with shell escape disabled and regenerated auxiliaries succeeded for all three entries. All **469 pages** match the native PDFs in extracted text and same-renderer **72-dpi RGB arrays**. PDF bytes differ. The full log has four underfull notices, the principal and companion none; no undefined-reference/citation, missing-character, overfull-box or LaTeX-error pattern was found in the checked final logs. Actual visual inspection covered principal pp. **36, 38, 40 and 42** at **108 dpi**. No clipping or unreadable formula was observed on those pages. Mechanical parity is not all-page visual inspection. [D1]

The independent mathematical program imports no author checker. It checks **240 exact signed cyclic blocks**, **six exact Riccati curvature Jacobians**, **15 odd-cycle sign-erasure controls**, **294 exact normalized density identities**, **42 axis-amplitude recoveries**, **252 offset-dependent-efficiency controls**, **72 actual finite geometric stationary configurations**, and the polar curvature/convexity formulas. The largest finite envelope relative discrepancy is below $10^{-7}$; the two numerical geometric curvature Jacobians agree to below $1.6\times10^{-11}$ in maximum-entry error. These are numerical finite controls, not rigorous bounds on an infinite orbit. [D2]

Normal and optimized runs emit identical JSON. The author's preservation/mathematical checker was not rerun. The frozen-source verifier is reused from the preceding independent review, and the baseline comparator is adapted to v64. No finite test proves Banach holomorphy, arbitrary-order differentiation, trace-class convergence, global analytic continuation, or exceptional significance.

## Source keys

All S-keys refer to compiled source `06a197e4d11bc3d4193e9f0b7904105df35875fa`, under `papers/A2-v17-boundary-information-coarsening/`.

- **S1:** `article/10b_periodic_contact_inverse_v65.tex`, lines 1–708; principal Section 9, pp. 34–43. Line ranges in the discussion identify the relevant obligations.
- **S2:** `article/00f_periodic_contact_overview_v65.tex`; principal Theorem 1.1, p. 4, and its proof map.
- **S3:** `rigidity.tex`; `journal/00_principal_introduction_v61.tex`; `article/00e_periodic_mechanism_overview_v64.tex`; current statement hierarchy and observation comparisons.
- **S4:** `article/10a_periodic_itinerary_relative_v64.tex`, lines 1–549; graph-transfer inputs, relative normalization, physical residual and three-obstacle realization. Earlier finite-chain/full-phase prerequisites are not wholly recertified.
- **S5:** `article/23a3_conditional_observation_inverse_v60.tex`, contracted-evaluation criterion and real-to-disc lemma, lines 1–150; `journal/DEPENDENCY_LEDGER_V65.md`.
- **R1:** [Preceding v64 report](https://github.com/TrillionniumFoundation/theta-theory/blob/838e62dd0435f350ca9f398df09374e189a6e44c/reviews/a2-v64-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md).
- **R2:** `RESPONSE_TO_REFEREE_V65.md`, `HISTORICAL_DERIVATION_AUDIT_V65.md`, `COVER_LETTER_V65.md`, `LITERATURE_CHECK_V65.md`; provenance and author claims, not proof substitutes.
- **D1:** `AUDIT_LEDGER.md`, `AUDIT_RESULTS.json`, `verify_delivery.py`, `compare_baseline.py` in this review directory; native artifacts 10432052220 and 10429927974, and the GitHub source-to-products comparison.
- **D2:** `independent_checks.py`; complete emitted records and fresh-build logs accompany the independent audit archive.
- **L1:** Sergey Bolotin and Dmitry Treschev, *Hill's formula*, [arXiv:1006.1532](https://arxiv.org/abs/1006.1532), Theorem 2.1 and orientation discussion, printed p. 12; Russian Mathematical Surveys 65 (2010), 191–257, DOI 10.1070/RM2010v065n02ABEH004671.
- **L2:** Peter Balint, Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, [arXiv:1809.08947v3](https://arxiv.org/abs/1809.08947v3), Theorem D, Corollary E and Remark 2.3, printed pp. 9–10; DOI 10.1007/s00220-019-03448-x.
- **L3:** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890](https://arxiv.org/abs/1905.00890), primary abstract; DOI 10.1007/s00222-023-01191-8.
- **L4:** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983](https://arxiv.org/abs/2510.18983), primary abstract/version record.
- **L5:** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), primary abstract and explicit correction notice.
