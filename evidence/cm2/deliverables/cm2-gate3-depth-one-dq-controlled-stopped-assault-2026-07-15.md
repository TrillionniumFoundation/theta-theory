# CM2 Gate 3--5: corrected depth-one DQ and controlled stopped algebra

Date: 2026-07-15 (Asia/Shanghai)  
Model: centred rational two-disk torus pilot on the standard solid-boundary
section `N=G disjoint-union W`  
Verdict: **the collision-coordinate coarea scale is corrected, the complete
depth-one fixed-gauge transfer DQ is certified, and a controlled dyadic
stopped algebra plus a global slope envelope `<29` are certified; the
iterated `MT_DQ`, physical stopped recovery and CM2 norm lifts remain
`NOT_CERTIFIED`**

## 1. Decision-changing correction

The seventh-round global-current artifact used the tangent graph coordinate

\[
 p=\sin\varphi,\qquad c_p=\cos\varphi=\sqrt{1-p^2},
\]

but multiplied the graph velocity by `cos(phi)` after that factor had already
been absorbed by the change of variables

\[
 dp=c_p\,d\varphi,
 \qquad
 \cos\varphi\,dr\,d\varphi=dr\,dp.
\]

Consequently the old displayed law

\[
 R_{\rm source}\frac{c_p^2|u_y|}{\ell_T}\,d\theta
\]

is **superseded**.  The correct positive collision-flux coarea law is

\[
 \boxed{
 dm_e=R_{\rm source}\frac{c_p|u_y|}{\ell_T}\,d\theta.}
 \tag{1.1}
\]

The correction removes exactly one factor `cp`.  It does not alter the
64-row registry, the hit-minus-miss mark, the 32 exact `Jx` pairs, or the
previous numerical TV upper bound, because `0<c_p<=1` in the row interior.
All eighth-round Gate-4/5 ledgers are rebound to (1.1); the frozen
seventh-round manifests remain historical provenance and are not edited.

## 2. Exact coordinate derivation

For a source state `(q,u)`, target centre `C_T(s)` and radius `R_T`, put

\[
 d=C_T(s)-q,
 \quad
 \ell_T=u\cdot d,
 \quad
 w_T=u^\perp\cdot d,
 \quad
 \Delta_T=R_T^2-w_T^2.
\]

On the signed tangent sheet `w_T=epsilon R_T`, with

\[
 \eta={\bf1}_{T=W}-{\bf1}_{S=W},
\]

the exact derivatives at fixed collision coordinates are

\[
 \partial_s\Delta_T=2\eta\epsilon R_Tu_y,
 \qquad
 \partial_p\Delta_T=
 \frac{2\epsilon R_T\ell_T}{c_p}.
 \tag{2.1}
\]

Therefore the signed coarea coefficient and graph velocity are

\[
 \frac{\partial_s\Delta_T}{|\partial_p\Delta_T|}
 =\eta\epsilon\frac{c_pu_y}{\ell_T},
 \qquad
 \dot p_e=-\frac{\partial_s\Delta_T}{\partial_p\Delta_T}
 =-\eta\frac{c_pu_y}{\ell_T}.
 \tag{2.2}
\]

Since the collision law in `(r,p)` has density one and
`dr=R_source dtheta`, taking the absolute graph velocity gives (1.1), not
the old `cp^2` law.

The exact geometric envelope is unchanged:

\[
 \ell_T^2\ge\frac{36337}{3260000}>\frac1{100},
 \qquad \ell_T>\frac1{10},
\]

so

\[
 \frac{dm_e}{d\theta}
 \le \frac{9}{25}\,10=\frac{18}{5}.
\]

Thus, still up to the common factor `Z_N^{-1}`,

\[
 m_e(A_e)\le\frac{126}{5},\qquad
 \sum_em_e(A_e)\le\frac{8064}{5},\qquad
 \|J\|_{TV}\le\frac{16128}{5}.
 \tag{2.3}
\]

