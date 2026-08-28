# Round303-B unified attachment component-edge promotion — exact sealed report

Status:
`PASS_SEALED_ROUND303B_43912_B1_192_B2_COMPONENT_EDGES__4_W_TAIL_PAIRS_UNRESOLVED__ZERO_DSU_AND_DOWNSTREAM_CREDIT`.

Round303-B promotes exactly 44,104 previously ineligible cross-component
Source-G pairs to formal component-edge rows:

- `43,912` B1 monotone graph-side attachments;
- `192` B2 analytic/physical target-sheet attachments;
- `4` W-tail pairs remain unresolved, with no nonedge or exclusion credit.

The package does not apply an edge to a DSU.  A later round must rebuild a
fresh DSU from the expanded registry and frozen edge ledgers; neither the old
`63,224` result nor the conditional `92,696` diagnostic partition is consumed.

## Frozen artifact pins

```text
producer_sha256=02ce70a560b7fa029e2c7a70a1e4627cb423ac67ba187dba059b57194a646735
b1_ledger_file_sha256=776f1164f96731a2e71b6553ac08165aaa3fe05bb051c0f6602cd8edfd73fa43
b2a_ledger_file_sha256=6095269bd2b791c78b0c305599e7dc3b518dc762e47c00aedeaebe080548e515
b2b_ledger_file_sha256=ca88dcf992c9c2a2483485109f80634376e6cc02239ffd3146f6e1dd318bca96
component_edge_ledger_file_sha256=650df67dfcc3033c42b36638a0da4b3d63ce575469cab84a5e8971ed7b23243a
wtail_unresolved_ledger_file_sha256=eaa18cdec4217e57238d8e5b4209c33295dc325dbb352f1d52347e0d18acdf8e
result_file_sha256=4bd7127f9d935cf7b334fd7660fa6332f8aa23a9c819ac7e018c8add8473eaa1
result_object_sha256=2ca258de5a58175164267bd3ca81b0da8b25a4ebffcd998805e8f7254d172fc2
verifier_sha256=420883fbc6b2ad5a8413e51635b814bac7c1f059e1ff937765e38c8ac98ff88f
attack_suite_file_sha256=c7d87135c2fd77d89855c276be98908649979793d757accadd9bf3dd974b9ab7
attack_suite_object_sha256=feaa6ce50e733dd394a5994d56857cde8a7bd73cb4a7ad814585124d8842029e
verification_file_sha256=6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a
verification_object_sha256=a803d41e9be3513fb2b2e1ac87e22b35c83c2e678647105708a0857339cbfe57
```

## Exact census and commitment closure

| Ledger | Rows | Rows SHA-256 | Row IDs SHA-256 | Row hashes SHA-256 |
| --- | ---: | --- | --- | --- |
| B1 | 43,912 | `3a60a03b057d0d1e084b8af5ab6ec686e09c3c3c91aa2800f839eda569a1f345` | `3c082b7e8f68b99c83e2fbd99935c3cebcfdd818ebb77c2cb05179cdf9f1f159` | `450a7b0b205669b1d29d1b269805d1bbf5c59435a950dce5afee777bcb498c2f` |
| B2a | 192 | `f50aca595114d8a1dc031d39e902187928073e9d087df91be416c91cffe51410` | `ed4e6c9ebab2e30adb345b0ae104860eaa5618f9d98344bf8780ec52bde04305` | `0bf2051f08ff7afe40f1b4e2ad96b7a5a1f54936b633027e5b29c7016b500597` |
| B2b | 192 | `4f1ae1e91459b38df7090c2b8de36650c8b459d16e1059d4991239e3bf119ef6` | `7881322636943a6c991312c9e1e83f42357bcd219e5da384ead9e58394115187` | `9f6570fa5cb9e950cbd6564893627075aafceaa248f6e399fb532cc4925aaa64` |
| component edge | 44,104 | `2a161f4fecc6558bac8f156e2a3de35d5e41694f18183ab455c91261a4964ad8` | `a41da94732f101e2d3c0037d0fb7f167c2e52a139bb1c76d8bb07a9bbe23d6b6` | `1f5a281a7d48506c3c6a700072940243c39892f1d714dc93a8b7d25e7cacb956` |
| W-tail unresolved | 4 | `9d3b489612db47e1d863865e0fcf21fde7063ee961c74ee7a05514f372dc0842` | `e6a9978c274b174ca314d996123279b89989d02b6e6d2713f81870c5e8af7c33` | `4ea28f4cb3abb8acbe982f4876b9d6cb1f4c75fee4925e342b9212b070f19583` |

An independent framing audit confirmed strict canonical JSON, deterministic
single-member GZIP framing, lexical row-ID order, every row's own SHA-256,
the three list commitments, exact file hashes, and the result self-closure.

## Producer replay equality

| Replay | Hash seed / invocation seed | Mode | Exit | Wall time | Maximum RSS |
| --- | --- | --- | ---: | ---: | ---: |
| formal | `303201` / `303201` | formal write | `0` | `1,370.97 s` | `3,345,788 KiB` |
| cold | `303997` / `303997` | isolated no-write | `0` | `1,409.19 s` | `3,347,784 KiB` |

Both replays reported the same five ledger hashes, result file hash, and
embedded result closure above.  The no-write replay is exact reported-hash
equality; it does not claim a comparison against persisted staging files.

## Independent cacheless verification

The independent verifier treats the producer only as the inert byte pin shown
above.  It reconstructs all expected rows, deterministic GZIP bytes, result
semantics, and commitments before opening candidate output bytes.  It never
imports or executes the producer.

| Replay | Hash seed | Mode | Exit | Wall time | Maximum RSS | Verification file SHA-256 |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| formal | `303271` | formal artifact write | `0` | `2,007.38 s` | `3,172,476 KiB` | `6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a` |
| cold | `303929` | isolated no-write | `0` | `2,040.89 s` | `3,172,484 KiB` | `6dde1fc938c5059290b811d297306ae16347fd93624a29d7b0ba59974cc06d5a` |

Both runs returned `PASS_EXACT_CACHELESS_EXPECTED_STATE`.  The suite rejected
exactly `55 / 55` attacks, accepted none, and independently enforced the
Round294B builder-admission closure before consuming Round294.

## Exact package and strict nonclaims

The manifest binds exactly 12 members: producer, five ledgers, result,
independent verifier, verification, attack suite, this report, and the cold
replay record.

Round303-B grants exactly `44,104` component-edge credits.  It grants zero DSU
rank-reduction, component quotient/union, identity/key merge, seam or Jx/Jy,
maximality, fibre, global-disposition, Source-W, D02, Gate5, or unconditional
CM2 credit.  The four W-tail pairs remain unresolved and are neither nonedges
nor exclusions.
