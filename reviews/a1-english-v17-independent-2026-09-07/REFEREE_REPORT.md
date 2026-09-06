# Referee report on A1 English v17

**Manuscript:** *Attainable information geometry in positive experiments*, Qian Qi.  
**Submission reviewed:** `1f3838d89a5820b853d1e4b78194293b23e70bd2`.  
**Source branch:** `revision/a1-english-v17-referee-response-2026-09-07`.  
**Date:** 7 September 2026.  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica.

This is an owner-requested, AI-assisted external-referee-style assessment. It is not a report commissioned by any journal, an assertion of appointment by its editors, or a formal proof certificate. The mathematical analysis and diagnostic program in this directory were prepared for this review; neither the author's validators nor an earlier referee's execution counts are presented as independent execution in this round. Source identifiers, inspection limits, and the public literature consulted are recorded in [SOURCE_INDEX.md](SOURCE_INDEX.md).

## 1. Recommendation and mathematical disposition

**Recommendation: REJECT for the requested four-journal standard.**

**Mathematical disposition: no blocking counterexample or essential unfilled step was found in the new operational-reconstruction results or in the principal forward proof chains examined below, under their printed hypotheses.** This is not a claim that every statement, program, historical appendix, or uniform constant in the entire submission has been formally verified.

These two judgments must not be conflated. The negative recommendation is based on the mathematical significance of the submission for this venue level, not on an invented correctness objection. Conversely, a successful source-preservation check, an explicit elementary proof, or a large finite diagnostic count is not by itself a positive publication recommendation.

The revision does answer the previous report. The ambiguity about finite commands has been removed. The new section supplies an actual converse characterization of the scale products from the entire optimal checkpoint-risk curve. It deals correctly with integer budgets, repeated scales, vanishing products, and past-dimension truncation. It does not merely rename the old forward theorem. Nevertheless, its additional mathematical step is an ordered-envelope duality, conditional on precisely the forward metric classification already proved. It does not identify a new attainable geometry, enlarge the class for which that geometry is established, or provide an independent route from an otherwise unclassified experiment to the proposed invariant. The author now says this explicitly. The issue is therefore the weight of the contribution, not a misleading theorem statement.

My assessment gives substantial credit to the inherited uniform collision theorem: its actual-history minorization, dimension-truncated global cover, and gap-free causal implementation belong together and are not consequences of an ambient singular-value calculation alone. The circular example also correctly distinguishes acquisition attenuation from observation attenuation. Even after that credit, I am not persuaded that the cumulative result has the breadth of mathematical consequence or the conceptual force needed for the requested recommendation. Another referee could reasonably put greater weight on the collision-uniform theorem. The judgment here is not a theorem that these results cannot be important.

## 2. What the paper actually establishes

The resource model is a finite persistent-label model, not finite-precision arithmetic in disguise. A filter keeps one of at most M labels between inputs. The clock, known calibration, fixed model data, and read-only program are not charged to this count. Commands are real-valued; their past values are unavailable except through the label. The future query is selected independently after the label has been formed. Only that query is executed. These conventions are coherent, although conclusions about program length, transient workspace, unknown calibration, or a finite command alphabet would require different statements. The manuscript does not silently assert those conclusions. See `core/06_streaming.tex`, `def:finite-state`, and `sections/structural_comparison.tex`.

For the positive sparse monomial model, the principal conclusion is the two-sided checkpoint law

$$
R_{M;n,m}^{a}\asymp
\max_{1\leq\ell\leq p_{n,m}}
 \left(\frac{\mathcal V_{m,\ell}(a)}{M}\right)^{2/\ell},
\qquad p_{n,m}=\min\{n(r-1),q_m\}.
$$

The constants are uniform on the stated compact subset of the strictly ordered one-step exponent chamber, through collisions of additive future sums. The corresponding causal law is the maximum over checkpoints, attained by one stage-compatible filter, not by unrelated retrospective encoders. The exact continuous-state dimension is the separate quantity `min{n(r-1), |mA|-1}`. The distinction between exact dimension and uniform finite-resolution behavior is legitimate. See `core/03_transversality.tex` and `core/06b_collision_geometry.tex`.

