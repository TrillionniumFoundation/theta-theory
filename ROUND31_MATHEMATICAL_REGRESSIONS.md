# Round-Thirty-One Mathematical Regression Ledger

Each row records a direct Round-Thirty counterexample and the invariant that must appear in the active Round-Thirty-One source. Compilation is necessary but not sufficient; the executable verifier also checks representative source tokens for every row.

| ID | Round-30 failure | Required Round-31 invariant |
|---|---|---|
| R31-A1-01 | covariance derivative left `J^m` but was claimed trace class on `J^m` | covariance is formed and differentiated on the common reporting space `H_r=J^{m+2r}` |
| R31-A1-02 | seam current did not satisfy the weighted projection condition | explicit exponential estimate for `P_0Y_q` and the weighted two-sided sum |
| R31-A1-03 | derivative loss was hidden in covariance notation | every derivative is embedded by `iota_{m+2j,m+2r}` before tensoring |
| R31-A2-01 | exact nonarithmeticity was called open | exact Diophantine arithmetic leaf; only geometric inequalities are relatively open |
| R31-A2-02 | good/bad bounds at `b=0` contradicted `L_0^n 1=1` | central Riesz decomposition retained; twisted cancellation restricted to `|b|>=B_0` |
| R31-A2-03 | exponential-width intermediate region had nonintegrable majorant | intermediate region ends at `n^A`; direct `n^q|b|^{-M}` tail starts there |
| R31-A2-04 | D1 imported an unproved high-order local theorem | A2 exports an `N^{-1}` mixed Edgeworth theorem with four source derivatives |
| R31-A3-01 | KL was integrated against holding occupation | KL is integrated against transition-count marginal `nu` |
| R31-A3-02 | constant return `R=r` produced cost `H` instead of `H/r` | exact renewal relation gives transition mass `1/r` and cost `H/r` |
| R31-A3-03 | leading telescoping identity lost slow chronology | mesoscopic incoming/outgoing current yields a separate slow divergence equation |
| R31-A3-04 | overshoot was assumed independent of central variables | terminal-state matrix amplitude retains overshoot/terminal/central dependence |
| R31-A4-01 | graph-bounded perturbation was treated as Hilbert-bounded | resolvent-small relative perturbation theorem with `sup ||A(z-L0)^{-1}||<1` |
| R31-A4-02 | graph-bounded observation lost a resolvent power | resolved basis lies in `D(L*)`; observation is bounded on the Hilbert space |
| R31-A4-03 | every bounded potential was given a simple leading projection | finite potentials are used only along certified spectral bridges |
| R31-B1-01 | equal anchor velocities made the momentum-energy minor singular | relative energy is integrated as a positive quadratic phase near `w=0` |
| R31-B1-02 | good-block event could cut anchor smoothness | anchor labels are excluded from the event, which is non-anchor measurable |
| R31-B1-03 | exceptional Fourier event had no integrable density | regular coarea plus quadratic anchor smoothing applies on both event components |
| R31-B2-01 | Cauchy radius loss was iterated for arbitrary time at fixed gap | `a(t)=a0-Lambda t` and Ovsyannikov evolution spend radius linearly |
| R31-B2-02 | pivot rank was placed inside an unverified certificate | chronological tree Jacobian is inverted and tangent pivots are constructed by induction |
| R31-B2-03 | subtree variations could break tree contacts | every pivot is projected by `X_e=a_e-R_TDF_Ta_e`, so `DF_TX_e=0` |
| R31-B2-04 | nested loop powers lacked one simultaneous determinant | all surplus closures use one lower-triangular simultaneous coarea determinant |
| R31-B2-05 | initial correlation/graph tails were not closed | factorial initial cumulants plus the time-dependent analytic-radius majorant |
| R31-B3-01 | resampling a root could move the stopping time | no root resampling; deterministic-interval moments give a pathwise temporal modulus |
| R31-B3-02 | Efron--Stein controlled variance, not drift/full increment | even moments and conditional drift are estimated separately |
| R31-B3-03 | cycle contact directions were lost | full normal/cycle covariance and Hessian retain positive cycle cost |
| R31-B4-01 | entropy plus energy was falsely said to imply `W_2` compactness | ballistic energy compactification records boundary recession energy |
| R31-B4-02 | global sup-norm strong continuity failed at unbounded energy | strong continuity is on each fixed compact energy shell |
| R31-B4-03 | comparison used a noncompact `W_2` shell | doubled-variable comparison is on the compact ballistic shell |
| R31-B4-04 | zero-recession `W_2` upgrade lacked uniform integrability | explicit superlinear de la Vallee--Poussin gate |
| R31-C1-01 | each active stratum contributed probability one | selection probabilities `p_s` sum to one and remain in the RN density |
| R31-C1-02 | deterministic Bayes multiplication was falsely projectively contractive | finite-window induced-law Gram/Riccati coercivity on observable quotient |
| R31-C1-03 | a finite global Sobolev dimension was assigned to histories | projective cylindrical distribution scale with finite-dimensional tests only |
| R31-C1-04 | hidden-map inverse was used without invertibility | derivatives pair with `partial_theta(phi o Phi)` and require no inverse |
| R31-C1-05 | pointwise signal separation did not identify mixtures | uniform Hellinger separation of induced observation laws over reachable beliefs |
| R31-C2-01 | likelihood used one common filter | numerator uses `Pi^theta`; denominator uses `Pi^{theta0}` |
| R31-C2-02 | weak kernel convergence was assumed to imply filter convergence | quantitative observable-quotient filter stability and continuation-kernel convergence |
| R31-C2-03 | pressure localization imported unavailable arbitrary base potentials | only A4 certified potential bridges are admissible |
| R31-C2-04 | one blanket BSDE theorem mixed all channels | separate discrete, marked-point, and Brownian BSDE theorems |
| R31-D1-01 | summed lattice phase cell kept the single-site `N^{-d_Z/2}` factor | central lattice Riemann sum cancels that power |
| R31-D1-02 | exact lattice fibre and phase cell were conflated | separate exponents `kappa^fib` and `kappa^cell` |
| R31-D1-03 | upstream did not export the assumed expansion | A2/B1 four-source-derivative `N^{-1}` Edgeworth interface |
| R31-D1-04 | raw `K_N` was scaled as if normalized | fluctuation is `(K_N-Nk_j)/sqrt N` |
| R31-D1-05 | adaptive-policy expansion followed from compactness alone | finite-memory policy charts plus a quantitative causal approximation theorem |
| R31-D1-06 | policy manifold was treated by Laplace integration | deterministic epi-argmax; no policy-volume factor |

The verifier rejects old Round-Twenty-Nine imports and representative obsolete formulas. Passing the ledger means that the formal counterexamples have active replacements; it is not a substitute for specialist assessment of the new estimates.
