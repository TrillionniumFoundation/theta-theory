# CM2 Gate 3/4 Round 53 — effective clock decomposition and relative-atlas frontier

Date: 2026-07-20  
Scope: numerical `H_bump/H_out`, fixed-parameter `H_cover/beta`, and strict type separation  
Strict verdict: **Gate 4 NOT CERTIFIED; CM2 NO-GO**

## Result

This round obtains one new numerical component of the SYZ clock and one new
fixed-parameter qualitative atlas statement.  Neither result closes the
uniform numerical Gate-4 interface.

1. In the Euclidean `Z` convention used by the SYZ proper-family argument,
   the frozen project's numerical Growth recurrence gives

   ```text
   n_p <= 696*317 = 220632.
   ```

   This is the first numerical part extracted from the hidden coupling-gap
   schedule beyond Round 52's outer prefactor and hyperbolic rate.

2. The previously opaque `Delta` is reduced to five typed nonnumerical rows.
   If these rows are denoted `zeta0,S,R,C,lambda`, and

   ```text
   L_rec = min{L>=0 : 2*C*lambda^L <= zeta0*(1-zeta0)},
   ```

   then the exact SYZ scheduling algebra gives the safe bound

   ```text
   Delta <= D = 3*S + 2*R + 220632 + L_rec.
   ```

   Thus the project no longer treats all of `Delta` as one unexplained
   scalar.  The magnet/mixing and gap-tail rows remain nonnumerical, so no
   integer `D`, `H_bump`, or `H_out` is promoted.

3. For each fixed parameter `sigma`, the enlarged direct-C24 sufficient
   cover has a qualitative adapted relative source-thickness

   ```text
   eta_sigma^*
   = inf_V sup_U ell_*(U)/ell_*(V) > 0,
   ```

   where `V` is still selected into the compact admissible long-curve class
   by the Euclidean condition `|V|>=delta_rect`, while `U`
   ranges over source subcurves whose common finite-time image strictly
   crosses the appended direct-C24 Cantor rectangle.  This follows from
   compactness and openness of strict finite-time crossing.  It is fixed-map,
   nonnumerical, and conditional per admissible canonical proper family.

4. The exact conditional source-fraction conversion on every retained piece
   is

   ```text
   beta_sigma > (1999/2000)*eta_sigma^*.
   ```

   For this conditional `beta_sigma` to exceed the direct-C24 constant
   `2688/893303125`, the safe condition is

   ```text
   eta_sigma^* >= 43008/14285703575
               ~= 3.0106e-6.
   ```

   The strict lower bound on `beta_sigma` makes `>=` on `eta_sigma^*` safe and
   gives a strict `>` conclusion.  After multiplying by retained mass, the
   aggregate hit mass is strictly greater than

   ```text
   h_sigma > (3996001/64000000)*eta_sigma^*;
   ```

   the same `eta_sigma^*` threshold makes `h_sigma>21/111718750`.  No
   numerical `eta_sigma^*` is available.

## Numerical `n_p` component

The pinned project Growth recurrence in the Euclidean metric is

```text
Z_n^E/mass <= (C_p^E/2)*(1 + a^n*Z_0^E/mass),
a = 360134800/360493663,
C_p^E = 141*10^90*360493663/358863.
```

Exact integer arithmetic gives

```text
2*360134800^696 < 360493663^696,
a^696 < 1/2,
C_p^E < 2^317.
```

If the input is proper, `Z_0^E/mass<C_p^E`.  At
`n=696*317`, therefore,

```text
a^n*Z_0^E/mass < 2^-317*2^317 = 1.
```

The Growth upper is then strictly below `C_p^E`, so

```text
n_p <= 220632.
```

This statement is deliberately restricted to the frozen numerical project
class and its canonical Euclidean subdivision.  It is not a numerical
estimate for arbitrary billiard classes.

## Exact five-row decomposition of `Delta`

For a finite compatible reference chain, write:

| row | required numerical datum |
|---|---|
| `zeta0` | a positive lower bound for `tilde_zeta=min_q zeta(K_q)`, using `0<zeta0<=tilde_zeta<=1/2` |
| `S` | a nonnegative integer upper bound for `max_q s(K_q)`, including fixed-map mixing and super-proper crossing |
| `R` | a nonnegative integer upper bound for `max_q max(r_gap_top(K_q),s_prime(K_q))` |
| `C` | a finite upper bound `C>=1` for the rank-gap proper-recovery tail prefactor |
| `lambda` | a numerical upper bound `0<lambda<1` for the uniform gap-recovery base |

The official source chooses

```text
Delta0 = L_rec + max(s) + n_p,
Delta  = 2*max(s) + 2*max(r) + Delta0.
```

