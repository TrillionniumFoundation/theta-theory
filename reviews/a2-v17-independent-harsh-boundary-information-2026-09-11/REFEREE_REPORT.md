# Independent harsh referee-style report on A2 v17

**Manuscript:** Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*.

**Review date:** 11 September 2026.

**Requested standard:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the American Mathematical Society.

**Author revision branch:** `revision/a2-v17-boundary-information-coarsening-2026-09-11`.

**Immutable author head reviewed:** `106836283ebe3fabee0479df8976d24f6dbe0bf6`.

**Immediate predecessor reviewed in the previous round:** author source `bd27ed3208cc869f6c7a6547453a2557bfcd03ed`, with the v16 referee report at review commit `c5fed5340df3147f64cb3479cf1837357f73e7a8`.

This is an author-requested, AI-assisted independent referee-style assessment. It is not a journal-commissioned report or an editorial decision by any of the journals named above. I distinguish theorem correctness, originality/significance, exposition, and submission readiness. I do not convert finite diagnostic scripts or a source manifest into a proof certificate.

## 1. Recommendation to the editor

**Recommendation: reject at the requested four-journal level.**

I would not recommend acceptance, conditional acceptance, or a routine major revision carrying an implied route to acceptance at this level.

The reason is no longer a failure to identify what v17 is trying to add. The new revision does contain a real theorem: after residual time is integrated out, the tangent endpoint density vanishes linearly at a moving support boundary, its Hellinger distance is of order `t^2 log(1/|t|)`, and the corresponding endpoint-only billiard experiment has a Gaussian critical profile at the scale `q_j^2 log(1/q_j)`. The fixed-table physical transfer and the resulting hierarchy between full records, endpoint records, and success indicators are mathematically coherent and genuinely sharper than what follows by naively contracting the old full-record total-variation bound.

Nevertheless, this does **not** close the decisive v16 significance objection. The revision itself correctly acknowledges that the linearly vanishing moving-boundary phenomenon is classical: Smith (Biometrika 72 (1985), 67--90, DOI 10.1093/biomet/72.1.67) already records asymptotic normality at a different rate in the `alpha=2` nonregular boundary case. I independently checked the official Oxford Academic abstract at this level. I do **not** claim that Smith contains the manuscript's exact hypersurface coefficient, rare-event thinning statement, billiard whitening, or the exact total-variation testing profile. Those are legitimate additions. My point is editorial: the new general theorem is obtained by a coarea reduction, a truncated-score likelihood expansion, and a triangular-array CLT around a known nonregular mechanism; its billiard application is then an exact ellipse/cap computation followed by the previously established tangent-to-physical TV approximation. That is technically good mathematics, but it is not, in my judgment, a conceptual advance of the breadth or depth normally required to reverse a four-journal rejection.

The strongest mathematical component of the submission remains the pre-v17 nonlinear relative boundary law and its physical determinant normalization on a nonshrinking collar, together with the associated profile inverse and the restricted independent-contact jet inverse. v17 improves the statistical understanding of one observation coarsening of that structure. It does not upgrade the geometric conclusion to unrestricted rigidity, does not produce a new global dynamical mechanism, and does not solve the unknown-table smooth inverse problem at a sharp minimax level.

I found **no fatal mathematical error in the newly added v17 core theorem chain under its printed finite-critical hypotheses**. A harsh report should not manufacture one. I do, however, identify below a concrete statement-level defect concerning the `b=+infinity` regime, together with a continuing build/readiness blocker and a substantial editorial architecture problem.

## 2. What v17 actually adds

The four active additions are the observation hierarchy, the general boundary-information theorem, the endpoint critical experiment, and a random-hazard clarification. The new central route is:

1. for a normalized density `f_t=a_t(w_t)_+` with a regular moving support and linear vanishing at the boundary, prove
   `H^2(f_t,f_0) = (I_Sigma/4) t^2 log(1/|t|) + O(t^2)`;
2. at finite positive information scale, truncate the infinite-variance score at `h=|t| log(1/|t|)^(1/4)`, prove a triangular-array normal likelihood limit, and retain the rare-event failure atom exactly;
3. identify the billiard endpoint tangent law, after common whitening, as
   `f_zeta(x)=(2/pi)(1-exp(-zeta)x_1^2-exp(zeta)x_2^2)_+`;
4. compute the boundary-information coefficient to be exactly one and use `zeta_j~2 exp(-j gamma)`;
5. deduce the endpoint critical scale `r_j=q_j^2 log(1/q_j)`, with limiting TV `2 Phi(sqrt(b))-1` when the effective sample size times `r_j` tends to `b`;
6. transfer this to positive physical offsets by the retained uniform tangent estimate, requiring `omega(d_j)=o(r_j)`;
7. compare, for the same fixed table and preparations, full endpoint--residual records, endpoints alone, and success indicators.

