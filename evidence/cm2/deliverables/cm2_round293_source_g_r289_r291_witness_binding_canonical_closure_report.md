# CM2 Round293 — R289/R291 witness-binding canonical closure

## Verdict

Round293 is the superseding canonical closure of the Round292 R289/R291
witness-binding audit.  It fixes the result-object JSON round-trip defect and
adds the previously missing full mathematical independent verifier.

The new producer and verifier both preserve the underlying census exactly:

- Round289 relation-binding rows: `9,528`;
- Round291 physical-witness rows: `113,452`;
- Round291 absence/no-binding rows: `28,016`;
- Round289 unresolved physical-incidence subcells: `396`;
- Round291 unresolved positive-`t` retained-owner witnesses: `576`; and
- every occurrence, alias, component, seam, DSU-rank, maximality, fibre,
  disposition, and `Jx/Jy` glue credit: `0`.

Accordingly this is a **ZERO-CREDIT fail-closed audit**, not a mathematical
promotion.  Gate5 remains `10/18`, D02 remains `BLOCKED`, and CM2 remains
`NO-GO_FOR_CLAIM`.

No Round292 artifact was modified.  Their byte commitments remain:

- producer:
  `72ff71aa4e74c2d4274afb760879d11d63ffae09dbfe9e6773519ee7a5abc163`;
- result file:
  `07ced5c6e0f5c06b4f22019deda6c770341b264b654fe6ddb9a8f44ec68472ca`;
- ledger:
  `5602f3bd5860ca70277f820e36b602273d7253073c4c4ba6111f6eff2f500570`.

## Canonical JSON defect and repair

The Round292 build formed
`Round289.tail_directed_endpoint_target_count_histogram` with integer keys.
Before serialization, `sort_keys=True` ordered those keys numerically:

```text
3, 13, 81, 82, 90, 96, 282
```

After JSON parsing, the keys are strings and canonical sorting is
lexicographic:

```text
"13", "282", "3", "81", "82", "90", "96"
```

Thus the Round292 embedded in-memory commitment
`919634dc108d9bf06c6b40209b8245f223ae52e2909fb76c71a1e9c25f291db0`
does not equal the canonical digest recomputed from its persisted JSON
semantics,
`ea99ee814e41fe22ea55ba04682fc44d3a5538aab1e41ccd7a154160a538c670`.

Round293 recursively normalizes every mapping key to a string before any
enclosing commitment is computed, rejects normalization collisions, writes
canonical JSON, reparses the exact bytes to be written, removes
`result_sha256`, and recomputes the digest from that parsed value.

The resulting persisted closure is exact:

- embedded Round293 result-object SHA-256:
  `35f50db2bc6e245d7c391581da33b471bfbe556b16a90dd8b8b2593568a6e870`;
- recomputed from persisted JSON:
  `35f50db2bc6e245d7c391581da33b471bfbe556b16a90dd8b8b2593568a6e870`;
- result file SHA-256:
  `36459f330fdd577031f35d8d8f7e93cf3ebc96bef049a4f687b22c9e39e91613`.

## Independently reconstructed mathematics

The standalone verifier does not import or execute either the Round292 or
Round293 producer.  It does not use the Round292 result or ledger, nor the
Round293 candidate result or ledger, as an expected-value oracle.

Before opening either Round293 candidate artifact, it reconstructs the
complete expected ledger and result directly from the pinned frozen inputs:

- Round182 clipped graph/pair arrangement;
- Round204 local replacement regions;
- Round275 reverse-rechart regions;
- Round279 collar atoms;
- Round287 terminal dispositions;
- Round288 atom occurrence dispositions;
- Round289 seam-tail relations;
- Round291 lower-stratum dispositions; and
- Round292A full-registry overlap refinement.

The reconstruction independently rebuilds all atom maps, terminal support
cells, exact seam-facing rectangle partitions, target-reference unions,
lower-stratum physical incidences, absence rows, exact rational areas, row
hashes, table hashes, and summaries.  Only then are the candidate files
opened and required to equal the complete independently built objects and
their canonical bytes.

