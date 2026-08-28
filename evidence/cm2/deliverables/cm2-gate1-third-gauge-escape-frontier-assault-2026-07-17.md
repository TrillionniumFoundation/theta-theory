# CM2 Gate 1: third-gauge finite-obstruction escape frontier

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the fifteenth-round same-representative shadow obstruction,
the connector first-jet obstruction, and the selected numerical QNL
homoclinic loop  
Strict verdict: **the two currently certified periodic first-jet witnesses
are not universal gauge obstructions.  They can be cancelled independently
by disjoint local `SL(2,R)` gauge bumps that equal the identity on the
selected homoclinic orbit closure, so the frozen loop and four wedges remain
unchanged.  Moreover, an exact full-shift example refutes any general claim
that the canonical holonomy family or weak typicality is invariant under
Hölder cohomology.  Both representatives in that example belong to class
`H`; no claim about invariance of class-`H` membership is made.
The actual billiard's variable-diagonal all-groupoid resonant equations and
uniform Hölder constants remain open; Gate 1 is `NOT_CERTIFIED`.**

## 1. Why a finite first-jet obstruction is repairable

Let `p` be a fixed point of a return `G`.  Work in common base-stable and
fiber eigen-coordinates, and write

```text
A(p)=diag(Lambda,nu),       DG(p)v_s=nu v_s,
Lambda nu=1.
```

Compose the current cocycle with a new gauge `E` satisfying `E(p)=I`, and
put `X=dE_p[v_s]`.  Direct differentiation gives

```text
dA_E[v_s]=dA[v_s]-nu X A(p)+A(p)X.
```

If `c` denotes the lower-left coefficient used by the frozen stable-tail
witness, then

```text
c_E=c+(nu-1)X_21.
```

Both frozen stable multipliers satisfy `nu!=1`.  Hence the exact choice

```text
X_21=c/(1-nu)
```

makes `c_E=0`.  The generator `X_21 E_21` is traceless, so it is an
`sl(2,R)` first jet.  The value `E(p)=I` leaves the periodic product and its
pinching eigenvalues unchanged.

This applies separately to the 96-collision periodic shadow and to the
connector return in its certified unstable/stable eigen-coordinates.  It
removes the particular nonzero-coefficient divergence witness.  It does
**not** imply that the repaired canonical comparison converges; higher
terms and all other plaques remain unanalysed.

## 2. The repair need not change the selected loop

The selected point `z_h` is a certified nonperiodic homoclinic point of the
QNL fixed point `p`.  Therefore

```text
K=closure(Orb(z_h))=Orb(z_h) union {p}.
```

A non-`p` periodic point cannot lie in `Orb(z_h)`: invertibility would make
`z_h` periodic.  Consequently the finite shadow and connector periodic
orbits are disjoint from the compact set `K`, and have positive distance
from it.

Choose mutually disjoint neighbourhoods of the relevant periodic base
points, also disjoint from a neighbourhood of `K` and from every other point
of either finite periodic orbit.  In a local section coordinate take

```text
E(q)=exp(chi(q) ell(q) M),
tr M=0, ell(q_*)=0, d ell_(q_*)(v_s)=1.
```

Choose `chi` identically one on a neighbourhood of `q_*`; in particular
`chi(q_*)=1` and `dchi(q_*)=0`.  It supplies compact support without changing
the requested first jet.  The two supports are mutually disjoint and avoid
all other points of their respective periodic orbits.  Products of the
shadow and connector corrections are still `SL(2,R)` valued and equal `I`
on a neighbourhood of `K`.

For every point of the selected orbit both endpoint gauge values in

```text
B_E(x)=E(Tx)^(-1) B(x)E(x)
```

are therefore `I`.  Every frozen finite stable/unstable approximant, its
limit loop, and all four selected wedges are exactly unchanged.  Thus a
third gauge can pass the two known finite jet tests without sacrificing the
selected twisting.  This is an escape from the tests, not an all-plaque
class-`H` construction.

## 3. Exact cohomologous class-H plus twisting model

The following model rules out a stronger but invalid no-go argument based
only on Hölder cohomology.

Let the base be the full two-shift with metric `d(x,y)=2^{-N(x,y)}` and put

```text
A=diag(2,1/2),             rho=1/4,
u(x)=sum_(k>=1) rho^k x_(-k),
v(x)=sum_(k>=1) rho^k x_k,
D(x)=(I+v(x)E_12)(I+u(x)E_21),
B(x)=D(sigma x)^(-1) A D(x).
```

The series are Lipschitz and bounded by `1/3`; `det D=1` exactly.  Thus `B`
is a Lipschitz cocycle continuously cohomologous to the constant diagonal
cocycle `A`.

For a local stable pair, `x_i=y_i` for `i>=0`, so

```text
u(sigma^n y)-u(sigma^n x)
  =4^{-n}(u(y)-u(x)).
```

