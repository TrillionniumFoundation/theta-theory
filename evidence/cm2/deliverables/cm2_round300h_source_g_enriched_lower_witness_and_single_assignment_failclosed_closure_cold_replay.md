# Round300-H cold replay

All commands were run from the workspace root with bytecode generation
disabled.  The producer and verifier do not consume random seeds; the
different `PYTHONHASHSEED` values audit accidental set/map ordering.

| role | `PYTHONHASHSEED` | mode | elapsed | max RSS | status |
|---|---:|---|---:|---:|---|
| producer | 17 | write | 40.22 s | 86,412 KiB | PASS |
| verifier | 23 | write | 192.02 s | 2,696,480 KiB | PASS |
| verifier | 97 | strict `--no-write` replay | 190.48 s | 2,692,680 KiB | PASS, byte-identical |

Producer command:

```text
env PYTHONHASHSEED=17 python -B deliverables/cm2_round300h_source_g_enriched_lower_witness_and_single_assignment_failclosed_closure.py
```

Verifier write command:

```text
env PYTHONHASHSEED=23 python -B deliverables/cm2_round300h_source_g_enriched_lower_witness_and_single_assignment_failclosed_closure_verifier.py
```

Verifier replay command:

```text
env PYTHONHASHSEED=97 python -B deliverables/cm2_round300h_source_g_enriched_lower_witness_and_single_assignment_failclosed_closure_verifier.py --no-write
```

The replay reproduced the already-written attack-suite and verification bytes
exactly.  Both verifier runs emitted the same closed verification commitment:
`fa07ace45219a4cae46779ef75448af121a824fa71b8ffdddfdbd3e04bae5547`.
The verifier also required exact equality between all four candidate artifacts
and independently reconstructed deterministic bytes.
