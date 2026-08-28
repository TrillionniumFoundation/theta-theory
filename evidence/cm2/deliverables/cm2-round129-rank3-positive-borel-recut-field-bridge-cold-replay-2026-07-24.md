# CM2 Round129 cold replay

Date: 2026-07-24

## Frozen digests

```text
producer
  bb0884aa14c256d16acd86c47ef1bf75e910507fa0b9334be704a6ee3995a054
certificate
  1e2527ddb73158554ad238ff2f9f7fd6cb805f80d55bdafd770a8c9c1688d762
certificate result
  79cb3501fd7d52d1a22fecf3dc0faaa979dfd9b06fea7ce7afd872b39fbf2bd5
verifier
  64c20bae8ea2944cb8487b253f9e0ff0a1a68a0c11fe0cd8d6d2206427981ea7
verification
  4d22ba14e44fe05bf564914d05b335a831f375560e6fbd6b31831f52eb6351db
verification result
  680c9cadb5612c28a157124bed9e8154dc112b4ead7d9ef46871b1c7b28f8905
```

## Two-seed producer replay

Two complete producer runs used:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=987654321
```

Each executed:

```text
python
  deliverables/cm2_round129_rank3_positive_borel_recut_field_bridge.py
  --output <cold-output>.json
```

Both runs exited `0`.  Their 6.8 MB certificates were byte-identical to one
another and to the frozen certificate:

```text
certificate SHA256
  1e2527ddb73158554ad238ff2f9f7fd6cb805f80d55bdafd770a8c9c1688d762
certificate result SHA256
  79cb3501fd7d52d1a22fecf3dc0faaa979dfd9b06fea7ce7afd872b39fbf2bd5
```

## Two-seed verifier replay

The same hash seeds were used for complete, mutation-enabled verifier runs:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=<seed>
  python
  deliverables/cm2_round129_rank3_positive_borel_recut_field_bridge_verifier.py
  --certificate
    deliverables/cm2-round129-rank3-positive-borel-recut-field-bridge-2026-07-24.json
  --output <cold-verification>.json
```

Both runs exited `0`, printed `PASS`, and produced byte-identical artifacts.
The cold artifacts are byte-identical to the frozen verification JSON:

```text
verification SHA256
  4d22ba14e44fe05bf564914d05b335a831f375560e6fbd6b31831f52eb6351db
verification result SHA256
  680c9cadb5612c28a157124bed9e8154dc112b4ead7d9ef46871b1c7b28f8905
semantic mutations                     77/77 rejected
strict-JSON attacks                     16/16 rejected
```

The verification JSON is written with sorted keys, two-space indentation,
`allow_nan=False`, and one final newline.  Its stored result digest equals an
independent canonical recomputation.

## Independently replayed mathematics

The verifier does not import or execute the Round129 producer.  At 4096-bit
precision it independently verifies:

```text
lambda center                         3/65536
lambda radius                           2^-512
fixed c0                              1/16384
uniform t-root face signs                 +,-
F_t                                     (-8,-7)
F_lambda            (1/500000,3/1000000)
dt/dlambda           (1/4000000,1/3000000)
db/dlambda           (1/2250000,1/2000000)
pullback face guards                         23
strictly positive common ranks               24
minimum guarded rank gap                 >1/200
```

It then applies the frozen independent Round122 native Jet2 layer to the full
lambda theta-guard and independent `|s|<=2^-512` collar:

```text
candidate stages                        57/55/57
candidates per common rank                    169
candidate checks over 24 ranks               4056
C24 core-face checks                         1152
integer-corner-ray checks                    2040
physical five-face incidences                   0
residual physical faces                         0
```

All twelve typed physical minima strictly exceed their frozen rational
margins.  All 23 moving artificial faces, 48 traces, and 24 child/face
incidences remain present.

## Registry replay

The verifier independently reconstructs and closes:

```text
uniform pullback guards                       23
stage recut templates                         26
common-rank templates                         24
base-key templates                           120
field-slot templates                        1680
certified fields per base                     14
```

Every base receives exactly one template for F1–F13 and F16.  The
uncountable family is not converted into a finite census; `1680` is the
per-exact-fibre actual slot count and the finite template-row count.

## Negative input and output replay

Fresh output paths were used for every negative case:

```text
valid official certificate       rc=0, PASS, output written
missing certificate              rc=1, output absent
tampered certificate             rc=1, output absent
certificate symlink              rc=1, output absent
certificate hardlink             rc=1, output absent
certificate FIFO                 rc=1, output absent
output symlink                   rc=1
output hardlink to certificate   rc=1
output FIFO                      rc=1
```

The verifier checks the official certificate byte and result hashes before
writing.  Resolved path and inode identity protect the certificate,
producer, verifier, all 36 primary upstream pins, and all six independent
mathematical helper pins.

## Safety replay

Both deterministic artifacts retain:

```text
positive-Borel local maturity       14/18
whole-family actual row census        null
global complete 18-field blocks          0
Gate5 blocks                             0
global Gate5 maturity                10/18
Gate5 status                 NOT_CERTIFIED
CM2                         NO-GO_FOR_CLAIM
```

The cold replay proves one positive-Borel local F1–F13/F16 family.  It does
not install F14/F15/F17/F18 on that family and does not promote a local
template registry into global Gate5 coverage.
