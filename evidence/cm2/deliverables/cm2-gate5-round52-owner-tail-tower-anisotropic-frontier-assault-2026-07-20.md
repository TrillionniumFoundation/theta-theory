# CM2 Round 52 Gate-5 owner-tail / face-tower / anisotropic frontier

Date: 2026-07-20  
Scope: Gate 5 only, base parameter `s=0`; old artifacts are untouched.

## Verdict

Round 52 closes the same-ID occurrence-tail transfer at exactly the largest
scope justified by positivity: **for each fixed insertion time `j`**, after
aggregating the registered regular arbitrary-`R_n` records with `j<n` and
applying owner deduplication, the raw source-rank `4^{-b}` tail transfers with
constant one.  Every finite regular suffix preserves record total mass and
the retained source-rank mark.  Distinct records have distinct suffix maps,
so this is not a domination statement on common target Borel subsets.

This is not a face-tower theorem.  An exact nested-tube model shows why:
collision-SRB survivor mass may decay like `rho^p` while a collision-null
never-return face retains all trace mass.  In that model the owner charge is
constant, the ordinary `Z`/mass forcing is summable at the Round-42 weight,
and every recurrence with `kappa_B<1` eventually fails.  Since

```text
2rho/(1+rho)<1,
```

the current certified inputs cannot give the required fixed-weight
contraction.

The natural stable-curve anisotropic test candidate also fails to control the
full Eulerian divergence current: it controls stable-tangential derivatives,
whereas the physical bulk insertion has two vector components.  Adding a
uniform full-gradient term repairs the source pairing but reintroduces the
unbounded suffix multiplier already isolated in Round 51.

Therefore:

```text
fixed-insertion same-ID owner tail transfer: CERTIFIED
all-insertion-time owner tail sum:           NOT CERTIFIED
kappa_B < 2rho/(1+rho):                      NOT CERTIFIED
aggregate Z_B / face-tower moment:           NOT CERTIFIED
physical anisotropic F17:                    NOT CERTIFIED
strong F13 / complete F10:                   NOT CERTIFIED
Gate-5 maturity:                             10/18
complete 18-field blocks:                    0
CM2:                                         NO-GO
```

## 1. Constant-one owner-tail transfer at a fixed insertion time

Round 49 already typed the occurrence kernel on a fixed record as

```text
K_occ(y,e,A)
 = Z_N^-1 integral 1_(A intersect R_y)(iota_e(theta)) w_e(theta) dtheta.
```

Thus it is a positive restriction of the raw occurrence coarea law.  Fix one
insertion time `j`.  Aggregate over all finite return depths `n>j`, all
regular arbitrary-`R_n` path records and all 64 occurrence seeds.  After the
corner/simultaneous-event cemetery removal:

1. the return levels and frozen-owner path fibres are pairwise disjoint;
2. restriction by one regular record only deletes mass;
3. owner minimization only deletes duplicate representations;
4. a finite regular suffix pushforward preserves record total mass and the
   retained source-rank mark.

Consequently, on the disjoint source-marked union,

```text
sum_a m_(j,a)^owner{B>b} <= m_occ{B>b},
```

and the corresponding total-mass inequality holds.  After the recordwise
suffix pushforwards, these total/marked-tail inequalities remain true on the
disjoint marked target union.  Since the suffix maps differ with `a`, no
inequality against `m_occ(A)` for one unmarked target Borel set `A` is
asserted.

The complete raw rank tail therefore transfers without a density loss:

```text
sum_a m_(j,a)^owner{B>b}
 <= (9158592/6875) 4^(-b),       b>=14.
```

The exact fixed-time integrals are the Round-51 values:

```text
integral 2^B                       < 23253221519103/880000,
forward F10 owner charge           < 395304765824751/220000,
reverse F10 owner charge           < 162772550633721/176000,
bidirectional F10 owner charge     < 2395081816467609/880000.
```

This genuinely repairs the earlier statement that there was no transfer at
all.  The remaining distinction is temporal: the inequality is uniform in
`j`, but it contains no factor decaying with `j`.  Summing this constant bound
over insertion times is illegal.

It also remains a TV/positive-trace statement.  It does not supply the
full-gradient bulk pairing required by F17.

## 2. Exact collision-null face-tower obstruction

Let

```text
rho=(111718729/111718750)^9148,
w_Z=(1+rho^-1)/2.
```

On `X=[0,1]^2`, take collision volume `mu=dx dy`, the face

```text
Gamma={0}x[0,1],
nu=H^1 restricted to Gamma,
```

and nested survivor sets

```text
Q_p=[0,rho^p]x[0,1],
R_p=Q_(p-1)\Q_p.
```

Then

```text
mu(Q_p)=rho^p,
intersection_p Q_p=Gamma,
mu(Gamma)=0,
nu(Q_p)=nu(Gamma)=1.
```

Put the constant rank `B=14` on `Gamma` and use one owner event with the same
face ID in every block.  Every fixed-time raw tail and every raw rank moment
is finite, yet

```text
b_p=integral_(Gamma intersect Q_p) 2^B dnu=2^14
```

for all `p`.  At the same time, the model forcing sequences

```text
z_p=m_p=rho^p
```

are summable at the frozen aggregate weight because

```text
w_Z*rho=(1+rho)/2<1.
```

For any finite `A_B,C_B` and `0<=kappa_B<1`,

```text
b_(p+1) <= kappa_B b_p + A_B z_p + C_B m_p
```

fails for all sufficiently large `p`.  Thus the current hypotheses permit an
asymptotic coefficient at least one, while the Round-50 requirement is

```text
kappa_B < 2rho/(1+rho) < 1.
```

