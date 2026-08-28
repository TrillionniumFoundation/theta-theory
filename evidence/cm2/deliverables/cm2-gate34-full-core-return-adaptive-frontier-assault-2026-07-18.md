# CM2 Gate 3/4 — Full-core adaptive first-return frontier

Date: 2026-07-18  
Status: append-only strict leaf; no prior artifact modified

## Frozen conclusion

This leaf is the first materialized finite-dimensional return calculation on
the **entire 24-core source carrier**, rather than on the earlier one-dimensional
charged curves.  For every `|s|<=1/400`, each source atom retains a positive
two-dimensional `(t,p)` collision rectangle.  The already certified complete
first-owner comparison on each parent core is replayed, and every child image
is admitted with 384-bit Arb only by the fail-closed trichotomy

```text
RETURN_AT_1_INNER
SURVIVE_THROUGH_1_INNER
UNRESOLVED_OUTER
```

The raw cover has 33,960 leaves:

| strict class | leaf count | parameter-averaged base mass |
|---|---:|---:|
| `RETURN_AT_1_INNER` | 4,216 | `6473/256000000` |
| `SURVIVE_THROUGH_1_INNER` | 2,868 | `123841/80000000` |
| `UNRESOLVED_OUTER` | 26,876 | `44519/256000000` |

The three rational base masses add exactly to the full C24 source base mass
`273/156250`.  Leaf interiors are disjoint and their union covers
`C24 × [-1/400,1/400]` modulo shared source-box faces.  The unresolved rows
are an outer cover caused by chart/core boundaries and interval dependency;
they are not declared singular or assigned to either `R1` or `Q1`.

## Adaptive policy and raw audit

All unresolved boxes are binary refined to depth 12.  A strict midpoint
return test then acts only as a **proposal** for further refinement; 3,472
such parents are refined to depth 15.  Final admission always replays the
whole child Arb box.  No midpoint value is accepted as proof.

For each leaf, the manifest materializes:

- exact source core ID and dyadic path;
- rational `(t,p,s)` bounds;
- complete-parent first-owner witness binding;
- strict return/survival/unresolved class and destination core when present;
- output normal and target-`p` Arb enclosures;
- deterministic per-core separation-witness digest;
- parameter-averaged rational mass bracket;
- exact invariant `(r,p=sin(phi))` inverse area Jacobian `1` and log-area
  distortion `0`.

The 4,216 strict return leaves arise from 16 source cores and hit 16
destination cores.  All 24 parent collision branches are regular at step 1;
there is no step-1 collision-singular cemetery atom on this frozen carrier.

## Collision-mass bounds

On `|t|<=7/10`,

```text
dtheta/dt < 1401/1000,
(1401/1000)^2 (1-(7/10)^2) > 1.
```

Together with `pi<22/7`, the parameter-averaged strict return-inner normalized
collision-SRB mass is

```text
> 45311/11714560000 > 1/300000.
```

Relative to the C24 base mass,

```text
return-inner / C24     = 32365/2236416 > 1/70,
survivor-inner / C24   = 123841/139776,
unresolved-outer / C24 = 222595/2236416 < 1/10.
```

The parameter average is normalized uniform `ds` on the full parameter
window; it is not silently promoted to a pointwise statement.

## Uniform-in-parameter immediate return

The leaf additionally materializes 32 finest open parameter-slab rows.  On
every slab the three fixed-`s` base masses add exactly to `273/156250`, and
each slab has a positive strict return-inner carrier.  The worst slab gives

```text
fixed-s return-inner base mass >= 711/32000000,
fixed-s return-inner / C24 base > 1/80,
fixed-s normalized return-inner mass
  > 4977/1464320000 > 1/400000.
```

At a dyadic parameter boundary, either adjacent closed-leaf partition may be
chosen: every strict box certificate includes its parameter endpoint.  Thus
the same positive immediate-return lower bound holds for all
`|s|<=1/400`, including the endpoints.

For the full core mass, the eight axis cores use
`dtheta/dt<1001/1000`, the sixteen diagonal cores use
`dtheta/dt<1401/1000`, and `pi>3`.  This gives

```text
mu_s(C24) < 29021/75000000 < 1/2500.
```

Consequently the normalized C24 conditional mass of the materialized
first-return-at-one inner atoms satisfies, uniformly in `s`,

```text
P_{mu_{C24,s}}(tau_C^+=1)
  > 9331875/1062400768
  > 1/160.
```

This is an **unconditional time-zero immediate-return atom weight**.  It is
not a survivor-conditioned hazard lower bound at later times and therefore
does not imply an exponential tail.

## Strict nonpromotion

The following remain `NOT_CERTIFIED`:

- removal of the nonempty step-1 unresolved outer cover;
- a complete physical `R_n/Q_n` first-return partition for arbitrary `n`;
- an unweighted or `q`-weighted exponential excursion/cemetery tail;
- source/test strong distortion loads on all return branches;
- common forward/reverse restriction IDs and the induced strong
  Lasota–Yorke coefficient;
- Gates 3, 4, and 5.

In particular, the one-step bound `>1/160` cannot be iterated without a
uniform survivor recovery/admissibility theorem.

## Frozen artifacts and replay

- `cm2_gate34_full_core_return_adaptive_frontier_cert.py`
- `cm2_gate34_full_core_return_adaptive_frontier_verifier.py`
- `cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.json`
- `cm2-gate34-full-core-return-adaptive-frontier-manifest-2026-07-18.sha256`

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_full_core_return_adaptive_frontier_verifier.py \
  --integrity-only

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_full_core_return_adaptive_frontier_verifier.py \
  --replay

PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_full_core_return_adaptive_frontier_verifier.py \
  --self-test
```

Default live mode exits `2` and preserves the fail-closed status.
