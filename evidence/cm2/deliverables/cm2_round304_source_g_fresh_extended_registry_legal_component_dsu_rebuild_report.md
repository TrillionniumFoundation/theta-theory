# Round304 fresh extended-registry legal-component DSU rebuild — exact promotion report

Status:
`PASS_ROUND304_FRESH_EXTENDED_REGISTRY_LEGAL_DSU__275268_RANK_REDUCTIONS__92696_COMPONENTS__ZERO_MAXIMALITY_FIBRE_GLOBAL_DISPOSITION_CREDIT`.

Round304 constructs a fresh DSU over exactly `564,492` extended-registry
members and applies exactly `478,710` frozen legal edge rows.  It starts from
`367,964` base roots, performs `275,268` rank reductions, and produces exactly
`92,696` final components.  Forward and reverse applications reconstruct the
same partition:
`72a745845f322255b95bfabb4b7254709e3f7c40359a0314e96b8e0d91c4bcff`.

No serialized historical DSU state is reused.  In particular, neither the old
`63,224` partition nor the earlier conditional `92,696` diagnostic partition
is loaded as state.  The coincident final count of `92,696` is obtained anew
from the extended member registry and the frozen legal edge ledgers.

## Frozen implementation, schema, candidate, and verification pins

```text
producer_sha256=fff60d4a108355299ee6b9e3106549eca130ada2f4451d8f4deb50f0056520f5
verifier_sha256=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
schema_snapshot_sha256=90a2697d70abe3f927b5b1f08449d6dc394c4c39f3b7c10766b2c37af0e4b51e

edge_ledger_file_sha256=5018e0d9356596f7c679d2fa2ea4d84df9672a3e3d1a977faeae20edf61722fb
member_ledger_file_sha256=9a7e8c8a0ef810cfd6f29d99c0d2d6701b537ac76d1ab224dcbb60bec966dbd0
residual_ledger_file_sha256=665b61ce0f54d28106159b485cd39171590cd657a3a6d9b823762d1b42123d5f
wtail_ledger_file_sha256=d7552fe4fd03de2bd45e1586500ac438d95c00288d085ad4e270890f0e93a934
result_file_sha256=2975a8cc61c1b7812fedff6bc9dffd4db8517e822311c54a09317403b3592f7d
result_object_sha256=d9f0c8b573d8d3462091bb075711a4983219b8eb23a3ac5db91bc83e0ded5a0c

attack_suite_file_sha256=b14726d34e790a1a944778978260ca23173c3d4ab60c5580175262103bf283c8
attack_suite_object_sha256=6ba930103fe3a5202dd70712641daa31af2dcb69c32934bc4d8d5c7eb95e61c0
attack_rows_sha256=8caaff102225ceb3a42d7d510480614cb7e4dd55afa0e1877cfefa17f2811e41
verification_file_sha256=482c1124cfd9d6daaa8c5d3af4f1a5023efb368946ff01718f73360bd3e558d3
verification_object_sha256=9b5ce8aebb8a96c1b146f0adf17496b85cb5c3ed6d3d8d08bdcebd887080984a
```

The candidate promotion unit is exactly the four ledgers plus the result shown
above.  The result file is byte-for-byte canonical after parsing, and removing
`result_sha256` from the parsed object recomputes the embedded result-object
closure exactly.

## Rejected first staging batch and repaired canonical gate

The initial seed-A and seed-B staging batches were isolated under the
`r304-invalid-noncanonical-*` private staging directories and were never
promoted or consumed for formal credit.  Their four GZIP ledger files already
had the final hashes, but their result JSON was not parse-canonical: histogram
maps were ordered while their keys were integers, whereas a JSON parse turns
those keys into strings and therefore requires lexical string-key order.

The repaired producer constructs those histogram keys as strings before
canonical sorting.  It now recursively rejects any non-string object key,
requires canonical bytes to survive a parse-and-reencode replay for both the
open payload and the closed result, and verifies the parsed result self-hash
after removing `result_sha256`.  Only the repaired batch with producer pin
`fff60d4a...6520f5` is admitted.  The repaired seed-A and seed-B staging
directories and the formal deliverables match byte-for-byte for all five
candidate files.

