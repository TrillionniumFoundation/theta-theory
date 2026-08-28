# CM2 Round186 — source-G factor-face feasibility spike

Date: 2026-07-26

## Verdict: PARTIAL

Question: can the `18,324` Round182 outgoing-W residual collar leaves be
closed by factoring

```text
Nx^2-Ny^2 = (Nx+Ny)(Nx-Ny)
```

and then applying a bounded number of `p` splits?

Evidence: the factorization is useful, but bounded `p` splitting is not a
closure mechanism.  The complete baseline run and a depth-four adaptive run
both exited successfully.  The measured pre-hardening probe source had
SHA256

```text
ebf5ff4964ff2cefafc55372926f5ad4b8f51b545c782603ad3862a0d07b8e55
```

The baseline run took `6:28.67` with maximum RSS `670,916 KiB`.  The
depth-four run took `9:51.05` with maximum RSS `670,684 KiB`.

## Baseline factor census

The input contains `18,324` outgoing-W residual leaves, `8,268` origins and
`11,960` retained children, with exact coordinate volume

```text
861459/419430400000.
```

Their `18,412` unresolved t-faces decompose as follows:

| factor-face class | faces |
|---|---:|
| both factors strict | 4 |
| one active factor absent | 1,172 |
| one active factor full graph | 1,104 |
| one active factor strict derivative, no complete bracket | 16,132 |

No two-active-factor case occurred, and all `18,412` face boxes excluded a
zero target normal.  Thus the exact factorization reduces every unresolved
face to at most one active factor and validates `p` as the preferred graph
axis.

A single split closes `2,288` original leaves and leaves `16,036` original
leaves residual.  Only `64` of those residual parents retain two residual
children; the rest retain a single narrowing branch.

## Depth-four stress result

The depth-four run has the exact terminal census

```text
CLOSED@0       2,256
CLOSED@1      16,036
CLOSED@2      16,100
CLOSED@3      16,100
CLOSED@4      16,100
RESIDUAL@4    16,100
```

It still closes only `2,288/18,324` original leaves.  The residual coordinate
volume is

```text
1550697/13421772800000,
```

or `5.625256832%` of the input volume.  Fixed-depth splitting therefore makes
the residual tubes thin but does not remove the clipped factor curves.

## What worked

- Exact signed factorization separates the inactive factor from one active
  scalar factor on every unresolved face.
- Centered C0 enclosures and strict C1 derivatives directly resolve `2,280`
  faces.
- `p` is slightly better than `s` for the first rectangular split.
- Exact rational volume conservation holds in the depth-four run.

## What failed

- Increasing only the `p` split depth does not increase the whole-original-
  leaf closure count beyond `2,288`.
- The spike does not cover the separate `64` wall-G residual leaves.
- It emits aggregate diagnostics, not reconstructible per-face graph,
  clipping-endpoint, split-lineage or return-signature rows.
- It is not a certificate and contributes zero global exact-key or whole-
  parent credit.

## Recommendation

Do not continue blind fixed-depth `p` refinement.  Build a factorized clipped-
face arrangement instead:

1. use strict `partial_p h` to represent the active zero set as `p=phi(s)`;
2. isolate zeros of the two p-boundary functions with one-dimensional
   interval Newton;
3. materialize empty, full-graph and clipped-curve pieces plus their 0D
   endpoints;
4. treat the `88` two-sided U leaves and `64` wall-G leaves separately; and
5. retain 3D, 2D, 1D and 0D ledgers without promoting local signatures to
   global dispositions.

After the measurements, the probe was guard-hardened to reject non-W targets,
conflicting factor normal forms, unknown Round182 states and invalid negative
depths, and to send progress to stderr.  The hardened source SHA256 is

```text
5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64.
```

Because these spike runs are noncertifying measurements, the strict global
state remains:

```text
source-G global dispositions     0/224580
D02                               BLOCKED
Gate5                             10/18
complete 18-field blocks         0
CM2                               NO-GO_FOR_CLAIM.
```
