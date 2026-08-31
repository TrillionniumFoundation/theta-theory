# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** B1 — Microcanonical Preparation  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `4f8a63c1fa8e3d0f9931ce2bf3f582f9794bf03b4be4fca707780e9ad486d77b`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject.**

## Executive assessment

Round ten retains the correct source-dependent saddle, restricts targets to a relative-interior chart, uses an exact finite-volume centering, and chooses a continuous shell wider than the central-limit scale. These changes remove the earlier fixed-saddle counterexample and the exponentially thin-shell pathology.

The new Fourier theorem is nevertheless incomplete. Its three cases leave an entire compact nonzero frequency region uncontrolled, and its large-frequency polynomial bound is independent of the large-deviation speed and therefore cannot imply the claimed \(\mu_\varepsilon^{-1/2}\) sharp coefficient. More fundamentally, the good-block argument assumes a conditional regenerative independence that is not available under a dynamical path/contact tilt of the hard-sphere system. The microcanonical transfer remains unproved.

## Major mathematical objections

### 1. The characteristic-function theorem omits a whole frequency region

The three displayed cases cover:

1. \(|t|+|u|\le\delta\);
2. \(\delta\le|t|\le\pi\) and \(|u|\le R\); and
3. \(|u|>R\).

They do not cover, for example,

\[
t=0,\qquad \delta<|u|\le R.
\]

This compact continuous-frequency annulus is exactly where a nonlattice spectral gap or aperiodicity estimate is needed. No bound is stated, and the proof's number-lattice factor does nothing when \(t=0\). Fourier inversion for the mixed local coefficient therefore has an uncontrolled region of positive volume.

### 2. The polynomial high-frequency tail is too weak for a sharp local coefficient

For \(|u|>R\), the theorem gives

\[
|\varphi_\varepsilon(t,u)|
\le e^{-c\mu_\varepsilon}+C_s(1+|u|)^{-s}.
\]

The second term has no \(\mu_\varepsilon\)-decay. Integrating it over the fixed tail \(|u|>R\) gives a constant depending on \(R\), not an error of order \(o(\mu_\varepsilon^{-1/2})\). The desired exact-number coefficient is itself only of order \(\mu_\varepsilon^{-1/2}\), so a fixed small Fourier tail is not enough.

One would need a bound exploiting linearly many good blocks—such as an exponentially small annular factor or a polynomial order growing with \(\mu_\varepsilon\)—together with uniform constants on a growing frequency cutoff. The proof explicitly uses only a fixed number of smoothing blocks and loses the needed speed dependence.

### 3. Dynamical path/contact tilts do not yield conditionally independent good blocks

The argument partitions the initial configuration into separated spatial cells and treats good-block contributions as conditionally independent after fixing the exterior. Hard-core exclusion is local at time zero, but the source \(H\) depends on future particle paths and actual contacts. Particles initially in different cells can later collide directly or through a collision genealogy, and unbounded velocities prevent a fixed spatial separation from shielding their histories.

A convergent static polymer correction does not prove independence, or even the factorization needed for repeated convolution, under the full dynamical source. The manuscript must derive a source-uniform decoupling theorem from the real-trajectory cluster expansion. It currently assumes the regenerative structure that the hard-sphere analysis is supposed to establish.

### 4. The typical-sector covariance proof is not quantitative enough

The proof claims \(c\mu_\varepsilon\) mutually separated insertion cells with occupancy probabilities uniformly bounded away from zero and one on the full source chart. Cell volume, separation scale, velocity patch, and source-dependent insertion energy are not specified. In Boltzmann–Grad scaling these quantities are delicate: cells of diameter comparable with the hard-core radius have activity tending to zero, while larger cells are not automatically independent under the dynamic tilt.

The lower covariance bound may be true on a sufficiently small source/time chart, but no theorem proves it with the declared uniformity.

### 5. The shell coefficient is asserted beyond the proved Fourier input

The shell width

\[
\delta_\varepsilon\downarrow0,
\qquad
\sqrt{\mu_\varepsilon}\delta_\varepsilon\to\infty
\]

is a sensible intensive-window regime. At the exact saddle its continuous Gaussian mass tends to one, leaving the exact-number coefficient. But that conclusion requires a uniform local limit theorem whose intermediate and high-frequency errors are \(o(\mu_\varepsilon^{-1/2})\). The current characteristic theorem does not provide such errors.

Smoothing upper and lower approximations of a shrinking box also requires uniform control of their Fourier norms and boundary errors; none is tracked.

### 6. The final transfer to the B2 source class is circular at the analytic level

The main theorem says it applies jointly to B2 particle and actual-contact sources. Yet the good-block and connected-pressure estimates needed here are precisely part of B2's unproved grand-canonical marked expansion. The dependency ledger may order B2-GC before B1, but the B1 proof does not cite or reproduce a theorem with the required complex-frequency and conditional-block bounds.

### 7. The valid variational formula does not rescue the missing coefficient

The source-dependent expression

\[
Q(H,\lambda_{H,a})-\lambda_{H,a}\cdot a
-Q(0,\lambda_{0,a})+\lambda_{0,a}\cdot a
\]

is the right candidate. It follows from shell conditioning only after numerator and denominator coefficients are established uniformly. A correct candidate formula is not itself a proof of ensemble transfer.

## Dependency and editorial assessment

B1 is the bridge from the grand-canonical hard-sphere theory to B2-MC, B3, B4, C1, and D1. Until the full source-uniform mixed local theorem is proved, those downstream microcanonical statements remain conditional.

A viable submission would isolate and prove one sharp coefficient theorem for the actual tilted hard-sphere partition function, including all compact and high Fourier ranges. The present paper states that theorem without the necessary dynamical decoupling.

## Recommendation

**Reject.** The fixed-saddle error is repaired, but the replacement characteristic estimate has an explicit coverage gap and insufficient high-frequency decay. The source-uniform hard-sphere shell coefficient—the paper's main theorem—remains unproved.
