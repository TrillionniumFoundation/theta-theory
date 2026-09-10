# Analytic normal-form benchmark for relative endpoint flux

**Companion to the independent A2 v13 referee report, 10 September 2026.**

**Reviewed source:** `0e54099f079232df233316ae6fe7986fc51b7ea1`, `papers/A2-v13-two-flight-relative-invariants`.

This note derives a restricted forward comparator. It is not a proof that the complete smooth physical theorem, geometric inverse, or statistical experiment of A2 is contained in an earlier publication. In particular, existence of uniformly parameter-dependent normalizing charts for an arbitrary smooth family is **not** assumed to follow from the analytic theorem cited below.

## 1. Input and precise scope

The local analytic normal form is recalled, with Moser–Sternberg attribution, in De Simoi–Kaloshin–Leguil, arXiv:1905.00890v4, printed p. 10; see p. 13 for its distinction from geometric symmetry requirements. This note uses the local statement, not the global inverse theorem.

Take an analytic canonical map

$$
N(s,p)=(\Delta(sp)s,\Delta(sp)^{-1}p),\qquad \Delta(0)=\lambda\in(0,1).
\tag{NF1}
$$

All coordinates are near zero. For an A2 two-step return, the contracting eigenvalue here is $\lambda=e^{-2\gamma}$; it is not the manuscript's one-flight abbreviation $e^{-\gamma}$. The calculation below concerns $n$ returns, hence the even-flight subsequence $j=2n$.

Suppose the physical initial and terminal canonical charts are

$$
(u,P)=\mathcal C_L(s,p),\qquad (v,Q)=\mathcal C_R(q,t),
\tag{NF2}
$$

with physical configuration projections $u=U(s,p)$ and $v=V(q,t)$. Assume

$$
U(0,0)=V(0,0)=0,\qquad U_s(0,0)V_t(0,0)\ne0.
\tag{NF3}
$$

These are transversality assumptions on the stable and unstable projections. They are not additional observations supplied to a statistical estimator. For a fixed analytic billiard, the nonvertical stable and unstable directions of its dispersing normal orbit give these local projection conditions. Equivalently, one can take (NF1)–(NF3) as the hypotheses of this benchmark without asserting a billiard application.

We prove exponential relative factorization on a fixed small physical endpoint box. Constants may depend on the charts and the requested finite derivative order. A parameter-uniform conclusion is obtained **only if** the normal-form functions and charts themselves are supplied as a uniformly bounded smooth parameter family, with uniform transversality and $\lambda$ in a compact subinterval of $(0,1)$.

## 2. Mixed-boundary equation and its exact derivative

Prescribe $s=s_0$ at the initial end and $t=p_n$ at the terminal end. Since $I=sp$ is invariant under (NF1),

$$
I=st\Delta(I)^n,\qquad p_0=t\Delta(I)^n,\qquad q=s_n=s\Delta(I)^n.
\tag{NF4}
$$

Choose $\lambda<\mu<1$ and a neighborhood where $0<\Delta\le\mu$. After shrinking the fixed $(s,t)$ box, the first equation is a contraction in $I$, uniformly in $n\ge1$. Indeed,

$$
|st|\,n\mu^{n-1}\|\Delta'\|_\infty<\tfrac12
$$

can be required for every $n$ because $\sup_n n\mu^{n-1}<\infty$. Its image remains in the chosen $I$ interval. The unique solution satisfies $|I|\le C\mu^n$. Its intermediate coordinates are $(s\Delta(I)^i,t\Delta(I)^{n-i})$, so the entire orbit remains in the fixed local box. Put

