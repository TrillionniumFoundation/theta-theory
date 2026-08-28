# CM2 Gate 1: variable-diagonal all-plaque groupoid frontier

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the faithful finite clean SFT, its invariant-frame diagonal
class-`H` representative, and the third-gauge escape audit  
Strict verdict: **the stable and unstable variable-diagonal resonant Green
equations are now solved separately on every plaque.  Their product has one
explicit noncommutative critical cross term; that nonlinear gluing limit is
not yet certified, so one same class-`H` twisting representative and Gate 1
remain open.**

## 1. Variable coefficients are not the linear obstruction

On the finite clean SFT write the faithful invariant-frame cocycle as

```text
A_diag(x)=diag(a_u(x),a_s(x)),
r(x)=a_s(x)/a_u(x),
sup |r|=kappa<1.
```

Apply the scalar Sinai cohomology lemma separately to the two diagonal
entries.  In a Hölder diagonal gauge both entries may be taken to depend only
on the future; the time-reversed lemma gives a diagonal-cohomologous ratio
depending only on the past.  These diagonal changes preserve every periodic
product and the QNL pinching eigenvalues.

For the future-normalised ratio and a Hölder future-cylinder marker `xi`, set

```text
u(x)=sum_{k>=1} r^(k)(sigma^-k x) xi(sigma^-k x).
```

The series converges uniformly and satisfies

```text
u(sigma x)=r(x)(u(x)+xi(x)).
```

For a local stable pair `x,y`, future dependence gives the exact identity

```text
u(sigma^n y)-u(sigma^n x)
 =r^(n)(x)(u(y)-u(x)).
```

The lower shear `L_u=I+uE_21` therefore has the canonical stable limit

```text
H^s_(x,y)
 =L_u(y)^-1 [I+(u(y)-u(x))E_21] L_u(x),
```

because conjugation by `A_diag^n` cancels the full variable product
`r^(n)(x)` exactly.  In the opposite time direction the same lower defect is
contracted.  The geometric series and the Hölder one-sided transfer give a
uniform Hölder modulus on every local plaque, and finite tails extend the
family to every global plaque.  Thus the lower-shear representative belongs
to Butler--Park class `H`.

The time-reversed construction gives an upper shear `U_v=I+vE_12` with the
same conclusions and an exact canonical unstable limit on every plaque.
Consequently the two variable-diagonal **linear** groupoid equations formerly
listed as unsolved are now solved separately.  No constant periodic ratio is
used.

## 2. The exact nonlinear gluing term

The two one-sided gauges cannot simply be multiplied while dropping their
commutator.  For `D=U_vL_u`, direct `2x2` algebra gives

```text
D_y D_x^-1
 =[[1+v_y du, dv-v_y du v_x],
   [du,         1-du v_x]],
du=u_y-u_x, dv=v_y-v_x.
```

The stable critical coordinate is the clean `du`, but the unstable critical
coordinate is

```text
dv-v_y du v_x.
```

Reversing the order gives

```text
D_y D_x^-1
 =[[1-u_x dv,       dv],
   [du-u_yu_xdv, 1+u_y dv]],
```

so the unstable coordinate is clean and the stable coordinate carries the
symmetric cross term.  The certificate replays both identities exactly over
the rationals.

For the first order, the only remaining all-plaque condition is uniform
Hölder convergence on every local unstable plaque of

```text
R_-n^-1 v(sigma^-n y)
  [u(sigma^-n y)-u(sigma^-n x)] v(sigma^-n x).
```

A third diagonal/nonlinear correction may cancel this term, but no such
global physical solution or limit bound is presently certified.  This is the
precise nonlinear third-gauge frontier; it replaces the previous vague pair
of unsolved variable-diagonal equations.

## 3. Exact status

```text
STABLE VARIABLE-DIAGONAL GREEN EQUATION:           SOLVED SEPARATELY
UNSTABLE VARIABLE-DIAGONAL GREEN EQUATION:         SOLVED SEPARATELY
LOWER-SHEAR ALL-PLAQUE CLASS H:                    CERTIFIED THEOREM
UPPER-SHEAR ALL-PLAQUE CLASS H:                    CERTIFIED THEOREM
NONCOMMUTATIVE CROSS-TERM IDENTITY:                CERTIFIED
COMBINED ALL-PLAQUE THIRD GAUGE:                   NOT CERTIFIED
SAME REPRESENTATIVE CLASS H PLUS TWISTING:         NOT CERTIFIED
FULL-MASS PHYSICAL PPE:                            NOT CERTIFIED
GATE 1:                                            NOT CERTIFIED
```

The next exact attack is no longer periodic-jet repair.  It is to solve or
bound the displayed renormalised cross term, preferably by a third diagonal
Green correction on the same finite SFT, and then evaluate the two selected
homoclinic wedges in that combined canonical family.

## 4. Technology check

Butler--Park `arXiv:1909.11548v2` still defines class `H` by convergence of
the canonical stable/unstable limits and their Hölder continuity.  The
official arXiv metadata checked on 2026-07-17 exposes no newer theorem that
solves this cohomology-constrained non-fibre-bunched gluing problem.  The
advance here is direct groupoid algebra, not a literature bypass.

## 5. Replay

```bash
PYTHONPATH=deliverables python3 -m py_compile \
  deliverables/cm2_gate1_variable_diagonal_groupoid_frontier_cert.py \
  deliverables/cm2_gate1_variable_diagonal_groupoid_frontier_verifier.py

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate1_variable_diagonal_groupoid_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate1_variable_diagonal_groupoid_frontier_verifier.py \
  --self-test

# Expected exit 2: nonlinear gluing and Gate 1 remain open.
PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate1_variable_diagonal_groupoid_frontier_verifier.py
```
