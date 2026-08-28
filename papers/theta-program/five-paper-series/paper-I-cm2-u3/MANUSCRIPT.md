# Bilateral graph-current mixing and higher response for systems with moving singularities

## Abstract

We introduce a bilateral criterion for parameter response in systems whose
singularity sets move.  The derivative of the transfer operator is decomposed
into same-occurrence graph-current atoms.  A reverse estimate contracts the
past variable while allowing forward graph growth, and a forward estimate
contracts the future variable while allowing backward graph growth.  A strict
crossed-rate inequality converts these two one-sided estimates into a genuine
product tail in the two time variables.  This yields absolute summability of
the response array, convergence of finite-difference arrays in
`l1(N^2)`, and a direct third-source totalization theorem.  The latter produces
a continuous third derivative of the reduced spectral data, denoted U3.

The abstract result is nonempty.  We prove it for an open four-branch
pinball-cylinder family with three moving physical seams.  Its source is a
nonzero saltus current for every parameter, its first three operator
derivatives lose only finitely many derivatives, and its centered transfer
operator contracts uniformly on a fixed-cut Sobolev--BV scale.  Consequently
the family has uniform product-CM2, full finite-DQ convergence, and actual U3.
The theorem does not claim an unrestricted universal result for all moving
scatterers; such a claim is excluded by the rate-gap and totalization
obstructions recorded below.

---

## 1. The response problem

Let `A` be a compact parameter interval.  For `a in A`, let

\[
T_a:M\longrightarrow M
\]

be a piecewise smooth nonsingular map with transfer operator `L_a`, invariant
rank-one projection `Pi_a`, and centered operator

\[
Q_a=L_a-\Pi_a.
\]

The singularity partition is allowed to move with `a`.  After transporting all
fibres to a common measurable model, a parameter derivative is not merely a
branch-interior differential operator.  It has the form

\[
\partial_aL_a
=K_a^{\rm reg}
 +\sum_{\omega\in\Omega_a}J_{a,\omega},
\tag{1.1}
\]

where `J_{a,omega}` is a graph current supported on a physical moving face or
one of its recovered descendants.  The label `omega` contains the physical
face, incident side, owner, branch word, homogeneity itinerary, orientation,
and parameter chamber.  Terms with different occurrence labels are never
cancelled before the estimates are proved.

For centered `g` and a test `f`, the basic two-time atom is

\[
A_{m,n}^{\omega}(a;g,f)
 =\left\langle Q_a^nJ_{a,\omega}Q_a^mg,f\right\rangle .
\tag{1.2}
\]

An additive estimate such as `rho^m+rho^n` is not sufficient: its double sum
diverges.  The purpose of CM2 is to obtain a product estimate.

---

## 2. The bilateral packet

We use two Banach scales.  `X_-` controls the source-side history and `X_+`
controls target-side propagation.  The test space is denoted `Y`.  The exact
spaces may be anisotropic density spaces, standard-family graph norms, or
fixed-cut Sobolev--BV spaces.

### Definition 2.1 (same-occurrence bilateral packet)

A family has a bilateral CM2 packet if the following data are supplied.

1. **Atlas and ownership.**  Every physical occurrence has a parameter-stable
   UID and exactly the declared incident sides.  Common refinements preserve
   UIDs, owners, and orientations.
2. **Reverse/source estimate.**  There are `0<alpha<1`, `Gamma_+>=1`, and
   constants `C_omega^-` such that
   \[
   |A_{m,n}^{\omega}|
   \le C_\omega^-\alpha^m\Gamma_+^n
   \|g\|_{X_-}\|f\|_Y.
   \tag{2.1}
   \]
3. **Forward/target estimate.**  There are `0<beta<1`, `Gamma_- >=1`, and
   constants `C_omega^+` such that
   \[
   |A_{m,n}^{\omega}|
   \le C_\omega^+\Gamma_-^m\beta^n
   \|g\|_{X_-}\|f\|_Y.
   \tag{2.2}
   \]
4. **Strict crossed-rate window.**  With
   \[
   A_0=\log(1/\alpha),\quad B_0=\log(1/\beta),\quad
   C_0=\log\Gamma_+,\quad D_0=\log\Gamma_-,
   \]
   one has
   \[
   A_0B_0>C_0D_0.
   \tag{2.3}
   \]
5. **Occurrence summability.**  The interpolated constants in Theorem 2.2 are
   summable over `omega`.
6. **Finite-DQ compatibility.**  Difference quotients preserve the occurrence
   registry and converge in the two-time summability topology.

### Theorem 2.2 (bilateral product-tail CM2)

Let a bilateral packet satisfy Definition 2.1.  Set

\[
\lambda_*
=\frac{B_0+D_0}{A_0+B_0+C_0+D_0}
\]

and

