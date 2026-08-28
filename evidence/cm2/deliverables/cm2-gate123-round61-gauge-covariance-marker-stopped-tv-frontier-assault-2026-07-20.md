# CM2 Round 61 Gate 1/2/3 — gauge covariance, landing-marker holonomy and stopped graph-TV frontier

Date: 2026-07-20  
Scope: append-only structural assault from the frozen Round-60 aggregate,
Gate-1/2/3 leaf, Gate-4 landing marker and the earlier physical stopped-kernel
typing  
Strict verdict: **Round 61 does not promote Gate 1, Gate 2 or Gate 3.  It
does, however, remove one artificial Gate-1 numerical obligation, identify
the exact Gate-2/Gate-4 same-law equation, and replace Gate 3's raw
`8*162^n` word enumeration by an actual norm-one stopped restriction on the
weak graph-TV carrier.  The last result is deliberately not a physical
strong `R_s/Q_s`, Piola or `MT_DQ` theorem.  Gate 1, Gate 2 and Gate 3 remain
`NOT_CERTIFIED`; the official Gate-2 registry remains `0/17`, the physical
landing join remains `1/7`, composite gates remain `0/5`, and CM2 remains
`NO-GO_FOR_CLAIM`.**

## 1. Frozen recursive inputs

This leaf pins, without editing, the following inputs.

```text
Round60 aggregate report SHA256
  ef3f2739a7a0ed8c91e82400c05564f97f0c3326ebc1373764b51bbd48f04212

Round60 aggregate recursive-ledger SHA256
  5f6c90735cbb74ec7b36f6c1d2b012ccccaafa40793d291dfcb6a0e212044e9e

Round60 Gate123 manifest SHA256
  f897d81a2e85c4a8e45c436f169043feaef93b019f18229a44da0227c75b2a88

Round60 Gate123 ledger SHA256
  6a29c47462a9526138a059f8577abcf879cd162feca14b435906cce1cd8c087a

Round60 Gate4 manifest / ledger SHA256
  08cda3c966ce03967471c5d87216f4b32ee29a293d81d9dcdd434eb39f7696b3
  4d7c3f06e1671319482c064ec3ea817562567202b111fd014434b7be0a460fac

Round50 physical stopped-kernel manifest / ledger SHA256
  79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73
  7fd9547443951d9960b466aa914f73b1a36f73897e31585018eceed409be4716
```

The frozen rows used below are precisely these:

```text
selected compact-log QNL germ/loop and four strict wedges: CERTIFIED_LOCAL
all-plaque combined half-density class H:                  NOT_CERTIFIED
actual common-landing marker kappa_B<=mu_C, 0<=g_B<=1:    CERTIFIED
physical all-depth stable base/projection/J_hol:           NOT_CERTIFIED
integer-valued Dbar and stopped physical kernel:           BOREL
actual physical fixed-depth first-root formula:            CERTIFIED
fixed-depth physical variables/atoms/degree:                8n+5 / 830n+12 / 4
```

No local fact is silently upgraded to an all-plaque, all-depth or strong
operator statement.

## 2. Gate 1 — exact gauge covariance eliminates an artificial comparison

### 2.1 The same-loop covariance theorem

Let `p` be one immutable physical periodic basepoint.  Let `A_p` be its
return, `Psi_p` the immutable physical holonomy loop at `p`, and let
`v_1,v_2` be the two physical eigenvectors used in the four twisting tests.
Suppose an actual combined half-density gauge `D(x)` is constructed on the
same physical base and gives an exact cocycle cohomology.  At `p`,

```text
A_p^D   = D(p) A_p D(p)^-1,
Psi_p^D = D(p) Psi_p D(p)^-1,
v_i^D   = D(p) v_i.
```

Then, for every `i,j`,

```text
det(Psi_p^D v_i^D, v_j^D)
 = det(D(p) Psi_p v_i, D(p) v_j)
 = det(D(p)) det(Psi_p v_i,v_j).                       (2.1)
```

Thus any invertible exact gauge preserves nonvanishing.  In the
determinant-one combined half-density gauge the four numerical wedge values
are exactly unchanged.

