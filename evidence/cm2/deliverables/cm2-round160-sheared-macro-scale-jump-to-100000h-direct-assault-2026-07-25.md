# CM2 Round160 — direct assault on the upper-tail scale barrier

Date: 2026-07-25

## Objective and certified scope

Round159 showed that repeated 4h continuation was formally sound but could
not practically reach the first real chart-scale obstruction. Round160
attacks that scale barrier directly. It certifies one sheared macro slab from
`352h` through `100000h`, producing the combined corridor

```text
abs(delta_x)/h in [0,100000]
combined exact slabs       74
combined typed boxes      222
interior untyped cells      0.
```

This is a full R1648-scale certificate, not the earlier frontier-only remote
diagnostic. Its upper endpoint remains nonterminal, so the result advances
D02 but does not close it.

## Why the direct axis-aligned assault wrapped

In physical h units, the C24 and D3 graphs drift with
`delta_beta/h` at a slope close to 2.807 as `abs(delta_x)/h` grows.
Placing the full tail in an axis-aligned
`(abs(delta_x)/h,delta_beta/h)` rectangle discards this correlation. The
resulting wide interval evaluates combinations that do not occur on the
physical sheet and loses discriminant and event signs.

Round160 instead follows the drift with the exact rational shear

```text
u = abs(delta_x)/h = -delta_x/h
s = 2807/1000
w = delta_beta/h - s u.
```

The physical map and its constant generator Jacobian are

```text
(delta_x,delta_beta) = (-u h,(s u+w)h)

J = [[-h,             0],
     [2807/1000 h,    h]].
```

The `w` widths stay bounded while `u` crosses 99,648h. This preserves the
dominant parameter correlation inside every propagated affine model.

## One slab in place of 24,912

The exact macro domain is

```text
u in [352,100000]
u width = 99648h
equivalent exact 4h slabs = 24912.
```

It is partitioned only in `w`:

```text
C24_EVENT             [-420,-405]
STRICT_RETURN_BRIDGE  [-405, -10]
D3_EVENT              [ -10,  10].
```

The partition is closed and gap-free. The C24/bridge face is exactly
`w=-405`; the bridge/D3 face is exactly `w=-10`. There is one new typed slab,
three new typed boxes, zero internal untyped cells and zero new event
families.

The corresponding physical beta/h hulls are

```text
C24       [71008/125, 280295]
bridge    [72883/125, 280690]
D3        [122258/125,280710].
```

These large physical hulls do not reintroduce axis-aligned wrapping because
the engine propagates the correlated generators `(u,w)` rather than
independent physical-coordinate boxes.

## Exact inheritance at 352h

At the Round159/Round160 seam, the physical beta faces and strict
intersections are

```text
C24
  prior     [542,594]
  macro     [71008/125,72883/125]
  overlap   [71008/125,72883/125]

bridge
  prior     [594,965]
  macro     [72883/125,122258/125]
  overlap   [594,965]

D3
  prior     [965,991]
  macro     [122258/125,124758/125]
  overlap   [122258/125,991].
```

All three intersections have positive width. The macro slab therefore joins
the inherited connected sheet rather than merely certifying a remote
look-alike box.

## Typed-face proof obligations

### C24 boundary

The complete collision-1648 terminal event audit proves:

- the event function `terminal_p(u,w)+1/50` has opposite strict signs on
  `w=-420` and `w=-405`;
- its partial derivative in `w` is strictly positive on the full macro
  domain;
- parametric interval Newton maps strictly inside the C24 box;
- every fixed `u` fibre has one transverse C24 root;
- the intended terminal core is the sole unresolved core, with every other
  terminal constraint strict;
- the complete 1,648-collision path remains central with incidence 14, and
  all 265,328 radius-four candidate tests are decided.

The C24 strict-margin ledger reaches dyadic depth 4,284, which is why the
engine retains 8,192-bit working precision.

### Strict-return bridge

The bridge uses both bounding event graphs:

- D3 is strictly increasing in `w`, and its value at the upper bridge face
  `w=-10` is strictly negative for every `u`;
- the terminal event is strictly increasing in `w`, and its value at the
  lower bridge face `w=-405` is strictly positive for every `u`;
- hence the entire bridge is strictly between the two event graphs and is
  forced to `RETURN_AT_3_INNER`;
- the complete 1,648-collision path, retained-chart and full-radius-four
  candidate audits all pass, contributing another 265,328 candidate tests.

The D3 bridge miss has dyadic depth 4,290. Correlation is preserved through
the sheared scalar-affine D3 model rather than recovered by subtracting wide
independent intervals.

### D3 boundary

The collision-three event audit proves:

- D3 has opposite strict signs on `w=-10` and `w=10`;
- its `w` derivative is strictly positive on the complete macro domain;
- parametric interval Newton lies strictly inside the D3 box;
- every fixed `u` fibre has one transverse D3 root;
- the anchor `W[0,0]` is the sole unresolved radius-four candidate and its
  double root strictly preempts the frozen nonanchor winner;
- every other retained and full-radius-four candidate decision and winner
  gap is strict.

