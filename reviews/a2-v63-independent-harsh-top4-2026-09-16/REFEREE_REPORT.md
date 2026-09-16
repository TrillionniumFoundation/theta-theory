# Independent referee report on A2, revision 63

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 16, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted referee-style assessment, not a commissioned journal report, an editorial decision, or a formal proof certificate. Correctness, reproducibility, originality, and exceptional significance are assessed separately. The author's response and delivery records are claims to check, not substitutes for the mathematical argument.

## 1. Recommendation and frozen submission

**Recommendation: decline at the requested highest general-journal level on the present exceptional-significance case. The concrete correction and literature request from the preceding report are satisfactorily addressed. No new mandatory core mathematical repair is established in this round.**

The all-history pilot-time error R62-m1 is closed: equation (13.24) now retains the ceiling allowance and distinguishes a successful stopping event from the complete programmed grid. The published Zelditch comparison is appropriately qualified. Neither change alters the two confidence rates or their complete analytic-germ target. It would be incorrect to continue citing the old arithmetic error, or the absence of that comparison, as an outstanding objection.

The adverse recommendation is consequently editorial, not a claim that a new counterexample has been found. Revision 63 is a correction and contextualization of revision 62, not another new mathematical theorem. Its improvements deserve credit without being made to bear the weight of a new exceptional-significance argument. The judgment in Section 6 engages the strengthened finite-experiment results; it does not revert to the obsolete claim that the work has only exact, freely observed limiting laws.

| Object | Immutable identity |
|---|---|
| Review-ready branch | `revision/a2-v63-review-ready-2026-09-16` |
| Review-ready head | `ecf359fcaf72e649f0c2a411bdd155bba3c82708` |
| Actual compiled mathematical source | `f5517519440b897707ddc60deeafba19e86bb5a5` |
| Reconstructed manuscript subtree | `b042811c7ceb2c5fd841b2a03ab0b8c232c39dce` |
| Manuscript directory | `papers/A2-v17-boundary-information-coarsening/` |
| Source branch | `revision/a2-v63-referee-response-2026-09-16` |
| Native workflow / attempt / artifact | `35050788011` / `1` / `10428569064` |
| Previous v62 report | `a568573d1d4a5d976f6db3c54122d97c769acd38` |
| Source reviewed in that report | `037c80dc44d8191e6f808591ea0651e813234d06` |

The principal article has **125 pages**, the full technical manuscript **301 pages**, and the companion **seven pages**. Page references below are to the principal article unless prefixed by F. The source-to-review-ready comparison contains three delivery commits and no intervening change to a compiled mathematical input. The current finite-experiment module was also fetched directly at the compiled commit; its Git blob, `5b5284c6fffb3ac4be504aa545b1abd647fc2153`, agrees with the frozen archive. [D1]

### Coverage and exclusions

This round reads the complete current finite-experiment module and the complete physical position-pilot construction, including the localization, mass, grid, and cap arguments. It follows the normalized finite-density interface through the physical flux formula and the two-ended relative determinant proof; re-examines the realizable-law inverse and statistical selection interfaces; and checks the active principal statements, contribution discussion, revised comparison, response, cover letter, and dependency declaration. [S1–S7]

This is **not** a fresh line-by-line proof audit of all 433 pages. The complete earlier finite-chain/full-phase prerequisites, the entire v59 Banach-space inverse and v60 continuation construction, every global matching/lattice and moving-family proof, all support-coordinate conversions, the realized quartic example, the remaining adaptive/statistical catalogue, and the companion's mathematics are not freshly certified in their entirety. The unchanged analytic inverse and conditional observation theorem remain previously scoped inputs; their role in the current finite-experiment argument is examined directly. Mechanical reproduction covers every page, which is a different assertion.

## 2. Disposition of the previous report

