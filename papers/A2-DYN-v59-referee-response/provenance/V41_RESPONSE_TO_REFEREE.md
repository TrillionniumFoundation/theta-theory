# Response to the external referee: A2-DYN revision 41

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Latest controlling report at the start of this revision:** `reviews/a2-dyn-v39-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Review commit / blob:** `a76fcf9d6ef7288ea324fed327c4f2f0ce088461` / `34fd05b1740816104f38ca84c75826b11eec1694`.  
**Source reviewed by that report:** `75eda04842b69319ae81c97ce1502129d55ee5fc`.  
**Immediate mathematical baseline:** v40 at `d07c73f9db6a27c216fcfb2f32f844d63858c90b`.  
**Frozen complete v40 paper tree:** `647d3d842655bf71e1d64afdc3321b016c190229`.  
**New manuscript:** `papers/A2-DYN-v41-referee-response/main.tex`.

The repository already contained a substantive v40 response when this revision began. We therefore continue from that author source rather than returning to v35 or to an empty v36 branch. The v39 report remains the latest controlling report found; no unobserved v40 review is attributed to a referee. The title, actual section, physical family, full four-coordinate return record and original pointwise raw-density target are unchanged.

Revision 40 supplied full fixed-band long powers, finite endpoint residues and a fixed-radius arithmetic interval local law. Revision 41 evaluates the parameter transitions left unevaluated there and proves a microscopic conditional bridge for the same actual return record. Three new complete proof modules are included in the article.

## 1. Fixed-count control, not an Abel average

Module 87 evaluates the rank-one integrals of the v40 fixed-count spectral decomposition. Near each genuine resonance at a reference radius, it continues the scalar eigenvalue and locates the unique real maximum of its modulus at neighboring radii. The resulting data are the peak frequency, eigenvalue, nonnegative damping exponent, real drift, complex symmetric Gaussian curvature, and actual section endpoint coefficient.

`thm:v41-uniform-transition` gives an explicit finite Gaussian expression for `m^2 P{K_n=k,N_n=m,T_n-t in J}`, uniformly in the radius, including sequences crossing changes of arithmetic type. This is stronger than an unevaluated finite spectral inverse. The expression retains `lambda_peak(R)^m`: a branch strictly inside the unit circle is not discarded when its damping is of order `1/m`. At a fixed radius the formula reduces to the v40 arithmetic factor times the original Gaussian. It does not replace that factor by one.

Scalar endpoint continuity is proved using fixed physical pairings and uniform spectral approximation, not a presumed strong-norm continuity of a moving indicator. Twist-derivative continuity follows from a normal-family argument and Cauchy's formula on common complex frequency disks; the table parameter is not differentiated.

## 2. Every resonance residue, including near-resonant contributions

The v40 general projection formula remains the residue input. The new transition formula keeps its analytically continued endpoint amplitude on every chart. At an actual resonance it is exactly the squared section mean, at any scalar eigenvalue. Near such a point it may be complex and may decay with the iterate; both features remain in the formula.

`thm:v41-zero-residue-criterion` gives a necessary and sufficient condition for the radius-uniform unmodulated exact-index interval law on a compact parameter set: all nontrivial section residues vanish. Equivalently, the section phase-class masses are uniform. The sufficiency proof controls approaching, nonperipheral branches by compactness and their damping, not just the exact resonance at each radius. The condition is not asserted verified for every radius of this family.

## 3. The nonresonant complement

The full-torus inequalities and peripheral decomposition in v40 remain load-bearing, inherited inputs. The new work adds neither a continuous-spectrum shortcut nor a new unverified induced spectral gap. Its nonresonant error is exponentially small on each fixed roof band. The phase charts can be fixed near zero roof frequency because all actual occupation resonances have zero roof coordinate. Enlarging a fixed outer band adds only a compact nonresonant region.

`lem:v41-peak-derivatives` gives uniform derivatives through order four of centered block powers. Centering at the moving peak drift is essential. A Cauchy circle of radius proportional to the inverse square root of the block length gives the Gaussian derivative scale; complementary powers remain exponentially small after this centering.

## 4. A genuine conditional path consequence at exact indices

Module 88 proves the new Theorem 6 path assertion. The conditioned event is exactly

`E = {K_n=k, N_n=m, T_n-t in J}`

under the original normalized section probability. Both displacement coordinates and the collision count are fixed integers. The roof interval is fixed and positive. There is no replacement event and no averaging of the conditioning return index.

For a collision path tied to its own actual endpoint, the block frequency shifts have exactly zero length-weighted sum. Consequently both the linear drift and the mixed Gaussian term cancel on every continued spectral branch. Branches which survive the collision limit have curvature tending to the same actual `Omega_R`; their arithmetic coefficients therefore cancel between the marked and unmarked local probabilities. This proves an unnormalized, radius-uniform pinned characteristic factorization.

A separate fourth-moment proof is provided. It differentiates the chronological three-block pairing for an increment minus its fraction of the actual total record, uses a fixed positive roof majorant, and retains the four-frequency volume factor `m^(-2)`. It gives the unnormalized bound `C_J l^2 m^(-2)`. Division is performed only after this bound, under the explicit assumption `m^2 P(E) >= epsilon`. This yields continuous-path tightness, not only finite-dimensional convergence.

The exact half-open occupation identity then transfers the bridge to genuine return times. The polygonal process with values `(J_l-(l/n)J_n)/sqrt(n)` converges to the centered Brownian bridge with covariance `D_R`. The clock and process are not assumed independent. At each fixed radius all positive arithmetic classes already have the required denominator by v40, so the bridge is unconditional within that proved class. The radius-uniform theorem states its microscopic denominator condition explicitly.

## 5. Pointwise roof inversion

The new transition theorem is a sharp fixed-interval law. Its diagonal corollary also gives a common slowly shrinking interval, but no prescribed polynomial shrinking rate. A shrinking-interval law does not automatically control smaller density spikes. The common pointwise coarea correction, complete critical/singular edge control, and full roof-frequency tail remain requirements of the unchanged raw-density theorem.

The new conditional bridge is therefore an exact-index, interval-roof path theorem, not a pointwise roof-conditioned theorem. The manuscript and metadata keep these statements separate. No finite diagnostic changes a raw-density proof flag.

## 6. Uniformity, cutoffs and a finite resolution theorem

Every spectral calculation fixes the roof band before the collision limit. The positive-envelope limit enlarges the band afterwards. The transition kernel is built from fixed near-resonance charts, so it does not depend on a later growing bandwidth. No polynomial error rate for the local theorem or uniform lower bound for every positive residue across radius changes is claimed.

Module 89 also proves a radius-uniform unmodulated law for a fixed finite packet of consecutive return indices. Its length is a common multiple of the uniformly bounded resonance orders, independent of the collision count. The exact finite index sum inserts a trigonometric polynomial which annihilates every possible nonzero occupation resonance. Damping and continuity control nearby nonperipheral branches. The packet need not diverge, unlike the earlier fine-window theorem.

The packet is a separate original-event union, not a substitute for the preassigned singleton in the bridge theorem. It supplies a positive packet denominator and guarantees at least one exact constituent event with natural microscopic mass at every central target and radius. No numerical value of the inherited order bound is asserted.

## 7. Independent specialist audit

No independent human audit has been obtained in this author revision. The new proof uses the inherited full-torus curve refinement and anisotropic estimates; these remain specialist audit items. `SPECIALIST_AUDIT_MAP.md` separates those continuum inputs from the new scalar continuity, peak expansion, pinned block products, fourth-moment estimate and genuine-clock argument.

Finite tests check exact Gaussian pinning algebra, complex Gaussian normalization, finite bridge moments, half-open return identities, finite filters and counterexamples to invalid inferences. They do not certify the billiard estimates, spectral realization or complete raw theorem.

## 8. Generality and novelty

Gaussian conditioning and Brownian bridges are not claimed as new general objects. The new result is a transfer from a compact-family finite-resonance local inverse to a tied path under the actual rare return event, with the arithmetic coefficient allowed to change with the table. The decisive cancellation is performed before division by a probability, and the fourth-moment estimate is in the local scale rather than the unconditional scale. It requires no mixing theorem for the induced map.

The method is stated in the present mechanical setting with exact references to every inherited input. Its reusable part is the finite collection of analytic scalar branches with Gaussian maxima, a decaying fixed-band complement, a physical endpoint pairing, and an exact additive/return-clock identity. The existing prior-art comparison with collision, mixing-local-limit and suspension frameworks is retained; no assertion of historical priority or automatic top-four acceptance is made.

## 9. Article structure and preservation

Theorem 6 states the uniform exact-index transition law and the microscopic return bridge. The direct Part II route adds modules 87--89 immediately after the v40 exact-count modules. All 86 inherited core files, all 99 inherited Python scripts, the bibliography, and the compiled A--X synopsis remain byte-identical. All 1141 inherited mathematical labels remain. Previous front matter and source records are archived under `provenance/V40_*`.

This is an extension of the same article, not a topic change, a replacement paper or a venue downgrade. The original pointwise target remains explicit. The new response identifies which requests were already addressed in v40, which are advanced by v41, and which are not closed by the present proofs.

## Execution evidence

The immediate baseline is the successful v40 copy run `37712106593`, artifact `11522510709`, archive SHA-256 `c00600988509686535fab99545f974213997d833daae0c86eb3ecfb497cd9198`. The archive was downloaded and its digest and complete baseline source tree were checked locally. That run is baseline evidence only.

The new read-only workflow verifies the exact v41 ordinary source, frozen v40 tree, original controlling-report blob, inherited byte identities, all theorem labels and inclusions, normal/optimized finite diagnostics, native TeX and actual-label proof-page rendering. The dynamic receipt records the actual final event SHA, run ID, PDF hash and source cleanliness. No v41 run is declared successful in advance.
