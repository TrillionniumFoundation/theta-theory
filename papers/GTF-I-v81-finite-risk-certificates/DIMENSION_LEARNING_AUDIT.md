# Revision 78 dimension and interior learning audit

## Object and conclusion

This is an independent symbolic review of
`sections/60-dimension-accuracy-learning.tex`, read together with the
horizontal derivative argument in Section 53, the Bernoulli lower bound
in Section 51, the fresh-block definition and theorem in Section 58,
and the cited primary tomography theorem.

No blocking mathematical gap was found in the stated weak-measurement
information lemma, coherent adaptive lower bound, fixed-confidence
operator-norm corollary, dimension-free interior comparison, or sharp
interior learning theorem. The proof genuinely couples dimension and
accuracy; it does not multiply unrelated lower bounds. Confidence is
fixed at `1/8` in the joint upper/lower equivalences, as required by the
argument actually supplied.

This audit establishes neither priority nor a physical implementation.
It is a written proof review; the analytic statements are not inferred
from finite numerical experiments or manuscript compilation.

| Claim | Stable source label | Result of review |
| --- | --- | --- |
| Information increment for label-dependent weak binary measurements | `lem:weakmeasurementinfo78` | Valid for already correlated inputs and retained memory |
| Joint lower bound in dimension and future accuracy | `thm:dimensionlower78` | Valid uniformly for every `d,N >= 1` in the displayed small-error range |
| Operator-norm minimax order at constant confidence | `cor:binaryoperatorlearning78` | Lower bound is supplied here; upper bound is the cited existing estimator |
| Dimension-free metric comparison on a fixed interior | `lem:interiormetric78` | Both constants follow without a Hilbert–Schmidt dimension loss |
| Sharp interior future-loss learning | `thm:interiorlearning78` | Valid at failure `1/8`, using one-call fresh probes for the upper bound |

## 1. The weak-measurement output state is correct

For a fixed label, let `rho_AR` be any joint input state and put
`rho = Tr_A rho_AR`. The consuming binary channel with
`E = I/2 + H` produces blocks

\[
\omega_{YR}=|1\rangle\langle1|\otimes(\rho/2+\Delta)
 +|0\rangle\langle0|\otimes(\rho/2-\Delta),
\qquad
\Delta=\operatorname{tr}_A[(H\otimes I)\rho_{AR}].
\]

Partial cyclicity on `A` makes `Delta` Hermitian. To see its order bound
without assuming a product of positive matrices is positive, one may
write `Tr_A[(rI +/- H) rho_AR]` as the partial trace of
`sqrt(rI +/- H) rho_AR sqrt(rI +/- H)`. Thus

\[
-r\rho\preceq\Delta\preceq r\rho.
\]

This implies that `Delta` is supported on `supp rho`; its support
factorization is `Delta = rho^(1/2) K rho^(1/2)` with Hermitian
`||K||_op <= r`. The post-call retained marginal is exactly `rho`,
which is essential for the information comparison.

The argument uses the stated consuming, classical-output interface.
Access to a measurement environment or residual quantum output would
change the output system being bounded and is not covered.

## 2. Noncommuting collision calculation and Jensen bound

With `sigma = (I_Y/2) tensor rho`, direct summation of the two classical
blocks cancels all linear terms and gives

\[
\operatorname{tr}(\omega^2\sigma^{-1})
 =1+4\operatorname{tr}(\Delta^2\rho^{-1}).
\]

The noncommuting part is legitimate: cyclicity of the trace, rather
than a commutation assumption, gives

\[
\operatorname{tr}(\Delta^2\rho^{-1})
 =\operatorname{tr}(K\rho K)
 =\operatorname{tr}(\rho K^2)\le r^2.
\]

All inverses are on `supp rho`. Singular retained states therefore
cause no gap.

For density matrices `a,b` with `supp a` contained in `supp b`, use
their spectral bases and the probability weights
`w_ij = a_i |<u_i,v_j>|^2`. Terms of zero weight are omitted. Then

\[
D(a\|b)=\sum_{ij}w_{ij}\log(a_i/b_j)
 \le\log\sum_{ij}w_{ij}(a_i/b_j)
 =\log\operatorname{tr}(a^2b^{-1}).
\]

This is scalar Jensen applied to the displayed probability distribution;
it does not assert a generally false operator Jensen identity for the
noncommuting logarithms. It proves the precise relative-entropy upper
bound used in the section.

The finite-output scalar-reference extension in the following paragraph
also checks out. With `Delta_y = rho^(1/2) K_y rho^(1/2)` and
`||K_y|| <= r p_y`, the collision contribution is at most
`sum_y r^2 p_y = r^2`, and the linear terms vanish by
`sum_y Delta_y = 0`. Only its binary specialization is used later.

## 3. Why prior label correlations do not defeat the information bound

Write `tau_Y = I_Y/2`. For the output ensemble, the exact identity is

\[
\begin{split}
&\sum_x p_x D(\omega^x_{YR}\|\tau_Y\otimes\rho^x_R)
 -D(\omega_{YR}\|\tau_Y\otimes\omega_R)\\
&\hspace{35mm}=I(X:Y\mid R)_{\rm out}.
\end{split}
\]

The second relative entropy is nonnegative. The collision estimate
therefore bounds conditional mutual information by `log(1+4r^2)`.
Since the retained marginal is unchanged,

\[
I(X:YR)_{\rm out}
 \le I(X:R)_{\rm in}+\log(1+4r^2)
 \le I(X:AR)_{\rm in}+\log(1+4r^2).
\]

