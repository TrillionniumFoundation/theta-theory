# CM2 Round 55 Gate-4 hereditary terminal-`Z` / refinement frontier assault

Date: 2026-07-20  
Strict status: **the every-collision C24-killed Growth theorem now gives a
finite all-time survivor boundary ledger and a finite two-orientation coarse
terminal-`Z` ledger.  This bypasses, but does not prove, the Round-54
`Phi_pair` summability interface.  The physical natural-cell/image-recut
refinement to `J_pair` remains open, so `I_D`, physical `q`, Gate 4, and CM2
remain not certified.**

## 1. Frozen inputs and scope

This append-only leaf pins eight existing manifests: the Round-41/42
hereditary numerical C24 Growth block, the Round-54 same-ID survivor and
terminal extraction, the Round-53 `J_pair -> I_D` bridge, the Round-35 common
carrier and physical rank moment, the Round-50 whole-family grouping, and the
Round-36 correlated-rank separator.  No frozen file is edited.

The new executable artifacts are:

- `cm2_gate34_round55_hereditary_terminal_z_refinement_frontier_cert.py`;
- `cm2_gate34_round55_hereditary_terminal_z_refinement_frontier_verifier.py`;
- `cm2-gate34-round55-hereditary-terminal-z-refinement-frontier-manifest-2026-07-20.json`;
- `cm2-gate34-round55-hereditary-terminal-z-refinement-frontier-manifest-2026-07-20.sha256`.

The parameter scope is uniform for every fixed `|s|<=1/400`.  Nothing below
upgrades the frozen stationary Growth statement to an arbitrary moving
sequence.

## 2. Restore the all-mass one-step estimate

Round 41 correctly distinguishes two operators:

```text
hat_F_(sigma) = closed billiard image with boundary(C_sigma) added as an
                artificial singularity, retaining every descendant;
O_sigma        = delete from hat_F_(sigma) every descendant inside C_sigma.
```

Round 42 records the numerical one-step output only as an `O_sigma` field.
For terminal extraction one must replay the earlier all-mass calculation,
not infer an estimate for the removed pieces from an estimate for the
survivor.

The replay uses

```text
R     = 2000/1999,
B0    = 49,
theta = 900337/901685.
```

The short descendants contribute `R*B0*theta`; equal chopping contributes
`2`.  Thus, before any deletion,

```text
Z(hat_F_sigma G) <= Z1 Z(G),
Z1 = (2000/1999)*49*(900337/901685)+2
   = 18367592526/360493663.
```

Every retained or terminal family is a positive subfamily of this all-mass
family, so deletion can only decrease its unnormalised mass and boundary
numerator.

## 3. Fill every collision residue

Round 42 supplies the numerical killed block

```text
n_*   = 9148,
gamma = (2000/1999)*(1+48*9148)*(900337/901685)^9148 < 1/2.
```

On the common block

```text
L   = 9148*N_open,
g   = gamma^N_open < 1,
rho = (111718729/111718750)^9148 < 1,
```

write `z_p=Z(F_(sigma,pL))`.  The frozen aggregate theorem gives

```text
z_(p+1) <= g z_p + C_N m_base rho^p,
C_N = Z0*(1-g)/(1-gamma) <= Z0/(1-gamma),

sum_p z_p
 <= z_0/(1-g) + C_N*m_base/((1-g)*(1-rho)) < infinity.
```

For `n=pL+j`, `0<=j<L`, the one-step bound and positive-subfamily
monotonicity give

```text
Z(F_(sigma,n)) <= Z1^j z_p.
```

Since the frozen theorem supplies one finite uniform integer `N_open`, the
finite residue multiplier

```text
A_L = sum_(j=0)^(L-1) Z1^j = (Z1^L-1)/(Z1-1)
```

is finite even though it is not numerical.  Therefore

```text
sum_(n>=0) Z(F_(sigma,n)) <= A_L sum_(p>=0)z_p < infinity.
```

The bridge explicitly installs four typings:

1. `F_(fw,0)=mu_s|C_s` is joined to the Round-41 controlled finite-`Z`
   base-cone input through the pinned inner-core characteristic source
   multiplier `2000/1999`.
2. Round 27 identifies `C_s` as the disjoint-mod-faces union of the same 24
   physical cores and its path fibres cover `C24` modulo the singular null
   set; hence the two hole names are joined on the physical carrier.
3. The Round-41/42 killed family and the Round-54 `Q_n` half-open prefix
   owners are the same every-collision complement restriction.
4. The complementary all-mass descendants carry the Round-54 `R_(n+1)`
   terminal IDs.
5. The reverse core is `I(C_s)`.  The frozen unstable cone is
   time-reversal invariant and `I` preserves collision-SRB mass, carrier
   arclength and pulled-back density ratios, hence the standard-family class
   and `Z`; no equality `I(C_s)=C_s` is asserted.

