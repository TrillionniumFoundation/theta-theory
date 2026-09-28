# Response to the independent referee on A2, revision 69

**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Revision:** 70  
**Date:** September 16, 2026

The report answered here is `reviews/a2-v69-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md`, frozen at commit `ba42d7a3a7873739c596497c5b2b884452f130d1`. Its reviewed mathematical source is `1a46fd69a508bccb90c6d2553892124f068f4657`, manuscript subtree `e0c2434849fe72a715cec1fae5e6e36bf90b5669`. This response is an author-side submission document, not another independent assessment.

## Nature of this revision

We respond to the report's actual distinction: the new finite-preparation proofs withstood its scoped examination, while the case for exceptional significance and the organization of several observation models remained unpersuasive. There is no identified fatal error to repair in those proofs. We have therefore not manufactured a replacement theorem, weakened the smooth conclusion, substituted an analytic hypothesis, or removed any of the retained mathematics.

The revision changes the mathematical exposition and proof architecture. The principal article now opens with a common-model main theorem, the two essential proof interfaces, the finite-preparation consequence, an actual nonformal separation example, and a data-sensitive literature comparison. The full periodic proof chain is printed immediately after that introduction. The prior broad formulations remain printed in the appendices; all finite-chain, analytic, global matching, calibration, statistical and companion arguments remain active in their respective complete entries. Theorem `thm:v70-main` and Theorem `thm:v70-finite` consolidate existing results. They are not counted as new mathematical discoveries.

## R69-E1: the mathematical thesis and the significance of acquisition

The revised opening is [article/00i_main_thesis_v70.tex](article/00i_main_thesis_v70.tex). Its thesis is the following concrete inverse statement: conditioning near one supplied clear periodic polygon retains enough information to determine actual smooth contact functions, including flat differences, despite an exponentially vanishing unconditioned mass. This is not an assertion that a list of kernel and concentration lemmas creates a new general statistical theory.

The introduction displays both indispensable interfaces rather than relying on the number of conclusions. First, the exact cofactor identity removes the reference mixed twist before the determinant comparison and before probability normalization. Absolute convergence of stationary actions is not a replacement for this relative physical estimate. Second, the actual stationary envelope has a nonvanishing initial-visit term and later visits contracting with constant one. Global quadratic comparison and the signed finite-jet inverse align the jets; a finite high-vanishing norm then eliminates the remaining smooth difference. Equal Taylor coefficients alone do not give this conclusion.

The actual equal-area flat family is part of the principal mathematical thesis. It preserves contact and action Taylor jets while changing the boundary laws on every sufficiently small collar. Consequently, the distinction between a complete law and a formal all-order contact record is realized by closed obstacles, not merely by two formal series or an abstract generating-function example. The finite experiment makes this distinction accessible at each fixed nonzero separation, with failures and endpoint recording error included in the stated threshold.

The finite-preparation result is now presented exactly as the report credits it: an acquisition consequence of the geometric mechanism, using classical statistical ingredients and an essential realizable-selection interface. It changes the input of this inverse problem from an exact law to a finite charged record. We do not claim a new general statistical inverse method, a sharp acquisition threshold, efficient enumeration, or a new geometric theorem arising solely from the revision's reorganization.

We maintain the submission's proposed highest general-journal scope on the relative-law/actual-smooth-contact mechanism and its nonformal physical content. This is an affirmative mathematical case for specialist assessment, not a claim that editorial significance has been proved or that the adverse recommendation is automatically closed.

## R69-E2: observation assumptions, norms and quantitative scope

The new introduction defines the supplied polygon, phase labels, tangent/normal frames and closing translation before the main theorem. It explicitly distinguishes the measured tangent projection from the unknown normal graph height. The following hypotheses are retained, not silently removed:

