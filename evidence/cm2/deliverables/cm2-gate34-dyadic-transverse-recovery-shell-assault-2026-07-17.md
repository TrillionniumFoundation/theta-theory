# CM2 Gates 3/4: dyadic transverse recovery shell

Date: 2026-07-17 (Asia/Shanghai)  
Frozen input: the 64 positive-width boundary-carrier patches  
Strict verdict: **all 64 occurrences admit one explicit two-sided physical
phase-angle shell.  The hit side first hits the tangent target and then the
fixed miss target; the miss side hits that miss target directly.  Both sides
land regularly in the same suffix collision chart.  This is one phase-space
shell, not the parameter-DQ transverse family, an all-scale limit, or a
24-core recovery theorem; Gates 3 and 4 remain open.**

## 1. One common dyadic angular shell

For each event row rotate the tangent outgoing velocity by an angle with
magnitude

```text
1/65536 <= |alpha| <= 1/32768.
```

The sign convention is exact:

```text
hit side:  sign(alpha)=epsilon,
miss side: sign(alpha)=-epsilon.
```

Adaptive Arb replay uses only three event-base half-widths:

```text
half-width 1/1024: 36 rows,
half-width 1/2048: 24 rows,
half-width 1/4096:  4 rows.
```

The 64 labelled base patches have total `(z,s)` coordinate area
`169/1048576`; including both angular slabs gives coordinate volume
`169/34359738368`.  These coordinates are not claimed to be invariant mass.

## 2. Complete local first-hit replay

Each flight is tested against both obstacle species on a `9x9` lattice
window centered at the current collision lift.  The current obstacle is
removed, leaving 161 candidates.  Every certified owner flight is strictly
below `2`, while the radius-4 lattice window exceeds the possible center
offset, so the comparison is locally complete.

For every row the resulting target sequences are

```text
hit tube:  source -> tangent target -> fixed miss target,
miss tube: source ------------------> fixed miss target.
```

The two successor states are generally different, but they are both regular
and lie in the same dominant-coordinate suffix chart.  Uniformly,

```text
successor cos(phi) > 1/20,
successor |p|      < 999/1000,
each owner flight  < 2.
```

The suffix chart histogram remains

```text
G:E/G:N/G:S/G:W = 10/12/12/10,
W:E/W:N/W:S/W:W =  4/ 6/ 6/ 4.
```

## 3. Exact progress against the recovery ledger

The recovery registry now has four physical layers:

```text
64 event-base carrier IDs,
128 oriented boundary trace seeds,
64 positive-width boundary patches,
128 explicit transverse phase-space tubes with common regular suffix charts.
```

This closes the former absence of a physical carrier and gives a concrete
first regular chart for both sides.  It does not yet give first entrance into
the 24 contracting cores.

## 4. Strict nonpromotion

The angular transverse coordinate is a phase-space probe.  It has not been
identified with the actual moving-parameter coordinate used by `DQ`, and one
dyadic slab does not provide an all-scale shell family or a differentiability
limit.  No bounded grazing pushforward, strong-space restriction, 24-core
destination, or `2018/12108` no-recut itinerary is certified.

```text
DYADIC TRANSVERSE RECOVERY SHELLS:         64 CERTIFIED
ORIENTED PHASE-SPACE TUBES:                128 CERTIFIED
COMMON REGULAR SUFFIX CHARTS:              64 CERTIFIED
PARAMETER-DQ TRANSVERSE IDENTIFICATION:    NOT CERTIFIED
ALL-SCALE SHELL FAMILY:                    NOT CERTIFIED
FIRST 24-CORE DESTINATION:                 NOT CERTIFIED
NATIVE NO-RECUT DWELL:                     NOT CERTIFIED
GATE 3:                                    NOT CERTIFIED
GATE 4:                                    NOT CERTIFIED
```
