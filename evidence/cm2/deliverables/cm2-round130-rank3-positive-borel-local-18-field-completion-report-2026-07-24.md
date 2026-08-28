# CM2 Round130 — positive-Borel local 18-field completion

Date: 2026-07-24

Verdict: **VERIFIED for one explicit positive-Borel rank-three family on
which every exact lambda fibre carries a local 18/18 registry over all 24
common children.  This is not a global Gate5 block.**

## Scope inherited from Round129

Round130 keeps the byte-pinned Round129 analytic family root

```text
lambda = b3
c0     = 1/16384
center = 3/65536
radius = 2^-512
```

inside one Round113 parent and one Round117 operator cell.  The strictly
increasing analytic map

```text
b(lambda) = acos(1/16384) - (36/25)*(pi-asin(t(lambda)))
```

is used only in the forward direction: an exact lambda key determines its
derived exact `b` key.  An independently supplied `b` locator or key is not
accepted.

## Canonical exact-lambda key

The mathematical fibre key is versioned as

```text
round130-canonical-exact-lambda-key-v1
```

For exact collar endpoints `L<U`, define

```text
u = (lambda-L)/(U-L),  0 <= u <= 1.
```

The canonical cases are:

```text
0 <= u < 1   unique binary expansion not eventually all 1
dyadic u     terminating expansion, hence eventually all 0
u = 1        dedicated UPPER_ENDPOINT case; no binary sequence
```

The independent verifier replays the exact test vectors `u=0,1/2,1`,
isolates the corresponding analytic roots, derives three strictly ordered
`b` enclosures, and constructs three distinct canonical lambda keys.  It
then rebuilds the actual slot namespace on all three fibres.  No numeric
guard text and no independently supplied `b` key enters those identities.

The finite certificate does not claim to serialize every member of an
uncountable family.  Its rows are mathematical templates whose actual
constructors require one shared canonical exact-lambda key.

## Widened stage-three geometry

Round130 independently installs the stage-three adapted coordinate over the
full Round129 collar.  At 4096-bit precision the verifier proves

```text
192 < U3(lambda,1)/delta < 193
192 < U3_x(lambda,x)/delta < 193
```

and checks:

```text
widened endpoint guards                         192
stage-three natural cells                       193
combined internal cuts                          215
stage-three output fragments                    216
child output partitions                          24
accepted three-stage norm legs                   72
```

Every widened guard has strict signs `(-,+)` for all exact lambda fibres.
The 215 input and stage-three cuts are put into one strict order, every
fragment has positive guarded length, and each child partition is disjoint,
half-open, and exhaustive up to the measure-zero endpoint set.

The accepted normalized output-length thresholds remain

```text
stage 0   > 3/100
stage 1   > 17/200
stage 2   > 4/125
```

## F14 and F15 on every exact fibre

For each of the 120 base-key templates, Round130 installs

```text
F14 regular-density operator cost       < 34
F15 standard-family operator cost       < 34
```

F14 is a genuine arbitrary-positive-density one-step theorem on the widened
output partition.  Its family inverse-length estimate is

```text
sum_j M_j/ell_j < (100/(3*delta))*M.
```

F15 adds the countable tagged Tonelli lift, signed Jordan completion, and
strict adapted properness.  Its relative recovery clock is zero because the
accepted relative partition is exhaustive:

```text
restricted relative cemetery             ZERO
ambient pre-regularization cemetery       NOT_INSTALLED
all-time owner cemetery                   NOT_INSTALLED
global raw-Z/Orlicz owner drift           NOT_CLAIMED
```

The relative-zero statement is not promoted into an ambient or all-time
cemetery theorem.

## F17 physical graph-current recipient

The verifier independently replays the full `lambda × s` geometry using the
byte-pinned Round122 native Jet2 layer.  Per exact lambda fibre it closes:

```text
input artificial traces                         144
input inter-child incidences                      69
stage-three output traces                        432
stage-three output incidences                    215
same-input incidences cancelled                  192
inter-child incidences retained                   23
physical graph-current legs                       72
recipient components                               4
recipient pullback maps                           72
source-injection derivations                       3
F17 slots                                        120
```

Cancellation requires the same exact lambda and the same source-family tag.
Cross-lambda and cross-tag cancellation are forbidden.  All 72 physical
Piola pullbacks, four recipient components, incidence signs, determinant
identities, guarded target cosines, and stagewise F17 bounds are checked:

```text
stage 0   < 4915200
stage 1   < 2457600
stage 2   < 2457600
```

## F18 and local 18/18 registry

Round130 binds F1–F17 exactly once on each shared base key and adds one F18
slot with direct-standard-N structural phase bookkeeping:

```text
stage block       z^j*z^(r-j)=z^r
child path        z^2*z^1*z^2=z^5
```

This proves the symbolic factorization on the same local operator carrier.
It does not prove Wiener invertibility, Wiener aperiodicity, Kac closure, or
global phase registration.

For every exact lambda fibre:

```text
children                                      24
base keys                                    120
F1-F17 slots                                2040
F18 slots                                    120
all field slots                             2160
local complete 18-field level blocks         120
local complete 18-field child packets         24
local maturity                              18/18
```

The verifier materializes this crosswalk independently for `u=0,1/2,1`.
Each test fibre has 2160 unique slot IDs and 120 complete blocks; the three
slot namespaces are pairwise disjoint.

## Independent verifier and assault

The verifier never imports or executes the Round130 producer.  It uses:

- a byte-pinned independent Round129 verifier and certificate replay;
- the byte-pinned independent Round122 Jet2 mathematical layer;
- an independent canonical-lambda and one-way lambda-to-`b` replay;
- an independent stage-three, F17, and actual-slot reconstruction;
- 78 fully re-signed semantic mutations;
- 16 byte-level strict-JSON attacks;
- regular-file, resolved-path, inode, and atomic-output protection.

```text
producer SHA256
  441b714c6795646a1eeafe94be7419c9b91e14838ea0c321878cde2e11efff31
certificate SHA256
  5bbef09b759c33b635edcf74544af8052ec88915e4f323272d27febfbfe220d5
certificate result SHA256
  6f5af2315002ab6d382028793bbe0ae0c0058196364d9c215f56c1c82c0ee1b0
verifier SHA256
  59d1becfad10272b56ba034396500424cc1f6b29ab8a4a3673050d77a82cf136
verification SHA256
  510ffb04b90277004f2968e27db4367d9253c2e678b51f384dcfd4dc6c241888
verification result SHA256
  bf10f2ef8a4242bfe122a754c6408afe04f98cb350bc9cb0734dd8b17aa4eb28
```

Both producer hash seeds reconstructed the frozen certificate byte for byte.
Both verifier hash seeds reconstructed the frozen verification artifact byte
for byte.  Missing, tampered, symlinked, hardlinked, and FIFO certificate
inputs fail closed without output; symlink, hardlink, FIFO, and protected
output targets are rejected.

## Frozen safety boundary

```text
positive-Borel every-exact-fibre maturity      18/18
whole-family actual row census                   null
global complete 18-field blocks                    0
complete 18-field blocks                           0
Gate5 blocks                                       0
global Gate5 maturity                          10/18
Gate5 status                           NOT_CERTIFIED
CM2                                   NO-GO_FOR_CLAIM
```

Round130 does not cover the remaining global return-word universe or
arbitrary return depth.  It does not install a global nonempty F10 ledger,
global raw-Z/Orlicz/cemetery control, global all-input vector-current
recipient, global Wiener theorem, or Kac closure.  Therefore the local
positive-Borel 18/18 family cannot be counted as a global Gate5 block.
