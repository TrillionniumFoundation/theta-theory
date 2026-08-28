# CM2 Round 61 — independent core-frontier audit

Date label: 2026-07-20 (the final freeze crossed local midnight but remains
in the same Round-61 request batch)  
Audit mode: append-only; no frozen Round-61 main leaf edited  
Verdict: **PASS after two pre-freeze type corrections.  The three main
leaves are mutually consistent, all exact algebra/measure claims survive
independent replay, and no composite gate closes.**

## 1. Frozen objects and red-team history

The audit locks both the manifest and four-row SHA ledger of every main leaf:

| leaf | manifest SHA-256 | ledger SHA-256 |
|---|---|---|
| Gate 4 | `2edf4d7801525c746c619cb85b39c59d30018df7c6971f5e48639dc390573b9b` | `a7499c939a1b167a21b62f8f0485ceaac5b44a9c21d2c59e3e22ee45805c56e2` |
| Gate 5 | `59bce010748cccc1ffb829a9c232cab77185e6467433b3fed34988913649ae75` | `27f936d543d7b0f4794741f6896387ab0dcbc4b5d2e729f3412beb6ddc190d26` |
| Gate 1/2/3 | `bb0d263454a33acdf8b2ba443fcc5e247ff1b9214c385f70fa1af2fc26e7c019` | `744bf350c4b3511bb35cefb12d294d4ef407d9c09b43dacb1123eba6103a1f0b` |

All `12/12` main-leaf sidecar rows resolve to regular files in
`deliverables/` and match their recorded hashes.  The leaves pin `30/30`
older baseline/dependency artifacts; this audit adds the six frozen
manifest/ledger pins.

Two type issues were caught before the hashes above were frozen:

1. Gate 4 initially risked calling the marked curve lift a regular standard
   family and using its separator against every anisotropic norm.  The final
   leaf calls it exactly a **cone-curve measure lift**, states that arbitrary
   Borel marking need not remain regular, and restricts the separator to
   BV/derivative trace.
2. Gate 5 initially described a countable algebra containing every labelled
   cemetery atom.  Continuous endpoint/root labels make that impossible.
   The final leaf uses a standard-Borel product cemetery sector, a Borel
   embedding and countable separating generator; it explicitly states that
   the SubProb evaluation code is injective.  Report, producer, verifier and
   manifest all carry the corrected wording.

The Gate-1/2/3 leaf was authored by the present audit agent.  To avoid
self-review masquerading as independence, the root red team independently
checked its stopped-partition dependency chain and its same-token covariance
typing before freeze.  The audit verifier below nevertheless recomputes all
of its exact algebra/RN/TV rows from scratch.

## 2. Gate 4 independent replay

### 2.1 Marker-weighted cone-curve measure lift

The frozen physical law has an exact countable tagged representation

```text
mu_C=integral mu_omega dP(omega).
```

For the actual RN marker `0<=g_B<=1`, Tonelli and linearity give

```text
g_B mu_C=integral (g_B mu_omega)dP(omega).             (2.1)
```

This is an exact positive measure identity.  It retains the branch tags and
does not normalize null curves.  It does **not** assert that the marked
measures form a disjoint Rokhlin partition or remain in a regular standard
family; arbitrary Borel multiplication can create zero density, infinitely
many support components and unbounded log/BV oscillation.  Fields 1 and 4
therefore gain partial curve-measure interfaces only.

### 2.2 Weighted graph-TV lattice

For a finite signed tagged graph measure,

```text
||nu||_X=integral 2^D_land d|nu|
```

is a Banach-lattice norm because multiplication by `2^D_land` is an
isometric order isomorphism to finite signed measures with total variation.
The pinned bad moment is exactly the norm of the included bad graph:

```text
||Gamma_B||_X=integral_B h(y)2^D_land(y)dlambda(y)<infinity.
```

The independent rational sample is

```text
(D,mass)=(2,3/20),(5,1/80),(7,1/320),
ordinary mass=53/320,
weighted norm=3/5+2/5+2/5=7/5.
```

Both endpoint pushforwards contract ordinary TV since `2^D>=1`.  The
identity

```text
Gamma_cap=Gamma_G+iota_B(Gamma_B)
```

preserves source, landing, `n/path/ID/owner` and once charge.  It neither
deletes positive bad mass nor renames it singular cemetery.  Four of five
graph-ledger interfaces are complete, but only the tag row of the requested
strong-current/cemetery interfaces is complete.

### 2.3 Smooth strong separator

With

```text
C_p=4*10^90*360493663/358863,
L=2/(3C_p),
g_N(x)=1/2+(1/4)sin(2*pi*N*x/L),
```

one has exactly

