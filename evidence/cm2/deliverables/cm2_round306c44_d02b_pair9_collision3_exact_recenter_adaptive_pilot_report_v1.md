# CM2 Round306 C44 D02-B pair-9 collision-3 exact-recenter pilot report v1

Status: **PASS READ-ONLY PILOT; ZERO FORMAL CREDIT; NO AUTHORITY WRITE**.

## Frozen implementation and replay

- Source:
  `deliverables/cm2_round306c44_d02b_pair9_collision3_exact_recenter_adaptive_pilot_v1.py`
- Source SHA-256:
  `18ba0d94ab8875c2cbbf8c03f727e5fc606dd8f17953df63b480dee766872d28`
- Runtime: `python-flint 0.9.0`, Arb precision 384 bits.
- Self-test: `12/12` fail-closed tests passed.
- Pilot bounds: additional depth 6, at most 1,024 nodes per physical side.
- Canonical pilot stdout SHA-256, reproduced independently:
  `ee824bd571aaac140268ec32ce17ae3c9370677950df868659de52b3bd11ecfe`.

No runtime authority pointer was touched.  The pilot wrote no candidate,
receipt, audit or authority object and assigns `formal_credit=0`.

## Exact pair-9 result

The representative and reflected physical sides received distinct, newly
minted collision-2-to-collision-3 handoff identities:

- representative:
  `c44-collision3-handoff:b2ae773935a4b8fbf77d78b8e91be472fe75e989fa86ef99cc171e1072569abd`;
- reflected:
  `c44-collision3-handoff:849896b0213a45e2d866c38922bbeaa361d1eb3cdf46936085eeacee72248991`.

Each side independently produced:

- 99 visited adaptive nodes;
- 49 exact rational splits;
- 50 prefix-free leaves;
- relative Kraft sum exactly 1;
- 18 strict collision-3-live leaves handed to collision 4 with complete
  zero-credit occurrence evidence;
- 32 bounded-pilot unresolved leaves, each carrying an exact next p-axis
  split/recenter decision and the failing discriminant witness.

Across both sides this is 36 strict live collision-4 handoffs plus 64 explicit
unresolved next decisions.  No leaf was credited as excluded merely because it
disagreed with a C35--C37 template.

## Evidence discipline

Every strict live leaf binds a fresh physical occurrence and its exact
collision-3 evidence: owner, discriminant, isolated root/order, official word,
chart, wall/order margin, homogeneity, incidence, core/C24 margin and terminal
decision.  A new collision-4 handoff is derived from that occurrence evidence.

The reflected template is used only through its explicit C37 horizontal
reflection assertion and its exact C36 margin-binding row.  Template owner,
word or chart values are diagnostic priorities, never occurrence proof.

The following conditions remain nonterminal and receive no credit:

- unresolved candidate decision or root order;
- nonstrict discriminant, wall, order or homogeneity margin;
- incomplete incidence, face, endpoint or corner ownership;
- incomplete core/C24 margin;
- pilot depth/node budget exhaustion.

## Next batch contract

The same engine may be expanded over the 7,463 collision-3-ready representative
rows only if it preserves pair/ambient/side occurrence identity.  Both physical
sides must be independently bound.  Adaptive split faces, endpoints and corners
need separate canonical-owner ledgers, and every parent must independently
rebuild prefix-free Kraft conservation and reflection transport.

Accepted terminal dispositions remain limited to strict exclusion, connection
to a known component, or a strict cemetery/disconnected certificate.  A live
collision-3 occurrence continues to collision 4; it is not a D02 terminal.

D02 remains blocked, D03 unauthorized, and CM2 remains
`NO-GO_FOR_CLAIM`.
