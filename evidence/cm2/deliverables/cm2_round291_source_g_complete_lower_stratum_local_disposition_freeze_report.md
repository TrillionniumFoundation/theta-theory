# CM2 Round291: complete lower-stratum local-disposition freeze

Date: 2026-07-29  
Status: `PASS_INDEPENDENT_ROUND291_COMPLETE_LOWER_STRATUM_LOCAL_DISPOSITION_FREEZE__ZERO_CREDIT`

## Scope and claim boundary

Round291 independently reopens all 55,428 nominal lower-stratum supports from
Round267 and reconstructs their local physical-existence/absence disposition
from the pinned Round174, Round179, Round182, Round204, and Round208
artifacts.

Round280 and Round281 producers and outputs are not read or trusted.  The
Round291 producer is treated by the verifier only as inert pinned bytes and
is never imported or executed.  The verifier finishes its expected
reconstruction before opening the candidate ledger or result.

This is a local disposition result only.  It issues no expanded-occurrence,
component-edge, maximality, exact-key-fibre, global-disposition, or Jx/Jy
same-point glue credit.

## Complete local census

The full Round267 nominal universe is recovered without orphan, duplicate, or
unresolved rows:

| Local disposition | Count |
|---|---:|
| Whole physical support | 39,252 |
| Whole support absent | 16,168 |
| Partitioned physical and absent | 8 |
| Unresolved | 0 |
| Total | 55,428 |

The canonical support-kind input partition is:

| Canonical support kind | Count |
|---|---:|
| Nominal regular zero set if present | 30,444 |
| Nominal regular factor union if present | 24,656 |
| Nominal transverse pair candidate | 328 |

Evidence-basis conservation:

| Basis | Count |
|---|---:|
| Round182 explicit full/clipped 2D graph sheet | 38,244 |
| Round182 exhaustive empty closed collar | 15,492 |
| Round182 strict transverse 1D line | 112 |
| Round182 strict same-sign pair absence | 216 |
| Round204 explicit half-open 2D sheet lineage | 32 |
| Round208 explicit residual outgoing graph sheet/sides | 52 |
| Round208 exhaustive residual outgoing emptiness | 4 |
| Round179 exact two-child fully-replaced cover | 396 |
| Round204 positive-t exact owner | 440 |
| Round204 complete positive-owner shadow cover | 372 |
| Round174 complete positive-parent absence | 60 |
| Exact mixed shadow/absence partition | 8 |

The eight mixed rows are parent dispositions only; no whole-row physical
credit is issued.  Their exact physical and absent child cells are recorded
separately.

## Fully-replaced-origin reconstruction

The 396 Round179 fully-replaced nominal origins are reconstructed as:

```text
284 outgoing supports
112 wall supports
```

Each origin is covered by exactly two resolved `p` children, with no retained
or guard child and exact rational coordinate-volume conservation.

The 112 wall supports (224 children, 448 endpoint factors) are evaluated on
the complete rational child box using a local pure-`Fraction` interval
implementation.  Square roots use exact 256-bit dyadic outward enclosures
constructed with integer square root.  No `python-flint`, Round179 verifier,
or other executable evaluator is imported.

All factors are strict.  The support-level sign-pair census is:

```text
negative | negative: 48
positive | positive: 48
negative | positive:  8
positive | negative:  8
```

The smallest certified endpoint-factor margin is greater than `1/6000`; the
smallest discriminant lower bound is greater than `3/50`.  No precision tail
or extra subdivision remains.

## Exact t=0 owner/shadow partition

The remaining 880 factor sheets are decided by the pinned outcome-blind
positive-t half-open owner policy over the complete Round174 parent universe:

```text
440 positive-t owners
372 complete negative-t shadows
 60 complete absences
  8 exact mixed shadow/absence partitions
```

Exact face-area conservation:

```text
total:     31/640
physical: 59/1280
absent:    3/1280
delta:          0
```

## Determinism and independent verification

Producer seeds `291071` and `291929` are byte-for-byte identical:

```text
ledger SHA256:
  412b616b2cf75ef1373d98086cfcb2eb90a8c544e9f6b4d16a673f6cfeeb57ab
result file SHA256:
  f07aae7d12b9d33aea0313737b7dafa51b22c1c8b1e5526ecf87ad53c5a8f705
result object SHA256:
  2397c4d1e83155fdf1c8cd625fb772be0a5c39e1b758d6f7e5ae7bb8131dbc77
```

The cacheless verifier independently rebuilds every row, ID, provenance
reference, witness cell, disposition, canonical sort, row digest, ledger
digest, deterministic gzip byte, result field, and result self-digest before
opening the candidate.

It then proves full row/ledger/result equality and rejects 23/23 independently
resigned row/ledger/gzip/result attacks.  The producer's separate 28/28
self-attacks also reject all attempted credit, route, evidence, binding,
classification, count, and digest forgeries.

Verifier commitments:

```text
verifier SHA256:
  4f7940564dd60a19cbc25b9348c794aeae0cdac386f835de37b868e2edd24512
verification file SHA256:
  8011e1de7de9c931db3b6626523bda3757beb07e7dbcd3645ad4413ae5af148e
verification object SHA256:
  705469f37b2b68a8a79ea6e5075525f13aba9ed48cb5d2eef2fd3ae24c3b5b68
```

## Strict non-promotion

Whole-absent rows are explicitly marked
`NO_OCCURRENCE__LOCAL_ABSENCE`.  Physical rows and only the physical cells of
partitioned rows remain `PENDING_FINAL_OCCURRENCE_REGISTRY`.

The global baseline therefore remains:

```text
expanded occurrences: 126,468
quotient:               63,224
maximality:             0/63,224
exact-key fibres:       0/116
global dispositions:    0/224,580
Gate5:                  10/18
D02:                    BLOCKED
CM2:                    NO-GO_FOR_CLAIM
Jx/Jy glue credit:      0
```

## Next gate

Bind every physical witness or shadow patch—and only the physical child cells
of the eight mixed rows—to the independently frozen final occurrence registry
using exact provenance, geometry, complete signature, and exact-key identity.
Absence rows bind to no occurrence.  Only after this binding is complete may
the 152 true-seam patches enter the DSU and the maximality/fibre exhaustions
begin.