## Exact universe and fresh-rebuild census

| Quantity | Exact value |
| --- | ---: |
| Extended-registry members | 564,492 |
| Base roots before DSU application | 367,964 |
| Unkeyed members | 0 |
| Actual official registry keys | 124 |
| Stale official-key count rejected | 116 |
| Pre-Round303B frozen legal edge rows | 434,606 |
| Pre-Round303B fresh rank reductions | 246,016 |
| Pre-Round303B fresh components | 121,948 |
| Sealed Round303B component-edge rows | 44,104 |
| Round303B incremental forward rank reductions | 29,252 |
| Full Round304 legal edge applications | 478,710 |
| Full Round304 rank reductions | 275,268 |
| Full Round304 final components | 92,696 |

All `564,492` members are assigned to one of the actual `124` official keys.
The obsolete denominator `116` is explicitly rejected and is not accepted as
a registry census or issuance boundary.

## Forward/reverse partition closure

| Application | Edge rows | Rank reductions | Components | Partition SHA-256 |
| --- | ---: | ---: | ---: | --- |
| Forward | 478,710 | 275,268 | 92,696 | `72a745845f322255b95bfabb4b7254709e3f7c40359a0314e96b8e0d91c4bcff` |
| Reverse | 478,710 | 275,268 | 92,696 | `72a745845f322255b95bfabb4b7254709e3f7c40359a0314e96b8e0d91c4bcff` |

The pre-Round303B fresh reconstruction had partition
`c1ab6beed75d5e7379103975d6a9ac1b1095a3eb24b34c87288782e7c97cfe09`.
Application-order attribution differs, while total rank and the final
partition agree exactly:

| Source channel | Forward rank reductions | Reverse rank reductions |
| --- | ---: | ---: |
| R296 true seam | 5,212 | 52 |
| R297 ordinary face | 221,916 | 206,684 |
| R299C signed face | 4,332 | 7,064 |
| R300B complete face | 16 | 2,584 |
| R300C positive volume | 5,890 | 5,752 |
| R300E half-open owner | 8,476 | 8,948 |
| R300F/R245 half-open owner | 174 | 264 |
| R303B unified attachment | 29,252 | 43,920 |
| **Total** | **275,268** | **275,268** |

## Exact ledger census and list commitments

| Ledger | Rows | File SHA-256 | Row IDs SHA-256 | Row hashes SHA-256 | Rows SHA-256 |
| --- | ---: | --- | --- | --- | --- |
| Edge application | 478,710 | `5018e0d9356596f7c679d2fa2ea4d84df9672a3e3d1a977faeae20edf61722fb` | `e07866a8bb775a3947f4f8feafc19018f8a0c58c93e1a7a045929a50f6cbe551` | `7fb15ba4a544058d71e4277711067c6d6b357e0d1c7ededaebd7967d9589bf95` | `b9537cf9ded9f83bfcc9a5d9ea801653f83c7cccfb28967ccf82846a3ac024cb` |
| Member/component | 564,492 | `9a7e8c8a0ef810cfd6f29d99c0d2d6701b537ac76d1ab224dcbb60bec966dbd0` | `e9a61126c08810e716f000e34a11983d93249d7ece85ecbe7eeeec74754b25fa` | `be117bd1cf28af09e13409c26be949ccda1f1927d27791aa55f0329b293152bb` | `7c32876075c8da2ff243db50e5ff73860dc11a386a91c76130078fa3fd379bb1` |
| Residual gate | 1 | `665b61ce0f54d28106159b485cd39171590cd657a3a6d9b823762d1b42123d5f` | `5d4e727ba5e24104f2958158e974107902dbe11e5f74af82d728dc41cadad80c` | `9743de78f069f53958e43a7f767cf9c63b8169de23fc522c1b41a5e4e7df748c` | `ddbf36548b5e94198a2ad170d7cfeb39b0d124d72295ff6f99bca3fd322c25e3` |
| W-tail disposition | 4 | `d7552fe4fd03de2bd45e1586500ac438d95c00288d085ad4e270890f0e93a934` | `ac1946ff7fc6470f5b8b8c4b2739372754ca592b7c0ce1a898839cd674fdad3f` | `dca99d46a6bd98dbe1d7c1a979bb471795afc81ea3697d5d5e42179def184df4` | `327e431c4c82ca6e81da97500e0fcbb25b600ee7dd1ef766d797923359a4eb31` |

