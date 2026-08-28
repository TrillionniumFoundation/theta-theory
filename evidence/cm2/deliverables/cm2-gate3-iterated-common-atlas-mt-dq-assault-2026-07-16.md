# CM2 Gate 3: iterated common-atlas and `MT_DQ` direct assault

Date: 2026-07-16 (Asia/Shanghai)  
Frozen inputs: tenth-pass Gate-3 branch-record frontier, corrected depth-one
fixed-gauge DQ, and finite-`s` common-mesh recovery  
Strict verdict: **the moving stopped endpoints are now registered on a genuine
finite-`s` common DQ carrier; at `s=0`, a full-measure component-indexed
depth-two atlas modulo a discrete zero-coarea singular set is certified, with
97.9606% additionally given explicit immutable box labels; finite-`s` depth
two, strong-source invariance, fixed-time branch-record `MT_DQ`, `FACE_2CUT`,
`FACE_TIME`, and Gate 3 remain `NOT_CERTIFIED`**

## 1. Decision-changing common mass atlas

The finite-`s` recovery construction cuts every maximal occurrence row in its
moving cumulative-mass coordinate

```text
u=u_{e,r}(theta),              dm_{e,r}=M_e(r) du.
```

For the finite difference quotient put `r=tau*s`, `0<=tau<=1`, and use the
fixed labelled carrier

```text
A_mass = disjoint_union_(e=1)^64 ([0,1]_tau x [0,1]_u).
```

On this carrier the positive face source is exactly

```text
dq_s = d tau M_e(tau*s) du,
```

and every formerly moving dyadic endpoint is the fixed line

```text
u=j/2^K.
```

Thus the record `(e,K,j)` is a component-indexed record on one fixed metric
space, not a symbolic cylinder whose physical endpoint still moves.  At
`K=2` there are exactly `64*4=256` components.  At cutoff `L` the common
refinement has `64*2^L` components and `64*(2^L+1)` labelled boundary
components.

The uniform positive-mass and graph-current bounds give the exact boundary
tightness

```text
|J_s|([S_L]_rho)
 <= min(16128/5, (32256/5)(2^L+1) rho).
```

Hence the dyadic record boundary has exponent `theta=1`.  For every fixed
cutoff, continuity of the total row masses and analytic one-sided trace maps
gives BL-star convergence on this same carrier as `s->0`.  The certificate
materializes and checks the arithmetic through `L=12`; the displayed formula
proves the same statement for every finite `L`.

This closes the precise tenth-pass blocker

```text
moving dyadic endpoints not registered in the Gate-3 common DQ atlas.
```

It does **not** construct the future-dynamical common atlas.  The carrier
above registers the stopped endpoints and the depth-one face current only;
preimages of later grazing/owner singularities under `T_s^k` are additional
boundaries and are not silently included.

## 2. A genuine physical `s=0` depth-two registry

The second layer is a direct billiard replay, not the formal operator
telescope.  On every one of the 64 maximal rows it performs:

1. the tangent event and its already-certified strict miss owner;
2. the exact miss collision and specular reflection;
3. comparison with the complete shifted 68- or 76-target horizon candidate
   universe;
4. certification of a unique next target before time `3` on each retained
   connected interval.

The contact and reflection formulas are evaluated in a dependency-reduced
form.  If `ell=u dot d`, `w=u_perp dot d`,
`Delta=R^2-w^2`, then

```text
q_miss-C_m = -sqrt(Delta) u - w u_perp,
u_out = (1-2 Delta/R^2)u - (2 sqrt(Delta)w/R^2)u_perp.
```

The one-sided grazing continuation is also recordwise exact:

```text
T_0^tr(z_T(theta)) = y_M(theta).
```

Indeed reflection at exact tangency leaves the velocity unchanged, and the
declared miss owner is the first strict collision after that contact.  The hit
trace therefore enters the new registry after its canonical grazing
continuation, while the miss trace enters it immediately.

### Quantitative replay

The replay uses 384-bit Arb arithmetic, 2,048 initial connected intervals,
and adaptive depth at most 10.  It obtains

```text
certified immutable leaf components       185,068
certified normalized 64-row length        128399/2048
certified-box coverage                     128399/131072
                                             = 97.96066284179688%

unresolved outer-cover leaf boxes          42,768
unresolved normalized 64-row length        2673/2048
unresolved outer-cover fraction            2673/131072
                                             = 2.039337158203125%
distinct certified next-target labels      31
```

The two open-row endpoints are removed by an **absolute inward angular** trim
`2^-20` on each side.  In the actual coordinate formula

```text
distance = trim + (row_width-2 trim)t,
```

`trim` is a `dtheta` width, not a normalized-`t` width.  Therefore the
uniform density bound `18/5 dtheta` gives, without an extra row-width factor,

```text
endpoint cemetery positive mass <= 9/20480,
endpoint cemetery graph TV      <= 9/10240.
```

