# CM2 Round229 cold replay

Date: 2026-07-27

## Producer replay

Commands:

```text
PYTHONHASHSEED=229041 python3 deliverables/cm2_round229_source_g_global_occurrence_known_block_frontier.py --no-write
PYTHONHASHSEED=229777 python3 deliverables/cm2_round229_source_g_global_occurrence_known_block_frontier.py --no-write
```

Both runs exited `0` and printed the same hashes:

- producer:
  `2518319a103acacc0b6a3dbdd165d9cefd3656d6c323063094daa598bede454c`;
- result:
  `936e140d7113dbdd565f4b1a9381de3b90313e7198266c1950532b80ba153230`;
- certificate:
  `c4152f4764ed7fe977046ef728e8257344803433053e06c0ac11ec68b86ff11a`.

Both reported:

```text
occurrences=53968 attached_known_block=35432 unattached=18536
known_blocks=7404 mixed_key_blocks=0 global_fibres=0/116
```

## Verifier replay

Commands:

```text
PYTHONHASHSEED=229919 python3 deliverables/cm2_round229_source_g_global_occurrence_known_block_frontier_verifier.py --no-write
PYTHONHASHSEED=229041 python3 deliverables/cm2_round229_source_g_global_occurrence_known_block_frontier_verifier.py
```

Both runs exited `0` with byte-identical verification output:

- verifier:
  `0e8245faa5e6d1e52310f0ce1545062a4de62b59dca7692b5bebd6d4c1ff397f`;
- verification result:
  `dce1ea3733b78b1f476da80953380a679924a09c94e86bd9e0584a1695875e86`;
- verification:
  `f570c2148256087687d0b35baebc14bd64c99cdd60326e96fcb320e31605968a`.

Both reported:

```text
PASS_PARTIAL_FORMAL_ROUND229
occurrences=53968 attached=35432 unattached=18536
interfaces=8960 materialized=460 block_reference=456 event_trace=0
semantic=12/12 JSON=16/16 file=8/8 global_fibres=0/116
```

Temporary attack-suite files were created only under a bounded temporary
directory adjacent to the verifier and were removed automatically.