```text
h=L/2,
J=1/2,
z=J/h=1/L=3C_p/2,
D_land=2,
h2^D=2L,
integral_0^L |g_N'|dx=N.
```

Thus the graph moment stays fixed while BV/derivative trace diverges.  This
is a logical smooth product separator, not a billiard realization and not a
claim against every possible anisotropic space.

The seven-field count is correctly `1/7`, with fields `1,4,7` partial;
Gate 2's official score remains `0/17`.  Physical fibrewise properness,
strong current/cemetery, later clocks and `q in L^(6/5)` remain open.

## 3. Gate 5 independent replay

### 3.1 Fixed-insertion same-law RN anchor

Fix one insertion time `j`.  The final leaf takes the actual Round-52
positive owner law `m_j^own` and its Borel Round-54 root/collar map `q_j`:

```text
nu_j=(q_j)_#m_j^own.
```

For a nonnegative integrable orientation cost `c`, define

```text
xi_j(A)=integral_(q_j^-1 A)c dm_j^own.
```

If `nu_j(A)=0`, then `m_j^own(q_j^-1 A)=0`, hence `xi_j(A)=0` and
`xi_j<<nu_j`.  Borel RN versions therefore exist on the same actual law.
The exact fixed-time arithmetic is

```text
395304765824751/220000
+162772550633721/176000
=2395081816467609/880000.
```

Restricting these positive densities to `A_col^c` preserves finiteness.
This certifies a fixed-`j` complement mass/F10 anchor, not any sum over `j`
and not a Jordan identification.

The labelled cemetery map retains the immutable token, continuous
endpoint/root label and insertion time in a standard-Borel product.  A
positive pushforward preserves fixed-`j` mass and marked F10 integral.  It
does not give a strong trace, deduplicated all-time assembly or strong
cemetery.

### 3.2 Seven Borel predicates after the correction

The collision-plus-cemetery state `X` is standard Borel.  Its continuous
cemetery labels are not enumerated atom by atom.  A Borel embedding of the
label tuple space into `[0,1]`, rational collision rectangles and rational
cylinder intervals generate a countable separating algebra `{D_m}`.

Finite subprobability measures on a standard-Borel space are determined by
their values on a countable generating algebra.  Therefore

```text
K -> (K(D_m))_(m>=0)
```

is injective, and equality of all coordinates is equivalent to equality of
kernels.  Borel kernel evaluation then makes input, word/C24 operator and
output/next-input equality predicates Borel.  Sentinels totalize code maps
without reading `K` or `R` outside `A_col`.

The final count is exactly

```text
Borel suffix predicates: 7/7,
universal values:         2 true / 5 open,
Borel R on A_col:         certified,
physical R>=r_K:          not certified.
```

Borel typing does not assert any of the five missing values.

### 3.3 Power-Orlicz frontier

On the same actual owner law put

```text
Y=w_Z^r_K,
q_col=log(2)/(beta log(w_Z))=1/alpha_opt,
Phi(t)=t^q_col.
```

Since `beta(K+1)<=r_K<beta(K+1)+1`,

```text
2^(K+1)<=Phi(Y)<w_Z^q_col 2^(K+1).                    (3.1)
```

Thus raw `Z_col` is finite iff the explicit power-Orlicz moment is finite.
The independent high-precision replay verifies (3.1) at
`K=0,1,2,16,4381,10000`.  The result is an exact same-law criterion, not a
finite RHS: raw `Z_col`, active Abel and the Orlicz moment remain uncertified
finite.

The fixed-`j` hybrid now has a genuinely finite complement term, but its
long recovery and short raw-debt terms remain open.  A uniform bound with no
decay cannot be summed against `w_Z^j>1`.  Weighted Jordan variation,
weighted common mode and all-time complement cemetery are therefore all
still unpaid.  Gate-5 maturity remains `10/18`, with zero complete
18-field blocks.

## 4. Gate 1/2/3 independent replay

### 4.1 Gate 1 same-token covariance

For one immutable physical basepoint/loop token, transform the loop and both
physical eigenvectors simultaneously:

```text
Psi^D=D Psi D^-1,
v_i^D=Dv_i.
```

Then

```text
det(Psi^D v_i^D,v_j^D)=det(D)det(Psi v_i,v_j).        (4.1)
```

The rational replay with

```text
D=[[2,1],[1,1]], det D=1,
Psi=[[2,3],[5,7]]
```

gives the same four wedges `(-5,2,-7,3)` before and after transport.
Equation (4.1) does not assert coordinate invariance under an arbitrary
basis change: the loop token and both vectors must be the same physical
objects and must be transported together.  The future exact same-token
cohomology and all-plaque combined class-H gauge remain absent.

### 4.2 Gate 2 marker covariance

If `h_*mu_u=J_hol mu_v`, then the RN chain rule gives