Under `Jx`, `cp`, `ell_T`, `|u_y|`, `R_source` and `dtheta` are invariant,
while the signed parameter polarity reverses.  Hence all 32 positive-law
pairs and the exact global signed scalar mass zero survive the correction.

## 3. Complete depth-one fixed-gauge DQ

### 3.1 Statement

Let `P_s` be the one-step collision transfer operator on the common
arclength gauge of `N`.  Because only the centre of `W` translates and both
radii are fixed, the normalized collision probability

\[
 d\mu_N=Z_N^{-1}\cos\varphi\,dr\,d\varphi
\]

is independent of `s`.  For `h in C^1(N)` and
`Phi in C^{1,alpha}` on the compactified collision section,
`0<alpha<=1`, the new certificate proves

\[
 \frac{(P_s-P_0)h}{s}\longrightarrow D_0h
 \quad\hbox{in }(C^{1,\alpha})^*.
 \tag{3.1}
\]

The limit is the sum of the persistent smooth-core derivative and the
corrected 64-row face current:

\[
\begin{aligned}
 \langle D_0h,\Phi\rangle
={}&\sum_B\int_B h(x)
 D\Phi(T_0x)\,\partial_sT_s(x)|_{s=0}\,d\mu_N(x)\\
 &+\sum_e\sigma_e\int_{A_e}h(x_e(\theta))
 \{\Phi(z_T(\theta))-\Phi(y_M(\theta))\}\,dm_e(\theta).
\end{aligned}
\tag{3.2}
\]

The same conclusion holds after the fixed double projection

\[
 \Pi_0^\perp\frac{P_s-P_0}{s}\Pi_0^\perp,
\]

because `mu_N`, hence `Pi_0`, is fixed.

### 3.2 Why the global finite atlas is sufficient

The exact predecessor chain supplies all hypotheses needed by the circular
moving-domain theorem:

1. the horizon is strictly below `3`, with 162 conservative target lifts;
2. the 64 maximal rows cover every physical parameter-active first-tangency
   face;
3. all two-dimensional first/miss/polarity ambiguity has area exactly zero;
4. there are no pair or triple simultaneous first collisions;
5. each physical tangency is a regular radical face;
6. every chart seam has one owner and duplicate torus/lift traces are
   identified before absolute values.

The exact flight lower bound gives the uniform angular submersion

\[
 |\partial_\varphi\Delta_T|=2R_T\ell_T
 >2\frac4{25}\frac1{10}=\frac4{125}.
 \tag{3.3}
\]

On each persistent smooth branch, joint analyticity in `(s,x)` and the
fundamental theorem of calculus give the first line of (3.2).  Same-colour
relative branches have zero parameter velocity; cross-colour regular
branches are analytic.

Near a target tangency, the collision root has the standard square-root
form.  The interior parameter derivative is dominated by

\[
 C\{1+(\Delta_T)_+^{-1/2}\}.
\]

Coarea with (3.3) gives the uniform collar estimate

\[
 \int_{0<\Delta_T<\rho}
 \{1+\Delta_T^{-1/2}\}\,d\mu_N
 \le C\rho^{1/2}.
 \tag{3.4}
\]

The coefficient measures converge in total variation after pulling every
finite-`s` radical chart to the common face.  Reynolds' formula then produces
exactly the second line of (3.2), with the corrected law (1.1).

At a common tangent of two distinct target disks, the contact times are
strictly ordered.  Hence the one-step derivative envelope is a finite **sum**
of individual inverse square roots, never their nonintegrable product.
There are no triple first events.  The remaining row endpoints contribute no
atoms:

- source grazing: (1.1) vanishes with `cp`;
- polarity switch: (1.1) vanishes with `u_y`;
- first-visibility and miss-switch endpoints: finite one-dimensional base
  endpoints have zero `m_e` mass;