This is a meaningful and internally differentiated addition. In particular, it is not merely the v16 stopped coupling rewritten with different notation.

## 3. Audit of the general boundary-information theorem

### 3.1 Hellinger coefficient

The coarea calculation is sound in the inspected argument. Near the regular hypersurface `Sigma={w_0=0}`, the score contains `v/w_0`; under `f_0=a_0 w_0` this produces a logarithmic second moment. The coefficient

`I_Sigma = integral_Sigma a_0 v^2 / |grad w_0| d sigma`

is the correct boundary coefficient for the displayed representation, and the invariance check under multiplication of the defining function by a positive smooth factor is correct. The omitted boundary collar has mass `O(h^2)`, while the interior score variance is `I_Sigma log(1/h)+O(1)`. Choosing `h` proportional to `|t|` yields the claimed Hellinger leading term.

I also checked the potentially delicate remainder bookkeeping. On `D_h`, the density ratio has the form `1+tS+t^2 R_t` with `R_t=O(1+w_0^{-1})`; the cross term contributes only `O(|t|^3 log(1/|t|))`, while the cubic term at `h~|t|` is `O(t^2)`. None of these terms changes the leading `t^2 log(1/|t|)` coefficient.

### 3.2 Finite critical likelihood limit

For `0<b<infinity`, the truncation `h=|t| L`, `L=log(1/|t|)^(1/4)`, is appropriate. At the critical scale `n p t^2 log(1/|t|)->b`, the probability that a successful sample enters the omitted collar is `O(n p h^2)=o(1)`, the truncated linear score satisfies Lindeberg because each normalized summand is `O(1/L)`, and the quadratic score term concentrates. The resulting null log-likelihood limit

`N(-I_Sigma b/2, I_Sigma b)`

and the TV profile obtained from `E[min(1,exp(Z))]` are consistent.

The Bernoulli thinning contributes no extra likelihood term because the two hypotheses have the same success probability `p_n`; the retained failure atom is therefore handled correctly.

### 3.3 A concrete statement-level defect: the exclusive-support sentence must be scoped

**C17-M1 (minor but real mathematical statement defect).** The sentence in `thm:v17-boundary-information` stating that "the probability of a support-exclusive observation tends to zero under either hypothesis at this scale" must be explicitly restricted to the **finite critical regime** `0<b<infinity` (and of course the subcritical regime).

The proof uses

`n p t^2 = (n p t^2 log(1/|t|)) / log(1/|t|) -> 0`,

which is valid when the information scale has a finite limit. Under only

`n p t^2 log(1/|t|) -> infinity`,

one cannot conclude `n p t^2 -> 0`; for example one may arrange `n p t^2 -> 1`, in which case support-exclusive observations need not be negligible. This does **not** invalidate the theorem's `b=infinity` conclusion `TV->1`, because the proof of that conclusion uses multiplicative Hellinger affinity and does not require exclusivity to vanish. But the theorem statement is ambiguous enough to be false if the sentence is read as applying to all `b in [0,infinity]`. This should be corrected before any submission.

This is not a fatal error in the critical Gaussian result. It is exactly the kind of quantifier/scope issue that a final paper should remove.

## 4. Audit of the billiard endpoint application

### 4.1 Exact cap law and coefficient

The tangent calculation is clean. The whitened Hessian has reciprocal eigenvalues `exp(-zeta_j)` and `exp(zeta_j)`, with determinant one. Integrating residual time converts the uniform three-dimensional cap law into the two-dimensional positive-part density

`(2/pi)(1-exp(-zeta)x_1^2-exp(zeta)x_2^2)_+`.

The determinant-one coordinate change proves normalization. At `zeta=0`, `v=x_1^2-x_2^2` and `|grad w_0|=2` on the unit circle, giving `I_Sigma=1`. Since `zeta_j=2q_j+O(q_j^3)`, the Hellinger expansion becomes

`H^2 = q_j^2 log(1/q_j) + O(q_j^2)`.

The constants in the stated Gaussian profile are consequently consistent: when `k_j r_j->b`, the null log-likelihood tends to `N(-2b,4b)` and the TV distance tends to `2 Phi(sqrt(b))-1`.

### 4.2 Physical transfer is correct in the printed regime, but the regime is severe

The transfer from tangent endpoints to actual positive-offset endpoints uses the old estimate

`TV(actual,tangent) <= C omega(d)`

