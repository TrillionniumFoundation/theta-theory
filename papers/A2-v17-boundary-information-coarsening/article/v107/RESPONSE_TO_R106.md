# Response to the independent referee report on A2 v106

**Revision:** A2 v107, *Hankel information and nonlinear contact of synchronized roots*  
**Reviewed source:** `5cbbe96cd2ac590bfa2e17bcef97b0630cd91c4a`  
**Report:** `bcd8052659a783632de3873af49f05f600a8f764`, `reviews/a2-v106-independent-harsh-top4-2026-09-21/REFEREE_REPORT.md`  
**New branch:** `revision/a2-v107-synchronized-root-contact-budget-geometry-2026-09-21`

We thank the referee for distinguishing the genuine v106 mathematical advances from the earlier source-state issue. This revision responds to the remaining structural objections with new theorems and complete proofs. It does not delete or replace the earlier mathematical record. The principal article imports every v104 and v106 mathematical part used by the reviewed manuscript, while reorganizing the exposition around a new nonlinear contact theorem. The source parts, historical articles, and report remain unchanged.

The descriptions below identify what is supplied for renewed review. They are not an assertion that an independent referee has already accepted the proofs or priority claims.

## R106.1 — A central theorem coupling the difficult regimes

**New source:** `parts/01-critical-contact.tex`, `thm:synchronized` and `ex:synchronized-critical`.

The model is the calibrated binary polynomial experiment, with root pairs constrained to split under shared parameters: the roots at site i are `r_i+s_i/2 ± a_i^T eta`. Loadings are fixed independently of any desired information matrix. The variance image is the rank-one quadratic measurement cone `q_A(eta)=((a_i^T eta)^2)_i`, not an arbitrary prescribed contrast metric.

The theorem proves both inclusions for the complete normalized probability residual, localizes all minimizing sequences, and gives the exact Hellinger contact formula

`min_{v in V_A} min_{z>=0} (v-b,z)^T Q (v-b,z)`.

The same unrestricted observation model forces `Q^{-1}` into the Hankel congruence class. In the one-colour visible subclass the labelled endpoint profile on the positive retained orthant reconstructs Q up to endpoint gauge. That gauge preserves its extension to all real retained directions, and therefore determines the nonlinear contact for every loading family and target. The extension is stated explicitly because `v-b` need not be nonnegative.

The two-parameter, three-cluster example has `q=(eta_1^2,eta_2^2,(eta_1+eta_2)^2)`. Over the marked fast variances there are two distinct observed slow values, not merely duplicate root labels. Its entire critical residual is the quadratic cone `(v_3-v_1-v_2)^2=4v_1v_2`. With two endpoints it lies in the native fully visible class. This example has `cM` of order one; it does not claim the additional localization ratio `c/r` tends to zero. The full-cone theorem avoids that inverse-tube restriction.

The earlier regular symmetric-coordinate compatibility theorem remains intact as a companion result. The new theorem does not restate its observationally collapsed sheets as a singular unification.

## R106.2 — Intrinsic objects versus marked presentations

**Sources:** retained `v106/parts/01-categories.tex`; new `parts/03-geometry.tex`, `prop:fast-switch`, `ex:marked-certificate`, and `rem:order-faces`; rewritten abstract and introduction.

The new main claim concerns a feasible residual image and a labelled endpoint object. The fast derivative criterion is explicitly a certificate for a marked fast map and tube. A transverse observation-coordinate transition now has a displayed chain rule, a second-derivative bound, and precise hypotheses under which smallness transfers. A simple coordinate-swap example shows why arbitrary changes of the fast observable need not preserve the certificate, even though they preserve the underlying residual germ with its transported metric. Thus the invariant statement and the presentation-dependent statement are separated by a mathematical transition result, not only a caveat.

## R106.3 — Genuine stability, not just fixed orders

**New sources:** `parts/03-geometry.tex`, `thm:critical-jets`; `parts/01-critical-contact.tex`, final assertion of `thm:synchronized`.

The weighted initial-map theorem gives uniform normalized residual and minimum limits on compact coefficient families with a positive properness margin on the weighted unit section and a uniform higher-weight gap. The leading coefficients may vary; no simultaneous resolution or fixed divisorial orders are assumed. The synchronized theorem also permits higher-order perturbations of the loading functions and proves that the same leading cone and contact formula persist. These are positive coefficient-space stability results in the stated broad classes.

Fixed-resolution/order persistence remains a distinct claim in the inherited certificate theorem. The precise facewise interpretation of its weak and strict inequalities is given in `rem:order-faces`; there is no claim of one simultaneous resolution for arbitrary coefficient perturbations.

## R106.4 — Critical-boundary normal forms beyond one example

**New sources:** `thm:critical-jets`, `thm:synchronized`, `ex:synchronized-critical`.

For a proper weighted leading observation map P, the complete critical residual is proved to be `P(K)-b`, and its cost is the minimum in the native positive metric on this closed set. Both residual inclusions and convergence of minima are proved by weighted localization. This covers coupled leading polynomials and perturbations with higher weighted degree. The synchronized-root class supplies a natural statistical instance where the surviving polynomial map is non-affine and its metric is not independently designed.

