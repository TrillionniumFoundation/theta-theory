# Higher pressure response and physical diffusion for suspensions over moving-singularity dynamics

## Abstract

Starting from the product-CM2 and U3 interface of Paper I, we derive the
physical-time spectral objects needed by homogenization.  We first stabilize a
finite Banach bundle inside one fixed direct-sum space; this removes the common
operator-space ambiguity that otherwise makes cross-parameter Kato calculus
ill-typed.  We then study the jointly twisted collision operator

\[
L_{a,q,s}h=L_a(e^{q\cdot\kappa_a-s\tau_a}h).
\]

Its simple leading eigenvalue gives a three-times differentiable pressure.  The
implicit physical-time root of that pressure produces drift and covariance,
while a renewal decomposition gives the low-frequency suspension resolvent.
We prove that the pressure Hessian, the continuous-time Green--Kubo tensor, and
the bracket of the Gordin martingale agree.  Their parameter derivative is
therefore controlled by the third-order response from Paper I.

Finally, a corrected Nemytskii lift turns the parameter coefficients into
`(x,p)` fields, and a spectral non-coboundary criterion yields uniform
ellipticity after macroscopic coupling.  The open four-branch moving-seam
family from Paper I provides an actual example with a strictly positive
physical diffusion coefficient.  No full high-frequency moving-flow graph
space is required or claimed.

---

## 1. Imported response interface

Let `A` be a compact parameter set.  We import the following outputs from
Paper I:

```text
P1-CM2      absolute double-time product summability
P1-FDQ      finite-DQ convergence in l1(N^2)
P1-U3       continuous first three operator/source derivatives
P1-RWORDS   continuous third-order reduced-resolvent words
```

The import applies on declared strong/source/test scales and includes a simple
isolated eigenvalue at one.  No unnamed moving-flow theorem is imported.

---

## 2. A genuine common operator realization

A family of fibre spaces `B_a` may be locally trivial without living in one
fixed operator space.  We give a finite-atlas stabilization that is sufficient
for Kato calculus.

### Assumption 2.1 (finite Banach atlas)

There are finitely many open parameter charts `U_alpha`, Banach spaces
`B_alpha`, and bounded isomorphisms

\[
G_{\alpha,a}:B_a\longrightarrow B_\alpha,
\qquad a\in U_\alpha,
\]

whose transition maps and inverses are uniformly bounded and `C^3` on compact
subcharts.  Let `chi_alpha` be a smooth partition of unity subordinate to the
atlas.

### Theorem 2.2 (finite-atlas stabilization)

Set

\[
B_*:=\bigoplus_{\alpha=1}^N B_\alpha
\]

and define

\[
J_ah=
\bigl(\sqrt{\chi_\alpha(a)}G_{\alpha,a}h\bigr)_\alpha,
\tag{2.1}
\]

\[
R_a(v_\alpha)_\alpha
=
\sum_{\alpha=1}^N
\sqrt{\chi_\alpha(a)}G_{\alpha,a}^{-1}v_\alpha.
\tag{2.2}
\]

Then

\[
R_aJ_a=I_{B_a}.
\tag{2.3}
\]

Consequently `E_a=J_aB_a` is a uniformly complemented subspace of `B_*`,

\[
P_a:=J_aR_a
\]

is the projection onto `E_a`, and every fibre operator `L_a` has the fixed-space
realization

\[
\widehat L_a:=J_aL_aR_a\in\mathcal L(B_*).
\tag{2.4}
\]

The maps `a -> J_a,R_a,P_a,widehat L_a` have the same parameter regularity as
the atlas and the original operator family.

#### Proof

For `h in B_a`,

\[
R_aJ_ah
=
\sum_\alpha\chi_\alpha(a)
G_{\alpha,a}^{-1}G_{\alpha,a}h
=h.
\]

Thus `P_a^2=J_aR_aJ_aR_a=P_a`, and its range is `E_a`.  Uniform bounds follow
from finiteness of the atlas and the transition bounds.  Differentiation of
(2.1)--(2.4) is a finite product rule.  This gives a fixed ambient operator
space without identifying different fibres by an unjustified canonical
subtraction.

### Remark 2.3

A fixed-image trivialization is the special case `E_a=E_*`.  The stabilization
above also covers genuinely moving images.

