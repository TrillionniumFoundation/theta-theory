# Round-Four Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B3 — *Hamilton--Boltzmann Cotangent Geometry from Deterministic Hard-Sphere Collisions*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round4-referee-positive-closure-11paper-2026-08-30@cbee394d6ee33db471b63420131314bd05909a0f`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `4c76a34348f8207598b169879b0509ff8170a687`

## Overall assessment

The revision fixes an important previous defect. Collision work is now paired with genuine continuous functions and Radon measures rather than an `A_f`-equivalence-class Orlicz space which could not detect singular collision current. The paper also recognizes the complete gauge `(p,psi) ~ (p+r,psi-Delta r)` and uses the correct finite-volume Hessian normalization.

The controlling functional spaces are nevertheless inconsistent: the graph space allows collision increments with quadratic weight, while the gauge complex declares that their sum with a bounded source belongs to `C_b`. Thus the principal quotient map is not well defined. The covariance nullspace and process-level Gaussian theorem are also not proved, and the fourth-increment estimate used for tightness is false uniformly at microscopic time scales.

## Major objections

### 1. The gauge complex is not a well-defined map between the declared spaces

The graph norm controls

\[
\|\Delta p/W_c\|_\infty,
\qquad
W_c(v,v_*)=1+|v|^2+|v_*|^2.
\]

Therefore `Delta p` may grow quadratically. The collision source, however, is taken in

\[
C_b(\mathfrak C_T),
\]

and the manuscript declares

\[
\mathfrak D:\mathcal Y_p\times C_b
\longrightarrow C_b,
\qquad
\mathfrak D(p,\psi)=\Delta p+\psi.
\]

For a general `p in Y_p`, the right-hand side is not bounded. Hence `mathfrak D` does not map into `C_b`, `mathfrak G r=(r,-Delta r)` does not map into `Y_p x C_b`, and the displayed exact sequence is not even typed.

The natural repair would use the weighted continuous space `C_{W_c}` throughout, with an explicitly chosen bounded-strict topology and a source domain on which `exp(z)` is integrable. Alternatively, the density cotangent must be restricted so that `Delta p` is bounded. The present theorem cannot stand.

### 2. The exponential Hamiltonian is not finite on the full weighted source space

Even replacing `C_b` by `C_{W_c}` is not automatic. If `z` has positive quadratic growth, then

\[
\int e^z\,dA_f
\]

requires a Gaussian exponential moment with a coefficient below the available tail exponent. The paper does not define this open exponential source domain or its topology. A linear weighted space is too large for the exponential functional.

Thus the claimed global quotient is incompatible with the nonlinear Hamiltonian unless it is restricted to a convex exponential-integrability chart.

### 3. The singular-measure Fenchel argument is useful but incomplete in the weighted setting

For a compact `A_f`-null set charged by `Gamma`, the Urysohn construction correctly shows that bounded continuous tests can force infinite cost. However, the proof assumes the collision state is locally compact/normal enough for the required compact support and that the approximating functions lie in the source class used by the Hamiltonian. These topological facts should be stated for the quotient collision space with its velocity weight.

The final sentence claiming smooth compactly supported approximation from “weighted tightness and graph completion” is not a proof, particularly near grazing and pre/post quotient faces.

### 4. The positive quotient covariance lemma confuses temporal coboundaries with pointwise constants

Zero asymptotic variance of an additive path observable does not make it constant on every microscopic configuration. It may be a nontrivial time coboundary. The proof says that varying one free flight and one binary contact identifies every zero-variance direction with a balance gauge. That does not address telescoping temporal coboundaries or endpoint functions.

A valid positivity theorem needs a complete cohomological characterization of the kernel of the path-pressure Hessian on the chosen time-dependent density/collision source space. The local-variation density lemma identifies the annihilator of instantaneous balanced tangents, not the kernel of long-time covariance. These are different statements.

Therefore invertibility of the mean map and uniqueness of macro multipliers are unproved.

### 5. The balanced-tangent density lemma is not established

The proof relies on B2's “positive collision right inverse,” itself unproved. It also says that a partition of unity reduces every smooth balanced tangent to finitely many free-flight and collision pieces. Balance is a global transport constraint with endpoint traces; localizing it creates commutator defects which must be solved with uniform estimates.

No density theorem in the declared weighted graph topology is supplied. Hence the annihilator conclusion cannot be used as a substitute for a constraint qualification.

### 6. The fourth-increment estimate is false uniformly in time

The manuscript claims

\[
\mathbb E|\langle\zeta_t^\varepsilon-\zeta_s^\varepsilon,\phi\rangle|^4
\le C|t-s|^2
\]

uniformly in `epsilon`, with an analogous collision estimate.

For a centered jump/counting fluctuation scaled by `sqrt(mu_epsilon)`, a single contact during an interval of length `h` contributes a fourth-moment diagonal term of order

\[
\frac{h}{\mu_\varepsilon},
\]

in addition to an `h^2` term. For `h << 1/mu_epsilon`, the former dominates `h^2`, so the asserted bound cannot hold uniformly for all `s,t`.

A tightness argument may still be possible using Aldous' criterion, predictable brackets, or a bound `C(h^2+h/mu_epsilon)`. The displayed lemma and its proof are wrong as stated.

### 7. Vanishing cumulants does not by itself give path-space Gaussian convergence

Normal convergence of finite-dimensional cumulants can establish finite-dimensional Gaussian limits. Process convergence additionally needs tightness, identification of the time covariance, and control of jumps. Since the increment lemma fails, this bridge is absent.

The proof also treats cumulants of an entire path-valued field as though every connected order-`k` term had one universal scale. The required estimates must be uniform over time-localized nuclear test sets and must include boundary/contact singularities.

### 8. The formula for the collision fluctuation is not fully typed

The derivative `Dq_f[zeta]` is defined through a backward adjoint solution `p[f]`, but B2 has not constructed a smooth map `f -> p[f]` on the announced path space. The collision martingale and density martingale are correlated through the same contact noise; listing their separate brackets does not specify the full joint covariance, including cross-brackets.

Without those data, the “unique centered Gaussian solution” is not a well-defined martingale problem.

### 9. The constrained information projection conclusion is local and conditional

Even with a positive Hessian on a finite-dimensional source family, the inverse-function theorem gives a local source-to-mean chart. It does not prove global uniqueness of a path-space information projection for every target in a broadly described mean image. The theorem must be limited to the exact local chart and effective domain supplied by B2.

### 10. The paper inherits B1 and B2

The pressure, rate, source derivatives, initial covariance, and compactness all depend on B1/B2, which are not presently proved. B3 cannot serve as a certified downstream cotangent or Gaussian theorem.

## Status of previous objections

The full representation gauge is now conceptually correct, and the use of Radon collision tests fixes the prior singular-current blindness. These are substantial improvements. The active spaces, however, have not been made compatible with that gauge or with the exponential Hamiltonian.

## Minimum viable reconstruction

A rigorous version should:

1. choose a weighted continuous collision-source space `C_{W_c}` and an explicit exponential-integrability chart;
2. redefine `Y_p` so that `Delta p` lies in that same chart;
3. prove a closed exact gauge sequence there;
4. prove a cohomological kernel theorem for the path-pressure Hessian;
5. establish process tightness with correct jump-scale increment estimates; and
6. state the full joint Gaussian martingale covariance, including cross-brackets.

## Recommendation

**Reject.** The revision fixes the correct gauge concept but the principal map is ill typed, and the claimed process-level fluctuating Boltzmann theorem is not proved.