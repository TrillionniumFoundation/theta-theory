# Round-Six Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B1 — *Microcanonical Preparation and Exponential-Scale Ensemble Transfer for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round6-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `fb2ccfafab262f31f5b6f960df23e31258a59223`  
**Reviewed tree:** `2d3992ea12cfd513359a5f204bb1c2ae027bc7c4`  
**Active controlling module:** `ROUND6_POSITIVE_CLOSURE.tex`, blob `cdc6f6e9d7a8b59a9afa4fe42914fce81def7ce9`

## Editorial summary

The exact finite-volume saddle is the right centering, and separating the singleton compound-Poisson exponent from the connected logarithm is conceptually superior to inserting an independent smoothing block. The revision therefore addresses the most obvious error of the previous candidate.

The replacement mixed local-limit theorem is nevertheless false as stated. The one-particle momentum–energy mark is supported on a paraboloid and cannot have the full-dimensional density assumed in (C2). The compound-Poisson law retains an empty-configuration atom, so its characteristic function cannot satisfy a pure polynomial bound tending to zero at large continuous frequency. There is also a dimensional inconsistency in the shell center and width. These failures invalidate the coefficient theorem and all source-dependent microcanonical transfers built from it.

## Major mathematical objections

### 1. Condition (C2) is impossible for the declared physical momentum–energy constraints

The continuous part of the singleton mark contains

\[
(v,|v|^2/2)\in\mathbb R^3\times\mathbb R.
\]

For one particle this vector lies on the three-dimensional paraboloid

\[
e=|p|^2/2
\]

inside four-dimensional momentum–energy space. Its pushforward is singular with respect to four-dimensional Lebesgue measure; it cannot have a `C^{d+4}` density on an open subset of the full continuous constraint space.

Adding further marks `chi_j(x,v)` does not repair this. If the full continuous singleton vector had a Lebesgue density, its projection onto `(v,|v|^2/2)` would be absolutely continuous, contradicting the paraboloid support. The manuscript's own phrase “after conditioning on number” does not change the one-particle geometry.

The required smoothing arises only from convolution powers involving sufficiently many particles. That is compatible with the compound-Poisson strategy, but it is not condition (C2), and the covariance/Cramér proofs repeatedly use full-dimensional singleton patches. The hypotheses are therefore not satisfied by the model the paper claims to treat.

### 2. The large-frequency bound contradicts the compound-Poisson atom

The exact singleton factor is

\[
\exp\{\mu_\varepsilon\mathfrak p_{1,\varepsilon}(t,u)\}
=e^{-\mu_\varepsilon a_1}
\sum_{n\ge0}\frac{\mu_\varepsilon^n}{n!}
\widehat a(t,u)^n.
\]

The term `n=0` is the empty compound-Poisson configuration and equals

\[
e^{-\mu_\varepsilon a_1}>0.
\]

As `|u|` tends to infinity, the Fourier transforms of absolutely continuous positive-particle sectors may vanish, but this atom remains. The full grand-canonical law likewise has positive mass at the empty configuration, so its joint continuous characteristic function cannot tend to zero for fixed `epsilon`.

`thm:r6-b1-characteristic` instead asserts, for all sufficiently large `|u|`,

\[
|\varphi_\varepsilon(t,u)|
\le C_M(1+\sqrt{\mu_\varepsilon}|u|)^{-M},
\]

whose right side tends to zero. This is an explicit contradiction. The correct type of estimate must contain an additional exponentially small term, for example

\[
e^{-c\mu_\varepsilon}+
C_M(1+\sqrt{\mu_\varepsilon}|u|)^{-M},
\]

and must track every discrete/atomic particle sector. The previous round already used such a two-term form; round six has incorrectly removed the necessary atom.

### 3. Small convolution powers cannot be “handled directly” in the claimed integrable majorant

Even after restoring the empty-sector term, the proof says that a convolution power of order at least `d+4` is smooth and that “the finitely many smaller powers are handled directly.” Smaller powers of the momentum–energy surface measure remain singular on lower-dimensional convolution surfaces. Their Fourier transforms need not have an integrable polynomial majorant of arbitrary order.

They can only be separated as finitely many exponentially small Poisson sectors, with their total weights estimated before Fourier integration, or treated by an explicit oscillatory-integral theorem. The manuscript does neither. Exponentiating the singleton activity does not automatically turn every sector into a smooth density.

### 4. The connected remainder estimate is not uniform at unbounded frequency

The lemma provides only

\[
|\partial_\theta^j\mathfrak r_\varepsilon|
\le C(T+\varepsilon),\qquad j\le4,
\]

