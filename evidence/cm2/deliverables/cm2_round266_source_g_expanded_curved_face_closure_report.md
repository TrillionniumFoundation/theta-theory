# CM2 Round266: expanded curved full-face closure

## Certified result

Round266 reconstructs and closes all `2,652` curved R174--R204/R208
full-signature face candidates left fail-closed by Round265.

- all `2,652` complete faces are strict `MATCH` at canonical depth zero;
- all carry exact positive common-face area;
- all have two explicit strict inward 3D corridors (`5,304` total);
- `1,476` rows were already internal and `1,176` crossed components;
- the distinct cross-component pairs yield `588` rank reductions and `16`
  independently certified redundant pairs;
- the quotient changes `63,812 -> 63,224`;
- component, occurrence, key, virtual-node, and member frontiers are rebuilt
  at `63,224 / 126,468 / 116 / 133,284 / 259,752`.

Exact accepted face area sums to `5728631/1638400000`; exact inward corridor
volume sums to `302487513/3355443200000`.

Certificate result SHA256:
`39bc6d46bc7b83e73af0cc3466b79196defa4a2518e1db704b7a3f61f2e2173b`.
Complete certificate SHA256:
`2d30be104dc522ebb1664129894acf851180b9e5f51dd8471c33137447b599bf`.

## Independent verification and reproducibility

The independent verifier pins the producer as inert bytes, rebuilds the
complete candidate pool from the frozen R174/R204/R208 geometry, replays the
hash-pinned R259/R260 evaluators at fixed 256-bit Arb precision, and rebuilds
the DSU plus every frontier before opening the 934,776,249-byte candidate.
The complete expected object matches with `PASS_INDEPENDENT_ROUND266`.
All `10/10` semantic attacks are rejected.

Producer seeds `266071` and `266929` are byte-identical.  Independent
verification SHA256:
`a6436c716cbbe74f0195e2d87f4084a28ca2a2e27b9fe5eeb98b6835df92b75b`.

## Strict non-promotion

Complete full-signature face closure is glue but is not component
maximality.  Maximal assignments remain `0/63,224`, exhausted fibres
`0/116`, global dispositions `0/224,580`, Jx/Jy same-point credit `0`,
Gate5 `10/18`, D02 blocked, and CM2 `NO-GO_FOR_CLAIM`.

Remaining channels are the Round267 lower-stratum lineage, `184,452`
Round182 closed leaves lacking side-specific exact-key signatures, `152`
positive-area true source-seam owner/shadow candidates, and `880`
positive-volume chart guards requiring reverse rechart.
