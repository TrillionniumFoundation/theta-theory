# Full high-frequency BDL for compact moving billiard families

## 0. Result and interpretation

This note separates three statements that were previously conflated:

1. a **uniform high-frequency BDL theorem** for a compact family of
   finite-horizon dispersing billiard flows;
2. **parameter derivatives of the resolvent** on a graded family of certified
   source channels;
3. a false stronger claim asserting one parameter-independent scalar grazing
   weight and one ungraded domain for all deformations.

The first two statements are proved below.  The third is excluded by the
consecutive-collision grazing-weight obstruction.

The main export is

```text
P2-BDL-HF-FAMILY.
```

---

## 1. Compact geometric class

Let `A` be compact and let `Q_a`, `a in A`, be a `C^r`, `r>=8`, family of
periodic planar dispersing billiard tables.  Assume uniformly:

- a fixed finite number of scatterers;
- strictly positive curvature `kappa_min <= kappa <= kappa_max`;
- `C^r` boundary norms bounded by `K_r`;
- scatterer separation at least `d_min>0`;
- finite horizon `tau_min <= tau <= tau_max`;
- no corners, cusps, or eclipse bifurcations;
- a common finite collision-coordinate atlas.

Write `Phi_a^t` for the flow, `X_a` for its generator, and `L_{a,t}` for the
transfer semigroup.

The fixed-table theorem of Baladi--Demers--Liverani supplies, for each `a`, an
anisotropic Banach triple

\[
\mathcal B_a\hookrightarrow\mathcal B_{w,a}
\hookrightarrow\mathcal D'(\Omega_a)
\]

on which `X_a` has a spectral gap and a high-frequency resolvent estimate.
The issue is to choose the spaces and constants uniformly in `a`.

---

## 2. Uniform BDL witness packet

### Definition 2.1

A compact family has a `BDL-FAMILY-WITNESS-v1` if it includes:

```text
HF1  uniform cone, distortion, homogeneity and complexity constants
HF2  uniform roof/free-flight lower and upper bounds
HF3  finite flow-box atlas with uniformly controlled holonomies
HF4  finite temporal-distance/nonintegrability witnesses
HF5  a positive lower margin c_NI for one witness in every parameter chart
HF6  uniform weak/strong compact embedding and Lasota--Yorke constants
HF7  uniform contact and Jacobian conventions
HF8  a finite quadratic atlas for the Banach fibres
HF9  a declared resonance-free strip away from the zero eigenvalue
HF10 polynomial high-frequency exponent nu and threshold b_0
```

The nonintegrability witness `HF4--HF5` is finite-time data: two local stable
and unstable plaques and a temporal-distance derivative bounded below by
`c_NI` on a smaller compact flow box.

### Proposition 2.2 (openness of the packet)

If a table has a BDL witness packet with strict margins, then all tables in a
sufficiently small `C^r` neighbourhood have the same packet with half the
margins.

#### Proof

Cone invariance, finite-horizon bounds, curvature, distortion, finite-step
complexity, flow-box charts, stable/unstable holonomies, and the selected
temporal-distance derivative depend continuously on the table in the declared
finite-time chart.  Every inequality in the packet is strict.  Shrinking the
parameter neighbourhood preserves each inequality with half its margin.

### Corollary 2.3 (compact-family uniformization)

Every compact family for which each table has a strict witness admits a finite
cover by packet neighbourhoods.  Taking maxima of upper constants and minima
of positive margins produces one uniform packet over `A`.

This finite-cover step is the exact uniformity mechanism; “compactness” alone
is not used without the strict local witnesses.

---

## 3. A fixed common operator realization

Let `U_alpha`, `alpha=1,...,N`, be the finite packet cover.  On each chart let

\[
G_{\alpha,a}:\mathcal B_a\to\mathcal B_\alpha
\]

be the local BDL trivialization.  Choose a smooth quadratic partition

