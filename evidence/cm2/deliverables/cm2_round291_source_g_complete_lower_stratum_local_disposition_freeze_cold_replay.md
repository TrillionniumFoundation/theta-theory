# CM2 Round291 complete lower-stratum local-disposition cold replay

Date: 2026-07-29  
Scope: local lower-stratum existence/absence only; all global credits remain zero.

## Producer replays

The finalized producer was run twice from the pinned upstream artifacts:

```text
seed 291071
seed 291929
```

The seed is deliberately outcome-irrelevant.  The two runs produced
byte-for-byte identical outputs:

```text
ledger cmp: MATCH
result cmp: MATCH
```

Final file commitments:

```text
producer:
  1f485f0add666eecb83e73b5cd498b490d0f8895726717bccb4c8727600838c7
ledger:
  412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab
result file:
  f07aae7d12b9d33aea0313737b7dafa51b22c1c8b1e5526ecf87ad53c5a8f705
result object:
  2397c4d1e83155fdf1c8cd625fb772be0a5c39e1b758d6f7e5ae7bb8131dbc77
```

Both gzip payloads passed `gzip -t`; both result self-digests were
independently recomputed from canonical JSON and matched.

## Independent verifier replays

The cacheless verifier was also run twice, including a replay with
`PYTHONHASHSEED=291929`.  Both runs independently rebuilt all 55,428 rows
before opening the candidate, rejected 23/23 fully resigned attacks, and
produced byte-for-byte identical verification files:

```text
verification cmp: MATCH
verifier:
  4f7940564dd60a19cbc25b9348c794aeae0cdac386f835de37b868e2edd24512
verification file:
  8011e1de7de9c931db3b6626523bda3757beb07e7dbcd3645ad4413ae5af148e
verification object:
  705469f37b2b68a8a79ea6e5075525f13aba9ed48cb5d2eef2fd3ae24c3b5b68
```

## Deterministic census

```text
Round267 nominal universe:             55,428
whole physical:                        39,252
whole absent:                          16,168
partitioned physical/absent:                8
unresolved:                                 0

fully replaced supports:
  outgoing:                               284
  wall:                                   112

wall support sign pairs:
  negative | negative:                     48
  positive | positive:                     48
  negative | positive:                      8
  positive | negative:                      8

t=0 exact face area:
  total:                               31/640
  physical:                          59/1280
  absent:                             3/1280
  partition delta:                          0
```

The 112 wall supports were rebuilt on all 224 resolved children using only
exact `Fraction` interval arithmetic and exact 256-bit dyadic outward square
root enclosures.  All 448 source/target endpoint-factor signs were strict.
No `python-flint`, upstream producer, or upstream verifier was imported or
executed.

## Non-promotion contract

The producer's 28 resigned mutation attacks were all rejected.  Every row
keeps occurrence, component, maximality, fibre, global-disposition, and
Jx/Jy same-point glue credit at zero.  Whole-absent rows are explicitly
`NO_OCCURRENCE__LOCAL_ABSENCE`; only physical or partitioned-physical cells
remain pending final occurrence-registry binding.

Global state is unchanged:

```text
expanded occurrences: 126,468
quotient:               63,224
maximality:             0/63,224
exact-key fibres:       0/116
global dispositions:    0/224,580
Gate5:                  10/18
D02:                    BLOCKED
CM2:                    NO-GO_FOR_CLAIM
```
