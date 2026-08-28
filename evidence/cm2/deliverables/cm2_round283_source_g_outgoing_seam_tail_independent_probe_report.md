# CM2 Round283 — independent outgoing-seam tail probe

Status: **analytic residual zero is feasible; formal credit remains zero**.

## Input and exact finite overlay

The probe reads only the frozen Round275, Round280, and Round282 universes.
Round282's remaining set is exactly:

- 24 true-seam patches;
- 40 directed patch endpoints;
- 48 guard-channel incidences (32 endpoints have one candidate guard and
  eight endpoints have two);
- 540 disjoint rational `p×s` residual cells;
- 6,596 incident Round275 region rows;
- 9,528 Round275-region/residual-cell incidences;
- 1,128 canonical
  `(endpoint, adjacent chart, owner target, root sign, p×s cell)` channels.

The 48 whole guard gaps contain no competing event: the full dynamic
evaluator returns only `outgoing_chart_seam` on every gap.

## Strict regularity on the whole seam-to-collar gap

For all 48 guard channels, both on the algebraic seam and on the entire
normal gap to the rational Round275 collar:

- `∂F/∂t` is strict and keeps its sign;
- `∂F/∂p` is strict and keeps its sign.

Here `F = outgoing_normal_x² - outgoing_normal_y²`.

For the 32 G-target channels, `F` is structurally independent of `s` because
the target center is independent of `s`.  For the 16 W-target channels,
`∂F/∂s` is strict: eight positive and eight negative.

Consequently every nonempty zero set is a fold-free regular `p` graph over
the whole normal gap.  Strict `t` monotonicity, together with exact
`s`-independence for G or strict `s` monotonicity for W, makes its clipped
positive and negative sides connected.  A half-open owner convention can
assign the graph once without duplicating it on the shadow side.

## Exact arrangement census

The 48 channels divide as follows:

- 24 G-target channels: opposite strict `p`-face signs, hence one full
  `s`-base regular `p` graph;
- 16 W-target channels: one `p` face overwraps and the other is strict;
- eight G-target channels: equal strict `p`-face signs, hence no zero.

Every W endpoint case is exact, not a precision tail.  Its overwrapping face
is `p=0`; the two strict `s`-face signs are opposite, and the unique boundary
zero is exactly `(p,s)=(0,0)`.  At this point the source normal and the W
target center are exactly diagonal and collinear, so the outgoing normal is
diagonal and `F=0`.  Splitting at the already-frozen rational coordinate
`s=0` gives one regular-graph child and one strict-absence child.

Thus the required analytic partition has:

- no new `p` split;
- 16 logical `s=0` splits;
- 64 children in total;
- 40 regular-graph children;
- 24 strict-absence children;
- 104 connected open sign corridors;
- 40 uniquely owned zero graphs;
- zero remaining analytic tail endpoints and patches.

This is stronger than repeatedly shrinking rational boxes: the zero graph is
retained and certified as a regular analytic stratum.

## Strict non-promotion and remaining risk

This probe grants no occurrence, component-edge, maximality, fibre,
disposition, D02, Gate5, CM2, or Jx/Jy credit.  The frozen baseline remains
quotient 63,224; expanded occurrences 126,468; maximality 0/63,224; fibres
0/116; global dispositions 0/224,580; Gate5 10/18; D02 blocked; CM2
`NO-GO_FOR_CLAIM`.

The formal producer/verifier must still:

1. materialize the 64 half-open analytic children;
2. bind each sign child to the correct frozen Round275 region signatures;
3. preserve the eight two-guard endpoint channels without collapsing them by
   target or signature;
4. disposition all 6,596 region hits / 9,528 cell incidences under the
   occurrence-identity contract;
5. pair both directed sides of all 152 true-seam patches before emitting any
   DSU edge.

The 64 children overlap across return branches and must not be counted as 64
new occurrences.  The `p=s=0` owner rule must be pinned to the existing
Round182/Round268 half-open convention.  Jx/Jy remains forbidden.

## Artifacts and replay

- producer/probe:
  `cm2_round283_source_g_outgoing_seam_tail_independent_probe.py`
- complete 40-endpoint ledger:
  `cm2_round283_source_g_outgoing_seam_tail_independent_probe_ledger.json.gz`
- result:
  `cm2_round283_source_g_outgoing_seam_tail_independent_probe_result.json`

The gzip ledger passes decompression.  Two cold executions are byte-identical
for both result and ledger.

