# CM2 Round 57 Gate 4 — unshifted first-return and killed-path frontier

Date: 2026-07-20  
Strict status: **the common raw restriction has an exact same-ID physical
first-return graph with `tau_cap=n`, and both physical marginals have finite
`Z`; the graph is not proved proper.  The synchronized proper pushforward is
a legal once-charged reference graph lift, not a physical `Q_cap`.  Recovery
path avoidance, a proper unshifted landing, later clocks, physical `q`, Gate
4 and CM2 remain open.**

## 1. The type boundary after `J_cap`

The preceding Round-57 leaf proves

```text
J_cap,total < infinity,
integral h exp(D_cap/6) < infinity,
```

and produces two proper stopped views of one common raw restriction.  It
also pulls that restriction exactly back to subintervals of the original
Round-35 cells

```text
A_c subset R_n,
B_c=T_s^n(A_c) subset C_s.
```

The immutable return-depth and path tags are retained.  Therefore the next
interface separates into three different statements:

```text
exact same-ID first-return graph, tau_cap=n:  CERTIFIED_BUT_UNPROPER
source and landing finite-Z:                 CERTIFIED
proper landing kernel at the same time n:    NOT_CERTIFIED
```

Conflating these statements is the remaining type error.

## 2. The physical raw first-return graph is already exact

Let `kappa_cap` be the once-charged common raw law returned to the original
`A_c` coordinate.  Define

```text
tau_cap(y,x)=n(y),
Q_cap(y,x)=T_s^n(x).
```

The countable half-open registry makes `n` an integer-valued Borel tag.  As
`x` remains in its original `R_n` cell,

```text
T_s^j(x) notin C_s,  1<=j<n,
T_s^n(x) in C_s.
```

Thus

```text
Gamma_cap=(id,Q_cap)_# kappa_cap
```

is an exact physical `C_s` first-return graph measure with the same physical
restriction ID and exactly one parent charge.  The palindromic pullback gives
finite adapted `Z` on the source restriction.  The corresponding common
restriction on `I(B_c)` also has finite adapted `Z`; time reversal gives
finite `Z` on the physical landing marginal in `B_c`.

This certifies a measurable finite-`Z` first-return graph, not a proper
strong-space kernel.

The `R_n` predicate certifies intermediate `C_s` avoidance only on the
original segment `A->B`.  It says nothing about every collision of any later
properisation or terminal schedule.

## 3. Finite `Z` does not imply properness in the same coordinates

Write

```text
C_p=4*10^90*360493663/358863.
```

Take one isolated positive carrier of mass one and adapted length

```text
ell=1/(2 C_p).
```

Its normalized boundary functional is finite but improper:

```text
Z/mass=1/ell=2 C_p>C_p.
```

Any exact positive carrier representation of that same isolated support uses
carriers of length at most `ell`.  Hence

```text
Z >= sum_i p_i/ell = 1/ell = 2 C_p.
```

Positive cuts only shorten carriers.  Retaining or forgetting proof tags
cannot beat this support-length lower bound.  Consequently qualitative
finiteness of the physical source and landing `Z` does not provide an exact
proper disintegration at the unshifted time-`n` collision coordinate.

The shortest legitimate closure is therefore quantitative or geometric:
prove that the exact time-`n` common landing law already has `Z/h<C_p`, or
construct an exact same-time positive coarsening/disintegration with that
bound.

## 4. A positive recovery clock cannot be hidden in a first return

Suppose `x` first returns to `C_s` at time `n`, and append any pointwise
positive clock `r(x)>0`.  There are only two cases:

```text
T_s^(n+r)x notin C_s:  it is not a return;
T_s^(n+r)x in C_s:     time n is an earlier C_s hit.
```

Thus `n+r` is never the first return.  This pointwise argument applies to a
fixed clock, a global clock, a tag-constant clock, or a Borel-variable clock.

Moving the source inside the original excursion does not repair the type:
for `0<r<n`, `T_s^r x` lies outside `C_s` by the `R_n` predicate.  It may be a
valid latent coordinate for the residual excursion, but it is not a source
of the induced `C_s`-to-`C_s` first-return map.  For `r>=n`, the shift has
already crossed the original return.

An exact two-state separator makes all three failures visible.  Let `T` swap
a short `C24` carrier of length `1/(2C_p)` with an outside carrier of length
one by their common mass coordinate.  The `C24` first return is time two.

```text
r=0: first return in C24, but landing Z=2C_p and is improper;
r odd: landing is proper, but outside C24;
r even, r>0: landing is in C24 after the earlier time-two return and is improper.
```

