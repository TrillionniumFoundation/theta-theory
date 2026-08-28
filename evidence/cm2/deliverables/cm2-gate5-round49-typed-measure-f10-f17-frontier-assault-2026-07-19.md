# CM2 Gate 5 Round-49 typed-measure F10/F17 frontier assault

Date: 2026-07-19  
Strict verdict: **a fixed-record typed direct-sum measure kernel is now
formalized, but the face currents are singular with respect to collision-SRB
D1.  One-step coarea moments do not imply return-depth integrability, and the
crude suffix-product route fails even under the best current exponential
tail.  Gate-5 maturity remains `10/18`; complete block count remains `0`.**

## 1. What can be joined without changing measure type

For each fixed `s=0`, finite `n`, and fixed regular arbitrary-`R_n`
restriction record, use the common token

```text
(component-id,n,path-key,parent-W-id,time-j,face-kind,
 primitive-key,connected-rank-0,trace-side).
```

The following four measure-valued objects can be stored on that record:

```text
K_mu:    collision-SRB volume restriction carrying c_D1,n;
K_occ:   Round-39 positive occurrence coarea restrictions;
K_core:  Round-47 finite signed core/two-trace restrictions;
K_7:     Round-48 regular seven-boundary face-germ restrictions.
```

Their absolute sum

```text
Lambda_y=K_mu+sum_e |K_occ|+sum_c |K_core|+sum_f |K_7|
```

is a valid dominating measure for that one record, so all four components
have Radon--Nikodym representatives relative to `Lambda_y`.  This is a typed
direct sum, not a proof that the four original physical measures coincide.

The collision-SRB parent kernel, 64 occurrence seeds/128 traces, and the
finite-path two-trace sublayer are already materialized.  The seven-face
extension is only recordwise on an individually registered nonempty regular
germ.  Round 48 froze candidate slots and seed types, but not a global
nonempty-component enumeration, cross-record owner deduplication, or a
jointly measurable all-record kernel.

## 2. Exact Lebesgue-decomposition obstruction

The measure types are:

```text
D1:          two-dimensional collision-SRB volume density;
occurrence:  one-dimensional positive coarea curve measure;
core/trace:  one-dimensional finite signed boundary measure;
seven-face:  density relative to a one-dimensional regular face measure.
```

For a smooth regular physical face `Gamma`,

```text
mu_s(Gamma)=0,
nu_face(Gamma)>0
```

on every nonempty moving germ.  Thus, even after introducing `Lambda`,

```text
d(c_D1*mu_s)/dLambda=0
```

on its face sector.  No finite constant can make a nonzero face current
dominated by `c_D1*mu_s`.

The certificate freezes the exact local model

```text
mu=dx*dy on [0,1]^2,
Gamma={x=1/2},
nu=H^1|Gamma,
A_epsilon={|x-1/2|<epsilon}.
```

Then `nu(A_epsilon)=1`, whereas `mu(A_epsilon)=2 epsilon`; the ratio diverges
as `epsilon` tends to zero.  A common collision normalization `Z_N^-1`
multiplies both sides but cannot change this singularity.

Consequently the Round-48 formal coefficient

```text
13571096530812446357 / 14837273637760415744 < 1
```

remains certified arithmetic, not a physical D1-dominated F10 theorem.

## 3. Return-depth weighted coarea is a separate theorem

The certified one-step occurrence data remain:

```text
positive coarea mass                         < 8064/5;
integral 2^(3B/2) dm                         < 46506443753721/13750;
bidirectional raw-F10 L^(3/2) moment sum     < 272016189515514129/13750.
```

They do not control the unbounded return-depth tower.  The exact
countermodel is

```text
b_n=1/(n(n+1)),
B=14 identically.
```

It satisfies

```text
sum_n b_n=1,
integral 2^(3B/2) db=2^21<infinity,
sum_n n*b_n=sum_n 1/(n+1)=infinity.
```

