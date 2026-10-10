# Collision-theory input map

This note records the scope of the load-bearing import in `lem:collision-spectral-input`. It is not an additional unverified induced-operator hypothesis.

## Primary sources and conventions

M. F. Demers and H.-K. Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, Communications in Mathematical Physics 324 (2013), 767–830, arXiv:1210.1261. The relevant locations in the 45-page preprint are Theorem 2.1(3), Theorems 2.5–2.6, Remark 2.7(b), the transfer convention in Section 3.2, and the strong/weak norms in Section 3.3. The unforced spectral-gap input is their *Spectral analysis of the transfer operator for the Lorentz gas*, Journal of Modern Dynamics 5 (2011), 665–709.

The source was checked at the stated theorem and norm definitions, including the PDF pages containing them. These sources concern collision maps. They do not supply the anisotropic realization of the present unbounded induced record or the all-branch raw density estimate.

## Geometric correspondence

| Source requirement | This family |
|---|---|
| Strictly dispersing smooth obstacles and positive minimum flight | Circular obstacles, R in [9/20,47/100]; curvature in [100/47,20/9]; separation at least 3/50 |
| Uniform finite horizon | The smallest radius exceeds the triangular corridor threshold sqrt(3)/4; the compact radius interval has a common horizon |
| Common boundary parameter intervals | At R0 use r0=R0 alpha; the nearby boundary map is r0 -> R n_(r0/R0), with speed R/R0 and uniformly controlled C3 derivatives |
| Small deformations including changes in boundary length | The preceding parametrization is C2-close as R approaches R0; Remark 2.7(b) expressly permits the boundary-length reparametrization, with slightly weakened common constants |
| A conventional periodic planar table | The rectangular two-disk cover has periods (1,0),(0,sqrt(3)) and centers 0,b. The deck translation commutes with the map; its invariant closed subspace gives the original triangular quotient without affine distortion of reflection |
| Common invariant reference probability | In angle coordinates, dnu=(4pi)^(-1)cos(phi)dalpha dphi; p=sin(phi) gives the flat collision cylinder. No inverse p-to-phi conjugation is used at grazing |

## Spectral and multiplier correspondence

At each fixed unforced table, one is a simple isolated eigenvalue and the rest of the collision spectrum lies inside the unit circle. Strong/weak perturbation stability and Theorem 2.1(3) provide the complementary power estimate on a neighborhood. A finite cover of the compact radius interval gives uniform constants; it does not assert one global space for arbitrary induced maps.

The smooth multiplier bound is also explained in the manuscript directly from the source norms. The stable part controls a test function multiplied by a C1 function. For matched curves at distance epsilon, the new difference of the restrictions of a C2 multiplier has Cq norm at most C ||g||_C2 epsilon^(1-q). The defining exponents satisfy beta <= p-q with p <= 1/3, hence beta < 1-q. Division by epsilon^beta is therefore harmless. The weak part uses the same single-curve estimate. Completion extends the multiplier to the distribution space.

Smooth densities are interpreted relative to the invariant reference measure, not by assuming that Lebesgue density across grazing is C1. The mass functional is evaluation on the constant test function. Thus the smooth two-observable correlation bound used in revision 9 follows by applying the collision splitting to a nu and testing against b through the smooth multiplier and mass functional.

## New ingredients not imported from these sources

The finite-horizon one-collision root is a bounded semialgebraic family in rational angular charts. The uniform fiber monotonicity and differentiable cell decomposition used for its BV bound are the results in M. Coste, *An introduction to o-minimal geometry*, Sections 2.1–2.2 and 6.2. The manuscript proves explicitly how slice variation gives the two distributional derivatives, and treats the moving rectangular section separately.

Mean-preserving reflected smoothing, the small-L1 residual variance estimate, the exact stopped compensation, the shrinking-scale characteristic estimate, the Hilbert-space coboundary construction, and the fourth-moment coarse-grid functional argument are proved in the three new sections. None is attributed to an induced billiard theorem absent from the cited source.

For historical positioning only, the common-renewal section cites S. Gouëzel, *Sharp polynomial estimates for the decay of correlations*, Israel Journal of Mathematics 139 (2004), 29–65. Its operator-renewal algebra is not claimed as new; no hypotheses or conclusions of its renewal spectral theorem are silently imported here.

## Review boundary

A dynamics specialist should check the local common-space identification and smooth multiplier against the chosen source norms, and the application of uniform semialgebraic slicing at collision singularities. The proof is supplied for that review. Finite diagnostics cannot check these continuum facts, and no independent human specialist endorsement is claimed.