For the circular model, with Haar prior and sufficiently small known contrast, the physical real scales are

$$
\tau^2,\tau^2,\tau^4,\tau^4,\ldots,
\tau^{2k},\tau^{2k},\qquad k=\min(n,m).
$$

Accordingly, the checkpoint law is

$$
R_{M;n,m}^{\tau}\asymp
 \max_{1\leq j\leq k}\tau^{2(j+1)}M^{-1/j}.
$$

The powers do not follow from the number of Fourier coefficients alone. The acquired posterior coefficient carries one factor of `tau^j`, and the physical query contributes another. The assumptions of known contrast, Haar prior, and fixed horizon are visible, not defects concealed in the proof. See `sections/circular.tex`.

The v17 addition says that, within an already established ordered-scale family, the complete integer-budget curve determines every initial scale product up to the same kind of uniform comparison. It thereby characterizes comparison of the whole checkpoint laws, rather than only their eventual slopes. This is stronger information than the dimension alone, but its strength comes from the full forward profile together with the ordered-envelope identity. See `sections/operational_reconstruction.tex`.

## 3. Disposition of the previous report

| Previous item | Disposition in v17 | Consequence for this report |
| --- | --- | --- |
| E16.1: wording could suggest finitely many detector commands | **Resolved.** Both the circular experiment and the comparison section explicitly specify a continuous gate cube and distinguish it from the finite detector, report, query, and label alphabets. The introduction also states continuous commands. | This is not repeated as a current objection. The finite-command countermodel is only an explanation of why the correction mattered. |
| E16.2: the requested significance case was not compelling | **Substantively answered, without reversing the editorial judgment.** There is a new proved inverse formulation, not merely an additional assertion of novelty. | The new result is audited on its merits below. Its elementary character is acknowledged by the author and is not an attribution complaint. |

The v16 report did not establish a fatal error in the principal theorems it examined. It would be improper to convert its negative recommendation into evidence of such an error now. Likewise, statements of clarification that are already present must not become an indefinitely renewable list of referee demands. The present decision is an assessment of this submission, not a device for requiring one more example in each round.

The Git object identity of the complete `core/` subtrees in the v16 and v17 directories was independently compared: both are `ec90bdd89964db07fb2cab26e973ee93fd4c610c`. This confirms preservation of those source bytes. It does not verify the separate claim about all compiled proof blocks or establish their mathematical validity. The complete compiled-preservation validator was not rerun in this review.

## 4. The new inverse theorem: proof assessment

Write `V_0=1`, `V_l=s_1...s_l`, with nonnegative ordered scales, and

$$
e_s(b)=\max_{1\leq j\leq p}(V_j/b)^{1/j},\qquad b\geq1.
$$

For a positive `s_l`, set

$$
b_\ell=V_\ell/s_\ell^\ell.
$$

Order gives `b_l>=1`. Every branch at this budget is at most `s_l`: for an earlier branch one divides out a product of scales at least `s_l`; for a later branch one multiplies by scales at most `s_l`. The l-th branch is equal to `s_l`. Thus

$$
\inf_{b\geq1}b\,e_s(b)^\ell=V_\ell.
$$

The lower inequality holds at every budget, not just the selected one. Replacing `b_l` by its ceiling gives the integer upper inequality, since `e_s` is decreasing and the ceiling is at most twice `b_l`. This validates the factor-two sandwich in `lem:integer-envelope-duality`. It is important not to replace that sandwich by an equality without further assumptions. The audit gives the exact witness `s=(1,2/3,2/3)`, for which the integer infimum for `l=2` is strictly greater than `V_2`.

Repeated scales cause no difficulty; they can share the same supporting budget. If the number of positive scales is r and `l>r`, the last positive branch dominates eventually, and

$$
b\,e_s(b)^\ell=V_r^{\ell/r}b^{1-\ell/r}\longrightarrow0.
$$

The all-zero case is separate and immediate. There is no illicit inference that zero transformed volume entails an exact predictor at a finite budget.

For `c e_s(M)^2 <= R_s(M) <= C e_s(M)^2`, taking the infimum after raising to `l/2` gives

