# CM2 Gate 4/5 round 34: corrected weighted-tail interface refresh

Date: 2026-07-19  
Status: **the recovered-cone hit lower is already certified; the physical strong-q tail remains open**

## Corrected baseline

Round 33 incorrectly described the recovered-cone C24 hit lower as missing.
The frozen 2026-07-18 sparse-hit certificate already proves, uniformly over
`|s|<=1/400`,

```text
epsilon_hit = 21/111718750,
r           = 111718729/111718750 < 1,
P_(mu_C24,s)(tau_C24^+>n)
  < (550000/147) r^floor(n/N_open),
```

where `N_open>=1` is one uniform theorem-supplied, nonnumeric integer.  The
correction is append-only; no frozen round-33 artifact was rewritten.  The
certified tail is unweighted.  It does not imply the strong `q` excursion or
cemetery tail.

## Six-interface refresh

| # | strong first-return interface | round-34 state |
|---:|---|---|
| 1 | positive-mass fixed-`s` `R_n` rows | partial: 4,216 finite R1 anchors only |
| 2 | actual recuts + common fw/rev carrier | actual parameterized recuts certified; common carrier absent |
| 3 | numeric `C_fw,C_rev,c=q/m` | zero rows |
| 4 | physical first-return `L^p` envelope | zero; one-collision coarea seed only |
| 5 | strong singular/cemetery charge | zero |
| 6 | induced F14--F18 common block | not certified |

Thus the first true tail blocker is no longer a cone hit estimate.  It is the
same-ID common standard-family recovery carrier and numerical physical
`c=q/m` rows.

## Current F7--F10 state

Round 31 supplies actual parameterized parent-W and recut-instance IDs.  Round
32 supplies numeric Q2 F7 slots on all 228,012 base rules with coefficient
`360134800/360493663<1`, plus the common F8 lower `1/5`.  Round 33 supplies
zero F9/F10 on 96 stationary source faces and seed-level F10 on 64 moving
occurrences.  The companion round-34 leaf adds a rank-path F9 template for
intermediate and terminal core preimages.  Still missing are arbitrary-depth
same-ID Rn F7 charges, owner/singularity and moving-occurrence F9, and all
non-seed F10 rows.

Global Gate-5 maturity remains `6/18` because templates without a complete
same-ID limiting component and operator assembly do not earn a global field.

## Explicit one-collision `L^(3/2)` seed

The endpoint-rank ledger has

```text
m_e{B>b} <= (9158592/6875) 4^-b,       b>=14,
m_e(total) <= 8064/5,
c_e^(1)=151*2^B.
```

For `a=2^(3/2)`, use `a^14=2^21`, `a-1<2`,
`a/4=1/sqrt(2)<5/7`, and `(a/4)^14=1/128`.  Exact summation gives

```text
integral 2^(3B/2) dm_e < 46506443753721/13750,
integral (151*2^B)^(3/2) dm_e
  < 91292149088554323/13750.
```

This is a genuine finite one-collision endpoint-coarea moment.  It is not on
the normalized fixed-`s` physical first-return component mass ledger, so it
does not instantiate the conditional weighted-tail transfer theorem.

## Latest technology audit

Official arXiv pages were rechecked on 2026-07-19:

- `2604.19671v2` proves small boundary-hole response using the special
  long-standard-pair foliation geometry of the hole image; it does not supply
  the C24 phase-rectangle branchwise `q`, cemetery, or F14--F18 rows.
- `2606.10155v1` is the current transfer-operator/cone review and blueprint,
  but contains no CM2-specific same-ID numerical payload.
- `2104.06947v3` is already the theorem source behind the certified sparse
  hit and unweighted tail; it does not itself close the induced strong tail.

No external theorem was promoted.

## Evidence and replay

- `deliverables/cm2_gate45_round34_weighted_tail_interface_refresh_cert.py`
- `deliverables/cm2_gate45_round34_weighted_tail_interface_refresh_verifier.py`
- `deliverables/cm2-gate45-round34-weighted-tail-interface-refresh-manifest-2026-07-19.json`

Using `.venv-neurips/bin/python`:

```text
--integrity-only:                 AUDIT_MODE: PASS
--replay:                         AUDIT_MODE: PASS
--self-test:                      HOSTILE_MUTATIONS_REJECTED: 17/17
default live mode:                exits 2
```