---

## 3. Jointly twisted collision operators

Let

\[
\kappa_a:M\to\mathbb R^d
\]

be a displacement observable and

\[
\tau_a:M\to(0,\infty)
\]

a roof function.  Assume they and all multipliers needed through total order
three act boundedly on the Paper-I scales.  Define

\[
L_{a,q,s}h
=L_a\left(e^{q\cdot\kappa_a-s\tau_a}h\right),
\tag{3.1}
\]

for `(q,s)` in a small complex neighbourhood of zero.

### Assumption 3.1 (spectral window)

On the stabilized space, `widehat L_{a,q,s}` has a simple leading eigenvalue
`lambda(a,q,s)` separated by a uniform contour from the rest of the spectrum.
At `(q,s)=(0,0)`, `lambda=1`.

Define the pressure

\[
\mathscr P(a,q,s)=\log\lambda(a,q,s),
\tag{3.2}
\]

with the branch satisfying `mathscr P(a,0,0)=0`.

### Theorem 3.2 (three-jet pressure response)

Under Paper I, Theorem 2.2, and Assumption 3.1, the maps

\[
(a,q,s)\mapsto
\lambda,\quad \Pi_{a,q,s},\quad R_{a,q,s}^{\perp},\quad
\mathscr P
\]

are `C^3` on the real parameter window.  Each derivative of total order at
most three is a finite sum of:

1. a direct derivative of the twisted operator;
2. a contour/Riesz projection term;
3. reduced-resolvent words made from the first three source operators.

#### Proof

Paper I gives continuous derivatives of the stabilized operator through order
three, including the moving-singularity currents.  The Riesz projection is

\[
\Pi_{a,q,s}
=
\frac1{2\pi i}\int_\Gamma
(z-\widehat L_{a,q,s})^{-1}\,dz.
\]

Differentiate the resolvent identity

\[
D(z-L)^{-1}=(z-L)^{-1}(DL)(z-L)^{-1}.
\]

At orders two and three this produces exactly the finite words controlled by
`P1-RWORDS`.  Uniform contour separation permits differentiation under the
integral.  A normalized left/right eigenpair then gives the eigenvalue and its
logarithm.

---

## 4. Physical-time pressure root

Let `Lambda_a(q)` be the small solution of

\[
\mathscr P(a,q,\Lambda_a(q))=0.
\tag{4.1}
\]

Since

\[
\partial_s\mathscr P(a,0,0)
=-\int\tau_a\,d\mu_a
=-\bar\tau_a<0,
\tag{4.2}
\]

the implicit-function theorem applies.

### Theorem 4.1 (physical drift and covariance)

The map `(a,q)->Lambda_a(q)` is `C^3`.  Its first derivative is the physical
mean velocity.  In the centered convention

\[
\partial_{q_i}\mathscr P(a,0,0)=0,
\]

one has

\[
D_q\Lambda_a(0)=0
\]

and

\[
\Sigma_{ij}(a)
:=\partial_{q_iq_j}\Lambda_a(0)
=
\frac{\mathscr P_{q_iq_j}(a,0,0)}{\bar\tau_a}.
\tag{4.3}
\]

The physical diffusion matrix is

\[
D^{\rm phys}(a)=\frac12\Sigma(a).
\tag{4.4}
\]

Moreover,

\[
\boxed{
\partial_a\Sigma_{ij}
=
\frac{\mathscr P_{a q_iq_j}}{\bar\tau}
-
\frac{\mathscr P_{q_iq_j}\,\partial_a\bar\tau}
     {\bar\tau^2}.
}
\tag{4.5}
\]

#### Proof

Differentiate (4.1).  At `q=0`, the first derivative vanishes by centering.
The second derivative satisfies

\[
0=\mathscr P_{q_iq_j}
 +\mathscr P_s\Lambda_{q_iq_j},
\]

which gives (4.3) using (4.2).  Differentiate (4.3) in `a` to obtain (4.5).
The mixed derivative `mathscr P_{a q_iq_j}` has total order three and is
therefore exactly within the U3 interface.

---

## 5. The low-frequency suspension resolvent

Let

\[
M_a^\tau=\{(x,u):0\le u<\tau_a(x)\}/\sim
\]