$$
c^{\ell/2}V_\ell\leq
\mathcal I_\ell(R_s)
\leq2C^{\ell/2}V_\ell,
\qquad
\mathcal I_\ell(R)=\inf_{M\geq1}M R(M)^{\ell/2}.
$$

This is the precise mathematical content of `thm:operational-reconstruction`. Uniform curve comparison implies uniform product comparison by this inequality. The reverse implication follows by comparing each term in the finite maximum, using the fixed maximum dimension. Neither direction permits comparison constants that deteriorate with the singular parameter. The claim concerns products and scale orders, not exact multiplicative constants of the unknown optimal risk.

The monomial corollary correctly uses the ordered Leja pivots and their product comparison with determinant volumes; it does not apply the identity directly to arbitrary coefficients of a maximum. Truncation is implemented by padding the scale list with zeros. The circular corollary correctly recovers odd products even though the corresponding odd branches need not be separately dominant. For its paired list, the two products are `tau^(2j^2)` and `tau^(2j(j+1))`. These claims and their zero-contrast cases survived the independent calculations.

No mathematical revision is requested for these four new results on the basis of this audit. The detailed derivation, including the integer-only witness and boundary examples, is in [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md).

## 5. The forward results cannot be dismissed as spectral notation

### 5.1 Actual acquisition and normalization

The binomial factors used in `lem:binomial-tangent` are attainable interior failure factors. Their true product differential spans `n(r-1)+1` separated monomials. This remains useful when the future additive sums collide. In the mixed pairing, the constant coordinate must be kept until normalization: the product belongs to the tangent, so normalization loses exactly one rank, not an unspecified number.

The determinant integration argument in `sections/positive_history.tex` is appropriate for every full-support prior on the stated interval, including priors without a density. Full support gives positive measure to separated interior intervals. It is not being used as an unsupported replacement for rank. The two strict Chebyshev systems provide the determinant sign and nonvanishing needed before integration.

The quantitative minorization also includes the evidence of the selected report word and integrates over the kernel coordinates of the command map. Merely selecting a local section would have produced a zero-measure subset of the original command space. The actual proof avoids that error. This is an important part of the result and deserves more credit than a rank count.

### 5.2 Global cover and exact collisions

The upper bound is not inferred from the local minorized patch. At each fixed calibration, the whole finite-report history image is rational in the command variables, with a positive evidence denominator and bounded semialgebraic format. Prior integrals enter as real coefficients. They need not be semialgebraic functions of the prior or of calibration.

The thin-rectangle estimate in `lem:tame-rectangle` uses bounded section complexity and the classical real Vitushkin entropy inequality. The dimension bound makes higher variations vanish; projection volumes of the containing rectangle give products of its largest sides. The supplied argument also deals with small integer budgets and replaces covering centers by reachable representatives. I found no inference here from a small ambient box alone to a dimension-truncated cover of an unrestricted smooth set.

For the Leja reduction, the pivots are genuinely nonincreasing because the normalized gaps are at most one. The active triangular block remains uniformly conditioned, while inactive pivots are left zero. A reciprocal vanishing gap is not smuggled into the comparison. Complete confluent prefixes, rather than arbitrarily selected isolated Hermite derivatives, are used for attainment. These distinctions are mathematically necessary and are respected.

### 5.3 Causal implementation and randomization

Both principal constructions update a reachable representative and then quantize in the next reachable set. Positivity bounds the denominator on segments between reachable states. Raw monomial moments, and weighted rather than deattenuated Fourier moments, give a gap-free finite-horizon Lipschitz recurrence. Iterating that recurrence accounts for earlier lossy updates; the proof does not reconstruct the exact discarded prefix at a changeover.

For the lower bounds, each checkpoint state is an M-message encoder of the prefix under the same independent exploration law. Projection and conditional averaging allow unrestricted prediction centers and remove decoder randomization for squared loss. Fixing independent public coding randomness does not change the acquisition law. This last qualification matters: a shared variable that generated and remembered the command sequence would be a different resource model.

