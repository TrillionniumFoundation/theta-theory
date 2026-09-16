# Response to the independent referee on A2, revision 62

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Revision:** 63, September 16, 2026  
**Report:** `reviews/a2-v62-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md`, frozen at `a568573d1d4a5d976f6db3c54122d97c769acd38`.  
**Reviewed mathematical source:** `037c80dc44d8191e6f808591ea0651e813234d06`.

We thank the referee for distinguishing the scope of the mathematical checks from the assessment of significance. The report finds no fatal error in the two new confidence rates, identifies one literal error in an auxiliary all-history time bound, and requests a more precise primary-literature comparison. We correct that error in the proof itself and incorporate the comparison in the existing introductory discussion of both manuscripts. We retain the complete principal article, full technical manuscript and two-collision companion, including the geometric rigidity theorems, every inherited proof module and all five finite-experiment statements. No statement is replaced by a conjecture, a fixed-jet substitute, a finite-dimensional restriction or an impossibility result.

## R62-m1 and R62-D2: the deterministic grid endpoint

**Accepted and corrected.** In the proof of `cor:v62-total-budget`, the time bound now uses the actual retained grid. If

\[
q=j(g_+-g_-)/\varepsilon,\qquad L=\lceil q\rceil+2,
\]

then the new displayed identity `eq:v63-pilot-time` is (the manuscript writes `L_grid` to distinguish this index from the preceding logarithmic quantity)

\[
t_L-jg_+=(\lceil q\rceil-q+2)\varepsilon\in[2\varepsilon,3\varepsilon).
\]

Consequently every programmed pilot time is strictly below `jg_+ + 3 epsilon`. The proof separately retains the pilot theorem's sharper `T_{e,b} <= jg_e + 2 epsilon` on its successful stopping event. Failed histories may reach the last grid point and are covered by the former bound. The deterministic cap already includes all `L+1` points. Neither the number of preparations, either confidence exponent, nor the order of the evolution-time bound changes.

The referee's example is reproduced exactly: `j=2`, `g_-=1`, `g_+=3/2`, `epsilon=2/101` give `t_L=308/101`, while the old bound is `307/101`. The revised proof does not reinterpret this arithmetic correction as a defect in the relative law or the inverse theorem. The original module is preserved under `history/v62-review-baseline/`.

**Location:** `article/23f2_finite_experiment_analytic_inverse_v62.tex`, final proof; the same corrected module is actively included by `rigidity.tex` and `main.tex`.

## R62-M1--M3: normalization, realizable laws and random success counts

We retain these arguments unchanged. The finite unnormalized numerator is estimated before division by a common positive normalizer. The relative mixed-derivative comparison, rather than an absolute error estimate divided by a rare-event probability, remains a substantive prerequisite. The physical acceptance probability still charges rejected preparations.

Finite-bridge densities are compared to realizable limiting densities before applying the single-offset inverse. We do not impose the limiting separated formula on a finite bridge. The fixed-attempt construction retains binomial success counts; conditioning on a fixed count is justified by the factorization over successful indices, not by conditioning a stopped experiment on completion. The outside category and the denominator counting all selected successes remain unchanged.

These are retained mathematical arguments, not new theorems claimed for this revision. Their locations and dependence on the relative determinant theorem, phase integration and conditional analytic inverse are recorded in `journal/DEPENDENCY_LEDGER_V63.md`.

## R62-M4: estimator existence versus computation

We agree with the distinction. The countable dense realizable-image selector proves the existence and measurability of an approximate minimum-distance estimator. It does not establish a finite running-time bound for evaluating a countable infimum. A sentence in the shared introductory comparison now makes this explicit at the point where the statistical consequence is discussed. No computational complexity theorem is added, and no such result is used as a premise of geometric rigidity or confidence control.

The estimator, its complete-germ target and the positive approximation tolerance are retained. The restriction on computation is not a reduction to a fixed finite jet or to a finite-dimensional parameter family.

## R62-M5--M6: confidence powers and charged calibration

We retain the two distinct conclusions:

\[
\left(\frac{\log(CN/\alpha)}{N}\right)^{\vartheta\omega/(4\omega+\Gamma)}
\quad\hbox{and}\quad
\left(\frac{[\log(C_0B/\alpha)]^2}{B}\right)^{\vartheta\omega/(12\omega+\Gamma)}.
\]

The first counts `2N` independent attempts with exact calibration. The second uses the actual position-pilot cap and counts the complete preparation budget. The factor `12 omega` still arises from `epsilon` of order `h^4` and a scan cost of order `epsilon^{-3}`; it is not replaced by the exact-calibration factor `4 omega`. The coordinate-displacement argument retains the boundary-tube estimate without assuming a Jacobian for the Borel observation map. Fresh attempts remain independent of the pilot history.

