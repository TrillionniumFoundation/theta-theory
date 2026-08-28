# CM2 Gate-4/5 induced strong-payload frontier assault

Date: 2026-07-18  
Status: append-only strict leaf; no aggregate, root, report history, or memory modified.

## New exact C24 mass upper

The frozen 24-core producer has eight axis rectangles and sixteen diagonal
rectangles, evenly split between source obstacles `G` and `W`.  Their
radius-weighted `dt dp` bases are

\[
A=\frac{13}{156250},\qquad
D=\frac{26}{15625},\qquad
A+D=\frac{273}{156250}.
\]

Since `dr=R dtheta` and

\[
\frac{d\theta}{dt}=\frac1{\sqrt{1-t^2}},
\]

the rational bounds

\[
\frac{d\theta}{dt}<\frac{1001}{1000}
\quad (|t|\le 1/50),
\qquad
\frac{d\theta}{dt}<\frac{1401}{1000}
\quad (|t|\le 7/10)
\]

are certified by the exact squared witnesses

\[
\left(\frac{1001}{1000}\right)^2\left(1-\frac1{50^2}\right)
=\frac{2504000499}{2500000000}>1,
\]

\[
\left(\frac{1401}{1000}\right)^2\left(1-\frac{49}{100}\right)
=\frac{100102851}{100000000}>1.
\]

Thus the unnormalized core mass is strictly below

\[
A\frac{1001}{1000}+D\frac{1401}{1000}
=\frac{377273}{156250000}.
\]

The total collision volume is `4*pi*(R_G+R_W)`.  Using `pi>3` and
`R_G+R_W=13/25` gives the uniform parameterwise interval

\[
\boxed{
\frac{147}{550000}<\mu_s(C_{24})
<\frac{29021}{75000000}<\frac1{2500}
}
\qquad (|s|\le 1/400).
\]

This supplies the previously missing exact normalized core-mass upper.  It is
only a small-measure input; it does not by itself prove the open-hole
`O1'`/`O2`, cone admissibility, recovery, or an exponential escape rate.

## Complete measurable return payload

For every fixed parameter and integer `n>=1`, the certificate freezes

\[
A_{s,n}=C_s\cap\bigcap_{k=1}^{n-1}T_s^{-k}C_s^c
       \cap T_s^{-n}C_s,
\qquad
B_{s,n}=T_s^n(A_{s,n}).
\]

Modulo the singular null set, the `A_{s,n}` and `B_{s,n}` are respectively
the forward- and backward-return partitions of `C_s`.  The same immutable
restriction schema binds

\[
T_s^n|_{A_{s,n}}:A_{s,n}\to B_{s,n}
\quad\text{and}\quad
T_s^{-n}|_{B_{s,n}}:B_{s,n}\to A_{s,n}.
\]

The resulting exact Borel payload is:

- `m_{s,n}=mu_s(A_{s,n})=mu_s(B_{s,n})>=0`;
- `sum_n m_{s,n}=mu_s(C_s)` and `sum_n p_{s,n}=1`;
- singular-orbit cemetery mass `0` and nonreturning mass `0`;
- collision-SRB area Jacobian `1` and log area-Jacobian distortion `0`;
- `sum_n R_{s,n}` is the measurable induced Perron operator on
  `L1(mu_C_s)`, with norm `1`.

The absolute survivor mass has the uniform outer bound

\[
\mu_s(C_s\cap\{\tau_C^+>n\})
\le \min\!\left(\mu_s(C_s),\frac1{n+1}\right).
\]

Nine exact sample rows are frozen.  The rational crossover is recorded at
`n=2584`: before it the new core-mass upper is sharper; from that row onward
the general Kac first-moment bound is sharper.

## Strong payload audit

The measurable payload is deliberately separated from the strong geometric
payload.

On the 24 selected source cores / 28 selected component levels, fields
`F1,F3,F4,F7` remain completed.  The exact existing one-collision seeds are
also retained:

- adapted unstable inverse-Jacobian seed `<144000/180337`;
- Euclidean inverse-Jacobian seed `<27410400/180337`;
- log-Jacobian Holder exponent `1/3` and canonical variation `<3/200000`;
- Borel prefix/suffix TV--Linf constant `1`;
- one-collision C1 and geometric costs `151*2^B_s` and `204*2^B_s`;
- log-Holder constant `52` and initial mesh `69986663973833932800`.

None is attached to a full-dimensional geometric first-return branch.  The
machine registry therefore has:

- geometric connected `R_n` branch rows: `0`;
- numeric exact branch-mass rows: `0`;
- stepwise collision/homogeneity/hidden-recut margin rows: `0`;
- completed induced strong-field slots: `0`;
- complete 18-field induced operator blocks: `0`.

The invariant-area Jacobian `1` is not an unstable-curve Jacobian.  Likewise,
the common Borel restriction schema is not a common fw/rev strong carrier,
and the symbolic `m_{s,n}` are not materialized numeric component masses.

## Thirteen-interface maturity

The earlier all-missing ledger is now split by type.  Eleven of thirteen
interfaces have a nontrivial measurable theorem or one-collision seed:

- complete source partition and complement guards exist modulo null as Borel
  level-set formulas;
- `R_n/Q_n`, symbolic `m_n`, common Borel restriction IDs, singular mass zero,
  survivor outer bounds, and induced `L1` norm one are certified;
- source-local unstable/distortion and one-collision norm seeds are frozen.

But the count of **complete geometric strong interfaces remains `0/13`**.
The two wholly absent payloads are the homogeneity/hidden-recut refinement
and the weighted `q` excursion tail.  Every other row is incomplete at the
geometric strong level.

The next genuinely promotable object must contain full-dimensional connected
`R_n/Q_n` refinement atoms, strict collision and recut margins, numeric
`m_n`, unstable Jacobian and distortion, `q_n`, common strong carriers, and a
weighted exponential tail compatible with the strong loss coefficient.

## Strict verdict

- C24 normalized collision-SRB mass upper: `CERTIFIED`;
- measurable modulo-null first-return payload: `CERTIFIED`;
- common Borel fw/rev restriction schema: `CERTIFIED`;
- full-dimensional geometric `R_n/Q_n` payload: `NOT_CERTIFIED`;
- weighted exponential `q` tail: `NOT_CERTIFIED`;
- induced strong Lasota--Yorke coefficient: `NOT_CERTIFIED`;
- Gate 4: `NOT_CERTIFIED`;
- Gate 5: `NOT_CERTIFIED`.

## Reproduction

Use `.venv-neurips/bin/python` and `PYTHONPATH=deliverables`:

```text
cm2_gate45_induced_strong_payload_frontier_verifier.py --integrity-only
  REPLAY_AND_INTEGRITY: PASS

cm2_gate45_induced_strong_payload_frontier_verifier.py --replay
  REPLAY_AND_INTEGRITY: PASS

cm2_gate45_induced_strong_payload_frontier_verifier.py --self-test
  SELF_TEST: PASS (76/76 mutations rejected)

cm2_gate45_induced_strong_payload_frontier_verifier.py
  exits 2 (strict live non-promotion)
```
