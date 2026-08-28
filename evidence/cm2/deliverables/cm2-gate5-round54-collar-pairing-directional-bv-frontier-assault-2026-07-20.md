# CM2 Gate 5 Round 54: stagewise collar `E_j/Tr_j`, signed pairing, and directional-BV frontier

Date: 2026-07-20  
Scope: Gate 5 at `s=0`, plus a conditional typed join to the fixed Gate-3
free graph-current carrier.  The positive owner law remains restricted to
one labelled finite regular record at a time.  No all-insertion-time sum is
silently taken.

## Verdict

Round 54 installs an exact owner-trace extension/recovery Borel-kernel schema
on the explicitly collar-admissible subregistry

```text
A_col={omega:d_other(omega)>0}.
```

For such a root, select a canonical one-sided anchored half-open dyadic collar
whose only possible boundary contact is the already-owned root face and whose
remaining points lie in one open fixed-word side cell.  At source stage `j`, `E_j` spreads the root mass
uniformly over that labelled collar.  At every later registered stage `t`,
`Tr_t` collapses the pushed collar to the **mapped** one-sided root.  On owner
trace laws restricted to `A_col`,

```text
Tr_j composed E_j = Id,
K_trace_(j,t) = Tr_t composed K_word_(j,t) composed E_j.
```

Both kernels have mass norm one.  The owner base is standard Borel and may
carry a continuous outer law; it is not retyped as a countable atom list.
Neither positive nor full owner-trace mass of `A_col` is known.  This is not
the missing uniformly proper Round-53 bridge.  The extension pays the exact
one-sided collar debt

```text
Z_col(E nu)=integral_(A_col) ell(omega)^(-1)dnu(omega).
```

Every admissible individual collar has finite cost, but the aggregate may be
infinite.  A grazing root may have `d(omega)=0` because infinitely many
homogeneity strips accumulate at it, despite transverse rank zero.  The
existing parent-`W` owner `Z_B` does not control this new debt:
an exact separator has parent length one and finite full parent debt
`Z_B=2^14`, but collar
lengths `2^(-k^2)` and divergent `sum 2^(k^2-k)`.  Thus no quantitative trace
contraction is promoted.

Two additional routes are sharpened.

1. The immutable hit-minus-miss current admits an exact bounded-Lipschitz
   paired-image estimate before Jordan absolute values.  If its paired
   distance charge decayed at rate `rho`, the existing Round-42 weight would
   already sum it because `w_Z rho=(1+rho)/2<1`.  This bypasses the positive
   `q_*>2` Hölder threshold, but only for the signed current.  No physical
   paired-image rate is known, and the result gives neither positive F10 nor
   cemetery mass.
2. Since the physical Eulerian generator is divergence-free in collision
   area coordinates, `-div(Xh)` is an order-zero signed measure whenever
   `h` has finite directional variation `D_X h` and a finite normal trace.
   On this `BV_X^tr` subcarrier,
   every suffix has TV multiplier exactly one.  The missing suffix derivative
   product disappears, but the source `BV_X` cost and its same-ID boundary
   join are not controlled by the existing `c_X ||h||_infinity` ledger.

Consequently Gate 5 remains `10/18`, complete blocks remain zero, Gate 3 is
not promoted, and CM2 remains `NO-GO`.

## 1. A stage-dependent collar extension/recovery on `A_col`

Fix one label

```text
a=(restriction-id,time-j,physical-event-signature,primitive-key,
   connected-rank-0,side-label,word-cell).
```

Let `nu_j` be the finite Borel owner/root law on the standard-Borel base; it
may have continuous and discrete disintegrations.  Refine a root's parent by
every singularity, homogeneity, owner, and hole boundary occurring in the
fixed finite word.  After selecting the owned side, define `d(omega)` as the
one-sided distance from the anchor root face to the next **other** singularity,
homogeneity, owner, or hole boundary.  The already-owned anchor face is
excluded from that distance.  Retain only `A_col={omega:d(omega)>0}`.  This is an extra physical
predicate: transverse connected rank zero alone does not imply it.  Define

```text
k(omega)=min{k>=0:2^(-k)<=min(1,d(omega))},
ell(omega)=2^(-(k(omega)+1))<d(omega).
```

The extension lives on the joint labelled carrier

```text
Mtilde_j={(omega,x):omega in A_col, x in I_(omega,j)}.
```

The `omega`/record label is retained through `E_j`, the word operator, and
`Tr_t`.  Consequently overlapping physical collar images from two owner
records never make `Tr_t` multivalued.  In each countable chart/word label,
the predicate that an anchored half-open dyadic candidate has no boundary
contact except the designated anchor face and otherwise lies in one open
fixed-word side cell is Borel because the word has
registered continuous inequalities and homogeneity data.  Thus `A_col` is a
countable union of Borel predicates, the least candidate is Borel, and
pushing normalized Lebesgue through the registered collar chart gives a
Borel probability kernel.  More explicitly, with anchor `xi=xi_(omega,j)`,

