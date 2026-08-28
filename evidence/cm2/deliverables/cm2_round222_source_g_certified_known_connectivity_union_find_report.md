# CM2 Round222 — source-G certified known-connectivity union-find

Date: 2026-07-27

## Verdict

`CERTIFIED_KNOWN_CONNECTIVITY_LOWER_BOUND__NOT_MAXIMAL_PHYSICAL_COMPONENTS__ZERO_PROMOTION`

Round222 independently reconstructs the current proved sheet-edge graph from
the pinned Round211, Round214, Round217, and Round219 boundary.  It certifies a
lower-bound connectivity quotient, not the maximal physical-component
equivalence relation.

## Exact census

- Round211 sheet rows: `17,716`;
- Round214 reconstructed safe pairs: `5,935`;
- Round217 exact TRACE pairs: `448`;
- Round219 TRACE pairs: `6,588`;
- cumulative Round217+219 unique TRACE pairs: `7,036`;
- current proved-edge incident sheets: `15,248`;
- isolated sheets under the proved edge set: `2,468`;
- certified known-connectivity blocks: `7,640`;
- unresolved/nonedge frontier accounts: `7,280`;
- mapping failures, false edges, and self loops: `0`.

The ordered known-connectivity membership SHA256 is
`715008789165502798276611bd763a8f6cf3160d9c74d8559a63c3cf7e467cd9`.

## Independent verification repair and result

The first hostile replay found that the verifier did not bind the aggregate
`incomplete_exact_contact_partition_still_required` flag.  The second replay
found that it also did not bind
`producer_outcome_or_oracle_dependency`.  Both were verifier weaknesses, not
accepted changes to the certificate.

The verifier was hardened to bind the complete `7016/28/236` frontier census,
the `6120+896` incomplete-exact decomposition, all 236 cross-block unresolved
pairs, the Round214 reconstruction/trust contract, and outcome blindness.  Its
strict JSON reader now rejects non-integral numeric tokens and invalid Unicode
surrogates.

The final independent run passed and rejected:

- `15/15` genuinely re-signed semantic attacks;
- `16/16` strict JSON attacks; and
- `10/10` filesystem/path/file-object attacks.

It checked all `7,036` edge rows, `7,640` block rows, `17,716` assignment
rows, and `7,280` frontier rows without importing or executing the producer.

## Frozen hashes

- producer: `58b5b63dc25a44c7d2279d54b1eb842d88cc61e3abd6c31f889688d3d2801a22`;
- certificate: `700174fc3bdfa57805ce8a2a97630fd9e6183ce5aee443c430f14db6184e9e9e`;
- certificate result: `1b80b806fa6716135480a500ff1248cc8dfabb37af7b3802ba50ba1bf62b493e`;
- verifier: `21c75e4349b313b88eea6f80cc2ad68e531dee766f131c907b74bc6ecca079bd`;
- verification: `99db3624c076165558f50f33b2d019f4be0a35335f943dc1567534e79b104461`;
- verification result: `ef3a2e4b4c866e972db058ac4ad1c28dc8ea800582a3ebbcd8e59e9e33a0bb21`.

## Strict boundary

The 7,640 blocks are not claimed to be maximal physical components.
Physical-component, whole-origin, global-fibre, and exact-key-disposition
credits remain zero.  D02 remains `BLOCKED`, Gate5 remains `10/18`, and CM2
remains `NO-GO_FOR_CLAIM`.

