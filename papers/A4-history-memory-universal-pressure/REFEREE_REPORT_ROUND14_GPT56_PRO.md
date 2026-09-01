# Independent Referee Report — Round 14

**Manuscript:** A4 — *History, Memory, and Universal Pressure*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `fd1385ef2661d0a9d98b1bcd41e315d901b9ecfa2632d0f602fb34ff5cdb6fd0`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

The revision makes several correct conceptual repairs. Complete-past total-variation minorization is replaced by a metric that discounts the remote tail; the Poisson martingale is now centered correctly; the nonlinear tower uses an eigenfunction Doob transform; and memory descriptors are extracted only after forming the final Schur complement.

Those repairs do not amount to proofs of the new headline theorems. The claimed global Wasserstein contraction is not obtained from the stated summable-variation estimate, the Feynman–Kac “chart” is not a defined analytic Banach neighborhood, the renewal-resolvent theorem simply imports the unresolved A2 high-frequency theory, and the projected Volterra statement omits the orthogonal forcing term for a general initial observable.

## Decisive objections

### 1. Summable past variation does not prove the stated global contraction

The only quantitative comparison of transition kernels is

\[
\|P(h,\cdot)-P(\tilde h,\cdot)\|_{TV}
\le C\vartheta^r
\]

when the two pasts agree in their last `r` excursions. The theorem, however, asserts for all pasts

\[
\mathcal W_{d_\beta}(P^m(h,\cdot),P^m(\tilde h,\cdot))
\le\rho d_\beta(h,\tilde h).
\]

The proof does not supply a coupling or minorization for histories with different current entrance/exit states. “Use maximal coupling until the first common new excursion” presupposes a uniformly positive probability of drawing a common admissible symbol. Summable variations only says that already close histories have close kernels; it does not give global coalescence on a countable Markov graph.

A finite connector property can yield a small-set or weak-Harris argument, but the relevant set, minorization metric, return time, and constants must be proved. They do not appear here.

### 2. The contraction estimate is stronger than the accompanying drift argument

The metric is bounded in each coordinate, whereas the weight `W` is unbounded. The proof controls coupling failure by a weighted tail but the theorem's first inequality has no additive term involving `W(h)+W(tilde h)`. The weighted failure estimate therefore cannot imply the displayed pure Lipschitz contraction for arbitrary high-weight histories.

At best the sketch suggests a weak-Harris estimate in a weighted distance such as

\[
d_\beta(h,\tilde h)(1+W(h)+W(\tilde h)),
\]

not the theorem written.

### 3. The Feynman–Kac source class is not an analytic Banach neighborhood

The set

\[
\mathscr V_\eta
=\{V:\|V\|_{Lip}<\infty,\ |V(h)|\le c_V+\eta\log W(h)\}
\]

is given no norm controlling the constant `c_V`, the Lipschitz part, and the logarithmic growth coefficient. Consequently “a neighborhood of zero” and “analytic in `V`” are undefined.

Analytic operator perturbation requires one fixed Banach source space and a power-series estimate uniform in its norm. Mapping each multiplier to a “slightly heavier” target weight, without fixing the domain/codomain scale for all powers and derivatives, is not an analytic-family theorem.

### 4. The rough invariance theorem is still only a proof outline

A spectral gap for scalar weighted Lipschitz functions can give a Poisson equation. The enhanced quenched theorem additionally requires:

- a vector-valued bracket law uniform over initial histories;
- tightness of iterated integrals;
- identification of the antisymmetric area correction;
- a joint renewal time-change theorem; and
- uniform control of the terminal roof residual at the rough-path scale.

The proof names martingale CLT, Burkholder, and A3 but provides none of the uniform estimates. A3 itself has not established the stopped physical-clock theorem used here.

### 5. The renewal-resolvent theorem is not derived from the stated A2 input

A2 gives estimates for powers of twisted transfer operators. A4 uses them as a uniform theorem for

\[
(I-\mathcal L_{V,z})^{-1}
\]

on a complex strip, with two vertical derivatives and a Feynman–Kac source. This requires summing operator powers in the correct strong/weak spaces, excluding peripheral spectrum, differentiating the resolvent, and tracking entrance/residual operators. These steps are not supplied.

Moreover, the A2 very-high-frequency estimate is itself unsupported in Round 14, so it cannot be imported as a closed interface.

### 6. Vertical decay of the suspension resolvent does not automatically pass through matrix inversion

The memory contains

\[
C_V(z)^{-1}.
\]

Bounds on `C_V` and its derivatives do not yield corresponding bounds on its inverse without quantitative lower bounds on the smallest singular value away from the explicitly removed zeros. The paper states that genuine zeros are finite and subtracts their principal parts, but it does not prove a uniform inverse bound on the remaining unbounded strip.

This is precisely what is needed to justify the claimed residual estimate for `Khat_V` and the Bromwich shift.

### 7. The projected Volterra equation omits the orthogonal forcing term

For a general observable `A`, the Mori–Zwanzig decomposition contains an inhomogeneous term generated by the unresolved initial component, schematically

\[
P L e^{tQL}Q A.
\]

A homogeneous closed Volterra equation for

\[
x(t)=P_{\mathcal R}U_tA
\]

holds only under an additional condition such as `QA=0`, or after the forcing/noise term is included. The corollary is stated for every `A in D(L_V)` but only mentions the memory distribution. It therefore does not state the exact projected dynamics.

### 8. Descriptor minimality and uniqueness are asserted without a realization theorem

A principal-part expansion of a finite meromorphic matrix can be realized by a finite descriptor system. To claim a unique normalized decomposition one must specify the input/output spaces, polynomial feedthrough, controllability and observability notions, and how poles on the stability boundary are treated. “Standard reduction” does not prove compatibility with the unbounded suspension generator or with source differentiation.

### 9. Standalone novelty depends entirely on unproved interfaces

The Doob logarithmic tower is a general identity once eigen-data exist, and the Schur-complement memory formula is standard operator algebra once all domains and resolvents are constructed. The model-specific value would lie in the weighted coupling, rough suspension limit, and renewal-resolvent estimates. Those are the parts not proved.

## Dependency assessment

A4 cannot presently serve as a source of history kernels, quenched rough limits, memory decay, or optional-projection convergence for C2. Its main inputs A2 and A3 remain open, and its own global coupling and forcing interfaces are incomplete.

## Required reconstruction

A viable paper should prove one focused theorem on a precisely defined weighted history space:

1. a weak-Harris/Wasserstein contraction with the correct weighted metric;
2. a normed multiplier algebra and analytic Doob chart;
3. a suspension resolvent theorem with quantitative inverse bounds; and
4. the full inhomogeneous Mori–Zwanzig equation, including unresolved forcing.

## Recommendation

**Reject.** The revision now uses the right conceptual objects, but the model-specific spectral, rough, and memory theorems remain unproved and the stated projected equation is incomplete.