```text
I_(omega,j)=(xi,xi+ell] on the plus side,
I_(omega,j)=[xi-ell,xi) on the minus side.
```

Its closure may meet the anchor face at `xi`, while the far endpoint remains
strictly interior because `ell<d`.  Put

```text
E_j(omega,d(omega,x))
 =delta_omega(domega)*ell(omega)^(-1)H1(dx)|I_(omega,j).
```

For the regular word suffix `S_(j,t)`, define

```text
Tr_t(omega,S_(j,t)x)
 =(omega,S_(j,t)^side(xi_(omega,j))).
```

The target is the mapped root, not the original source root.  By construction
apart from the designated anchor root face, the whole collar lies in one
connected open side cell of the full fixed-word refinement.  Therefore at
each registered stage:

- `S_(j,t)` is one regular diffeomorphic one-sided branch on the collar interior;
- the killed/survivor bit is the same as the selected one-sided root value;
- there is no internal singularity, homogeneity, owner, or hole cut other
  than the designated anchor contact;
- half-open endpoints are owned exactly once; and
- pushforward preserves the collar mass.

The word operator acts fiberwise and never drops `omega`.

These facts give exactly

```text
||E_j||_mass=||Tr_t||_mass=1 on nu_j|A_col,
Tr_j E_j=Id on nu_j|A_col,
K_trace_(j,t)=Tr_t K_word_(j,t) E_j.
```

In particular `E=Tr=0` is impossible.  This closes the algebraic and
measure-theoretic part of the bridge on each collar-admissible finite record.

It does not close properness.  The source collar density is constant, hence
has log-Hölder mark zero, but its standard-family inverse-length charge is
the extended Borel integral

```text
Z_col(E nu)=integral_(A_col) ell(omega)^(-1)dnu(omega) in [0,infinity].
```

Finiteness is `NOT CERTIFIED`.  A finite aggregate extension would require
this integral to be finite; the following separators show why it cannot be
assumed.  A Round-42 contraction additionally needs the common orientation,
uniform/block recovery, and proper-family hypotheses.  None is certified.

The distinction from the Round-50 parent debt is strict.  On labels `k>=1`
take

```text
p_k=2^(-k),   parent length=1,   B=14,
ell_k=2^(-k^2).
```

Then

```text
sum p_k=1,
sum p_k/(parent length)=1,
sum 2^14 p_k/(parent length)=2^14=16384,
sum p_k/ell_k=sum 2^(k^2-k)=infinity,
sum 2^14 p_k/ell_k=infinity.
```

Thus the current parent-`W` owner `Z_B` cannot be renamed `Z_col,B` without a
new geometric comparison.

There is a second, genuinely grazing obstruction.  On a one-sided coordinate
`c in (0,ell]`, take uniform probability `dc/ell` and the exact shells

```text
H_k=(ell/(k+1)^2,ell/k^2],  k>=1.
```

Their lengths are

```text
ell*(1/k^2-1/(k+1)^2),
```

so the shell masses telescope to one.  After canonical shell subdivision,
each inverse-length contribution is exactly `1/ell`; summing infinitely many
nonempty shells gives `Z=infinity`.  The root `c=0` has full-word clearance
zero.  Therefore a moving-occurrence/grazing root is not admitted to `A_col`
merely because its face intersection is transverse.  The trace mass of
`A_col` is currently unknown, so this subregistry cannot be promoted to the
all-owner bridge.

## 2. Signed hit/miss pairing before absolute values

Work fiberwise on the disjoint marked union over immutable physical record,
event/orientation, and retained source rank `B`; no product coupling is taken
across distinct records or ranks.  The coefficient is the actual physical
signed flux `sigma_e`, not the occurrence-rank envelope `2^B`.  Write its
common-source law as the Jordan decomposition

```text
lambda_p=lambda_p^+-lambda_p^-.
```

With the immutable positive hit/miss kernels `H_p,M_p`, form

```text
mu_p^+=H_p*lambda_p^+ + M_p*lambda_p^-,
mu_p^-=M_p*lambda_p^+ + H_p*lambda_p^-,
J_p=mu_p^+-mu_p^-.
```

Both marginals have the same mass
`m_p=|lambda_p|(source)<=C_flux=8064/5`, the frozen Round-44 one-sign physical
flux upper bound; consequently `J_p(1)=0`.  No equality between `sigma_e` and
`2^B` is asserted.

There is also no continuous-fiber measurable-selection gap.  In each fixed
marked standard-Borel fiber define the canonical normalized-product kernel

```text
pi_p=0                                      if m_p=0,
pi_p=(mu_p^+ tensor mu_p^-)/m_p             if m_p>0.
```

