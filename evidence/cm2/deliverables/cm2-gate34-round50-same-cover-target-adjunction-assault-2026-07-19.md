# CM2 Gate 3/4 Round 50 — Enlarged-cover C24 target adjunction

Date: 2026-07-19  
Scope: Gate 4 target-sensitive cover only  
Strict verdict: Gate 4 **NOT CERTIFIED**; CM2 **NO-GO**

## Result

The Round-49 cover-membership gap is closed at the strongest level supported
by the cited arguments: **for each fixed parameter** `s`, a positive
closure-contained direct-C24 target rectangle can be adjoined to enlarge the
published countable sufficient cover.  A separate positive uniformly-dense
subset of that target, rather than a global `0.9` claim about the target
rectangle itself, is used to rerun the proof of Proposition 3.19.

The proposition is applied to the physical billiard `hat_T_s`.  Writing
`T_s=A_s^{-1} hat_T_s A_s`, compactness and the diffeomorphism property give

```text
m_s = inf_x sigma_min(DA_s(x)) > 0,
hat_delta_s = m_s * delta_rect > 0.
```

Thus a reference admissible `u`-curve of length at least

```text
delta_rect
= 119621 /
  (41476958890128 * 10^90),
```

maps to a physical admissible `u`-curve of length at least `hat_delta_s`.
There exists a finite, but nonnumerical, iterate `N_s` such that every curve
in this pulled-back admissible class contains a subcurve whose `N_s`-th
`T_s` image crosses a solid rectangle contained in C24.  No claim is made for
arbitrary curves outside that admissible class.

This is a fixed-map qualitative theorem.  It is not a numerical `H_cover`,
does not produce a source-length or source-mass fraction, and is not uniform
over `|s|<=1/400`.

## Enlarged-cover adjunction and fixed-s pullback

The proof graph is as follows.

1. Fix `s`, put `hat_O_s=A_s(O_s)`, and use the physical finite-horizon
   billiard `hat_T_s`.  The positive scale supplied to Proposition 3.19 is
   `hat_delta_s=m_s*delta_rect`, not `delta_rect` without conversion.
2. The Baladi--Demers open-target construction gives a positive locally
   maximal physical Cantor rectangle `hat_R_*` with
   `D(hat_R_*) subset hat_O_s`.
3. Leafwise Lebesgue differentiation and absolute continuity select a
   separate positive uniformly-dense subset `hat_P_* subset hat_R_*` in the
   orientation required by the forward unstable-curve argument.  The suite
   does **not** assert that `hat_R_*` itself satisfies the published cover's
   global `0.9` condition.
4. If `hat_R` is the published countable cover, then
   `hat_R' = hat_R union {hat_R_*}` is an enlarged countable cover.  At
   `hat_delta_s`, retain the original finite proper-crossing source subcover.
5. Liouville mixing for the finitely many original-source/`hat_P_*` pairs
   gives one finite iterate `N_s`.  The crossing argument extracts the
   required physical target-crossing subcurve.
6. Pull `hat_R'`, `hat_R_*`, and the subcurve back by `A_s^{-1}`.  Conjugacy
   preserves stable/unstable manifolds and crossing, while the pulled-back
   solid rectangle lies in `O_s subset C24`.

The enlarged-cover adjunction and conjugacy pullback are derived lemmas, not
verbatim numbered theorems.  Appending the target changes neither
countability nor any previous target statement, while the new target is
handled by one additional finite family of mixing intersections.

## Literature audit

The official arXiv API was rechecked on 2026-07-19: the current versions are
still `2604.25881v1` and `1807.02330v4`.

