# CM2 Round119 — eight repaired grazing traces: whole-trace C2 reach on extended source cylinders

Date: 2026-07-23  
Verdict: **VERIFIED per-trace reach `1/2500000000` in both extended/periodic source-cylinder models for all `8/8` repaired grazing traces.**

## Result

Round119 closes the whole-trace regularity and per-trace self-reach step that
Round118 deliberately left open:

- all `8/8` repaired source-grazing traces have a certified C2 splice between
  the second-order base block and the closed Round115 root graph;
- every individual trace has reach at least `1/2500000000` in
  `S^1_(9/25) x R_c` with metric `dr^2+dc^2`;
- every individual trace has the same certified reach in
  `S^1_(9/25) x R_p` with metric `dr^2+dp^2`;
- endpoint/interior, endpoint/endpoint, and distinct periodic-copy cases are
  paid inside the quantitative proof;
- an independent 1024-bit verifier replays all eight traces without importing
  the producer and rejects `69` semantic attacks plus `15` strict-JSON attacks.

The result is intentionally per trace and in extended ambient cylinders.  It
does not install reach of the union of the eight traces, separation from
unrelated singular strata, or an endpoint-inclusive two-sided collar in the
bounded physical phase space.

## Coordinate and scope contract

The source component is `G`, with radius `R_G=9/25`.  Put

```text
r(c) = (9/25) theta(c),
Gamma_c(c) = (r(c), c),
Gamma_p(c) = (r(c), p(c)).
```

The angular lift is selected independently on each trace by an orthogonal
local-normal matrix.  Reflected matrices merely reverse the local chart
orientation; they do not change the cylinder metric.  Every selected lift has
`local_x>0` and angular span strictly below `3/2`, so it remains in one
projective chart and admits a controlled periodic lift.

The source cosine `c` is the common monotone coordinate.  The closed root
portion contains `c=0`; the base portion continues to the far regular end.
The two ambient coordinates differ only in their second component:

- the cosine master uses the coordinate `c` itself;
- the momentum master uses the fixed-sign branch `p`.

## Base, root, and splice census

The producer uses 768-bit directed Arb arithmetic and exact rational
thresholds.  The base starts from `1024` cells per trace and adaptively bisects
only where a complete second-order metric/path box is not yet certified.

| ray | base accepted leaves | maximum base depth | root leaves | join cells |
|---:|---:|---:|---:|---:|
| 0 | 1,621 | 24 | 512 | 512 |
| 1 | 1,621 | 24 | 512 | 512 |
| 2 | 3,015 | 25 | 512 | 512 |
| 3 | 1,985 | 24 | 512 | 512 |
| 4 | 3,015 | 25 | 512 | 512 |
| 5 | 1,985 | 24 | 512 | 512 |
| 6 | 8,375 | 26 | 2,048 | 512 |
| 7 | 8,375 | 26 | 2,048 | 512 |
| **total** | **29,992** | — | **7,168** | **4,096** |

All base and root failure counts are zero.  The common producer join
partition digest is
`61f3f6fd3aa109e05aa31cc4d74f333d17c8f73ced22284db2209e96a39884af`.

The splice is not inferred from two unrelated interval images.  On the exact
positive-width neighborhood

```text
1/32768 <= c <= 1/16384
```

the fixed reverse path is `(1,-1,-1)`.  The projective definition, positive
flights, fixed incidence signs, the two algebraic reflection involutions, and
the unique Round115 affine implicit root identify the base and root formulae
with the same analytic physical state.  Also `q'(c)` is nonzero on this
neighborhood because

```text
q'(0)=0,
|q''|>1/1000,
|q'(c)|>c/1000>=1/32768000.
```

Therefore `theta`, `c`, and `p`, together with their first and second
`c`-derivatives, agree through the closure at `c=1/16384`.  The Round115
outer-upper projective value is used only as a base-cover bound; it is not
promoted to a physical point.

## Exact momentum identity and derivative bounds

On the base, each circle normal is unit by its certified circle equation; the
stereographic tangent is unit; and specular reflections are orthogonal.
Thus the initial velocity and source normal are exact unit vectors.  The
planar Lagrange identity gives

```text
c^2+p^2=1.
```

On the root, the source-chart normal is unit and
`p=sigma0*sqrt(1-c^2)`, so the same identity holds directly.  The analytic
splice keeps the same fixed `sigma0` branch.  Hence

```text
p_c  = -c/p,
p_cc = -1/p^3.
```

The certified `|p|>1/51` gives `|p_cc|<51^3=132651` exactly.  No
dependency-prone interval subtraction between equivalent formulas is used as
an acceptance predicate.

The worst directed bounds over all eight whole traces are:

| quantity | certified global enclosure summary | acceptance threshold |
|---|---:|---:|
| `theta_c` lower | `> 0.405959029507` | `> 2/5` |
| `theta_c` upper | `< 24.0468277123` | `< 28` |
| `|theta_cc|` | `< 24959754.293` | `< 30000000` |
| `|p|` | `> 0.0196099796808` | `> 1/51` |
| `|r_cc|` | `< 8985559.83234` | `< 10800000` |
| selected `local_x` | `> 0.696539278944` | `> 0` |
| angular span | `< 0.926365816374` | `< 3/2` |

Since `r_c=(9/25)theta_c`, both ambient curves have speed strictly above

```text
m = (9/25)(2/5) = 18/125.
```

For the momentum curve,

```text
|Gamma_p''| <= |r_cc|+|p_cc|
             < 10800000+132651
             = 10932651
             < 11000000.
```

The cosine curve obeys the same common acceleration budget
`A=11000000`.

## Quantitative reach lemma