This is a logical countermodel, not a claim that the actual billiard trace is
supported on its never-return set.  It identifies the new first missing
physical theorem precisely:

```text
trace-nullity of the collision-null never-return/cemetery set,
```

or a quantitative trace-survivor contraction strong enough to replace that
nullity.

Collision-SRB Kac recurrence alone cannot provide it because the face law is
singular to collision volume.

## 3. Why the existing `L^q`, `q<2`, tail cannot meet the fixed weight

Even grant the currently missing estimate

```text
nu_p(total) <= rho^p nu_0(total).
```

If the rank cost has an `L^q(nu_0)` moment, Holder gives only

```text
b_p <= C_q rho^(p(1-1/q)),
kappa_q=rho^(1-1/q).
```

The raw endpoint tail supplies every `q<2`; `q=3/2` is explicitly certified.
But for every `1<q<=2`,

```text
kappa_q >= sqrt(rho) > 2rho/(1+rho).
```

The strict endpoint inequality is exact:

```text
[2rho/(1+rho)]^2 < rho
iff 4rho < (1+rho)^2
iff (1-rho)^2>0.
```

Thus even a hypothetical `L^2` endpoint plus trace-mass decay would miss the
fixed Round-42 threshold.  That route needs a genuine `q>2` owner-law moment,
or cancellation/recurrence information sharper than Holder interpolation.

There is a possible weaker-weight route, but it remains conditional.  If the
trace-survivor decay were proved, the certified `q=3/2` moment could use

```text
w_face=(1+rho^(-1/3))/2 < w_Z,
w_face*rho^(1/3)=(1+rho^(1/3))/2<1.
```

The Round-42 ordinary forcing sums would remain finite at the smaller weight.
This would give a weaker positive face-tower exponent, but no trace-survivor
decay is currently available, so nothing is promoted.

## 4. Physical anisotropic F17 candidate and transverse-current failure

The stable-curve spaces reviewed by Demers--Liverani test distributions
against Holder observables on stable curves and add a separate transverse
comparison seminorm.  Their scalar test core suggests

```text
||phi||_sc=||phi||_infinity+||partial_stable phi||_infinity.
```

This is dynamically natural along the matched stable geometry, but it is not
the physical F17 pairing required here.  The Round-43 bulk insertion is

```text
T_K(phi)=integral K dot grad(phi) dmu,
K=X*(P_j h),
```

and no certified identity makes the transverse component of `X` vanish.

The exact local countermodel is

```text
U_L=[0,1/L]x[0,1],
stable direction=e_2,
phi_L(u,s)=L*u,
K=e_1.
```

Then

```text
||phi_L||_sc=1,
integral_(U_L)|K|=1/L,
T_K(phi_L)=1.
```

The response-to-source-mass ratio is `L`, hence no finite scalar stable-curve
constant controls the full divergence pairing.

Adding a uniform full-gradient term controls this source pairing, but the
area-preserving diagonal suffix family from Round 51 makes its pullback norm
unbounded.  The two incomplete halves therefore cannot simply be added.

A valid physical F17 construction must instead be a vector-current graph
space containing

```text
-div(K)+B
```

with all four interfaces proved on the same space:

1. an explicit injection for both components of the Eulerian vector current
   `K`;
2. an explicit injection for the physical two-trace boundary current `B`;
3. pairing with the required physical CM2 observable algebra;
4. suffix pushforward cost below `7961063/7800000` (or a rebalanced block
   theorem with an explicitly compatible larger cost).

The official `2606.10155v1` stable/unstable norms do not state this typed
vector-current injection or the required numerical comparison constant.
They therefore guide the construction but do not close F17.

## 5. Downstream field audit

The fixed-insertion transfer is a real sublayer, not a completed field:

```text
complete all-face F10:
  blocked by insertion-time face-tower summability, quotient/corner cemetery
  and the remaining all-face joins;

strong F13:
  blocked by the vector-current F17 transport and face-tower convergence;

F14 / F15:
  still lack the complete regular-density and common recovered
  standard-family operator costs;

F17:
  blocked by the missing common vector-current anisotropic space;

F18:
  blocked because F14--F17 are not complete on one physical block.
```

Gate 5 therefore stays `10/18`, with zero complete 18-field blocks.

## 6. Strict continuation route

The shortest Gate-5 continuation is now:

1. prove that the collision-null never-return/cemetery set is also null for
   the owner trace law, or prove an explicit blockwise trace-survivor
   contraction;
2. combine that theorem with either a `q>2` same-ID owner moment at the fixed
   `w_Z`, a sharper signed recurrence, or the explicitly weaker
   `w_face` route;
3. build the vector-current anisotropic graph space with the four typed F17
   interfaces above;
4. only then promote aggregate `Z_B`, the face-tower moment, complete F10,
   strong F13, F14/F15/F17/F18 and cemetery-compatible F16.

## 7. Validation

Artifacts:

- `cm2_gate5_round52_owner_tail_tower_anisotropic_frontier_cert.py`;
- `cm2_gate5_round52_owner_tail_tower_anisotropic_frontier_verifier.py`;
- `cm2-gate5-round52-owner-tail-tower-anisotropic-frontier-manifest-2026-07-20.json`;
- this report and its SHA ledger.

The suite hash-pins eight dependencies and independently recomputes the exact
rank integrals, aggregate weight identities, AM--GM threshold separation,
nested-tube rows and transverse-current rows.

```text
syntax:                    2/2 PASS
strict JSON:               duplicate keys and NaN/Infinity rejected
deterministic replay:      PASS
hostile mutations:         104/104 rejected
default cert/verifier:     fail closed with exit 2
Gate-5 maturity:           10/18
complete blocks:           0
CM2:                       NO-GO_FOR_CLAIM
```
