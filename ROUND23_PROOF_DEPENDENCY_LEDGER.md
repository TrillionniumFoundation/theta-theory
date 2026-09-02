# Round-Twenty-Three proof dependency ledger

**Branch:** `revision/round23-referee-positive-closure-11paper-2026-09-02`  
**Referee baseline:** `REFEREE_REPORT_ROUND22_GPT56_PRO_HARSH.md`  
**Rule:** a file is upstream only when its active Round-Twenty-Three theorem and proof are already available.  File existence, a build, or a reference to a prior revision does not count as a mathematical import.

## Global directed acyclic order

```text
A1
A2 -> A3 -> A4
B2-GC -> B1 -> B2-MC -> B3 -> B4
A2,A3,A4,B1,B2-GC,B2-MC,B3,B4 -> C1
A3,A4,B3,B4,C1 -> C2
A1,A2,A3,A4,B1,B2-GC,B2-MC,B3,B4,C1,C2 -> D1
```

`B2-GC` and `B2-MC` are two theorem groups in one active B2 paper.  The former is a root for the hard-sphere branch; the latter is proved only after importing B1's exact-number coefficient theorem.

## Paper-level proof contracts

| Node | Self-contained Round-Twenty-Three gates | Imported gates | Exports |
|---|---|---|---|
| A1 | labelled exact suspension; positive-test incidence dual; fixed-fibre closed material derivative; strongly measurable current observable; explicit projective response norm; Bochner differentiation; Hilbert martingale approximation; trace-class covariance identity | none | exact benchmark; typed current response and FCLT interface |
| A2 | weighted branch derivative sum; periodic-data annihilator certificate; covariance nondegeneracy; two-coordinate original-section UNI/coarea; exhaustive Fourier majorant; raw mixed lattice--roof inversion | standard finite-horizon billiard geometry and cited anisotropic spectral input, with all extra hypotheses stated | source-inserted four-dimensional local theorem; conditional density interface for A3/C1/D1 |
| A3 | exact complete-history kernel; Lyapunov-weighted mark moment; chronological marked point measure; ordered physical path; terminal and recession sectors; predictable entropy representation; conditional-reference finite-KL recovery; stopped compactness and lower bound | A2 branch estimates and source-inserted local theorem for conditioned finite-memory functionals | ordered collision/physical-time LDPs and legal path-conditioning interface |
| A4 | two-scale remote-past influence estimate; drift and synchronized minorization; weighted operator gap; analytic source algebra; typed renewal entry/exit maps; closed block generator; exact Schur--Feshbach memory identity and rough path | A3 exact history kernel and moment; A2 local/renewal estimates | prepared pressure/Doob platform, history process limits, domain-safe memory kernel |
| B2-GC | closed incoming Green trace; regular `L^p(A_f)` grazing control and entropy approximation; determinant-ideal stratification; loop-opening surplus gain; factorial connected coefficients; complete open-half-edge collision-history hierarchy; exact finite-time composition/cutting; tilted concentration; positive control recovery; GC pressure and LDP | established deterministic hard-sphere geometry and cited cluster inputs, with all additional loop/history steps proved in the active source | source-uniform GC pressure/cumulants; density/contact/history LDP; root for B1/B3/C1 |
| B1 | probability-normalised canonical MGF; explicit ideal-gas renormalisation; quotient constraints; deterministic labelled block exposure; adapted boundary-flat atlas; global characteristic majorant; full mixed local Gaussian; activity/constraint saddle and exact-N coefficient ratio | B2-GC analytic pressure and history cumulant bounds | exact-number/microcanonical denominator, full covariance and Schur conditioning for B2-MC/B3/C1/D1 |
| B2-MC | conditioned exponential tightness and Laplace principle on the full collision-history hierarchy | B2-GC LDP and B1 source-inserted local coefficient | microcanonical density/contact/history LDP |
| B3 | global Maxwellian collision comparison; transport--collision observability and closed range modulo invariants; nuclear test triple; conditional stopping-time cumulants after full-state restart; Gaussian process; defect-coordinate positive chart; exact nonlinear-balance recovery; Mosco second epi-derivative | B2-GC/B2-MC history cumulants and action; B1 conditional initial covariance | tangent right inverse, Gaussian covariance, correct kinetic Hessian |
| B4 | superquadratic `W_2` state shell; compact action sublevels; product collision continuity; direct Wasserstein transfer; strongly continuous Nisio semigroup; implicit nonlinear resolvent; explicit Hamiltonian core, containment and comparison; finite BBGKY corrector and diagonal graph convergence | B2 collision-history cutting/loop gain; B1/B2 exact-number preparation; B3 graph form where tangent identification is used | nonlinear kinetic control/semigroup platform for C1/C2/D1 |
| C1 | deterministic hidden prediction without common domination; dominated observation strata; integrated evidence/Bayes continuity; risk-sensitive DPP; convex belief reconstruction; recursively differentiated likelihood; persistent excitation, tests, LAN and BvM | A2/A4 inserted Sinai observation blocks; B1/B2/B3/B4 inserted hard-sphere observation blocks, compactness, Gaussian/control interfaces | Feller belief kernel, policy likelihood, posterior-control/statistical interface |
| C2 | weighted strict topology as exact pullback; full hard-sphere adjoint; form-level Schur compression; equilibrium localisation; constructive Livsic theorem; prediction-process/UT optional-projection theorem; strictly positive innovation likelihood; concrete data contractions | A3/A4 ordered history and memory; B3/B4 forms; C1 integrated filter and likelihoods | rigidity, optional projections, stochastic tangent/contraction interface |
| D1 | exact microscopic phase cells; compact/noncompact rate separation; source-inserted local phase coefficient; Morse--Bott weights; labelled component LDP; phase-posterior Bellman state; shared-policy value; dominance-qualified complex chart; phase-centred Gaussian mixture | all upstream rates, local coefficients, filters, tangent laws, memory and control interfaces | terminal synthesis |

