# Author Response to the Round-Thirty Referee Report

**Repository:** `TrillionniumFoundation/theta-theory`  
**Revision branch:** `revision/round31-referee-positive-closure-11paper-2026-09-03`  
**Controlling review branch:** `review/round30-gpt56-pro-harsh-11paper-2026-09-02`  
**Controlling review commit:** `4c6aa83111d404d9139acad1699b1f31bdb792e4`  
**Reviewed Round-29 mathematical commit:** `76f7ae36d7f894673383ceccda41c86b1cb6ac5c`  
**Active revision:** Round Thirty One  
**Date:** 3 September 2026

## 1. Revision policy

The Round-Thirty report identified new contradictions in the active Round-Twenty-Nine sources. Round Thirty One therefore replaces all eleven active theorem files and all eleven wrappers. It does not treat a response, manifest, successful build, or regression token as a proof. Earlier derivations are retained only where their hypotheses and types survive the new counterexamples.

The positive programme is unchanged: current response and functional limits, Sinai mixed local expansions, chronological path large deviations, history pressure and memory, hard-sphere preparation and dynamic large deviations, kinetic process and nonlinear-semigroup limits, filtering and adaptive inference, cotangent rigidity, and phase/control synthesis. The repair strategy strengthens state spaces, hypotheses, and intermediate theorems instead of replacing the programme by a no-go statement.

## 2. New cross-paper tools

1. **Loss-Buffered Covariance Calculus.** All parameter derivatives are embedded in one common, sufficiently weak current Hilbert space before rank-one covariance tensors are differentiated.
2. **Exact Arithmetic Leaf with Polynomial Fourier Crossover.** Exact nonarithmetic identities define a fixed leaf; geometric estimates are open only relative to that leaf. The intermediate Fourier interval is polynomial and the direct coarea tail begins there.
3. **Transition-Clock Entropy and Two-Scale Current.** KL is charged against transition count. Holding occupation is reconstructed from transition flow and return lengths, while a mesoscopic divergence current retains slow chronology.
4. **Resolvent-Small Compression.** Orthogonal dynamics is generated through a uniform relative-resolvent bound, not the bounded perturbation theorem. Resolved observations are Hilbert bounded.
5. **Quadratic Relative-Energy Anchor.** The equal-velocity momentum-energy degeneracy is integrated by radial stationary phase in relative velocities instead of being assigned a nonexistent full-rank minor.
6. **Ovsyannikov Collision-History Evolution.** The analytic radius decreases linearly in time, exactly matching the Cauchy creation estimate.
7. **Temporal-Modulus Cumulant Compiler.** Deterministic-interval even moments and dyadic chaining prove a uniform path modulus; arbitrary stopping times are then controlled pathwise.
8. **Ballistic Energy Compactification.** Escaping quadratic energy is retained at a velocity boundary where spatial phase is collapsed, giving compact fixed-energy shells without false `W_2` compactness.
9. **Stratum-Selection Observation Law.** Explicit probabilities choose the observation stratum before the conditional channel is sampled, so the full disjoint-union density integrates to one.
10. **Observable-Quotient Filter Calculus.** Finite-window induced observation laws provide coercivity on observable belief/parameter tangents; deterministic latent directions are retained rather than falsely contracted.
11. **Lattice Cell/Fibre Dichotomy.** Exact lattice conditioning retains the single-site local power, while summing a central phase cell cancels it.

## 3. Point-by-point response

### A1 — covariance derivatives and the seam projection condition

**Report.** The current derivative leaves the base Hilbert space, so differentiating `D_0 tensor D_0` in trace norm on that base space is not typed. The seam current was not shown to satisfy the weighted two-sided projection condition used by the FCLT.

**Round 31.** The reporting space is fixed at `H_r=J^{m+2r}`. Every derivative `D_0^{(j)} in J^{m+2j}` embeds continuously in `H_r`, and the covariance is a trace-class operator on `H_r`. Trace-norm differentiation is proved there and is not claimed on `J^m`. For the affine seam current, the product branch identity gives exponential shell decay; a projection can see both the origin and coordinate `q` only through sheets of depth at least `|q|`, yielding the required `(1+|q|)^{1/2}`-weighted summability. A genuine fractional polygonal interpolation remains active.

### A2 — arithmetic openness, zero frequency, and the noncentral integral

**Report.** Exact nonarithmeticity is not open. Combining the good/bad estimates at zero frequency contradicts `L_0^n 1=1`. The previous intermediate-frequency majorant does not have a negligible integral over an exponentially large region.

