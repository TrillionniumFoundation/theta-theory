# Response to the v34 referee report

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Report:** `e8ad32bfd0a8641c239c67e9776ba08d3aaab72a`, report blob `339750c06e20fb9f7608c3ffb7ba1428bbdd225f`  
**Reviewed author:** `ed3876b8a82e2c46bc1533457978c15fea1a2114`  
**Revision:** A2 v35, 4 October 2026

We thank the referee for distinguishing the substantive fixed-spread inverse and its proof from the information-contract and significance questions. We retain the original topic, all reviewed mathematical statements, and the prior localized, stationary and adversarial results. We add two mathematical results directed at the two principal outstanding restrictions: supplied knowledge of the entire footprint and the absence of a stationary-noise lower bound.

## 1. Erosion and rolling-radius thresholds

The proof of Lemma `lem:cap-mass` now chooses uniform interior rolling radii `r_C,r_K`, puts `r_P=r_C+r_K`, and restricts `e_0` below one sixty-fourth of their minimum and below one eighth of the common collar depth. Thus the erosions by `e/4` are strictly below all relevant rolling thresholds.

## 2. Signed high-order approximation kernel

The proof of Proposition `prop:jitter-modulus` now calls the kernel an explicitly **signed approximation kernel**, not a launch probability density. The coefficients `(8/5,-4/5,8/35,-1/35)` on dilation scales `1,2,3,4` give integral one and vanish at all nonconstant moments through degree six. The interpolation argument and its rate are unchanged.

## 3. The entire footprint need not be supplied

Theorems `thm:self-exact` and `thm:self-finite` replace that functional calibration input with a two-scale experiment. The footprint `K` and its laboratory Steiner point are unknown. At two known, fixed positive scales the same stationary mechanism has supports `lambda_1 K` and `lambda_2 K`. The controller knows their scale factors and common dilation origin, uniform inball/envelope/curvature/smoothness bounds, and boundary-mass constants, but has no support-function or density oracle.

The reciprocal killed-walk inverse first reconstructs the expanded bodies `P_i=C+(-lambda_i K)`. The uniform inball produces strict nesting, a containment-based correspondence, and two support equations recover both the original body and the unknown footprint. The finite algorithm therefore removes the footprint-function oracle rather than hiding it in a local query.

The new hypothesis is explicit: two exact homothetic settings are required. Independently drifting footprints, unknown scale factors, unbounded jitter and unpriced metrology are not covered.

## 4. A stationary-noise lower bound under one common law

Theorem `thm:stationary-lower` gives the expected-attempt lower power `nu^(-(s+1)/(s-2))`. It fixes a **single known uniform-disk density**, identical for every table and every command, with exact implementation. The controller may choose short directions, arbitrary-precision centers and any launch scale in a fixed positive interval. The lattice and species labels may be supplied.

Lemma `lem:mean-contraction` gives a uniform `O(h^s)` range for every Bernoulli response over the physical packing. Lemma `lem:binary-range` and Proposition `prop:stopped-contraction` propagate this contraction through arbitrary adaptive stopping. The lower exponent is deliberately not presented as matching the stationary upper exponent.

For gamma zero, the retained upper exponent is `(3s+1)/(s-2)` and the new lower exponent is `(s+1)/(s-2)`; the gap is `2s/(s-2)`. No claim of sharp confidence dependence or stationary minimax optimality is made.

## 5. Fixed spread versus physical calibration

The abstract and full new theorems keep fixed random spread, nominal positioning, exact directions/durations, homothetic scale control and physical calibration distinct. The controller never observes actual starts or learns the nuisance density. Every solid start and miss remains charged. Manufacturing and calibration of the apparatus are not silently priced into attempted-bit complexity.

## 6. Prior-relative period decisions

The finite two-scale theorem works on `B_eta` with the retained whole-patch nonperiod margin and bounded periodic presentation. Period tests are performed after footprint subtraction. Exact rational relations and primitive orbit counts remain separate from approximate real period vectors and free areas. No crystallinity conclusion for arbitrary nonperiodic configurations is added.

## 7. Scope

The new results remain about the scalar collision sensor and active inputs. They are not recast as passive count-germ, marked-length or spectral rigidity. Support addition, convex parallel-body geometry, active line search and entropy arguments are used as proof tools; no priority claim is made for those general principles.

## 8. One article and source preservation

The primary is self-contained. The reviewed v34 source and v33 archive remain untouched at their existing repository paths. The new revision adds only the v35 article directory and verification workflow. Local evidence records 4,254 current finite diagnostics, 19 current contract tests, and reruns 5,886 v34 diagnostics and 21 v34 contract checks in ordinary and optimized Python with identical output. These are reproducibility evidence, not formal proof certification or physical-sensor execution.