| Result | Observation and prior | Target and conclusion |
|---|---|---|
| Exact smooth contact determination | Same clear nongrazing marked polygon, positive-curvature smooth contacts, phase-resolved laws at two exact separated offsets | Complete contact germs, with no initial candidate closeness or analytic prior |
| Real-profile stability | Bounded positive `C^{m+3}` class, a common collar and sufficiently small realizable `C^m` law distance | Complete real profiles in `C^0`; low-jet alignment precedes the weighted comparison |
| Finite-preparation recovery | Finite forward smoothness bounds, exact success/gate tags and offsets, independent full-phase resets, bounded post-acceptance endpoint errors | Measurable actual-table estimator and a sufficient all-preparations-charged upper rate |
| Analytic norm inversion | Local bounded-holomorphic neighborhood and specified complex radii | Complete analytic germs in that norm |
| Whole-obstacle continuation | Connected closed analytic boundaries, fixed placement/lattice and full visitation | Whole labelled obstacle images |
| Unregistered alternating multichannel reconstruction | Its weaker local marks, single-offset law and separate matching/visitation hypotheses | The previously stated lattice reconstruction and finite ambiguity |

The displayed finite-preparation summary includes the actual exponents `alpha=s/[2(m+s)+2]`, `beta=alpha*omega/(omega+alpha*Gamma)` and `gamma=s/(m+s+3)`, and rounds flight length down to a returning multiple of `P`. The sufficient-success conditions and the bandwidth/small-error requirements remain explicit. We have not converted the illustrative weak-contraction substitutions into an exhibited table, an optimality claim, or a lower bound.

The real estimator and the pair-dependent weighted inverse are also separated. A candidate-pair envelope is used for a comparison theorem. It is not asserted to be an observation-only algorithm. Likewise, countable minimum-distance selection is measurable but need not be computationally useful. Exact labels, gates and offsets are still essential. Endpoint readout robustness is not advertised as robustness to mislabeled events, uncertain calibration, arbitrary contamination, or dependence along a single trajectory.

These qualifications are the previously proved hypotheses, not a reduction from smooth to analytic contact rigidity. Contact-local smooth determination and global analytic continuation remain distinct conclusions.

## R69-E3: reader-facing proof architecture

The principal article and complete technical manuscript now follow the same central order:

`marked experiment -> exact relative physical law -> action extraction and actual envelope -> global curvature and signed jets -> smooth separation and aligned stability -> finite charged experiment`.

The five core proof modules `10a` through `10e` are printed consecutively immediately after the new introduction. Their mathematical bodies are byte-for-byte unchanged. In particular, the general periodic law is no longer reached only after an alternating-channel catalogue, and the smooth theorem is not introduced as a subsidiary item in a combined analytic/global statement.

The remainder of each entry is divided by purpose: finite-chain foundations and alternating laws; analytic and intrinsic multichannel consequences; and, in the full manuscript, physical information/coarsening and finite-resolution/global reconstruction. Broader formulations and comparisons are moved, not discarded, to the printed appendices. The only changes inside the two older introductory modules replace their opening heading `Introduction` by `Further formulations and comparisons`.

All 136 inherited active TeX inputs remain active across the three complete entries. Every inherited theorem/proof module is retained. The old principal and full entry files and the two renamed introductory modules are archived byte-exactly with their original Git modes. The original README is archived as well. The older broad abstract remains active in the full technical entry, while the principal article has a focused new abstract. No statement is replaced by a proof summary.

The [dependency ledger](journal/DEPENDENCY_LEDGER_V70.md) distinguishes core edges from branches that do not enter smooth rigidity. It names the exact theorem or lemma at every interface and records the observation, norm and extra hypotheses. The organization is not a claim that a large number of retained pages or a successful input-graph traversal proves exceptional significance.

## R69-M1 through R69-M7: preservation and interface checks

**R69-M1 — Relative forward bounds and normalization.** The v64 forward proof and v69 uniform bounds are unchanged. The new opening prints the physical momentum terms, exact reference twist and unconditioned phase factor. The gate is on the larger square `Q_+`; restriction to `Q` is not a second conditioning. The free-area hypothesis remains an upper bound for the acceptance lower bound. Fixed-order geometric priors are not an observed density-error oracle.

