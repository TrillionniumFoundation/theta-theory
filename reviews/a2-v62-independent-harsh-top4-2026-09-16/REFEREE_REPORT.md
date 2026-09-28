# Independent referee report on A2, revision 62

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 16, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted referee-style assessment. It is not commissioned by any journal, is not an editorial decision, and is not a formal proof certificate. Mathematical correctness, reproducibility, originality, and exceptional significance are assessed separately. The author's response and verification records are claims to check, not substitutes for the proofs.

## 1. Recommendation and frozen submission

**Recommendation: decline at the requested highest general-journal level on the present case for exceptional mathematical significance.** Revision 62 makes a real mathematical advance over the previously reviewed formulation: it gives finite-preparation confidence bounds for complete local analytic contact germs, including a separate calibration-inclusive bound. An objection that the work has no finite-experiment consequence would now be inaccurate.

**No fatal error in the new statistical rates is established in this review.** Within the coverage below, Lemma 13.5, Theorems 13.6–13.7 and Corollaries 13.8–13.9 have sound arguments, with one minor correction to an auxiliary sentence about the last pilot-grid time, detailed in R62-m1. The correction does not change either exponent, the preparation cap, or the asserted order of the evolution-time bound. It must not be inflated into an alleged failure of the main result. Conversely, the scoped acceptance of these arguments is not certification of the entire 432-page delivery.

| Object | Immutable identity |
|---|---|
| Review-ready branch | `revision/a2-v62-review-ready-2026-09-16` |
| Review-ready head | `fa322c27f9aea6ce1f21b46f41e7e2ce02dcc631` |
| Actual compiled mathematical source | `037c80dc44d8191e6f808591ea0651e813234d06` |
| Reconstructed manuscript subtree | `160735632f3977d47dcf708fb2292699ab79fafd` |
| Source branch | `revision/a2-v62-finite-experiment-2026-09-16` |
| Manuscript directory | `papers/A2-v17-boundary-information-coarsening/` |
| Native workflow / attempt / artifact | `35047150051` / `1` / `10427846002` |
| Addressed v61 report | `9ec2004a18cccc69ed473685bdf94c91f0b25d4d` |
| Actual source reviewed in that report | `71e0bd6306f54466728c2e6e781bb0f422c5cfb0` |

The principal article has **125 pages**, the full technical manuscript **300 pages**, and the companion **seven pages**. Page references are to the principal article unless prefixed by F. The source-to-review-ready GitHub comparison has three delivery commits and no intervening alteration of compiled mathematical inputs. The new proof module was also fetched directly at the compiled commit; its Git blob is `e3ead4bc73e52556490977ad17b4c6868384d03e`, matching the downloaded source. [D1]

### Coverage of this round

The complete new module `article/23f2_finite_experiment_analytic_inverse_v62.tex`, lines 1–463, was read and checked. Its substantive dependencies were followed through the conditional real-observation inverse, the four-density identity, the physical phase integration, the relative determinant/density interface, and the complete printed position-pilot construction and cap. The principal structural statements, new overview, response, cover-letter argument, derivation audit, and dependency declaration were checked for consistency. [S1–S7]

This is **not** a fresh line-by-line proof audit of all 432 pages. The full earlier nonlinear finite-chain construction, the complete v59 Banach-space construction, every global congruence/lattice and moving-family proof, the realized quartic comparison, the remaining adaptive/stopped-experiment catalogue, and the companion's mathematics are not freshly certified here. The v59 analytic inverse is retained as a previously scoped input; the current v60-to-v62 interface is examined directly. In contrast to merely reading a dependency label, this round does read the position-pilot theorem and its proof, including its elementary localization and mass argument, while not claiming to reprove every earlier geometric prerequisite.

## 2. What changed, and what should no longer be objected to

The v61 report established no mandatory new core proof repair. Its mechanism-centered presentation request had been met; its remaining recommendation concerned significance. The present response correctly treats v62 as an extension, not as a repair of a theorem previously shown false. [R1–R2]