The D3 audit performs 322 prefix and 161 collision-three candidate tests,
for 483 tests in total.

## Complete census

```text
complete R1648 C24 objects reconstructed               1
complete R1648 bridge objects reconstructed            1
collision-stage/object pairs                       3,296
R1648-path radius-four candidate tests            530,656
complete D3 event boxes reconstructed                   1
D3 event-box radius-four candidate tests              483
all new radius-four candidate tests                531,139
```

Together with the inherited Round159 atlas, this gives 74 slabs, 222 typed
boxes and zero interior untyped cells throughout `[0,100000]`.

## 8,192-bit decisions versus 256-bit display outers

The engine sets `ctx.prec=8192` before propagation and before all graph,
edge-sign, derivative and interval-Newton decisions. It serializes selected
Arb values through a fixed padded outer representation that defaults to only
256 bits so the JSON remains finite and deterministic.

For ordinary-sized quantities that display is informative. For D3 quantities
near dyadic depths 4,000 and beyond, the 256-bit display quantum is much
coarser than the value. A printed D3 derivative outer can therefore
conservatively straddle zero even though the underlying 8,192-bit Arb ball is
strictly positive. Similarly, the whole event-box outer is expected to
straddle zero because the event graph crosses the box.

The logical order is decisive:

1. calculate the Arb enclosure at 8,192 bits;
2. require its strict edge or derivative predicate;
3. calculate the interval-Newton inclusion;
4. only then serialize a coarse outer for documentary visibility.

The verifier reruns this computation and checks the resulting strict Boolean
claims. The 256-bit outers are not used as substitute sign certificates.

## Independent reconstruction and attack surface

The independent verifier does not import or execute the producer. It pins
the producer source, pins and identifies the scale-jump engine module,
cross-binds the Round159 certificate and verifier, and reconstructs:

- the C24, bridge and D3 full audits;
- the one macro slab and its three typed boxes;
- both exact `w` adjacencies;
- all three inherited physical-beta overlaps at `352h`;
- the 24,912 equivalent-slab count;
- the complete new census;
- the 74/222/0 combined atlas;
- the open `100000h` endpoint and every strict nonpromotion field.

The verifier status is `PASS`. It rejects 67/67 semantic or document
mutations and 12/12 strict JSON or encoding attacks, including coherent
rehashed mutations of the shear, typed audits, macro list, adjacency,
inheritance, census, atlas, endpoint, runtime restoration and nonpromotion.

## Cryptographic bindings

```text
scale-jump engine source
  1de1fe55020fbb7de975c4fa04cd820723e9296a4d69db493092fe9b3f579122

producer source
  dcc73eb24b893b65f6919640843fa289b849ad483ca38e3923849b12a21a901d
certificate file
  f2243caf5d14e5876388f48f468927b5846284c5997879e23d70d1456a6bca5f
certificate result
  984855ea7a08fa5aea8728b7f51f5b5e3ed8a57ca840e7d2448c39adf0d7a4a0

verifier source
  d8cd7921dd098cec363d0944e9e3eae2fa2b0756ea6b6d6840619b31bb98b12e
verification file
  7495730c2be0df01470169469c4a91af659b1f926e6fb1748aaec220d072c731
verification result
  a07050a832d7d0971c6e0dce43c14b2a958fdc48116444ef5ca7b1dd4b5f0279

typed-audit bundle
  ff0e9c03d59594aa705affcbd5a8adce2343199c69cd37bb5a5a2ee7ae2513ae
macro-slab list
  25048155dca5eec915215cbc972d76df54aaf178f7e5653cec7ca6672f7542c2
```

## Meaning of the coordinate name

`SHEARED_COMPACT_ANGLE_LIFT` means that the affine generators are aligned
with the compact-angle drift while computations remain on a lifted `u`
coordinate. It is not a claim that the lift has already been quotiented by
the physical angular symmetry. In particular, Round160 has not yet:

- reached or typed the first chart/owner/event/terminal face beyond
  `100000h`;
- glued all chart faces on a compact fundamental angular domain;
- branch-and-bound classified the complement of the connected sheet;
- excluded disconnected exterior maximal-component sheets.

The coordinate label therefore carries no credit for compact exterior
completion.

## Technology review

The method review checked the relevance of CAPD doubleton and QR/Lohner
wrapping control, Ariadne Taylor-model propagation, Julia TaylorModels and
Codac contractors/set inversion. Each remains a reasonable fallback for a
later dependency blow-up or nontrivial exterior-domain split.

The first macro jump closes with the existing pinned Arb/affine machinery,
so this round introduces no CAPD, Ariadne, TaylorModels or Codac dependency.

## Strict state and next assault

```text
D02                                      BLOCKED
D03 authorized                           false
global Gate5                             10/18
global complete 18-field blocks              0
CM2                             NO-GO_FOR_CLAIM
```

The next assault starts at `100000h` and performs dyadic sheared-slope
recentering, updating the rational shear as necessary, until the first
certified chart, owner, event or terminal face is reached. That face must be
typed and glued before any chart transition. The subsequent D02 core gate is
a full branch-and-bound exclusion of disconnected exterior sheets on the
fundamental angular domain.
