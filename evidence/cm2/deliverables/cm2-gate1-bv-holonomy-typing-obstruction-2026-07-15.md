# CM2 Gate 1: Bonatti--Viana holonomy-typing audit

Date: 2026-07-15  
Model: frozen centered rational fixed-section pilot  
Scope: the exact QNL periodic point `p_A` and the certified 96-collision
closed shadow orbit `z_*`  
Verdict: **finite shadow twisting remains certified; strict QNL-fiber
holonomy identification is OPEN / NO-GO**

## 1. What was tested

The previous certificate produced a genuine closed billiard word based at
`z_*`, a consecutive same-orbit derivative `L:T_{z_*}M -> T_{z_*}M`, and
four nonzero wedges after both `T_{z_*}M` and `T_{p_A}M` were written in the
same global gray `(s,p)` coordinates.  The remaining question was whether
this is the twisting loop required by Bonatti--Viana/Park--Piraino.

The answer is currently **no**.  Three independent issues were audited:

| item | result |
|---|---|
| `z_*` is a `p_A`-homoclinic point | **REFUTED** |
| Park--Piraino fiber bunching for the natural two-collision coding | **REFUTED** |
| Park--Piraino fiber bunching for the induced gray-return coding | **REFUTED** |
| global gray trivialization is a canonical holonomy | **REFUTED** |
| an alternative actual one-vertex locally constant coding | **NOT CERTIFIED** |
| exact `H^s H^u` loop on the `p_A` fiber | **OPEN / FAIL-CLOSED** |

This does not retract any finite geometric statement from
`cm2_gate1_closed_shadow_twisting_cert.py`.  It prevents that finite result
from being silently promoted to the theorem-level typicality hypothesis.

## 2. Exact theorem requirement

