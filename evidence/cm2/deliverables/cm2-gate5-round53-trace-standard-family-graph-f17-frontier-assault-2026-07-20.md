# CM2 Gate 5 Round 53: trace-to-standard-family / graph-current F17 frontier

Date: 2026-07-20  
Scope: Gate 5 at the base parameter `s=0`; for owner occurrence laws, one fixed
insertion time `j` and the registered finite regular range `j<n`.  Distinct
suffix records remain source-rank marked; no domination on a common unmarked
target Borel set is asserted.

## Verdict

Round 53 resolves the measure-typing question behind the proposed Round-42
bridge.  The owner face law is obtained by selecting one transverse rank-zero
root on each parent curve and integrating those root atoms over the parent
law.  It is a transverse trace law, not an unstable proper-standard-family
density.  A foliated-square separator shows that no finite positive
domination from a collision/proper-family law follows: the trace gives a
transverse face mass one, while every non-atomic along-leaf law gives that
face mass zero.

The face-tower frontier is also sharpened.  Even trace-nullity of the
never-return set is insufficient for an exponentially weighted tower.  A
nested exact model has both collision and trace nullity at the limiting set,
but trace survivor mass `1/(p+1)` and hence owner charge
`2^14/(p+1)`.  Its `w_Z`-weighted face sum diverges.

The exact conditional closure region is now frozen.  On one common same-ID
trace law, if

```text
nu_0(Q_p) <= C_tr delta^p,
||2^B||_(L^q(nu_0)) <= M_q,
```

then Hölder gives an exponentially weighted tower precisely when

```text
w delta^(1-1/q) < 1.
```

For `delta=rho` and the fixed Round-42 weight, the critical moment is

```text
q_*=1/(1-log(2rho/(1+rho))/log(rho))
   =2.0008601538040746333039402493451877... .
```

The certified raw `4^-b` rank tail has critical moment `q=2`: an exact
saturating positive law satisfies every current mass/tail upper bound but has
infinite `integral 2^(qB)` for every `q>=2`.  Thus the fixed-weight route needs
new owner grazing sparsity or signed geometric cancellation.  The weaker
`q=3/2` weight remains a valid conditional route only after a quantitative
trace-survivor contraction is proved.

On F17, the physical source graph-current injection is now explicit:

```text
T_(K,B)(phi)=integral K dot grad(phi) dm+B(phi),
||T_(K,B)||_(Lip*) <= ||K||_L1+TV(B).
```

The injection constant is exactly one.  Boundary-trace TV also has suffix
Piola multiplier one.  The bulk vector part does not: a determinant-one
diagonal family forces multiplier at least `L`.  Hence a generic `H(div)` or
`L^1` graph space does not close physical F17; a billiard-specific
directional Piola estimate or quotient/coboundary cancellation remains
necessary.

No complete field is added.  Gate 5 remains `10/18`, complete blocks remain
zero, and CM2 remains `NO-GO`.

## 1. Why the owner face law is not a proper standard family

Round 50 freezes the owner trace as one unique transverse connected-rank-zero
root on each parent `W`.  Abstractly its positive law has the form

```text
nu(A)=integral 1_A(xi(W)) dlambda(W).
```

This is not the same operation as integrating a density along each `W`.
The distinction is exact in the model

```text
X=[0,1]^2,
W_y=[0,1]x{y},
lambda=dy,
Gamma={0}x[0,1],
xi(W_y)=(0,y).
```

The owner-root law is

```text
nu=H^1 restricted to Gamma,
nu(Gamma)=1.
```

The uniform proper-family law is

```text
sigma(A)=integral_0^1 integral_(W_y) 1_A(x,y) dx dy,
sigma(Gamma)=0.
```

More generally, every standard-family density which is non-atomic along
`W_y` gives each singleton intersection `W_y intersect Gamma` zero mass.
Therefore it cannot positively dominate `nu` with a finite constant.

The tube rows make the loss quantitative:

| `epsilon` | `nu([0,epsilon]x[0,1])` | uniform-family mass | ratio |
|---:|---:|---:|---:|
| `1` | `1` | `1` | `1` |
| `1/4` | `1` | `1/4` | `4` |
| `1/64` | `1` | `1/64` | `64` |
| `1/1024` | `1` | `1/1024` | `1024` |

This is a measure-type nonimplication, not an impossibility theorem for the
physical billiard.  It shows that the Round-42 collision/proper-family Growth
and mass recurrence cannot simply be relabelled as a trace recurrence.

