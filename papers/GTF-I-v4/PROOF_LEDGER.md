# Proof ledger — GTF I, fourth revision

Stable labels identify the native TeX statements. `evidence/BUILD_RECEIPT.json` records their compiled numbers and pages. The proofs are ordinary mathematical proofs, not machine-checked formalizations.

## Main dependency graph

```
standard Borel kernel realization + renewal reward + conditional orthogonality
  -> posterior-orbit lower bound and Nn+1-state upper bound
  -> quantization exponent invariance
  -> autonomous shift-closed ray characterization (separate subclass)

posterior-orbit converse + explicit Gaussian posterior + orbit small balls
  -> sharp noisy expanding law
suffix conditional means + charged word states
  -> exact upper risk -> uniform critical window and joint noise/memory profile

retained v3 exact Gaussian nuisance quotient
  + Newton identities/Rouche root counts
  + moment-cancelling real configurations
  + minimum-distance estimation/Gaussian testing/label covering
  -> global and separated-cluster calibrated moment minimax laws
```

The new orbit and expanding proofs do not depend on the retained scalar doubling theorem, positive-refresh filter theorem, finite-reference Bellman theorem, or any of the eleven historical spectral/LDP/operator gates. The new collision theorem uses only the retained exact nuisance quotient, not the retained assumed-contact theorem.

## Statements, assumptions, work, and scope

| Label | Hypotheses and actual proof | Quantifiers and boundary |
|---|---|---|
| `lem:v4-kernels` | Standard Borel observations and outputs; finite persistent register; inverse-distribution randomization of each time-indexed kernel | All independent public/private randomization is included. A data-dependent persistent seed position is charged. |
| `thm:v4-orbit` | IID renewal lengths of finite mean, independent fresh `(U,Y)` pairs, Borel `T`, bounded `f`; conditional orthogonality; truncated decoder strings; Cesaro renewal counts; explicit `(i,k)` chain | Lower bound for every randomized nonstationary machine with liminf average loss. Upper is stationary deterministic and uses `Nn+1`, not `N`, states. No computability of arbitrary Borel encoders is asserted. |
| `cor:v4-exponent` | Tail `W(n)<=A exp(-c n^beta)` and existence of a finite positive squared-quantization exponent; choose `n` of order `(log M)^(1/beta)` | Equality of exponents, not equality of constants or errors. Explicit logarithmic overhead under two-sided power bounds. Supremum excess version requires geometric renewal. |
| `prop:v4-closure` | Stationary deterministic autonomous no-data update; finitely many decoder rays | Exact characterization for this subclass. It is not a claim that random/nonstationary machines are always stationary-optimal. |
| `ex:v4-gap` | Two-point hidden space; every reset starts at 1; next no-reset step is 0; geometric resets | Orbit is deterministic and has one-centre error zero; a one-state output cannot retain the random indicator, giving `pq`. Two states attain zero. |
| `lem:v4-smallballs` | Haar torus; integer base; monotone posterior attenuation; `W(n)<=A w_n` | Before-wrap separation plus a volume bound covers arbitrary off-image Hilbert centres. Constants include actual state count `S_n`, not an uncharged precision register. |
| `thm:v4-noisy` | Integer `b>=2`, dimension `d>=1`, Haar resets, independent wrapped Gaussian acquisition, bounded mean residual lifetime | Matched profile for all budgets/noise levels; lower permits all randomized nonstationary machines. Exact suffix upper. Supremum raw assertion proved for geometric renewals through monotone age loss. |
| `cor:v4-noise-memory` | Previous hypotheses; posterior orthogonality and `Psi_w-Psi_v <= B/d` | A noise- and renewal-law-independent suffix decoder attains the raw-risk order. The excess-optimal decoder may use noise level. |
| `cor:v4-critical` | Geometric renewals, noiseless memory profile, `q_n=b^-2 exp(x/n)` | Uniform bounded-`x` Riemann-sum limit; exact coefficient for the suffix machine; only constant-factor profile for the optimum. Compact-`q` uniform constants; not uniform as `q` tends to 1. |
| `prop:v4-conjugacy` | Transport the whole experiment under Borel conjugacy; for changed readout use compact images and two-sided metric comparison | Exact transported risks; changed-readout raw risk factors `c^2/4,4C^2`. Does not identify nonlinear posterior excess risks. |
| `lem:v4-root-modulus` | Ordered real roots in a compact interval; first `d` power sums; optional known separated clusters | Newton recursion controls coefficients; Rouche on unions of disks preserves root multiplicities; sorting preserves maximum matching displacement. Exponents `1/d` and `1/r_j` derived, not assumed. |
| `lem:v4-root-testing` | Real-rooted monic polynomial with simple interior roots; small nonzero constant perturbation | Real roots persist by sign changes. Newton identities match moments through `r-1`; scale/translation make all first `d` discrepancies `O(h^r)` and root distance order `h`. |
| `thm:v4-roots` | Correlated Gaussian pair with unrestricted additive nuisance; fixed positive definite covariance shape; ordered-root or fixed cluster domain | Exact quotient; measurable minimum-distance upper; product-cover hard-M upper; two-point statistical lower; positive-volume representation lower. Uniform M/noise constants, not uniform dimension/gap/conditioning constants. |

## Retained results

All v3 `regenerative.tex` and `calibration.tex`, the byte-identical v2 quantitative body in v3 `retained-results.tex`, and the original foundational sections and appendices are compiled unchanged. Their mathematical labels must all resolve. The original v1/v2/v3 introductions, manifests, responses, and source editions remain in their original directories. The new introduction changes the reading order but does not remove a previous theorem or proof.

The exact nuisance quotient is needed in the new collision chain. The scalar checkpoint comparison is a complementary comparison, not the source of the new torus converse. The general causal-resolution, positive-refresh, acquisition, and control results have independent assumptions and are retained for completeness. A source-preservation check does not supply a missing mathematical review of them.

## Constant and asymptotic audit

1. General renewal realization needs finite mean only; exponent preservation adds a stretched-exponential age tail. These are distinct hypotheses.
2. Sharp torus bounds need `W(n)<=A w_n`; a claim for arbitrary heavy tails would exceed this proof.
3. Squared quantization exponent is used throughout; no unnoticed conversion from root-mean-square error changes a power.
4. The critical limit is in depth `n`, with exactly `S_n` suffix states. Arbitrary `M` uses `n_M` and retains the possible lattice constant oscillation.
5. The optimal critical prefactor is not identified by two-sided inequalities. Only the explicit suffix prefactor is proved.
6. Noise floor is the full-history Bayes risk; it is not a second encoding budget or a replacement observation.
7. The nonconstant-slope examples are genuine smooth conjugates, not a thermodynamic-pressure theorem for unrelated maps.
8. Root-cluster domains contain open sets of distinct roots, so the representation exponent is `2/d`; an exact multiplicity manifold would have a different dimension.
9. Root constants may deteriorate with small gaps, interval widths, large dimension, and covariance conditioning. The former contact theorem's constants remain conditional on controlled `lambda,Lambda`.

## Reproducibility versus proof

`verify.py` checks finite exact/rational identities and deterministic numerical regressions. Four deliberately wrong variants must fail both ordinary and optimized Python: uncharged age states, erased critical logarithm, omitted noise floor, and regularized collision exponent. These tests detect those regressions; they do not validate all quantifiers of the theorems. The build checks all hash-bound inputs, old source identities, resolved mathematical labels, and stable typesetting. Rendering checks inspect the resulting document. Independent mathematical refereeing is a separate step.
