# CM2 Round 63 — independent core-frontier audit

Date: 2026-07-21  
Verdict: **PASS; no source-leaf correction was required.  The strict state is
`Gate 1/2/3/4/5 = NOT_CERTIFIED`, complete composite gates `0/5`, Gate-5
maturity `10/18` with zero complete 18-field blocks, and
`CM2=NO-GO_FOR_CLAIM`.**

## 1. Frozen scope and independence

The Gate-1/3, Gate-2/4 and Gate-5 authors, followed by the root agent,
explicitly confirmed that all three Round-63 sidecars were final before this
audit read them.  This audit did not author any of the three leaves and did
not modify them.  It pins the complete Round-62 recursive root and the final
Round-63 leaf roots.

```text
Gate 1/3 manifest:
bdd351955c4537e649009e753900a7f61e3befcc16db55f810af2902dd3581ea
Gate 1/3 SHA ledger:
b48def6d29a68f9cf30db2b349a41e06b3e5df58766f8d9323e256f75c6ad058

Gate 2/4 manifest:
955908ee74ff6ec0354224978850ef683aeacd1923ce85bffd1290467321d23f
Gate 2/4 SHA ledger:
a739ffbe1bb9f14fdc8c72c573594f56930a7c4f32efb77fa4dac60d256ec870

Gate 5 manifest:
a052e9c278a6359bdcd554020de28b2e8d821eb0e1267758a702bf3dff130ab8
Gate 5 SHA ledger:
605487e4aee375b589f5fd13e9de85ab716e41d8db285cb3327529c7cc857a9e
```

The recursive Round-62 pins are

```text
aggregate report:
873557a6653a826700d5daf11e8b118f5ddca1cf911e085f9c20aa591ab2136f
recursive 15-row ledger:
e54b5a1de2b4bddf0c7589b77997b1f28284040b64b31fdfbf58af9e73233bac
```

All eight direct pins and all twelve leaf sidecar rows replay exactly.  The
three leaves contain `13 + 15 + 13 = 41` dependency/baseline pin rows, with
intentional recursive overlap; all 41 row hashes and the Round-62 recursive
15-row ledger were recomputed.

## 2. Gate 1/3 — independent algebra, incidence and typing audit

### 2.1 Endpoint conjugacy and the sharp model budget

For

```text
B(x)=C(fx)^-1 A(x)C(x)
```

direct multiplication gives

```text
H_B^s(x,y;n)
=C(y)^-1[H_A^s(x,y;n)+Delta_n^s(x,y)]C(x),

Delta_n^s
=A^n(y)^-1[C(f^n y)C(f^n x)^-1-I]A^n(x).
```

If the canonical `H_A` family is already uniformly Hölder, `C,C^-1` have
uniform bounded Hölder moduli on the actual plaques, and the forward and
backward defects converge uniformly to zero, the limit is explicitly

```text
H_B^s=C(y)^-1 H_A^s C(x),
H_B^u=C(y)^-1 H_A^u C(x).
```

The Hölder bound follows from this endpoint product.  Consequently a
separate equi-Hölder modulus for every finite approximant is not an
independent debt under those hypotheses.  This does not remove the actual
all-plaque transfer or defect-decay debts.

The norm calculation gives only the sufficient estimate

```text
||Delta_n^s||
 <=M_s H_C K_C L_s^alpha
   (kappa_s lambda_s^alpha)^n d(x,y)^alpha,
```

and its backward analogue.  Thus `theta_s,theta_u<1` are sufficient, not
necessary physical conditions.  Their strictness is sharp only in the
declared logical diagonal `SL(2)` model:

```text
A=diag(a,a^-1),
A^-n(lambda^n E_21)A^n=(a^2 lambda)^n E_21.
```

The 30 replay samples correctly realize decay at `9/16`, a nonzero constant
at `1`, and divergence at `2`.  No actual billiard third gauge is inferred.

### 2.2 Incidence reduction and the F13 boundary

At a shared oriented face the independently recomputed current is

```text
B_e=v_e[(Y_i)_*(rho_i trace_e)-(Y_j)_*(rho_j trace_e)].
```

It cancels before total variation only when the branch/formula, density
trace, signed velocity, landing trace and retained quotient tag agree.
Half-open ownership alone does not cancel it.  The three artificial-cut
rows cancel exactly, while the mismatched-landing replay has pairing `-1`
and total variation `2`.

