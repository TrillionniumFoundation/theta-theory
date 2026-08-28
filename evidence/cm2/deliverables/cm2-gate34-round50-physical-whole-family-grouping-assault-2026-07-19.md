# CM2 Gate 4 Round 50 — physical whole-family grouping and common-law frontier

## Verdict

This round installs the object-level grouping that was absent in Round 49.
For every fixed `|s|<=1/400` and finite return depth, the physical
arbitrary-`R_n` registry now has a Borel `family_id`, an exact outer
disintegration, recordwise finite forward/reverse boundary numerators, and a
recordwise properization in each orientation.

The upgrade does **not** install the literal Round-49 common-parent-law join.
The raw `K_par` fibre is generally nonproper, and pulling two different proper
orientation-specific pushforwards back to the raw charge does not change that
geometric type.  A two-proper-view pullback lemma or an explicitly selected
common proper pushforward kernel is still absent.  Independently, the
pre-properization defect has no certified physical exponential moment.  Thus
complete `C_fw/C_rev/q`, a proper common intersection, and the strong cemetery
remain open.  Gate 4 is still `NOT_CERTIFIED`; the global verdict remains
`0/5`, CM2 `NO-GO_FOR_CLAIM`.

## 1. Physical Borel grouping

The Round-35 index is projected to

```text
rn-whole-family:
  (s, component-id, b, source-interval-rank, incidence-rank-path).
```

The projection forgets `natural-short-cell-k` and `image-recut-rank`.  Thus
one group contains one complete positive source-fibre interval, every one of
its deterministic `10^-90` source cells, and every deterministic image recut.

This is a genuine finite family at each outer index:

- the source interval is bounded and has positive finite length;
- its fixed-size natural recut therefore has finitely many cells;
- on a fixed finite incidence-rank path,
  `D_path=product_i(150*2^B_i)<infinity` uniformly bounds the branch
  derivative;
- consequently `length(H(A_k))<=D_path*length(A_k)<infinity`, so each source
  cell has finitely many image recuts and the whole grouped fibre is finite.

Internal recut endpoints use an oriented half-open owner
`[k*10^-90,(k+1)*10^-90)`; image recuts use the same one-sided convention.
The two outer endpoints belong to the pre-existing null regular boundary.
Thus there is no internal duplication and the only omitted points are already
in the null cemetery.  This is only a null-endpoint representative retyping of
the frozen Round-35 recuts; it changes no positive-mass restriction.

The Round-35 record space is Borel, and the projection forgetting `k` and the
image-recut rank has finite fibres.  Lusin--Novikov therefore makes the image
Borel and gives Borel enumerations of the finite fibres.  The discrete
component, interval, and rank codes remain countable, while `b` is a Borel
leaf coordinate.

After pulling image recuts back to the source restriction, the two finite
partitions obey, modulo the null outer boundary,

```text
sum_(k,j) K_fw(y,k,j;A)  = K_par(y,A),
sum_(k,j) K_rev(y,k,j;A) = K_par(y,A).
```

Integrating `K_par` over `b` and summing the countable codes therefore
reconstructs collision-SRB measure on the regular `R_n` registry modulo its
already certified null boundary.  Forward and reverse are alternative
partitions of this one charge, never two charges.

## 2. Recordwise finite boundary numerator

For every positive group `y`, both recut collections are finite and all
regular cell lengths are positive.  In each orientation the cell weights sum
to the same parent mass `p(y)`.  Therefore

```text
J_fw(y)  = sum_j p_fw(y,j)  / ell_fw(y,j)  < infinity,
J_rev(y) = sum_j p_rev(y,j) / ell_rev(y,j) < infinity.
```

Let

```text
M(y)=ceil(log2(1/min_j(ell_fw(y,j),ell_rev(y,j))))_+.
```

Then `M` is finite and Borel, and

```text
max(J_fw,J_rev) <= 2^M p(y).
```

This does not claim a uniform bound in `y`.

## 3. Exact recordwise properization and the remaining type mismatch

Write

```text
a   = 360134800/360493663,
C_p = 4*10^90*360493663/358863.
```

Round 49 proved that `696` is the exact first integer with `a^696<1/2`,
while closed evolution gives

```text
Z(T^r G)/mass(G) <= a^r Z(G)/mass(G) + C_p/2.
```

Define the safe common defect

```text
Dbar(M)=0,                                  if 2^M<=C_p,
Dbar(M)=min{d>=1: 2^-d 2^M<C_p/2},         otherwise.
```

After `696*Dbar(M)` orientation-specific closed evolution, both alternative
whole families are proper.  Since `Dbar` is integer-valued Borel, the stopped
pushforward kernel is Borel by decomposition over `{Dbar=d}`.

The raw once-charged law is

```text
m_raw(dy,dx)=lambda(dy) K_par(y,dx).
```