conditionally and `C p^0 omega(d)` for raw preparations. At the endpoint-critical sample size, the accumulated transfer error is therefore controlled precisely when `omega(d_j)=o(r_j)`. The critical-subsample argument also correctly handles the supercritical case without demanding vanishing approximation error over the entire supercritical sample.

This appears correct, but it is important editorially that the physical regime is very narrow. Since `r_j ~ j gamma exp(-2j gamma)`, the general smooth condition `sqrt(d_j)=o(r_j)` means `d_j=o(r_j^2)`, while the even-contact condition is `d_j=o(r_j)`. The manuscript supplies nonempty sequences, so there is no logical emptiness. But "nonempty" is much weaker than robustness: the sharp endpoint phenomenon is proved in a highly singular joint limit with correspondingly enormous raw preparation cost. This is acceptable as a theorem, but it weakens the claim that the result fundamentally changes the geometric inverse problem.

### 4.3 What the hierarchy proves -- and what it does not

The three-way hierarchy is one of the best parts of v17. For the same simple finite/boundary pair and the same physical preparations, complete records, endpoints, and success bits genuinely have different asymptotic comparison scales. The exact cancellation of the tangent success mass makes the success bit uninformative while the endpoint shape still carries logarithmic boundary information.

But this remains a **fixed-table model-comparison theorem**. The common whitening may depend on the known table because it is used only to compare two known simple hypotheses. The theorem does not provide an observation rule that learns an unknown gap/curvature from endpoint samples at this scale, nor does it establish asymptotic equivalence or minimax optimality for the full unknown smooth-table experiment. The manuscript says this explicitly. For correctness this restraint is a strength; for top-four significance it is a limitation.

## 5. Novelty and significance at the requested level

### 5.1 The new nonregular mechanism is not a new general phenomenon

The official abstract of R. L. Smith, *Maximum likelihood estimation in a class of nonregular cases*, Biometrika 72 (1985), 67--90, explicitly distinguishes the `alpha=2` case, where the density vanishes linearly at the moving endpoint, and states that the MLE is asymptotically normal at a different rate. The present paper appropriately cites this fact.

I do **not** infer from that abstract that Smith already contains the exact multidimensional hypersurface coefficient, the Hellinger expansion in this notation, the thinning formulation, or the billiard cap law. The manuscript's theorem therefore has legitimate content. Nevertheless, the conceptual source of the logarithm and the different normal rate is classical. The multidimensional extension is achieved by a regular tubular/coarea reduction; the simple-experiment limit follows from a truncated score CLT. This is elegant and useful, but not a new foundational statistical principle.

A four-journal case would require a substantially stronger explanation of why the boundary-information theorem changes the mathematical landscape beyond this application. The present `LITERATURE_VERIFICATION.md` expressly says that no exhaustive originality search is claimed and that only the official Smith abstract was checked. That is responsible scholarship for a working revision, but it is not an adequate novelty audit on which to base a claim of top-four significance.

### 5.2 v17 does not strengthen the principal geometric rigidity theorem

The genuinely geometric inverse content remains split:

- the general smooth result determines symmetrized energy/width profiles rather than arbitrary asymmetric contacts;
- the independent-contact jet inverse requires individually even contacts and supplied labelled leading geometry;
- two-flight germs already recover fixed finite jets in that restricted setting;
- analytic continuation is classical once the relevant analytic germ has been recovered;
- the full-profile acquisition exponent is a sufficient procedure bound, not a minimax theorem.

v17 adds a sharp validity/testing scale for one coarsened observation of the finite-versus-boundary law. It does not remove any of the preceding restrictions. Thus the revision makes the paper broader, but it does not make its central geometric conclusion deeper.

### 5.3 The paper is becoming a research dossier rather than a top-journal article

The current entry point has **60 direct inputs** and retains a long chain of previous experiment variants, inverse blocks, calibration results, adaptive results, lower bounds, comparisons, and historical appendices. The new boundary-information theorem is sufficiently distinct that the paper's narrative now contains at least four major themes:

1. nonlinear physical relative laws for long bridges;
2. geometric/profile determination and finite-jet inversion;
3. statistical acquisition/calibration of profiles;
4. nonregular model-comparison limits under observation coarsening and adaptive/stopped experiments.

Long papers are not disqualified by length. The problem is hierarchy. The new result was introduced to answer a significance objection, but the introduction's organization paragraph still describes the second part mainly through Abel stability and regularized profile observation and does not give the new boundary-information theorem the conceptual position its role in the response would require. The abstract, response letter, proof ledger, and body now carry different emphases.

