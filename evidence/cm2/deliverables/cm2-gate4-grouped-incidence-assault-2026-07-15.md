# CM2 Gate 4 continuation: a grouped non-grazing reversal row

Date: 2026-07-15  
Model: centered two-disk table on the standard solid-boundary section
`N=G disjoint-union W`; `R_G=9/25`, `R_W=4/25`, and the white center is
`(1/2+s,1/2)`.  The frozen v51/v52 files and the shared research log were not
edited.

## Decision

**Gate 4 remains `NOT_CERTIFIED` globally.**  The global event inventory is
still absent, so the construction below has not been repeated on every
physical incidence or attached to the stopped-parent law.

There is, however, a decision-changing local advance.  The explicit
gray-to-white tangency from the previous audit does not have to be sourced at
the white grazing point in its second representation.  Continuing the same
tangent ray to its next transverse collision produces a non-grazing endpoint
on `G[1,1]`.  On a rigorously certified positive-width band this gives:

1. a Borel path-reversal involution on one physical incidence;
2. a stable source curve at `G[0,0]` and an unstable image curve at `G[1,1]`;
3. the same positive coarea measure in both parametrizations;
4. two exact, restrictionwise, **nonadditive** representations of the same
   compactified one-step face current; and
5. a legitimate pre-recovery local single charge
   `q_0=max(C_backward,C_forward)m`.

Thus the earlier statement “this explicit occurrence cannot be given two
typed carriers” is too strong.  What fails is only the attempted **direct
grazing-source** view.  Grouping the grazing contact with its next transverse
collision repairs the current/coarea/typing layer for this one row.  It does
not yet repair the stopped-recovery layer: arbitrary owner/parent
restrictions of the row have not been shown to recover with a common
exponential moment.  The result cannot be promoted to all of Gate 4 without
the missing Gate-3 inventory and that recovery audit.

## 1. Certified grouped incidence

Parametrize a small source band on the central gray disk by

\[
 q(\theta)=\frac9{25}(\cos\theta,\sin\theta),
 \qquad |\theta|\le 10^{-7}.
\]

Let `d=(1/2,1/2)-q`, `R=4/25`, and

\[
 L=(|d|^2-R^2)^{1/2},
 \qquad
 u=\frac{(Ld_x+Rd_y,\;Ld_y-Rd_x)}{|d|^2}.
\tag{1.1}
\]

Direct algebra gives

\[
 |u|=1,\qquad u\cdot d=L,
 \qquad u^\perp\cdot d=R.
\tag{1.2}
\]

Hence the ray is tangent to `W[0,0]` at time `L` for every theta in the
band.  Continuing the unchanged tangent velocity, put

\[
 D=q-(1,1),\qquad
 \Delta_B=(D\cdot u)^2-(|D|^2-R_G^2),
\]

\[
 t_B=-D\cdot u-\sqrt{\Delta_B},qquad
 y_B=q+t_Bu.
\tag{1.3}
\]

The 200-bit Arb certificate proves uniformly on the whole band:

\[
 0.49<L<0.50,qquad 0.82<t_B<0.84,
 \qquad t_B-L>0.33,
\]

\[
 0.81<(y_B)_x<0.83,qquad
 0.68<(y_B)_y<0.70,
\]

and the incoming cosine at `G[1,1]` is greater than `0.99`.  It checks all
95 other gray/white lifts in `[-3,3]^2`: each has negative discriminant, is
wholly behind the source, or has its first root after `t_B`.  The displayed
segment box makes this lift scan exhaustive.  Thus the physical grouped path
is

```text
G[0,0]  -- tangent to W[0,0] --  G[1,1],
```

with both gray endpoints non-grazing and no intervening crossing.

The reverse ray is the same segment with velocity reversed, so it gives the
physical reverse path

```text
G[1,1]  -- tangent to W[0,0] --  G[0,0].
```

This is a genuine path-level reversal, not a numerical nearest-point match.

## 2. The reversal map and trace matching

Let `T_GB` be the smooth ghost/direct collision branch from `G[0,0]` to
`G[1,1]` obtained by continuing through the tangent contact, and let `R` be
the collision time-reversal involution.  On the oriented incidence band set

\[
 \rho=R\circ T_{GB}.
\tag{2.1}
\]

