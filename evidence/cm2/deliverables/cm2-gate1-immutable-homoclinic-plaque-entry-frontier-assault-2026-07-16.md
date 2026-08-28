# CM2 Gate 1: immutable QNL homoclinic orbit and plaque-entry frontier

Date: 2026-07-16 (Asia/Shanghai)  
Frozen baseline: twelfth-round Gate 1 stacks and every earlier geometric
certificate  
Strict verdict: **one immutable, regular, phase-aligned physical QNL
homoclinic itinerary and its plaque-entry times are certified; the selected
holonomy loop is now well typed, but its numerical matrix, four twisting
wedges, global class `H`, and Gate 1 remain `NOT_CERTIFIED`**

## 1. Exact advance

Let `T` be the one-collision billiard map, `I(theta,p)=(theta,-p)` its
time-reversal involution, and `F=T^2` the phase-aligned QNL return fixing the
selected normal point `p`.  In exact QNL eigen-coordinates `(x,y)`, the frozen
graph-transform certificate supplies

```text
W^u_loc(p)={(x,h_u(x)): |x|<=2e-9},
|h_u(x)|<=x^2,  |h_u'(x)|<=1e-4.
```

The present certificate fixes the interval

```text
x in x_0 +/- 1e-50,
x_0=-8.29376219432960196343742681642621812913699299...e-15,
```

and replays the complete 48-collision half word

```text
Q5^2 B^2.
```

Here `Q5` is the frozen ten-collision/five-QNL-return block and `B` is the
frozen fourteen-collision connector block.  A collision-by-collision,
correlation-preserving 1000-bit Arb Taylor replay covers the whole graph tube

```text
|y|<=7e-29.
```

This tube strictly contains `h_u(x)` throughout the root interval.  On its
two `x` faces the terminal momentum obeys, uniformly in the transverse
coordinate,

```text
p_48(left)<-1e-23,   p_48(right)>1e-23.
```

On the entire box,

```text
partial_x p_48 >2e27,   |partial_y p_48|<100.
```

Consequently, along every graph with `|h'|<=1e-4`,

```text
d/dx p_48(x,h(x)) >1e27.
```

The intermediate-value theorem and strict monotonicity therefore select one
and only one actual invariant-graph point

```text
z_h=(x_h,h_u(x_h))
```

in the frozen interval for which `T^48 z_h` lies on `Fix(I)={p=0}`.  The
decimal centre is merely a discovery seed; acceptance uses the two strict
face signs and the derivative lower bound, not the centre residual.

## 2. Immutable physical itinerary and plaque-entry times

The half-word tube has the uniform physical margins

```text
minimum flight        >18/100,
minimum discriminant > 1/100,
minimum incidence     >63/100,
minimum clearance     >22/100.
```

All registered lifts are replayed, the terminal half lift is `(0,0)`, and
the frozen lattice-exhaustion test is rerun.  Thus the root is regular and
the collision word is physical, not a formal symbolic concatenation.

If `w=T^48 z_h`, then `Iw=w`.  Exact reversibility gives

```text
T^48 w = I z_h,
T^96 z_h = I z_h.
```

The reflected half is `B^2 Q5^2`, so the complete immutable excursion is

```text
Q5^2 B^4 Q5^2                         (96 solid collisions).
```

Both the half and full key tuples are stored through their complete block
registries and SHA-256 digests in the JSON manifest.  Since `z_h` is already
on `W^u_loc(p)` and `I z_h` is on `W^s_loc(p)`, while 96 collisions equal 48
`F` returns, the entry times are exactly

```text
unstable local plaque: N_u=0,
stable local plaque:   N_s=48,
F^48 z_h=I z_h.
```

The bi-infinite physical record is therefore

```text
... QNL | Q5^2 B^4 Q5^2 | QNL ... .
```

It is phase aligned and nonperiodic.  Indeed the root interval excludes the
QNL point; a periodic point whose backward orbit converged to the QNL orbit
would have to be that orbit itself.

## 3. Explicit compact-gauge core for this orbit

The predecessor used abstract nested QNL neighborhoods.  This pass fixes
numerical disks

```text
r_core=1e-12,   r_chart=1e-10
```

and the standard flat bump

```text
beta(t)=0 (t<=0), exp(-1/t) (t>0),
sigma(t)=beta(1-t)/(beta(1-t)+beta(t)),
chi(x,y)=sigma(((x^2+y^2)-r_core^2)/(r_chart^2-r_core^2)).
```