The independently recovered table commitments are:

- Round289 rows:
  `b78346f576d3742cec9238ab5704c4bcc8c5374a2779fc80e24b8f5caa17fbf9`;
- Round291 physical rows:
  `e2ca331f0bb325729e5e5fb6ad8227e1cd3057bcea1900315594bff6ebbd8b8c`;
- Round291 absence rows:
  `3922acf4bb087f352d82d8cbe3ae8c0beaa2117cbaba7464ce9ddd752a0e5790`.

The deterministic Round293 gzip ledger SHA-256 is
`0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c`.

## Unresolved obligations retained

Round289 retains `396` uncovered exact subcells with total exact open
`(p,s)` area `351/409600`.  They affect `20` directed endpoints across `16`
true-seam patches.  They are not converted into occurrence bindings or seam
edges.

Round291 retains `576` positive-`t` owner/shadow witnesses whose retained
open volume has no issued registry occurrence.  In addition, all `28,016`
absence witnesses remain proven no-binding rows.  No absence row is turned
into physical incidence.

These facts are deliberately unchanged from the mathematical Round292
baseline.

## Targeted attack audit

The independent verifier rejects `22/22` targeted attacks:

- `3` independently re-signed row/table attacks;
- `9` result-level attacks reclosed under their own result SHA-256;
- `4` integer/mixed/duplicate mapping-key attacks;
- `3` stale row/table/result hash attacks;
- `1` coordinated row → table → gzip → result credit re-sign;
- `1` alternate gzip-header encoding of the same decoded object; and
- `1` alternate JSON formatting of the same decoded object.

The attacks cover target-reference substitution, absence-to-physical
forgery, changes to the `396/576` unresolved censuses, registry-census
forgery, upstream/file-hash substitution, nonzero occurrence/DSU/`JxJy`
credit, integer-key restoration, duplicate JSON-key ambiguity, and
fully coordinated recommitment.

## Cold replay

The producer completed under `PYTHONHASHSEED=293001` in `112.76 s`
(`MAXRSS_KB=4443948`).

The independent verifier completed twice:

- `PYTHONHASHSEED=293071`: `149.69 s`, `MAXRSS_KB=4447516`;
- `PYTHONHASHSEED=293929`: `150.55 s`, `MAXRSS_KB=4447208`.

Both runs returned the same PASS status, the same embedded verification
SHA-256
`9a31f1ee14800b2477b7060a1c3e04c19ff99fda1b9d229efa7dab0017ef17fe`,
and byte-identical verification files with SHA-256
`7eed8a1edf0f725a09239e5e440109954aeb26cdd57d6ea5eeee4a2e8809c9ec`.

## Round293 artifact commitments

- producer:
  `988282e3ef57c10f882c9796056d7ca68109ee5d294feb2512b554908251ef00`;
- result:
  `36459f330fdd577031f35d8d8f7e93cf3ebc96bef049a4f687b22c9e39e91613`;
- deterministic gzip ledger:
  `0e7395a69844734cc51563882f471987cc566db28a55ccae6e6d15d045f9e53c`;
- independent verifier:
  `c43cb58d137c2808aa9ca6c70ee940126cb78669f2f058e702daa9d4ed41aeb5`;
- verification:
  `7eed8a1edf0f725a09239e5e440109954aeb26cdd57d6ea5eeee4a2e8809c9ec`.

## Required next

The canonical closure removes an evidence-integrity defect; it does not
resolve the physical obligations.  The next mathematical step must close
the `576` retained positive-`t` owner/shadow open-region identities and
refine the `396` uncovered Round289 seam-facing subcells.  Only after those
are physically bound may the `152` directed true-seam endpoint cells be
paired and a canonical seam/frontier edge ledger be built.  Component DSU,
maximality, all `116` fibres, and all `224,580` global dispositions remain
strictly downstream.
