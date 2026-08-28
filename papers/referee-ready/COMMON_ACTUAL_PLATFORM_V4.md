# Common actual platform for the five θ-Theory papers — revision v4

## 1. Purpose

This file fixes the actual system used by the complete positive chain.  It is
not a theorem substitute.  Each assertion below points to a theorem proved in
one of the five controlling `main.tex` files.

The platform has three deterministic factors:

1. a nonconjugate symplectic Markov collision map carrying moving seams;
2. an optional noncompact hidden-state product shift used by the filtering
   paper;
3. the slow state recursion and control/game coordinates.

Probability is the invariant reference law of this deterministic product
system.  There is no externally substituted i.i.d. process in the end-to-end
chain.

## 2. The moving collision factor

For

```text
I = [-1/40,1/40]
```

define

```text
w_1(a)=1/10+a,
 w_2(a)=1/5+2a,
 w_3(a)=3/10-a,
 w_4(a)=2/5-2a.
```

Let `s_0=0`, `s_i=sum_{j<=i} w_j`, and

```text
T_a(x)=(x-s_{i-1}(a))/w_i(a),
       x in [s_{i-1}(a),s_i(a)).
```

The two-dimensional invertible collision map is

```text
B_a(x,y)=(T_a(x),s_{i-1}(a)+w_i(a)y).
```

Each branch has derivative

```text
diag(1/w_i(a), w_i(a)),
```

so `B_a` is area preserving and uniformly hyperbolic.  Its vertical and
horizontal seams move with the parameter.  The mapping-torus suspension with a
positive bounded roof is a deterministic finite-flight collision flow.

The unstable quotient transfer operator is

```text
(L_a h)(y)=sum_i w_i(a)h(s_{i-1}(a)+w_i(a)y).
```

Lebesgue measure is invariant.  The maximum branch width is `9/20`, which gives
the uniform centered contraction on every periodic `W^{r,1}` level.

## 3. Nonconjugacy

Branches two and three contain regular interior fixed points.  Their unstable
multipliers are respectively

```text
1/w_2(a), 1/w_3(a).
```

On the parameter interval, the multiplier ranges are disjoint and both vary
strictly.  A `C^1` conjugacy cannot exchange the fixed points and must preserve
their multipliers.  Distinct parameters are therefore not `C^1` conjugate.

This nonconjugacy is used in Paper I only as a geometric identity check; all
response estimates are proved independently by operator formulas.

## 4. All-order operator response

For

```text
v=(1,2,-1,-2),
A_i=sum_{j<=i}v_j,
r_i(y)=A_{i-1}+v_i y,
psi_i^a(y)=s_{i-1}(a)+w_i(a)y,
```

Paper I proves

```text
partial_a^k L_a h
 = sum_i [k v_i r_i^{k-1} h^{(k-1)}(psi_i^a)
          +w_i(a)r_i^k h^{(k)}(psi_i^a)].
```

Hence

```text
partial_a^k L_a : W^{r+k,1} -> W^{r,1}
```

and every letter is centered.  Together with the contraction of `Q_a`, this
gives

```text
|<Q_a^n (partial_a^k L_a) Q_a^m g,f>|
 <= C rho^{m+n} ||g||_{W^{r+k,1}} ||f||_{(W^{r,1})*}.
```

Consequences proved in Paper I:

- complete finite-DQ convergence;
- arbitrary finite spectral jets;
- repeated insertion on the same invariant ladder;
- arbitrary independently prescribed correlation susceptibility;
- no need for an assembly reset or a cohomological source hypothesis.

## 5. Exact predictable innovations

Let `A_k` be any parameter measurable with respect to the previous branch
history.  Start the fast unstable coordinate with the Lebesgue law and iterate

```text
X_{k+1}^f=T_{A_k}(X_k^f).
```

Paper I proves inductively:

```text
Law(X_k^f | past)=Lebesgue,
P(I_k=i | past)=w_i(A_k),
Law(X_{k+1}^f | past,I_k)=Lebesgue,
```

and the last variable is independent of the enlarged past.  Therefore every
centered branch vector is an exact martingale difference with its displayed
predictable covariance.

The Doob-selected branch probabilities

```text
p_i(a,zeta)=w_i(a)e^{zeta.c_i}/sum_j w_j(a)e^{zeta.c_j}
```

are again positive full-cover branch widths.  The exact innovation theorem
therefore applies to predictable Doob parameters as well.

## 6. Pressure, roof, and physical covariance

Choose branchwise displacement vectors `c_i(a)` and positive roof values
`tau_i(a)`.  Paper II proves the explicit pressure formula

```text
P(a,q,s)=log sum_i w_i(a) exp(q.c_i(a)-s tau_i(a)).
```

The physical-time root `Lambda_a(q)` solves

```text
P(a,q,Lambda_a(q))=0.
```

For centered displacement,

```text
Sigma_ij(a)=P_{q_i q_j}(a,0,0)/bar_tau(a).
```

The collision covariance is the finite one-step variance

```text
C_coll(a)=sum_i w_i(a)(c_i-bar_c) tensor (c_i-bar_c).
```