The fixed-horizon dependence of constants is real. It is not an unfilled proof obligation for an unbounded-horizon theorem that the manuscript does not state. Similarly, separate existential codebooks for each known calibration are not a calibration-blind effective construction; the text says so.

### 5.4 Prior uncertainty is a separate result

The inspected prior-ambiguity argument correctly normalizes a pullback to the prior before claiming an exact posterior tilt. The common-moment lower bound uses two actual priors in one interior consistency class, and overlapping history laws, not priors chosen after each realized history. Its error floor is consequently a different phenomenon from the known-prior scale profile. The new inverse section expressly excludes applying its zero-rank interpretation to a curve with a positive error floor.

I checked these logical separations and the displayed normalization and overlap calculations. I did not independently execute the complete finite-precision synthesis and conformance machinery on all of its inputs. Its preservation and the existence of its author-side tests should not be confused with that additional audit.

## 6. Publication-decisive concern E17.1: significance after the inverse formulation

**Classification: editorial significance; not a mathematical contradiction.**

The strongest favorable case for the paper is the operational identification of the same anisotropic scales in three places: attainable history mass, global approximation, and causal memory. Uniformity through intersecting collisions is a genuine strengthening over a theorem proved only at fixed separated exponents. The circular double attenuation is also a genuine warning against identifying finite memory with the dimension or the observed spectrum alone. I have not located a primary source that simply contains the exact combined minimax theorem in the paper's experiment. This report does not allege that such a source exists.

The difficulty with a positive four-journal recommendation is more specific. Once the matching accessible flags, global covering bounds, and stable updates have been established, the memory law is the rectangular product envelope. The major model-specific identifications are obtained by the separated binomial tangent plus complete Chebyshev--Newton tests, or by the elementary symmetric-polynomial map plus Haar orthogonality. The general positive-history criterion is a useful sufficient test, but not a classification of which positive experiments satisfy these requirements. The new inverse theorem then dualizes the already available envelope. It does not supply a new necessity theorem for the geometric hypotheses that led to that envelope.

This does not make the inverse statement vacuous. Log-concavity of the initial products is exactly what prevents information from being hidden below the maximum, and the integer and zero-rank endpoints deserve a correct proof. But the inverse result's domain of classification is the equivalence class of full checkpoint-risk curves already represented by ordered products. It is not a recovered latent model, an independently identified observation structure, or a statistical reconstruction from finitely observed errors. The manuscript correctly disclaims these stronger readings. Consequently they also cannot supply its significance case.

In my judgment, the added result consolidates the mathematical organization rather than changing the paper's center of gravity. The circular corollary reads the same known paired products back out; the monomial corollary reads the same previously identified attainable determinant products back out. No new posterior directions are shown to exist, no global covering difficulty is resolved for a previously untreated attainable image, and no additional causal obstruction is overcome by the inversion. These are statements about the logical role of the new results, not accusations that the author concealed their role.

An elementary argument can certainly carry a major mathematical contribution, and a specialized class can support a major paper. Therefore neither elementary proof length nor specialized hypotheses alone is a valid rejection argument. The relevant question is what substantial new mathematical understanding follows in this case. I do not find that the present inverse formulation, added to the two forward classifications and the related uncertainty statements, supplies a consequence of sufficient reach to change my recommendation. In particular, the manuscript still establishes two carefully constructed settings rather than a necessity-and-sufficiency structural theory for a broader pre-existing class. Such a structural theory is one possible source of greater significance, not a mandatory theorem that this version improperly omits.

The repair is not another paragraph declaring the same theorem fundamental, another enumeration of preserved statements, or another finite diagnostic suite. Nor do I require a third example, an arbitrary circular prior, growing horizon, or unknown contrast as a mechanically imposed next task. Those would be different research choices, and their absence is not a correctness defect. A materially different editorial case would have to rest on a substantive mathematical consequence or on a persuasive independent assessment of the importance of the present uniform classification itself. There is no correction-sized checklist in this report whose completion promises acceptance.

## 7. Boundaries that must remain explicit

Three statements are worth retaining as guardrails, not as newly discovered flaws.