| Previous point | Present disposition |
|---|---|
| R62-m1 / R62-D2: universal pilot-time bound omitted a ceiling allowance | **Closed.** The printed proof now gives the correct strict all-history bound and separately retains the sharper good-history bound. |
| R62-E2: focused comparison with orbit-local inverse spectral recovery | **Addressed.** Both active introductions contain the same hypothesis-qualified comparison with Zelditch's published theorem. |
| R62-M4: measurable estimator existence is not a finite computational algorithm | **Clarified in the introduction.** No finite running-time theorem is claimed or used. |
| Finite preparations and calibration-inclusive confidence for complete germs | **Retained.** Neither target nor exponent is weakened to a fixed-jet or finite-dimensional result. |
| Distinction between analytic prior, actual observations, and global reconstruction | **Retained.** Closed scope qualifications are not reopened as hidden gaps. |
| Exceptional significance | Reassessed in Section 6; neither a citation nor a ceiling correction establishes it. |

Independent comparison of the two frozen archives finds all **767 inherited source paths** retained: **759 unchanged**, eight modified with byte-exact originals archived. All **126 inherited active inputs** remain active; one shared literature input makes 127. The five finite-experiment statement bodies are byte-identical. These are source-level findings, not counts of independent mathematical results. [D1]

## 3. The corrected pilot bound and the complete-budget argument

### R63-M1. The all-history correction is exact, not merely asymptotically harmless

**Location:** `article/23f2_finite_experiment_analytic_inverse_v62.tex`, lines 448–465; equation (13.24), p. 69. Compare the retained grid and cap in `article/25a_common_observables_v25.tex`, equations `eq:v25-pilot-grid` and `eq:v25-pilot-cap`. [S1–S2]

The actual grid is

$$t_\ell=jg_-+\ell\varepsilon,\qquad L_{\rm grid}=\left\lceil\frac{j(g_+-g_-)}\varepsilon\right\rceil+2.$$

Writing $q=j(g_+-g_-)/\varepsilon$, the revised proof gives

$$t_{L_{\rm grid}}-jg_+=(\lceil q\rceil-q+2)\varepsilon\in[2\varepsilon,3\varepsilon).$$

The left endpoint is attained when $q$ is integral. The upper endpoint is never attained. Thus every programmed pilot time is strictly less than $jg_++3\varepsilon$, including on failed scans. The previous example now fits the corrected statement exactly:

$$j=2,\quad g_-=1,\quad g_+=3/2,\quad\varepsilon=2/101,$$

$$t_L=308/101>307/101=jg_++2\varepsilon,\qquad t_L<309/101=jg_++3\varepsilon.$$

The good-history statement $T_{e,b}\le jg_e+2\varepsilon$ is different: it concerns stopping by a near-onset successful grid point. The source now expressly says that a failed scan may reach the last programmed point. It does not try to apply the good-history estimate universally. The deterministic preparation cap already counts all $L_{\rm grid}+1$ points, so no extra attempts have been omitted.

There is a further useful check on the time accounting. If all scans exhaust, their total evolution time is

$$2|E|N_{\rm pil}\left[(L_{\rm grid}+1)jg_-+\frac{\varepsilon L_{\rm grid}(L_{\rm grid}+1)}2\right]
\le B_{\rm pil}\,t_{L_{\rm grid}}.$$

The proof need not use this exact sum, but it confirms that cap times maximum duration covers the worst history. Clipping the preliminary gap to the known interval, with a default on failure, also bounds all later programmed times. Consequently the final $CB\log(C_0B/\alpha)$ evolution-time bound includes failed histories. This closes the actual objection; no change of theorem statement or confidence exponent is needed. [S1, D2]

### R63-M2. The physical pilot is substantive and its scan logic is sound

The imported position pilot, full Theorem F.46.2, is not merely a reference label. Its proof obtains uniform endpoint localization from the positive Hessian of the distance at the selected normal contact and a positive margin away from that contact. Small total excess forces each flight to be short enough for the local estimate. The first and last recorded positions are therefore $O(\sqrt\varepsilon)$ from their contacts, with constants uniform on the declared compact marked class. [S2]

