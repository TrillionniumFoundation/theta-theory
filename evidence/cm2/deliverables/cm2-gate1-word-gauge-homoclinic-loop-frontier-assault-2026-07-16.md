# CM2 Gate 1: finite-word gauge and homoclinic-loop frontier assault

Date: 2026-07-16 (Asia/Shanghai)  
Frozen inputs: compact QNL gauge/plaque holonomies, clean basic-set topology,
the 96-collision closed shadow, and the BV typing obstruction  
Strict verdict: **finite-word chart/gauge compatibility and homoclinic-tail
typing are certified; no specific QNL twisting loop is certified, so Gate 1
remains open**

## 1. Exact advance

The compact logarithmic gauge is not merely a matrix available in one local
calculation.  Because its cutoff vanishes on a collar of the QNL chart
boundary, it defines one intrinsic bundle automorphism `B_hat` on the whole
declared return section.  In any other tangent chart its matrix is obtained
by ordinary coordinate conjugacy; there is no independent connector-gauge
choice to match.

On the full collision section, use this automorphism on the selected QNL
obstacle component and the identity on every other (disjoint) obstacle
component.  It is important to separate the two base maps.  Let `T` be the
one-collision billiard map with derivative cocycle `C`.  The QNL orbit has
full-collision period two, so the phase-aligned return is

```text
F=T^2,  A(x)=C^2(x),  Fp=p.
```

During a finite excursion, the orbit may leave the local QNL branch; only
regularity of the finite physical word is needed.

For the one-collision cocycle define

```text
C_hat(x)=B_hat(Tx)^-1 C(x) B_hat(x).
```

The inverse placement is forced by the frozen resonant-gauge convention
`B(Fx)^-1 A(x) B(x)`; reversing it would describe a different gauge.

Exact multiplication gives, on every finite regular collision word,

```text
C_hat^m(x)=B_hat(T^m x)^-1 C^m(x) B_hat(x).           (1.1)
```

The return cocycle is consequently

```text
A_hat(x)=C_hat^2(x)=B_hat(Fx)^-1 A(x) B_hat(x),
A_hat^n(x)=B_hat(F^n x)^-1 A^n(x) B_hat(x).           (1.2)
```

Every intermediate factor cancels in both (1.1) and (1.2).  Thus the QNL and
connector finite-word charts do not leave an overlap cocycle.  For a closed
`m`-collision word based at `z`,

```text
L_hat(z)=B_hat(z)^-1 L(z) B_hat(z).
```

In particular, `T^96 z_*=z_*` gives this formula for the already certified
96-collision periodic shadow.  It remains an endomorphism of `E_(z_*)`; the
conjugacy does not move it to the QNL fiber.

## 2. Local holonomies extend along genuine global tails

Let `p` be the QNL point fixed by `F=T^2`.  The frozen compact-gauge
certificate gives canonical stable and unstable limits on the sufficiently
local plaques through `p`.  If a global stable point `z` enters that plaque
after `N` returns, `z_N=F^N z`, the finite-prefix identity is

```text
H^s_(p,z)
 =A_hat^(N)(z)^-1 H^s_(p,z_N) A_hat^(N)(p)
 :E_p -> E_z.                                         (2.1)
```

Likewise, if `z_-N=F^-N z` is in the local unstable plaque,

```text
H^u_(p,z)
 =A_hat^(-N)(z)^-1 H^u_(p,z_-N) A_hat^(-N)(p)
 :E_p -> E_z.                                         (2.2)
```

The right sides contain only finite invertible factors and an already
convergent local tail.  Hence local convergence extends to every regular
global point on the corresponding QNL stable or unstable leaf.

The frozen topology audit independently places QNL and the connector in one
nontrivial clean locally maximal hyperbolic `T`-basic set.  Passing to the
cyclic component for `F=T^2` that contains the selected phase `p` preserves
local product structure and supplies nontrivial clean phase-aligned points

```text
z in W^s_F(p) intersection W^u_F(p).
```

This cyclic-component step is what makes the two tails in (2.1)--(2.2) end
at the same QNL phase.  For every such point `z`,

```text
H^u_(p,z):E_p -> E_z,
H^s_(z,p):E_z -> E_p,
```

