# CM2 Gate 3/4 Round 52 — proof-level outer rate and C24 outer-majorant frontier

Date: 2026-07-20  
Scope: Gate 4 numerical `H_bump`, `H_cover/beta`, and common terminal survivor  
Strict verdict: **Gate 4 NOT CERTIFIED; CM2 NO-GO**

## Result

Round 51's uniform existential bump time can be effectivised further than the
black-box pair `C_bump,theta_bump` suggests.  Reopening the coupling proof in
Stenlund--Young--Zhang (`arXiv:1210.0011v4`) gives, for proper-start families
and a Lipschitz observable,

```text
C_1 = 2 max((1-tilde_zeta/2)^(-1),hat_c^(-1)),
coupling rate = (1-tilde_zeta/2)^(1/(2 Delta)).
```

The frozen pilot already has

```text
hat_c = 20/3807,
Lambda = 180337/144000.
```

Since `0<tilde_zeta<1`, the first entry in the maximum is `<2`, while
`hat_c^(-1)=3807/20>2`.  Therefore the proof-level outer prefactor is now
fully numerical:

```text
C_bump,outer <= 3807/10.
```

The immediately preceding observable estimate in the official source is

```text
2 Lip_1(f) hat_c^(-1) Lambda^(-n/2).
```

The final displayed line prints `Lambda^(-gamma)/2`.  That faster expression
is not the nth-root rate of the preceding bound and is not used here.  The
safe rate is `Lambda^(-1/2)`, for which exact integer arithmetic gives

```text
14400000 < 14607297 = 81*180337,
Lambda^(-1/2) < 9/10.
```

Thus the complete safe proof-level rate has been reduced to

```text
theta_safe
= max((1-tilde_zeta/2)^(1/(2 Delta)), 9/10).
```

Only two scalar rate data are now nonnumerical:

1. a positive lower bound for `tilde_zeta`, the minimum compatible magnet
   coupling fraction;
2. a finite integer upper bound for `Delta`, the maximum coupling-time gap
   including mixing, recovery and compact-configuration scheduling.

Neither is published numerically.  Hence `H_bump` remains nonnumerical.

## Why the proper-start formula applies without hiding a numerical shift

Round 51's input is a normalized canonical family with finite numerical `Z`
and dynamic log-density constant at most `2e27`.  The finite regularity
threshold in the SYZ proof may be enlarged to contain this constant.  The
properness threshold may likewise be enlarged to contain the frozen proper
family bound.  Enlarging these upper thresholds preserves the inequalities;
the resulting deterioration of the magnet construction is absorbed into
the still-hidden `tilde_zeta,Delta`.

On the comparison side, Lemma `1' implies 1` gives the common invariant
collision law a finite-`Z` regular unstable representation.  Its eventual
proper pushforward represents the same law because the collision law is
invariant.  Thus that law admits a proper representation.  The coupling
proof can start with proper representations of both laws; no separate
nonnumerical initial regularisation clock is inserted into `H_bump`.

This argument does not make the selected regularity/properness thresholds
numerical.  It only shows that their effect occurs inside the two remaining
magnet scalars, not as a third independent outer-rate constant.

## Exact conditional integer interface

Let numerical data eventually give

```text
0 < zeta0 <= tilde_zeta,
Delta <= D,  D in positive integers.
```

Define `m` to be the least nonnegative integer satisfying the two exact
rational tests

```text
(2724*3807/10)*(1-zeta0/2)^m < 21/111718750,
(2724*3807/10)*(9/10)^(2*D*m) < 21/111718750.
```

Then

```text
H_bump = 2*D*m
```

is safe.  This avoids floating logarithms and roots entirely.  The exact
scale ratio is

```text
(2724*3807/10)/(21/111718750)
= 38618445937500/7.
```

As a verifier-only arithmetic example, the hypothetical values
`zeta0=1/2,D=1` give `m=140,H=280`; block `m=139` fails.  This example is not
a physical magnet claim.

## Sharp remaining non-effectivity

The two scalar rows are individually necessary for this proof route.

- If `tilde_zeta=1/2` is held fixed but no numerical upper bound for `Delta`
  is known, then for any proposed `H0` the formally admissible choice
  `Delta=H0+1` gives

  ```text
  (3/4)^(H0/(2(H0+1))) > 3/4.
  ```

- If `Delta=1` is held fixed but no positive numerical lower bound for
  `tilde_zeta` is known, choose

  ```text
  tilde_zeta=1/(2(H0+1)^2).
  ```

  Directly for `H0=0,1`, and by Bernoulli for `H0>=2`, the coupling branch at
  `H0` is again `>3/4`.

In either case the available error majorant is still larger than

```text
2724*(3807/10)*(3/4) = 7777701/10
                       >> 21/111718750.
```

These are models of the unpublished proof constants, not counterexamples to
the physical billiard.  They prove that the currently available theorem data
cannot certify any proposed integer.

## A uniform Lipschitz outer majorant for all 24 C24 boxes

A second, independent increment gives a large common terminal survivor.
For each certified C24 coordinate rectangle, take the product of two
piecewise-linear trapezoids which equal one on the closed rectangle and taper
to zero across the following padding:

| core type | `delta_t` | `delta_p` | padded widths |
|---|---:|---:|---:|
| 8 axis boxes | `1/1000` | `1/1000` | `(3/250,3/500)` |
| 16 diagonal boxes | `1/1000` | `1/100` | `(3/250,3/50)` |

Let `g_out` be the maximum of the 24 products.  Then

```text
1_C24 <= g_out <= 1.
```

All coordinates and the fixed-label collision gauge are independent of
`s`.  The padded supports satisfy

