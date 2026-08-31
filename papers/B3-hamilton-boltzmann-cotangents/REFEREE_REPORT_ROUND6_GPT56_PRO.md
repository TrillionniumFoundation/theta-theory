# Round-Six Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B3 — *Hamilton–Boltzmann Cotangents and Prepared Fluctuation Fields*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round6-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `fb2ccfafab262f31f5b6f960df23e31258a59223`  
**Reviewed tree:** `2d3992ea12cfd513359a5f204bb1c2ae027bc7c4`  
**Active controlling module:** `ROUND6_POSITIVE_CLOSURE.tex`, blob `f829db047f05c1e5ac1669ffe389854f8807a792`

## Editorial summary

Separating the local analytic source chart from the global compactly supported Fenchel domain is the correct repair of the previous version. The exact finite-volume centering is also mathematically necessary and is now stated honestly.

The central covariance-kernel theorem, however, remains a formal convex-duality argument rather than a proof. The action is nonlinear in the density through `A_f`; its second variation is neither computed nor shown coercive on the balanced tangent space. Positivity on a dense family does not identify the annihilator with the closed gauge range, and infinite-dimensional Legendre Hessians cannot simply be inverted. The process tightness theorem then relies on the unproved B2 stopping-contact trace estimate. B3 therefore does not supply the Gaussian interface claimed by B4, C1, C2, or D1.

## Major mathematical objections

### 1. The displayed “second variation” of the action is not derived and is generally incomplete

The dynamic action is

\[
J(f,\Gamma)=\int\ell\left(\frac{d\Gamma}{dA_f}\right)dA_f,
\qquad A_f\sim ff_*B.
\]

Both the reference measure `A_f` and the density ratio `q=dGamma/dA_f` vary with `f`. The manuscript writes schematically

\[
\delta^2I=\delta^2I_0+
\int\frac{\dot q^2}{q}\,dA_f+
\text{the quadratic variation of }A_f\text{ in }\dot f
\]

and treats this as a positive quadratic form. No formula defines `dot q`, no cross terms between `dot Gamma` and `dot f` are included, and the second derivative of the quadratic map `f -> A_f` is omitted.

At a regular biased point, the correct first-order tangent is naturally

\[
\dot\Gamma-q\,DA_f[\dot f],
\]

with additional terms from the variation of `q` and from `D^2A_f`. Away from the zero-cost point `q=1`, these terms are not manifestly positive. Joint convexity of relative entropy in `(Gamma,A_f)` does not imply convexity after the nonlinear substitution `A_f=ff_*B`.

Without an exact quadratic expansion, there is no basis for the claimed coercive tangent action or for Hessian inversion.

### 2. Strict curvature of a support function does not follow from Hahn–Banach separation

The proof says that if a source quotient class is nonzero, Hahn–Banach provides a smooth balanced tangent with nonzero pairing; because the action is positive on that tangent, the local support function is strictly curved in the source direction.

This implication is false without quantitative coercivity and a two-sided tangent construction. A convex function may have a positive cost in every nonzero feasible direction while its conjugate is nondifferentiable, has zero second derivative, or has an unbounded Hessian. One needs a Hilbertian quadratic approximation with a closed range, not merely positivity of the nonlinear action.

The B2 regularization lemma, even if valid, gives density of finite-action paths in an action topology. It does not show that every linearized balanced tangent is realized at order `s` with cost `s^2 Q(dot x)/2+o(s^2)`, nor that the tangent cone is a closed linear subspace.

### 3. The annihilator of balanced tangents is not proved equal to the gauge range

The theorem identifies zero-variance sources with the closed balance gauge, endpoint coboundaries, and prepared constraints. The proof only establishes the easy inclusion: exact balance identities have zero microscopic fluctuation.

For the converse, vanishing pairing against all smooth balanced tangent directions yields membership in the annihilator of that tangent space. To identify this annihilator with

\[
\operatorname{Ran}\mathfrak G
\]

one needs a closed-range theorem for the full linearized balance operator, including endpoint traces, transport domains, collision invariants, and velocity weights. The fact that `Ran G` is the graph of `-Delta` inside the source product says nothing about the range of the primal balance operator or whether its annihilator has additional elements.

Boundary conditions, non-surjectivity of the linearized collision map, and dynamically inaccessible tangent directions may create further null classes. Hahn–Banach does not remove them.

### 4. Infinite-dimensional Legendre “Hessian inversion” is unjustified

The sentence “Legendre Hessian inversion therefore gives positive pressure variance” is valid in a finite-dimensional smooth, strictly convex setting with an invertible Hessian. Here the primal space is an infinite-dimensional path-measure space, the action may be merely lower semicontinuous, and no Banach-space second differentiability or bounded inverse is shown.

Even strict positivity on each fixed finite-dimensional test family gives only nondegeneracy of those projected covariance matrices, not an exact global kernel theorem. Eigenvalues may tend to zero along a sequence of quotient directions, the range may be nonclosed, and the conjugate need not be twice Fréchet differentiable.

