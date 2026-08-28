# CM2 Gate 1: compact logarithmic gauge and local-plaque holonomy assault

Date: 2026-07-16 (Asia/Shanghai)  
Frozen input: the eleventh-round exact QNL logarithmic-gauge frontier  
Strict verdict: **one seam-free gauge on the physical QNL return section and
canonical limits for every pair on the local QNL stable/unstable plaques are
certified; a global faithful coding, global Hoelder holonomies, typed twisting,
Gate 1 and unconditional CM2 remain `NOT_CERTIFIED`**

## 1. Result

The eleventh round constructed the exact local two-axis gauge

```text
B_u(x)B_s(y)
 =(I+k x^2 log|x| E_12)(I+k y^2 log|y| E_21),
k=-325/(144 log(mu)),
```

and proved convergence of the stable and unstable canonical tails relative
to the QNL periodic point.  This pass removes the artificial chart-boundary
qualification and promotes reference-point tails to all pairs on each local
QNL plaque.

Choose nested neighbourhoods on the same analytic, non-grazing induced
return branch,

```text
p in U_core,  closure(U_core) subset U_chart,
```

and a smooth cutoff `chi` which is one on `U_core` and zero on a collar of
the boundary of `U_chart`.  Define

```text
t_s(x,y)=chi(x,y) k y^2 log|y|,
t_u(x,y)=chi(x,y) k x^2 log|x|,

B_hat=(I+t_u E_12)(I+t_s E_21)  on U_chart,
B_hat=I                             outside U_chart.
```

Then `B_hat` is a single globally defined gauge on the return section.  It is
`C^1` and `C^{1,alpha}` for every `alpha<1`, equals the identity on a full
chart-boundary collar, and has determinant one exactly.  Hence no transition
or inverse singularity is introduced at the support boundary.

## 2. Why compact support preserves the repaired tails

Every sufficiently local stable point enters `U_core` and stays there in
forward time.  Every sufficiently local unstable point does the same under
backward iteration.  From the entry time onward, `B_hat` equals the exact
local logarithmic gauge of the predecessor certificate.  Before entry, only
finitely many fixed invertible factors occur.

The predecessor's summable envelopes

```text
O(n mu^n),  O(n mu^(2n)),  O(mu^(4n))
```

therefore remain summable.  Thus, for every sufficiently local point `z`,

```text
H^s_(p,z)=lim_(n->infinity) A_hat^n(z)^-1 A_hat^n(p),
H^u_(p,z)=lim_(n->-infinity) A_hat^n(z)^-1 A_hat^n(p)
```

exist in the appropriate local stable or unstable plaque.  The result is not
restricted to a selected orbit representative.

## 3. Exact all-pairs local-plaque factorisation

For finite `n`, reference-point transports satisfy the algebraic identity

```text
H^s_(x,y;n)
 =A_hat^n(y)^-1 A_hat^n(x)
 =H^s_(p,y;n) (H^s_(p,x;n))^-1.
```

Both factors converge, so

```text
H^s_(x,y)=H^s_(p,y)(H^s_(p,x))^-1
```

exists for every pair `x,y` on the declared local stable plaque.  The
backward identity gives the same statement on the local unstable plaque.
The identity, inverse and cocycle/groupoid laws follow from the same finite-n
matrix identities and passage to the limit.

This is stronger than two selected tails and weaker than a global holonomy
family.  No uniform Hoelder modulus over all symbolic rectangles has been
proved.

## 4. Exact remaining boundary

The compact extension closes two local compatibility questions:

```text
single seam-free gauge on the QNL return section:       CERTIFIED
all-pairs canonical limits on local stable plaque:      CERTIFIED
all-pairs canonical limits on local unstable plaque:    CERTIFIED
```

It does not supply:

1. a finite faithful coding of the full physical derivative cocycle;
2. one uniform Hoelder holonomy modulus over every coded plaque;
3. compatible transport across every physical singularity/chart overlap;
4. a genuine typed QNL homoclinic loop with twisting in this same gauge;
5. the Butler--Park class-`H` or projective spectral/PPE conclusion.

The periodic eigenvalue ratio is unchanged under a bounded point-dependent
gauge, so Park--Piraino fiber bunching on the two frozen natural codings
remains impossible.  No global Gate-1 claim is made.

## 5. Latest-technology boundary

The official arXiv search was rerun on 2026-07-16 after the generic search
provider rate-limited.  It found no 2026 theorem turning one local compact
gauge into the missing singular-billiard global coding and uniform canonical
holonomy family.  Butler--Park `arXiv:1909.11548v2` still assumes precisely
that global class-`H` input.  The compact-support argument above is therefore
a direct local advance, not an imported global bypass.

## 6. Reproduction

```bash
PY=/tmp/cm2-flint-venv/bin/python

$PY -m py_compile \
  deliverables/cm2_gate1_compact_log_gauge_plaque_holonomy_frontier_cert.py \
  deliverables/cm2_gate1_compact_log_gauge_plaque_holonomy_frontier_verifier.py

$PY deliverables/cm2_gate1_compact_log_gauge_plaque_holonomy_frontier_verifier.py \
  --replay --integrity-only
$PY deliverables/cm2_gate1_compact_log_gauge_plaque_holonomy_frontier_verifier.py \
  --self-test

# Expected exit 2: global class H and Gate 1 remain fail-closed.
$PY deliverables/cm2_gate1_compact_log_gauge_plaque_holonomy_frontier_verifier.py
```
