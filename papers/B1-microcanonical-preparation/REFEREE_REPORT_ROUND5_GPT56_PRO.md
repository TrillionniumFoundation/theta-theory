# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B1 — *Microcanonical Preparation and Exponential-Scale Ensemble Transfer for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `5877d3aaa6cf21562b461521fcc64c7d46177465`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/B1_FINITE_SADDLE_MIXED_LLT.tex`, blob `cc7d82f904070f3ae6176a15dfb1c366bc7a2a22`

## Source-control verdict

The active B1 paper is unchanged from round four and still performs local coefficient extraction at the limiting saddle rather than at an exact finite-volume saddle. No convergence rate places the finite mean inside the shrinking shell, so the central coefficient theorem remains unproved.

The round-five candidate correctly changes to an exact finite-volume source-dependent saddle. That is the right repair and removes the previous moderate-deviation centering objection at the formal level. The packet is not materialized, and its mixed lattice–continuous local-limit proof contains unresolved probabilistic and cluster-expansion gaps.

## Audit of the proposed round-five replacement

### 1. The `m0`-particle singleton block is not a demonstrated term of the connected logarithm

The proof obtains a four-dimensional smooth momentum–energy density by grouping `m0=5` independent singleton velocities and then treats its Fourier transform as a negative real contribution to the normalized connected log characteristic function.

In a grand-canonical logarithm, the one-label connected sector is a compound-Poisson exponent. Five independent singleton particles are not a new connected cluster term which may simply be added to the logarithm. Their convolution appears only after expanding the exponential of the one-particle activity, with particle-number combinatorics and hard-core corrections that must be tracked.

A correct proof may exploit the compound-Poisson singleton component to obtain smoothing after sufficiently many jumps, but it must derive the characteristic function decomposition and coefficient bounds explicitly. The packet currently inserts the `m0` block without that derivation.

### 2. The asserted uniform mixed Cramér estimate is not proved

The theorem requires a gap on every compact frequency set away from `(0,0)` and arbitrary-order decay in the unbounded continuous frequencies, uniformly in the dynamic path/contact source. The argument cites three integrations by parts and then says that increasing the block size gives every fixed order. It does not establish:

- smoothness of the finite-volume tilted density under a path-dependent source;
- boundary behavior at the energy cone `e=|p|^2/m0`;
- uniform derivatives after hard-core and dynamic cluster corrections;
- control of mixed number/energy resonances; or
- an integrable Fourier majorant uniform in the source and in `epsilon`.

These estimates are the substance of the mixed lattice/nonlattice local limit theorem, not a routine corollary of coarea.

### 3. Uniform strict convexity is conditional on the unproved B2 pressure

The packet splits the Hessian into a singleton sector and a connected remainder of order `T`. The dynamic pressure, its complex derivatives, and the uniform remainder bound are supplied only by the proposed B2 theorem, which itself is not established. B1 therefore cannot be treated as an independent preparation theorem.

Moreover, the assertion that the mixed number–momentum–energy covariance is uniformly positive over the complete compact source set requires an explicit constraint-rank hypothesis and a proof that no dynamic tilt drives the relevant singleton activity to the boundary. These conditions are described informally rather than stated as theorem hypotheses.

### 4. Existence of the exact finite saddle requires a finite-volume mean-image theorem

Uniform positivity of the Hessian gives local injectivity. It does not by itself show that every compatible target `a_epsilon` lies in the image of the finite-volume gradient on the chosen multiplier chart. A boundary margin and a quantitative convergence of the finite gradient map are needed. The packet asserts existence before proving this range condition.

### 5. The shell coefficient treats a source-uniform shrinking family without quantitative smoothing bounds

Even when centered at the exact saddle, a uniform asymptotic

\[
\mathbb P\{N=N_\varepsilon,\ Y-\mathbb EY\in\mu_\varepsilon B_\varepsilon\}
=\mu_\varepsilon^{-1/2}(c_H+o(1))
\]

requires uniform control of the shape, boundary regularity, and rate at which the continuous shell shrinks. The condition `sqrt(mu_epsilon) delta_epsilon -> infinity` makes its Gaussian mass tend to one, but it does not by itself control Fourier approximation errors for arbitrary rectangular or “smooth” shells uniformly over all sources and targets.

### 6. The microcanonical initial LDP is asserted too quickly

The candidate concludes a full good initial empirical-measure LDP from the finite-dimensional shell coefficient and a conditional Laplace principle. One still needs exponential tightness in the selected empirical-measure topology and a separating global source class. The B2 local source chart is not automatically sufficient for the full initial rate.

### 7. The final formula is nevertheless the correct candidate

The source-dependent pressure

\[
Q^a(H)=
\inf_\lambda\{Q(H,\lambda)-\lambda\cdot a\}
-
\inf_\lambda\{Q(0,\lambda)-\lambda\cdot a\}
\]

and its Schur-complement Hessian are the correct formal objects. The old time-zero counterexample no longer attacks this formula. The present issue is proof, not the variational candidate.

## Required reconstruction

B1 should be rebuilt around an explicit finite-volume compound-Poisson/hard-core characteristic-function theorem, with the exact saddle and mean-image condition stated quantitatively. The mixed LLT must be proved independently of suggestive block language, and the source class and shell geometry must be fixed precisely. Only then should the conditional empirical-measure LDP be deduced.

## Recommendation

**Reject.** The active paper remains centered at the wrong saddle. The unmaterialized candidate makes the essential conceptual correction, but its mixed local-limit theorem relies on an unproved `m0` singleton-block decomposition, unverified uniform Fourier estimates, and the unresolved B2 grand-canonical pressure.