The cubic v106 wall example and its complete calculation are retained. The general theorem does not assert that every singular germ is weighted homogeneous; its proper-leading-map hypotheses are part of the normal-form statement.

## R106.5 — Endpoint proof architecture and exhaustion

**New source:** `parts/04-endpoint-completion.tex`.

`lem:planar-fan` displays all four primal sectors in the chain normalization and all four dual sectors in the fork normalization, including exact optimizer formulas and inequalities. Its convex-cone arguments prove the nesting or disjointness required for the global value-function formulas. `prop:planar-exhaustion` derives the chain/fork trichotomy from the intrinsic Boolean order, establishes the rank lower bound for every competitor, fixes signs from labelled regions, and proves that the scalar families exhaust all minimal competitors. The ratio bounds are shown necessary and sufficient on the entire cone; boundaries follow by continuity. A collapsed interval leaves only two scale parameters.

`lem:missing-singleton` and `lem:missing-extreme` separately prove the missing-singleton, missing-full, and missing-empty reconstructions. Pair range intersections, normalized coefficient recovery, and the dual construction are displayed explicitly.

Beyond the requested first strata, `thm:all-strata` gives an exact finite active-cone-intersection equality test for arbitrary visibility and rank patterns. It determines minimal dimension by finitely many semialgebraic feasibility problems and obtains a finite partition with constant normalized fibre type. This is an effective presentation, not a claim that every higher-dimensional fibre has a simple scalar normal form.

## R106.6 — Hankel proof and theorem-level priority analysis

**New sources:** `parts/02-design.tex`, `lem:rational-inverse`, `ex:four-clock-inverse`, `prop:overidentified`; `parts/05-positioning.tex`; `newreferences.tex`.

The rational coefficient inverse is now isolated with all dimensions, principal-part signs, and polynomial-basis changes. An exact four-clock example is included. The rectangular-clock proposition states the surviving full-rank Gram/dual-minimization formula and gives an exact seven-clock counterexample to preserving the selected square-design Hankel congruence.

The literature comparison is organized by theorem, not by broad subject labels. It distinguishes classical moment cones, regression information, interpolation, Cauchy total positivity, Schur complements, forward complementarity, phase retrieval, tangent-cone statistics, and semialgebraic triviality from the particular implications proved here. The central claim is the native model-to-inverse-information-to-nonlinear-contact relationship. Six additional references include Balan–Casazza–Edidin, PhaseLift, Drton, Cottle–Pang–Stone, Pukelsheim, and Hardt. The inherited references on moments, total positivity, design equivalence, latent identifiability, resolution, and asymptotic statistics remain.

Exact deterministic noiseless dual-value queries remain a secondary corollary. No query count is described as sample complexity or transferred to an information-value oracle.

## R106.7 — Fixed-total-exposure geometry

**New source:** `parts/02-design.tex`, `thm:budget` and `cor:scalar-budget`.

The reciprocal budget function is minimized over each positive moment fibre. Its unique minimizer, analytic dependence, homogeneity, and positive Hessian are proved. The full fixed-budget image and all exposure fibres are then classified:

- Two endpoints: a smooth moment hypersurface with one exposure vector per point.
- One endpoint: a convex moment region, one exposure vector on its boundary, and exactly two in every interior fibre.
- No endpoints: a convex moment region, one exposure vector on its boundary, and a circular interior fibre.

The distinction follows from the moment-kernel dimension `2-e`. The fibre classification is proved by strict convexity and radial parametrization, not inferred from a numerical rank. The scalar budget optimum is identified as a classical Cauchy–Schwarz corollary, not a separate novelty claim.

## R106.8 — Dependency and provenance map

**New source:** `parts/06-dependencies.tex`, Appendix `app:dependencies`.

The table pins the reviewed source and report, names every principal source part, distinguishes retained v104/v106 results from new v107 results, and states the logical inputs. In particular the critical contact theorem does not depend on the affine derivative certificate. The complete older source record is retained. Build receipts identify the actual compiled revision by its commit and hash every recursively included TeX source; no self-referential guessed commit is inserted into the manuscript.

## R106.9 — Source-bound native build and replay

**New sources:** `build_review.py`, `checks.py`, and `.github/workflows/a2-v107-native-review.yml`.

The replay command materializes the exact recursively included source closure of v106 at `5cbbe96cd2ac590bfa2e17bcef97b0630cd91c4a` and the new v107 closure at the checked-out commit. It compiles both with native TeX, checks final references, records compiler commands and versions, emits source/PDF SHA-256 hashes, and runs finite exact algebra examples. The branch-specific workflow retains all source closures, PDFs, logs, and a receipt. It has read-only repository permissions and never merges or edits other branches.

A script or workflow is not itself a successful receipt. Actual execution status and artifact identifiers are recorded separately after a run. The evidentiary order remains manuscript proof, independently checkable finite examples, then native build evidence. None of these build assertions substitutes for independent mathematical review.

## Minor comments

The fixed-clock moment cone is consistently distinguished from arbitrary-support moment cones. The total-positivity conjugation uses the retained ordered-site sign convention. The deterministic noiseless oracle qualification is retained. The scalar-interval singleton case is explicit. The synchronized theorem states the Hellinger convention directly, including the factor four. The order region is described facewise because weak inequalities are present. Language-model assistance is disclosed separately from any validation or acceptance claim.