Substituting the new numerical `n_p` bound gives

```text
D = 3*S + 2*R + 220632 + L_rec.
```

The upper convention `tilde_zeta<=1/2` is harmless: the source crossing
bound already forces its chosen coupling fractions below `1/4`, and one may
always couple a smaller fraction.  On `(0,1/2]`, `zeta*(1-zeta)` is
increasing, so replacing `tilde_zeta` by its lower bound `zeta0` makes the
integer recovery test conservative.

The project Growth recurrence does not fill the other rows.  The
post-coupling gap collection contains arbitrarily short rank gaps and can
have infinite aggregate `Z`; a finite-`Z` recurrence alone gives neither the
rank-tail prefactor `C` nor the magnet/mixing fraction `zeta0`.

## Exact conditional `H_bump` and `H_out`

Once the five rows produce `D`, Round 52's safe proof-level comparison can be
evaluated with integer/rational inequalities only.

For the inner bump, take the least `m` satisfying

```text
(2724*3807/10)*(1-zeta0/2)^m < 21/111718750,
(2724*3807/10)*(9/10)^(2*D*m) < 21/111718750,
```

and set

```text
H_bump = 2*D*m.
```

For the outer majorant, take the least `m` satisfying

```text
(7251*3807/10)*(1-zeta0/2)^m < 1/1000,
(7251*3807/10)*(9/10)^(2*D*m) < 1/1000,
```

and set

```text
H_out = 2*D*m.
```

Verifier-only samples with the nonphysical values `zeta0=1/2,D=1` give
`H_bump=280` and `H_out=208`.  They are arithmetic checks, not pilot claims.

## Fixed-parameter compact/open relative-thickening lemma

Fix `sigma`.  Round 50 gives one finite but nonnumerical `N_sigma` such that
every admissible curve `V` selected by the Euclidean condition
`|V|>=delta_rect`, where

```text
delta_rect
=119621/(41476958890128*10^90)
```

contains a nondegenerate subcurve `U` whose `N_sigma`-th image crosses the
appended direct-C24 Cantor rectangle.

For each `V`, shrink `U` to a crossing core with positive stable-side and
singularity margins.  The branch is smooth on this core, and crossing is
strict because unstable curves are transverse to the stable sides.  Hence a
whole neighborhood of `V`, in the curve topology used in the sufficient-
rectangles compactness argument, retains a crossing subcurve.  Continuity
and uniform equivalence of the adapted line element make the adapted ratio
`ell_*(U)/ell_*(V)` stay bounded below by half its value at `V`.

The long-curve class is compact.  A finite subcover therefore gives

```text
eta_sigma^*
=inf_V sup{ell_*(U)/ell_*(V) : T_sigma^N_sigma U strictly crosses R_*}
>0.
```

Round 49's conditional density ratio `<2000/1999` is with respect to adapted
line length, so the crossing mass fraction on every retained piece is
strictly greater than

```text
(1999/2000)*eta_sigma^*.
```

This conditional fraction is the project `beta_sigma` type in the Round-49
direct-C24 ledger.  Multiplying by retained family mass `>1999/32000` gives
the aggregate strict hit bound above.  The pieces are disjoint, so the
aggregate is once-counted.

## Threshold typing ledger

The conditional and aggregate comparisons are different types but yield the
same exact adapted `eta_sigma^*` threshold:

| quantity | strict lower envelope | benchmark | safe condition on `eta_sigma^*` |
|---|---:|---:|---:|
| conditional retained-piece `beta_sigma` | `(1999/2000) eta_sigma^*` | `2688/893303125` | `eta_sigma^* >= 43008/14285703575` |
| aggregate crossing mass | `(3996001/64000000) eta_sigma^*` | hit gap `21/111718750` | `eta_sigma^* >= 43008/14285703575` |

Indeed,

```text
(2688/893303125)/(1999/2000)
= (21/111718750)/(3996001/64000000)
= 43008/14285703575.
```

The direct constant is conditional per retained piece; the hit gap is the
aggregate benchmark.  Cross-comparing the aggregate mass to the conditional
constant would be a type error and is not used.

## Why positivity is still non-effective

Qualitative compact/open thickness does not give a numerical lower bound
without numerical branch data.  For any `epsilon>0`, take the compact
singleton curve class `V=[0,1]`, with adapted line element equal to Euclidean
length, a source subcurve `U=[0,epsilon]`, and a
smooth branch mapping `U` across a unit target.  Fixed-map existence and
openness hold, but the best relative width is `epsilon`.  Thus the strict
inferable numerical lower from qualitative inputs remains zero.

A numerical lower could be obtained from rows such as

