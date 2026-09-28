# Scalar linearization and the information content of stable-action width

Companion to the independent A2 v14 report, 11 September 2026. Reviewed author commit: `e136929b120912586266fb78e0ae7b3c9d43bfd6`.

This note supplies the calculation behind C14-1 and Section 5 of the report. It is a self-contained comparison with classical scalar dynamics, not a claim to a new linearization theorem. It neither constructs a two-ended physical billiard experiment from an arbitrary scalar map nor replaces the manuscript's relative determinant argument.

## 1. A direct smooth scalar construction

Let $R$ be a smooth orientation-preserving local map of the line such that

$$
R(0)=0,\qquad R'(0)=\lambda\in(0,1).
$$

After restriction to a closed interval $I=[-a,a]$, assume

$$
0<\ell\le R'(u)\le q<1,\qquad u\in I.
$$

Then $R(I)\subset I$, and the orbit satisfies $|R^n(u)|\le q^n|u|$. Put

$$
h(u)=\log\frac{R'(u)}{\lambda}.
$$

The function $h$ is smooth and $h(0)=0$. Define

$$
L(u)=\sum_{k=0}^{\infty}h(R^k(u)),\qquad
B(u)=e^{L(u)},\qquad
\zeta(u)=\int_0^u B(v)\,dv. \tag{1}
$$

### Proposition 1

The series in (1) converges with every fixed derivative on a sufficiently small common interval. The functions $B$ and $\zeta$ are smooth, $B>0$, $B(0)=1$, and

$$
B(R(u))R'(u)=\lambda B(u),\qquad
\zeta(R(u))=\lambda\zeta(u). \tag{2}
$$

The coordinate $\zeta$ is the unique differentiable normalized local coordinate satisfying the second identity, where normalized means $\zeta(0)=0$ and $\zeta'(0)=1$.

These statements hold jointly smoothly in a supplied compact smooth parameter family with a common fixed point, uniform positive derivative bounds, and a uniform contraction margin. At each fixed derivative order the constants may depend on the corresponding higher family norms.

### Proof

The undifferentiated summand is bounded by $Cq^k|u|$, since $h(0)=0$. For derivatives, write $x_n(u)=R^n(u)$ and differentiate

$$
x_{n+1}=R(x_n).
$$

The highest derivative is multiplied by $R'(x_n)$, bounded by $q$. Every other term contains lower derivatives of $x_n$ and bounded derivatives of $R$. The first endpoint derivative is bounded by $q^n$; induction and the resulting inhomogeneous scalar recurrence bound each fixed higher derivative by a constant times a fixed polynomial in $n$ times $q^n$.

For mixed parameter derivatives the same argument applies. An explicit parameter derivative of $R$ with no differentiated orbit factor vanishes at the common fixed point, because $R_\xi(0)=0$ for the whole family. Evaluated at $x_n$, it is therefore $O(q^n)$. Terms with differentiated orbit factors already have a decaying factor. The recurrence may add powers of $n$, but no nondecaying forcing term. Thus each fixed mixed derivative of $x_n$ has a bound $C(1+n)^M q^n$, with a fixed-order exponent $M$.

The same reasoning applies to $h_\xi(x_n)$, because $h_\xi(0)=0$ throughout the family. The differentiated series is consequently absolutely and uniformly summable. This proves the claimed smoothness on one interval; it does not require an interval that shrinks with iteration number or an analyticity assumption.

Shifting the index in the series gives

$$
L(R(u))=L(u)-h(u).
$$

Exponentiating proves the first identity in (2). Integrating its two sides from zero proves the second identity. Positivity of $B$ makes $\zeta$ a local coordinate.

If $\widetilde\zeta$ is another normalized differentiable coordinate, set $f=\widetilde\zeta\circ\zeta^{-1}$. Then

$$
f(\lambda x)=\lambda f(x),\qquad f(0)=0,\qquad f'(0)=1.
$$

For a fixed sufficiently small $x$, iteration gives $f(x)=\lambda^{-n}f(\lambda^n x)$, which tends to $x$ by differentiability at zero. Thus $f(x)=x$, proving uniqueness. The argument works on both sides of the fixed point. □

## 2. Normalized iterates and the sharper rate

The finite product in (1) is exactly

$$
\exp\left\{\sum_{k=0}^{n-1}h(R^k(u))\right\}
       =\lambda^{-n}(R^n)'(u). \tag{3}
$$

Thus (1) already identifies the limiting derivative. The exact conjugacy gives the sharper normalized iterate estimates without a potentially invalid direct division of an absolute error:

$$
R^n(u)=\zeta^{-1}(\lambda^n\zeta(u)).
$$

Write $\zeta^{-1}(x)=x+x^2a(x)$, with $a$ smooth. It follows that

$$
\lambda^{-n}R^n(u)
 =\zeta(u)+\lambda^n\zeta(u)^2a(\lambda^n\zeta(u)). \tag{4}
$$

For a compact parameter family with $0<\lambda_-\le\lambda\le\lambda_+<1$, each fixed mixed derivative of the remainder is bounded by

$$
C_k(1+n)^{M_k}\lambda_+^n.
$$

For any fixed $\sigma\in(\lambda_+,1)$, that is at most $C_{k,\sigma}\sigma^n$. An extra endpoint derivative proves the corresponding convergence in (3) to $B=\zeta'$. Parameter differentiation of the multiplier changes the polynomial factor, not the existence of an exponential margin. This is the same scalar mechanism used in A2 v14 after its physical amplitude has been identified.

## 3. Two alternating contact maps

Suppose two smooth first-hit maps satisfy

$$
\varphi_b(0)=0,\qquad \varphi_b'(0)=r_b>0,\qquad
R_b=\varphi_{1-b}\circ\varphi_b,\qquad r_0r_1=\lambda<1.
$$

Assume their domains have been restricted so both returns are contractions and the relevant compositions are defined. Let $\zeta_b$ be the uniquely normalized scalar coordinate constructed for $R_b$. The composition identity

$$
\varphi_b\circ R_b=R_{1-b}\circ\varphi_b
$$

implies that

$$
\eta_b(u):=r_b^{-1}\zeta_{1-b}(\varphi_b(u))
$$

is another normalized differentiable coordinate linearizing $R_b$. Uniqueness therefore gives

$$
\zeta_{1-b}(\varphi_b(u))=r_b\zeta_b(u),
\qquad
B_{1-b}(\varphi_b(u))\varphi_b'(u)=r_bB_b(u). \tag{5}
$$

Accordingly, the compatibility of normalized first-flight scalar coordinates follows from scalar uniqueness. It is not an additional independent normal-form existence theorem.

### What remains specifically physical in A2

A2 does not begin with the definition (1). Its amplitude is defined through an edge product and a relative Fredholm determinant along a stationary half-line. The manuscript's exact concatenation formula, divided by the finite reference twist before taking a limit, proves (5) **for that physical amplitude**. This identification is a real step and its normalization matters.

Once that step is established, the return cocycle and continuity at zero also prove the identity

$$
B_b(u)=
\exp\left\{\sum_{k=0}^{\infty}
 \log\frac{R_b'(R_b^k(u))}{\lambda}\right\}. \tag{6}
$$

Indeed, the quotient of the physical density and the density in (1) is invariant under $R_b$ and has value one at zero; iteration makes the quotient identically one. Formula (6) is a useful explicit determinant-to-scalar-product comparison.

Neither (1) nor (6), on its own, controls an arbitrary two-ended finite bridge, the variation of its physical mixed derivative, the choice of a first-hit event, or integration against the billiard phase measure. In particular, this note does not derive A2's full relative probability law from a one-dimensional linearization theorem. Its purpose is to separate the classical scalar consequences from the physically normalized identification.

## 4. Width and profile are equivalent descriptions of the same datum

Let $S$ be a smooth strictly convex germ with $S(0)=S'(0)=0$, $S''(0)=a>0$, and let $B>0$, $B(0)=1$. Use the coordinate $\zeta'=B$, $\zeta(0)=0$, and put $\widehat S=S\circ\zeta^{-1}$. Suppose the normalized energy profile $V$ is defined by

$$
(S_*[B(u)\,du])(E)=\sqrt{2/a}\,E^{-1/2}V(E)\,dE,
\qquad V(0)=1.
$$

If $u_-(E)<0<u_+(E)$ are the two solutions of $S(u)=E$, integration gives

$$
\mathcal W(E):=\sqrt{a/2}\,[\zeta(u_+(E))-\zeta(u_-(E))]
     =\int_0^E x^{-1/2}V(x)\,dx. \tag{7}
$$

Conversely,

$$
V(E)=\sqrt E\,\mathcal W'(E),\qquad E>0, \tag{8}
$$

with its normalized smooth extension at zero. The leading term of $\mathcal W$ is $2\sqrt E$. Equations (7)–(8) show that a theorem recovering $V$ already recovers $\mathcal W$, and conversely. The latter interpretation identifies the geometry of the recovered measure, but does not add an independent datum.

For an even $S$ and even $B$, $\zeta$ is odd, so the unnormalized width gives both intrinsic inverse branches. In general it gives their difference, not their midpoint. Separate knowledge of $a$ is needed to recover the unnormalized width from (7).

## 5. An abstract equal-width calculation, with its scope kept explicit

For a small constant $\varepsilon$, set

$$
x=h_\varepsilon(t)=t+\frac{\varepsilon}{2}t^2,
\qquad
\widehat S_\varepsilon(x)=\frac12\bigl(h_\varepsilon^{-1}(x)\bigr)^2.
$$

The map $h_\varepsilon$ is an increasing smooth coordinate on a small interval. The potential has value and first derivative zero at the origin and second derivative one there; it is strictly convex after shrinking the interval. Its two inverse branches at energy $E$ are exactly

$$
x_\pm(E)=\pm\sqrt{2E}+\varepsilon E.
$$

Consequently,

$$
x_+(E)-x_-(E)=2\sqrt{2E},\qquad
\frac{x_+(E)+x_-(E)}2=\varepsilon E.
$$

All these wells have the same Lebesgue sublevel width and the same normalized profile $V(E)=1$, but different inverse-branch midpoints. For example,

$$
\widehat S_\varepsilon(x)=\tfrac12x^2-\tfrac{\varepsilon}{2}x^3+O(x^4).
$$

Any residual product integral depending only on their sublevel pushforward measures is therefore unchanged on a common small collar. The ambiguity is visible without replacing smooth functions by their formal jets.

**Scope:** these are abstract wells in the intrinsic coordinate. No claim is made that varying $\varepsilon$ is realizable by a Euclidean periodic billiard while keeping all the required half-line dynamics and leading data fixed. Such a statement would require a separate physical realization argument. The example is not a counterexample to the manuscript's analytic even-contact inverse, its physical finite-jet image, or its stated complete-profile theorem. It explains why a width, considered as a datum, must not be renamed unrestricted asymmetric boundary information.

## 6. Relation to classical literature and to the diagnostics

The classical smooth one-dimensional linearization regime is stated in the introduction of Eynard-Bontemps–Navas, [arXiv:2212.13646v2](https://arxiv.org/html/2212.13646v2). That paper studies failures at low regularity; those failures do not apply here. The proof above is included to make the comparison independent of a citation alone and to specify the family assumptions actually needed.

The rational part of `verify_review.py` tests two-type Möbius conjugacies, for which the densities and normalized iterate remainders are exact rational functions. Its width checks use rational values of $t$, so the energy $t^2/2$ and the two sheared branches are exact. The Euclidean part tests the physical identification numerically on finite stationary local graph bridges. None of those finite tests substitutes for the proofs or removes the physical-realization caveat in Section 5.
