# CM2 Gate 3/4 Round 54 — numerical Growth, magnet-gap rate, and interval-atlas frontier

Date: 2026-07-20  
Scope: Round-53 five-row SYZ clock and adapted direct-C24 crossing atlas  
Strict verdict: **Gate 4 NOT CERTIFIED; CM2 NO-GO**

## Result

This branch isolates a genuine numerical **conditional replacement
candidate** for one of Round 53's five nonnumerical clock rows.  Independent
audit found that the official magnet-gap density `checkrho|V` has not yet
been identified, with the same ID, with the project's numerical
`2000/1999` adapted-density cone.  Consequently the candidate cannot fill
the official five-row `lambda` line.

```text
conditional magnet-gap candidate lambda_bar = 9997/10000:         CERTIFIED CONDITIONAL
same-ID checkrho density-cone join:                               NOT CERTIFIED
numeric official five-row lambda:                                NOT CERTIFIED
numeric C, R, zeta0, S:                                           NOT CERTIFIED
numeric Delta, H_bump, H_out:                                     NOT CERTIFIED
uniform numerical eta_sigma^*, H_cover, beta:                     NOT CERTIFIED
```

The two other advances are:

1. an explicit frozen fixed-map version of the Growth lemma, with numerical
   `C_gr` and `vartheta`, together with a pinned check of the upstream
   Euclidean SYZ recurrence; and
2. a strict rational interval-atlas schema which pays the correct
   Euclidean/adapted conversion and can fail close on incomplete physical
   branch rows.

No whole-family hit is renamed a crossing, no endpoint collision-rank tail is
used as a magnet-gap rank tail, and the `696` half-life is not renamed the
SYZ constant `c_p`.

## 1. A numerical square-root-growth constant `C_e`

Round 42 proved, on every physical smooth branch and uniformly for
`|sigma|<=1/400`,

```text
ell_E(T_sigma W) < C_len sqrt(ell_E(W)),
C_len = 5962448355/5191.
```

If all intermediate images are homogeneous, iteration gives

```text
ell_E(T_sigma^n W)
 < C_len^(2-2^(1-n)) ell_E(W)^(2^-n)
 < C_len^2 ell_E(W)^(2^-n).
```

Thus the official square-root-growth row can safely use

```text
C_e = (5962448355/5191)^2 < 2^41.                 (1.1)
```

This is restricted to the frozen stationary physical family.  It is not a
numerical theorem for arbitrary moving-configuration sequences.

## 2. Numerical frozen fixed-map Growth lemma

The project boundary recurrence is in adapted length:

```text
Z_n^* <= a^n Z_0^* + [B/(1-a)] mass_*,
a = 360134800/360493663,
B = 2*10^90,
delta_* = 10^-90.
```

To recover the official Euclidean endpoint-tail type, both metric
conversions must be paid.  On the invariant cone,

```text
(5/27) dell_E < dell_* < (141/4) dell_E.
```

For Euclidean arclength `m_E`, compare first with adapted arclength `m_*`:

```text
m_E <= (27/5)m_*.
```

An Euclidean endpoint collar of length `epsilon` has adapted length below
`(141/4)epsilon`.  The conditional density ratio is below `2000/1999`, so

```text
m_E{r_artificial,n<epsilon}
 <= (27/5)(141/2)(2000/1999) epsilon Z_n^*.
```

The true homogeneous endpoint event is a subset of the artificial-chop
endpoint event.  Equal adapted `delta_*` subdivision gives

```text
Z_0^* <= 1 + (141/2)ell_E(W)/delta_*,
mass_*(W) <= (141/4)ell_E(W).
```

Consequently

```text
m_E{r_W,n<epsilon}
 <= C_gr [a^n+ell_E(W)] epsilon,                   (2.1)

C_gr
= 6456698162465400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
  /239122379.
```

Equation (2.1) is a numerical Growth lemma for the registered stationary
project class.  The deliberately huge number is a proof-safe constant, not
an optimisation.

The dependency validator also pins the upstream **Euclidean**, not only
adapted, SYZ recurrence:

```text
Z_n^E/mass <= (C_p^E/2)(1+a^n Z_0^E/mass).          (2.2)
```

Its properness test is

```text
a^N Z_0^E/mass < 1,                                 (2.3)
```

because (2.2) then gives `Z_N^E<C_p^E`.  Applying (2.2)--(2.3) to a
particular gap law still requires that law to lie on the same registered
numerical density carrier.

## 3. Conditional numerical magnet-gap exponential rate

For a magnet gap of rank `R>=1`, the official recovery proof starts from

