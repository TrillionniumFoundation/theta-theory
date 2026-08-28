# CM2 Gate 3/4 Round 51 — fixed-gauge and uniform bump frontier

Date: 2026-07-20  
Scope: Gate 4 cover/minorisation effectivity  
Strict verdict: **Gate 4 NOT CERTIFIED; CM2 NO-GO**

## Result

The abstract conjugacy loss left in Round 50 is absent for the frozen pilot.
The actual path is

```text
G fixed,
W translated by (s,0),
R_G=9/25, R_W=4/25,
|s|<=1/400,
```

with fixed obstacle labels and intrinsic boundary-arclength/outgoing-angle
coordinates on `N=G disjoint-union W`.  In these coordinates the labelled
map from the common section to the physical section is the coordinate
identity on both components; the physical embedding on `W` differs only by
an ambient translation.  Hence

```text
D_(r,phi) A_s = I_2,
m_s = inf sigma_min(D A_s) = 1,
hat_delta_s = delta_rect
            = 119621/(41476958890128*10^90)
```

uniformly on the whole parameter window.

This conclusion is instance-specific.  The generic `A_s` in
`cm2-bridge-note-v51.tex` is only an imposed `C^{r+1}`
measure-trivialising interface and contains no quantitative `C1` or
least-singular-value bound.  No numerical conclusion is drawn from that
generic interface.

The literature metric is the same metric used here.  Climenhaga--Day
parametrise each collision component by boundary arclength and define
admissible curves as graphs in `(r,phi)`.  Baladi--Demers explicitly use the
Euclidean metric on each such collision component.  Thus the Round-49
Euclidean leaf-length lower bound is passed to Proposition 3.19 without an
unrecorded adapted-metric conversion.

## A numerical uniform open C24 target

Inside the `G:E` axis C24 core

```text
t in (1/100,1/50),
p in (-1/500,1/500),
```

take the parameter-independent open box

```text
O_*:
t in (11/1000,19/1000),
p in (-3/2000,3/2000).
```

Its closure lies strictly inside the C24 core.  Since

```text
dr = R_G dt/sqrt(1-t^2),
cos(phi)dphi = dp,
4*pi*(R_G+R_W) < 1144/175,
```

its normalized collision mass satisfies

```text
mu_s(O_*) > 189/143000000
           = (225/32)*(21/111718750)
```

for every `|s|<=1/400`.

This is a numerical open coordinate target, not a dynamical Cantor rectangle.
Its edges are not asserted to be stable/unstable manifolds.

## Uniform qualitative time with a numerical hit fraction

The frozen smooth bump already satisfies

```text
0 <= g <= 1_C24,
mu_s(g) > 21/55859375
        = 2*(21/111718750),
||g||_infinity + Lip_1(g) < 2724.
```

Theorem 1' of Stenlund--Young--Zhang, arXiv:1210.0011v4, applies to regular
measured unstable families.  The object-type join is quantitative before the
theorem is called.  The frozen cone gives

```text
|log rho(x)-log rho(y)| <= 5e26 ell_*(x,y)^(1/3),
(inverse adapted contraction)^(1/3) < 93/100.
```

Every admissible image `u`-curve has Euclidean length
`<9*pi/25<198/175`, hence adapted length `<40`.  If `s(x,y)=n` is the
homogeneous separation time, pullback through the common branch therefore
gives

```text
|log rho(x)-log rho(y)|
 < 2e27*(93/100)^s(x,y).
```

This is precisely the SYZ dynamical log-Hölder type.  The same numeric cone
provides a finite uniform Euclidean `Z` envelope.  On the comparison side,
the invariant collision law is the same probability for every `s`, has
constant density `1` and log-density constant `0`; SYZ Lemma `1'implies1`
embeds this smooth-density case into Theorem 1'.

Applying that theorem to a normalized canonical family `G` and this common
probability for the stationary sequence `K_s,K_s,...` gives existential
constants

```text
C_bump < infinity,
0 < theta_bump < 1,
```

common to all such `G` and all `|s|<=1/400`.  Therefore one common finite
integer exists with

```text
H_bump
= max(0,1+ceil(log(2724*C_bump/epsilon_hit)
               /(-log(theta_bump))))

(T_s^H_bump)_* G(C24) > epsilon_hit,
epsilon_hit = 21/111718750.
```

This is stronger than Round 50's pointwise-in-`s` existence statement: the
integer can be chosen uniformly over the parameter window and over the
frozen canonical family class.  It is still not numerical, because the
paper does not publish values of `C_bump` or `theta_bump`.

The conclusion is a whole-family C24 mass minorisation at an existential
uniform time.  It is not a per-retained-leaf crossing-width statement and
does not materialise the sufficient-rectangles source atlas.

## Exact non-effectivity check

No candidate integer can be certified from the qualitative inequalities
`C<infinity` and `0<theta<1` alone.  For any proposed `H0`, the admissible
formal choice

```text
C=1,
theta=1-1/(2(H0+1))
```

