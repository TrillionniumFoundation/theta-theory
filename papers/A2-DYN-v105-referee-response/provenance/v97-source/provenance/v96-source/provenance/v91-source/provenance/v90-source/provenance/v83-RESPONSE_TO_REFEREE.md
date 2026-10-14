# Response to the external report on A2-DYN revision 81

**Author:** Qian Qi. **Revision:** 83, 11 October 2026.

**Controlling report:** `reviews/a2-dyn-v81-external-top4-review-2026-10-11/REFEREE_REPORT.md`, commit `614b15b2bb77f2887e95f685a0cfb6b2db44e99d`, blob `818e5932c895aea686da68fe37cec6018d2de759`.

**Preserved author baseline:** revision 82 at `81012268c5b8826a188a77715a84e75b1e1aa002`, paper tree `d1908253a6d134b5b1e4c732e84ad111ad4f836a`. The reviewed v81 author tree is `1d68fef5bbd1abc573d8e517e845cf889fe6431c` at `49957346c784071bf6f2e18a7ae6f2d724254f20`. Revision 82 was already present when this task began; it is preserved, not overwritten or counted as new work.

We thank the referee for distinguishing actual complete-source estimates from exact identities and conditional reformulations. The new results are complete optical local-norm bounds with no initial critical cutoff, and a quantitative local-mass bound for the actual nongrazing first-exit surface assignment. They keep the original source, labels, guard, arithmetic reference and pointwise objective. They are not represented as essential-height bounds or as closure of the original theorem.

## 1. Complete critical initial height — request 1

Module 190 uses the actual untruncated insertion `I_m |g|^{-eta}`, `0<eta<1/2`, already proved finite before the collision limit. The explicit radial flow replaces the first inverse gradient by a kernel with exponent `(1-eta)/2`. Negative optical variation pays both surviving inverse-twist loss and the entire positive initial weight of a genuine grazing first exit. The two classes are disjoint, and common target-direction covariance sums every actual word without a word-count factor.

Theorem `thm:v83-complete-weak-height` then proves a complete weak-L^q bound for every fixed `2<q<4`, together with strong L^p bounds for `p<q`. On a previously fixed roof interval of length r its normalized weak norm is at most `C_q r`. For the initial critical source `|g|<sqrt(r)`, the choice eta=1/4 yields `C r^(1+97/256)` in weak L^(8/3). This is a genuine untruncated estimate; it does not take the fixed-cutoff v81 bound through a forbidden interchange.

The requested essential-height estimate is not thereby proved. Module 192 isolates the remaining full microscopic tail with the whole finite-count tail inside the normalized supremum and collision limsup. It also proves a concrete uniform finite-count envelope sufficient for that tail. The required exponent is strictly larger than `(1-eta)/2`, rather than 1/2. No endpoint eta=1/2 or exponent 1/4 is claimed.

## 2. Actual nongrazing first-exit surface height — request 2

Module 191 defines the full one-sided outgoing flux with its incident physical component, backward lifetime and first-exit selection; there is no initial lower cutoff. The new inequality controls the surface source itself, not only the cost of pulling it back. On a nongrazing exit, positive optical variation bounds the terminal optical weight by its initial weight plus drift. Negative variation supplies the reverse comparison. Both costs are bounded by the actual fractional volume potential after the correct coarea change of variables. The inverse Jacobian remains in the exact exit identity; the two variation estimates pay its cost rather than deleting it.

Every true starting exit is contained in the complete tapered incidence, clearance or section-decision layers. The physical bad-source estimate and the all-depth marked transverse-strip theorem then give a roof-interval mass bound `C |J| r^(1/32)` after the legal ordered limits. This includes initial, internal and terminal section tests, competing hits and simultaneous failures. Combining it with positive optical variation proves Theorem `thm:v83-surface-local-mass`: on each fixed interval of length r the normalized mass of the actual outgoing first-exit assignment is `O(r^(33/32))`.

This is new quantitative control for the actual surface assignment. It is not a surface essential-height or surface spectral theorem. The remaining height stays explicitly in the original endpoint budget.

## 3. Original exact-label pointwise theorem — request 3

Theorem `thm:v83-endpoint` preserves the original target and gives its error in terms of the untruncated first-exit surface height, the complete microscopic fractional tail, and already controlled elementary errors. The main objective is not replaced by a weak-L^q theorem, a smoothed local law, a different physical realization or a specialist-journal topic. The new local-norm theorems are proved steps towards that same objective. The full pointwise and unconditional downstream flags remain false because the two height conditions have not been established.

