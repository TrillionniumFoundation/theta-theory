# CM2 Round290 — isolated canonical-atom inner-support closure

## Verdict

Round290 closes the complete `21,160`-atom inner-support residual left by
Round288.  Every residual atom now has a strictly positive-volume rational
inner box, with:

- full ten-field return signature and exact key recomputed on the whole box;
- source chart and owner target recomputed and matched;
- source signed-region active factor/graph side verified independently of the
  return signature;
- strict containment in both the canonical atom's frozen envelope and its
  original Round182 leaf;
- strict interior status for the true source-chart guard; and
- no contact with a half-open or excluded face.

The failure residual is `0`.  Round290 remains a **zero-credit** closure:
formal occurrence, component, maximality, fibre, disposition, seam, and
`Jx/Jy` credits are all zero.  The standalone independent verifier now passes,
but occurrence identity still requires a later explicit promotion round.

## Closed census

| Source tranche | Inner boxes |
|---|---:|
| Round269 connected outgoing-W factor sides | 3,968 |
| Round270 connected outgoing-G factor sides | 6,728 |
| Round271 WALL sides | 10,448 |
| Round272 boundary-WALL sides | 16 |
| **Total** | **21,160** |

All `10,696` Round269/Round270 rows use one finite, seed-inert ordered rational
catalogue of `11^3 = 1,331` candidate centers.  Each accepted box separately
passes:

- pinned Round269 W or Round270 exact-G factor evaluation;
- strict `HPLUS` and `HMINUS` signs;
- the requested product/region sign; and
- whole-box dynamic return-signature reconstruction.

All `10,464` Round271/Round272 WALL rows use nested dyadic expansions around
their pinned strict rational witness.  The witness is only a search center,
never the inner support.  Expansions are attempted from largest to smallest;
the largest successful dyadic-box depth is recorded per row.  Every row closes
at depth `0`.

Every ledger row records its canonical atom ID, exact source-signature row ID,
Round182 leaf, deterministic witness-generation path, exact box, exact volume,
expected and recomputed signatures, exact key, and the independent signed-side
proof.

## Duplicate and frontier audit

Round290 rechecks the new boxes rather than inheriting the Round288 envelope
audit:

- complete existing Round266 frontier: `126,468` occurrences;
- exact existing-frontier interval shortlist comparisons: `2,307,614`;
- positive-volume overlap with existing frontier: `0`;
- same-chart/same-signature pairwise shortlist comparisons: `25,564`;
- positive-volume duplicate pairs between distinct Round290 atoms: `0`.

The new support boxes therefore preserve Round288's conditional arithmetic:

- conditionally distinct new atom candidates: `295,336`;
- conditional occurrence total if the verified Round288 and Round290
  candidates are later explicitly promoted: `421,804`.

These are conditional counts, not Round290 formal credits.

## Standalone independent verification

The cacheless verifier does not import or execute the Round290 producer.  It
first reconstructs all expected boxes, signatures, signed sides, chart guards,
and both overlap audits.  Only after those computations finish does it open the
candidate result and ledger.

The evaluator boundary is source-closed: the complete `16`-module local
transitive import closure is byte-pinned before any evaluator import; preloaded
modules are rejected; and a source-only loader compiles the pinned `.py` bytes
directly with no `.pyc` input.  Every loaded module's resolved `__file__` and
`spec.origin` is rebound to its pinned file.

Independent reconstruction exactly reproduces:

- ledger rows SHA-256:
  `3ab9344c1fa492d87eee4937d11659872ea848c6ff9bf02419c10ae77a0636cd`;
- row IDs SHA-256:
  `90364fbc92c8ec21100eba1d7ba5cb8ceeb616506f138dfdc21315e63709edb1`;
- row hashes SHA-256:
  `925b4c51ea0c6ee2142a4b4fdf4c20cedb351fb24044c953fa5faf3652cefc81`;
- deterministic gzip SHA-256:
  `9c2a596f3b981d24baa039e02c72e5270889d145dc146963532f3dedebc94025`.

All `38/38` targeted re-signed attacks are rejected, including a coordinated
row + ledger-object + gzip-byte + result-object re-signing attack.  Independent
verifier cold replays with `PYTHONHASHSEED/--seed` `290071` and `290929` are
byte-identical.

The verifier source SHA-256 is
`3fcfaa67a4784fe66bb025a20d72035922933be672d5c48778d5b7e26e20ef91`.
The verification JSON file SHA-256 is
`94a8b1a3a0274bfb14d6f9e9b00d896673792548220e309b0211f2f2e3367b51`;
its embedded verification-object SHA-256 is
`138097bc8d8400f5eef957fba5b06d363d90b1a3857b97621647dde48c258c68`.

The runtime package is `python-flint==0.9.0` at `256`-bit Arb precision.
The producer result's legacy field named `python_flint_version` contains a
rendering of the full FLINT context, not the package semantic version; the
independent verification records and hard-checks the actual package version
separately.

## Fail-closed contract

The producer contains a closed failure-residual ledger.  A Round269/Round270
failure is emitted only after the complete ordered rational catalogue is
exhausted.  A Round271/Round272 failure is emitted only after all `61` nested
dyadic depths fail.  Any such row is preserved verbatim and receives zero
credit.  The frozen Round290 residual ledger has row count `0`.

Neither a whole-leaf envelope nor a zero-volume point witness can satisfy this
gate.

## Frozen nonpromotion baseline

- expanded occurrences: `126,468`;
- quotient components: `63,224`;
- maximality: `0/63,224`;
- exact-key fibres: `0/116`;
- dispositions: `0/224,580`;
- Gate5: `10/18`;
- D02: `BLOCKED`;
- CM2: `NO-GO_FOR_CLAIM`;
- true-seam credit: `0`;
- `Jx/Jy` same-point glue credit: `0`.

## Required next

1. A later explicit occurrence-promotion round may consume the independently
   verified Round288 corridor partition and Round290 isolated partition.
2. That round must issue occurrence identities transactionally; Round290
   itself supplies no formal promotion or component credit.
3. The `152` true seams, final DSU, maximality, all `116` fibres, and all
   `224,580` dispositions remain downstream gates.