## Active labels by node

| Node | Required active labels |
|---|---|
| A1 | `prop:r23-a1-suspension`, `def:r23-a1-domain`, `thm:r23-a1-response`, `thm:r23-a1-fclt`, `prop:r23-a1-regression` |
| A2 | `lem:r23-a2-arithmetic`, `thm:r23-a2-fourier`, `thm:r23-a2-llt` |
| A3 | `lem:r23-a3-moment`, `prop:r23-a3-order`, `lem:r23-a3-recovery`, `thm:r23-a3-ldp`, `cor:r23-a3-conditioned` |
| A4 | `lem:r23-a4-small`, `prop:r23-a4-renewal`, `thm:r23-a4-memory` |
| B2-GC | `lem:r23-b2-loop`, `thm:r23-b2-gc-pressure`, `thm:r23-b2-gc-ldp` |
| B1 | `prop:r23-b1-normalization`, `lem:r23-b1-block`, `thm:r23-b1-llt`, `thm:r23-b1-extraction` |
| B2-MC | `thm:r23-b2-mc` |
| B3 | `lem:r23-b3-gap`, `thm:r23-b3-range`, `thm:r23-b3-clt`, `thm:r23-b3-mosco` |
| B4 | `lem:r23-b4-compact`, `prop:r23-b4-product`, `thm:r23-b4-resolvent`, `thm:r23-b4-limit` |
| C1 | `prop:r23-c1-observation`, `thm:r23-c1-filter`, `prop:r23-c1-finite`, `thm:r23-c1-bvm` |
| C2 | `thm:r23-c2-dual`, `thm:r23-c2-annihilator`, `lem:r23-c2-periodic`, `thm:r23-c2-optional` |
| D1 | `lem:r23-d1-separation`, `thm:r23-d1-weights`, `thm:r23-d1-control`, `thm:r23-d1-gaussian` |

## Anti-circularity checks

1. **B2-GC before B1.**  `thm:r23-b2-gc-pressure` and `thm:r23-b2-gc-ldp` are proved from the loop-opening/history hierarchy.  Neither imports B1.  B1 imports only this GC group.
2. **B1 before B2-MC.**  `thm:r23-b1-extraction` supplies the exact-number local coefficient.  Only `thm:r23-b2-mc` imports it.
3. **B3 covariance before Hessian identification.**  `thm:r23-b3-clt` is constructed from B2 connected cumulants and stopping-time tightness.  `thm:r23-b3-mosco` subsequently identifies its Cameron--Martin inverse.
4. **B4 comparison independent of graph convergence.**  Product continuity, containment and the `W_2` doubling argument establish comparison before `thm:r23-b4-limit` uses microscopic correctors.
5. **C1 observation theorem is conditional, not aggregate.**  `prop:r23-c1-observation` repeats source-inserted inversion with the hidden entrance history retained; it does not infer pointwise conditional density from an aggregate LLT.
6. **C1 BvM after excitation and tests.**  The policy class is restricted by explicit persistent excitation and Kullback separation.  Tests and posterior contraction precede the Gaussian posterior conclusion.
7. **C2 periodic data after equilibrium localisation.**  A pressure derivative yields equilibrium means only.  `lem:r23-c2-periodic` is a separate bridge to periodic measures, after which Livsic is applied.
8. **C2 stochastic exponential after prediction convergence and positivity.**  Optional projection/bracket convergence precedes innovation representation, and strict positive equivalence precedes logarithmic likelihood calculus.
9. **D1 polynomial weights before mixture/control synthesis.**  `thm:r23-d1-weights` imports local coefficients, not only LDP rates.  Control fixes a common policy before summing components.

## Round-Twenty-Two blocker coverage matrix

