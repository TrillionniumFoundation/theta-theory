# A2 v3 — proof, observation and preservation ledger

Controlling report: `fbe11e631e2e8f19eacff804cebbc5496d1fb822`.  
Reviewed manuscript: `daeea828a7666acc42adcabdb9ab9057e9e1bac7`.  
New branch: `revision/a2-geometric-thresholds-v3-observability-2026-09-09`.

## Theorem 1.1: arbitrary periodic dispersing configurations

The class consists of any fixed full-rank planar lattice and a positive finite number of bounded smooth strictly convex obstacles of positive curvature, with disjoint closures of distinct lifts. A compact smooth finite-dimensional deformation family is restricted to a neighborhood of an arbitrary reference configuration. Finite horizon, congruence, central symmetry and proximity to a circle are not premises. Constants depend on positive geometric margins and the relevant smooth norms, not on the flight number.

`v3/10_geometry_action.tex`, Lemma 2.1: finitely many potentially short lifted pairs; uniqueness of closest convex displacement and support points; positive contact Hessian; clearance of every globally minimizing chord; separation of normal outgoing states; small total excess forces small excess at every flight and specular reversal. This proves whole-event localization with one collar. Own-onset statements for a nonminimal channel retain physical itinerary selection.

Lemma 3.1: scale the full alternating quadratic action, not just its recurrence; retain the parity-dependent diagonal endpoint factors; derive the Hessian, determinant/twist ratio and two-step multiplier. The Hessian stays uniformly positive independently of the exponentially small mixed entry.

Lemma 3.2: explicit Green inverse and weighted convolution bound; uniformly contractive Dirichlet equation; derivative induction in the same weighted spaces; strict convexity gives uniqueness throughout the local box; summable endpoint weights control the action remainder. The exact corner-cofactor formula, an entrywise-to-trace-norm perturbation bound, and a convergent logarithmic determinant give a relative rather than absolute estimate. Parameter derivatives have bounded banded reference matrices and a trace-class perturbation factor. Even analytic data give the old circular cubic/quartic improvements.

`v3/20_integration.tex`: flight-tube normalization gives `-W_uv du dv dr/(2 pi A)` for actual full-phase preparation; no artificial transverse law is imposed. The residual interval has length `d-(W-jg)` and cannot be truncated by previous or extra terminal impacts. Uniform Morse coordinates cover the entire active sublevel. Radial integration gives the coefficient and smooth relative order-d remainder, including for nonsymmetric boundary jets. Finite oriented channel sums give competition; positivity and exact axial parity give the source-domain boundary. Smooth tests and transverse moving cuts remain separately defined.

## Theorem 1.2 and Proposition 5.1: the conditional endpoint metric

`v3/30_observability.tex`: the fixed unit-disk conditional density at zero offset is `2(1-|z|^2)/pi`, with second moment `I/6`. The endpoint inverse Morse differential is the inverse square root of the endpoint Hessian. After physical flux normalization this yields `Cov(u,v)/d = H^{-1}/3 + O(d)`. Radial parity gives smooth order-d errors rather than square-root errors despite cubic jets. Passing to actual Euclidean position variances and subtracting measured means eliminates the unknown contact point; orthogonality of normal and tangent leaves the leading diagonal unchanged. No tangent or area is supplied to the estimator.

At odd flight number the two endpoints belong to opposite obstacles. Their leading diagonal variances give the ratio of the two curvature factors and the strictly monotone scalar function `coth(j gamma)/sinh gamma`. Its derivative is bounded above and away from zero on compact positive boxes, uniformly in odd j. This proves the two-sided Lipschitz statement, including equal endpoint curvatures. No inverse of an exponentially small off-diagonal entry is used. Projection to the compact forward image supplies a well-defined noisy reconstruction with error `C(d+delta)`.

## Proposition 5.2: accuracy with physical preparation cost

Independent successes from independent full-phase preparations are paired. Squared endpoint differences divided by `2d` are unbiased variance estimators and uniformly bounded. The log-mgf variance argument proves concentration without a dynamical mixing or independent-impact assumption. Inverting gives the finite-offset error bound. The expected number of attempted preparations is `2K/Pr(E)`, hence order `K d^{-2} exp(j gamma)`. Uniform conditional conditioning is not claimed to remove this rare-event cost. The offset and selected physical window are specified; raw sensor noise or unknown timing is not silently covered.

## Theorem 5.3: an actual fixed-amplitude geometric fiber

The lattice is `3 Z x 4 Z`, the reference obstacle is the unit disk. Three explicit trigonometric polynomials control the two contact second jets and compensate area without changing them. Their area derivative is `3 pi/4`, so an analytic implicit-function correction holds obstacle area exactly pi. The two contacts remain at fixed support values with zero first derivatives. Thus g=1, A=12-pi, and the curvature factors are `2 exp(s)` and `2 exp(-s)`. Positive curvature and the strict distance gap to other translates persist. The two horizontal orientations exhaust every ground onset, with all leading count coefficients fixed. Their endpoint variance ratio is `exp(2s)`. The theorem does not assert equality of higher onset coefficients or a global isospectral family.

## Theorem 6.1 and Proposition 6.3: retained unlabelled data and calibrated information content

`v3/40_inverse.tex` retains the original equal-gap support family and its exact reconstruction, including the absolutely convergent odd-index Möbius transform, Hankel rank at repeated nodes, weights, multiplicities and two-amplitude subfamily. The finite-exponential-sum recovery is attributed to Prony theory without suppressing its proof.

The added area formula proves that A is a symmetric function of the observed gap and recovered curvature triple, not a fourth independent unknown. The explicit circular tangent has vanishing first amplitude derivative while the curvature multiset changes linearly. This does not contradict exact infinite-data identification. Stable recovery is instead proved for the separately defined endpoint-record observation, not falsely asserted for the same unlabelled finite vector.

## Architecture and retention

General geometry and the reusable relative-flux lemma now precede integration and the marked inverse. The complete circular hierarchy, source formulas, explicit Green/Hessian/cofactor/logdet expressions, records and independent-roof comparison remain in Appendices A–G. Repeated circular contraction and determinant proofs use the established even analytic case. Their original full sources remain unchanged in `sections/`; all original geometric sources remain in `v2/`. The main entrypoint, README and build wrapper of v2 are archived under `history/v2-publication/`.

All 118 labels in the old active source closure remain in the new one. The seven old theorems, twelve lemmas, five propositions and five corollaries have counterparts; five results are added. This is preservation or explicit generalization, not a claim that every old statement and proof is word-for-word unchanged. `PRESERVATION.json` records the labels, source map and unchanged files. The complete reviewed subtree is the Git base, so historical files missing from the local source cache are still retained remotely.

The exact `two_collision.tex` companion is unchanged; its seven PDF page texts agree with the source-package v2 output. The historical Round 33 chapter retains its arithmetic and conditional Fourier-inversion results. It is not used to infer an unrestricted mechanical long-time theorem from onset windows.

## Verification boundary

The current native build has 31+7 pages and real, converged references. Its source Git objects and SHA-256 values are recorded before publication. Six normal/optimized diagnostic executions passed with pairwise identical outputs. The new suite's exact finite calculations and floating quadratures are separate from analytical continuum proofs. No formal proof assistant, interval certification, full-equilibrium simulation, exhaustive priority survey or new GitHub Actions execution is claimed. The controlling referee's own 241-check suite was read through the report but not replayed.
