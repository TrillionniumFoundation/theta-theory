# CM2 Round306 C43B0 eligibility superseding addendum v1

Date: 2026-08-11 (Asia/Shanghai)

## Supersession and authority boundary

This addendum supersedes the target-set and projected-census portions of
`cm2_round306c43b0_five_sole_deficit_formal_closure_contract_and_audit_design_v1.md`.
The earlier closed-box, reflection, lower-strata, Kraft, manifest, no-authority,
and independent-audit requirements remain in force where they are compatible
with this narrower tranche.

This is a read-only eligibility audit. It creates no candidate, receipt, audit,
token, seal, pointer, or formal credit. The installed input remains C42 f1:

- candidate object
  `a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2`;
- independent-audit object
  `85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c`;
- authority-seal object
  `b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460`;
- authority-seal file SHA-256
  `0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d`.

The installed formal baseline is still 574 paired coarse cells, 287 of 862
whole representatives, 575 representatives remaining, and 1,150 unresolved
paired continuations.

## Independent global-incidence method

The eligibility scan read all 91,879 installed C41
`routed_ambient_cells.jsonl.gz` rows and used exact rational arithmetic. For each
target source side, it collected every longitudinal endpoint of every incident
closed ambient box, clipped those endpoints to the side, sorted the exact
breakpoints, evaluated every open segment, and separately evaluated every
breakpoint. It performed the same census on `closed_representative_box` and
`closed_reflected_box`.

The canonical owner key is the installed C41/C42 rule

`(source path, pair index, C41 ambient id)`.

Reflection changes exact geometry but does not invent a new sortable path. The
reflected census therefore uses the same canonical source-path key, as C41/C42
do. A path-relabelled reflected owner order would be a new, unauthorized
semantic rule.

The effective terminal set for this tranche is:

1. every C41 `TERMINAL_EXCLUDED` ambient row;
2. installed C42 pair 391's effective terminal ambient row; and
3. candidate-effective terminal rows for pairs 592 and 715 only.

Pairs 97, 211, and 664 remain residual while eligibility is evaluated. The scan
uses global half-open ownership: a non-owner incident may remain residual only
if its duplicate boundary role is explicitly excluded and the unique canonical
owner is terminal. C42's stronger all-incidents-terminal condition is sufficient
but is not necessary under this canonical-owner partition. A formal producer
must materialize every incident and every non-owner exclusion; it may not omit a
residual non-owner from the ledger.

## Superseding eligibility result

| pair | result | exact global-owner reason |
|---:|---|---|
| 97 | **REJECT, zero credit** | Representative `t_upper` and its two endpoint corners are canonically owned by residual pair 668; the reflected obstruction is the Jy image. |
| 211 | **REJECT, zero credit** | Representative `t_upper` is owned by residual pair 496; `p_upper` is owned by residual pair 783; three corners inherit those residual owners. Reflected sides carry the same blockers. |
| 592 | **INCIDENCE-ELIGIBLE** | Every representative/reflected exterior open segment and corner has canonical owner pair 592 path `000000000`, which becomes terminal in this tranche. |
| 664 | **REJECT, zero credit** | Representative `p_upper` and both `p_upper` corners are canonically owned by residual pair 695; the reflected `p_lower` carries the same blocker. |
| 715 | **INCIDENCE-ELIGIBLE** | Every exterior owner is either candidate-terminal pair 715 path `101010101` or already-terminal pair 715 sibling path `101010100`. |

`INCIDENCE-ELIGIBLE` is deliberately weaker than formal closure. Pairs 592 and
715 receive credit only after their representative and reflected closed leaves,
all exterior restrictions, all corners, and the internal split face plus its
endpoints are directly recomputed and certified terminal.

## Exact rejection witnesses

### Pair 97

Representative `t_upper`, over
`p=[-801/2048,-25/64]`, has canonical owner:

- pair 668, path `101010101`;
- ambient id
  `c41-ambient:f7356c5fae21a4fcdcf9a92b6c79f40c0d53e1409c0f8611e51b495bb2a5cbe5`;