$$
a_n=\Delta(I)^n,\qquad D_n=1-nI\frac{\Delta'(I)}{\Delta(I)}.
$$

The contraction gives $|D_n|\ge1/2$. Differentiating (NF4) at fixed $s$ yields

$$
\boxed{\quad
\frac{\partial p_0}{\partial t}\bigg|_s
 =\frac{\Delta(I)^n}{1-nI\Delta'(I)/\Delta(I)}
 =:T_n(s,t).
\quad}
\tag{NF5}
$$

The formula extends across $s=0$: it is obtained by differentiating $p_0=t\Delta(I)^n$, not by dividing $I$ by $s$. The identical calculation gives $\partial q/\partial s=T_n$, consistent with a mixed generating function.

This is already a relative, rather than merely absolute, estimate. Since $\Delta(I)/\lambda=1+O(I)$,

$$
\frac{\Delta(I)^n}{\lambda^n}
 =\exp\{n\log(\Delta(I)/\lambda)\}=1+O(n\mu^n).
$$

Implicit differentiation of (NF4) at every fixed order leaves $D_n$ multiplying the highest derivative. The other terms contain derivatives of $\Delta$, derivatives of powers of $\Delta$, and previously bounded derivatives of $I$. Induction bounds them by a fixed polynomial in $n$ times $\mu^n$, after increasing a strict exponential margin when necessary. The same reasoning applies to (NF5) **after normalization by $\lambda^n$**. Thus, for a fixed $\sigma\in(\mu,1)$ and every fixed $k$,

$$
\|\lambda^{-n}T_n-1\|_{C^k}\le C_k\sigma^n.
\tag{NF6}
$$

For the parameter-family assertion in Section 1, derivatives of $\lambda$ introduce fixed powers of $n$. The identity $\Delta(0)/\lambda=1$ holds throughout the family, so the normalized difference still vanishes with $I$. These powers are absorbed by the same strict margin. This argument does not produce the parameter-dependent charts it assumes.

## 3. Transfer to physical configuration endpoints

Define the actual endpoint map in mixed coordinates by

$$
\Phi_n(s,t)=\big(U(s,t a_n),V(s a_n,t)\big).
\tag{NF7}
$$

It converges in every fixed derivative norm to

$$
\Phi_\infty(s,t)=\big(U(s,0),V(0,t)\big).
$$

Write $s=\alpha(u)$ and $t=\beta(v)$ for the inverses of these two limiting scalar projections. By (NF3), and by making the box small and $n$ sufficiently large, $\Phi_n$ has an inverse on a common smaller **nonshrinking** physical endpoint box. The inverse follows either from a fixed contraction around $\Phi_\infty^{-1}$ or from a Jacobian uniformly close to that of $\Phi_\infty$. It differs from $(\alpha(u),\beta(v))$ by an exponentially small term in each fixed derivative norm.

Set

$$
\mathcal D_n(s,t)=\det D_{s,t}\Phi_n(s,t).
$$

Canonicity of the initial chart gives $du\wedge dP=ds\wedge dp_0$. Pulling this equality back to $(s,t)$ gives the exact physical endpoint flux

$$
J_n(u,v):=\left|\frac{\partial P}{\partial v}\bigg|_u\right|
 =\left|\frac{T_n(s,t)}{\mathcal D_n(s,t)}\right|,
\qquad (s,t)=\Phi_n^{-1}(u,v).
\tag{NF8}
$$

In a billiard endpoint generating function, $P=-W_{n,u}$; hence $J_n=|W_{n,uv}|$. On the dispersing branch, it is the positive quantity $-W_{n,uv}$ used by A2. Formula (NF8) is the crucial projection step: canonical mixed-boundary coordinates must not be silently identified with physical endpoint positions.

At the normal orbit one has exactly

$$
\mathcal D_n(0,0)=U_s(0,0)V_t(0,0)
 -\lambda^{2n}U_p(0,0)V_q(0,0),\qquad T_n(0,0)=\lambda^n.
\tag{NF9}
$$

Since $\mathcal D_n$ stays bounded away from zero, (NF6)–(NF9) imply

$$
\left\|\frac{J_n(u,v)}{J_n(0,0)}-B_L(u)B_R(v)\right\|_{C^k}
 \le C_k\sigma^n,
\tag{NF10}
$$

where, with signs constant on the small neighborhoods,

$$
B_L(u)=\frac{U_s(0,0)}{U_s(\alpha(u),0)},\qquad
B_R(v)=\frac{V_t(0,0)}{V_t(0,\beta(v))}.
\tag{NF11}
$$

These factors are positive and normalized to one at zero. They are normalized inverse projection Jacobians of the two invariant axes.

For the same physical section, $V=U$, the determinant in (NF9) becomes $U_s(0,0)U_p(0,0)(1-\lambda^{2n})$. Thus the exact reference flux has the expected $\lambda^n/(1-\lambda^{2n})$ dependence, not just its leading exponential. This is consistent with the manuscript's $\operatorname{csch}(2n\gamma)$ reference normalization. The remaining constant is set by the linear physical chart.

## 4. Stationary action and the boundary interpretation

When the map is generated by the physical stationary action, its first variations are $W_{n,u}=-P$ and $W_{n,v}=Q$. Equations (NF4) and (NF7) show that these gradients converge respectively to a function of $u$ alone and a function of $v$ alone. Integrating those functions from the origin defines $S_L,S_R$. With $E_n=W_n-W_n(0,0)$ and $S_L(0)=S_R(0)=0$, integration of the gradient error along endpoint segments yields

$$
\|E_n-S_L\oplus S_R\|_{C^k}\le C_k\sigma^n.
\tag{NF12}
$$

For the convex dispersing endpoint problem, positive limiting action Hessians follow from its quadratic geometry. Under this additional physical condition, a common Morse-coordinate argument can transfer (NF10)–(NF12) through the normalized residual-time integral, as in the explicit transport proposition in `article/15_operator_comparison.tex`. That integration step is a further argument, not part of the normal-form existence theorem.

If A2's determinant construction and this benchmark are both applied to the same analytic physical endpoint problem, their normalized limiting fluxes must agree by uniqueness of limits. Evaluation at $v=0$ or $u=0$ identifies the individually normalized factors. This provides an analytic stable/unstable-projection interpretation of the half-line amplitudes. It does not identify the invariant normal-form function $\Delta$ alone with all of the physical boundary information: the projection charts matter.

## 5. What the comparison establishes, and what it does not

The qualitative phenomenon of an exponentially small twist having a nonlinear product limit on a fixed endpoint box is already accessible from classical analytic hyperbolic coordinates plus an explicit physical projection calculation. Consequently a comparison solely with elementary cofactor identities and global inverse-spectral theorems misses a relevant forward mechanism.

This note has **not** proved existence of a suitable jointly smooth normal form for all of A2's $C^\infty$ families, nor identified sharp uniform derivative bounds in that generality. It has not supplied A2's half-line Fredholm formula, global physical channel localization, a full odd-parity argument, the energy-profile inverse, independent-contact jet separation, physical realization, or charged binary acquisition. It does not assert that A2 is false or entirely known.

The referee request is to identify the actual theorem-level increment after this restricted comparator, not to replace the paper's valid smooth proof or require an unrelated new theorem.

**Primary source consulted:** De Simoi–Kaloshin–Leguil, arXiv:1905.00890v4, printed pp. 10 and 13, [versioned source](https://arxiv.org/abs/1905.00890v4). The original 1956 Moser article was not separately read in full for this review. The endpoint calculation (NF4)–(NF12) is derived in this memorandum rather than quoted from that source.