The minimal valid replacement is one of:

1. a same-ID trace-to-uniformly-proper-family extension with an explicit loss
   and survivor compatibility;
2. a transverse holonomy/regularisation theorem controlling the trace after
   extension and restriction; or
3. a direct contraction theorem on the owner trace law itself.

The attractive bridge is therefore exact but conditional.  It requires
positive maps `E` (trace extension) and `Tr` (trace recovery) which preserve
the owner IDs, have norm at most one, put `E nu` in the Round-42 proper-family
class, and satisfy both

```text
Tr composed E = Id                 on the owner trace laws,
K_trace = Tr composed K_proper composed E
                                    for the killed-block survivor operators.
```

The recovery identity explicitly excludes the vacuous choice `E=Tr=0`.
Under these hypotheses,

```text
kappa_trace<=rho<2rho/(1+rho).
```

That would clear the fixed recurrence threshold.  No such `E/Tr` pair is
currently installed; the separator above explains why it cannot be the
identity or a finite positive domination between the two physical laws.

## 2. Trace-nullity is necessary but not an exponential tower theorem

Let

```text
rho=(111718729/111718750)^9148,
w_Z=(1+rho^-1)/2.
```

On `X=[0,1]^2` with collision volume `mu=dx dy` and trace
`nu=H^1|Gamma`, set

```text
Gamma={0}x[0,1],
Q_p=[0,rho^p]x[0,1/(p+1)].
```

Then

```text
mu(Q_p)=rho^p/(p+1)<=rho^p,
nu(Q_p)=1/(p+1),
intersection_p Q_p={(0,0)},
mu(intersection Q_p)=nu(intersection Q_p)=0.
```

Put `B=14` on the face and retain one owner event.  The face charge is

```text
b_p=2^14/(p+1).
```

The ordinary forcing majorant `z_p=m_p=rho^p` is summable at `w_Z`, since

```text
w_Z rho=(1+rho)/2<1.
```

But

```text
sum_p w_Z^p b_p=infinity
```

because its terms do not even tend to zero.  Equivalently, for every fixed
`kappa<1` and finite `A,C`,

```text
b_(p+1) <= kappa b_p+A rho^p+C rho^p
```

eventually fails.  Thus the statement

```text
nu(intersection_p Q_p)=0
```

must not be promoted to an exponential trace-return moment.  The missing
input is quantitative, not merely null-set theoretic.

## 3. Sharp conditional trace-survivor region

Assume a future theorem supplies one common same-ID source trace law `nu_0`,
nested survivor restrictions

```text
nu_p=1_(Q_p) nu_0,
```

and a retained mark `g=2^B` satisfying

```text
nu_0(Q_p)<=C_tr delta^p,
||g||_(L^q(nu_0))<=M_q,
q>1.
```

Hölder then gives

```text
b_p=integral_(Q_p)g dnu_0
   <=M_q C_tr^(1-1/q) delta^(p(1-1/q)).
```

Therefore

```text
sum_p w^p b_p<infinity
```

whenever, and at the level of this information exactly when,

```text
w delta^(1-1/q)<1.
```

For the fixed Round-42 weight, write

```text
kappa_*=1/w_Z=2rho/(1+rho)
       =0.9991402160751072492560129714996435... .
```

If `delta=rho`, the threshold is the `q_*` displayed in the verdict.  Two
exact checkpoints are:

```text
q=2 fails:
  kappa_*<sqrt(rho)
  iff (1-sqrt(rho))^2>0;
  after squaring this is also iff (1-rho)^2>0;

q=3 succeeds conditionally:
  rho^(2/3)<kappa_* iff (1+rho)^3<8rho.
```

For `q=3/2`, the fixed-weight condition is

```text
delta<kappa_*^3
     =0.9974228652749375667196429917741988... .
```

Taking `delta=rho=0.9982819093369480988641178885301253...` misses it.
However, the weaker conditional choice

```text
w_face=(1+rho^(-1/3))/2
      =1.0002866768644751831264877673779233...,
w_face rho^(1/3)
      =(1+rho^(1/3))/2
      =0.9997134874085874944662437634034334...<1
```

would work if the same-ID trace contraction at rate `rho` were actually
proved.  It is not currently proved, so no weak resolvent is promoted.

The strict inequality in the criterion is sharp at the level of these two
hypotheses.  On disjoint shells `S_r`, take

```text
nu_0(S_r)=(1-delta)delta^r,
Q_p=disjoint_union_(r>=p)S_r,
g|S_r=delta^(-r/q)/(r+1)^a,
a=(q+1)/(2q).
```

