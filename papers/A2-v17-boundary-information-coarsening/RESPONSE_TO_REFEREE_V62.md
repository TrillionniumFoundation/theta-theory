# Response to the independent report on A2, revision 61

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Revision:** 62, September 16, 2026  
**Addressed report:** `review/a2-v61-independent-harsh-top4-2026-09-16`, immutable head `9ec2004a18cccc69ed473685bdf94c91f0b25d4d`.  
**Reviewed mathematical source:** `71e0bd6306f54466728c2e6e781bb0f422c5cfb0`; native artifact `10426471183`.

We thank the referee for distinguishing correctness within the inspected arguments from the case for exceptional significance. The report establishes no mandatory new core repair and expressly says that the mechanism-centered revision was responsive. We do not turn its adverse placement recommendation into an invented mathematical error. Nor do we abandon the stated inverse problem, replace its conclusions by weaker ones, or remove the technical corpus.

## 1. The mathematical change

Revision 62 connects two established parts of the paper while retaining the complete local analytic contact pair as the target. The previous finite-flight inverse controlled each fixed jet order in a strong real norm. The conditional analytic inverse controlled complete germs from two *limiting* laws. The new subsection, **Finite preparations and complete analytic contact recovery**, gives their finite-experiment counterpart and a confidence bound in a complete-germ norm.

Its principal statements are `lem:v62-finite-densities`, `thm:v62-finite-contact`, `thm:v62-budget`, `cor:v62-calibration`, and `cor:v62-total-budget`, all proved in `article/23f2_finite_experiment_analytic_inverse_v62.tex` and included in both manuscripts. They establish:

1. Uniform finite-to-limiting density control on an interior square, uniform offset continuity, and the exact full-phase acceptance lower bound `p_j >= c exp(-Gamma j)`. These use relative normalization before division by the probability.
2. A two-point complete-germ estimate from actual finite laws,
   `||psi-psi_tilde||_r <= C (|g-g_tilde| + (e_jk + exp(-omega j) + exp(-omega k))^vartheta)`,
   and simultaneous bounds for all Taylor coefficients on every smaller radius.
3. In an exactly calibrated selected-channel experiment, an estimator using **2N raw independent full-phase preparations**, including failures, with confidence radius
   `C (log(C_* N/alpha)/N)^[vartheta omega/(4 omega + Gamma)]`.
   The observation is a finite endpoint histogram and the success counters required to normalize it. The flight number is even and logarithmic in N; the grid is refined with N. The target is not restricted to a finite-dimensional model.
4. With estimated gap and endpoint coordinates, an explicit error budget containing the amplified offset error `j v_g + v_t` and the hard-cell displacement error `r_c/h`. A preliminary calibration cap is added to the raw attempt count. The existing position-sensor pilot yields a calibration-inclusive complete-germ confidence conclusion, at its actual additional hypotheses.
5. Estimating the pilot cap explicitly gives the total-budget confidence radius `C ([log(C B/alpha)]^2/B)^(vartheta omega/(12 omega+Gamma))`, with at most B preparations including the full onset scan. The exponent 12 comes from the actual pilot grid and successful-onset probability, not an unexplained cost assumption.

The proof does **not** apply the four-density identity to a finite-bridge density or an empirical histogram. It fits cell averages of a realizable limiting law, compares that law to the true limiting law, and applies the two-point analytic inverse only afterwards. A countable dense image and a positive-tolerance first-index rule make the estimator measurable without asserting a finite computational search bound. The binomial and cell concentration arguments, the finite bridge error, and the even-flight/grid rounding are given explicitly.

The added result is a quantitative consequence of the relative/action mechanism and elementary sampling estimates, not an unrelated new rigidity principle. Its role is to demonstrate what the nonlinear information can support in a finite, fully charged experiment. It is not offered as an automatic answer to the referee's general-journal importance judgment.

## 2. Response to the significance assessment

The report fairly identifies the limitations of the demonstrated reach: localized alternating channels, a diagonally dominant variational problem, rich law-valued exact data, and additional hypotheses for global quantitative conclusions. We preserve these facts. Our affirmative case remains that a physically normalized rare-event law retains and recovers complete nonlinear contact geometry despite an exponentially vanishing twist. The actual-smooth factorization and relative determinant argument are still the core analytical contributions, not a collection of independent claims for every downstream reconstruction step.

