# Response to the latest external referee: A2-DYN revision 37

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v36-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Review commit / blob:** `ef921b94134118b9b41a4ca8237c3f87a34a02bd` / `a3b919fec33408b58505649125f4f74c3a9af5ef`.  
**Actual author baseline:** `fda52bb72045204b50159e8263c05afaa6a9dc58`, revision 35.  
**Frozen ordinary paper tree, including its manifest:** `1634006e867a2258b09d85db6f9fcecc668f53d1`.  
**New article:** `papers/A2-DYN-v37-referee-response/main.tex`.  
**Date:** 8 October 2026.

We thank the referee for separating submission identity from mathematical substance. The revision-36 aliases did not contain a new manuscript. We do not represent them, or any unverified local working record, as a mathematical baseline. This revision starts from the latest report commit, preserves both reports and the actual revision-35 source, and adds a complete ordinary manuscript directory. It also proves a new local constraint on the original four-coordinate return record, rather than only adding another stationary-flow application.

## 1. An actual theorem-bearing revision

The active manuscript is revision 37 throughout its date, directory, manifest, workflow and two branch names. The new modules are 76--79. All 75 inherited core modules and the compiled A--X appendix remain included. Of these core files, 73 are byte-identical to revision 35; modules 72 and 74 receive six exact, recorded replacements. All 83 inherited Python files and the bibliography are unchanged. The old main source and both edited core sources are retained verbatim under provenance.

The new source verifier reconstructs the edits from the frozen baseline and checks the complete ordinary-source Merkle identity. Creating the branches at the report commit is only the initial step, not the delivery. The new author commit and its exact-source execution receipt are the objects for the next review.

## 2. Noncircular strong-space faithfulness

The final paragraph of `lem:v35-faithful-strong` has been replaced. The proof now extends the already vanishing smooth curve pairings to the little `C^q` stable tests by norm density. Their defining supremum is zero, so the strong stable seminorm vanishes. Each matched-pair difference is a difference of two zero pairings, hence the unstable seminorm also vanishes.

The completion step is explicit: the normalized stable pairings and normalized matched differences embed smooth densities isometrically in two spaces of bounded scalar families. A strong Cauchy sequence converges uniformly in these families. Their suprema are therefore the completed seminorms. No injective inclusion of the strong space into the weak space is invoked. The independently stated inclusions in DPZ Lemma 3.2(c), footnote 7, are cited only for comparison, not as a premise of this direct argument.

## 3. Finite-cover mixing and separated hypotheses

`prop:v37-finite-cover-mixing` pins the external mixing input to Stenlund--Young--Zhang, Theorem 3, arXiv:1210.0011v4, pages 6--7, with the configuration class immediately before Theorem 2. The proof checks the stronger transverse finite-horizon condition, positive flight gap, uniform curvature and boundary derivative bounds for each fixed finite cover. The conclusion is collision-map mixing. It is not inferred from connectedness or from mixing of the suspension alone.

The finite lattice cover is a fixed flat Euclidean torus with finitely many obstacles. A rectangular Euclidean cover may be used without changing the reflection metric. Its size and the number of obstacles may enter the correlation constants. The arithmetic proof fixes one prime cover at a time and needs no bound uniform in the prime. Smooth correlation decay is extended to `L2` mixing by approximation with an error uniform in the iterate. Mixing excludes the nonzero constant-step character; ergodicity alone handles the zero constant-step character.

Module 74 now separates table geometry, local common spaces and unweighted estimates, action/matching, finite-cover dynamics, parameter continuity/normalization, preceding-flight multipliers, and observation regularity. The ellipse proof explicitly invokes the new mixing proposition. The general principle states finite-cover mixing as an independent hypothesis instead of hiding it inside “uniform table geometry.”

## 4. A new local theorem for the original return record

Modules 77 and 78 address the difference emphasized in the report: the constant collision step is not the true section occupation. For the original actual section, write

`A_m = sum_{j=0}^{m-1} 1_{Y*}(T^j x)`.

The section is a fixed finite union of coordinate rectangles, uniformly away from grazing. Its horizontal and vertical sides are transverse to the stable cone. `lem:v37-section-multiplier` verifies the fixed-partition hypotheses of DPZ Lemma 3.3(b), and proves that the actual, unsmoothed section indicator is a bounded strong-space multiplier. Its exponential is the exact analytic expression

`exp(-iv c*) [I + (exp(iv)-1) M_eta]`.

This yields a four-variable collision operator with the current occupation on the source side and the preceding displacement--roof on the image side. The chronological pairing records exactly the visits in `[0,m)`. It neither smooths the section nor replaces it by the constant collision step.

The joint covariance is `Omega_R = c* L_R D_R L_R^T`, where the explicitly displayed matrix `L_R` has determinant `c*`. The inherited actual-return covariance theorem therefore gives uniform positivity. Analytic perturbation supplies the joint expansion near zero. On each fixed nonzero displacement--roof band the already proved compact-frequency gap persists for sufficiently small occupation frequency, by a resolvent argument. No estimate on the full occupation torus is assumed.

