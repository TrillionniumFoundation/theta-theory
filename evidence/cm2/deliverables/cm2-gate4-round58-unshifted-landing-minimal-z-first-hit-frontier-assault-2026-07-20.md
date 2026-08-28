# CM2 Round 58 Gate 4 — unshifted landing minimal-`Z` / first-hit frontier

Date: 2026-07-20  
Strict status: **the exact same-time representation problem is now solved as
an iff.  The physical maximal connected landing components attain the minimum
possible boundary functional `J_land,min`; Round 57 implies
`J_land,min,total<∞`, and the associated full dyadic `D_land` moment is finite.
The required strict fibrewise inequality `J_land,min<C_p h` is not proved, so
the exact time-`n` physical landing and return kernel remain unproper.  A
once-covering next-return extraction has finite aggregate `Z` but neither
repairs the original time nor forces properness.  Gate 4 and CM2 remain open.**

## 1. Frozen input and the remaining type question

Round 56 proves the full induced identity

```text
E_fw,total=(T_C_s)_#(mu_s|C_s)=mu_s|C_s
```

exactly once and with a controlled finite-`Z` representation.  Round 57 then
constructs an exact once-charged common raw law `kappa_cap` with

```text
tau_cap=n,
Q_cap(x)=T_s^n x,
T_s^j x notin C_s for 1<=j<n,
T_s^n x in C_s,
```

and finite physical source and landing `Z`.  Separately, it proves finite
`J_cap,total` and builds a proper stopped two-view reference carrier with a
finite `D_cap` clock moment.

The unresolved question is strictly same-coordinate:

```text
Can the physical time-n landing law on B be represented properly
without changing n, the physical ID, the first-hit predicate or its charge?
```

The answer is now reduced to one exact threshold.

## 2. Physical maximal components minimize every exact positive `Z`

Fix one immutable

```text
(y, physical landing carrier chart, physical restriction ID).
```

Remove the already frozen singular, null and cemetery punctures, and let
`C` range over the maximal connected positive components of the actual
physical landing support.  Define

```text
J_land,min(y)=sum_C kappa_y(C)/ell(C).
```

This is Borel.  Round 57 enumerates the maximal components by their least
rational owners with Borel endpoint infima and suprema.  Component mass and
adapted length are Borel, and the displayed quantity is a monotone countable
sum.  The empty fibre has `h=J_land,min=z_land=0` and is never normalized.

Every admissible standard-pair density is strictly positive on its connected
carrier.  Hence an exact positive carrier cannot cross a positive-length
zero-law gap or an omitted singular/cemetery puncture.  It lies in one
maximal component `C`, so its length is at most `ell(C)`.  Summing over every
pair representing the mass on `C` gives

```text
sum_(W subset C) p_W/ell(W) >= kappa_y(C)/ell(C).
```

Conversely, restricting the inherited regular density once to every maximal
component attains equality.  Therefore

```text
boxed:  inf_(all exact positive same-coordinate representations) Z
        =J_land,min(y).
```

This exhausts all legal same-time freedom **within the frozen `(y, physical
carrier chart, immutable physical ID)`**:

- positive cuts only shorten carriers;
- forgetting proof tags cannot lower the maximal-component value;
- every actual-union coarsening has already been performed;
- no coarsening may cross a true gap or puncture;
- forgetting an immutable physical ID changes the kernel contract.

It does not exclude a future cross-`y`/cross-chart physical Rokhlin
redisintegration built from an actual stable-holonomy quotient.  That would
be a new Gate-2/physical interface, not a same-ID positive coarsening, and is
not currently certified.

Even allowing countably many proposed proper families does not weaken the
criterion.  If each positive subfamily has `J_i/h_i<C_p`, their union has

```text
(sum_i J_i)/(sum_i h_i)<C_p
```

as the outer mass-weighted average.  Conversely, the single maximal-component
family works whenever the total ratio is below threshold.  Thus

