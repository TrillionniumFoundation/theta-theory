# Proof ledger — fifth intrinsic revision

The statements below are ordinary mathematical proofs in the native TeX. Compiled statement numbers and pages for both views are recorded in `evidence/BUILD_RECEIPT.json`. Stable labels are authoritative across builds.

## Dependency graph

```
separated C^(1+gamma) inverse branches + Hölder Gibbs law
  -> bounded distortion + weighted orbit cylinder separation
  -> contracting child energies + stationary suffix domination
  -> balanced greedy partitions + fixed-budget-dilation comparison
  -> arbitrary off-image quantization lower / cylinder upper
  -> EXACT suffix closure of full greedy tree
  -> intrinsic finite-state profile theorem

Gibbs/variational principles + cylinder distortion
  -> mixed partition sum = spatial-prefix/survival convolution
  -> two-pressure maximum
  -> tilted Gibbs lower bound + summable energy upper bound
  -> intrinsic exponent / threshold / entropy ratios
  -> positive Markov matrix formula and certified pressure enclosures

conditional Q(x,du)K(u,dy) >= epsilon mu(du)K(u,dy)
  + invariant marginals + exogenous renewal clock
  -> dependent raw-risk lower / restarting-observer upper
  -> pressure law with persistent hidden state
  -> noisy expanding law with retained hidden memory
```

The only retained mathematical dependencies of the new main chain are the full v4 posterior-orbit converse/kernel representation and the v4 noisy expanding quantization and suffix results. Their complete proofs occur in both views. The collision-moment theorem, assumed-contact theorem, HMM theorem and finite-reference Bellman theorem are not premises of the new intrinsic theorem.

## Statements and proof work

| Stable label | Hypotheses and proof work | Scope and quantifiers |
|---|---|---|
| `lem:v5-cylinder` | Separated increasing finite C^(1+gamma) contractions; bounded logarithmic derivative variation; Gibbs mass bounds; stationarity | Cylinder orbit separation uses the first post-prefix separation, not an assumed orbit metric equivalence. Exact `V(uv)<=V(u)V(v)` and `a(uv)<=a(v)` hold without independent symbols. |
| `lem:v5-greedy` | One-letter child energies between uniform positive factors, and total child contraction | Complete maximal-energy prefix tree; balanced leaf energies; fixed budget dilation comparison is proved before any exponent formula. |
| `lem:v5-quantization` | Disjoint tubes around incomparable orbit cylinders; at least four times as many cylinders as centres | Lower bound for arbitrary Hilbert centres, including off-image centres. Not restricted to cylinder encoders. |
| `lem:v5-suffix` | Full support and stationarity give strict `a(uv)<a(v)` for nonempty u; maximal-energy splitting | Every proper suffix of an internal vertex has already been split. Parents then put leaf suffixes in the same tree. EXACT full-tree count `(bL-1)/(b-1)`, not an unspecified log-depth overhead. |
| `thm:v5-intrinsic` | Prior four lemmas + retained general orbit converse + fixed-dilation comparison | `cG_M<=e_M^2<=R_M<=CG_M`; liminf lower for each randomized nonstationary observer. Stationary deterministic upper. Average and supremum risk orders, not exact optimal constants. |
| `lem:v5-pressure-sum` | Classical finite-full-shift Gibbs theorem; bounded cylinder oscillation; concavity of x^s for 0<s<1 | Partition sum bounded below by two endpoints and above by their time convolution. The pressure is a maximum of two pressures, not pressure of a pointwise maximum potential. |
| `thm:v5-pressure` | Positive conditional masses, strict pressure monotonicity, summability above the larger root, tilted Gibbs measure at that root | Existence of the squared-error exponent is proved; it is not assumed. Both root existence and the threshold are proved. At criticality the finite profile still governs risk. |
| `cor:v5-variational` | Variational pressure with uniformly positive and bounded information/expansion denominators | Entropy-over-information-and-expansion formulas; no replacement by the Lyapunov exponent of one chosen measure. |
| `prop:v5-enclosures` | Cylinder infimum/supremum, summable Hölder variations | Finite lower/upper pressure enclosures. Actual numerical effectiveness requires certified access to real input functions. |
| `cor:v5-markov` | Strictly positive finite transition matrix and affine unequal contractions | Perron roots of ENTRYWISE probability powers. Nonuniform stationary initial factor is handled by Gibbs comparison. |
| `ex:v5-variable` | Explicit nonlinear polynomial inverse branches and positive Markov law | Uniform derivative/separation verification; unequal fixed-point multipliers exclude a nondegenerate C^1 equal-multiplier conjugacy. Topological symbolic coding is not denied. |
| `thm:v5-dependent` | Standard Borel T,Q,K; mu invariant for T and Q; Q>=epsilon mu; exogenous IID finite-mean renewal times | Raw-risk lower for every randomized time-dependent observer. Truncated `Nn+1` upper. Exact one-time expected-loss transfer for restarting observers, not equality of full-history posteriors. |
| `cor:v5-dependentpressure` | Exact acquisitions on the Gibbs repeller; minorized invariant Q | Same finite profile/exponent even when Q retains Tx with probability 1-epsilon. Fixed positive epsilon; no uniform claim as epsilon tends to zero. |
| `cor:v5-dependentnoise` | Wrapped Gaussian acquisition, integer torus expansion, bounded mean residual life | Noise- and budget-uniform raw-profile comparison. Uses retained small-ball lemma directly for the quantization lower bound. Older data may improve the true Bayes floor. |

