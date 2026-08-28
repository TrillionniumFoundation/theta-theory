# CM2 Round168 — dimension-safe source-W combined stage-one ledger

Date: 2026-07-26

## Decision

Round168 certifies a single dimension-safe composition ledger for the frozen
source-W first collision:

```text
refined source-W record space                    76,832
admitted whole-record exclusions                 73,162
conservative live records or composites           3,670
conservation                           73,162+3,670=76,832
```

The result combines only three pairwise-disjoint exclusion blocks whose
whole-record meaning is independently supported.  It does not promote the
Round166 six-level prototype, does not credit any internal mismatch side of
a Round165 typed collar as a whole record, and does not close D02.

## Admitted evidence and disjoint credit

The admitted credit rows are:

```text
Round164-v2 prior dimension-safe exclusions       37,480
Round165 whole mismatch terminal rectangles          118
Round166 immediate whole-parent exclusions        35,564
combined whole-record exclusions                  73,162
```

They occupy distinct pinned classes:

1. Round164's already-excluded baseline precedes the later refinements.
2. Round165's 118 records replace members of the 618 outgoing-chart seam
   class.
3. Round166's 35,564 records partition members of the separate 38,180
   multi-candidate class.

The Round164 remaining partition is independently checked as:

```text
original prefix stage-one match                       518
outgoing-chart seam parents                           618
tangency ambient bulk                                  32
multi-candidate parents                            38,180
sum                                                39,348
```

Together with the 37,480 prior exclusions, this recovers the original
76,828-record Round164 space.  Round165 replaces 618 seam parents by 622
terminal rectangles or collars, yielding the refined total 76,832.

## Dimension-safe live ledger

The conservative live side of the refined ledger is:

```text
original prefix stage-one matches                     518
Round165 seam live composites                         504
Round164 tangency ambient bulk                         32
Round166 owner-active multi parents                 2,616
total                                               3,670
```

The 504 Round165 seam composites are exactly:

```text
whole-W terminal rectangles                           224
typed collar composites                               280
```

Each typed collar counts once as one conservative live composite.  Its
internal three-stratum materialization remains:

```text
3D W-open side                     live at stage one
3D adjacent mismatch open side     not whole-record credit
2D W-owned half-open graph         live analytic stratum
```

Therefore the 280 adjacent mismatch sides receive zero whole-record
exclusion credit.  The Round164 typed tangency graph likewise receives zero
whole-parent credit because the off-graph ambient bulk remains live.

## Round166 scope firewall

Round168 opens and consumes only the pinned Round166 limited independent
verification envelope and pins its verifier source.  It does not open the
Round166 stats document or producer as evidence.

The only imported Round166 counts are the independently replayed immediate
baseline:

```text
multi-candidate parents                           38,180
owner has no real intersection                    34,310
owner intersection is behind                       1,178
owner dominated by a strict future root               76
immediate whole-parent exclusions                 35,564
owner-active subdivision inputs                    2,616
```

The witness partition satisfies:

```text
34,310+1,178+76=35,564
35,564+2,616=38,180.
```

The Round166 six-level tree was not independently replayed, the prototype is
not fully promoted, and every deeper-profile statistic receives zero credit.
In particular, the Round166 deep-profile box count is neither included nor
reported as evidence in the Round168 certificate.

## Independent verification

The Round168 verifier byte-pins but never imports or executes the producer.
It independently validates the admitted Round164/165/166 chains, rebuilds
every baseline, credit, and live row with row digests, and then requires:

```text
full expected canonical document equality          true
recursive exact-key tree equality                   true
canonical single-newline JSON                       true
```

Its fail-closed attack suites pass:

```text
re-signed semantic mutations rejected              55/55
strict JSON attacks rejected                         9/9
path-safety attacks rejected                         7/7
```

Every semantic mutation is re-signed at the result-envelope level.  The
suite covers the record delta, all credit and live counts, disjointness,
row/table digests, the 280-collar counting rule and mismatch-side noncredit,
the 2,616 owner-active count, attempted Round166 deep-profile admission,
scope/nonpromotion fields, provenance pins, and the exact next-gate text.

The strict-JSON suite rejects duplicate keys, floats, NaN, BOM, raw and
escaped NUL, unpaired surrogates, trailing documents, and a non-object top
level.  The path suite rejects symlink, hardlink, and oversized inputs plus
outside-directory, protected-alias, symlink, and hardlink outputs.

Cold replay in clean environments under `PYTHONHASHSEED=1` and
`PYTHONHASHSEED=987654321` is byte-identical for both certificate and
verification:

```text
producer source SHA256
4b867ad8acf8ea8ff7ca1b2a0b0e510fcef1f7a22a31eccb30f2d2bc97644abe

certificate result SHA256
1544a7b865df882bab92dbec333e723fea28dd382567945e09ad609e7a811201

certificate file SHA256
adbdcc3ffbd791126dd759a5699bf65902ebb8529b173db52e4b45e5f299494e

verifier source SHA256
087134652c7950ce2956557dc5be6b6255b38d69bc04c2498a9b36b09d08b17d

verification result SHA256
07f9bcc6fd42f5439322e1090b281a3f0780c3a706bb19ceeb9f51b666280031

verification file SHA256
994037b25d321e731e4cf4b61c92610fa99fadfccfa2d15ce2a38ccbe20a5cc9
```

## Strict state and next gate

```text
D02                                      BLOCKED
D03 negative oracle                     UNAUTHORIZED
Global Gate5                            10/18
global complete 18-field blocks             0
CM2                                      NO-GO_FOR_CLAIM
```

The next core work must preserve dimensions:

1. Continue later frozen-prefix stages on the 224 whole-W rectangles.
2. For each of the 280 collars, first materialize and separately ledger the
   W-open side, adjacent mismatch side, and W-owned graph; only live strata
   may continue to later prefix stages.
3. Materialize the 32 tangency ambient recuts.
4. Resolve the 2,616 owner-active multi parents without importing unverified
   deep-profile credit.