- Climenhaga--Day,
  [arXiv:2604.25881v1](https://arxiv.org/abs/2604.25881), Proposition 3.19
  and its proof sketch: source lines 1568--1586 in the official source,
  SHA256
  `b8f79a99f5f98648f91848cd7b4e489846f4512d6ed35ebd042229da3c89ee94`.
  The proof explicitly separates the finite proper-crossing source subcover
  from the target-dependent dense-set/mixing step.
- Baladi--Demers,
  [arXiv:1807.02330v4](https://arxiv.org/abs/1807.02330): locally maximal
  and proper-crossing rectangles at source lines 2430--2468, countable
  high-density cover at lines 3914--3944, and a positive Cantor rectangle
  with solid hull inside an arbitrary open target at lines 4067--4096.
  Official-source SHA256:
  `c1e0189b271fdd1303b425d096a9e1d8685a83f74d139b37a534a0530a6020aa`.
- The finite-pair mixing/crossing mechanism is visible in the same
  Baladi--Demers source at lines 2508--2533.  These lines support selecting a
  separate uniformly-dense target subset; they do not promote the arbitrary
  open-target rectangle itself to the global `0.9` cover class.

These sources support the fixed-parameter adjunction.  They expose no
numerical rectangle rows, density radius, mixing time or crossing width.

## Exact numerical frontier

Round 49 retains incidence-safe family mass strictly greater than
`1999/32000`.  The direct-C24 route would close the desired hit gap if the
source fraction on every retained leaf satisfied

```text
zeta_direct >= 2688/893303125,
1/332330 > 2688/893303125 > 1/332331,
(1999/32000)*(2688/893303125) = 21/111718750.
```

Proposition 3.19 gives a nonempty crossing subcurve, not this quantitative
fraction.  Positive mixing intersection can be supported on arbitrarily thin
subcurves.  Therefore the strict uniform lower bound inferable for both the
source fraction and actual `beta` remains `0`.

The first missing numerical constants are now frozen as:

| ID | Missing datum |
|---|---|
| `K_rect` | finite proper-crossing physical source-cover cardinality and coordinates at `hat_delta_s` |
| `m_conjugacy` | numerical lower length factor for `A_s`, including a uniform version for a common atlas |
| `m_rect` | numerical Liouville masses of source rectangles and `P_*` |
| `delta_density` | density radius from the Lebesgue-density step |
| `C_mix, theta_mix` | effective correlation constants for the actual sets |
| `N_mix` | first common positive-intersection time |
| `r_transverse` | transverse-intersection margin in the crossing lemma |
| `J_branch` | inverse-Jacobian/distortion conversion to source mass |
| `omega_parameter` | persistence modulus over `|s|<=1/400` |

Without these rows there is no interval-enumerable `H_cover` and no
quantitative `beta`.

## Parameter-window boundary

The sufficient-rectangles theorem quantifies over one fixed physical billiard
map.  The pointwise factor `m_s>0` follows qualitatively from the fixed-s
diffeomorphism, but no numerical value or parameter-uniform numerical lower
bound is installed.
Compactness of `[-1/400,1/400]` alone does not turn pointwise finite times
into one common time: one first needs an open parameter neighborhood on which
the labelled source and target rectangles, proper-crossing margins,
singularity avoidance, and the selected mixing/crossing branches persist.
No such robustness modulus is present in the cited arguments or the current
physical registry.

Thus the precise status is:

- fixed-`s` qualitative enlarged-cover C24 target hit on the pulled-back
  admissible `u`-curve class: **CERTIFIED**;
- fixed-`s` finite but unspecified target-hit iterate: **CERTIFIED**;
- numerical target rectangle/source-cover rows: **NOT CERTIFIED**;
- uniform numerical `H_cover` over `|s|<=1/400`: **NOT CERTIFIED**;
- quantitative source fraction and actual `beta`: **NOT CERTIFIED**;
- physical whole-family grouping and same-ID fw/rev cover: **NOT CERTIFIED**;
- `C_fw/C_rev/q`, strong cemetery and Gate 4: **NOT CERTIFIED**.

## Validation

- Python syntax: `2/2` PASS;
- strict JSON and deterministic manifest replay: PASS;
- verifier replay/integrity: PASS;
- hostile mutation rejection: `72/72` PASS;
- certificate and verifier default mode: fail closed with exit `2`;
- dependency hash and independently recomputed internal replay digest: PASS;
- duplicate keys, unknown top-level keys, and non-finite JSON constants are
  rejected.

Artifacts:

- `cm2_gate34_round50_same_cover_target_adjunction_cert.py`
- `cm2_gate34_round50_same_cover_target_adjunction_verifier.py`
- `cm2-gate34-round50-same-cover-target-adjunction-manifest-2026-07-19.json`

## Next shortest route

1. Numerically bound the conjugacy length factor, materialize one direct-C24
   target rectangle and the finite proper-crossing physical source subcover
   with interval coordinates for a seed parameter.
2. Certify transverse margins and branch/singularity persistence on a
   rational parameter interval; subdivide `[-1/400,1/400]` until finitely
   covered.
3. Add effective Liouville mixing/correlation bounds and use them to compute
   `N_mix`, then propagate a transverse ball backward with certified
   distortion to obtain a genuine source-fraction lower bound.
4. Join the resulting rows to the physical Borel whole-family registry,
   same-ID fw/rev return, `C_fw/C_rev/q`, and cemetery.

Until those numerical and measure-theoretic joins are installed, strict Gate
4 and unconditional CM2 remain open.
