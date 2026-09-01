# Independent Referee Report — Round 14

**Manuscript:** A2 — *Sinai Homological Pressure*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `2994d777b03e5c89464ef9a2e2e062045f09709fafc43778a7bc2f342e9775f1`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 14 correctly restores the four-dimensional Gaussian prefactor and separates the genuinely small, compact, moderate, and very-high Fourier ranges. It also replaces the earlier impossible one-collision winding certificate by a closing construction and treats a symbolic fold through a parent push-forward rather than a Heaviside branch.

The resulting theorem is still not proved. The very-high-frequency estimate contradicts the block length used in its own Dolgopyat argument; the manuscript never decides whether its transfer operator is the collision map or an induced return map; and the claimed lattice-rank and UNI certificates remain geometric narratives rather than verified billiard statements. These are exactly the inputs on which the LLT depends.

## Decisive objections

### 1. The operator and the return-count observable are not typed on one dynamical system

The section starts with the collision map `T_R` and its physical inverse branches. It later twists the same operator by a nonconstant integer return count `r_R`, uses periodic loops with different values of that count, and invokes return branches to a Markov rectangle.

There are two possible interpretations, neither matching the paper:

- For the one-collision map, the collision count per iterate is identically one. Its variance is zero, so the four-dimensional covariance of `(kappa_1,kappa_2,r,tau)` cannot be positive definite.
- For an induced return map, `r_R` is nonconstant and generally unbounded. Then the Banach spaces, exponential multiplier estimates, singularity partitions, displacement/roof tails, and uniform parameter theorem must be constructed for the induced operator, not inherited from the one-step collision map by notation.

No inducing domain, induced kernel, or conjugacy between these two operators is defined. The four-coordinate pressure is therefore not attached to a single specified transfer operator.

### 2. The very-high-frequency `e^{-cn}` factor is incompatible with the stated return-block cost

The UNI proof itself says that accessing a phase-cancellation block at frequency `b` costs

\[
O(\log |b|)
\]

iterates. Hence at most

\[
O\!\left({n\over\log|b|}\right)
\]

independent cancellation blocks fit into `n` iterates. A fixed contraction per block gives at best

\[
\exp\left\{-c{n\over\log|b|}\right\},
\]

not `e^{-cn}`.

Nevertheless the last Fourier range asserts

\[
\|\mathcal L_{\theta+i\omega}^n\|
\le Ce^{-cn}(1+|b|)^{-3}
\qquad (|b|>e^{\kappa\sqrt n}).
\]

The proof says that a “fixed positive fraction” of the remaining returned blocks yields `e^{-cn}`, but a positive fraction of `n/log|b|` blocks still yields only `e^{-cn/log|b|}`. This is an internal scaling contradiction.

A bound of the form

\[
C(1+|b|)^{-3}e^{-cn/\log|b|}
\]

could still be integrable on the indicated tail, but that is not the theorem written and would require a complete nonstationary-phase proof.

### 3. Three integrations by parts on one branch pair are not justified uniformly

Repeated integration by parts requires uniform control of:

- derivatives of the inverse branches and stable holonomies;
- derivatives of the amplitude and all homogeneous cutoffs;
- inverse powers and derivatives of the temporal-distance derivative; and
- boundary terms across every singularity subpartition.

The manuscript only states that one reserved UNI block supplies three integrations and that boundary terms cancel. In billiard anisotropic spaces, the homogeneous partition boundaries and branch-dependent distortion are the central difficulty. No estimate is given that is uniform in `R`, `b`, the central insertion, and the material derivatives.

### 4. The full-lattice-span lemma is asserted rather than constructed

The proof claims six regular periodic loops whose differences of homology/count marks are exactly the three standard basis vectors. It invokes clockwise/counterclockwise circuits, a triangular detour, a shortcut, and a “one-step extension.” This does not establish that the two words in each pair:

- start and finish in the same Markov rectangle;
- have identical connector contributions;
- realize exactly the claimed lattice difference;
- satisfy the reflection equations; and
- stay uniformly away from all other scatterers for every radius in the interval.

The statement that total length is strictly convex on a product of boundary arcs is also not proved and is not a generic fact for arbitrary billiard itineraries. A top-journal arithmetic certificate requires explicit interval geometry or a complete closing lemma with the marks tracked.

### 5. The returned-branch UNI theorem is not established by the symmetry argument

The proof computes a first unequal momentum derivative at one symmetric orbit, appends a common word, and declares all later terms geometrically small. It does not define the return time of the inverse branches, show that the two branches have the same lattice/count marks, or control singularity cuts as the unstable coordinate varies.

Most importantly, a nonzero derivative at one orbit is not a uniform temporal-distance derivative on an entire common interval. The distortion and continuation estimates needed to obtain

\[
\inf_{R,x}|D_R'(x)|>0
\]

are not supplied.

### 6. Parent-fold smoothness in a distribution pairing is not the announced anisotropic bundle theorem

The identity

\[
\langle (\pi_R)_*(J_Rf),\varphi\rangle
=\int J_Rf\,\varphi(y,z^2-(R-R_0))\,dy\,dz
\]

can be smooth for a fixed smooth test. It does not prove `C^q` dependence in the strong billiard anisotropic norm, where the stable curves, homogeneity strips, singularity preimages, trace terms, and admissible test families themselves move with `R`.

The subsequent bundle theorem simply lists uniform finite-horizon constants and invokes a growth lemma. The model-specific moving-singularity estimates that were the main obstacle in earlier rounds remain absent.

### 7. The LLT is conditional on all the missing inputs

The corrected factor

\[
(2\pi n)^{-2}
\]

is dimensionally right. But Fourier inversion only proves the stated local theorem if the complete operator bounds, insertion estimates, aperiodicity, and nondegenerate covariance have already been established. They have not. The LLT proof is therefore a formal final step over unproved packets.

## Dependency assessment

A2 remains the first open gate in the Sinai chain. A3 cannot use its joint roof/count conditioning, A4 cannot use its high-frequency renewal resolvent, and C2/D1 cannot use the resulting phase response as certified input.

## Required reconstruction

A credible paper should first specify one induced collision/return operator and prove, on that operator:

1. the parameter-uniform anisotropic bundle;
2. the exact lattice-mark closing certificate;
3. a returned-branch UNI theorem with interval estimates;
4. a genuinely integrable high-frequency bound with the correct `n/log|b|` block count; and
5. only then the four-dimensional LLT.

## Recommendation

**Reject.** The Gaussian dimension has been repaired, but the model-specific spectral/arithmetic theorem remains a proof sketch and the very-high-frequency estimate contradicts its own block geometry.