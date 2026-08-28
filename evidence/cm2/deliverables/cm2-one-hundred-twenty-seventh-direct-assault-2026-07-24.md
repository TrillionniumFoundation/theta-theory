# CM2 one-hundred-twenty-seventh direct assault

Date: 2026-07-24

Result: **61/61 fully re-signed semantic mutations and 14/14 strict-JSON
attacks rejected.**

## Re-signed semantic assault

Every semantic attack starts from a deep copy of the canonical Round127
certificate.  Affected field-binding aggregates, row hashes, list aggregate
hashes, and the outer result digest are recomputed before verification.
Rejection therefore depends on independent reconstruction and semantic
constraints, not merely on stale stored hashes.

The 61 attacks cover the following surfaces.

### Envelope, scope, and incidence semantics

- schema swap, missing result field, and unknown result field;
- status or terminology promoted from incidence to physical coverage;
- global domain decisions or a concrete global nonempty census falsely
  installed;
- `120` seed-local bases assigned a global symbolic denominator;
- altered word and word/roof incidence numerators or fractions;
- broadened all-Borel-key scope or removed nonclaims.

### Global registry membership

- tampered global word ordinal;
- tampered retained-pair or crossing-pattern ordinal;
- changed global word row target or row digest;
- altered return length or reordered official word rows;
- tampered frozen 441280-row stream digest.

### Relative / absolute namespace

- second-leg relative target changed from `G[1,1]` to the absolute owner
  `G[0,0]`;
- namespace-separation flags disabled;
- global-domain or physical-coverage claims installed on one word row.

### Pinned root chain

- altered Round113 path ID;
- altered Round117 operator-cell ID;
- altered Round121 exact-seed ID;
- altered upstream Round126 certificate pin.

### Subbranch and carrier joins

- changed common rank or physical homogeneity;
- seed-local subbranch promoted to a global registry entry;
- changed carrier stage, roof split, operator digest, or physical scope;
- changed immutable base roof, stage, operator carrier, or F18 source row
  hash.

### Exact-once field and slot census

- duplicated field index;
- changed source round;
- changed source canonical row hash followed by full re-signing;
- duplicated slot ID or injected an orphan slot ID;
- reduced the base field count or promoted one base to a global block;
- reduced the slot census or disabled exact-once/same-root flags;
- reordered base rows.

### Global nonpromotion

- promoted 120 local levels into global blocks;
- promoted complete-block or Gate5-block counts;
- upgraded global maturity to 18/18;
- changed Gate5 status to `CERTIFIED`;
- changed CM2 to `GO_FOR_CLAIM`.

All 61 candidates fail the independent exact-rational registry replay or
the exact Round113–Round126 reconstruction.

## Strict JSON assault

The byte-level parser rejects all 14 attacks:

```text
duplicate top-level schema key
duplicate result status key
closed envelope extra key
closed result extra key
floating-point integer
NaN constant
positive Infinity constant
negative Infinity constant
UTF-8 BOM
invalid UTF-8
unpaired surrogate
top-level array
trailing second document
stale outer result digest
```

Duplicate keys, widened schemas, floating and non-finite JSON values,
encoding faults, wrong top-level types, trailing documents, and stale outer
signatures are all fail-closed.

## CLI and deterministic assault

```text
valid canonical certificate                rc=0, PASS
missing certificate                        rc=1, no output
tampered schema certificate                rc=1, no output
```

Two full producer/verifier cold replays used `PYTHONHASHSEED=127031` and
`127249` with `LC_ALL=C`, `TZ=UTC`, and bytecode disabled.  Both producer
certificates and both verification artifacts are byte-identical to their
frozen counterparts.

## Frozen executable and artifact hashes

```text
producer       ea461b3ed1301149bca350f32190348aca955f0a04ce42663fab23451144b0dd
certificate    4aa7cde5e22883dfcb8e59f16e7bd6ab16c4436229c9964384ef72dda0c16408
verifier       24de0b53c872d43f0a0d7422164e5a2a776a1d35879c923bcf5a07afef94e157
verification   5958b4905b8e005886302a6bffc32d15fd1091cf8dbe20b743488e3f91eeb383
```

## State after assault

```text
global symbolic word keys                  441280
global symbolic word/roof positions       3286976
exact path official words                       3
exact path symbolic word/roof positions         5
Round121 refined subbranches                   24
word/subbranch carriers                        72
seed-local base keys                          120
seed-local field slots                       2160
seed-local maturity                         18/18
global Gate5                                10/18
global complete blocks                          0
Gate5 blocks                                    0
Gate5 status                        NOT_CERTIFIED
CM2                                  NO-GO_FOR_CLAIM
```

The assault protects the exact boundary between symbolic membership,
seed-local operator registration, and absent global physical coverage.
