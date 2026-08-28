# CM2 Round 53 Gate-4 fractional-Z / common-return frontier

Date: 2026-07-20  
Strict status: **an exact same-measure boundary-Z bridge now reduces the
physical defect moment to one global cell numerator, and a second conditional
bridge prices the extra common-refinement properisation clock.  Neither
physical numerator is currently bounded.  Physical `q`, strong cemetery,
Gate 4, and CM2 remain not certified.**

## 1. Scope and provenance

This append-only leaf reads the full Round-35 common carrier and physical D1
ledgers, the Round-50 physical grouping, the Round-51 two-proper-view law, the
Round-52 defect/common-survivor leaf, the Round-36 aggregate growth recurrence,
the Round-52 fixed-insertion owner tail, and the Round-28 physical `q` typing.
It changes no earlier artifact.

The new executable artifacts are:

- `cm2_gate34_round53_fractional_z_common_return_frontier_cert.py`;
- `cm2_gate34_round53_fractional_z_common_return_frontier_verifier.py`;
- `cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.json`;
- `cm2-gate34-round53-fractional-z-common-return-frontier-manifest-2026-07-20.sha256`.

Eight dependency manifests are hash-pinned.  All claims below are either
exact implications with explicitly stated hypotheses or exact
nonimplications.  No external theorem is promoted.

## 2. The correct cell quantity and its exact tail

Round 52 certified the Borel, once-charged retyping that retains
`natural-short-cell-k` and `image-recut-rank`.  For every positive common cell
`c`, let

```text
p_c       = its one physical mass,
ell_fw,c  = its forward carrier length,
ell_rev,c = its reverse carrier length.
```

Forward and reverse are two views of this one charge.  Define the full
physical-cell target

\[
 J_{\rm pair}
 =\int\sum_c p_c
   \left(\ell_{{\rm fw},c}^{-1}+\ell_{{\rm rev},c}^{-1}\right)
   \,d\lambda .
\]

This is an unnormalised standard-family boundary numerator on the cell law;
it is not the additive incidence-rank D1 mark.

Put

\[
 M_c=\left\lceil
       \log_2\frac1{\min(\ell_{{\rm fw},c},\ell_{{\rm rev},c})}
     \right\rceil_+ .
\]

For every integer `m>=0`, the strict Round-52 tail convention gives the exact
event identity

\[
 \{M_c>m\}
 =\{\min(\ell_{{\rm fw},c},\ell_{{\rm rev},c})<2^{-m}\}.
\]

There is no dyadic rounding loss.  On that event,

\[
 p_c
 <2^{-m}\frac{p_c}{\min(\ell_{{\rm fw},c},\ell_{{\rm rev},c})}
 \le 2^{-m}p_c
   \left(\ell_{{\rm fw},c}^{-1}+\ell_{{\rm rev},c}^{-1}\right).
\]

Consequently, on the identical once-charged cell measure,

\[
 T_m=\nu\{M_c>m\}<2^{-m}J_{\rm pair}.
\]

Thus `J_pair<infinity` would imply the Round-52 quarter-block condition with
`C_quarter=J_pair`, and in fact gives the stronger linear dyadic tail.

## 3. Exact direct defect-moment coefficient

The proof does not use a floating-point exponential estimate.  For `k>=2`,

\[
 k!\ge2\,3^{k-2},
\]

so

\[
 e^{1/6}
 <1+\frac16+\frac1{72}\sum_{j\ge0}\left(\frac1{18}\right)^j
 =1+\frac16+\frac1{68}
 =\frac{241}{204}
 <\frac{13}{11}.
\]

The last inequality has integer cross-product gap one:
`13*204-241*11=1`.

Insert `T_m<=2^-m J_pair` into the exact Round-52 skip-one layer-cake identity

\[
 I_D=\nu(X)+(a^2-1)T_{310}
 +(a-1)\sum_{m\ge311}a^{m-309}T_m,
 \qquad a=e^{1/6}.
\]

Using `a<13/11`, the full rational coefficient is

\[
 \begin{aligned}
 &\left[\left(\frac{13}{11}\right)^2-1\right]2^{-310}
 +\frac2{11}2^{-309}
   \sum_{d\ge2}\left(\frac{13}{22}\right)^d \\
 &\hspace{4em}=\frac{35}{99}\,2^{-309}
 =\frac{70}{99}\,2^{-310}.
 \end{aligned}
\]

Therefore the exact conditional bridge is

\[
 \boxed{
 I_D<\nu(X)+\frac{35}{99\,2^{309}}J_{\rm pair}
 }.
\]

This is the shortest same-measure route found so far.  The physical full-law
bound `J_pair<infinity` is not currently certified, so `I_D` remains open.

## 4. Cross-gate aggregate-Z resolvent

Round 36 froze the abstract physical-level recurrence

\[
 Z_{n+1}\le aZ_n+b m_n+F_n,
 \qquad
 a=\frac{360134800}{360493663},
 \quad b=2\cdot10^{90}.
\]

Here `F_n` denotes the full new-face injection.  Summing through `N-1` gives
the exact finite identity

