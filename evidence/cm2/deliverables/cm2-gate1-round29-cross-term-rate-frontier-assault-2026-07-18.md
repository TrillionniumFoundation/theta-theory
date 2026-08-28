# CM2 Gate 1 round 29: nonlinear Green cross-term rate frontier

Date: 2026-07-18 (Asia/Shanghai)  
Parent root: `cm2-twenty-eighth-direct-assault-manifest-2026-07-18.sha256`  
Strict verdict: **the last cross term isolated by the variable-diagonal
all-plaque construction now has two exact sufficient closure routes: a
uniform exponential rate gap and eventual finite-memory cancellation.  A
separate exact countermodel proves that merely shrinking a nonzero shear
amplitude cannot repair an adverse exponential rate.  None of the new
hypotheses has yet been instantiated on the physical billiard registry, and
the selected twisting wedges have not been recomputed in the combined Green
family.  Gate 1 and CM2 therefore remain fail-closed.**

## 1. Frozen same-representative frontier

On the finite clean SFT, the faithful invariant-frame cocycle is diagonal:

```text
A_diag(x)=diag(a_u(x),a_s(x)),
r(x)=a_s(x)/a_u(x),
0<|r(x)|<1.
```

The earlier variable-diagonal leaf solved the lower stable Green equation
and upper unstable Green equation separately.  For the candidate combined
gauge

```text
D=U_v L_u
```

the stable critical coordinate stays clean.  On a local unstable pair
`x,y`, the only remaining combined limit is the renormalised cross term

```text
Z_n
 = R_-n(x)^(-1)
   v(sigma^-n y)
   [u(sigma^-n y)-u(sigma^-n x)]
   v(sigma^-n x).
```

Here `R_-n` is the positive backward diagonal ratio product.  This leaf does
not splice that candidate to the round-25 compact gauge: the compact gauge
has `q>999/1000` and selected twisting, but is already refuted as class `H`
on the frozen connector basic set.

## 2. Uniform rate-gap theorem

Assume one immutable combined physical registry supplies constants

```text
R_-n(x) >= m^n,                    0<m<1,
|u(sigma^-n y)-u(sigma^-n x)|
  <= H omega^n d(x,y)^beta,        0<=omega<m,
|v(sigma^-n x)|,|v(sigma^-n y)| <= V.
```

Then directly

```text
|Z_n|
 <= V^2 H (omega/m)^n d(x,y)^beta.
```

Because `omega/m<1`, the cross term converges uniformly to zero with the
same Hölder exponent.  The combined unstable canonical limit is therefore
the already certified clean upper-Green limit; the stable limit remains the
clean lower-Green limit.  Under these same-registry hypotheses the combined
gauge belongs to Butler--Park class `H`.

This is a sufficient theorem, not a current numerical billiard estimate.
It needs a **lower** bound on the backward ratio product and an independently
typed unstable-plaque decay rate for the lower Green solution.  The old
upper domination `sup|r|<1` is not that lower bound.

The exact rational replay uses

```text
m=3/5, omega=1/3, omega/m=5/9,
V_x=2, V_y=3, delta=7/11,
Z_n=(42/11)(5/9)^n.
```

## 3. Exact finite-memory route

There is a second, rate-free sufficient condition.  If one uniform integer
`L` satisfies

```text
u(sigma^-n y)=u(sigma^-n x)
```

for every local unstable pair and every `n>L`, then `Z_n=0` eventually.  No
comparison between `omega` and `m` is needed.

This is the mechanism in the exact finite-memory full-shift model: the
relevant past/future markers have bounded memory.  The actual billiard's
Sinai-normalised diagonal ratio and Green marker are Hölder functions on the
full coding; exact finite memory has not been proved.  Approximation by a
finite-memory function is insufficient for a canonical-limit certificate.

## 4. Why amplitude-only repair fails

Take the exact scalar countermodel

```text
R_-n=m^n,
du_n=omega^n,
v_x=v_y=epsilon>0,
omega/m>1.
```

Then

```text
Z_n=epsilon^2(omega/m)^n.
```

Every fixed nonzero `epsilon` changes only the prefactor and leaves the bad
successive ratio unchanged.  The replay chooses

```text
m=1/3, omega=1/2, omega/m=3/2,
epsilon=10^-12.
```

Thus shrinking a twisting shear cannot by itself establish convergence.
Setting the upper shear identically to zero would remove this cross term,
but it would also remove the selected upper twisting mechanism and does not
close Gate 1.

## 5. Current physical instantiation

```text
same combined third-gauge rows:                         0
uniform backward-ratio lower rows:                     0
numeric lower-Green unstable-defect rate rows:         0
exact finite-memory rows:                              0
selected wedges recomputed in the combined family:     0
```

Consequently this leaf closes the mathematical compatibility interface but
does not create an actual same-representative class-`H` plus twisting
candidate.  The official statuses remain

```text
combined all-plaque third gauge:                  NOT CERTIFIED
same representative class H plus twisting:       NOT CERTIFIED
full-mass physical projective PPE:                NOT CERTIFIED
Gate 1:                                           NOT CERTIFIED
CM2:                                              NO-GO FOR CLAIM
```

## 6. Shortest Gate-1 continuation

The next constructive certificate must do one of the following on the
actual finite clean SFT:

1. compute a uniform lower ratio `m` and a lower-Green unstable defect rate
   `omega<m`, with Hölder constants on all plaques; or
2. solve an exact finite-memory/cohomological reduction of the physical
   normalised ratio and marker; or
3. build a different nonlinear correction whose groupoid algebra cancels
   `Z_n` identically.

After that, the selected homoclinic loop and all four wedges must be
recomputed in that **same** combined family.  A positive big cell in the
old compact family is not transferable by naming alone.

## 7. Replay

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate1_round29_cross_term_rate_frontier_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate1_round29_cross_term_rate_frontier_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate1_round29_cross_term_rate_frontier_verifier.py \
  --self-test

# Expected live fail-close: exit 2.
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate1_round29_cross_term_rate_frontier_verifier.py
```