```text
Z_(R-1)/mass
 <= C_e^2 c_g^-2 |W_tilde|^-2 Lambda^(2R),
Lambda = 180337/144000.                              (3.1)
```

Assume the still-unmaterialised same-magnet rows are supplied in dyadic form,
and assume a same-ID density join places the official `checkrho|V` law in the
registered `2000/1999` cone:

```text
c_g >= 2^-G,
|W_tilde| >= 2^-W,
G,W nonnegative integers.
```

The density join must also supply a rank-independent total clock debit
`I_density`, absorbing both density regularisation and the recovery needed
for any certified entry-`Z` inflation.  This is an independent hypothesis,
not a value extracted in this round.

Using (1.1), `Lambda^2<2`, and the certified strict half-life

```text
a^696 < 1/2,
```

the initial exponent in (3.1) is strictly below

```text
2^[82+2G+2W+R].
```

Only under that join may (2.2) be applied to (3.1).  Then (2.3) holds and
every rank-`R` gap is proper before

```text
(R-1)+I_density+696(82+2G+2W+R)
=697R+696(82+2G+2W)-1+I_density.                    (3.2)
```

This is not the assertion `c_p=696`.  The extra original rank time produces
the slope `697`, while density recovery and all unknown same-magnet constants
enter a rank-independent intercept and the prefactor.

The rank tail has base `Lambda^-1`.  Therefore the exact algebraic bad-mass
base implied by (3.2) is `Lambda^(-1/697)`.  Exact integer arithmetic gives

```text
(9997/10000)^697 > 144000/180337 = Lambda^-1,
(2499/2500)^697 <= 144000/180337.                    (3.3)
```

Hence

```text
lambda_bar = 9997/10000                              (3.4)
```

is a safe rational replacement candidate on the frozen stationary class
**conditional on the same-ID density join**.  Since that join is open, the
Round-53 five-row `lambda` remains `None`/`NOT CERTIFIED`.

### Reparameterising `proper_part`

Let `C_g''` be the same-magnet regular-density rank-tail constant, and let
`r_base` cover the rank-zero gaps, top density and excess pieces.  Put

```text
K      = 82+2G+2W,
A_gap  = 696K-1+I_density,
C_bar  = max(1,C_g'') lambda_bar^(-max(A_gap,r_base)).
```

Then the nonproper mass is at most `C_bar lambda_bar^m`.  Once

```text
C_bar lambda_bar^r < 1-zeta,
```

the same operation as in the official `proper_part` proof adds a suitable
portion of already proper mass to make the declared bad mass exactly
`C_bar lambda_bar^m`.  Thus `(C_bar,lambda_bar)` is a valid safe
reparameterisation, not merely a formal asymptotic comparison.

`C_bar` and `r` are not numerical because the density join and
`I_density,G,W,C_g'',zeta,r_base` are not.
The verifier's nonphysical arithmetic sample `G=W=1`, `C_g''=1`,
`zeta=1/4`, `I_density=r_base=0` gives `A_gap=59855` and least gap-only
`r=60814`.  Its zero density intercept is sample data, not a physical claim.

## 4. Exact atomisation of the missing prefactor

The new `C_gr` reduces the official Cantor/gap prefactor to fewer physical
rows.  If

```text
tildeC <= T
```

in the stable-length comparison

```text
r^s >= tildeC^-1 inf_n Lambda^n r_(W,n),
```

then the official proof gives

```text
C_g' <= C_gr*T*69/(1-Lambda^-1),
C_g  <= (hat_c+11/10) C_g',
hat_c=20/3807.
```

Here the upstream homogeneous-curve bound is pinned explicitly as
`L0<68`, hence the factor `1+L0` is safely replaced by `69`.

After installing the same-magnet density-carrier join with ratio
`<=2000/1999`,

```text
C_g'' <= K_g T,

K_g
=25371039574349071106520000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
 /2481327254508611.                                 (4.1)
```

The minimal remaining physical rows are now explicit:

- a numerical upper `T` for the stable-length comparison;
- a same-magnet `c_g>=2^-G`;
- a same-magnet `|W_tilde|>=2^-W`;
- the same-ID `checkrho|V` density-carrier identification needed both for
  `C_g''` and for the Euclidean recovery recurrence, including its
  rank-independent density intercept;
- a numerical rank-zero/top/excess clock `r_base`.

The one-collision endpoint-rank tail is not any of these rows and is not used.

## 5. Fail-closed rational interval-atlas builder

Round 53's target remains

```text
eta_sigma^* >= 43008/14285703575.                    (5.1)
```

