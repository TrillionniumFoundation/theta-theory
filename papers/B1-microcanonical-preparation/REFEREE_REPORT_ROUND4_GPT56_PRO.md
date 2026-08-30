# Round-Four Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B1 — *Microcanonical Preparation and Exponential-Scale Ensemble Transfer for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round4-referee-positive-closure-11paper-2026-08-30@cbee394d6ee33db471b63420131314bd05909a0f`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `5877d3aaa6cf21562b461521fcc64c7d46177465`

## Overall assessment

The revision has corrected the principal conceptual error identified in the earlier reports. The microcanonical pressure is now expressed through a source-dependent saddle `lambda_H`, and the time-zero source test gives the required exact value. This is a real and important improvement.

The coefficient-extraction theorem which is used to justify the saddle formula is nevertheless not proved. The Fourier expansion is centered at the limiting saddle rather than the finite-volume exact saddle, and no convergence rate is supplied which would keep the finite mean inside the shrinking central window. Several nonlattice and covariance hypotheses are also stronger than the assumptions stated. Since B1 is the preparation bridge for B2--B4, these gaps remain load bearing.

## Major objections

### 1. The shell coefficient is centered at the wrong finite-volume mean

The limiting saddle is defined by

\[
D_\lambda Q(H,\lambda_H)=a.
\]

The finite-volume law used in the coefficient theorem has mean

\[
D_\lambda Q_\varepsilon(H,\lambda_H),
\]

which need not equal `a`. Local uniform convergence of the pressure and its derivatives gives only

\[
D_\lambda Q_\varepsilon(H,\lambda_H)-a\to0.
\]

For the local coefficient

\[
\mathbb P_{H,\lambda_H,\varepsilon}
\{N=N_\varepsilon,\ |Y-a'|\le\delta_\varepsilon\}
\]

to have the claimed central asymptotic, one needs the finite mean mismatch to satisfy at least

\[
\sqrt{\mu_\varepsilon}\,
\big|D_\lambda Q_\varepsilon(H,\lambda_H)-a\big|
=o(1)
\]

in the lattice direction, and a compatible bound relative to the continuous shell width. No such rate is proved.

A convergence error of size `epsilon^alpha` with `alpha<1` would be harmless at pressure scale but becomes a diverging moderate-deviation displacement after multiplication by `sqrt(mu_epsilon)=epsilon^{-1}`. The exact-number coefficient would then contain a nontrivial or exponentially small factor, not `mu_epsilon^{-1/2}(c_H+o(1))`.

The standard repair is to define a finite-volume saddle

\[
D_\lambda Q_\varepsilon(H,\lambda_{H,\varepsilon})=a_\varepsilon
\]

and prove `lambda_{H,epsilon}->lambda_H`, or to establish an explicit derivative convergence rate. The manuscript does neither.

### 2. The continuous shell may not be centered under the chosen tilted law

The proof says that the continuous shell contains a number of Gaussian standard deviations tending to infinity. This is true only if its center differs from the finite-volume tilted mean by `o(delta_epsilon)`. Again, the limiting saddle equation supplies no such finite-volume estimate.

The argument therefore cannot conclude that the continuous Gaussian factor tends to one uniformly over source and target sets.

### 3. The covariance lower-bound proof mishandles the particle-number coordinate

The constraint vector includes the constant coordinate `1`. The proof says that finitely many patches make the *centered* vectors of `C` span all of `R^d`. The centered constant coordinate is identically zero, so that statement is impossible.

A grand-canonical Poisson/number fluctuation can indeed make the full uncentered constraint covariance nondegenerate, but it must be proved through the joint activity Hessian. The argument needs a block decomposition separating number activity from conditional mark covariance. As written, the claimed singleton covariance lower bound does not follow.

### 4. Arbitrary bounded `C^1` constraints do not give the asserted Fourier decay

The high continuous-frequency estimate assumes that, for every direction `u`, one constraint combination has a derivative bounded away from zero on a patch, allowing repeated integration by parts. Linear independence modulo the conserved quantities does not imply such a submersion/nonstationary-phase condition.

A smooth random vector may be nondegenerate in covariance while its distribution is supported on a lower-dimensional curved image or has critical points in every projection. Repeated polynomial Fourier decay requires explicit regularity and nonlattice hypotheses on the push-forward density of the constraint map. These are not stated.

The joint lattice--continuous local coefficient theorem therefore has missing assumptions even apart from the centering error.

### 5. The minor-arc dominance is not uniform near mixed resonances

The singleton number sector gives a strong gap when the number frequency stays away from zero. For `t` near zero but the continuous frequency outside the central region, the proof relies on the unproved integration-by-parts argument. It does not exclude mixed arithmetic resonances of `(N,Y)` or show a uniform Cramér condition on the complete compact frequency set.

A valid mixed local limit theorem must identify the exact lattice subgroup and prove nonlattice behavior of every nonlattice linear combination.

### 6. The source-dependent saddle formula depends on the unproved coefficient

The variational expression

\[
Q^{\rm mc,a}(H)
=
\inf_\lambda\{Q(H,\lambda)-\lambda\cdot a\}
-
\inf_\lambda\{Q(0,\lambda)-\lambda\cdot a\}
\]

is the correct candidate. The change-of-measure proof, however, uses the shell coefficient at `lambda_H`. Since that coefficient has not been established, the theorem is not yet proved.

The time-zero test checks internal consistency of the candidate formula; it does not prove coefficient extraction from the microscopic shell.

### 7. The initial LDP is asserted from the same incomplete argument

The constrained initial rate follows from a conditional LDP only after verifying the exact conditioning exponent and exponential tightness in the chosen empirical-measure topology. The proof simply refers back to “the same source-dependent conditioning argument.” It does not construct the full initial pressure domain or establish the lower bound for arbitrary constrained empirical measures.

### 8. B1 remains dependent on B2-GC

The derivative bounds, complex pressure, and all-contact sources are imported from B2's grand-canonical marked expansion. That expansion is not established in the present series. The new logical ordering removes circularity, but it does not discharge the upstream theorem.

## Status of the previous decisive counterexample

The old fixed-saddle theorem is no longer the active statement. The source-dependent formula passes the exact time-zero test and conceptually closes that objection. This should be recognized.

The present rejection rests on a different issue: the manuscript has not justified extracting a shrinking mixed lattice/continuous shell coefficient uniformly at the source-dependent saddle.

## Minimum viable reconstruction

A rigorous version should:

1. construct `lambda_{H,epsilon}` solving the finite-volume mean equation;
2. prove uniform convergence and interiority of these saddles;
3. state explicit lattice-span and multivariate nonlattice hypotheses for the constraint vector;
4. prove a uniform mixed local central limit theorem at the finite saddle;
5. track the actual shell widths relative to all finite-volume mean errors; and
6. then derive the constrained pressure and initial rate.

## Recommendation

**Reject.** The revision fixes the central variational formula, but the microscopic shell coefficient on which that formula rests is not proved and is centered incorrectly at finite volume.