The unresolved fraction `2673/131072` is the length of a finite-resolution
**outer cover of boxes that may meet a second-collision singularity**.  It is
not a lower bound, and it makes no claim that the actual singular set has
positive length or positive physical mass.  Of the 42,768 unresolved boxes,
42,632 are conservative possible-earlier-tangency boxes and 136 are
dependency-limited original-miss boxes.

### The actual `s=0` singular set has zero coarea mass

The positive outer-cover length above is purely computational.  A separate
analytic audit checks all `4,704` next-target tangency discriminant functions.
For every occurrence/candidate pair, one of the 16 dyadic points

```text
t=(2j+1)/32,  0<=j<16,
```

has a 384-bit Arb enclosure strictly separated from zero.  Hence none of the
discriminants is identically zero.  On each open maximal row the original
miss discriminant is strictly positive and all subsequent circle-flight and
reflection formulas are real analytic.  Therefore:

```text
each candidate tangency zero set is discrete on the open row;
it is finite on every compact trimmed subarc;
the finite candidate union is at most countable on the open row;
its row length and corrected coarea mass are exactly zero.
```

Distinct periodic scatterer disks are disjoint, so two strict positive
collision roots cannot coincide.  The first next target can change only when
a candidate root is born or dies at one of those tangencies.  Consequently
the complement is a countable union of connected intervals on which the next
target is immutable; ordering those intervals gives a full-measure
component-indexed `s=0` depth-two atlas, finite on every compact trim.

The explicit box registry and the analytic atlas play different roles: the
former supplies `185,068` replayable labels on 97.96% of the normalized
domain, while the latter proves that the actual omitted `s=0` singular set is
zero-coarea.  Neither statement supplies finite-`s` root continuation or a
uniform dynamic boundary-`Z` constant.

In particular, a countable full-measure `s=0` atlas is not the finite common
`A_{L,m,n}` required by v52: possible endpoint accumulation must still be
absorbed with a uniform finite-`s` collar and the same dynamic test modulus.

## 3. What the exact telescope would still need

The depth-two identity is

```text
(P_s^2-P_0^2)/s
 = P_s ((P_s-P_0)/s) + ((P_s-P_0)/s) P_0.
```

It becomes an analytic depth-two DQ theorem if, on fixed spaces `B2,B0`,

```text
P_0(B2) subset B2,
P_s -> P_0 in B0->B0,
((P_s-P_0)/s) -> D_0 in B2->B0
```

in operator norm.  Then the quotient converges in `B2->B0` to

```text
P_0 D_0 + D_0 P_0.
```

The frozen input proves only fixed-source convergence for each `C^1` source.
It does not prove that every component-restricted `P_0 h` stays in one strong
space, uniform fixed-time source invariance, or operator-norm one-step DQ.
The unresolved second-singularity outer cover is exactly where those missing
restriction estimates must act.  Therefore no formal cancellation is used
as a replacement for convergence.

## 4. Exact remaining boundary

Fixed-time branch-record `MT_DQ` still needs all of:

1. finite-`s` continuation of the root-isolated `s=0` atlas across the
   second-collision parameter strips, with a uniform boundary-`Z` estimate;
2. a positive domination or vanishing-collar theorem for those strips on the
   same common component atlas;
3. strong-source invariance and operator-norm DQ for every component
   restriction;
4. common BL convergence of the dynamic branch tests away from the complete
   future singular set;
5. regular, face, product-current, and response propagation on that identical
   atlas.

Physical `FACE_2CUT/FACE_TIME` additionally still need genuine physical word
depth, record-preserving propagated-`q` domination, the no-`|s|^-1` positive
per-depth estimate, repeated-cut recovery, and the physical norm lifts.  The
finite-`s` auxiliary recovery clock is not substituted for any of them.

## 5. Technology boundary

The newest applicable frozen audit remains unchanged.  Stenlund--Young--Zhang
`arXiv:1210.0011v4` gives uniform one-time recovery on the compact moving-table
class, but not a differentiable future-singularity atlas.  Demers--Liverani
`arXiv:2606.10155v1`, Problem 8.7, explicitly leaves general loss of memory
after characteristic-function restrictions open.  Canestrari
`arXiv:2604.19671v2` supplies a closed-map Growth Lemma layer, not the present
finite-`s` branch-record DQ or repeated-cut interface.  No theorem in the
2026-07-16 audit closes the five items above.

## 6. Reproduction and fail-closed behavior

```bash
PY=/tmp/cm2-flint-venv/bin/python

$PY -m py_compile \
  deliverables/cm2_gate3_iterated_common_atlas_mt_dq_cert.py \
  deliverables/cm2_gate3_iterated_common_atlas_mt_dq_verifier.py

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_iterated_common_atlas_mt_dq_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_iterated_common_atlas_mt_dq_verifier.py \
  --self-test

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate3_iterated_common_atlas_mt_dq_verifier.py
```

The replay and nine-mutation self-test exit zero.  The live default prints
the two certified sublayers, keeps finite-`s` depth two, `MT_DQ`,
`FACE_2CUT/FACE_TIME`, and Gate 3 `NOT_CERTIFIED`, and exits `2` by design.
