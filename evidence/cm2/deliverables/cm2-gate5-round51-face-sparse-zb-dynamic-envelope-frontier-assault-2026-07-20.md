# CM2 Round 51 Gate-5 face-local `Z_B` / dynamic-envelope assault

Date: 2026-07-20  
Scope: Gate 5 only; base parameter `s=0`; all finite regular suffix records,
with the unbounded arbitrary-`R_n` owner-depth join kept fail-closed.

## Verdict

Round 51 isolates the only full-rank one-step face and proves that its raw
physical seed measure is integrable at the required exponent `theta=1`.
This is a genuine refinement of Round 50: the moving-occurrence seed itself
does **not** cause the divergent generic Growth majorant.

The result does not close the owner-`Z_B` recurrence.  The certified
`4^{-b}` rank tail lives on the raw endpoint-coarea law, whereas the desired
recurrence lives on the arbitrary-`R_n` owner-leaf law.  No same-ID uniform
transfer between those measures is available.  Moreover, exact scalar
`+/-` cancellation and one owned event per parent are jointly insufficient
for a `C^1` current bound.

On the F17 side, one common suffix-envelope test space is constructed.  Every
finite regular suffix pullback has operator norm at most one on this space,
so its algebraic multiplier is exactly `C_dyn=1`.  The missing point is now
strictly the physical compatibility map: the required physical `C^1/CM2`
tests are not known to embed in that envelope with any finite constant.

Consequently:

```text
raw moving-occurrence theta=1 seed L1:       CERTIFIED
same-ID arbitrary-R_n owner-Z_B recurrence: NOT CERTIFIED
common algebraic suffix envelope C_dyn=1:   CERTIFIED
physical branch-uniform F17 test embedding: NOT CERTIFIED
strong F13 / complete F10 / F17:            NOT CERTIFIED
Gate-5 maturity:                            10/18
complete 18-field blocks:                   0
CM2:                                        NO-GO
```

## 1. Five-face rank localization

The five physical face kinds separate as follows.

| physical face | one-step current | rank role |
|---|---|---|
| source core clipping | zero in the fixed common source coordinates | none |
| intermediate core avoidance preimage | affine C24 core-edge flux | rank-zero central seed; fixed ordinary-`Z` cost |
| terminal core preimage | affine C24 core-edge flux | rank-zero central seed; fixed ordinary-`Z` cost |
| collision singularity / owner change | seven frozen boundary-kind seeds | fixed tangency/corner costs; five zero-speed types vanish |
| moving occurrence | `sigma*(tau_hit-tau_miss)` | bidirectional raw cost `<103*2^B` |

Thus the moving-occurrence face is the only one-step physical face that
requires the full rank weight.  This localization is only an insertion
ledger.  It does not remove the separate suffix bulk/tangential derivative
problem.

Artificial chart and homogeneity faces remain assembled before absolute
values and are not reintroduced as physical events.

## 2. Full `theta=1` is finite on the raw occurrence seed law

Round 39 supplies, on the unnormalized positive endpoint-coarea seed law
`m_occ`,

```text
m_occ(total) < 8064/5,
m_occ{B>b} <= (9158592/6875)*4^(-b),  b>=14.
```

For integer `B>=14`,

```text
2^B = 2^14 + sum_(b=14)^(B-1) 2^b,
sum_(b>=14) 2^b 4^(-b) = 2^(-13).
```

Therefore

```text
integral 2^B dm_occ
 < 2^14*(8064/5) + (9158592/6875)*2^(-13)
 = 23253221519103/880000.
```

Using the existing raw seed envelopes

```text
F10_fw < 68*2^B,
F10_rev < 35*2^B,
```

gives the exact rational bounds

```text
integral F10_fw dm_occ  < 395304765824751/220000,
integral F10_rev dm_occ < 162772550633721/176000,
bidirectional total     < 2395081816467609/880000.
```

This is a certified physical `theta=1` seed bound.  It is deliberately not
called an arbitrary-return theorem: `m_occ` is not identified with the
owner-leaf law after arbitrary restrictions, and no return-depth weighted
coarea moment follows.

## 3. Why owner timing and scalar cancellation do not close `Z_B`

The exact Gate-3 `J_x` involution proves paired positive scalar laws and
zero signed scalar roof mass.  The Kac ledger likewise records

```text
global signed scalar coarea mass = 0.
```

Both sources explicitly reject arbitrary-test current cancellation.  The
Round-44 occurrence current is

```text
J_(n,j,e)=sigma_e*(tau_hit-tau_miss),
```

so `J(1)=0` is preserved, but a nonconstant test still sees the difference
of the two images.

The Round-51 exact nonimplication model makes this boundary sharp.  For each
`k>=6121`, take one disjoint parent `W_k`, one owned event, and

```text
a_k = 1/[k(k+1)],
Bbar(k)=ceil(log2(2(k+1)^2)),
nu_k=a_k*2^Bbar(k)*(delta_1-delta_0).
```

Then

```text
sum_k a_k = 1/6121,
nu_k(1)=0,
```

and every parent has exactly one active strip and one owned event.  But for
`phi(y)=y/2`, whose `sup + derivative-sup` norm is one,