Paper II identifies it simultaneously with the symmetrized Green--Kubo series,
the pressure Hessian, the asymptotic variance, and the Gordin martingale
bracket.

For dimensions larger than three, take a finite Cartesian product of copies of
the four-branch collision map.  The product remains a nonconjugate symplectic
Markov collision map, its transfer operator is the tensor product, exact
innovations tensorize, and branch vectors can be chosen so that the covariance
is uniformly positive in any prescribed finite dimension.

## 7. Full-frequency suspension

For branchwise roofs, the twisted operator is

```text
L_{a,z}h=sum_i w_i(a)e^{-z tau_i(a)}
          h(s_{i-1}(a)+w_i(a)y).
```

The constants form a scalar block

```text
lambda_a(z)=sum_i w_i(a)e^{-z tau_i(a)},
```

while the quotient by constants contracts uniformly.  A Diophantine roof
vector gives a polynomial lower bound on `|1-lambda_a(ib)|`.  The block inverse
therefore gives a full-frequency resolvent and all finite parameter
derivatives.  The oriented renewal formula converts this operator estimate to
the suspension correlation response.

## 8. Slow recursion and rough limit

Let `Theta` be a globally Lipschitz parameter selector and define

```text
A_k=Theta(X_k^epsilon),
X_{k+1}^epsilon
 =X_k^epsilon+epsilon m_{I_k}(A_k)+epsilon^2 b(X_k^epsilon).
```

The exact innovation theorem gives the martingale differences and predictable
bracket.  Paper III proves the canonical geometric enhanced martingale limit,
including the diagonal one-half tensor term, and obtains the limiting SDE/RDE.

The pressure covariance of Paper II and the martingale covariance of Paper III
are the same finite branch matrix.

## 9. Microscopic theta recursion

For a terminal payoff, Paper III defines

```text
(T_h phi)(x)
 =(1/theta) log sum_i w_i(Theta(x))
  exp(theta phi(x+h b(x)+sqrt(h)m_i(Theta(x)))).
```

The finite-horizon backward recursion is the microscopic value problem.  It is
pointwise, monotone, cash invariant, and stable.  Taylor expansion gives the
complete consistency operator.  Its limit is

```text
-u_t-b.Du-(1/2)Sigma:D2u
 -(theta/2)Du^T Sigma Du=0.
```

A compact-control supremum of the same one-step collision evaluations produces
the controlled theta-semigroup.

## 10. Hidden-state extension

For Paper IV, take a deterministic product shift whose coordinates realize

```text
P(y,.)=delta gamma+(1-delta)N(ry,1-r^2).
```

The common refresh component supplies TV contraction.  The autoregressive
component supplies genuine memory and a quadratic Lyapunov drift.  The
observation likelihood

```text
g_o(y)=(1+o epsilon_o tanh y)/2
```

is bounded above and below.  The product of this shift with the collision map
is the actual partially observed deterministic platform.

## 11. Pure game extension

Controls enter the slow drift, covariance, and running payoff.  The local
mechanical payoff is

```text
F=F_0-(mu/2)|u|^2+(nu/2)|v|^2.
```

When the actuator curvatures dominate the unfavourable Hessians of `F_0`, the
saddle variational inequality is strongly monotone.  It has a unique pure
Lipschitz selector.  The lower and upper finite collision-game schemes converge
to the same pure Isaacs equation.

In the one-dimensional energy model,

```text
F(p;u,v)=p(u+v)-(mu/2)u^2+(nu/2)v^2,
```

and

```text
H(p)=(1/2)(mu^{-1}-nu^{-1})p^2.
```

The Hamiltonian is concave when `mu>nu`.

## 12. Tangent laws

For every microscopic collision path law `P_h`, Paper V defines

```text
dQ_h^phi/dP_h
 = exp(theta phi(X_T^h))/E exp(theta phi(X_T^h)).
```

The exact finite recursion gives the first and second terminal derivatives as
expectation and covariance under this law.  The collision homogenization
implies convergence of `P_h`, and bounded exponential tilting implies
convergence of `Q_h^phi`, the derivative operators, and their finite-time
cocycles.

The continuum law has density process

```text
M_s=exp(theta u(s,X_s)-theta u(t,x)),
```

which Paper V proves is a uniformly integrable stochastic exponential.  This is
the tangent-law Girsanov theorem.

## 13. Companion physical specular class

Papers I--II also contain an independent stronger geometric application:
analytic no-eclipse open dispersing billiards.  Symbolic desingularization puts
the family on one fixed Hölder shift space.  Ruelle perturbation gives
all-order response, while a temporal-shear condition gives a uniform
moving-family Dolgopyat resolvent.  This class is not needed to establish the
nonemptiness of the end-to-end Markov collision chain; it proves that the new
response mechanism also applies to a genuine moving specular billiard.

## 14. Dependency statement

The common actual chain is:

```text
moving collision response
 -> pressure / physical covariance / suspension
 -> exact-innovation rough homogenization
 -> microscopic HJB / theta-semigroup
 -> filtering and pure Isaacs game
 -> tangent laws / Girsanov / BSDE / PPDE.
```

Every arrow has an actual object on this platform.  The representation layer is
strictly downstream and is not used to prove the HJB limit.
