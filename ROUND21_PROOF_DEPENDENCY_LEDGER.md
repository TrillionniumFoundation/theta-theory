# Round-Twenty-One proof dependency ledger

**Branch:** `revision/round21-referee-positive-closure-11paper-2026-09-02`  
**Reviewed objections:** all eleven reports on `review/round20-gpt56-pro-harsh-11paper-2026-09-02`, together with the detailed Round-Eighteen reports incorporated there by reference.

This ledger records mathematical dependence, not file presence or compilation.
Every imported item must have a theorem and proof in an earlier node of the
order below.

## Global order

```text
A1
A2 -> A3 -> A4
B2-GC -> B1 -> B2-MC -> B3 -> B4
A2,A3,A4,B1,B2-GC,B2-MC,B3,B4 -> C1
A3,A4,B3,B4,C1 -> C2
A1,A2,A3,A4,B1,B2,B3,B4,C1,C2 -> D1
```

## Paper-level gates

| Node | Self-contained gates | Imported gates | Downstream exports |
|---|---|---|---|
| A1 | labelled baker diffeomorphism; proper mapping torus; descended exact symplectic form; incidence-dual current Hilbert scale; fixed-fibre derivative; response trees; projective Hilbert FCLT | none | exact work cocycle; typed response/current platform |
| A2 | weighted countable-branch complexity; parent-fold bundle; periodic rank; returned UNI; two-coordinate coarea; exhaustive Fourier theorem; roof density; raw four-dimensional LLT | standard finite-horizon dispersing billiard geometry stated inside the module | inserted local estimates and conditioning windows for A3/C1/D1 |
| A3 | exact marked-history representation; exponential coercive mark; Polish stopped state; stopped entropy representation; compactness; legal recovery; explicit rates | A2 inverse-Jacobian disintegration and inserted local theorem | collision/physical-time LDPs and conditional kernels for A4/C1/C2/D1 |
| A4 | stable-holonomy exponential variation; drift; synchronized minorization; direct Banach gap; fixed-space source family; rough path proof; renewal factorization; transmission closure; memory inversion | A2 induced Fourier estimates; A3 exact history state | pressure, Doob kernel, renewal/memory, conditional process limits for C1/C2/D1 |
| B2-GC | closed trace graph; precontact rank atlas; normalized Catalan expansion; finite-time concatenation; actual-contact pressure; positive balance recovery; exact microscopic tilt; GC LDP | none of B1--B4 | source-uniform pressure/cumulants for B1/B3/B4/C1 |
| B1 | quotient constraint saddle; fixed-size smoothing blocks; global characteristic majorant; mixed local coefficient; activity/constraint extraction | B2-GC analytic pressure and normalized connected bounds | exact-number/microcanonical denominator and Schur corrections for B2-MC/B3/C1/D1 |
| B2-MC | conditioned upper/lower bounds and good constrained action | B2-GC plus B1 inserted coefficient theorem | microcanonical path/contact LDP for B3/B4/C1/C2/D1 |
| B3 | cutoff graph coercivity; nuclear test triple; localized cumulants; Aldous tightness; Gaussian process; positive balance chart; nonconvex second epi-derivative | B2 normalized expansion and pressure; B1 saddle derivatives | covariance, tangent right inverse, process CLT for B4/C1/C2/D1 |
| B4 | action compactness; direct positive transfer; Nisio semigroup; implicit nonlinear resolvent; Janossy reconstruction; exact boundary corrector; diagonal nonuniform-exponent limit; nonlinear Trotter--Kato | B2 action/compactness and precontact bounds; B3 graph coercivity only for tangent form interfaces | kinetic semigroup/control platform for C1/C2/D1 |
| C1 | typed transition/observation experiment; stratified domination; cemetery state; Feller belief kernel; DPP/selectors; finite coordinates; direct LAQ/LAN; tests and BvM | A2/A4 Sinai density and mixing; B1/B2/B3/B4 hard-sphere densities, CLT, and control compactness | dominated filters, likelihoods, posterior control, statistical interfaces for C2/D1 |
| C2 | weighted strict dual; platform form verification; Schur compression; countable-history Livsic; hard-sphere annihilator; changing-filtration Aldous theorem; innovation representation; data-only contraction calculus | A3/A4 invariant history platform; B3/B4 graph forms; C1 conditional kernels | rigidity, optional projections, stochastic contractions for D1 |
| D1 | finite-volume phase partition; component weight asymptotics; exact mixture LDP; phase-conditioned belief state; shared-policy Bellman principle; complex zero-free chart; corrected Gaussian coexistence | all component LDP, local, pressure, filter, tangent, and contraction interfaces above | terminal synthesis only |

