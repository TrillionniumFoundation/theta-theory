# Round300-D independent closure report

## Verdict

PASS: the sealed Round295-A lower-physical-witness ledger projects to exactly
111,524 canonical unordered **incidence edges**, plus 1,600 one-target
assignment exclusions.

The word “edge” in this package has the narrow value
`CANONICAL_TWO_TARGET_LOWER_PHYSICAL_WITNESS_INCIDENCE_EDGE`.  It does not
denote topological occurrence-union connectivity and it cannot be applied to
a component DSU.  No included-stratum plus two-attachment/corridor gluing
lemma is pinned here.

## Exact reconstruction

| Item | Exact result |
|---|---:|
| Complete Round295-A incidence rows | 113,452 |
| One-target assignment-only rows | 1,600 |
| Two-target raw witness rows | 111,852 |
| Distinct two-target endpoints | 223,048 |
| Canonical unordered incidence edges | 111,524 |
| Duplicate two-target witness rows | 328 |
| Self pairs | 0 |
| Same-final-key edges | 86,308 |
| Cross-final-key edges | 25,216 |
| Unkeyed target occurrences | 0 |
| DSU-eligible edges from this package | 0 |

Two-target raw witness families are GRAPH 111,524, NEG_T0 128,
TRANSVERSE 112, and POS_T0 88.  Canonical edge witness multiplicity is
`{1:111380, 2:56, 3:32, 4:16, 5:40}`.

Raw endpoint tranches are 111,660 R288–R288 witness rows and 192
preserved–preserved witness rows.  Canonical tranches are 111,332 R288–R288
edges and 192 preserved–preserved edges.  There are no mixed-tranche or R292
endpoint edges.

For cross-key edges, the lowest-source-row canonical primary witness family is
GRAPH 25,119, NEG_T0 27, POS_T0 29, and TRANSVERSE 41.  The complete raw
cross-key witness family census, retaining extra witnesses on multiply
witnessed pairs, is GRAPH 25,216, NEG_T0 128, POS_T0 88, and TRANSVERSE 112.
These are deliberately separate censuses.

The 1,600 assignment rows mention 1,216 distinct occurrences: 96 also occur
as two-target endpoints and 1,120 occur only in assignments.  Therefore the
complete target set reopened against Round294 has 224,168 occurrences.  It
contains 1,396 preserved Round266 occurrences, backed by 122 distinct
Round266 component-root rows.

## Sealed boundary

The producer and independent verifier directly byte-pin:

- Round295-A package and the complete 113,452-row physical-incidence ledger;
- Round294 registry/result/verification and the complete 431,208-row registry;
- Round299-A package and the complete 9,404-row refined binding table,
  establishing the final 124-key universe without merging keys;
- Round266 certificate/verification, including independent recommitment of
  all 126,468 expanded occurrence-member rows and all 63,224 component-root
  rows.

The verifier never imports, executes, or parses the Round300-D producer.
Producer bytes are used only as the inert SHA-256 pin
`56e414eba093fb0ceb9a78895b94b63ccff3beaf590b05d4e969d43d767ac333`.
Expected rows and deterministic gzip bytes are rebuilt cachelessly from the
sealed mathematical sources.

## Formal credit boundary

Every canonical row has incidence-edge credit 1.  Every assignment exclusion
has incidence-edge credit 0.  All of the following remain exactly zero:

- occurrence-identity collapse and official-key merge;
- formal component edge, component union, and component quotient;
- component DSU eligibility and DSU rank reduction;
- seam and Jx/Jy glue;
- maximality, fibre, and global disposition.

The historical value 29,984 is retained only as an uncomputed diagnostic
hypothesis.  It receives no formal rank credit and no quotient count is
issued.  Same-key is not an identity/connectivity shortcut; cross-key is not
an exclusion or a license to merge official keys.

## Independent attacks

The independent attack suite rejects 60 of 60 attacks, including 48
semantically reclosed mutations.  Covered classes include:

- forged DSU eligibility, component edge/union/quotient, rank reduction,
  topological glue, identity collapse, key merge, maximality, fibre, and
  disposition;
- single-target assignment mispromotion and self-pair/endpoint mutation;
- same-key shortcut, cross-key rejection, and cross-key key merging;
- source witness count/kind/hash, Round294 registry, tranche, and Round266
  member/root tampering;
- promotion of the diagnostic 29,984 value;
- row deletion/addition/reordering with recomputed commitments;
- gzip mtime/payload/concatenated-member, output-path, and manifest attacks.

Attack suite: file SHA-256
`b0b201a2c3f7255bd9d386bead2ab1e7b66711581d1cf09033cb4edfe267fbcf`;
self SHA-256
`85f057a5a716d5f1e205bc8813ba1ccfd7fee20bf0e17038da8d858f9b28e1b8`.

## Replays and resources

Producer alpha (`seed=300401`) passed in 444.83 s wall time with maximum RSS
998,016 KB.  Producer beta (`seed=987654321`) passed in 418.95 s wall time
with maximum RSS 1,001,500 KB; its ledger and result are byte-identical to
alpha.

Verifier alpha (`seed=300411`) passed in 464.00 s wall time with maximum RSS
1,137,280 KB.  Verifier beta (`seed=300499`,
`PYTHONHASHSEED=733`) passed in 468.04 s wall time with maximum RSS
1,138,024 KB; its attack suite and verification artifact are byte-identical
to alpha.

The cold replay procedure checks both seed runs for byte identity, validates
single-member deterministic gzip, result/verification self-closure,
single-link regular-file confinement, and the final eight-member manifest.

## Stable artifact pins before report/manifest

- producer:
  `56e414eba093fb0ceb9a78895b94b63ccff3beaf590b05d4e969d43d767ac333`
- incidence-edge ledger:
  `287d1382b25fd3d5cd0a52c6da8cabbb012040b8a6e35c9f887d7a425b812fa7`
- result file:
  `59b7e788ed217ceb590a3e2125cc13aefbf447af236315ea607f4f631cb29c84`
- result self-closure:
  `17b9d2989f7616b74db5a11adda13eff971f43e737211bb488a8a2a7db4c156e`
- independent verifier:
  `d7fbbeeb3f0959de54e55f20928f276a36df75100907b1af16bb2e46317ddc26`
- attack suite file:
  `b0b201a2c3f7255bd9d386bead2ab1e7b66711581d1cf09033cb4edfe267fbcf`
- verification file:
  `a5bd12b10103b4785574bd4633e608c7fd5107369ba8f2343ebffe7e08eba1c7`
- verification self-closure:
  `523c96fcc0a428912c8cb6a73b75fbe7b115e965643b1b2965a6c624e093a60f`