The positive mass estimate uses a small endpoint region and a residual-time interval inside the event, together with the relative twist and phase normalization. It supplies

$$p_*(j,\varepsilon)=c_*\varepsilon^2e^{-\Gamma j}$$

at a grid point whose excess lies in $[\varepsilon,2\varepsilon]$. The scan does not infer impossibility from finitely many failures and does not require a lower mass bound at every later time. A grid point in the required interval exists for every permitted onset. Failure at that one point bounds the failure of the scan to have stopped by it. This remains valid if an earlier successful stop has already occurred.

The count of grid points and attempts per point yields

$$B_{\rm pil}\le C(j+1)e^{\Gamma j}\varepsilon^{-3}\log(C/\alpha).$$

The experiment assumes planar position sensors in a common frame for the two types of a channel, a clock, retained labels, and independent normalized phase-volume preparations. It is not a transverse-histogram-only pilot, an unmarked channel-discovery theorem, or a mixing result for a single orbit. These are declared experimental assumptions, not newly uncovered defects.

### R63-M3. The two confidence exponents retain their different cost meanings

For exact calibration, the pre-inversion error has the form

$$e^{-\omega j}+h+\sqrt{\frac{x e^{\Gamma j}}{Nh^2}}+\frac{x e^{\Gamma j}}{Nh^2}+\xi.$$

Balancing the square-root term with the first-order histogram bias gives $h\asymp(xe^{\Gamma j}/N)^{1/4}$. The printed even-flight schedule then gives the complete-germ rate

$$\left(\frac{\log(CN/\alpha)}N\right)^{\vartheta\omega/(4\omega+\Gamma)}.$$

The cost is **$2N$ attempts**, including rejected preparations, not $N$ successful observations. The radius loss and outer analytic prior enter through the conditional inverse, rather than being inferred from the finite record. [S1, S5]

For calibration, the timing error is amplified to $\Delta=jv_g+v_t$. If the observable coordinate map moves points by at most $r_c$, a cell changes membership only in its boundary tube. For a square of side $h$,

$$|(\partial C)_{r_c}|\le(h+2r_c)^2-(h-2r_c)^2=8hr_c.$$

This gives cell-average bias $8Fr_c/h$ and displaced cell probability at most $5Fh^2$ when $r_c\le h/2$. No Jacobian or density for the displaced observation map is assumed. Fresh observations are analyzed conditionally on a good pilot history, then the pilot failure probability is added. [S1]

Since the pilot gives $r_c=O(\sqrt\varepsilon)$, taking $\varepsilon\asymp h^4$ makes $r_c/h=O(h)$ but costs $h^{-12}$ in the scan. With $h\asymp e^{-\omega j}$, the complete cap is bounded by

$$C(j+1)e^{(12\omega+\Gamma)j}\bigl(\log(C/\alpha)+\omega j\bigr).$$

Inverting this cap with the stated even schedule gives

$$\left(\frac{[\log(C_0B/\alpha)]^2}B\right)^{\vartheta\omega/(12\omega+\Gamma)}.$$

The corrected last-grid time affects neither balance. The slower exponent is genuinely calibration-inclusive; it is not the exact-calibration rate with the pilot omitted. Both powers are constructive upper bounds for specified policies, not minimax exponents. I find no new error in these balances within the printed large-budget regime. [S1, D2]

## 4. Re-examined statistical and analytical interfaces

### R63-M4. Conditioning, fitting, and normalization are not interchangeable operations

With a fixed number of independent attempts, the success count $M_b$ is binomial. Conditional on $M_b=m$, the successful marks have the conditional success law: fix the successful indices, factor the joint measure, and sum over index sets. The count need not be ancillary. This argument does not condition a stopped stream on having completed a cap. The concentration bound is uniform over every $m$ above the specified lower threshold, so integrating over those counts is legitimate. [S1]