so the endomorphism

```text
psi_z = H^s_(z,p) o H^u_(p,z) : E_p -> E_p
```

is well typed in the repaired cocycle.  This is an existential typing result:
no coordinate, immutable bi-infinite itinerary, or numerical matrix for a
particular `z` is selected here.  In particular, existence and typing alone
say nothing about the four twisting wedges.

## 3. Why the finite shadow still does not give twisting

The frozen 96-collision orbit is based at `z_*`.  It is periodic and distinct
from the QNL orbit, so the earlier exact periodic-orbit argument refutes
`z_* in W^s(p) intersection W^u(p)`.  Its matrix has type

```text
L : E_(z_*) -> E_(z_*),
```

whereas a QNL homoclinic loop has type

```text
psi_z : E_p -> E_p.
```

Putting both matrices into the same gray coordinate chart is not a canonical
fiber map.  In particular, the raw expression `psi_z=L` is ill typed.  If the
periodic shadow is to be used, one must first certify a gauge-covariant
transport

```text
J_(z_*,p):E_(z_*) -> E_p
```

and compare two endomorphisms of the same fiber,

```text
psi_z
  versus
J_(z_*,p) L J_(z_*,p)^-1 : E_p -> E_p.               (3.1)
```

The frozen gauge counterexample changes a strict raw shadow wedge to exact
zero, so even an extremely small untyped cross-fiber identification cannot
be used.

The first missing interface is therefore exactly

```text
SHADOW_TO_HOMOCLINIC_ORBIT_COCYCLE_IDENTIFICATION.
```

It requires all of the following data in one certificate:

1. one selected regular bi-infinite `p`-tail/excursion/`p`-tail orbit `z`,
   with immutable physical itinerary and stable/unstable plaque-entry times;
2. its actual infinite-tail map `psi_z=H^s H^u` on `E_p`;
3. either a direct computation of `psi_z`, or a certified transport `J` and
   an equality/error bound comparing `psi_z` with `J L J^-1`; and
4. four nonzero wedges between `psi_z` and the two QNL Perron lines.

None is provided by finite endpoint conjugacy alone.

## 4. Strict labels

```text
FINITE_REGISTERED_WORD_GAUGE_COMPATIBILITY:       CERTIFIED
CHART_OVERLAP_OR_CONNECTOR_GAUGE_PATCH:            NOT NEEDED FOR FINITE WORDS
QNL_HOLONOMIES_ALONG_ANY GENUINE FINITE-TAIL ORBIT: CERTIFIED
EXISTENTIAL_TYPED_QNL_HOMOCLINIC_ENDOMORPHISM:     CERTIFIED
SELECTED_IMMUTABLE_QNL_HOMOCLINIC WORD/POINT:      NOT CERTIFIED
SHADOW L = QNL HOMOCLINIC psi_z:                   NOT CERTIFIED
FOUR QNL-FIBER TWISTING WEDGES:                    NOT CERTIFIED
UNIFORM ALL-PLAQUE HOLDER HOLONOMIES / CLASS H:    NOT CERTIFIED
GATE 1:                                             NOT CERTIFIED
```

The positive existential endomorphism must not be shortened to “typed
twisting loop”: twisting is precisely the missing numerical property.  Nor
may the closed-word conjugacy be described as a transport from `E_(z_*)` to
`E_p`; it only changes the gauge on `E_(z_*)`.

## 5. Reproduction

```bash
PY=python3
$PY -m py_compile \
  deliverables/cm2_gate1_word_gauge_homoclinic_loop_frontier_cert.py \
  deliverables/cm2_gate1_word_gauge_homoclinic_loop_frontier_verifier.py

$PY deliverables/cm2_gate1_word_gauge_homoclinic_loop_frontier_verifier.py \
  --replay --integrity-only

$PY deliverables/cm2_gate1_word_gauge_homoclinic_loop_frontier_verifier.py \
  --self-test

# Expected fail-close live verdict: exit 2.
$PY deliverables/cm2_gate1_word_gauge_homoclinic_loop_frontier_verifier.py

sha256sum -c \
  deliverables/cm2-gate1-word-gauge-homoclinic-loop-frontier-manifest-2026-07-16.sha256
```
