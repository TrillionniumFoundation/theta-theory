# CM2 Gate 3 continuation: forward-time audit and an immutable row orbit

Date: 2026-07-15  
Verdict: **the sixteen previously claimed physical vertices are retracted as nonforward; one complete `Jx/Jy` orbit of compact immutable physical subrows is certified; the global component registry, DQ, and scalar matching remain NOT CERTIFIED**

## 1. Mandatory correction

The first endpoint pass isolated sixteen exact algebraic roots at which one
oriented line is tangent to three target circles.  Exact algebraicity is not
enough for a billiard event: every relevant contact time must also be on the
forward ray.

The earlier classifier compared the common-tangent partner time with the
distinguished target time but omitted the condition

\[
\ell_{\mathrm{other}}>0.
\]

The corrected predecessor adds this condition.  The new independent
certificate replays all sixteen old collars at 320-bit precision and proves,
uniformly on each whole collar,

\[
0<\ell_T<3,
\qquad
\ell_{\mathrm{other}}<0.
\]

Thus all sixteen partner contacts lie behind the source point.  They are
exact common-line algebraic roots but **not physical forward event vertices**.
The corrected physical vertex count for this family is zero.

This retraction changes the endpoint ledger to:

```text
82,048 target-target descriptors
= 81,760 strict on the full parameter window
+ 288 first-pass unresolved;

288 first-pass unresolved
= 284 fully resolved by adaptive strict subdivision
+ 4 uniformly nonphysical tau=3 collars.
```

The four remaining collars form one `Jx/Jy` orbit and carry the uniform
witness `0<ell_other<ell_target`; consequently the distinguished target is
not first.  Numerically unresolved target-target collars remain zero, but no
physical endpoint vertex is manufactured.

An independently pinned descriptor resolver also replays the entire original
320-row suspect set, not only the sixteen retracted collars.  Its exact
whole-row classification is:

| empty witness | descriptors |
|---|---:|
| earlier common tangent behind source | 52 |
| later partner is not next | 12 |
| no source intersection | 32 |
| strict third target before distinguished target | 164 |
| distinguished target behind source | 60 |
| total | 320 |

Its adaptive closed cover has 448 leaves at maximum depth 3 and returns
`physical=0`, `unresolved=0`.  Both that resolver manifest and its SHA
manifest are pinned by the continuation certificate.

## 2. One complete immutable `Jx/Jy` subrow orbit

The retraction does not affect the following direct first/miss computation.
Take the representative signed tangency sheet

```text
source G, target W[0,0], epsilon=+1.
```

On the full parameter window `|s|<=1/400` and the compact rectangle

\[
0\leq t\leq10^{-5}
\]

in the `G:E` chart, the certificate constructs the tangent graph and proves
uniformly that:

- the source cosine is positive and the tangent graph stays in `-1<p<1`;
- the tangent time is positive and below 3;
- `W[0,0]` is the unique first tangency;
- the continued ray has unique miss owner `G[1,1]`;
- the parameter coarea has a strict positive sign.

The graph is continuous over a connected closed rational `(t,s)` rectangle.
Every first-root, miss-root, and coarea inequality is strict on that whole
rectangle, so it is a connected immutable physical **subrow**.

Direct Arb checks certify all four symmetry members:

| symmetry | chart and `t` interval | signed target | miss owner | coarea polarity |
|---|---|---|---|---:|
| `id` | `G:E`, `[0,10^-5]` | `W[0,0], +` | `G[1,1]` | `+1` |
| `Jx` | `G:W`, `[0,10^-5]` | `W[-1,0], -` | `G[-1,1]` | `-1` |
| `Jy` | `G:E`, `[-10^-5,0]` | `W[0,-1], -` | `G[1,-1]` | `+1` |
| `JxJy` | `G:W`, `[-10^-5,0]` | `W[-1,-1], +` | `G[-1,-1]` | `-1` |

The absolute coarea intervals agree under reflection.  Hence a
symmetry-invariant scalar density and constant test cancel pairwise on this
orbit.  The four currents have different supports, so no cancellation against
an arbitrary test function is claimed.

These four subrows are not claimed to be the maximal connected components of
their full signed sheets.

## 3. Exact finite global reduction

The certificate independently recomputes:

```text
288 signed sheets
= 128 cross-colour parameter-active sheets
+ 160 same-colour sheets with partial_s Delta identically zero.
```

The 128 active sheets form 32 four-element `Jx/Jy` orbits.  Their finite raw
endpoint ledger is:

| active descriptor type | count |
|---|---:|
| target-target common tangencies | 36,352 |
| source grazing | 256 |
| parameter boundary | 256 |
| `u_y=0` polarity splits | 128 |
| total | 36,992 |

This is a finite semialgebraic arrangement problem, not 36,992 physical
events.  Empty, nonforward, duplicate, and non-first descriptors must be
removed before maximal rows are counted.

## 4. Minimum remaining blockers

1. quotient every genuinely physical duplicate endpoint across raw
   descriptors;
2. enumerate every connected visible component of all 288 signed sheets;
3. cut until miss trace and coarea polarity are constant;
4. prove maximality and emit exact physical event rows;
5. assemble the global distributional derivative quotient;
6. prove rowwise DQ matching and global scalar-current matching.

Executable verdict:

```text
GATE3_RETRACTED_16_NONFORWARD_VERTEX_AUDIT: CERTIFIED
GATE3_ONE_COMPLETE_JX_JY_IMMUTABLE_SUBROW_ORBIT: CERTIFIED
GATE3_ALL_288_CONNECTED_EVENT_ROWS: NOT_CERTIFIED
GATE3_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED
```

No unconditional CM2 conclusion follows from this local orbit.