```text
adapted-compatible target transverse width w_sigma^*,
finite N_sigma,
N_sigma-step singularity clearance,
adapted branch derivative/distortion upper J_sigma^*,
adapted maximum source length L_max^*,
parameter-persistence modulus.
```

With all width, derivative and length rows in the adapted metric, the
elementary conditional bound would be

```text
eta_sigma^* >= w_sigma^*/((J_sigma^*)^N_sigma*L_max^*).
```

No such full branch row is currently registered.

Pointwise positivity also does not imply parameter-uniform positivity.
Knowing `eta_sigma^*>0` and `N_sigma<infinity` separately for every
`|sigma|<=1/400` does not give `inf eta_sigma^*>0` or `sup N_sigma<infinity`
without an open parameter neighborhood preserving the same branch,
singularity clearance, sides, and crossing margins.

Finally, whole-family target mass remains a different object: a regular
unstable segment can lie inside an open C24 box and have target mass one
without crossing the two stable sides of any registered Cantor rectangle.
Neither `H_bump` nor `tilde_zeta` is renamed `H_cover/beta`.

## Latest-technology audit

Official metadata and sources were rechecked on 2026-07-20.  The relevant
versions remain `2606.10155v1`, `2604.25881v1`, `2604.19671v2`,
`2502.07765v2`, and `1210.0011v4`.

- `1210.0011v4`, `Moving_final.tex`, exposes the exact coupling-time
  scheduling algebra.  It leaves magnet mixing `zeta,s`, stable scheduling
  `s_prime`, and gap/top recovery `r,C,lambda` qualitative.
- `2604.25881v1`, Proposition 3.19, supports the fixed-map compact/open
  thickening above, but publishes no numerical target sides, common iterate,
  branch clearance, derivative conversion, or parameter modulus.
- `2502.07765v2` applies complex projective cones to sequential dispersing
  billiards, but its billiard application imports existential
  `N_F(delta)`, `epsilon`, and finite cone diameter from the cited DL22
  interface.  It gives no pilot-specific numerical C24 mixing/atlas rows.

No checked source supplies the five missing magnet rows or a numerical
adapted relative source thickness for this pilot.

## Strict frontier

```text
numeric Euclidean SYZ n_p upper 220632:          CERTIFIED
five-row exact Delta decomposition:              CERTIFIED
numeric zeta0,S,R,C,lambda / numeric Delta:      NOT CERTIFIED
numeric H_bump / H_out:                          NOT CERTIFIED
fixed-s qualitative eta_sigma^*>0:               CERTIFIED CONDITIONAL
numeric or parameter-uniform eta_sigma^*:        NOT CERTIFIED
numeric H_cover / actual beta:                   NOT CERTIFIED
proper same-ID forward/reverse return:           NOT CERTIFIED
C_fw/C_rev/q and strong cemetery:                NOT CERTIFIED
Gate 4 / CM2:                                    NOT CERTIFIED / NO-GO
```

## Validation

- Python syntax: `2/2` PASS;
- strict JSON with duplicate-key, non-finite and unknown-top-level rejection:
  PASS;
- deterministic certificate replay and manifest integrity: PASS;
- independent exact rational arithmetic for `n_p`, the five-row `Delta`
  formula, both conditional clocks, aggregate coefficient, and both typed
  `eta` thresholds: PASS;
- hostile manifest mutations: `104/104` rejected;
- certificate and verifier default modes: both fail closed with exact exit
  `2`;
- pinned dependencies and official archive/member hash scopes: PASS.

Artifacts:

- `cm2_gate34_round53_effective_clock_relative_atlas_frontier_cert.py`
- `cm2_gate34_round53_effective_clock_relative_atlas_frontier_verifier.py`
- `cm2-gate34-round53-effective-clock-relative-atlas-frontier-manifest-2026-07-20.json`

## Next shortest route

1. Numerically construct one compatible magnet/source rectangle registry and
   fill `zeta0,S,R,C,lambda`; the exact formulas here then output genuine
   `Delta`, `H_bump`, and `H_out`.
2. On the direct-C24 cover branch, interval-enumerate the target stable sides,
   `N_sigma`-step clean branches, and adapted-compatible transverse widths,
   derivative bounds and maximum source length.
   First target the safe typed condition
   `eta_sigma^*>=43008/14285703575`.
3. Prove branch persistence on rational parameter intervals and finitely
   cover `[-1/400,1/400]`; fixed-map positivity alone is insufficient.
4. Keep the cover result separate from whole-family mixing, then join any
   numerical cover clock to the physical common-refinement/proper-return,
   `C_fw/C_rev/q`, and strong cemetery interfaces.