## Anti-circularity checks

1. **B2/B1.** `thm:r21-b2-pressure` and `thm:r21-b2-gc` are proved from the normalized grand-canonical connected expansion before B1 is invoked. B1 uses those results to prove exact-number coefficient extraction. `thm:r21-b2-mc` is the only B2 theorem importing B1.
2. **B3 covariance/action.** `thm:r21-b3-clt` constructs the Gaussian covariance from microscopic cumulants before `thm:r21-b3-mosco` identifies it with the inverse second epi-derivative.
3. **B4 comparison.** The maximal dissipative graph comes from the independently derived nonlinear resolvent relation. Semigroup convergence then uses comparison; comparison is not assumed to prove the resolvent.
4. **C1 inference.** LAN is derived by a triangular-array Taylor expansion plus upstream score CLTs. BvM additionally uses `lem:r21-c1-tests`; it is not inferred from LAN alone.
5. **C2 stochastic representation.** Process optional-projection convergence is proved before the innovation representation. The stochastic exponential follows only after the limiting filtration is shown to be the innovation filtration.
6. **D1 control.** Component values are aggregated under a fixed common policy. Optimization occurs only after aggregation, so no phase-observing controller is introduced.

## Referee-blocker coverage matrix

| Paper | Round-Twenty decisive blocker | Active closure label |
|---|---|---|
| A1 | generated quotient not proved proper/Hausdorff | `thm:r21-a1-suspension` |
| A1 | negative Sobolev trace direction reversed | `thm:r21-a1-incidence` |
| A1 | labelled Hilbert scale and closability absent | `thm:r21-a1-incidence`, `prop:r21-a1-derivative` |
| A1 | response/FCLT estimates asserted | `thm:r21-a1-response`, `lem:r21-a1-projective`, `thm:r21-a1-fclt` |
| A2 | impossible unweighted branch sum | `thm:r21-a2-complexity` |
| A2 | bundle and arithmetic/UNI implication absent | `thm:r21-a2-bundle`, `lem:r21-a2-periodic`, `lem:r21-a2-uni` |
| A2 | high-frequency derivative-order circularity | `lem:r21-a2-coarea`, `thm:r21-a2-fourier` |
| A2 | no raw integrable majorant/density | `thm:r21-a2-fourier`, `lem:r21-a2-density`, `thm:r21-a2-llt` |
| A3 | one-step surrogate inconsistent with history kernel | `thm:r21-a3-history` |
| A3 | undefined state/coercive cost | `lem:r21-a3-moment`, `prop:r21-a3-space` |
| A3 | compactness/recovery/rate absent | `lem:r21-a3-compact`, `thm:r21-a3-recovery`, `thm:r21-a3-ldp` |
| A3 | point-probability prefix formula | `thm:r21-a3-entropy` |
| A4 | summable variation falsely made exponential | `lem:r21-a4-variation` |
| A4 | drift/minorization/operator gap asserted | `lem:r21-a4-drift`, `lem:r21-a4-small`, `thm:r21-a4-harris` |
| A4 | source class not fixed-space analytic | `thm:r21-a4-fk` |
| A4 | scalar estimates promoted to renewal/memory | `thm:r21-a4-renewal`, `lem:r21-a4-transmission`, `thm:r21-a4-memory` |
| B1 | `C^4` versus `O(N)` integrations by parts | `lem:r21-b1-block`, `thm:r21-b1-fourier` |
| B1 | velocity variables miss position constraints | `lem:r21-b1-oneblock` |
| B1 | shell/extraction overclaimed | `thm:r21-b1-coefficient`, `thm:r21-b1-extraction` |
| B2 | trace and precontact atlas absent | `thm:r21-b2-trace`, `thm:r21-b2-atlas` |
| B2 | factorial dropped from genealogy sum | `thm:r21-b2-majorant` |
| B2 | nonlinear positive recovery and deterministic tilt absent | `thm:r21-b2-recovery`, exact tilt preceding `lem:r21-b2-legendre` |
| B2 | full LDP identification absent | `thm:r21-b2-gc`, `thm:r21-b2-mc` |
| B3 | false cutoff `H^1_v` coercivity | `lem:r21-b3-gap`, `thm:r21-b3-observability` |
| B3 | nuclear process tightness/covariance absent | `lem:r21-b3-nuclear`, `lem:r21-b3-tight`, `thm:r21-b3-clt` |
| B3 | global convexity and recovery invalid | `lem:r21-b3-chart`, `thm:r21-b3-mosco` |
| B4 | linear pseudo-resolvent identity used nonlinearly | `thm:r21-b4-resolvent` |
| B4 | transfer/compactness/strong continuity absent | `lem:r21-b4-transfer`, `thm:r21-b4-compact`, `thm:r21-b4-nisio` |
| B4 | graph core/Trotter--Kato asserted | `lem:r21-b4-diagonal`, `thm:r21-b4-corrector`, `thm:r21-b4-limit` |
| C1 | hidden transition/observation and domination untyped | `thm:r21-c1-chart` and definitions before it |
| C1 | atomic smoothing and zero-evidence state invalid | stratified measure construction, `thm:r21-c1-filter` |
| C1 | DPP/finite coordinates unsupported | `thm:r21-c1-dpp`, `prop:r21-c1-finite` |
| C1 | fixed-QMD/score CLT promoted to LAN/BvM | `thm:r21-c1-lan`, `lem:r21-c1-tests`, `thm:r21-c1-bvm` |
| C2 | weighted strict dual incomplete/invariant measure absent | `thm:r21-c2-dual`, `cor:r21-c2-coboundary` |
| C2 | form and model rigidity hypotheses unverified | `thm:r21-c2-typeb`, `thm:r21-c2-schur`, `thm:r21-c2-rigidity` |
| C2 | fixed-time kernels promoted to process/stochastic exponential | `thm:r21-c2-optional`, `lem:r21-c2-innovation`, `thm:r21-c2-girsanov` |
| C2 | category encoded conclusions | data-only definition and `thm:r21-c2-functor` |
| D1 | phase experiment assumed | `thm:r21-d1-phases` |
| D1 | insufficient state/common domination | `thm:r21-d1-information` |
| D1 | separately optimized log-sum | `thm:r21-d1-semigroup` |
| D1 | zero-free estimate assumed | `thm:r21-d1-zero` |
| D1 | Gaussian scaling and tie exponent wrong | `thm:r21-d1-gaussian` |

## Fail-closed publication rule

A branch may be proposed for merge only if:

- all eleven `main.tex` files input the replaced active source;
- every active module contains a main theorem and a proof environment;
- the dependency graph above is acyclic;
- no active proof contains the superseded false mechanisms listed in the
  hostile verifier;
- all eleven TeX projects compile from a clean checkout;
- the branch contains the Round-Twenty author response, historical audit, and
  hostile rereview.

Passing these repository gates establishes internal consistency and
reproducibility only. It is not a substitute for independent peer review.