The outside category is retained and the denominator counts all selected successes. Discarding successes outside the observation square while leaving the candidate cell probabilities unchanged would fit a different law; the manuscript does not make that substitution. Conditional Bernstein bounds use the upper cell mass $Fh^2$, followed by a union bound over both types and cells. The lower-tail allowance and cell allowance fit within the stated failure probability.

The countable dense realizable-image construction proves existence of a measurable approximate minimum-distance selector. A positive tolerance and a first-index rule relative to a countable infimum avoid assuming an attained minimum. Its countable output range also gives measurability in the inner-disc norm. For a calibrated gap strip, the positive slack allows approximation of the true image within the strip. None of this proves that the infimum or selected index can be computed in finite time. The new introduction correctly states that distinction. [S1, S6]

Crucially, the empirical histogram is not assumed to be smooth. The proof first bounds the residual of the selected realizable limiting law, then compares two realizable laws with a common Lipschitz bound. Only then does it convert cell-average control into uniform real control and invoke the analytic inverse. Likewise, a finite-bridge law is compared with its limiting law before using the separated density identity. The proof does not impose the limiting factorization on a finite bridge or a corrupted histogram.

### R63-M5. The rare-event normalization remains the main substantive forward input

The finite-density lemma compares unnormalized numerators

$$F_{j,d'}=b_j(d'-E_j)_+,\qquad F_{\infty,d'}=B_b(u)B_b(v)(d'-S_b(u)-S_b(v))_+.$$

The relative boundary theorem controls $b_j$ and $E_j$ on a common fixed collar. Positive-part Lipschitz continuity controls both numerator and integral, and a common interior square supplies a positive normalization floor. Thus normalization of the conditional density does not divide a crude absolute error by an exponentially small success probability. The physical probability itself is kept separate:

$$p_{j,b,d'}^T=\frac{a_b}{2\pi A(T)\sinh(j\gamma(T))}Z_{j,b,d'}\ge ce^{-\Gamma j}.$$

The phase-flux formula and residual-time integration, rather than the conditional density alone, determine this charged acceptance mass. Selected itineraries are not automatically identified with an entire maximal-collision event. [S1, S3]

The re-examined two-ended proof starts from the normalized cofactor identity

$$\log b_j=\sum_i\log\{g[-\ell_{uv}(y_i,y_{i+1})]\}-\log\det(I+G_j\Delta H_j).$$

Endpoint localization makes the perturbation summable. Trimming endpoint tails, comparing the retained end blocks to half-line operators, and controlling reflected and cross-end Green terms are essential. A number-of-sites times operator-norm estimate would not replace this trace-norm argument. The logarithmic series uses the telescoping estimate

$$|\operatorname{tr}(T^m-\widetilde T^m)|\le m q^{m-1}\|T-\widetilde T\|_1,\qquad \|T\|,\|\widetilde T\|\le q<1.$$

Fixed differentiation orders introduce polynomial losses absorbed by a strict exponential margin; this does not assert order-uniform real derivative estimates. I found no new defect in this examined relative-normalization interface. Its proof, not a histogram diagnostic, carries the forward approximation. The complete earlier finite-chain prerequisites are outside a fresh full certification here. [S3]

The law inverse then uses

$$1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}=t(u)t(v),\qquad t=\frac{S}{d-S}.$$

A nonzero anchor controls one scalar square root and retains signed odd coefficients. That algebra is useful but is not itself the relative billiard theorem. The complete action inverse and its conditional real-observation consequence remain distinct analytical inputs. [S4–S5]

### R63-S1. The strengthened statistical conclusion is local, but not merely finite-jet

The finite-preparation result estimates the entire analytic contact pair on a smaller disc and simultaneously controls all factorial-weighted Taylor coefficients. It does not first fix a maximal derivative order. This is a real improvement over an exact limiting-law formulation and must remain credited.

It is still an approximate confidence statement under a fixed analytic prior and declared preparation/sensor model. It is not exact recovery of infinitely many coefficients from one finite record, a uniform rate over arbitrary recording efficiencies, or a computational reconstruction algorithm. The exact global finite-fiber/lattice result and the model-local finite-scalar coordinate result retain separate hypotheses. The new local rate does not quantify full-obstacle continuation or choose every global matching alternative. These restrictions are correctly disclosed; they are not pending corrections. [S1, S5, S7]

