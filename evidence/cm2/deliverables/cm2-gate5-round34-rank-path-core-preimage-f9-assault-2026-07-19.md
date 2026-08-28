# CM2 Gate 5 round 34: rank-path core-preimage F9

Date: 2026-07-19  
Status: **two arbitrary-time core-face kinds receive a strict rank-path F9 template; Gate 5 remains open**

## Verdict

The 96 stationary C24 boundary faces admit affine Birkhoff level functions.
On every finite regular homogeneous rank path, their intermediate and terminal
preimages therefore receive an explicit finite unit-speed `C2` bound.  This
advances the five-kind F9 matrix from one to three certified kinds, but it is
not a complete instantiated face atlas and gives no global Gate-5 field credit.

```text
source core clipping F9:                         CERTIFIED, value 0
intermediate core-preimage F9:                   CERTIFIED rank-path template
terminal core-preimage F9:                       CERTIFIED rank-path template
owner-change / collision-singularity F9:         NOT CERTIFIED
moving-occurrence physical-face F9:              NOT CERTIFIED
complete physical F9 atlas:                      NOT CERTIFIED
Gate-5 maturity:                                 6/18 unchanged
CM2:                                             NO-GO FOR CLAIM
```

## Affine core-face representation

Each frozen core boundary is either `t=constant` or `p=constant`.  On its
fixed collision chart, `t` is monotone in boundary arclength and the core is
central with `|p|<3/10`.  Hence the same geometric face can be represented by
one of the affine Birkhoff equations

```text
r-r_edge=0,                 phi-arcsin(p_edge)=0.
```

The level gradient has coordinate `l1` norm one and the base Hessian is zero.
No derivative of the auxiliary `(t,p)` coordinates is inserted into the
pullback estimate.

## Exact arbitrary-time recurrence

On a regular homogeneous collision step choose an incidence rank `B>=14`
which dominates both inverse incidence cosines.  The frozen one-step bounds
give

```text
L(B) = 150*2^B,                 ||DT||_infinity, ||DT^-1||_infinity < L(B),
M(B) = 42672*2^(3B),            ||D2T||_infinity < M(B).
```

For a rank path `(B_1,...,B_j)`, set

```text
D_0=E_0=1, H_0=0,
D_i=L(B_i)D_(i-1),
E_i=L(B_i)E_(i-1),
H_i=M(B_i)D_(i-1)^2+L(B_i)H_(i-1).
```

For `F_j=e_coordinate o T_s^j-c`, duality and the inverse derivative give

```text
||dF_j||_1 > 1/E_j,
||dF_j||_2 > 1/(sqrt(2)E_j),
||D2F_j||_2 < H_j.
```

Thus every regular connected level component has a unit-speed chart with

```text
|gamma''| = curvature(F_j=0)
          < sqrt(2) E_j H_j
          < (3/2) E_j H_j.
```

The certificate checks the recurrence against its independently expanded
composition sum and freezes sample paths through depth four.  The constants
are intentionally crude and grow rapidly; finiteness on each finite rank path
does not imply a depth/rank-uniform bound.

## Strict typing boundary

This leaf does not price or instantiate all arbitrary-depth components.  It
also does not cover collision singularities, owner changes, or the physical
moving-occurrence faces.  In particular, the carrier-curvature constant
`4949` is still not retyped as physical-face F9.  F10 is unchanged from round
33: zero on stationary source faces and parameterized only on 64 occurrence
seeds.

## Evidence and replay

- `deliverables/cm2_gate5_round34_rank_path_core_preimage_f9_cert.py`
- `deliverables/cm2_gate5_round34_rank_path_core_preimage_f9_verifier.py`
- `deliverables/cm2-gate5-round34-rank-path-core-preimage-f9-manifest-2026-07-19.json`

Using `.venv-neurips/bin/python`:

```text
--integrity-only:                 AUDIT_MODE: PASS
--replay:                         AUDIT_MODE: PASS
--self-test:                      HOSTILE_MUTATIONS_REJECTED: 14/14
default live mode:                exits 2
```

