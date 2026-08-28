# Round305A post-Round304 residual-scope reprojection — exact promotion report

Candidate status:
`PASS_ROUND305A_EXACT_R300A_POST_R304_RESIDUAL_SCOPE_REPROJECTION__1024_RESIDUAL_PAIRS__ZERO_DOWNSTREAM_CREDIT`.

Independent promotion status:
`PASS_EXACT_CACHELESS_ROUND305A_SCOPE_REPROJECTION`.

Round305A exactly reprojects the complete sealed Round300A `3,232`-pair
frontier through the sealed Round304 member-to-component map.  It seals the
resulting residual scope; it does not issue a physical-inclusion witness,
component edge, union, maximality result, fibre result, or global disposition.

## Frozen implementation and artifact pins

```text
producer_file_sha256=42e7cc1eeabaedee883a37b8de9301ee71d5ba068d2fb76fafc80b95061b6772
verifier_file_sha256=d4fd7bfd4c2bb90e1df515a9318d8f925fc9dab4bb8cb3872f496a3d665647bf
schema_snapshot_sha256=19dd648b76f13ff02d161d4e5f3968c7e527f74887cb37c725c7a467912515f3

ledger_file_sha256=8db30279e03aac90ea96b7a603e51aaa6fb2a70ad6c1593915c55b1befe991b6
ledger_object_sha256=e9ee0b466af93bf80be8dc1f6ad1a98e15f1bc91992c351216fb6089b879cf62
ledger_self_sha256=4ac632ae2183c96024fcaad4ff522c1ed71db68fd0f330b9061c2e9e28bae781
result_file_sha256=b985df80cc0b447f25509ef6d4095b9d0aa810ffcef05d4b5475bf84d36542f1
result_object_sha256=c391ecca3f5af8227052c628bda77104ec564d4eeaa625fafbde32a3ada352eb

attack_suite_file_sha256=3795cd3b03f961e010b351d5132f55f5d3bda8d4245707755d999e780a9c71b7
attack_suite_object_sha256=e060b0d4807014a341fa621742b1b5255ecc52036bd02c530779c485ba2367f7
attack_rows_sha256=ca9ee4336aa200afbee298ebae7bb39f09c69e5790f73b19c843d08c3a806e94
verification_file_sha256=5c98bd02f4245d3b6fd7d35518b6932f984ec05d3e91b607854bf9e180b29c4d
verification_object_sha256=9654f43c32aacfd3a27b6baa18d65755dfb9c867bd869aaa586a9b736fcf7589
```

The producer, ledger, result, and verifier hashes were recorded before formal
promotion and were unchanged afterward.  The independent verification also
records
`all_source_and_candidate_PRE_POST_fd_identities_equal=true`.

## Exact reprojection census

| Classification | Rows |
| --- | ---: |
| Prior Round295A witnessed and in the same Round304 final component | 128 |
| Unwitnessed but reclosed by another sealed legal DSU path | 2,080 |
| Unwitnessed, cross-component, and requiring a formal physical-inclusion package | 1,024 |
| **Complete Round300A scope** | **3,232** |

The complete scope uses `4,892` distinct endpoints.  The residual scope uses
exactly `2,048` distinct endpoints, each of residual degree one.  Its primary
commitments are:

```text
complete_pair_set_sha256=e7206fca536d237276ccf84da9542e32b3a0c82e44d0e8541275b5a5dead4275
complete_endpoint_set_sha256=306c249d452b5778cfb462296c981f1644a430700451df24bee6b735f5eba6f5
residual_pair_set_sha256=f7f9941f84428df71039b4708dfa251eae6c962267f68ccd13945ee445c5bf29
residual_endpoint_set_sha256=b09fe8149f89a95c2c9effcbce33bc49df24065987c870fc65b09ac85fe98779
residual_final_component_pairs_sha256=0e783f8ded68b885bd4e0a70dd27049e6e74194c6f301c8e49ebfc8d1add1344
legacy_Round304_projection_sha256=8646795f43524e80a04eeaa7852ba331a3f9767842ee14bcad66db9aa6b03b08
```

The `1,024` residual rows group into exactly `8` unordered Round304 final
component pairs over `16` distinct components, with `128` rows in every
group.  This is only a derived task compression.  It does not convert the
rows into eight component edges: every row still requires an admissible
two-sided physical-inclusion/gluing witness or a fail-closed exclusion, and
Round305A grants zero edge and union credit.

## Independent reconstruction and attack gate

The promotion verifier treats the producer as inert pinned bytes only: it is
not imported, executed, parsed, or tokenized.  Before opening candidate output
it independently rebuilds the complete expected ledger and result bytes from
the sealed Round300A and Round304 inputs; Round303B is validated only as
lineage and is not used as a reprojection input.  Candidate and independently
rebuilt file pins match exactly.

All `36 / 36` attack fixtures were rejected across all `36` mechanisms:

| Category | Rejected fixtures |
| --- | ---: |
| CASCADE | 14 |
| CREDIT | 8 |
| UPSTREAM | 3 |
| WIRE_OS_AST | 11 |
| **Total** | **36** |

Exactly `25` fixtures were coherently re-signed before rejection.  The suite
also exercises no-clobber, race, wrong-commit-order, temporary-input,
hard-link, symbolic-link, bounded-gzip, canonical-JSON, source-separation,
provenance, classification, and forbidden-credit boundaries.

The formal publisher used a private stage, complete two-target no-clobber
preflight, and atomic `RENAME_NOREPLACE`.  The attack suite was committed
first at `2026-07-31 23:40:00.700109092 +0800`; the verification artifact was
the required last marker at `2026-07-31 23:40:00.704983611 +0800`, exactly
`4,874,519 ns` later.

## Replays

| Replay | Seed | Mode | Exit | Wall time | Maximum RSS |
| --- | ---: | --- | ---: | ---: | ---: |
| Independent verifier formal promotion | 305305 | write attack then verification | 0 | 133.34 s | 411,260 KiB |
| Independent verifier cold replay | 905701 | `-I`, isolated pycache, no write | 0 | 139.51 s | 410,496 KiB |
| Producer seed A | 305001 | private no-clobber staging | 0 | 82.10 s | 77,872 KiB |
| Producer seed B | 305997 | private no-clobber staging | 0 | 82.26 s | 76,248 KiB |
| Independent dual-seed comparison | 777331 | exact-byte comparison, no write | 0 | 83.49 s | 410,684 KiB |

The cold verifier reproduced the formal attack and verification hashes
exactly and reported
`candidate_and_promotion_outputs_written=false`.  The two producer seeds
generated byte-identical ledger and result files, and the independent
dual-directory comparison emitted `PASS_DUAL_SEED_EXACT_BYTES` with
`seed_affects_output=false`.  Replay staging and isolated pycache directories
were removed after comparison and were never admitted as formal promotion or
credit inputs.

## Exact credit boundary

Round305A seals only the exact post-Round304 classification and the exact
`1,024`-row residual scope.  It grants zero:

- physical-inclusion or Jx/Jy same-point gluing credit;
- component-edge or DSU-rank-reduction credit;
- maximality, fibre, or global-disposition credit.

No fresh DSU rebuild is performed and no new component edge is issued.
Physical inclusion and a two-sided gluing theorem remain absent.  D02 remains
`BLOCKED`; complete Gate5 18-field blocks remain `0`; unconditional CM2
remains `NO-GO_FOR_CLAIM`.