```text
boxed: exact unshifted same-ID landing proper
       iff J_land,min(y)<C_p h(y)
       for almost every positive fibre y.
```

## 3. A new physical finite quantity and its dyadic moment

Round 57 step 3 constructs the common restriction on `I(B)` with global
affine bound

```text
Z_3<infinity.
```

Time reversal preserves adapted length and `Z`.  Physical maximal-component
coarsening therefore gives the new actual quantity

```text
J_land,min,total<=Z_3<infinity.                     (3.1)
```

Put

```text
z_land(y)=J_land,min(y)/h(y),

D_land=0                              if z_land<C_p,
D_land=min{d>=1:2^-d z_land<C_p/2}    otherwise.
```

The strict boundary matters: `z_land=C_p` is not proper and gives
`D_land=2`.  On every positive defect stratum,

```text
2^D_land<=4 z_land/C_p.
```

Consequently

```text
integral h(y)2^D_land(y) dlambda(y)
 <=H+(4/C_p)J_land,min,total
 <infinity.                                            (3.2)
```

This is distinct from `D_cap`:

```text
D_cap  = stopped proper-view common-refinement geometry,
D_land = unshifted physical B geometry.
```

Equation (3.2) is a real landing-complexity upgrade.  It is not permission to
evolve `696 D_land` collisions and append them to `tau_cap=n`; any positive
postclock is no longer the original first return.

For

```text
B_k={y:z_land(y)>=2^k C_p},
```

Markov gives

```text
integral_(B_k) h dlambda
 <=J_land,min,total/(2^k C_p) ->0.                    (3.3)
```

The `k=0` bound is only finite, not zero.  Discarding `B_0` can lose positive
physical mass and cannot be charged to a null cemetery.

## 4. Finite high-mass separator: ambient proper and `D_cap=0` still fail

Let

```text
N=floor(C_p)+1.
```

On one unit half-open collision interval with Lebesgue law and identity
first return at time one, retain `N` equal intervals of total mass `999/1000`,
separated by `N-1` equal positive gaps of total mass `1/1000`.  All endpoints
have unique half-open owners and the pieces remain in one immutable physical
landing chart/ID.

The model satisfies the installed mass facts:

```text
999/1000>249/250,
21/111718750<1/1000<1/500.
```

The full induced ambient law is proper with normalized `Z=1`.  The exact
physical common first return is `tau=1`, `Q=id`, and has finite but improper
minimal landing functional

```text
J_land,min=N,
z_land=N/(999/1000)>C_p.
```

A finite piecewise-translation reference isomorphism can place the retained
pieces adjacently on `[0,999/1000)`.  In two identical reference orientations

```text
J_cap=1+1=2,
z_cap=2/(999/1000)<C_p,
D_cap=0.
```

That is a stopped/reference reassembler, not a physical same-coordinate
coarsening: its inverse endpoint map restores all true landing gaps.  Thus

```text
full ambient proper return
+ high common mass
+ finite physical landing Z
+ finite J_cap and D_cap=0
does not imply unshifted physical landing properness.
```

This is a logical exact-standard-family nonimplication model, not a claim
that the billiard realizes the fragmentation.

## 5. Why the full ambient return cannot absorb the marker

The full induced identity plus a Borel common marker `chi` is enough for weak
integrals and for the exact graph measure.  At the strong standard-family
level, however, multiplication by `chi` replaces the ambient law by
`chi mu`.  Its boundary price is precisely `J_land,min`, not the boundary
price of the unmarked ambient family.

Therefore the full induced law may remain the ambient carrier, but it cannot
serve as the required physical strong kernel until a same-coordinate
characteristic-multiplier theorem proves

```text
J_land,min<C_p h
```

on the identical marked IDs.  Likewise, a proper stopped reference law and
its inverse endpoint maps recover the graph measure but do not transfer
properness to the physical endpoint coordinate.

## 6. Once-covering first-hit extraction and reinduction

For any controlled finite-`Z` positive law on `C_s`, the disjoint cylinders

```text
{tau_C_s^+=j}, j>=1,
```

