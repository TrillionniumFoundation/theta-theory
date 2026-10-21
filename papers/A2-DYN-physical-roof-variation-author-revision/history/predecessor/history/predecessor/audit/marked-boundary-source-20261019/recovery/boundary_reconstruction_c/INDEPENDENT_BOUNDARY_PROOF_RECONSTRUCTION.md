# Independent mathematical reconstruction of native author module 317

This is an internal reconstruction of an author proof, not a referee report,
external expert certification, or a decision about publication. The exact
source and dependency identities, execution times and auxiliary run receipts
are recorded in `INDEPENDENT_RECONSTRUCTION_RECEIPT.json`.

## Conclusion and scope

The displayed mathematical mechanism in module 317 is valid on its explicitly
defined physical source. I independently reconstructed the positive boundary
flux identities, the foot-split optical determinant and Wronskian, the common
formal gradient disk, the signed-clearance derivative estimates, the quadratic
Euler cancellation, and the summation on the actual marked angular source.
No correction of a mathematical constant, radius factor, derivative order or
quantifier was necessary in the examined consolidated draft.

The strongest new conclusion is a uniform bound for the positive physical
boundary-curve charge on **covered critical zero-offset clearance pieces**.
Its constant is independent of the actual collision count, word, retained
labels, radius and size or connectedness of the selected physical pieces.
This class is geometrically specified by a limiting physical critical word,
zero clearance offset at that word, and agreement of all contacts with its
common formal inverse. The theorem does not prove that every near-critical
physical boundary piece belongs to that class. It does not remove the actual
nonzero critical offset, a section/pairing boundary term, or the incoming
critical fan at zero endpoint gradient. These are real remaining interfaces.

The proof also gives an exact all-regular-word optical identity. Neither this
identity nor the covered-boundary estimate proves the whole pressure sum, an
essential-height bound for all original positive sources, the raw pointwise
local limit theorem, or the four-coordinate inverse theorem. The draft keeps
those distinctions explicit.

## 1. Physical coordinates and the two boundary Jacobians

Write `g = grad_q F`, `G = D_q^2 F`, `z = |g|`,
`e = g/z` and `chi = e_perp^T G e_perp`. In the inherited endpoint angles,
`g = R(-p_0,p_m)`. The actual marked chart is `q = Q(vartheta,u)`, where
`u` is the line clearance of a specified nonincident disk and the foot is not
a collision. Its full physical line measure is

\[
  d\nu_R=(4\pi R)^{-1}\,d\vartheta\,du.
\]

The original conditioning contributes exactly one factor `c_*^{-1}`. All
initial/terminal section tests, lattice and occupation labels and roof tests
remain selector weights; none becomes a new normalization.

The inherited Gauss determinant is

\[
 |\det D_{(\vartheta,u)}(F,\theta)|=\chi/(R\omega).
\]

For a two-by-two matrix with rows `(S_vartheta,S_u)` and
`(theta_vartheta,theta_u)`, the lower left entry of its inverse is
`-theta_vartheta/det`. Therefore the original positive trace coefficient
satisfies precisely

\[
 \frac{\omega W^\varepsilon}{4\pi c_*\chi}
       |\theta_\vartheta|\,d\vartheta
 =\frac{W^\varepsilon}{4\pi Rc_*}
       |u_t|_{\theta}\,d\vartheta.
\]

For the specified section coordinates `(v,b)=(p_i,alpha_i-a)` or
`(alpha_i,p_i-a)`, collision-area invariance instead gives density
`(4 pi c_*)^{-1}` and determinant `chi/omega`. The corresponding identity
has no factor `R^{-1}`. Thus the two formulas are consistent with each other
and with their different source coordinates.

The argument concerns positive measures on already defined boundary germs.
Countably disjointizing monotonicity intervals of the boundary-to-angle map
preserves the full multiplicity. The image of its zero-derivative set is null
for one-dimensional Lebesgue measure, by the elementary `C^1` one-dimensional
area argument. This gives the stated positive trace formula without requiring
global monotonicity. It does not manufacture a one-sided trace for an arbitrary
Borel function. The original bad weight is retained; in particular it is one
at zero unvisited clearance.

