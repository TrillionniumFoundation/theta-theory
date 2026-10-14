# Response to the referee on A2-DYN revision 74

**Revision:** 75, 11 October 2026.  
**Controlling report:** `reviews/a2-dyn-v74-external-top4-review-2026-10-11/REFEREE_REPORT.md`.  
**Report commit / blob:** `18c51226fbc3bcc580ae66bee926d944be590c81` / `83ab4fa82c4f5be6ee930865c87633ef5d94717f`.  
**Reviewed author baseline:** `5a4704bc945d75e0fa181983a7b66a5dc5a73350`.

We thank the referee for distinguishing the exact endpoint reduction from the dynamical estimate it requires. We retain the original pointwise theorem and respond with a new physical geometric argument, not with a change of topic or a declaration that the endpoint is impossible. The new argument eliminates an uncontrolled wordwise coarea-complexity loss. It does not yet control the complete weighted sum of physical words at the collision-normalized scale. We identify that distinction in the abstract, theorem statements and authoritative manifest.

## 1. Physical short-excursion decay — substantive advance; request not fully closed

The referee asks for decay derived from the Lorentz geometry rather than fixed-count BV or an integrated estimate. Module 168 proves a new collision-independent geometric theorem. For every regular word, a fixed sixteen-direction cover at each endpoint supplies projection coordinates in which a global supporting action is strongly convex. Its restriction to the actual physical image has Hessian between `50/47` and `1360/9`, with no lower incidence or clearance cutoff. The supporting action is built from the Euclidean length minimization over the assigned internal closed disks. Convexity and the sign of the reflected contact gradients prove the support inequality and endpoint uniqueness directly.

The global support, not merely the local Hessian sign, is crucial: the physical image may be disconnected. Module 169 places all its roof-level arcs on one convex boundary. Their Gauss map has at most one inverse per normal direction and their coarea integral is at most `2*pi/lambda`. The earlier exponential wordwise level-multiplicity factor is therefore removed, including for the inverse-incidence insertion in module 131.

The resulting complete density is exactly the integral of the explicit nonnegative trace in equation `eq:v75-gauss-density`, retaining the inverse twist, both endpoint coordinate Jacobians, tangential curvature, the full guard and every exact event indicator. Module 170 proves that a paired roof modulus of this complete trace bounds the original component-length tail.

What remains is the collision-normalized bound on that weighted trace, after all physical words have been summed. The per-word constant cannot substitute for such a bound: the improved complete inverse-incidence estimate still contains an exponential word sum. We have not asserted the missing bound or promoted the scalar endpoint. `primary_referee_request_closed` remains false. This is a proved geometric advance toward the same endpoint, not a completed response to the principal decay request.

## 2. Every exact label — retained

The journal states `Pi = Y* intersect {K_m^c=k, A_m=n} intersect T^{-m}Y*`, with occupation at collisions `0,...,m-1` and the terminal section test at `m`. The Gauss trace carries this indicator on each original physical trajectory. The sixteen-cap choice is a disjoint coordinate partition, not label pooling. Displacement, collision count, return index, all clearance components and arithmetic zero classes are unchanged. The auxiliary convex minimizers are never included in the source.

## 3. Order of limits — stated and preserved

The outer band, guard, roof width, every finite Riemann mesh and the auxiliary spectral band are fixed before the collision limsup. Mesh refinement and auxiliary-band enlargement occur afterwards; the outer band is enlarged last. The ordered modulus retains `sup_R esssup_t`, allowing the exceptional roof set to depend on the radius. No collision-dependent width or spectral band is inserted. The complete trace is not truncated at the central-target boundary.

## 4. Scalar theorem before path and likelihood conclusions — retained

The exact scalar target is equation `eq:v75-original-target`. The path remainder, positive-reference normalization and clock-transfer implications remain downstream of scalar closure. Module 170 invokes them only under its explicitly stated dynamical premise. The inherited scalar/path error equality and all original zero classes are preserved, without claiming path-space total variation.

## 5. Specialist-auditable quantitative geometry — new proof supplied

The proofs give the covering angle `5*pi/16 < pi/3`, 256 cap pairs, the two uniform curvature constants and the coefficient `C_G = 2 R_+/(pi c_* R_-^2)` of the inverse-twist majorant. The supporting inequality treats every regular physical word at once; local smoothness uses the positive internal contact Hessian. The total-turning proof handles all disconnected physical arcs collectively. Compact regular exhaustions retain approaches to grazing and first-hit boundaries, without declaring a continuation across them.

No uniform radius of a physical neighborhood, higher-derivative estimate, weighted-word count or collision-uniform trace modulus is claimed. The fixed-count inverse-incidence corollary explicitly displays its remaining exponential factor. These limits are part of the theorem statements, not hidden in a constant.

## 6. Active specialist-audit metadata — corrected

The stale active v74 `SPECIALIST_AUDIT.md` is preserved byte-for-byte at `provenance/v74-SPECIALIST_AUDIT.md`. A new v75 audit map identifies modules 168--170, their inherited interfaces and the remaining independent checks. `SPECIALIST_AUDIT_MAP.md`, `PROOF_LEDGER.md`, generated status documents and the revision index are aligned with that map. Historical files and branches are not edited.

## 7. Journal and complete supplement — retained

The journal states the physical event, original guard, reference target, source-pinned analytic assumptions, explicit constants and short proof route. The supplement retains all preceding 167 proof modules, appendices and bibliographies, including the full mathematical body and abstract of v74. The three new modules give 170 active cores in total. Native recorder coverage tests the actual inputs rather than merely counting files. No mathematical source is arbitrarily deleted.

## 8. Independent human review — not represented as obtained

No independent human audit has been obtained in this revision. The audit map requests checks of the support inequality, all-level Gauss injectivity, physical endpoint Jacobian and measurable inverse, and the inherited tame, spectral, arithmetic and return-clock inputs. Numerical physical fixtures, exact finite identities, source hashes and PDF checks are separately documented; none is described as independent human review or a proof certificate.

## Handoff

The new revision and its identical referee copy are intended for further substantive review of the new geometric mechanism and its precise interface with the original endpoint. The complete weighted dynamical estimate remains the principal unfinished mathematical obligation, not an editorially discarded objective.