It is not generally a kernel of proper fibres.  The forward and reverse
properizations are two different measure-preserving pushforwards.  Pulling
their predicates back to `m_raw` preserves their charges but does not make the
raw `K_par` geometry proper.  Hence the literal Round-49 hypothesis

```text
y -> one whole proper G_y under one K_par
```

is not installed, and the fixed-`H` physical `W_r` moment remains conditional.
A valid repair must either prove a Borel measure-preserving two-proper-view
pullback lemma, or choose one proper law, for example
`K_par^*=(F_fw)_#K_par`, and transport the reverse predicate through
`F_rev o F_fw^-1`.

## 4. Why the global clock still fails

Conditional on first installing that missing common-law repair, paying the
variable pre-properization time would give

```text
Wtilde_r = exp(Dbar/(6r)) W_r,
```

because `696/4176=1/6`.  Its `r`-th moment needs

```text
integral p(y) exp(Dbar(y)/6) dlambda(y) < infinity.
```

A rational sufficient input is

```text
integral p(y) (6/5)^Dbar(y) dlambda(y) < infinity.
```

No current artifact proves either the common-law repair or this moment.

The shortest useful new interface is a physical short-length tail on this
same grouped `R_n` kernel:

```text
mass{M>m} <= C_len 2^-m.
```

Exact layer cake with `a=6/5` then yields

```text
integral (6/5)^M p
  <= mass_total + C_len*(a-1)/(1-a/2)
  =  mass_total + C_len/2.
```

Round 26's linear tube concerns the one-step C24 boundary kernel, not the
arbitrary-`R_n` grouped restrictions above, so it cannot be substituted.

The obstruction is localized to endpoint fragments.  Full natural cells
have the fixed `10^-90` scale; arbitrarily short clipped endpoints remain.
The registry only certifies a countable collection of source intervals and
does not bound their physical multiplicity or its inverse-length moment.

## 5. D1 does not logically supply the missing moment

An exact standard-Borel uniform-area model shows the gap.  On disjoint
`b`-bands of width `2^-n`, partition a unit `r`-fibre into `2^(n^2)` equal
intervals of length `2^(-n^2)`, while keeping incidence rank `B=14`.

Then

```text
mass_n  = 2^-n,
J_n     = 2^(n^2-n),
J_n/m_n = 2^(n^2).
```

The D1 density is constant, so its physical `L^(6/5)` moment is finite.  But
the defect grows quadratically and

```text
2^-n (6/5)^D_Z(n)
```

does not even tend to zero.  This is a logical nonimplication model, not a
claim that the model is realized by the billiard.  It proves that the fields
currently frozen in Round 35 cannot by themselves fill the inverse-length
interface.

## 6. Cemetery and joint return

For each fixed `(s,n)`, canonical finite-rank/minimum-length exhaustions
`E_M(s,n)` are Borel, nested, and cover the regular registry.  On the
countable full first-return union, define `E_M^global` by additionally
requiring the return-depth code `n<=M`.  These global sets are also nested and
exhaust the finite physical first-return mass.  Hence discarded mass tends to
zero by monotone convergence: the weak `L1` cemetery is certified in both
scopes.

No uniform integrability of inverse length follows.  Discarded boundary `J`
or defect-weighted mass can remain divergent even while discarded mass tends
to zero.  Therefore strong trace/current cemetery is not certified.

Both ambient orientation families become proper recordwise, but their
intersection need not be proper.  The same-ID common intersection, complete
`C_fw/C_rev`, collision time `q`, and strong cemetery remain
`NOT_CERTIFIED`.

## 7. Mechanical verification

- Python syntax: `2/2` PASS;
- strict duplicate-key/non-finite-constant rejection and exact top-level JSON
  keys: PASS;
- exact independent arithmetic and deterministic replay: PASS;
- hostile mutations: `84/84` rejected;
- certificate and verifier default modes fail closed with exit `2`;
- deterministic manifest replay: PASS.

Artifacts:

- `cm2_gate34_round50_physical_whole_family_grouping_cert.py`
- `cm2_gate34_round50_physical_whole_family_grouping_verifier.py`
- `cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json`

## 8. Next shortest route

1. Install the two-proper-view pullback lemma, or construct one explicit common
   proper pushforward kernel and transport the other orientation's predicate
   to it.
2. Prove the same-kernel short-endpoint tail
   `mass{M>m}<=C_len*2^-m`, or directly certify
   `integral p(6/5)^Dbar<infinity`.
3. Add the `696*Dbar` preclock to the repaired Round-49 `W_r` law and join the existing
   physical D1 `L^(6/5)` moment.
4. Combine with a real numerical `H_cover/beta` to obtain complete
   `C_fw/C_rev`; then address the proper common intersection, `q`, and strong
   cemetery.