## 5. The new published-literature comparison

### R63-L1. Zelditch is relevant context, not a reduction or a competing endpoint-law theorem

The new shared passage appears in both active introductions. Its comparison was checked against **the published** Annals paper, including printed pp. 208–209, rather than only against a title or an earlier arXiv abstract. Zelditch's Theorem 1.1 concerns the class $\mathcal D_{1,L}$ of simply connected analytic plane domains, with a reversing involution, a nondegenerate bouncing-ball orbit, isolated iterated lengths, and the specified additional endpoint and elliptic exclusions. The symmetry relates the two boundary graphs; it does not merely declare both graphs independently even. [L1]

The revised text appropriately credits orbit-local all-order recovery from wave-trace information. It then contrasts the present controlled endpoint-law observation, relative rare-bridge normalization, and two-contact inverse without a symmetry relation between the graphs. These are distinctions of hypotheses and observation maps, not a proof that the present theorem removes assumptions from Zelditch's spectral theorem. No information ordering between full spectral data and endpoint laws is established or claimed. The request R62-E2 is therefore met. [S6, L1]

The internal realized comparison with specified leading gap/area/quadratic/count data is a different matter. The new text limits that comparison to those data; it does not promote it to equal full Laplace spectra or equal marked length spectra. This round checks the accuracy of that scope declaration, not the complete quartic example afresh.

### R63-L2. The other comparisons remain hypothesis-dependent

The refreshed primary records distinguish Finamore–Leguil's **enriched** marked-length datum for finite-horizon Sinai billiards from the analytic open-billiard setting of De Simoi–Kaloshin–Leguil. Neither establishes a reduction to the present controlled law. Osius supplies association-model context, and Trefethen supplies conditional-continuation context; neither supplies the billiard relative inverse. Florio–Leguil's version-5 notice removes the affected geometric open-billiard spectral-rigidity assertion while retaining dynamical conclusions. The removed statement is not an available competing theorem. [L2–L6]

This is a targeted primary-source and observation-scope check, not an exhaustive priority investigation or complete proof audit of those works. I do not claim that the present main theorem is already known. A harsh review cannot infer redundancy from related titles any more than it can infer novelty from different terminology.

## 6. Exceptional significance and editorial assessment

### R63-E1. The strongest case is one mechanism, not the accumulation of consequences

The manuscript now presents a coherent chain: a physically normalized relative long-bridge law retains nonlinear half-line actions; stationary cancellation justifies actual-smooth signed contact inversion; the full analytic action inverse and a prior-dependent restriction estimate control complete germs; finite observations access that target with a charged calibration-inclusive confidence bound. The unknown lattice and channel poses in the exact global theorem are genuine outputs, not geometry supplied to the inverse.

These are strengths. They do not, in my judgment, yet establish the exceptional mathematical significance needed for the requested highest general journals. The central relative/action argument operates in a deliberately selected alternating-channel setting with protected collars and a uniformly controlled local variational problem. The two-ended trace-class comparison is substantive, but the submission has not persuaded me that its demonstrated reach and depth, as distinct from the number of consequences attached to it, warrant the proposed placement.

After the relative law and contact inverse are available, many subsequent steps are familiar types of argument: finite-dimensional triangular inversion, inverse-function reasoning, conditional analytic propagation, finite congruence matching, a displacement cochain, histogram concentration, measurable minimum-distance selection, and cost balancing. Their compatibility is not automatic and is often carefully handled here. Nevertheless, presenting each as another exceptional innovation would overstate the case. The statistical extension explains usefulness; it does not independently establish a sharp information principle or a corresponding global quantitative rigidity theorem. Those stronger conclusions are not required for correctness, but their absence limits what significance can be inferred from this particular extension.