**R69-M2 — Derivative estimation.** Lemma `lem:v69-density-estimation` is unchanged. Its dimension-two variance and Bernstein terms, interior boundary treatment, grid interpolation and pathwise `delta*h^{-(m+3)}` perturbation remain in the complete proof. The new introductory theorem does not substitute total variation for a differentiated norm, claim positivity of the kernel estimate, or silently allow corrupted success tags.

**R69-M3 — Measurable realizable selection.** The countable actual-law image and first-index approximate minimization remain unchanged. The introduction places this step before the geometric inverse. Neither finite-flight laws nor noisy density estimates are assumed to satisfy exact limiting billiard identities. No compact image or exact distance minimizer is asserted.

**R69-M4 — Accepted-sample exponents.** The displayed sampling and readout exponents agree with the unchanged proof. Finite-flight bias, the two stochastic terms, approximation tolerance and bandwidth restrictions remain distinct. The new theorem is a consolidated statement of the existing rate, not a minimax or all-jet claim.

**R69-M5 — Charging failures.** The latent Bernoulli/conditional-mark representation, deterministic budget and binomial tail are unchanged. The final error probability remains `2*zeta`, all `JB` attempts are counted, and the rarity exponent remains in `beta`. The introduction retains the floor in the flight count and the explicit conditions for varying confidence.

**R69-M6 — Actual smooth inverse.** The entire v68 module is unchanged. The new proof discussion displays the constant-one visit bound, candidate-pair integrated envelope and finite weighted contraction. It states why full action equality is used again after jet agreement. For stability it records polynomial alignment before the high-vanishing norm. The global quadratic inverse and the corrected stopping propagation are unchanged. No curvature closeness or analyticity premise has been added to exact smooth contact identity.

**R69-M7 — Flat-family test.** The actual equal-area construction and fixed-separation test are unchanged and are now visible in the principal introduction. The radius must be below `Delta/3`, with `Delta=epsilon*exp(-1/u_*^2)`. A fixed noise floor can prevent this inequality, and the statement is not uniform inexpensive recovery as `u_*` approaches zero. No equal-full-spectrum or normalized-density-jet claim is made.

These are preservation and exposition responses to favorable scoped mathematical findings. We do not relabel them as seven new gaps solved in this revision.

## Targeted primary-literature comparison

The current arXiv records for the four billiard comparisons were checked directly. The Bálint--De Simoi--Kaloshin--Leguil Theorem D/Corollary E/Remark 2.3 page was inspected, together with the analytic and enriched-spectrum abstracts and version records. The comparison is given in the main introduction and [LITERATURE_CHECK_V70.md](LITERATURE_CHECK_V70.md). The corrected Florio--Leguil geometric claim is not reinstated. The kernel citation remains context for a classical ingredient, not a citation for the exact billiard derivative/noise theorem.

No exhaustive priority or same-data dominance claim is made. The positive comparison within the manuscript is instead a proved strict distinction between its specified formal contact/action record and its complete boundary-law record in an actual geometric family.

## R69-D1 through R69-D5: final disposition

**D1, correctness:** no mandatory new core repair was identified by the report; the examined proof bodies are retained. The new main statements are checked against them. This is not a fresh certificate of every theorem in the whole corpus.

**D2, advance:** finite charged complete-profile recovery remains a main consequence. The obsolete objection that this theorem necessarily observes an exact differentiated density is not reintroduced.

**D3, scope:** the original exact-data, independent-reset, bounded-class, collar and small-error hypotheses remain visible. The smooth conclusion and the full catalogue are not weakened.

**D4, reproducibility:** the strict source-archive mode correction is retained unchanged. The v69 artifact was downloaded afresh; all 895 source bytes, lengths, Git blobs and modes were checked, and its manuscript tree was independently reproduced before revision. The new native build and author delivery checks are reported separately, with their actual visual and mathematical coverage. Old reviews and deliveries are immutable.

**D5, placement:** the principal thesis and proof route have been substantively recast to address the stated editorial objection. The requested venue level is maintained. Its acceptance or exceptional significance remains for independent specialist/editorial judgment, rather than being marked closed by an author response, a build, or a file count.