- row SHA-256
  `a74c75fd37422428cf2480c6e213ea831192f91e3837131d725eb541534d289d`;
- C41 disposition `RESIDUAL_OUTER`.

At the two `t_upper` endpoints, the owners are residual pair 668 paths
`101010100` and `101010101`. The former has ambient id
`c41-ambient:90a3d56f196453fd2808afc7d557f371511b2602be74ab8e6920d042d149711e`
and row SHA-256
`f7a17bff728c90bc32489afd931db1486333a03d9ed832a7d3c8c1e70cfba7e9`.
The reflected `t_lower` and its corresponding corners reproduce the same two
residual source-path owners. Closing pair 97's interiors cannot close strata
owned by pair 668, so pair 97 must receive zero credit.

### Pair 211

Representative `t_upper`, over
`p=[-1057/2048,-33/64]`, has residual canonical owner:

- pair 496, path `010101010`;
- ambient id
  `c41-ambient:dca11279c7e655cdf2a4f416ee808982969f7db668eb052adb2f311a8be6b420`;
- row SHA-256
  `ed7fd1aef482c1f98024c6ffb26bc551c9fbe6ac80d44f55311d8d0e2272f269`.

Representative `p_upper`, over
`t=[209391/512000,6549/16000]`, has residual canonical owner:

- pair 783, path `101010101`;
- ambient id
  `c41-ambient:103421275cefb13d4c9cf57ba7eb24d515274bc6549378e55781d06d3c26d39b`;
- row SHA-256
  `0c485027b0b16ddf3dd3b11c07a854c3dbe314c28e08cfd3b364714e4718e012`.

The affected corners are owned by residual pair 496 paths `010101000` and
`010101010`, and residual pair 783 path `101010100`. Jy carries these obstructions
to reflected `t_lower` and `p_lower`. Pair 211 therefore receives zero credit.

### Pair 664

Representative `p_upper`, over
`t=[5133/16000,164433/512000]`, and both of its corners have canonical owner:

- pair 695, path `000000000`;
- ambient id
  `c41-ambient:501d5fac72deae8167d270eef6d3377b4b156e18fe9523b8767c32975054dfd9`;
- row SHA-256
  `6f91a95a08bbc7f71f9dfcf5d30e82e9ae7ddacc39a485a543919655d85457a6`;
- C41 disposition `RESIDUAL_OUTER`.

Reflected `p_lower` and its corners have the same canonical source owner. Pair
664's own direct terminal leaves cannot discharge pair 695's owned stratum, so
pair 664 receives zero credit.

## Complete eligible exterior census

No eligible exterior side contains an internal longitudinal breakpoint: every
side has exactly its two endpoints and exactly one open segment. Thus each pair
has four representative plus four reflected open-segment obligations and four
representative plus four reflected corner obligations. A C42-style paired
ledger may encode these as four face rows and four corner rows per pair, but both
orientations must be explicit.

### Pair 592

Target effective owner:

- pair 592, path `000000000`;
- ambient id
  `c41-ambient:1155af61875379b5b198bfbe3e3369548d256f096ca0c467dc847e9340df8cee`;
- row SHA-256
  `bf089245fa0f96196014cbd425b0b3d3e265b0350477779f731b32dc05f8985e`.

Representative source box:
`t=[1593/3200,255057/512000]`,
`p=[113/128,1809/2048]`. Reflected source box has the same `t` interval and
`p=[-1809/2048,-113/128]`.

All eight oriented open faces and all eight oriented source corners have the
target above as canonical owner. Some incidences contain residual pair 190 rows,
but their paths start `010...`, while the canonical target path starts `000...`;
they are non-owners and must be explicitly recorded as duplicate-boundary
exclusions. There is no residual canonical owner.

The adaptive cover has exactly two representative leaves split at
`p=3617/4096`, with the reflected split at `p=-3617/4096`. Formal eligibility
still requires direct closed restriction of both split lines and their four
oriented endpoint obligations, plus exact transport of the lower-bit ownership
role under Jy.