The statement should be reduced to finite-dimensional projected nondegeneracy under explicit quantitative assumptions, unless a complete functional-analytic Hessian theorem is supplied.

### 5. The global pressure extension is not shown to be a well-defined convex functional

The formula

\[
\overline Q(p,\psi)=
\sup_M\lim_{R\to\infty}Q(p^{M,R},\psi^{M,R})
\]

uses unspecified truncations and a limit in `R` that need not be monotone for signed sources. Different cutoff schemes can give different values. A log-mgf is monotone in a nonnegative source, not in a general signed density/contact cotangent.

The Fenchel theorem itself can be formulated as a supremum over the union of bounded compactly supported tests, and that scalar duality argument is largely sound. But the paper additionally treats `overline Q` as a proper lower-semicontinuous pressure compatible with local analytic charts without proving independence of truncation, convexity, or convergence from finite volume. Those claims should be separated from the pointwise integral conjugacy.

### 6. The conditional cumulant estimate depends on an unavailable B2 state

`lem:r6-b3-cumulants` asserts the same source-derivative bound after an arbitrary stopping time, conditioned on the complete trace hierarchy at that time. The B2 report explains why a state conditioned on a specific collision can be a singular boundary measure rather than an element of the declared `L1` trace Banach space. B2 also has no valid uniform cyclic estimate.

Consequently the claimed “same compact trace ball” after stopping is not established. Without that conditional estimate, the fourth-moment bound does not hold uniformly for stopping-time increments and Aldous' criterion cannot be invoked as written.

Unconditional analytic cumulants at deterministic intervals do not by themselves imply process tightness for a non-Markov projected density/contact field.

### 7. The factor `|I|` in every connected cumulant is not proved

A source localized in a short interval ensures that one marked time lies in `I`, but connected hard-sphere clusters can enter and leave the interval through boundary configurations whose densities have singular time traces. The proof adds an “endpoint atom” of order `mu^{-k/2}` without deriving it, and does not control clusters with several events accumulating at an endpoint.

To obtain a uniform `C_k |I|` bound one needs an integrable time density for all marked connected cumulants, uniformly in `epsilon` and in the biased source. This is essentially a local contact-correlation theorem; it does not follow from normal convergence of a pressure on the whole horizon.

### 8. The Gaussian identification requires more than vanishing cumulants of fixed tests

Even if finite-dimensional cumulants converge, the limiting covariance must satisfy positivity, consistency across times, and continuity in the nuclear test topology. The paper names a “countably Hilbert nuclear scale with Maxwellian weights” but never defines it, proves nuclearity, or shows that the covariance form is continuous on it.

Mitoma's theorem applies to specified nuclear spaces and requires tightness of every scalar projection in the appropriate dual path topology. The contact component is a measure-valued cumulative process while the density component has weak balance dynamics; their joint topology and jumps are not declared precisely enough for the theorem quoted.

### 9. The dynamic covariance formula is only formal

Differentiating a limiting Hamilton–Jacobi equation twice can suggest the Lyapunov covariance formula, but it does not construct a Gaussian martingale problem for deterministic contacts. The propagator `U(t,s)` is not defined on the weighted distribution scale, and uniqueness of the linearized biased balance is not proved. The covariance also depends on the invalid B1 initial Schur complement and the unproved B2 pressure derivatives.

Thus the formula may be a reasonable candidate, but it is not a theorem derived from the microscopic model in the submitted text.

## What is actually established

The weighted typing of `Delta p`, the closed graph of the source gauge, and the scalar Fenchel computation over all bounded compactly supported contact tests are useful formal structures. They do not by themselves prove a covariance rigidity theorem or a process central limit theorem.

## Dependency consequences

B4 cites B3 for comparison compactness and the Gaussian tangent. C1 uses B3 for strict quotient covariance and LAN. C2 and D1 use the same process/tangent interfaces. Since B3 also depends on invalid B1 and B2 inputs, none of those downstream Gaussian or statistical conclusions can be credited.

## Required reconstruction

A viable revision must:

1. compute the exact second variation of the density–contact action on a declared linearized balanced tangent space;
2. prove a closed-range/annihilator theorem for the primal balance operator;
3. restrict covariance rigidity to finite-dimensional projections or establish a genuine Banach/Hilbert Hessian isomorphism;
4. define a scheme-independent global pressure domain;
5. prove deterministic- and stopping-time localized cumulant estimates independently of the missing B2 conditional trace assertion; and
6. specify the nuclear test space, path topology, linearized propagator, and uniqueness theorem for the Gaussian limit.

## Recommendation

**Reject.** The two-domain duality architecture is improved and the exact centering is correct, but the covariance kernel and Gaussian process remain formal. The proof substitutes Hahn–Banach and “Legendre Hessian inversion” for the missing quadratic-action and closed-range analysis, and process tightness depends on an unavailable B2 stopping-state estimate.