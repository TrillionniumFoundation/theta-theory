# CM2 Gate 4/5 round 35: physical Rn rank-sum Lp tail

Date: 2026-07-19  
Status: **a physical first-return L^(6/5) envelope and exponential tail are certified for the additive D1 incidence-rank charge only**

## Physical incidence rank

In collision coordinates `p=sin(phi)` and `cp=sqrt(1-p^2)`, define

```text
B_inc(x)=max(14,
             ceil(log2(1/cp(x))),
             ceil(log2(1/cp(T_s x)))).
```

Because `mu_s` is normalized `dr dp`, for every integer `b>=14`,

```text
mu_s{cp<2^-b}=1-sqrt(1-4^-b)<4^-b.
```

Invariance and the source/target union bound yield

```text
mu_s{B_inc>b}<2*4^-b.
```

With `a=2^(3/2)`, layer-cake summation and

```text
a^14=2^21,
a-1<2,
(a/4)^14=1/128,
sum_(b>=14)(a/4)^b<7/256
```

give the direct physical collision-SRB moment

```text
integral 2^(3 B_inc/2) dmu_s < 134217735/64.
```

This bypasses the round-34 endpoint-coarea measure mismatch.

## Additive D1 charge on Rn

For a regular point of `R_n`, set

```text
B_i(x)=B_inc(T_s^(i-1)x),
c_D1,n(x)=151 sum_(i=1)^n 2^B_i(x).
```

On each physical first-return component `R_n,k`, define

```text
q_D1,n,k = integral_(R_n,k) c_D1,n dmu_s.
```

This is charged once on the shared fw/rev restriction.  Jensen converts the
pointwise moment into the component-mean `q/m` moment required by the
round-28 global `L^p` transfer theorem.

## Global L^(6/5) moment

Take `p=6/5`, `q0=3/2`, so `p/q0=4/5`.  Write

```text
A = 550000/147,
epsilon = 21/111718750,
r = 1-epsilon = 111718729/111718750,
M_rank = 134217735/64.
```

Hölder on `R_n subset Q_(n-1)`, followed by the certified survivor bound,
gives

```text
integral_(R_n) c_D1,n^(6/5) dnu_s
  < 22801 A M_rank n^2 r^(floor((n-1)/N_open)/5),
```

where `dnu_s=dmu_s/mu_s(C_s)`.  Grouping return times by
`b=floor((n-1)/N_open)` uses

```text
sum_block n^2 <= N_open^3 (b+1)^2,
h=r^(1/5)<=1-epsilon/5,
sum_(b>=0)(b+1)^2 h^b=(1+h)/(1-h)^3<250/epsilon^3.
```

Therefore

```text
sum_(n,k) mbar_n,k cbar_D1,n,k^(6/5) < K_rank N_open^3,

K_rank =
3055930500533353804145008325576782226562500/453789.
```

`N_open` is uniform and finite but theorem-supplied rather than numerical.

## Weighted-tail consequence

The global `L^p` transfer theorem now gives

```text
Wbar_D1(n)
  < (K_rank N_open^3)^(5/6) A^(1/6)
    r^(floor(n/N_open)/6).
```

This is a physical first-return exponential weighted tail for the additive
incidence-rank channel.  It is not the full branch pullback cost, does not
dominate complete `C_fw,C_rev`, and is not the final same-ID `q` or cemetery
tail.

## Evidence and replay

- `deliverables/cm2_gate45_round35_physical_rn_rank_sum_lp_cert.py`
- `deliverables/cm2_gate45_round35_physical_rn_rank_sum_lp_verifier.py`
- `deliverables/cm2-gate45-round35-physical-rn-rank-sum-lp-manifest-2026-07-19.json`

Using `.venv-neurips/bin/python`:

```text
independent replay:               AUDIT_MODE: PASS
self-test:                        HOSTILE_MUTATIONS_REJECTED: 17/17
default live mode:                exits 2
```

