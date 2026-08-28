# CM2 Gate 2 after the physical full-cross: return-base and quotient audit

Date: 2026-07-15 (Asia/Shanghai)  
Scope: Gate 2 continuation using the certified directed QNL-to-connector
full-cross; frozen v51/v52 and the shared research log are not edited  
Verdict: **an actual positive-SRB two-dimensional return base is now
instantiated, but its reverse kernel is deterministic; the required stable
quotient and physical Gate 2 remain OPEN / NO-GO**

## 1. Executive result

The Gate-1 input has genuinely advanced.  The source rectangle

```text
S_A={|a-t0|<=10^-20, |b|<=2.1*10^-18}
```

is propagated through one immutable 24-collision word and full-crosses the
connector rectangle.  The inherited reverse strip and both endpoint
transition derivatives are also certified.  Four-face full-cross is no
longer a missing Gate-2 premise.

This permits a new physical construction which was unavailable in the
previous audit: `S_A` itself is a positive collision-SRB set and can be used
as a Poincare return base.  In the canonical QNL eigenchart

```text
s=a+b,        p=k_A(a-b),        k_A>0,
```

the collision law is constant.  Its exact physical mass is

```text
mu(S_A)=(105 k_A/(13 pi))*10^-38
       =1.7429936716407675...*10^-37.                       (1.1)
```

Poincare recurrence therefore gives an actual full-mass first-return map on
`S_A`, and Kac gives

```text
E_{S_A} R_A=1/mu(S_A)
 =5.737255483312511...*10^36.                              (1.2)
```

This does **not** close the requested quotient.  The billiard and its
two-dimensional first-return map are invertible.  Consequently every point
has one past return almost everywhere and the exact reverse kernel is a
Dirac kernel.  Its projective law remains atomic and its two-copy Riesz
energy has coefficient one.  The countable non-invertible random kernel

```text
p_a(x)=rho(h_a x)|h_a'(x)|/rho(x)
```

appears only after collapsing genuine stable leaves in a stable-saturated
Young/Markov rectangle.  The affine full-cross rectangle has not been
certified to be such a product rectangle, and no full-image stable quotient
partition is available.

The 24-collision word is also certified **not** to be a return to `S_A`: its
target is separated from `S_A` by a gray collision-angle gap greater than

```text
0.0013055742.
```

It is an actual transition branch, not the first member of a return
alphabet.  A closed dwell/shadowing return remains necessary to obtain even
one explicit q-anchored return strip.  Beyond that finite Gate-1 task, Gate 2
still needs a stable-saturated full-mass base, its complete return partition,
and a tail stronger than the Kac bound.

## 2. Exact use of the new full-cross certificate

The new certified layers are

| object | status |
|---|---:|
| actual QNL and connector invariant graphs | certified |
| true transverse common vertex | certified |
| directed 24-collision four-face full-cross | certified |
| reverse inherited transition strip | certified |
| forward/reverse endpoint transition derivatives | certified |
| closed connector dwell/shadowing return | open |
| transported twisting on a closed loop | open |

The physical source coordinates satisfy

```text
(a,b) -> (s,p)=(a+b,k_A(a-b)),
|det d(s,p)/d(a,b)|=2k_A.                                  (2.1)
```

The whole source rectangle has the fixed word and the strict first-hit
margins from the Gate-1 certificate.  It is far from grazing:

```text
sup_{S_A}|p| < 9.465*10^-9.
```

Thus it is a legitimate open collision-phase set, not a Cantor conditional
or a tangent-only tube.

The target rectangle uses connector eigen-coordinates `(x,u)`.  Converting
both source and target to the gray collision angle gives the strict enclosure

```text
dist_angle(S_A,R_B)>0.0013055742159.                        (2.2)
```

Consequently no point of the certified source returns to the source at the
end of this 24-collision word.  The word may be used as an `A -> B`
transition in a future return construction, but it is not an inverse branch
`h_a:S_A -> S_A`.

## 3. Exact collision-SRB mass of the source rectangle

There is one gray and one white solid obstacle per torus cell, with radii

```text
R_G=9/25,        R_W=4/25.
```

Their total boundary length is

```text
|partial Q|=2 pi(R_G+R_W)=26 pi/25.
```

In arclength--momentum coordinates `(s,p=sin phi)`, the normalized collision
law is

```text
dmu=(2|partial Q|)^-1 ds dp = 25/(52 pi) ds dp.             (3.1)
```

Combining (2.1), (3.1), and the two source half-widths gives

