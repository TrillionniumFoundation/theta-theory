# Response to the A1 v6 referee report

**Revision:** A1 English v7 — *Sparse observation algebras, confluent directions, and finite-state memory*  
**Author:** Qian Qi  
**Date:** 6 September 2026  
**Controlling review:** `review/a1-english-v6-harsh-referee-2026-09-06`, commit `414f8c43a6236586362c1532c00aa9b9da01fe64`  
**Reviewed manuscript:** `750a65ef62422e81307b4a61fd891ee42fa2639e`, `papers/A1-english-v6/`  
**New branch:** `revision/a1-english-v7-confluent-resolution-2026-09-06`

The report distinguishes a sound principal argument from an insufficient demonstration of significance at the requested general-mathematics-journal level. We accept that distinction. We do not recast the report as finding an error in the sparse rank formula, and do not reopen the preceding objections that the report explicitly closed. The revision retains the complete exact theory and its proofs, and adds a uniform quantitative theory at additive collisions. The publication objective remains Annals / Inventiones / JAMS / Acta; neither the additional theorems nor their numerical diagnostics constitute a journal-level acceptance judgment.

The principal manuscript contains all 15 previous result labels and 10 additional result labels, with their proofs. Its new sections are integrated before, between and after the existing streaming results, rather than attached as an unproved research plan. The original v6 source directory, the complete v5 companion inside it, the earlier foundations, and every pre-existing repository file are inherited without alteration. Updated historical wording and bibliography occur only in the new v7 directory.

## E1 — The central contribution must carry its significance

**Response.** The revision's mathematical object is now the attainable product--test pairing together with its resolution scales. The exact sparse formula remains a starting theorem, not a surrogate for a quantitative result. Section 5, Theorem 5.1 (`thm:confluent-law`), proves a class-wide uniform law for affinely varying exponent sets with a fixed positive coefficient calibration and a fixed full-support prior.

At a future additive collision, group formal sum exponents by their limiting value. A cluster of multiplicity `s` contributes the divided-difference orders `0,...,s-1`. Omitting the constant coordinate gives an ordered list `nu_1,...,nu_d`. Subject to the explicit full-future condition `d <= n(r-1)`, the optimal checkpoint distortion, both unconditional in a single fixed exploration experiment and minimax over histories, is bounded above and below by constant multiples of

```
Phi_theta(M) = max_(1 <= ell <= d)
               theta^(2(nu_1+...+nu_ell)/ell) M^(-2/ell).
```

The constants are uniform in the state budget and the collision parameter, including the limiting calibration. This is not a theorem obtained by continuity of matrix rank. Its substantive steps are as follows.

* A confluent generalized Vandermonde argument proves strict pairing against `t^lambda (log t)^k/k!` for every full-support prior, including singular priors. The limiting binomial product tangent is genuinely attainable inside the same command cube.
* Newton interpolation factors the **physical** query map into a fixed injective matrix and the diagonal scale matrix `diag(theta^nu_i)`. The logarithmic jets are analytic coordinates, not fictitious new sensor outputs. Thus an arbitrarily chosen Euclidean norm in desingularized coordinates is not mistaken for prediction risk.
* Uniform inverse bounds and positive failure evidence give an unconditional, uniformly nondegenerate cube in desingularized coordinates. The subsequent rectangular quantization calculation gives the scale-sensitive rate.

The classical status of divided differences, total positivity, sumset/Hilbert correspondences, Euclidean quantization and conditional-variance identities is stated and cited. We make no new general quantization or Blackwell-principle claim. The new mathematical assertion is their attainable and quantitatively uniform junction, with an additional causal realization in the family below. Whether this contribution meets the significance threshold of a particular journal remains a matter for the next referee; it is not recorded as an issue the author can unilaterally close.

## E2 — Exact rank does not classify resolved predictive directions

**Response.** We address the report's example itself, retaining its source attribution, common labels, fixed horizon and uniformly positive detector. We do not substitute a rarer experiment or rescale its score.

For `A_theta={0,1,2+theta}`, `0<=theta<=1/2`, Theorem 7.1 (`thm:uniform-streaming`) proves