For a positive level `u_0`, the selected side is part of the assertion. A
second incident side produces a second positive charge and must be added.
At zero unvisited clearance the prescribed physical side is `u>0`. This
convention prevents an implicit doubling or cancellation of two charges.

## 2. Normal speed, the truncated estimate and the local germ

Differentiating `g=ze` while keeping `e` fixed gives

\[
 \left.\frac{dq}{dt}\right|_\theta
 =\frac{G^{-1}e}{z\,e^TG^{-1}e}
 =\frac{G^{-1}g}{g^TG^{-1}g}.
\]

The inherited positive Hessian bounds imply the stated
`Lambda_circ/(lambda_circ z)` norm bound. The individual signed line clearance
is controlled by the same segment Hausdorff derivative argument as the least
clearance. Combining its `2 C_Delta sigma^d` depth bound with
`z=R |(p_0,p_m)|` produces exactly the denominator `R_- r` in the speed bound.
The radius already present in the line density remains separate.

For the complete angular measure, native 316 gives
`A(s) <= 2 H_nm s`, where `A(s)` is the mass with `r<s`. For `s>1` this
follows by intersecting the momentum interval with `(-1,1)` and then using
`2 H_nm <= 2 H_nm s`. Both endpoint times are legitimate positive collision
counts: the backward count at the initial endpoint is `j+1`, including `j=0`.
No independence between endpoint momenta is used. Tonelli applied to

\[
 r^{-1}=L^{-1}+\int_r^L s^{-2}\,ds,\qquad L=\sqrt2,
\]

gives the displayed logarithmic bound on `r>=rho`. Multiplying the factors
`(4 pi R_- c_*)^{-1}`, `2 C_Delta Lambda_circ/(lambda_circ R_-)`, and
`2 H_nm` reproduces `C_bf` exactly. A complete source bound outside a critical
core is not a bound inside that core; the draft explicitly retains the latter.

For a `C^2` nongrazing boundary germ through a critical point,

\[
 g(s)=as+\tfrac12bs^2+o(s^2),\qquad
 g'(s)=a+bs+o(s),
\]

so the angular numerator is
`det(g,g') = det(a,b) s^2/2 + o(s^2)`. Positive definiteness gives `a!=0`.
Dividing by `|g|^2` proves the finite angular derivative limit, with the factor
`1/2`. The optical trace density and `chi` have the designated physical
one-sided limits. The two antipodal Gauss limits have the same quadratic
Hessian denominator. This is a curve trace, not the angular coefficient of
a two-dimensional incoming critical fan.

For the local quantitative version, `|g''|<=L_G` and `|g'|<=Lambda_circ`
give `|g(s)|>=lambda_circ |s|/2` on the stated interval. Writing the angular
numerator as the integral of `det(g'(v),g'(s)-g'(v))` bounds it by
`Lambda_circ L_G s^2/2`. The displayed bound
`2 Lambda_circ L_G/lambda_circ^2` follows. A boundary curvature allowance
must be established on that actual germ; no uniform curvature assertion is
silently used in the later zero-offset theorem.

## 3. Independent derivation of the foot-split optical identity

At an incoming collision write the true velocity as `v^-=-c n+p t`, with
`t` the counterclockwise unit tangent. A displacement `delta q=t delta s`
has incoming transverse component `J=-c delta s`. Differentiating
`p=v^- dot t` and `dt/ds=-kappa n` gives