\[
 (1-a)\sum_{n=1}^{N-1}Z_n+Z_N
 \le aZ_0+b\sum_{n=0}^{N-1}m_n+
        \sum_{n=0}^{N-1}F_n.
\]

Hence

\[
 \sum_{n\ge1}Z_n
 \le \frac{aZ_0+b\sum_n m_n+\sum_nF_n}{1-a},
 \qquad
 \frac1{1-a}=\frac{360493663}{358863},
\]

whenever both forcing sums are finite.

Round 28 gives the normalized survivor tail

```text
S_n < (550000/147)*(111718729/111718750)^floor(n/N_open),
```

so `sum S_n<(550000/147)*N_open/(1-r)<infinity`; the integer `N_open` is
finite but nonnumerical.  This does **not** yet prove `sum m_n<infinity` in
the Round-36 recurrence.  Round 28 types

```text
S_n=mu_s(Q_n)/mu_s(C_s),
a_n=S_(n-1)-S_n,
```

whereas Round 36 calls `m_n` the mass in one unnormalised same-ID
survivor/return-level standard-family representation.  No pinned artifact
identifies the component ID, level shift, or normalization of these two
symbols.

Only conditionally, if a theorem proves

```text
m_n=mu_s(C_s)*S_n
```

or an explicit fixed shift/domination by that quantity on the same IDs, does
the Round-28 tail imply

```text
sum_n m_n < mu_s(C_s)*(550000/147)*N_open/(1-r) < infinity.
```

Three physical joins are therefore indispensable:

1. a same-ID level-index and normalization theorem from Round-28 `S_n` to
   the Round-36 unnormalised `m_n`;
2. the all-insertion-time same-ID face-tower bound `sum F_n<infinity`,
   including cemetery;
3. a same-law terminal-extraction inequality that bounds `J_pair` by the
   evolved aggregate `Z` plus the terminal face injection.

This typing distinction is strict.  Round 52's owner `Z_B` is a positive
face injection built from roots divided by the parent-W length.  Its
fixed-insertion tail does not itself equal or dominate the terminal cell
numerator `J_pair`.  It first needs the full Growth join above.  Since the
current owner estimate is uniform in insertion time but has no time decay,
it cannot be summed.

Once all three joins are installed, the displayed resolvent would give
`J_pair<infinity`, and the boxed estimate would close physical `I_D` in the
same stroke.  This is a conditional cross-gate consequence, not an actual
Round-53 physical `J_pair` estimate.

## 5. A second Z is required for the common survivor

The first numerator prices the orientation cell endpoints.  It does not
control the fragmentation of the Round-52 common terminal survivor under the
two-view transport.

Let `h(y)>249p(y)/250` be the same-parent common terminal-survivor mass.  A
future physical common-refinement theorem must first provide standard-Borel
regular connected-component kernels in both orientations, with exact outer
disintegration and no duplicate charge.  On that identical raw restriction,
define

\[
 J_{\cap}(y)=J_{\cap,{\rm fw}}(y)+J_{\cap,{\rm rev}}(y),
 \qquad
 z_{\cap}(y)=\frac{J_{\cap}(y)}{h(y)}.
\]

The required new global hypothesis is

\[
 J_{\cap,{\rm total}}=\int J_{\cap}(y)\,d\lambda(y)<\infty.
\]

Use the strict properness threshold.  Define

```text
D_cap=0                              if z_cap<C_p,
D_cap=min{d>=1:2^-d*z_cap<C_p/2}     if z_cap>=C_p.
```

In particular, exact equality `z_cap=C_p` is not declared proper: it gives
`D_cap=2`, because `d=1` only reaches equality `C_p/2`.

For positive `D_cap`, minimality gives

\[
 2^{D_{\cap}}\le\frac{4z_{\cap}}{C_p}.
\]

The exact half-block inequality `a^696<1/2` then makes the two
orientation-specific pushforwards proper after the synchronized extra clock
`696 D_cap`.  The raw common points are still charged once; Round 51 may
select one proper reference law and transport the other view.

This gives a proper **two-view reference carrier**.  It does not turn the two
orientation-specific pushforwards into one physical first-return kernel.

The extra clock has a clean fractional-Z moment.  Since

\[
 e^{D_{\cap}/6}
 <\left(\frac{13}{11}\right)^{D_{\cap}}
 <\left(\frac{13}{11}\right)^3 2^{D_{\cap}/4},
\]

Hölder gives, with `H=integral h`,

\[
 \int h e^{D_{\cap}/6}
 \le H+\frac{2197}{1331}
        \left(\frac4{C_p}\right)^{1/4}
        H^{3/4}J_{\cap,{\rm total}}^{1/4}.
\]

Since `C_p>4`, the same quantity is strictly below the purely rational
relaxation

\[
 H+\frac{2197}{1331}H^{3/4}J_{\cap,{\rm total}}^{1/4}.
\]

Thus a physical finite `J_cap` would simultaneously provide common two-view
properisation and the moment of this **one** additional synchronized recovery
clock.  The physical Borel common-refinement atlas and its `J_cap` integral
are not yet certified.