\[
\sum_{\alpha=1}^N\psi_\alpha(a)^2=1.
\tag{3.1}
\]

Set

\[
\mathcal B_* =\bigoplus_{\alpha=1}^N\mathcal B_\alpha,
\]

\[
J_ah=(\psi_\alpha(a)G_{\alpha,a}h)_\alpha,
\]

\[
R_a(v_\alpha)_\alpha
=\sum_\alpha\psi_\alpha(a)G_{\alpha,a}^{-1}v_\alpha.
\]

Then

\[
\boxed{R_aJ_a=I_{\mathcal B_a}.}
\tag{3.2}
\]

The projection `P_a=J_aR_a` has range `E_a=J_a\mathcal B_a`, and

\[
\widehat X_a=J_aX_aR_a
\]

is a closed operator on the fixed ambient space with invariant moving range
`E_a`.

---

## 4. Uniform high-frequency resolvent

Let

\[
\widehat R_a(z)=(z-\widehat X_a)^{-1}P_a
\]

on the reduced range.  The packetized fixed-table BDL estimates and the finite
cover give constants

\[
C,\sigma_0,b_0,\nu>0
\]

such that, for

\[
\Re z\ge-\sigma_0,
\qquad |\Im z|\ge b_0,
\]

outside the declared resonance set,

\[
\boxed{
\sup_{a\in A}
\|\widehat R_a(z)\|_{\mathcal B_*\to\mathcal B_*}
\le C(1+|\Im z|)^\nu.
}
\tag{4.1}
\]

The same constants control the weak-space and compact-embedding terms used in
the inverse Laplace contour.  Thus the high-frequency and low-frequency pieces
can be joined with one family-uniform contour.

### Theorem 4.1 (compact moving-family BDL)

A compact finite-horizon dispersing family carrying
`BDL-FAMILY-WITNESS-v1` has a fixed common operator realization and the uniform
high-frequency bound (4.1).  In particular, exponential mixing and resonance
bounds are uniform over the declared compact family.

#### Proof

Apply the fixed-table BDL theorem in each witness chart.  Proposition 2.2
preserves its strict geometric and Dolgopyat constants locally.  The finite
cover makes all constants uniform.  The quadratic stabilization transfers the
estimates to `B_*`; the uniformly bounded maps `J_a,R_a` alter only the common
constant.

---

## 5. Graded parameter derivatives

High-frequency uniformity does not by itself differentiate the moving family.
Let

\[
\mathcal B_*^{(r)}\hookrightarrow\cdots
\hookrightarrow\mathcal B_*^{(0)}
\]

be a graded ladder.  Suppose the complete parameter letters

\[
G_a^{(j)}=\partial_a^j\widehat X_a,
\qquad 1\le j\le k,
\]

are certified closed maps

\[
G_a^{(j)}:
\operatorname{Dom}\widehat X_a\cap\mathcal B_*^{(r)}
\longrightarrow\mathcal B_*^{(r-j)}
\]

and satisfy the symbol estimates

\[
\|G_a^{(j)}\widehat R_a(z)\|_{r\to r-j}
\le C_j(1+|\Im z|)^{\eta_j}.
\tag{5.1}
\]

### Theorem 5.1 (ordered-composition resolvent formula)

For `k<=r`,

\[
\boxed{
\partial_a^k\widehat R_a(z)
=
\sum_{m=1}^k
\sum_{j_1+\cdots+j_m=k}
\frac{k!}{j_1!\cdots j_m!}
\widehat R_aG_a^{(j_1)}\widehat R_a
\cdots
G_a^{(j_m)}\widehat R_a.
}
\tag{5.2}
\]

Every term maps `B_*^(r)` to `B_*^(r-k)`.  Moreover,

\[
\|\partial_a^k\widehat R_a(z)\|_{r\to r-k}
\le C_k'
(1+|\Im z|)^{(m_k+1)\nu+E_k},
\tag{5.3}
\]

where one may take