Thus even bounded rank plus finite raw coarea mass does not imply the needed
return-depth face-current moment.  Kac's formula for collision-SRB cannot be
transferred to a singular coarea/trace measure without a new bridge.

The missing input is one of:

1. a direct face-tower moment on the same restriction IDs; or
2. a trace/boundary-`Z_B` theorem plus a summable insertion-time aggregate
   resolvent.

## 4. Exact F17 suffix-product obstruction

At source time the complete bulk-plus-trace coefficient remains

```text
X/D1       = 25/151,
F13/D1     = 3816937/47112000,
total/D1   = 11616937/47112000 < 1/4,
quarter slack = 161063/47112000.
```

The crude nonempty-suffix estimate pays at least

```text
D_min=150*2^14=2457600
```

per suffix collision.  With

```text
r=111718729/111718750,
```

one already has

```text
D_min*r=5491198967808/2234375 > 1.
```

Take a geometric return law

```text
P(N=n)=(1-r)r^(n-1),  B_i=14.
```

Then `c_D1=151*2^14*N`, so all polynomial D1 moments are finite, but the first
insertion suffix moment has ratio `D_min*r>1` and diverges.  This works at the
best possible block interpretation `N_open=1`; a larger `N_open` only weakens
the per-collision decay.

Hence the Round-35 D1 `L^(6/5)` moment and exponential tail cannot supply the
joint insertion/suffix product moment.

A future dynamic-test theorem with suffix multiplier `C_dyn` has the exact
targets

```text
C_dyn < 7961063/7800000    => total source ratio remains below 1/4;
C_dyn < 43295063/7800000   => total source ratio remains below 1.
```

No such F17 theorem is currently installed.

## 5. Measure-correct conditional boundary-Z_B alternative

There is a typed alternative to D1 domination.  For one registered face
meeting each canonical parent leaf at most once, the existing conditional
density ratio `2000/1999` and normalized F8 wedge `>1/5` give the conditional
single-atom TV multiplier

```text
5*(2000/1999)=10000/1999.
```

Define

```text
Z(G)   = integral |W|^-1 d lambda(W),
Z_B(G) = integral 2^B(W intersect Gamma) |W|^-1 d lambda(W).
```

After owner deduplication, the formal recordwise target is

```text
Q_F10(G)
 < (276024578258731962000000/95909140889781247)*Z(G)
   + (1030000/1999)*Z_B(G).
```

The first coefficient contains the Round-48 worst W-source seven-boundary
cost and all 192 rank-zero C24 core traces.  The second carries the
rank-dependent bidirectional occurrence cost.

This is only an atom/TV trace lemma.  A complete F10 theorem still requires
the same-ID `Z_B` trace bound, insertion-time aggregate `Z_B` resolvent,
leaf-density derivative terms, global owner deduplication, corner policy and
cemetery domination.

## 6. Strict maturity and next interface

The new certified sublayers are:

```text
typed fixed-record direct-sum measure kernel;
Lebesgue-decomposition obstruction to D1 domination;
exact return-depth nonimplication;
exact F17 suffix-product nonimplication;
conditional boundary-Z_B replacement interface.
```

None is a completed new Gate-5 field.  Therefore:

```text
same-measure all-record F10:          NOT CERTIFIED
return-depth face integrability:      NOT CERTIFIED
complete all-face F10:                NOT CERTIFIED
F17 dynamic test:                     NOT CERTIFIED
strong F13:                           NOT CERTIFIED
cemetery:                             NOT CERTIFIED
Gate-5 maturity:                      10/18
complete 18-field blocks:             0
complete composite gates:             0/5
CM2:                                  NO-GO
```

The shortest valid continuation is to build a common owner-aware
trace-`Z_B` kernel and insertion-time aggregate resolvent.  In parallel, F17
must be attacked through a genuinely dynamic/anisotropic test estimate;
further scalar suffix-product moment estimates cannot close the gap.