Then `nu_0(Q_p)=delta^p`, while

```text
integral g^q dnu_0
  is comparable to sum_r (r+1)^(-(q+1)/2)<infinity,

b_p is comparable to
  delta^(p(1-1/q))/(p+1)^a.
```

At the critical equality `w delta^(1-1/q)=1`, the weighted tower is
comparable to `sum_p (p+1)^(-a)`, which diverges because
`1/q<a<1`.  The retyping

```text
g_tilde=2^max(14,ceil(log2 g))
```

has `g<=g_tilde<2g` on every sufficiently large shell; the
finitely many initial shells are fixed at rank `14` and do not affect either
series.  Hence the separator retains the same asymptotics with an integer
incidence rank `B>=14`.

## 4. The raw `4^-b` tail cannot supply the fixed-weight moment

Let

```text
C_tail=9158592/6875,
s=4 C_tail 4^-14=143103/7208960000.
```

On atoms `B=14+k`, put

```text
m_k=s*(3/4)*4^-k,  k>=0.
```

Then the total mass `s` is far below the certified raw coarea mass upper
`8064/5`, and for every `k>=0`,

```text
m{B>14+k}=C_tail 4^(-(14+k)).
```

Thus the current tail estimate is saturated exactly.  The successive terms
in the `q` moment have ratio

```text
2^q/4.
```

Consequently

```text
integral 2^(qB) dm < infinity  iff q<2,
integral 2^(qB) dm = infinity  for q>=2.
```

At `q=2`, every atom contributes the same positive amount
`3 C_tail`.  The owner rule may be taken to be the identity, so owner
deduplication by itself does not improve this example.

This does not claim that the actual physical owner law saturates the upper
tail.  It proves that neither `q>q_*` nor even endpoint `q=2` follows from the
certified raw tail.  The fixed-weight route needs an extra owner-face grazing
sparsity theorem, paired-image cancellation, or a different signed
recurrence.

## 5. Physical graph-current injection and the remaining F17 loss

For a vector current `K` and finite signed boundary trace `B`, define

```text
T_(K,B)(phi)=integral_U K dot grad(phi) dm+B(phi),
||phi||_Lip=max(||phi||_infinity,||grad phi||_infinity).
```

Directly,

```text
||T_(K,B)||_(Lip*)<=||K||_L1+TV(B).
```

This installs both physical source interfaces with constant one:

```text
bulk Eulerian injection:   1,
two-trace injection:       1.
```

For an area-preserving regular suffix `S`,

```text
S_*T_(K,B)=T_(Piola_S K,S_*B),
Piola_S K(Sx)=DS(x)K(x).
```

The boundary part satisfies

```text
TV(S_*B)=TV(B),
```

which is the same geometric multiplier-one mechanism behind the certified
F16 flux transport.  The bulk part satisfies only

```text
||Piola_S K||_L1=integral_U |DS(x)K(x)|dm(x).
```

The exact determinant-one separator is

```text
U_L=[0,1/L]x[0,1],
V_L=[0,1]x[0,1/L],
S_L=diag(L,L^-1),
K=e_1.
```

Then

```text
||K||_(L1(U_L))=1/L,
Piola_S K=L e_1,
||Piola_S K||_(L1(V_L))=1.
```

The unit physical test `phi(y)=y_1` gives target pairing one.  Hence any
common physical graph-current suffix multiplier allowed by these hypotheses
is at least `L`, and no finite uniform constant follows from
`det DS=1` alone.

This separator is logical: it does not assert that every diagonal map occurs
as an actual billiard suffix.  It proves that the present generic inputs
(area preservation, Piola flux naturality and source `L^1` current charge)
cannot yield the required

```text
C_dyn<7961063/7800000.
```

A valid F17 theorem still needs one common anisotropic current norm with:

1. bounded injection of both Eulerian components of `K`;
2. bounded injection of all physical two-trace currents;
3. bounded inclusion of the required CM2 observable algebra; and
4. a billiard-specific directional Piola or quotient/coboundary estimate
   below the numerical suffix threshold.

## 6. Typed conditional bridge to Gate 3

The Gate-3 common free graph-current carrier has `41,508` fixed slots.  Its
source records and the present representation

```text
T_(K,B)=-div(K)+B
```

are compatible at the level of bulk/trace typing.  Therefore a future
physical vector-current F17 space could supply part of the missing maps

```text
R_s:B2_physical->X2_hat,
Q_s:X0_hat->B0_physical.
```