Since

```text
A^{-n}E_21 A^n=4^n E_21,
```

the canonical stable limit is

```text
H^s_(x,y)
 =D(y)^(-1)[I+(u(y)-u(x))E_21]D(x).
```

If two sequences first differ at distance `N`, their `u` difference is at
most `(4/3)4^{-N}`.  Using `|u|,|v|<=1/3`, the exact max-row estimate for the
displayed holonomy is `52/81` times that difference; norm equivalence gives
a standard operator-norm Lipschitz constant strictly below `2`.

For a local unstable pair the symmetric identity is

```text
v(sigma^{-n}y)-v(sigma^{-n}x)
  =4^{-n}(v(y)-v(x)),
A^nE_12A^{-n}=4^nE_12.
```

With the chosen factor order in `D`, the endpoint factors cancel exactly
and `H^u_(x,y)=I` on local unstable plaques.  Both canonical families exist
and are Lipschitz.  Therefore `B` belongs to Butler--Park class `H`.

Now let `p=0^Z` and let the homoclinic point `z` have only `z_0=1`.  Here
`D(p)=D(z)=I`, and direct global-limit calculation yields

```text
H^s_(z,p)=I-E_21,
H^u_(p,z)=I+E_12,
psi_z=(I-E_21)(I+E_12)
     =[[1,1],[-1,0]].
```

For the two periodic eigenaxes,

```text
det(e_u,psi_z e_u)=-1,
det(e_s,psi_z e_s)=-1.
```

The constant diagonal representative `A` also belongs to class `H`: both of
its canonical families are the identity.  Hence `B` is weakly typical while
the cohomologous class-`H` representative `A` has zero twisting.

There is no reliance on allowing the same homoclinic point twice in the
definition.  Take `z_+` as above and take the distinct point `z_-` with its
only nonzero symbol at coordinate `1`.  Its loop is

```text
psi_(z_-)=[[1,1/4],[-4,0]],
```

so `det(e_s,psi_(z_-)e_s)=-1/4`, while the first point gives
`det(e_u,psi_(z_+)e_u)=-1`.

This example does not model the billiard's variable diagonal entries.  Its
purpose is exact and narrower: the canonical holonomy family and weak
typicality are not general Hölder-cohomology invariants outside the
fiber-bunched transport regime.  Since both `A` and `B` lie in class `H`, the
model neither proves nor disproves invariance of class-`H` membership.

## 4. Butler--Park scope

In `arXiv:1909.11548v2`, class `H` consists of representatives for which

1. the canonical stable and unstable limits converge; and
2. those canonical limits are Hölder in the base points.

The paper notes that continuous conjugacy preserves Lyapunov exponents,
pressure, and equilibrium states.  It does not state that canonical
holonomies or weak typicality are preserved by an arbitrary Hölder
conjugacy.  The exact model above shows why such a statement would be false.

Thus neither the diagonal class-`H` representative's zero twisting nor the
compact representative's finite periodic failures can decide the canonical
holonomies or weak typicality of every cohomologous representative.

## 5. Exact remaining Gate-1 boundary

The actual clean-horseshoe derivative in invariant frames is diagonal but
its two scalar entries vary Hölder-continuously with the full symbolic
point.  Closing Gate 1 now requires an actual gauge solving, simultaneously,

1. every stable groupoid resonant tail equation;
2. every unstable groupoid resonant tail equation;
3. uniform Hölder estimates for both canonical families; and
4. nonzero selected twisting in that same representative.

The full-shift constant model proves feasibility in principle but supplies
none of these variable-coefficient identities.  No finite list of
independently adjustable periodic first jets is a substitute for the global
groupoid compatibility problem.

```text
finite shadow/connector jet witnesses universal:       REFUTED
selected loop preserved by disjoint local repairs:      CERTIFIED
canonical holonomies invariant under Hölder cohomology: REFUTED
weak typicality invariant under Hölder cohomology:      REFUTED
class-H membership invariant under Hölder cohomology:   NOT ADDRESSED
actual variable-diagonal all-groupoid gauge:             NOT CERTIFIED
same actual representative with H plus twisting:         NOT CERTIFIED
Gate 1:                                                   NOT CERTIFIED
```

## 6. Replay

```bash
PY=/tmp/cm2-flint-venv/bin/python

PYTHONPATH=deliverables $PY -m py_compile \
  deliverables/cm2_gate1_third_gauge_escape_frontier_cert.py \
  deliverables/cm2_gate1_third_gauge_escape_frontier_verifier.py

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate1_third_gauge_escape_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate1_third_gauge_escape_frontier_verifier.py \
  --self-test

# Expected fail-close live verdict: exit 2.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate1_third_gauge_escape_frontier_verifier.py

sha256sum -c \
  deliverables/cm2-gate1-third-gauge-escape-frontier-manifest-2026-07-17.sha256
```
