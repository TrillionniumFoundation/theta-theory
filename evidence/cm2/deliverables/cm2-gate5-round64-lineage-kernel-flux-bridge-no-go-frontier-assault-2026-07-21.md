# CM2 Round 64 Gate 5 — lineage kernel and flux-bridge no-go frontier

Date: 2026-07-21

Strict verdict: **Gate-5 maturity remains 10/18, complete 18-field blocks
remain zero, complete composite gates remain 0/5, and CM2 remains
NO-GO_FOR_CLAIM.**

## 1. Frozen scope

This append-only leaf pins the Round-63 aggregate and independent audit, the
Round-63 Gate-5 leaf, and the Round-44, 50, 52, 54, 56, 60, 61 and 62
Gate-5 physical frontiers used below.  No frozen artifact is edited.

## 2. Exact owner-lineage kernel criterion

Let E_j and E_(j+1) be standard-Borel slices with immutable non-time label
maps ell_j:E_j->L and ell_(j+1):E_(j+1)->L.  Put

    beta_j=(ell_j)_# Lambda_j.

For 0<=c<=1, there exists a label-preserving substochastic kernel K_j with

    Lambda_(j+1)=Lambda_j K_j,        K_j 1<=c

if and only if

    beta_(j+1)<=c beta_j.

Necessity is projection.  For sufficiency disintegrate both measures over
L, set r=d beta_(j+1)/d beta_j, and on each source fibre use mass r(ell_j x)
times the target conditional law.  The smallest possible coefficient is

    c_* = ||d beta_(j+1)/d beta_j||_infinity,

with c_*=infinity when absolute continuity fails.

This reduces the Round-63 abstract K_j debt to one exact same-label,
cross-j marginal domination row.  It is absent from the frozen inputs.
A singular label switch admits no preserving kernel.  A stationary
nonzero label law has c_*=1 and cannot meet w_Z c_*<1 because w_Z>1.

For a fibre-constant Lyapunov weight V_j=v_j o ell_j, the exact row is

    r_j v_(j+1) <= kappa_j v_j.

This weighted row is used together with the unweighted sub-Markov row
r_j<=1 from the first criterion; it does not replace it.

The uniform condition may be weakened to the nonuniform summability

    sum_j w_Z^j product_(i<j) kappa_i < infinity.

Fixed-j uniform anchors do not imply either cross-time statement.

## 3. The trace-density exponent is not q_col

Use the pinned Round-52 values

    rho=(111718729/111718750)^9148,
    w_Z=(1+rho^(-1))/2.

If an optimistic trace RN density belongs only to L^q, the Hölder survival
factor is rho^(1-1/q).  The exact critical exponent is

    q_trace^*
      =1/(1-log(w_Z)/(-log(rho))) > 2.

Indeed at q=2,

    w_Z sqrt(rho)
      =(sqrt(rho)+1/sqrt(rho))/2 > 1.

Thus every frozen trace exponent q<=2 misses the required threshold even
after importing the collision-survivor factor.  Round 61's
q_col=806.0249... is an Orlicz moment exponent for the different random
variable w_Z^(r_K) on the owner law; it is not a trace RN-density exponent
and cannot be substituted across types.

## 4. Every positive sector needs its own Feynman--Kac drift

For each active-clock, raw-Z, Orlicz, complement, variation, common-mode
and cemetery sector with positive charge H, a base trace drift must be
supplemented by

    P_j H_(j+1) <= kappa_H H_j,       w_Z kappa_H<1.

A base mass estimate alone is insufficient.  Take

    w=3/2,  mu_j=3^(-j),  H_j=2^j/(j+1).

Then

    sum_j w^j mu_j=sum_j 2^(-j)=2,

while

    sum_j w^j mu_j H_j=sum_j 1/(j+1)=infinity.

No signed cancellation can pay the positive common mode.

There is also an upstream obstruction before any kappa is estimated:
fixed-j complement/variation/common-mode costs are finite, but the actual
raw-Z/power-Orlicz right side may still be infinite and the positive
pre-cemetery slice law has not been materialized.  Thus the unified finite
positive Lambda_j itself is not yet available.

## 5. Small gaps and cemetery

The remaining exact-cut set is first split into six same-law coded families:
chart/atlas, homogeneity, hole/cemetery boundary, owner tie/change,
non-source endpoint, and later-word singularity/pullback.  Positivity gives
zero charge on their countable union if and only if every coded row has
zero charge.  Absolute continuity from nu_j to the orientation-cost law
only transfers a proved nu_j-zero row forward; it does not prove any of
these six missing source rows.

Let G_j be the infimum of all registered positive gaps and

    Y_j=ceil(log_2^+(1/G_j)).

