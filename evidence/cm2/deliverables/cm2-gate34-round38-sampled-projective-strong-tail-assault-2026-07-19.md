# CM2 Gates 3/4 round 38: sampled projective strong tail

Date: 2026-07-19  
Status: **the scheduled C24 killed operator has a qualitative strong
exponential tail in the Demers--Liverani projective order norm, but no
standard-family `Z` tail or all-collision `Q_n` bridge is certified**

## 1. Strong upgrade on the scheduled skeleton

The frozen sparse-opening block has one uniform theorem-supplied length
`N_open` and exact per-block survival factor

```text
r=111718729/111718750<1.
```

For every fixed `|s|<=1/400`, Proposition 8.7 of
Demers--Liverani (`arXiv:2104.06947v3`) sends every normalized block output
into a strict subcone

```text
C_chi=C_{chi*c,chi*A,chi*L}(delta).
```

Proposition 6.13 gives this strict subcone finite Hilbert diameter
`Delta_open` inside the base cone `C=C_{c,A,L}(delta)`.  With the order norm
of Definition 8.14,

```text
||f||_*=inf{lambda>=0:-lambda<=_C f<=_C lambda},
```

take a normalized output `h` and the constant density `1`.  Equal mass gives
`alpha(h,1)<=1<=beta(h,1)`, while finite projective diameter gives
`beta/alpha<=exp(Delta_open)`.  Therefore

```text
exp(-Delta_open)<=alpha<=1<=beta<=exp(Delta_open),
||h||_*<=K_cone:=exp(Delta_open)<infinity.
```

Combining this with the exact round-34 hit gap yields, for every `k>=1`,

```text
||K_s^k f||_*<K_cone*r^k*mass(f),
K_s f=L_s^N_open(1_{C24^c}f).
```

This is a genuine strong survivor tail, in the paper's projective-cone order
norm rather than only collision-SRB mass.

## 2. Exact weighted resolvent

Choose

```text
w=223437479/223437458>1.
```

Then exact rational arithmetic gives

```text
w*r=223437479/223437500<1,
1-w*r=21/223437500.
```

Hence the scheduled strong Green sum obeys the safe qualitative bound

```text
sum_{k>=1} w^k ||K_s^k f||_*
 < K_cone*(223437500/21)*mass(f).
```

The exponential rate and resolvent multiplier are explicit.  The block
length `N_open`, Hilbert diameter `Delta_open`, and `K_cone` remain
theorem-supplied rather than numeric.

## 3. Why this is not the required standard-family Z

The projective cone is a density-level object.  The standard-family Growth
functional depends on the chosen disintegration.  The exact unit-square
model makes the mismatch unavoidable:

- disintegrate density `1` into full horizontal leaves of length `1`; then
  `Z=1`;
- split every horizontal leaf into `k` equal pieces, assign each normalized
  piece weight `1/k`, and obtain the same density but `Z=k`.

The density, projective cone element, projective norm, and physical mass are
identical for every `k`, while representation-dependent `Z` is unbounded.
Thus the new order-norm tail cannot be promoted to the canonical
standard-family `Z` ledger without an explicit same-ID comparison theorem.

The round-35 arbitrary-`R_n` parent-`W` registry supplies a canonical physical
carrier schema, but the sparse projective output is not yet joined to it.

## 4. Strict installation boundary

```text
SCHEDULED C24 PROJECTIVE STRONG TAIL:   CERTIFIED QUALITATIVELY
EXPLICIT BLOCK RATE / RESOLVENT:        CERTIFIED
NUMERIC N_open, Delta_open, K_cone:     NOT CERTIFIED
ALL-COLLISION FULL-Q_N STRONG TAIL:     NOT CERTIFIED
STANDARD-FAMILY Z/GROWTH TAIL:          NOT CERTIFIED
GATE 3 / GATE 4 / CM2:                  NOT CERTIFIED / NO-GO
```

Replacing the frozen first-return construction by the sampled return map is
also not automatic.  It would require a same-phase Kac/inducing equivalence
and transport of the DQ, moving-current, and cemetery ledgers.

The shortest bridge is now either:

1. compare the scheduled projective order norm to canonical same-ID `Z`
   uniformly on survivor outputs; or
2. directly prove a physical full-`Q_N` characteristic multiplier `C_N` with
   `C_N a^N<1`.

## Evidence

- `deliverables/cm2_gate34_round38_sampled_projective_strong_tail_cert.py`
- `deliverables/cm2_gate34_round38_sampled_projective_strong_tail_verifier.py`
- `deliverables/cm2-gate34-round38-sampled-projective-strong-tail-manifest-2026-07-19.json`

Syntax, frozen dependency hashes, strict JSON, exact rational replay and live
fail-close pass.  The verifier rejects `19/19` hostile mutations.
