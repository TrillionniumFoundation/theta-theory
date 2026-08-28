# Round292 R287 registry-overlap cold replay

## Producer artifacts

The frozen producer artifacts are:

- producer:
  `69078405b39dff3e924630ffbc9fbe35c14e4114e1e33c946b9ab44fe26e8c4c`;
- result:
  `f3887e75f4ef62459b75d8c77eee4781ec14f57651b4feb09b8d7ca8e372c508`;
- deterministic gzip ledger:
  `8863126e88ffd30438938d0a8bdb577f5928ae81f3f17f4b506829d59103a8ab`;
- embedded result object:
  `f6bc26c2a7f674901e411342ce388b5c2a9e8facc9a253ce244375bcf7e47372`.

The ledger has `22,820` rows and rows SHA-256
`556bd0ed95709fe43ff7837522d8729582ce0e7c9679879a57365f864f6ba055`.

## Independent verifier replay

The standalone verifier was executed twice:

```text
PYTHONHASHSEED=292071 python3 -B \
  deliverables/cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_verifier.py \
  --seed 292071 \
  --output /tmp/round292_overlap_verification_292071.json

PYTHONHASHSEED=292929 python3 -B \
  deliverables/cm2_round292_source_g_r287_registry_overlap_exhaustion_probe_verifier.py \
  --seed 292929 \
  --output /tmp/round292_overlap_verification_292929.json
```

Both runs returned:

```text
PASS_INDEPENDENT_CACHELESS_ROUND292_R287_REGISTRY_OVERLAP__
421804_REGISTRY_ROWS__10020_SOURCE_UNIONS__10668_SOURCE_CELLS__
1564_EXACT_OVERLAPS__11852_EXACT_REFINEMENT_CELLS__
9404_REFINED_NEW_SUPPORTS__UNRESOLVED_ZERO__ZERO_CREDIT
```

The two verification files are byte-identical:

- verifier source SHA-256:
  `9efd78054cdde8172b016a684951395f1ca96958412122034dfc1971312ea010`;
- verification file SHA-256:
  `7088e4f0927100e3c2b36f164e4f64e7b7aa0db5f81b4201c3967f16ba07ddfd`;
- embedded verification-object SHA-256:
  `608a3d0e93df4f4849f8efb83715ac04d7317d13f2732e101d5d3c7ef5ae9a39`.

The seed label and external hash seed do not enter the canonical verification
object.

## Independent checks

- frozen preserved occurrences rebuilt: `126,468`;
- conditional Round288 new-atom candidates rebuilt: `295,336`;
- complete conditional base/atom registry rebuilt: `421,804`;
- registry IDs injective: PASS;
- Round287 support unions rebuilt: `10,020`;
- Round287 exact source cells rebuilt: `10,668`;
- registry shortlist comparisons: `295,720`;
- exact positive overlaps: `1,564`;
- overlap-incident unions: `920`;
- exact `(t^2,p,s)` partition cells: `11,852`;
- occupied unique-target cells: `1,600`;
- multi-target occupied cells: `0`;
- uncovered cells: `10,252`;
- local exact-face connectivity rank: `848`;
- refined connected support candidates: `9,404`;
- fully covered / partially covered / untouched unions:
  `616 / 304 / 9,100`;
- exact transformed volume conservation: PASS;
- pairwise shortlist comparisons: `231,880`;
- same-union positive overlaps: `0`;
- distinct unresolved positive overlaps: `0`;
- exact candidate result equality: PASS;
- exact candidate ledger equality: PASS;
- exact deterministic gzip-byte equality: PASS;
- every row independently closed by SHA-256: PASS;
- targeted re-signed attacks rejected: `31/31`;
- coordinated row→ledger→result re-sign attack rejected: PASS;
- alternate gzip header with identical decoded object rejected: PASS;
- deterministic gzip ledger passes `gzip -t`: PASS;
- all formal credits: `0`;
- D02: `BLOCKED`;
- CM2: `NO-GO_FOR_CLAIM`;
- `Jx/Jy` same-point glue credit: `0`.