| Paper | Referee blocker | Positive closure mechanism | Machine regression/source gate |
|---|---|---|---|
| A1 | arbitrary Hilbert vector assigned exponential projection rate | rate is a term of `C_eta^r` norm | source requires `def:r23-a1-domain`; synthetic slow-tail sequence confirms bare `l2` has no exponential rate |
| A1 | untyped expectation/FCLT/covariance | strongly measurable Bochner observable, projective filtration, `tr Q=E||D||^2` | required labels and trace-token checks |
| A2 | determinant over reals used for lattice aperiodicity | exact integer generators plus irrational roof pair and coprime periods | finite character regression and required proof text |
| A2 | two orbit returns treated as independent | derivatives in original `(r,phi)` chart | source gate rejects old dependent-coordinate phrase and requires full Jacobian token |
| A2 | branch mass used as derivative norm | weighted `C^4` homogeneity sum | required estimate marker `(A2.1)` |
| A3 | unordered state | chronological start coordinate and complete mark | permutation regression distinguishes `AB` and `BA` |
| A3 | atomic recovery has infinite KL | conditional-reference cell recovery | exact discrete data-processing regression |
| A3 | `nu_N/N` falsely bounded below | recession sector retains one-long-excursion controls | source requires recession and forbids lower-return assertion |
| A4 | Lyapunov tail uniformly truncated | stable influence weight `theta/rho` distinct from `V` | remote-large-mark numeric regression |
| A4 | regular-point residue used | genuine Riesz poles only | source gate forbids transmission augmentation phrase |
| A4 | false `O(z^-2)` memory transform | exact `z^-1 PLQLP` expansion; explicit leading-pole subtraction | block-matrix Feshbach/high-frequency regression |
| B1 | `1/N!` pressure diverges | probability normalisation or explicit ideal-gas renormalisation | Stirling-versus-normalised regression |
| B1 | nonpredictable block choice/boundary density | deterministic label blocks and adapted flat atlas | source token/structure gates |
| B1 | omitted mixed covariance | full covariance, shifted conditional mean and Schur complement | Gaussian block-matrix regression |
| B2 | moments used for grazing trace | regular `L^p(A_f)` density plus entropy approximation | analytic grazing exponent regression/source gate |
| B2 | no regular surplus gain | loop-closure tube plus determinant-ideal optimization | positive optimized exponent regression |
| B2 | reduced finite-time state | complete open-half-edge history hierarchy | source requires exact `star` composition and history norm |
| B3 | Hessian charges zero-cost manifold | defect `h=delta Gamma-D A_f[u]` | finite-difference zero-manifold and normal-defect regressions |
| B3 | deterministic intervals promoted to stopping times | full microscopic restart plus conditional history bound | required conditional estimate marker `(B3.12)` |
| B4 | second moment not compact | `(2+delta)` moment and `W_2` | escaping-mass moment regression |
| B4 | weak metric promoted to strong transfer | direct synchronous `W_2` estimate | source gate requires `(B4.5)` and forbids weak-upgrade text |
| C1 | impossible common domination of Dirac transitions | no hidden-state density; observation-only domination | finite atom-mass regression and source gate |
| C1 | small evidence/infinite stratum | integrated numerator inequality | direct ratio inequality regression |
| C1 | uninformative policy assigned positive information | explicit persistent-excitation class | zero-information action regression |
| C2 | incorrect weighted strict sequential criterion | pullback of exact strict topology theorem | finite-measure transformation regression/source gate |
| C2 | collision adjoint omitted | explicit `-L_f^* r` | required token gate |
| C2 | pressure means promoted to periodic sums | equilibrium localisation then Livsic | dependency/label gate |
| C2 | weak convergence promoted to filters/brackets | prediction process plus UT characteristics | source gate requires assumptions (i)--(iv) |
| C2 | likelihood may hit zero | strict positive equivalent likelihood with reciprocal moment | positive-exponential regression |
| D1 | LDP used for polynomial weights | local coefficient and Morse--Bott integral | polynomial-exponent regression |
| D1 | phase cells/noncompact complement unsupported | `I`-continuity cells plus exponential tightness | source gate and finite-rate separation regression |
| D1 | separately optimised components | one common policy on full posterior state | source gate forbids phasewise optimiser formula |

## Import discipline

- A theorem may cite established literature for a standard platform result only when the active source states the exact version, verifies that its model lies in the cited class, and proves all additional interfaces used downstream.
- A source-inserted local theorem must retain the insertion through the Fourier/coefficient proof; an aggregate local theorem cannot be used as a conditional density theorem by disintegration alone.
- A topology or operator domain is part of a theorem's type.  No downstream paper may silently strengthen convergence, compactness, or domain membership.
- Polynomial prefactors, covariance shifts, and memory leading coefficients are not exponential-scale decorations; they must be imported from the theorem that computes them.

## Fail-closed publication rule

A Round-Twenty-Three branch is eligible for the next external review only if:

1. all eleven `main.tex` files import `ROUND23_POSITIVE_CLOSURE.tex`;
2. every paper contains the required labels above and a matching `AUTHOR_RESPONSE_ROUND22.md`;
3. every citation key in the active source resolves in that paper's bibliography set;
4. the dependency graph is acyclic and respects the B2-GC/B1/B2-MC split;
5. all executable referee-counterexample regressions pass;
6. all eleven projects clean-build from one checkout;
7. the exact source and PDF hashes are recorded;
8. the inherited Round-Twenty-Two report is retained unchanged.

These conditions establish a reproducible positive revision.  They do not certify journal correctness; that remains the task of independent specialist review.