The newly added spectral comparison improves this discussion. In particular, it prevents the facile objection that localizing near a special orbit is itself disqualifying. My reservation is about the demonstrated depth and reach of the present relative/action mechanism, not a categorical rule against orbit-local inverse problems, infinite-dimensional data, or long papers. The targeted literature search does not justify a claim of redundancy, and a specialist may reasonably value this mechanism more highly.

Revision 63 does not introduce a new theorem changing that assessment. Correcting the pilot endpoint and improving attribution are necessary scholarly improvements, not evidence for a different mathematical scope. I therefore retain the adverse placement recommendation after crediting the actual advances already present in v62.

### R63-E2. No further nominal repair cycle is prescribed

The author has complied with the concrete requests of the preceding report. I do not recommend inventing another small blocker, appending an unrelated stronger inverse problem, or adding another verification certificate as though one of those would settle an importance judgment. No new abstraction section or arbitrary deletion of proved material is requested. The principal article and full technical corpus should remain distinct.

A further independent editorial assessment should concentrate on the central relative/action theorem and why its mechanism is—or is not—an exceptional advance. It should not repeat closed objections, treat the finite-data result as absent, or call a computational method established where only a measurable estimator has been proved. Another expert's positive recommendation would need a substantive account of that mechanism, not a tally of revisions.

## 7. Disposition codes

**R63-D1 — Correction:** R62-m1 is closed by the printed all-history identity and its good-history distinction. The deterministic cap and both exponents are unchanged.

**R63-D2 — Comparison and attribution:** R62-E2 is addressed by the shared, published-theorem comparison. The estimator-existence/computation distinction is now explicit in the introductory discussion.

**R63-D3 — Mathematical status:** no new mandatory core repair or fatal counterexample is established within this round's coverage. This is not certification of every theorem in the three entries.

**R63-D4 — Editorial disposition:** decline at the requested level on the present exceptional-significance case. Do not reinterpret this as an unresolved arithmetic gap or a request for another routine repair-only iteration.

## 8. Independent reproduction and evidence limits

The downloaded v63 native artifact has SHA-256

`2a2c8d78236274484f1fd3ff6ba905a01ee4eab4c0c2d60e363c5b9670af79ba`.

Independent checks verify file lengths, SHA-256 values and Git blob identities for **784 frozen files**, reconstruct the manuscript subtree using recorded Git modes, check **127 distinct active inputs**, and verify **45 build-report evidence entries**. Per-entry active counts are 116 full, 48 principal, and one companion. The separate baseline comparison verifies both source manifests, inherited paths, the eight archived originals, and the five unchanged finite-experiment statement bodies. Hash consistency is not authentication of authorship or a reconstruction of the entire repository tree. [D1]

All three entries were freshly compiled with shell escape disabled, regenerated auxiliaries, and companion/full/principal build order. All **433 pages** match the native PDFs in extracted text and same-renderer **72-dpi RGB arrays**. PDF bytes differ. The final full log has three underfull notices; principal and companion have none. No undefined-reference/citation, missing-character, overfull-box or LaTeX-error match was found. Actual visual inspection covered principal pp. **9, 66, 68 and 69** at **108 dpi**; no clipping or unreadable mathematical expression was observed there. All-page computational parity is not all-page visual inspection. [D1]

The independent mathematical diagnostic checks **100 exact rational grid configurations**, **500 onset locations**, **400 exact worst-duration bounds**, **1,476 exact conditional-count factorizations**, **36 numerical pilot-failure bounds**, **four symbolic exponent identities**, and **12 exact displaced-cell mass inequalities**. It detects 52 failures of the superseded all-history $2\varepsilon$ bound; these are negative controls of the old sentence, not counterexamples to the corrected theorem. Ordinary and optimized Python emit identical JSON. No manuscript checker is imported, and the author's preservation/diagnostic program was not rerun. [D2]

These controls do not prove an infinite-dimensional inverse, trace-class convergence, physical realization of arbitrary numerical parameters, global analytic continuation, or minimax optimality. Reproduction and finite checks support a transparent audit trail; they do not settle a mathematical-significance judgment.

