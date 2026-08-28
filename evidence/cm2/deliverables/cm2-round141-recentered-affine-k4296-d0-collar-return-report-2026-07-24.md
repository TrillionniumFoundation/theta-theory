# Round141 recentered-affine K4296 D0 collar

Status: **CERTIFIED / independently verified**

Round141 certifies the exact fixed-`s=0`, slope-four leaf collar

`[x_star - 2^-4296, x_star)`

on the minus side of the same Round139 `D3=0` endpoint.  The whole collar has
one strict 1648-collision first-return owner/official-word sequence.  This is
a `2^1592` width gain over Round139's `2^-5888` graph collar.

## Formal artifacts

- Producer SHA-256:
  `687aa8d868586f903951e616c9712401b4eb6b2f52832837bf59f58a3b392c28`
- Centered engine SHA-256:
  `5656f33a4974b63124bda19c56716dccb7c52ad7840741668512795560007ef1`
- Certificate SHA-256:
  `a17660dbf106611e6ec9dc680d0d7e4075dd6504f9d727415b8c365e50d0cafe`
- Certificate result SHA-256:
  `48af243b2d8a77fb3f96751fbda7dc9ffeaf2f0768f8ec76426253d07702ea3f`
- Independent verifier SHA-256:
  `1bb85fdd8dc22aa941084666b5eb9c41154f9e890f6d87c42eaf8808a4748f65`
- Verification SHA-256:
  `43770a85918cd4986e232cc1e3c401bae9ff8d0ee772b92eea8c46c3c55d4e3c`
- Verification result SHA-256:
  `8c94e2f846062cae13be0d9fb8520877cb6de7903354090df87ad084d74153a4`

## Rigorous centered model

The model has two parameter generators:

1. intrinsic leaf displacement `z in [-2^-4296,0]`;
2. the frozen Round139 deep `D0` root enclosure.

At each collision the four-dimensional physical state is represented as
`center + A*xi + remainder`.  A full interval `4x4` Jacobian on the current
state box propagates the affine generators and rigorous componentwise
remainders.  Every output center and affine coefficient is replaced by its
exact Arb midpoint; both center loss and coefficient loss times parameter
radius are explicitly added to the new remainder.

- Model ledger rows: `1648`
- Primary 8192-bit model-ledger SHA-256:
  `d8d745379c32a86e4c2c2bad6206a1eee30dc6c75b45bfc30c2979a9a91d1685`
- Secondary 12288-bit model-ledger SHA-256:
  `470ff2c7f4be3aae51c3b2c8b33d16cd834a57cfaeb03816a1604ac2decb4530`
- Worst total state-radius witness: collision `1648`, outgoing `u_x`,
  rigorously `< 2^-14`
- Terminal state-radius component bounds:
  `q_x<2^-17`, `q_y<2^-17`, `u_x<2^-14`, `u_y<2^-14`

The exact leaf enclosure remains strictly inside the selected Round116 strip
and source core.  Its far endpoint has `D3<0` with dyadic margin depth `4291`;
`D3` is strictly increasing along the entire closed model domain.  Thus the
collision-three `W[0,0]` anchor is excluded only from the exact half-open leaf
at that one collision, exactly as in Round139.

## Complete physical replay

- Collision stages: `1648`
- Full radius-four candidates per stage: `161`
- Full radius-four candidate tests: `265328`
- Collision-three analytic anchor exclusions: `1`
- Preterminal strict nonreturns: `1647`
- Terminal strict returns: `1`
- Terminal owner: `G[-7,-13]`
- Terminal destination:
  `core:e47f553e056452faa012129434cdbbb6a55cd9671a19ea04e6b8a9f43054c4c2`
- Owner sequence SHA-256:
  `c50277af0c038521b8933672d2a5a2b9035473895694c3c2878842274337cac3`
- Official sequence SHA-256:
  `f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e`
- Compact path SHA-256:
  `c37571201fa15065a7f8e4eeec9df5a79f36e077feac37a1aec7b910970e1f17`
- Homogeneity: `H0_CENTRAL x 1648`
- Incidence rank: `14 x 1648`
- Worst decision-value depth: `18`, in the full-radius-four miss
  discriminant family

The terminal `p` enclosure is approximately
`[-0.0070198,-0.0068553]`, strictly inside the destination `G:S` core's
`(-1/50,1/50)` momentum interval.

## Independent verification and hostile tests

The verifier imports neither the producer nor the centered engine.  It uses
an independent affine-state class, initial exact-leaf map, ray/circle map,
recentered remainder recurrence, and the generic fixed-section dual-number
implementation.

It reconstructed all decisions at both 8192 and 12288 bits.  Owner, official,
compact, homogeneity, incidence, C24, and worst-margin identities agree; the
secondary state-radius bounds are no worse than the primary bounds.

- Semantic mutations: `20/20` rejected
- Strict JSON attacks: `9/9` rejected
- Path-safety attacks: `9/9` rejected
- Separate process/I/O attacks: `21/21` rejected
- Hash-seed-91 producer cold replay: byte-identical certificate

## Strict scope

This is a centered intrinsic-`x` **local fixed-leaf collar**.  It does not
materialize a historical maximal component ID, historical least component
rank, Round35 restriction, natural `1e-90` short-cell rank, parent-W ID, or
image-recut rank.  It does not create Round50, Round54, or Round67 objects.

Gate5 remains `10/18`, the complete-block count remains zero, and CM2 remains
`NO-GO_FOR_CLAIM`.
