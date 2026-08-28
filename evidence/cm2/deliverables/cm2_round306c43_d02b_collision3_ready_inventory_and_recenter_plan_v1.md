# CM2 C43 D02-B collision-3-ready inventory and recenter plan

Status: read-only design evidence, zero formal credit. No runtime candidate,
pointer, seal, or canonical status was written by this work.

## Exact C41 queue

The pinned C41 `routed_ambient_cells` ledger
(`ea75405c8f8ba53c795c64a228aea75f9587017d93aa1cd08e73c287931e78a8`)
contains exactly 7,463 unique `COLLISION3_READY` representative rows from
2,158 C40 leaves and 136 representative/reflection pairs. They explicitly
materialize 14,926 physical side branches.

- original collision-2 match / owner `G[0,1]`: 3,364;
- reflected collision-2 match / owner `G[0,0]`: 4,099;
- depth 0 carry: 660 rows at volume `1/64`;
- depth 3: 6,803 rows at volume `1/512`;
- route boxes are all `W:E -> W:E`; exact horizontal reflection checks have
  zero mismatches;
- every `obligation_ids` list is empty and every D02, collision-3, terminal,
  and lower-dimensional credit field is zero.

The queue covers pair indices 9 through 859 (not every intervening index).
The largest pair queue is pair 613 with 145 rows; the smallest queues have one.
Each representative row has a distinct row hash, ambient id, `(pair,path)`,
representative box, and reflected box.

## Collision 3 through 1,648 obligations

Every still-live branch must be processed until a strict terminal certificate
or through collision 1,648. The upper bound before early termination is:

- `7,463 * 1,646 = 12,284,098` representative step bindings;
- `14,926 * 1,646 = 24,568,196` physical-side step bindings.

Each binding must independently carry side/parent identity, collision index,
incoming owner, all candidate discriminants, isolated roots and strict order,
selected owner, official word, outgoing chart, wall events and endpoint
margins, homogeneity, incidence ownership, core/cemetery disposition, and a
terminal margin. Allowed terminal results are strict exclusion, attachment to
a known component, or a strict cemetery/disconnected certificate.

C35-C37 provide all 1,648 occurrence templates: 137 geometry templates and
197 official-word variants, including reflected margin transport. For indices
3-1,648 the original row-hash sequence is
`4bf396ed29aef1cc93202905bc8898a34c9cc386de9e006eaa4e9d1fb557b295`;
the reflected sequence is
`0d03211e3a3cdd1926126690b606606e51d38536721cca2fa86a5c534b94b3ad`.
These templates permit computation reuse only. They cannot replace an exact
per-row, per-side, per-collision binding or issue formal credit.

## Why naïve `strict_next_owner` fails on pair 9

For the deterministic pair-9 ready leaf beginning at path `011110111`, the
whole-box legacy pipeline resolves collision 2 to `G[0,1]`, but its collision-2
normal enclosure straddles the outgoing chart seam. Consequently
`second_outgoing_state` cannot select one strict chart, so collision-3
`strict_next_owner` cannot safely run on the whole enclosure.

Plain longest-axis bisection does not cure the underlying dependency. Once a
chart becomes selectable, most children still return
`unresolved_competitor:unresolved_discriminant`; exact-center evaluations do
select `W[0,0]` or `W[0,-1]`, but those point values are hints, not box proofs.
Thus the failure is interval dependency plus a real chart-stratum obligation,
not evidence that no next owner exists.

## Centered/adaptive collision-3 pilot contract

1. Recenter each collision map at the exact rational box center and propagate
   `center + J*delta + certified remainder` for contact, root, normal, chart,
   word, and core margins.
2. Use the point owner only to prioritize candidate evaluation. Prove it by a
   positive discriminant, isolated near root, strict gap to every competitor,
   and strict `tau_max` margin on the full closed box.
3. If a chart margin crosses zero, split or materialize the exact chart seam;
   its faces/corners receive explicit owners and remain zero ambient credit.
4. Choose the next split axis from the sensitivity contribution to the failing
   margin, rather than blindly using the longest geometric axis.
5. Bind the selected C35/C36/C37 template and reflected transport to every
   occurrence. Recompute whenever the transported margin is not strict.
6. Preserve a prefix-free queue and exact Kraft sum for every one of the 862
   parents. Credit is issued only when an entire representative plus reflection
   and all lower strata are terminal.

Executable read-only planner:
`cm2_round306c43_collision3_ready_inventory_planner_v1.py`.

The current global verdict is unchanged: D02 remains blocked and CM2 remains
`NO-GO_FOR_CLAIM`.
