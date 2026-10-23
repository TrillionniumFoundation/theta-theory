# Author derivation: selected endpoint kernels and critical tightness

## Files and status

The proposed native LaTeX body is clearance_selected_endpoint_kernel.tex.
It contains one new lemma, two new theorems, and their full proofs.
It does not assert completion of the endpoint shortage or the raw local
limit. It is an optional genuine geometric increment for the root author
to independently audit and integrate, rather than an external referee report.

The source inspected was the materialized native paper
papers/A2-DYN-localized-clearance-records-author-revision, at the
evidence-carrier commit e84c06c758bed5b2dc09222ad725cfe0ba0d58dd.
All its existing source bodies remain unchanged by this work.

## New mathematical content

For the real m-collision flow and an actual clearance witness at flight j,
the full endpoint-momentum root density obeys

    D(m,j,delta;a,v) <= C_end [delta + theta_r^max(j,m-1-j)].

The estimate includes j=0 and j=m-1, all actual collision words,
both signs, arbitrary original Borel observations by positive restriction,
and every regular endpoint momentum value. Reversal is performed on the
same physical orbit; it is not an independence argument.

The genuinely new argument fills the initial-flight gap in 327.
For the first image of a clearance-selected horizontal fibre, it retains
both the sum of density suprema and the sum of density-supremum times
physical curve length. The second sum is O(delta). A uniform ratio bound
for the exact first-image density on each homogeneous piece establishes
this assertion without a common lower incidence cutoff. The subsequent
renewal weights its transient term by the first budget and its long-piece
term by the second budget. The last-collision momentum cancellation is
then applied exactly once.

Applying the existing exact critical angular change of variables and
the physical-side sector proof gives a new positive-width critical
coefficient estimate, including shallow indices:

    sum J(x) beta_y(x) <= C_crit [delta + theta_r^max(j,m-1-j)].

For the original exponentially depth-weighted clearance guard this
becomes

    C_crit [4 epsilon(B)/(1-q0^(1/4)) + m theta_r^((m-1)/2)].

Its order of limits is the original collision limit first and B second,
but its norm is the unscaled complete critical-coefficient norm.

## What is inherited, rather than new

| Native result | Use in the proposed proof | New content beyond it |
| --- | --- | --- |
| 327 thm:lc-renewal | Exact weighted transport on physical short curves | Retains selected mass through the first physical image, before renewal |
| 327 lem:lc-cover | At most K_c initial intervals with O(delta) total source length | No new clearance cover is claimed |
| 327 thm:lc-local-half | For j>=1 gives delta plus the forward-tail error | Handles j=0 uniformly and combines both physical time directions |
| 284 lem:mc-first | Exact density d/[RA sqrt(1+V_1^2)] | Explicit homogeneous ratio and weighted-mass budget |
| 284 eq:mc-last-cancellation | One actual last collision removes terminal inverse incidence | Unchanged cancellation, no artificial terminal homogeneity subdivision |
| 285 lem:mc-angle and thm:mc-critical-sectors | Converts selected endpoint density to one-sided critical coefficient | The density used now carries a small clearance width and a decaying long-side transient |
| 322 pc:representatives | Finite analytic physical-side angular limits | No new analytic sector theorem is claimed |
| 322 pc:fan | Existing zero-clearance critical-fan exponential estimate | The proposed theorem controls all widths in (0,delta_*); the old zero-level theorem remains sharper at zero |

## Inequalities and normalization audit

1. Homogeneous strip density ratio:
   sin(k^-2)/sin((k+1)^-2) <= (pi/2)((k+1)/k)^2.
   This uses sin x <= x and sin x >= 2x/pi on [0,pi/2].
   Both strip signs have the same cosine ratio.
2. The denominator A=c+tau/R satisfies
   tau_-/R_+ <= A <= 1+tau_+/R_- even as the initial incidence
   tends to zero. This prevents an unrecorded initial inverse-incidence loss.
3. rho_sup |C| <= D_first integral_C rho is proved on each
   homogeneous piece; no comparison across infinitely separated strips occurs.
4. The first-image sup budget is multiplied by K_c because each of the
   J_0 preliminary arcs can contain K_c selected cover intervals.
   The selected source-mass budget is multiplied by J_0, not K_c again,
   because L_c delta already sums all cover intervals on an arc.
5. For j=0, the true collision count is 1+(m-2)+1=m; the factor
   theta_r^-1 in C_first changes theta_r^(m-2) to
   theta_r^(m-1) with no missing generation.
6. For j>=1, 327 is used with h=j-1, n=m-j-1, and l=m.
7. Physical reversal maps j to m-1-j, exchanges endpoint momenta with
   their signs, and preserves inverse root weights by the exact
   determinant-one collision derivative. Taking the smaller of the two
   positive upper bounds gives the exponent max, not min.
8. The fibre measure is d alpha_0, not boundary arclength.
   d nu_R^* has the single factor 1/(4 pi c_*).
   In the critical proof this factor is removed when applying the
   unconditioned endpoint kernel and reappears once in the critical
   coarea factor U_2/(2 c_*).
9. Pointwise regular-root bounds are obtained by continuity on finite
   collections of actual inverse branches and then nonnegative exhaustion.
   They are not restrictions of an arbitrary almost-everywhere density version.
10. Boundary witnesses with clearance zero or delta are handled with a
    fixed delta+eta neighborhood, at fixed R,m and finite germ family,
    before eta tends to zero and the germ family is exhausted.
    The critical theorem accordingly states delta<delta_*.
11. At most two flights have a given depth. Therefore
    sum_j 2epsilon q0^(depth/4) <= 4epsilon/(1-q0^(1/4)).
12. All mark/source sums precede label and radius suprema. Arbitrary
    Borel tests can only restrict already bounded positive quantities.

## Precise unresolved closure

The new estimate has no hidden m^-2 factor. In particular
m^2 epsilon(B) cannot be made small when B is fixed before m grows.
Consequently this result does not establish equation
eq:lc-final-shortage. A critical leading-coefficient estimate also
does not control the total coarea remainder at a common roof.

A sufficient future mechanism would be a uniform joint original-roof
and exact-record smoothing estimate for these actual selected
horizontal/short-curve families, whose normalized bound uses their
selected-length budget while paying the complete branch complexity.
The original mark torus, all arithmetic classes, real section cuts,
and microscopic window must be retained. The current endpoint kernel
does not supply that analytic estimate.

There is no valid direct inference from a small selected area and a
uniform BV bound to a small essential density height. Near a nondegenerate
two-dimensional critical minimum the coarea density can retain a
nonzero incoming fan on every sufficiently small sublevel set. This
generic local calculation is only a logical diagnostic; it has not
been substituted for the triangular Lorentz gas.

## Validation executed here

structure_check.json records 12 unique new labels, no collisions
with existing labels, no unknown references, and matched proof/theorem
environments. The mathematical checks above are analytical.
No compilation or CI success is claimed by this subtask. The root
author must compile the integrated manuscript and independently
audit the new argument before publication.