`thm:v37-occupation-local-central` then proves a mixed local--central limit: cell displacement is an exact lattice point, roof time lies in a fixed unscaled interval, and the true centered occupation divided by `sqrt(m)` has a Gaussian law conditional on that local collision constraint. Its conditional mean and variance are the explicit Schur complement of `Omega_R`. To remove the roof test, the proof does not order complex characteristic integrands: it dominates their replacement error by the positive upper-minus-lower envelope at occupation frequency zero. The band is fixed before taking the collision count to infinity.

`prop:v37-exact-return-disintegration` transfers this theorem to the actual return record. On an orbit starting and ending in the section at collision times 0 and m, `A_m=n` is equivalent to `N_n=m`. Both displacement and roof then agree exactly with the n-return record. This gives Theorem 3 in the introduction and `thm:v37-return-window`: a local limit for the original return law with exact collision count and displacement, a fixed roof interval, and a diffusive window of genuine return indices. The normalized amplitude is `c* g_Omega`, equivalently `c*^(-2) g_D(c*^(-1/2)L^(-1)(z,y))`; the determinant calculation is in the proof.

This is a substantive advance on the original four-coordinate measure. It is not its full raw pointwise LLT. Single-return-index inversion still needs noncentral occupation-frequency control, and pointwise roof inversion still needs the common correction and complete roof-frequency complement. Those original requirements are retained without changing their topology or marking them proved. A window limit is not used as a substitute for a singleton limit.

## 5. Generality and a verified nonelliptic application

Module 79 verifies the action principle for a compact support-function family on the same triangular lattice:

`h(psi)=R+e cos(3(psi-theta))+f cos(4(psi-phi))`,

with `R in [91/200,93/200]` and `|e|+|f|<=1/250`. The curvature radius is between `79/200` and `21/40`; the obstacles lie between disks of radii `451/1000` and `469/1000`. A nonzero third harmonic prevents central symmetry, so this family is genuinely nonelliptic, not a relabeling of the ellipse parameters.

The proof checks one-flight partition complexity in rational trigonometric charts before normalized arclength, uniform square-root entry regularity at nondegenerate tangency, stable/unstable transversality, finite-cover mixing, and closed exceptional neighborhoods for the observation cell. The perimeter, area and mean roof are computed explicitly. This is another verified application of the same mechanism, not a claim that standard fixed-table local limits or all of suspension local-limit theory are new. The more direct contribution to the raw-return problem is the exact occupation/window theorem in item 4.

## 6. Specialist audit and source imports

No independent human specialist audit has been obtained. `SPECIALIST_AUDIT_MAP.md` states the continuum assertions requiring that audit. The source checks and finite arithmetic do not establish them.

The norm references are now pinned at the point of use. DZ Lemma 3.2(a)--(d), page 12 of arXiv:1210.1261v1, supplies the never-long, total-Jacobian, length-weighted, and inverse-Jacobian-power sums. DZ Lemma 3.3, pages 13--14, gives the matched graph and Jacobian estimates with its intermediate-regularity hypotheses. Proposition 4.1 and equations (4.1)--(4.3), (4.7)--(4.11), (4.14), (4.18) identify the three norm calculations. The section multiplier is checked against DPZ Lemma 3.3(b), page 13 of arXiv:1902.06850v1. The published DPZ reference and its preprint-numbering note remain unchanged.

## 7. Portmanteau, selectors, and limits

The corrected module-70 hypothesis is inherited byte-for-byte. Closed exceptional neighborhoods of small limiting measure and null boundary remain required in every varying endpoint passage. The new support-function application checks this condition explicitly.

Regular endpoint amplitudes are still distinguished from arbitrary bounded posterior tests. A positive selected denominator requires a uniformly positive product of regular selector means. The total-variation norm is fixed explicitly as `sup_{|F|<=1}|mu(F)-nu(F)|`; the probability distance `sup_A|mu(A)-nu(A)|` is half of it. The compact-family and occupation local laws are qualitative `o(1)` statements. The polynomial posterior comparison uses its separate explicit source error and a proved denominator, not a growing-band spectral constant.

## 8. Version and execution evidence

The two revision-37 branches start at the latest report commit and receive the same new mathematical tree. The source manifest, article date, active directory and qualification workflow agree. The old revision-36 aliases and all previous manuscripts and reports are preserved.

`build.sh` rechecks the frozen actual revision-35 source, runs the new source/finite checks normally and with `-O`, compares the outputs, runs inherited diagnostics and compiles the full article natively. The read-only workflow archives the exact source and reports; its dynamic receipt carries the checked-out event SHA, run ID and attempt, scoped-source cleanliness, source hashes and PDF hash. The page-render receipt derives its page numbers from the actual LaTeX labels. A successful build is reported only after observing the corresponding completed run; it is not mathematical proof certification.

We submit this actual new author source for a further review of the exact occupation multiplier, the mixed local--central theorem and return disintegration, the repaired functional-analytic endpoint, the finite-cover input, and the nonelliptic verification, together with the retained original raw-return problem.