**Round 31.** Exact periodic roof and lattice data define a closed Diophantine arithmetic leaf. Only curvature, clearance, distortion, and transversality are varied openly within that leaf. Near zero the full spectral decomposition `lambda(xi)^n Pi(xi)+N(xi)^n` is retained. Returned-branch and bad-language cancellation is stated only for `|b|>=B_0`, so it never removes the untwisted eigenprojection. The intermediate range ends at `n^A`; beyond that point the direct coarea bound `n^q |b|^{-M}` is integrated explicitly. The parameters satisfy `A(M-d_c)>q+(3+d_c)/2+4`, which makes the stated noncentral integral smaller than the Edgeworth scale. The local expansion is carried through `N^{-1}` with four source derivatives for D1.

### A3 — entropy clock, chronological balance, and overshoot

**Report.** The action charged KL against holding occupation, giving a factor error even when `R` is constant. The scaled telescoping identity did not provide the claimed slow chronological equation. The scalar Gaussian-times-overshoot factorization was not derived.

**Round 31.** The transition-count occupation assigns mass `1/N` to each selected mark and is the measure in the entropy action. Holding occupation is a separate measure satisfying an exact finite-word renewal identity; when `R=r`, transition mass is `1/r` and the action is the exact `H/r`. The leading telescoping identity gives fast stationarity. A windowed mesoscopic incoming/outgoing current, with `delta_N downarrow 0` and `N delta_N to infinity`, gives the slow distributional divergence equation and endpoints. Random stopping is treated on an enlarged residual-clock/terminal-state transfer operator. The local theorem contains a nonnegative matrix amplitude depending on overshoot, terminal cylinder, and central direction; scalar independence is asserted only under an additional rank-one terminal theorem.

### A4 — graph perturbations, memory remainder, and finite-amplitude pressure

**Report.** A graph-bounded perturbation was fed into the bounded perturbation theorem. A graph-bounded observation lost a power in the vertical resolvent expansion. Local perturbation at zero did not justify simple spectrum at every bounded base potential.

**Round 31.** The compression hypothesis is the verifiable relative-resolvent bound `sup ||A(z-L_0)^{-1}||<1`. A Neumann resolvent formula and Hille--Yosida estimates produce the compressed semigroup. The finite resolved basis lies in `D(L^*)`, making the observation `C_Q` bounded on the Hilbert space; the vertical memory expansion is then obtained by repeated resolvent identities without graph-norm growth. Finite exposing potentials are available only along a certified bridge carrying uniform drift, Lasota--Yorke, irreducibility, and Riesz-contour separation. Bounded multiplication alone is not used.

### B1 — equal-velocity degeneracy and event-dependent smoothing

**Report.** At equal anchor velocities, the energy differential is a linear combination of momentum differentials, so a uniformly full-rank anchor is impossible. Conditioning on a good-block event can cut the anchor density.

**Round 31.** Reserved anchors are excluded from every good-block definition, so the good/exceptional event is non-anchor measurable. In centre-of-mass and relative coordinates, momentum is linear in the centre and relative energy is the positive quadratic form `|w|^2/2`. Away from `w=0`, ordinary coarea is used. Near `w=0`, an explicit radial Fresnel/stationary-phase calculation gives polynomial decay; several disjoint anchor groups yield any required integrable exponent. Thus the rank-degenerate set is handled by its true quadratic geometry and both events retain the same anchor smoothing.

### B2 — analytic radius and loop-pivot construction

**Report.** A `1/(a-a')` creation estimate does not imply arbitrary-time evolution at a fixed radius gap. The pivot certificate assumed the desired rank, and graphwise coarea/majorants were not completed.

**Round 31.** The history radius is `a(t)=a_0-Lambda t`. An Ovsyannikov fixed-point theorem proves existence only while the initial radius reserve covers elapsed time, exactly as the analytic-translation counterexample requires. For Poisson/Maxwellian initial kernels every finite starting radius is available, so any fixed regular Boltzmann time is covered by choosing `a_0`. Tree contacts are solved chronologically: the time/direction Jacobian is block lower triangular and is inverted by forward substitution. Surplus ambient variations are projected onto the exact tree tangent bundle and orthogonalized chronologically. Failure of a diagonal derivative is shown to force one of the explicitly controlled singular strata. Simultaneous coarea, label factorials, chart changes, singular strata, and the graph tail are summed under one Ovsyannikov majorant.

### B3 — stopping times and full second moments

**Report.** Resampling a root can move the stopping time and the entire observation interval. Efron--Stein controls variance, not the full stopped increment and drift.

**Round 31.** Root resampling is removed. B2 connected source derivatives give all fixed even moments on deterministic intervals. Moment-cumulant partitions yield `E||Z_t-Z_s||^{2p} <= C|t-s|^p+o(1)`; the weak balance equation separately controls the conditional drift. A dyadic chaining argument gives a uniform temporal modulus. For any temporal stopping time, the stopped increment is pathwise bounded by that same modulus, proving Aldous without changing the roots or stopping rule. The full normal/cycle contact covariance and Mosco Hessian are retained.

### B4 — compactness and strong continuity

**Report.** Gaussian relative entropy plus a second-moment bound does not imply `W_2` compactness. Global strong continuity fails on the union of unbounded energy states.

