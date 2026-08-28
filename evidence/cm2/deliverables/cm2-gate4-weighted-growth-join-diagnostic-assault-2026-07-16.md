# CM2 Gate 4 contraction-weighted Growth join diagnostic

Date: 2026-07-16 (Asia/Shanghai)

## Verdict

The frozen Gate-4 stacks do not contain a componentwise
`multiplicity x inverse-expansion` join.  The number `35,024` belongs to an
ambient ray/horizon witness cover, while `448` belongs to a conservative
source-chart/target candidate registry.  Neither ledger has a short unstable
curve identifier, a physical continuity-component identifier, a homogeneity
child identifier, or a per-child inverse-expansion weight.  The `152/153`
result is an unweighted complexity envelope.

Exact rational completions of the aggregate constraints give both a
contracting and a noncontracting sum, even with the same 153 positive
component slots.  Hence the current aggregate fields are rigorously
non-identifying.  No honest value can yet be assigned to the global one-step
Growth coefficient, `delta_1`, `C_p`, `vartheta_p`, or propagated
`C_fw,C_rev,q`.

```text
AGGREGATE GROWTH-DATA NONIDENTIFIABILITY:       CERTIFIED
COMPONENTWISE MULTIPLICITY x INVERSE JOIN:      NOT CERTIFIED
NUMERIC GLOBAL GROWTH CONTRACTION:              NOT CERTIFIED
GATE 4:                                         NOT CERTIFIED
```

This is a strict diagnostic result, not a physical counterexample to the
billiard Growth Lemma.

## 1. Frozen inputs and their actual types

Four frozen manifests are replayed read-only.

| Frozen number | Actual schema role | Missing for Growth |
|---|---|---|
| `35,024` | Boxes in an ambient `(x,y,direction)` cover proving `tau<3` and a penetration slack | no collision-chart curve ID, true child ID, homogeneity rank, or inverse-expansion field |
| `448` | Conservative chart-target pairs surviving horizon and outgoing-halfspace necessary tests | no materialized physical first-hit continuity partition or per-child weight |
| `152` | Upper bound on intersections of one unstable graph with the signed raw tangency-sheet universe | no physical incidence list or contraction weight |
| `153` | Resulting unweighted continuity-component count upper | no component identifiers or join relation |
| `900337/901685` | Homogeneity-cut sum on one true continuity branch | cannot be charged once to an unspecified collection of up to 153 physical branches |

The horizon manifest stores a digest of its witness rows, not physical
continuity rows.  The first-hit snapshot stores per-chart candidate digests,
and explicitly leaves `all_retained_event_rows` and
`all_first_hit_partitions` null.  A digest authenticates a ledger; it is not
a typed relation joining two ledgers.

In particular, none of the replayed schemas contains any of

```text
short_unstable_curve_cell_id
uniform_small_curve_threshold_delta_1
physical_continuity_component_id
parent_short_curve_cell_id
homogeneity_child_id
physical_component_multiplicity
inverse_expansion_sup_upper
componentwise_weighted_sum_upper
componentwise_weighted_sum_margin
```

The existing derivative envelope

```text
||D2 T||_infinity < 42672/c_1^3
```

and the oriented-carrier distortion number `6000000000000` do not create
these missing incidence and inverse-expansion fields.

## 2. Exact aggregate arithmetic

The certified central inverse-contraction envelope and the declared two-sided
high-strip tail are

```text
theta = 144000/180337,
tail  = 1/5.
```

On one true branch this gives

```text
q_branch
 = theta + tail
 = 900337/901685
 = 1 - 1348/901685
 < 1.                                                    (2.1)
```

The unweighted component count alone gives only

```text
Xi_1 <= 153 q_branch
     = 137751561/901685
     > 1.                                                (2.2)
```

Equation (2.2) is a valid upper diagnostic, but not a contraction.

## 3. Why the aggregate data cannot decide the missing sum

Consider only the information actually joined by the frozen aggregate
schemas:

```text
1 <= N <= 153,
0 < w_j < q_branch.
```

Use exactly `N=153` slots in both of the following abstract completions.

The contracting completion assigns every slot

```text
w_j = q_branch/(2*153),
sum_j w_j = q_branch/2 < 1.                             (3.1)
```

The noncontracting completion assigns every slot