No row is simultaneously a `C24` landing, a first return, and proper.

The synchronized `696 D_cap` clock remains valid for constructing a proper
reference view.  On every `D_cap>0` stratum it cannot be appended to
`tau_cap` and relabelled as the original physical first-return time.

## 5. Strongest legal substitute: a proper reference graph lift

Keep the outer record, the clock stratum and every half-open inverse-branch
tag.  Let

```text
S_fw : (y,x) -> z,
kappa_fw^*=(S_fw)_# kappa_cap
```

be the selected proper stopped view.  On this tagged carrier the inverse is
Borel modulo the pinned null cemetery.  Define endpoint maps

```text
X(z)=physical source projection of S_fw^-1(z),
Y(z)=T_s^n(X(z)).
```

Then exactly

```text
(X,Y)_# kappa_fw^*
  =(id,Q_cap)_# kappa_cap
  =Gamma_cap.
```

This is real progress: it is a proper, once-charged latent parametrization of
the exact physical first-return graph.  It is not a physical `Q_cap` kernel:

- the proper coordinate `z` need not lie in `C_s`;
- `Y` is defined through the inverse endpoint map, not as the first `C_s`
  hit of the orbit starting at `z`;
- `X_#kappa_fw^*=kappa_cap` is still only finite-`Z`, not proper;
- no physical strong-norm or transfer-operator intertwining through `X,Y`
  has been certified.

The reverse fields may be transported by

```text
Theta=S_rev o S_fw^-1
```

without a second parent charge.  An unweighted tagged forward/reverse direct
sum has mass `2h`.  A half-weighted tagged sum has mass `h` and pulls back to
the same graph, but lives on an artificial disjoint union.  Neither becomes
a physical deterministic first-return coordinate by forgetting the tag.

## 6. Terminal nonhit is not path avoidance

Consider

```text
X=(Z/1001Z)x[0,1],
T(i,u)=(i+1 mod 1001,u),
C24={0}x[0,1].
```

The invariant core mass is `1/1001<1/1000`.  Start at state zero and inspect
time `H=1002`.  Every point hits `C24` at the intermediate time `1001`, then
ends at state one outside `C24`.  Therefore

```text
terminal-nonhit mass = 1,
all-intermediate-avoidance mass = 0.
```

A valid added schedule needs the killed predicate on the identical raw ID,

```text
K_H(x)=product_(j=1)^H 1_(C_s^c)(T_s^j x).
```

For a physical return at `tau`, the correct predicate is instead

```text
[product_(j=1)^(tau-1) 1_(C_s^c)(T_s^j x)]
*1_(C_s)(T_s^tau x).
```

If a recovery path hits `C_s` early, that first hit must be extracted as the
physical return branch and its unshifted landing law proved proper.  It may
not be discarded or relabelled as the planned terminal time.

The hereditary killed-Growth theorem controls `Z` for an already defined
positive killed subfamily.  It does not by itself prove positive common mass,
exact once coverage, or unshifted landing properness.

## 7. Strict frontier

```text
physical J_cap,total:                              CERTIFIED_FINITE (pinned)
exact same-ID tau_cap=n first-return graph:         CERTIFIED_BUT_UNPROPER
physical source and landing finite-Z:               CERTIFIED
original R_n intermediate C_s avoidance:            CERTIFIED
proper once-charged reference graph lift:            CERTIFIED
physical proper same-ID first-return landing kernel: NOT_CERTIFIED
intermediate C24 avoidance during added recovery:    NOT_CERTIFIED
later/repeated recovery-clock moments:               NOT_CERTIFIED
physical collision-time q in L^(6/5):                NOT_CERTIFIED
strong singular/current cemetery:                    NOT_CERTIFIED
Gate 4:                                               NOT_CERTIFIED
complete composite gates:                            0/5
CM2:                                                  NO-GO_FOR_CLAIM
```

## 8. Executable evidence

- `cm2_gate4_round57_unshifted_first_return_frontier_cert.py`;
- `cm2_gate4_round57_unshifted_first_return_frontier_verifier.py`;
- `cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.json`;
- `cm2-gate4-round57-unshifted-first-return-frontier-manifest-2026-07-20.sha256`.

The verifier independently replays the finite/improper carrier arithmetic,
the postclock trilemma, the selected/direct-sum charge ledger, the
`1001`-cycle terminal-versus-killed separator, every pinned dependency and
every strict nonpromotion field.  Default certificate and verifier entry
points fail closed with exit `2`.