\[
\log\rho_*
=\frac{C_0D_0-A_0B_0}
       {A_0+B_0+C_0+D_0}.
\tag{2.4}
\]

Then `0<rho_*<1` and

\[
|A_{m,n}^{\omega}|
\le
(C_\omega^-)^{\lambda_*}
(C_\omega^+)^{1-\lambda_*}
\rho_*^{m+n}
\|g\|_{X_-}\|f\|_Y.
\tag{2.5}
\]

Consequently, if

\[
\sum_\omega
(C_\omega^-)^{\lambda_*}
(C_\omega^+)^{1-\lambda_*}<\infty,
\tag{2.6}
\]

then

\[
\sum_\omega\sum_{m,n\ge0}
|A_{m,n}^{\omega}|<\infty.
\tag{2.7}
\]

#### Proof

Raise (2.1) to the power `lambda` and (2.2) to the power `1-lambda`.
Since the same nonnegative quantity is bounded by both right-hand sides,

\[
|A_{m,n}^{\omega}|
\le
(C_\omega^-)^\lambda(C_\omega^+)^{1-\lambda}
(\alpha^\lambda\Gamma_-^{1-\lambda})^m
(\Gamma_+^\lambda\beta^{1-\lambda})^n
\|g\|_{X_-}\|f\|_Y.
\]

Choose `lambda=lambda_*`.  The logarithms of the two time factors are then
equal.  Direct substitution gives (2.4).  The strict inequality (2.3) makes
this logarithm negative.  Summing the two geometric series and then using
(2.6) proves (2.7).  No cancellation between distinct occurrences was used.

### Corollary 2.3 (regularity-loss route)

Assume there are spaces `X_hi` and `X_lo` such that, on the centered
subspaces,

\[
\|Q_a^mg\|_{X_{hi}}
\le C_{hi}\rho_{hi}^m\|g\|_{X_{hi}},
\]

\[
\|Q_a^nu\|_{X_{lo}}
\le C_{lo}\rho_{lo}^n\|u\|_{X_{lo}},
\]

and

\[
K_a:X_{hi}\to X_{lo},\qquad \Pi_aK_a=0.
\]

Then

\[
|\langle Q_a^nK_aQ_a^mg,f\rangle|
\le
C_{lo}\|K_a\|C_{hi}
\rho_{lo}^n\rho_{hi}^m
\|g\|_{X_{hi}}\|f\|_{X_{lo}^*}.
\tag{2.8}
\]

This is the diagonal special case of Theorem 2.2 and permits a finite loss of
regularity at the moving singularity.

---

## 3. Difference quotients in the CM2 topology

For `h != 0`, let

\[
K_{a,h}=\frac{L_{a+h}-L_a}{h}.
\]

### Definition 3.1 (finite-DQ CM2 convergence)

We say the finite difference quotient converges in CM2 if

\[
\sum_{m,n\ge0}
\left|
\left\langle
Q_{a+h}^nK_{a,h}Q_a^mg
-Q_a^nK_aQ_a^mg,
 f
\right\rangle
\right|
\longrightarrow0
\tag{3.1}
\]

uniformly on the declared unit balls and compact parameter chambers.

### Proposition 3.2 (head--tail criterion)

Suppose:

1. for every finite rectangle `0<=m,n<=N`, the arrays converge uniformly as
   `h->0`;
2. the finite-DQ arrays and the limiting derivative array share a summable
   product envelope independent of small `h`.

Then (3.1) holds.

#### Proof

Choose `N` so that the common envelope outside the finite rectangle has total
mass below `epsilon/3`.  On the finite rectangle, uniform convergence makes
the sum below `epsilon/3` for small `h`.  The two tails contribute less than
`2epsilon/3`.  This proves convergence in `l1(N^2)`.

The proposition is elementary, but it prevents the invalid inference from
pointwise `(m,n)` convergence to convergence of the complete response series.

---

## 4. Third-source totalization and U3

Higher response contains not one current but a countable collection of
interior, face, intersection, endpoint, and refinement atoms.  The third
source is therefore constructed as a directed limit.

Let

\[
d=(K,\varepsilon,\mathcal P)
\]

record a homogeneity-depth cutoff, a vertex/intersection cap, and a finite
atlas partition.  Define

\[
G_{3,d}(a)
=
\operatorname{Tot}_{\mathfrak S_d}
\{\eta_{a,\omega}:\omega\in I_d\}
+S_d^{\rm seam}(a).
\tag{4.1}
\]

For an atom, define

\[
\|\eta_{a,\omega}\|_{\rm CM2}
=
\sup_{\|g\|\le1,\|f\|\le1}
\sum_{m,n\ge0}
|\langle Q_a^n\eta_{a,\omega}Q_a^mg,f\rangle|.
\tag{4.2}
\]