The actual stopped cells are indexed by `(Dbar, physical word, maximal
component)`.  Proof-only CAD/dyadic subdivisions therefore do not enter the
incidence chain.  Duplicate chart/lift seams cancel only under their pinned
trace identifications; genuine physical and cemetery faces remain.

The Round-44 F13 join is correctly limited to the base parameter `s=0`,
regular-density Borel-TV layer on the same IDs:

```text
c_F13,n <=(3816937/7800000)c_X,n
          <(1/2)c_X,n=(25/302)c_D1,n.
```

It does not pay a finite-`s` strong pullback, cemetery, or stopping-clock
trace.  In particular the safe-clock replay has

```text
Dbar(310)=0, Dbar(311)=2,
R0: 0 -> 1392,
```

and later unit changes of `Dbar` cost `696`.  This moving clock-jump is a
sixth debt outside Round 44's five regular F13 grammars.  The exact reduced
ledger remains

```text
E_stop^red=E_regular,physical+E_clock+E_cemetery,
```

with only the base regular Borel term paid.  Bulk anisotropic Piola,
physical strong `R_s/Q_s` and `MT_DQ` remain open.

Independent executable acceptance:

```text
dependency pins:                  13/13
threshold regimes / samples:      3/3 / 30/30
incidence / taxonomy rows:        3/3 / 11/11
clock / F13 ratio rows:            13/13 / 2/2
integrity / replay / reemit:       PASS / PASS / byte-identical
hostile semantic / strict JSON:    385/385 + 15/15 rejected
SHA sidecar:                       4/4
default cert/verifier:             2/2 exit 2
```

## 3. Gate 2/4 — independent square, `L1` and transport audit

For future physical source and landing holonomies, direct addition and
subtraction gives

```text
Delta_L=D_v Delta_S+(D_vP_S-P_LD_u)a_u.
```

If the declared branch--holonomy square and reference-law transports commute,
the commutator vanishes and the dynamic `L1` isometry yields

```text
||Delta_L||_1=||Delta_S||_1.
```

This preserves the marker debt; it does not force either defect to vanish.
The three-point replay has both defect norms `1/6` with a zero square
commutator, so it is also a direct nonimplication model.

For exactly two plaques with outer weights `1/2,1/2`, the saturation
distance is

```text
delta_sat
=1/2 inf_f (||g_u-f||_1+||g_v-Pf||_1)
=1/2||g_v-Pg_u||_1.
```

The lower bound is the triangle inequality and `f=g_u` attains it.  The
factor `1/2` is essential and is explicitly present in both the theorem and
the replay (`delta_sat=1/12`).  No many-plaque or conditional-expectation
projection is claimed.

For a `C1` holonomy with adapted-arclength derivative
`0<m<=lambda<=M` and the declared density transport,

```text
F_v=F_u,
|E_v|>=m theta_u L_u,
R_v<=R_u M/m,
z_v<=F_u R_u M/(m^2 theta_u L_u).
```

One factor of `m` pays span contraction and the other comes from the
`1/lambda` density ratio.  The rational replay is exactly `72`.  The bound
is conditional: none of `F,R,theta,L,m,M` is installed on the actual common
landing law.  Zero stable defect also leaves both the short-span and
fragmentation separators above `C_p`.

The graph-cylinder remains a bookkeeping current.  Its weighted trace is
`2^D nu`, so `2^-D` is still required to recover `nu`; no physical
anisotropic/Piola strong assembly follows.  The landing ledger remains
`1/7` complete with fields 1, 4 and 7 partial, and Gate 2 remains `0/17`.

Independent executable acceptance:

```text
dependency/baseline pins:          15/15
square / saturation / m^2 replay:  PASS / PASS / PASS
zero-defect separators:            2/2
integrity / replay / reemit:       PASS / PASS / byte-identical
hostile semantic / strict JSON:    180/180 + 4/4 rejected
SHA sidecar:                       4/4
default cert/verifier:             2/2 exit 2
```

## 4. Gate 5 — independent kernel, Jordan and complement audit

### 4.1 The killed trace-kernel theorem is conditional

For positive laws and substochastic kernels on the immutable time-labelled
direct sum, measure domination and the Lyapunov row imply

