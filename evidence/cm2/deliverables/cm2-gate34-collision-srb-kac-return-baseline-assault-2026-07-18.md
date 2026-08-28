# CM2 Gate 3/4 collision-SRB Kac return baseline assault — 2026-07-18

## Frozen result

For every fixed parameter `|s|<=1/400`, let `mu_s` be the normalized
collision-SRB probability on the usual solid collision section and let
`C_s` be the union of the 24 frozen compact physical cores.  The existing
registry proves the strict uniform mass bound

```text
mu_s(C_s) > 147/550000.
```

Poincare recurrence and the general Kac formula can therefore be applied
directly, without an ergodicity assumption.  With

```text
tau_C_s^+(x) = inf{n>=1 : T_s^n(x) in C_s},
```

the following aggregate collision-SRB statements are now frozen:

```text
mu_C_s{tau_C_s^+<infinity} = 1,
sum_{n>=1} mu_s(C_s intersection {tau_C_s^+=n}) = mu_s(C_s),
integral_C_s tau_C_s^+ dmu_s = mu_s(saturation_T_s(C_s)) <= 1,
E_mu_C_s[tau_C_s^+] < 550000/147.
```

Here `mu_C_s=mu_s(. intersection C_s)/mu_s(C_s)`.  Numerically,
`550000/147 = 3741.496598639456...`.  The singular orbit cemetery is a
countable union of grazing/corner preimages and has collision-SRB mass zero;
the nonreturning part of `C_s` is also null.

The tail-sum identity gives the exact unweighted first-moment control

```text
sum_{n>=0} mu_C_s{tau_C_s^+>n}
  = E_mu_C_s[tau_C_s^+]
  < 550000/147.
```

For each integer `n>=0`, Markov's inequality additionally gives

```text
mu_C_s{tau_C_s^+>n}
  <= E_mu_C_s[tau_C_s^+]/(n+1)
  < 550000/(147(n+1)).
```

The probability cap is still the only useful displayed bound at horizon
2018.  The first nontrivial integer sample frozen by the certificate is

```text
mu_C_s{tau_C_s^+>3741} < 275000/275037,
```

and at the longer existing horizon,

```text
mu_C_s{tau_C_s^+>12108} < 550000/1780023
                              = 0.3089847715450868....
```

The pointwise `1/(n+1)` envelope is coarse and is not an exponential tail.
The separately frozen tail-sum identity is nevertheless a genuine finite
aggregate collision-SRB `L1` first-moment statement.

## Measurable induced baseline

The first-return map

```text
T_C_s(x) = T_s^(tau_C_s^+(x))(x)
```

is defined `mu_C_s`-almost everywhere and preserves `mu_C_s`.  Its measurable
Perron operator is positive, preserves integrals, and has `L1(mu_C_s)`
operator norm exactly one.  This closes the measure-theoretic induced-map
baseline only.

It is not the branch-materialized CM2 induced operator: no connected return
partition, collision words, intermediate complement guards, Jacobian or
distortion rows, `m_n/q_n` payloads, common forward/reverse restriction IDs,
or three-strong-norm estimates are supplied by Kac's theorem.

## Dependency binding

The producer fail-closes on five frozen interfaces:

- the 24-core registry and its strict normalized mass lower bound;
- the fixed-parameter solid billiard map on `|s|<=1/400`;
- the common invariant normalized `cos(phi) dr dphi = dr dp` probability;
- full regular collision-step coverage modulo the singular null set;
- the Round-23 warning that four equal labelled coordinate boxes are not a
  collision-SRB probability sample and do not form the full induced operator.

The Kac identity used here is the general formula

```text
integral_C tau_C^+ dmu = mu(saturation_T(C)),
```

so no unbound claim that `C_s` has full ergodic saturation is required.  In
particular, the certificate records `<=1`, not the stronger equality `=1`.

## Strict nonpromotion

The following remain `NOT_CERTIFIED`:

- materialized `R_n=M_C L(M_{C^c}L)^(n-1)M_C` and
  `Q_n=(M_{C^c}L)^nM_C` branch rows;
- a connected collision-SRB first-return partition with raw margins;
- branchwise Jacobian, distortion, mass `m_n`, and strong charge `q_n`;
- a `q`-weighted exponential excursion/cemetery tail;
- a common two-view strong space and induced Lasota–Yorke coefficient;
- complete 18-field physical operator blocks and Gates 3, 4, and 5.

Thus this leaf removes the aggregate unweighted mass-conservation and finite
first-moment ambiguity, but it does not close the remaining strong CM2 gate.

## Frozen artifacts and replay

- `cm2_gate34_collision_srb_kac_return_baseline_cert.py`
- `cm2_gate34_collision_srb_kac_return_baseline_verifier.py`
- `cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.json`
- this report
- `cm2-gate34-collision-srb-kac-return-baseline-manifest-2026-07-18.sha256`

Verification modes:

```text
--integrity-only  PASS
--replay          PASS
--self-test       PASS (55/55 hostile mutations rejected)
live mode         exit 2 by design
```
