# CM2 Round277 collar common-face MATCH probe

Status: `ORIENTATION_CORRECTED_COLD_REPLAY__ZERO_CREDIT`

## Scope and method

Round276 produced 330,724 same-signature positive common-face candidate edges
between canonical `(Round182 leaf, complete signature)` atom candidates.  This
probe reconstructs every candidate from the frozen Rounds208/269/270/271/272
ledgers and Round182 leaf geometry.

For each candidate it searches a dyadic adaptive subdivision of the common
two-dimensional face through depth 4.  Acceptance requires:

1. a strictly positive-area face patch on which the frozen Round174 evaluator
   reconstructs the complete signature exactly;
2. one inward positive-volume corridor in each incident leaf, each carrying
   that same complete signature.

Corridor widths are tried dyadically through depth 24 at 256-bit precision.
The geometric side of each endpoint is inferred from whether its exact upper
or lower leaf coordinate equals the shared-face coordinate.  A finite-depth
patch miss is fail-closed and is **not** an emptiness proof.

## Orientation audit

An initial preliminary run incorrectly treated lexicographic endpoint order as
geometric negative/positive side order.  Independent audit found that tuple
order agrees with geometry for 165,439 candidates and is reversed for 165,285.
That preliminary corridor ledger was immediately withdrawn.

The corrected cold replay uses exact leaf endpoints to choose both inward
directions.  It found zero invalid face orientations.  The face-patch census
is unchanged, while the corridor-depth profile and accepted witness digest
were independently regenerated.

## Corrected full census

- input candidate edges: **330,724**
- accepted positive MATCH patch plus two correctly oriented corridors:
  **240,932**
- fail-closed, no patch found by face depth 4: **89,792**
- fail-closed due to a missing correctly oriented corridor after a patch:
  **0**
- accepted corridor witnesses: **481,864** (exactly two per accepted edge)
- deepest corridor witness used: **20**
- corrected accepted-edge witness digest:
  `91132d39a7f1982657476bb60c0878faa108bba2b20c285ef6406f0263af458a`

The exact corrected corridor-depth histogram is frozen in the companion result
JSON and sums to 481,864.

## Interpretation

The 240,932 accepted rows are probe-level local geometric edge certificates.
They are not yet component unions because the formal producer, independent
verifier, canonical occurrence-atom materialization ledger, and true-support
candidate-universe audit have not yet been frozen.

The 89,792 depth-limit misses remain unresolved arrangement tails.  They are
neither rejected edges nor certified absences.  The next pass reconstructs
their index ledger, classifies them by face geometry, and closes them by deeper
adaptive patches or explicit graph/wall arrangements.

Strict non-promotion remains:

- expanded-occurrence credit: 0
- component-edge credit: 0
- maximality credit: 0
- `Jx/Jy` glue credit: 0
- CM2: `NO-GO_FOR_CLAIM`

## Artifacts

- `deliverables/cm2_round277_source_g_collar_common_face_match_probe.py`
- `deliverables/cm2_round277_source_g_collar_common_face_match_probe_result.json`

The Round278 four-row W-tail artificial-split alias probe is a separate
zero-credit prerequisite.  A later formal producer must also clip the candidate
universe to each canonical atom's true support before consuming any local
edge.