## 6. Exact independence of the two Z interfaces

The existing countermodels now have a sharper interpretation.

### 6.1 D1 and fixed-insertion owner tails do not imply `J_pair`

On the Round-52 band of mass `2^-n`, split a unit fibre into `2^(n^2)`
cells of length `2^(-n^2)`, retain fixed physical D1 density `D0`, and charge
the band once.  Then

```text
D1 L^(6/5) mass moment:  D0^(6/5)*sum_n 2^-n < infinity,
J_pair band lower:       2^(n^2-n),
defect band moment:      2^-n*exp((n^2-309)/6).
```

The last lower bound has successive ratio

\[
 \frac12e^{(2n+1)/6}
 >\frac12\left(\frac76\right)^{2n+1}>1
 \qquad(n\ge18),
\]

so it diverges.  Every fixed insertion record is finite, but the all-time
sum is not.  Hence neither the physical D1 moment nor the current
fixed-insertion owner transfer closes `J_pair`.

### 6.2 Finite marginal Z does not imply `J_cap`

The Round-52 interval-translation separator has two marginal survivor
families with normalized boundary `1000/999<C_p`, terminal common mass
`499/500`, but common pullback pieces `A_k` satisfying

\[
 J_{\cap}=\sum_k\frac{m(A_k)}{|A_k|}=\sum_k1=\infty.
\]

Thus even a future proof of finite `J_pair` would not, by itself, prove the
common-refinement numerator.  A physical curvewise/refinement estimate is
independent and necessary.

### 6.3 Absolutely continuous Z does not imply strong cemetery

The Round-52 nested-tube separator has a collision-null never-return set with
full trace mass.  Therefore finite collision-SRB/standard-family numerators
do not automatically control singular boundary currents.  Trace-nullity or
a quantitative trace-survivor contraction remains an independent physical
theorem.

All three models are logical nonimplications for the installed fields.  None
asserts that the billiard realizes the abstract separator.

## 7. Strict `q` and cemetery typing

Certified by this leaf:

1. the exact same-law implication
   `J_pair<infinity => T_m<2^-m J_pair => I_D<infinity`;
2. the exact rational coefficient `35/(99*2^309)`;
3. the unweighted aggregate-Z `l1` resolvent and its conditional cross-gate
   route to `J_pair`;
4. the conditional implication from a physical finite `J_cap` to two
   orientation-specific proper pushforwards and one extra synchronized-clock
   moment;
5. exact separation of D1, fixed-time owner, marginal Z, and strong cemetery
   from the two target numerators.

Still not certified:

1. the full-law physical `J_pair` and hence physical `I_D`;
2. the Round28-`Q_n` to Round36-`m_n` same-ID, level-index and normalization
   join;
3. all-time face forcing and same-law terminal extraction;
4. the physical common-refinement registry and `J_cap`;
5. a physical proper same-ID first-return kernel;
6. every later/repeated recovery-clock moment;
7. intermediate C24 avoidance and numerical `H_joint`;
8. physical `C_fw,C_rev,q` in the Round-28 sense;
9. strong singular/current cemetery;
10. Gate 4 and CM2.

The Round-52 parent-charged postclock ambient max-envelope remains valid.
Neither conditional Z bridge upgrades that ambient envelope to physical `q`.

## 8. Next shortest route

1. First identify the Round-36 unnormalised `m_n` with an explicitly shifted
   and normalized Round-28 survivor/return mass on the same IDs.  Then prove
   the physical all-time face-tower sum and an exact terminal-extraction
   inequality on the once-charged cell law.  Through the Round-36 resolvent,
   these three joins close `J_pair` and `I_D` together.
2. Independently materialise the common terminal-survivor component atlas and
   prove `integral J_cap<infinity`.  Then apply the synchronized conditional
   properisation-clock bridge above.
3. Prove the physical first-return/intermediate-avoidance typing and the
   moments of every remaining/repeated recovery clock before defining `q`.
4. Prove trace-nullity or trace-survivor contraction and construct the strong
   singular/current cemetery on the same carrier.
5. Only after these joins, combine with numerical `H_bump/H_out` and the
   independent `H_cover/beta` atlas to promote complete `C_fw,C_rev,q`.

## 9. Verification

The verifier independently reconstructs the exponential remainder, the
skip-one layer-cake coefficient, all cell rows, the exact aggregate
recurrence, the strict `z=C_p -> D_cap=2` boundary, the 696 half-block, and
the separation-model rows.  It is fail-closed on dependency hashes, unsafe
paths, duplicate JSON keys, NaN/Infinity, schema changes, replay mismatch,
typing promotion, and verdict mutation.

Final replay targets:

- Python syntax: `2/2 PASS`;
- dependency SHA validation: `8/8 PASS`;
- integrity, independent arithmetic, and deterministic replay: `PASS`;
- adversarial mutations: `172/172 REJECTED`;
- deterministic manifest re-emission: byte-identical `PASS`;
- certificate and verifier default modes: both exit exactly `2`;
- strict gate verdict: `0/5`, CM2 `NO-GO_FOR_CLAIM`.