```text
mu(S_A)
 =25/(52pi) * 2k_A * (2*10^-20)(2*2.1*10^-18)
 =(105k_A/(13pi))*10^-38.                                  (3.2)
```

The exact QNL slope is

```text
k_A=sqrt(gamma_A/beta_A),
beta_A=(859-550sqrt(2))/100,
gamma_A=625(25-4sqrt(2))/324,
```

and the Arb certificate gives

```text
k_A=6.7795323317182630386...,
1.7*10^-37 < mu(S_A) < 1.8*10^-37.                         (3.3)
```

This is the first actual q-anchored SRB mass in the Gate-2 chain.

## 4. The actual two-dimensional first-return alphabet

Let

```text
R_A(z)=min{n>=1:T^n z in S_A},
F_A(z)=T^{R_A(z)}z.
```

Since the finite-horizon billiard is ergodic and `mu(S_A)>0`, Poincare
recurrence gives `R_A<infinity` for normalized `mu|S_A`-almost every point.
An actual countable smooth alphabet can be defined without truncation:

```text
C_A = disjoint union over n>=1 of connected components of
      {R_A=n} cut by every collision singularity, lift word,
       homogeneity word, and genuine component boundary.                  (4.1)
```

For `C in C_A`, put

```text
F_C=T^{R_C}|_C:C -> F_C(C),
h_C=F_C^-1:F_C(C) -> C.                                   (4.2)
```

This is an actual full-mass branch registry at the definition/theorem level.
It is not an executable word list: no component of (4.1) has yet been
enumerated, and the certified 24-word is excluded by (2.2).

More importantly, (4.1) is not the desired full-branch alphabet.  The image
`F_C(C)` is generally a proper subset of `S_A`, rather than all of a
one-dimensional reference interval.

## 5. Exact obstruction: the two-dimensional reverse kernel is Dirac

The first return of an invertible measure-preserving transformation is
invertible almost everywhere.  Its inverse is the previous return.  Thus the
sets `F_C(C)` partition `S_A` modulo zero and exactly one branch is available
at almost every target point.

Because (3.1) is constant and every collision map preserves `ds wedge dp`,

```text
|det Dh_C|=1
```

in the same base chart.  The physical branch formula becomes

```text
p_C(z)=1_{F_C(C)}(z)|det Dh_C(z)|,
sum_C p_C(z)=1,                                             (5.1)
```

with exactly one nonzero summand.  Equivalently,

```text
K_2D(z,.)=delta_{F_A^-1 z}.                                (5.2)
```

Let `V_r(u,v)=max(r,|pi(u)-pi(v)|)^(-alpha)`.  Starting two
conditionally independent copies from the same state still gives the same
deterministic child, so

```text
(K_2D tensor K_2D)V_r(u,u)=r^-alpha.                        (5.3)
```

No inequality

```text
(K_2D tensor K_2D)V_r <= kappa V_r+C_0,       kappa<1,
```

can hold uniformly in `r`: at `u=v`, (5.3) would imply
`(1-kappa)r^-alpha<=C_0`.

This is a strict new obstruction, not a missing numerical constant.  A
positive two-dimensional return set does not generate the random inverse
branches required by projective Frostman regularisation.

## 6. The first genuinely missing quotient object

There is now an actual unstable reference **curve candidate** inside the
source rectangle:

```text
I_A={gamma_A(t)=(t,h_A(t)):
     |t-t0|<=10^-20}.                                      (6.1)
```

The certified bound `|h_A(t)|<1.95*10^-18<2.1*10^-18` places it strictly
inside `S_A`.

What is absent is a stable-saturated product set `Lambda_A subset S_A` and a
stable holonomy

```text
pi^s:Lambda_A -> I_A                                      (6.2)
```

for which a countable family of return strips maps across `Lambda_A` and
induces onto inverse branches

```text
h_a:I_A -> I_a.                                            (6.3)
```

The affine transverse coordinate `b` is an eigen-coordinate, not a certified
field of actual stable plaques, and cannot be declared to be (6.2).

Only after (6.2)--(6.3) exist does the quotient SRB density `rho` become a
defined one-dimensional object and the physical kernel become

```text
p_a(x)=rho(h_a x)|h_a'(x)|/rho(x).                          (6.4)
```

The directed full-cross supplies a future gate strip for such a quotient.
It does not construct the stable saturation, full return partition, or onto
property.

## 7. What a closed dwell would and would not close

A validated connector dwell/shadowing word joining the incoming and
involuted outgoing strips would give a closed q-anchored return strip and its
transported derivative.  This would be a substantial first branch and would
also unlock the twisting check.