At the requested level, adding another technically correct theorem is not a substitute for a sharper central thesis. The manuscript presently reads like an accumulating dossier of every valid consequence discovered during successive referee rounds. That makes it harder, not easier, to see a single theorem whose depth dominates the surrounding machinery.

## 6. Status of the previous v16 objections

| Previous item | v17 assessment |
| --- | --- |
| C16-E1: four-journal significance | **Still open and decisive.** The new endpoint theorem is real, but in my judgment does not reverse the editorial conclusion. |
| C16-R1: complete native companion-first/main build | **Still open.** The new workflow run failed before any step was reported; no successful complete build is established. |
| C16-R2: stale root discovery pointer | **Closed.** The revision branch root README now points to A2 v17 and labels older versions as historical. |
| v16 adaptive common-history mathematics | **Retained; not reopened.** The new random-hazard corollary is a correct clarification under the printed hypotheses. |
| scalar linearization / physical Fredholm identification | **Retained closed in this review.** v17 does not reintroduce the old conflation. |
| multiplier and finite-jet hierarchy corrections | **Retained closed in this review.** |
| New fatal v17 theorem-correctness blocker | **None established in the audited core route.** C17-M1 is a scope correction, not a collapse of the theorem. |

## 7. Submission readiness and reproducibility

The author revision adds `.github/workflows/a2-v17-native-build.yml` precisely to run the companion-first full native build. At the immutable head reviewed here, GitHub Actions run `34566157170` completed with conclusion `failure`; its single job `103158602793` has an empty step list, no runner, and completed within seconds. Therefore this run does **not** establish a LaTeX failure, but equally it does **not** establish a successful build. The cause is not inferable from the returned job record.

`VERIFICATION.json` correctly refuses to claim a successful full build and records the finite boundary diagnostics separately. The 143 diagnostics are useful negative controls for algebra/source identities, but they do not verify the coarea theorem, the asymptotic probability arguments, the inherited geometric estimates, or the complete manuscript.

For a submission-ready version, the authors should retain a successful build of the exact immutable source reviewed, including the original companion, the complete active `main.tex`, bibliography resolution, final log, and product hash. This is a readiness condition, not the reason for my top-four rejection.

## 8. Required changes before this version should be circulated as a finished revision

**C17-M1 -- theorem scope.** Restrict the support-exclusive-negligibility sentence in `thm:v17-boundary-information` to finite critical/subcritical information scale. Do not let it read as a claim under arbitrary `b=infinity` sequences.

**C17-E1 -- significance.** Do not treat the boundary-information addition as automatically closing the v16 editorial objection. State more sharply what is new beyond classical `alpha=2` moving-boundary nonregular asymptotics, and what genuinely billiard-specific obstruction is solved by the new theorem.

**C17-E2 -- literature positioning.** A top-level submission needs a broader primary-literature audit of nonregular moving-support LAN/likelihood theory than an abstract-level check of Smith. The current narrow attribution is honest, but it is not enough to support an aggressive originality claim.

**C17-E3 -- contribution hierarchy.** Rebuild the introduction and organization around one dominant theorem chain. If the endpoint-information theorem is supposed to be the conceptual response to v16, it cannot remain mostly an added second-part module while the introduction's organizational summary still foregrounds the older acquisition program.

**C17-R1 -- complete build.** Produce a successful, retained, immutable companion-first full native build. Do not substitute isolated-section builds or finite diagnostics.

None of these items should be interpreted as a checklist whose completion would guarantee acceptance at the four named journals. In particular, C17-E1 is an editorial assessment, not a local defect with an automatic repair.

## 9. Final assessment

v17 is a serious improvement over v16 in one respect: it adds a mathematically meaningful observation-dependent critical law instead of merely accumulating another stopped-coupling corollary. I would credit the authors with having answered the previous report in good faith and with having kept the fixed-table, unknown-table, finite-jet, smooth-profile, and minimax scopes more carefully separated than in earlier versions.

But the revision still does not meet the requested four-journal threshold. The new endpoint theorem is best viewed as a sharp, billiard-specific realization and multidimensional coefficient calculation for a classical nonregular boundary mechanism. It does not create a new global rigidity principle, does not eliminate the manuscript's restricted inverse hypotheses, and does not turn the smooth observation problem into a sharp general minimax theorem. Meanwhile the manuscript has become still more encyclopedic, and the complete native build is still not demonstrated.

**Editorial recommendation: reject at the requested top-four level.**

**Mathematical recommendation:** the boundary-information/endpoint-critical module is worth preserving. After C17-M1 is fixed and the literature position is deepened, I would regard it as a technically credible component of a more focused submission. The present report does not certify every retained historical appendix, and it should not be cited as doing so.