```text
axis:     |t|<=21/1000,  dtheta/dt<1001/1000,
diagonal: |t|<=701/1000, dtheta/dt<141/100.
```

The exact union-bound calculation is

```text
axis unnormalised base     = 117/781250,
diagonal unnormalised base = 234/78125,
padded raw mass            < 3416517/781250000.
```

Using `4*pi*(R_G+R_W)>156/25`,

```text
mu_s(supp g_out)
 < 87603/125000000
 < 1/1000
```

uniformly for `|s|<=1/400`.

For the Lipschitz norm,

```text
|dt/dr| <= 1/R <= 25/4,
|dp/dphi| <= 1.
```

Hence every axis product has `Lip_1<7250`, every diagonal product has
`Lip_1<6350`, and a finite maximum preserves the largest Lipschitz constant:

```text
||g_out||_infinity + Lip_1(g_out) < 7251.
```

## Common terminal nonhit on the once-charged two-view law

Apply the same uniform SYZ comparison to `g_out` and choose a common finite
existential `H_out` so that the error is `<1/1000`.  For every normalized
proper view,

```text
mass(T_s^(-H_out) C24)
 <= integral g_out o T_s^H_out
 < 1/1000 + 1/1000
 = 1/500.
```

Round 51 places the forward and reverse proper views on one same-ID,
once-charged reference law.  Pulling the two terminal-hit predicates to that
law and using the union bound gives the relative common terminal survivor
fraction

```text
1 - 1/500 - 1/500 = 249/250,
```

with a strict `>` inequality.

This is only a common **terminal nonhit** statement.  It does not certify
avoidance at intermediate collisions, properness of the intersection after
restriction, a proper same-ID forward/reverse return, or a numerical
`H_out`.

## Why this does not produce `H_cover/beta`

The bump route and sufficient-rectangles route have different output types.

- `H_bump` controls total C24 mass of the whole normalized family.
- `H_cover/beta` requires a once-counted source fraction on every retained
  long leaf whose image properly crosses a registered direct-C24 Cantor
  rectangle.

A regular unstable segment can lie wholly inside an open C24 box.  Its C24
mass is one, but it need not cross both stable sides of any registered Cantor
rectangle.  Thus even a numerical whole-family hit cannot be renamed a
proper-crossing atlas.

The exact direct-cover threshold remains

```text
(1999/32000)*(2688/893303125)=21/111718750,
```

but the actual per-leaf crossing fraction is still null and the strictly
inferable lower bound remains zero.  Likewise, the SYZ coupling fraction
`tilde_zeta` is not `beta`: the former couples through a time-dependent
magnet, while the latter counts project-registered direct-C24 crossing
bundles.

## Latest-technology audit

The official arXiv feed was rechecked on 2026-07-20.  The latest relevant
versions remain `2606.10155v1`, `2604.25881v1`, `2604.19671v2`, and
`1210.0011v4`.

- `1210.0011v4` exposes the algebraic outer coupling rate but leaves the
  magnet fraction and compact reference schedule nonnumerical.
- The Demers--Liverani review `2606.10155v1` records
  `Lambda=1+2*kappa_min*tau_min` and surveys coupling/transfer-operator
  methods.  It contains no computer-assisted numerical magnet fraction,
  coupling gap, or C24 atlas for this pilot.
- `2604.25881v1` remains a qualitative sufficient-rectangles result and
  supplies neither a numerical common iterate nor a source width.

No newer official result found in this audit closes either of the two scalar
rate rows or the separate proper-crossing atlas.

## Strict frontier

```text
proof-level C_bump outer upper 3807/10:      CERTIFIED
safe hyperbolic rate upper 9/10:             CERTIFIED
numeric tilde_zeta lower / Delta upper:      NOT CERTIFIED
numeric H_bump:                              NOT CERTIFIED
uniform C24 outer majorant mass/norm:        CERTIFIED
existential common terminal nonhit relative fraction >249/250: CERTIFIED
numeric H_out:                               NOT CERTIFIED
proper common terminal restriction/return:  NOT CERTIFIED
numeric H_cover and actual beta:             NOT CERTIFIED
C_fw/C_rev/q and strong cemetery:            NOT CERTIFIED
Gate 4 / CM2:                                NOT CERTIFIED / NO-GO
```

## Validation

- Python syntax: `2/2` PASS;
- strict JSON with duplicate-key, non-finite and unknown-top-level rejection:
  PASS;
- deterministic certificate replay and manifest integrity: PASS;
- independent exact rational arithmetic for the outer prefactor, safe rate,
  conditional sample, majorant mass, Lipschitz norm and cover threshold: PASS;
- hostile manifest mutations: `98/98` rejected;
- certificate and verifier default modes: both fail closed with exact exit
  `2`;
- pinned dependencies and official-source/member hash scopes: PASS.

Artifacts:

- `cm2_gate34_round52_outer_rate_numeric_frontier_cert.py`
- `cm2_gate34_round52_outer_rate_numeric_frontier_verifier.py`
- `cm2-gate34-round52-outer-rate-numeric-frontier-manifest-2026-07-20.json`

## Next shortest route

1. Materialise one numerical lower `tilde_zeta` and upper `Delta` for the
   compatible compact pilot magnet.  The exact rational interface then
   produces a genuine integer `H_bump` and, with norm `7251`, a numerical
   `H_out` as well.
2. Independently properise the relative-`>249/250` same-ID common terminal nonhit
   restriction.  Positivity alone is not properness.
3. Continue the separate interval-certified Cantor source atlas to obtain
   numerical `H_cover/beta`; neither the bump nor magnet fraction substitutes
   for that object.
4. Join the resulting numerical clock(s) to the short-end defect moment,
   same-ID proper return, `C_fw/C_rev/q`, and strong cemetery.
