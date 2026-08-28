# CM2 Round 64 Gate 1/3 — resonant tails, transport current and clock frontier

Date: 2026-07-21

Strict verdict: **Gate 1 and Gate 3 remain NOT_CERTIFIED.  No composite gate
is closed and CM2 remains NO-GO_FOR_CLAIM.**

## 1. Frozen scope

This leaf is append-only from the frozen Round-63 root.  It pins the Round-63
aggregate and recursive ledger, the independent audit and its ledger, and the
Round-63 Gate-1/3 manifest and ledger.  No older artifact is edited.

The new result is a quantifier correction and a genuine weakening of one
Gate-3 current ledger.  It does not materialize a moving billiard atlas,
anisotropic Piola map, or an all-plaque third gauge.

## 2. Gate 1: zero tails cannot create twisting

Keep the convention

    B(x)=C(fx)^(-1) A(x) C(x)

and the finite endpoint identity

    H_B^s(x,y;n)
      =C(y)^(-1)[H_A^s(x,y;n)+Delta_n^s(x,y)]C(x),

with the analogous unstable formula.

Round 63 used uniform zero-tail convergence as a sufficient interface for
Hölder inheritance.  That interface is valid for regularity, but it is too
strong for the missing twisting.  If the faithful diagonal class-H
representative has a zero canonical loop and both renormalized defects tend
to zero, the limiting loop is only conjugated and stays zero-twisting.
Conjugacy cannot manufacture a nonzero axis wedge.

The correct resonant-tail interface allows uniform Hölder limits

    Delta_n^s -> L_s,        Delta_n^u -> L_u.

Then

    H_B^s=C(y)^(-1)(H_A^s+L_s)C(x),
    H_B^u=C(y)^(-1)(H_A^u+L_u)C(x).

At a homoclinic base point p the loop is

    C(p)^(-1)(H_A^s+L_s)(H_A^u+L_u)C(p).

Thus the missing row is not merely decay: it is one all-plaque, two-sided,
uniform Hölder resonant-tail registry whose limiting loop has the selected
nonzero twisting token.

An exact critical model takes

    A=diag(2,1/2),  H_A^s=H_A^u=I,
    L_s=-E_21,      L_u=E_12.

The loop before outer conjugacy is

    (I-E_21)(I+E_12)=[[1,1],[-1,0]],

has determinant one, and has nonzero wedge -1 on both coordinate axes.
With L_s=L_u=0 the same canonical loop is I and both wedges vanish.  This is
a logical sharp separator, not an actual billiard third gauge.

## 3. Gate 3: replace raw endpoint TV by transport cost

For positive endpoint traces alpha delta_y and beta delta_z, the
bounded-Lipschitz dual norm obeys

    ||alpha delta_y-beta delta_z||_(BL*)
      <= |alpha-beta|+min(alpha,beta) min(2,d(y,z)).

The bound follows by separating the mass mismatch and transporting the
common mass.  It is strictly weaker than raw endpoint total variation.

For alpha=beta=1, y=0 and z_n=2^(-n), every nonzero raw-TV row costs 2, so
the all-depth raw-TV sum diverges.  The transport rows cost at most 2^(-n)
and sum exactly to 1.  Hence a physical landing-distance/speed ledger could
pay endpoint motion even when the raw endpoint-TV ledger cannot.  The
frozen inputs contain no such same-ID all-depth physical ledger, so this is
an exact improved interface rather than a Gate-3 closure.

## 4. Clock coboundary and moving-null separator

For a one-step operator P and integers r'<r excluded, the clock jump has the
exact telescoping expansion

    P^(r')-P^r
      =sum_(k=r)^(r'-1) P^k(P-I).

The safe clock has

    Dbar(M)=0                   for M<=310,
    Dbar(M)=M-309               for M>=311,
    R0=696 Dbar.

Thus its first jump contains 1392 one-step coboundaries and every later
unit-M jump contains 696.  This re-expresses the sixth clock debt in a
single dyadic level-trace/coarea ledger; it does not bound that ledger in
the physical strong norm.

Fixed-time null mass also cannot erase a moving current.  For

    mu_s=1_[s,1] dx

the moving endpoint has zero Lebesgue mass at s=0, but

    d/ds mu_s at 0 = -delta_0

as a distribution.  The same logical issue applies to grazing and cemetery
boundaries.

Finally, a lawful strong assembly must retain both product rules

    D(QPR)=(DQ)PR+Q(DP)R+QP(DR),
    D(T^n)=sum_(k=0)^(n-1) T^(n-1-k)(DT)T^k.

The frozen chain supplies neither bounded differentiable physical R_s/Q_s
nor the required anisotropic Piola and MT_DQ maps.

## 5. Strict frontier

    Gate-1 resonant-tail identity:                 CERTIFIED_EXACT_INTERFACE
    zero-tail twisting shortcut:                  CERTIFIED_FALSE
    critical SL(2) separator:                     CERTIFIED_EXACT_LOGICAL
    actual all-plaque nonzero tails/Hölder:        NOT_CERTIFIED
    same representative class-H plus twisting:    NOT_CERTIFIED

    endpoint BL* transport bound:                 CERTIFIED_EXACT
    raw-TV versus transport separator:             CERTIFIED_EXACT
    safe-clock closed form/coboundary counts:      CERTIFIED_EXACT
    physical all-depth landing transport ledger:  NOT_CERTIFIED
    clock/cemetery strong trace sum:               NOT_CERTIFIED
    anisotropic Piola, R_s/Q_s, MT_DQ:             NOT_CERTIFIED

    Gate 1 / Gate 3:                              NOT_CERTIFIED
    complete composite gates:                     0/5
    CM2:                                          NO-GO_FOR_CLAIM

Latest-paper checks remain nonpromoting: arXiv:2604.19671v2 concerns a
shrinking boundary hole and conditional survival, while arXiv:2606.10155v1
is a transfer-operator review.  Neither supplies the moving-scatterer
resonant-tail registry or finite-parameter current/Piola assembly used here.

## 6. Executable evidence

The companion producer and independent verifier pin the frozen root, replay
the matrix loop, all transport rows, safe-clock closed form, coboundary
counts and product-rule arities, regenerate canonical JSON byte-for-byte,
reject hostile semantic and strict-JSON mutations, and fail closed with
default exit code 2.
