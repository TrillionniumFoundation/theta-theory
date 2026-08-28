# Paper IV theorem interface

## Imports

- `P3-DOOB`
- `P3-RWIP`
- `P3-NAHOM`

Paper III's basic HJB/theta result is not re-proved here.  The game and filter
branches use the control-uniform K2 characteristics.

## Exports

- `P4-FILTER-B`: bounded filter contraction plus vanishing-initial-layer value
  collapse.
- `P4-FILTER-W`: weighted filter theorem with Lyapunov, moment, initial-layer,
  and comparison gates.
- `P4-SEQ`: sequential lower and upper HJB limits.
- `P4-MIXED`: simultaneous relaxed mixed-Isaacs value.
- `P4-PURE-GATE`: additional pure-saddle certificate.
- `P4-BELIEF`: belief-state HJB.
- `P4-PATH`: path-state DPP and PPDE interface.
- `P4-ACTUAL-4B`: actual hidden-symbol filtering/game realization.

## Non-exports

- pure Isaacs equality from mixed minimax alone;
- value collapse from a bounded filter Lipschitz estimate alone;
- weighted PDE uniqueness from Lyapunov coupling alone.
