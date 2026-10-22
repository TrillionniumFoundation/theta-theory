# Author verification: normalized physical source, singular volume and optical pressure

This document records an author-side mathematical reconstruction of the
complete drafts 312 and 313. It supplements
`AUTHOR_MATHEMATICAL_CHECK_310_311.md`. It is not a new referee report or an
independent human expert's certification. The associated deterministic
verification outputs identify the exact native source hashes checked.

## 312: the normalized exceptional source

The source remains the restriction of the actual original collision
probability to its original exact event, then pushed by the original full
physical clock. The finite-overlap atlas is used to bound the optical weight
of all contributing trajectories by positive volume of nearby trajectories
which still have all their actual first-hit collisions.

For a witness of depth `d`, the atlas widening is
`2 C_Delta a_epsilon sigma^d` for clearance and
`2 C_c a_epsilon sigma^d` for incidence or section collar. These are one
sixteenth of the corresponding diameter constants in 310 because
`a_epsilon=s_epsilon/8`. Thus 310's uniform rational depth certificate
applies to every atlas widening without increasing the original widths.
The enlarged widths appear exclusively in a proved positive upper bound.

There are at most two true contacts or flights of a given depth. In the
incidence term this count and the exact inequality
`(u+v)^2 <= 2u^2+2v^2` give
`2 * 2 * (2 C_c a_epsilon)^2 = 16 C_c^2 a_epsilon^2`.
The six terms of the displayed budget `V_epsilon(D)` have the correct
clearance, incidence, and section probability factors. In particular the
section factor is `1/pi` after its two depth occurrences, and the
conditioned source is not paid a second time in this physical volume.

The actual multiplier satisfies the half-guard bound
`I_m <= H_epsilon = 1+(4/epsilon)q0^(3/4)/(1-q0^(3/4))` on the full
atlas tubes. The stated constant also dominates the slightly smaller
constant needed on the original full-guard source. Hence insertion of the
actual `I_m` into the exceptional bulk source requires precisely a fixed
`H_epsilon` factor and no marked-pressure theorem.

At `D_m=ceil(theta m)`, the floor convention gives
`j(D_m)>=theta m/N-2`. Consequently the slowest observation term decays
at rate at least
`lambda_b=theta min(|log(q_a)|/(4N),|log(sigma)|)>0`.
The estimates hold at every finite `m,D` before this substitution; the
small initial counts below the explicit certified depth do not affect the
collision limit. Every other outer width remains fixed.

## 312: exact physical marks, clock and Fourier comparison

All actual central marks are inherited from the proved complete geometric
theorem 309, on the complement of its original exceptional source. The
comparison retains both central endpoint section tests and the half-open
occupation range `[d,m-d)`. The two lattice coordinates and the number of
actual flights are exactly unchanged. The global comparison minimum need
not be physical at its full end portions; the theorem only assigns a
physical trajectory to its proved central record.

The exact clock relation is `L_d(Y)=L_d(Q)+W_d+T_clock,d`, with the
nonnegative clock cost controlled by the anchor contraction. Its necessary
Fourier correction is therefore **`exp(-i s W_d)`**:

`exp(-i s W_d) exp(i s L_d(Y))
=exp(i s L_d(Q)) exp(i s T_clock,d)`.

The opposite sign would leave an extra `2sW_d`; it is explicitly rejected
by the symbolic check. The error on the good source has modulus at most
`|s|T_clock,d`. On the exceptional source the comparison coefficient is
zero and the actual coefficient has modulus at most one, so that source
is paid by the newly proved positive original-roof density. This defines a
comparison coefficient, not a fictitious physical trajectory or a new
observational law.

The pointwise clock, phase and transverse costs are bounded before any
pushforward. The uniform full guarded source height from 311 therefore
pays them on the original full clock without the old whole-cylinder
pressure premise. Their rate is
`lambda_c=theta |log(q_a)|/N`. The exceptional contribution is independent
of all twists. The allowed physical frequency range
`|s|<=exp(lambda m)`, `lambda<lambda_c`, only multiplies the clock cost;
it does not multiply the separate exceptional-source bound. The proof
correctly distinguishes these two rates and does not integrate an
unbounded Fourier range.

The central coefficient is unambiguous because the active central
geometry agrees for every global minimum. At fixed radius and finite
collision count, a selection of one minimum for each finite word is
another Borel way to express it. Both end portions of the original
record remain in the full roof, full original event and their exact
phase factors throughout.

## 312: the actual inverse-gradient singular volume

The identity `|grad_q F|=R |zeta|` fixes the radius factor. On
`|zeta|>=rho`, the original insertion is bounded by
`H_epsilon/(R_minus rho)`, so the full guarded roof-density estimate
gives exactly the first term of the claimed integral bound.

For every word having a selected point with `|zeta|<rho`, the physical
inverse ball of radius `4rho` about that point's momentum contains the
whole disk `B(0,2rho)`. The actual inverse there yields a true regular
critical center. Equal-momentum uniqueness on the entire physical word,
not an unproved connectedness assumption, makes the origin-centered
inverse the same one for every selected point of this word.

These critical tubes are disjoint across different words because the
same physical initial state cannot have two distinct full lifted words.
Their overlap factor is therefore one. Each tube lies in the enlarged
actual witness event `E^+`: it is constructed in the chosen physical
endpoint ball around a selected point, and its full endpoint diameter is
within the proved widening allowance. Exact unconditioned tube volume
and two-sided optical distortion give
`sum u_w(0) <= C_dist nu(E^+)/rho^2`.

