# CM2 Gate 5 round 37: global F10 summability obstruction

Date: 2026-07-19  
Status: **pointwise compact-germ F10 remains certified, but it cannot be
promoted to a global weighted field without a new physical tail**

## Exact countermodel

For `k>=1`, assign one compact analytic affine face germ

```text
G_k(x,s)=x-(2^k-1/2)s
```

with physical face mass `m_k=2^-k`.  Every germ has

```text
F8=1,
F9=0,
rho_k=2^k-1/2,
d_tau rho_k=d_s rho_k=0,
N_F10(k)=2^k.
```

The total face mass is one and every F10 integer is finite.  Nevertheless,

```text
m_k N_F10(k)=1,
sum_(k=1)^K m_k N_F10(k)=K,
sum_k m_k N_F10(k)=infinity.
```

Thus countability, analytic compactness, perfect F8/F9 data, and pointwise
finite F10 do not imply a global physical `L1` or weighted sum.  The model is
a logical non-implication, not a physical billiard face law.

## Required quantitative input

Any one of the following would be sufficient to escape this obstruction:

- a uniform `sup_g N_F10(g)<infinity`;
- a physical face `L^p`, `p>1`, bound on `N_F10`;
- a summable shell ledger
  `sum_l 2^l mu_face{2^(l-1)<N_F10<=2^l}<infinity`;
- an explicit summable coupling between analytic margins, incidence rank,
  rank-path derivative products, and physical face mass.

Round 35's D1 estimate is additive in one-time incidence ranks.  It does not
dominate arbitrary rank-path products or vanishing analytic margins, so it
cannot fill this interface.

## Downstream boundary

F12 remains candidate-local at one-step R1 and is not return-wide on arbitrary
`R_n`.  F13 still has no global moving-current/two-trace join on the common
physical IDs.  Consequently dynamic `MT_DQ`, F14--F18 and the induced
coefficient remain open.

```text
GLOBAL WEIGHTED F10:                    NOT CERTIFIED
RETURN-WIDE F12 / MOVING F13:           NOT CERTIFIED
DYNAMIC MT_DQ / F14--F18:               NOT CERTIFIED
COMPLETE 18-FIELD BLOCKS:               0
GATE 5 MATURITY:                        7/18 UNCHANGED
CM2:                                    NO-GO FOR CLAIM
```

## Evidence

- `deliverables/cm2_gate5_round37_f10_summability_obstruction_cert.py`
- `deliverables/cm2_gate5_round37_f10_summability_obstruction_verifier.py`
- `deliverables/cm2-gate5-round37-f10-summability-obstruction-manifest-2026-07-19.json`

Syntax, dependency integrity, replay and live fail-close pass.  The verifier
rejects `17/17` hostile mutations.
