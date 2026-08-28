# CM2 Round191 — source-G stereographic endpoint-chart spike

Date: 2026-07-26  
Verdict: `VALIDATED` for the 288-face endpoint-chart feasibility question

## Question

Can the `288` Round188 outgoing-W factor faces that touch `p=+/-1` be
resolved without further p bisection by replacing

`rp = sqrt(1-p^2)`

with the smooth rational endpoint chart

```text
p  = sigma * (1-u^2) / (1+u^2)
rp =             2*u / (1+u^2),  u >= 0,
```

and then applying a complete four-corner/four-edge boundary arrangement in
`(u,s)`?

## Method

The read-only probe
`cm2_round191_source_g_stereographic_endpoint_chart_probe.py` was run at
SHA256

`b37c0a06a392107d7d859c65ab323cf04c7f06cdd4f51cba59c2049c53f70b9f`.

It pins Round186, Round188, Round189, and the complete verified Round182
package. Because the Python imports occur before the pins can be checked,
this remains a probe-only trust boundary rather than an adversarial import
sandbox.

For endpoint sign `sigma in {-1,+1}` and the opposite p edge `p_inner`, the
probe uses

```text
u_max^2 = (1-sigma*p_inner)/(1+sigma*p_inner).
```

For every face it checks with exact rational arithmetic that:

- `u=0` maps to `(p,rp)=(sigma,0)`;
- `u=u_max` maps exactly to `p=p_inner`;
- the numerator polynomial of `p^2+rp^2-1` is identically `(0,0,0)`; and
- the algebraic `u_max` is enclosed by the least selected 192-bit dyadic
  upper bound used for the full-face interval evaluation.

The outgoing-W factor geometry is rebuilt as an `(u,s)` dual on each fixed
t-face. The transformed and original Round186 values of `HPLUS`, `HMINUS`,
`NX`, and `NY` are required to overlap at all four exact corners.

For the strict inactive factor the probe requires full-face direct or
centered C0 exclusion. For the active factor it computes full-face `du` and
`ds`, all four corner signs, and on every edge both a direct/centered C0
enclosure and the tangential derivative. Each edge must be either strictly
zero-free or contain one uniquely bracketed zero.

Two mutually exclusive face normal forms are accepted:

1. `UNIQUE_TWO_ENDPOINT_FACTOR_CURVE`: exactly two uniquely bracketed
   boundary endpoints and one strict full-face graph derivative.
2. `STRICT_MONOTONE_ACTIVE_FACTOR_ABSENT`: no bracketed endpoint, one strict
   full-face graph derivative, and the two graph-axis endpoint edges have
   the same strict whole-edge C0 sign, agreeing with all four corners.

The second form is important: a preliminary curve-only development run
classified `32` zero-free faces as residual merely because they had zero
boundary endpoints. That overly narrow classification was discarded. No
probe criterion was weakened; the final absence form adds a strict monotone
whole-face zero-exclusion proof.

The final run used:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=191052 \
  /usr/bin/time -v -o /tmp/cm2_round191_seed191052.time \
  ../.venv-neurips/bin/python -B \
  cm2_round191_source_g_stereographic_endpoint_chart_probe.py \
  > /tmp/cm2_round191_seed191052.json \
  2> /tmp/cm2_round191_seed191052.stderr
```

The script has no output-path option. A synthetic `--output` attempt exited
`2` and created no file.

## Evidence

The final run exited zero:

- elapsed: `3:07.01`;
- maximum RSS: `671,076 KiB`;
- probe result SHA256:
  `2960b6cc90981f8f53f490fecb1b990a882140e4165f6041d2809d9f46793399`;
- output JSON SHA256:
  `8e696da8610e8949e7f1ccb7cff6bc6961993d6e13303c2fcec92854c4c53003`;
- compact 288-row evidence SHA256:
  `3678ef705be6fd7afb43c7f44b44a277fbd7641a6ca41c7321ad2f74a95f8cb6`.

Independent canonical re-hashing reproduced the embedded probe-result
digest.

The exact endpoint cohort was reconstructed:

| item | count |
|---|---:|
| endpoint faces | 288 |
| distinct leaves | 288 |
| distinct origins | 8 |
| `p=-1` faces | 144 |
| `p=+1` faces | 144 |
| endpoint faces on U\|U leaves | 0 |

The pinned Round189 depth-2 result was also rebuilt exactly:

- verdict: `PARTIAL`;
- original faces: `288 = 32 resolved + 256 residual`;
- exact area:
  `1/655360 = 1/819200 + 1/3276800`;
- refinement-result SHA256:
  `52ad352756cd5a9dcdd800142145d771c01a5db5e7c5b9ac634c8e2e694f2b0f`;
- audit-row SHA256:
  `a3e3c264699820d08d0e406b2692987a5c41aebc8a804ef9d7c3029526c99550`.

The stereographic chart closes the complete 288-face cohort:

| final face normal form | count |
|---|---:|
| unique two-endpoint factor curve | 256 |
| strict-monotone active factor absent | 32 |
| residual | 0 |

All `288` faces select `u` as a strict graph axis. The full-face derivative
sign pairs are balanced:

| `(du,ds)` sign pair | count |
|---|---:|
| `(strict negative, strict negative)` | 144 |
| `(strict positive, strict negative)` | 144 |

The active factor is also balanced:

| active factor | count |
|---|---:|
| `HPLUS` | 144 |
| `HMINUS` | 144 |

The complete edge census is:

| edge evidence | count |
|---|---:|
| E strict C0 zero absent | 288 |
| W strict C0 zero absent | 288 |
| N unique bracketed zero | 256 |
| S unique bracketed zero | 256 |
| N strict C0 zero absent | 32 |
| S strict C0 zero absent | 32 |

Thus the `256` curve faces all have endpoint pair `N|S`. The remaining `32`
faces have all four edges strictly zero-free; their W/E graph-axis endpoint
edges have one common strict sign, and strict `du` transports that
zero-exclusion across the full face.

All four endpoint-chart boundary labels are explicit: W is `u=0`
(`p=sigma`), E is `u=u_max` (`p=p_inner`), and S/N are the exact s endpoints.
There are no artificial p-split edges in this probe. Formal half-open
ownership of shared arrangement edges is deliberately not materialized.

## Verdict

`VALIDATED`: the rational stereographic chart is a complete finite
face-level replacement for continued p bisection on all `288` Round188
endpoint faces. It yields `256` unique two-endpoint factor curves and `32`
strict-monotone active-factor absences, with no face residual.

The result is narrower than a source-G gate closure. It does not yet:

- materialize the 288 evidence rows as a formal attachment;
- combine them with the other Round188 factor-face rows;
- assign half-open boundary ownership or side-specific return signatures;
- solve cross-t ordering/glue for the separate `88` U\|U leaves;
- process the separate `64` wall-G residual leaves; or
- provide a producer/certificate/independent-verifier package.

## Promotion boundary

This spike remains diagnostic:

- whole-leaf credit: `0`;
- source-G global dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- CM2: `NO-GO_FOR_CLAIM`.

The next production step is a formal factorized clipped-face certificate
that incorporates the Round188 atlas plus these two endpoint normal forms,
then adds exact half-open ownership, side-specific signatures, U\|U ordering,
the wall-G tail, full dimensional ledgers, and an independent verifier that
does not import or execute its producer.