An oriented record consists of its initial gray phase point, the central
white tangent contact, and the terminal gray phase point.  On these records
`rho` swaps the gray endpoints, reverses every velocity, preserves the white
contact, and satisfies `rho^2=id`.  The corresponding unoriented id is

```text
{G[0,0],G[1,1]} | tangent W[0,0] | theta band | s=0.
```

Write `z_W(theta)` for the white grazing trace and `y(theta)=T_GB x(theta)`
for the post-collision state at `G[1,1]`.  The local one-step face current is

\[
 J(\Phi)=\int_I
  \{\Phi(z_W(\theta))-\Phi(y(\theta))\}\,dm(\theta),
 \qquad I=[-10^{-7},10^{-7}].
\tag{2.2}
\]

The sign in (2.2) is fixed once by the positive parameter derivative below;
reversing the chosen owner changes the global polarity but not the common
positive measure `m`.

Equation (2.2) has two nonadditive factorizations.  On the gray source band,

\[
 E_-(\Phi)(\theta)=
 \Phi(z_W(\theta))-\Phi(y(\theta)).
\tag{2.3}
\]

On the image curve `Y=T_GB(I)`, with `theta(y)` the analytic inverse,

\[
 E_+(\Phi)(y)=
 \Phi(z_W(\theta(y)))-\Phi(y),
 \qquad m_+=(T_{GB})_*m.
\tag{2.4}
\]

For every Borel restriction `A subset I`, ordinary change of variables gives

\[
 \int_A E_-(\Phi)\,dm
 =\int_{T_{GB}A}E_+(\Phi)\,dm_+.
\tag{2.5}
\]

This is trace-by-trace equality, not a norm estimate and not equality only
after summing two events.  The two sides of (2.5) are alternative views of
one coefficient occurrence; they are never added.

The direct operator identity

\[
 D_a=-PRD_{\rho(a)}RP
\]

on the uncompactified one-step section is still not asserted, because `P` at
the white grazing state needs a separately defined boundary extension.  The
grouped current (2.2)--(2.5) avoids that undefined operation while retaining
both actual one-step traces.

## 3. Exact equality of the coarea coefficient

In source coordinates `(theta,phi)`, let `H_s` be the white-circle
discriminant.  On the selected tangent branch,

\[
 \partial_sH_0=2R u_y>0,
 \qquad
 \partial_\varphi H_0=2RL>0.
\]

Up to the table-wide SRB normalization, the positive face measure is

\[
 dm(\theta)
 =R_G\cos\varphi_G(\theta)
   \frac{|\partial_sH_0|}{|\partial_\varphi H_0|}\,d\theta
 =R_G\cos\varphi_G(\theta)\frac{u_y(\theta)}{L(\theta)}\,d\theta.
\tag{3.1}
\]

The certificate proves

\[
 0.33<\frac{dm}{d\theta}<0.34.
\tag{3.2}
\]

There is also an invariant coordinate proof that (3.1) is the reverse
coarea coefficient, including the flux/Jacobian cancellation.  Define

\[
 H_B=H_G\circ (R T_{GB})^{-1}.
\]

Both `T_GB` and `R` preserve the collision area form
`cos(phi) dr dphi`.  Therefore, for every bounded Borel `f`,

\[
 \int f\,\delta(H_B)|\partial_sH_B|\,d\mu
 =\int (f\circ RT_{GB})\,
   \delta(H_G)|\partial_sH_G|\,d\mu.
\tag{3.3}
\]

Formula (3.3) is exactly the missing grazing-flux/Jacobian cancellation; it
does not divide by the zero SRB flux at the white contact.  It transports the
coarea law between the two non-grazing gray endpoints.  In impact arclength
on `G[1,1]`, the certificate obtains

\[
 2.4<\frac{dm_+}{dr_B}<2.6.
\tag{3.4}
\]

Thus `m` and `m_+` are the same coefficient measure on the common occurrence
base, not two separately normalized laws.

## 4. Opposite typed carriers and the pre-recovery single charge

The certified Birkhoff slopes are

\[
 -4<\frac{d\varphi_G}{dr_G}<-3.8,
 \qquad
 5.7<\frac{d\varphi_B}{dr_B}<5.9.
\tag{4.1}
\]