| Earlier point | Present disposition |
|---|---|
| Finite flights previously controlled a fixed jet order in a strong real norm | Theorem 13.6 now controls the complete analytic contact pair on an inner disc under the additional analytic prior. |
| Complete-germ conditional stability previously concerned limiting laws | Theorem 13.7 now supplies a finite-record estimator and a charged confidence rate. |
| Calibration costs must not be omitted | Corollaries 13.8–13.9 explicitly include them and give a different, slower total-budget rate. |
| The full inverse is not merely a bounded diagonal | Retained; no diagonal-only substitution appears in the new proof. |
| Real observations do not control the same-disc analytic norm without a prior | Still true, still not claimed, and not an outstanding defect. |
| Global acquisition depends on substantive extra inputs | Retained. The new physical pilot dependency is explicitly declared and its actual cap is used. |
| Exceptional significance | Reassessed on the stronger finite-experiment result below; not automatically inherited from v61. |

The independent frozen-source comparison verifies that all 753 v61 source paths remain, with 750 byte-identical. Only `main.tex`, `rigidity.tex`, and the manuscript `README.md` change among inherited files. All 123 inherited active paths remain active; three new paths give a union of 126. These are byte-level and input-graph findings, not a semantic count of independent theorems. [D1]

## 3. Detailed assessment of the finite-experiment proof

### R62-M1. The finite-density and acceptance estimates use the right normalization

Lemma 13.5, p. 64, begins with the actual finite numerator and its limiting counterpart,

$$F_{j,d'}=b_j(d'-E_j)_+,\qquad F_{\infty,d'}=B_b(u)B_b(v)(d'-S_b(u)-S_b(v))_+.$$

The relative theorem controls both $E_j$ and the normalized twist $b_j$ on one fixed contact box. Positive part is Lipschitz, so it controls the unnormalized densities and their integrals there. A fixed small square and a compact positive-offset interval give a common positive lower bound for the normalizers. Division therefore gives the stated density estimate; it does not divide an absolute approximation error by an exponentially small success probability. On the strictly interior square the cutoff is inactive, and the first endpoint-derivative bounds supply the common Lipschitz constant. Uniform offset continuity needs only positive-part Lipschitz continuity, not an unjustified derivative of a moving boundary. [S1, S4]

The uniformity assumptions are consequential. A common outer holomorphic bound gives the finitely many real derivative bounds on a protected smaller collar. The gap, curvature, separation, clearance, roof and area margins are supplied uniformly. This does not assert uniform control over arbitrary analytic tables or differentiation with respect to every infinite-dimensional geometric parameter.

For even $j$, the exact physical success mass is

$$p_{j,b,d'}^T=\frac{a_b}{2\pi A(T)\sinh(j\gamma(T))}Z_{j,b,d'}.$$

The lower bounds for $a_b,Z_{j,b,d'}$, the upper area bound, and $1/\sinh(j\gamma)\ge2e^{-j\gamma}$ yield $p_j\ge ce^{-\Gamma j}$. This is the normalization arising from the first-impact phase measure, with residual time integrated out. Selected nonminimal channels remain selected itineraries rather than being equated with the entire maximal-count event. [S1, S4]

This interface is sound within the stated uniform geometric class. The underlying two-ended relative determinant estimate remains a substantive ingredient: the sampling lemma does not prove it anew.

### R62-M2. Finite bridges are compared through realizable limiting laws

Theorem 13.6, p. 65, uses the triangle inequality

$$\|f_{b,d}^{T}-f_{b,d}^{\widetilde T}\|_{C^0(Q)}\le e_{j,k}+C(e^{-\omega j}+e^{-\omega k})$$

before invoking the conditional analytic inverse. Neither finite-bridge density is asserted to have the separated limiting form. Consequently the theorem does not apply a rank-one identity to a law for which that identity is false. [S1–S3]

The underlying law identity is still

$$1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}=t(u)t(v),\qquad t=\frac{S}{d-S}.$$

A fixed nonzero anchor controls the scalar square root, and the joint gap/action inverse handles varying leading Hessians without observing curvature separately. The conditional continuation step has an outer analytic bound and a smaller output radius chosen before observing the error. Those hypotheses are inherited, not generated by the data. [S2–S3]

The coefficient consequence is correctly weighted:

$$\sum_{n\ge2}\frac{t^n}{n!}\max_b|\Delta\psi_b^{(n)}(0)|\le\frac{(t/r)^2}{1-t/r}\|\Delta\psi\|_r,\qquad 0<t<r.$$