### Theorem 4.1 (CM2-to-U3 joint Cauchy theorem)

Assume:

1. each finite map `a -> G_{3,d}(a)` is continuous in a complete graded source
   space `X`;
2. all third-source atoms satisfy Theorem 2.2 or Corollary 2.3;
3. there is a summable envelope
   \[
   \sup_a\|\eta_{a,\omega}\|_{\rm CM2}\le b_\omega,
   \qquad \sum_\omega b_\omega<\infty;
   \tag{4.3}
   \]
4. the vertex/intersection cap error is bounded by
   `omega_vert(epsilon)->0`;
5. the seam/refinement defect is bounded by
   `omega_seam(P)->0`;
6. on every common refinement, equal UIDs with opposite orientations cancel
   exactly and no distinct occurrence is re-keyed.

Then, for `d1,d2` refining `d`,

\[
\|G_{3,d_1}-G_{3,d_2}\|_X
\le
2\sum_{\omega\notin I_d}b_\omega
+2\omega_{\rm vert}(\varepsilon)
+2\omega_{\rm seam}(\mathcal P).
\tag{4.4}
\]

Hence `G_{3,d}` converges uniformly in `a` to a unique continuous third source
`G_3`.  If the reduced resolvent `R_a` is uniformly bounded on the graded
source spaces, then the third-order words

\[
R_aG_3R_a,
\quad R_aG_2R_aG_1R_a,
\quad R_aG_1R_aG_2R_a,
\quad R_aG_1R_aG_1R_aG_1R_a
\tag{4.5}
\]

exist and depend continuously on `a`.  We call this conclusion U3.

#### Proof

Pass to a common refinement.  All common atoms cancel by UID and orientation.
The remaining atoms are outside the old cutoff or lie in the cap/refinement
error.  The first group is bounded by the tail of (4.3), and the other two by
the declared moduli.  This gives (4.4).  Completeness gives `G_3`; uniform
convergence gives parameter continuity.  Boundedness of the reduced
resolvents and finite multiplication then gives convergence of every word in
(4.5).

### Remark 4.2

First-order CM2 alone does not imply U3.  The CM2 estimate must hold for the
actual derivative atoms entering `G_3`, and the totalization and cap defects
must be controlled.  This is the precise content of the arrow `CM2 -> U3`.

---

## 5. An actual open moving-seam family

We now verify the complete finite-order package in a deterministic billiard
model.

### 5.1 The pinball cylinder

Let

\[
\mathcal Q=(\mathbb R/\mathbb Z)\times[0,1].
\]

A collision with the bottom wall resets the particle vertically upward.  At
the top wall, the outgoing direction is chosen so that the next bottom
coordinate is the value of a full-branch expanding map.

For

\[
I=[-1/40,1/40],
\]

define

\[
\begin{aligned}
w_1(a)&=1/10+a,&
 w_2(a)&=1/5+2a,\\
w_3(a)&=3/10-a,&
 w_4(a)&=2/5-2a.
\end{aligned}
\tag{5.1}
\]

Let `s_0=0`, `s_i=sum_{j<=i}w_j`, and on the `i`th branch set

\[
T_a(x)=\frac{x-s_{i-1}(a)}{w_i(a)}\pmod1.
\tag{5.2}
\]

Distinct winding lifts at the top wall make the three internal seams physical
direction discontinuities.  Their velocities are `1,3,2`, respectively.  On
`I`,

\[
3/40\le w_i(a)\le9/20,
\]

so the expansion is uniform.

The Perron operator with respect to Lebesgue probability is

\[
(L_ah)(y)=\sum_{i=1}^4w_i(a)
 h(s_{i-1}(a)+w_i(a)y).
\tag{5.3}
\]

Lebesgue probability is invariant for every `a`; therefore `Pi h=int h` is
independent of the parameter.

### 5.2 Fixed-cut spaces

For `r>=1`, let

\[
X_r=\{h:h|_{(0,1)}\in W^{r,1}(0,1)\}
\]

with norm

\[
\|h\|_{X_r}
=\|h\|_1+
\sum_{j=0}^{r-1}\operatorname{Var}_{\mathbb T}(h^{(j)}),
\tag{5.4}
\]

where circular variation includes the jump at the fixed coordinate cut.
Set `Y=X_1`.

A weighted-partition variation calculation gives, for centered functions,

\[
\|Q_a^nh\|_{X_r}
\le2\rho^n\|h\|_{X_r},
\qquad \rho=9/20,
\tag{5.5}
\]

for `r=1,2,3,4`.  The constant and rate are uniform in `a`.

### 5.3 The first three operator derivatives

Put

\[
v=(1,2,-1,-2),
\]

and let `A_i=sum_{j<=i}v_j`.  For