on the declared source/multiplier sets. A bounded complex factor with four derivatives is not “absorbed by convolution” into arbitrary-order Fourier decay. Multiplying a decaying characteristic function by `exp{mu r(t,u)}` may also amplify the high-frequency region unless a uniform negative real-part estimate is supplied.

The statement that the connected remainder is smaller than the singleton gap works on a fixed compact minor arc. It does not control all `|u|>=C`, where the singleton real-part gap may approach the atom level and derivatives of dynamic marks can grow. The high-frequency portion of the mixed inversion is therefore not proved.

### 5. The shell theorem is dimensionally inconsistent

Earlier, `a_epsilon` is defined as the normalized mean because

\[
D_\lambda Q_\varepsilon
=\mu_\varepsilon^{-1}
\mathbb E\sum_i C(z_i).
\]

The continuous total `Y` is extensive, of order `mu_epsilon`. Nevertheless `thm:r6-b1-coefficient` states the event

\[
Y-a_\varepsilon'\in\delta_\varepsilon B,
\]

with `delta_epsilon` tending to zero. If `a_epsilon'` is the normalized target used in the saddle equation, the center should be `mu_epsilon a_epsilon'`. If `Y` has silently been renormalized by `mu_epsilon`, that definition is missing and the Fourier scaling in the proof changes.

The assertion that the shell contains an increasing number of standard deviations corresponds to an extensive shell of width `mu_epsilon delta_epsilon`, or a normalized shell of width `delta_epsilon`, not to the event as written for an extensive `Y`. In the literal statement, a shrinking width around an order-one center cannot have probability `mu_epsilon^{-1/2}` under an order-`mu_epsilon` total.

This scaling error propagates to the exact change-of-measure formula, where the multiplier term and shell center are used interchangeably.

### 6. Uniform strict convexity is not proved from the stated singleton geometry

The Schur-complement argument says that conditional-on-number continuous covariance is positive by (C2). Since (C2) fails for momentum–energy, the proof does not establish a uniform lower Hessian bound for the actual five physical constraints.

One can obtain positive covariance from sectors containing sufficiently many particles, but then the proof must quantify their activity uniformly under every source-dependent finite saddle and show that the connected correction cannot cancel the resulting block. That compound-sector calculation is absent. It is not enough to cite spanning “activity patches” of a nonexistent singleton density.

### 7. The finite-volume mean-image argument assumes more convergence than B2 supplies

The saddle theorem invokes uniform convergence of finite gradients and a global diffeomorphism of a compact multiplier chart. B2, even on its own terms, claims local analytic convergence on bounded source balls; it does not establish global injectivity or properness of the constraint gradient over a chart large enough to contain every target and every source-dependent saddle.

A uniform Hessian lower bound would give local injectivity, but existence for all target points requires boundary-degree or coercivity estimates. The sentence that the limiting gradient maps the chart diffeomorphically onto an open set is an additional hypothesis, not a consequence proved in this paper.

### 8. The prepared LDP does not follow from a separating bounded source class alone

The final paragraph invokes a conditional Laplace principle on bounded time-zero cylinders plus a “small quadratic velocity chart” and concludes a good empirical-measure LDP. A full lower bound and exponential tightness on the microcanonical constraint surface require a precise topology, an exposed-point or entropy approximation theorem, and uniform shell transfer for the approximating sources. None is stated. This conclusion also depends on the invalid mixed coefficient theorem.

## Dependency consequences

B2-MC explicitly uses B1 for every bounded density/contact source. B3 uses the B1 constrained covariance; B4, C1, C2, and D1 then inherit that preparation. Until the actual mixed characteristic estimate and shell coefficient are proved, the hard-sphere chain stops at grand-canonical B2 even if B2 itself were otherwise valid.

## Required reconstruction

A viable revision must:

1. formulate the nondegeneracy condition on a sufficiently high compound-Poisson convolution sector, not on one singleton momentum–energy mark;
2. retain and estimate every atomic/small-particle sector, including an explicit `e^{-c mu}` term at large frequency;
3. prove high-frequency estimates for the connected factor rather than claiming arbitrary decay from four derivatives;
4. define normalized versus extensive constraints consistently and restate the shell at the correct scale;
5. prove uniform covariance and mean-image coverage at the exact finite saddle; and
6. establish the prepared initial LDP in a declared topology with an actual lower-bound argument.

## Recommendation

**Reject.** The revision adopts the correct finite-saddle and compound-Poisson architecture, but its hypotheses do not hold for the physical momentum–energy singleton, its characteristic bound is contradicted by the empty-sector atom, and its shell statement is dimensionally inconsistent. The microcanonical coefficient and all downstream prepared results are therefore unproved.