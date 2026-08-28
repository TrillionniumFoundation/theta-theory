# CM2 Round 60 — independent core-frontier audit

Date: 2026-07-20  
Audit mode: append-only; no frozen Round-60 main leaf edited  
Verdict: **PASS after one pre-freeze type correction.  The three main leaves
are mutually consistent, every new statement survives independent
measure/arithmetic/operator typing replay, and no composite gate closes.**

## 1. Frozen objects

The audit locks both the manifest and the four-row SHA ledger of every main
leaf:

| leaf | manifest SHA-256 | ledger SHA-256 |
|---|---|---|
| Gate 4 | `08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3` | `4d7c3f06e1671319482c064ec3ea817562567202b111fd014434b7be0a460fac` |
| Gate 5 | `d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778` | `ba1fc62efa4ed68df1d1ac0e9117642880768f0cd0374b95f8a1dc557274c483` |
| Gate 1/2/3 | `f897d81a2e85c4a8e45c436f169043feaef93b019f18229a44da0227c75b2a88` | `6a29c47462a9526138a059f8577abcf879cd162feca14b435906cce1cd8c087a` |

All `12/12` leaf-ledger rows resolve to regular files in `deliverables/` and
match their recorded hashes.  The main leaves pin `26/26` older dependency
or baseline artifacts; this audit adds `6/6` frozen leaf/ledger pins.

Before the final Gate-5 freeze the red team found one typing overstatement:
the hybrid integral had been called an unconditional exact iff although its
`R` was only a conditional Borel schema and `C_bad` was not constructed.  The
report, certificate, verifier and manifest were regenerated so that the iff
is now explicitly conditional on a supplied Borel `R` on `A_col` and a
same-law measurable nonnegative `C_bad` on `A_col^c`.  The hashes above are
the corrected hashes.

## 2. Gate 4 replay

### 2.1 The new RN marker is correctly typed

The domination chain is genuinely on one physical induced law.  The frozen
Round-56 input pins

```text
(T_Cs)_#(mu_s|C_s)=mu_s|C_s
```

exactly once and pins the initial source as the same positive measure
dominated by `mu_s|C_s`.  Round 57 then makes `kappa_A` an exact positive
once-charged restriction of that source, with half-open owner tags preventing
duplicate charge.  Therefore, for every Borel `A`,

```text
kappa_B(A)=kappa_A(T_Cs^(-1)A)
          <=mu_C(T_Cs^(-1)A)
          =mu_C(A).
```

Thus `g_B=d kappa_B/d mu_C` exists and `0<=g_B<=1` almost everywhere.  This
does not construct an unstable quotient.  On any future supplied physical
disintegration `mu_C=integral mu_u deta(u)`, the identities

```text
tilde_kappa_u=g_B mu_u,
m(u)=integral g_B dmu_u,
eta_B=m eta,
kappa_u=(g_B/m(u))mu_u on {m>0}
```

are exact Bayes/Rokhlin formulas.  They are `eta`-a.e./conditional-law-a.s.
statements and never divide by `eta({u})`.  Since the physical unstable
quotient, marker component geometry and density/log-distortion bounds remain
absent, field 4 is only partial and the seven-field join remains `1/7`.

### 2.2 Quantitative and good/bad guards

Both smooth product separators replay exactly.  With

```text
C_p=4*10^90*360493663/358863,
L=2/(3C_p),
```

the full short plaque has normalized boundary `3C_p/2` and strict dyadic
defect `D_land=2`.  With `H=999/1000` and `N=floor(C_p)+1`, the unit plaque
with `N` positive components has

```text
C_p<N/H<2C_p,
D_land=2.
```

Hence even qualitative perfection of fields 1--4 does not imply the strict
field-5 threshold.

The Borel split `G={z_land<C_p}`, `B={z_land>=C_p}` retains the original
same-ID first-hit graph.  `Gamma_G` has a proper original-time **landing**
representation but may have zero mass; source properness is not inferred, so
this is not yet a full proper return kernel.  Finite
`integral_B h 2^D_land` neither makes `B` null nor turns it into the
collision-null singular cemetery.  The proposed bad-part route correctly
remains conditional on five missing positive strong interfaces.  Whole-graph
properness, later clocks, physical
`q in L^(6/5)` and the strong current cemetery remain uncertified.

## 3. Gate 5 replay

The Round-50 token is exactly the projection of the Round-54 token obtained
by forgetting only `word-cell`; the first six immutable coordinates are
identical and coordinate projection is Borel on the standard-Borel labelled
registry.  This does not create the missing Round-25-to-50 numeric root-ID
crosswalk.

On the regular owner law, `d_other=0` is exhausted by coincidence with an
other registered cut or membership in its closure/accumulation set.  Thus
the `N_cut union N_acc` frontier is exact, while its owner-trace mass is not
known.  Collision-area nullity is correctly not substituted for singular
owner-trace nullity.