All four W-tail rows are excluded from DSU input and are in the same final
component by a stronger legal DSU path.  Their exact disposition is
`RECLOSED_BY_STRONGER_LEGAL_DSU_PATH__ZERO_NEW_EDGE`; they receive zero new
component-edge credit.

## Dual-seed replay and independent cacheless verification

| Replay | Hash/invocation seed | Mode | Exit | Wall time | Maximum RSS |
| --- | ---: | --- | ---: | ---: | ---: |
| Producer formal | 304001 | private staging write | 0 | `23:45.36` | 2,740,664 KiB |
| Producer cold | 304557 | isolated no-write | 0 | `24:01.26` | 2,731,860 KiB |
| Verifier formal | 304271 | formal attack/verification write | 0 | `25:57.69` | 2,677,792 KiB |
| Verifier cold | 304983 | isolated no-write | 0 | `25:49.95` | 2,687,552 KiB |

The producer formal replay, fixed seed-B staging, and formal candidate set are
exactly equal for all five candidate files.  The no-write producer returned
the same commitments and closure.  Every timed pane recorded the producer and
verifier pins unchanged before and after execution.  The formal verification
also records
`all_source_and_candidate_PRE_POST_fd_identities_equal=true`.

The independent verifier treats the producer only as inert pinned bytes: it
does not import, execute, parse, or tokenize it.  It reconstructs the complete
expected candidate bytes before opening candidate output.  It then matches all
five exact pins, validates forward/reverse partition equality, and emits
`PASS_EXACT_CACHELESS_EXPECTED_STATE`.

The defense-in-depth suite rejected exactly `58 / 58` concrete fixtures across
`55` mechanisms: `40` shared-validator cascades, `11` OS/AST fixtures, and `7`
wire-format fixtures.  All four baseline guards passed.  The attack artifact
is committed first and the verification artifact is the last marker of the
atomic promotion pair; private staging, two-target no-clobber preflight, and
atomic `RENAME_NOREPLACE` are required.

The formal atomic ordering is visible in the promoted files' nanosecond
mtimes: the attack suite is `2026-07-31 20:31:51.860677263 +0800`, and the
verification last marker is `2026-07-31 20:31:51.865771185 +0800`, exactly
`5,093,922 ns` later.

## Residual gates and exact credit boundary

The Round300A maximality census contains `3,232` pairs: `128` prior witnessed
pairs are in the same final component, `2,080` previously unwitnessed pairs are
reclosed by another legal DSU path, and exactly `1,024` pairs remain
cross-component and unwitnessed.  No sealed physical-inclusion package closes
those `1,024`, so maximality remains unproved.

All `124` official keys are enumerated, but physical fibre exhaustion is not
proved because its maximality dependency is unsatisfied.  The Source-G global
denominator remains exactly `224,580`; all `224,580` dispositions are
unresolved and the global disposition count remains zero.

Round304 grants only the following formal credit:

- `478,710` legal component-edge applications;
- `275,268` DSU rank reductions/successful unions;
- one fresh component quotient;
- the exact resulting census of `92,696` components.

It grants zero maximality, fibre, global-disposition, Jx/Jy same-point,
W-tail new-edge, or Source-W credit.  D02 remains `BLOCKED`; the number of
complete Gate5 18-field blocks is `0`; unconditional CM2 remains
`NO-GO_FOR_CLAIM`.
