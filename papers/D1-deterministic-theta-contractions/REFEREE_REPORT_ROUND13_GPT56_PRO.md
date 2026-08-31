# Independent Referee Report — Round 13

**Manuscript:** D1 — *Deterministic Theta Contractions*  
**Reviewed branch:** `revision/round13-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `5c8b71e67d62d4a63c53a5a59e7a10f1ccc0f688`  
**Reviewed tree:** `586de2e3cf8c547ca3cbfbc0cb0daba2fd05af59`  
**Controlling module:** `ROUND13_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `379314ae492c385f08c558a91f9257492b4a844785a3ed4cf6b1b11a29d7971e`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject; remove as a standalone submission**

## Executive assessment

Round 13 correctly abandons nonpositive spectral projections as phase probabilities, defines labels by genuine measurable events on the original sample space, retains a boundary component, and separates normalized conditional pressures from unnormalized restricted partition functions. These are genuine corrections.

The new paper is nevertheless an elementary conditional mixture lemma wrapped around assumptions that contain all of the difficult platform mathematics. Its component-LDP theorem gives the wrong rate on basin boundaries: lower-semicontinuous closure does not create recovery sequences inside the conditioned basin. Its “commutation” theorem also treats finite mixing as though it commuted with a nonlinear logarithmic semigroup; log-sum-exp is not a mixture of component log values. Finally, the labels are not canonical—they depend on an arbitrary order parameter, distance, threshold, and chosen compact sublevel—and the local zero-free theorem assumes the phase contribution it claims to construct.

## Decisive objections

### 1. The conditional component rate is wrong on basin boundaries

The theorem states that conditioning on `B_j` gives

\[
 I_j(x)=I(x)-\alpha_j
 \quad\text{for every }x\in\overline B_j.
\]

The assumptions require recovery sequences inside `B_j` only for finite-rate points **in** `B_j`, not for boundary points. The proof says that boundary points follow by lower-semicontinuous closure. That is false.

Consider a sequence of laws on `R` with probability one half at `0` and one half at `delta+1/n`, and let

\[
 B=(-\delta,\delta).
\]

The full laws satisfy an LDP with rate zero at both `0` and `delta`. The conditioned law on `B` is the point mass at `0`; it has infinite rate at the boundary point `delta`. Yet `delta` belongs to `closure B` and the formula above assigns it rate zero.

The correct conditional rate is the lower-semicontinuous envelope of `I` restricted to sequences that actually remain in `B_j`, after subtracting the basin weight exponent. It need not equal `I-alpha_j` on the full closure.

### 2. The nonlinear log-Laplace operation does not commute with finite phase mixing

For component laws `P_{n,j}` and weights `w_{n,j}`, the physical log-Laplace value is

\[
 {1\over n}\log
 \sum_jw_{n,j}
 \mathbb E_{n,j}e^{nF}.
\]

It is not

\[
 \sum_jw_{n,j}
 {1\over n}\log\mathbb E_{n,j}e^{nF}.
\]

Take two deterministic phases with terminal payoffs `0` and `1` and equal weights. The component log values are `0` and `1`; their weighted mixture is `1/2`, while the physical value is

\[
 {1\over n}\log{1+e^n\over2}\longrightarrow1.
\]

The proof says that dynamic evolution is linear before the nonlinear logarithm and that finite summation “commutes with these exact operations.” Linearity before the logarithm is precisely why the result is log-sum-exp rather than a positive mixture of component nonlinear semigroups.

A labelled vector of component values can be propagated phasewise. Forgetting the label after taking exponential values produces a log-sum-exp envelope, not a commuting scalar semigroup.

### 3. The basin labels are not canonical

The label depends on:

- the chosen order parameter `M`;
- the selected compact rate sublevel;
- the chosen components `K_j` within that sublevel;
- the arbitrary threshold `delta`; and
- the metric used in order-parameter space.

Different admissible choices give different boundary bands and different conditional laws. The law-of-total-probability decomposition is exact for every such choice, but exactness does not make one choice canonical or phase intrinsic.

The main theorem's claim that every regular chart “admits a canonical positive basin label” is therefore stronger than anything constructed.

### 4. A full LDP does not automatically give component LDPs

The component theorem assumes:

- basin boundaries are `I`-continuity sets;
- every finite-rate interior point has a recovery sequence staying in the basin;
- the basin weight exponent exists; and
- the conditional rate is good.

These are essentially the component lower-bound theorem. A platform LDP alone gives the restricted upper bound but not the lower bound after conditioning on a possibly moving or thin basin. The paper does not derive these assumptions from A3 or B2.

Thus the main “phase-resolved LDP” content is conditional on the conclusion it needs.

### 5. The localized zero-free theorem is not implied by a real rate gap

A real LDP gap controls absolute magnitudes on the real source axis. A uniform complex zero-free chart additionally requires a nonvanishing analytic leading contribution with a quantitative lower bound and control of complex cancellations.

The proof invokes a “simple analytic phase contribution” supplied by the platform source theorem. A3 and B2 do not construct such a contribution for a hard basin indicator or its smooth cutoff. Multiplying by `chi_j` can destroy the transfer/cluster eigenstructure, and a real `e^{-gn}` remainder estimate does not by itself provide the complex relative bound needed by Rouché's theorem.

### 6. The boundary label cannot be both arbitrary and analytically negligible

The boundary component is defined as every point outside the `delta`-neighborhoods of the chosen compact components. Its rate may be comparable to an interior phase, may contain additional phases, or may have complicated nonanalytic behavior. Retaining it is correct, but then the finite set `K_1,...,K_J` is not a complete phase classification and the claimed finite component formulas do not close.

### 7. The shell mixture formula needs component-specific target rates

The notation

\[
 w_{n,j}c_{n,j}(a)e^{-nI_j(a)}
\]

treats `a` as though the contraction of the full path rate to the shell were a scalar evaluation. For general vector/thin-shell constraints the exponent is an infimum over the shell in each component, with possible boundary minimizers and different saddle dimensions. Uniform component coefficients are exactly the unproved A2/B1 inputs.

### 8. No independent top-journal theorem remains

The exact positive disintegration is the law of total probability. The pressure formula is finite log-sum-exp. The minimum-rate contraction is the finite-union LDP lemma once component LDPs are assumed. The remaining shell, Gaussian, and dynamic statements import every substantive result from A2–C2.

A synthesis paper can be valuable after the platform theorems exist, but it is not an independent top-four submission in the present state.

## Genuine improvements recognized

The use of measurable positive basins, explicit boundary label, correct single-count pressure convention, and refusal to interpret nonleading Riesz projections as probabilities should all be retained.

## Dependency assessment

D1 is maximally downstream. A2/A3/A4 and B1/B2/B3/B4/C1/C2 remain unproved or false in their current form. D1 cannot close any of them and should not be used as evidence that the series is complete.

## Required reconstruction

Remove D1 as a standalone paper. Once a platform has independently constructed phase components with genuine conditional LDPs and uniform coefficients, a short section can state the exact finite-mixture formulas. Boundary rates must be defined by basin-internal recovery, and nonlinear log-Laplace values must be combined by log-sum-exp rather than by a claimed commutation with phase mixing.

## Recommendation

**Reject; remove as a standalone submission.** The paper's exact decomposition is elementary, the component theorems are assumed, the boundary rate formula is false, and nonlinear dynamic values do not commute with finite mixing as claimed.