The powers are constructive upper bounds for the printed experimental policies. They are not asserted to be minimax exponents. The source label containing `optimal-schedule` is an inherited cross-reference identifier, not a mathematical optimality claim; its label and the theorem's explicit disclaimer are retained to avoid unnecessary reference churn.

## R62-S1 and R62-D3: the full scope of the finite result

The complete analytic contact pair on a smaller disc remains the target; all weighted Taylor coefficients are controlled simultaneously. The outer analytic prior, fixed protected radii and geometric margins are not inferred from data. Independent normalized full-phase preparations, marked channels, ideal recording for the new rate and the stronger physical position-pilot sensors remain declared hypotheses.

The result is neither exact recovery of infinitely many real coefficients from one finite record nor a finite-time computational reconstruction algorithm. It is not a mixing theorem for one orbit, unmarked channel discovery, a rate uniform over arbitrary recording efficiency, or a global quantitative continuation/lattice theorem. Those distinctions were already part of the theorem statements and are preserved rather than introduced as new limitations. The exact global finite-fiber/lattice results, unknown channel poses and finite-dimensional differential-coordinate results also remain in their original full scope.

## R62-E1 and R62-D4: the positive mathematical case

We retain the intended general-journal submission and make its case at the level of the mechanism. The central contribution is not the number of consequences or the use of familiar concentration inequalities. It is the passage from exponentially vanishing reference twist to a physically normalized nonlinear endpoint law on a fixed collar, followed by an actual-smooth, two-contact inverse. The full function-space inverse and the charged finite-observation results demonstrate distinct consequences of this same passage.

The introduction now separates three logically different comparisons. First, the internal realized family in `thm:v4-jet-fiber` proves that the positive-offset law detects nonlinear contact information absent from the specified leading gap/area/Hessian/count data. Second, comparison with spectral and marked-length problems concerns different observation maps; no unproved equivalence or information ordering is asserted. Third, the finite confidence results explain how controlled observations access the complete local germ, without turning standard statistical steps into independent breakthroughs.

We respectfully maintain that the nonlinear relative-action mechanism and its geometric consequences merit assessment as one coherent contribution. Correcting an auxiliary bound, adding a citation or completing a build does not settle an editorial importance judgment. Revision 63 neither claims to force acceptance nor treats the report as a no-go for the research program. No unrelated stronger inverse problem is imposed as a repair condition, and no additional abstraction section is added merely to increase the apparent scope.

## R62-E2: primary-literature comparison

**Implemented in both manuscripts.** The new shared text `article/00d_orbit_local_comparison_v63.tex` is inserted inside the existing introductory literature discussion. It cites Zelditch's published Annals paper, specifically its Theorem 1.1 and the defining hypotheses of `D_{1,L}`: a simply connected analytic domain, a reversing involution, a nondegenerate bouncing-ball orbit, isolated iterated lengths, and the additional endpoint/nonresonance conditions stated there. The comparison explicitly credits orbit-local all-order recovery from wave-trace invariants and the symmetry relating the two boundary graphs.

The text then identifies what differs here: controlled endpoint-law observations, relative normalization at exponentially rare bridges, fixed positive offsets, actual-smooth remainder control, the two signed contacts without a symmetry relation, and prior-dependent complete-germ inference. It does not claim that merely localizing near a periodic orbit is novel, that our theorem removes hypotheses from Zelditch's theorem, or that endpoint laws and spectral data are equivalent. Both bibliography files contain the published citation and DOI.

The earlier hypothesis-accurate comparisons with Finamore--Leguil, De Simoi--Kaloshin--Leguil, Osius and Trefethen remain. The Florio--Leguil version-5 correction remains explicit; its removed geometric assertion is not cited as an available theorem. The primary records and the exact extent of this literature check are recorded in `LITERATURE_CHECK_V63.md`.

## R62-D1: verification and its limits

The source-preservation check compares every frozen v62 path against the new manuscript, requires exact archived originals for every authorized modification, checks retention of every inherited active input, and confirms that all five statement bodies in the finite-experiment module are unchanged. It also checks the grid arithmetic using exact rationals and the unchanged rate-balance identities. Normal and optimized executions must agree.

Native compilation and product provenance are reported separately in the delivery guide. They test source identity, references and build reproducibility; they are not substitutes for mathematical proof or a fresh line-by-line certification of the whole manuscript. This revision's direct proof work is the all-history time correction; its broader mathematical reading follows the relative-action, smooth-envelope, analytic-inverse and physical-pilot dependencies needed to make the comparison accurately. The retained historical audits identify earlier rounds rather than being presented as independent new certifications.