For a rational parameter interval row `I_j`, a branch word of depth `N_j`,
target-crossing width `w_j`, **per-step** derivative/distortion upper `J_j`,
and maximum source length `L_j`, the builder accepts exactly two coherent
modes.  Thus `J_j^N_j` is the registered `N_j`-step product upper.

All-adapted data:

```text
eta_j >= w_j/(J_j^N_j L_j).                          (5.2)
```

All-Euclidean data:

```text
eta_j^* >= (20/3807) w_j/(J_j^N_j L_j).              (5.3)
```

The factor in (5.3) is

```text
(adapted/Euclidean target lower)
 /(adapted/Euclidean source upper)
=(5/27)/(141/4)=20/3807.
```

Mixed-metric rows are rejected.  A physical success requires an exact finite
cover of `[-1/400,1/400]` and of the entire Euclidean-selected long-curve
class, the same enlarged sufficient-cover target ID inside direct C24,
physical branch words, strict singularity clearance, crossing-side margins,
and interval-wide—not midpoint-only—parameter persistence.  Only then may

```text
eta_uniform=min_j eta_j
```

be compared with (5.1).

No such physical row is currently registered.  The manifest contains only
two exact arithmetic samples and reports both physical row counts as zero.

## 6. Technology audit

Official metadata and source members were checked again on 2026-07-20.

- `1210.0011v4` exposes the rank-recovery structure used above, but its
  `c_g,C_g'',W_tilde` and top constants remain qualitative.
- `2104.06947v3` exposes many projective-cone formulas, but its proper-crossing
  proof still chooses mixing times `n_i^*` existentially and obtains a common
  block through a qualitative compact subcover.
- `2604.25881v1` remains target-sensitive but supplies no numerical source
  width, branch clearance, derivative or parameter-interval atlas.
- `2502.07765v2` continues to import existential finite mixing and
  cone-diameter constants.

No checked source supplies the physical rows missing from (4.1) or (5.2)--
(5.3).

## 7. Strict frontier

```text
numeric frozen fixed-map C_e,C_gr,vartheta:         CERTIFIED
conditional gap candidate 9997/10000:              CERTIFIED CONDITIONAL ON SAME-ID DENSITY JOIN
official five-row lambda:                          NOT CERTIFIED
same-ID checkrho density join/intercept:            NOT CERTIFIED
numeric same-magnet C and recovery R:               NOT CERTIFIED
numeric zeta0 and mixing S:                         NOT CERTIFIED
numeric Delta/H_bump/H_out:                         NOT CERTIFIED
metric-safe conditional interval-atlas schema:      CERTIFIED
physical parameter interval rows:                   0
uniform numeric eta_sigma^*/H_cover/beta:            NOT CERTIFIED
proper same-ID return/q/strong cemetery:             NOT CERTIFIED
Gate 4 / CM2:                                       NOT CERTIFIED / NO-GO
```

## 8. Validation

- Python syntax: `2/2` PASS;
- pinned dependency and official source hash scopes: PASS;
- strict JSON, duplicate-key, non-finite and unknown-top-level rejection:
  PASS;
- deterministic replay/re-emission: PASS;
- independent exact rational checks for `C_e`, `C_gr`, the rank slope `697`,
  both sides of (3.3), `K_g`, and both metric modes: PASS;
- hostile mutations: `216/216` rejected;
- certificate and verifier defaults: both exact `exit 2`;
- leaf SHA ledger: PASS.

Artifacts:

- `cm2_gate34_round54_numeric_growth_gap_rate_interval_atlas_frontier_cert.py`
- `cm2_gate34_round54_numeric_growth_gap_rate_interval_atlas_frontier_verifier.py`
- `cm2-gate34-round54-numeric-growth-gap-rate-interval-atlas-frontier-manifest-2026-07-20.json`

## Next shortest route

1. Interval-prove `tildeC<=T`, `c_g>=2^-G`, and
   `|W_tilde|>=2^-W` on one same-cover magnet registry; identify its
   `checkrho|V` with the numerical density cone and bound the resulting
   rank-independent density intercept.  Then (4.1) makes `C_g''`, `C_bar`
   and the gap part of `R` numerical, and promotes the conditional
   `9997/10000` candidate.
2. Numerically close the rank-zero/top/excess clock and the magnet fraction
   `zeta0`; combine them with the promoted `lambda_bar` in the Round-53
   exact `Delta/H_bump/H_out` builder.
3. Populate the interval-atlas schema with clean physical branch words and
   adapted-compatible widths, first targeting (5.1), and exactly cover the
   full parameter window and the full selected source-curve cover.
4. Keep this crossing atlas separate from whole-family mixing, then join it
   to the physical common-refinement/proper-return and cemetery interfaces.
