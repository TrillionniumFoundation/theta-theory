# Actual nonconjugate specular finite-horizon Sinai U3

## 0. Result and scope

This note closes the specular-Sinai strengthening at its maximal valid scope.
It proves an actual all-order response theorem for the invariant projector and
for exact-coboundary twists in a genuinely nonconjugate radial family.  The
proof uses complete differentiated-invariance assemblies, so the moving
singularity currents are present and cancel only after the physical response
word is assembled.  It does not claim that arbitrary noncoboundary twists have
third response from local geometry alone.

The main theorem is denoted

```text
SINAI-RADIAL-ASSEMBLED-U-INFINITY-1.
```

Its order-three consequence is the requested actual U3 packet.

---

## 1. Radial family and fixed collision coordinates

Let `Q_a` be a `C^{J+6}` family of planar periodic finite-horizon dispersing
billiard tables, `a in (-a_0,a_0)`.  All scatterers except `D_1(a)` are fixed,
and

\[
D_1(a)=\{x:|x-c_1|\le R_1+a\}.
\]

Choose `a_0` so that the scatterers remain disjoint, the curvature is bounded
away from zero, and the horizon is uniformly finite.  The collision space is

\[
M_a=\bigsqcup_{i=1}^N\partial D_i(a)\times
[-\pi/2,\pi/2].
\]

Parametrize every boundary component by a fixed normalized coordinate
`s in T_i`; thus

\[
dr_a=\ell_i(a)\,ds,
\qquad
\ell_1(a)=2\pi(R_1+a),
\]

and `ell_i(a)` is constant for `i>1`.  This transports every `M_a` to the
fixed measurable manifold

\[
M=\bigsqcup_i\mathbb T_i\times[-\pi/2,\pi/2].
\]

Write `L_a` for the transported Perron--Frobenius operator with respect to
`dm=ds dphi`.  Its invariant probability density is explicit:

\[
\boxed{
\rho_a(s,\varphi)
=
\frac{\ell_i(a)\cos\varphi}
{2\sum_j\ell_j(a)}
\quad\text{on }\mathbb T_i\times[-\pi/2,\pi/2].
}
\tag{1.1}
\]

Hence `a -> rho_a` is `C^infinity` in every ordinary smooth density norm and

\[
L_a\rho_a=\rho_a,
\qquad
\int_M\rho_a\,dm=1.
\tag{1.2}
\]

The table family is not assumed conjugate.

---

## 2. Explicit nonconjugacy witness

Choose a non-grazing period-two orbit along the line joining the centers of the
inflated circle and a fixed circular scatterer of radius `R_2`.  Let the center
distance be `d`, and put

\[
\tau(a)=d-(R_1+a)-R_2,
\qquad
\kappa_1(a)=\frac1{R_1+a},
\qquad
\kappa_2=\frac1{R_2}.
\]

In paraxial Jacobi coordinates, free flight and reflection are represented by

\[
F(\tau)=
\begin{pmatrix}1&\tau\\0&1\end{pmatrix},
\qquad
C(\kappa)=
\begin{pmatrix}1&0\\2\kappa&1\end{pmatrix}.
\]

The round-trip monodromy is

\[
M(a)=C(\kappa_1(a))F(\tau(a))
C(\kappa_2)F(\tau(a)),
\]

and

\[
\operatorname{tr}M(a)
=2+4\kappa_1\tau+4\kappa_2\tau
 +4\kappa_1\kappa_2\tau^2.
\tag{2.1}
\]

Direct differentiation gives

\[
\boxed{
\frac d{da}\operatorname{tr}M(a)\bigg|_{a=0}
=-\frac{4d(d-R_2)}{R_1^2R_2}\ne0.
}
\tag{2.2}
\]

The hyperbolic multiplier of a periodic orbit is invariant under a smooth
conjugacy.  Thus the radial family is genuinely nonconjugate.

---

## 3. Distributional parameter letters

The moving singularity sets prevent `a -> L_a` from being differentiable as a
bounded operator on one ungraded density space.  The collision source calculus
nevertheless defines, for a smooth input `h`, the distributional letters

\[
L_0^{[k]}h
=
\partial_a^k(L_ah)|_{a=0},
\qquad 1\le k\le J,
\tag{3.1}
\]

as finite sums of interior terms, one-face conormal currents, clean
intersection currents, and endpoint terms.  They are first defined against
smooth tests and then placed in the label-resolved source module.

An individual letter need not be a strong density.  Only the complete physical
assembly below is claimed strong.

---

## 4. Differentiated-invariance assembly

Differentiate the exact identity `L_a rho_a=rho_a` `j` times.  The Leibniz rule
in the distributional source module gives

\[
\sum_{k=0}^{j}\binom jk
L_0^{[k]}\rho_0^{(j-k)}
=\rho_0^{(j)}.
\tag{4.1}
\]

Define the complete order-`j` moving-singularity source

\[
S_j
=
\sum_{k=1}^{j}\binom jk
L_0^{[k]}\rho_0^{(j-k)}.
\tag{4.2}
\]