No hypothesis says that `rho_AR^x` is independent of `x`. This is the
key point allowing induction through coherent adaptive queries. All
common intervening channels decrease mutual information; initial
resources have zero information about the random packing label. The
complete final quantum and classical record consequently has information
at most `4 M r^2`.

Every-record bounded stopping is covered by appending ignored dummy
queries. An expected-call budget is a different resource convention and
is not substituted into this argument.

## 4. Packing, future-loss separation, and the exact Fano constants

The real space of Hermitian `d` by `d` matrices has dimension `p=d^2`.
A maximal `r/4`-separated subset of its operator-norm ball of radius
`r` is finite by compactness and covers that ball by translates of
radius `r/4`. Volume scaling therefore gives at least `4^p` centers.
This argument works for every finite `d`, including `d=1`; it does not
use an asymptotic spherical approximation.

With

\[
r=2048\delta/\sqrt N,\qquad 0<\delta\le2^{-13},
\]

one has `r <= 1/4`, so every `I/2 + H_x` is in the stated fixed
interior. For two distinct centers, a unit eigenvector achieving
`||H_x-H_z||_op` gives Bernoulli parameters separated by at least
`r/4`. Repeating this same input `N` times yields

\[
T_N\ge\tfrac12\sqrt N\,(r/4)=256\delta.
\]

The `1/64` Bernoulli lower constant gives `d_N >= 4 delta`, since
`256 delta <= 1`. The repeated input is allowed to depend on the pair:
it is a packing-separation witness, not the purported common learner.

Choosing a nearest packing center from the estimate is a valid testing
reduction. The estimate may lie outside the interior family and still
within the full legal effect body. If its loss to the correct center
is at most `delta`, every wrong center is at least `3 delta` away,
so no equality ambiguity can cause a wrong decision on the success
event. No efficient evaluation of `d_N` is required from the learner.

For a uniform packing label and `eta <= 1/8`, Fano gives

\[
4Mr^2\ge(1-\eta)\log L-\log2
 \ge\tfrac34d^2\log2.
\]

The last inequality holds even at `d=1`. In particular the proof permits
the explicit absolute constant

\[
c=\frac{3\log2}{2^{26}}
\]

in `M >= c d^2 N delta^(-2)`. A smaller constant may be chosen elsewhere
for convenient common ranges.

## 5. Interior comparison avoids a dimension loss

On the segment joining effects in `[I/8,7I/8]`, one has

\[
S=\sqrt{G(I-G)}\succeq\frac{\sqrt7}{8}I\succeq I/4.
\]

The Sylvester integral

\[
K=\int_0^\infty e^{-uS}He^{-uS}\,du
\]

solves `SK+KS=H` and gives `||K||_op <= 2 ||H||_op`. The checked
horizontal identity in Section 53 has `alpha=K^2` and `beta=0`, so
the derivative of any fixed common `N`-query tester's output has trace
norm at most `2 sqrt(N) ||K||_op`. Integrating the fixed tester first
and then taking the supremum proves

\[
d_N(E,F)\le4\sqrt N\,\|E-F\|_{\rm op}.
\]

There is no substitution of a Hilbert–Schmidt norm and therefore no
hidden `sqrt(d)` factor. The positive fixed interior permits the
unregularized horizontal tangent directly. The lower constant `1/128`
follows from the repeated eigenvector input and
`min(1,T_N) >= (1/2) min(1,sqrt(N)||E-F||_op)`.

## 6. Independently verified external upper theorem

Primary source checked directly: Mele–Bittel,
[arXiv:2512.10214v3](https://arxiv.org/html/2512.10214v3),
Section III.2, Lemmas III.7–III.8, and Corollary III.9.

The source identifies the binary diamond distance as twice the effect
operator norm, extracts an exactly legal effect from a CPTP estimate,
and gives `1024 d^2 epsilon^(-2) + O(d epsilon^(-2) log(1/eta))`
calls when `eta > 4 exp(-4d^2)`. Thus `eta=1/8` is allowed even for
`d=1`. Its calls prepare independent maximally entangled
probe–reference pairs; collective processing occurs after acquisition.

The manuscript's `N=1, delta=2 epsilon` reduction and its interior
choice `epsilon=delta/(8 sqrt(N))` therefore have the stated orders.
The latter event also guarantees `F` lies in `[I/8,7I/8]`, where the
interior comparison gives future loss at most `delta/2`.

## 7. Scope conditions and boundaries retained

The joint equivalences `Theta(d^2 epsilon^(-2))` and
`Theta(d^2 N delta^(-2))` are stated at failure probability `1/8`.
The Fano argument provides the same dimension lower term for all
`eta <= 1/8`, but does not supply a multiplicative `log(1/eta)`.

For the full effect body and the fresh-block class, the simultaneous
dimension and projective confidence lower bounds imply their sum after
reducing an absolute constant. Their common range is

\[
d\ge2,\quad1\le b\le N,\quad
0<\delta\le\min\{2^{-13},\delta_*\},\quad0<\eta\le1/8.
\]

This is a sum of two independently necessary resource obstructions,
not a product of lower bounds. It does not match the constructive
`d^4` factor on the full body.

Finally, the finite-control theorem in Section 59 explicitly verifies
finite classical computations and preparations for the paper's common
matrix and block-capped learners. It is not, by itself, a finite-outcome
or finite-controller realization of the cited collective tomography
estimator. No such additional implementation claim is needed for the
information-theoretic upper bound in Section 60. If that claim is later
desired, its continuous outcomes and collective postprocessing require a
separate discretization argument.