This is simultaneous covariance of the loop **and both physical vectors**.
It is not the false assertion that matrix-coordinate entries are invariant
under an arbitrary basis change.  It also requires the same basepoint and
same immutable physical loop token.  Renaming a different loop or comparing
vectors in an untransported basis does not meet (2.1).

The executable rational replay uses

```text
D   = [[2,1],[1,1]],                   det D=1,
A   = diag(3,1/3),
Psi = [[2,3],[5,7]],
v_1=e_1, v_2=e_2.
```

The four wedges before and after simultaneous transport are exactly

```text
(-5, 2, -7, 3).
```

### 2.2 What this changes and what it does not

Round 60 gave the same-basis approximate route

```text
K_gauge < 216800000000000000000000/1071 > 2*10^20.
```

That route remains correct if one only has an error comparison.  Equation
(2.1) proves that a genuine exact immutable cohomology join needs no
`10^-29` loop-matrix approximation and no finite `K_gauge` at all: twisting
is transported algebraically.

This removes a downstream numerical obligation; it does not construct the
combined gauge.  The missing object is still one physical all-actual-plaque
combined gauge whose weighted projective increments are summable and whose
canonical stable/unstable holonomies exist on the intended registry.  The
exact compact-to-combined loop token join is also not currently materialized.

The strict Gate-1 ledger is therefore

```text
same-loop SL(2) twisting covariance:                    CERTIFIED_EXACT_INTERFACE
need for 10^-29 comparison under an exact join:         REMOVED
physical all-plaque combined-gauge registry:            NOT_CERTIFIED
exact compact-to-combined same-loop cohomology:          NOT_CERTIFIED
same representative class H:                            NOT_CERTIFIED
Gate 1:                                                  NOT_CERTIFIED
```

## 3. Gate 2 — the exact landing-marker/holonomy join

### 3.1 The Radon--Nikodym covariance equation

Round 60 constructed the actual common landing as a positive submeasure of
one induced physical law:

```text
0 <= kappa_B <= mu_C,
g_B=d kappa_B/d mu_C,
0<=g_B<=1.
```

Now suppose future work constructs two actual unstable plaques `u,v` and a
physical stable holonomy

```text
h:u->v,
h_* mu_u = J_hol mu_v.
```

For a source marker `g_u`, the elementary RN chain rule gives

```text
d[h_*(g_u mu_u)]/d mu_v
  = (g_u o h^-1) J_hol.                               (3.1)
```

Consequently, if `g_v` is the frozen landing marker on the target plaque,
then the assertion that the holonomy transports the **same common landing
law** is equivalent to the single typed equation

```text
g_v = (g_u o h^-1) J_hol,       mu_v-a.e.             (3.2)
```

Equation (3.2) is stronger than merely knowing `0<=g_u,g_v<=1` or having a
bounded holonomy Jacobian.  It is also independent of singleton
normalisation: all statements are measure-level and almost everywhere.

The finite exact replay uses

```text
mu_u=(1/2,1/3,1/6),
mu_v=(1/4,1/2,1/4),
g_u=(1,1/2,0),
h:0->1, 1->2, 2->0.
```

It yields

```text
h_*mu_u=(1/6,1/2,1/3),
J_hol=(2/3,1,4/3),
d[h_*(g_u mu_u)]/dmu_v=(0,1,2/3)
                       =(g_u o h^-1)J_hol.
```

### 3.2 A sharp qualitative-holonomy separator

Even the perfect qualitative product case does not force (3.2).  On two
two-point fibres take the same law `(1/2,1/2)`, identity holonomy and
`J_hol=1`, but markers

```text
g_u=(1,0),
g_v=(0,1).
```

Both submeasures have common mass `1/2`; both markers lie in `[0,1]`; the
holonomy and reference density are perfect.  Yet the marker equation fails.
This is an exact logical same-mass model, not a billiard realization.  It
proves that physical stable plaques, bounded `J_hol` and equal total common
mass would still require an actual same-law covariance check.

The Gate-2/Gate-4 join is now more sharply typed:

```text
field 6 tagged first-return inverse:                    CERTIFIED
field 4 actual common-landing RN marker:                PARTIAL_ROUND60
marker-holonomy same-law equation:                      CERTIFIED_EXACT_INTERFACE
physical all-depth plaques/projection/two-sided J_hol:  NOT_CERTIFIED
physical equation (3.2):                                NOT_CERTIFIED
physical landing join:                                  1/7
official immutable Gate-2 fields:                       0/17
Gate 2:                                                  NOT_CERTIFIED
```

No interface row is counted as a new official field.

## 4. Gate 3 — actual stopped graph-TV compression

### 4.1 The actual countable stopped partition

Let `X` denote the pinned joint physical parameter/state carrier.  The
frozen stopped kernel supplies an integer-valued Borel `Dbar`.  On every
stratum `{Dbar=d}`, the relevant schedule depth `N(d)` is finite.  At each
fixed finite depth, the actual Round-59/60 physical formula and half-open
first-root ownership give finitely many Borel word cells; the fixed-depth
semialgebraic theorem gives finitely many connected components.  Singular,
grazing and tie records remain in the explicit cemetery.

Write

```text
A_(d,w,c)
 ={Dbar=d}
  intersect {actual half-open first-root word w at depth N(d)}
  intersect {connected component c}.
```

After empty cells are discarded, the `A_(d,w,c)` plus cemetery form a
countable disjoint Borel partition of `X`.  There is no sum over unrealized
candidate words in the following measure identity.

### 4.2 Exact weak source restriction and output assembly

For a finite signed Borel source measure `mu`, define

```text
R_stop mu = (1_A mu)_A
```

in the `ell^1` direct sum of cellwise finite signed Borel measures.  Countable
additivity of total variation over a measurable partition gives

```text
sum_A ||1_A mu||_TV = ||mu||_TV.                       (4.1)
```

Let `Q_source` sum cellwise source measures.  Then

```text
Q_source R_stop mu=mu.                                 (4.2)
```

On each cell, push forward by the actual graph map and let `Q_output` sum the
resulting output measures.  The triangle inequality gives

```text
||Q_output(nu_A)||_TV <= sum_A ||nu_A||_TV.            (4.3)
```

For positive measures, mass is preserved and counted exactly once.  Hence
the raw candidate factor `8*162^n` is not needed on this weak stopped
graph-TV carrier.  This is a genuine improvement over the Round-60 raw
enumeration route.

The typing is strict:

```text
R_stop: finite signed Borel source measures
        -> ell1(cellwise finite signed Borel source measures),

Q_source: cellwise source measures -> source measure,

Q_output: cellwise graph pushforwards -> output measure.
```

`Q_output` is not called an adjoint, a Banach-space quotient, a physical
strong assembly or a Piola map.

### 4.3 Why weak norm one is not strong norm one

Take `f=1_[0,1)` on the real line and split it into `m` half-open interval
indicators.  Total `L^1` mass remains one.  The zero extension of the source
has variation two, so source `L^1+BV` norm is three.  Each split indicator
has two endpoint jumps.  Thus the direct-sum zero-extension norm is

```text
1+2m,
```

and the restriction ratio is `(1+2m)/3`, which is unbounded.  The executable
replay checks `m=1,2,4,8,16,32`, ending at `65/3`.

This is an exact strong-norm separator, not a lower bound for physical
billiard fragmentation.  It proves precisely why (4.1)--(4.3) do not
produce the missing strong operator: endpoint traces, inverse component
lengths, moving singular faces and current terms must be paid separately.

The Gate-3 boundary is therefore

```text
actual stopped weak graph-TV R/Q:                       CERTIFIED_NORM_ONE
raw 8*162^n factor in weak stopped TV:                  NOT_NEEDED
graph-level strong restriction/assembly:                NOT_CERTIFIED
physical strong R_s/Q_s:                                NOT_CERTIFIED
moving-scatterer directional Piola/current:              NOT_CERTIFIED
MT_DQ:                                                   NOT_CERTIFIED
Gate 3:                                                  NOT_CERTIFIED
```

## 5. Latest official-technology audit