```text
w_j = 3/4 < theta < q_branch,
sum_j w_j = 153*(3/4) = 459/4 > 1.                     (3.2)
```

Both satisfy every aggregate count and per-slot inequality used here.  They
are deliberately **not** asserted to be realizable billiard configurations.
They prove the narrower and exact statement needed for this audit: the
present aggregate fields do not identify the missing weighted sum.  A
physical row-level join or a compressed theorem carrying equivalent
information is indispensable.

The resulting schema-only interval has infimum zero and non-strict upper
envelope `137751561/901685`; it straddles one.

## 4. The smallest actionable contraction budget

At the frozen cutoff `k0=41`, the certified `1/5` tail envelope is only for
the descendants of **one true continuity branch**.  A global tail budget is
not currently certified.  If a future incidence theorem proves that all
high-strip children of one short parent curve can be charged together to one
global tail of at most `1/5`, then the central children must have a joined
weight sum strictly below

```text
1 - 1/5 = 4/5.                                         (4.1)
```

Under that explicit additional hypothesis, one use of the uniform central
envelope succeeds:

```text
4/5 - 144000/180337 = 1348/901685 > 0.                 (4.2)
```

Repeating that envelope twice already makes the proof method fail:

```text
2*(144000/180337) = 288000/180337 > 1.                 (4.3)
```

Equation (4.3) does not prove that the physical sum is above one.  It proves
that an unlinked repetition of the existing uniform central bound cannot
certify contraction once two central children are allowed.

Thus `4/5` and the displayed positive margin are a conditional sufficient
budget, not a newly certified global Growth coefficient.  There are two
honest ways forward.

1. Produce one explicit `delta_1` and a replayable sheet-separation/incidence
   theorem showing that every unstable curve of length at most `delta_1` has
   at most one central child, while every other child is charged to one
   **global**, rather than per-candidate, grazing tail of at most `1/5`.
2. Materialize every physical child and certify directly that its joined
   central-plus-homogeneity weights sum to less than one.

## 5. Executable missing join contract

A direct ledger must contain, for each short-curve cover cell,

```text
short_unstable_curve_cell_id
uniform_small_curve_threshold_delta_1
configuration_parameter_interval
source_collision_chart
complete_physical_child_count
```

and, for each physical child,

```text
parent_short_curve_cell_id
physical_continuity_component_id
target_obstacle_lift
homogeneity_child_id_or_central_tag
physical_component_multiplicity
inverse_expansion_sup_upper
```

The verifier must additionally prove that every true singularity and
homogeneity cut occurs exactly once, that no conservative candidate is
charged merely because it survived pruning, that all weights use the same
adapted metric and finite-`s` map, and that the exact total has a positive
margin below one.

An equivalent compressed replacement is acceptable: an explicit
sheet-separation/incidence theorem at numerical `delta_1` that proves the
one-central-child/global-tail statement in Section 4.

## 6. Scope

This diagnostic does not weaken any previously certified geometry,
hyperbolicity, `D2T`, or carrier-distortion leaf.  It only prevents a typing
error: multiplying an unweighted candidate/component count by a local
one-branch contraction is not the physical Growth sum.

Consequently:

```text
numeric delta_1:                           NOT CERTIFIED
componentwise weighted one-step sum:       NOT CERTIFIED
numeric global Growth contraction:         NOT CERTIFIED
numeric C_p,vartheta_p:                     NOT CERTIFIED
complete numeric C_fw,C_rev,q:              NOT CERTIFIED
Gate 4:                                     NOT CERTIFIED
```

## 7. Replay

Files:

```text
deliverables/cm2_gate4_weighted_growth_join_diagnostic_cert.py
deliverables/cm2_gate4_weighted_growth_join_diagnostic_verifier.py
deliverables/cm2-gate4-weighted-growth-join-diagnostic-manifest-2026-07-16.json
deliverables/cm2-gate4-weighted-growth-join-diagnostic-manifest-2026-07-16.sha256
```

Commands:

```bash
PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_weighted_growth_join_diagnostic_verifier.py --replay

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_weighted_growth_join_diagnostic_verifier.py --self-test

PYTHONPATH=deliverables python \
  deliverables/cm2_gate4_weighted_growth_join_diagnostic_verifier.py
```

The default live invocation must exit `2` because Gate 4 remains fail-closed.
