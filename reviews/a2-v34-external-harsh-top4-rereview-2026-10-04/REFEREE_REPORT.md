# External top-four referee report on A2 v34

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v34-calibration-experiments-2026-10-04`  
**Equivalent referee-copy alias:** `revision/a2-v34-referee-copy-2026-10-04`  
**Reviewed commit:** `ed3876b8a82e2c46bc1533457978c15fea1a2114`  
**Reviewed repository tree:** `26e7db3cd999c260e21d086352864334cc1a38c6`  
**Mathematical checkpoint:** `477cbff26270b6a04af2c09b9a82d5e804345c46`  
**Controlling preceding report:** `3d825951afb2c2bd1da258de8648287c046cdc13`  
**Manuscript directory:** `papers/A2-v34-calibration-experiments`  
**Date:** 4 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision, proof certificate, apparatus validation, or exhaustive priority determination.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 34 is a genuine and mathematically substantive response to the v33 report. It does substantially more than restate the scope of the adversarial calibration lower bound. The revision first makes that lower bound's uncertainty quantifiers and pointwise boundary convention explicit. More importantly, it proves a positive reconstruction theorem in a materially different experiment: every command uses a fixed calibrated convex launch footprint, while the fresh additive launch density on that footprint is unknown, may be asymmetric and may have nonzero mean. Under a quantitative lower bound on its mass near the footprint boundary, the manuscript reconstructs the table without estimating this nuisance density and without shrinking the random footprint as the requested geometric accuracy tends to zero.

On the new v34 core audited in detail, I found no fatal counterexample. The reciprocal cancellation with fresh stationary launch noise, positivity-set/Minkowski-sum identity, rolling-lens boundary-mass estimate, comparison of occupations with different nuisance densities, fixed-aperture Green bound, indeterminate-layer query, support-function subtraction, period locking after subtraction, and the displayed attempted-bit exponent are coherent under the stated hypotheses. The retained v33 resource converses remain active, and the final exact-SHA one-article qualification succeeds at the reviewed head. The negative recommendation is therefore not based on a known false central theorem or on a delivery defect.

The remaining objection is conceptual and editorial. The new theorem is an active calibrated input-output result, not a natural billiard invariant. The apparatus is told the complete launch footprint `K`, its laboratory placement and regularity bounds, a lower boundary-mass pair `(b_0, gamma)`, the compass step, a fixed protective aperture, all geometric prior constants, and the positive nonperiod-patch margin needed for uniform finite period decisions. Nominal command positions must still be refined to scale `nu^{s/(s-2)}` even though the random launch spread is fixed. Apparatus motion, construction and calibration of the footprint law, command-coordinate bit complexity beyond the disclosed descriptions, and physical metrology are not included in the attempted-bit count.

The central geometric mechanism is elegant but classical in character. The unknown density is eliminated because the support of the blurred occupation is the known Minkowski dilation `C+(-K)`; one then subtracts the known support function of `-K`. The quantitative theorem combines rolling-disk overlap, Brunn--Minkowski concavity, killed-walk potential estimates, active radial boundary search and interpolation. This synthesis is meaningful in the collision-bit model, but it does not introduce a new general inverse-geometric or probabilistic principle of the breadth ordinarily required at the four journals named above. The stationary-noise sample exponent is only a sufficient upper bound; there is no matching lower bound, minimax theorem, or sharp comparison showing that the large power is intrinsic to this experiment.

In my judgment the focused twenty-eight-page article is now a serious and potentially strong specialist-journal paper. It is substantially clearer and stronger than v33. It remains below the exceptional naturality, universality and conceptual transformation expected at the requested top-four benchmark. I would not recommend another open-ended revision cycle at that benchmark.

## 2. Frozen source and chronology

Both v34 revision names listed above resolve to the same author head

`ed3876b8a82e2c46bc1533457978c15fea1a2114`

with repository tree

`26e7db3cd999c260e21d086352864334cc1a38c6`.

The mathematical checkpoint is

`477cbff26270b6a04af2c09b9a82d5e804345c46`,

which is based directly on the final v33 external-review head

`3d825951afb2c2bd1da258de8648287c046cdc13`.

That report reviewed v33 author commit

`245a2bf5d13b72d81ef85b784e9fcb2dd88ca490`.

The two commits after the v34 mathematical checkpoint modify only the exact-source workflow, one reproduction sentence in the README, and a CI-environment record. They do not modify the active mathematical TeX, test logic, source pins or preserved archive. Thus the mathematical object and the final qualified delivery are cleanly separated.

The exact reviewed v33 paper is preserved under

`papers/A2-v34-calibration-experiments/archive/v33`

at tree

`213cecf77265c5ebea98791a99126b9def5d25f0`.

No A2 revision branch later than v34 existed when this review was frozen. The present review branch starts directly from the final v34 author head and adds files only under

`reviews/a2-v34-external-harsh-top4-rereview-2026-10-04/`.

No manuscript source, author revision branch, previous report, workflow, preserved archive or unrelated paper is modified.

The active article consists of `main.tex`, `references.tex`, and the twelve inputs

- `core/00_setting.tex`;
- `core/00b_resource_overview.tex`;
- `core/00c_stationary_overview.tex`;
- `core/01_local_queries.tex`;
- `core/02_adaptive_boundary.tex`;
- `core/06_finite_precision.tex`;
- `core/03_period_recognition.tex`;
- `core/04_information_bound.tex`;
- `core/07_sequential_gauge.tex`;
- `core/08_calibration_resolution.tex`;
- `core/09_stationary_jitter.tex`;
- `core/05_comparison.tex`.

I also inspected the response, proof/history/literature ledgers, source pins, submission map, current diagnostics and contract tests, local receipt, exact-SHA workflow and run, preserved v33 source, and the complete v33 external report.

## 3. The two calibration experiments

The revision correctly separates two different uncertainty classes.

### 3.1 Localized commands with adversarial bounded implementation error

The retained experiment localizes a nominal start near a chosen center and permits bounded position, duration and angular implementation errors. Its positive theorem uses localization and combined tolerance of order

\[
  \sigma \asymp \nu^{s/(s-2)},
  \qquad \ell+\tau+t\alpha\lesssim\sigma,
  \qquad s=6+\beta.
\]

The v33 converse now has the explicit controller-uniform order

\[
 \forall r\ \exists (\mathcal O_0,F_0),(\mathcal O_1,F_1)\ 
 \forall \mathcal A:
 \mathsf{Law}^{\mathcal A}_{\mathcal O_0,F_0}(Z)
 =\mathsf{Law}^{\mathcal A}_{\mathcal O_1,F_1}(Z).
\]

The two admissible implementation maps may be different and may depend on the table, nominal command and nominal draw. This is a valid worst-case minimax nonidentifiability statement. The revised theorem no longer suggests a lower bound for one common stationary or known noise device. The closed-solid/closed-sweep convention and the inward/outward resolution of every disagreement are also stated pointwise, including tangencies.

### 3.2 A common unknown stationary launch law

The new experiment fixes a known strictly convex footprint `K` satisfying

\[
       t+\operatorname{diam}K<d_0.
\]

At nominal center `x`, the forward command starts at `x+Z` and the reciprocal command at `x+Z+a`, with fresh draws from one unknown density `j` supported on `K`. The law is fixed across commands and independent of the table. It obeys

\[
 j(z)\ge b_0\operatorname{dist}(z,\partial K)^\gamma
 \quad\text{a.e. on }\operatorname{int}K.
\]

No symmetry, zero mean, upper bound, derivative bound or density-evaluation oracle is assumed. This model is genuinely different from the adversarial implementation class, and the manuscript now says so consistently.

## 4. Audit of the stationary reciprocal reduction

For each fixed `z` and compass displacement `a`, the original reciprocal identity gives

\[
 B_a(x+z)-B_{-a}(x+z+a)
   =\mathbf 1_{\mathcal O}(x+z+a)
     -\mathbf 1_{\mathcal O}(x+z).
\]

Averaging the two separately sampled commands against the same stationary law yields

\[
       g_j=(T-I)v_j,
       \qquad
       v_j(x)=\int_K j(z)\mathbf1_{\mathcal O}(x+z)\,dz.
\]

The two physical particles need not share the same realization of `Z`; equality of the prescribed joint laws is sufficient at the level of means. It is essential that the same density and support are used for every direction and command. Command-dependent or table-dependent launch laws would define a different experiment.

The fixed footprint enlarges one component to

\[
              P_C=C+(-K).
\]

The strict gap assumption makes distinct `P_C` separated by more than one compass step, so the retained stopped-walk inverse applies to the blurred occupation. This use of the earlier Bellman argument is legitimate: it needs a bounded function between zero and one, bounded separated positive components, and the forcing `(T-I)v`, not knowledge or smoothness of the convolution kernel.

## 5. Audit of support recovery without density deconvolution

Because the density lower bound is strictly positive at almost every interior point of `K`,

\[
  v_j(x)>0
  \quad\Longleftrightarrow\quad
  C\cap(x+K)\text{ has positive area for some }C
  \quad\Longleftrightarrow\quad
  x\in\operatorname{int}(C+(-K)).
\]

Thus the connected positive components of the exact blurred occupation are precisely the interiors of the Minkowski sums `P_C`. No value of `j` is needed after this support identification. Since support functions add under Minkowski addition,

\[
       p_C^{\rm lab}=p_{P_C}^{\rm lab}-p_{-K}^{\rm lab}.
\]

The subtraction is performed in the supplied laboratory frame. In the finite theorem the estimated difference is shown to remain a support function because the true radius of curvature of `C` has a positive lower bound and the `C^2` reconstruction error tends to zero. This is not a formal set subtraction of two noisy convex bodies.

I found this exact support argument sound. It is also the principal reason that an unknown compactly supported density can be tolerated without Fourier deconvolution. The result would not survive unchanged if the support of `j` were unknown, shifted by an unknown command-dependent amount, or unbounded.

## 6. Audit of the boundary-mass estimate

A finite procedure must distinguish a point a distance `e` inside `P_C` from a point outside it. The manuscript proves

\[
        x\in(P_C)_{-e}
        \quad\Longrightarrow\quad
        v_j(x)\ge c e^{\gamma+3/2}.
\]

The exponent has the correct geometry. At a supporting contact of `C` and `x+K`, uniform interior rolling disks overlap after an inward displacement `d`. A rectangle of tangential width `c\sqrt d` and normal height `c d` lies in the lens, giving area `c d^{3/2}`. Brunn--Minkowski concavity of the square root of the overlap area extends a fixed collar bound to deeper points. Replacing `K` by its erosion `K_{-e/4}` keeps the overlap a distance comparable to `e` from the boundary of `K`; the density assumption contributes the factor `e^\gamma`.

The argument is coherent, including the case `gamma=0`. In a final journal version, the proof should state at the moment of use that `e` is below the uniform rolling-radius thresholds for both `K` and `P_C`. This is what justifies the support identities

\[
 p_{K_{-e/4}}=p_K-e/4,
 \qquad
 p_{(P_C)_{-e/4}}=p_{P_C}-e/4.
\]

The text already places `e` below a prior-dependent `e_0`; making the dependency explicit would remove a small avoidable ambiguity.

## 7. Audit of the inverse modulus with different nuisance densities

Let two experiments have possibly different densities `j_0,j_1` in the same calibrated class and reciprocal forcings differing by `Delta`. The stopped comparison inherited from v31 gives

\[
        \|v_{j_0}-v_{j_1}\|_\infty\le H_K\Delta.
\]

Take

\[
       e\asymp\Delta^{1/(\gamma+3/2)}.
\]

Every point of one expanded component is within `e` of a point in its erosion, where the corresponding occupation exceeds `2H_K Delta`; that point must lie in the positive set of the other occupation. Reversing the roles gives Hausdorff distance `O(e)` between the unions. Component separation then gives a bijection. Subtracting the common footprint preserves the support-function difference, and interpolation on the uniform `C^{6,\beta}` class gives

\[
 \|p_{C_0}-p_{C_1}\|_{C^2}
   \le C\Delta^{(s-2)/(s(\gamma+3/2))}.
\]

I found this reasoning sound. The smoothing sentence should say explicitly that the high-order approximation kernel with vanishing moments through degree six may be signed. A nonnegative probability mollifier cannot have all nonconstant even moments vanish. The required interpolation inequality is standard and unaffected; the terminology should simply avoid suggesting an impossible positive kernel.

## 8. Audit of the fixed-aperture high-accuracy query

The earlier constant-accuracy local query cannot locate the blurred boundary at vanishing scale, so v34 estimates each occupation value to accuracy proportional to

\[
       b_e=e^{\gamma+3/2}.
\]

The new Green estimate is the right way to prevent an artificial factor equal to the Bellman depth. If `E_n` is the difference between noisy and exact killed iterates, nonexpansiveness gives

\[
       E_{n+1}\le T^W E_n+\xi+\zeta.
\]

Summation of the killed transition yields

\[
  E_n(x)\le(\xi+\zeta)
       \mathbb E_x\min(n,\tau_W)
  \le H_W(\xi+\zeta).
\]

The fixed rectangle meets only a prior-bounded number of states in any translate of the compass lattice. Increasing the iteration depth therefore increases computation but not the number of distinct command centers needed for one target. Choosing the survival tail and the forcing/update errors as fixed fractions of `b_e` gives a correct threshold between zero and `b_e`.

Hoeffding estimation of a bounded mean to absolute error `b_e` costs `O(b_e^{-2}\log(1/epsilon))`, hence

\[
        O(e^{-(2\gamma+3)}\log(1/epsilon))
\]

attempts per local membership query. This upper bound is conservative but correct.

## 9. Audit of the finite reconstruction and exponent

Use angular spacing

\[
        h\asymp\nu^{1/(s-2)},
        \qquad e\asymp h^s.
\]

There are `O(h^{-1}\log(1/h))` adaptive radial queries. Multiplying by the cost of one fixed-jitter query gives

\[
  N_\nu
  \lesssim h^{-1}e^{-(2\gamma+3)}
      \log(C/h)\log(C/(h\delta))
  =\nu^{-((2\gamma+3)s+1)/(s-2)}
      \operatorname{polylog}(1/\nu,1/\delta).
\]

For `gamma=0`, the stated power is `(3s+1)/(s-2)`. The exponent algebra is correct. The radial reconstruction of `P_C`, subtraction of the known footprint, preservation of positive curvature, and application of the retained finite period-locking theorem are in the right logical order. The period test is applied to the recovered original bodies, not to the blurred components.

The finite theorem does **not** establish that this exponent is optimal. It uses absolute Hoeffding accuracy for small occupation values and a robust boundary search; other sampling or sequential rare-event methods may improve the rate. A top-four significance claim should therefore rest on the qualitative fixed-spread inverse and its uniform modulus, not on the displayed sample power.

## 10. What v34 closes from the preceding report

The response to v33 is substantive.

1. The table-dependent calibration converse now states the order of quantifiers and the transcript contents explicitly.
2. The pointwise boundary convention and the forced inward/outward displacement are part of the lemma, not dismissed as null-set details.
3. Digital command descriptions remain separated from physical launch precision.
4. The manuscript no longer treats the adversarial lower bound as a universal noise law; it proves a contrasting positive theorem for one common stationary launch distribution.
5. The journal package is reduced to one self-contained article. Full historical source is retained in the repository archive without being made a mandatory nested supplement.

These are real improvements in mathematics and presentation.

## 11. Remaining qualifications

The following boundaries should remain adjacent to every headline statement.

### 11.1 “Fixed spread” does not mean calibration-free

The random footprint `K` does not shrink, but its complete support, laboratory placement, curvature/smoothness bounds, and the constants `b_0,gamma` are calibrated. Nominal command centers are refined to scale `nu^{s/(s-2)}`; durations and directions are exact in the stationary model apart from certified numerical rounding. Unknown support shift, command-dependent jitter, additional bounded duration/angle errors and unbounded noise are outside the theorem.

### 11.2 The new rate is an upper bound

There is no lower bound for the stationary-nuisance experiment, no optimal confidence dependence, and no proof that the boundary-mass exponent must enter quadratically through Hoeffding. The phrase “no resolution floor” is justified in the specified model, but “optimal fixed-jitter complexity” would not be.

### 11.3 Period recognition remains prior-relative

Uniform finite primitive-period decisions still use a bounded periodic presentation and a known positive whole-patch nonperiod margin. Without that margin, only pointwise eventual decisions are retained. The theorem does not infer periodicity or crystallinity from an arbitrary unknown arrangement.

### 11.4 The observation is active and engineered

Each bit is scalar, but its information depends on a selected localized center, an exactly prescribed reciprocal joint command, all-attempt normalization, a calibrated footprint and repeated fresh preparations. This is not rigidity from passive trajectories, a marked-length spectrum, uniformly prepared count germs or a spectral invariant.

## 12. Literature and novelty assessment

The closest algorithmic comparison remains active smooth-boundary estimation: once a reliable indeterminate-layer membership query has been constructed, radial bisection and high-order interpolation are established mechanisms. The manuscript appropriately credits this and does not claim a new abstract bisection principle.

Noisy convex-support estimation is also relevant, but the observation categories differ. Work on convex support recovery from noisy continuous vectors does not directly contain the present pooled collision-bit inverse, while v34 does not address Gaussian or unknown-support deconvolution. The support-function addition, rolling-body geometry and Brunn--Minkowski concavity used to remove the nuisance density are classical convex geometry.

I did not find in this focused review a cited theorem containing the complete combination of reciprocal collision bits, unknown stationary compactly supported launch density, support-only nuisance removal, fixed-aperture Bellman recovery and periodic-table assembly. That synthesis is a meaningful contribution. This was not an exhaustive priority search.

At the requested editorial level, however, the central novelty remains a carefully engineered reduction under a strong apparatus contract. It does not create a general rigidity theorem from a natural dynamical invariant or a new universal theory of active inverse problems.

## 13. Independent diagnostics and source qualification

The accompanying `verify_review.py` imports no author code. Ordinary and optimized Python executions produced identical output. It performs **89,669** finite checks, principally in exact integer or rational arithmetic, covering:

- the reciprocal endpoint truth table and stationary translation identity;
- one-dimensional and Fourier support addition/subtraction controls;
- rolling-disk lens rectangles and the `gamma+3/2` exponent;
- fixed-aperture Bellman monotonicity and Green perturbation bounds;
- query-error allocation and support thresholds;
- adversarial indeterminate-layer bisection;
- exponent balances;
- finite rational period arithmetic; and
- finite binary-cap controls.

These checks are diagnostics, not a continuum proof certificate, a physical sensor execution, a TeX build or a significance judgment.

The author's local source-content receipt records 5,886 current finite checks, 21 current contract tests, ordinary/optimized agreement, successful reruns of the stated retained v33/v32 suites, and a warning-free twenty-eight-page primary. It explicitly does not authenticate a Git checkout or execute a physical apparatus.

The final exact-SHA workflow run `37174046426`, bound to the reviewed head, completed successfully. It checked out the exact triggering commit, verified the numerical dependency inventory, qualified the current article and preserved archive, bound the actual source and execution outputs, and uploaded artifact `11292677471` with digest

`sha256:8117e6340d009ea5bc956fb97083d6e8070495fc0b1112a119e0efa9fe94ca86`.

Two earlier workflow failures, caused by missing retained-suite numerical dependencies, are preserved rather than relabelled. Source delivery is therefore not a basis for the present negative recommendation.

## 14. Final verdict

**Response to the v33 report:** substantively successful.

**New mathematical core:** no fatal counterexample found in the fixed-footprint stationary-jitter inverse, boundary-mass estimate, density-independent modulus, Green-bound query or finite reconstruction chain.

**Minor revisions:** make the erosion/rolling-radius threshold explicit; call the vanishing-moment approximation kernel signed or otherwise specify its construction; keep the exact stationary apparatus contract adjacent to every “no fixed-jitter floor” statement.

**Editorial assessment:** the paper is technically serious, focused, reproducible and potentially strong for a specialist journal. Its strongest theorems remain active-control results under a highly specified apparatus and periodic prior, built from largely classical convex-geometric, potential-theoretic and active-estimation mechanisms. The stationary-noise rate is not known to be sharp, and no natural passive rigidity theorem emerges.

**Recommendation: reject at the requested Annals / Acta / Inventiones / JAMS benchmark.**
