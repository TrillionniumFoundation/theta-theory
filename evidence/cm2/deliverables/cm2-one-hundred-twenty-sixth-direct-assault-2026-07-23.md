# CM2 one-hundred-twenty-sixth direct assault

Date: 2026-07-23

Result: **38/38 re-signed semantic mutations and 12/12 strict-JSON attacks
rejected.**

## Semantic assault contract

Each semantic attack starts from a deep copy of the canonical Round126
certificate.  Affected map rows, F18 rows, aggregate registries, and the outer
result digest are re-signed before evaluation.  Acceptance therefore cannot
be prevented merely by a stale stored hash.

The 38 attacks cover:

- schema swaps, missing or unknown result fields, and status downgrades;
- altered upstream pins and broadened scope;
- changing the direct-standard-`N` route into a Wiener or global theorem;
- altered stage lengths, path exponents, prefix/suffix monomials, or
  structural field semantics;
- false Wiener invertibility, aperiodicity/Kac closure, global phase, or CM2
  claims;
- corrupt immutable word keys, operator-carrier hashes, field counts, source
  bindings, or source canonical digests;
- reordered F1–F17 maps or F18 rows;
- wrong local level/child counts or certified-field registries;
- a smuggled global complete-block count, global maturity upgrade, Gate5
  block, or `GO_FOR_CLAIM`.

All 38 re-signed candidates fail the independent exact reconstruction.

## Strict JSON assault

The strict parser rejects all 12 byte-level attacks:

```text
duplicate top-level schema key
duplicate nested status key
floating-point integer
NaN
positive Infinity
negative Infinity
UTF-8 BOM
invalid UTF-8
unpaired surrogate
top-level array
trailing second document
closed-envelope extra field
```

Duplicate keys, non-finite values, floating JSON numbers, encoding faults,
wrong top-level types, trailing documents, and envelope widening are all
fail-closed.

## CLI fail-closed checks

```text
valid canonical certificate                 rc=0, PASS
missing certificate                         rc=1, no output
tampered certificate with stale digest      rc=1, no output
tampered and fully re-signed certificate    rc=1, no output
```

Two distinct `PYTHONHASHSEED` values produce byte-identical verification
artifacts.  The producer likewise reproduces the canonical certificate
byte-for-byte.

## State after assault

```text
children                                      24
F1–F17 slots                                2040
F18 slots                                    120
combined child-local slots                  2160
seed-local maturity                         18/18
seed-local level blocks                       120
seed-local child packets                       24
global Gate5                                10/18
global complete blocks                          0
Gate5 blocks                                    0
CM2                                  NO-GO_FOR_CLAIM
```

The assault specifically protects the distinction between seed-local
structural registration and a global physical operator theorem.
