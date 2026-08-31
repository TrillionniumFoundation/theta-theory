# Independent Referee Report — Round 12

**Manuscript:** C1 — *Information and Risk-Sensitive Saddles*  
**Reviewed branch:** `revision/round12-referee-positive-closure-11paper-2026-08-31`  
**Reviewed commit:** `10b553a750b3ba3f82c751e699446ed40db80d62`  
**Controlling module:** `ROUND12_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `44564b80b77d9b7dc336c23e59e5b2bcdc3e8974984c88a93621b816d3543a3b`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 12 makes the correct conceptual separation between positive posterior measures and oriented geometric currents, uses Rokhlin/coarea disintegration rather than pairing a positive-dimensional current with the scalar one, and explicitly adds a zero-evidence direction. Those are genuine improvements.

The reduced-game theorem is nevertheless false under the stated “reachable analytic class.” Matching finitely many cumulants does not make two probability laws close in Wasserstein distance, even when both moment-generating functions are entire and uniformly bounded on a fixed complex ball. Analyticity makes the full infinite cumulant sequence determining; it does not make a fixed finite truncation asymptotically sufficient. The paper supplies no \(\mu_\varepsilon\)-dependent decay of omitted cumulants in the definition of the class. The Feller disintegration and strategy-uniform Bernstein–von Mises theorem also require substantial hypotheses not provided, and the coefficient theorem inherits B1's false Fourier tail.

## Decisive objections

### 1. Finitely many cumulants do not determine a law up to \(o(1)\)

Lemma 4.1 claims that, on a class whose factorial cumulant generating functional is analytic on a fixed radius and bounded by \(M\), matching a finite list \(\kappa_{\rm fin}\) yields a coupling with weighted Wasserstein error \(o(1)\).

This is false. Already if only the first moment is retained,

\[
\mu_1=\tfrac12\delta_{-1}+\tfrac12\delta_1,
\qquad
\mu_2=\delta_0
\]

have the same mean, entire moment-generating functions, and uniformly bounded analytic norms on every fixed ball, but

\[
W_1(\mu_1,\mu_2)=1.
\]

More generally, for every fixed \(K\), the truncated moment problem supplies distinct compactly supported probability measures with the same first \(K\) moments and positive Wasserstein separation. Their moment-generating functions are entire.

Cauchy estimates give bounds on higher cumulants; they do not make the omitted tail tend to zero as \(\varepsilon\to0\). The definition of \(\mathfrak R_\varepsilon(r_*,M)\) contains no scaling such as

\[
|\kappa_j|\le C^j\mu_\varepsilon^{1-j}
\]

that would force higher correlations to vanish. Thus the claimed finite-coordinate reduction is not a consequence of analyticity.

### 2. “Moment determining” is not a quantitative truncation theorem

The proof says exponential moment tightness makes the cumulants moment determining and then bounds the discrepancy by the tail of an absolutely convergent series. Moment determination uses the **entire infinite sequence**. For a fixed analytic radius, the tail after a fixed truncation is merely bounded by a geometric quantity depending on the truncation order; it is not \(o(1)\) unless that order tends to infinity or the cumulants themselves vanish with \(\mu_\varepsilon\).

The theorem keeps a finite list and claims a limit as \(\varepsilon\to0\), so the conclusion does not follow.

### 3. The reduced DPP depends entirely on the false coupling lemma

The Bellman error estimate is valid only after one has a one-step transition coupling with \(o(1)\) error. Since Lemma 4.1 does not provide it, the statement that a finite density/contact/phase state approximates the full posterior law is unproved.

The exact full-belief DPP may be meaningful; the finite-dimensional reduction is a separate theorem and is presently absent.

### 4. Integrated disintegration continuity does not give a Feller posterior kernel

Weak continuity of the joint positive measure and the integrated coarea identity do not imply continuity of the map

\[
(\text{prior},y)\mapsto\nu_{O,y}
\]

into posterior probability measures. Regular conditional probabilities can jump when fiber topology changes or when densities vanish, even if the integrated joint law varies continuously.

The manuscript explicitly says pointwise continuity of an individual fiber is not asserted, but then concludes that the posterior-valued prediction–observation kernel is Feller. For a payoff that is nonlinear in the posterior, integrated continuity of the unnormalized law is insufficient. Stronger uniform density, transversality, and denominator hypotheses are required on each stratum.

### 5. The zero-evidence blow-up does not by itself make the update unique

The state \([0,1]\times\mathcal K_M\) records a direction \(\nu\) at \(r=0\), which is the correct issue to retain. But after prediction and slicing, a zero-mass slice can have several projective subsequential directions depending on how the observation value and prior approach the boundary. The proof says “divide before taking the limit” and declares uniqueness; compactness gives subsequences, not uniqueness.

A well-defined boundary kernel requires a specified tangent/disintegration rule or a set-valued boundary transition.

### 6. The inserted coefficient inherits B1's false high-frequency theorem

C1 invokes B1's “compact-annulus and high-frequency pressure gaps” for the enlarged observation vector. Round 12 B1's speed-dependent power tail is contradicted by the compound-Poisson empty-sector atom. Therefore the claimed relative local coefficient, zero-free denominator, and posterior ratio theorem are not available.

Rouché's theorem cannot be invoked until a uniform complex relative approximation has actually been proved.

### 7. Uniform LAN over all admissible strategies is not implied by one information matrix

The theorem assumes a nonsingular information matrix at \(\vartheta_0\) and then claims LAN uniformly over admissible strategies. An adaptive controller can choose an observation/control sequence with little or no information about \(\vartheta\), making the accumulated information singular or random.

Uniform LAN requires a strategy-uniform lower information bound, predictable design convergence, and a uniform likelihood expansion. None is stated. A single regular phase information matrix does not cover all strategies.

### 8. The Bernstein–von Mises conclusion is too strong at the declared boundary

Total-variation BvM under adaptive, risk-sensitive, exact observations requires local asymptotic normality, posterior tightness, identifiability, prior regularity, and control of model misspecification/phase switching uniformly under the random design. The proof delegates all of this to an “observation LDP” and B3. B3's joint contact covariance is incorrectly typed, and no global observation LDP has been proved.

## Genuine improvements recognized

The following Round 12 choices should be retained:

- positive disintegration measures separated from oriented currents;
- explicit critical-rank strata;
- a projective zero-evidence direction;
- separate numerator and denominator saddles;
- exact full-belief control before any reduction; and
- restriction of BvM to identifiable regular phases away from coexistence.

## Required reconstruction

The exact filtering state should be completed first, with a proved Feller theorem for a restricted smooth observation model. Any reduced state must include either an increasing cumulant order or an explicit quantitative chaos estimate with \(\mu_\varepsilon\)-vanishing higher cumulants. Strategy-uniform LAN must be restricted to designs satisfying a uniform information condition. The local coefficient cannot be used until B1 is repaired.

## Recommendation

**Reject.** The exact-state architecture is improved, but the central finite-correlation reduction is contradicted by elementary moment-problem examples. The Feller, coefficient, LAN, and BvM interfaces also remain unproved or inherit false upstream theorems.