Official arXiv API/HTML were checked on 2026-07-20.  No external theorem is
imported into a physical CM2 certification.

### `arXiv:2603.19509v3`, *A Mathematical Framework for Linear Response Theory for Nonautonomous Systems*

The paper turns sequential dynamics into a global transfer operator on a
sequence space of measures.  Its abstract response theorem assumes common
strong/weak spaces, uniform strong bounds on the equivariant family, strong
differentiability of the operator cocycle and strong exponential loss of
memory.  This is a useful exact blueprint for a sequence-space version of
the direct strong route.

Its applications verify those assumptions for sequential `C^3` expanding
maps and for noisy maps with uniformly positive kernels.  They do not
construct a moving-billiard singular-domain restriction, directional
Piola/current, cemetery trace or the pinned CM2 carrier join.  In particular,
the paper's strong differentiability assumption is the missing conclusion
here, not a theorem that supplies it.

### `arXiv:2604.25881v1`, *Every finite horizon Sinai billiard map has a unique measure of maximal entropy*

Theorem B proves, for a fixed finite-horizon table and an unstable curve of
length at least `delta`, that the sum of lengths of the connected components
of `T^n V` is comparable to `exp(n h_top)`.  It does not bound the number of
components, their minimum length, inverse-length boundary charge, the SRB
landing law, or moving-parameter Piola terms.  Its MME carrier is also not
the pinned collision Liouville/SRB landing carrier.

### Other checked sources

- `arXiv:2604.19671v2` preserves already regular standard families for a
  fixed table with a varying small hole; it does not install the missing
  moving-scatterer strong carrier.
- `arXiv:2605.18110v3` samples components of one inequation under generic
  smoothness; it supplies no depth-integrated inverse-length or boundary
  estimate for the multi-atom billiard formula.

## 6. Strict Round-61 ledger

```text
Gate 1 exact same-loop SL(2) covariance:                 CERTIFIED_EXACT_INTERFACE
Gate 1 physical all-plaque combined class H:             NOT_CERTIFIED

Gate 2 exact marker/J_hol covariance equation:           CERTIFIED_EXACT_INTERFACE
Gate 2 physical all-depth stable carrier/equation:        NOT_CERTIFIED
Gate 2 landing join / official fields:                    1/7 / 0/17

Gate 3 actual weak stopped graph-TV compression:          CERTIFIED_NORM_ONE
Gate 3 physical strong R/Q/Piola/MT_DQ:                   NOT_CERTIFIED

Gate 1 / Gate 2 / Gate 3:                                NOT_CERTIFIED
complete composite gates:                                0/5
CM2:                                                     NO-GO_FOR_CLAIM
```

## 7. Shortest continuation

1. **Gate 1:** construct the physical all-actual-plaque combined
   half-density gauge and its summable weighted-projective registry.  If it
   is joined exactly to the compact physical loop on the same immutable
   base, twisting follows from (2.1); no numerical loop replay is needed.
2. **Gate 2:** construct the all-depth stable base/projection and two-sided
   physical `J_hol`, then verify (3.2) for the actual landing marker while
   controlling fragmentation/span/density and installing strong assembly.
3. **Gate 3:** retain the stopped graph-TV partition, but add a physical
   weighted endpoint/face trace estimate or a genuine strong partition norm;
   then prove moving Piola/current differentiability and `MT_DQ` on the same
   immutable carrier.

## 8. Executable evidence

- `cm2_gate123_round61_gauge_covariance_marker_stopped_tv_frontier_cert.py`;
- `cm2_gate123_round61_gauge_covariance_marker_stopped_tv_frontier_verifier.py`;
- `cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.json`;
- `cm2-gate123-round61-gauge-covariance-marker-stopped-tv-frontier-manifest-2026-07-20.sha256`.

The producer and independent verifier pin eight recursive inputs, replay
the exact simultaneous gauge covariance, the finite RN marker chain rule,
the countable-partition TV identities and the fragmentation separator.  They
enforce deterministic canonical JSON, dependency and artifact hashes,
strict hostile-mutation rejection and fail-closed default execution.
Positive audit modes exit `0`; default execution exits `2` because no
composite gate is closed.
