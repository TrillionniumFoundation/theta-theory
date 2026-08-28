# CM2 Eighty-Third Direct Assault — 2026-07-22

## Scope

Round 83 attacks the 37,876 different-third-candidate overlap boxes left by
Round 82.  It replaces the ill-conditioned pair of collision discriminants by
the post-second-collision outgoing line and the finite set of oriented common
tangents of the two candidate obstacles.  The round separately closes
positive-area boxes, degenerate carrier interfaces, and a centered
second-order hard frontier.  It then tests whether the resulting data qualify
as a complete rank-three face quotient, numeric/RN rows, a physical tail
contraction, or an all-depth Gate-4 crosswalk.

## Common-Tangent Coordinate Change

If two third-candidate discriminants vanish at the same phase point, the
post-second-collision outgoing line must equal one of eight oriented
common-tangent targets obtained from the four signed-radius pairs and two
normal branches.  The new system uses either `(normal_x, line_offset_h)` or
`(normal_y, line_offset_h)`, choosing the better midpoint Jacobian chart.  This
removes the near-dependent discriminant gradients that defeated blind
two-dimensional subdivision in Round 82.

The 384-bit Arb primary pass processes all 1,836 residual component pairs and
37,876 residual boxes with 672,696 interval line tests at maximum depth 12:

- 21,154 positive-area boxes are strictly disjoint;
- 16,108 boxes lie on degenerate carrier interfaces;
- 614 positive-area boxes remain hard;
- no common-tangent intersection root is certified.

The zero certified-root count is not used as a disjointness claim for the 614
hard boxes.

## Degenerate Interface Closure

Every degenerate interface box is reduced to a one-dimensional outgoing-line
common-tangent exclusion problem.  Across 1,180 component pairs, 61,316 Arb
line tests certify all 16,108/16,108 boxes disjoint.  There are no unresolved
degenerate pairs or leaves.

Together with the Round-82 prefilter, the complete exact box partition is

`165608 = 127732 + 21154 + 16108 + 614`.

Here the terms are respectively the full unique overlap registry, the
Round-82 strict exclusions, the Round-83 positive-area exclusions, the closed
degenerate interfaces, and the remaining hard positive-area boxes.

## Centered Hard Frontier

The 614 hard boxes occur in 42 component pairs.  A second-order centered
Taylor line map, centered gradients, interval Newton exclusion, and
slope-matrix Krawczyk refinement perform 104,774 additional tests.  No root is
certified.  The remaining 11,840 leaves have exact area

`19743/335544320000`,

compared with initial hard area `281/20480000`.  The exact ratio is

`19743/4603904 < 1/200`.

This is only contraction of the certification frontier under spatial
refinement.  It is not a physical rank-survival or Radon–Nikodym tail
contraction and is not used to promote Gate 5.

## Face, RN, and Gate Qualification

The different-candidate intersection atlas remains incomplete on the 42 hard
pairs.  Therefore the 1,672 joined rank-three root components from Round 82
are not renamed complete physical faces.  The strict eligibility ledger is:

- complete rank-three physical face rows: `0`;
- rank-three F8/F9/F10/F13/F16 rows: `0`;
- rank-three return-face RN rows: `0`;
- uniform physical rank-transition contraction: not certified;
- all-rank RN summability: not certified.

Round 81's fixed-`s=0`, depth-two cellular commuting square remains valid.
Round 83 does not construct the missing same-key all-depth stable/material
crosswalk, so Gate 4 is not promoted.

## Cold Audit

The common-tangent primary resolver, degenerate-interface resolver, and
centered hard-frontier resolver were rerun from cold state under
`python-flint==0.9.0`; all three outputs are byte-identical.  The integrated
certificate and independent hostile verifier were then regenerated.  The
verifier rejects 12/12 hostile semantic mutations and 4/4 strict-JSON attacks
and verifies every input pin.  All Round-83 Python sources compile, and the
accompanying SHA-256 list pins the sources, outputs, audit, and this report.

## Strict State

- Gate 4: `1/7`.
- Gate 5: `10/18`, complete blocks `0`.
- Complete composite gates: `0/5`.
- CM2: `NO-GO_FOR_CLAIM`.

## Next Shortest Route

Do not add more blind dyadic depth.  Reduce the 42 hard component pairs by the
already certified lattice/dihedral action, then construct an exact
common-tangent line-space resultant or a directional support-hyperplane
separation certificate on each orbit representative.  This should decide the
remaining 614 boxes without reproducing the discriminant dependency.  Only
after the full intersection quotient closes should the physical rank-three
face and numeric/RN rows be generated and a genuine rank-transition tail be
tested.  Gate 4 still requires the independent same-key all-depth
stable/material crosswalk.
