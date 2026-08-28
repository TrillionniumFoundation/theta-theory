# CM2 Gate 5 round 38: F10 margin exponent frontier

Date: 2026-07-19  
Status: **the exact physical exponent inequality needed for global F10 is
frozen, but neither exponent is yet certified on arbitrary-`R_n` same IDs**

## 1. Exact dyadic integrability criterion

Let `eta in (0,1]` be an analytic/singularity margin and suppose

```text
mu{eta<=t} <= C_eta t^alpha,
N_F10 <= A_eta eta^(-r).
```

On the shell `2^(-(k+1))<eta<=2^(-k)`, the mass is at most
`C_eta 2^(-alpha*k)` and the `p`-th power of F10 is at most
`A_eta^p 2^(r*p*(k+1))`.  The shell series has ratio

```text
2^(r*p-alpha).
```

Consequently

```text
r*p<alpha
```

is the strict sufficient condition, with explicit bound

```text
integral N_F10^p dmu
 <= A_eta^p C_eta 2^(r*p)/(1-2^(r*p-alpha)).
```

This criterion is sharp from the two hypotheses alone.

## 2. Critical linear-tail countermodel

Put mass `1/2` at the safe atom `eta=1,N_F10=1`.  For each `k>=1`, put

```text
mass_k=2^(-(k+1)),
eta_k=2^(-k),
N_F10,k=2^k.
```

This probability law satisfies the sharp linear tube estimate

```text
mu{eta<=t}<=t, 0<t<1,
```

and every F10 value is finite.  Yet every shell contributes `1/2` to the
F10 `L^1` sum, so the first `K` shells contribute `K/2` and the global sum
diverges.  This is the critical case `alpha=r=p=1`.

The model is a logical sharpness witness, not a claim that the billiard F10
law actually has inverse-first-power blow-up.

## 3. What the physical tube theorem really gives

Round 26 proves, at one step and after parameter averaging,

```text
mu(U_d)<(50/39)h_d,
h_d=2^(-floor(d/3)).
```

The physical width exponent is therefore `alpha=1` in `h`; `1/3` is the
rate against computational depth `d`, not a margin exponent.  Even under the
optimistic transfer `alpha=1`, an `L^p` target needs

```text
r<1/p.
```

In particular every `p>1` requires a strictly sublinear physical F10
blow-up exponent `r<1`.

The compact-germ theorem currently proves only that each radius and F10
integer is finite.  It gives no margin-to-F10 power `r`.  The tube theorem is
only one-step, while the target requires an arbitrary-`R_n` margin tail and
rank-path product ledger on the same physical face IDs.  The D1 additive
rank tail does not dominate those products.

## 4. Exact next target

```text
derive physical exponents r and alpha on arbitrary-R_n same face IDs,
find p>=1 with r*p<alpha,
and sum the remaining rank-path factors.
```

Until then:

```text
F10 MARGIN INTEGRABILITY CRITERION:     CERTIFIED
PHYSICAL ARBITRARY-R_n r AND alpha:     NOT CERTIFIED
COMPLETE GLOBAL F10:                    NOT CERTIFIED
F12/F13/F14--F18:                       NOT CERTIFIED
GATE-5 MATURITY:                        7/18 UNCHANGED
CM2:                                    NO-GO
```

## Evidence

- `deliverables/cm2_gate5_round38_f10_margin_exponent_frontier_cert.py`
- `deliverables/cm2_gate5_round38_f10_margin_exponent_frontier_verifier.py`
- `deliverables/cm2-gate5-round38-f10-margin-exponent-frontier-manifest-2026-07-19.json`

Syntax, frozen dependency hashes, strict JSON, exact shell replay and live
fail-close pass.  The verifier rejects `20/20` hostile mutations.
