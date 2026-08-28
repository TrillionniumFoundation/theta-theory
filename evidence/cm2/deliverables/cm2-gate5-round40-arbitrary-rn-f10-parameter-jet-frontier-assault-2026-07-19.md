# CM2 Gate 5 round 40: arbitrary-Rn F10 mixed-parameter-jet frontier

Date: 2026-07-19  
Status: **the full second-order chain rule for arbitrary finite pullbacks is
now frozen and replayable; physical rank-indexed mixed jets and their joint
path moment remain missing**

## 1. Why seed F10 does not automatically pull back

Round 39 certifies on 64 moving-occurrence seeds and 128 oriented traces

```text
alpha=2, r=1, p=3/2,
physical raw-coarea L^(3/2) F10 < infinity.
```

For an arbitrary finite branch

```text
x_i=T_i(x_(i-1),s),
```

Round 36 supplies only the spatial one-step envelopes

```text
A_i=||D_x T_i|| <= 150*2^B_i,
B_i=||D_x^2 T_i|| <= 42672*2^(3B_i).
```

F10 differentiates the coarea density in the parameter.  It therefore also
requires

```text
U_i=||partial_s T_i||,
V_i=||D_x partial_s T_i||,
W_i=||partial_s^2 T_i||.
```

No physical rank-indexed `U(B),V(B),W(B)` table currently exists in the
arbitrary-`R_n` registry.

## 2. Exact arbitrary-path recurrence

For the prefix map `X_i`, set

```text
D_i=||D_x X_i||,
H_i=||D_x^2 X_i||,
P_i=||partial_s X_i||,
Q_i=||D_x partial_s X_i||,
S_i=||partial_s^2 X_i||.
```

With `D_0=1` and `H_0=P_0=Q_0=S_0=0`, the second-order chain rule gives

```text
D_i <= A_i D_(i-1),
H_i <= B_i D_(i-1)^2 + A_i H_(i-1),
P_i <= U_i + A_i P_(i-1),
Q_i <= V_i D_(i-1) + B_i P_(i-1)D_(i-1) + A_i Q_(i-1),
S_i <= W_i + 2V_iP_(i-1) + B_iP_(i-1)^2 + A_iS_(i-1).
```

This recurrence is finite for every fixed finite analytic path with finite
step jets.  Three exact integer test paths, including `(14,16,18)`, are
materialized under a clearly labeled synthetic `U/V/W` policy and replayed
independently.  Those synthetic numbers are algebra tests, not physical
bounds.

## 3. Exact F10 derivative interface

For a pulled-back face level

```text
F(x,s)=G(X_j(x,s),s),
```

the required derivatives include

```text
F_x  =(D_xX_j)^T G_x,
F_s  =G_s+G_x dot P_j,
F_xs =Q_j^T G_x+(D_xX_j)^T(G_xs+G_xx P_j),
F_ss =G_ss+2G_xs dot P_j+P_j^T G_xx P_j+G_x dot S_j.
```

Together with `F_xx`, these feed `rho`, `d_tau rho`, and `d_s rho`.  Hence
the all-face base levels also need numeric `G_s,G_xs,G_ss` envelopes.

The previous compact-germ result remains constructive: every fixed compact
regular analytic germ has a positive parameter radius and a terminating
interval search.  The new recurrence can be evaluated inside each such
germ.  This is not a global `L^p` theorem because no uniform joint
spacetime atlas, margin tail, or physical path moment is installed.

## 4. Exact first missing payload

The shortest arbitrary-`R_n` F10 installation now has four explicit inputs:

1. physical one-step rank envelopes `U(B),V(B),W(B)` on identical branch IDs;
2. all-five-face base parameter jets `G_s,G_xs,G_ss`;
3. a joint spacetime component-persistence and denominator-margin tail;
4. a same-law physical path moment for the nonlinear `D/H/P/Q/S` recurrence.

The endpoint seed tail alone cannot supply item 4: pullback cost depends on
the whole rank word and mixed jets, not only the terminal seed rank.  Atlas
failures, simultaneous roots, grazing endpoints, vanishing wedges and branch
loss must feed the independent strong cemetery.

## 5. Strict boundary

```text
ARBITRARY-PATH MIXED-JET RECURRENCE: CERTIFIED
COMPACT-GERM CONSTRUCTIVE F10:       CERTIFIED
PHYSICAL RANK U/V/W:                 NOT CERTIFIED
ARBITRARY-R_n PULLBACK F10:          NOT CERTIFIED
COMPLETE ALL-FACE F10:               NOT CERTIFIED
F12 / F13 / STRONG CEMETERY:         NOT CERTIFIED
F14--F18 / COMPLETE BLOCKS:          NOT CERTIFIED / 0
GATE-5 MATURITY:                     7/18 UNCHANGED
CM2:                                 NO-GO
```

## Evidence

- `deliverables/cm2_gate5_round40_arbitrary_rn_f10_parameter_jet_frontier_cert.py`
- `deliverables/cm2_gate5_round40_arbitrary_rn_f10_parameter_jet_frontier_verifier.py`
- `deliverables/cm2-gate5-round40-arbitrary-rn-f10-parameter-jet-frontier-manifest-2026-07-19.json`

Syntax, frozen dependency hashes, strict JSON, independent integer replay and
live fail-close pass.  The verifier rejects `24/24` hostile mutations.
