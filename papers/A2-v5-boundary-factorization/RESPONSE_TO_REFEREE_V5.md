# Response to the independent referee: A2 v5

**Author:** Qian Qi.  
**Date:** September 9, 2026.  
**Revised article:** *Relative boundary factorization and collision thresholds in periodic dispersing billiards*.  
**Controlling review:** `ec861ecfcdd83a81880c1a9082becc19b0c76977`, `reviews/a2-v4-nonlinear-boundary-laws-harsh-independent-2026-09-09/REFEREE_REPORT.md`.  
**Reviewed manuscript:** `68bbf5b841a66dcc2b85f4d76ce66b1ae8b9782f`.  
**New directory:** `papers/A2-v5-boundary-factorization`.

The report credits the nonlinear relative-flux analysis and concludes that the previous OBS requests received substantive answers. Its remaining negative recommendation concerns importance and positioning, rather than an established fatal counterexample. We have treated that distinction literally. The revision neither withdraws the nonlinear theorem nor presents additional finite checks as a substitute for a mathematical importance argument. It adds a reusable factorization theorem, a positive pairwise inverse at the singular exponent identified by the referee, and a different recorded-data normalization that improves calibration sensitivity. Every previously active mathematical label is retained.

## NBL-R1: distinguish nonlinear information from an order-dependent information hierarchy

**Requested distinction.** The fixed-leading-data fourth-jet fiber separates nonlinear probabilities from the leading hierarchy. It does not show that its parameter first becomes visible only in long records.

**Response.** Proposition 7.3 (`prop:v5-one-flight`, `v5/30_nonlinear_information.tex`) places the one-flight comparison immediately after the realized geometric fiber. With the manuscript's notation it proves

\[
\partial_q\mathcal R_1(0)=-\frac{g^2c^2}{12(c^2-1)^2},\qquad
\left.\partial_s\mathcal R_1^{(s)}(0)\right|_0=\frac89.
\]

The long-bridge derivative remains \(\sqrt3/2\). The one-flight action has no interior variables; its fourth-jet variation has no quadratic mixed-amplitude term. The proof computes the physical residual-time-weighted quartic integral and explicitly records the empty interior determinant. The introduction and comparison section distinguish these two observations. We do not claim a strictly increasing inverse-information hierarchy in collision order.

The additional analytical content is now formulated independently of the period-two model. **Theorem 5.1**, `thm:v5-chain-factorization`, proves uniform relative factorization for a spatially varying sequence of scalar nearest-neighbor generating functions. Its assumptions are a common coordinate box, positive twist bounded above and below, uniform endpoint convexity exceeding the twist by a positive margin, and bounded fixed-order derivatives. Periodicity and an explicit hyperbolic Green formula are not assumed. The theorem gives smooth half-line actions and relative Fredholm amplitudes, a common endpoint box, and an exponential rate independent of the interval endpoints and length.

The proof gives the Neumann-series Green bounds, finite-to-half-line kernel comparison, weighted stationary-segment construction, uniqueness, nonlinear gluing, cofactor identity, trace-norm boundary truncation, and differentiated determinant comparison. The small flux is normalized by an exact cofactor identity, not by dividing an absolute action error. The period-two billiard construction and its explicit constants remain in Section 6. Its full-phase physical limit, Theorem 6.3, remains a separate step using the suspension measure and a common Morse construction. This is the revised central chain, rather than an enlarged interpretation of the scalar fourth-jet example.

## NBL-R2: a positive, sharp pairwise inverse

**Requested distinction.** The circular-reference exponent one half is correct but does not extend to arbitrary pairs of nearby noncircular tables. The referee's two-sided path has cubic amplitude cancellation.

**Response.** The circular-reference results, Theorems 12.1 and 12.2, are retained with their original reference-point statements. **Theorem 13.1**, `thm:v5-pairwise`, proves a different positive theorem: on a sufficiently small fixed-gap neighborhood in the realized three-parameter support-function family,

\[
\operatorname{dist}_{\rm match}(\kappa,\widetilde\kappa)
 \le C\left(\max_{1\le j\le4}|C_j-\widetilde C_j|\right)^{1/3}.
\]

The same four amplitudes give a Lipschitz estimate for the area normalizer. The theorem is pairwise, includes repeated curvatures, and needs neither channel labels nor prior area knowledge. A compact-image minimum-discrepancy reconstruction gives the corresponding finite-noisy-data guarantee. The four amplitudes here are limiting threshold coefficients, not raw counts with their acquisition cost suppressed.

The proof passes to the three elementary symmetric functions of the shifted contact variables. A temporary analytic enlargement allows the area normalizer to be an independent coordinate for the Jacobian calculation; it is then restricted back to the actual geometric family, where area is a symmetric dependent quantity. No fourth independent physical shape parameter is asserted. Lemma 13.2 computes the four-amplitude collision Jacobian explicitly and proves that it never vanishes for \(c>1\). The inverse bound holds in a convex coefficient neighborhood. Lemma 13.3 gives a multiplicity-preserving cubic-root matching estimate by Rouché's theorem; mere Hausdorff proximity would not suffice.