be the suspension and `Phi_a^t` its flow.  For a flow observable `F`, define
its roof-cell Laplace transform

\[
\widehat F_{a,z}(x)
=
\int_0^{\tau_a(x)}e^{-zu}F(x,u)\,du.
\tag{5.1}
\]

Set

\[
L_{a,z}h=L_a(e^{-z\tau_a}h).
\tag{5.2}
\]

### Proposition 5.1 (renewal decomposition)

For observables supported in the declared roof-cell class, the Laplace
transform of the correlation function has the form

\[
\widehat C_{F,G}(a,z)
=H_{a,z}^{\rm same}(F,G)
+
\left\langle
\widehat F_{a,z},
(I-L_{a,z})^{-1}\widehat G_{a,z}
\right\rangle,
\tag{5.3}
\]

where `H^same` contains only pairs of points in the same or adjacent finite
roof cells.

#### Proof

Split every flow segment according to the number of completed returns to the
section.  Zero completed returns give `H^same`.  A segment with `n>=1` returns
contributes the `n-1`st iterate of `L_{a,z}` between the roof-integrated entry
and exit observables.  Summing the geometric series gives (5.3).

Near `z=0`, write

\[
(I-L_{a,z})^{-1}
=
\frac{\Pi_{a,z}}{1-\lambda(a,0,z)}
+R_{a,z}^{\perp}.
\tag{5.4}
\]

For centered correlations the pole cancels against the mean term.

### Theorem 5.2 (low-frequency suspension response)

Under the Paper-I U3 interface and roof multiplier regularity, the centered
quantity in (5.3), the reduced resolvent in (5.4), and all derivatives of total
order at most three in `(a,z)` are continuous for `z` in a neighbourhood of
zero.  In particular, integrated flow correlations and their parameter
responses exist.

#### Proof

The finite roof-cell term is differentiated by ordinary Leibniz and endpoint
rules.  The long-return term is a collision twisted resolvent and is covered by
Theorem 3.2.  Pole cancellation on the centered subspace is uniform because
`partial_z lambda(a,0,0)=-bar tau_a` stays away from zero.

### Scope statement

The theorem is the low-frequency result needed for physical diffusion and
homogenization.  It does not assert a complete high-frequency moving-family
Dolgopyat/BDL graph-domain theorem.

---

## 6. Three equal covariance formulas

Let `kappa_a` be centered.  Define the collision Green--Kubo matrix

\[
C_{ij}^{\rm coll}(a)
=
\int\kappa_{a,i}\kappa_{a,j}\,d\mu_a
+
\sum_{n\ge1}
\int\left(
\kappa_{a,i}\,\kappa_{a,j}\circ T_a^n
+
\kappa_{a,j}\,\kappa_{a,i}\circ T_a^n
\right)d\mu_a.
\tag{6.1}
\]

Absolute convergence follows from Paper I and the spectral gap.

### Theorem 6.1 (pressure--Green--Kubo--bracket identity)

One has

\[
\mathscr P_{q_iq_j}(a,0,0)
=C_{ij}^{\rm coll}(a).
\tag{6.2}
\]

Let `chi_a` solve the Poisson equation on the centered subspace and let
`m_a` be the associated Gordin martingale difference.  Then

\[
C^{\rm coll}(a)
=\int m_a\otimes m_a\,d\mu_a.
\tag{6.3}
\]

Consequently

\[
\Sigma(a)=\frac{C^{\rm coll}(a)}{\bar\tau_a}
\tag{6.4}
\]

is simultaneously the pressure Hessian per unit physical time, the
continuous-time Green--Kubo tensor, and the limiting martingale bracket.

#### Proof

Differentiate the eigenvalue equation twice in `q`.  The first derivative is
zero by centering.  The second derivative is the instantaneous covariance plus
the two reduced-resolvent insertions, whose Neumann series gives (6.1).
Solving the Poisson equation and expanding the square of the martingale
increment telescopes the same correlation series, proving (6.3).  Dividing by
mean roof time gives (6.4).

### Corollary 6.2 (positivity and coboundary kernel)

`Sigma(a)` is positive semidefinite.  For a vector `xi`,

\[
\xi^T\Sigma(a)\xi=0
\]

if and only if `xi dot kappa_a` is a coboundary in the declared spectral
class.  Thus a uniform non-coboundary margin on a compact parameter set gives
uniform positive definiteness.