```text
nu_k(phi)
 = a_k*2^Bbar(k)/2
 >= (k+1)/k
 > 1.
```

Hence the first `N` responses exceed `N`.  This proves only a logical
nonimplication; it does not assert divergence of the actual billiard
current.

There are now two precise valid replacement interfaces:

1. transfer the raw `4^{-b}` occurrence tail to the same-ID arbitrary-`R_n`
   owner-leaf law uniformly in insertion time; or
2. prove a paired-image estimate.  In the model, if the hit/miss image
   separation is `d_k`, `sum_k d_k<infinity` is sufficient.  In particular,
   `d_k=O(k^{-1-epsilon})`, and more strongly
   `d_k=O(c_target)=O(k^{-2})`, would cancel the rank loss.

The global `J_x` pairing reflects target labels and does not certify such a
same-target small separation.  The exact scalar symmetry must therefore not
be substituted for a `C^1` current estimate.

## 4. Aggregate resolvent remains conditional

The Round-50 sharp threshold is unchanged:

```text
rho=(111718729/111718750)^9148,
kappa_B < 2rho/(1+rho),
99914/100000 < 2rho/(1+rho) < 99915/100000.
```

The finite raw seed bound supplies a possible forcing term only.  It does
not supply the recurrence coefficient `kappa_B`.  Thus neither the
unconditional aggregate resolvent nor the return-depth face-tower moment is
promoted.

## 5. One common suffix-envelope, with exact multiplier one

Let `S_reg` be the standard-Borel registry of all finite regular suffix
branches, including the identity.  Define

```text
E_0={physical C1 tests phi:
     sup_(S in S_reg) ||phi composed S||_C1(source(S)) < infinity}
```

and let `T_env` be its norm completion for

```text
||phi||_env = sup_(S in S_reg) ||phi composed S||_C1(source(S)).
```

For every suffix `S`, the composition operator

```text
C_S:T_env -> C1(source(S)),
C_S phi=phi composed S
```

has norm at most one by definition.  Dually, for every source current
`T in (C1(source(S)))^*`,

```text
||S_*T||_(T_env^*) <= ||T||_(C1^*).
```

This is a single common space, rather than a separate norm for each branch,
and its algebraic suffix multiplier is exactly

```text
C_dyn=1.
```

It passes both arithmetic thresholds

```text
1 < 7961063/7800000   (preserve the source quarter),
1 < 43295063/7800000  (preserve a subunit source bound).
```

The construction still is not physical F17.  The area-preserving family

```text
A_L=diag(L,L^-1),  phi(y)=y_1/2,
U_L=[0,L^-1]x[0,1],  V_L=[0,1]x[0,L^-1],  A_L(U_L)=V_L
```

has bounded physical `C^1` norm on a unit chart but envelope pullback
gradient at least `L/2`.  Therefore area preservation and Piola flux alone
do not give a bounded inclusion

```text
C1_physical -> T_env.
```

The next theorem must be billiard-specific: a stable-curve or
dynamic-Hölder anisotropic test space must both control the full-gradient
bulk current and contain the required physical CM2 test algebra with an
explicit comparison constant.  Until then the envelope can be certified as
an algebraic common test layer only; F17 and strong F13 remain open.

## 6. Latest-technology audit

Official versions were rechecked on 2026-07-20:

```text
Demers--Liverani  arXiv:2606.10155v1
Canestrari        arXiv:2604.19671v2
Climenhaga--Day  arXiv:2604.25881v1
```

The Demers--Liverani survey records the relevant stable-curve Hölder test
norms and strong stable/unstable anisotropic Lasota--Yorke mechanism.  Its
constants are not the explicit arbitrary-suffix full-gradient comparison
needed here, and it does not give `C_dyn<7961063/7800000` for this current.
Canestrari gives fixed-map standard-family Growth/small-hole response but no
same-ID coarea-to-owner-leaf tail transfer.  Climenhaga--Day gives
qualitative sufficient rectangles/coding, not a boundary-`Z_B` recurrence
or an F17 constant.  No direct Gate-5 upgrade was found.

## 7. Strict continuation route

The shortest remaining Gate-5 route is:

1. prove a same-ID transfer of the `4^{-b}` moving-occurrence coarea tail to
   the arbitrary-`R_n` owner-leaf law, or prove summable hit/miss image
   separation;
2. derive an actual one-step `kappa_B` below `2rho/(1+rho)` and apply the
   already certified aggregate resolvent;
3. construct a billiard anisotropic test space with bounded physical CM2
   inclusion and explicit full-gradient current pairing;
4. only then promote dynamic F17, strong F13, the face-tower moment and the
   complete all-face F10 field.

## 8. Validation

The suite hash-pins seven dependencies and independently replays all exact
fractions, face rows, the owner/scalar countermodel, the resolvent threshold,
the common-envelope threshold arithmetic and the diagonal compatibility
obstruction.

```text
syntax:                    2/2 PASS
strict JSON:               duplicate keys and NaN/Infinity rejected
deterministic replay:      PASS
hostile mutations:         100/100 rejected
default cert/verifier:     fail closed with exit 2
Gate-5 maturity:           10/18
complete blocks:           0
CM2:                       NO-GO_FOR_CLAIM
```