Let `rho=1/2500000000`.  Compactness gives nearest-point existence on each
closed trace.

If a point at distance below `rho` had two nearest points
`Gamma(c),Gamma(d)`, write `h=d-c`, `Delta=Gamma(d)-Gamma(c)`, and
`w=y-Gamma(c)`.  Equal distances give
`w dot Delta=|Delta|^2/2`.  Interior stationarity, or the one-sided
minimum condition at the left endpoint, gives
`w dot Gamma'(c)<=0`.  Taylor's theorem and monotonicity of `r` yield

```text
|Delta| >= m h,
|Delta-Gamma'(c)h| <= A h^2/2.
```

The resulting contradiction has exact margin

```text
m^2-A rho = 1021/62500 > 0.
```

This single argument includes interior/interior, endpoint/interior, and
endpoint/endpoint double minimizers.

For injectivity of the radius-`rho` normal map, the local/far split uses
`|N'|<=A/m`.  The exact margins are

```text
m^2-4A rho = 49/15625 > 0,
(m^2-A rho)/m = 1021/9000 > 0.
```

Finally, each angular span is below `3/2`.  Since `pi>3`, distinct
`2*pi` lifts of one trace have centre separation greater than

```text
(9/25)(6-3/2) = 81/50 > 2 rho.
```

Thus the same reach bound descends to both periodic cylinder models.

## Independent verification and hostile tests

The verifier uses 1024-bit arithmetic, imports neither the Round119 producer
nor a shared Round119 mathematics helper, and independently reparses the
byte-pinned upstream certificates and formula sources.  It reproduces:

- all `29,992` adaptive base leaves and all `7,168` root leaves;
- all eight base/root C2 joins;
- all eight endpoint/interior and endpoint/endpoint reach cases;
- all eight periodic-lift separation cases;
- both ambient reach counts, `8/8` each.

The producer stores measured join bounds.  They are not trusted merely
because they clear a coarse threshold.  For each ray the verifier performs a
full-cover 1024-bit refinement of the same exact
`[1/32768,1/16384]` implicit graph and simultaneously dominates all twelve
saved quantitative claims:

- nine lower bounds: `F_e`, `|q''|`, two discriminants, three flights,
  the projective denominator, and the signed tangent side;
- three upper bounds: root-error width, tangent-side residual, and
  low-level equation residual.

The bounded policy permits refinement depths `1..3` but accepts only one
depth that dominates all twelve fields; it never splices individual fields
from different depths.  All eight rays pass at depth `1`, factor `2`, with
`1024` refined join cells each.  Total refined join cells are `8,192`, and
the failed-refinement count is zero.

Two tempting but mathematically false acceptance shortcuts were explicitly
removed during hardening:

- interval widths obtained by subtracting two analytically equivalent state
  or derivative formulae are dependency artifacts; they remain diagnostics
  only and are not acceptance predicates;
- a fixed source-chart radial sign cannot be required along the complete base
  trace, because the certified base legitimately crosses the registered
  source-chart seam.  The erroneous whole-base radial-sign guard was removed.
  The verifier instead checks the repaired Round118 chart/seam identity, the
  selected projective lift through `local_x>0`, the physical path margins, and
  the exact analytic root/base join.

The hostile suite rejects:

- `57` static semantic/schema/type/claim mutations;
- `12` re-signed measured-bound attacks, one inflation for every lower field
  and one deflation for every upper field;
- `15` strict-JSON attacks.

For the dynamic attacks, ray 0 is independently replayed at depths
`1,2,3`, using `1024`, `2048`, and `4096` cells.  Every forged measured
bound is rejected at every permitted depth.  A separate end-to-end
`F_e x 2` re-signed mutant passes the static contract, fails at all three
depths, and reaches bounded exhaustion, confirming fail-closed search
semantics.

## Cold replay and final hashes

One canonical producer run, two independent producer replays (including a
seeded `C`/`UTC` environment replay), two independent full verifier replays,
and the canonical verification artifact are byte-identical within their
respective classes.  Detailed commands and comparisons are recorded in the
Round119 cold-replay note.

Final byte hashes:

- producer:
  `c384d1e3b67d4560e34de542637317e6ce9f84dcaa4b12f3fd8030ce646fc057`
- certificate:
  `9ff985c91472e0ef57ced9fc10dbb6b2aa9e9627a5ac94c999caeefeca29a749`
- verifier:
  `9749f5e15e0106f0a07c963e69bfaad75e65fc192a120c36d237687623d41ace`
- verification:
  `c86d3694cd90c19c98f08965f0492f9f0ae41ed5f8fc272d393c9f64d1060cde`

Certificate result digest:
`f984a23b741a899b4d07bdcfc46a83faf9e9d42b619e12bb6d956cbf188a0247`.
Verification result digest:
`31e2c1e5c0f8be6954265e1912759fa946711391a5baf534d31c5f2fefab82fb`.

## Gate discipline

Round119 changes no frozen upstream artifact and makes no Gate5 promotion:

- Gate5 remains `10/18`;
- complete 18-field blocks remain `0`;
- F1--F6 actual-child fields remain `{0,0,0,0,0,0}`;
- actual standard-curve children remain `0`;
- canonical recut instances remain `0`;
- cross-trace union reach remains `0`;
- whole-trace uniform other-singularity separation remains `0`;
- endpoint-inclusive bounded-physical two-sided collars remain `0`;
- CM2 remains `NO-GO_FOR_CLAIM`.

At the closed grazing endpoint `c=0`, one has `p=sigma0=+1` or `-1`, so
`1-|p|=0`.  The extended-cylinder reach theorem therefore cannot be promoted
to a two-sided physical momentum collar at that endpoint.
