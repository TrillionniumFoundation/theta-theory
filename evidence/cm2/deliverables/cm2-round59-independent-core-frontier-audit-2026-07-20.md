# CM2 Round 59 — independent core-frontier audit

Date: 2026-07-20  
Audit mode: append-only, no Round-59 main leaf edited  
Verdict: **PASS.  The three frozen leaves are mutually consistent, their
new claims survive independent arithmetic/type replay, and none closes a
composite gate.**

## 1. Frozen objects

The audit locks both the manifest and the four-entry SHA ledger of every
main leaf:

| leaf | frozen manifest SHA-256 | frozen ledger SHA-256 |
|---|---|---|
| Gate 4 | `e7305e0b72eed28bc68b115e1201fc02e2b66d3cc95906fc6d1efc5e9463a4f5` | `967421bc83b283510cdb25013f2e723e5761337e56471fad64a9ef74b35536c0` |
| Gate 5 | `46eb285a7532377b89e37c1ba2ce6a5b28db1e661eaee4889e576c0a89c94ced` | `2a1487d9fcfb9535f1d05c4c538ff56e6b726d209fe12e48bd637ad2e11b1161` |
| Gate 1/2/3 | `16a2562868df58b2e14bf672d2d0d11735581016ff50e10f5a6d2c1e660d3466` | `985910708fe715d0c891cd6a288b37a5e1b88530db858a712e7e82e80cbb4b71` |

All `12/12` ledger rows resolve to regular files inside `deliverables/` and
match their recorded digests.  The main leaves pin `31/31` older dependency
artifacts; this audit adds `6/6` frozen leaf/ledger pins.

## 2. Gate 4 replay

The two-fibre separator arithmetic is exact.  With

```text
H=999/1000,   N=floor(C_p)+1,   epsilon_m=1/(mN),
```

the good and bad normalized landing charges satisfy

```text
z_good=1/H<C_p<z_bad=N/H<2C_p.
```

Under the frozen strict dyadic convention the bad fibre therefore has
`D_bad=2`, not `1`.  Independent expansion gives

```text
J_total=1+1/m-1/(mN),
integral h 2^D=H(1+3/(mN)),
```

while the bad common mass `epsilon_m H` remains positive.  Hence even an
arbitrarily good aggregate moment cannot prove the almost-everywhere
fibrewise threshold.

The product-rectangle estimate is also correctly typed in one adapted
arclength:

```text
J_u<=F d_+,   h_u>=d_- theta L,
J_u/h_u<=F R/(theta L).
```

For the arithmetic-only row it equals `7833600000/1999<C_p`.  The leaf
explicitly prevents joining those numerical fields to the actual landing
law.

The standard-Borel statement has the advertised weak scope.  For
`eta=(q o pr_landing)_#Gamma_cap`, a supplied Borel `q:landing->U` gives an
`eta`-almost-everywhere probability kernel `Gamma_u` and the integral
reassembly of the same tagged graph measure.  This is not division by the
singleton mass `eta({u})`, which may vanish almost everywhere.  Graph,
endpoint and tag identities hold `Gamma_u`-a.s. for `eta`-a.e. `u`; kernel
values on a quotient-null set are arbitrary.  It does not construct a
stable-product partition, proper conditional standard families, or strong
assembly.  The new branch-inverse row is therefore exactly `1/7` of the
local landing interface and is not a Gate-2 field promotion; Gate 2 remains
`0/17`.

## 3. Gate 5 replay

Putting `Kbar=infinity` on `A_col^c` correctly merges coverage and clock
summability.  For every finite truncation,

```text
M_N=a_0 nu(total)+sum_{j<N}(a_{j+1}-a_j)Fbar_j,
```

and monotone convergence makes `Mbar<infinity` equivalent to both full
coverage and the physical same-law clock moment.  A separate finite atomic
law was replayed directly on both sides of the Abel identity.

Because `r_j=ceil(beta(j+1))` and `0<beta<1`, the jump is zero on plateaux and
is exactly `(w_Z-1)w_Z^{r_j}` on the active set.  Telescoping gives
`#(S intersect [0,N))=r_N-r_0`, hence positive asymptotic density.  The
critical family reduces exactly to a `p`-series on `S`, so the threshold is
`p>1`; `p=1` has full coverage but divergent moment.  The Orlicz statement
is correctly limited to existence for one fixed finite law and is not a
uniform physical estimate.

The Round-25 isolated-root theorem does not pin the Round-50/54 root ID and
does not control accumulation of nonphysical full-word cuts.  The stated
logical separator is therefore a nonjoin, not a claimed billiard orbit.

