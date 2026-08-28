# C47 D02-A pair-668 exact-route adaptive feasibility spike v1

Date: 2026-08-11 (Asia/Shanghai)

Status: `PASS_READ_ONLY_C47_PAIR668_EXACT_ROUTE_ADAPTIVE_FEASIBILITY__PREFIX_FREE_PENDING__ZERO_CREDIT`

This is a numerical-oracle feasibility probe, not a producer, audit, D02-A
closure, or promotion.  It wrote nothing below `.cm2-runtime` and assigned no
ambient, terminal, whole-parent, D02, or formal credit.

## Frozen inputs and deterministic task

- C46-A source SHA-256:
  `365432e96f2c287ef3c5497b7d15e01a80775f52d8cf5b71810d6f4c0e4442ea`
- C46-A 64-shard plan object SHA-256:
  `7d004f59282dee21a28db0cd0b727a9045f4befce207c96be4efb07d1399c9bf`
- C41 source SHA-256:
  `3fbf6cec247903d6e6ba147d4d06e912638b1472b74adc8311323c554e6e5bde`
- Installed C42 seal object SHA-256:
  `b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460`

The probe selected the lexicographically first of the 43 frozen pair-668
`OWNER_PREREQUISITE` tasks:

- task binding:
  `64400932860d6f224a90204e56a5614bf982eb3a1b87f37f04b86ba112a3ff9f`
- C41 ambient:
  `c41-ambient:a828b4c95611e3e12ab8b3131f19f801ce8e1f1541106010ea94f34ba981a351`
- C41 C2 primary:
  `c41-c2-outer:4037ee276cf83fdf894f563b3967beba1dc5889764f951a8b8d2c4441b3258e4`
- C40 source:
  `c40-leaf:5f9aa773a13633d0cb6187596d47858afa6b6e08e52bcdbd4cdd3479513513a0`
- frozen path: `010111011`; the task unblocks sole-deficit pair 97.

The fresh C41 route replay reproduced the exact frozen ambient row hash,
primary row hash, graph/endpoint/incidence counts, boundary row, and all four
face and four corner IDs before any new split.

## Actual adaptive route

With an event budget of four, C41's exact route and exact split primitives
needed only two splits; no mathematical fixed-depth cutoff was used:

1. Relative root `""`: C2 status `WALL_ENDPOINT`; split.
2. Relative `0`: strict `EXCLUDED_C40_COLLISION2_OWNER_MISMATCH`; retained
   pending because the complete two-side terminal certificate is absent.
3. Relative `1`: C2 status `WALL_ENDPOINT`; split.
4. Relatives `10` and `11`: both strict owner mismatch; retained pending for
   the same certificate reason.

The final zero-credit frontier is `0, 10, 11`; it is prefix-free and has exact
relative Kraft sum `1/2 + 1/4 + 1/4 = 1`.  The checkpoint object SHA-256 is
`6ed628697caf0feb81a0dc5428e1a27bf472c2ec59496556dcffa60ba5ddba5e`.

Every evaluated residual node records the C1/C2 result hashes, normalized
graph rows, endpoint rows, pair incidences, boundary, faces, corners, and their
owner states.  This selected B0 task has zero normalized surfaces, endpoints,
and pair incidences.  Its first route blocker is exactly
`C41.route_at_path.c2_status=WALL_ENDPOINT`; the first explicit global-owner
blocker is exactly
`boundary.global_sibling_adjacency_and_half_open_owner_complete=false`.
All four face owners and all four corner owners are likewise unresolved at
that residual node.

## Exact stop

C43 cannot supply the missing certificate: its rejected, zero-credit candidate
has exact sources only for pairs 592 and 715 and source-preflight scope only
for 97, 211, 592, 664, and 715.  It has no exact source or global-owner
certificate for pair 668.

Although all three final representative-side boxes route to strict owner
mismatch, C47 emits no candidate exit.  The first terminal-certificate field
not supplied by the frozen helpers is
`physical_sides.REFLECTED.independent_exact_route_certificate=absent`; a
strict terminal margin is also absent.  These leaves therefore remain
`RESUMABLE_PENDING_ZERO_CREDIT` rather than being promoted by inference or by
the resource budget.

The narrow next implementation step is an independently replayable reflected
occurrence adapter plus exact terminal margins, followed by global
boundary/face/corner owner reconstruction.  Only after every required field is
present may a zero-credit candidate exit be emitted for later independent
verification.

## Validation transcript

- Source SHA-256:
  `28c7eb805729f4ab8d5adaf5fac211394616877b5e08c39bd9f288c1f7640a1f`
- `py_compile`: PASS.
- Self-test: 10/10 PASS; object SHA-256
  `f454fe823c964837971414c901be73cdac42f8bb6d33d17e1622830cad6d7fd1`.
- Read-only budget-4 probe: PASS; object SHA-256
  `c57bc2711dbc7dad13178643b26f5722d48db703598d3238bfd98aa254e4f9f4`.
- C42 candidate pointer, audit pointer, and seal file hashes remained
  `fbc5dd3c...7f07`, `59aca53c...36e5`, and `0e5a7605...312d`.
- All three C43 authority nodes remained absent; no producer or auditor ran.