It has marginals `mu_p^+,mu_p^-`, total mass `m_p`, and depends Borelly on the
fiber law.  For

```text
||phi||_BL=max(||phi||_infinity,Lip(phi)),
```

one has pointwise

```text
|phi(y+)-phi(y-)|
 <=min(2,d(y+,y-)) ||phi||_BL.
```

Hence

```text
d_p(pi_p)=integral min(2,d(y+,y-))d pi_p(y+,y-),
||J_p||_(BL*)<=d_p.
```

For paired-distance upper bounds `2,1,1/16,1/1024`, the corresponding exact
physical-flux charge uppers are respectively
`16128/5, 8064/5, 504/5, 63/40`.

This estimate uses the signed physical pair before taking the two Jordan
parts separately.  It is stronger than constant-test cancellation, but it
contains a new geometric mark: the distance between the two suffix images.

If a future theorem gives

```text
d_p<=C_pair delta_pair^p,
```

then

```text
sum_p w^p ||J_p||_(BL*)
 <=C_pair/(1-w delta_pair)
```

whenever `w delta_pair<1`.  In particular, for

```text
rho=(111718729/111718750)^9148,
w_Z=(1+rho^(-1))/2,
```

the choice `delta_pair=rho` gives

```text
w_Z rho=(1+rho)/2<1,
sum_p w_Z^p ||J_p||_(BL*)<=2 C_pair/(1-rho).
```

This route does not need a positive `L^q`, `q>q_*`, moment.  A useful
physical-flux sufficient condition is

```text
support(pi_p) subset {d(y+,y-)<=A delta_pair^p}.
```

It yields `d_p<=A(8064/5) delta_pair^p`.  Alternatively, a future purely
rank-envelope theorem could assume both

```text
m_p<=C_sigma 2^B,
support(pi_p) subset {d<=A 2^(-B)delta_pair^p},
```

and then obtain `d_p<=A C_sigma delta_pair^p`; this is an envelope
hypothesis, not `sigma_e=2^B`.  No such
physical paired-image separation has been proved.  In particular:

```text
physical paired-image rho-rate:       NOT CERTIFIED
unconditional signed BL resolvent:    NOT CERTIFIED
positive F10/TV face tower:           NOT CERTIFIED
```

The last boundary is essential: signed image cancellation cannot pay a
positive coarea or cemetery ledger.

## 3. Divergence-free order reduction on a directional-BV source

In collision area coordinates, the regular Eulerian generator satisfies

```text
X_s=(partial_s F_s) composed F_s^(-1),
div_mu X_s=0.
```

Define the trace-equipped directional space

```text
BV_X^tr(U)={h in L1(U):D_X h is a finite signed measure and
            gamma_Xh is a finite normal trace satisfying Gauss--Green}.
```

Here `mu=R dr dp`, and `D_Xh` is the divergence/current derivative relative
to `mu`, characterized on compact interior tests by

```text
integral phi d(D_Xh)=-integral h X(phi)dmu.
```

For compactly supported `h`, distributional integration by parts gives

```text
T_h=-D_X h.
```

On a regular branch domain `U`, the correctly typed identity is

```text
T_h=-D_X h+gamma_Xh,
gamma_Xh=(R h X dot n_U)H^1|partial U when the classical trace exists.
```

Each physical boundary trace is included exactly once.  Thus

```text
C_BVXtr(h;U)=TV(D_X h)+TV(gamma_Xh),
TV(T_h)<=C_BVXtr(h;U).
```

After order reduction, any finite regular suffix merely pushes forward a
finite signed measure:

```text
TV(S_*T_h)<=TV(T_h).
```

Therefore this subcarrier has

```text
C_dyn=1
```

in the order-zero TV / `C^0`-dual transport norm, below the quarter threshold
`7961063/7800000`.  This is not a completed common physical dynamic-test
field.  No bounded identification with the required physical `B0`,
dynamic-Hölder tests, and all 18 operator fields has been installed.

The directional and normal-trace source cost is genuinely stronger than the current pointwise source
charge.  In the logical flat separator take `U=[0,1]^2`, `X=e_1`, and
normalize `R=1`; let `h_N` be a triangle wave with `N`
periods and range `[-1,1]`.  Then

```text
||h_N||_infinity=1,
TV(D_X h_N)=4N.
```

Thus `c_X ||h||_infinity` cannot control `C_BVX`.  For a piecewise constant
flat density the interior derivative does vanish, leaving only the physical
boundary flux, but Gate 5 needs the full physical input class, not only this
subcarrier.

The exact frontier is now:

```text
directional-BV order reduction:             CERTIFIED
order-zero suffix TV multiplier 1:          CERTIFIED_SUBCARRIER
all-input physical BV_X source bound:       NOT CERTIFIED
same-ID boundary-flux assembly for BV_X:    NOT CERTIFIED
complete physical F17:                      NOT CERTIFIED
```