## 4. Order of limits and the inherited dyadic notation — request 4

The fractional source is defined and finite at each collision count. All roof widths, eta and optional initial upper thresholds are fixed before the collision limit; auxiliary bands are enlarged afterwards, and the reconstruction parameter B is last. The microscopic tail is not replaced by the sum of individual scale limsups. The source restrictions are removed at finite count through positive integrability, not by commuting the first inverse-gradient cutoff with the collision limit.

The inherited module 189 labels its intervals as absolute roof intervals but writes `v(t+s)` inside their integrals. The active module 192 explicitly corrects this double-translation notation: integrate s from ell_j/2 to ell_j, or integrate v(u) on (t+ell_j/2,t+ell_j]. The original file is preserved verbatim; the supplement carries an adjacent clarification. The new ordered-tail statement also replaces the informal tail-uniformity wording by an explicit nested limit. No historical hypothesis is silently promoted to a proved estimate.

## 5. Common-space and spectral interfaces — request 5

The compact inputs in the article state the actual marked-strip, original-guard and fractional-insertion estimates, including finite-count remainders and their band dependence. The specialist appendix records the precise common-space route: the small norm belongs to the particular endpoint indicator vector, not to the multiplier on arbitrary vectors; arbitrary rank-one peaks are normalized by a nonzero smooth test, not by dividing by Pi 1; homogeneous traces use bounded strong Cesaro approximants; and the two chronological cases retain the forward occupation coefficient. The incidence cap is integrated before the gradient layer cake, which explains the strict eta<1/2 range.

The new proofs use these source-pinned analytic inputs. They do not claim that the cited external billiard paper proves the repository's entire four-record spectral chain, or independently re-prove that historical chain here.

## 6. Coarea covariance, optical signs and boundary exhaustion — request 6

The new appendix states the physical source and angular fiber normalizations in one coordinate convention and proves graph covariance by change of variables on (x,h), disintegration over (F,h), and a countable determining algebra. Nonnegative graph selectors and singular truncations use the same joint versions. Physical word pieces are disjoint; Borel chart seams are used for summation only and do not become exits.

The first-exit proposition displays the initial weight divided by the forward Jacobian. The backward lifetime excludes re-entry and faces are counted with their incident physical component. Compact regular flow-box exhaustion and actual one-sided face exhaustion are taken at fixed collision count. Positive variation is used for the upper bound on outgoing surface weight, and negative variation for starting mass and grazing loss; these directions are not interchanged.

## 7. Final-SHA source qualification — request 7

The v83 workflow pins the exact v82 paper tree, reviewed v81 tree and controlling v81 report blob. It verifies every inherited core, appendix, Python source, bibliography and provenance file, and all v81/v82 top-level snapshots. It compiles the new journal and the complete inherited supplement with actual recorder coverage of all 192 cores, and checks ordinary/optimized finite fixtures, stable warning-free references and PDF geometry. Intake of the source, earlier successful runs and local builds are not called final-SHA qualification. Final run results are reported at their actual author SHA.

## 8. Journal architecture — request 8

The focused article now presents the unchanged physical problem, a single theorem summarizing the new complete bounds, three explicit input statements, the new proofs, and a specialist appendix. The reader can see every analytic assumption used without scanning the historical status archive. All 189 inherited cores and both complete v81 and v82 articles remain in the technical supplement and provenance. The historical snapshot with the dyadic notation issue is retained with a separate clarification, not deleted or silently rewritten.

## 9. Independent specialist review — request 9

No independent human specialist approval, commissioned journal report, acceptance decision or formal proof certificate is claimed. The audit targets are the actual fractional source, first-exit graph and optical variation, joint kernels, marked section layers, and the remaining microscopic and surface height estimates. Finite fixtures and native builds provide source and execution evidence only.

## Status for the next external examination

Modules 190–192 prove the scoped complete optical norm, exit-layer local mass, actual first-exit surface mass, and ordered-tail implications under the stated inherited inputs. The essential-height endpoint remains a separate task. The title, raw actual-return interpretation, original normalization, exact occupation and displacement, all arithmetic peaks and zero classes, and scalar-before-path order remain unchanged.