\[
 \delta p=-c\,\delta\vartheta^-+\kappa c\,\delta s
          =-(\kappa J+cJ').
\]

Both transverse coordinates reverse sign together when the reflection is
unfolded. This yields a single sign for an entire endpoint derivative row,
not separate freely chosen signs for its two columns.

At the marked foot `-sigma(R+u) v_vartheta^perp`, the angular derivative of
position is longitudinal. The forward angular field is consequently `(0,1)`
and its clearance field is `(-sigma,0)`. The backward ray has angle
`vartheta+pi` and transverse frame `-v_vartheta^perp`, so its two fields are
`(0,1)` and `(sigma,0)`. Time reversal also negates the endpoint momentum,
which changes the whole backward row by one sign.

Propagating to the incoming side of each endpoint with the actual matrices
`P` and `K` therefore gives

\[
 D(p_0,p_m)=
 \begin{pmatrix}
  s_0 A_-^p&\sigma s_0 B_-^p\\
  s_m A_+^p&-\sigma s_m B_+^p
 \end{pmatrix}.
\]

The endpoint reflection is correctly excluded from each incoming-side
product. Taking the determinant gives its sign times the **positive sum**
`A_-^p B_+^p+B_-^p A_+^p`. Thus the two rays cannot cancel this determinant.

For a half-product `M=L P(a_foot)` put `(X,Y)=(kappa,c)L`. Then
`B^p=X`, `A^p=a_foot X+Y`, and

\[
 h=\frac1{a_{\rm foot}+Y/X}.
\]

For one collision `Y/X=c/kappa<=R_+`. For two or more collisions, the
rightmost factor of `L` is the first physical reflection kick. If its preceding
row is `(x,y)`, that kick sends it to `(x+y k_1,y)`. Hence
`Y/X<=1/k_1<=R_+/2`. The standoff and true horizon then prove the displayed
uniform ratio bounds. No upper bound on a grazing kick is needed.

The same unconditioned collision measure has endpoint-momentum density
`u_x/(4 pi)`. Comparing this with the line density gives

\[
 u_x=\frac1{R A_-^p A_+^p(h_-+h_+)}.
\]

The angular numerator is
`|p_0 s_m A_+^p-p_m s_0 A_-^p|/r^2`. Dividing by the two half-products
produces exactly the signed Wronskian in the draft. In particular its
numerator is `s_m p_0/A_-^p-s_0 p_m/A_+^p`.

Finally `det D_q(p_0,p_m)` has absolute value `det G/R^2`, so
`u_x=R^2 omega/det G`. With `h_x=R^2 chi/det G`, one gets
`f^epsilon=W^epsilon u_x/(4 pi c_* h_x)`. The metric `h_x` is thus different
from either half-ray ratio. There is one factor of `c_*^{-1}` and precisely
the single line-coordinate radius factor. The retained signed expression is
useful information; its two terms cannot simply be bounded independently
and then used to claim critical cancellation.

## 4. Complex domain and the uniform real inverse

The inherited analytic reflection theorem applies also at a fixed-word
one-sided grazing limit. At the chosen closed physical critical reference,
all flight lengths still exceed the common positive minimum and the analytic
reflection inverse has its original weighted bound. This is a statement
about the same reflection equations, not a claim of physical continuation
through grazing.

On `|h_0|,|h_m|<eta/4`, the inherited weighted contact bound is
`P(|h_0|+|h_m|)<P eta/2=r_*/8`. For the two complexifications `X^+` and
`X^-` of a flight, each relative perturbation is at most one quarter. Thus
both magnitudes lie between `3 tau/4` and `5 tau/4`. On the fixed square-root
branch, the magnitude of the analytic length is at least `3 tau/4`. The
complex Euclidean norm of the unit direction is bounded by `5/3`; explicitly
its square is

\[
 \frac{|X^+|^2+|X^-|^2}{2|X^+X^-|}\le25/9.
\]

The circular normal/tangent norm is less than two on the inherited contact
ball. Therefore each holomorphic endpoint gradient component has magnitude
at most `4 R_+`. This uses the first variation of the endpoint action and
interior stationarity, and avoids a bound proportional to total action or
collision count. The same identity follows directly from the analytic
reflection equations, including at a grazing reference; no open physical
neighborhood of that reference is assumed.

The margin from the smaller polydisk of radius `eta/8` to the larger one is
`eta/8` in each coordinate. Cauchy's formula gives a repeated second partial
bound `2! (4R_+) (8/eta)^2=512 R_+/eta^2`; mixed derivatives are smaller.
For a two-dimensional Hessian derivative the Euclidean operator norm is at
most `2 sqrt(2)` times this entry allowance times `|h|`, which is bounded by
the stated factor four. This verifies `K_F^an=2048 R_+/eta^2`.

At the closed critical physical reference the endpoint incidences are one.
The continuous reduced Hessian formula gives `G_*>=R I>=2 g_under I`,
including a simultaneous interior-grazing limit. Its inherited upper bound is
`Lambda_circ I`. On the endpoint ball of radius
`a_an=min(eta/16,g_under/(2 K_F^an))`, the Hessian change is at most
`g_under/2`. This proves the stated weaker bounds
`g_under I <=G<=2 Lambda_circ I` with slack on both sides.

For any `|g|<b_an=g_under a_an/4`, minimizing
`F(q_*+h)-g dot h` on the closed endpoint ball gives an interior minimizer:
on its boundary the outward radial derivative is positive. Strict convexity
gives uniqueness. Strong monotonicity gives
`|q(g)-q_*|<=|g|/g_under<a_an/4`. The inverse is therefore defined on the
entire common gradient disk, and its image is safely inside the domain on
which the complex derivative estimates were established. Differentiating
`grad F(q(g))=g` gives exactly

\[
 \|Dq\|\le\underline g^{-1},\qquad
 \|D^2q\|\le K_F^{\rm an}\underline g^{-3}.
\]

No endpoint neighborhood radius depends on the smallest visited incidence,
the word length, an unvisited obstacle margin or a section margin.

## 5. Individual marked clearance and both chain-rule terms

The marked defining function uses a fixed center and a fixed signed line
impact. Its differentiability does not require choosing a differentiable
minimum among competing unvisited disks. The weighted analytic contact
bound implies
`|delta alpha_j|+|delta alpha_{j+1}|<=P s gamma^d`, with the original flight
depth `d=min(j,m-1-j)` and `s=|h_0|+|h_m|`. Complex circular position
increments give the factor `2 R_+ P s gamma^d`.

Differentiating `X/(X dot X)^(1/2)` in the complex Euclidean norm gives
operator bound

\[
 \frac{1+(5/3)^2}{3\tau_-/4}
 =\frac{136}{27\tau_-}<\frac6{\tau_-}.
\]

Thus the direction difference has the stated `12 (R_+/tau_-) P s gamma^d`
bound. The reference vector from departure contact to the marked center is
bounded by the actual foot distance plus the perpendicular impact, hence by
`28/5+R_++3/200=1217/200`. Combining the position increment against the new
direction and the direction increment against this reference vector proves

\[
 |B(q_*+h)-B(q_*)|\le L_B s\gamma^d.
\]

On the larger polydisk this is at most `L_B eta gamma^d/2`. Cauchy on the
smaller polydisk gives a first partial bound `4 L_B gamma^d`; the Euclidean
gradient bound `4 sqrt(2) L_B` is strictly below `6 L_B`. A repeated second
partial is at most `64 L_B gamma^d/eta`; converting the two-by-two matrix to
operator norm gives `128 L_B gamma^d/eta`. The constants in the draft are
therefore valid without an omitted dimension or factorial.

For `mathcal B=B composed with q`, the complete second derivative is

\[
 D^2\mathcal B[\xi,\zeta]
 =D^2B[Dq\,\xi,Dq\,\zeta]+DB[D^2q[\xi,\zeta]].
\]

Both terms survive in general. Their norm bound is exactly

\[
 \left(\frac{K_{B,2}}{\underline g^2}
       +\frac{K_{B,1}K_F^{\rm an}}{\underline g^3}\right)
 \gamma^d=K_{B,g}\gamma^d.
\]

The auxiliary check includes a nonlinear gradient inverse example with a
nonzero second composition term, so omitting that term would fail the check.

## 6. The exact cancellation and the physical summation

On a covered boundary point, both `mathcal B(g)` and `mathcal B(0)` are zero.
For any twice differentiable function on the full formal gradient segment,
ordinary integration by parts gives

\[
 D\mathcal B(g)\,g
 =\mathcal B(g)-\mathcal B(0)
   +\int_0^1 s D^2\mathcal B(sg)[g,g]\,ds.
\]

This is an exact identity, not a Taylor expansion with a radius-dependent
error. Here it bounds the numerator by `K_B,g gamma^d |g|^2/2`. At the actual
physical endpoint record,

\[
 u_t|_\theta
 =\frac{D\mathcal B(g)\,g}{g^T G^{-1}g}.
\]

The denominator is at least `|g|^2/(2 Lambda_circ)`. Cancelling these quadratic
factors before bounding gives exactly `Lambda_circ K_B,g gamma^d`, uniformly
down to positive `|g|` arbitrarily close to zero. The formal segment is used
only in an analytic identity. All points at which a physical speed or measure
is evaluated are actual covered regular boundary records with their complete
contact configuration and original cuts.

The pointwise estimate has the same constant for every eligible critical
chart. At fixed radius, count and marked flight, the actual one-copy source
is parametrized by angle and impact sign. It is not a separate measure for
every word. A boundary point can be assigned to its first eligible critical
chart before applying the uniform pointwise estimate. The complete two-sign
angular mass is `4 pi`; therefore the trace formula gives

\[
 \mathfrak B^{crit}_{j,u_0}
 \le \frac{\Lambda_\circ K_{B,g}}{4\pi R_-c_*}\gamma^d
         (4\pi)
 =C_{zf}\gamma^d.
\]

No bound on the number of words is inserted. Original exact record and roof
selectors decrease this positive measure. Different active marked disks
remain different marked sources. If the original pairing counts an event
once, the fixed active-constraint convention is applied on that source; the
marked sum is an upper bound before this restriction.

The finite disjoint assignment also has a valid geometric basis. The fixed
horizon bounds make the actual words and candidate marks finite at fixed
count and radius. To check uniqueness at a **closed**, possibly grazing,
critical reference, pass the two native support inequalities to their
physical one-sided limits. All incidences are nonnegative and both endpoint
incidences are one. Their sum forces the first and last contacts to agree.
The two individual support gaps then sum to zero and are nonnegative. Each
flight norm support gap is consequently zero, so corresponding nonzero
flight vectors are positively collinear. Starting from the common first
contact, the next designated disk has a unique entry or tangent intersection
with nonnegative incoming incidence; the exit root would have the wrong
sign. Recursion fixes every contact, including each visited tangency.
Equivalently, the common normal outgoing first direction and the specified
word give the same recursive uniqueness. The limiting flight lengths stay
positive, so no zero-vector equality case is present.

Thus a word has at most one such closed physical critical configuration.
Fixed local angular lifts and seams can be assigned once. Equality with its
continuous full formal contact lift, plus the original finite physical tests,
defines Borel source sets. Short or disconnected actual pieces cause no new
factor and no continuity assumption across forbidden physical regions.

At most two indices have any given flight depth. The tail is therefore
`2 C_zf gamma^D/(1-gamma)`. For `D=ceil(theta_* m)` with fixed positive
`theta_*`, multiplication by `m^2` leaves a polynomial times a strictly
decaying exponential. This is a uniform finite-count inequality followed by
an ordinary limit; it changes neither the original microscopic roof window
nor the order of the original outer and collision limits. The roof
pushforward contracts total variation. A total-variation bound for this
boundary measure is not an essential-height estimate for a density.

## 7. Remaining terms are mathematically necessary

If the critical offset is `a_w=mathcal B(0)!=0`, the exact numerator is

\[
 -a_w+\int_0^1 s D^2\mathcal B(sg)[g,g]\,ds.
\]

The first term is not bounded by the just proved quadratic remainder. Its
weighted angular-source sum requires an additional estimate. A small
positive offset is not automatically negligible near a small gradient.
Likewise, the coverage definition must not be replaced by agreement of the
two endpoint angles alone; agreement of all contacts is essential to
identifying the formal branch with the physical point.

The current theorem integrates positive `|g|` and does not assign a boundary
curve value to the incoming critical fan at `g=0`. The existing fan theorem
retains its own physical-side and regularity assumptions. No angular-null or
collision-area-null argument is used to discard a singular endpoint charge.
A further global proof is still required for the unrepresented section and
pairing boundaries, nonzero offsets, uncovered physical critical pieces,
whole-word pressure and the original normalized low-incidence shortage.

## 8. Auxiliary execution and evidentiary limits

`check_independent_boundary_reconstruction.py` checks exact rational constant
relations, all Cauchy factorial/dimension conversions, an explicit nonlinear
second-order composition identity, the Euler remainder monomials, the signed
optical determinant and Wronskian, 135 rational positive optical products,
and 2,750 count/depth pairs. Its normal and optimized-interpreter outputs and
details are compared byte for byte by the recorded execution wrapper.

These are finite algebra checks supporting the written reconstruction. They
are not substitutes for the continuous proofs above, do not numerically
certify all physical billiard trajectories, and are not a new external review.