- chart and lift seams: the physical traces agree and cancel.

Equations (3.3)--(3.4), the finite cover and the exact endpoint assembly prove
(3.1).  This closes the complete **depth-one static-test** quotient.  It does
not supply the iterated branchwise tests, response spaces or summable
two-time majorant required by the full frozen `MT_DQ` interface.

## 4. Controlled stopped interval algebra

On every open maximal row, (1.1) is finite, analytic and strictly positive.
Let

\[
 u_e(\theta)
 =\frac{m_e((\theta_e^-,\theta))}{m_e(A_e)}\in(0,1).
 \tag{4.1}
\]

This is a canonical increasing mass-coordinate homeomorphism.  At declared
depth `K`, use the dyadic atoms

\[
 I_{K,j}=[j2^{-K},(j+1)2^{-K}),
 \qquad 0\le j<2^K.
 \tag{4.2}
\]

The finite Boolean algebras generated by (4.2) are nested; their union over
`K` is a countable Boolean algebra.  Exactly,

\[
 m_e(I_{K,j})=2^{-K}m_e(A_e).
 \tag{4.3}
\]

Therefore every nonempty admitted restriction at depth `K` has:

```text
at most 2^K interval components;
mass at least 2^-K m_e(A_e);
parent-normalization cost at most 2^K.
```

For `2<=L<=K`, discard the first and last `2^{K-L}` atoms.  The compact core
has exact mass fraction

\[
 1-2^{1-L},
\]

and the two endpoint cemeteries have exact total mass fraction

\[
 2^{1-L}.
 \tag{4.4}
\]

Every connected core atom is transported by both occurrence views to one
analytic interval carrier.  A positive-mass nowhere-dense fat Cantor set is
not an admitted restriction, so the previous support obstruction is removed
inside this declared policy.

This is not yet physical recovery.  The stopped law must still prove a
moment of the form

\[
 \mathbb E_q\!left[
 2^K e^{\gamma(R_{\rm fw}+R_{\rm rev})}
 \right]<\infty
 \tag{4.5}
\]

and must sum the endpoint cemeteries as `L` grows.

## 5. All-row oriented slope envelope

The tangent family has exact Birkhoff slope

\[
 \frac{d\varphi_{\rm source}}{dr_{\rm source}}
 =-\kappa_{\rm source}-\frac{c_{p,{\rm source}}}{\ell_T}.
 \tag{5.1}
\]

At the first strict miss collision, reflection sends the reversed stable
family to the outgoing image family with

\[
 \frac{d\varphi_{\rm miss}}{dr_{\rm miss}}
 =\kappa_{\rm miss}
  +\frac{c_{p,{\rm miss}}}{t_{\rm miss}-\ell_T}.
 \tag{5.2}
\]

For the two radii,

\[
 \kappa_{\min}=\frac{25}{9},
 \qquad
 \kappa_{\max}=\frac{25}{4}.
\]

The global squared separation margins are

\[
 \frac{301}{625}\quad(G/G),\qquad
 \frac{561}{625}\quad(W/W),\qquad
 \frac{36337}{160000}\quad(G/W).
\]

Both physical boundary points occur before time `3`; hence the relevant
centre distance plus the radius sum is strictly below `5`.  Thus

\[
 t_{\rm miss}-\ell_T
 >\frac{36337}{800000}.
 \tag{5.3}
\]

Using `cp<=1`, (5.1)--(5.3) give

\[
 -\frac{65}{4}
 <\frac{d\varphi_{\rm source}}{dr_{\rm source}}
 <-\frac{25}{9},
\]

\[
 \frac{25}{9}
 <\frac{d\varphi_{\rm miss}}{dr_{\rm miss}}
 <\frac{4108425}{145348}<29.
 \tag{5.4}
\]

All 64 source carriers are therefore stable-oriented, all 64 miss-image
carriers are unstable-oriented, and one exact broad slope-only subcharge is