**Round 31.** The state consists of the compactified mass image and the quadratic-energy image on a radial velocity compactification. At infinite velocity, spatial points with the same direction are identified; this is the ballistic quotient needed for small-time continuity. Every fixed total-energy shell is compact in this topology. Boundary energy records the exact defect in quadratic uniform integrability. `W_2` is recovered only on the zero-recession face under a genuine superquadratic de la Vallee--Poussin bound. The Nisio semigroup is strongly continuous on each fixed compact energy shell, not in a global sup norm over unbounded energy. Comparison is performed on the compact ballistic shell.

### C1 — full-channel normalization and deterministic filtering

**Report.** Each active stratum contributed probability one. Positive observation multiplication after deterministic hidden evolution did not contract Hilbert projective distance. The finite-dimensional Sobolev chart did not cover the actual infinite-dimensional hidden state, and pointwise signal separation did not identify observation mixtures.

**Round 31.** State/action/parameter-dependent probabilities `p_s` first select a stratum and sum to one. Relative to envelope weight `alpha_s q_s m_s`, the density is `p_s rho_s/(alpha_s q_s)`, so integration gives `sum_s p_s=1`. Hidden push-forwards are differentiated against finite cylindrical tests and closed in a projective negative-Sobolev scale; no global manifold dimension or inverse hidden map is assumed. Stability is a finite-window induced-law Gram/Riccati inequality on the observable quotient. Latent deterministic directions are retained. Global testing assumes Hellinger separation of the induced observation laws over reachable beliefs, which rules out hidden relabellings.

### C2 — likelihood filters, optional projection, and BSDEs

**Report.** The discrete likelihood used one common filter in numerator and denominator. Weak primitive-kernel convergence alone did not imply nonlinear-filter or optional-projection convergence. The pressure localization imported an unavailable A4 theorem, and the BSDE statement mixed distinct channels.

**Round 31.** The likelihood product uses `Pi_{k-1}^theta` in the numerator and `Pi_{k-1}^{theta0}` in the denominator. A quantitative filter-stability theorem combines primitive-kernel error with C1 observable-quotient contraction and continuation-kernel convergence. This identifies optional projections of full paths and their characteristics. Pressure localization imports only A4 certified bridges. Discrete, marked-point, and Brownian BSDE stability are separate theorems with their own likelihood, martingale representation, jump norm, terminal, and driver hypotheses.

### D1 — lattice power, upstream expansion, scaling, and policies

**Report.** A summed lattice phase cell was assigned the single-site `N^{-d_Z/2}` factor with the wrong sign. The assumed high-order local theorem was not exported by A2/B1. The final raw lattice variable was scaled inconsistently, and policy uniformity was assumed.

**Round 31.** An exact lattice fibre retains `d_Z/2` in the polynomial exponent. In a phase cell, the `N^{d_Z/2}` central lattice sites cancel the single-site factor, leaving only the continuous Morse--Bott codimension. A2 and B1 now export the required `N^{-1}` Edgeworth expansion with four source derivatives. The state is `bar xi_N=(K_N/N,Y_N)` and the fluctuation is `((K_N-Nk_j)/sqrt N, sqrt N(Y_N-y_j))`. Finite-memory randomized policies produce a finite source vector covered by the upstream theorem. A causal finite-memory approximation with `N epsilon_m=o(1)` extends the expansion to compact strategic measures. Common-policy selection remains an epi-argmax problem and never integrates over policy space.

## 4. Dependency order

The active order is:

```text
A2 -> A3 -> A4 -> C2
A1 -> C2/D1 finite current outputs
B2-GC -> B1 -> B2-MC -> B3 -> B4
C1 -> C2 -> D1
A2/B1 Edgeworth -> D1
```

B2 grand-canonical pressure is established before B1 extraction. B1 then supplies the exact-number coefficient used for the microcanonical contraction. B3 and B4 do not feed back into B2. D1 remains terminal.

## 5. Verification scope

The Round-31 verifier checks:

- all eleven `main.tex` files resolve only to Round Thirty One;
- no active source imports Round Twenty Nine;
- theorem/proof balance, unique Round-31 labels, printable UTF-8, and wrapper identity;
- the explicit counterexample replacements named above;
- the dependency order and report identity;
- eleven independent LaTeX builds plus the consolidated dossier;
- PDF headers and page inventory.

Those checks establish source identity, reproducibility, and removal of the report's enumerated formal contradictions. They do not substitute for independent specialist review of the new analytic and geometric arguments.

## 6. Status for the next review

Every direct contradiction and every minimum reconstruction requirement in the Round-Thirty report has a corresponding active definition, theorem, proof mechanism, dependency contract, or executable regression in Round Thirty One. The revision remains a positive attempt at the full programme. Final mathematical acceptance is reserved for the next independent referee round.
