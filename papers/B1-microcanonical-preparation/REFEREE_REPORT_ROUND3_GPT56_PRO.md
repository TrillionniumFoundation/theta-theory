# Round-Three Referee Report — GPT-5.6 Pro

**Manuscript:** B1 — *Microcanonical Preparation and Exponential-Scale Ensemble Transfer for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round3-full-positive-closure-11paper-2026-08-30@6a31720e5b0b6ab156b575f947596f9b66f56efe`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `696fdba46f585eb836bd8291e786e6647a850dbb`

## Executive assessment

This paper contains the clearest genuine correction in the round-three hard-sphere series. The fixed zero-source information projection has been replaced by a source-dependent constrained saddle

\[
Q^{\rm mc,a}(H)
=
\inf_\lambda\{Q(H,\lambda)-\lambda\cdot a\}
-
\inf_\lambda\{Q(0,\lambda)-\lambda\cdot a\},
\]

and the manuscript verifies the time-zero constraint source formally. This is the correct variational structure and removes the explicit counterexample that invalidated the previous version.

The theorem is nevertheless not proved. Its joint lattice/continuous coefficient estimate rests on a safe-box characteristic-function argument with the wrong Boltzmann–Grad scaling. A cube of side `L epsilon` has one-particle activity of order `mu epsilon^3 = epsilon`, not order one. The contraction accumulated over the number of safe cubes used in the proof is therefore too weak by a factor of `epsilon^{-1}`. The uniform local coefficient theorem, on which the entire source-dependent shell transfer depends, does not follow.

The paper also relies on B2’s grand-canonical all-contact pressure, which is not established in the controlling B2 manuscript. Thus B1 has corrected its target theorem but has not supplied the required coefficient extraction.

## Improvements relative to the preceding circulation

1. The source multiplier is reoptimized at every path/collision source.
2. The time-zero source identity now has the correct value `eta·a`.
3. The initial constrained rate is no longer collapsed to zero/infinity at one density; it retains the full grand-canonical rate on the constraint surface.
4. The prepared covariance is correctly identified as a Schur complement.
5. The B1/B2 construction order is made noncircular at the level of intended dependencies: B2 grand-canonical pressure first, B1 conditioning second, B2 microcanonical LDP third.

These are substantial conceptual repairs and should be preserved.

## Major mathematical objections

### 1. The particle-number characteristic gap has the wrong safe-box scaling

The proof partitions the unit torus into cubes of side `L epsilon`. There are of order

\[
\epsilon^{-3}
\]

such cubes. At Boltzmann–Grad activity

\[
\mu_\epsilon=\epsilon^{-2},
\]

the expected one-particle activity in one insertion subcube of volume `O(epsilon^3)` is

\[
z_B=O(\mu_\epsilon\epsilon^3)=O(\epsilon),
\]

not a quantity bounded below by a positive constant.

Accordingly,

\[
\frac{|1+z_Be^{it}|}{1+z_B}
=1-O(\epsilon)\sin^2(t/2),
\]

rather than `1-c sin²(t/2)`. The active proof then says that using `c mu_epsilon` disjoint safe choices gives an exponential gap `e^{-c mu_epsilon}`. With the actual local activity, `mu_epsilon` choices yield only

\[
\exp\{-c\mu_\epsilon\epsilon\}
=
\exp\{-c\epsilon^{-1}\},
\]

which is subexponential at the claimed speed `mu_epsilon=epsilon^{-2}`.

A potentially viable argument would have to exploit order `epsilon^{-3}` separated insertion cells, with a rigorous conditional factorization or cluster estimate over that much larger family. The current proof does not do so.

### 2. The separate “span-one” repair is not incorporated and repeats the same issue

The repository contains

```text
revision/round3-rereview/B1_B3_NULLSPACE_PACKET.tex
```

whose B1 lemma asserts that the local one-particle weight in each mesoscopic safe region satisfies `c <= z_B <= C`. At the declared cube scale this is again incompatible with `mu_epsilon epsilon^3 = epsilon`. The file is not included in the controlling manuscript in any case.

Thus the internal hostile-audit blocker has neither been materialized nor mathematically resolved.

### 3. The continuous-frequency estimate is only a heuristic

The proof conditions on all particles but one, integrates by parts in a spanning box, and then says that repeating this over a positive fraction of safe boxes gives arbitrary polynomial decay. For an interacting hard-core trajectory tilt, the conditional one-particle factors are not shown to be independent, their densities and derivatives are not bounded uniformly after the path/collision source is introduced, and the direction-dependent spanning boxes are not assembled into a uniform nonstationary-phase theorem.

A joint lattice/continuous local central limit theorem requires a complete Fourier decomposition, uniform complex-pressure control, a central Gaussian expansion, and quantitative minor-arc bounds. None is supplied by the short safe-box paragraph.

### 4. Uniform strict constraint convexity under dynamic tilts is not proved

The lower Hessian bound is justified by “conditional Bernoulli fluctuations” in disjoint boxes. The source `H` depends on entire particle trajectories and actual contacts, so it creates nonlocal correlations among initial placements. Positivity of an untitled one-particle activity on finitely many boxes does not by itself give a covariance lower bound uniform over the dynamic source ball.

One needs either a cluster-cumulant perturbation theorem proving stability of the covariance matrix from its zero-source value, or a conditional insertion argument with source-uniform Radon–Nikodym bounds. The manuscript states neither estimate.

### 5. The shell coefficient theorem is unsupported

The theorem

\[
P_{H,\lambda_H,\epsilon}
\left(N=N_\epsilon,|Y-a'|\le\delta_\epsilon\right)
=
\mu_\epsilon^{-1/2}(c_H+o(1))
\]

is a mixed lattice/continuous local limit theorem. It is the load-bearing result: only after this estimate can the shell probability be discarded at exponential speed. Because the minor-arc gap and continuous-frequency decay are not proved, the coefficient theorem is not available.

The source-dependent saddle formula is formally correct, but formal change of measure cannot replace the missing coefficient asymptotic.

### 6. Dependence on B2 remains unresolved

The pressure `Q_epsilon(H,lambda)` is assumed to have normal convergence, three source derivatives, and a complex neighborhood uniform in both the all-contact source and the constraint multiplier. The controlling B2 paper proves none of those statements at the required global source scope. B1 therefore uses its principal analytic input before it has been established.

### 7. The hard-core correction estimate is not the dynamic transfer theorem

The estimate

\[
N_\epsilon^2\epsilon^3=O(\epsilon^{-1})=o(\mu_\epsilon)
\]

is a coarse static excluded-volume count. It does not control the source-decorated trajectory partition function, its Fourier transform, or the saddle coefficient. The revision appropriately says it is only subleading, but the proof still lacks the dynamic estimate that must replace it.

### 8. The controlling manuscript is not standalone

The active `main.tex` delegates everything to one closure file and does not provide a complete definition of the grand-canonical reference law, source norms, constraint scaling, collision observable, or the B2 theorem being imported. The reader cannot verify the coefficient theorem from the paper alone.

## What is correct and worth retaining

The following formal consequences are sound once a genuine source-uniform coefficient theorem is supplied:

- the constrained saddle formula;
- the exact time-zero source test;
- analytic dependence of the multiplier under a uniformly positive constraint Hessian; and
- the Schur-complement Hessian of the conditioned pressure.

These constitute a useful blueprint for the correct theorem.

## Editorial recommendation

**Reject.** Unlike the previous version, the theorem being targeted is now the right one. The principal local-coefficient proof is quantitatively wrong at the Boltzmann–Grad scale, however, and the required B2 pressure input is absent. A viable resubmission must prove a source-uniform mixed lattice/continuous local limit or coefficient-extraction theorem with correctly scaled insertion cells, and it must be logically downstream of a rigorous grand-canonical all-contact pressure theorem.