This controls every coefficient simultaneously in the declared analytic scale. It is not a uniform bound on all unweighted derivatives. Nor does approximation of a complete germ from a finite sample mean exact identification of infinitely many real coefficients from one finite record.

### R62-M3. The random success count is handled without an invalid stopping argument

Theorem 13.7, pp. 65–67, has a fixed number of attempts: $N$ independent full-phase preparations for each starting type. Hence $M_b$ is binomial. Conditional on $M_b=m$, the marks at the successful indices have the actual conditional success law. One can verify this directly by fixing those indices: the product of the success densities and failure probabilities factors, and summing over the index sets gives the same conditional product law. The count does not have to be ancillary, and the proof does not claim that it is. [S1]

This differs from conditioning a stopped experiment on having completed its cap. The latter shortcut would need separate justification; the present fixed-attempt construction does not use it.

The lower-tail estimate at

$$m_0=\tfrac c2Ne^{-\Gamma j}$$

has failure probability at most $2\exp(-cNe^{-\Gamma j}/8)\le\alpha/4$ under the printed condition. For a cell with probability at most $Fh^2$, the conditional Bernstein bound gives

$$\left|\widehat f_{b,i}-h^{-2}\int_{C_i}f_{j,b,d}\right|\le\sqrt{\frac{2Fx}{mh^2}}+\frac{2x}{3mh^2},\qquad x=\log\frac{16(J+1)}\alpha.$$

The bound is uniform in every $m\ge m_0$, so integrating over those counts is legitimate. Union bounding over two types and $J$ cells costs at most $4Je^{-x}\le\alpha/4$. The stated $1-\alpha$ event is conservative, not missing a factor from random sample size. [S1]

The outside category matters to the printed normalization. $M_b$ counts all selected successes, not only endpoints in $Q_+$. Dropping outside successes while retaining the same candidate cell masses would change the fitted target. An exact finite control gives a cell probability $2/7$ before recropping and $2/5$ after conditioning on a window of mass $5/7$. An alternative consistently recropped experiment is not ruled out by this example; it is simply not the experiment proved here. [D2]

### R62-M4. The estimator is measurable, but not a finite computational search algorithm

The countable dense-image construction resolves an important existence issue. A subset of $C(Q_+)^2$ is separable. Choose a countable dense subset of the realizable limiting-density image and a realizing table for each point. For each candidate the finite cell residual is measurable. A positive tolerance $\xi$ and the first-index rule relative to the countable infimum give a measurable approximate selector, including a default on empty success groups. Its contact-pair output is measurable in the inner-disc norm because its range is countable. Compactness of the entire infinite-dimensional parameter set is not needed for this particular construction. [S1]

There is no claim of an attained minimum, and no need to assume one. There is also no proven finite running-time bound for evaluating the countable infimum or finding the selected index. Calling this an existence theorem for a measurable estimator is accurate; calling it a supplied computational reconstruction algorithm would not be.

The fitted candidate and the true table both have realizable limiting laws with the common real Lipschitz bound. Their cell-average differences are controlled by the two residual inequalities and the finite-flight error. Passing from averages to values therefore costs $2\sqrt2Hh$. This is regularity of the two candidate laws, not regularity of an empirical step-function histogram. Only after that comparison does the analytic inverse apply. This ordering is correct.

### R62-M5. The exactly calibrated rate has the stated balance

Ignoring fixed constants, the error before analytic inversion is

$$e^{-\omega j}+h+\sqrt{\frac{x e^{\Gamma j}}{Nh^2}}+\frac{x e^{\Gamma j}}{Nh^2}+\xi.$$

The square-root term balances the first-order spatial bias at $h\asymp(xe^{\Gamma j}/N)^{1/4}$. Writing $a_N=L_N/N$ and $\zeta=\omega/(4\omega+\Gamma)$, the even schedule gives

$$e^{-\omega j_N}\le e^{2\omega}a_N^\zeta,\qquad h_N\asymp a_N^\zeta$$

up to fixed rounding factors; the variance term is $O(a_N^\zeta)$ and the linear concentration term $O(a_N^{2\zeta})$. The bound $J_N\le C(N/L_N)^{2\zeta}$ controls the logarithm, and $Ne^{-\Gamma j_N}/L_N\ge(N/L_N)^{4\zeta}$ supplies the success-count condition for the stated large-budget regime. Thus