cover the recurrent law modulo the frozen null set.  Retaining the original
ID and adding the return-path suffix charges every point exactly once.  The
Round 41/42 hereditary killed resolvent and Round 55 terminal extraction give
a finite aggregate landing `Z` for this next-return law.

Applied to the physical `B` marginal, this produces an exact first return
from `B` to `C_s`.  From the original `A` endpoint it is the second return,
not the original `tau_cap=n` return.  Moreover:

- the rebased `B` source is still possibly improper;
- the new landing is only finite-`Z`, not necessarily below `C_p`;
- starting at the proper stopped reference view may give a physical first
  entrance, but that view need not lie in `C_s`;
- no finite number of reinductions forces properness: the identity separator
  returns the same fragmented improper law at every occurrence.

The strongest legal upgrade is therefore

```text
once-covering rebased next-return graph: finite-Z, exact, unproper.
```

A future occurrence becomes a proper physical first-return kernel only if
both its rebased source and landing satisfy their maximal-component
thresholds.  It would still not retroactively properize the original
time-`n` landing.

## 7. Latest technical audit

Official metadata and the 2026 review source were checked for:

- arXiv `2606.10155v1`, Demers--Liverani, *Recent Progress in the
  Application of Transfer Operators to Dispersing Billiards*;
- arXiv `2104.06947v3`, Demers--Liverani, *Projective Cones for Sequential
  Dispersing Billiards*;
- arXiv `2501.16102v2`, Balint--Komalovics, *Improved estimates of statistical
  properties in some non-uniformly hyperbolic dynamical systems*.

They provide/review Growth, projective-cone and induced/tower technology but
do not state a theorem converting an arbitrary marked finite-`Z` induced
landing into a proper landing at the same physical time and on the same IDs.
No external theorem is promoted.

## 8. Strict frontier

```text
physical J_cap,total and D_cap moment:              CERTIFIED (pinned)
exact unshifted same-ID first-return graph:          CERTIFIED_BUT_UNPROPER
physical source/landing finite Z:                    CERTIFIED
physical J_land,min,total:                           CERTIFIED_FINITE
physical full dyadic D_land moment:                  CERTIFIED_FINITE
maximal-component minimal-Z / properness iff:        CERTIFIED
same-time cut/coarsening/disintegration freedom:     EXHAUSTED_BY_IFF_WITHIN_FROZEN_ID_AND_CHART
once-covering rebased next-return graph:             CERTIFIED_FINITE_Z_BUT_UNPROPER
physical proper same-ID first-return kernel:         NOT_CERTIFIED
intermediate C24 avoidance during added recovery:    NOT_CERTIFIED
later/repeated recovery-clock moments:               NOT_CERTIFIED
physical q in L^(6/5):                               NOT_CERTIFIED
strong singular/current cemetery:                    NOT_CERTIFIED
Gate 4:                                               NOT_CERTIFIED
complete composite gates:                            0/5
CM2:                                                  NO-GO_FOR_CLAIM
```

The shortest remaining physical input is no longer representational:

```text
prove J_land,min(y)<C_p h(y) almost everywhere on the identical physical
landing IDs, preferably with a uniform margin.
```

If this fails on positive mass, the original unshifted kernel cannot be
properized without changing its physical first-return semantics.

## 9. Executable evidence

- `cm2_gate4_round58_unshifted_landing_minimal_z_first_hit_frontier_cert.py`;
- `cm2_gate4_round58_unshifted_landing_minimal_z_first_hit_frontier_verifier.py`;
- `cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.json`;
- `cm2-gate4-round58-unshifted-landing-minimal-z-first-hit-frontier-manifest-2026-07-20.sha256`.

Validation freezes dependency/report hashes, strict JSON, independent exact
rational replay, deterministic manifest regeneration, byte-identical reemit,
`82/82` hostile-mutation rejection, default fail-closed exit `2`, and the
strict `0/5` / `NO-GO_FOR_CLAIM` boundary.