Along a physical momentum ray the exact bound `h<=2R_plus` gives
`0<L_w(r e_theta)-a_w <= R_plus r^2`. Consequently

`1/(Rr) <= sqrt(R_plus)/(R_minus sqrt(t-a_w))`.

The inequality is in this direction; the original physical critical
roof `a_w` is retained separately for each word. Combined with radial
coarea and its `2pi` angular integral, the density envelope has coefficient

`H_epsilon U C_dist sqrt(R_plus)/(2 c_star R_minus)`

times `sum u_w(0)(t-a_w)^(-1/2)1_{t>a_w}`. The complete word sum has
already been bounded by physical volume, so no word cardinality enters.
Its roots need not share a physical roof or the same momentum radius.

For any Borel roof set of finite measure `ell`, layer cake gives the exact
uniform inequality

`integral_I (t-a)_+^(-1/2)1_{t>a} dt
<= integral_0^infinity min(ell,v^(-2)) dv = 2 sqrt(ell)`.

This includes `ell=0` by direct evaluation of the zero upper bound.
The resulting factor of two cancels the displayed denominator two and
produces precisely
`H_epsilon U C_dist^2 sqrt(R_plus)/(c_star R_minus rho^2)`.
The near-critical term has one additional physical `R_minus^(-1)`;
neither an extra source conditioning factor nor a missing momentum-disk
area remains.

Truncation of the nonnegative weight and monotone coarea show absolute
continuity and local integrability of this weighted original-roof
measure. The estimate permits square-root singularities at critical
roofs and makes no false assertion of a bounded pointwise inverse-gradient
density there. The finitely many regular critical source points have
zero collision area; this does not imply that a separate paired trace
has zero mass.

The full true physical roof is supported in an interval of length at
most `m(28/5-3/50)=277m/50`. Thus the total singular volume has at most
`O(m+sqrt(m))` additional window loss. Its positive exceptional-source
factor still decays exponentially, so multiplication by `m^2` tends
to zero uniformly in the claimed original variables. This is an
interior volume payment. A boundary term can use it only through an
independently proved inequality charging that same source.

## 312 and 313: actual optical normalization and guarded pressure

The two endpoint Jacobians give the exact identity
`u=R^2 omega/det(G)`. The physical endpoint Schur bound yields
`det(G)<=R^4 U^2`, so `omega<=R_plus^2 U^2 u`.
The actual stable-arclength comparison proved in 313 gives
`j_m<=30000 omega/c_m`. On the guarded source its endpoint cap
implies `c_m>1/2`, hence
`j_m<=60000 R_plus^2 U^2 u`.

For each word, the covering tubes and their upper optical distortion
bound its stable-Jacobian supremum by the sum of its tube-center
weights, whether or not the supremum is attained. The total center
sum is at most `25 C_dist/rho^2` by unconditioned physical volume and
the already proved finite overlap. Therefore the exact pressure
coefficient is `60000*25=1,500,000`. No `c_star` occurs in this
unconditioned pressure bound. The sum uses all physically realizable
words and the true stable norm. It remains explicitly restricted to
the fixed original guard and endpoint cap.

The full 313 proof was reconstructed separately. The physical derivative
has the scalar sign `-M`; its positive matrix has determinant `c/c'`.
The slope map sends the specified positive cone into itself and has
contraction at most `47/48`, uniformly over the true physical flight
range. Backward regularity defines the unstable line; reversal defines
the stable line. The exact invariant-area identity gives true Euclidean
stable contraction, including the incidence-ratio cancellation.

The column comparison uses fixed inequalities preserved by positive
left multiplication. It introduces no constant raised to collision
count. The exact optical conjugacy has the correct order
`B_{i+1}M_iB_i^{-1}=C_{i+1}S_i`; all intermediate coordinate factors
telescope. The original endpoint inverse derivative is
`omega=R c_0/b_m`, with only one radius factor. The final exact ratio
is

`omega/(c_m j_m)=R (u_m/b_m) e(T^m x)/e(x)`.

The displayed rational inequalities give constants 30000 and 6400.
The `M_R'` set has full invariant collision measure by countable
regular changes of variables and the actual one-step singular sets.
This is a bulk measure statement, not a claim about singular traces.

## Executed checks and their limits

`check_physical_source_height.py` supports the validator's `--details`
interface and raises explicit runtime exceptions on failure; Python
optimization cannot disable its checks. Normal and `-O` runs both passed
with identical deterministic JSON, including the source hashes.

Checks include exact rational physical caps and inverse-ball margins,
the continuous interval argument behind overlap 25, 121 rational grid
boundary illustrations, 33,408 central index cases with 128 retained
singletons and 16,768 empty ranges, all 94 partial anchor blocks, 3,072
floor/ceiling cases, and symbolic Jacobian, singular layer-cake,
Fourier-sign and pressure-normalization identities. These are auxiliary
verification of the written all-source proof, not a simulation claimed
to prove continuum dynamics.

The original full normalized shortage remains open outside the stated
guarded source and on its unpaid shallow comparison/capacity terms.
The proofs do not exchange the collision limit and the outer `B` limit,
exhaust the zero-margin complement uniformly, claim unrestricted
whole-cylinder pressure, or finish the full spectral/arithmetic raw
pointwise inversion theorem.