$$\Pr\{\|\widehat\psi-\psi\|_r>C(L_N/N)^{\vartheta\omega/(4\omega+\Gamma)}\}\le\alpha$$

has the claimed derivation. The cost is $2N$ attempts, not $N$ accepted samples. The evolution-time charge is also explicitly included. [S1]

The denominator $4\omega+\Gamma$ reflects the particular two-dimensional first-order histogram estimate and exponential thinning. It is an upper-bound construction, not an information lower bound. The superscript in the source label `optimal-schedule` should not be mistaken for a minimax assertion: the printed theorem expressly makes none. No optimality result is needed for the upper bound to be valid.

### R62-M6. The calibration terms and the slower complete-budget rate are substantive

Corollary 13.8, pp. 67–68, correctly amplifies gap error to $\Delta=jv_g+v_t$. A good pilot produces an observable map whose displacement is at most $r_c$; the proof does not assume that its pushforward law has a density or a Jacobian. A category can change only in a boundary tube. For a square of side $h$ and $r_c\le h/2$,

$$|(\partial C)_{r_c}|\le(h+2r_c)^2-(h-2r_c)^2=8hr_c.$$

Thus the cell-average bias is at most $8Fr_c/h$, and the displaced cell probability is at most $5Fh^2$. The modified Bernstein argument follows. The outer edges and the outside category are included, so there is no uncharged spatial recropping term. [S1]

For variable gaps, restricting the countable candidate set to $|g_l-\widehat g|<v_g+\xi$ is also legitimate. The positive slack ensures that the true image can be approximated from within the admissible strip; the selected gap error is at most $2v_g+\xi$. Concentration is applied conditionally on every good pilot history to fresh attempts, then integrated with the pilot failure probability added. The charge is $B_{\rm pil}+2N$ on all histories, not only on completed pilots.

The imported position pilot is full Theorem F.46.2, not a transverse-histogram-only calibration. It uses planar positions in one sensor frame for both types of a channel, a clock, retained channel/type/deck labels, and independent phase-volume preparations. Inter-channel poses are not thereby supplied. Its onset scan needs only a lower success mass at a grid point within $[\varepsilon,2\varepsilon]$ of onset; it does not infer zero probability from a finite run of failures. The scan's first successful position yields $j|\widehat g-g|\le\varepsilon$ and a projection error $O(\sqrt\varepsilon)$. These assertions follow from the printed localization, mass bound and normalization of the contact displacement. [S5]

The actual pilot cap has the dependence

$$B_{\rm pil}\le C(j+1)e^{\Gamma j}\varepsilon^{-3}\log(C/\alpha).$$

There are $O((j+1)/\varepsilon)$ scan points and $O(\varepsilon^{-2}e^{\Gamma j}\log(C/\alpha))$ attempts per point. Choosing $\varepsilon\asymp h^4$ makes $r_c/h=O(h)$ and costs $h^{-12}$, not $h^{-4}$. With $h\asymp e^{-\omega j}$, the total cap is bounded by

$$C(j+1)e^{(12\omega+\Gamma)j}(\log(C/\alpha)+\omega j).$$

Inverting this bound with the even schedule and a squared logarithmic allowance gives the exponent $\vartheta\omega/(12\omega+\Gamma)$ in Corollary 13.9. The stronger exactly calibrated exponent is not being mislabeled as a calibration-inclusive rate. The full pilot theorem and its cap are substantive dependencies, visibly aliased into the principal article; no new hidden use of the larger global acquisition theorem is needed for this local rate. [S1, S5–S6]

### R62-m1. Minor correction: the last pilot-grid time has an extra ceiling allowance

**Location:** new module lines 448–450, principal p. 69, near the end of the proof of Corollary 13.9; compare `article/25a_common_observables_v25.tex`, lines 113–129, equation `eq:v25-pilot-grid`.

The unqualified sentence that every pilot time is at most $jg_++2\varepsilon$ is not literally true for the retained grid. That grid has

$$L=\left\lceil\frac{j(g_+-g_-)}\varepsilon\right\rceil+2,\qquad t_L=jg_-+L\varepsilon.$$

Putting $q=j(g_+-g_-)/\varepsilon$ gives

$$t_L-jg_+=(\lceil q\rceil-q+2)\varepsilon\in[2\varepsilon,3\varepsilon).$$

