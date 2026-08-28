# CM2 Gate 2: actual stable-plaque continuation and second local branch

Date: 2026-07-15  
Precision: 2400-bit Arb, `python-flint==0.9.0`  
Verdict: **the actual `W^s(z_*)` is validated to the common-chart face
`v=0`, and a positive-width physical 96-word strip around that crossing
full-crosses the common rectangle; stable saturation, a two-branch quotient,
and physical Gate 2 remain OPEN / NO-GO.**

## Certified continuation

The reversible half-word root was refined from radius `10^-200` to a
validated interval-Newton box of radius `10^-600`.  This removes the earlier
wrapping uncertainty at the remote stable face.

The local unstable plaque supplied by the predecessor has slope at most
`10^-40`.  Starting at

```text
u_0 = 7.2136102973143465356...*10^-121,
|delta u_0| <= 10^-250,
|v_0| <= 7.214*10^-161,
```

two collisionwise 96-word Taylor replays, with a rigorous rebox after the
first return, give opposite global-`u` face signs

```text
-1.14973804412714...*10^-144,
+1.14973804412714...*10^-144.
```

Hence `F^2(W^u_loc(z_*))` meets global `u=0`.  Reversibility swaps the loop
Perron coordinates and proves that the actual stable plaque meets `v=0` at

```text
u_cross = a_* + 1.00724611956196203516...*10^-42,
crossing uncertainty < 8.53*10^-172.
```

Unlike the affine mixed corner, this actual crossing follows all 96
declared first hits.  Its uniform point margins include

```text
flight > 0.18710678118,
discriminant > 0.01026432354,
incidence > 0.63320623699,
clearance > 0.22283858113.
```

## Positive-width second local branch

Around the actual crossing take the loop-Perron source strip with half-widths

```text
(r_u,r_v)=(8*10^-68,10^-80).
```

The entire strip follows the 96-word first-hit itinerary.  Its image in the
common rectangle has

```text
negative u-face < -1.68718*10^-14,
positive u-face >  2.84304*10^-16,
stable image      = -8.2937621943*10^-15 +/- 4.74*10^-38.
```

These strictly cross the common interval
`[a_*/2-4.2*10^-15,a_*/2+4.2*10^-15]` in the unstable direction and enter it
in the stable direction.  The strip is disjoint from the short-QNL source.

On the full strip the derivative enclosure is

```text
[[1.07225838496*10^53 +/- 5.76*10^29,
  -7.95391600179*10^25 +/- 4.47*10^2],
 [                 +/- 5.08*10^29,
                   +/- 3.77*10^2]].
```

The `10^-20` unstable and inverse-stable cones map to slopes below
`4.74*10^-24` and `7.42*10^-28`, respectively.

Thus there are now **two local physical crossings in one common rectangle**:
the two-collision QNL strip and the actual-plaque 96-collision strip.

## Remaining Gate-2 gap

The new second strip has stable half-height `10^-80`; it is not a certified
full-height stable-saturated Markov strip.  Still missing are:

1. stable saturation and invariant holonomy on both source strips;
2. two well-defined onto inverse branches on one quotient interval;
3. a full-mass countable return partition and density `rho`;
4. physical reverse weights, tail/off-diagonal energy bounds and stopped PPE;
5. same-carrier endpoints and the exhaustive normalized amplitude registry.

Accordingly this is a strict local-geometry advance, not physical Gate 2 or
unconditional CM2.

Reproduce with:

```bash
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate2_actual_stable_plaque_continuation_cert.py
```
