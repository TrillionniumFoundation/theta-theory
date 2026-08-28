# CM2 Round 77: boundary-following tube atlas and actual RN-dominated finite face sum

Date: 2026-07-21  
Strict status: **the entire frozen depth-20 outer ledger is now partitioned by its first failed strict test and covered by 65 explicit interval carrier tubes.  The certified 64 physical R1/R2 faces also receive a finite two-rank upper bound under the actual tagged branch Radon--Nikodym law, using `0<=g_B<=1` rather than an invented geometric depth weight.  A genuine codimension-one carrier atlas, exact numeric RN face weights, ranks at least three, and the official limiting weighted sum remain unproved.  Gate 4 stays `1/7`; Gate 5 stays `10/18`, blocks `0`; the composite state stays `0/5`, `CM2=NO-GO_FOR_CLAIM`.**

## 1. Frozen depth-20 outer taxonomy

The Round-76 tree is replayed without changing its collision classifier.  Its
`670724` terminal leaves remain

```text
R1       45080
R2       23184
Q2      339388
outer   263072
```

The `263072` outer leaves, normalized area `8221/32768`, are now split by the
first failed strict test:

```text
time-one destination faces                         58928  area 3683/65536
time-two competitor discriminants                 166304  area 5197/32768
time-two destination faces                         34624  area 541/16384
time-one outgoing chart or outgoing geometry        3216  area 201/65536
```

There are exactly 19 disjoint reason rows.  Resolving the reason rows to
specific candidate identities gives exactly 65 finite carrier tubes:

```text
16 time-one destination-core face tubes
40 time-two candidate tangency/discriminant tubes
 8 time-two destination-core face tubes
 1 outgoing-chart/outgoing-geometry tube
```

Every outer leaf has at least one carrier and the uncovered count is zero.
The complete leaf-ID union digest is frozen in the JSON proof object.

This is an **interval tube cover**, not yet a proof that every tube contains a
unique smooth physical curve.  Interval dependency can make a strict test
unresolved even when its equality carrier misses the box.  Consequently the
actual codimension-one carrier atlas is deliberately recorded as
`NOT_CERTIFIED`.

## 2. Complement labels

The complement of those frozen outer tubes is exactly the already certified
`407652` strict leaves: `45080` R1, `23184` R2 and `339388` Q2.  Thus every
open dyadic complement cell at depth 20 has a fixed physical label.  This is
a frozen-resolution statement; it neither removes the tube thickness nor
proves the limiting complement.

## 3. Actual finite RN domination

Round 62 proves on every immutable tagged invertible first-return branch

```text
0 <= g_B = d kappa_B / d mu_U <= 1,
a = g_B o H,
```

with no extra coordinate Jacobian in the RN ratio.  The Round-73/75 typed
incidence attaches each physical face to its adjacent tagged path cell, so a
face `f` receives the actual branch charge

```text
kappa_B(U_f) = integral_U_f g_B d mu_U <= mu_U(U_f) <= 1.
```

Applying this domination rowwise to the 32 physical R1 faces and 32 physical
R2 faces gives the first actual-law finite cross-rank bounds:

```text
F9   <= 22138859900062518371942432
F10  <= 512
F13   < 5354429251/250000000000
F16   < 5354429251/250000000000
```

Unlike Round 76's `2^{-time_j}` demonstration, these inequalities use the
actual tagged RN law.  They are upper bounds, not materialized exact face
weights: the 64 numeric density values are still absent.  They also say
nothing about ranks at least three or uniform all-rank summability, so the
official limiting weighted-sum row is not promoted.

## 4. Technology check

The arXiv API was rechecked for `arXiv:2602.07718`, *Certified surface
approximations using the interval Krawczyk test* by Burr, Hauenstein and Lee.
Its generalized Krawczyk test supports certified approximation of nonsquare
analytic varieties and is algorithmically relevant to turning the 65 tubes
into curve carriers.  It is not a moving-billiard theorem and is not used to
promote any current gate.

## 5. Strict frontier

```text
frozen depth-20 outer reason partition                 CERTIFIED 263072/263072
finite interval carrier-tube cover                     CERTIFIED 65 TUBES
frozen complement strict R1/R2/Q2 labels               CERTIFIED 407652 LEAVES
actual codimension-one carrier continuation            NOT CERTIFIED
actual RN-dominated finite R1/R2 face sum               CERTIFIED 64/64
exact numeric RN weights on those incidences            NOT CERTIFIED
rank >= 3 physical atlas and uniform weighted sum        NOT CERTIFIED
Gate 4                                                    1/7
Gate 5                                                   10/18, blocks 0
complete composite gates                                  0/5
CM2                                                       NO-GO_FOR_CLAIM
```

The next shortest route is no longer uniform dyadic refinement.  It is to
run generalized interval-Krawczyk continuation separately on the 40
candidate-discriminant tubes, the 24 destination-face tubes and the outgoing
seam tube, rejecting empty tubes and producing connected physical carriers
for the survivors.  Only after that should the construction lift to rank
three and seek an all-rank RN summability estimate.