The new consequence makes one aspect of that reach more concrete. Complete analytic local geometry can be estimated from finite records without first fixing a highest jet order, and exponential rarity enters the preparation-error exponent explicitly. This contrasts with simply interpreting a limiting function-valued datum as already observed. The cost is visible: logarithmic flight length, an increasing number of cells, a local analytic prior, loss of radius, and charged failed preparations. No statistical optimality, ordinary marked-length implication, single-orbit mixing theorem, or unrestricted finite-scalar global inverse is asserted.

The exactly calibrated power rate is **not** claimed for the total cost of learning the calibration. For the estimated-calibration experiment the total count is `B_pil + 2N`, with `B_pil` supplied by the retained pilot theorem. We now estimate its dependence: the scan has cap at most `C (j+1) exp(Gamma j) epsilon_pil^(-3) log(C/alpha)`. Taking `epsilon_pil` proportional to `h^4` controls cell displacement and yields the slower complete-budget exponent above. Thus the stronger ideal-calibration exponent is not mislabeled as a total-cost rate. Likewise, the new local-germ norm is not silently replaced by a global obstacle or lattice norm. Existing global reconstruction and acquisition results remain available at their stated strength.

We request an independent reassessment of the original mechanism and this finite-experiment consequence. An adverse importance assessment is not declared mathematically closed by the new theorem, the page count, or a successful build.

## 3. Disposition of the report's numbered items

| Item | Treatment in revision 62 |
|---|---|
| R61-M1: physical phase measure | All original phase-measure and localization proofs are unchanged. The new acceptance lemma uses the exact phase-volume formula, not a proposed substitute endpoint ensemble. Selected nonminimal channels remain selected itineraries. |
| R61-M2: cofactor and trace-class normalization | Original proofs are unchanged. The new density bound starts from their relative estimate. It never divides an absolute action remainder by an exponentially small twist. |
| R61-M3: actual-smooth inverse | All original smooth factorization, odd-jet and full analytic inverse modules are unchanged. Complete-germ confidence estimates use the bounded analytic neighborhood of v60, not bounds on smooth Taylor coefficients. |
| R61-M4: finite-flight strong-norm inverse | The fixed-order result and proof remain verbatim. The new theorem concerns the complete analytic target under its additional analytic prior; it does not rewrite the earlier theorem's hypotheses. |
| R61-M5: realized area/jet comparison | The entire support-family construction is unchanged. Its assertion remains confined to the horizontal ground-onset leading record; no comparison with every channel or a complete marked length spectrum is introduced. |
| R61-M6: action and determinant response | Both contributions and the coefficient `sqrt(3)/2` remain unchanged. Scalar mass variation and conditional law variation are not conflated. |
| R61-E1: mathematical reach and significance | Addressed by the explicit finite-experiment consequence and the affirmative argument above, with its assumptions and costs. No claim that it compels a positive editorial decision. |
| R61-E2: no nominal repair iteration | No new error is attributed to the report, no second introduction rewrite is performed, and no old theorem is removed. The short added overview points to new proved results rather than restating the earlier placement debate in the article. |
| R61-D1: bounded correctness assessment | Accepted at its stated coverage. It is not cited as certification of all 420 previous pages or of the new proof. |
| R61-D2: preceding response was addressed | Explicitly acknowledged. Revision 61 is not relabeled nonresponsive. |
| R61-D3: preserve observation and dependency scope | Marks, laws versus samples, smooth versus analytic categories, finite global alternatives, nuisance-window results and substantive acquisition inputs are retained. The new pilot dependency is explicitly declared. |
| R61-D4: independent editorial judgment | Requested. Mathematical preservation and native delivery are verified separately and are not evidence of exceptional significance. |

## 4. Preservation, literature, and delivery

Before editing, all 753 files in the v61 frozen native source were checked for byte length, SHA-256 and Git blob identity. All inherited paths remain. Only the two entry files and the manuscript README are amended; exact originals are archived. Every inherited theorem/proof module, including the v61 introduction, remains byte-identical and active in its original relative order. The principal route adds explicit aliases for the existing full-manuscript pilot dependencies.

`HISTORICAL_DERIVATION_AUDIT_V62.md` records the proof interfaces examined. `journal/DEPENDENCY_LEDGER_V62.md` distinguishes the new local statements from the additional physical pilot application. `LITERATURE_CHECK_V62.md` records a targeted current check of primary records, not an exhaustive priority investigation. The new mathematical controls test the sampling inequalities, rounding and cell geometry; they do not certify the relative determinant or the analytic inverse. Final native source, PDF, workflow and visual-inspection identities belong to the review-ready delivery record.