## 4. Coarse terminal pair is now summable

For the exact terminal families,

```text
E_(fw,n+1)  = 1_C_s       hat_F_fw(F_(fw,n)),
E_(rev,n+1) = 1_I(C_s)    hat_F_rev(F_(rev,n)).
```

They are positive subfamilies of the all-mass images, hence

```text
Z(E_(sigma,n+1)) <= Z1 Z(F_(sigma,n)).
```

Summing both orientations gives

```text
Z_term,coarse,pair
 <= Z1 sum_n [Z(F_(fw,n))+Z(F_(rev,n))]
 < infinity.
```

This conclusion does not use the Round-54 closed-step recurrence and does
not use `Phi_pair`.  It therefore removes that forcing ledger from the
shortest route to the coarse terminal result.  It does **not** prove
`sum Phi_pair<infinity` and does not rename the coarse ledger as `J_pair`.

## 5. Why the official gap extension is not a zero-debit join

The official source of arXiv `1210.0011v4` was rechecked byte-for-byte.  On a
gap `V=(x,y)`, the regular extension chooses a point `z` and is constant with
density `rho(x)` on `(x,z)` and `rho(y)` on `(z,y)`.  Splitting at `z` makes
each half constant-density, but the Growth entry uses the whole gap as one
carrier.  No theorem bounds `z` away from either endpoint, so one half may
have arbitrarily small entry length and arbitrarily large boundary `Z`.

Keeping the whole gap avoids this length loss but retains a possible density
jump with ratio `11/9`, whereas the registered numerical cone ratio is only
`2000/1999`:

```text
11/9 > 2000/1999.
```

Thus the candidate `I_density=0` join is rejected.  A uniform cutpoint
position theorem or a new one-jump paired-carrier Growth lemma would be
needed.

Official-source provenance recorded in the manifest:

```text
1210.0011v4 source tar SHA-256:
b705ed4fc89a42ac8e78957d65873211c71f9566599bfba90173812fe5ffe5c5

Moving_final.tex SHA-256:
921fe3477c2f3280a256a459c9e2a2bc6b719a971016a8320e6d0d5e9cd25f44
```

## 6. The exact remaining refinement numerator

Round 53 needs

```text
J_pair = integral sum_c p_c*(ell_fw,c^-1+ell_rev,c^-1) dlambda
```

after the exact natural-short-cell/image-recut subdivision.  For one coarse
terminal record `j`, let `N_(sigma,j)` be its number of final cells.  The
registered density oscillation gives

```text
sum_(c subset j) p_c/ell_(sigma,c)
 <= (2000/1999)*N_(sigma,j)*p_j/ell_(sigma,j).
```

Therefore a sufficient remaining physical quantity is

```text
K_mult,pair
 = sum_(sigma,j) N_(sigma,j)*p_j/ell_(sigma,j).
```

If `K_mult,pair<infinity` on the identical once-charged terminal law, then

```text
J_pair <= (2000/1999) K_mult,pair < infinity,
I_D < nu(X) + [35/(99*2^309)] J_pair.
```

Round 50 proves only that each record has finitely many cells.  It does not
integrate the multiplicity-weighted numerator.  Round 36 also supplies the
sharp logical warning: a perfectly correlated rank law can have the stronger
one-time tail `P(B>b)=4^-b` and every fixed-depth additive D1 `L^(6/5)`
moment, while every positive moment of the `n`-step recut product fails once
`beta*n>=2`.  That model is not claimed physical; it proves that the current
marginal/D1 fields alone do not close this interface.

## 7. Strict frontier

```text
all-mass hat_F one-step Z1:             CERTIFIED_NUMERICAL_REPLAY
all-collision physical survivor Z l1:   CERTIFIED_FINITE_NONNUMERIC_N_OPEN
two-orientation coarse terminal Z l1:   CERTIFIED_FINITE_NONNUMERIC_N_OPEN
Phi_pair needed for coarse terminal Z:  BYPASSED
Phi_pair l1 itself:                     NOT_CERTIFIED
gap zero-density-debit join:             REJECTED
terminal refinement K_mult,pair:         NOT_CERTIFIED
physical J_pair and I_D:                 NOT_CERTIFIED
physical q / strong cemetery:            NOT_CERTIFIED
Gate 4:                                  NOT_CERTIFIED
complete composite gates:                0/5
CM2:                                     NO-GO_FOR_CLAIM
```

## 8. Validation

The certificate/verifier pair enforces pinned dependency hashes, strict JSON
without duplicate or nonfinite numbers, exact rational replay, provenance
parity, verdict parity, byte-identical manifest re-emission, and default
fail-close exit `2`.  The hostile suite rejects `40/40` mutations.