\[
 q_e^{\rm slope}=29m_e.
 \tag{5.5}
\]

Its global positive mass is at most `233856/5 Z_N^{-1}`, and its
hit-minus-miss TV is at most `467712/5 Z_N^{-1}`.

The interval `(25/9,29)` is a broad geometric orientation envelope, not the
fixed proper-standard-family cone.  Homogeneity-weighted curvature,
log-density, inverse-chart, test-pullback and recovery costs are still absent;
(5.5) is not the final `q_e`.

## 6. Corrected Gate-4/5 rebind

The complete structural ledger is rebuilt on (1.1):

```text
64 maximal physical occurrences;
64 corrected common positive laws m_e;
64 symbolic q_e=max(C_fw,C_rev,2)m_e expressions;
64 numeric slope-only subcharges q_e^slope=29m_e;
64 controlled cumulative-mass coordinates u_e;
128 singular Kac coordinates;
64 shared (+1,-1) Kac marks;
32 exact Jx scalar pairs.
```

The exact endpoint adjoint, Kac tower, prefix/suffix pairing and four-term
finite-Borel algebra are homogeneous in the occurrence measure.  Replacing
the superseded row law by (1.1) therefore preserves those identities, now
with every coordinate bound to the corrected `m_e`.  It does not create the
missing physical Banach typing or recovery clocks.

## 7. Latest-theory audit

A fresh arXiv API audit on 2026-07-15 queried linear response, perturbations,
standard families and moving scatterers for dispersing/Sinai billiards.  The
only 2026 result directly matching linear-response terminology remains

```text
arXiv:2604.19671v2
Giovanni Canestrari, Linear response for Sinai billiards with small holes
updated 2026-05-21.
```

Its hole-image standard-family construction is useful for the next recovery
attack, but it does not provide:

- the full moving-scatterer iterated `MT_DQ` interface;
- an all-row homogeneity and test-pullback cost ledger;
- the moment (4.5) for the present dyadic stopped policy; or
- the three CM2 norm intertwiners.

The search found no newer arXiv theorem that supplies those missing inputs.
The 2012 moving-scatterer result remains a loss-of-memory theorem, not a
linear-response or stopped-current recovery theorem.

## 8. Exact remaining boundary

Certified in this assault:

1. correction of the global collision-coordinate coarea law;
2. corrected 64-row finite-Borel current and exact `Jx` scalar matching;
3. complete depth-one fixed-gauge transfer DQ in `(C^{1,alpha})*`;
4. smooth-core derivative and regular-radical boundary tightness;
5. countable nested dyadic stopped interval algebra with exact normalization
   and cemetery costs;
6. all-row stable/unstable orientation and a strict slope envelope `<29`;
7. corrected 64-row single-charge and 128-coordinate Borel Kac ledger.

Still not certified:

1. iterated dynamic-`C^1` branch-record convergence and the full `MT_DQ`
   three-space interface;
2. complete homogeneity-weighted numeric `C_fw,C_rev`;
3. the depth/recovery moment (4.5) and controlled stopped-parent recovery;
4. physical prefix/suffix inverse-Jacobian and distortion sums;
5. standard-family, flux-face and dynamic-test CM2 norm lifts;
6. Gate 1 and Gate 2's pre-existing hard obstructions.

Accordingly the strict unconditional verdict remains `NO-GO FOR CLAIM` and
the composite gate count remains `0/5`.

## 9. Reproduction

```bash
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate3_depth_one_fixed_gauge_dq_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate45_controlled_stopped_interval_algebra_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate45_all_row_oriented_slope_envelope_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate45_corrected_maximal_row_kac_ledger_verifier.py \
  --replay --integrity-only
```

Each live default verifier deliberately exits `2` while the iterated
`MT_DQ`, complete `C_fw/C_rev`, physical recovery and CM2 norm lifts remain
open.