The operator-capacity schema contains seven distinct bits.  Only `L_id` and
`L_word` are frozen; input, `C24`, operator, output and horizon joins remain
open.  Its cost is correctly extended: `R` and `r_K` are used only on
`A_col`, while every record in `A_col^c` receives infinite policy cost.
Thus the policy criterion explicitly includes `nu(A_col^c)=0` and never
evaluates an undefined finite `K` outside its domain.  Finally,

```text
mu_+ + mu_- = |mu_+-mu_-| + 2(mu_+ wedge mu_-)
```

is exact in the finite-measure lattice.  Independent weighted atoms confirm
that positive charge requires both Jordan variation and common mode.  The
one-anchor finite-cost separator and the zero-signed separator correctly
rule out cancellation-based payment of positive `F10`/cemetery debt.

## 4. Gate 1/2/3 replay

Gate 1's summable rows are confined to the selected physical QNL germ in
the frozen compact-log gauge.  The sums `100/81` and `10000/9801`, the
depth-260 error `<10^-29`, and preservation of the four selected wedges are
consistent.  No all-plaque or combined half-density gauge row is claimed.

Gate 2's `96/96` zero collision-shadow rows concern the positive-width
finite-prefix affine strip.  They are not projected all-depth stable-shadow
rows and do not construct invariant stable plaques.  Its landing audit
agrees with Gate 4: exactly the tagged branch inverse is complete (`1/7`),
while official maturity stays `0/17`.

For Gate 3, the no-earlier-root Boolean formula was tested independently on
exact rational root grids.  With `b>0`, it is equivalent to exclusion of a
root in `(0,tau)`:

```text
a<=0 OR Delta<0 OR (a-tau>=0 AND Delta<=(a-tau)^2).
```

The final squaring is guarded by `a-tau>=0`; endpoint equality is allowed
because the interval is open, and distinct-disk simultaneous contacts are
excluded by the pinned disjointness/tie policy.

Inlining `a,b,Delta` uses four Boolean atoms per distinct competitor.  The
leaf's five-row allocation for all `161` nonchosen slots is conservative;
the remaining flight/contact/normal/reflection/sign/owner/cemetery rows fit
the stated `25`-row reserve.  Thus

```text
variables <=8n+5,
atoms <=830n+12,
degree <=4
```

fits the declared `400n+20`, `2000n+100`, degree-`8` budget.  The complete
conservative word universe is `8*162^n` (two obstacle types and `9*9` lifts).
This is a fixed-depth formula/CAD majorant only; it is not depth-integrable
complexity, a strong `R_s/Q_s`, directional Piola, or `MT_DQ`.

## 5. Literature type audit

The official arXiv API metadata was independently checked for all cited
2026 records.  Their titles and versions match the leaves.  The MME local
product paper concerns its constructed maximal-entropy measure, not the
pinned collision Liouville/SRB landing restriction.  The inter-sign OT paper
does not turn cancellation into unbounded positive Jordan anchors.  The
o-minimal/CAD papers do not instantiate the growing-depth billiard formula
with the required strong boundary/operator norms.  No external theorem is
used as a CM2 promotion.

## 6. Cross-leaf state and acceptance

The strict state is consistent across all three leaves:

```text
Gate 1 / Gate 2 / Gate 3 / Gate 4 / Gate 5: NOT_CERTIFIED
Gate 2 immutable fields:                     0/17
Gate 5 maturity / complete blocks:           10/18 / 0
complete composite gates:                    0/5
CM2:                                        NO-GO_FOR_CLAIM
```

Main-leaf acceptance replay:

```text
syntax:                       6/6
older dependency pins:       31/31
frozen manifest/ledger pins: 6/6
leaf-ledger artifact rows:    12/12
integrity/replay/reemit:      3/3, 3/3, 3/3
hostile mutations:           272/272 rejected
default cert/verifier:        6/6 exit 2
```

Independent-audit leaf acceptance:

```text
syntax:                       2/2
frozen manifest/ledger pins: 6/6
leaf-ledger artifact rows:    12/12
integrity/replay/reemit:      1/1, 1/1, 1/1
hostile mutations:           59/59 rejected
default cert/verifier:        2/2 exit 2
SHA ledger:                   4/4
```

Final four-leaf matrix:

```text
syntax:                       8/8
dependency pins:             37/37  (31 older + 6 frozen-leaf pins)
integrity/replay/reemit:      4/4, 4/4, 4/4
hostile mutations:           331/331 rejected
SHA ledger rows:              16/16
default cert/verifier:        8/8 exit 2
Round-59 stale/temp files:    0
```