## 4. Conditional Gate-3 join

The two order-reduced pieces have different destinations in the fixed free
carrier

```text
X0_hat=(C^{1,alpha}(N))* direct-sum_1 l1(Omega_<=2;M(I)).
```

The bulk order-zero measure `-D_Xh` belongs to the first
`(C^{1,alpha}(N))*` summand.  Only parameterized boundary graph fluxes
`gamma_Xh` belong to the `41,508` `M(I)` slots in the second summand.  A bulk
measure is never retyped as a graph slot.

The following joins still have to be proved on the actual `41,508` slots:

1. bind every moving boundary graph/component and owner ID to its fixed graph slot;
2. lift physical `B2` inputs with a uniform `BV_X^tr` bound;
3. assemble duplicate/artificial domain fluxes before total variation;
4. include both the bulk order-zero measure and boundary graph-slot family
   boundedly in physical `B0`;
5. prove the common-atlas moving limit and growing-depth no-`|s|^-1` tail;
6. complete the other 17 fields on one recovered physical block.

Therefore `R_s`, `Q_s`, `Q_s P_hat_s R_s=P_s`, and `MT_DQ` remain not
certified.  The finite-record distribution identity is only a typed
conditional join.

## 5. Latest-technology audit

The official arXiv query was repeated on 2026-07-20.  The relevant snapshots
remain

```text
2606.10155v1 / 2604.19671v2 / 2604.25881v1 / 2502.07765v2.
```

The available mechanisms are stable-curve anisotropic norms, projective
cones, standard-family Growth, and small/sparse-hole recovery.  None states
the same-ID one-sided collar debt bound, a hit/miss paired-image contraction,
or a numerical `BV_X`-to-physical operator block.  No direct field upgrade
was imported.

## 6. Strict status and continuation

Certified this round:

```text
collar-admissible stagewise mass E_j/Tr_j:   CERTIFIED
Tr_j E_j=Id and killed-word intertwining:    CERTIFIED_ON_A_col
one-sided collar debt and separator:         CERTIFIED
signed hit/miss BL pair bound:               CERTIFIED
conditional rho-weight signed resolvent:     CERTIFIED_CONDITIONAL_ONLY
directional-BV order reduction / suffix 1:   CERTIFIED_SUBCARRIER
Gate-3 directional-BV typed join:            CERTIFIED_CONDITIONAL_ONLY
```

Not certified:

```text
Round-53 uniformly proper trace bridge:       NOT CERTIFIED
positive/full owner trace mass of A_col:       NOT CERTIFIED
aggregate Z_col / trace contraction:          NOT CERTIFIED
physical paired-image rho-rate:               NOT CERTIFIED
positive F10 / face tower / cemetery:          NOT CERTIFIED
all-input physical BV_X and boundary join:     NOT CERTIFIED
physical F17 / strong F13 / F14/F15/F18:       NOT CERTIFIED
Gate-3 Q_s/R_s and MT_DQ:                      NOT CERTIFIED
Gate-5 maturity / complete blocks:             10/18 / 0
complete composite gates:                      0/5
CM2:                                           NO-GO_FOR_CLAIM
```

The shortest next route is now one of:

1. first prove that `A_col` carries the required positive/full owner-trace
   mass, then bound its all-time one-sided collar debt and combine it with a
   uniform recovery/proper-family block;
2. prove a physical-flux hit/miss paired-image separation, either directly at
   rate `rho` or through a separately proved `2^B` mass envelope paired with
   `2^(-B)` distance decay;
3. prove the all-input `BV_X` source and boundary assembly in the physical
   block, then bind its order-zero measure to `B0` and the Gate-3 slots.

## 7. Validation

Artifacts:

- `cm2_gate5_round54_collar_pairing_directional_bv_frontier_cert.py`;
- `cm2_gate5_round54_collar_pairing_directional_bv_frontier_verifier.py`;
- `cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json`;
- this report and its SHA ledger.

The suite pins seven dependency manifests and semantically checks the
Round-53 recovery/intertwining requirements, the Round-50 owner registry,
the Round-44 common signed pair, the Round-43 divergence-free current, the
Round-47 boundary-only scope, the Round-42 weight, and the Gate-3 slot count.
It independently recomputes all collar, pairing, weight, and directional-BV
rows and freezes every nonpromotion boundary.

```text
syntax:                    2/2 PASS
strict JSON:               duplicate keys and NaN/Infinity rejected
dependency hashes:         7/7 PASS
deterministic replay:      PASS
deterministic re-emission: PASS
hostile mutations:         141/141 rejected
default cert/verifier:     both fail closed with exit 2
Gate-5 maturity:           10/18
complete blocks:           0
CM2:                       NO-GO_FOR_CLAIM
```