The clock arithmetic also replays:

```text
1<w_Z<2,
r_K=ceil(beta(K+1))<=K+1,
w_Z^r_K<2^(K+1)=ell(K)^(-1).
```

Therefore finite raw `Z_col` would pay the optimal clock, but neither raw
`Z_col`, the active Abel series nor a physical Orlicz bound is certified.

All seven suffix definitions are explicit.  Exactly four predicates are
Borel on the frozen registry (`L_id,L_word,L_C24,L_horizon`) and three remain
conditional on missing input/kernel-evaluation/output code maps.  Five
universal values remain open.  Hence `R` is only a conditional Borel schema,
and the corrected hybrid statement is precisely:

```text
given Borel R on A_col and measurable nonnegative same-law C_bad on A_col^c,
integral C_hyb<infinity
iff its long-collar, short/raw-debt and complement-positive integrals
are all finite.
```

No physical hybrid finiteness is claimed.

Finally, the exact fixed-insertion arithmetic

```text
395304765824751/220000
+162772550633721/176000
=2395081816467609/880000
```

pays the positive forward/reverse orientation ledgers.  It does not identify
them with the Round-54 Jordan marginals.  The latter have only a fixed marked
unweighted mass anchor.  Without a same-owner-law domination and all-time
decay, neither weighted Jordan variation nor weighted common mode is paid.

## 4. Gate 1/2/3 replay

For Gate 1 the conditional compact-to-combined budget is arithmetically
exact:

```text
(17344/10^32)/(8568/10^52)
=216800000000000000000000/1071
>2*10^20.
```

No physical `K_gauge` or all-plaque registry is supplied.  The selected
series sums to `100/81`, while the logical second plaque may carry a harmonic
combined-gauge tail, so selected twisting cannot be promoted to all plaques.

Gate 2's depth-97 logical completion agrees with every actual certified
prefix `1..96` and shows why finite-prefix collision shadows do not imply an
all-depth stable quotient.  The landing join remains `1/7`, and the official
Gate-2 score remains `0/17`.

For Gate 3, with `b>0`, the no-earlier-root predicate

```text
a<=0 OR Delta<0 OR [a-tau>=0 AND Delta<=(a-tau)^2]
```

is the exact complement of a root in `(0,tau)`; the squaring is guarded and
endpoint equality is allowed.  The padded count

```text
161*5+25=830
```

is an upper bound, not an undercount.  The logical law
`P{N=n}=2^(-n-1)` pays `E exp(N/6)` but makes the current raw candidate bound
have expectation `4 sum 81^n=infinity`.  This only blocks the raw enumeration
payment route; it is not a lower bound on actual nonempty branches.  The CAD
degree recurrence `D_(r+1)=2D_r^2`, `D_0=8`, has the stated solution
`D_r=2^(4*2^r-1)`.

## 5. Literature typing

The cited 2026 sources are used only as type audits.  Small-hole Sinai
billiard standard-family invariance starts from an already regular family
and does not construct the actual common landing law, moving-scatterer
Piola/`MT_DQ`, or a strong space containing standard pairs.  The recent CAD
papers do not pay growing-depth inverse-component boundary complexity.  The
inter-sign transport paper does not turn signed cancellation into positive
Jordan/common-mode moments.  No external theorem is imported as a CM2
promotion.

## 6. State and acceptance

The three leaves agree on the strict state:

```text
Gate 1 / Gate 2 / Gate 3 / Gate 4 / Gate 5: NOT_CERTIFIED
Gate 2 immutable fields:                     0/17
Gate 5 maturity / complete blocks:           10/18 / 0
complete composite gates:                    0/5
CM2:                                         NO-GO_FOR_CLAIM
```

Main-leaf acceptance replay:

```text
syntax:                         6/6
older dependency/artifact pins: 26/26
frozen manifest/ledger pins:    6/6
leaf-ledger artifact rows:      12/12
integrity / replay / reemit:    3/3 / 3/3 / 3/3
hostile + strict-JSON guards:   516/516 rejected
default cert/verifier:          6/6 exit 2
```

Independent-audit leaf acceptance:

```text
syntax:                         2/2
frozen manifest/ledger pins:    6/6
leaf-ledger artifact rows:      12/12
integrity / replay / reemit:    1/1 / 1/1 / 1/1
hostile + strict-JSON guards:   80/80 rejected
default cert/verifier:          2/2 exit 2
SHA ledger:                     4/4
```

Final four-leaf matrix:

```text
syntax:                         8/8
dependency/artifact pins:       32/32
integrity / replay / reemit:    4/4 / 4/4 / 4/4
hostile + strict-JSON guards:   596/596 rejected
SHA ledger rows:                16/16
default cert/verifier:          8/8 exit 2
Round-60 stale/temp files:      0
```