For this table `kappa_min=25/9`, `kappa_max=25/4`, and the existing certified
free-flight lower bound is `tau_min>1821/10000`.  Hence both intervals in
(4.1) lie compactly inside the usual stable and unstable dispersing-billiard
cones, respectively.  Their collision cosines are bounded below by `0.55`
and `0.99`, so both stay in a central homogeneity region.

The curves and the densities (3.1), (3.4) are positive analytic functions on
a fixed compact band.  They therefore define finite stable and unstable
standard-pair carriers with finite local boundary and density marks.  This
does **not** prove that they, or every stopped restriction of them, are
already proper for the fixed global proper-family threshold.  Consequently
no value of `R_-` or `R_+` is frozen here.

Let `C_-` and `C_+` be one plus the fixed source, boundary, density,
inverse-chart and test-pullback norms of (2.3) and (2.4) on this compact band.
These are finite constants determined before any product-time query.  Define

\[
 q_0=\max\{C_-,C_+,2\}\,m.
\tag{4.2}
\]

This is one positive measure on one base row, and (2.5) makes either
orientation an exact representation of the same scalar current.  Therefore
(4.2), not `q_-+q_+`, is the correct **pre-recovery** single charge for this
local grouped row.

No recovery mark is hidden in `C_-/C_+`.  To obtain the final admissible `q`,
one must enlarge (4.2) once by the maximum of both predictable recovery
costs, then prove both exponential moments under every required
stopped-parent/owner restriction of that same enlarged measure.  Neither
step is certified here.

### 4.1 A strict restriction no-go

There is a concrete reason not to infer that last step from the local
analytic curves.  Let `K subset I` be a positive-`m` compact nowhere-dense
set (for example a fat Cantor set), after deleting the zero-`m` set of
finite-time singular preimages.  On every fixed finite clean itinerary, the
billiard map is a local diffeomorphism.  Hence the image of `K` is again
nowhere dense in its image curve.

A positive regular standard pair has a density bounded away from zero on a
nondegenerate interval carrier, so its support contains an interval.  It
cannot equal the propagated restriction `m|K`.  If a proposed finite
recovery clock takes countably many integer values, one clock level has
positive restricted mass; on each clean component at that level the same
homeomorphism argument applies.  Therefore:

> Analyticity and opposite cone orientation do not give exact proper-family
> recovery uniformly under arbitrary positive-mass Borel restrictions of
> the occurrence coordinate.

Domination by the unrestricted analytic pair is possible, but its normalized
Radon--Nikodym cost can grow like `1/m(K)` and must be charged in `q`; no
uniform conditional moment follows.  The final registry must consequently
do one of two things before freezing `q`:

1. restrict admissible stopped/owner filters to a countable interval or
   cylinder algebra with quantitative component control; or
2. use the Gate-2 stopped-parent PPE/Frostman input to dominate every
   permitted restriction, with the parentwise normalization cost included in
   both oriented recovery envelopes.

This is a genuine dependency of Gate 4 on Gate 2, not a missing application
of time-reversal invariance.

## 5. Local Gate-5 Kac singular terms on the same row

The grouped row also instantiates a local-only part of Gate 5.  Let the
height-two event set be the hit side

\[
 E_s=\{H_s>0\},\qquad r_s=1+\one_{E_s}.
\]

Let `g` be a base test and let `h` be a phase observable, with `h_1` denoting
its level-one (white-collision) coordinate.  Since `partial_s H_0>0` on this
row, differentiation of the indicator and the coarea formula (3.1) give the
two singular Kac coordinates separately:

\[
 \left\langle(\dot{\mathcal S}h)^{\rm face}_a,g\right\rangle
 =\int_I g(x(\theta))h_1(z_W(\theta))\,dm(\theta),
\tag{5.1}
\]

\[
 \left\langle \dot r_a\,\widehat\mu(h),g\right\rangle
 =\widehat\mu(h)\int_I g(x(\theta))\,dm(\theta).
\tag{5.2}
\]

Thus the singular part of the differentiated Kac combination on this row is

