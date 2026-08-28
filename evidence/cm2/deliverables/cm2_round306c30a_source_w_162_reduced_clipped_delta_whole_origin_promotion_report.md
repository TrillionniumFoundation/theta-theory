# CM2 Round306C30a — Source-W reduced clipped-Delta whole-origin audit

## Verdict

`PASS_FORMAL_C30A__160_WHOLE_ORIGIN_EXCLUSIONS__2_INHERITED_H_HOLDS__SOURCE_W_252_TO_92__D02_STILL_BLOCKED`.

C30a independently reconstructs the pinned R184/R215/C29 boundary, disposes all 12,888 reduced clipped-Delta cells, and promotes only complete original physical parents whose inherited and newly proved 3D/2D/1D/0D partitions are all excluded.

The requested `252 -> 90` transition is not valid. Full replay found two symmetric origins with inherited positive-measure outgoing-H matching sides:

```text
W:N:04.00.10101011
W:S:H.04.00.10101011
```

They are held at zero whole-origin exclusion credit. The auditable transition is therefore `252 -> 92`.

## Exact cell and whole-origin result

The 12,888-cell partition is:

| Disposition | Cells |
|---|---:|
| reduced candidate owner mismatch, excluded | 9,900 |
| frozen owner outgoing-chart mismatch, excluded | 2,968 |
| full-Delta negative open side not excluded | 20 |
| **Total** | **12,888** |

The first two classes give 12,868 complete closed-cell exclusions. The 20 residual cells are reserved for the two full-Delta origins and receive no whole-origin credit here.

Exactly 160 of the 162 outcome-blind candidate origins have complete excluded inherited and final partitions. Their ordered-key digest is `df619f757a7176b1cea40af96944387f21e18fa249ca14c07af61c2d8092ab0e`. The two held keys have digest `7a41c001b740c99223c152d96e75176b56f6bf083df962155b912e32b43afd08`.

No child count, rational volume, individual face, finite-depth decay statistic, or analytic stratum is converted into whole-origin integer credit.

## Conservative Source-W ledger

```text
before: 74,584 excluded + 2,248 conservative live = 76,832
delta:      +160 excluded -   160 conservative live
after:  74,744 excluded + 2,088 conservative live = 76,832
unresolved whole-origin tail: 252 -> 92
```

The exact 92-origin frontier is:

| Lane | Origins |
|---|---:|
| outgoing-H | 12 |
| full-Delta | 2 |
| multi-Delta | 20 |
| reduced-live | 2 |
| retained physical source seams | 2 |
| compact-q | 54 |
| **Total** | **92** |

This corrects the earlier 90-origin plan, which omitted the two reduced-live origins.

## Independent verification and hardening

The verifier does not import or execute the producer. It rebuilds the complete R184/R215/C29 input boundary and reconstructs 12,888 cell rows, 160 promoted origin rows, two held-origin rows, and the canonical result object.

- independent rows reconstructed: 13,050/13,050;
- coherent attacks rejected: 9/9;
- two producer seeds: four output files byte-identical;
- scrubbed cold replay: passed;
- stdout-only verifier contract: one stdout write, zero candidate/deliverable writes;
- published result object SHA256: `32c449bc9af41a22ab5468d194431d14fadf5bc95b30067d639f9e4443538e09`.

The attack suite includes result-field mutations, false D02/CM2 promotions, child/volume credit, pin retargeting, fully reclosed cell and origin ledger forgeries, and a fully rehashed ledger-order attack that can be rejected only by complete source reconstruction.

## Strict nonpromotion and next work

C30a changes only Source-W whole-origin exclusion credit:

```text
D02 = BLOCKED_BY_92_REMAINING_SOURCE_W_ORIGINS
D03 = UNAUTHORIZED
D04 = NOT_MINTED
Gate5 = 10/18
complete global 18-field blocks = 0
CM2 = NO-GO_FOR_CLAIM
```

For the remaining lanes, “resolved origin” and “whole-origin exclusion” must be separate ledger fields. Frozen evidence already contains strict positive-measure `LIVE` and half-open `MIXED` strata. A complete origin may therefore be dispositioned as excluded, live, or mixed, but exclusion integer credit is legal only when every owned stratum is excluded.
