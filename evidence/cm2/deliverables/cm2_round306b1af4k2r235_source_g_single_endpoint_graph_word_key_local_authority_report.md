# CM2 Round306B1AF4K2R235 — hardened local Round235 authority

## Verdict

`PASS_R235_SINGLE_ENDPOINT_LOCAL_GRAPH_WORD_KEY_PARTITION_AUTHORITY_ONLY__16_DOUBLE_ENDPOINT_FACTORS_BLOCKED__ZERO_GLOBAL_FORMAL_CREDIT`.

The package grants the narrowest supportable authority: exactly `38,328`
Round235 rows certify a local single-endpoint graph, strict first/last wall-word
insertion, and the corresponding official exact-key partition on the two open
sides.  This is row-local partition authority only.  It is not normalized
full support, physical incidence/equivalence, representation pullback, G2
authority, B1A, B2, component maximality, fibre completion, or CM2.

The complete endpoint frontier is `38,344 = 38,328 + 16`.  The remaining `16`
rows have both endpoint factors active (`8` X-wall and `8` Y-wall rows, `32`
active-factor instances) and remain `BLOCKED` pending a two-factor endpoint
arrangement.  They receive zero local partition credit.

## Exact census and selected tables

- active single factors: source `552`, target `37,776`;
- transition tokens: X+, X-, Y+, Y- each `9,582`;
- distinct candidate official exact keys: `92`;
- selected R234 endpoints: `38,344 / 38,376`, ordered rows
  `4baadb2e...04c7`;
- selected R234 released descendants: `10,832 / 12,200`, ordered rows
  `65fe0c3c...fc7d`;
- selected R220 interfaces: `2,232 / 13,076`, ordered rows
  `ef9ceaaf...61dd7`;
- selected R179 resolved siblings: `2,232 / 17,192`, ordered rows
  `b6750b72...fffc`;
- frozen R235 single rows: `38,328`, ordered rows `e9a37945...731`;
- frozen R235 double-deferred rows: `16`, ordered rows `52e01cc8...572`.

Every one of the `38,344` authority-ledger rows contains its full canonical
input commitment (R234 endpoint, R220 interface, R179 sibling, all applicable
R234 released descendants, and the held engine/registry chain), every source
row SHA-256, the old output-row SHA-256, and an input-bound conclusion digest.

## Old-package defects closed

The old four-member manifest did not include its report or cold replay; those
files were mistakenly written under `deliverables/deliverables/`.  The old
producer/verifier also lacked manifest-first package validation, held-FD
two-pass/final path revalidation, per-row canonical input commitments,
post-decode 8 MiB canonical-row enforcement, duplicate/nonintegral/NaN JSON
rejection, type-strict bool/int equality, a structured mutation suite, and a
sealed no-write proof.  Its `lstat` followed by pathname `read_bytes` admitted
a TOCTOU window.

K2R235 closes these engineering defects with manifest-first sealed replay,
held descriptors, exact sizes and SHA-256 pins, two hash passes and a final
FD/path/hash pass, symlink/hardlink rejection, strict JSON, an enforced
`8,388,608`-byte final decoded-row cap, deterministic gzip (`mtime=0`), direct
write-once publication without `TMPDIR` or spill, type-strict equality, and an
independent verifier that never imports or executes the producer.

## Frozen core hashes

- producer: `4345e341120089b854ab57809f4b4dd58a017c89a0babac28628af5dd70f074e`;
- row ledger: `904d6504cb3263e29f9bb93d1935ce959d823d026192589a34932665041109f5` (`28,926,015` bytes);
- result file: `ff907604d7b992d4206d6847481ad1988efb2dc428c74e22f0e071e8caf65f8a`;
- result object: `066abcdcbb2da3a7b2e35bf4e9b027676d17f6f1276bf52d603205954e8330ee`;
- independent verifier: `931bc3ce11a2235d036e1ec35bbf1168726139a950c42c404c20cf993c88e0b0`;
- attack suite: `6595b5ccf0f2fa8437759b6960eb02ae3f6991d48784ec65e790f64626155089` (`13/13`);
- verification file: `f039ed8d185f155191e323cadf9f2a0c1c33d929058b76d178e12e54bc9790b7`;
- verification result: `74ba8a89b0758d7b800bbcaa6b108faf35413af2d9d51902ddfdededbb1a8cb5`.

## Nonpromotion

Normalized full support, physical incidence/equivalence, representation
pullback, G2, B1A, B2, maximality, fibre, and CM2 credits are all exactly zero.
CM2 remains `NO-GO_FOR_CLAIM`.