## Constant and interface audit

1. Strong separation g>0, bounded distortion, finite full alphabet, and full-support stationary Gibbs law are real assumptions. Overlapping maps, arbitrary subshifts with forbidden transitions and countable partitions are not silently included.
2. Gibbs constants, r_-, r_+, the Hölder modulus and g enter comparison constants. Uniformity in q is on compact subintervals of (0,1), not at weak-acquisition q=1.
3. The exact tree state count is independent of these constants. Its conversion to a same-M distortion comparison uses the proved fixed-dilation lemma.
4. Geometry uses ambient coordinate squared loss on the repeller, not an arbitrarily assigned ultrametric. Cylinder equivalence is derived from the derivative cocycle and physical image gaps.
5. The quantization and causal exponents concern squared error; no RMS conversion is hidden.
6. The finite G_M profile is sharp up to constants for every budget. The pressure formula is an exponent theorem. It does not supply a universal optimal leading constant or a universal logarithmic correction for every Gibbs measure.
7. The nonlinear examples have genuine variable metric expansion. Every member still has a full-shift topological coding; no impossible claim of absence of Borel conjugacy is made.
8. The acquisition indicator is an update input only, not a free decoder input. Every word, exhausted state and data-dependent persistent quantity is charged.
9. The reference B_0 in the dependent theorem is the single-acquisition orthogonality term, not the full-history dependent Bayes risk. The latter may be strictly smaller; `verify.py` includes an explicit rational example.
10. Q acts on the pre-acquisition state and K then observes the new state. The observation kernel is not incorrectly evaluated on the old state.
11. The dependence theorem requires an exogenous clock, invariant marginal law and positive minorization. It is not a claim about all endogenous controlled acquisitions.
12. Older full mathematical bodies are preserved, not automatically independently re-proved by preservation. Classical thermodynamic formalism, tree construction and static functional quantization are cited rather than claimed as inventions.

## Proof versus diagnostics

`verify.py` checks exact rational word identities, full-tree suffix closure, pressure root and threshold arithmetic, finite partition sums, a dependent posterior example, and the stated nonlinear family bounds. Five incorrect variants must fail in both normal and optimized Python. None is a machine-checked proof of the infinite-dimensional or asymptotic statements. The independent referee must judge the proofs and mathematical significance.