For example, $j=2$, $g_-=1$, $g_+=3/2$, $\varepsilon=2/101$ give $t_L=308/101$, whereas $jg_++2\varepsilon=307/101$. Analogous fractional grid lengths occur at arbitrarily small resolutions. This is an arithmetic control of the prescribed grid, not a counterexample to a billiard rigidity theorem. [D2]

**Required correction:** replace the universal bound by $t_l<jg_++3\varepsilon$ (or by $t_l\le jg_++3\varepsilon$). Alternatively, qualify the $2\varepsilon$ sentence as a good-history bound on the times actually reached before successful stopping, and separately give the all-history $3\varepsilon$ grid bound. Bad histories can reach the final grid point.

**Effect:** none on the asserted $CB\log(C_0B/\alpha)$ bound, since both bounds are $O(j+1)$; none on the preparation cap, which already uses $L+1$; none on either confidence exponent. This is a minor literal correction, not a mandatory new core theorem or a reason to redo the entire statistical construction.

## 4. Scope checks and the remaining significance question

### R62-S1. What the new finite result genuinely adds

The previous limiting-law datum is no longer simply treated as observed for free. The new theorem has finite records, an increasing finite grid, a logarithmically increasing even flight number, explicit confidence, and every rejected preparation charged. It estimates a complete analytic germ rather than first fixing a maximal jet degree. The calibration-inclusive result goes further than a free-calibration oracle. These are meaningful improvements and must be credited in any subsequent summary. [S1, S7]

Several distinctions remain. The theorem uses independent normalized full-phase preparations, not a mixing or recurrence argument for one orbit. Uniform access to that preparation distribution is part of the declared experiment; the theorem does not construct a sampling apparatus for an unknown phase space or price the computational evaluation of the fitted model. The class has a fixed local analytic prior, protected radii, uniform margins, ideal recording in the new subsection, and retained marked channels. The pilot adds stronger sensor hypotheses rather than solving unmarked discovery.

The target is local contact geometry. The global finite-fiber/lattice theorem and the finite-scalar coordinate theorem on immersed finite-dimensional models remain different conclusions. The new rate does not quantify continuation around an entire obstacle or decide all global matching alternatives. Nor does it give a bound uniform over arbitrarily inefficient recording. These restrictions are explicitly present; they are not newly uncovered omissions. A fixed finite collection of histogram categories is also not claimed to determine every member exactly: the grid refines with the budget.

### R62-E1. Why the placement recommendation remains adverse after crediting that advance

The strongest case for the manuscript is now a coherent mechanism, not merely a catalogue of consequences: a physically normalized long-bridge law retains nonlinear local action data despite the vanishing reference twist; stationary cancellation gives actual-smooth contact inversion; an analytic function-space inverse and a prior-dependent restriction estimate give complete-germ stability; finite observations can exploit it at an explicitly charged rate.

My objection is not that this chain is false, that local periodic-orbit arguments are inherently minor, or that infinite-dimensional observations disqualify a rigidity theorem. The difficult point is the relative/action mechanism itself. It is proved in a protected alternating-channel setting with a uniformly diagonally dominant local variational problem. The two-ended trace-class comparison is carefully organized and substantive. Yet the current submission does not persuade me that the mechanism's demonstrated reach and depth, as opposed to the number of consequences obtained from it, justify the requested exceptional general-journal placement.

Once the relative density approximation and conditional inverse are available, the new statistical route consists of standard thinning/concentration, histogram bias control, a measurable minimum-distance construction, and elementary cost balancing. Its correct composition is useful and not automatic, but the individual statistical steps are not separate breakthroughs. The pilot-inclusive exponent describes a concrete conservative acquisition policy; it is neither a sharp information barrier nor a new general theory of experimental design. Those are not obligations for correctness, but they limit what weight this extension can carry in an exceptional-significance case.

The unknown lattice and unregistered channel poses are genuine outputs in the exact global theorem. They should not be dismissed as supplied geometry. Nevertheless, the new confidence rate is not a corresponding global quantitative advance: the analytic propagation and finite incidence-matching stages retain their earlier, separate scope. Thus v62 strengthens the interpretation and usefulness of the core mechanism, without independently settling the broader placement question.