satisfies, by Bernoulli's inequality,

```text
theta^H0 >= 1-H0/(2(H0+1)) > 1/2,
2724*C*theta^H0 > 1362 > epsilon_hit.
```

This is a logical non-effectivity model, not a counterexample to the physical
billiard.  It proves that an explicit `H0` requires numerical exponential
constants or a direct interval crossing computation.

## Why the existing finite registries are not the missing source atlas

The local registries do contain substantial finite geometry, but their
types do not match Proposition 3.19's finite proper-crossing source cover.

- The 24 C24 boxes are coordinate target boxes with total normalized mass
  strictly below `1/2500`; their edges are not registered stable/unstable
  manifolds.
- The 441280 candidate-key universe is a branch envelope, not a cover by
  dynamically defined Cantor rectangles, and its exact nonempty count is
  not known.
- Neither registry supplies proper-crossing margins for every admissible
  `u`-curve at `delta_rect`.

Consequently they cannot be renamed `K_rect` or used to assign a crossing
source fraction.

## Remaining numerical cover rows

The original sufficient-rectangles route still lacks:

| ID | Missing numerical object |
|---|---|
| `R_Cantor` | stable/unstable sides and a positive dense subset of a dynamical Cantor target inside `O_*` |
| `K_rect` | interval rows and cardinality of a finite proper-crossing source subcover at `delta_rect` |
| `delta_density` | quantitative target leaf-density radius |
| `C_mix,theta_mix` | effective correlations for the actual source/target sets, or numerical `C_bump,theta_bump` for the now type-complete bump bypass |
| `N_mix` | numerical common hit iterate |
| `r_transverse` | target-crossing margin |
| `J_branch` | inverse unstable-Jacobian/distortion conversion to source width |
| `omega_parameter_dynamic` | persistence modulus for Cantor sides, singularity avoidance and crossing branches |

The gauge factor and an explicit open target are no longer missing.  The
strict numerical state remains

```text
uniform m_s=1:                                  CERTIFIED
explicit uniform open C24 target:               CERTIFIED
uniform finite H_bump exists:                   CERTIFIED
whole-family hit fraction >21/111718750 there:  CERTIFIED
numeric H_bump / numeric H_cover:               NOT CERTIFIED
per-leaf cover crossing source fraction:        NOT CERTIFIED
complete numeric C_fw/C_rev/q:                  NOT CERTIFIED
strong cemetery / Gate 4 / CM2:                 NOT CERTIFIED / NO-GO
```

## Literature audit

Official arXiv metadata was rechecked on 2026-07-20.  The relevant versions
remain `1210.0011v4`, `2604.25881v1`, `1807.02330v4`, and
`2104.06947v3`.

The pinned-source hash type is explicit: the `2604.25881v1` and
`1807.02330v4` hashes identify the main TeX archive members
`billiard-mme-arXiv-v1.tex` and `maxentropypublished.tex`, respectively,
while the `1210.0011v4` hash identifies the whole source tar archive; its
`Moving_final.tex` member is pinned separately.

- Climenhaga--Day Proposition 3.19 is fixed-map and qualitative.  Its proof
  exposes no numerical finite cover, mixing time, or crossing width.
- Baladi--Demers supplies the Euclidean collision metric and qualitative
  Cantor-rectangle constructions, but not their numerical dynamical sides or
  density radius.
- Stenlund--Young--Zhang supplies uniform exponential memory loss on a
  compact configuration class, including regular measured unstable
  families.  Its rates are uniform but existential.

No checked source supplies the numerical constants needed to turn
`H_bump<infinity` into an integer.

## Validation

- Python syntax: `2/2` PASS;
- strict JSON with duplicate-key and non-finite-constant rejection: PASS;
- deterministic certificate replay and manifest integrity: PASS;
- independent exact gauge/target/threshold arithmetic: PASS;
- hostile manifest mutations: `90/90` rejected;
- certificate and verifier default modes: fail closed with exit `2`;
- dependency, leaf and recursive SHA replay: PASS.

Artifacts:

- `cm2_gate34_round51_uniform_gauge_bump_frontier_cert.py`
- `cm2_gate34_round51_uniform_gauge_bump_frontier_verifier.py`
- `cm2-gate34-round51-uniform-gauge-bump-frontier-manifest-2026-07-20.json`

## Next shortest route

1. Extract or prove numerical `C_bump,theta_bump` for the frozen compact
   two-disk class; the displayed formula then immediately gives a real
   integer `H_bump` without constructing Cantor rectangles.
2. If that is unavailable, interval-enumerate the stable/unstable sides of
   one target Cantor rectangle and a finite proper-crossing source atlas,
   including transverse and singularity margins.
3. Join the resulting numerical clock to the common proper-law repair and
   the same-measure short-end moment before forming `C_fw/C_rev/q` and the
   strong cemetery.

Until a numerical time and those object-level joins are installed, Gate 4
and unconditional CM2 remain open.
