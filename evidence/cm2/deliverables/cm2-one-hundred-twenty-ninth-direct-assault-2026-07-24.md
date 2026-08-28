# CM2 one-hundred-twenty-ninth direct assault

Date: 2026-07-24

Result: **77/77 re-signed semantic mutations and 16/16 strict-JSON attacks
rejected.**

## Assault model

Every semantic attack begins with a deep copy of the official Round129
certificate.  After mutation, the harness recursively recomputes:

```text
affected row_sha256 values
affected nested list/object aggregate SHA256 values
outer result_sha256
```

Rejection therefore depends on the independent interval replay, registry
reconstruction, typed crosslinks, exact-once schemas, and fail-closed safety
contract rather than on a stale signature.

The verifier never imports or executes the Round129 producer.

## Provenance and lambda-sheet assault

The suite rejects changes to:

- the certificate schema, status, or precision;
- any frozen primary or verification pin;
- the analytic family-root ID, Round112 sheet kind, branch, or parent cell;
- `c0`, lambda center, radius, or closed collar;
- uniform t-root face signs;
- the signs or enclosures of `F_t`, `F_lambda`, `dt/dlambda`, or
  `db/dlambda`;
- strict monotonicity of `b(lambda)`;
- the positive lower bound on the Borel image length.

The independent replay checks

```text
F = Delta3 + (16/625)lambda^2
F_lambda = (32/625)lambda
-8 < F_t < -7
dt/dlambda > 0
db/dlambda > 0
```

and reconstructs the stable family ID from exact rational data.

## Parameter-namespace assault

Attacks that identify or substitute the two parameters are rejected:

```text
lambda = b3 exact-fibre coordinate
s      = physical horizontal W-translation
```

The suite mutates `lambda_is_not_s`, replaces the `s` collar by the lambda
collar, disables identifier separation, and attempts to finite-enumerate the
uncountable parent-W registry.  All fail.

## Recut and common-rank assault

The verifier rejects:

- stage-orientation and natural-cell-count changes;
- cut-count or cut-order changes;
- invalid U1/U2 length or derivative enclosures;
- duplicate, reordered, or relabelled endpoint guards;
- changed endpoint IDs, exact equations, signs, uniqueness, or dyadic
  brackets;
- duplicate recuts, wrong face references, wrong orientations, or removal of
  actual-per-fibre materialization;
- duplicate common ranks, zero or inflated gaps, changed stage coverings,
  changed path IDs, or broken recut references.

It independently checks all 23 root-face guards and all 24 positive gaps.
Every recut and common-rank ID is rebuilt from the family root, exact stage,
natural index, and fixed analytic constructors.

## Physical five-face/seven-boundary assault

The following re-signed mutations are rejected:

- changing the 4056 candidate-tangency census;
- lowering any stored physical minimum through its claimed margin;
- setting the physical-empty conclusion false;
- inventing a physical five-face or residual incidence;
- changing a C24 core-face count or core incidence;
- deleting a five-face row or changing a seven-boundary instance count;
- changing a 57/55/57 candidate-stage census;
- relabelling the designated BYPASS `b3` as a collision angle;
- replacing actual owners, charts, or the diagnostic/F11 distinction.

The independent `lambda × s` replay verifies all twelve typed predicates,
169 candidates per rank, 24 common ranks, 1152 core-face checks, and zero
physical face incidence.

## Artificial-face assault

The suite rejects:

- changing the 25-face, 48-trace, or 24-incidence census;
- erasing the artificial registry after the physical-empty statement;
- relabelling a moving or stationary artificial face as physical;
- clearing `artificial_not_physical`;
- merging lambda and `s` on a moving face;
- orphaning a trace or common-rank reference;
- changing an incidence face/trace pair;
- inventing a physical incidence on an artificial child boundary.

The verifier reconstructs each face, trace, and incidence template ID and
requires every common rank to retain exactly two artificial boundary faces.

## Base and field-template assault

The verifier independently rebuilds the 120 base templates and all 1680
field templates from pinned Round121/Round122 rows.  It rejects:

- deleted or duplicated base rows;
- changed official words, stages, roofs, common ranks, or recut references;
- treating a template as a pre-enumerated actual family key;
- deleted, duplicated, or relabelled field rows;
- inserting F14 into the certified field set;
- changing inherited field values or bound semantics;
- breaking face-incidence references for F7–F13/F16;
- using along-curve diagnostics as F11;
- changing a full-phase F11 envelope;
- promoting the fixed three-leg F6 statement to arbitrary return depth.

Every one of the 120 base templates must carry exactly one instance of

```text
F1,F2,...,F13,F16.
```

## Count and global-promotion assault

The suite rejects:

- assigning a finite whole-family child or slot count;
- changing any finite template or per-fibre count;
- installing F14/F15/F17/F18 on the positive-Borel family;
- promoting local maturity from 14/18 to 18/18;
- promoting global Gate5 from 10/18;
- inventing a global complete block or Gate5 block;
- changing CM2 to go-for-claim;
- widening the strict scope or deleting a strict nonclaim.

The finite `1680` registry is simultaneously a finite template census and a
per-exact-fibre actual-slot count.  It is never the cardinality of all actual
slots across the uncountable family.

## Strict JSON assault

The byte parser rejects all 16 attacks:

```text
duplicate top-level schema key
duplicate nested precision key
floating-point integer
exponent-form number
NaN
Infinity
UTF-8 BOM
invalid UTF-8
negative zero
oversized integer
unpaired surrogate
top-level array
closed-envelope extra key
closed-result extra key
stale outer result digest
noncanonical rational fraction
```

The parser forbids JSON floats and nonfinite constants, enforces int64
canonical integers, rejects duplicate keys and invalid Unicode, and closes
both the envelope and result schemas.

## CLI, link, and nonregular-file assault

```text
valid official certificate       rc=0, PASS
missing certificate              rc=1, output absent
tampered certificate             rc=1, output absent
certificate symlink              rc=1, output absent
certificate hardlink             rc=1, output absent
certificate FIFO                 rc=1, output absent
output symlink                   rc=1
output hardlink                  rc=1
output FIFO                      rc=1
```

The protected output set covers the official certificate, producer,
verifier, all 36 frozen primary files, and all six mathematical helper
files.  Both resolved path and inode identity are checked.

Two full verifier runs with `PYTHONHASHSEED=0` and `987654321` produced
byte-identical artifacts.

## Frozen hashes

```text
producer
  bb0884aa14c256d16acd86c47ef1bf75e910507fa0b9334be704a6ee3995a054
certificate
  1e2527ddb73158554ad238ff2f9f7fd6cb805f80d55bdafd770a8c9c1688d762
verifier
  64c20bae8ea2944cb8487b253f9e0ff0a1a68a0c11fe0cd8d6d2206427981ea7
verification
  4d22ba14e44fe05bf564914d05b335a831f375560e6fbd6b31831f52eb6351db
```

## State after assault

```text
positive-Borel local maturity       14/18
per-exact-fibre children                24
per-exact-fibre base keys              120
per-exact-fibre F1-F13/F16 slots      1680
physical face incidences                  0
global complete 18-field blocks          0
Gate5 blocks                             0
global Gate5 maturity                10/18
Gate5 status                 NOT_CERTIFIED
CM2                         NO-GO_FOR_CLAIM
```

The assault protects the boundary between a rigorously parameterized local
Borel family and absent global arbitrary-return, all-word, same-root
18-field coverage.