\[
 \left\langle
  \{\dot{\mathcal S}h-\dot r\,\widehat\mu(h)\}^{\rm face}_a,g
 \right\rangle
 =\int_I g(x(\theta))
  \{h_1(z_W(\theta))-\widehat\mu(h)\}\,dm(\theta).
\tag{5.3}
\]

Equations (5.1) and (5.2) are two coordinates of one vector-valued occurrence,
not two copies of its positive mass.  Freeze the structural combination mark

```text
owner      = kac-return-boundary:G00-W00-G11
coordinates= (moving-level dot(S), roof dot(r)*phase-mean)
vector     = (+1,-1)
polarity   = +
coefficient= m
```

before `h` or `g` is queried.  The physical test lift supplies the two
coordinates

\[
 \bigl(g(x)h_1(z_W),\;g(x)\widehat\mu(h)\bigr),
\]

and the fixed vector `(+1,-1)` performs the Kac combination.  Because
`widehat mu` is a probability,

\[
 |h_1(z_W)-\widehat\mu(h)|
 \le 2\|h\|_\infty.
\]

Consequently the combined local test cost is at most `2`, already included
in the single pre-recovery envelope (4.2).  Both (5.1) and (5.2), and their
combination (5.3), therefore use the **same** `m` and the **same once-charged**
`q_0`.

This closes only the singular face part of two Kac coordinates on this one
row.  It does not cover the interior moving-level derivative, other return
boundaries, the remaining two terms `S dot(h)` and
`r partial_s[mu_hat_s(h_s)]`, or either global phase CM2 norm.  Moreover the
local roof current has positive mass; the identity
`mu(dot r)=0` follows only after all oriented return-boundary rows cancel in
the complete registry.  That global cancellation is not inferred here.

```text
LOCAL_KAC_DOT_S_FACE_ON_GROUPED_ROW: CERTIFIED
LOCAL_KAC_DOT_R_MEAN_ON_GROUPED_ROW: CERTIFIED
LOCAL_KAC_COMMON_m_AND_q0_MARK: CERTIFIED
GLOBAL_FOUR_TERM_KAC_TYPING: NOT CERTIFIED
GLOBAL_MEAN_ROOF_CANCELLATION_BY_ROWS: NOT CERTIFIED
```

## 6. What this changes, and what remains open

Certified for this one positive-width row:

```text
PHYSICAL_G00_W00_G11_GROUPED_PATH: CERTIFIED
PATH_REVERSAL_INVOLUTION: CERTIFIED
COMMON_COAREA_MEASURE: PROVED
RESTRICTIONWISE_TWO_VIEW_CURRENT_IDENTITY: PROVED
LOCAL_OPPOSITE_ORIENTATION_TYPING: PROVED
LOCAL_PRE_RECOVERY_SINGLE_CHARGE_q0_MAX: PROVED
LOCAL_BIDIRECTIONAL_RECOVERY_TIMES: NOT CERTIFIED
LOCAL_KAC_DOT_S_DOT_R_COMMON_MARK: PROVED
```

Still open:

1. candidate/first-root rows for every Gate-3 source chart and target lift;
2. pair/triple incidences and consistent grouping when two tangencies or a
   phase endpoint occur together;
3. a boundary extension proving the direct one-step operator conjugacy at a
   grazing trace, if that ungrouped formulation is retained;
4. uniform carrier/test constants over the complete event registry;
5. both stopped-parent exponential recovery moments under the one frozen
   global `q`; and
6. attachment to the actual physical source kernel and global DQ matching.

Consequently:

```text
GLOBAL_EVENTWISE_REVERSAL_REGISTRY: NOT CERTIFIED
GLOBAL_SINGLE_CHARGE_q_MAX: NOT CERTIFIED
GLOBAL_BIDIRECTIONAL_RECOVERY: NOT CERTIFIED
GATE_4: NOT CERTIFIED
```

## Reproduction

```bash
python3 -m py_compile deliverables/cm2_gate4_grouped_incidence_cert.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate4_grouped_incidence_cert.py
python3 -m json.tool \
  deliverables/cm2-gate4-grouped-incidence-manifest-2026-07-15.json \
  >/dev/null
sha256sum -c deliverables/cm2-gate4-grouped-incidence-manifest-2026-07-15.sha256
sha256sum -c deliverables/cm2-v52-manifest.sha256
```