This is only a conditional bridge.  The following remain independent:

1. same physical branch/component and owner IDs for every moving Gate-3 slot;
2. quotient assembly of artificial/duplicate traces before absolute values;
3. moving-test convergence on the component-indexed atlas;
4. the physical observable inclusion and F17 suffix bound;
5. all 18 operator fields on one common recovered block; and
6. cemetery plus the growing-depth no-`|s|^-1` current tail.

Thus neither the physical `Q_s/R_s` lift/quotient nor branch-record `MT_DQ`
is promoted.

## 7. Latest-technology audit

Official sources were rechecked on 2026-07-20:

```text
Demers--Liverani survey / stable-curve norms: 2606.10155v1
Demers--Liverani complex cones / sequential CLT: 2502.07765v2
```

The official source archive hashes are respectively

```text
d568ad1351593e1d33d7855079583dd28d3c1ff6a26f673ca01ebc2784c132a6
a703115d1c2b943b82303a9f9f5d728ff819f2fa86365e663c8c2419ff02f60f
```

These works provide stable-curve/projective cone mechanisms and sequential
collision-volume transfer laws.  They do not state a positive injection of
the singular transverse owner-root law into a uniformly proper family, nor
an `H(div)`-type physical vector-current F17 injection with the required
numeric suffix constant.  No direct field upgrade was found.

## 8. Strict status and shortest continuation

Certified this round:

```text
owner trace versus proper-family measure-type separator: CERTIFIED
trace-nullity without exponential tower separator:       CERTIFIED
sharp conditional trace Holder/weight region:             CERTIFIED
raw 4^-b q=2 critical moment separator:                   CERTIFIED
physical source graph-current injection constant 1:       CERTIFIED
boundary-trace suffix TV multiplier 1:                    CERTIFIED
bulk Piola uniform-multiplier separator:                  CERTIFIED
Gate3 graph-current typed conditional bridge:             CERTIFIED_CONDITIONAL_ONLY
```

Not certified:

```text
trace-to-proper-standard-family injection: NOT CERTIFIED
quantitative trace-survivor contraction:   NOT CERTIFIED
fixed-weight q>q_* owner moment:           NOT CERTIFIED
unconditional weak face resolvent:         NOT CERTIFIED
aggregate owner-Z_B / face tower:          NOT CERTIFIED
physical bulk F17 suffix constant:         NOT CERTIFIED
complete all-face F10 / strong F13:        NOT CERTIFIED
F14/F15/F17/F18 / strong cemetery:         NOT CERTIFIED
Gate3 physical Q_s/R_s and MT_DQ:          NOT CERTIFIED
Gate-5 maturity / complete blocks:         10/18 / 0
complete composite gates:                  0/5
CM2:                                       NO-GO_FOR_CLAIM
```

The shortest valid continuation is now:

1. prove a quantitative transverse trace-survivor theorem on the same owner
   IDs, or construct a trace extension to uniformly proper families with an
   explicit loss and survivor compatibility;
2. pair it either with new owner grazing sparsity past `q_*`, a signed
   recurrence sharper than Hölder, or the conditional weaker `w_face` route;
3. prove a billiard-specific directional Piola/coboundary bound in one common
   physical graph-current anisotropic space;
4. only then promote the face tower, physical F17, complete F10, strong F13,
   F14/F15/F18 and the Gate-3 physical lift/quotient and `MT_DQ`.

## 9. Validation

Artifacts:

- `cm2_gate5_round53_trace_standard_family_graph_f17_frontier_cert.py`;
- `cm2_gate5_round53_trace_standard_family_graph_f17_frontier_verifier.py`;
- `cm2-gate5-round53-trace-standard-family-graph-f17-frontier-manifest-2026-07-20.json`;
- this report and its SHA ledger.

The suite hash-pins eight dependencies, semantically checks the Round-52
transferred `4^-b` tail and explicit `q=3/2` scope plus the Gate-3 `41,508`
fixed slots, and independently recomputes the
foliated trace rows, the trace-null tower, the exact fixed-weight inequalities,
the saturated rank law, the graph-current diagonal rows and all nonpromotion
boundaries.

```text
syntax:                    2/2 PASS
strict JSON:               duplicate keys and NaN/Infinity rejected
deterministic replay:      PASS
hostile mutations:         109/109 rejected
default cert/verifier:     fail closed with exit 2
Gate-5 maturity:           10/18
complete blocks:           0
CM2:                       NO-GO_FOR_CLAIM
```