```text
Lambda_(j+1)<=Lambda_j K_j,
K_j V_(j+1)<=kappa V_j,
V_j>=1

=> Lambda_j(1)<=Lambda_j(V_j)
                  <=kappa^j Lambda_0(V_0).
```

Hence positivity and Tonelli give the displayed weighted bound only when
`w_Z kappa<1`.  The one-point rows with ratios `3/4,1,9/8` replay the sharp
subcritical, critical and supercritical cases.  Distinct insertion times
remain distinct slices.  The frozen physical inputs construct none of
`K_j,V_j,kappa<w_Z^-1`; a charge-preserving trace kernel has `kappa=1` and
diverges because `w_Z>1`.  Thus the result is an exact conditional interface,
not all-time decay.

### 4.2 Cost-Jordan is not the Round-54 flux law

On the same actual fixed-`j` owner law the two positive Round-61 orientation
cost measures satisfy the measure-lattice identity

```text
xi_j^f+xi_j^r=|xi_j^f-xi_j^r|+2(xi_j^f wedge xi_j^r).
```

The rational total is exactly

```text
395304765824751/220000
+162772550633721/176000
=2395081816467609/880000.
```

Restriction to `A_col^c` preserves the identity and fixed-time finiteness.
This is the orientation-**cost** Jordan law.  It is explicitly not identified
with Round 54's actual signed physical hit/miss flux `J_p`; neither positive
F10 nor strong cemetery is upgraded, and variation/common mode do not gain
an all-time sum.

### 4.3 Complement strata

Absolute continuity of both cost measures with respect to the actual owner
law correctly turns the already proved source exact-grazing null set into
zero fixed-`j` orientation cost.  For the remaining exact cuts, positivity
gives nullity of the countable union iff every enumerated cut has zero cost.
For positive individual gaps with zero infimum, the decreasing small-gap
sets satisfy

```text
chi_j(N_acc)=lim_k chi_j(A_(j,k)).
```

Continuity from above is legal because the fixed-`j` cost law is finite.
No same-law bound for the remaining cut rows, no full-word small-gap tail,
and no pre-regularization cemetery payment exists.  The source `eta/B` tail
cannot be renamed as a later/full-word clearance tail.  The seven suffix
predicates remain Borel, but only two values are known and five stay open.

Independent executable acceptance:

```text
dependency/baseline pins:          13/13
killed-kernel rows:                3/3
cost-Jordan rational/lattice rows: PASS
complement strata rows:            4/4
integrity / replay / reemit:       PASS / PASS / byte-identical
hostile semantic / strict JSON:    160/160 + 4/4 rejected
SHA sidecar:                       4/4
default cert/verifier:             2/2 exit 2
```

## 5. Cross-leaf consistency and final state

The cross-leaf review found no legal substitution that promotes a composite
gate:

1. Gate-3's base regular F13 charge does not pay its moving strong,
   clock-jump, cemetery or bulk-Piola rows.
2. Gate-2/4's exact square transports stable-marker debt without annihilating
   it, and zero marker defect still does not pay quantitative properness.
3. The Gate-2/4 graph-cylinder is not a physical Gate-3 strong current.
4. Gate-5's fixed-time orientation-cost Jordan law is not Round-54 signed
   flux and cannot be used for signed telescoping.
5. A conditional Gate-5 killed-kernel theorem is not an actual all-time
   recurrence or decay row.

Combined source-leaf acceptance is

```text
syntax:                         6/6
dependency/baseline pin rows:  41/41
integrity:                      3/3
replay:                         3/3
reemit:                         3/3 byte-identical
hostile semantic:               725/725 rejected
strict JSON:                    23/23 rejected
hostile plus strict JSON:       748/748 rejected
SHA sidecar rows:               12/12
default entry points:           6/6 exit 2
```

The strict final state is therefore

```text
Gate 1: NOT_CERTIFIED
Gate 2: NOT_CERTIFIED; official fields 0/17
Gate 3: NOT_CERTIFIED
Gate 4: NOT_CERTIFIED; landing join 1/7, fields 1,4,7 partial
Gate 5: NOT_CERTIFIED; maturity 10/18; complete blocks 0
complete composite gates: 0/5
CM2: NO-GO_FOR_CLAIM
```

No external theorem is promoted by this audit.