This is an evaluative referee judgment, not proof of redundancy, lack of novelty, or an impossibility claim. A specialist may value the mechanism more highly. The recommendation is reconsidered on v62, rather than inherited because previous reports were negative. Correcting R62-m1 alone would not change it. I do not impose ordinary marked-length rigidity, unmarked recovery, minimax optimality, or an unrelated stronger inverse problem as a repair condition for the stated theorems.

### R62-E2. A focused primary-literature comparison would be more useful than another abstract framework

The refreshed primary records preserve the previously noted distinctions. Finamore–Leguil's finite-horizon Sinai result uses an enriched marked length datum. De Simoi–Kaloshin–Leguil concerns analytic open billiards under non-eclipse and stated symmetry/genericity hypotheses. No reduction between those data and the present controlled conditional-law observation is established. Osius supplies association-model context, not the billiard inverse. Trefethen supplies conditional-continuation context, not a new billiard theorem. Florio–Leguil's version-5 notice removes the affected geometric open-billiard spectral-rigidity claim; that removed statement cannot be used as a competing theorem. [L1–L5]

A further relevant point of comparison is Zelditch's Annals paper on analytic symmetric plane domains: its published abstract describes localized wave-trace invariants around periodic billiard orbits and spectral determination under the stated symmetries. This is a different interior spectral problem, not a theorem about these dispersing endpoint laws. Nevertheless it is useful context for explaining which part of all-order orbit-local boundary recovery is familiar and which part the present relative law changes. Such a comparison would sharpen the originality discussion and also prevent the mistaken argument that localization around a special orbit is itself disqualifying. I recommend a brief, hypothesis-accurate comparison, not an assertion of equivalence or a new theorem. [L6]

These checks concern primary records and observation scope, not complete proof audits of those papers or an exhaustive priority investigation. The search does not establish that the present main theorem is already known. Arbitrary deletion of the principal or full technical corpus is not requested, nor is another abstraction section needed merely to respond to this report.

## 5. Disposition codes

**R62-D1 — Mathematical status:** the five new statements withstand the scoped examination, subject to the minor literal correction R62-m1. No fatal counterexample to either rate or new mandatory core reconstruction is established. This is not a complete proof certificate for the delivery.

**R62-D2 — Concrete correction:** correct the all-history pilot-grid endpoint bound to allow the ceiling. Preserve the distinction between good-history stopping times and the deterministic all-history grid/cap. No change of asymptotic theorem statement is needed.

**R62-D3 — Updated contribution and dependencies:** retire an unqualified objection that complete-germ recovery has no finite-sample or calibration-inclusive consequence. Preserve the analytic prior, radius loss, marked independent-preparation experiment, ideal-recording restriction of the new subsection, substantive position pilot, and distinction between statistical existence and finite computation.

**R62-D4 — Editorial recommendation:** decline at the requested level on the current exceptional-significance case. A further editorial assessment should evaluate the relative/action mechanism and the actual strength of its consequences, not equate another small technical amendment or successful build with closure of an importance judgment.

## 6. Independent reproduction and evidentiary limits

The downloaded native artifact has SHA-256 `e02c1f9bb6cb60ad1cbd08dfd1923f2e92672d52ab97ec7f2e6d10b6da2710bc`. Independent verification checked lengths, SHA-256 values and Git blob identities for all **767 frozen files**, reconstructed the manuscript subtree in Section 1, verified **126 distinct active inputs**, and checked **45 build-report evidence entries**. The separate v61 archive comparison verifies the preservation figures in Section 2. Hash comparison is not authentication of authorship or a reconstruction of the entire repository tree. [D1]

All three entries were freshly rebuilt from the extracted manuscript source with shell escape disabled, regenerated auxiliaries, and companion/full/principal build order. All **432 pages** agree with the native PDFs in extracted text and same-renderer 72-dpi RGB arrays. The rebuilt PDF bytes differ. Final logs have four full-manuscript and one principal underfull notices, none in the companion, and no match for undefined references/citations, missing characters, overfull boxes or LaTeX errors. Actual visual inspection covered principal pp. **65, 68 and 69** at **108 dpi**. No clipping or unreadable mathematical expression was observed on those pages. All-page computational parity is not all-page visual inspection. [D1]