First, the inverse uses the entire curve over unbounded integer budgets. For any finite B, the ordered lists `(1, epsilon)` and `(1,0)` have identical exact envelope-squared curves for every `1<=M<=B` whenever `epsilon<=1/B`, yet their second products and eventual dimensions differ. This is an exact envelope example, not a claim that two particular experimental optimal risks coincide exactly. The v17 text already excludes finite-observation reconstruction.

Second, comparison of curves does not recover the exact geometric configuration or the exact optimal-risk constants. It recovers uniformly comparable ordered products within the proved representation. Parameter-dependent rescalings with unbounded condition number cannot be absorbed into a uniform invariant. The text's qualification to uniformly conditioned changes is appropriate.

Third, neither taking a maximum over checkpoints nor adding a positive uncertainty floor preserves all of the information needed for the stated checkpoint inverse. The manuscript does not assert either extrapolation. An author response should preserve those exclusions rather than broaden the theorem in prose.

## 8. Literature and attribution

The equation-level Fourier comparison is materially accurate in the portions checked. Van den Berg's published Section 2.2, equations (12)--(15), explicitly describes Fourier representations and their product/update rules [P1 in the source index]. De Neeve and coauthors use reduced-contrast likelihoods and a neighboring-coefficient Bayesian update in Section II, equations (1)--(3) [P2]. A1 does not claim those representations or recursions as new. The finite-label minimax loss in A1 is not the same resource or objective as those displayed phase-estimation procedures. Those cited passages therefore do not establish duplication of A1's sharp law.

The real-geometry inputs are also identified at the appropriate level. Comte--Halupczok recall the classical real variations and entropy inequality in equations (4)--(5) of their introduction [P3]; their nonarchimedean results are not what A1 uses. Zhang--Kileel's Lemma 2.18 provides coefficient-independent regularity bounds for semialgebraic sets [P4]. These inputs do not by themselves establish that A1's attained set has the required format, dimensions, or physical scales; those verifications remain the manuscript's responsibility and are supplied in the inspected argument.

This was a targeted primary-source check, not an exhaustive priority search. In particular, the phrase “standard envelope calculation” in this report rests on the explicit calculation in Section 4 and the audit, not on an unsupported assertion that a particular prior publication contains the same operational theorem.

## 9. Reproducibility and limits of the present assessment

The accompanying standard-library program was written independently for this review and executed successfully. Its recorded run contains **19,166 exact rational/integer assertions and 520 floating Laurent checks, 19,686 in total**, over 461 ordered scale lists and eight node multisets, among other finite cases. The largest recorded scaled floating residual was about `1.11e-16`, against a `3e-12` threshold. The exact tests include repeated scales, zero padding, integer rounding, colliding Leja lists, paired products, finite-budget indistinguishability, and prior-tilt normalization. Floating checks test weighted updates and the physical finite-query identity by direct Laurent multiplication.

The number of assertions is not a number of independent theorems: many assertions are instances of the same identity. In particular, the diagnostics neither optimize over all encoders nor certify compact-family inverse-function constants. They support error detection and reproducibility; the mathematical judgments above rest on the written arguments. Details are in [EXECUTION_REPORT.json](EXECUTION_REPORT.json), and the program is [verify_review.py](verify_review.py).

The submission's PDF was not rebuilt or visually inspected in this round. The author-side complete source manifest and proof-preservation validator were not rerun; neither were previous referees' programs or every inherited compiler test. The full `core/` tree identity was checked separately through GitHub metadata. The principal mathematical sections and the specific secondary arguments listed in the source index were read from the pinned source. No statement here should be interpreted as a fresh exhaustive certification of every appendix.

## 10. Final disposition

The corrected command model and the new inverse results should be retained as legitimate improvements. The examined principal theorems should not be retracted, weakened, or described as disproved on the basis of this report. There is no new blocking mathematical defect identified here.

Nevertheless, I do not recommend publication of this version at the requested four-journal level. The decisive reservation is the cumulative mathematical significance, after full credit for the actual-history, collision-uniform, global-covering, and causal arguments, and after an independent favorable audit of the new envelope inverse. The appropriate decision under that assessment is rejection, not an invitation to an indefinite sequence of cosmetic revisions presented as major mathematical repairs.
