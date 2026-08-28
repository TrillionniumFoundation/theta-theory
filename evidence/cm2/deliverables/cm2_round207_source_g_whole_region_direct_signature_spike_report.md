# CM2 Round207 — source-G whole-region direct return-signature spike

Date: 2026-07-26  
Verdict: `VALIDATED` for local outgoing-W direct-signature feasibility

## Question

Can every one of the `36,040` strict Round195 outgoing-W candidate regions
directly certify a complete canonical local return signature, including the
`32,776` regions left unanchored by Round203, without using a resolved
anchor, parent-wide signature base, component propagation, or a sampled
point?

The required fields are:

- unique first target lift;
- ordered integer wall events;
- signed wall word;
- roof;
- outgoing cell and target chart; and
- official Gate5 key row, ordinal, and identifier.

## Method and trust boundary

The read-only probe
`cm2_round207_source_g_whole_region_direct_signature_probe.py` was run at
SHA256

`0262235b43d74084c37b742b8b4fc435b82e752663d5f816e092faf14e64404a`.

It pins the final Round203 source and report, which recursively pin the
Round198/Round195 and verified Round174/Round179/Round182 chain. Imports
occur before local hash checks, so this is a feasibility-probe trust
boundary rather than an adversarial verifier.

The method is outcome-blind and is applied to all `18,324` leaves and all
`36,040` candidate regions, not merely to the Round203 residual cohort.

For each leaf, the probe:

1. requires the exact rational leaf box to lie strictly inside its true
   source chart;
2. evaluates the complete retained list of `57` target lifts with the
   pinned interval first-hit atlas;
3. selects a unique first future target without using the frozen collar
   owner as input;
4. requires a positive discriminant, strict positive near root, and return
   time below three;
5. recomputes the target normal and hit endpoint;
6. certifies every X/Y integer-wall endpoint and crossing count on the
   entire leaf enclosure;
7. certifies the complete strict crossing-time order on that enclosure; and
8. rebuilds the word, roof, and exact Gate5 key from the independently
   reconstructed registry.

The frozen collar owner is used only after this calculation as a consistency
check.

The whole leaf intentionally remains unresolved only in its outgoing chart:
every leaf has interval status `outgoing_chart_seam`. Each candidate region
is therefore treated separately. Its strict HPLUS/HMINUS sign pair from the
Round195 factorized arrangement gives exactly one outgoing cell:

| HPLUS | HMINUS | outgoing cell |
|---|---|---|
| positive | positive | E |
| negative | negative | W |
| positive | negative | N |
| negative | positive | S |

Target and wall fields are certified on the containing leaf enclosure,
which is stronger than certifying them only on the region subset. The
outgoing chart is certified on the strict region itself. The fields are
combined only after both proofs succeed.

No Round174/Round179 resolved signature row, Round198 direct-adjacency
assignment, or Round203 component membership is read as a signature input.

## Development and final replay

The initial outcome-blind development run established the full census. A
second development run added the strict source-chart guard and diagnostic
partition. Those outputs were used only to install fail-closed exact pins
for:

- direct leaf rows;
- all candidate assignment rows;
- U|U assignment rows;
- the complete census;
- probe result; and
- output JSON bytes.

Development outputs are not final evidence.

Static checks:

- AST parse: pass;
- synthetic `--bad-option`: rejected with exit `2`;
- output-path option present: no;
- runtime filesystem writes: zero.

Two final hash seeds were run from the pinned final source:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=207052 \
  ../.venv-neurips/bin/python -B \
  cm2_round207_source_g_whole_region_direct_signature_probe.py \
  > /tmp/cm2_round207_seed207052.json

env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=207062 \
  ../.venv-neurips/bin/python -B \
  cm2_round207_source_g_whole_region_direct_signature_probe.py \
  > /tmp/cm2_round207_seed207062.json