```
c max{M^(-1/2), theta^(2/5) M^(-2/5)}
  <= optimal streaming regret
  <= C max{M^(-1/2), theta^(2/5) M^(-2/5)},
```

with positive constants independent of **both** `theta` and `M`. The prior can be any one fixed full-support probability on `[0,1]`, not only the uniform prior in the technical note. The horizon is five, every report factor is at least `1/24`, and all command/query labels stay fixed. The lower bound uses the same independently uniform three-command acquisition law for all calibrations. The upper filter is stronger than an unconditional construction: it works at every checkpoint and every admitted history and requantizes after each input.

This determines the order of the crossover at `M=theta^(-4)` and distortion `theta^2`. It also gives the sharp order `theta^(2/5)` of the best all-budget lower constant in the eventual five-dimensional rate. Corollary 7.3 (`cor:uniform-bits`) gives the uniform bit law

```
B_*(epsilon,theta)
  = log_2 max{epsilon^(-2), theta epsilon^(-5/2)} + O(1).
```

The `O(1)` is uniform in the calibration interval. These are comparison orders, not leading quantization constants or an exact integer switching budget.

### Why the fifth direction survives after desingularization

At the common binomial tuple, the zero-calibration product tangent is the polynomial space through degree six. The limiting future basis is

```
1, t, t^2, t^2 log(t), t^3, t^4.
```

Strict confluent pairing gives rank six before normalization and five afterward. This is a proof at the singular parameter, not a numerical extrapolation from positive parameters. For the uniform prior, one displayed six-by-six minor is exactly `1/338751673344000000`; the all-prior result is proved independently of that fixture. Compactness then supplies uniform local inverse and evidence bounds on the entire interval `[0,1/2]`.

### Why the filter does not lose uniformity during online updates

The stored exact model is two normalized-factor coordinates at time one, four chronological-factor coordinates at time two, the following five physical coordinates at time three,

```
w = (M_1, M_2, M_(3+theta), M_(4+2theta), M_(2+theta)-M_2),
```

and `(M_1,M_(2+theta))` at time four. The last coordinate of `w` has width at most `theta`. A rectangular grid with at most `M` reachable representatives attains the needed scale at this stage. The preceding and subsequent stages require only isotropic two- or four-dimensional coverings.

Most importantly, the time-three-to-four Bayes update contains **no division by `theta`**. Its coefficients and its positive denominator are uniformly controlled in the physical `w` coordinates. The factor-to-moment changeover also has a uniform bound. The written error recurrence includes all earlier lossy updates; the implemented transducer reads only its previous index and current command/report. There is no exact-prefix tape at the changeover.

The report's bound `C(M^(-1/2)+theta^2)` remains correct and is not presented as an erratum. It describes an unresolved-direction upper strategy. The new law supplies matching lower bounds and an upper strategy after the weak direction becomes resolved.

## E3 — Connect the new sparse direction to one evolving decision problem

**Response.** Section 8 keeps the same three-step exploration, the same two-step query, and the same future Bernoulli event. After the state has been formed it reveals an independent uniform ticket price `U`. The terminal action is binary and the bounded payoff is `A(Y-U)`. Only one query is executed and all five trials are counted. The action changes the payoff, not the detector or the acquisition law.

Proposition 8.1 proves that, for each fixed streaming encoder, the optimal decision loss is exactly half its optimal squared-prediction regret. Thus the same uniform streaming law holds for an optimal binary decision, not just for a reported vector of probabilities. This identity is elementary and is not itself offered as the new structural advance.

Theorem 8.2 (`thm:resolved-value`) supplies the substantive common-value comparison. Let `T_theta` retain the first four coordinates of `w` but discard its weak fifth coordinate. This is explicitly a deterministic postprocessing of a history, **not** a raw one-step symbol erasure and **not** a claim about every four-dimensional encoding. Let `V_T` allow a terminal policy the entire exact statistic `T_theta`, with unlimited precision and no memory restriction. Then

```
c_e theta^2 <= V_full - V_T <= C_e theta^2,
```

uniformly, and for `M >= K theta^(-4)` an actual `M`-state streaming policy satisfies

```
V_M - V_T >= (c_e/2) theta^2 > 0.
```