---

## 7. From parameter coefficients to `(x,p)` fields

Let `K` be a compact slow/cotangent window and let

\[
\Theta:K\to A
\]

be a `C^{3,alpha}` selector.  At this stage `p` is an external cotangent
signal; it is not yet identified with the gradient of an unknown HJB solution.

Let `B(x,p)` be a macroscopic coupling matrix and set

\[
A(x,p)
=\frac12B(x,p)\Sigma(\Theta(x,p))B(x,p)^T.
\tag{7.1}
\]

### Theorem 7.1 (coefficient lift)

If the parameter coefficients and `Theta,B` have the stated
`C^{3,alpha}` regularity, then `A`, the effective drift, the area anomaly, and
the roof-normalized response coefficients are `C^{3,alpha}` on `K`.

#### Proof

After Theorem 2.2 all parameter coefficients are maps between fixed finite or
Banach spaces.  The corrected Hölder Nemytskii theorem and the ordinary finite-
dimensional chain rule apply to the composition with `Theta`; products with
`B` preserve the same regularity.

### Theorem 7.2 (ellipticity transfer)

Assume

\[
\Sigma(a)\ge\lambda_\Sigma I_d
\]

on `A` and

\[
B(x,p)B(x,p)^T\ge\lambda_B^2I_m
\]

on `K`.  Then

\[
A(x,p)\ge
\frac12\lambda_\Sigma\lambda_B^2I_m.
\tag{7.2}
\]

#### Proof

For `z in R^m`,

\[
z^TAz
=\frac12(B^Tz)^T\Sigma(B^Tz)
\ge\frac12\lambda_\Sigma|B^Tz|^2
\ge\frac12\lambda_\Sigma\lambda_B^2|z|^2.
\]

---

## 8. Actual coefficient package for the four-branch family

Use the Paper-I family and choose

\[
\kappa(y)=\cos(2\pi y),
\qquad
\tau_a(y)=1+\delta\sin(2\pi y)+\delta_1a,
\tag{8.1}
\]

with `|delta|+|delta_1|/40<1/2`.  The roof is uniformly positive and all
multipliers are bounded on the fixed-cut scales.

The point `y=0` is a fixed point of the first branch and

\[
\kappa(0)=1.
\]

Since `int kappa=0`, a coboundary identity

\[
\kappa=\psi-\psi\circ T_a
\]

would give `kappa(0)=0`, a contradiction.  Hence the scalar asymptotic variance
is positive for every parameter.  Continuity and compactness give

\[
\inf_{a\in I}\Sigma(a)>0.
\]

### Theorem 8.1 (actual pressure, suspension, and diffusion response)

For the open moving-seam family with data (8.1):

1. the twisted pressure is `C^3` in `(a,q,s)`;
2. the low-frequency suspension resolvent has `C^3` parameter response;
3. the physical diffusion coefficient is strictly positive and `C^1` in `a`;
4. formula (4.5) gives its derivative;
5. every smooth compact selector into `I` generates a smooth uniformly
   elliptic coefficient field after any full-rank macroscopic coupling.

#### Proof

Paper I gives actual U3.  The roof and displacement satisfy the finite
multiplier hypotheses, so Theorems 3.2--7.2 apply.  The fixed-point argument
proves non-coboundary and hence strict positivity.

---

## 9. Exported interface

Paper III may import only:

```text
P2-COMMON      fixed common operator realization
P2-PRESSURE3   C3 twisted pressure and reduced resolvent
P2-SUSP0       low-frequency suspension response
P2-PHYS        physical drift/covariance/diffusion response
P2-COEFF       C3alpha (x,p) coefficient fields
P2-ELL         uniform ellipticity under explicit rank/noncoboundary margins
P2-ACTUAL-4B   actual moving-seam coefficient package
```

No full high-frequency moving-flow theorem is exported.

---

## 10. Conclusion

Paper I controls moving singularities at the collision level.  The present
paper converts that response into physical-time spectral and probabilistic
objects, while repairing the common-space problem needed for parameter
composition.  The resulting pressure root, suspension resolvent, and diffusion
field are precisely the frozen inputs required by nonautonomous rough
homogenization; no HJB or stochastic representation has been used in their
construction.