The theorem also incorporates the actual two-sided geometric path from the report. Its weighted whole-sequence discrepancy is comparable to \(|s|^3\), whereas its curvature matching distance is comparable to \(|s|\). The strict exponential margin absorbs the third-derivative polynomial in the flight number. This proves that the attained pairwise exponent one third is sharp, even when the whole absolute-error sequence is supplied. The radial exponent one half and the pairwise exponent one third therefore coexist; neither theorem is used as a replacement for the other.

## NBL-R3: timing sensitivity and a residual-normalized experiment

**Requested distinction.** Extrapolation cancels calibrated offset powers but does not cancel the leading sensitivity caused by a wrong programmed-offset denominator. Calibration is not included for free in the preparation count.

**Response.** Proposition 10.1 (`prop:v5-harmonic`) proves the report's harmonic identity and the precise derivative

\[
P_b'(0)=-v_{j,b}H_m/h+O_m(1),\qquad \tau=j\Delta g.
\]

The original estimator, its known-gap qualifications, and its \(h^{m+1}/j\) sufficient calibration remain unchanged in Section 9.

The revision also uses an additional observable already present in the physical collision record: the time \(r\) from preparation to the first impact. Lemma 10.2 proves the uniform smooth expansion \(3\mathbb E r/d=1+O(d)\). Thus

\[
T_{j,b}(d)=\frac{\operatorname{Var}(Q_b)}{3\mathbb E r}
          =v_{j,b}+d\,t_{j,b}(d)
\]

has a uniformly bounded offset derivative. **Theorem 10.3**, `thm:v5-residual-recovery`, estimates this ratio with a clipped positive denominator from independent successful preparations, and extrapolates at the same programmed windows. Its curvature error is bounded by

\[
C_m\left[h^m+\sqrt{\log(C_m/\eta)/K}
                   +j|\Delta g|+|\Delta g|\right].
\]

There is no inverse-offset factor in this bound. Preserving an order-\(h^m\) deterministic error requires only the sufficient scale \(|\Delta g|=O_m(h^m/j)\), with the stated positive-window condition. The estimator uses residual times in addition to endpoint positions; it is not described as a repair using exactly the old endpoint-only datum.

The proof includes bounded-variable concentration for both numerator and denominator, handles their within-window dependence without an independence assumption, applies the uniform gap--variance inverse, and gives expected and simultaneous high-probability waiting-time bounds. The sufficient preparation order remains \(e^{j\gamma}\epsilon^{-(2+2/m)}\) times the stated logarithm, at fixed extrapolation order. It is not a minimax claim. The gap is still externally supplied to the inverse, with quantified error. No experiment for learning an unknown gap, no sensor-noise model, and no cost for such an experiment are silently included.

## Secondary requests: determinants, poles, and literature

The operator-norm bounds on all fixed derivatives of the Green operators and the trace-norm bounds on the Hessian perturbations are now displayed before the determinant comparisons, in Sections 5 and 6. Their product derivatives retain a trace-class factor. Green derivatives are not incorrectly called trace class.

The paragraph following the onset-series decomposition explicitly states that derivatives of a geometric parameter moving \(\gamma\) may increase the order of the principal poles. The holomorphic remainder and its derivatives retain the stated smaller domains. The series still uses a different physical window in each coefficient and is not promoted to a fixed-window dynamical zeta function.

The comparison section and bibliography now include De Simoi--Kaloshin--Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, Inventiones Mathematicae 233 (2023), 829--901, DOI 10.1007/s00222-023-01191-8. The axial-symmetry, analyticity, and genericity hypotheses and the difference between marked-length and probability data remain explicit. No absence-of-search-result argument is used to certify priority.

## Article structure and preservation

The article begins with the collision-threshold problem and the relative boundary mechanism. The abstract chain theorem, explicit billiard specialization, and full-phase limiting law form its main sequence. Inverse observations and acquisition estimates follow that sequence. Referee-specific discussion is concentrated in this letter and the proof ledger, not used as the article's organizing narrative.

All 176 formerly active v4 labels remain active. The original geometric and flux proofs, exact equal-gap inverse, scalar fibers, endpoint metric inverse, marked response, circular calculations, two-collision companion, and preserved Round 33 source remain available. Original `v3` and `v4` source files are not edited in place; the amended sections are new files in `v5`. Old entry-point metadata and the previous main source are preserved under `history/v4-publication`. The publication is made on a new revision branch with the controlling review as its parent, not by overwriting a review branch or merging into `main`.

## Executed validation and limits

The full native build produced the 55-page article and the unchanged 7-page companion with stable auxiliaries, no undefined or duplicate references, no overfull boxes, and no substituted statements. The recorder agrees with the complete declared source closure. All 55 article pages were inspected as rendered contact sheets, with selected mathematical pages additionally inspected at enlarged resolution.

The new independent finite diagnostic script passes 141 checks: 90 exact symbolic/rational checks, 39 ordinary floating-point checks, and 12 high-precision non-interval checks. Normal and optimized Python outputs are identical. The four inherited suites were also rerun normally and with `python -O`: 411 threshold, 328 geometry, 257 observability, and 252 boundary checks passed, with matching outputs. These are execution reports, not proof-assistant or interval certificates. We did not rerun the latest referee's separate 81-check script, execute remote CI, or simulate the full equilibrium billiard.

The new assertions are offered with complete mathematical proofs for renewed independent scrutiny. Neither the test count nor this response supplies an editorial judgment about their importance.