\[
\psi_i^a(y)=s_{i-1}(a)+w_i(a)y,
\qquad
r_i(y)=A_{i-1}+v_i y,
\]

both `w_i` and `psi_i` are affine in `a`.  Repeated differentiation of (5.3)
gives, for `k=1,2,3`,

\[
\boxed{
\partial_a^kL_ah
=
\sum_{i=1}^4
\left[
 k v_i r_i^{k-1}h^{(k-1)}(\psi_i^a)
 +w_i(a)r_i^kh^{(k)}(\psi_i^a)
\right].
}
\tag{5.6}
\]

The formula follows by induction because `partial_a w_i=v_i`,
`partial_a psi_i=r_i`, and all higher derivatives of `w_i,psi_i` vanish.
The fixed-cut variation inequality and boundedness of `r_i` imply

\[
\|\partial_a^kL_ah\|_Y
\le C_k\|h\|_{X_{k+1}},
\qquad k=1,2,3,
\tag{5.7}
\]

uniformly on `I`.  Conservation of mass gives

\[
\Pi\partial_a^kL_a=0.
\tag{5.8}
\]

Combining (5.5)--(5.8) with Corollary 2.3 yields

\[
|\langle Q_a^n(\partial_a^kL_a)Q_a^mg,f\rangle|
\le4C_k\rho^{m+n}
\|g\|_{X_{k+1}}\|f\|_\infty.
\tag{5.9}
\]

Thus the complete double sum is finite for `k=1,2,3`.

### 5.4 Nonzero moving singularity

For `k=1`, (5.6) has a circular saltus.  Choose a smooth plateau supported
near the first seam and disjoint from the other seams and the coordinate cut.
Its same-occurrence jump under `partial_aL_a` is exactly the nonzero first-seam
coefficient.  Hence

\[
\partial_aL_a\ne0
\]

for every `a in I`; the theorem is not an exact-conjugacy zero-source example.

### Theorem 5.1 (actual scoped CM2 and U3)

The open family (5.1)--(5.3) satisfies:

1. a nonzero physical moving-seam source for every parameter;
2. uniform product-CM2 for the first three operator derivatives;
3. finite-DQ convergence in the corresponding double-time `l1` topology;
4. a finite, parameter-stable occurrence atlas;
5. actual U3 and continuous third-order reduced-resolvent words.

#### Proof

Items 1 and 2 were proved above.  Taylor's formula with integral remainder and
the same `X_4 -> Y` bounds gives a common summable envelope for finite
quotients, so Proposition 3.2 proves item 3.  The four physical branches and
three seams give item 4.  Since the source atlas is finite, the totalization
errors in Theorem 4.1 vanish; (5.9) gives item 5.

### Scope statement

The model is a deterministic billiard with moving physical seams and nonzero
saltus current.  It is not a specular dispersing Sinai billiard.  The abstract
theorems apply to a specular family only after its bilateral packet is proved.

---

## 6. Maximality and no-go boundary

### Proposition 6.1 (finite local data do not determine CM2)

Fix any finite collection of atlas records and any finite rectangle of the
array (1.2).  There are two abstract completions agreeing on all those records:
one whose unobserved atoms have a summable product tail, and one whose
unobserved atoms have positive masses comparable to `1/(m+n+1)` on disjoint
occurrences.  The latter double sum diverges.

#### Proof

Leave the prescribed finite records unchanged.  In the first completion set
all remaining atoms to zero.  In the second, add mutually independent formal
occurrences outside the inspected cutoff with the stated positive matrix
elements.  Both completions agree on the finite prefix, but only the first is
CM2.  Thus no finite-prefix verifier or local atlas schema can imply global
summability.

### Corollary 6.2

A general moving-singularity theorem must contain an actual product-tail or an
equivalent bilateral recovery/rate packet.  This hypothesis cannot be deleted
and replaced by local geometry alone.

This is the maximality sense used in this paper.  Stronger no-go results for
particular billiard classes may be added without changing the positive theorem.

---

## 7. Exported interface

Paper II may import only the following named outputs:

```text
P1-CM2        product-tail double summability
P1-FDQ        finite-DQ convergence in l1(N^2)
P1-U3         continuous first three operator/source derivatives
P1-RWORDS     continuous third-order reduced-resolvent words
P1-ACTUAL-4B  actual open four-branch moving-seam witness
```

It may not import an unnamed full moving-flow response package.

---

## 8. Conclusion

The response problem with moving singularities is controlled by two logically
separate mechanisms: bilateral time decay and source totalization.  The strict
crossed-rate inequality solves the first, and the CM2 atom Cauchy theorem solves
the second.  Together they yield U3.  The four-branch pinball family shows that
the theorem is nonempty and genuinely nonzero.  The theorem's explicit packet
is also its correct maximal boundary: removing it would revive a false
unrestricted universal claim.