Thus `chi=1` on the core disk and `chi=0` outside the chart disk.  The whole
square `|x|,|y|<=1e-10` is replayed through the exact QNL return and retains
strict flight, discriminant, incidence and clearance margins.  The selected
unstable endpoint and its reflected stable endpoint lie deep inside the core.
The frozen graph expansion keeps the backward unstable tail inside it; exact
reversibility gives the same for the forward stable tail.  Hence the compact
logarithmic gauge is literally equal to its local analytic formula on both
tails, from the certified entry times onward.

## 4. The selected typed loop

The twelfth-round finite-word algebra and local logarithmic-gauge limits now
apply to this particular immutable orbit rather than only to an existential
homoclinic point.  Put `A_hat` for the repaired `F` cocycle.  Then

```text
H_hat^u_(p,z_h):E_p -> E_(z_h),
H_hat^s_(z_h,p):E_(z_h) -> E_p,
psi_z=H_hat^s_(z_h,p) o H_hat^u_(p,z_h):E_p -> E_p.
```

Using `F^48 z_h=I z_h`, the exact finite-entry formula is

```text
psi_z
 =A_hat^48(p)^-1
  H_hat^s_(I z_h,p)
  A_hat^48(z_h)
  H_hat^u_(p,z_h).                    (4.1)
```

Every arrow in (4.1) has a declared source and target fiber.  This closes the
previous `SELECTED_IMMUTABLE_QNL_HOMOCLINIC_WORD/POINT` blocker and promotes
the loop from existential typing to one selected typed limit.

## 5. Why twisting is still fail-closed

The frozen local-tail proof records the summable orders

```text
O(n mu^n), O(n mu^(2n)), O(mu^(4n)),
```

but it does not provide numerical majorant constants, a certified truncation
index/error, or interval matrices for either local holonomy in (4.1).
Therefore the present data do not enclose `psi_z` numerically.

The 96-collision periodic shadow remains based at `z_*`, with

```text
L:E_(z_*) -> E_(z_*),
```

whereas (4.1) acts on `E_p`.  No gauge-covariant
`J:E_(z_*) -> E_p` and no bound comparing `psi_z` with `J L J^-1` have been
constructed.  The raw common-chart finite excursion is not a substitute:
the frozen gauge counterexample already shows that a tiny untyped change can
erase a strict raw wedge when the loop norm is enormous.

Consequently:

```text
SELECTED_IMMUTABLE_REGULAR_QNL_HOMOCLINIC ORBIT: CERTIFIED
PHYSICAL F-PLAQUE ENTRY TIMES 0 AND 48:          CERTIFIED
SELECTED TYPED QNL HOMOCLINIC LIMIT LOOP:        CERTIFIED
NUMERICAL MATRIX FOR psi_z:                      NOT CERTIFIED
psi_z VS J L J^-1 ERROR BOUND:                   NOT CERTIFIED
FOUR QNL-FIBER TWISTING WEDGES:                  NOT CERTIFIED
GLOBAL UNIFORM HOLDER HOLONOMIES / CLASS H:       NOT CERTIFIED
GATE 1:                                           NOT CERTIFIED
```

One selected loop cannot by itself supply Butler--Park class `H`: that also
needs a faithful global coding and one uniform Hölder holonomy family on all
coded plaques.

## 6. Latest-technology audit

The official arXiv feed was checked again on 2026-07-16 for recent
homoclinic-holonomy and non-fiber-bunched cocycle results.  No new theorem was
found that turns qualitative local convergence plus a singular-billiard
finite excursion into the missing numerical `psi_z` matrix, or that removes
the global class-`H` hypotheses.  The closest frozen references remain
Butler--Park (`arXiv:1909.11548v2`) and Park--Piraino
(`arXiv:2007.02349`), whose relevant interfaces are precisely the ones kept
open above.

## 7. Reproduction

```bash
PY=/tmp/cm2-flint-venv/bin/python

$PY -m py_compile \
  deliverables/cm2_gate1_immutable_homoclinic_plaque_entry_frontier_cert.py \
  deliverables/cm2_gate1_immutable_homoclinic_plaque_entry_frontier_verifier.py

$PY deliverables/cm2_gate1_immutable_homoclinic_plaque_entry_frontier_verifier.py \
  --replay --integrity-only

$PY deliverables/cm2_gate1_immutable_homoclinic_plaque_entry_frontier_verifier.py \
  --self-test

# Expected fail-close live verdict: exit 2.
$PY deliverables/cm2_gate1_immutable_homoclinic_plaque_entry_frontier_verifier.py

sha256sum -c \
  deliverables/cm2-gate1-immutable-homoclinic-plaque-entry-frontier-manifest-2026-07-16.sha256
```