## Source keys

All S-keys refer to actual source `f5517519440b897707ddc60deeafba19e86bb5a5` under `papers/A2-v17-boundary-information-coarsening/`. [Immutable source root](https://github.com/TrillionniumFoundation/theta-theory/tree/f5517519440b897707ddc60deeafba19e86bb5a5/papers/A2-v17-boundary-information-coarsening).

- **S1:** `article/23f2_finite_experiment_analytic_inverse_v62.tex`, lines 1–474; complete finite-experiment module. Theorem 13.7, p. 66; Corollary 13.9, pp. 68–69; corrected equation (13.24), p. 69, source lines 448–465.
- **S2:** `article/25a_common_observables_v25.tex`, lines 1–266; physical position pilot, full Theorem F.46.2 and its exact grid/cap. This round reads the proof, not merely its citation.
- **S3:** `v4/10_boundary_layers.tex`, lines 1–386; half-line and two-ended relative normalization. `v3/20_integration.tex`, physical flux and residual-time normalization interface. Complete earlier finite-chain/full-phase prerequisites are not freshly certified.
- **S4:** `article/23f_single_offset_law_inverse_v42.tex`, especially lines 1–162; realizable density-ratio inverse and its observation conventions.
- **S5:** unchanged `article/23a2_analytic_contact_inverse_v59.tex` and `article/23a3_conditional_observation_inverse_v60.tex`, as retained analytic inputs, not a new complete proof audit of those modules; their current use is explicit in S1.
- **S6:** `article/00d_orbit_local_comparison_v63.tex`, lines 1–53; `journal/00_principal_introduction_v61.tex`; `article/00_structural_introduction_v48.tex`; both published bibliography entries. The shared comparison is actively included by both manuscripts.
- **S7:** `rigidity.tex`; `journal/01_structural_statements_v56.tex`; `journal/DEPENDENCY_LEDGER_V63.md`; `RESPONSE_TO_REFEREE_V63.md`; `COVER_LETTER_V63.md`; `LITERATURE_CHECK_V63.md`. Author-side claims and current scope, not proof substitutes.
- **R1:** [Previous v62 report](https://github.com/TrillionniumFoundation/theta-theory/blob/a568573d1d4a5d976f6db3c54122d97c769acd38/reviews/a2-v62-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md), especially R62-m1 and R62-E2.
- **D1:** `AUDIT_LEDGER.md`, `AUDIT_RESULTS.json`, `verify_delivery.py`, and `compare_baseline.py` in this review directory; native artifacts 10428569064 and 10427846002; source-to-review-ready GitHub comparison.
- **D2:** `independent_checks.py` and the actual emitted diagnostic results summarized in `AUDIT_RESULTS.json`; full outputs and fresh-build logs accompany the downloadable audit archive.
- **L1:** Steve Zelditch, *Inverse spectral problem for analytic domains, II: Z2-symmetric domains*, Annals of Mathematics 170 (2009), 205–269, DOI 10.4007/annals.2009.170.205. [Publisher](https://annals.math.princeton.edu/2009/170-1/p06); [published PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v170-n1-p06-p.pdf), especially printed pp. 208–209.
- **L2:** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983](https://arxiv.org/abs/2510.18983).
- **L3:** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), related DOI 10.1007/s00222-023-01191-8.
- **L4:** Gerhard Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37 (2009), 459–489, [arXiv:0903.0702](https://arxiv.org/abs/0903.0702).
- **L5:** Lloyd N. Trefethen, *Quantifying the ill-conditioning of analytic continuation*, BIT Numerical Mathematics 60 (2020), 901–915, [publisher](https://link.springer.com/article/10.1007/s10543-020-00802-7).
- **L6:** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), including its correction notice.

Primary records above were checked on September 16, 2026. The published Zelditch hypothesis pages were also inspected as PDF screenshots. The other primary records were checked for the stated scope and attribution, not subjected to complete proof audits.
