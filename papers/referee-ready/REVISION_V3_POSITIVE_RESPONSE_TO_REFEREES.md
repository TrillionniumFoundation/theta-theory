# Consolidated positive response to the referee reports — revision v3

**Revision branch:** `theta-referee-revision-v3-positive-closure-2026-08-28`  
**Parent revision:** `theta-referee-revision-v2-2026-08-28`  
**Report branch:** `review/top4-harsh-referee-reports-2026-08-28`  
**Scope:** θ-Theory only.

## Revision principle

Revision v3 does not close a mathematical objection by deleting the disputed
phenomenon, replacing it by a no-go statement, or merely weakening a title.
Every major referee objection is answered by one of the following positive
objects:

1. a proved theorem on the common moving-cut reference platform;
2. a corrected positive geometric theorem with an explicit open parameter
   margin;
3. a quantitative analytic estimate that supplies the previously unnamed
   arrow;
4. a fully specified stochastic/deterministic representation with its actual
   density process, DPP, or tangent equation.

The reports reviewed older monograph and three-paper snapshots.  Revision v3
nevertheless treats their objections as proof obligations for all five current
papers.

## The common actual platform

All five papers now use the same deterministic moving-cut platform.  For
`a in [-1/40,1/40]`, let

\[
T_a(x)=\frac{x-s_{i-1}(a)}{w_i(a)},\qquad
x\in [s_{i-1}(a),s_i(a)),
\]

with

\[
(w_1,w_2,w_3,w_4)
=(1/10+a,\ 1/5+2a,\ 3/10-a,\ 2/5-2a).
\]

The parameter may vary predictably with the previously generated branch
history.  The new **exact innovation theorem** proves inductively that, under
Lebesgue initial data, the current fibre coordinate is conditionally uniform,
the next branch symbol has probabilities `w_i(a_k)`, and the post-collision
coordinate is again uniform and independent of the enlarged past.  Hence the
conditionally independent branch array used in Papers II--IV is not an
external random model: it is the exact symbolic process of the deterministic
nonautonomous moving-cut dynamics.

The same paper proves nonconjugacy.  The three interior fixed points have
multipliers `w_i(a)^{-1}`, `i=1,2,3`.  Their parameter ranges are disjoint, so a
`C^1` conjugacy cannot permute them; equality of multiplier multisets forces
equality of the parameters.

A collision-flow realization on a cylinder is supplied: the bottom collision
launches vertically, and the top deterministic reflection law sends the next
bottom footpoint to `T_a(x)`.  The three discontinuity seams move with the
parameter and the Poincare map is exactly `T_a`.

## Positive closure table

| Referee blocker | Positive v3 theorem or construction |
|---|---|
| No actual moving/nonconjugate system closing the chain | The common platform theorem proves moving physical seams, a nonzero source, nonconjugacy, exact innovations, pressure, diffusion, rough homogenization and the downstream value recursions on one model. |
| CM2 packets merely rename the result | On the common platform every parameter letter is explicit and the product tail follows from two independently proved centered contractions. No escape, cemetery, reverse-Hölder, or face-envelope hypothesis is used. |
| Future insertion after assembly was not justified | The fixed graded spaces are invariant, and each total parameter letter maps `W^{r+k,1}` to `W^{r,1}`. All future Kato insertions are ordinary bounded compositions on that invariant ladder. |
| Uniform family spectral theorem missing | A direct derivative-seminorm contraction and periodic Poincare inequality give a uniform spectral gap for the whole parameter interval. |
| No actual high-frequency moving-family theorem | For a branchwise Diophantine roof, the twisted moving-cut operator has a one-dimensional constant block and a quotient contraction. A quantitative torus-separation estimate yields polynomial all-frequency resolvent bounds and their parameter derivatives. |
| Incorrect triangular Lorentz finite-horizon interval | A corrected theorem proves finite horizon for the triangular lattice when `sqrt(3)/4 < r < 1/2`, and proves openness under a quantitative `C^2` normal-deformation margin. |
| Response was confused with homogenization | Exact innovations give a martingale triangular array for predictable parameter paths. Conditional Lindeberg, bracket convergence and second-level convergence are proved directly, yielding the nonautonomous rough limit. |
| Anisotropic pairing did not imply pointwise viscosity inequalities | The actual HJB and game values are pointwise monotone recursions. Their consistency estimates are local-uniform Taylor estimates, so half-relaxed limits give pointwise viscosity inequalities directly. |
| Comparison only on a compact gradient window | The actual entropic and quadratic-game equations are globally defined and are transformed exactly to linear uniformly parabolic equations by Cole--Hopf. The abstract theorem uses global Lipschitz/ellipticity structure. |
| Green--Kubo tensor was not symmetric positive | The tensor is the symmetrized correlation series and is proved equal to a variance limit, a pressure Hessian and a martingale bracket. |
| Nonconvexity was planted in a primitive port | A curvature-compensation theorem turns a general `C^2` two-player mechanical payoff into a strongly concave--convex game by actual quadratic actuator energies. The resulting pure saddle produces the nonconvex Hamiltonian. |
| General pure-strategy Isaacs saddle missing | Strong monotonicity of the saddle operator yields a unique pure saddle and a Lipschitz selector. Lower and upper semi-Lagrangian schemes converge to the same Isaacs value. |
| Weighted noncompact filter was trivial | A Gaussian refresh--autoregression has a genuine noncompact state, geometric drift, a strict total-variation prediction contraction `(1-delta)`, and a nontrivial bounded observation update. The observation-gap theorem gives quantitative posterior contraction. |
| Semigroup differentiability had been assumed | Paper V proves a parabolic-Hölder implicit-function theorem and, on the actual entropic branch, an exact analytic terminal-map formula with derivatives equal to tilted cumulants. |
| `Z=sigma(x,p)^T p` had been inverted incorrectly | No inversion is used. In tangent and BSDE formulas, `Z=sigma^T Du` is retained as the martingale integrand. |
| Alleged Girsanov theorem was only algebra | The new theorem constructs the terminal exponential tilt, its density martingale, the stochastic exponential, a Novikov/BMO condition, the Radon--Nikodym derivative, and the changed drift. |
| Path-dependent/2BSDE branches lacked actualization | Bounded path payoffs are treated by an exact entropic path evaluation and quadratic BSDE; volatility control produces a stable nondominated family, a path DPP, the path `G`-heat PPDE and its 2BSDE representation. |

## Five-paper positive dependency chain

```text
Paper I
  exact moving-cut response + nonconjugacy + exact innovations
      |
      v
Paper II
  pressure/root/symmetric covariance + Diophantine high-frequency suspension
      |
      v
Paper III
  predictable martingale rough limit + pointwise entropic HJB/theta semigroup
      |
      v
Paper IV
  noncompact filtering + strong pure Isaacs + actual lower/upper game limit
      |
      v
Paper V
  analytic tangent laws + genuine Girsanov + BSDE/PPDE/2BSDE representations
```

No downstream theorem is used to establish an upstream one.

## Verification boundary

Revision v3 is a full internal proof revision.  It does not claim that the
external referees have accepted the new proofs.  The revised files must be
compiled in a clean checkout and returned to the same specialist referees for
a second line-by-line review.  Formula and structural scripts verify only the
identities encoded in them; they do not certify the analytical arguments.