The independent mathematical script imports no author checker and uses no removable assertions. It checks **1,458 exact conditional count configurations**, **16 binomial and 80 Bernstein finite-tail cases**, **12 exact cell-tube cases**, **four symbolic exponent identities**, **27 calibrated and 21 complete-budget even schedules**, and **three exact fractional-grid counterexamples** to the literal time bound. Ordinary and optimized Python emit identical JSON. These are finite checks of the algebra and probability interfaces, not proofs of the relative determinant limit, infinite-dimensional inversion, billiard realization of arbitrary numerical parameters, global continuation, or minimax optimality. The author's own preservation/diagnostic checker was not rerun. [D2]

The report, audit ledger, results, independent diagnostic and reproducibility utilities are retained together in this new review directory. Only review files are added; manuscript source, old reviews, native deliveries, default-branch refs and repository permissions are not altered by this review.

## Source keys

All S-keys refer to actual source `037c80dc44d8191e6f808591ea0651e813234d06` under `papers/A2-v17-boundary-information-coarsening/`.

- **S1:** `article/23f2_finite_experiment_analytic_inverse_v62.tex`, lines 1–463; principal Section 13.4, pp. 63–69. Five new statements, including R62-m1 at lines 448–450.
- **S2:** `article/23a3_conditional_observation_inverse_v60.tex`; particularly the bounded real-restriction lemma and conditional contact theorem, principal Theorem 12.15, p. 58. The complete v59 function-space construction is a retained earlier input, not freshly recertified in full here.
- **S3:** `article/23f_single_offset_law_inverse_v42.tex`, lines 1–174; four-density inverse, fixed-order stability and earlier finite-flight consequence.
- **S4:** `v3/20_integration.tex`, physical flux and residual-time integration; `v4/10_boundary_layers.tex`, half-line/relative normalization and two-ended determinant proof, particularly lines 120–326. The complete earlier finite-chain construction is outside fresh full certification.
- **S5:** `article/25a_common_observables_v25.tex`, lines 1–266; full Theorem F.46.2, exact scan cap F.46.5, physical observation space and coordinate error. The grid definition is at lines 113–129.
- **S6:** `journal/DEPENDENCY_LEDGER_V62.md`; `journal/full_reference_routes_v62.tex`; explicit full-only aliases and retained dependencies.
- **S7:** `rigidity.tex`; `journal/01_structural_statements_v56.tex`; `article/00c_finite_experiment_overview_v62.tex`; current structural scope and additive finite-experiment overview.
- **R1:** `reviews/a2-v61-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md`, frozen at `9ec2004a18cccc69ed473685bdf94c91f0b25d4d`; complete report read.
- **R2:** `RESPONSE_TO_REFEREE_V62.md`, `HISTORICAL_DERIVATION_AUDIT_V62.md`, `COVER_LETTER_V62.md`, `LITERATURE_CHECK_V62.md`; author-side arguments and provenance, not proof substitutes.
- **D1:** `AUDIT_LEDGER.md`, `AUDIT_RESULTS.json`, `verify_delivery.py`, `compare_baseline.py` in this review directory; native artifacts 10427846002 and 10426471183; source-to-review-ready GitHub comparison.
- **D2:** `independent_checks.py` and the full emitted results summarized in `AUDIT_RESULTS.json`; reproducible full logs/output accompany the local audit archive.
- **L1:** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983, primary record accessed September 16, 2026: https://arxiv.org/abs/2510.18983 .
- **L2:** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4, related DOI 10.1007/s00222-023-01191-8: https://arxiv.org/abs/1905.00890v4 .
- **L3:** Gerhard Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37 (2009), 459–489, arXiv:0903.0702: https://arxiv.org/abs/0903.0702 .
- **L4:** Lloyd N. Trefethen, *Quantifying the ill-conditioning of analytic continuation*, arXiv:1908.11097: https://arxiv.org/abs/1908.11097 .
- **L5:** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, arXiv:2010.04120v5, including its correction notice: https://arxiv.org/abs/2010.04120v5 .
- **L6:** Steve Zelditch, *Inverse spectral problem for analytic domains, II: Z2-symmetric domains*, Annals of Mathematics 170 (2009), 205–269, DOI 10.4007/annals.2009.170.205; publisher's abstract and primary record, not a fresh proof audit: https://annals.math.princeton.edu/2009/170-1/p06 .
