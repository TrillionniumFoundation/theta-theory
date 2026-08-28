# Paper IV theorem interface

## Imports

- `P3-DOOB`
- `P3-RWIP`
- `P3-NAHOM`
- `P3-RWIP-OPTIMAL-WETA-P` (optional quantitative block-rate input)

Paper III's basic HJB/theta result is not re-proved here. The game and filter
branches use the control-uniform K2 characteristics.

## Exports

- `P4-FILTER-B`: bounded filter contraction plus vanishing-initial-layer value
  collapse.
- `P4-FILTER-W`: weighted filter theorem with Lyapunov, moment, initial-layer,
  and comparison gates.
- `P4-WEIGHTED-NONCOMPACT-ACTUAL`: actual unbounded AR(1) hidden signal driven
  by a deterministic countable full-branch map, with a polynomial Lyapunov
  function, invariant posterior moment ball, and exponentially stable weighted
  filter; normative proof:
  `../../maximal-strengthening/WEIGHTED_NONCOMPACT_PATH_ACTUALIZATION.md`.
- `P4-SEQ`: sequential lower and upper HJB limits.
- `P4-MIXED`: simultaneous relaxed mixed-Isaacs value.
- `P4-PURE-GATE`: compatibility alias for a submitted pure-saddle
  certificate.
- `P4-PURE-ISAACS-MAXIMAL`: exact compact-action equivalence
  `pure saddle <=> H^-=H^+`, measurable saddle selection, unique saddle on
  uniformly strong concave-convex and finite strict-margin classes, and an
  actual four-branch quadratic-bilinear pure game; normative proof:
  `../../maximal-strengthening/PURE_STRATEGY_ISAACS.md`.
- `P4-BELIEF`: belief-state HJB.
- `P4-PATH`: path-state DPP and PPDE interface.
- `P4-ACTUAL-4B`: actual hidden-symbol realization through exact filter
  collapse, lower/upper monotone schemes, relaxed mixed-Isaacs scheme,
  comparison, and convergence; see `TECHNICAL_APPENDIX_GAME_SCHEME.md`.

## Pure-strategy scope

General pure-saddle existence is false, as shown by matching pennies. Mixed
minimax cannot be promoted to pure feedback. The maximal general theorem is
the exact pure-Isaacs equivalence plus a measurable selector when the saddle
correspondence is nonempty. The actual positive class is strong
concave-convex, which yields a unique Lipschitz pure selector.

## Non-exports

- pure Isaacs equality from mixed minimax alone;
- value collapse from a bounded filter Lipschitz estimate alone;
- weighted PDE uniqueness from Lyapunov coupling alone;
- an actual weighted filter without an explicit noncompact signal, moment ball,
  and observation-gap calculation.