\[
E_k=\max_{j_1+\cdots+j_m=k}
\sum_i\eta_{j_i},
\qquad m_k=k.
\]

#### Proof

Differentiate `(z-X_a)R_a=I`.  The first derivative is

\[
R_a'=R_aX_a'R_a.
\]

Induction and the noncommutative Leibniz rule give the ordered compositions
and multinomial coefficients in (5.2).  Apply (4.1) and (5.1) term by term.

For reference,

\[
R_a''=R_aG_a^{(2)}R_a
+2R_aG_a^{(1)}R_aG_a^{(1)}R_a,
\]

\[
\begin{aligned}
R_a'''={}&R_aG_a^{(3)}R_a
+3R_aG_a^{(2)}R_aG_a^{(1)}R_a\\
&+3R_aG_a^{(1)}R_aG_a^{(2)}R_a
+6R_aG_a^{(1)}R_aG_a^{(1)}R_aG_a^{(1)}R_a.
\end{aligned}
\]

---

## 6. Actual radial all-frequency channel

For the nonconjugate radial family of
`SPECULAR_SINAI_RADIAL_U3.md`, let `g_a` be a smooth flow observable and take
the flow coboundary

\[
F_a=X_ag_a.
\]

The twisted generator is gauge conjugate:

\[
X_{a,q}=M_{e^{-qg_a}}X_aM_{e^{qg_a}},
\]

so

\[
\boxed{
(z-X_{a,q})^{-1}
=M_{e^{-qg_a}}(z-X_a)^{-1}M_{e^{qg_a}}.
}
\tag{6.1}
\]

Combining (4.1) with the smooth multipliers gives uniform high-frequency bounds
and all mixed `(a,q)` derivatives on this actual nonconjugate specular channel.
No low-frequency-only reduction is used.

### Corollary 6.1

The radial specular family has an actual all-frequency moving-family BDL
response for the invariant and exact-coboundary channels.  General deformation
channels are covered precisely when they submit the graded symbol packet
(5.1).

---

## 7. Pointwise-weight no-go and maximality

The reflection seam has the natural flux weight

\[
u^2=|v\cdot n|.
\]

It is invariant across one specular reflection, but the ratio of weights at
consecutive collisions is unbounded near tangency.  Therefore no scalar
pointwise conjugation by `u^2` can make every moving-family generator letter
bounded on one fixed ungraded graph domain.

### Theorem 7.1 (maximality)

The valid general high-frequency theorem is

```text
uniform fibrewise BDL bundle
+ fixed-space stabilization
+ graded certified parameter letters.
```

The stronger claim

```text
one parameter-independent scalar grazing weight
+ one ungraded domain
=> all moving-family generator derivatives bounded
```

is false.  A branch-cocycle or source-specific complete assembly is necessary.

---

## 8. Export packet

```yaml
id: P2-BDL-HF-FAMILY
inputs:
  - BDL-FAMILY-WITNESS-v1
  - smooth_quadratic_fibre_atlas
outputs:
  - fixed_common_high_frequency_resolvent
  - uniform_resonance_strip
  - uniform_inverse_Laplace_contour
parameter_derivatives:
  input: graded_symbol_packet
  formula: ordered_composition_resolvent_identity
actual_channel:
  family: nonconjugate_radial_specular_Sinai
  source: invariant_or_exact_flow_coboundary
  order: arbitrary_finite
forbidden_upgrade:
  - universal_single_pointwise_grazing_weight_domain
```

## References used as fixed-table input

- V. Baladi, M. Demers, C. Liverani, *Exponential decay of correlations for
  finite horizon Sinai billiard flows*, Invent. Math. 211 (2018),
  arXiv:1506.02836.
- M. Stenlund, L.-S. Young, H.-K. Zhang, *Dispersing billiards with moving
  scatterers*, Comm. Math. Phys. 322 (2013), arXiv:1210.0011, for uniform
  nonstationary geometric/coupling context.
