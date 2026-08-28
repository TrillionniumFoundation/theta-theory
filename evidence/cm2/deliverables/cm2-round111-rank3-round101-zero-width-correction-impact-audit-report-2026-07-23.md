# CM2 Round 111 — Round101 zero-width correction and downstream impact audit

Round111 does not install the planned source-grazing collars.  It first
corrects a fail-closed defect in the frozen Round101 endpoint chain and
quantifies exactly what remains usable downstream.

## Frozen defect

For each of the eight corrected exterior rays, Round94 stores two different
objects:

- `first_physical_terminal_event_parameter_bracket = [seam_outer, grazing_inner]`;
- `transferred_grazing_parameter_bracket = [grazing_inner, grazing_outer]`.

Round101 selected index `0` of the first bracket as the adjacent-chart
terminal.  That value is `seam_outer`, which is also the start of its
adjacent-chart partition.  Consequently all `8 x 65 = 520` advertised
adjacent rows have `qa = qb`: they are repeated seam points, not positive-
width intervals.

This is confirmed dynamically rather than only by reading the source.  The
Round111 producer independently reconstructs all eight frozen Round101 full
segment digests, including the 1,032 frozen old-source-chart rows and the 520
collapsed adjacent rows.  Digest reconstruction does not preserve the old
same-table completeness claim: on the last old-source-chart segment of every
ray, the centered source normal is chart-indeterminate.  A corrected source
layer separately certifies 1,024 strict same-chart rows plus eight rows
against the union of all four first-hit candidate tables.  The 640-bit
verifier reconstructs both layers without importing the Round111 producer or
the Round96 producer implementation.

Therefore the Round101 fields
`adjacent_chart_segment_count = 520` and
`remaining_open_exterior_ray_count = 0` cannot retain their advertised
whole-interval meaning.

## Positive-width reconstruction actually certified

Using the correct adjacent interval `[seam_outer, grazing_inner]`, Round111
builds the intended 65 positive-width base intervals on every ray: 520 true
base intervals exist.  The strict certified subset is:

- nonterminal positive-width base cells: **512/520**;
- ordinary same-chart correlated replays: **496**;
- replays whose enclosure begins at `seam_outer` and is source-normal
  chart-indeterminate, checked against the union of all four first-hit
  candidate tables: **8**;
- replays crossing an internal outgoing-normal representation seam, checked
  against the union of all four immutable candidate tables: **8**;
- complete first/second/third competitor clearance on every one of those 512
  cells;
- endpoint dyadic rings certified per ray: **32**;
- certified endpoint rings in total: **256**.

The centered enclosure for corrected adjacent segment zero contains
`seam_outer` and has a chart-indeterminate source normal, so its first-hit
clearance uses the four-chart union.  This does not locate the actual source
chart seam at that endpoint: Round93 only traps the transfer seam inside
`[old_chart_inner,seam_outer]`, and that whole interval remains unbridged.
The separate outgoing-normal union occurs later (segment 16 or 17).  Neither
operation is the missing source-chart transfer bridge.

Three separate residual objects remain on each ray and are not conflated:

1. the Round93 bracket `[old_chart_inner, seam_outer]`, whose whole interval
   is not bridged;
2. the pre-root-bracket interval tail left after 32 dyadic rings, ending at
   `grazing_inner` and having relative width `2^-32` inside the terminal base
   cell; these rings approach only the bracket's lower endpoint and do not
   prove that source cosine tends to zero;
3. the tight algebraic source-grazing root bracket
   `[grazing_inner, grazing_outer]`.

Thus end-to-end source-grazing ray closure is **0/8**, not 8/8.  The 256-ring
prefix is finite evidence and is not promoted to a proof of the infinite
dyadic exhaustion.

## Downstream impact

- **Round102:** face IDs, registered ports, internal links, and the
  source-grazing event-type/candidate incidence remain useful.  The eight
  broad terminal brackets, bracket-derived endpoint IDs, endpoint
  completeness, eight cap-to-grazing whole-face domains, and zero-residual
  conclusion are withdrawn.
- **Rounds103–105:** face/ID mechanisms and face-local chart/direction
  metadata remain useful.  Tangent faces are not homogeneous operator
  children, and a three-owner tuple is not an official word.  No actual-child
  F1–F4 slot is preserved; those fields must be rebuilt on genuine children.
- **Round106:** its conservative obstruction and zero F5/F6 promotion remain
  valid.
- **Rounds107–108:** the 24 rational local witness boxes, their immutable
  candidate replays, and their fixed-box official word paths remain valid in
  their stated local scope.  They do not extend through the eight open
  endpoint chains.
- **Round109:** all 52 internal registered-arc whole-tube reaudits and 41,984
  immutable-table strips remain valid.  They do not certify exterior collars.
- **Round110:** all 56 internal gap pairs and 112 strict-`D` side ownership
  rows remain valid as an internal combinatorial ledger.  They cannot be
  embedded into an endpoint-complete twelve-face physical quotient yet.

Actual homogeneous-child maturity is therefore **0/18**.  Face-local records
are metadata, not completed operator blocks.

## Independent verification

- producer precision: **512 bits**;
- independent verifier precision: **640 bits**;
- Round111 producer imported by verifier: **false**;
- frozen Round101 full digests independently rebuilt: **8/8**;
- frozen source rows rebuilt: **1,032/1,032**, with the old same-table
  completeness claim explicitly withdrawn on eight terminal enclosures;
- corrected source rows replayed: **1,032/1,032** = **1,024** same-chart +
  **8** source-normal four-chart-union;
- zero-width adjacent rows confirmed: **520/520**;
- corrected nonterminal base cells replayed: **512/512**;
- endpoint dyadic rings replayed: **256/256**;
- endpoint-ring source normals proven strict in the adjacent chart:
  **256/256**;
- hostile semantic mutations rejected: **12/12**;
- duplicate-key, nonfinite, and unknown-top-level JSON attacks rejected:
  **3/3**.

## Strict conclusion

Positive-width root-centred `(eta,c3)` collars certified: **0**.  Whole-collar
57-candidate orderings certified: **0**.  New F5/F6 slots: **0/0**.  Complete
18-field blocks: **0**.  Global Gate5 remains `10/18`, blocks zero, and CM2
remains `NO-GO_FOR_CLAIM`.

The next lawful step is to bridge the eight source-chart seam brackets and
construct a root-regularized `(eta,c3)` endpoint atlas that handles the tight
algebraic root and the countable `H_{sigma,k}` family without replacing an
infinite exhaustion by a finite prefix.