### Pair 715

Candidate-effective target owner:

- pair 715, path `101010101`;
- ambient id
  `c41-ambient:dbe6919f75a7e46a66b98e9a34302b051595f3ccef428e3965876d382a75545e`;
- row SHA-256
  `24b8a1114e0bda5b0ff4d88b8f7daddfd6b009724fb2e418ea9ac52de42df349`.

Already-terminal sibling owner:

- pair 715, path `101010100`;
- ambient id
  `c41-ambient:9bfb086caef5f2f362b91bb4ae5a64ff8985d4a2cc38333f6ed1868b41c68e91`;
- row SHA-256
  `0d5e15cf1e5375bd885f42ea754bf2da7d999af4192a87b721ca19f64478a7e6`;
- C41 disposition `TERMINAL_EXCLUDED`.

Representative source box:
`t=[1239/3200,99297/256000]`,
`p=[-1921/2048,-15/16]`. Reflected source box has the same `t` interval and
`p=[15/16,1921/2048]`.

- Representative `p_lower` and its two corners are owned by the terminal sibling;
  representative `p_upper`, both `t` faces, and the remaining corners are owned
  by the candidate-effective target.
- Reflection swaps the geometric `p` sides: reflected `p_upper` and its corners
  are owned by the terminal sibling, while reflected `p_lower`, both `t` faces,
  and the remaining corners are owned by the target.

Some `t_lower` incidences include residual pair 555 path `111111111`; it is a
non-owner because both pair-715 canonical paths start `101...`. It must remain in
the complete incidence ledger with its duplicate-boundary exclusion role.

The adaptive cover has exactly two representative leaves split at
`t=198417/512000`; the reflected split uses the same `t` coordinate. Formal
eligibility still requires direct closed restriction of both oriented split
lines and their endpoints.

## Legal parent delta and corrected projected census

Subset credit is legal only as an exact two-row delta applied to a complete
rebuild of all 862 installed C42 parent rows. A two-row parent ledger by itself
is not sufficient.

- The 860 unchanged rows, including pairs 97, 211, 391, and 664, must bind their
  exact installed C42 row hashes and remain semantically unchanged.
- Pair 592 and pair 715 each start at terminal fraction `511/512`, add exact
  representative fraction `1/512`, end at terminal fraction `1` and unresolved
  fraction `0`, and receive paired C34 credit 2 only after all closed-strata
  obligations pass.
- Per-pair relative Kraft is exactly 1; per-pair absolute gain is exactly
  `1/512`; pair 391 remains unchanged.

If both eligible pairs pass formal production and independent audit, and only
then, the corrected candidate census is:

| quantity | installed C42 | corrected C43 candidate |
|---|---:|---:|
| whole representatives | 287 | 289 |
| remaining representatives | 575 | 573 |
| paired coarse cells terminal | 574 | 578 |
| earliest-prefix excluded | 75,386 | 75,390 |
| typed-event graph | 296 | 296 |
| unresolved | 1,150 | 1,146 |
| total | 76,832 | 76,832 |

The result must still state `unresolved_zero=false`,
`D02=BLOCKED_BY_1146_COMPLETE_R1648_CONTINUATIONS`, `D03=UNAUTHORIZED`,
`D04=NOT_MINTED`, `Gate5=10/18`, and `CM2=NO-GO_FOR_CLAIM`.

## Auditor acceptance rule

The independent C43 auditor must derive and require the exact credit set
`{592,715}`. It must reject any candidate that credits pair 97, 211, or 664,
even if their two-dimensional child interiors route to exclusions. It must also
reject omission of any residual non-owner incident, a reflected path-order
change, a missing direct face/point restriction, a two-row-only parent ledger,
or any projected census other than 578 paired / 289 representatives / 1,146
unresolved.

Until that auditor passes a stable candidate and a later independent installer
commits it, the formal authority remains C42 at 574 paired / 287 representatives
/ 1,150 unresolved.
