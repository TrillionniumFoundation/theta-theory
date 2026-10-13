# Response to the external referee: A2-DYN revision 59

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling review:** `reviews/a2-dyn-v58-external-top4-review-2026-10-09/REFEREE_REPORT.md`.  
**Frozen review commit/blob:** `94c9ef54bd84d9eb04fbd3b4d3431776beab64de` / `d70134c2f027a53d8bde20187a2b3b706011782c`.  
**Reviewed author SHA:** `b9c8e1f15b65e4843d1321f23ed5b816378b855c`.  
**Frozen complete paper tree:** `e7be5ba545bfc80e08c86e3c596e36b483bbedf7`.  
**New source:** `papers/A2-DYN-v59-referee-response/main.tex`.

We thank the referee for the detailed audit of the flat-contact and canonical-reference arguments. The present revision preserves the original Lorentz record and unrestricted pointwise target. It supplies the requested standalone scalar details and a correlated singular realization in which a continuous roof density and positive source heights are actually estimated. The latter tests additional geometric inputs rather than relabelling a finite-digit characteristic function as a density theorem.

## 26.1--26.4. Incidence/clearance heights and same-roof consequences

The existing Lorentz height problem has been checked against the exact positive source split in modules 104, 108 and 110, the physical image-side multipliers in 105--106, and the finite protected-height and endpoint bounds in 115--120. The estimates available there are not silently upgraded from local variation, weak integrability or good-anchor control to a uniform essential supremum.

No proof of the two Lorentz incidence/clearance essential-height estimates is claimed in this revision. Accordingly the unrestricted four-coordinate pointwise law and its unrestricted same-roof/forward-essential-likelihood consequences remain unproved. The actual word, exact discrete labels, half-open occupation convention and clearance mark at the next collision remain unchanged. This statement records the precise remaining work; it does not remove, replace or declare impossible the organizing endpoint.

New `thm:v59-markov-boundary-height` proves the analogous kind of positive essential-height bound for three explicitly specified boundary sources in a different singular deterministic realization. It identifies exactly the extra input used: a stable coarea derivative bounded below independently of the word, plus positive cylinder local bounds. Those inputs are proved for that model and are not assumed for Lorentz incidence or competing-hit seams. No orbit is continued through a Lorentz seam by this comparison.

## 26.5. Independent verification

No independent human specialist review has been obtained. `SPECIALIST_AUDIT_MAP.md` retains the Lorentz audit obligations and adds precise checks for the new operator, spectral quotient, coarea identity and positive cylinder bound. Finite computations check coefficients and exact finite sources, not continuum proofs.

## 26.6. A correlated realization with an actual density consequence

Module 126 constructs a two-state Markov baker map with transition matrix `[[3/4,1/4],[1/3,2/3]]` and invariant state weights `(4/7,3/7)`. Its state covariance is `(12/49)(5/12)^r`, so the chosen observations are not independent. This is not a claim that a mixing Markov shift lacks a Bernoulli isomorphism.

The roof is `3+j+epsilon*i*j+y_next-y`. It is positive, continuous along each regular stable fiber and has genuine jumps on the map partition. Its roof sum retains the actual stable endpoint difference. The proof constructs an infinite-dimensional Lipschitz conditional-expectation operator. Its quotient by functions constant on stable fibers contracts, while its two-dimensional invariant subspace carries the matrix pressure. A block resolvent argument gives the full local splitting needed for physical scalar witnesses; the witnesses are fixed endpoint functions, not frequency-dependent tests introduced after the estimate.

The pressure covariance is `[[204,192],[192,198]]/343`. The new peak satisfies

`a_epsilon=2*pi-(32*pi/17)*epsilon+O(epsilon^2)`,

`kappa_epsilon=(12*pi^2/119)*epsilon^2+O(epsilon^3)`,

`v_epsilon=-(3456*pi^2/99127)*epsilon^2+O(epsilon^3)`.

All coefficients are derived from the characteristic polynomial, with the centered logarithm written immediately beside the drift calculation. The continuous roof has the same pressure and covariance by its bounded endpoint coboundary. Contact at the actual zero-damping locus follows from an exact complex-frequency identity. Thus the difficult abstract hypotheses are verified for this physical pairing, rather than postulated for a finite exponential sum.