It therefore beats every `M`-message compression of the erased statistic, even though the displayed comparator is stronger and is given that statistic uncompressed. The same actual calibration, target, payoff, query, exploration law and total Bayes-value baseline occur on both sides.

The lower value bound uses the **same** five-dimensional attainable cube as the streaming theorem. On that cube the desingularized weak coordinate has conditional variance bounded below after the first four coordinates are observed. Its coefficient in the physical query is order `theta`, hence its value is order `theta^2`. There is no separate categorical example standing in for the sparse geometry.

The absolute gain vanishes at collision, as it must. The theorem gives a nondegenerate fraction of the true weak-direction value at the stated resolution scale, not a claim of a numerically large practical advantage. The prescribed acquisition law is not promoted to an arbitrary optimal-exploration lower bound. The mechanical collision-bit theorem remains intact as a distinct application.

## P1 — Published sumset reference

The Eliahou–Mazumdar entry is updated to *Journal of Algebra* **593** (2022), 274–294, DOI `10.1016/j.jalgebra.2021.11.019`. The preprint remains identifiable through the DOI record and historical references. The new divided-difference reference is de Boor, *Surveys in Approximation Theory* **1** (2005), 46–69. `REFERENCE_AUDIT.md` records the primary records used and the limits of the literature check.

## P2 — Meaning of the finite-state construction

The old heading “Constructive streaming upper bound” is changed in v7 to “Finite-state streaming upper bound.” The statement itself now says that reachable representatives and read-only real transition functions are supplied existentially from the exact model. The new uniform theorem uses the same convention, repeated next to its implementation. No synthesis algorithm from finite-precision exponents or unsupplied moment data is claimed. This formal resource model does not treat discarded real input commands as a free historical tape.

## P3 — Borel conventions

Section 2 now takes all spaces with their Borel sigma-algebras, deterministic rules to be Borel measurable, and randomized rules to be Borel kernels. The finite rectangular quantizers use deterministic boundary conventions. Independent seeds and charged historical information remain distinguished. Conditional expectations in Section 8 exist on these standard Borel spaces, and threshold decisions are measurable.

## P4 — History encoding versus quotient chart

The complete original distinction is retained in the introduction, experiment definition, and Theorem 3.4. Chronological normalized factors may retain redundant factorization information. Neither the singular operational quotient nor the newly desingularized map is asserted to possess a global coordinate chart merely because a local rank is known. The lower distributions live in justified local coordinate patches.

## P5 — Diagnostics and reproducibility

The new suite has **97/97 passing finite checks**, including exact confluent minors with higher multiplicities, normalized physical and desingularized ranks under three full-support priors, fixed-label query coefficients, exact shrinking Bayes updates, rectangular integer budgets, and **12 actual index-only finite-input streaming fixtures**. Those fixtures use two fixed commands and four reports, cover 4,096 prefixes through time four, and store one integer in the tested runtime object. They do not test a continuous-input asymptotic theorem.

The unmodified v6 author script was freshly rerun on a copy: **101/101**, including its family of 1,057 mixed minors. The unmodified v6 referee script was also freshly rerun: **108/108**. These are regressions of distinct existing scripts, not a new independent referee appointment and not a sum of mathematical proofs. The full v6 regression receipts, the v7 execution console receipt and input hashes are in `validation/local/`; CI supplies a fresh full v7 diagnostic receipt. The original v6 and review receipts are not overwritten or relabeled.

The principal v7 PDF was freshly compiled in three passes with shell escape disabled. Its 28 pages were rendered and inspected; the final log has no undefined references or citations and no overfull boxes. Two underfull-box notices remain. The complete legacy source is preserved, but no new compilation or mathematical re-audit of the entire eleven-paper program is implied. Repository CI repeats the principal build and diagnostics and records its own environment rather than reusing a local “pass” assertion.

## New-review focus

The key new proof obligations for the next referee are the full-rank confluent pairing at zero; the fixed physical query-metric factorization; uniform local inverse bounds with retained failure evidence; the absence of a singular amplification factor in the actual online update; and the conditional-variance lower bound for the same-task erasure. `PROOF_LEDGER.md` provides exact labels and dependencies. All are supplied as written arguments for scrutiny, not as unresolved placeholders or claims certified by the diagnostics.