It would not by itself make (6.3) full mass.  One finite closed strip is a
clean subsystem and may have negative relative pressure.  Gate 2 would still
need either

1. an anchored Young/Gibbs inducing scheme whose complete countable return
   partition contains this strip; or
2. a proven transfer from a standard full-mass billiard Young tower to the
   declared q-anchored reference interval, preserving the cocycle and
   physical weights.

No such identification is currently certified.

## 8. The only presently certified return tail

Kac gives the exact mean (1.2).  Markov's inequality gives, for the normalized
base law,

```text
mu_{S_A}{R_A>L}
 <= min{1,1/(mu(S_A)L)}.                                   (8.1)
```

This is a valid full-mass tail with no truncation or survivor
renormalisation.  It is also far too weak for the prescribed logarithmic
depth.  With `L=C log(1/r)`, its decaying part is only

```text
O(1/log(1/r)),
```

which is not `O(r^theta)` for any `theta>0`.

The actual billiard return to a suitable Young base is expected to have an
exponential tail, but neither exponential mixing nor the abstract existence
of a tower identifies that tail with this tiny source rectangle and the
certified transition labels.  The v52 return/grazing/context moments remain
conditional at this q-anchored base.

## 9. Projective and same-carrier audit after full-cross

The new endpoint matrices `D H_AB` and `D H_BA` are actual directed
transition derivatives.  They can now be inserted into a branch matrix
record with their correct endpoint trivializations.

They are not yet a stationary projective kernel:

- `H_AB` has target `R_B`, not the source base;
- `H_BA` starts at the involuted strip;
- no finite closed word joins the two endpoints;
- the complete full-mass stable quotient alphabet is absent.

Likewise, these transition matrices do not instantiate the PPE endpoint
covectors `dX,dY` on one retained carrier.  The same-carrier endpoint wedge,
denominator bound, actual stopped antichain, and exhaustive amplitude
registry remain open.

## 10. Updated dependency graph

```text
actual true-graph vertex                              CERTIFIED
directed/reverse positive-width transition strips    CERTIFIED
actual transition endpoint derivatives               CERTIFIED
positive-SRB 2D source base and exact mass            CERTIFIED
full-mass 2D Poincare return                          PROVED
2D reverse kernel                                     DETERMINISTIC / BLOCKED
closed explicit q-return branch                       NOT CERTIFIED
stable-saturated q-anchored Young rectangle           NOT CERTIFIED
onto countable stable quotient alphabet               NOT CERTIFIED
rho,h_a,p_a and projective maps on that quotient      NOT INSTANTIATED
exponential return/grazing/context tail               NOT INSTANTIATED
stopped-parent PPE and same-carrier endpoint          NOT CERTIFIED
```

Thus the earliest obstruction is no longer four-face geometry.  It is the
construction of the non-invertible stable quotient on a full-mass product
base.  The missing closed dwell is the first finite branch-level task inside
that larger construction.

## 11. Minimal next certificate

1. Finish the finite closed dwell/shadowing return and certify the resulting
   first q-anchored return strip and matrix.
2. Construct actual stable plaques across a declared subrectangle of `S_A`,
   record `pi^s`, and verify that the closed strip is full-image after
   quotient.
3. Anchor a complete Young return partition to this rectangle and enumerate
   a growing branch core without renormalising it.
4. Replace the Kac-only bound (8.1) by a certified exponential
   return--grazing--context tail on the same branch labels.
5. Apply the previously proved unnormalised-core energy theorem and certify
   the off-diagonal projective near-collision statistic.

## 12. Reproduction

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate2_post_full_cross_return_base_cert.py \
  deliverables/cm2_gate2_post_full_cross_manifest_verifier.py
/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate2_post_full_cross_return_base_cert.py
python3 deliverables/cm2_gate2_post_full_cross_manifest_verifier.py --self-test
python3 deliverables/cm2_gate2_post_full_cross_manifest_verifier.py
sha256sum -c \
  deliverables/cm2-gate2-post-full-cross-manifest-2026-07-15.sha256
sha256sum -c deliverables/cm2-v52-manifest.sha256
```

The positive arithmetic/geometry certificate exits zero.  The live physical
manifest exits two by design.  Final verdict:

```text
Q_ANCHORED_2D_RETURN_BASE: CERTIFIED
Q_ANCHORED_STABLE_QUOTIENT: NOT CERTIFIED
EXECUTABLE_RETURN_BRANCH: NOT CERTIFIED
PHYSICAL_GATE2: OPEN / NO-GO
```