Park--Piraino, *Transfer operators and limit laws for typical cocycles*,
[arXiv:2007.02349](https://arxiv.org/abs/2007.02349), Section 2 and Definition
2.2, work with a theta-Hölder, fiber-bunched cocycle over a subshift.  In
their normalization,

```text
||A(x)|| ||A(x)^(-1)|| < 2^theta,    0 < theta <= 1.
```

Fiber bunching supplies the canonical limits

```text
H^s_{x,y} = lim_{n -> +infinity} A^n(y)^(-1) A^n(x),
H^u_{x,y} = lim_{n -> -infinity} A^n(y)^(-1) A^n(x).
```

Their 1-typicality definition then requires a periodic point `p`, a genuine
`p`-homoclinic point `z`, and the endomorphism of the **`p` fiber**

```text
psi_z = H^s_{z,p} o H^u_{p,z}.
```

Thus a finite periodic product at a nearby basepoint is not the same object.
One must either certify the displayed limits and the homoclinic typing, or
construct an exact finite Markov model for the actual cocycle in which the
holonomy loop legitimately reduces to a finite one-vertex excursion.

## 3. The natural derivative cocycle is not Park--Piraino fiber-bunched

The exact QNL two-collision return matrix is

```text
P_A = [[alpha,beta],[gamma,alpha]],

alpha = (661-325 sqrt(2))/36,
beta  = (859-550 sqrt(2))/100,
gamma = 625(25-4 sqrt(2))/324,
det P_A = 1.
```

The new certificate first checks `det P_A=1` exactly in `Q(sqrt(2))`, then
uses 900-bit Arb for the strict spectral inequalities

```text
lambda_u = 11.09770193380148422524... > 11,
lambda_s =  0.09010874557318850472... in (0.09,0.091),
lambda_u/lambda_s = 123.1589882115012025611... > 123.
```

For every operator norm,

```text
kappa(P_A)=||P_A|| ||P_A^(-1)||
          >= |lambda_u|/|lambda_s|
          > 123.
```

On the natural solid-collision coding, `p_A` has period two.  If each step
satisfied Park--Piraino fiber bunching, submultiplicativity would give

```text
kappa(P_A) < (2^theta)^2 <= 4,
```

contradicting the certified lower bound.  If the gray-to-gray QNL return is
instead taken as one induced step, `p_A` is fixed and the required bound is
even stronger:

```text
kappa(P_A) < 2^theta <= 2.
```

Therefore the Park--Piraino fiber-bunching hypothesis is rigorously false
for both natural codings already present in the certificate stack.  This is
a periodic spectral obstruction and cannot be repaired by merely changing
the gray fiber coordinates.

This conclusion is deliberately scoped.  It does not assert that every
conceivable recoding or every direct stable/unstable limit is impossible.
An alternative coding must be explicitly constructed, must represent the
actual billiard derivative cocycle rather than frozen periodic matrices,
and must carry its own Hölder/fiber-bunching or direct convergence proof.
None is currently certified.

## 4. `z_*` is not a `p_A`-homoclinic point

The predecessor's frozen interval-Newton box is

```text
a(z_*) = -8.2937621943296019634...e-15 +/- 3.60e-200,
p(z_*) = 0,
```

whereas the gray phase of the QNL point has `a(p_A)=0, p(p_A)=0`.  The box
strictly excludes zero.  The predecessor certifies that `z_*` is periodic
under its 96-collision word; `p_A` is the distinct period-two QNL orbit.

The elementary periodic-orbit lemma is decisive.  If two periodic points of
an invertible map are forward asymptotic, then the finite sequence of
distances obtained over the least common multiple of their periods repeats
forever.  A repeating nonnegative sequence can converge to zero only if
every entry is zero.  Hence the two points lie on the same periodic orbit.
The same argument holds backward.  Consequently a periodic orbit distinct
from `p_A` cannot be in both `W^s(p_A)` and `W^u(p_A)`.

It follows that neither `H^u_{p_A,z_*}` nor `H^s_{z_*,p_A}` has the basepoint
typing appearing in Definition 2.2.  Finite shadowing for ten QNL returns
does not replace asymptotic agreement for all negative and positive times.

## 5. Exact gauge counterexample to the global-coordinate shortcut

The closed shadow derivative has the certified form

```text
L = [[a_L,b_L],[c_L,a_L]],    b_L>0, c_L>0.
```

Its Perron slopes are `+/-k_L`, where

```text
k_L^2 = c_L/b_L.
```

Let `+/-k_A` be the QNL slopes.  In the original common gray coordinates,
the replayed same-line wedge is

```text
det(v_A^+,L v_A^+)
  = -4.0146568962138184860...e28 < -1e28.
```

Now change the fiber coordinates over the `z_*` orbit by the positive
matrix

```text
C = diag(1,r),
r = k_A/k_L
  = 1.0000000000000000000000000552267196578...,
```

and leave the coordinate gauge over `p_A` equal to the identity.  The new
shadow return is `L'=C L C^(-1)`.  Because `C(1,+/-k_L)` is exactly
`(1,+/-k_A)`, elementary algebra gives

```text
det(v_A^+,L' v_A^+) = 0,
det(v_A^-,L' v_A^-) = 0.
```

The certificate also checks that the corresponding Arb enclosures contain
zero.  The identities themselves are exact consequences of
`r=k_A/k_L` and `k_L^2=c_L/b_L`; no rounded-zero acceptance test is used.

This is a legitimate Hölder gauge counterexample on any finite Markov
coding containing the two disjoint periodic orbits.  Choose disjoint clopen
cylinder neighborhoods of the finite `z_*` orbit and the `p_A` orbit; set
the gauge to the displayed positive matrix on the former and to the
identity on the latter.  The result is locally constant, hence Hölder.

Canonical holonomies are gauge-covariant: a genuine loop on the `p_A` fiber
and the `p_A` eigenlines transform together, so its twisting property is
unchanged.  The raw identity map between `T_{z_*}M` and `T_{p_A}M` does not
have that invariance.  The explicit gauge above changes a strict raw wedge
to exact zero.  Therefore

```text
GLOBAL_GRAY_TRIVIALIZATION_AS_CANONICAL_HOLONOMY: REFUTED.
```

The fact that `C` is only about `5.5e-26` from the identity also shows why a
large raw wedge is not a robustness substitute: `L` expands by about
`1e53`, so an extremely small cross-fiber gauge change can alter the wedge
by order `1e28`.

## 6. Why the one-vertex shortcut is still open

A locally constant one-vertex model could, in principle, reduce a
homoclinic holonomy loop to a finite excursion.  But the object needed is a
bi-infinite coded point with `p_A` tails in both time directions and one
finite admissible excursion.  Repeating the excursion instead produces the
distinct periodic point `z_*`, which is exactly the wrong basepoint type.

The current certificates establish a physical QNL-to-connector full cross,
its reversible counterpart, and the repeated closed shadow word.  They do
not yet establish all of the following:

1. one finite Markov coding with a declared `p_A` vertex and a single
   `p_A`-tail/excursion/`p_A`-tail homoclinic sequence;
2. the actual billiard derivative cocycle on that coding, with the needed
   regularity and canonical holonomies;
3. equality of its homoclinic loop with the previously computed periodic
   shadow matrix `L`;
4. four nonzero wedges for `psi_z` in the exact `p_A` fiber.

Freezing the QNL, connector, and transition matrices as symbol labels would
define a different locally constant cocycle.  It cannot certify the actual
place-dependent billiard derivative without a further cohomology or exact
constancy theorem.

## 7. Minimal remaining theorem-level task

The shortest honest route is now one of the following.

**Direct holonomy route.**  Construct a genuine
`z in W^u(p_A) intersection W^s(p_A)` through the certified heteroclinic
cycle; prove convergence of both derivative limits (without appealing to
the refuted natural fiber-bunching condition); compute
`psi_z=H^s H^u` on `T_{p_A}M`; and certify all four wedges there.

**Alternative coding route.**  Give an explicit finite Markov coding and
metric/Hölder exponent for the actual cocycle, prove the applicable
holonomy theorem or direct one-vertex reduction, and then compute its exact
excursion matrix.  Any recoding must retain the actual place dependence of
the derivative.

Until one route is completed, the correct labels are

```text
PARK_PIRAINO_CANONICAL_HOLONOMY_FROM_FIBER_BUNCHING: UNAVAILABLE
FINITE_ONE_VERTEX_ACTUAL_DERIVATIVE_COCYCLE: NOT CERTIFIED
BONATTI_VIANA_QNL_FIBER_HOLONOMY_IDENTIFICATION: OPEN / FAIL-CLOSED
GATE1_UNCONDITIONAL_TYPICALITY_INPUT: OPEN / NO-GO
```

## 8. Reproduction

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate1_bv_holonomy_typing_obstruction_cert.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate1_bv_holonomy_typing_obstruction_cert.py

sha256sum -c \
  deliverables/cm2-gate1-bv-holonomy-typing-obstruction-manifest-2026-07-15.sha256

sha256sum -c deliverables/cm2-v52-manifest.sha256
```

The new certificate must exit zero.  This is a successful obstruction
certificate, not a successful holonomy identification.  The frozen v52 and
predecessor artifacts are read but never modified.