Module 127 then proves, at epsilon zero, the complete continuous-roof estimate

`ess sup_t |sqrt(m)*p_m(t)-g_sigma((t-24*m/7)/sqrt(m))| <= C log(2+m)/sqrt(m)`

with `sigma^2=204/343`. The proof does not differentiate a weak limit. It writes the exact finite-word coarea density, proves a positive stable-cylinder local bound uniformly for cylinder depth up to `m/2`, and sums all words. For initial forward-cut strips, terminal backward-cut strips and initial-age boundary strips, the normalized essential heights are at most `C(s+(3/4)^floor(m/2))`. No exceptional roof set is deleted.

The regular endpoint-weighted density theorem keeps a one-periodic overlap factor, not a presumed product of means. The unweighted factor is one by an exact triangle periodization. The density theorem is not asserted uniformly for epsilon different from zero; the perturbed family verifies pressure contact. This separation prevents an unwarranted extension of the pointwise claim.

The model remains an explicitly solvable coboundary extension of a finite-state additive process. It is more demanding than the previous independent finite-support example, but is not presented as a replacement for billiard singularity growth or as a complete universal theorem for singular hyperbolic systems.

## 26.7. Standalone scalar proof details

Module 125 supplies `lem:v59-physical-root`, with the amplitude lower bound used before taking roots and the exponentially small remainder retained in the inequality. `lem:v59-witness-cover` states the compact-cover argument independently. `lem:v59-accretive-gaussian` prints the Hermitian inverse identity, determinant branch and exact center/matrix derivatives. The explicit diagonal is `delta_m=min(delta_0/2,m^(-1/2))`. The real quadratic gap norm `h_j` and the full complex modulus `omega` remain different quantities.

The inherited modules 123--124 are unchanged, so the referee can compare the additional proofs without an unreported rewrite of the previously audited chain.

## 26.8. Proof route and preservation

The opening retains two principal Lorentz statements and adds a short paragraph identifying the correlated test and its separate scope. The direct route is root/Gaussian details, flat contact, canonical arithmetic reference, and the inherited global tail/graph-coupling inputs. The independent continuous-roof calculation is self-contained in two sections. `JOURNAL_ROUTE.md` provides exact labels and dependencies; source hashes and qualification records stay outside the mathematical body.

All 124 inherited core modules, all 167 inherited Python files, all compiled appendices and every old mathematical label are retained. The old main, bibliography and eleven supporting files are preserved under `provenance/v58-*`. The bibliography only appends the Markov additive density comparison. No historical referee report or unrelated paper path is changed.

## 26.9. Literature and novelty

The retained comparison with Szász--Varjú, Demers--Pène--Zhang and Dolgopyat--Nándori concerns the exact record, arithmetic transition and path topology. The new comparison with Hervé--Ledoux explicitly acknowledges finite-state Markov additive density theory. Analytic Perron perturbation, finite-state lattice local limits, pressure domination and Gaussian differentiation are not claimed as newly discovered methods.

The revision's mathematical addition is the explicit correlated continuous-roof verification, with the singular deterministic coding, physical operator, moving-peak coefficients, pointwise coarea inversion, endpoint overlap and positive boundary heights checked together. Its relation to the Lorentz problem is an identified sufficient geometric mechanism, not an inference from integrated Lorentz estimates to heights.

## Technical comments 1--35

Comments 1--10 are addressed in module 125 and the centered expansion of module 126. Comments 11--16 are addressed by separating the old finite-support baker, the new continuous-roof theorem, and the Lorentz theorem; the signed reference, two `1/c` factors, integer lift convention and zero extension are explicit. Comments 17--27 remain in the unchanged canonical theorem: `O(n^2)` cells, `n^(-2)` density, ordered central/tail limits, separate tightness inputs, zero residue classes, half-variation probability TV, graph-coupled rather than independent bridges, and record-only full-output postselection with `Delta_n/r_n -> 0`.

Comments 28--32 are reflected in every status flag and in the last paragraph of module 127. A Markov boundary-height theorem is not a Lorentz boundary-height theorem. Comments 33--35 are handled by a short front-matter addition and a direct reading route without further historical theorem hierarchies. The complete prior derivation remains available for the requested continuing review.