Use the extended value Y_j=infinity when G_j=0.  Equivalently,

    A_(j,k)={every individual gap is positive, G_j<=2^(-k)}

decreases to N_acc; one must not insert 0<G_j in this definition.

For a>0, the joint same-law condition

    sum_j w_Z^j integral 2^(aY_j) d chi_j < infinity

simultaneously kills the accumulation set G_j=0 and gives the Markov tail

    chi_j(Y_j>=k)
      <=2^(-ak) integral 2^(aY_j)dchi_j.

Fixed-j positivity is not enough.  In the exact test model w=3/2, a=1,
gap_j=2^(-j), and mass_j=3^(-j)/(j+1), every layer has a positive gap and
no accumulation atom, but its weighted charge is 1/(j+1) and diverges.

A positive cemetery must also be a one-shot arrival ledger.  If a positive
kill is represented as absorbing occupancy and counted on every later time
slice, its w_Z-weighted sum diverges for w_Z>1.  Live conditional drift may
pay arrivals; the pre-regularization cemetery remains outside that law.

## 6. Signed flux does not determine positive orientation cost

After a tag-preserving p-to-j crosswalk T has been supplied, every positive
pair on the common carrier has the unique decomposition

    (mu^+,mu^-)=(J^+ + lambda, J^- + lambda),
    J=mu^+-mu^-,      lambda=mu^+ wedge mu^-.

Exact alignment is T_*mu^+=xi^f and T_*mu^-=xi^r, equivalently both
signed-law equality and common-mode equality on that typed carrier.
A weaker lawful domination requires bounded RN rows

    T_*mu^+ <= C_f xi^f,       T_*mu^- <= C_r xi^r,

and only yields

    |T_*J| <= C_f xi^f+C_r xi^r.

It is not Jordan alignment or positive F10 without separate charge
compatibility.  Signed equality alone is insufficient: the one-point
pairs (1,1) and (M,M) both have signed law zero for arbitrary M, but their
positive totals and common modes differ without bound.

The frozen Round-54 physical hit/miss flux and Round-61 orientation-cost
pair have no certified common carrier pushforward, RN domination, or
common-mode identification.  Round 63's cost-Jordan identity therefore
cannot be promoted to the physical Jordan law.

## 7. Five suffix bits remain independent

Fix the two certified suffix predicates to true.  A 32-atom standard-Borel
cube realizes all 2^5 assignments of the remaining five predicates.  Hence
Borel typing plus the first two truths implies none of the remaining five,
and it does not imply the independent numerical inequality R>=r_K.

Lexicographic first-failure cells give the exact disjoint compression

    {R<r_K}=disjoint_union_(b,s)(F_(b,s) intersect {b<r_K}).

Universal R>=r_K is equivalent to every such cell being empty.  A drift
bound can pay positive charge on cells; it cannot prove their emptiness.

## 8. Strict frontier

    owner-lineage kernel iff criterion:             CERTIFIED_EXACT
    minimum coefficient c_*:                       CERTIFIED_EXACT
    singular/stationary separators:                 CERTIFIED_EXACT
    actual cross-j label marginal contraction:      NOT_CERTIFIED
    fibre Lyapunov/nonuniform criterion:             CERTIFIED_EXACT

    trace critical exponent q_trace^*>2:            CERTIFIED_EXACT
    q_col-to-trace substitution:                    CERTIFIED_FALSE
    remaining N_cut six-family zero rows:           NOT_CERTIFIED
    sectorwise positive Feynman--Kac rows:           NOT_CERTIFIED
    unified finite positive slice before drift:      NOT_CERTIFIED
    same-law all-time small-gap charge:              NOT_CERTIFIED
    one-shot pre-regularization cemetery:            NOT_CERTIFIED

    signed-plus-common Jordan bridge:                CERTIFIED_EXACT
    Round54/Round61 carrier/common-mode alignment:   NOT_CERTIFIED
    suffix typing / values:                          7/7 / 2 true + 5 open
    physical R>=r_K:                                 NOT_CERTIFIED

    Gate-5 maturity / complete blocks:               10/18 / 0
    complete composite gates:                        0/5
    CM2:                                             NO-GO_FOR_CLAIM

The latest small-hole response, operator-renewal and signed-transport papers
do not supply this immutable owner-trace marginal contraction or the
positive common mode.  No external theorem is promoted.

## 9. Executable evidence

The producer and independent verifier pin the full frozen chain, replay the
finite label kernels, critical trace exponent, Feynman--Kac and small-gap
harmonic separators, cemetery occupancy, Jordan common mode and all 32
suffix atoms, regenerate canonical JSON byte-for-byte, reject hostile
semantic/strict-JSON mutations, and fail closed by default with exit 2.
