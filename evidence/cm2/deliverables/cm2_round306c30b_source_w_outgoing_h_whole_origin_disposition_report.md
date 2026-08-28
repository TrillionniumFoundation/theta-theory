# CM2 Round306C30b — Source-W outgoing-H whole-origin disposition

## Verdict

`PASS_FORMAL_C30B__688_H_CELLS__2_WHOLE_ORIGIN_EXCLUSIONS__10_RESOLVED_MIXED__SOURCE_W_92_TO_80__D02_STILL_BLOCKED`.

C30b disposes the complete outgoing-H lane inherited from the formally sealed C30a frontier. It resolves 12 original physical Source-W origins, but only two are whole-origin exclusions. The other ten contain complete, positive-measure `LIVE`/`MIXED` ownership and are recorded as `RESOLVED_MIXED` rather than exclusions.

This distinction is mandatory: 12 dispositions are not 12 exclusions.

## Exact result

The 688 H cells are reconstructed from four disjoint sources:

| Source | Cells |
|---|---:|
| Round215 residual outgoing-H | 560 |
| Round180 inherited outgoing-H | 112 |
| Round180 inherited same-sign Delta follow-up H | 8 |
| C30a held inherited outgoing-H | 8 |
| **Total** | **688** |

Their dispositions are `352 EXCLUDED + 144 LIVE + 192 MIXED = 688`.

The 12 whole-origin dispositions are:

| Disposition | Origins |
|---|---:|
| `EXCLUDED` | 2 |
| `RESOLVED_MIXED` | 10 |
| **Total** | **12** |

The two excluded origins are:

```text
W:N:07.01.01100010
W:S:H.07.01.01100010
```

## Whole-origin ownership proof

The independent verifier does not import or execute the C30b producer. It rebuilds the pinned Round176/Round184/Round215/C30a boundary, captures the unique first-pass Round176 closure inside the same Round215 replay, and independently reconstructs all candidate rows and the result object.

For the 12 origins it checks:

- 5,942 positive-volume 3D leaves;
- 1,665,956 unordered 3D interior-disjointness tests;
- 6,002 raw 2D and 43,634 raw 1D strata;
- 27,974 atomic 2D, 36,244 atomic 1D, and 14,224 atomic 0D half-open owners;
- exact containment, volume exhaustion, unique ownership, and pointwise disposition closure.

The atomic disposition census is `73,720 EXCLUDED + 3,212 MIXED + 1,510 LIVE`. No child count, rational volume, single face, finite-depth subdivision, or sampled observation is converted into a whole-origin integer exclusion.

## Conservative Source-W ledger

```text
before: excluded 74,744; conservative_live 2,088; resolved_nonexcluded 1,996; remaining 92
credit: 2 exclusions; 10 resolved nonexcluded; 12 resolved dispositions
after:  excluded 74,746; conservative_live 2,086; resolved_nonexcluded 2,006; remaining 80
conservation: 74,746 + 2,086 = 76,832
```

C30a corrected the earlier proposed `252 -> 90` path to the auditable `252 -> 92`. C30b now formally advances `92 -> 80`.

The remaining 80-origin frontier is:

| Lane | Origins |
|---|---:|
| full-Delta | 2 |
| multi-Delta | 20 |
| reduced-live | 2 |
| retained physical source seams | 2 |
| compact-q | 54 |
| **Total** | **80** |

## Hardening and publication

- two controlled producer seeds yielded four byte-identical files;
- the final independent verifier passed against both controlled candidates and the published sealed copy;
- 13/13 coherent corruptions were rejected with exact `Reject` types and reason prefixes;
- the published four-file copy is byte-identical to the official controlled candidate;
- the scrubbed syscall replay emitted one canonical stdout JSON object, read no historical `c30b-final-*` or `c30b-sealed-*` candidate, and made zero writes or path mutations under `deliverables/` or `.cm2-runtime/candidates/`;
- the 14-member manifest must pass before the final verifier replay begins, and the replay must reproduce the phase-one canonical stdout without modifying published files.

Published result object SHA256: `7abf8da628eb35b20ed27b032dc55ea29e9944530d2d5a6a64993a995f1ad85e`.

## Strict nonpromotion

```text
D02 = BLOCKED_BY_80_REMAINING_SOURCE_W_ORIGINS_AND_COMPOSITE_GATE
D03 = UNAUTHORIZED
D04 = NOT_MINTED
Gate5 = 10/18
complete global 18-field blocks = 0
CM2 = NO-GO_FOR_CLAIM
```

C30b does not authorize C30c or any later lane automatically. Each later lane must consume a fixed sealed authority, independently reconstruct complete 3D/2D/1D/0D ownership, pass true controlled-seed and corruption tests, and receive its own manifest before any formal credit.
