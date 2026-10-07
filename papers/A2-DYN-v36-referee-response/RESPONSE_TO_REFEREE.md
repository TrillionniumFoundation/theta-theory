# Response to the external referee: A2-DYN revision 36

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v35-external-top4-review-2026-10-07/REFEREE_REPORT.md`.  
**Frozen review commit / blob:** `8bcdf384a36b6bbc86e276b128354dc5766b99e2` / `e7d2a7ea4932d5d7354ddfbd279ae04047e7b647`.  
**Reviewed author SHA:** `fda52bb72045204b50159e8263c05afaa6a9dc58`.  
**Frozen full author paper tree:** `1634006e867a2258b09d85db6f9fcecc668f53d1`.  
**Revised article:** `papers/A2-DYN-v36-referee-response/main.tex`.

We thank the referee for the detailed audit and for distinguishing the completed stationary theorem from the original raw four-coordinate return problem. This revision addresses the v35 report. It preserves the title, mechanical setting, actual return record and its raw mixed-density target, while proving a new exact-event conditional path theorem and answering the identified analytic and geometric clarification requests. The new bridge is a theorem on the original stationary singleton, not a replacement by a return event or a smoothed observation.

## 1. Principal endpoint and the new microscopic path theorem

The original common pointwise return correction and complete return-frequency complement are not inferred from a three-coordinate collision theorem. They remain explicit requirements in Part II. We have neither removed those results and interfaces nor relabelled the physical theorem as the four-coordinate raw-return theorem.

The substantial new endpoint in this revision is `thm:v36-microscopic-path-bridge`, stated as Theorem 3 in the introduction. On the exact stationary event `{W_lambda(t)=k, C_lambda(t)=m}`, the physical path

` t^(-1/2) (W_lambda(ts), C_lambda(ts)-ts/bar_tau_lambda), 0<=s<=1 `

converges in conditional law to the Gaussian bridge with endpoint `xi_(t,lambda)(k,m)` and covariance kernel `(min(s,u)-su) V_lambda`. The distance is uniform on central compact sets and compact parameter families satisfying the separated inputs. The theorem also covers the specified nonnegative regular endpoint selectors with uniformly positive products of stationary means. This closes the stationary microscopic bridge scope formerly left outside the proved local law; it does not assert an arbitrary selected-path Gaussian amplitude or the original four-coordinate density theorem.

The proof is in two new modules. Module 77 differentiates one deterministic block in the exact collision-operator product. Near zero, its fourth derivative is bounded by `(l^2+l^4|omega|^4) exp(-c l|omega|^2)`; outside zero, on each fixed band, at most four derivative insertions leave total undifferentiated length at least `m-4`. Fourier integration against a fixed positive interval majorant gives the **unnormalized local fourth moment** `C l^2 m^(-3/2)`. The exact age-overlap formula and the proved original denominator then give conditioned polygonal increments of fourth moment at most `C(l/m)^2`. This proves tightness without losing a factor `m^(3/2)` by an unconditional moment bound.

Module 78 inserts separate frequencies in successive collision blocks and evaluates the endpoint Fourier integral. The Gaussian exponent is the conditional covariance of independent Gaussian increments given their total, not their unconditioned covariance. For complex probes, the error in interval approximation is dominated by an unprobed positive upper-minus-lower envelope. Every spectral band is fixed before the collision count tends to infinity. Endpoint overlap tests use exactly the corrected closed-exceptional-neighborhood condition. The actual initial age and both cell offsets remain throughout. Finally conditional tightness controls the physical clock on the same event; the exact clock identity identifies the physical covariance and pin. No independence of the clock and path is needed.

The positive-band posterior has the same bridge by contraction of total variation under the original path map. Its `O(m^(-P))` distance is a comparison between two source posteriors, not a rate of convergence to Brownian bridge.

## 2. Independent specialist audit

No independent human specialist audit has been obtained during this author revision. It is not claimed in the source, manifest, receipt or publication status. `SPECIALIST_AUDIT_MAP.md` isolates the original norm/matching inputs and the new differentiated-block, local-moment, endpoint-probe and conditional-clock arguments. The proof text, finite diagnostics and build evidence are supplied for that audit, not as a substitute for it.

## 3. Finite-cover mixing

New `prop:v36-cover-mixing` states the input separately. It applies Young, Section 8.1, Theorem 6(b), to each actual finite lattice cover, which is again a finite-horizon planar dispersing billiard with finitely many C3 strictly positively curved obstacles on a Euclidean flat torus. That is a collision-map correlation theorem; the statement preceding it explicitly records total ergodicity in this class. Smooth/Hölder correlation mixing extends to L2 observables by invariant L2 approximation, so it applies to the bounded physical character constructed in the arithmetic proof.

For the triangular lattice one may use the rectangular Euclidean cover with periods `(p,0)` and `(0,p sqrt(3))` and then pass to the `p Lambda` factor. No affine distortion of the reflection law is used. No rate uniform in the number of sheets is required. The text separates mixing for the nontrivial constant-step eigenvalue from ergodicity for the mean-zero invariant character. Connectedness is no longer used as shorthand for mixing. Module 74 explicitly invokes this proposition for the ellipse application.

## 4. Noncircular strong-space faithfulness

The final paragraph of `lem:v35-faithful-strong` has been replaced by a direct conclusion in the two strong seminorms. Transverse averaging first annihilates each smooth stable-curve pairing. Density of smooth tests in the little-Cq class gives every stable pairing. Each unstable coordinate is a scaled difference of two such pairings, so it also vanishes. The map to the two bounded coordinate families is isometric for the strong norm and its completion has closed range. All coordinates zero therefore imply strong norm zero. The argument does not assume the injectivity of the strong-to-weak inclusion it is meant to clarify.

This is an exact, recorded proof edit. The former module is preserved under provenance; no statement or label was deleted.

## 5. Exact continuum source locations

Module 76 and `SOURCE_INPUT_MAP.md` pin the four Jacobian/length sums to Demers--Zhang, arXiv:1210.1261v1, Lemma 3.2(a)--(d), and locate last-long-ancestor payment, matching, unmatched pieces, and test/Jacobian errors in the relevant displayed equations. They pin the multiplier and completion conventions to Demers--Pene--Zhang, arXiv:1902.06850v1, Lemmas 3.2(c), 3.3(b), footnote 7 and Lemma 3.9. The bibliography remains byte-identical to v35, retaining the published DPZ citation and the preprint numbering convention. The Young finite-cover source is the author preprint ESI 445, Theorem 6(b).

These are source locators and declared continuum inputs, not claims that finite regression tests prove their geometric hypotheses.

## 6. Reusable separated hypotheses

New module 76 lists H1 mechanical geometry; H2 local common collision spaces and unweighted estimates; H3 finite-cover mixing and product structure; H4 action and regular matching; H5 preceding-flight multiplier partition; H6 parameter comparison; and H7 one-flight observations and regular endpoint selectors. The local-family theorem points to this list rather than bundling all inputs into uniform table geometry. Local common Banach spaces on a finite cover are distinguished from one global space. Fixed-band dependence, qualitative local convergence, null boundaries, closed exceptional neighborhoods and selected denominator conditions remain explicit.

## 7. A verified application beyond ellipses

New module 79 verifies H1--H7 for fixed-degree support functions

`h(theta)=r+sum_(j=2)^D [a_j cos(j theta)+b_j sin(j theta)]`,

with `r in [91/200,93/200]` and `sum (j^2-1)sqrt(a_j^2+b_j^2) <= 1/200`. The rotation-invariant coefficient bound puts the curvature radius in `[0.45,0.47]` and the support function strictly between the corresponding disk supports. Rational trigonometric charts and fixed-degree quantifier elimination give a one-flight finite-complexity partition before normalizing arclength. Tangency has a uniform nonzero quadratic curvature term, giving the required one-half-Hölder roots. The observation exceptions admit the same closed-neighborhood treatment. The degree is fixed before constants are chosen.

The example `h=23/50+epsilon cos(3 theta)`, `0<|epsilon|<=1/1600`, is not centrally symmetric; a translation changes only the first harmonic and cannot remove its third harmonic. Thus this application is not a reparametrized ellipse. The exact perimeter, area and mean roof are computed. Both the local law and the new conditional path bridge hold uniformly for this compact family on the original lattice.

The theorem-level comparison continues to acknowledge existing collision and suspension local-limit theory. A microscopic conditioned path limit requires the new local moment and multiblock arguments; it is not inferred from a scalar local theorem or posterior comparison alone. No unverified historical priority claim is made.

## 8. Journal architecture and preservation

The introduction contains three principal results, and Part I has a direct proof route to them. The new local moment and bridge proofs follow the compact-family theorem; the nonelliptic family is a checked application. Part II and the compiled A--X appendix retain the entire original return analysis. All 75 inherited core modules remain compiled. Exactly two cores receive recorded clarification edits; 73 are byte-identical. All 83 inherited Python scripts, all 1,010 inherited mathematical labels, the bibliography and all 24 A--X statements remain. The v35 main and the two edited modules are retained under provenance.

The requested original topic and raw target have not been replaced by a separate paper. The statement of what each theorem proves is kept precise rather than obtained by deleting the remaining problem.

## Technical comments 1--14

The equivalent norm still depends on a fixed band; no growing-band spectral constants are controlled. The ellipse quadratic now explicitly uses the minus root for first entry when `C0>0`, `B0<0` and the discriminant is positive; the current-obstacle zero root is removed before minimizing. The finite-complexity partition is built before normalized arclength; a smooth monotone coordinate change then preserves its properties. Circular orientation remains redundant but harmless. Every regular selected assertion points to H7 and its denominator condition. Total variation is the full variation norm, twice the supremum event discrepancy for probabilities. Local and bridge limits are qualitative. Arbitrary bounded posterior tests remain distinct from regular selector Gaussian amplitudes. Published/preprint citations, local spaces, the separate roles of mixing and ergodicity, and the count-as-suspension-reward identity are retained. The physical singleton theorem is not called the full four-coordinate raw-return theorem.

## Exact execution evidence

The frozen baseline has two successful runs: `37640998381` and `37641024948`, at `fda52bb72045204b50159e8263c05afaa6a9dc58`. Its response artifact is `11491613256`, digest `34c64e0fe01633f8ac55d4cc654c6f12105f6f5d7565ad585f162313da29baec`. These are baseline records only. New runs are reported only after execution. The new workflow checks the exact ordinary source tree, explicit edits, all inputs and labels, normal/optimized diagnostics, native typesetting and proof-page renders; its dynamic receipt records the actual event SHA, run ID and PDF hash.
