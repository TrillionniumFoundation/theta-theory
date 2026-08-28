# CM2 Round160 — sheared macro scale jump to 100000h

Date: 2026-07-25

## Result

Round160 replaces the proposed mechanical 4h upper-tail tiling with one
correlation-preserving sheared macro slab. It strictly extends the connected
typed atlas from `abs(delta_x)/h=352` to `100000`. Its exact status is

```text
CERTIFIED_SHEARED_MACRO_SCALE_JUMP_TO_100000H__D02_STILL_BLOCKED
```

The combined certified corridor is now

```text
abs(delta_x)/h in [0,100000].
```

The combined atlas has 74 exact typed slabs, 222 typed boxes and zero
interior untyped event cells. The lower symmetry-axis endpoint remains
terminal. The new upper endpoint at `100000h` is explicitly nonterminal.

## Correlation-preserving macro coordinates

The new slab uses

```text
u = abs(delta_x)/h = -delta_x/h
w = delta_beta/h - s u
s = 2807/1000.
```

Thus

```text
delta_x    = -u h
delta_beta = (s u + w) h
```

and the generator Jacobian into physical coordinates is

```text
[[-h,             0],
 [2807/1000 h,    h]].
```

The shear retains the dominant correlation between `abs(delta_x)` and
`delta_beta` that was lost by the earlier axis-aligned macro probe. On the
single exact macro slab

```text
u in [352,100000]
width = 99648h,
```

the gap-free typed chain is

```text
C24 event box            w in [-420,-405]
strict RETURN bridge     w in [-405, -10]
D3 event box             w in [ -10,  10].
```

The two internal shared faces are exactly `w=-405` and `w=-10`. This one
macro slab replaces 24,912 exact 4h slabs without introducing an untyped
interior event cell or a new event family.

## Inherited 352h face

All three new boxes have strict physical-beta overlap with their Round159
predecessors at the shared `u=352` face:

```text
type       Round159 beta/h       Round160 beta/h             strict overlap
C24        [542,594]             [71008/125,72883/125]       [71008/125,72883/125]
bridge     [594,965]             [72883/125,122258/125]      [594,965]
D3         [965,991]             [122258/125,124758/125]     [122258/125,991]
```

Equivalently, the three macro faces are
`[568.064,583.064]`, `[583.064,978.064]` and
`[978.064,998.064]` in beta/h units. The inherited seam therefore remains
connected in every typed family.

## Full audit census

The macro slab is not a frontier-only probe. Its C24 box and strict-return
bridge each replay the complete 1,648-collision path and the full radius-four
candidate universe; its D3 box receives the complete collision-three event
audit.

```text
new complete R1648 C24 audits                       1
new complete R1648 bridge audits                    1
new collision-stage/object pairs                3,296
new R1648-path radius-four candidate tests     530,656
new complete D3 event-box audits                    1
new D3 event-box radius-four candidate tests      483
new total radius-four candidate tests         531,139
```

Both R1648 objects have 1,648 collisions and 265,328 full-radius-four
candidate tests. The C24 box retains only the intended terminal C24
constraint as unresolved. The bridge is strictly
`RETURN_AT_3_INNER`, and the D3 box retains only the intended
collision-three anchor discriminant. All runtime adapters used to reuse the
pinned full-audit engines are checked as restored.

## Precision note

The engine computes at 8,192-bit Arb precision. Several D3 quantities are
far below the 256-bit rational lattice used only to serialize compact outer
intervals into the certificate. Consequently, a displayed 256-bit D3 outer
interval can straddle zero even when the underlying derivative has a strict
sign; the bridge D3 miss, for example, has a worst dyadic depth of 4,290.

Those 256-bit outers are conservative coarse displays, not the sign oracle.
Every strict C24, bridge and D3 sign is tested against the original 8,192-bit
enclosure before serialization, and the independent verifier recomputes the
same high-precision predicates. No strict conclusion is inferred from a
zero-straddling coarse display field.

## Independent verification

The verifier imports or executes neither the producer nor its result builder.
It pins the producer and engine sources, reconstructs the macro slab and all
three typed audits, recomputes both exact `w` adjacencies, all three inherited
352h overlaps, the census and the combined atlas, and cross-binds the
Round159 certificate and verification results.

It reports `PASS` and rejects:

```text
semantic/document mutations        67/67
strict JSON/encoding attacks        12/12
```

The rejected mutations cover the shear, macro width and equivalent slab
count, typed-box chain and digests, inherited seam, event-family and terminal
claims, census, atlas totals, runtime-adapter restoration, inheritance,
type-confusion, wrapper and all strict nonpromotion fields.

## Hashes

```text
scale-jump engine source SHA256
  1de1fe55020fbb7de975c4fa04cd820723e9296a4d69db493092fe9b3f579122
producer source SHA256
  dcc73eb24b893b65f6919640843fa289b849ad483ca38e3923849b12a21a901d
certificate file SHA256
  f2243caf5d14e5876388f48f468927b5846284c5997879e23d70d1456a6bca5f
certificate result SHA256
  984855ea7a08fa5aea8728b7f51f5b5e3ed8a57ca840e7d2448c39adf0d7a4a0
verifier source SHA256
  d8cd7921dd098cec363d0944e9e3eae2fa2b0756ea6b6d6840619b31bb98b12e
verification file SHA256
  7495730c2be0df01470169469c4a91af659b1f926e6fb1748aaec220d072c731
verification result SHA256
  a07050a832d7d0971c6e0dce43c14b2a958fdc48116444ef5ca7b1dd4b5f0279
```

The certificate additionally binds the three typed audits by
`ff0e9c03d59594aa705affcbd5a8adce2343199c69cd37bb5a5a2ee7ae2513ae`
and the macro-slab list by
`25048155dca5eec915215cbc972d76df54aaf178f7e5653cec7ca6672f7542c2`.

## Method review and dependency decision

The fallback technology review covered CAPD doubleton/QR-Lohner wrapping
control, Ariadne Taylor models, Julia TaylorModels and Codac validated
set-inversion/contractor methods. They remain viable fallbacks if later
dyadic recentering or exterior branch-and-bound develops dependency blow-up.
The present certificate needed none of them: its pinned local affine/Arb
engine closes the first macro jump, so Round160 introduces no new external
dependency.

## Strict nonpromotion and next gate

`SHEARED_COMPACT_ANGLE_LIFT` names the correlation-preserving lifted
coordinate chart used by this slab. It does **not** certify that the compact
angular fundamental domain, its chart-face gluings, or disconnected exterior
sheets have been exhausted. It also does not make `100000h` terminal.

```text
D02                                  BLOCKED
D03 negative oracle            unauthorized
global Gate5                         10/18
global complete blocks                   0
CM2                        NO-GO_FOR_CLAIM
```

The next core gate is to continue beyond `100000h` by dyadic sheared-slope
recentering until the first certified chart, owner, event or terminal face.
After that face is typed and glued, the remaining D02 obligation is
disconnected-exterior-sheet exclusion on the fundamental angular domain.
