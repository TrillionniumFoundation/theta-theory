# CM2 Round274 Source-G reverse-rechart tail arrangement probe

## Status

`ROUND274_REVERSE_RECHART_TAIL_ARRANGEMENT_PROBE__ZERO_CREDIT`

This probe closes the *geometric classification* of all 56 Round273
reverse-rechart tails.  It is not yet a frozen producer/verifier certificate,
so it grants no expanded-occurrence, component, maximality, fibre, disposition,
or CM2 claim credit.

## Frozen inputs and method

- Reconstruct the 880 Round174/Round179 guards and the exact adjacent-chart
  relation `t'^2 = 1 - t^2`, `p' = p`, `s' = s`.
- Reproduce Round273's deterministic depth-9 cover on a 128-bit rational
  outward enclosure.
- Retain only the 56 guards and 5,012 cells whose complete Round174 signature
  still overwraps one genuine event equation.
- Evaluate the active event and its interval derivatives with the Round179
  256-bit dual-Arb geometry.
- Use coordinatewise strict monotonicity to select the exact minimum and
  maximum corners.  Re-run the complete Round174 signature evaluator at both
  corners.  Equal strict corner signs certify an absent zero set; opposite
  signs plus strict `t` derivative certify one regular graph and two connected
  open sides.

## Exact census

- input tail guards: **56 / 56**
- arrangement cells: **5,012 / 5,012**
- outgoing-chart-seam cells: **3,604**
- `X=0` wall-event cells: **704**
- `Y=0` wall-event cells: **704**
- regular graph crossings: **3,488**
- exact zero-set absences: **1,524**
- connected open-region signatures: **8,500**
- strict extremal evaluator successes: **10,024 / 10,024**
- cells without a strict derivative axis: **0**
- undecided cells: **0**

Every arrangement cell has a strict `t` derivative.  For G targets the active
factor is independent of `s`; for W targets the probe also obtains a strict
`s` derivative.  No precision-only subdivision is used as a proof of closure.

## Full-signature transition audit

All 1,524 absent-zero cells have byte-identical complete 10-field signatures
at their two extrema.  Every crossing cell changes exactly the fields dictated
by its sole active event:

- 2,464 outgoing-seam cells change only `outgoing_cell` and `target_chart`.
- 512 `X=0` cells and 512 `Y=0` cells change only the official exact-key
  identity/row/ordinal, ordered wall events, roof, and signed wall word.

No crossing changes owner target, source chart, or unrelated return data.

## Deterministic digests

- arrangement rows SHA256:
  `065b49c9677471445b3e8fc7466751af37939ad85d167b28fbe3add24a0db86b`
- row-hash list SHA256:
  `5254ec491bde37ace0b4eba907f0b4147e8958060e7d61152484db331305e881`
- 56 tail guard IDs SHA256:
  `f6b2b6b18b279f3aa72306b3d22e1e443c90a914026846df15750eb9edef833c`
- probe source SHA256:
  `677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292`

## Non-promotion and next gate

The strict baseline remains unchanged: quotient 63,224; expanded occurrences
126,468; maximality 0/63,224; fibres 0/116; dispositions 0/224,580; Gate5
10/18; D02 BLOCKED; CM2 `NO-GO_FOR_CLAIM`.  Jx/Jy same-point glue credit
remains zero.

The next formal gate is to convert the Round273 824-guard strict cover and this
Round274 56-tail arrangement into a pinned producer/independent-verifier pair.
Only after byte-identical dual-seed replay and attack rejection may the 152
true-seam patches be incident-bound and the final DSU recomputed.