```

Both pinned replays exited zero:

| seed | elapsed | maximum RSS |
|---:|---:|---:|
| 207052 | `18:47.30` | `722,116 KiB` |
| 207062 | `18:49.73` | `723,216 KiB` |

The elevated wall time includes substantial host contention from unrelated
multi-worker jobs; each replay remained deterministic and completed. The
two output JSON files are byte-for-byte identical.

Final pinned hashes:

- probe result:
  `d49b3c9cef0738a03bca8f6477121c7b27aa63e3be8b9ac5854c2521f97448ce`;
- output JSON:
  `21b388fbd147219f5f52fbdcbe8528b7b9afc06590f2bb997e70042a759f5277`.

## Whole-leaf base census

All `18,324` leaf boxes pass:

| property | count |
|---|---:|
| strictly inside the true source chart | 18,324 |
| complete target-list unique first target | 18,324 |
| direct target agrees with frozen collar owner | 18,324 |
| target root strict, non-grazing, future, and below three | 18,324 |
| wall endpoints/counts and event order strict | 18,324 |
| whole-leaf outgoing status is only `outgoing_chart_seam` | 18,324 |
| direct leaf residual | 0 |

Every complete retained target list has `57` entries.

The direct-leaf rows have SHA256

`4d541ea5bfc4b9db30e78f994e36177dee7112b4c4057c71d6d6376650e20e9e`.

The independently reconstructed Round195 leaf rows retain SHA256

`0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5`.

## Whole-region signature census

All candidate regions receive one direct canonical signature:

| status | regions |
|---|---:|
| directly certified | 36,040 |
| residual | 0 |

This logically covers every Round203 unanchored candidate because the same
anchor-free algorithm was applied successfully to the complete candidate
set:

- Round203 directly anchored candidates: `3,264`;
- Round203 unanchored candidates: `32,776`;
- newly shown directly certifiable among that residual cohort: `32,776`.

The compact assignment rows have SHA256

`e46fc7e35f2728e48a81e47cd0266cf25c07ad63e534a9fd5b57cc8b0007bb72`.

The local signature census is:

| item | count |
|---|---:|
| distinct complete local signatures | 52 |
| involved official Gate5 exact keys | 24 |
| distinct target lifts | 12 |
| word length 0 regions | 30,080 |
| word length 1 regions | 5,960 |

The exact-key ID and ordinal set hashes are respectively:

- `2c7aa2236eed360cfb41c318d6b9904c5b33b8c1a78979451d66a36b74f83b33`;
- `7b9394fd0da52793cb900cb82a26f7456d4097159b00f6fcf7a09bf14dc1f58c`.

Outgoing cells are balanced:

- E: `9,008`;
- N: `9,012`;
- S: `9,012`;
- W: `9,008`.

Residual leaves, origins, and parents are all zero in this scoped local
feasibility census.

## U|U side-specific audit

All `88` U|U leaves are rebuilt with the Round195 cross-t ordering proof.
Their `176` candidate regions are evaluated as separate strict sides:

- directly certified sides: `176`;
- residual sides: `0`;
- leaves with both sides certified: `88`.

The U|U assignment rows have SHA256

`de20109df8b913a12627b42340ccdacb88e633a5c96cd56bcdd8bafe410fee53`.

No signature is inferred by crossing the outgoing seam or by copying one
U|U side to the other.

## Verdict and promotion boundary

`VALIDATED`: direct interval reconstruction is feasible for all `36,040`
strict outgoing-W candidate regions. The previous adjacency/component
obstruction was an artifact of requiring a resolved geometric anchor; it
is not an obstruction to directly recomputing the signature fields.

This does not yet create an official local-signature attachment or a global
source-G disposition. Required remaining work includes:

- a formal producer and independent verifier for all direct rows;
- separate closure of the `64` wall-G residual leaves;
- explicit half-open boundary ownership;
- global occurrence join/deduplication by official exact key; and
- proof that every complete exact-key fibre is covered or excluded.

The strict global state remains:

- source-G global dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- CM2: `NO-GO_FOR_CLAIM`.
