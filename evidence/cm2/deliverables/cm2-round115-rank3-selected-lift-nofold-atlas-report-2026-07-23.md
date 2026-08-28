# CM2 Round 115 — selected-lift no-fold atlas

Date: 2026-07-23  
Verdict: **VERIFIED selected-lift no-fold atlas on 8/8 traces; physical-owner, reach, and collar gates remain open.**

## What Round115 pays

Round114 supplied continuous image coverage of each shared grazing root edge,
but did not prove that its projective coordinate was one-to-one.  Round115
closes exactly that gap.

For each of the eight edges, write

```text
F(t,c0) = Delta3(t,c0) = 0,       0 <= c0 <= 1/16384.
```

A correlated affine coordinate

```text
t = t_ref + a(c0-1/32768) + e
```

is installed with `|e| <= 3e-8`.  On every full parameter tube, `F_e` has a
fixed sign and absolute value greater than `7`.  Directed mean-form bounds on
the two `e` faces have opposite signs and margins greater than `1e-9`.
Consequently each `c0` has one and only one root in the tube.

The corner derivative is handled separately and exactly.  With
counterclockwise `J(x,y)=(-y,x)`, the source convention is

```text
v = c0 n + p0 Jn,        p0(0)=sigma0,
n_t = epsilon Jn/s,      s=sqrt(1-t^2).
```

For `lambda=epsilon sigma0 s`, the source phase-state derivative is

```text
D(x,v) = (R0 v, 0).
```

This is only a free-flight shift along the same ray.  It leaves the first hit,
all later selected collisions, `Delta3`, and the outgoing projective `q`
unchanged.  Since `F_t` is nonzero, the implicit root therefore satisfies

```text
t'(0)=lambda,       q'(0)=0.
```

Thus Round115 does **not** claim that `q'` avoids zero on the closed edge.

On the positive interior, the verifier evaluates the full implicit second
derivative

```text
e'  = -F_c/F_e,
e'' = -(F_cc + 2 F_ce e' + F_ee (e')^2)/F_e,
q'' = q_cc + 2 q_ce e' + q_ee (e')^2 + q_e e''.
```

The first six edges use 512 dyadic leaves each; the last two use 2048 each,
for 7168 independently replayed leaves.  Every leaf has one fixed `q''` sign
and

```text
|q''| > 1/1000.
```

Integrating from the stationary corner gives, for every `c0>0`,

```text
sign(q') = sign(q''),       |q'(c0)/c0| > 1/1000.
```

The sign is opposite the oriented Round114 projective parameter direction on
all eight edges.  The root-edge image therefore enters the pre-root chain in
the correct direction, and the overlap crosswalk is unique.  Together with
the inherited `q`-parametrized base chain and Cartesian seam bridge, this pays
the **selected-lift whole-trace no-fold atlas on 8/8 traces**.

Round115 also installs conservative root-graph bounds

```text
|dt/dc0| < 2,       |d2t/dc0^2| < 10,
root-graph parameter-plane curvature < 10,
|q''| < 10.
```

These are local `C2`/curvature bounds, not a reach theorem.

## What remains open

- physical first/second/third owner closure: **0/8**;
- positive normal reach for the whole physical trace: **0/8**;
- uniform distance from every other collision singularity, corner, cap, and
  representation seam: **0/8**;
- two-sided physical collar: **0/8**;
- complete 57-candidate collar ordering: **0/8**;
- new actual-child Gate5 fields: **0**.

Injectivity of one selected-lift coordinate and bounded local curvature do not
give a quantitative nonlocal self-separation bound.  They also do not compare
the trace with every other singularity.  HIT and BYPASS remain separate real
sheets sharing only `c3=b3=0`.

## Independent verification

- producer precision: **640 bits**;
- independent verifier precision: **896 bits**;
- Round115 producer imported by verifier: **false**;
- correlated root tubes replayed: **8/8**;
- exact flow-shift corner lemmas plus high-precision derivative checks:
  **8/8**;
- implicit `q''` leaves replayed: **7168/7168**;
- monotone root-edge/base-chain crosswalks replayed: **8/8**;
- semantic/schema/strict-JSON attacks rejected: **20/20**.

CM2 remains **`NO-GO_FOR_CLAIM`**.