Then

\[
\boxed{
S_j=(I-L_0)\rho_0^{(j)}.
}
\tag{4.3}
\]

The right-hand side is an ordinary smooth centered density.  Therefore all
face, intersection, endpoint, and terminal currents in the left-hand complete
assembly cancel in the represented source space.  Since

\[
\int\rho_a\,dm=1,
\]

we also have

\[
\int S_j\,dm=0.
\tag{4.4}
\]

Let

\[
R_0=(I-L_0)^{-1}(I-\Pi_0)
\]

be the reduced collision resolvent on the centered strong density space.
Equation (4.3) gives the exact Poisson recovery

\[
\boxed{
R_0S_j=\rho_0^{(j)}.
}
\tag{4.5}
\]

Here `Pi_0 rho_0^{(j)}=0` for `j>=1`.

### Theorem 4.1 (all-order assembled invariant response)

For every finite `J` allowed by the boundary smoothness and the finite-order
source chart, the complete sources `S_1,...,S_J` are centered strong densities
and satisfy (4.5).  Consequently the invariant projector

\[
\Pi_a h=\rho_a\int_Mh\,dm
\tag{4.6}
\]

is `C^J` as a map from the declared observable space to the strong density
space.

#### Proof

Formula (1.1) gives `rho_a in C^J`.  Finite-order branch differentiation gives
(4.1) in distributions.  Rearrangement yields (4.3), whose right-hand side is
strong.  The spectral gap on centered strong densities gives (4.5).  Finally,
(4.6) is explicit.

### Corollary 4.2 (actual radial U3)

At `J=3`, the nonconjugate specular radial family has an actual third-order
moving-singularity source, an actual third derivative of the invariant
projector, and well-typed reduced-resolvent recovery.  This is an actual U3
channel, not a conjugacy or zero-source model.

---

## 5. Exact-coboundary twisted U-infinity

Let `g_a` be a `C^J` family of bounded branchwise smooth functions and define
the collision coboundary

\[
\kappa_a=g_a-g_a\circ T_a.
\tag{5.1}
\]

For complex `q` near zero, let

\[
L_{a,q}h=L_a(e^{q\kappa_a}h).
\]

The transfer identity

\[
L_a((\psi\circ T_a)h)=\psi L_ah
\]

gives the exact gauge conjugacy

\[
\boxed{
L_{a,q}
=M_{e^{-qg_a}}L_aM_{e^{qg_a}}.
}
\tag{5.2}
\]

Hence the leading eigenvalue remains one, while the eigenprojector is

\[
\boxed{
\Pi_{a,q}
=M_{e^{-qg_a}}\Pi_aM_{e^{qg_a}}.
}
\tag{5.3}
\]

All mixed derivatives `partial_a^r partial_q^s Pi_{a,q}` with `r+s<=J`
exist explicitly.  The corresponding reduced resolvent is

\[
R_{a,q}
=M_{e^{-qg_a}}R_aM_{e^{qg_a}}
\tag{5.4}
\]

on the gauge-transformed centered space.

### Theorem 5.1 (actual twisted U-infinity channel)

The nonconjugate radial specular family has an actual all-order twisted
spectral response for every exact-coboundary channel (5.1).  The channel is
nonzero at the operator level even though its pressure is identically zero.

---

## 6. Why this does not imply generic noncoboundary U3

The previous response audit proves that, on the dynamically cut weighted
primitive/Poisson-pullback graph domain, the local moving-face gluing map is
split surjective onto smooth face profiles.  Its passing kernel is complemented
and infinite-codimensional, and the affine defect repeats at every source-jet
order.  Therefore finite-horizon geometry, compactness, parity, or a finite
list of Ward identities cannot force arbitrary third sources to recover.

### Theorem 6.1 (maximality)

There is no theorem of the form

```text
uniform finite-horizon specular geometry
+ finite boundary smoothness
=> all noncoboundary moving-scatterer U3 sources recover.
```

A correct noncoboundary theorem must additionally provide either

1. a complete source-specific assembly such as (4.2), or
2. the bilateral product-tail/third-source packet of Paper I.

#### Proof

The split-surjective gluing map realizes arbitrary face defects on the stated
weighted graph domain.  Its complement is open and dense.  At the next jet,
the admissible source is an affine translate of another infinite-codimensional
kernel.  Hence primitive geometry alone does not imply the needed cancellation.

---

## 7. Export

The new export is

```text
P1-SINAI-RADIAL-U3
```

with fields:

```yaml
ambient_system: nonconjugate_specular_finite_horizon_Sinai_radial_family
response_type:
  - invariant_projector_U_infinity
  - exact_coboundary_twisted_U_infinity
moving_singularity_assembly: differentiated_invariance
actual_order_three: true
generic_noncoboundary_upgrade: requires_P1_CM2_third_source_packet
```

This export may be used downstream only for invariant/coboundary channels or
for claims that separately supply the noncoboundary Paper-I packet.
