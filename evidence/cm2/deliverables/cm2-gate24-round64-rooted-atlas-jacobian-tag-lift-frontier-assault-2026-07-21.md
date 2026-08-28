# CM2 Round 64 Gate 2/4 — rooted atlas, Jacobian bridge and tag-lift frontier

Date: 2026-07-21

Strict verdict: **Gate 2 remains 0/17; Gate 4's landing join remains 1/7
with fields 1, 4 and 7 partial.  Gate 2 and Gate 4 remain NOT_CERTIFIED,
complete composite gates remain 0/5, and CM2 remains NO-GO_FOR_CLAIM.**

## 1. Frozen scope

This append-only leaf pins the Round-63 aggregate root, independent audit,
Round-63 Gate-2/4 leaf, and the Round-62 actual branch-covariance graph
manifest.  No older artifact is edited.

## 2. Exact bridge from conditional RN data to arclength

Let h send a source plaque to a landing plaque.  Write rho_u and rho_v for
the conditional reference densities with respect to adapted arclength,
J for the measure-holonomy Radon--Nikodym factor, and
lambda=dh/ds for the metric derivative.  Change of variables gives the
exact compatibility row

    J(hx) rho_v(hx)=rho_u(x)/lambda(x),
    lambda(x)=rho_u(x)/(J(hx)rho_v(hx)).

If the marker has zero stable defect, its arclength density obeys

    psi_v(hx)=psi_u(x)/lambda(x).

Suppose

    a_u<=rho_u<=b_u,  a_v<=rho_v<=b_v,  j_-<=J<=j_+.

Then

    a_u/(j_+ b_v) <= lambda <= b_u/(j_- a_v).

Substitution into Round 63's sharp landing budget

    F R M < C_p m^2 theta L

produces the equivalent sufficient condition

    F R b_u j_+^2 b_v^2
      < C_p j_- a_v a_u^2 theta L.

This bridge prevents measure-Jacobian and metric-derivative rows from being
silently conflated.  None of the six physical density/Jacobian bounds is
materialized on the frozen common landing law.

## 3. Countable rooted plaque atlas

Let plaque 0 be a root and P_i positive L1 holonomy isometries from the root
to plaque i.  For weights w_i>0 summing to one and markers g_i, assume

    sum_i w_i ||P_i^(-1)g_i||_1 < infinity.

Put h_i=P_i^(-1)g_i.  Tonelli and the scalar weighted-median theorem give

    delta_atlas
      =inf_f sum_i w_i ||g_i-P_i f||_1
      =integral inf_t sum_i w_i |h_i-t| dmu_0.

The infimum is attained by a measurable pointwise weighted median.  It is
zero exactly when all pulled-back markers agree almost everywhere.

If

    P=sum_(i<k) w_i w_k ||h_i-h_k||_1,

then pointwise symmetrization gives the sharp sandwich

    P <= delta_atlas <= 2P.

Under a branch--holonomy commuting tree, the dynamic transfers are L1
isometries and the source and landing atlas distances are exactly equal.
Commuting squares transport the full many-plaque saturation debt; they
still do not force it to vanish.

For a two-atom root law, weights (1/5,1/2,3/10), and pulled-back markers

    (0,1), (1,3), (4,0),

the coordinate median costs are 11/10 and 13/10.  Hence

    delta_atlas=6/5,    P=3/4,

which strictly realizes P<delta_atlas<2P.

## 4. Actual graph tag lift and the missing strong bound

The pinned Round-62 bad-graph branch law has the typed form

    Gamma_B=L_K kappa_B,        pi_# L_K nu=nu.

The unweighted lift preserves total variation.  For graph weight 2^D set

    W_D(x)=integral 2^(D(z)) K_x(dz).

Then for positive nu, and by polar decomposition for signed nu,

    ||L_K nu||_(X_D)=integral W_D d|nu|.

Consequently

    L_K:L1(kappa_B)->X_D^graph is bounded
      iff W_D belongs to L-infinity(kappa_B),

and its norm is the essential supremum of W_D.  The frozen actual input
only controls one integrated vector; it does not give this operator bound.

The exact separator uses kappa_n=3*4^(-n), D(n)=n and a deterministic tag
kernel.  Its one-vector moment is

    sum_n kappa_n 2^n=3,

but W_D(n)=2^n is unbounded.  Unit-L1 atoms have lifted norms 2^n, proving
that one finite moment cannot be promoted to a bounded strong lift.

## 5. Strict frontier

    conditional-density/J/metric bridge:          CERTIFIED_EXACT
    rooted countable weighted-median formula:      CERTIFIED_EXACT
    pairwise-dispersion sandwich:                  CERTIFIED_EXACT
    source/landing atlas equality under squares:   CERTIFIED_CONDITIONAL
    actual stable root/edges and zero defect:       NOT_CERTIFIED
    actual F,R,theta,L and density/J bounds:        NOT_CERTIFIED

    actual tagged graph covariance:                CERTIFIED_PINNED
    weighted tag-lift iff criterion:                CERTIFIED_EXACT
    finite-moment/unbounded-operator separator:     CERTIFIED_EXACT
    physical anisotropic/Piola strong lift:         NOT_CERTIFIED

    Gate 2 official fields:                        0/17
    Gate 4 landing join:                           1/7; fields 1,4,7 partial
    Gate 2 / Gate 4:                               NOT_CERTIFIED
    complete composite gates:                      0/5
    CM2:                                           NO-GO_FOR_CLAIM

The current literature boundary is unchanged.  The local product structure
in arXiv:2604.25881v1 is for the unique MME built from symbolic Hausdorff
measures, not the collision-SRB owner law pinned here; arXiv:2606.10155v1 is
a review.  Neither result is promoted.

## 6. Executable evidence

The producer and independent verifier pin all frozen roots, replay the
Jacobian substitution, weighted medians and pairwise dispersion, the graph
moment and unbounded atomic norms, deterministic canonical re-emission,
hostile semantic and strict-JSON rejection, and default fail-closed exit 2.