```text
d[h_*(g_u mu_u)]/dmu_v=(g_u o h^-1)J_hol.            (4.2)
```

The three-atom replay yields

```text
J_hol=(2/3,1,4/3),
pushed marker=(0,1,2/3).
```

Hence equality with the actual target marker is the exact same-landing-law
join.  Identity holonomy and equal common mass alone do not force it.  The
physical all-depth stable carrier and equation (4.2) remain uninstalled;
the landing join stays `1/7`, and official Gate-2 fields stay `0/17`.

### 4.3 Gate 3 stopped weak graph-TV

The dependency chain was independently checked as

```text
integer-valued Borel Dbar
+ finite schedule N(d)
+ actual half-open first-root word cells
+ finitely many fixed-depth components
= countable disjoint Borel stopped partition.
```

For that partition,

```text
sum_A ||1_A mu||_TV=||mu||_TV,
Q_source R_stop mu=mu,
||Q_output nu||_TV<=sum_A||nu_A||_TV.
```

Thus positive mass is counted once and the raw `8*162^n` factor is not
needed on the weak stopped graph-TV route.  This does not remove endpoint
fragmentation from a strong space.  Splitting `1_[0,1)` into `m` half-open
pieces leaves `L^1` mass one but changes the direct-sum zero-extension
`L^1+BV` ratio to `(1+2m)/3`, which is unbounded.

No physical strong `R_s/Q_s`, moving Piola/current or `MT_DQ` follows.

## 5. Cross-leaf consistency

No state or carrier collision was found:

- Gate 4's `X_D^graph` uses the landing defect `D_land`; Gate 3's stopped
  graph partition uses the preproperisation Borel `Dbar`.  Neither mark is
  substituted for the other.
- Gate 3 removes word enumeration only from weak stopped TV.  Gate 4's
  weighted graph-TV and both strong separators retain all endpoint/trace
  debts.
- Gate 4's positive bad graph and Gate 5's fixed-`j` labelled complement
  pushforward are not collision-null cemetery and are not a strong
  current/cemetery theorem.
- Gate 5's orientation-positive RN costs are not renamed Jordan marginals.
- Gate 2's exact marker equation uses the actual `g_B` only as an input; it
  does not manufacture stable holonomy or a Rokhlin quotient.
- Exact Gate-1 twisting transport remains conditional on the future exact
  same-token cohomology join.

## 6. Latest-technology typing

The checked 2026 sources are used only as type audits.  Fixed-table MME
total-length growth does not control component count, minimum component
length or the pinned SRB marker.  Small-hole standard-family evolution
starts from an already regular family and does not construct moving-domain
Piola/current or a strong space containing the present graph carriers.
Nonautonomous sequence-space linear response assumes uniform strong
differentiability and memory loss; those hypotheses are precisely missing
for the moving billiard.  Inter-sign transport does not convert cancellation
into positive Jordan/common-mode moments.  No external theorem is imported
as a physical promotion.

## 7. State and acceptance matrix

The three main leaves agree on the strict state:

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
older dependency/artifact pins: 30/30
frozen manifest/ledger pins:    6/6
leaf-ledger artifact rows:      12/12
integrity / replay / reemit:    3/3 / 3/3 / 3/3
hostile + strict-JSON guards:   615/615 rejected
default cert/verifier:          6/6 exit 2
```

Independent-audit leaf acceptance:

```text
syntax:                         2/2
frozen manifest/ledger pins:    6/6
leaf-ledger artifact rows:      12/12
integrity / replay / reemit:    1/1 / 1/1 / 1/1
hostile + strict-JSON guards:   108/108 rejected
default cert/verifier:          2/2 exit 2
SHA ledger:                     4/4
```

Final four-leaf matrix:

```text
syntax:                         8/8
dependency/artifact pins:       36/36
integrity / replay / reemit:    4/4 / 4/4 / 4/4
hostile + strict-JSON guards:   723/723 rejected
SHA ledger rows:                16/16
default cert/verifier:          8/8 exit 2
Round-61 stale/temp files:      0
```

## 8. Executable evidence

- `cm2_round61_independent_core_frontier_audit_cert.py`;
- `cm2_round61_independent_core_frontier_audit_verifier.py`;
- `cm2-round61-independent-core-frontier-audit-manifest-2026-07-20.json`;
- `cm2-round61-independent-core-frontier-audit-manifest-2026-07-20.sha256`.

The audit producer and verifier pin all six main-leaf manifest/ledger
objects, resolve all twelve sidecar rows, independently replay the Gate-4
weighted graph/BV arithmetic, Gate-5 RN/code/Orlicz typing and Gate-1/2/3
covariance/RN/stopped-TV identities, reject hostile semantic/JSON mutations,
require byte-identical producer regeneration and fail closed by default.
