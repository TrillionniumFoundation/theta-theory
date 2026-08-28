# CM2 Gate 5 round 36: compact-germ F10 frontier

Date: 2026-07-19  
Status: **every closure-contained compact regular face germ has a finite terminating F10 search; global F10 remains open**

## Verdict

Fix one finite return depth, one regular analytic component, one physical face
piece and one rational dyadic carrier subinterval whose closure stays away
from corners, simultaneous roots, face intersections and grazing endpoints.
On that compact germ, the physical signed coarea density has a canonical
finite integer C1 bound discoverable by a terminating exact interval search.

This closes a pointwise compact-germ existence interface for all five face
grammars.  It does not enumerate arbitrary-`R_n` faces, provide a uniform
parameter radius, or sum the values.  Gate-5 maturity therefore stays
`7/18`.

## Analytic compactness argument

On one fixed finite regular collision word, write the face as

```text
G(x,s)=0.
```

The arbitrary-`R_n` schema supplies a real-analytic local diffeomorphism on
the regular branch.  All-face F9 gives a nonzero level-gradient lower on each
finite rank path, and F8 gives same-ID parent-W transversality `>1/5`.
Therefore the signed coarea density has the local form

```text
rho(x,s) = analytic current numerator
           / nonvanishing analytic level/trace denominator.
```

On a compact parameter germ, `rho`, its tangential derivative and its
parameter derivative are continuous and bounded.  If the physical face has
identically zero parameter normal speed, the signed current and all three
quantities are exactly zero.  No logarithmic derivative is required at a
density zero.

## Canonical terminating search

For compact germ `g`, define `k(g)` as the least `k>=1` for which exact
outward-rounded interval arithmetic certifies

```text
K_g x [-2^-k,2^-k]
```

inside one analytic branch with all strict margins and denominators separated
from zero.  Compactness and strict regularity imply that this dyadic-halving
search terminates.

Then dovetail positive integers `N` with fair dyadic subdivisions and define

```text
N_F10(g) = least N such that every interval box certifies
           |rho|+|d_tau rho|+|d_s rho| < N.
```

Analyticity and compactness imply that this second search also terminates.
The result is canonical and replayable for each germ.

## Five face kinds

```text
source-core face:                               exact zero current at level zero
intermediate core preimage:                     finite compact-germ search
terminal core preimage:                         finite compact-germ search
owner/singularity noncorner face:               finite compact-germ search
moving occurrence / pullback face:              seed bounds plus finite germ search
```

The germ ID extends the same common restriction, physical face instance,
parent-W and connected-rank IDs used by both fw/rev views.  One physical face
injection is not double charged.

## Strict boundary

```text
compact regular germ F10 search schema:          CERTIFIED
materialized arbitrary-Rn N_F10 values:          0
uniform parameter radius:                        NOT CERTIFIED
uniform F10 integer:                             NOT CERTIFIED
global rank-path Lp/weighted F10 sum:             NOT CERTIFIED
complete global F10 field:                       NOT CERTIFIED
Gate-5 maturity:                                 7/18 unchanged
complete operator blocks:                        0
CM2:                                             NO-GO FOR CLAIM
```

The exceptional corners, simultaneous roots, face intersections and grazing
endpoints remain assigned to the strong cemetery.

## Evidence

- `deliverables/cm2_gate5_round36_compact_germ_f10_frontier_cert.py`
- `deliverables/cm2_gate5_round36_compact_germ_f10_frontier_verifier.py`
- `deliverables/cm2-gate5-round36-compact-germ-f10-frontier-manifest-2026-07-19.json`

Validation passes syntax, dependency integrity, replay and live fail-close;
the suite rejects `20/20` hostile mutations.
